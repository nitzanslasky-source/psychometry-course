"""Topic 26 - Work and rates. Course review 2026-09 fixes.
See t26_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q

TOPIC = 26
# Sidebars use the OLD question numbers; renumber_guided() maps them to the final order.
# New guided questions get 12, 13, 14 (learn section) and 15 (advanced section), in creation order.
LEARN_SB = ['Question %d' % n for n in (1, 2, 3, 4, 5, 12, 13, 14)]
ADV_SB = ['Question %d' % n for n in (6, 7, 8, 9, 10, 11, 15)]


def TABLE(headers, rows, h=170):
    return dict(k='vis', v={'type': 'table', 'headers': headers, 'rows': rows}, w=720, h=h)


def _solution(M, qid, intro, slides, learn=True):
    n = M.next_question_number(TOPIC)
    sb = LEARN_SB if learn else ADV_SB
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for sl in slides:
        title, script = sl[0], sl[1]
        pre = sl[2] if len(sl) > 2 else [Q(qid)]
        beats.append(dict(mode='question', active=sb.index('Question %d' % n), title=title, pre=pre, script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Work & Rate Questions', sb, beats, M.section_of(qid), kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Work & Rate Questions' if learn else 'Advanced Work & Rate'
    v['hybrid']['num'] = 33 if learn else 37
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _fix_draw(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _fix_say(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = l['say'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _rename_title(M, vid, title):
    v = M.video(vid)
    v['title'] = v['navLabel'] = title
    v.setdefault('hybrid', {})['title'] = title
    b = v['beats'][0]
    b['title'] = title
    b['bigTitle'] = title


def apply(M):
    S = M.set_q
    # =====================================================================================
    # 1. Lesson "Work, Rate and Time" (wp-092)
    # =====================================================================================
    L1 = 'wp-092'
    _fix_draw(M, L1, 2, 'work : rate', 'work ÷ rate')
    _fix_draw(M, L1, 2, 'work : time', 'work ÷ time')
    _fix_draw(M, L1, 3, 'rate = 18 : 3', 'rate = 18 ÷ 3')
    _fix_draw(M, L1, 4, '"42 : 7 = 6 per minute" and "42 : 6 = 7 minutes"', '"42 ÷ 7 = 6 per minute" and "42 ÷ 6 = 7 minutes"')
    _fix_say(M, L1, 6, 'Fractions feel awkward? Pick a convenient job size instead — forty units: eight per hour and five per hour. Same relationship.',
             'Fractions feel awkward? Pick a job size that both times divide — the LCM. Five and eight: forty units. Eight units per hour and five units per hour. Same relationship, no fractions.')
    # new slide 6: rate changes by a percent
    M.insert_slides(L1, 5, [dict(mode='concept', active=4, title='Rate in percent', script=[
        "Exam questions love percents here.",
        "The rate goes up by twenty-five percent. The job is the same. What happens to the time?",
        A("'Rate × 5/4 → time × 4/5' appears", T('Work fixed: rate $\\times\\frac54$ $\\to$ time $\\times\\frac45$', size=44, gap=60)),
        "Twenty-five percent more means times five quarters.",
        "Work fixed — that's inverse. So flip the fraction: the time is times four fifths.",
        D('Write "4/5 = 80% → time −20%"'),
        "Four fifths is eighty percent. The time drops by twenty percent. Not twenty-five!",
        A("'Rate +25% → time −20%' appears", T('Rate $+25\\%$ $\\to$ time $-20\\%$', size=44, gap=60)),
        "The rule: turn the percent into a fraction. Flip it. Multiply the time.",
        A("'Rate −20% → time +25%' appears", T('Rate $-20\\%$ $\\to$ rate $\\times\\frac45$ $\\to$ time $\\times\\frac54$ $=+25\\%$', size=44, gap=60)),
        "It works the other way too. Rate down twenty percent: times four fifths. Time times five quarters — up twenty-five percent.",
    ])])
    M.set_slide(L1, 7, active=5)
    M.set_slide(L1, 8, active=6, script=[
        "Let's lock it in.",
        A("'Rate × Time = Work' appears", T('Rate $\\times$ Time $=$ Work', size=46)),
        A("'Rate = work in ONE time unit' appears", T('Rate = work in ONE time unit — always a fraction', size=42)),
        A("'Direct / inverse' appears", T('Time or rate fixed $\\to$ direct · Work fixed $\\to$ inverse', size=42)),
        A("'Rate in percent' appears", T('Rate in percent: fraction, flip it, multiply the time', size=42)),
        D('Underline "inverse"'),
        "Next: two questions. Try each one first — then watch the solution.",
    ])
    M.set_sidebar(L1, ['The formula', 'Rate has a time unit', 'Work = rate × time', 'Three relationships',
                       'Rate in percent', 'One job = 1', 'Recap'])

    # =====================================================================================
    # 2. Lesson "Working Together" (wp-094): two-worker shortcut + sense check
    # =====================================================================================
    L2 = 'wp-094'
    M.insert_slides(L2, 4, [
        dict(mode='concept', active=3, title='Two-worker shortcut', script=[
            "A shortcut for exactly two workers.",
            A("'Together time = ab/(a+b)' appears", T('Two workers: together time $=\\frac{a\\cdot b}{a+b}$', size=48, gap=60)),
            "a and b are the times each one needs alone.",
            "Times over plus. Multiply the two times, divide by their sum.",
            D('Write "4 h and 6 h → (4 · 6)/(4 + 6) = 24/10 = 2.4 h"'),
            "Four hours and six hours: twenty-four over ten. Two point four hours.",
            A("'Two equal workers → half the time' appears", T('Two equal workers $\\to$ half the time', size=44, gap=60)),
            "And when both need the same time — together they need half of it.",
            "Careful: the shortcut is for two workers only. Three workers? Add the rates.",
        ]),
        dict(mode='concept', active=4, title='Sense check', script=[
            "Before you calculate — know where the answer must be.",
            A("'Together < fastest alone' appears", T('Together $<$ the fastest one alone', size=46, gap=60)),
            "Help never slows you down. Together is faster than the fastest worker alone.",
            A("'Together ≥ fastest ÷ 2' appears", T('Together $\\ge$ the fastest time $\\div 2$', size=46, gap=60)),
            "Two workers as fast as the fastest one would need half the time.",
            "The partner is slower — so together is more than that half. Exactly half only if they are equally fast.",
            D('Write "4 h and 6 h → between 2 h and 4 h"'),
            "Four and six: the answer is between two and four hours. Two point four — it fits.",
            "On the exam, use this first. Cross out every choice outside the range. Often only one is left.",
        ]),
    ])
    M.set_slide(L2, 7, active=5, script=[
        "Let's lock it in.",
        A("'Together → add the rates' appears", T('Together $\\to$ add the rates', size=44)),
        A("'Working against → subtract' appears", T('Working against $\\to$ subtract its rate', size=44)),
        A("'Different times' appears", T('Nice common multiple $\\to$ equalize times · otherwise fractions', size=40)),
        A("'Two workers: ab/(a+b)' appears", T('Two workers: $\\frac{ab}{a+b}$ · check the range first', size=44)),
        D('Tick each line'),
        "Three questions next. Try each one first.",
    ])
    M.set_sidebar(L2, ['Add the rates', 'Working against you', 'Match the times', 'Two-worker shortcut', 'Sense check', 'Recap'])

    # =====================================================================================
    # 3. Lesson "Team Questions" (wp-097): clearer memory line
    # =====================================================================================
    M.edit_lines('wp-097', 4, lambda ls: [
        {'say': "Easy to remember: work ALWAYS sits in the middle — Team, Work, Time."}
        if 'Team questions need more time' in l.get('say', '') else l for l in ls])
    M.edit_lines('wp-097', 4, lambda ls: [
        dict(l, say="Then two ways to solve: ratios — or the V method. You'll see both, with the general V rule, in the next question.")
        if 'Then two ways to solve' in l.get('say', '') else l for l in ls])

    # =====================================================================================
    # 4. Lesson "Work Time" -> "Worker-Hours" (wp-099): one name; joins/leaves; average rate
    # =====================================================================================
    L4 = 'wp-099'
    _rename_title(M, L4, 'Worker-Hours')
    M.set_slide(L4, 1, title='Worker-Hours', script=[
        "The last type: worker-hours.",
        "A small twist on team questions.",
    ])
    M.set_slide(L4, 2, title='What worker-hours are', script=[
        A("'Worker-hours = workers × hours' appears", T('Worker-hours $=$ workers $\\times$ hours', size=46, gap=70)),
        "Worker-hours measure the size of the job.",
        "Three workers, each working four hours.",
        D('Write "3 × 4 = 12 worker-hours"'),
        "Only four hours pass on the clock. But there are twelve hours of work in there.",
        "So one worker alone would need twelve hours.",
        "Think like the boss paying salaries: you pay every worker, for every hour.",
        "With days instead of hours, it's worker-days. Same idea.",
    ])
    M.insert_slides(L4, 3, [
        dict(mode='concept', active=2, title='Joins or leaves', script=[
            "The classic exam twist: someone joins or leaves in the middle.",
            A("'Whole job − done = left' appears", T('Whole job $-$ done so far $=$ left', size=46, gap=60)),
            A("'Eight workers, 15 days; after 5 days, 3 leave' appears", T('8 workers need 15 days. After 5 days, 3 leave.', size=42, gap=60)),
            "Identical workers? Count worker-days.",
            D('Write "whole job: 8 × 15 = 120 worker-days"'),
            "The whole job: eight times fifteen — a hundred twenty worker-days.",
            D('Write "done: 8 × 5 = 40 → left: 120 − 40 = 80"'),
            "Done in five days: forty. Left: eighty.",
            D('Write "80 ÷ 5 workers = 16 more days"'),
            "Five workers stay. Eighty divided by five: sixteen more days.",
            "Workers with different rates? Pick a job size — the LCM of their times — and do the same three steps. Next question.",
            "And read the question: do they want the days that are LEFT, or the whole job from the start?",
        ]),
        dict(mode='concept', active=3, title='Average rate', script=[
            "One more trap. The average rate over two jobs.",
            A("'Average rate = total work ÷ total time' appears", T('Average rate $=\\frac{\\text{total work}}{\\text{total time}}$', size=48, gap=60)),
            A("'60 pages at 20 per hour, then 60 pages at 60 per hour' appears", T('60 pages at 20 per hour, then 60 pages at 60 per hour', size=40, gap=60)),
            D('Write "60 ÷ 20 = 3 h · 60 ÷ 60 = 1 h"'),
            "Three hours for the first part. One hour for the second.",
            D('Write "120 pages ÷ 4 h = 30 per hour"'),
            "A hundred twenty pages in four hours: thirty per hour.",
            D('Write "not (20 + 60) ÷ 2 = 40"'),
            "Not forty! The worker spent more time at the slow rate — so the average is closer to the slow rate.",
            "This is a weighted average, weighted by TIME. You'll meet the same trap in motion questions, with average speed.",
        ]),
    ])
    M.set_slide(L4, 6, active=4)   # Matching units
    M.set_slide(L4, 7, active=5, script=[
        "Let's lock it in.",
        A("'Worker-hours = workers × hours' appears", T('Worker-hours $=$ workers $\\times$ hours', size=44)),
        A("'Phases → add each phase' appears", T('Phases $\\to$ add each phase', size=44)),
        A("'Joins or leaves' appears", T('Joins or leaves: whole job $-$ done $=$ left', size=44)),
        A("'Average rate' appears", T('Average rate $=$ total work $\\div$ total time', size=44)),
        D('Tick each line'),
        "Two more questions in this set — then the advanced ones.",
    ])
    M.set_sidebar(L4, ['What worker-hours are', 'Jobs in phases', 'Joins or leaves', 'Average rate', 'Matching units', 'Recap'])

    # =====================================================================================
    # 5. Existing guided questions: text + solution videos
    # =====================================================================================
    for vid in ['solve-wp26-g093', 'solve-wp26-g095', 'solve-wp26-g096', 'solve-wp26-g098', 'solve-wp26-g100']:
        M.set_sidebar(vid, LEARN_SB)
    for vid in ['solve-wp26-g101', 'solve-wp26-g102', 'solve-wp26-g103', 'solve-wp26-g104', 'solve-wp26-g105', 'solve-wp26-g105b']:
        M.set_sidebar(vid, ADV_SB)

    # Q1 (g093)
    S('wp26-g093', expl=[
        'Two changes, and each one multiplies the output: rate $\\times3$, and time $\\times4$ (from $y$ to $4y$).',
        'Samples: $x\\cdot3\\cdot4=12x$. The factors multiply; they do not add up to $7x$.',
        'Check with numbers: $x=6$, $y=2$. The old rate is 3 per minute, the new rate is 9 per minute, and in 8 minutes the robot packs $9\\times8=72=12\\cdot6$ samples ✓.'])
    V = 'solve-wp26-g093'
    M.set_slide(V, 2, title='Method 1 · Step by step')
    _fix_draw(M, V, 2, 'In row 2 write "3x"', 'In the row "Rate × 3" write "3x"')
    _fix_draw(M, V, 2, 'In row 3 write "12x"', 'In the last row write "12x"')
    M.edit_lines(V, 2, lambda ls: [dict(l, say="The table: samples and minutes. Row one is what they give us: x samples in y minutes. Now the rate triples.")
                                   if l.get('say', '').startswith('The robot packs x samples') else l for l in ls])
    M.set_slide(V, 3, title='Method 3 · Rate × time', script=[
        "Or use the formula. Rate is work over time.",
        D('Write "rate = x/y samples per minute"'),
        "x samples in y minutes: x over y per minute.",
        D('Write "new rate = 3x/y"'),
        "Three times as fast: three x over y.",
        D('Write "work = 3x/y × 4y = 12x"'),
        "Work is rate times time. The time is four y. The y's cancel: twelve x.",
        "Careful: the two changes multiply — three times four. Don't add them to seven.",
        D('Circle choice 2'),
    ])
    M.insert_slides(V, 3, [dict(mode='question', active=0, title='Method 4 · Plug in numbers', pre=[Q('wp26-g093')], script=[
        "Letters in the answers? Plug in easy numbers.",
        D('Write "x = 6, y = 2 → 3 per minute"'),
        "Say six samples in two minutes. That's three a minute.",
        D('Write "× 3 → 9 per minute · 4y = 8 minutes → 9 × 8 = 72"'),
        "Three times as fast: nine a minute. Four y is eight minutes. Seventy-two samples.",
        D('Write "3x = 18 · 12x = 72 ✓ · 7x = 42 · 4x/3 = 8"'),
        "Now put x equals six into each choice. Only twelve x gives seventy-two.",
        D('Circle choice 2'),
        "Pick numbers that are not zero or one, and not equal to each other. Then only one choice survives.",
    ])])

    # Pass 2: the original "Method 2 · Triple value" is back, named "triangle value" as in the ratio topic
    M.insert_slides(V, 2, [dict(mode='question', active=0, title='Method 2 · Triangle value', pre=[Q('wp26-g093')], script=[
        "Ratios not your thing? Use the triangle value: multiply along the diagonal and divide by what's left.",
        D('Write "? = (4y · 3x) ÷ y"'),
        "Four y times three x, divided by y.",
        D('Cancel the y\'s and write "= 12x"'),
        "The y's cancel. Twelve x.",
        "Careful: the two changes multiply — three times four. Don't add them to seven.",
        D('Circle choice 2'),
    ])])

    # Q2 (g095)
    S('wp26-g095',
      stem='Two identical inlets each fill a tank in 8 hours. A drain empties a full tank in 12 hours. At 9 a.m. the tank is empty, and both inlets and the drain are opened. At what time is the tank full?',
      choices=['3 p.m.', '1 p.m.', '2 p.m.', '5 p.m.'],
      expl=['Rates in tanks per hour: $\\frac18+\\frac18-\\frac1{12}=\\frac3{24}+\\frac3{24}-\\frac2{24}=\\frac4{24}=\\frac16$.',
            'One tank at $\\frac16$ of a tank per hour takes 6 hours. 9 a.m. plus 6 hours is 3 p.m.'])
    _fix_draw(M, 'solve-wp26-g095', 2, 'Write "09:00 + 6 h = 15:00" and circle choice 1', 'Write "9 a.m. + 6 h = 3 p.m." and circle choice 1')
    _fix_draw(M, 'solve-wp26-g095', 3, '24 : 4 = 6 h', '24 ÷ 4 = 6 h')
    _fix_say(M, 'solve-wp26-g095', 3, 'Fractions bothering you? Choose a tank of twenty-four units.',
             'Fractions bothering you? Choose a tank of twenty-four units — the LCM of eight and twelve.')

    # Q3 (g096)
    S('wp26-g096', expl=[
        'Equalize the times: in 12 hours A fills $12\\div4=3$ orders and B fills $12\\div6=2$. Together: 5 orders in 12 hours.',
        'One order: $\\frac{12}{5}$ hours $=\\frac{12}{5}\\times60=144$ minutes.',
        'Shortcut for two workers: $\\frac{4\\cdot6}{4+6}=\\frac{24}{10}=2.4$ hours $=144$ minutes.'])
    M.edit_lines('solve-wp26-g096', 3, lambda ls: ls[:-1] + [
        {'draw': 'Write "shortcut: (4 · 6)/(4 + 6) = 24/10 = 2.4 h"'},
        {'say': "Or the two-worker shortcut: four times six over four plus six. Two point four hours. Same answer."},
        ls[-1]])

    # Q4 (g098) - the general V rule
    S('wp26-g098', expl=[
        'Table (team, work, time). Row 1: 5, 30, 4. Row 2: 8, 72, ?.',
        'More work means more time ($\\times\\frac{72}{30}$); more workers means less time ($\\times\\frac58$): $4\\times\\frac{72}{30}\\times\\frac58=4\\times\\frac{12}5\\times\\frac58=6$ hours.',
        'Or worker-hours: $5\\times4=20$ worker-hours make 30 boards, so 72 boards need 48 worker-hours, and $48\\div8=6$ hours.'])
    V = 'solve-wp26-g098'
    M.set_slide(V, 3, script=[
        "Now the method that solves these in seconds — no thinking about directions at all.",
        A('The same table appears', TABLE(['Team', 'Work', 'Time'], [['5', '30', '4'], ['8', '72', '?']])),
        "The blank is in row two, in the Time column.",
        D('Draw a V through 5, 72 and 4'),
        "Draw a V: top-left, down to the bottom-middle, up to the top-right. Five, seventy-two, four.",
        "Multiply the three numbers on the V. Divide by the other two.",
        D('Write "? = (5 · 72 · 4) ÷ (30 · 8)"'),
        "Five times seventy-two times four, over thirty times eight.",
        D('Cancel, then write "= 6"'),
        "Cancel before you multiply: six hours.",
        D('Circle choice 2'),
        "Six. Choice two.",
    ])
    M.insert_slides(V, 3, [dict(mode='question', active=3, title='The V rule', pre=[], script=[
        A('The V rule appears', T('Blank in Team or Time: V = top-left $\\times$ bottom-middle $\\times$ top-right, $\\div$ the other two', size=38, gap=40)),
        "Here's the general rule. Always put the question row second.",
        "Blank in the Team column or the Time column? Same V. Top-left, bottom-middle, top-right. Divide by the other two numbers.",
        A('The upside-down V rule appears', T('Blank in Work: upside-down V = bottom-left $\\times$ top-middle $\\times$ bottom-right, $\\div$ the other two', size=38, gap=40)),
        "Blank in the Work column? Turn the V upside down. Bottom-left, top-middle, bottom-right.",
        A('An example table appears', TABLE(['Team', 'Work', 'Time'], [['5', '30', '4'], ['8', '?', '6']])),
        "Example: five workers make thirty boards in four hours. How many boards do eight workers make in six hours?",
        D('Draw an upside-down V through 8, 30 and 6; write "? = (8 · 30 · 6) ÷ (5 · 4) = 1440 ÷ 20 = 72"'),
        "Eight, thirty, six on the upside-down V. Divide by five and four. Seventy-two boards.",
        "Sense check: more workers AND more hours — so more than thirty boards. Good.",
    ])])
    _fix_draw(M, V, 5, '48 : 8 = 6', '48 ÷ 8 = 6')

    # Q5 (g100)
    S('wp26-g100', expl=[
        'Worker-days: $18\\times8=144$ and $12\\times7=84$. Total: $144+84=228$ worker-days.',
        'One worker does one worker-day each day, so alone the path takes 228 days.'])
    V = 'solve-wp26-g100'
    _fix_say(M, V, 1, "They ask about ONE worker — that's work time.", "They ask about ONE worker — count the worker-days.")
    M.set_slide(V, 2, title='Worker-days')
    _fix_say(M, V, 2, "How long would one worker need for the whole path? That's work time.",
             "How long would one worker need for the whole path? Count the worker-days.")

    # Q6 (g101)
    S('wp26-g101',
      stem='The combined rate of 3 high-speed scanners is twice the combined rate of 9 standard scanners. Scanners of the same type are identical. How many times as fast is one high-speed scanner as one standard scanner?',
      expl=['Let $F$ be the rate of one high-speed scanner and $S$ the rate of one standard scanner.',
            'The high-speed team is twice as fast, so the 2 goes on the smaller side: $3F=2\\cdot9S=18S$, therefore $F=6S$.'])
    M.edit_lines('solve-wp26-g101', 2, lambda ls: [
        dict(l, say="Rule: the times two goes on the SMALLER side. Then both sides are equal.")
        if 'give to the poor one' in l.get('say', '') else l for l in ls])

    # Q7 (g102)
    S('wp26-g102', expl=[
        'Machine: $24\\times5=120$ pieces added.',
        '5 hours $=300$ minutes $=4\\times75$ minutes, so the technician finishes $4\\times35=140$ pieces.',
        'Remaining: $50+120-140=30$ pieces.'])

    # Q8 (g103)
    S('wp26-g103', expl=[
        'Equalize to 6 hours: A covers $360\\times2=720$ m², B covers $40\\times3=120$ m². Together: 840 m² in 6 hours.',
        '$140=\\frac{840}6$, so the time is $6\\div6=1$ hour $=60$ minutes.',
        'Sense check: A alone does 120 m² per hour, so 140 m² takes it 70 minutes. Together is less than 70 and more than $70\\div2=35$. Only 60 fits.'])
    _fix_draw(M, 'solve-wp26-g103', 2, '6 h : 6 = 1 h', '6 h ÷ 6 = 1 h')

    # Q9 (g104)
    S('wp26-g104', expl=[
        'All three: 1 job in 8 hours, so 2 jobs in 16 hours. Ava and Ben: 1 job in 16 hours.',
        'Cleo does the difference: $2-1=1$ job in 16 hours, which is $\\frac1{16}$ of the job per hour. (With rates: $\\frac18-\\frac1{16}=\\frac1{16}$.)'])

    # Q10 (g105)
    S('wp26-g105', expl=[
        'Worker-hours: the cabinet needs $8\\times6=48$, the bench needs $9\\times8=72$. Total: $48+72=120$.',
        'In 24 hours: $120\\div24=5$ makers (2 on the cabinet, 3 on the bench).'])
    V = 'solve-wp26-g105'
    _fix_draw(M, V, 2, '"8·1·6 : (1·24) = 2"', '"(8 · 1 · 6) ÷ (1 · 24) = 2"')
    _fix_draw(M, V, 2, '"9·1·8 : (1·24) = 3"', '"(9 · 1 · 8) ÷ (1 · 24) = 3"')
    _fix_draw(M, V, 3, '8 : 4 = 2', '8 ÷ 4 = 2')
    _fix_draw(M, V, 3, '9 : 3 = 3', '9 ÷ 3 = 3')
    M.set_slide(V, 4, title='Method 3 · Worker-hours')
    _fix_draw(M, V, 4, '120 : 24 = 5', '120 ÷ 24 = 5')
    _fix_say(M, V, 4, 'The cabinet takes forty-eight hours of work. The bench, seventy-two.',
             'The cabinet takes forty-eight worker-hours. The bench, seventy-two.')
    _fix_say(M, V, 4, 'A hundred twenty hours of work, done in twenty-four hours: five makers.',
             'A hundred twenty worker-hours, done in twenty-four hours: five makers.')

    # Q11 (g105b)
    S('wp26-g105b', expl=[
        'Animal-days (like worker-days): $240\\times6=1{,}440$.',
        '90 animals: $1{,}440\\div90=16$ days.'])
    _fix_draw(M, 'solve-wp26-g105b', 3, '1,440 : 90 = 16', '1,440 ÷ 90 = 16')
    _fix_draw(M, 'solve-wp26-g105b', 4, '"240·1·6 : 90 = 16"', '"(240 · 1 · 6) ÷ (90 · 1) = 16"')

    # =====================================================================================
    # 6. New guided questions (created in this order: numbers 12, 13, 14, 15 before renumbering)
    # =====================================================================================
    # --- G1: rate in percent (after Q1) ---
    g1 = 'q-r26-t26-01'
    M.new_q(g1, TOPIC,
            'A printer finishes a job in 60 minutes. Its speed increases by 20%. How many minutes does the same job take now?',
            ['48', '50', '40', '72'], 2,
            ['Speed $+20\\%$ means speed $\\times\\frac65$. The job is the same, so the time is multiplied by the flipped fraction, $\\frac56$.',
             '$60\\times\\frac56=50$ minutes. Trap: the time does not drop by 20% (48).'])
    M.place_q(g1, 'wp26-learn', after='solve-wp26-g093')
    _solution(M, g1, ["A rate in percent.", "The trap is waiting in the choices."], [
        ('Method 1 · Flip the fraction', [
            "Twenty percent faster. First, turn the percent into a fraction.",
            D('Write "speed +20% = speed × 6/5"'),
            "A hundred twenty percent is six fifths.",
            "Same job — work fixed. That's inverse. So flip it: the time is times five sixths.",
            D('Write "60 × 5/6 = 50"'),
            "Sixty times five sixths: fifty minutes.",
            D('Circle choice 2'),
            "Fifty. Choice two.",
            "And the trap: forty-eight. Twenty percent faster does NOT mean twenty percent less time.",
        ]),
        ('Method 2 · Pick a job size', [
            "Not sure about flipping? Pick numbers.",
            D('Write "job = 60 pages → 1 page per minute"'),
            "Say the job is sixty pages. Sixty minutes: one page a minute.",
            D('Write "20% faster → 1.2 pages per minute → 60 ÷ 1.2 = 50"'),
            "Twenty percent faster: one point two pages a minute. Sixty divided by one point two: fifty minutes.",
            D('Circle choice 2'),
        ]),
    ])

    # --- G2: two workers - sense check + shortcut (after Q3) ---
    g2 = 'q-r26-t26-02'
    M.new_q(g2, TOPIC,
            'Worker A can do a job alone in 10 hours. Worker B can do the same job alone in 15 hours. How many hours do they need if they work together?',
            ['12.5', '25', '4', '6'], 4,
            ['Sense check: together is faster than A alone (less than 10 hours), but B is slower than A, so it takes more than $10\\div2=5$ hours. Only 6 fits.',
             'Shortcut: $\\frac{10\\cdot15}{10+15}=\\frac{150}{25}=6$ hours. (Job of 30 units: A does 3 per hour, B does 2, together 5, and $30\\div5=6$.)'])
    M.place_q(g2, 'wp26-learn', after='solve-wp26-g096')
    _solution(M, g2, ["Two workers. This time — cross out before you calculate."], [
        ('Method 1 · Sense check', [
            "A needs ten hours alone. With help, it's faster. So less than ten.",
            D('Cross out choices 1 and 2'),
            "Twelve and a half and twenty-five are out. Twelve and a half is the average of the times — a classic trap.",
            "Two workers as fast as A would need half: five hours. B is slower than A, so together it's more than five.",
            D('Cross out choice 3'),
            "Four is out.",
            D('Circle choice 4'),
            "Between five and ten — only six. Choice four. No calculation at all.",
        ]),
        ('Method 2 · The shortcut', [
            "Want to be sure? Times over plus.",
            D('Write "(10 · 15)/(10 + 15) = 150/25 = 6"'),
            "Ten times fifteen, a hundred fifty. Over ten plus fifteen, twenty-five. Six hours.",
            D('Write "job = 30 units: 3 + 2 = 5 per hour → 30 ÷ 5 = 6"'),
            "Or pick a job of thirty units: A does three an hour, B two. Five an hour — six hours.",
            D('Circle choice 4'),
        ]),
    ])

    # --- G3: a worker joins midway, different rates (after Q5) ---
    g3 = 'q-r26-t26-03'
    M.new_q(g3, TOPIC,
            'Pipe A fills a pool in 12 hours. Pipe B fills the same pool in 6 hours. Pipe A runs alone for 3 hours, and then pipe B is also opened. How many more hours are needed to fill the pool?',
            ['4.5', '3', '4', '6'], 2,
            ['Pick a pool of 12 units: A fills 1 unit per hour, B fills 2.',
             'In the first 3 hours A fills 3 units, so $12-3=9$ are left. Together: $1+2=3$ units per hour, and $9\\div3=3$ more hours.'])
    M.place_q(g3, 'wp26-learn', after='solve-wp26-g100')
    _solution(M, g3, ["Someone joins in the middle.", "Whole job, minus what's done, equals what's left."], [
        ('Method 1 · Pick a job size', [
            "Different rates — so pick a pool size. The LCM of twelve and six: twelve units.",
            D('Write "pool = 12 units · A: 1 per hour · B: 2 per hour"'),
            "A: twelve units in twelve hours — one an hour. B: twelve in six — two an hour.",
            D('Write "done: 3 × 1 = 3 → left: 12 − 3 = 9"'),
            "A works alone three hours: three units. Nine left.",
            D('Write "together: 1 + 2 = 3 per hour → 9 ÷ 3 = 3"'),
            "Together: three units an hour. Nine units: three more hours.",
            D('Circle choice 2'),
            "Three. Choice two.",
            "Four is the trap: that's the whole pool together, from the start.",
        ]),
        ('Method 2 · Fractions', [
            "The same with fractions.",
            D('Write "A: 3 × 1/12 = 1/4 done → 3/4 left"'),
            "A fills one twelfth an hour. Three hours: a quarter. Three quarters left.",
            D('Write "1/12 + 1/6 = 3/12 = 1/4 per hour → 3/4 ÷ 1/4 = 3"'),
            "Together: a quarter an hour. Three quarters take three hours.",
            D('Circle choice 2'),
        ]),
    ])

    # --- G4: average rate (advanced, after Q7) ---
    g4 = 'q-r26-t26-04'
    M.new_q(g4, TOPIC,
            'A machine makes 60 parts at a rate of 30 parts per hour, and then 60 more parts at a rate of 20 parts per hour. What is its average rate for all 120 parts, in parts per hour?',
            ['25', '24', '50', '22'], 2,
            ['Time: $60\\div30=2$ hours, and $60\\div20=3$ hours. Total: 5 hours.',
             'Average rate $=$ total work $\\div$ total time $=120\\div5=24$ parts per hour. Not 25: the machine spends more time at the slow rate.'])
    M.place_q(g4, 'wp26-advanced', after='solve-wp26-g102')
    _solution(M, g4, ["An average rate.", "The average of the two rates is a trap."], [
        ('Method 1 · Total work ÷ total time', [
            "Average rate: total work over total time.",
            D('Write "60 ÷ 30 = 2 h · 60 ÷ 20 = 3 h → 5 h"'),
            "Sixty parts at thirty an hour: two hours. Sixty at twenty: three hours. Five hours in total.",
            D('Write "120 ÷ 5 = 24"'),
            "A hundred twenty parts in five hours: twenty-four an hour.",
            D('Circle choice 2'),
            "Twenty-four. Choice two.",
        ]),
        ('Method 2 · Estimate', [
            "The average of thirty and twenty is twenty-five. Tempting — choice one.",
            "But the machine works longer at the SLOW rate. Three hours at twenty, only two at thirty.",
            D('Cross out choices 1 and 3'),
            "So the average is below twenty-five, and above twenty.",
            D('Cross out choice 4'),
            "Twenty-two or twenty-four? The times are three and two — almost equal. So the answer is close to twenty-five.",
            D('Circle choice 2'),
        ]),
    ], learn=False)

    # =====================================================================================
    # 7. Memory card
    # =====================================================================================
    c = M.card('mem-work-rate')
    c['intro'] = 'One formula, three relationships, and the tools for each question type.'
    c['tables'] = [
        {'title': 'The formula', 'head': ['Want', 'Use'], 'rows': [
            ['Work', 'rate × time'], ['Rate', 'work ÷ time (always "per" one time unit)'], ['Time', 'work ÷ rate']]},
        {'title': 'Relationships', 'head': ['Fixed', 'Change', 'Effect'], 'rows': [
            ['Time', 'rate × 2', 'work × 2 (direct)'], ['Rate', 'time × 2', 'work × 2 (direct)'],
            ['Work', 'rate × 2', 'time × ½ (inverse)'],
            ['Work', 'rate +25% (× 5/4)', 'time × 4/5 = −20% (flip the fraction)']]},
        {'title': 'Question types', 'head': ['Type', 'Tool'], 'rows': [
            ['Working together', 'add the rates. Nice common multiple → equalize the times; otherwise → fractions'],
            ['No job size given', 'pick a job size = LCM of the times (no fractions)'],
            ['Two workers (a h, b h)', 'together = ab ÷ (a + b); two equal workers → half the time'],
            ['Working against', 'subtract its rate'],
            ['Team (identical workers)', 'table Team · Work · Time → ratios or the V method'],
            ['Worker-hours (one worker alone)', 'workers × hours; add the phases'],
            ['Joins or leaves midway', 'whole job − done = left; then ÷ the new rate'],
            ['Average rate', 'total work ÷ total time (not the average of the rates)']]}]
    c['tips'] = [
        'Add rates — never completion times.',
        'Sense check (two workers): together < the fastest alone, and ≥ the fastest time ÷ 2. Cross out first.',
        'V method (question row second): blank in Team or Time → top-left × bottom-middle × top-right ÷ the other two. Blank in Work → upside-down V.',
        'Letters in the answers? Plug in numbers (not 0 or 1, not equal) and test every choice.',
        'Minutes → hours: divide by 60. 75 minutes = 1.25 hours.']

    # =====================================================================================
    # 8. Practice: text, removals, new exam-level items, order
    # =====================================================================================
    S('wp26-p01', stem='Eva folds 4 boxes in 6 minutes. Max labels 5 boxes in 8 minutes. Each of them works for 24 minutes at these constant rates. What is the total number of boxes folded by Eva and boxes labeled by Max?',
      expl=['Eva: $24=4\\times6$, so she folds $4\\times4=16$ boxes. Max: $24=3\\times8$, so he labels $3\\times5=15$ boxes.',
            'Total: $16+15=31$.'])
    # Pass 2: p02, p14, p15 restored (originals)
    S('wp26-p02', stem='Printer A produces $x$ posters per hour. Printer B is 3 times as fast. How many posters does B produce in 4 hours?',
      expl=['B produces $3x$ posters per hour.', 'In 4 hours: $4\\cdot3x=12x$ posters.'])
    S('wp26-p03', expl=['Small: $3\\div6=\\frac12$ hour. Large: $5\\div4=1\\frac14$ hours.',
                        'Total: $\\frac12+1\\frac14=1\\frac34$ hours = 1 hour 45 minutes.'])
    S('wp26-p04', expl=['Seven packers make 96 more items than three packers because of the $7-3=4$ extra packers.',
                        'One packer: $96\\div4=24$ items per hour.'])
    S('wp26-p05', expl=['V method (team, work, time). Row 1: 4, 18, 6. Row 2: 3, 27, ?.',
                        '$?=\\frac{4\\cdot27\\cdot6}{18\\cdot3}=\\frac{648}{54}=12$ minutes.'])
    S('wp26-p06', expl=['One person: $60\\div12=5$ parts per hour.', '$480\\div5=96$ people.'])
    S('wp26-p07', stem='Four identical pumps fill a reservoir in 9 hours. A fifth pump works twice as fast as one of the original pumps. How many hours do all five pumps need together?',
      expl=['The job: $4\\times9=36$ pump-hours (ordinary pumps). The fast pump counts as 2 ordinary pumps, so the team is worth $4+2=6$ pumps.',
            '$36\\div6=6$ hours.'])
    S('wp26-p08', expl=['Job A: $5\\times8=40$ worker-days. Job B: $6\\times10=60$ worker-days. Total: 100.',
                        'Ten workers: $100\\div10=10$ days.'])
    S('wp26-p09', expl=['Plain: $48\\div24=2$ days. Decorated: $48\\div8=6$ days.',
                        'Average rate $=$ total work $\\div$ total time $=96\\div8=12$ mugs per day (not the average of 24 and 8, which is 16).'])
    # Pass 2: p10 back to the original circular floor (uses circle area) -> moved to the T33 practice.
    # The half-smooth, half-rough version stays in T26 as q-r26-t26-13 (added with the new practice below).
    S('wp26-p10',
      stem='A machine paints 600 m² per hour on a smooth surface. On a rough surface its rate is halved. How many hours does it need to paint a rough circular floor of radius 15 meters?',
      expl=['On the rough surface the rate is $600\\div2=300$ m² per hour.',
            'The floor area is $\\pi\\cdot15^2=225\\pi$ m². Time $=$ work $\\div$ rate $=\\frac{225\\pi}{300}=\\frac{3\\pi}{4}$ hours.'])
    M.move('wp26-p10', 'geo33-foundation-practice')
    S('wp26-p11', expl=['A: $\\frac16$ of the tank per hour. B: $\\frac1{12}$. Together: $\\frac2{12}+\\frac1{12}=\\frac3{12}=\\frac14$, so 4 hours.',
                        'Shortcut: $\\frac{6\\cdot12}{6+12}=\\frac{72}{18}=4$.'])
    S('wp26-p12', stem='A robot seals $p$ envelopes in $q$ minutes at a constant rate. How many minutes does it need to seal $2q$ envelopes?',
      expl=['One envelope takes $\\frac qp$ minutes. For $2q$ envelopes: $2q\\cdot\\frac qp=\\frac{2q^2}{p}$ minutes.',
            'Check with numbers: $p=2$, $q=10$. One envelope takes $5$ minutes, and $2q=20$ envelopes take $100$ minutes. $\\frac{2\\cdot10^2}{2}=100$ ✓.'])
    S('wp26-p13', expl=['The team works $5\\times2=10$ worker-hours for 8 crates. One crate: $10\\div8=1.25$ worker-hours.',
                        'One worker needs 1.25 hours $=75$ minutes.'])
    S('wp26-p14', expl=['The three hoses fill $\\frac15$ of the tank per hour. The two hoses fill $\\frac1{10}$ per hour.',
                        'The third hose fills the difference: $\\frac15-\\frac1{10}=\\frac2{10}-\\frac1{10}=\\frac1{10}$ of the tank per hour.'])
    S('wp26-p15', stem='Three expert sorters process twice as many letters per hour as four trainees. What is one expert’s rate divided by one trainee’s rate?',
      expl=['Let $e$ be the rate of one expert and $t$ the rate of one trainee.',
            'The experts are twice as fast, so the 2 goes on the smaller side: $3e=2\\cdot4t=8t$. Divide by $3t$: $\\frac et=\\frac83$.'])
    S('wp26-p16', expl=['Four slow cycles: $4\\times\\frac35=\\frac{12}5$ seconds.',
                        'Seven fast cycles take the same time, therefore one fast cycle takes $\\frac{12}5\\div7=\\frac{12}{35}$ second.'])
    S('wp26-p17', expl=['One scanner: $\\frac LM$ pages per hour. D scanners: $\\frac{DL}M$ pages per hour.',
                        'In 3 hours: $\\frac{3DL}M$. (Check: $M=2$, $L=10$, $D=4$: one scanner does 5 per hour, four do 20 per hour, 60 in 3 hours, and $\\frac{3\\cdot4\\cdot10}2=60$ ✓.)'])
    S('wp26-p18', expl=['Four painters: $\\frac16$ of the wall per hour. Five painters: $\\frac14$.',
                        'The fifth painter adds $\\frac14-\\frac16=\\frac3{12}-\\frac2{12}=\\frac1{12}$ per hour, therefore alone he needs 12 hours.'])
    S('wp26-p19', stem='A tap fills a container in 10 hours. Three identical drains empty a full container in 4 hours. How many hours does one drain need to remove the amount of water that four taps supply in 15 hours?', expl=['Four taps for 15 hours: $4\\times15=60$ tap-hours. One container needs 10 tap-hours, so they supply $60\\div10=6$ containers.',
                        'Three drains empty a container in 4 hours, so one drain needs $3\\times4=12$ hours per container. Six containers: $6\\times12=72$ hours.'])
    S('wp26-p20', expl=['Rates: slow = 1 part, fast = 3 parts, together = 4 parts.',
                        'The slow machine alone has $\\frac14$ of the team rate, so it needs 4 times as long: $4\\times12=48$ hours.'])
    S('wp26-p21', stem='A pump fills a tank in 8 hours, while a leak empties a full tank in 24 hours. The tank starts empty. How many hours does it take to fill with both operating?',
      expl=['Net rate: $\\frac18-\\frac1{24}=\\frac3{24}-\\frac1{24}=\\frac2{24}=\\frac1{12}$ of the tank per hour.', 'One tank: 12 hours.'])
    S('wp26-p22', expl=['Pick a job of 15 units: each worker does 1 unit per hour. After 5 hours, 5 units are done and 10 are left.',
                        'Two workers do 2 units per hour: $10\\div2=5$ more hours.'])
    S('wp26-p23', expl=['The job: $6\\times14=84$ worker-days. First 4 days: $6\\times4=24$. Left: $84-24=60$.',
                        'Four workers remain: $60\\div4=15$ more days.'])
    S('wp26-p24', expl=['A: $18\\div6=3$ parts per minute. B: $20\\div5=4$ parts per minute.',
                        'Together: 7 per minute, so $84\\div7=12$ minutes.'])
    S('wp26-p25', stem='A printer’s speed increases by 25%. A job used to take 50 minutes. How many minutes does the same job take now?',
      expl=['Speed $+25\\%$ means speed $\\times\\frac54$. Same job, therefore time $\\times\\frac45$.',
            '$50\\times\\frac45=40$ minutes (a 20% drop, not 25%).'])
    S('wp26-p26', stem='A container is emptied by drain A in 9 minutes or by drain B in 18 minutes. Drain A works alone for 3 minutes, and then drain B also opens. How many minutes after drain B opens is the container empty?',
      expl=['Pick a container of 18 units: A removes 2 per minute, B removes 1.',
            'In 3 minutes A removes 6, so 12 are left. Together they remove 3 per minute: $12\\div3=4$ minutes.'])
    S('wp26-p27', expl=['V method (team, work, time). Row 1: 8, 960, 3. Row 2: ?, 1,600, 4.',
                        '$?=\\frac{8\\cdot1600\\cdot3}{960\\cdot4}=\\frac{38400}{3840}=10$ machines.'])

    P = 'wp26-practice'
    new = [
        ('q-r26-t26-05',
         'A machine’s rate decreases by 20%. A job used to take it 4 hours. How many hours does the same job take now?',
         ['4.8', '5', '3.2', '6'], 2,
         ['Rate $-20\\%$ means rate $\\times\\frac45$. Same job, therefore time $\\times\\frac54$: $4\\times\\frac54=5$ hours.',
          'Trap: $4\\times1.2=4.8$. The time rises by 25%, not by 20%.']),
        ('q-r26-t26-06',
         'Worker A alone does a job in 12 hours. Together with worker B, the job takes 4 hours. How many hours does worker B need alone?',
         ['8', '6', '3', '16'], 2,
         ['Together: $\\frac14$ of the job per hour. A: $\\frac1{12}$. B: $\\frac14-\\frac1{12}=\\frac3{12}-\\frac1{12}=\\frac2{12}=\\frac16$, therefore 6 hours.',
          'Or a job of 12 units: together 3 per hour, A does 1, so B does 2 and needs $12\\div2=6$ hours.']),
        ('q-r26-t26-07',
         'Worker A can do a job in 10 days, and worker B can do it in 15 days. They start together. After 3 days, A leaves. How many more days does B need to finish the job?',
         ['7.5', '6', '9', '4.5'], 1,
         ['Pick a job of 30 units: A does 3 per day, B does 2 per day.',
          'Together for 3 days: $3\\times(3+2)=15$ units. Left: $30-15=15$. B alone: $15\\div2=7.5$ days.']),
        ('q-r26-t26-08',
         'Pipes A and B together fill a tank in 6 hours. They run together for 2 hours, and then pipe A is closed. Pipe B fills the rest of the tank in 10 more hours. How many hours would pipe A need alone to fill the tank?',
         ['10', '15', '12', '9'], 1,
         ['Together: $\\frac16$ of the tank per hour. In 2 hours: $\\frac26=\\frac13$. B fills the other $\\frac23$ in 10 hours, therefore B fills $\\frac23\\div10=\\frac1{15}$ per hour.',
          'A: $\\frac16-\\frac1{15}=\\frac5{30}-\\frac2{30}=\\frac3{30}=\\frac1{10}$, therefore 10 hours alone.']),
        ('q-r26-t26-09',
         'A worker’s speed increases by 50%, and the job becomes 20% larger. The old job took 10 hours. How many hours does the new job take?',
         ['7', '8', '12', '9'], 2,
         ['Work $\\times\\frac65$ means time $\\times\\frac65$. Speed $\\times\\frac32$ means time $\\times\\frac23$.',
          '$10\\times\\frac65\\times\\frac23=10\\times\\frac{12}{15}=8$ hours. Trap: $10\\times(1+0.2-0.5)=7$. The changes multiply; they do not add.']),
        ('q-r26-t26-10',
         'Worker A does a job alone in a hours, and worker B does it alone in b hours ($a>0$ and $b>0$). How many hours do they need together?',
         ['$\\frac{a+b}{2}$', '$a+b$', '$\\frac{ab}{a+b}$', '$\\frac{a+b}{ab}$'], 3,
         ['Rates: $\\frac1a+\\frac1b=\\frac{a+b}{ab}$ of the job per hour. Time $=1\\div\\frac{a+b}{ab}=\\frac{ab}{a+b}$.',
          'Plug in $a=3$, $b=6$: rates $\\frac13+\\frac16=\\frac12$, so 2 hours. Choices: 4.5, 9, 2, $\\frac12$. Only $\\frac{ab}{a+b}$ gives 2.']),
        ('q-r26-t26-11',
         'A machine works for 2 hours at 30 parts per hour and then for 3 hours at 40 parts per hour. What is its average rate for the 5 hours, in parts per hour?',
         ['35', '36', '34', '70'], 2,
         ['Total work: $2\\times30+3\\times40=60+120=180$ parts. Total time: 5 hours.',
          'Average: $180\\div5=36$. Not 35: the machine spends more time at 40 parts per hour.']),
        ('q-r26-t26-12',
         'Twelve identical workers are supposed to finish a job in 10 days. After 4 days, 4 more workers join them. How many days does the whole job take?',
         ['4.5', '8.5', '7.5', '9'], 2,
         ['The job: $12\\times10=120$ worker-days. First 4 days: $12\\times4=48$. Left: $120-48=72$.',
          'Now $12+4=16$ workers: $72\\div16=4.5$ more days. The whole job: $4+4.5=8.5$ days. (4.5 is only the part after they join.)']),
        ('q-r26-t26-13',
         'A machine paints 600 m² per hour on a smooth surface. On a rough surface its rate is halved. A floor of 600 m² is half smooth and half rough. How many minutes does the machine need to paint the whole floor?',
         ['60', '80', '90', '120'], 3,
         ['Smooth half: $300\\div600=\\frac12$ hour. Rough half: the rate is 300 m² per hour, so $300\\div300=1$ hour.',
          'Total: $1\\frac12$ hours $=90$ minutes. Trap: the average rate, 450 m² per hour, gives 80 minutes — but the machine spends more time at the slow rate.']),
    ]
    for qid, stem, ch, cor, ex in new:
        M.new_q(qid, TOPIC, stem, ch, cor, ex)
        M.place_q(qid, P)

    M.practice_order(P, [
        # easy
        'wp26-p06', 'wp26-p02', 'wp26-p24', 'wp26-p11', 'wp26-p21', 'wp26-p03', 'wp26-p01', 'wp26-p04', 'wp26-p12', 'wp26-p17',
        'wp26-p13', 'q-r26-t26-05', 'wp26-p25',
        # medium
        'wp26-p05', 'wp26-p27', 'wp26-p08', 'wp26-p09', 'wp26-p16', 'wp26-p20', 'q-r26-t26-06', 'wp26-p18',
        'wp26-p15', 'wp26-p14', 'wp26-p22', 'wp26-p23', 'q-r26-t26-10', 'q-r26-t26-11',
        # exam-hard
        'q-r26-t26-13', 'wp26-p26', 'wp26-p07', 'wp26-p19', 'q-r26-t26-07', 'q-r26-t26-12', 'q-r26-t26-09', 'q-r26-t26-08',
    ])

    summary(M)

    # =====================================================================================
    # 9. Cleanup: American spelling, trimmed stems, solution-video titles in sync with stems
    # =====================================================================================
    _fix_say(M, 'wp-092', 4, 'memorise', 'memorize')
    b = M.slide('wp-094', 3)
    for it in b['items']:
        if it.get('t') == '9 litres in, 4 litres out — every minute':
            it['t'] = '9 liters in, 4 liters out — every minute'
    for l in b['lines']:
        if 'label' in l: l['label'] = l['label'].replace('litres', 'liters')
    _fix_say(M, 'wp-094', 3, 'five litres a minute', 'five liters a minute')
    _fix_say(M, 'solve-wp26-g103', 2, 'square metres', 'square meters')
    for f in list(M.D['flow']):
        if f['topic'] == TOPIC and f['type'] == 'question':
            q = M.q(f['ref'])
            if q['stemRich'] != q['stemRich'].strip():
                S(f['ref'], stem=q['stemRich'].strip())
    for v in M.D['videos'].values():
        if v['topic'] == TOPIC and v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']
    # keep the teacher's "on screen" note of pre-loaded questions in sync with the rewritten stems
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            pre = b['items'][:b['pre']]
            if len(pre) == 1 and pre[0].get('k') == 'q' and b.get('canvas', '').startswith('Pre-loaded — question'):
                qid = pre[0]['qid']
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, M.q(qid)['stem'])

    cut_repeats(M)
    add_methods(M)   # 2026-10-06 new exam methods (runs last)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)


def _b(label, tex, size=42):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summary(M):
    """Pass 2: a summary lesson right before the practice (end of the further guided examples)."""
    last = [f['ref'] for f in M.D['flow'] if f['section'] == 'wp26-advanced'][-1]
    sb = ['The formula', 'Three relationships', 'Rate in percent', 'One job = 1', 'Working together',
          'Two workers', 'Team questions', 'Worker-hours', 'Average rate', 'Before you practice']
    M.new_video('r26-t26-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            'A quick summary before the practice.',
            'Everything important about work and rate — in about three minutes.']),
        dict(title='The formula', active=0, script=[
            _b('Rate × Time = Work', 'Rate $\\times$ Time $=$ Work'),
            'One formula. They give you two of the three — you find the third.',
            _b('Rate = work in ONE time unit', 'Rate $=$ work in ONE time unit: $28$ pages in $4$ min $\\to$ $7$ per minute', size=40),
            'A rate is always "per": per minute, per hour. Work is everything you did.',
            _b('Matching units', 'Combine only matching units: minutes $\\to$ hours: $\\div 60$'),
            'Per hour and per minute? Convert first.']),
        dict(title='Three relationships', active=1, script=[
            _b('Time or rate fixed → direct', 'Time or rate fixed $\\to$ direct: rate $\\times2$ $\\to$ work $\\times2$'),
            _b('Work fixed → inverse', 'Work fixed $\\to$ inverse: rate $\\times2$ $\\to$ time $\\times\\frac12$'),
            'Same job, twice as fast? Half the time.',
            _b('Two changes multiply: ×2 and ×5 → ×10', 'Two changes multiply: $\\times2$ and $\\times5$ $\\to$ $\\times10$, not $\\times7$'),
            'Two changes at once? Multiply them. Never add them.']),
        dict(title='Rate in percent', active=2, script=[
            _b('Rate +100% → time −50%', 'Rate $+100\\%$ $=\\times2$ $\\to$ time $\\times\\frac12$ $=-50\\%$'),
            'Turn the percent into a fraction. Flip it. Multiply the time.',
            _b('Rate −25% → time +33⅓%', 'Rate $-25\\%$ $=\\times\\frac34$ $\\to$ time $\\times\\frac43$ $=+33\\frac13\\%$'),
            'Twenty-five percent slower does NOT mean twenty-five percent more time.']),
        dict(title='One job = 1', active=3, script=[
            _b('One job in 7 hours → 1/7 per hour', 'One job in $7$ hours $\\to$ $\\frac17$ of the job per hour'),
            'No job size? Call the whole job one.',
            _b('Or pick a job size: the LCM of the times', 'Or pick a job size: the LCM of the times. $4$ h and $10$ h $\\to$ $20$ units', size=40),
            'Four and ten hours: a job of twenty units. Five and two units per hour. No fractions.']),
        dict(title='Working together', active=4, script=[
            _b('Together → add the rates', 'Together $\\to$ add the rates · never the times'),
            'Working together? Add the rates. Never add the completion times.',
            _b('Working against → subtract its rate', 'Working against $\\to$ subtract its rate: $10-4=+6$ per minute'),
            'A drain or a leak gets a minus.',
            _b('Match the times first', 'Match the times first: in $10$ h, A does $5$ jobs, B does $2$'),
            'A nice common time? Stretch both workers to it, then add.']),
        dict(title='Two workers', active=5, script=[
            _b('Two workers: ab/(a + b)', 'Two workers: together $=\\frac{a\\cdot b}{a+b}$ · $\\frac{3\\cdot6}{3+6}=2$ h'),
            'Times over plus — for exactly two workers. Two equal workers: half the time.',
            _b('Sense check: fastest ÷ 2 ≤ together < fastest', 'Sense check: fastest time $\\div2$ $\\le$ together $<$ fastest time'),
            'Three and six hours: the answer is between one and a half and three. Cross out everything outside first.']),
        dict(title='Team questions', active=6, script=[
            _b('Identical workers → table Team · Work · Time', 'Identical, constant rate $\\to$ table: Team · Work · Time'),
            'Identical workers and a group? A team question. Work always sits in the middle.',
            _b('V method', 'V: top-left $\\times$ bottom-middle $\\times$ top-right $\\div$ the other two', size=40),
            'Question row second. Blank in Team or Time: the V. Blank in Work: the V upside down.',
            _b('More work → more time · more workers → less time', 'More work $\\to$ more time · More workers $\\to$ less time'),
            'Then a quick sense check of the direction.']),
        dict(title='Worker-hours', active=7, script=[
            _b('Worker-hours = workers × hours', 'Worker-hours $=$ workers $\\times$ hours: $4\\times5=20$'),
            'Worker-hours measure the size of the job. One worker alone needs that many hours.',
            _b('Phases: add each phase', 'Phases: $8\\times3+5\\times2=34$ worker-days'),
            _b('Joins or leaves: whole − done = left', 'Joins or leaves: whole job $-$ done $=$ left, then $\\div$ the new team'),
            'Someone joins or leaves? Whole job, minus what\'s done, is what\'s left.']),
        dict(title='Average rate', active=8, script=[
            _b('Average rate = total work ÷ total time', 'Average rate $=\\dfrac{\\text{total work}}{\\text{total time}}$'),
            _b('40 at 10/h, 40 at 40/h → 80 ÷ 5 = 16, not 25', '$40$ at $10$ per hour, $40$ at $40$ per hour: $\\frac{80}{4+1}=16$, not $25$', size=40),
            'Not the average of the rates. More time goes to the slow rate, so the answer is closer to it.']),
        dict(title='Before you practice', active=9, script=[
            'Before you practice, ask yourself these questions.',
            _b('What is the work, what is the rate, what is the time?', 'What is the work? The rate? The time?'),
            _b('What stays fixed? Direct or inverse?', 'What stays fixed? Direct or inverse?'),
            _b('Where must the answer be?', 'Where must the answer be? Cross out first.'),
            _b('Left, or the whole job?', 'Do they want what is LEFT, or the whole job?'),
            _b('Letters in the answers? Plug in numbers.', 'Letters in the answers? Plug in numbers (not $0$ or $1$, not equal).'),
            'The traps: adding times instead of rates, a percent in the rate taken as the same percent in the time, the average of two rates, and mixing minutes with hours.',
            'Good luck.'])],
        'wp26-advanced', after=last)


# =====================================================================================
# 2026-10-05 cut repeats: each lesson back to a short intro (Hebrew style); every idea a
# question video already teaches is cut from the lesson; ideas no question teaches stay or
# move as one line + board item into the question video that uses them.
# =====================================================================================
def _add_line(M, vid, n, before_say, line, item=None, label=None):
    """Insert one spoken line (+ optional board item) right before the line containing `before_say`
    (before_say=None: at the end of the slide)."""
    b = M.slide(vid, n); script = []; hit = False
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


def _keep_slides(M, vid, keep, sidebar):
    """Keep only the slides `keep` (1-based, in order); set the sidebar; renumber 'active'."""
    v = M.video(vid)
    M.remove_slides(vid, [k for k in range(1, len(v['beats']) + 1) if k not in keep])
    a = 0
    for b in v['beats']:
        if b.get('mode') == 'concept':
            b['active'] = a; a += 1
    M.set_sidebar(vid, sidebar)


def _say_check(M, vid, n, old, new):
    assert any(old in (l.get('say') or '') for l in M.slide(vid, n)['lines']), '%s #%d: not found: %s' % (vid, n, old)
    _fix_say(M, vid, n, old, new)


def cut_repeats(M):
    # ---- Work, Rate and Time: keep title + The formula (triangle) + Rate has a time unit ----
    # (the Hebrew theory lesson teaches exactly these two)
    vid = 'wp-092'
    _keep_slides(M, vid, [1, 2, 3], ['The formula', 'Rate has a time unit'])
    _add_line(M, vid, 3, None, "Now two questions. Try each one first — then watch the solution.")
    # "Work = rate x time" forwards/backwards -> the triangle (slide 2) + Q1 method 3.
    # "Three relationships": direct -> Q1 method 1; inverse -> Q2 (printer). Board item for the inverse:
    _add_line(M, 'solve-q-r26-t26-01', 2, 'Same job — work fixed',
              "The rule: when the work is fixed, faster means less time — inverse.",
              T(r'Work fixed: rate $\times2$ $\to$ time $\times\frac12$ (inverse)', 36),
              "'Work fixed: rate ×2 → time ×½ (inverse)' appears")
    # "Rate in percent" -> Q2 method 1; move "the other way" there
    _add_line(M, 'solve-q-r26-t26-01', 2, None,
              "It works the other way too: rate down twenty percent is times four fifths — so the time is times five quarters, up twenty-five percent.",
              T(r'Rate $-20\%$ $\to$ time $\times\frac54$ $=+25\%$', 36),
              "'Rate −20% → time ×5/4 = +25%' appears")
    # "One job = 1" -> Q3 (tank: one eighth per hour; method 2: LCM job size). Make "call it one" explicit:
    _add_line(M, 'solve-wp26-g095', 2, 'Rate is work over time. One tank in eight hours',
              "We don't know the tank's size — so call the whole tank one job.",
              T(r'One job $=1$ $\to$ $8$ hours: $\frac18$ per hour', 36),
              "'One job = 1 → 8 hours: 1/8 per hour' appears")

    # ---- Working Together: keep title + Add the rates + Working against you (the Hebrew intro) ----
    vid = 'wp-094'
    _keep_slides(M, vid, [1, 2, 3], ['Add the rates', 'Working against you'])
    _add_line(M, vid, 3, None, "Let's see it in three questions.")
    # "Match the times" -> Q4 method 1 (equalize the times); "Two-worker shortcut" -> Q4 method 2 + Q5 method 2;
    # "Sense check" -> Q5 method 1 (and Q4). Move the two shortcut details into Q5 method 2:
    _add_line(M, 'solve-q-r26-t26-02', 3, None,
              "Two equal workers? Together they need half the time. And this shortcut is for two workers only — three workers, add the rates.",
              T(r'Equal workers $\to$ half the time · $3$ workers $\to$ add rates', 36),
              "'Equal workers → half the time · 3 workers → add rates' appears")

    # ---- Team Questions (not cut): its "three relationships" slide is gone, reword the reference ----
    _say_check(M, 'wp-097', 3, 'Now remember the three relationships.', 'Remember from the first questions:')

    # ---- Worker-Hours: keep title + What worker-hours are (the Hebrew intro) ----
    vid = 'wp-099'
    _keep_slides(M, vid, [1, 2], ['What worker-hours are'])
    _add_line(M, vid, 2, None, "Let's see it in the questions.")
    # "Jobs in phases" -> Q7 (path: 18 x 8 + 12 x 7); "Joins or leaves" -> Q8 (pipe B joins: whole - done = left,
    # "left or whole" trap). "Average rate" -> Q11 (q-r26-t26-04); move the "weighted by time" line there:
    _add_line(M, 'solve-q-r26-t26-04', 3, None,
              "It's a weighted average — weighted by TIME. You'll meet the same trap with average speed.",
              T('Average rate: weighted by time', 36), "'Average rate: weighted by time' appears")
    # "Matching units" -> Q10 (g102: hours become minutes); board item there:
    _add_line(M, 'solve-wp26-g102', 2, 'Hours to minutes: times sixty',
              "Combine only matching units — convert first.",
              T('Combine only matching units', 36), "'Combine only matching units' appears")


# =====================================================================================
# 2026-10-06 new exam methods (teacher-approved): compare by factors (the V made general)
# and catching up = gap ÷ difference in rates. Nothing in topic 26 is recorded.
# =====================================================================================
def add_methods(M):
    # ---- 1. Concept video "Compare by Factors" at the end of the learning sequence (before the summary) ----
    sb = ['Two things change', 'The rule', 'The V is one case', 'When it fails', 'Remember']
    q6 = M.video('solve-wp26-g098')['beats'][0]['bigTitle']   # old number; renumber_guided maps it to the final one
    M.new_video('r26-t26-factors', TOPIC, 'Compare by Factors', sb, [
        dict(mode='title', title='Compare by Factors', script=[
            'Compare by factors.',
            'The V handles one table. But many exam questions change two things at once — and give only relations: "three quarters as many", "twice as fast".',
            'For those there is one general tool. No equations.']),
        dict(mode='concept', active=0, title='Two things change', script=[
            A("'Lia and Ben' appears", T(r'Lia works $\frac34$ as many hours a day as Ben. Per hour she does $\frac23$ of what he does. Ben finishes a job in $8$ days. How many days does Lia need?', size=36, gap=40)),
            'Two things are different for Lia: her hours a day, and her work per hour.',
            'What does a day of work depend on? Hours a day, times work per hour.',
            A("'Work per day = hours a day × work per hour' appears", T(r'Work per day $=$ hours a day $\times$ work per hour', size=40, gap=40)),
            D('Write "Lia per day: 3/4 · 2/3 = 1/2 of Ben"'),
            'Her hours: times three quarters. Each hour: times two thirds. Three quarters times two thirds — one half.',
            'Why multiply, not add? Each change scales what is already there. Fewer hours — and less in each of them. A fraction of a fraction.',
            D('Write "same job, half per day → 8 · 2 = 16 days"'),
            'Same job, half as much each day — twice as many days. Sixteen.',
            'We never knew Ben\'s real hours or his real rate. We didn\'t need them.']),
        dict(mode='concept', active=1, title='The rule', script=[
            A("'New = old × every factor that changed' appears", T(r'New value $=$ old value $\times$ every factor that changed', size=40, gap=50)),
            A("'Same way → as is · opposite way → flip it' appears", T(r'Pushes the same way $\to$ as is · pushes the opposite way $\to$ flip it', size=40, gap=50)),
            'The rule: start from the old value and multiply by every factor that changed.',
            'For each factor ask: when this grows, does my answer grow too? Yes — as it is. No — flip it.',
            D('Write "days = 8 × 4/3 × 3/2 = 16"'),
            'We want days. More hours a day means fewer days — opposite. Three quarters flips to four thirds. More per hour — opposite too. Two thirds flips to three halves.',
            'Eight times four thirds times three halves: sixteen. One line.',
            A("'Anything shared cancels' appears", T(r'Anything that is the same for both $\to$ cancels', size=40, gap=50)),
            'And the size of the job? The same for both — it cancels. You never need it.']),
        dict(mode='concept', active=2, title='The V is one case', script=[
            A("'Team · Work · Time table' appears", TABLE(['Team', 'Work', 'Time'], [['5', '30', '4'], ['8', '72', '?']])),
            'Remember the question with five workers, thirty boards, four hours? Then eight workers, seventy-two boards.',
            D('Write "4 × 72/30 × 5/8 = 6"'),
            'Its first method was exactly this rule. More work pushes the time the same way — as is. More workers — the opposite way, flipped.',
            A("'V = factors for a 3-column table' appears", T(r'The V $=$ compare by factors for a $3$-column table', size=40, gap=50)),
            'The V is the same rule drawn as a picture, for a table where the middle is the product of the other two. It just does the flipping for you.',
            'Compare by factors works everywhere else too: price times quantity, three things multiplied, or a formula they give you.']),
        dict(mode='concept', active=3, title='When it fails', script=[
            A("'+k is not a factor → equation' appears", T(r'A fixed amount added ($+k$) is not a factor $\to$ write an equation', size=40, gap=50)),
            'One limit: every change must be a TIMES change.',
            A("'Lia packs 2 more boxes an hour than Ben' appears", T(r'"Lia packs $2$ more boxes an hour than Ben."', size=40, gap=50)),
            'Two more than ten is twenty percent more. Two more than four is fifty percent more. The factor depends on Ben\'s real number — which we don\'t have.',
            D('Write "Ben: x per hour · Lia: x + 2 → equation"'),
            'Here, give Ben\'s rate a letter and write an equation.',
            'The cue is in the words: "times", "as many as", "a fraction of", "percent of" — factors. "More than" by a number — an equation.']),
        dict(mode='concept', active=4, title='Remember', script=[
            A("'Two or more things change → multiply the factors' appears", T(r'Two or more things change, only relations given $\to$ multiply the factors', size=40, gap=50)),
            A("'Same way as is · opposite way flipped · shared cancels' appears", T(r'Same way: as is · opposite way: flipped · shared: cancels', size=40, gap=50)),
            'New value equals old value times every factor that changed. Same way — as is. Opposite — flipped. Shared — gone.',
            'Then a sense check: should the answer go up or down?',
            'One question next. Try it first.'])],
        'wp26-advanced', after='solve-wp26-g105b')

    # ---- guided question: budget ÷ price (two factors, one flipped) ----
    qid = 'q-r26-t26-21'
    M.new_q(qid, TOPIC,
            'Last month Dana spent her whole budget on notebooks and bought 30 of them. This month her budget is 20% larger, '
            'and each notebook costs 1.5 times as much as last month. How many notebooks can she buy this month with her whole budget?',
            ['54', '20', '24', '21'], 3,
            ['Notebooks $=$ budget $\\div$ price. Two things change, so multiply by both factors.',
             'Budget $+20\\%$ $=\\times\\frac65$. A larger budget buys more notebooks (same way): $\\times\\frac65$ as it is.',
             'Price $\\times\\frac32$. A higher price buys fewer notebooks (opposite way): flip it, $\\times\\frac23$.',
             '$30\\times\\frac65\\times\\frac23=24$ notebooks.',
             'Traps: $54=30\\times\\frac65\\times\\frac32$ (the price was not flipped); $21$ adds the percents ($+20\\%$ and $-50\\%$).'])
    M.place_q(qid, 'wp26-advanced', after='r26-t26-factors')
    n = M.next_question_number(TOPIC)
    lab = 'Question %d' % n
    v = M.new_video('solve-' + qid, TOPIC, 'Advanced Work & Rate', [lab], [
        dict(mode='title', title=lab, script=[
            'Question %s.' % ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen'][n],
            'No workers this time — a budget and a price. The same tool.']),
        dict(mode='question', active=0, title='Method 1 · Compare by factors', pre=[Q(qid)], script=[
            'Two things change: the budget and the price. And we get no real budget, no real price. Only relations — compare by factors.',
            'First, what does the number of notebooks depend on? The budget divided by the price.',
            A("'Notebooks = budget ÷ price' appears", T(r'Notebooks $=$ budget $\div$ price', size=36)),
            'Budget twenty percent larger: times six fifths. A bigger budget buys MORE notebooks — the same way. As it is.',
            D('Write "budget: × 6/5 (same way)"'),
            'Price one and a half times: times three halves. A higher price buys FEWER notebooks — the opposite way. Flip it: two thirds.',
            D('Write "price: × 3/2 → flip → × 2/3"'),
            D('Write "30 × 6/5 × 2/3 = 24"'),
            'Thirty times six fifths is thirty-six. Times two thirds: twenty-four.',
            D('Circle choice 3'),
            'Twenty-four. Choice three.']),
        dict(mode='question', active=0, title='The traps', pre=[Q(qid)], script=[
            'Look at the wrong choices — each one is a real mistake.',
            D('Next to choice 1 write "price not flipped: 30 × 6/5 × 3/2"'),
            'Fifty-four: multiplying by the price as it is. A higher price can\'t give you MORE notebooks. Sense check kills it.',
            D('Next to choice 4 write "+20% − 50% = −30%"'),
            'Twenty-one: adding percents. Plus twenty, minus fifty. Changes multiply — never add them.',
            D('Next to choice 2 write "forgot the budget: 30 × 2/3"'),
            'Twenty: forgetting that the budget changed too. Every factor that changed goes in.',
            'Check the answer: last month, say, a budget of thirty dollars at one dollar each. Now thirty-six dollars at a dollar fifty: twenty-four notebooks.'])],
        'wp26-advanced', kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Advanced Work & Rate'
    v['title'] = v['navLabel'] = M.q(qid)['stem']

    # ---- 2. Catching up = gap ÷ difference in rates: one slide in the queue question (Q10, g102) ----
    vid = 'solve-wp26-g102'
    act = M.slide(vid, 2)['active']
    M.insert_slides(vid, 3, [dict(mode='question', active=act, title='Same idea: catching up', pre=[], script=[
        'One more tool from the same idea: one rate against another. Only the difference counts.',
        A("'Catching up: days = gap ÷ difference in rates' appears", T(r'Catching up: time $=$ gap $\div$ difference in rates', size=40, gap=50)),
        A("'Printer example' appears", T(r'A printer normally prints $6$ hours a day. It was down for $5$ days. Now it prints $16$ hours a day. How many days until it catches up?', size=36, gap=40)),
        D('Write "behind: 5 × 6 = 30 hours"'),
        'Five days down, six hours a day: it is thirty hours of work behind. That is the gap.',
        'Now it runs sixteen hours a day. But each day it still owes its normal six.',
        D('Write "gains: 16 − 6 = 10 hours a day → 30 ÷ 10 = 3 days"'),
        'So it gains only ten extra hours a day. Thirty hours behind, ten a day: three days.',
        'Why the difference? The normal work keeps coming every day. Only the extra part closes the gap.',
        'The trap is thirty divided by sixteen. And in motion you\'ll meet the same idea as a chase: the gap divided by the difference in speeds.'])])

    # ---- memory card rows ----
    c = M.card('mem-work-rate')
    rows = next(t for t in c['tables'] if t.get('title') == 'Question types')['rows']
    k = next(i for i, r in enumerate(rows) if r[0].startswith('Team')) + 1
    rows.insert(k, ['Two or more things change (only relations)',
                    'compare by factors: new $=$ old $\\times$ every factor; same way as is, opposite way flipped, shared cancels. '
                    '$\\frac34$ the hours, $\\frac23$ per hour, $8$ days $\\to$ $8\\times\\frac43\\times\\frac32=16$'])
    rows.append(['Catching up', 'gap $\\div$ difference in rates: $30$ h behind, $16-6=10$ more a day $\\to$ $3$ days'])
    c['tips'].append('A fixed amount more ("2 more an hour") is not a factor: give it a letter and write an equation.')


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
    _pm_add(M, 'wp26-p05', [r'Method 2 · Compare by factors: from $18$ to $27$ applications the work is $\times\frac32$ (time goes the same way). From $4$ to $3$ clerks the team is $\times\frac34$ (time goes the opposite way → flip to $\frac43$). $6\cdot\frac32\cdot\frac43=12$ minutes.'])
    _pm_add(M, 'wp26-p27', [r'Method 2 · Compare by factors: the items are $\times\frac{1{,}600}{960}=\frac53$ (more work, more machines: same way). The hours are $\times\frac43$ (more time, fewer machines → flip to $\frac34$). $8\cdot\frac53\cdot\frac34=10$ machines.'])
    _pm_add(M, 'wp26-p17', [r'Method 2 · Compare by factors: scanners $\times\frac DM$ and hours $\times3$. Both push the pages the same way: $L\cdot\frac DM\cdot3=\frac{3DL}{M}$.'])
    _pm_add(M, 'wp26-p12', [r'Method 2 · Compare by factors: the work goes from $p$ to $2q$ envelopes, $\times\frac{2q}{p}$, and the time goes the same way: $q\cdot\frac{2q}{p}=\frac{2q^2}{p}$.'])
    _pm_add(M, 'wp26-p13', [r'Method 2 · Compare by factors, starting from $120$ minutes: crates $\times\frac18$ (same way); workers $\times\frac15$ (fewer workers, more time → flip to $5$). $120\cdot\frac18\cdot5=75$ minutes.'])
    _pm_add(M, 'wp26-p16', [r'Method 2 · Compare by factors: in the same time the fast signal makes $\frac74$ as many cycles. A cycle goes the opposite way → flip to $\frac47$: $\frac35\cdot\frac47=\frac{12}{35}$ second.'])
    _pm_add(M, 'q-r26-t26-11', [r'Method 2 · Percent shares as weights (the weights are the hours): $3$ of the $5$ hours ($60\%$) are at $40$. Average $=30+0.6\cdot10=36$.'])


# ======================================================================================================
# 2026-10-06 renumber pass (teacher-approved): the English course must not look like the Hebrew one.
# Every Hebrew-derived question (guided wp26-g093 ... g105b, practice wp26-p01 ... p20) gets a new story and new
# numbers - same concept, same trap, same level, same methods (V method, adding rates, equalize the times, worker-hours,
# compare by factors) - and every guided solution video is rewritten to match. Hebrew-derived lesson examples
# (wp-092 rate, wp-094 add / subtract the rates, wp-099 worker-hours) get new numbers; the factors lesson slide that quotes
# the team question, the memory-card tip and the "Method 2" practice lines are updated. Practice clean-up 35 -> 25.
# Nothing in topic 26 is recorded. Runs last.
# ======================================================================================================
RN_RECORDED = set()   # no take of any topic-26 video in ~/Documents/Course.recordings (checked 2026-10-06)


def _rn_sub(M, vid, n, pairs):
    """Exact substring replacements on one slide: board items, item labels, spoken lines, draw cues."""
    if vid in RN_RECORDED: return
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = 0
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit += 1
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit += 1
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    M.touched_videos.add(vid)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides):
    """Rewrite the question slides 2, 3, ... of a guided solution video (None = keep that slide). Pre-loaded items stay."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) >= len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        if script is None: continue
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script)


