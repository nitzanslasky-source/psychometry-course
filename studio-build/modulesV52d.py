# Quantitative Reasoning · Topic 52 · Charts & Tables — SELF-PRACTICE units 6-10 (charts practice book).
# Source: the charts practice book, units 6-10 (chart pages b018-b027, key b048, written solutions b070-b089).
# The book sets are scanned real NITE sets, so nothing is copied: every unit is an ORIGINAL set with a new story and
# new data, but the same chart type, the same number and kinds of questions with the same tricks, and the correct
# answer in the same position as the book key:
#   unit 6  3 4 1 2   (two-level table: rate % + count for 4 bodies over 5 years)       -> flight schools
#   unit 7  3 2 3 1   (stacked columns: salary / output + employment timeline bars)     -> magazine photographers
#   unit 8  4 4 3 3   (score table, +1 / -1 scoring, two groups of participants)        -> puzzle championship
#   unit 9  4 2 4 4   (grid table, two numbers per cell split by a diagonal)            -> wall tiles in a store
#   unit 10 1 2 1 3   (table with a follow-up triangle: produced / good / used by year)  -> plant nursery
# _verify() (run at import) recomputes every answer from the data below and checks that exactly one choice is right
# and that it sits at the book-key position.
import re
from vbank import _q
from math_api import rich_html, rich_plain

T52 = 52
INK, TEAL, AMBER, SOFT, GRID, MUTED = '#0F172A', '#0F766E', '#F5A524', '#E6F4F1', '#D8E6E3', '#5B6B7A'
MID = '#7FB8AE'           # medium teal (second series)
FONT = "font-family=\"'Helvetica Neue',Helvetica,Arial,sans-serif\""
NOTE = 'Note: In answering each question, disregard the information appearing in the other questions.'


# =====================================================================================================================
# svg helpers
# =====================================================================================================================
def _svg(W, H, label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s"><title>%s</title>'
            '<rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W, H, label, label, W, H, body))


def _t(x, y, s, size=18, color=INK, anchor='middle', weight=400, rot=None):
    tr = ' transform="rotate(%d %.1f %.1f)"' % (rot, x, y) if rot else ''
    s = str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle" fill="%s" %s font-size="%d" font-weight="%d"%s>%s</text>'
            % (x, y, anchor, color, FONT, size, weight, tr, s))


def _tl(x, y, lines, size=18, color=INK, anchor='middle', weight=400, gap=1.18):
    """several centred lines around y"""
    n = len(lines)
    return ''.join(_t(x, y + (j - (n - 1) / 2.0) * size * gap, ln, size, color, anchor, weight) for j, ln in enumerate(lines))


def _l(x1, y1, x2, y2, color=INK, w=1.5, dash=None):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, color, w, ' stroke-dasharray="%s"' % dash if dash else ''))


def _r(x, y, w, h, fill='none', stroke=INK, sw=1.5, rx=0):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="%s" rx="%s"/>'
            % (x, y, w, h, fill, stroke, sw, rx))


def _n(v):
    """1,250 style"""
    return '{:,}'.format(v)


# =====================================================================================================================
# UNIT 6 · two-level table (book: 4 job-training institutes, success % + recommendation letters, 5 years)
#         -> 4 flight schools, pass rate % + number of enquiries, 2011-2015
# =====================================================================================================================
U6_YEARS = [2011, 2012, 2013, 2014, 2015]
U6_SCHOOLS = ['Aurora', 'Borealis', 'Cirrus', 'Nimbus']
U6 = {   # school: (pass rates %, enquiries) per year
    'Aurora':   ([70, 70, 70, 75, 75], [700, 800, 900, 1000, 1300]),
    'Borealis': ([95, 85, 80, 90, 95], [900, 1000, 800, 1100, 1050]),
    'Cirrus':   ([80, 85, 85, 90, 80], [800, 900, 1000, 1200, 1100]),
    'Nimbus':   ([90, 80, 85, 70, 60], [1200, 1000, 900, 800, 500]),
}


def u6_svg():
    W, x0, yc = 900, 20, 110.0
    sub = [86.0, 106.0]                       # pass rate, enquiries
    gw = sum(sub)
    top, h1, h2, rh = 16, 48, 64, 52
    b = []
    y1, y2, y3 = top, top + h1, top + h1 + h2
    b.append(_r(x0, y2, yc, h2 + rh * 5, '#fff', INK, 1.5))
    b.append(_t(x0 + yc / 2, y2 + h2 / 2, 'Year', 19, INK, 'middle', 700))
    for k, s in enumerate(U6_SCHOOLS):
        gx = x0 + yc + k * gw
        b.append(_r(gx, y1, gw, h1, SOFT, INK, 1.5))
        b.append(_t(gx + gw / 2, y1 + h1 / 2, s, 21, INK, 'middle', 700))
        b.append(_r(gx, y2, sub[0], h2, '#fff', INK, 1.2))
        b.append(_tl(gx + sub[0] / 2, y2 + h2 / 2, ['Pass', 'rate (%)'], 16, INK, 'middle', 700))
        b.append(_r(gx + sub[0], y2, sub[1], h2, GRID, INK, 1.2))
        b.append(_tl(gx + sub[0] + sub[1] / 2, y2 + h2 / 2, ['Number of', 'enquiries'], 16, INK, 'middle', 700))
        rates, enq = U6[s]
        for i in range(5):
            y = y3 + i * rh
            b.append(_r(gx, y, sub[0], rh, '#fff', INK, 1.2))
            b.append(_t(gx + sub[0] / 2, y + rh / 2, rates[i], 20))
            b.append(_r(gx + sub[0], y, sub[1], rh, SOFT, INK, 1.2))
            b.append(_t(gx + sub[0] + sub[1] / 2, y + rh / 2, _n(enq[i]), 20))
    for i, yr in enumerate(U6_YEARS):
        y = y3 + i * rh
        b.append(_r(x0, y, yc, rh, '#fff', INK, 1.2))
        b.append(_t(x0 + yc / 2, y + rh / 2, yr, 20, INK, 'middle', 700))
    b.append(_r(x0 + yc, y1, 4 * gw, h1 + h2 + 5 * rh, 'none', INK, 2.5))
    return _svg(W, int(y3 + 5 * rh + 18), 'Flight schools: pass rates and enquiries 2011-2015', ''.join(b))


U6_INTRO = ('Study the table below, then answer the four questions that follow.\n'
            'The table below presents data on four flight schools that prepare students for the pilot licence exam: '
            'Aurora, Borealis, Cirrus and Nimbus.\n'
            'The data refer to the pass rate of each school and to the number of enquiries (people asking about studying '
            'there) that each school received in each of the years 2011-2015.\n'
            'The "pass rate" is the percentage of the students of the school who took the licence exam in that year and passed it.\n'
            'For example, in 2015 the Nimbus school received 500 enquiries and its pass rate was 60%.\n' + NOTE)

