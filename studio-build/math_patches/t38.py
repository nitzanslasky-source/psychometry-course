"""Topic 38 - Geometric reasoning. Course review 2026-09 fixes.
See t38_CHANGES.md for the plain-language list."""
import math, re
import math_api
from math_api import VIS
from dsl import T, H, A, D, Q

TOPIC = 38
SHAPE, MINMAX, DIAG = 'geo-172', 'geo-175', 'geo-177'
LEARN, PRACT = 'geo38-learn-1', 'geo38-core-practice'
CARD = 'mem-geo-reasoning'

# ------------------------------------------------------------------ SVG helpers (same style as the course figures)
INK, TEAL, ORANGE, GRAY = '#203344', '#087f83', '#bb6821', '#9aa8c0'
FILL, FILL2, TFILL = '#e8eefb', '#eef4fb', '#d5f1ed'
FONT = 'DejaVu Sans,Arial,sans-serif'


def _svg(vb, label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, ''.join(body)))


def _t(x, y, s, fill=INK, size=20, weight=None, anchor='middle'):
    w = ' font-weight="%s"' % weight if weight else ''
    return ('<text x="%.3f" y="%.3f" text-anchor="%s" dominant-baseline="middle" fill="%s" font-family="%s" '
            'font-size="%s"%s>%s</text>' % (x, y, anchor, fill, FONT, size, w, s))


def _ln(x1, y1, x2, y2, stroke=INK, w=2.5, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, stroke, w, d)


def _poly(pts, fill=FILL, stroke=INK, w=2.5):
    return ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>'
            % (' '.join('%.3f,%.3f' % p for p in pts), fill, stroke, w))


def _dot(x, y, r=3.2, fill=INK):
    return '<circle cx="%.3f" cy="%.3f" r="%s" fill="%s"/>' % (x, y, r, fill)


def _right(cx, cy, ux, uy, vx, vy, s=14, stroke=TEAL):
    """Right-angle mark at (cx, cy) between unit directions u and v."""
    p1 = (cx + s * ux, cy + s * uy); p2 = (p1[0] + s * vx, p1[1] + s * vy); p3 = (cx + s * vx, cy + s * vy)
    return _ln(*p1, *p2, stroke=stroke, w=1.7) + _ln(*p2, *p3, stroke=stroke, w=1.7)


# ---------- Q4: trapezoid PQRS, ST perpendicular to QR
def _trap(P, S, Q_, R, vb):
    T_ = (S[0], Q_[1])
    body = [_poly([P, Q_, T_, S], FILL, INK), _poly([T_, R, S], TFILL, TEAL),
            _right(T_[0], T_[1], 0, -1, 1, 0),
            _t(P[0] - 12, P[1] - 20, 'P'), _t(Q_[0] - 16, Q_[1] + 16, 'Q'), _t(R[0] + 16, R[1] + 16, 'R'),
            _t(S[0] + 12, S[1] - 20, 'S'), _t(T_[0], T_[1] + 23, 'T')]
    return _svg(vb, 'A trapezoid split by a perpendicular from an upper vertex', body)


# near-isosceles: the "first glance" drawing (the trapezoid is clearly bigger)
FIG_Q4 = _trap((190, 110), (350, 110), (130, 250), (410, 250), '70 64 400 235')
# the exaggerated drawing: QR stretched far to the right (the triangle is clearly bigger)
FIG_Q4_STRETCH = _trap((130, 110), (230, 110), (100, 250), (590, 250), '48 64 580 235')


# ---------- Q5: diameter AB and chord CD perpendicular to it
def _disk(cx_chord, vb='152.2 26.5 335.6 307.9'):
    ox, oy, r = 320.0, 180.0, 116.8
    h = math.sqrt(r * r - (cx_chord - ox) ** 2); top, bot = oy - h, oy + h
    a0 = math.pi; a1 = math.atan2(-(top - oy), cx_chord - ox)   # math angles (y up)
    arc = [(ox + r * math.cos(a0 + (a1 - a0) * k / 60), oy - r * math.sin(a0 + (a1 - a0) * k / 60)) for k in range(61)]
    left, right = (203.2 + cx_chord) / 2, (cx_chord + 436.8) / 2
    small = cx_chord > 380
    body = ['<circle cx="320.000" cy="180.000" r="116.800" fill="%s" stroke="%s" stroke-width="2.5"/>' % (FILL, INK),
            _poly([(cx_chord, oy)] + arc + [(cx_chord, top)], TFILL, 'none'),
            _ln(203.2, oy, 436.8, oy), _ln(cx_chord, top, cx_chord, bot),
            _right(cx_chord, oy, 1, 0, 0, -1, s=8.76),
            _t(184.2, oy, 'A'), _t(455.8, oy, 'B'), _t(cx_chord + 15, top - 17, 'C'), _t(cx_chord + 15, bot + 18, 'D'),
            _t(left, 136.2, 'I', size=21), _t(left, 223.8, 'II', size=21),
            _t(right, 204 if small else 209.2, 'III', size=19 if small else 21),
            _t(right, 156 if small else 150.8, 'IV', size=19 if small else 21)]
    return _svg(vb, 'A horizontal diameter and a perpendicular chord divide a disk into four regions', body)


FIG_Q5 = _disk(327.0)           # CD almost through the center: "all four look like quarters"
FIG_Q5_EXAG = _disk(392.0)      # CD pushed toward B