def _tab(headers, rows, w=720, h=170):
    return dict(k='vis', v={'type': 'table', 'headers': list(headers), 'rows': [list(r) for r in rows]}, w=w, h=h)


def rn_lessons(M):
    # wp-092 #3: 18 labels in 3 minutes -> 6 per minute (Hebrew: 8 in 2 -> 4)  ==>  45 bottles in 5 minutes -> 9
    _rn_sub(M, 'wp-092', 3, [
        ('A machine prints 18 labels in 3 minutes', 'A machine fills 45 bottles in 5 minutes'),
        ('Eighteen labels — everything it did. The time? Three minutes.', 'Forty-five bottles — everything it did. The time? Five minutes.'),
        ('rate = 18 ÷ 3', 'rate = 45 ÷ 5'),
        ('Eighteen over three…', 'Forty-five over five…'),
        ('= 6 labels PER MINUTE', '= 9 bottles PER MINUTE'),
        ('…six. But careful — it\'s not "six". It\'s six labels PER MINUTE.', '…nine. But careful — it\'s not "nine". It\'s nine bottles PER MINUTE.'),
        ('Six labels is nobody\'s rate. Six labels per minute — that\'s a rate.', 'Nine bottles is nobody\'s rate. Nine bottles per minute — that\'s a rate.'),
        ('Even six over one is still a fraction.', 'Even nine over one is still a fraction.'),
        ('And eighteen in three minutes is the same rate as six in one.', 'And forty-five in five minutes is the same rate as nine in one.'),
    ])
    # wp-094 #2: 4 + 7 = 11 per minute (Hebrew 3 + 2 = 5)  ==>  5 + 8 = 13
    _rn_sub(M, 'wp-094', 2, [
        ('4 per minute $+$ 7 per minute $=$ 11 per minute', '5 per minute $+$ 8 per minute $=$ 13 per minute'),
        ('4 per minute + 7 per minute = 11 per minute', '5 per minute + 8 per minute = 13 per minute'),
        ('One makes four items a minute, the other seven.', 'One makes five items a minute, the other eight.'),
        ('Underline "11"', 'Underline "13"'),
        ('Together: eleven a minute.', 'Together: thirteen a minute.'),
        ('four hours and seven hours together is NOT eleven hours', 'five hours and eight hours together is NOT thirteen hours'),
    ])
    # wp-094 #3: 9 liters in, 4 out -> +5 (Hebrew: wash 5, dirty 2 -> 3)  ==>  12 in, 5 out -> +7
    _rn_sub(M, 'wp-094', 3, [
        ('9 liters in, 4 liters out — every minute', '12 liters in, 5 liters out — every minute'),
        ('9 − 4 = +5 per minute', '12 − 5 = +7 per minute'),
        ('Nine in, four out: the tank gains five liters a minute.', 'Twelve in, five out: the tank gains seven liters a minute.'),
    ])
    # wp-099 #2: 3 workers x 4 hours = 12 (Hebrew 2 x 3 = 6)  ==>  5 workers x 6 hours = 30
    _rn_sub(M, 'wp-099', 2, [
        ('Three workers, each working four hours.', 'Five workers, each working six hours.'),
        ('3 × 4 = 12 worker-hours', '5 × 6 = 30 worker-hours'),
        ('Only four hours pass on the clock. But there are twelve hours of work in there.',
         'Only six hours pass on the clock. But there are thirty hours of work in there.'),
        ('So one worker alone would need twelve hours.', 'So one worker alone would need thirty hours.'),
    ])
    # Compare by Factors #4 quotes the team question (old Q6 numbers) -> the new numbers
    M.set_slide('r26-t26-factors', 4, script=[
        A("'Team · Work · Time table' appears", TABLE(['Team', 'Work', 'Time'], [['3', '40', '5'], ['4', '96', '?']])),
        'Remember the question with three gardeners, forty trees, five hours? Then four gardeners, ninety-six trees.',
        D('Write "5 × 96/40 × 3/4 = 9"'),
        'Its first method was exactly this rule. More work pushes the time the same way — as is. More workers — the opposite way, flipped.',
        A("'V = factors for a 3-column table' appears", T(r'The V $=$ compare by factors for a $3$-column table', size=40, gap=50)),
        'The V is the same rule drawn as a picture, for a table where the middle is the product of the other two. It just does the flipping for you.',
        'Compare by factors works everywhere else too: price times quantity, three things multiplied, or a formula they give you.'])
    # memory card: the unit tip quoted the queue question (75 minutes)
    c = M.card('mem-work-rate')
    k = c['tips'].index('Minutes → hours: divide by 60. 75 minutes = 1.25 hours.')
    c['tips'][k] = 'Minutes → hours: divide by 60. 40 minutes = ⅔ hour (not 0.4).'


