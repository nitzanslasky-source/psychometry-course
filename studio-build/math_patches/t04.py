"""Topic 4 - Expressions: Fundamentals. Course review 2026-09 (review_t3-4.md, PLAN.md)."""
from math_api import T, A, D, Q

TOPIC = 4
LEARN = 'expression-foundation'
PRACTICE = 'unit-t4-1'
LESSON = 'expression-basics'
FORMULAS = 'r26-t04-formulas'
TRINOM = 'r26-t04-trinomials'


def G(*lines):
    """'Given:' block with the conditions stacked, then the question."""
    return 'Given:\n' + lines[0] + '\n' + '\n'.join(lines[1:])


def CASES(*eqs):
    return r'$\begin{cases} ' + r' \\ '.join(eqs) + r' \end{cases}$'


def beat_to_slide(b):
    """Old beat -> slide dict (same items, lines and appear order)."""
    script = []
    for l in b['lines']:
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        else: script.append(D(l['draw']))
    return dict(title=b['title'], mode=b['mode'], active=b['active'], pre=[dict(it) for it in b['items'][:b['pre']]], script=script)


def replace_say(M, vid, n, old, new):
    def fn(lines):
        hit = False
        for l in lines:
            if l.get('say') == old: l['say'] = new; hit = True
        assert hit, (vid, n, old)
        return lines
    M.edit_lines(vid, n, fn)


def replace_draw(M, vid, n, old, new):
    def fn(lines):
        hit = False
        for l in lines:
            if l.get('draw') == old: l['draw'] = new; hit = True
        assert hit, (vid, n, old)
        return lines
    M.edit_lines(vid, n, fn)


# ======================================================================================================
# 1. Lesson video "Expressions - Fundamentals": small fixes, new examples, split off the formulas
# ======================================================================================================
def fix_lesson(M):
    v = M.video(LESSON)
    old = [dict(b) for b in v['beats']]
    formula_beats = [beat_to_slide(old[k]) for k in (8, 9, 10, 11)]   # slides 9-12 move to the new formulas video

    # slide 1 (title)
    replace_say(M, LESSON, 1, "Most of this you remember from school — so let's review it fast and make it airtight.",
                "Most of this you remember from school. Let's review it fast and make it airtight.")
    replace_say(M, LESSON, 1, "And then: the three short multiplication formulas. Those are gold on this exam.",
                "In the next video: the three short multiplication formulas. Those are gold on this exam.")

    # slide 3 like terms: color spelling + roots behave like letters
    replace_draw(M, LESSON, 3, 'Underline 5x and −2x in one colour, 6y and −2y in another, −3x² and 7x² in a third',
                 'Underline 5x and −2x in one color, 6y and −2y in another, −3x² and 7x² in a third')
    replace_say(M, LESSON, 3, "Let's colour the families. And remember — every minus sign travels with the term after it.",
                "Let's color the families. And remember — every minus sign travels with the term after it.")
    b3 = beat_to_slide(M.slide(LESSON, 3))
    b3['script'] += [
        A('3√5 − √5 appears', T(r'$3\sqrt{5}-\sqrt{5}$', size=56)),
        'Roots work the same way. Root five is one family. Root two is another family.',
        D('Write "= 2√5"'),
        'Three root five minus one root five: two root five. Just like three x minus x.',
    ]
    M.set_slide(LESSON, 3, script=b3['script'])

    # slide 4 multiplying terms: explicit draw note + a · a³ = a⁴
    replace_draw(M, LESSON, 4, 'Under them write "5a" and "6a²"', 'Under 2a + 3a write "= 5a"; under 2a · 3a write "= 6a²"')
    b4 = beat_to_slide(M.slide(LESSON, 4))
    b4['script'] += [
        A('a · a³ appears', T(r'$a\cdot a^3$', size=56)),
        'One more. a times a cubed.',
        'a cubed is three a\'s multiplied. One more a makes four a\'s.',
        D('Write "= a · a · a · a = a⁴"'),
        'a to the fourth. Just count the a\'s. The full power rules come later, in the powers topic.',
    ]
    M.set_slide(LESSON, 4, script=b4['script'])

    # slide 7 two brackets: second example with a minus
    b7 = beat_to_slide(M.slide(LESSON, 7))
    b7['pre'] = [dict(b7['pre'][0], gap=190)]
    b7['script'] += [
        A('(x − 5)(x + 2) appears', T(r'$(x-5)(x+2)$', size=64)),
        'Now with a minus. This is where sign mistakes live.',
        'Keep each sign glued to its number. The minus five is one piece.',
        D('Write "= x² + 2x − 5x − 10"'),
        'x times x: x squared. x times two: two x. Minus five times x: minus five x. Minus five times two: minus ten.',
        D('Write "= x² − 3x − 10"'),
        'Two x minus five x: minus three x. x squared minus three x minus ten.',
    ]
    M.set_slide(LESSON, 7, pre=b7['pre'], script=b7['script'])

    # slide 8 common factor: the "cancel vs reduce" remark moves here from the Q1 video
    b8 = beat_to_slide(M.slide(LESSON, 8))
    b8['script'] += [
        'One word about words. In five a minus five a, equal terms CANCEL each other — they make zero.',
        'In a fraction, a common FACTOR of the top and the bottom is REDUCED. That needs a product, not a sum.',
    ]
    M.set_slide(LESSON, 8, script=b8['script'])

    # remove slides 9-12 (they move to the formulas video); 13 (recap) becomes 9
    M.remove_slides(LESSON, [9, 10, 11, 12])

    # new slide 9: a whole bracket as a common factor
    bracket = dict(title='Bracket as a factor', mode='concept', active=7, pre=[], script=[
        'The common factor can be a whole bracket.',
        A('x(a + b) + 3(a + b) appears', T(r'$x(a+b)+3(a+b)$', size=60, gap=150)),
        'Two terms. Both of them have the bracket a plus b.',
        D('Underline both copies of (a + b)'),
        'So take the whole bracket out, just like a number.',
        D('Write "= (a + b)(x + 3)"'),
        'What is left from the first term? x. From the second? Three. a plus b, times x plus three.',
        A('a(x − 2) − 5(x − 2) appears', T(r'$a(x-2)-5(x-2)$', size=60)),
        'Same idea with a minus. The minus five stays with the five.',
        D('Write "= (x − 2)(a − 5)"'),
        'x minus two, times a minus five. Check by opening if you are not sure.',
    ])
    M.insert_slides(LESSON, 8, [bracket])

    # recap (now slide 10)
    M.set_slide(LESSON, 10, title='Recap', mode='concept', active=8, pre=[], script=[
        "Let's lock it in.",
        A("'Add and subtract only like terms' appears", T('Add and subtract only like terms', size=44)),
        A("'A minus before a bracket flips every sign' appears", T('A minus before a bracket flips every sign', size=44)),
        A("'Two brackets: every term meets every term' appears", T('Two brackets: every term meets every term', size=44)),
        A("'Expand to combine · Factor to cancel' appears", T('Expand to combine · Factor to cancel', size=44)),
        D('Circle "Factor to cancel"'),
        'The big takeaway: taking out a common factor. A number, a letter, or a whole bracket.',
        'Next video: the three short multiplication formulas.',
    ])
    M.set_sidebar(LESSON, ['Terms & coefficients', 'Like terms', 'Multiplying terms', 'Opening brackets', 'Minus before brackets',
                           'Two brackets', 'Common factor', 'Bracket as a factor', 'Recap'])
    return formula_beats


