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