def rn_guided(M):
    # ---------- Q1 g093: robot, x in y minutes, rate x3, 4y minutes -> 12x (Hebrew: x in y, x2, 3y -> 6x)
    #            ==>  volunteer folds x flyers in y minutes, rate x3, 5y minutes -> 15x
    q = 'wp26-g093'
    _rn_q(M, q, 'A volunteer folds $x$ flyers in $y$ minutes at a constant rate, where $x$ and $y$ are positive. '
                'How many flyers will she fold in $5y$ minutes if her rate becomes 3 times as great?',
          ['$8x$', '$\\frac{5x}{3}$', '$15x$', '$3x$'], 3, [
        'Two changes, and each one multiplies the output: rate $\\times3$, and time $\\times5$ (from $y$ to $5y$).',
        'Flyers: $x\\cdot3\\cdot5=15x$. The factors multiply; they do not add up to $8x$.',
        'Check with numbers: $x=4$, $y=2$. The old rate is 2 per minute, the new rate is 6 per minute, and in 10 minutes she folds $6\\times10=60=15\\cdot4$ flyers ✓.'])
    _rn_video(M, q, [[
        "The table: flyers and minutes. Row one is what they give us: x flyers in y minutes. Now the rate triples.",
        A('A table appears: flyers and minutes, three rows', _tab(['', 'Flyers', 'Minutes'], [['Now', 'x', 'y'], ['Rate × 3', '', 'y'], ['Rate × 3, longer', '', '5y']], h=190)),
        "Same time, triple the rate — triple the flyers.",
        D('In the row "Rate × 3" write "3x"'),
        "So: 3x flyers in y minutes.",
        "Now the time goes from y to 5y. That's times five.",
        D('Draw an arrow "×5" down the minutes column'),
        "More time, same rate — the work grows by the same factor.",
        D('In the last row write "15x"'),
        "Times five on the flyers too: fifteen x.",
        "Read it across instead? Same thing: 5y minutes at 3x per y minutes — fifteen x.",
        D('Circle choice 3'),
        "Fifteen x. Choice three.",
    ], [
        "Ratios not your thing? Use the triangle value: multiply along the diagonal and divide by what's left.",
        D('Write "? = (5y · 3x) ÷ y"'),
        "Five y times three x, divided by y.",
        D('Cancel the y\'s and write "= 15x"'),
        "The y's cancel. Fifteen x.",
        "Careful: the two changes multiply — three times five. Don't add them to eight.",
        D('Circle choice 3'),
    ], [
        "Or use the formula. Rate is work over time.",
        D('Write "rate = x/y flyers per minute"'),
        "x flyers in y minutes: x over y per minute.",
        D('Write "new rate = 3x/y"'),
        "Three times as fast: three x over y.",
        D('Write "work = 3x/y × 5y = 15x"'),
        "Work is rate times time. The time is five y. The y's cancel: fifteen x.",
        "Careful: the two changes multiply — three times five. Don't add them to eight.",
        D('Circle choice 3'),
    ], [
        "Letters in the answers? Plug in easy numbers.",
        D('Write "x = 4, y = 2 → 2 per minute"'),
        "Say four flyers in two minutes. That's two a minute.",
        D('Write "× 3 → 6 per minute · 5y = 10 minutes → 6 × 10 = 60"'),
        "Three times as fast: six a minute. Five y is ten minutes. Sixty flyers.",
        D('Write "8x = 32 · 5x/3 = 20/3 · 15x = 60 ✓ · 3x = 12"'),
        "Now put x equals four into each choice. Only fifteen x gives sixty.",
        D('Circle choice 3'),
        "Pick numbers that are not zero or one, and not equal to each other. Then only one choice survives.",
    ]])

    # ---------- Q3 g095: 2 inlets 8 h, drain 12 h, 9 a.m. -> 3 p.m. (Hebrew: 6 h / 9 h, 8:00 -> 12:30)
    #            ==>  2 hoses fill a pond in 15 h each, outlet empties it in 20 h, 7 a.m. -> 7 p.m.
    q = 'wp26-g095'
    _rn_q(M, q, 'Two identical hoses each fill a pond in 15 hours. An outlet pipe empties a full pond in 20 hours. '
                'At 7 a.m. the pond is empty, and both hoses and the outlet pipe are opened. At what time is the pond full?',
          ['2:30 p.m.', '7 p.m.', '5 p.m.', '9 p.m.'], 2, [
        'Rates in ponds per hour: $\\frac1{15}+\\frac1{15}-\\frac1{20}=\\frac4{60}+\\frac4{60}-\\frac3{60}=\\frac5{60}=\\frac1{12}$.',
        'One pond at $\\frac1{12}$ of a pond per hour takes 12 hours. 7 a.m. plus 12 hours is 7 p.m.',
        'Trap: without the outlet, $\\frac2{15}$ of a pond per hour gives 7.5 hours (2:30 p.m.).'])
    _rn_sub(M, 'solve-' + q, 1, [('Two pumps fill, one empties.', 'Two hoses fill, one pipe empties.')])
    _rn_video(M, q, [[
        "Find the combined rate of all three.",
        A("'One job = 1 → 15 hours: 1/15 per hour' appears", T(r'One job $=1$ $\to$ $15$ hours: $\frac1{15}$ per hour', 36)),
        "We don't know the pond's size — so call the whole pond one job.",
        "Rate is work over time. One pond in fifteen hours — one fifteenth of a pond per hour.",
        D('Write "1/15 + 1/15"'),
        "Two identical hoses: one fifteenth plus one fifteenth.",
        "The outlet works against them — so it gets a minus.",
        D('Write "− 1/20"'),
        "It empties a pond in twenty hours: minus one twentieth.",
        D('Write "= 4/60 + 4/60 − 3/60 = 5/60 = 1/12"'),
        "Common denominator: sixty. Together: five sixtieths — one twelfth.",
        "What does one twelfth mean? Work over time — one pond in twelve hours.",
        D('Write "1 pond in 12 hours"'),
        "They started at seven in the morning.",
        D('Write "7 a.m. + 12 h = 7 p.m." and circle choice 2'),
        "Seven plus twelve hours: seven in the evening. Choice two.",
        "They asked for a clock time — don't stop at twelve hours.",
        "And the trap: forget the outlet, and you get seven and a half hours — two thirty, the trap in choice one.",
    ], [
        "Fractions bothering you? Choose a pond of sixty units — the LCM of fifteen and twenty.",
        D('Write "hose 4/h · hose 4/h · outlet −3/h"'),
        "Each hose adds four units an hour. The outlet takes three.",
        D('Write "4 + 4 − 3 = 5 per hour → 60 ÷ 5 = 12 h"'),
        "Net five an hour. Sixty units: twelve hours. Same answer.",
        D('Circle choice 2'),
    ]])

    # ---------- Q4 g096: machines 4 h and 6 h -> 144 min (Hebrew: 3 h and 2 h -> 72 min)
    #            ==>  printers 6 h and 10 h -> 225 min
    q = 'wp26-g096'
    _rn_q(M, q, 'Printer A prints one batch of catalogs in 6 hours, while printer B prints the same batch in 10 hours. '
                'If they work together at their usual constant rates, how many minutes do they need for one batch?',
          ['180', '225', '480', '240'], 2, [
        'Equalize the times: in 30 hours A prints $30\\div6=5$ batches and B prints $30\\div10=3$. Together: 8 batches in 30 hours.',
        'One batch: $\\frac{30}{8}=\\frac{15}{4}$ hours $=\\frac{15}{4}\\times60=225$ minutes.',
        'Shortcut for two workers: $\\frac{6\\cdot10}{6+10}=\\frac{60}{16}=3.75$ hours $=225$ minutes.'])
    _rn_sub(M, 'solve-' + q, 1, [('Two machines, two different times.', 'Two printers, two different times.')])
    _rn_video(M, q, [[
        "Printer A: one batch in six hours. Printer B: one batch in ten.",
        "Different times — so I can't just add them.",
        "Equalize the times first. A time that works for both: thirty — a common multiple of six and ten.",
        A('A table appears: A and B over 30 hours', _tab(['Printer', 'Batches', 'Hours'],
          [['A', '1', '6'], ['B', '1', '10'], ['A', '', '30'], ['B', '', '30'], ['Together', '', '30']], h=250)),
        D('Fill in A: 5, B: 3'),
        "Six hours to thirty is times five: A prints five batches. Ten to thirty is times three: B prints three.",
        D('Fill in Together: 8'),
        "Now I can add. Eight batches in the same thirty hours — they work side by side, so we add batches, not hours.",
        "They want ONE batch. Eight down to one — divide by eight. Same for the time.",
        D('Write "1 batch in 30/8 = 15/4 hours"'),
        "Thirty eighths — that's fifteen quarters of an hour. They want minutes — times sixty.",
        D('Write "15/4 × 60 = 225" and circle choice 2'),
        "Two hundred twenty-five minutes. Choice two.",
    ], [
        "Same thing with rates: a sixth of a batch an hour, plus a tenth.",
        D('Write "1/6 + 1/10 = 8/30 = 4/15 → 15/4 h = 225 min"'),
        "Four fifteenths per hour. One batch: fifteen quarters of an hour — two hundred twenty-five minutes.",
        "Sense check: together must beat A's six hours — and two printers as fast as A would need three. Three hours forty-five sits right in between.",
        D('Write "shortcut: (6 · 10)/(6 + 10) = 60/16 = 3.75 h"'),
        "Or the two-worker shortcut: six times ten over six plus ten. Three point seven five hours. Same answer.",
        D('Circle choice 2'),
    ]])

    # ---------- Q6 g098: 5 workers 30 boards 4 h; 8 workers 72 boards -> 6 (Hebrew: 4 / 20 / 3; 6 / 60 -> 6)
    #            ==>  3 gardeners 40 trees 5 h; 4 gardeners 96 trees -> 9
    q = 'wp26-g098'
    _rn_q(M, q, 'Three identical gardeners plant 40 trees in 5 hours. How many hours do four such gardeners need to plant 96 trees?',
          ['16', '9', '12', '7.2'], 2, [
        'Table (team, work, time). Row 1: 3, 40, 5. Row 2: 4, 96, ?.',
        'More work means more time ($\\times\\frac{96}{40}$); more workers means less time ($\\times\\frac34$): $5\\times\\frac{96}{40}\\times\\frac34=5\\times\\frac{12}5\\times\\frac34=9$ hours.',
        'Or worker-hours: $3\\times5=15$ worker-hours plant 40 trees, so 96 trees need $15\\times\\frac{96}{40}=36$ worker-hours, and $36\\div4=9$ hours.'])
    TBL = TABLE(['Team', 'Work', 'Time'], [['3', '40', '5'], ['4', '96', '?']])
    _rn_video(M, q, [[
        "Identical workers, a group of them — team question. Into the table.",
        A('The table appears: 3 · 40 · 5 and 4 · 96 · ?', TBL),
        "We want the time. So ask: what does each change do to the time?",
        "Work went from forty to ninety-six trees. More work — more time, same factor.",
        D('Write "5 × 96/40"'),
        "The team went from three to four. More workers — LESS time. So flip it.",
        D('Write "× 3/4"'),
        "Same factor for the work, the opposite factor for the team.",
        D('Write "= 5 × 12/5 × 3/4 = 9"'),
        "Ninety-six over forty is twelve fifths. The fives cancel. Twelve times three over four — nine hours.",
        D('Circle choice 2'),
        "Nine. Choice two.",
    ], [
        "Now the method that solves these in seconds — no thinking about directions at all.",
        A('The same table appears', TBL),
        "The blank is in row two, in the Time column.",
        D('Draw a V through 3, 96 and 5'),
        "Draw a V: top-left, down to the bottom-middle, up to the top-right. Three, ninety-six, five.",
        "Multiply the three numbers on the V. Divide by the other two.",
        D('Write "? = (3 · 96 · 5) ÷ (40 · 4)"'),
        "Three times ninety-six times five, over forty times four.",
        D('Cancel, then write "= 9"'),
        "Cancel before you multiply: nine hours.",
        D('Circle choice 2'),
        "Nine. Choice two.",
    ], [
        A('The V rule appears', T('Blank in Team or Time: V = top-left $\\times$ bottom-middle $\\times$ top-right, $\\div$ the other two', size=38, gap=40)),
        "Here's the general rule. Always put the question row second.",
        "Blank in the Team column or the Time column? Same V. Top-left, bottom-middle, top-right. Divide by the other two numbers.",
        A('The upside-down V rule appears', T('Blank in Work: upside-down V = bottom-left $\\times$ top-middle $\\times$ bottom-right, $\\div$ the other two', size=38, gap=40)),
        "Blank in the Work column? Turn the V upside down. Bottom-left, top-middle, bottom-right.",
        A('An example table appears', TABLE(['Team', 'Work', 'Time'], [['3', '40', '5'], ['4', '?', '6']])),
        "Example: three gardeners plant forty trees in five hours. How many trees do four gardeners plant in six hours?",
        D('Draw an upside-down V through 4, 40 and 6; write "? = (4 · 40 · 6) ÷ (3 · 5) = 960 ÷ 15 = 64"'),
        "Four, forty, six on the upside-down V. Divide by three and five. Sixty-four trees.",
        "Sense check: more gardeners AND more hours — so more than forty trees. Good.",
    ], [
        "One more view. Three gardeners for five hours: fifteen worker-hours planted forty trees.",
        D('Write "15 → 40 trees · 96 trees → 36 worker-hours → 36 ÷ 4 = 9"'),
        "Ninety-six trees need thirty-six worker-hours. Four gardeners share them: nine hours.",
        D('Circle choice 2'),
    ]])

    # ---------- Q7 g100: path 18 x 8 + 12 x 7 = 228 (Hebrew: road 20 x 10 + 15 x 10 = 350)
    #            ==>  fence 14 x 9 + 6 x 11 = 192
    q = 'wp26-g100'
    _rn_q(M, q, 'A fence around a park is completed by 14 workers working for 9 days, followed by 6 workers working for 11 days. '
                'All work at the same constant rate. How many days would one worker need to complete the whole fence alone?',
          ['126', '400', '192', '200'], 3, [
        'Worker-days: $14\\times9=126$ and $6\\times11=66$. Total: $126+66=192$ worker-days.',
        'One worker does one worker-day each day, so alone the fence takes 192 days.'])
    _rn_video(M, q, [[
        "How long would one worker need for the whole fence? Count the worker-days.",
        "Think like the contractor: how many days of wages do I pay?",
        D('Write "14 × 9 = 126"'),
        "First phase: fourteen workers, nine days each — a hundred twenty-six worker-days.",
        D('Write "6 × 11 = 66"'),
        "Second phase: six workers, eleven days each — sixty-six.",
        D('Write "126 + 66 = 192" and circle choice 3'),
        "Together a hundred ninety-two worker-days. That's how long one worker alone would need. Choice three.",
        "Don't add fourteen and six and multiply by twenty — twenty workers never worked together.",
    ]])

    # ---------- A1 g101: 3 fast = 2 x 9 standard -> 6 (Hebrew: 4 fast = 2 x 6 slow -> 3)
    #            ==>  5 large dishwashers = 2 x 10 small -> 4
    q = 'wp26-g101'
    _rn_q(M, q, 'The combined rate of 5 large dishwashers is twice the combined rate of 10 small dishwashers. '
                'Dishwashers of the same type are identical. How many times as fast is one large dishwasher as one small dishwasher?',
          ['1', '4', '2', '10'], 2, [
        'Let $L$ be the rate of one large dishwasher and $S$ the rate of one small dishwasher.',
        'The large team is twice as fast, so the 2 goes on the smaller side: $5L=2\\cdot10S=20S$, therefore $L=4S$.',
        'Trap: doubling the larger side gives $2\\cdot5L=10S$, so $L=S$ (choice 1).'])
    _rn_video(M, q, [[
        "Call a large dishwasher L. A small one, S.",
        D('Write "5L" and "10S"'),
        "Five large dishwashers: 5L. Ten small: 10S.",
        "I want them equal — but they're not. The large team is TWICE as fast.",
        "So who gets multiplied by two? Many students double the bigger side. That only makes it bigger.",
        "Rule: the times two goes on the SMALLER side. Then both sides are equal.",
        D('Write "5L = 2 · 10S"'),
        D('Write "5L = 20S → L = 4S"'),
        "Five L equals twenty S. Divide by five: one large dishwasher equals four small ones.",
        D('Circle choice 2'),
        "Four. Choice two.",
        "Double the wrong side, and you get ten L equals ten S — one. That's the trap in choice one.",
    ], [
        "Not sure how to build the equation? Plug in and start rolling.",
        "Say one small dishwasher washes one plate a minute.",
        D('Write "1 small: 1 → 10 small: 10"'),
        "Ten of them: ten plates a minute.",
        D('Write "5 large: 2 × 10 = 20 → 1 large: 4"'),
        "The large team does twice that — twenty. Five large dishwashers, twenty plates: four each.",
        "Four times the small one. You didn't need to know where to start — you just started.",
        D('Circle choice 2'),
    ]])

    # ---------- A2 g102: +24/h, 35 per 75 min, 50 at start, 5 h -> 30 (Hebrew: mole 20/h, gardener 30 per 75 min, 40, 5 h -> 20)
    #            ==>  bakery queue: +18 orders/h, baker 15 per 40 min, 60 at start, 4 h -> 42
    q = 'wp26-g102'
    _rn_q(M, q, 'Customers add 18 orders to a bakery’s queue each hour. The baker completes 15 orders every 40 minutes. '
                'There are initially 60 orders in the queue. At these constant rates, how many orders are in the queue after 4 hours?',
          ['72', '24', '42', '12'], 3, [
        'Customers: $18\\times4=72$ orders added.',
        '4 hours $=240$ minutes $=6\\times40$ minutes, so the baker completes $6\\times15=90$ orders.',
        'In the queue: $60+72-90=42$ orders.',
        'Trap: taking "15 every 40 minutes" as 15 per hour gives $60+72-60=72$.'])
    _rn_video(M, q, [[
        "Start with some order. Customers add eighteen orders an hour.",
        D('Write "customers: 18 per hour × 4 = 72"'),
        "Four hours — times four: seventy-two new orders.",
        "The baker: fifteen orders in forty minutes. That's minutes — so the four hours must become minutes too.",
        D('Write "4 hours = 4 × 60 = 240 minutes"'),
        A("'Combine only matching units' appears", T('Combine only matching units', 36)),
        "Combine only matching units — convert first.",
        "Hours to minutes: times sixty. Two hundred forty minutes.",
        D('Write "40 → 240 is × 6 → 15 × 6 = 90"'),
        "Forty to two hundred forty is exactly times six. So ninety orders completed.",
        "Don't see the six? Cross-multiply: fifteen times two hundred forty over forty. Reduce by forty first.",
        D('Write "60 + 72 − 90 = 42" and circle choice 3'),
        "Sixty waiting, plus seventy-two, minus ninety: forty-two. Choice three.",
    ], [
        "Or turn the minutes into hours. Minutes to hours: divide by sixty.",
        D('Write "40 min = 40/60 h = 2/3 h"'),
        "Forty minutes is forty sixtieths — two thirds of an hour. Not zero point four!",
        D('Write "2/3 × 6 = 4 → 15 × 6 = 90"'),
        "Two thirds of an hour, times six, is four hours. Times six again: ninety.",
        "Same order as before: forty-two left.",
        D('Circle choice 3'),
    ]])   # slide 4 (catching up) stays

    # ---------- A4 g103: 360 m2 / 3 h, 40 m2 / 2 h, 140 m2 -> 60 min (Hebrew: 300 / 2 h, 50 / 3 h, 100 -> 36 min)
    #            ==>  polishers 200 m2 / 4 h, 30 m2 / 6 h, 110 m2 -> 120 min
    q = 'wp26-g103'
    _rn_q(M, q, 'Polisher A polishes 200 m² of floor in 4 hours. Polisher B polishes 30 m² in 6 hours. '
                'Working together at these constant rates, how many minutes do they need for 110 m²?',
          ['120', '66', '132', '150'], 1, [
        'Equalize to 12 hours: A polishes $200\\times3=600$ m², B polishes $30\\times2=60$ m². Together: 660 m² in 12 hours.',
        '$110=\\frac{660}6$, so the time is $12\\div6=2$ hours $=120$ minutes.',
        'Sense check: A alone does 50 m² per hour, so 110 m² takes it 2.2 hours = 132 minutes. Together is less than 132 and more than $132\\div2=66$. Only 120 fits.'])
    _rn_video(M, q, [[
        "A: two hundred square meters in four hours. B: thirty in six hours.",
        "To add them, the times must match. Common multiple of four and six: twelve hours.",
        A('A table appears: A and B over 12 hours', _tab(['Polisher', 'm²', 'Hours'],
          [['A', '200', '4'], ['B', '30', '6'], ['A', '', '12'], ['B', '', '12'], ['Together', '', '12']], h=250)),
        D('Fill in A: 600, B: 60, Together: 660'),
        "A: times three — six hundred. B: times two — sixty. Together, six hundred sixty in the same twelve hours.",
        "They want a hundred ten. That's one sixth of six hundred sixty — so one sixth of the time.",
        D('Write "12 h ÷ 6 = 2 h = 120 min" and circle choice 1'),
        "Two hours. In minutes: a hundred twenty. Choice one.",
    ], [
        "Now the psychometric way — estimate the size.",
        D('Write "A alone: 110 at 50/h → 2.2 h = 132 min"'),
        "A alone does fifty an hour. A hundred ten takes it two point two hours — a hundred thirty-two minutes.",
        "B helps — so together it's LESS than a hundred thirty-two.",
        D('Cross out choices 3 and 4'),
        "A hundred thirty-two and a hundred fifty are out.",
        "Two polishers as fast as A would take half — sixty-six minutes. But B is much slower. B helps, but only a little.",
        "Like the elephant and the mouse walking along — and the mouse says: look how much dust WE'RE making.",
        D('Cross out choice 2 and circle choice 1'),
        "So more than sixty-six, less than a hundred thirty-two. Only a hundred twenty fits.",
    ]])

    # ---------- A5 g104: all three 8 h, two of them 16 h -> 1/16 (Hebrew: 6 h, 12 h -> 1/12)
    #            ==>  Omar, Priya and Sam: 9 h, 18 h -> 1/18
    q = 'wp26-g104'
    _rn_q(M, q, 'Omar, Priya and Sam each work at a constant rate. Together they complete a job in 9 hours. '
                'Omar and Priya together complete it in 18 hours. What fraction of the job does Sam complete in one hour?',
          ['$\\frac19$', '$\\frac1{27}$', '$\\frac1{18}$', '$\\frac16$'], 3, [
        'All three: 1 job in 9 hours, so 2 jobs in 18 hours. Omar and Priya: 1 job in 18 hours.',
        'Sam does the difference: $2-1=1$ job in 18 hours, which is $\\frac1{18}$ of the job per hour. (With rates: $\\frac19-\\frac1{18}=\\frac1{18}$.)'])
    _rn_video(M, q, [[
        "Omar, Priya and Sam. All three: one job in nine hours. Omar and Priya: one job in eighteen.",
        "I don't know how Omar and Priya split the work. And I don't care.",
        "Maybe they share it equally. Maybe Priya sits with a coffee while Omar does everything. Together they do one job in eighteen hours.",
        D('Bracket "Omar and Priya" and write "one worker"'),
        "So merge them into one worker — call it Omar-Priya. Now it's a normal two-worker question.",
        "Equalize the times: eighteen hours.",
        D('Write "all three: 2 jobs in 18 h"'),
        "All three in eighteen hours: two jobs.",
        D('Write "Omar-Priya: 1 job in 18 h → Sam: 1 job in 18 h"'),
        "Omar-Priya does one of them. So Sam does the other — one job in eighteen hours.",
        D('Write "1/18 per hour" and circle choice 3'),
        "In one hour: one eighteenth. Choice three.",
    ], [
        "Here's the flash of insight.",
        "All three work for nine hours. Omar-Priya needs eighteen for a whole job — so in nine hours they do half.",
        D('Write "9 h: Omar-Priya = ½ → Sam = ½"'),
        "So Sam does the other half. Sam alone works exactly as fast as Omar and Priya together.",
        "Half a job in nine hours: a whole job in eighteen. One eighteenth per hour.",
        D('Circle choice 3'),
    ]])

    # ---------- A6 g105: 8 makers cabinet 6 h, 9 makers bench 8 h, both in 24 h -> 5 (Hebrew: 10 table 3 h, 9 chair 5 h, 15 h -> 5)
    #            ==>  event crew: 12 workers stage 2 h, 14 workers seating 4 h, both in 8 h -> 10
    q = 'wp26-g105'
    _rn_q(M, q, 'Twelve identical workers can set up one stage in 2 hours. Fourteen such workers can set up the seating in 4 hours. '
                'How many workers are needed to set up one stage and the seating in 8 hours?',
          ['26', '10', '13', '7'], 2, [
        'Worker-hours: the stage needs $12\\times2=24$, the seating needs $14\\times4=56$. Total: $24+56=80$.',
        'In 8 hours: $80\\div8=10$ workers (3 on the stage, 7 on the seating).'])
    _rn_video(M, q, [[
        '"Identical workers" — a team question. But two teams: one on the stage, one on the seating, working at the same time.',
        A('Two tables appear: stage and seating', _tab(['', 'Team', 'Work', 'Time'],
          [['Stage', '12', '1', '2'], ['', '?', '1', '8'], ['Seating', '14', '1', '4'], ['', '?', '1', '8']], w=760, h=250)),
        D('Draw a V through 12, 1, 2 and write "(12 · 1 · 2) ÷ (1 · 8) = 3"'),
        "Stage: V through twelve, one, two. Multiply, divide by what's left: three workers.",
        D('Draw a V through 14, 1, 4 and write "(14 · 1 · 4) ÷ (1 · 8) = 7"'),
        "Seating: fourteen times one times four, over eight: seven workers.",
        D('Write "3 + 7 = 10" and circle choice 2'),
        "Three on the stage, seven on the seating, both working the same eight hours. Ten. Choice two.",
    ], [
        "Faster here: ratios. The job didn't change — only the time.",
        "More time — fewer workers.",
        D('Write "2 → 8 h: × 4 → 12 ÷ 4 = 3"'),
        "Stage: four times the time — so a quarter of the workers. Three.",
        D('Write "4 → 8 h: × 2 → 14 ÷ 2 = 7"'),
        "Seating: twice the time — half the workers. Seven. Send the rest home.",
        "Only ONE thing changes? Ratios. Two things change? The V method.",
        D('Circle choice 2'),
    ], [
        "And the boss paying salaries.",
        D('Write "12 × 2 = 24 · 14 × 4 = 56"'),
        "The stage takes twenty-four worker-hours. The seating, fifty-six.",
        D('Write "24 + 56 = 80 → 80 ÷ 8 = 10"'),
        "Eighty worker-hours, done in eight hours: ten workers.",
        D('Circle choice 2'),
    ]])

    # ---------- A7 g105b: feed for 240 animals 6 days -> 90 animals 16 days (Hebrew: water, 220 dunam 5 days -> 100 dunam 11)
    #            ==>  hay for 200 sheep 9 days -> 150 sheep 12 days
    q = 'wp26-g105b'
    _rn_q(M, q, 'A supply of hay is enough for 200 identical sheep for 9 days. Each sheep eats the same constant amount per day. '
                'For how many days would that supply feed 150 sheep?',
          ['12', '18', '6.75', '15'], 1, [
        'Sheep-days (like worker-days): $200\\times9=1{,}800$.',
        '150 sheep: $1{,}800\\div150=12$ days.'])
    _rn_sub(M, 'solve-' + q, 1, [('Last question.', 'The last team question.')])   # (a factors question follows it)
    _rn_video(M, q, [[
        "This time let's start the psychometric way — estimate.",
        "Fewer sheep — the same hay lasts LONGER. More than nine days.",
        D('Cross out choice 3'),
        "Six point seven five is out — that's fewer days.",
        D('Write "200 → 100 sheep: 9 → 18 days"'),
        "Half of two hundred is a hundred. Half the sheep — double the days: eighteen.",
        D('Cross out choice 2'),
        "But a hundred fifty is more than a hundred — so FEWER than eighteen days. Eighteen is out.",
        D('Write "150 = 3/2 of 100 → 18 × 2/3 = 12"'),
        "A hundred fifty is three halves of a hundred — so two thirds of the time. Twelve.",
        D('Circle choice 1'),
    ], [
        "Plug in. Say each sheep eats one unit a day.",
        D('Write "200 × 9 = 1,800 units"'),
        "Two hundred sheep, nine days: one thousand eight hundred units of hay.",
        D('Write "1,800 ÷ 150 = 12"'),
        "A hundred fifty sheep eat a hundred fifty a day. Eighteen hundred over a hundred fifty: twelve days.",
        D('Circle choice 1'),
    ], [
        "It's even a team question — once you see who the team is.",
        "The sheep are the workers. Their job — eating. The hay is the work, and it never changes.",
        A('The table appears: 200 · 1 · 9 and 150 · 1 · ?', TABLE(['Team', 'Work', 'Time'], [['200', '1', '9'], ['150', '1', '?']])),
        D('Draw a V through 200, 1, 9 and write "(200 · 1 · 9) ÷ (150 · 1) = 12"'),
        "V method: two hundred times one times nine, over a hundred fifty. Twelve.",
        D('Circle choice 1'),
        "The hard part was seeing who the team is. If you can't — estimate or plug in.",
    ]])


