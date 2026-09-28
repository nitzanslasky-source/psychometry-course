# Quantitative Reasoning · Topic 52 · Charts & Tables - SELF PRACTICE, units 16-20.
# Modelled on the charts practice book (charts_src/practice_book, units 16-20 = pages b038-b047, key b049,
# solutions b108-b124). The book's sets are real NITE exam sets, so every set here is ORIGINAL: a new story and new
# data, but the same chart type, the same number and kind of questions with the same tricks, and the correct answer
# in the same position as the book key (16: 2 2 2 3 · 17: 4 3 3 2 4 · 18: 2 4 4 3 · 19: 4 2 3 2 · 20: 4 1 4 1).
# _verify() recomputes every answer from the data below and checks that exactly one choice is right.
from vbank import _q
from math_api import rich_html, rich_plain
from charts_assets import table, _t, _l, _r, _c, _svg, _esc, INK, TEAL, AMBER, SOFT, GRID, MUTED

T52 = 52
PANEL = '#EEF3F2'
QUESTIONS, FIG = {}, {}
NOTE = 'Note: In answering each question, disregard the information appearing in the other questions.'


def _nest(svg, x, y, w, h):
    return svg.replace('<svg ', '<svg x="%d" y="%d" width="%d" height="%d" ' % (x, y, w, h), 1)


def _vb(svg):
    return [float(v) for v in svg.split('viewBox="', 1)[1].split('"', 1)[0].split()]


def _circ_label(x, y, n, size=15):
    return _c(x, y, 14, '#fff', INK, 1.6) + _t(x, y + size * 0.36, n, size, INK, 'middle', 700)


# =====================================================================================================================
# UNIT 16 · a journey in time (book: time-travel line graph with a cumulative y axis, 4 questions)
# Kai, a computer-game hero, jumps between the first 20 days of March and wins gold coins in treasure hunts.
# =====================================================================================================================
U16_HUNTS = [3, 7, 10, 14, 17, 19]
# segments of the journey: list of (date, cumulative coins in thousands, kind) ; kind 'w' = win in a hunt
U16_SEGS = [
    [(2, 0, ''), (5, 0, '')],                                   # days 1-4
    [(11, 0, ''), (15, 0, '')],                                 # days 5-9
    [(8, 0, ''), (10, 3, 'w'), (14, 5, 'w'), (16, 5, '')],      # days 10-18
    [(2, 5, ''), (3, 9, 'w'), (7, 11, 'w'), (20, 11, '')],      # days 19-37
    [(16, 11, ''), (17, 14, 'w'), (19, 20, 'w'), (20, 20, '')],  # days 38-42
]
# circled journey-day labels: (date, value, day number, dx, dy)
U16_LABELS = [(2, 0, 1, 0, -26), (5, 0, 4, 0, -26), (11, 0, 5, 0, -26), (15, 0, 9, 0, -26), (8, 0, 10, 0, -26),
              (16, 5, 18, 0, -26), (2, 5, 19, -28, 0), (20, 11, 37, 26, 0), (16, 11, 38, 0, 26), (20, 20, 42, 26, 0)]


def u16x(d): return 120 + (d - 1) * 38.0
def u16y(v): return 445 - v * 15.0


def u16_days():
    """Journey day by day: list of (journey day, date)."""
    out, day = [], 1
    for seg in U16_SEGS:
        for d in range(seg[0][0], seg[-1][0] + 1):
            out.append((day, d)); day += 1
    return out


def u16_wins():
    """Wins in journey order: (date, cumulative after the win, amount won)."""
    out, prev = [], 0
    for seg in U16_SEGS:
        for d, v, k in seg:
            if k == 'w': out.append((d, v, v - prev))
            prev = v
    return out


def u16_svg():
    W, H = 900, 580
    b = []
    # grid
    for d in range(1, 21):
        b.append(_l(u16x(d), u16y(0), u16x(d), u16y(20.6), '#C9D6D3', 1, '2 4'))
    for v in range(1, 21):
        b.append(_l(100, u16y(v), u16x(20) + 8, u16y(v), '#9FB4AF' if v % 5 == 0 else '#E3ECEA', 1.2 if v % 5 == 0 else 1,
                    '5 4' if v % 5 == 0 else '2 4'))
    # axes
    b.append(_l(100, u16y(0), u16x(20) + 22, u16y(0), INK, 2))
    b.append('<path d="M%.1f %.1f l-12 -6 v12 z" fill="%s"/>' % (u16x(20) + 30, u16y(0), INK))
    b.append(_l(100, u16y(0) + 10, 100, u16y(20) - 30, INK, 2))
    b.append('<path d="M100 %.1f l-6 12 h12 z" fill="%s"/>' % (u16y(20) - 38, INK))
    for v in range(0, 21):
        b.append(_l(94 if v % 5 else 90, u16y(v), 100, u16y(v), INK, 1.5))
    for v in range(0, 21, 5):
        b.append(_t(84, u16y(v) + 7, v, 19, INK, 'end'))
    for d in range(1, 21):
        b.append(_l(u16x(d), u16y(0), u16x(d), u16y(0) + 8, INK, 1.5))
        b.append(_t(u16x(d), u16y(0) + 28, d, 17, INK))
    for d in U16_HUNTS:
        b.append(_r(u16x(d) - 23, u16y(0) + 38, 46, 22, SOFT, TEAL, 1.2, 4))
        b.append(_t(u16x(d), u16y(0) + 54, 'Hunt', 15, TEAL, 'middle', 700))
    b.append(_t(u16x(20) + 36, u16y(0) + 86, 'Date in March', 18, INK, 'end', 700))
    b.append(_t(22, 56, 'Cumulative gold coins won', 17, INK, 'start', 700))
    b.append(_t(22, 77, 'since the start of the journey', 17, INK, 'start', 700))
    b.append(_t(22, 97, '(in thousands)', 16, MUTED, 'start'))
    # journey
    for seg in U16_SEGS:
        pts = ' '.join('%.1f,%.1f' % (u16x(d), u16y(v)) for d, v, k in seg)
        b.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % (pts, INK))
    for i, seg in enumerate(U16_SEGS):
        for j, (d, v, k) in enumerate(seg):
            if k == 'w':
                b.append(_r(u16x(d) - 7, u16y(v) - 7, 14, 14, '#fff', INK, 2.2))
            elif (j == 0 and i > 0) or (j == len(seg) - 1 and i < len(U16_SEGS) - 1):
                b.append(_c(u16x(d), u16y(v), 7, INK))
    for d, v, n, dx, dy in U16_LABELS:
        b.append(_circ_label(u16x(d) + dx, u16y(v) + dy, n))
    # legend (top right)
    lx, ly = 392, 14
    b.append(_r(lx, ly, 496, 92, '#fff', MUTED, 1.2, 6))
    b.append(_l(lx + 16, ly + 28, lx + 50, ly + 28, INK, 4)); b.append(_t(lx + 60, ly + 34, "Kai's journey", 17, INK, 'start'))
    b.append(_circ_label(lx + 33, ly + 66, 'x')); b.append(_t(lx + 60, ly + 72, 'day x of the journey', 17, INK, 'start'))
    b.append(_c(lx + 272, ly + 28, 7, INK)); b.append(_t(lx + 290, ly + 34, 'jump from / to this day', 17, INK, 'start'))
    b.append(_r(lx + 265, ly + 59, 14, 14, '#fff', INK, 2.2)); b.append(_t(lx + 290, ly + 72, 'win in a hunt', 17, INK, 'start'))
    return _svg(W, H, ''.join(b), "Kai's journey in time")


