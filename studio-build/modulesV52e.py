# Quantitative Reasoning · Topic 52 · Charts & Tables - self-practice units 11-15 (charts practice book).
# Source: charts_src/practice_book b028-b037 (charts + questions), key b049, written solutions b090-b108.
# The book sets are scanned real NITE sets, so every unit here is an ORIGINAL set: new story, new data, the same chart
# type and visual features, the same number / types of questions with the same tricks, and the correct answer in the
# same position as the book key.  _verify() (run at import) recomputes every answer from the data below and asserts
# that exactly one choice is right and that it sits at the key position.
import datetime as _dt
import re
from vbank import _q
from math_api import rich_html

T52 = 52
INK, TEAL, AMBER, SOFT, GRID, MUTED = '#0F172A', '#0F766E', '#F5A524', '#E6F4F1', '#D8E6E3', '#5B6B7A'
AMBER_SOFT, GREYBG = '#FDEBC8', '#E3E8EC'
FONT = "font-family=\"'Helvetica Neue',Helvetica,Arial,sans-serif\""
NOTE = 'Note: In answering each question, disregard the information appearing in the other questions.'

QUESTIONS, FIG = {}, {}
KEY = {11: [1, 1, 4, 1, 2], 12: [2, 2, 3, 4, 2], 13: [4, 3, 3, 1], 14: [4, 3, 3, 4, 1], 15: [3, 3, 4, 2]}   # book key (b049)


# =====================================================================================================================
# svg helpers
# =====================================================================================================================
def _svg(W, H, label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s"><title>%s</title>'
            '<rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W, H, label, label, W, H, body))


def _t(x, y, s, size=18, color=INK, anchor='middle', weight=400, rot=None, halo=False):
    tr = ' transform="rotate(%d %.1f %.1f)"' % (rot, x, y) if rot else ''
    if halo: tr += ' stroke="#ffffff" stroke-width="4" paint-order="stroke" stroke-linejoin="round"'
    s = str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle" fill="%s" %s font-size="%d" font-weight="%d"%s>%s</text>'
            % (x, y, anchor, color, FONT, size, weight, tr, s))


def _l(x1, y1, x2, y2, color=INK, w=1.5, dash=None):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, color, w, ' stroke-dasharray="%s"' % dash if dash else ''))


def _r(x, y, w, h, fill='none', stroke=INK, sw=1.5):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, w, h, fill, stroke, sw)


def _c(x, y, r, fill='#ffffff', stroke=INK, sw=2):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fill, stroke, sw)