# =====================================================================================================================
# UNIT 7 · stacked column chart + employment bars (book: research team, salary / articles / researchers 1990-1998)
#         -> photographers of a nature magazine, salary / photos published / photographers 2010-2018
# =====================================================================================================================
U7_YEARS = list(range(2010, 2019))
U7_SAL = dict(zip(U7_YEARS, [2000, 2250, 1750, 2250, 2500, 2250, 2750, 2500, 3000]))
U7_PH = dict(zip(U7_YEARS, [40, 35, 45, 50, 60, 60, 55, 70, 65]))
U7_LANES = [   # (name, start, end) - start/end as year fractions: 2012.5 = the middle of 2012; end 2012 = start of 2012
    [('Adam', 2010, 2012), ('Dor', 2012, 2018), ('Shira', 2018, 2019)],
    [('Bella', 2010, 2011), ('Eden', 2011, 2019)],
    [('Carmel', 2010, 2014), ('Gil', 2014, 2017), ('Lia', 2017.5, 2019)],
    [('Nadav', 2012.5, 2015), ('Rotem', 2015, 2017), ('Yoni', 2017, 2019)],
]


def u7_staff(year):
    """photographers who worked during the whole of the given year"""
    return sorted(n for lane in U7_LANES for (n, a, e) in lane if a <= year and e >= year + 1)


def u7_svg():
    W, H = 900, 930
    X0, X1 = 215.0, 885.0
    cw = (X1 - X0) / 9
    def X(yr): return X0 + (yr - 2010) * cw
    b = []
    # ---- upper panel: salary (1,000-3,000, broken axis)
    UT, UB = 110.0, 400.0
    def ys(v): return 375.0 - (v - 1000) * (375.0 - 125.0) / 2000.0
    b.append(_tl(95, 50, ['Average monthly', 'salary per', 'photographer'], 18, INK, 'middle', 700))
    b.append(_t(95, 98, '(shekels)', 16, MUTED))
    for v in range(1000, 3001, 250):
        b.append(_l(X0, ys(v), X1, ys(v), '#B9C7CC', 1, '5 4'))
        b.append(_l(X0 - 8, ys(v), X0, ys(v), INK, 1.5))
        b.append(_t(X0 - 14, ys(v), _n(v), 16, INK, 'end'))
    for yr in U7_YEARS:
        b.append(_r(X(yr), ys(U7_SAL[yr]), cw, UB - ys(U7_SAL[yr]), SOFT, TEAL, 1.6))
    b.append(_l(X0 - 12, 392, X0 + 6, 384, INK, 2))            # axis break
    b.append(_l(X0 - 12, 398, X0 + 6, 390, INK, 2))
    # ---- middle panel: photos (0-80)
    MB = 660.0
    def yp(v): return MB - v * 3.0
    b.append(_tl(95, 420, ['Number of', 'photos published'], 18, INK, 'middle', 700))
    for v in range(0, 81, 10):
        b.append(_l(X0, yp(v), X1, yp(v), '#B9C7CC', 1, '5 4'))
        b.append(_l(X0 - 8, yp(v), X0, yp(v), INK, 1.5))
        b.append(_t(X0 - 14, yp(v), v, 16, INK, 'end'))
    for yr in U7_YEARS:
        b.append(_r(X(yr), yp(U7_PH[yr]), cw, MB - yp(U7_PH[yr]), MID, TEAL, 1.6))
    b.append(_l(X0, UB, X1, UB, INK, 1.5))
    b.append(_l(X0, MB, X1, MB, INK, 1.5))
    # ---- year strip
    b.append(_r(X0, MB, X1 - X0, 44, '#fff', INK, 1.5))
    for yr in U7_YEARS:
        b.append(_t(X(yr) + cw / 2, MB + 22, yr, 18, INK, 'middle', 700))
    # ---- employment lanes
    LT = MB + 56
    for i, lane in enumerate(U7_LANES):
        y = LT + i * 40
        for (nm, a, e) in lane:
            b.append(_r(X(a) + 1, y, (e - a) * cw - 2, 30, '#fff', INK, 1.6))
            b.append(_t((X(a) + X(e)) / 2, y + 15, nm, 17))
    YB = LT + 4 * 40 + 6
    b.append(_r(X0, YB, X1 - X0, 40, '#fff', INK, 1.5))
    for yr in U7_YEARS:
        b.append(_t(X(yr) + cw / 2, YB + 20, yr, 18, INK, 'middle', 700))
    b.append(_t(X0 - 14, YB + 20, 'Year', 18, INK, 'end', 700))
    b.append(_t(X0 - 14, LT + 80, 'Photographers', 17, INK, 'end', 700))
    # column separators through the whole chart
    for k in range(10):
        x = X0 + k * cw
        b.append(_l(x, UT - 10, x, YB + 40, INK, 1.1))
    return _svg(W, H, 'Magazine photographers 2010-2018: salary, photos and employment', ''.join(b))


U7_INTRO = ('Study the graph below, then answer the four questions that follow.\n'
            'The graph describes the work of the photographers employed by a nature magazine, whose main job is taking '
            'photographs for the magazine.\n'
            'The graph is divided into three parts:\n'
            'Each bar in the bottom part of the graph represents the period of employment of one photographer: the left end '
            'of the bar marks the start of the employment, and the right end marks its end. At any time, at most four '
            'photographers work for the magazine.\n'
            'The columns in the middle part of the graph represent the total number of photos published by the '
            "magazine's photographers in each of the years.\n"
            'The columns in the upper part of the graph represent the average monthly salary per photographer in each of the years.\n'
            'For example: at the start of 2011 Bella left the staff, and Eden joined the staff in her place. In 2011 the '
            'photographers published 35 photos, and the average monthly salary per photographer in that year was 2,250 shekels.\n'
            + NOTE)

# =====================================================================================================================
# UNIT 8 · score table (book: quiz, 6 topics, 5 men A-E + 7 women F-L, +1 / -1)
#         -> puzzle championship, 6 categories, 5 players of Team North (A-E) + 7 of Team South (F-L)
# =====================================================================================================================
U8_CATS = ['Logic', 'Words', 'Numbers', 'Maps', 'Memory', 'Riddles']
U8_PLAYERS = list('ABCDEFGHIJKL')
U8_NORTH = set('ABCDE')
U8 = {   # Logic, Words, Numbers, Maps, Memory, Riddles
    'A': [2, -1, 25, 5, 8, 0],
    'B': [3, 1, 5, 2, 2, 3],
    'C': [-2, -3, 10, 1, 3, 0],
    'D': [4, 0, 5, 6, 8, 2],
    'E': [5, -2, 10, 7, 9, 0],
    'F': [5, -1, 25, 4, 6, 3],
    'G': [3, 2, 5, 3, -1, 2],
    'H': [6, -2, 10, 8, 8, 4],
    'I': [6, -1, 20, 6, 6, 3],
    'J': [1, -1, 0, 3, 3, 0],
    'K': [6, 1, 15, 9, 12, 5],
    'L': [-3, 3, 30, 9, 10, 1],
}