U16_INTRO = ('Study the graph below, then answer the four questions that follow.\n'
             'In the computer game "Time Runner", the hero Kai has a time portal. With it he can jump in time, and so he can '
             'take part in the treasure hunts more than once.\n'
             "The graph describes Kai's journey in time. The journey takes place over the first 20 days of March (the "
             'horizontal axis).\n'
             "The bold lines describe the course of Kai's journey: the numbers in circles are day numbers of Kai's journey. "
             'The journey began on the day marked (1) and ended on the day marked (42), that is, the journey lasted 42 days. '
             "Consecutive days of Kai's journey are not necessarily consecutive dates in March.\n"
             'A line connecting two days whose numbers are circled describes a period in March in which Kai did not jump in time.\n'
             'A black dot marks a day from which or to which Kai jumped in time.\n'
             'During the journey, 6 treasure hunts were held (marked "Hunt" under the horizontal axis). A win in a treasure '
             "hunt is marked in the graph by a square. The vertical axis shows the cumulative number of gold coins (in "
             'thousands) that Kai won in the treasure hunts. The coins from a win are received on the day of the hunt.\n'
             'For example: On day 38 of his journey, Kai arrived at March 16 for the third time. The next day (March 17) he '
             'won 3 thousand coins in the treasure hunt, and his cumulative number of coins rose from 11 to 14 thousand.\n' + NOTE)


# =====================================================================================================================
# UNIT 17 · first-name letter charts (book: four classes, letters beside a 1-6 axis, 5 questions)
# "Lakeside" summer camp, four cabins.
# =====================================================================================================================
U17_CABINS = ['Cedar', 'Maple', 'Pine', 'Willow']
U17 = {   # cabin: {count: letters}
    'Cedar':  {6: 'M', 5: 'L', 4: 'ET', 3: 'CR', 2: 'AGK', 1: 'BHJNPW'},
    'Maple':  {5: 'K', 4: 'RW', 3: 'LT', 2: 'AJNS', 1: 'BDGOQZ'},
    'Pine':   {5: 'L', 4: 'AMR', 3: 'NS', 2: 'EGY', 1: 'BCDFIPV'},
    'Willow': {6: 'L', 4: 'AS', 3: 'RTY', 2: 'EMN', 1: 'CDGHK'},
}


def u17_count(cabin, letter):
    for n, ls in U17[cabin].items():
        if letter in ls: return n
    return 0


def u17_total(cabin): return sum(n * len(ls) for n, ls in U17[cabin].items())


def u17_svg():
    W, H = 900, 400
    b = []
    pw = 216
    for k, cab in enumerate(U17_CABINS):
        px = 6 + k * (pw + 5)
        b.append(_r(px, 6, pw, H - 12, PANEL, MUTED, 1.5, 4))
        b.append(_r(px + 8, 14, 96, 36, INK, 'none', 0, 3))
        b.append(_t(px + 56, 39, cab, 20, '#fff', 'middle', 700))
        b.append(_t(px + 162, 28, 'Number of', 14, MUTED, 'middle'))
        b.append(_t(px + 162, 45, 'campers', 14, MUTED, 'middle'))
        ax = px + 52
        def y(v): return 362 - (v - 1) * 52
        b.append(_l(ax, 380, ax, 78, INK, 2))
        b.append('<path d="M%.1f 68 l-6 12 h12 z" fill="%s"/>' % (ax, INK))
        for v in range(1, 7):
            b.append(_l(ax - 7, y(v), ax, y(v), INK, 2))
            b.append(_t(ax - 12, y(v) + 7, v, 19, INK, 'end'))
            for j, ch in enumerate(U17[cab].get(v, '')):
                b.append(_t(ax + 20 + j * 20, y(v) + 7, ch, 20, INK, 'middle', 700))
    return _svg(W, H, ''.join(b), 'First letters of the campers names')


U17_INTRO = ('Study the charts below, then answer the five questions that follow.\n'
             'The "Lakeside" summer camp has four cabins: Cedar, Maple, Pine and Willow.\n'
             'The charts give data on the first names of the campers in each of the four cabins.\n'
             'Each number on each axis indicates the number of campers in the cabin whose names begin with the letter '
             'written to the right of that number.\n'
             'For example: In Pine cabin there are 3 campers whose names begin with N and 3 campers whose names begin '
             'with S. There is no camper in this cabin whose name begins with T (the letter T does not appear in the '
             'chart for Pine).\n' + NOTE)


# =====================================================================================================================
# UNIT 18 · two tables, a cohort followed over years (book: insurance plan, women / men, 4 questions)
# A mobile-phone plan for young people aged 18-23, joined in 2021, still on the plan in 2022 / 2023 (thousands).
# =====================================================================================================================
U18_AGES = [18, 19, 20, 21, 22, 23]
U18_W = {18: (88, 86, 84), 19: (80, 78, 76), 20: (71, 69, 63), 21: (60, 58, 48), 22: (45, 43, 41), 23: (30, 28, 26)}
U18_M = {18: (90, 87, 82.5), 19: (84, 80, 73.5), 20: (76, 70, 63), 21: (68, 61, 52), 22: (60, 51, 39), 23: (45, 33, 22)}


def _k(v):
    return '{:,}'.format(int(round(v * 1000)))