def rn_practice_questions(M):
    S = _rn_q
    # p01: Eva 4 boxes / 6 min, Max 5 / 8 min, 24 min -> 31  ==>  Nora 3 gifts / 5 min, Theo 7 / 10 min, 30 min -> 39
    S(M, 'wp26-p01', 'Nora wraps 3 gifts in 5 minutes. Theo ties ribbons on 7 gifts in 10 minutes. Each of them works for 30 minutes '
                     'at these constant rates. What is the total number of gifts wrapped by Nora and gifts tied by Theo?',
      ['36', '42', '39', '33'], 3, [
        'Nora: $30=6\\times5$, so she wraps $6\\times3=18$ gifts. Theo: $30=3\\times10$, so he ties $3\\times7=21$ gifts.',
        'Total: $18+21=39$.'])
    # p02: A x posters/h, B 3x as fast, 4 h -> 12x  ==>  oven A x loaves/h, B 4x as fast, 5 h -> 20x
    S(M, 'wp26-p02', 'Oven A bakes $x$ loaves per hour. Oven B is 4 times as fast. How many loaves does B bake in 5 hours?',
      ['$9x$', '$\\frac{x}{20}$', '$20x$', '$\\frac{5x}{4}$'], 3, [
        'B bakes $4x$ loaves per hour.', 'In 5 hours: $5\\cdot4x=20x$ loaves.'])
    # p03: 6 small/h or 4 large/h, 3 small + 5 large -> 1 h 45  ==>  tailor 12 pants/h or 2 coats/h, 8 pants + 3 coats -> 2 h 10
    S(M, 'wp26-p03', 'A tailor hems 12 pairs of pants per hour or 2 coats per hour. How long does it take to hem 8 pairs of pants '
                     'and 3 coats, one after another?',
      ['1 hour 50 minutes', '2 hours 10 minutes', '2 hours 30 minutes', '2 hours 20 minutes'], 2, [
        'Pants: $8\\div12=\\frac23$ hour $=40$ minutes. Coats: $3\\div2=1\\frac12$ hours $=90$ minutes.',
        'Total: $40+90=130$ minutes $=$ 2 hours 10 minutes.'])
    # p04: 7 packers make 96 more than 3 -> 24  ==>  9 sewing machines make 140 more than 4 -> 28
    S(M, 'wp26-p04', 'Identical sewing machines work at a constant rate. Nine machines sew 140 more shirts in a day than four machines do. '
                     'How many shirts does one machine sew per day?',
      ['20', '35', '28', '14'], 3, [
        'Nine machines sew 140 more shirts than four machines because of the $9-4=5$ extra machines.',
        'One machine: $140\\div5=28$ shirts per day.'])
    # p05: 4 clerks 18 / 6 min; 3 clerks 27 -> 12  ==>  6 cashiers 45 customers / 10 min; 4 cashiers 54 -> 18
    S(M, 'wp26-p05', 'Six cashiers serve 45 customers in 10 minutes. At the same individual rate, how many minutes do four cashiers '
                     'need to serve 54 customers?',
      ['12', '18', '8', '27'], 2, [
        'V method (team, work, time). Row 1: 6, 45, 10. Row 2: 4, 54, ?.',
        '$?=\\frac{6\\cdot54\\cdot10}{45\\cdot4}=\\frac{3240}{180}=18$ minutes.',
        'Method 2 · Compare by factors: from $45$ to $54$ customers the work is $\\times\\frac65$ (time goes the same way). '
        'From $6$ to $4$ cashiers the team is $\\times\\frac23$ (time goes the opposite way → flip to $\\frac32$). $10\\cdot\\frac65\\cdot\\frac32=18$ minutes.'])
    # p06: machine 480 parts/h, person 1 per 12 min -> 96  ==>  machine 360 jars/h, worker 1 per 4 min -> 24
    S(M, 'wp26-p06', 'A machine seals 360 jars per hour. One worker seals one jar every 4 minutes. How many workers working together '
                     'match the machine’s rate?',
      ['90', '6', '24', '30'], 3, [
        'One worker: $60\\div4=15$ jars per hour.', '$360\\div15=24$ workers.'])
    # p07: 4 pumps 9 h + a pump twice as fast -> 6  ==>  5 printers 8 h + a printer three times as fast -> 5
    S(M, 'wp26-p07', 'Five identical printers finish a print run in 8 hours. A sixth printer works three times as fast as one of the '
                     'original printers. How many hours do all six printers need together?',
      ['$6\\frac23$', '5', '4', '6'], 2, [
        'The job: $5\\times8=40$ printer-hours (ordinary printers). The fast printer counts as 3 ordinary printers, so the team is worth $5+3=8$ printers.',
        '$40\\div8=5$ hours. (Trap: counting the fast printer as an ordinary one gives $40\\div6=6\\frac23$.)'])
    # p08: 5 x 8 + 6 x 10 = 100 worker-days, 10 workers -> 10  ==>  4 x 9 + 8 x 6 = 84 painter-days, 12 painters -> 7
    S(M, 'wp26-p08', 'Four painters finish house A in 9 days. Eight equally fast painters finish house B in 6 days. '
                     'How many days do twelve such painters need to finish both houses?',
      ['15', '6', '7', '8'], 3, [
        'House A: $4\\times9=36$ painter-days. House B: $8\\times6=48$ painter-days. Total: 84.',
        'Twelve painters: $84\\div12=7$ days.'])
    # p09: 24 plain or 8 decorated mugs a day, 48 each -> 12 (not 16)  ==>  20 small or 5 large bowls, 40 each -> 8 (not 12.5)
    S(M, 'wp26-p09', 'A potter can make 20 small bowls or 5 large bowls in one day. She makes 40 of each kind. '
                     'What is her average number of bowls made per working day?',
      ['12.5', '8', '10', '6'], 2, [
        'Small: $40\\div20=2$ days. Large: $40\\div5=8$ days.',
        'Average rate $=$ total work $\\div$ total time $=80\\div10=8$ bowls per day (not the average of 20 and 5, which is 12.5).'])
    # p11: pipes 6 h and 12 h -> 4  ==>  pumps 5 h and 20 h -> 4 hours
    S(M, 'wp26-p11', 'Pump A fills a small reservoir in 5 hours, and pump B fills it in 20 hours. How many hours do they take together, '
                     'starting with the reservoir empty?',
      ['12.5', '2.5', '4', '10'], 3, [
        'A: $\\frac15$ of the reservoir per hour. B: $\\frac1{20}$. Together: $\\frac4{20}+\\frac1{20}=\\frac5{20}=\\frac14$, so 4 hours.',
        'Shortcut: $\\frac{5\\cdot20}{5+20}=\\frac{100}{25}=4$.'])
    # p12: p envelopes in q minutes, 2q envelopes -> 2q^2/p  ==>  m bottles in n minutes, 3n bottles -> 3n^2/m
    S(M, 'wp26-p12', 'A machine labels $m$ bottles in $n$ minutes at a constant rate. How many minutes does it need to label $3n$ bottles?',
      ['$\\frac{3m^2}{n}$', '$\\frac{3n^2}{m}$', '$\\frac{3m}{n}$', '$\\frac{n^2}{3m}$'], 2, [
        'One bottle takes $\\frac nm$ minutes. For $3n$ bottles: $3n\\cdot\\frac nm=\\frac{3n^2}{m}$ minutes.',
        'Check with numbers: $m=3$, $n=6$. One bottle takes $2$ minutes, and $3n=18$ bottles take $36$ minutes. $\\frac{3\\cdot6^2}{3}=36$ ✓.',
        'Method 2 · Compare by factors: the work goes from $m$ to $3n$ bottles, $\\times\\frac{3n}{m}$, and the time goes the same way: $n\\cdot\\frac{3n}{m}=\\frac{3n^2}{m}$.'])
    # p13: 5 workers 8 crates 2 h -> one crate 75 min  ==>  3 workers 12 boxes 3 h -> 45 min
    S(M, 'wp26-p13', 'Three identical workers pack 12 boxes in 3 hours. How many minutes does one worker need to pack one box?',
      ['15', '5', '45', '60'], 3, [
        'The team works $3\\times3=9$ worker-hours for 12 boxes. One box: $9\\div12=0.75$ worker-hours.',
        'One worker needs 0.75 hours $=45$ minutes.',
        'Method 2 · Compare by factors, starting from $180$ minutes: boxes $\\times\\frac1{12}$ (same way); workers $\\times\\frac13$ '
        '(fewer workers, more time → flip to $3$). $180\\cdot\\frac1{12}\\cdot3=45$ minutes.'])
    # p14: 3 hoses 5 h, 2 of them 10 h -> 1/10  ==>  3 sprinklers 4 h, 2 of them 12 h -> 1/6
    S(M, 'wp26-p14', 'Three sprinklers together water a field in 4 hours. Two of those sprinklers together water the same field in 12 hours. '
                     'What fraction of the field does the third sprinkler water in one hour?',
      ['$\\frac{1}{4}$', '$\\frac{1}{6}$', '$\\frac{1}{3}$', '$\\frac{1}{12}$'], 2, [
        'The three sprinklers water $\\frac14$ of the field per hour. The two sprinklers water $\\frac1{12}$ per hour.',
        'The third sprinkler waters the difference: $\\frac14-\\frac1{12}=\\frac3{12}-\\frac1{12}=\\frac2{12}=\\frac16$ of the field per hour.'])
    # p15: 3 experts = 2 x 4 trainees -> 8/3  ==>  5 senior cooks = 2 x 3 junior cooks -> 6/5
    S(M, 'wp26-p15', 'Five senior cooks prepare twice as many meals per hour as three junior cooks. '
                     'What is one senior cook’s rate divided by one junior cook’s rate?',
      ['$\\frac{5}{6}$', '$\\frac{6}{5}$', '$\\frac{3}{10}$', '$\\frac{10}{3}$'], 2, [
        'Let $s$ be the rate of one senior cook and $j$ the rate of one junior cook.',
        'The seniors are twice as fast as a team, so the 2 goes on the smaller side: $5s=2\\cdot3j=6j$. Divide by $5j$: $\\frac sj=\\frac65$.'])
    # p16: slow signal 4 cycles = fast 7 cycles, slow cycle 3/5 s -> 12/35  ==>  drummers 5 beats = 8 beats, slow beat 2/3 s -> 5/12
    #      (review 2026-10-06: first version 3 beats / 8 beats -> 1/4 made the slow total a whole number - easier than the original)
    S(M, 'wp26-p16', 'In the time a slow drummer plays 5 beats, a fast drummer plays 8 beats. Each slow beat takes $\\frac23$ of a second. '
                     'How long is one fast beat?',
      ['$\\frac{16}{15}$ seconds', '$\\frac{8}{5}$ seconds', '$\\frac{5}{12}$ second', '$\\frac{5}{8}$ second'], 3, [
        'Five slow beats: $5\\times\\frac23=\\frac{10}3$ seconds.',
        'Eight fast beats take the same time, therefore one fast beat takes $\\frac{10}3\\div8=\\frac{10}{24}=\\frac5{12}$ second.',
        'Method 2 · Compare by factors: in the same time the fast drummer plays $\\frac85$ as many beats. A beat goes the opposite way → '
        'flip to $\\frac58$: $\\frac23\\cdot\\frac58=\\frac{10}{24}=\\frac5{12}$ second.'])
    # p17: M scanners L pages/h, D scanners 3 h -> 3DL/M  ==>  K printers P pages/h, N printers 5 h -> 5NP/K
    S(M, 'wp26-p17', '$K$ identical printers print $P$ pages in one hour. How many pages do $N$ such printers print in 5 hours?',
      ['$\\frac{5NP}{K}$', '$\\frac{5KP}{N}$', '$\\frac{NP}{5K}$', '$\\frac{5NK}{P}$'], 1, [
        'One printer: $\\frac PK$ pages per hour. $N$ printers: $\\frac{NP}K$ pages per hour.',
        'In 5 hours: $\\frac{5NP}K$. (Check: $K=3$, $P=12$, $N=6$: one printer does 4 per hour, six do 24 per hour, 120 in 5 hours, and $\\frac{5\\cdot6\\cdot12}3=120$ ✓.)',
        'Method 2 · Compare by factors: printers $\\times\\frac NK$ and hours $\\times5$. Both push the pages the same way: $P\\cdot\\frac NK\\cdot5=\\frac{5NP}{K}$.'])
    # p18: 4 painters 6 h, with a 5th 4 h -> 12  ==>  3 cleaners 8 h, with a 4th 6 h -> 24
    S(M, 'wp26-p18', 'Three identical cleaners clean an office in 8 hours. With a fourth cleaner, who works at a different rate, '
                     'the office takes 6 hours. How many hours would the fourth cleaner need alone?',
      ['14', '2', '24', '48'], 3, [
        'Three cleaners: $\\frac18$ of the office per hour. Four cleaners: $\\frac16$.',
        'The fourth cleaner adds $\\frac16-\\frac18=\\frac4{24}-\\frac3{24}=\\frac1{24}$ per hour, therefore alone she needs 24 hours.'])
    # p19: tap 10 h, 3 drains 4 h, 4 taps x 15 h -> 72  ==>  pipe 8 h, 2 drains 5 h, 3 pipes x 16 h -> 60
    S(M, 'wp26-p19', 'A pipe fills a cistern in 8 hours. Two identical drains empty a full cistern in 5 hours. How many hours does one drain '
                     'need to remove the amount of water that three such pipes supply in 16 hours?',
      ['30', '60', '120', '48'], 2, [
        'Three pipes for 16 hours: $3\\times16=48$ pipe-hours. One cistern needs 8 pipe-hours, so they supply $48\\div8=6$ cisterns.',
        'Two drains empty a cistern in 5 hours, so one drain needs $2\\times5=10$ hours per cistern. Six cisterns: $6\\times10=60$ hours.'])
    # p20: fast 3x slow, together 12 h -> slow 48  ==>  new robot 4x old, together 10 h -> old 50
    S(M, 'wp26-p20', 'A new robot works four times as fast as an old robot. Together they finish an order in 10 hours. '
                     'How many hours would the old robot need alone?',
      ['40', '12.5', '25', '50'], 4, [
        'Rates: old = 1 part, new = 4 parts, together = 5 parts.',
        'The old robot alone has $\\frac15$ of the team rate, so it needs 5 times as long: $5\\times10=50$ hours.'])


