# Quantitative Reasoning · Topic 52 · Charts & Tables — SELF-PRACTICE, units 1-5 of the charts practice book.
# Source: charts practice book (charts_src/practice_book), unit N = chart page b(2N+6) + questions page b(2N+7),
# key on b048, written solutions b050-b071. The book's sets are real NITE exam sets, so every set here is ORIGINAL:
# a new story and new data, but the same chart type, the same number and kind of questions with the same tricks,
# and the correct answer in the same position as the book key. _verify() (run at import) recomputes every answer from
# the data below and asserts that exactly one choice is right, at the key position.
#   unit 1  book: two scatter charts of letters (2 travel agencies, trip price by length, 4 countries)   key 3 1 4 3
#           here: two language schools, course price by number of lessons, 4 languages
#   unit 2  book: work hours / training hours plane cut into diagonal stress bands, 16 numbered people  key 2 3 4 4
#           here: water / fertilizer per week for 16 numbered houseplants, diagonal leaf-damage bands
#   unit 3  book: a delivery van's altitude by distance, delivery squares, round-hour dots, 8 segments  key 2 3 1 4 3
#           here: a one-day hike, altitude by distance, rest-stop squares, round-hour dots, 8 segments
#   unit 4  book: table of call-minute / text prices of 4 phone companies by quarter                    key 3 1 1 1 3
#           here: table of riding-minute / unlock prices of 4 bike-sharing companies by quarter
#   unit 5  book: sea temperature line, line style = wave height, weather icons per half month          key 2 4 2 2
#           here: river water level line, line style = current speed, weather icons per half month
import math
import re

from vbank import _q
from math_api import rich_html

T52 = 52
INK, TEAL, AMBER, SOFT, GRID, MUTED = '#0F172A', '#0F766E', '#F5A524', '#E6F4F1', '#D8E6E3', '#5B6B7A'
FONT = "font-family=\"'Helvetica Neue',Helvetica,Arial,sans-serif\""

QUESTIONS = {}
ORDER = []


# =====================================================================================================================
# svg helpers
# =====================================================================================================================
def _svg(W, H, label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s"><title>%s</title>'
            '<rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W, H, label, label, W, H, body))


def _t(x, y, s, size=18, color=INK, anchor='middle', weight=400, rot=None):
    tr = ' transform="rotate(%d %.1f %.1f)"' % (rot, x, y) if rot else ''
    s = str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle" fill="%s" %s font-size="%d" '
            'font-weight="%d"%s>%s</text>' % (x, y, anchor, color, FONT, size, weight, tr, s))


def _l(x1, y1, x2, y2, color=INK, w=1.5, dash=None):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, color, w, ' stroke-dasharray="%s"' % dash if dash else ''))


def _r(x, y, w, h, fill='none', stroke=INK, sw=1.5, rx=0):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (x, y, w, h, rx, fill, stroke, sw))


def _c(x, y, r, fill=INK, stroke='none', sw=0):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fill, stroke, sw)


def _poly(pts, fill, stroke='none', sw=0):
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        ' '.join('%.1f,%.1f' % p for p in pts), fill, stroke, sw)


def _path(pts, color=INK, w=2.5, cap='round'):
    d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"/>'
            % (d, color, w, cap))


def pchip(knots):
    """monotone cubic through the knots (extrema only at knots, no overshoot) -> f(x)."""
    xs = [float(a) for a, b in knots]; ys = [float(b) for a, b in knots]
    n = len(xs); h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    dl = [(ys[i + 1] - ys[i]) / h[i] for i in range(n - 1)]
    m = [0.0] * n
    m[0] = dl[0]; m[-1] = dl[-1]
    for i in range(1, n - 1):
        if dl[i - 1] * dl[i] <= 0: m[i] = 0.0
        else:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / dl[i - 1] + w2 / dl[i])
    if n > 2:
        if dl[0] * dl[1] <= 0: m[0] = 0.0
        if dl[-1] * dl[-2] <= 0: m[-1] = 0.0

    def f(x):
        i = max(0, min(n - 2, max(k for k in range(n - 1) if xs[k] <= x) if x >= xs[0] else 0))
        t = (x - xs[i]) / h[i]
        h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
        return h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1]
    return f


def crossings(f, a, b, level, step=0.001):
    """number of times the graph of f on [a, b] reaches the level (a touch counts once)."""
    n, prev, x, on = 0, f(a) - level, a, False
    if abs(prev) < 1e-9: n, on = 1, True
    while x < b - 1e-12:
        x = min(b, x + step); cur = f(x) - level
        if abs(cur) < 1e-9:
            if not on: n += 1
            on = True
        else:
            if not on and prev * cur < 0: n += 1
            on = False
        prev = cur
    return n


# =====================================================================================================================
# question builder
# =====================================================================================================================
def _plain(s):
    s = re.sub(r'(\d)\\frac', r'\1 \\frac', str(s))
    s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'\1/\2', s)
    s = s.replace('{,}', ',').replace('\\cdot', '·').replace('\\times', '×').replace('\\approx', '≈')
    s = s.replace('\\le', '≤').replace('\\ge', '≥').replace('\\,', ' ').replace('$', '')
    s = re.sub(r'\\text\{([^{}]*)\}', r'\1', s)
    return re.sub(r'[ \t]+', ' ', s).strip()


LEAD = 'Study the chart below, then answer the questions that follow.\n'
LEAD_T = 'Study the table below, then answer the questions that follow.\n'
NOTE = '\nNote: In answering each question, disregard the information appearing in the other questions.'


def mk(unit, n, intro, title, stem, choices, key, steps, fig):
    qid = 'chp%02d-q%d' % (unit, n)
    full = intro + '\n\n' + stem
    q = _q(qid, T52, _plain(full), [_plain(c) for c in choices], key, '',
           dict(subject='charts', trustRank=1, reviewFlag=False,
                source='Charts practice book unit %d q%d (original set modelled on it)' % (unit, n),
                setTitle='Unit %d · %s' % (unit, title)))
    q.update(stem=_plain(full), stemRich=full, stemHtml=rich_html(full),
             choices=[_plain(c) for c in choices], choicesRich=list(choices), choicesHtml=[rich_html(c) for c in choices],
             explanation=list(steps), answerHtml=''.join('<p>%s</p>' % rich_html(e) for e in steps),
             work=[], workText=[], methods=[dict(title='Worked solution', steps=list(steps), work=[], independent=False, board=[])],
             navLabel=_plain(stem.replace('\n', ' '))[:120], questionVisual={'type': 'geometry', 'svg': fig},
             setIntro=intro)
    QUESTIONS[qid] = q; ORDER.append(qid)
    return qid


# =====================================================================================================================
# UNIT 1 · two scatter charts of letters: course price by number of lessons, two language schools
# =====================================================================================================================
U1_LANG = [('F', 'French', INK), ('G', 'German', TEAL), ('P', 'Portuguese', '#8A5A00'), ('S', 'Spanish', '#2F6B9A')]
U1_LEN = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
U1 = {   # school -> language letter -> prices (dollars) for 5, 10, ..., 50 lessons
    'Lingo': {'F': [300, 500, 800, 1000, 1100, 1600, 1400, 1700, 1800, 2000],
              'G': [400, 600, 900, 800, 1200, 1300, 1500, 1800, 1500, 1900],
              'P': [500, 700, 700, 900, 1300, 1400, 1700, 1600, 1900, 1800],
              'S': [200, 400, 600, 1100, 1000, 1200, 1300, 1500, 1600, 1700]},
    'Verba': {'F': [400, 600, 700, 1000, 1200, 1300, 1500, 1600, 1700, 1900],
              'G': [300, 500, 800, 900, 1000, 1400, 1300, 1700, 1800, 2000],
              'P': [600, 400, 900, 1100, 1300, 1200, 1600, 1500, 2000, 1700],
              'S': [500, 700, 600, 800, 1100, 1500, 1400, 1800, 1900, 1600]},
}


def u1p(school, lang, n): return U1[school][lang][U1_LEN.index(n)]


