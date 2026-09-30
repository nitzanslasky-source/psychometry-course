"""Small SVG chart library for topic 52 (Charts & Tables). Every function returns an SVG string (viewBox-based,
default 900 x 520) in the studio colours; put it on a slide with vis(svg, w, h).

    vis(svg, w=820, h=None, x=None, y=None) -> slide item (h from the viewBox ratio when omitted)

Charts (all keyword arguments are optional unless shown):
    table(headers, rows, highlight=[(r, c)], hl_rows=[r], hl_cols=[c], title, note, col_w=[..], row_h, size)
        r/c are 0-based data-row / column indices. A cell may be a string, a list of lines, or ('tri', a, b, c):
        three numbers placed top-left / centre / bottom-right in one cell.
    legend_strip(items, W=1200)     a stand-alone legend row (e.g. under two charts side by side)
    scatter(cats, series, ...)      series = [dict(name, values, marker='star'|'star_o'|'dot'|'x'|'square'|'tri'|'diamond',
                                    labels=[..] (text written instead of a marker))]
    line(cats, series, ...)         series = [dict(name, values, style='solid'|'bold'|'dash'|'dot'|'dashdot', marker=None)]
    bar(cats, series, mode='grouped'|'stacked'|'overlap', orient='v'|'h', values=False, panels=False, ...)
                                    series = [dict(name, values, fill=None)]; highlight = [(series_i, cat_i)]
    continuous(xmin, xmax, xstep, curve=[(x, y)..] | bars=[(x, y)..], bar_w, strips=[(x1, x2, key)], strip_keys=
                                    {key: (fill, name)}, xfmt=callable, ...)  numeric x axis (hours, simulations...)
    range_chart(cats, series, ...)  series = [dict(name, mins, maxs, means=None)]; highlight = [(cat_i, 'min'|'max'|'mean'|'bar')]
    regions(xmin, xmax, xstep, ymin, ymax, ystep, polys=[dict(pts=[(x, y)..], label, fill, striped)], ...)
    pie(slices=[(name, percent)], highlight=[i], title)
    radial(values=[(hour, value)..], rmax=500, ring_step=100, bands=[dict(name, spans=[(h1, h2)..])], style='curve'|'points'|'bars',
           highlight_hours=[h], highlight_spans=[(band_i, h1, h2)], guide_hours=[h])
    cumulative(cats, values, ...)   line of running totals (soft fill under it)
    change(cats, values, show_line=True, ...)  points = change from the previous period; zero line in bold

Common axis options (scatter, line, bar, cumulative, change, range_chart, continuous, regions):
    ymin, ymax, ystep, ylabel, xlabel, title, legend='top'|'right'|None, ybreak=True (zig-zag "Z" on the value axis
    when it does not start at 0), yfmt=callable, W=900, H=520, marks=[...] (drawn on top, amber):
        ('pt', x, y)                 ring round a point           ('guide', x, y[, text])  dashed lines to both axes
        ('seg', x1, y1, x2, y2)      thick amber segment (slope)  ('col', x1, x2)          soft amber band across x
        ('label', x, y, text)        amber note at a point         ('brace', x, y1, y2, text) difference bracket
        ('cross', x, y)              amber X                       ('hline', y[, text])     dashed level line
    x in marks = category index (0-based, fractions allowed) for category charts, the real x for numeric charts.
Colours: ink #0F172A, teal #0F766E, amber #F5A524 (highlight), soft teal #E6F4F1, grid #D8E6E3, muted #5B6B7A.
"""
import math

INK, TEAL, AMBER, SOFT, GRID, MUTED = '#0F172A', '#0F766E', '#F5A524', '#E6F4F1', '#D8E6E3', '#5B6B7A'
AMBER_SOFT, WHITE, GREY = '#FDEBC8', '#FFFFFF', '#9AA8B5'
FONT = 'Helvetica Neue, Helvetica, Arial, sans-serif'
SERIES = [INK, TEAL, '#8A5A00', MUTED, '#2F6B9A']        # series colours (amber is kept for highlights)


def vis(svg, w=820, h=None, x=None, y=None):
    """Slide item for an SVG string; h follows the viewBox ratio when omitted."""
    if h is None:
        vb = svg.split('viewBox="', 1)[1].split('"', 1)[0].split()
        h = int(round(w * float(vb[3]) / float(vb[2])))
    d = dict(k='vis', v={'type': 'geometry', 'svg': svg}, w=w, h=h)
    if x is not None: d['x'] = x
    if y is not None: d['y'] = y
    return d


# ------------------------------------------------------------------------------------------------ primitives
def _esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _t(x, y, s, size=20, color=INK, anchor='middle', weight=400, italic=False, extra=''):
    return ('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s"%s%s>%s</text>'
            % (x, y, size, color, anchor, weight, ' font-style="italic"' if italic else '', extra, _esc(s)))


def _l(x1, y1, x2, y2, color=INK, w=2, dash=None, cap='butt'):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="%s"/>'
            % (x1, y1, x2, y2, color, w, ' stroke-dasharray="%s"' % dash if dash else '', cap))


def _r(x, y, w, h, fill, stroke='none', sw=0, rx=0, extra=''):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="%s" rx="%s"%s/>'
            % (x, y, max(0, w), max(0, h), fill, stroke, sw, rx, extra))


def _c(x, y, r, fill, stroke='none', sw=0):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fill, stroke, sw)


def _svg(W, H, body, label='Chart', defs=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s" '
            'font-family="%s"><title>%s</title>%s<rect width="%d" height="%d" fill="#fff"/>%s</svg>'
            % (W, H, _esc(label), FONT, _esc(label), '<defs>%s</defs>' % defs if defs else '', W, H, body))


STRIPES = ('<pattern id="stripe" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)">'
           '<rect width="10" height="10" fill="#fff"/><rect width="4" height="10" fill="%s"/></pattern>' % '#9FC9C1')


def _star(x, y, r, fill, stroke=INK, sw=2):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append('%.1f,%.1f' % (x + rr * math.cos(a), y + rr * math.sin(a)))
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (' '.join(pts), fill, stroke, sw)


