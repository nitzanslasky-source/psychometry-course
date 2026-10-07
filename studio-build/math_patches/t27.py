"""Topic 27 - Motion. Course review 2026-09 fixes.
See t27_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q
from math_api import _word

TOPIC = 27
L1, L2, L3, L4 = 'wp-106', 'wp-108-after', 'wp-110', 'wp-113'
SPECIAL = 'r26-t27-special'
GRAPHS = 'r26-t27-graphs'
SPECIAL_SB = ['Question %d' % n for n in (14, 15, 16)]
GRAPHS_SB = ['Question %d' % n for n in (17, 18)]


def TABLE(headers, rows, w=1000, h=200):
    return dict(k='vis', v={'type': 'table', 'headers': headers, 'rows': rows}, w=w, h=h)


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
    beats = [dict(mode='title', title=label, script=['Question %s.' % _word(n)] + intro)]
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
        "Honestly? Rare on the exam.",
        "But the idea behind it shows up in disguise. And it's a classic trap — most students fall into it the first time.",
        "So let's understand it properly.",
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
    # wp27-p10: the original asks for a central angle (circles, T33) -> restored and moved to the T33 practice.
    # The "fraction of the track" version stays in T27 under a new id (q-r26-t27-23, created below).
    S('wp27-p10', stem='Two runners leave the same point on a circular track at the same time, in opposite directions. One runs five times as fast as the other. At their first meeting, what central angle corresponds to the arc traveled by the slower runner?',
      choices=['45°', '72°', '90°', '60°'], correct=4, expl=[
        'At their first meeting, together they have covered one full circle.',
        'Equal times: their distances are in the same ratio as their speeds, $1:5$. The circle is $1+5=6$ parts, and the slower runner covers $1$ part: $\\frac16$ of the circle.',
        'Central angle: $\\frac{360°}{6}=60°$.'])
    M.move('wp27-p10', 'geo33-foundation-practice')
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

    # restored originals (pass 2): text clean-up only
    S('wp27-p14', stem='Two cyclists start together and ride in the same direction on a 3-km circular track. Their speeds are 15 and 9 kph. After how many minutes does the faster rider first lap the slower one?', expl=[
        'Lapping means gaining one full lap: $3$ kilometers.',
        'The gain rate is $15-9=6$ kilometers per hour.',
        '$3$ kilometers at that rate take $\\frac36=\\frac12$ hour $=30$ minutes.'])
    S('wp27-p21', stem='A cyclist rides 24 km at 12 kph and returns along the same route at 8 kph. What is the average speed for the whole trip?', expl=[
        'The outward trip takes $\\frac{24}{12}=2$ hours, and the return $\\frac{24}{8}=3$ hours.',
        'The total distance is $24+24=48$ kilometers in $2+3=5$ hours. Average speed $=\\frac{48}{5}=9.6$ kilometers per hour.'])
    S('wp27-p22', stem='Two trains start 420 km apart and move toward each other at 80 and 60 kph. After how many hours do they meet?', expl=[
        'Each hour, the gap falls by $80+60=140$ km.',
        'A gap of $420$ km closes in $\\frac{420}{140}=3$ hours.'])
    S('wp27-p23', stem='A runner travels at 3 meters per second. How many kilometers does she cover in 25 minutes?', expl=[
        '$25$ minutes is $25\\times60=1{,}500$ seconds.',
        'At $3$ meters per second, the distance is $3\\times1{,}500=4{,}500$ meters, or $4.5$ kilometers.'])

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
    # 9. New lesson video: special cases (train length, current, circular track)
    # =====================================================================================
    sb = ['Train length', 'Current', 'Circular track', 'Recap']
    M.new_video(SPECIAL, TOPIC, 'Special Motion Cases', sb, [
        dict(mode='title', title='Special Motion Cases', script=[
            "Special cases.",
            "Trains that have a length. Boats on a river. And circular tracks.",
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
        dict(mode='concept', active=1, title='Current', script=[
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
        dict(mode='concept', active=2, title='Circular track', script=[
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
        dict(mode='concept', active=3, title='Recap', script=[
            "Let's lock it in.",
            A("'Train past a post: its own length' appears", T('Train past a post: its own length', size=36)),
            A("'Tunnel: tunnel + train' appears", T('Through a tunnel: tunnel $+$ train', size=36)),
            A("'River: add or subtract; current = half the difference' appears", T('River: down $=$ boat $+$ current, up $=$ boat $-$ current; current $=$ half the difference', size=36)),
            A("'Circle: one lap per meeting' appears", T('Circle: one lap per meeting — same direction subtract, opposite add', size=36)),
            D('Tick each line'),
            "Three questions next. Try each one first — then watch.",
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
    _solution(M, g1, 'Special Motion Cases', SPECIAL_SB, ["A train with a length."], [
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
    _solution(M, g2, 'Special Motion Cases', SPECIAL_SB, ["Downstream, upstream — find the current."], [
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
    _solution(M, g3, 'Special Motion Cases', SPECIAL_SB, ["A circular track — opposite directions."], [
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

    # =====================================================================================
    # 10. New lesson video: percents and letters (the distance-time graphs block was removed by the teacher)
    # =====================================================================================
    sb = ['Speed % → time %', 'Answers in letters', 'Recap']
    M.new_video(GRAPHS, TOPIC, 'Percents and Letters', sb, [
        dict(mode='title', title='Percents and Letters', script=[
            "Two exam favorites.",
            "Speed changes by a percent. And answers written with letters.",
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
        dict(mode='concept', active=2, title='Recap', script=[
            "Let's lock it in.",
            A("'Speed × fraction → time × the flipped fraction' appears", T('Speed $\\times\\frac54$ $\\to$ time $\\times\\frac45$: $+25\\%$ speed $=-20\\%$ time', size=38)),
            A("'Letters: plug in easy numbers' appears", T('Letters in the choices: plug in easy numbers (not $0$ or $1$)', size=38)),
            D('Tick each line'),
            "Two questions next.",
        ]),
    ], 'wp27-advanced', after='solve-' + g3)

    # ---- guided Q18: percent speed -> time
    g5 = 'q-r26-t27-05'
    M.new_q(g5, TOPIC, 'A cyclist rides from home to work at a constant speed. If she rode 25% faster, the trip would take 12 minutes less. How many minutes does the trip take at her usual speed?',
            ['$36$', '$48$', '$60$', '$72$'], 3, [
        '25% faster: the speed is multiplied by $\\frac54$. Same distance: the time is multiplied by $\\frac45$. That is 20% less time.',
        '20% of the usual time is $12$ minutes: $\\frac15T=12$. Therefore $T=60$ minutes.',
        'Check: $60\\times\\frac45=48$ minutes, which is $12$ minutes less.',
        'Trap: $12\\div0.25=48$ assumes that the time drops by 25%. And $48$ is the new time, not the usual time.'])
    M.place_q(g5, 'wp27-advanced', after=GRAPHS)
    _solution(M, g5, 'Percents and Letters', GRAPHS_SB, ["Faster by a percent — how much time is saved?"], [
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
    _solution(M, g6, 'Percents and Letters', GRAPHS_SB, ["Letters in the question, letters in the answers."], [
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

    # ---- memory card for the new methods
    M.new_card('mem-r26-t27-special', TOPIC, 'wp27-advanced', {
        'title': 'Motion — special cases',
        'intro': 'Trains, rivers, circular tracks, percents and letters.',
        'tables': [
            {'title': 'Special cases', 'head': ['Situation', 'Distance', 'Speed'], 'rows': [
                ['Train passes a post or a person', 'the train’s length', 'the train’s speed'],
                ['Train passes through a tunnel or over a bridge', 'tunnel $+$ train', 'the train’s speed'],
                ['Boat downstream / upstream', '—', 'boat $+$ current / boat $-$ current'],
                ['Both trips given', '—', 'current $=\\frac{\\text{down}-\\text{up}}{2}$, boat $=\\frac{\\text{down}+\\text{up}}{2}$'],
                ['Circle, same direction', '$1$ lap per meeting', 'difference of the speeds'],
                ['Circle, opposite directions', '$1$ lap per meeting', 'sum of the speeds']]},
            {'title': 'Speed % → time % (same distance)', 'head': ['Speed', 'Time'], 'rows': [
                ['$+25\\%$ ($\\times\\frac54$)', '$-20\\%$ ($\\times\\frac45$)'],
                ['$+50\\%$ ($\\times\\frac32$)', '$-33\\frac13\\%$ ($\\times\\frac23$)'],
                ['$+100\\%$ ($\\times2$)', '$-50\\%$ ($\\times\\frac12$)'],
                ['$-20\\%$ ($\\times\\frac45$)', '$+25\\%$ ($\\times\\frac54$)']]}],
        'tips': [
            'Letters in the choices? Plug in easy numbers (not $0$ or $1$), find the target, and test every choice.',
            'If two choices give the target, try other numbers on those two.',
            'Speed changes by a percent? Write it as a fraction, flip it, and read the change of the time.']},
        after='solve-' + g6)

    # =====================================================================================
    # 11. New practice questions (exam level)
    # =====================================================================================
    P = {}
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
    # the pass-1 version of wp27-p10 ("fraction of the track"), kept under a new id; the original moved to T33
    P['23'] = ('Two runners leave the same point on a circular track at the same time and run in opposite directions. One runs five times as fast as the other. What fraction of the track has the slower runner covered when they meet for the first time?',
               ['$\\frac18$', '$\\frac15$', '$\\frac14$', '$\\frac16$'], 4, [
        'Opposite directions on a circle: at the first meeting, together they have covered exactly one lap.',
        'Equal times: the distances follow the speed ratio $1:5$. The lap is $1+5=6$ parts.',
        'The slower runner covers $1$ part: $\\frac16$ of the track.',
        'Trap: $\\frac15$ compares the two runners, not the slower runner with the whole lap.'], None)
    for k, (stem, ch, cor, ex, fig) in P.items():
        M.new_q('q-r26-t27-' + k, TOPIC, stem, ch, cor, ex, figure=fig)
        M.place_q('q-r26-t27-' + k, 'wp27-practice')

    # =====================================================================================
    # 12. Practice order: easy -> hard
    # =====================================================================================
    n = lambda k: 'q-r26-t27-' + k
    M.practice_order('wp27-practice', [
        'wp27-p13', 'wp27-p23', 'wp27-p18', 'wp27-p01', 'wp27-p04', 'wp27-p27', 'wp27-p22', 'wp27-p12', 'wp27-p08',
        'wp27-p09', 'wp27-p05', 'wp27-p06', n('15'), 'wp27-p07', 'wp27-p26', 'wp27-p11', 'wp27-p20', 'wp27-p21',
        n('21'), 'wp27-p24', 'wp27-p14', 'wp27-p25', 'wp27-p15', 'wp27-p16', n('23'), 'wp27-p02', 'wp27-p03',
        n('18'), n('10'), 'wp27-p19', n('17'), 'wp27-p17', n('16'), n('22'), n('09'), n('11'), n('12')])

    # =====================================================================================
    # 12b. Summary lesson right before the practice (pass 2)
    # =====================================================================================
    sbS = ['The formula', 'The table', 'Average speed', 'What is fixed?', 'Relative speed', 'Special cases',
           'Percents and letters', 'Before you practice']
    M.new_video('r26-t27-summary', TOPIC, 'Summary', sbS, [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of motion.",
            "Everything important, in a few minutes.",
        ]),
        dict(mode='concept', active=0, title='The formula', script=[
            A('The formula appears', T('$\\text{distance}=\\text{time}\\times\\text{speed}$', size=46)),
            "Distance equals time times speed. Need the time? Distance divided by speed.",
            A("'Same units, always' appears", T('Same units, always: $36$ minutes $=\\frac35$ hour, $50$ minutes $=\\frac56$ hour', size=38)),
            "Always work in the same units. Minutes are fractions of an hour.",
            A("'Identical ratios, not 3.6' appears", T('Converting a speed? Identical ratios ($\\times60$, $\\times15$) — not $3.6$', size=38)),
            "Converting a speed? Use identical ratios. Forget three point six.",
        ]),
        dict(mode='concept', active=1, title='The table', script=[
            A('The table appears', TABLE(['', 'Distance', 'Speed', 'Time'], [['Part 1', '', '', ''], ['Part 2', '', '', ''],
                                                                            ['Total', '', '', '']], w=900, h=260)),
            "Two people, or one trip in two parts? A table. One row for each.",
            "In every row: distance equals speed times time.",
            "In the total row, add the distances and add the times. Never add the speeds.",
            "Then find the link: equal times, equal distances, or a total. That's your equation.",
        ]),
        dict(mode='concept', active=2, title='Average speed', script=[
            A('The rule appears', T('Average speed $=$ total distance $\\div$ total time', size=42)),
            "Average speed: total distance over total time. Stops count as time too.",
            A("'Equal times → plain average' appears", T('Equal times $\\to$ the plain average', size=40)),
            A("'Equal distances → closer to the slower' appears", T('Equal distances $\\to$ closer to the slower speed', size=40)),
            "Equal times? The plain average works. Equal distances? The answer sits closer to the slower speed.",
            "Distance missing? Pick a friendly number.",
        ]),
        dict(mode='concept', active=3, title='What is fixed?', script=[
            A("'Same time → distances follow speeds' appears", T('Same time $\\to$ distances follow the speeds', size=40)),
            A("'Same speed → distances follow times' appears", T('Same speed $\\to$ distances follow the times', size=40)),
            A("'Same distance → times flip' appears", T('Same distance $\\to$ times flip: speeds $5:2$, times $2:5$', size=40)),
            "Ratios save calculation. First ask: what is fixed?",
            "Same time: distances follow the speeds. Same distance: the times flip.",
        ]),
        dict(mode='concept', active=4, title='Relative speed', script=[
            A("'Toward or apart: add' appears", T('Toward each other or apart: add the speeds', size=40)),
            A("'A chase: subtract' appears", T('A chase (same direction): subtract the speeds', size=40)),
            "Toward each other, or moving apart: add the speeds. A chase: subtract.",
            A("'Only the gap at the start' appears", T('The distance that matters: the gap at the start', size=40)),
            "In a chase, the only distance that matters is the gap at the start.",
            "One left earlier? Work out the head start first. That's your gap.",
        ]),
        dict(mode='concept', active=5, title='Special cases', script=[
            A("'Train' appears", T('Train: past a post $=$ its length; tunnel $=$ tunnel $+$ train', size=38)),
            "A train has a length. Past a post: its own length. Through a tunnel: tunnel plus train.",
            A("'River' appears", T('River: down $=$ boat $+$ current, up $=$ boat $-$ current', size=38)),
            "A river: downstream, add the current. Upstream, subtract. The current is half the difference.",
            A("'Circle' appears", T('Circle: one lap per meeting — same direction subtract, opposite add', size=38)),
            "A circular track: they meet once every lap — gained, or covered together.",
        ]),
        dict(mode='concept', active=6, title='Percents and letters', script=[
            A("'Speed × 3/4 → time × 4/3' appears", T('Speed $\\times\\frac34$ $\\to$ time $\\times\\frac43$: $-25\\%$ speed $=+33\\frac13\\%$ time', size=38)),
            "The speed changes by a percent? Write it as a fraction and flip it. Twenty-five percent slower: a third more time.",
            A("'Letters: plug in easy numbers' appears", T('Letters in the choices: plug in easy numbers (not $0$ or $1$)', size=38)),
            "Letters in the choices? Plug in easy numbers, find the target, and test every choice.",
        ]),
        dict(mode='concept', active=7, title='Before you practice', script=[
            "Before every question, ask yourself:",
            A('Check 1 appears', T('Same units everywhere?', size=40)),
            A('Check 2 appears', T('What is fixed: time, speed or distance?', size=40)),
            A('Check 3 appears', T('Toward each other, or a chase? What is the gap at the start?', size=40)),
            A('Check 4 appears', T('Average speed? Total distance $\\div$ total time', size=40)),
            "And the traps: fifty minutes is not point five of an hour. The average speed is not the average of the speeds.",
            "In a chase, count only the starting gap. And draw a sketch — every time.",
            "Good luck. Let's practice.",
        ]),
    ], 'wp27-advanced', after='mem-r26-t27-special')

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
    cut_repeats(M)
    add_methods(M)   # 2026-10-06 new exam methods (runs last)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)


# =====================================================================================
# 2026-10-05 cut repeats: each lesson back to a short intro (Hebrew style); every idea a
# question video already teaches is cut from the lesson; ideas no question teaches stay or
# move as one line + board item into the question video that uses them.
# =====================================================================================
def _add_line(M, vid, n, before_say, line, item=None, label=None):
    """Insert one spoken line (+ optional board item) right before the line containing `before_say`
    (before_say=None: at the end of the slide). Keeps the slide's loads/canvas text."""
    b = M.slide(vid, n); keep = (b.get('loads'), b.get('canvas')); script = []; hit = False
    add = ([A(label, item)] if item is not None else []) + [line]
    for l in b['lines']:
        if before_say is not None and not hit and before_say in (l.get('say') or l.get('draw') or l.get('label') or ''):
            script += add; hit = True
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        else: script.append(D(l['draw']))
    if before_say is None:
        script += add; hit = True
    assert hit, '%s #%d: not found: %s' % (vid, n, before_say)
    M.set_slide(vid, n, script=script)
    b = M.slide(vid, n); b['loads'], b['canvas'] = keep