# ======================================================================================================
# 2. New lesson video "Multiplication Formulas" (old slides 9-12 + new slides)
# ======================================================================================================
def formulas_video(M, fb):
    s_ab, s_amb, s_sd, s_back = fb
    s_ab['active'] = 0
    s_ab['script'] = ['First formula: a plus b, all squared.' if x == "Now the short multiplication formulas. They show up a LOT on the exam — know them cold." else x
                      for x in s_ab['script']]
    s_amb['active'] = 1
    s_sd['active'] = 3
    s_back['active'] = 5
    s_back['script'] = ['You have to recognize the formulas backward too.' if x == "You have to recognise the formulas backwards too." else x
                        for x in s_back['script']]
    slides = [
        dict(mode='title', title='Multiplication Formulas', script=[
            'Now the three short multiplication formulas.',
            'They show up a LOT on the exam. Know them cold — forward and backward.',
        ]),
        s_ab, s_amb,
        dict(title='Power first', mode='concept', active=2, pre=[], script=[
            'One more trap: a number in front of a square.',
            A('3(x + 3)² appears', T(r'$3(x+3)^2$', size=64, gap=190)),
            'Order of operations: the power comes first. The three waits outside.',
            D('Write "= 3(x² + 6x + 9)"'),
            'First, x plus three, squared: x squared plus six x plus nine.',
            D('Write "= 3x² + 18x + 27"'),
            'Then the three multiplies every term. Three x squared, plus eighteen x, plus twenty-seven.',
            D('Next to it write "(3x + 9)² ✗"'),
            'Don\'t push the three inside the square. Three x plus nine, squared, is three times too big.',
            A('−x² and (−x)² appear side by side', {'k': 'row', 'items': ['$-x^2$', '$(-x)^2$'], 'sp': 320, 'below': 110}),
            'Same rule with a minus. In minus x squared, only x is squared. The minus comes after.',
            D('For x = 3: under −x² write "= −9"; under (−x)² write "= 9"'),
            'x equals three. Minus x squared: minus nine. Minus x in brackets, squared: plus nine.',
            'The brackets decide what gets squared.',
        ]),
        s_sd,
        dict(title='Number shortcuts', mode='concept', active=4, pre=[], script=[
            'The difference of squares works with plain numbers too.',
            A('98 · 102 appears', T(r'$98\cdot102$', size=64, gap=150)),
            'Ninety-eight and one hundred two are at the same distance from one hundred.',
            D('Write "= (100 − 2)(100 + 2) = 100² − 2² = 10000 − 4 = 9996"'),
            'One hundred minus two, times one hundred plus two. One hundred squared minus two squared: nine thousand nine hundred ninety-six.',
            A('31² − 29² appears', T(r'$31^2-29^2$', size=64)),
            'And backward: a difference of two squares.',
            D('Write "= (31 − 29)(31 + 29) = 2 · 60 = 120"'),
            'Thirty-one minus twenty-nine: two. Thirty-one plus twenty-nine: sixty. Two times sixty: one hundred twenty.',
            'No big squares at all. On the exam, that saves a full minute.',
        ]),
        s_back,
        dict(title='Perfect-square check', mode='concept', active=6, pre=[], script=[
            'Is a trinomial a perfect square? Three quick checks.',
            A('9x² − 12x + 4 appears', T(r'$9x^2-12x+4$', size=60, gap=110)),
            A('Check 1 appears', T('1. Are the first and last terms squares?', size=38)),
            D('Write "9x² = (3x)², 4 = 2² ✓"'),
            'Nine x squared is three x, squared. Four is two squared. Check one passes.',
            A('Check 2 appears', T(r'2. Is the middle term $2\cdot\text{first}\cdot\text{last}$?', size=38)),
            D('Write "2 · 3x · 2 = 12x ✓"'),
            'Two times three x times two: twelve x. Check two passes.',
            A('Check 3 appears', T('3. The sign of the middle term goes into the bracket', size=38)),
            D('Write "= (3x − 2)²"'),
            'The middle term is negative. Three x minus two, squared.',
            'If check two fails, it is not a perfect square. Take x squared plus ten x plus sixteen: two times four is eight, not ten.',
            'For those, there is the sum-product method. It comes later in this topic.',
        ]),
        dict(title='Value without x', mode='concept', active=7, pre=[], script=[
            'A favorite exam question. You get a plus b, and a times b.',
            A('The two conditions appear', T(CASES('a+b=7', 'ab=10'), size=54, gap=60)),
            'They ask for a squared plus b squared. Don\'t look for a and b. Use the formula.',
            A('(a + b)² = a² + 2ab + b² appears', T(r'$(a+b)^2=a^2+2ab+b^2$', size=50, gap=120)),
            'a plus b, squared, holds everything we need: a squared plus b squared, and two a b.',
            D('Write "49 = a² + b² + 20"'),
            'a plus b is seven. Seven squared: forty-nine. And ab is ten. Two a b: twenty.',
            D('Write "a² + b² = 49 − 20 = 29"'),
            'Forty-nine minus twenty: twenty-nine.',
            'The rule: square the sum, then subtract two a b.',
        ]),
        dict(title='Value without x (2)', mode='concept', active=7, pre=[], script=[
            'Now they give the sum and the difference.',
            A('The two conditions appear', T(CASES('a+b=5', 'a-b=3'), size=54, gap=60)),
            'They ask for a squared minus b squared.',
            A('a² − b² = (a + b)(a − b) appears', T(r'$a^2-b^2=(a+b)(a-b)$', size=50, gap=90)),
            D('Write "= 5 · 3 = 15"'),
            'Difference of squares: the sum times the difference. Five times three: fifteen.',
            'One more you will meet: x plus one over x.',
            A('(x + 1/x)² appears', T(r'$\left(x+\frac{1}{x}\right)^2=x^2+2+\frac{1}{x^2}$', size=50)),
            'The middle term is two, times x, times one over x. The x\'s cancel. It is just two.',
            'Know x plus one over x? Square it, then subtract two.',
        ]),
        dict(title='Recap', mode='concept', active=8, pre=[], script=[
            "Let's lock it in.",
            A('(a + b)² appears', T(r'$(a+b)^2=a^2+2ab+b^2$', size=44)),
            A('(a − b)² appears', T(r'$(a-b)^2=a^2-2ab+b^2$', size=44)),
            A('(a − b)(a + b) appears', T(r'$(a-b)(a+b)=a^2-b^2$', size=44)),
            A('a² + b² appears', T(r'$a^2+b^2=(a+b)^2-2ab$', size=44)),
            D('Circle the three formulas'),
            'Three formulas — and the middle term is where the points are lost.',
            'Use them forward to expand, backward to factor, and to find values without finding x.',
            'Two big takeaways from this lesson: taking out a common factor, and the three formulas.',
            'Now try a question — then watch its solution video.',
        ]),
    ]
    M.new_video(FORMULAS, TOPIC, 'Multiplication Formulas',
                ['(a + b)²', '(a − b)²', 'Power first', 'Sum × difference', 'Number shortcuts', 'Formulas backward',
                 'Perfect-square check', 'Value without x', 'Recap'], slides, LEARN, after=LESSON)


