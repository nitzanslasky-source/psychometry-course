# Quantitative Reasoning · Topic 52 · Charts & Tables - the lessons (the practice sets are in modulesV52b.py).
# Backbone: the teacher's ten Hebrew lessons (charts_src/seg01-seg10): intro, tables, points on axes, line graph,
# bar chart, continuous line, range (min-max) + regions, circle chart, cumulative graph, change graph.
# Every example chart / table the teacher uses is RE-CREATED from the subtitles (charts_assets.py): same type, same
# story, every value he reads out; the other values are chosen to agree with everything he says about them.
# Rule for the slides: whenever the teacher talks about a chart, it is on the board (pre-loaded), and the point he
# talks about is highlighted in amber (the chart is drawn again with the highlight on the next slide).
import math
from dsl import *
from charts_assets import (vis, table, scatter, line, bar, continuous, range_chart, regions, radial, cumulative, change,
                           smooth, legend_strip, Frame, _r, _t, _l, _c, _svg, _tag, _yaxis, marker, INK, TEAL, AMBER, SOFT, GRID,
                           MUTED, AMBER_SOFT, GREY)

T52 = 52


# =====================================================================================================================
# layout helpers
# =====================================================================================================================
def side(svg, w=830):
    """Chart on the left of the board; notes go in the right-hand column (NS)."""
    return vis(svg, w=w, x=345, y=92)


def wide(svg, w=1060, y=82):
    return vis(svg, w=w, x=345 + (1250 - w) // 2, y=y)


class Notes:
    """Stacks text items (estimates wrapped height)."""
    def __init__(self, x=1195, y=110, w=390, size=27, gap=18):
        self.x, self.y, self.w, self.size, self.gap = x, y, w, size, gap

    def __call__(self, text, size=None, gap=None):
        z = size or self.size
        it = T(text, size=z, x=self.x, y=self.y, w=self.w)
        rows = max(1, math.ceil(len(text) * 0.53 * z / self.w))
        self.y += int(rows * z * 1.3 + 4) + (self.gap if gap is None else gap)
        return it


def NS(): return Notes()                                   # right-hand column beside a side() chart
def NU(y, x=410, w=1130, size=30): return Notes(x=x, y=y, w=w, size=size)   # notes under a chart


def S(sb, active, script, pre=None):
    d = dict(mode='concept', active=active, title=sb[active], script=script)
    if pre: d['pre'] = pre
    return d


def TITLE(t, script): return dict(mode='title', title=t, script=script)


def hours(v): return '%d:00' % v


# =====================================================================================================================
# the re-created charts (data)
# =====================================================================================================================
# ---- intro: the chart-set page (schematic) ----
def set_page(hl=None):
    """A chart set as it appears in the exam: explanation + example, the chart, notes, then the questions."""
    W, H = 900, 560
    b = []
    def part(key, y, h, label):
        on = hl == key
        b.append(_r(20, y, 860, h, AMBER_SOFT if on else '#fff', AMBER if on else GRID, 4 if on else 2, 10))
        b.append(_t(40, y + 30, label, 20, '#8A5A00' if on else MUTED, 'start', 700))
    part('instr', 14, 46, 'Study the chart below, then answer the questions that follow.')
    part('expl', 70, 96, 'The explanation: what the chart describes')
    for k in range(2): b.append(_r(40, 112 + k * 18, 700 - k * 180, 8, GRID, rx=4))
    b.append(_t(40, 157, 'For example: in 2010, 60 thousand vehicles were sold.', 18, INK if hl != 'example' else '#8A5A00', 'start',
                700 if hl == 'example' else 400, True))
    if hl == 'example': b.append(_r(34, 138, 520, 28, 'none', AMBER, 3, 6))
    part('chart', 176, 250, 'The chart / table  (titles, units)')
    # a mini bar chart inside
    for k, v in enumerate([60, 80, 80, 100]):
        b.append(_r(330 + k * 90, 400 - v * 1.7, 50, v * 1.7, SOFT, INK, 2))
    b.append(_l(310, 400, 700, 400, INK, 2)); b.append(_l(310, 400, 310, 220, INK, 2))
    b.append(_t(300, 222, 'thousands', 15, MUTED, 'end', 600))
    b.append(_t(720, 396, 'Note: ...', 17, '#8A5A00' if hl == 'units' else MUTED, 'start', 700, True))
    if hl == 'units':
        b.append(_r(236, 206, 72, 24, 'none', AMBER, 3, 5)); b.append(_r(712, 376, 86, 28, 'none', AMBER, 3, 5))
    part('qs', 436, 110, 'The questions: 4 or 5, easy → hard')
    for k in range(5):
        b.append(_c(60 + k * 170, 500, 16, SOFT, TEAL, 2)); b.append(_t(60 + k * 170, 507, str(k + 1), 17, TEAL, 'middle', 700))
        b.append(_r(84 + k * 170, 494, 90 - k * 5, 10, GRID, rx=4))
    return _svg(W, H, ''.join(b), 'A chart set')


def chart_menu():
    """'Insert chart' - the same data can be shown as columns, a line or a pie."""
    W, H = 900, 300
    b = [_r(10, 10, 880, 280, '#F7FAF9', GRID, 2, 12), _t(40, 50, 'Insert chart', 22, INK, 'start', 700)]
    xs = [60, 350, 640]
    for k, name in enumerate(['Column', 'Line', 'Pie']):
        x = xs[k]
        b.append(_r(x, 75, 200, 170, '#fff', GRID, 2, 8))
        if k == 0:
            for j, v in enumerate([50, 80, 65, 110]): b.append(_r(x + 25 + j * 40, 225 - v, 26, v, TEAL))
        elif k == 1:
            b.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="4"/>' % (
                ' '.join('%d,%d' % (x + 25 + j * 50, 225 - v) for j, v in enumerate([40, 90, 70, 120])), TEAL))
        else:
            b.append('<path d="M %d 160 L %d 95 A 65 65 0 1 1 %d 160 Z" fill="%s"/>' % (x + 100, x + 100, x + 35, TEAL))
            b.append('<path d="M %d 160 L %d 160 A 65 65 0 0 1 %d 95 Z" fill="%s"/>' % (x + 100, x + 35, x + 100, SOFT))
        b.append(_t(x + 100, 275, name, 20, INK, 'middle', 600))
    return _svg(W, H, ''.join(b), 'Insert chart menu')


SIB_H = ['Age', 'Siblings\n(average)', 'Children\n(average)', 'Friends\n(average)', 'Salary, NIS\n(average)', 'Rooms at\nhome (avg.)']
SIB_R = [['21–30', '2.3', '0.4', '12', '6,200', '2.5'],
         ['31–40', '2.8', '1.6', '9', '8,300', '3.5'],
         ['41–50', '3.6', '2.5', '7', '10,100', '4.5']]


def sib_table(ncols=2, **k):
    return table(SIB_H[:ncols], [r[:ncols] for r in SIB_R], title='Ages and family data (averages)', W=900 if ncols > 3 else 150 * ncols + 300, **k)


SIM_A = smooth([(1, 480), (2, 540), (3, 585), (4, 620), (5, 645), (6, 660), (7, 670), (8, 676), (9, 679), (10, 681), (12, 683), (15, 685)], 0.1)
SIM_B = smooth([(1, 500), (2, 503), (3, 507), (4, 512), (5, 525), (6, 565), (7, 605), (8, 640), (9, 655), (10, 662), (11, 665), (13, 667), (15, 668)], 0.1)
SIM_C = smooth([(1, 500), (3, 504), (5, 508), (7, 512), (8, 516), (9, 525), (10, 560), (11, 600), (12, 635), (13, 660), (14, 675), (15, 685)], 0.1)


def sim_chart(curve, marks=(), title='Score by number of simulations', extra=None):
    return continuous(1, 15, 1, 450, 700, 50, curve=curve, ylabel='Score', xlabel='Simulation number', title=title,
                      ybreak=True, marks=marks, curves=[dict(pts=extra, color=GREY, dash='12 8')] if extra else None)


# ---- cars (tables, points, lines, bars) ----
YEARS = ['2010', '2011', '2012', '2013']
SOLD, PRIV, POWN, COMM = [60, 80, 80, 100], [45, 60, 62, 75], [40, 50, 50, 65], [4, 5, 5, 6]
CAR_H = ['Year', 'Vehicles\nsold', 'Private\ncars', 'Privately\nowned', 'Commercial,\nprivately owned']
CAR_ROWS = [[y, a, b, c, d] for y, a, b, c, d in zip(YEARS, SOLD, PRIV, POWN, COMM)]
CAR_TITLE = 'New vehicles sold in Israel, 2010–2013 (thousands)'


def car_table(ncols=5, **k):
    k.setdefault('W', max(640, 180 * ncols))
    return table(CAR_H[:ncols], [r[:ncols] for r in CAR_ROWS], title=CAR_TITLE, **k)


CAR_S = [dict(name='Vehicles sold', values=SOLD, marker='star'),
         dict(name='Private cars', values=PRIV, marker='dot'),
         dict(name='Privately owned', values=POWN, marker='star_o'),
         dict(name='Commercial,\nprivately owned', values=COMM, marker='x')]


def car_scatter(n=4, only=None, **k):
    ser = [dict(s) for s in CAR_S[:n]]
    if only is not None:
        ser = [dict(s, values=[v if i < only else None for i, v in enumerate(s['values'])]) for s in ser]
    kw = dict(ymin=0, ymax=110, ystep=10, ylabel='Thousands', title='Vehicles sold, 2010–2013')
    kw.update(k)
    return scatter(YEARS, ser, **kw)


STYLES = ['bold', 'solid', 'dash', 'dashdot']
CAR_NAMES = ['Vehicles sold', 'Private cars', 'Privately owned', 'Commercial, privately owned']
CAR_LEG = [('box', (f, INK), n_) for f, n_ in zip(['#fff', INK, GREY, SOFT], CAR_NAMES)]                 # bars
CAR_LEG_L = [('line', (st, INK), n_) for st, n_ in zip(STYLES, CAR_NAMES)]                              # lines
CAR_LEG_S = [('marker', (c['marker'], INK), n_) for c, n_ in zip(CAR_S, CAR_NAMES)]                    # points


def car_line(styles=True, points=False, **k):
    ser = [dict(name=s['name'], values=s['values'], style=STYLES[i] if styles else 'solid', marker=s['marker'])
           for i, s in enumerate(CAR_S)]
    kw = dict(ymin=0, ymax=110, ystep=10, ylabel='Thousands', title='Vehicles sold, 2010–2013', legend='right' if styles else None)
    kw.update(k)
    return line(YEARS, ser, points=points, **kw)


def car_bar(n=4, **k):
    ser = [dict(name=s['name'], values=s['values']) for s in CAR_S[:n]]
    kw = dict(ymin=0, ymax=110, ystep=10, ylabel='Thousands', title='Vehicles sold, 2010–2013')
    kw.update(k)
    return bar(YEARS, ser, **kw)


STACK = [dict(name='Private cars', values=[45, 55, 60, 70], fill=INK),
         dict(name='Commercial', values=[15, 25, 50, 45], fill=GREY),
         dict(name='Motorcycles', values=[5, 6, 8, 10], fill='#fff')]


def stack_chart(**k):
    return bar(YEARS, STACK, mode='stacked', ymin=0, ymax=140, ystep=20, ylabel='Thousands',
               title='Vehicles sold by a dealer group, 2010–2013', **k)


SCHOOLS = [dict(name='"Carob" school', values=[82, 75, 68, 88]), dict(name='"Zucchini" school', values=[70, 80, 77, 72])]
SUBJ = ['Maths', 'English', 'History', 'Literature']


def school_chart(**k):
    return bar(SUBJ, SCHOOLS, orient='h', panels=True, ymin=0, ymax=100, ystep=20, xlabel='Average grade',
               title='Average grades at the end of 10th grade', **k)


def overlap_fig(case):
    """2011: 80 thousand sold; 60 thousand private cars; 50 thousand privately owned. case 1 = the 50 all inside
    the 60 (bottom); case 2 = the 50 pushed to the top: only 30 are both."""
    W, H = 900, 520
    F = Frame(W, H, 0, 1, 0, 90, left=92, right=380, top=60, bottom=40)
    b = [_yaxis(F, 10, ylabel='Thousands (2011)')]
    b.append(_l(F.X0, F.Y0, F.X1, F.Y0, INK, 2.5))
    x0 = F.X0 + 70
    b.append(_r(x0, F.y(80), 300, F.y(0) - F.y(80), '#fff', INK, 2.5))
    b.append(_t(x0 + 150, F.y(80) - 10, 'Vehicles sold: 80', 19, INK, 'middle', 700))
    b.append(_r(x0 + 30, F.y(60), 100, F.y(0) - F.y(60), INK, INK, 2))
    b.append(_t(x0 + 80, F.y(14), 'Private', 17, '#fff', 'middle', 700)); b.append(_t(x0 + 80, F.y(14) + 22, '60', 19, '#fff', 'middle', 700))
    lo, hi = (0, 50) if case == 1 else (30, 80)
    b.append(_r(x0 + 170, F.y(hi), 100, F.y(lo) - F.y(hi), GREY, INK, 2))
    b.append(_t(x0 + 220, F.y((lo + hi) / 2), 'Privately', 17, INK, 'middle', 700))
    b.append(_t(x0 + 220, F.y((lo + hi) / 2) + 20, 'owned 50', 17, INK, 'middle', 700))
    both_lo, both_hi = max(0, lo), min(60, hi)
    b.append(_r(x0 + 12, F.y(both_hi), 276, F.y(both_lo) - F.y(both_hi), 'none', AMBER, 5, 4))
    b.append(_tag(x0 + 320, F.y((both_lo + both_hi) / 2) + 8, 'both: %d' % (both_hi - both_lo)))
    b.append(_t(W - 20, 40, 'Case %d' % case, 24, INK, 'end', 700))
    b.append(_t(W - 20, 72, 'all 50 inside the 60' if case == 1 else 'the 50 pushed to the top', 19, MUTED, 'end', 600))
    return _svg(W, H, ''.join(b), 'Bar inside a bar')


# ---- the "Psycho" website (continuous line + circle chart) ----
VISITORS = [200, 160, 120, 80, 50, 40, 45, 60, 80, 300, 330, 320, 325, 290, 310, 350, 390, 370, 390, 410, 430, 480, 400, 420, 260]
HV = list(enumerate(VISITORS))                      # (hour, visitors), 0..24
AREAS = [(0, 2, 'f'), (2, 8, 'o'), (8, 9, 'e'), (9, 10, 'f'), (10, 12, 'p'), (12, 16, 'e'), (16, 17, 'f'), (17, 18, 'e'),
         (18, 20, 'p'), (20, 24, 'f')]