def rn_practice(M):
    """Approved clean-up (35 -> 25): no copies in this topic. Keep 3 extra-bank warm-ups (p24 add the rates, p25 rate in
    percent, p23 workers leave) and 3 September items of types the Hebrew practice does not have (q-07 a worker with a
    different rate leaves, q-08 together then one stops - find its rate, q-09 two percent changes multiply)."""
    P = 'wp26-practice'
    N = lambda k: 'q-r26-t26-' + k
    out = [
        'wp26-p21',   # pump + leak: guided Q3 and p19 (working against)
        'wp26-p22',   # equal worker joins: guided Q8 (joins midway) and p23
        'wp26-p26',   # one drain, then a second joins: guided Q8 (same type)
        'wp26-p27',   # V method, blank in the team: p05 and guided Q14 (stage / seating)
        N('05'),      # rate -20%: p25 (rate in percent) and guided Q2
        N('06'),      # find B from together: p18 (find the extra worker)
        N('10'),      # ab/(a+b) with letters: guided Q4 / Q5 shortcut
        N('11'),      # average rate, time weights: p09 and guided Q11
        N('12'),      # workers join, whole job: p23 and guided Q8 ("left or whole" trap)
        N('13'),      # average-rate trap, half smooth / half rough: p09
    ]
    for qid in out:
        assert M.section_of(qid) == P, qid
        M.unplace(qid)
    M.practice_order(P, [
        # easy
        'wp26-p06', 'wp26-p02', 'wp26-p24', 'wp26-p11', 'wp26-p03', 'wp26-p01', 'wp26-p04', 'wp26-p12', 'wp26-p17', 'wp26-p13', 'wp26-p25',
        # medium
        'wp26-p05', 'wp26-p08', 'wp26-p09', 'wp26-p16', 'wp26-p20', 'wp26-p18', 'wp26-p15', 'wp26-p14', 'wp26-p23',
        # exam-hard
        'wp26-p07', 'wp26-p19', N('07'), N('09'), N('08'),
    ])