def u18_svg():
    parts, y = [], 0
    for name, data in (('Women', U18_W), ('Men', U18_M)):
        who = name.lower()
        s = table(['Age at\njoining', 'Number of %s\nwho joined the\nplan in 2021' % who,
                   'Number of %s\nstill on the plan\nin 2022' % who, 'Number of %s\nstill on the plan\nin 2023' % who],
                  [[str(a)] + [_k(v) for v in data[a]] for a in U18_AGES], title=name, col_w=[0.62, 1, 1, 1],
                  size=19, head_size=17, row_h=38)
        w, h = _vb(s)[2], _vb(s)[3]
        parts.append(_nest(s, 0, y, int(w), int(h))); y += int(h) + 14
    return _svg(900, y - 10, ''.join(parts), 'Women and men on the plan')


U18_INTRO = ('Study the tables below, then answer the four questions that follow.\n'
             'The tables give data on the women and the men who joined a special mobile-phone plan of a certain company '
             'in 2021. Only young people aged 18-23 can join the plan.\n'
             'For each age at which it is possible to join the plan, the tables give the number of women and men who '
             'joined the plan in 2021, and the number of women and men who were still on the plan in 2022 and in 2023.\n'
             'For example: The number of men aged 18 who joined the plan in 2021 is 90,000, and 82,500 of them were '
             'still on the plan in 2023 (when they were 20 years old).\n' + NOTE)


# =====================================================================================================================
# UNIT 19 · triangular matrix of lines (book: bus lines between 8 sites; price = background, time, frequency dots)
# Water-taxi lines between 8 piers on a lake. Fares 3 / 5 / 8 dollars; every 15 min / 30 min / hour.
# =====================================================================================================================
U19 = {   # (i, j): (minutes, fare in dollars, frequency dots)
    (1, 2): (10, 3, 2), (1, 3): (20, 3, 3), (1, 4): (15, 8, 3), (1, 5): (35, 5, 2), (1, 6): (60, 5, 1),
    (1, 7): (80, 5, 3), (1, 8): (90, 8, 2),
    (2, 3): (15, 5, 3), (2, 4): (25, 3, 1), (2, 5): (45, 5, 2), (2, 6): (70, 8, 2), (2, 7): (85, 5, 1), (2, 8): (95, 5, 3),
    (3, 4): (15, 8, 2), (3, 5): (30, 5, 3), (3, 6): (50, 3, 2), (3, 7): (55, 5, 3), (3, 8): (75, 5, 1),
    (4, 5): (20, 3, 3), (4, 6): (40, 5, 1), (4, 7): (65, 5, 2), (4, 8): (40, 8, 3),
    (5, 6): (15, 8, 3), (5, 7): (30, 5, 2), (5, 8): (60, 5, 1),
    (6, 7): (25, 5, 3), (6, 8): (45, 3, 1),
    (7, 8): (10, 5, 2),
}
U19_FILL = {3: '#FFFFFF', 5: 'url(#u19h)', 8: '#C3CFDA'}
U19_DEFS = ('<pattern id="u19h" patternUnits="userSpaceOnUse" width="9" height="9" patternTransform="rotate(45)">'
            '<rect width="9" height="9" fill="#fff"/><rect width="2.2" height="9" fill="#9DB8B3"/></pattern>')


def u19_svg():
    W, H = 900, 590
    cw, ch, gx, gy = 66, 60, 78, 58
    b = [_t(24, 40, 'Piers', 18, INK, 'start', 700), _l(20, 50, gx - 4, 50, INK, 1.5), _l(gx - 4, 20, gx - 4, gy + 8 * ch, INK, 1.5)]
    for j in range(1, 9):
        b.append(_t(gx + (j - 1) * cw + cw / 2, 42, j, 19, INK, 'middle', 700))
    for i in range(1, 9):
        y = gy + (i - 1) * ch
        b.append(_t(gx - 26, y + ch / 2 + 7, i, 19, INK, 'middle', 700))
        for j in range(i, 9):
            x = gx + (j - 1) * cw
            if j == i:
                b.append(_r(x, y, cw, ch, '#fff', INK, 1.5)); continue
            t, f, n = U19[(i, j)]
            b.append(_r(x, y, cw, ch, U19_FILL[f], INK, 1.5))
            b.append(_r(x + cw / 2 - 20, y + 8, 40, 24, '#fff' if f != 8 else '#C3CFDA', 'none'))
            b.append(_t(x + cw / 2, y + 27, t, 20, INK, 'middle', 700))
            for k in range(n):
                b.append(_c(x + cw / 2 + (k - (n - 1) / 2.0) * 12, y + 45, 4.2, INK))
    # legend
    lx = 650
    b.append(_r(lx, 190, 230, 170, '#fff', MUTED, 1.2, 6))
    b.append(_t(lx + 115, 220, 'Fare', 18, INK, 'middle', 700))
    for k, (f, lab) in enumerate(((3, '3 dollars'), (5, '5 dollars'), (8, '8 dollars'))):
        yy = 240 + k * 38
        b.append(_r(lx + 30, yy, 28, 26, U19_FILL[f], INK, 1.5))
        b.append(_t(lx + 72, yy + 20, lab, 18, INK, 'start'))
    b.append(_r(lx, 380, 230, 170, '#fff', MUTED, 1.2, 6))
    b.append(_t(lx + 115, 408, 'Water-taxi frequency', 18, INK, 'middle', 700))
    for k, (n, a, c) in enumerate(((3, 'high:', 'every 15 minutes'), (2, 'medium:', 'every 30 minutes'), (1, 'low:', 'every hour'))):
        yy = 440 + k * 36
        for m in range(n):
            b.append(_c(lx + 24 + m * 11, yy, 4.2, INK))
        b.append(_t(lx + 66, yy - 2, a, 16, INK, 'start', 700))
        b.append(_t(lx + 66, yy + 16, c, 16, INK, 'start'))
    return _svg(W, H, ''.join(b), 'Water-taxi lines between eight piers', U19_DEFS)