def _keep_slides(M, vid, keep, sidebar):
    """Keep only the slides `keep` (1-based, in order); set the sidebar; renumber 'active'."""
    v = M.video(vid)
    M.remove_slides(vid, [k for k in range(1, len(v['beats']) + 1) if k not in keep])
    a = 0
    for b in v['beats']:
        if b.get('mode') == 'concept':
            b['active'] = a; a += 1
    M.set_sidebar(vid, sidebar)


def cut_repeats(M):
    # ---- Distance, Speed and Time: kept (= the Hebrew intro); only the recap is cut ---------
    vid = 'wp-106'
    _keep_slides(M, vid, [1, 2, 3, 4, 5, 6, 7], ['Motion is work', 'The formula', 'Units', 'Forget 3.6', 'The table', 'Draw a sketch'])
    _add_line(M, vid, 7, None, 'Two questions next. Then: average speed.')

    # ---- Average Speed: the recap repeats the lesson and Q3 (estimate first, 2ab/(a+b)) ----
    vid = 'wp-108-after'
    _keep_slides(M, vid, [1, 2, 3, 4], ['What it means', 'The formula', 'Not the average'])
    _add_line(M, vid, 4, None, 'One question next — then speed ratios.')

    # ---- Speed Ratios: recap cut (repeats slides 3-6) ---------------------------------------
    vid = 'wp-110'
    _keep_slides(M, vid, [1, 2, 3, 4, 5, 6], ['No calculation', 'Same time', 'Same speed', 'Same distance', 'What is fixed?'])
    _add_line(M, vid, 6, None, 'Two questions next — watch how the ratios do all the work.')

    # ---- Relative Speed: recap cut (the rest is the Hebrew intro, kept) ---------------------
    vid = 'wp-113'
    _keep_slides(M, vid, [1, 2, 3, 4, 5], ['What it is', 'Opposite directions', 'Same direction', 'The gap only'])
    _add_line(M, vid, 5, None, 'Chases are where students slip. Three questions next.')

    # ---- Special Motion Cases: title only; each case is taught in its question -------------
    vid = 'r26-t27-special'
    _keep_slides(M, vid, [1], [])
    M.edit_lines(vid, 1, lambda ls: [
        {'say': 'Special cases.'},
        {'say': 'Trains that have a length. Boats on a river. And circular tracks.'},
        {'say': 'The formula stays the same: distance equals time times speed. Only the distance, or the speed, is different.'},
        {'say': "Each case has one idea — and we'll learn each one in its question. Try each one first — then watch."}])
    # Train length -> Q14 (post = its own length, bridge = bridge + train, with the drawing)
    _add_line(M, 'solve-q-r26-t27-01', 2, 'First the speed.',
              'Until now, every body was a dot. A train is not a dot — it has a length.',
              T('A train has a length: past a post $=$ its length · bridge $=$ bridge $+$ train', 34),
              "'A train has a length: past a post = its length · bridge = bridge + train' appears")
    # Current -> Q15 (boat + current, boat − current, half the difference); move the wind line
    _add_line(M, 'solve-q-r26-t27-02', 2, 'First, the two speeds.',
              'With the current — downstream — add it. Against it — upstream — subtract. A plane with the wind? The same: a tailwind adds, a headwind subtracts.',
              T(r'Down $=$ boat $+$ current · up $=$ boat $-$ current (wind: the same)', 34),
              "'Down = boat + current · up = boat − current (wind: the same)' appears")
    # Circular track -> Q13 (same direction: one extra lap, subtract) and Q16 (opposite: one lap together, add)

    # ---- Percents and Letters: title only; both ideas are taught in Q17 and Q18 ------------
    vid = 'r26-t27-graphs'
    _keep_slides(M, vid, [1], [])
    M.edit_lines(vid, 1, lambda ls: [
        {'say': 'Two exam favorites.'},
        {'say': 'Speed changes by a percent. And answers written with letters.'},
        {'say': 'One warning: a percent faster is NOT the same percent less time.'},
        {'say': 'Two questions next — one of each.'}])
    # Speed % -> time %: Q17 teaches "write it as a fraction, flip it"; move the "slower" row there
    _add_line(M, 'solve-q-r26-t27-05', 2, 'Forty-eight is the trap.',
              'Slower works the same way: twenty percent slower is speed times four fifths — so the time is times five quarters, twenty-five percent MORE.',
              T(r'Speed $\times\frac45$ $\to$ time $\times\frac54$: $-20\%$ speed $=+25\%$ time', 34),
              "'Speed × 4/5 → time × 5/4: −20% speed = +25% time' appears")
    # Letters: Q18 teaches plug in (not 0 or 1), the target, test every choice; add the remedy
    _fix_say(M, 'solve-q-r26-t27-06', 2, 'Then choices three and four both give the target.',
             'Then choices three and four both give the target. Two choices give the target? Try other numbers on those two.')

    # ---- follow-up: nothing lost -------------------------------------------------------------
    # "+50% speed -> -33 1/3% time" and "twice as fast -> half the time" (from the cut Speed % slide) -> Q17
    _add_line(M, 'solve-q-r26-t27-05', 2, 'Slower works the same way',
              'Fifty percent faster: speed times three halves, time times two thirds — thirty-three and a third percent less. Twice as fast: half the time.',
              T(r'$+50\%$ speed $\to$ time $\times\frac23$: $-33\frac13\%$ · twice as fast $\to$ half the time', 34),
              "'+50% speed → time × 2/3: −33⅓% · twice as fast → half the time' appears")
    # "boat in still water = the average of the two speeds" (from the cut Current slide) -> Q15 check
    _add_line(M, 'solve-q-r26-t27-02', 3, None,
              'And the boat in still water is the average of the two speeds: twenty-four plus sixteen, over two — twenty.',
              T(r'Boat $=\frac{\text{down}+\text{up}}{2}=\frac{24+16}{2}=20$', 34),
              "'Boat = (down + up) ÷ 2 = (24 + 16) ÷ 2 = 20' appears")


# =====================================================================================
# 2026-10-06 new exam methods (teacher-approved). Nothing in topic 27 is recorded.
# 1. Product in the middle: every motion table is Speed · Distance · Time (like Team · Work · Time), so the V works.
# 2. Speed Ratios: one slide "Two things change? The V" + one guided question with a solution video.
# 3. Card: the V row and "x times slower / smaller = ÷ x".
# =====================================================================================
def _reorder_tables(M):
    """Every Distance/Speed/Time table in topic 27 -> Speed, Distance, Time (other columns keep their place)."""
    done = []
    for f in M.D['flow']:
        if f['topic'] != TOPIC or f['type'] != 'video': continue
        v = M.video(f['ref'])
        for n, b in enumerate(v['beats'], 1):
            for it in b['items']:
                tv = it.get('v') or {}
                if tv.get('type') != 'table': continue
                h = tv['headers']
                if not {'Distance', 'Speed', 'Time'} <= set(h): continue
                pos = sorted(h.index(x) for x in ('Distance', 'Speed', 'Time'))
                src = [h.index('Speed'), h.index('Distance'), h.index('Time')]
                perm = list(range(len(h)))
                for p, s_ in zip(pos, src): perm[p] = s_
                tv['headers'] = [h[k] for k in perm]
                tv['rows'] = [[r[k] for k in perm] for r in tv['rows']]
                M.touched_videos.add(v['id']); done.append((v['id'], n))
    return done