def rn_titles(M):
    """Solution videos: title and the pre-loaded-question note follow the new stems."""
    for f in M.D['flow']:
        if f['topic'] != TOPIC or f['type'] != 'video': continue
        v = M.video(f['ref']); qid = v.get('questionId')
        if not qid or qid not in M.D['questions'] or f['ref'] in RN_RECORDED: continue
        stem = M.q(qid)['stem']
        v['title'] = v['navLabel'] = stem
        for b in v['beats']:
            pre = b['items'][:b['pre']]
            if len(pre) == 1 and pre[0].get('k') == 'q':
                if not b['loads']:   # (finish() would otherwise overwrite the canvas note of a rebuilt slide)
                    sb = v.get('hybrid', {}).get('sidebar', [])
                    lab = sb[b['active']] if 0 <= b['active'] < len(sb) else b['title']
                    b['loads'] = 'Sidebar with "%s" highlighted; the items listed are already on the canvas.' % lab
                b['canvas'] ='Pre-loaded — question %s with its four answer choices — "%s"' % (pre[0]['qid'], M.q(pre[0]['qid'])['stem'])
        M.touched_videos.add(f['ref'])


def rv_fixes(M):
    """2026-10-06 review: leftovers of the old stories outside the stems/videos."""
    def tab(headers, rows): return {'type': 'table', 'headers': headers, 'rows': rows}
    M.q('wp26-g093')['solutionVisual'] = tab(['Situation', 'Time', 'Output'], [
        ['Original', 'y', 'x'], ['Triple rate', 'y', '3x'], ['Triple rate, five times longer', '5y', '15x']])
    M.q('wp26-g096')['solutionVisual'] = tab(['Printer', 'Batches in 30 hours'], [['A', '5'], ['B', '3'], ['Together', '8']])
    M.q('wp26-g098')['solutionVisual'] = tab(['Gardeners', 'Trees', 'Hours'], [['3', '40', '5'], ['4', '96', '?']])
    M.q('wp26-g105')['solutionVisual'] = tab(['Job', 'Original team', 'Hours', 'Worker-hours'], [
        ['Stage', '12', '2', '24'], ['Seating', '14', '4', '56'], ['Together', '', '', '80']])
    # g095 is about a pond now
    b = M.video('solve-wp26-g095')['beats'][2]
    assert b['title'] == 'Method 2 · Pick a tank size', b['title']
    b['title'] = 'Method 2 · Pick a pond size'
    M.touched_videos.add('solve-wp26-g095')