AREA_KEYS = {'e': (TEAL, 'Explanations'), 'p': ('#9FC9C1', 'Practice'), 'f': ('#6B7785', 'Forum'), 'o': ('#fff', 'Other')}
SITE_TITLE = 'Visitors on the "Psycho" website over 24 hours'


def site_bars(step=4, hl=(), marks=()):
    if step >= 1:
        bars = [(h, VISITORS[h]) for h in range(0, 24, step)]
        bw = 1.6 if step == 4 else 0.8
    else:
        bars = [(x + 0.125, y) for x, y in smooth(HV, 0.25) if x < 24]
        bw = 0.25
    return continuous(0, 24, 4 if step >= 1 else 4, 0, 500, 100, bars=bars, bar_w=bw, strips=AREAS, strip_keys=AREA_KEYS,
                      xfmt=hours, ylabel='Visitors', title=SITE_TITLE, highlight_bars=hl, marks=marks)


def site_curve(marks=(), strips=True):
    return continuous(0, 24, 4, 0, 500, 100, curve=smooth(HV, 0.25), strips=AREAS if strips else None, strip_keys=AREA_KEYS,
                      xfmt=hours, ylabel='Visitors', title=SITE_TITLE, marks=marks)


BANDS = [dict(name='Explanations', spans=[(8, 9), (12, 16), (17, 18)]), dict(name='Practice', spans=[(10, 12), (18, 20)]),
         dict(name='Forum', spans=[(0, 2), (9, 10), (16, 17), (20, 24)]), dict(name='Other', spans=[(2, 8)])]


def site_circle(**k):
    k.setdefault('bands', BANDS)
    return radial(HV, rmax=500, ring_step=100, **k)


# ---- rents in Tel Aviv (range chart) ----
ROOMS = ['1', '2', '3', '4', '5', '6']
RENT = dict(name='Tel Aviv', mins=[2, 2.5, 3, 4, 4.5, 4.5], maxs=[4, 4.5, 6, 7, 7.5, 8], means=[3, 4, 4.5, 5.5, 6, 6.5])
RENT_J = dict(name='Jerusalem', mins=[1.8, 2.2, 2.8, 3.5, 4, 4.5], maxs=[3.2, 4, 5, 6, 7, 7.5], means=[2.5, 3, 3.8, 4.6, 5.2, 6])
RENT_E = dict(name='Eilat', mins=[1.5, 2, 2.5, 3, 3.5, 4], maxs=[2.8, 3.4, 4.2, 5, 5.8, 6.5], means=[2, 2.6, 3.2, 3.9, 4.5, 5.2])
RENT_TITLE = 'Monthly rent, Tel Aviv, 2012'


def rent_chart(hl=(), marks=(), series=None, title=RENT_TITLE, legend=None):
    return range_chart(ROOMS, series or [RENT], ymin=2, ymax=9, ystep=1, ylabel='Thousands of NIS', xlabel='Number of rooms',
                       title=title, highlight=hl, marks=marks, legend=legend)


def _k(v): return ('%g' % v)


def rent_table(cities=(RENT,), hl=()):
    rows = [[c['name']] + [('tri', _k(a), _k(m), _k(z)) for a, m, z in zip(c['mins'], c['means'], c['maxs'])] for c in cities]
    return table(['Rooms'] + ROOMS, rows, title='Monthly rent, 2012 (thousands of NIS)', col_w=[1.5] + [1] * 6,
                 note='In each cell: top left = lowest rent · centre = mean · bottom right = highest', highlight=hl)


# ---- health insurance (regions) ----
INS = [dict(pts=[(150, 40), (200, 40), (200, 120), (150, 70)], label='4', at=(186, 70), fill='#F4F8F7'),
       dict(pts=[(150, 70), (200, 120), (200, 140), (150, 90)], label='6', at=(191, 121), striped=True),
       dict(pts=[(150, 90), (200, 140), (200, 160), (150, 110)], label='8', at=(186, 136), fill='#DDEFEA'),
       dict(pts=[(150, 110), (200, 160), (180, 160), (150, 130)], label='10', at=(170, 141), fill='#C6E3DC'),
       dict(pts=[(150, 130), (180, 160), (150, 160)], label='12', at=(156, 152), fill='#AED6CC')]


def ins_chart(marks=(), hl=()):
    return regions(150, 200, 10, 40, 160, 20, INS, xlabel='Height (cm)', ylabel='Weight (kg)',
                   title='Health insurance: yearly cost (thousands of NIS)', marks=marks, highlight=hl)


# ---- Pixeltech (cumulative) ----
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
PIX = [10, 20, 50, 50, 70, 80]


def pix_chart(marks=(), hl=()):
    return cumulative(MONTHS, PIX, 0, 90, 10, ylabel='Thousands of NIS', title='Pixeltech: cumulative income, Jan–Jun 2013',
                      marks=marks, highlight=hl, name='Cumulative income')


# ---- "Green Light" volunteers (change graph) ----
WEEKS = [str(i) for i in range(1, 11)]
VOL = [15, 10, 5, 5, 0, -10, 10, -5, 0, 0]


def vol_chart(show_line=True, hl=(), marks=()):
    return change(WEEKS, VOL, -15, 20, 5, ylabel='Change', xlabel='End of week',
                  title='"Green Light": change in volunteers vs. the previous week', show_line=show_line,
                  highlight=hl, marks=marks)


# =====================================================================================================================
# LESSON 1 · introduction (seg01)
# =====================================================================================================================
SB1 = ['The chart set', 'Specific types', 'The instructions', 'The explanation', 'The example', 'If it is not clear',
       'Titles, units, notes', 'The questions', 'Table or chart?', 'Position = difficulty', 'Charts are accurate',
       'Table: many data', 'Chart: see the trend']


def L_intro():
    s = [TITLE('Charts & Tables', [
        "Introduction to drawing conclusions from a chart or a table.",
    ])]
    n = NS()
    s.append(S(SB1, 0, [
        "In the quantitative section we get a chart or a table, and after it four or five questions.",
        A('4-5 questions appears', n('A chart or a table → 4 or 5 questions')),
        "The recommended time: five to six minutes. A bit more than a minute per question.",
        A('Time appears', n('Recommended time: 5–6 minutes')),
        "In practice, we invest a minute, a minute and a half in understanding the chart — and only then go to the questions.",
        A('Understand first appears', n('1–1.5 minutes to understand the chart, then the questions')),
        "The skill being tested: our ability to understand and analyse data presented in different forms — in a table, or in different kinds of charts.",
        A('Skill appears', n('Tested: understanding and analysing data in different forms')),
    ], pre=[side(set_page('chart'))]))
    n = NU(610)
    s.append(S(SB1, 1, [
        "A common opinion — I hear it a lot — is that any kind of chart can appear on the psychometric exam, and there's no way to prepare except knowing the basic types.",
        "In practice, that's not true.",
        A('Specific types appears', n('The exam uses very specific types of charts — we will go through all of them')),
        "The exam has very, very specific types of charts. We'll go through all of them in the next lessons.",
        "Only in very, very rare cases — once in a year, two, three — a chart comes up that really doesn't belong to these types.",
        A('95% appears', n('About 95% of the charts belong to the types in these lessons')),
        "In the vast majority of cases, 95 percent, the charts will be of the types we learn here.",
    ], pre=[wide(chart_menu(), w=900)]))
    n = NU(620)
    s.append(S(SB1, 2, [
        A('Instructions appear', n('"Study the graph (table) below, then answer the four questions that follow."', size=32)),
        "The instructions: study the graph or the table below, then answer the questions that follow.",
        "In other words, we don't really have instructions. Read the chart, look at it, and answer the questions after it.",
        "How is it built? Let's go through it from top to bottom.",
    ], pre=[wide(set_page('instr'), w=800)]))
    n = NS()
    s.append(S(SB1, 3, [
        "Before every chart there's always an explanation — an explanation of what the chart in front of us describes.",
        A('Explanation appears', n('Before the chart: an explanation of what it describes')),
        "And at the end of the explanation there's an example. That too — in most cases there's an example, almost always.",
        A('Example appears', n('At the end of the explanation: an example (almost always)')),
        "You might meet a chart without an example, but it's very likely you won't.",
    ], pre=[side(set_page('expl'))]))
    n = NS()
    s.append(S(SB1, 4, [
        "The example is the most important thing in a chart, as far as I'm concerned.",
        A('Most important appears', n('The example is the most important thing', size=30)),
        "The example is what lets me check whether I understand the chart or not.",
        "I read the example, I go to the chart, and I check: is what's written in the example really what I understand from the chart?",
        A('Check appears', n('Read the example → find it in the chart → does it match what you understand?')),
        D('Point from the example sentence to the bar of 2010'),
        "If yes — I understood. I can move on to the questions.",
        A('Yes appears', n('Yes → go to the questions')),
        "If not — stop. There's no point going on to the questions if I didn't understand the example. If I didn't understand the example, I didn't understand the chart.",
        A('No appears', n('No → stop: no example = no chart')),
    ], pre=[side(set_page('example'))]))
    n = NU(620)
    s.append(S(SB1, 5, [
        "So what do I do in that situation? I go back and read again — slowly, line by line — and try to understand the chart and the example after all.",
        A('Read again appears', n('Read again, slowly, line by line')),
        "If I managed — excellent, to the questions.",
        "If not — it's better to leave the chart for now. Go on with the rest of the section, the other questions, and come back to the chart at the end.",
        A('Leave it appears', n('Still not clear → leave it, finish the section, come back at the end')),
        "So as not to waste time on it, trying to answer questions without even understanding the chart or the table in front of me.",
    ], pre=[wide(set_page('example'), w=800)]))
    n = NS()
    s.append(S(SB1, 6, [
        "After the explanation and the example, there's the chart or the table itself.",
        "Here it's important that you really look at the chart: at the titles, at the units.",
        A('Titles appears', n('Look at the titles and the units')),
        D('Circle "thousands" on the axis'),
        "Is it given in thousands, or in units, or hundreds, or tens — or in percent, for example?",
        A('Units appears', n('Thousands? Hundreds? Percent?')),
        "Pay attention to everything the chart gives you, including notes. Sometimes there's a note about the chart, and it's very important to notice it — without it, something probably won't add up.",
        A('Notes appears', n('Read every note — without it, something will not add up')),
    ], pre=[side(set_page('units'))]))
    n = NS()
    s.append(S(SB1, 7, [
        "After the chart come the questions — four or five of them.",
        "They appear in rising order of difficulty. The first is the easiest and the last is the hardest.",
        A('Rising appears', n('Rising difficulty: first = easiest, last = hardest')),
        "The last one can be either harder, or simply take more time in terms of calculations.",
        "Usually the first question is an understanding question — pulling out a piece of data. They pick some value in the chart and just check that you really understand it.",
        A('First appears', n('Question 1: usually pull out one value')),
        "The questions after that go up. Sometimes it's calculations, and sometimes a deeper understanding of the chart.",
        A('Then appears', n('Then: calculations, or deeper understanding')),
    ], pre=[side(set_page('qs'))]))
    n = NU(410)
    s.append(S(SB1, 8, [
        "Let's see the difference between a chart and a table.",
        "A table is a way to gather data that are related to each other, in a short and convenient way. You know it: rows and columns.",
        A('Table appears', n('Table: rows and columns — cross a row and a column to find a value')),
        "By crossing a row and a column, I pull out and find a specific value.",
        "A chart is a visual way to describe data.",
        A('Chart appears', n('Chart: a visual way to show the same data')),
        "Whoever knows Excel: Excel is one big table. I can write data in it, and then do 'insert chart'. It opens a menu and asks: which kind of chart would you like? Columns, line, pie, and so on.",
        "Because the chart is visual, I choose the chart that fits the kind of data I want to show. We'll see later how different charts help us see different things.",
        A('Choose appears', n('Different charts help us see different things')),
    ], pre=[wide(chart_menu(), w=560, y=90)]))
    n = NS()
    s.append(S(SB1, 9, [
        "Level of difficulty. We said the questions after the chart are in rising order of difficulty.",
        "The chart itself also sits in the section according to its difficulty. At the start of the section it's very easy; at the end, very hard.",
        A('Position appears', n('The chart\'s place in the section = its difficulty')),
        "Now there's a recommendation you often hear given to students: always skip the chart. Skip it, finish the whole section, and only at the end come back to the chart.",
        "That's a mistake, and I'll explain why.",
        A('Mistake appears', n('"Always skip the chart" → a mistake')),
        "A chart at the start of the section is not just very easy. Statistically, it's also easier than the other questions at the start of the section.",
        "If I check students' success rates, when there was a chart at the start: say 80 percent success on the first questions — then on the chart it'll be something like 85 percent.",
        A('85 appears', n('First questions ≈ 80% success · chart at the start ≈ 85%')),
        "So a chart at the start or up to the middle of the section — do it when you get to it. There's no reason to skip it. At the end — you get to it at the end anyway.",
        A('Do it appears', n('Start or middle → solve it when you reach it. End → you reach it last anyway')),
        "Someone who is individually weaker in charts may prefer to skip — that's individual. As general advice: don't skip a chart at the start of the section.",
    ], pre=[side(set_page(None))]))
    n = NU(612)
    s.append(S(SB1, 10, [
        "Accuracy. Notice: unlike figures in geometry — we know the geometry figures in the exam don't have to be accurate — in charts, a drawing is always accurate.",
        A('Accurate appears', n('Geometry figures: not necessarily to scale · Charts: always accurate')),
        "Not only is it worth using it and relying on it when you solve — it's recommended. There are questions whose quick solution is by looking at the drawing.",
        "I see a trend — a sharper angle, a line with a steeper slope — and I understand right away that it has consequences.",
        A('Look appears', n('Use your eyes: higher, lower, steeper — often no calculation needed')),
        D('Point at the steepest part of the line'),
    ], pre=[wide(site_curve(strips=False, marks=[('seg', 8, 80, 9, 300)]), w=900)]))
    n = NS()
    s.append(S(SB1, 11, [
        "So when do we use a table and when a chart? In a table, the advantage is that I can give a lot of data about one object.",
        "For example, here's a table about different ages, and they checked the average number of siblings.",
        "At ages 21 to 30 the average number of siblings is 2.3; 31 to 40 — 2.8; 41 to 50 — 3.6.",
        A('Siblings appears', n('One value per row: 2.3 · 2.8 · 3.6')),
        "And now I can add more data.",
    ], pre=[side(sib_table(2, hl_cols=[1]), w=640)]))
    n = NU(530)
    s.append(S(SB1, 11, [
        "How many children people of these ages have — I add the number of children.",
        "The average number of friends — just like that. We can see that younger people have more friends than older people.",
        "The average salary: 6,200, 8,300 — and here too I see a rise. The older I am, the higher my salary.",
        "And the average number of rooms in the home they live in, and so on and so on. No problem adding a lot of data.",
        A('Many appears', n('A table can hold a lot of data')),
        "And if only one specific value interests me, I just focus on it. The other data don't really bother me.",
        A('Focus appears', n('Need one value? Focus on it — the rest does not disturb you')),
        "Unlike a chart, as we'll see: when you add more and more data, there are too many lines or too many bars — it's hard to see something specific.",
    ], pre=[wide(sib_table(6, hl_cols=[4]), w=1060)]))
    n = NU(530)
    s.append(S(SB1, 12, [
        "In a chart, on the other hand, the big advantage is that I can see things — draw conclusions visually, at a glance. The trend, a rise, a fall, who is bigger.",
        "In a table I have to really go in: read the numbers here and see there's growth; read here and see growth; read here and understand there's a decrease.",
        A('Read appears', n('Table: you must read the numbers to see a rise or a fall')),
        D('Point: salary goes up, friends go down'),
        "If it were in a chart, I'd just see lines going up or lines going down — within seconds.",
        A('See appears', n('Chart: you see the lines go up or down — in seconds')),
    ], pre=[wide(sib_table(6, hl_cols=[3, 4]), w=1060)]))
    n = NS()
    s.append(S(SB1, 12, [
        "Let's see an example. In this chart we see how our score improves according to the number of simulations we do.",
        "Maybe the more simulations I do, the higher my score. Maybe.",
        "In this graph we see that at the start the improvement is very, very big: from the first simulation to the second, third, fourth, fifth.",
        A('Big at first appears', n('Steep at the start = a big improvement')),
        "And from simulation 8–9 I see I'm hardly improving any more.",
        A('Flat appears', n('From 8–9: almost flat = almost no improvement')),
    ], pre=[side(sim_chart(SIM_A, marks=[('seg', 1, 480, 4, 620), ('col', 8.5, 15)]))]))
    n = NS()
    s.append(S(SB1, 12, [
        "Another possible graph: at the start there's almost no improvement — second, third, fourth — and only from the fourth or fifth there's suddenly a bigger improvement.",
        "From 5 to 6 I go up here, from 6 to 7 I go up, from 7 to 8. The slope is sharper, so the improvement is bigger.",
        A('Steeper appears', n('Sharper slope → bigger improvement')),
        "And again, here there's almost no improvement: from 10 or 11 up to 15 I keep going, but there's almost no rise on the y-axis — almost no rise in the score.",
        A('Ceiling appears', n('10–15: moving on, but the score hardly rises')),
        "Or a different chart: at the start almost no improvement up to simulation 7, 8, 9 — and only then a sharp improvement starts.",
        A('Other appears', n('Dashed: another possible curve — flat until 7–9, then sharp')),
    ], pre=[side(sim_chart(SIM_B, marks=[('seg', 5, 525, 8, 640)], extra=SIM_C), w=830)]))
    n = NS()
    s.append(S(SB1, 12, [
        "By the way, about the simulations we do at the end of our preparation for the psychometric exam — the correct chart is this one.",
        A('Real appears', n('The real simulation curve')),
        "Don't be upset if you start with a few simulations and see almost no improvement.",
        "The improvement comes more or less from the fourth or fifth simulation, and then there's a significant improvement. Then we reach a kind of ceiling where we stop, more or less.",
        A('Real text appears', n('Little at first → a big jump from about the 5th → a ceiling')),
        "That's it for the introduction. In the next lessons we'll go through the different types: tables, bar charts, line graphs, continuous lines, circle charts and so on. See you there.",
    ], pre=[side(sim_chart(SIM_B, marks=[('col', 1, 4.5), ('seg', 5, 525, 8, 640), ('col', 10, 15)]))]))
    return lesson('ch52-intro', 'Charts & Tables', SB1, s, T52)


