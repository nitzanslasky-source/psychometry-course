"""Topic 30 - Lines and angles. Course review 2026-09 fixes.
Pass 2 (teacher-approved remove/restore plan): the C-shape bend and the units-digit tip are removed; the "dot in the
right-angle square" line, foundation p09, p14 (original) and p15 are restored; a summary video comes before each practice.
See t30_CHANGES.md for the plain-language list."""
import math
import re
from dsl import T, H, A, D, Q

TOPIC = 30
L1 = 'geo-001'           # lesson "Lines and Angles"
L2 = 'geo-004'           # lesson "Lines and Angles: Advanced"
LEARN1 = 'geo30-learn-1'
LEARN2 = 'geo30-learn-2'
FOUND = 'geo30-foundation-practice'
ADV = 'geo30-advanced-practice'
# Sidebars use the OLD question numbers; renumber_guided() maps them to the final order.
# New guided questions are created as 5, 6 (learn section 1) and 7 (learn section 2).
LEARN1_SB = ['Question 1', 'Question 5', 'Question 6']
LEARN2_SB = ['Question 2', 'Question 3', 'Question 4', 'Question 7']
NEW = ['q-r26-t30-%02d' % k for k in range(0, 12)]   # NEW[1] ... NEW[10]

# ------------------------------------------------------------------------------------------
# SVG helpers (same style as the course figures: 640x360, #203344 lines, #087f83 marks)
# ------------------------------------------------------------------------------------------
INK, MARK = '#203344', '#087f83'
FONT = 'DejaVu Sans,Arial,sans-serif'


def _svg(label, body, vb='0 0 640 360'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, ''.join(body)))


def _ln(x1, y1, x2, y2, c=INK, w=2.5):
    return '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%s"/>' % (x1, y1, x2, y2, c, w)


def _tx(x, y, t, c=INK, size=20, anchor='middle'):
    return ('<text x="%.3f" y="%.3f" text-anchor="%s" dominant-baseline="middle" fill="%s" font-family="%s" font-size="%d">%s</text>'
            % (x, y, anchor, c, FONT, size, t))


def _pt(r, deg, cx, cy):
    return cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg))


def _arc(cx, cy, r, a1, a2):
    """Arc of an angle at (cx, cy) from math angle a1 to a2 (degrees, counterclockwise, y up)."""
    x1, y1 = _pt(r, a1, cx, cy); x2, y2 = _pt(r, a2, cx, cy)
    big = 1 if (a2 - a1) % 360 > 180 else 0
    return ('<path d="M %.3f %.3f A %.3f %.3f 0 %d 0 %.3f %.3f" fill="none" stroke="%s" stroke-width="2"/>'
            % (x1, y1, r, r, big, x2, y2, MARK))


def _alab(cx, cy, r, a1, a2, t, anchor='middle'):
    """Angle label on the bisector, at distance r."""
    x, y = _pt(r, (a1 + a2) / 2.0, cx, cy)
    return _tx(x, y, t, MARK, 18, anchor)


def _right(cx, cy, a1, a2, s=12):
    x1, y1 = _pt(s, a1, cx, cy); x2, y2 = _pt(s, a2, cx, cy)
    xm, ym = x1 + x2 - cx, y1 + y2 - cy
    return _ln(x1, y1, xm, ym, MARK, 1.7) + _ln(xm, ym, x2, y2, MARK, 1.7)


def _dot(x, y):
    return '<circle cx="%.3f" cy="%.3f" r="3.2" fill="%s"/>' % (x, y, INK)


def _crop(svg, vb):
    return re.sub(r'viewBox="[^"]*"', 'viewBox="%s"' % vb, svg, count=1)


def _walk(start, steps):
    """Bent line: start point, then (math direction in degrees, vertical drop) pieces. Returns the points."""
    pts = [start]
    for deg, drop in steps:
        x, y = pts[-1]; L = drop / abs(math.sin(math.radians(deg)))
        pts.append(_pt(L, deg, x, y))
    return pts


def _dir(p, q):
    return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0])) % 360


# --- lesson figures ------------------------------------------------------------------------
def fig_z_fixed(old):
    """v10 (slide 'Look for the Z'): move the two alpha marks INTO the corners of the highlighted Z."""
    body = re.sub(r'<path d="M 392\.525.*?</text><path d="M 247\.475.*?</text>', '', old)
    assert body != old, 'Z figure changed'
    tx, ty, bx, by = 360.892, 121.6, 279.108, 238.4
    t = math.degrees(math.atan2(243.334, 170.384))           # slope of the transversal, about 55 degrees
    add = (_arc(tx, ty, 31.633, 180, 180 + t) + _alab(tx, ty, 50, 180, 180 + t, 'α')
           + _arc(bx, by, 31.633, 0, t) + _alab(bx, by, 50, 0, t, 'α'))
    return body.replace('</svg>', add + '</svg>')


def fig_vertical_fixed(old):
    """v5 (slide 'Vertical angles'): keep only the 40-degree arc (the big 220-degree arc is removed)."""
    new = re.sub(r'<path d="M 343\.966 159\.890.*?/><path d="M 288\.714 180\.000.*?/>', '', old)
    assert new != old, 'v5 changed'
    return new


def fig_segments_demo():
    y = 170; xs = [(150, 'A'), (270, 'B'), (350, 'C'), (490, 'D')]
    b = [_ln(110, y, 530, y)]
    for x, n in xs: b += [_dot(x, y), _tx(x, y + 24, n)]
    b += [_ln(150, 120, 350, 120, MARK, 3), _tx(250, 104, 'AC', MARK, 18),
          _ln(270, 140, 490, 140, MARK, 3), _tx(380, 124, 'BD', MARK, 18)]
    return _svg('Points A, B, C and D on a line; segments AC and BD overlap on BC', b, '90 80 460 130')


def fig_u_shape():
    ay, by_, bx = 121.6, 238.4, 279.108
    t = math.degrees(math.atan2(243.334, 170.384)); tx = bx + (by_ - ay) / math.tan(math.radians(t))
    b = [_ln(105.867, ay, 534.133, ay), _ln(105.867, by_, 534.133, by_),
         _ln(234.808, 301.667, 405.192, 58.333), _tx(93.7, ay, 'a'), _tx(93.7, by_, 'b'),
         _ln(tx, ay, 466, ay, MARK, 5), _ln(tx, ay, bx, by_, MARK, 5), _ln(bx, by_, 466, by_, MARK, 5),
         _arc(tx, ay, 28, 180 + t, 360), _alab(tx, ay, 50, 180 + t, 360, 'β'),
         _arc(bx, by_, 31.633, 0, t), _alab(bx, by_, 50, 0, t, 'α')]
    return _svg('Parallel lines cut by a transversal; a U shape holds two angles on the same side', b, '61.7 32.3 498.4 295.3')


# --- question figures ----------------------------------------------------------------------
def fig_g1():
    """a and b both perpendicular to c; transversal d; 50 at a, x at b."""
    a, b_, cx = 110, 250, 170
    t = 50; xb = 330; xa = xb + (b_ - a) / math.tan(math.radians(t))
    lo = _pt(40 / math.sin(math.radians(t)), 180 + t, xb, b_); hi = _pt(40 / math.sin(math.radians(t)), t, xa, a)
    bd = [_ln(120, a, 540, a), _ln(120, b_, 540, b_), _ln(cx, 60, cx, 300), _ln(lo[0], lo[1], hi[0], hi[1]),
          _tx(105, a, 'a'), _tx(105, b_, 'b'), _tx(cx, 46, 'c'), _tx(hi[0] + 10, hi[1] - 12, 'd'),
          _right(cx, a, 0, 90), _right(cx, b_, 0, 90),
          _arc(xa, a, 28, 0, t), _alab(xa, a, 48, 0, t, '50°'),
          _arc(xb, b_, 22, t, 180), _alab(xb, b_, 42, t, 180, 'x')]
    return _svg('Lines a and b are perpendicular to line c; line d crosses a and b', bd)


def fig_g2():
    y = 180; u = 18; x0 = 140
    xs = [(0, 'A'), (6, 'B'), (11, 'C'), (20, 'D')]
    bd = [_ln(105, y, 535, y)]
    for k, n in xs: bd += [_dot(x0 + u * k, y), _tx(x0 + u * k, y + 24, n)]
    return _svg('Points A, B, C and D on a line, in this order', bd, '90 130 460 90')


def _bent(pts, labels, title, vb='0 0 640 360'):
    """Parallel lines y=90 and y=290 with a bent line through pts; labels = [(vertex index, a1, a2, text), ...]."""
    bd = [_ln(120, 90, 540, 90), _ln(120, 290, 540, 290), _tx(106, 90, 'a'), _tx(106, 290, 'b')]
    for p, q in zip(pts, pts[1:]): bd.append(_ln(p[0], p[1], q[0], q[1]))
    for k, a1, a2, t in labels:
        x, y = pts[k]; r = 22 if k not in (0, len(pts) - 1) else 26
        lr = r + 32 if k == len(pts) - 1 else r + 20
        bd += [_arc(x, y, r, a1, a2), _alab(x, y, lr, a1, a2, t)]
    return _svg(title, bd, vb)


def fig_g3():
    # angles: 40 at a, x at the first bend, 65 at the second bend, 35 at b
    pts = _walk((250.0, 90.0), [(-40, 64.28), (210, 45.0), (-35, 90.72)])
    return _bent(pts, [(0, -40, 0, '40°'), (1, 140, 210, 'x'), (2, -35, 30, '65°'), (3, 145, 180, '35°')],
                 'Parallel lines a and b with a line that bends twice between them')


def fig_p07():
    # angles: 50 at a, 80 at the first bend, x at the second bend, 20 at b
    pts = _walk((230.0, 90.0), [(-50, 70.0), (210, 50.0), (-20, 80.0)])
    return _bent(pts, [(0, -50, 0, '50°'), (1, 130, 210, '80°'), (2, -20, 30, 'x'), (3, 160, 180, '20°')],
                 'Parallel lines a and b with a line that bends twice between them')


def _transversal(deg, top_label, bot_label, top_arc, bot_arc, title, names=('a', 'b', 't'), lines=None):
    """Two horizontal lines (y=110, y=250) and a transversal at angle deg through (300, 250)."""
    ay, by_, xb = 110, 250, 300
    xa = xb + (by_ - ay) / math.tan(math.radians(deg))
    lo = _pt(40 / math.sin(math.radians(deg)), 180 + deg, xb, by_); hi = _pt(40 / math.sin(math.radians(deg)), deg, xa, ay)
    bd = lines or [_ln(130, ay, 520, ay), _ln(130, by_, 520, by_)]
    bd = bd + [_ln(lo[0], lo[1], hi[0], hi[1]), _tx(116, ay, names[0]), _tx(116, by_, names[1]),
               _tx(hi[0] + 12, hi[1] - 10, names[2])]
    (a1, a2, ra), (b1, b2, rb) = top_arc, bot_arc
    bd += [_arc(xa, ay, 26, a1, a2), _alab(xa, ay, ra, a1, a2, top_label),
           _arc(xb, by_, 26, b1, b2), _alab(xb, by_, rb, b1, b2, bot_label)]
    return _svg(title, bd)


def fig_p04():
    # 2026-10-01: nothing says a || b, but the U on line t (108° + 72° = 180°) proves it; x sits in a U on line s
    ay, by_ = 110, 250
    bd = [_ln(100, ay, 580, ay), _ln(100, by_, 580, by_), _tx(86, ay, 'a'), _tx(86, by_, 'b')]
    arcs = {'t': ((252, 360, 48, '108°'), (0, 72, 46, '72°')), 's': ((305, 360, 50, '55°'), (0, 125, 40, 'x'))}
    for xb, deg, name in ((230, 72, 't'), (480, 125, 's')):
        xa = xb + (by_ - ay) / math.tan(math.radians(deg))
        ext = 40 / math.sin(math.radians(deg))
        lo = _pt(ext, 180 + deg, xb, by_); hi = _pt(ext, deg, xa, ay)
        bd += [_ln(lo[0], lo[1], hi[0], hi[1]), _tx(hi[0] + (12 if deg < 90 else -12), hi[1] - 10, name)]
        (a1, a2, ra, la), (b1, b2, rb, lb) = arcs[name]
        bd += [_arc(xa, ay, 26, a1, a2), _alab(xa, ay, ra, a1, a2, la),
               _arc(xb, by_, 26, b1, b2), _alab(xb, by_, rb, b1, b2, lb)]
    return _svg('Lines t and s cross lines a and b', bd)


def fig_p05():
    return _transversal(70, '4x + 10°', '2x + 20°', (250, 360, 62), (0, 70, 62), 'Parallel lines a and b cut by a transversal')


def fig_p10():
    return _transversal(73, '107°', '73°', (253, 360, 52), (0, 73, 50), 'Line t crosses lines a and b')


def fig_adv05():
    """Three lines through O: horizontal, 72 and 116 degrees. 116 = from 0 to 116; 136 = from 116 to 252; x = 180..252."""
    O = (320.0, 180.0); R = 150
    bd = []
    for d in (0, 72, 116):
        p, q = _pt(R, d, *O), _pt(R, d + 180, *O); bd.append(_ln(p[0], p[1], q[0], q[1]))
    bd += [_arc(O[0], O[1], 58, 0, 116), _alab(O[0], O[1], 78, 0, 116 - 30, '116°'),
           _arc(O[0], O[1], 40, 116, 252), _alab(O[0], O[1], 58, 125, 165, '136°'),
           _arc(O[0], O[1], 22, 180, 252), _alab(O[0], O[1], 36, 180, 252, 'x'),
           _tx(O[0] + 20, O[1] + 12, 'O', INK, 18)]
    return _svg('Three lines meet at O; angles of 116 and 136 degrees overlap', bd)


