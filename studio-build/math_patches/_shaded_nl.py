"""Shaded number-line figures for inequality answers (2026-10-07 "shaded number lines", teacher idea:
show the solution range coloured in on a number line - x² > k as two outward rays, x² < k as a segment, systems as
the overlap). Same look as the topic-13 'within 4 of 2' figure (t13.py NL_SVG): ink #203344, teal #087f83, band #d5f1ed.

Not a patch itself (math_api only loads t*.py); t12/t13/t17 import it with load().

    fig(lo, hi, ticks, segs, signs=(), bars=(), title='', center=None, cap=None) -> svg string (640 wide, cropped to its content)
        lo, hi  : the values at the two ends of the drawn line (rays run to the arrows)
        ticks   : [(value, label)] - a tick + label for each key number (label None = tick only)
        segs    : [(a, b, a_closed, b_closed)] - shaded on the line; a=None: ray to the left, b=None: ray to the right
                  a 5th element 'dark' = the overlap of a system (darker teal)
        signs   : [(value, '+' / '−')] - sign-table signs written above the parts
        bars    : [(a, b, a_closed, b_closed, label)] - a system's single ranges, as thin bars above the line
    two(fig_a, fig_b) -> two lines stacked in one svg (dicts of fig() arguments)
    add(M, vid, n, after_say, svg, label, say, w) -> the figure appears right after a spoken line, plus one spoken line
    recorded(vid)     -> True if a take of vid was recorded before CUTOFF (then the video must stay as recorded)
"""
import glob as _glob, html as _html, os as _os, re as _re

INK, TEAL, BAND, DARK = '#203344', '#087f83', '#d5f1ed', '#5bb8ae'
FONT = 'font-family="DejaVu Sans,Arial,sans-serif"'
L, R, Y = 40, 600, 92          # line ends, axis height
CUTOFF = '2026-10-07T14-44-12'  # UTC; takes recorded before this keep the old video (set when this change was built)


def recorded(vid):
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


def _m(n):
    return ('−' + _fmt(-n)) if n < 0 else _fmt(n)


def _fmt(n):
    return str(int(n)) if float(n).is_integer() else str(n)


def _body(lo, hi, ticks, segs, signs=(), bars=(), dy=0, center=None, cap=None):
    X = lambda v: L + 30 + (v - lo) / float(hi - lo) * (R - L - 60)
    y = Y + dy
    s = []
    # the line; an end with a ray gets a teal arrow instead of the dark one
    left_ray = any(g[0] is None for g in segs)
    right_ray = any(g[1] is None for g in segs)
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/>' % (L - 10, y, R + 10, y, INK))
    s.append('<path d="M %d %d l 12 -7 l 0 14 Z" fill="%s"/>' % (L - 14, y, TEAL if left_ray else INK))
    s.append('<path d="M %d %d l -12 -7 l 0 14 Z" fill="%s"/>' % (R + 14, y, TEAL if right_ray else INK))
    for g in segs:
        a, b, ca, cb = g[:4]
        fill = DARK if len(g) > 4 and g[4] == 'dark' else BAND
        x1 = X(a) if a is not None else L - 2
        x2 = X(b) if b is not None else R + 2
        s.append('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (x1, y - 7, x2 - x1, fill, TEAL))
    for k, (a, b, ca, cb, lab) in enumerate(bars):
        yy = y - 30 - 22 * k
        x1 = X(a) if a is not None else L
        x2 = X(b) if b is not None else R
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (x1, yy, x2, yy, TEAL))
        if a is None: s.append('<path d="M %.1f %d l 11 -6 l 0 12 Z" fill="%s"/>' % (x1 - 4, yy, TEAL))
        if b is None: s.append('<path d="M %.1f %d l -11 -6 l 0 12 Z" fill="%s"/>' % (x2 + 4, yy, TEAL))
        for v, c in ((a, ca), (b, cb)):
            if v is not None:
                s.append('<circle cx="%.1f" cy="%d" r="5" fill="%s" stroke="%s" stroke-width="2.5"/>' % (X(v), yy, TEAL if c else '#ffffff', TEAL))
        tx = (x1 + x2) / 2
        s.append('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="22" font-weight="bold">%s</text>' % (tx, yy - 9, TEAL, FONT, _html.escape(lab)))
    for v, lab in ticks:
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (X(v), y - 11, X(v), y + 11, INK))
        if lab is not None:
            s.append('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="25" font-weight="bold">%s</text>' % (X(v), y + 40, INK, FONT, lab))
    for g in segs:   # endpoint circles on top of the ticks
        a, b, ca, cb = g[:4]
        for v, c in ((a, ca), (b, cb)):
            if v is not None:
                s.append('<circle cx="%.1f" cy="%d" r="7" fill="%s" stroke="%s" stroke-width="2.5"/>' % (X(v), y, TEAL if c else '#ffffff', TEAL))
    if center is not None:   # |x - c| figures: a dark dot at c and the distance r to both ends, above the line
        c, r = center
        s.append('<circle cx="%.1f" cy="%d" r="6" fill="%s"/>' % (X(c), y, INK))
        for e in (c - r, c + r):
            d = -1 if e > c else 1
            s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.5"/>' % (X(c), y - 34, X(e) + 4 * d, y - 34, TEAL))
            s.append('<path d="M %.1f %d l %d -6 l 0 12 Z" fill="%s"/>' % (X(e), y - 34, 12 * d, TEAL))
            s.append('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="24" font-weight="bold">%s</text>' % ((X(c) + X(e)) / 2, y - 42, TEAL, FONT, _fmt(r)))
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.5" stroke-dasharray="4 4"/>' % (X(c), y - 34, X(c), y - 7, INK))
    if cap:
        s.append('<text x="%d" y="%d" fill="%s" %s font-size="24" font-weight="bold">%s</text>' % (L - 14, y - 30, INK, FONT, _html.escape(cap)))
    for v, sg in signs:
        s.append('<text x="%.1f" y="%d" text-anchor="middle" fill="%s" %s font-size="32" font-weight="bold">%s</text>' % (X(v), y - 18, TEAL if sg == '−' else INK, FONT, sg))
    return ''.join(s)