U19_INTRO = ('Study the chart below, then answer the four questions that follow.\n'
             'The chart gives data on all the water-taxi lines that connect eight piers on a lake. The piers are '
             'numbered from 1 to 8.\n'
             'Each square in the chart (that is not empty) represents one water-taxi line that connects two piers:\n'
             'the background of the square represents the fare on the line, the number in the square indicates the '
             'length of the trip on the line (in minutes), and the number of black dots represents the frequency of the '
             'water taxis on the line (see legend).\n'
             'The fare, the length of the trip and the frequency of the water taxis are the same in both directions of '
             'the line.\n'
             'The first water taxis leave all the piers at 06:00 in the morning. After that, the water taxis leave the '
             'piers at the frequency shown in the chart, with no delays.\n'
             'For example: On the line connecting piers 7 and 8 the frequency of the water taxis is medium. The trip on '
             'this line takes 10 minutes, and the fare is 5 dollars.\n' + NOTE)


# =====================================================================================================================
# UNIT 20 · quartile lines in four panels (book: 4 measures x 4 countries, dots = the whole world)
# Four measures in four cities A-D; dots = the whole country.
# =====================================================================================================================
U20 = [   # (title, unit, vmin, vmax, minor, major, {city: (lower quartile, median, upper quartile)}, country dots)
    ('Daily commute', '(in minutes)', 0, 70, 5, 10,
     {'A': (30, 40, 55), 'B': (35, 45, 55), 'C': (15, 30, 60), 'D': (20, 30, 40)}, (20, 30, 45)),
    ('Monthly rent', '(in dollars)', 200, 2400, 200, 400,
     {'A': (600, 1400, 2200), 'B': (1000, 1400, 1800), 'C': (400, 800, 1600), 'D': (400, 600, 1000)}, (600, 1000, 1600)),
    ('Age of home', '(in years)', 0, 60, 5, 10,
     {'A': (20, 30, 45), 'B': (25, 30, 40), 'C': (15, 25, 40), 'D': (10, 20, 30)}, (10, 25, 35)),
    ('Sleep per night', '(in hours)', 4, 10, 0.5, 1,
     {'A': (6.5, 7.5, 9), 'B': (7, 7.5, 8.5), 'C': (5.5, 7, 8.5), 'D': (5.5, 6.5, 7)}, (6, 7, 8)),
]


def _num(v):
    return ('%g' % v) if v < 1000 else '{:,}'.format(int(v)).replace(',', '')


def u20_svg():
    W, H = 900, 680
    b = []
    # legend
    lx, ly = 330, 12
    b.append(_r(lx, ly, 240, 112, '#fff', MUTED, 1.2, 6))
    bx = lx + 120
    b.append(_l(bx, ly + 22, bx, ly + 92, INK, 3))
    for yy, pct, lab in ((ly + 22, '75%', 'upper quartile'), (ly + 57, '50%', 'median'), (ly + 92, '25%', 'lower quartile')):
        b.append(_l(bx - 8, yy, bx + 8, yy, INK, 3))
        b.append(_t(bx - 16, yy + 6, pct, 16, INK, 'end'))
        b.append(_t(bx + 16, yy + 6, lab, 16, INK, 'start'))
    pw = 216
    for k, (title, unit, vmin, vmax, minor, major, cities, dots) in enumerate(U20):
        px = 6 + k * (pw + 5)
        b.append(_t(px + pw / 2, 158, title, 19, INK, 'middle', 700))
        b.append(_t(px + pw / 2, 180, unit, 15, MUTED, 'middle'))
        b.append(_r(px, 192, pw, 480, PANEL, 'none'))
        ax = px + 124
        def y(v): return 632 - (v - vmin) * (400.0 / (vmax - vmin))
        b.append(_l(ax, 656, ax, 214, INK, 2))
        b.append('<path d="M%.1f 204 l-6 12 h12 z" fill="%s"/>' % (ax, INK))
        v = vmin
        while v <= vmax + 1e-9:
            big = abs((v - vmin) / major - round((v - vmin) / major)) < 1e-9
            b.append(_l(ax - (9 if big else 5), y(v), ax, y(v), INK, 1.6))
            if big: b.append(_t(ax - 13, y(v) + 6, _num(v), 16, INK, 'end'))
            v += minor
        for d in dots:
            b.append(_c(ax, y(d), 5.5, INK))
        for c, bx2 in (('A', px + 24), ('B', px + 50), ('C', px + 158), ('D', px + 186)):
            lo, me, hi = cities[c]
            b.append(_l(bx2, y(lo), bx2, y(hi), INK, 3))
            for vv in (lo, me, hi):
                b.append(_l(bx2 - 8, y(vv), bx2 + 8, y(vv), INK, 3))
            b.append(_t(bx2, y(hi) - 10, c, 17, INK, 'middle', 700))
    return _svg(W, H, ''.join(b), 'Four measures in four cities')


U20_INTRO = ('Study the charts below, then answer the four questions that follow.\n'
             'The charts give data on four measures: daily commute (in minutes), monthly rent (in dollars), age of home '
             '(in years) and sleep per night (in hours). The data were measured in four cities: A, B, C and D.\n'
             'The data measured in each of the cities are shown in the charts by a vertical line (see legend):\n'
             'the mark at the lower end of each line represents the value that 25% of the population are equal to or '
             'below; it is called the "lower quartile";\n'
             'the mark in the middle of each line represents the value that 50% of the population are equal to or '
             'below; it is called the "median";\n'
             'the mark at the upper end of each line represents the value that 75% of the population are equal to or '
             'below; it is called the "upper quartile".\n'
             'The dots marked on the number axes represent the same data for the whole country.\n'
             'For example: In city C, 25% of the population sleep 5.5 hours per night or less, 50% of the population '
             'sleep 7 hours per night or less, and 75% of the population sleep 8.5 hours per night or less.\n' + NOTE)


# =====================================================================================================================
# questions
# =====================================================================================================================
TITLES = {16: 'A journey in time', 17: 'Letters of first names', 18: 'A phone plan over three years',
          19: 'Water-taxi lines', 20: 'Quartiles in four cities'}


def mk(unit, n, intro, stem, choices, key, steps, fig, plain=None):
    qid = 'chp%02d-q%d' % (unit, n)
    full = intro + '\n\n' + stem
    plain = plain or [rich_plain(c) for c in choices]
    q = _q(qid, T52, rich_plain(full), plain, key, '',
           dict(subject='charts', trustRank=1, reviewFlag=False,
                source='Charts practice book unit %d q%d (original set modelled on it)' % (unit, n),
                setTitle='Unit %d · %s' % (unit, TITLES[unit])))
    q.update(stem=full.replace('$', ''), stemRich=full, stemHtml=rich_html(full),
             choices=list(plain), choicesRich=list(choices), choicesHtml=[rich_html(c) for c in choices],
             explanation=list(steps), answerHtml=''.join('<p>%s</p>' % rich_html(e) for e in steps),
             work=[], workText=[], methods=[dict(title='Worked solution', steps=list(steps), work=[], independent=False, board=[])],
             navLabel=rich_plain(stem.replace('\n', ' '))[:120], questionVisual={'type': 'geometry', 'svg': fig},
             setIntro=intro)
    QUESTIONS[qid] = q; FIG[qid] = fig