# ======================================================================================================
# 3. New lesson video: factoring trinomials (sum-product method)
# ======================================================================================================
def trinomial_video(M, after):
    slides = [
        dict(mode='title', title='Factoring Trinomials', script=[
            'One more tool, and the exam uses it a lot.',
            'Expressions like x squared plus five x plus six. Three terms: a trinomial.',
            'We will turn it into two brackets.',
        ]),
        dict(title='Brackets to trinomial', mode='concept', active=0, pre=[], script=[
            'Start from two brackets. We know how to open them.',
            A('(x + 2)(x + 3) appears', T(r'$(x+2)(x+3)$', size=64, gap=170)),
            D('Write "= x² + 3x + 2x + 6 = x² + 5x + 6"'),
            'x squared, plus three x, plus two x, plus six. x squared plus five x plus six.',
            D('Under 5x write "2 + 3"; under 6 write "2 · 3"'),
            'Look where the numbers went. Five is two PLUS three. Six is two TIMES three.',
            'The middle number is the sum. The last number is the product.',
            A('The general rule appears', T(r'$(x+p)(x+q)=x^2+(p+q)x+pq$', size=50)),
            'In general: p plus q in the middle, p times q at the end.',
        ]),
        dict(title='Sum and product', mode='concept', active=1, pre=[], script=[
            'Now backward. Factor x squared plus seven x plus ten.',
            A('x² + 7x + 10 appears', T(r'$x^2+7x+10$', size=64, gap=230)),
            'We need two numbers. Their product: ten. Their sum: seven.',
            D('List the pairs with product 10: "1 · 10 → sum 11", "2 · 5 → sum 7 ✓"'),
            'Start from the product. One and ten: sum eleven. Two and five: sum seven. Found them.',
            D('Write "= (x + 2)(x + 5)"'),
            'Two and five go into the brackets. x plus two, times x plus five.',
            D('Write "check: x² + 5x + 2x + 10 = x² + 7x + 10 ✓"'),
            'Check by opening: x squared, plus seven x, plus ten. It works.',
            'Always start from the product. A product has only a few pairs. A sum has endless pairs.',
        ]),
        dict(title='Signs', mode='concept', active=2, pre=[], script=[
            'What about minus signs? Same method. The signs belong to the numbers.',
            A('x² − 7x + 12 appears', T(r'$x^2-7x+12$', size=60, gap=150)),
            'Product: plus twelve. Sum: minus seven.',
            D('Write "(−3) · (−4) = 12, (−3) + (−4) = −7" and "= (x − 3)(x − 4)"'),
            'A positive product with a negative sum: both numbers are negative. Minus three and minus four.',
            A('x² + x − 12 appears', T(r'$x^2+x-12$', size=60, gap=150)),
            'Now x squared plus x minus twelve. Product: MINUS twelve. Sum: plus one.',
            D('Write "4 · (−3) = −12, 4 + (−3) = 1" and "= (x + 4)(x − 3)"'),
            'A negative product: one number is positive, one is negative. Here they differ by one: four and three.',
            'The sum is plus one. The bigger one gets the plus. Plus four, minus three.',
        ]),
        dict(title='Sign rules', mode='concept', active=3, pre=[], script=[
            'Here are the sign rules in one place.',
            A('Rule 1 appears', T(r'Last term $+$, middle term $+$: both numbers are $+$', size=38)),
            A('Rule 2 appears', T(r'Last term $+$, middle term $-$: both numbers are $-$', size=38)),
            'A positive last term: the two numbers have the same sign. The middle term tells you which sign.',
            A('Rule 3 appears', T(r'Last term $-$: one number is $+$, one is $-$', size=38)),
            A('Rule 4 appears', T('The bigger one gets the sign of the middle term', size=38, gap=90)),
            'A negative last term: different signs. The bigger number takes the sign of the middle term.',
            A('x² + 5x − 6 appears', T(r'$x^2+5x-6$', size=56)),
            D('Write "6 · (−1) = −6, 6 + (−1) = 5" and "= (x + 6)(x − 1)"'),
            'Product minus six, sum plus five. Six and minus one. x plus six, times x minus one.',
        ]),
        dict(title='Common factor first', mode='concept', active=4, pre=[], script=[
            'If x squared has a number in front, look for a common factor first.',
            A('2x² + 10x + 12 appears', T(r'$2x^2+10x+12$', size=60, gap=150)),
            D('Write "= 2(x² + 5x + 6) = 2(x + 2)(x + 3)"'),
            'Two comes out. Inside: product six, sum five. Two and three.',
            A('The fraction appears', T(r'$\dfrac{x^2+5x+6}{x+2}$', size=60)),
            'And here is why we factor: to reduce fractions.',
            D('Rewrite the top as "(x + 2)(x + 3)", cross out (x + 2) on the top and on the bottom, write "= x + 3"'),
            'The top is x plus two, times x plus three. Reduce x plus two with the bottom. x plus three is left.',
            'One condition: x is not negative two. The bottom can never be zero.',
        ]),
        dict(title='Check with a number', mode='concept', active=5, pre=[], script=[
            'Not sure about your brackets? Plug in a number.',
            A('The claim appears', T(r'$x^2+5x+6\ \overset{?}{=}\ (x+1)(x+6)$', size=54, gap=150)),
            'Say you wrote x plus one, times x plus six. Is it right?',
            D('Write "x = 0: 6 and 1 · 6 = 6"'),
            'x equals zero: both sides give six. Looks fine — but zero hides mistakes in the middle term.',
            D('Write "x = 2: 4 + 10 + 6 = 20, but 3 · 8 = 24 ✗"'),
            'x equals two: the left side is twenty, the right side is twenty-four. Wrong brackets.',
            'The product is right, but the sum is seven, not five. Two and three give the right sum.',
            'So pick a small number, but not zero and not one.',
        ]),
        dict(title='Recap', mode='concept', active=6, pre=[], script=[
            "Let's lock it in.",
            A('Line 1 appears', T('Two numbers: product = last term, sum = middle term', size=42)),
            A('Line 2 appears', T('Start from the pairs of the product', size=42)),
            A('Line 3 appears', T('Signs: same sign if the last term is $+$, different signs if it is $-$', size=42)),
            A('Line 4 appears', T('Common factor first · factor to reduce · check with a number', size=42)),
            'Product and sum. That is the whole method.',
            'Now try the questions.',
        ]),
    ]
    M.new_video(TRINOM, TOPIC, 'Factoring Trinomials',
                ['Brackets to trinomial', 'Sum and product', 'Signs', 'Sign rules', 'Common factor first',
                 'Check with a number', 'Recap'], slides, LEARN, after=after)


# ======================================================================================================
# 4. Memory cards
# ======================================================================================================
def cards(M):
    c = M.card('mem-formulas')
    c['intro'] = 'Use them forward to expand and backward to factor. They also find values without finding the letters.'
    c['tables'] = [{'title': '', 'head': ['Formula', 'Example'], 'rows': [
        [r'$(a+b)^2=a^2+2ab+b^2$', r'$(3+2)^2=9+12+4=25$'],
        [r'$(a-b)^2=a^2-2ab+b^2$', r'$(5-3)^2=25-30+9=4$'],
        [r'$(a-b)(a+b)=a^2-b^2$', r'$48\cdot52=50^2-2^2=2500-4=2496$'],
        [r'$a^2+b^2=(a+b)^2-2ab$', r'$a+b=7$ and $ab=10$: $a^2+b^2=49-20=29$'],
        [r'$\left(x+\frac{1}{x}\right)^2=x^2+2+\frac{1}{x^2}$', r'$x+\frac{1}{x}=3$: $x^2+\frac{1}{x^2}=9-2=7$'],
        [r'$ka+kb=k(a+b)$', r'$6x+15=3(2x+5)$; $x(a+b)+3(a+b)=(a+b)(x+3)$'],
        [r'$-(b-c)=-b+c$', 'a minus before a bracket flips every sign'],
    ]}]
    c['tips'] = [
        r'$(a+b)^2\ne a^2+b^2$ — the middle term $2ab$ is the whole point.',
        r'Power first: $3(x+3)^2=3(x^2+6x+9)=3x^2+18x+27$, not $(3x+9)^2$.',
        r'$-x^2$ is not $(-x)^2$: for $x=3$, $-x^2=-9$ but $(-x)^2=9$.',
        r'$(b-a)^2=(a-b)^2$, but $b-a=-(a-b)$, and $\frac{a-b}{b-a}=-1$ (when $a\ne b$).',
        r'Perfect square? (1) first and last terms are squares, (2) middle term $=2\cdot$first$\cdot$last, (3) its sign goes into the bracket.',
        r'$a\cdot a^3=a^4$: count the factors of $a$ ($1+3=4$).',
    ]
    M.new_card('mem-r26-t04-trinomials', TOPIC, LEARN, {
        'title': 'Factoring trinomials',
        'intro': r'Find two numbers: product = last term, sum = middle term. $x^2+(p+q)x+pq=(x+p)(x+q)$',
        'tables': [{'title': '', 'head': ['Trinomial', 'Two numbers', 'Factored'], 'rows': [
            [r'$x^2+5x+6$', r'$2$ and $3$', r'$(x+2)(x+3)$'],
            [r'$x^2-7x+12$', r'$-3$ and $-4$', r'$(x-3)(x-4)$'],
            [r'$x^2+x-12$', r'$4$ and $-3$', r'$(x+4)(x-3)$'],
            [r'$x^2-x-12$', r'$-4$ and $3$', r'$(x-4)(x+3)$'],
            [r'$2x^2+10x+12$', r'take out $2$ first', r'$2(x+2)(x+3)$'],
        ]}],
        'tips': [
            r'Last term $+$: both numbers have the sign of the middle term. Last term $-$: one $+$, one $-$; the bigger one gets the sign of the middle term.',
            'Start from the pairs of the product: there are only a few.',
            r'Check with a number (not $0$ or $1$): $x=2$ in $x^2+5x+6$ gives $20=4\cdot5$.',
            r'Factor to reduce: $\frac{x^2+5x+6}{x+2}=x+3$ (for $x\ne-2$).',
        ],
    }, after=TRINOM)