def add_methods(M):
    # ---- 1. the table order -------------------------------------------------------------
    done = _reorder_tables(M)
    assert len(done) >= 6, done
    _fix_say(M, L1, 6, 'Three columns: distance, speed, time.',
             'Three columns: speed, distance, time. Distance in the middle — because distance is speed times time, just like work in Team, Work, Time.')
    _fix_say(M, 'solve-wp27-g119', 2, 'A distance–time–speed table.', 'A speed–distance–time table.')
    c = M.card('mem-motion')
    c['tips'] = [t.replace('Make a distance–speed–time table: one row each.',
                           'Make a speed–distance–time table (distance in the middle): one row each.') for t in c['tips']]
    assert any('distance in the middle' in t for t in c['tips'])

    # ---- 2. Speed Ratios: "Two things change? The V" ---------------------------------------
    vid = L3   # wp-110
    last = len(M.video(vid)['beats'])
    M.edit_lines(vid, last, lambda ls: [l for l in ls if l.get('say') != 'Two questions next — watch how the ratios do all the work.'])
    M.insert_slides(vid, last, [dict(mode='concept', active=5, title='Two things change? The V', script=[
        'One more tool. What if TWO things change at once — the speed and the time — and you get only relations?',
        A("'A and B' appears", T(r'A is $3$ times as fast as B and drives half as long. A covers $90$ km. How far does B drive?', size=36, gap=40)),
        'Make the table like a team table: speed, distance, time. Distance in the middle — it is speed times time, like work is team times time.',
        A("'Speed · Distance · Time table' appears", TABLE(['', 'Speed', 'Distance', 'Time'], [['A', '3', '90', '1'], ['B', '1', '?', '2']], w=720, h=170)),
        'No real speeds or times? Put in the relations. A: speed three, time one. B: speed one — and time two, because A drives half as long as B.',
        'The question row goes second. The blank is in the middle column — so the V turns upside down: bottom-left, top-middle, bottom-right.',
        D('Draw an upside-down V through 1, 90 and 2; write "? = (1 · 90 · 2) ÷ (3 · 1) = 60"'),
        'One times ninety times two, divided by the other two — three times one. Sixty kilometers.',
        'Why it works: B is three times slower — a third of the distance — but drives twice as long — twice the distance. Ninety times a third times two: sixty.',
        A("'Two things change → the V, distance in the middle' appears", T(r'Two things change? The V, distance in the middle', size=40, gap=50)),
        'So: two things change? The V, with distance in the middle.',
        'Three questions next — watch how the ratios do all the work.'])])
    sb = M.video(vid)['hybrid']['sidebar']
    M.set_sidebar(vid, sb + ['Two things change'])

    # ---- guided question right after Q5 (wp27-g112) -----------------------------------------
    qid = 'q-r26-t27-31'
    M.new_q(qid, TOPIC,
            "A delivery van travels 3 times as far as a scooter, at 1.5 times the scooter's speed. "
            "The scooter's trip takes 40 minutes. How many minutes does the van's trip take?",
            ['20', '80', '120', '180'], 2,
            ['Table Speed · Distance · Time. Scooter: $1$, $1$, $40$. Van: $1.5$, $3$, $?$.',
             'The blank is in the Time column, so the V: top-left $\\times$ bottom-middle $\\times$ top-right, divided by the other two: '
             '$\\frac{1\\cdot3\\cdot40}{1\\cdot1.5}=\\frac{120}{1.5}=80$ minutes.',
             'Or by factors: time $=$ distance $\\div$ speed. Distance $\\times3$ (same way), speed $\\times1.5$ (opposite way, flip): '
             '$40\\times3\\times\\frac23=80$.',
             'Traps: $180=40\\times3\\times1.5$ (speed not flipped); $120$ ignores the speed.'])
    M.place_q(qid, M.section_of('wp27-g112'), after='solve-wp27-g112')
    group_sb = list(M.video('solve-wp27-g112')['hybrid']['sidebar'])
    n = M.next_question_number(TOPIC)
    lab = 'Question %d' % n
    new_sb = group_sb + [lab]
    for v in M.D['videos'].values():
        if v['topic'] == TOPIC and v.get('kind') == 'solution' and v.get('hybrid', {}).get('sidebar') == group_sb:
            M.set_sidebar(v['id'], new_sb)
    group = M.video('solve-wp27-g112')['beats'][0]['title']
    _solution(M, qid, group, new_sb, ['Two things change at once — the distance and the speed. The V.'], [
        ('Method 1 · The V', [
            'No real distances, no real speed. Only relations — and one real time.',
            A("'Speed · Distance · Time table' appears", TABLE(['', 'Speed', 'Distance', 'Time'], [['Scooter', '1', '1', '40'], ['Van', '1.5', '3', '?']], w=720, h=170)),
            'Speed, distance, time — distance in the middle. Scooter: speed one, distance one, forty minutes.',
            'Van: speed one and a half, distance three. The time is the question — row two.',
            'The blank is in the Time column. A normal V: top-left, bottom-middle, top-right.',
            D('Draw a V through 1, 3 and 40; write "? = (1 · 3 · 40) ÷ (1 · 1.5) = 120 ÷ 1.5 = 80"'),
            'One times three times forty: a hundred twenty. Divided by the other two, one times one and a half: eighty.',
            D('Circle choice 2'),
            'Eighty minutes. Choice two.']),
        ('Method 2 · Compare by factors', [
            'The same thing without a table. Time equals distance divided by speed.',
            D('Write "distance × 3 → time × 3 (same way)"'),
            'Three times as far: more distance, more time. Same way — times three.',
            D('Write "speed × 3/2 → time × 2/3 (opposite way)"'),
            'One and a half times as fast: more speed, LESS time. Opposite way — flip three halves to two thirds.',
            D('Write "40 × 3 × 2/3 = 80"'),
            'Forty times three times two thirds: eighty.',
            'A hundred eighty is the trap: the speed was not flipped. A hundred twenty forgot the speed. A faster van with three times the road — more than forty, less than a hundred twenty.']),
    ])

    # ---- 3. memory card ------------------------------------------------------------------------
    rows = next(t for t in c['tables'] if t.get('title', '').startswith('Ratios'))['rows']
    rows.append(['Two things change', 'table Speed · Distance · Time, distance in the middle $\\to$ the V',
                 'A: $3$, $90$, $1$ · B: $1$, $?$, $2$ $\\to$ $\\frac{1\\cdot90\\cdot2}{3\\cdot1}=60$'])
    c['tips'].insert(1, '"$x$ times slower / smaller" $=\\div x$: A is $3$ times slower than B $\\to$ A\'s speed $=$ B\'s $\\div3$.')


# =====================================================================================
# 2026-10-06 practice: new methods (runs LAST). Extra method lines appended to practice
# explanations, using the course names of the 2026-10-06 methods.
# =====================================================================================

def _pm_add(M, qid, lines):
    """Append extra-method lines to a PRACTICE question explanation (existing lines kept)."""
    sec = M.section_of(qid)
    assert sec.endswith("-practice"), (qid, sec)
    ex = list(M.q(qid).get("explanation") or [])
    if any(l in ex for l in lines): return
    M.set_q(qid, expl=ex + list(lines))


def practice_methods(M):
    _pm_add(M, 'wp27-p02', [r'Method 2 · The V in motion: table Speed · Distance · Time, rows $(1, d, t)$ and $(3, ?, 2t)$. The blank is in the middle → upside-down V: $?=\frac{3\cdot2t\cdot d}{1\cdot t}=6d$.'])
    _pm_add(M, 'wp27-p12', [r'Method 2 · Compare by factors, evening against morning: distance $\times\frac{2.4}{1.8}=\frac43$ (same way); speed $\times\frac12$ (opposite → flip to $2$). Evening: $30\cdot\frac43\cdot2=80$ minutes, and $30+80=110$.'])
    _pm_add(M, 'wp27-p21', [r'Method 2 · Percent shares as weights (the weights are the hours): $3$ of the $5$ hours ($60\%$) are at $8$ kph and $40\%$ at $12$ kph. Average $=8+0.4\cdot4=9.6$ kph.'])


# =====================================================================================
# 2026-10-06 renumber pass (runs LAST). Every Hebrew-derived question (guided wp27-g107…g121,
# practice wp27-p01…p20) gets a new story and new numbers; the concept, the trap, the level and
# the methods stay the same. Solution videos rewritten to match. Hebrew-derived lesson examples
# (seeds 20 per hour, walker 5 m/s for half an hour, walkers 4 + 6) get new numbers.
# Practice clean-up: copies, extra warm-ups beyond 3, September items whose type the Hebrew covers.
# Nothing in topic 27 is recorded (~/Documents/Course.recordings has only algebra takes).
# =====================================================================================
from math_api import rich_plain

RN_RECORDED = set()   # no take of any topic-27 video (checked 2026-10-06)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. The pre-loaded question stays."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script)


def _vis(v, w, h): return dict(k='vis', v=v, w=w, h=h)


def rn_lessons(M):
    # ---- wp-106 #1-#2: "20 seeds per hour / 20 km per hour" (the Hebrew's own example) -> 25 boxes / 25 km
    _fix_say(M, L1, 1, 'Instead of cracking seeds, you\'re covering distance.', 'Instead of packing boxes, you\'re covering distance.')
    M.set_slide(L1, 2, script=[
        'In work problems, you packed twenty-five boxes an hour.',
        A("'Work: 25 boxes per hour' appears", T('Work: $25$ boxes per hour', size=48)),
        'In motion, you cover twenty-five kilometers an hour.',
        A("'Motion: 25 km per hour' appears", T('Motion: $25$ km per hour', size=48)),
        D('Draw an equals sign between the two lines'),
        "Exactly the same idea. You'll keep seeing the parallels.",
        "A few things ARE different — and that's what this lesson is about."])
    # ---- wp-106 #5: walker 5 m/s, half an hour -> 9 km (Hebrew) ==> cyclist 8 m/s, 25 minutes -> 12 km
    M.set_slide(L1, 5, script=[
        'Some books teach: meters per second to kilometers per hour — multiply by three point six.',
        'Forget it. It almost never appears on the exam — and nobody remembers whether to multiply or divide.',
        'Instead: identical ratios. Watch.',
        A('The example appears: 8 meters per second — how many km in 25 minutes?',
          T('A cyclist rides at $8$ meters per second. How many km does she cover in $25$ minutes?', size=38)),
        A('A time–distance table appears with two blank rows',
          TABLE(['Time', 'Distance'], [['1 second', '8 m'], ['1 minute', ''], ['25 minutes', '']], w=700, h=190)),
        D('Write "×60" beside the rows and fill in 480 m'),
        'One second to one minute: times sixty. So the distance times sixty too — four hundred eighty meters.',
        D('Write "×25" and fill in 12,000 m = 12 km'),
        'One minute to twenty-five minutes: times twenty-five. Twelve thousand meters — twelve kilometers.',
        'Easy — and you never have to memorize a conversion factor.'])
    # ---- wp-113 #3: walkers 4 + 6 = 10 (the Hebrew's 6 and 4) ==> 3 + 5 = 8
    M.set_slide(L4, 3, script=[
        A("'Toward each other: add the speeds' appears", T('Toward each other: add the speeds', size=46)),
        'Two bodies coming toward each other? Add the speeds.',
        'Picture a head-on crash — the crash hits at both speeds combined.',
        A("'3 + 5 = 8 km per hour' appears", T('$3+5=8$ km per hour', size=50)),
        D('Draw two arrows pointing at each other above the sum'),
        'Walkers at three and five kilometers an hour, coming together: the gap shrinks eight kilometers every hour.',
        'Moving apart in opposite directions? Same thing — add. The gap GROWS eight kilometers an hour.'])
    # ---- memory card: its examples were the guided questions' numbers (0.8/12, 288/5, 72 and 48)
    c = M.card('mem-motion')
    for t in c['tables']:
        for r in t['rows']:
            for k, x in enumerate(r):
                r[k] = (x.replace('$\\frac{0.8}{12}=\\frac1{15}$ hour', '$\\frac{1.5}{9}=\\frac16$ hour')
                         .replace('$\\frac{288}{5}=57.6$ kph', '$\\frac{240}{8}=30$ kph')
                         .replace('$72$ and $48\\to57.6$', '$40$ and $24\\to30$'))
    flat = repr(c['tables'])
    assert '57.6' not in flat and '0.8' not in flat and '$40$ and $24' in flat, flat[:300]