# =====================================================================================================================
# LESSON 2 · tables (seg02)
# =====================================================================================================================
SB2 = ['The car table', 'Adding columns', 'Privately owned', 'Commercial vehicles', 'Any topic can come',
       'Average question', 'Symmetric shortcut', 'Percent question', 'Know your eighths', 'Overlap question',
       'The squares method', 'Learn it last']


def grid(cells, hl=()):
    """2010 overlap grid: rows private / commercial, columns privately owned / company-owned (thousands)."""
    a, b_, c = cells
    return table(['2010', 'Privately\nowned', 'Company-\nowned', 'Total'],
                 [['Private cars', a, b_, '45'], ['Commercial', c, '', ''], ['Total', '40', '', '60']],
                 highlight=hl, col_w=[1.5, 1, 1, 1], W=640)


def L_tables():
    s = [TITLE('Tables', ["Drawing conclusions from a table."])]
    n = NU(520)
    s.append(S(SB2, 0, [
        "After the introduction, where we saw the pros and cons of a table and of a chart, let's start with the first type: the table.",
        "We'll start with an example. The table in front of you describes the number of new vehicles sold in Israel in the years 2010 to 2013.",
        "Here I have the year, and here the total number of vehicles sold.",
        A('Example appears', n('For example: in 2010, 60 thousand new vehicles were sold.')),
        "For example: in 2010, 60 thousand new vehicles were sold. Very simple to understand.",
    ], pre=[wide(car_table(2, highlight=[(0, 1)]), w=720)]))
    n = NU(560)
    s.append(S(SB2, 1, [
        "Let's take this example and expand it a bit — add more data.",
        "We added private cars. How many of them are private cars? What does 'of them' mean? Of all the vehicles sold.",
        "60 thousand were sold; of them, 45 thousand are private cars. That's 2010, of course, and here are the other years.",
        A('Of them appears', n('"Of them" = out of all the vehicles sold: 45 of the 60 thousand')),
    ], pre=[wide(car_table(3, highlight=[(0, 1), (0, 2)]), w=760)]))
    n = NU(560)
    s.append(S(SB2, 2, [
        "Let's expand a bit more and add another column: how many are privately owned.",
        "A vehicle can be privately owned, or owned by a company, for example.",
        A('Ownership appears', n('Ownership: private, or a company')),
        "So — vehicles in private ownership. Here.",
    ], pre=[wide(car_table(4, hl_cols=[3]), w=900)]))
    n = NU(560)
    s.append(S(SB2, 3, [
        "And one more: how many are commercial vehicles in private ownership.",
        "Because there are private cars and there are commercial vehicles — and they added a column: how many commercial vehicles are privately owned.",
        A('Commercial appears', n('Some private people own commercial vehicles')),
        "There are private people who own commercial vehicles.",
    ], pre=[wide(car_table(5, hl_cols=[4]))]))
    n = NU(560)
    s.append(S(SB2, 4, [
        "In chart and table questions they can actually combine topics from the whole quantitative field — the different types of problems.",
        A('Topics appears', n('Percent · averages · overlap · work · even motion — anything can come')),
        "Percent problems, averages, overlap, work, and even motion — everything.",
        "So it's recommended to learn this whole topic of charts and tables after we've finished all the other types of problems.",
        A('Last appears', n('Learn charts & tables after all the other problem types')),
        "Let's see examples of questions from different fields.",
    ], pre=[wide(car_table(5))]))
    n = NU(560)
    s.append(S(SB2, 5, [
        "The topic of averages. What is the yearly average of the total vehicles sold?",
        A('Q appears', n('What is the yearly average of all the vehicles sold?')),
        "I look at the total vehicles sold. In the table I have 2010 to 2013; I need the average of these years.",
        "60 plus 80 plus 80 plus 100, divided by 4. That's 320 divided by 4 — 80. The average is the sum of the items divided by the number of items.",
        A('Calc appears', n('(60 + 80 + 80 + 100) ÷ 4 = 320 ÷ 4 = 80')),
    ], pre=[wide(car_table(5, hl_cols=[1]))]))
    n = NU(560)
    s.append(S(SB2, 6, [
        "If you notice, I didn't really need this calculation. Why?",
        "Because this is a symmetric group, with equal distances between the numbers: 60, 80, 80, 100.",
        A('Symmetric appears', n('60, 80, 80, 100: distance 20 · 0 · 20 → symmetric')),
        D('Mark the gaps: 20, 0, 20'),
        "The distance here is 20, the distance here is 20, and here there's nothing — it's the same.",
        "So the average must be in the middle — exactly 80.",
        A('Middle appears', n('Symmetric group → the average is the middle: 80')),
    ], pre=[wide(car_table(5, hl_cols=[1]))]))
    n = NU(560)
    s.append(S(SB2, 7, [
        "Another example, from the world of percents. What percent of the vehicles sold were privately owned?",
        A('Q appears', n('What percent of the vehicles sold were privately owned?')),
        "Privately owned is here; vehicles sold is here. With percents it's always important to know who the whole is. 'Of' — what comes after 'of' is the whole.",
        A('Whole appears', n('"Of the vehicles sold" → the vehicles sold are the whole (100%)')),
        "2010: 40 thousand privately owned out of 60 thousand in total. 40 over 60 is two-thirds — 66 and two-thirds percent.",
        "2011: 50 thousand out of 80 thousand. 50 over 80 is five-eighths — 62.5 percent. 2012 is also 50 over 80.",
        "And 2013 is 65 over 100 — that's already very simple: 65 percent.",
        A('Calc appears', n('40/60 = 66⅔% · 50/80 = 62.5% · 50/80 = 62.5% · 65/100 = 65%')),
    ], pre=[wide(car_table(5, hl_cols=[1, 3]))]))
    n = NS()
    s.append(S(SB2, 8, [
        "Here I remind you: it's very important to know the eighths. One-eighth is 12.5 percent. How do you remember?",
        "A quarter is 25 percent, and an eighth is exactly half of a quarter. Half of 25 is 12.5.",
        A('Eighth appears', n('1/4 = 25% → 1/8 = half = 12.5%', size=30)),
        "But you need to master the extensions too.",
        A('Ext appears', n('3/8 = 37.5% · 5/8 = 62.5%', size=30)),
        "One-eighth is 12.5, three-eighths 37.5, five-eighths 62.5.",
    ], pre=[side(car_table(5, highlight=[(1, 1), (1, 3)]), w=800)]))
    n = NU(430, x=1030, w=540, size=28)
    s.append(S(SB2, 9, [
        "Let's see a question in another field: overlap.",
        A('Q appears', n('How many private cars were owned by a company in 2010?')),
        "How many private cars were commercially owned — owned by a company — in 2010?",
        "We have groups here. On one side, private cars or commercial vehicles. On the other side, private ownership or company ownership.",
        A('Groups appears', n('Groups: private / commercial × privately owned / company-owned')),
    ], pre=[wide(car_table(5, hl_rows=[0]), w=900, y=80), vis(grid(('', '', '')), w=640, x=360, y=430)]))
    n = NU(430, x=1030, w=540, size=28)
    s.append(S(SB2, 10, [
        "If we remember the squares method from overlap — very convenient for us.",
        "One group is private cars: in 2010 there were 45 thousand. The other group is ownership. Let's take private ownership, since that's in the table — very easy. Privately owned: 40 thousand.",
        "We know that commercial vehicles in private ownership were 4 thousand. That square belongs to commercial and to private ownership — so here I can put 4.",
        A('4 appears', n('Commercial + privately owned = 4')),
        "From here it's like sudoku. These two squares together must make 40, so 40 minus 4 is 36.",
        A('36 appears', n('40 − 4 = 36 private cars, privately owned')),
        "And to get the square that's left here: 45 minus 36 is 9.",
        A('9 appears', n('45 − 36 = 9 → 9,000 private cars owned by a company')),
        "They asked about private cars owned by a company. Here are private cars privately owned — so what's left here is private cars owned by a company: 9,000.",
    ], pre=[wide(car_table(5, highlight=[(0, 2), (0, 3), (0, 4)]), w=900, y=80),
            vis(grid(('36', '9', '4'), hl=[(0, 1)]), w=640, x=360, y=430)]))
    n = NU(560)
    s.append(S(SB2, 11, [
        "That's it for our lesson on tables. A short lesson.",
        "What mattered to me most was to show you that questions from different types of problems can appear inside charts and tables.",
        A('Any appears', n('Questions from any problem type can come inside a chart or a table')),
        "Not always — sometimes it's pure understanding of a chart or a table — but these questions can appear. So learn charts and tables towards the end, after you've gone through the other types of problems.",
        A('Order appears', n('So: learn this topic after the other problem types')),
        "From here we go on to the charts. We'll go through the whole evolution of charts, slowly: we start with a coordinate system and move on to graphs of different kinds. See you in the next lessons.",
    ], pre=[wide(car_table(5))]))
    return lesson('ch52-tables', 'Tables', SB2, s, T52)


# =====================================================================================================================
# LESSON 3 · points on axes (seg03)
# =====================================================================================================================
SB3 = ['The basic chart', 'From table to chart', 'Axes and units', 'The legend', 'Plotting the points',
       'All four series', 'Easy to see changes', 'Numbers as markers', 'Average per dealer', 'Negative values',
       'The scale is exact', 'Axis break (Z)']

AGENCIES = ['5', '8', '10', '15']


