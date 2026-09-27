"""Topic 27 - Motion. Course review 2026-09 fixes.
See t27_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q

TOPIC = 27
L1, L2, L3, L4 = 'wp-106', 'wp-108-after', 'wp-110', 'wp-113'
SPECIAL = 'r26-t27-special'
GRAPHS = 'r26-t27-graphs'
SPECIAL_SB = ['Question %d' % n for n in (14, 15, 16, 17)]
GRAPHS_SB = ['Question %d' % n for n in (18, 19, 20)]


def VIS(svg, w=1150, h=647):
    return dict(k='vis', v={'type': 'geometry', 'svg': svg}, w=w, h=h)


def TABLE(headers, rows, w=1000, h=200):
    return dict(k='vis', v={'type': 'table', 'headers': headers, 'rows': rows}, w=w, h=h)


# ------------------------------------------------------------------------------------------------ graphs
_F = 'font-family="DejaVu Sans,Arial,sans-serif"'


def _txt(x, y, s, size=16, anchor='middle', fill='#203344', weight=None):
    w = ' font-weight="%s"' % weight if weight else ''
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle" fill="%s" %s font-size="%d"%s>%s</text>'
            % (x, y, anchor, fill, _F, size, w, s))


def _graph(series, xmax, ymax, xt, yt, grid=True, guides=(), title='Distance-time graph',
           xlabel='time (hours)', ylabel='distance (km)'):
    """Distance-time graph in the course figure style (viewBox 640 x 360).
    series = [(points, color, name, (label_x, label_y) in data units)]"""
    L, R, TP, B = 78.0, 585.0, 40.0, 300.0
    X = lambda t: L + (R - L) * t / xmax
    Y = lambda d: B - (B - TP) * d / ymax
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="%s"><title>%s</title>' % (title, title)]
    if grid:
        for t in xt: s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e1e7ee" stroke-width="1.2"/>' % (X(t), B, X(t), TP))
        for d in yt: s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e1e7ee" stroke-width="1.2"/>' % (L, Y(d), R, Y(d)))
    for (t, d) in guides:
        s.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="#9aa8b5" stroke-width="1.4" stroke-dasharray="5 4"/>'
                 % (X(t), B, X(t), Y(d), L, Y(d)))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#71818d" stroke-width="1.8"/>' % (L, B, R + 22, B))
    s.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="#71818d" stroke-width="1.8"/>' % (R + 15, B - 4, R + 22, B, R + 15, B + 4))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#71818d" stroke-width="1.8"/>' % (L, B, L, TP - 18))
    s.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="#71818d" stroke-width="1.8"/>' % (L - 4, TP - 11, L, TP - 18, L + 4, TP - 11))
    s.append(_txt(L - 14, B + 16, '0', 15))
    for t in xt:
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#71818d" stroke-width="1.5"/>' % (X(t), B - 4, X(t), B + 4))
        s.append(_txt(X(t), B + 20, ('%g' % t), 15))
    for d in yt:
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#71818d" stroke-width="1.5"/>' % (L - 4, Y(d), L + 4, Y(d)))
        s.append(_txt(L - 10, Y(d), ('%g' % d), 15, 'end'))
    s.append(_txt(R + 22, B + 46, xlabel, 16, 'end'))
    s.append(_txt(L + 10, TP - 24, ylabel, 16, 'start'))
    for pts, color, name, at in series:
        s.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/>'
                 % (' '.join('%.1f,%.1f' % (X(t), Y(d)) for t, d in pts), color))
        for t, d in pts: s.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (X(t), Y(d), color))
        if name: s.append(_txt(X(at[0]), Y(at[1]), name, 18, 'middle', color, 700))
    s.append('</svg>')
    return ''.join(s)


TEAL, ORANGE = '#087f83', '#b8661a'
# lesson: one trip - 60 km in 1 h, stop 1 h, then 100 km in 2 h
G_LESSON1 = _graph([([(0, 0), (1, 60), (2, 60), (4, 160)], TEAL, '', (0, 0))], 4.4, 175, [1, 2, 3, 4], [60, 160], grid=False,
                   guides=[(1, 60), (4, 160)], title='Distance-time graph of one trip')
# lesson: two travelers - A from P at 20 kph, B from 120 km toward P at 40 kph; they cross at (2, 40)
G_LESSON2 = _graph([([(0, 0), (4, 80)], TEAL, 'A', (4.15, 88)), ([(0, 120), (3, 0)], ORANGE, 'B', (0.35, 128))],
                   4.6, 135, [1, 2, 3, 4], [40, 80, 120], grid=True, title='Distance-time graph of two travelers')
# guided Q20: trip out and back
G_Q20 = _graph([([(0, 0), (2, 30), (3, 30), (4, 50), (6, 0)], TEAL, '', (0, 0))], 6.5, 56, [1, 2, 3, 4, 5, 6],
               [10, 20, 30, 40, 50], grid=True, title='Distance of a cyclist from her home',
               ylabel='distance from home (km)')
# practice: two cyclists, no grid
G_P19 = _graph([([(0, 0), (4, 80)], TEAL, 'A', (4.15, 90)), ([(0, 120), (3, 0)], ORANGE, 'B', (0.35, 128))],
               4.6, 135, [3, 4], [80, 120], grid=False, guides=[(4, 80)], title='Distance of two cyclists from town P',
               ylabel='distance from P (km)')
# practice: one trip with a stop
G_P20 = _graph([([(0, 0), (2, 60), (3, 60), (4, 100)], TEAL, '', (0, 0))], 4.4, 110, [1, 2, 3, 4], [20, 40, 60, 80, 100],
               grid=True, title='Distance-time graph of a car trip')


# ------------------------------------------------------------------------------------------------ helpers
def _lines(M, vid, n, fn_line):
    def fn(lines):
        for l in lines: fn_line(l)
        return lines
    M.edit_lines(vid, n, fn)


def _fix(M, vid, n, key, old, new):
    found = []
    def f(l):
        if key in l and old in l[key]:
            l[key] = l[key].replace(old, new); found.append(1)
    _lines(M, vid, n, f)
    assert found, '%s #%d: not found: %s' % (vid, n, old)


def _fix_draw(M, vid, n, old, new): _fix(M, vid, n, 'draw', old, new)
def _fix_say(M, vid, n, old, new): _fix(M, vid, n, 'say', old, new)


def _insert(M, vid, n, match, new, before=False):
    conv = lambda x: {'say': x} if isinstance(x, str) else {'draw': x[1]}
    def fn(lines):
        for k, l in enumerate(lines):
            if match in (l.get('say') or l.get('draw') or ''):
                j = k if before else k + 1
                return lines[:j] + [conv(x) for x in new] + lines[j:]
        raise AssertionError('%s #%d: not found: %s' % (vid, n, match))
    M.edit_lines(vid, n, fn)


_SPELL = [('kilometre', 'kilometer'), ('Kilometre', 'Kilometer'), ('metre', 'meter'), ('Metre', 'Meter'),
          ('memorise', 'memorize'), ('memorising', 'memorizing'), ('travelled', 'traveled'), ('towards', 'toward'), ('organise', 'organize')]


def _us(s):
    for a, b in _SPELL: s = s.replace(a, b)
    return s


def _text_fixes(M, vid):
    """American spelling everywhere; '..., so x' / '... — so x' (= therefore) -> '. So x'."""
    v = M.video(vid)
    v['title'] = _us(v['title']); v['navLabel'] = _us(v.get('navLabel', ''))
    for n, b in enumerate(v['beats'], 1):
        b['title'] = _us(b['title'])
        for it in b['items']:
            if it.get('t'): it['t'] = _us(it['t'])
        def f(l):
            for key in ('say', 'draw', 'label'):
                if key in l:
                    t = _us(l[key])
                    if key == 'say':
                        t = re.sub(r'(,| —) so ([a-z])', lambda m: '. So ' + m.group(2), t)
                    l[key] = t
        _lines(M, vid, n, f)


def _solution(M, qid, group, sb, intro, slides):
    n = M.next_question_number(TOPIC)
    label = 'Question %d' % n
    beats = [dict(mode='title', title=label, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=sb.index(label), title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, group, sb, beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = 43
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Lesson "Distance, Speed and Time" (wp-106)
    # =====================================================================================
    _fix_draw(M, L1, 3, '"t = d : v" and "v = d : t"', '"t = d ÷ v" and "v = d ÷ t"')

    # slide 4 Units: add the minutes -> fractions of an hour table
    M.set_slide(L1, 4, script=[
        "Motion questions love to mix units. Your job: work in the SAME units, always.",
        A('The unit facts appear', T('$1$ km $=1{,}000$ m · $1$ hour $=60$ minutes · $1$ minute $=60$ seconds', size=40)),
        "Kilometers per hour: how many kilometers in ONE hour.",
        "Meters per second: how many meters in ONE second.",
        A('A table appears: minutes as fractions of an hour',
          TABLE(['Minutes', '12', '15', '20', '30', '40', '45'], [['Hours', '⅕', '¼', '⅓', '½', '⅔', '¾']], w=1100, h=180)),
        "Minutes turn into fractions of an hour. Learn this row by heart.",
        D('Under the table write "20 min = 20/60 h = 1/3 h"'),
        "Why is twenty minutes a third? Twenty out of sixty. Divide both by twenty: one third.",
        "Forty minutes: two thirds. Twelve minutes: one fifth. Forty-five minutes: three quarters.",
        A("'1.25 hours = 1 hour 15 minutes' appears", T('$1.25$ hours $=1$ hour $15$ minutes', size=44)),
        D('Circle "15 minutes"'),
        "And careful with decimals of an hour. One point two five hours is one hour fifteen minutes — not twenty-five.",
    ])

    # slide 6 Draw a sketch: Pythagoras reminder (T31 comes later) + the sketch habit
    M.set_slide(L1, 6, script=[
        "Some motion questions sneak in geometry — Pythagoras.",
        "A plane climbing at an angle. One person walking north, another walking west.",
        A("'Different directions? Draw a sketch.' appears", T('Different directions? Draw a sketch.', size=46)),
        "The moment the directions differ — draw it.",
        A("'Right triangle: a² + b² = c²' appears", T('Right triangle: $a^2+b^2=c^2$ ($c$ = the side opposite the right angle)', size=40)),
        "You'll study it in geometry. For now, one line: in a right triangle, the two short sides squared add up to the long side squared.",
        "In fact, in every motion problem: draw. A dot for each starting point, an arrow for each direction, and mark the gap.",
        A("'Distance = the path actually traveled' appears", T('Distance in the formula $=$ the path actually traveled', size=42)),
        D('Underline "actually traveled"'),
        "The distance in the formula is the real path — the sloping flight path, the whole round trip.",
    ])

    # slide 7 Recap
    M.set_slide(L1, 7, script=[
        "Let's lock it in.",
        A("'distance = time × speed' appears", T('$\\text{distance}=\\text{time}\\times\\text{speed}$', size=40)),
        A("'Same units, always' appears", T('Same units, always — minutes are fractions of an hour', size=40)),
        A("'Converting? Identical ratios — not 3.6' appears", T('Converting? Identical ratios — not $3.6$', size=40)),
        A("'Two people or two parts? A table' appears", T('Two people or two parts of a trip? A distance–speed–time table', size=40)),
        A("'Always draw a sketch' appears", T('Always draw a sketch', size=40)),
        D('Tick each line'),
        "Two questions next. Then: average speed.",
    ])

    # new slide 6: the distance-speed-time table
    M.insert_slides(L1, 5, [dict(mode='concept', active=4, title='The table', script=[
        "Many motion questions have two people — or one trip in two parts. Organize them in a table.",
        A('The example appears', T('A cyclist rides $2$ hours at $15$ km per hour, then $20$ km at $10$ km per hour.', size=38)),
        A('A distance–speed–time table appears',
          TABLE(['', 'Distance', 'Speed', 'Time'], [['Part 1', '', '15 km/h', '2 h'], ['Part 2', '20 km', '10 km/h', ''],
                                                   ['Total', '', '', '']], w=1000, h=300)),
        "One row for each person, or each part of the trip. Three columns: distance, speed, time.",
        "In every row, distance equals speed times time. Know two boxes? The row gives you the third.",
        D('In row 1 fill in "15 × 2 = 30 km"'),
        "Part one: fifteen for two hours — thirty kilometers.",
        D('In row 2 fill in "20 ÷ 10 = 2 h"'),
        "Part two: twenty kilometers at ten — two hours.",
        D('In the total row fill in "50 km" and "4 h"'),
        "Totals: add the distances, add the times. Fifty kilometers in four hours.",
        "Speeds don't add up in the total row. That's the next video — average speed.",
        "Then look for the link the question gives you: equal times, equal distances, or a total. That link is your equation.",
    ])])
    M.set_sidebar(L1, ['Motion is work', 'The formula', 'Units', 'Forget 3.6', 'The table', 'Draw a sketch', 'Recap'])
    for n, a in ((7, 5), (8, 6)):
        M.slide(L1, n)['active'] = a

    # =====================================================================================
    # 2. Lesson "Average Speed" (wp-108-after)
    # =====================================================================================
    M.set_slide(L2, 1, script=[
        "Average speed.",
        "A classic trap — most students fall into it the first time.",
        "Let's understand it properly.",
    ])
    M.set_slide(L2, 4, script=[
        "And here's the big one.",
        A("'Average speed ≠ the average of the speeds' appears", T('Average speed $\\ne$ the average of the speeds', size=44)),
        D('Underline "≠"'),
        "Average speed is NOT the average of the speeds. At least, not necessarily.",
        "Go one way fast and come back slow — the SAME distance each way. The slow part takes MORE time.",
        A("'Equal distances → closer to the slower speed' appears", T('Equal distances $\\to$ closer to the slower speed', size=42)),
        "More time at the slow speed. So the average speed sits closer to the slower speed.",
        "Remember weighted averages? The bigger group pulls the average toward itself. Here, the longer time does the pulling.",
        A("'Equal times → the plain average' appears", T('Equal times $\\to$ the plain average', size=42)),
        "But if you drive the SAME time at each speed — say, one hour at sixty and one hour at ninety — the plain average is right: seventy-five.",
        "So first ask: equal distances, or equal times?",
        "Then: total distance over total time — and if the distance is missing, pick a friendly number.",
    ])
    M.set_slide(L2, 5, script=[
        "Let's lock it in.",
        A("'Total distance ÷ total time' appears", T('Average speed $=$ total distance $\\div$ total time', size=42)),
        A("'Equal times → plain average' appears", T('Equal times $\\to$ the plain average', size=42)),
        A("'Equal distances → closer to the slower speed' appears", T('Equal distances $\\to$ closer to the slower speed', size=42)),
        D('Circle "slower"'),
        "Estimate first: which side of the middle is the answer? Cross out the choices on the wrong side.",
        A("'Strong-student check: 2ab over a + b' appears", T('Equal distances, speeds $a$ and $b$: check with $\\frac{2ab}{a+b}$', size=40)),
        "A check for strong students — only for equal distances: two times a times b, over a plus b. Seventy-two and forty-eight give fifty-seven point six.",
        "One question next — then speed ratios.",
    ])

    # =====================================================================================
    # 3. Lesson "Speed Ratios" (wp-110)
    # =====================================================================================
    _fix_draw(M, L3, 3, 'Draw an arrow from "3 : 4" to "3 : 4"', 'Draw an arrow from the ratio "3 : 4" to the ratio "3 : 4"')
    _fix_draw(M, L3, 5, 'Draw a crossing arrow from "3 : 4" to "4 : 3"', 'Draw a crossing arrow from the ratio "3 : 4" to the ratio "4 : 3"')
    M.insert_slides(L3, 5, [dict(mode='concept', active=4, title='What is fixed?', script=[
        "The real skill: before you use a rule, ask — what is fixed here? Time, speed, or distance?",
        "Quick check. Four situations.",
        A("'1. Two cars leave together and drive for 3 hours' appears", T('1. Two cars leave together and drive for $3$ hours.', size=38)),
        D('Next to 1 write "time → distances follow speeds"'),
        "Same three hours for both: the time is fixed. Distances follow the speeds.",
        A("'2. Dana walks to school and runs back home' appears", T('2. Dana walks to school and runs back home.', size=38)),
        D('Next to 2 write "distance → times flip"'),
        "The same road both ways: the distance is fixed. The times flip.",
        A("'3. Two runners start together from both ends and meet' appears", T('3. Two runners start together from the two ends of a path and meet.', size=38)),
        D('Next to 3 write "time → distances follow speeds"'),
        "They start together and stop together: the time is fixed. Distances follow the speeds.",
        A("'4. A bus drives at the same speed on Monday and Tuesday' appears", T('4. A bus drives at the same speed on Monday and on Tuesday.', size=38)),
        D('Next to 4 write "speed → distances follow times"'),
        "The speed is fixed. More time, more distance.",
    ])])
    M.set_slide(L3, 7, script=[
        "The rules are easy to read. What matters: using them fast, without calculating.",
        A("'First: what is fixed?' appears", T('First ask: what is fixed?', size=44)),
        A("'Same time → distance follows speed' appears", T('Same time $\\to$ distance follows speed', size=44)),
        A("'Same speed → distance follows time' appears", T('Same speed $\\to$ distance follows time', size=44)),
        A("'Same distance → time flips' appears", T('Same distance $\\to$ time flips', size=44)),
        D('Circle "flips"'),
        "Two questions next — watch how the ratios do all the work.",
    ])
    M.set_sidebar(L3, ['No calculation', 'Same time', 'Same speed', 'Same distance', 'What is fixed?', 'Recap'])
    M.slide(L3, 7)['active'] = 5

    # =====================================================================================
    # 4. Lesson "Relative Speed" (wp-113): show the sketch habit on the board
    # =====================================================================================
    M.set_slide(L4, 5, script=[
        "Here's the classic mistake — and it's almost always in chase questions.",
        A("'The distance that matters: the gap at the start' appears", T('The distance that matters: the gap at the start', size=44)),
        D('Underline "the gap at the start"'),
        "The only distance you care about is the gap between them at the start.",
        "Not the whole way they travel. Not where they end up. Just that starting gap.",
        "One of them leaves earlier? First work out that head start — that's your gap.",
        A('A sketch appears: the chaser and the leader, 2 km apart',
          dict(k='vis', v={'type': 'route', 'labels': ['Chaser', 'Leader'], 'positions': [0, 2], 'arrows': ['→', '→']}, w=1000, h=210)),
        "Sketch it every time. A dot for each one, an arrow for each direction.",
        D('Between the dots write "gap = 2 km"'),
        "And mark the gap. Here the chaser starts two kilometers behind — that's the distance to close.",
    ])

    # =====================================================================================
    # 5. Existing solution videos
    # =====================================================================================
    _fix_draw(M, 'solve-wp27-g108', 2, 'with ":30" beside it', 'with "÷30" beside it')
    _fix_say(M, 'solve-wp27-g108', 2, "Don't know that triple? Thirteen squared minus twelve squared: twenty-five. Root: five.",
             "Don't know that triple? Pythagoras: thirteen squared minus twelve squared — one sixty-nine minus one forty-four, twenty-five. Root: five.")

    _fix_draw(M, 'solve-wp27-g109', 2, '288 : 5 = 57.6', '288 ÷ 5 = 57.6')
    M.edit_lines('solve-wp27-g109', 2, lambda ls: ls + [
        {'draw': 'Write "2 × 72 × 48 ÷ (72 + 48) = 57.6"'},
        {'say': "A check for strong students, for equal distances only: two times seventy-two times forty-eight, over one hundred twenty. Fifty-seven point six again."}])

    _fix_draw(M, 'solve-wp27-g111', 2, 'Write "1 : 1.75 = 4 : 7"', 'Write the ratio "1 : 1.75 = 4 : 7"')
    _fix_draw(M, 'solve-wp27-g112', 2, 'Write "1 : 3.5 = 2 : 7"', 'Write the ratio "1 : 3.5 = 2 : 7"')

    _fix_draw(M, 'solve-wp27-g114', 2, '0.8 : 12 = 1/15 hour', '0.8 ÷ 12 = 1/15 hour')
    _fix_draw(M, 'solve-wp27-g114', 2, '60 : 15 = 4 minutes', '60 ÷ 15 = 4 minutes')

    _fix_draw(M, 'solve-wp27-g115', 2, '"8:00–8:30: 60 × ½ = 30 km"', '"first ½ hour: 60 × ½ = 30 km"')
    _fix_draw(M, 'solve-wp27-g115', 2, '75 : 150 = ½ hour', '75 ÷ 150 = ½ hour')

    _fix_draw(M, 'solve-wp27-g116', 2, '1 : ⅔ = 1.5', '1 ÷ ⅔ = 1 × 3/2 = 1.5')
    _fix_say(M, 'solve-wp27-g116', 2, 'One divided by two thirds: one and a half.',
             'One divided by two thirds. Dividing by a fraction is multiplying by its reciprocal: one times three halves — one and a half.')
    _fix_draw(M, 'solve-wp27-g116', 3, '3 : ⅔ = 4.5', '3 ÷ ⅔ = 3 × 3/2 = 4.5')

    _fix_draw(M, 'solve-wp27-g117', 2, '9 : ⅕ = 45', '9 ÷ ⅕ = 9 × 5 = 45')
    _fix_say(M, 'solve-wp27-g117', 2, 'Multiply by the reciprocal — forty-five.',
             'Dividing by a fraction is multiplying by its reciprocal: nine times five — forty-five.')
    _fix_draw(M, 'solve-wp27-g117', 2, '12 : 9/60 = 12 × 60/9 = 80', '12 ÷ 9/60 = 12 × 60/9 = 80')

    _fix_draw(M, 'solve-wp27-g118', 2, '180 : 12 = 15 m/s', '180 ÷ 12 = 15 m/s')

    _fix_draw(M, 'solve-wp27-g119', 2, 'Write "2x/24 = ⅓ + x/18"', 'Write "2x/24 = x/12  →  x/12 = ⅓ + x/18"')
    _fix_say(M, 'solve-wp27-g119', 2, 'Clear the denominators: three x equals twelve plus two x. x is twelve.',
             "Two x over twenty-four is x over twelve. Multiply everything by thirty-six — the smallest number that twelve, three and eighteen all go into. Three x equals twelve plus two x. x is twelve.")
    _fix_draw(M, 'solve-wp27-g119', 3, '24 : 24 = 1 h', '24 ÷ 24 = 1 h')
    _fix_draw(M, 'solve-wp27-g119', 3, '20 min + 12 : 18 h', '20 min + 12/18 h')
    _fix_say(M, 'solve-wp27-g119', 3, "Not luck. The exam checks whether you know what to plug in first — the round, friendly numbers.",
             "Not luck. Start with the round, friendly choice. Working back from the answers saves time in many motion questions.")

    _fix_draw(M, 'solve-wp27-g120', 2, '1,350 : 9 = 150', '1,350 ÷ 9 = 150')
    _fix_draw(M, 'solve-wp27-g120', 2, '1,350 : 270 = 5', '1,350 ÷ 270 = 5')
    _fix_draw(M, 'solve-wp27-g120', 3, '9 : 1.8 = 90 : 18 = 5', '9 ÷ 1.8 = 90 ÷ 18 = 5')
    M.set_slide('solve-wp27-g120', 4, script=[
        "Now the quick estimate. If it were twice as fast — half the time: four and a half hours.",
        D('Cross out choice 1'),
        "But it's not quite twice as fast. It takes MORE than four and a half. Out.",
        D('Cross out choice 3'),
        "And a faster train taking more than nine hours? Sixteen point two — out.",
        "Six or five? Try one more easy speed: one and a half times as fast.",
        D('Write "9 ÷ 1.5 = 6 hours"'),
        "One and a half times as fast: nine divided by one point five — six hours.",
        D('Write "1.5 < 1.8 < 2  →  4.5 < time < 6"'),
        "One point eight is faster than one point five. So the time is LESS than six hours — and more than four and a half.",
        D('Cross out choice 2 and circle choice 4'),
        "Six is out. Only five is left. Choice four — and no exact division at all.",
    ])

    # Q13: relative speed first, the equation only as a check
    track = dict(M.slide('solve-wp27-g121', 2)['items'][1])
    M.set_slide('solve-wp27-g121', 2, title='Method 1 · Relative speed', script=[
        "First — what do 'consecutive meetings' mean?",
        A('The track appears: 600 m, speeds 30 and 24 km/h', track),
        "They start together. The faster one pulls away — then chases the slower one from behind.",
        "It meets the slower one again exactly when it has gained one full lap.",
        D('Circle "1 extra lap"'),
        "Same direction — a chase. Subtract the speeds.",
        D('Write "30 − 24 = 6 km/h"'),
        "Tell the slow one: you stand still. The fast one moves at the difference — six kilometers an hour.",
        D('Write "6 km — 60 min" and below it "0.6 km — 6 min"'),
        "One lap: six hundred meters, zero point six kilometers. Six kilometers take sixty minutes. Divide both by ten: zero point six kilometers in six minutes.",
        D('Circle choice 2'),
        "Six minutes. Choice two.",
    ])
    M.set_slide('solve-wp27-g121', 3, title='Method 2 · Check with an equation', script=[
        "Want to check? Write an equation.",
        "Same time t for both. The fast one covers one extra lap: zero point six kilometers.",
        D('Write "30t = 24t + 0.6"'),
        "Thirty t equals twenty-four t plus zero point six.",
        D('Write "6t = 0.6 → t = 0.1 h = 6 min"'),
        "Six t is zero point six. t is a tenth of an hour: six minutes. The same answer.",
        "On a circle, imagine one of them standing still — the other just needs one lap.",
    ])

    # =====================================================================================
    # 6. Guided questions Q1-Q13: text (TeX, no ":" for division, numbers in every solution)
    # =====================================================================================
    S('wp27-g107', stem='A small cart moves at 4 meters per second. How many kilometers does it travel in 25 minutes?', expl=[
        'In $1$ second the cart covers $4$ meters. In $1$ minute ($60$ seconds) it covers $4\\times60=240$ meters.',
        'In $25$ minutes: $240\\times25=6{,}000$ meters $=6$ km.',
        'Trap: $4\\times25=100$ mixes seconds with minutes.'])
    S('wp27-g108', stem='A drone climbs along a straight line at 390 kph. After 2 minutes, its horizontal distance from its starting point is 12 kilometers. How high above its starting level is it, in kilometers?', expl=[
        '$2$ minutes $=\\frac{2}{60}=\\frac1{30}$ hour. The drone flies $390\\times\\frac1{30}=13$ km along its sloping path.',
        'Sketch a right triangle: the ground ($12$ km) and the height are the two short sides. The path ($13$ km) is the long side.',
        'Pythagoras: $h^2=13^2-12^2=169-144=25$. Therefore $h=5$ km.',
        'Trap: $13$ is the length of the path, not the height.'])
    S('wp27-g109', stem='A shuttle travels from a station to a hotel at 72 kph and returns along the same route at 48 kph, without stopping. What is its average speed for the whole round trip?', expl=[
        'Estimate first: the plain average is $\\frac{72+48}2=60$. The slow part takes more time. Therefore the answer is below $60$: choices (1) and (3) are out.',
        'Choose a distance that both speeds divide: $144$ km each way. There: $\\frac{144}{72}=2$ hours. Back: $\\frac{144}{48}=3$ hours.',
        'Average speed $=\\frac{\\text{total distance}}{\\text{total time}}=\\frac{288}{5}=57.6$ kph.',
        'Check (equal distances only): $\\frac{2\\cdot72\\cdot48}{72+48}=\\frac{6{,}912}{120}=57.6$.'])
    S('wp27-g111', stem='Noor and Eli start at the same time from opposite ends of a path and walk toward each other. Eli walks at 1.75 times Noor\u2019s speed. What fraction of the path does Noor cover before they meet?', expl=[
        'They start together and stop at the meeting: equal times. With equal times, the distances have the same ratio as the speeds.',
        'Speed ratio Noor : Eli $=1:1.75=4:7$ (multiply by $4$).',
        'The path is $4+7=11$ parts. Noor covers $\\frac4{11}$ of it.',
        'Check by elimination: Eli is faster, therefore Noor covers less than $\\frac12$. If Eli were twice as fast, Noor would cover $\\frac13$. Eli is slower than that, therefore Noor covers more than $\\frac13$. Only $\\frac4{11}$ fits.'])
    S('wp27-g112', expl=[
        'Equal times: from the start until B arrives. Speed ratio A : B $=1:3.5=2:7$. Therefore in that time the ratio of their distances is also $2:7$.',
        'The whole canal is B’s $7$ parts, because B travels the full length alone. A covers $\\frac27$ of the canal.',
        'Trap: $\\frac29$ adds $2+7$, as in a meeting question. Here they do not meet at the end.'])
    S('wp27-g114', expl=[
        'Opposite directions: the gap grows at $5+7=12$ kph.',
        'Same units: $800$ m $=0.8$ km.',
        'Time $=\\frac{0.8}{12}=\\frac1{15}$ hour $=\\frac{60}{15}=4$ minutes.'])
    S('wp27-g115', expl=[
        'From 08:00 to 08:30 only the van moves: $60\\times\\frac12=30$ km.',
        'When the car starts, the gap is $105-30=75$ km. They drive toward each other: the gap closes at $60+90=150$ kph.',
        'Time $=\\frac{75}{150}=\\frac12$ hour. They meet half an hour after the car starts, at 09:00.',
        'Trap: $\\frac{105}{150}=0.7$ hour $=42$ minutes after 08:00 (choice 1) counts the car as driving before it left.'])
    S('wp27-g116', expl=[
        '$20$ minutes $=\\frac13$ hour. Mina’s head start: $3\\times\\frac13=1$ km.',
        'Owen closes the $1$ km gap in $40$ minutes $=\\frac23$ hour. The gap closes at $1\\div\\frac23=1\\times\\frac32=1.5$ kph. This is the difference between the speeds.',
        'Owen’s speed $=3+1.5=4.5$ kph.',
        'Check: Mina walks $20+40=60$ minutes in total, $3$ km. Owen walks the same $3$ km in $\\frac23$ hour: $3\\div\\frac23=4.5$ kph.'])
    S('wp27-g117', expl=[
        'A: $60$ minutes is $5$ times $12$ minutes. In an hour A covers $9\\times5=45$ km: $45$ kph.',
        'B: $12$ km in $9$ minutes is $4$ km in $3$ minutes. An hour is $20$ times $3$ minutes: $4\\times20=80$ kph.',
        'Difference: $80-45=35$ kph.'])
    S('wp27-g118', stem='A cable car normally travels along a cable 180 meters long in 12 seconds, at a constant speed. On one trip, it travels the first half of the cable at twice its normal speed and the second half at half its normal speed. How many seconds does this trip take?', expl=[
        'At the normal speed, each half takes $\\frac{12}2=6$ seconds.',
        'First half at twice the speed: half the time, $3$ seconds. Second half at half the speed: twice the time, $12$ seconds.',
        'Total: $3+12=15$ seconds.',
        'Trap: "double, then half — they cancel" gives $12$. The two speeds apply to equal distances, not to equal times. The slow half adds $6$ seconds, and the fast half saves only $3$.'])
    S('wp27-g119', expl=[
        'Let each half be $x$ km. Then AC $=2x$.',
        'First cyclist: $\\frac{2x}{24}=\\frac{x}{12}$ hours. Second cyclist: $20$ minutes $=\\frac13$ hour, plus $\\frac{x}{18}$ hours.',
        'Equal times: $\\frac{x}{12}=\\frac13+\\frac{x}{18}$. Multiply by $36$, the smallest number that $12$, $3$ and $18$ divide: $3x=12+2x$. Therefore $x=12$.',
        'AC $=2x=24$ km. Check: $\\frac{24}{24}=1$ hour, and $\\frac13+\\frac{12}{18}=\\frac13+\\frac23=1$ hour.',
        'Faster: work back from the answers. Start with a friendly one, like $24$.'])
    S('wp27-g120', stem='A train covers a route of 1,350 kilometers in 9 hours. A new train travels 80% faster. How many hours does the new train take on the same route?', expl=[
        '80% faster: the new speed is $1.8$ times the old speed.',
        'Same distance: the time is divided by $1.8$. $9\\div1.8=\\frac{90}{18}=5$ hours.',
        'Estimate: twice as fast would take $\\frac92=4.5$ hours. One and a half times as fast would take $9\\div1.5=6$ hours. $1.8$ is between $1.5$ and $2$. Therefore the time is between $4.5$ and $6$ hours: only $5$ fits.',
        'Trap: 80% faster does not mean 80% less time. The time is multiplied by $\\frac1{1.8}=\\frac59$.'])
    S('wp27-g121', expl=[
        'Same direction on a circle: the faster cyclist gains on the slower one at $30-24=6$ kph.',
        'They meet again each time the faster one has gained one full lap: $600$ m $=0.6$ km.',
        'Time $=\\frac{0.6}{6}=0.1$ hour $=6$ minutes.',
        'Check with an equation: $30t=24t+0.6$. Therefore $6t=0.6$ and $t=0.1$ hour.'])

    # =====================================================================================
    # 7. Practice: text
    # =====================================================================================
    S('wp27-p01', stem='A cyclist completes one lap every 2 minutes at speed A, and three laps every 8 minutes at speed B. She rides for 24 minutes at each speed. How many laps does she complete in total?', expl=[
        'At speed A: $\\frac{24}{2}=12$ laps.',
        'At speed B: $24$ minutes are $\\frac{24}{8}=3$ blocks of $8$ minutes, with $3$ laps in each: $3\\times3=9$ laps.',
        'Total: $12+9=21$ laps.'])
    S('wp27-p02', stem='A ferry travels $d$ kilometers in $t$ hours. At three times that speed, how many kilometers does it travel in $2t$ hours?', expl=[
        'Speed $=\\frac{d}{t}$. Three times that speed: $\\frac{3d}{t}$.',
        'Distance $=\\frac{3d}{t}\\cdot2t=6d$.',
        'Or plug in numbers: $d=10$, $t=1$. The speed is $10$, the new speed $30$, and in $2$ hours the ferry travels $60=6\\cdot10$.'])
    S('wp27-p03', stem='A robot travels for $x$ hours at $2x$ kph, and then for $y$ hours at $3y$ kph. What is its total distance, in kilometers?', expl=[
        'First part: $x\\cdot2x=2x^2$. Second part: $y\\cdot3y=3y^2$. Total: $2x^2+3y^2$.',
        'Or plug in numbers: $x=2$, $y=1$. The robot travels $2\\cdot4=8$ km and then $1\\cdot3=3$ km: $11$ km. Only $2x^2+3y^2=8+3=11$ fits (the others give $49$, $7$ and $15$).',
        'Do not choose $x=1$ and $y=1$: then two choices both give $5$.'])
    S('wp27-p04', stem='A bus travels from A to B at 64 kph for 3 hours. The route from B to C is 48 km longer than the route from A to B. How many hours does the trip from B to C take at 80 kph?', expl=[
        'A to B: $64\\times3=192$ km.',
        'B to C: $192+48=240$ km.',
        'Time: $\\frac{240}{80}=3$ hours.'])
    S('wp27-p05', expl=[
        '$1$ hour $20$ minutes $=80$ minutes.',
        'Same distance: the times flip. The speed ratio is $72:48=3:2$, therefore the ratio of the times is $2:3$.',
        'Return time: $80\\times\\frac32=120$ minutes $=2$ hours.'])
    S('wp27-p06', expl=[
        'Same distance: the time is divided by $1.6$.',
        '$4\\div1.6=\\frac{40}{16}=2.5$ hours $=2$ hours $30$ minutes.',
        'Trap: $2.5$ hours is not $2$ hours $50$ minutes, and $2$ hours $24$ minutes is $2.4$ hours.'])
    S('wp27-p07', stem='A fast cyclist chases a slower cyclist along a straight road. The slow cyclist rides at 12 kph, and the fast cyclist at 30 kph. At the start, the gap between them is 9 km. How long does it take the fast cyclist to catch up?', expl=[
        'A chase: the gap closes at $30-12=18$ kph.',
        'Time $=\\frac{9}{18}=\\frac12$ hour $=30$ minutes.'])
    S('wp27-p08', expl=[
        'From 08:00 to 11:00 is $3$ hours. The route: $4\\times3=12$ km.',
        'At $6$ kph: $\\frac{12}{6}=2$ hours.',
        'The second walker leaves $2$ hours before 11:00, at 09:00.'])
    S('wp27-p09', stem='A van travels 360 km. It covers the first 120 km at 60 kph, then one quarter of the remaining distance at 120 kph, and the rest at 30 kph. How many hours does the whole trip take?', expl=[
        'First part: $\\frac{120}{60}=2$ hours.',
        'Remaining: $360-120=240$ km. One quarter of it: $\\frac{240}{4}=60$ km at $120$ kph, $\\frac{60}{120}=0.5$ hour.',
        'The rest: $240-60=180$ km at $30$ kph, $\\frac{180}{30}=6$ hours.',
        'Total: $2+0.5+6=8.5$ hours.'])
    S('wp27-p10', stem='Two runners leave the same point on a circular track at the same time and run in opposite directions. One runs five times as fast as the other. What fraction of the track has the slower runner covered when they meet for the first time?',
      choices=['$\\frac18$', '$\\frac15$', '$\\frac14$', '$\\frac16$'], correct=4, expl=[
        'Opposite directions on a circle: at the first meeting, together they have covered exactly one lap.',
        'Equal times: the distances follow the speed ratio $1:5$. The lap is $1+5=6$ parts.',
        'The slower runner covers $1$ part: $\\frac16$ of the track.',
        'Trap: $\\frac15$ compares the two runners, not the slower runner with the whole lap.'])
    S('wp27-p11', stem='Two buses start together and travel the same route of 180 km. Bus A is 15 kph faster than bus B. How much earlier does bus A arrive?', expl=[
        'Plug in two pairs of speeds that differ by $15$ kph.',
        'Speeds $45$ and $30$: times $\\frac{180}{45}=4$ and $\\frac{180}{30}=6$ hours. A arrives $2$ hours earlier.',
        'Speeds $90$ and $75$: times $\\frac{180}{90}=2$ and $\\frac{180}{75}=2.4$ hours. A arrives $0.4$ hour $=24$ minutes earlier.',
        'Two different answers: it cannot be determined.'])
    S('wp27-p12', expl=[
        'Morning: $1.8$ km $=1{,}800$ m at $60$ m per minute: $\\frac{1{,}800}{60}=30$ minutes.',
        'Evening speed: $\\frac{60}{2}=30$ m per minute. $2{,}400$ m take $\\frac{2{,}400}{30}=80$ minutes.',
        'Total: $30+80=110$ minutes.'])
    S('wp27-p13', expl=[
        '$200{,}000{,}000=2\\times10^8$.',
        'Distance $=2\\times10^8\\cdot3\\times10^{-9}=6\\times10^{-1}=0.6$ meter.'])
    S('wp27-p15', stem='Two vans leave the same place together and drive along the same road. One drives at 90 kph, the other at 60 kph. When the faster van has driven 180 km, it stops for 1.5 hours. How many hours after they leave does the slower van reach the stopped van?', expl=[
        'The faster van reaches $180$ km after $\\frac{180}{90}=2$ hours. It stays there until $2+1.5=3.5$ hours.',
        'The slower van reaches $180$ km after $\\frac{180}{60}=3$ hours.',
        '$3$ hours is before $3.5$ hours: the faster van is still stopped. The answer is $3$ hours.'])
    S('wp27-p16', stem='A road from A to B is 140 km long. At 08:00 a car leaves A toward B. At 09:00 another car leaves B toward A at the same speed. They meet 30 km from B. What is their common speed, in kph?', expl=[
        'The second car drives $30$ km. The first drives $140-30=110$ km.',
        'Same speed, but the first car drove $1$ hour longer. That extra hour gave it $110-30=80$ km more.',
        'Therefore the speed is $80$ kph.',
        'Or work back from the answers: at $80$ kph, the first car drives $80$ km by 09:00. The gap is $60$ km, closed at $160$ kph in $\\frac{60}{160}=\\frac38$ hour. The second car drives $80\\times\\frac38=30$ km. It fits.'])
    S('wp27-p17', stem='A car travels a distance $D$ in 4 hours. It covers half of the distance at speed $v$ and the other half at speed $3v$. How many hours would the whole distance take at speed $v$?', expl=[
        'Let $T$ be the time for the whole distance at speed $v$. The first half, at speed $v$, takes $\\frac{T}{2}$.',
        'The second half at three times the speed takes a third of that: $\\frac{T}{6}$.',
        '$\\frac{T}{2}+\\frac{T}{6}=\\frac{3T+T}{6}=\\frac{2T}{3}=4$. Therefore $T=6$ hours.',
        'Or work back from the answers: $T=6$ gives $3+1=4$ hours.'])
    S('wp27-p18', expl=[
        '$18$ kph means $18{,}000$ m in $60$ minutes: $\\frac{18{,}000}{60}=300$ m per minute.',
        'Each jump: $\\frac{300}{40}=7.5$ m.'])
    S('wp27-p19', stem='Two runners start together from the same point of a circular track 500 meters long. They run in opposite directions at the same speed, and each runs exactly 3,750 meters. How many times do they meet after the start? (Count a meeting at the finish, if there is one.)', expl=[
        'Opposite directions: they meet each time their total distance grows by one lap, $500$ m.',
        'Together they run $2\\times3{,}750=7{,}500$ m. $\\frac{7{,}500}{500}=15$ meetings.',
        'The $15$th meeting happens exactly at the finish, and it counts: $15$.'])
    S('wp27-p20', expl=[
        'The first walker walks from 10:00 to 10:45: $\\frac34$ hour. Distance: $6\\times\\frac34=4.5$ km, half of the road.',
        'The second walker also covers $4.5$ km, at $9$ kph: $\\frac{4.5}{9}=\\frac12$ hour $=30$ minutes.',
        'The second walker started $30$ minutes before 10:45, at 10:15: $15$ minutes after the first.'])
    S('wp27-p24', stem='A boat moves at 15 kph in still water. The speed of the river’s current is 3 kph. How many hours does a trip of 72 km downstream take?', expl=[
        'Downstream, the current helps: $15+3=18$ kph.',
        'Time $=\\frac{72}{18}=4$ hours.',
        'Trap: $\\frac{72}{15}=4.8$ ignores the current, and $\\frac{72}{12}=6$ is the time upstream.'])
    S('wp27-p25', stem='A train 180 meters long passes a post in 12 seconds, at a constant speed. How many seconds does it take to pass completely through a tunnel 270 meters long?', expl=[
        'Passing a post, the train moves its own length. Speed $=\\frac{180}{12}=15$ m per second.',
        'Through the tunnel, from the moment the front enters until the back leaves, the train moves $270+180=450$ m.',
        'Time $=\\frac{450}{15}=30$ seconds.',
        'Trap: $\\frac{270}{15}=18$ forgets the length of the train.'])
    S('wp27-p26', stem='A cyclist leaves at 07:00 at 16 kph. Another cyclist leaves the same place at 07:30 at 24 kph, along the same road. At what time does the second cyclist catch up with the first?', expl=[
        'Head start: $\\frac12$ hour at $16$ kph $=8$ km.',
        'The gap closes at $24-16=8$ kph: $\\frac{8}{8}=1$ hour after 07:30.',
        'They meet at 08:30.'])
    S('wp27-p27', stem='A driver covers the first half of a journey in 2 hours and the second half in 3 hours. The whole journey is 240 km. By how many kph is the speed in the first half greater than the speed in the second half?', expl=[
        'Each half: $\\frac{240}{2}=120$ km.',
        'First half: $\\frac{120}{2}=60$ kph. Second half: $\\frac{120}{3}=40$ kph.',
        'Difference: $60-40=20$ kph.'])

    # near-duplicates / one-step repeats
    for qid in ['wp27-p14', 'wp27-p21', 'wp27-p22', 'wp27-p23']:
        M.unplace(qid)

    # =====================================================================================
    # 8. Memory card "Motion — rules to know" (basics)
    # =====================================================================================
    c = M.card('mem-motion')
    c['intro'] = 'Motion is a work problem where the work is distance.'
    c['tables'] = [
        {'title': 'The formula', 'head': ['Want', 'Do', 'Example'], 'rows': [
            ['Distance', 'time × speed', '$18\\times2=36$ km'],
            ['Time', 'distance ÷ speed', '$\\frac{0.8}{12}=\\frac1{15}$ hour'],
            ['Speed', 'distance ÷ time', '$\\frac{288}{5}=57.6$ kph']]},
        {'title': 'Units', 'head': ['Fact', 'Note'], 'rows': [
            ['$1$ km $=1{,}000$ m', 'work in ONE set of units'],
            ['$1$ hour $=60$ min, $1$ min $=60$ s', '$1.25$ hours $=1$ h $15$ min'],
            ['Converting a speed', 'identical ratios (×60, ×30 …) — no need for 3.6']]},
        {'title': 'Minutes as parts of an hour', 'head': ['Minutes', '12', '15', '20', '30', '40', '45'], 'rows': [
            ['Hours', '$\\frac15$', '$\\frac14$', '$\\frac13$', '$\\frac12$', '$\\frac23$', '$\\frac34$']]},
        {'title': 'Ratios — first ask: what is fixed?', 'head': ['Fixed', 'Relationship', 'Example'], 'rows': [
            ['Same time', 'distance follows speed (direct)', 'speeds $3:4\\to$ distances $3:4$'],
            ['Same speed', 'distance follows time (direct)', 'more time, more distance'],
            ['Same distance', 'time flips (inverse)', 'speeds $3:4\\to$ times $4:3$']]},
        {'title': 'Average speed', 'head': ['Case', 'Rule', 'Example'], 'rows': [
            ['Always', 'total distance ÷ total time', '$\\frac{288}{5}=57.6$ kph'],
            ['Equal times', 'the plain average', '$1$ h at $60$, $1$ h at $90\\to75$'],
            ['Equal distances', 'closer to the slower speed; check $\\frac{2ab}{a+b}$', '$72$ and $48\\to57.6$']]},
        {'title': 'Relative speed', 'head': ['Situation', 'Speed of the gap'], 'rows': [
            ['Toward each other / moving apart', 'add the speeds'],
            ['Same direction (a chase)', 'subtract the speeds'],
            ['Circular track, same direction', 'subtract; they meet each time the faster one gains one lap'],
            ['Circular track, opposite directions', 'add; they meet each time together they cover one lap']]}]
    c['tips'] = [
        'Two people or two parts of a trip? Make a distance–speed–time table: one row each.',
        'In a chase, the only distance that matters is the gap at the start.',
        'Always draw a sketch: a dot for each starting point, an arrow for each direction, and the gap.',
        'Estimate first: which side of the middle is the answer? Cross out the rest.',
        'Work back from the answers: start with a friendly one.']

    # =====================================================================================
    # 9. New lesson video: special cases (trains, current, circular track, meeting twice)
    # =====================================================================================
    sb = ['Train length', 'Two trains', 'Current', 'Circular track', 'Meeting twice', 'Recap']
    M.new_video(SPECIAL, TOPIC, 'Special Motion Cases', sb, [
        dict(mode='title', title='Special Motion Cases', script=[
            "Special cases.",
            "Trains that have a length. Boats on a river. Circular tracks. And two walkers who meet twice.",
            "Each one has one idea. Learn it once — and these questions become easy.",
        ]),
        dict(mode='concept', active=0, title='Train length', script=[
            "Until now, every body was a dot. A train is not a dot — it has a length.",
            A("'Past a post: distance = the train' appears", T('Past a post (or a person): distance $=$ the train', size=42)),
            "Passing a post starts when the front reaches the post. It ends when the back passes it.",
            "In that time, the train moves exactly its own length.",
            A("'Through a tunnel: distance = tunnel + train' appears", T('Through a tunnel (or over a bridge): distance $=$ tunnel $+$ train', size=42)),
            D('Draw the tunnel; draw the train with its front at the entrance, and again with its back at the exit'),
            "Through a tunnel: from the moment the front enters, until the back leaves.",
            "The front travels the whole tunnel — and then one more train length, until the back gets out.",
            A('The example appears', T('Train $200$ m, tunnel $400$ m, speed $20$ m per second', size=42)),
            D('Write "(400 + 200) ÷ 20 = 30 seconds"'),
            "Four hundred plus two hundred: six hundred meters. At twenty meters per second: thirty seconds.",
        ]),
        dict(mode='concept', active=1, title='Two trains', script=[
            "Two trains pass each other. Now both have a length.",
            A("'Two trains passing: distance = both lengths' appears", T('Two trains pass each other: distance $=$ the sum of the lengths', size=42)),
            "From the moment the fronts meet until the backs separate, the gap covers both lengths.",
            A("'Speed = relative speed' appears", T('Speed $=$ relative speed: toward each other add, same direction subtract', size=40)),
            "And the speed? The relative speed — the rule you already know. Toward each other: add. One overtakes the other: subtract.",
            A('The example appears', T('Trains $150$ m and $250$ m, toward each other at $15$ and $25$ m per second', size=40)),
            D('Write "(150 + 250) ÷ (15 + 25) = 400 ÷ 40 = 10 seconds"'),
            "Four hundred meters, closing at forty meters per second: ten seconds.",
        ]),
        dict(mode='concept', active=2, title='Current', script=[
            "A boat on a river. The water moves too.",
            A("'Downstream: boat + current' appears", T('Downstream (with the current): boat $+$ current', size=42)),
            A("'Upstream: boat − current' appears", T('Upstream (against the current): boat $-$ current', size=42)),
            "With the current — downstream — the river pushes you: add. Against it — upstream — subtract.",
            "A plane with the wind? The same. A tailwind adds, a headwind subtracts.",
            "The favorite exam question gives both trips and asks for the current.",
            A("'Current = half the difference' appears", T('Current $=\\frac{\\text{downstream}-\\text{upstream}}{2}$', size=46)),
            "Why half? Downstream minus upstream is the current twice: once added, once taken away.",
            D('Write "downstream 20, upstream 12 → current (20 − 12) ÷ 2 = 4, boat (20 + 12) ÷ 2 = 16"'),
            "Downstream twenty, upstream twelve. The current: eight, halved — four. The boat in still water: the average — sixteen.",
        ]),
        dict(mode='concept', active=3, title='Circular track', script=[
            "A circular track. Two runners start together from the same point.",
            A("'Same direction: subtract — meet each time the faster gains one lap' appears",
              T('Same direction: subtract the speeds — they meet each time the faster one gains one lap', size=38)),
            "Same direction — a chase. They meet each time the faster one gains one full lap on the slower one.",
            A("'Opposite directions: add — meet each time together they cover one lap' appears",
              T('Opposite directions: add the speeds — they meet each time together they cover one lap', size=38)),
            "Opposite directions — they run toward each other around the circle. They meet each time their TOTAL distance grows by one lap.",
            A('The example appears', T('Track $400$ m, speeds $3$ and $5$ m per second', size=42)),
            D('Write "same direction: 400 ÷ (5 − 3) = 200 s;  opposite: 400 ÷ (5 + 3) = 50 s"'),
            "Same direction: four hundred over two — a meeting every two hundred seconds. Opposite directions: four hundred over eight — every fifty seconds.",
        ]),
        dict(mode='concept', active=4, title='Meeting twice', script=[
            "The hardest classic. Two walkers start at the same time from the two ends of a road and walk toward each other.",
            "They meet. Each one continues to the far end, turns back at once — and they meet again.",
            D('Draw the road; mark the first meeting, both ends, and the second meeting'),
            A("'First meeting: together 1 road length' appears", T('First meeting: together they walk $1$ road length', size=42)),
            "Until the first meeting, together they walk one road length.",
            A("'Second meeting: together 3 road lengths' appears", T('Second meeting: together they walk $3$ road lengths', size=42)),
            "Then each one walks to the far end — together, one more length. Then they walk toward each other and meet — one more. Three in total.",
            "Constant speeds: three lengths together take three times as long.",
            D('Write "1st meeting after 1 hour → 2nd meeting after 3 hours"'),
            "First meeting after one hour? The second is after three hours — and each walker has walked three times as far as at the first meeting.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            "Let's lock it in.",
            A("'Train past a post: its own length' appears", T('Train past a post: its own length', size=36)),
            A("'Tunnel: tunnel + train' appears", T('Through a tunnel: tunnel $+$ train', size=36)),
            A("'Two trains: both lengths, relative speed' appears", T('Two trains: both lengths, at the relative speed', size=36)),
            A("'River: add or subtract; current = half the difference' appears", T('River: down $=$ boat $+$ current, up $=$ boat $-$ current; current $=$ half the difference', size=36)),
            A("'Circle: one lap per meeting' appears", T('Circle: one lap per meeting — same direction subtract, opposite add', size=36)),
            A("'Meeting twice: 3 lengths' appears", T('Meeting twice: together $3$ road lengths, $3$ times the time', size=36)),
            D('Tick each line'),
            "Four questions next. Try each one first — then watch.",
        ]),
    ], 'wp27-advanced', after='solve-wp27-g121')

    # ---- guided Q14: train over a bridge
    g1 = 'q-r26-t27-01'
    M.new_q(g1, TOPIC, 'A train 300 meters long travels at a constant speed. It passes a signal post in 15 seconds. How many seconds does it take to cross a bridge 500 meters long completely?',
            ['$25$', '$40$', '$10$', '$55$'], 2, [
        'Passing a post, the train moves its own length: speed $=\\frac{300}{15}=20$ m per second.',
        'Crossing the bridge completely (from the moment the front gets on until the back gets off), the front moves the bridge plus the train: $500+300=800$ m.',
        'Time $=\\frac{800}{20}=40$ seconds.',
        'Trap: $\\frac{500}{20}=25$ forgets the length of the train.'])
    M.place_q(g1, 'wp27-advanced', after=SPECIAL)
    _solution(M, g1, 'Special Motion Cases', SPECIAL_SB, ["Question fourteen.", "A train with a length."], [
        ('Post, then bridge', [
            "First the speed. Passing a post, the train moves its own length.",
            D('Write "300 ÷ 15 = 20 m/s"'),
            "Three hundred meters in fifteen seconds: twenty meters per second.",
            D('Draw the bridge; the train with its front at the start, and again with its back at the end'),
            "Now the bridge. From the moment the front gets on, until the back gets off.",
            D('Write "500 + 300 = 800 m"'),
            "The front travels the bridge — and then one more train length. Eight hundred meters.",
            D('Write "800 ÷ 20 = 40 seconds" and circle choice 2'),
            "Eight hundred over twenty: forty seconds. Choice two.",
            "Twenty-five is the trap. It forgets the train's own length.",
        ]),
    ])

    # ---- guided Q15: current from two trips
    g2 = 'q-r26-t27-02'
    M.new_q(g2, TOPIC, 'A boat travels 48 km downstream in 2 hours. The return trip upstream, along the same route, takes 3 hours. The boat’s speed in still water does not change. What is the speed of the current, in kph?',
            ['$8$', '$20$', '$4$', '$2$'], 3, [
        'Downstream speed: $\\frac{48}{2}=24$ kph. Upstream speed: $\\frac{48}{3}=16$ kph.',
        'Boat $b$, current $c$:\n$\\begin{cases} b+c=24 \\\\ b-c=16 \\end{cases}$',
        'Subtract the equations: $2c=8$. Therefore $c=4$ kph (and $b=20$ kph).',
        'Shortcut: current $=\\frac{24-16}{2}=4$. Trap: $8$ is the difference before halving, and $20$ is the speed of the boat.'])
    M.place_q(g2, 'wp27-advanced', after='solve-' + g1)
    _solution(M, g2, 'Special Motion Cases', SPECIAL_SB, ["Question fifteen.", "Downstream, upstream — find the current."], [
        ('Two speeds, then half the difference', [
            "First, the two speeds.",
            D('Write "downstream: 48 ÷ 2 = 24 kph,  upstream: 48 ÷ 3 = 16 kph"'),
            "Downstream: forty-eight in two hours — twenty-four. Upstream: forty-eight in three hours — sixteen.",
            A('The two equations appear', T('$\\begin{cases} b+c=24 \\\\ b-c=16 \\end{cases}$', size=46)),
            "Boat plus current is twenty-four. Boat minus current is sixteen.",
            D('Write "2c = 8 → c = 4" and circle choice 3'),
            "Subtract the equations: two c equals eight. The current is four. Choice three.",
            "Eight is the trap — it forgets to halve. And twenty? That's the boat, not the current.",
        ]),
        ('Check', [
            "Quick check. Boat twenty, current four.",
            D('Write "20 + 4 = 24: 48 ÷ 24 = 2 h ✓   20 − 4 = 16: 48 ÷ 16 = 3 h ✓"'),
            "Downstream twenty-four: two hours. Upstream sixteen: three hours. Both fit.",
        ]),
    ])

    # ---- guided Q16: circular track, opposite directions
    g3 = 'q-r26-t27-03'
    M.new_q(g3, TOPIC, 'Two cyclists start together from the same point of a circular track 1.2 km long and ride in opposite directions. Their speeds are 20 kph and 16 kph. After how many minutes do they meet for the first time?',
            ['$18$', '$3.6$', '$2$', '$4.5$'], 3, [
        'Opposite directions: they meet when together they have covered one lap, $1.2$ km.',
        'Together they cover $20+16=36$ km per hour.',
        'Time $=\\frac{1.2}{36}=\\frac{1}{30}$ hour $=\\frac{60}{30}=2$ minutes.',
        'Trap: $\\frac{1.2}{20-16}=0.3$ hour $=18$ minutes is the answer for the same direction.'])
    M.place_q(g3, 'wp27-advanced', after='solve-' + g2)
    _solution(M, g3, 'Special Motion Cases', SPECIAL_SB, ["Question sixteen.", "A circular track — opposite directions."], [
        ('Opposite directions: add', [
            "Opposite directions on a circle. They ride toward each other around the track.",
            "They meet when together they have covered one full lap.",
            D('Write "20 + 16 = 36 kph"'),
            "Add the speeds: thirty-six kilometers per hour.",
            D('Write "36 km — 60 min" and below it "1.2 km — 2 min", with "÷30" beside it'),
            "Thirty-six kilometers take sixty minutes. Divide both by thirty: one point two kilometers in two minutes.",
            D('Circle choice 3'),
            "Two minutes. Choice three.",
            "Eighteen is the trap — that's the same-direction answer, with the difference of the speeds.",
        ]),
    ])

    # ---- guided Q17: meeting twice
    g4 = 'q-r26-t27-04'
    M.new_q(g4, TOPIC, 'Two walkers start at the same time from the two ends, A and B, of a straight road and walk toward each other at constant speeds. They meet for the first time 4 km from A. Each walker continues to the far end and turns back at once. They meet for the second time 2 km from B. How long is the road, in km?',
            ['$6$', '$10$', '$12$', '$14$'], 2, [
        'Until the first meeting, together they walk $1$ road length. Until the second meeting, together they walk $3$ road lengths: one to meet, one more to reach the far ends, and one more to meet again.',
        'Constant speeds: $3$ times the distance together takes $3$ times the time. The walker from A walks $3\\times4=12$ km.',
        'Those $12$ km are the whole road plus $2$ km back from B: $L+2=12$. Therefore $L=10$ km.',
        'Check: at the first meeting they have walked $4$ and $6$ km. By the second meeting, $12=10+2$ and $18=10+8$. Both are $2$ km from B.'])
    M.place_q(g4, 'wp27-advanced', after='solve-' + g3)
    _solution(M, g4, 'Special Motion Cases', SPECIAL_SB, ["Question seventeen.", "They meet — and meet again."], [
        ('Count the road lengths', [
            D('Draw the road A to B; mark the first meeting 4 km from A and the second meeting 2 km from B'),
            "Draw it first. The first meeting: four kilometers from A. The second: two kilometers from B.",
            "Until the first meeting, together they walk one road length. The walker from A walks four of it.",
            "Until the second meeting, together they walk three road lengths.",
            "Three times the distance together — three times the time. So each one walks three times as far.",
            D('Write "walker from A: 4 × 3 = 12 km"'),
            "The walker from A: three times four, twelve kilometers.",
            D('Write "12 = L + 2 → L = 10" and circle choice 2'),
            "Twelve kilometers: the whole road to B, then two kilometers back. The road is ten kilometers. Choice two.",
        ]),
        ('Check', [
            "Check with ten.",
            D('Write "1st meeting: 4 and 6 km"'),
            "First meeting: the walker from A walked four, the other one six.",
            D('Write "2nd meeting: 12 = 10 + 2 and 18 = 10 + 8"'),
            "By the second meeting: twelve — ten to B and two back. And eighteen — ten to A and eight back. Eight from A is two from B. It fits.",
            "Six, twelve and fourteen are traps: adding the numbers, forgetting the road, or adding two instead of taking it back.",
        ]),
    ])

    # =====================================================================================
    # 10. New lesson video: percents, letters, graphs
    # =====================================================================================
    sb = ['Speed % → time %', 'Answers in letters', 'Distance–time graphs', 'Two travelers', 'Recap']
    M.new_video(GRAPHS, TOPIC, 'Percents, Letters and Graphs', sb, [
        dict(mode='title', title='Percents, Letters and Graphs', script=[
            "Three exam favorites.",
            "Speed changes by a percent. Answers written with letters. And distance–time graphs.",
        ]),
        dict(mode='concept', active=0, title='Speed % → time %', script=[
            "A classic trap: the speed goes up by some percent. By what percent does the time go down?",
            "Same distance — speed and time are inverse. Just like rate and time in work problems.",
            A('A table appears: speed change and time change',
              TABLE(['Speed', 'Speed ×', 'Time ×', 'Time'], [['+25%', '5/4', '4/5', '−20%'], ['+50%', '3/2', '2/3', '−33⅓%'],
                                                         ['+100%', '2', '1/2', '−50%'], ['−20%', '4/5', '5/4', '+25%']], w=1000, h=380)),
            "The method: write the new speed as a fraction of the old one. Flip it. That's the time.",
            D('Circle the row "+25% → −20%"'),
            "Twenty-five percent faster: speed times five quarters. Time times four fifths — twenty percent LESS. Not twenty-five!",
            "Fifty percent faster: times three halves. Time times two thirds — thirty-three and a third percent less.",
            "Twice as fast: half the time.",
            "And slower by twenty percent — times four fifths — takes twenty-five percent MORE time.",
        ]),
        dict(mode='concept', active=1, title='Answers in letters', script=[
            "Some questions give only letters — and the choices are expressions.",
            A('The question appears', T('A car travels $d$ km in $t$ hours. How many km does it travel in $m$ minutes?', size=40)),
            A('The four choices appear', T('(1) $\\frac{md}{60t}$ (2) $\\frac{60md}{t}$ (3) $\\frac{mt}{60d}$ (4) $\\frac{60d}{mt}$', size=44)),
            "The strong-student method: plug in numbers for the letters.",
            "Step one: choose easy numbers. Not zero or one — they hide the differences between the choices.",
            D('Write "d = 120, t = 2, m = 30"'),
            "A hundred twenty kilometers in two hours: sixty kilometers an hour. In thirty minutes — half an hour — thirty kilometers.",
            D('Write "target: 30"'),
            "Step two: put the same numbers into every choice. Only one should give thirty.",
            D('Write "(1) 3,600 ÷ 120 = 30 ✓  (2) 108,000  (3) 1/120  (4) 120" and circle choice 1'),
            "Choice one gives thirty. The others don't. Choice one.",
            "Two choices give the target? Try other numbers on those two.",
        ]),
        dict(mode='concept', active=2, title='Distance–time graphs', script=[
            "Sometimes the exam gives a graph: time across, distance up.",
            A('A distance–time graph appears', VIS(G_LESSON1)),
            "Three things to read.",
            "One: the steepness is the speed — how much the distance grows in one hour.",
            D('On the first part write "60 ÷ 1 = 60 kph"'),
            "First part: sixty kilometers in one hour. Sixty kilometers per hour.",
            "Two: a flat line. Time goes on, but the distance doesn't change. The car is standing still.",
            D('On the flat part write "stop"'),
            D('On the last part write "(160 − 60) ÷ 2 = 50 kph"'),
            "Three: the last part. From sixty to a hundred sixty — a hundred kilometers in two hours. Fifty. Less steep, slower.",
            D('Write "average: 160 ÷ 4 = 40 kph"'),
            "The average speed? Total distance over total time — the stop counts too. A hundred sixty over four: forty.",
        ]),
        dict(mode='concept', active=3, title='Two travelers', script=[
            "Two lines on one graph: two travelers.",
            A('A graph with two travelers appears', VIS(G_LESSON2)),
            "A starts at zero and moves away. B starts a hundred twenty kilometers away and comes back toward zero.",
            "A line going DOWN is not slower. It means: moving back toward the starting point.",
            D('Circle the point where the lines cross and write "meeting"'),
            "Where the lines cross, they are at the same place at the same time. They meet.",
            D('Write "A: 80 ÷ 4 = 20 kph,  B: 120 ÷ 3 = 40 kph"'),
            "Can't read the crossing exactly? Calculate. A: twenty kilometers per hour. B: forty.",
            D('Write "120 ÷ (20 + 40) = 2 h → 20 × 2 = 40 km"'),
            "Toward each other — add: sixty. A hundred twenty over sixty: two hours. They meet forty kilometers from the start.",
        ]),
        dict(mode='concept', active=4, title='Recap', script=[
            "Let's lock it in.",
            A("'Speed × fraction → time × the flipped fraction' appears", T('Speed $\\times\\frac54$ $\\to$ time $\\times\\frac45$: $+25\\%$ speed $=-20\\%$ time', size=38)),
            A("'Letters: plug in easy numbers' appears", T('Letters in the choices: plug in easy numbers (not $0$ or $1$)', size=38)),
            A("'Graph: steep = fast, flat = stop' appears", T('Graph: steepness $=$ speed, flat $=$ stop', size=38)),
            A("'Lines cross = meeting' appears", T('Two lines cross $=$ a meeting', size=38)),
            D('Tick each line'),
            "Three questions next.",
        ]),
    ], 'wp27-advanced', after='solve-' + g4)

    # ---- guided Q18: percent speed -> time
    g5 = 'q-r26-t27-05'
    M.new_q(g5, TOPIC, 'A cyclist rides from home to work at a constant speed. If she rode 25% faster, the trip would take 12 minutes less. How many minutes does the trip take at her usual speed?',
            ['$36$', '$48$', '$60$', '$72$'], 3, [
        '25% faster: the speed is multiplied by $\\frac54$. Same distance: the time is multiplied by $\\frac45$. That is 20% less time.',
        '20% of the usual time is $12$ minutes: $\\frac15T=12$. Therefore $T=60$ minutes.',
        'Check: $60\\times\\frac45=48$ minutes, which is $12$ minutes less.',
        'Trap: $12\\div0.25=48$ assumes that the time drops by 25%. And $48$ is the new time, not the usual time.'])
    M.place_q(g5, 'wp27-advanced', after=GRAPHS)
    _solution(M, g5, 'Percents, Letters and Graphs', GRAPHS_SB, ["Question eighteen.", "Faster by a percent — how much time is saved?"], [
        ('Flip the fraction', [
            "Twenty-five percent faster: the speed is times five quarters.",
            D('Write "speed × 5/4 → time × 4/5"'),
            "Same route. The time is multiplied by four fifths — twenty percent less time.",
            D('Write "20% of T = 12 min → T = 60 min"'),
            "Those twenty percent are the twelve minutes saved. One fifth of the trip is twelve minutes. The whole trip: sixty.",
            D('Circle choice 3'),
            "Choice three.",
            "Forty-eight is the trap. It thinks the time drops by twenty-five percent. And forty-eight is also the NEW time — read what they ask.",
        ]),
        ('Check with numbers', [
            "Check sixty. Say she rides sixty kilometers at sixty kilometers per hour: sixty minutes.",
            D('Write "60 × 5/4 = 75 kph → 60 ÷ 75 = 4/5 h = 48 min"'),
            "Twenty-five percent faster: seventy-five. Sixty over seventy-five: four fifths of an hour — forty-eight minutes.",
            "Sixty minus forty-eight: twelve minutes less. It fits.",
        ]),
    ])

    # ---- guided Q19: answers in letters
    g6 = 'q-r26-t27-06'
    M.new_q(g6, TOPIC, 'A car travels $d$ kilometers in $t$ hours. At the same speed, how many minutes does it take to travel $k$ kilometers?',
            ['$\\frac{kt}{60d}$', '$\\frac{60d}{kt}$', '$\\frac{60kt}{d}$', '$\\frac{kd}{60t}$'], 3, [
        'Plug in numbers: $d=40$, $t=2$, $k=10$. The speed is $\\frac{40}{2}=20$ kph. $10$ km take $\\frac{10}{20}=\\frac12$ hour $=30$ minutes. The target is $30$.',
        'The choices: (1) $\\frac{10\\cdot2}{60\\cdot40}=\\frac1{120}$, (2) $\\frac{60\\cdot40}{10\\cdot2}=120$, (3) $\\frac{60\\cdot10\\cdot2}{40}=30$, (4) $\\frac{10\\cdot40}{60\\cdot2}=\\frac{10}{3}$. Only (3) gives $30$.',
        'With algebra: speed $=\\frac{d}{t}$. Time $=k\\div\\frac{d}{t}=\\frac{kt}{d}$ hours $=\\frac{60kt}{d}$ minutes.',
        'Avoid a speed of $60$ kph when you plug in: then choices (3) and (4) give the same number.'])
    M.place_q(g6, 'wp27-advanced', after='solve-' + g5)
    _solution(M, g6, 'Percents, Letters and Graphs', GRAPHS_SB, ["Question nineteen.", "Letters in the question, letters in the answers."], [
        ('Method 1 · Plug in numbers', [
            "Plug in easy numbers. Not zero, not one.",
            D('Write "d = 40, t = 2, k = 10"'),
            "Forty kilometers in two hours: twenty kilometers per hour.",
            D('Write "10 ÷ 20 = ½ h = 30 min → target 30"'),
            "Ten kilometers at twenty: half an hour. They ask for minutes — thirty.",
            D('Next to each choice write its value: "1/120", "120", "30", "10/3"'),
            "Now every choice with the same numbers. One: tiny. Two: a hundred twenty. Three: sixty times ten times two, over forty — thirty. Four: ten thirds.",
            D('Circle choice 3'),
            "Only choice three gives thirty. Choice three.",
            "One warning: don't pick a speed of sixty here. Then choices three and four both give the target.",
        ]),
        ('Method 2 · Algebra', [
            "The algebra, for a check.",
            D('Write "speed = d/t → time = k ÷ (d/t) = kt/d hours"'),
            "Speed: d over t. Time: k divided by d over t. Multiply by the reciprocal: k t over d hours.",
            D('Write "× 60 → 60kt/d minutes"'),
            "Hours to minutes: times sixty. Sixty k t over d. The same choice.",
        ]),
    ])

    # ---- guided Q20: reading a distance-time graph
    g7 = 'q-r26-t27-07'
    M.new_q(g7, TOPIC, 'The graph shows a cyclist’s distance from her home during a trip. What was her speed, in kph, during the part of the trip in which she rode fastest?',
            ['$15$', '$20$', '$25$', '$30$'], 3, [
        'Read each part. Speed $=$ the change in distance $\\div$ the time.',
        'From $0$ to $2$ hours: $\\frac{30}{2}=15$ kph. From $2$ to $3$ hours: the line is flat, she stops. From $3$ to $4$ hours: $\\frac{50-30}{1}=20$ kph.',
        'From $4$ to $6$ hours: she rides back home, from $50$ km to $0$: $\\frac{50}{2}=25$ kph.',
        'The fastest part is the ride back: $25$ kph. Trap: a line going down is not slower — it means riding back toward home.'],
            figure=G_Q20)
    M.place_q(g7, 'wp27-advanced', after='solve-' + g6)
    _solution(M, g7, 'Percents, Letters and Graphs', GRAPHS_SB, ["Question twenty.", "A graph — read every part."], [
        ('Read each part', [
            "Speed is how much the distance changes in one hour. Read each part.",
            D('On the first part write "30 ÷ 2 = 15"'),
            "First part: thirty kilometers in two hours. Fifteen.",
            D('On the flat part write "stop"'),
            "Then flat: she stops for an hour.",
            D('On the third part write "20 ÷ 1 = 20"'),
            "Then from thirty to fifty in one hour: twenty.",
            D('On the last part write "50 ÷ 2 = 25"'),
            "Last part: the line goes down — from fifty kilometers to zero. She rides back home. Fifty kilometers in two hours: twenty-five.",
            D('Circle choice 3'),
            "The fastest part: twenty-five kilometers per hour. Choice three.",
            "The trap is choice two. A line going down is not slower. The steepness is the speed, up or down.",
        ]),
    ])

    # ---- memory card for the new methods
    M.new_card('mem-r26-t27-special', TOPIC, 'wp27-advanced', {
        'title': 'Motion — special cases',
        'intro': 'Trains, rivers, circular tracks, meeting twice, percents, letters and graphs.',
        'tables': [
            {'title': 'Special cases', 'head': ['Situation', 'Distance', 'Speed'], 'rows': [
                ['Train passes a post or a person', 'the train’s length', 'the train’s speed'],
                ['Train passes through a tunnel or over a bridge', 'tunnel $+$ train', 'the train’s speed'],
                ['Two trains pass each other', 'the sum of the lengths', 'relative speed (add or subtract)'],
                ['Boat downstream / upstream', '—', 'boat $+$ current / boat $-$ current'],
                ['Both trips given', '—', 'current $=\\frac{\\text{down}-\\text{up}}{2}$, boat $=\\frac{\\text{down}+\\text{up}}{2}$'],
                ['Circle, same direction', '$1$ lap per meeting', 'difference of the speeds'],
                ['Circle, opposite directions', '$1$ lap per meeting', 'sum of the speeds'],
                ['Two walkers meet, go on to the ends, meet again', 'together $3$ road lengths', '$3$ times the time of the first meeting']]},
            {'title': 'Speed % → time % (same distance)', 'head': ['Speed', 'Time'], 'rows': [
                ['$+25\\%$ ($\\times\\frac54$)', '$-20\\%$ ($\\times\\frac45$)'],
                ['$+50\\%$ ($\\times\\frac32$)', '$-33\\frac13\\%$ ($\\times\\frac23$)'],
                ['$+100\\%$ ($\\times2$)', '$-50\\%$ ($\\times\\frac12$)'],
                ['$-20\\%$ ($\\times\\frac45$)', '$+25\\%$ ($\\times\\frac54$)']]},
            {'title': 'Distance–time graphs', 'head': ['You see', 'It means'], 'rows': [
                ['A steeper line', 'a higher speed (steepness $=$ speed)'],
                ['A flat line', 'a stop'],
                ['A line going down', 'moving back toward the starting point'],
                ['Two lines cross', 'a meeting']]}],
        'tips': [
            'Letters in the choices? Plug in easy numbers (not $0$ or $1$), find the target, and test every choice.',
            'If two choices give the target, try other numbers on those two.',
            'Speed changes by a percent? Write it as a fraction, flip it, and read the change of the time.']},
        after='solve-' + g7)

    # =====================================================================================
    # 11. New practice questions (exam level)
    # =====================================================================================
    P = {}
    P['08'] = ('Two trains, 120 meters and 180 meters long, travel toward each other on parallel tracks, at 20 and 30 meters per second. From the moment their fronts meet, how many seconds pass until their backs separate?',
               ['$30$', '$15$', '$6$', '$2.4$'], 3, [
        'The distance: the sum of the lengths, $120+180=300$ m.',
        'Toward each other: the relative speed is $20+30=50$ m per second.',
        'Time $=\\frac{300}{50}=6$ seconds.'], None)
    P['09'] = ('A train passes a man standing on a platform in 10 seconds. At the same speed, it takes the train 25 seconds to pass a platform 300 meters long completely. How long is the train, in meters?',
               ['$120$', '$200$', '$300$', '$500$'], 2, [
        'Let the train be $L$ meters long, at speed $v$ meters per second.',
        'Passing the man: $L=10v$. Passing the platform: $L+300=25v$.',
        'Subtract: the extra $300$ m take $25-10=15$ seconds. Therefore $v=\\frac{300}{15}=20$ m per second.',
        '$L=10\\times20=200$ m. Check: $\\frac{300+200}{20}=25$ seconds.'], None)
    P['10'] = ('A plane flies 1,200 km with the wind in 2 hours. It returns along the same route, against the same wind, in 3 hours. What is the plane’s speed in still air, in kph?',
               ['$100$', '$480$', '$500$', '$400$'], 3, [
        'With the wind: $\\frac{1{,}200}{2}=600$ kph. Against it: $\\frac{1{,}200}{3}=400$ kph.',
        'Plane $=\\frac{600+400}{2}=500$ kph (and the wind $=\\frac{600-400}{2}=100$ kph).',
        'Trap: $\\frac{2{,}400}{5}=480$ is the average speed of the round trip, not the speed in still air.'], None)
    P['11'] = ('A boat’s speed in still water is 4 times the speed of the current. A trip of 30 km downstream takes 2 hours. How many hours does the same trip take upstream?',
               ['$1.2$', '$2.5$', '$3\\frac13$', '$4$'], 3, [
        'Let the current be $c$. The boat is $4c$. Downstream: $4c+c=5c$. Upstream: $4c-c=3c$.',
        'Downstream: $\\frac{30}{2}=15$ kph $=5c$. Therefore $c=3$, and upstream the speed is $3c=9$ kph.',
        'Upstream time: $\\frac{30}{9}=3\\frac13$ hours.',
        'Or with ratios: same distance, speed ratio $5:3$, therefore the times are in the ratio $3:5$: $2\\times\\frac53=3\\frac13$.'], None)
    P['12'] = ('Two runners start together from the same point of a circular track. If they run in opposite directions, they meet for the first time after 40 seconds. If they run in the same direction, the faster runner first catches the slower one after 200 seconds. What is the ratio of their speeds (faster : slower)?',
               ['$5:1$', '$3:2$', '$4:3$', '$2:1$'], 2, [
        'Let the lap be $L$ and the speeds $a>b$.',
        'Opposite directions (one lap together): $a+b=\\frac{L}{40}$. Same direction (one lap gained): $a-b=\\frac{L}{200}$.',
        'Therefore $a+b=5(a-b)$. Then $6b=4a$, and the ratio is $a:b=3:2$.',
        'Check with $a=3$, $b=2$ and $L=200$: $\\frac{200}{5}=40$ and $\\frac{200}{1}=200$ seconds.',
        'Trap: $5:1$ is the ratio of the two times, not of the speeds.'], None)
    P['13'] = ('Two cars start at the same time from towns A and B and drive toward each other at constant speeds. They first meet 60 km from A. Each car continues to the other town and turns back at once. They meet for the second time 20 km from A. How far apart are the towns, in km?',
               ['$80$', '$100$', '$160$', '$180$'], 2, [
        'Until the second meeting, together they drive $3$ times the distance between the towns. The car from A drives $3\\times60=180$ km.',
        'The car from A drives to B ($L$) and then back toward A, and stops $20$ km from A: $L+(L-20)=180$.',
        'Therefore $2L=200$ and $L=100$ km.',
        'Check: at the first meeting the cars drove $60$ and $40$ km. By the second: $180=100+80$ and $120=100+20$. Both are $20$ km from A.'], None)
    P['14'] = ('Two walkers start at the same time from the two ends of a path and walk toward each other at constant speeds. They meet for the first time after 20 minutes. Each walker continues to the far end and turns back at once. How many minutes after the start do they meet for the second time?',
               ['$40$', '$60$', '$80$', '$30$'], 2, [
        'Until the first meeting, together they walk $1$ path length: $20$ minutes.',
        'Until the second meeting, together they walk $3$ path lengths.',
        'Constant speeds: $3\\times20=60$ minutes.'], None)
    P['15'] = ('A driver usually drives to work in 30 minutes. How many minutes would the trip take if she drove 50% faster?',
               ['$15$', '$20$', '$22.5$', '$45$'], 2, [
        '50% faster: the speed is multiplied by $\\frac32$.',
        'Same distance: the time is multiplied by $\\frac23$. $30\\times\\frac23=20$ minutes.',
        'Trap: $15$ assumes that the time drops by 50%.'], None)
    P['16'] = ('A train reduced its speed by 20%. By what percent did the time of its trip along the same route increase?',
               ['16%', '20%', '25%', '80%'], 3, [
        'Speed down by 20%: the speed is multiplied by $\\frac45$.',
        'Same distance: the time is multiplied by $\\frac54=1.25$. The time increased by 25%.',
        'Check: $100$ km at $100$ kph take $1$ hour. At $80$ kph they take $\\frac{100}{80}=1.25$ hours.'], None)
    P['17'] = ('A runner runs $x$ meters in $y$ seconds. At the same speed, how many kilometers does she run in $z$ minutes?',
               ['$\\frac{60xz}{y}$', '$\\frac{3xz}{50y}$', '$\\frac{xz}{60y}$', '$\\frac{50y}{3xz}$'], 2, [
        'Plug in numbers: $x=10$, $y=2$, $z=10$. The speed is $5$ m per second, $300$ m per minute. In $10$ minutes: $3{,}000$ m $=3$ km. The target is $3$.',
        'The choices: (1) $\\frac{60\\cdot10\\cdot10}{2}=3{,}000$ (meters, not km), (2) $\\frac{3\\cdot10\\cdot10}{50\\cdot2}=3$, (3) $\\frac{100}{120}$, (4) $\\frac{100}{300}$. Only (2) gives $3$.',
        'With algebra: $\\frac{x}{y}$ m per second $=\\frac{60x}{y}$ m per minute. In $z$ minutes: $\\frac{60xz}{y}$ m $=\\frac{60xz}{1{,}000y}=\\frac{3xz}{50y}$ km.'], None)
    P['18'] = ('Car A leaves a town at $v$ kph. Car B leaves the same town $h$ hours later and drives along the same road at $2v$ kph. How many hours after it leaves does car B catch up with car A?',
               ['$\\frac{h}{2}$', '$h$', '$2h$', '$vh$'], 2, [
        'Head start of A: $v\\cdot h$ km.',
        'A chase: the gap closes at $2v-v=v$ kph. Time $=\\frac{vh}{v}=h$ hours.',
        'Or plug in numbers: $v=10$, $h=1$. A is $10$ km ahead, and B gains $10$ km per hour: $1$ hour $=h$.'], None)
    P['19'] = ('The graph shows the distances of two cyclists, A and B, from town P. They start at the same time and ride at constant speeds. How far from P do they meet, in km?',
               ['$60$', '$40$', '$48$', '$80$'], 2, [
        'Read the speeds. A: $80$ km in $4$ hours, $\\frac{80}{4}=20$ kph, away from P. B: $120$ km in $3$ hours, $\\frac{120}{3}=40$ kph, toward P.',
        'At the start they are $120$ km apart and ride toward each other: the gap closes at $20+40=60$ kph.',
        'They meet after $\\frac{120}{60}=2$ hours. A has ridden $20\\times2=40$ km from P.'], G_P19)
    P['20'] = ('The graph shows a car trip. What is the average speed of the car for the whole trip, in kph?',
               ['$35$', '$33\\frac13$', '$25$', '$40$'], 3, [
        'The car drives $100$ km in $4$ hours in total. The flat part (a stop) counts as time too.',
        'Average speed $=\\frac{100}{4}=25$ kph.',
        'Traps: $35$ averages the two driving speeds, $30$ and $40$. $33\\frac13=\\frac{100}{3}$ leaves out the stop.'], G_P20)
    P['21'] = ('A car drives for 2 hours at 60 kph and then for 2 more hours at 90 kph. What is its average speed for the whole trip, in kph?',
               ['$72$', '$75$', '$70$', '$80$'], 2, [
        'Total distance: $2\\times60+2\\times90=120+180=300$ km, in $4$ hours.',
        'Average speed $=\\frac{300}{4}=75$ kph.',
        'Equal times, therefore the plain average of $60$ and $90$ is right. Trap: $72=\\frac{2\\cdot60\\cdot90}{150}$ is for equal distances.'], None)
    P['22'] = ('A car travels the first third of a route at 30 kph and the rest of the route at 60 kph. What is its average speed for the whole route, in kph?',
               ['$50$', '$40$', '$45$', '$48$'], 3, [
        'Choose a route of $90$ km. First third: $30$ km at $30$ kph, $1$ hour. The rest: $60$ km at $60$ kph, $1$ hour.',
        'Average speed $=\\frac{90}{2}=45$ kph.',
        'Trap: $50=\\frac13\\cdot30+\\frac23\\cdot60$ weights the speeds by distance. Speeds must be weighted by time.'], None)
    for k, (stem, ch, cor, ex, fig) in P.items():
        M.new_q('q-r26-t27-' + k, TOPIC, stem, ch, cor, ex, figure=fig)
        M.place_q('q-r26-t27-' + k, 'wp27-practice')

    # =====================================================================================
    # 12. Practice order: easy -> hard
    # =====================================================================================
    n = lambda k: 'q-r26-t27-' + k
    M.practice_order('wp27-practice', [
        'wp27-p13', 'wp27-p18', 'wp27-p01', 'wp27-p04', 'wp27-p27', 'wp27-p12', 'wp27-p08', 'wp27-p09',
        'wp27-p05', 'wp27-p06', n('15'), 'wp27-p07', 'wp27-p26', 'wp27-p11', 'wp27-p20', n('21'),
        'wp27-p24', 'wp27-p25', n('08'), 'wp27-p15', 'wp27-p16', 'wp27-p10', 'wp27-p02', 'wp27-p03', n('18'),
        n('20'), n('19'), n('10'), 'wp27-p19', n('14'), n('17'), 'wp27-p17', n('16'), n('22'),
        n('09'), n('11'), n('12'), n('13')])

    # trim stray spaces around the old stems
    for f in [f for f in M.D['flow'] if f['topic'] == TOPIC and f['type'] == 'question']:
        st = M.q(f['ref'])['stemRich']
        if st != st.strip(): S(f['ref'], stem=st.strip())

    # =====================================================================================
    # 13. Text fixes in every video of the topic; keep stems shown on slides in sync
    # =====================================================================================
    for vid, v in list(M.D['videos'].items()):
        if v['topic'] != TOPIC: continue
        _text_fixes(M, vid)
        qid = v.get('questionId')
        if qid and qid in M.D['questions']:
            stem = M.q(qid)['stem']
            if qid in ('wp27-g108', 'wp27-g111', 'wp27-g118', 'wp27-g120') or vid.startswith('solve-q-r26'):
                v['title'] = v['navLabel'] = stem
            for b in v['beats']:
                if b.get('canvas', '').startswith('Pre-loaded — question'):
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, stem)