def fig_adv10():
    """Three lines through one point: horizontal, 70 and 120 degrees. p = 0..120, q = 70..180, x = 70..120."""
    O = (320.0, 190.0); R = 150
    bd = []
    for d in (0, 70, 120):
        p, q = _pt(R, d, *O), _pt(R, d + 180, *O); bd.append(_ln(p[0], p[1], q[0], q[1]))
    bd += [_arc(O[0], O[1], 36, 0, 120), _alab(O[0], O[1], 52, 0, 35, 'p'),
           _arc(O[0], O[1], 62, 70, 180), _alab(O[0], O[1], 78, 150, 170, 'q'),
           _arc(O[0], O[1], 88, 70, 120), _alab(O[0], O[1], 104, 90, 100, 'x')]
    return _svg('Three lines meet at one point; angles p and q overlap on the angle x', bd)


# ------------------------------------------------------------------------------------------
# small editing helpers
# ------------------------------------------------------------------------------------------
def _fix_say(M, vid, n, old, new):
    def fn(lines):
        hit = False
        for l in lines:
            if 'say' in l and old in l['say']: l['say'] = l['say'].replace(old, new); hit = True
        assert hit, (vid, n, old)
        return lines
    M.edit_lines(vid, n, fn)


def _set_vis(M, vid, n, fn):
    for it in M.slide(vid, n)['items']:
        if it.get('k') == 'vis': it['v']['svg'] = fn(it['v']['svg']); M.touched_videos.add(vid); return
    raise KeyError((vid, n))


def _set_qfig(M, qid, svg):
    """Question figure + every pre-loaded copy on slides (their viewBox crop is kept)."""
    M.set_q(qid, figure=svg)
    for v in M.D['videos'].values():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and isinstance(it.get('fig'), dict):
                    vb = re.search(r'viewBox="([^"]*)"', it['fig']['svg']).group(1)
                    it['fig']['svg'] = _crop(svg, vb); M.touched_videos.add(v['id'])


def _qpre(qid, fig=None):
    return [Q(qid, fig={'type': 'geometry', 'svg': fig}, figw=0.56, figalign='left')] if fig else [Q(qid)]


def _bt(t, y, size=34):
    """Board text next to a pre-loaded question."""
    return T(t, size=size, x=1060, y=y, w=470)