def renumber_pass(M):
    rn_lessons(M)
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_titles(M)
    rv_fixes(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-07 methods spread (runs last). The 2026-10-06 methods are added where they really solve a question and
# the solution does not show them yet: a "Method N" line at the end of the written solution, and one extra slide in
# the clearest solution video. Nothing in topic 26 is recorded (checked 2026-10-07).
# ======================================================================================================
def _sp_line(M, qid, line):
    ex = list(M.q(qid).get('explanation') or [])
    if line in ex: return
    M.set_q(qid, expl=ex + [line])


def _sp_slide(M, qid, after_n, title, script):
    vid = 'solve-' + qid
    assert M.video(vid)['questionId'] == qid, vid
    act = M.slide(vid, 2)['active']
    M.insert_slides(vid, after_n, [dict(mode='question', active=act, title=title, pre=[Q(qid)], script=script)])


def spread_methods(M):
    # Q10 bakery queue: one rate against another -> only the difference counts
    _sp_line(M, 'wp26-g102', r'Method 3 · Catching up (difference in rates): the baker completes $15$ orders in $40$ minutes $=22.5$ an hour, and $18$ come in. The queue shrinks by $22.5-18=4.5$ orders an hour. In $4$ hours: $4\cdot4.5=18$ fewer, and $60-18=42$.')
    # Q11 average rate: the hours are the weights (topic 25)
    _sp_line(M, 'q-r26-t26-04', r'Method 3 · Percent shares as weights (the weights are the hours): $3$ of the $5$ hours are at $20$ and $2$ of the $5$ ($40\%$) at $30$. Average $=20+0.4\cdot10=24$.')
    _sp_slide(M, 'q-r26-t26-04', 3, 'Method 3 · Shares as weights', [
        'Weighted by time — so the hours are the weights. Two of the five hours are at thirty.',
        A("'Share at 30: 2 of 5 h = 40%' appears", T(r'Share at $30$: $\ 2$ of $5$ hours $=40\%$', size=40, gap=50)),
        A("'20 + 0.4 · 10 = 24' appears", T(r'$20+0.4\cdot(30-20)=24$', size=44, gap=50)),
        'Start at the slow rate, twenty. Add forty percent of the gap of ten: four. Twenty-four.',
        D('Circle choice 2'),
        'Choice two — exact, with no division by the total time.'])
    # Q15 hay: compare by factors (the V made general)
    _sp_line(M, 'wp26-g105b', r'Method 2 · Compare by factors: the sheep are $\times\frac{150}{200}=\times\frac34$. Fewer sheep, more days (opposite way) → flip to $\frac43$: $9\cdot\frac43=12$ days.')
    # practice
    _pm_add(M, 'wp26-p09', [r'Method 2 · Percent shares as weights (the weights are the days): $2$ of the $10$ days ($20\%$) are at $20$ bowls a day, the rest at $5$. Average $=5+0.2\cdot15=8$ bowls a day.'])
    _pm_add(M, 'wp26-p23', [r'Method 2 · Compare by factors: after $4$ days, six workers would need $14-4=10$ more days. The team is $\times\frac46=\frac23$; fewer workers, more days (opposite way) → flip to $\frac32$: $10\cdot\frac32=15$ days.'])
    _pm_add(M, 'wp26-p07', [r'Method 2 · Compare by factors: the team grows from $5$ to $5+3=8$ ordinary printers, $\times\frac85$. More printers, less time (opposite way) → flip to $\frac58$: $8\cdot\frac58=5$ hours.'])


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


# =====================================================================================
# 2026-10-07 study-plan order: students meet the topics in the STUDY PLAN order (src/lib/planData.ts ORDER), not
# by topic number. A named method used before the topic that teaches it (in the plan) becomes a self-contained
# "Shortcut · <name>: <why>" line; a "Shortcut" whose method the plan already taught becomes a normal
# "Method N · <name>" line. Unrecorded videos only. Runs LAST.
# =====================================================================================

def _po_line(M, qid, start, new):
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(start)]
    assert len(k) == 1, (qid, start, k)
    ex[k[0]] = new
    M.set_q(qid, expl=ex)