# ======================================================================================================
# 5. Guided questions Q1, Q2 (text + video fixes)
# ======================================================================================================
def fix_guided(M):
    M.set_q('q-120', stem=r'$(a+b)^2-(a-b)^2=?$',
            choices=[r'$a-b$', r'$a^2-b^2$', r'$0$', r'$4ab$'],
            expl=[r'Expand both squares and keep the second one in brackets: $(a^2+2ab+b^2)-(a^2-2ab+b^2)$.',
                  r'The minus flips every sign in the second bracket: $a^2+2ab+b^2-a^2+2ab-b^2=4ab$ (choice 4).',
                  r'Check with $a=3$, $b=4$: $7^2-(-1)^2=49-1=48$, and $4\cdot3\cdot4=48$. The other choices give $-1$, $-7$ and $0$.'])
    M.set_q('q-121', stem=r'$(m-2)(m+2)-(n-2)(n+2)=?$',
            choices=[r'$4$', r'$m+n$', r'$m^2-n^2$', r'$0$'],
            expl=[r'Each product is a difference of squares: $(m-2)(m+2)=m^2-4$ and $(n-2)(n+2)=n^2-4$.',
                  r'Subtract, keeping the brackets: $(m^2-4)-(n^2-4)=m^2-4-n^2+4=m^2-n^2$ (choice 3).',
                  r'Check with $m=3$, $n=4$: $1\cdot5-2\cdot6=5-12=-7$, and $9-16=-7$.'])
    # Q1 video: move the cancel/reduce remark to the lesson; add the plug-in rule (Pass 2: twin identity removed)
    M.edit_lines('solve-q-120', 2, lambda ls: [l for l in ls if not l.get('say', '').startswith('Small nuance')])
    b = beat_to_slide(M.slide('solve-q-120', 3))
    k = b['script'].index('Check it by plugging in: a equals three, b equals four.')
    b['script'][k + 1:k + 1] = [
        'Why three and four? Choose numbers that are different from each other, and not zero or one.',
        'With a equal to b, or with zero, different choices can give the same value — and the check proves nothing.']
    M.set_slide('solve-q-120', 3, script=b['script'])


# ======================================================================================================
# 6. New guided questions Q3-Q8
# ======================================================================================================
def Qslide(qid, act, title, script):
    return dict(mode='question', active=act, title=title, pre=[Q(qid)], script=script)


def guided_new(M):
    qs = []   # (qid, video slides builder)

    # ---- Q3: x + y and xy -> x² + y²
    q3 = 'q-r26-t04-01'
    M.new_q(q3, TOPIC, G(CASES('x+y=6', 'xy=5'), r'What is the value of $x^2+y^2$?'),
            [r'$36$', r'$31$', r'$26$', r'$46$'], 3,
            [r'Square the sum: $(x+y)^2=x^2+2xy+y^2$.',
             r'Substitute: $6^2=x^2+y^2+2\cdot5$, that is, $36=x^2+y^2+10$.',
             r'Therefore $x^2+y^2=36-10=26$ (choice 3).',
             r'Check: $x=1$ and $y=5$ fit both conditions, and $1^2+5^2=1+25=26$. Choice 1 ($36$) is the trap: it forgets the middle term $2xy$.'])
    qs.append((q3, 'Given a sum and a product — find the squares.', [
        ('Method 1 · Square the sum', [
            'They give a sum and a product. They ask for squares. You know this one.',
            'Don\'t look for x and y. Square the sum.',
            D('Write "(x + y)² = x² + 2xy + y²"'),
            'x plus y, squared: x squared, plus two x y, plus y squared.',
            D('Write "36 = x² + y² + 10"'),
            'x plus y is six. Six squared: thirty-six. xy is five. Two x y: ten.',
            D('Write "x² + y² = 36 − 10 = 26" and circle choice 3'),
            'Thirty-six minus ten: twenty-six. Choice three.',
            'Here\'s the trap: thirty-six is choice one. That is what you get if you forget the middle term.',
        ]),
        ('Method 2 · Spot the numbers', [
            'A shortcut for strong students. Two numbers with sum six and product five?',
            D('Write "x = 1, y = 5: 1 + 5 = 6 ✓, 1 · 5 = 5 ✓"'),
            'One and five. Both conditions work.',
            D('Write "1² + 5² = 1 + 25 = 26"'),
            'One squared plus five squared: twenty-six. Same answer. Choice three.',
            'This works when the numbers are easy to spot. When they are not, the formula always works.',
        ]),
    ]))

    # ---- Q4: 51² − 49²
    q4 = 'q-r26-t04-02'
    M.new_q(q4, TOPIC, r'$51^2-49^2=?$', [r'$2$', r'$4$', r'$100$', r'$200$'], 4,
            [r'Use the difference of squares: $a^2-b^2=(a-b)(a+b)$.',
             r'$51^2-49^2=(51-49)(51+49)=2\cdot100=200$ (choice 4).',
             r'The long way gives the same: $2601-2401=200$. Choice 2 ($4$) is $(51-49)^2$, a different expression.'])
    qs.append((q4, 'Big squares? Look for the formula.', [
        ('Method 1 · Difference of squares', [
            'Two squares with a minus between them. That is a difference of squares.',
            D('Write "= (51 − 49)(51 + 49)"'),
            'The difference times the sum.',
            D('Write "= 2 · 100 = 200" and circle choice 4'),
            'Fifty-one minus forty-nine: two. Fifty-one plus forty-nine: one hundred. Two times one hundred: two hundred. Choice four.',
            'The trap: choice two, four. That is fifty-one minus forty-nine, squared. A different expression.',
        ]),
        ('Method 2 · The long way', [
            'Could you just square them? Yes — but look at the work.',
            D('Write "51² = 2601, 49² = 2401, 2601 − 2401 = 200"'),
            'Fifty-one squared: two thousand six hundred one. Forty-nine squared: two thousand four hundred one. The difference: two hundred.',
            'Same answer, choice four. But it took a minute, and there were many chances for a mistake.',
        ]),
    ]))

    # ---- Q5: (a − b)² = (b − a)²
    q5 = 'q-r26-t04-03'
    M.new_q(q5, TOPIC, r'Which of the following expressions is equal to $(a-b)^2$ for all values of $a$ and $b$?',
            [r'$a^2-b^2$', r'$(b-a)^2$', r'$-(b-a)^2$', r'$a^2+b^2$'], 2,
            [r'$b-a$ is the opposite of $a-b$: $b-a=-(a-b)$.',
             r'Squaring removes the minus: $(b-a)^2=(-1)^2(a-b)^2=(a-b)^2$ (choice 2).',
             r'Check with $a=5$, $b=2$: $(a-b)^2=9$. The choices give $21$, $9$, $-9$ and $29$. Only choice 2 gives $9$.',
             r'In choice 3 the minus is outside the square. Nothing removes it.'])
    qs.append((q5, 'Opposite brackets.', [
        ('Method 1 · Opposite brackets', [
            'Look at choice two. b minus a is the opposite of a minus b.',
            D('Write "b − a = −(a − b)"'),
            'Flip both signs: b minus a equals minus, a minus b.',
            D('Write "(b − a)² = (−1)² · (a − b)² = (a − b)²" and circle choice 2'),
            'Now square it. Minus one squared is one. The minus disappears. Choice two.',
            'Choice three keeps the minus OUTSIDE the square. Nothing squares it away.',
        ]),
        ('Method 2 · Plug in', [
            'Check with numbers: a equals five, b equals two. Different numbers, not zero, not one.',
            D('Write "(5 − 2)² = 9"'),
            'Five minus two, squared: nine.',
            D('Next to the choices write their values: 21, 9, −9, 29'),
            'Twenty-five minus four: twenty-one. Two minus five, squared: nine. Minus nine. Twenty-five plus four: twenty-nine.',
            D('Circle choice 2'),
            'Only choice two gives nine. Choice two.',
        ]),
    ]))

    # ---- Q6: x + 1/x = 3
    q6 = 'q-r26-t04-04'
    M.new_q(q6, TOPIC, r'Given: $x+\frac{1}{x}=3$ ($x\ne0$).' + '\n' + r'What is the value of $x^2+\frac{1}{x^2}$?',
            [r'$7$', r'$9$', r'$11$', r'$5$'], 1,
            [r'Square both sides: $\left(x+\frac{1}{x}\right)^2=3^2=9$.',
             r'Expand: $x^2+2\cdot x\cdot\frac{1}{x}+\frac{1}{x^2}=x^2+2+\frac{1}{x^2}$, because $x\cdot\frac{1}{x}=1$.',
             r'Therefore $x^2+2+\frac{1}{x^2}=9$, and $x^2+\frac{1}{x^2}=9-2=7$ (choice 1).',
             r'Choice 2 ($9$) forgets the middle term $2$; choice 3 ($11$) adds it instead of subtracting it.'])
    qs.append((q6, 'x plus one over x.', [
        ('Method 1 · Square both sides', [
            'They give x plus one over x. They ask for squares. Square both sides.',
            D('Write "(x + 1/x)² = 3² = 9"'),
            'x plus one over x, squared, equals nine.',
            D('Write "(x + 1/x)² = x² + 2 · x · (1/x) + 1/x²"'),
            'The formula: the first squared, plus two times the first times the second, plus the second squared.',
            D('Circle "x · (1/x)" and write "= 1"'),
            'x times one over x is one. The middle term is just two.',
            D('Write "x² + 2 + 1/x² = 9, x² + 1/x² = 7" and circle choice 1'),
            'Nine minus two: seven. Choice one.',
            'The trap: choice two, nine. That forgets the middle term.',
        ]),
        ('Why not find x?', [
            'Could we find x first? Try it. No nice number works — x is an ugly number with a square root.',
            'When the numbers are ugly, that is a hint: the question wants a formula.',
            'Square the sum. Subtract the middle term. Done in twenty seconds.',
        ]),
    ]))

    # ---- Q7: factor x² + x − 12
    q7 = 'q-r26-t04-05'
    M.new_q(q7, TOPIC, r'Which of the following is equal to $x^2+x-12$?',
            [r'$(x-4)(x+3)$', r'$(x+4)(x-3)$', r'$(x+6)(x-2)$', r'$(x-6)(x+2)$'], 2,
            [r'Find two numbers with product $-12$ and sum $+1$.',
             r'The product is negative: one number is positive and one is negative. Pairs of $12$: $1\cdot12$, $2\cdot6$, $3\cdot4$. Only $3$ and $4$ differ by $1$.',
             r'The sum is $+1$. Therefore the bigger one is positive: $4$ and $-3$. Therefore $x^2+x-12=(x+4)(x-3)$ (choice 2).',
             r'Check by opening: $x^2-3x+4x-12=x^2+x-12$. With $x=2$: $4+2-12=-6$ and $6\cdot(-1)=-6$.'])
    qs.append((q7, 'Sum and product.', [
        ('Method 1 · Sum and product', [
            'Two numbers. Product: minus twelve. Sum: plus one.',
            D('List the pairs of 12: "1 · 12", "2 · 6", "3 · 4"'),
            'A negative product: one number is plus, one is minus. They must differ by one. Three and four.',
            D('Write "4 + (−3) = 1 ✓" and "= (x + 4)(x − 3)"'),
            'The sum is plus one. The bigger one gets the plus. Plus four, minus three.',
            D('Circle choice 2'),
            'x plus four, times x minus three. Choice two.',
            'Choice one has the signs the other way around. That gives minus x in the middle.',
        ]),
        ('Method 2 · Plug in', [
            'Check with a number. Why not zero? Look.',
            D('Write "x = 0: every choice gives −12"'),
            'With x equal to zero, all four choices give minus twelve. Zero cannot tell them apart.',
            D('Write "x = 2: 4 + 2 − 12 = −6"'),
            'Take x equals two. The expression: four plus two minus twelve. Minus six.',
            D('Next to the choices write their values: −10, −6, 0, −16'),
            'Minus two times five: minus ten. Six times minus one: minus six. Eight times zero: zero. Minus four times four: minus sixteen.',
            D('Circle choice 2'),
            'Only choice two gives minus six. Choice two.',
        ]),
    ]))

    # ---- Q8: (x² − 9)/(x² + x − 6)
    q8 = 'q-r26-t04-06'
    M.new_q(q8, TOPIC, r'Given: $x\ne2$ and $x\ne-3$.' + '\n' + r'Which of the following is equal to $\dfrac{x^2-9}{x^2+x-6}$?',
            [r'$\dfrac{x+3}{x-2}$', r'$\dfrac{x-3}{x+2}$', r'$\dfrac{x-3}{x-2}$', r'$\dfrac{9}{6-x}$'], 3,
            [r'Factor the top (difference of squares): $x^2-9=(x-3)(x+3)$.',
             r'Factor the bottom (product $-6$, sum $+1$: the numbers $3$ and $-2$): $x^2+x-6=(x+3)(x-2)$.',
             r'Reduce the common factor $x+3$: $\frac{(x-3)(x+3)}{(x+3)(x-2)}=\frac{x-3}{x-2}$ (choice 3).',
             r'Check with $x=4$: $\frac{16-9}{16+4-6}=\frac{7}{14}=\frac{1}{2}$, and $\frac{4-3}{4-2}=\frac{1}{2}$. Choice 4 comes from crossing out $x^2$, which is not allowed: only factors can be reduced.'])
    qs.append((q8, 'Factor, then reduce.', [
        ('Method 1 · Factor, then reduce', [
            'A fraction with plus and minus signs. You cannot reduce anything yet. First factor.',
            D('Under the top write "(x − 3)(x + 3)"'),
            'The top: x squared minus nine. Difference of squares. x minus three, times x plus three.',
            D('Under the bottom write "(x + 3)(x − 2)"'),
            'The bottom: product minus six, sum plus one. Three and minus two. x plus three, times x minus two.',
            D('Cross out (x + 3) on the top and on the bottom; write "= (x − 3)/(x − 2)"'),
            'Now x plus three is a factor on the top and on the bottom. Reduce it. x minus three over x minus two.',
            D('Circle choice 3'),
            'Choice three.',
            'The trap: choice four crosses out x squared. You can never reduce across a plus or a minus. Only factors.',
        ]),
        ('Method 2 · Plug in', [
            'Check with x equals four.',
            D('Write "(16 − 9)/(16 + 4 − 6) = 7/14 = 1/2"'),
            'Top: sixteen minus nine, seven. Bottom: sixteen plus four minus six, fourteen. One half.',
            D('Next to the choices write their values: 7/2, 1/6, 1/2, 9/2'),
            'Seven over two. One over six. One over two. Nine over two.',
            D('Circle choice 3'),
            'Only choice three gives one half. Choice three.',
        ]),
    ]))
    return qs