def L_scatter():
    s = [TITLE('Points on Axes', ["Points on a coordinate system."])]
    n = NS()
    s.append(S(SB3, 0, [
        "In the previous lesson we learned tables. Now we start the different types of charts on the exam.",
        "The first type is points on a coordinate system. It's actually the most important type — a kind of introduction, the basic thing from which all the other charts grow.",
        A('Basic appears', n('Points on axes: the base of all the other charts')),
    ], pre=[side(car_scatter(4))]))
    n = NU(560)
    s.append(S(SB3, 1, [
        "Let's first recall the table from the previous lesson: the number of vehicles in 2010 to 2013 — how many were sold, how many private, privately owned, commercial privately owned.",
        "Let's see how we turn the data in the table into a chart on a coordinate system.",
        A('Convert appears', n('Same data: from the table → to points on axes')),
    ], pre=[wide(car_table(5))]))
    n = NS()
    s.append(S(SB3, 2, [
        "We draw a coordinate system. On the x-axis we have the years, 2010 to 2013.",
        A('X appears', n('x-axis: the years')),
        "On the y-axis — the amount, in thousands.",
        A('Y appears', n('y-axis: the amount, in thousands')),
        D('Circle "Thousands"'),
        "That means that when it says 90 here, it's not really 90 — it's 90,000.",
        A('90 appears', n('"90" on the axis = 90,000')),
    ], pre=[side(car_scatter(1, only=0, marks=[('hline', 90, '90 = 90,000')]))]))
    n = NS()
    s.append(S(SB3, 3, [
        "Now we take these data and turn them into points on the coordinate system, each point in its place.",
        "The first thing we need is a legend.",
        A('Legend appears', n('First: the legend — which marker is which series')),
        "Vehicles sold — we mark with this black star.",
        A('Star appears', n('★ = vehicles sold')),
    ], pre=[side(car_scatter(1, only=0))]))
    n = NS()
    s.append(S(SB3, 4, [
        "We know that in 2010, 60 thousand vehicles were sold. So we're at 2010, we go up until 60, and mark a star here.",
        A('2010 appears', n('2010 → up to 60 → ★')),
        "In 2011 we have 80 thousand, so we mark at 2011 — 80. 2012, also 80. In 2013 we have 100 thousand — we go up and mark 100 thousand.",
        A('Rest appears', n('2011: 80 · 2012: 80 · 2013: 100')),
        "Notice the points appear exactly at the value. If I want to know 2012 — 80 thousand — that really matches the table.",
    ], pre=[side(car_scatter(1, highlight=[(0, 0)], marks=[('guide', 0, 60, '60')]))]))
    n = NS()
    s.append(S(SB3, 5, [
        "In the same way we mark the other data too — we just adapt the legend.",
        "Private cars — with a dot. Privately owned — with a white star. And commercial vehicles in private ownership — with an x.",
        A('Legend appears', n('● private cars · ☆ privately owned · × commercial, privately owned')),
        "Here — we've marked all the data. The chart we got describes exactly the data in the table. Everything in the table appears in the chart.",
        A('Same appears', n('Every value in the table is a point in the chart')),
    ], pre=[side(car_scatter(4))]))
    n = NS()
    s.append(S(SB3, 6, [
        "The advantage of the chart is that it's more visual. I can easily see where there's a rise and where it stays the same.",
        "Unlike the table, where I really have to go in and read, and notice that here it's 50 and here it's 50 — look closely at every column and every row to see if it went up or down.",
        "Here I just see the points: up, stayed, up.",
        A('See appears', n('Sold: up · stayed · up')),
        "Here it stayed or almost stayed, and here there's a small rise. I can see it easily.",
        A('Almost appears', n('Private cars: 60 → 62 almost stayed, then a small rise')),
    ], pre=[side(car_scatter(4, highlight=[(0, 1), (0, 2), (1, 1), (1, 2)]))]))
    n = NS()
    s.append(S(SB3, 7, [
        "Let's go on. Sometimes the data won't appear as points or stars, but in another form — and then they add another parameter, another piece of data.",
        "Instead of stars I can write numbers here, and somewhere on the side it says what these numbers represent — for example, the number of car dealers that sold the vehicles.",
        A('Numbers appear', n('The number at each point = the number of dealers that sold the vehicles')),
        "So in 2011, 8 dealers sold the vehicles.",
        A('2011 appears', n('2011: 80 thousand vehicles, 8 dealers')),
    ], pre=[side(car_scatter_num(hl=[(0, 1)]))]))
    n = NU(560, size=28)
    s.append(S(SB3, 8, [
        "Let's see a sample question. In which year was the average number of vehicles sold per dealer the greatest?",
        A('Q appears', n('In which year was the average number of vehicles sold per dealer the greatest?  (1) 2010  (2) 2011  (3) 2012  (4) 2013')),
        "I go to 2010: 60 thousand cars were sold, by 5 dealers. To find the average: 60 divided by 5 — 12 thousand.",
        "In 2011, 8 dealers sold 80 thousand in total — 80 over 8 is 10. In 2012, 10 dealers: 80 over 10 is 8.",
        "And in 2013, 100 thousand vehicles by 15 dealers. 100 over 15 doesn't really interest me — it's clearly less than 10, and I already have more than 10.",
        A('Calc appears', n('60/5 = 12 · 80/8 = 10 · 80/10 = 8 · 100/15 < 10  → answer (1)')),
        D('Circle choice 1'),
        "So I know answer 1 is correct.",
    ], pre=[wide(car_scatter_num(hl=[(0, 0)]), w=820, y=80)]))
    n = NS()
    s.append(S(SB3, 9, [
        "More nuances that can appear on a coordinate system. First: a coordinate system can also take negative values.",
        "Say in 2010 no cars were sold at all — and not only that, 10,000 cars were even returned. Then I can write minus 10 here.",
        A('Neg appears', n('Below 0: e.g. −10 = 10,000 cars returned')),
        "Of course, in other charts there can be a different story behind it, and the minuses can be much bigger or smaller.",
    ], pre=[side(scatter(YEARS, [dict(name='Vehicles sold', values=[-10, 80, 80, 100], marker='star')], ymin=-20, ymax=110,
                         ystep=10, ylabel='Thousands', title='Vehicles sold (imagine: 2010 = −10)', highlight=[(0, 0)],
                         legend=None, marks=[('label', 0.25, -10, '−10 = 10,000 returned')]))]))
    n = NS()
    s.append(S(SB3, 10, [
        "Another thing: here we can see that our units are fixed — and notice, it's accurate.",
        "10, 20, 30, 40 — it starts from 0, and every such line marks a jump of 10,000.",
        A('Fixed appears', n('Every gridline = the same jump: 10,000')),
    ], pre=[side(car_scatter(4, marks=[('brace', 3.3, 10, 20, '10,000'), ('brace', 3.3, 30, 40, '10,000')]))]))
    n = NS()
    s.append(S(SB3, 11, [
        "There can be a chart where the data don't start from 10, but from 50. Nothing appears below, so I don't need it — it starts from 50.",
        "And here I have a problem, because we said charts are accurate — but the distance between 50 and 60 is not the same as between 0 and 50.",
        "In that case they mark the bottom part of the axis like this: a kind of zigzag, a kind of Z.",
        A('Z appears', n('Z (zig-zag) on the axis: this part is NOT to scale')),
        D('Circle the zig-zag'),
        "The Z tells me that the distance here isn't the fixed distance between all the other ticks. We simply don't care what happened below 50.",
        "And of course in that case I won't have data down there — like the x from the previous chart.",
        A('No data appears', n('Nothing is shown below 50 (the × series is gone)')),
        "That's it for points on a coordinate system. As I said, it's the introduction and the base for all the other charts we'll learn. See you in the next lesson.",
    ], pre=[side(car_scatter(3, ymin=50, ymax=110, ystep=10))]))
    return lesson('ch52-scatter', 'Points on Axes', SB3, s, T52)


def car_scatter_num(hl=()):
    return scatter(YEARS, [dict(name='Vehicles sold', values=SOLD, labels=AGENCIES)], ymin=0, ymax=110, ystep=10,
                   ylabel='Thousands', title='Vehicles sold (the number = car dealers)', legend=None,
                   highlight=hl)


# =====================================================================================================================
# LESSON 4 · line graph (seg04)
# =====================================================================================================================
SB4 = ['Connect the dots', 'Four lines', 'Different line styles', 'Only the points count', 'The line = trend',
       'Steeper = bigger rise', 'Points vs. lines', 'Line graph: summary']


def L_line():
    s = [TITLE('Line Graph', ["The line graph."])]
    n = NS()
    s.append(S(SB4, 0, [
        "A line graph is really the same chart we had before — points on a coordinate system — only this time we connect the points with a line.",
        A('Same appears', n('Line graph = points on axes, connected by a line')),
        "Why do we do that? We'll see in a moment — it helps me see things more clearly than with the points alone.",
        "Let's take the chart from the previous lesson, the cars and the sales data. In 2010 — 60 thousand, then 2011 80 thousand, 80 thousand and 100 thousand.",
        "What we'll do is simply connect them with a line.",
    ], pre=[side(line(YEARS, [dict(name='Vehicles sold', values=SOLD, style='bold', marker='star')] +
                      [dict(name=c['name'], values=c['values'], style='solid', marker=c['marker'], color='#C9D3DC') for c in CAR_S[1:]],
                      0, 110, 10, ylabel='Thousands', title='Vehicles sold, 2010–2013', legend=None))]))
    n = NS()
    s.append(S(SB4, 1, [
        "The same for privately owned vehicles — we connect them with a line. And commercial vehicles in private ownership.",
        "Now that I've connected the points with a line, I can actually make the points disappear.",
        A('Hide appears', n('Connect the points → the points can disappear')),
        "Only — now I have four lines that all look the same. I can't tell them apart.",
        A('Same appears', n('Problem: four identical lines')),
    ], pre=[side(car_line(styles=False, points=False))]))
    n = NS()
    s.append(S(SB4, 2, [
        "So what we do is draw different lines — we mark each line in a different way.",
        "A bold line, a dashed line, a dash-dot line.",
        A('Styles appears', n('Bold · plain · dashed · dash-dot')),
        "And of course we make sure to change the legend accordingly.",
        A('Legend appears', n('…and the legend shows each style')),
        "Now it's as if I have the points from before — only connected by a line.",
    ], pre=[side(car_line())]))
    n = NS()
    s.append(S(SB4, 3, [
        "Notice — and it's important to understand — the line itself has no meaning in terms of the points it passes through. Only the points themselves, in 2010, in 2011.",
        "If in 2010 we sold 60 thousand vehicles — I have no data about 2010 and a half, that there were 70,000. There's no such thing as 2010 and a half. There's no measurement point there.",
        A('No half appears', n('No "2010½": there is no measurement between the years')),
        D('Point at the line between 2010 and 2011'),
        "The points are here, and here, and here. We replaced the points with lines — but the line itself has no numerical value, only at the points it passes through, the points that were marked.",
        A('Points appears', n('Numbers only at the marked points')),
    ], pre=[side(car_line(points=True, marks=[('cross', 0.5, 70), ('label', 0.6, 88, '2010½? No data'), ('pt', 0, 60), ('pt', 1, 80)]))]))
    n = NS()
    s.append(S(SB4, 4, [
        "The only meaning the line itself has is the trend.",
        A('Trend appears', n('The line itself = the trend only')),
        "What's a trend? Here I can see there's no change; here I can see there's a rise.",
        A('Flat appears', n('Flat = no change · going up = a rise')),
    ], pre=[side(car_line(highlight=[(2, 1), (2, 2)]))]))
    n = NS()
    s.append(S(SB4, 5, [
        "And by the angle of the line I can see whether the rise was bigger or smaller.",
        "I can see that the angle here is bigger than here. So I understand that here there was a bigger upward trend than here.",
        A('Angle appears', n('Steeper line = a bigger rise')),
        D('Compare the two slopes'),
        A('Values appears', n('Privately owned: 2010→2011 +10 · 2012→2013 +15')),
    ], pre=[side(car_line(highlight=[(2, 0), (2, 2)]))]))
    n = NU(665)
    s.append(S(SB4, 6, [
        "Let's compare it with the points chart we had before. We take away the trend lines at the back for a moment.",
        "Here I really see two points — but it's hard to see in which of them the rise was bigger.",
        A('Dots appears', n('Points only: hard to see which rise is bigger')),
        "In the line graph, on the other hand, it's easier to see that here the rise was bigger, because the slope of the line is sharper than the slope of this line.",
        A('Lines appears', n('Lines: the steeper slope shows it at once')),
        "That's the advantage of a line graph over points: I can see the slopes, the trend. With points it's a bit harder.",
    ], pre=[vis(car_scatter(4, legend=None, W=620, marks=[('pt', 0, 40), ('pt', 1, 50), ('pt', 2, 50), ('pt', 3, 65)]), w=600, x=345, y=85),
            vis(car_line(legend=None, W=620, highlight=[(2, 0), (2, 2)]), w=600, x=965, y=85),
            vis(legend_strip(CAR_LEG_S), w=1200, x=365, y=598)]))
    n = NS()
    s.append(S(SB4, 7, [
        "That's it for the line graph. The difference, again, is the ability to see trends visually.",
        A('Trends appears', n('Advantage: you see the trends')),
        "But it's important to say: the line itself has no meaning — only the points it passes through, the same points that were marked before.",
        A('Points appears', n('Values only at the points — the line between them means nothing')),
        "See you in the next lesson.",
    ], pre=[side(car_line(points=True))]))
    return lesson('ch52-line', 'Line Graph', SB4, s, T52)


# =====================================================================================================================
# LESSON 5 · bar chart (seg05)
# =====================================================================================================================
SB5 = ['Same data, bars', 'Bars up to the line', 'Four series of bars', 'Reading a bar', 'Bar inside a bar',
       'Overlap in bars', 'Stacked bars', 'Reading a stack', 'Fit the user', 'Horizontal bars',
       'Turn it 90°', 'Bar chart: summary']


