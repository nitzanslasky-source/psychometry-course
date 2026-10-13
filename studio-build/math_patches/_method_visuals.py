"""Method visuals library (2026-10-13, teacher: "always check if the visuals change a bit. Like when we have the V method,
we need to teach it with the V table and the way it looks ... The seesaw method also has special visuals of its own").

Every method that has a SIGNATURE visual in the Hebrew course is shown with THAT visual, built step by step at the
spoken words - never as a plain list of lines. The catalog (what each looks like, the drawing order, where it is first
taught) is the section "Method visuals library" of real_exam/TEACHING_STYLE_GUIDE.md.

Not a patch (math_api only loads t*.py). A topic's _ai_vis_tNN.py loads it with importlib and turns the layers into
board items with its own _layers() (the same layer mechanics as DIST / STRIP / TREE / ZL there):

    MV = _load('_method_visuals')                      # importlib, like _shaded_nl
    sl = MV.items(_layers, 'n1', MV.SLOT(...), col=0)  # -> {key: item}; show them IN ORDER at the spoken words

Every builder returns [(key, svg), ...]: the first key is 'line' (the base layer: drawn first, a figure item of its own),
every later key is a layer drawn over it at the same place (over=1), shown in the listed order. The SVG uses only
<svg> <title> <line> <path> <rect> <circle> <text> <tspan> (strict XML; svgcheck), the palette of _shaded_nl (ink,
teal, band) and big bold labels (about the handwriting size). `fit` = the board width the figure wants at a 1:1 scale
(1 svg unit = 1 board px), so labels match the typed items next to it.

Builders (topic = where the Hebrew course first teaches the method)
    SLOT(rule, rows)              substitution: the rule with its slots boxed, then THE SAME template with the input in
                                  each slot (teal), then the calculation            (19, alg 18862)
    CHAIN(rows, up=None)          inside out / circular: each row is one call; the value found flows (arrow) into the next
                                  row's slot; up = the values climbing back up       (19, alg 18910-18925)
    COLS(rows, op, marks)         stacked digit columns, built column by column     (18, alg 18215-18219)
    VTABLE(given, asked, unknown) the team | work | time table and the V (or the upside-down V)   (26, wp 6285-6341)
    SEESAW(v1, w1, v2, w2, avg)   the weighted-average axis: values above, weights below, w1 + w2 units, the pivot
                                                                                    (25, wp 5698-5777)
    RATIO(cols, given, asked)     the ratio table, the x k arrows or the diagonal  (22, wp 1302-1392; reused 23-29, 36)
    DST(rows)                     the distance | time | speed table                 (27, wp 7175, 7550)
    PCTTREE(root, first, second)  the percent tree                                  (23, wp 3338-3376)
    VENN(...) / STRIP4(...)       two overlapping circles / the squares method      (24, wp 4339, 4570-4617)
    TRI(top, left, right)         the formula triangle (work / motion)              (26, 27, wp 5945, 7004)
Helpers: carry(ns, plan) - the "so far" box on a cleared slide; post(ns) - this module's visual fixes and carry-overs for
a topic file (called at the very end of _ai_vis_tNN.py, AFTER the clarity overlay, so Codex's cue checks are untouched).
"""
import html as _html

INK, TEAL, BAND, LIGHT = '#203344', '#087f83', '#d5f1ed', '#eef8f6'
RED = '#d62d48'
FONT = 'font-family="DejaVu Sans,Arial,sans-serif"'


def _esc(t):
    return _html.escape(str(t), quote=True)


def _svg(w, h, body, title, y0=0):
    t = _esc(title)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 %d %d %d" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (y0, w, h, t, t, body))


# ------------------------------------------------------------------------------------------- a tiny math-text layout
# markup: [[x]] = a slot (x in a teal box), {{x}} = a value put in (teal, bold, light fill), ^2 or ^{..} = a superscript.
def _cw(c):
    # about Arial / DejaVu bold (the slide font falls back to Arial on a Mac): a little wide is safe (a gap), narrow
    # would overlap
    if c in '()[]|.,:;·\'': return .36
    if c == ' ': return .29
    if c == '◆': return .8
    if c in '−+=<>×÷': return .62
    if c in 'mwMW': return .88
    if c.isdigit(): return .6
    return .6


def _parse(s):
    """-> [(text, kind)] kind: n | sup | slot | val | supval"""
    out, i, cur = [], 0, ''
    def flush():
        nonlocal cur
        if cur: out.append((cur, 'n')); cur = ''
    while i < len(s):
        if s.startswith('[[', i):
            flush(); j = s.index(']]', i); out.append((s[i + 2:j], 'slot')); i = j + 2
        elif s.startswith('{{', i):
            flush(); j = s.index('}}', i); out.append((s[i + 2:j], 'val')); i = j + 2
        elif s[i] == '^':
            flush()
            if s[i + 1] == '{': j = s.index('}', i); txt = s[i + 2:j]; i = j + 1
            else: txt = s[i + 1]; i += 2
            if out and out[-1][1] == 'val' and txt: out.append((txt, 'sup'))
            else: out.append((txt, 'sup'))
        else:
            cur += s[i]; i += 1
    flush()
    return out


def _width(s, size):
    w = 0
    for t, k in _parse(s):
        f = .62 if k == 'sup' else 1
        w += sum(_cw(c) for c in t) * size * f + (14 if k in ('slot', 'val') else 0)
    return w