def marker(kind, x, y, color=INK, size=11):
    """One marker shape centred at (x, y)."""
    if kind == 'star': return _star(x, y, size * 1.25, color, color, 1.5)
    if kind == 'star_o': return _star(x, y, size * 1.25, '#fff', color, 2.2)
    if kind == 'dot': return _c(x, y, size * 0.72, color)
    if kind == 'circle_o': return _c(x, y, size * 0.72, '#fff', color, 2.5)
    if kind == 'x':
        d = size * 0.72
        return _l(x - d, y - d, x + d, y + d, color, 3.5, cap='round') + _l(x - d, y + d, x + d, y - d, color, 3.5, cap='round')
    if kind == 'square': return _r(x - size * .7, y - size * .7, size * 1.4, size * 1.4, color)
    if kind == 'tri':
        d = size
        return '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (x, y - d, x - d, y + d * .75, x + d, y + d * .75, color)
    if kind == 'diamond':
        d = size
        return '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (x, y - d, x + d, y, x, y + d, x - d, y, color)
    return ''


DASH = {'solid': None, 'bold': None, 'dash': '14 9', 'dot': '3 7', 'dashdot': '16 7 3 7'}
WIDTH = {'solid': 3, 'bold': 5.5, 'dash': 3, 'dot': 3.5, 'dashdot': 3}


def _num(v):
    if isinstance(v, float) and v.is_integer(): v = int(v)
    if isinstance(v, int) and abs(v) >= 10000: return '{:,}'.format(v)
    return str(v)


# ------------------------------------------------------------------------------------------------ frame
class Frame:
    """Plot area + value mapping. cat = number of categories (categorical x) or None (numeric x)."""

    def __init__(self, W, H, xmin, xmax, ymin, ymax, left=92, right=30, top=70, bottom=70, ybreak=False):
        self.W, self.H = W, H
        self.X0, self.X1, self.Y0, self.Y1 = left, W - right, H - bottom, top
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.brk = 34 if ybreak else 0

    def x(self, v): return self.X0 + (v - self.xmin) / float(self.xmax - self.xmin) * (self.X1 - self.X0)

    def y(self, v):
        return (self.Y0 - self.brk) - (v - self.ymin) / float(self.ymax - self.ymin) * ((self.Y0 - self.brk) - self.Y1)


def _yaxis(F, ystep, yfmt=None, ylabel=None, grid=True, orient='v'):
    b = []
    v = F.ymin
    ticks = []
    while v <= F.ymax + 1e-9:
        ticks.append(round(v, 6)); v += ystep
    for v in ticks:
        yy = F.y(v)
        if grid and v != 0: b.append(_l(F.X0, yy, F.X1, yy, GRID, 1.5))
        b.append(_l(F.X0 - 7, yy, F.X0, yy, INK, 2))
        b.append(_t(F.X0 - 13, yy + 7, (yfmt or _num)(v), 20, INK, 'end'))
    if F.brk:   # zig-zag: the distance from 0 to the first value is not to scale
        b.append(_t(F.X0 - 13, F.Y0 + 7, '0', 20, INK, 'end'))
        z0, z1 = F.Y0, F.Y0 - F.brk
        m = (z0 + z1) / 2
        b.append(_l(F.X0, z0, F.X0, m + 9, INK, 2.5))
        b.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="2.5"/>'
                 % (F.X0, m + 9, F.X0 - 9, m + 4, F.X0 + 9, m - 4, F.X0, m - 9, INK))
        b.append(_l(F.X0, m - 9, F.X0, z1, INK, 2.5))
        b.append(_l(F.X0, z1, F.X0, F.Y1 - 12, INK, 2.5))
    else:
        b.append(_l(F.X0, F.Y0, F.X0, F.Y1 - 12, INK, 2.5))
    if ylabel: b.append(_t(F.X0 - 70, F.Y1 - 30, ylabel, 19, MUTED, 'start', 600))
    return ''.join(b)


def _xaxis_cats(F, cats, xlabel=None, size=20):
    b = []
    y0 = F.y(max(F.ymin, 0)) if F.ymin <= 0 else F.Y0
    b.append(_l(F.X0, y0, F.X1, y0, INK, 2.5 if F.ymin < 0 else 2.5))
    for i, c in enumerate(cats):
        xx = F.x(i)
        b.append(_l(xx, y0, xx, y0 + 7, INK, 2))
        b.append(_t(xx, F.Y0 + 30 if F.ymin >= 0 else F.Y0 + 30, c, size, INK, 'middle'))
    if F.ymin < 0: b.append(_l(F.X0, F.Y0, F.X1, F.Y0, GRID, 1.5))
    if xlabel: b.append(_t(F.X1, F.Y0 + 58, xlabel, 19, MUTED, 'end', 600))
    return ''.join(b)


def _legend(items, W, y=34, x=None, right=False, F=None, size=19):
    """items = [(kind, spec, name)]; kind 'marker' (spec = (shape, colour)), 'line' (style, colour), 'box' (fill, stroke)."""
    b = []
    def sym(kind, spec, xx, yy):
        if kind == 'marker': return marker(spec[0], xx + 14, yy, spec[1], 10)
        if kind == 'line': return _l(xx, yy, xx + 38, yy, spec[1], WIDTH[spec[0]], DASH[spec[0]])
        return _r(xx + 2, yy - 10, 28, 20, spec[0], spec[1] if len(spec) > 1 else INK, 2)
    if right:
        xx = x if x is not None else W - 235
        yy = y
        for kind, spec, name in items:
            b.append(sym(kind, spec, xx, yy))
            lines = name.split('\n')
            for k, ln in enumerate(lines):
                b.append(_t(xx + 48, yy + 7 + k * 22, ln, size, INK, 'start'))
            yy += 34 + 22 * (len(lines) - 1)
        return ''.join(b)
    # one row across the top (centred)
    widths = [48 + len(n) * size * 0.53 + 26 for _, _, n in items]
    xx = x if x is not None else (W - sum(widths)) / 2
    for (kind, spec, name), w in zip(items, widths):
        b.append(sym(kind, spec, xx, y))
        b.append(_t(xx + 48, y + 7, name, size, INK, 'start'))
        xx += w
    return ''.join(b)


