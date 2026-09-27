"""Topic 23 - Percentages. Course review 2026-09 fixes.
See t23_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q


def _plain(s):
    s = re.sub(r'\\frac\{?(\w)\}?\{?(\w+)\}?', r' \1/\2', s)
    return s.replace('\\%', '%').replace('\\left', '').replace('\\right', '').replace('\\', '')

TOPIC = 23
L1 = 'wp-052'          # Calculating Percentages
L2 = 'wp-053'          # Percent of a Percent
TRAPS = 'r26-t23-traps'
CARD = 'mem-percent'
CARD2 = 'mem-r26-t23-traps'
ADV = 'wp23-advanced'
PRAC = 'wp23-practice'
# advanced-section solution videos: old numbers 2..10 + new guided questions 11..15 (renumbered automatically)
QSIDEBAR = ['Question %d' % n for n in range(2, 16)]


def VIS(v, **k): return dict(k='vis', v=v, **k)


def _solution(M, qid, intro, slides, after=None):
    """Guided-question solution video in the style of solve-wp23-g057..g065."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=QSIDEBAR.index('Question %d' % n), title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Advanced Percentages', QSIDEBAR, beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = 'Advanced Percentages'
    v['hybrid']['num'] = 21
    v['title'] = v['navLabel'] = _plain(M.q(qid)['stem'])
    return n