def unit1_svg():
    W, H = 900, 1100
    o = []
    # legend
    o.append(_r(140, 14, 620, 40, '#ffffff', INK, 1.4, 4))
    o.append(_t(160, 34, 'Legend:', 18, INK, 'start', 700))
    for k, (ch, name, col) in enumerate(U1_LANG):
        x = 250 + k * 130
        o.append(_t(x, 34, ch, 20, col, 'middle', 800)); o.append(_t(x + 14, 34, '– ' + name, 17, INK, 'start'))
    X0, X1 = 120.0, 860.0
    def px(n): return X0 + (X1 - X0) * n / 52.5
    for school, top in (('Lingo', 80), ('Verba', 600)):
        YT, YB = top + 40.0, top + 440.0
        def py(v): return YB - (YB - YT) * v / 2000.0
        o.append(_t(X1, top + 12, '"%s" language school' % school, 21, TEAL, 'end', 800))
        for v in range(0, 2001, 100):
            y = py(v)
            if v % 200 == 0:
                o.append(_l(X0, y, X1, y, GRID, 1.3, '5 4'))
                o.append(_t(X0 - 10, y, '{:,}'.format(v), 16, INK, 'end'))
            else:
                o.append(_l(X0, y, X1, y, '#EDF3F1', 1, '2 5'))
        for n in U1_LEN:
            o.append(_l(px(n), YT, px(n), YB, GRID, 1.2, '5 4'))
            o.append(_t(px(n), YB + 20, str(n), 17))
        o.append(_l(X0, YB, X1 + 10, YB, INK, 2)); o.append(_l(X0, YB, X0, YT - 22, INK, 2))
        o.append(_poly([(X1 + 18, YB), (X1 + 6, YB - 6), (X1 + 6, YB + 6)], INK))
        o.append(_poly([(X0, YT - 30), (X0 - 6, YT - 18), (X0 + 6, YT - 18)], INK))
        o.append(_t(X0 - 14, top + 6, 'Price', 17, INK, 'end', 700))
        o.append(_t(X0 - 14, top + 25, '(dollars)', 15, INK, 'end', 700))
        o.append(_t((X0 + X1) / 2, YB + 46, 'Number of lessons in the course', 18, INK, 'middle', 700))
        for ch, name, col in U1_LANG:
            for n in U1_LEN:
                o.append(_t(px(n), py(u1p(school, ch, n)) + 1, ch, 19, col, 'middle', 800))
    return _svg(W, H, 'Two scatter charts: course price in dollars by number of lessons, for four languages, '
                      'at the Lingo and Verba language schools', ''.join(o))


U1_INTRO = (LEAD +
            'Two language schools, "Lingo" and "Verba", offer courses in four different languages: French, German, Portuguese '
            'and Spanish (see legend). The charts show the prices of the courses (in dollars) that each school offers, '
            'according to the number of lessons in the course.\n'
            'For example, a 25-lesson French course at the "Lingo" school costs 1,100 dollars.' + NOTE)
U1_T = 'Language Schools'


def build_unit1():
    S = unit1_svg()
    mk(1, 1, U1_INTRO, U1_T,
       'The cost of the textbooks in a Spanish course is 35% of the price of the course.\n'
       'What is the cost (in dollars) of the textbooks in a 20-lesson Spanish course at the "Verba" school?',
       ['210', '245', '280', '385'], 3, [
           'First find the price of the course: in the "Verba" chart (the lower one), go up from 20 lessons to the letter S. '
           'It is at 800, so the course costs 800 dollars.',
           'The textbooks cost 35% of 800: $\\frac{35}{100}\\cdot 800 = 35\\cdot 8 = 280$.',
           'Another way: 10% of 800 is 80, so 30% is 240; 5% is half of 10%, which is 40. So 35% = 240 + 40 = 280.',
           'Traps: 385 is 35% of 1,100 (the S at 20 lessons in the "Lingo" chart); 210 and 245 come from the S at 15 or at 10 lessons.'],
       S)
    mk(1, 2, U1_INTRO, U1_T,
       'Dana took a 45-lesson German course, and then a 50-lesson Portuguese course (not necessarily at the same school).\n'
       'How many dollars, at the least, did Dana pay?',
       ['3,200', '3,300', '3,500', '3,600'], 1, [
           '"At the least" = for each course, take the school where it is cheaper.',
           '45-lesson German course (the letter G above 45): "Lingo" 1,500, "Verba" 1,800. The cheaper one is 1,500.',
           '50-lesson Portuguese course (the letter P above 50): "Lingo" 1,800, "Verba" 1,700. The cheaper one is 1,700.',
           'Least total: 1,500 + 1,700 = 3,200 dollars.',
           'Traps: both courses at "Lingo" = 3,300; both at "Verba" = 3,500; the more expensive school each time = 3,600.'],
       S)
    mk(1, 3, U1_INTRO, U1_T,
       'In which of the following courses at the "Lingo" school is the average price per lesson the lowest?',
       ['A 20-lesson French course', 'A 20-lesson Spanish course', 'A 30-lesson French course', 'A 30-lesson Spanish course'], 4, [
           'Average price per lesson = the price of the course divided by the number of lessons.',
           'Shortcut: choices (1) and (2) have the same number of lessons (20), and so do (3) and (4) (30). When the number of '
           'lessons is the same, the cheaper course also has the lower price per lesson, so compare the prices only.',
           '(1) or (2): in the "Lingo" chart at 20 lessons, F is at 1,000 and S is at 1,100. French is cheaper, so (2) is out.',
           '(3) or (4): at 30 lessons, F is at 1,600 and S is at 1,200. Spanish is cheaper, so (3) is out.',
           'Now compute the two that are left: (1) $\\frac{1{,}000}{20}=50$ dollars per lesson; (4) $\\frac{1{,}200}{30}=40$ dollars per lesson.',
           'The lowest is the 30-lesson Spanish course.'],
       S)
    mk(1, 4, U1_INTRO, U1_T,
       'Anna, Ben and Carmen enrolled in Portuguese courses at the "Lingo" school.\n'
       'Anna enrolled in one 40-lesson course,\n'
       'Ben enrolled in two 20-lesson courses,\n'
       'and Carmen enrolled in a 25-lesson course and a 15-lesson course.\n'
       'Which of the three paid the highest price per lesson (on average)?',
       ['Anna', 'Ben', 'Carmen', 'All three paid the same price'], 3, [
           'Each of the three takes 40 lessons in all (40, 20 + 20, 25 + 15). With the same number of lessons, you do not need '
           'the price per lesson: whoever paid the most in total also paid the most per lesson.',
           'Anna: the P above 40 is at 1,600 dollars.',
           'Ben: the P above 20 is at 900, and he paid for two courses: 2 · 900 = 1,800 dollars.',
           'Carmen: the P above 25 is at 1,300 and the P above 15 is at 700: 1,300 + 700 = 2,000 dollars.',
           'Carmen paid the most, so she paid the highest price per lesson.'],
       S)


# =====================================================================================================================
# UNIT 2 · regions chart: water / fertilizer per week, diagonal leaf-damage bands, 16 numbered plants
# =====================================================================================================================
U2_X, U2_Y = (300, 900), (0, 120)
U2_CUTS = [230, 320, 420, 530, 620, 720]            # on d = water − 2.5 · fertilizer
U2_LEVELS = ['Medium', 'Low', 'Very low', 'Low', 'Medium', 'High', 'Very high']
U2_FILL = {'Very low': '#EEF8F5', 'Low': '#C5E5DC', 'Medium': '#FBE7B2', 'High': '#F3BD84', 'Very high': '#DA8A5E'}
U2_P = {1: (350, 20), 2: (350, 80), 3: (400, 20), 4: (400, 60), 5: (450, 100), 6: (500, 60), 7: (550, 30), 8: (600, 60),
        9: (700, 80), 10: (650, 40), 11: (650, 80), 12: (650, 110), 13: (750, 60), 14: (750, 100), 15: (900, 30), 16: (900, 100)}