S16, S17, S18, S19, S20 = u16_svg(), u17_svg(), u18_svg(), u19_svg(), u20_svg()

# ---------------- Unit 16 (book b038-b039; key 2 2 2 3) ----------------
mk(16, 1, U16_INTRO, 'How many times during his journey was Kai on March 10?', ['1', '2', '3', '0'], 2, [
    'Look at the column of March 10 (above the date 10 on the horizontal axis) and count how many times a bold line '
    'passes through it.',
    'The line of days 10-18 (from March 8 to March 16) passes through it - here Kai won in the hunt (the square at 3).',
    'The long line of days 19-37 (from March 2 to March 20) also passes through it, at height 11 - here he did not win.',
    'The lines on the horizontal axis (March 2-5 and March 11-15) do not reach March 10, and neither does the last line '
    '(March 16-20). So Kai was on March 10 twice.',
    'Trap: counting only the square (1) - a day on which Kai did not win is still a day on which he was there.'], S16)

mk(16, 2, U16_INTRO, 'What was the cumulative number of coins (in thousands) that Kai had after he had won 5 times in the '
   'treasure hunts?', ['11', '14', '19', '20'], 2, [
    'Way 1: the cumulative number only goes up, so the higher a square is, the later the win was in the journey. The 5th '
    'win is the 5th square from the bottom: 3, 5, 9, 11, 14. Its height is 14.',
    'Way 2: follow the journey by the circled day numbers: March 10 (day 12), March 14 (day 16), March 3 (day 20), '
    'March 7 (day 24), March 17 (day 39). The 5th win brings the total to 14 thousand coins.',
    '11 is the total after only 4 wins, 20 is the total after all 6 wins, and 19 is a day number (circled), not a value.'], S16)

mk(16, 3, U16_INTRO, 'How many coins (in thousands) did Kai win in the treasure hunt of March 7?', ['0', '2', '9', '11'], 2, [
    'The square on March 7 is at height 11 - but that is the CUMULATIVE number of coins from all his wins so far, not '
    'the win of that day.',
    'The win of a day = the total after the win minus the total before it. Before March 7 (the previous win, on March 3) '
    'the total was 9.',
    '$11 - 9 = 2$ thousand coins.'], S16)

mk(16, 4, U16_INTRO, "The first time in Kai's journey that he won a treasure hunt was on March ___.",
   ['7', '3', '10', '14'], 3, [
    'Way 1: the cumulative number only goes up, so the first win is the LOWEST square in the graph: the square at '
    'height 3, above March 10.',
    'Way 2: follow the journey by the circled numbers. Days 1-4 (March 2-5) and days 5-9 (March 11-15) have no square. '
    'The next line starts on day 10 at March 8, and the first square on it is on March 10 (day 12).',
    'Trap: March 3 is the earliest DATE with a win, but Kai won there only later in his journey (day 20).'], S16)

# ---------------- Unit 17 (book b040-b041; key 4 3 3 2 4) ----------------
mk(17, 1, U17_INTRO, 'Tom, Tara and Tyler are in the same cabin at the "Lakeside" camp.\nIn which cabin are they, for certain?',
   ['In Cedar', 'In Maple', 'In Pine', 'It cannot be determined'], 4, [
    'All three names begin with T, so we need a cabin with at least 3 campers whose names begin with T.',
    'Look for T in every chart: Cedar - T is next to 4; Maple - T is next to 3; Willow - T is next to 3; Pine - no T.',
    'The three could be in Cedar, in Maple or in Willow, so the cabin cannot be determined for certain.',
    'Trap: stopping at the first cabin that fits (Cedar). "For certain" means you must check the other cabins too.'], S17)

mk(17, 2, U17_INTRO, 'It is known that the names of 40% of the boys in Willow cabin begin with S, and that there is no girl in '
   'this cabin whose name begins with S.\nHow many girls are there in Willow cabin?', ['14', '20', '24', '30'], 3, [
    'In Willow, S is next to 4: 4 campers - all of them boys - and they are 40% of the boys.',
    '40% is 4, so 100% is 10: there are 10 boys. (Or: $\\frac{40}{100} \\cdot x = 4$, so $x = 10$.)',
    'Total campers in Willow (number x letters in the row): $6 \\cdot 1 + 4 \\cdot 2 + 3 \\cdot 3 + 2 \\cdot 3 + 1 \\cdot 5 = 34$.',
    'Girls: $34 - 10 = 24$.',
    'Traps: 30 subtracts only the 4 S-boys; 14 is the number of different letters, not of campers.'], S17)

mk(17, 3, U17_INTRO, 'On a certain day some of the campers in Maple cabin were absent. Among the campers who were present in '
   'the cabin, there were no two (or more) whose names begin with the same letter.\nAt least how many campers were absent '
   'from the cabin on that day?', ['14', '16', '18', '20'], 3, [
    'For each letter, at most one camper was present. So from a letter with n campers, at least $n - 1$ were absent.',
    'Maple: K - 5 campers (4 absent); R and W - 4 each (3 + 3 absent); L and T - 3 each (2 + 2 absent); '
    'A, J, N, S - 2 each (1 absent from each, 4 in all); the letters with 1 camper - nobody has to be absent.',
    '$4 + 3 + 3 + 2 + 2 + 1 + 1 + 1 + 1 = 18$.',
    'Check: Maple has 33 campers and 15 different letters, so at most 15 were present: $33 - 15 = 18$.'], S17)

mk(17, 4, U17_INTRO, 'Ethan is a camper in Cedar cabin. Every morning the counselor of Cedar cabin reads out the first names '
   'of the campers in alphabetical order (from A to Z).\nHow many names does the counselor read out before she reads '
   "out Ethan's name?", ['At most 8', 'At most 9', 'At least 8', 'At least 9'], 2, [
    'The letters before E are A, B, C and D. In Cedar: A - 2 campers, B - 1, C - 3, D - none. These 6 names are read '
    'before Ethan for certain.',
    'E is next to 4: Ethan and 3 more campers whose names begin with E. We do not know if they come before or after '
    'Ethan, so 0 to 3 more names may be read before him.',
    'So between 6 and 9 names are read before Ethan - at most 9.',
    '"At most 8" is wrong, since 9 is possible; "at least 8" and "at least 9" are wrong, since 6 is possible.'], S17)