def L_bar():
    s = [TITLE('Bar Chart', ["The bar chart."])]
    def two(l, r, *legs):
        legs = legs or (CAR_LEG_L, CAR_LEG)
        return [vis(l, w=600, x=345, y=85), vis(r, w=600, x=965, y=85)] + [
            vis(legend_strip(g), w=1200, x=365, y=596 + 46 * k) for k, g in enumerate(legs)]
    n = NU(665)
    s.append(S(SB5, 0, [
        "A bar chart is another way to present the same data we showed before — in a table, as points on axes, or as a line graph. This time we show it with bars.",
        A('Same appears', n('Bar chart: the same data, shown with bars')),
        "Let's take the chart we had with the lines and put it on the left — that stays with lines. And here we'll turn everything into bars, so we have a reference.",
    ], pre=two(car_line(legend=None, W=620), car_bar(0, legend=None, W=620), CAR_LEG_L)))
    n = NU(665)
    s.append(S(SB5, 1, [
        "Let's start. We hide the three lower lines, to go line by line.",
        "Instead of this line — instead of vehicles sold — we make bars that start at the bottom and go up to this point.",
        "The bars went up exactly to the points where the line was. If I hide the line: in 2010 I have 60 thousand, in 2011 80, in 2012 80 thousand, in 2013 100 thousand.",
        A('Heights appears', n('The bars reach exactly the points: 60 · 80 · 80 · 100')),
        "Exactly as we had before — in the table, and in the points chart.",
        "What I do need to notice: in my legend I no longer have a line for vehicles — I have a white bar. The white bar marks the vehicles sold.",
        A('Legend appears', n('Legend: white bar = vehicles sold')),
    ], pre=two(line(YEARS, [dict(name='Vehicles sold', values=SOLD, style='bold')], 0, 110, 10, ylabel='Thousands',
                         title='Vehicles sold, 2010–2013', legend=None, W=620), car_bar(1, W=620, legend=None),
               [('line', ('bold', INK), 'Vehicles sold (line)'), ('box', ('#fff', INK), 'Vehicles sold (white bar)')])))
    n = NU(705)
    s.append(S(SB5, 2, [
        "Now to the next line — private cars. Only it would appear inside the same bar, so we move it a bit to the right, and raise bars to the right points.",
        "These bars replaced this line. Of course we updated the legend too.",
        "We continue with the two other lines — move them a bit, so the bars stand one beside the other — and commercial vehicles, also a bit to the right. Raise bars, and mark the legend.",
        A('Grouped appears', n('Bars side by side, one colour per series (see the legend)')),
        "Notice: we have two charts that say exactly the same thing. They describe exactly the same data.",
    ], pre=two(car_line(legend=None, W=620), car_bar(4, legend=None, W=620))))
    n = NU(705)
    s.append(S(SB5, 3, [
        "In 2010, privately owned vehicles were 40 thousand — the height of the bar is 40 thousand.",
        A('2010 appears', n('2010, privately owned: bar height = 40 thousand = the point on the line')),
        "2010, privately owned, 40 thousand — that's this point here.",
        D('Connect the bar top to the point on the line'),
    ], pre=two(car_line(legend=None, W=620, marks=[('guide', 0, 40, '40')]), car_bar(4, legend=None, W=620, highlight=[(2, 0)], marks=[('hline', 40, '40')]))))
    n = NS()
    s.append(S(SB5, 4, [
        "More nuances in a bar chart. Sometimes the bars appear one inside the other.",
        "For example, take the private cars. In total 60 thousand vehicles were sold; of them, 45 thousand were private cars.",
        "So the height of the black bar shows the private cars, and the height of the white bar, up to 60, is all the vehicles sold.",
        A('Inside appears', n('Black (inside) = private cars 45 · white (back) = all sold 60')),
        "The same here: of the 40 thousand privately owned vehicles, something like 4,000 are commercial vehicles in private ownership. So what's left here is private cars in private ownership.",
        A('Inside2 appears', n('Of the 40 privately owned: 4 commercial → the rest are private cars')),
    ], pre=[side(bar(YEARS, [dict(name='Vehicles sold', values=SOLD, fill='#fff'), dict(name='Private cars', values=PRIV, fill=INK)],
                     mode='overlap', ymax=110, ystep=10, ylabel='Thousands', title='Bar inside a bar', highlight=[(0, 0), (1, 0)]))]))
    n = NS()
    s.append(S(SB5, 5, [
        "A bar inside a bar can also appear like this: the back bar, the general one, is bigger, because it contains several things.",
        "In total we have 80 thousand vehicles. Of them, 60 thousand are private cars. And of the 80, also 50 thousand are privately owned.",
        A('Data appears', n('2011: 80 sold · 60 private cars · 50 privately owned')),
        "I've really created an overlap question here: of all the vehicles, how many are both private cars and privately owned?",
        A('Q appears', n('How many are both private cars AND privately owned?')),
        "It could be that all the privately owned vehicles — all 50 thousand — are contained in this bar. All 50 thousand privately owned vehicles are also private cars.",
        A('Case1 appears', n('Case 1: all 50 inside the 60 → 50 are both')),
    ], pre=[side(overlap_fig(1))]))
    n = NS()
    s.append(S(SB5, 5, [
        "And it could be — if I take it up, like ranges — that I push it to the top, and then I see that only 30 thousand are both.",
        A('Case2 appears', n('Case 2: pushed to the top → only 30 are both')),
        "A bit like an overlap question. Whoever hasn't learned overlap yet — I suggest going back before this lesson, or at least trying to follow roughly what I'm saying, and carrying on.",
        A('Range appears', n('So "both" is anywhere from 30 to 50 thousand')),
    ], pre=[side(overlap_fig(2))]))
    n = NS()
    s.append(S(SB5, 6, [
        "Another nuance. Let's change the chart a bit, change the legend a bit.",
        "Say the black bars are private cars, the grey ones are commercial vehicles — that's no longer the same kind: a vehicle can't be both private and commercial. Either you're a van or you're a small car.",
        "And we have motorcycles — motorcycles of course don't belong to either.",
        A('Types appears', n('Separate kinds: private · commercial · motorcycles')),
        "Here we can show the data cumulatively. What does that mean? We can put the bars one on top of the other.",
        A('Stack appears', n('Stacked: the bars sit one on top of the other')),
    ], pre=[side(stack_chart())]))
    n = NS()
    s.append(S(SB5, 7, [
        "Why would I want to show a chart like this? Maybe I own a dealership that sells private cars, commercial vehicles and motorcycles.",
        "At one glance I don't really care how much I sold of each thing. I want to know: how many vehicles did we sell in total?",
        "I look and see we sold almost 120 thousand vehicles — 117 or 118 thousand during 2012.",
        A('Total appears', n('Top of the stack = the total: 2012 ≈ 118 thousand')),
        "If I wanted to know how many of one kind — how many commercial vehicles, for example — then it's from 60 to 110. From 60 to 110 — that's 50. 50 thousand commercial vehicles.",
        A('Part appears', n('Commercial = from 60 to 110 → 50 thousand, not 110!')),
        D('Mark the grey part from 60 to 110'),
    ], pre=[side(stack_chart(highlight=[(1, 2)], marks=[('brace', 2.3, 60, 110, '50'), ('hline', 118, '≈ 118')]))]))
    n = NU(560)
    s.append(S(SB5, 8, [
        "But maybe what usually interests me is only the total.",
        "Here we see that charts can be tailored to the needs of whoever uses them.",
        A('Fit appears', n('The same data can be shown in different ways — for different users')),
        "I can take the same data and present it to one employee in a table, to another in bars — and to the manager in stacked bars, one on top of the other, because that's the figure that interests him.",
        A('Users appears', n('Employee 1: a table · employee 2: bars · the manager: stacked bars (the total)')),
    ], pre=[vis(car_table(5), w=620, x=345, y=120), vis(stack_chart(), w=600, x=975, y=85)]))
    n = NU(610)
    s.append(S(SB5, 9, [
        "Another nuance that appears on the psychometric exam — and not rarely, by the way — is horizontal bars.",
        "It's exactly a bar chart, only it appears sideways instead of upright. Sometimes it confuses students.",
        A('Horizontal appears', n('Horizontal bars = a bar chart lying on its side')),
        "Let's see an example. The chart describes the average grades at the end of 10th grade in two schools — 'Carob' and 'Zucchini'.",
        A('Example appears', n('For example: the average grade in English was 75 at "Carob" and 80 at "Zucchini".')),
        "For example: the average grade in English at the 'Carob' school was 75, and at 'Zucchini' — 80.",
    ], pre=[wide(school_chart(), w=880)]))
    n = NU(610)
    s.append(S(SB5, 10, [
        "Let's look at the chart. My values are here: from 0 to 100 belongs to the 'Carob' school, and from 0 to 100 here belongs to 'Zucchini'.",
        "Notice the bars are sideways. Unlike the upright bars we had, where the values were on the y-axis, here the values are on the x-axis.",
        A('X values appears', n('The values are on the x-axis now')),
        "They tell us the average English grade at 'Carob' was 75 — 'Carob', English — it really reaches 75. And at 'Zucchini', English reaches the grade 80.",
        A('Check appears', n('Carob, English → 75 ✓ · Zucchini, English → 80 ✓')),
        "So horizontal bars are exactly like bars. If you like, take your notebook and turn it 90 degrees. The bars simply move right and left instead of up and down.",
        A('Turn appears', n('Turn the page 90° — it is an ordinary bar chart')),
    ], pre=[wide(school_chart(highlight=[(0, 1), (1, 1)]), w=880)]))
    n = NS()
    s.append(S(SB5, 11, [
        "That's it for the bar chart. A very common chart on the exam. It's worth going over and knowing the small nuances we went through:",
        A('Nuances appears', n('Horizontal bars · stacked bars · a bar inside a bar')),
        "horizontal bars, stacked bars, a bar inside a bar and so on.",
        "And it's very important to really notice: is it stacked? Is one inside the other? So you don't get confused and think the commercial vehicles are 110 — and not only 50, only the gap.",
        A('Trap appears', n('Trap: in a stack, a part = the gap (50), not the top (110)')),
        "That's it for the bar chart. See you in the next chart.",
    ], pre=[side(stack_chart(highlight=[(1, 2)], marks=[('brace', 2.3, 60, 110, '50'), ('cross', 2, 110)]))]))
    return lesson('ch52-bar', 'Bar Chart', SB5, s, T52)


# =====================================================================================================================
# LESSON 6 · continuous line (seg06)
# =====================================================================================================================
SB6 = ['Start from bars', 'The area strips', 'Check the example', 'Every hour', 'Every quarter hour',
       'Bars become a line', 'Every point counts', 'When is it used?', 'Relative growth', 'Use the slope',
       'The answer: 9:00']


def L_continuous():
    s = [TITLE('Continuous Line Graph', ["The continuous line graph."])]
    n = NU(640)
    s.append(S(SB6, 0, [
        "To understand what a continuous line graph is — and why we need such a graph at all — we'll start with an example. Actually, with a bar chart.",
        "The chart describes data about visitors' activity on the 'Psycho' website over 24 hours in a row.",
        A('Story appears', n('Visitors on the "Psycho" website over 24 hours')),
        "Here I have the hours, and here the number of visitors.",
    ], pre=[wide(site_bars(4), w=950)]))
    n = NU(640)
    s.append(S(SB6, 1, [
        "The rectangles at the bottom of the chart — these rectangles — show the area of the site where most of the visitors are during that hour.",
        A('Strips appears', n('The rectangles at the bottom = the area of the site where MOST visitors are in that hour')),
        D('Run along the rectangles'),
    ], pre=[wide(site_bars(4, marks=[('col', 0, 24)]), w=950)]))
    n = NU(640)
    s.append(S(SB6, 2, [
        "For example — let's look at the example and make sure we really understand the chart.",
        A('Example appears', n('For example: at 16:00 there were 390 visitors on the site; between 16:00 and 17:00 most of them were in the forum.')),
        "At 16:00 there were 390 visitors on the site. I look, and I really see the bar reaches a bit less than 400.",
        "And between 16:00 and 17:00 — that's this area — we have a grey mark here. Grey, according to the legend, is the forum.",
        "Most visitors are in the site's forum. So between 16:00 and 17:00, the visitors are usually in the forum.",
    ], pre=[wide(site_bars(4, hl=[16], marks=[('hline', 390, '390'), ('col', 16, 17)]), w=950)]))
    n = NU(640)
    s.append(S(SB6, 3, [
        "Here we see a measurement every 4 hours. Sometimes I'll want to measure in shorter ranges — say every hour.",
        "Then I add my bars for every hour, and I can still see, in a bar chart, more or less what happens in every hour.",
        A('Hourly appears', n('A bar every hour')),
    ], pre=[wide(site_bars(1), w=950)]))
    n = NU(640)
    s.append(S(SB6, 4, [
        "And sometimes I'll want to know in even smaller ranges: every quarter of an hour, 20 minutes, 10 minutes — sometimes even every minute.",
        "What happens then is lots and lots of bars, close to each other, until I can't see anything — I just see one big area.",
        A('Quarter appears', n('A bar every quarter hour → one big area')),
    ], pre=[wide(site_bars(0), w=950)]))
    n = NU(640)
    s.append(S(SB6, 5, [
        "And if I see one big area, I can replace the bars with a kind of continuous line.",
        A('Line appears', n('Replace the bars with one continuous line')),
    ], pre=[wide(site_curve(), w=950)]))
    n = NU(645)
    s.append(S(SB6, 6, [
        "Unlike the line we had before — a line graph made of straight lines that connected points —",
        "in the continuous line, every point on the line has a meaning.",
        A('Every appears', n('Continuous line: EVERY point on the line is a measurement')),
        "Because, as you saw, what we measured is really all the points. Wherever I am on the graph, there's meaning. Here we chose every quarter hour; I could have chosen every 10 minutes, or every minute.",
        "The more points I add, the more bars I add — I reach a stage where there's no point adding bars any more, and I see a continuous line: I measure all the time.",
        A('Vs appears', n('Line graph (cars): values only at the points · continuous line: everywhere')),
    ], pre=[wide(site_curve(marks=[('pt', 10.5, 324), ('pt', 13.25, 292), ('pt', 18.75, 405)]), w=950)]))
    n = NU(640)
    s.append(S(SB6, 7, [
        "It's common, for example, when measuring temperature. I don't necessarily measure temperature every round hour — when something runs continuously over time, I can measure it with a continuous line, because I measure at every point.",
        A('Temp appears', n('Used for things measured all the time — e.g. temperature')),
        "Unlike the earlier chart, for example, that checked how many vehicles we sold in a certain year. That was a kind of sum for the year: 2010, 2011. I didn't check every day how many I sold.",
        "I could have checked how many cars were sold every day — and then maybe I'd use a continuous line graph.",
        A('Cars appears', n('Cars: one total per year → points / line graph')),
    ], pre=[wide(site_curve(), w=950)]))
    n = NU(640, size=28)
    s.append(S(SB6, 8, [
        "Let's see a sample question. At which hour was the relative increase in the number of visitors on the site, compared with the hour before it, the greatest?",
        A('Q appears', n('At which hour was the relative increase in visitors, compared with the hour before, the greatest?  (1) 9:00  (2) 16:00  (3) 21:00  (4) 23:00')),
        "Relative increase is a bit of a percent matter: understanding where the increase was the most significant — not necessarily in numbers, but relative to what came before.",
        "Was the growth times 1, times 2, times 3, times 4, times 1.5 and so on? The bigger the 'times', the bigger the relative increase.",
        A('Relative appears', n('Relative increase = how many TIMES bigger than the hour before')),
    ], pre=[wide(site_curve(marks=[('pt', 9, 300), ('pt', 16, 390), ('pt', 21, 480), ('pt', 23, 420)]), w=950)]))
    n = NU(640, size=28)
    s.append(S(SB6, 9, [
        "So let's first see the hours in question. At 9:00 we have 300 visitors, and at 8:00 about 80.",
        "That's a very, very big increase. From 100 to 300 is times 3 — so from 80 it's almost times 4.",
        A('9 appears', n('8:00 → 9:00: about 80 → 300, almost ×4')),
        "At 16:00, and a bit before at 15:00: about 350, and 390 — not a very significant increase.",
        "From 20:00 to 21:00, too, there's an increase of about another 50 visitors. And at 23:00, the increase is relatively small.",
        A('Others appears', n('15→16, 20→21, 22→23: small increases compared with the numbers')),
        "Instead of going point by point, calculating what the number is here and there, and computing differences — we use the fact that the chart is visual.",
        "I can mark the trend of the line before each point, and see that here the trend is much sharper — the relative increase was much bigger than at the other points.",
        A('Slope appears', n('Mark the slope before each point → the sharpest one wins')),
        D('Draw the slope before each of the four hours'),
    ], pre=[wide(site_curve(marks=[('seg', 8, 80, 9, 300), ('seg', 15, 350, 16, 390), ('seg', 20, 430, 21, 480), ('seg', 22, 400, 23, 420)]), w=950)]))
    n = NU(640, size=28)
    s.append(S(SB6, 10, [
        "There are also elements of how many visitors I'm at — we won't go into that too much.",
        "But if we compare, for example, two points that are similar in the number of visitors, we can see the slope here is bigger — so the change here was bigger.",
        A('Similar appears', n('Similar numbers of visitors → the steeper slope = the bigger change')),
        "I can see it with my eye; I don't really need to calculate the numbers, add or subtract and so on.",
        "So, as we said, answer 1 is correct. Here we had the greatest relative increase.",
        A('Answer appears', n('Answer (1): 9:00')),
        D('Circle choice 1'),
        "That's it — see you in the next lesson, as usual.",
    ], pre=[wide(site_curve(marks=[('seg', 8, 80, 9, 300), ('label', 9.3, 200, 'almost ×4')]), w=950)]))
    return lesson('ch52-continuous', 'Continuous Line Graph', SB6, s, T52)