def u2d(x, y): return x - 2.5 * y


def u2band(x, y):
    d = u2d(x, y)
    k = sum(d > c for c in U2_CUTS)
    return k


def u2level(p): return U2_LEVELS[u2band(*U2_P[p])]


U2_BOX = (110.0, 830.0, 580.0, 100.0)                 # X0, X1, YB, YT


def u2px(x): return U2_BOX[0] + (U2_BOX[1] - U2_BOX[0]) * (x - 300) / 600.0
def u2py(y): return U2_BOX[2] - (U2_BOX[2] - U2_BOX[3]) * y / 120.0


def _clip(poly, a, b, c):
    """keep the part of the polygon with a·x + b·y <= c."""
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0: out.append(p)
        if fp * fq < 0:
            t = fp / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def unit2_svg():
    W, H = 900, 660
    o = []
    rect = [(300, 0), (900, 0), (900, 120), (300, 120)]
    cuts = [-1e9] + U2_CUTS + [1e9]
    for k, lev in enumerate(U2_LEVELS):
        poly = _clip(_clip(rect, -1, 2.5, -cuts[k]), 1, -2.5, cuts[k + 1])     # cuts[k] <= x − 2.5y <= cuts[k+1]
        if poly: o.append(_poly([(u2px(x), u2py(y)) for x, y in poly], U2_FILL[lev]))
    X0, X1, YB, YT = U2_BOX
    for v in range(0, 121, 10):
        o.append(_l(X0, u2py(v), X1, u2py(v), '#9DB3AE', 0.8, '3 4'))
        o.append(_t(X0 - 10, u2py(v), str(v), 16, INK, 'end'))
    for v in range(300, 901, 50):
        o.append(_l(u2px(v), YT, u2px(v), YB, '#9DB3AE', 0.8, '3 4'))
        o.append(_t(u2px(v), YB + 20, str(v), 16))
    for c in U2_CUTS:                                    # band borders
        seg = _clip(_clip(rect, -1, 2.5, -c + 1e-6), 1, -2.5, c + 1e-6)
        pts = [(x, y) for x, y in seg if abs(u2d(x, y) - c) < 1e-3]
        if len(pts) >= 2: o.append(_l(u2px(pts[0][0]), u2py(pts[0][1]), u2px(pts[-1][0]), u2py(pts[-1][1]), INK, 1.8))
    o.append(_r(X0, YT, X1 - X0, YB - YT, 'none', INK, 1.6))
    o.append(_l(X0, YB, X1 + 25, YB, INK, 2)); o.append(_l(X0, YB, X0, YT - 30, INK, 2))
    o.append(_poly([(X1 + 33, YB), (X1 + 21, YB - 6), (X1 + 21, YB + 6)], INK))
    o.append(_poly([(X0, YT - 38), (X0 - 6, YT - 26), (X0 + 6, YT - 26)], INK))
    o.append(_t(X0 + 14, 44, 'Fertilizer solution per week (ml)', 18, INK, 'start', 700))
    o.append(_t((X0 + X1) / 2, YB + 52, 'Water per week (ml)', 18, INK, 'middle', 700))
    # band labels, along the middle of each band
    rot = -int(round(math.degrees(math.atan2(u2py(0) - u2py(1), u2px(2.5) - u2px(0)))))
    spots = {0: 95, 1: 100, 2: 45, 3: 20, 4: 94, 5: 50, 6: 14}      # fertilizer level at which each label sits
    for k, lev in enumerate(U2_LEVELS):
        lo, hi = cuts[k], cuts[k + 1]
        if k == 0: mid = 120
        elif k == len(U2_LEVELS) - 1: mid = 800
        else: mid = (lo + hi) / 2.0
        y = spots[k]; x = mid + 2.5 * y
        cx, cy = u2px(x), u2py(y)
        w = 10 * len(lev) + 16
        o.append('<g transform="rotate(%d %.1f %.1f)">%s%s</g>' % (
            rot, cx, cy, _r(cx - w / 2, cy - 12, w, 24, '#ffffff', INK, 1, 4), _t(cx, cy + 1, lev, 16, INK, 'middle', 700)))
    for p, (x, y) in U2_P.items():
        o.append(_c(u2px(x), u2py(y), 5.5, INK))
        o.append(_t(u2px(x) + 9, u2py(y) - 13, str(p), 18, INK, 'start', 800))
    return _svg(W, H, 'Regions chart: water and fertilizer per week for 16 numbered plants, with diagonal bands of leaf-damage level',
                ''.join(o))


U2_INTRO = (LEAD +
            'The chart shows data from a study on the relation between the amounts of water and of fertilizer solution that a '
            'houseplant receives each week and the level of damage to its leaves.\n'
            'The chart is divided into areas painted in different colours. The colour of an area and the label in it show the '
            'level of leaf damage: very low, low, medium, high or very high.\n'
            'The dots on the chart show the data of the 16 plants that took part in the study, numbered 1 to 16.\n'
            'For example, plant number 6 receives 500 ml of water and 60 ml of fertilizer solution per week, and the level of '
            'damage to its leaves is very low.' + NOTE)
U2_T = 'Houseplants'


def build_unit2():
    S = unit2_svg()
    mk(2, 1, U2_INTRO, U2_T,
       'The plants in the study were divided into groups according to the level of damage to their leaves.\n'
       'In the group with the largest number of plants, the level of leaf damage is ______ .',
       ['very low', 'low', 'medium', 'high'], 2, [
           'The question asks in which colour of area there are the most dots. Count the dots in each level.',
           'Careful: the level "low" appears in two separate strips (on both sides of "very low"), and so does "medium". '
           'Count both strips of each level.',
           'Low: plants 7, 8, 9, 11 and 14 in the right-hand strip, and plants 1 and 4 in the left-hand strip: 7 plants.',
           'Medium: plants 2 and 5 on the left, 10 and 13 on the right: 4 plants. Very low: plants 3, 6 and 12: 3 plants. '
           'High: plant 16 only.',
           'The largest group is the one with a low level of leaf damage.'],
       S)
    mk(2, 2, U2_INTRO, U2_T,
       'Some of the plants in the study could lower the level of damage to their leaves by receiving less water each week '
       '(without changing the amount of fertilizer solution they receive).\n'
       'According to the chart, which of the following plants would need the greatest reduction in its weekly amount of '
       'water in order to lower its level of leaf damage from medium to low?',
       ['Plant 10', 'Plant 5', 'Plant 13', 'Plant 12'], 3, [
           'Less water = moving to the LEFT, along a horizontal line (the fertilizer stays the same, so the dot does not go up or down).',
           'Plant 10 (650, 40) is in a medium area. Moving left, it reaches the low strip after a short way (a little more than 20 ml).',
           'Plant 5 is also in a medium area, but in the left-hand one. To reach the low strip it must move RIGHT, which means '
           'more water, not less. Out.',
           'Plant 13 (750, 60) is in the right-hand medium area. Moving left, it reaches the low strip only after about 70 ml '
           '(at a little less than 680 ml).',
           'Plant 12 is in the very low area, not in a medium one. Out.',
           'Plant 13 needs the greatest reduction.'],
       S)
    mk(2, 3, U2_INTRO, U2_T,
       'How many of the plants in the study whose level of leaf damage is low or very low receive more water per week than plant 8?',
       ['8', '6', '3', '4'], 4, [
           'Plant 8 receives 600 ml of water. Draw a vertical line at 600: plants that receive more water are to the right of it.',
           'To the right of the line there are 8 plants: 9, 10, 11, 12, 13, 14, 15, 16. Keep only those in a low or very low area.',
           'Low: plants 9, 11 and 14. Very low: plant 12. Plants 10 and 13 are medium, 16 is high and 15 is very high.',
           'In all: 4 plants.',
           'Traps: 8 counts all the plants to the right of the line; 3 forgets the "very low" plant.'],
       S)
    mk(2, 4, U2_INTRO, U2_T,
       'What is the greatest difference between the amount of water (in ml) that a plant in the study receives per week and '
       'the amount of fertilizer solution (in ml) that it receives per week?',
       ['270', '330', '800', '870'], 4, [
           'Difference = water − fertilizer. For it to be as large as possible, look for a plant with a lot of water (far to the '
           'right) and little fertilizer (low down): the bottom-right corner of the chart.',
           'Plant 15 receives 900 ml of water (the most) and only 30 ml of fertilizer: 900 − 30 = 870.',
           'Plant 16 also receives 900 ml of water, but 100 ml of fertilizer: 800. 270 is the SMALLEST difference (plant 2: 350 − 80).'],
       S)