def u8_svg():
    W = 900
    gx, gw, px, pw = 20.0, 150.0, 170.0, 70.0
    cx0 = px + pw
    cw = (880.0 - cx0) / 6
    top, h1, h2, rh = 14, 46, 44, 40
    b = []
    y2, y3 = top + h1, top + h1 + h2
    b.append(_r(gx, top, gw + pw, h1 + h2, SOFT, INK, 1.5))
    b.append(_t(gx + (gw + pw) / 2, top + (h1 + h2) / 2, 'Players', 22, INK, 'middle', 700))
    b.append(_r(cx0, top, 6 * cw, h1, '#fff', INK, 1.5))
    b.append(_t(cx0 + 3 * cw, top + h1 / 2, 'Puzzle categories', 22, INK, 'middle', 700))
    for k, c in enumerate(U8_CATS):
        b.append(_r(cx0 + k * cw, y2, cw, h2, '#fff', INK, 1.2))
        b.append(_t(cx0 + k * cw + cw / 2, y2 + h2 / 2, c, 19, INK, 'middle', 700))
    for i, p in enumerate(U8_PLAYERS):
        y = y3 + i * rh
        b.append(_r(px, y, pw, rh, GRID, INK, 1.2))
        b.append(_t(px + pw / 2, y + rh / 2, p, 20, INK, 'middle', 700))
        for k, v in enumerate(U8[p]):
            b.append(_r(cx0 + k * cw, y, cw, rh, '#fff', INK, 1.2))
            b.append(_t(cx0 + k * cw + cw / 2, y + rh / 2, v, 20))
    b.append(_r(gx, y3, gw, 5 * rh, SOFT, INK, 1.5))
    b.append(_tl(gx + gw / 2, y3 + 2.5 * rh, ['Team', 'North'], 20, INK, 'middle', 700))
    b.append(_r(gx, y3 + 5 * rh, gw, 7 * rh, SOFT, INK, 1.5))
    b.append(_tl(gx + gw / 2, y3 + 8.5 * rh, ['Team', 'South'], 20, INK, 'middle', 700))
    b.append(_l(gx, y3 + 5 * rh, 880, y3 + 5 * rh, INK, 3))
    b.append(_r(gx, top, 880 - gx, h1 + h2 + 12 * rh, 'none', INK, 2.5))
    return _svg(W, int(y3 + 12 * rh + 16), 'Puzzle championship scores', ''.join(b))


U8_INTRO = ('Study the table below, then answer the four questions that follow.\n'
            'A puzzle championship was held among several players.\n'
            'In the championship, puzzles were presented in six categories: Logic, Words, Numbers, Maps, Memory and Riddles.\n'
            '12 players competed in the championship: 5 players of Team North (marked in the table by the letters A to E) '
            'and 7 players of Team South (marked in the table by the letters F to L).\n'
            "A player's score in a certain category is the total number of points he collected in this category: a correctly "
            'solved puzzle earned the player one point, and a wrong solution cost him one point (a skipped puzzle did not change '
            "the player's score).\n"
            'The table shows the score of each of the players in each of the categories of the championship.\n'
            'For example: the letter I marks a player of Team South. The score she received in the Riddles category is 3.\n'
            + NOTE)

# =====================================================================================================================
# UNIT 9 · grid table, each cell split by a diagonal (book: machines by teeth on gear A / gear B: count + power)
#         -> wall tiles in a store by height / width (cm): number of tiles + price of one tile
# =====================================================================================================================
U9_SIZES = [10, 15, 20, 30, 40, 60]
U9 = {   # (height, width): (number of tiles in the store, price of one tile in shekels); missing = no such tiles
    (10, 10): (18, 12), (10, 15): (20, 14), (10, 20): (15, 16), (10, 30): (12, 18), (10, 40): (10, 22), (10, 60): (6, 30),
    (15, 10): (10, 15), (15, 15): (16, 12), (15, 30): (9, 20), (15, 40): (8, 24), (15, 60): (5, 28),
    (20, 15): (7, 26), (20, 20): (9, 12), (20, 30): (11, 22), (20, 60): (4, 35),
    (30, 15): (6, 18), (30, 40): (5, 30),
    (40, 10): (8, 20), (40, 20): (3, 30),
    (60, 10): (1, 25), (60, 15): (1, 32), (60, 30): (1, 40), (60, 60): (1, 12),
}


def u9_cell(x, y, w, h, cell, size=21, small=None):
    b = [_r(x, y, w, h, '#fff', INK, 1.3)]
    if cell is None:
        b.append(_l(x + w / 2 - 14, y + h / 2, x + w / 2 + 14, y + h / 2, INK, 2.2))
        return ''.join(b)
    n, p = cell
    b.append(_l(x + 4, y + h - 4, x + w - 4, y + 4, INK, 1.2))
    b.append(_t(x + 8, y + 18, n, size, INK, 'start', 700))
    b.append(_t(x + w - 8, y + h - 16, p, size, MUTED, 'end', 400))
    return ''.join(b)


def u9_svg():
    W, H = 900, 620
    gx, gy, cw, ch = 170.0, 140.0, 86.0, 72.0
    b = []
    b.append(_t(gx + 3 * cw, 50, 'Width of the tile (cm)', 22, INK, 'middle', 700))
    b.append(_t(40, gy + 3 * ch + 20, 'Height of the tile (cm)', 22, INK, 'middle', 700, -90))
    for k, w in enumerate(U9_SIZES):
        b.append(_r(gx + k * cw, gy - 64, cw, 64, GRID, INK, 1.3))
        b.append(_t(gx + k * cw + cw / 2, gy - 32, w, 22, INK, 'middle', 700))
    for i, hgt in enumerate(U9_SIZES):
        b.append(_r(gx - 90, gy + i * ch, 90, ch, GRID, INK, 1.3))
        b.append(_t(gx - 45, gy + i * ch + ch / 2, hgt, 22, INK, 'middle', 700))
        for k, w in enumerate(U9_SIZES):
            b.append(u9_cell(gx + k * cw, gy + i * ch, cw, ch, U9.get((hgt, w))))
    b.append(_r(gx - 90, gy - 64, 90, 64, '#fff', INK, 1.3))
    # legend
    lx, ly, lw, lh = 720.0, 170.0, 165.0, 150.0
    b.append(_t(lx, ly - 22, 'Key:', 20, INK, 'start', 700))
    b.append(_r(lx, ly, lw, lh, '#fff', INK, 1.5))
    b.append(_l(lx + 4, ly + lh - 4, lx + lw - 4, ly + 4, INK, 1.2))
    b.append(_tl(lx + 8, ly + 34, ['Number of', 'tiles in', 'the store'], 15, INK, 'start', 700))
    b.append(_tl(lx + lw - 8, ly + lh - 34, ['Price of', 'one tile', '(shekels)'], 15, MUTED, 'end', 400))
    return _svg(W, H, 'Wall tiles by height and width', ''.join(b))