def _say_replace(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            for key in ('say', 'draw'):
                if key in l and old in l[key]:
                    l[key] = l[key].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _set_active(M, vid, mapping):
    for n, a in mapping.items():
        M.slide(vid, n)['active'] = a
    M.touched_videos.add(vid)


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Lesson 1 "Calculating Percentages" (wp-052)
    # =====================================================================================
    row1 = M.slide(L1, 4)['items'][0]
    row2 = M.slide(L1, 4)['items'][1]
    row3 = M.slide(L1, 4)['items'][2]
    # slide 4: halves and tenths only
    M.set_slide(L1, 4, pre=[], script=[
        "Some conversions you must know by heart for this exam.",
        A('A row appears: 1/2 = 50%, 1/4 = 25%, 1/8 = 12.5%', row1),
        "A half: fifty. A quarter: twenty-five. Almost everyone knows those.",
        "What people forget: one eighth is twelve and a half percent.",
        D('Draw "÷2" arrows from 50% to 25% to 12.5%'),
        "Here's how to remember it. A quarter is half of a half — and twenty-five is half of fifty. An eighth is half of a quarter — half of twenty-five: twelve and a half.",
        "As decimals it's exactly the same: zero point five, zero point two five, zero point one two five.",
        A('A row appears: 1/10 = 10%, 1/5 = 20%, 1/20 = 5%', row2),
        "A tenth: ten percent. A fifth is two tenths: twenty. A twentieth is half a tenth: five.",
        "On the exam you'll see twelve point five AND twelve and a half. Get used to both.",
    ])
    # new slide 5: thirds and families (the old "sixteen and a bit" line is gone)
    M.insert_slides(L1, 4, [dict(mode='concept', active=3, title='Thirds and families', script=[
        A('A row appears: 1/3 = 33⅓%, 1/6 = 16⅔%', row3),
        "A third: thirty-three and a third percent.",
        D('Draw a "÷2" arrow from 1/3 to 1/6'),
        "A sixth is half a third. Half of thirty-three is sixteen and a half. Half of one third is one sixth.",
        D('Write "16½ + ⅙ = 16⅔"'),
        "Sixteen and a half, plus one sixth: sixteen and two thirds percent.",
        "Now build the families. Take a basic fraction a few times.",
        A('A row appears: 3/8 = 37.5%, 5/8 = 62.5%',
          dict(k='row', items=['$\\frac38=37.5\\%$', '$\\frac58=62.5\\%$'], sp=420, below=70)),
        "Three eighths: three times twelve and a half — thirty-seven and a half. Five eighths: sixty-two and a half.",
        A('A row appears: 3/5 = 60%, 7/20 = 35%',
          dict(k='row', items=['$\\frac35=60\\%$', '$\\frac7{20}=35\\%$'], sp=420)),
        "Three fifths: three times twenty — sixty. Seven twentieths: seven fives — thirty-five.",
        "Don't memorize every family. Know the basic fraction, then multiply.",
    ])])
    # slide 6 (was 5): the letter-inside-the-percent example is exam level
    _say_replace(M, L1, 6, "And the exam version — a letter inside the percent.",
                 "And the exam version — a letter inside the percent. This one is harder. If it feels fast, come back to it after the guided questions.")
    # slide 7 (was 6): one name for the method - "triangle value" as in the ratio topic
    _say_replace(M, L1, 7, "Method two: equal ratios — the triple value. Perfect for quick calculations.",
                 "Method two: equal ratios — the triangle value from the ratio lesson. Perfect for quick calculations.")
    _say_replace(M, L1, 7, "Percents on one side, amounts on the other.",
                 "A table with two columns: percents on the left, amounts on the right.")
    # slide 9 (was 8): the change rule on the board
    it = M.slide(L1, 9)['items']
    sm = lambda x: dict(x, size=44, gap=40)
    M.set_slide(L1, 9, pre=[], script=[
        "A few extra tools.",
        A("'16% of 25 = 25% of 16' appears", sm(it[0])),
        D('Write "= 4"'),
        "Swap them: a percent of b equals b percent of a. Sixteen percent of twenty-five equals twenty-five percent of sixteen — a quarter of sixteen. Four.",
        A("'30% of the whole is 54' appears", sm(it[1])),
        D('Write "10% → 18,  100% → 180"'),
        "Whole missing? Thirty percent is fifty-four, so ten percent is eighteen — and the whole is a hundred eighty.",
        A("'From 80 to 100' appears", sm(it[2])),
        "And a change is always measured against where it STARTED — the original.",
        A("'change in % = change ÷ original × 100' appears",
          T('Change in $\\% = \\frac{\\text{change}}{\\text{original}}\\times100$', size=44)),
        D('Write "20/80 × 100 = 25%"'),
        "Eighty up to a hundred: the change is twenty. Twenty out of the original eighty — a quarter. Twenty-five percent.",
        "Learn this rule. Change, divided by the original, times a hundred.",
    ])
    # slide 10 (was 9): recap with the change rule
    M.set_slide(L1, 10, pre=[], script=[
        "Let's lock it in.",
        A("'Percent = over 100 · \"of\" = times' appears", T('Percent = over $100$ · "of" = times', size=42)),
        A("'Equation · Triangle value · 10% chunks' appears", T('Equation · Triangle value · $10\\%$ chunks', size=42)),
        A("'Change: divide by the ORIGINAL' appears", T('Change: divide by the ORIGINAL', size=42)),
        A("'Know the fraction table by heart' appears", T('Know the fraction table by heart', size=42)),
        D('Underline "by heart"'),
        "Three methods — pick the one that fits the numbers.",
        "Next lesson: a percent of a percent — when the whole isn't given at all.",
    ])
    M.set_sidebar(L1, ['What a percent is', 'Percent ↔ fraction', 'Fractions to know', 'Thirds and families',
                       'The percent equation', 'Equal ratios', 'The 10% method', 'More tools', 'Recap'])
    _set_active(M, L1, {6: 4, 7: 5, 8: 6, 9: 7, 10: 8})

    # =====================================================================================
    # 2. Lesson 2 "Percent of a Percent" (wp-053): multipliers, up-and-down rule
    # =====================================================================================
    M.insert_slides(L2, 3, [
        dict(mode='concept', active=2, title='Multipliers', script=[
            "Here's the fastest tool for changes: the multiplier.",
            A("'+20% → ×1.2 and −15% → ×0.85' appears",
              T('$+20\\%\\ \\to\\ \\times1.2 \\qquad -15\\%\\ \\to\\ \\times0.85$', size=46, gap=40)),
            "Up twenty percent: you keep all of it — a hundred percent — and add twenty. A hundred twenty percent: times one point two.",
            "Down fifteen percent: you keep eighty-five percent. Times zero point eight five.",
            A("'Up x%: ×(1 + x/100) · Down x%: ×(1 − x/100)' appears",
              T('Up $x\\%$: $\\times\\left(1+\\frac{x}{100}\\right)$ $\\qquad$ Down $x\\%$: $\\times\\left(1-\\frac{x}{100}\\right)$', size=40, gap=40)),
            "Two changes? Multiply the two factors.",
            A("'+10%, then +10%: 1.1 × 1.1 = 1.21' appears", T('$+10\\%$, then $+10\\%$: $\\ 1.1\\times1.1=1.21$', size=44, gap=40)),
            D('Write "→ +21%"'),
            "Up ten percent twice: one point one times one point one — one point two one. Up twenty-one percent, not twenty.",
            A("'−25%, then −20%: 0.75 × 0.8 = 0.6' appears", T('$-25\\%$, then $-20\\%$: $\\ 0.75\\times0.8=0.6$', size=44)),
            D('Write "→ keep 60%, lost 40%"'),
            "The two losses from before: zero point seven five times zero point eight — zero point six. We keep sixty percent, so we lost forty. Same answer, one line.",
        ]),
        dict(mode='concept', active=3, title='Up and down', script=[
            A("'+20%, then −20%: 1.2 × 0.8 = 0.96' appears", T('$+20\\%$, then $-20\\%$: $\\ 1.2\\times0.8=0.96$', size=44, gap=40)),
            "Up twenty, then down twenty. Back to the start? No.",
            D('Write "→ 4% lower"'),
            "One point two times zero point eight: zero point nine six. Four percent lower.",
            "Down first, then up? Zero point eight times one point two. The same. The order doesn't matter.",
            A("'Up p% and down p%: a loss of p²/100 %' appears", T('Up $p\\%$ and down $p\\%$: a loss of $\\frac{p^2}{100}\\%$', size=44, gap=40)),
            "The rule: up p percent and down p percent always loses p squared over a hundred percent. Twenty squared is four hundred. Over a hundred: four.",
            "Up thirty, down thirty? Nine hundred over a hundred: a nine percent loss.",
            A("'Any two changes a% and b%: a + b + ab/100' appears", T('Any two changes $a\\%$ and $b\\%$: $\\ a+b+\\frac{ab}{100}$', size=42)),
            "For strong students — any two changes: add them, then add a times b over a hundred. A fall is a minus number.",
            D('Write "+25, −20:  25 − 20 − 5 = 0"'),
            "Up twenty-five, down twenty. Twenty-five minus twenty is five. Twenty-five times minus twenty, over a hundred, is minus five. Five minus five: zero. No change — exactly what we got at the start.",
        ]),
    ])
    # old slide 6 "Working backwards" is now slide 8
    M.edit_lines(L2, 8, lambda ls: ls + [
        {'say': "With a multiplier: ninety-six is the start times zero point eight. So the start is ninety-six divided by zero point eight — a hundred twenty."}])
    # recap (now slide 9)
    M.set_slide(L2, 9, pre=[], script=[
        "Let's lock it in.",
        A("'Whole not given? Plug in 100' appears", T('Whole not given? Plug in $100$', size=44)),
        A("'The whole comes after \"of\" / \"than\" — in the question' appears", T('The whole comes after "of" / "than" — in the question', size=40)),
        A("'Each new percent sits on the new amount' appears", T('Each new percent sits on the new amount', size=44)),
        A("'Several changes? Multiply the factors' appears", T('Several changes? Multiply the factors', size=44)),
        D('Circle "in the question"'),
        "Next: a survey question — and a second way to see it, the percent tree.",
    ])
    M.set_sidebar(L2, ['Plug in 100', 'Two losses', 'Multipliers', 'Up and down', 'Who is the 100?',
                       'When 100 fails', 'Working backwards', 'Recap'])
    _set_active(M, L2, {6: 4, 7: 5, 8: 6, 9: 7})

    # =====================================================================================
    # 3. Existing solution videos
    # =====================================================================================
    _say_replace(M, 'solve-wp23-g054', 3, "practised", "practiced")
    # Q7: the swap rule in plain words
    _say_replace(M, 'solve-wp23-g062', 3,
                 "A percent of a number equals that number percent of the percent — it's one multiplication.",
                 "a percent of b equals b percent of a — you can swap them. It's one multiplication.")
    # Q8 method 2: show choice 1 too
    M.set_slide('solve-wp23-g063', 3, script=[
        "Or think in ratios. Twenty percent of a hundred is twenty. Double the whole to two hundred — you need half the percent, ten, to still get twenty.",
        D('Write "percent × k  ⟺  whole ÷ k"'),
        "Percent up, whole down by the same factor — same result.",
        D('Next to choice 1 write "percent × 2/3,  whole × 3/2"'),
        "Choice one: ten percent is two thirds of fifteen. Six x is three halves of four x. Two thirds times three halves is one. Balanced.",
        "Choice two: the percent is four times bigger, the whole four times smaller. Balanced. Choice three: a third of the percent, three times the whole. Balanced.",
        D('Circle choice 4'),
        "Choice four: the percent doubled — and the whole stayed four x. Nothing balances it. Choice four.",
    ])
    # Q10: American spelling; it is no longer the last question
    for n in (1, 2, 3):
        _say_replace(M, 'solve-wp23-g065', n, 'litres', 'liters')
    _say_replace(M, 'solve-wp23-g065', 1, "Last question of the set.", "A tank that loses water.")
    _say_replace(M, 'solve-wp23-g065', 2, "Now twenty percent of what's in the tank NOW — keep eighty percent of eighty: sixty-four percent.",
                 "Now twenty percent of what's in the tank NOW — keep eighty percent of eighty: sixty-four percent. With multipliers: zero point eight times zero point eight.")
    for vid in ['solve-wp23-g057', 'solve-wp23-g058', 'solve-wp23-g059', 'solve-wp23-g060', 'solve-wp23-g061',
                'solve-wp23-g062', 'solve-wp23-g063', 'solve-wp23-g064', 'solve-wp23-g065']:
        M.set_sidebar(vid, QSIDEBAR)

    # =====================================================================================
    # 4. Existing questions: TeX, numbers in every solution, stacked conditions, no ":" for division
    # =====================================================================================
    S('wp23-g054', expl=[
        'Plug in $100$ people. $55$ do not own a bicycle, so $100-55=45$ own one.',
        'The $40\\%$ is of the owners: $10\\%$ of $45$ is $4.5$, so $40\\%$ of $45$ is $4\\times4.5=18$ electric.',
        'Ordinary only: $45-18=27$ people out of $100$, so $27\\%$.',
        'Percent tree: $60\\%$ of $45\\%$ is $0.6\\times45\\%=27\\%$.'])
    S('wp23-g057', expl=[
        'Remaining: $100\\%-72.5\\%=27.5\\%$.',
        '$27.5\\%=\\frac{27.5}{100}=\\frac{55}{200}$ (top and bottom times $2$). Reduce by $5$: $\\frac{11}{40}$.'])
    S('wp23-g058', expl=[
        'A $75\\%$ reduction leaves $100\\%-75\\%=25\\%=\\frac14$ of the price.',
        '$760\\div4=190$.'])
    S('wp23-g059', expl=[
        'Each rise is $6$ credits.',
        'First rise: $\\frac{6}{60}=\\frac1{10}=10\\%$. Second rise: $\\frac{6}{66}=\\frac1{11}$.',
        'Same top, bigger bottom: $\\frac1{11}<\\frac1{10}$. The first percentage increase is larger.'])
    S('wp23-g060', expl=[
        'Plug in $100$ points. Giving away $25\\%$ leaves $75$.',
        'The bonus is $30\\%$ of $75$: $3\\times7.5=22.5$. Final score: $75+22.5=97.5$.',
        '$97.5$ out of $100$: $2.5\\%$ lower.',
        'With multipliers: $0.75\\times1.3=0.975$, which is $97.5\\%$ of the original.'])
    S('wp23-g061', stem='Rae earns $20\\%$ more than Sol. Tia earns $16\\frac23\\%$ less than Rae. What is Tia’s wage divided by Sol’s wage?',
      expl=['Plug in $100$ for Sol. Rae earns $20\\%$ more: $120$.',
            '$16\\frac23\\%=\\frac16$. Tia earns $\\frac16$ less than Rae: $120-\\frac{120}{6}=120-20=100$.',
            'Tia’s wage divided by Sol’s wage: $100\\div100=1$.'])
    S('wp23-g062', stem='$50\\%$ of $15\\%$ of $x$ equals $12$. What is $22.5\\%$ of $x$?', expl=[
        '$50\\%$ of $15\\%$ is half of $15\\%$: $7.5\\%$. So $7.5\\%$ of $x$ is $12$.',
        '$22.5\\%=3\\times7.5\\%$, so $22.5\\%$ of $x$ is $3\\times12=36$. There is no need to find $x$.'])
    S('wp23-g063', stem='For $x>0$, which expression is not equal to $15\\%$ of $4x$?',
      choices=['$10\\%$ of $6x$', '$60\\%$ of $x$', '$5\\%$ of $12x$', '$30\\%$ of $4x$'], expl=[
        '$15\\%$ of $4x=\\frac{15\\cdot4x}{100}=\\frac{60x}{100}$.',
        'Every choice is also over $100$, so compare the tops: $10\\cdot6x=60x$, $60\\cdot x=60x$, $5\\cdot12x=60x$, but $30\\cdot4x=120x$.',
        'Since $x>0$, $120x\\ne60x$. Only $30\\%$ of $4x$ is not equal.'])
    S('wp23-g064', expl=[
        'Monday: $80\\%$. Tuesday: the rest, $100\\%-80\\%=20\\%$.',
        'The difference is $80\\%-20\\%=60\\%$, and it equals $36$ planks.',
        '$60\\%\\to36$, so $20\\%\\to36\\div3=12$ planks.'])
    S('wp23-g065', stem='At the end of each hour, $20\\%$ of the water then in a tank is removed. After two hours, $128$ liters remain. How many liters were there at the start?',
      expl=['Each hour $20\\%$ is removed, so $80\\%$ stays: multiply by $0.8$.',
            'After two hours: $0.8\\times0.8=0.64$, so $64\\%$ of the start remains.',
            '$64\\%=128$ liters, so $1\\%=2$ liters and $100\\%=200$ liters.',
            'Check: $200\\to160\\to128$ ✓.'])

    S('wp23-p01', stem='What is $75\\%$ of $\\frac89$?', expl=[
        '$75\\%=\\frac34$.', '$\\frac34\\times\\frac89=\\frac{3\\cdot8}{4\\cdot9}=\\frac{24}{36}=\\frac23$.'])
    S('wp23-p02', expl=[
        'White: half of $80$ is $40$. Not white: $80-40=40$.',
        'Purple is $65\\%$ of them, so orange is $100\\%-65\\%=35\\%$ of $40$.',
        '$10\\%$ of $40$ is $4$, so $35\\%$ of $40$ is $3\\times4+2=14$.'])
    S('wp23-p03', stem='A subscription begins at $96$ credits. After each annual review, its price rises by $50\\%$. After which review is its price first not a whole number of credits?',
      expl=['A $50\\%$ rise multiplies the price by $1.5=\\frac32$: times $3$, divided by $2$.',
            'Each review uses up one factor $2$. $96=2^5\\cdot3$ has five factors $2$.',
            'So reviews 1 to 5 give whole numbers: $96\\to144\\to216\\to324\\to486\\to729$, and $729=3^6$ has no factor $2$ left.',
            'Review 6: $729\\times1.5=1093.5$. The first price that is not a whole number comes after review 6.'])
    S('wp23-p04', stem='$40\\%$ of $25\\%$ of $x$ equals $9$. What is $\\frac3{10}x$?', expl=[
        '$40\\%$ of $25\\%$: $\\frac25\\times\\frac14=\\frac1{10}$. So $\\frac1{10}x=9$.',
        '$\\frac3{10}x=3\\times9=27$.'])
    S('wp23-p05', expl=[
        'She hits on $40\\%$, so she misses on $100\\%-40\\%=60\\%$ of her attempts.',
        '$60\\%=18$ attempts, so $10\\%=3$ and $100\\%=30$ attempts.'])
    S('wp23-p06', expl=[
        'The more members the club has, the smaller the juniors’ share. So use the smallest share: $25\\%$.',
        '$15$ juniors $=25\\%=\\frac14$ of the club, so the club has $4\\times15=60$ members.',
        'Seniors: $60-15=45$.'])
    S('wp23-p07', expl=[
        'Plug in $100$. A $50\\%$ rise: $150$.',
        '$20\\%$ of $150$ is $30$. The recipient keeps $150-30=120$.',
        '$120$ out of the original $100$: $120\\%$. With multipliers: $1.5\\times0.8=1.2$.'])
    S('wp23-p08', stem='Given:\n$\\begin{cases} a+b=200 \\\\ a=b+60 \\end{cases}$\nWhat percentage of $a+b$ is $b$?', expl=[
        'Put $a=b+60$ into the sum: $(b+60)+b=200$, so $2b=140$ and $b=70$.',
        '$\\frac{70}{200}=\\frac{35}{100}=35\\%$.'])
    S('wp23-p09', stem='$15\\%$ of $3x$ is $18$. What percentage of $x$ is $18$?', expl=[
        '$15\\%$ of $3x=\\frac{15\\cdot3x}{100}=\\frac{45x}{100}$, which is $45\\%$ of $x$.',
        'So $18$ is $45\\%$ of $x$. There is no need to find $x$.'])
    S('wp23-p10', expl=[
        'Two $10\\%$ rises: multiply by $1.1\\times1.1=1.21$. In total the price rises by $21\\%$.',
        '$21\\%$ of the original price is $63$, so $1\\%=3$ and $100\\%=300$.',
        'Check: $300\\to330\\to363$, and $363-300=63$ ✓.'])
    S('wp23-p11', expl=[
        'Owners to non-owners is $3$ to $1$, so owners are $\\frac34=75\\%$ of the students.',
        'Touch-screen owners: $40\\%$ of $75\\%$ is $0.4\\times75\\%=30\\%$ of all students.',
        'The rest: $100\\%-30\\%=70\\%$.'])
    S('wp23-p12', stem='$75\\%$ of a training group hold a certificate. Eighteen people hold only a first-aid certificate, and every other certificate holder holds only a coaching certificate. The number with coaching certificates equals the number with no certificate. How many people are in the group?',
      expl=['No certificate: $100\\%-75\\%=25\\%$.',
            'Coaching equals no certificate: $25\\%$. First aid: $75\\%-25\\%=50\\%$.',
            '$50\\%=18$ people, so $100\\%=36$.'])
    S('wp23-p13', expl=[
        'Plug in $100$ for the original price. New price: $140$. Target: $112$.',
        'The drop is $140-112=28$. Measure it against the current price, $140$: $\\frac{28}{140}=\\frac15=20\\%$.'])
    S('wp23-p14', stem='Of the same savings balance, $p\\%$ is $90$ credits and $q\\%$ is $150$ credits. Which of the following is necessarily true?',
      expl=['Percents of the same whole are in the same ratio as their amounts: $\\frac pq=\\frac{90}{150}=\\frac35$.',
            'Cross-multiply: $5p=3q$.'])
    S('wp23-p15', expl=[
        '$14+6=20$ sticks remain. That is half, so $20$ were used and there were $40$ at the start: $20$ of each color.',
        'Yellow used: $20-6=14$. Out of the $20$ used: $\\frac{14}{20}=\\frac{70}{100}=70\\%$.'])
    S('wp23-p16', expl=[
        'Buyers are $\\frac bN$ of all visitors.',
        'The same fraction of the $b$ buyers chose English: $b\\times\\frac bN=\\frac{b^2}{N}$.',
        'Check with numbers: $N=10$ and $b=4$. $\\frac4{10}$ of $4$ is $1.6$, and $\\frac{b^2}{N}=\\frac{16}{10}=1.6$ ✓.'])
    S('wp23-p17', stem='A coat is reduced from $240$ credits to $174$ credits. The discount is $a\\%$. Which interval contains $a$?',
      expl=['The discount is $240-174=66$ credits.',
            'Estimate: $25\\%$ of $240$ is $60$ and $30\\%$ of $240$ is $72$. $66$ is between them, so $25<a<30$.',
            'Exact: $\\frac{66}{240}\\times100=27.5$.'])
    S('wp23-p18', expl=[
        'Plug in numbers: $100$ books and $p=50$. A gets $50$, $50$ remain, and B gets $25$. The ratio is $50:25=2:1$.',
        'Check the choices with $p=50$: only the ratio $100:(100-p)=100:50=2:1$ fits.',
        'In general: A gets $\\frac p{100}T$ and B gets $\\frac p{100}\\cdot\\frac{100-p}{100}T$. Their ratio is $1:\\frac{100-p}{100}=100:(100-p)$.'])
    S('wp23-p19', expl=[
        'A ratio gives only the relative size, not an amount of credits. Paying $\\frac45$ of the price could be $80$ out of $100$ or $160$ out of $200$.',
        'Each other choice gives at least one amount in credits, so the price can be found. For example, original price $=$ amount saved $+$ price paid.'])
    S('wp23-p20', expl=[
        'The original price is $x+36$.',
        'Change divided by the original, times $100$: $\\frac{36}{x+36}\\times100=\\frac{3600}{x+36}$.',
        'Check with a number: if $x=64$, the original price is $100$ and the discount is $36\\%$. $\\frac{3600}{64+36}=36$ ✓.'])
    # p21 repeated the lesson example exactly (16% of 25) - new numbers
    S('wp23-p21', stem='What is $28\\%$ of $75$?', choices=['$18$', '$24$', '$28$', '$21$'], correct=4, expl=[
        'Swap: $28\\%$ of $75$ equals $75\\%$ of $28$.',
        '$75\\%=\\frac34$, and $\\frac34\\times28=21$.'])
    S('wp23-p22', expl=[
        'Plug in $100$: up $20\\%$ to $120$. Then $20\\%$ of $120$ is $24$, so the price falls to $120-24=96$.',
        '$96$ out of $100$: a $4\\%$ decrease.',
        'Rule: up $p\\%$ and down $p\\%$ loses $\\frac{p^2}{100}\\%=\\frac{400}{100}\\%=4\\%$.'])
    S('wp23-p23', stem='A container holds $300$ g of salt water that is $20\\%$ salt. How many grams of pure water must be added to make it $15\\%$ salt?',
      expl=['Adding water does not change the salt. Salt: $20\\%$ of $300$ is $60$ g.',
            'After: $60$ g is $15\\%$ of the new total. $15\\%=60$, so $5\\%=20$ and $100\\%=400$ g.',
            'Water to add: $400-300=100$ g.'])
    S('wp23-p24', expl=[
        '$30\\%$ off: $160\\times0.7=112$.',
        'Two discounts: $160\\times0.8\\times0.85=128\\times0.85=108.8$.',
        'Difference: $112-108.8=3.2$ credits.'])
    S('wp23-p25', stem='A town’s population grows from $12{,}000$ to $13{,}500$. What is the percentage increase?', expl=[
        'Increase: $13{,}500-12{,}000=1{,}500$.',
        'Divide by the original: $\\frac{1500}{12000}=\\frac18=12.5\\%$.'])
    S('wp23-p26', expl=[
        'Plug in $100$ for the trainee, so the worker earns $125$.',
        'The trainee earns $25$ less, measured against the worker: $\\frac{25}{125}=\\frac15=20\\%$.'])
    S('wp23-p27', expl=[
        'The paid price is $100\\%-15\\%=85\\%$ of the original.',
        '$85\\%=306$. $85\\%$ is $17$ times $5\\%$, so $5\\%=306\\div17=18$ and $100\\%=20\\times18=360$.',
        'Or test the round choice: $360\\times0.85=306$ ✓.'])

    S('wp23-p18', stem='A library lends $p\\%$ of its books to Branch A, then lends $p\\%$ of the remaining books to Branch B, where $0<p<100$. What is the ratio of the number sent to A to the number sent to B?')
    S('wp23-p19', stem='A tablet is sold at a discount. Which information alone is not enough to find its original price?')
    # solution-video titles follow the rewritten stems (liters, no capitals)
    for g in ('wp23-g061', 'wp23-g062', 'wp23-g063', 'wp23-g065'):
        v = M.video('solve-' + g); v['title'] = v['navLabel'] = _plain(M.q(g)['stem'])

    # =====================================================================================
    # 5. New guided question 1: multipliers (after Question 5)
    # =====================================================================================
    g1 = 'q-r26-t23-01'
    M.new_q(g1, TOPIC, 'A price rises by $25\\%$. Later, the new price falls by $12\\%$. By what percent is the final price higher than the original price?',
            ['$13\\%$', '$12.5\\%$', '$3\\%$', '$10\\%$'], 4, [
                'Multipliers: up $25\\%$ is $\\times1.25$, and down $12\\%$ is $\\times0.88$.',
                '$1.25\\times0.88=0.88+\\frac14\\times0.88=0.88+0.22=1.1$. The final price is $110\\%$ of the original: $10\\%$ higher.',
                'Plug in $100$: $100\\to125$. $12\\%$ of $125$ is $15$, so $125-15=110$ ✓.',
                'Shortcut: $25-12+\\frac{25\\cdot(-12)}{100}=25-12-3=10$.'])
    M.place_q(g1, ADV, after='solve-wp23-g060')
    _solution(M, g1, ["Up twenty-five, then down twelve. Where do we land?", "Try it first. Then let's solve it together."], [
        ('Method 1 · Multipliers', [
            "Two changes in a row. Use multipliers.",
            D('Write "+25% → ×1.25,   −12% → ×0.88"'),
            "Up twenty-five percent: times one point two five. Down twelve percent: we keep eighty-eight percent — times zero point eight eight.",
            D('Write "1.25 × 0.88 = 0.88 + 0.22 = 1.1"'),
            "One point two five times zero point eight eight: one times zero point eight eight, plus a quarter of it — zero point two two. Together, one point one.",
            D('Write "×1.1 → 10% higher" and circle choice 4'),
            "Times one point one: ten percent higher. Choice four.",
            "The trap is choice one: twenty-five minus twelve, thirteen. But the twelve percent is taken from the NEW, bigger price.",
        ]),
        ('Method 2 · Plug in 100', [
            D('Write "100 → 125"'),
            "Start at a hundred. Up twenty-five percent: a hundred twenty-five.",
            D('Write "12% of 125 = 12.5 + 2.5 = 15 → 110"'),
            "Twelve percent of one twenty-five: ten percent is twelve and a half, two percent is two and a half. Fifteen. A hundred twenty-five minus fifteen: a hundred ten.",
            D('Circle choice 4'),
            "A hundred ten: ten percent higher. Choice four.",
            D('Write "25 − 12 − 3 = 10"'),
            "Strong students: twenty-five minus twelve, then minus twenty-five times twelve over a hundred — minus three. Ten.",
        ]),
    ])

    # =====================================================================================
    # 6. New lesson video "Percent Traps and Shortcuts" + card + guided questions 2-5
    # =====================================================================================
    sb = ['More than or of?', 'Percentage points', 'Mixtures', 'Letters: plug in numbers', 'Estimate and test', 'Recap']
    M.new_video(TRAPS, TOPIC, 'Percent Traps and Shortcuts', sb, [
        dict(mode='title', title='Percent Traps and Shortcuts', script=[
            "The exam loves a few percent traps.",
            "Today: three traps — and two shortcuts that save a lot of time.",
        ]),
        dict(mode='concept', active=0, title='More than or of?', script=[
            A("'150% of 80' appears", T('$150\\%$ of $80$', size=48, gap=40)),
            D('Write "= 1.5 × 80 = 120"'),
            "A hundred fifty percent OF eighty: one and a half times eighty. A hundred twenty.",
            A("'50% more than 80' appears", T('$50\\%$ more than $80$', size=48, gap=40)),
            D('Write "= 80 + 40 = 120"'),
            "Fifty percent MORE than eighty: eighty, plus half of eighty. Also a hundred twenty. The same!",
            A("'150% more than 80' appears", T('$150\\%$ more than $80$', size=48, gap=40)),
            D('Write "= 80 + 120 = 200"'),
            "But a hundred fifty percent MORE than eighty: eighty, plus a hundred twenty. Two hundred.",
            A("'p% more than = (100 + p)% of' appears", T('$p\\%$ more than $=\\ (100+p)\\%$ of', size=48)),
            "The rule: p percent more than a number is a hundred plus p percent of it.",
            "Read the question slowly. \"Of\" or \"more than\"? It changes everything.",
        ]),
        dict(mode='concept', active=1, title='Percentage points', script=[
            A('A table appears: pass rate 20% in 2024, 25% in 2025',
              VIS({'type': 'table', 'headers': ['Year', 'Pass rate'], 'rows': [['2024', '20%'], ['2025', '25%']]}, w=560, h=150, gap=50)),
            "The pass rate at a school went from twenty percent to twenty-five percent. How much did it rise?",
            D('Write "25 − 20 = 5 percentage points"'),
            "Twenty-five minus twenty: five. But five WHAT? Five percentage points. That's the difference between two percents.",
            D('Write "5/20 × 100 = 25%"'),
            "The rise in percent? Use the change rule: the change, five, divided by the original, twenty. A quarter. Twenty-five percent.",
            A("'20% → 25%: up 5 percentage points = up 25%' appears",
              T('$20\\%\\to25\\%$: up $5$ percentage points $=$ up $25\\%$', size=42)),
            "So both are true: up five percentage points, and up twenty-five percent.",
            "The trap choice says \"up five percent\". That's wrong.",
        ]),
        dict(mode='concept', active=2, title='Mixtures', script=[
            A("'200 g of salt water is 10% salt. Add water to make it 8% salt. How much water?' appears",
              T('$200$ g of salt water is $10\\%$ salt. How much water must we add to make it $8\\%$ salt?', size=40, gap=50)),
            "A mixture question. The key: find what does NOT change.",
            "We add only water. So the salt stays the same.",
            D('Write "salt: 10% of 200 = 20 g"'),
            "Salt: ten percent of two hundred. Twenty grams — before and after.",
            D('Write "20 g = 8% → 1% = 2.5 g → 100% = 250 g"'),
            "After, those twenty grams are eight percent of the new total. One percent is two and a half grams. The whole: two hundred fifty grams.",
            D('Write "250 − 200 = 50 g of water"'),
            "We had two hundred. So we add fifty grams of water.",
            "Adding salt instead? Then the WATER stays the same. Always ask: what stays?",
        ]),
        dict(mode='concept', active=3, title='Letters: plug in numbers', script=[
            A("'What percent of a is b?' appears", T('What percent of $a$ is $b$?', size=48, gap=40)),
            A('The four choices appear',
              T('(1) $\\frac{100b}{a}$ $\\quad$ (2) $\\frac{b}{100a}$ $\\quad$ (3) $\\frac{100a}{b}$ $\\quad$ (4) $\\frac{ab}{100}$', size=46, gap=40)),
            "Letters in the answers? Plug in numbers — for the letters too.",
            "Choose easy numbers. Not zero, not one, and a different number for each letter.",
            D('Write "a = 50, b = 10:  10 out of 50 = 20%"'),
            "Say a is fifty and b is ten. Ten out of fifty is one fifth: twenty percent. That's our target.",
            D('Write "(1) 1000/50 = 20 ✓  (2) 10/5000  (3) 5000/10 = 500  (4) 500/100 = 5"'),
            "Now put the numbers into each choice. Only choice one gives twenty.",
            "If two choices give the target, choose new numbers — and test only those two.",
        ]),
        dict(mode='concept', active=4, title='Estimate and test', script=[
            A("'What percent of 320 is 90?' appears", T('What percent of $320$ is $90$?', size=48, gap=40)),
            A('The four choices appear', T('(1) $22\\%$ $\\quad$ (2) $28.125\\%$ $\\quad$ (3) $32\\%$ $\\quad$ (4) $36\\%$', size=44, gap=50)),
            "You don't always need the exact number. Estimate.",
            D('Write "25% of 320 = 80,   30% of 320 = 96"'),
            "Twenty-five percent of three twenty: a quarter — eighty. Thirty percent: ninety-six.",
            "Ninety is between eighty and ninety-six. So the answer is between twenty-five and thirty percent.",
            D('Circle choice 2'),
            "Only choice two is in that range. Done — no long division.",
            A("'After a 20% rise the price is 180. Original?' appears", T('After a $20\\%$ rise, the price is $180$. Original?', size=44)),
            "Second shortcut: test the choices. Start with a round one — say a hundred fifty.",
            D('Write "150 × 1.2 = 180 ✓"'),
            "A hundred fifty times one point two: a hundred eighty. It works. No equation needed.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            "Let's lock it in.",
            A("'p% more than = (100 + p)% of' appears", T('"$p\\%$ more than" $=$ "$(100+p)\\%$ of"', size=40)),
            A("'Difference of two percents = percentage points' appears", T('Difference of two percents $=$ percentage points', size=40)),
            A("'Mixtures: find what stays the same' appears", T('Mixtures: find what stays the same', size=40)),
            A("'Letters in the choices: plug in numbers' appears", T('Letters in the choices: plug in numbers', size=40)),
            A("'Estimate · test a round choice' appears", T('Estimate · test a round choice', size=40)),
            D('Tick each line'),
            "Four questions next. Try each one first. Then watch.",
        ]),
    ], ADV, after='solve-wp23-g065')

    M.new_card(CARD2, TOPIC, ADV, {
        'title': 'Percent traps and shortcuts',
        'intro': 'Three traps the exam loves, and two shortcuts that save time.',
        'tables': [{'title': 'Traps and shortcuts', 'head': ['Idea', 'Example'], 'rows': [
            ['"$p\\%$ more than" $=$ "$(100+p)\\%$ of"', '$50\\%$ more than $80=150\\%$ of $80=120$; $150\\%$ more than $80=200$'],
            ['Percentage points', '$20\\%\\to25\\%$: up $5$ percentage points, but up $\\frac{5}{20}=25\\%$'],
            ['Mixtures: what stays the same?', 'Add water: the salt stays. $20$ g salt $=8\\%$ → total $250$ g'],
            ['Letters in the choices: plug in numbers', 'What percent of $a$ is $b$? $a=50$, $b=10$ → $20\\%$ → test each choice'],
            ['Estimate', '$90$ of $320$: $25\\%=80$, $30\\%=96$ → between $25\\%$ and $30\\%$'],
            ['Test the choices', 'Start with a round choice: $150\\times1.2=180$ ✓'],
        ]}],
        'tips': ['Plugging in numbers: not $0$, not $1$, and a different number for each letter.',
                 'If two choices give your target, choose new numbers and test only those two.'],
    }, after=TRAPS)

    # guided 2: percentage points
    g2 = 'q-r26-t23-02'
    M.new_q(g2, TOPIC, 'Last year, $40\\%$ of the students in a school passed a test. This year, $50\\%$ of the students passed. The number of students in the school did not change. By what percent did the number of students who passed increase?',
            ['$10\\%$', '$20\\%$', '$25\\%$', '$125\\%$'], 3, [
                'Plug in $100$ students. Last year $40$ passed, and this year $50$ passed.',
                'The change is $50-40=10$. Divide by the original: $\\frac{10}{40}=\\frac14=25\\%$.',
                'The rate rose by $10$ percentage points, but the number of students who passed rose by $25\\%$.'])
    M.place_q(g2, ADV, after=CARD2)
    _solution(M, g2, ["The pass rate went up by ten. Ten what?", "Try it first. Then let's solve it together."], [
        ('Method 1 · Plug in 100', [
            "The number of students didn't change. Plug in a hundred students.",
            D('Write "last year: 40 passed,   this year: 50 passed"'),
            "Forty percent of a hundred: forty passed. Then fifty percent: fifty passed.",
            D('Write "change = 10,   10/40 = 1/4 = 25%" and circle choice 3'),
            "The change is ten. Divide by the ORIGINAL — forty. One quarter. Twenty-five percent. Choice three.",
            "The trap is choice one. Fifty minus forty is ten — but that's ten percentage points, not ten percent.",
            "And choice two divides by fifty, the new number. The change is always divided by where it started.",
        ]),
        ('Method 2 · Multiplier', [
            "Faster: the number of students is the same, so compare the rates directly.",
            D('Write "50/40 = 1.25 → +25%"'),
            "Fifty over forty: one point two five. A multiplier of one point two five means up twenty-five percent. Choice three.",
        ]),
    ])

    # guided 3: "of" vs "more than"
    g3 = 'q-r26-t23-03'
    M.new_q(g3, TOPIC, 'The price of a desk is $150\\%$ of the price of a chair. The price of a table is $150\\%$ more than the price of the chair. By what percent is the price of the table higher than the price of the desk?',
            ['$40\\%$', '$66\\frac23\\%$', '$100\\%$', '$50\\%$'], 2, [
                'Plug in $100$ for the chair. The desk is $150\\%$ of $100$: $150$.',
                'The table is $150\\%$ more than $100$: $100+150=250$.',
                'Compared with the desk: the change is $250-150=100$, and $\\frac{100}{150}=\\frac23=66\\frac23\\%$.'])
    M.place_q(g3, ADV, after='solve-' + g2)
    _solution(M, g3, ["Of, or more than? Read carefully.", "Try it first. Then let's solve it together."], [
        ('Method 1 · Plug in 100', [
            "No prices given. Plug in a hundred. Into whom? Both prices are compared to the chair — so the chair is the hundred.",
            D('Write "chair 100"'),
            D('Write "desk: 150% of 100 = 150"'),
            "The desk is a hundred fifty percent OF the chair: a hundred fifty.",
            D('Write "table: 100 + 150 = 250"'),
            "The table is a hundred fifty percent MORE than the chair: a hundred, plus a hundred fifty. Two hundred fifty.",
            "Now the question: higher than the DESK. So now the desk is the original.",
            D('Write "250 − 150 = 100,   100/150 = 2/3 = 66⅔%" and circle choice 2'),
            "The change is a hundred. Out of the desk's hundred fifty: two thirds. Sixty-six and two thirds percent. Choice two.",
        ]),
        ('The traps', [
            "Look at the traps.",
            D('Next to choice 3 write "difference 100 ≠ 100%"'),
            "Choice three: the difference is a hundred — but that's not a hundred percent. Divide by the desk's price.",
            D('Next to choice 1 write "100/250 — wrong base"'),
            "Choice one divides by the table's price. Wrong base.",
            D('Next to choice 4 write "150 − 100 = 50?"'),
            "Choice four reads both prices as a hundred fifty percent — and forgets the word \"more\".",
        ]),
    ])

    # guided 4: mixtures
    g4 = 'q-r26-t23-04'
    M.new_q(g4, TOPIC, 'A $300$-gram mixture of sugar and water is $20\\%$ sugar. How many grams of sugar must be added to make the mixture $40\\%$ sugar?',
            ['$100$', '$60$', '$80$', '$120$'], 1, [
                'Adding sugar does not change the water. Water: $80\\%$ of $300$ is $240$ g.',
                'After, the mixture is $60\\%$ water. $60\\%=240$ g, so $20\\%=80$ g and $100\\%=400$ g.',
                'Sugar to add: $400-300=100$ g.',
                'Check: sugar $60+100=160$ g out of $400$ g: $\\frac{160}{400}=40\\%$ ✓.'])
    M.place_q(g4, ADV, after='solve-' + g3)
    _solution(M, g4, ["A mixture question. Find what stays the same.", "Try it first. Then let's solve it together."], [
        ('Method 1 · What stays?', [
            "We add sugar. So the sugar changes, and the total changes. What stays? The water.",
            D('Write "water: 80% of 300 = 240 g"'),
            "The mixture is twenty percent sugar, so eighty percent water. Eighty percent of three hundred: two hundred forty grams of water.",
            D('Write "after: 240 g = 60%"'),
            "After, the mixture is forty percent sugar — sixty percent water. And the water is still two hundred forty grams.",
            D('Write "20% = 80 g → 100% = 400 g"'),
            "Sixty percent is two hundred forty, so twenty percent is eighty. The whole: four hundred grams.",
            D('Write "400 − 300 = 100 g of sugar" and circle choice 1'),
            "It was three hundred. So we added a hundred grams of sugar. Choice one.",
        ]),
        ('Method 2 · Test the choices', [
            "Or test the choices. Try the round one — a hundred.",
            D('Write "sugar 60 + 100 = 160,   total 400,   160/400 = 40% ✓"'),
            "Sugar: sixty, plus a hundred — a hundred sixty. Total: four hundred. A hundred sixty out of four hundred: forty percent. It works.",
            "The trap is choice two, sixty: that's twenty percent more of three hundred. But the total grows too.",
        ]),
    ])

    # guided 5: letters in the choices
    g5 = 'q-r26-t23-05'
    M.new_q(g5, TOPIC, 'A school has $N$ students, and $g$ of them are girls. $25\\%$ of the girls play chess. What percent of all the students are girls who play chess?',
            ['$\\frac{g}{4N}\\%$', '$\\frac{100g}{N}\\%$', '$\\frac{25g}{N}\\%$', '$\\frac{25N}{g}\\%$'], 3, [
                'Plug in numbers: $N=200$ and $g=80$. $25\\%$ of $80$ girls is $20$ girls who play chess.',
                '$\\frac{20}{200}=10\\%$. The target is $10$.',
                'Check the choices: $\\frac{80}{800}=0.1$, $\\frac{8000}{200}=40$, $\\frac{2000}{200}=10$ ✓, $\\frac{5000}{80}=62.5$.',
                'In general: $\\frac g4$ girls play chess, and $\\frac{g}{4}\\div N\\times100=\\frac{25g}{N}$.'])
    M.place_q(g5, ADV, after='solve-' + g4)
    _solution(M, g5, ["Letters in the answers. Plug in numbers.", "Try it first. Then let's solve it together."], [
        ('Method 1 · Plug in numbers', [
            "Choose easy numbers. N, the students: two hundred. g, the girls: eighty.",
            D('Write "N = 200,  g = 80"'),
            D('Write "25% of 80 = 20 girls play chess"'),
            "A quarter of eighty girls play chess: twenty.",
            D('Write "20/200 = 10%"'),
            "Out of all two hundred students: ten percent. Our target is ten.",
            D('Write "(1) 80/800 = 0.1  (2) 8000/200 = 40  (3) 2000/200 = 10 ✓  (4) 5000/80 = 62.5"'),
            "Choice one: a tenth. Choice two: forty — that's the percent of girls. Choice three: ten. Choice four: sixty-two and a half.",
            D('Circle choice 3'),
            "Only choice three gives ten. Choice three.",
        ]),
        ('Method 2 · Build it', [
            "Or build it. The girls who play chess: a quarter of g — g over four.",
            D('Write "(g/4) ÷ N × 100 = 25g/N"'),
            "Part over whole, times a hundred: g over four, divided by N, times a hundred. Twenty-five g over N. Choice three.",
            "Choice one is g over four N. That's a fraction of the students, not a percent. Watch for it.",
        ]),
    ])
    M.section_title(ADV, 'Further guided examples')

    # =====================================================================================
    # 7. Main memory card: after the percent tree, one name for the method, new rules
    # =====================================================================================
    M.move(CARD, 'wp23-learn', after='solve-wp23-g054')
    c = M.card(CARD)
    for tb in c['tables']:
        for r in tb['rows']:
            for k, x in enumerate(r):
                r[k] = x.replace('Equal ratios (triple value)', 'Equal ratios (triangle value)')
    meth = c['tables'][1]['rows']
    meth.insert(3, ['Change in percent', 'a rise or a fall', 'change $\\div$ original $\\times100$: $80\\to100$ is $\\frac{20}{80}=25\\%$'])
    meth.insert(4, ['Multiplier', 'one change or several', '$+20\\%\\to\\times1.2$, $-15\\%\\to\\times0.85$; $+10\\%$ twice: $1.1^2=1.21$'])
    c['tips'] = c['tips'] + [
        'Up $p\\%$ and down $p\\%$ (any order): a loss of $\\frac{p^2}{100}\\%$. $+20\\%$, $-20\\%$ → $-4\\%$.',
        'Any two changes $a\\%$ and $b\\%$: $a+b+\\frac{ab}{100}$ (a fall is negative). $+25$, $-20$ → $25-20-5=0$.']

    # =====================================================================================
    # 8. New practice questions (exam level) and the practice order
    # =====================================================================================
    P = [
        ('q-r26-t23-06', 'The number of members in a club grows by $10\\%$ every year. By what percent does it grow over three years?',
         ['$30\\%$', '$21\\%$', '$33.1\\%$', '$31\\%$'], 3,
         ['Each year: $\\times1.1$. Three years: $1.1^3=1.21\\times1.1=1.331$.',
          'That is $133.1\\%$ of the start: a growth of $33.1\\%$.']),
        ('q-r26-t23-07', 'In January, $20\\%$ of the workers in a factory worked at night. In February, $25\\%$ of the same workers worked at night. Which of the following statements is true?\nI. The share of night workers rose by $5$ percentage points.\nII. The number of night workers rose by $25\\%$.',
         ['I only', 'II only', 'Both I and II', 'Neither I nor II'], 3,
         ['I: $25\\%-20\\%=5$ percentage points. True.',
          'II: plug in $100$ workers. Night workers: $20\\to25$. The change is $5$, and $\\frac5{20}=25\\%$. True.']),
        ('q-r26-t23-08', 'A bank lowered its interest rate from $5\\%$ to $4\\%$. By what percent did the interest rate fall?',
         ['$1\\%$', '$20\\%$', '$25\\%$', '$4\\%$'], 2,
         ['The rate fell by $5-4=1$ percentage point.',
          'In percent: change divided by the original, $\\frac15=20\\%$.']),
        ('q-r26-t23-09', 'Given: $y>0$, and $x$ is $300\\%$ more than $y$. $x$ is what percent of $y$?',
         ['$300\\%$', '$400\\%$', '$200\\%$', '$133\\frac13\\%$'], 2,
         ['$300\\%$ more than $y$ is $(100+300)\\%=400\\%$ of $y$.',
          'Check: $y=10$ gives $x=10+30=40$, and $\\frac{40}{10}=400\\%$ ✓.']),
        ('q-r26-t23-10', 'A price was raised, and the new price was $120\\%$ of the original price. Later it was raised again, and it became $150\\%$ of the original price. By what percent was the price raised the second time?',
         ['$30\\%$', '$20\\%$', '$50\\%$', '$25\\%$'], 4,
         ['Plug in $100$ for the original price: $100\\to120\\to150$.',
          'The second rise is $150-120=30$, measured against $120$: $\\frac{30}{120}=\\frac14=25\\%$.',
          'The trap: $150-120=30$ percentage points is not $30\\%$.']),
        ('q-r26-t23-11', 'A $60$-liter drink is $25\\%$ juice, and the rest is water. How many liters of water must be removed so that the drink becomes $40\\%$ juice?',
         ['$22.5$', '$9$', '$15$', '$24$'], 1,
         ['Removing water does not change the juice: $25\\%$ of $60$ is $15$ liters.',
          'After: $15$ liters is $40\\%$ of the drink. $40\\%=15$, so $20\\%=7.5$ and $100\\%=37.5$ liters.',
          'Water to remove: $60-37.5=22.5$ liters.']),
        ('q-r26-t23-12', '$20$ liters of a drink that is $10\\%$ juice are mixed with $30$ liters of a drink that is $20\\%$ juice. What percent of the mixture is juice?',
         ['$15\\%$', '$30\\%$', '$16\\%$', '$14\\%$'], 3,
         ['Juice: $10\\%$ of $20$ is $2$ liters, and $20\\%$ of $30$ is $6$ liters. Together: $8$ liters.',
          'Mixture: $20+30=50$ liters. $\\frac{8}{50}=\\frac{16}{100}=16\\%$.',
          'The trap: $15\\%$ is the simple average, but there is more of the $20\\%$ drink.']),
        ('q-r26-t23-13', 'The price of a coat was raised by $20\\%$. Then the new price was lowered by $25\\%$, and the coat now costs $180$ credits. What was the original price?',
         ['$180$', '$200$', '$216$', '$225$'], 2,
         ['Multipliers: $1.2\\times0.75=0.9$. The final price is $90\\%$ of the original.',
          '$90\\%=180$, so $10\\%=20$ and $100\\%=200$.',
          'Or test the round choice: $200\\to240\\to240-60=180$ ✓.']),
        ('q-r26-t23-14', 'A number $x>0$ is increased by $p\\%$, and the result is then decreased by $p\\%$. What is the final number?',
         ['$x$', '$x\\left(1-\\frac{p}{100}\\right)^2$', '$x\\left(1-\\frac{p^2}{100}\\right)$', '$x\\left(1-\\frac{p^2}{10000}\\right)$'], 4,
         ['Multipliers: $x\\left(1+\\frac{p}{100}\\right)\\left(1-\\frac{p}{100}\\right)=x\\left(1-\\frac{p^2}{10000}\\right)$.',
          'Check with numbers: $x=100$ and $p=10$: $100\\to110\\to99$. The choices give $100$, $81$, $0$ and $99$ ✓.']),
    ]
    for qid, stem, ch, cor, ex in P:
        M.new_q(qid, TOPIC, stem, ch, cor, ex)
        M.place_q(qid, PRAC)

    M.practice_order(PRAC, [
        'wp23-p21', 'wp23-p01', 'wp23-p05', 'wp23-p02', 'wp23-p04', 'wp23-p09', 'wp23-p25', 'wp23-p26',
        'wp23-p12', 'wp23-p07', 'wp23-p22', 'wp23-p13', 'wp23-p15', 'wp23-p11', 'wp23-p27', 'wp23-p24',
        'wp23-p17', 'wp23-p08', 'q-r26-t23-08', 'q-r26-t23-07', 'wp23-p06', 'q-r26-t23-09', 'q-r26-t23-10',
        'wp23-p10', 'q-r26-t23-13', 'q-r26-t23-06', 'wp23-p14', 'wp23-p19', 'wp23-p23', 'q-r26-t23-11',
        'q-r26-t23-12', 'wp23-p20', 'wp23-p16', 'wp23-p18', 'q-r26-t23-14', 'wp23-p03'])