# =====================================================================================================================
# UNIT 3 · line graph: altitude of a hiking group by distance, rest stops, round-hour dots, 8 segments
# =====================================================================================================================
U3_KNOTS = [(0, 450), (1.5, 400), (3, 350), (4, 250), (8, 250), (10, 100), (11, 200), (12, 300), (14, 550), (15.5, 450),
            (17, 650), (19, 850), (20, 950), (21, 850), (22.5, 600), (24, 350)]
U3F = pchip(U3_KNOTS)
U3_HOURS = [0, 3, 6.5, 9.5, 12.5, 16, 19, 21, 24]                       # position at 08:00, 09:00, ..., 16:00
U3_STOPS = [1.5, 4.5, 5.5, 7.5, 11, 13.5, 15, 17, 18, 20, 22, 23]       # rest stops (distance, km)
U3_START = 8


def u3alt(x): return U3F(x)


def unit3_svg():
    W, H = 900, 640
    X0, X1, YB, YT = 95.0, 805.0, 545.0, 150.0
    def px(x): return X0 + (X1 - X0) * x / 24.0
    def py(v): return YB - (YB - YT) * v / 1000.0
    o = []
    o.append(_r(300, 14, 300, 70, '#ffffff', INK, 1.4, 4))
    o.append(_t(318, 30, 'Legend:', 16, INK, 'start', 700))
    o.append(_r(320, 44, 14, 14, '#ffffff', INK, 1.6)); o.append(_c(327, 51, 2.2, INK))
    o.append(_t(345, 51, 'Rest stop of the group', 16, INK, 'start'))
    o.append(_c(327, 71, 5, INK)); o.append(_t(345, 71, 'Position of the group at a round hour', 16, INK, 'start'))
    for v in range(0, 1001, 50):
        o.append(_l(X0, py(v), X1, py(v), GRID if v % 100 == 0 else '#EDF3F1', 1.2 if v % 100 == 0 else 1, '5 4'))
        if v % 100 == 0:
            o.append(_t(X0 - 12, py(v), str(v), 16, INK, 'end', 700))
            o.append(_t(X1 + 12, py(v), str(v), 16, INK, 'start', 700))
    for x in range(0, 25):
        o.append(_l(px(x), YT, px(x), YB, GRID if x % 2 == 0 else '#EDF3F1', 1.1, '5 4'))
        o.append(_l(px(x), YB, px(x), YB + (8 if x % 2 == 0 else 5), INK, 1.3))
        if x % 2 == 0: o.append(_t(px(x), YB + 22, str(x), 16, INK, 'middle', 700))
    o.append(_l(X0, YB, X1, YB, INK, 2))
    for xa, anchor in ((X0, 'end'), (X1, 'start')):
        o.append(_l(xa, YB, xa, YT - 35, INK, 2)); o.append(_poly([(xa, YT - 45), (xa - 6, YT - 32), (xa + 6, YT - 32)], INK))
        o.append(_t(xa, YT - 70, 'Altitude', 16, INK, 'middle', 700)); o.append(_t(xa, YT - 53, '(metres)', 14, INK, 'middle', 700))
    o.append(_t((X0 + X1) / 2, YB + 55, 'Distance from the starting point (km)', 18, INK, 'middle', 700))
    pts = [(px(k / 50.0), py(U3F(k / 50.0))) for k in range(0, 24 * 50 + 1)]
    o.append(_path(pts, INK, 2.2))
    for s in U3_STOPS:
        x, y = px(s), py(U3F(s))
        o.append(_r(x - 7, y - 9, 14, 18, '#ffffff', INK, 1.6)); o.append(_c(x, y, 2.2, INK))
    for h in U3_HOURS: o.append(_c(px(h), py(U3F(h)), 5.5, INK))
    lab = {1: (1.4, 520), 2: (5.0, 335), 3: (8.0, 335), 4: (10.6, 45), 5: (13.8, 650), 6: (17.9, 560), 7: (20.0, 1040), 8: (23.5, 640)}
    for sg, (x, alt) in lab.items():
        cx, cy = px(x), py(alt)
        o.append(_c(cx, cy, 11, '#C9D3D9')); o.append(_t(cx, cy + 1, str(sg), 15, INK, 'middle', 800))
    return _svg(W, H, 'Line graph: altitude of a hiking group by distance from the starting point, with rest stops, '
                      'round-hour positions and 8 numbered hike segments', ''.join(o))


U3_INTRO = (LEAD +
            'The chart describes one day of hiking of a hiking group.\n'
            'The hike began at 08:00 and ended 8 hours later, at 16:00.\n'
            'The length of the trail from the starting point to the end point is 24 km.\n'
            'The graph shows the distance from the starting point and the altitude at which the group was located along the hike.\n'
            'The squares on the graph mark the rest stops of the group. The exact location of a rest stop is shown by the point '
            'in the centre of the square. The dots on the graph mark the position of the group at round hours (see legend).\n'
            'A "hike segment" is the part of the graph between two consecutive dots. The hike segments are numbered 1 to 8.\n'
            'For example: at 09:00, when the group finished hike segment 1, it was 3 km from the starting point, at an altitude '
            'of 350 metres. During hike segment 1 the group rested at a rest stop located 1.5 km from the starting point, at an '
            'altitude of 400 metres.' + NOTE)
U3_T = 'A Day Hike'


def build_unit3():
    S = unit3_svg()
    mk(3, 1, U3_INTRO, U3_T,
       'What is the difference in altitude between the highest rest stop and the lowest rest stop?',
       ['700 metres', '750 metres', '850 metres', '950 metres'], 2, [
           'Look only at the squares (rest stops), not at the whole graph.',
           'The highest square is at the top of the peak, 20 km from the start: 950 metres.',
           'The lowest square is on the climb out of the deep valley, 11 km from the start: 200 metres. '
           '(The bottom of the valley, 100 metres, is not a rest stop.)',
           'Difference: 950 − 200 = 750 metres.',
           'Traps: 850 = the highest point minus the lowest point of the whole graph; 700 = using the stops on the flat part '
           '(250 metres) as the lowest ones.'],
       S)
    mk(3, 2, U3_INTRO, U3_T,
       'The group hiked hike segment 5 between ______ and ______ .',
       ['10:00 ; 11:00', '11:00 ; 12:00', '12:00 ; 13:00', '13:00 ; 14:00'], 3, [
           'Each dot marks a round hour, and a hike segment lies between two consecutive dots, so every segment lasts exactly one hour.',
           'The hike began at 08:00: segment 1 is 08:00-09:00, segment 2 is 09:00-10:00, segment 3 is 10:00-11:00, '
           'segment 4 is 11:00-12:00, segment 5 is 12:00-13:00.',
           'Check from the end: the hike ended at 16:00, so segment 8 is 15:00-16:00, and going back, segment 5 is 12:00-13:00.'],
       S)
    mk(3, 3, U3_INTRO, U3_T,
       'Which of the following altitudes cannot be the altitude at which the group was located at 15:30?',
       ['300 metres', '450 metres', '600 metres', '800 metres'], 1, [
           '15:30 is between 15:00 and 16:00, which is the last hour of the hike: hike segment 8.',
           'Look at the altitudes in segment 8: it starts at 850 metres (the dot at 15:00, 21 km) and goes down to 350 metres '
           '(the end of the hike at 16:00).',
           'So at 15:30 the group was somewhere between 350 and 850 metres. 450, 600 and 800 are all possible.',
           '300 metres is lower than any point of segment 8, so it is impossible.'],
       S)
    mk(3, 4, U3_INTRO, U3_T,
       'What is the average number of rest stops per hike segment?',
       ['1', '2', '$1\\frac{1}{3}$', '$1\\frac{1}{2}$'], 4, [
           'Average = the total number of rest stops divided by the number of hike segments.',
           'Count the squares on the whole graph: 12 rest stops.',
           'There are 8 hike segments (numbered 1 to 8).',
           'Average: $\\frac{12}{8}=1\\frac{1}{2}$ rest stops per segment.',
           'Trap: dividing by the number of dots (9) gives $\\frac{12}{9}=1\\frac{1}{3}$. The dots are not the segments: 9 dots make 8 segments.'],
       S)
    mk(3, 5, U3_INTRO, U3_T,
       'During its hike, which of the following altitudes did the group reach the greatest number of times?',
       ['600 metres', '300 metres', '500 metres', '400 metres'], 3, [
           'The altitude is on the vertical axis. For each choice, draw a horizontal line at that altitude and count how many '
           'times the graph touches or crosses it.',
           '600 metres: on the long climb to the peak and on the way down at the end: 2 times.',
           '300 metres: on the way down to the flat part and on the climb out of the valley: 2 times.',
           '500 metres: on the climb to the small hill (550), on the way down from it (450), on the climb to the peak, and on '
           'the way down at the end: 4 times.',
           '400 metres: at the start, on the climb out of the valley and on the way down at the end: 3 times. '
           '(Between the small hill and the peak the graph stays above 450, so it does not reach 400 there.)',
           'The answer is 500 metres.',
           'Tip: look for the altitude band where the graph goes up and down the most (here, the small hill between 450 and 550).'],
       S)