U9_INTRO = ('Study the table below, then answer the four questions that follow.\n'
            'The table below presents data on the wall tiles sold in a certain store.\n'
            'Every tile in the store is a rectangle with a height and a width. The type of each tile is determined by its '
            'height and its width (in cm).\n'
            'Each cell of the table shows the number of tiles of the corresponding type in the store, and the price (in shekels) '
            'of one tile of that type (see the key).\n'
            'If the store has no tiles of a certain type, this is indicated by the sign \u2014 in the corresponding place in the table.\n'
            'For example: the store has no tiles 20 cm high and 10 cm wide. The store has 11 tiles 20 cm high and 30 cm wide; '
            'the price of each such tile is 22 shekels.\n' + NOTE)

# =====================================================================================================================
# UNIT 10 · table with a follow-up triangle (book: components produced / good / installed in robots in each year)
#          -> plant nursery: seedlings grown / healthy / healthy seedlings sold in each year, 2016-2020
# =====================================================================================================================
U10_YEARS = [2016, 2017, 2018, 2019, 2020]
U10_GROWN = dict(zip(U10_YEARS, [2000, 1800, 1500, 1600, 1250]))
U10_HEALTHY = dict(zip(U10_YEARS, [900, 1080, 870, 1040, 700]))
U10_SOLD = {   # year grown: {year sold: number of healthy seedlings sold}
    2016: {2016: 500, 2017: 220, 2018: 80, 2019: 30, 2020: 10},
    2017: {2017: 700, 2018: 350, 2019: 0, 2020: 30},
    2018: {2018: 400, 2019: 180, 2020: 150},
    2019: {2019: 420, 2020: 300},
    2020: {2020: 330},
}


def u10_svg():
    W = 900
    x0, c0, c1, c2 = 20.0, 110.0, 145.0, 145.0
    cs = (880.0 - x0 - c0 - c1 - c2) / 5
    top, h1, h2, rh = 14, 48, 44, 50
    b = []
    xs = x0 + c0 + c1 + c2
    b.append(_r(x0, top, c0, h1 + h2, '#fff', INK, 1.5))
    b.append(_tl(x0 + c0 / 2, top + (h1 + h2) / 2, ['Year', 'grown'], 19, INK, 'middle', 700))
    b.append(_r(x0 + c0, top, c1, h1 + h2, SOFT, INK, 1.5))
    b.append(_tl(x0 + c0 + c1 / 2, top + (h1 + h2) / 2, ['Number of', 'seedlings', 'grown'], 18, INK, 'middle', 700))
    b.append(_r(x0 + c0 + c1, top, c2, h1 + h2, SOFT, INK, 1.5))
    b.append(_tl(x0 + c0 + c1 + c2 / 2, top + (h1 + h2) / 2, ['Number of', 'healthy', 'seedlings'], 18, INK, 'middle', 700))
    b.append(_r(xs, top, 5 * cs, h1, GRID, INK, 1.5))
    b.append(_tl(xs + 2.5 * cs, top + h1 / 2, ['Number of healthy seedlings sold in the year'], 19, INK, 'middle', 700))
    for k, yr in enumerate(U10_YEARS):
        b.append(_r(xs + k * cs, top + h1, cs, h2, GRID, INK, 1.2))
        b.append(_t(xs + k * cs + cs / 2, top + h1 + h2 / 2, yr, 19, INK, 'middle', 700))
    y3 = top + h1 + h2
    for i, yr in enumerate(U10_YEARS):
        y = y3 + i * rh
        b.append(_r(x0, y, c0, rh, '#fff', INK, 1.2))
        b.append(_t(x0 + c0 / 2, y + rh / 2, yr, 20, INK, 'middle', 700))
        b.append(_r(x0 + c0, y, c1, rh, '#fff', INK, 1.2))
        b.append(_t(x0 + c0 + c1 / 2, y + rh / 2, _n(U10_GROWN[yr]), 20))
        b.append(_r(x0 + c0 + c1, y, c2, rh, '#fff', INK, 1.2))
        b.append(_t(x0 + c0 + c1 + c2 / 2, y + rh / 2, _n(U10_HEALTHY[yr]), 20))
        for k, ys in enumerate(U10_YEARS):
            b.append(_r(xs + k * cs, y, cs, rh, '#fff', INK, 1.2))
            if ys in U10_SOLD[yr]:
                b.append(_t(xs + k * cs + cs / 2, y + rh / 2, _n(U10_SOLD[yr][ys]), 20))
    b.append(_r(x0, top, 880 - x0, h1 + h2 + 5 * rh, 'none', INK, 2.5))
    b.append(_l(xs, top, xs, y3 + 5 * rh, INK, 2.5))
    return _svg(W, int(y3 + 5 * rh + 16), 'Plant nursery seedlings 2016-2020', ''.join(b))


U10_INTRO = ('Study the table below, then answer the four questions that follow.\n'
            'A certain plant nursery grows seedlings. The table below presents data on the seedlings grown in the nursery '
            'in the years 2016-2020.\n'
            'For each year, the table shows the number of seedlings grown in that year and how many of them were healthy.\n'
            'In addition, the table shows the number of healthy seedlings from each year of growing that were sold in each of '
            'the years 2016-2020 (each seedling is sold only once).\n'
            'For example: in 2019 the nursery grew 1,600 seedlings, of which 1,040 were healthy. Of these healthy seedlings, '
            '420 were sold in 2019 and 300 were sold in 2020.\n' + NOTE)


# =====================================================================================================================
# questions
# =====================================================================================================================
QUESTIONS = {}
FIG = {}
TITLES = {6: 'Flight schools', 7: 'Magazine photographers', 8: 'Puzzle championship', 9: 'Wall tiles', 10: 'Plant nursery'}
KEYS = {6: [3, 4, 1, 2], 7: [3, 2, 3, 1], 8: [4, 4, 3, 3], 9: [4, 2, 4, 4], 10: [1, 2, 1, 3]}


def _plain(s):
    s = str(s)
    for _ in range(3):
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'\1/\2', s)
    s = re.sub(r'\\text\{([^{}]*)\}', r'\1', s)
    s = s.replace('\\cdot', '·').replace('\\times', '×').replace('\\approx', '≈').replace('\\ne', '≠')
    s = s.replace('\\le', '≤').replace('\\ge', '≥').replace('\\,', ' ').replace('\\%', '%').replace('\\', '')
    return rich_plain(s)