def _tri(x, y, s, fill=TEAL, stroke=TEAL, sw=1.5):
    return ('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (x, y - s, x + s * 0.95, y + s * 0.7, x - s * 0.95, y + s * 0.7, fill, stroke, sw))


def _nest(svg, x, y, w, h):
    return svg.replace('<svg ', '<svg x="%d" y="%d" width="%d" height="%d" ' % (x, y, w, h), 1)


def _plain(s):
    s = re.sub(r'(\d)\\frac\{(\d+)\}\{(\d+)\}', r'\1 \2/\3', s)
    s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
    s = s.replace(r'\cdot', '·').replace(r'\times', '×').replace(r'\approx', '≈').replace(r'\ge', '≥').replace(r'\le', '≤')
    s = s.replace(r'\%', '%').replace(r'\;', ' ').replace(r'\,', ' ').replace(r'\text', '').replace('{', '').replace('}', '')
    return re.sub(r'[ \t]+', ' ', s.replace('$', '')).strip()


INTRO_HEAD = {'chart': 'Study the chart below, then answer the questions that follow.',
              'charts': 'Study the charts below, then answer the questions that follow.',
              'tables': 'Study the tables below, then answer the questions that follow.',
              'table': 'Study the table below, then answer the questions that follow.'}


def mk(unit, n, title, intro, stem, choices, key, steps, fig):
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
    QUESTIONS[qid] = q; FIG[qid] = fig


# =====================================================================================================================
# UNIT 11 · two tagged storks on their migration (book: two travellers, countries x months, circles / triangles,
# day-of-month labels, the second traveller's countries as 3 two-row bands on the right)
# =====================================================================================================================
U11_MONTHS = [(2022, 9), (2022, 10), (2022, 11), (2022, 12), (2023, 1), (2023, 2), (2023, 3), (2023, 4), (2023, 5)]
U11_MNAME = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
U11_ROWS = ['Romania', 'Turkey', 'Israel', 'Egypt', 'Sudan', 'Kenya']          # Luna, row 0 = bottom
U11_BANDS = ['Romania', 'Jordan', 'Ethiopia']                                  # Max, band k = rows 2k and 2k+1
D = _dt.date
LUNA = [(D(2022, 9, 12), 0), (D(2022, 9, 24), 0), (D(2022, 9, 24), 1), (D(2022, 10, 6), 1), (D(2022, 10, 9), 2),
        (D(2022, 10, 19), 2), (D(2022, 10, 23), 3), (D(2022, 11, 4), 3), (D(2022, 11, 15), 3), (D(2022, 11, 24), 3),
        (D(2022, 12, 6), 3), (D(2022, 12, 10), 4), (D(2022, 12, 22), 4), (D(2023, 1, 4), 4), (D(2023, 1, 12), 5),
        (D(2023, 1, 25), 5), (D(2023, 2, 8), 5), (D(2023, 2, 22), 5), (D(2023, 2, 27), 4), (D(2023, 3, 12), 4),
        (D(2023, 3, 16), 3), (D(2023, 3, 27), 3), (D(2023, 4, 5), 2), (D(2023, 5, 6), 0), (D(2023, 5, 25), 0)]
MAX = [(D(2022, 9, 1), 1), (D(2022, 9, 16), 1), (D(2022, 9, 28), 3), (D(2022, 10, 9), 3), (D(2022, 10, 18), 4),
       (D(2022, 11, 2), 4), (D(2022, 11, 15), 4), (D(2022, 11, 27), 4), (D(2022, 12, 6), 2), (D(2023, 1, 1), 2),
       (D(2023, 1, 12), 4), (D(2023, 1, 30), 4), (D(2023, 2, 14), 4), (D(2023, 3, 3), 2), (D(2023, 3, 17), 2),
       (D(2023, 3, 25), 2), (D(2023, 4, 14), 1), (D(2023, 5, 8), 1)]
def luna_c(r): return U11_ROWS[r]
def max_c(r): return U11_BANDS[r // 2]

U11_X0, U11_CW, U11_Y1, U11_RH = 150.0, 80.0, 540.0, 66.0
U11_PAD = 6.0


def u11x(d):
    k = U11_MONTHS.index((d.year, d.month))
    nxt = D(d.year + (d.month == 12), d.month % 12 + 1, 1)
    days = (nxt - D(d.year, d.month, 1)).days
    return U11_X0 + U11_PAD + (k + (d.day - 0.5) / days) * (9 * U11_CW - 2 * U11_PAD) / 9.0


def u11y(r): return U11_Y1 - (r + 0.5) * U11_RH


def u11_svg():
    W, H = 1000, 610
    X1, Y0 = U11_X0 + 9 * U11_CW, U11_Y1 - 6 * U11_RH
    o = []
    # legend
    o.append(_r(220, 12, 560, 40, '#ffffff', INK, 1.4))
    o.append(_l(245, 32, 300, 32, INK, 2)); o.append(_c(245, 32, 7)); o.append(_c(300, 32, 7))
    o.append(_t(316, 33, 'Sightings of Luna', 17, INK, 'start', 600))
    o.append(_l(520, 32, 575, 32, TEAL, 2, '6 4')); o.append(_tri(520, 33, 9)); o.append(_tri(575, 33, 9))
    o.append(_t(591, 33, 'Sightings of Max', 17, INK, 'start', 600))
    # headings
    o.append(_t(22, 78, 'Countries where Luna', 16, INK, 'start', 700)); o.append(_t(22, 97, 'was sighted', 16, INK, 'start', 700))
    o.append(_c(128, 97, 6.5))
    o.append(_t(980, 78, 'Countries where Max', 16, INK, 'end', 700)); o.append(_t(955, 97, 'was sighted', 16, INK, 'end', 700))
    o.append(_tri(970, 98, 7.5))
    # left labels (Luna, one per row) and right bands (Max, one per two rows)
    for r, name in enumerate(U11_ROWS):
        y = u11y(r)
        o.append(_r(18, y - U11_RH / 2, U11_X0 - 24, U11_RH, GREYBG, INK, 1.4))
        o.append(_t(18 + (U11_X0 - 24) / 2, y, name, 18, INK, 'middle', 600))
    band_fill = [AMBER_SOFT, SOFT, '#EDE7F6']
    for k, name in enumerate(U11_BANDS):
        yb = U11_Y1 - 2 * k * U11_RH
        o.append(_r(X1 + 6, yb - 2 * U11_RH, 124, 2 * U11_RH, band_fill[k], INK, 1.4))
        o.append(_t(X1 + 68, yb - U11_RH, name, 19, INK, 'middle', 700))
    # grid
    for r in range(7):
        o.append(_l(U11_X0, U11_Y1 - r * U11_RH, X1, U11_Y1 - r * U11_RH, GRID, 1.2))
    for k in range(10):
        x = U11_X0 + k * U11_CW
        o.append(_l(x, Y0, x, U11_Y1 + 50, GRID if 0 < k < 9 else INK, 1.2))
    o.append(_r(U11_X0, Y0, X1 - U11_X0, U11_Y1 - Y0, 'none', INK, 1.6))
    for k, (yy, mm) in enumerate(U11_MONTHS):
        x = U11_X0 + (k + 0.5) * U11_CW
        o.append(_t(x, U11_Y1 + 16, U11_MNAME[k], 17, INK, 'middle', 700)); o.append(_t(x, U11_Y1 + 37, str(yy), 15, INK, 'middle', 600))
    o.append(_l(U11_X0, U11_Y1 + 50, X1, U11_Y1 + 50, INK, 1.4))
    # paths (helper lines), then markers and day labels
    def path(pts, color, dash):
        s = ' '.join('%.1f,%.1f' % (u11x(d), u11y(r)) for d, r in pts)
        return '<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (s, color, 1.8, ' stroke-dasharray="%s"' % dash if dash else '')
    o.append(path(MAX, TEAL, '6 4')); o.append(path(LUNA, INK, None))
    for d, r in MAX:
        x, y = u11x(d), u11y(r)
        o.append(_tri(x, y + 1, 8.5)); o.append(_t(x, y - 17, d.day, 15, TEAL, 'middle', 800, halo=True))
    for d, r in LUNA:
        x, y = u11x(d), u11y(r)
        o.append(_c(x, y, 6.5)); o.append(_t(x, y - 17, d.day, 15, INK, 'middle', 800, halo=True))
    return _svg(W, H, 'Chart of the sightings of two storks, Luna and Max, by country and month, September 2022 to May 2023',
                ''.join(o))


S11 = u11_svg()
U11_INTRO = (INTRO_HEAD['chart'] + '\n'
             'The chart describes the sightings of two storks, Luna and Max, that carried tracking tags during their migration. '
             'The months from September 2022 to May 2023 are marked on the horizontal axis.\n'
             'On the vertical axis on the left are the countries in which Luna was sighted, and on the vertical axis on the right '
             'are the countries in which Max was sighted. Every sighting of Luna is marked with a circle, and every sighting of '
             'Max is marked with a triangle (see legend).\n'
             'Each circle and each triangle represents one sighting: its position on the chart shows the country and the date of '
             'the sighting, and the number above it is the day of the month on which the stork was sighted.\n'
             'Notes:\n- A stork that was sighted twice in a row in the same country did not leave that country between these sightings.\n'
             '- The lines connecting the markers are only helper lines.\n'
             'For example, on September 1, 2022, Max was sighted in Romania, and on October 9, 2022, Luna was sighted in Israel.\n'
             + NOTE)
U11T = 'Two storks on the move'

mk(11, 1, U11T, U11_INTRO, 'In which of the following months was Luna sighted in Israel and Max sighted in Jordan?',
   ['October 2022', 'December 2022', 'March 2023', 'April 2023'], 1, [
    'Luna = circles, and her countries are the labels on the LEFT. The Israel row has circles only in October 2022 (the 9th and the 19th) and in April 2023 (the 5th).',
    'Max = triangles, and his countries are the bands on the RIGHT. The Jordan band covers two rows (the Israel and the Egypt rows). '
    'It has triangles in September 2022, October 2022, December 2022 - January 2023 and March 2023.',
    'The only month in both lists is October 2022.',
    'Trap: in December and in March Max\'s triangles sit on the "Israel" row, but for Max that row belongs to Jordan, and Luna was in Egypt or Sudan then. '
    'In April Luna was in Israel, but Max was already in Romania.'], S11)
mk(11, 2, U11T, U11_INTRO, 'In which of the following countries did Max certainly stay for at least 30 days in a row?',
   ['Ethiopia only', 'Jordan only', 'Ethiopia and Jordan', 'Ethiopia and Romania'], 1, [
    'Look for a long horizontal run of triangles in one band: the stay is certain from the first sighting of the run to the last one.',
    'A column is one month, so a run of at least 30 days has to be about as wide as a whole column (or wider).',
    'Ethiopia: October 18 to November 27 (40 days) and January 12 to February 14 (33 days) - both at least 30 days.',
    'Jordan: the longest run is December 6 to January 1 - it crosses a column border but it is only 26 days. '
    'Romania: September 1-16 (15 days) and April 14 - May 8 (24 days).',
    'So only Ethiopia.'], S11)
mk(11, 3, U11T, U11_INTRO, 'In how many of the countries that Luna passed through during the period described in the chart was she sighted on four dates or more?',
   ['5', '6', '3', '4'], 4, [
    'Go over Luna\'s rows (the circles) one by one and count the circles in each row - also circles from a second visit to the same country.',
    'Kenya: 4 circles - yes. Sudan: 3 (December - January) + 2 (February - March) = 5 - yes. Egypt: 5 + 2 = 7 - clearly more than 4, no need to count exactly.',
    'Israel: 2 + 1 = 3 - no. Turkey: 2 - no. Romania: 2 in September + 2 in May = 4 - yes.',
    'In all: Kenya, Sudan, Egypt and Romania - 4 countries. (Forgetting Romania\'s second visit gives 3.)'], S11)
mk(11, 4, U11T, U11_INTRO, 'During the period described in the chart, how many times was the same stork sighted in two different countries on the same day?',
   ['1', '2', '3', '0'], 1, [
    'Two sightings of the SAME stork on the same date have the same position on the horizontal axis, but different rows: two circles (or two triangles) one exactly above the other, joined by a vertical line.',
    'There is only one such place: September 24, 2022 - Luna was sighted both in Romania and in Turkey.',
    'Careful: on December 6 and on January 12 there is a circle above a triangle, but those are two DIFFERENT storks, so they do not count.'], S11)
mk(11, 5, U11T, U11_INTRO, 'Because of stormy weather, Luna stayed in one of the countries for more than 21 days but fewer than 30 days in a row.\nWhich of the following countries was it?',
   ['Kenya', 'Sudan', 'Egypt', 'Turkey'], 2, [
    'We need a horizontal run of circles that is a little shorter than a whole column (a column = a month): more than 3 weeks, less than a month.',
    'Sudan: December 10 to January 4 - 25 days. That fits.',
    'Kenya (January 12 - February 22, 41 days) and Egypt (October 23 - December 6, 44 days) are longer than a month; '
    'Turkey (September 24 - October 6) is less than 2 weeks.'], S11)


# =====================================================================================================================
# UNIT 12 · cooking contest, five judges (book: song contest; table of points per place + cumulative-score table,
# the last judge's row hidden)
# =====================================================================================================================
PTS = {1: 12, 2: 7, 3: 3, 4: 1, 5: 0, 6: 0}
COOKS = ['Amir', 'Bella', 'Carmen', 'Dylan', 'Eva', 'Felix']
JUDGES = ['A', 'B', 'C', 'D']
RANK = {   # judge: contestants from 1st to 6th place (judge E is not shown)
    'A': ['Carmen', 'Felix', 'Bella', 'Dylan', 'Amir', 'Eva'],
    'B': ['Dylan', 'Carmen', 'Eva', 'Bella', 'Felix', 'Amir'],
    'C': ['Dylan', 'Eva', 'Felix', 'Bella', 'Amir', 'Carmen'],
    'D': ['Felix', 'Carmen', 'Dylan', 'Amir', 'Eva', 'Bella'],
}
def cum_table():
    tot, rows = {c: 0 for c in COOKS}, []
    for j in JUDGES:
        for p, c in enumerate(RANK[j], 1): tot[c] += PTS[p]
        rows.append([tot[c] for c in COOKS])
    return rows
CUM = cum_table()


def u12_svg():
    W, H = 900, 640
    o = [_t(40, 30, 'Table 1:', 20, INK, 'start', 800), _t(150, 30, 'Points awarded for each place in the ranking', 19, INK, 'start', 700)]
    x0, y0, cw, rh = 300, 55, 150, 34
    o.append(_r(x0, y0, cw, rh, SOFT, INK, 1.4)); o.append(_r(x0 + cw, y0, cw, rh, SOFT, INK, 1.4))
    o.append(_t(x0 + cw / 2, y0 + rh / 2, 'Place', 18, INK, 'middle', 700)); o.append(_t(x0 + cw * 1.5, y0 + rh / 2, 'Points', 18, INK, 'middle', 700))
    for k in range(6):
        y = y0 + rh * (k + 1)
        o.append(_r(x0, y, cw, rh, '#ffffff', INK, 1.2)); o.append(_r(x0 + cw, y, cw, rh, '#ffffff', INK, 1.2))
        o.append(_t(x0 + cw / 2, y + rh / 2, ['1st', '2nd', '3rd', '4th', '5th', '6th'][k] + ' place', 18))
        o.append(_t(x0 + cw * 1.5, y + rh / 2, PTS[k + 1], 19, INK, 'middle', 600))
    ty = 330
    o.append(_t(40, ty, 'Table 2:', 20, INK, 'start', 800)); o.append(_t(150, ty, 'Cumulative score of each contestant in the contest', 19, INK, 'start', 700))
    lx, lw, cw2, rh2, top = 40, 250, 98, 46, ty + 25
    o.append(_r(lx, top, lw, rh2, '#ffffff', 'none', 0))
    for k, c in enumerate(COOKS):
        o.append(_r(lx + lw + k * cw2, top, cw2, rh2, SOFT, INK, 1.4)); o.append(_t(lx + lw + (k + .5) * cw2, top + rh2 / 2, c, 18, INK, 'middle', 700))
    for r in range(5):
        y = top + rh2 * (r + 1)
        o.append(_r(lx, y, lw, rh2, SOFT, INK, 1.4))
        o.append(_t(lx + 12, y + rh2 / 2, 'After the ranking of judge ' + 'ABCDE'[r], 17, INK, 'start', 600))
        for k in range(6):
            o.append(_r(lx + lw + k * cw2, y, cw2, rh2, '#ffffff' if r < 4 else '#F4F6F8', INK, 1.2))
            o.append(_t(lx + lw + (k + .5) * cw2, y + rh2 / 2, CUM[r][k] if r < 4 else '?', 20, INK if r < 4 else MUTED, 'middle', 500))
    return _svg(W, H, 'Two tables: points for each place, and the cumulative score of six contestants after each of judges A to D', ''.join(o))


S12 = u12_svg()
U12_INTRO = (INTRO_HEAD['tables'] + '\n'
             'Six contestants took part in a cooking contest: Amir, Bella, Carmen, Dylan, Eva and Felix. Each contestant served a dish to '
             'the five judges of the contest (judges A, B, C, D and E). Each judge in turn (from judge A to judge E) ranked the contestants '
             'from first place to sixth place. Every place earned the contestant points (according to Table 1). Table 2 shows the '
             'cumulative score of each contestant after each of judges A-D ranked the contestants. The cumulative score after the '
             'ranking of judge E does not appear in the table.\n'
             'The final score of each contestant was the cumulative score after all five judges, A-E, ranked the contestants. '
             'The winner of the contest was the contestant who received the highest final score. If several contestants reached '
             'the same final score, and it was the highest, all of them were declared winners.\n'
             'For example: judge C ranked Felix in third place, and therefore Felix was awarded 3 points. His cumulative score rose from 7 to 10.\n'
             + NOTE)
U12T = 'Cooking contest'

mk(12, 1, U12T, U12_INTRO, 'Judge ____ and judge ____ ranked the same contestant in first place.',
   ['A ; B', 'B ; C', 'C ; D', 'A ; D'], 2, [
    'Table 2 is CUMULATIVE: what a judge gave a contestant = the score after that judge minus the score before him.',
    'First place is worth 12 points (Table 1), so look, column by column, for a jump of 12.',
    'Carmen: 0 → 12 after judge A. Dylan: 1 → 13 after judge B and 13 → 25 after judge C - two jumps of 12. Felix: 10 → 22 after judge D.',
    'So judges B and C both ranked Dylan first. Check the choices: (2).'], S12)
mk(12, 2, U12T, U12_INTRO, 'In which place did judge D rank Carmen?',
   ['in first place', 'in second place', 'in fifth place', 'in fourth place'], 2, [
    'Carmen\'s cumulative score before judge D (after judge C) was 19, and after judge D it was 26.',
    'So judge D gave her 26 − 19 = 7 points.',
    'In Table 1, 7 points = second place. (Do not read the 26 itself - it is the total of four judges.)'], S12)
mk(12, 3, U12T, U12_INTRO, 'When was it possible to know for certain, for the first time, that Amir would not win the contest?',
   ['after the ranking of judge A', 'after the ranking of judge B', 'after the ranking of judge C', 'after the ranking of judge D'], 3, [
    'Amir surely cannot win once, even if EVERY remaining judge ranks him first (12 points each), he still stays below the contestant who is leading at that moment.',
    'After judge A: Amir has 0 and four judges are left: 0 + 4 · 12 = 48 > 12 (the leader, Carmen). Still open.',
    'After judge B: Amir has 0 and three judges are left: 0 + 3 · 12 = 36 > 19 (Carmen). Still open.',
    'After judge C: Amir has 0 and two judges are left: 0 + 2 · 12 = 24 < 25 (Dylan). Even with two first places he cannot catch Dylan - he surely does not win.',
    'So the first time is after the ranking of judge C.'], S12)
mk(12, 4, U12T, U12_INTRO, 'Which contestant was certainly ranked in sixth place by judge C?',
   ['Bella', 'Carmen', 'Amir', 'It cannot be determined from the data'], 4, [
    'By Table 1, fifth place and sixth place are both worth 0 points.',
    'Judge C gave 0 points to two contestants: Amir (0 → 0) and Carmen (19 → 19). One of them was fifth and the other sixth, and the table cannot tell which.',
    'Bella went up by 1 point (4 → 5), so she was fourth.',
    'So it cannot be determined.'], S12)
mk(12, 5, U12T, U12_INTRO, 'What was the average final score of the six contestants at the end of the contest (after the ranking of judge E)?',
   [r'$15\frac{1}{3}$', r'$19\frac{1}{6}$', '23', r'$28\frac{3}{4}$'], 2, [
    'Average = (sum of all the final scores) ÷ (number of contestants). We do not know judge E\'s ranking, but we do not need it.',
    'Every judge gives out exactly the points of Table 1: 12 + 7 + 3 + 1 + 0 + 0 = 23 points.',
    r'Five judges: $5 \cdot 23 = 115$ points in all, shared by 6 contestants: $\frac{115}{6} = \frac{114}{6} + \frac{1}{6} = 19\frac{1}{6}$.',
    r'Shortcut: $\frac{115}{6}$ is a little more than $\frac{114}{6} = 19$ - only choice (2) fits. '
    r'($15\frac{1}{3}$ uses only judges A-D, 23 is one judge\'s points, and $28\frac{3}{4}$ divides by 4.)'], S12)


# =====================================================================================================================
# UNIT 13 · gift survey, three bar charts (book: desert-island item / gender / age survey)
# =====================================================================================================================
ITEMS = [('Watch', 9), ('Headphones', 4), ('Book', 6), ('Plant', 8), ('Mug', 4), ('Backpack', 7)]
GENDER = [('Men', 22), ('Women', 16)]
AGES = [('20 or under', 7), ('21-40', 15), ('41-60', 10), ('61 or over', 6)]


def _barchart(x, y, w, h, title, cats, vmax, step, bw=None, size=17):
    o = []
    o.append(_r(x + w / 2 - 95, y, 190, 34, INK, INK, 0)); o.append(_t(x + w / 2, y + 17, title, 19, '#ffffff', 'middle', 800))
    o.append(_t(x, y + 50, 'Number of people', 15, INK, 'start', 700))
    px0, py0, px1, py1 = x + 46, y + 78, x + w, y + h - 46
    sy = (py1 - py0) / float(vmax)
    for v in range(step, vmax + 1, step):
        yy = py1 - v * sy
        o.append(_l(px0, yy, px1, yy, GRID, 1.2)); o.append(_t(px0 - 8, yy, v, 16, INK, 'end', 700))
    n = len(cats); slot = (px1 - px0) / n; bw = bw or slot * 0.46
    for k, (name, v) in enumerate(cats):
        cx = px0 + (k + .5) * slot
        o.append(_r(cx - bw / 2, py1 - v * sy, bw, v * sy, SOFT, TEAL, 1.8))
        parts = name.split(' ', 1) if (' ' in name and len(name) > 8) else [name]
        for i, p in enumerate(parts): o.append(_t(cx, py1 + 16 + i * 19, p, size, INK, 'middle', 700))
    o.append(_l(px0, py1, px1, py1, INK, 2)); o.append(_l(px0, py0 - 8, px0, py1, INK, 2))
    return ''.join(o)


def u13_svg():
    W, H = 900, 760
    o = [_barchart(40, 10, 820, 380, 'Item chosen', ITEMS, 10, 1)]
    o.append(_barchart(20, 420, 480, 330, 'Age', AGES, 15, 5))
    o.append(_barchart(580, 420, 300, 330, 'Gender', GENDER, 25, 5, bw=70))
    return _svg(W, H, 'Three bar charts: number of people by item chosen, by age group and by gender', ''.join(o))


S13 = u13_svg()
U13_INTRO = (INTRO_HEAD['charts'] + '\n'
             'Maya conducted a survey that included 3 questions:\n'
             'a. Which one of the following items would you most like to receive as a gift: a watch, headphones, a book, a plant, a mug or a backpack?\n'
             'b. What is your gender?\n'
             'c. What is your age (in years)?\n'
             'The three charts summarize the answers that were received.\n'
             'For example: according to the results of the survey, 10 of the people who took part in the survey are 41 to 60 years old.\n'
             + NOTE)
U13T = 'Gift survey'

mk(13, 1, U13T, U13_INTRO, 'The women who took part in the survey chose only two of the items on the list.\nWhich two items could they have been?',
   ['a watch and a mug', 'headphones and a book', 'a plant and a mug', 'a watch and a backpack'], 4, [
    'By the Gender chart, 16 women took part. All of them chose one of the two items, so these two items together were chosen by at least 16 people '
    '(men may have chosen them too).',
    'Check the choices with the Item chosen chart: (1) watch + mug = 9 + 4 = 13 - not enough. (2) headphones + book = 4 + 6 = 10 - not enough. '
    '(3) plant + mug = 8 + 4 = 12 - not enough.',
    'Tip: three choices are out, so (4) is the answer without checking. For completeness: watch + backpack = 9 + 7 = 16 - fits.'], S13)
mk(13, 2, U13T, U13_INTRO, 'What is the greatest possible number of people who took part in the survey who chose the same item and are of the same gender and in the same age group?',
   ['6', '8', '9', '15'], 3, [
    'We want the largest group that fits in the largest bar of EACH chart at the same time, so it can be no larger than the smallest of these three bars.',
    'Largest group by item: watch - 9. Largest by age: 21-40 - 15. Largest by gender: men - 22.',
    'The overlap can be at most the smallest of them: 9 (for example, 9 men aged 21-40 who all chose a watch). So 9.'], S13)
mk(13, 3, U13T, U13_INTRO, 'Exactly 9 of the men who took part in the survey chose a book or a backpack.\nWhat percentage of the women who took part in the survey did not choose a book or a backpack?',
   ['25%', '60%', '75%', '80%'], 3, [
    'By the Item chosen chart, 6 people chose a book and 7 chose a backpack: 13 people in all. 9 of them are men, so 13 − 9 = 4 are women.',
    'There were 16 women, so 16 − 4 = 12 women did NOT choose a book or a backpack.',
    r'$\frac{12}{16} = \frac{3}{4} = 75\%$.',
    'Trap: 25% is the share of the women who DID choose a book or a backpack.'], S13)
mk(13, 4, U13T, U13_INTRO, 'The number of men who took part in the survey who are 41 or older is at least ____ and at most ____.',
   ['0 ; 16', '0 ; 22', '6 ; 16', '6 ; 22'], 1, [
    'By the Age chart, 10 people are 41-60 and 6 are 61 or over: 16 people aged 41 or older.',
    'At most: all 16 of them may be men (there are 22 men) - 16.',
    'At least: there are exactly 16 women, so all 16 people aged 41 or older may be women - then 0 of them are men.',
    'So at least 0 and at most 16.'], S13)


# =====================================================================================================================
# UNIT 14 · new lending library, three kinds of books (book: film library, drama / thriller / comedy; a grey strip for
# the stock before opening day)
# =====================================================================================================================
KINDS = ['Novels', 'Comics', 'Cookbooks']
START = {'Novels': 100, 'Comics': 80, 'Cookbooks': 70}
STOCK = {   # end of day 1..15
    'Novels':    [40, 35, 50, 20, 50, 45, 40, 30, 55, 50, 65, 60, 50, 45, 60],
    'Comics':    [55, 60, 30, 35, 65, 70, 70, 25, 60, 45, 45, 45, 55, 30, 50],
    'Cookbooks': [25, 30, 45, 45, 20, 30, 20, 60, 50, 35, 55, 40, 25, 50, 35],
}


def _mark14(kind, x, y, s=9):
    if kind == 'Novels':
        return _r(x - s, y - s, 2 * s, 2 * s, '#ffffff', INK, 2) + _c(x, y, 2, INK, INK, 0)
    if kind == 'Comics':
        return _c(x, y, s + 1, '#ffffff', INK, 2) + _c(x, y, 2, INK, INK, 0)
    return _tri(x, y + 1, s + 2, '#ffffff', INK, 2)


def u14_svg():
    W, H = 900, 620
    X0, X1, YB, YT = 175.0, 830.0, 550.0, 110.0
    def xx(d): return X0 + (X1 - X0) * (d - 0.5) / 15.0
    def yy(v): return YB - (YB - YT) * v / 100.0
    o = [_r(250, 12, 520, 40, '#ffffff', INK, 1.4)]
    for k, (kind, lab) in enumerate(zip(KINDS, ['Novels', 'Comics', 'Cookbooks'])):
        x = 280 + k * 170
        o.append(_mark14(kind, x, 32)); o.append(_t(x + 18, 33, lab, 18, INK, 'start', 600))
    o.append(_t(30, 70, 'Number of books', 17, INK, 'start', 700)); o.append(_t(30, 89, 'in the library', 17, INK, 'start', 700))
    # grey strip: before opening day
    o.append(_r(100, YT - 10, 44, YB - YT + 10, GREYBG, 'none', 0))
    for v in range(0, 101, 5):
        y = yy(v)
        o.append(_l(X0 - 12, y, X1, y, GRID, 1.2 if v % 10 == 0 else 0.8, None if v % 10 == 0 else '3 4'))
        if v % 10 == 0: o.append(_t(92, y, v, 17, INK, 'end', 700)); o.append(_l(94, y, 100, y, INK, 1.5))
    for d in range(1, 16):
        x = xx(d); o.append(_l(x, YT - 10, x, YB, GRID, 1.2))
        o.append(_t(x, YB + 20, d, 17, INK, 'middle', 700))
    o.append(_l(100, YB, X1, YB, INK, 2)); o.append(_l(100, YT - 10, 100, YB, INK, 2))
    o.append(_t(X1 + 12, YB + 14, 'End of', 15, INK, 'start', 700)); o.append(_t(X1 + 12, YB + 32, 'day', 15, INK, 'start', 700))
    o.append(_t(122, YB + 26, 'Before', 14, INK, 'middle', 700)); o.append(_t(122, YB + 43, 'opening', 14, INK, 'middle', 700))
    o.append(_t(122, YB + 60, 'day', 14, INK, 'middle', 700))
    for kind in KINDS:
        o.append(_mark14(kind, 122, yy(START[kind])))
        for d, v in enumerate(STOCK[kind], 1): o.append(_mark14(kind, xx(d), yy(v)))
    return _svg(W, H, 'Chart of the number of novels, comics and cookbooks left in a library at the end of each of its first 15 days', ''.join(o))


S14 = u14_svg()
U14_INTRO = (INTRO_HEAD['chart'] + '\n'
             'A new library that lends books opened in town. It has books of three kinds: 100 novels, 80 comics and 70 cookbooks.\n'
             'The chart describes the number of books of each kind that were left in the library at the end of each of the first 15 days '
             'of its activity (see legend).\n'
             'In addition, the chart shows the number of books of each kind that were in the library before opening day (in the grey strip).\n'
             'For example: at the end of day 4, 20 novels, 35 comics and 45 cookbooks were left in the library.\n'
             + NOTE)
U14T = 'Library lending'

mk(14, 1, U14T, U14_INTRO, 'On how many of the days described in the chart was the number of novels left in the library at the end of the day equal to the number of novels that were on loan?',
   ['0', '6', '5', '4'], 4, [
    'The library has 100 novels (grey strip). Left in the library + on loan = 100.',
    'The two numbers are equal when half of them are in the library: 50 novels left and 50 on loan.',
    'Look along the 50 line for squares (novels): days 3, 5, 10 and 13 - 4 days.'], S14)
mk(14, 2, U14T, U14_INTRO, 'Dana is the first reader to enter the library every morning. When she comes in, she checks which kind of book the library has the most of, and borrows one book of that kind.\nOn how many of the days described in the chart did Dana borrow a comic?',
   ['5', '6', '7', '8'], 3, [
    'In the morning the library has what was left at the end of the day before. So we need the days on which comics (circles) were the highest of the three shapes at the end of the day.',
    'Before opening day there are more novels (100), so on day 1 she borrows a novel. At the end of day 15 the novels are highest again, so the last day does not matter either.',
    'The circle is the highest shape at the end of days 1, 2, 5, 6, 7, 9 and 13 - 7 times, so she borrowed a comic on 7 mornings (days 2, 3, 6, 7, 8, 10 and 14).'], S14)
mk(14, 3, U14T, U14_INTRO, 'At the end of day 12, what was the ratio between the number of novels that were on loan and the number of cookbooks that were on loan?',
   ['3 : 2', '3 : 4', '4 : 3', '2 : 1'], 3, [
    'The chart shows how many books were LEFT; the question asks how many were ON LOAN. On loan = the number before opening day − the number left.',
    'At the end of day 12: 60 novels left, so 100 − 60 = 40 novels on loan. 40 cookbooks left, so 70 − 40 = 30 cookbooks on loan.',
    'Ratio 40 : 30 = 4 : 3.',
    'Trap: 60 : 40 = 3 : 2 is the ratio of the books LEFT in the library.'], S14)
mk(14, 4, U14T, U14_INTRO, 'At least how many books were returned to the library on day 7?',
   ['5', '10', '15', '0'], 4, [
    'Compare the end of day 6 with the end of day 7 for each kind.',
    'Novels: 45 → 40 (down). Comics: 70 → 70 (no change). Cookbooks: 30 → 20 (down).',
    'We can be sure that books of some kind were returned only if their number went UP. No kind went up: the comics may have stayed the same because nobody borrowed or returned one.',
    'So it is possible that no book was returned at all: at least 0.'], S14)
mk(14, 5, U14T, U14_INTRO, 'Each reader may borrow at most three books a day.\nWhat is the least possible number of readers who borrowed books on day 1?',
   ['44', '43', '40', '33'], 1, [
    'First find how many books were borrowed on day 1 (at least - books may also have been returned, which only means more were borrowed).',
    'Novels 100 → 40: 60. Comics 80 → 55: 25. Cookbooks 70 → 25: 45. In all: 60 + 25 + 45 = 130 books.',
    r'Fewest readers = each one borrows 3: $\frac{130}{3} = \frac{129}{3} + \frac{1}{3} = 43\frac{1}{3}$.',
    'There is no third of a reader: 43 readers can borrow only 129 books, so at least 44 readers.'], S14)


# =====================================================================================================================
# UNIT 15 · fruit stall, price / quantity in split cells (book: vegetable stall, 8 vegetables x 6 days)
# =====================================================================================================================
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
FRUITS = ['Apples', 'Bananas', 'Pears', 'Oranges', 'Grapes', 'Plums', 'Peaches', 'Mangoes']
FT = {   # fruit: [(price in shekels per kg, quantity sold in kg) for Sunday..Friday]
    'Apples':  [(3.70, 110), (3.90, 120), (4.10, 100), (4.50, 95), (4.40, 105), (4.00, 130)],
    'Bananas': [(2.40, 90), (2.50, 105), (2.60, 100), (2.30, 110), (2.20, 95), (2.40, 85)],
    'Pears':   [(4.20, 70), (4.00, 85), (3.80, 90), (3.60, 80), (3.50, 95), (4.00, 75)],
    'Oranges': [(3.00, 95), (3.20, 80), (3.10, 90), (2.90, 100), (3.30, 105), (3.40, 100)],
    'Grapes':  [(8.50, 120), (8.20, 150), (8.60, 90), (8.90, 100), (9.20, 70), (8.40, 85)],
    'Plums':   [(4.60, 75), (4.80, 110), (4.00, 60), (4.30, 80), (5.00, 90), (4.50, 85)],
    'Peaches': [(6.20, 50), (6.00, 65), (5.90, 45), (5.50, 60), (5.40, 70), (5.60, 55)],
    'Mangoes': [(6.80, 40), (6.40, 35), (6.10, 45), (5.90, 50), (5.60, 30), (5.80, 60)],
}
U15_OPTS = [[120, 270, 310], [120, 210, 360], [120, 270, 360], [120, 150, 90]]


def _cell(x, y, w, h, price, qty):
    return (_r(x, y, w, h, '#ffffff', INK, 1.2)
            + '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#CBD5DC"/>' % (x, y + h, x + w, y, x + w, y + h)
            + _l(x, y + h, x + w, y, MUTED, 1) + _r(x, y, w, h, 'none', INK, 1.2)
            + _t(x + 6, y + 15, '%.2f' % price, 17, INK, 'start', 500) + _t(x + w - 6, y + h - 13, qty, 17, INK, 'end', 800))


def u15_table(W=980):
    lx, lw, cw, hh, rh, top = 20, 120, 102, 40, 56, 50
    o = [_t(lx + lw + 4 * cw, 22, 'Kind of fruit', 20, INK, 'middle', 800)]
    for k, f in enumerate(FRUITS):
        o.append(_r(lx + lw + k * cw, top, cw, hh, SOFT, INK, 1.4)); o.append(_t(lx + lw + (k + .5) * cw, top + hh / 2, f, 17, INK, 'middle', 700))
    for r, d in enumerate(DAYS):
        y = top + hh + r * rh
        o.append(_r(lx, y, lw, rh, SOFT, INK, 1.4)); o.append(_t(lx + 10, y + rh / 2, d, 17, INK, 'start', 700))
        for k, f in enumerate(FRUITS):
            p, q = FT[f][r]; o.append(_cell(lx + lw + k * cw, y, cw, rh, p, q))
    ky = top + hh + 6 * rh + 22
    o.append(_t(360, ky + 34, 'Legend:', 18, INK, 'end', 800))
    kx, kw, kh = 380, 250, 70
    o.append(_r(kx, ky, kw, kh, '#ffffff', INK, 1.4))
    o.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#CBD5DC"/>' % (kx, ky + kh, kx + kw, ky, kx + kw, ky + kh))
    o.append(_l(kx, ky + kh, kx + kw, ky, MUTED, 1)); o.append(_r(kx, ky, kw, kh, 'none', INK, 1.4))
    o.append(_t(kx + 8, ky + 16, 'Price', 15, INK, 'start', 700)); o.append(_t(kx + 8, ky + 33, '(shekels per kg)', 14, INK, 'start', 500))
    o.append(_t(kx + kw - 8, ky + kh - 30, 'Quantity sold', 15, INK, 'end', 700)); o.append(_t(kx + kw - 8, ky + kh - 13, '(kg)', 14, INK, 'end', 500))
    return ''.join(o), ky + kh + 20


def u15_svg():
    body, h = u15_table()
    return _svg(980, h, 'Table of the price and the quantity sold of 8 kinds of fruit on each of six days', body)


def u15_opts_svg():
    body, h = u15_table()
    o = [body, _l(20, h, 960, h, GRID, 2), _t(490, h + 24, 'Cumulative quantity of grapes sold (kg)', 18, MUTED, 'middle', 700)]
    for k, vals in enumerate(U15_OPTS):
        px, py = 20 + (k % 2) * 480, h + 44 + (k // 2) * 300
        x0, x1, yb, yt = px + 140, px + 450, py + 240, py + 30
        sy = (yb - yt) / 400.0
        o.append(_t(px + 20, py + 18, '(%d)' % (k + 1), 24, TEAL, 'middle', 800))
        o.append(_t(px + 52, py + 70, 'Cumulative', 15, INK, 'middle', 700)); o.append(_t(px + 52, py + 88, 'quantity', 15, INK, 'middle', 700))
        o.append(_t(px + 52, py + 106, 'sold (kg)', 15, INK, 'middle', 700))
        for v in range(0, 401, 100):
            y = yb - v * sy
            if v: o.append(_l(x0, y, x1, y, GRID, 1, '4 4'))
            o.append(_t(x0 - 8, y, v, 15, INK, 'end', 600))
        slot = (x1 - x0) / 3.0
        for j, v in enumerate(vals):
            cx = x0 + (j + .5) * slot
            o.append(_r(cx - 26, yb - v * sy, 52, v * sy, SOFT, TEAL, 1.8))
            o.append(_t(cx, yb + 16, DAYS[j], 15, INK, 'middle', 700))
        o.append(_l(x0, yb, x1, yb, INK, 1.8)); o.append(_l(x0, yt - 6, x0, yb, INK, 1.8))
    return _svg(980, h + 44 + 600, 'The fruit table, followed by four bar charts of the cumulative quantity of grapes sold, labelled (1) to (4)', ''.join(o))


S15, S15o = u15_svg(), u15_opts_svg()
U15_INTRO = (INTRO_HEAD['table'] + '\n'
             'The table presents data on the sales at a fruit stall on the six working days of a certain week. For each kind of fruit, '
             'the table shows its price (in shekels per kg) and the quantity of it that was sold (in kg) on each day of that week (see legend).\n'
             'For example: on Thursday, 70 kg of peaches were sold at a price of 5.40 shekels per kg.\n'
             + NOTE)
U15T = 'Fruit stall'

mk(15, 1, U15T, U15_INTRO, 'For each of the first three days of the week, which of the following charts describes the CUMULATIVE quantity (in kg) of grapes sold from the beginning of the week until the end of that day?',
   ['(1)', '(2)', '(3)', '(4)'], 3, [
    'Cumulative = everything sold from the beginning of the week up to and including that day.',
    'Grapes: Sunday 120 kg, so the cumulative quantity at the end of Sunday is 120.',
    'Monday 150 kg: 120 + 150 = 270. Tuesday 90 kg: 270 + 90 = 360.',
    'Look for bars of 120, 270 and 360: chart (3). Chart (4) shows the daily quantities, not the cumulative ones; (1) and (2) are wrong on Tuesday or on Monday.'], S15o)
mk(15, 2, U15T, U15_INTRO, 'Which of the following statements is true?',
   ['On each day of the week, the quantity of grapes sold (in kg) was greater than the quantity of plums sold (in kg)',
    'On each day of the week, the total weight of the bananas and the oranges sold was less than 200 kg',
    'On each day of the week, the price of mangoes was higher than the price of peaches',
    'On each day of the week, the average of the prices of apples and pears was lower than 4 shekels per kg'], 3, [
    'Each statement says "on each day", so one day that breaks it is enough to rule it out.',
    '(1) On Thursday 70 kg of grapes and 90 kg of plums were sold (and on Friday 85 and 85) - false.',
    '(2) On Wednesday 110 + 100 = 210 kg (and on Thursday exactly 95 + 105 = 200, which is not less than 200) - false.',
    '(3) Mangoes against peaches, day by day: 6.80 > 6.20, 6.40 > 6.00, 6.10 > 5.90, 5.90 > 5.50, 5.60 > 5.40, 5.80 > 5.60 - true.',
    'Tip: once you find the true statement you may stop. For completeness, (4): on Wednesday (4.50 + 3.60) ÷ 2 = 4.05, and on Friday (4.00 + 4.00) ÷ 2 = 4.00 - not lower than 4.'], S15)
mk(15, 3, U15T, U15_INTRO, 'For each kind of fruit, we define its "price range" as the difference between its highest price and its lowest price (in shekels per kg) during the week.\nFor which of the following kinds of fruit is the "price range" the greatest?',
   ['Apples', 'Pears', 'Plums', 'Mangoes'], 4, [
    'Only the four fruits in the choices: for each, find the highest and the lowest price in its column.',
    '(1) Apples: 4.50 (Wednesday) − 3.70 (Sunday) = 0.80.',
    '(2) Pears: 4.20 (Sunday) − 3.50 (Thursday) = 0.70.',
    '(3) Plums: 5.00 (Thursday) − 4.00 (Tuesday) = 1.00.',
    '(4) Mangoes: 6.80 (Sunday) − 5.60 (Thursday) = 1.20 - the greatest.'], S15)
mk(15, 4, U15T, U15_INTRO, 'Which of the following amounts (in shekels) is the smallest?',
   ['The total amount paid at the stall for oranges on Monday', 'The total amount paid at the stall for mangoes on Monday',
    'The total amount paid at the stall for bananas on Tuesday', 'The total amount paid at the stall for plums on Tuesday'], 2, [
    'Total amount paid = price per kg × quantity sold (kg). Compute it for each choice.',
    r'(1) Oranges, Monday: $3.20 \cdot 80 = 256$.',
    r'(2) Mangoes, Monday: $6.40 \cdot 35 = 224$.',
    r'(3) Bananas, Tuesday: $2.60 \cdot 100 = 260$.',
    r'(4) Plums, Tuesday: $4.00 \cdot 60 = 240$.',
    'The smallest is 224 - the mangoes, although they have the highest price: very little was sold.'], S15)


# =====================================================================================================================
# verification: recompute every answer from the data; exactly one correct choice, at the book-key position
# =====================================================================================================================
def _verify():
    def one(qid, vals, good):
        hits = [k + 1 for k, v in enumerate(vals) if good(v)]
        unit, n = int(qid[3:5]), int(qid.split('-q')[1])
        assert hits == [QUESTIONS[qid]['correct'][0] + 1] == [KEY[unit][n - 1]], (qid, hits, KEY[unit][n - 1])
    for u in KEY: assert len([q for q in QUESTIONS if q.startswith('chp%02d' % u)]) == len(KEY[u]), u

    # ---- unit 11
    assert LUNA == sorted(LUNA, key=lambda p: (p[0], p[1])) and MAX == sorted(MAX, key=lambda p: p[0])
    def mon(d): return (d.year, d.month)
    def runs(seq, cf):                         # consecutive sightings in the same country: (country, first, last)
        out = []
        for d, r in seq:
            c = cf(r)
            if out and out[-1][0] == c: out[-1][2] = d
            else: out.append([c, d, d])
        return out
    MO = {'October 2022': (2022, 10), 'December 2022': (2022, 12), 'March 2023': (2023, 3), 'April 2023': (2023, 4)}
    def both(m): return (any(mon(d) == MO[m] and luna_c(r) == 'Israel' for d, r in LUNA)
                         and any(mon(d) == MO[m] and max_c(r) == 'Jordan' for d, r in MAX))
    one('chp11-q1', list(MO), both)
    long30 = {c for c, a, b in runs(MAX, max_c) if (b - a).days >= 30}
    one('chp11-q2', [{'Ethiopia'}, {'Jordan'}, {'Ethiopia', 'Jordan'}, {'Ethiopia', 'Romania'}], lambda s: s == long30)
    assert max((b - a).days for c, a, b in runs(MAX, max_c) if c == 'Jordan') >= 25    # the near-miss trap exists
    cnt = {c: sum(luna_c(r) == c for d, r in LUNA) for c in U11_ROWS}
    n4 = sum(v >= 4 for v in cnt.values())
    one('chp11-q3', [5, 6, 3, 4], lambda v: v == n4)
    assert cnt['Romania'] == 4 and len([1 for c, a, b in runs(LUNA, luna_c) if c == 'Romania']) == 2   # 2 visits trap
    same = sum(1 for seq, cf in ((LUNA, luna_c), (MAX, max_c)) for d in {p[0] for p in seq}
               if len({cf(r) for dd, r in seq if dd == d}) > 1)
    one('chp11-q4', [1, 2, 3, 0], lambda v: v == same)
    assert {d for d, r in LUNA} & {d for d, r in MAX}      # different storks on the same day (trap) exist
    fit = {c for c, a, b in runs(LUNA, luna_c) if 21 < (b - a).days < 30}
    one('chp11-q5', ['Kenya', 'Sudan', 'Egypt', 'Turkey'], lambda c: {c} == fit)
    # no marker hides another one (same row, too close)
    pts = sorted([(r, u11x(d)) for d, r in LUNA + MAX])
    for (r1, x1), (r2, x2) in zip(pts, pts[1:]):
        assert r1 != r2 or x2 - x1 > 18, (r1, x1, x2)

    # ---- unit 12
    for j in JUDGES: assert sorted(RANK[j]) == sorted(COOKS)
    assert CUM[2][COOKS.index('Felix')] - CUM[1][COOKS.index('Felix')] == 3 and CUM[1][COOKS.index('Felix')] == 7
    firsts = {j: RANK[j][0] for j in JUDGES}
    one('chp12-q1', [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')], lambda p: firsts[p[0]] == firsts[p[1]])
    gain = CUM[3][COOKS.index('Carmen')] - CUM[2][COOKS.index('Carmen')]
    place = [p for p in PTS if PTS[p] == gain]; assert len(place) == 1
    one('chp12-q2', [1, 2, 5, 4], lambda v: v == place[0])
    def out_after(k):                              # k = judges done (1..4); 5 - k judges left
        i = COOKS.index('Amir'); return CUM[k - 1][i] + 12 * (5 - k) < max(CUM[k - 1])
    first = min(k for k in range(1, 5) if out_after(k))
    one('chp12-q3', [1, 2, 3, 4], lambda v: v == first)
    zero_c = [c for c in COOKS if CUM[2][COOKS.index(c)] == CUM[1][COOKS.index(c)]]
    assert sorted(zero_c) == ['Amir', 'Carmen'] and CUM[2][1] - CUM[1][1] == 1
    one('chp12-q4', ['Bella', 'Carmen', 'Amir', 'na'], lambda v: v == ('na' if len(zero_c) > 1 else zero_c[0]))
    avg = 5 * sum(PTS.values()) / 6.0
    one('chp12-q5', [15 + 1 / 3., 19 + 1 / 6., 23, 28.75], lambda v: abs(v - avg) < 1e-9)
    assert abs(sum(CUM[3]) / 6.0 - (15 + 1 / 3.)) < 1e-9 and abs(115 / 4. - 28.75) < 1e-9

    # ---- unit 13
    it, g, a = dict(ITEMS), dict(GENDER), dict(AGES)
    assert sum(it.values()) == sum(g.values()) == sum(a.values()) == 38 and a['41-60'] == 10
    W = g['Women']
    one('chp13-q1', [('Watch', 'Mug'), ('Headphones', 'Book'), ('Plant', 'Mug'), ('Watch', 'Backpack')],
        lambda p: it[p[0]] + it[p[1]] >= W)
    one('chp13-q2', [6, 8, 9, 15], lambda v: v == min(max(it.values()), max(g.values()), max(a.values())))
    wom = it['Book'] + it['Backpack'] - 9; assert 0 <= wom <= W
    one('chp13-q3', [25, 60, 75, 80], lambda v: v * W == 100 * (W - wom))
    old = a['41-60'] + a['61 or over']
    lo, hi = max(0, old - W), min(old, g['Men'])
    one('chp13-q4', [(0, 16), (0, 22), (6, 16), (6, 22)], lambda v: v == (lo, hi))

    # ---- unit 14
    for k in KINDS:
        assert all(0 <= v <= START[k] and v % 5 == 0 for v in STOCK[k])
    assert (STOCK['Novels'][3], STOCK['Comics'][3], STOCK['Cookbooks'][3]) == (20, 35, 45)
    one('chp14-q1', [0, 6, 5, 4], lambda v: v == sum(n == START['Novels'] - n for n in STOCK['Novels']))
    def top(d):                                # kind with the most books at the end of day d (0 = before opening)
        vals = {k: (START[k] if d == 0 else STOCK[k][d - 1]) for k in KINDS}
        m = max(vals.values()); w = [k for k in vals if vals[k] == m]; assert len(w) == 1, d; return w[0]
    mornings = sum(top(d - 1) == 'Comics' for d in range(1, 16))
    assert mornings == sum(top(d) == 'Comics' for d in range(1, 16))     # both readings of "the days" agree
    one('chp14-q2', [5, 6, 7, 8], lambda v: v == mornings)
    nl, kl = START['Novels'] - STOCK['Novels'][11], START['Cookbooks'] - STOCK['Cookbooks'][11]
    one('chp14-q3', [(3, 2), (3, 4), (4, 3), (2, 1)], lambda v: v[0] * kl == v[1] * nl)
    rises = sum(max(0, STOCK[k][6] - STOCK[k][5]) for k in KINDS)
    one('chp14-q4', [5, 10, 15, 0], lambda v: v == rises)
    borrowed = sum(START[k] - STOCK[k][0] for k in KINDS)
    one('chp14-q5', [44, 43, 40, 33], lambda v: v == -(-borrowed // 3))

    # ---- unit 15
    assert FT['Peaches'][4] == (5.40, 70)
    cum, s = [], 0
    for d in range(3): s += FT['Grapes'][d][1]; cum.append(s)
    one('chp15-q1', U15_OPTS, lambda v: v == cum)
    st = [all(FT['Grapes'][d][1] > FT['Plums'][d][1] for d in range(6)),
          all(FT['Bananas'][d][1] + FT['Oranges'][d][1] < 200 for d in range(6)),
          all(FT['Mangoes'][d][0] > FT['Peaches'][d][0] for d in range(6)),
          all((FT['Apples'][d][0] + FT['Pears'][d][0]) / 2 < 4 - 1e-9 for d in range(6))]
    one('chp15-q2', st, lambda v: v)
    rng = {f: round(max(p for p, q in FT[f]) - min(p for p, q in FT[f]), 2) for f in FRUITS}
    ch = ['Apples', 'Pears', 'Plums', 'Mangoes']
    one('chp15-q3', ch, lambda f: rng[f] == max(rng[x] for x in ch) and sorted(rng[x] for x in ch)[-2] < rng[f])
    amt = [round(FT[f][d][0] * FT[f][d][1], 2) for f, d in (('Oranges', 1), ('Mangoes', 1), ('Bananas', 2), ('Plums', 2))]
    assert amt == [256, 224, 260, 240]
    one('chp15-q4', amt, lambda v: v == min(amt))
    return True


_verify()

MODULES = []
PRACTICE = {52: [q for u in (11, 12, 13, 14, 15) for q in sorted(QUESTIONS) if q.startswith('chp%02d-' % u)]}
MEMORY = []
