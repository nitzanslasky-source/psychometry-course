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
# advanced-section solution videos: old numbers 2..10 + new guided questions 11..14 (renumbered automatically)
QSIDEBAR = ['Question %d' % n for n in range(2, 15)]


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
    # new slide 5: thirds and families (pass 2: the original "sixteen and a bit" line is back, before the exact value)
    M.insert_slides(L1, 4, [dict(mode='concept', active=3, title='Thirds and families', script=[
        A('A row appears: 1/3 = 33⅓%, 1/6 = 16⅔%', row3),
        "A third: thirty-three and a third percent.",
        D('Draw a "÷2" arrow from 1/3 to 1/6'),
        "A sixth is half a third. Can't halve it precisely? Half of thirty-two is sixteen — so it's sixteen and a bit.",
        "Exactly: half of thirty-three is sixteen and a half. Half of one third is one sixth.",
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
    # pass 2: the original p21 (16% of 25) is restored; the "28% of 75" version stays as a new question
    S('wp23-p21', stem='What is $16\\%$ of $25$?', choices=['$2$', '$6$', '$8$', '$4$'], correct=4, expl=[
        'Swap: $16\\%$ of $25$ equals $25\\%$ of $16$.',
        '$25\\%=\\frac14$, and $\\frac14\\times16=4$.',
        'The swap works because both are $\\frac{16\\times25}{100}=\\frac{400}{100}=4$.'])
    M.new_q('q-r26-t23-15', TOPIC, 'What is $28\\%$ of $75$?', ['$18$', '$24$', '$28$', '$21$'], 4, [
        'Swap: $28\\%$ of $75$ equals $75\\%$ of $28$.',
        '$75\\%=\\frac34$, and $\\frac34\\times28=21$.'])
    M.place_q('q-r26-t23-15', PRAC, after='wp23-p21')
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
    sb = ['More than or of?', 'Mixtures', 'Letters: plug in numbers', 'Estimate and test', 'Recap']
    M.new_video(TRAPS, TOPIC, 'Percent Traps and Shortcuts', sb, [
        dict(mode='title', title='Percent Traps and Shortcuts', script=[
            "The exam loves a few percent traps.",
            "Today: two traps — and two shortcuts that save a lot of time.",
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
        dict(mode='concept', active=1, title='Mixtures', script=[
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
        dict(mode='concept', active=2, title='Letters: plug in numbers', script=[
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
        dict(mode='concept', active=3, title='Estimate and test', script=[
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
        dict(mode='concept', active=4, title='Recap', script=[
            "Let's lock it in.",
            A("'p% more than = (100 + p)% of' appears", T('"$p\\%$ more than" $=$ "$(100+p)\\%$ of"', size=40)),
            A("'Mixtures: find what stays the same' appears", T('Mixtures: find what stays the same', size=40)),
            A("'Letters in the choices: plug in numbers' appears", T('Letters in the choices: plug in numbers', size=40)),
            A("'Estimate · test a round choice' appears", T('Estimate · test a round choice', size=40)),
            D('Tick each line'),
            "Three questions next. Try each one first. Then watch.",
        ]),
    ], ADV, after='solve-wp23-g065')

    M.new_card(CARD2, TOPIC, ADV, {
        'title': 'Percent traps and shortcuts',
        'intro': 'Two traps the exam loves, and two shortcuts that save time.',
        'tables': [{'title': 'Traps and shortcuts', 'head': ['Idea', 'Example'], 'rows': [
            ['"$p\\%$ more than" $=$ "$(100+p)\\%$ of"', '$50\\%$ more than $80=150\\%$ of $80=120$; $150\\%$ more than $80=200$'],
            ['Mixtures: what stays the same?', 'Add water: the salt stays. $20$ g salt $=8\\%$ → total $250$ g'],
            ['Letters in the choices: plug in numbers', 'What percent of $a$ is $b$? $a=50$, $b=10$ → $20\\%$ → test each choice'],
            ['Estimate', '$90$ of $320$: $25\\%=80$, $30\\%=96$ → between $25\\%$ and $30\\%$'],
            ['Test the choices', 'Start with a round choice: $150\\times1.2=180$ ✓'],
        ]}],
        'tips': ['Plugging in numbers: not $0$, not $1$, and a different number for each letter.',
                 'If two choices give your target, choose new numbers and test only those two.'],
    }, after=TRAPS)

    # guided 3: "of" vs "more than"
    g3 = 'q-r26-t23-03'
    M.new_q(g3, TOPIC, 'The price of a desk is $150\\%$ of the price of a chair. The price of a table is $150\\%$ more than the price of the chair. By what percent is the price of the table higher than the price of the desk?',
            ['$40\\%$', '$66\\frac23\\%$', '$100\\%$', '$50\\%$'], 2, [
                'Plug in $100$ for the chair. The desk is $150\\%$ of $100$: $150$.',
                'The table is $150\\%$ more than $100$: $100+150=250$.',
                'Compared with the desk: the change is $250-150=100$, and $\\frac{100}{150}=\\frac23=66\\frac23\\%$.'])
    M.place_q(g3, ADV, after=CARD2)
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
        ('q-r26-t23-09', 'Given: $y>0$, and $x$ is $300\\%$ more than $y$. $x$ is what percent of $y$?',
         ['$300\\%$', '$400\\%$', '$200\\%$', '$133\\frac13\\%$'], 2,
         ['$300\\%$ more than $y$ is $(100+300)\\%=400\\%$ of $y$.',
          'Check: $y=10$ gives $x=10+30=40$, and $\\frac{40}{10}=400\\%$ ✓.']),
        ('q-r26-t23-10', 'A price was raised, and the new price was $120\\%$ of the original price. Later it was raised again, and it became $150\\%$ of the original price. By what percent was the price raised the second time?',
         ['$30\\%$', '$20\\%$', '$50\\%$', '$25\\%$'], 4,
         ['Plug in $100$ for the original price: $100\\to120\\to150$.',
          'The second rise is $150-120=30$, measured against $120$: $\\frac{30}{120}=\\frac14=25\\%$.',
          'The trap is $30\\%$: the rise of $30$ is measured against $120$, not against the original $100$.']),
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
        'wp23-p21', 'q-r26-t23-15', 'wp23-p01', 'wp23-p05', 'wp23-p02', 'wp23-p04', 'wp23-p09', 'wp23-p25', 'wp23-p26',
        'wp23-p12', 'wp23-p07', 'wp23-p22', 'wp23-p13', 'wp23-p15', 'wp23-p11', 'wp23-p27', 'wp23-p24',
        'wp23-p17', 'wp23-p08', 'wp23-p06', 'q-r26-t23-09', 'q-r26-t23-10',
        'wp23-p10', 'q-r26-t23-13', 'q-r26-t23-06', 'wp23-p14', 'wp23-p19', 'wp23-p23', 'q-r26-t23-11',
        'q-r26-t23-12', 'wp23-p20', 'wp23-p16', 'wp23-p18', 'q-r26-t23-14', 'wp23-p03'])
    summary(M)
    cut_repeats(M)
    add_methods(M)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)


# =====================================================================================
# 9. Pass 2: summary lesson right before the practice
# =====================================================================================
def summary(M):
    sb = ['The percent formula', 'Fractions to know', 'Equal ratios', 'The 10% method', 'Change in percent',
          'What is my 100%?', 'Multipliers', 'Traps and shortcuts', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of percentages.",
            "Everything important, one idea at a time."]),
        S(0, [
            A('\'Percent = over 100 · "of" = times\' appears', T('Percent = over $100$ · "of" = times', size=44, gap=40)),
            "Percent means over a hundred. \"Of\" means times.",
            A("'p/100 × whole = part' appears", T('$\\frac{p}{100}\\times\\text{whole}=\\text{part}$', size=54, gap=40)),
            "That's the percent formula. Ninety-five percent of sixty: ninety-five over a hundred, times sixty. Fifty-seven.",
            "Unknown percent? Unknown whole? The same equation — just solve it.",
            A("'8% of 50 = 50% of 8 = 4' appears", T('$8\\%$ of $50=50\\%$ of $8=4$', size=46)),
            "And you may swap them: a percent of b equals b percent of a."]),
        S(1, [
            A('A row appears: 1/2, 1/4, 1/8',
              dict(k='row', items=['$\\frac12=50\\%$', '$\\frac14=25\\%$', '$\\frac18=12.5\\%$'], sp=340, below=70)),
            A('A row appears: 1/5, 1/10, 1/20',
              dict(k='row', items=['$\\frac15=20\\%$', '$\\frac1{10}=10\\%$', '$\\frac1{20}=5\\%$'], sp=340, below=70)),
            A('A row appears: 1/3, 1/6',
              dict(k='row', items=['$\\frac13=33\\frac13\\%$', '$\\frac16=16\\frac23\\%$'], sp=420)),
            "Know these by heart. Halve to go down: fifty, twenty-five, twelve and a half.",
            "Then build the families. Seven eighths: seven times twelve and a half — eighty-seven and a half."]),
        S(2, [
            A('A ratio table appears: 100% → 60, 95% → ?',
              dict(k='vis', v={'type': 'table', 'headers': ['Percent', 'Amount'], 'rows': [['100%', '60'], ['95%', '?']]},
                   w=560, h=150, gap=50)),
            "Equal ratios — the triangle value. Percents on the left, amounts on the right.",
            A("'Multiply along the diagonal, divide by what's left' appears",
              T("Multiply along the diagonal, divide by what's left", size=42, gap=40)),
            D('Write "95 × 60 ÷ 100 = 57"'),
            "Ninety-five times sixty, divided by a hundred: fifty-seven.",
            "You can also jump between percents. Twelve percent is thirty? Then four percent is ten, and twenty-eight percent is seventy. No whole needed."]),
        S(3, [
            A("'10% of 340 = 34' appears", T('$10\\%$ of $340=34$', size=50, gap=40)),
            "Ten percent: just divide by ten.",
            A("'45% = 40% + 5% = 136 + 17 = 153' appears", T('$45\\%=40\\%+5\\%=136+17=153$', size=46, gap=40)),
            "Then build any percent from ten-percent chunks. Five percent is half of ten percent.",
            A("'40% = 68 → 10% = 17 → 100% = 170' appears", T('$40\\%=68\\ \\to\\ 10\\%=17\\ \\to\\ 100\\%=170$', size=46)),
            "Whole missing? Go down to ten percent, then up to a hundred."]),
        S(4, [
            A("'Change in % = change ÷ original × 100' appears",
              T('Change in $\\% = \\frac{\\text{change}}{\\text{original}}\\times100$', size=46, gap=40)),
            "A change is always measured against where it started — the original.",
            A("'40 → 50: 10/40 = 25%' appears", T('$40\\to50$: $\\ \\frac{10}{40}=25\\%$', size=48, gap=40)),
            "Forty up to fifty: ten out of forty. Twenty-five percent — not twenty.",
            A("'After a 25% loss: 45 = 75% → 100% = 60' appears", T('After a $25\\%$ loss: $\\ 45=75\\%\\ \\to\\ 100\\%=60$', size=44)),
            "Going backwards? Forty-five is what STAYED — seventy-five percent. The original: sixty."]),
        S(5, [
            A("'Whole not given? Plug in 100' appears", T('Whole not given? Plug in $100$', size=46, gap=40)),
            "No starting number? Plug in a hundred. The number you get at the end is the percent.",
            A('\'The whole comes after "of" / "than"\' appears', T('The whole comes after "of" / "than" — in the question', size=40, gap=40)),
            "Who is the hundred? The word after \"of\" or \"than\" — in the question itself.",
            A("'100 → 150 → 120' appears", T('$+50\\%$, then $-20\\%$: $\\ 100\\to150\\to120$', size=46)),
            "And it can change on the way. After the rise, the twenty percent is of a hundred fifty, not of a hundred.",
            "Each new percent sits on the new amount.",
            "A fixed amount in the story? Then a hundred doesn't work. Use the real number, or a letter."]),
        S(6, [
            A("'Up x%: ×(1 + x/100) · Down x%: ×(1 − x/100)' appears",
              T('Up $x\\%$: $\\times\\left(1+\\frac{x}{100}\\right)$ $\\qquad$ Down $x\\%$: $\\times\\left(1-\\frac{x}{100}\\right)$', size=40, gap=40)),
            "Up forty percent: times one point four. Down thirty-five: times zero point six five.",
            A("'−10%, then −10%: 0.9 × 0.9 = 0.81' appears", T('$-10\\%$, then $-10\\%$: $\\ 0.9\\times0.9=0.81$', size=44, gap=40)),
            "Several changes? Multiply the factors. Down ten percent twice is down nineteen, not twenty.",
            A("'Up p% and down p%: a loss of p²/100 %' appears", T('Up $p\\%$ and down $p\\%$: a loss of $\\frac{p^2}{100}\\%$', size=42, gap=40)),
            "Up forty and down forty is not back to the start. It's sixteen percent lower.",
            A("'40% of 30% = 12%' appears", T('$40\\%$ of $30\\%=0.4\\times30\\%=12\\%$', size=44)),
            "A percent of a percent? Multiply them — the percent tree."]),
        S(7, [
            A("'p% more than = (100 + p)% of' appears", T('$p\\%$ more than $=\\ (100+p)\\%$ of', size=44, gap=40)),
            "Forty percent more than sixty is a hundred forty percent of sixty: eighty-four.",
            A("'Mixtures: find what stays the same' appears", T('Mixtures: find what stays the same', size=42, gap=40)),
            "Add water? The salt stays. Add sugar? The water stays.",
            A("'Letters in the choices: plug in numbers' appears", T('Letters in the choices: plug in numbers', size=42, gap=40)),
            "Not zero, not one, and a different number for each letter.",
            A("'Estimate · test a round choice' appears", T('Estimate · test a round choice', size=42)),
            "And you don't always need the exact number. Estimate, or test a round choice."]),
        S(8, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('What is my $100\\%$? It can change when there are several stages.', size=38, gap=30)),
            A('Check 2 appears', T('"Of" or "more than"?', size=40, gap=30)),
            A('Check 3 appears', T('A change? Divide by the ORIGINAL.', size=40, gap=30)),
            A('Check 4 appears', T('A mixture? What stays the same?', size=40)),
            "And the traps: adding percents that sit on different amounts, dividing a change by the new number, and thinking that up and down brings you back to the start.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t23-summary', TOPIC, 'Summary: Percentages', sb, slides, ADV, after=last)


# =====================================================================================
# 2026-10-05 cut repeats: "Percent Traps and Shortcuts" back to a short intro; every idea a
# question video right after it teaches is cut; what no question teaches stays or moves as
# one line + board item into the question video that uses it.
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


def cut_repeats(M):
    vid = 'r26-t23-traps'
    b5 = M.slide(vid, 5); its = b5['items']
    q_item = next(it for it in its if 'What percent of' in (it.get('t') or ''))
    ch_item = next(it for it in its if '28.125' in (it.get('t') or ''))
    M.remove_slides(vid, [2, 3, 4, 6])
    M.set_slide(vid, 1, script=[
        'The exam loves a few percent traps.',
        "We'll meet them in the questions. First, one shortcut no question shows: estimate."])
    M.set_slide(vid, 2, title='Estimate', active=0, pre=[], script=[
        A("'What percent of 320 is 90?' appears", dict(q_item)),
        A("The four choices appear", dict(ch_item)),
        "You don't always need the exact number. Estimate.",
        D('Write "25% of 320 = 80,   30% of 320 = 96"'),
        'Twenty-five percent of three twenty: a quarter — eighty. Thirty percent: ninety-six.',
        'Ninety is between eighty and ninety-six. So the answer is between twenty-five and thirty percent.',
        D('Circle choice 2'),
        'Only choice two is in that range. Done — no long division.',
        'Three questions next. Try each one first. Then watch.'])
    M.set_sidebar(vid, ['Estimate'])

    # "More than or of?" -> taught in Q (desk/table); move the general rule there
    _add_line(M, 'solve-q-r26-t23-03', 2, 'The table is a hundred fifty percent MORE',
              'The rule: p percent more than a number is a hundred plus p percent of it.',
              T(r'$p\%$ more than $=\ (100+p)\%$ of', 36), "'p% more than = (100 + p)% of' appears")
    # "Mixtures" -> taught in Q (sugar); add the other direction
    _add_line(M, 'solve-q-r26-t23-04', 2, 'We add sugar. So the sugar changes',
              'Mixtures: always ask what stays the same. Add water, and the sugar stays. Add sugar, and the water stays.',
              T('Mixtures: find what stays the same', 36), "'Mixtures: find what stays the same' appears")
    # "Letters: plug in numbers" -> taught in Q (chess); add the number-choice rules
    _add_line(M, 'solve-q-r26-t23-05', 2, 'Choose easy numbers',
              'Easy numbers: not zero, not one, a different number for each letter. If two choices hit the target, pick new numbers and test only those two.',
              T('Not 0, not 1, different numbers · two hit? new numbers', 34),
              "'Not 0, not 1, different numbers · two hit? new numbers' appears")


# =====================================================================================
# 2026-10-06 new exam methods (teacher-approved): the flip rule, the arrow map, fee on top,
# "rose by" vs "became", and a softer plug-in rule (0 / "nothing changes" can be the best number).
# Runs last.
# =====================================================================================
def add_methods(M):
    # ---- 1. The flip rule: two new slides in "Calculating Percentages", before the recap -----------
    M.insert_slides(L1, 9, [
        dict(mode='concept', active=8, title='Same part: flip', script=[
            "Here's a question type the exam loves.",
            A("'40% of A = 15% of B. Ratio A : B?' appears", T(r'$40\%$ of $A\ =\ 15\%$ of $B$. $\quad$ Ratio $A:B\ =\ ?$', size=42, gap=40)),
            "The cue: one amount, written as a percent of two different things. Forty percent of A and fifteen percent of B are the same number.",
            "First, think. Which one is bigger, A or B?",
            "To get the same amount, a big percent needs only a small whole. A small percent needs a big whole.",
            "So A, with the big percent, is the smaller one.",
            A("'Same part → flip: ratio A : B = 15 : 40 = 3 : 8' appears", T(r'Same part $\to$ flip: $\ $ ratio $A:B=15:40=3:8$', size=42, gap=40)),
            "And that's the rule: the ratio is the percents — flipped. A to B is fifteen to forty. Divide both by five: three to eight.",
            D('Write "0.4A = 0.15B  →  A/B = 0.15/0.4 = 15/40"'),
            "Why does it flip? Write it as an equation: zero point four A equals zero point one five B. Divide both sides by B, and by zero point four. A over B is zero point one five over zero point four — fifteen over forty.",
            D('Write "check A = 3, B = 8:  0.4 · 3 = 1.2,  0.15 · 8 = 1.2 ✓"'),
            "Check it. A is three, B is eight. Forty percent of three: one point two. Fifteen percent of eight: one point two. Equal.",
            "You know this from ratios: four mugs cost the same as three plates — so mug to plate is three to four. Reversed. It's the same idea.",
            D('Write "2/3 of A = 4/5 of B  →  ratio A : B = 4/5 : 2/3 = 6 : 5"'),
            "It works with fractions too. Two thirds of A equals four fifths of B: A to B is four fifths to two thirds. Times fifteen: twelve to ten. Six to five.",
            "One warning. The two amounts must be EQUAL. If forty percent of A is six MORE than fifteen percent of B, there's no flip — write the equation.",
        ]),
        dict(mode='concept', active=9, title='Same whole: keep', script=[
            "Now the opposite case.",
            A("'a = 50% of b,  c = 125% of b. Ratio c : a?' appears", T(r'$a=50\%$ of $b$, $\ c=125\%$ of $b$. $\quad$ Ratio $c:a\ =\ ?$', size=42, gap=40)),
            "Here the two amounts are percents of the SAME whole, b.",
            "Same whole — then the bigger percent gives the bigger amount. The amounts are in the same ratio as the percents. No flip.",
            D('Write "b = 100  →  a = 50,  c = 125"'),
            "See it with a hundred. b is a hundred: a is fifty, c is a hundred twenty-five.",
            A("'Same whole → keep: ratio c : a = 125 : 50 = 5 : 2' appears", T(r'Same whole $\to$ keep: $\ $ ratio $c:a=125:50=5:2$', size=42, gap=40)),
            "c to a: a hundred twenty-five to fifty. Divide by twenty-five: five to two. So c is two hundred fifty percent of a.",
            A("'Same PART → flip · Same WHOLE → keep' appears", T('Same PART $\\to$ flip $\\ \\cdot\\ $ Same WHOLE $\\to$ keep', size=46)),
            "So ask one question: what is shared?",
            "The same part — flip the percents. The same whole — keep their order.",
        ]),
    ])
    M.set_sidebar(L1, ['What a percent is', 'Percent ↔ fraction', 'Fractions to know', 'Thirds and families',
                       'The percent equation', 'Equal ratios', 'The 10% method', 'More tools', 'Same part: flip',
                       'Same whole: keep', 'Recap'])
    _set_active(M, L1, {12: 10})

    # ---- 2. The arrow map: two new slides in "Percent of a Percent", after "Working backwards" -------
    M.insert_slides(L2, 8, [
        dict(mode='concept', active=7, title='The arrow map', script=[
            "One more picture, for chains of comparisons: the arrow map.",
            "The cue: sentences like \"x is twenty percent more than y\", or \"P is forty percent of Q\".",
            A("'x is 20% more than y:  y → x, ×1.2' appears", T(r'$x$ is $20\%$ more than $y$: $\quad y\xrightarrow{\ \times1.2\ }x$', size=46, gap=40)),
            "Each sentence is one arrow. It starts at the whole — the word after \"than\" or \"of\" — and points to the other one.",
            "On the arrow, write the multiplier. Twenty percent more than y: from y to x, times one point two.",
            A("'Along the arrow: × · Against it: ÷' appears", T(r'Along the arrow: $\times$ $\quad\cdot\quad$ Against it: $\div$', size=46, gap=40)),
            "Along the arrow, multiply. Against the arrow, divide.",
            "Now: what percent of x is y? We go from x to y — against the arrow. So we divide.",
            D('Write "y = x ÷ 1.2 = x · 5/6 → 83⅓% of x"'),
            "x divided by one point two. One point two is six fifths, and dividing by six fifths is multiplying by five sixths. Five sixths: eighty-three and a third percent.",
            D('Next to it write "not 80%!"'),
            "The trap is eighty percent. Twenty percent more one way is NOT twenty percent less the other way — the whole has changed.",
        ]),
        dict(mode='concept', active=8, title='Walk the path', script=[
            A("'P = 40% of Q,  R is 25% more than Q. R is what % of P?' appears",
              T(r'$P=40\%$ of $Q$, $\ R$ is $25\%$ more than $Q$. $\ R$ is what $\%$ of $P$?', size=40, gap=40)),
            "A longer one. Two sentences, and both start at Q.",
            A("'P ← ×0.4 — Q — ×1.25 → R' appears", T(r'$P\xleftarrow{\ \times0.4\ }Q\xrightarrow{\ \times1.25\ }R$', size=50, gap=40)),
            "P is forty percent of Q: an arrow from Q to P, times zero point four. R is twenty-five percent more than Q: an arrow from Q to R, times one point two five.",
            "We need R compared with P. So walk from P to R.",
            "P back to Q — against the arrow: divide by zero point four. Then Q to R — along the arrow: times one point two five.",
            D('Write "R/P = 1.25 ÷ 0.4 = 3.125 = 312.5%"'),
            "One point two five divided by zero point four: three point one two five. R is three hundred twelve and a half percent of P.",
            D('Write "check Q = 100:  P = 40,  R = 125,  125/40 = 3.125 ✓"'),
            "Check with a hundred. Q is a hundred, P is forty, R is a hundred twenty-five. A hundred twenty-five over forty: three point one two five. The same.",
            "So plugging in a hundred still works. The map is a second picture — it helps when the chain is long, or when the hundred doesn't land on the right person.",
            "The limit: every step must be a percent or a multiple. If a fixed amount is added — plus fifteen credits — it's not one multiplier. Use real numbers.",
            A("'Answer = the product along the path' appears", T('Answer $=$ the product along the path', size=46)),
            "The rule: along the arrow, multiply. Against it, divide. The answer is the product along your path.",
        ]),
    ])
    M.set_sidebar(L2, ['Plug in 100', 'Two losses', 'Multipliers', 'Up and down', 'Who is the 100?',
                       'When 100 fails', 'Working backwards', 'The arrow map', 'Walk the path', 'Recap'])
    _set_active(M, L2, {11: 9})

    # ---- 3. Guided question: the flip rule (after Q9 "not equal to 15% of 4x", the inverse-ratio question) ---
    qs2 = ['Question %d' % n for n in range(2, 16)]
    for v in M.D['videos'].values():
        if v['topic'] == TOPIC and v.get('kind') == 'solution' and (v.get('hybrid') or {}).get('sidebar') == QSIDEBAR:
            M.set_sidebar(v['id'], qs2)
    g = 'q-r26-t23-16'
    M.new_q(g, TOPIC, 'A library has only novels and textbooks, $600$ books in all. $45\\%$ of the novels is the same number of books as $30\\%$ of the textbooks. How many novels does the library have?',
            ['$360$', '$240$', '$300$', '$180$'], 2, [
                'The same amount is $45\\%$ of the novels $N$ and $30\\%$ of the textbooks $T$: $0.45N=0.3T$.',
                'Same part, so flip the percents: the ratio $N:T=30:45=2:3$.',
                '$2+3=5$ parts $=600$ books, so $1$ part $=120$ and $N=2\\cdot120=240$.',
                'Check: $45\\%$ of $240$ is $108$, and $30\\%$ of $600-240=360$ is $108$ ✓.'])
    M.place_q(g, ADV, after='solve-wp23-g063')
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=[
        "Two percents, one amount. There's a shortcut for this.", "Try it first. Then let's solve it together."])]
    for title, script in [
        ('Method 1 · The flip rule', [
            "Forty-five percent of the novels and thirty percent of the textbooks are the SAME number of books. One part, two different wholes. That's the cue for the flip rule.",
            D('Write "45% of N = 30% of T"'),
            "Which pile is bigger? To get the same amount, the smaller percent needs the bigger whole. Thirty is the smaller percent — so there are more textbooks.",
            D('Write "0.45N = 0.3T  →  N/T = 0.3/0.45"'),
            "As an equation: zero point four five N equals zero point three T. Divide both sides by T and by zero point four five: N over T is zero point three over zero point four five. The percents, flipped.",
            D('Write "ratio N : T = 30 : 45 = 2 : 3"'),
            "Novels to textbooks: thirty to forty-five. Divide both by fifteen: two to three.",
            D('Write "5 parts = 600  →  1 part = 120  →  N = 2 · 120 = 240"'),
            "Two plus three: five parts. Six hundred books over five parts: a hundred twenty in a part. The novels get two parts: two hundred forty.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
        ('Check and the traps', [
            D('Write "45% of 240 = 108,   30% of 360 = 108 ✓"'),
            "Always check. Textbooks: six hundred minus two forty — three sixty. Forty-five percent of two forty: a hundred eight. Thirty percent of three sixty: a hundred eight. Equal.",
            D('Next to choice 1 write "no flip"'),
            "Choice one, three sixty, is the trap: the ratio forty-five to thirty, with no flip. It gives the novels the bigger pile — but the bigger percent belongs to the SMALLER pile.",
            D('Next to choice 4 write "30% of 600"'),
            "Choice four is thirty percent of all six hundred. But each percent is of its own pile, not of the total.",
            "The rule: the same part — flip the percents. The same whole — keep them.",
        ])]:
        beats.append(dict(mode='question', active=qs2.index('Question %d' % n), title=title, pre=[Q(g)], script=script))
    v = M.new_video('solve-' + g, TOPIC, 'Advanced Percentages', qs2, beats, ADV, kind='solution', qid=g)
    v['beats'][0]['title'] = 'Advanced Percentages'
    v['hybrid']['num'] = 21
    v['title'] = v['navLabel'] = _plain(M.q(g)['stem'])

    # ---- 4. Memory cards ---------------------------------------------------------------------------
    c = M.card(CARD)
    meth = c['tables'][1]['rows']
    k = next(i for i, r in enumerate(meth) if r[0] == 'Multiplier') + 1
    meth[k:k] = [
        ['Flip rule', 'the same amount is a percent of two things',
         '$40\\%$ of $A=15\\%$ of $B$ → ratio $A:B=15:40=3:8$. Same WHOLE → keep the order: $a=50\\%$ of $b$, $c=125\\%$ of $b$ → $c:a=125:50$'],
        ['Arrow map', 'a chain of "is $p\\%$ of" / "$p\\%$ more (less) than"',
         'each sentence is an arrow with its multiplier; along it $\\times$, against it $\\div$: $x=1.2y$ → $y=x\\div1.2=83\\frac13\\%$ of $x$ (not $80\\%$)'],
    ]
    c2 = M.card(CARD2)
    c2['intro'] = 'Traps the exam loves, and shortcuts that save time.'
    c2['tables'][0]['rows'] += [
        ['Fee or tax on top: divide, don\'t take $75\\%$', 'paid $100$ with a $25\\%$ tax → before tax $100\\div1.25=80$, not $75$ (check: $80\\cdot1.25=100$)'],
        ['"Rose BY" or "became"?', '$\\times3.75$: it became $375\\%$ of the start — it rose BY $275\\%$'],
    ]
    c2['tips'] = [
        'Plugging in numbers: usually avoid $0$ and $1$, and use a different number for each letter. But if $0$ (or "nothing changes") makes the answer obvious, use it. Example: $k$ new students join — when $k=0$ the change must be $0$, so only a choice that gives $0$ at $k=0$ survives. If two choices survive, plug in a second number.',
        'If two choices give your target, choose new numbers and test only those two.']
    # the same softer rule where it is spoken (Q "N students, g girls" and the summary)
    vid = 'solve-q-r26-t23-05'
    for b in M.video(vid)['beats']:
        for it in b['items']:
            if (it.get('t') or '').startswith('Not 0, not 1'):
                it['t'] = 'Usually not 0 or 1, different numbers · two hit? new numbers'
        for l in b['lines']:
            if l.get('label', '').startswith("'Not 0, not 1"):
                l['label'] = "'Usually not 0 or 1, different numbers · two hit? new numbers' appears"
            if 'say' in l and l['say'].startswith('Easy numbers: not zero, not one,'):
                l['say'] = l['say'].replace('Easy numbers: not zero, not one,', 'Easy numbers: usually not zero or one, and')
    M.touched_videos.add(vid)
    vid = 'r26-t23-summary'
    for b in M.video(vid)['beats']:
        for l in b['lines']:
            if l.get('say') == 'Not zero, not one, and a different number for each letter.':
                l['say'] = 'Usually not zero or one, and a different number for each letter.'
    M.touched_videos.add(vid)


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
    _pm_add(M, 'wp23-p26', [r'Method 2 · Arrow map: trainee → worker is the arrow $\times1.25$. Going back against the arrow, divide: $\div1.25=\times0.8$. The trainee earns $80\%$ of the worker’s wage: $20\%$ lower.'])
    _pm_add(M, 'wp23-p14', [r'Method 2 · Flip rule, same whole → keep: both percents are of the same balance, therefore the bigger percent gives the bigger amount and the order stays. The ratio $p:q=90:150=3:5$, that is, $5p=3q$. (Flipping it, $3p=5q$, is the trap.)'])
    _pm_add(M, 'wp23-p13', [r'Method 2 · Arrow map: original → new price is $\times1.4$, and original → target is $\times1.12$. From the new price to the target, go against the first arrow and along the second: $1.12\div1.4=0.8$. The price drops to $80\%$: a $20\%$ fall.'])
    _pm_add(M, 'q-r26-t23-10', [r'Method 2 · Arrow map: original → first price $\times1.2$, original → second price $\times1.5$. From the first price to the second: $1.5\div1.2=1.25$, a rise of $25\%$.'])
    _pm_add(M, 'q-r26-t23-09', [r'"Rose BY" or "became"? $300\%$ more means $x$ rose BY $300\%$. It BECAME $100\%+300\%=400\%$ of $y$ (the multiplier $\times4$). The trap $300\%$ mixes up the two.'])
    _pm_add(M, 'q-r26-t23-13', [r'Method 2 · Arrow map: original $\times1.2$, then $\times0.75$, gives $180$. Walk back against the arrows, dividing: $180\div0.75\div1.2=240\div1.2=200$.'])


# =====================================================================================
# 2026-10-06 renumber pass (runs LAST, after practice_methods)
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived question (guided
# wp23-g054, g057 .. g065; practice wp23-p01 .. p20) gets new numbers and a new story (names, objects, setting) -
# same concept, same trap, same level, at least the same methods - and every guided solution video is rewritten to
# match. The Hebrew lesson examples in "Calculating Percentages" and "Percent of a Percent" get new numbers, and the
# memory card follows them. g058 (the easiest) moves before g057. Approved practice clean-up: 35 -> 26.
# Nothing in topic 23 is recorded (no take in ~/Documents/Course.recordings, checked 2026-10-06).
# =====================================================================================
RN_RECORDED = set()


def _rn_walk(x, mp, used):
    """Replace exact whole strings (keys of mp) anywhere inside x (str / list / dict)."""
    if isinstance(x, str):
        if x in mp: used.add(x); return mp[x]
        return x
    if isinstance(x, list): return [_rn_walk(y, mp, used) for y in x]
    if isinstance(x, dict): return {k: (_rn_walk(v, mp, used) if k not in ('k', 'qid') else v) for k, v in x.items()}
    return x


def _rn_slide(M, vid, n, mp):
    """Exact whole-string replacement on one slide (spoken lines, draw cues, labels, board items, tables).
    Every key must be found. Single pass: a replacement never feeds another one."""
    from math_api import rich_plain
    if vid in RN_RECORDED: return
    b = M.slide(vid, n); used = set()
    b['lines'] = _rn_walk(b['lines'], mp, used)
    b['items'] = _rn_walk(b['items'], mp, used)
    miss = set(mp) - used
    assert not miss, '%s #%d: not found: %s' % (vid, n, sorted(miss))
    if b['pre'] and (b.get('canvas') or '').startswith('Pre-loaded'):
        b['canvas'] = 'Pre-loaded — ' + '; '.join(rich_plain(it.get('t', it.get('qid', 'figure'))).replace('\\%', '%') for it in b['items'][:b['pre']])
    M.touched_videos.add(vid)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_item(M, vid, n, k):
    b = M.slide(vid, n); return b['items'][k]


def _rn_video(M, qid, title_lines, slides):
    """Rewrite a guided question's solution video: title-slide lines + every question slide (title, script).
    The pre-loaded question stays."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    if title_lines is not None:
        # {line index: new text}. Spoken "Question N" uses the BASE numbering (renumber_guided() maps it),
        # so the first line ("Question six.") is normally kept as it is.
        b0 = v['beats'][0]; assert b0['mode'] == 'title'
        for k, t in title_lines.items():
            assert 'say' in b0['lines'][k], (vid, k)
            b0['lines'][k] = {'say': t}
    for n, (title, script) in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, title=title, script=script)
    v['title'] = v['navLabel'] = _plain(M.q(qid)['stem'])
    M.touched_videos.add(vid)


def rn_guided(M):
    # ---------- G1 wp23-g054: survey, 55% no bicycle; of owners 40% electric, rest ordinary only -> 27%
    #            ==> students, 35% play no instrument; of players 80% piano, rest guitar only -> 13%
    g = 'wp23-g054'
    _rn_q(M, g, 'In a survey, $35\\%$ of the students do not play a musical instrument. Of the students who play an instrument, $80\\%$ play the piano and the rest play only the guitar. What percentage of all the surveyed students play only the guitar?',
          ['$20\\%$', '$52\\%$', '$13\\%$', '$80\\%$'], 3, [
              'Plug in $100$ students. $35$ do not play an instrument, so $100-35=65$ play one.',
              'The $80\\%$ is of the players: $10\\%$ of $65$ is $6.5$, so $80\\%$ of $65$ is $8\\times6.5=52$ play the piano.',
              'Guitar only: $65-52=13$ students out of $100$, so $13\\%$.',
              'Percent tree: $20\\%$ of $65\\%$ is $0.2\\times65\\%=13\\%$.'])
    tree = dict(_rn_item(M, 'solve-' + g, 3, 1))
    tree['v'] = dict(tree['v'], values=['100%', '65%', '?'], labels=['Everyone', 'Players', 'Guitar only'])
    _rn_video(M, g, None, [
        (None, [
            "The whole is the survey. So: a hundred students.",
            D('Above "35%" write "35" and next to it "players 65"'),
            "Thirty-five don't play an instrument. So sixty-five do.",
            "Now eighty percent — of whom? Of the players. Of sixty-five.",
            D('Above "80%" write "80% of 65 = 52"'),
            "Ten percent of sixty-five: six and a half. Eighty percent: eight times that — fifty-two play the piano.",
            D('Write "65 − 52 = 13" and circle choice 3'),
            "The rest play only the guitar: sixty-five minus fifty-two — thirteen. We started from a hundred, so that's thirteen percent. Choice three.",
            "Or skip the subtraction: twenty percent of sixty-five — thirteen directly.",
            "Notice what I did: I wrote the numbers right on top of the question. Do exactly that in the exam.",
        ]),
        (None, [
            "Second way: a percent tree. More visual — but more writing.",
            A('The tree path appears: Everyone → Players → Guitar only', tree),
            "Split the survey: thirty-five percent don't play — the other branch, sixty-five percent players.",
            "Now split the players. And here's the classic mistake: every time you go down a branch, that group becomes the new hundred percent.",
            D('Under "Guitar only" write "20% of players"'),
            "Eighty percent piano — so twenty percent guitar only, of the players. Branches always add up to a hundred.",
            D('Write "20% × 65% = 13%" and circle choice 3'),
            "To get a bottom branch, multiply along the path: twenty percent of sixty-five percent. Twenty percent is a fifth — a fifth of sixty-five is thirteen. Thirteen percent.",
            "Visual, yes. But once you've practiced it, plugging in a hundred is faster.",
        ])])

    # ---------- G3 wp23-g058: 760 credits, -75% -> 190  ==>  winter coat 680 credits, -75% -> 170
    g = 'wp23-g058'
    _rn_q(M, g, 'A winter coat originally costs $680$ credits. In a clearance sale, its price is reduced by $75\\%$. What is the new price?',
          ['$510$', '$170$', '$605$', '$160$'], 2, [
              'A $75\\%$ reduction leaves $100\\%-75\\%=25\\%=\\frac14$ of the price.',
              '$680\\div4=170$.'])
    # g058 now comes first in the section. Spoken numbers use the OLD numbering: renumber_guided() maps them
    # (old "three" -> new two for g058, old "two" -> new three for g057).
    _rn_video(M, g, {0: "Advanced percentages — question three.", 1: "Easy one — but there's a smarter route."}, [
        (None, [
            "Start: six eighty. The price drops seventy-five percent.",
            D('Write "10% = 68"'),
            "Ten percent of six eighty: sixty-eight.",
            D('Write "75% = 7·68 + 34 = 476 + 34 = 510"'),
            "Seventy percent: seven times sixty-eight — four seventy-six. Five percent is half of ten: thirty-four. Seventy-five percent: five ten.",
            D('Write "680 − 510 = 170" and circle choice 2'),
            "That's the drop. The new price: six eighty minus five ten — a hundred seventy. Choice two.",
            "Choice one, five ten, is the trap: that's the drop, not the new price.",
        ]),
        (None, [
            "But in percent questions it's often easier to calculate what's LEFT — the complement.",
            D('Write "100% − 75% = 25%"'),
            "A seventy-five percent drop leaves twenty-five percent.",
            D('Write "680 ÷ 4 = 170" and circle choice 2'),
            "Twenty-five percent is a quarter. Halve twice: three forty, one seventy. Same answer — much shorter.",
        ])])

    # ---------- G2 wp23-g057: battery used 72.5% -> 11/40 remains  ==>  ink cartridge used 57.5% -> 17/40
    g = 'wp23-g057'
    _rn_q(M, g, 'A printer cartridge has used $57.5\\%$ of its ink. What fraction of the ink remains?',
          ['$\\frac{23}{40}$', '$\\frac{17}{40}$', '$\\frac{17}{20}$', '$\\frac{2}{5}$'], 2, [
              'Remaining: $100\\%-57.5\\%=42.5\\%$.',
              '$42.5\\%=\\frac{42.5}{100}=\\frac{85}{200}$ (top and bottom times $2$). Reduce by $5$: $\\frac{17}{40}$.'])
    _rn_video(M, g, {0: "Question two.", 1: "The answer choices here hide a shortcut. Watch."}, [
        (None, [
            "Fifty-seven point five percent used. So what's left?",
            D('Write "100 − 57.5 = 42.5%"'),
            "Forty-two and a half percent remains.",
            "But the answers are fractions. So convert — put it over a hundred.",
            D('Write "42.5/100 → ×2 → 85/200"'),
            "First get rid of the decimal point: expand by two. Eighty-five over two hundred.",
            D('Write "÷5 → 17/40" and circle choice 2'),
            "Reduce by five: seventeen fortieths. Choice two.",
        ]),
        (None, [
            "Now psychometric thinking. These choices aren't random.",
            D('Next to choice 3 write "1/20 = 5% → 17/20 = 85%"'),
            "Plenty of you know one twentieth is five percent — a hundred over twenty. So seventeen twentieths is seventeen fives: eighty-five percent. Not ours.",
            D('Next to choice 2 write "half of 85% = 42.5% ✓"'),
            "But seventeen fortieths is exactly HALF of seventeen twentieths. Half of eighty-five: forty-two and a half. That's it.",
            D('Next to choice 1 write "57.5% — the ink USED"'),
            "And choice one, twenty-three fortieths, is fifty-seven and a half percent — the ink that was used. A trap.",
            D('Circle choice 2'),
            "The examiners built these choices so the sharp student gets there fast. Choice two.",
        ])])

    # ---------- G4 wp23-g059: 60 -> 66 -> 72, compare the rises (10% vs 1/11)  ==>  ticket 40 -> 50 -> 60 (25% vs 20%)
    g = 'wp23-g059'
    _rn_q(M, g, 'The price of a cinema ticket rises from $40$ credits to $50$ credits, and later to $60$ credits. How do the two percentage increases compare?',
          ['The increases are equal', 'The second percentage increase is larger', 'The first percentage increase is larger',
           'Their sizes cannot be compared'], 3, [
              'Each rise is $10$ credits.',
              'First rise: $\\frac{10}{40}=\\frac14=25\\%$. Second rise: $\\frac{10}{50}=\\frac15=20\\%$.',
              'Same top, bigger bottom: $\\frac15<\\frac14$. The first percentage increase is larger.'])
    _rn_video(M, g, None, [
        (None, [
            "Forty to fifty, then fifty to sixty. Ten credits each time.",
            D('Write "10/40 = 1/4 = 25%"'),
            "First rise: ten out of forty — a quarter. Twenty-five percent.",
            D('Write "10/50 = 1/5 = 20%"'),
            "Second rise: ten out of fifty — one fifth. Twenty percent.",
            "Bigger or smaller? One cake for four kids — or one cake for five kids? Five kids each get less.",
            D('Write "1/5 < 1/4" and circle choice 3'),
            "Same top, bigger bottom — smaller fraction. The first rise is larger. Choice three.",
        ]),
        ('Method 2 · Add 25% again', [
            "Another way. What if the second rise were twenty-five percent too?",
            D('Write "50 + 12.5 = 62.5 > 60"'),
            "Twenty-five percent of fifty is twelve and a half — you'd reach sixty-two and a half. But it only reached sixty. Less than twenty-five percent.",
            D('Circle choice 3'),
            "Same ten credits — but the whole grew, so the percent shrank. Choice three.",
        ])])

    # ---------- G5 wp23-g060: gives away 25% of points, bonus 30% of the rest -> 2.5% lower
    #            ==>  Noa loses 30% of her coins, prize 40% of the rest -> 2% fewer
    g = 'wp23-g060'
    _rn_q(M, g, 'In a computer game, Noa loses $30\\%$ of her coins. She then wins a prize equal to $40\\%$ of the coins she has left. Compared with the number of coins she had at the start, how many coins does she have now?',
          ['$2\\%$ more', '$2\\%$ fewer', '$10\\%$ more', '$12\\%$ fewer'], 2, [
              'Plug in $100$ coins. Losing $30\\%$ leaves $70$.',
              'The prize is $40\\%$ of $70$: $4\\times7=28$. Final number: $70+28=98$.',
              '$98$ out of $100$: $2\\%$ fewer.',
              'With multipliers: $0.7\\times1.4=0.98$, which is $98\\%$ of the start.'])
    _rn_video(M, g, {1: "She loses some, then wins some back. Up or down?"}, [
        (None, [
            "Let's start with algebra. She has x coins.",
            D('Write "x − 30% of x = 70% of x"'),
            "She loses thirty percent OF x. A percent never stands alone — always attach its whole. And x minus thirty percent of x? Take the complement: seventy percent of x.",
            D('Write "+40% of that → 1.4 × 0.7x = 0.98x"'),
            "Then a prize of forty percent — of what she has LEFT. Keep all of it and add forty percent: one point four times.",
            D('Write "98% of x → 2% fewer" and circle choice 2'),
            "Ninety-eight percent of x. Two percent fewer. Choice two.",
        ]),
        (None, [
            "Now the psychometric way. No numbers given — plug in a hundred. Into the whole: the coins she had at the start.",
            D('Write "100 → 70"'),
            "A hundred coins. Lose thirty: seventy.",
            D('Write "40% of 70 = 28 → 98"'),
            "Prize: forty percent of seventy — not forty coins! Ten percent is seven; forty percent is twenty-eight. Total: ninety-eight.",
            D('Circle choice 2'),
            "Two short of a hundred — two percent fewer. Choice two.",
            "The trap is choice three: forty minus thirty, ten percent more. But the forty percent is of the smaller amount.",
            "Would two hundred work? Two hundred, lose sixty: a hundred forty. Plus forty percent: fifty-six. A hundred ninety-six — four out of two hundred. Still two percent.",
            "So why a hundred? Two reasons. Your final number IS the percent — no converting. And percents of a hundred are the easiest there are.",
        ])])

    # ---------- G7 wp23-g061: Rae 20% more than Sol, Tia 16 2/3% less than Rae -> 1  (+1/5, -1/6)
    #            ==>  Dana 50% more than Omer, Lior 33 1/3% less than Dana -> 1  (+1/2, -1/3)
    g = 'wp23-g061'
    _rn_q(M, g, 'Dana earns $50\\%$ more than Omer. Lior earns $33\\frac13\\%$ less than Dana. What is Lior’s wage divided by Omer’s wage?',
          ['$\\frac32$', '$\\frac76$', '$\\frac23$', '$1$'], 4, [
              'Plug in $100$ for Omer. Dana earns $50\\%$ more: $150$.',
              '$33\\frac13\\%=\\frac13$. Lior earns $\\frac13$ less than Dana: $150-\\frac{150}{3}=150-50=100$.',
              'Lior’s wage divided by Omer’s wage: $100\\div100=1$.'])
    ex = dict(_rn_item(M, 'solve-' + g, 3, 1), t='$+\\frac13$ then $-\\frac14$ $\\qquad$ $+\\frac15$ then $-\\frac16$')  # review: not 1/4, 1/5 (the Hebrew question's +25%, -20%)
    _rn_video(M, g, {1: "Up fifty percent, down thirty-three and a third. Where do we land?"}, [
        (None, [
            "No wages given — plug in a hundred. Into whom? Dana earns more than Omer — so Omer is the whole.",
            D('Write "Omer 100 → Dana 150"'),
            "Omer: a hundred. Dana, fifty percent more: a hundred fifty.",
            D('Write "1/3 of 150 = 50 → Lior 100"'),
            "Thirty-three and a third percent — that's one third, straight from our table. A third of one fifty is fifty. Lior: a hundred.",
            D('Write "100 ÷ 100 = 1" and circle choice 4'),
            "Lior over Omer: a hundred over a hundred. One. Choice four.",
            "The trap is choice two: fifty minus thirty-three and a third, sixteen and two thirds percent more. But the third is taken from Dana's bigger wage.",
        ]),
        (None, [
            "We added fifty percent, removed thirty-three and a third — and landed right back. Coincidence? No.",
            D('Write "+1/2, then −1/3"'),
            "Fifty percent is one half. Thirty-three and a third percent is one third.",
            A('Two examples appear: +1/3 then −1/4, and +1/5 then −1/6', ex),
            "A whole is three thirds. Add a third: four thirds. Now remove a quarter — one of those four thirds — and you're back.",
            "Add a fifth: six fifths. Remove a sixth — one of the six — back again.",
            D('Write "2 halves → 3 halves → remove 1 of 3 → 2 halves" and circle choice 4'),
            "Here: two halves, add one — three. Remove a third — one of the three — back to two halves. Consecutive unit fractions always cancel. Choice four.",
        ])])

    # ---------- G8 wp23-g062: 50% of 15% of x = 12, 22.5% of x? -> 36  ==>  25% of 18% of y = 9, 13.5% of y? -> 27
    g = 'wp23-g062'
    _rn_q(M, g, '$25\\%$ of $18\\%$ of $y$ equals $9$. What is $13.5\\%$ of $y$?',
          ['$18$', '$27$', '$22.5$', '$36$'], 2, [
              '$25\\%$ of $18\\%$ is a quarter of $18\\%$: $4.5\\%$. So $4.5\\%$ of $y$ is $9$.',
              '$13.5\\%=3\\times4.5\\%$, so $13.5\\%$ of $y$ is $3\\times9=27$. There is no need to find $y$.'])
    _rn_video(M, g, None, [
        (None, [
            "Twenty-five percent of eighteen percent of y is nine. \"Of\" means times — so it's all one multiplication.",
            D('Write "1/4 × 9/50 × y = 9"'),
            "Twenty-five percent: a quarter. Eighteen percent: eighteen hundredths — nine fiftieths.",
            D('Write "9y/200 = 9 → y = 200"'),
            "Nine two-hundredths of y is nine. So one two-hundredth of y is one, and y is two hundred.",
            D('Write "13.5% of 200 = 20 + 6 + 1 = 27" and circle choice 2'),
            "Thirteen and a half percent of two hundred: ten percent is twenty, three percent is six, half a percent is one. Twenty-seven. Choice two.",
        ]),
        (None, [
            "Now the trick. a percent of b equals b percent of a — you can swap them. It's one multiplication. Thirty-seven percent of sixty-four is sixty-four percent of thirty-seven.",
            "So twenty-five percent of eighteen: just a quarter of eighteen. Four and a half.",
            D('Write "4.5% of y = 9"'),
            "Four and a half percent of y is nine.",
            D('Write "13.5% = 3 × 4.5% → 3 × 9 = 27" and circle choice 2'),
            "Thirteen and a half is exactly three times four and a half. So three times nine: twenty-seven. We never even needed y.",
        ])])

    # ---------- G9 wp23-g063: not equal to 15% of 4x (10% of 6x, 60% of x, 5% of 12x, 30% of 4x)
    #            ==>  not equal to 16% of 5y (40% of 2y, 8% of 10y, 32% of 5y, 20% of 4y)
    g = 'wp23-g063'
    _rn_q(M, g, 'For $y>0$, which expression is not equal to $16\\%$ of $5y$?',
          ['$40\\%$ of $2y$', '$8\\%$ of $10y$', '$32\\%$ of $5y$', '$20\\%$ of $4y$'], 3, [
              '$16\\%$ of $5y=\\frac{16\\cdot5y}{100}=\\frac{80y}{100}$.',
              'Every choice is also over $100$, so compare the tops: $40\\cdot2y=80y$, $8\\cdot10y=80y$, $32\\cdot5y=160y$, $20\\cdot4y=80y$.',
              'Since $y>0$, $160y\\ne80y$. Only $32\\%$ of $5y$ is not equal.'])
    _rn_video(M, g, None, [
        (None, [
            "Which is NOT equal to sixteen percent of five y?",
            D('Write "16/100 × 5y = 80y/100"'),
            "Sixteen over a hundred, times five y: eighty y over a hundred.",
            "Every choice will also be something over a hundred. So don't reduce — just compare the tops.",
            D('Next to choices 1, 2 and 4 write "80y"'),
            "Forty times two y: eighty y. Eight times ten y: eighty y. Twenty times four y: eighty y. All equal — cross them out.",
            D('Next to choice 3 write "160y" and circle choice 3'),
            "Thirty-two times five y: a hundred sixty y. Not equal. Choice three.",
        ]),
        (None, [
            "Or think in ratios. Twenty percent of a hundred is twenty. Double the whole to two hundred — you need half the percent, ten, to still get twenty.",
            D('Write "percent × k  ⟺  whole ÷ k"'),
            "Percent up, whole down by the same factor — same result.",
            D('Next to choice 1 write "percent × 5/2,  whole × 2/5"'),
            "Choice one: forty percent is five halves of sixteen. Two y is two fifths of five y. Five halves times two fifths is one. Balanced.",
            "Choice two: the percent is halved, the whole is doubled. Balanced. Choice four: the percent times five quarters, the whole times four fifths. Balanced.",
            D('Circle choice 3'),
            "Choice three: the percent doubled — and the whole stayed five y. Nothing balances it. Choice three.",
        ])])

    # ---------- G11 wp23-g064: 80% Monday, rest Tuesday, difference 36 planks -> Tuesday 12
    #            ==>  70% to a market, rest to a juice factory, difference 48 kg -> factory 36
    g = 'wp23-g064'
    _rn_q(M, g, 'A farmer sells $70\\%$ of his apples at a market and all the rest to a juice factory. The market gets $48$ kg more apples than the factory. How many kilograms of apples does the factory get?',
          ['$24$', '$36$', '$48$', '$84$'], 2, [
              'Market: $70\\%$. Factory: the rest, $100\\%-70\\%=30\\%$.',
              'The difference is $70\\%-30\\%=40\\%$, and it equals $48$ kg.',
              '$40\\%\\to48$, so $10\\%\\to48\\div4=12$ and $30\\%\\to3\\times12=36$ kg.'])
    tab = dict(_rn_item(M, 'solve-' + g, 2, 1))
    tab['v'] = dict(tab['v'], headers=['Percent', 'Kilograms'], rows=[['40%', '48'], ['30%', '?']])
    _rn_video(M, g, {1: "The difference is the key — not the factory's amount."}, [
        (None, [
            "Market: seventy percent. The factory: the rest — thirty percent.",
            D('Write "70% − 30% = 40% ↔ 48"'),
            "The difference is forty percent — and that difference is forty-eight kilograms.",
            A('A ratio table appears: 40% → 48, 30% → ?', tab),
            "Put it in the ratio table.",
            D('Write "30 × 48 ÷ 40 = 36" and circle choice 2'),
            "Multiply the diagonal, divide by what's left: thirty times forty-eight, over forty. Thirty-six. Choice two.",
            "Choice three, forty-eight, is the trap: that's the difference, not the factory's apples.",
        ]),
        (None, [
            "Faster. Forty percent to thirty percent isn't one easy step. So take a middle step: forty percent down to ten percent — divide by four.",
            D('Write "48 ÷ 4 = 12 → 12 × 3 = 36" and circle choice 2'),
            "Forty-eight divided by four: twelve. That's ten percent. Thirty percent is three times that: thirty-six. Done.",
            "The trick: when the ratio isn't obvious, take a middle step — divide by ten, or by the easy number — until it is.",
        ])])

    # ---------- G12 wp23-g065: each hour 20% removed, 128 L after two hours -> 200
    #            ==>  each day 10% of a rain barrel used, 243 L after two days -> 300
    g = 'wp23-g065'
    _rn_q(M, g, 'At the end of each day, $10\\%$ of the water then in a rain barrel is used to water the garden. After two days, $243$ liters remain. How many liters were in the barrel at the start?',
          ['$270$', '$324$', '$300$', '$280$'], 3, [
              'Each day $10\\%$ is used, so $90\\%$ stays: multiply by $0.9$.',
              'After two days: $0.9\\times0.9=0.81$, so $81\\%$ of the start remains.',
              '$81\\%=243$ liters, so $1\\%=3$ liters and $100\\%=300$ liters.',
              'Check: $300\\to270\\to243$ ✓.'])
    chain = dict(_rn_item(M, 'solve-' + g, 2, 1))
    chain['v'] = dict(chain['v'], labels=['Start', 'After 1 day', 'After 2 days'])
    _rn_video(M, g, {0: "A barrel that loses water.", 1: "Water is used every day. Go back two days."}, [
        (None, [
            "Ten percent is used every day. After two days: two hundred forty-three liters. How much at the start?",
            "Plug in a hundred — but careful. We already have a real number here, so we can't say \"a hundred liters\". We plug in a hundred PERCENT.",
            A('A chain appears: Start → After 1 day → After 2 days', chain),
            D('Write "90%" in the second box'),
            "Ten percent used: ninety percent left.",
            D('Write "81%" in the third box'),
            "Now ten percent of what's in the barrel NOW — keep ninety percent of ninety: eighty-one percent. With multipliers: zero point nine times zero point nine.",
            D('Write "81% = 243 L → 1% = 3 L → 100% = 300 L" and circle choice 3'),
            "Eighty-one percent is two hundred forty-three liters — so every percent is three liters. A hundred percent: three hundred. Choice three.",
            "Choice one, two seventy, goes back only one day.",
        ]),
        (None, [
            "Or test the choices. Which first? The roundest one — three hundred.",
            D('Write "300 → 270 → 243 ✓" and circle choice 3'),
            "Three hundred, keep ninety percent: two hundred seventy. Keep ninety percent again: two hundred forty-three. Bang on. Choice three.",
            "The round answer isn't always right — but it's usually the smartest one to test first.",
        ])])


def rn_order(M):
    """g058 (75% off - the easiest) moves before g057 (fraction left). renumber_guided() renumbers the titles."""
    M.move('wp23-g058', ADV, before='wp23-g057')
    M.move('solve-wp23-g058', ADV, after='wp23-g058')


def rn_lessons(M):
    """Hebrew-derived lesson examples get new numbers (the English-made slides keep theirs).
    2026-10-06 review: (10+x)% of 60 = (60-x)% of 40 -> (5+x) / (70-x) (the Hebrew had (10+x)% of 80 = (60-x)% of 60), and
    15% -> 54 => 35% -> 25% (the Hebrew asked 14% -> 56 => 35%)."""
    # ---- "Calculating Percentages" (wp-052) ----
    _rn_slide(M, L1, 2, {
        '$37\\%=\\frac{37}{100}$': '$29\\%=\\frac{29}{100}$',
        "'37% = 37/100' appears": "'29% = 29/100' appears",
        'Thirty-seven percent: thirty-seven hundredths.': 'Twenty-nine percent: twenty-nine hundredths.',
        "And it's not a count until you know the whole. Thirty-seven percent of a hundred tickets is thirty-seven. Of two hundred tickets — seventy-four.":
            "And it's not a count until you know the whole. Twenty-nine percent of a hundred tickets is twenty-nine. Of two hundred tickets — fifty-eight.",
    })
    _rn_slide(M, L1, 3, {
        '$20\\%=\\frac{20}{100}$': '$30\\%=\\frac{30}{100}$',
        "'20% = 20/100' appears": "'30% = 30/100' appears",
        'Write "= 1/5"': 'Write "= 3/10"',
        'Twenty percent: twenty hundredths — one fifth.': 'Thirty percent: thirty hundredths — three tenths.',
        '$\\frac34$': '$\\frac{11}{25}$',
        '3/4 appears': '11/25 appears',
        'Write "×25" on top and bottom, then "= 75/100 = 75%"': 'Write "×4" on top and bottom, then "= 44/100 = 44%"',
        'Four times twenty-five is a hundred. Three times twenty-five: seventy-five. Seventy-five percent.':
            'Twenty-five times four is a hundred. Eleven times four: forty-four. Forty-four percent.',
        '$\\frac25$': '$\\frac7{50}$',
        '2/5 appears': '7/50 appears',
        'Write "×20" on top and bottom, then "= 40/100 = 40%"': 'Write "×2" on top and bottom, then "= 14/100 = 14%"',
        'Five times twenty: a hundred. Two times twenty: forty percent.': 'Fifty times two: a hundred. Seven times two: fourteen percent.',
    })
    _rn_slide(M, L1, 6, {
        '$65\\%$ of $80$ = ?': '$45\\%$ of $80$ = ?',
        'Write "= 65/100 × 80"': 'Write "= 45/100 × 80"',
        'Sixty-five over a hundred, times eighty.': 'Forty-five over a hundred, times eighty.',
        'Write "= 65 × 4/5 = 52"': 'Write "= 45 × 4/5 = 36"',
        'Cancel twenty: four fifths of sixty-five. Fifty-two.': 'Cancel twenty: four fifths of forty-five. Thirty-six.',
        '$A\\%$ of $60$ is $21$. $\\ A=?$': '$A\\%$ of $75$ is $21$. $\\ A=?$',
        "'A% of 60 is 21. A = ?' appears": "'A% of 75 is 21. A = ?' appears",
        'Write "A/100 × 60 = 21 → 60A = 2100 → A = 35"': 'Write "A/100 × 75 = 21 → 75A = 2100 → A = 28"',
        'A over a hundred, times sixty, is twenty-one. Multiply by a hundred: sixty A is twenty-one hundred. A is thirty-five.':
            'A over a hundred, times seventy-five, is twenty-one. Multiply by a hundred: seventy-five A is twenty-one hundred. A is twenty-eight.',
        '$(20+x)\\%$ of $60$ = $(80-x)\\%$ of $40$': '$(5+x)\\%$ of $60$ = $(70-x)\\%$ of $40$',
        "'(20+x)% of 60 = (80−x)% of 40' appears": "'(5+x)% of 60 = (70−x)% of 40' appears",
        'Write "(20+x)·60 = (80−x)·40"': 'Write "(5+x)·60 = (70−x)·40"',
        'Write "÷20: 3(20+x) = 2(80−x) → 5x = 100 → x = 20"': 'Write "÷20: 3(5+x) = 2(70−x) → 5x = 125 → x = 25"',
        'Cancel twenty: three times twenty plus x equals two times eighty minus x. Sixty plus three x equals a hundred sixty minus two x. Five x is a hundred. x is twenty.':
            'Cancel twenty: three times five plus x equals two times seventy minus x. Fifteen plus three x equals a hundred forty minus two x. Five x is a hundred twenty-five. x is twenty-five.',
    })
    _rn_slide(M, L1, 7, {
        '65%': '45%', '42': '54', '35%': '25%',      # table cells (exact cells only)
        'A ratio table appears: 100% → 80, 65% → ?': 'A ratio table appears: 100% → 80, 45% → ?',
        'Draw the diagonal 65 × 80, then write "÷ 100 = 52"': 'Draw the diagonal 45 × 80, then write "÷ 100 = 36"',
        'Multiply across the diagonal, divide by what\'s left. Sixty-five times eighty, over a hundred: fifty-two.':
            'Multiply across the diagonal, divide by what\'s left. Forty-five times eighty, over a hundred: thirty-six.',
        'A second table appears: 15% → 42, 35% → ?': 'A second table appears: 15% → 54, 25% → ?',
        "Now the real power. Fifteen percent of some number is forty-two. What's thirty-five percent of it?":
            "Now the real power. Fifteen percent of some number is fifty-four. What's twenty-five percent of it?",
        'Write "÷3 → 5% = 14", then "×7 → 35% = 98"': 'Write "÷3 → 5% = 18", then "×5 → 25% = 90"',
        'Divide both sides by three: five percent is fourteen. Seven of those: ninety-eight.':
            'Divide both sides by three: five percent is eighteen. Five of those: ninety.',
    })
    _rn_slide(M, L1, 8, {
        '$10\\%$ of $230=23$': '$10\\%$ of $270=27$', '$10\\%$ of $66=6.6$': '$10\\%$ of $48=4.8$',
        "'10% of 230 = 23' and '10% of 66 = 6.6' appear": "'10% of 270 = 27' and '10% of 48 = 4.8' appear",
        'Ten percent of two thirty: twenty-three. Ten percent of sixty-six: six point six — the point just hops one place left.':
            'Ten percent of two seventy: twenty-seven. Ten percent of forty-eight: four point eight — the point just hops one place left.',
        '$30\\%$ of $230$': '$30\\%$ of $270$', "'30% of 230' appears": "'30% of 270' appears",
        'Write "= 3 × 23 = 69"': 'Write "= 3 × 27 = 81"',
        'Thirty percent? Three ten-percent chunks: sixty-nine.': 'Thirty percent? Three ten-percent chunks: eighty-one.',
        '$35\\%$ of $230$': '$35\\%$ of $270$', "'35% of 230' appears": "'35% of 270' appears",
        'Write "30% → 69,  5% → 11.5,  total 80.5"': 'Write "30% → 81,  5% → 13.5,  total 94.5"',
        'Thirty-five percent: split it. Thirty percent is sixty-nine. Five percent is half of ten percent: eleven and a half. Together: eighty and a half.':
            'Thirty-five percent: split it. Thirty percent is eighty-one. Five percent is half of ten percent: thirteen and a half. Together: ninety-four and a half.',
    })
    _rn_slide(M, L1, 9, {
        '$16\\%$ of $25$ = $25\\%$ of $16$': '$36\\%$ of $25$ = $25\\%$ of $36$',
        "'16% of 25 = 25% of 16' appears": "'36% of 25 = 25% of 36' appears",
        'Write "= 4"': 'Write "= 9"',
        'Swap them: a percent of b equals b percent of a. Sixteen percent of twenty-five equals twenty-five percent of sixteen — a quarter of sixteen. Four.':
            'Swap them: a percent of b equals b percent of a. Thirty-six percent of twenty-five equals twenty-five percent of thirty-six — a quarter of thirty-six. Nine.',
        '$30\\%$ of the whole is $54$': '$30\\%$ of the whole is $63$',
        "'30% of the whole is 54' appears": "'30% of the whole is 63' appears",
        'Write "10% → 18,  100% → 180"': 'Write "10% → 21,  100% → 210"',
        'Whole missing? Thirty percent is fifty-four, so ten percent is eighteen — and the whole is a hundred eighty.':
            'Whole missing? Thirty percent is sixty-three, so ten percent is twenty-one — and the whole is two hundred ten.',
        'From $80$ to $100$': 'From $50$ to $60$', "'From 80 to 100' appears": "'From 50 to 60' appears",
        'Write "20/80 × 100 = 25%"': 'Write "10/50 × 100 = 20%"',
        'Eighty up to a hundred: the change is twenty. Twenty out of the original eighty — a quarter. Twenty-five percent.':
            'Fifty up to sixty: the change is ten. Ten out of the original fifty — a fifth. Twenty percent.',
    })

    # ---- "Percent of a Percent" (wp-053) ----
    _rn_slide(M, L2, 2, {
        'A price rises $25\\%$, then falls by $20\\%$ of the new price. What is the overall change?':
            'A price rises $80\\%$, then falls by $25\\%$ of the new price. What is the overall change?',
        'Write "→ 125"': 'Write "→ 180"',
        'Up twenty-five percent: a hundred twenty-five.': 'Up eighty percent: a hundred eighty.',
        'Now careful. The twenty percent is of the NEW price. The hundred is history — the whole is now a hundred twenty-five.':
            'Now careful. The twenty-five percent is of the NEW price. The hundred is history — the whole is now a hundred eighty.',
        'Write "20% of 125 = 25 → 100"': 'Write "25% of 180 = 45 → 135"',
        'Twenty percent of one twenty-five: twenty-five. Back down to a hundred.':
            'Twenty-five percent of one eighty — a quarter: forty-five. Down to a hundred thirty-five.',
        'Write "change: 0%"': 'Write "change: +35%"',
        'Back where we started! Not because twenty equals twenty-five — because the second percent sits on a bigger base.':
            'Up thirty-five percent — not eighty minus twenty-five, fifty-five! Because the second percent sits on a bigger base.',
    })
    _rn_slide(M, L2, 3, {
        'A stock of material loses $25\\%$, then $20\\%$ of what remains. What percent was lost in total?':
            'A stock of material loses $30\\%$, then $20\\%$ of what remains. What percent was lost in total?',
        'After 25% loss': 'After 30% loss',
        'A chain of three boxes appears: Start → After 25% loss → After 20% more':
            'A chain of three boxes appears: Start → After 30% loss → After 20% more',
        'Write "75" in the second box': 'Write "70" in the second box',
        'Lose twenty-five percent: seventy-five left.': 'Lose thirty percent: seventy left.',
        'Write "60" in the third box': 'Write "56" in the third box',
        'Twenty percent of what remains — of seventy-five. Ten percent is seven and a half; twenty percent is fifteen. Sixty left.':
            'Twenty percent of what remains — of seventy. Ten percent is seven; twenty percent is fourteen. Fifty-six left.',
        'Under the chain write "lost 40%"': 'Under the chain write "lost 44%"',
        'A hundred down to sixty: we lost forty. Forty percent.': 'A hundred down to fifty-six: we lost forty-four. Forty-four percent.',
        'Not forty-five! The second twenty percent came out of a smaller amount.': 'Not fifty! The second twenty percent came out of a smaller amount.',
        'Shortcut: think about what STAYS. Lose twenty-five percent — keep seventy-five. Lose twenty percent of that — keep eighty percent of seventy-five: sixty. Straight there.':
            'Shortcut: think about what STAYS. Lose thirty percent — keep seventy. Lose twenty percent of that — keep eighty percent of seventy: fifty-six. Straight there.',
    })
    _rn_slide(M, L2, 4, {
        '$-25\\%$, then $-20\\%$: $\\ 0.75\\times0.8=0.6$': '$-30\\%$, then $-20\\%$: $\\ 0.7\\times0.8=0.56$',
        "'−25%, then −20%: 0.75 × 0.8 = 0.6' appears": "'−30%, then −20%: 0.7 × 0.8 = 0.56' appears",
        'Write "→ keep 60%, lost 40%"': 'Write "→ keep 56%, lost 44%"',
        'The two losses from before: zero point seven five times zero point eight — zero point six. We keep sixty percent, so we lost forty. Same answer, one line.':
            'The two losses from before: zero point seven times zero point eight — zero point five six. We keep fifty-six percent, so we lost forty-four. Same answer, one line.',
    })
    _rn_slide(M, L2, 5, {
        'Write "+25, −20:  25 − 20 − 5 = 0"': 'Write "+80, −25:  80 − 25 − 20 = 35"',
        'Up twenty-five, down twenty. Twenty-five minus twenty is five. Twenty-five times minus twenty, over a hundred, is minus five. Five minus five: zero. No change — exactly what we got at the start.':
            'Up eighty, down twenty-five. Eighty minus twenty-five is fifty-five. Eighty times minus twenty-five, over a hundred, is minus twenty. Fifty-five minus twenty: thirty-five. Up thirty-five percent — exactly what we got at the start.',
    })
    _rn_slide(M, L2, 6, {
        "Lena earns $25\\%$ more than Noor. Ari earns $40\\%$ less than Lena. By what percent is Ari's pay lower than Noor's?":
            "Tal earns $60\\%$ more than Ben. Eli earns $45\\%$ less than Tal. By what percent is Eli's pay lower than Ben's?",
        'But this question has several "thans". Lena than Noor. Ari than Lena. Ari than Noor.':
            'But this question has several "thans". Tal than Ben. Eli than Tal. Eli than Ben.',
        'Underline "than Noor\'s" in the last sentence': 'Underline "than Ben\'s" in the last sentence',
        'The one that decides is the "than" in the QUESTION itself — lower than Noor\'s. So Noor is our hundred.':
            'The one that decides is the "than" in the QUESTION itself — lower than Ben\'s. So Ben is our hundred.',
        'Write "Noor 100 → Lena 125 → Ari 75"': 'Write "Ben 100 → Tal 160 → Eli 88"',
        'Noor: a hundred. Lena, twenty-five percent more: a hundred twenty-five. Ari, forty percent less than Lena: keep sixty percent of one twenty-five — seventy-five.':
            'Ben: a hundred. Tal, sixty percent more: a hundred sixty. Eli, forty-five percent less than Tal: keep fifty-five percent of one sixty — eighty-eight.',
        'Write "25% lower"': 'Write "12% lower"',
        'Seventy-five against a hundred: twenty-five percent lower.': 'Eighty-eight against a hundred: twelve percent lower. Not fifteen percent higher!',
    })
    _rn_slide(M, L2, 7, {
        'Rise $20\\%$, then add a fixed $15$ credits': 'Rise $10\\%$, then add a fixed $20$ credits',
        "'Rise 20%, then add a fixed 15 credits' appears": "'Rise 10%, then add a fixed 20 credits' appears",
        'Write "100 → 135 (35%)   200 → 255 (27.5%)"': 'Write "100 → 130 (30%)   200 → 240 (20%)"',
        'Add a fixed fifteen credits, and the answer changes with the real starting price. From a hundred: thirty-five percent up. From two hundred: twenty-seven and a half.':
            'Add a fixed twenty credits, and the answer changes with the real starting price. From a hundred: thirty percent up. From two hundred: twenty.',
    })
    _rn_slide(M, L2, 8, {
        'After a $20\\%$ loss, $96$ remain. Original?': 'After a $30\\%$ loss, $91$ remain. Original?',
        "'After a 20% loss, 96 remain. Original?' appears": "'After a 30% loss, 91 remain. Original?' appears",
        "Going backwards? Ninety-six isn't the whole — it's what STAYED.": "Going backwards? Ninety-one isn't the whole — it's what STAYED.",
        'Write "96 = 80% → 10% = 12 → 100% = 120"': 'Write "91 = 70% → 10% = 13 → 100% = 130"',
        'Ninety-six is eighty percent. Ten percent is twelve. The original: a hundred twenty.':
            'Ninety-one is seventy percent. Ten percent is thirteen. The original: a hundred thirty.',
        "Don't just add twenty percent of ninety-six — that twenty percent was taken from the original, not from ninety-six.":
            "Don't just add thirty percent of ninety-one — that thirty percent was taken from the original, not from ninety-one.",
        'With a multiplier: ninety-six is the start times zero point eight. So the start is ninety-six divided by zero point eight — a hundred twenty.':
            'With a multiplier: ninety-one is the start times zero point seven. So the start is ninety-one divided by zero point seven — a hundred thirty.',
    })
    _rn_slide(M, L2, 10, {   # same fixed amount as "When 100 fails"
        "The limit: every step must be a percent or a multiple. If a fixed amount is added — plus fifteen credits — it's not one multiplier. Use real numbers.":
            "The limit: every step must be a percent or a multiple. If a fixed amount is added — plus twenty credits — it's not one multiplier. Use real numbers.",
    })


def rn_cards(M):
    c = M.card(CARD)
    new = {
        'Percent equation': '$45\\%$ of $80=\\frac{45}{100}\\cdot80=36$',
        'Equal ratios (triangle value)': '$15\\%\\to54 \\Rightarrow 25\\%\\to90$',
        '$10\\%$ chunks': '$35\\%$ of $270=81+13.5$',
        'Change in percent': 'change $\\div$ original $\\times100$: $50\\to60$ is $\\frac{10}{50}=20\\%$',
        'Complement': 'drop $35\\%$ → keep $65\\%$',
        'Plug in $100$': '$100\\to180\\to135$',
        'Percent tree': '$70\\%\\times40\\%=28\\%$',
    }
    rows = c['tables'][1]['rows']; done = set()
    for r in rows:
        if r[0] in new: r[2] = new[r[0]]; done.add(r[0])
    assert done == set(new), set(new) - done
    tips = {
        'Each new percent sits on the NEW amount: $+25\\%$ then $-20\\%$ returns to the start.':
            'Each new percent sits on the NEW amount: $+80\\%$ then $-25\\%$ gives $+35\\%$, not $+55\\%$.',
        'Adding $\\frac1n$ and then removing $\\frac1{n+1}$ brings you back: $+20\\%$, $-16\\frac23\\%$.':
            'Adding $\\frac1n$ and then removing $\\frac1{n+1}$ brings you back: $+33\\frac13\\%$, $-25\\%$.',
        'Any two changes $a\\%$ and $b\\%$: $a+b+\\frac{ab}{100}$ (a fall is negative). $+25$, $-20$ → $25-20-5=0$.':
            'Any two changes $a\\%$ and $b\\%$: $a+b+\\frac{ab}{100}$ (a fall is negative). $+80$, $-25$ → $80-25-20=35$.',
    }
    assert all(t in c['tips'] for t in tips), [t for t in tips if t not in c['tips']]
    c['tips'] = [tips.get(t, t) for t in c['tips']]


def rn_practice_questions(M):
    # p01: 75% of 8/9 -> 2/3  ==>  60% of 5/12 -> 1/4
    _rn_q(M, 'wp23-p01', 'What is $60\\%$ of $\\frac{5}{12}$?', ['$\\frac13$', '$\\frac35$', '$\\frac14$', '$\\frac7{12}$'], 3, [
        '$60\\%=\\frac35$.', '$\\frac35\\times\\frac5{12}=\\frac{3\\cdot5}{5\\cdot12}=\\frac{15}{60}=\\frac14$.'])
    # p02: 80 beads, half white, 65% of the rest purple -> 14 orange  ==>  60 pens, a third blue, 45% of the rest black -> 22 red
    _rn_q(M, 'wp23-p02', 'A box holds $60$ pens, each blue, black, or red. A third of them are blue. Of the pens that are not blue, $45\\%$ are black. How many pens are red?',
          ['$18$', '$33$', '$22$', '$27$'], 3, [
              'Blue: a third of $60$ is $20$. Not blue: $60-20=40$.',
              'Black is $45\\%$ of them, so red is $100\\%-45\\%=55\\%$ of $40$.',
              '$10\\%$ of $40$ is $4$, so $55\\%$ of $40$ is $5\\times4+2=22$.'])
    # p03: 96 credits, +50% a year, first not whole after review 6  ==>  stamp 112 credits, first not whole after year 5
    _rn_q(M, 'wp23-p03', 'A rare stamp is worth $112$ credits. Every year, its value rises by $50\\%$. After which year is its value first not a whole number of credits?',
          ['$4$', '$6$', '$5$', '$7$'], 3, [
              'A $50\\%$ rise multiplies the value by $1.5=\\frac32$: times $3$, divided by $2$.',
              'Each year uses up one factor $2$. $112=2^4\\cdot7$ has four factors $2$.',
              'So years 1 to 4 give whole numbers: $112\\to168\\to252\\to378\\to567$, and $567=3^4\\cdot7$ has no factor $2$ left.',
              'Year 5: $567\\times1.5=850.5$. The first value that is not a whole number comes after year 5.'])
    # p04: 40% of 25% of x = 9, 3/10 x? -> 27  ==>  80% of 12.5% of x = 8, 7/10 x? -> 56
    _rn_q(M, 'wp23-p04', '$80\\%$ of $12.5\\%$ of $x$ equals $8$. What is $\\frac7{10}x$?', ['$16$', '$28$', '$80$', '$56$'], 4, [
        '$80\\%$ of $12.5\\%$: $\\frac45\\times\\frac18=\\frac1{10}$. So $\\frac1{10}x=8$.',
        '$\\frac7{10}x=7\\times8=56$.'])
    # p05: hits 40%, misses 18 -> 30  ==>  scores on 65%, misses 14 -> 40
    _rn_q(M, 'wp23-p05', 'A basketball player scores on $65\\%$ of his shots. He misses $14$ shots. How many shots does he take?',
          ['$28$', '$35$', '$40$', '$54$'], 3, [
              'He scores on $65\\%$, so he misses $100\\%-65\\%=35\\%$ of his shots.',
              '$35\\%=14$ shots, so $5\\%=2$ and $100\\%=40$ shots.'])
    # p06: 15 juniors, 25%..75% -> at most 45 seniors  ==>  12 sopranos, 20%..60% -> at most 48 others
    _rn_q(M, 'wp23-p06', 'A choir has $12$ sopranos. The sopranos make up at least $20\\%$ and at most $60\\%$ of the choir. What is the greatest possible number of other singers in the choir?',
          ['$8$', '$60$', '$36$', '$48$'], 4, [
              'The more singers the choir has, the smaller the sopranos’ share. So use the smallest share: $20\\%$.',
              '$12$ sopranos $=20\\%=\\frac15$ of the choir, so the choir has $5\\times12=60$ singers.',
              'Other singers: $60-12=48$.'])
    # p07: +50%, gives 20% of the new amount -> 120%  ==>  Dina's salary +40%, saves 25% of the new salary -> 105%
    _rn_q(M, 'wp23-p07', 'Dina’s monthly salary rises by $40\\%$. She then puts $25\\%$ of the new salary into savings. The amount left is what percentage of her original salary?',
          ['$115\\%$', '$110\\%$', '$105\\%$', '$100\\%$'], 3, [
              'Plug in $100$. A $40\\%$ rise: $140$.',
              '$25\\%$ of $140$ is $35$. She has $140-35=105$ left.',
              '$105$ out of the original $100$: $105\\%$. With multipliers: $1.4\\times0.75=1.05$.'])
    # p08: a+b=200, a=b+60 -> b is 35%  ==>  x+y=250, x=y+40 -> y is 42%
    _rn_q(M, 'wp23-p08', 'Given:\n$\\begin{cases} x+y=250 \\\\ x=y+40 \\end{cases}$\nWhat percentage of $x+y$ is $y$?',
          ['$58\\%$', '$42\\%$', '$16\\%$', '$40\\%$'], 2, [
              'Put $x=y+40$ into the sum: $(y+40)+y=250$, so $2y=210$ and $y=105$.',
              '$\\frac{105}{250}=\\frac{42}{100}=42\\%$.'])
    # p09: 15% of 3x is 18 -> 45% of x  ==>  35% of 2x is 21 -> 70% of x
    _rn_q(M, 'wp23-p09', '$35\\%$ of $2x$ is $21$. What percentage of $x$ is $21$?', ['$35\\%$', '$70\\%$', '$17.5\\%$', '$105\\%$'], 2, [
        '$35\\%$ of $2x=\\frac{35\\cdot2x}{100}=\\frac{70x}{100}$, which is $70\\%$ of $x$.',
        'So $21$ is $70\\%$ of $x$. There is no need to find $x$.'])
    # p10: +10% two years, 63 above -> 300  ==>  painting +20% two years, 220 above -> 500
    _rn_q(M, 'wp23-p10', 'A painting’s value rises by $20\\%$ in each of two years. After the second year, its value is $220$ credits above its original value. What was its original value?',
          ['$1100$', '$550$', '$720$', '$500$'], 4, [
              'Two $20\\%$ rises: multiply by $1.2\\times1.2=1.44$. In total the value rises by $44\\%$.',
              '$44\\%$ of the original value is $220$, so $1\\%=5$ and $100\\%=500$.',
              'Check: $500\\to600\\to720$, and $720-500=220$ ✓.'])
    # p11: laptop owners 3 to 1, 40% touch-screen -> 70% not  ==>  car owners 3 to 2, 30% electric -> 82% not
    _rn_q(M, 'wp23-p11', 'In a town, car owners outnumber non-owners by $3$ to $2$. Of the car owners, $30\\%$ own an electric car. What percentage of all the residents do not own an electric car?',
          ['$70\\%$', '$40\\%$', '$82\\%$', '$60\\%$'], 3, [
              'Owners to non-owners is $3$ to $2$, so owners are $\\frac35=60\\%$ of the residents.',
              'Electric-car owners: $30\\%$ of $60\\%$ is $0.3\\times60\\%=18\\%$ of all residents.',
              'The rest: $100\\%-18\\%=82\\%$.'])
    # p12: 75% certified, 18 first aid only, coaching = none -> 36  ==>  70% team sport, 24 basketball only, football = none -> 60
    _rn_q(M, 'wp23-p12', '$70\\%$ of the members of a sports club play a team sport. Twenty-four members play only basketball, and every other team-sport player plays only football. The number who play football equals the number who play no team sport. How many members does the club have?',
          ['$80$', '$40$', '$60$', '$48$'], 3, [
              'No team sport: $100\\%-70\\%=30\\%$.',
              'Football equals no team sport: $30\\%$. Basketball: $70\\%-30\\%=40\\%$.',
              '$40\\%=24$ members, so $10\\%=6$ and $100\\%=60$.'])
    # p13: +40%, fall to +12% -> 20%  ==>  laptop +60%, fall to +20% -> 25%
    _rn_q(M, 'wp23-p13', 'After a price rise, a laptop costs $60\\%$ more than its original price. By what percentage must the new price fall so that it is only $20\\%$ above the original price?',
          ['$40\\%$', '$25\\%$', '$20\\%$', '$37.5\\%$'], 2, [
              'Plug in $100$ for the original price. New price: $160$. Target: $120$.',
              'The drop is $160-120=40$. Measure it against the current price, $160$: $\\frac{40}{160}=\\frac14=25\\%$.',
              'Method 2 · Arrow map: original → new price is $\\times1.6$, and original → target is $\\times1.2$. From the new price to the target, go against the first arrow and along the second: $1.2\\div1.6=0.75$. The price drops to $75\\%$: a $25\\%$ fall.'])
    # p14: same balance, p% = 90, q% = 150 -> 5p = 3q  ==>  same shopping budget, a% = 120, b% = 280 -> 7a = 3b
    _rn_q(M, 'wp23-p14', 'Of the same shopping budget, $a\\%$ is $120$ credits and $b\\%$ is $280$ credits. Which of the following is necessarily true?',
          ['$3a=7b$', '$b<a$', '$a=b-160$', '$7a=3b$'], 4, [
              'Percents of the same whole are in the same ratio as their amounts: $\\frac ab=\\frac{120}{280}=\\frac37$.',
              'Cross-multiply: $7a=3b$.',
              'Method 2 · Flip rule, same whole → keep: both percents are of the same budget, therefore the bigger percent gives the bigger amount and the order stays. The ratio $a:b=120:280=3:7$, that is, $7a=3b$. (Flipping it, $3a=7b$, is the trap.)'])
    # p15: equal blue/yellow, half used, 14 blue + 6 yellow left -> 70% of the used were yellow
    #      ==>  equal red/green marbles, half taken out, 9 red + 15 green left -> 62.5% of the taken were red
    _rn_q(M, 'wp23-p15', 'A bag begins with equal numbers of red and green marbles. After half of all the marbles are taken out, $9$ red and $15$ green marbles remain. What percentage of the marbles taken out were red?',
          ['$37.5\\%$', '$60\\%$', '$62.5\\%$', '$75\\%$'], 3, [
              '$9+15=24$ marbles remain. That is half, so $24$ were taken out and there were $48$ at the start: $24$ of each color.',
              'Red taken out: $24-9=15$. Out of the $24$ taken out: $\\frac{15}{24}=\\frac58=62.5\\%$.'])
    # p16: N visitors, b audio guides -> b^2/N  ==>  T students, s in a science club -> s^2/T (choices reordered)
    _rn_q(M, 'wp23-p16', 'A school has $T$ students, and $s$ of them joined a science club. The fraction of club members who chose robotics equals the fraction of all the students who joined the club. How many students chose robotics?',
          ['$\\frac{s^2}{T}$', '$\\frac{T^2}{s}$', '$T-s$', '$\\frac{s}{T^2}$'], 1, [
              'Club members are $\\frac sT$ of all the students.',
              'The same fraction of the $s$ club members chose robotics: $s\\times\\frac sT=\\frac{s^2}{T}$.',
              'Check with numbers: $T=25$ and $s=10$. $\\frac{10}{25}$ of $10$ is $4$, and $\\frac{s^2}{T}=\\frac{100}{25}=4$ ✓.'])
    # p17: 240 -> 174, a in 25..30 (27.5)  ==>  boots 320 -> 248, a in 20..25 (22.5)
    _rn_q(M, 'wp23-p17', 'A pair of boots is reduced from $320$ credits to $248$ credits. The discount is $a\\%$. Which interval contains $a$?',
          ['$20<a<25$', '$25<a<30$', '$15<a<20$', '$30<a<35$'], 1, [
              'The discount is $320-248=72$ credits.',
              'Estimate: $20\\%$ of $320$ is $64$ and $25\\%$ of $320$ is $80$. $72$ is between them, so $20<a<25$.',
              'Exact: $\\frac{72}{320}\\times100=22.5$.'])
    # p18: library p% to A, p% of the rest to B -> 100:(100-p)  ==>  baker q% to a café, q% of the rest to a school
    _rn_q(M, 'wp23-p18', 'A baker sells $q\\%$ of her loaves to a café, and then sells $q\\%$ of the remaining loaves to a school, where $0<q<100$. What is the ratio of the number of loaves sold to the café to the number sold to the school?',
          ['$(100-q):100$', '$100:(100-q)$', '$q:100$', '$1:1$'], 2, [
              'Plug in numbers: $100$ loaves and $q=20$. The café gets $20$, $80$ remain, and the school gets $20\\%$ of $80$, which is $16$. The ratio is $20:16=5:4$.',
              'Check the choices with $q=20$: only the ratio $100:(100-q)=100:80=5:4$ fits.',
              'In general, with $L$ loaves: the café gets $\\frac q{100}L$ and the school gets $\\frac q{100}\\cdot\\frac{100-q}{100}L$. Their ratio is $1:\\frac{100-q}{100}=100:(100-q)$.'])
    # p19: tablet; the ratio alone is not enough (choices reordered)  ==>  bicycle
    _rn_q(M, 'wp23-p19', 'A bicycle is sold at a discount. Which information alone is not enough to find its original price?',
          ['The amount saved and the paid price', 'The discount percentage and the amount saved',
           'The ratio of the paid price to the original price', 'The discount percentage and the paid price'], 3, [
              'A ratio gives only the relative size, not an amount of credits. Paying $\\frac34$ of the price could be $75$ out of $100$ or $150$ out of $200$.',
              'Each other choice gives at least one amount in credits, so the price can be found. For example, original price $=$ amount saved $+$ price paid.'])
    # p20: jacket -36, price x -> 3600/(x+36)  ==>  lamp -45, price y -> 4500/(y+45)
    _rn_q(M, 'wp23-p20', 'A lamp is discounted by $45$ credits. Its price after the discount is $y$ credits. What is the discount percentage?',
          ['$\\frac{4500}{y}$', '$\\frac{45y}{100}$', '$\\frac{4500}{y+45}$', '$\\frac{100(y+45)}{45}$'], 3, [
              'The original price is $y+45$.',
              'Change divided by the original, times $100$: $\\frac{45}{y+45}\\times100=\\frac{4500}{y+45}$.',
              'Check with a number: if $y=55$, the original price is $100$ and the discount is $45\\%$. $\\frac{4500}{55+45}=45$ ✓.'])


def rn_practice(M):
    """Approved clean-up: the copy out, at most 3 extra-bank warm-ups, September items whose type the Hebrew covers out."""
    N = lambda k: 'q-r26-t23-' + k
    out = [
        N('15'),        # copy: 28% of 75 (swap) - the same item as p21 and Topic 1's fast-practice-6 (practice_audit)
        # extra-bank warm-ups beyond 3 (kept: p25 percent increase, p26 "25% more -> ?% less", p24 one discount vs two)
        'wp23-p21',     # 16% of 25 - the swap example the lesson used (and a copy of q-r26-t23-15)
        'wp23-p22',     # +20% then -20% - the lesson's own "Up and down" example
        'wp23-p23',     # add water to salt water - mixtures are practised by q-r26-t23-11 / -12 and guided Q14
        'wp23-p27',     # 15% off, paid 306 - working backwards, as p05 and guided Q12
        # September items of a type the Hebrew practice covers
        N('06'),        # +10% for 3 years: multipliers over years, as p10
        N('10'),        # 120% then 150% of the original -> second rise: as p13
        N('13'),        # +20%, -25%, now 180 -> original: working backwards through two changes, as p10
        N('14'),        # up p% and down p% with letters: letters + p% of the new amount, as p18 / p16 / p20
    ]
    for qid in out:
        assert M.section_of(qid) == PRAC, qid
        M.unplace(qid)
    M.practice_order(PRAC, [
        'wp23-p01', 'wp23-p05', 'wp23-p02', 'wp23-p04', 'wp23-p09', 'wp23-p25', 'wp23-p26', 'wp23-p12', 'wp23-p07',
        'wp23-p13', 'wp23-p15', 'wp23-p11', 'wp23-p24', 'wp23-p17', 'wp23-p08', 'wp23-p06', N('09'), 'wp23-p10',
        'wp23-p14', 'wp23-p19', N('11'), N('12'), 'wp23-p20', 'wp23-p16', 'wp23-p18', 'wp23-p03'])


def renumber_pass(M):
    rn_guided(M)
    rn_order(M)
    rn_lessons(M)
    rn_cards(M)
    rn_practice_questions(M)
    rn_practice(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-07 methods spread (runs last). The 2026-10-06 exam methods are added wherever they genuinely solve a
# question: one written line at the end of the solution (existing lines kept), and on the clearest guided videos
# one extra "Method N" slide (board lines by click, pen only for marks). Methods taught in a later topic are
# written as a self-contained "Shortcut · <name>" line. Nothing in this topic is recorded (checked 2026-10-07).
# ======================================================================================================
SPREAD_RECORDED = set()


def _sp_line(M, qid, line):
    ex = list(M.q(qid).get('explanation') or [])
    if line in ex: return
    M.set_q(qid, expl=ex + [line])


def _sp_slide(M, qid, after_n, title, script):
    vid = 'solve-' + qid
    if vid in SPREAD_RECORDED: return
    assert M.video(vid)['questionId'] == qid, vid
    act = M.slide(vid, 2)['active']
    M.insert_slides(vid, after_n, [dict(mode='question', active=act, title=title, pre=[Q(qid)], script=script)])


def spread_methods(M):
    # ---- Arrow map (this topic, "Percent of a Percent") ----
    _sp_line(M, 'wp23-g061', r'Method 2 · Arrow map: Omer → Dana is $\times1.5$, and Dana → Lior is $\times\frac23$ ($33\frac13\%$ less leaves $\frac23$). From Omer to Lior, walk along both arrows: $1.5\cdot\frac23=1$. Lior earns exactly what Omer earns.')
    _sp_line(M, 'q-r26-t23-03', r'Method 2 · Arrow map: chair → desk is $\times1.5$ ($150\%$ OF), and chair → table is $\times2.5$ ($150\%$ MORE). From the desk to the table, go against the first arrow and along the second: $2.5\div1.5=\frac53$. The table is $\frac53$ of the desk: $66\frac23\%$ higher.')
    # ---- Percent shares as weights (topic 25), written as a self-contained shortcut ----
    _sp_line(M, 'q-r26-t23-12', r'Shortcut · Percent shares as weights: $30$ of the $50$ liters ($60\%$) are the $20\%$ drink. The mix moves $60\%$ of the way from $10\%$ toward $20\%$: $10\%+0.6\cdot10\%=16\%$. The simple average, $15\%$, is right only for a $50$–$50$ mix.')
    _sp_slide(M, 'wp23-g061', 3, 'Method 3 · Arrow map', [
        'Or the arrow map. Each sentence is one arrow, starting at the word after "than".',
        A("'Omer → Dana ×1.5 → Lior ×2/3' appears", T(r'Omer $\xrightarrow{\ \times1.5\ }$ Dana $\xrightarrow{\ \times\frac23\ }$ Lior', size=44)),
        'Fifty percent more: times one point five. A third less leaves two thirds: times two thirds.',
        A("'1.5 · 2/3 = 1' appears", T(r'$1.5\cdot\frac23=1$', size=44)),
        'From Omer to Lior we walk along both arrows. One point five times two thirds: one.',
        D('Circle choice 4'),
        'Choice four.'])
    _sp_slide(M, 'q-r26-t23-03', 2, 'Method 2 · Arrow map', [
        'Or the arrow map. Both sentences start at the chair.',
        A("'desk ← ×1.5 chair ×2.5 → table' appears", T(r'desk $\xleftarrow{\ \times1.5\ }$ chair $\xrightarrow{\ \times2.5\ }$ table', size=44)),
        'A hundred fifty percent OF the chair: times one point five. A hundred fifty percent MORE: times two point five.',
        A("'2.5 ÷ 1.5 = 5/3 → 66⅔% higher' appears", T(r'desk $\to$ table: $\ 2.5\div1.5=\frac53$ $\ \to\ 66\frac23\%$ higher', size=44)),
        'From the desk, back to the chair against the arrow: divide. Then on to the table: multiply. Five thirds — sixty-six and two thirds percent higher.',
        D('Circle choice 2'),
        'Choice two.'])


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last