def place_guided(M, qs):
    n0 = M.next_question_number(TOPIC)     # 3
    total = n0 - 1 + len(qs)
    side = ['Question %d' % k for k in range(1, total + 1)]
    for vid in ('solve-q-120', 'solve-q-121'): M.set_sidebar(vid, side)
    after = 'solve-q-121'
    for k, (qid, intro, parts) in enumerate(qs):
        n = n0 + k
        if qid == 'q-r26-t04-05':        # Q7, Q8 come after the trinomial lesson
            trinomial_video(M, after)
            after = TRINOM
        M.place_q(qid, LEARN, after=after)
        slides = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % ['three', 'four', 'five', 'six', 'seven', 'eight'][n - 3], intro])]
        slides += [Qslide(qid, n - 1, t, s) for t, s in parts]
        M.new_video('solve-' + qid, TOPIC, 'Expression Questions', side, slides, LEARN, kind='solution', qid=qid)
        after = 'solve-' + qid
    # solution-video titles follow the course convention: the plain question stem
    for qid in ['q-120', 'q-121'] + [q for q, _, _ in qs]:
        v = M.video('solve-' + qid); v['title'] = v['navLabel'] = M.q(qid)['stem']


# ======================================================================================================
# 7. Practice: text fixes, removals, new exam-level items, order
# ======================================================================================================
def practice(M):
    S = M.set_q
    S('q-100', stem=r'$8a+5b-3a-2b=?$', choices=[r'$3a+5b$', r'$5a+3b$', r'$5(a+b)$', r'$5a+2b$'],
      expl=[r'Collect like terms: $8a-3a=5a$ and $5b-2b=3b$. The result is $5a+3b$ (choice 2).'])
    S('q-101', stem=r'$-\sqrt{5}-7\sqrt{2}+2\sqrt{2}+3\sqrt{5}=?$',
      choices=[r'$2\sqrt{5}-7\sqrt{2}$', r'$2\sqrt{5}+5\sqrt{2}$', r'$4\sqrt{5}-5\sqrt{2}$', r'$2\sqrt{5}-5\sqrt{2}$'],
      expl=[r'Treat $\sqrt{5}$ and $\sqrt{2}$ like two different letters.',
            r'$\sqrt{5}$ terms: $-\sqrt{5}+3\sqrt{5}=2\sqrt{5}$. $\sqrt{2}$ terms: $-7\sqrt{2}+2\sqrt{2}=-5\sqrt{2}$.',
            r'Together: $2\sqrt{5}-5\sqrt{2}$ (choice 4).'])
    S('q-102', stem=r'$(-4x)\cdot6z\cdot2y=?$', choices=[r'$-xyz$', r'$-12xyz$', r'$-24xyz$', r'$-48xyz$'],
      expl=[r'Numbers with numbers: $(-4)\cdot6\cdot2=-48$. Letters with letters: $x\cdot z\cdot y=xyz$.',
            r'The result is $-48xyz$ (choice 4).'])
    S('q-103', stem=r'$5\cdot(-a)\cdot a^3\cdot(-2a)=?$', choices=[r'$-10a^5$', r'$10a^5$', r'$10a^4$', r'$-10a^4$'],
      expl=[r'Numbers: $5\cdot(-1)\cdot(-2)=10$. Two minus signs give a plus.',
            r'Letters: count the factors of $a$. $a\cdot a^3\cdot a$ has $1+3+1=5$ of them. It is $a^5$.',
            r'The result is $10a^5$ (choice 2).'])
    S('q-104', stem=r'$3x\cdot2x^2y\cdot(-4xy^2)=?$', choices=[r'$-9x^4y^3$', r'$-24x^4y^3$', r'$-24x^3y^3$', r'$-24x^3y^4$'],
      expl=[r'Numbers: $3\cdot2\cdot(-4)=-24$.',
            r'Count the factors of $x$: $x\cdot x^2\cdot x=x^4$. Count the factors of $y$: $y\cdot y^2=y^3$.',
            r'The result is $-24x^4y^3$ (choice 2).'])
    S('q-105', stem=r'$-4(3x-5)=?$', choices=[r'$-12x+20$', r'$12x-20$', r'$-12x-20$', r'$12x+20$'],
      expl=[r'The $-4$ multiplies every term: $-4\cdot3x=-12x$ and $-4\cdot(-5)=+20$.',
            r'The result is $-12x+20$ (choice 1).'])
    S('q-106', stem=r'$(x-1)(x^3+x^2+x+1)=?$', choices=[r'$x^4+1$', r'$x^4$', r'$x^4-1$', r'$1$'],
      expl=[r'Multiply $x$ by every term: $x^4+x^3+x^2+x$. Multiply $-1$ by every term: $-x^3-x^2-x-1$.',
            r'Add: $x^3$, $x^2$ and $x$ cancel in pairs. What is left is $x^4-1$ (choice 3).',
            r'Faster: plug in $x=2$. $(2-1)(8+4+2+1)=15$. The choices give $17$, $16$, $15$ and $1$. Only choice 3 gives $15$.'])
    S('q-107', stem=r'$(p-q)-(q-p)=?$', choices=[r'$0$', r'$2p-2q$', r'$-2q$', r'$2p$'],
      expl=[r'The minus before the second bracket flips both signs: $p-q-q+p$.',
            r'Collect: $2p-2q$ (choice 2).'])
    S('q-110', stem=r'$(m-n)-\big(-n-(-m)\big)=?$', choices=[r'$0$', r'$2m-2n$', r'$-2n$', r'$2m$'],
      expl=[r'Work from the inside out: $-(-m)=+m$. The second bracket is $-n+m$.',
            r'Then $(m-n)-(-n+m)=m-n+n-m=0$ (choice 1).'])
    S('q-112', stem=r'$3(x+3)^2=?$', choices=[r'$3x^2+27$', r'$9x^2+81$', r'$3x^2+18x+27$', r'$9x^2+54x+81$'], correct=3,
      expl=[r'Power first: $(x+3)^2=x^2+6x+9$.',
            r'Then multiply every term by $3$: $3x^2+18x+27$ (choice 3).',
            r'Choice 4 is $(3x+9)^2$: it puts the $3$ inside the square. That is a mistake.'])
    S('q-113', stem=r'Which of the following is equal to $x^2+14x+49$?',
      choices=[r'$(x+4)^2$', r'$(x+14)^2$', r'$7(x+2)^2$', r'$(x+7)^2$'],
      expl=[r'Check the perfect-square pattern: $49=7^2$, and the middle term is $2\cdot x\cdot7=14x$.',
            r'Both checks pass. Therefore $x^2+14x+49=(x+7)^2$ (choice 4).'])
    S('q-114', stem=r'$(2x-3)^2=?$', choices=[r'$4x^2-9$', r'$4x^2+9$', r'$4x^2-12x-9$', r'$4x^2-12x+9$'],
      expl=[r'Use $(a-b)^2=a^2-2ab+b^2$ with $a=2x$ and $b=3$.',
            r'$(2x)^2=4x^2$, $2\cdot2x\cdot3=12x$, $3^2=9$. The result is $4x^2-12x+9$ (choice 4).'])
    S('q-115', stem=r'$(a-b)^2-(a+b)^2=?$', choices=[r'$2a^2-2b^2$', r'$0$', r'$4ab$', r'$-4ab$'],
      expl=[r'Expand both squares and keep the second in brackets: $(a^2-2ab+b^2)-(a^2+2ab+b^2)$.',
            r'Open the brackets: $a^2-2ab+b^2-a^2-2ab-b^2=-4ab$ (choice 4).',
            r'Check with $a=3$, $b=1$: $4-16=-12$, and $-4\cdot3\cdot1=-12$.'])
    S('q-116', stem=r'Which of the following is equal to $4x^2+49-28x$?',
      choices=[r'$2(x-7)^2$', r'$(-2x-7)^2$', r'$(2x-7)^2$', r'$2(-x-7)^2$'],
      expl=[r'Put the terms in order: $4x^2-28x+49$.',
            r'Check: $4x^2=(2x)^2$ and $49=7^2$. The middle term: $2\cdot2x\cdot7=28x$, with a minus.',
            r'Therefore $4x^2-28x+49=(2x-7)^2$ (choice 3).'])
    S('q-118', stem=r'$4(x-3)(x+3)=?$', choices=[r'$4x^2-36$', r'$4x^2+36$', r'$4x^2-24x-36$', r'$4x^2-12x-36$'],
      expl=[r'Brackets first, with the difference of squares: $(x-3)(x+3)=x^2-9$.',
            r'Then multiply by $4$: $4x^2-36$ (choice 1).'])
    S('q-119', stem=r'Which of the following is equal to $16-9x^2$?',
      choices=[r'$(4+3x)^2$', r'$(4-\sqrt{3}x)(4+\sqrt{3}x)$', r'$(4-3x)^2$', r'$(4-3x)(4+3x)$'],
      expl=[r'A difference of squares: $16=4^2$ and $9x^2=(3x)^2$.',
            r'Therefore $16-9x^2=(4-3x)(4+3x)$ (choice 4).'])
    S('alg-extra-unit-t4-1-1', stem=r'$3x+5y-2x-3y=?$', choices=[r'$x+8y$', r'$3xy$', r'$x+2y$', r'$5x+8y$'],
      expl=[r'Collect like terms: $3x-2x=x$ and $5y-3y=2y$.', r'The result is $x+2y$ (choice 3).'])
    S('alg-extra-unit-t4-1-2', stem=r'$3(x+4)-2(x+1)=?$', choices=[r'$x+10$', r'$x+8$', r'$5x+10$', r'$x+13$'],
      expl=[r'Open both brackets. The $-2$ multiplies both terms: $3x+12-2x-2$.',
            r'Collect: $3x-2x=x$ and $12-2=10$. The result is $x+10$ (choice 1).'])
    S('alg-extra-unit-t4-1-3', stem=r'Which of the following is equal to $x^2+8x+15$?',
      choices=[r'$(x+2)(x+6)$', r'$(x-3)(x-5)$', r'$(x+1)(x+15)$', r'$(x+3)(x+5)$'],
      expl=[r'Find two numbers with product $15$ and sum $8$. Pairs of $15$: $1\cdot15$ (sum $16$), $3\cdot5$ (sum $8$).',
            r'Both are positive, because the last term and the middle term are positive. $x^2+8x+15=(x+3)(x+5)$ (choice 4).',
            r'Check by opening: $x^2+5x+3x+15=x^2+8x+15$.'])
    S('alg-extra-unit-t4-1-4', stem=r'Given: $x\ne3$.' + '\n' + r'Which of the following is equal to $\frac{x^2-9}{x-3}$?',
      choices=[r'$x$', r'$2x+3$', r'$x+3$', r'$x-3$'],
      expl=[r'Factor the top: $x^2-9=(x-3)(x+3)$.',
            r'Reduce $x-3$ (it is not zero): $\frac{(x-3)(x+3)}{x-3}=x+3$ (choice 3).'])
    S('alg-extra-unit-t4-1-5', stem=r'$97\cdot103=?$', choices=[r'$9997$', r'$9991$', r'$10009$', r'$9994$'],
      expl=[r'$97$ and $103$ are both $3$ away from $100$: $97\cdot103=(100-3)(100+3)$.',
            r'Difference of squares: $100^2-3^2=10000-9=9991$ (choice 2).'])
    S('alg-extra-unit-t4-1-6', stem=r'$(u+v)(w-3)+(u+v)(w+3)=?$', choices=[r'$0$', r'$2w(u+v)$', r'$6(u+v)$', r'$2w+u+v$'],
      expl=[r'The bracket $u+v$ is a common factor: $(u+v)\big[(w-3)+(w+3)\big]$.',
            r'Inside: $w-3+w+3=2w$. The result is $2w(u+v)$ (choice 2).'])
    S('alg-extra-unit-t4-1-7', stem=r'Given: $x\ne0$.' + '\n' + r'Which of the following is equal to $\frac{3x^2+15x}{3x}$?',
      choices=[r'$x+5$', r'$3x+5$', r'$x+15$', r'$x^2+5$'],
      expl=[r'Take out the common factor $3x$ on the top: $3x^2+15x=3x(x+5)$.',
            r'Reduce $3x$: $\frac{3x(x+5)}{3x}=x+5$ (choice 1).'])

    # Pass 2: the original q-108, q-109, q-111, q-117 stay (only text clean-up)
    S('q-108', stem=r'$(3a-b)-(-b+3a)=?$', choices=[r'$6a$', r'$6a-2b$', r'$-2b$', r'$0$'],
      expl=[r'The two brackets hold the same expression: $-b+3a$ is $3a-b$ written in the other order.',
            r'The minus flips both signs of the second bracket: $3a-b+b-3a=0$ (choice 4).'])
    S('q-109', stem=r'$(-q+p)-(-p-q)=?$', choices=[r'$2p$', r'$-2q$', r'$2p-2q$', r'$0$'],
      expl=[r'The minus flips both signs of the second bracket: $-q+p+p+q$.',
            r'The q terms cancel and the p terms add up: $2p$ (choice 1).'])
    S('q-111', stem=r'$(3x+4)^2=?$', choices=[r'$9x^2+16$', r'$9x^2+16+12x$', r'$9x^2+16+24x$', r'$9x^2+16+48x$'],
      expl=[r'Use $(a+b)^2=a^2+2ab+b^2$ with $a=3x$ and $b=4$.',
            r'$(3x)^2=9x^2$, $2\cdot3x\cdot4=24x$, $4^2=16$. The result is $9x^2+24x+16$ (choice 3).'])
    S('q-117', stem=r'$(x-8)(x+8)=?$', choices=[r'$x^2-64$', r'$x^2+64$', r'$x^2-64-16x$', r'$x^2-64-64x$'],
      expl=[r'Difference of squares: $(a-b)(a+b)=a^2-b^2$ with $a=x$ and $b=8$.',
            r'$x^2-8^2=x^2-64$ (choice 1). There is no middle term.'])

    # new exam-level practice
    N = lambda n: 'q-r26-t04-%02d' % n
    new = [
        (7, G(CASES('a-b=3', 'ab=4'), r'What is the value of $a^2+b^2$?'), [r'$1$', r'$17$', r'$13$', r'$25$'], 2,
         [r'Square the difference: $(a-b)^2=a^2-2ab+b^2$.',
          r'Substitute: $9=a^2+b^2-8$. Therefore $a^2+b^2=9+8=17$ (choice 2).',
          r'Check: $a=4$, $b=1$ fit both conditions, and $16+1=17$.']),
        (8, G(CASES('x+y=8', 'x-y=2'), r'What is the value of $x^2-y^2$?'), [r'$16$', r'$10$', r'$60$', r'$6$'], 1,
         [r'Difference of squares: $x^2-y^2=(x+y)(x-y)=8\cdot2=16$ (choice 1).',
          r'Check: $x=5$, $y=3$ fit both conditions, and $25-9=16$.']),
        (9, r'$1001^2-999^2=?$', [r'$2$', r'$4$', r'$2000$', r'$4000$'], 4,
         [r'Difference of squares: $(1001-999)(1001+999)=2\cdot2000=4000$ (choice 4).']),
        (10, r'Given: $x+\frac{1}{x}=4$ ($x\ne0$).' + '\n' + r'What is the value of $x^2+\frac{1}{x^2}$?',
         [r'$16$', r'$18$', r'$14$', r'$8$'], 3,
         [r'Square both sides: $x^2+2+\frac{1}{x^2}=16$, because $2\cdot x\cdot\frac{1}{x}=2$.',
          r'Therefore $x^2+\frac{1}{x^2}=16-2=14$ (choice 3).']),
        (11, r'Which of the following is equal to $x^2-2x-15$?',
         [r'$(x+5)(x-3)$', r'$(x-5)(x+3)$', r'$(x-5)(x-3)$', r'$(x-15)(x+1)$'], 2,
         [r'Find two numbers with product $-15$ and sum $-2$.',
          r'A negative product: one number is positive, one is negative. $3$ and $5$ differ by $2$; the bigger one gets the minus: $-5$ and $3$.',
          r'Therefore $x^2-2x-15=(x-5)(x+3)$ (choice 2). Check: $x^2+3x-5x-15=x^2-2x-15$.']),
        (12, r'Which of the following is equal to $x^2-7x+12$?',
         [r'$(x+3)(x+4)$', r'$(x-2)(x-6)$', r'$(x-3)(x-4)$', r'$(x-1)(x-12)$'], 3,
         [r'Find two numbers with product $12$ and sum $-7$. Positive product, negative sum: both numbers are negative.',
          r'Pairs of $12$: $1\cdot12$, $2\cdot6$, $3\cdot4$. Only $3+4=7$. The numbers are $-3$ and $-4$.',
          r'Therefore $x^2-7x+12=(x-3)(x-4)$ (choice 3).']),
        (13, r'Given: $x\ne2$ and $x\ne-2$.' + '\n' + r'Which of the following is equal to $\dfrac{x^2+x-6}{x^2-4}$?',
         [r'$\dfrac{x+3}{x+2}$', r'$\dfrac{x-3}{x+2}$', r'$\dfrac{x+3}{x-2}$', r'$\dfrac{6-x}{4}$'], 1,
         [r'Top: product $-6$, sum $+1$. The numbers are $3$ and $-2$: $x^2+x-6=(x+3)(x-2)$.',
          r'Bottom: difference of squares: $x^2-4=(x-2)(x+2)$.',
          r'Reduce $x-2$: $\frac{(x+3)(x-2)}{(x-2)(x+2)}=\frac{x+3}{x+2}$ (choice 1).',
          r'Check with $x=3$: $\frac{9+3-6}{9-4}=\frac{6}{5}$, and $\frac{3+3}{3+2}=\frac{6}{5}$.']),
        (14, r'$(2a+b)^2-(2a-b)^2=?$', [r'$8ab$', r'$4ab$', r'$2b^2$', r'$8a^2$'], 1,
         [r'Expand: $(4a^2+4ab+b^2)-(4a^2-4ab+b^2)=4ab+4ab=8ab$ (choice 1).',
          r'Check with $a=2$, $b=1$: $5^2-3^2=16$, and $8\cdot2\cdot1=16$. The other choices give $8$, $2$ and $32$.']),
        (15, G(CASES('(a+b)^2=49', '(a-b)^2=9'), r'What is the value of $ab$?'), [r'$40$', r'$10$', r'$20$', r'$29$'], 2,
         [r'Subtract the two expansions: $(a+b)^2-(a-b)^2=4ab$.',
          r'So $4ab=49-9=40$, and $ab=10$ (choice 2).',
          r'Check: $a=5$, $b=2$ give $(a+b)^2=49$ and $(a-b)^2=9$, and $ab=10$.']),
        (16, r'$\dfrac{2021^2-2019^2}{2020}=?$', [r'$1$', r'$2$', r'$4$', r'$2020$'], 3,
         [r'Difference of squares on the top: $(2021-2019)(2021+2019)=2\cdot4040$.',
          r'Divide: $\frac{2\cdot4040}{2020}=2\cdot2=4$ (choice 3).']),
        (17, r'Given: $x-y=5$.' + '\n' + r'What is the value of $x^2-2xy+y^2-2x+2y$?', [r'$15$', r'$35$', r'$25$', r'$20$'], 1,
         [r'Group: $x^2-2xy+y^2=(x-y)^2$ and $-2x+2y=-2(x-y)$.',
          r'Substitute: $5^2-2\cdot5=25-10=15$ (choice 1).',
          r'Check with $x=5$, $y=0$: $25-0+0-10+0=15$.']),
        (18, G(CASES('x^2-y^2=24', 'x+y=6'), r'What is the value of $x$?'), [r'$4$', r'$5$', r'$1$', r'$3$'], 2,
         [r'Difference of squares: $x^2-y^2=(x+y)(x-y)$. Therefore $24=6(x-y)$ and $x-y=4$.',
          r'Add the two equations $x+y=6$ and $x-y=4$: $2x=10$ and $x=5$ (choice 2).',
          r'Check: $y=1$, and $25-1=24$.']),
        (19, r'For every $x$, $(x+3)^2-(x-3)(x+3)=?$', [r'$18$', r'$6x+18$', r'$6x$', r'$2x^2+6x+18$'], 2,
         [r'Expand: $(x+3)^2=x^2+6x+9$ and $(x-3)(x+3)=x^2-9$.',
          r'Subtract, keeping brackets: $x^2+6x+9-(x^2-9)=6x+18$ (choice 2).',
          r'Faster: plug in $x=1$. $16-(-2)(4)=16+8=24$. The choices give $18$, $24$, $6$ and $26$. Only choice 2 gives $24$.']),
    ]
    for n, stem, ch, cor, ex in new:
        M.new_q(N(n), TOPIC, stem, ch, cor, ex)
        M.place_q(N(n), PRACTICE)

    order = ['q-100', 'alg-extra-unit-t4-1-1', 'q-102', 'q-103', 'q-104', 'q-101', 'q-105', 'alg-extra-unit-t4-1-2',
             'q-107', 'q-108', 'q-109', 'q-110', 'q-111', 'q-114', 'q-117', 'q-112', 'q-118', 'q-113', 'q-116', 'q-119', 'alg-extra-unit-t4-1-5',
             'alg-extra-unit-t4-1-6', 'alg-extra-unit-t4-1-7', 'alg-extra-unit-t4-1-4', 'q-115', 'q-106',
             'alg-extra-unit-t4-1-3', N(12), N(11), N(8), N(9), N(7), N(10), N(14), N(19),
             N(13), N(16), N(15), N(18), N(17)]
    M.practice_order(PRACTICE, order)