# =====================================================================================================================
# LESSON 7 · range chart (seg07, first part)
# =====================================================================================================================
SB7 = ['Min–max again', 'Tel Aviv rents', 'The Z on the axis', 'Bottom, top, mean', 'Check: 6 rooms',
       'Mean is not the middle', 'Ella and Daniel', 'Rent vs. rent out', "Ella's savings", "Daniel's savings",
       "What can't it be?", 'The same as a table', 'Table or chart?']


def L_range():
    s = [TITLE('Range Chart', ["The range chart: minimum and maximum."])]
    n = NS()
    s.append(S(SB7, 0, [
        "In charts too, almost like in every other topic in the psychometric exam, we have the nuance of minimum and maximum — a range of values.",
        "As we've mentioned in many lessons, the National Institute (NITE) really likes this nuance — understanding a range of values. And it shows up here in charts too.",
        A('Range appears', n('Minimum–maximum: NITE loves ranges of values')),
    ], pre=[side(rent_chart())]))
    n = NS()
    s.append(S(SB7, 1, [
        "In front of you is a chart describing the results of a survey that checked the monthly rent of flats in Tel Aviv in 2012, by number of rooms.",
        "Here we can see the number of rooms on the x-axis, and the price in thousands of shekels.",
        A('Axes appears', n('x: number of rooms · y: rent, thousands of NIS')),
    ], pre=[side(rent_chart())]))
    n = NS()
    s.append(S(SB7, 2, [
        "Notice — here we have the zigzag, which tells us that the distance from 0 to 2 is a different distance. It's not really the distance between the other ticks.",
        A('Z appears', n('Z: from 0 to 2 is not to scale')),
        D('Circle the zig-zag'),
        "Here the distance is fixed and accurate; here the distance is a bit different.",
    ], pre=[side(rent_chart())]))
    n = NS()
    s.append(S(SB7, 3, [
        "We have bars by number of rooms. The bottom end of each bar shows the lowest rent that was set, and the top end shows the highest rent.",
        A('Ends appears', n('Bottom of the bar = lowest rent · top = highest rent')),
        "The bold line inside each bar shows the mean rent set for the flats.",
        A('Mean appears', n('Bold line inside = the mean rent')),
    ], pre=[side(rent_chart(hl=[(5, 'min'), (5, 'max')]))]))
    n = NS()
    s.append(S(SB7, 4, [
        "For example, take a 6-room flat. In 6-room flats, the minimum price set was 4,500, and the maximum price was 8,000.",
        A('6 appears', n('For example: 6 rooms — lowest 4,500 · highest 8,000 · mean 6,500')),
        "The mean price was 6,500 — that's the bold line.",
    ], pre=[side(rent_chart(hl=[(5, 'min'), (5, 'max'), (5, 'mean')]))]))
    n = NS()
    s.append(S(SB7, 5, [
        "So this chart also deals with the mean. There's a bold line showing the mean rent.",
        "And as we know the mean: it doesn't always have to be in the middle, between the minimum value and the maximum.",
        A('Not middle appears', n('The mean is not necessarily in the middle of the bar')),
        "When it's higher than the middle, for example, it means there are more expensive flats than cheap ones, and the expensive flats pull the mean up.",
        A('Pull appears', n('Mean near the top → more expensive flats pull it up')),
        "Say, just for example, there's only one flat that costs 2,500, and all the other flats cost 4 or 4.5 — so the mean will be higher.",
        A('Example appears', n('2 rooms: one flat at 2,500, the rest 4–4.5 → mean 4')),
    ], pre=[side(rent_chart(hl=[(1, 'min'), (1, 'mean'), (1, 'max')]))]))
    n = NU(610, size=28)
    s.append(S(SB7, 6, [
        "Let's see a sample question. Ella rents a 2-room flat and rents out a 5-room flat. Daniel rents a 1-room flat and rents out a 4-room flat.",
        "They deposit the difference between the rents in a monthly savings plan.",
        "Which of the following cannot be the difference between their monthly deposits, in shekels?",
        A('Q appears', n('Ella rents a 2-room flat and rents out a 5-room flat. Daniel rents a 1-room flat and rents out a 4-room flat. Each deposits the difference between the rents in savings every month. Which of the following cannot be the difference between their monthly deposits (NIS)?  (1) 0  (2) 2,500  (3) 5,000  (4) 5,500')),
    ], pre=[wide(rent_chart(), w=880)]))
    n = NS()
    s.append(S(SB7, 7, [
        "What are they telling us? Take Ella, for example. She has her own flat, a 5-room flat, which she rents out.",
        "By the way, when I rent out a flat, I'm the one giving the flat, and someone pays me. If I live in a flat, I don't rent it out — I rent it.",
        A('Out appears', n('Rent OUT = you own it, you GET the money')),
        A('Rent appears', n('Rent = you live there, you PAY')),
        "So Ella again: she has a 5-room flat that she rents out — that's the money she gets. And a 2-room flat she lives in, which she rents — that's the money she pays.",
        A('Ella appears', n('Ella: gets the 5-room rent, pays the 2-room rent')),
    ], pre=[side(rent_chart(hl=[(1, 'bar'), (4, 'bar')]))]))
    n = NS()
    s.append(S(SB7, 8, [
        "Let's see what her monthly deposit can be. Take the maximum. The maximum means she gets the most money.",
        "Say she gets 7,500 shekels — the maximum for a 5-room flat — and pays the minimum for a 2-room flat. She gets 7,500 and pays 2,500.",
        A('Max appears', n('Most: gets 7,500 − pays 2,500 = 5,000')),
        "So her savings can be up to 5,000 shekels.",
    ], pre=[side(rent_chart(hl=[(4, 'max'), (1, 'min')]))]))
    n = NS()
    s.append(S(SB7, 8, [
        "The minimum, by the way: maybe she gets only 4,500 — the minimum — and also pays 4,500, because she took the fanciest 2-room flat.",
        "Then it really cancels out: 4.5 minus 4.5 is 0.",
        A('Min appears', n('Least: gets 4,500 − pays 4,500 = 0')),
        "So her savings can be between 0 and 5,000.",
        A('Range appears', n('Ella: from 0 to 5,000')),
    ], pre=[side(rent_chart(hl=[(4, 'min'), (1, 'max')]))]))
    n = NS()
    s.append(S(SB7, 9, [
        "Let's see Daniel. Daniel rents a 1-room flat and rents out a 4-room flat.",
        "The maximum his savings can be: he gets 7,000 if he rents out the 4-room flat at the maximum price, and pays 2,000 — the minimum he'll pay. 7,000 minus 2,000 — also 5,000.",
        A('Max appears', n('Most: gets 7,000 − pays 2,000 = 5,000')),
        "And the minimum: he gets only 4,000 — the minimum — and pays the maximum for a 1-room flat, which is also 4,000. So here too the deposit is 0.",
        A('Min appears', n('Least: gets 4,000 − pays 4,000 = 0')),
        "So for Daniel too, it's between 0 and 5,000.",
        A('Range appears', n('Daniel: from 0 to 5,000')),
    ], pre=[side(rent_chart(hl=[(3, 'max'), (0, 'min'), (3, 'min'), (0, 'max')]))]))
    n = NU(610, size=28)
    s.append(S(SB7, 10, [
        "Which cannot be the difference between the monthly deposits? Can the difference be 0? Yes — say both deposit 5,000 shekels; the difference is 0.",
        "Can it be 2,500? Yes. It can be 2,500 and also 5,000.",
        A('Can appears', n('0 ✓ · 2,500 ✓ · 5,000 ✓ (Ella 5,000, Daniel 0)')),
        "It can't be 5,500. The most each of them can deposit is 5,000. Even in the extreme case where Ella deposits 5,000 and Daniel deposits 0, the difference between them is only 5,000.",
        A('Cannot appears', n('5,500 ✗ — each deposits between 0 and 5,000, so the difference is at most 5,000 → answer (4)')),
        D('Circle choice 4'),
    ], pre=[wide(rent_chart(hl=[(4, 'max'), (1, 'min'), (3, 'min'), (0, 'max')]), w=880)]))
    n = NU(560)
    s.append(S(SB7, 11, [
        "Let's see how this chart would look if they gave it to us in a table.",
        "Here's the number of rooms, and inside the table, in each cell, three numbers.",
        "The reason I'm showing you this table: it's also common on the exam. Often they give tables where, instead of one value in a cell, there are two or three values — each with a different meaning according to its position.",
        A('Cell appears', n('Several numbers in one cell — the position tells you the meaning')),
        "Say they tell us that the top number on the left is the minimum price, the mean is in the middle, and the bottom one is the maximum price.",
        "For example, 1-room flats: 2,000 is the minimum, 3,000 the mean, and 4,000 the maximum. 3,000 marks this line — the mean — and between 2,000 and 4,000 is the range.",
        A('1 room appears', n('1 room: 2 (lowest) · 3 (mean) · 4 (highest) — thousands')),
    ], pre=[vis(rent_table(hl=[(0, 1)]), w=1100, x=410, y=90)]))
    n = NU(600)
    s.append(S(SB7, 12, [
        "What's the advantage of the table? In a table, if I want to add Jerusalem or Eilat to Tel Aviv, I can easily add them.",
        A('Add appears', n('Table: easy to add more cities — one more row each')),
    ], pre=[vis(rent_table((RENT, RENT_J, RENT_E), hl=[]), w=1000, x=380, y=90)]))
    n = NS()
    s.append(S(SB7, 12, [
        "In the chart, if I had to start adding bars, it would create lots and lots of noise — a mess for the eyes. It would be better to see it in three different charts.",
        A('Noise appears', n('Chart: more bars = more noise')),
        "On the other hand, if I did add bars here, it would be easier to compare visually between Tel Aviv and Jerusalem, or Tel Aviv and Eilat — I'd simply see higher or lower bars, depending on the city where we rent.",
        A('Compare appears', n('…but easier to compare the cities by eye: higher or lower bars')),
    ], pre=[side(rent_chart(series=[RENT, RENT_J, RENT_E], title='Monthly rent, 2012', legend='top'))]))
    return lesson('ch52-range', 'Range Chart', SB7, s, T52)


# =====================================================================================================================
# LESSON 8 · regions chart (seg07, second part)
# =====================================================================================================================
SB8 = ['Ranges as areas', 'Health insurance', 'Numbers inside', 'Check the example', 'Any insured person']


def L_regions():
    s = [TITLE('Regions Chart', ["Ranges as areas on the axes."])]
    n = NS()
    s.append(S(SB8, 0, [
        "So far we've seen the range chart as it appears with bars. Another kind of range chart is a chart of areas.",
        "Not bars or specific points on the coordinate system — but a range of numbers: areas on the coordinate system.",
        A('Areas appears', n('Not points or bars: AREAS on the axes')),
    ], pre=[side(ins_chart())]))
    n = NS()
    s.append(S(SB8, 1, [
        "Let's see an example. The graph describes the cost of health insurance according to the height and weight of the insured.",
        "Here I have the height of the insured, and here the weight.",
        A('Axes appears', n('x: height (cm) · y: weight (kg)')),
    ], pre=[side(ins_chart())]))
    n = NS()
    s.append(S(SB8, 2, [
        "And the cost of the insurance is marked inside. Let's see exactly how.",
        "The numbers inside the graph are the yearly cost of health insurance, in thousands of shekels. So it's not 4 — it's 4,000.",
        A('Inside appears', n('The number in each area = the yearly cost, thousands of NIS')),
        "Health insurance prices range from 4,000 to 12,000 shekels a year. We see it really starts at 4 — the lowest — and 12 is the highest.",
        A('Range appears', n('From 4 (4,000) to 12 (12,000)')),
    ], pre=[side(ins_chart(hl=[0, 4]))]))
    n = NS()
    s.append(S(SB8, 3, [
        "For example — the example always puts things in order, to make sure we really understand the chart.",
        A('Example appears', n('For example: an insured person weighing 100 kg, 174 cm tall, pays 6,000 NIS a year.')),
        "An insured person who weighs 100 kilograms: here's 100 kilograms — he's somewhere on this line. And his height is 174 centimetres — he's somewhere on this line.",
        D('Follow 100 kg across and 174 cm up'),
        "Where they cross — this insured person is here, at this point. He pays 6,000 shekels a year for health insurance.",
        "And we really see that this point fell in the area marked with the number 6, the striped area. That's the price of the health insurance he'll pay.",
        A('6 appears', n('The crossing point falls in the striped area "6" → 6,000 NIS ✓')),
    ], pre=[side(ins_chart(marks=[('guide', 174, 100)], hl=[1]))]))
    n = NS()
    s.append(S(SB8, 4, [
        "In the same way I can know for every insured person — once I know his height and his weight — how much he pays for the insurance.",
        A('Any appears', n('Height + weight → the point → the area → the price')),
        "So we've seen an example of a range chart by areas on a coordinate system — not exactly points, but certain areas. According to the point I'm at, I know the amount of the health insurance.",
        "That's it for range charts — minimum–maximum, in between. From here we move on to the next chart. As usual, see you there.",
    ], pre=[side(ins_chart(marks=[('guide', 174, 100)]))]))
    return lesson('ch52-regions', 'Regions Chart', SB8, s, T52)


# =====================================================================================================================
# LESSON 9 · circle chart (seg08)
# =====================================================================================================================
SB9 = ['Common on the exam', 'Same website story', 'Circles = visitors', 'The dark areas', 'Check: 9:00',
       'Axes in a circle', 'Points, bars, line', 'Two identical charts', 'Check: 12:00',
       '12:00–16:00', 'The latest hour?', 'Most, not all', 'Cannot be known']


def circ(**k): return vis(site_circle(**k), w=740, x=345, y=85)