def _solution(M, qid, sb, section, num, intro, slides):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script, pre in slides:
        beats.append(dict(mode='question', active=sb.index('Question %d' % n), title=title, pre=pre, script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Lines and Angles Questions', sb, beats, section, kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Lines and Angles Question' if section == LEARN1 else 'Lines and Angles Questions'
    v['hybrid']['num'] = num
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


GIVEN = lambda *eqs: 'Given:\n$\\begin{cases} ' + ' \\\\ '.join(eqs) + ' \\end{cases}$\n'
CBD = 'It cannot be determined from the information given.'


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Lesson "Lines and Angles" (geo-001)
    # =====================================================================================
    # --- slide 13 Recap (rewritten; done first so later insertions don't move it) ---
    M.set_slide(L1, 13, script=[
        A("'Full circle 360° · Straight angle 180° · Right angle 90°' appears",
          T('Full circle $360°$ · Straight angle $180°$ · Right angle $90°$ (only if marked)', size=36)),
        A("'Adjacent angles on a straight line: sum 180° · Vertical angles: equal' appears",
          T('Adjacent angles on a straight line: sum $180°$ · Vertical angles: equal', size=36)),
        A("'Parallel lines: small = small, large = large, small + large = 180°' appears",
          T('Parallel lines: small $=$ small · large $=$ large · small $+$ large $=180°$', size=36)),
        A("'Z → equal · U → sum 180°' appears", T('Z $\\to$ equal · U $\\to$ sum $180°$', size=36)),
        A("'Parallel only if given or proved' appears",
          T('$\\perp$ or $\\parallel$ to the same line $\\to$ parallel · never assume from the picture', size=36)),
        A("'Segments: count the gaps' appears", T('Segments: count the gaps · $AC+BD=AD+BC$', size=36)),
        D("Underline 'Z' and 'U'"),
        "Those are the rules. Now let's see a sample question.",
    ])
    # --- slide 12 Look for the Z: the two alpha marks now sit inside the Z corners ---
    _set_vis(M, L1, 12, fig_z_fixed)
    M.edit_lines(L1, 12, lambda ls: [dict(l, label='Parallel lines with a Z shape and the two equal angles in its corners appear')
                                     if 'appear' in l else l for l in ls])
    _fix_say(M, L1, 12, 'The Z holds two angles inside it. The angle here and the angle here — the two angles in the corners of the Z — are equal.',
             'The Z holds two angles inside it — one in each corner. The angle here, under line a, and the angle here, above line b. They are equal.')
    _fix_say(M, L1, 12, 'In school these have names: alternate, corresponding, co-interior and so on. We don\'t really need them.',
             'In school these have names: alternate, corresponding and so on. We don\'t really need them.')
    # --- new slide after the Z: the U shape ---
    M.insert_slides(L1, 12, [dict(mode='concept', active=0, title='The U shape', script=[
        "One more shape: the U.",
        A('Parallel lines with a U shape and the two angles inside it appear', dict(k='vis', v={'type': 'geometry', 'svg': fig_u_shape()}, w=1000, h=440)),
        "Here the two angles sit inside a U. Same side of the transversal, between the two lines.",
        "They are not equal. One is small, one is large.",
        A("'Inside the U: α + β = 180°' appears", T('Inside the U: $\\alpha+\\beta=180°$', size=46, x=410, y=640)),
        "Small plus large — 180. So the two angles inside a U add up to 180.",
        D('Write "α = 55° → β = 180° − 55° = 125°"'),
        "If the small one is 55, the large one is 125.",
        "So: Z — the angles are equal. U — they add up to 180.",
    ])])
    # --- slide 10 Parallel lines: one more line + new slide "Parallel or not?" ---
    M.insert_slides(L1, 10, [dict(mode='concept', active=0, title='Parallel or not?', script=[
        "When do we KNOW that two lines are parallel? Three rules.",
        A("'Two lines ⊥ the same line → parallel' appears", T('Two lines $\\perp$ the same line $\\to$ parallel', size=42)),
        D('Draw a vertical line c, and two horizontal lines crossing it, each with a square mark'),
        "Two lines, both perpendicular to the same line. Both cross it at 90 degrees — they go in the same direction. They never meet. Parallel.",
        A("'Two lines ∥ the same line → parallel' appears", T('Two lines $\\parallel$ the same line $\\to$ parallel', size=42)),
        "Two lines, both parallel to a third line — they are parallel to each other too.",
        A("'Equal small angles, or small + large = 180° → parallel' appears",
          T('A transversal makes equal small angles, or small $+$ large $=180°$ $\\to$ parallel', size=40)),
        "And the reverse of what's coming next: if the angles behave like parallel-line angles — the lines are parallel.",
        A("'Not to scale: parallel only if given or proved · 90° only if marked' appears",
          T('Figures are not to scale: parallel only if given or proved · $90°$ only if marked', size=40)),
        "Now the trap. On the exam, figures are not drawn to scale.",
        "Two lines can LOOK parallel. Don't trust your eyes.",
        "Parallel only if it's given, or one of these rules proves it. Ninety degrees only if it's marked or given.",
        "Nothing given? Don't assume they're parallel. First look for one of these three rules in the figure. It's often there.",
    ])])
    # --- slide 8 bisector: "÷", not ":" ---
    b = M.slide(L1, 8)
    for it in b['items']:
        if it.get('t') == '$72°:2=36°$': it['t'] = '$72°\\div2=36°$'
    M.edit_lines(L1, 8, lambda ls: [dict(l, label='72° ÷ 2 = 36° appears') if l.get('label') == '72° : 2 = 36° appears' else l for l in ls])
    # --- slide 7 vertical angles: one arc only (the 40-degree angle) ---
    _set_vis(M, L1, 7, fig_vertical_fixed)
    # --- slide 6 adjacent angles: "on a straight line" ---
    _fix_say(M, L1, 6, 'Adjacent angles: two neighbouring angles formed where two lines cross — and together they add up to 180.',
             'Adjacent angles on a straight line: two angles side by side, on one straight line. Together they add up to 180.')
    M.edit_lines(L1, 6, lambda ls: ls + [{'say': "Careful: two angles side by side that are NOT on one straight line don't have to add up to 180."}])
    # --- slide 4 right angle: keep the (true) "dot" line; add: never assume 90 ---
    def _add_rule(ls):
        k = next(i for i, l in enumerate(ls) if l.get('say', '').startswith('On the psychometric exam, in almost every case'))
        return ls[:k + 1] + [{'say': "The rule for the exam: an angle is 90 degrees only if it's marked like this, or it's given. Looks like 90? That's not enough."}] + ls[k + 1:]
    M.edit_lines(L1, 4, _add_rule)
    # --- new slide after 2: segments on a line ---
    M.insert_slides(L1, 2, [dict(mode='concept', active=0, title='Segments on a line', script=[
        "Points on one line make segments. Two tricks for the exam.",
        A('Points A, B, C and D on a line, with AC and BD marked, appear', dict(k='vis', v={'type': 'geometry', 'svg': fig_segments_demo()}, w=1000, h=300)),
        "A, B, C and D, in this order. Look at AC and BD. They overlap — BC is inside both.",
        A("'AC + BD = AD + BC' appears", T('$AC+BD=AD+BC$', size=48, x=410, y=520)),
        "So AC plus BD covers the whole AD — and BC one more time.",
        D('Write "AC = 9, BD = 10, AD = 15 → 9 + 10 = 15 + BC → BC = 4"'),
        "Nine plus ten is nineteen. The whole is fifteen. The extra four is BC.",
        A("'Equal parts: count the gaps, not the points' appears", T('Equal parts: count the gaps, not the points', size=44, x=410, y=640)),
        D('Draw 5 equally spaced dots on a line and number the 4 gaps between them'),
        "Second trap. Five points, equally spaced. How many gaps? Four, not five.",
        "Lengths live in the gaps. Count the spaces between the points.",
    ])])
    # --- slide 1: strong students may skip ---
    M.edit_lines(L1, 1, lambda ls: ls[:-1] + [{'say': "Already know the basic definitions? Skip ahead to 'Parallel lines' — but don't skip 'Segments on a line' and 'Parallel or not?'."}, ls[-1]])
    # --- actives + sidebar (slides now: 1 title, 2..16) ---
    SB1 = ['Lines and segments', 'Segments on a line', 'Angles at a point', 'Right angle', 'Acute/obtuse/straight',
           'Adjacent angles', 'Vertical angles', 'Angle bisector', 'Naming angles', 'Parallel lines', 'Parallel or not?',
           'Small and large angles', 'Look for the Z', 'The U shape', 'Recap']
    for n in range(2, 17): M.set_slide(L1, n, active=n - 2)
    M.set_sidebar(L1, SB1)

    # =====================================================================================
    # 2. Memory card
    # =====================================================================================
    c = M.card('mem-lines-angles')
    c['tables'][0]['rows'] = [
        ['Full circle (angles around a point)', '$360°$', 'four angles at a crossing add to $360°$'],
        ['Straight angle', '$180°$', 'half of a full circle — a straight line'],
        ['Right angle', '$90°$', 'only if marked with a small square, or given'],
        ['Acute / obtuse', '$<90°$ / $>90°$', 'next to an acute angle sits an obtuse one'],
        ['Adjacent angles on a straight line', 'sum $180°$', 'one acute + one obtuse, or $90°+90°$'],
        ['Vertical angles', 'equal', 'they complete the same angle to $180°$'],
        ['Angle bisector', 'two equal halves', '$\\alpha$ and $\\alpha$'],
        ['Parallel lines + transversal', 'small = small, large = large', 'small + large $=180°$'],
        ['Z shape', 'the two angles in its corners are equal', 'look for the Z first'],
        ['U shape', 'the two angles inside it add to $180°$', 'one small, one large'],
        ['When are lines parallel?', '$\\perp$ to the same line, or $\\parallel$ to the same line', 'or equal small angles / small + large $=180°$'],
        ['Not to scale', 'parallel only if given or proved', 'looks parallel $\\ne$ parallel'],
        ['Bent line (Z-type bends)', 'angles pointing left $=$ angles pointing right', 'one bend: $x=a+b$'],
        ['Segments on a line', '$AC+BD=AD+BC$', 'equal parts: count the gaps, not the points'],
    ]
    c['tips'] = [
        'Letters instead of numbers? Plug in round numbers that look like the figure. Check that the four answers come out different — if two tie, plug in again.',
        'Overlapping angles: add them and subtract the full turn ($360°$) or the straight angle ($180°$).',
        'A bent line between parallels? Draw a line through each bend, parallel to both. It always works.',
        'Adding angles to $180°$? Use the units digit: $83°+54°+x=180°$ → $3+4=7$. Therefore, $x$ ends in $3$.',
        'Two lines look parallel, but nothing says so? Look for a rule that proves it: two angles inside a U that add up to $180°$, equal small angles, or two lines $\\perp$ to the same line.',
    ]

    # =====================================================================================
    # 3. Guided Question 1 (geo30-g002): figure without the stray arc, clean text
    # =====================================================================================
    q1fig = M.q('geo30-g002')['questionVisual']['svg']
    new = q1fig.replace('<path d="M 264.772 238.400 A 31.633 31.633 0 0 0 284.555 267.730" fill="none" stroke="#087f83" stroke-width="2"/>', '')
    assert new != q1fig
    _set_qfig(M, 'geo30-g002', new)
    S('geo30-g002', stem='In the accompanying figure, $a\\parallel b$. The marked lines are perpendicular. What is the value of $x$?',
      expl=['$a\\parallel b$, and small angles are equal. At line $b$, the angle between the transversal and line $b$ (above $b$) is also $68°$.',
            'The marked right angle is made of this $68°$ angle and $x$: $68°+x=90°$.',
            'Therefore, $x=90°-68°=22°$. Choice 3.'])

    # =====================================================================================
    # 4. New guided question: perpendicular to the same line (learn section 1)
    # =====================================================================================
    g1 = NEW[1]; f1 = fig_g1()
    M.new_q(g1, TOPIC, 'In the accompanying figure, lines $a$ and $b$ are both perpendicular to line $c$. Line $d$ crosses lines $a$ and $b$. What is the value of $x$?',
            ['$50°$', '$40°$', '$130°$', CBD], 3,
            ['$a\\perp c$ and $b\\perp c$. Two lines perpendicular to the same line are parallel. Therefore, $a\\parallel b$.',
             'Now $d$ is a transversal of two parallel lines. The $50°$ angle is a small angle, and $x$ is a large angle.',
             'Small $+$ large $=180°$: $x=180°-50°=130°$. Choice 3.',
             'Choice 4 is the trap: "$a\\parallel b$" is not written, but the two right angles prove it.'], figure=f1)
    M.place_q(g1, LEARN1, after='solve-geo30-g002')
    _solution(M, g1, LEARN1_SB, LEARN1, 2, ["A question where the parallel lines are hidden."], [
        ('Prove it is parallel', [
            "Lines a and b are both perpendicular to line c. Line d crosses them. What is x?",
            "Is a parallel to b? The question doesn't say so. Can we prove it?",
            D('Point to the two square marks on line c'),
            "Yes. Two lines perpendicular to the same line are parallel.",
            A("'a ⊥ c, b ⊥ c → a ∥ b' appears", _bt('$a\\perp c,\\ b\\perp c\\ \\to\\ a\\parallel b$', 250, 36)),
            "Now it's the usual picture: two parallel lines and a transversal, d.",
            "The 50 at line a is a small angle. x is a large angle.",
            D('Mark the 50° angle "small" and x "large"'),
            A("'x = 180° − 50° = 130°' appears", _bt('$x=180°-50°=130°$', 330, 38)),
            "Small plus large is 180. So x is 180 minus 50: 130.",
            D('Circle choice 3'),
            "Choice three.",
            "The trap is choice four. Parallel is not written — but the two right angles prove it.",
        ], _qpre(g1, _crop(f1, '95 35 460 270'))),
    ])

    # =====================================================================================
    # 5. New guided question: segments on a line (learn section 1)
    # =====================================================================================
    g2 = NEW[2]; f2 = fig_g2()
    M.new_q(g2, TOPIC, 'Points $A$, $B$, $C$ and $D$ lie on a line in this order, as shown in the accompanying figure.\n'
            + GIVEN('AC=11', 'BD=14', 'AD=20') + 'What is the length of $BC$?',
            ['$9$', '$6$', '$5$', '$25$'], 3,
            ['$AC$ and $BD$ overlap on $BC$: $AC+BD=AD+BC$.',
             '$11+14=20+BC$. Therefore, $25=20+BC$ and $BC=5$. Choice 3.',
             'Step by step: $AB=AD-BD=20-14=6$, and $BC=AC-AB=11-6=5$.'], figure=f2)
    M.place_q(g2, LEARN1, after='solve-' + g1)
    _solution(M, g2, LEARN1_SB, LEARN1, 2, ["Segments on a line."], [
        ('Step by step', [
            "Four points on a line, in this order. AC is 11, BD is 14, AD is 20. What is BC?",
            "Method one: find the pieces one by one.",
            D('Mark AD = 20 over the whole line and BD = 14 from B to D'),
            "AD is the whole line. BD is the part from B to the end.",
            A("'AB = 20 − 14 = 6' appears", _bt('$AB=AD-BD=20-14=6$', 250, 34)),
            "So AB is what's left: 20 minus 14. Six.",
            A("'BC = 11 − 6 = 5' appears", _bt('$BC=AC-AB=11-6=5$', 320, 34)),
            "AC is AB plus BC. 11 minus 6: BC is 5.",
            D('Circle choice 3'),
            "Choice three.",
        ], _qpre(g2, f2)),
        ('The overlap rule', [
            "Method two: the overlap rule, in one line.",
            A("'AC + BD = AD + BC' appears", _bt('$AC+BD=AD+BC$', 250, 38)),
            "AC and BD together cover the whole line — and BC twice.",
            A("'11 + 14 = 20 + BC → BC = 5' appears", _bt('$11+14=20+BC$\n$BC=25-20=5$', 330, 34)),
            "11 plus 14 is 25. The whole is 20. The extra 5 is BC.",
            "The traps: 9 is CD, 6 is AB — the wrong piece. 25 is AC plus BD, with BC counted twice.",
            D('Circle choice 3'),
            "Choice three again.",
        ], _qpre(g2, f2)),
    ])
    M.set_sidebar('solve-geo30-g002', LEARN1_SB)

    # =====================================================================================
    # 6. Lesson "Lines and Angles: Advanced" (geo-004) and Q2-Q4 videos
    # =====================================================================================
    _fix_say(M, L2, 1, "we'll practise psychometric", "we'll practice psychometric")
    _fix_say(M, L2, 1, "we'll practise only a few", "we'll practice only a few")
    _fix_say(M, L2, 2, 'We\'ll see each of them in the next three questions.', 'We\'ll see each of them in the next questions.')
    # Q3 (g006): plug-in check + name the insight
    V3 = 'solve-geo30-g006'
    M.edit_lines(V3, 3, lambda ls: ls + [
        {'say': "One warning. The same number for p, q and r is quick — but check that the four answers come out different."},
        {'say': "Here they did: 150, 270, 90 and a negative. If two answers tie, plug in again with other numbers."}])
    _fix_say(M, V3, 3, 'So q is 150 — its neighbour is 30. And r is 150 — its neighbour is 30.',
             'So q is 150 — its neighbor is 30. And r is 150 — its neighbor is 30.')
    M.edit_lines(V3, 4, lambda ls: ls[:5] + [{'say': "Give this idea a name: overlapping angles. Add them, and subtract the full turn."}] + ls[6:])
    # Q4 (g007): the zig-zag rule
    V4 = 'solve-geo30-g007'
    _fix_say(M, V4, 2, "and realising that you need to add one at all.", "and realizing that you need to add one at all.")
    M.edit_lines(V4, 2, lambda ls: [l for l in ls if l.get('say') != "That's it for lines and angles."])
    M.insert_slides(V4, 2, [
        dict(mode='question', active=2, title='The zig-zag rule', pre=_qpre('geo30-g007', M.slide(V4, 2)['items'][0]['fig']['svg']), script=[
            "Now a shortcut for any zig-zag between two parallel lines.",
            A("'Angles pointing left = angles pointing right' appears", _bt('Angles pointing left $=$ angles pointing right', 250, 34)),
            "Look at each marked angle. Where does its tip — the vertex — point?",
            D('Draw a small arrow at each marked angle, in the direction its tip points'),
            "38 points left. 57 points left. x points right.",
            A("'x = 38° + 57° = 95°' appears", _bt('$x=38°+57°=95°$', 340, 36)),
            "So x equals 38 plus 57: 95. One step.",
            "Two bends? Same rule. Add the angles that point left, add the ones that point right — equal.",
            "The rule is for the angles inside the zig-zag, between neighboring pieces. Not sure? Draw a parallel line through each bend. That always works.",
        ]),
    ])

    # =====================================================================================
    # 7. New guided question: two bends (learn section 2, after Q4)
    # =====================================================================================
    g3 = NEW[3]; f3 = fig_g3()
    M.new_q(g3, TOPIC, 'In the accompanying figure, $a\\parallel b$. What is the value of $x$?',
            ['$80°$', '$70°$', '$105°$', '$140°$'], 2,
            ['Zig-zag rule: the angles pointing left $=$ the angles pointing right.',
             'Pointing left: $40°$ and $65°$. Pointing right: $x$ and $35°$.',
             '$40°+65°=x+35°$. Therefore, $105°=x+35°$ and $x=70°$. Choice 2.',
             'Check with parallel lines through both bends: the lower bend splits into $35°$ and $65°-35°=30°$; the upper bend splits into $40°$ and $30°$. Therefore, $x=40°+30°=70°$.'],
            figure=f3)
    M.place_q(g3, LEARN2, after='solve-geo30-g007')
    _solution(M, g3, LEARN2_SB, LEARN2, 4, ["A hard one: two bends."], [
        ('Method 1 · The zig-zag rule', [
            "a is parallel to b. The line between them bends twice. What is x?",
            "Use the zig-zag rule: the angles pointing left equal the angles pointing right.",
            D('At each marked angle, draw a small arrow where its tip points'),
            "40 points left. 65 points left. x points right. 35 points right.",
            A("'40° + 65° = x + 35°' appears", _bt('$40°+65°=x+35°$', 250, 36)),
            A("'x = 105° − 35° = 70°' appears", _bt('$x=105°-35°=70°$', 330, 36)),
            "40 plus 65 is 105. x plus 35 is 105. So x is 70.",
            D('Circle choice 2'),
            "Choice two.",
        ], _qpre(g3, _crop(f3, '95 70 450 240'))),
        ('Method 2 · Parallel lines', [
            "Don't trust a rule you don't remember? Draw a parallel line through each bend.",
            D('Draw a line through each bend, parallel to a and b'),
            "Start at the bottom. The lower bend, 65, splits in two. The lower piece makes a Z with the 35 — so it's 35.",
            A("'65° − 35° = 30°' appears", _bt('$65°-35°=30°$', 250, 36)),
            "The upper piece is 65 minus 35: 30.",
            "That 30 makes a Z with the lower piece of x. So that piece is 30 too.",
            "The upper piece of x makes a Z with the 40 at line a. It's 40.",
            A("'x = 40° + 30° = 70°' appears", _bt('$x=40°+30°=70°$', 330, 36)),
            "x is 40 plus 30: 70. Same answer.",
            "The traps: 105 adds only the left side. 140 adds everything.",
        ], _qpre(g3, _crop(f3, '95 70 450 240'))),
    ])
    for vid in ('solve-geo30-g005', 'solve-geo30-g006', 'solve-geo30-g007'):
        M.set_sidebar(vid, LEARN2_SB)
    M.set_slide(L2, 2, script=[
        "So what makes a line-and-angle question harder? Three things.",
        A("'1 · A crowded figure' appears", T('1 · A crowded figure — several pairs of lines', size=44)),
        A("'2 · Letters instead of numbers' appears", T('2 · Letters instead of numbers', size=44)),
        A("'3 · A missing line — an auxiliary construction' appears", T('3 · A missing line — an auxiliary construction', size=44)),
        "We'll see each of them in the next questions. Let's start with a sample question.",
    ])

    # =====================================================================================
    # 8. Guided Q2-Q4 written solutions
    # =====================================================================================
    S('geo30-g005', expl=['$a\\parallel b$ (line $c$ crosses them): the acute angles are equal. Therefore, the acute angle next to $x$ at the lower left is $83°$.',
                          '$c\\parallel d$ (the diagonal crosses them): the other acute angle next to $x$ is $54°$.',
                          'The three angles make a straight angle: $83°+54°+x=180°$. Therefore, $x=180°-137°=43°$. Choice 2.',
                          'Shortcut: $3+4=7$. Therefore, $x$ must end in $3$. Only $43°$ does.'])
    S('geo30-g006', expl=['The angle next to $p$ is $180°-p$, the angle next to $q$ is $180°-q$, the angle next to $r$ is $180°-r$.',
                          'These three angles and $\\theta$ make a straight angle: $(180°-p)+(180°-q)+(180°-r)+\\theta=180°$.',
                          'Therefore, $540°-(p+q+r)+\\theta=180°$ and $\\theta=p+q+r-360°$. Choice 3.',
                          'Plug in: $p=q=r=150°$ gives $\\theta=3\\cdot30°=90°$. Choices 1, 2 and 4 give $150°$, $270°$ and $-150°$. Only choice 3 gives $90°$.'])
    S('geo30-g007', expl=['Draw a line through the bend, parallel to $a$ and $b$. It splits $x$ into two parts.',
                          'The upper part makes a Z with the $38°$ angle. Therefore, it is $38°$. The lower part makes a Z with the $57°$ angle. Therefore, it is $57°$.',
                          '$x=38°+57°=95°$. Choice 4.',
                          'Zig-zag rule: $x$ points right, $38°$ and $57°$ point left. Therefore, $x=38°+57°$.'])

    # =====================================================================================
    # 9. Foundation practice
    # =====================================================================================
    S('geo30-foundation-p01', expl=['$x$ and $42°$ are adjacent angles on a straight line: $x+42°=180°$.', '$x=180°-42°=138°$.'])
    S('geo30-foundation-p02', expl=['The $138°$ angle is the right angle plus the angle above the horizontal line: $138°-90°=48°$.',
                                    '$x$ and $48°$ are on a straight line: $x=180°-48°=132°$.'])
    S('geo30-foundation-p03', expl=['The angle vertical to the upper $4x$ is also $4x$.',
                                    'On the lower straight line: $x+4x+4x=180°$.', '$9x=180°$. Therefore, $x=20°$.'])
    S('geo30-foundation-p04', expl=['$p$ and $76°$ are on a straight line: $p=180°-76°=104°$.',
                                    '$p=2q$. Therefore, $q=\\frac{104°}{2}=52°$.',
                                    '$q$, $r$, $s$ and $t$ make a full circle. Therefore, $r+s+t=360°-52°=308°$.'])
    S('geo30-foundation-p05', expl=['The small angles are equal. Therefore, the acute angle at line $b$ is $62°$.',
                                    '$x$ is a large angle: $x=180°-62°=118°$.'])
    S('geo30-foundation-p06', expl=['$\\beta$ is a small angle: $\\beta=34°$.',
                                    '$\\alpha$ and $\\gamma$ are large angles: $\\alpha=\\gamma=180°-34°=146°$.',
                                    '$\\alpha+\\beta+\\gamma=146°+34°+146°=326°$.'])
    S('geo30-foundation-p07', expl=['$y$ is vertical to the $64°$ angle: $y=64°$.',
                                    '$x$ is a large angle: $x=180°-64°=116°$.', '$x-y=116°-64°=52°$.'])
    S('geo30-foundation-p08', expl=['$\\alpha$ and $\\gamma$ are both large angles. Therefore, they are equal: $-\\alpha+\\gamma=0$.',
                                    'What is left is $\\beta$, a small angle: $\\beta=180°-124°=56°$.'])
    S('geo30-foundation-p10', expl=['$x$ is a small angle and $8x$ is a large angle: $x+8x=180°$.', '$9x=180°$. Therefore, $x=20°$.'])
    S('geo30-foundation-p11', expl=['The angle next to $124°$ on the straight line is $180°-124°=56°$.',
                                    'The ray cuts it into two equal halves: $x=\\frac{56°}{2}=28°$.'])
    S('geo30-foundation-p12', expl=['The known angles: $85°+75°+110°=270°$.',
                                    'All four angles make a full circle: $x=360°-270°=90°$.'])
    f13 = M.q('geo30-foundation-p13')['questionVisual']['svg']
    f13n = (f13.replace('<text x="406.336" y="100.682" text-anchor="middle"', '<text x="400.000" y="99.000" text-anchor="start"')
               .replace('<text x="233.664" y="259.318" text-anchor="middle"', '<text x="240.000" y="263.000" text-anchor="end"'))
    assert f13n.count('text-anchor="start"') == 1 and f13n.count('text-anchor="end"') == 1
    _set_qfig(M, 'geo30-foundation-p13', f13n)
    S('geo30-foundation-p13', expl=['Both marked angles are small angles (acute). Therefore, they are equal: $3x+7=5x-23$.',
                                    '$30=2x$. Therefore, $x=15$.', 'Check: $3\\cdot15+7=52$ and $5\\cdot15-23=52$.'])
    S('geo30-foundation-p16', expl=['The distance between parallel lines is measured along a line perpendicular to both.',
                                    'This segment is exactly that distance: $7$ cm.'])
    S('geo30-foundation-p17', expl=['$2+3+4=9$ units make $180°$. Therefore, one unit is $\\frac{180°}{9}=20°$.',
                                    'The largest angle is $4$ units: $4\\cdot20°=80°$.'])
    # Pass 2 (plan): the original p09, p14 and p15 stay in the foundation practice (text clean-up only)
    S('geo30-foundation-p09', expl=['$\\alpha$ and the $122°$ angle are adjacent on line $a$: $\\alpha=180°-122°=58°$.',
                                    '$\\beta$ is a small angle, like $\\alpha$. Small angles are equal: $\\beta=58°$.',
                                    '$\\alpha+\\beta=58°+58°=116°$.'])
    S('geo30-foundation-p14', stem='In the accompanying figure, lines $a$ and $b$ are parallel. What is the value of $x$?',
      expl=['Draw a line through the bend, parallel to $a$ and $b$. It splits $x$ into two parts.',
            'The upper part makes a Z with the $39°$ angle, and the lower part makes a Z with the $63°$ angle.',
            '$x=39°+63°=102°$.'])
    S('geo30-foundation-p15', expl=['The fourth line crosses each of the three parallel lines exactly once.',
                                    'The parallel lines never meet, so the three crossing points are different: $3$ points.'])

    n4 = NEW[4]
    # 2026-10-01 elite comparison: "cannot be determined" is now the trap, not the answer
    M.new_q(n4, TOPIC, 'In the accompanying figure, lines $t$ and $s$ cross lines $a$ and $b$. What is the value of $x$?',
            ['$55°$', '$72°$', '$125°$', CBD], 3,
            ['Nothing says $a\\parallel b$ — but the angles on line $t$ prove it. $108°$ and $72°$ sit inside a U, and $108°+72°=180°$. Therefore, $a\\parallel b$.',
             'Now line $s$. The $55°$ angle and $x$ also sit inside a U between the parallel lines: $x=180°-55°=125°$. Choice 3.',
             'Trap: "It cannot be determined". Before you choose it, check whether the figure proves the lines parallel.'], figure=fig_p04())
    M.place_q(n4, FOUND)
    n5 = NEW[5]
    M.new_q(n5, TOPIC, 'In the accompanying figure, $a\\parallel b$. What is the value of $x$?',
            ['$5$', '$25$', '$30$', '$35$'], 2,
            ['The two marked angles sit inside a U: they add up to $180°$.',
             '$(4x+10)+(2x+20)=180$. Therefore, $6x+30=180$ and $6x=150$.', '$x=25$. Check: $110°+70°=180°$.'], figure=fig_p05())
    M.place_q(n5, FOUND)

    # =====================================================================================
    # 10. Advanced practice
    # =====================================================================================
    S('geo30-advanced-p01', expl=['$\\alpha$ and $\\beta$ are vertical angles, and $\\beta$ and $\\gamma$ are both small angles: $\\alpha=\\beta=\\gamma$.',
                                  '$\\frac{4\\alpha+\\gamma}{\\beta}=\\frac{4\\beta+\\beta}{\\beta}=\\frac{5\\beta}{\\beta}=5$.'])
    S('geo30-advanced-p02', stem='Five different lines are given:\n$\\begin{cases} p\\parallel q \\\\ q\\perp r \\\\ r\\parallel s \\\\ s\\perp t \\end{cases}$\nWhich of the following is necessarily true?',
      expl=['$p\\parallel q$ and $q\\perp r$. Therefore, $p\\perp r$. $r\\parallel s$. Therefore, $p\\perp s$ too.',
            '$p\\perp s$ and $t\\perp s$: two lines perpendicular to the same line are parallel. Therefore, $p\\parallel t$.'])
    S('geo30-advanced-p03', expl=['$x$ covers $8$ equal gaps and $y$ covers $4$. Count the gaps, not the tick marks.',
                                  '$\\frac{x}{y}=\\frac{8}{4}=2$.'])
    S('geo30-advanced-p04', expl=['The four angles make a full circle: $x+2x+3x+168°=360°$.', '$6x=192°$. Therefore, $x=32°$.'])
    S('geo30-advanced-p05', stem='In the accompanying figure, three lines meet at point $O$. What is the value of $x$?',
      expl=['The $116°$ angle and the angle next to it are on a straight line: that angle is $180°-116°=64°$.',
            'The $136°$ angle is made of this $64°$ angle and $x$: $64°+x=136°$.', '$x=136°-64°=72°$.'],
      figure=fig_adv05())
    S('geo30-advanced-p06', stem=GIVEN('\\alpha+u=180°', '\\beta+3u=180°', '0°<u<60°') + 'Which of the following is necessarily true?',
      expl=['$\\alpha=180°-u$ and $\\beta=180°-3u$.',
            'Since $u>0$, $3u>u$: $\\beta$ subtracts more from the same $180°$. Therefore, $\\beta<\\alpha$.',
            'Plug in to check: $u=10°$ gives $\\alpha=170°$ and $\\beta=150°$.'])
    S('geo30-advanced-p07', stem='Four different lines are given:\n$\\begin{cases} k\\perp l \\\\ l\\perp m \\\\ m\\perp n \\end{cases}$\nWhich of the following is necessarily true?',
      expl=['$k$ and $m$ are both perpendicular to $l$. Two lines perpendicular to the same line are parallel: $k\\parallel m$.',
            '(Also $l\\parallel n$, since both are perpendicular to $m$. Therefore, choice 3, $l\\perp n$, is false.)'])
    S('geo30-advanced-p08', expl=['$\\alpha$, $48°$ and $103°$ make a straight angle: $\\alpha=180°-103°-48°=29°$.',
                                  '$\\beta$ is made of $48°$ and $\\alpha$: $\\beta=48°+29°=77°$.', '$\\alpha+\\beta=29°+77°=106°$.'])
    S('geo30-advanced-p09', stem='Points $P$, $Q$, $R$ and $S$ lie on a line in this order.\n' + GIVEN('a=PR', 'b=QS') + 'Which of the following is necessarily true?', expl=['$a+b=PR+QS=(PQ+QR)+(QR+RS)$.', '$PS+QR=(PQ+QR+RS)+QR$.',
                                  'Both sums have $PQ$ once, $RS$ once and $QR$ twice. They are equal: $a+b=PS+QR$.'])
    S('geo30-advanced-p10', stem='In the accompanying figure, three lines meet at one point. The angles $p$ and $q$ overlap on the angle $x$. Which expression equals $x$?',
      expl=['$p$ and $q$ together cover the straight angle once, and $x$ twice: $p+q=180°+x$.',
            'Therefore, $x=p+q-180°$. Choice 2.',
            'Plug in to check: $p=120°$, $q=110°$ gives $x=50°$. Choice 1 gives $130°$, choice 3 about $77°$, choice 4 $-10°$.'],
      figure=fig_adv10())
    S('geo30-advanced-p11', expl=['Call the two angles $2a$ and $2b$: $2a+2b=180°$.',
                                  'The angle between the bisectors is $a+b=\\frac{180°}{2}=90°$.'])
    S('geo30-advanced-p12', expl=['The obtuse and the acute angle are adjacent on a straight line:\n$\\begin{cases} \\text{obtuse}+\\text{acute}=180° \\\\ \\text{obtuse}-\\text{acute}=46° \\end{cases}$',
                                  'Add the two equations: $2\\cdot\\text{obtuse}=226°$. Therefore, the obtuse angle is $113°$.'])
    S('geo30-advanced-p13', expl=['Lines in the same family are parallel and never meet.',
                                  'Each of the $2$ lines meets each of the $3$ lines once: $2\\cdot3=6$ points.'])
    S('geo30-advanced-p14', expl=['Let the first angle be $t$. The parts are $t$, $t+18°$ and $2t$.',
                                  '$t+(t+18°)+2t=180°$. Therefore, $4t=162°$ and $t=40.5°$.', 'The third angle is $2t=81°$.'])
    S('geo30-advanced-p15', expl=['An acute angle and an obtuse angle here are small $+$ large: $(2x+11)+(5x+1)=180$.',
                                  '$7x+12=180$. Therefore, $7x=168$ and $x=24$.'])
    S('geo30-advanced-p16', stem='Points $A$, $B$, $C$ and $D$ lie on a line in this order.\n' + GIVEN('AC=17\\text{ cm}', 'BD=19\\text{ cm}', 'BC=6\\text{ cm}') + 'What is the length of $AD$ (in cm)?', expl=['$AC+BD=AD+BC$ (the overlap $BC$ is counted twice).',
                                  '$17+19=AD+6$. Therefore, $AD=36-6=30$ cm.'])
    S('geo30-advanced-p17', expl=['Let each of the three equal angles be $t$. Then $3t+(t+24°)=360°$.',
                                  '$4t=336°$. Therefore, $t=84°$. The largest angle is $84°+24°=108°$.'])

    n6 = NEW[6]
    M.new_q(n6, TOPIC, 'Ten points are marked on a line, in order, at equal distances. The distance between the first point and the last point is $45$ cm. What is the distance between the third point and the seventh point (in cm)?',
            ['$18$', '$25$', '$20$', '$22.5$'], 3,
            ['Ten points make $9$ gaps (count the gaps, not the points): each gap is $\\frac{45}{9}=5$ cm.',
             'From the 3rd point to the 7th point there are $7-3=4$ gaps: $4\\cdot5=20$ cm.'])
    M.place_q(n6, ADV)
    n7 = NEW[7]
    M.new_q(n7, TOPIC, 'In the accompanying figure, $a\\parallel b$. What is the value of $x$?',
            ['$30°$', '$50°$', '$110°$', '$150°$'], 2,
            ['Zig-zag rule: the angles pointing left $=$ the angles pointing right.',
             'Pointing left: $50°$ and $x$. Pointing right: $80°$ and $20°$.',
             '$50°+x=80°+20°$. Therefore, $x=100°-50°=50°$.'], figure=fig_p07())
    M.place_q(n7, ADV)
    n9 = NEW[9]
    M.new_q(n9, TOPIC, 'In the accompanying figure, line $t$ crosses lines $a$ and $b$. Which of the following is necessarily true?',
            ['Lines $a$ and $b$ are parallel.', 'Lines $a$ and $b$ meet to the right of line $t$.',
             'Lines $a$ and $b$ meet to the left of line $t$.', CBD], 1,
            ['The two marked angles are on the same side of $t$, between the lines (a U): $107°+73°=180°$.',
             'A small angle and a large angle that add up to $180°$ inside the U: the lines are parallel.',
             'Therefore, $a\\parallel b$. Choice 1.'], figure=fig_p10())
    M.place_q(n9, ADV)

    # =====================================================================================
    # 11. Practice order: easy -> hard
    # =====================================================================================
    M.practice_order(FOUND, [
        'geo30-foundation-p16', 'geo30-foundation-p01', 'geo30-foundation-p02', 'geo30-foundation-p12',
        'geo30-foundation-p17', 'geo30-foundation-p11', 'geo30-foundation-p03', 'geo30-foundation-p04',
        'geo30-foundation-p15', 'geo30-foundation-p05', 'geo30-foundation-p09', 'geo30-foundation-p10',
        'geo30-foundation-p13', n5, 'geo30-foundation-p06', 'geo30-foundation-p07', 'geo30-foundation-p08',
        'geo30-foundation-p14', n4])
    M.practice_order(ADV, [
        'geo30-advanced-p12', 'geo30-advanced-p11', 'geo30-advanced-p14', 'geo30-advanced-p17', 'geo30-advanced-p04',
        'geo30-advanced-p15', 'geo30-advanced-p01', 'geo30-advanced-p05', 'geo30-advanced-p08', 'geo30-advanced-p13',
        'geo30-advanced-p07', 'geo30-advanced-p02', n6, 'geo30-advanced-p03', 'geo30-advanced-p16', 'geo30-advanced-p09',
        'geo30-advanced-p06', 'geo30-advanced-p10', n9, n7])

    S('geo30-foundation-p11', stem='A ray bisects the angle adjacent to the marked $124°$ angle. Based on this information and the information in the accompanying figure, what is the value of $x$?')
    S('geo30-foundation-p16', stem='Two parallel lines are $7$ cm apart. A line segment joining them is perpendicular to both. What is the length of the segment (in cm)?')
    S('geo30-advanced-p12', stem='Two lines intersect. The difference between an obtuse angle and an acute angle at the intersection is $46°$. What is the obtuse angle?')
    S('geo30-advanced-p14', stem='A straight angle is divided into three parts. The second part is $18°$ larger than the first, and the third is twice the first. What is the third angle?')
    S('geo30-advanced-p17', stem='Four rays divide a full turn into four angles. Three angles are equal, and the fourth is $24°$ larger than each of them. What is the largest angle?')
    for f in list(M.D['flow']):
        if f['topic'] == TOPIC and f['type'] == 'question':
            q = M.q(f['ref'])
            if q['stemRich'] != q['stemRich'].strip(): S(f['ref'], stem=q['stemRich'].strip())

    summaries(M)

    # =====================================================================================
    # 12. Cleanup: spelling, solution-video titles and "on screen" notes in sync
    # =====================================================================================
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k in l:
                        s0 = l[k]
                        s1 = (s0.replace('neighbouring', 'neighboring').replace('neighbour', 'neighbor')
                                .replace('practise', 'practice').replace('realising', 'realizing'))
                        if s1 != s0: l[k] = s1; M.touched_videos.add(v['id'])
        if v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']
            for b in v['beats']:
                pre = b['items'][:b['pre']]
                if len(pre) == 1 and pre[0].get('k') == 'q' and b.get('canvas', '').startswith('Pre-loaded — question'):
                    qid = pre[0]['qid']
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, M.q(qid)['stem'])

    cut_repeats(M)   # 2026-10-05: runs last


# =====================================================================================
# Pass 2: summary lessons right before each practice section
# =====================================================================================
def summaries(M):
    # --- 1. end of "Learn and try", before the foundation practice ---
    sb = ['Angles at a point', 'Right angle', 'Adjacent and vertical', 'Parallel lines', 'Z and U', 'Parallel or not?',
          'Segments on a line', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of lines and angles.",
            "All the rules, one at a time."]),
        S(0, [
            A("'Full circle = 360°' appears", T('Full circle (angles around a point) $=360°$', size=44, gap=40)),
            "All the angles around one point add up to 360.",
            A("'Straight angle = 180°' appears", T('Straight angle $=180°$ — half of the circle', size=44, gap=40)),
            "A straight line is half of that: 180.",
            A("'Acute < 90° < obtuse' appears", T('Acute $<90°<$ obtuse', size=44)),
            "Smaller than 90: acute. Bigger than 90: obtuse."]),
        S(1, [
            A("'Right angle = 90° — a small square' appears", T('Right angle $=90°$ — marked with a small square', size=44, gap=40)),
            "A right angle is 90 degrees. Two perpendicular lines make it.",
            "On the exam, there is almost always a dot in the middle of the square.",
            A("'90° only if marked or given' appears", T('$90°$ only if it is marked or given', size=44)),
            "Looks like 90? That's not enough. It must be marked, or given."]),
        S(2, [
            A("'Adjacent on a straight line: sum 180°' appears", T('Adjacent on a straight line: sum $180°$', size=44, gap=40)),
            "Two angles side by side on one straight line add up to 180. Forty-seven next to x? x is 133.",
            A("'Vertical angles: equal' appears", T('Vertical angles: equal', size=44, gap=40)),
            "Two lines cross: the angles facing each other are equal.",
            A("'Bisector: two equal halves' appears", T('Bisector: $64°\\div2=32°$', size=44)),
            "A bisector splits an angle into two equal halves."]),
        S(3, [
            A("'small = small · large = large' appears", T('small $=$ small $\\cdot$ large $=$ large', size=46, gap=40)),
            "Parallel lines and a transversal give eight angles: four small and four large.",
            "All the small ones are equal. All the large ones are equal.",
            A("'small + large = 180°' appears", T('small $+$ large $=180°$', size=46)),
            "And a small one plus a large one is always 180."]),
        S(4, [
            A("'Z → equal' appears", T('Z $\\to$ the two angles are equal', size=46, gap=40)),
            "See parallel lines? Look for the Z. The two angles in its corners are equal.",
            A("'U → sum 180°' appears", T('U $\\to$ the two angles add up to $180°$', size=46)),
            "Two angles inside a U — same side, between the lines — add up to 180. Fifty-three and 127."]),
        S(5, [
            A("'⊥ or ∥ to the same line → parallel' appears",
              T('Two lines $\\perp$ or $\\parallel$ to the same line $\\to$ parallel', size=42, gap=40)),
            "Two lines perpendicular to the same line are parallel. So are two lines parallel to the same line.",
            A("'Not to scale: parallel only if given or proved' appears",
              T('Not to scale: parallel only if given or proved', size=42)),
            "Lines can LOOK parallel. Don't trust your eyes.",
            "Nothing given? Look for a rule in the figure that proves it — a U that adds up to 180, for example."]),
        S(6, [
            A("'AC + BD = AD + BC' appears", T('$AC+BD=AD+BC$', size=50, gap=40)),
            "Four points on a line: AC and BD overlap on BC. Twelve plus nine, minus the whole sixteen: BC is five.",
            A("'Count the gaps, not the points' appears", T('Equal parts: count the gaps, not the points', size=44)),
            "Seven equally spaced points make six gaps, not seven."]),
        S(7, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('Is it really $90°$? Is it marked or given?', size=40, gap=30)),
            A('Check 2 appears', T('Are the lines really parallel? Given, or proved?', size=40, gap=30)),
            A('Check 3 appears', T('Small or large? Equal, or a sum of $180°$?', size=40, gap=30)),
            A('Check 4 appears', T('Segments: did I count the gaps?', size=40)),
            "And the traps: trusting the picture, and counting points instead of gaps.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN1][-1]
    M.new_video('r26-t30-summary', TOPIC, 'Summary: Lines and Angles', sb, slides, LEARN1, after=last)

    # --- 2. end of "Further guided examples", before the advanced practice ---
    sb = ['Crowded figures', 'Anchor: 180° or 360°', 'Letters: plug in', 'Overlapping angles', 'A missing line',
          'The zig-zag rule', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before the advanced practice — a quick summary of the harder questions.",
            "Three things make them harder: a crowded figure, letters, and a missing line."]),
        S(0, [
            A("'One pair of parallel lines at a time' appears", T('Crowded figure: one pair of parallel lines at a time', size=42, gap=40)),
            "Several pairs of lines? Take one pair and its transversal. Ignore the rest.",
            "Move the angle you know to the place you need. Then the next pair.",
            A("'76° + 58° + x = 180° → x = 46°' appears", T('$76°+58°+x=180°\\ \\to\\ x=46°$', size=46)),
            "Then build the equation.",
            "Shortcut: six plus eight is fourteen, so x must end in six. Only forty-six does."]),
        S(1, [
            A("'Anchor: a straight angle 180° or a full turn 360°' appears",
              T('Anchor: a straight angle $180°$ or a full turn $360°$', size=42, gap=40)),
            "Lost? Look for an anchor: angles that make a straight line, or a full circle.",
            A("'The angle next to p: 180° − p' appears", T('The angle next to $p$: $\\ 180°-p$', size=44)),
            "Every angle gives you its neighbor: 180 minus it."]),
        S(2, [
            A("'Letters? Plug in round numbers' appears", T('Letters? Plug in round numbers that look like the figure', size=40, gap=40)),
            "Letters instead of numbers? Put numbers back. Looks obtuse? Plug in 130.",
            A("'p = q = r = 130° → θ = 30°' appears", T('$p=q=r=130°\\ \\to\\ \\theta=30°$', size=46, gap=40)),
            "Then plug the same numbers into the choices. Cross out every choice that doesn't give thirty.",
            "Check that the four choices come out different. If two tie, plug in again."]),
        S(3, [
            A("'Overlapping angles: add, subtract the full turn' appears",
              T('Overlapping angles: add them, subtract $360°$ or $180°$', size=40, gap=40)),
            "Angles that overlap count a piece twice.",
            A("'θ = p + q + r − 360°' appears", T('$\\theta=p+q+r-360°$', size=48)),
            "p, q and r cover the full turn, and theta one more time. So theta is their sum minus 360."]),
        S(4, [
            A("'A bent line? Draw a parallel line through the bend' appears",
              T('A bent line? Draw a parallel line through the bend', size=42, gap=40)),
            "No straight transversal? Add an auxiliary line: through the bend, parallel to both lines.",
            A("'x = 41° + 69° = 110°' appears", T('$x=41°+69°=110°$', size=46)),
            "It splits x into two pieces. Each piece makes a Z with a given angle.",
            "The hard part is seeing that you need a line at all."]),
        S(5, [
            A("'Angles pointing left = angles pointing right' appears",
              T('Zig-zag: angles pointing left $=$ angles pointing right', size=42, gap=40)),
            "The shortcut. Look where each angle's tip points.",
            A("'50° + 70° = x + 45° → x = 75°' appears", T('$50°+70°=x+45°\\ \\to\\ x=75°$', size=46)),
            "Two bends? Same rule. Left side equals right side.",
            "Not sure? A parallel line through each bend always works."]),
        S(6, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('Which pair of lines is parallel — and which line cuts them?', size=38, gap=30)),
            A('Check 2 appears', T('Where is my anchor: $180°$ or $360°$?', size=40, gap=30)),
            A('Check 3 appears', T('Letters? Plug in — and check the choices come out different.', size=38, gap=30)),
            A('Check 4 appears', T('A bent line? Draw a parallel line through the bend.', size=38)),
            "And the traps: adding only one side of the zig-zag, and forgetting that overlapping angles count a piece twice.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN2][-1]
    M.new_video('r26-t30-summary-2', TOPIC, 'Summary: Harder Line and Angle Questions', sb, slides, LEARN2, after=last)