# ---------- the rods picture: two fixed sides, the angle between them opens
def _rods():
    B = (260.0, 330.0); C = (580.0, 330.0); L = 200.0
    pts = {a: (B[0] + L * math.cos(math.radians(a)), B[1] - L * math.sin(math.radians(a))) for a in (50, 90, 130)}
    col = {50: TEAL, 90: ORANGE, 130: INK}
    body = [_ln(90, pts[50][1], 420, pts[50][1], GRAY, 1.6, '6 5'), _t(430, pts[50][1] - 2, 'same height', GRAY, 19, anchor='start')]
    for a in (130, 90, 50):
        X = pts[a]
        body += [_ln(X[0], X[1], C[0], C[1], col[a], 1.8, '7 5'), _ln(B[0], B[1], X[0], X[1], col[a], 3), _dot(X[0], X[1], 4.5, col[a])]
    body += [_ln(B[0], B[1], C[0], C[1], INK, 3), _dot(*B, r=4), _dot(*C, r=4),
             _t(pts[50][0] + 26, pts[50][1] - 18, '50°', TEAL, 20, '700'),
             _t(pts[90][0] + 30, pts[90][1] - 6, '90°', ORANGE, 20, '700'),
             _t(pts[130][0] - 30, pts[130][1] - 18, '130°', INK, 20, '700'),
             _t(B[0] - 12, B[1] + 20, 'B', size=22), _t(C[0] + 12, C[1] + 20, 'C', size=22),
             _t(420, B[1] + 22, '8', ORANGE, 20, '700'), _t(238, 225, '5', ORANGE, 20, '700')]
    return _svg('60 100 620 262', 'Two fixed sides joined at B with the angle between them opening', body)


# ---------- slide the apex: same base, apex on a parallel line
def _apex():
    k, m = 120.0, 300.0; A_, B_ = (230.0, m), (390.0, m)
    body = [_ln(90, k, 620, k, INK, 2), _ln(90, m, 620, m, INK, 2), _t(74, k, 'k', size=21), _t(74, m, 'm', size=21)]
    for x, c, fl in ((150, TEAL, 'none'), (310, ORANGE, 'none'), (540, INK, 'none')):
        body.append(_poly([A_, B_, (x, k)], fl, c, 2.4))
    body += [_ln(310, k, 310, m, GRAY, 1.6, '6 5'), _right(310, m, 0, -1, 1, 0, s=12),
             _t(322, 210, 'h', ORANGE, 21, '700', 'start'),
             _dot(150, k, 4.5, TEAL), _dot(310, k, 4.5, ORANGE), _dot(540, k, 4.5, INK),
             _t(150, k - 22, 'P₁', TEAL, 22, '700'), _t(310, k - 22, 'P₂', ORANGE, 22, '700'), _t(540, k - 22, 'P₃', INK, 22, '700'),
             _t(A_[0] - 6, m + 22, 'A', size=22), _t(B_[0] + 6, m + 22, 'B', size=22)]
    return _svg('50 80 600 255', 'Triangles with the same base AB and apexes on a line parallel to AB', body)


# ---------- guided "slide the apex" question: trapezoid with its diagonals
def _trap_diag(shade=False):
    A_, D_, B_, C_ = (230.0, 100.0), (410.0, 100.0), (130.0, 280.0), (540.0, 280.0)
    t = 180.0 / 590.0; E = (A_[0] + t * 310, A_[1] + t * 180)
    body = [_poly([A_, D_, C_, B_], FILL, INK)]
    if shade:
        body += [_poly([A_, B_, E], TFILL, TEAL, 1.5), _poly([D_, C_, E], '#f6e3d2', ORANGE, 1.5)]
    body += [_ln(*A_, *C_, INK, 2), _ln(*B_, *D_, INK, 2), _poly([A_, D_, C_, B_], 'none', INK), _dot(*E),
             _t(A_[0] - 10, A_[1] - 18, 'A'), _t(D_[0] + 10, D_[1] - 18, 'D'),
             _t(B_[0] - 14, B_[1] + 16, 'B'), _t(C_[0] + 14, C_[1] + 16, 'C'), _t(E[0], E[1] - 22, 'E')]
    return _svg('100 66 470 240', 'A trapezoid with its two diagonals meeting at E', body)


# ---------- practice: P moves along a line parallel to AB
def _moving_p():
    k, m = 110.0, 270.0; A_, B_, P = (230.0, m), (390.0, m), (480.0, k)
    body = [_ln(90, k, 610, k, INK, 2), _ln(90, m, 610, m, INK, 2), _t(74, k, 'k', size=21), _t(74, m, 'm', size=21),
            _poly([A_, B_, P], FILL, TEAL, 2.4), _ln(P[0], k, P[0], m, GRAY, 1.6, '6 5'), _right(P[0], m, 0, -1, -1, 0, s=12),
            _dot(*P, r=4.5, fill=TEAL), _t(P[0], k - 20, 'P'), _t(A_[0] - 6, m + 20, 'A'), _t(B_[0] + 4, m + 20, 'B'),
            _t(310, m + 22, '6', ORANGE, 20, '700'), _t(P[0] + 14, 190, '4', ORANGE, 20, '700', 'start')]
    return _svg('50 72 580 230', 'Base AB on line m and a point P moving along the parallel line k', body)


# ------------------------------------------------------------------ small helpers
_BRIT = [('practise', 'practice'), ('Practise', 'Practice'), ('metre', 'meter'), ('centre', 'center'), ('colour', 'color')]


def _us(t):
    for a, b in _BRIT: t = t.replace(a, b)
    return t


def _so(t):
    """'..., so x' / '... — so x' (so = therefore) -> '... . So, x'."""
    return re.sub(r'(,| —) so (?!that\b|often\b|much\b|many\b|far\b|on\b)(\w)', lambda mo: '. So, ' + mo.group(2), t)


def _script(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _replace_say(M, vid, n, old, new):
    """Replace the spoken line containing `old` by the line(s) `new` (str or list). new=None deletes it."""
    def fn(lines):
        out = []; hit = False
        for l in lines:
            if 'say' in l and old in l['say'] and not hit:
                hit = True
                for s in ([] if new is None else [new] if isinstance(new, str) else new): out.append({'say': s})
            else: out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _set_fig(M, vid, n, svg):
    for it in M.slide(vid, n)['items']:
        if it.get('k') == 'q' and 'fig' in it: it['fig'] = {'type': 'geometry', 'svg': svg}
    M.touched_videos.add(vid)


def _lesson_actives(M, vid):
    k = 0
    for b in M.video(vid)['beats']:
        if b['mode'] == 'concept': b['active'] = k; k += 1


def _solution(M, qid, group_title, intro, slides, fig=False):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % math_api._word(n)] + intro)]
    for s in slides:
        pre = [Q(qid, figw=0.56, figalign='left', **({'fig': {'type': 'geometry', 'svg': s[2]}} if len(s) > 2 else {}))] \
            if fig else [Q(qid)]
        beats.append(dict(mode='question', active=0, title=s[0], pre=pre, script=s[1]))
    v = M.new_video('solve-' + qid, TOPIC, group_title, ['Question %d' % n], beats, M.section_of(qid),
                    kind='solution', qid=qid)
    v['beats'][0]['title'] = group_title
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def R(x, y, t, size=34):
    """Board text in the right-hand column of a question slide that shows a figure."""
    return T(t, size=size, x=1060, y=y, w=470)