def _po_relabel(M, qid, old, name):
    import re as _re
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(old)]
    assert len(k) == 1, (qid, old, k)
    used = [int(n) for l in ex for n in _re.findall(r'^Method (\d+) ·', l)]
    rest = ex[k[0]][len(old):].lstrip()
    if _re.match(r'[A-Z][a-z]', rest): rest = rest[0].lower() + rest[1:]
    ex[k[0]] = 'Method %d · %s: %s' % (max(used) + 1 if used else 2, name, rest)
    M.set_q(qid, expl=ex)


def _po_say(M, vid, n, old, new):
    """Replace the spoken line `old` (exact) on slide n with `new` (a string, or a list of strings)."""
    b = M.slide(vid, n)
    k = [i for i, l in enumerate(b['lines']) if l.get('say') == old]
    assert len(k) == 1, (vid, n, old)
    M.edit_lines(vid, n, lambda ls: ls[:k[0]] + [{'say': s} for s in ([new] if isinstance(new, str) else new)] + ls[k[0] + 1:])


def plan_order_fix(M):
    # wp26-g105b comes before the lesson "Compare by Factors" (r26-t26-factors) in this topic.
    _po_line(M, 'wp26-g105b', 'Method 2 · Compare by factors:', "Shortcut · Compare by factors: only the number of sheep changes, and the days go the opposite way (fewer sheep, more days), so multiply the days by the flipped factor. The sheep are $\\times\\frac{150}{200}=\\times\\frac34$ → the days are $\\times\\frac43$: $9\\cdot\\frac43=12$ days.")


_apply_before_plan_order_fix = apply


def apply(M):
    _apply_before_plan_order_fix(M)
    plan_order_fix(M)   # 2026-10-07 study-plan order: runs last


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
    _mn_load().method_names(M, 26)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 coverage fixes (teacher approved "go ahead"). A full check of the teacher's Hebrew course against this
# topic found points that were taught only WEAKLY or were MISSING; each one goes back as one or two short spoken lines
# in an unrecorded video (or, for a video recorded before CF.CUTOFF, into the written solution / card). Runs LAST.
# Helpers: _hebrew_back.py loaded as its own copy with this pass's CUTOFF. See tNN_CHANGES.md "2026-10-08 coverage fixes".
# =====================================================================================================================
import importlib.util as _ilu_cf, os as _os_cf
_s_cf = _ilu_cf.spec_from_file_location('_hebrew_back_cf', _os_cf.path.join(_os_cf.path.dirname(_os_cf.path.abspath(__file__)), '_hebrew_back.py'))
CF = _ilu_cf.module_from_spec(_s_cf); _s_cf.loader.exec_module(CF)
CF.CUTOFF = '2026-10-08T08-43-14'   # UTC, when this pass finished: a take recorded before it keeps its video unchanged


def _cf_replace(M, vid, title, sub, new):
    """replace the one line containing sub (spoken / drawn / item) on slide `title` by new (line or list). False if recorded."""
    if CF.recorded(vid): return False
    CF.set_slide(M, vid, title, CF.replace_line(CF.lines_of(M, vid, title), sub, new))
    return True


def coverage_fixes(M):
    # #20 (Hebrew 6138-6158): read a combined rate a/b as "a jobs in b hours", then scale to one job
    if not _cf_replace(M, 'solve-wp26-g096', 'Method 2 · Algebra', 'Four fifteenths per hour. One batch', [
            "Four fifteenths per hour. Read it as: four batches in fifteen hours.",
            "So one batch takes a quarter of that: fifteen quarters of an hour — two hundred twenty-five minutes."]):
        CF.add_expl(M, 'wp26-g096', "Read $\\frac{4}{15}$ per hour as 4 batches in 15 hours: one batch takes $\\frac{15}{4}$ hours.")
    # #49 (Hebrew 6586-6612): hours come out as an awkward decimal - switch to minutes
    if not _cf_replace(M, 'solve-wp26-g103', 'Method 2 · Estimation', 'A hundred ten takes it two point two hours', [
            "A alone does fifty an hour. A hundred ten takes it two point two hours.",
            "Hours come out as an awkward decimal? Switch to minutes: two point two hours is a hundred thirty-two minutes."]):
        CF.add_expl(M, 'wp26-g103', "Hours come out as an awkward decimal ($2.2$ h)? Switch to minutes: $132$ minutes.")
    # #67 (Hebrew 6977-6978): "hidden team" questions appear on recent exams - checked real_exam/quant_real.md: a supply
    # used up by eaters/consumers (2023 spring bees and nectar, 2025 spring a pack of pencils, 2025 winter cat food)
    if not CF.add_lines(M, 'solve-wp26-g105b', 'Advanced Work & Rate', "Hard to see who's the team", [
            "Questions like this, where the team is hidden, have shown up on recent exams. Worth knowing."]):
        CF.add_expl(M, 'wp26-g105b', "Questions with a hidden team (eaters using up a supply) have shown up on recent exams.")
    # #46 (Hebrew 6493-6501, "75 or a multiple of 100? reduce by 25"): belongs to the topic-2 arithmetic card, which is
    # outside this topic's file; topic 26's numbers no longer use 75 - not added here.


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST
