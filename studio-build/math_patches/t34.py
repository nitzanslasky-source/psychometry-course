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
    cut_repeats(M)           # 2026-10-05
    renumber_pass(M)         # 2026-10-06 renumber pass: last


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


def _cr_drop_item(M, vid, n, k):
    """remove board item k of a slide, its APPEAR line and the spoken line right after it; later APPEARs follow."""
    b = M.slide(vid, n); b['items'].pop(k)
    def fn(lines):
        i = next(i for i, l in enumerate(lines) if l.get('appear') == k)
        del lines[i:i + 2]
        return [dict(l, appear=l['appear'] - 1) if l.get('appear') is not None and l['appear'] > k else l for l in lines]
    M.edit_lines(vid, n, fn)


def cut_repeats(M):
    # --- Polygons (geo-104): slide 5 "How many diagonals" = solve-q-r26-t34-02 (n − 3 from one vertex, n(n − 3),
    #     halve because each diagonal has two ends); slide 13 "Angle → sides" = solve-q-r26-t34-01 (the formula way and
    #     the fast way through the exterior angle). Slide 12 "Exterior angles" stays: the definition and the reason
    #     (walk around = 360) are not taught in a question video. The recap loses the two cut items.
    _cr_cut(M, MAIN, [5, 13])
    rec = len(M.video(MAIN)['beats'])
    k = next(i for i, it in enumerate(M.slide(MAIN, rec)['items']) if 'n-3' in it.get('t', ''))
    _cr_drop_item(M, MAIN, rec, k)
    for it in M.slide(MAIN, rec)['items']:
        if it.get('t', '').startswith('Exterior angles'): it['t'] = r'Exterior angles: $360°$ in all'
    M.edit_lines(MAIN, rec, lambda L: [dict(l, label='Exterior angles: 360° in all appears')
                                       if str(l.get('label', '')).startswith('Exterior angles') else l for l in L])
    _cr_say(M, MAIN, rec, 'And the exterior angles always add up to 360.', 'And the exterior angles always add up to 360.')

    # --- Polygons Meeting at a Point (r26-t34-meet): the whole lesson (hexagon + square: 360 around the point, then
    #     the isosceles triangle) is taught again right after by solve-q-r26-t34-03 (square + pentagon, same two
    #     steps). The lesson leaves the flow; its one extra fact (polygons that fill a point: 360, honeycomb) moves
    #     into the question video as one line.
    M.unplace('r26-t34-meet')
    _cr_say(M, 'solve-q-r26-t34-03', 1, 'A square and a pentagon on a common side',
            'A square and a pentagon on a common side — the exam loves this picture.')
    _cr_add(M, 'solve-q-r26-t34-03', 2, None,
            ["The same 360 tells you when regular polygons fill a point with no gaps: three hexagons, 3 times 120 — a honeycomb."],
            T(r'Fill a point: $3\times120°=360°$', size=30, x=1060, y=330, w=470),
            "'Fill a point: 3 × 120° = 360°' appears")


# ================================================================================================================
# 2026-10-06 renumber pass (runs LAST, after cut_repeats). The English course must not look like the Hebrew one:
# every Hebrew-derived question (guided geo34-g106 ... g117, practice geo34-core-p01 ... p20) gets new numbers (a
# changed story / new letters / new names where there is one); idea, trap, level and methods stay. Every guided
# solution video is rewritten to match, changed figures are redrawn or relabelled. Practice clean-up 34 -> 25.
# The English-made guided questions q-r26-t34-01 ... 03 stay. Nothing in topic 34 is recorded (checked
# ~/Documents/Course.recordings 2026-10-06), so RN_RECORDED is empty.
# ================================================================================================================
RN_RECORDED = set()
_RN_CW = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
_RN_WC = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
_RN_CHOICE = re.compile(r'\b([Cc]hoices? )((?:[1-4]|one|two|three|four)(?:(?:, | and | or )(?:[1-4]|one|two|three|four))*)\b')
GRAY = '#71818d'
ORANGE = '#bb6821'