def rn_guided(M):
    # ---------- g107: cart 4 m/s, 25 min -> 6 km (Hebrew: walker 5 m/s, half an hour -> 9 km)
    #            ==>  electric scooter 6 m/s, 50 min -> 18 km
    _rn_q(M, 'wp27-g107', 'An electric scooter moves at 6 meters per second. How many kilometers does it travel in 50 minutes?',
          ['$0.3$', '$1.8$', '$18$', '$30$'], 3, [
        'In $1$ second the scooter covers $6$ meters. In $1$ minute ($60$ seconds) it covers $6\\times60=360$ meters.',
        'In $50$ minutes: $360\\times50=18{,}000$ meters $=18$ km.',
        'Trap: $6\\times50=300$ meters $=0.3$ km mixes seconds with minutes.'])
    _rn_video(M, 'wp27-g107', [[
        'Meters per second — but the answer is in kilometers, after fifty minutes.',
        'No three point six. Identical ratios.',
        A('A time–distance table appears', TABLE(['Time', 'Distance'], [['1 second', '6 m'], ['1 minute', ''], ['50 minutes', '']], w=700, h=190)),
        D('Write "×60" and fill in 360 m'),
        'One second to one minute: times sixty. Six meters becomes three hundred sixty.',
        D('Write "×50" and fill in 18,000 m'),
        'One minute to fifty minutes: times fifty. Eighteen thousand meters.',
        D('Write "= 18 km" and circle choice 3'),
        'A thousand meters in a kilometer — eighteen kilometers. Choice three.',
        'Notice the trap: six times fifty — three hundred meters — mixes seconds with minutes.',
    ]])

    # ---------- g108: drone 390 kph, 2 min, ground 12 -> height 5 (Hebrew: plane 300 kph, 1 min, ground 4 -> 3)
    #            ==>  gondola lift 17 kph, 6 min, ground 1.5 km -> height 0.8 km (8-15-17)
    _rn_q(M, 'wp27-g108', 'A gondola lift climbs along a straight cable at 17 kph. After 6 minutes, its horizontal distance from the bottom station is 1.5 kilometers. How high above the bottom station is it, in kilometers?',
          ['$1.7$', '$0.8$', '$1.5$', '$0.2$'], 2, [
        '$6$ minutes $=\\frac{6}{60}=\\frac1{10}$ hour. The gondola travels $17\\times\\frac1{10}=1.7$ km along its sloping cable.',
        'Sketch a right triangle: the ground ($1.5$ km) and the height are the two short sides. The path along the cable ($1.7$ km) is the long side.',
        'Pythagoras: $h^2=1.7^2-1.5^2=2.89-2.25=0.64$. Therefore $h=0.8$ km. (In tenths of a km: $17^2-15^2=289-225=64$, root $8$.)',
        'Trap: $1.7$ is the length of the path, not the height.'])
    _rn_video(M, 'wp27-g108', [[
        'Motion plus geometry. First: how far did the gondola actually travel?',
        'Seventeen kilometers an hour — and we need six minutes.',
        D('Write "17 km — 60 min" and below it "1.7 km — 6 min", with "÷10" beside it'),
        'An hour is sixty minutes. Sixty to six: divide by ten. Seventeen over ten: one point seven kilometers.',
        'Now draw it — the sketch shows a right triangle.',
        A('A right triangle appears: ground 1.5 km, height and slope unknown',
          _vis({'type': 'rightTriangle', 'base': '1.5 km', 'height': '?', 'hypotenuse': '?'}, 900, 250)),
        D('Write 1.7 on the sloping side'),
        'One point seven is the sloping path — the distance it really traveled.',
        'One point five along the ground. Drop a perpendicular — the height is the missing side.',
        D('Write 0.8 for the height and circle choice 2'),
        'Count in tenths of a kilometer: fifteen and seventeen. Eight, fifteen, seventeen. The height is eight tenths — zero point eight kilometers. Choice two.',
        "Don't know that triple? Pythagoras: seventeen squared minus fifteen squared — two eighty-nine minus two twenty-five, sixty-four. Root: eight. Eight tenths of a kilometer.",
    ]])

    # ---------- g109: 72 / 48 -> 57.6 (Hebrew: 60 / 40 -> 48, 120 km)  ==>  105 / 70 -> 84 (210 km)
    _rn_q(M, 'wp27-g109', 'A car drives from a city to the coast at 105 kph and returns along the same road at 70 kph, without stopping. What is its average speed for the whole round trip?',
          ['$90$ kph', '$84$ kph', '$87.5$ kph', '$80$ kph'], 2, [
        'Estimate first: the plain average is $\\frac{105+70}2=87.5$. The slow part takes more time. Therefore the answer is below $87.5$: choices (1) and (3) are out.',
        'Choose a distance that both speeds divide: $210$ km each way. There: $\\frac{210}{105}=2$ hours. Back: $\\frac{210}{70}=3$ hours.',
        'Average speed $=\\frac{\\text{total distance}}{\\text{total time}}=\\frac{420}{5}=84$ kph.',
        'Check (equal distances only): $\\frac{2\\cdot105\\cdot70}{105+70}=\\frac{14{,}700}{175}=84$.'])
    _rn_video(M, 'wp27-g109', [[
        'Average speed. First — what it is NOT.',
        D('Write "≠ 87.5" next to the question'),
        "It's not eighty-seven and a half, the plain average of a hundred five and seventy.",
        'Going there is faster. So it takes less time. Coming back slow takes more time.',
        'More time at seventy. So the answer sits closer to seventy. Below eighty-seven and a half.',
        D('Cross out choices 1 and 3'),
        'Ninety and eighty-seven and a half are out.',
        'Now calculate. No distance given? Pick a friendly one — something both speeds divide.',
        'Two hundred ten: a hundred five and seventy both go into it.',
        A('A trip table appears', TABLE(['Leg', 'Speed', 'Distance', 'Time'], [['There', '105', '210 km', ''], ['Back', '70', '210 km', ''], ['Total', '', '', '']], w=1000, h=210)),
        D('Fill in the times 2 and 3, then the totals 420 and 5'),
        'There: two hours. Back: three hours. In total: four hundred twenty kilometers in five hours.',
        D('Write "420 ÷ 5 = 84" and circle choice 2'),
        'Total distance over total time: eighty-four. Choice two.',
        D('Write "2 × 105 × 70 ÷ (105 + 70) = 84"'),
        'A check for strong students, for equal distances only: two times a hundred five times seventy, over a hundred seventy-five. Eighty-four again.',
    ]])

    # ---------- g111: toward each other, 1.75 times -> 4/11 (Hebrew: Danny and Dina, 1.5 -> 2/5)
    #            ==>  Maya and Theo on a bike trail, 1.25 times -> 4/9
    _rn_q(M, 'wp27-g111', 'Maya and Theo start at the same time from opposite ends of a bike trail and ride toward each other. Theo rides at 1.25 times Maya’s speed. What fraction of the trail does Maya cover before they meet?',
          ['$\\frac14$', '$\\frac49$', '$\\frac12$', '$\\frac59$'], 2, [
        'They start together and stop at the meeting: equal times. With equal times, the distances have the same ratio as the speeds.',
        'Speed ratio Maya : Theo $=1:1.25=4:5$ (multiply by $4$).',
        'The trail is $4+5=9$ parts. Maya covers $\\frac49$ of it.',
        'Check by elimination: Theo is faster, therefore Maya covers less than $\\frac12$. If Theo were twice as fast, Maya would cover $\\frac13$. Theo is slower than that, therefore Maya covers more than $\\frac13$. Only $\\frac49$ fits.'])
    _rn_video(M, 'wp27-g111', [[
        "No distance. No time. No real speeds. Just 'one point two five times'.",
        'They start together and stop when they meet. So the time is equal. Distances follow the speeds.',
        D('Write the ratio "1 : 1.25 = 4 : 5"'),
        'One to one point two five. Multiply by four: four to five.',
        A('Two bars appear: Maya 4 parts, Theo 5 parts', _vis({'type': 'bars', 'labels': ['Maya', 'Theo'], 'values': [4, 5]}, 700, 260)),
        'Maya rides four parts, Theo rides five. The whole trail: nine parts.',
        D('Write "4/9" and circle choice 2'),
        'Maya covers four out of nine. Choice two.',
    ], [
        'Ratios not your thing? Missing data — plug in friendly numbers.',
        D('Write "Maya 16 km/h, Theo 20 km/h, 1 hour"'),
        'Maya at sixteen kilometers an hour, Theo at twenty — one and a quarter times sixteen. Say they meet after one hour — the simplest.',
        'Maya rides sixteen kilometers, Theo twenty. The trail is thirty-six.',
        D('Write "16/36 = 4/9"'),
        'Sixteen out of thirty-six: four ninths — the same answer.',
    ], [
        'And the psychometric way — pure logic.',
        'Theo is faster. So Maya covers LESS than half.',
        D('Cross out choices 3 and 4'),
        'One half is out. Five ninths is more than half — out.',
        'Now imagine Theo were exactly twice as fast. Then Maya would cover one third.',
        'But Theo is only one point two five times as fast. So Maya covers MORE than a third.',
        D('Cross out choice 1 and circle choice 2'),
        'One quarter is less than a third — out. Four ninths is left.',
    ]])

    # ---------- g112: B 3.5 times as fast, B covers it all -> 2/7 (Hebrew: two planes, 2.5 -> 2/5)
    #            ==>  rowboat and motorboat on a lake, 4.5 times -> 2/9 (trap 2/11)
    _rn_q(M, 'wp27-g112', 'A rowboat and a motorboat leave opposite ends of a lake at the same time, each heading for the other end. The motorboat is 4.5 times as fast as the rowboat. By the time the motorboat reaches the far end, what fraction of the length of the lake has the rowboat traveled?',
          ['$\\frac2{11}$', '$\\frac79$', '$\\frac29$', '$\\frac9{11}$'], 3, [
        'Equal times: from the start until the motorboat arrives. Speed ratio rowboat : motorboat $=1:4.5=2:9$. Therefore in that time the ratio of their distances is also $2:9$.',
        'The whole lake is the motorboat’s $9$ parts, because the motorboat travels the full length alone. The rowboat covers $\\frac29$ of the lake.',
        'Trap: $\\frac2{11}$ adds $2+9$, as in a meeting question. Here the question does not stop at the meeting.'])
    _rn_video(M, 'wp27-g112', [[
        'Careful — this time the question does NOT stop when they meet.',
        'The motorboat travels the whole lake. The rowboat is still somewhere on the way.',
        D('Write the ratio "1 : 4.5 = 2 : 9"'),
        'Speed ratio one to four point five. Double it: two to nine.',
        'Same time. So the distances are two to nine.',
        "But the WHOLE lake is only the motorboat's nine parts. Not two plus nine.",
        D('Write "2/9" and circle choice 3'),
        'The rowboat covers two parts out of nine. Choice three.',
        'Two elevenths would be a meeting question. Here, the motorboat covers the whole length alone.',
    ], [
        'Now plug in numbers.',
        D('Write "rowboat 4 km/h, motorboat 18 km/h, 1 hour"'),
        'The rowboat at four kilometers an hour, the motorboat at eighteen — four and a half times four.',
        'The motorboat reaches the far end after one hour. So the lake is eighteen kilometers long.',
        D('Write "4/18 = 2/9"'),
        'In that hour the rowboat covers four. Four out of eighteen: two ninths.',
    ]])

    # ---------- g114: 5 + 7, 800 m -> 4 min (Hebrew: 6 + 4, 500 m -> 3 min)  ==>  runners 8 + 10, 1,800 m -> 6 min
    _rn_q(M, 'wp27-g114', 'Two runners leave the same gate at the same time and run in opposite directions along a straight path. Their speeds are 8 and 10 kph. After how many minutes are they 1,800 meters apart?',
          ['$6$', '$10$', '$54$', '$3$'], 1, [
        'Opposite directions: the gap grows at $8+10=18$ kph.',
        'Same units: $1{,}800$ m $=1.8$ km.',
        'Time $=\\frac{1.8}{18}=\\frac1{10}$ hour $=\\frac{60}{10}=6$ minutes.',
        'Traps: $\\frac1{10}$ hour is not $10$ minutes. And $54$ minutes uses $10-8=2$ kph, as if they ran in the same direction.'])
    _rn_video(M, 'wp27-g114', [[
        'Two runners, opposite directions — moving apart. Add the speeds.',
        D('Write "8 + 10 = 18 km/h"'),
        'Eight plus ten: the gap grows eighteen kilometers every hour.',
        'The distance is in meters, the speed in kilometers. Same units!',
        D('Write "1,800 m = 1.8 km"'),
        A('A distance–speed–time table appears', TABLE(['Speed', 'Distance', 'Time'], [['18 km/h', '1.8 km', '']], w=800, h=110)),
        'Time is distance over speed: one point eight over eighteen.',
        D('Write "1.8 ÷ 18 = 1/10 hour"'),
        'One tenth of an hour.',
        D('Write "60 ÷ 10 = 6 minutes" and circle choice 1'),
        'They asked for minutes. Sixty divided by ten: six minutes. Choice one.',
        'Ten is the trap — a tenth of an hour is not ten minutes.',
    ]])

    # ---------- g115: 08:00 van 60, 08:30 car 90, 105 km -> 09:00 (Hebrew: 6:00 truck 80, 6:30 car 100, 130 km -> 7:00)
    #            ==>  09:00 bus 72, 09:20 car 108, 204 km -> 10:20 (trap 10:08)
    _rn_q(M, 'wp27-g115', 'At 09:00 a bus leaves Oakton for Bayside at 72 kph. At 09:20 a car leaves Bayside for Oakton at 108 kph. The towns are 204 kilometers apart. When do they meet?',
          ['10:08', '10:20', '10:40', '10:00'], 2, [
        'From 09:00 to 09:20 only the bus moves: $20$ minutes $=\\frac13$ hour, $72\\times\\frac13=24$ km.',
        'When the car starts, the gap is $204-24=180$ km. They drive toward each other: the gap closes at $72+108=180$ kph.',
        'Time $=\\frac{180}{180}=1$ hour. They meet one hour after the car starts, at 10:20.',
        'Trap: $\\frac{204}{180}=1\\frac2{15}$ hours $=68$ minutes after 09:00 (choice 1) counts the car as driving before it left.'])
    _rn_video(M, 'wp27-g115', [[
        'Step by step. Stage one: the bus drives alone.',
        D('Write "first ⅓ hour: 72 × ⅓ = 24 km"'),
        'From nine to nine twenty, only the bus moves. Twenty minutes is a third of an hour. Seventy-two for a third of an hour: twenty-four kilometers.',
        A('The route appears: Oakton, the bus at 09:20, Bayside',
          _vis({'type': 'route', 'labels': ['Oakton', 'Bus', 'Bayside'], 'positions': [0, 24, 204], 'arrows': ['→', '→', '←']}, 1000, 210)),
        D('Write "204 − 24 = 180" over the gap'),
        'The whole distance is two hundred four. So a hundred eighty kilometers are left.',
        'Stage two: the car starts, heading toward the bus. Add the speeds — a hundred eighty.',
        D('Write "180 ÷ 180 = 1 hour"'),
        'The distance that matters is the gap between them: a hundred eighty. Over a hundred eighty: one hour.',
        D('Write "9:20 + 1 h = 10:20" and circle choice 2'),
        'One hour after nine twenty: ten twenty. Choice two.',
        'Always draw it — the sketch makes the two stages obvious.',
    ]])

    # ---------- g116: Mina 3 kph, 20 min ahead, caught after 40 min -> 4.5 (Hebrew: Miki 4 kph, 15 min, 30 min -> 6)
    #            ==>  Zoe 15 kph by bike, 12 min ahead, caught after 20 min -> 24 (trap 9 = the difference)
    _rn_q(M, 'wp27-g116', 'Zoe rides her bike from home at 15 kph. Twelve minutes later, her brother Sam leaves home along the same route and catches up with Zoe 20 minutes after he starts. What is Sam’s speed?',
          ['$9$ kph', '$20$ kph', '$24$ kph', '$18$ kph'], 3, [
        '$12$ minutes $=\\frac15$ hour. Zoe’s head start: $15\\times\\frac15=3$ km.',
        'Sam closes the $3$ km gap in $20$ minutes $=\\frac13$ hour. The gap closes at $3\\div\\frac13=3\\times3=9$ kph. This is the difference between the speeds.',
        'Sam’s speed $=15+9=24$ kph.',
        'Check: Zoe rides $12+20=32$ minutes in total: $15\\times\\frac{32}{60}=8$ km. Sam rides the same $8$ km in $\\frac13$ hour: $8\\div\\frac13=24$ kph.',
        'Trap: $9$ kph is only how much faster Sam is.'])
    _rn_video(M, 'wp27-g116', [[
        'A chase. First: how far ahead is Zoe when Sam leaves?',
        D('Write "15 × ⅕ = 3 km"'),
        'Twelve minutes is a fifth of an hour. At fifteen kilometers an hour: three kilometers ahead.',
        'Now the chase. The ONLY distance that matters: that three-kilometer gap. Not the whole way they ride.',
        A('A gap table appears', TABLE(['Gap', 'Time', 'Speed difference'], [['3 km', '⅓ hour', '']], w=900, h=110)),
        'Sam closes it in twenty minutes — one third of an hour.',
        D('Write "3 ÷ ⅓ = 3 × 3 = 9"'),
        'Three divided by one third. Dividing by a fraction is multiplying by its reciprocal: three times three — nine.',
        "Careful — that's not Sam's speed. That's how much FASTER he is than Zoe.",
        D('Write "15 + 9 = 24" and circle choice 3'),
        "Zoe's fifteen plus nine: twenty-four kilometers an hour. Choice three.",
        "At nine he'd never catch her — she's faster!",
    ], [
        'Quick check. Zoe rides twelve plus twenty minutes — thirty-two minutes.',
        'Fifteen kilometers an hour is a quarter of a kilometer every minute. Thirty-two quarters: eight kilometers.',
        'Sam covers the same eight kilometers in twenty minutes.',
        D('Write "8 ÷ ⅓ = 8 × 3 = 24"'),
        'Eight over one third: twenty-four. Same answer.',
    ]])

    # ---------- g117: 9 km in 12 min vs 12 km in 9 min -> 35 (Hebrew: 8 km / 10 min vs 10 km / 8 min -> 27)
    #            ==>  motorbike 9 km in 15 min, train 15 km in 9 min -> 36 and 100 -> 64
    #            (review 2026-10-06: was 6 km / 10 min vs 10 km / 6 min — "10 min = 1/6 h, ×6" was the Hebrew's own step)
    _rn_q(M, 'wp27-g117', 'A motorbike travels 9 kilometers in 15 minutes. A train travels 15 kilometers in 9 minutes. What is the difference between their speeds, in kph?',
          ['$46$', '$64$', '$74$', '$136$'], 2, [
        'Motorbike: $60$ minutes is $4$ times $15$ minutes. In an hour it covers $9\\times4=36$ km: $36$ kph.',
        'Train: $15$ km in $9$ minutes is $5$ km in $3$ minutes. An hour is $20$ times $3$ minutes: $5\\times20=100$ kph.',
        'Difference: $100-36=64$ kph. (Quick: $104-40=64$.)',
        'Trap: $136$ adds the speeds.'])
    _rn_video(M, 'wp27-g117', [[
        'Kilometers per hour — but the times are in minutes. Convert to hours first.',
        D('Write "15 min = 15/60 h = ¼ h"'),
        'Fifteen minutes is fifteen sixtieths of an hour — one quarter.',
        D('Write "9 ÷ ¼ = 9 × 4 = 36"'),
        'Distance over time: nine divided by one quarter. Dividing by a fraction is multiplying by its reciprocal: nine times four — thirty-six.',
        D('Write "15 ÷ 9/60 = 15 × 60/9 = 100"'),
        'The train: fifteen divided by nine sixtieths. Fifteen times sixty over nine: a hundred.',
        'Now a hundred minus thirty-six. Before any long subtraction — two quick tricks.',
        D('Write "104 − 40 = 64"'),
        'One: add four to both, to reach a round forty. A hundred four minus forty: sixty-four.',
        D('Write "36 → 40 → 100: 4 + 60 = 64"'),
        "Two: walk from thirty-six to a round anchor — forty — that's four. Then forty to a hundred — sixty. Sixty-four.",
        D('Circle choice 2'),
        'Choice two.',
    ], [
        'Now the faster way — identical ratios. This is the one I recommend.',
        A('A time–distance table appears', TABLE(['Vehicle', 'Time', 'Distance'], [['Motorbike', '15 min', '9 km'], ['Motorbike', '60 min', ''], ['Train', '9 min', '15 km'], ['Train', '60 min', '']], w=900, h=250)),
        D('Write "×4" and fill in 36'),
        'The motorbike: fifteen minutes to sixty is times four. Nine times four — thirty-six kilometers an hour.',
        D('Write "3 min → 5 km", then "×20", and fill in 100'),
        'The train: fifteen kilometers in nine minutes. Divide by three — five kilometers every three minutes. An hour is twenty of those: a hundred.',
        'A hundred minus thirty-six: sixty-four. Same answer — far less work.',
    ]])

    # ---------- g118: cable car 180 m, 12 s, double / half -> 15 (Hebrew: zip line 120 m, 10 s -> 12.5)
    #            ==>  elevator 60 m, 20 s -> 25
    _rn_q(M, 'wp27-g118', 'An elevator normally rises 60 meters in 20 seconds, at a constant speed. On one trip, it rises the first half of the way at twice its normal speed and the second half at half its normal speed. How many seconds does this trip take?',
          ['$20$', '$25$', '$10$', '$15$'], 2, [
        'At the normal speed, each half takes $\\frac{20}2=10$ seconds.',
        'First half at twice the speed: half the time, $5$ seconds. Second half at half the speed: twice the time, $20$ seconds.',
        'Total: $5+20=25$ seconds.',
        'Trap: "double, then half — they cancel" gives $20$. The two speeds apply to equal distances, not to equal times. The slow half adds $10$ seconds, and the fast half saves only $5$.'])
    _rn_video(M, 'wp27-g118', [[
        "Instinct says: double speed, then half speed — they cancel. Twenty seconds. Wrong. Let's see why.",
        D('Write "60 ÷ 20 = 3 m/s"'),
        'Normal speed: sixty meters in twenty seconds — three meters per second.',
        A('A half-by-half table appears', TABLE(['Half', 'Speed', 'Distance', 'Time'], [['First', '6 m/s', '30 m', ''], ['Second', '1.5 m/s', '30 m', '']], w=1000, h=160)),
        'Each half is thirty meters. First half at double speed: six. Second half at half speed: one point five.',
        D('Fill in the times 5 and 20, and write "= 25"'),
        'Thirty over six: five seconds. Thirty over one point five: twenty. Total: twenty-five.',
        D('Circle choice 2'),
        'Twenty-five seconds. Choice two.',
    ], [
        'Faster: ratios. Double the speed — half the time. Half the speed — double the time.',
        D('Write "10 + 10" above the question'),
        'On a normal trip, each half takes ten seconds.',
        D('Write "5 + 20 = 25" below it'),
        'First half twice as fast: five seconds. Second half half as fast: twenty. Twenty-five — with no speeds at all.',
    ], [
        'And the spark of insight.',
        'The slow half alone takes twenty seconds — the whole normal trip!',
        'Plus the fast half on top. So the answer is MORE than twenty.',
        D('Cross out choices 1, 3 and 4'),
        'Twenty, ten and fifteen are out. Only twenty-five is left.',
        'Which should you use? Ratios. The insight is great — if you happen to see it.',
    ]])

    # ---------- g119: midpoint, 24 kph vs 20 min + 18 kph -> 24 (Hebrew: 30 kph vs 30 min + 20 kph -> 60)
    #            ==>  motorcyclists, 48 kph vs 20 min + 36 kph -> x = 24, AC = 48 (trap 24 = x)
    _rn_q(M, 'wp27-g119', 'B is the midpoint of a straight road from A to C. One motorcyclist rides from A to C at 48 kph. Another takes 20 minutes from A to B, then rides from B to C at 36 kph. Their total travel times are equal. How many kilometers long is AC?',
          ['$24$', '$36$', '$48$', '$72$'], 3, [
        'Let each half be $x$ km. Then AC $=2x$.',
        'First rider: $\\frac{2x}{48}=\\frac{x}{24}$ hours. Second rider: $20$ minutes $=\\frac13$ hour, plus $\\frac{x}{36}$ hours.',
        'Equal times: $\\frac{x}{24}=\\frac13+\\frac{x}{36}$. Multiply by $72$, the smallest number that $24$, $3$ and $36$ divide: $3x=24+2x$. Therefore $x=24$.',
        'AC $=2x=48$ km. Check: $\\frac{48}{48}=1$ hour, and $\\frac13+\\frac{24}{36}=\\frac13+\\frac23=1$ hour.',
        'Faster: work back from the answers. Start with a friendly one, like $48$. Trap: $24$ is only $x$, half of the road.'])
    _rn_video(M, 'wp27-g119', [[
        'A speed–distance–time table. B is the midpoint. So call each HALF x. No x over two.',
        A('A table for both riders appears', TABLE(['Rider', 'Speed', 'Distance', 'Time'], [['First: A→C', '48', '2x', ''], ['Second: A→B', '', 'x', '20 min'], ['Second: B→C', '36', 'x', '']], w=1000, h=210)),
        D('Fill in 2x/48 and x/36, and write "20 min = ⅓ h"'),
        'First rider: two x over forty-eight. Second rider: a third of an hour, then x over thirty-six.',
        "Stay in hours — we're in kilometers per hour.",
        'The times are equal. So build the equation.',
        D('Write "2x/48 = x/24  →  x/24 = ⅓ + x/36"'),
        D('Multiply by 72: write "3x = 24 + 2x → x = 24"'),
        'Two x over forty-eight is x over twenty-four. Multiply everything by seventy-two — the smallest number that twenty-four, three and thirty-six all go into. Three x equals twenty-four plus two x. x is twenty-four.',
        D('Write "AC = 2x = 48" and circle choice 3'),
        'But x is only half the road. The whole thing: forty-eight. Choice three.',
        'Twenty-four is the trap — that is only x, half the road.',
    ], [
        'Or plug in the answers. Start with the friendliest one.',
        'Forty-eight: halves of twenty-four — easy with forty-eight and thirty-six.',
        D('Write "48 ÷ 48 = 1 h"'),
        'First rider: forty-eight kilometers at forty-eight — one hour.',
        D('Write "20 min + 24/36 h = 20 + 40 = 60 min"'),
        'Second: twenty minutes, then twenty-four kilometers at thirty-six — two thirds of an hour, forty minutes. Sixty in total. Equal!',
        'Not luck. Start with the round, friendly choice. Working back from the answers saves time in many motion questions.',
    ]])

    # ---------- g120: 1,350 km, 9 h, 80% faster -> 5 (Hebrew: train 1,600 km, 6 h, 50% faster -> 4)
    #            ==>  ferry 360 km, 12 h, 60% faster -> 7.5 (estimate 6 < t < 8)
    _rn_q(M, 'wp27-g120', 'A ferry covers a route of 360 kilometers in 12 hours. A new ferry travels 60% faster. How many hours does the new ferry take on the same route?',
          ['$6$', '$8$', '$19.2$', '$7.5$'], 4, [
        '60% faster: the new speed is $1.6$ times the old speed.',
        'Same distance: the time is divided by $1.6$. $12\\div1.6=\\frac{120}{16}=7.5$ hours.',
        'Estimate: twice as fast would take $\\frac{12}2=6$ hours. One and a half times as fast would take $12\\div1.5=8$ hours. $1.6$ is between $1.5$ and $2$. Therefore the time is between $6$ and $8$ hours: only $7.5$ fits.',
        'Trap: 60% faster does not mean 60% less time. The time is multiplied by $\\frac1{1.6}=\\frac58$. And $19.2=12\\times1.6$ multiplies instead of dividing.'])
    _rn_video(M, 'wp27-g120', [[
        D('Write "360 ÷ 12 = 30"'),
        'The old speed: three sixty over twelve — thirty kilometers an hour.',
        'Sixty percent faster. Adding sixty percent means multiplying by one point six.',
        D('Write "30 × 1.6 = 48"'),
        D('Write "360 ÷ 48 = 7.5" and circle choice 4'),
        'Three sixty at forty-eight: seven and a half hours. Choice four.',
    ], [
        'Ratios: the speed goes up — the time comes down, in the same ratio.',
        'Twice as fast — half the time. Three times as fast — a third of the time.',
        'One point six times as fast? Divide the time by one point six.',
        D('Write "12 ÷ 1.6 = 120 ÷ 16 = 7.5"'),
        'Twelve over one point six — times ten: a hundred twenty over sixteen. Seven and a half.',
    ], [
        'Now the quick estimate. If it were twice as fast — half the time: six hours.',
        D('Cross out choice 1'),
        "But it's not quite twice as fast. It takes MORE than six. Out.",
        D('Cross out choice 3'),
        'And a faster ferry taking more than twelve hours? Nineteen point two — out.',
        'Eight or seven and a half? Try one more easy speed: one and a half times as fast.',
        D('Write "12 ÷ 1.5 = 8 hours"'),
        'One and a half times as fast: twelve divided by one point five — eight hours.',
        D('Write "1.5 < 1.6 < 2  →  6 < time < 8"'),
        'One point six is faster than one point five. So the time is LESS than eight hours — and more than six.',
        D('Cross out choice 2 and circle choice 4'),
        'Eight is out. Only seven and a half is left. Choice four — and no exact division at all.',
    ]])

    # ---------- g121: circle 600 m, 30 / 24 -> 6 min (Hebrew: karts, 500 m, 60 / 50 -> 3 min)
    #            ==>  runners, 400 m track, 12 / 9 -> 8 min (fast 4 laps, slow 3 laps)
    _rn_q(M, 'wp27-g121', 'Two runners start together from the same point of a circular track, running in the same direction. The track is 400 meters long. Their speeds are 12 and 9 kph. How many minutes pass between consecutive meetings?',
          ['$2$', '$4$', '$8$', '$16$'], 3, [
        'Same direction on a circle: the faster runner gains on the slower one at $12-9=3$ kph.',
        'They meet again each time the faster one has gained one full lap: $400$ m $=0.4$ km.',
        'Time $=\\frac{0.4}{3}=\\frac2{15}$ hour $=\\frac2{15}\\times60=8$ minutes.',
        'Check with an equation: $12t=9t+0.4$. Therefore $3t=0.4$ and $t=\\frac2{15}$ hour $=8$ minutes.'])
    _rn_video(M, 'wp27-g121', [[
        "First — what do 'consecutive meetings' mean?",
        A('The track appears: 400 m, speeds 12 and 9 km/h',
          _vis({'type': 'circularMotion', 'circumference': '400 m', 'fast': '12 km/h', 'slow': '9 km/h', 'lapsFast': 4, 'lapsSlow': 3}, 1100, 300)),
        'They start together. The faster one pulls away — then chases the slower one from behind.',
        'It meets the slower one again exactly when it has gained one full lap.',
        D('Circle "1 extra lap"'),
        'Same direction — a chase. Subtract the speeds.',
        D('Write "12 − 9 = 3 km/h"'),
        'Tell the slow one: you stand still. The fast one moves at the difference — three kilometers an hour.',
        D('Write "3 km — 60 min", below it "1 km — 20 min", and below that "0.4 km — 8 min"'),
        'One lap: four hundred meters, zero point four kilometers. Three kilometers take sixty minutes — so one kilometer takes twenty. Zero point four of twenty: eight minutes.',
        D('Circle choice 3'),
        'Eight minutes. Choice three.',
    ], [
        'Want to check? Write an equation.',
        'Same time t for both. The fast one covers one extra lap: zero point four kilometers.',
        D('Write "12t = 9t + 0.4"'),
        'Twelve t equals nine t plus zero point four.',
        D('Write "3t = 0.4 → t = 2/15 h = 8 min"'),
        'Three t is zero point four. t is two fifteenths of an hour — sixty times two fifteenths: eight minutes. The same answer.',
        'On a circle, imagine one of them standing still — the other just needs one lap.',
    ]])