def L_circle():
    s = [TITLE('Circle Chart', ["The circle chart."])]
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 0, [
        "The circle chart is a very common chart on the psychometric exam. Of course it doesn't appear on every exam date — no type of chart does — but it appears quite a lot.",
        A('Common appears', n('Common on the exam — know it well')),
        "It's very, very important to know the circle chart, because it's different from the charts we've learned so far.",
    ], pre=[circ()]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 1, [
        "Let's see an example. We already know the story behind this chart, from the continuous line graph.",
        "The chart describes data about visitors' activity on the 'Psycho' website over 24 hours in a row.",
        A('Story appears', n('Same story: visitors on the "Psycho" website over 24 hours')),
        "Here we have the hours, around the circle.",
        A('Hours appears', n('The hours go round the circle')),
    ], pre=[circ()]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 2, [
        "The number of visitors is shown by the circles. We see this is the line of 500, 400, 300 and so on.",
        A('Circles appears', n('Each circle = a number of visitors: 100, 200 … 500')),
        D('Trace the 300 circle'),
    ], pre=[circ()]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 3, [
        "And the dark areas show the area of the site where most of the visitors are during that hour.",
        A('Dark appears', n('Dark arcs = the area where MOST visitors are in that hour')),
        "If you remember, we had the coloured rectangles at the bottom of the previous chart. We'll see that again in a moment.",
    ], pre=[circ(highlight_spans=[(0, 12, 16), (1, 18, 20), (2, 9, 10)])]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 4, [
        "For example: at 9:00 there are 300 visitors on the site. We go along the line and see the point here — this point is 300 visitors.",
        A('Example appears', n('For example: at 9:00 there were 300 visitors; between 9:00 and 10:00 most were in the forum.')),
        "And between 9:00 and 10:00 — in this range — we see what's coloured grey is this part.",
        "And if I look here, I see it says 'forum'. So between 9:00 and 10:00, most visitors are in the site's forum.",
    ], pre=[circ(guide_hours=[9], highlight_spans=[(2, 9, 10)])]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 5, [
        "Notice the difference between a circle chart and a chart on a coordinate system.",
        "All the charts we saw before, except the table, were charts on a coordinate system: points on axes, bars, a broken line, a continuous line.",
        "Here too we have a kind of coordinate system — only it's turned, curved.",
        A('Bent appears', n('A circle chart = a coordinate system bent into a circle')),
    ], pre=[circ()]))
    n = NU(640)
    s.append(S(SB9, 6, [
        "I can see points here — like points on axes.",
        "I can see a circle chart with bars — like bars on axes: each bar reaches the right height according to the ticks here. The circles are really the height lines.",
        "And I can have a continuous line that runs and connects the points, as we saw in that chart.",
        A('Three appears', n('Points · bars · a continuous line — all can be drawn in a circle')),
    ], pre=[vis(site_circle(style='points', show_band_names=False, bands=()), w=390, x=345, y=85),
            vis(site_circle(style='bars', show_band_names=False, bands=()), w=390, x=765, y=85),
            vis(site_circle(style='curve', show_band_names=False, bands=()), w=390, x=1185, y=85)]))
    n = NU(640)
    s.append(S(SB9, 7, [
        "Let's recall the continuous line graph on the coordinate system: the number of visitors, the hours, and the coloured rectangles here.",
        "In this case, instead of being coloured in different colours, they were simply in a different place on the edge of the circle. On the outer ring — the explanations; then practice, then forum, then other.",
        A('Rings appears', n('Rectangles at the bottom ↔ rings round the circle (outside → in: explanations, practice, forum, other)')),
        "And we had the continuous line running inside the chart.",
        "So what we have here are two charts that are completely identical. Whatever is described here is described exactly here too.",
        A('Same appears', n('Two identical charts: same data, different shape')),
    ], pre=[vis(site_curve(), w=640, x=345, y=110), vis(site_circle(show_band_names=False), w=500, x=1030, y=85)]))
    n = NU(640)
    s.append(S(SB9, 8, [
        "Let's see an example. At 12:00 I can see I have a bit more than 300 visitors — 320 or 330.",
        "Let's see it here at 12:00. I go here and I see the point is really here, a bit past the line of 300. About 320 visitors.",
        A('12 appears', n('12:00: a bit more than 300 (≈ 320) — in both charts')),
    ], pre=[vis(site_curve(marks=[('guide', 12, 325)]), w=640, x=345, y=110), vis(site_circle(show_band_names=False, guide_hours=[12]), w=500, x=1030, y=85)]))
    n = NU(640)
    s.append(S(SB9, 9, [
        "I can see that between 12:00 and 16:00 — four hours — most visitors were in the explanations area.",
        "I look here between 12:00 and 16:00 and I really see the grey colour is here — on the outer edge, the outermost ring — which belongs to the explanations.",
        A('Expl appears', n('12:00–16:00: most visitors in the explanations (outer ring)')),
        "So what we really have is exactly the same chart; it just looks different.",
    ], pre=[vis(site_curve(marks=[('col', 12, 16)]), w=640, x=345, y=110), vis(site_circle(show_band_names=False, highlight_spans=[(0, 12, 16)]), w=500, x=1030, y=85)]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 10, [
        "Let's see a sample question. What is the latest hour at which there are visitors in the practice area of the site?",
        A('Q appears', n('What is the latest hour at which there are visitors in the practice area?')),
        "Let's do it on the circle chart. The practice area is here. For a late hour I start from here, and I see that around 20:00 is the last hour where the practice area is coloured.",
        A('20 appears', n('The practice arc ends at 20:00 …')),
        "But is that really the last hour at which there are visitors in the practice area?",
    ], pre=[circ(highlight_spans=[(1, 18, 20)], highlight_hours=[20])]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 11, [
        "Notice what the question is and what the data say. The data say the dark areas show the area of the site where most of the visitors are in that hour.",
        "What does that mean? Between 18:00 and 20:00, most of the visitors on the site were in the practice area.",
        A('Most appears', n('Dark = where MOST visitors are — not where ALL of them are')),
        "Were there people in the practice area at later hours too? Maybe. Take, for example, between 22:00 and 23:00: I know most were in the forum.",
        "But that still doesn't mean nobody was in the practice area. Maybe a few visitors were in practice, and in explanations, or other areas.",
        A('Some appears', n('22:00–23:00: most in the forum — some may still be practising')),
        "The grey mark doesn't show where all the visitors are — only where most are, more than half.",
    ], pre=[circ(highlight_spans=[(1, 18, 20), (2, 22, 23)])]))
    n = NU(120, x=1110, w=470, size=27)
    s.append(S(SB9, 12, [
        "So we can't really know the latest hour. Maybe until midnight someone was still practising on the site. He wasn't the majority, but he was there.",
        "Or maybe, on the other hand, at 23:00 that's it — nobody was practising any more. People were on the site, some in explanations, most in the forum, some elsewhere — but nobody in practice.",
        A('Cannot appears', n('So the latest hour in practice cannot be known from the chart')),
        "So we can't know the latest hour at which there are visitors in the practice area — I don't know whether after 20:00 they stayed there or not, and when people stopped being there.",
        "What's important to me that you understand from this lesson: it's exactly like a chart on a coordinate system, only the ticks of the y-axis are marked as circles all around.",
        "Theoretically I could cut the chart here and spread it out — fold this part to the right and this half to the left — and I'd get straight lines. The same chart on a coordinate system.",
        A('Unfold appears', n('Cut it open and unfold it → a normal chart on axes')),
        "That's it — see you, as usual, in the next lesson. Bye.",
    ], pre=[circ(highlight_spans=[(1, 18, 20)])]))
    return lesson('ch52-circle', 'Circle Chart', SB9, s, T52)


# =====================================================================================================================
# LESSON 10 · cumulative graph (seg09)
# =====================================================================================================================
SB10 = ['Values add up', 'Pixeltech income', 'Check: May', 'Not May alone', 'Like a bank account',
        'Month = difference', 'No income?', 'Flat = zero', 'Total income', 'Cumulative: summary']