# =====================================================================================
# 2026-10-05 cut repeats: a lesson slide that the next question video teaches again is cut
# =====================================================================================
def _slide_no(M, vid, title):
    for n, b in enumerate(M.video(vid)['beats'], 1):
        if b.get('title') == title: return n
    raise KeyError('%s: no slide %r' % (vid, title))


def cut_repeats(M):
    # geo-001 "Segments on a line": the overlap rule (AC + BD = AD + BC) is taught again, with its own
    # numbers and board, in solve-q-r26-t30-02 slide 3 ("The overlap rule"). Keep only the gaps trap,
    # which no question video teaches.
    n = _slide_no(M, L1, 'Segments on a line')
    M.set_slide(L1, n, pre=[], script=[
        "Points on one line make segments. One trap for the exam.",
        A("'Equal parts: count the gaps, not the points' appears", T('Equal parts: count the gaps, not the points', size=44)),
        D('Draw 5 equally spaced dots on a line and number the 4 gaps between them'),
        "Five points, equally spaced. How many gaps? Four, not five.",
        "Lengths live in the gaps. Count the spaces between the points.",
    ])
    r = M.slide(L1, _slide_no(M, L1, 'Recap'))
    for it in r['items']:
        if it.get('t', '').startswith('Segments: count the gaps'): it['t'] = 'Segments: count the gaps, not the points'