def rn_order(M):
    # Further guided group: the Hebrew levels say g120 (medium) before g119 (medium plus) -> easy -> hard.
    # Nothing in g120's video uses g119. renumber_guided renumbers the titles and the sidebar.
    sec = M.section_of('wp27-g120')
    assert M.section_of('wp27-g119') == sec
    M.move('wp27-g120', sec, before='wp27-g119')
    M.move('solve-wp27-g120', sec, after='wp27-g120')


def rn_practice_questions(M):
    P = {}
    # p01 cyclist: 1 lap / 2 min, 3 laps / 8 min, 24 min each -> 21  ==>  runner 1 lap / 3 min, 2 laps / 5 min, 30 min each -> 22
    P['wp27-p01'] = ('A runner completes one lap every 3 minutes at pace A, and two laps every 5 minutes at pace B. She runs for 30 minutes at each pace. How many laps does she complete in total?',
        ['16', '22', '25', '20'], 2, [
        'At pace A: $\\frac{30}{3}=10$ laps.',
        'At pace B: $30$ minutes are $\\frac{30}{5}=6$ blocks of $5$ minutes, with $2$ laps in each: $6\\times2=12$ laps.',
        'Total: $10+12=22$ laps.',
        'Trap: $10+6=16$ counts only one lap in each block of $5$ minutes.'])
    # p02 ferry d km in t h, 3x speed, 2t h -> 6d  ==>  bus a km in b h, 2x speed, 4b h -> 8a
    P['wp27-p02'] = ('A bus travels $a$ kilometers in $b$ hours. At twice that speed, how many kilometers does it travel in $4b$ hours?',
        ['$2a$', '$6a$', '$\\frac{a}{2}$', '$8a$'], 4, [
        'Speed $=\\frac{a}{b}$. Twice that speed: $\\frac{2a}{b}$.',
        'Distance $=\\frac{2a}{b}\\cdot4b=8a$.',
        'Or plug in numbers: $a=10$, $b=1$. The speed is $10$, the new speed $20$, and in $4$ hours the bus travels $80=8\\cdot10$.',
        'Method 2 · The V in motion: table Speed · Distance · Time, rows $(1, a, b)$ and $(2, ?, 4b)$. The blank is in the middle → upside-down V: $?=\\frac{2\\cdot4b\\cdot a}{1\\cdot b}=8a$.'])
    # p03 robot x h at 2x, y h at 3y -> 2x^2 + 3y^2  ==>  drone a h at 3a, b h at 4b -> 3a^2 + 4b^2
    P['wp27-p03'] = ('A drone flies for $a$ hours at $3a$ kph, and then for $b$ hours at $4b$ kph. What is its total distance, in kilometers?',
        ['$3a+4b$', '$3a^2+4b^2$', '$7(a+b)$', '$(3a+4b)^2$'], 2, [
        'First part: $a\\cdot3a=3a^2$. Second part: $b\\cdot4b=4b^2$. Total: $3a^2+4b^2$.',
        'Or plug in numbers: $a=2$, $b=1$. The drone flies $2\\cdot6=12$ km and then $1\\cdot4=4$ km: $16$ km. Only $3a^2+4b^2=12+4=16$ fits (the others give $10$, $21$ and $100$).',
        'Do not choose $a=1$ and $b=1$: then two choices both give $7$.'])
    # p04 bus 64 kph x 3 h, +48 km, 80 kph -> 3  ==>  train 75 kph x 4 h, +60 km, 90 kph -> 4
    P['wp27-p04'] = ('A train travels from A to B at 75 kph for 4 hours. The route from B to C is 60 km longer than the route from A to B. How many hours does the trip from B to C take at 90 kph?',
        ['$3\\frac13$', '$4.5$', '$4$', '$5$'], 3, [
        'A to B: $75\\times4=300$ km.',
        'B to C: $300+60=360$ km.',
        'Time: $\\frac{360}{90}=4$ hours.',
        'Trap: $\\frac{300}{90}=3\\frac13$ forgets the extra $60$ km.'])
    # p05 taxi 72 kph in 1 h 20 min, back at 48 -> 2 h  ==>  cyclist 20 kph in 1 h 40 min, back at 16 -> 2 h 5 min
    P['wp27-p05'] = ('A cyclist rides from home to a lake at 20 kph in 1 hour 40 minutes. She returns along the same route at 16 kph. How long does the return take?',
        ['1 hour 20 minutes', '1 hour 50 minutes', '2 hours 5 minutes', '2 hours 30 minutes'], 3, [
        '$1$ hour $40$ minutes $=100$ minutes.',
        'Same distance: the times flip. The speed ratio is $20:16=5:4$, therefore the ratio of the times is $4:5$.',
        'Return time: $100\\times\\frac54=125$ minutes $=2$ hours $5$ minutes.',
        'Trap: $100\\times\\frac45=80$ minutes ($1$ hour $20$ minutes) does not flip the ratio.'])
    # p06 4 h at 1.6x -> 2 h 30 min  ==>  6 h at 1.6x -> 3 h 45 min
    P['wp27-p06'] = ('A truck trip takes 6 hours at a constant speed. How long would the same trip take at 1.6 times that speed?',
        ['3 hours 36 minutes', '9 hours 36 minutes', '3 hours 45 minutes', '4 hours'], 3, [
        'Same distance: the time is divided by $1.6$.',
        '$6\\div1.6=\\frac{60}{16}=3.75$ hours $=3$ hours $45$ minutes ($0.75$ hour $=45$ minutes).',
        'Traps: $3$ hours $36$ minutes is $3.6$ hours, not $3.75$. And $9$ hours $36$ minutes $=6\\times1.6$ multiplies instead of dividing.'])
    # p07 cyclists 12 / 30, gap 9 km -> 30 min  ==>  truck 75, police car 100, gap 5 km -> 12 min
    P['wp27-p07'] = ('A police car chases a truck along a straight highway. The truck drives at 75 kph, and the police car at 100 kph. At the start, the gap between them is 5 km. How long does it take the police car to catch up?',
        ['3 minutes', '12 minutes', '20 minutes', '1 hour'], 2, [
        'A chase: the gap closes at $100-75=25$ kph.',
        'Time $=\\frac{5}{25}=\\frac15$ hour $=12$ minutes.',
        'Trap: $\\frac{5}{100}$ hour $=3$ minutes ignores the speed of the truck.'])
    # p08 walker 08:00-11:00 at 4, other at 6 -> 09:00  ==>  cyclist 07:00-09:00 at 15, other at 20 -> 07:30
    P['wp27-p08'] = ('A cyclist leaves at 07:00, rides at 15 kph, and arrives at 09:00. Another cyclist rides the same route at 20 kph. When should the second cyclist leave to arrive at 09:00?',
        ['07:20', '07:45', '07:30', '08:00'], 3, [
        'From 07:00 to 09:00 is $2$ hours. The route: $15\\times2=30$ km.',
        'At $20$ kph: $\\frac{30}{20}=1.5$ hours.',
        'The second cyclist leaves $1.5$ hours before 09:00, at 07:30.'])
    # p09 van 360: 120 at 60, 1/4 of rest at 120, rest at 30 -> 8.5  ==>  bus 400: 100 at 50, 1/3 of rest at 100, rest at 40 -> 8
    P['wp27-p09'] = ('A bus travels 400 km. It covers the first 100 km at 50 kph, then one third of the remaining distance at 100 kph, and the rest at 40 kph. How many hours does the whole trip take?',
        ['7', '9', '8', '7.5'], 3, [
        'First part: $\\frac{100}{50}=2$ hours.',
        'Remaining: $400-100=300$ km. One third of it: $\\frac{300}{3}=100$ km at $100$ kph, $1$ hour.',
        'The rest: $300-100=200$ km at $40$ kph, $\\frac{200}{40}=5$ hours.',
        'Total: $2+1+5=8$ hours.'])
    # p11 buses 180 km, 15 kph faster -> cannot  ==>  trains 240 km, 20 kph faster -> cannot
    P['wp27-p11'] = ('Two trains start together and travel the same route of 240 km. Train A is 20 kph faster than train B. How much earlier does train A arrive?',
        ['20 minutes', '40 minutes', '1 hour', 'It cannot be determined from the information given.'], 4, [
        'Plug in two pairs of speeds that differ by $20$ kph.',
        'Speeds $60$ and $40$: times $\\frac{240}{60}=4$ and $\\frac{240}{40}=6$ hours. A arrives $2$ hours earlier.',
        'Speeds $120$ and $100$: times $\\frac{240}{120}=2$ and $\\frac{240}{100}=2.4$ hours. A arrives $0.4$ hour $=24$ minutes earlier.',
        'Two different answers: it cannot be determined.'])
    # p12 swimmer 1.8 / 2.4 km, 60 m/min, evening half -> 110  ==>  rower 1.5 / 2.4 km, 150 m/min, evening half -> 42
    P['wp27-p12'] = ('A rower covers 1.5 km each morning and 2.4 km each evening. Her morning speed is 150 meters per minute; her evening speed is half as great. How many minutes does she row in a day?',
        ['26', '42', '36', '52'], 2, [
        'Morning: $1.5$ km $=1{,}500$ m at $150$ m per minute: $\\frac{1{,}500}{150}=10$ minutes.',
        'Evening speed: $\\frac{150}{2}=75$ m per minute. $2{,}400$ m take $\\frac{2{,}400}{75}=32$ minutes.',
        'Total: $10+32=42$ minutes.',
        'Method 2 · Compare by factors, evening against morning: distance $\\times\\frac{2.4}{1.5}=\\frac85$ (same way); speed $\\times\\frac12$ (opposite → flip to $2$). Evening: $10\\cdot\\frac85\\cdot2=32$ minutes, and $10+32=42$.'])
    # p13 signal 2e8 m/s x 3e-9 s -> 0.6 m  ==>  light 3e8 m/s x 4e-9 s -> 1.2 m
    P['wp27-p13'] = ('Light travels through the air at $300{,}000{,}000$ meters per second. How far does it travel in $4\\times10^{-9}$ seconds?',
        ['12 meters', '1.2 meters', '0.12 meter', '120 meters'], 2, [
        '$300{,}000{,}000=3\\times10^8$.',
        'Distance $=3\\times10^8\\cdot4\\times10^{-9}=12\\times10^{-1}=1.2$ meters.'])
    # p14 3 km circle, 15 / 9 -> 30 min  ==>  2 km circular road, 28 / 20 -> 15 min
    P['wp27-p14'] = ('Two cyclists start together and ride in the same direction on a circular road 2 km long. Their speeds are 28 and 20 kph. After how many minutes does the faster rider first lap the slower one?',
        ['6', '2.5', '15', '30'], 3, [
        'Lapping means gaining one full lap: $2$ kilometers.',
        'The gain rate is $28-20=8$ kph.',
        '$2$ kilometers at that rate take $\\frac28=\\frac14$ hour $=15$ minutes.',
        'Trap: $\\frac{2}{48}$ hour $=2.5$ minutes adds the speeds, as if they rode in opposite directions.'])
    # p15 vans 90 / 60, stop at 180 km for 1.5 h -> 3  ==>  trucks 80 / 60, stop at 240 km for 2 h -> 4
    P['wp27-p15'] = ('Two trucks leave the same depot together and drive along the same road. One drives at 80 kph, the other at 60 kph. When the faster truck has driven 240 km, it stops for 2 hours. How many hours after they leave does the slower truck reach the stopped truck?',
        ['3', '5', '4', '6'], 3, [
        'The faster truck reaches $240$ km after $\\frac{240}{80}=3$ hours. It stays there until $3+2=5$ hours.',
        'The slower truck reaches $240$ km after $\\frac{240}{60}=4$ hours.',
        '$4$ hours is before $5$ hours: the faster truck is still stopped. The answer is $4$ hours.'])
    # p16 road 140, 08:00 / 09:00, meet 30 km from B -> 80  ==>  road 170, 07:00 / 08:00, meet 50 km from B -> 70
    P['wp27-p16'] = ('A road from A to B is 170 km long. At 07:00 a car leaves A toward B. At 08:00 another car leaves B toward A at the same speed. They meet 50 km from B. What is their common speed, in kph?',
        ['50', '60', '70', '85'], 3, [
        'The second car drives $50$ km. The first drives $170-50=120$ km.',
        'Same speed, but the first car drove $1$ hour longer. That extra hour gave it $120-50=70$ km more.',
        'Therefore the speed is $70$ kph.',
        'Or work back from the answers: at $70$ kph, the first car drives $70$ km by 08:00. The gap is $100$ km, closed at $140$ kph in $\\frac{100}{140}=\\frac57$ hour. The second car drives $70\\times\\frac57=50$ km. It fits.'])
    # p17 D in 4 h, halves at v and 3v -> 6  ==>  D in 5 h, halves at v and 4v -> 8
    P['wp27-p17'] = ('A train travels a distance $D$ in 5 hours. It covers half of the distance at speed $v$ and the other half at speed $4v$. How many hours would the whole distance take at speed $v$?',
        ['10', '8', '7', '6'], 2, [
        'Let $T$ be the time for the whole distance at speed $v$. The first half, at speed $v$, takes $\\frac{T}{2}$.',
        'The second half at four times the speed takes a quarter of that: $\\frac{T}{8}$.',
        '$\\frac{T}{2}+\\frac{T}{8}=\\frac{4T+T}{8}=\\frac{5T}{8}=5$. Therefore $T=8$ hours.',
        'Or work back from the answers: $T=8$ gives $4+1=5$ hours.'])
    # p18 robot 40 jumps / min at 18 kph -> 7.5 m  ==>  horse 120 strides / min at 36 kph -> 5 m
    P['wp27-p18'] = ('A horse takes 120 equal strides per minute and moves at 36 kph. How long is each stride?',
        ['3 meters', '5 meters', '6 meters', '0.3 meter'], 2, [
        '$36$ kph means $36{,}000$ m in $60$ minutes: $\\frac{36{,}000}{60}=600$ m per minute.',
        'Each stride: $\\frac{600}{120}=5$ m.',
        'Trap: $\\frac{36}{120}=0.3$ forgets to change the units.'])
    # p19 500 m track, 3,750 m each, opposite, same speed -> 15  ==>  cyclists, 400 m, 2,600 m each -> 13
    P['wp27-p19'] = ('Two cyclists start together from the same point of a circular track 400 meters long. They ride in opposite directions at the same speed, and each rides exactly 2,600 meters. How many times do they meet after the start? (Count a meeting at the finish, if there is one.)',
        ['12', '26', '13', '6'], 3, [
        'Opposite directions: they meet each time their total distance grows by one lap, $400$ m.',
        'Together they ride $2\\times2{,}600=5{,}200$ m. $\\frac{5{,}200}{400}=13$ meetings.',
        'The $13$th meeting happens exactly at the finish, and it counts: $13$.',
        'Traps: $12$ forgets the meeting at the finish; $6$ counts the laps of one cyclist ($\\frac{2{,}600}{400}=6.5$).'])
    # p20 walkers 10:00 at 6 / 9, halfway at 10:45 -> 15  ==>  cyclists 14:00 at 16 / 24, halfway at 15:30 -> 30
    P['wp27-p20'] = ('At 14:00, a cyclist leaves A toward B at 16 kph. A second cyclist leaves B later at 24 kph. They meet halfway between A and B at 15:30. How many minutes later did the second cyclist start?',
        ['20', '30', '45', '60'], 2, [
        'The first cyclist rides from 14:00 to 15:30: $1.5$ hours. Distance: $16\\times1.5=24$ km, half of the road.',
        'The second cyclist also covers $24$ km, at $24$ kph: $\\frac{24}{24}=1$ hour.',
        'The second cyclist started $1$ hour before 15:30, at 14:30: $30$ minutes after the first.'])
    # September item q-r26-t27-21: 2 h at 60 + 2 h at 90 -> 75 was the Average Speed lesson's own example -> new numbers
    P['q-r26-t27-21'] = ('A car drives for 2 hours at 70 kph and then for 2 more hours at 30 kph. What is its average speed for the whole trip, in kph?',
        ['$42$', '$50$', '$45$', '$56$'], 2, [
        'Total distance: $2\\times70+2\\times30=140+60=200$ km, in $4$ hours.',
        'Average speed $=\\frac{200}{4}=50$ kph.',
        'Equal times, therefore the plain average of $70$ and $30$ is right. Trap: $42=\\frac{2\\cdot70\\cdot30}{100}$ is for equal distances.'])
    for qid, (stem, ch, k, ex) in P.items():
        _rn_q(M, qid, stem, ch, k, ex)
    # wp27-p21 (removed, a copy of Q3) carried the "percent shares as weights" line: it moves to q-r26-t27-22
    _pm_add(M, 'q-r26-t27-22', [r'Method 2 · Percent shares as weights (the weights are the hours): $1$ of the $2$ hours ($50\%$) at each speed. Average $=30+0.5\cdot30=45$ kph.'])


