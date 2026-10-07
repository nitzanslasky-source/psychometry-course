"""Topic 25 - Averages. Course review 2026-09 fixes.
See t25_CHANGES.md for the plain-language list."""
import math_api
from dsl import T, H, A, D, Q

TOPIC = 25
L1, L2, LW = 'wp-080', 'wp-081', 'wp-086'
LEARN, ADV, PRACT = 'wp25-learn', 'wp25-advanced', 'wp25-practice'


def _word(n):
    return math_api._word(n).capitalize()


def _script(M, vid, n):
    """The current script of a slide, in DSL form (so it can be edited and passed to set_slide)."""
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _fix_draw(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _solution(M, qid, intro_line, slides):
    """Guided-question solution video in the style of solve-wp25-g082..085 (placed right after its question)."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % math_api._word(n)] + intro_line)]
    for title, script in slides:
        beats.append(dict(mode='question', active=0, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Average Questions', ['Question %d' % n], beats, M.section_of(qid),
                    kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Average Questions'
    v['hybrid']['num'] = 29
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _lesson_actives(M, vid):
    k = 0
    for b in M.video(vid)['beats']:
        if b['mode'] == 'concept':
            b['active'] = k; k += 1


def apply(M):
    S = M.set_q
    # =====================================================================================
    # 1. Lesson 1 "Averages": evenly spaced, balance, base number, every value changes
    # =====================================================================================
    M.insert_slides(L1, 2, [dict(mode='concept', title='Evenly spaced', script=[
        "Symmetric groups show up on the exam in disguise: evenly spaced numbers.",
        A('3, 7, 11, 15, 19 appears', T(r'$3,\quad 7,\quad 11,\quad 15,\quad 19$', size=50, gap=50)),
        "Three, seven, eleven, fifteen, nineteen. Each one is four more than the one before.",
        "Evenly spaced numbers are symmetric around the middle one.",
        D('Circle 11; write "average = 11"'),
        "The average is simply the middle number: eleven.",
        A("'Evenly spaced: average = middle = (first + last) ÷ 2' appears",
          T(r'Evenly spaced: average $=$ middle $=\dfrac{\text{first}+\text{last}}{2}$', size=44, gap=50)),
        D('Write "(3 + 19) ÷ 2 = 11"'),
        "Or take the first and the last. Three plus nineteen is twenty-two. Half of it: eleven.",
        "Consecutive numbers are evenly spaced too. One, two, three, up to a hundred? One plus a hundred, over two: fifty and a half.",
        "An even number of values? There is no single middle number. The average is halfway between the two middle ones.",
    ])])
    # slides now: 1 title, 2 middle, 3 evenly spaced, 4 adding the average, 5 towers, 6 formula, 7 one value, 8 recap
    M.insert_slides(L1, 5, [dict(mode='concept', title='The balance', script=[
        "Here's the fastest method on the exam: the balance.",
        "When we shared the blocks, the tall towers gave exactly what the short towers got.",
        A("'Above the average = below the average' appears", T(r'Above the average $=$ below the average', size=48, gap=50)),
        "The amounts above the average always equal the amounts below it. Together, the differences add up to zero.",
        A("'Scores 86, 93, 95, ? — average 90' appears", T(r'Scores $86,\ 93,\ 95,\ ?$ Average: $90$', size=48, gap=50)),
        "Four scores: eighty-six, ninety-three, ninety-five, and one more. The average is ninety. What's the missing score?",
        D('Under the scores write "−4, +3, +5"'),
        "Compare each score to ninety. Eighty-six is four below: minus four. Ninety-three: plus three. Ninety-five: plus five.",
        D('Write "−4 + 3 + 5 = +4"'),
        "Together: plus four. Four too many above the average.",
        D('Write "? = 90 − 4 = 86"'),
        "The missing score must be four below the average: eighty-six. Now the differences add up to zero.",
        "No big sum, no division. Just small differences.",
    ])])
    # slides: ... 6 balance, 7 formula, 8 one value, 9 recap
    M.insert_slides(L1, 7, [dict(mode='concept', title='A base number', script=[
        "A calculation shortcut, built on the balance.",
        A('97, 102, 104, 99 appears', T(r'$97,\quad 102,\quad 104,\quad 99$', size=50, gap=50)),
        "Four numbers near one hundred. Don't add them up.",
        "Pick a round number nearby — one hundred — and write only the differences.",
        D('Under the numbers write "−3, +2, +4, −1"'),
        "Minus three, plus two, plus four, minus one.",
        D('Write "−3 + 2 + 4 − 1 = +2  →  2 ÷ 4 = 0.5"'),
        "Together: plus two. Shared over four numbers: plus one half.",
        D('Write "average = 100 + 0.5 = 100.5"'),
        "The average is one hundred and a half. Small numbers, fewer mistakes.",
    ])])
    # slides: ... 8 base number, 9 one value changes, 10 recap
    M.insert_slides(L1, 9, [dict(mode='concept', title='Every value changes', script=[
        "Now every value changes in the same way.",
        A("'Add k to every value → the average goes up by k' appears",
          T(r'Add $k$ to every value $\to$ the average goes up by $k$', size=44, gap=40)),
        "Add five to every value? Every tower grows by five. The average grows by five.",
        A("'Multiply every value by k → the average is multiplied by k' appears",
          T(r'Multiply every value by $k$ $\to$ the average is multiplied by $k$', size=44, gap=40)),
        "Multiply every value by three? The sum is three times bigger, and the number of values stays the same. The average is three times bigger.",
        A("'Average age 30 now → 35 in five years' appears", T(r'Average age $30$ now $\to$ $35$ in five years', size=44, gap=40)),
        "The classic: a family's average age is thirty. In five years, everyone is five years older. The average age will be thirty-five.",
        D('Write "8, 10, 12 → average 10;  ×3 then +1: 25, 31, 37 → average 31 = 3 · 10 + 1"'),
        "Both at once? Do them in the same order. Eight, ten, twelve: average ten. Times three, plus one: twenty-five, thirty-one, thirty-seven. Average thirty-one. That's three times ten, plus one.",
    ])])
    # slides: ... 9 one value changes, 10 every value changes, 11 recap
    M.set_slide(L1, 11, script=[
        "Let's lock it in.",
        A("'Symmetric or evenly spaced? The average is the middle.' appears",
          T('Symmetric or evenly spaced? The average is the middle.', size=42)),
        A("'Adding the average doesn't change it.' appears", T("Adding the average doesn't change it.", size=42)),
        A("'Always between the smallest and the largest.' appears", T('Always between the smallest and the largest.', size=42)),
        A("'Above the average = below the average' appears", T(r'Above the average $=$ below the average', size=42)),
        A("'Average = sum ÷ number of values' appears", T(r'Average $=$ sum $\div$ number of values', size=42)),
        A("'Every value +k or ×k → the average +k or ×k' appears",
          T(r'Every value $+k$ or $\times k$ $\to$ the average $+k$ or $\times k$', size=42)),
        D('Underline "sum ÷ number of values"'),
        "Next: turning the formula around — the most useful move in average questions.",
    ])
    M.set_sidebar(L1, ['The middle', 'Evenly spaced', 'Adding the average', 'Towers of blocks', 'The balance',
                       'The formula', 'A base number', 'One value changes', 'Every value changes', 'Recap'])
    _lesson_actives(M, L1)

    # =====================================================================================
    # 2. Lesson 2 "Sum from the Average": largest possible value, how many were there?
    # =====================================================================================
    M.insert_slides(L2, 4, [dict(mode='concept', title='Largest possible value', script=[
        A("'5 positive integers, average 10. Largest possible value?' appears",
          T(r'$5$ positive integers, average $10$. What is the largest possible value of one of them?', size=44, gap=50)),
        "Five positive integers with an average of ten. How big can one of them be?",
        D('Write "sum = 5 × 10 = 50"'),
        "First the sum: fifty.",
        "To make one number as big as possible, make all the others as small as possible.",
        D('Write "1 + 1 + 1 + 1 = 4  →  50 − 4 = 46"'),
        "The smallest positive integer is one. Four ones use four. The big one gets the rest: forty-six.",
        A("'Trap: different integers' appears", T('Trap: the integers must be different', size=44, gap=50)),
        "Now the trap. What if the integers must be different?",
        D('Write "1 + 2 + 3 + 4 = 10  →  50 − 10 = 40"'),
        "Then the others can't all be one. The smallest they can be: one, two, three, four. That's ten. The big one gets forty.",
        "Read every word: positive, different, integers. Each word changes the answer.",
    ])])
    # slides: 1 title, 2 turn, 3 each, 4 what one can be, 5 largest, 6 new member, 7 recap
    M.insert_slides(L2, 6, [dict(mode='concept', title='How many were there?', script=[
        A("'Average 20. A new value 30 joins. New average 22. How many values were there?' appears",
          T('Average 20. A new value of 30 joins. The new average is 22. How many values were there before?',
            size=44, gap=50)),
        "Now turn it around. We know the averages — but not how many values there were.",
        "Use the balance. Compare the new value to the NEW average.",
        D('Write "30 − 22 = 8 above"'),
        "Thirty is eight above twenty-two.",
        D('Write "each old value: 22 − 20 = 2 below"'),
        "Each old value counted as twenty. Now it must count as twenty-two. Each one needs two more.",
        D('Write "8 ÷ 2 = 4 old values"'),
        "The eight extra units are shared in twos: four old values.",
        D('Write "check: 4 × 20 + 30 = 110 = 5 × 22"'),
        "Check: four times twenty, plus thirty, is a hundred ten. Five times twenty-two is a hundred ten.",
        D('Write "or: 20n + 30 = 22(n + 1)  →  8 = 2n  →  n = 4"'),
        "With an equation it's the same: twenty n plus thirty equals twenty-two times n plus one. n is four.",
        "Careful: four is the number BEFORE the new value joined. Now there are five. Read which one they ask for.",
    ])])
    M.set_slide(L2, 8, script=[
        A("'sum = number × average' appears", T(r'sum $=$ number $\times$ average', size=46)),
        A("'Treat every value as the average.' appears", T('Treat every value as the average.', size=44)),
        A("'Largest one: make the others as small as possible' appears",
          T('Largest one: make the others as small as possible.', size=44)),
        A("'How many before? (new value − new average) ÷ (rise of the average)' appears",
          T(r'How many before? $\dfrac{\text{new value}-\text{new average}}{\text{rise of the average}}$', size=44)),
        D('Underline "number × average"'),
        "Now let's use it on real exam questions.",
    ])
    M.set_sidebar(L2, ['Turn it around', 'Each as the average', 'What one can be', 'Largest possible value',
                       'A new member', 'How many were there?', 'Recap'])
    _lesson_actives(M, L2)

    # =====================================================================================
    # 3. Lesson 3 "Weighted Averages": heavy side gets the small part; equal-groups trap; bigger group rule
    # =====================================================================================
    sc = _script(M, LW, 6)
    k = sc.index("Twenty over four: parts of five. One part from seventy: seventy-five.")
    sc[k + 1:k + 1] = [
        "Which side gets the small part? The heavy side. The heavy side gets the SMALL part of the gap.",
        A("'The heavy side gets the small part.' appears", T('The heavy side gets the small part.', size=44)),
    ]
    M.set_slide(LW, 6, script=sc)
    M.set_slide(LW, 7, script=[
        "When you combine groups, the size of each group is its weight.",
        A("'6 values average 50; 9 values average 70' appears", T('6 values average 50; 9 values average 70', size=44, gap=60)),
        D('Write "size ratio 6 : 9 = 2 : 3"'),
        "Six to nine is two to three. Reduce the weights first — it doesn't change the average.",
        D('Write "(2·50 + 3·70) ÷ 5 = 310 ÷ 5 = 62"'),
        "Sixty-two. Not sixty — the bigger group pulls harder.",
        A("'50 and 70 → 60 only if the groups are equal' appears",
          T(r'The average of $50$ and $70$ is $60$ only if the groups are equal.', size=42, gap=40)),
        "Here's the trap. The average of fifty and seventy is sixty only if the two groups are the same size.",
        A("'Two groups: the answer is closer to the bigger group' appears",
          T('Two groups: the answer is closer to the bigger group.', size=42)),
        "And a quick check before you calculate. The answer is on the side of the bigger group.",
        D('Write "9 > 6 → the answer is above 60"'),
        "Nine values at seventy, only six at fifty. The answer must be above sixty. Sixty-two is. Good.",
    ])
    M.set_slide(LW, 8, script=[
        A("'Weight = number of copies' appears", T('Weight = number of copies', size=44)),
        A("'Divide by the sum of the weights' appears", T('Divide by the sum of the weights', size=44)),
        A("'Closer to the heavier group — distances are the weights flipped' appears",
          T('Closer to the heavier group: distances = weights, flipped', size=44)),
        A("'The heavy side gets the small part' appears", T('The heavy side gets the small part', size=44)),
        D('Underline "flipped"'),
        "Formula or ratios — both work. With a little practice, ratios are much faster.",
    ])

    # =====================================================================================
    # 4. Existing guided questions: text and videos
    # =====================================================================================
    S('wp25-g082', expl=['Sum $=$ number $\\times$ average: $9\\times8=72$.',
                         'The students do not each need to solve exactly $8$ puzzles. The average gives only their total.'])
    S('wp25-g083', expl=[
        'The balance point: the average of two numbers is exactly halfway between them. Leo is $176-171=5$ cm above '
        'the average, therefore Mina is $5$ cm below it: $171-5=166$ cm.',
        'Noor: $166+13=179$ cm.',
        'With the formula: $176+M=2\\cdot171=342$, therefore $M=166$.'])
    S('wp25-g084', choices=['$4$ times the average of the four numbers', '$6$ times the average of the four numbers',
                            '$2$ times the average of the four numbers', '$3$ times the average of the four numbers'],
      expl=['Call the numbers $a, b, c, d$. Each number appears in $3$ of the $6$ pairs, and each pair average is half '
            'of the pair sum.',
            'The sum of the six pair averages is therefore $\\frac{3(a+b+c+d)}{2}$.',
            'The average of the four numbers is $\\frac{a+b+c+d}{4}$, and $\\frac32=\\frac64$. Therefore the sum of the '
            'pair averages is $6$ times the average.',
            'Faster: plug in $a=b=c=d=1$. Each pair average is $1$, the sum is $6$ and the average is $1$. Only choice (2) gives $6$.'])
    S('wp25-g085', expl=[
        'Two tests: an average lead of $3$ points is a total lead of $2\\cdot3=6$ points for Kai.',
        'In art Kai is $5$ points behind. To finish $6$ points ahead, he must lead in science by $5+6=11$ points.',
        'Plug in: Kai $80$ and $80$ (average $80$). Zara: art $85$, average $77$, total $154$, science $154-85=69$. '
        '$80-69=11$.'])
    S('wp25-g087', expl=[
        'The exam counts twice: $\\frac{68+68+92}{3}=\\frac{228}{3}=76$.',
        'See-saw: weight ratio $2:1$, distance ratio $1:2$. The gap $92-68=24$ splits into $3$ parts of $8$. '
        'One part above $68$: $76$.'])
    S('wp25-g088', expl=[
        'See-saw: weight ratio $5:1$, distance ratio $1:5$. The gap $94-64=30$ splits into $6$ parts of $5$.',
        'The course score is one part below the heavy side: $94-5=89$.',
        'Check with the formula: $\\frac{5\\cdot94+64}{6}=\\frac{534}{6}=89$.'])
    S('wp25-g089', expl=[
        'The group sizes are the weights. Size ratio $6:9=2:3$.',
        '$\\frac{2\\cdot62+3\\cdot82}{5}=\\frac{124+246}{5}=\\frac{370}{5}=74$.',
        'Check: the bigger group is at $82$, therefore the answer must be above the midpoint $72$.'])
    S('wp25-g090', expl=[
        'Extra per item: if every line had $4$ words, there would be $1{,}200\\cdot4=4{,}800$ words.',
        'The real total is $1{,}200\\cdot4.5=5{,}400$ words: $600$ extra. Each $6$-word line adds $2$ extra words: '
        '$600\\div2=300$ lines.',
        'See-saw: $4.5$ is $0.5$ from $4$ and $1.5$ from $6$. Therefore the $4$-word group is $3$ times bigger: '
        '$1{,}200\\div4=300$ six-word lines.'])

    # Q3 video: a way out for weak students, and the plug-in warning
    M.edit_lines('solve-wp25-g084', 1, lambda ls: ls + [{'say': "If the algebra is hard for you, go straight to method two."}])
    M.edit_lines('solve-wp25-g084', 3, lambda ls: ls + [
        {'say': "One warning. With all the numbers equal, two choices can give the same result. Then try other numbers — like one, two, three, four."}])
    # colons in draw notes -> say "ratio"
    _fix_draw(M, 'solve-wp25-g088', 2, 'weights 1 : 5 → distances 5 : 1', 'weight ratio 1 : 5 → distance ratio 5 : 1')
    _fix_draw(M, 'solve-wp25-g089', 3, 'weights 2 : 3 → distances 3 : 2', 'weight ratio 2 : 3 → distance ratio 3 : 2')
    # Q8 video: method 3, "extra per item"
    M.insert_slides('solve-wp25-g090', 3, [dict(mode='question', title='Method 3 · Extra per item', pre=[Q('wp25-g090')], script=[
        "A third way: start everyone at the low value, then count the extra.",
        D('Write "all lines with 4 words: 1,200 × 4 = 4,800"'),
        "Pretend every line has four words: four thousand eight hundred words.",
        D('Write "real: 1,200 × 4.5 = 5,400  →  600 extra"'),
        "The real total is five thousand four hundred. Six hundred words are extra.",
        D('Write "each 6-word line adds 2  →  600 ÷ 2 = 300"'),
        "Each six-word line has two extra words. Six hundred over two: three hundred lines. Choice one.",
    ])])

    # =====================================================================================
    # 5. New guided questions (learn section)
    # =====================================================================================
    g = ['q-r26-t25-%02d' % k for k in range(1, 6)]

    # A - how many were there? (after Q1)
    M.new_q(g[0], TOPIC, 'The average score of the students in a class was 70. A new student with a score of 94 joined '
            'the class, and the class average rose to 73. How many students were in the class before the new student joined?',
            ['$6$', '$7$', '$8$', '$9$'], 2, [
                'The balance: the new score is $94-73=21$ points above the new average.',
                'Each old student moved from the old average to the new one: $73-70=3$ points. The $21$ extra points give '
                '$3$ points to each old student: $21\\div3=7$ students.',
                'Check: $7\\cdot70+94=490+94=584$, and $8\\cdot73=584$ ✓.',
                'With an equation: $70n+94=73(n+1)$, therefore $3n=21$ and $n=7$. The trap is $8$ — the number of students '
                'after the new student joined.'])
    M.place_q(g[0], LEARN, after='solve-wp25-g082')
    _solution(M, g[0], ["They give the averages. They want the number of students."], [
        ('Method 1 · The balance', [
            "Use the balance. Compare the new student to the NEW average.",
            D('Write "94 − 73 = 21 above"'),
            "Ninety-four is twenty-one above seventy-three.",
            D('Write "73 − 70 = 3 for each old student"'),
            "Every old student counted as seventy. Now each one must count as seventy-three: three more each.",
            D('Write "21 ÷ 3 = 7"'),
            "Twenty-one shared in threes: seven old students.",
            D('Circle choice 2'),
            "Choice two. Careful — eight is the number after the new student joined. That's the trap.",
        ]),
        ('Method 2 · Equation', [
            "Not sure? Write the sums. Before: n students, average seventy.",
            D('Write "70n + 94 = 73(n + 1)"'),
            "Add ninety-four. That equals the new sum: n plus one students, times seventy-three.",
            D('Write "70n + 94 = 73n + 73  →  21 = 3n  →  n = 7"'),
            "Open the brackets. Twenty-one equals three n. n is seven. Same answer.",
        ]),
    ])

    # B - balance with five scores (after Q2)
    M.new_q(g[1], TOPIC, 'Dana took five tests. Her scores on four of them were 78, 85, 91 and 88. The average of all five '
            'scores is 85. What was her score on the fifth test?',
            ['$81$', '$83$', '$85$', '$87$'], 2, [
                'The balance. Compare each score to the average $85$: $78\\to-7$, $85\\to0$, $91\\to+6$, $88\\to+3$.',
                'Together: $-7+0+6+3=+2$. The differences must add up to zero. Therefore the fifth score is $2$ below the '
                'average: $85-2=83$.',
                'Check: $78+85+91+88+83=425=5\\cdot85$ ✓.'])
    M.place_q(g[1], LEARN, after='solve-wp25-g083')
    _solution(M, g[1], ["Five scores and an average. Use the balance."], [
        ('Method 1 · The balance', [
            "Above the average equals below the average. Compare each score to eighty-five.",
            D('Under the scores write "−7, 0, +6, +3"'),
            "Seventy-eight: minus seven. Eighty-five: zero. Ninety-one: plus six. Eighty-eight: plus three.",
            D('Write "−7 + 0 + 6 + 3 = +2"'),
            "Together: plus two.",
            D('Write "fifth = 85 − 2 = 83"'),
            "The fifth score must bring it back to zero: two below eighty-five. Eighty-three.",
            D('Circle choice 2'),
            "Choice two. Eighty-seven is the trap: it adds the two instead of taking it away.",
        ]),
        ('Method 2 · The formula', [
            "The formula works too — with bigger numbers.",
            D('Write "5 × 85 = 425"'),
            "All five scores total four hundred twenty-five.",
            D('Write "78 + 85 + 91 + 88 = 342  →  425 − 342 = 83"'),
            "The four we know total three hundred forty-two. The fifth: eighty-three. Same answer, more work.",
        ]),
    ])

    # C - largest possible value with different integers
    M.new_q(g[2], TOPIC, 'Six different positive integers have an average of 9. What is the largest possible value of one of them?',
            ['$39$', '$44$', '$49$', '$54$'], 1, [
                'The sum is $6\\cdot9=54$.',
                'To make one number as large as possible, make the other five as small as possible. They must be different '
                'positive integers: $1, 2, 3, 4, 5$. Together: $15$.',
                'The largest possible value is $54-15=39$. With five ones the answer would be $49$, but the integers must be different.'])
    M.place_q(g[2], LEARN, after='solve-' + g[1])
    _solution(M, g[2], ["The largest possible value — and a trap in one word."], [
        ('Others as small as possible', [
            "First the sum. Six integers, average nine.",
            D('Write "6 × 9 = 54"'),
            "Fifty-four.",
            "To make one of them big, make the other five as small as possible.",
            D('Write "1 + 1 + 1 + 1 + 1 ✗"'),
            "Five ones? No — the integers must be different.",
            D('Write "1 + 2 + 3 + 4 + 5 = 15"'),
            "The five smallest different positive integers: one to five. Fifteen.",
            D('Write "54 − 15 = 39"'),
            "The big one gets the rest: thirty-nine.",
            D('Circle choice 1'),
            "Choice one. Forty-nine is the trap — five ones.",
        ]),
    ])

    # D - evenly spaced numbers
    M.new_q(g[3], TOPIC, 'The average of nine consecutive even numbers is 30. What is the largest of them?',
            ['$34$', '$38$', '$39$', '$46$'], 2, [
                'Consecutive even numbers are evenly spaced. Therefore the average is the middle number: the 5th of the nine '
                'numbers is $30$.',
                'Above it there are $4$ more numbers, each $2$ more than the one before: $30+4\\cdot2=38$.',
                'The numbers are $22, 24, \\ldots, 38$. Check: $\\frac{22+38}{2}=30$ ✓.'])
    M.place_q(g[3], LEARN, after='solve-' + g[2])
    _solution(M, g[3], ["Evenly spaced numbers. Find the middle first."], [
        ('The middle number', [
            "Consecutive even numbers: each one is two more than the one before. Evenly spaced.",
            "Evenly spaced? The average is the middle number.",
            D('Draw nine boxes in a row; write "30" in the middle box'),
            "Nine numbers: the middle one is the fifth. It's thirty.",
            D('Fill the boxes to the right: 32, 34, 36, 38'),
            "Four more numbers to the right, two apart: thirty-two, thirty-four, thirty-six, thirty-eight.",
            D('Circle choice 2'),
            "The largest is thirty-eight. Choice two.",
            "The trap: thirty-four. That's what you get if you forget that the numbers are even — two apart, not one.",
        ]),
    ])

    # E - every value changes
    M.new_q(g[4], TOPIC, 'The average of $a$, $b$ and $c$ is $20$. What is the average of $3a+2$, $3b+2$ and $3c+2$?',
            ['$60$', '$62$', '$66$', '$22$'], 2, [
                'Multiplying every value by $3$ multiplies the average by $3$: $3\\cdot20=60$.',
                'Adding $2$ to every value adds $2$ to the average: $60+2=62$.',
                'Plug in: $a=b=c=20$. Each new value is $3\\cdot20+2=62$, and the average is $62$.'])
    M.place_q(g[4], LEARN, after='solve-' + g[3])
    _solution(M, g[4], ["Every value changes the same way."], [
        ('Method 1 · Every value changes', [
            "Every value changes in the same way. The average changes in the same way.",
            D('Write "× 3: 20 → 60"'),
            "Every value times three: the average times three. Sixty.",
            D('Write "+ 2: 60 → 62"'),
            "Then plus two for every value: plus two for the average. Sixty-two.",
            D('Circle choice 2'),
            "Choice two. Sixty-six is the trap: it adds the two before multiplying.",
        ]),
        ('Method 2 · Plug in', [
            "Or plug in numbers. The easiest: all three are twenty.",
            D('Write "a = b = c = 20  →  3 · 20 + 2 = 62"'),
            "Each new value is three times twenty, plus two: sixty-two. All three are sixty-two. The average is sixty-two.",
        ]),
    ])

    # =====================================================================================
    # 6. Memory card
    # =====================================================================================
    c = M.card('mem-averages')
    c['intro'] = 'The middle, the sum, the balance and the see-saw.'
    c['tables'] = [
        {'title': 'Basics', 'head': ['Fact', 'In symbols / example'], 'rows': [
            ['Average', '$\\frac{\\text{sum}}{\\text{number of values}}$: $\\frac{3+8+4+10+5}{5}=6$'],
            ['Sum from the average', 'sum $=$ number $\\times$ average: $7\\times9=63$'],
            ['Symmetric group', 'the middle: $12,\\ 28\\to20$'],
            ['Evenly spaced (consecutive)', 'average $=$ middle $=\\frac{\\text{first}+\\text{last}}{2}$: $3, 7, 11, 15, 19\\to11$'],
            ['Add or remove the average', 'the average does not change'],
            ['Where it lies', 'between the smallest and the largest value'],
            ['Balance', 'above the average $=$ below it. $86, 93, 95, ?$ with average $90$: $-4+3+5=+4\\to ?=86$'],
            ['Base number', '$97, 102, 104, 99$: base $100$, $\\frac{-3+2+4-1}{4}=+0.5\\to100.5$'],
            ['Every value $+k$ or $\\times k$', 'the average $+k$ or $\\times k$ (ages in $5$ years: $+5$)'],
            ['Largest possible value', 'make the others as small as possible; different integers: $1, 2, 3, \\ldots$'],
            ['How many values before?', '$\\frac{\\text{new value}-\\text{new average}}{\\text{rise of the average}}$: $\\frac{30-22}{22-20}=4$'],
        ]},
        {'title': 'Weighted averages', 'head': ['Fact', 'In symbols / example'], 'rows': [
            ['Weighted average', '$\\frac{v_1w_1+v_2w_2}{w_1+w_2}$: $\\frac{70\\cdot3+90\\cdot1}{4}=75$'],
            ['See-saw', 'distances $=$ weights flipped: weight ratio $3:1\\to$ distance ratio $1:3$'],
            ['Groups', 'group size is the weight; reduce the ratio first ($6:9=2:3$)'],
            ['Two groups', 'the answer is closer to the bigger group; $50$ and $70$ give $60$ only if the groups are equal'],
            ['Extra per item', 'start everyone at the low value, count the extra: $\\frac{5{,}400-4{,}800}{2}=300$'],
        ]},
    ]
    c['tips'] = [
        'Given the number of values and the average? Multiply — that is the sum.',
        'Two values: the average is exactly halfway — use the balance point instead of the formula.',
        'On the exam a weighted average is just called "average".',
        'The heavy side gets the SMALL part of the gap.',
        'Letter answers? Plug in all values equal (for example, all $1$). If two choices match, try other numbers.',
        'Read every word: "positive", "different" and "integers" change the largest possible value.',
    ]

    # =====================================================================================
    # 7. Practice: text fixes and rewrites
    # =====================================================================================
    S('wp25-p01', expl=['For $5$ and $15$: average $\\frac{5+15}{2}=10$, difference $15-5=10$ ✓.',
                        'The others: $4$ and $10$ give average $7$, difference $6$. $6$ and $20$ give $13$ and $14$. '
                        '$8$ and $22$ give $15$ and $14$.'])
    S('wp25-p02', expl=['$70-64=6$ and $82-70=12$. The combined average is closer to Team A.',
                        'Distance ratio $6:12=1:2$, therefore the size ratio of A to B is $2:1$. Team A has more members.'])
    S('wp25-p03', expl=['Both groups have three numbers, and sum $=3\\times$ average. Equal averages give equal sums.',
                        'The difference of the sums is $0$.'])
    # p05: the original "average of 2/3 and 1/6" (restored, Pass 2); the "how many at first" version is q-r26-t25-14
    S('wp25-p05', expl=['$\\frac23=\\frac46$, therefore $\\frac23+\\frac16=\\frac46+\\frac16=\\frac56$.',
                        'The average is half of the sum: $\\frac56\\div2=\\frac5{12}$.'])
    S('wp25-p07', expl=['Adding Chen did not change the average. Therefore Chen’s score equals that average: $84$.',
                        'Ava and Ben average $84$, therefore they total $2\\cdot84=168$. Ava: $168-72=96$.'])
    S('wp25-p08', expl=['The middle temperature equals the average: its difference is $0$.',
                        'The differences add up to zero. Therefore the upper temperature is as far above the average as '
                        'the lower one is below it. The gaps are equal: ratio $1:1$.'])
    S('wp25-p09', expl=['$\\frac{18+a+b}{3}>\\frac{24+a}{2}$. Multiply by $6$: $36+2a+2b>72+3a$.',
                        'Therefore $2b-36>a$, that is, $a<2b-36$.'])
    S('wp25-p10', stem='$M$ is the average of $x$, $y$ and $z$. Given: $x<M<z$. Which of the following statements is necessarily true?',
      expl=['$M<z$ means $\\frac{x+y+z}{3}<z$. Multiply by $3$: $x+y+z<3z$.',
            'Therefore $x+y<2z$, and $\\frac{x+y}{2}<z$.'])
    S('wp25-p11', stem='The numbers $a$ and $b$ satisfy $b=a+2$, and their average is $3a$. What is their average in terms of $b$?',
      expl=['$\\frac{a+b}{2}=3a$, therefore $a+b=6a$ and $b=5a$, that is, $a=\\frac b5$.',
            'The average is $3a=3\\cdot\\frac b5=\\frac{3b}{5}$. (The condition $b=a+2$ is not needed for this. It gives $a=\\frac12$ and '
            '$b=\\frac52$, and indeed $\\frac{3}{5}\\cdot\\frac52=\\frac32=3\\cdot\\frac12$.)'])
    S('wp25-p12', expl=['An average cannot equal the largest value if any value is smaller: the balance would have only '
                        'values below it.', 'Therefore $r=s=t$.'])
    S('wp25-p13', expl=['The first two total $2\\cdot4=8$. The last two total $2\\cdot6=12$. Together: $20$, with the '
                        'second result counted twice.',
                        'All three total $3\\cdot5=15$. The second result is $20-15=5$.'])
    S('wp25-p14', expl=['The sum is at most $5\\cdot12=60$. The other four are at least $1$ each: $4$.',
                        'The largest possible value is $60-4=56$.'])
    S('wp25-p15', expl=['Year total: $12\\cdot140=1{,}680$. First eight months: $8\\cdot180=1{,}440$.',
                        'The last four months total $1{,}680-1{,}440=240$. December can have all $240$ if September, '
                        'October and November have $0$.'])
    S('wp25-p16', expl=['Both pairs contain Finn. The two-person averages differ by $11$, therefore the pair totals differ '
                        'by $2\\cdot11=22$.', '$(E+F)-(F+G)=E-G=22$. Ella has $22$ more stickers than Grace.'])
    S('wp25-p17', expl=['A’s average: $\\frac{6+6+8+12}{4}=8$. B’s average: $\\frac{11+13+15+17}{4}=14$.',
                        'Leaving lowers A’s average only if the score is above $8$. Joining lowers B’s average only if the '
                        'score is below $14$. The only score of A between $8$ and $14$ is $12$.'])
    S('wp25-p18', expl=['Three numbers in each group: an average gap of $3$ is a sum gap of $3\\cdot3=9$.',
                        '$(a+b+14)-(b+c+20)=9$, therefore $a-c-6=9$ and $a-c=15$.'])
    S('wp25-p19', expl=['Expensive tea: $84-72=12$ above the blend price. Cheap tea: $72-54=18$ below it.',
                        'Balance: $12E=18C$. Weight ratio $E:C=18:12=3:2$.'])
    S('wp25-p20', expl=['The combined average is $\\frac{76x+91y}{x+y}$. Divide the top and the bottom by $y$: '
                        '$\\frac{76\\cdot\\frac xy+91}{\\frac xy+1}$.',
                        'Therefore the ratio $\\frac xy$ is enough. Knowing only $x+y$, $x-y$ or $xy$ does not fix the ratio.'])
    S('wp25-p21', expl=['Old sum: $6\\cdot18=108$. New sum: $7\\cdot20=140$. The added number: $140-108=32$.',
                        'Faster (balance): the new number is the new average plus $2$ for each of the $6$ old numbers: '
                        '$20+6\\cdot2=32$.'])
    S('wp25-p22', expl=['Sum: $5\\cdot24=120$. Remove $39$: $120-39=81$, for four values.',
                        'New average: $\\frac{81}{4}=20.25$.'])
    S('wp25-p23', choices=['$74$', '$72$', '$76$', '$80$'],
      expl=['$\\frac{3\\cdot68+92}{4}=\\frac{204+92}{4}=\\frac{296}{4}=74$.',
            'See-saw: the gap $92-68=24$ splits into $4$ parts of $6$. One part above the heavy side: $68+6=74$.'])
    S('wp25-p24', expl=['Multiplying every number by $3$ multiplies the average by $3$: $3\\cdot15=45$.',
                        'Subtracting $4$ from every number subtracts $4$ from the average: $45-4=41$.'])
    S('wp25-p25', choices=['$168$', '$175$', '$161$', '$154$'],
      expl=['Sum $=$ number $\\times$ average: $7\\cdot23=161$.',
            'That the integers are consecutive is not needed for the sum.'])
    S('wp25-p26', expl=['Old total: $20\\cdot30=600$. New total: $25\\cdot32=800$.',
                        'The five newcomers total $800-600=200$ years. Their average: $\\frac{200}{5}=40$.'])
    S('wp25-p27', expl=['Extra per item: $30$ notebooks at $4$ credits would bring $30\\cdot4=120$ credits. The real '
                        'revenue is $30\\cdot6=180$ credits: $60$ extra.',
                        'Each $9$-credit notebook adds $9-4=5$ extra credits: $60\\div5=12$.'])
    # stems: letters and numbers of the math in TeX
    S('wp25-p04', stem='$u$ is the average of $a$ and $b$, and $v$ is the average of $c$ and $d$. Given: $S=a+b+c+d$. '
                       'What is the average of $u$ and $v$?')
    S('wp25-p09', stem='The average of $18$, $a$ and $b$ is greater than the average of $24$ and $a$. Which of the '
                       'following inequalities is necessarily true?')
    S('wp25-p12', stem='Given: $r\\le s\\le t$. The average of $r$, $s$ and $t$ is $t$. Which of the following is '
                       'necessarily true?')
    S('wp25-p18', stem='The average of $a$, $b$ and $14$ is $3$ greater than the average of $b$, $c$ and $20$. What is $a-c$?')
    S('wp25-p20', stem='A group has $x$ members with an average of 76 points and $y$ members with an average of 91 points '
                       '($x>0$ and $y>0$). Which piece of information is always enough to find the average of the whole group?')
    # p06 restored (Pass 2): the original "two rope lengths" question
    S('wp25-p06', choices=['$1:1$', '$1:2$', '$2:3$', '$3:4$'],
      expl=['If the two lengths were different, their average would lie strictly between them: above the shorter length and '
            'below the longer one. For example, $4$ and $6$ have the average $5$.',
            'The average equals one of the lengths only if both lengths are equal. The ratio is $1:1$.'])

    # =====================================================================================
    # 8. New practice questions
    # =====================================================================================
    P = {}
    P['06'] = ('The average of $47$, $52$, $55$, $49$ and $x$ is $50$. $x=?$', ['$44$', '$47$', '$50$', '$53$'], 2, [
        'Balance around $50$: $-3+2+5-1=+3$.',
        'The differences must add up to zero, therefore $x$ is $3$ below $50$: $x=47$.',
        'Check: $47+52+55+49+47=250=5\\cdot50$ ✓.'])
    P['07'] = ('The average age of the workers in a team is 34. A worker aged 58 joins the team, and the average age '
               'becomes 36. How many workers are in the team now?', ['$10$', '$11$', '$12$', '$13$'], 3, [
        'The new worker is $58-36=22$ years above the new average. Each old worker counts $36-34=2$ years more.',
        '$22\\div2=11$ old workers. With the new worker: $12$.',
        'Check: $11\\cdot34+58=374+58=432=12\\cdot36$ ✓.'])
    P['08'] = ('Four different positive integers have an average of 10. What is the smallest possible value of the '
               'largest of them?', ['$10$', '$11$', '$12$', '$13$'], 3, [
        'The sum is $4\\cdot10=40$. To keep the largest number small, keep the four numbers close together.',
        'If the largest were $11$, the biggest possible sum would be $11+10+9+8=38<40$. Impossible.',
        'With $12$: $8+9+11+12=40$ ✓. The answer is $12$.'])
    P['09'] = ('The average of eight consecutive odd numbers is 24. What is the smallest of them?',
               ['$15$', '$17$', '$19$', '$21$'], 2, [
        'Consecutive odd numbers are evenly spaced. With eight numbers, the average $24$ is halfway between the two '
        'middle numbers: $23$ and $25$.',
        'Below $23$ there are $3$ more numbers: $21, 19, 17$. The smallest is $17$.',
        'Check: the numbers are $17, 19, \\ldots, 31$, and $\\frac{17+31}{2}=24$ ✓.'])
    P['10'] = ('What is the average of all the integers from 13 to 57?', ['$34$', '$35$', '$36$', '$44$'], 2, [
        'Consecutive integers are evenly spaced: average $=\\frac{\\text{first}+\\text{last}}{2}=\\frac{13+57}{2}=35$.'])
    P['11'] = ('In 3 years, the average age of four siblings will be 15. Today a baby is born into the family. What is '
               'the average age of the five children today?', ['$9$', '$9.6$', '$12$', '$12.6$'], 2, [
        'In $3$ years every sibling is $3$ years older. Therefore today their average is $15-3=12$.',
        'Today’s total: $4\\cdot12=48$. The baby adds $0$: $\\frac{48}{5}=9.6$.',
        'The trap: $\\frac{4\\cdot15}{5}=12$ forgets that the ages are given for 3 years from now.'])
    P['12'] = ('In a class, 10 students have an average score of 60, 15 students have an average of 80, and 25 students '
               'have an average of 72. What is the average score of the whole class?',
               ['$70$', '$70\\frac23$', '$72$', '$74$'], 3, [
        '$\\frac{10\\cdot60+15\\cdot80+25\\cdot72}{50}=\\frac{600+1{,}200+1{,}800}{50}=\\frac{3{,}600}{50}=72$.',
        'Faster: the first two groups have size ratio $10:15=2:3$ and average $\\frac{2\\cdot60+3\\cdot80}{5}=72$. The third '
        'group is also at $72$. Therefore the whole class averages $72$.',
        'The trap: $\\frac{60+80+72}{3}=70\\frac23$ ignores the group sizes.'])
    P['13'] = ('What is the average of $998$, $1{,}003$, $1{,}005$, $996$ and $1{,}008$?',
               ['$1{,}001$', '$1{,}002$', '$1{,}003$', '$1{,}010$'], 2, [
        'Base number $1{,}000$. The differences: $-2+3+5-4+8=+10$.',
        'Shared over $5$ numbers: $10\\div5=2$. The average is $1{,}000+2=1{,}002$.'])
    # Pass 2: the fixer's new versions of p05 and p25 stay as extra questions under new ids
    P['14'] = ('The average of a list of numbers is 40. The number 16 is removed from the list, and the average of the '
               'remaining numbers is 43. How many numbers were in the list at first?', ['$7$', '$8$', '$9$', '$10$'], 3, [
        'The removed number is $40-16=24$ below the old average. Without it, each remaining number counts '
        '$43-40=3$ more.',
        '$24\\div3=8$ numbers remain. At first there were $8+1=9$.',
        'Check: $9\\cdot40-16=360-16=344=8\\cdot43$ ✓.'])
    P['15'] = ('Seven consecutive integers have an average of 23. What is the largest of them?',
               ['$26$', '$27$', '$29$', '$30$'], 1, [
        'Consecutive integers are evenly spaced. Therefore the average is the middle (4th) number: $23$.',
        'Three more numbers above it: $24, 25, 26$. The largest is $26$.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t25-' + k, TOPIC, stem, ch, cor, ex)
        M.place_q('q-r26-t25-' + k, PRACT)
    n = lambda k: 'q-r26-t25-' + k
    M.practice_order(PRACT, [
        'wp25-p05', 'wp25-p25', 'wp25-p21', 'wp25-p22', 'wp25-p26', 'wp25-p24', n('10'), n('15'), 'wp25-p23', 'wp25-p03',
        'wp25-p04', 'wp25-p01', n('06'), n('13'), 'wp25-p07', 'wp25-p27', 'wp25-p19', 'wp25-p02', 'wp25-p13', n('14'),
        n('07'), n('09'), 'wp25-p14', 'wp25-p15', n('08'), n('11'), n('12'), 'wp25-p16', 'wp25-p18', 'wp25-p06',
        'wp25-p08', 'wp25-p12',
        'wp25-p11', 'wp25-p09', 'wp25-p10', 'wp25-p17', 'wp25-p20'])

    summary(M)
    letters(M)

    # =====================================================================================
    # 9. Solution-video sidebars (one per section, in flow order) and pre-loaded stems
    # =====================================================================================
    for sec, _, _ in M.sections_of_topic(TOPIC):
        vids = [f['ref'] for f in M.D['flow'] if f['section'] == sec and f['type'] == 'video'
                and M.video(f['ref']).get('kind') == 'solution']
        labels = [M.video(v)['beats'][0]['bigTitle'] for v in vids]
        for k, v in enumerate(vids):
            M.set_sidebar(v, labels)
            for b in M.video(v)['beats']:
                if b['mode'] != 'title': b['active'] = k
    for v in M.D['videos'].values():
        if v['topic'] == TOPIC and v.get('questionId') in M.D['questions']:
            q = M.q(v['questionId'])
            for b in v['beats']:
                if b.get('canvas', '').startswith('Pre-loaded — question'):
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (q['id'], q['stem'])
    cut_repeats(M)
    add_methods(M)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)


def _b(label, tex, size=42):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summary(M):
    """Pass 2: a summary lesson right before the practice (end of the further guided examples)."""
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    sb = ['The middle', 'Sum and average', 'The balance', 'When values change', 'Largest value, how many',
          'Weighted averages', 'The see-saw', 'Groups', 'Before you practice']
    M.new_video('r26-t25-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            'A quick summary before the practice.',
            'Everything important about averages — in about three minutes.']),
        dict(title='The middle', active=0, script=[
            _b('Symmetric or evenly spaced: average = middle', 'Symmetric or evenly spaced: average $=$ middle $=\\dfrac{\\text{first}+\\text{last}}{2}$'),
            'Symmetric numbers? The average is the middle. No calculation.',
            _b('4, 10, 16, 22, 28 → 16', '$4,\\ 10,\\ 16,\\ 22,\\ 28\\ \\to\\ 16$'),
            'Evenly spaced numbers are symmetric too. The middle one, or first plus last, over two.',
            _b('Add or remove the average → no change', 'Add or remove a value equal to the average $\\to$ no change'),
            _b('Always between the smallest and the largest', 'Always between the smallest and the largest value'),
            'And the average always sits between the smallest and the largest value.']),
        dict(title='Sum and average', active=1, script=[
            _b('average = sum ÷ number', 'average $=\\dfrac{\\text{sum}}{\\text{number of values}}$'),
            _b('sum = number × average', 'sum $=$ number $\\times$ average: $8$ values, average $7\\ \\to\\ 56$'),
            'The most useful move: turn it around. Sum equals number times average.',
            'You don\'t know the values? You don\'t need them. Treat every value as the average.',
            _b('New value: update the sum AND the number', 'A new value: update the sum AND the number of values'),
            'A value joins or leaves? Change the sum, and change what you divide by.']),
        dict(title='The balance', active=2, script=[
            _b('Above the average = below the average', 'Above the average $=$ below the average'),
            'The differences from the average always add up to zero.',
            _b('77, 85, 86, ? with average 80: −3 + 5 + 6 = +8 → ? = 72', '$77,\\ 85,\\ 86,\\ ?$ average $80$: $-3+5+6=+8\\ \\to\\ ?=72$', size=40),
            'Plus eight too many above. So the missing one is eight below: seventy-two.',
            _b('Base number: 58, 63, 64, 59 → 60 + 4/4 = 61', 'Base number: $58,\\ 63,\\ 64,\\ 59\\ \\to\\ 60+\\frac{4}{4}=61$', size=40),
            'Numbers near a round number? Work only with the differences.']),
        dict(title='When values change', active=3, script=[
            _b('One value +12, four values → average +3', 'One value $+12$, four values $\\to$ average $+\\frac{12}{4}=+3$'),
            'One value changes? Share the change over all the values.',
            _b('Every value +k or ×k → average +k or ×k', 'Every value $+k$ or $\\times k$ $\\to$ the average $+k$ or $\\times k$'),
            'Every value changes the same way? The average changes the same way.',
            _b('Ages: average 24 now → 27 in three years', 'Average age $24$ now $\\to$ $27$ in three years'),
            'Both at once? Same order: times two, then plus five.']),
        dict(title='Largest value, how many', active=4, script=[
            _b('Largest one: the others as small as possible', 'Largest one: make the others as small as possible'),
            _b('6 positive integers, average 8: 48 − 5 = 43; different: 48 − 15 = 33', '$6$ positive integers, average $8$: $48-5=43$ · different: $48-15=33$', size=40),
            'Five ones? Only if they may be equal. Different integers: one, two, three, four, five.',
            _b('How many before? (new value − new average) ÷ (rise)', 'How many before? $\\dfrac{\\text{new value}-\\text{new average}}{\\text{rise of the average}}=\\dfrac{27-17}{17-15}=5$', size=40),
            'Compare the new value to the NEW average. Share the extra among the old values.',
            'And check: before the new value joined, or after?']),
        dict(title='Weighted averages', active=5, script=[
            'On the exam it just says "average". You must notice the weights.',
            _b('Weight = number of copies', 'Weight $=$ number of copies: $50, 50, 50, 50, 100\\ \\to\\ \\frac{300}{5}=60$'),
            _b('Weighted average formula', '$\\dfrac{v_1w_1+v_2w_2}{w_1+w_2}=\\dfrac{50\\cdot4+100\\cdot1}{4+1}=60$'),
            'Each value times its weight. Divide by the sum of the weights — not by the number of values.']),
        dict(title='The see-saw', active=6, script=[
            _b('Weight ratio 4 : 1 → distance ratio 1 : 4', 'Weight ratio $4:1\\ \\to$ distance ratio $1:4$'),
            'The distances are the weights, flipped.',
            _b('The heavy side gets the small part', 'The heavy side gets the SMALL part of the gap'),
            'Fifty and one hundred: a gap of fifty. Five parts of ten. One part from the heavy side: sixty.',
            _b('Extra per item', 'Extra per item: everyone at the low value, then count the extra'),
            'Only two kinds of items? Start everyone at the low value. Share the extra.']),
        dict(title='Groups', active=7, script=[
            _b('Group size = weight; reduce the ratio first', 'Group size $=$ weight · reduce the ratio first: $9:12=3:4$'),
            'Combining groups? The size of each group is its weight.',
            _b('40 and 60 → 50 only if the groups are equal', 'The average of $40$ and $60$ is $50$ only if the groups are equal'),
            _b('Closer to the bigger group', 'The answer is closer to the bigger group'),
            'Before you calculate: the answer is on the side of the bigger group.']),
        dict(title='Before you practice', active=8, script=[
            'Before you practice, ask yourself these questions.',
            _b('Do I know the number and the average? Then I know the sum.', 'Number and average given? Multiply: that\'s the sum.'),
            _b('Is it weighted? Which side is heavier?', 'Is it weighted? Which side is heavier?'),
            _b('Positive? Different? Integers?', 'Positive? Different? Integers? Every word counts.'),
            _b('Before or after the change?', 'Before or after the new value joined?'),
            _b('Letters in the answers? Plug in numbers.', 'Letters in the answers? Plug in numbers (all equal, then others).'),
            'The traps: the average of two group averages when the groups are not equal, dividing by the wrong number, and counting before instead of after.',
            'Good luck.'])],
        ADV, after=last)


# =====================================================================================
# 2026-10-01 elite comparison: averages written with letters (every "average" -> a sum), the balance with letters,
# and wp25-p18 becomes a guided question with a solution video.
# Real exam: 2023_autumn_q1_03, 2026_spring_q1_04, 2023_winter_q1_04, 2025_winter_q2_16, 2024_autumn_q1_08, 2020_autumn_q2_15
# =====================================================================================
def letters(M):
    # lesson 2 "Sum from the Average": 1 title, 2 turn, 3 each, 4 what one can be, 5 largest, 6 new member,
    # 7 how many were there?, 8 recap  ->  new slides 8, 9, 10; recap becomes 11
    M.insert_slides(L2, 7, [
        dict(mode='concept', title='Averages with letters', script=[
            "Now the same move — with letters. Many hard exam questions look like this.",
            A("'average of a and b is m → a + b = 2m' appears",
              T(r'The average of $a$ and $b$ is $m$ $\to$ $a+b=2m$', size=44, gap=30)),
            A("'average of a, b and c is k → a + b + c = 3k' appears",
              T(r'The average of $a$, $b$ and $c$ is $k$ $\to$ $a+b+c=3k$', size=44, gap=50)),
            "Every time you read \"the average\", write a sum instead: the number of values, times the average.",
            A("'The average of a and b is 7. The average of a, b and c is 10. c = ?' appears",
              T('The average of $a$ and $b$ is $7$.\nThe average of $a$, $b$ and $c$ is $10$.\n$c=?$', size=42)),
            D('Write "a + b = 2 · 7 = 14" and under it "a + b + c = 3 · 10 = 30"'),
            "Two averages — two sums. a plus b is fourteen. a plus b plus c is thirty.",
            D('Write "c = 30 − 14 = 16"'),
            "Now subtract. a and b cancel. c is sixteen.",
            "We never found a or b. We didn't need them.",
        ]),
        dict(mode='concept', title='An average equal to a letter', script=[
            A("'The average of x, y and z is x' appears", T('The average of $x$, $y$ and $z$ is $x$', size=46, gap=60)),
            "Sometimes the average equals one of the letters. Same move.",
            D('Write "x + y + z = 3x  →  y + z = 2x"'),
            "Three values with an average of x: the sum is three x. Take x away from both sides: y plus z is two x.",
            D('Write "→ the average of y and z is x"'),
            "So y and z also have an average of x.",
            A("'The average of a and b is a − b' appears", T('The average of $a$ and $b$ is $a-b$', size=46)),
            D('Write "a + b = 2(a − b)  →  a + b = 2a − 2b  →  a = 3b"'),
            "The average equals the difference? Two values: the sum is twice the difference. Open the brackets: a is three b.",
            "Brackets! Two times the WHOLE difference.",
        ]),
        dict(mode='concept', title='The balance with letters', script=[
            A("'The average of a, b, c and d is less than 6. The average of a, b and c is more than 6.' appears",
              T('The average of $a$, $b$, $c$ and $d$ is less than $6$.\nThe average of $a$, $b$ and $c$ is more than $6$.',
                size=42, gap=50)),
            "Less than, more than — the balance still works.",
            "Six is the line. a, b and c are above the line on average. Together they have extra.",
            "But all four together are below the line. Someone must pull them down — by more than that extra.",
            D('Write "d < 6"'),
            "Only d is left. So d must be less than six.",
            D('Write "check: d ≥ 6 → a + b + c + d > 18 + 6 = 24 → average > 6 ✗"'),
            "Check with sums. a plus b plus c is more than eighteen. If d were six or more, all four would add up to more than twenty-four. The average would be above six. Impossible.",
            D('Write "a = 2, b = 9, c = 8, d = 1 ✓  →  a < 6"'),
            "And a alone? It can be below six. Two, nine and eight have an average above six. Add one: the average of all four is five.",
            "So only d is sure. Necessarily true? Test the other letters with numbers.",
        ]),
    ])
    M.set_slide(L2, 11, script=[
        A("'sum = number × average' appears", T(r'sum $=$ number $\times$ average', size=44)),
        A("'Treat every value as the average.' appears", T('Treat every value as the average.', size=42)),
        A("'Largest one: make the others as small as possible' appears",
          T('Largest one: make the others as small as possible.', size=42)),
        A("'How many before? (new value − new average) ÷ (rise of the average)' appears",
          T(r'How many before? $\dfrac{\text{new value}-\text{new average}}{\text{rise of the average}}$', size=42)),
        A("'Letters? Every average becomes a sum: a + b + c = 3k' appears",
          T('Letters? Every average becomes a sum: $a+b+c=3k$', size=42)),
        D('Underline "number × average"'),
        "Now let's use it on real exam questions.",
    ])
    M.set_sidebar(L2, ['Turn it around', 'Each as the average', 'What one can be', 'Largest possible value',
                       'A new member', 'How many were there?', 'Averages with letters', 'An average equal to a letter',
                       'The balance with letters', 'Recap'])
    _lesson_actives(M, L2)

    # wp25-p18 (practice) -> guided question with a solution video, last guided question of "Learn and try"
    qid = 'wp25-p18'
    M.move(qid, LEARN, after='solve-wp25-g085')
    M.set_q(qid, expl=[
        'Turn each average into a sum. Three numbers in each group: an average gap of $3$ is a sum gap of $3\\cdot3=9$.',
        '$(a+b+14)-(b+c+20)=9$. The $b$ cancels: $a-c-6=9$, therefore $a-c=15$.',
        'Plug in: $b=0$ and $c=10$. The average of $0$, $10$ and $20$ is $10$. Then the average of $a$, $0$ and $14$ is '
        '$13$: $a+14=39$, $a=25$. $a-c=25-10=15$.',
        'The trap is $3$: the gap of the averages, not the gap of the sums.'])
    _solution(M, qid, ["Two averages with letters. Turn each one into a sum."], [
        ('Method 1 · Averages into sums', [
            "Each average is a sum of three numbers, divided by three.",
            "One average is three more than the other. Then its sum is three times three more: nine.",
            D('Write "(a + b + 14) − (b + c + 20) = 3 · 3 = 9"'),
            "First sum minus second sum: nine.",
            D('Write "a − c − 6 = 9"'),
            "b cancels. Fourteen minus twenty is minus six.",
            D('Write "a − c = 15"'),
            "So a minus c is fifteen.",
            D('Circle choice 1'),
            "Choice one. Three is the trap: that's the gap of the averages, not of the sums.",
        ]),
        ('Method 2 · Plug in', [
            "Or choose your own numbers. One condition, three letters: pick b and c, and a follows.",
            D('Write "b = 0, c = 10 → average of 0, 10, 20 = 10"'),
            "b is zero, c is ten. Zero, ten and twenty: the average is ten.",
            D('Write "average of a, 0, 14 = 13 → a + 14 = 39 → a = 25"'),
            "The first average is three more: thirteen. Its sum is thirty-nine. So a is twenty-five.",
            D('Write "a − c = 25 − 10 = 15"'),
            "Twenty-five minus ten: fifteen. Choice one again.",
        ]),
    ])


# =====================================================================================
# 2026-10-05 cut repeats: each lesson back to a short intro (Hebrew style); every idea a
# question video right after it already teaches is cut from the lesson; ideas no question
# teaches stay, or move as one line + board item into the question video that uses them.
# Runs last. Edited solution slides keep their pre-loaded canvas note (stem text).
# =====================================================================================
def _add_line(M, vid, n, before_say, line, item=None, label=None):
    """Insert one spoken line (+ optional board item) right before the line containing `before_say`
    (None: at the end of the slide). Keeps the slide's loads/canvas notes."""
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


def _fix_say(M, vid, n, old, new):
    def fn(lines):
        hit = False
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = l['say'].replace(old, new); hit = True
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
        return lines
    M.edit_lines(vid, n, fn)


def _keep_slides(M, vid, keep, sidebar):
    v = M.video(vid)
    M.remove_slides(vid, [k for k in range(1, len(v['beats']) + 1) if k not in keep])
    M.set_sidebar(vid, sidebar)
    _lesson_actives(M, vid)


def cut_repeats(M):
    # ---- Sum from the Average: keep title, "Turn it around", and the two letter slides no question teaches
    vid = L2
    _keep_slides(M, vid, [1, 2, 9, 10], ['Turn it around', 'An average equal to a letter', 'The balance with letters'])
    _add_line(M, vid, 2, None, "Every time you read 'the average', write a sum instead. Let's see it in the questions — and then two harder cases with letters.")
    _fix_say(M, vid, 3, 'Sometimes the average equals one of the letters. Same move.',
             'Sometimes the average equals one of the letters. Same move: write the sum.')
    _add_line(M, vid, 4, None, "Now let's use it on real exam questions.")
    # "Each as the average" -> Q1 (treat each student as eight). "What one can be" -> one line in Q1:
    _add_line(M, 'solve-wp25-g082', 2, 'The average hands you the total',
              "So one student alone could solve all seventy-two — but never more than the whole group.",
              T(r'One value $\le$ the whole sum $72$', 36), "'One value ≤ the whole sum 72' appears")
    # "Largest possible value" -> Q5 (others as small as possible, the "different" trap).
    # "A new member" -> one line in Q2 method 2; "How many were there?" -> Q2 (balance, equation, before/after trap).
    _add_line(M, 'solve-q-r26-t25-01', 3, 'Add ninety-four. That equals the new sum',
              "A new member changes both parts: the sum and the number of values.",
              T('New member: update the sum AND the number', 36), "'New member: update the sum AND the number' appears")
    # "Averages with letters" -> Q10 (wp25-p18: each average into a sum, b cancels).

    # ---- Weighted Averages: keep title + "Different weights" ----------------------------
    vid = 'wp-086'
    _keep_slides(M, vid, [1, 2], ['Different weights'])
    _add_line(M, vid, 2, None, "How to calculate it — the formula and the see-saw — we'll learn in the questions.")
    # "Repeated copies" -> Q11 (exam = two copies, divide by three); "The formula" -> Q12 method 2, Q13 method 1;
    # "The see-saw" + "Split the gap" -> Q11 method 2, Q12 method 1 (axis, weights flipped). Board item in Q11:
    _add_line(M, 'solve-wp25-g087', 3, 'Mark 76, one part above 68',
              "The heavy side always gets the small part of the gap.",
              T('The heavy side gets the small part', 36), "'The heavy side gets the small part' appears")
    # "Groups as weights" -> Q13 (same sizes 6 and 9, reduce to 2 : 3, midpoint trap, closer to the bigger group).
    # follow-up: the "3 × 5 = 1 × 15" balance check from "The see-saw" -> Q11 method 2 (76: 8 from 68, 16 from 92)
    _add_line(M, 'solve-wp25-g087', 3, None,
              "Why does it balance? Weight times distance is the same on both sides: two times eight, one times sixteen.",
              T(r'Balanced: $2\times8=1\times16$', 36, y=620), "'Balanced: 2 × 8 = 1 × 16' appears")


# =====================================================================================
# 2026-10-06 new exam methods (teacher-approved): percent shares as weights (board slide in Q13
# + card row), group totals "in t years", and the plug-in tip for "not necessarily equal". Runs last.
# =====================================================================================
def add_methods(M):
    # ---- 1. Percent shares as weights: one slide at the end of Q13 (groups as weights) ------------
    vid = 'solve-wp25-g089'
    act = M.slide(vid, 3)['active']
    M.insert_slides(vid, 3, [dict(mode='concept', active=act, title='Shares as weights', script=[
        "One more case the exam loves: the group sizes are given as PERCENTS.",
        A("'70% at 30, the rest at 50. Average?' appears",
          T(r'$70\%$ of the items cost $30$, the rest cost $50$. Average?', size=42, gap=40)),
        "The percents are the weights. Seventy percent at thirty, thirty percent at fifty.",
        A("'average = cheap + (share of the expensive) × gap' appears",
          T(r'Average $=$ cheap $+$ (share of the expensive) $\times$ gap', size=42, gap=40)),
        "Here's the fast way. Start at the cheap value. The average moves toward the expensive value — exactly by the share of the expensive ones.",
        D('Write "30 + 0.3 · 20 = 30 + 6 = 36"'),
        "The gap is fifty minus thirty: twenty. The expensive share is thirty percent. Thirty percent of twenty is six. Thirty plus six: thirty-six.",
        "Why? It's the see-saw again. Thirty percent of the weight sits at fifty, so the average goes thirty percent of the way from thirty to fifty.",
        D('Write "balance: 70 × 6 = 30 × 14 = 420 ✓"'),
        "Check the balance. Thirty-six is six above the cheap side and fourteen below the expensive side. Seventy times six, thirty times fourteen: four hundred twenty both. Balanced.",
        "And the heavy side — seventy percent — got the small part of the gap, as always.",
        "The trap is forty, the plain middle. That's only right when the shares are fifty-fifty.",
        A("'Percent shares = weights' appears", T('Percent shares $=$ weights', size=46)),
        "The rule: percent shares are weights. Cheap value, plus the expensive share times the gap.",
    ])])

    # ---- 2. Memory card -----------------------------------------------------------------------------
    c = M.card('mem-averages')
    basics = c['tables'][0]['rows']
    k = next(i for i, r in enumerate(basics) if r[0].startswith('Every value')) + 1
    basics.insert(k, ['Groups of different sizes, "in $t$ years"',
                      'each group\'s TOTAL grows by $t\\times$ its head-count: $5$ boys, $3$ girls, $4$ years → '
                      'boys $+20$, girls $+12$, the gap between the totals grows by $8$'])
    weighted = c['tables'][1]['rows']
    k = next(i for i, r in enumerate(weighted) if r[0] == 'Two groups') + 1
    weighted.insert(k, ['Percent shares as weights',
                        'average $=$ cheap value $+$ (share of the expensive) $\\times$ gap: $70\\%$ at $30$, the rest at $50$ → '
                        '$30+0.3\\cdot20=36$ (the see-saw: $70\\cdot6=30\\cdot14$)'])
    k = next(i for i, t in enumerate(c['tips']) if t.startswith('Letter answers? Plug in all values equal'))
    c['tips'].insert(k + 1, '"Not necessarily equal to the average"? Equal numbers catch nothing — every choice '
                            'equals the average. Use uneven numbers, like $0, 0, 0, 4$ (average $1$).')


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
    _pm_add(M, 'wp25-p23', [r'Method 2 · Percent shares as weights: the project has $1$ of the $4$ weights ($25\%$). Average $=$ low $+$ share $\times$ difference $=68+\frac14\cdot24=74$.'])
    _pm_add(M, 'wp25-p27', [r'Method 2 · Percent shares as weights, backwards: $6=4+\text{share}\cdot(9-4)$, therefore the share of 9-credit notebooks is $\frac25$. $\frac25\cdot30=12$.'])
    _pm_add(M, 'wp25-p19', [r'Method 2 · Percent shares as weights: $72=54+\text{share}\cdot(84-54)$, therefore the expensive share is $\frac{18}{30}=\frac35$ and the cheap share is $\frac25$. The ratio is $3:2$.'])
    _pm_add(M, 'wp25-p02', [r'Method 2 · Percent shares as weights: $70=64+(\text{share of B})\cdot18$, therefore Team B is $\frac13$ of all the members and Team A is $\frac23$. Team A has more members.'])
    _pm_add(M, 'q-r26-t25-11', [r'"In $t$ years": in $3$ years the four siblings total $4\cdot15=60$. A group’s total grows by $t\times$ the number of people: $3\cdot4=12$. Today they total $60-12=48$. With the baby: $\frac{48}{5}=9.6$.'])
    _pm_add(M, 'wp25-p20', [r'Method 2 · Percent shares as weights: average $=76+(\text{share of the }y\text{ members})\cdot15$, and that share is $\frac{y}{x+y}=\frac{1}{\frac xy+1}$. It depends only on $\frac xy$.'])
    _pm_add(M, 'wp25-p16', [r'Shortcut · Pick values that fit: one fact and three unknown counts. The question expects one answer, therefore any counts that fit give it. Finn $=0$ and Grace $=0$: Finn and Grace average $0$, therefore Ella and Finn average $11$, and Ella $=22$. $22-0=22$.'])
    _pm_add(M, 'wp25-p04', [r'Shortcut · Pick values that fit: the answer must work for all values, therefore take $a=b=c=d=1$. Then $S=4$ and $u=v=1$, with average $1=\frac S4$. The other choices give $\frac12$, $2$ and $8$.'])


# ======================================================================================================
# 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived question (guided wp25-g082 ..
# g090 and wp25-p18, practice wp25-p01 .. p20) gets new numbers and, where there is a story, a new story (names, objects,
# setting) - same concept, same trap, same level, at least the same methods (balance / balance point, sum = number x
# average, plug in, the see-saw, extra per item, percent shares as weights). Every guided solution video is rewritten to
# match. Hebrew-derived lesson examples get new numbers (the middle, adding the average, the towers + the formula,
# "8 / 2 = 4", the 5-unit matriculation example), and the summary's weighted example (50 / 100 with weights 4 : 1 =
# the Hebrew lesson's numbers) too. Order: Q3 heights (easy, the balance point) moves up to Q2; the balance with five
# scores follows; "how many were there?" after them. Practice clean-up 36 -> 26. Nothing in topic 25 is recorded.
# Runs last.
# ======================================================================================================
RN_RECORDED = set()   # no take of any topic-25 video in ~/Documents/Course.recordings (checked 2026-10-06)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides):
    """Rewrite the question slides (2, 3, ...) of a guided solution video. The pre-loaded question stays; the slide's
    loads / canvas notes are kept (canvas: the new stem)."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    for n, script in slides.items():
        b = v['beats'][n - 1]
        assert b['mode'] == 'question', (vid, n)
        keep = (b.get('loads'), b.get('canvas'))
        M.set_slide(vid, n, script=script)
        b = M.slide(vid, n); b['loads'], b['canvas'] = keep
    q = M.q(qid)
    v['title'] = v['navLabel'] = q['stem']
    for b in v['beats']:
        c = b.get('canvas') or ''
        if c.startswith('Pre-loaded — question'):
            b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])


def _rn_lines(M, vid, n, pairs):
    """Replace text in the spoken lines, draw notes, labels and board items of one slide. Every pair must hit."""
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = False
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]:
                    l[key] = l[key].replace(old, new); hit = True
        for it in b['items']:
            if isinstance(it.get('t'), str) and old in it['t']:
                it['t'] = it['t'].replace(old, new); hit = True
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    M.touched_videos.add(vid)


def rn_lessons(M):
    # ---- wp-080 #2 the middle: 12, 28 -> 20; 4, 8, 12, 16 -> 10  ==>  16, 30 -> 23; 6, 10, 14, 18 -> 12
    _rn_lines(M, L1, 2, [
        ('$12,\\quad 28$', '$16,\\quad 30$'), ('12 and 28 appear', '16 and 30 appear'),
        ('Twelve and twenty-eight.', 'Sixteen and thirty.'), ('Write "→ 20" next to them', 'Write "→ 23" next to them'),
        ('Twenty. Eight below it, eight above it.', 'Twenty-three. Seven below it, seven above it.'),
        ('$4,\\quad 8,\\quad 12,\\quad 16$', '$6,\\quad 10,\\quad 14,\\quad 18$'),
        ('4, 8, 12, 16 appear', '6, 10, 14, 18 appear'),
        ('Pair 4 with 16 and 8 with 12 using two arcs; write "→ 10"', 'Pair 6 with 18 and 10 with 14 using two arcs; write "→ 12"'),
        ("Four with sixteen, eight with twelve. Each pair's middle is ten. So the average is ten.",
         "Six with eighteen, ten with fourteen. Each pair's middle is twelve. So the average is twelve."),
    ])
    # ---- wp-080 #4 adding the average: 4, 6, 8 (+6) -> 6  ==>  3, 5, 7 (+5) -> 5
    _rn_lines(M, L1, 4, [
        ('$4,\\quad 6,\\quad 8$', '$3,\\quad 5,\\quad 7$'), ('$4,\\quad 6,\\quad 6,\\quad 8$', '$3,\\quad 5,\\quad 5,\\quad 7$'),
        ('4, 6, 8 appear', '3, 5, 7 appear'), ('4, 6, 6, 8 appear', '3, 5, 5, 7 appear'),
        ('Write "avg 6" under the list', 'Write "avg 5" under the list'),
        ('Write "avg 6" under the new list', 'Write "avg 5" under the new list'),
        ('Four, six, eight. The average is six — and notice, six is also one of the numbers.',
         'Three, five, seven. The average is five — and notice, five is also one of the numbers.'),
        ('Now add another six.', 'Now add another five.'), ('Still six.', 'Still five.'),
    ])
    # ---- wp-080 #5 towers 3, 8, 4, 10, 5 -> 6  ==>  4, 9, 3, 11, 8 -> 7 ; #7 the formula 30 / 5 = 6  ==>  35 / 5 = 7
    b = M.slide(L1, 5)
    b['items'][0]['v']['values'] = [4, 9, 3, 11, 8]
    b['items'][1]['v']['values'] = [7, 7, 7, 7, 7]
    _rn_lines(M, L1, 5, [
        ('Five block towers appear: 3, 8, 4, 10, 5', 'Five block towers appear: 4, 9, 3, 11, 8'),
        ('Circle the tallest tower (10) and the shortest (3)', 'Circle the tallest tower (11) and the shortest (3)'),
        ('five towers of 6', 'five towers of 7'),
        ('Five towers of blocks: three, eight, four, ten, five.', 'Five towers of blocks: four, nine, three, eleven, eight.'),
        ('no tower can end up taller than ten, or shorter than three.', 'no tower can end up taller than eleven, or shorter than three.'),
        ('every tower is six.', 'every tower is seven.'), ('Six is the average.', 'Seven is the average.'),
    ])
    _rn_lines(M, L1, 7, [
        ('$\\dfrac{3+8+4+10+5}{5}$', '$\\dfrac{4+9+3+11+8}{5}$'), ('3 + 8 + 4 + 10 + 5 appears', '4 + 9 + 3 + 11 + 8 appears'),
        ('Write "= 30/5 = 6"', 'Write "= 35/5 = 7"'), ('Thirty blocks, five towers. Six.', 'Thirty-five blocks, five towers. Seven.'),
    ])
    # ---- wp-081 #2: "8 / 2 = 4 -> 8 = 2 · 4" (the Hebrew's own example)  ==>  "12 / 3 = 4 -> 12 = 3 · 4"
    _rn_lines(M, L2, 2, [
        ('Under it write "8/2 = 4 → 8 = 2 · 4"', 'Under it write "12/3 = 4 → 12 = 3 · 4"'),
        ('Eight divided by two is four — so eight is two times four.',
         'Twelve divided by three is four — so twelve is three times four.'),
    ])
    # ---- wp-086 #2: 5-unit vs 1-unit matriculation exam (the Hebrew's example)  ==>  4-unit vs 2-unit
    _rn_lines(M, LW, 2, [
        ('Matriculation: a 5-unit math exam counts 5 times as much as a 1-unit exam',
         'Matriculation: a 4-unit exam counts twice as much as a 2-unit exam'),
        ("'5-unit math vs 1-unit language' appears", "'4-unit exam vs 2-unit exam' appears"),
        ('a five-unit exam counts five times as much as a one-unit exam.', 'a four-unit exam counts twice as much as a two-unit exam.'),
    ])
    # ---- summary: 50 / 100 with weights 4 : 1 (= the Hebrew lesson's 100 / 50, weights 4 : 1, gap 50)  ==>  30 / 90 -> 42
    sv = 'r26-t25-summary'
    _rn_lines(M, sv, 7, [
        ('$50, 50, 50, 50, 100\\ \\to\\ \\frac{300}{5}=60$', '$30, 30, 30, 30, 90\\ \\to\\ \\frac{210}{5}=42$'),
        ('$\\dfrac{v_1w_1+v_2w_2}{w_1+w_2}=\\dfrac{50\\cdot4+100\\cdot1}{4+1}=60$',
         '$\\dfrac{v_1w_1+v_2w_2}{w_1+w_2}=\\dfrac{30\\cdot4+90\\cdot1}{4+1}=42$'),
    ])
    _rn_lines(M, sv, 8, [
        ('Fifty and one hundred: a gap of fifty. Five parts of ten. One part from the heavy side: sixty.',
         'Thirty and ninety: a gap of sixty. Five parts of twelve. One part from the heavy side: forty-two.'),
    ])
    # ---- memory card: the examples that quote a renumbered lesson example / question
    c = M.card('mem-averages')
    rows = {r[0]: r for t in c['tables'] for r in t['rows']}
    rows['Average'][1] = '$\\frac{\\text{sum}}{\\text{number of values}}$: $\\frac{4+9+3+11+8}{5}=7$'
    rows['Symmetric group'][1] = 'the middle: $16,\\ 30\\to23$'
    rows['Groups'][1] = 'group size is the weight; reduce the ratio first ($8:12=2:3$)'
    rows['Extra per item'][1] = 'start everyone at the low value, count the extra: $\\frac{6{,}800-6{,}000}{2}=400$'


def rn_guided(M):
    # ---- g082 (Q1): 9 students, average 8 puzzles -> 72  ==>  12 volunteers, average 7 bags -> 84
    _rn_q(M, 'wp25-g082', 'Twelve volunteers clean a beach. On average, each volunteer fills 7 bags of litter. How many bags '
                          'do they fill altogether?', ['84', '91', '96', '72'], 1, [
        'Sum $=$ number $\\times$ average: $12\\times7=84$.',
        'The volunteers do not each need to fill exactly $7$ bags. The average gives only their total.'])
    _rn_video(M, 'wp25-g082', {2: [
        "Twelve volunteers, seven bags each on average. How many altogether?",
        "We don't know what each volunteer filled — and we don't need to.",
        "Treat each volunteer as filling exactly seven.",
        D('Write "12 × 7 = 84"'),
        "Twelve times seven: eighty-four.",
        D('Circle choice 1'),
        "Choice one.",
        A("'One value ≤ the whole sum 84' appears", T(r'One value $\le$ the whole sum $84$', 36)),
        "So one volunteer alone could fill all eighty-four — but never more than the whole group.",
        "The average hands you the total — without a single individual count.",
    ]})

    # ---- g083: Leo 176, average 171, Noor = Mina + 13 -> 179  (Hebrew: 171, 168, +16 -> 181)
    #      ==>  Ethan 169, average 164, Ryan = Chloe + 18 -> 177
    _rn_q(M, 'wp25-g083', 'Ethan is 169 cm tall. The average height of Ethan and Chloe is 164 cm. Ryan is 18 cm taller than '
                          'Chloe. How tall is Ryan?', ['182', '172', '187', '177'], 4, [
        'The balance point: the average of two numbers is exactly halfway between them. Ethan is $169-164=5$ cm above '
        'the average, therefore Chloe is $5$ cm below it: $164-5=159$ cm.',
        'Ryan: $159+18=177$ cm.',
        'With the formula: $169+C=2\\cdot164=328$, therefore $C=159$.'])
    # 2026-10-06 review: the question's own number line still showed Mina 166 / Mean 171 / Leo 176 / Noor 179
    M.q('wp25-g083')['solutionVisual'] = {'type': 'numberline', 'min': 155, 'max': 180, 'points': [159, 164, 169, 177],
                                          'labels': ['Chloe 159', 'Mean 164', 'Ethan 169', 'Ryan 177']}
    _rn_video(M, 'wp25-g083', {
        2: ["The average of Ethan and Chloe is one sixty-four. Put it into the formula.",
            D('Write "(169 + C) / 2 = 164"'),
            "Ethan plus Chloe, over two, is one sixty-four.",
            D('Write "169 + C = 328"'),
            "Multiply by two: three twenty-eight.",
            D('Write "C = 159"'),
            "Take away Ethan's one sixty-nine: Chloe is one fifty-nine.",
            D('Write "Ryan = 159 + 18 = 177"'),
            "Ryan is eighteen taller than Chloe: one seventy-seven.",
            D('Circle choice 4'),
            "Choice four."],
        3: ["Faster: the average of two numbers is exactly in the middle between them.",
            A('A number line from 155 to 180 appears', {'k': 'nl', 'min': 155, 'max': 180, 'y': 330}),
            D('Mark 164 (average) and 169 (Ethan) on the line'),
            "Ethan is one sixty-nine — five above the average.",
            D('Mark 159 (Chloe) five below 164'),
            "So Chloe must be five below it. One fifty-nine.",
            D('Mark 177 (Ryan), 18 above Chloe'),
            "Add eighteen for Ryan: one seventy-seven. Choice four — and almost no calculation."],
    })

    # ---- g084 (letter-only): four numbers, sum of the six pair averages = 6 x the average.
    #      Letters a, b, c, d  ==>  p, q, r, s; choice order 4, 6, 2, 3 (key 2)  ==>  4, 2, 6, 3 (key 3)
    _rn_q(M, 'wp25-g084', 'Four numbers are given. Take the average of each of the six different pairs, then add those six '
                          'averages. The result equals which of the following?',
          ['$4$ times the average of the four numbers', '$2$ times the average of the four numbers',
           '$6$ times the average of the four numbers', '$3$ times the average of the four numbers'], 3, [
        'Call the numbers $p, q, r, s$. Each number appears in $3$ of the $6$ pairs, and each pair average is half of the '
        'pair sum.',
        'The sum of the six pair averages is therefore $\\frac{3(p+q+r+s)}{2}$.',
        'The average of the four numbers is $\\frac{p+q+r+s}{4}$, and $\\frac32=\\frac64$. Therefore the sum of the pair '
        'averages is $6$ times the average.',
        'Faster: plug in $p=q=r=s=1$. Each pair average is $1$, the sum is $6$ and the average is $1$. Only choice (3) gives $6$.'])
    _rn_video(M, 'wp25-g084', {
        2: ["Call the four numbers p, q, r, s. There are six pairs.",
            D('List the pairs: pq, pr, ps, qr, qs, rs'),
            "Each pair's average is the two numbers over two.",
            "Add all six — the same denominator, so just add the tops.",
            D('Write "p appears 3 times → 3(p+q+r+s)/2"'),
            "Every number appears in three pairs. So the sum is three times p plus q plus r plus s, over two.",
            D('Write "average = (p+q+r+s)/4"'),
            "The overall average is the sum over four.",
            D('Write "3/2 = 6/4 → 6 × average"'),
            "Three halves is six quarters. So the sum is six times the average.",
            D('Circle choice 3'),
            "Choice three."],
        3: ["Now the psychometric way. Plug in numbers.",
            "Nothing says the numbers must be different. So make them all one.",
            D('Write "p = q = r = s = 1"'),
            "Every pair average is one. Six pairs: the sum is six. The overall average is one.",
            D('Next to the choices write: 4, 2, 6, 3'),
            "Four times the average: four. Out. Twice: two. Out. Six times: six — matches. Three times: three. Out.",
            D('Cross out choices 1, 2 and 4; circle choice 3'),
            "Three eliminated — only now we mark choice three.",
            "A hard question, solved in seconds.",
            "One warning. With all the numbers equal, two choices can give the same result. Then try other numbers — like one, two, three, four."],
    })

    # ---- g085: art / science, Zara +5, Kai's average +3 -> 11  (Hebrew: history / chemistry, +3, +4 -> 11)
    #      ==>  geography / music, Lena +6, Omar's average +5 -> 16
    _rn_q(M, 'wp25-g085', 'Omar and Lena take two tests, geography and music. Lena’s geography score is 6 points higher than '
                          'Omar’s. Omar’s two-test average is 5 points higher than Lena’s. How much higher is Omar’s music '
                          'score than Lena’s?', ['11', '4', '16', '10'], 3, [
        'Two tests: an average lead of $5$ points is a total lead of $2\\cdot5=10$ points for Omar.',
        'In geography Omar is $6$ points behind. To finish $10$ points ahead, he must lead in music by $6+10=16$ points.',
        'Plug in: Omar $70$ and $70$ (average $70$). Lena: geography $76$, average $65$, total $130$, music $130-76=54$. '
        '$70-54=16$.'])
    _rn_video(M, 'wp25-g085', {
        2: ["Two people, two tests. Let's make a table.",
            A('A table appears: Omar and Lena × geography, music',
              {'k': 'vis', 'v': {'type': 'table', 'headers': ['', 'Geography', 'Music'],
                                 'rows': [['Omar', '', ''], ['Lena', '', '']]}, 'w': 900, 'h': 180, 'y': 330}),
            "Omar's geography score — unknown. Call it g.",
            D('Fill in: Omar geography = g, Lena geography = g + 6'),
            "Lena scored six more in geography: g plus six.",
            D('Fill in: Omar music = m, Lena music = n'),
            "Music isn't given — two more unknowns.",
            D('Write "(g + m)/2 = (g + 6 + n)/2 + 5"'),
            "Omar's average is five more than Lena's.",
            D('Write "g + m = g + 6 + n + 10"'),
            "Multiply by two. The g's cancel.",
            D('Write "m = n + 16"'),
            "Omar's music is sixteen more.",
            D('Circle choice 3'),
            "Choice three. Eleven is the trap: six plus five forgets that an average lead of five is a total lead of ten."],
        3: ["Now the psychometric way: plug in numbers.",
            A('The same table appears',
              {'k': 'vis', 'v': {'type': 'table', 'headers': ['', 'Geography', 'Music', 'Average'],
                                 'rows': [['Omar', '', '', ''], ['Lena', '', '', '']]}, 'w': 1000, 'h': 180, 'y': 330}),
            D('Fill in: Omar geography 70, Lena geography 76'),
            "Say Omar got seventy in geography. Lena got six more: seventy-six.",
            D('Fill in: Omar music 70, Omar average 70'),
            "Omar's music? Pick seventy too — then his average is simply seventy.",
            D('Fill in: Lena average 65'),
            "Omar's average is five higher than Lena's. So Lena averages sixty-five.",
            D('Fill in: Lena music 54'),
            "Balance point: her seventy-six is eleven above sixty-five, so her music is eleven below. Fifty-four.",
            D('Write "70 − 54 = 16"'),
            "Seventy minus fifty-four: sixteen. Choice three — no equations."],
    })

    # ---- p18 (guided): avg(a, b, 14) = avg(b, c, 20) + 3 -> a - c = 15  ==>  avg(x, y, 11) = avg(y, z, 17) + 4 -> x - z = 18
    _rn_q(M, 'wp25-p18', 'The average of $x$, $y$ and $11$ is $4$ greater than the average of $y$, $z$ and $17$. What is $x-z$?',
          ['$12$', '$4$', '$18$', '$6$'], 3, [
        'Turn each average into a sum. Three numbers in each group: an average gap of $4$ is a sum gap of $3\\cdot4=12$.',
        '$(x+y+11)-(y+z+17)=12$. The $y$ cancels: $x-z-6=12$, therefore $x-z=18$.',
        'Plug in: $y=0$ and $z=10$. The average of $0$, $10$ and $17$ is $9$. Then the average of $x$, $0$ and $11$ is '
        '$13$: $x+11=39$, $x=28$. $x-z=28-10=18$.',
        'The traps: $4$ is the gap of the averages, not the gap of the sums. $12$ forgets the $11$ and the $17$, and $6$ '
        'subtracts the $6$ instead of adding it.'])
    _rn_video(M, 'wp25-p18', {
        2: ["Each average is a sum of three numbers, divided by three.",
            "One average is four more than the other. Then its sum is three times four more: twelve.",
            D('Write "(x + y + 11) − (y + z + 17) = 3 · 4 = 12"'),
            "First sum minus second sum: twelve.",
            D('Write "x − z − 6 = 12"'),
            "y cancels. Eleven minus seventeen is minus six.",
            D('Write "x − z = 18"'),
            "So x minus z is eighteen.",
            D('Circle choice 3'),
            "Choice three. Four is the trap: that's the gap of the averages, not of the sums."],
        3: ["Or choose your own numbers. One condition, three letters: pick y and z, and x follows.",
            D('Write "y = 0, z = 10 → average of 0, 10, 17 = 9"'),
            "y is zero, z is ten. Zero, ten and seventeen: the average is nine.",
            D('Write "average of x, 0, 11 = 13 → x + 11 = 39 → x = 28"'),
            "The first average is four more: thirteen. Its sum is thirty-nine. So x is twenty-eight.",
            D('Write "x − z = 28 − 10 = 18"'),
            "Twenty-eight minus ten: eighteen. Choice three again."],
    })

    # ---- g087: exam twice the project, 68 / 92 -> 76  ==>  written exam twice the oral exam, 61 / 97 -> 73
    _rn_q(M, 'wp25-g087', 'A final grade counts the written exam twice as much as the oral exam. Sara scores 61 on the written '
                          'exam and 97 on the oral exam. What is her final grade?', ['79', '70', '85', '73'], 4, [
        'The written exam counts twice: $\\frac{61+61+97}{3}=\\frac{219}{3}=73$.',
        'See-saw: weight ratio $2:1$, distance ratio $1:2$. The gap $97-61=36$ splits into $3$ parts of $12$. '
        'One part above $61$: $73$.',
        'The trap is $79$, the plain middle: it treats both exams as equal.'])
    _rn_video(M, 'wp25-g087', {
        2: ["The written exam counts twice — so treat it as two copies.",
            D('Write "(61 + 61 + 97) / 3"'),
            "Sixty-one, sixty-one, ninety-seven — divided by three weights, not two.",
            D('Write "= 219 / 3 = 73"'),
            "Two nineteen over three: seventy-three.",
            D('Circle choice 4'),
            "Choice four."],
        3: ["Now the see-saw. Weights two to one — so distances one to two.",
            A('An axis appears: 61 (weight 2) and 97 (weight 1)',
              {'k': 'vis', 'v': {'type': 'numberline', 'min': 59, 'max': 99, 'points': [61, 97],
                                 'labels': ['61 · w2', '97 · w1']}, 'w': 1000, 'h': 250, 'y': 330}),
            D('Split the gap 61→97 into 3 parts; write "36 ÷ 3 = 12"'),
            "The gap is thirty-six. Three parts of twelve.",
            A("'The heavy side gets the small part' appears", T('The heavy side gets the small part', 36)),
            "The heavy side always gets the small part of the gap.",
            D('Mark 73, one part above 61'),
            "One part from the heavy side: seventy-three. Choice four.",
            A("'Balanced: 2 × 12 = 1 × 24' appears", T(r'Balanced: $2\times12=1\times24$', 36, y=620)),
            "Why does it balance? Weight times distance is the same on both sides: two times twelve, one times twenty-four."],
    })

    # ---- g088: weight 5 / 1, exam 94, presentation 64 -> 89  ==>  lab report 5 / quiz 1, 91 / 55 -> 85
    _rn_q(M, 'wp25-g088', 'A lab report has weight 5 and a quiz has weight 1. A student scores 91 on the lab report and 55 on '
                          'the quiz. What is the weighted course score?', ['73', '85', '61', '79'], 2, [
        'See-saw: weight ratio $5:1$, distance ratio $1:5$. The gap $91-55=36$ splits into $6$ parts of $6$.',
        'The course score is one part below the heavy side: $91-6=85$.',
        'Check with the formula: $\\frac{5\\cdot91+55}{6}=\\frac{510}{6}=85$.'])
    _rn_video(M, 'wp25-g088', {
        2: ["Draw the axis: the scores on top, the weights underneath.",
            A('An axis appears: 55 (weight 1) and 91 (weight 5)',
              {'k': 'vis', 'v': {'type': 'numberline', 'min': 53, 'max': 93, 'points': [55, 91],
                                 'labels': ['55 · w1', '91 · w5']}, 'w': 1000, 'h': 250, 'y': 330}),
            "The lab report weighs five times as much — the average is five times closer to it.",
            D('Write "weight ratio 1 : 5 → distance ratio 5 : 1"'),
            D('Split the gap into 6 parts; write "36 ÷ 6 = 6"'),
            "The gap is thirty-six. Six parts of six.",
            D('Mark 85, one part below 91'),
            "One part down from ninety-one: eighty-five.",
            D('Circle choice 2'),
            "Choice two."],
        3: ["Check with the formula.",
            D('Write "(5·91 + 55) / 6 = (455 + 55) / 6 = 510 / 6 = 85"'),
            "Five ninety-ones and one fifty-five: five hundred ten. Over six: eighty-five. Same answer."],
    })

    # ---- g089: 6 numbers avg 62, 9 numbers avg 82 -> 74  (Hebrew: 5 / 70, 10 / 85 -> 80)
    #      ==>  8 numbers avg 58, 12 numbers avg 78 -> 70 (midpoint 68; flipped 66)
    _rn_q(M, 'wp25-g089', 'Eight numbers have an average of 58, and twelve other numbers have an average of 78. What is the '
                          'average of all twenty numbers?', ['70', '68', '72', '66'], 1, [
        'The group sizes are the weights. Size ratio $8:12=2:3$.',
        '$\\frac{2\\cdot58+3\\cdot78}{5}=\\frac{116+234}{5}=\\frac{350}{5}=70$.',
        'Check: the bigger group is at $78$, therefore the answer must be above the midpoint $68$.'])
    _rn_video(M, 'wp25-g089', {
        2: ["The values are the averages. The weights are the group sizes.",
            D('Write "(8·58 + 12·78) / 20"'),
            "Eight times fifty-eight, plus twelve times seventy-eight, over twenty.",
            "Make it easier: reduce the weights first. Eight to twelve is two to three.",
            D('Write "= (2·58 + 3·78) / 5 = (116 + 234) / 5 = 70"'),
            "Two fifty-eights and three seventy-eights: three hundred fifty. Over five: seventy.",
            D('Circle choice 1'),
            "Choice one. Reducing the weights always gives the same average — it's just a common factor."],
        3: ["Now without calculating. The midpoint of fifty-eight and seventy-eight is sixty-eight.",
            "The bigger group is at seventy-eight — so the average must be above sixty-eight.",
            D('Cross out choices 2 and 4'),
            "Sixty-eight and sixty-six are out.",
            "Sometimes that alone settles it. Here two choices survive — seventy and seventy-two — so we finish with ratios.",
            A('An axis appears: 58 (weight 2) and 78 (weight 3)',
              {'k': 'vis', 'v': {'type': 'numberline', 'min': 56, 'max': 80, 'points': [58, 78],
                                 'labels': ['58 · w2', '78 · w3']}, 'w': 1000, 'h': 250, 'y': 330}),
            D('Write "weight ratio 2 : 3 → distance ratio 3 : 2"; split 20 into 5 parts of 4'),
            "Weights two to three, distances three to two. Twenty into five parts of four.",
            D('Mark 70, three parts above 58'),
            "Three parts up from fifty-eight: seventy. Choice one."],
    })

    # ---- g090: 1,200 lines, 4 or 6 words, average 4.5 -> 300  (Hebrew: 1,000 lines, 6 or 7 words, 6.25 -> 250)
    #      ==>  2,000 boxes, 3 kg or 5 kg, average 3.4 kg -> 400 (traps: 500 = four parts, 800 = extra not halved, 1,600)
    _rn_q(M, 'wp25-g090', 'A delivery company ships 2,000 boxes. Every box weighs either 3 kg or 5 kg, and the average weight '
                          'is 3.4 kg per box. How many boxes weigh 5 kg?', ['500', '1,600', '400', '800'], 3, [
        'Extra per item: if every box weighed $3$ kg, the boxes would weigh $2{,}000\\cdot3=6{,}000$ kg.',
        'The real total is $2{,}000\\cdot3.4=6{,}800$ kg: $800$ kg extra. Each $5$-kg box adds $2$ extra kg: '
        '$800\\div2=400$ boxes.',
        'See-saw: $3.4$ is $0.4$ from $3$ and $1.6$ from $5$. Therefore the $3$-kg group is $4$ times bigger: $5$ parts, '
        '$2{,}000\\div5=400$ five-kg boxes.'])
    _rn_video(M, 'wp25-g090', {
        2: ["The values are three and five kilograms. Each value counts as many times as there are boxes of it.",
            "How many five-kilogram boxes? Unknown — call it x.",
            D('Write "x boxes of 5 kg, (2,000 − x) boxes of 3 kg"'),
            "The rest — two thousand minus x — weigh three kilograms.",
            D('Write "(5x + 3(2,000 − x)) / 2,000 = 3.4"'),
            "Divide by all two thousand boxes, and that equals three point four.",
            D('Write "5x + 6,000 − 3x = 6,800 → 2x = 800 → x = 400"'),
            "Multiply by two thousand: two x is eight hundred. x is four hundred.",
            D('Circle choice 3'),
            "Choice three."],
        3: ["Now with ratios. Put three, five and the average on the axis.",
            A('An axis appears: 3, 3.4 (average) and 5',
              {'k': 'vis', 'v': {'type': 'numberline', 'min': 2.5, 'max': 5.5, 'points': [3, 3.4, 5],
                                 'labels': ['3', '3.4', '5']}, 'w': 1000, 'h': 250, 'y': 330}),
            D('Mark the distances: 0.4 (from 3) and 1.6 (to 5)'),
            "Three point four is zero point four from three, one point six from five.",
            "Four times closer to three — so the three-kilogram group is four times bigger.",
            D('Write "2,000 ÷ 5 = 400"'),
            "Four parts and one part: five parts. Two thousand over five is four hundred. Five-kilogram boxes: one part. Four hundred.",
            "Careful: not two thousand over four. Five hundred is the trap.",
            "Choice three again — almost no calculation."],
        4: ["A third way: start everyone at the low value, then count the extra.",
            D('Write "all boxes 3 kg: 2,000 × 3 = 6,000"'),
            "Pretend every box weighs three kilograms: six thousand kilograms.",
            D('Write "real: 2,000 × 3.4 = 6,800  →  800 extra"'),
            "The real total is six thousand eight hundred. Eight hundred kilograms are extra.",
            D('Write "each 5-kg box adds 2  →  800 ÷ 2 = 400"'),
            "Each five-kilogram box has two extra kilograms. Eight hundred over two: four hundred boxes. Choice three."],
    })


def rn_order(M):
    """Q3 heights (easy, Hebrew Q4 'easy', the balance point) moves up right after Q1; then the balance with five scores;
    then 'how many were there?' (harder). Nothing is used before it is taught (the balance is in lesson 1)."""
    M.move('wp25-g083', LEARN, after='solve-wp25-g082')
    M.move('solve-wp25-g083', LEARN, after='wp25-g083')
    M.move('q-r26-t25-02', LEARN, after='solve-wp25-g083')
    M.move('solve-q-r26-t25-02', LEARN, after='q-r26-t25-02')
    # q-r26-t25-01 and its video now follow solve-q-r26-t25-02 (they kept their place before q-r26-t25-03)


def rn_practice_questions(M):
    # p01: average = difference, 5 and 15  ==>  7 and 21
    _rn_q(M, 'wp25-p01', 'Two positive integers have an average equal to their difference. Which pair could they be?',
          ['6 and 16', '9 and 25', '7 and 21', '8 and 20'], 3, [
        'For $7$ and $21$: average $\\frac{7+21}{2}=14$, difference $21-7=14$ ✓.',
        'The others: $6$ and $16$ give average $11$, difference $10$. $9$ and $25$ give $17$ and $16$. '
        '$8$ and $20$ give $14$ and $12$.'])
    # p02: teams 64 / 82, combined 70 -> A bigger  ==>  morning / evening classes 66 / 81, combined 71 -> morning bigger
    _rn_q(M, 'wp25-p02', 'The morning class has an average score of 66, and the evening class has an average score of 81. The '
                         'average of both classes together is 71. Which of the following statements is necessarily true?',
          ['The morning class has more students', 'The classes have equal sizes', 'The evening class has more students',
           'The sizes cannot be compared'], 1, [
        '$71-66=5$ and $81-71=10$. The combined average is closer to the morning class.',
        'Distance ratio $5:10=1:2$, therefore the size ratio of morning to evening is $2:1$. The morning class has more students.',
        'Method 2 · Percent shares as weights: $71=66+(\\text{share of the evening class})\\cdot15$, therefore the evening '
        'class is $\\frac13$ of all the students and the morning class is $\\frac23$. The morning class has more students.'])
    # p03 (letters): triples (a,b,c), (d,e,f)  ==>  (p,q,r), (x,y,z); choices reordered
    _rn_q(M, 'wp25-p03', 'The averages of the triples $(p,q,r)$ and $(x,y,z)$ are equal. What is $(p+q+r)-(x+y+z)$?',
          ['$p-x$', 'It cannot be determined from the information given.', '$0$', '$1$'], 3, [
        'Both groups have three numbers, and sum $=3\\times$ average. Equal averages give equal sums.',
        'The difference of the sums is $0$.'])
    # p04 (letters): u, v, a..d, S  ==>  m, n, p..s, T; choices reordered
    _rn_q(M, 'wp25-p04', '$m$ is the average of $p$ and $q$, and $n$ is the average of $r$ and $s$. Given: $T=p+q+r+s$. '
                         'What is the average of $m$ and $n$?',
          ['$2T$', '$\\frac T2$', '$\\frac T4$', '$\\frac T8$'], 3, [
        'First $m=\\frac{p+q}{2}$ and $n=\\frac{r+s}{2}$. Their average is $\\frac{m+n}{2}=\\frac{p+q+r+s}{4}=\\frac T4$.',
        'Shortcut · Pick values that fit: the answer must work for all values, therefore take $p=q=r=s=1$. Then $T=4$ and '
        '$m=n=1$, with average $1=\\frac T4$. The other choices give $8$, $2$ and $\\frac12$.'])
    # p05: average of 2/3 and 1/6 -> 5/12  ==>  3/4 and 1/8 -> 7/16
    _rn_q(M, 'wp25-p05', 'What is the average of $\\frac34$ and $\\frac18$?',
          ['$\\frac{1}{3}$', '$\\frac{7}{8}$', '$\\frac{3}{8}$', '$\\frac{7}{16}$'], 4, [
        '$\\frac34=\\frac68$, therefore $\\frac34+\\frac18=\\frac68+\\frac18=\\frac78$.',
        'The average is half of the sum: $\\frac78\\div2=\\frac7{16}$.'])
    # p06: two rope lengths, average = one of them -> 1:1  ==>  two package weights; choices reordered
    _rn_q(M, 'wp25-p06', 'Two packages have positive weights, and the average of the two weights equals one of the weights. '
                         'What is the ratio of the two weights?',
          ['$1:2$', '$1:1$', '$3:4$', '$2:3$'], 2, [
        'If the two weights were different, their average would lie strictly between them: above the lighter weight and '
        'below the heavier one. For example, $2$ and $8$ have the average $5$.',
        'The average equals one of the weights only if both weights are equal. The ratio is $1:1$.'])
    # p07: Ava, Ben, Chen; Ben 72, Chen 84 -> Ava 96  ==>  Mia, Leo, Sam; Leo 69, Sam 78 -> Mia 87
    _rn_q(M, 'wp25-p07', 'The average of Mia’s, Leo’s and Sam’s scores equals the average of Mia’s and Leo’s scores. Leo scored '
                         '69 and Sam scored 78. What did Mia score?', ['93', '78', '81', '87'], 4, [
        'Adding Sam did not change the average. Therefore Sam’s score equals that average: $78$.',
        'Mia and Leo average $78$, therefore they total $2\\cdot78=156$. Mia: $156-69=87$.'])
    # p08: three temperatures, average = middle -> gaps 1:1  ==>  three prices; choices reordered
    _rn_q(M, 'wp25-p08', 'Three different prices have an average equal to the middle price. What is the ratio of the gap '
                         'between the highest and the middle price to the gap between the middle and the lowest price?',
          ['$1:1$', '$1:2$', 'It cannot be determined from the information given.', '$2:1$'], 1, [
        'The middle price equals the average: its difference is $0$.',
        'The differences add up to zero. Therefore the highest price is as far above the average as the lowest one is '
        'below it. The gaps are equal: ratio $1:1$.'])
    # p09: avg(18, a, b) > avg(24, a) -> a < 2b - 36  ==>  avg(14, a, b) > avg(22, a) -> a < 2b - 38
    _rn_q(M, 'wp25-p09', 'The average of $14$, $a$ and $b$ is greater than the average of $22$ and $a$. Which of the following '
                         'inequalities is necessarily true?',
          ['$a<2b-38$', '$a>2b-38$', '$b<a-8$', '$a>2b+38$'], 1, [
        '$\\frac{14+a+b}{3}>\\frac{22+a}{2}$. Multiply by $6$: $28+2a+2b>66+3a$.',
        'Therefore $2b-38>a$, that is, $a<2b-38$.'])
    # p10 (letters): M avg of x, y, z; x < M < z  ==>  A avg of p, q, r; p < A < r; choices reordered
    _rn_q(M, 'wp25-p10', '$A$ is the average of $p$, $q$ and $r$. Given: $p<A<r$. Which of the following statements is '
                         'necessarily true?',
          ['$q=A$', '$\\frac{p+r}{2}<q$', '$\\frac{q+r}{2}<p$', '$\\frac{p+q}{2}<r$'], 4, [
        '$A<r$ means $\\frac{p+q+r}{3}<r$. Multiply by $3$: $p+q+r<3r$.',
        'Therefore $p+q<2r$, and $\\frac{p+q}{2}<r$.'])
    # p11: b = a + 2, average 3a -> 3b/5  ==>  b = a + 3, average 4a -> 4b/7 (trap 4b/3: a + b = 4a)
    _rn_q(M, 'wp25-p11', 'The numbers $a$ and $b$ satisfy $b=a+3$, and their average is $4a$. What is their average in terms of $b$?',
          ['$\\frac{4b}{3}$', '$\\frac b2$', '$\\frac{4b}{7}$', '$2b$'], 3, [
        '$\\frac{a+b}{2}=4a$, therefore $a+b=8a$ and $b=7a$, that is, $a=\\frac b7$.',
        'The average is $4a=4\\cdot\\frac b7=\\frac{4b}{7}$. (The condition $b=a+3$ is not needed for this. It gives '
        '$a=\\frac12$ and $b=\\frac72$, and indeed $\\frac{4}{7}\\cdot\\frac72=2=4\\cdot\\frac12$.)'])
    # p12 (letters): r <= s <= t, average t  ==>  x <= y <= z, average z; choices reordered
    _rn_q(M, 'wp25-p12', 'Given: $x\\le y\\le z$. The average of $x$, $y$ and $z$ is $z$. Which of the following is necessarily true?',
          ['$x+y=z$', '$x=y=z$', '$x<0$', '$z=0$'], 2, [
        'An average cannot equal the largest value if any value is smaller: the balance would have only values below it.',
        'Therefore $x=y=z$.'])
    # p13: spinner, all three 5, first two 4, last two 6 -> 5  ==>  darts, all three 6, first two 5, last two 8 -> 8
    _rn_q(M, 'wp25-p13', 'Emma throws three darts. The average score of all three darts is 6. The first two darts average 5, '
                         'and the last two average 8. What is the score of the second dart?', ['7', '6', '8', '10'], 3, [
        'The first two total $2\\cdot5=10$. The last two total $2\\cdot8=16$. Together: $26$, with the second dart counted twice.',
        'All three total $3\\cdot6=18$. The second dart is $26-18=8$. (The darts score $2$, $8$ and $8$.)'])
    # p14: five positive integers, average at most 12 -> 56  ==>  average at most 14 -> 66
    _rn_q(M, 'wp25-p14', 'Five positive integers have an average of at most 14. What is the largest possible value of one of them?',
          ['$65$', '$70$', '$66$', '$60$'], 3, [
        'The sum is at most $5\\cdot14=70$. The other four are at least $1$ each: $4$.',
        'The largest possible value is $70-4=66$. ($60$ would be right only if the integers had to be different.)'])
    # p15: charity, 140 per month, first 8 months 180 -> 240  ==>  library, 150 per month, first 8 months 170 -> 440
    _rn_q(M, 'wp25-p15', 'A library lends an average of 150 books per month over a year. In the first eight months, the average '
                         'is 170 books per month. At most how many books could it lend in December, assuming monthly totals '
                         'are nonnegative?', ['110', '600', '440', '170'], 3, [
        'Year total: $12\\cdot150=1{,}800$. First eight months: $8\\cdot170=1{,}360$.',
        'The last four months total $1{,}800-1{,}360=440$. December can have all $440$ if September, October and November '
        'have $0$.'])
    # p16: Ella & Finn vs Finn & Grace, +11 -> 22  ==>  Nina & Paul vs Paul & Rosa, +9 stamps -> 18
    _rn_q(M, 'wp25-p16', 'The average of Nina’s and Paul’s stamp counts is 9 greater than the average of Paul’s and Rosa’s '
                         'counts. How many more stamps does Nina have than Rosa?', ['$9$', '$27$', '$18$', '$36$'], 3, [
        'Both pairs contain Paul. The two-person averages differ by $9$, therefore the pair totals differ by $2\\cdot9=18$.',
        '$(N+P)-(P+R)=N-R=18$. Nina has $18$ more stamps than Rosa.',
        'Shortcut · Pick values that fit: one fact and three unknown counts. The question expects one answer, therefore '
        'any counts that fit give it. Paul $=0$ and Rosa $=0$: Paul and Rosa average $0$, therefore Nina and Paul average '
        '$9$, and Nina $=18$. $18-0=18$.'])
    # p17: A 6, 6, 8, 12 / B 11, 13, 15, 17 -> 12  ==>  team A 4, 9, 9, 14 / team B 12, 16, 18, 22 -> 14
    _rn_q(M, 'wp25-p17', 'In a game, the players of Team A scored 4, 9, 9 and 14 points, and the players of Team B scored 12, '
                         '16, 18 and 22 points. One player moves from Team A to Team B, and both team averages fall. What is '
                         'that player’s score?', ['9', '14', 'Impossible', '4'], 2, [
        'Team A’s average: $\\frac{4+9+9+14}{4}=9$. Team B’s average: $\\frac{12+16+18+22}{4}=17$.',
        'Leaving lowers A’s average only if the score is above $9$. Joining lowers B’s average only if the score is below '
        '$17$. The only score of A between $9$ and $17$ is $14$.'])
    # p19: tea 84 / 54, blend 72 -> 3:2  ==>  coffee 100 / 60, blend 85 -> 5:3 (trap 3:5 flipped, 5:8 the share)
    _rn_q(M, 'wp25-p19', 'Coffee costing 100 credits per kilogram is mixed with coffee costing 60 credits per kilogram. The '
                         'blend costs 85 credits per kilogram. What is the expensive-to-cheap weight ratio?',
          ['$3:5$', '$2:1$', '$5:3$', '$5:8$'], 3, [
        'Expensive coffee: $100-85=15$ above the blend price. Cheap coffee: $85-60=25$ below it.',
        'Balance: $15E=25C$. Weight ratio $E:C=25:15=5:3$.',
        'Method 2 · Percent shares as weights: $85=60+\\text{share}\\cdot(100-60)$, therefore the expensive share is '
        '$\\frac{25}{40}=\\frac58$ and the cheap share is $\\frac38$. The ratio is $5:3$.'])
    # p20: x members at 76, y at 91 -> x/y  ==>  m adults at 42, n children at 11 -> m/n; choices reordered
    _rn_q(M, 'wp25-p20', 'A club has $m$ adults with an average age of 42 and $n$ children with an average age of 11 ($m>0$ and '
                         '$n>0$). Which piece of information is always enough to find the average age of the whole club?',
          ['$m+n$', '$mn$', '$\\frac mn$', '$m-n$'], 3, [
        'The average age is $\\frac{42m+11n}{m+n}$. Divide the top and the bottom by $n$: $\\frac{42\\cdot\\frac mn+11}{\\frac mn+1}$.',
        'Therefore the ratio $\\frac mn$ is enough. Knowing only $m+n$, $m-n$ or $mn$ does not fix the ratio.',
        'Method 2 · Percent shares as weights: average $=11+(\\text{share of the adults})\\cdot31$, and that share is '
        '$\\frac{m}{m+n}=\\frac{\\frac mn}{\\frac mn+1}$. It depends only on $\\frac mn$.'])


def rn_practice(M):
    """Approved clean-up (36 -> 26). Copy: q-r26-t25-15 (= p25 with "largest"). Extra-bank items kept (3): p21 (a value
    joins), p23 (weights 3 : 1, percent shares), p27 (extra per item / shares backwards). September items kept (4, types
    the Hebrew practice does not have): q-06 (the balance, missing value), q-07 (how many were there), q-09 (evenly
    spaced), q-11 (every value changes, "in t years")."""
    N = lambda k: 'q-r26-t25-' + k
    out = [
        N('15'),      # copy of p25 (seven consecutive integers, average 23)
        'wp25-p22',   # extra: a value leaves (sum, then divide) - p21 / q-07 keep the type
        'wp25-p24',   # extra: every value x3 - 4 - guided Q7 and q-11
        'wp25-p25',   # extra: sum of consecutive integers = number x average - guided Q1
        'wp25-p26',   # extra: a group joins - p21 / p15 (sum from the average)
        N('08'),      # smallest possible largest value: the Hebrew practice has "largest possible" (p14)
        N('10'),      # average of 13 ... 57: evenly spaced, kept in q-09
        N('12'),      # three groups, weighted: the Hebrew practice has weighted groups (p02, p19, p20)
        N('13'),      # base number: the balance, kept in q-06
        N('14'),      # a value leaves, how many at first: kept in q-07
    ]
    for qid in out:
        assert M.section_of(qid) == PRACT, qid
        M.unplace(qid)
    M.practice_order(PRACT, [
        'wp25-p05', 'wp25-p21', N('06'), 'wp25-p01', 'wp25-p03', 'wp25-p04', 'wp25-p07', N('09'), 'wp25-p23', 'wp25-p27',
        'wp25-p19', 'wp25-p02', 'wp25-p13', N('07'), 'wp25-p14', 'wp25-p15', N('11'), 'wp25-p16', 'wp25-p06', 'wp25-p08',
        'wp25-p12', 'wp25-p11', 'wp25-p09', 'wp25-p10', 'wp25-p17', 'wp25-p20'])


def renumber_pass(M):
    rn_lessons(M)
    rn_guided(M)
    rn_order(M)
    rn_practice_questions(M)
    rn_practice(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-07 methods spread (runs last). Percent shares as weights (taught in Q13 "Shares as weights") is added as
# a written line to the other guided weighted-average questions. No slide: each of these videos already shows the
# see-saw, which is the same picture. Nothing in topic 25 is recorded (checked 2026-10-07).
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
    _sp_line(M, 'wp25-g087', r'Shortcut · Percent shares as weights: the weights $2$ and $1$ are shares $\frac23$ and $\frac13$. Start at the low score and add the share of the high one times the gap: $61+\frac13\cdot36=61+12=73$.')
    _sp_line(M, 'wp25-g088', r'Shortcut · Percent shares as weights: the lab report has $5$ of the $6$ weights. Start at the quiz score: $55+\frac56\cdot36=55+30=85$.')
    _sp_line(M, 'wp25-g089', r'Method 2 · Percent shares as weights: the $12$ numbers are $\frac{12}{20}=60\%$ of all the numbers. Average $=58+0.6\cdot(78-58)=58+12=70$.')
    _sp_line(M, 'wp25-g090', r'Method 2 · Percent shares as weights, backwards: $3.4=3+\text{share}\cdot(5-3)$, therefore the share of $5$-kg boxes is $\frac{0.4}{2}=\frac15$. $\frac15\cdot2{,}000=400$.')


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
    # "Pick values that fit" is taught in topic 51 (day 6), before topic 25: a normal method line.
    _po_relabel(M, 'wp25-p04', 'Shortcut · Pick values that fit:', 'Pick values that fit')
    _po_relabel(M, 'wp25-p16', 'Shortcut · Pick values that fit:', 'Pick values that fit')


_apply_before_plan_order_fix = apply


def apply(M):
    _apply_before_plan_order_fix(M)
    plan_order_fix(M)   # 2026-10-07 study-plan order: runs last