# ======================================================================================================
# 2026-10-06 renumber pass (runs LAST). The English course must not look like the Hebrew one: every Hebrew-derived
# question (guided geo30-g002, g005, g006, g007; practice foundation p01-p10 and advanced p01-p10) gets new numbers
# (letter-only questions: new letters and choice order). Idea, trap, level and methods stay. Every figure of a changed
# question is redrawn to its new angles, and every guided solution video is rewritten to match. Practice clean-up 39 -> 26.
# Nothing in topic 30 is recorded (checked ~/Documents/Course.recordings 2026-10-06).
# ======================================================================================================
RN_RECORDED = set()


def _rn_q(M, qid, stem=None, choices=None, correct=None, expl=None, figure=None):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)
    if figure is not None: _set_qfig(M, qid, figure)


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


def _rn_lines(M, vid, n, lines):
    """Replace all lines of a slide (items stay; 'appear' lines must point at the same items)."""
    if vid in RN_RECORDED: return
    old = [l['appear'] for l in M.slide(vid, n)['lines'] if 'appear' in l]
    assert old == [l['appear'] for l in lines if 'appear' in l], (vid, n)
    M.edit_lines(vid, n, lambda ls: lines)


def _rn_slide_no(M, vid, title):
    return next(i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title)


def _relabel(svg, mp):
    """Change the text of figure labels (exact <text> contents)."""
    for old, new in mp.items():
        n = len(re.findall('>%s</text>' % re.escape(old), svg))
        assert n == 1, (old, n)
    return re.sub(r'>([^<]+)</text>', lambda mo: '>%s</text>' % mp.get(mo.group(1), mo.group(1)), svg)