mk(17, 5, U17_INTRO, 'Gabe, Ivy, Owen and Quinn are campers at the "Lakeside" camp.\nHence, ___ and ___ are definitely in '
   'the same cabin.', ['Gabe ; Ivy', 'Gabe ; Owen', 'Ivy ; Quinn', 'Owen ; Quinn'], 4, [
    'Two campers are definitely in the same cabin only if each of their letters appears in one cabin only - and it is '
    'the same cabin. So look for the "rare" letters, those that appear in the fewest charts.',
    'O appears only in Maple (once), and Q appears only in Maple (once). So Owen and Quinn are both in Maple.',
    'The others: G appears in all four cabins, so Gabe could be anywhere; I appears only in Pine, and Q only in Maple, '
    'so Ivy and Quinn are definitely NOT together.'], S17)

# ---------------- Unit 18 (book b042-b043; key 2 4 4 3) ----------------
mk(18, 1, U18_INTRO, 'What is the number of men who were still on the plan in 2022 and who, when they joined the plan in '
   '2021, were older by at least 4 years than other customers who joined the plan that year?',
   ['33,000', '84,000', '105,000', '145,000'], 2, [
    'The youngest customers who joined in 2021 were 18. Older by at least 4 years: men who joined at 22 or 23.',
    'Men still on the plan in 2022 (third column of the men table): age 22 - 51,000; age 23 - 33,000.',
    '$51,000 + 33,000 = 84,000$.',
    'Traps: 105,000 uses the 2021 column; 145,000 adds age 21 as well; 33,000 takes age 23 only.'], S18)

mk(18, 2, U18_INTRO, 'Among the men who joined the plan in 2021 at the age of 22, what percentage were no longer on the plan '
   'in 2023?', ['20%', '25%', '30%', '35%'], 4, [
    'Way 1: 60,000 men aged 22 joined in 2021, and 39,000 of them were still on the plan in 2023. So 21,000 left.',
    '$\\frac{21}{60} = \\frac{35}{100} = 35\\%$ (the zeros can be dropped - only the ratio matters).',
    'Way 2 - plugging in the answers (start with a middle one): 30% of 60,000 is 18,000, which would leave 42,000 - '
    'but only 39,000 remained, so more than 30% left. Only (4) is left; check: 35% of 60,000 = 21,000 and '
    '$60,000 - 21,000 = 39,000$.'], S18)

mk(18, 3, U18_INTRO, 'A "loyal customer" of the company is a customer who joined the plan in year x and was still on the plan '
   'in year x+2.\nAmong the customers who joined the plan in 2021, what is the difference between the number of women '
   'who are loyal customers and the number of men who are loyal customers?', ['2,000', '3,500', '4,000', '6,000'], 4, [
    'The loyal customers among those who joined in 2021 are those still on the plan in 2023: the last column of each table.',
    'Instead of adding each column, subtract row by row (women minus men, in thousands): '
    '$84 - 82.5 = 1.5$, $76 - 73.5 = 2.5$, $63 - 63 = 0$, $48 - 52 = -4$, $41 - 39 = 2$, $26 - 22 = 4$.',
    '$1.5 + 2.5 + 0 - 4 + 2 + 4 = 6$, so the difference is 6,000 (more women).',
    'Careful with the one negative row (age 21): there are more men than women there.'], S18)

mk(18, 4, U18_INTRO, 'The higher the age at which women joined the plan, the percentage of women who were no longer on the '
   'plan in 2022, out of those who joined it in 2021, ___.',
   ['remains constant', 'decreases', 'increases', 'first decreases and then increases'], 3, [
    'In every row of the women table, the 2022 number is smaller by exactly 2,000 than the 2021 number: 2,000 women of '
    'each age left.',
    'But the question asks about a PERCENTAGE of those who joined. The numbers who joined go down as the age goes up '
    '(88,000, 80,000, ..., 30,000).',
    'The same part (2,000) out of a smaller and smaller whole is a larger and larger percentage: '
    '$\\frac{2}{88} < \\frac{2}{80} < ... < \\frac{2}{30}$. So the percentage increases.',
    'Trap: "remains constant" is true for the NUMBER of women who left, not for the percentage.'], S18)

# ---------------- Unit 19 (book b044-b045; key 4 2 3 2) ----------------
mk(19, 1, U19_INTRO, 'Of the lines on which the trip takes 15 minutes, what percentage are lines on which the fare is 8 '
   'dollars?', ['25%', '$33\\frac{1}{3}$%', '50%', '75%'], 4, [
    'First find all the lines with 15 in the square: 1-4, 2-3, 3-4 and 5-6 - 4 lines.',
    'Of these, the dark (8 dollars) squares are 1-4, 3-4 and 5-6 - 3 lines (2-3 is striped: 5 dollars).',
    '$\\frac{3}{4} = 75\\%$.'], S19, ['25%', '33 1/3%', '50%', '75%'])

mk(19, 2, U19_INTRO, 'On average, how long (in minutes) does the trip take between piers whose numbers differ by 4?',
   ['40', '50', '60', '70'], 2, [
    'The pairs whose numbers differ by 4: 1-5, 2-6, 3-7 and 4-8 (they lie on one diagonal of the chart).',
    'Their trip lengths: 1-5 - 35, 2-6 - 70, 3-7 - 55, 4-8 - 40 minutes.',
    'Average: $\\frac{35 + 70 + 55 + 40}{4} = \\frac{200}{4} = 50$ minutes.'], S19)