# ======================================================================================================
# 8. Pass 2: summary video right before the practice
# ======================================================================================================
def summary(M):
    sb = ['Like terms', 'Brackets', 'Common factor', 'The three formulas', 'Formula traps', 'Number shortcuts',
          'Value without x', 'Trinomials', 'Before you practice']
    C = lambda i, title, script: dict(title=title, mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice, let's review the whole topic in a few minutes.",
            'The rules, the formulas, and the traps.']),
        C(0, 'Like terms', [
            'Add and subtract only like terms. Same letters, same powers.',
            A('Like terms example', T(r'$9a+7b-4a-3b=5a+4b$', size=50)),
            A('Roots example', T(r'$5\sqrt{3}-2\sqrt{3}=3\sqrt{3}$', size=50)),
            'Roots behave like letters. Root three is one family.',
            A('Multiplying terms', T(r'$4a\cdot5a=20a^2\qquad a^2\cdot a^3=a^5$', size=50)),
            'Multiplying? Numbers with numbers, letters with letters. Count the factors.']),
        C(1, 'Brackets', [
            'Opening brackets.',
            A('Minus before a bracket', T(r'$-(b-c)=-b+c$', size=50)),
            'A minus before a bracket flips every sign inside.',
            A('Two brackets', T(r'$(x-3)(x+7)=x^2+7x-3x-21=x^2+4x-21$', size=46)),
            'Two brackets: every term meets every term. Keep each sign glued to its number.']),
        C(2, 'Common factor', [
            'Taking out a common factor: the big tool of this topic.',
            A('Number factor', T(r'$8x+12=4(2x+3)$', size=50)),
            A('Bracket factor', T(r'$x(a-b)+4(a-b)=(a-b)(x+4)$', size=50)),
            'The common factor can be a number, a letter, or a whole bracket.',
            A('Reduce needs a product', T(r'$\dfrac{2x^2+8x}{2x}=\dfrac{2x(x+4)}{2x}=x+4$', size=50)),
            'In a fraction, reduce only a common factor. Factor first, then reduce.']),
        C(3, 'The three formulas', [
            'The three short multiplication formulas. Know them cold.',
            A('(a + b)²', T(r'$(a+b)^2=a^2+2ab+b^2$', size=48)),
            A('(a − b)²', T(r'$(a-b)^2=a^2-2ab+b^2$', size=48)),
            A('(a − b)(a + b)', T(r'$(a-b)(a+b)=a^2-b^2$', size=48)),
            'Forward to expand. Backward to factor.']),
        C(4, 'Formula traps', [
            'Three traps.',
            A('Middle term', T(r'$(a+b)^2\ne a^2+b^2$', size=48)),
            'Don\'t forget the middle term, two a b.',
            A('Power first', T(r'$2(x+4)^2=2(x^2+8x+16)=2x^2+16x+32$', size=46)),
            'Power first. The two waits outside the square.',
            A('Minus and square', T(r'For $x=6$: $-x^2=-36$, but $(-x)^2=36$', size=46)),
            'In minus x squared, only x is squared.']),
        C(5, 'Number shortcuts', [
            'The formulas work with plain numbers too.',
            A('95 · 105', T(r'$95\cdot105=100^2-5^2=10000-25=9975$', size=46)),
            A('52² − 48²', T(r'$52^2-48^2=(52-48)(52+48)=4\cdot100=400$', size=46)),
            'No big multiplications at all.',
            A('Perfect-square check', T(r'$4x^2-20x+25=(2x-5)^2$ because $2\cdot2x\cdot5=20x$', size=44)),
            'Perfect square? First and last terms are squares, and the middle term is two times first times last.']),
        C(6, 'Value without x', [
            'They give a sum and a product? Don\'t look for the letters.',
            A('a² + b²', T(r'$a^2+b^2=(a+b)^2-2ab$', size=48)),
            'a plus b is eight, a b is twelve: sixty-four minus twenty-four, forty.',
            A('a² − b²', T(r'$a^2-b^2=(a+b)(a-b)$', size=48)),
            A('x + 1/x', T(r'$\left(x+\frac{1}{x}\right)^2=x^2+2+\frac{1}{x^2}$', size=48)),
            'Know x plus one over x? Square it, then subtract two.']),
        C(7, 'Trinomials', [
            'Factoring a trinomial: find two numbers.',
            A('The rule', T('Product = last term · Sum = middle term', size=44)),
            A('Example', T(r'$x^2+9x+14=(x+2)(x+7)$', size=50)),
            'Start from the pairs of the product. Two times seven is fourteen, two plus seven is nine.',
            A('Signs', T(r'$x^2+x-20=(x+5)(x-4)$', size=50)),
            'Last term negative: one plus, one minus. Take out a common factor first, if there is one.']),
        C(8, 'Before you practice', [
            'Before you practice, always ask yourself:',
            A('Check 1', T('1. Is there a common factor to take out first?', size=42)),
            A('Check 2', T('2. Do I see one of the three formulas — forward or backward?', size=42)),
            A('Check 3', T('3. Can I find the value without finding x?', size=42)),
            A('Check 4', T('4. Check with a number: different numbers, not 0 or 1', size=42)),
            'And watch the traps: the lost middle term, a minus before a bracket, and the power that comes first.',
            'You know all of this. Go practice.']),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    M.new_video('r26-t04-summary', TOPIC, 'Expressions: Summary', sb, slides, LEARN, after=last)


def apply(M):
    fb = fix_lesson(M)
    formulas_video(M, fb)
    fix_guided(M)
    qs = guided_new(M)
    place_guided(M, qs)
    cards(M)
    practice(M)
    summary(M)
    # the formulas card comes right after the formulas video (it already follows it in the flow)