def mk(unit, n, intro, stem, choices, key, steps, fig):
    qid = 'chp%02d-q%d' % (unit, n)
    assert key == KEYS[unit][n - 1], (qid, key)
    full = intro + '\n\n' + stem
    title = 'Unit %d \u00b7 %s' % (unit, TITLES[unit])
    q = _q(qid, T52, _plain(full), [_plain(c) for c in choices], key, '',
           dict(subject='charts', trustRank=1, reviewFlag=False,
                source='Charts practice book unit %d q%d (original set modelled on it)' % (unit, n), setTitle=title))
    q.update(stem=_plain(full), stemRich=full, stemHtml=rich_html(full),
             choices=[_plain(c) for c in choices], choicesRich=list(choices), choicesHtml=[rich_html(c) for c in choices],
             explanation=list(steps), answerHtml=''.join('<p>%s</p>' % rich_html(e) for e in steps),
             work=[], workText=[], methods=[dict(title='Worked solution', steps=list(steps), work=[], independent=False, board=[])],
             navLabel=_plain(stem.replace('\n', ' '))[:120], questionVisual={'type': 'geometry', 'svg': fig},
             setIntro=intro)
    QUESTIONS[qid] = q
    FIG[qid] = fig


S6, S7, S8, S9, S10 = u6_svg(), u7_svg(), u8_svg(), u9_svg(), u10_svg()

# ---------------- Unit 6 (book key 3 4 1 2) ----------------
mk(6, 1, U6_INTRO, 'At which of the schools was the average number of enquiries per year the greatest?',
   ['Aurora', 'Borealis', 'Cirrus', 'Nimbus'], 3, [
    r'Average per year $= \frac{\text{total enquiries}}{\text{number of years}}$. All four schools have the same 5 years, '
    'so the school with the greatest average is simply the school with the greatest total. No need to divide.',
    'Way 1 - cancel equal values: every school had one year with 800, one with 900 and one with 1,000 enquiries. '
    'Cross them out and compare only the two numbers left in each column: Aurora 700 + 1,300 = 2,000; '
    'Borealis 1,100 + 1,050 = 2,150; Cirrus 1,200 + 1,100 = 2,300; Nimbus 1,200 + 500 = 1,700. Cirrus is the greatest.',
    'Way 2 - order of magnitude: Nimbus leads in 2011 (1,200), but in the other years it falls far behind, so its lead '
    'in one year is not a real "threat". Year by year, Cirrus is the school that is usually at the top.',
    'Way 3 - compute (drop the zeros): Aurora 7 + 8 + 9 + 10 + 13 = 47; Borealis 9 + 10 + 8 + 11 + 10.5 = 48.5; '
    'Cirrus 8 + 9 + 10 + 12 + 11 = 50; Nimbus 12 + 10 + 9 + 8 + 5 = 44 (hundreds). Answer: Cirrus.'], S6)

mk(6, 2, U6_INTRO, 'Which of the following statements is necessarily true?',
   ['Every school whose pass rate rose from 2011 to 2012 continued to raise its pass rate from year to year until 2015',
    'The school with the largest number of students who took the licence exam in 2015 was Aurora',
    'Every school received more than 4,500 enquiries in the years 2011-2015',
    'From 2012 to 2013, the pass rate fell at only one of the schools'], 4, [
    'Check each statement against the table.',
    'Statement (1): only Cirrus rose from 2011 to 2012 (80% to 85%). But in 2013 it stayed at 85% and in 2015 it fell '
    'from 90% to 80%, so it did not keep rising. Rejected.',
    'Statement (2): the table has no data at all about the number of students who took the exam at each school '
    '(only pass rates and enquiries), so this cannot be concluded. Rejected.',
    'Statement (3): this is the total we found in the previous question. If you did not compute it there, scan for the '
    'school that looks smallest - Nimbus: 1,200 + 1,000 + 900 + 800 + 500 = 4,400, which is less than 4,500. Rejected.',
    'Tip: three statements are rejected, so (4) can be marked without checking. For completeness: from 2012 to 2013 '
    'only Borealis fell (85% to 80%); Aurora and Cirrus stayed the same and Nimbus rose (80% to 85%). Statement (4) is correct.'], S6)

mk(6, 3, U6_INTRO, 'At the Aurora school the same number of students take the licence exam every year.\n'
   'Over the 5 years, what percentage of all the Aurora students who took the licence exam passed it?',
   ['72%', '72.5%', '73%', '74%'], 1, [
    'We want the pass rate of Aurora over all 5 years together. Since the same number of students take the exam every '
    'year, every year has the same weight, and the answer is the ordinary average of the 5 pass rates.',
    'Way 1 - see-saw (weighted average): in 3 years the rate was 70% and in 2 years it was 75%. The groups are 3 : 2, '
    'so the distances from the average are the other way round, 2 : 3. The gap from 70 to 75 is 5 = 5 "jumps" of 1; '
    'the average is 2 jumps above 70, that is 72%.',
    r'Way 2 - the average formula: $\frac{70 + 70 + 70 + 75 + 75}{5} = \frac{360}{5} = 72$, so 72%.',
    'Trap: 72.5% is the middle of 70 and 75 - it ignores that 70% appears in more years than 75%.'], S6)

mk(6, 4, U6_INTRO, r'At which of the schools was the ratio $\frac{\text{pass rate}}{\text{number of enquiries}}$ '
   'the greatest in 2011?', ['Aurora', 'Borealis', 'Cirrus', 'Nimbus'], 2, [
    r'In 2011 the ratios are: Aurora $\frac{70}{700}$, Borealis $\frac{95}{900}$, Cirrus $\frac{80}{800}$, Nimbus $\frac{90}{1{,}200}$.',
    r'Way 1 - compare with a familiar fraction: we only need the greatest, not exact values. Compare each with $\frac{1}{10}$: '
    r'$\frac{70}{700} = \frac{1}{10}$ and $\frac{80}{800} = \frac{1}{10}$ exactly; $\frac{95}{900} > \frac{1}{10}$ '
    r'(the numerator is more than a tenth of the denominator); $\frac{90}{1{,}200} < \frac{1}{10}$. Only Borealis is above $\frac{1}{10}$.',
    r'Way 2 - semi-finals and final: $\frac{90}{1{,}200} < \frac{90}{900} < \frac{95}{900}$, so Nimbus loses to Borealis; '
    r'$\frac{70}{700} = \frac{80}{800} = \frac{1}{10} < \frac{95}{900}$. Borealis has the greatest ratio.'], S6)