RN_REMOVE = [
    'wp27-p23', 'wp27-p21',                    # copies (practice_audit/copies_by_topic.txt): p23 = Q1 (m/s for 25 min), p21 = Q3 (there and back)
    'wp27-p25', 'wp27-p26',                    # extra warm-ups beyond 3 (p25 = the Q15 train idea, p26 = the Q9 head-start chase)
    'q-r26-t27-15', 'q-r26-t27-16',            # September: speed change -> time (Hebrew p05, p06)
    'q-r26-t27-17', 'q-r26-t27-18',            # September: letters (Hebrew p02, p03)
    'q-r26-t27-23', 'q-r26-t27-12',            # September: circular track (Hebrew p14, p19)
    'q-r26-t27-11',                            # September: river current (kept: p24 warm-up, q-r26-t27-10)
]
RN_ORDER = ['wp27-p13', 'wp27-p18', 'wp27-p01', 'wp27-p04', 'wp27-p27', 'wp27-p22', 'wp27-p12', 'wp27-p08', 'wp27-p09',
            'wp27-p05', 'wp27-p06', 'wp27-p07', 'wp27-p11', 'wp27-p20', 'q-r26-t27-21', 'q-r26-t27-22', 'wp27-p24',
            'wp27-p14', 'wp27-p15', 'wp27-p16', 'wp27-p02', 'wp27-p03', 'q-r26-t27-10', 'wp27-p19', 'wp27-p17',
            'q-r26-t27-09']