# =====================================================================================================================
# UNIT 4 · table: prices (cents) per riding minute and per unlock, 4 bike-sharing companies, 4 quarters
# =====================================================================================================================
U4_CO = ['Pedal', 'Spin', 'Wheelo', 'Ryde']
U4 = {   # company -> (price per minute, price per unlock) for quarters 1-4, in cents
    'Pedal':  ([25, 20, 25, 30], [30, 30, 25, 30]),
    'Spin':   ([25, 30, 35, 25], [20, 0, 20, 20]),
    'Wheelo': ([20, 35, 30, 15], [20, 10, 20, 40]),
    'Ryde':   ([20, 25, 40, 35], [40, 20, 10, 10]),
}


def unit4_svg():
    W, H = 900, 500
    o = []
    x0, xs = 30.0, [30, 170, 360, 495, 630, 765, 870]      # company | item | Q1..Q4
    y0, hh, rh = 20.0, 46.0, 46.0
    o.append(_r(xs[0], y0, xs[-1] - xs[0], 2 * hh + 8 * rh, '#ffffff', INK, 2))
    o.append(_r(xs[2], y0, xs[-1] - xs[2], hh, SOFT, 'none', 0))
    o.append(_r(xs[2], y0 + hh, xs[-1] - xs[2], hh, SOFT, 'none', 0))
    o.append(_r(xs[0], y0, xs[1] - xs[0], 2 * hh, SOFT, 'none', 0))
    o.append(_t((xs[2] + xs[-1]) / 2, y0 + hh / 2, 'Price in cents', 20, INK, 'middle', 800))
    o.append(_t((xs[0] + xs[1]) / 2, y0 + hh, 'Company', 20, INK, 'middle', 800))
    for q in range(4):
        o.append(_t((xs[2 + q] + xs[3 + q]) / 2, y0 + 1.5 * hh, 'Quarter %d' % (q + 1), 18, INK, 'middle', 700))
    o.append(_l(xs[2], y0 + hh, xs[-1], y0 + hh, INK, 1.2))
    for x in xs[1:-1]:
        o.append(_l(x, y0 + (hh if x > xs[2] else 0), x, y0 + 2 * hh + 8 * rh, INK, 1.2))
    for k, co in enumerate(U4_CO):
        top = y0 + 2 * hh + 2 * k * rh
        o.append(_l(xs[0], top, xs[-1], top, INK, 2))
        o.append(_l(xs[1], top + rh, xs[-1], top + rh, INK, 1))
        o.append(_t((xs[0] + xs[1]) / 2, top + rh, co, 21, INK, 'middle', 800))
        for j, (name, vals) in enumerate((('Riding minute', U4[co][0]), ('Unlock', U4[co][1]))):
            yy = top + j * rh + rh / 2
            o.append(_t(xs[1] + 14, yy, name, 18, INK, 'start'))
            for q in range(4): o.append(_t((xs[2 + q] + xs[3 + q]) / 2, yy, str(vals[q]), 19))
    return _svg(W, H, 'Table: prices in cents per riding minute and per unlock at four bike-sharing companies, by quarter',
                ''.join(o))


U4_INTRO = (LEAD_T +
            'The table shows the prices of the services of four bike-sharing companies - Pedal, Spin, Wheelo and Ryde - which '
            'they charged their customers in a certain year.\n'
            'The year is divided into four quarters, and for each quarter the table shows the prices (in cents) that each '
            'company charged for one minute of riding (or part of a minute) and for unlocking a bike (once at the start of '
            'every ride).\n'
            'For example: in quarter 3 of the year, Wheelo charged its customers 30 cents per minute of riding and 20 cents '
            'per unlock.\n'
            '(100 cents = 1 dollar)' + NOTE)
U4_T = 'Bike-Sharing Prices'


def build_unit4():
    S = unit4_svg()
    mk(4, 1, U4_INTRO, U4_T,
       'Maya is a customer of Pedal. In a certain month of quarter 3, she made 40 rides, and she rode for a total of 200 minutes.\n'
       'How much did Maya pay that month (in dollars)?',
       ['50', '52', '60', '72'], 3, [
           'Maya is a customer of Pedal, and the month is in quarter 3: the Pedal column of quarter 3. The answer is asked in '
           'dollars, so change cents into dollars.',
           'In quarter 3, Pedal charged 25 cents per minute and 25 cents per unlock: 25 cents = $\\frac{1}{4}$ dollar each.',
           'She paid for 200 minutes and for 40 unlocks (one unlock per ride): $\\frac{1}{4}\\cdot 200+\\frac{1}{4}\\cdot 40='
           '\\frac{1}{4}\\cdot(200+40)=\\frac{1}{4}\\cdot 240=60$ dollars.',
           'Traps: 50 forgets the unlocks; 52 and 72 use the prices of quarter 2 or quarter 4.'],
       S)
    mk(4, 2, U4_INTRO, U4_T,
       'When the difference between the highest price per riding minute and the lowest price per riding minute is 5 cents or '
       'less, it is said that there is "price alignment" between the companies.\n'
       'In which of the quarters was there price alignment between the companies?',
       ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4'], 1, [
           '"Price alignment" is about the riding-minute rows only. In each quarter, compare the highest and the lowest of the '
           'four riding-minute prices.',
           'Quarter 1: highest 25, lowest 20. Difference 5, which is "5 cents or less": price alignment. This is the answer.',
           'Tip: once you have found a quarter that works, you can stop. For completeness:',
           'Quarter 2: 35 − 20 = 15. Quarter 3: 40 − 25 = 15. Quarter 4: 35 − 15 = 20. All more than 5.'],
       S)
    mk(4, 3, U4_INTRO, U4_T,
       'Throughout the year, Noa paid an average of 15 cents per unlock.\n'
       'Noa cannot have been a customer of ______ throughout the whole year.',
       ['Pedal', 'Spin', 'Wheelo', 'Ryde'], 1, [
           'Noa paid 15 cents on average. This is possible only if the company\'s unlock price was exactly 15 all year, or if it was '
           'sometimes above 15 and sometimes below 15. An average cannot be lower than the lowest price or higher than the highest one.',
           'So look for a company whose unlock prices are ALL above 15 (or all below it).',
           'Pedal: unlock prices 30, 30, 25, 30. The lowest is 25, more than 15, so the average cannot be 15. This is the answer.',
           'Spin (0 to 20), Wheelo (10 to 40) and Ryde (10 to 40) each have prices below 15 and above 15, so an average of 15 is possible.'],
       S)
    mk(4, 4, U4_INTRO, U4_T,
       'The total number of riding minutes of Spin\'s customers doubled from quarter to quarter.\n'
       'Spin\'s income from riding minutes in quarter 4 was ______ times its income from riding minutes in quarter 1.',
       ['8', '6', '4', '2'], 1, [
           'Notice: Spin\'s price per riding minute is the same in quarter 1 and in quarter 4 (25 cents). So the income changes '
           'only because of the number of minutes.',
           'The number of minutes doubled three times: quarter 1 → 2 (×2), 2 → 3 (×2), 3 → 4 (×2). In all, $2\\cdot 2\\cdot 2=8$ times.',
           'Plugging in a number: say 1 minute in quarter 1 (income 25 cents). Then 2, 4 and 8 minutes; in quarter 4 the income is '
           '8 · 25 = 200 cents. $\\frac{200}{25}=8$.',
           'Traps: 6 adds the doublings (2 + 2 + 2) instead of multiplying them; 4 counts only two doublings.'],
       S)
    mk(4, 5, U4_INTRO, U4_T,
       'In quarter 4, Dan made one ride (one unlock) for every 5 minutes of riding.\n'
       'At which company would Dan pay the lowest total amount in quarter 4?',
       ['Pedal', 'Spin', 'Wheelo', 'Ryde'], 3, [
           'Plug in a convenient number: 5 minutes of riding and 1 unlock, with the prices of quarter 4.',
           'Pedal: 5 · 30 + 30 = 180 cents. Spin: 5 · 25 + 20 = 145 cents.',
           'Wheelo: 5 · 15 + 40 = 115 cents. Ryde: 5 · 35 + 10 = 185 cents.',
           'The lowest is Wheelo.',
           'Estimation: Dan pays for 5 times as many minutes as unlocks, so the minute price matters most. Wheelo has the lowest '
           'minute price (15), and even with its expensive unlock (40) it pays 115, while at every other company the minutes '
           'alone already cost 125 or more.'],
       S)


# =====================================================================================================================
# UNIT 5 · water level line, line style = current speed, weather icons per half month (October-May)
# =====================================================================================================================
U5_MONTHS = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
U5_MONTH_NAMES = ['October', 'November', 'December', 'January', 'February', 'March', 'April', 'May']
U5_KNOTS = [(0, 60), (0.5, 65), (1, 70), (1.5, 95), (2, 80), (2.3, 100), (2.6, 90), (3, 110), (3.4, 125), (4, 100),
            (4.5, 108), (5, 120), (5.4, 130), (6, 125), (6.5, 118), (7, 105), (8, 105)]
U5F = pchip(U5_KNOTS)
# weather in each half month: S sunny, P partly cloudy, C cloudy, R rainy
U5_WEATHER = ['S', 'P', 'C', 'R', 'R', 'C', 'R', 'R', 'C', 'P', 'R', 'P', 'P', 'S', 'S', 'S']
# current speed (0 = 0-1, 1 = 1-2, 2 = 2-3 metres per second) in each half month
U5_SPEED = [0, 0, 1, 2, 2, 1, 2, 1, 0, 1, 2, 0, 1, 1, 0, 0]
U5_SPEED_NAME = ['0-1 metres per second', '1-2 metres per second', '2-3 metres per second']
U5_STYLE = [(INK, 2.4), ('#8CC4B8', 6.5), (TEAL, 7.5)]
U5_WNAME = {'S': 'Sunny', 'P': 'Partly cloudy', 'C': 'Cloudy', 'R': 'Rainy'}
U5_SUN = {'S': 3, 'P': 2, 'C': 1, 'R': 0}


def _icon(k, x, y, s=1.0):
    o = []
    def sun(cx, cy, r):
        out = [_c(cx, cy, r, '#ffffff', INK, 1.4)]
        for a in range(8):
            t = a * math.pi / 4
            out.append(_l(cx + (r + 2.5) * math.cos(t), cy + (r + 2.5) * math.sin(t),
                          cx + (r + 6.5) * math.cos(t), cy + (r + 6.5) * math.sin(t), INK, 1.4))
        return ''.join(out)
    def cloud(cx, cy, w):
        u = w / 26.0
        d = ('M%.1f,%.1f h%.1f a%.1f,%.1f 0 0 0 0,-%.1f a%.1f,%.1f 0 0 0 -%.1f,-%.1f a%.1f,%.1f 0 0 0 -%.1f,%.1f '
             'a%.1f,%.1f 0 0 0 0,%.1f z' % (cx - 11 * u, cy + 6 * u, 22 * u, 5 * u, 5 * u, 10 * u, 7 * u, 7 * u, 10 * u, 4 * u,
                                          7 * u, 7 * u, 12 * u, 0.5 * u, 5 * u, 5 * u, 9.5 * u))
        return '<path d="%s" fill="#ffffff" stroke="%s" stroke-width="1.4" stroke-linejoin="round"/>' % (d, INK)
    if k == 'S': o.append(sun(x, y, 6.5 * s))
    elif k == 'C': o.append(cloud(x, y + 2, 30 * s))
    elif k == 'P': o.append(sun(x - 5 * s, y - 5, 5 * s)); o.append(cloud(x + 3, y + 4, 25 * s))
    else:
        o.append(cloud(x, y - 1, 28 * s))
        for dx in (-6, 0, 6): o.append(_l(x + dx, y + 8, x + dx - 2.5, y + 14, TEAL, 1.6))
    return ''.join(o)


def unit5_svg():
    W, H = 900, 640
    X0, X1, YB, YT = 95.0, 695.0, 470.0, 120.0
    def px(x): return X0 + (X1 - X0) * x / 8.0
    def py(v): return YB - (YB - YT) * (v - 50) / 90.0
    o = []
    for v in range(50, 141, 5):
        if v % 10 == 0:
            o.append(_l(X0, py(v), X1, py(v), GRID, 1.1, '5 4')); o.append(_t(X0 - 12, py(v), str(v), 16, INK, 'end', 700))
        else: o.append(_l(X0 - 5, py(v), X0, py(v), INK, 1.2))
    for k in range(17):
        x = px(k / 2.0)
        o.append(_l(x, YT - 10, x, YB, INK if k % 2 == 0 else GRID, 1.3 if k % 2 == 0 else 1.1, None if k % 2 == 0 else '5 4'))
    o.append(_l(X0, YB, X1, YB, INK, 2)); o.append(_l(X0, YB, X0, YT - 30, INK, 2))
    o.append(_poly([(X0, YT - 40), (X0 - 6, YT - 27), (X0 + 6, YT - 27)], INK))
    o.append(_t(X0, YT - 76, 'Water level', 17, INK, 'middle', 700)); o.append(_t(X0, YT - 57, '(cm)', 15, INK, 'middle', 700))
    for i in range(16):
        c, w = U5_STYLE[U5_SPEED[i]]
        pts = [(px(i / 2.0 + j / 100.0), py(U5F(i / 2.0 + j / 100.0))) for j in range(0, 51)]
        o.append(_path(pts, c, w, 'butt'))
    # weather row and month row
    r1, r2 = YB + 10, YB + 58
    o.append(_r(X0, r1, X1 - X0, 48, '#ffffff', INK, 1.3)); o.append(_r(X0, r2, X1 - X0, 36, '#ffffff', INK, 1.3))
    for i in range(16):
        x = px(i / 2.0)
        o.append(_l(x, r1, x, r1 + 48, INK, 1.3 if i % 2 == 0 else 0.8))
        o.append(_icon(U5_WEATHER[i], x + (X1 - X0) / 32.0, r1 + 22))
    for m in range(8):
        o.append(_l(px(m), r2, px(m), r2 + 36, INK, 1.3))
        o.append(_t(px(m + 0.5), r2 + 19, U5_MONTHS[m], 17, INK, 'middle', 700))
    o.append(_t(X0 - 10, r1 + 24, 'Weather', 15, INK, 'end', 700)); o.append(_t(X0 - 10, r2 + 19, 'Month', 15, INK, 'end', 700))
    # legend
    lx = 712
    o.append(_t(lx, 100, 'Legend:', 18, INK, 'start', 800))
    o.append(_r(lx, 114, 180, 136, '#ffffff', INK, 1.3))
    o.append(_t(lx + 90, 134, 'Current speed', 16, INK, 'middle', 800))
    o.append(_t(lx + 90, 152, '(metres per second)', 13, MUTED, 'middle'))
    for k, lab in enumerate(['0-1', '1-2', '2-3']):
        y = 180 + k * 26; c, w = U5_STYLE[k]
        o.append(_l(lx + 14, y, lx + 64, y, c, w)); o.append(_t(lx + 78, y, lab, 17, INK, 'start', 700))
    o.append(_r(lx, 266, 180, 176, '#ffffff', INK, 1.3))
    o.append(_t(lx + 90, 286, 'Weather', 16, INK, 'middle', 800))
    for k, w in enumerate(['S', 'P', 'C', 'R']):
        y = 318 + k * 34
        o.append(_icon(w, lx + 30, y)); o.append(_t(lx + 58, y + 2, U5_WNAME[w], 16, INK, 'start'))
    return _svg(W, H, 'Line graph: river water level from October to May, line style showing the current speed, with the '
                      'weather in each half month', ''.join(o))


U5_INTRO = (LEAD +
            'The chart shows data on the water level of a river at a measuring station, on the speed of the river\'s current and on '
            'the weather, from the month of October to the month of May of a certain year.\n'
            'The vertical axis shows the water level in centimetres. The horizontal axis shows the names of the months, and for each '
            'month two symbols are marked: on the left - the weather that prevailed in the first half of the month, and on the '
            'right - the weather that prevailed in the second half of the month (see legend). The styles of the line of the graph '
            'show the speed of the current, according to the legend.\n'
            'For example: in the first half of October the weather was sunny, the water level rose from 60 cm to 65 cm, and the '
            'speed of the current was between 0 and 1 metres per second.' + NOTE)
U5_T = 'River Level'


def u5_month_rose(m): return U5F(m + 1) > U5F(m) + 1e-9


def build_unit5():
    S = unit5_svg()
    mk(5, 1, U5_INTRO, U5_T,
       'In how many of the months shown in the chart was the water level at the end of the month higher than the water level '
       'at the beginning of the month?',
       ['6', '5', '4', '3'], 2, [
           'The water level is on the vertical axis. For each month, compare only the two ends: the point on its left border '
           '(beginning) and the point on its right border (end). What happens in the middle of the month does not matter.',
           'October 60 → 70, November 70 → 80, December 80 → 110, February 100 → 120, March 120 → 125: higher at the end.',
           'January 110 → 100: the level rose in the middle of the month, but at the end it was lower than at the beginning.',
           'April 125 → 105: lower. May 105 → 105: the same, not higher.',
           'In all: 5 months.'],
       S)
    mk(5, 2, U5_INTRO, U5_T,
       'Which of the following statements is necessarily true according to the data in the chart?',
       ['When the weather is partly cloudy, the speed of the current is between 1 and 2 metres per second',
        'When the weather is cloudy, the speed of the current is between 2 and 3 metres per second',
        'When the speed of the current is between 1 and 2 metres per second, the weather is not rainy',
        'When the speed of the current is between 2 and 3 metres per second, the weather is not sunny'], 4, [
           '"Necessarily true" = true for EVERY half month. One counterexample is enough to rule a statement out.',
           '(1) In the second half of October the weather was partly cloudy, but the line is thin (0-1 metres per second). Out.',
           '(2) In the first half of November the weather was cloudy, but the current was 1-2 metres per second (light thick line). Out.',
           '(3) In the second half of January the current was 1-2 metres per second, and the weather was rainy. Out.',
           'Tip: after ruling out three choices you may mark (4) without checking it. For completeness:',
           '(4) The dark thick line (2-3 metres per second) appears in the second half of November, the first half of December, '
           'the first half of January and the first half of March. In all of them the weather was rainy, never sunny. True.'],
       S)
    mk(5, 3, U5_INTRO, U5_T,
       'What was the lowest water level in December?',
       ['70 cm', '80 cm', '90 cm', '110 cm'], 2, [
           'The water level is on the vertical axis. Look at the part of the graph between the left and right borders of December, '
           'and find its lowest point.',
           'In the middle of December the graph dips, but only to 90 cm. The lowest point of December is at its very beginning '
           '(the left border): 80 cm. After it the graph only goes up to 100 cm and then stays above 90 cm.',
           'Traps: 90 cm is the dip in the middle of the month; 110 cm is the level at the end of the month.'],
       S)
    mk(5, 4, U5_INTRO, U5_T,
       'A research institute defined a "sun score" for each kind of weather: sunny - 3, partly cloudy - 2, cloudy - 1, rainy - 0.\n'
       'The average "sun score" in the period from the beginning of February to the end of April was -',
       ['between 0 and 1', 'between 1 and 2', 'exactly 2', 'between 2 and 3'], 2, [
           'First find the weather in each half month from February to April (6 halves), and write its score:',
           'February: cloudy (1), partly cloudy (2). March: rainy (0), partly cloudy (2). April: partly cloudy (2), sunny (3).',
           'Estimation: the "extreme" scores 0 and 3 appear once each, and all the other scores are 1 or 2, so the average must be '
           'between 1 and 2.',
           'Exact: $\\frac{1+2+0+2+2+3}{6}=\\frac{10}{6}=1\\frac{2}{3}$, which is between 1 and 2.'],
       S)


# =====================================================================================================================
# verification: recompute every answer from the data; exactly one correct choice, at the book key position
# =====================================================================================================================
BOOK_KEY = {1: [3, 1, 4, 3], 2: [2, 3, 4, 4], 3: [2, 3, 1, 4, 3], 4: [3, 1, 1, 1, 3], 5: [2, 4, 2, 2]}