def _rn_rx(old):
    e = re.escape(old)
    if old[0].isdigit(): e = r'(?:(?<![\d.A-Za-z/])|(?<=\\cdot)|(?<=\\times))' + e
    if old[-1].isdigit(): e = e + r'(?![\d.]\d)(?!\d)'
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
    and board item (the title slide's big 'Question N' stays). slides={n: (title or None, script)} rewrites slides
    first (their new text is still run through the choice permutation, so write their choice numbers in the NEW
    order and pass them with perm=None, or rewrite slide by slide)."""
    if vid in RN_RECORDED: return
    v = M.video(vid)
    for n, (title, script) in (slides or {}).items():
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, title=title, script=script)
    hits = set()
    for n, b in enumerate(v['beats'], 1):
        if slides and n in slides: continue          # already in the new numbers / new choice order
        if b['mode'] != 'title': b['title'] = _rn_text(b['title'], pairs, perm, hits)
        for l in b['lines']:
            for k in ('say', 'draw', 'label'):
                if k in l: l[k] = _rn_text(l[k], pairs, perm, hits)
        for it in b['items']:
            if it.get('t'): it['t'] = _rn_text(it['t'], pairs, perm, hits)
    miss = [o for o, _ in pairs if o not in hits]
    assert not miss, (vid, miss)
    M.touched_videos.add(vid)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_stem(M, qid, *pairs):
    s = M.q(qid)['stemRich']
    for o, n in pairs:
        assert o in s, (qid, o)
        s = s.replace(o, n)
    return s


def _rn_lbl(svg, mp):
    """rename <text> labels at once (each old label must exist)."""
    keep = {}
    for k, (o, n) in enumerate(mp.items()):
        tag = '>%s</text>' % o
        assert tag in svg, o
        svg = svg.replace(tag, '>\x00%d\x00</text>' % k); keep[k] = n
    return re.sub('\x00(\\d+)\x00', lambda m: keep[int(m.group(1))], svg)


def _rn_slide_figs(M, qid):
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for it in b['items']:
                if it.get('k') == 'q' and it.get('qid') == qid and it.get('fig'):
                    yield v, it


def _rn_relabel(M, qid, mp):
    """new letters on the question figure and on every copy of it on the solution slides."""
    M.set_q(qid, figure=_rn_lbl(M.q(qid)['questionVisual']['svg'], mp))
    for v, it in _rn_slide_figs(M, qid):
        it['fig'] = {'type': 'geometry', 'svg': _rn_lbl(it['fig']['svg'], mp)}
        M.touched_videos.add(v['id'])


def _rn_figure(M, qid, svg):
    """a redrawn figure: the question gets it in the 16:9 frame, every slide copy gets it cropped tight."""
    M.set_q(qid, figure=_zoom(svg))
    for v, it in _rn_slide_figs(M, qid):
        it['fig'] = {'type': 'geometry', 'svg': _crop_tight(svg)}
        M.touched_videos.add(v['id'])


def _rn_right(c, p, q, s=10.7):
    """right-angle mark at c between the rays c->p and c->q."""
    def u(t):
        dx, dy = t[0] - c[0], t[1] - c[1]; L = math.hypot(dx, dy); return dx / L * s, dy / L * s
    a, b = u(p), u(q)
    p1 = (c[0] + a[0], c[1] + a[1]); p2 = (p1[0] + b[0], p1[1] + b[1]); p3 = (c[0] + b[0], c[1] + b[1])
    return _line(p1, p2, TEAL, 1.7) + _line(p2, p3, TEAL, 1.7)


def _rn_side_lbl(p, q, txt, centre, d=20, size=20, color=INK):
    """label at the midpoint of side pq, pushed d px away from the shape's centre."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    nx, ny = -(q[1] - p[1]), q[0] - p[0]; L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
    if (mx - centre[0]) * nx + (my - centre[1]) * ny < 0: nx, ny = -nx, -ny
    return _t(mx + d * nx, my + d * ny, txt, size, color)


# ---------------------------------------------------------------- figures (same style as the existing ones)
def rn_fig_g106():
    """pentagon ABCDE: AB = BC = AE = 15, DE = 8, right angles at B, C, E (8-15-17)."""
    u = 15.3; bx, top = 530.0, 70.0
    A_, B_, C_ = (bx - 15 * u, top), (bx, top), (bx, top + 15 * u)
    D_ = (bx - 23 * u, top + 15 * u)
    E_ = (A_[0] - 3600 / 289 * u, A_[1] + 2415 / 289 * u)        # AE = 15, DE = 8, AD = 17
    P = [A_, B_, C_, D_, E_]; cen = (sum(x for x, _ in P) / 5, sum(y for _, y in P) / 5)
    b = _poly(P) + _rn_right(B_, A_, C_) + _rn_right(C_, B_, D_) + _rn_right(E_, A_, D_)
    b += (_rn_side_lbl(A_, B_, '15', cen) + _rn_side_lbl(B_, C_, '15', cen) + _rn_side_lbl(A_, E_, '15', cen)
          + _rn_side_lbl(E_, D_, '8', cen, 18))
    b += (_t(A_[0], A_[1] - 20, 'A') + _t(B_[0] + 15, B_[1] - 15, 'B') + _t(C_[0] + 15, C_[1] + 15, 'C')
          + _t(D_[0] - 10, D_[1] + 20, 'D') + _t(E_[0] - 18, E_[1] - 5, 'E'))
    return _svg('An irregular pentagon split into a square and two right triangles', b)


def rn_fig_g111():
    """regular 9-sided polygon ABCDEFGHI in its circle, all radii drawn, center O."""
    c, R = (320.0, 180.0), 107.353
    V = _reg(c[0], c[1], R, 9, 90)
    b = _poly(V)
    for k, nm in enumerate('ABCDEFGHI'):
        a = math.radians(90 + 40 * k)
        b += _t(c[0] + (R + 16.1) * math.cos(a), c[1] - (R + 16.1) * math.sin(a), nm)
    b += '<circle cx="320.000" cy="180.000" r="%.3f" fill="none" stroke="%s" stroke-width="2.5"/>' % (R, ORANGE)
    for p in V: b += _line(c, p, TEAL)
    b += '<circle cx="320.000" cy="180.000" r="3.2" fill="%s"/>' % INK
    b += _t(c[0] + 40 * math.cos(math.radians(-10)), c[1] - 40 * math.sin(math.radians(-10)), 'O')
    return _svg('Regular 9-sided polygon', b)


def rn_fig_g113():
    """regular hexagon with squares built outward on five of its six sides (not on the lower-right side)."""
    V = [(380.833, 180.0), (350.417, 127.317), (289.583, 127.317), (259.167, 180.0), (289.583, 232.683), (350.417, 232.683)]
    c = (320.0, 180.0); b = _poly(V)
    for k in range(5):
        p, q = V[k], V[k + 1]
        nx, ny = -(q[1] - p[1]), q[0] - p[0]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        if (mx - c[0]) * nx + (my - c[1]) * ny < 0: nx, ny = -nx, -ny
        b += _poly([p, q, (q[0] + nx, q[1] + ny), (p[0] + nx, p[1] + ny)], TEAL, FILL)
    return _svg('Five squares attached to sides of a regular hexagon', b)


def rn_fig_p04():
    """six regular hexagons around a hexagonal opening (a honeycomb ring)."""
    s = 42.0; c = (320.0, 180.0); b = ''
    for k in range(6):
        a = math.radians(30 + 60 * k); d = s * math.sqrt(3)
        b += _poly(_reg(c[0] + d * math.cos(a), c[1] - d * math.sin(a), s, 6, 0), INK, FILL)
    return _svg('Six regular hexagons surrounding a hexagonal opening', b)


def rn_fig_p08():
    """two regular octagons sharing one complete (vertical) side."""
    R = 95.0; ap = R * math.cos(math.radians(22.5))
    b = _poly(_reg(320 + ap, 180, R, 8, 22.5 + 180)) + _poly(_reg(320 - ap, 180, R, 8, 22.5))
    return _svg('Two regular octagons sharing one complete side', b)


def rn_fig_p15():
    """regular octagon with its radii; a congruent triangle attached on every other side; alpha at the top vertex."""
    c, R = (320.0, 180.0), 70.0
    V = _reg(c[0], c[1], R, 8, 90)
    b = _poly(V)
    for p in V: b += _line(c, p, GRAY, 1.5)
    for k in (0, 2, 4, 6):
        p, q = V[k], V[k + 1]
        b += _poly([p, q, (p[0] + q[0] - c[0], p[1] + q[1] - c[1])], TEAL, FILL)
    X = (V[0][0] + V[1][0] - c[0], V[0][1] + V[1][1] - c[1])
    b += _arc(V[0], V[7], X, 14)
    u1 = (V[7][0] - V[0][0], V[7][1] - V[0][1]); u2 = (X[0] - V[0][0], X[1] - V[0][1])
    n1, n2 = math.hypot(*u1), math.hypot(*u2)
    bis = (u1[0] / n1 + u2[0] / n2, u1[1] / n1 + u2[1] / n2); nb = math.hypot(*bis)
    b += _t(V[0][0] + 27 * bis[0] / nb, V[0][1] + 27 * bis[1] / nb, 'α', 18, TEAL)
    return _svg('Congruent isosceles triangles attached to a regular octagon', b)


def rn_fig_p16():
    """pentagon = rectangle BCDE (BC = 2a) + isosceles triangle ABE (AB = AE = 6a, angle A = 120°)."""
    k = 40.0; yB = 190.0; hw = 3 * math.sqrt(3) * k
    A_, B_, E_ = (320.0, yB - 3 * k), (320 - hw, yB), (320 + hw, yB)
    C_, D_ = (B_[0], yB + 2 * k), (E_[0], yB + 2 * k)
    cen = (320.0, yB)
    b = _poly([A_, B_, C_, D_, E_]) + _line(B_, E_, TEAL)
    b += (_t(A_[0], A_[1] - 20, 'A') + _t(B_[0] - 20, B_[1], 'B') + _t(C_[0] - 13, C_[1] + 17, 'C')
          + _t(D_[0] + 13, D_[1] + 17, 'D') + _t(E_[0] + 20, E_[1], 'E'))
    b += _arc(A_, B_, E_, 38) + _t(A_[0], A_[1] + 62, '120°', 18, TEAL)
    b += _rn_side_lbl(A_, B_, '6a', cen) + _rn_side_lbl(A_, E_, '6a', cen) + _t(B_[0] - 20, yB + k, '2a')
    return _svg('An isosceles roof triangle on a rectangle', b)


# ---------------------------------------------------------------- guided questions and their videos
def rn_guided(M):
    # ---------- g106: 5-12-13, AB = BC = AE = 12, DE = 5 -> 204  ==>  8-15-17, 15 / 8 -> 225 + 60 + 60 = 345
    g = 'geo34-g106'
    _rn_q(M, g, _rn_stem(M, g, ('AB=BC=AE=12', 'AB=BC=AE=15'), ('DE=5', 'DE=8')),
          ['$465$', '$345$', '$405$', '$285$'], 2, [
        "Draw $AD$. Triangle $AED$ has a right angle at $E$ and legs $15$ and $8$. Its area is $\\frac{15\\cdot8}{2}=60$, and $AD=17$ (the 8-15-17 triple).",
        "Drop the height $AH$ to $CD$. $ABCH$ is a square with side $15$. Its area is $15^2=225$.",
        "Triangle $AHD$ has hypotenuse $AD=17$ and leg $AH=15$, so $DH=8$. Its area is $\\frac{15\\cdot8}{2}=60$.",
        "Total: $225+60+60=345$."])
    _rn_figure(M, g, rn_fig_g106())
    _rn_video(M, 'solve-' + g, [('12', '15'), ('5', '8'), ('13', '17'), ('30', '60'), ('144', '225'), ('204', '345'),
                                ('174', '285')], {1: 1, 2: 3, 3: 2, 4: 4})

    # ---------- g107: side 8 -> 96√3  ==>  side 12 -> one triangle 36√3, six 216√3 (trap: one triangle)
    g = 'geo34-g107'
    _rn_q(M, g, _rn_stem(M, g, ('side length 8 cm', 'side length 12 cm')),
          ['$36\\sqrt3$', '$144\\sqrt3$', '$432\\sqrt3$', '$216\\sqrt3$'], 4, [
        "The three long diagonals split the hexagon into 6 equilateral triangles with side $12$.",
        "One triangle: $\\frac{12^2\\sqrt3}{4}=\\frac{144\\sqrt3}{4}=36\\sqrt3$.",
        "Six triangles: $6\\cdot36\\sqrt3=216\\sqrt3$."])
    _rn_video(M, 'solve-' + g, [('8', '12'), ('64', '144'), ('16', '36'), ('96', '216')], {1: 4, 2: 1, 3: 2, 4: 3})

    # ---------- g108: octagon side 5 -> 50 + 50√2  ==>  side 10 -> 100 + 100 + 200√2 = 200 + 200√2
    g = 'geo34-g108'
    _rn_q(M, g, _rn_stem(M, g, ('side length 5 cm', 'side length 10 cm')),
          ['$200+200\\sqrt2$', '$200+100\\sqrt2$', '$400$', '$100+100\\sqrt2$'], 1, [
        "Split the octagon: a square in the middle, 4 rectangles and 4 corner right isosceles triangles.",
        "Square: $10^2=100$.",
        "Each corner triangle has hypotenuse $10$, so its legs are $\\frac{10}{\\sqrt2}=5\\sqrt2$. Its area is $\\frac12\\cdot5\\sqrt2\\cdot5\\sqrt2=25$. Four triangles: $100$.",
        "Each rectangle: $10\\cdot5\\sqrt2=50\\sqrt2$. Four rectangles: $200\\sqrt2$.",
        "Total: $100+100+200\\sqrt2=200+200\\sqrt2$."])
    s3 = [
        A('Square: 10² = 100 appears', T('Square: $10^2=100$', size=38, x=1060, y=280, w=470)),
        "The square in the middle: side 10 — 100. That's clear.",
        "The four triangles together — they're equal to the square.",
        A('4 triangles = square = 100 appears', T('4 triangles $=$ square $=100$', size=38, x=1060, y=350, w=470)),
        "If we took them and put them inside the square, they'd make exactly the square.",
        "And that's true in EVERY regular octagon — always. Each triangle is exactly a quarter of the square.",
        D('Write 25 in each corner triangle'),
        "So each one is 100 over 4 — 25."]
    s4 = [
        "The rectangle: one side I know — it's a side of the octagon, 10.",
        "The other side I don't know. But it's the leg of the corner triangle.",
        "Hypotenuse 10, and it's a silver triangle — from the hypotenuse to the leg, divide by root 2.",
        A('10 ÷ √2 = 5√2 appears', T('$\\frac{10}{\\sqrt2}=\\frac{10\\sqrt2}{2}=5\\sqrt2$', size=40, x=1060, y=280, w=470)),
        D('Write 5√2 on the short side of one rectangle'),
        "10 over root 2 — 10 root 2 over 2. That's 5 root 2.",
        A('Rectangle: 10 · 5√2 = 50√2 appears', T('Rectangle: $10\\cdot5\\sqrt2=50\\sqrt2$', size=36, x=1060, y=360, w=470)),
        "So one rectangle is 10 times 5 root 2 — 50 root 2.",
        A('4 rectangles = 200√2 appears', T('4 rectangles $=200\\sqrt2$', size=38, x=1060, y=440, w=470)),
        "Four of them — 200 root 2."]
    s5 = [
        A('100 + 100 + 200√2 = 200 + 200√2 appears', T('$100+100+200\\sqrt2=200+200\\sqrt2$', size=34, x=1060, y=280, w=470)),
        "The whole octagon: 100, plus 100 for the triangles, plus 4 rectangles — 200 root 2.",
        "Total: 200 plus 200 root 2.",
        D('Circle choice 1'),
        "Choice one.",
        "Notice — there's a pattern here that's ALWAYS true in a regular octagon.",
        A('S = 2a² + 2a²√2 appears', T('$S=2a^2+2a^2\\sqrt2$', size=40, x=1060, y=360, w=470)),
        "The area of a regular octagon is always 2a squared plus 2a squared root 2. a is the octagon's side.",
        "So instead of remembering a formula: the square in the middle is just the side squared — 100.",
        "Take it twice — 200. Then write the same number again, this time with root 2. 200 plus 200 root 2.",
        A('Side 3 → 18 + 18√2 · side 7 → 98 + 98√2 appears',
          T('$3\\rightarrow18+18\\sqrt2$ · $7\\rightarrow98+98\\sqrt2$', size=32, x=1060, y=440, w=470)),
        "Side 3: the square is 9, twice — 18. 18 plus 18 root 2. Side 7: 49, twice — 98. 98 plus 98 root 2."]
    s6 = [
        "Notice — this split is ALWAYS useful, even when they don't ask for the whole octagon.",
        "Sometimes they ask for just part of it — only the middle, only the triangles, anything.",
        "Split it like this and you find any part almost without calculating.",
        D('Shade the cross: the middle square and the four rectangles'),
        "Say they ask for this cross in the middle.",
        A('Cross = 200 + 200√2 − 100 = 100 + 200√2 appears',
          T('Cross $=200+200\\sqrt2-100$ $=100+200\\sqrt2$', size=32, x=1060, y=280, w=470)),
        "Take the whole octagon, 200 plus 200 root 2, and remove the triangles on the sides — 100.",
        "The cross: the plain number only once — 100 — and the 200 root 2 of the rectangles.",
        D('Cross out choice 2'),
        "And that's how you spot the traps: 200 plus 100 root 2 — someone counted only half the rectangles."]
    _rn_video(M, 'solve-' + g, [('side length 5', 'side length 10'), ('octagon — 5.', 'octagon — 10.')], None,
              {3: (None, s3), 4: (None, s4), 5: (None, s5), 6: (None, s6)})

    # ---------- g110: letter-only: pentagon ABCDE, angle ADB  ==>  pentagon PQRST, angle PSQ; new choice order
    g = 'geo34-g110'
    _rn_q(M, g, 'PQRST is a regular pentagon. What is the size of angle PSQ (marked $x$ in the figure)?',
          ['$72°$', '$108°$', '$36°$', '$54°$'], 3, [
        "Each angle of a regular pentagon is $\\frac{540°}{5}=108°$.",
        "Triangle $QRS$ is isosceles ($RQ=RS$) with vertex angle $108°$, so $\\angle QSR=\\frac{180°-108°}{2}=36°$. In the same way, $\\angle TSP=36°$.",
        "$x=\\angle PSQ=108°-36°-36°=36°$."])
    _rn_relabel(M, g, {'A': 'P', 'B': 'Q', 'C': 'R', 'D': 'S', 'E': 'T'})
    s2 = [
        'PQRST is a regular pentagon. What is angle PSQ?',
        'Why several ways? Because we can cut a polygon into shapes we know — triangles, quadrilaterals — and work with diagonals.',
        'Way one: through triangle SRQ.',
        'Regular polygon — all sides equal. So SR equals RQ. The triangle is isosceles.',
        'What do we know about angle R? The angle sum of a pentagon is 540. Five equal angles —',
        A('540 ÷ 5 = 108° appears', T('$\\frac{540°}{5}=108°$', size=40, x=1060, y=250, w=470)),
        '— 540 divided by 5: every angle is 108. Know this by heart!',
        D('Write 108° at R'),
        'So R is 108. And so are P, Q, T — and the whole angle at S.',
        A('(180 − 108) ÷ 2 = 36° appears', T('$\\frac{180°-108°}{2}=36°$', size=34, x=1060, y=330, w=470)),
        'Isosceles triangle, vertex angle 108. The two base angles together: 72. Each one — 36.',
        D('Write 36° at angle QSR'),
        'Same thing on the other side: triangle STP — sides ST and TP equal, vertex 108.',
        D('Write 36° at angle TSP'),
        'So angle TSP is 36 too.',
        A('x = 108 − 36 − 36 = 36° appears', T('$x=108°-36°-36°=36°$', size=34, x=1060, y=410, w=470)),
        'The whole angle at S is 108. Take away 36 and 36 — the middle piece is 36.',
        D('Circle choice 3'),
        'Choice three. A simple way — through the triangle.']
    s3 = [
        'Way two: through the trapezoid.',
        D('Shade quadrilateral PQST'),
        "PQST is a trapezoid. If you didn't know — now you do:",
        A('One diagonal → isosceles trapezoid + triangle appears',
          T('In a regular pentagon, one diagonal cuts off a triangle and leaves an isosceles trapezoid.', size=34, x=1060, y=250, w=470)),
        'In every regular pentagon, one diagonal gives an isosceles trapezoid and a triangle.',
        "Angles P and T — the trapezoid's top base angles — are 108 each: pentagon angles.",
        "The legs are equal, so it's isosceles — and the bottom base angles are equal too.",
        A('180 − 108 = 72° appears', T('$\\angle TSQ=180°-108°=72°$', size=34, x=1060, y=420, w=470)),
        'Top angle plus bottom angle on the same leg: 180. So the bottom angle TSQ is 72.',
        D('Write 72° at angle TSQ'),
        "TSQ is 72. The small angle TSP we found: 36. What's left for the middle — 36.",
        D('Circle choice 3'),
        'Same answer. Choice three.']
    s4 = [
        'Way three: through the diagonals.',
        'In a regular polygon the diagonals are symmetric. From S we can draw only two: to Q and to P. S to R and S to T are sides.',
        "The diagonals from one vertex split its angle into EQUAL pieces. Let's prove it once.",
        D('Draw the circle through all five vertices'),
        'Every regular polygon can be inscribed in a circle.',
        'The three small angles at S rest on the chords QR, PQ and PT — sides of the pentagon. Equal chords.',
        A('Equal chords → equal inscribed angles appears', T('Inscribed angles on equal chords are equal.', size=34, x=1060, y=250, w=470)),
        'Inscribed angles on equal chords are equal. Call each one x.',
        D('Write x in each of the three pieces at S'),
        A('3x = 108° appears', T('$3x=108°$', size=40, x=1060, y=400, w=470)),
        'Three x together: the whole angle at S — 108.',
        A('108 = 90 + 18 → 30 + 6 = 36 appears', T('$108=90+18\\ \\rightarrow\\ 30+6=36$', size=34, x=1060, y=470, w=470)),
        '108 divided by 3? Split it into something easy: 90 plus 18. 90 over 3 is 30, 18 over 3 is 6. 36.',
        D('Circle choice 3'),
        'The middle angle is x — 36. Choice three.',
        'Three ways: the triangle, the trapezoid, the diagonals. These are the common ways for questions like this.']
    _rn_video(M, 'solve-' + g, slides={2: (None, s2), 3: (None, s3), 4: (None, s4)})

    # ---------- g111: regular octagon, false "perimeter = 8r"  ==>  regular 9-sided polygon, false "perimeter = 9r"
    #            (central 40°, base angles 70°: the side faces 40°, the radius 70°)
    g = 'geo34-g111'
    _rn_q(M, g, 'A regular 9-sided polygon ABCDEFGHI is inscribed in a circle with center O and radius r. Which of the following statements is not true?',
          ['The circumference of the circle is greater than the perimeter of the polygon.', 'Angle AOB equals angle GOH.',
           'The perimeter of the polygon is $9r$.', 'Angle BCO equals angle OCD.'], 3, [
        "Statement 2 is true: every central angle is $\\frac{360°}{9}=40°$.",
        "Statement 1 is true: each arc is longer than its chord (the side), so the circumference is greater than the perimeter.",
        "Statement 4 is true: triangles $OBC$ and $OCD$ have three pairs of equal sides, so they are congruent and $\\angle BCO=\\angle OCD$.",
        "Statement 3 is false: triangle $OCD$ has the angles $40°$, $70°$ and $70°$. The side $CD$ faces $40°$ and a radius faces $70°$, so $CD<r$ and the perimeter is less than $9r$."])
    _rn_figure(M, g, rn_fig_g111())
    _rn_video(M, 'solve-' + g, [
        ('regular octagon', 'regular 9-sided polygon'), ('octagon', 'polygon'), ('8r', '9r'), ('8', '9'), ('45', '40'),
        ('135', '140'), ('67 and a half', '70'), ('67.5', '70'), ('eight', 'nine'),
        ("Eight sides — the same. That's our question.", "Eight sides — the same. Nine sides — that's our question.")],
        {1: 4, 2: 3, 3: 2, 4: 1})

    # ---------- g112: perimeter of ACE 30 -> 20√3  ==>  42 -> AC 14 -> AB 14/√3 -> 84/√3 = 28√3
    #            (estimates: 24√3 < 24 · 1.75 = 42, 24√2 ≈ 34, 28√2 < 28 · 1.5 = 42, 28√3 > 42)
    g = 'geo34-g112'
    _rn_q(M, g, _rn_stem(M, g, ('ACE is 30 cm', 'ACE is 42 cm')),
          ['$24\\sqrt2$', '$28\\sqrt3$', '$24\\sqrt3$', '$28\\sqrt2$'], 2, [
        "The three corner triangles are congruent, so triangle $ACE$ is equilateral: $AC=\\frac{42}{3}=14$.",
        "Triangle $ABC$ is isosceles with vertex angle $120°$. The height from $B$ splits $AC$ into $7$ and $7$ and makes two 30-60-90 triangles.",
        "In each one the long leg is $7$, so the short leg is $\\frac{7}{\\sqrt3}$ and the hypotenuse is $AB=\\frac{14}{\\sqrt3}$.",
        "Perimeter: $6\\cdot\\frac{14}{\\sqrt3}=\\frac{84}{\\sqrt3}=28\\sqrt3$."])
    s2 = [
        'ABCDEF is a regular hexagon. The perimeter of triangle ACE is 42. What is the perimeter of the hexagon?',
        "First, the math solution. We need to see that ACE is equilateral. Let's prove it once — from now on, you know it.",
        A('720 ÷ 6 = 120° appears', T('$\\frac{720°}{6}=120°$', size=40, x=1060, y=250, w=470)),
        'The angle sum of a hexagon is 720 — each angle 720 over 6: 120. Know it by heart.',
        D('Write 120° at B'),
        'Triangle ABC: isosceles — hexagon sides. The base angles together: 60. Each one: 30.',
        D('Write 30° at A and at C inside triangle ABC'),
        'Same in triangle AFE, and in triangle CDE: 30 and 30.',
        A('120 − 30 − 30 = 60° appears', T('$120°-30°-30°=60°$', size=34, x=1060, y=330, w=470)),
        'The angle of the triangle at A: 120, minus 30, minus 30 — 60. Same at C and at E.',
        'All angles 60: equilateral. Proved.',
        'Or by symmetry: all three corner triangles are congruent, so the three diagonals are equal.',
        A('42 ÷ 3 = 14 appears', T('$AC=\\frac{42}{3}=14$', size=40, x=1060, y=420, w=470)),
        'The perimeter is 42, so each side of the triangle is 14.',
        D('Write 14 on AC, CE and EA')]
    s3 = [
        "Now from the triangle's side to the hexagon's side. Work in triangle ABC.",
        D('Drop the altitude from B to AC; mark H'),
        'Isosceles — so the altitude is also a median and an angle bisector.',
        D('Write 60° and 60° at B, 7 and 7 on AH and HC'),
        'It splits 120 into 60 and 60, and 14 into 7 and 7.',
        "60, 90 — the angle at A is 30. That's not just a right triangle: it's a golden triangle.",
        A('AB = 14/√3 appears', T('$AH=7\\ \\rightarrow\\ \\frac{7}{\\sqrt3}\\ \\rightarrow\\ AB=\\frac{14}{\\sqrt3}$', size=34, x=1060, y=250, w=470)),
        "7 faces 60 — it's the long leg. To the short leg: divide by root 3. To the hypotenuse: double. AB is 14 over root 3.",
        A('P = 6 · 14/√3 = 28√3 appears', T('$P=6\\cdot\\frac{14}{\\sqrt3}=\\frac{84}{\\sqrt3}=28\\sqrt3$', size=34, x=1060, y=350, w=470)),
        'Six sides: 84 over root 3. Ignore the root, 84 over 3 is 28, attach the root — 28 root 3.',
        D('Circle choice 2'),
        "Choice two. That's the math solution.",
        'Remember this for later: in a regular hexagon, the short diagonal is the side times root 3. Here: 14 over root 3, times root 3 — 14.',
        'And the long diagonal, through the center, is twice the side.']
    s4 = [
        'Now the psychometric solution — estimating the size.',
        "The hexagon's perimeter MUST be bigger than the triangle's. Why?",
        D('Mark AF, FE and AE'),
        'In triangle AFE: AF plus FE is greater than AE — two sides are always greater than the third.',
        "Same in the other two corner triangles. So the hexagon's perimeter is greater than 42.",
        A('P > 42 appears', T('$P>42$', size=44, x=1060, y=250, w=470)),
        'Now to the answers — on the exam they usually help us.',
        A('√3 ≈ 1.7, √2 ≈ 1.4 appears', T('$\\sqrt3\\approx1.7\\quad\\sqrt2\\approx1.4$', size=38, x=1060, y=330, w=470)),
        '24 root 3: 24 times 1.7 — about 41. Less than 42 — out.',
        D('Cross out choice 3'),
        "It's close — if you want to be sure: root 3 is less than 1.75, and 24 times 1.75 is exactly 42. So 24 root 3 is under 42.",
        '24 root 2: about 24 times 1.4 — around 34. Out.',
        D('Cross out choice 1'),
        A('28 × 1.5 = 42 appears', T('$28\\times1.5=42$', size=38, x=1060, y=410, w=470)),
        "28 root 2 — 28 times 1.4 isn't hard, but here's a trick: multiply by something easy, 1.5. 28 times 1.5 is 42.",
        'Root 2 is less than 1.5, so 28 root 2 is less than 42. Out.',
        D('Cross out choice 4'),
        "And 28 root 3: root 3 is more than 1.5, so it's more than 42. Possible.",
        D('Circle choice 2'),
        'Three out — choice two.']
    _rn_video(M, 'solve-' + g, [], {1: 3, 2: 1, 3: 4, 4: 2}, {2: (None, s2), 3: (None, s3), 4: (None, s4)})

    # ---------- g112-area: hexagon side 6 -> 3 corner triangles 27√3  ==>  side 10 -> 3 · 25√3 = 75√3
    g = 'geo34-g112-area'
    _rn_q(M, g, _rn_stem(M, g, ('side 6 cm', 'side 10 cm')),
          ['$25\\sqrt3$', '$150\\sqrt3$', '$75\\sqrt3$', '$50\\sqrt3$'], 3, [
        "Each corner triangle ($ABC$, $CDE$, $EFA$) is $\\frac16$ of the hexagon: the same area as an equilateral triangle with side $10$, $\\frac{10^2\\sqrt3}{4}=25\\sqrt3$.",
        "Three triangles: $3\\cdot25\\sqrt3=75\\sqrt3$ (half of the hexagon, $150\\sqrt3$)."])
    s2 = [
        'A regular hexagon with side 10. What is the sum of the areas of triangles ABC, CDE and EFA — the shaded area?',
        'The full way: drop an altitude in a corner triangle and work with 30, 60, 90.',
        D('Drop the altitude from B to AC'),
        'The legs are 10, the vertex is 120 — the altitude makes two golden triangles with hypotenuse 10.',
        A('Short leg 5, long leg 5√3 appears', T('Short leg $5$, long leg $5\\sqrt3$', size=34, x=1060, y=250, w=470)),
        "Short leg: 5 — that's the height. Long leg: 5 root 3 — so the base is 10 root 3.",
        A('10√3 · 5 ÷ 2 = 25√3 appears', T('$\\frac{10\\sqrt3\\cdot5}{2}=25\\sqrt3$', size=40, x=1060, y=330, w=470)),
        'Base times height over 2: 25 root 3. Times three triangles.',
        A('3 · 25√3 = 75√3 appears', T('$3\\cdot25\\sqrt3=75\\sqrt3$', size=40, x=1060, y=420, w=470)),
        "75 root 3. It works — but it's long.",
        D('Circle choice 3'),
        'Choice three.']
    s3 = [
        'Now the understanding way.',
        'Each shaded triangle is one sixth of the hexagon — the same area as an equilateral triangle with side 10.',
        A('S = 3 · 10²√3/4 appears', T('$S=3\\cdot\\frac{10^2\\sqrt3}{4}$', size=40, x=1060, y=250, w=470)),
        'So: three times 10 squared root 3 over 4.',
        A('= 3 · 25√3 = 75√3 appears', T('$=3\\cdot25\\sqrt3=75\\sqrt3$', size=40, x=1060, y=340, w=470)),
        '100 over 4 is 25. Three times 25 root 3 — 75 root 3.',
        D('Circle choice 3'),
        'Choice three. No altitudes, no golden triangles.']
    _rn_video(M, 'solve-' + g, slides={2: (None, s2), 3: (None, s3)})

    # ---------- g113: 4 squares, Maya "3 ×" (false), Daniel "areas bigger" (true)
    #            ==>  5 squares, Ella "3 ×" (20 sides vs 18, false), Adam "areas bigger" (true); plug in side 1
    g = 'geo34-g113'
    _rn_q(M, g, ' Five squares are constructed externally on five sides of a regular hexagon. Ella claims that the sum of the five square perimeters is 3 times the hexagon perimeter. Adam claims that the sum of the five square areas is greater than the hexagon area. Which of the following is true? ',
          ['Only Ella is correct.', 'Both are correct.', 'Neither is correct.', 'Only Adam is correct.'], 4, [
        "Plug in a number: side $=1$.",
        "Ella: the five squares have perimeter $5\\cdot4=20$. The hexagon has perimeter $6\\cdot1=6$, and $3\\cdot6=18\\ne20$. Ella is wrong.",
        "Adam: the five squares have area $5\\cdot1=5$. The hexagon has area $6\\cdot\\frac{1^2\\sqrt3}{4}=\\frac{3\\sqrt3}{2}<\\frac{3\\cdot2}{2}=3<5$. Adam is right.",
        "Only Adam is correct."])
    _rn_figure(M, g, rn_fig_g113())
    s2 = [
        "Squares on five sides of a regular hexagon. Ella: the square perimeters are 3 times the hexagon's. Adam: the square areas are bigger than the hexagon's.",
        'Is Ella right? Is Adam? Both, or neither?',
        "The full solution — but instead of x, we plug in a number. The hexagon side is also the square side. What's simpler than 1? Let it be 1.",
        A('Squares: 5 · 4 = 20 appears', T('Squares: $5\\cdot4=20$', size=38, x=1060, y=340, w=470)),
        'One square: 4 sides of 1 — perimeter 4. Five squares: 20.',
        A('Hexagon: 6 · 1 = 6 appears', T('Hexagon: $6\\cdot1=6$', size=38, x=1060, y=410, w=470)),
        'The hexagon: 6 sides of 1 — 6.',
        '3 times 6 is 18 — not 20. Ella is wrong.',
        D('Cross out choices 1 and 2'),
        "So we can already eliminate two answers: 'only Ella' and 'both correct'.",
        "Why do this first? If we're out of time, at least we've doubled our chances.",
        A('Squares: 5 · 1 = 5 appears', T('Squares: $5\\cdot1=5$', size=38, x=1060, y=480, w=470)),
        'Now Adam. One square: 1 squared, 1. Five squares: 5.',
        A('Hexagon: 6 · 1²√3/4 = 3√3/2 appears', T('Hexagon: $6\\cdot\\frac{1^2\\sqrt3}{4}=\\frac{3\\sqrt3}{2}$', size=38, x=1060, y=560, w=470)),
        'The hexagon: six equilateral triangles with side 1. Six times 1 squared root 3 over 4 — 3 root 3 over 2.',
        '5 or 3 root 3 over 2? No need to calculate — just estimate. Root 3 is less than 2, so 3 root 3 over 2 is less than 3 — less than 5.',
        'Adam is right.',
        D('Circle choice 4'),
        'Only Adam — choice four. The full, standard solution.']
    s3 = [
        'Another solution — geometric understanding.',
        'Ella first. No x, no numbers — just count sides.',
        A('20 sides vs 18 appears', T('$5\\cdot4=20$ sides vs $3\\cdot6=18$', size=38, x=1060, y=340, w=470)),
        'Each square has 4 sides — five squares: 20. The hexagon has 6. All the same length.',
        "3 times 6 is 18 — not 20. Ella is wrong.",
        'Adam is the trickier part. We need to cut the hexagon in a smart way:',
        D('Split the hexagon into three rhombi'),
        'Into three rhombi. Now: which is bigger — one rhombus or one square?',
        "Both have all sides equal. What's different? In the square every angle is 90. In the rhombus this angle is sharper.",
        'Squeeze the angle — the opening shrinks and shrinks, down to zero. Straighten it towards 90 — the area grows.',
        A('Same sides: square > rhombus appears', T('Same sides: the square always has the most area.', size=34, x=1060, y=450, w=470)),
        'Same perimeter — but the square always has more area. It uses its sides in the best way.',
        'So three squares are already bigger than the three rhombi — the hexagon. And we have five squares.',
        D('Circle choice 4'),
        'Adam is right, Ella is wrong. Choice four.']
    _rn_video(M, 'solve-' + g, slides={2: (None, s2), 3: (None, s3)})
    v = M.video('solve-' + g); v['title'] = v['navLabel'] = 'Five attached squares: compare perimeter and area'

    # ---------- g114: letter-only (AE = 1 plug-in): AB ⊥ CD at E, Lina / Noam  ==>  KL ⊥ MN at T, Sara / Ben
    g = 'geo34-g114'
    _rn_q(M, g, ' The accompanying figure shows a regular octagon. KL and MN are perpendicular and intersect at T. K, L, M and N are vertices of the octagon, as shown in the figure. Sara claims that $LT>2KT$. Ben claims that the perimeter of triangle KMT equals MN. Which of the following is true? ',
          ['Only Ben is correct.', 'Both are correct.', 'Only Sara is correct.', 'Neither is correct.'], 2, [
        "Let $KT=MT=1$. Triangle $KMT$ is right isosceles, so $KM=\\sqrt2$. All the octagon sides are $\\sqrt2$.",
        "Sara: $LT=\\sqrt2+1\\approx2.4$ and $2KT=2$. $LT>2KT$, so Sara is correct.",
        "Ben: the perimeter of $KMT$ is $1+1+\\sqrt2=2+\\sqrt2$, and $MN=1+\\sqrt2+1=2+\\sqrt2$. They are equal, so Ben is correct.",
        "Both are correct."])
    _rn_relabel(M, g, {'A': 'K', 'B': 'L', 'C': 'M', 'D': 'N', 'E': 'T'})
    s2 = [
        'A regular octagon. KL and MN are perpendicular and meet at T. Sara: LT is greater than 2KT. Ben: the perimeter of triangle KMT equals MN.',
        'Whichever way we choose, first we must split the octagon the right way — as we learned.',
        D('Complete the partition lines'),
        'What do we get? A square, four silver triangles — together equal to the square —',
        "— and four rectangles. Very, very important to know this partition, and to draw it when it's not drawn."]
    s3 = [
        'Way one: plug in numbers.',
        "We could plug a number into the octagon's side — but then to get KT we'd divide by root 2. We'd rather multiply.",
        "So plug in KT. What's simpler than 1?",
        D('Write 1 on KT and on MT'),
        A('KT = MT = 1, KM = √2 appears', T('$KT=MT=1,\\ KM=\\sqrt2$', size=38, x=1060, y=340, w=470)),
        'KT is 1, so MT is 1 — a silver triangle. KM, the hypotenuse, is root 2 times bigger: root 2.',
        D("Write √2 on the square's side and 1 on the bottom corner leg"),
        "KM is an octagon side — so all sides are root 2, and so is the square's side. And the corner triangle at the bottom: leg 1.",
        A('LT = 1 + √2, 2KT = 2 appears', T('$LT=1+\\sqrt2,\\quad 2KT=2$', size=38, x=1060, y=410, w=470)),
        'Sara: LT is from T down to L — root 2 plus 1. Twice KT is 2.',
        '1 plus 1.4 against 2 — LT is bigger. Sara is right.',
        D('Cross out choices 1 and 4'),
        "Eliminate every answer that says otherwise: 'only Ben' and 'neither'.",
        A('P(KMT) = 2 + √2 = MN appears', T('$P_{KMT}=2+\\sqrt2=MN$', size=38, x=1060, y=480, w=470)),
        'Ben: triangle KMT — 1 plus 1 plus root 2: 2 plus root 2. MN: 1, plus root 2, plus 1 — also 2 plus root 2.',
        'Equal — Ben is right too.',
        D('Circle choice 2'),
        'Both are correct. Choice two.']
    s4 = [
        'Way two: estimate — and know the octagon.',
        D('Mark KT and the bottom corner leg of LT'),
        'Sara compares 2KT with LT. One KT is the same as the bottom leg on LT — the silver-triangle legs are equal.',
        "Cancel them. What's left? One KT — against the square's side.",
        "Which is bigger? The square's side is an octagon side — the hypotenuse of a corner triangle. KT is only a leg.",
        A('Square side = hypotenuse > leg KT appears', T('Square side $=$ hypotenuse $>$ leg $KT$', size=34, x=1060, y=340, w=470)),
        'In a right triangle the hypotenuse is always the longest side. So LT is more than 2KT.',
        'Sara is right.',
        'Ben: here we just need to know which piece cancels which.',
        'MT is on both sides — cancel it. KT is the same as the leg on the left of MN. KM is an octagon side — the same as the middle of MN.',
        D('Circle choice 2'),
        'Everything cancels — Ben is right too. Choice two.']
    _rn_video(M, 'solve-' + g, slides={2: (None, s2), 3: (None, s3), 4: (None, s4)})

    # ---------- g115: white rectangle 8 + 8√2 -> shaded the same  ==>  12 + 12√2
    g = 'geo34-g115'
    _rn_q(M, g, _rn_stem(M, g, ('$8+8\\sqrt2$', '$12+12\\sqrt2$')),
          ['$12+12\\sqrt2$', '$6+12\\sqrt2$', '$12+24\\sqrt2$', '$24+24\\sqrt2$'], 1, [
        "Split the octagon the standard way: a middle square, 4 congruent rectangles and 4 corner triangles. The 4 triangles together equal the middle square.",
        "White: the middle square $+$ 2 rectangles.",
        "Shaded: 4 triangles $+$ 2 rectangles $=$ (the middle square) $+$ 2 rectangles.",
        "The shaded area equals the white area: $12+12\\sqrt2$."])
    _rn_video(M, 'solve-' + g, [('8 plus 8 root 2', '12 plus 12 root 2')], {1: 2, 2: 3, 3: 4, 4: 1})

    # ---------- g116: angle sum 1,620° -> 11 sides  ==>  1,440° -> 10 sides (trap 8 = 1440/180)
    g = 'geo34-g116'
    _rn_q(M, g, _rn_stem(M, g, ('1,620°', '1,440°')), ['$9$', '$11$', '$10$', '$8$'], 3, [
        "$180(n-2)=1440$. Divide by $180$: $n-2=8$, so $n=10$.",
        "Or use an anchor: the octagon has $1080°$. Each extra side adds $180°$: $1260°$ (9 sides), $1440°$ (10 sides).",
        "($8$ is the trap: $\\frac{1440}{180}=8$ is $n-2$, not $n$.)"])
    s2 = [
        'The sum of the interior angles of a polygon is 1,440. How many sides?',
        'Two ways: the math way, and an understanding way through an anchor.',
        'The formula: the angle sum is 180 times n minus 2 — n is the number of sides.',
        A('180(n − 2) = 1440 appears', T('$180(n-2)=1440$', size=40, x=410, y=260, w=1100)),
        'We could open the brackets — but we want the smallest numbers possible. Simplify first.',
        A('18(n − 2) = 144 appears', T('$18(n-2)=144$', size=40, x=410, y=330, w=1100)),
        'Both divide by 10.',
        A('9(n − 2) = 72 appears', T('$9(n-2)=72$', size=40, x=410, y=400, w=1100)),
        'Is 144 divisible by 18? Hard to see — but both are even. Divide by 2.',
        A('n − 2 = 8 → n = 10 appears', T('$n-2=8\\ \\Rightarrow\\ n=10$', size=40, x=410, y=470, w=1100)),
        '72 divides by 9 — times table. n minus 2 is 8, so n is 10.',
        D('Circle choice 3'),
        'Choice three. The standard way — through the formula.']
    s3 = [
        'Another way — through an anchor.',
        'Which angle sums do we know by heart? Triangle 180, quadrilateral 360 —',
        A('Pentagon 540 · hexagon 720 · octagon 1080 appears',
          T('Pentagon $540°\\ \\cdot$ hexagon $720°\\ \\cdot$ octagon $1080°$', size=38, x=410, y=260, w=1100)),
        '— and you should know: pentagon 540, hexagon 720, octagon 1,080.',
        "1,440 we don't know. But the octagon is close — and 1,440 is bigger, so more than 8 sides.",
        'Now the pattern: every extra side adds 180. Triangle 180, quadrilateral 360, pentagon 540 — always plus 180.',
        A('1080 → 1260 → 1440 appears', T('$1080\\rightarrow1260\\rightarrow1440$', size=40, x=410, y=340, w=1100)),
        'From the octagon, add 180: 1,260 — nine sides. Easy way: add 200, take away 20.',
        D('Under the numbers write 8, 9, 10'),
        'Again: 1,440 — ten sides.',
        D('Circle choice 3'),
        'Ten sides. Choice three.']
    _rn_video(M, 'solve-' + g, slides={2: (None, s2), 3: (None, s3)})

    # ---------- g117: 12 and 17 sides -> +5 sides -> 900° -> heptagon (trap: pentagon)
    #            ==>  14 and 20 sides -> +6 sides -> 1,080° -> octagon (trap: hexagon)
    g = 'geo34-g117'
    _rn_q(M, g, _rn_stem(M, g, ('12-sided', '14-sided'), ('17-sided', '20-sided')),
          ['A hexagon', 'An octagon', 'A decagon', 'A heptagon'], 2, [
        "$B-A=180(20-2)-180(14-2)=180(18-12)=6\\cdot180=1080°$.",
        "$180°(n-2)=1080°$ gives $n-2=6$, so $n=8$: an octagon.",
        "Faster: 20 sides is 6 sides more than 14, and each side adds $180°$: $6\\cdot180°=1080°$. (A hexagon is the trap: 6 is the number of extra sides, not the answer.)"])
    s2 = [
        'A is the angle sum of a 14-sided polygon, B of a 20-sided polygon. B minus A equals the angle sum of which polygon?',
        A('B = 180(20 − 2) = 180 · 18 appears', T('$B=180(20-2)=180\\cdot18$', size=40, x=410, y=260, w=1100)),
        'Express B with the formula: 180 times 20 minus 2 — 180 times 18.',
        A('A = 180(14 − 2) = 180 · 12 appears', T('$A=180(14-2)=180\\cdot12$', size=40, x=410, y=330, w=1100)),
        'A: 180 times 12.',
        "We won't calculate each one and subtract. We take out a common factor — easier arithmetic.",
        A('B − A = 180(18 − 12) = 6 · 180 = 1080 appears', T('$B-A=180(18-12)=6\\cdot180=1080°$', size=40, x=410, y=400, w=1100)),
        '180 times 18 minus 12 — 6 times 180: 1,080.',
        A('1080 = 180(8 − 2) → octagon appears', T('$1080°=180(8-2)\\ \\Rightarrow$ octagon', size=40, x=410, y=470, w=1100)),
        "Which polygon has 1,080? 6 triangles' worth — plus 2: eight sides. An octagon.",
        D('Circle choice 2'),
        'Choice two.']
    s3 = [
        'Now the understanding way.',
        "What's the difference between B and A in sides? 20 minus 14 — 6 extra sides.",
        A('+6 sides → 6 · 180 = 1080 appears', T('$+6$ sides $\\rightarrow 6\\cdot180°=1080°$', size=40, x=410, y=260, w=1100)),
        'Every side adds 180. Six sides — 6 times 180: 1,080.',
        '1,080 is 6 times 180 — a polygon with 6 plus 2 sides. An octagon.',
        D('Cross out choice 1'),
        "A hexagon? That's the trap — 6 is the number of extra sides, not the answer.",
        D('Circle choice 2'),
        'Choice two. Very simple — once you understand the plus 180.',
        "That's it for polygons: the regular pentagon, hexagon and octagon — and general polygons."]
    _rn_video(M, 'solve-' + g, slides={2: (None, s2), 3: (None, s3)})


# ---------------------------------------------------------------- practice: Hebrew-derived questions, new numbers
def rn_practice_questions(M):
    P = lambda k: 'geo34-core-p%02d' % k

    # p01: hexagon side 3, trapezoid AGHF -> 8 sides = 24  ==>  side 5 -> 40
    q = P(1)
    _rn_q(M, q, _rn_stem(M, q, ('side length 3 cm', 'side length 5 cm')), ['$35$', '$40$', '$30$', '$45$'], 2, [
        "Each hexagon angle is $120°$, so the angle next to it on line $CD$ is $180°-120°=60°$.",
        "Triangles $GBC$ and $HED$ have two $60°$ angles, so they are equilateral with side $5$.",
        "$AG=5+5=10$, $FH=10$, $GH=5+5+5=15$ and $AF=5$.",
        "Perimeter: $10+15+10+5=40$."])

    # p02: four hexagons, side 2.4 -> AB = 5 sides = 12  ==>  side 2.6 -> 13
    q = P(2)
    _rn_q(M, q, _rn_stem(M, q, ('side length 2.4 cm', 'side length 2.6 cm')), ['$10.4$', '$15.6$', '$13$', '$7.8$'], 3, [
        "Along $AB$: the left hexagon gives a long diagonal, $2\\cdot2.6=5.2$. Then comes one side, $2.6$. Then the right hexagon gives another long diagonal, $5.2$.",
        "$AB=5.2+2.6+5.2=13$."])

    # p03: which polygon has 900° -> heptagon  ==>  1,620° -> 11 sides (trap 9 = 1620/180)
    q = P(3)
    _rn_q(M, q, 'Which polygon has an interior-angle sum of 1,620°?',
          ['A polygon with 10 sides', 'A polygon with 11 sides', 'A polygon with 9 sides', 'A polygon with 12 sides'], 2, [
        "$180°(n-2)=1620°$, so $n-2=\\frac{1620}{180}=9$ and $n=11$.",
        "(9 is the trap: $\\frac{1620}{180}=9$ is $n-2$, not $n$.)"])

    # p04: four octagons around a square opening -> 20/32 = 5/8  ==>  six hexagons around a hexagonal opening -> 18/36
    q = P(4)
    _rn_q(M, q, ' The accompanying figure shows six congruent regular hexagons surrounding a hexagonal opening. What is the ratio of the length of the outer boundary of the arrangement to the sum of the perimeters of the six hexagons? (Do not include the boundary of the central opening.) ',
          ['$\\frac56$', '$\\frac12$', '$\\frac23$', '$\\frac13$'], 2, [
        "Each hexagon has 6 sides. It shares 1 side with the opening and 1 side with each of its two neighbors, so 3 of its sides are on the outer boundary.",
        "Outer boundary: $6\\cdot3=18$ sides. The six perimeters: $6\\cdot6=36$ sides.",
        "The ratio is $\\frac{18}{36}=\\frac12$."])
    _rn_figure(M, q, rn_fig_p04())

    # p05: square side 4 + right isosceles roof -> 12 + 4√2  ==>  side 6 -> 18 + 6√2
    q = P(5)
    _rn_q(M, q, _rn_stem(M, q, ('side 4 cm', 'side 6 cm')), ['$18+6\\sqrt2$', '$24+6\\sqrt2$', '$30$', '$18+12\\sqrt2$'], 1, [
        "$BE=6$ is the hypotenuse of the right isosceles triangle $ABE$, so $AB=AE=\\frac{6}{\\sqrt2}=3\\sqrt2$.",
        "The boundary has three square sides and two roof sides: $3\\cdot6+2\\cdot3\\sqrt2=18+6\\sqrt2$."])

    # p06: letter-only: octagon ABCDEFGH, angle BAC  ==>  octagon KLMNPQRS, angle LKM; new choice order
    q = P(6)
    _rn_q(M, q, 'KLMNPQRS is a regular octagon. What is the size of angle LKM (marked $\\alpha$ in the figure)?',
          ['$45°$', '$30°$', '$67.5°$', '$22.5°$'], 4, [
        "Each angle of a regular octagon is $180°-\\frac{360°}{8}=135°$.",
        "Triangle $KLM$ is isosceles ($KL=LM$) with vertex angle $135°$, so $\\alpha=\\angle LKM=\\frac{180°-135°}{2}=22.5°$."])
    _rn_relabel(M, q, dict(zip('ABCDEFGH', 'KLMNPQRS')))

    # p07: hexagon side 7 -> CF = 14  ==>  side 9 -> 18
    q = P(7)
    _rn_q(M, q, _rn_stem(M, q, ('side length 7 cm', 'side length 9 cm')), ['$9\\sqrt3$', '$9$', '$18\\sqrt3$', '$18$'], 4, [
        "$C$ and $F$ are opposite vertices, so $CF$ is a long diagonal. It passes through the center.",
        "The hexagon is made of 6 equilateral triangles, so the radius equals the side, $9$. $CF=2\\cdot9=18$."])

    # p08: two heptagons, outer boundary 84 -> 12 sides of 7 -> 49  ==>  two octagons, 70 -> 14 sides of 5 -> 40
    q = P(8)
    _rn_q(M, q, 'Two congruent regular octagons share one entire side and lie on opposite sides of it. The perimeter of their combined outer boundary is 70 cm. What is the perimeter of one octagon (in cm)?',
          ['$45$', '$40$', '$50$', '$35$'], 2, [
        "Two octagons have $2\\cdot8=16$ sides. The shared side is inside the shape, so it is counted in neither boundary: the outer boundary has $16-2=14$ equal sides.",
        "Each side: $\\frac{70}{14}=5$ cm. One octagon: $8\\cdot5=40$ cm.",
        "($35$ is the trap: $\\frac{70}{16}\\cdot8$ forgets that the shared side is not on the boundary.)"])
    _rn_figure(M, q, rn_fig_p08())

    # p09: letter-only: octagon ABCDEFGH, alpha = DEF, beta = ABG  ==>  PQRSTUVW, alpha = STU, beta = PQV
    q = P(9)
    _rn_q(M, q, 'PQRSTUVW is a regular octagon. Given:\n$\\begin{cases} \\alpha=\\angle STU \\\\ \\beta=\\angle PQV \\end{cases}$\nWhat is $\\alpha-\\beta$?',
          ['$45°$', '$180°$', '$90°$', '$135°$'], 3, [
        "$\\alpha$ is an angle of the octagon: $\\alpha=180°-\\frac{360°}{8}=135°$.",
        "Quadrilateral $PQVW$ is an isosceles trapezoid: $PW\\parallel QV$ and the legs $PQ$ and $WV$ are octagon sides. Its angles at $P$ and $W$ are octagon angles, $135°$.",
        "So $\\beta=\\angle PQV=180°-135°=45°$.",
        "$\\alpha-\\beta=135°-45°=90°$."])
    _rn_relabel(M, q, dict(zip('ABCDEFGH', 'PQRSTUVW')))

    # p10: 8 circles radius 2 at octagon vertices -> 8 · 5/8 · 4π = 20π  ==>  radius 3 -> 8 · 5/8 · 9π = 45π
    q = P(10)
    _rn_q(M, q, _rn_stem(M, q, ('radius 2 cm', 'radius 3 cm')), ['$27\\pi$', '$72\\pi$', '$36\\pi$', '$45\\pi$'], 4, [
        "The octagon angle is $135°$, so at each vertex $\\frac{135}{360}=\\frac38$ of the circle is inside the octagon and $\\frac58$ is outside.",
        "Each circle: $\\pi\\cdot3^2=9\\pi$. The part outside: $\\frac58\\cdot9\\pi=\\frac{45}{8}\\pi$.",
        "Eight circles: $8\\cdot\\frac{45}{8}\\pi=45\\pi$."])

    # p11: parallelogram / regular pentagon, heptagon, decagon  ==>  trapezoid / regular pentagon, hexagon, octagon
    q = P(11)
    _rn_q(M, q, M.q(q)['stemRich'], ['A regular hexagon', 'A regular pentagon', 'A trapezoid', 'A regular octagon'], 3, [
        "A trapezoid has only 2 diagonals, and they cross each other inside the shape. So all its diagonals meet at one point.",
        "A regular pentagon has $\\frac{5\\cdot2}{2}=5$ diagonals, and they do not all pass through one point. The same is true for the octagon. In the regular hexagon only the 3 long diagonals meet at the center; the 6 short ones do not pass through it."])

    # p12: letter-only: hexagon ABCDEF, tangent at F, T on BA extended  ==>  KLMNPQ, tangent at Q, S on LK extended
    q = P(12)
    _rn_q(M, q, 'KLMNPQ is a regular hexagon inscribed in a circle. The tangent at Q meets the extension of LK beyond K at S. What is angle KSQ?',
          ['$90°$', '$60°$', '$120°$', '$72°$'], 1, [
        "$\\angle SKQ$ is next to the hexagon angle $\\angle LKQ=120°$ on line $LS$, so $\\angle SKQ=180°-120°=60°$.",
        "Let $O$ be the center. A radius is perpendicular to the tangent: $\\angle OQS=90°$.",
        "Triangle $OKQ$ is equilateral (in a regular hexagon the side equals the radius), so $\\angle OQK=60°$ and $\\angle KQS=90°-60°=30°$.",
        "In triangle $KSQ$: $\\angle KSQ=180°-60°-30°=90°$."])
    _rn_relabel(M, q, {'A': 'K', 'B': 'L', 'C': 'M', 'D': 'N', 'E': 'P', 'F': 'Q', 'T': 'S'})

    # p13: six rhombi, perimeter 20 -> side 5 -> inner hexagon 30  ==>  perimeter 28 -> side 7 -> 42
    q = P(13)
    _rn_q(M, q, _rn_stem(M, q, ('perimeter 20 cm', 'perimeter 28 cm')), ['$28$', '$84$', '$42$', '$42\\sqrt2$'], 3, [
        "The 6 equal angles at the common vertex fill $360°$, so each is $\\frac{360°}{6}=60°$.",
        "Each rhombus side is $\\frac{28}{4}=7$.",
        "Each rhombus is made of two triangles with two sides $7$ and a $60°$ angle between them: equilateral triangles. So its short diagonal (a side of the inner hexagon) is $7$.",
        "Perimeter: $6\\cdot7=42$."])

    # p14: angle sum 1,980° -> 13 sides  ==>  2,160° -> 14 sides
    q = P(14)
    _rn_q(M, q, _rn_stem(M, q, ('1,980°', '2,160°')), ['$12$', '$14$', '$15$', '$13$'], 2, [
        "$180°(n-2)=2{,}160°$, so $n-2=\\frac{2160}{180}=12$ and $n=14$."])

    # p15: decagon + 5 attached triangles -> alpha = 360 − 144 − 72 = 144  ==>  octagon + 4 -> 360 − 135 − 67.5 = 157.5
    q = P(15)
    _rn_q(M, q, ' A regular octagon is divided into eight congruent triangles by joining its center to its vertices. On every other side, a congruent triangle is constructed externally. What is the outside angle α in the accompanying figure between one attached triangle and the adjacent octagon side? ',
          ['$112.5°$', '$165°$', '$135°$', '$157.5°$'], 4, [
        "The octagon angle is $180°-\\frac{360°}{8}=135°$.",
        "Each central triangle has head angle $\\frac{360°}{8}=45°$ and base angles $\\frac{180°-45°}{2}=67.5°$. The attached triangle is congruent, so its angle at the marked vertex is $67.5°$.",
        "Around the vertex: $\\alpha=360°-135°-67.5°=157.5°$."])
    _rn_figure(M, q, rn_fig_p15())

    # p16: AB = AE = 4a, BC = a, 120° -> 4√3a² + 4√3a² = 8√3a²  ==>  AB = AE = 6a, BC = 2a -> 9√3a² + 12√3a² = 21√3a²
    q = P(16)
    _rn_q(M, q, 'Pentagon ABCDE consists of rectangle BCDE and isosceles triangle ABE. Given:\n$\\begin{cases} AB=AE=6a \\\\ BC=2a \\\\ \\angle BAE=120° \\end{cases}$\nWhat is the area of the pentagon?',
          ['$9\\sqrt3\\,a^2$', '$21\\sqrt3\\,a^2$', '$30\\sqrt3\\,a^2$', '$12\\sqrt3\\,a^2$'], 2, [
        "Draw the height from $A$ to $BE$. It splits triangle $ABE$ into two 30-60-90 triangles with hypotenuse $6a$.",
        "The height (short leg) is $3a$. Half of $BE$ (long leg) is $3a\\sqrt3$, so $BE=6a\\sqrt3$.",
        "Triangle: $\\frac{6a\\sqrt3\\cdot3a}{2}=9\\sqrt3\\,a^2$. Rectangle: $6a\\sqrt3\\cdot2a=12\\sqrt3\\,a^2$.",
        "Total: $21\\sqrt3\\,a^2$."])
    _rn_figure(M, q, rn_fig_p16())

    # p17: octagon side 3, cross = 9 + 18√2  ==>  side 8 -> 64 + 128√2
    q = P(17)
    _rn_q(M, q, _rn_stem(M, q, ('side length 3 cm', 'side length 8 cm')),
          ['$64+64\\sqrt2$', '$64+128\\sqrt2$', '$128+128\\sqrt2$', '$128+64\\sqrt2$'], 2, [
        "Square: $8^2=64$.",
        "Each rectangle has sides $8$ and $\\frac{8}{\\sqrt2}=4\\sqrt2$, so its area is $8\\cdot4\\sqrt2=32\\sqrt2$. Four rectangles: $128\\sqrt2$.",
        "Shaded: $64+128\\sqrt2$."])

    # p18: P n+1 sides, Q m+3 sides -> 180(n − m − 2)  ==>  K a+2 sides, L b+5 sides -> 180(a − b − 3)
    q = P(18)
    _rn_q(M, q, 'Polygon K has $a+2$ sides and polygon L has $b+5$ sides. a and b are whole numbers, $b\\ge3$ and $a>b+3$. By how much is the interior-angle sum of K greater than that of L?',
          ['$180°(a-b)$', '$180°(a-b-3)$', '$180°(a+b-3)$', '$180°(a-b+3)$'], 2, [
        "$K$: $180°(a+2-2)=180°a$. $L$: $180°(b+5-2)=180°(b+3)$.",
        "Difference: $180°a-180°(b+3)=180°(a-b-3)$.",
        "Faster: $K$ has $(a+2)-(b+5)=a-b-3$ more sides, and each side adds $180°$."])

    # p19: no numbers: new choice order only
    q = P(19)
    _rn_q(M, q, M.q(q)['stemRich'], ['$2:1$', '$3:1$', '$4:3$', '$4:1$'], 4, list(M.q(q)['explanation']))

    # p20: 10 regions -> 9 sides  ==>  13 regions -> 12 sides
    q = P(20)
    _rn_q(M, q, _rn_stem(M, q, ('into 10 separate', 'into 13 separate')), ['$13$', '$11$', '$12$', '$14$'], 3, [
        "Each side cuts off one region between the side and the circle: $n$ regions. The inside of the polygon is one more region.",
        "$n+1=13$, so $n=12$."])


# ---------------------------------------------------------------- practice clean-up 34 -> 25 and order easy -> hard
def rn_practice(M):
    P = lambda k: 'geo34-core-p%02d' % k
    S = lambda k: 'q-r26-t34-%02d' % k
    # copy: p21 (150° -> 12 sides) = guided q-r26-t34-01 (160° -> 18) and the card example
    # English extras: keep 2 (p26 one regular angle from n, p27 star partition half); drop p22 (exterior angles -
    # q-r26-t34-05 practises them), p23 (diagonals from one vertex - q-r26-t34-07), p24 (hexagon area - g107),
    # p25 (octagon corner triangles - p17)
    # September items: keep 05 (exterior angles), 07 (diagonal count), 09 (common side -> isosceles) - types the
    # Hebrew practice does not have; drop 04 (one angle of a decagon - p26, p06), 08 (polygons filling a point - p13,
    # p15), 10 (octagon area - p17, g108), 11 (hexagon rectangle area - g112, p27)
    for qid in [P(21), P(22), P(23), P(24), P(25), S(4), S(8), S(10), S(11)]: M.unplace(qid)
    M.practice_order(PRACTICE, [
        P(3), P(14), P(26), S(5), P(8), P(7), P(6), S(7), P(11), P(27), P(5), P(2), P(1), P(18), P(20), P(17), P(9),
        S(9), P(13), P(12), P(16), P(19), P(15), P(4), P(10)])
    n = sum(1 for f in M.D['flow'] if f['section'] == PRACTICE and f['type'] == 'question')
    assert n == 25, n


def _rn_sync(M):
    """'Pre-loaded' notes of the solution slides follow the (changed) stems."""
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC or v.get('kind') != 'solution': continue
        for b in v['beats']:
            pre = b['items'][:b['pre']]
            if len(pre) == 1 and pre[0].get('k') == 'q' and (b.get('canvas') or '').startswith('Pre-loaded — question'):
                qid = pre[0]['qid']
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, M.q(qid)['stem'])
        M.touched_videos.add(v['id'])


def renumber_pass(M):
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    _rn_sync(M)