# --- redrawn figures (same frame as the old ones, so the solution-slide crops still fit) ---------------
def _rn_rays(title, rays, arcs, lines=(), extra=()):
    """Rays from (320, 180): rays = directions (deg); lines = full lines through the point; arcs = (a1, a2, label, r, rl)."""
    O = (320.0, 180.0); R = 156.429
    b = []
    for d in lines:
        p, q = _pt(R, d, *O), _pt(R, d + 180, *O); b.append(_ln(p[0], p[1], q[0], q[1]))
    for d in rays:
        p = _pt(R, d, *O); b.append(_ln(O[0], O[1], p[0], p[1]))
    for a1, a2, t, r, rl in arcs: b += [_arc(O[0], O[1], r, a1, a2), _alab(O[0], O[1], rl, a1, a2, t)]
    return _svg(title, b + list(extra))


def _rn_par(title, rows, deg, arcs, ext=107.353):
    """Horizontal lines rows = [(y, name)], a transversal through (320, 180) at deg; arcs = (y, a1, a2, label)."""
    b = []
    for y, nm in rows: b += [_ln(131.059, y, 508.941, y), _tx(120.324, y, nm)]
    dx = ext / math.tan(math.radians(deg))
    b.append(_ln(320 - dx, 180 + ext, 320 + dx, 180 - ext))
    for y, a1, a2, t in arcs:
        cx = 320 + (180 - y) / math.tan(math.radians(deg))
        b += [_arc(cx, y, 25.765, a1, a2), _alab(cx, y, 44, a1, a2, t)]
    return _svg(title, b)


AB = [(119.882, 'a'), (240.118, 'b')]
ABC = [(119.882, 'a'), (180.0, 'b'), (240.118, 'c')]


def rn_fig_g002():
    t = 64; ay, by_ = 121.6, 238.4; xb = 293.0; xa = xb + (by_ - ay) / math.tan(math.radians(t))
    lo, hi = (xb - (301.667 - by_) / math.tan(math.radians(t)), 301.667), (xb + (by_ - 58.333) / math.tan(math.radians(t)), 58.333)
    pl, pr = _pt(52.5, t + 90, xb, by_), _pt(126.5, t - 90, xb, by_)
    b = [_ln(105.867, ay, 534.133, ay), _ln(105.867, by_, 534.133, by_), _ln(lo[0], lo[1], hi[0], hi[1]),
         _tx(93.7, ay, 'a'), _tx(93.7, by_, 'b'),
         _arc(xa, ay, 31.633, 0, t), _alab(xa, ay, 52, 0, t, '64°'),
         _ln(pl[0], pl[1], pr[0], pr[1]), _right(xb, by_, t, t - 90, 13.63),
         _arc(xb, by_, 46.233, t - 90, 0), _alab(xb, by_, 66, t - 90, 0, 'x')]
    return _svg('Two parallel lines cut by a transversal', b)


def rn_fig_g005():
    ay, by_ = 137.059, 222.941; c_dir, d_deg = 103, 47
    X0 = 277.0; Xd = X0 + (by_ - ay) / math.tan(math.radians(d_deg))
    def steep(x_at, y_at):   # line in direction c_dir through (x_at, y_at), from y=64.059 to y=295.941
        k = 1 / math.tan(math.radians(c_dir))
        return _ln(x_at + (y_at - 64.059) * k, 64.059, x_at + (y_at - 295.941) * k, 295.941)
    k = 1 / math.tan(math.radians(c_dir)); ca = X0 + (by_ - ay) * k
    lo, hi = _pt(122.0, 180 + d_deg, X0, by_), _pt(115.0, d_deg, Xd, ay)
    b = [_ln(148.235, ay, 491.765, ay), _ln(148.235, by_, 491.765, by_), steep(X0, by_), steep(Xd, ay),
         _ln(lo[0], lo[1], hi[0], hi[1]),
         _tx(135.353, ay, 'a'), _tx(135.353, by_, 'b'),
         _tx(X0 + (by_ - 64.059) * k - 14, 66.0, 'c'), _tx(Xd + (ay - 64.059) * k + 13, 64.059, 'd'),
         _arc(ca, ay, 24.906, c_dir, 180), _alab(ca, ay, 43, c_dir, 180, '77°'),
         _arc(Xd, ay, 24.906, d_deg, c_dir), _alab(Xd, ay, 42, d_deg, c_dir, '56°'),
         _arc(X0, by_, 30.918, 180, 180 + d_deg), _alab(X0, by_, 47, 180, 180 + d_deg, 'x')]
    return _svg('Two pairs of parallel lines and a diagonal', b)


def rn_fig_g007():
    ay, by_ = 134.912, 225.088; t1, t2 = 36, 62; h = by_ - ay
    drop = (h / math.tan(math.radians(t2))) / (1 / math.tan(math.radians(t1)) + 1 / math.tan(math.radians(t2)))
    X = 320.0; bx, byy = X + drop / math.tan(math.radians(t1)), ay + drop
    b = [_ln(148.235, ay, 491.765, ay), _ln(148.235, by_, 491.765, by_), _ln(X, ay, bx, byy), _ln(X, by_, bx, byy),
         _tx(137.5, ay, 'a'), _tx(137.5, by_, 'b'),
         _arc(X, ay, 30.059, -t1, 0), _alab(X, ay, 49, -t1, 0, '36°'),
         _arc(X, by_, 30.059, 0, t2), _alab(X, by_, 47, 0, t2, '62°'),
         _arc(bx, byy, 21.471, 180 - t1, 180 + t2), _alab(bx, byy, 37, 180 - t1, 180 + t2, 'x')]
    return _svg('Parallel lines and a bent transversal', b)


def rn_fig_p01():
    return _rn_rays('Angles at a point', [0, 37, 180], [(0, 37, '37°', 31.286, 53), (37, 180, 'x', 31.286, 53)])


def rn_fig_p02():
    return _rn_rays('Angles at a point', [0, 56, 180, 270], [(-90, 56, '146°', 31.286, 53), (56, 180, 'x', 31.286, 53)],
                    extra=[_right(320.0, 180.0, 0, -90, 14.6)])


def rn_fig_p03():
    return _rn_rays('Angles at a point', [], [(180, 216, 'x', 31.286, 53), (36, 108, '2x', 31.286, 53),
                                              (288, 360, '2x', 31.286, 53)], lines=[0, 36, 108])


def rn_fig_p04():
    y = 180.0; b = [_ln(105.294, y, 534.706, y)]
    for cx, d in ((221.235, 70), (414.47, 125)):
        p, q = _pt(85.882 / math.sin(math.radians(d)), d, cx, y), _pt(85.882 / math.sin(math.radians(d)), d + 180, cx, y)
        b.append(_ln(p[0], p[1], q[0], q[1]))
    for cx, a1, a2, t in ((221.235, 0, 70, '70°'), (221.235, 70, 180, 'p'), (414.47, 125, 180, 'q'),
                          (414.47, 0, 125, 'r'), (414.47, 180, 305, 's'), (414.47, 305, 360, 't')):
        b += [_arc(cx, y, 25.765, a1, a2), _alab(cx, y, 44, a1, a2, t)]
    return _svg('Two intersections with a given angle ratio', b)


def rn_fig_p05():
    return _rn_par('Parallel lines and a transversal', AB, 57, [(119.882, 0, 57, '57°'), (240.118, 57, 180, 'x')])


def rn_fig_p06():
    return _rn_par('Parallel lines and a transversal', AB, 38, [(119.882, 38, 180, 'α'), (119.882, 218, 360, 'γ'),
                                                                (240.118, 0, 38, '38°'), (240.118, 180, 218, 'β')])


def rn_fig_p07():
    return _rn_par('Parallel lines and a transversal', ABC, 71, [(119.882, 0, 71, '71°'), (119.882, 180, 251, 'y'),
                                                                 (240.118, 251, 360, 'x')])


def rn_fig_p08():
    return _rn_par('Parallel lines and a transversal', ABC, 63, [(119.882, 63, 180, '117°'), (119.882, 243, 360, 'γ'),
                                                                 (180.0, 63, 180, 'α'), (240.118, 180, 243, 'β')])


def rn_fig_p09():
    return _rn_par('Parallel lines and a transversal', AB, 52, [(119.882, 52, 180, '128°'), (119.882, 180, 232, 'α'),
                                                                (240.118, 0, 52, 'β')])


def rn_fig_p10():
    return _rn_par('Parallel lines and a transversal', AB, 30, [(119.882, 180, 210, 'x'), (240.118, 30, 180, '5x')])


def rn_fig_adv03():
    y = 180.0; x0, u = 126.765, 32.206
    b = [_ln(113.882, y, 526.118, y)] + [_ln(x0 + u * k, 185.582, x0 + u * k, 174.418) for k in range(13)]
    b += [_ln(x0 + u * 1, 154.235, x0 + u * 11, 154.235, MARK), _tx(x0 + u * 6, 139.206, 'x'),
          _ln(x0 + u * 4, 205.765, x0 + u * 8, 205.765, MARK), _tx(x0 + u * 6, 220.794, 'y')]
    return _svg('Equal segments on a line', b)


def rn_fig_adv04():
    return _rn_rays('Angles at a point', [0, 35, 105, 210], [(0, 35, 'x', 31.286, 53), (35, 105, '2x', 31.286, 53),
                                                            (105, 210, '3x', 31.286, 53), (210, 360, '150°', 31.286, 53)])


def rn_fig_adv05():
    """Three lines through O: horizontal, 78 and 114 degrees. 114 = 0..114; 144 = 114..258; x = 180..258."""
    O = (320.0, 180.0); R = 150
    bd = []
    for d in (0, 78, 114):
        p, q = _pt(R, d, *O), _pt(R, d + 180, *O); bd.append(_ln(p[0], p[1], q[0], q[1]))
    bd += [_arc(O[0], O[1], 58, 0, 114), _alab(O[0], O[1], 78, 0, 114 - 30, '114°'),
           _arc(O[0], O[1], 40, 114, 258), _alab(O[0], O[1], 58, 125, 165, '144°'),
           _arc(O[0], O[1], 22, 180, 258), _alab(O[0], O[1], 36, 180, 258, 'x'),
           _tx(O[0] + 20, O[1] + 12, 'O', INK, 18)]
    return _svg('Three lines meet at O; angles of 114 and 144 degrees overlap', bd)


def rn_fig_adv08():
    return _rn_rays('Angles at a point', [0, 28, 71, 180], [(0, 28, 'α', 31.286, 53), (28, 71, '43°', 31.286, 55),
                                                           (71, 180, '109°', 31.286, 55), (0, 71, 'β', 78.214, 96)])


def rn_fig_adv10():
    """Three lines through one point: horizontal, 60 and 130 degrees. u = 0..130, v = 60..180, y = 60..130."""
    O = (320.0, 190.0); R = 150
    bd = []
    for d in (0, 60, 130):
        p, q = _pt(R, d, *O), _pt(R, d + 180, *O); bd.append(_ln(p[0], p[1], q[0], q[1]))
    bd += [_arc(O[0], O[1], 36, 0, 130), _alab(O[0], O[1], 52, 0, 40, 'u'),
           _arc(O[0], O[1], 62, 60, 180), _alab(O[0], O[1], 78, 150, 170, 'v'),
           _arc(O[0], O[1], 88, 60, 130), _alab(O[0], O[1], 104, 90, 100, 'y')]
    return _svg('Three lines meet at one point; angles u and v overlap on the angle y', bd)


