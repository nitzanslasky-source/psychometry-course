# Quantitative Reasoning · Topic 52 · Charts & Tables — PRACTICE part (the three chart sets).
# Source: course book pp. 228-233 ("Chart 1", "Chart 2", "Chart 3", 15 questions; key on p. 234) and the teacher's
# solutions (charts_src/seg11_practice_solutions.txt). Every chart is redrawn with CHANGED data (teacher's request):
# same chart type, same question types and tricks, correct answer in the same position as the book key.
# _verify() recomputes every answer from the data below and checks that exactly one choice is right.
from dsl import *
from vbank import _q
from math_api import rich_html, rich_plain

T52 = 52
INK, TEAL, AMBER, SOFT, GRID, MUTED = '#0F172A', '#0F766E', '#F5A524', '#E6F4F1', '#D8E6E3', '#5B6B7A'
FONT = "font-family=\"'Helvetica Neue',Helvetica,Arial,sans-serif\""


# =====================================================================================================================
# svg helpers
# =====================================================================================================================
def _svg(vb, label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s"><title>%s</title>'
            '<rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (vb[0], vb[1], label, label, vb[0], vb[1], body))


def _t(x, y, s, size=18, color=INK, anchor='middle', weight=400, rot=None):
    tr = ' transform="rotate(%d %.1f %.1f)"' % (rot, x, y) if rot else ''
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle" fill="%s" %s font-size="%d" font-weight="%d"%s>%s</text>'
            % (x, y, anchor, color, FONT, size, weight, tr, s))


def _l(x1, y1, x2, y2, color=INK, w=1.5, dash=None):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, color, w, ' stroke-dasharray="%s"' % dash if dash else ''))


def _r(x, y, w, h, fill='none', stroke=INK, sw=1.5):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, w, h, fill, stroke, sw)


def _nest(svg, x, y, w, h):
    return svg.replace('<svg ', '<svg x="%d" y="%d" width="%d" height="%d" ' % (x, y, w, h), 1)


# =====================================================================================================================
# CHART 1 · soil samples from 5 planets (scatter).  Book: Uranus / Venus / Jupiter / Saturn / Mars.
# =====================================================================================================================
C1 = {   # planet: [(carbon %, hydrogen %), ...]
    'Mercury': [(36, 6), (43, 15), (49, 24), (55, 33), (62, 42), (66, 48), (71, 57)],   # clean rising line (book: Mars)
    'Venus':   [(10, 44), (13, 57), (16, 36), (19, 64), (23, 48), (27, 33), (30, 53)],
    'Mars':    [(20, 22), (27, 42), (31, 28), (36, 36), (39, 23), (44, 32), (50, 44)],
    'Saturn':  [(8, 26), (17, 33), (24, 16), (33, 43), (41, 27), (48, 37), (55, 22)],  # widest carbon range (book: Venus)
    'Neptune': [(40, 18), (46, 12), (52, 16), (59, 12), (64, 8), (68, 7), (74, 3)],     # low-H corner; 59% ring touches the 60% line
}
C1_ORDER = ['Mercury', 'Venus', 'Mars', 'Saturn', 'Neptune']
C1_VB = (900, 560)
C1_X0, C1_X1, C1_YB, C1_YT = 95.0, 865.0, 505.0, 100.0          # plot box: carbon 0-80 %, hydrogen 0-70 %
def c1x(c): return C1_X0 + (C1_X1 - C1_X0) * c / 80.0
def c1y(h): return C1_YB - (C1_YB - C1_YT) * h / 70.0


def _marker(p, x, y):
    if p == 'Mercury': return '<circle cx="%.1f" cy="%.1f" r="8.5" fill="%s"/>' % (x, y, INK)
    if p == 'Venus': return _r(x - 8, y - 8, 16, 16, AMBER, '#9A6200', 1.5)
    if p == 'Mars': return '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="%s" stroke-width="1.5"/>' % (
        x, y - 11, x + 10, y, x, y + 11, x - 10, y, SOFT, TEAL)
    if p == 'Saturn': return '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="%s" stroke-width="1.5"/>' % (
        x, y - 10, x + 10, y + 8, x - 10, y + 8, TEAL, TEAL)
    return ('<circle cx="%.1f" cy="%.1f" r="10.5" fill="#ffffff" stroke="%s" stroke-width="2"/>'
            '<circle cx="%.1f" cy="%.1f" r="4.5" fill="none" stroke="%s" stroke-width="2"/>' % (x, y, INK, x, y, INK))


def chart1_svg():
    o = [_t(450, 20, 'Soil samples from 5 planets  ·  Note: the exact location of each shape is its centre', 17, MUTED)]
    xs = [120, 285, 440, 580, 735]
    for p, x in zip(C1_ORDER, xs):
        o.append(_marker(p, x, 52)); o.append(_t(x + 18, 53, p, 19, INK, 'start', 600))
    for k in range(0, 71, 5):   # hydrogen grid (dashed every 5 %)
        y = c1y(k)
        o.append(_l(C1_X0, y, C1_X1, y, GRID, 1.2 if k % 10 == 0 else 1, None if k % 10 == 0 else '4 4'))
        if k % 10 == 0: o.append(_t(C1_X0 - 10, y, '%d%%' % k, 17, INK, 'end'))
    for k in range(0, 81, 10):
        x = c1x(k); o.append(_l(x, C1_YT, x, C1_YB, GRID, 1.2)); o.append(_t(x, C1_YB + 20, '%d%%' % k, 17))
    o.append(_r(C1_X0, C1_YT, C1_X1 - C1_X0, C1_YB - C1_YT, 'none', INK, 1.8))
    o.append(_t(480, 548, 'Percentage of carbon in the sample', 19, INK, 'middle', 700))
    o.append(_t(20, (C1_YT + C1_YB) / 2, 'Percentage of hydrogen in the sample', 19, INK, 'middle', 700, -90))
    for p in C1_ORDER:
        for c, h in C1[p]: o.append(_marker(p, c1x(c), c1y(h)))
    return _svg(C1_VB, 'Scatter graph: carbon and hydrogen percentages in soil samples from five planets', ''.join(o))