# ---------------- Unit 7 (book key 3 2 3 1) ----------------
mk(7, 1, U7_INTRO, 'In 2010, the total number of photos published by Adam and Carmel was equal to the number of photos '
   'published by Bella.\nHow many photos did Bella publish in 2010?', ['10', '40', '20', '30'], 3, [
    'In the bottom part of the graph, look at the 2010 column: three photographers worked that year - Adam, Bella and Carmel.',
    'Adam and Carmel together published as many photos as Bella, so Bella published half of all the photos of 2010 '
    '(and Adam and Carmel the other half).',
    'In the middle part, the 2010 column shows 40 photos. Half of 40 is 20.'], S7)

mk(7, 2, U7_INTRO, 'In how many of the years 2011-2018 did the number of photos published by the photographers rise '
   'compared with the previous year, while the average monthly salary per photographer fell compared with the previous year?',
   ['1', '2', '3', '0'], 2, [
    'Scan smartly: first go over the upper columns (salary) only and find the years in which the salary fell compared '
    'with the year before: 2012 (2,250 to 1,750), 2015 (2,500 to 2,250) and 2017 (2,750 to 2,500).',
    'Now check only these three years in the middle columns (photos): 2012 - 35 to 45, a rise; 2015 - 60 to 60, no '
    'change (not a rise); 2017 - 55 to 70, a rise.',
    'So there are exactly 2 such years (2012 and 2017).'], S7)

mk(7, 3, U7_INTRO, 'It is known that in 2016 Rotem earned 1,250 shekels a month.\n'
   'What was the average monthly salary of the other photographers who worked in 2016?',
   ['1,500 shekels', '2,750 shekels', '3,250 shekels', '3,000 shekels'], 3, [
    'In the bottom part, four photographers worked in 2016: Dor, Eden, Gil and Rotem. In the upper part, the average '
    'monthly salary of the four in 2016 was 2,750 shekels.',
    'Way 1 - order of magnitude: Rotem earned much less than the average of 2,750, so he "pulls" the average down. '
    'To balance him, the other three must be above 2,750, so 1,500 and 2,750 are ruled out. To choose between 3,250 and 3,000, use way 2 or way 3.',
    'Way 2 - see-saw: 1 photographer against 3, so the distances are 3 : 1. From 1,250 to 2,750 is 1,500 = 3 jumps of 500. '
    'The others are 1 jump above the average: 2,750 + 500 = 3,250 shekels.',
    r'Way 3 - formula: total of the four $= 4 \cdot 2{,}750 = 11{,}000$. Without Rotem: $11{,}000 - 1{,}250 = 9{,}750$. '
    r'Average of the three $= \frac{9{,}750}{3} = 3{,}250$ shekels.'], S7)

mk(7, 4, U7_INTRO, 'Between which two consecutive years was the greatest increase, in percent, in the average monthly '
   'salary per photographer?',
   ['Between 2012 and 2013', 'Between 2013 and 2014', 'Between 2015 and 2016', 'Between 2017 and 2018'], 1, [
    'A percent increase depends on two things: the larger the increase, the larger the percent; and the smaller the '
    'starting value, the larger the percent. (A raise of 5 shekels on 100 is 5%; on 10 it is 50%.)',
    'Read the increases: 2012-2013 from 1,750 to 2,250 (+500); 2013-2014 from 2,250 to 2,500 (+250); '
    '2015-2016 from 2,250 to 2,750 (+500); 2017-2018 from 2,500 to 3,000 (+500).',
    'Three choices have the same increase of 500 (two grid lines). The one that starts from the lowest salary is '
    '2012-2013 (from 1,750), so it has the greatest percent increase (about 29%, against 22% and 20%).'], S7)

# ---------------- Unit 8 (book key 4 4 3 3) ----------------
mk(8, 1, U8_INTRO, 'A player\'s "overall score" in the championship is the sum of the scores he received in the six categories.\n'
   'How many players have an overall score less than 20?', ['1', '2', '3', '4'], 4, [
    'We only need to know whether each total is below 20 - estimate, and compute only when it is close.',
    'A: 25 in Numbers alone; the small minus in Words does not bring it below 20. Not below 20.',
    'B: close, so compute: 3 + 1 + 5 + 2 + 2 + 3 = 16. Below 20.',
    'C: 10 + 1 + 3 = 14 points, and the other categories only lower it (-2, -3). Below 20.',
    'D: 4 + 5 + 6 + 8 + 2 = 25 already. Not below 20. E: 10 + 7 + 9 + 5 = 31 minus 2. Not below 20.',
    'F: 25 in Numbers; losing 1 point in Words does not matter. Not below 20.',
    'G: compute: 3 + 2 + 5 + 3 - 1 + 2 = 14. Below 20.',
    'H, I: many points in almost every category (H 34, I 40). J: very few points - 1 - 1 + 0 + 3 + 3 + 0 = 6. Below 20.',
    'We already have 4 players below 20 (B, C, G, J) and 4 is the largest choice, so we can stop (K and L are clearly above 20).'], S8)

mk(8, 2, U8_INTRO, 'Out of the players who received a score of 0 in the Riddles category, one player is chosen at random.\n'
   'What is the probability that this player is from Team North?',
   [r'$\frac{1}{3}$', r'$\frac{1}{2}$', r'$\frac{2}{3}$', r'$\frac{3}{4}$'], 4, [
    'The chosen player is picked only from those with 0 in Riddles. Look at the Riddles column: A, C, E and J have 0. '
    'So there are 4 possible players.',
    r'Of them, A, C and E are from Team North (letters A to E). Probability $= \frac{3}{4}$.'], S8)

mk(8, 3, U8_INTRO, 'A "cut score" in a certain category is a number such that half of the players received in this category '
   'a score higher than it or equal to it, and half of the players received a score lower than it.\n'
   'Which of the following numbers is a cut score in the Memory category?', ['4', '6', '7', '10'], 3, [
    'There are 12 players, so a cut score must have exactly 6 players with that score or higher, and 6 players below it.',
    'Way 1 - plug in the choices, starting from a middle one: 6 - the players with 6 or more are A, D, E, F, H, I, K, L '
    '(8 players). Too many, so 6 is too small; 4 (smaller still) is out too.',
    '7 - the players with 7 or more are A, D, E, H, K, L: exactly 6, and the other 6 are below 7. 7 is a cut score.',
    'For completeness, 10 - only K and L (2 players). Rejected.',
    'Way 2 - understanding: sort the Memory scores: -1, 2, 3, 3, 6, 6 | 8, 8, 8, 9, 10, 12. The cut score must be above '
    'the 6 lowest (above 6) and not above the 6 highest (at most 8): it can be 7 or 8. Only 7 is a choice.'], S8)