def _row(s, x, y, size, ink=INK, boxes=None):
    """draw markup s with its left end at x, baseline y -> (svg, [(x0, x1) of every slot / value box], end x)"""
    body, bx = '', []
    for t, k in _parse(s):
        if k == 'sup':
            w = sum(_cw(c) for c in t) * size * .62
            body += '<text x="%.1f" y="%.1f" fill="%s" %s font-size="%d" font-weight="bold">%s</text>' % (x, y - size * .45, ink, FONT, size * .62, _esc(t))
            x += w; continue
        w = sum(_cw(c) for c in t) * size
        if k in ('slot', 'val'):
            pad = 7; x0 = x; x += pad
            fill, col = (LIGHT, TEAL) if k == 'slot' else (BAND, TEAL)
            body += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x0, y - size * .86, w + 2 * pad, size * 1.14, fill, col)
            body += '<text x="%.1f" y="%.1f" fill="%s" %s font-size="%d" font-weight="bold">%s</text>' % (x, y, TEAL if k == 'val' else ink, FONT, size, _esc(t))
            x += w + pad; bx.append((x0, x)); continue
        body += '<text x="%.1f" y="%.1f" fill="%s" %s font-size="%d" font-weight="bold" xml:space="preserve">%s</text>' % (x, y, ink, FONT, size, _esc(t))
        x += w
    return body, bx, x


def _arrow(x1, y1, x2, y2, col=TEAL, w=2.6):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 13
    p1 = (x2 - L * math.cos(a - .42), y2 - L * math.sin(a - .42)); p2 = (x2 - L * math.cos(a + .42), y2 - L * math.sin(a + .42))
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"/>' % (x1, y1, x2 - 6 * math.cos(a), y2 - 6 * math.sin(a), col, w) +
            '<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="%s"/>' % (x2, y2, p1[0], p1[1], p2[0], p2[1], col))


def _text(x, y, t, size=26, col=INK, anchor='middle', weight='bold', style=''):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" fill="%s" %s font-size="%d" font-weight="%s"%s>%s</text>'
            % (x, y, anchor, col, FONT, size, weight, (' font-style="%s"' % style) if style else '', _esc(t)))


# ------------------------------------------------------------------------------------------------ topic 19: SLOT
def SLOT(rule, rows, size=34, title='Substitution'):
    """the substitution picture (Hebrew topic 19: «זה בדיוק אותה תבנית... איפה שהיה לי a אני מציב 4», "the same template,
    and where there was an a, I put the 4"): the rule, its slots boxed; under it the SAME template with the input in
    every slot (teal); then the calculation rows.
      rule  markup, slots as [[a]]            e.g. '◆([[a]]) = [[a]]^2 − 4·[[a]]'
      rows  [(key, markup)], the first one is the template filled in, values as {{6}}  e.g. ('in', '◆({{6}}) = {{6}}^2 − 4·{{6}}')
    Arrows go from every slot of the rule down to the matching value of the FIRST row (same count).
    -> [('line', rule), (key, row) ...]"""
    gap = size * 1.75; x0 = 12
    W = int(max([_width(rule, size)] + [_width(m, size) for _, m in rows]) + 2 * x0 + 10)
    y = size * 1.05
    b0, slots, _ = _row(rule, x0, y, size)
    H = int(y + gap * len(rows) + size * .5)
    out = [('line', _svg(W, H, b0, 'The rule: ' + _plain(rule)))]
    for i, (key, m) in enumerate(rows):
        yy = y + gap * (i + 1)
        b, vals, _ = _row(m, x0, yy, size)
        if i == 0:
            for (a0, a1), (c0, c1) in zip(slots, vals):
                b = _arrow((a0 + a1) / 2, y + size * .32, (c0 + c1) / 2, yy - size * .9) + b
        out.append((key, _svg(W, H, b, _plain(m))))
    return out


# ------------------------------------------------------------------------------------------------ topic 19: CHAIN
def CHAIN(rows, up=None, size=34, title='Inside out', links=None):
    """one row per call of the operation, top to bottom; the result found in a row flows (a teal arrow) into the next row:
    from the row's LAST box ({{v}} or [[x]]) to the next row's FIRST box.
      rows  [(key, markup)]  first key should be 'line'    e.g. ('line', '◆([[◆(5)]])'), ('in', '[[◆(5)]] = 5^2 = {{25}}'),
                                                          ('out', '◆({{25}}) = 25^2 = {{625}}')
      up    circular rules: [(key, value), ...] for the rows ABOVE the bottom one, from the bottom up - the value of each
            row, written at its right end, with a teal arrow climbing from the row below ("climb back up")
    -> [(key, svg) ...] in the order to show them (rows, then the up values)"""
    gap = size * 1.75; x0 = 12
    widths = [_width(m, size) for _, m in rows]
    xr = max(widths) + x0 + 40
    upw = max([_width('= ' + v, size) for _, v in (up or [])] + [0])
    W = int(xr + upw + 30 if up else max(widths) + 2 * x0 + 10)
    H = int(size * 1.05 + gap * (len(rows) - 1) + size * .55)
    out, prev = [], None
    for i, (key, m) in enumerate(rows):
        y = size * 1.05 + gap * i
        b, bx, xe = _row(m, x0, y, size)
        if prev and bx and (links is None or i in links):
            (p0, p1), py = prev
            b = _arrow((p0 + p1) / 2, py + size * .32, (bx[0][0] + bx[0][1]) / 2, y - size * .9) + b
        prev = (bx[-1], y) if bx else None
        out.append((key if i else 'line', _svg(W, H, b, _plain(m))))
    # the climb back up: the bottom row is the start value (it holds its own number); every row above it gets its value
    # at the right end, with a teal arrow climbing from the row below
    for j, (key, v) in enumerate(up or []):
        i = len(rows) - 2 - j
        y = size * 1.05 + gap * i
        b, _, _ = _row('= {{%s}}' % v, xr, y, size)
        if j == 0 and prev:
            (p0, p1), py = prev
            b = _arrow(p1 + 8, py - size * .4, xr + 40, y + size * .38) + b
        elif j:
            b = _arrow(xr + 40, y + gap - size * .95, xr + 40, y + size * .38) + b
        out.append((key, _svg(W, H, b, '= ' + v)))
    return out