def _marks(F, marks):
    b = []
    for m in marks or []:
        k = m[0]
        if k == 'pt':
            b.append(_c(F.x(m[1]), F.y(m[2]), 19, 'none', AMBER, 4))
        elif k == 'guide':
            xx, yy = F.x(m[1]), F.y(m[2])
            b.append(_l(F.X0, yy, xx, yy, AMBER, 3, '9 6'))
            b.append(_l(xx, F.Y0, xx, yy, AMBER, 3, '9 6'))
            b.append(_c(xx, yy, 19, 'none', AMBER, 4))
            if len(m) > 3: b.append(_tag(xx + 26, yy - 26, m[3]))
        elif k == 'seg':
            b.append(_l(F.x(m[1]), F.y(m[2]), F.x(m[3]), F.y(m[4]), AMBER, 9, cap='round'))
        elif k == 'col':
            b.insert(0, _r(F.x(m[1]), F.Y1 - 10, F.x(m[2]) - F.x(m[1]), F.Y0 - F.Y1 + 10, AMBER, extra=' fill-opacity="0.18"'))
        elif k == 'label':
            b.append(_tag(F.x(m[1]), F.y(m[2]), m[3], m[4] if len(m) > 4 else 'start'))
        elif k == 'brace':
            xx, y1, y2 = F.x(m[1]), F.y(m[2]), F.y(m[3])
            b.append('<path d="M %.1f %.1f h 12 V %.1f h -12" fill="none" stroke="%s" stroke-width="4"/>' % (xx, y1, y2, AMBER))
            if len(m) > 4: b.append(_tag(xx + 22, (y1 + y2) / 2 + 2, m[4]))
        elif k == 'cross':
            xx, yy = F.x(m[1]), F.y(m[2])
            b.append(_l(xx - 16, yy - 16, xx + 16, yy + 16, AMBER, 6, cap='round') + _l(xx - 16, yy + 16, xx + 16, yy - 16, AMBER, 6, cap='round'))
        elif k == 'hline':
            yy = F.y(m[1])
            b.append(_l(F.X0, yy, F.X1, yy, AMBER, 3, '9 6'))
            if len(m) > 2: b.append(_tag(F.X1 - 4, yy - 20, m[2], 'end'))
    return ''.join(b)


def _tag(x, y, text, anchor='start', size=20):
    """Amber label with a white-backed box (readable over lines)."""
    w = len(str(text)) * size * 0.56 + 18
    x0 = x if anchor == 'start' else (x - w if anchor == 'end' else x - w / 2)
    return (_r(x0, y - size * 0.95, w, size * 1.4, '#FFF7E6', AMBER, 2, 6) +
            _t(x0 + w / 2, y + size * 0.05 + 1, text, size, '#8A5A00', 'middle', 700))


def _title(W, title, sub=None):
    b = ''
    if title: b += _t(W / 2, 30, title, 22, INK, 'middle', 700)
    return b


# ------------------------------------------------------------------------------------------------ table
def table(headers, rows, highlight=(), hl_rows=(), hl_cols=(), title=None, note=None, col_w=None, row_h=None,
          size=21, head_size=None, W=900, first_bold=True, dim=()):
    """headers: list of column titles ('\\n' splits lines). rows: list of rows. dim = cells shown in muted grey."""
    ncol = len(headers)
    col_w = col_w or [W / ncol] * ncol
    scale = W / float(sum(col_w)); col_w = [c * scale for c in col_w]
    head_size = head_size or size
    hl = set(tuple(h) for h in highlight)
    hlines = max(len(str(h).split('\n')) for h in headers)
    hh = 18 + hlines * head_size * 1.22
    def lines_of(c):
        if isinstance(c, (list, tuple)) and (not c or c[0] != 'tri'): return [str(x) for x in c]
        return str(c).split('\n')
    rh = row_h or max(52, max((len(lines_of(c)) if not (isinstance(c, tuple) and c and c[0] == 'tri') else 3)
                              for r in rows for c in r) * size * 1.25 + 16)
    top = 50 if title else 4
    H = top + hh + rh * len(rows) + (44 if note else 6)
    b = [_title(W, title)] if title else []
    xs = [sum(col_w[:k]) for k in range(ncol)]
    # header
    for k, h in enumerate(headers):
        on = k in hl_cols
        b.append(_r(xs[k] + 1, top, col_w[k] - 2, hh, AMBER_SOFT if on else SOFT, TEAL if not on else AMBER, 2))
        ls = str(h).split('\n')
        for j, ln in enumerate(ls):
            b.append(_t(xs[k] + col_w[k] / 2, top + hh / 2 + (j - (len(ls) - 1) / 2.0) * head_size * 1.18 + head_size * .36,
                        ln, head_size, INK, 'middle', 700))
    for r, row in enumerate(rows):
        y = top + hh + r * rh
        for k, c in enumerate(row):
            on = (r, k) in hl or r in hl_rows or k in hl_cols
            b.append(_r(xs[k] + 1, y, col_w[k] - 2, rh, AMBER_SOFT if on else '#fff', GRID, 2))
            col = MUTED if (r, k) in set(tuple(d) for d in dim) else INK
            wt = 700 if (first_bold and k == 0) or on else 400
            if isinstance(c, tuple) and c and c[0] == 'tri':
                a, m_, z = c[1], c[2], c[3]
                b.append(_t(xs[k] + 14, y + size + 6, a, size, col, 'start', wt))
                b.append(_t(xs[k] + col_w[k] / 2, y + rh / 2 + size * .36, m_, size, col, 'middle', wt))
                b.append(_t(xs[k] + col_w[k] - 14, y + rh - 12, z, size, col, 'end', wt))
                continue
            ls = lines_of(c)
            for j, ln in enumerate(ls):
                b.append(_t(xs[k] + col_w[k] / 2, y + rh / 2 + (j - (len(ls) - 1) / 2.0) * size * 1.2 + size * .36, ln, size, col, 'middle', wt))
        # amber outline on highlighted cells (drawn last so it sits on top)
    for (r, k) in hl:
        y = top + hh + r * rh
        b.append(_r(xs[k] + 2, y + 1, col_w[k] - 4, rh - 2, 'none', AMBER, 4))
    for r in hl_rows:
        y = top + hh + r * rh
        b.append(_r(3, y + 1, W - 6, rh - 2, 'none', AMBER, 4))
    for k in hl_cols:
        b.append(_r(xs[k] + 2, top + 1, col_w[k] - 4, hh + rh * len(rows) - 2, 'none', AMBER, 4))
    if note: b.append(_t(4, H - 14, note, 18, MUTED, 'start', 400, True))
    return _svg(int(W), int(math.ceil(H)), ''.join(b), title or 'Table')