mk(19, 3, U19_INTRO, 'The fare from pier A to pier B is 8 dollars.\nWhich of the following statements could be true?',
   ['On the line connecting pier A and pier B the frequency of the water taxis is low',
    'The trip from pier A to pier B takes 60 minutes', 'Pier B is pier 6',
    'The difference between the numbers of piers A and B is 5'], 3, [
    'The 8-dollar lines are the dark squares: 1-4 (15 min, 3 dots), 1-8 (90, 2 dots), 2-6 (70, 2 dots), 3-4 (15, 2 dots), '
    '4-8 (40, 3 dots), 5-6 (15, 3 dots). Check each answer only against these squares.',
    '(1) Low frequency = one dot. No dark square has one dot - rejected.',
    '(2) No dark square has 60 in it (the 60-minute lines, 1-6 and 5-8, are striped) - rejected.',
    '(3) Pier 6 appears in the dark squares 2-6 and 5-6, so B could be pier 6 (and A pier 2 or 5) - this is the answer.',
    'Tip: once you find an answer that could be true, you can stop. For completeness, (4): the differences in the dark '
    'squares are 3, 7, 4, 1, 4 and 1 - never 5, so (4) is rejected.'], S19)

mk(19, 4, U19_INTRO, 'On each of the days Monday to Friday, Noa travels in the morning from pier 3 to pier 6, and in the '
   'afternoon she travels back on the same line from pier 6 to pier 3. These are her only trips.\nThe water-taxi company '
   'decided to raise the fare on this line to 8 dollars.\nBy how much will the total fare that Noa pays for all her '
   'trips from Monday to Friday of one week increase (in dollars)?', ['80', '50', '40', '25'], 2, [
    'Monday to Friday is 5 days, with 2 trips each day: 10 trips a week.',
    'The square 3-6 is white: the fare now is 3 dollars. It rises to 8 dollars - an increase of 5 dollars per trip.',
    '$10 \\cdot 5 = 50$ dollars.',
    'Traps: 80 is the whole new weekly fare, not the increase; 25 counts one trip a day.'], S19)

# ---------------- Unit 20 (book b046-b047; key 4 1 4 1) ----------------
mk(20, 1, U20_INTRO, 'The home of ___ of the residents of city ___ is 30 years old or less.',
   ['25% ; A', '25% ; B', '75% ; C', '75% ; D'], 4, [
    'Look at the "Age of home" chart and find, for each city in the answers, the mark at 30.',
    '(1) In A, 30 is the MIDDLE mark - the median, that is 50%, not 25%. Rejected.',
    '(2) In B, 30 is also the median (50%). Rejected.',
    '(3) In C there is no mark at 30 at all (its marks are 15, 25 and 40). Rejected.',
    'Tip: after rejecting three answers you may mark the fourth. Check: in D, 30 is the UPPER mark - the upper quartile, '
    '75%. Correct.'], S20)

mk(20, 2, U20_INTRO, 'In how many of the cities is the median sleep per night lower than the median sleep per night in the '
   'whole country?', ['1', '2', '3', '0'], 1, [
    'The country median is the middle dot on the axis of the "Sleep per night" chart: 7 hours.',
    'The medians (middle marks) of the cities: A - 7.5, B - 7.5, C - 7, D - 6.5.',
    'Only D is lower than 7. C is EQUAL to 7, not lower - so the answer is 1 city.'], S20)

mk(20, 3, U20_INTRO, 'The "rent-gap index" of a city is defined as the gap in monthly rent between the upper quartile and '
   'the lower quartile in that city.\nWhat is the order of the cities by their rent-gap index, from the largest to the '
   'smallest (from left to right)?', ['A, B, C, D', 'C, A, D, B', 'A, C, D, B', 'A, C, B, D'], 4, [
    'The upper quartile is the top of each line and the lower quartile is its bottom, so the gap is simply the LENGTH '
    'of the line in the "Monthly rent" chart.',
    'A: 600 to 2,200 - 1,600. C: 400 to 1,600 - 1,200. B: 1,000 to 1,800 - 800. D: 400 to 1,000 - 600.',
    'From the longest line to the shortest: A, C, B, D.',
    'Trap: A, B, C, D orders the cities by the TOP of the line only.'], S20)

mk(20, 4, U20_INTRO, 'A "quality-of-life index" is defined as follows:\n'
   '10 · (lower quartile of daily commute + lower quartile of monthly rent + lower quartile of age of home + lower '
   'quartile of sleep per night)\nThe quality-of-life index in city C is ___ the quality-of-life index in city D.',
   ['equal to', 'higher by 50 than', 'lower by 50 than', 'higher by 5 than'], 1, [
    'We compare only the bottoms of the lines of C and D in the four charts - no need to add everything up.',
    'Monthly rent: both 400 - no difference. Sleep: both 5.5 - no difference.',
    'Daily commute: C 15, D 20 - C lower by 5. Age of home: C 15, D 10 - C higher by 5.',
    'The two differences cancel, so the sums are equal, and so are the sums times 10: the indexes are equal.',
    'Traps: "lower by 50" / "higher by 50" look at one chart only (times 10); "higher by 5" also forgets the 10.'], S20)