# --- guided questions and their videos ----------------------------------------------------------------
def rn_guided(M):
    # ---------- g002: 68 -> x = 22 (Hebrew 75 -> 15)  ==>  64 -> x = 26
    g = 'geo30-g002'
    _rn_q(M, g, choices=['$64°$', '$26°$', '$116°$', '$36°$'], correct=2, expl=[
        '$a\\parallel b$, and small angles are equal. At line $b$, the angle between the transversal and line $b$ (above $b$) is also $64°$.',
        'The marked right angle is made of this $64°$ angle and $x$: $64°+x=90°$.',
        'Therefore, $x=90°-64°=26°$. Choice 2.'], figure=rn_fig_g002())
    _rn_sub(M, 'solve-' + g, 2, [
        ('write 68° in the small angle', 'write 64° in the small angle'),
        ('So this angle down here is also 68.', 'So this angle down here is also 64.'),
        ('And 68 plus x together', 'And 64 plus x together'),
        ('Write x = 90° − 68° = 22°', 'Write x = 90° − 64° = 26°'),
        ('So x is 90 minus 68: 22.', 'So x is 90 minus 64: 26.'),
        ('Circle choice 3', 'Circle choice 2'), ('Choice three.', 'Choice two.')])

    # ---------- g005: 83 + 54 -> x = 43 (Hebrew 86 + 53 -> 41)  ==>  77 + 56 -> x = 47 (units digit 7 + 6 = 13 -> x ends in 7)
    g = 'geo30-g005'
    _rn_q(M, g, choices=['$33°$', '$21°$', '$59°$', '$47°$'], correct=4, expl=[
        '$a\\parallel b$ (line $c$ crosses them): the acute angles are equal. Therefore, the acute angle next to $x$ at the lower left is $77°$.',
        '$c\\parallel d$ (the diagonal crosses them): the other acute angle next to $x$ is $56°$.',
        'The three angles make a straight angle: $77°+56°+x=180°$. Therefore, $x=180°-133°=47°$. Choice 4.',
        'Shortcut: $7+6=13$, which ends in $3$. Therefore, $x$ must end in $7$. Only $47°$ does.'], figure=rn_fig_g005())
    V = 'solve-' + g
    _rn_sub(M, V, 2, [
        ('write 83° in the acute angle next to x', 'write 77° in the acute angle next to x'),
        ('The angle we want here is also 83', 'The angle we want here is also 77'),
        ('So this angle is 54.', 'So this angle is 56.'),
        ('write 54° in the other acute angle next to x', 'write 56° in the other acute angle next to x'),
        ('Write 83° + 54° + x = 180°', 'Write 77° + 56° + x = 180°'),
        ('83 plus 54: add the tens — 80 plus 50 is 130. 3 and 4 is 7. 137.',
         '77 plus 56: add the tens — 70 plus 50 is 120. 7 and 6 is 13. 133.'),
        ('Write x = 180° − 137° = 43°', 'Write x = 180° − 133° = 47°'),
        ('137 plus something is 180. 180 minus 137 — 43.', '133 plus something is 180. 180 minus 133 — 47.'),
        ('Circle choice 2', 'Circle choice 4'), ('Choice two.', 'Choice four.')])
    _rn_sub(M, V, 3, [
        ('one angle ends in 3, one ends in 4, plus something.', 'one angle ends in 7, one ends in 6, plus something.'),
        ('Write 3 + 4 = 7 → x ends in 3', 'Write 7 + 6 = 13 → x ends in 7'),
        ('3 and 4 is 7, so x has to end in 3.', '7 and 6 is 13 — it ends in 3. So x has to end in 7.'),
        ('Cross out 51°, 29° and 37°; circle choice 2', 'Cross out 33°, 21° and 59°; circle choice 4'),
        ('Straight to the choices: 1 — doesn\'t fit. 9 — doesn\'t fit. 7 — doesn\'t fit. 3 fits. Mark it.',
         'Straight to the choices: 3 — doesn\'t fit. 1 — doesn\'t fit. 9 — doesn\'t fit. 7 fits. Mark it.')])

    # ---------- g006 (letters only): p, q, r, theta; choice 3 (Hebrew alpha, beta, gamma, delta; choice 1; plug in 150)
    #            ==>  m, n, k, x; choice 4; plug in 140
    g = 'geo30-g006'
    _rn_q(M, g, stem='In the accompanying figure, four lines intersect at one point. Which expression equals $x$?',
          choices=['$m+n+k-180°$', '$m-n+k$', '$m-n-k$', '$m+n+k-360°$'], correct=4, expl=[
        'The angle next to $m$ is $180°-m$, the angle next to $n$ is $180°-n$, the angle next to $k$ is $180°-k$.',
        'These three angles and $x$ make a straight angle: $(180°-m)+(180°-n)+(180°-k)+x=180°$.',
        'Therefore, $540°-(m+n+k)+x=180°$ and $x=m+n+k-360°$. Choice 4.',
        'Plug in: $m=n=k=140°$ gives $x=180°-3\\cdot40°=60°$. Choices 1, 2 and 3 give $240°$, $140°$ and $-140°$. Only choice 4 gives $60°$.'],
          figure=_relabel(M.q(g)['questionVisual']['svg'], {'p': 'm', 'q': 'n', 'r': 'k', 'θ': 'x'}))
    V = 'solve-' + g
    M.slide(V, 2)['items'][1]['t'] = '$(180°-m)+(180°-n)+(180°-k)+x=180°$'
    _rn_lines(M, V, 2, [
        {'say': "In the accompanying figure, four lines meet at one point. Based on the figure — which expression equals x?"},
        {'say': "What's hard about this question? All the information is given with unknowns — not with numbers."},
        {'say': "And that's the main way psychometric geometry questions get harder: working with unknowns instead of numbers."},
        {'say': "We'll solve it three ways: the full mathematical way, the psychometric way — plugging in numbers instead of the unknowns — and a flash of insight, for those who see it."},
        {'say': "Full math first. Where do we start? We need x, and there are lots of unknowns."},
        {'say': "Our base has to be some anchor: either a full angle — 360 degrees — or a straight angle — 180."},
        {'draw': "In the angle next to m, write 180° − m"},
        {'say': "Start with m, the first given. If this angle is m, the angle next to it is 180 minus m."},
        {'draw': "In the angle next to n, write 180° − n"},
        {'say': "Move on to n. The angle next to it is 180 minus n."},
        {'draw': "In the angle next to k, write 180° − k"},
        {'say': "Same for k: 180 minus k."},
        {'say': "Now we have to notice that these three angles and x together make a straight angle — so their sum is 180."},
        {'say': "Once we see that, we've almost finished the question."},
        {'appear': 1, 'label': "The equation appears: (180° − m) + (180° − n) + (180° − k) + x = 180°"},
        {'say': "It's important to be careful with the parentheses. A plus in front doesn't affect the parentheses — but if there were a minus here, it would affect both terms inside."},
        {'say': "In this case we can simply drop the parentheses, because it's all addition."},
        {'draw': "Cross out one 180° on each side of the equation"},
        {'say': "180 and 180 cancel."},
        {'say': "We want x, so we keep it on the left. Move minus m across as plus — and minus n, and minus k. So on the right we have m plus n plus k."},
        {'say': "The two 180s left make 360 together — move it across: minus 360."},
        {'draw': "Write x = m + n + k − 360°"},
        {'say': "So x equals m plus n plus k minus 360."},
        {'draw': "Circle choice 4"},
        {'say': "Choice four."},
        {'say': "Once it was clear what to do, the solution was simple. The question is how you spot it in advance — and on the last question of the section, that's not simple."},
    ])
    _rn_lines(M, V, 3, [
        {'say': "Method two: plugging in numbers."},
        {'say': "There's a way to turn these questions into simpler ones. They made the question harder by putting unknowns instead of numbers."},
        {'say': "So we'll put things back the way they were: numbers instead of unknowns. That turns the question into an easy one."},
        {'say': "If there were a number instead of m — which number? Whatever's comfortable. But it looks obtuse, so plug in an obtuse angle. And don't make it hard for yourself — use round angles."},
        {'say': "It looks like about 140 degrees. So I chose m = 140. 130 would be completely fine too."},
        {'draw': "Write 140° by m, and 40° in the angle next to it"},
        {'say': "If m is 140, the angle next to it is 40. Numbers roll easily — with numbers I complete automatically. With unknowns it's a bit less natural."},
        {'say': "Now n. We could choose something else — but we get to pick the case that's easiest for us. So 140 again."},
        {'say': "Why? Afterwards we'll plug these values into the answers. It's much easier to use the same angle everywhere than to remember: m was 140, n was something else… That could confuse us."},
        {'draw': "Write 140° by n and by k, and 40° next to each"},
        {'say': "So n is 140 — its neighbor is 40. And k is 140 — its neighbor is 40."},
        {'draw': "Write 40° + 40° + 40° = 120°, so x = 180° − 120° = 60°"},
        {'say': "40, 40 and 40 make 120. Together with x they make a straight angle — so x is 180 minus 120: 60 degrees, in this case."},
        {'say': "What now? To the answers. Plug in 140 for m, n and k — and look for 60, in the case we chose."},
        {'say': "Any answer that fits, we can't eliminate. We're hoping to eliminate three answers."},
        {'draw': "Next to choice 1 write 240 and cross it out"},
        {'say': "Choice one: three times 140 is 420, minus 180. Some students already see it's too big — no need to calculate. If you do: 420 minus 200 is 220, plus 20 — 240. Eliminated. We need 60."},
        {'draw': "Next to choice 2 write 140 and cross it out"},
        {'say': "Choice two: 140 minus 140 is 0, plus 140 — 140. Eliminated."},
        {'draw': "Next to choice 3 write −140 and cross it out"},
        {'say': "Choice three: 140 minus 140 is 0, minus 140 — negative. Eliminated."},
        {'draw': "Next to choice 4 write 60 ✓"},
        {'say': "Choice four: 420 minus 360 — exactly 60. It fits."},
        {'say': "And we may mark it only because the other three are already eliminated. That's the rule of plugging in: eliminate three answers first."},
        {'draw': "Circle choice 4"},
        {'say': "Three answers eliminated — mark choice four."},
        {'say': "One warning. The same number for m, n and k is quick — but check that the four answers come out different."},
        {'say': "Here they did: 240, 140, a negative, and 60. If two answers tie, plug in again with other numbers."},
    ])
    M.slide(V, 4)['items'][1]['t'] = '$m+n+k=360°+x$'
    _rn_lines(M, V, 4, [
        {'say': "Now the third solution: a flash of insight."},
        {'say': "Some students — usually very strong students — look at the question and understand in advance that the answer is choice four. How?"},
        {'draw': "Trace the arcs of m, n and k around the point, and shade x"},
        {'say': "They see that m plus n plus k is 360 degrees — plus something more: x. The angle x is counted twice here."},
        {'say': "So if I add m, n and k and subtract 360 from that sum — I'm left with x."},
        {'say': "Give this idea a name: overlapping angles. Add them, and subtract the full turn."},
        {'appear': 1, 'label': "m + n + k = 360° + x appears"},
        {'say': "On one side: m plus n plus k. On the other side — what does it equal? 360 gets us to here, and there's another piece: x."},
        {'draw': "Write x = m + n + k − 360°"},
        {'say': "To isolate x, move the 360 across: x equals m plus n plus k minus 360. Choice four."},
        {'say': "So we've seen three ways. Which one do we choose?"},
        {'say': "The shortest way is the insight. But the vast majority of students don't see it on the exam, in such a short time."},
        {'say': "It's the last question — you're under pressure near the end of the section. If you saw it — wonderful, that's the shortest way. There's almost no work here."},
        {'say': "For most students that leaves two options: mathematical work, or psychometric work with plugging in."},
        {'say': "If you're very strong in geometry and algebra, the mathematical work is completely fine."},
        {'say': "For most students, it's much, much simpler to solve this question by plugging in numbers."},
        {'say': "It turns the question from a very high level into a low one. The completions are almost immediate — and the answer is certain."},
    ])

    # ---------- g007: 38 + 57 = 95 (Hebrew 45 + 50 = 95)  ==>  36 + 62 = 98
    g = 'geo30-g007'
    _rn_q(M, g, choices=['$82°$', '$98°$', '$26°$', '$108°$'], correct=2, expl=[
        'Draw a line through the bend, parallel to $a$ and $b$. It splits $x$ into two parts.',
        'The upper part makes a Z with the $36°$ angle. Therefore, it is $36°$. The lower part makes a Z with the $62°$ angle. Therefore, it is $62°$.',
        '$x=36°+62°=98°$. Choice 2.',
        'Zig-zag rule: $x$ points right, $36°$ and $62°$ point left. Therefore, $x=36°+62°$.'], figure=rn_fig_g007())
    V = 'solve-' + g
    _rn_sub(M, V, 2, [
        ('Write 38° in the upper part of x', 'Write 36° in the upper part of x'),
        ('So this angle equals 38.', 'So this angle equals 36.'),
        ('Write 57° in the lower part of x', 'Write 62° in the lower part of x'),
        ('the acute angle 57 equals the angle here. So this angle is also 57.', 'the acute angle 62 equals the angle here. So this angle is also 62.'),
        ('Write x = 38° + 57° = 95°', 'Write x = 36° + 62° = 98°'),
        ('So x equals 38 plus 57: 95 degrees.', 'So x equals 36 plus 62: 98 degrees.'),
        ('Circle choice 4', 'Circle choice 2'), ('Choice four.', 'Choice two.')])
    _rn_sub(M, V, 3, [
        ('38 points left. 57 points left. x points right.', '36 points left. 62 points left. x points right.'),
        ("'x = 38° + 57° = 95°' appears", "'x = 36° + 62° = 98°' appears"),
        ('$x=38°+57°=95°$', '$x=36°+62°=98°$'),
        ('So x equals 38 plus 57: 95. One step.', 'So x equals 36 plus 62: 98. One step.')])