def _plain(m):
    return m.replace('[[', '').replace(']]', '').replace('{{', '').replace('}}', '').replace('^{', '^').replace('}', '')


# ------------------------------------------------------------------------------------------------ topic 18: COLS
def COLS(rows, op='+', size=46, marks=(), title='Written in columns'):
    """stacked digit columns (Hebrew topic 18: «נכתוב את זה במאונך», write it vertically - the columns line up), built
    column by column. rows = the numbers as strings, right-aligned (letters or digits, e.g. ['BA', 'DA']); op = the sign
    in front of the last row; the result row is the LAST string of `rows` (under the line).
    marks = [(key, column, kind)] layers drawn on top, in order: column = 0 for the ones, 1 for the tens ...;
    kind 'ring' (a teal box around the whole column), 'carry:1' (a small carry digit above the column),
    'digit:R:x' (write x under row R of that column, teal).  -> [('line', the frame), (key, layer) ...]"""
    cw = size * .78; n = max(len(r) for r in rows); x_right = 40 + cw * (n + 1); gap = size * 1.22; top = size * 1.6
    W = int(x_right + 30); H = int(top + gap * len(rows) + size * .5)
    X = lambda c: x_right - cw * (c + .5)
    body = ''
    for i, r in enumerate(rows):
        y = top + gap * i + (size * .25 if i == len(rows) - 1 else 0)
        for c, ch in enumerate(reversed(r)):
            body += _text(X(c), y, ch, size)
        if i == len(rows) - 2:
            body += _text(X(n) + 4, y, op, size)
            yl = y + size * .32
            body += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>' % (X(n) - cw * .4, yl, x_right, yl, INK)
    out = [('line', _svg(W, H, body, title))]
    for key, c, kind in marks:
        if kind == 'ring':
            b = '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="none" stroke="%s" stroke-width="3"/>' % (X(c) - cw * .48, top - size * .95, cw * .96, gap * (len(rows) - 1) + size * 1.45, TEAL)
        elif kind.startswith('carry:'):
            b = _text(X(c), top - size * .95, kind[6:], int(size * .55), TEAL)
        elif kind.startswith('digit:'):
            _, r, x = kind.split(':', 2)
            y = top + gap * int(r) + (size * .25 if int(r) == len(rows) - 1 else 0) + size * .62
            b = _text(X(c), y, x, int(size * .5), TEAL)
        else:
            continue
        out.append((key, _svg(W, H, b, '%s column %d' % (kind, c))))
    return out


# ------------------------------------------------------------------------------------------- a table frame (shared)
def _table(cols, nrows, colw, rowh, x0=10, y0=10, head_h=None):
    head_h = head_h or rowh
    W = x0 * 2 + sum(colw); H = y0 * 2 + head_h + rowh * nrows
    xs = [x0]
    for w in colw: xs.append(xs[-1] + w)
    body = ''
    for i, c in enumerate(cols):
        body += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (xs[i], y0, colw[i], head_h, LIGHT)
        body += _text((xs[i] + xs[i + 1]) / 2, y0 + head_h * .66, c, 24)
    for k in range(nrows + 2):
        y = y0 + (head_h + rowh * (k - 1) if k else 0)
        if k == 0: y = y0
        body += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"/>' % (x0, y, xs[-1], y, INK, 2.4 if k < 2 else 1.6)
    for x in xs:
        body += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>' % (x, y0, x, y0 + head_h + rowh * nrows, INK)
    cell = lambda r, c: ((xs[c] + xs[c + 1]) / 2, y0 + head_h + rowh * r + rowh * .64)
    return W, H, body, cell, xs


# --------------------------------------------------------------------------------------------- topic 26: VTABLE
def VTABLE(given, asked, unknown='time', title='The V method'):
    """the team table of the V method (Hebrew wp 6285-6341: «בטבלת צוות, עבודה, זמן... שהעבודה תהיה באמצע... אנחנו
    מסמנים V בין הנתונים... לכפול בין המספרים שמחוברים בקו ולחלק במה שנשאר»): columns team | work | time (work ALWAYS in
    the middle), row 1 = the given situation, row 2 = the asked one. The V joins three numbers: its bottom point on the
    row-2 work, its arms up to the row-1 team and the row-1 time. Multiply the three joined numbers, divide by the other
    two. When the WORK is the unknown, the V is upside down: apex on the row-1 work, arms down to the row-2 team and time.
      given, asked  (team, work, time) as strings, '?' = the unknown (drawn teal)
    -> [('line', the empty table), ('r1', the given row), ('r2', the asked row), ('v', the V), ('calc', the rule line)]"""
    colw = [170, 170, 170]; W, H, body, cell, xs = _table(('Team', 'Work', 'Time'), 2, colw, 74, y0=10)
    H += 60
    out = [('line', _svg(W, H, body, title + ': team, work, time'))]
    for r, row in enumerate((given, asked)):
        b = ''.join(_text(*cell(r, c), v, 30, TEAL if v == '?' else INK) for c, v in enumerate(row) if v != '')
        out.append(('r%d' % (r + 1), _svg(W, H, b, 'row %d: team %s, work %s, time %s' % ((r + 1,) + tuple(row)))))
    (xt1, yt1), (xw1, yw1), (xm1, ym1) = cell(0, 0), cell(0, 1), cell(0, 2)
    (xt2, yt2), (xw2, yw2), (xm2, ym2) = cell(1, 0), cell(1, 1), cell(1, 2)
    if unknown != 'work':      # V: bottom point on the row-2 work
        b = ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>'
             % (xt1 + 26, yt1 - 6, xw2, yw2 + 12, xm1 - 26, ym1 - 6, TEAL))
        joined = '%s · %s · %s' % (given[0], asked[1], given[2])
    else:                      # the upside-down V: apex on the row-1 work
        b = ('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>'
             % (xt2 + 26, yt2 - 14, xw1, yw1 - 30, xm2 - 26, ym2 - 14, TEAL))
        joined = '%s · %s · %s' % (asked[0], given[1], asked[2])
    out.append(('v', _svg(W, H, b, 'the V joins ' + joined)))
    out.append(('calc', _svg(W, H, _text(W / 2, H - 22, 'multiply the V, divide by the other two', 22, TEAL), 'multiply the V, divide by the other two')))
    return out