# ------------------------------------------------------------------------------------------------ category charts
def _cat_frame(cats, ymin, ymax, W, H, legend, ybreak, left=92, bottom=70):
    right = 250 if legend == 'right' else 30
    top = 88 if legend == 'top' else 70
    return Frame(W, H, -0.5, len(cats) - 0.5, ymin, ymax, left=left, right=right, top=top, bottom=bottom, ybreak=ybreak)


def scatter(cats, series, ymin=0, ymax=100, ystep=10, ylabel=None, xlabel=None, title=None, legend='right',
            ybreak=None, yfmt=None, marks=(), highlight=(), W=900, H=520, y2=None):
    """Points on axes. highlight = [(series_i, cat_i)] -> amber marker. y2 = dict(ymin, ymax, ystep, label) right axis."""
    ybreak = (ymin > 0) if ybreak is None else ybreak
    F = _cat_frame(cats, ymin, ymax, W, H, legend, ybreak)
    if y2: F.X1 -= 60
    b = [_title(W, title), _yaxis(F, ystep, yfmt, ylabel), _xaxis_cats(F, cats, xlabel)]
    hl = set(tuple(h) for h in highlight)
    for si, s in enumerate(series):
        for ci, v in enumerate(s['values']):
            if v is None or v < ymin: continue
            xx, yy = F.x(ci), F.y(v)
            col = s.get('color', INK)
            if (si, ci) in hl: b.append(_c(xx, yy, 22, AMBER_SOFT, AMBER, 3))
            if s.get('labels'):
                b.append(_c(xx, yy, 17, '#fff', col, 2.5))
                b.append(_t(xx, yy + 7, s['labels'][ci], 19, col, 'middle', 700))
            else:
                b.append(marker(s.get('marker', 'dot'), xx, yy, AMBER if (si, ci) in hl and s.get('marker') == 'star' else col, 11))
    if y2:
        F2 = Frame(W, H, 0, 1, y2['ymin'], y2['ymax'], top=F.Y1, bottom=H - F.Y0)
        v = y2['ymin']
        while v <= y2['ymax'] + 1e-9:
            yy = F2.y(v); b.append(_l(F.X1, yy, F.X1 + 7, yy, INK, 2)); b.append(_t(F.X1 + 12, yy + 7, _num(v), 20, INK, 'start'))
            v += y2['ystep']
        b.append(_l(F.X1, F.Y0, F.X1, F.Y1 - 12, INK, 2.5))
        if y2.get('label'): b.append(_t(F.X1 + 60, F.Y1 - 30, y2['label'], 19, MUTED, 'end', 600))
    if legend:
        items = [('marker', (s.get('marker', 'dot'), s.get('color', INK)), s['name']) for s in series if not s.get('labels')]
        b.append(_legend(items, W, y=F.Y1 + 10 if legend == 'right' else 60, right=(legend == 'right')))
    b.append(_marks(F, marks))
    return _svg(W, H, ''.join(b), title or 'Scatter chart')


def line(cats, series, ymin=0, ymax=100, ystep=10, ylabel=None, xlabel=None, title=None, legend='right',
         ybreak=None, yfmt=None, marks=(), highlight=(), W=900, H=520, points=True, fill=None):
    """Line graph. highlight = [(series_i, seg_i)] -> amber segment from cat seg_i to seg_i+1.
    points=False hides the markers (the line alone)."""
    ybreak = (ymin > 0) if ybreak is None else ybreak
    F = _cat_frame(cats, ymin, ymax, W, H, legend, ybreak)
    b = [_title(W, title), _yaxis(F, ystep, yfmt, ylabel), _xaxis_cats(F, cats, xlabel)]
    hl = set(tuple(h) for h in highlight)
    for si, s in enumerate(series):
        pts = [(F.x(i), F.y(v)) for i, v in enumerate(s['values']) if v is not None]
        col = s.get('color', INK)
        st = s.get('style', 'solid')
        if fill:
            b.append('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % p for p in [(pts[0][0], F.y(max(F.ymin, 0)))] + pts +
                                                                        [(pts[-1][0], F.y(max(F.ymin, 0)))]), fill))
        b.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s stroke-linejoin="round" stroke-linecap="round"/>'
                 % (' '.join('%.1f,%.1f' % p for p in pts), col, WIDTH[st], ' stroke-dasharray="%s"' % DASH[st] if DASH[st] else ''))
        for (s_, g) in hl:
            if s_ == si: b.append(_l(pts[g][0], pts[g][1], pts[g + 1][0], pts[g + 1][1], AMBER, 9, cap='round'))
        mk = s.get('marker', 'dot' if points else None)
        if points and mk:
            for p in pts: b.append(marker(mk, p[0], p[1], col, 9))
    if legend:
        items = [('line', (s.get('style', 'solid'), s.get('color', INK)), s['name']) for s in series]
        b.append(_legend(items, W, y=F.Y1 + 10 if legend == 'right' else 60, right=(legend == 'right')))
    b.append(_marks(F, marks))
    return _svg(W, H, ''.join(b), title or 'Line graph')