def W(y, t, size=36):
    """Board text under a question without a figure."""
    return T(t, size=size, x=410, y=y, w=1100)


# ==================================================================================== apply
def apply(M):
    S = M.set_q

    # ================================================================================
    # 1. WRONG RULES / MISLEADING WORDS
    # ================================================================================
    # --- Q9 (geo38-g183), slide 2: "60 degrees -> equilateral" is false for sides 3 and 6
    _replace_say(M, 'solve-geo38-g183', 2, 'A 60 degree angle would send us straight',
                 ["There's another way we learned: an anchor. Try 60 degrees.",
                  "Careful: sides 3 and 6 with 60 degrees between them are NOT an equilateral triangle. The sides aren't equal.",
                  "6 is twice 3. It's the 30-60-90 triangle: the right angle is at A, and AC is 3 root 3 — about 5.2."])
    _replace_say(M, 'solve-geo38-g183', 2, 'Here the angle is 75',
                 ["Our angle is 75 — wider than 60. The angle opened, and AC got even longer than 5.2.",
                  "Either way, AC is much longer than AB."])

    def q9s2(lines):
        # the anchor line gets its own board item
        k = next(i for i, l in enumerate(lines) if 'say' in l and "It's the 30-60-90" in l['say'])
        b = M.slide('solve-geo38-g183', 2)
        b['items'].append(R(0, 370, r'$60°$ with sides $3, 6$: a $30°$-$60°$-$90°$ triangle, $AC=3\sqrt3\approx5.2$', 30))
        lines.insert(k, {'appear': len(b['items']) - 1, 'label': "'60° with sides 3, 6: 30-60-90' appears"})
        return lines
    M.edit_lines('solve-geo38-g183', 2, q9s2)
    # slide 3: name the rods rule
    _replace_say(M, 'solve-geo38-g183', 3, "That's the angle-opening principle",
                 "That's the rods rule: two fixed sides — a wider angle between them makes a longer third side.")
    # slide 4: the height grows only up to 90 degrees
    _replace_say(M, 'solve-geo38-g183', 4, 'By the angle — exactly like before',
                 ["By the angle. The side of 3 leans at 75 in the first one, at 45 in the second.",
                  "Up to 90 degrees, the wider the angle, the taller the height. Both angles here are below 90."])
    _replace_say(M, 'solve-geo38-g183', 5, 'As it approaches 0, the height shrinks',
                 ["As it approaches 0, the height shrinks and shrinks — the area is just a hair above 0.",
                  "And past 90? The height shrinks again. 105 degrees gives the same height as 75 — the same area."])
    S('geo38-g183', figure=M.slide('solve-geo38-g183', 2)['items'][0]['fig']['svg'],   # H was cut off
      expl=['Take the 6-cm sides as bases. Then the area is $6\\cdot h$, where $h$ is the height from A (or from E).',
            'The side of 3 leans at $75°$ in ABCD and at $45°$ in EFGH. Up to $90°$, a wider angle gives a taller height. '
            'With $45°$, the height is $\\frac{3}{\\sqrt2}\\approx2.1$. With $75°$, it is more than that (and less than 3).',
            'Same base, taller height: ABCD has the greater area. Equal areas cannot be true: choice 1.',
            'The other claims are true: $AC>3=AB$ (triangle inequality), $AC>EG$ (a wider angle between the same sides), '
            'and both perimeters are $2(3+6)=18$.'])

    # --- Q3 (geo38-g176) video: rods rule instead of the wrong back-reference; one goodbye only (at the end)
    _replace_say(M, 'solve-geo38-g176', 3, 'Remember the start of the lesson',
                 'Remember the rods rule: two sides stay the same — the wider the angle between them, the longer the third side.')
    _replace_say(M, 'solve-geo38-g176', 4, "That's it for minimum–maximum — and that's the last",
                 "That's it for this anchor. One more question on the rods rule.")
    _replace_say(M, 'solve-geo38-g176', 4, 'What can I wish you', None)
    _replace_say(M, 'solve-geo38-g176', 4, 'So — go up and succeed', None)
    S('geo38-g176', expl=['Anchor: if $\\alpha$ were $90°$, the side opposite it would be 15, because $9, 12, 15$ is the triple $3, 4, 5$ times 3.',
                          'The side is 16, longer than 15. Two fixed sides (9 and 12) with a longer third side: the angle between them opened. So, $\\alpha>90°$.',
                          'Check: $16^2=256>9^2+12^2=225$.'])

    # --- "Move the vertex away": only when the vertex moves straight away
    sc = _script(M, MINMAX, 3)
    j = next(i for i, x in enumerate(sc) if isinstance(x, tuple) and x[0] == 'A' and x[2].get('k') == 't')
    sc[j] = A(sc[j][1], dict(sc[j][2], t='The vertex moves straight away from the segment $\\rightarrow$ the angle gets smaller'))
    k = next(i for i, x in enumerate(sc) if isinstance(x, str) and x.startswith('If I move the vertex away'))
    sc[k] = 'If I move the vertex straight away, along the dashed line — and away again — the angle gets smaller and smaller. It closes.'
    sc.insert(k + 1, "Careful: 'straight away' matters. A point that is farther, but off to the side, is a different story.")
    M.set_slide(MINMAX, 3, script=sc)

    # --- Q4 (geo38-g178): the first drawing is near-isosceles, the exaggerated one is stretched
    S('geo38-g178', figure=FIG_Q4,
      expl=['Both regions have height ST. Trapezoid PQTS: $\\frac{(PS+QT)\\cdot ST}{2}$. Triangle STR: $\\frac{TR\\cdot ST}{2}$.',
            'Compare $TR$ with $PS+QT$. The givens do not fix TR (QR can be stretched to the right).',
            'Example: $PS=3$, $QT=4$, $ST=3$: the trapezoid is 10.5. $TR=2$ gives a triangle of 3, $TR=7$ gives 10.5, '
            '$TR=10$ gives 15. All three cases happen, so none of the claims must be true: choice 4.'])
    _set_fig(M, 'solve-geo38-g178', 2, FIG_Q4)
    for n in (3, 4, 5): _set_fig(M, 'solve-geo38-g178', n, FIG_Q4_STRETCH)
    _replace_say(M, 'solve-geo38-g178', 3, 'Look at the legs PQ and SR',
                 "In the first drawing, the legs PQ and SR looked about equal — but nobody said the trapezoid is isosceles.")

    def q4s3(lines):
        for l in lines:
            if 'draw' in l and 'Extend QR' in l['draw']: l['draw'] = 'Point at the stretched base QR and the long leg SR'
        return lines
    M.edit_lines('solve-geo38-g178', 3, q4s3)
    _replace_say(M, 'solve-geo38-g178', 3, 'For example: stretch the base QR',
                 "For example: stretch the base QR — really stretch it to the right, like here. The leg SR gets much longer.")

    # --- Q5 (geo38-g179): the question figure really looks like four quarters; slides 3-4 show the exaggerated one
    S('geo38-g179', figure=FIG_Q5,
      expl=['AB is a diameter, and a diameter is a line of symmetry. Reflect across AB: I goes onto II, and IV goes onto III. So, I = II and III = IV (Ava is right).',
            'I + IV is half the disk (above AB). Since IV = III, I + III is also half the disk, and so is II + IV. Mia is right.',
            'CD is only a chord. Push it toward B: III becomes tiny while II stays large. II = III need not be true. Answer: Ava and Mia only, choice 3.'])
    _set_fig(M, 'solve-geo38-g179', 2, FIG_Q5)
    for n in (3, 4): _set_fig(M, 'solve-geo38-g179', n, FIG_Q5_EXAG)
    _replace_say(M, 'solve-geo38-g179', 3, 'Look at the exaggerated picture',
                 "Look at the exaggerated picture: CD is close to B. Two is big, three is tiny. Before, they only looked equal.")

    # --- Q12 (box cut): "edges" means box edges here -> "extremes"
    b = M.slide('solve-geo38-g186', 3)
    for it in b['items']:
        if it.get('t') and 'edges' in it['t']: it['t'] = 'Answers $10, 11, 12, 15$ · the extremes: $10$ and $15$'
    for n in (3, 4, 5):
        def ext(lines):
            for l in lines:
                for key in ('say', 'label'):
                    if key in l:
                        l[key] = (l[key].replace('Here the edges are', 'Here the extremes are').replace('at the edges', 'at the extremes')
                                  .replace("there's our edge", "there's our extreme").replace('edges: 10 and 15', 'extremes: 10 and 15'))
            return lines
        M.edit_lines('solve-geo38-g186', n, ext)

    # ================================================================================
    # 2. MISSING METHODS
    # ================================================================================
    # --- (a) rods rule + greatest area, in the Minimum and Maximum lesson (after "Stretch the segment")
    M.insert_slides(MINMAX, 4, [
        dict(mode='concept', title='Two rods', script=[
            "Now a situation the exam loves: two sides that don't change, and the angle between them changes.",
            A('Rods figure appears', VIS(_rods(), w=1000, h=520)),
            "Picture two rods joined at B: one of length 5, one of length 8. I open the angle between them.",
            "50 degrees, 90 degrees, 130 degrees. Look at the dashed lines — the third side.",
            A("'Wider angle → longer third side' appears",
              T('Same two sides, wider angle $\\rightarrow$ longer third side', size=36, x=410, y=640)),
            "The wider the angle, the longer the third side. Always.",
            "The height is different. It grows only up to 90 degrees. At 90, the rod of 5 stands straight up — that's the tallest.",
            "Past 90, the rod leans the other way, and the height shrinks again.",
            A("'50° and 130°: the same height' appears",
              T('Height and area: greatest at $90°$ · $\\theta$ and $180°-\\theta$ give the same area', size=36, x=410, y=710)),
            "Look at 50 and 130: they reach the same dashed line. Same height, same area.",
            "Here's the trap: a wider angle does NOT always mean a bigger area. Only up to 90.",
        ]),
        dict(mode='concept', title='Greatest area', script=[
            "So what is the greatest possible area with two given sides?",
            A("'Sides 5 and 8: greatest area?' appears", T('Two sides $5$ and $8$. Greatest possible area?', size=44)),
            "Make the angle 90. Then one side is the base, and the other is the height.",
            A("'At 90°: 5·8/2 = 20' appears", T('At $90°$: $\\dfrac{5\\cdot8}{2}=20$', size=46)),
            "5 times 8 over 2: 20. Every other angle gives less than 20.",
            A("'Parallelogram with sides 5 and 8: at most 40' appears",
              T('Parallelogram with sides $5$ and $8$: at most $5\\cdot8=40$ (a rectangle)', size=40)),
            "A parallelogram with sides 5 and 8? At most 40 — when it's a rectangle.",
            "And the area can be as small as you like: close the angle, and the area goes down toward 0.",
        ])])
    # slides now: 1 title, 2 min-max, 3 vertex away, 4 stretch, 5 rods, 6 greatest area, 7 arc, 8 diameter, 9 anchor
    M.insert_slides(MINMAX, 9, [dict(mode='concept', title='Acute or obtuse?', script=[
        "The anchor you'll use most: the right angle. You can check it with the sides alone.",
        A("'Longest side c, the other sides a and b' appears", T('Longest side $c$, the other two sides $a$ and $b$:', size=40)),
        A("'c² = a² + b²: right' appears", T('$c^2=a^2+b^2$ $\\rightarrow$ a right angle', size=42)),
        "If c squared equals a squared plus b squared — Pythagoras — the angle opposite c is exactly 90.",
        A("'c² > a² + b²: obtuse' appears", T('$c^2>a^2+b^2$ $\\rightarrow$ an obtuse angle', size=42)),
        "If c is longer than that, the rods opened wider: the angle is obtuse.",
        A("'c² < a² + b²: acute' appears", T('$c^2<a^2+b^2$ $\\rightarrow$ all three angles are acute', size=42)),
        "If c is shorter, the angle closed: it's acute. And since it's the biggest angle, all three are acute.",
        A("'7, 8, 10' appears", T('$7, 8, 10$: $\\ 10^2=100<49+64=113$ $\\rightarrow$ acute', size=40)),
        "For example 7, 8 and 10. 100 is less than 113. All the angles are acute.",
        "Always use the LONGEST side as c.",
    ])])
    M.set_sidebar(MINMAX, ['Min–max in geometry', 'Move the vertex away', 'Stretch the segment', 'Two rods', 'Greatest area',
                           'Angles on an arc', 'Angle on a diameter', 'Min–max with an anchor', 'Acute or obtuse?'])
    _lesson_actives(M, MINMAX)

    # guided question: greatest area with two fixed sides (after Question 3)
    g1 = 'q-r26-t38-01'
    M.new_q(g1, TOPIC, 'Two sides of a triangle are 6 cm and 10 cm long. The angle between them can change. '
                       'What is the greatest possible area of the triangle?',
            ['$24$ cm²', '$30$ cm²', '$60$ cm²', '$15$ cm²'], 2,
            ['Take the side of 10 as the base. The area is $\\frac{10\\cdot h}{2}$, and the height $h$ is at most 6.',
             'The height is 6 exactly when the angle is $90°$. Then the area is $\\frac{10\\cdot6}{2}=30$.',
             'Trap: 24 is the area of the 6-8-10 right triangle. There, 10 is the hypotenuse, and the angle between 6 and 10 is not $90°$.'])
    M.place_q(g1, LEARN, after='solve-geo38-g176')
    _solution(M, g1, 'Minimum and Maximum Question', ['Two sides, and the angle is free.'], [
        ('Fix the base', [
            'Two sides of a triangle are 6 and 10. The angle between them can change. What is the greatest possible area?',
            'Two fixed sides, a free angle. That\'s the rods rule.',
            "Take 10 as the base. It doesn't change.",
            A("'Area = 10·h/2' appears", W(250, 'Area $=\\dfrac{10\\cdot h}{2}$', 40)),
            'So the area depends only on the height: the distance from the end of the 6 down to the base.',
        ]),
        ('Open the rod', [
            'Open the angle. At 90 degrees, the side of 6 stands straight up. The height is the whole 6.',
            'At any other angle, the side leans, and the height is less than 6.',
            A("'Greatest at 90°: h = 6' appears", W(330, 'Greatest at $90°$: $h=6$', 40)),
            A("'10·6/2 = 30' appears", W(410, '$\\dfrac{10\\cdot6}{2}=30$', 40)),
            '10 times 6 over 2: 30.',
            D('Circle choice 2'),
            'Choice two.',
        ]),
        ('The trap', [
            'The trap is 24. Students see 6 and 10 and think of the 6, 8, 10 triangle.',
            'But there, 10 is the hypotenuse. The angle between the 6 and the 10 is not 90.',
            A("'6, 8, 10: area 24 — not the greatest' appears", W(250, '$6, 8, 10$: area $24$ — not the greatest', 38)),
            'Here we choose the angle freely. So we make it 90 — and get 30.',
            "That's it for minimum and maximum. Next: diagrams that can change.",
        ])])

    # --- (b) Diagrams That Can Change: slide the apex + push to the extremes
    M.insert_slides(DIAG, 3, [
        dict(mode='concept', title='Slide the apex', script=[
            "One classic flexible diagram: the apex slides, and the area doesn't change.",
            A('Apex figure appears', VIS(_apex(), w=1000, h=520)),
            "Lines k and m are parallel. The base AB sits on m. The apex P can be anywhere on k.",
            "P one, P two, P three. Three very different triangles.",
            "But the height is always the distance between the parallel lines — h.",
            A("'Same base, apex on a parallel line → same area' appears",
              T('Same base, apex on a parallel line $\\rightarrow$ same height $\\rightarrow$ same area', size=36, x=410, y=640)),
            "Same base, same height — the same area. All three.",
            A("'The perimeter does change' appears", T('The perimeter DOES change', size=36, x=410, y=710)),
            "Careful: the perimeter does change. Slide P far away, and the sides get very long.",
            "You'll see this in a trapezoid too: the two top corners are on a line parallel to the base.",
        ]),
        dict(mode='concept', title='Push to the extremes', script=[
            "How do we exaggerate? Three moves to try.",
            A("'1 · Push the free point to the end' appears", T('1 · Push the free point to the end (the shape almost goes flat)', size=38)),
            "One: push the free point all the way to the end. The shape almost goes flat.",
            A("'2 · Put it in the middle' appears", T('2 · Put it in the middle (a symmetric shape)', size=38)),
            "Two: put it exactly in the middle. The shape becomes symmetric.",
            A("'3 · Find what is free' appears", T('3 · Find what is free: an angle, a side, a split', size=38)),
            "Three: find what the givens don't fix. An angle? A side? Where a segment is split?",
            A("'Free and the answer depends on it → cannot be determined' appears",
              T('The answer depends on a free quantity $\\rightarrow$ it cannot be determined', size=38)),
            "If the answer depends on something free — it cannot be determined.",
            "And the opposite: if a claim survives all the extremes, it's usually a 'must'. Then look for the reason.",
        ])])
    M.set_sidebar(DIAG, ['Must or could?', 'How to test a claim', 'Slide the apex', 'Push to the extremes'])
    _lesson_actives(M, DIAG)

    # guided question: slide the apex in a trapezoid (before Question 4)
    g2 = 'q-r26-t38-02'
    M.new_q(g2, TOPIC, 'ABCD is a trapezoid with AD ∥ BC. Its diagonals AC and BD meet at E. '
                       'Which of the following statements is necessarily true?',
            ['The area of triangle ABE is greater than the area of triangle DCE.', '$AE=EC$',
             'The area of triangle ABE equals the area of triangle DCE.',
             'The area of triangle ABE equals the area of triangle AED.'], 3,
            ['Triangles ABC and DBC have the same base BC. A and D lie on AD, which is parallel to BC, so both triangles have the same height. Their areas are equal.',
             'Both triangles contain triangle EBC. Take it away from each: $S_{ABE}=S_{ABC}-S_{EBC}=S_{DBC}-S_{EBC}=S_{DCE}$. Choice 3.',
             'AE = EC only in a parallelogram. ABE = AED fails when AD is very short: AED almost disappears, and ABE does not.'],
            figure=_trap_diag())
    M.place_q(g2, LEARN, after=DIAG)
    _solution(M, g2, 'Reasoning Questions', ['A trapezoid and its diagonals.'], [
        ('Same base, same height', [
            'ABCD is a trapezoid, AD parallel to BC. The diagonals meet at E. Which statement must be true?',
            'Look for triangles with the same base and an apex on a parallel line.',
            D('Shade triangle ABC, then triangle DBC'),
            'Triangle ABC and triangle DBC. The same base: BC.',
            'A and D are both on line AD — parallel to BC. So the two apexes are at the same height.',
            A("'S(ABC) = S(DBC)' appears", R(0, 250, '$S_{ABC}=S_{DBC}$', 40)),
            'Same base, same height — the same area.',
        ]),
        ('Take away the shared part', [
            'Both triangles contain the same piece: triangle EBC.',
            A("'S(ABE) = S(ABC) − S(EBC)' appears", R(0, 250, '$S_{ABE}=S_{ABC}-S_{EBC}$', 36)),
            A("'S(DCE) = S(DBC) − S(EBC)' appears", R(0, 330, '$S_{DCE}=S_{DBC}-S_{EBC}$', 36)),
            'Equal areas, minus the same piece. What is left is equal: ABE equals DCE.',
            A("'S(ABE) = S(DCE)' appears", R(0, 420, '$S_{ABE}=S_{DCE}$', 42)),
            D('Circle choice 3'),
            'Choice three.',
        ], _trap_diag(shade=True)),
        ('Check the others', [
            'Choice one says ABE is bigger. We just saw they are always equal. Out.',
            'AE equals EC? That happens only when the diagonals cut each other in half — a parallelogram. Here AD is shorter than BC. Out.',
            'ABE equals AED? Exaggerate: make AD tiny. Triangle AED almost disappears, but ABE does not. Out.',
            A("'Short AD → AED almost disappears' appears", R(0, 250, 'Short $AD$ $\\rightarrow$ $S_{AED}\\approx0$', 36)),
            'Remember this picture: same base, apex on a parallel line.',
        ], _trap_diag(shade=True))], fig=True)
    _replace_say(M, 'solve-geo38-g178', 4, "Here we don't have enough givens",
                 ["Here we don't have enough givens to decide.",
                  "Notice: TR is free. Nothing in the givens fixes it. That's the 'find what is free' check."])

    # --- (c) Q10: the angle-bisector shortcut for strong students
    b = M.slide('solve-geo38-g184', 5)
    b['items'].append(R(0, 510, 'Shortcut: $\\dfrac{KN}{NL}=\\dfrac{KM}{ML}>1$', 32))
    M.edit_lines('solve-geo38-g184', 5, lambda ls: ls + [
        {'say': 'A shortcut for strong students: a bisector splits the opposite side in the same ratio as the two sides next to it.'},
        {'appear': len(b['items']) - 1, 'label': "'KN/NL = KM/ML > 1' appears"},
        {'say': 'KN to NL is like KM to ML. KM is the hypotenuse — longer than ML. So KN is longer than NL. One line.'}])
    S('geo38-g184', expl=['Drop NE perpendicular to KM. Right triangles MNE and MNL have equal angles at M and the same hypotenuse MN. They are congruent, therefore NE = NL.',
                          'In right triangle KNE, KN is the hypotenuse, therefore KN > NE = NL. Choice 3.',
                          'Shortcut: the bisector gives $\\frac{KN}{NL}=\\frac{KM}{ML}$, and $KM>ML$ (KM is the hypotenuse).'])

    # --- (d) goodbye only at the very end (Question 13 video)
    _replace_say(M, 'solve-geo38-g187', 3, "That's it — we've finished geometric understanding",
                 ["That's it — we've finished geometric understanding, and in fact we've finished geometry altogether.",
                  "What can I wish you? That you do as well in the other topics as you do in geometry — and I'm waiting for you there too."])

    # --- (e) memory card: after the last guided question, covering the whole topic
    M.move(CARD, LEARN, after='solve-geo38-g187')
    c = M.card(CARD)
    rows = c['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0].startswith('Vertex moves away from the segment'))
    rows[k] = ['Vertex moves straight away from the segment', 'the angle gets smaller (nearer $\\rightarrow$ opens toward $180°$)']
    k = next(i for i, r in enumerate(rows) if 'Anchor' in r[0])
    rows[k + 1:k + 1] = [
        ['!Two fixed sides, the angle opens', 'the third side gets longer · the height and area grow up to $90°$, then shrink · $\\theta$ and $180°-\\theta$ give the same area'],
        ['Greatest area with sides $a$, $b$', 'at $90°$: triangle $\\frac{ab}{2}$, parallelogram $ab$'],
        ['Acute, right or obtuse?', 'longest side $c$: $c^2=a^2+b^2$ right · $c^2>a^2+b^2$ obtuse · $c^2<a^2+b^2$ acute'],
        ['!Must / could / cannot', 'must = in every allowed case · could = in at least one · cannot = in none'],
        ['!Flexible drawing', 'exaggerate the drawing, but keep every given'],
        ['Extreme cases', '1 · push the free point to the end · 2 · put it in the middle · 3 · find what is free'],
        ['Cannot be determined?', 'the answer depends on something the givens do not fix (an angle, a side, a split)'],
        ['!Slide the apex', 'same base, apex on a parallel line $\\rightarrow$ the same area (the perimeter changes)'],
    ]
    c['tips'] = c['tips'] + ['Before you trust a drawing: which lengths and angles are really given?',
                             'The choices have a smallest and a largest value? Check the extremes first.']

    # ================================================================================
    # 3. TEXT
    # ================================================================================
    S('geo38-core-p03', expl=[
        'Try one example with coordinates: $A(0, 7)$, $C(0, 3)$, $E(0, 0)$, $B(4, 7)$, $D(2, 3)$, $F(8, 0)$. AB, CD and EF are all horizontal, so they are perpendicular to k.',
        'Check the right angle with Pythagoras: $BD^2=2^2+4^2=20$, $DF^2=6^2+3^2=45$, $BF^2=4^2+7^2=65=20+45$. So, ∠BDF = 90°.',
        'But $AB=4\\ne8=EF$, $AC=4\\ne3=CE$, and $BD=\\sqrt{20}\\ne\\sqrt{45}=DF$. None of the claims must be true: choice 4.'])
    S('geo38-core-p19', expl=[
        'Perimeter 28: every side is $\\frac{28}{4}=7$.',
        'Area = side × height: $h=\\frac{35}{7}=5$. A side of 7 that rises exactly 5 fixes how the rhombus leans. Leaning the other way gives a mirror image — the same rhombus.',
        'So there is exactly one rhombus: choice 1.'])
    S('geo38-core-p22', expl=['For a fixed perimeter, the rectangle closest to a square has the greatest area.',
                              'Each side of the square is $\\frac{36}{4}=9$. The greatest area is $9\\cdot9=81$ m².'])
    S('geo38-g174', expl=['Both plots are hexagons with the same area. The regular hexagon is more like a circle, so it needs less perimeter.',
                          'The nonregular hexagon has the greater perimeter: choice 3.'])
    S('geo38-g182', expl=['The center is 5 cm from A and from B. Cut P is $6-5=1$ cm from the center. Cut Q is $8-5=3$ cm from the center.',
                          'Each cut keeps the whole sphere surface and adds two flat disks. Closer to the center means a bigger disk: '
                          '$\\rho^2=25-1=24$ for P, $\\rho^2=25-9=16$ for Q.',
                          'Cut P gives the greater total: choice 2.'])

    # ================================================================================
    # 4. FIGURES
    # ================================================================================
    # v788: labels were cut off at the right edge and crossed by a line
    b = M.slide(MINMAX, 3)
    for it in b['items']:
        if it.get('k') == 'vis':
            s = it['v']['svg']
            s = s.replace('viewBox="141.4 4.0 409.5 370.0"', 'viewBox="141.4 4.0 580 370.0"')
            s = s.replace('x="380.0" y="252.0"', 'x="478.0" y="252.0"').replace('x="380.0" y="152.0"', 'x="478.0" y="152.0"')
            s = s.replace('x="380.0" y="37.0"', 'x="478.0" y="37.0"')
            s = s.replace('farther still: narrower', 'farthest: narrowest')
            it['v']['svg'] = s
    # p04: O label at the vertex
    q = M.q('geo38-core-p04'); s = q['questionVisual']['svg']
    S('geo38-core-p04', figure=s.replace('</svg>', _t(303, 220, 'O') + '</svg>'))
    # p06: the answer (the semicircle) was drawn
    s = M.q('geo38-core-p06')['questionVisual']['svg']
    S('geo38-core-p06', figure=re.sub(r'<path d="M 514\.667[^>]*/>', '', s))
    # p20: unexplained orange segment through O and E
    s = M.q('geo38-core-p20')['questionVisual']['svg']
    S('geo38-core-p20', figure=re.sub(r'<line x1="267\.440"[^>]*/>', '', s).replace('x="305.000" y="197.000"', 'x="320.000" y="200.000"')
      .replace('</svg>', _dot(360.091, 150.8) + '</svg>'))
    # p21: separate chords with their own distance lines; letters at the chord ends
    ox, oy, r, u = 320.0, 180.0, 121.667, 24.333
    ha, hc = math.sqrt(r * r - u * u), math.sqrt(r * r - 9 * u * u)
    S('geo38-core-p21', figure=_svg('0 0 640 360', 'Two chords at different distances from the center', [
        '<circle cx="320.000" cy="180.000" r="121.667" fill="none" stroke="%s" stroke-width="2.5"/>' % INK,
        _ln(ox - ha, oy - u, ox + ha, oy - u, TEAL), _ln(ox - hc, oy + 3 * u, ox + hc, oy + 3 * u, TEAL),
        _ln(ox, oy, ox, oy - u, ORANGE, 2.5, '7 5'), _ln(ox, oy, ox, oy + 3 * u, ORANGE, 2.5, '7 5'),
        _dot(ox, oy), _t(ox - 17, oy + 2, 'O'),
        _t(ox + 14, oy - u / 2, '1', ORANGE, 20, '700', 'start'), _t(ox + 14, oy + 1.5 * u, '3', ORANGE, 20, '700', 'start'),
        _t(ox - ha - 16, oy - u - 4, 'A'), _t(ox + ha + 16, oy - u - 4, 'B'),
        _t(ox - hc - 14, oy + 3 * u + 10, 'C'), _t(ox + hc + 14, oy + 3 * u + 10, 'D')]))

    # ================================================================================
    # 5. PRACTICE: remove repeats, add exam-level questions, order easy -> hard
    # ================================================================================
    M.unplace('geo38-core-p18')   # the same rectangle fact as p22
    M.unplace('geo38-core-p26')   # a plain counting repeat (T28)
    NEW = [
        ('q-r26-t38-03', 'A parallelogram has sides 4 cm and 9 cm. Its angles can change. What is its greatest possible area?',
         ['$18$ cm²', '$26$ cm²', '$13$ cm²', '$36$ cm²'], 4,
         ['Take the side of 9 as the base. Area = $9\\cdot h$, and the height is at most the other side, 4.',
          'The height is 4 when the angle is $90°$ (a rectangle): $9\\cdot4=36$ cm².'], None),
        ('q-r26-t38-04', 'AB is a diameter of a circle. Point P is not on line AB, and ∠APB = 100°. Where is P?',
         ['On the circle', 'Inside the circle', 'Outside the circle', 'It cannot be determined from the information given.'], 2,
         ['On the circle, an angle on a diameter is exactly $90°$.',
          'Closer to AB (inside the circle), the angle opens: more than $90°$. Farther (outside), it closes: less than $90°$.',
          '$100°>90°$, therefore P is inside the circle.'], None),
        ('q-r26-t38-05', 'A triangle has side lengths 5 cm, 12 cm and $x$ cm, where $x$ is the longest side and $13<x<17$. '
                         'Which of the following is necessarily true about the angle opposite the side of length $x$?',
         ['It is obtuse.', 'It is a right angle.', 'It is acute.', 'It cannot be determined from the information given.'], 1,
         ['Anchor: $5, 12, 13$ is a right triangle ($25+144=169=13^2$).',
          'Here $x>13$, therefore $x^2>169=5^2+12^2$. The side opposite the angle is longer than in the right triangle, so the angle is obtuse.'], None),
        ('q-r26-t38-06', 'Lines k and m are parallel, and the distance between them is 4 cm. A and B lie on m, and AB = 6 cm. '
                         'Point P moves along line k. Which of the following is necessarily true about triangle ABP?',
         ['Its area and its perimeter do not change.', 'Its area is always 12 cm², and its perimeter changes.',
          'Its area changes, and its perimeter does not change.', 'Its area and its perimeter both change.'], 2,
         ['The base AB = 6 is fixed, and the height is always the distance between the lines, 4. Area: $\\frac{6\\cdot4}{2}=12$ cm², wherever P is.',
          'Slide P far along k: AP and BP get very long. The perimeter changes. Choice 2.'], _moving_p()),
        ('q-r26-t38-07', 'A cube is cut by one flat plane. Which of the following cannot be the shape of the cut face?',
         ['A triangle', 'A rectangle that is not a square', 'A regular hexagon', 'A shape with 7 sides'], 4,
         ['Each side of the cut face lies on one face of the cube, and the plane meets each face at most once. The cube has 6 faces, so the cut face has at most 6 sides.',
          'A triangle: cut off a corner. A rectangle that is not a square: cut through two opposite edges. A regular hexagon: cut through the center, straight across a long diagonal of the cube.',
          'A shape with 7 sides is impossible: choice 4.'], None),
        ('q-r26-t38-08', 'An ant walks on the surface of a cube with edge 2 cm, from one corner to the opposite corner (the corner farthest from it). '
                         'What is the length of the shortest path?',
         ['$2\\sqrt3$ cm', '$2\\sqrt5$ cm', '$2+2\\sqrt2$ cm', '$6$ cm'], 2,
         ['Unfold two neighboring faces into one flat $2\\times4$ rectangle. The shortest path is its diagonal: $\\sqrt{4^2+2^2}=\\sqrt{20}=2\\sqrt5\\approx4.5$.',
          'Traps: $2\\sqrt3$ goes through the inside of the cube (not allowed). A face diagonal and then an edge is $2+2\\sqrt2\\approx4.8$, and three edges are 6. Both are longer.'], None),
        ('q-r26-t38-09', 'Triangle 1 has two sides of 5 cm and 8 cm with a 50° angle between them. '
                         'Triangle 2 has two sides of 5 cm and 8 cm with a 130° angle between them. Which of the following is true?',
         ['The areas are equal, and the third sides are equal.', 'The areas are equal, and triangle 2 has the longer third side.',
          'Triangle 2 has the greater area.', 'Triangle 1 has the greater area, and triangle 2 has the longer third side.'], 2,
         ['Take the side of 8 as the base. At $50°$ and at $130°$, the side of 5 leans by the same amount (to different sides), so it reaches the same height. Same base, same height: the areas are equal.',
          'The third side: the same two sides with a wider angle give a longer third side. $130°>50°$, therefore triangle 2 has the longer third side. Choice 2.'], None),
        ('q-r26-t38-10', 'Two sides of a triangle are 6 cm and 8 cm long. Which of the following cannot be the area of the triangle?',
         ['$12$ cm²', '$24$ cm²', '$25$ cm²', '$20$ cm²'], 3,
         ['The greatest area is at $90°$: $\\frac{6\\cdot8}{2}=24$.',
          'Closing the angle makes the area as small as we like, so every area between 0 and 24 is possible (12, 20 and 24 too).',
          '25 is more than 24: impossible. Choice 3.'], None),
        ('q-r26-t38-11', "A circle and a square have the same perimeter. What is the ratio of the circle's area to the square's area?",
         ['$\\pi:4$', '$1:1$', '$4:\\pi$', '$2:\\pi$'], 3,
         ['Plug in a convenient perimeter: $4\\pi$.',
          'Square: side $\\pi$, area $\\pi^2$. Circle: $2\\pi r=4\\pi$, so $r=2$ and the area is $4\\pi$.',
          'The ratio is $4\\pi:\\pi^2=4:\\pi$. Since $\\pi<4$, the circle is bigger, as shape efficiency says.'], None),
    ]
    for qid, stem, ch, cor, ex, fig in NEW:
        M.new_q(qid, TOPIC, stem, ch, cor, ex, figure=fig)
        M.place_q(qid, PRACT)
    P = lambda n: 'geo38-core-p%02d' % n
    M.practice_order(PRACT, [
        P(22), P(23), P(24), P(21), P(1), P(4), 'q-r26-t38-04', 'q-r26-t38-03', P(5), P(25), 'q-r26-t38-05', P(20),
        P(13), P(14), 'q-r26-t38-06', P(9), P(6), P(7), 'q-r26-t38-07', 'q-r26-t38-08', P(2), P(10), P(16), P(8),
        'q-r26-t38-09', 'q-r26-t38-10', 'q-r26-t38-11', P(12), P(11), P(19), P(3), P(15), P(17)])

    # ================================================================================
    # 6. CLEAN-UP: American spelling, "so" = therefore, hyphens in words on pre-loaded canvases
    # ================================================================================
    for f in [f for f in M.D['flow'] if f['topic'] == TOPIC]:
        if f['type'] == 'question':
            q = M.q(f['ref']); ex = q.get('explanation') or []
            new = [_so(e) for e in ex]
            if new != ex: S(f['ref'], expl=new)
        if f['type'] != 'video': continue
        v = M.video(f['ref']); ch = False
        for b in v['beats']:
            for key in ('canvas', 'loads'):
                if b.get(key):
                    nb = re.sub(r'(?<=\d)−(?=[a-z])', '-', b[key])
                    if nb != b[key]: b[key] = nb; ch = True
            for l in b['lines']:
                if 'say' in l:
                    ns = _so(_us(l['say']))
                    if ns != l['say']: l['say'] = ns; ch = True
        if ch: M.touched_videos.add(f['ref'])