BINS = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%']
def c1_hbins():
    b = [0] * 7
    for p in C1:
        for c, h in C1[p]: b[int(h // 10)] += 1
    return b
def c1_cbins():
    b = [0] * 8
    for p in C1:
        for c, h in C1[p]: b[int(c // 10)] += 1
    return b[:7]
C1_HIST = [c1_cbins(), c1_hbins(), [5, 6, 6, 7, 7, 3, 1], [4, 7, 6, 7, 6, 2, 3]]   # (2) is the true one; (1) = carbon by mistake
C1_OPT_VB = (900, 650)


def chart1_options_svg():
    o = [_t(450, 18, 'Horizontal axis: percentage of hydrogen in the sample  ·  Vertical axis: number of samples', 17, MUTED)]
    for k, hist in enumerate(C1_HIST):
        px, py = (k % 2) * 450, 36 + (k // 2) * 307
        x0, x1, yb, yt = px + 70, px + 430, py + 262, py + 42
        bw = (x1 - x0) / 7.0; sy = (yb - yt) / 10.0
        o.append(_t(px + 26, py + 22, '(%d)' % (k + 1), 24, TEAL, 'middle', 800))
        for v in range(0, 11, 2):
            o.append(_l(x0, yb - v * sy, x1, yb - v * sy, GRID, 1)); o.append(_t(x0 - 8, yb - v * sy, str(v), 15, INK, 'end'))
        for j, n in enumerate(hist):
            if n: o.append(_r(x0 + j * bw, yb - n * sy, bw, n * sy, SOFT, TEAL, 1.6))
        o.append(_l(x0, yb, x1, yb, INK, 1.8)); o.append(_l(x0, yt, x0, yb, INK, 1.8))
        for j in range(8): o.append(_t(x0 + j * bw, yb + 17, BINS[j], 14))
    return _svg(C1_OPT_VB, 'Four histograms of the number of samples by percentage of hydrogen, labelled (1) to (4)', ''.join(o))


def chart1_q5_svg():
    return _svg((900, 1230), 'Scatter graph and four answer histograms',
                _nest(chart1_svg(), 0, 0, 900, 560) + _l(20, 575, 880, 575, GRID, 2) + _nest(chart1_options_svg(), 0, 580, 900, 650))


# =====================================================================================================================
# CHART 2 · car races 2017-2022 (table + prize table).  Book: 2011-2016, prizes 100,000 / 75,000 / 50,000 / 25,000 / 10,000.
# =====================================================================================================================
YEARS = [2017, 2018, 2019, 2020, 2021, 2022]
TEAMS = ['Road Runners', 'Desert Foxes', 'Night Owls', 'Iron Eagles', 'Blue Comets', 'Red Arrows', 'Silver Wolves']
PLACE = {'Road Runners': [4, 2, 5, 1, 3, 3], 'Desert Foxes': [1, 6, 3, 4, 1, 2], 'Night Owls': [2, 3, 2, 3, 2, 4],
         'Iron Eagles': [7, 5, 6, 7, 5, 7], 'Blue Comets': [6, 7, 7, 5, 4, 1], 'Red Arrows': [3, 1, 4, 6, 7, 5],
         'Silver Wolves': [5, 4, 1, 2, 6, 6]}
PRIZE = {1: 120000, 2: 80000, 3: 50000, 4: 20000, 5: 10000, 6: 0, 7: 0}
C2_VB = (900, 560)
C2_TX, C2_TY, C2_TW, C2_YW, C2_HH, C2_RH = 14, 48, 176, 72, 62, 62     # main table geometry
C2_PX = 660


def c2_row_bottom(team):   # y of the bottom border of a team's row (viewBox)
    return C2_TY + C2_HH + C2_RH * (TEAMS.index(team) + 1)


def _money(v): return '{:,}'.format(v)


def chart2_svg():
    o = [_t(C2_TX, 22, 'Place of each team in the race, by year', 18, MUTED, 'start', 600),
         _t(C2_PX, 22, 'Prize by place', 18, MUTED, 'start', 600)]
    W = C2_TW + 6 * C2_YW
    o.append(_r(C2_TX, C2_TY, W, C2_HH, SOFT, 'none', 0))
    o.append(_t(C2_TX + 12, C2_TY + C2_HH / 2, 'Team \\ Year', 18, INK, 'start', 700))
    for k, yr in enumerate(YEARS):
        o.append(_t(C2_TX + C2_TW + C2_YW * (k + .5), C2_TY + C2_HH / 2, str(yr), 19, INK, 'middle', 700))
    for r, tm in enumerate(TEAMS):
        y = C2_TY + C2_HH + C2_RH * r
        o.append(_t(C2_TX + 12, y + C2_RH / 2, tm, 19, INK, 'start', 600))
        for k, pl in enumerate(PLACE[tm]):
            o.append(_t(C2_TX + C2_TW + C2_YW * (k + .5), y + C2_RH / 2, str(pl), 22))
    for r in range(9):
        y = C2_TY + (0 if r == 0 else C2_HH + C2_RH * (r - 1)); o.append(_l(C2_TX, y, C2_TX + W, y, INK if r in (0, 1, 8) else '#9FB3B0', 1.5))
    for c in range(8):
        x = C2_TX + (0 if c == 0 else C2_TW + C2_YW * (c - 1)); o.append(_l(x, C2_TY, x, C2_TY + C2_HH + 7 * C2_RH, INK if c in (0, 1, 7) else '#9FB3B0', 1.5))
    # prize table
    PW1, PW2 = 92, 136
    o.append(_r(C2_PX, C2_TY, PW1 + PW2, C2_HH, SOFT, 'none', 0))
    o.append(_t(C2_PX + PW1 / 2, C2_TY + 20, 'Place in', 16, INK, 'middle', 700)); o.append(_t(C2_PX + PW1 / 2, C2_TY + 42, 'the race', 16, INK, 'middle', 700))
    o.append(_t(C2_PX + PW1 + PW2 / 2, C2_TY + 20, 'Prize', 16, INK, 'middle', 700)); o.append(_t(C2_PX + PW1 + PW2 / 2, C2_TY + 42, '(shekels)', 16, INK, 'middle', 700))
    for r in range(7):
        y = C2_TY + C2_HH + C2_RH * r
        o.append(_t(C2_PX + PW1 / 2, y + C2_RH / 2, str(r + 1), 22)); o.append(_t(C2_PX + PW1 + PW2 / 2, y + C2_RH / 2, _money(PRIZE[r + 1]), 21))
    for r in range(9):
        y = C2_TY + (0 if r == 0 else C2_HH + C2_RH * (r - 1)); o.append(_l(C2_PX, y, C2_PX + PW1 + PW2, y, INK if r in (0, 1, 8) else '#9FB3B0', 1.5))
    for x in (C2_PX, C2_PX + PW1, C2_PX + PW1 + PW2): o.append(_l(x, C2_TY, x, C2_TY + C2_HH + 7 * C2_RH, INK, 1.5))
    return _svg(C2_VB, 'Table of the place of seven teams in car races 2017-2022, and a table of the prize for each place', ''.join(o))


# =====================================================================================================================
# CHART 3 · weddings in an event hall (bars + a pie above each bar).  Book: 300/400/200/250/400 guests.
# =====================================================================================================================
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
GUESTS = {'Sunday': 300, 'Monday': 400, 'Tuesday': 500, 'Wednesday': 200, 'Thursday': 350}
SPLIT = {'Sunday': (60, 20, 20), 'Monday': (50, 25, 25), 'Tuesday': (25, 50, 25), 'Wednesday': (35, 35, 30),
         'Thursday': (30, 50, 20)}     # % (groom's side only, bride's side only, shared)
C3_VB = (900, 560)
C3_X0, C3_X1, C3_YB, C3_YT = 110.0, 880.0, 500.0, 200.0         # 0-600 guests
def c3y(n): return C3_YB - (C3_YB - C3_YT) * n / 600.0
def c3x(k): return C3_X0 + (C3_X1 - C3_X0) * (k + .5) / 5.0


def _pie(cx, cy, r, parts):
    import math
    cols = [(TEAL, '#ffffff'), ('#ffffff', INK), (AMBER, INK)]
    o, a = [], -90.0
    for (pct, (fill, tc)) in zip(parts, cols):
        if not pct: continue
        b = a + 360.0 * pct / 100
        x1, y1 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        x2, y2 = cx + r * math.cos(math.radians(b)), cy + r * math.sin(math.radians(b))
        o.append('<path d="M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 1 %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="1.5"/>'
                 % (cx, cy, x1, y1, r, r, 1 if pct > 50 else 0, x2, y2, fill, INK))
        m = math.radians((a + b) / 2)
        o.append(_t(cx + r * .58 * math.cos(m), cy + r * .58 * math.sin(m), '%d%%' % pct, 16, tc, 'middle', 700))
        a = b
    return ''.join(o)


def chart3_svg():
    o = [_t(450, 18, 'Number of guests at each wedding last week, and how they divide (in %)', 17, MUTED)]
    lg = [(TEAL, "Groom's side only"), ('#ffffff', "Bride's side only"), (AMBER, 'Shared (groom and bride)')]
    for (fill, name), x in zip(lg, (150, 395, 640)):
        o.append(_r(x - 30, 42, 22, 18, fill, INK, 1.4)); o.append(_t(x, 52, name, 18, INK, 'start', 600))
    for n in range(0, 601, 100):
        y = c3y(n); o.append(_l(C3_X0, y, C3_X1, y, GRID if n else INK, 1.2 if n else 1.8, None if n else None))
        o.append(_t(C3_X0 - 10, y, str(n), 17, INK, 'end'))
    o.append(_l(C3_X0, C3_YT, C3_X0, C3_YB, INK, 1.8))
    o.append(_t(24, (C3_YT + C3_YB) / 2, 'Number of guests', 19, INK, 'middle', 700, -90))
    for k, d in enumerate(DAYS):
        x = c3x(k); n = GUESTS[d]
        o.append(_r(x - 38, c3y(n), 76, C3_YB - c3y(n), TEAL, INK, 1.2))
        o.append(_t(x, C3_YB + 22, d, 19, INK, 'middle', 700))
        o.append(_pie(x, 128, 56, SPLIT[d]))
    o.append(_t(C3_X0 - 10, C3_YB + 46, 'Day:', 18, MUTED, 'end', 700))
    return _svg(C3_VB, 'Bar graph of the number of wedding guests on each day, with a pie of the guest groups above each bar', ''.join(o))


# =====================================================================================================================
# questions
# =====================================================================================================================
QUESTIONS = {}
FIG = {}   # qid -> svg shown with the question (site + slides)

C1_INTRO = ('Study the graph below, then answer the five questions that follow.\n'
            'The graph below shows the percentage of carbon and the percentage of hydrogen in samples taken from the soil of '
            '5 planets (Mercury, Venus, Mars, Saturn and Neptune). Each sample is represented in the graph by a shape that '
            'stands for the planet from which it was taken. On each planet, samples were taken from several different regions.\n'
            'Note: The exact location of each shape is its centre.\n'
            'Note: In answering each question, disregard the information appearing in the other questions.')
C2_INTRO = ('Study the tables below, then answer the five questions that follow.\n'
            'The tables below show the results of car races held in the years 2017-2022, in which seven teams took part: '
            'Road Runners, Desert Foxes, Night Owls, Iron Eagles, Blue Comets, Red Arrows and Silver Wolves. The table on the left '
            'shows the place each team reached in the race each year, and the table on the right shows the prize (in shekels) '
            'that each team won according to its place in the race.\n'
            'Note: Only one race was held each year.\n'
            'For example, in the 2019 race, the team "Night Owls" reached second place and won a prize of 80,000 shekels.\n'
            'Note: In answering each question, disregard the information appearing in the other questions.')
C3_INTRO = ('Study the graph below, then answer the five questions that follow.\n'
            'A wedding is held every day in the "Golden Garden" event hall. The graph below shows the number of guests who came '
            'to each wedding last week. Above each bar, the distribution of the guests in percent is shown, according to three '
            "groups: guests from the groom's side only, guests from the bride's side only, and guests shared by the groom and the bride.\n"
            "For example: on Sunday, a wedding with 300 guests was held in the event hall. 60% of the guests who came were from the groom's side only.\n"
            'Note: In answering each question, disregard the information appearing in the other questions.')
SHORT = {}   # qid -> question text alone (slides)


def mk(qid, chart, page, n, intro, stem, choices, key, steps, fig):
    full = intro + '\n\n' + stem
    q = _q(qid, T52, rich_plain(full), [rich_plain(c) for c in choices], key, '',
           dict(subject='charts', trustRank=1, reviewFlag=False, source='Course book p.%d chart %d q%d (numbers changed)' % (page, chart, n)))
    q.update(stem=full, stemRich=full, stemHtml=rich_html(full),
             choices=[rich_plain(c) for c in choices], choicesRich=list(choices), choicesHtml=[rich_html(c) for c in choices],
             explanation=list(steps), answerHtml=''.join('<p>%s</p>' % rich_html(e) for e in steps),
             work=[], workText=[], methods=[dict(title='Worked solution', steps=list(steps), work=[], independent=False, board=[])],
             navLabel=rich_plain(stem.replace('\n', ' '))[:120], questionVisual={'type': 'geometry', 'svg': fig},
             setIntro=intro, setTitle='Chart %d' % chart)
    QUESTIONS[qid] = q; SHORT[qid] = stem; FIG[qid] = fig


S1, S2, S3 = chart1_svg(), chart2_svg(), chart3_svg()

# ---------------- Chart 1 (book p. 228-229; key 3 2 1 3 2) ----------------
mk('ch-q01', 1, 228, 1, C1_INTRO, 'In how many of the samples is the percentage of carbon greater than 60%?',
   ['7', '3', '6', '10'], 3, [
    'Carbon is on the horizontal axis. Draw a vertical line at 60% carbon and count the shapes whose centre is to the right of it.',
    'Mercury has 3 samples there (62%, 66%, 71%) and Neptune has 3 (64%, 68%, 74%): 6 samples.',
    "The Neptune ring at 59% touches the line, but its centre is to the left of it, so it does not count (counting it gives 7).",
    'Careful not to use the 60% of the hydrogen axis: above 60% hydrogen there is only 1 sample, which is not one of the choices.'], S1)
mk('ch-q02', 1, 228, 2, C1_INTRO,
   'It is known that a region is more suitable for human habitation the higher the percentage of carbon in its soil and the lower '
   'the percentage of hydrogen in its soil. On which planet is the region most suitable for human habitation?',
   ['Venus', 'Neptune', 'Saturn', 'Mercury'], 2, [
    'High carbon = the right side of the graph; low hydrogen = the bottom of the graph. Look at the bottom-right corner.',
    'The sample at 74% carbon and 3% hydrogen is a Neptune ring. It has more carbon than any other sample and less hydrogen than any other sample.',
    'Mercury has samples with a lot of carbon, but they also have a lot of hydrogen.'], S1)
mk('ch-q03', 1, 229, 3, C1_INTRO, 'The largest range of carbon percentages is found in the samples from the planet',
   ['Saturn', 'Mars', 'Venus', 'Neptune'], 1, [
    'Range = the distance between the leftmost and the rightmost sample of the planet (carbon is the horizontal axis).',
    'Saturn: from 8% to 55% (47 points). Mars: 20% to 50% (30). Venus: 10% to 30% (20). Neptune: 40% to 74% (34).',
    'You do not need the exact numbers: draw each range as a line and compare the lengths. Saturn\'s line is the longest.'], S1)
mk('ch-q04', 1, 229, 4, C1_INTRO, 'Which of the following statements is necessarily true?',
   ['On Venus, the higher the percentage of carbon in a sample, the higher the percentage of hydrogen in it',
    'On Neptune, the higher the percentage of carbon in a sample, the lower the percentage of hydrogen in it',
    'On Mercury, the higher the percentage of carbon in a sample, the higher the percentage of hydrogen in it',
    'On Saturn, the lower the percentage of carbon in a sample, the higher the percentage of hydrogen in it'], 3, [
    'All four statements describe a steady relation between carbon and hydrogen on one planet. Look for a planet whose shapes form a line.',
    'The Mercury dots rise steadily from (36%, 6%) to (71%, 57%): the more carbon, the more hydrogen, with no exception.',
    'Venus and Saturn go up and down. Neptune almost always goes down, but from 46% to 52% carbon the hydrogen rises (12% to 16%), '
    'so "necessarily" fails.'], S1)
mk('ch-q05', 1, 229, 5, C1_INTRO,
   'Which of the following graphs describes the number of samples collected on all five planets together in each of the ranges '
   'of hydrogen percentages that appear in it?', ['(1)', '(2)', '(3)', '(4)'], 2, [
    'Circle the word "hydrogen": the ranges are on the vertical axis of the big graph.',
    'Do not check every graph to the end. Find where the four graphs differ and check only there, starting with the edges.',
    'Below 10% hydrogen there are 4 samples (a Mercury dot at 6% and Neptune rings at 3%, 7% and 8%). Graphs (1) and (3) show 1 and 5: out.',
    'From 60% to 70% hydrogen there is 1 sample (Venus, 64%). Graph (4) shows 3: out. The answer is graph (2).',
    'Graph (1) is what you get if you count carbon instead of hydrogen.'], chart1_q5_svg())
FIG['ch-q05-options'] = chart1_options_svg()

# ---------------- Chart 2 (book p. 230-231; key 2 1 3 3 1) ----------------
mk('ch-q06', 2, 230, 1, C2_INTRO, 'Which team won 120,000 shekels twice in the years 2017-2022?',
   ['Road Runners', 'Desert Foxes', 'Red Arrows', 'Silver Wolves'], 2, [
    '120,000 shekels is the prize for first place, so look for the 1s in the table.',
    'Year by year, first place went to: Desert Foxes (2017), Red Arrows (2018), Silver Wolves (2019), Road Runners (2020), '
    'Desert Foxes (2021), Blue Comets (2022).',
    'Only Desert Foxes came first twice.'], S2)
mk('ch-q07', 2, 230, 2, C2_INTRO,
   'A "dramatic change" is defined as a change of three places or more in the ranking of a team between two consecutive races. '
   'How many "dramatic changes" occurred in the years 2017-2022?', ['9', '5', '3', '12'], 1, [
    'Go team by team (row by row) and compare each year with the next one. A change of exactly 3 counts too.',
    'Road Runners: 2→5, 5→1 (2). Desert Foxes: 1→6, 6→3, 4→1 (3). Night Owls and Iron Eagles: none. '
    'Blue Comets: 4→1 (1). Red Arrows: 1→4 (1). Silver Wolves: 4→1, 2→6 (2).',
    'In all: 2 + 3 + 0 + 0 + 1 + 1 + 2 = 9.'], S2)
mk('ch-q08', 2, 231, 3, C2_INTRO,
   'What is the average amount (in shekels) that the team "Night Owls" won per year in the years 2017-2022?',
   ['50,000', '55,000', '60,000', '72,000'], 3, [
    'Night Owls places: 2, 3, 2, 3, 2, 4, so the prizes are 80,000 three times, 50,000 twice and 20,000 once.',
    '240,000 + 100,000 + 20,000 = 360,000 in 6 years: 360,000 ÷ 6 = 60,000.',
    '72,000 is what you get if you divide by 5 instead of 6.'], S2)
mk('ch-q09', 2, 231, 4, C2_INTRO,
   'Over the races in the years 2017-2022, the team "Blue Comets" earned ______ shekels ______ than the team "Iron Eagles".',
   ['130,000 ; less', '150,000 ; less', '130,000 ; more', '150,000 ; more'], 3, [
    'Places 6 and 7 win nothing, so only places 1-5 matter.',
    'Blue Comets: 6, 7, 7, 5, 4, 1 → 10,000 + 20,000 + 120,000 = 150,000.',
    'Iron Eagles: 7, 5, 6, 7, 5, 7 → 10,000 + 10,000 = 20,000.',
    'Blue Comets earned 150,000 − 20,000 = 130,000 shekels more.'], S2)
mk('ch-q10', 2, 231, 5, C2_INTRO,
   'It is known that all seven teams took part in the race in 2016. That year, the teams "Night Owls" and "Red Arrows" reached '
   'first place together, and the sum of the prizes for first place and for second place was divided equally between the two teams. '
   'The division of the prizes for places 3-7 did not change.\n'
   'The average prize per team in 2016 was ______ the average prize per team in 2017.',
   ['equal to', r'$\frac{5}{6}$ of', r'$\frac{6}{7}$ of', r'$\frac{7}{6}$ of'], 1, [
    'In 2016 the two winners shared 120,000 + 80,000, so the total prize money was the same as in any other year: 280,000 shekels.',
    'The same 7 teams share the same total, so the average is the same: 280,000 ÷ 7 = 40,000 in both years.'], S2)

# ---------------- Chart 3 (book p. 232-233; key 3 3 4 2 1) ----------------
mk('ch-q11', 3, 232, 1, C3_INTRO,
   'A "happy wedding" is a wedding with an equal number of guests from the groom\'s side and from the bride\'s side. '
   'On which day was a "happy wedding" held in the hall?', ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 3, [
    "Shared guests belong to both sides, so they add the same number to each side. Compare only the groom's side only with the bride's side only.",
    'It is the same wedding, so the percentages are enough: Monday 50% and 25%, Tuesday 25% and 50%, Wednesday 35% and 35%, Thursday 30% and 50%.',
    'Only on Wednesday are they equal.'], S3)
mk('ch-q12', 3, 233, 2, C3_INTRO,
   "How many of the guests who came to the wedding held in the hall on Tuesday were from the bride's side and not from the groom's side?",
   ['125', '200', '250', '375'], 3, [
    "\"From the bride's side and not from the groom's side\" = the bride's side only (not the shared guests).",
    'Tuesday: 500 guests, 50% of them from the bride\'s side only: 250.',
    '375 includes the shared guests (75%); 125 is the groom\'s side only or the shared guests.'], S3)
mk('ch-q13', 3, 233, 3, C3_INTRO,
   'The photographer Daniel worked in the hall on one day last week, and photographed exactly 1% of the wedding guests. '
   'Which of the following cannot be the day on which Daniel worked?', ['Sunday', 'Monday', 'Tuesday', 'Thursday'], 4, [
    '1% of the guests must be a whole number of people, so the number of guests must be a multiple of 100.',
    'Sunday 300 → 3, Monday 400 → 4, Tuesday 500 → 5, Thursday 350 → 3.5 guests: impossible.'], S3)
mk('ch-q14', 3, 233, 4, C3_INTRO,
   "On which day was the number of guests from the groom's side (only or shared) the greatest?",
   ['Sunday', 'Monday', 'Tuesday', 'Thursday'], 2, [
    "Groom's side = groom's side only + shared. Multiply the percentage by the number of guests.",
    'Sunday 80% of 300 = 240. Monday 75% of 400 = 300. Tuesday 50% of 500 = 250. Thursday 50% of 350 = 175.',
    'Monday. Not the tallest bar (Tuesday) and not the largest percentage (Sunday).'], S3)
mk('ch-q15', 3, 233, 5, C3_INTRO,
   "At the wedding on Monday, the guests from the groom's side only gave a gift of 150 shekels on average. The guests from the "
   "bride's side only gave a gift of 250 shekels on average. The shared guests gave a gift of 350 shekels on average.\n"
   'What can be said about the average amount of money that each guest gave at the wedding on Monday?',
   ['It is less than 250 shekels', 'It is more than 250 shekels', 'It is equal to 250 shekels',
    'It cannot be determined from the information given'], 1, [
    'Monday: 50% of the guests gave 150, 25% gave 250 and 25% gave 350.',
    'Weighted average: 0.5·150 + 0.25·250 + 0.25·350 = 75 + 62.5 + 87.5 = 225 shekels, less than 250.',
    'Insight: 250 is exactly in the middle of 150 and 350. Half of the guests are at 150, so the average is pulled down below 250.'], S3)


# =====================================================================================================================
# verification: recompute every answer from the data; exactly one correct choice
# =====================================================================================================================
def _verify():
    pts = [(p, c, h) for p in C1 for c, h in C1[p]]
    def ans(qid): return QUESTIONS[qid]['correct'][0] + 1
    def one(qid, vals, good):
        hits = [k + 1 for k, v in enumerate(vals) if good(v)]
        assert hits == [ans(qid)], (qid, hits, ans(qid))
    # chart 1
    n60 = sum(c > 60 for p, c, h in pts); assert n60 == 6 and sum(c >= 59 for p, c, h in pts) == 7
    assert sum(h > 60 for p, c, h in pts) == 1 and 1 not in (7, 3, 6, 10)
    assert sum(c > 50 for p, c, h in pts) == 10
    one('ch-q01', [7, 3, 6, 10], lambda v: v == n60)
    best = [(p, c, h) for p, c, h in pts if all(c >= c2 and h <= h2 for p2, c2, h2 in pts)]
    assert len(best) == 1
    one('ch-q02', ['Venus', 'Neptune', 'Saturn', 'Mercury'], lambda v: v == best[0][0])
    rng = {p: max(c for c, h in C1[p]) - min(c for c, h in C1[p]) for p in C1}
    top = max(rng, key=rng.get); assert sorted(rng.values())[-1] > sorted(rng.values())[-2]
    one('ch-q03', ['Saturn', 'Mars', 'Venus', 'Neptune'], lambda v: v == top)
    def mono(p, sign):
        s = sorted(C1[p]); return all((b[1] - a[1]) * sign > 0 for a, b in zip(s, s[1:]))
    one('ch-q04', [('Venus', 1), ('Neptune', -1), ('Mercury', 1), ('Saturn', -1)], lambda v: mono(*v))
    one('ch-q05', C1_HIST, lambda v: v == c1_hbins())
    assert C1_HIST[1] == [4, 6, 7, 7, 7, 3, 1]
    # edges tell them apart: left edge leaves (2) and (4), right edge leaves (2)
    assert [h[0] == C1_HIST[1][0] for h in C1_HIST] == [False, True, False, True] and C1_HIST[3][6] != C1_HIST[1][6]
    for p, c, h in pts: assert min(h % 10, 10 - h % 10) >= 1.5 or h < 1, (p, c, h)   # no sample on a hydrogen bin border
    # chart 2
    for k in range(6): assert sorted(PLACE[t][k] for t in TEAMS) == list(range(1, 8))
    firsts = {t: PLACE[t].count(1) for t in TEAMS}
    one('ch-q06', ['Road Runners', 'Desert Foxes', 'Red Arrows', 'Silver Wolves'], lambda v: firsts[v] == 2)
    assert all(firsts[t] == 1 for t in ('Road Runners', 'Red Arrows', 'Silver Wolves'))
    ch = [abs(a - b) for t in TEAMS for a, b in zip(PLACE[t], PLACE[t][1:])]
    dram = sum(d >= 3 for d in ch)
    assert sum(d > 3 for d in ch) == 3 and sum(1 for t in TEAMS for a, b in zip(PLACE[t], PLACE[t][1:]) if a - b >= 3) == 5
    one('ch-q07', [9, 5, 3, 12], lambda v: v == dram)
    avg = sum(PRIZE[p] for p in PLACE['Night Owls']) / 6
    one('ch-q08', [50000, 55000, 60000, 72000], lambda v: v == avg)
    bc, ie = sum(PRIZE[p] for p in PLACE['Blue Comets']), sum(PRIZE[p] for p in PLACE['Iron Eagles'])
    one('ch-q09', [(130000, -1), (150000, -1), (130000, 1), (150000, 1)], lambda v: v[0] == abs(bc - ie) and v[1] * (bc - ie) > 0)
    tot17 = sum(PRIZE.values()); tot16 = 2 * ((PRIZE[1] + PRIZE[2]) / 2) + sum(PRIZE[k] for k in range(3, 8))
    one('ch-q10', [1, 5 / 6, 6 / 7, 7 / 6], lambda v: abs(v - (tot16 / 7) / (tot17 / 7)) < 1e-9)
    assert C2_INTRO.count('2019') and PLACE['Night Owls'][YEARS.index(2019)] == 2 and PRIZE[2] == 80000
    # chart 3
    cnt = {d: [GUESTS[d] * s / 100 for s in SPLIT[d]] for d in DAYS}
    for d in DAYS: assert sum(SPLIT[d]) == 100 and all(x == int(x) for x in cnt[d])
    assert GUESTS['Sunday'] == 300 and SPLIT['Sunday'][0] == 60
    one('ch-q11', ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], lambda d: cnt[d][0] + cnt[d][2] == cnt[d][1] + cnt[d][2])
    one('ch-q12', [125, 200, 250, 375], lambda v: v == cnt['Tuesday'][1])
    one('ch-q13', ['Sunday', 'Monday', 'Tuesday', 'Thursday'], lambda d: GUESTS[d] % 100 != 0)
    groom = {d: cnt[d][0] + cnt[d][2] for d in DAYS}
    one('ch-q14', ['Sunday', 'Monday', 'Tuesday', 'Thursday'], lambda d: groom[d] == max(groom[x] for x in ('Sunday', 'Monday', 'Tuesday', 'Thursday')))
    g = SPLIT['Monday']; w = (g[0] * 150 + g[1] * 250 + g[2] * 350) / 100
    one('ch-q15', ['lt', 'gt', 'eq', 'na'], lambda v: v == ('lt' if w < 250 else 'gt' if w > 250 else 'eq'))
    assert w == 225
    return True


_verify()


# =====================================================================================================================
# slide helpers: question on top, the chart as its own item (so highlight lines can be drawn over it), notes on the right
# =====================================================================================================================
CW = 680.0                        # chart width on the slide
RX, RW = 1112, 428                # right-hand column for pop-ins


def _stem_y(stem):
    lines = max(1, -(-len(stem) * 30 * .5 // 1130))
    return 78 + lines * 40 + 26


def _chart_item(svg, vb, y, w=CW):
    return dict(k='vis', v={'type': 'geometry', 'svg': svg}, x=410, y=round(y), w=round(w, 1), h=round(w * vb[1] / vb[0], 1))


SLIDE = {   # shorter question text for the slides (the full text is in the question itself)
    'ch-q02': 'A region is more suitable for human habitation the more carbon and the less hydrogen in its soil. '
              'On which planet is the most suitable region?',
    'ch-q05': 'Which graph describes the number of samples (all five planets together) in each range of hydrogen percentages?',
    'ch-q07': 'A "dramatic change" = a change of 3 places or more between two consecutive races. '
              'How many "dramatic changes" occurred in 2017-2022?',
    'ch-q10': 'In 2016, two teams tied for 1st and split the 1st + 2nd prizes equally (places 3-7 unchanged). '
              'The average prize per team in 2016 was ___ that of 2017.',
    'ch-q11': 'A "happy wedding" has equal numbers of guests from the groom\'s side and from the bride\'s side. '
              'On which day was a "happy wedding" held?',
    'ch-q13': 'A photographer worked on one day and photographed exactly 1% of the wedding guests. '
              'Which of the following cannot be that day?',
    'ch-q15': "Monday: the groom's side only gave 150 on average, the bride's side only 250, the shared guests 350. "
              'What about the average gift per guest?',
}


def QC(qid, stem=None, fig=None, vb=None):
    """pre-loaded question (short stem, no own figure) + the chart below it, as large as the free space allows."""
    st = stem or SLIDE.get(qid) or SHORT[qid]
    y = _stem_y(st)
    chart = {1: (S1, C1_VB), 2: (S2, C2_VB), 3: (S3, C3_VB)}[int(QUESTIONS[qid]['setTitle'][-1])]
    svg, v = (fig, vb) if fig else chart
    long = any(len(rich_plain(c)) > 30 for c in QUESTIONS[qid]['choicesRich'])
    top = (900 - 24 - 4 * 58 - 3 * 8) if long else (900 - 24 - 2 * 74 - 14)
    w = min(786.0, (top - 16 - y) * v[0] / v[1])
    return {'pre': [Q(qid, stem=st, nofig=True, size=30), _chart_item(svg, v, y, w)], 'y': y, 'w': w}


def R(t, y=None, size=25):
    """pop-in in the right-hand column (x and width are set per slide in G, next to the chart)."""
    return T(t, size=size, x=RX, y=y or 190, w=RW)


def HL(x1, y1, x2):
    """amber highlight line (horizontal), in chart viewBox coords (placed over the chart in G)."""
    return dict(k='bar', d=1, n=1, hl=(x1, y1, x2, y1))


def VL(x, y1, y2):
    return dict(k='bar', d=1, n=1, hl=(x, y1, x, y2))


def _place(it, o):
    it = dict(it)
    if it.get('k') == 't' and it.get('x') == RX:
        it['x'] = round(410 + o['w'] + 26); it['w'] = 1540 - it['x']
    if 'hl' in it:
        x1, y1, x2, y2 = it.pop('hl'); s = o['w'] / 900.0
        if y1 == y2: it.update(x=round(410 + x1 * s, 1), y=round(o['y'] + y1 * s - 2, 1), w=round((x2 - x1) * s, 1), h=4)
        else: it.update(x=round(410 + x1 * s - 2, 1), y=round(o['y'] + y1 * s, 1), w=4, h=round((y2 - y1) * s, 1))
    return it


def G(i, qid, group, intro, slides):
    """slides: (title, script, layout) with the layout from QC()."""
    out = []
    for t, sc, o in slides:
        sc = [('A', x[1], _place(x[2], o)) if isinstance(x, tuple) and x[0] == 'A' else x for x in sc]
        out.append((t, sc, {'pre': o['pre']}))
    return guided(i, qid, group, SB, intro, out, T52)


SB = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5']
G1, G2, G3 = 'Chart 1 · Soil Samples', 'Chart 2 · Car Races', 'Chart 3 · Wedding Hall'

# per-question layouts
L = {q: QC(q) for q in QUESTIONS}
L5opt = QC('ch-q05', fig=FIG['ch-q05-options'], vb=C1_OPT_VB)


def withx(o, *extra):
    return {'pre': o['pre'] + list(extra), 'y': o['y']}


# =====================================================================================================================
MODULES = [
# ------------------------------------------------------------------ lesson: how to attack a chart set
lesson('ch52-practice-intro', 'Solving a Chart Set',
 ['A set of questions', 'Intro and example', 'Read the chart', 'Then the questions', 'Solve by eye'], [
 dict(mode='title', title='Solving a Chart Set', script=[
  "Practice: three chart sets from the course book, with new numbers.",
  "Before we start — how do we attack a chart set on the exam?",
 ]),
 dict(mode='concept', active=0, title='A set of questions', script=[
  A("One chart, 4-5 questions appears", T('One chart or table → 4 or 5 questions', size=44)),
  "In the quantitative section there's a chart or a table, and after it four or five questions.",
  A("5-6 minutes appears", T('About 5-6 minutes for the whole set', size=40)),
  "Recommended time: five to six minutes — a little more than a minute per question.",
  A("Easy to hard appears", T('The questions go from easy to hard', size=40)),
  "The questions go from easy to hard. The first one is usually just pulling one fact out of the chart.",
 ]),
 dict(mode='concept', active=1, title='Intro and example', script=[
  A("Intro + example appears", T('Before the chart: an explanation, and at its end — an example', size=40)),
  "Before every chart there's an explanation of what it shows, and at the end of it — almost always — an example.",
  A("Example = test appears", T('The example is your test: find it in the chart', size=40)),
  "The example is the most important thing. Read it, go to the chart, and check that you see exactly what it says.",
  A("Not clear → reread appears", T("Don't understand the example? Read again, slowly — or come back later", size=36)),
  "If you don't understand the example, you don't understand the chart. Read again slowly — or leave the set for the end of the section.",
 ]),
 dict(mode='concept', active=2, title='Read the chart', script=[
  A("1-1.5 minutes appears", T('Spend 1 to 1.5 minutes on the chart itself', size=40)),
  "Invest a minute, a minute and a half, in the chart itself — before you look at any question.",
  A("Axes, units, legend, notes appears", T('Axes · units · legend · notes', size=44)),
  "Titles, axes, units — thousands, percent — the legend, and every note. A note is there for a reason.",
  A("Chart 1 appears", _chart_item(S1, C1_VB, 390, 560)),
  "Here, for example: two axes that both go up to 60 percent and more — and a note: the exact location of each shape is its centre.",
 ]),
 dict(mode='concept', active=3, title='Then the questions', script=[
  A("Each question alone appears", T('Each question stands alone', size=44)),
  "Now the questions. Each one stands alone: information given inside one question does not carry over to the next.",
  A("Circle the key word appears", T('Circle the key word: carbon or hydrogen? only or shared?', size=38)),
  "Circle the key word in each question, so you check exactly what's asked — and not the axis next to it.",
  A("Not in the choices → stop appears", T("Your answer isn't among the choices? Stop and check yourself", size=38)),
  "And if your answer isn't one of the choices — don't panic. Stop, and check the legend, the axis and the question again.",
 ]),
 dict(mode='concept', active=4, title='Solve by eye', script=[
  A("By eye appears", T('Solve by eye: lines, edges, comparisons — calculate only when needed', size=38)),
  "Most chart questions are solved by eye: draw a line, compare lengths, look at a corner. Calculate only when you must.",
  A("Mini-charts: differences appears", T('Graphs as answers → check only where they differ, edges first', size=38)),
  "When the answers are small graphs, don't check each one to the end. Find where they differ — usually the edges.",
  "Let's start with the first chart.",
 ]),
], T52),

# =================================================================== CHART 1
G(0, 'ch-q01', G1,
 ["The first chart: soil samples from five planets.", "A minute on the chart first — then the first question, pulling one fact out of it."],
 [('Read the chart', [
   "The graph shows the percentage of carbon and of hydrogen in soil samples from five planets. Each shape is one sample; the legend tells us the planet.",
   A("Carbon = horizontal appears", R('Carbon → horizontal axis', 200)),
   "Carbon is the horizontal axis. Hydrogen is the vertical axis.",
   A("Hydrogen = vertical appears", R('Hydrogen → vertical axis')),
   "And the note: the exact location of each shape is its centre. Keep that in mind — it will matter right away.",
   A("Centre note appears", R('Exact location = the centre of the shape')),
  ], L['ch-q01']),
  ('Draw a line at 60%', [
   "In how many of the samples is the percentage of carbon greater than 60 percent?",
   "Carbon — the horizontal axis. We want more than 60, so draw a boundary line at 60 percent. In your head or on the figure.",
   A("60% line appears", VL(c1x(60), C1_YT, C1_YB)),
   D("Draw a vertical line at 60% carbon"),
   "Everything to the right of the line: three Mercury dots — one, two, three. And three Neptune rings — four, five, six.",
   A("6 samples appears", R('Right of the line: 3 Mercury + 3 Neptune = 6', 200)),
   "What about this ring, right on the line? Its edge touches the line, but its centre is at 59 percent — to the left. The centre is what counts, so it's out.",
   A("59% ring out appears", R('The ring at 59%: centre left of the line → not counted')),
   "Six samples.",
   D("Circle choice 3"),
  ], L['ch-q01']),
  ('Which 60%?', [
   "One more thing. It happens under pressure: instead of the 60 percent of carbon, you check the 60 percent of hydrogen.",
   A("Wrong 60% line appears", HL(C1_X0, c1y(60), C1_X1)),
   "Above 60 percent hydrogen there is just one sample. And 1 isn't among the choices.",
   A("Stop and check appears", R("Got an answer that isn't a choice? Stop — check the axis and the legend", 200)),
   "So before you panic — stop. If you got a number that isn't in the choices, check yourself: the legend, the axis, exactly what was asked.",
  ], L['ch-q01'])]),

G(1, 'ch-q02', G1,
 ["Second question on the soil samples.", "A definition inside the question — and we solve it by eye."],
 [('Where to look', [
   "A region is more suitable for people the higher the carbon in its soil, and the lower the hydrogen. On which planet is the most suitable region?",
   "We don't start checking the exact percentages of every sample. We look visually.",
   A("High carbon → right appears", R('More carbon → the right side', 200)),
   "High carbon — the right side of the graph.",
   A("Low hydrogen → bottom appears", R('Less hydrogen → the bottom')),
   "Low hydrogen — the bottom of the graph. So: the right side and the bottom — the bottom-right corner.",
   A("Carbon line appears", VL(c1x(60), C1_YT, C1_YB)),
   A("Hydrogen line appears", HL(C1_X0, c1y(10), C1_X1)),
   D("Shade the bottom-right corner"),
  ], L['ch-q02']),
  ('The corner', [
   "What's in the corner? Neptune rings. And the ring at 74 percent carbon and 3 percent hydrogen is the extreme one: the most carbon of all the samples, and the least hydrogen.",
   A("Neptune appears", R('Bottom-right corner: Neptune (74% carbon, 3% hydrogen)', 200)),
   "Mercury? It has samples with a lot of carbon — but look how high they are. A lot of hydrogen too.",
   D("Circle choice 2"),
   "Neptune — choice two.",
  ], L['ch-q02'])]),

G(2, 'ch-q03', G1,
 ["Third question: the range.", "Range — from the smallest to the largest. And again, by eye."],
 [('What is a range', [
   "The largest range of carbon percentages is found in the samples from which planet?",
   A("Range appears", R('Range = the leftmost sample → the rightmost sample', 200)),
   "Range of carbon: in each planet, the leftmost sample and the rightmost sample — carbon is the horizontal axis.",
   "I don't calculate 8 percent here and 55 there and subtract. I just draw a line from the leftmost to the rightmost, and compare the lengths.",
  ], L['ch-q03']),
  ('Compare the lines', [
   "Venus: the squares, from about 10 to 30. A short line.",
   A("Venus range appears", HL(c1x(10), c1y(50), c1x(30))),
   "Saturn: the triangles. The leftmost is near 8 percent, the rightmost at 55. Already much longer than Venus — cross out Venus.",
   A("Saturn range appears", HL(c1x(8), c1y(30), c1x(55))),
   D("Cross out choice 3"),
   "Mars: the diamonds, from 20 to 50. Shorter than Saturn.",
   A("Mars range appears", HL(c1x(20), c1y(39), c1x(50))),
   D("Cross out choice 2"),
   "Neptune: the rings, from 40 to 74. Also shorter than Saturn's line.",
   A("Neptune range appears", HL(c1x(40), c1y(5), c1x(74))),
   D("Cross out choice 4"),
   A("Saturn longest appears", R('Longest line: Saturn (8% → 55%)', 200)),
   D("Circle choice 1"),
   "Saturn — choice one. That's one of the main ways we solve chart questions: visually, not by calculating.",
  ], L['ch-q03'])]),

G(3, 'ch-q04', G1,
 ["Fourth question: which statement is necessarily true.", "Before checking one by one — look at all the choices together."],
 [('Look at all four', [
   "Which of the following is necessarily true?",
   "Usually we'd read the first choice and go to the chart. But first look at all four: they're all the same idea.",
   A("Same idea appears", R('Every choice: a steady relation between carbon and hydrogen on one planet', 200)),
   "Each time a planet, and a relation: more carbon — more hydrogen, or more carbon — less hydrogen. Direct or inverse.",
   "So look at the whole chart: is there a planet whose samples form a line — a trend?",
   D("Draw a line through the Mercury dots"),
   A("Mercury trend appears", R('Mercury: the dots rise in a straight line → more carbon, more hydrogen')),
   "One jumps right out: the Mercury dots. The more carbon, the more hydrogen. All the others are a kind of cloud.",
  ], L['ch-q04']),
  ('Check the others', [
   "Let's still check them in detail. Venus: as carbon rises, hydrogen goes up, then down, then up again. Not steady — out.",
   D("Cross out choice 1"),
   "Neptune: careful here. Almost all the way the hydrogen goes down — but from 46 to 52 percent carbon it goes up, from 12 to 16.",
   A("Neptune exception appears", R('Neptune: 46% → 52% carbon, hydrogen 12% → 16% — goes up', 200)),
   "\"Necessarily\" means no exceptions. One exception is enough — out.",
   D("Cross out choice 2"),
   "Saturn: up, down, up — no steady trend. Out.",
   D("Cross out choice 4"),
   "Mercury — every step to the right is also a step up.",
   D("Circle choice 3"),
   "Choice three.",
  ], L['ch-q04'])]),

G(4, 'ch-q05', G1,
 ["Last question of the set: which graph is right.", "A different kind of question — but a very common one: the answers are small graphs."],
 [('Four mini-graphs', [
   "Which graph describes the number of samples from all five planets together in each range of hydrogen percentages?",
   "A small tip: circle the word hydrogen, so you remember that's what you check — and not carbon.",
   D("Circle the word hydrogen"),
   A("Hydrogen = vertical appears", R('Hydrogen → the vertical axis of the big graph', 200)),
   "The data of these mini-graphs comes from the big graph, and only one of them is right.",
   "We won't check graph one bin by bin, then graph two... We look for the places where the graphs differ — and the easiest place is usually the edges.",
   A("Edges first appears", R('Check only where they differ — edges first')),
   "The left edge — below 10 percent: the graphs show 1, 4, 5 and 4. Whatever the count is, it throws out at least two graphs.",
  ], L5opt),
  ('The left edge', [
   "So — hydrogen below 10 percent. Draw a line at 10 percent hydrogen and count what's under it.",
   A("10% line appears", HL(C1_X0, c1y(10), C1_X1)),
   "One — the Mercury dot at 6. Two, three, four — the Neptune rings. Centres, remember. Four samples.",
   A("Below 10%: 4 appears", R('Below 10% hydrogen: 4 samples → (2) or (4)', 200)),
   "Graphs one and three show 1 and 5 — out. We're left with two and four.",
   D("Cross out choices 1 and 3"),
  ], L['ch-q05']),
  ('The right edge', [
   "Now tell two and four apart. The middle is possible — but between 30 and 40 I'd need two lines and a careful count. The edge is easier.",
   "The other edge: from 60 to 70 percent hydrogen. Graph two says 1, graph four says 3.",
   A("60% line appears", HL(C1_X0, c1y(60), C1_X1)),
   "Above the line — just one square, Venus at 64.",
   A("Above 60%: 1 appears", R('60% to 70% hydrogen: 1 sample → graph (2)', 200)),
   "Graph four is out.",
  ], L['ch-q05']),
  ('Graph two', [
   "Graph two is right.",
   D("Circle choice 2"),
   A("Graph 1 = carbon appears", R('Graph (1) = carbon instead of hydrogen — the axis trap', 200)),
   "And graph one? It's what you get if you count carbon instead of hydrogen. That's why we circle the word.",
   "So: in questions with mini-graphs we don't check each graph to the end. Find the points where they differ, start with the edges — usually that's enough.",
  ], L5opt)]),

# =================================================================== CHART 2
G(0, 'ch-q06', G2,
 ["The second chart: a table of car races.", "First the table and the example — then the first question."],
 [('Read the tables', [
   "Two tables. On the left: seven teams, six years, and the place each team reached in each race. On the right: the prize for each place.",
   A("Two tables appears", R('Left: place by year · Right: prize by place', 200)),
   "Check with the example: in 2019, Night Owls came second and won 80,000. Night Owls row, 2019 column — 2. Second place in the prize table — 80,000. We understand the table.",
   A("Example row appears", HL(C2_TX, c2_row_bottom('Night Owls'), C2_TX + C2_TW + 6 * C2_YW)),
   A("Example checks appears", R('Night Owls, 2019: place 2 → 80,000 ✓')),
   "Notice: places 6 and 7 win nothing.",
  ], L['ch-q06']),
  ('Find the 1s', [
   "Which team won 120,000 shekels twice?",
   "First translate the money into a place: 120,000 is first place. So we're looking for the 1s.",
   A("120,000 = 1st appears", R('120,000 = first place → look for the 1s', 200)),
   "Go year by year — each column has exactly one 1. 2017: Desert Foxes. 2018: Red Arrows. 2019: Silver Wolves. 2020: Road Runners. 2021: Desert Foxes again. 2022: Blue Comets.",
   A("Desert Foxes twice appears", R('Desert Foxes: 1st in 2017 and 2021')),
   "Only Desert Foxes came first twice.",
   D("Circle choice 2"),
   "Choice two.",
  ], L['ch-q06'])]),

G(1, 'ch-q07', G2,
 ["Second question on the car races: a definition, and a careful count.", "A question that takes time rather than insight — so work in order."],
 [('Row by row', [
   "A dramatic change: a change of three places or more between two consecutive races. How many were there?",
   A("3 or more appears", R('3 or more — a change of exactly 3 counts too', 200)),
   "Circle \"or more\": a change of exactly three counts.",
   "Work row by row: each team, each year against the next. And the steady teams go fast — Night Owls: 2, 3, 2, 3, 2, 4. Nothing. Iron Eagles: 7, 5, 6, 7, 5, 7. Nothing.",
   A("Zero rows appears", R('Night Owls, Iron Eagles: 0')),
  ], L['ch-q07']),
  ('Count', [
   "Road Runners: 4 to 2 — no. 2 to 5 — yes. 5 to 1 — yes. Two.",
   A("RR 2 appears", R('Road Runners: 2→5, 5→1 → 2', 190, 25)),
   "Desert Foxes: 1 to 6, 6 to 3, and 4 to 1. Three.",
   A("DF 3 appears", R('Desert Foxes: 1→6, 6→3, 4→1 → 3', None, 25)),
   "Blue Comets: only the jump from 4 to 1. One. Red Arrows: 1 to 4. One.",
   A("BC RA appears", R('Blue Comets 1 · Red Arrows 1', None, 25)),
   "Silver Wolves: 4 to 1, and 2 to 6. Two.",
   A("SW 2 appears", R('Silver Wolves: 4→1, 2→6 → 2', None, 25)),
   "Total: 2 plus 3 plus 1 plus 1 plus 2 — nine.",
   A("Total 9 appears", R('2 + 3 + 1 + 1 + 2 = 9', None, 30)),
   D("Circle choice 1"),
   "Choice one. If you got 3, you counted only changes of more than three places.",
  ], L['ch-q07'])]),

G(2, 'ch-q08', G2,
 ["Third question: an average.", "Places into prizes — and a short sum."],
 [('Places → prizes', [
   "What is the average amount the Night Owls won per year?",
   A("Night Owls row appears", HL(C2_TX, c2_row_bottom('Night Owls'), C2_TX + C2_TW + 6 * C2_YW)),
   "Night Owls row: 2, 3, 2, 3, 2, 4.",
   A("Places appears", R('Places: 2, 3, 2, 3, 2, 4', 200)),
   "Group them: three times second place — 3 times 80,000 is 240,000. Twice third — 100,000. Once fourth — 20,000.",
   A("Prizes appears", R('3·80,000 + 2·50,000 + 20,000 = 360,000')),
  ], L['ch-q08']),
  ('Divide by 6', [
   "360,000 over six years.",
   A("Average appears", R('360,000 ÷ 6 = 60,000', 200, 30)),
   "60,000.",
   D("Circle choice 3"),
   "Choice three. 72,000 is the trap: dividing by 5 instead of 6. Six years — 2017 to 2022 inclusive.",
  ], L['ch-q08'])]),

G(3, 'ch-q09', G2,
 ["Fourth question: two teams, over all the years.", "A shortcut: most of the places win nothing."],
 [('Only places 1-5', [
   "Over the years, Blue Comets earned how much more — or less — than Iron Eagles?",
   A("6-7 = 0 appears", R('Places 6 and 7 win 0 → skip them', 200)),
   "Places 6 and 7 win nothing, so skip them.",
   A("BC row appears", HL(C2_TX, c2_row_bottom('Blue Comets'), C2_TX + C2_TW + 6 * C2_YW)),
   "Blue Comets: 6, 7, 7 — nothing. Then 5, 4, 1: 10,000 plus 20,000 plus 120,000 — 150,000.",
   A("BC total appears", R('Blue Comets: 10,000 + 20,000 + 120,000 = 150,000')),
   A("IE row appears", HL(C2_TX, c2_row_bottom('Iron Eagles'), C2_TX + C2_TW + 6 * C2_YW)),
   "Iron Eagles: 7, 5, 6, 7, 5, 7 — two fifth places: 20,000.",
   A("IE total appears", R('Iron Eagles: 2 · 10,000 = 20,000')),
  ], L['ch-q09']),
  ('More or less', [
   "150,000 minus 20,000 — 130,000. And Blue Comets earned more.",
   A("130,000 more appears", R('150,000 − 20,000 = 130,000 → more', 200, 30)),
   "Check both blanks: the number and the direction. 150,000 is Blue Comets' total — you forgot to subtract.",
   D("Circle choice 3"),
   "Choice three.",
  ], L['ch-q09'])]),

G(4, 'ch-q10', G2,
 ["Last question on the car races — the hardest of the set.", "It looks like a calculation. It's really an insight."],
 [('What changed?', [
   "In 2016, Night Owls and Red Arrows tied for first place. The first and second prizes were added together and split equally between them. Places 3 to 7 — no change.",
   "How does the average prize per team in 2016 compare with 2017?",
   A("Total unchanged appears", R('1st + 2nd prizes: shared, but the same money', 200)),
   "Think about the total. The two winners share 120,000 plus 80,000 — the same 200,000 as always. The other prizes are unchanged.",
   A("Same total appears", R('Total 2016 = total 2017 = 280,000')),
  ], L['ch-q10']),
  ('Same average', [
   "Same total money, same seven teams — the same average.",
   A("Same average appears", R('280,000 ÷ 7 = 40,000 in both years', 200)),
   "If you want a number: 280,000 over 7 — 40,000 in both years. But you don't need it.",
   D("Circle choice 1"),
   "Choice one: equal. In the last question of a set, look for the idea before you calculate.",
  ], L['ch-q10'])]),

# =================================================================== CHART 3
G(0, 'ch-q11', G3,
 ["The third chart: weddings in an event hall.", "Bars and pies together — first understand both, and the example."],
 [('Read the chart', [
   "Each bar: the number of guests at that day's wedding. Above each bar, a pie: how the guests divide — groom's side only, bride's side only, and shared.",
   A("Bars and pies appears", R('Bar = number of guests · Pie = the split in %', 200)),
   "Check with the example: Sunday, 300 guests — the Sunday bar reaches 300. 60 percent from the groom's side only — the dark slice on Sunday's pie says 60. Good.",
   A("Example checks appears", R("Sunday: 300 guests, 60% groom's side only ✓")),
  ], L['ch-q11']),
  ('Shared counts twice', [
   "A happy wedding: an equal number of guests from the groom's side and from the bride's side. On which day?",
   "Careful: the shared guests are on both sides. They add the same amount to the groom's side and to the bride's side.",
   A("Compare only-only appears", R("Shared is on both sides → compare groom's only with bride's only", 200)),
   "So compare only the groom's-only slice with the bride's-only slice. It's the same wedding, so the percentages are enough.",
   "Monday: 50 and 25. Tuesday: 25 and 50. Wednesday: 35 and 35. Thursday: 30 and 50.",
   A("Wednesday appears", R('Wednesday: 35% = 35%')),
   "Tuesday is the trap: groom's side with the shared is 50 — the same as the bride's-only 50. But then you gave the shared guests to one side only.",
   D("Circle choice 3"),
   "Wednesday — choice three.",
  ], L['ch-q11'])]),

G(1, 'ch-q12', G3,
 ["Second question on the weddings.", "One bar, one slice."],
 [('One slice', [
   "How many of the guests at Tuesday's wedding were from the bride's side and not from the groom's side?",
   "\"And not from the groom's side\" — so not the shared ones. Only the bride's-only slice.",
   A("Bride only appears", R("Bride's side, not groom's = bride's only", 200)),
   A("500 line appears", HL(C3_X0, c3y(500), C3_X1)),
   "Tuesday: the bar reaches 500. The bride's-only slice: 50 percent. Half of 500 — 250.",
   A("250 appears", R('50% of 500 = 250')),
   D("Circle choice 3"),
   "Choice three. 375 adds the shared guests — exactly what the question excluded.",
  ], L['ch-q12'])]),

G(2, 'ch-q13', G3,
 ["Third question on the weddings.", "Which day cannot be — look for what breaks."],
 [('Whole people', [
   "The photographer worked one day and photographed exactly 1 percent of the guests. Which day cannot be?",
   "What could break here? People come whole. 1 percent of the guests must be a whole number.",
   A("Whole number appears", R('1% of the guests must be a whole number of people', 200)),
   "So the number of guests must be a multiple of 100. Sunday 300 — 3 people. Monday 400 — 4. Tuesday 500 — 5.",
   A("350 line appears", HL(C3_X0, c3y(350), C3_X1)),
   "Thursday: the bar stops between 300 and 400 — at 350. 1 percent of 350 is 3.5 people. Impossible.",
   A("3.5 appears", R('Thursday: 1% of 350 = 3.5 → impossible')),
   D("Circle choice 4"),
   "Choice four.",
  ], L['ch-q13'])]),

G(3, 'ch-q14', G3,
 ["Fourth question on the weddings.", "Percent of a total — both numbers matter."],
 [('Percent times total', [
   "On which day was the number of guests from the groom's side — only or shared — the greatest?",
   A("Groom side appears", R("Groom's side = groom's only + shared", 200)),
   "Groom's side: the groom's-only slice plus the shared slice. And it's a number of people, so percent times the bar.",
   "Sunday: 60 plus 20 — 80 percent of 300: 240. Monday: 75 percent of 400: 300.",
   A("Sun Mon appears", R('Sunday 80% · 300 = 240 · Monday 75% · 400 = 300')),
   "Tuesday: 50 percent of 500: 250. Thursday: 50 percent of 350: 175.",
   A("Tue Thu appears", R('Tuesday 50% · 500 = 250 · Thursday 50% · 350 = 175')),
  ], L['ch-q14']),
  ('Monday', [
   "Monday — 300.",
   D("Circle choice 2"),
   A("Two traps appears", R('Not the tallest bar (Tuesday), not the biggest % (Sunday)', 200)),
   "Choice two. And look at the two traps: the tallest bar is Tuesday, the biggest percentage is Sunday. Neither is the answer — you need both numbers.",
  ], L['ch-q14'])]),

G(4, 'ch-q15', G3,
 ["Last question of the set: an average.", "Can we say something without a full calculation?"],
 [('Weights', [
   "Monday: the groom's-only guests gave 150 on average, the bride's-only 250, the shared 350. What about the average gift per guest?",
   "Many answer: 150, 250, 350 — the average is 250. But that's only true if each group is the same size.",
   A("Weighted appears", R('The groups are not the same size → a weighted average', 200)),
   "Monday's pie: 50 percent groom's only, 25 bride's only, 25 shared. Half of the guests gave the lowest amount.",
   A("Monday split appears", R("Monday: 50% gave 150 · 25% gave 250 · 25% gave 350")),
  ], L['ch-q15']),
  ('Less than 250', [
   "250 sits exactly in the middle of 150 and 350. The 150 side has the bigger weight — so the average is pulled below 250.",
   A("Calc appears", R('0.5·150 + 0.25·250 + 0.25·350 = 225', 200)),
   "And in numbers: 75 plus 62.5 plus 87.5 — 225.",
   D("Circle choice 1"),
   "Less than 250 — choice one.",
  ], L['ch-q15'])]),
]

PRACTICE = {52: []}      # every practice question is solved in a guided video
MEMORY = []