# =====================================================================================================================
# verification
# =====================================================================================================================
def _verify():
    def ans(qid): return QUESTIONS[qid]['correct'][0] + 1
    def one(qid, vals, good):
        hits = [k + 1 for k, v in enumerate(vals) if good(v)]
        assert hits == [ans(qid)], (qid, hits, ans(qid))
        assert len(QUESTIONS[qid]['choices']) == 4
    # ---- unit 16
    days = u16_days(); assert len(days) == 42 and days[-1] == (42, 20)
    lab = {n: (d, v) for d, v, n, dx, dy in U16_LABELS}
    for n, (d, v) in lab.items(): assert dict(days)[n] == d, (n, d)
    wins = u16_wins(); assert [w[0] for w in wins] == [10, 14, 3, 7, 17, 19] and all(w[0] in U16_HUNTS for w in wins)
    assert all(w[2] > 0 for w in wins)
    for seg in U16_SEGS:   # cumulative value changes only at a win
        for (d1, v1, k1), (d2, v2, k2) in zip(seg, seg[1:]): assert v2 == v1 or k2 == 'w'
    for a, b2 in zip(U16_SEGS, U16_SEGS[1:]): assert a[-1][1] == b2[0][1]      # a jump keeps the total
    ex = [n for n, d in days if d == 16]; assert ex == [18, 33, 38]              # example: day 38 = 3rd time at March 16
    w17 = [w for w in wins if w[0] == 17][0]; assert w17[2] == 3 and w17[1] == 14 and dict(days)[39] == 17
    one('chp16-q1', [1, 2, 3, 0], lambda v: v == sum(1 for n, d in days if d == 10))
    one('chp16-q2', [11, 14, 19, 20], lambda v: v == wins[4][1])
    one('chp16-q3', [0, 2, 9, 11], lambda v: v == [w for w in wins if w[0] == 7][0][2])
    one('chp16-q4', [7, 3, 10, 14], lambda v: v == wins[0][0])
    assert sorted(w[1] for w in wins)[4] == wins[4][1] and min(w[1] for w in wins) == wins[0][1]   # "by height" shortcut
    # ---- unit 17
    for c in U17: assert all(len(set(ls)) == len(ls) for ls in U17[c].values())
    allL = {c: ''.join(U17[c].values()) for c in U17}
    for c in allL: assert len(set(allL[c])) == len(allL[c])
    assert u17_count('Pine', 'N') == 3 and u17_count('Pine', 'S') == 3 and u17_count('Pine', 'T') == 0
    fits = [c for c in U17_CABINS if u17_count(c, 'T') >= 3]
    one('chp17-q1', ['Cedar', 'Maple', 'Pine', None], lambda v: (v is None) == (len(fits) > 1) and (v is None or fits == [v]))
    boys = u17_count('Willow', 'S') / 0.4; assert boys == int(boys)
    one('chp17-q2', [14, 20, 24, 30], lambda v: v == u17_total('Willow') - boys)
    assert len(allL['Willow']) == 14
    one('chp17-q3', [14, 16, 18, 20], lambda v: v == sum(n - 1 for n in (u17_count('Maple', ch) for ch in allL['Maple'])))
    sure = sum(u17_count('Cedar', ch) for ch in 'ABCD'); lo, hi = sure, sure + u17_count('Cedar', 'E') - 1
    one('chp17-q4', [('max', 8), ('max', 9), ('min', 8), ('min', 9)],
        lambda v: (v[0] == 'max' and v[1] == hi) or (v[0] == 'min' and v[1] == lo))
    where = {ch: [c for c in U17_CABINS if u17_count(c, ch)] for ch in 'GIOQ'}
    def same(p): a, b2 = where[p[0]], where[p[1]]; return len(a) == 1 and a == b2
    one('chp17-q5', ['GI', 'GO', 'IQ', 'OQ'], same)
    # ---- unit 18
    for tab in (U18_W, U18_M):
        for a in U18_AGES: assert tab[a][0] > tab[a][1] > tab[a][2]
    assert U18_M[18][0] == 90 and U18_M[18][2] == 82.5
    old = [a for a in U18_AGES if a >= min(U18_AGES) + 4]
    one('chp18-q1', [33000, 84000, 105000, 145000], lambda v: v == sum(U18_M[a][1] for a in old) * 1000)
    one('chp18-q2', [20, 25, 30, 35], lambda v: abs(v - 100.0 * (U18_M[22][0] - U18_M[22][2]) / U18_M[22][0]) < 1e-9)
    d3 = sum(U18_W[a][2] for a in U18_AGES) - sum(U18_M[a][2] for a in U18_AGES)
    one('chp18-q3', [2000, 3500, 4000, 6000], lambda v: abs(v - d3 * 1000) < 1e-6)
    pct = [(U18_W[a][0] - U18_W[a][1]) / U18_W[a][0] for a in U18_AGES]
    trend = ('const' if all(abs(p - pct[0]) < 1e-12 for p in pct) else 'up' if all(x < y for x, y in zip(pct, pct[1:]))
             else 'down' if all(x > y for x, y in zip(pct, pct[1:])) else 'mixed')
    one('chp18-q4', ['const', 'down', 'up', 'downup'], lambda v: v == trend)
    # ---- unit 19
    assert len(U19) == 28 and U19[(7, 8)] == (10, 5, 2)
    l15 = [p for p in U19 if U19[p][0] == 15]
    one('chp19-q1', [25, 100 / 3.0, 50, 75], lambda v: abs(v - 100.0 * sum(U19[p][1] == 8 for p in l15) / len(l15)) < 1e-9)
    d4 = [U19[(i, i + 4)][0] for i in range(1, 5)]
    one('chp19-q2', [40, 50, 60, 70], lambda v: v == sum(d4) / 4.0)
    dark = [p for p in U19 if U19[p][1] == 8]
    one('chp19-q3', [lambda p: U19[p][2] == 1, lambda p: U19[p][0] == 60, lambda p: 6 in p, lambda p: abs(p[0] - p[1]) == 5],
        lambda f: any(f(p) for p in dark))
    one('chp19-q4', [80, 50, 40, 25], lambda v: v == 5 * 2 * (8 - U19[(3, 6)][1]))
    # ---- unit 20
    P = {t: cities for t, u, a, b2, mi, ma, cities, dots in U20}
    D = {t: dots for t, u, a, b2, mi, ma, cities, dots in U20}
    for t in P:
        for c in P[t]: assert P[t][c][0] < P[t][c][1] < P[t][c][2]
    assert P['Sleep per night']['C'] == (5.5, 7, 8.5)
    def q1(v):
        pct, c = v; q = P['Age of home'][c]
        return 30 in q and {0: 25, 1: 50, 2: 75}[q.index(30)] == pct
    one('chp20-q1', [(25, 'A'), (25, 'B'), (75, 'C'), (75, 'D')], q1)
    one('chp20-q2', [1, 2, 3, 0], lambda v: v == sum(P['Sleep per night'][c][1] < D['Sleep per night'][1] for c in 'ABCD'))
    gap = {c: P['Monthly rent'][c][2] - P['Monthly rent'][c][0] for c in 'ABCD'}
    assert len(set(gap.values())) == 4
    order = ''.join(sorted('ABCD', key=lambda c: -gap[c]))
    one('chp20-q3', ['ABCD', 'CADB', 'ACDB', 'ACBD'], lambda v: v == order)
    idx = {c: 10 * sum(P[t][c][0] for t in P) for c in 'CD'}
    one('chp20-q4', [0, 50, -50, 5], lambda v: abs(idx['C'] - idx['D'] - v) < 1e-9)
    return True


_verify()

MODULES = []
PRACTICE = {52: ['chp16-q1', 'chp16-q2', 'chp16-q3', 'chp16-q4',
                 'chp17-q1', 'chp17-q2', 'chp17-q3', 'chp17-q4', 'chp17-q5',
                 'chp18-q1', 'chp18-q2', 'chp18-q3', 'chp18-q4',
                 'chp19-q1', 'chp19-q2', 'chp19-q3', 'chp19-q4',
                 'chp20-q1', 'chp20-q2', 'chp20-q3', 'chp20-q4']}
MEMORY = []
assert PRACTICE[52] == list(QUESTIONS)
