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
    S('wp25-p07', expl=['Adding Chen did not change the average. Therefore Chen\'s score equals that average: $84$.',
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
    S('wp25-p17', expl=['A\'s average: $\\frac{6+6+8+12}{4}=8$. B\'s average: $\\frac{11+13+15+17}{4}=14$.',
                        'Leaving lowers A\'s average only if the score is above $8$. Joining lowers B\'s average only if the '
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
        'Today\'s total: $4\\cdot12=48$. The baby adds $0$: $\\frac{48}{5}=9.6$.',
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