mk(8, 4, U8_INTRO, 'One of the players received the highest score of the championship in 4 of the categories.\n'
   'Who is this player?', ['H', 'I', 'K', 'L'], 3, [
    'Way 1 - scan the table: mark the highest score in each column: Logic 6 (H, I, K), Words 3 (L), Numbers 30 (L), '
    'Maps 9 (K, L), Memory 12 (K), Riddles 5 (K). Then count per row: K has the highest score in Logic, Maps, Memory and Riddles - 4 categories.',
    'Way 2 - plug in the choices: H - highest in Logic, but not in Words, Numbers or Maps; already it cannot reach 4 '
    'categories (only 2 are left). Rejected. I - the same: highest only in Logic among the first four. Rejected.',
    'K - Logic (6) yes, Words (1) no, Numbers (15) no, Maps (9) yes, Memory (12) yes, Riddles (5) yes: 4 categories. Correct.',
    'For completeness, L - highest in Words, Numbers and Maps only: 3 categories. Rejected.'], S8)

# ---------------- Unit 9 (book key 4 2 4 4) ----------------
mk(9, 1, U9_INTRO, 'How many of the tiles in the store have a price higher than 25 shekels?', ['29', '30', '31', '32'], 4, [
    'The price is the number in the lower part of each cell. Scan the table for prices higher than 25 (26 and up - a price '
    'of exactly 25 does not count), and add the numbers of tiles in the upper part of those cells.',
    'The cells are: 10 x 60: 6 tiles (30); 15 x 60: 5 tiles (28); 20 x 15: 7 tiles (26); 20 x 60: 4 tiles (35); '
    '30 x 40: 5 tiles (30); 40 x 20: 3 tiles (30); 60 x 15: 1 tile (32); 60 x 30: 1 tile (40) (height x width).',
    '6 + 5 + 7 + 4 + 5 + 3 + 1 + 1 = 32.',
    'Trap: the tile 60 x 10 costs exactly 25 shekels and does not count; counting it gives 33.'], S9)

mk(9, 2, U9_INTRO, 'The store has no tile whose height is ____ cm and whose width is equal to this number or greater than it.',
   ['30', '40', '60', '20'], 2, [
    'Plug in each choice: go to the row of that height, and check the cells whose width is equal to the height or greater '
    '(to the right of the diagonal of equal sizes).',
    '(1) height 30: the cell 30 x 40 has 5 tiles. Rejected.',
    '(2) height 40: the cells 40 x 40 and 40 x 60 both show \u2014. There is no such tile. Correct.',
    'Tip: once the correct answer is found there is no need to go on. For completeness: (3) height 60: the cell 60 x 60 '
    'has 1 tile. Rejected. (4) height 20: the cells 20 x 20, 20 x 30 and 20 x 60 have tiles. Rejected.'], S9)

mk(9, 3, U9_INTRO, 'One of the tiles in the store broke, and it turned out that it was the only tile of its type in the store.\n'
   'Which of the following statements about this tile is necessarily true?',
   ['Its price is 25 shekels', 'Its price is 12 shekels', 'Its width is 10 cm', 'Its height is 60 cm'], 4, [
    'For a statement to be necessarily true, it must hold for every tile type that has only one tile in the store.',
    'Find all the cells with the number 1 in the upper part: 60 x 10, 60 x 15, 60 x 30 and 60 x 60 (height x width).',
    'Their prices are different (25, 32, 40, 12) and their widths are different, so (1), (2) and (3) are not necessarily true.',
    'What they all have in common is the height: 60 cm. Answer (4).'], S9)

mk(9, 4, U9_INTRO, 'What is the total price (in shekels) of all the tiles in the store whose height is equal to their width?',
   ['48', '216', '336', '528'], 4, [
    'Tiles whose height equals their width are the "square" types - the cells on the diagonal of the table: '
    '10 x 10, 15 x 15, 20 x 20, 30 x 30, 40 x 40, 60 x 60.',
    '10 x 10: 18 tiles at 12 shekels = 216. 15 x 15: 16 tiles at 12 = 192. 20 x 20: 9 tiles at 12 = 108. '
    '30 x 30 and 40 x 40: no tiles. 60 x 60: 1 tile at 12 = 12.',
    '216 + 192 + 108 + 12 = 528 shekels.',
    'Shortcut: every square type costs 12 shekels a tile, so count the tiles (18 + 16 + 9 + 1 = 44) and multiply once: '
    r'$44 \cdot 12 = 528$.',
    'Traps: 48 adds the prices of the types without the number of tiles (4 x 12); 216 counts only the 10 x 10 tiles.'], S9)

# ---------------- Unit 10 (book key 1 2 1 3) ----------------
mk(10, 1, U10_INTRO, r'In ____, exactly $\frac{1}{4}$ of all the seedlings grown in the nursery in that year were sold in that same year.',
   ['2016', '2017', '2019', '2020'], 1, [
    'For each year, compare the number of seedlings grown (second column) with the number sold in the same year (the '
    'cell in the "sold" part under the same year).',
    r'2016: 2,000 seedlings were grown and 500 of them were sold in 2016: $\frac{500}{2{,}000} = \frac{1}{4}$. Correct.',
    r'For completeness: 2017 $\frac{700}{1{,}800}$, 2019 $\frac{420}{1{,}600}$, 2020 $\frac{330}{1{,}250}$ - none of them is exactly $\frac{1}{4}$.',
    'Careful to use the seedlings grown, not the healthy seedlings.'], S10)

mk(10, 2, U10_INTRO, 'From which year of growing were no healthy seedlings left unsold at the end of 2020?',
   ['2016', '2017', '2018', '2019'], 2, [
    'No healthy seedlings are left from a year if all its healthy seedlings were sold: the sum of its row in the '
    '"sold" part must equal its number of healthy seedlings.',
    '(2) 2017: 700 + 350 + 0 + 30 = 1,080 = the number of healthy seedlings. None are left. Correct.',
    'Tip: once the correct answer is found there is no need to go on. For completeness: (1) 2016: 500 + 220 + 80 + 30 + 10 = 840, '
    'less than 900. (3) 2018: 400 + 180 + 150 = 730, less than 870. (4) 2019: 420 + 300 = 720, less than 1,040.'], S10)

mk(10, 3, U10_INTRO, 'Of the following years, in which year of growing was the percentage of healthy seedlings (out of the '
   'seedlings grown in that year) the lowest?', ['2016', '2018', '2019', '2020'], 1, [
    'We need healthy seedlings divided by seedlings grown in each year. There is no need to compute exactly - compare with one half.',
    '2016: 900 healthy out of 2,000 - less than half (half of 2,000 is 1,000).',
    '2018: 870 out of 1,500 - more than half (750). 2019: 1,040 out of 1,600 - more than half (800). '
    '2020: 700 out of 1,250 - more than half (625).',
    'Only 2016 is below one half, so it has the lowest percentage (45%).'], S10)