def _top(signs=(), bars=(), center=None, cap=None):
    """how far above the axis the figure's content reaches"""
    if bars: return 30 + 22 * (len(bars) - 1) + 34
    if center is not None: return 70
    if cap: return 56
    if signs: return 50
    return 22


def fig(lo, hi, ticks, segs, signs=(), bars=(), title='Number line', center=None, cap=None):
    top, bot = _top(signs, bars, center, cap), 52
    title = _html.escape(title, quote=True)   # strict XML: a raw < in a title freezes recordings
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 %d 640 %d" role="img" aria-label="%s">'
            '<title>%s</title>' % (Y - top, top + bot, title, title) + _body(lo, hi, ticks, segs, signs, bars, 0, center, cap) + '</svg>')


def two(a, b, title='Number lines'):
    """a, b: dicts of fig() arguments (without title); stacked in one svg."""
    out, y0 = [], 0
    title = _html.escape(title, quote=True)
    for d in (a, b):
        d = dict(d); top = _top(d.get('signs', ()), d.get('bars', ()), d.get('center'), d.get('cap'))
        out.append(_body(d.pop('lo'), d.pop('hi'), d.pop('ticks'), d.pop('segs'), dy=y0 + top - Y, **d))
        y0 += top + 52
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 %d" role="img" aria-label="%s"><title>%s</title>' % (y0, title, title)
            + ''.join(out) + '</svg>')


def add(M, vid, n, after_say, svg, label, say, w=900, gap=None):
    """Append the figure to slide n (1-based, math_api numbering) of vid and make it appear right after the spoken line
    that starts with after_say, followed by one short spoken line. Returns the new item index."""
    b = M.slide(vid, n)
    vb = [float(t) for t in _re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    h = int(round(w * vb[3] / vb[2]))
    it = {'k': 'vis', 'v': {'type': 'geometry', 'svg': svg}, 'w': w, 'h': h}
    if gap is not None: it['gap'] = gap
    b['items'].append(it)
    idx = len(b['items']) - 1

    def fn(ls):
        ls = list(ls)
        k = [i for i, l in enumerate(ls) if (l.get('say') or l.get('draw') or '').startswith(after_say)]
        assert len(k) == 1, (vid, n, after_say, k)
        ls[k[0] + 1:k[0] + 1] = [{'appear': idx, 'label': label}, {'say': say}]
        return ls
    M.edit_lines(vid, n, fn)
    return idx


def swap(M, vid, n, draw, svg, label, after_say, say, w=900):
    """Like add(), but the figure takes the place of a hand-drawn sketch: the teacher's draw note `draw` becomes the
    figure's click, and the new spoken line goes right after the spoken line that starts with after_say."""
    idx = add(M, vid, n, draw, svg, label, say, w)

    def fn(ls):
        ls = [l for l in ls if l.get('draw') != draw]
        k = [i for i, l in enumerate(ls) if l.get('say') == say]; assert len(k) == 1, (vid, say)
        new = ls.pop(k[0])
        j = [i for i, l in enumerate(ls) if (l.get('say') or '').startswith(after_say)]; assert len(j) == 1, (vid, after_say)
        ls.insert(j[0] + 1, new)
        return ls
    M.edit_lines(vid, n, fn)
    return idx


def load():
    return globals()