def bar(cats, series, mode='grouped', orient='v', ymin=0, ymax=100, ystep=10, ylabel=None, xlabel=None, title=None,
        legend='right', values=False, highlight=(), marks=(), W=900, H=520, panels=False, yfmt=None, bar_frac=0.72):
    """Bar chart. mode: grouped (side by side) · stacked (one on top of the other) · overlap (bar inside bar:
    series 0 is the wide back bar, later series narrower in front). orient='h' -> horizontal bars;
    panels=True with orient='h' -> one panel per series (each with its own value axis)."""
    hl = set(tuple(h) for h in highlight)
    fills = [s.get('fill') or ['#fff', INK, GREY, SOFT, TEAL][i % 5] for i, s in enumerate(series)]
    if orient == 'h':
        return _hbar(cats, series, fills, ymin, ymax, ystep, xlabel, title, legend, values, hl, W, H, panels)
    F = _cat_frame(cats, ymin, ymax, W, H, legend, False)
    b = [_title(W, title), _yaxis(F, ystep, yfmt, ylabel)]
    slot = (F.X1 - F.X0) / len(cats) * bar_frac
    n = len(series)
    for ci in range(len(cats)):
        cx = F.x(ci)
        base = ymin
        for si, s in enumerate(series):
            v = s['values'][ci]
            if v is None: continue
            if mode == 'grouped':
                bw = slot / n; x0 = cx - slot / 2 + si * bw; y0, y1 = F.y(ymin), F.y(v)
            elif mode == 'stacked':
                bw = slot * 0.62; x0 = cx - bw / 2; y0, y1 = F.y(base), F.y(base + v); base += v
            else:   # overlap
                bw = slot * (0.78 if si == 0 else 0.42); x0 = cx - bw / 2; y0, y1 = F.y(ymin), F.y(v)
            on = (si, ci) in hl
            b.append(_r(x0, y1, bw, y0 - y1, fills[si], AMBER if on else INK, 5 if on else 2))
            if values:
                lab = _num(v)
                if mode == 'stacked': b.append(_t(cx, (y0 + y1) / 2 + 7, lab, 18, '#fff' if fills[si] in (INK, TEAL) else INK, 'middle', 700))
                else: b.append(_t(x0 + bw / 2, y1 - 8, lab, 17, INK, 'middle', 600))
    b.append(_xaxis_cats(F, cats, xlabel))
    if legend:
        items = [('box', (fills[i], INK), s['name']) for i, s in enumerate(series)]
        b.append(_legend(items, W, y=F.Y1 + 10 if legend == 'right' else 60, right=(legend == 'right')))
    b.append(_marks(F, marks))
    return _svg(W, H, ''.join(b), title or 'Bar chart')


def _hbar(cats, series, fills, vmin, vmax, vstep, vlabel, title, legend, values, hl, W, H, panels):
    b = [_title(W, title)]
    left = 160
    top = 60 if title else 30
    bottom = 60
    groups = [[i] for i in range(len(series))] if panels else [list(range(len(series)))]
    gap = 40
    pw = (W - left - 20 - gap * (len(groups) - 1)) / len(groups)
    rowh = (H - top - bottom - 40) / len(cats)
    for gi, g in enumerate(groups):
        X0 = left + gi * (pw + gap); X1 = X0 + pw
        Y0 = top + 40 + rowh * len(cats)
        xv = lambda v: X0 + (v - vmin) / float(vmax - vmin) * (X1 - X0)
        if panels: b.append(_t((X0 + X1) / 2, top + 22, series[g[0]]['name'], 21, INK, 'middle', 700))
        v = vmin
        while v <= vmax + 1e-9:
            b.append(_l(xv(v), top + 36, xv(v), Y0, GRID, 1.5))
            b.append(_t(xv(v), Y0 + 28, _num(v), 18, INK, 'middle'))
            v += vstep
        b.append(_l(X0, top + 36, X0, Y0, INK, 2.5)); b.append(_l(X0, Y0, X1, Y0, INK, 2.5))
        bh = rowh * 0.62 / len(g)
        for ci, c in enumerate(cats):
            yc = top + 40 + rowh * (ci + 0.5)
            if gi == 0: b.append(_t(left - 14, yc + 7, c, 20, INK, 'end', 600))
            for k, si in enumerate(g):
                val = series[si]['values'][ci]
                y0 = yc - rowh * 0.31 + k * bh
                on = (si, ci) in hl
                b.append(_r(X0, y0, xv(val) - X0, bh, fills[si] if not panels else SOFT, AMBER if on else INK, 5 if on else 2))
                if values or on: b.append(_t(xv(val) + 8, y0 + bh / 2 + 7, _num(val), 18, '#8A5A00' if on else INK, 'start', 700))
        if vlabel: b.append(_t(X1, Y0 + 52, vlabel, 18, MUTED, 'end', 600))
    if legend and not panels:
        items = [('box', (fills[i], INK), s['name']) for i, s in enumerate(series)]
        b.append(_legend(items, W, y=top + 14))
    return _svg(W, H, ''.join(b), title or 'Horizontal bar chart')


def cumulative(cats, values, ymin=0, ymax=100, ystep=10, ylabel=None, xlabel=None, title=None, marks=(), highlight=(),
               W=900, H=520, name='Cumulative total'):
    """Cumulative graph: every point = the running total up to and including that period."""
    return line(cats, [dict(name=name, values=values, style='bold', color=TEAL, marker='dot')], ymin, ymax, ystep,
                ylabel, xlabel, title, None, False, None, marks, highlight, W, H, True, fill=SOFT)