def rn_practice(M):
    sec = 'wp27-practice'
    for qid in RN_REMOVE:
        assert M.section_of(qid) == sec, qid
        M.unplace(qid)
    left = [f['ref'] for f in M.D['flow'] if f['section'] == sec and f['type'] == 'question']
    assert sorted(left) == sorted(RN_ORDER), (sorted(set(left) ^ set(RN_ORDER)))
    M.practice_order(sec, RN_ORDER)


def rn_tidy(M):
    for vid, v in M.D['videos'].items():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            qs = [it for it in b['items'][:b['pre']] if it.get('k') == 'q']
            if b['mode'] == 'question' and qs:
                qid = qs[0]['qid']
                sb = v.get('hybrid', {}).get('sidebar', [])
                lab = sb[b['active']] if 0 <= b['active'] < len(sb) else b['title']
                b['loads'] = 'Sidebar with "%s" highlighted; the items listed are already on the canvas.' % lab
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, rich_plain(M.q(qid)['stemRich']))
        if v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = rich_plain(M.q(v['questionId'])['stemRich'])
        M.touched_videos.add(vid)


def rn_visuals(M):
    """Review 2026-10-06: the questions' stored solutionVisual data still had the old numbers / names."""
    V = {
        'wp27-g108': {'type': 'rightTriangle', 'base': '1.5 km', 'height': '0.8 km', 'hypotenuse': '1.7 km'},
        'wp27-g109': {'type': 'table', 'headers': ['Leg', 'Distance', 'Speed', 'Time'],
                      'rows': [['Outward', '210 km', '105 kph', '2 hours'], ['Return', '210 km', '70 kph', '3 hours'],
                               ['Total', '420 km', '', '5 hours']]},
        'wp27-g111': {'type': 'bars', 'labels': ['Maya', 'Theo'], 'values': [4, 5]},
        'wp27-g115': {'type': 'route', 'labels': ['Oakton', 'Bus', 'Bayside'], 'positions': [0, 24, 204],
                      'arrows': ['→', '→', '←']},
        'wp27-g118': {'type': 'table', 'headers': ['Half', 'Normal time', 'Speed multiplier', 'Actual time'],
                      'rows': [['First', '10 seconds', '2', '5 seconds'], ['Second', '10 seconds', 'one half', '20 seconds']]},
        'wp27-g119': {'type': 'route', 'labels': ['A', 'B · midpoint', 'C'], 'positions': [0, 24, 48]},
        'wp27-g121': {'type': 'circularMotion', 'circumference': '400 m', 'fast': '12 kph', 'slow': '9 kph',
                      'lapsFast': 4, 'lapsSlow': 3},
        'wp27-p09': {'type': 'table', 'headers': ['Stage', 'Distance (km)', 'Speed (kph)', 'Time (hours)'],
                     'rows': [['1', '100', '50', '2'], ['2', '100', '100', '1'], ['3', '200', '40', '5']]},
    }
    for qid, vis in V.items():
        if qid in RN_RECORDED: continue
        q = M.q(qid)
        assert q.get('solutionVisual'), qid
        q['solutionVisual'] = vis