mk(10, 4, U10_INTRO, 'According to the table, how many healthy seedlings were sold two years or more after the year in which '
   'they were grown?', ['70', '230', '300', '1,350'], 3, [
    'In each row, take only the cells that are at least two years to the right of the year of growing.',
    'Grown in 2016: sold in 2018, 2019 and 2020: 80 + 30 + 10 = 120.',
    'Grown in 2017: sold in 2019 and 2020: 0 + 30 = 30.',
    'Grown in 2018: sold in 2020: 150. (Seedlings grown in 2019 and 2020 had no time for that.)',
    '120 + 30 + 150 = 300.',
    'Traps: 230 counts only "exactly two years after"; 70 counts only "more than two years after".'], S10)


# =====================================================================================================================
# verification: recompute every answer from the data
# =====================================================================================================================
def _verify():
    from fractions import Fraction as Fr
    ok = {}

    def one(qid, flags):
        key = QUESTIONS[qid]['correct'][0]
        assert sum(bool(f) for f in flags) == 1 and flags[key], (qid, flags)
        ok[qid] = True

    def vals(qid, got):
        cs = [c.replace(',', '').replace('%', '').replace(' shekels', '') for c in QUESTIONS[qid]['choices']]
        one(qid, [abs(float(Fr(c)) - float(got)) < 1e-9 for c in cs])

    # unit 6
    tot = {s: sum(U6[s][1]) for s in U6_SCHOOLS}
    best = max(tot, key=tot.get)
    assert list(tot.values()).count(tot[best]) == 1
    one('chp06-q1', [s == best for s in U6_SCHOOLS])
    r = {s: U6[s][0] for s in U6_SCHOOLS}
    s1 = all(all(r[s][i + 1] > r[s][i] for i in range(1, 4)) for s in U6_SCHOOLS if r[s][1] > r[s][0])
    s2 = False                                           # no data on the number of students
    s3 = all(tot[s] > 4500 for s in U6_SCHOOLS)
    s4 = sum(r[s][2] < r[s][1] for s in U6_SCHOOLS) == 1
    one('chp06-q2', [s1, s2, s3, s4])
    vals('chp06-q3', Fr(sum(U6['Aurora'][0]), 5))
    ratio = {s: Fr(U6[s][0][0], U6[s][1][0]) for s in U6_SCHOOLS}
    bm = max(ratio.values()); assert list(ratio.values()).count(bm) == 1
    one('chp06-q4', [ratio[s] == bm for s in U6_SCHOOLS])
    # unit 7
    assert all(len([1 for lane in U7_LANES for (n, a, e) in lane if a <= t < e]) <= 4 for t in [2010 + k / 4.0 for k in range(36)])
    st = u7_staff(2010); assert st == ['Adam', 'Bella', 'Carmel'], st
    vals('chp07-q1', Fr(U7_PH[2010], 2))
    cnt = sum(1 for y in U7_YEARS[1:] if U7_PH[y] > U7_PH[y - 1] and U7_SAL[y] < U7_SAL[y - 1])
    vals('chp07-q2', cnt)
    st = u7_staff(2016); assert st == ['Dor', 'Eden', 'Gil', 'Rotem'], st
    assert all(e <= 2016 or a >= 2017 or n in st for lane in U7_LANES for (n, a, e) in lane)   # nobody part-time in 2016
    vals('chp07-q3', Fr(4 * U7_SAL[2016] - 1250, 3))
    pairs = [(2012, 2013), (2013, 2014), (2015, 2016), (2017, 2018)]
    inc = [Fr(U7_SAL[b] - U7_SAL[a], U7_SAL[a]) for a, b in pairs]
    one('chp07-q4', [v == max(inc) and inc.count(v) == 1 for v in inc])
    # unit 8
    tot8 = {p: sum(U8[p]) for p in U8_PLAYERS}
    vals('chp08-q1', sum(1 for p in U8_PLAYERS if tot8[p] < 20))
    zeros = [p for p in U8_PLAYERS if U8[p][5] == 0]
    one('chp08-q2', [Fr(c.replace('$\\frac{', '').replace('}{', '/').replace('}$', '')) == Fr(sum(p in U8_NORTH for p in zeros), len(zeros))
                     for c in QUESTIONS['chp08-q2']['choicesRich']])
    mem = [U8[p][4] for p in U8_PLAYERS]
    one('chp08-q3', [sum(v >= int(c) for v in mem) == 6 and sum(v < int(c) for v in mem) == 6 for c in QUESTIONS['chp08-q3']['choices']])
    top = [max(U8[p][k] for p in U8_PLAYERS) for k in range(6)]
    nt = {p: sum(U8[p][k] == top[k] for k in range(6)) for p in U8_PLAYERS}
    assert [p for p in U8_PLAYERS if nt[p] >= 4] == ['K'], nt
    one('chp08-q4', [nt[c] == 4 for c in QUESTIONS['chp08-q4']['choices']])
    # unit 9
    vals('chp09-q1', sum(n for (n, p) in U9.values() if p > 25))
    one('chp09-q2', [not any((int(c), w) in U9 for w in U9_SIZES if w >= int(c)) for c in QUESTIONS['chp09-q2']['choices']])
    singles = [(k, v) for k, v in U9.items() if v[0] == 1]
    f = [all(v[1] == 25 for k, v in singles), all(v[1] == 12 for k, v in singles),
         all(k[1] == 10 for k, v in singles), all(k[0] == 60 for k, v in singles)]
    one('chp09-q3', f)
    vals('chp09-q4', sum(n * p for (h, w), (n, p) in U9.items() if h == w))
    # unit 10
    for y in U10_YEARS: assert sum(U10_SOLD[y].values()) <= U10_HEALTHY[y] <= U10_GROWN[y]
    one('chp10-q1', [Fr(U10_SOLD[int(c)][int(c)], U10_GROWN[int(c)]) == Fr(1, 4) for c in QUESTIONS['chp10-q1']['choices']])
    one('chp10-q2', [sum(U10_SOLD[int(c)].values()) == U10_HEALTHY[int(c)] for c in QUESTIONS['chp10-q2']['choices']])
    pc = {y: Fr(U10_HEALTHY[y], U10_GROWN[y]) for y in U10_YEARS}
    ch = [int(c) for c in QUESTIONS['chp10-q3']['choices']]
    one('chp10-q3', [pc[y] == min(pc[c] for c in ch) for y in ch])
    vals('chp10-q4', sum(v for y in U10_YEARS for ys, v in U10_SOLD[y].items() if ys - y >= 2))
    assert len(ok) == len(QUESTIONS) == 20, (len(ok), len(QUESTIONS))
    for qid, q in QUESTIONS.items():
        u = int(qid[3:5]); n = int(qid[-1])
        assert q['correct'][0] + 1 == KEYS[u][n - 1]


_verify()

MODULES = []
PRACTICE = {52: ['chp%02d-q%d' % (u, n) for u in range(6, 11) for n in range(1, 5)]}
MEMORY = []