def change(cats, values, ymin=-20, ymax=20, ystep=5, ylabel=None, xlabel=None, title=None, show_line=True, marks=(),
           highlight=(), W=900, H=520, point_labels=True):
    """Change graph: each point = the change compared with the previous period (not the value itself).
    highlight = [cat_i] -> amber point."""
    F = _cat_frame(cats, ymin, ymax, W, H, None, False)
    fmt = lambda v: ('+' if v > 0 else ('−' if v < 0 else '')) + _num(abs(v))
    b = [_title(W, title), _yaxis(F, ystep, fmt, ylabel)]
    b.append(_xaxis_cats(F, cats, xlabel))
    b.append(_l(F.X0, F.y(0), F.X1, F.y(0), INK, 3))
    pts = [(F.x(i), F.y(v)) for i, v in enumerate(values)]
    if show_line:
        b.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
                 % (' '.join('%.1f,%.1f' % p for p in pts), GREY))
    for i, (p, v) in enumerate(zip(pts, values)):
        on = i in highlight
        if on: b.append(_c(p[0], p[1], 20, AMBER_SOFT, AMBER, 3))
        b.append(_c(p[0], p[1], 8, AMBER if on else TEAL))
        if point_labels: b.append(_t(p[0], p[1] - 16 if v >= 0 else p[1] + 32, fmt(v), 18, '#8A5A00' if on else TEAL, 'middle', 700))
    b.append(_marks(F, marks))
    return _svg(W, H, ''.join(b), title or 'Change graph')