DEPOSITS = table(['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                 [['Total so far', '10', '20', '50', '50', '70', '80'], ['This month', '10', '10', '30', '0', '20', '10']],
                 col_w=[1.7] + [1] * 6, W=900, size=22)


def L_cumulative():
    s = [TITLE('Cumulative Graph', ["The cumulative graph."])]
    n = NS()
    s.append(S(SB10, 0, [
        "A cumulative graph is a graph whose data appear cumulatively.",
        "That means the value of each point isn't really its own value — it's a sum of all the values before it.",
        A('Sum appears', n('Each point = the sum of everything up to it')),
        "To find the value at a certain point, we have to subtract what was at the previous point.",
        A('Subtract appears', n('A single period = this point − the previous point')),
    ], pre=[side(pix_chart())]))
    n = NS()
    s.append(S(SB10, 1, [
        "Let's see an example. In front of you is a graph describing the cumulative income of the 'Pixeltech' company during the first half of 2013.",
        "Here we can see months, and here cumulative income in thousands of shekels. So the 80 isn't 80 — it's 80,000 shekels.",
        A('Axes appears', n('x: months · y: cumulative income, thousands of NIS (80 = 80,000)')),
    ], pre=[side(pix_chart())]))
    n = NS()
    s.append(S(SB10, 2, [
        "For example, the income of Pixeltech in May was 20,000 shekels.",
        A('Example appears', n('For example: Pixeltech\'s income in May was 20,000 NIS.')),
        "I go to May, I go up — and I see I'm at 70,000 shekels. Why is that?",
        A('70 appears', n('But at May the graph shows 70 …')),
    ], pre=[side(pix_chart(marks=[('guide', 4, 70, '70')]))]))
    n = NS()
    s.append(S(SB10, 3, [
        "Let's see what's written here: the graph describes the cumulative income. What does cumulative income mean?",
        "The value at the May point isn't really what I had in May — it's not May's income. It's all the income of January, February, March, April and May together.",
        A('Together appears', n('70 = Jan + Feb + Mar + Apr + May together')),
        "So this point, 70,000 shekels, is really the income of all these months.",
        "And if I go to April, I have 50,000 shekels here. That's not April's income — it's all the income up to April: April, March, February and January together.",
        A('April appears', n('April: 50 = everything up to April')),
    ], pre=[side(pix_chart(marks=[('col', -0.4, 4.4), ('guide', 3, 50, '50')]))]))
    n = NS()
    s.append(S(SB10, 4, [
        "Imagine I'm depositing into a bank account. Here I had 0 in the account.",
        "In January I deposited 10,000 shekels, so I got to 10. In February I deposited more money and got to 20. In March I deposited more and got to 50.",
        "In April — again 50. In May I deposited more money and got to 70.",
        A('Bank appears', n('Like a bank account you only deposit into: the balance keeps growing')),
        "It's convenient to see it with a current account I only deposit into — because as long as I don't take out money (and don't!), the account keeps what was there before plus what I add.",
    ], pre=[side(pix_chart()), vis(DEPOSITS, w=800, x=350, y=620)]))
    n = NS()
    s.append(S(SB10, 5, [
        "So if from April to May I have a change of 20,000 — from 50 to 70 — that means in May I deposited only another 20,000 shekels.",
        A('Diff appears', n('May = 70 − 50 = 20 thousand NIS')),
        "As we see, in May our income was only 20,000 shekels: this is 70,000; this is the 50,000 from April; and how much I had to add to reach May's 70,000 — I added another 20,000 here.",
    ], pre=[side(pix_chart(marks=[('guide', 4, 70, '70'), ('hline', 50, '50'), ('brace', 4.15, 50, 70, '+20')]))]))
    n = NS()
    s.append(S(SB10, 6, [
        "Let's see a sample question. In which of the months described in the graph did Pixeltech have no income at all?",
        A('Q appears', n('In which month did Pixeltech have no income at all?')),
        "Here we can see it really visually.",
    ], pre=[side(pix_chart())]))
    n = NS()
    s.append(S(SB10, 7, [
        "Once I have a flat line here — if up to March I earned 50,000 shekels, and up to April I also earned 50,000 —",
        "that means in April there was no income. There was no income, so I stayed the same.",
        A('Flat appears', n('Flat segment = nothing was added = no income that month')),
        "If I'd deposited 50,000 into the account so far, in April I deposited nothing and stayed at 50,000. So our answer is April.",
        A('Answer appears', n('Answer: April')),
    ], pre=[side(pix_chart(hl=[(0, 2)]))]))
    n = NS()
    s.append(S(SB10, 8, [
        "Next question. What was Pixeltech's total income in all the months described in the graph?",
        A('Q appears', n('What was the total income in all the months in the graph?')),
        "I need the total of January, February, March, April, May and June. Notice — I don't need to start adding January plus February plus March.",
        "This whole chart describes cumulative income. So in June I'm at 80,000 — and those 80,000 shekels are the total income of all the months.",
        A('June appears', n('The last point = the total: 80,000 NIS')),
        "That's the whole meaning of a cumulative chart: a graph that accumulates everything up to now.",
    ], pre=[side(pix_chart(marks=[('guide', 5, 80, '80')]))]))
    n = NS()
    s.append(S(SB10, 9, [
        "This question is actually very simple. In June I'm at 80,000 — and 80,000 isn't in June, it's up to June. From January to June the income was 80,000 shekels.",
        A('Up to appears', n('"80 at June" = up to June, not in June')),
        "That's a cumulative graph. A cumulative graph is not very common — but it does appear, and it's important to know it.",
        "It's one of those types that it's better to know beforehand, and not meet for the first time in the exam.",
        A('Know appears', n('Not common — but meet it here, not first in the exam')),
        "That's it for the cumulative graph. See you in our last video, where we finish the topic of charts.",
    ], pre=[side(pix_chart())]))
    return lesson('ch52-cumulative', 'Cumulative Graph', SB10, s, T52)


# =====================================================================================================================
# LESSON 11 · change graph (seg10)
# =====================================================================================================================
SB11 = ['Rare but tricky', 'Values = changes', 'Ignore the line', 'Green Light', 'Check: week 2',
        'Down, but up', 'No change?', 'Remove the line', 'Weeks 5, 9, 10', 'From 75 in week 2',
        'Week by week', 'Change graph: summary']


def L_change():
    s = [TITLE('Change Graph', ["The change graph."])]
    n = NS()
    s.append(S(SB11, 0, [
        "The change graph is a very, very rare graph on the exam. It's unlikely we'll meet it.",
        "But because it's an unusually hard chart compared with the others, it's customary to teach it and learn it — so that if we happen to meet it on the exam, it won't be the first time, and we'll already know the catch behind it.",
        A('Rare appears', n('Very rare — but hard: know the catch')),
    ], pre=[side(vol_chart())]))
    n = NS()
    s.append(S(SB11, 1, [
        "What's a change graph? A graph whose values mark some change.",
        "They don't mark the numerical value of what we measure — but a change.",
        A('Change appears', n('Each value = a CHANGE, not the amount itself')),
    ], pre=[side(vol_chart())]))
    n = NS()
    s.append(S(SB11, 2, [
        "So as not to get confused, it's recommended to ignore the line in the graph and relate only to the points that represent the values.",
        A('Ignore appears', n('Ignore the line — look only at the points', size=30)),
    ], pre=[side(vol_chart(show_line=False))]))
    n = NS()
    s.append(S(SB11, 3, [
        "Let's see an example. The graph describes the change in the number of volunteers at the 'Green Light' association at the end of each week, compared with the end of the previous week, over a period of 10 weeks.",
        A('Story appears', n('Volunteers at "Green Light": change at the end of each week vs. the previous week')),
        "We have weeks here — 10 weeks — and the change in the number of volunteers. Here there's an addition of volunteers, and here a drop.",
        A('Signs appears', n('Above 0 = volunteers joined · below 0 = volunteers left')),
    ], pre=[side(vol_chart())]))
    n = NS()
    s.append(S(SB11, 4, [
        "For example: at the end of the second week there were 10 more volunteers at the association than at the end of the first week.",
        A('Example appears', n('For example: at the end of week 2 there were 10 more volunteers than at the end of week 1.')),
        "Notice: here it says plus 10. That's 10 more than what was here.",
        "Say at the end of the first week there were 100 volunteers — at the end of the second week there are 110. During the second week, 10 volunteers joined.",
        A('100 appears', n('Week 1: 100 → week 2: 110')),
    ], pre=[side(vol_chart(hl=[1]))]))
    n = NS()
    s.append(S(SB11, 5, [
        "The confusing part of the chart is, for example, this part. Here in the chart I have a drop: the line goes down.",
        "But there isn't really a drop here. In fact I have a rise in the number of volunteers. Why?",
        "Because if I ignore the line for a moment and look only at this point — this point says plus 5 compared with the previous week.",
        A('Up appears', n('Week 3: the line goes DOWN, but +5 = 5 MORE volunteers')),
        "So if last week there were 110, here there are 115.",
    ], pre=[side(vol_chart(hl=[2], marks=[('seg', 1, 10, 2, 5)]))]))
    n = NS()
    s.append(S(SB11, 6, [
        "Let's see a sample question. In how many of the weeks was there no change in the number of volunteers at the association?",
        A('Q appears', n('In how many of the weeks was there no change in the number of volunteers?')),
        "What does 'no change' mean? The change was 0.",
        A('Zero appears', n('No change = the point is at 0')),
    ], pre=[side(vol_chart())]))
    n = NS()
    s.append(S(SB11, 7, [
        "As we recommended before, let's ignore the line. Let's make the line disappear for a moment.",
        "In how many weeks was there no change — the change was 0? I can see I have three such weeks: the end of week 5, week 9 and week 10.",
        A('Three appears', n('At 0: weeks 5, 9, 10 → 3 weeks')),
    ], pre=[side(vol_chart(show_line=False, hl=[4, 8, 9]))]))
    n = NS()
    s.append(S(SB11, 8, [
        "Now let's bring the line back for a moment. Notice: here it looks as if there's a drop, and here as if there's a rise.",
        "There isn't really a rise. I ignore the line and look only at the point. This point tells me there was 0 change: what there was at the end of week 4 is exactly what there is at the end of week 5.",
        A('5 appears', n('Week 5: the line drops, but 0 = no change')),
        "The same here — there isn't really a rise. What there was at the end of week 8 is exactly what there is at the end of week 9, because in week 9 there was no change.",
        A('9 appears', n('Week 9: the line rises, but 0 = no change')),
        "So how many points have no change? 5, 9 and 10 — three such points, three weeks.",
    ], pre=[side(vol_chart(hl=[4, 8, 9], marks=[('seg', 3, 5, 4, 0), ('seg', 7, -5, 8, 0)]))]))
    n = NU(120, x=1195, w=390, size=26)
    s.append(S(SB11, 9, [
        "Another question. If at the end of the second week there were 75 volunteers at the association, how many were there at the end of the sixth week?",
        A('Q appears', n('Week 2 = 75 volunteers. How many at the end of week 6?')),
        "So at the end of week 2 I have 75 volunteers. That's what I have here.",
        "I make the line disappear, because it's more convenient to see only the points and relate only to them.",
        A('75 appears', n('Week 2: 75')),
    ], pre=[side(vol_chart(show_line=False, hl=[1]))]))
    n = NU(120, x=1195, w=390, size=26)
    s.append(S(SB11, 10, [
        "End of week 3: I have plus 5. Plus 5 means 5 more than week 2 — even though it looks like a drop, this point is lower than the end of week 2.",
        "I don't look at the previous point. I ignore everything here and look only at this point — and I see plus 5. So I add 5: I'm at 80.",
        A('3 appears', n('Week 3: +5 → 80')),
        "Now week 4. It looks like no change, because it's a straight line — but I ignore the line and everything before, and look only at this point. At the end of week 4: plus 5. So I add another 5.",
        A('4 appears', n('Week 4: +5 → 85')),
        "At the end of week 5 it looks like a drop — from 85 at week 4 to week 5. In fact, I look only at this point: no change, 0. If nothing changed, here I also have 85.",
        A('5 appears', n('Week 5: 0 → 85')),
        "And the last point: I can see I have minus 10. 85 minus 10 is 75.",
        A('6 appears', n('Week 6: −10 → 75')),
        "Notice — when I bring the line back, it's confusing. Here the line is straight, but in fact there's a rise. And here the line goes down, and in fact there's no change.",
        "So, as we said: ignore the line. Don't look at it — look only at the points themselves. At the end of week 6 we have 75 volunteers. Answer 1 is correct.",
        A('Answer appears', n('End of week 6: 75 volunteers', size=30)),
    ], pre=[side(vol_chart(hl=[2, 3, 4, 5]))]))
    n = NS()
    s.append(S(SB11, 11, [
        "To sum up the change graph: it's a confusing, hard graph. Maybe some of you will want to watch this video again — that's fine.",
        A('Hard appears', n('Confusing and hard — watch again if you need to')),
        "But on the other hand, we'll probably not meet it on the exam, because it's very, very rare.",
        "That's it — we've finished the topic of charts. As I told you at the start, in the introduction lesson: the types of charts on the psychometric exam are very clear. It's exactly the types we went through in the last lessons — including, as an extra, this change graph.",
        A('Types appears', n('The exam\'s charts = the types in these lessons')),
        "In very, very rare cases other charts will appear, like this change graph, or some chart in another form — but it's really rare.",
        "If you go over the chart lessons we learned and close the questions, you're simply ready for the exam. See you in the next topics.",
    ], pre=[side(vol_chart())]))
    return lesson('ch52-change', 'Change Graph', SB11, s, T52)


# =====================================================================================================================
# LESSON 12 · summary
# =====================================================================================================================
SB12 = ['Table', 'Points on axes', 'Line graph', 'Bar chart', 'Continuous line', 'Range chart', 'Regions chart',
        'Circle chart', 'Cumulative graph', 'Change graph', 'Before a chart set']


def _sum(sb, i, svg, read, trap, say_read, say_trap, w=830):
    n = NS()
    return S(sb, i, [
        A('How appears', n('How to read: ' + read)),
        say_read,
        A('Trap appears', n('Trap: ' + trap)),
        say_trap,
    ], pre=[side(svg, w=w)])


def L_summary():
    s = [TITLE('Charts & Tables: Summary', ["Let's sum up all the types of charts and tables — how to read each one, and its trap."])]
    sb = SB12
    s.append(_sum(sb, 0, car_table(5, highlight=[(0, 3)]),
                  'cross a row and a column; many data, focus on the one you need',
                  'who is the whole? ("of" → the whole) · the question may be percent, average, overlap…',
                  "A table: cross a row and a column to find a value. It holds lots of data — focus only on what you need.",
                  "The trap: in percent questions, know who the whole is — what comes after 'of'. And remember that any problem type — averages, overlap — can hide inside."))
    s.append(_sum(sb, 1, car_scatter(4),
                  'each marker (see the legend) sits exactly at its value; check the units',
                  '"90" may mean 90,000 · a Z on the axis = not to scale there',
                  "Points on axes: each series has its marker in the legend, and every point sits exactly at its value. Check the units.",
                  "The trap: thousands on the axis — 90 means 90,000. And a zigzag, a Z, means that part of the axis isn't to scale."))
    s.append(_sum(sb, 2, car_line(),
                  'values only at the marked points; the slope shows the trend',
                  'there is no "2010½" — the line between points means nothing',
                  "A line graph: the values are only at the marked points; the line shows the trend — steeper means a bigger change.",
                  "The trap: reading a value between two points. There's no 2010 and a half."))
    s.append(_sum(sb, 3, stack_chart(highlight=[(1, 2)], marks=[('brace', 2.3, 60, 110, '50')]),
                  'bar height = value; side by side, one inside another, stacked, or horizontal',
                  'stacked: a part = the gap (50), not the top (110)',
                  "A bar chart: the height is the value. Bars can stand side by side, one inside another, stacked, or lie horizontally — just turn the page.",
                  "The trap: in stacked bars a part is the gap — commercial vehicles are 50, not 110."))
    s.append(_sum(sb, 4, site_curve(marks=[('seg', 8, 80, 9, 300)]),
                  'every point on the line is a measurement; the steepest slope = the biggest change',
                  'use your eyes before you calculate · relative change = how many times',
                  "A continuous line: every point on it is a measurement. Compare slopes with your eyes.",
                  "The trap: calculating everything. For the biggest relative increase, look for the sharpest slope first."))
    s.append(_sum(sb, 5, rent_chart(hl=[(4, 'max'), (1, 'min')]),
                  'bottom = minimum, top = maximum, bold line = mean',
                  'the mean is not the middle · extreme cases: max − min and min − max',
                  "A range chart: the bottom of the bar is the minimum, the top the maximum, and the bold line the mean.",
                  "The trap: the mean isn't necessarily the middle. And for 'what can't it be', check the extreme cases: max minus min, min minus max."))
    s.append(_sum(sb, 6, ins_chart(marks=[('guide', 174, 100)], hl=[1]),
                  'find the point from both axes → read the number of its area',
                  'the number is in thousands (6 = 6,000) · always check against the example',
                  "A regions chart: find the point from both axes, and read the number of the area it falls in.",
                  "The trap: the units — 6 is 6,000. Always check against the example."))
    s.append(_sum(sb, 7, site_circle(highlight_spans=[(1, 18, 20)]),
                  'circles = the value lines; the hours go round; the rings = areas',
                  'dark = where MOST are, not all → "the latest hour" may be unknowable',
                  "A circle chart: it's a coordinate system bent into a circle. The circles are the value lines, the hours go round.",
                  "The trap: the dark area shows where most visitors are — not all. Sometimes the answer is: it can't be known.", w=720))
    s.append(_sum(sb, 8, pix_chart(hl=[(0, 2)], marks=[('guide', 5, 80, '80')]),
                  'each point = the total so far; one month = this point − the previous one',
                  'the value at May is NOT May\'s income · flat = zero that month · last point = the total',
                  "A cumulative graph: each point is the total so far. One month is this point minus the previous one.",
                  "The trap: reading May's point as May's income. Flat means zero that month; the last point is the grand total."))
    s.append(_sum(sb, 9, vol_chart(hl=[4, 8, 9]),
                  'each point = the change from the previous period; 0 = no change',
                  'ignore the line — "down" can be a rise, "flat" can be a rise',
                  "A change graph: each point is the change from the previous period. Zero means no change.",
                  "The trap: the line. Down can be a rise, flat can be a rise. Ignore it — look only at the points."))
    n = NS()
    s.append(S(sb, 10, [
        "And before every chart set, always:",
        A('1 appears', n('1 · Read the explanation')),
        A('2 appears', n('2 · Check the example in the chart — does it match?')),
        "Read the explanation, and check the example in the chart. Does it match what you understand?",
        A('3 appears', n('3 · Titles, units, notes')),
        "Look at the titles, the units — thousands, percent — and every note.",
        A('4 appears', n('4 · The questions get harder: Q1 = pull out a value')),
        "The questions get harder as you go; the first usually just pulls out a value.",
        A('5 appears', n('5 · Example still not clear? Skip, and come back at the end')),
        "And if the example still isn't clear after a slow second reading — skip the set and come back at the end. But a chart at the start of the section — don't skip it. Good luck.",
    ], pre=[side(set_page('example'))]))
    return lesson('ch52-summary', 'Charts & Tables: Summary', SB12, s, T52)


MODULES = [L_intro(), L_tables(), L_scatter(), L_line(), L_bar(), L_continuous(), L_range(), L_regions(), L_circle(),
           L_cumulative(), L_change(), L_summary()]

MEMORY = [
    dict(id='mem-ch52-chart-types', after='ch52-summary', title='Chart types at a glance',
         intro='Every chart set: read the explanation, check the example in the chart, look at titles, units and notes. '
               'The questions go from easy to hard.',
         tables=[dict(head=['Type', 'What it shows', 'How to read', 'Trap'], rows=[
             ['!Table', 'Many data about each item, in rows and columns', 'Cross a row and a column; focus on what you need',
              'Who is the whole in a percent ("of")? Any problem type can hide inside'],
             ['!Points on axes', 'Values as markers on a coordinate system', 'Legend → marker; each point sits exactly at its value',
              'Units (90 = 90,000); a Z on the axis = not to scale there'],
             ['!Line graph', 'The same points joined by lines', 'Values only at the points; slope = trend',
              'No values between the points ("2010½")'],
             ['!Bar chart', 'Bar height = value (grouped, nested, stacked, horizontal)', 'Read the height (or length) against the axis',
              'Stacked: a part = the gap, not the top'],
             ['!Continuous line', 'Something measured all the time', 'Every point is a value; compare slopes by eye',
              'Relative change = how many times, not how many more'],
             ['!Range chart', 'Minimum, maximum and mean per category', 'Bottom = min, top = max, bold line = mean',
              'Mean ≠ middle; check extreme cases (max − min, min − max)'],
             ['!Regions chart', 'Areas on two axes, each with a value', 'Find the point from both axes → read its area',
              'Units (6 = 6,000); check against the example'],
             ['!Circle chart', 'Axes bent into a circle (e.g. 24 hours)', 'Circles = value lines; hours go round; rings = areas',
              'Dark = where MOST are, not all → sometimes it cannot be known'],
             ['!Cumulative graph', 'Running totals', 'One period = this point − the previous one; last point = total',
              'The point at May is not May\'s value; flat = zero'],
             ['!Change graph (rare)', 'The change from the previous period', 'Look only at the points: + more, − fewer, 0 no change',
              'Ignore the line: down or flat can still be a rise'],
         ])],
         tips=['The example is the key: if it does not match what you see, stop and reread slowly.',
               'Still unclear? Skip the set and come back at the end - but do not skip a chart at the start of the section.',
               'Charts are drawn accurately: use your eyes (higher, steeper) before you calculate.',
               'Recommended time: 5-6 minutes per set.']),
]