# --------------------------------------------------------------------------------------------- topic 25: SEESAW
def SEESAW(v1, w1, v2, w2, avg=None, title='The seesaw'):
    """the weighted-average seesaw, in its exam form (Hebrew wp 5698-5777: «לדחוף את הציר של הנדנדה לכיוון הקבוצה הכבדה...
    בבחינה לא נצייר נדנדה... אנחנו מציירים ציר... מעל הציר הציונים... מתחת המשקל... היחס בין המשקלים 1:4, המרחקים 4:1»):
    a horizontal axis; ABOVE each end the group's value, BELOW it the group's weight; the gap is cut into w1 + w2 equal
    units; the pivot (the average) sits w2 units from v1 (closer to the heavier side).
      v1, v2 the two values (v1 < v2), w1, w2 their weights (numbers), avg = the label of the pivot (None: '?')
    -> [('line', the axis), ('vals', the values above), ('wts', the weights below), ('units', the w1 + w2 equal units),
        ('pivot', the pivot under the average and its two distances)]"""
    L_, R_, Y_ = 70, 570, 80; W, H = 640, 200
    body = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>' % (L_, Y_, R_, Y_, INK) +
            ''.join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (x, Y_ - 12, x, Y_ + 12, INK) for x in (L_, R_)))
    out = [('line', _svg(W, H, body, title))]
    out.append(('vals', _svg(W, H, _text(L_, Y_ - 24, v1, 30) + _text(R_, Y_ - 24, v2, 30), 'values %s and %s' % (v1, v2))))
    out.append(('wts', _svg(W, H, _text(L_, Y_ + 46, w1, 28, TEAL) + _text(R_, Y_ + 46, w2, 28, TEAL), 'weights %s and %s' % (w1, w2))))
    n = int(w1) + int(w2); step = (R_ - L_) / float(n)
    u = ''.join('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (L_ + k * step, Y_ - 7, L_ + k * step, Y_ + 7, TEAL) for k in range(1, n))
    out.append(('units', _svg(W, H, u, '%d equal units' % n)))
    xp = L_ + int(w2) * step
    b = ('<path d="M %.1f %d L %.1f %d L %.1f %d Z" fill="%s"/>' % (xp, Y_ + 4, xp - 17, Y_ + 34, xp + 17, Y_ + 34, TEAL)
         + _text(xp, Y_ + 66, avg if avg is not None else '?', 28, TEAL)
         + _text((L_ + xp) / 2, Y_ + 100, '%d unit%s' % (int(w2), '' if int(w2) == 1 else 's'), 20, TEAL) + _text((xp + R_) / 2, Y_ + 100, '%d unit%s' % (int(w1), '' if int(w1) == 1 else 's'), 20, TEAL))
    out.append(('pivot', _svg(W, H, b, 'the pivot, %s units from %s' % (w2, v1))))
    return out


# ---------------------------------------------------------------------------------------------- topic 22: RATIO
def RATIO(cols, given, asked, h=None, v=None, diag=False, title='Ratio table'):
    """the ratio table (Hebrew wp 1302-1392: «אני עושה עמודה של תבניות ועמודה של עוגיות... יחס אופקי שלם... כפול 6...
    יחס אנכי... כפלתי פי 4... היחס לא שלם ולכן אני מחבר קו באלכסון... כופל באלכסון, מחלק במה שנשאר»): one column per
    quantity, row 1 the known pair, row 2 the new value and the unknown ('?'). A whole factor: the horizontal arrow across
    row 1 (h, e.g. '×6') or the vertical arrow down a column (v, e.g. '×4'); otherwise the diagonal (the "triangle").
    -> [('line', header), ('r1', ...), ('r2', ...), then ('h' / 'v' / 'diag')]"""
    colw = [180] * len(cols); W, H, body, cell, xs = _table(tuple(cols), 2, colw, 74, y0=40)
    W += 80; H += 10
    out = [('line', _svg(W, H, body, title + ': ' + ', '.join(cols)))]
    for r, row in enumerate((given, asked)):
        b = ''.join(_text(*cell(r, c), val, 30, TEAL if val == '?' else INK) for c, val in enumerate(row) if val != '')
        out.append(('r%d' % (r + 1), _svg(W, H, b, 'row %d: %s' % (r + 1, ', '.join(row)))))
    if h:
        (x1, y1), (x2, _) = cell(0, 0), cell(0, 1)
        b = _arrow(x1 + 32, y1 - 10, x2 - 34, y1 - 10) + _text((x1 + x2) / 2, y1 - 26, h, 20, TEAL)
        out.append(('h', _svg(W, H, b, 'across: ' + h)))
    if v:
        (x, y1), (_, y2) = cell(0, len(cols) - 1), cell(1, len(cols) - 1)
        b = _arrow(xs[-1] + 24, y1 - 8, xs[-1] + 24, y2 - 18) + _text(xs[-1] + 52, (y1 + y2) / 2, v, 22, TEAL)
        out.append(('v', _svg(W, H, b, 'down: ' + v)))
    if diag:
        q = [(r, c) for r, row in enumerate((given, asked)) for c, val in enumerate(row) if val == '?'][0]
        (xa, ya) = cell(1 - q[0], q[1]); (xb, yb) = cell(q[0], 1 - q[1])
        b = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>' % (xa, ya - 10, xb, yb - 10, TEAL)
        out.append(('diag', _svg(W, H, b, 'multiply along the diagonal, divide by what is left')))
    return out


# ------------------------------------------------------------------------------------------------ topic 27: DST
def DST(rows, cols=('Distance', 'Time', 'Speed'), title='Distance, time, speed'):
    """the motion table (Hebrew wp 7175-7180, 7550-7555, 7879: «נציב את הנתונים בטבלה... תמיד אני שם את המרחק שבין שני
    הגופים»): one row per leg / per body (or one "between them" row); the unknown is x / t / '?' (teal).
    rows [(label, ...)] -> [('line', header), ('r1', ...) ...]"""
    colw = [150] + [170] * len(cols); W, H, body, cell, xs = _table(('',) + tuple(cols), len(rows), colw, 70)
    out = [('line', _svg(W, H, body, title))]
    for r, row in enumerate(rows):
        b = ''.join(_text(*cell(r, c), val, 28 if c else 22, TEAL if val in ('?', 'x', 't') else INK) for c, val in enumerate(row) if val != '')
        out.append(('r%d' % (r + 1), _svg(W, H, b, 'row %d: %s' % (r + 1, ', '.join(row)))))
    return out


# ------------------------------------------------------------------------------------------- topic 23: PCTTREE
def PCTTREE(root, first, second=None, title='Percent tree'):
    """the percent tree (Hebrew wp 3338-3376: «אנחנו משרטטים עץ. הסקר - ממנו אנחנו מתחילים... מתחלק ל-2... כל פעם שאני
    יורד ענף זה עכשיו השלם החדש, 100%... כופל בין האחוזים שהובילו לאותו ענף»): the root (the whole, 100%), its split
    (adds up to 100%), then ONE node splits again (its own 100%); a leaf = the product along its path. (The Hebrew course
    has no probability tree.)
      first [(label, pct)], second (index of the node that splits, [(label, pct)]) -> [('line', root), ('b1', ...), ('b2', ...)]"""
    W, H = 660, 300; rx, ry = 70, 150
    out = [('line', _svg(W, H, _text(8, ry + 9, root, 22, INK, 'start'), title))]
    ys = [ry - 80, ry + 80][:len(first)] if len(first) == 2 else [ry + (i - (len(first) - 1) / 2) * 90 for i in range(len(first))]
    b = ''
    for (lab, p), y in zip(first, ys):
        b += '<line x1="%d" y1="%d" x2="%d" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (150, ry, 280, y, INK) + _text(290, y + 8, lab, 22, INK, 'start') + _text(190, (ry + y) / 2 - 10, p, 22, TEAL)
    out.append(('b1', _svg(W, H, b, 'first split')))
    if second:
        k, kids = second; y0 = ys[k]; b = ''
        for j, (l2, p2) in enumerate(kids):
            y2 = y0 + (j - (len(kids) - 1) / 2) * 70
            b += '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (420, y0, 520, y2, INK) + _text(528, y2 + 8, l2, 20, INK, 'start') + _text(470, (y0 + y2) / 2 - 8, p2, 20, TEAL)
        out.append(('b2', _svg(W, H, b, 'the second split')))
    return out


# ---------------------------------------------------------------------------------------- topic 24: VENN, STRIP4
def VENN(la, lb, a_only=None, both=None, b_only=None, outside=None, title='Two groups'):
    """two overlapping circles (Hebrew wp 4339-4354: «סירות המפרש, העיגול הכחול, וסירות המנוע, העיגול הכתום... גם וגם...
    רק מפרש... לא ולא»): the circles with their names, then the regions, the overlap ("both") first.
    -> [('line', circles), ('both', ...), ('a', ...), ('b', ...), ('out', ...)] - only the parts given"""
    W, H = 560, 260
    body = ('<rect x="6" y="6" width="548" height="248" rx="10" fill="none" stroke="%s" stroke-width="1.6"/>' % INK +
            '<circle cx="215" cy="135" r="95" fill="none" stroke="%s" stroke-width="2.6"/>' % INK +
            '<circle cx="345" cy="135" r="95" fill="none" stroke="%s" stroke-width="2.6"/>' % TEAL +
            _text(150, 32, la, 22) + _text(410, 32, lb, 22, TEAL))
    out = [('line', _svg(W, H, body, title))]
    for key, val, x, y in (('both', both, 280, 145), ('a', a_only, 175, 145), ('b', b_only, 385, 145), ('out', outside, 510, 235)):
        if val is not None:
            out.append((key, _svg(W, H, _text(x, y, val, 30, TEAL if key == 'both' else INK), '%s: %s' % (key, val))))
    return out


def STRIP4(la, lb, cells=('', '', '', ''), ta=None, tb=None, total=None, title='The squares method'):
    """the squares method (Hebrew wp 4570-4617: «המלבן הזה מייצג... ניצור ביניהם חפיפה... אני הולך להוסיף ריבוע נוסף...
    הלא ולא... כמו סודוקו, למלא... אני ישר מצייר מלבן ארוך וישר מחלק אותו ל-4 ריבועים»): one long rectangle cut into 4
    equal boxes - only A | both | only B | neither (left to right in English); a bracket over boxes 1-2 = group A, a
    bracket over boxes 2-3 = group B, all four = the total. Filled like a sudoku.
    -> [('line', the 4 boxes), ('a', the A bracket + total), ('b', the B bracket + total), ('tot', the total),
        ('c1'..'c4', each box filled)]"""
    W, H = 720, 220; x0, y0, bw, bh = 20, 90, 150, 70
    body = ''.join('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x0 + i * bw, y0, bw, bh, LIGHT if i == 1 else 'none', INK) for i in range(4))
    body += ''.join(_text(x0 + i * bw + bw / 2, y0 + bh + 26, t, 18) for i, t in enumerate(('only ' + la, 'both', 'only ' + lb, 'neither')))
    out = [('line', _svg(W, H, body, title))]
    br = lambda i0, i1, y, lab, col: ('<path d="M %d %d L %d %d L %d %d L %d %d" fill="none" stroke="%s" stroke-width="2.6"/>'
                                      % (x0 + i0 * bw + 6, y + 12, x0 + i0 * bw + 6, y, x0 + i1 * bw - 6, y, x0 + i1 * bw - 6, y + 12, col) +
                                      _text(x0 + (i0 + i1) * bw / 2, y - 8, lab, 22, col))
    if ta is not None: out.append(('a', _svg(W, H, br(0, 2, 62, '%s: %s' % (la, ta), INK), 'group %s' % la)))
    if tb is not None: out.append(('b', _svg(W, H, br(1, 3, 30, '%s: %s' % (lb, tb), TEAL), 'group %s' % lb)))
    if total is not None: out.append(('tot', _svg(W, H, _text(x0 + 4 * bw + 6, y0 + bh / 2 + 8, '= %s' % total, 22, INK, 'start'), 'total %s' % total)))
    for i, c in enumerate(cells):
        if c != '':
            out.append(('c%d' % (i + 1), _svg(W, H, _text(x0 + i * bw + bw / 2, y0 + bh / 2 + 11, c, 30, TEAL), 'box %d: %s' % (i + 1, c))))
    return out


# --------------------------------------------------------------------------------------------- topics 26, 27: TRI
def TRI(top, left, right, title='Formula triangle'):
    """the formula triangle (Hebrew wp 5945-5950 «משולש ההספק... עז"ה... אני מסתיר אותו ומבצע כפל או חילוק», motion
    7004-7014 «משולש התנועה... אני פשוט מסתיר אותו»): the product on top (work / distance), its two factors at the bottom
    (time, rate / speed); cover the one you want. -> [('line', the triangle), ('vals', the three names)]"""
    W, H = 360, 250
    body = ('<path d="M 180 14 L 340 230 L 20 230 Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (LIGHT, INK) +
            '<line x1="80" y1="140" x2="280" y2="140" stroke="%s" stroke-width="2.4"/>' % INK +
            '<line x1="180" y1="140" x2="180" y2="230" stroke="%s" stroke-width="2.4"/>' % INK)
    out = [('line', _svg(W, H, body, title))]
    out.append(('vals', _svg(W, H, _text(180, 112, top, 26) + _text(120, 200, left, 24, TEAL) + _text(240, 200, right, 24, TEAL), '%s = %s × %s' % (top, left, right))))
    return out


# ------------------------------------------------------------------------------------------- items for a topic file
def items(layers_fn, name, out, w=None, col=0, fit=None):
    """[(key, svg)] -> {key: item} through the topic file's own _layers(name, out, w, col); w defaults to the 1:1 width
    (the viewBox width), capped at 1060 (left column) / 540 (right column)."""
    import re as _re
    if w is None:
        vb = [float(t) for t in _re.search(r'viewBox="([^"]+)"', out[0][1]).group(1).split()]
        w = int(min(vb[2], 1060 if col == 0 else 540))
    return layers_fn(name, out, w, col)


# =====================================================================================================================
# The post pass (2026-10-13): this module's method-visual fixes and the carry-over boxes, applied to a topic file at the
# very END of _ai_vis_tNN.py - after the visual passes AND after Codex's clarity overlay, so the overlay's cue checks
# (reviewed_cues / cue_anchors, by cue index) see exactly the plan they were made for. Visual only: no spoken text, no
# slide or paragraph changes (so no "needs re-read" flags); only cues and board items.
# =====================================================================================================================
import re as _re


def _cue_pos(ns, say, c):
    p = ns._phrase_pos(say, c)
    return 1e9 if p < 0 else p


def _insert(ns, ln, cue):
    """insert a cue into a line's cue list at its phrase's place (cues stay in speaking order)"""
    p = _cue_pos(ns, ln['say'], cue)
    assert p < 1e9, ('phrase not in the line', cue[2] if cue[0] != 'mark' else cue[3], ln['say'][:80])
    cs = ln['cues']; k = len(cs)
    for i, c in enumerate(cs):
        if _cue_pos(ns, ln['say'], c) > p: k = i; break
    cs.insert(k, cue)


def _find_show(V, name):
    for si, sl in enumerate(V['slides']):
        for li, ln in enumerate(sl['lines']):
            for ci, c in enumerate(ln['cues']):
                if c[0] == 'show' and c[1]['_name'] == name: return si, li, ci
    raise AssertionError('no show of item %s' % name)


def replace_with_figure(ns, V, old, figure, steps):
    """the item `old` (a plain typed layout) becomes a figure built in layers: its base keeps the old name and the old cue
    (so every POINT / mark on `old` still resolves), each later layer is shown at its phrase.
      figure = {key: item} from items(); steps = [(key, phrase, line offset from the old cue's line)]"""
    si, li, ci = _find_show(V, old)
    ln = V['slides'][si]['lines'][li]; c = ln['cues'][ci]
    base = figure['line']; base['_fig'] = _re.sub(r'_[^_]+$', '', base['_name']); base['_name'] = old
    ln['cues'][ci] = ('show', base, c[2])
    for key, ph, dl in steps:
        _insert(ns, V['slides'][si]['lines'][li + dl], ('show', figure[key], ph))


def add_figure(ns, V, si, li, figure, steps):
    """a new figure on slide si: steps = [(key, phrase, line index)], the base first"""
    for key, ph, l in steps:
        _insert(ns, V['slides'][si]['lines'][l], ('show', figure[key], ph))


def move_show(ns, V, name, phrase, si=None, li=None):
    """re-time an item: its show cue moves to `phrase` (in line li of slide si; default: its own line)"""
    s0, l0, c0 = _find_show(V, name)
    cue = V['slides'][s0]['lines'][l0]['cues'].pop(c0)
    ln = V['slides'][s0 if si is None else si]['lines'][l0 if li is None else li]
    _insert(ns, ln, ('show', cue[1], phrase))


def check_layers(V):
    """every layer item (over=1) must be shown right after its base or the previous layer of the same figure, on the
    same slide (studio_handwrite draws an over item at the last non-over item's y). -> [problem, ...]"""
    probs = []
    for si, sl in enumerate(V['slides']):
        shown = [c[1] for ln in sl['lines'] for c in ln['cues'] if c[0] == 'show']
        for k, it in enumerate(shown):
            if it.get('over'):
                prev = shown[k - 1] if k else None
                fam = lambda n: _re.sub(r'_[^_]+$', '', n)
                ok = prev is not None and (prev.get('over') or prev['k'] == 'vis') and (
                    fam(prev['_name']) == fam(it['_name']) or prev.get('_fig') == fam(it['_name']))
                if not ok: probs.append('slide %d: layer %s follows %s' % (si + 1, it['_name'], prev and prev['_name']))
    return probs


def carry(ns, plan):
    """the carry-over box (teacher 2026-10-13: "when you clear the slide, something that's important should stay"): on a
    slide that continues the same solution, the results the next step depends on stay on screen, in a small "So far" box
    at the top of the right column, shown with the slide's first words. plan = {vid: {slide index: [tex, ...]}}.
    It is never carried into a new method (each method starts from the givens, R30)."""
    for vid, slides in plan.items():
        V = ns.VIDEOS.get(vid)
        if not V: continue
        for si, keep in slides.items():
            sl = V['slides'][si]
            if si and sl['title'].startswith('Method') and V['slides'][si - 1]['sb'] != sl['sb']:
                raise AssertionError('%s slide %d starts a new method: no carry-over (R30)' % (vid, si + 1))
            ln = sl['lines'][0]; say = ln['say']
            m = _re.search(r'[A-Za-z]', ns.TAG.sub(lambda q: ' ' * len(q.group(0)), say))
            ph = ns._unique(say, m.start(), 2)
            shown = [c[1] for l2 in sl['lines'] for c in l2['cues'] if c[0] == 'show' and not c[1].get('over')]
            est = lambda col: sum((it['h'] if it['k'] == 'vis' else it.get('size', 36) * 1.55) + 16 for it in shown if it['_col'] == col)
            it = ns.I('keep%d' % si, 'So far: ' + ' $\\quad$ '.join(keep), size=26, col=1 if est(1) <= est(0) else 0)
            it['keep'] = 1
            ln['cues'].insert(0, ('show', it, ph))


CARRY = {
    # topic 13
    'solve-q-r26-t13-02': {1: ['(2) never', '(3) every $x$']},
    'solve-q-r26-t13-13': {1: ['$|a+b|<|a-b|$: opposite signs', '$|a+b|=4$']},
    # topic 14
    'solve-q-r26-t14-01': {1: ['$91=7\\cdot13$ ✗']},
    'solve-q-388': {1: ['$x=2^2\\cdot3\\cdot5^4$']},
    'solve-q-402': {1: ['Odd count: a perfect square']},
    'solve-q-393': {1: ['$a(b+4)=48$', '$a$ = the smaller factor']},
    'solve-q-396': {1: ['$a=12,\\ b=10$']},
    'solve-q-395': {1: ['$x$ has a $5$ and a $7$']},
    # topic 15
    'solve-q-426': {1: ['$5k+4$', '(2) ✓']},
    'solve-q-r26-t15-01': {1: ['$a-b=7(k-m)-3$']},
    'solve-q-428': {1: ['$X=2,\\ 5,\\ 8$']},
    'solve-q-430': {1: ['$15$: $60$ three-digit multiples']},
    'solve-q-431': {1: ['$b=5a,\\ c=4a$']},
    'solve-q-432': {1: ['$5(a-1)\\,a\\,(a+1)$']},
    'solve-q-435': {1: ['Yuval ✓ $\\quad$ Noga ✓'], 3: ['$x=4(2k+1)$', 'Yuval ✓ $\\quad$ Noga ✓']},
    # topic 16
    'solve-q-466': {2: ['$y<0<x$', '(1), (3) out']},
    'solve-q-472': {1: ['$b=2k$', '(1), (2) out']},
    # topic 17
    'solve-q-496': {1: ['$0<a<b<1<c<d$', '(1), (3) out']},
    'solve-q-501': {1: ['$0<p<1$, $\\ r<1$'], 2: ['$0<p<1$, $\\ r<1$', '(1), (2), (3) out']},
    # topic 18
    'solve-q-512': {1: ['$A=0$']},
    'solve-q-516': {1: ['$\\overline{BC}+46=\\overline{AAA}$']},
    'solve-q-519': {1: ['(1), (2), (3) out']},
    'solve-q-r26-t18-01': {1: ['$B=9$']},
}


def _cols(ns, name, rows, op, size=36, ring=False):
    """a typed column layout -> COLS built in layers: the two numbers and the line, then the result row, then (ring) the
    ones column boxed"""
    frame = COLS(rows[:-1] + [''], op, size=size)[0][1]
    full = COLS(rows, op, size=size, marks=[('ring', 0, 'ring')] if ring else ())
    vb = _re.search(r'viewBox="([^"]+)"', frame).group(1).split(); W, H = int(float(vb[2])), int(float(vb[3]))
    cw = size * .78; n = max(len(r) for r in rows); x_right = 40 + cw * (n + 1); gap = size * 1.22; top = size * 1.6
    y = top + gap * (len(rows) - 1) + size * .25
    body = ''.join(_text(x_right - cw * (c + .5), y, ch, size) for c, ch in enumerate(reversed(rows[-1])))
    layers = [('line', frame), ('res', _svg(W, H, body, 'the result row ' + rows[-1]))]
    if ring: layers.append(full[1])
    return items(ns._layers, name, layers, col=0)


def _fix_t18(ns):
    V = ns.VIDEOS
    plan = [('solve-q-512', 'a1', ['BA', 'DA', 'CCA'], '+', [('res', 'Now we can check', 0), ('ring', 'Step two, the ones', 1)]),
            ('solve-q-515', 'f1', ['BCA', 'BC', 'AAA'], '+', [('res', 'lining up the ones', 0)]),
            ]   # (q-513, q-516, q-518, q-519, q-r26-t18-01: their left columns are full - with the handwriting on, a
    #               built layout runs into the choices - so the typed layout stays there)
    small = {'solve-q-518': 28, 'solve-q-r26-t18-01': 28}          # a full left column: a smaller layout
    for vid, old, rows, op, steps in plan:
        if vid not in V: continue
        fig = _cols(ns, old + 'c', rows, op, size=small.get(vid, 36), ring=any(k == 'ring' for k, _, _ in steps))
        replace_with_figure(ns, V[vid], old, fig, steps)


def _fix_t17(ns):
    V = ns.VIDEOS
    # (solve-q-r26-t17-02: the question itself shows the number line, so no second line is drawn)
    if 'r26-t17-summary' in V:
        f = ns.ZL('sar', -2, 2, [('r4', [('arrow', 1.2, 1.85, '')]), ('r3', [('arrow', 0.8, 0.15, '')]),
                                 ('r2', [('arrow', -0.8, -0.15, 'odd')]), ('r1', [('arrow', -1.2, -1.85, 'odd')])], w=900)
        add_figure(ns, V['r26-t17-summary'], 5, 0, f, [('line', 'Above one', 0), ('r4', 'the arrow points right', 0),
                                                       ('r3', 'Between zero and one, left', 0), ('r2', 'Between negative one and zero', 0),
                                                       ('r1', 'Below negative one', 0)])


def _fix_t14(ns):
    V = ns.VIDEOS
    if 'solve-q-389' in V:                    # the carried 172 = 2²·43 sat between the 112 ladder's root and its layers
        move_show(ns, V['solve-q-389'], 'w1b', 'A hundred twelve is')
        sl = V['solve-q-389']['slides'][2]['lines'][0]['cues']
        k = next(i for i, c in enumerate(sl) if c[0] == 'show' and c[1]['_name'] == 'w1b'); c = sl.pop(k)
        j = next(i for i, c2 in enumerate(sl) if c2[0] == 'show' and c2[1]['_name'] == 'T112_root'); sl.insert(j, c)
    if 'r26-t14-summary' in V:                # the factor tree of 44 (camera lesson: "break it down" as a tree)
        f = ns.TREE('ft44', 44, [(2, 22), (2, 11)], col=1)
        Vs = V['r26-t14-summary']
        move_show(ns, Vs, 'f1s', 'so it divides by')
        add_figure(ns, Vs, 4, 0, f, [('root', 'Forty-four is', 0), (1, 'two times two', 0), (2, 'times eleven, so', 0)])


def _fix_t13(ns):
    V = ns.VIDEOS
    if 'r26-t13-summary' in V:                # the distance picture: |x + 6| = the distance from -6
        d = ns.DIST('hd6', -10, 1, -6, 3, base=(0,), w=760)
        add_figure(ns, V['r26-t13-summary'], 7, 1, {'line': d['line']}, [('line', 'the distance from negative six', 1)])


FIXES = {13: _fix_t13, 14: _fix_t14, 17: _fix_t17, 18: _fix_t18}


def post(ns, topic):
    """called last in _ai_vis_tNN.py: post(types.SimpleNamespace(**globals()), NN)"""
    if topic in FIXES: FIXES[topic](ns)
    carry(ns, {v: CARRY[v] for v in CARRY if v in ns.VIDEOS})
    probs = [(v, p) for v in ns.ORDER for p in check_layers(ns.VIDEOS[v])]
    if probs: raise AssertionError('figure layers out of order: %s' % probs)