def renumber_pass(M):
    rn_lessons(M)
    rn_guided(M)
    rn_order(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_visuals(M)
    rn_tidy(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-07 methods spread (runs last)
# The 2026-10-06 exam methods, shown wherever they genuinely help: one extra written line on the question
# (guided or practice; existing lines kept), and on the clearest guided videos one extra "Method N" slide.
# Nothing in topics 21-29 is recorded (checked ~/Documents/Course.recordings 2026-10-07).
# ======================================================================================================
SPREAD_RECORDED = set()


def _sp_line(M, qid, line):
    """Append one method line to a question's written solution (existing lines kept)."""
    ex = list(M.q(qid).get("explanation") or [])
    if line in ex: return
    M.set_q(qid, expl=ex + [line])


def _sp_slide(M, qid, after_n, title, script):
    """One extra method slide in the guided solution video of qid, after slide after_n. Sidebar unchanged."""
    vid = "solve-" + qid
    if vid in SPREAD_RECORDED: return
    assert M.video(vid)["questionId"] == qid, vid
    act = M.slide(vid, 2)["active"]
    M.insert_slides(vid, after_n, [dict(mode="question", active=act, title=title, pre=[Q(qid)], script=script)])


def spread_methods(M):
    # ---- Q3 average speed: percent shares as weights (the times flip) - line + slide ----
    qid = 'wp27-g109'
    _sp_line(M, qid, r'Method 2 · Percent shares as weights (the weights are the hours): same distance, therefore the times flip. The speed ratio is $105:70=3:2$, and the time ratio is $2:3$. So $\frac25$ of the time is at $105$: average $=70+\frac25\cdot35=70+14=84$ kph.')
    vid = 'solve-' + qid
    M.slide(vid, 2)['title'] = 'Method 1 · Logic, then a table'
    _sp_slide(M, qid, 2, 'Method 2 · Shares as weights', [
        'Another way, with no distance at all. The hours are the weights.',
        A("'Same distance → the times flip: time ratio 2 : 3' appears", T(r'Same distance $\to$ the times flip: time ratio $2:3$', size=40, gap=40)),
        'Same road both ways, so the times flip. Speeds three to two — times two to three.',
        A("'70 + 2/5 · 35 = 84' appears", T(r'$\frac25$ of the time at $105$: $\ 70+\frac25\cdot35=70+14=84$', size=40, gap=40)),
        'Two fifths of the time is at a hundred five. Start at seventy and move two fifths of the gap of thirty-five: fourteen.',
        D('Circle choice 2'),
        'Eighty-four. Choice two.'])

    # ---- Q19 letters in the choices: power count with units - line + slide ----
    qid = 'q-r26-t27-06'
    _sp_line(M, qid, r'Method 3 · Power count with units: $k$ and $d$ are kilometers, $t$ is hours, and the answer is a time. Choice 2 gives $\frac{1}{\text{hours}}$ and choice 4 gives $\frac{\text{km}^2}{\text{hours}}$: both are out. Minutes are $60$ times the hours, therefore the $60$ goes on top: choice 3.')
    _sp_slide(M, qid, 3, 'Method 3 · Power count with units', [
        'One more check, with no numbers: count the units.',
        A("'k, d: km · t: hours · the answer is a time' appears", T(r'$k$, $d$: km $\ \cdot\ $ $t$: hours $\ \cdot\ $ the answer is a time', size=40, gap=40)),
        'k and d are kilometers, t is hours. The answer is a time — so the kilometers must cancel.',
        A("'(2) 1/hours ✗ · (4) km²/hours ✗' appears", T(r'(2) $\frac{1}{\text{hours}}$ ✗ $\quad$ (4) $\frac{\text{km}^2}{\text{hours}}$ ✗', size=40, gap=40)),
        D('Cross out choices 2 and 4'),
        'Choice two gives one over hours. Choice four gives kilometers squared over hours. Not times — out.',
        A("'minutes = hours × 60 → 60 on top' appears", T(r'minutes $=$ hours $\times60$ $\to$ $60$ on top', size=40, gap=40)),
        'Choices one and three are both times. Minutes are sixty times the hours, so the sixty goes on top.',
        D('Circle choice 3'),
        'Choice three.'])

    # ---- practice: written lines only ----
    _sp_line(M, 'wp27-p08', r'Method 2 · Compare by factors: the same route, and the speed is $\times\frac{20}{15}=\frac43$. Time goes the opposite way → flip to $\frac34$: $2\cdot\frac34=1.5$ hours. $1.5$ hours before 09:00 is 07:30.')
    _sp_line(M, 'wp27-p03', r'Method 2 · Power count: each part is hours $\times$ speed, $a\cdot3a$ and $b\cdot4b$, power $2$. Choices 1 and 3 have power $1$: out. Choice 4 opens to $9a^2+24ab+16b^2$, not $3a^2+4b^2$: choice 2.')


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


# =====================================================================================
# 2026-10-07 method names: the method slides of this topic's unrecorded videos ("Method N · X") and the written
# solutions' "Method N · / Shortcut ·" labels use ONE short vocabulary (thinking methods of topic 51 + named
# techniques). Data and rules: _method_names.py (a video recorded before its CUTOFF keeps its old titles).
def _mn_load():
    import importlib.util, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_method_names.py')
    spec = importlib.util.spec_from_file_location('_method_names', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m


_apply_before_method_names = apply


def apply(M):
    _apply_before_method_names(M)
    _mn_load().method_names(M, 27)   # 2026-10-07 method names: runs last