# --- practice: new numbers ------------------------------------------------------------------------------
def rn_practice_questions(M):
    F = lambda k: 'geo30-foundation-p%02d' % k
    Ad = lambda k: 'geo30-advanced-p%02d' % k
    # f-p01: 42 -> 138  ==>  37 -> 143
    _rn_q(M, F(1), choices=['$37°$', '$143°$', '$153°$', '$147°$'], correct=2, expl=[
        '$x$ and $37°$ are adjacent angles on a straight line: $x+37°=180°$.', '$x=180°-37°=143°$.'], figure=rn_fig_p01())
    # f-p02: 138 = 90 + 48 -> 132  ==>  146 = 90 + 56 -> 124
    _rn_q(M, F(2), choices=['$34°$', '$146°$', '$56°$', '$124°$'], correct=4, expl=[
        'The $146°$ angle is the right angle plus the angle above the horizontal line: $146°-90°=56°$.',
        '$x$ and $56°$ are on a straight line: $x=180°-56°=124°$.'], figure=rn_fig_p02())
    # f-p03: x + 4x + 4x = 180 -> 20  ==>  x + 2x + 2x = 180 -> 36 (traps: forgot the vertical angle 60, the angle 2x = 72)
    _rn_q(M, F(3), choices=['$45°$', '$72°$', '$36°$', '$60°$'], correct=3, expl=[
        'The angle vertical to the upper $2x$ is also $2x$.', 'On the lower straight line: $x+2x+2x=180°$.',
        '$5x=180°$. Therefore, $x=36°$.'], figure=rn_fig_p03())
    # f-p04: 76, p = 2q -> 308  ==>  70, p = 2q -> 305
    _rn_q(M, F(4), choices=['$290°$', '$305°$', '$250°$', '$325°$'], correct=2, expl=[
        '$p$ and $70°$ are on a straight line: $p=180°-70°=110°$.', '$p=2q$. Therefore, $q=\\frac{110°}{2}=55°$.',
        '$q$, $r$, $s$ and $t$ make a full circle. Therefore, $r+s+t=360°-55°=305°$.'], figure=rn_fig_p04())
    # f-p05: 62 -> 118  ==>  57 -> 123
    _rn_q(M, F(5), choices=['$123°$', '$57°$', '$113°$', '$133°$'], correct=1, expl=[
        'The small angles are equal. Therefore, the acute angle at line $b$ is $57°$.',
        '$x$ is a large angle: $x=180°-57°=123°$.'], figure=rn_fig_p05())
    # f-p06: 34 -> 146 + 34 + 146 = 326  ==>  38 -> 142 + 38 + 142 = 322
    _rn_q(M, F(6), choices=['$360°$', '$218°$', '$284°$', '$322°$'], correct=4, expl=[
        '$\\beta$ is a small angle: $\\beta=38°$.', '$\\alpha$ and $\\gamma$ are large angles: $\\alpha=\\gamma=180°-38°=142°$.',
        '$\\alpha+\\beta+\\gamma=142°+38°+142°=322°$.'], figure=rn_fig_p06())
    # f-p07: 64 -> 116 - 64 = 52  ==>  71 -> 109 - 71 = 38
    _rn_q(M, F(7), choices=['$71°$', '$38°$', '$142°$', '$109°$'], correct=2, expl=[
        '$y$ is vertical to the $71°$ angle: $y=71°$.', '$x$ is a large angle: $x=180°-71°=109°$.',
        '$x-y=109°-71°=38°$.'], figure=rn_fig_p07())
    # f-p08: 124 -> beta = 56  ==>  117 -> beta = 63
    _rn_q(M, F(8), choices=['$117°$', '$54°$', '$180°$', '$63°$'], correct=4, expl=[
        '$\\alpha$ and $\\gamma$ are both large angles. Therefore, they are equal: $-\\alpha+\\gamma=0$.',
        'What is left is $\\beta$, a small angle: $\\beta=180°-117°=63°$.'], figure=rn_fig_p08())
    # f-p09: 122 -> 58 + 58 = 116  ==>  128 -> 52 + 52 = 104
    _rn_q(M, F(9), choices=['$104°$', '$52°$', '$128°$', '$256°$'], correct=1, expl=[
        '$\\alpha$ and the $128°$ angle are adjacent on line $a$: $\\alpha=180°-128°=52°$.',
        '$\\beta$ is a small angle, like $\\alpha$. Small angles are equal: $\\beta=52°$.',
        '$\\alpha+\\beta=52°+52°=104°$.'], figure=rn_fig_p09())
    # f-p10: x + 8x = 180 -> 20  ==>  x + 5x = 180 -> 30 (trap 180 / 5 = 36: forgot the x)
    _rn_q(M, F(10), choices=['$25°$', '$36°$', '$30°$', '$60°$'], correct=3, expl=[
        '$x$ is a small angle and $5x$ is a large angle: $x+5x=180°$.', '$6x=180°$. Therefore, $x=30°$.'], figure=rn_fig_p10())

    # a-p01: (4 alpha + gamma) / beta = 5  ==>  (alpha + 3 gamma) / beta = 4
    _rn_q(M, Ad(1), stem='In the accompanying figure, $a\\parallel b$. What is the value of $\\frac{\\alpha+3\\gamma}{\\beta}$?',
          choices=['$3$', '$4$', '$6$', '$2$'], correct=2, expl=[
        '$\\alpha$ and $\\beta$ are vertical angles, and $\\beta$ and $\\gamma$ are both small angles: $\\alpha=\\beta=\\gamma$.',
        '$\\frac{\\alpha+3\\gamma}{\\beta}=\\frac{\\beta+3\\beta}{\\beta}=\\frac{4\\beta}{\\beta}=4$.'])
    # a-p02 (letters): p, q, r, s, t -> p || t (choice 1)  ==>  c, d, e, f, g -> c || g (choice 3)
    _rn_q(M, Ad(2), stem='Five different lines are given:\n$\\begin{cases} c\\parallel d \\\\ d\\perp e \\\\ e\\parallel f \\\\ f\\perp g \\end{cases}$\nWhich of the following is necessarily true?',
          choices=['$c\\perp g$', '$d\\parallel e$', '$c\\parallel g$', '$f\\parallel g$'], correct=3, expl=[
        '$c\\parallel d$ and $d\\perp e$. Therefore, $c\\perp e$. $e\\parallel f$. Therefore, $c\\perp f$ too.',
        '$c\\perp f$ and $g\\perp f$: two lines perpendicular to the same line are parallel. Therefore, $c\\parallel g$.'])
    # a-p03: x = 8 gaps, y = 4 gaps -> 2  ==>  x = 10 gaps, y = 4 gaps -> 5/2 (tick-count trap 11/5)
    _rn_q(M, Ad(3), choices=['$\\frac52$', '$\\frac{11}{5}$', '$2$', '$3$'], correct=1, expl=[
        '$x$ covers $10$ equal gaps and $y$ covers $4$. Count the gaps, not the tick marks.',
        '$\\frac{x}{y}=\\frac{10}{4}=\\frac52$.'], figure=rn_fig_adv03())
    # a-p04: x + 2x + 3x + 168 = 360 -> 32  ==>  x + 2x + 3x + 150 = 360 -> 35 (trap 150 / 6 = 25)
    _rn_q(M, Ad(4), choices=['$35°$', '$25°$', '$70°$', '$45°$'], correct=1, expl=[
        'The four angles make a full circle: $x+2x+3x+150°=360°$.', '$6x=210°$. Therefore, $x=35°$.'], figure=rn_fig_adv04())
    # a-p05: 116 and 136 -> 72  ==>  114 and 144 -> 78
    _rn_q(M, Ad(5), choices=['$30°$', '$78°$', '$36°$', '$66°$'], correct=2, expl=[
        'The $114°$ angle and the angle next to it are on a straight line: that angle is $180°-114°=66°$.',
        'The $144°$ angle is made of this $66°$ angle and $x$: $66°+x=144°$.', '$x=144°-66°=78°$.'], figure=rn_fig_adv05())
    # a-p06 (letters): alpha + u, beta + 3u, 0 < u < 60 -> beta < alpha (choice 1)  ==>  gamma + v, delta + 4v, 0 < v < 45 (choice 3)
    _rn_q(M, Ad(6), stem=GIVEN('\\gamma+v=180°', '\\delta+4v=180°', '0°<v<45°') + 'Which of the following is necessarily true?',
          choices=['$\\delta>\\gamma$', '$\\delta=\\gamma$', '$\\delta<\\gamma$', CBD], correct=3, expl=[
        '$\\gamma=180°-v$ and $\\delta=180°-4v$.',
        'Since $v>0$, $4v>v$: $\\delta$ subtracts more from the same $180°$. Therefore, $\\delta<\\gamma$.',
        'Plug in to check: $v=10°$ gives $\\gamma=170°$ and $\\delta=140°$.'])
    # a-p07 (letters): k, l, m, n -> k || m (choice 1)  ==>  p, q, r, s -> p || r (choice 4)
    _rn_q(M, Ad(7), stem='Four different lines are given:\n$\\begin{cases} p\\perp q \\\\ q\\perp r \\\\ r\\perp s \\end{cases}$\nWhich of the following is necessarily true?',
          choices=['$q\\perp s$', '$p\\perp r$', '$p\\parallel s$', '$p\\parallel r$'], correct=4, expl=[
        '$p$ and $r$ are both perpendicular to $q$. Two lines perpendicular to the same line are parallel: $p\\parallel r$.',
        '(Also $q\\parallel s$, since both are perpendicular to $r$. Therefore, choice 1, $q\\perp s$, is false.)'])
    # a-p08: 103, 48 -> 29 + 77 = 106  ==>  109, 43 -> 28 + 71 = 99
    _rn_q(M, Ad(8), choices=['$71°$', '$137°$', '$99°$', '$114°$'], correct=3, expl=[
        '$\\alpha$, $43°$ and $109°$ make a straight angle: $\\alpha=180°-109°-43°=28°$.',
        '$\\beta$ is made of $43°$ and $\\alpha$: $\\beta=43°+28°=71°$.', '$\\alpha+\\beta=28°+71°=99°$.'], figure=rn_fig_adv08())
    # a-p09 (letters): P, Q, R, S; a = PR, b = QS (choice 1)  ==>  E, F, G, H; c = EG, d = FH (choice 2)
    _rn_q(M, Ad(9), stem='Points $E$, $F$, $G$ and $H$ lie on a line in this order.\n' + GIVEN('c=EG', 'd=FH') + 'Which of the following is necessarily true?',
          choices=['$c+d>EH+FG$', '$c+d=EH+FG$', '$c+d<EH+FG$', CBD], correct=2, expl=[
        '$c+d=EG+FH=(EF+FG)+(FG+GH)$.', '$EH+FG=(EF+FG+GH)+FG$.',
        'Both sums have $EF$ once, $GH$ once and $FG$ twice. They are equal: $c+d=EH+FG$.'],
          figure=_relabel(M.q(Ad(9))['questionVisual']['svg'], {'P': 'E', 'Q': 'F', 'R': 'G', 'S': 'H'}))
    # a-p10 (letters): p, q overlap on x (choice 2)  ==>  u, v overlap on y (choice 3); figure redrawn (0, 60, 130)
    _rn_q(M, Ad(10), stem='In the accompanying figure, three lines meet at one point. The angles $u$ and $v$ overlap on the angle $y$. Which expression equals $y$?',
          choices=['$v-u$', '$360°-u-v$', '$u+v-180°$', '$\\frac{u+v}{3}$'], correct=3, expl=[
        '$u$ and $v$ together cover the straight angle once, and $y$ twice: $u+v=180°+y$.',
        'Therefore, $y=u+v-180°$. Choice 3.',
        'Plug in to check: $u=130°$, $v=120°$ gives $y=70°$. Choice 1 gives $-10°$, choice 2 $110°$, choice 4 about $83°$.'],
          figure=rn_fig_adv10())


def rn_practice(M):
    """Approved clean-up (39 -> 26): the copy f-p14 (= guided g007); 9 of the 13 English extras (keep f-p13, f-p17,
    a-p11, a-p16); the September items whose type the Hebrew practice already has (q-05 U with algebra = f-p10,
    q-06 equal gaps = a-p03, q-09 parallel or not = q-04, which stays)."""
    out = ['geo30-foundation-p14',   # copy of guided g007 (one bend, parallel line through the bend)
           'geo30-foundation-p16',   # distance between parallel lines = 7: too easy
           'geo30-foundation-p12',   # full circle with numbers: the type is in a-p04
           'geo30-foundation-p11',   # bisector of the adjacent angle: bisectors stay in a-p11
           'geo30-foundation-p15',   # three parallel lines and a fourth line: too easy
           'geo30-advanced-p12',     # obtuse - acute = 46: small + large is in f-p10 / f-p05
           'geo30-advanced-p13',     # 3 + 2 parallel lines -> 6 points
           'geo30-advanced-p14',     # straight angle in three parts: the type is in f-p03 / f-p17
           'geo30-advanced-p15',     # (2x + 11) + (5x + 1) = 180: the type is in f-p10
           'geo30-advanced-p17',     # four angles of a full turn: the type is in a-p04
           'q-r26-t30-05',           # U with algebra: Hebrew f-p10
           'q-r26-t30-06',           # equal gaps on a line: Hebrew a-p03
           'q-r26-t30-09']           # parallel or not (U = 180): q-r26-t30-04 drills it and stays
    for qid in out:
        assert M.section_of(qid) in (FOUND, ADV), qid
        M.unplace(qid)
    F = lambda k: 'geo30-foundation-p%02d' % k
    Ad = lambda k: 'geo30-advanced-p%02d' % k
    M.practice_order(FOUND, [F(1), F(2), F(17), F(3), F(4), F(5), F(9), F(10), F(13), F(6), F(7), F(8), NEW[4]])
    M.practice_order(ADV, [Ad(11), Ad(4), Ad(1), Ad(5), Ad(8), Ad(7), Ad(2), Ad(3), Ad(16), Ad(9), Ad(6), Ad(10), NEW[7]])


def rn_lessons_cards(M):
    # card tip quoted the old g005 numbers (83 + 54 -> x ends in 3): a separate example now
    c = M.card('mem-lines-angles')
    old = 'Adding angles to $180°$? Use the units digit: $83°+54°+x=180°$ → $3+4=7$. Therefore, $x$ ends in $3$.'
    assert old in c['tips']
    c['tips'] = [('Adding angles to $180°$? Use the units digit: $64°+79°+x=180°$ → $4+9=13$. Therefore, $x$ ends in $7$.'
                  if t == old else t) for t in c['tips']]
    # summary 2: the letters of guided g006 changed (p, q, r, theta -> m, n, k, x)
    vid = 'r26-t30-summary-2'
    _rn_sub(M, vid, _rn_slide_no(M, vid, 'Anchor: 180° or 360°'), [
        ("'The angle next to p: 180° − p' appears", "'The angle next to m: 180° − m' appears"),
        ('The angle next to $p$: $\\ 180°-p$', 'The angle next to $m$: $\\ 180°-m$')])
    _rn_sub(M, vid, _rn_slide_no(M, vid, 'Letters: plug in'), [
        ("'p = q = r = 130° → θ = 30°' appears", "'m = n = k = 130° → x = 30°' appears"),
        ('$p=q=r=130°\\ \\to\\ \\theta=30°$', '$m=n=k=130°\\ \\to\\ x=30°$')])
    _rn_sub(M, vid, _rn_slide_no(M, vid, 'Overlapping angles'), [
        ("'θ = p + q + r − 360°' appears", "'x = m + n + k − 360°' appears"),
        ('$\\theta=p+q+r-360°$', '$x=m+n+k-360°$'),
        ('p, q and r cover the full turn, and theta one more time. So theta is their sum minus 360.',
         'm, n and k cover the full turn, and x one more time. So x is their sum minus 360.')])


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