# ------------------------------------------------------------------------------------------------ numeric-x charts
def smooth(pts, step=0.25):
    """Monotone (Fritsch-Carlson) interpolation through pts = [(x, y)], sampled every `step` -> [(x, y)]."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; n = len(pts)
    d = [(ys[k + 1] - ys[k]) / float(xs[k + 1] - xs[k]) for k in range(n - 1)]
    m = [d[0]] + [0 if d[k - 1] * d[k] <= 0 else (d[k - 1] + d[k]) / 2 for k in range(1, n - 1)] + [d[-1]]
    for k in range(n - 1):
        if d[k] == 0: m[k] = m[k + 1] = 0; continue
        a, bb = m[k] / d[k], m[k + 1] / d[k]
        s = a * a + bb * bb
        if s > 9:
            t = 3 / math.sqrt(s); m[k] = t * a * d[k]; m[k + 1] = t * bb * d[k]
    out = []
    x = xs[0]
    k = 0
    while x <= xs[-1] + 1e-9:
        while k < n - 2 and x > xs[k + 1]: k += 1
        h = xs[k + 1] - xs[k]; t = (x - xs[k]) / h
        h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
        out.append((round(x, 4), h00 * ys[k] + h10 * h * m[k] + h01 * ys[k + 1] + h11 * h * m[k + 1]))
        x += step
    return out


def continuous(xmin, xmax, xstep, ymin=0, ymax=100, ystep=10, curve=None, bars=None, bar_w=1.0, ylabel=None, xlabel=None,
               title=None, xfmt=None, strips=None, strip_keys=None, marks=(), highlight_bars=(), W=900, H=520, yfmt=None,
               curve_color=TEAL, bar_fill=SOFT, left=92, ybreak=False, curves=None):
    """Numeric x axis. curve = [(x, y)] drawn as one continuous line; bars = [(x, y)] bars of width bar_w centred on x
    (highlight_bars = [x] -> amber bar). strips = [(x1, x2, key)] coloured rectangles under the axis (strip_keys:
    key -> (fill, name) for the legend)."""
    extra = 58 if strips else 0
    F = Frame(W, H, xmin, xmax, ymin, ymax, left=left, right=34, top=70, bottom=70 + extra, ybreak=ybreak)
    b = [_title(W, title), _yaxis(F, ystep, yfmt, ylabel)]
    for x, v in bars or []:
        x0, x1 = max(F.X0 + 2, F.x(x - bar_w / 2.0)), min(F.X1, F.x(x + bar_w / 2.0))
        on = x in highlight_bars
        thin = (x1 - x0) < 8
        b.append(_r(x0, F.y(v), x1 - x0, F.y(ymin) - F.y(v), AMBER if on else (TEAL if thin else bar_fill),
                    'none' if thin else (AMBER if on else INK), 0 if thin else (4 if on else 2)))
    for cv in curves or []:   # extra curves: dict(pts, color, width, dash)
        b.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>'
                 % (' '.join('%.1f,%.1f' % (F.x(x), F.y(y)) for x, y in cv['pts']), cv.get('color', GREY), cv.get('width', 4),
                    ' stroke-dasharray="%s"' % cv['dash'] if cv.get('dash') else ''))
    if curve:
        b.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="4" stroke-linejoin="round"/>'
                 % (' '.join('%.1f,%.1f' % (F.x(x), F.y(y)) for x, y in curve), curve_color))
    # x axis
    b.append(_l(F.X0, F.Y0, F.X1, F.Y0, INK, 2.5))
    v = xmin
    while v <= xmax + 1e-9:
        b.append(_l(F.x(v), F.Y0, F.x(v), F.Y0 + 7, INK, 2))
        b.append(_t(F.x(v), F.Y0 + 30, (xfmt or _num)(v), 19, INK, 'middle'))
        v += xstep
    if xlabel: b.append(_t(F.X1, F.Y0 + 56 + extra, xlabel, 18, MUTED, 'end', 600))
    if strips:
        sy = F.Y0 + 44
        for x1, x2, key in strips:
            b.append(_r(F.x(x1), sy, F.x(x2) - F.x(x1), 22, strip_keys[key][0], INK, 1.2))
        xx = F.X0
        for key, (fill, name) in strip_keys.items():
            b.append(_r(xx, sy + 34, 26, 18, fill, INK, 1.2)); b.append(_t(xx + 34, sy + 50, name, 18, INK, 'start'))
            xx += 60 + len(name) * 10
    b.append(_marks(F, marks))
    return _svg(W, H, ''.join(b), title or 'Continuous line graph')


def range_chart(cats, series, ymin=0, ymax=10, ystep=1, ylabel=None, xlabel=None, title=None, legend=None, ybreak=None,
                yfmt=None, highlight=(), marks=(), W=900, H=520, labels=False):
    """Min-max range chart: a bar from min to max per category, a bold line at the mean.
    series = [dict(name, mins, maxs, means=None, fill)]; several series -> bars side by side.
    highlight = [(cat_i, 'min'|'max'|'mean'|'bar')] (series 0) or [(cat_i, part, series_i)]."""
    ybreak = (ymin > 0) if ybreak is None else ybreak
    F = _cat_frame(cats, ymin, ymax, W, H, legend, ybreak)
    b = [_title(W, title), _yaxis(F, ystep, yfmt, ylabel), _xaxis_cats(F, cats, xlabel)]
    n = len(series)
    slot = (F.X1 - F.X0) / len(cats) * (0.5 if n == 1 else 0.8)
    bw = slot / n
    hls = [(h[0], h[1], h[2] if len(h) > 2 else 0) for h in highlight]
    fills = [s.get('fill') or [SOFT, '#CFE3F5', '#F3E1C2'][i % 3] for i, s in enumerate(series)]
    for si, s in enumerate(series):
        for ci in range(len(cats)):
            lo, hi = s['mins'][ci], s['maxs'][ci]
            x0 = F.x(ci) - slot / 2 + si * bw
            parts = [p for (c, p, k) in hls if c == ci and k == si]
            b.append(_r(x0, F.y(hi), bw, F.y(lo) - F.y(hi), fills[si], AMBER if 'bar' in parts else INK, 4 if 'bar' in parts else 2))
            if s.get('means'):
                mv = s['means'][ci]
                b.append(_l(x0 - 3, F.y(mv), x0 + bw + 3, F.y(mv), AMBER if 'mean' in parts else INK, 7 if 'mean' in parts else 5))
            for p, val in (('min', lo), ('max', hi)):
                if p in parts:
                    b.append(_l(x0 - 6, F.y(val), x0 + bw + 6, F.y(val), AMBER, 7, cap='round'))
                    b.append(_tag(x0 + bw + 12, F.y(val) + 8, _num(val)))
            if 'mean' in parts and s.get('means'):
                b.append(_tag(x0 + bw + 12, F.y(s['means'][ci]) + 8, _num(s['means'][ci])))
            if labels and s.get('means'):
                pass
    if legend:
        items = [('box', (fills[i], INK), s['name']) for i, s in enumerate(series)]
        b.append(_legend(items, W, y=F.Y1 + 10 if legend == 'right' else 60, right=(legend == 'right')))
    b.append(_marks(F, marks))
    return _svg(W, H, ''.join(b), title or 'Range chart')


def regions(xmin, xmax, xstep, ymin, ymax, ystep, polys, xlabel=None, ylabel=None, title=None, marks=(), highlight=(),
            W=900, H=520, xfmt=None, yfmt=None):
    """Regions on axes: each polygon is an area with its value written inside (e.g. a price).
    polys = [dict(pts=[(x, y)..], label, at=(x, y) label position, fill, striped=False)]; highlight = [poly_i]."""
    F = Frame(W, H, xmin, xmax, ymin, ymax, left=92, right=34, top=70, bottom=70)
    b = [_title(W, title)]
    for i, p in enumerate(polys):
        fill = 'url(#stripe)' if p.get('striped') else p.get('fill', SOFT)
        on = i in highlight
        b.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
                 % (' '.join('%.1f,%.1f' % (F.x(x), F.y(y)) for x, y in p['pts']), fill, AMBER if on else INK, 5 if on else 1.5))
    for i, p in enumerate(polys):
        ax, ay = p['at']
        b.append(_c(F.x(ax), F.y(ay), 21, '#fff', AMBER if i in highlight else INK, 2.5 if i not in highlight else 4))
        b.append(_t(F.x(ax), F.y(ay) + 8, p['label'], 22, INK, 'middle', 700))
    b.append(_yaxis(F, ystep, yfmt, ylabel, grid=False))
    b.append(_l(F.X0, F.Y0, F.X1, F.Y0, INK, 2.5))
    v = xmin
    while v <= xmax + 1e-9:
        b.append(_l(F.x(v), F.Y0, F.x(v), F.Y0 + 7, INK, 2)); b.append(_t(F.x(v), F.Y0 + 30, (xfmt or _num)(v), 19, INK, 'middle'))
        v += xstep
    if xlabel: b.append(_t(F.X1, F.Y0 + 58, xlabel, 18, MUTED, 'end', 600))
    b.append(_marks(F, marks))
    return _svg(W, H, ''.join(b), title or 'Regions chart', defs=STRIPES)


# ------------------------------------------------------------------------------------------------ circles
def pie(slices, highlight=(), title=None, W=900, H=520, colors=None):
    """Classic pie: slices = [(name, percent)], % labels on the slices, legend on the right."""
    cx, cy, R = 300, H / 2 + (12 if title else 0), 200
    cols = colors or [TEAL, '#6FB3A8', SOFT, GREY, '#D7DEE5', INK]
    b = [_title(W, title)]
    a = -math.pi / 2
    for i, (name, pct) in enumerate(slices):
        a2 = a + 2 * math.pi * pct / 100.0
        big = 1 if a2 - a > math.pi else 0
        on = i in highlight
        off = 14 if on else 0
        mid = (a + a2) / 2
        ox, oy = off * math.cos(mid), off * math.sin(mid)
        b.append('<path d="M %.1f %.1f L %.1f %.1f A %d %d 0 %d 1 %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="%s"/>'
                 % (cx + ox, cy + oy, cx + ox + R * math.cos(a), cy + oy + R * math.sin(a), R, R, big,
                    cx + ox + R * math.cos(a2), cy + oy + R * math.sin(a2), AMBER if on else cols[i % len(cols)], '#fff', 3))
        lx, ly = cx + ox + R * 0.66 * math.cos(mid), cy + oy + R * 0.66 * math.sin(mid)
        dark = cols[i % len(cols)] in (TEAL, INK) and not on
        b.append(_t(lx, ly + 8, '%s%%' % _num(pct), 22, '#fff' if dark else INK, 'middle', 700))
        a = a2
    b.append(_legend([('box', (AMBER if i in highlight else cols[i % len(cols)], INK), n) for i, (n, _) in enumerate(slices)],
                     W, y=cy - 17 * len(slices), x=560, right=True))
    return _svg(W, H, ''.join(b), title or 'Pie chart')


def radial(values, rmax=500, ring_step=100, bands=(), style='curve', highlight_hours=(), highlight_spans=(),
           guide_hours=(), title=None, W=None, H=None, hours=24, band_w=18, label_every=1, show_band_names=True, R=230):
    """Circle chart on a 24-hour clock: the distance from the centre = the value (the circles are the value lines),
    hour 0 at the top, clockwise. bands = [dict(name, spans=[(h1, h2)])] from the OUTSIDE in: a dark arc = the hours
    in which that band applies. style: 'curve' (continuous line), 'points' (a dot each hour), 'bars' (a wedge each hour)."""
    Rout0 = R + 12 + len(bands) * (band_w + 5)
    margin = Rout0 + 52
    names_w = 250 if (show_band_names and bands) else 0
    W = W or int(2 * margin + names_w)
    H = H or int(2 * margin + (34 if title else 0))
    cx, cy = margin, margin + (34 if title else 0)
    r0 = 0
    rv = lambda v: r0 + (R - r0) * v / float(rmax)
    ang = lambda h: -math.pi / 2 + 2 * math.pi * h / float(hours)
    P = lambda h, r: (cx + r * math.cos(ang(h)), cy + r * math.sin(ang(h)))
    b = [_title(W, title)]
    # value circles
    v = ring_step
    while v <= rmax + 1e-9:
        b.append(_c(cx, cy, rv(v), 'none', GRID if v < rmax else MUTED, 1.5))
        v += ring_step
    for h in range(hours):
        x1, y1 = P(h, 0); x2, y2 = P(h, R)
        b.append(_l(x1, y1, x2, y2, GRID, 1))
    v = ring_step
    while v <= rmax + 1e-9:
        x, y = P(0, rv(v))
        b.append(_t(x + 6, y + 19, _num(v), 17, MUTED, 'start', 700))
        v += ring_step
    # bands (outside the value circle)
    names = []
    for bi, band in enumerate(bands):
        rin = R + 12 + (len(bands) - 1 - bi) * (band_w + 5)
        rout = rin + band_w
        b.append(_c(cx, cy, (rin + rout) / 2.0, 'none', '#EEF2F5', band_w))
        for h1, h2 in band['spans']:
            b.append(_arc(cx, cy, rin, rout, ang(h1), ang(h2), '#6B7785'))
            for (k, a, c) in highlight_spans:     # amber only on the highlighted hours
                if k == bi and max(h1, a) < min(h2, c):
                    b.append(_arc(cx, cy, rin - 2, rout + 2, ang(max(h1, a)), ang(min(h2, c)), AMBER))
        names.append((band['name'], (rin + rout) / 2.0))
    Rout = R + 12 + len(bands) * (band_w + 5)
    for h in range(0, hours, label_every):
        x, y = P(h, Rout + 28)
        on = h in highlight_hours or h in guide_hours
        b.append(_t(x, y + 7, '%d:00' % h, 19, '#8A5A00' if on else INK, 'middle', 700 if on else 400))
    # data
    pts = values
    if style == 'curve':
        sm = smooth(pts, 0.25)
        b.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/>'
                 % (' '.join('%.1f,%.1f' % P(h, rv(val)) for h, val in sm if h < hours), TEAL))
    elif style == 'points':
        for h, val in pts:
            if h < hours: x, y = P(h, rv(val)); b.append(_c(x, y, 6, TEAL))
    elif style == 'bars':
        for h, val in pts:
            if h < hours: b.append(_arc(cx, cy, 0.01, rv(val), ang(h - 0.38), ang(h + 0.38), '#9FC9C1', INK, 1))
    for h in guide_hours:
        val = dict(pts)[h]
        x0, y0 = P(h, 0); x1, y1 = P(h, rv(val))
        b.append(_l(x0, y0, x1, y1, AMBER, 3, '8 6'))
        b.append(_c(x1, y1, 13, AMBER_SOFT, AMBER, 3))
        b.append(_c(x1, y1, 5, TEAL))
    for h in highlight_hours:
        if h in guide_hours: continue
        val = dict(pts)[h]; x1, y1 = P(h, rv(val)); b.append(_c(x1, y1, 13, 'none', AMBER, 4))
    if show_band_names and names:
        # leader lines from each band (at about 4 o'clock of the dial, an empty angle) to its name on the right
        lx = cx + Rout + 60
        for k, (name, rr) in enumerate(names):
            hx, hy = P(4.3 + 0.55 * k, rr)   # between the hour labels
            ty = cy + 100 + k * 34
            b.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="1.5"/>'
                     % (hx, hy, lx - 16, ty - 6, lx - 4, ty - 6, MUTED))
            b.append(_t(lx, ty, name, 19, INK, 'start', 600))
        b.append(_t(lx, cy + 60, 'Rings, outside to inside:', 17, MUTED, 'start', 600))
    return _svg(W, H, ''.join(b), title or 'Circle chart')


def _arc(cx, cy, rin, rout, a1, a2, fill, stroke='none', sw=0):
    big = 1 if a2 - a1 > math.pi else 0
    p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
    o1, o2, i2, i1 = p(rout, a1), p(rout, a2), p(rin, a2), p(rin, a1)
    return ('<path d="M %.1f %.1f A %.1f %.1f 0 %d 1 %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (o1[0], o1[1], rout, rout, big, o2[0], o2[1], i2[0], i2[1], rin, rin, big, i1[0], i1[1], fill, stroke, sw))


def legend_strip(items, W=1200, H=46, size=21):
    """A stand-alone legend row (for two charts side by side). items = [(kind, spec, name)] as in _legend:
    ('marker', (shape, colour), name) · ('line', (style, colour), name) · ('box', (fill, stroke), name)."""
    return _svg(W, H, _legend(items, W, y=H / 2, size=size), 'Legend')