def _verify():
    def ans(u, n): return QUESTIONS['chp%02d-q%d' % (u, n)]['correct'][0] + 1
    def one(u, n, vals, good):
        hits = [k + 1 for k, v in enumerate(vals) if good(v)]
        assert hits == [ans(u, n)] == [BOOK_KEY[u][n - 1]], ('chp%02d-q%d' % (u, n), hits, ans(u, n))
    # ---- unit 1
    for sc in U1:
        for i in range(len(U1_LEN)):
            col = [U1[sc][c][i] for c in U1[sc]]
            assert len(set(col)) == 4                                   # no two letters on the same spot
    assert u1p('Lingo', 'F', 25) == 1100                                # example
    c = QUESTIONS['chp01-q1']['choices']
    one(1, 1, [int(x) for x in c], lambda v: 100 * v == 35 * u1p('Verba', 'S', 20))
    assert [35 * u1p(a, 'S', n) for a, n in (('Lingo', 20), ('Verba', 15), ('Verba', 10))] == [38500, 21000, 24500]
    best = min(u1p(s, 'G', 45) for s in U1) + min(u1p(s, 'P', 50) for s in U1)
    one(1, 2, [int(x.replace(',', '')) for x in QUESTIONS['chp01-q2']['choices']], lambda v: v == best)
    assert u1p('Lingo', 'G', 45) + u1p('Lingo', 'P', 50) == 3300 and u1p('Verba', 'G', 45) + u1p('Verba', 'P', 50) == 3500
    assert max(u1p(s, 'G', 45) for s in U1) + max(u1p(s, 'P', 50) for s in U1) == 3600
    per = [u1p('Lingo', 'F', 20) / 20.0, u1p('Lingo', 'S', 20) / 20.0, u1p('Lingo', 'F', 30) / 30.0, u1p('Lingo', 'S', 30) / 30.0]
    one(1, 3, per, lambda v: v == min(per))
    assert per[0] < per[1] and per[3] < per[2]                           # the pairing shortcut works
    tot = [u1p('Lingo', 'P', 40), 2 * u1p('Lingo', 'P', 20), u1p('Lingo', 'P', 25) + u1p('Lingo', 'P', 15)]
    assert len(set(tot)) == 3
    one(1, 4, tot + [None], lambda v: v == max(tot))
    # ---- unit 2
    for p, (x, y) in U2_P.items():
        assert min(abs(u2d(x, y) - c) for c in U2_CUTS) >= 20, p        # every dot clearly inside its band
    assert u2level(6) == 'Very low' and U2_P[6] == (500, 60)             # example
    cnt = {}
    for p in U2_P: cnt[u2level(p)] = cnt.get(u2level(p), 0) + 1
    one(2, 1, ['Very low', 'Low', 'Medium', 'High'], lambda v: cnt[v] == max(cnt.values()))
    assert sorted(cnt.values())[-1] > sorted(cnt.values())[-2]
    def need(p):   # water reduction needed to go from the right-hand Medium band into the right-hand Low band (None if impossible)
        x, y = U2_P[p]
        if u2band(x, y) != 4: return None
        return u2d(x, y) - U2_CUTS[3]
    red = [need(10), need(5), need(13), need(12)]
    assert u2level(5) == 'Medium' and u2band(*U2_P[5]) == 0 and u2level(12) == 'Very low'
    one(2, 2, red, lambda v: v is not None and v == max(r for r in red if r is not None))
    x8 = U2_P[8][0]
    right = [p for p in U2_P if U2_P[p][0] > x8]
    good = [p for p in right if u2level(p) in ('Low', 'Very low')]
    one(2, 3, [8, 6, 3, 4], lambda v: v == len(good))
    assert len(right) == 8 and len([p for p in right if u2level(p) == 'Low']) == 3
    assert len([p for p in right if u2level(p) in ('Low', 'Very low', 'Medium')]) == 6
    diffs = [x - y for x, y in U2_P.values()]
    one(2, 4, [270, 330, 800, 870], lambda v: v == max(diffs))
    assert min(diffs) == 270 and U2_P[1][0] - U2_P[1][1] == 330 and U2_P[16][0] - U2_P[16][1] == 800
    # ---- unit 3
    assert abs(u3alt(3) - 350) < 1e-9 and abs(u3alt(1.5) - 400) < 1e-9 and 1.5 in U3_STOPS          # example
    assert U3_HOURS[0] == 0 and U3_HOURS[-1] == 24 and len(U3_HOURS) == 9
    for a, b in zip(U3_HOURS, U3_HOURS[1:]): assert a < b
    assert not set(U3_HOURS) & set(U3_STOPS)
    alts = [u3alt(s) for s in U3_STOPS]
    diff = max(alts) - min(alts)
    one(3, 1, [700, 750, 850, 950], lambda v: abs(v - diff) < 1e-6)
    grid = [u3alt(k / 100.0) for k in range(2401)]
    assert abs(max(grid) - 950) < 1 and abs(min(grid) - 100) < 1 and abs(max(alts) - 950) < 1e-9 and abs(min(alts) - 200) < 1e-9
    seg = 5; start = U3_START + seg - 1
    one(3, 2, [(10, 11), (11, 12), (12, 13), (13, 14)], lambda v: v == (start, start + 1))
    seg8 = next(k for k in range(8) if U3_START + k <= 15.5 < U3_START + k + 1)
    a, b = U3_HOURS[seg8], U3_HOURS[seg8 + 1]
    vals = [u3alt(a + (b - a) * k / 1000.0) for k in range(1, 1000)]
    lo, hi = min(vals), max(vals)
    one(3, 3, [300, 450, 600, 800], lambda v: not (lo < v < hi))
    avg = len(U3_STOPS) / float(len(U3_HOURS) - 1)
    one(3, 4, [1, 2, 4 / 3.0, 1.5], lambda v: abs(v - avg) < 1e-9)
    assert abs(len(U3_STOPS) / float(len(U3_HOURS)) - 4 / 3.0) < 1e-9                                 # the 1 1/3 trap
    times = {L: crossings(u3alt, 0, 24, L) for L in (600, 300, 500, 400)}
    assert times == {600: 2, 300: 2, 500: 4, 400: 3}, times
    one(3, 5, [600, 300, 500, 400], lambda v: times[v] == max(times.values()))
    # ---- unit 4
    assert U4['Wheelo'][0][2] == 30 and U4['Wheelo'][1][2] == 20                                      # example
    def bill(co, q, minutes, rides): return (U4[co][0][q] * minutes + U4[co][1][q] * rides) / 100.0
    one(4, 1, [50, 52, 60, 72], lambda v: v == bill('Pedal', 2, 200, 40))
    assert bill('Pedal', 1, 200, 40) == 52 and bill('Pedal', 3, 200, 40) == 72 and U4['Pedal'][0][2] * 200 / 100.0 == 50
    spread = [max(U4[c][0][q] for c in U4) - min(U4[c][0][q] for c in U4) for q in range(4)]
    one(4, 2, [0, 1, 2, 3], lambda q: spread[q] <= 5)
    one(4, 3, U4_CO, lambda c: not (min(U4[c][1]) <= 15 <= max(U4[c][1])))
    ratio = 8 * U4['Spin'][0][3] / float(U4['Spin'][0][0])
    one(4, 4, [8, 6, 4, 2], lambda v: v == ratio)
    tot = [bill(c, 3, 5, 1) for c in U4_CO]
    one(4, 5, U4_CO, lambda c: bill(c, 3, 5, 1) == min(tot))
    k = U4_CO.index('Wheelo')
    assert all(U4[c][0][3] * 5 / 100.0 > tot[k] for c in U4_CO if c != 'Wheelo')                      # the estimation holds
    # ---- unit 5
    assert abs(U5F(0) - 60) < 1e-9 and abs(U5F(0.5) - 65) < 1e-9 and U5_WEATHER[0] == 'S' and U5_SPEED[0] == 0   # example
    rose = sum(u5_month_rose(m) for m in range(8))
    one(5, 1, [6, 5, 4, 3], lambda v: v == rose)
    assert not u5_month_rose(3) and max(U5F(3 + j / 100.0) for j in range(101)) > U5F(3) + 10               # January trap
    assert abs(U5F(8) - U5F(7)) < 1e-9                                                                      # May: flat
    halves = list(zip(U5_WEATHER, U5_SPEED))
    st = [all(s == 1 for w, s in halves if w == 'P'),
          all(s == 2 for w, s in halves if w == 'C'),
          all(w != 'R' for w, s in halves if s == 1),
          all(w != 'S' for w, s in halves if s == 2)]
    one(5, 2, st, lambda v: v)
    dec = [U5F(2 + j / 1000.0) for j in range(1001)]
    low = min(dec)
    assert abs(low - U5F(2)) < 1e-6 and abs(U5F(2.6) - 90) < 1e-9 and abs(U5F(3) - 110) < 1e-9
    one(5, 3, [70, 80, 90, 110], lambda v: abs(v - low) < 1e-6)
    sc = [U5_SUN[w] for w in U5_WEATHER[8:14]]                                                              # Feb, Mar, Apr
    avg = sum(sc) / float(len(sc))
    rng = [(0, 1), (1, 2), (2, 2), (2, 3)]
    one(5, 4, rng, lambda r: (r[0] == r[1] == avg) or (r[0] < r[1] and r[0] < avg < r[1]))
    # ---- general
    for q in QUESTIONS.values():
        assert not re.search(r'[\u0590-\u05FF]', q['stemRich'] + ''.join(q['choicesRich']) + ''.join(q['explanation']))
        assert len(q['choices']) == 4 and len(set(q['choices'])) == 4
    assert [len([q for q in ORDER if q.startswith('chp%02d' % u)]) for u in range(1, 6)] == [4, 4, 5, 5, 4]


build_unit1(); build_unit2(); build_unit3(); build_unit4(); build_unit5()
_verify()

MODULES = []
PRACTICE = {52: list(ORDER)}
MEMORY = []
