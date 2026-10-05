"""Topic 16 - Integers. Course review 2026-09 fixes.
See t16_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q
import math_api

TOPIC = 16
SIGNS = 'whole-numbers'
CONSEC = 'consecutive-integers'
PARITY = 'parity'
PROD = 'consecutive-products'
SUMS = 'r26-t16-consecutive-sums'
THEORY = 'whole-numbers-theory'
PRACTICE = 'unit-t16-3'

G1, G2, G3, G4 = ['q-r26-t16-%02d' % k for k in (1, 2, 3, 4)]
THEORY_SOLVES = ['solve-q-457', 'solve-q-458', 'solve-q-459', 'solve-q-460', 'solve-q-461', 'solve-q-462',
                 'solve-q-463', 'solve-q-464']


def _script(M, vid, n):
    """Current script of a slide in DSL form (so lines can be appended)."""
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _replace_say(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if l.get('say') == old: l['say'] = new
        return lines
    assert any(l.get('say') == old for l in M.slide(vid, n)['lines']), (vid, n, old)
    M.edit_lines(vid, n, fn)


def _division_signs(M, vid):
    """' : ' used as division in draw notes / labels -> ' ÷ '."""
    v = M.video(vid)
    for b in v['beats']:
        for l in b['lines']:
            for key in ('draw', 'label'):
                if key in l: l[key] = l[key].replace(' : ', ' ÷ ')
    M.touched_videos.add(vid)


def _solution(M, qid, intro_line, slides):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % math_api._word(n), intro_line])]
    for title, script in slides:
        beats.append(dict(mode='question', active=0, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Integer Questions', ['Question 1'], beats, M.section_of(qid),
                    kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Integer Questions'
    v['hybrid']['num'] = 51
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Signs video: division with ÷, new slide "Signs of sums", "Never negative" (+ odd powers, zero)
    # =====================================================================================
    M.set_slide(SIGNS, 4, script=[
        "Division? Exactly the same as multiplication. Nothing more to remember.",
        A('(−12) ÷ (−3) appears', T('$(-12)\\div(-3)$', size=56, gap=60)),
        D('Write "= +4"'),
        "Same signs — positive. Plus four.",
        A('(−12) ÷ 3 appears', T('$(-12)\\div3$', size=56, gap=60)),
        D('Write "= −4"'),
        "Different signs — negative. Minus four.",
    ])
    M.set_slide(SIGNS, 5, title='Never negative', active=4, script=[
        "Four facts you'll use in every sign question.",
        A('Even power: x² ≥ 0 appears', T('Even power: $x^2\\ge0$', size=46)),
        "A number to an even power is never negative — whatever the sign of the base. It is zero only when the base is zero.",
        A('Odd power keeps the sign appears', T('Odd power keeps the sign: $(-2)^3=-8$', size=46)),
        "An odd power keeps the sign. Minus two cubed is minus eight.",
        A('|y| > 0 when y ≠ 0 appears', T('Absolute value: $|y|>0$ when $y\\ne0$', size=46)),
        "An absolute value is zero or positive. And if y isn't zero — it's strictly positive.",
        A('x < 0 ⇒ −x > 0 appears', T('$x<0\\ \\Rightarrow\\ -x>0$', size=46)),
        D('Circle the minus in "−x"'),
        "And a minus in front of a letter doesn't mean negative. It means the opposite. If x is minus seven, minus x is plus seven.",
        "One more: zero is neither positive nor negative.",
        "In the question coming up: find the pieces that are surely positive — then the piece that decides the sign.",
    ])
    M.set_slide(SIGNS, 6, active=5, script=[
        "Let's lock it in.",
        A("'Same signs + · different signs −' appears", T('Same signs $+$ · different signs $-$ (for $\\times$ and $\\div$)', size=40)),
        A("'Count only the minuses' appears", T('Count only the minuses: odd $\\to\\ -$, even $\\to\\ +$', size=40)),
        A("'Sums: mixed signs, the bigger size wins' appears", T('Sums: two negatives $\\to\\ -$ · mixed signs: the bigger size wins', size=40)),
        A("'Even powers never negative, odd powers keep the sign' appears", T('Even powers and $|x|$: never negative · odd powers keep the sign', size=40)),
        "Multiplying and dividing: count the minuses. Adding: look at the sizes.",
        "Two questions next — then consecutive numbers.",
    ])
    M.insert_slides(SIGNS, 4, [dict(mode='concept', active=3, title='Signs of sums', script=[
        "Now adding. Here the rules are different — careful.",
        A('(+) + (+) → + appears', T('$(+)+(+)\\ \\to\\ +$', size=48, gap=30)),
        A('(−) + (−) → − appears', T('$(-)+(-)\\ \\to\\ -$', size=48, gap=50)),
        "Two positives: positive. Two negatives: negative. Minus three plus minus four is minus seven.",
        "With multiplication, two minuses made a plus. Not here! Adding negatives only goes further down.",
        A('Mixed signs: the bigger size wins appears', T('Mixed signs: the bigger size wins', size=46, gap=30)),
        A('−7 + 3 = −4 and 7 + (−3) = 4 appear', T('$-7+3=-4 \\qquad 7+(-3)=4$', size=48, gap=50)),
        "Mixed signs? Look at the sizes — the numbers without their signs.",
        D('Circle the 7 in each example'),
        "Minus seven plus three: seven is bigger in size, and it's negative. So the result is negative: minus four.",
        "Seven plus minus three: now the seven is positive. Plus four.",
        A('Bigger − smaller > 0 appears', T('Bigger $-$ smaller $>0$ · smaller $-$ bigger $<0$', size=42)),
        "And a difference: bigger minus smaller is always positive. Even when both are negative.",
        D('Write "−2 − (−5) = −2 + 5 = 3"'),
        "Minus two is bigger than minus five. Minus two minus minus five: plus three.",
    ])])
    M.set_sidebar(SIGNS, ['Sign rules', 'Count the minuses', 'Dividing', 'Signs of sums', 'Never negative', 'Recap'])

    c = M.card('mem-signs')
    c['intro'] = 'Multiplication and division share the same sign rules. Addition has its own rules.'
    c['tables'] = [
        {'title': 'Multiply and divide', 'head': ['Signs', 'Result'], 'rows': [
            ['same (+·+ or −·−)', 'positive'], ['different (+·− or −·+)', 'negative'], ['one factor is 0', '0']]},
        {'title': 'Add', 'head': ['Signs', 'Result'], 'rows': [
            ['positive + positive', 'positive'], ['negative + negative', 'negative'],
            ['mixed signs', 'the sign of the number that is bigger in size: $-7+3=-4$']]},
    ]
    c['tips'] = [
        'Count only the minus signs: odd count → negative, even count → positive.',
        'Even powers and $|x|$ are never negative. Odd powers keep the sign: $(-2)^3=-8$.',
        'Bigger minus smaller is positive, even for negative numbers: $-2-(-5)=3$.',
        '$-x$ means "the opposite of $x$", not "a negative number".',
        'Zero is neither positive nor negative.',
    ]

    # Q1 video: "always" was too strong
    _replace_say(M, 'solve-q-457', 2,
                 "Why does it say y isn't zero? So the denominator isn't zero. The exam always gives you that restriction.",
                 "Why does it say y isn't zero? So the denominator isn't zero. The exam usually states it.")

    # =====================================================================================
    # 2. New guided question: sign of a sum (after Q1)
    # =====================================================================================
    M.new_q(G1, TOPIC, 'Given:\n$\\begin{cases} x<0<y \\\\ x+y>0 \\end{cases}$\nWhich of the following is necessarily true?',
            ['$|x|>|y|$', '$|y|>|x|$', '$xy>0$', '$x-y>0$'], 2, [
        'x is negative and y is positive: mixed signs. In a sum with mixed signs, the number that is bigger in size wins.',
        'The sum is positive, so the positive number y is bigger in size: $|y|>|x|$.',
        'The others: (1) is the opposite. (3) Mixed signs give a negative product: $xy<0$. (4) $x-y$ is smaller minus bigger, so it is negative.',
        'Check: $x=-1$, $y=3$. Then $x+y=2>0$, and $|3|>|-1|$ ✓.'])
    M.place_q(G1, THEORY, after='solve-q-457')
    _solution(M, G1, "A sum with mixed signs.", [
        ('Mixed signs', [
            "x is negative, y is positive. Mixed signs.",
            "In a sum with mixed signs, the number that's bigger in size wins.",
            "The sum is positive. So the winner is the positive one — y.",
            D('Write "|y| > |x|"'),
            "y is bigger in size.",
            D('Circle choice 2'),
            "Choice two. Choice one is the trap — it's the opposite.",
            D('Next to choice 3 write "(−)(+) = −" and cross it out'),
            "Choice three: mixed signs multiply to a negative. Out.",
            D('Next to choice 4 write "smaller − bigger < 0" and cross it out'),
            "Choice four: x minus y is smaller minus bigger. Negative. Out.",
        ]),
        ('Check with numbers', [
            "Quick check with numbers.",
            D('Write "x = −1, y = 3: −1 + 3 = 2 > 0 ✓"'),
            "x is minus one, y is three. The sum is two — positive. It fits the givens.",
            D('Write "|−1| = 1 < 3"'),
            "And three is bigger in size than minus one. Choice two again.",
            "But one example doesn't prove \"necessarily\". The rule does: mixed signs — the bigger size wins.",
        ]),
    ])

    # =====================================================================================
    # 3. Consecutive video: plug-in check; new lesson "Sums of Consecutive Integers" + 2 guided questions
    # =====================================================================================
    sc = _script(M, CONSEC, 4)
    sc.insert(sc.index("I prefer the smallest numbers. Less arithmetic.") + 1,
              "One check first: the choices must give different values. If two choices tie, choose other numbers.")
    M.set_slide(CONSEC, 4, script=sc)
    M.card('mem-consecutive')['tips'] = [
        'Smaller minus bigger is negative: $b-a=1$ but $a-b=-1$.',
        '"Greater than 0" does not mean the list starts at 1.',
        'Plugging in? First check that the choices give different values. If two choices tie, choose other numbers.',
    ]

    sb = ['Count × middle', 'Even count', 'Divisible by the count?', 'Counting integers', 'Squares of neighbors', 'Recap']
    M.new_video(SUMS, TOPIC, 'Sums of Consecutive Integers', sb, [
        dict(mode='title', title='Sums of Consecutive Integers', script=[
            "Adding consecutive numbers.",
            "One rule does almost all the work. Then a trap, and a counting rule.",
        ]),
        dict(mode='concept', active=0, title='Count × middle', script=[
            A('11 + 12 + 13 + 14 + 15 appears', T('$11+12+13+14+15$', size=56, gap=40)),
            "Adding consecutive numbers? Don't add them one by one.",
            "Take the middle one: thirteen.",
            D('Draw arrows: 11 and 15 → 13, 12 and 14 → 13'),
            "Eleven is two below thirteen. Fifteen is two above. Together they're like two thirteens. Same for twelve and fourteen.",
            A('= 5 · 13 = 65 appears', T('$=5\\cdot13=65$', size=56, gap=50)),
            "So the sum is five thirteens: sixty-five.",
            A('Sum = count × middle appears', T('Sum $=$ count $\\times$ middle', size=50)),
            "Sum equals count times middle. And backwards: the sum divided by the count gives the middle.",
            "It works for consecutive even or odd numbers too.",
        ]),
        dict(mode='concept', active=1, title='Even count', script=[
            A('11 + 12 + 13 + 14 appears', T('$11+12+13+14$', size=56, gap=40)),
            "Four numbers? There's no single middle number.",
            "The middle is halfway between the two middle numbers: twelve and thirteen. Twelve and a half.",
            A('middle 12.5 → 4 · 12.5 = 50 appears', T('middle $=12.5\\ \\to\\ 4\\cdot12.5=50$', size=50)),
            "Four times twelve and a half: fifty.",
            D('Write "11 + 12 + 13 + 14 = 50 ✓"'),
            "Check: eleven plus twelve plus thirteen plus fourteen — fifty.",
        ]),
        dict(mode='concept', active=2, title='Divisible by the count?', script=[
            "Here's a trap the exam loves.",
            A('Odd count: divisible by the count appears', T('Odd count (3, 5, 7): the sum divides by the count', size=42, gap=40)),
            "An odd count of consecutive integers — three, five, seven. The middle is a whole number.",
            "So the sum is the count times a whole number. It always divides by the count.",
            D('Write "4 + 5 + 6 = 15 = 3 · 5"'),
            A('Even count: never appears', T('Even count (2, 4, 6): the sum NEVER divides by the count', size=42, gap=40)),
            "An even count — the middle ends in a half.",
            A('4a + 6 appears', T('$a+(a+1)+(a+2)+(a+3)=4a+6$', size=46)),
            "Four in a row: four a plus six. Four a divides by four — six doesn't. A multiple of four, plus two.",
            D('Write "1 + 2 + 3 + 4 = 10,  2 + 3 + 4 + 5 = 14"'),
            "Ten, fourteen. Even — but never divisible by four.",
            "This is for consecutive integers. Consecutive even numbers behave differently — check with numbers.",
        ]),
        dict(mode='concept', active=3, title='Counting integers', script=[
            "How many integers are there from three to ten?",
            "Ten minus three is seven. But that's wrong.",
            A('3, 4, 5, 6, 7, 8, 9, 10 appears', T('$3,\\ 4,\\ 5,\\ 6,\\ 7,\\ 8,\\ 9,\\ 10$', size=50, gap=40)),
            D('Number them 1 to 8'),
            "Count them: eight. Subtracting counts the gaps, not the numbers. Add one.",
            A('From a to b: b − a + 1 appears', T('From $a$ to $b$: $b-a+1$ integers', size=48, gap=40)),
            "Only even numbers, or only odd? Count the steps of two, then add one.",
            A('Evens from 4 to 20 appears', T('Evens from $4$ to $20$: $\\frac{20-4}{2}+1=9$', size=48)),
            "Four to twenty: sixteen over two is eight steps. Plus one: nine even numbers.",
        ]),
        dict(mode='concept', active=4, title='Squares of neighbors', script=[
            "One shortcut for strong students.",
            A('b² − a² = (b − a)(b + a) appears', T('$b^2-a^2=(b-a)(b+a)$', size=50, gap=40)),
            "a and b are consecutive, and b is bigger. b squared minus a squared: the third multiplication formula.",
            A('b − a = 1 → b² − a² = a + b appears', T('Consecutive: $b-a=1\\ \\to\\ b^2-a^2=a+b$', size=48, gap=40)),
            "b minus a is one. So b squared minus a squared is just a plus b.",
            A('5² − 4² = 9 = 4 + 5 appears', T('$5^2-4^2=25-16=9=4+5$', size=50)),
            "Five squared minus four squared: nine. Four plus five: nine.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            "Let's lock it in.",
            A("'Sum = count × middle' appears", T('Sum $=$ count $\\times$ middle', size=42)),
            A("'Odd count / even count' appears", T('Consecutive integers: odd count $\\to$ divides by the count · even count $\\to$ never', size=38)),
            A("'From a to b: b − a + 1' appears", T('From $a$ to $b$: $b-a+1$ integers', size=42)),
            A("'Neighbors: b² − a² = a + b' appears", T('Neighbors: $b^2-a^2=a+b$', size=42)),
            D('Tick each line'),
            "Two questions next. Try each one first — then watch.",
        ]),
    ], THEORY, after='solve-q-459')

    M.new_q(G2, TOPIC, 'The sum of seven consecutive integers is $91$. What is the largest of them?',
            ['$13$', '$14$', '$16$', '$19$'], 3, [
        'Sum = count × middle, so the middle number is $\\frac{91}{7}=13$.',
        'Seven numbers: three below the middle and three above it: $10, 11, 12, 13, 14, 15, 16$.',
        'The largest is $13+3=16$. Check: $7\\cdot13=91$ ✓.'])
    M.place_q(G2, THEORY, after=SUMS)
    _solution(M, G2, "Seven numbers in a row — and only their sum.", [
        ('Count × middle', [
            "Seven consecutive numbers add up to ninety-one.",
            "Sum equals count times middle. So the middle is the sum divided by the count.",
            D('Write "91 ÷ 7 = 13"'),
            "Ninety-one divided by seven: thirteen. That's the middle number — the fourth one.",
            D('Write "10, 11, 12, 13, 14, 15, 16"'),
            "Three below it, three above it. Ten up to sixteen.",
            D('Circle choice 3'),
            "The largest: sixteen. Choice three.",
            "The trap is choice one. Thirteen is the middle, not the largest.",
        ]),
        ('The algebra way', [
            "The algebra way, for comparison. Write all seven around the middle, b.",
            D('Write "(b − 3) + (b − 2) + ... + (b + 3) = 7b"'),
            "The minuses and the pluses cancel. Seven b.",
            D('Write "7b = 91 → b = 13"'),
            "Seven b is ninety-one, so b is thirteen. Same answer — count times middle is just faster.",
        ]),
    ])

    M.new_q(G3, TOPIC, 'The sum of four consecutive integers is always —',
            ['divisible by $4$', 'odd', 'even, but not divisible by $4$', 'divisible by $3$'], 3, [
        'Write the numbers as $a, a+1, a+2, a+3$. The sum is $4a+6$.',
        '$4a+6=2(2a+3)$, so the sum is always even.',
        '$4a+6=4(a+1)+2$: a multiple of 4, plus 2. So it is never divisible by 4.',
        'Check: $1+2+3+4=10$ and $2+3+4+5=14$. Both are even and not divisible by 4. And $10$ is not divisible by 3, so (4) is out.'])
    M.place_q(G3, THEORY, after='solve-' + G2)
    _solution(M, G3, "Four in a row. What's always true about the sum?", [
        ('One letter', [
            "Write the four numbers with one letter.",
            D('Write "a + (a + 1) + (a + 2) + (a + 3) = 4a + 6"'),
            "Four a plus six.",
            D('Write "4a + 6 = 2(2a + 3)" and cross out choice 2'),
            "Take out a two: always even. So it's never odd. Choice two is out.",
            D('Write "4a + 6 = 4(a + 1) + 2" and cross out choice 1'),
            "Divisible by four? It's a multiple of four, plus two. Never. Choice one is out.",
            D('Circle choice 3'),
            "Even, but not divisible by four. Choice three.",
        ]),
        ('Test choice 4', [
            "Choice four needs one counterexample.",
            D('Write "1 + 2 + 3 + 4 = 10,  2 + 3 + 4 + 5 = 14"'),
            "One to four: ten. Two to five: fourteen.",
            D('Next to choice 4 write "10 ✗" and cross it out'),
            "Ten doesn't divide by three. Out.",
            "Remember: an odd count of consecutive integers — the sum divides by the count. An even count — never.",
        ]),
    ])

    M.new_card('mem-r26-t16-sums', TOPIC, THEORY, {
        'title': 'Sums of consecutive integers',
        'intro': 'Sum = count × middle. The middle = sum ÷ count.',
        'tables': [{'title': '', 'head': ['Situation', 'Rule', 'Example'], 'rows': [
            ['Consecutive numbers (also evens or odds)', 'sum = count × middle', '$11+12+13+14+15=5\\cdot13=65$'],
            ['Even count', 'the middle ends in .5', '$11+12+13+14=4\\cdot12.5=50$'],
            ['Odd count of consecutive integers', 'the sum divides by the count', '$4+5+6=15=3\\cdot5$'],
            ['Even count of consecutive integers', 'the sum never divides by the count', '$1+2+3+4=10$'],
            ['Integers from $a$ to $b$', '$b-a+1$', 'from $3$ to $10$: $8$'],
            ['Evens (or odds) from $a$ to $b$', '$\\frac{b-a}{2}+1$', 'evens from $4$ to $20$: $9$'],
            ['Consecutive $a<b$', '$b^2-a^2=a+b$', '$5^2-4^2=9=4+5$'],
        ]}],
        'tips': ['Four consecutive integers: the sum is $4a+6$, even but never divisible by 4.'],
    }, after='solve-' + G3)

    # Q2, Q3 solution videos: ÷ instead of ":"
    _division_signs(M, 'solve-q-458')

    # =====================================================================================
    # 4. Even & odd video: ÷, odd-product rule, what a plug-in proves
    # =====================================================================================
    sc = _script(M, PARITY, 6)
    sc += [A('Odd product ⇔ every factor is odd appears', T('Odd product $\\iff$ every factor is odd', size=46)),
           "Turn it around: a product is odd only when EVERY factor is odd. One even factor, and the whole product is even."]
    M.set_slide(PARITY, 6, script=sc)
    b = M.slide(PARITY, 7)
    for it in b['items']:
        it['t'] = it['t'].replace('$:$', '$\\div$')
    _division_signs(M, PARITY)
    M.set_slide(PARITY, 8, title='What a plug-in proves', script=[
        "Here's the key difference.",
        "Adding and multiplying: the parity of the result depends ONLY on the parities you put in.",
        "So one number for each case settles it. Two times three is six — even times odd is always even.",
        A('± and ×: one plug-in per case appears', T('$\\pm,\\ \\times$: one plug-in for each parity case', size=44, gap=40)),
        "Division is different. Six over two is three — odd. Eight over two is four — even. Ten over four — a fraction.",
        A('Division → 3 plug-ins, close together appears', T('Division $\\to$ 3 plug-ins, close together', size=44, gap=40)),
        D('Underline "3"'),
        "So with division I plug in three times — to see the different results that can come out.",
        "Keep them close: one, two, three. Not two, then six, then ten.",
        A('A plug-in can disprove "always" appears', T('A plug-in can disprove "always" — it can\'t prove it', size=44)),
        "And know what a plug-in can do. One example that breaks the rule kills \"always\" at once.",
        "But a few examples that work don't PROVE \"always\". For that you need the reason.",
    ])
    M.set_slide(PARITY, 10, script=[
        "Summary.",
        A("'Plug in: 2 for even · 1 or 3 for odd' appears", T('Plug in: 2 for even · 1 or 3 for odd', size=42)),
        D('Circle "Plug in"'),
        "Even-and-odd question? Plug in numbers — one for each parity case. Don't overcomplicate it.",
        A("'Division: three close plug-ins' appears", T('Division: three close plug-ins', size=42)),
        A("'Delete powers' appears", T('Delete powers — they don\'t change parity', size=42)),
        A("'Odd product → every factor is odd' appears", T('Odd product $\\to$ every factor is odd', size=42)),
        "You can even plug in zero for even sometimes — but I'd avoid it. It can wipe things out and confuse you.",
        "Three questions next.",
    ])
    sb = M.video(PARITY)['hybrid']['sidebar']; sb[6] = 'What a plug-in proves'; M.set_sidebar(PARITY, sb)

    c = M.card('mem-parity')
    c['intro'] = 'Plug in 2 for even and 1 or 3 for odd. For $\\pm$ and $\\times$, one plug-in for each parity case is enough. For division, plug in three times.'
    for t in c['tables']:
        for r in t['rows']: r[0] = r[0].replace(' : ', ' ÷ ')
    c['tips'] = [
        '0 is even.',
        'In a sum, only the odd terms matter: an odd number of them → odd.',
        'One even factor makes a product even. A product is odd only if every factor is odd.',
        'Powers do not change parity (positive whole exponents).',
        'Division: plug in three times, with numbers close together.',
        'A plug-in can disprove "always", but it cannot prove it.',
    ]

    # Q4 (q-460): the stem asked for a condition, but the key says "never odd" -> reworded
    S('q-460', stem='x and y are positive integers, and $x+y$ is odd. Which of the following is true about the expression $x^y+y^x+7+6x$?',
      choices=['It is always odd.', 'It is odd when $x$ is odd and $y$ is even.', 'It is odd when $x$ is even and $y$ is odd.',
               'It is always even.'], correct=4, expl=[
        'Powers do not change parity, so delete them: the expression has the same parity as $x+y+7+6x$.',
        '$x+y$ is odd (given), $7$ is odd, and $6x$ is even. Odd + odd + even = even.',
        'So the expression is always even. Check: $x=1$, $y=2$: $1^2+2^1+7+6=16$. $x=2$, $y=1$: $2^1+1^2+7+12=22$. Both are even.'])
    _replace_say(M, 'solve-q-460', 2, "Even both times. The expression can never be odd. Choice four.",
                 "Even both times — and those are the only two cases. Always even. Choice four.")
    _replace_say(M, 'solve-q-460', 3, "Never odd. Choice four.", "Always even — never odd. Choice four.")
    _division_signs(M, 'solve-q-461')

    # =====================================================================================
    # 5. Products video: the false "smallest product is the divisor" rule -> candidate method; count the twos
    # =====================================================================================
    M.set_slide(PROD, 3, script=[
        A('Three in a row → divides by 6 appears', T('Three in a row $\\to$ divides by $6$', size=50, gap=60)),
        "Three in a row: at least one is even — and one of them divides by three. So the product divides by six.",
        D('Next to it write "1·2·3 = 6, 3·4·5 = 60"'),
        "One times two times three: six. Three times four times five: sixty. Divides by six.",
        A('Four in a row → divides by 24 appears', T('Four in a row $\\to$ divides by $24$', size=50, gap=60)),
        "Four in a row: one of them divides by four, and another one is even. That's eight.",
        "And one of them divides by three. Eight times three: twenty-four.",
        D('Next to it write "1·2·3·4 = 24, 2·3·4·5 = 120"'),
        "Two, three, four, five: a hundred and twenty. Divides by twenty-four.",
    ])
    M.set_slide(PROD, 4, title='Smallest case', script=[
        "That's a pile of rules. Here's a quick way to remember them.",
        A('1·2 = 2, 1·2·3 = 6, 1·2·3·4 = 24 appears', T('$1\\cdot2=2 \\qquad 1\\cdot2\\cdot3=6 \\qquad 1\\cdot2\\cdot3\\cdot4=24$', size=46)),
        "Plug in the smallest numbers. One times two: two. One, two, three: six. One to four: twenty-four.",
        D('Circle 2, 6 and 24'),
        "For these three rules, the smallest product is exactly the divisor. We just saw WHY.",
        "But careful. This is a memory trick for rules we proved — not a way to find new rules.",
    ])
    M.set_slide(PROD, 5, active=4, script=[
        "Now even numbers.",
        A('Two evens: (2a)(2b) = 4ab appears', T('Two evens: $(2a)(2b)=4ab$', size=48, gap=50)),
        "Two even numbers: each one is two times something. Together — four times something. So the product always divides by four.",
        D('Write "smallest case: 2 · 2 = 4"'),
        "The smallest case agrees: two times two, four.",
        A('Three evens: 2·2·2 = 8 appears', T('Three evens: $2\\cdot2\\cdot2=8$', size=48, gap=50)),
        "Three evens: three twos. Eight.",
        A('Two consecutive evens: 2·4 = 8 appears', T('Two consecutive evens: $2\\cdot4=8$', size=48)),
        D('Underline "consecutive"'),
        "Two CONSECUTIVE evens: one of them always divides by four. Two times four — eight.",
        "Never plug in zero here. Zero divides by every number — it tells you nothing.",
    ])
    M.set_slide(PROD, 6, active=6)
    M.set_slide(PROD, 7, active=7, script=[
        "The whole lesson:",
        A("'Proven rules' appears", T('Always: 2 in a row by $2$; 3 in a row by $6$; 4 in a row by $24$', size=40)),
        A("'Evens' appears", T('Always: two evens by $4$; two consecutive evens by $8$', size=40)),
        "These rules are proven — trust them.",
        A("'Smallest case = a candidate' appears", T('Anything else: the smallest case is only a candidate —\ncross out, then test a second case', size=40)),
        "Anything else: the smallest case gives a candidate. Cross out the choices it kills, then test a second case.",
        A("'Integer? Count the twos' appears", T('Integer? Count the twos', size=40)),
        "And for \"is it a whole number\": count the twos.",
        "Three questions next.",
    ])
    # new slide after "Even products": count the twos
    M.insert_slides(PROD, 5, [dict(mode='concept', active=5, title='Count the twos', script=[
        "Is the expression a whole number? Count the twos.",
        A('m even, n odd appears', T('$m$ even, $n$ odd', size=46, gap=40)),
        "m is even: at least one two. n is odd: no twos at all. But n plus one is even: one two.",
        A('m²(n + 1) over 8 appears', T('$\\frac{m^2(n+1)}{8}$', size=60, gap=40)),
        D('Under m² write "2 twos"; under (n + 1) write "1 two"'),
        "m squared: two twos. n plus one: one more. Three twos on top.",
        "Eight is two times two times two — three twos. They cancel. Always a whole number.",
        A('m(n + 1) over 8 appears', T('$\\frac{m(n+1)}{8}$', size=60)),
        D('Under m write "1 two"; under (n + 1) write "1 two"'),
        "Here only two twos for sure. Not enough. m equals two, n equals one: four over eight — a half.",
        "More twos can come by luck — m could be four. But \"necessarily\" means for EVERY choice of m and n.",
    ])])
    # new slide after "Smallest case": only a candidate (counterexample 1·3·5 vs 7·9·11)
    M.insert_slides(PROD, 4, [dict(mode='concept', active=3, title='Only a candidate', script=[
        "Watch what happens with three consecutive ODD numbers.",
        A('1·3·5 = 15 appears', T('$1\\cdot3\\cdot5=15$', size=50, gap=40)),
        "Smallest case: one, three, five. Fifteen. So the product always divides by fifteen?",
        A('7·9·11 = 693 appears', T('$7\\cdot9\\cdot11=693$', size=50, gap=40)),
        "Try seven, nine, eleven: six hundred ninety-three. It ends in three — it doesn't divide by five. So not by fifteen either.",
        D('Next to 693 write "÷ 5 ✗   ÷ 3 ✓"'),
        "Only three survives. Every third odd number is a multiple of three.",
        A('Smallest case = a candidate appears', T('Smallest case $\\to$ only a candidate', size=44, gap=30)),
        "So the smallest case gives the BIGGEST number that could work. Only a candidate.",
        A('Cross out, then test appears', T('① Cross out choices that don\'t divide it\n② Test a second case that avoids the factor', size=40)),
        "Use it like this. One: cross out every choice that doesn't divide the smallest case.",
        "Two: test a second case. Choose numbers that AVOID the factor you're checking — here, no five.",
        "Three, five, seven has a five inside. So does five, seven, nine. They won't catch the mistake.",
    ])])
    M.set_sidebar(PROD, ['Two in a row', 'Three and four', 'Smallest case', 'Only a candidate', 'Even products',
                         'Count the twos', 'Hidden products', 'Recap'])

    c = M.card('mem-products')
    c['intro'] = 'These products ALWAYS divide by a number, and each rule has a reason. For any other product, the smallest case gives only a candidate.'
    c['tables'] = [
        {'title': 'Proven rules', 'head': ['Product of…', 'Why', 'Always divides by'], 'rows': [
            ['2 consecutive', 'one is even', '2'],
            ['3 consecutive', 'one is even, one divides by 3', '6'],
            ['4 consecutive', 'one divides by 4, another is even, one divides by 3', '24'],
            ['2 even', '$(2a)(2b)=4ab$', '4'],
            ['3 even', 'three twos', '8'],
            ['2 consecutive even', 'one of them divides by 4', '8']]},
        {'title': 'The smallest case is only a candidate', 'head': ['Product of…', 'Smallest case', 'Second case', 'Always divides by'], 'rows': [
            ['3 consecutive odd', '$1\\cdot3\\cdot5=15$', '$7\\cdot9\\cdot11=693$ (not by 5)', 'only 3']]},
    ]
    c['tips'] = [
        'Smallest case → cross out the choices that do not divide it. Then test a second case that avoids the factor you are checking.',
        'Integer? Count the twos. $m$ even, $n$ odd: $\\frac{m^2(n+1)}{8}$ has three twos on top, so it is always an integer.',
        '$x^2-1=(x-1)(x+1)$ and $x^3-x=(x-1)x(x+1)$ hide consecutive numbers.',
        'Never use a case that gives 0: 0 is divisible by every number, so it tells you nothing.',
    ]

    # Q7 / Q8 videos: ÷, and plug-ins point the way while the reason proves it
    _division_signs(M, 'solve-q-463')
    _replace_say(M, 'solve-q-463', 2, "Twelve, zero, four — even every time. Always even. Choice three.",
                 "Twelve, zero, four — even every time. That points to choice three. The math on the next slide proves it.")
    _replace_say(M, 'solve-q-463', 3, "So plug in 1, 3, 5 — twenty seconds.",
                 "On the exam: plug in one, three, five — and remember the reason: two consecutive evens divide by eight.")
    _division_signs(M, 'solve-q-464')
    _replace_say(M, 'solve-q-464', 1, "Last question.", "Question eight.")
    _replace_say(M, 'solve-q-464', 2, "Always even. Choice two. And yes — zero is even.",
                 "Always even. Choice two. And yes — zero is even. The reason is on the next slide: three in a row divide by six.")

    # =====================================================================================
    # 6. New guided question: the candidate method (after Q8)
    # =====================================================================================
    M.new_q(G4, TOPIC, 'n is a positive odd number. The product $n(n+2)(n+4)$ is necessarily divisible by —',
            ['$45$', '$15$', '$5$', '$3$'], 4, [
        'Smallest case: $n=1$ gives $1\\cdot3\\cdot5=15$. A number that always divides the product must divide $15$. $45$ does not, so (1) is out.',
        'The smallest case is only a candidate. Test a second case with no multiple of 5: $n=7$ gives $7\\cdot9\\cdot11=693$. It ends in 3, so it is not divisible by 5, and not by 15. (2) and (3) are out.',
        'Why 3 always works: every third odd number is a multiple of 3 ($3, 9, 15, 21, \\dots$). Three odd numbers in a row always include one of them.',
        'Trap: $n=3$ gives $105$ and $n=5$ gives $315$. Both are divisible by 15, because each product has a 5 inside.'])
    M.place_q(G4, THEORY, after='solve-q-464')
    _solution(M, G4, "Three odd numbers in a row. Don't trust the smallest case.", [
        ('Smallest case, then a second case', [
            "Three odd numbers in a row. What always divides the product?",
            D('Write "n = 1: 1 · 3 · 5 = 15"'),
            "Smallest case first: one, three, five. Fifteen.",
            D('Cross out choice 1'),
            "Forty-five doesn't divide fifteen. Out.",
            "Fifteen, five and three all divide fifteen. But the smallest case is only a candidate. Test a second case.",
            "Which one? We want to check five. So choose three odd numbers with NO five inside.",
            D('Write "n = 7: 7 · 9 · 11 = 693"'),
            "Seven, nine, eleven. Six hundred ninety-three.",
            D('Cross out choices 2 and 3'),
            "It ends in three — it doesn't divide by five. So not by fifteen either. Both out.",
            D('Circle choice 4'),
            "Three is left. Choice four.",
        ]),
        ('Why 3 — and the trap', [
            "Why three, always? Every third odd number is a multiple of three.",
            D('Write "1, 3, 5, 7, 9, 11, 13, 15" and circle 3, 9 and 15'),
            "Three, nine, fifteen. Any three odd numbers in a row catch one of them.",
            "Now the trap. Plug in three, five, seven. Or five, seven, nine.",
            D('Write "3 · 5 · 7 = 105,  5 · 7 · 9 = 315"'),
            "Both divide by fifteen! Close numbers can fool you — each of them has a five inside.",
            "So choose the second case on purpose: avoid the factor you're testing.",
        ]),
    ])

    # sidebars of the theory solution videos (renumbered in flow order by math_api)
    labels = ['Question %d' % n for n in list(range(1, 9)) + [17, 18, 19, 20]]
    for vid in THEORY_SOLVES + ['solve-' + g for g in (G1, G2, G3, G4)]:
        M.set_sidebar(vid, labels)

    # =====================================================================================
    # 7. Advanced videos: small wording fixes
    # =====================================================================================
    _replace_say(M, 'solve-q-465', 3, "Now the same thing with numbers. The basic set for this picture: negative two, negative one, one, two.",
                 "Now the same thing with numbers. Simple numbers in this order: negative two, negative one, one, two.")
    _division_signs(M, 'solve-q-469')
    for vid in ['solve-q-%d' % k for k in range(465, 473)]:
        M.touched_videos.add(vid)

    # =====================================================================================
    # 8. Existing questions: TeX, ÷ / fractions, stacked givens, clear stems, solutions with numbers
    # =====================================================================================
    S('q-457', stem='Given:\n$\\begin{cases} y\\ne0 \\\\ \\frac{x^6\\cdot y^5}{|y|}<0 \\end{cases}$\nWhich of the following is necessarily true?', expl=[
        '$x^6$ is an even power, so $x^6\\ge0$. If $x=0$, the expression equals $0$, which is not negative. Therefore $x\\ne0$ and $x^6>0$.',
        'Since $y\\ne0$, $|y|>0$.',
        'The only piece that can make the expression negative is $y^5$. An odd power keeps the sign, so $y^5<0$ means $y<0$.',
        'Nothing is known about the sign of $x$. Choice (1) claims too much ($x<0$ is not necessarily true). Choices (2) and (4) say $y>0$, which contradicts $y<0$. The answer is (3).'])
    S('q-458', stem='a, b and c are consecutive even numbers, and $0<a<b<c$. $\\frac{c^2-a^2}{b}=?$', expl=[
        'Write the numbers around the middle: $a=b-2$ and $c=b+2$.',
        '$c^2-a^2=(b+2)^2-(b-2)^2=(b^2+4b+4)-(b^2-4b+4)=8b$.',
        '$\\frac{8b}{b}=8$.',
        'Check with $2, 4, 6$: $\\frac{36-4}{4}=\\frac{32}{4}=8$ ✓.'])
    S('q-459', stem='a, b, c and d are consecutive integers, and $a<b<c<d$. $\\frac{d-a}{c-b}-\\frac{a-c}{d-c}=?$', expl=[
        'In consecutive integers every difference is a fixed number: $d-a=3$, $c-b=1$, $a-c=-2$, $d-c=1$.',
        '$\\frac31-\\frac{-2}{1}=3-(-2)=3+2=5$.',
        'Watch the signs: $a-c$ is smaller minus bigger, so it is negative. Subtracting a negative adds.',
        'Check with $1, 2, 3, 4$: $\\frac{4-1}{3-2}-\\frac{1-3}{4-3}=3-(-2)=5$ ✓.'])
    S('q-461', stem='x and y are integers. x is even and not $0$, and y is odd. Which of the following is the most precise description of $\\frac{4y}{x^3}$?', expl=[
        'x is even, so $x=2k$ ($k$ is an integer, $k\\ne0$). Then $x^3=8k^3$.',
        '$\\frac{4y}{8k^3}=\\frac{y}{2k^3}$.',
        'The top, $y$, is odd. The bottom, $2k^3$, is even. Odd divided by even is never an integer, so the result is always a fraction.',
        'Check: $x=2$, $y=1$: $\\frac48=\\frac12$. $x=2$, $y=3$: $\\frac{12}{8}=\\frac32$. $x=4$, $y=3$: $\\frac{12}{64}=\\frac{3}{16}$.'])
    S('q-462', stem='x and y are integers. Given: $x-y=4$. Which of the following expressions is necessarily even?', expl=[
        '$x-y=4$ is even, so x and y have the same parity: both even or both odd.',
        'Plug in two odd numbers: $x=5$, $y=1$. (1) $2\\cdot5-1=9$, odd. (2) $25+1+25=51$, odd. (3) $5\\cdot25+2=127$, odd. (4) $25-1=24$, even.',
        'Why (4) is always even: $x^2-y^2=(x-y)(x+y)=4(x+y)$.'])
    S('q-463', stem='x is an odd number. Which of the following is the most precise description of $\\frac{x^2-1}{2}$?', expl=[
        '$x^2-1=(x-1)(x+1)$. x is odd, so $x-1$ and $x+1$ are two consecutive even numbers. One of them divides by 4, so the product divides by 8: $x^2-1=8k$.',
        '$\\frac{8k}{2}=4k$, which is always even.',
        'Check: $x=1, 3, 5$ give $\\frac02=0$, $\\frac82=4$, $\\frac{24}{2}=12$. All even.'])
    S('q-464', stem='x is an integer. The expression $\\frac{x^3-x}{3}$ is always —', expl=[
        '$x^3-x=x(x^2-1)=(x-1)\\cdot x\\cdot(x+1)$: three consecutive integers. Their product divides by 6: $x^3-x=6k$.',
        '$\\frac{6k}{3}=2k$, which is always even.',
        'Check: $x=1, 2, 3$ give $0$, $2$, $8$. $x=2$ gives $2$, which is not divisible by 4, so (3) is out.'])
    S('q-465', stem='Given: $p<q<0<r<s$. Which of the following expressions is necessarily negative?', expl=[
        'Bigger minus smaller is positive, and smaller minus bigger is negative. So $q-p>0$, $s-r>0$, $r-s<0$ and $p-q<0$. Also $p<0$ and $-r<0$.',
        '(1) $(+)(+)=+$. (2) $(-)(-)=+$. (3) $(-)(-)=+$. (4) $(+)(-)=-$.',
        'Only (4) is necessarily negative. Check with $p=-2$, $q=-1$, $r=1$, $s=2$: (4) gives $1\\cdot(-1)=-1$.'])
    S('q-466', stem='Given:\n$\\begin{cases} a<b \\\\ ab<0 \\end{cases}$\nWhich of the following expressions is necessarily positive?', expl=[
        '$ab<0$: a and b have opposite signs. Since $a<b$, the negative one is a: $a<0<b$.',
        '(1) The top, $b^2-a$, is positive plus positive, so it is positive. The bottom, $a$, is negative. Positive divided by negative: negative.',
        '(2) $\\frac{a^2-b^2}{a-b}=\\frac{(a-b)(a+b)}{a-b}=a+b$. Mixed signs: the sign depends on which number is bigger in size. Not necessarily positive.',
        '(3) The top, $a-b$, is smaller minus bigger: negative. The bottom, $a$, is negative. Negative divided by negative: always positive.',
        '(4) $\\frac{ab^2}{ba^2}=\\frac ba$, which is positive divided by negative, so it is negative.',
        'Check with $a=-1$, $b=1$: the four choices give $-2$, $0$, $2$, $-1$. Only (3) is positive.'])
    S('q-467', stem='Given:\n$\\begin{cases} d<e \\\\ d+e+f>0 \\end{cases}$\nWhich of the following additional givens makes f necessarily positive?', expl=[
        '(2) If $e<0$, then $d<e<0$. Both are negative, so $d+e<0$. For $d+e+f$ to be positive, f must be positive.',
        'The other choices do not force f to be positive:',
        '(1) $e=100$, $d=0$, $f=0$: $d+e+f=100>0$, but $f=0$.',
        '(3) $d=1$, $e=2$, $f=-1$: $d+e+f=2>0$, but $f<0$.',
        '(4) $d=-1$, $e=100$, $f=0$: $d+e+f=99>0$, but $f=0$.'])
    S('q-468', stem='m and n are consecutive even numbers, and p and q are consecutive even numbers. Given:\n$\\begin{cases} m<n \\\\ p<q \\\\ p+n\\ne0 \\end{cases}$\n$\\frac{n^2-m^2+q^2-p^2}{p+n}=?$', expl=[
        'Consecutive even numbers: $n=m+2$ and $q=p+2$.',
        '$n^2-m^2=(n-m)(n+m)=2(2m+2)=4m+4$, and $q^2-p^2=(q-p)(q+p)=2(2p+2)=4p+4$.',
        'The top: $4m+4p+8=4(m+p+2)$. The bottom: $p+n=p+m+2$.',
        '$\\frac{4(m+p+2)}{m+p+2}=4$.',
        'Check with $m=2$, $n=4$, $p=6$, $q=8$: $\\frac{16-4+64-36}{6+4}=\\frac{40}{10}=4$ ✓.'])
    S('q-469', stem='a, b and c are consecutive integers, and $a<b<c$. Given: $a^2+b^2=c^2$. Which of the following could be the sum of a, b and c?', expl=[
        'Write the numbers around the middle: $a=b-1$, $c=b+1$.',
        '$(b-1)^2+b^2=(b+1)^2$ gives $b^2-2b+1+b^2=b^2+2b+1$, so $b^2=4b$: $b=0$ or $b=4$.',
        '$b=4$: the numbers are $3, 4, 5$, with sum $12$. $b=0$: the numbers are $-1, 0, 1$, with sum $0$.',
        'Only $12$ is among the choices. Check: $9+16=25$ ✓.',
        'Faster: sum = count × middle, so the middle is the sum divided by 3. For $12$ the middle is $4$: $3^2+4^2=5^2$ ✓.'])
    S('q-470', stem='a and x are integers. Given: $x=(a-6)^2+(a+5)^3$. Which of the following statements is necessarily true?', expl=[
        '$a-6$ has the same parity as a (subtracting an even number). $a+5$ has the opposite parity (adding an odd number).',
        'Powers do not change parity, so $x$ has the same parity as $(a-6)+(a+5)=2a-1$, which is always odd.',
        'So x is always odd, and a can be even or odd. Check: $a=1$ gives $25+216=241$. $a=2$ gives $16+343=359$. Both odd.'])
    S('q-471', stem='m, p, q and r are integers. Given: $2m+1=(p+1)^2\\cdot q^5\\cdot(r-1)^2$. Which of the numbers m, p, q, r is necessarily odd?', expl=[
        '$2m+1$ is odd for every integer m. So the product on the right is odd.',
        'A product is odd only if every factor is odd.',
        '$(p+1)^2$ is odd, so $p+1$ is odd and p is even. $q^5$ is odd, so q is odd. $(r-1)^2$ is odd, so $r-1$ is odd and r is even.',
        'm can be even or odd: $p=0$, $q=1$, $r=2$ gives $2m+1=1$, so $m=0$. $p=0$, $q=3$, $r=2$ gives $2m+1=243$, so $m=121$. The answer is q.'])
    S('q-472', stem='m is an even positive number, and n is an odd positive number. Which of the following expressions is not necessarily an integer?', expl=[
        'Count the twos. m is even, so it has at least one two. n is odd, so $n+1$ and $n-1$ are even.',
        '(1) In $m(n+1)^2$ there is one two from m and two twos from $(n+1)^2$. Three twos, enough for $8=2^3$. Always an integer.',
        '(2) In $m^2n^2$ there are only two twos for sure (n is odd). With $m=2$ and $n=1$ the value is $\\frac{4\\cdot1}{8}=\\frac12$. Not necessarily an integer.',
        '(3) $(m+n)^2-(m-n)^2=4mn$. With $m=2k$: $8kn$. Always divisible by 8.',
        '(4) $n-1$ and $n+1$ are consecutive even numbers, so their product divides by 8.',
        'The answer is (2).'])
    S('q-473', stem='x and y are integers. Given: $x-y=6$. Which of the following expressions is necessarily even?',
      choices=['$x+y$ only', '$x+y$ and $x^2-y^2$ only', '$x^2+y^2$ only', '$x+y$, $x^2-y^2$ and $x^2+y^2$'], correct=4, expl=[
        '$x-y=6$ is even, so x and y have the same parity.',
        '$x+y$: even + even or odd + odd. Always even.',
        '$x^2-y^2=(x-y)(x+y)=6(x+y)$. Always even.',
        '$x^2+y^2$: powers do not change parity, so it has the parity of $x+y$. Always even.',
        'All three are always even. Check with $x=7$, $y=1$: $8$, $48$, $50$.'])
    S('q-474', stem='In class A, every child has 4 pencils. In class D, every child has 5 pencils. The number of children in class D is odd. The total number of pencils of all the children in classes A and D is necessarily —', expl=[
        'Total $=4\\cdot(\\text{children in A})+5\\cdot(\\text{children in D})$.',
        '$4$ times any number is even. $5$ times an odd number is odd × odd = odd.',
        'Even + odd = odd, so the total is necessarily odd.',
        'Check: 1 child in A and 1 child in D: $4+5=9$. Odd, and not divisible by 4 or by 5.'])
    S('q-475', stem='m and n are odd numbers. Which of the following expressions cannot be an integer?', expl=[
        'm and n are odd, so $mn$ is odd, and $m\\cdot\\frac n2=\\frac{mn}{2}$ is an odd number divided by 2. Never an integer.',
        'The others can be integers: (1) $m=3$, $n=7$: $\\frac{10}{5}=2$. (2) $m=3$, $n=5$: $\\frac82=4$. (3) $m=3$, $n=5$: $\\frac{15}{5}=3$.'])
    S('q-476', stem='Given: $p^5\\cdot q^4<0$. Which of the following statements is necessarily true?', expl=[
        '$q^4$ is an even power, so $q^4\\ge0$. If $q=0$, the product is $0$, which is not negative. So $q\\ne0$ and $q^4>0$.',
        'Then $p^5$ must be negative. An odd power keeps the sign, so $p<0$.',
        'The sign of q is not known: $p=-1$, $q=1$ and $p=-1$, $q=-1$ both work.'])
    S('q-478', stem='a, b and c are consecutive integers, and $0<a<b<c$. The product of the three numbers is 8 times their sum. $b=?$', expl=[
        'Write the numbers around the middle: $a=b-1$, $c=b+1$. The sum is $3b$ (count × middle). The product is $(b-1)b(b+1)$.',
        '$(b-1)b(b+1)=8\\cdot3b$. Divide by b ($b>0$): $(b-1)(b+1)=24$, so $b^2-1=24$, $b^2=25$ and $b=5$.',
        'Check: $4\\cdot5\\cdot6=120$ and $8\\cdot(4+5+6)=8\\cdot15=120$ ✓.'])
    S('q-479', stem='The number $10^7+7^{10}$ is —', expl=[
        '$10^7$ is even. $7^{10}$ is odd (an odd number to any power is odd). Even + odd = odd.',
        'An odd number is not divisible by 10. It is not divisible by 7 either: $7^{10}$ is divisible by 7, but $10^7$ is not, so the sum is not.'])
    S('q-480', stem='m and n are positive integers, and $n<m$. Given:\n$\\begin{cases} m^2n\\text{ is even} \\\\ m+n\\text{ is odd} \\end{cases}$\nWhich of the following statements is not correct?',
      choices=['$n(m^2+m)$ is even', '$m+n+1$ is even', '$mn^2$ is odd', '$m-n$ is odd'], expl=[
        '$m+n$ is odd, so one of m and n is even and the other is odd.',
        '$mn^2$ contains the even one, so it is even. The statement "$mn^2$ is odd" is not correct.',
        'The others are correct: (1) $m^2+m=m(m+1)$ is a product of consecutive numbers, so it is even. (2) $m+n+1=\\text{odd}+1=\\text{even}$. (4) Even minus odd, or odd minus even, is odd.'])
    S('q-481', stem='p and q are prime numbers, and $p\\le q$. Which of the following expressions is necessarily even?', expl=[
        'If $q=2$, then $p\\le2$ forces $p=2$: $p(q+1)=2\\cdot3=6$, even.',
        'If q is an odd prime, $q+1$ is even, so $p(q+1)$ is even.',
        'So (2) is always even. The others can be odd: (1) $p=3$, $q=5$: $15$. (3) $p=2$, $q=3$: $3\\cdot3=9$. (4) $p=2$, $q=3$: $5$.'])
    S('q-482', stem='a and b are positive consecutive integers, and $a<b$. Given: $a^2-b^2=-9$. $a+b=?$', expl=[
        'Consecutive: $b-a=1$, so $a-b=-1$ and $a^2-b^2=(a-b)(a+b)=-(a+b)$.',
        '$-(a+b)=-9$, so $a+b=9$.',
        'Shortcut: for consecutive $a<b$, $b^2-a^2=a+b$. Check: $a=4$, $b=5$: $16-25=-9$ ✓.'])
    S('q-483', stem='n is an even number. Which of the following could be the value of $\\frac{n^3}{2}$?', expl=[
        'n is even: $n=2k$. Then $n^3=8k^3$, so $\\frac{n^3}{2}=4k^3$. It must divide by 4.',
        'Only $256$ divides by 4 ($54$, $66$ and $86$ do not). And $256$ works: $n^3=512$, so $n=8$ ✓.'])
    S('q-484', stem='a, b and c are consecutive integers, and $a<b<c$. Given: $a^2+c^2=12b-16$. $a+b+c=?$', expl=[
        'Write the numbers around the middle: $a=b-1$, $c=b+1$.',
        '$(b-1)^2+(b+1)^2=2b^2+2$. So $2b^2+2=12b-16$, which gives $b^2-6b+9=0$, $(b-3)^2=0$ and $b=3$.',
        'The numbers are $2, 3, 4$, and the sum is $3b=9$. Check: $4+16=20$ and $12\\cdot3-16=20$ ✓.'])
    S('q-485', stem='Given: $x<y<z<0$. Which of the following expressions is necessarily positive?', expl=[
        'All three numbers are negative.',
        '(1) $xy>0$, divided by $z<0$: negative.',
        '(2) $x+y<0$ (negative + negative) and $-z>0$: negative.',
        '(3) $(-x)(-y)>0$, times $z<0$: negative.',
        '(4) $x<0$ and $y+z<0$ (negative + negative). Negative × negative = positive, always. The answer is (4).'])
    S('q-486', stem='j and n are integers. Given: $2n+1=j(4j+1)$. j is necessarily —', expl=[
        '$2n+1$ is odd for every integer n. $4j+1$ is also odd, because $4j$ is even.',
        'A product is odd only if every factor is odd. So j is odd.',
        'Divisibility by 3 is not fixed: $j=1$ gives $1\\cdot5=5=2\\cdot2+1$ ($n=2$), and $j=3$ gives $3\\cdot13=39=2\\cdot19+1$ ($n=19$).'])
    S('q-487', stem='a and b are consecutive integers. Given: $x=a^2-b^2+3a-3b$. Which of the following statements is necessarily true?', expl=[
        'Factor: $x=(a-b)(a+b)+3(a-b)=(a-b)(a+b+3)$.',
        'a and b are consecutive: $a-b=1$ or $a-b=-1$. Also $a+b$ is odd (one even, one odd), so $a+b+3$ is odd + odd = even.',
        'So $x=(\\pm1)\\cdot(\\text{even})$, and x is always even.',
        'The sign is not fixed: $a=2$, $b=1$ gives $x=1\\cdot6=6$. $a=1$, $b=2$ gives $x=(-1)\\cdot6=-6$.'])
    S('q-488', stem='m and n are integers. The expression $(m+1)(4n+m)$ is necessarily —', expl=[
        '$4n$ is even, so $4n+m$ has the same parity as m. $m+1$ has the opposite parity. So one of the two factors is even, and the product is always even.',
        'The others fail: (1) With $m=-3$ and $n=1$ the product is $(-2)\\cdot1=-2$, negative. (3) With $m=-1$ the product is $0$. (4) With $m=3$ and $n=1$ the product is $4\\cdot7=28$, not divisible by 3.'])
    S('q-489', stem='n is an integer greater than 1. At least half of the integers from 1 to n (inclusive) are —', expl=[
        'The list starts with 1, which is odd, and then goes odd, even, odd, even. So there are never fewer odd numbers than even numbers.',
        'For $n=4$, $1$ and $3$ are odd (2 of 4, exactly half). For $n=5$, $1$, $3$ and $5$ are odd (3 of 5, more than half).',
        'The others fail: (2) For $n=3$, only $2$ is even (1 of 3). (3) For $n=9$, the primes are $2, 3, 5, 7$ (4 of 9, less than half). (4) For $n=3$, only $1$ is not prime (1 of 3).'])
    S('q-490', stem='a and b are positive integers. Given: $ab=36$. Which of the following statements is necessarily true?', expl=[
        '$36=2^2\\cdot3^2$. If b is odd, b has no factor 2, so both twos are in a. Then a is even. So (3) is always true.',
        'Check every odd b: $b=1$, $3$, $9$ give $a=36$, $12$, $4$. All even.',
        'The others fail: (1) $a=b=6$. (2) $a=1$, $b=36$: $a+b=37>18$. (4) $a=2$, $b=18$: both even.'])
    S('q-491', stem='Given:\n$\\begin{cases} a<b \\\\ ab<c \\end{cases}$\nWhich of the following is not possible?', expl=[
        'If $b<0$, then $a<b<0$. Both are negative, so $ab>0$.',
        'If also $c<0$, then $ab<c$ says that a positive number is less than a negative number. Impossible. So (4) is not possible.',
        'The others are possible: (1) $a=1$, $b=2$, $c=5$. (2) $a=-1$, $b=2$, $c=-1$ ($ab=-2<-1$). (3) $a=-3$, $b=-2$, $c=10$ ($ab=6<10$).'])
    S('q-492', stem='m and n are positive integers. m is even and n is odd. Which of the following expressions is necessarily an integer?', expl=[
        'Count the twos. n is odd, so $n-1$ and $n+1$ are consecutive even numbers: one divides by 2 and the other by 4. That is three twos. m is even: one more two. Four twos: $2^4=16$. So (1) is always an integer.',
        'The others fail: (2) $m=2$, $n=3$: $\\frac{4\\cdot9}{8}=\\frac92$. (3) $m=6$, $n=1$: $\\frac{1\\cdot5\\cdot7}{3}=\\frac{35}{3}$. (4) $m=2$, $n=3$: $\\frac{3\\cdot2}{4}=\\frac32$.'])

    X = 'alg-extra-unit-t16-3-'
    S(X + '1', stem='a and b are odd integers. Which of the following expressions is necessarily even?', expl=[
        'Plug in $a=1$, $b=3$: (1) $3$, odd. (2) $5$, odd. (3) $1+9+1=11$, odd. (4) $4$, even.',
        'Why (4) is always even: odd + odd = even.'])
    S(X + '2', stem='The sum of three consecutive integers is $48$. What is the largest of them?',
      choices=['$16$', '$18$', '$17$', '$15$'], expl=[
        'Sum = count × middle, so the middle number is $\\frac{48}{3}=16$.',
        'The numbers are $15, 16, 17$. The largest is $17$.'])
    S(X + '3', stem='How many even integers are there between $-7$ and $9$?',
      choices=['$9$', '$10$', '$8$', '$7$'], expl=[
        'List them: $-6, -4, -2, 0, 2, 4, 6, 8$. That is 8 numbers. Remember: $0$ is even.',
        'Or count the steps of two from $-6$ to $8$: $\\frac{8-(-6)}{2}+1=7+1=8$.'])
    S(X + '4', stem='a and b are integers, and $ab$ is odd. Which of the following is necessarily true?',
      choices=['a and b are both positive', 'exactly one of a and b is even', '$a+b$ is odd', 'a and b are both odd'], expl=[
        'One even factor makes a product even. The product is odd, so neither factor is even: both are odd.',
        'The others fail: $a=-1$, $b=3$ gives an odd product, but a is not positive, and $a+b=2$ is even.'])
    S(X + '5', stem='What is the sum of all the integers from $-12$ to $15$ (inclusive)?',
      choices=['$42$', '$30$', '$39$', '$45$'], expl=[
        'Each number from $-12$ to $-1$ cancels its opposite from $1$ to $12$. Zero adds nothing.',
        'What is left: $13+14+15=42$.',
        'Check with count × middle: there are $15-(-12)+1=28$ numbers, and the middle is $\\frac{-12+15}{2}=1.5$. $28\\cdot1.5=42$ ✓.'])
    S(X + '6', stem='n is an integer. Which of the following expressions is necessarily odd?', expl=[
        '$2n^2$ is even, so $2n^2+1$ is always odd.',
        'The others fail: (1) $n(n+1)$ is a product of consecutive numbers, always even. (3) $n=1$: $1+1=2$, even. (4) $2n$ is always even.'])
    S(X + '7', stem='The sum of four consecutive even integers is $44$. What is the smallest of them?',
      choices=['$6$', '$10$', '$12$', '$8$'], expl=[
        'Write them as $n, n+2, n+4, n+6$. The sum is $4n+12=44$, so $4n=32$ and $n=8$.',
        'Or count × middle: the middle is $\\frac{44}{4}=11$, halfway between $10$ and $12$. The numbers are $8, 10, 12, 14$.'])

    # =====================================================================================
    # 9. Practice: remove a near-duplicate, add new items, order easy -> hard
    # =====================================================================================
    # Pass 2: q-477 is an original question and is restored (text clean-up only)
    S('q-477', stem='a, b and c are consecutive positive integers, and $a<b<c$. Given: $c^2-a^2=48$. $b=?$', expl=[
        'Consecutive: $b=a+1$ and $c=a+2$, so $c-a=2$ and $c+a=2a+2$.',
        '$c^2-a^2=(c-a)(c+a)=2(2a+2)=4(a+1)=4b$.',
        'So $4b=48$ and $b=12$.',
        'Check: $a=11$, $c=13$: $13^2-11^2=169-121=48$ ✓.'])
    P = {}
    P['05'] = ('Given: $a<b<0<c$. Which of the following expressions is necessarily negative?',
               ['$a+c$', '$c-a$', '$a+b$', '$ab$'], 3, [
        '(3) a and b are both negative. Negative + negative = negative, always.',
        'The others: (1) Mixed signs: the sign depends on which number is bigger in size. $a=-2$, $c=5$ gives $3>0$. (2) Bigger minus smaller: positive. (4) Negative × negative: positive.'])
    P['06'] = ('Given:\n$\\begin{cases} a+b<0 \\\\ ab>0 \\end{cases}$\nWhich of the following is necessarily true?',
               ['$a<0$ and $b<0$', '$a<0<b$', '$a>0$ and $b>0$', '$a<0$, but the sign of $b$ cannot be determined'], 1, [
        '$ab>0$: a and b have the same sign, and neither of them is $0$.',
        'If both were positive, the sum would be positive. The sum is negative, so both are negative.',
        'Check: $a=-1$, $b=-2$: $a+b=-3<0$ and $ab=2>0$ ✓.'])
    P['07'] = ('Given: $x<y<0$. Which of the following expressions is necessarily positive?',
               ['$x+y$', '$x-y$', '$y-x$', '$x+y^2$'], 3, [
        '(3) Bigger minus smaller is positive, even when both numbers are negative: $y-x>0$.',
        'The others: (1) Negative + negative: negative. (2) Smaller minus bigger: negative. (4) Not fixed: $x=-3$, $y=-2$ gives $-3+4=1$, but $x=-10$, $y=-1$ gives $-10+1=-9$.'])
    P['08'] = ('The sum of five consecutive integers is $85$. What is the largest of them?',
               ['$17$', '$18$', '$19$', '$21$'], 3, [
        'Sum = count × middle, so the middle number is $\\frac{85}{5}=17$.',
        'The numbers are $15, 16, 17, 18, 19$. The largest is $19$.'])
    P['09'] = ('Which of the following could be the sum of four consecutive integers?',
               ['$20$', '$24$', '$26$', '$28$'], 3, [
        'The sum of $a, a+1, a+2, a+3$ is $4a+6=4(a+1)+2$: even, but never divisible by 4.',
        '$20$, $24$ and $28$ are divisible by 4, so they are out.',
        '$26$: $4a+6=26$ gives $a=5$, and $5+6+7+8=26$ ✓.'])
    P['10'] = ('How many integers are there from $-5$ to $20$ (inclusive)?',
               ['$25$', '$26$', '$15$', '$24$'], 2, [
        'From a to b (inclusive) there are $b-a+1$ integers.',
        '$20-(-5)+1=25+1=26$.',
        'Check the rule on a small case: from $1$ to $3$ there are 3 numbers, and $3-1+1=3$.'])
    P['11'] = ('n is a positive integer. The product $(n+1)(n+2)(n+3)$ is necessarily divisible by —',
               ['$24$', '$12$', '$8$', '$6$'], 4, [
        'Three consecutive integers: the product always divides by 6 (one of them is even, and one divides by 3).',
        'The smallest case, $n=1$, gives $2\\cdot3\\cdot4=24$. All four choices divide 24, so it only gives candidates.',
        'Second case: $n=2$ gives $3\\cdot4\\cdot5=60$. $24$ and $8$ do not divide 60. Out.',
        'A case with no multiple of 4: $n=4$ gives $5\\cdot6\\cdot7=210$. $12$ does not divide 210. Out. The answer is $6$.'])
    P['12'] = ('n is an odd number. $n^2-1$ is necessarily divisible by —',
               ['$16$', '$24$', '$8$', '$48$'], 3, [
        '$n^2-1=(n-1)(n+1)$: two consecutive even numbers. One divides by 4 and the other by 2, so the product divides by 8.',
        'Do not use $n=1$: it gives $0$, and $0$ is divisible by every number. It tells you nothing.',
        '$n=5$ gives $24$: $16$ and $48$ are out. $n=3$ gives $8$: $24$ is out. The answer is $8$.'])
    P['13'] = ('k is an integer. Which of the following expressions is necessarily an integer?',
               ['$\\frac{k(k+1)(k+2)}{4}$', '$\\frac{k(k+1)(k+2)(k+3)}{8}$', '$\\frac{k^2(k+1)}{4}$', '$\\frac{(2k+1)(2k+3)}{3}$'], 2, [
        '(2) Four consecutive integers: the product always divides by 24, so it divides by 8. Always an integer.',
        'The others fail: (1) $k=1$: $\\frac{6}{4}$. (3) $k=1$: $\\frac{2}{4}$. (4) $k=2$: $\\frac{5\\cdot7}{3}=\\frac{35}{3}$.'])
    P['14'] = ('The sum of ten consecutive integers is $5$. What is the largest of them?',
               ['$4$', '$5$', '$6$', '$10$'], 2, [
        'Sum = count × middle, so the middle is $\\frac{5}{10}=0.5$. With an even count, the middle is halfway between the two middle numbers: $0$ and $1$.',
        'Five numbers from $1$ up: $1, 2, 3, 4, 5$. Five numbers from $0$ down: $0, -1, -2, -3, -4$.',
        'The largest is $5$. Check: $-4$ to $4$ cancel out, and $5$ is left ✓.'])
    P['15'] = ('How many odd integers are there from $11$ to $59$ (inclusive)?',
               ['$24$', '$25$', '$48$', '$49$'], 2, [
        'Odd numbers go up in steps of 2. The number of steps from 11 to 59 is $\\frac{59-11}{2}=24$.',
        'Add 1 for the first number: $24+1=25$.',
        'Check the rule on a small case: from $1$ to $5$ the odd numbers are $1, 3, 5$, and $\\frac{5-1}{2}+1=3$ ✓.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t16-' + k, TOPIC, stem, ch, cor, ex)
        M.place_q('q-r26-t16-' + k, PRACTICE)

    N = lambda k: 'q-r26-t16-' + k
    M.practice_order(PRACTICE, [
        X + '6', X + '1', X + '4', 'q-474', 'q-479', X + '2', X + '3', N('05'), N('07'), 'q-476', X + '7', N('08'),
        N('10'), X + '5', 'q-475', 'q-473', 'q-482', 'q-477', 'q-485', N('06'), N('15'), 'q-484', 'q-478', 'q-481', 'q-483',
        'q-486', 'q-487', 'q-488', N('09'), N('14'), N('11'), N('12'), N('13'), 'q-480', 'q-489', 'q-490', 'q-491',
        'q-492'])

    # =====================================================================================
    # 10. Solution videos of rewritten questions: title and slide description show the new stem
    # =====================================================================================
    for f in M.D['flow']:
        if f['topic'] != TOPIC or f['type'] != 'video': continue
        v = M.video(f['ref']); qid = v.get('questionId')
        if not qid or qid not in M.D['questions'] or f['ref'].startswith('solve-q-r26'): continue
        stem = M.q(qid)['stem']
        v['title'] = v['navLabel'] = stem
        for b in v['beats']:
            if b['mode'] == 'question' and b.get('canvas', '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, stem)
        M.touched_videos.add(f['ref'])

    summary(M)
    cut_repeats(M)   # 2026-10-05: last


# ======================================================================================================
# Pass 2: summary video right before the practice (end of the advanced section)
# ======================================================================================================
def summary(M):
    sb = ['Multiply and divide', 'Signs of sums', 'Never negative', 'Consecutive integers', 'Sums in a row',
          'Even and odd', 'Parity: plug in', 'Products in a row', 'Candidates and twos', 'Before you practice']
    C = lambda i, title, script: dict(title=title, mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice, a quick review of the whole topic.",
            "Signs, consecutive numbers, even and odd — and the traps."]),
        C(0, 'Multiply and divide', [
            "Multiplying and dividing: same rules.",
            A('Same / different', T('Same signs $\\to\\ +$ · different signs $\\to\\ -$', size=46)),
            A('Count the minuses', T('Count the minuses: odd $\\to\\ -$, even $\\to\\ +$', size=46)),
            "Only the minuses matter. Every two of them cancel.",
            A('ab > 0', T('$ab>0$: same sign — maybe both negative!', size=44)),
            "A positive product doesn't mean both are positive."]),
        C(1, 'Signs of sums', [
            "Adding has its own rules.",
            A('Two negatives', T('$(-)+(-)\\ \\to\\ -$', size=48)),
            A('Mixed', T('Mixed signs: the bigger size wins · $-9+4=-5$', size=44)),
            A('Difference', T('Bigger $-$ smaller $>0$ · $-3-(-8)=5$', size=46)),
            "Bigger minus smaller is positive — even when both are negative."]),
        C(2, 'Never negative', [
            "Find the pieces that are surely positive.",
            A('Even power', T('Even power: $x^2\\ge0$', size=46)),
            A('Odd power', T('Odd power keeps the sign: $(-3)^3=-27$', size=46)),
            A('Absolute value', T('$|y|>0$ when $y\\ne0$', size=46)),
            A('Minus x', T('$x<0\\ \\Rightarrow\\ -x>0$', size=46)),
            "Minus x means the opposite of x — not a negative number. And zero is neither positive nor negative."]),
        C(3, 'Consecutive integers', [
            "Consecutive numbers: three ways in.",
            A('Algebra', T('1 · One letter: $b-1,\\ b,\\ b+1$', size=44)),
            A('Plug in', T('2 · Plug in the smallest legal numbers', size=44)),
            A('Differences', T('3 · Differences: $b-a=1$, but $a-b=-1$', size=44)),
            "Plugging in? Make sure the choices give different values.",
            "Even or odd in a row: the gap is two.",
            "And \"greater than zero\" doesn't mean the list starts at one."]),
        C(4, 'Sums in a row', [
            "Adding numbers in a row.",
            A('Count x middle', T('Sum $=$ count $\\times$ middle · $16+\\ldots+20=5\\cdot18=90$', size=42)),
            A('Odd/even count', T('Odd count → divides by the count · even count → never', size=42)),
            A('Counting', T('From $a$ to $b$: $b-a+1$ integers', size=44)),
            A('Neighbors', T('Neighbors $a<b$: $b^2-a^2=a+b$', size=44)),
            "Four to twelve is nine numbers, not eight. Add one."]),
        C(5, 'Even and odd', [
            "Zero is even.",
            A('Add', T('Odd $\\pm$ odd $=$ even · even $\\pm$ odd $=$ odd', size=44)),
            A('Count odd terms', T('In a sum, count only the odd terms', size=44)),
            A('Multiply', T('One even factor → even · odd product ⇔ every factor odd', size=42)),
            A('Powers', T('Powers don\'t change parity — delete them', size=44)),
            "Odd divided by even is always a fraction."]),
        C(6, 'Parity: plug in', [
            "Parity questions? Plug in: two for even, one or three for odd.",
            A('One per case', T('$\\pm,\\ \\times$: one plug-in for each parity case', size=44)),
            A('Division', T('Division: three plug-ins, close together', size=44)),
            A('Proof', T('A plug-in can disprove "always" — it can\'t prove it', size=42)),
            "One example that fails kills \"always\". Examples that work prove nothing."]),
        C(7, 'Products in a row', [
            "These rules are proven. Trust them.",
            A('In a row', T('In a row: two by $2$ · three by $6$ · four by $24$', size=44)),
            A('Evens', T('Two evens by $4$ · two consecutive evens by $8$', size=44)),
            A('Hidden', T('$x^2-1=(x-1)(x+1)\\qquad x^3-x=(x-1)x(x+1)$', size=42)),
            "Watch for them hidden inside an expression.",
            "x odd? Then x squared minus one is two consecutive evens — it divides by eight."]),
        C(8, 'Candidates and twos', [
            "Anything else? The smallest case is only a candidate.",
            A('Odd in a row', T('$1\\cdot3\\cdot5=15$, but $9\\cdot11\\cdot13=1287$ → only $3$', size=44)),
            "Cross out, then test a second case that avoids the factor.",
            A('Count the twos', T('Integer? Count the twos: $\\frac{m^3(n+1)}{16}$ has four', size=44)),
            "m even, n odd: three twos from m cubed, one from n plus one. Enough for sixteen."]),
        C(9, 'Before you practice', [
            "Before each question, always ask yourself:",
            A('Check 1', T('1. Which pieces are surely positive? Which one decides?', size=40)),
            A('Check 2', T('2. Multiplying or adding? The sign rules differ.', size=40)),
            A('Check 3', T('3. Numbers in a row hiding here?', size=40)),
            A('Check 4', T('4. Did my plug-in prove it — or only fail to break it?', size=40)),
            "And the traps: zero is even, zero divides by everything, and minus x isn't always negative.",
            "You know all of this. Go practice."]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == 'whole-numbers-advanced'][-1]
    M.new_video('r26-t16-summary', TOPIC, 'Integers: Summary', sb, slides, 'whole-numbers-advanced', after=last)


# =====================================================================================
# 2026-10-05 cut repeats (helpers)
# =====================================================================================
def _cr_script(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _cr_add(M, vid, n, anchor, new, where='after'):
    """Insert script entries `new` before/after the spoken line containing `anchor` (None = at the end)."""
    sc = _cr_script(M, vid, n); out = []; hit = anchor is None
    for x in sc:
        if not hit and isinstance(x, str) and anchor in x:
            hit = True
            out += ([x] + new) if where == 'after' else (new + [x]); continue
        out.append(x)
    if anchor is None: out += new
    assert hit, '%s #%d: not found: %s' % (vid, n, anchor)
    M.set_slide(vid, n, script=out)


def _cr_say(M, vid, n, old, new):
    """Replace the whole spoken line containing `old` (new=None deletes it)."""
    def fn(lines):
        for k, l in enumerate(lines):
            if 'say' in l and old in l['say']:
                if new is None: lines.pop(k)
                else: l['say'] = new
                return lines
        raise AssertionError('%s #%d: not found: %s' % (vid, n, old))
    M.edit_lines(vid, n, fn)


def _cr_drop_item(M, vid, n, text):
    """Remove the pop-in board item whose text contains `text` (and its appear line)."""
    sc = [x for x in _cr_script(M, vid, n) if not (isinstance(x, tuple) and x[0] == 'A' and text in (x[2].get('t') or ''))]
    assert len(sc) < len(_cr_script(M, vid, n)), (vid, n, text)
    M.set_slide(vid, n, script=sc)


def _cr_cut(M, vid, titles):
    """Remove the slides with these titles; drop their sidebar labels and re-point the other slides."""
    v = M.video(vid); sb = list(v.get('hybrid', {}).get('sidebar') or [])
    ns = [k + 1 for k, b in enumerate(v['beats']) if b['title'] in titles]
    assert len(ns) == len(titles), (vid, titles, [b['title'] for b in v['beats']])
    gone = {v['beats'][n - 1]['active'] for n in ns}
    M.remove_slides(vid, ns)
    keep_used = {b['active'] for b in v['beats']}
    new_sb = [lab for k, lab in enumerate(sb) if k in keep_used]   # labels no remaining slide uses go
    for b in v['beats']:
        if 0 <= b['active'] < len(sb): b['active'] = new_sb.index(sb[b['active']])
    M.set_sidebar(vid, new_sb)


def cut_repeats(M):
    # ---- "Sums of Consecutive Integers": count x middle -> Q5 (q-r26-t16-02, + the "why" in one line);
    #      divisible by the count -> Q6 (q-r26-t16-03); even count (middle .5) -> one line in Q6.
    #      Kept: counting integers, squares of neighbors (no question video teaches them).
    _cr_cut(M, SUMS, ['Count × middle', 'Even count', 'Divisible by the count?', 'Recap'])
    M.set_slide(SUMS, 1, script=[
        'Adding consecutive numbers.',
        'The two questions after this video teach the main rule — count times middle.',
        "First, two short tools they don't use: counting the integers in a range, and squares of neighbors."])
    _cr_add(M, SUMS, 3, None, ['Two questions next. Try each one first — then watch.'])
    # Q5: why count x middle works (was the lesson's example)
    _cr_add(M, 'solve-q-r26-t16-02', 2, 'Sum equals count times middle', [
        A("'Sum = count × middle' appears", T('Sum $=$ count $\\times$ middle', size=40)),
        "Why? The numbers pair up around the middle. One below and one above together are like two middles."])
    # Q6: the even-count middle, and the rule said as a rule (no lesson slide to "remember")
    _cr_add(M, 'solve-q-r26-t16-03', 3, 'One to four: ten', [
        A("'Even count: the middle ends in .5' appears", T('Even count: the middle ends in $.5$ $\\to$ $4\\cdot2.5=10$', size=38)),
        "Count times middle still works: the middle is halfway between two and three — two and a half. Four times two and a half: ten."])
    _cr_say(M, 'solve-q-r26-t16-03', 3, 'Remember: an odd count',
            'The rule: an odd count of consecutive integers — the sum divides by the count. An even count — never.')
