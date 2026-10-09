"""Topic 18 - Exercises with Letters. Course review 2026-09 fixes.
See t18_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q
import math_api

TOPIC = 18
LESSON = 'digit-puzzles'
FACTS = 'r26-t18-facts'
THEORY = 'digit-puzzles-theory'
ADV = 'digit-puzzles-advanced'
PRACTICE = 'unit-t18-3'
ADV_SIDEBAR = ['Question %d' % n for n in range(4, 13)]


def ARR(top, mid, res):
    """Vertical exercise (same TeX layout as the existing slides)."""
    return '$\\begin{array}{r}%s\\\\%s\\\\\\hline %s\\end{array}$' % (top, mid, res)


def _say_replace(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = l['say'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _solution(M, qid, intro_tail, slides, after):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n,
                  script=['Question %s.' % math_api._word(n)] + intro_tail)]
    for title, script in slides:
        beats.append(dict(mode='question', active=n - 4, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Advanced Letter Exercises', ADV_SIDEBAR, beats, ADV,
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = 'Advanced Letter Exercises'
    v['hybrid']['num'] = 59
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


# =========================================================================================
# 1. Main lesson
# =========================================================================================
def lesson(M):
    # slide 2: the four steps - size in step 3, "or the choices" in step 4
    M.set_slide(LESSON, 2, script=[
        "Here's the technique. Four steps, every time.",
        A('Step 1 appears: write it vertically', T('1 · Write it vertically', 44)),
        "One: write the exercise vertically. Suddenly you can see things.",
        A('Step 2 appears: check the ones digit', T('2 · Check the ones digit', 44)),
        "Two: check the ones digit.",
        A('Step 3 appears: check the leftmost digit and the size', T('3 · Check the leftmost digit and the size', 44)),
        "Three: check the leftmost digit — and estimate the size.",
        A('Step 4 appears: plug in numbers or the choices', T('4 · Plug in numbers — or the choices', 44)),
        "Four: plug in numbers and see what fits. When they ask for one letter, plug in the choices.",
        D('Draw a big bracket around the four steps'),
        "Let's run it on an example — and on the way, see what the letters mean.",
    ])

    # slide 3: explain the bar notation used in every question
    def bar(lines):
        k = next(i for i, l in enumerate(lines) if 'NOT A times B' in l.get('say', ''))
        return lines[:k + 1] + [
            {'say': "On the exam you'll see a bar on top of the letters. The bar means: these letters are the digits of ONE number."},
        ] + lines[k + 1:]
    M.edit_lines(LESSON, 3, bar)

    # slide 4: the zero rule is safe only in the ones column
    M.set_slide(LESSON, 4, script=[
        'A, B, C and D are different digits. AB plus AD equals CDB.',
        "Step one — vertical. It's already on the board.",
        'Step two: the ones. B plus D ends in B.',
        D('Circle the ones column; write "D = 0"'),
        'B plus something ends in B. Nothing carries into the ones column — so that something is zero. D is zero.',
        'Step three: the leftmost digits. A plus A gives CD — and D is zero.',
        D('Write "A + A = 10"'),
        'Ten, twenty, thirty…? Two digits add up to eighteen at most. Only ten works.',
        D('Write "A = 5, C = 1"'),
        'Five plus five is ten. A is five, C is one.',
        'Notice the carry: the one from that ten went into the hundreds. Carries are part of the equation.',
        D('Write "A + C + D = 5 + 1 + 0 = 6"'),
        'Five plus one plus zero: six.',
        'Careful: "ends in the same digit, so it\'s zero" is safe only in the ones column. Next: why.',
    ])

    # new slide 5: carries
    M.insert_slides(LESSON, 4, [dict(mode='concept', active=3, title='Carries', script=[
        "Carries. This is where most mistakes happen.",
        A("'Two numbers: the carry is 0 or 1' appears", T('Two numbers: the carry is $0$ or $1$', 40)),
        "Two digits plus a carry: at most nine plus nine plus one — nineteen. So the carry is zero or one.",
        A("'Three or four numbers: the carry can be 2 or 3' appears", T('Three or four numbers: it can be $2$ or $3$', 40)),
        "Three or four numbers can carry more. Eight plus eight plus eight is twenty-four: write four, carry two.",
        A('1X7 + Y5 = 2X2 appears', T(ARR('1X7', '+\\ \\ Y5', '2X2'), 50, x=1250, y=480)),
        "Now the trap. One X seven, plus Y five, equals two X two. What is Y?",
        "Ones: seven plus five is twelve. Write two, carry one.",
        D('Write a small 1 above the tens column'),
        "Tens: X plus Y plus that one ends in X.",
        "Y zero? Then we get X plus one — that doesn't end in X. So Y plus one must be ten. Y is nine.",
        D('Write "Y + 1 = 10 → Y = 9"'),
        "That makes one more carry: the hundreds are one plus one — two. It fits.",
        D('Write "147 + 95 = 242 ✓"'),
        A("'Middle column: X + Y ends in X → Y = 0 or Y = 9' appears",
          T('Middle column: $X+Y$ ends in $X\\ \\to\\ Y=0$ or $9$', 40)),
        "So: in the ones column, \"ends in the same digit\" means zero. In any other column: zero or nine. Check the carry.",
    ])])

    # slide 6 (was 5): leading digit - "for two numbers"
    M.set_slide(LESSON, 6, active=4, script=[
        "Two rules about the leftmost digit.",
        A("'Leading digit ≠ 0' appears", T('Leading digit $\\ne 0$', 50)),
        "One: a leftmost digit is never zero. We don't write oh-eight. It's not a phone area code — it's just eight.",
        A("'Two numbers, more digits in the sum → leading digit 1' appears",
          T('Two numbers, more digits in the sum $\\to$ leading digit is $1$', 42)),
        "Two — and this one is gold: add TWO numbers, and the sum has more digits? Its leading digit is one.",
        A('99 + 99 = 198 appears', T('$99+99=198$', 56)),
        D('Circle the 1 in 198'),
        "Why? The biggest two-digit sum is ninety-nine plus ninety-nine — one ninety-eight.",
        "You can pass a hundred. You can never reach two hundred.",
        A("'Four numbers: 4 · 999 = 3996' appears", T('Four three-digit numbers: at most $4\\cdot999=3996$', 40)),
        "But careful — that's for two numbers. Four three-digit numbers can reach three thousand nine hundred ninety-six. The leading digit can be two or three.",
        "Step three is also about size. Estimate first — it throws out choices fast.",
    ])

    # slide 8 (was 7): plug in - pick different kinds of numbers; plug in the choices
    M.set_slide(LESSON, 8, active=6, script=[
        "Here's the truth: every letter question can be solved by plugging in numbers.",
        "A computer would just try every option. We're not computers — so first we look for shortcuts, then we plug in.",
        A("'AB − BA is always divisible by — ?' appears", T('$\\overline{AB}-\\overline{BA}$ is always divisible by — ?', 44, gap=130)),
        "Example: AB minus BA is always divisible by — what? There's no result to work from. So plug in.",
        D('Write "51 − 15 = 36"'),
        'AB is fifty-one. Fifty-one minus fifteen: thirty-six. Divisible by six, by nine, by four.',
        D('Write "52 − 25 = 27"'),
        'Take the next number, fifty-two. Fifty-two minus twenty-five: twenty-seven. Not by six, not by four. Only nine survives both.',
        "One warning: choose test numbers that are not alike — one even result and one odd result, for example. If two choices still survive, try a third number.",
        A('The two patterns appear', T('$\\overline{AB}-\\overline{BA}\\to$ divisible by $9$ · $\\overline{AB}+\\overline{BA}\\to$ divisible by $11$', 40)),
        'Worth remembering — it comes back on the exam. AB minus BA: always divisible by nine. AB plus BA: always divisible by eleven.',
        A("'Asked for one letter? Plug in the choices' appears", T('Asked for one letter? Plug in the choices, from the middle one.', 38)),
        "And when they ask for one letter, plug in the choices. Start from the middle one — too big or too small tells you which way to go.",
    ])

    # slide 9 (was 8): flip minus to plus - and division to multiplication
    M.edit_lines(LESSON, 9, lambda ls: ls + [
        {'say': "Same with division: flip it into a multiplication. We'll do that in question seven."}])
    M.slide(LESSON, 9)['active'] = 7

    # slide 10 (was 9): algebraic form - when to choose it
    def algebra(lines):
        return [l for l in lines if 'Some strong students' not in l.get('say', '')] + [
            {'say': "Which route? If a result is given, work the columns."},
            {'say': "If they ask what is ALWAYS true, and there's no result — plug in two numbers, or use the algebraic form. The algebraic form is the proof, and often just as fast."},
        ]
    M.edit_lines(LESSON, 10, algebra)
    M.slide(LESSON, 10)['active'] = 8

    # slide 11 (was 10): recap
    M.set_slide(LESSON, 11, active=9, script=[
        "Let's lock it in.",
        A('The four steps appear', T('1 · Vertical   2 · Ones digit   3 · Leftmost digit and size   4 · Plug in', 36)),
        "Our technique: vertical, ones digit, leftmost digit and size — then plug in.",
        A("'Ones column → 0 · middle column → 0 or 9' appears",
          T('"Ends in the same digit": ones column $\\to 0$ · other columns $\\to 0$ or $9$', 36)),
        "Ends in the same digit? In the ones column, zero. In any other column, zero or nine — check the carry.",
        A("'Special digits: 0, 1, 5, 6' appears", T('Special digits: $0,\\ 1,\\ 5,\\ 6$', 40)),
        A("'Two numbers, sum with more digits → leading 1' appears", T('Two numbers, sum with more digits $\\to$ leading digit $1$', 38)),
        A("'Subtraction → addition · division → multiplication' appears", T('Subtraction $\\to$ addition · Division $\\to$ multiplication', 38)),
        D('Circle "Plug in"'),
        "Plugging in works in almost every algebra topic — and in geometry too.",
        "One habit: a matching last digit isn't a full proof. Check the size as well.",
        "Three questions next. Try each one — then watch its solution.",
    ])
    M.set_sidebar(LESSON, ['The 4 steps', 'What letters mean', 'Worked example', 'Carries', 'Leading digit',
                           'Special digits', 'Plug in numbers', 'Minus → plus', 'Algebraic form', 'Recap'])

    # memory card of the lesson
    c = M.card('mem-letters')
    c['tables'][0]['rows'] = [['1', 'Write the exercise vertically'], ['2', 'Check the ones digit'],
                              ['3', 'Check the leftmost digit and the size'], ['4', 'Plug in numbers — or plug in the choices']]
    c['tables'][1]['rows'] = [
        ['$\\overline{AB}=10A+B$, $\\ \\overline{ABC}=100A+10B+C$', '$27=10\\cdot2+7$'],
        ['A leading digit is never $0$', 'we write $8$, not $08$'],
        ['Two numbers, sum with more digits → leading digit is $1$', '$99+99=198$'],
        ['Carry: two numbers → $0$ or $1$; three or four numbers → up to $2$ or $3$', '$8+8+8=24$: carry $2$'],
        ['Ones column: "$B+D$ ends in $B$" → $D=0$', '$5+0=5$'],
        ['Other columns: "$X+Y$ ends in $X$" → $Y=0$ or $Y=9$ (carry)', '$147+95=242$'],
        ['Special digits $0, 1, 5, 6$: $d\\cdot d$ ends in $d$', '$5\\cdot5=25,\\ 6\\cdot6=36$'],
        ['$5\\times$ even ends in $0$; $5\\times$ odd ends in $5$', '$5\\cdot4=20,\\ 5\\cdot7=35$'],
        ['$6\\times$ even keeps its ones digit', '$6\\cdot8=48$'],
        ['$\\overline{AB}-\\overline{BA}=9(A-B)$', 'always divisible by $9$'],
        ['$\\overline{AB}+\\overline{BA}=11(A+B)$', 'always divisible by $11$'],
    ]
    c['tips'] = [
        'A bar on top ($\\overline{AB}$) means: the digits of one number. $\\overline{AB}$ is not $A\\cdot B$.',
        'Flip a subtraction into an addition, and a division into a multiplication.',
        'Check whether the letters must be different digits.',
        'Asked for one letter? Plug in the choices, starting from the middle one.',
        'Plug in test numbers that are not alike. If two choices survive, try a third number.',
        'A result is given → work the columns. "Always divisible by" with no result → plug in two numbers, or use the algebraic form.',
    ]


# =========================================================================================
# 2. New lesson video: number facts (start of the advanced section) + card
# =========================================================================================
def facts(M):
    sb = ['Repdigits', 'Reversals', 'Products', 'Powers: ones digit', 'Largest and smallest', 'Recap']
    M.new_video(FACTS, TOPIC, 'Number Facts for Letter Puzzles', sb, [
        dict(mode='title', title='Number Facts', script=[
            "Number facts for letter puzzles.",
            "A few patterns come back again and again on the exam. Know them, and many questions take ten seconds.",
        ]),
        dict(mode='concept', active=0, title='Repdigits', script=[
            "First: numbers with one repeated digit.",
            A('AA = 11A appears', T('$\\overline{AA}=11A$', 54, gap=40)),
            "AA is eleven times A. Seventy-seven is eleven times seven.",
            A('AAA = 111A = 3 · 37 · A appears', T('$\\overline{AAA}=111A=3\\cdot37\\cdot A$', 54, gap=40)),
            "AAA is a hundred eleven times A. And a hundred eleven is three times thirty-seven.",
            D('Write "555 = 111 · 5 = 37 · 15"'),
            "So AAA is always divisible by three and by thirty-seven. Five fifty-five is thirty-seven times fifteen.",
            A('BBBB ÷ BB = 101 appears', T('$\\overline{BBBB}\\div\\overline{BB}=101$', 54)),
            "And BBBB divided by BB is always one hundred one. Seven thousand seven hundred seventy-seven, divided by seventy-seven: one oh one.",
        ]),
        dict(mode='concept', active=1, title='Reversals', script=[
            "Second: a number and its reversal.",
            A('AB − BA and AB + BA appear',
              T('$\\overline{AB}-\\overline{BA}=9(A-B)\\qquad\\overline{AB}+\\overline{BA}=11(A+B)$', 44, gap=40)),
            "You know these two from the first lesson.",
            A('ABC − CBA = 99(A − C) appears', T('$\\overline{ABC}-\\overline{CBA}=99(A-C)$', 54, gap=40)),
            "With three digits: ABC minus CBA is ninety-nine times A minus C. The middle digit cancels.",
            D('Write "521 − 125 = 396 = 99 · 4"'),
            "Five twenty-one minus one twenty-five: three ninety-six. That's ninety-nine times four — and five minus one is four.",
            A('Multiples of 99 appear', T('$99k$: $\\ 198,\\ 297,\\ 396,\\ \\ldots,\\ 891$', 46)),
            "Look at the multiples of ninety-nine: one ninety-eight, two ninety-seven, three ninety-six. Middle digit nine, and the outer digits add up to nine.",
            "So a difference like that is easy to spot among the choices.",
        ]),
        dict(mode='concept', active=2, title='Products', script=[
            "Third: products.",
            A("'Ones digit of a product: only the ones digits matter' appears",
              T('Ones digit of a product: only the ones digits matter', 42, gap=40)),
            D('Write "38 · 47 → 8 · 7 = 56 → ends in 6"'),
            "Thirty-eight times forty-seven. Don't multiply it all. Eight times seven is fifty-six — the product ends in six.",
            A("'Number of digits: add the counts, or one fewer' appears",
              T('Number of digits: add the two counts — or one fewer', 42, gap=40)),
            D('Write "10 · 10 = 100 (3 digits)   99 · 99 = 9801 (4 digits)"'),
            "A two-digit number times a two-digit number. Ten times ten is a hundred — three digits. Ninety-nine times ninety-nine, ninety-eight oh one — four digits.",
            "Two plus two is four digits — or one fewer, three. It always works that way.",
            "And estimate: twenty-four squared is five seventy-six, twenty-seven squared is seven twenty-nine. The size throws out choices fast.",
        ]),
        dict(mode='concept', active=3, title='Powers: ones digit', script=[
            "Fourth: the ones digit of a power.",
            A('Powers of 2 appear', T('$2,\\ 4,\\ 8,\\ 16,\\ 32,\\ 64,\\ \\ldots$', 50, gap=40)),
            "Two, four, eight, sixteen, thirty-two, sixty-four. Look only at the ones digits: two, four, eight, six — and back to two, four.",
            A('The cycles appear', T('Ones digits repeat: $2\\to2,4,8,6$ · $3\\to3,9,7,1$ · $7\\to7,9,3,1$', 40, gap=40)),
            "Every digit has a cycle like this. Four steps at most.",
            D('Write "2⁵⁰: 50 = 4 · 12 + 2 → like 2² → ends in 4"'),
            "Two to the fiftieth? The cycle has four steps. Fifty is twelve full cycles, plus two more. So it ends like two squared: four.",
            "And zero, one, five and six never change — our special digits again.",
        ]),
        dict(mode='concept', active=4, title='Largest and smallest', script=[
            "Last: the largest or smallest number with a given digit sum.",
            A("'Digit sum 8: largest 800, smallest 107' appears", T('Digit sum $8$: largest $800$ · smallest $107$', 48, gap=40)),
            "The largest three-digit number with digit sum eight: put everything on the left. Eight hundred.",
            "The smallest: the leftmost digit can't be zero, so it's one. Then zero. The rest goes on the right: seven. One oh seven.",
            D('Write "largest: big digits on the left · smallest: 1, then zeros, big digits on the right"'),
            "Largest: big digits on the left. Smallest: one first, then zeros, and the big digits on the right.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            "Let's lock it in.",
            A("'AAA = 3·37·A · ABC − CBA = 99(A − C)' appears",
              T('$\\overline{AAA}=3\\cdot37\\cdot A$ · $\\overline{ABC}-\\overline{CBA}=99(A-C)$', 40)),
            A("'Product: the ones digits decide the ones digit' appears", T('Product: the ones digits decide the ones digit', 40)),
            A("'Digits of a product: add the counts, or one fewer' appears", T('Digits of a product: add the counts, or one fewer', 40)),
            A("'Powers: the ones digits repeat in a cycle' appears", T('Powers: the ones digits repeat in a cycle', 40)),
            A("'Largest: big digits left · smallest: 1, zeros, big digits right' appears",
              T('Largest: big digits left · Smallest: $1$, zeros, big digits right', 40)),
            D('Tick each line'),
            "The next questions use these facts. Try each one first — then watch.",
        ]),
    ], ADV, before='q-515')

    M.new_card('mem-r26-t18-facts', TOPIC, ADV, {
        'title': 'Number facts for letter puzzles',
        'intro': 'Patterns that come back on the exam. Each one with an example.',
        'tables': [{'title': 'Facts', 'head': ['Fact', 'Example'], 'rows': [
            ['$\\overline{AA}=11A$, $\\ \\overline{AAA}=111A=3\\cdot37\\cdot A$', '$555=37\\cdot15$'],
            ['$\\overline{BBBB}\\div\\overline{BB}=101$', '$7777\\div77=101$'],
            ['$\\overline{AB}-\\overline{BA}=9(A-B)$, $\\ \\overline{AB}+\\overline{BA}=11(A+B)$', '$52-25=27$, $\\ 52+25=77$'],
            ['$\\overline{ABC}-\\overline{CBA}=99(A-C)$', '$521-125=396=99\\cdot4$'],
            ['Multiples of $99$: middle digit $9$, outer digits add up to $9$', '$198,\\ 297,\\ \\ldots,\\ 891$'],
            ['Ones digit of a product: multiply only the ones digits', '$38\\cdot47$: $8\\cdot7=56\\to6$'],
            ['Digits of a product: add the two counts, or one fewer', '$10\\cdot10=100$, $\\ 99\\cdot99=9801$'],
            ['Ones digits of powers repeat', '$2\\to2,4,8,6$; $\\ 3\\to3,9,7,1$; $\\ 7\\to7,9,3,1$'],
            ['Largest with a digit sum: big digits on the left', 'digit sum $8$: $800$'],
            ['Smallest with a digit sum: $1$, then zeros, big digits on the right', 'digit sum $8$: $107$'],
        ]}],
        'tips': [
            'The ones digit of $2^{50}$: the cycle has 4 steps, $50=4\\cdot12+2$, so it ends like $2^2$: $4$.',
            'Estimate the size first: $24^2=576$, $27^2=729$.',
        ]}, after=FACTS)


# =========================================================================================
# 3. Existing guided questions and their videos
# =========================================================================================
def guided_existing(M):
    S = M.set_q
    S('q-512', stem='A, B, C and D represent digits. Given: $\\overline{AB}+\\overline{CB}=\\overline{DDB}$\n$A+C+D=?$', expl=[
        'Write it vertically. Ones column: $B+B$ ends in $B$. Nothing carries into the ones column, so $B=0$.',
        'Two two-digit numbers give a three-digit number, so the leading digit is 1: $D=1$.',
        'Tens column: $A+C$ (nothing carries in, because $0+0=0$) gives the tens digit 1 and carries 1 into the hundreds. So $A+C=11$.',
        '$A+C+D=11+1=12$. Check: $A=5$, $C=6$: $50+60=110$ ✓.'])
    S('q-513', stem='A, B and C represent digits. Given: $\\overline{BA}\\times A=\\overline{CA}$\nWhich of the following could be A?', expl=[
        'Ones column: $A\\times A$ ends in $A$. Only the special digits do this: $0, 1, 5, 6$ ($0\\cdot0=0$, $1\\cdot1=1$, $5\\cdot5=25$, $6\\cdot6=36$).',
        'Choices (2) and (3) fail: $3\\cdot3=9$ and $2\\cdot2=4$.',
        'Choice (4) fails: $A=0$ makes the product $0$, not a two-digit number.',
        'Choice (1): $A=6$ and $B=1$ give $16\\times6=96$ ✓.'])
    S('q-514', stem='A and B represent nonzero digits. Which of the following necessarily divides $\\overline{AB}+\\overline{BA}$?', expl=[
        'Plug in two different numbers. $51+15=66$: it is not divisible by 9 or by 4, so choices (1) and (4) are out.',
        '$52+25=77$: it is not divisible by 6, so choice (2) is out. Only 11 is left.',
        'Why it always works: $\\overline{AB}+\\overline{BA}=(10A+B)+(10B+A)=11A+11B=11(A+B)$.'])
    S('q-515', stem='A, B and C represent digits. Given: $\\overline{ABC}+\\overline{AB}=\\overline{CCC}$\n$B=?$', expl=[
        'Ones column: $C+B$ ends in $C$. Nothing carries into the ones column, so $B=0$.',
        'Check the tens: $B+A=0+A$, so $A=C$. For example: $202+20=222$ ✓.'])
    S('q-516', stem='A, B and C represent digits. Given: $\\overline{AAA}-37=\\overline{BC}$\n$B+C=?$',
      choices=['$\\overline{AA}$', '$\\overline{AB}$', '$\\overline{AC}$', '$\\overline{BC}$'], expl=[
        'Flip the subtraction into an addition: $\\overline{BC}+37=\\overline{AAA}$.',
        'Two two-digit numbers give a three-digit number, so the leading digit is 1: $A=1$ and $\\overline{AAA}=111$.',
        '$111-37=74$, so $B=7$, $C=4$ and $B+C=11$.',
        '$A=1$, so $\\overline{AA}=11$. The other choices: $\\overline{AB}=17$, $\\overline{AC}=14$, $\\overline{BC}=74$.'])
    S('q-517', stem='A, B and C represent digits. Given: $\\overline{AB}\\times\\overline{AB}=\\overline{6CB}$\nWhich of the following could be $B-A$?', expl=[
        'Size first: $24^2=576$ is too small, and $27^2=729$ is too big. So $\\overline{AB}$ is 25 or 26, and $A=2$.',
        'Ones column: $B\\times B$ ends in $B$, so B is a special digit. Here $B=5$ or $B=6$.',
        '$25^2=625$ ✓ gives $B-A=5-2=3$, which is not a choice. $26^2=676$ ✓ gives $B-A=6-2=4$.'])
    S('q-518', stem='A, B and C represent digits. Given: $\\frac{\\overline{CBA}}{\\overline{AA}}=13$\n$A+B+C=?$', expl=[
        'Flip the division into a multiplication: $\\overline{AA}\\times13=\\overline{CBA}$.',
        'Ones column: $3\\times A$ ends in $A$. So $2A$ ends in 0: $A=0$ or $A=5$. $A=0$ is not possible, because $\\overline{AA}$ is a two-digit number. So $A=5$.',
        '$55\\times13=550+165=715$, so $C=7$, $B=1$ and $A=5$.',
        '$A+B+C=5+1+7=13$.'])
    S('q-519', stem='A, B, C and D represent different digits, and each of them is a prime number. Given: $\\overline{AC}+\\overline{CD}=\\overline{BA}$\n$C=?$', expl=[
        'The prime digits are 2, 3, 5 and 7. There are four different letters, so each prime digit is used once.',
        'Plug in the choices. $C=2$: take $D=3$. The ones column gives $2+3=5$, so $A=5$. Tens: $5+2=7=B$. Check: $52+23=75$ ✓.',
        'The other choices fail. $C=5$: $D=2$ gives $75+52=127$ (three digits), $D=3$ makes $A=8$, $D=7$ gives $25+57=82$ ($B=8$).',
        '$C=3$: $D=2$ gives $53+32=85$ ($B=8$), $D=5$ makes $A=8$, $D=7$ makes $A=0$. $C=7$: $D=2$ makes $A=9$, $D=3$ makes $A=0$, $D=5$ gives $27+75=102$.'])
    S('q-520', stem='x is a two-digit number. x is equal to the cube of its ones digit plus the sum of its digits. What is the tens digit of x?', expl=[
        'Plug in the choices for the tens digit T. Call the ones digit U, so $x=10T+U$.',
        '$T=3$: $30+U=U^3+3+U$, so $U^3=27$ and $U=3$. Check: $x=33$, and $3^3+3+3=27+6=33$ ✓.',
        'The other choices fail: $T=5$ gives $U^3=45$, $T=2$ gives $U^3=18$, $T=4$ gives $U^3=36$. None of them is a cube.',
        'Algebraic form: $10T+U=U^3+T+U$, so $9T=U^3$ — the same test.'])

    for qid in ['q-512', 'q-513', 'q-514', 'q-515', 'q-516', 'q-517', 'q-518', 'q-519', 'q-520']:
        v = M.video('solve-' + qid); v['title'] = v['navLabel'] = M.q(qid)['stem']

    # Q1: why B = 0 (ones column)
    _say_replace(M, 'solve-q-512', 2, 'Add B to B and land back on B? Only zero does that. B is zero.',
                 'Add B to B and land back on B? This is the ones column — nothing carries in. Only zero does that. B is zero.')
    # Q4: same
    _say_replace(M, 'solve-q-515', 2, 'So go to the ones. C plus B gives C.', 'So go to the ones. C plus B ends in C.')
    _say_replace(M, 'solve-q-515', 2, 'C plus something, back to C. That something is zero. B is zero.',
                 "C plus something, back to C. It's the ones column, so nothing carries in: that something is zero. B is zero.")
    _say_replace(M, 'solve-q-515', 2, 'Quick check: the tens are B plus A, which is just A — so A equals C.',
                 'Quick check: nothing carries, so the tens are B plus A — just A. So A equals C.')
    # Q7: delete the confusing "five-rule" half-sentence
    _say_replace(M, 'solve-q-518', 2,
                 "With a five here we'd use the five-rule. Here it's a three: three A ending in A means two A ends in zero — so A is zero or five. Three times five: fifteen. Ends in five.",
                 "Three A ending in A means two A ends in zero — so A is zero or five. Three times five: fifteen. It ends in five.")
    # Q8: American spelling
    _say_replace(M, 'solve-q-519', 1, 'organised', 'organized')
    # Q9: "ones digit" (the lesson's word) and a real plug-in method 2
    for n in (2, 3):
        _say_replace(M, 'solve-q-520', n, 'units digit', 'ones digit')
    M.set_slide('solve-q-520', 3, title='Method 2 · Plug in the choices', script=[
        "Method two: plug in the choices. They offer the tens digit — try each one as T.",
        D('Write "T = 3: 30 + U = U³ + 3 + U"'),
        "Try three. The number is thirty plus U. The condition: U cubed, plus three, plus U.",
        D('Write "→ U³ = 27 → U = 3"'),
        "Take U and three away from both sides: U cubed is twenty-seven. U is three — a real digit. It works.",
        D('Write "33: 27 + 3 + 3 = 33 ✓" and circle choice 3'),
        "Check: thirty-three. Three cubed, plus three, plus three — thirty-three. Choice three.",
        D('Next to choices 1, 2 and 4 write "U³ = 45, 18, 36 ✗"'),
        "The others work the same way: five gives U cubed forty-five, two gives eighteen, four gives thirty-six. None is a cube.",
    ])
    _say_replace(M, 'solve-q-520', 1, 'Two ways: the math, then plugging in the answers.',
                 'Two ways: the math, then plugging in the choices.')

    for vid in ['solve-q-515', 'solve-q-516', 'solve-q-517', 'solve-q-518', 'solve-q-519', 'solve-q-520']:
        M.set_sidebar(vid, ADV_SIDEBAR)


# =========================================================================================
# 4. New guided questions 10-12 (end of the advanced section)
# =========================================================================================
def guided_new(M):
    g1, g2, g3 = ['q-r26-t18-%02d' % k for k in (1, 2, 3)]

    M.new_q(g1, TOPIC, 'A and B represent digits. Given: $\\overline{2A6}+\\overline{B8}=\\overline{3A4}$\n$B=?$',
            ['$0$', '$1$', '$8$', '$9$'], 4, [
        'Ones column: $6+8=14$. Write 4 and carry 1 into the tens.',
        'Tens column: $A+B+1$ ends in $A$. So $B+1$ ends in 0: $B+1=10$ and $B=9$. This carries 1 again.',
        'Hundreds column: $2+1=3$ ✓.',
        'The trap is $B=0$: it forgets the carry. Check with $A=5$: $256+98=354$ ✓.'])
    M.place_q(g1, ADV, after='solve-q-520')
    _solution(M, g1, ["A middle column with a carry. Watch for the trap."], [
        ('Carry in the tens', [
            "Step one: vertical.",
            A('The vertical layout appears: 2A6 + B8 = 3A4', T(ARR('2A6', '+\\ \\ B8', '3A4'), 50, x=1150, y=330)),
            "Step two: the ones. Six plus eight is fourteen. Write four — it matches. Carry one.",
            D('Write a small 1 above the tens column'),
            "Tens: A plus B plus one ends in A.",
            "The trap: \"ends in A, so B is zero\". But there's a carry! A plus zero plus one ends in A plus one — not A.",
            D('Cross out choice 1'),
            "So B plus one must be ten. B is nine.",
            D('Write "B + 1 = 10 → B = 9"'),
            "That's another carry. The hundreds: two plus one — three. It fits.",
            D('Circle choice 4'),
            "Choice four.",
        ]),
        ('Plug in to check', [
            "Check with any A. Take A equal to five.",
            D('Write "256 + 98 = 354 ✓"'),
            "Two fifty-six plus ninety-eight: three fifty-four. Three, five, four — it fits. Choice four.",
        ]),
    ], after=g1)

    M.new_q(g2, TOPIC, 'A, B and C represent digits, and $A>C>0$. Which of the following could be the value of $\\overline{ABC}-\\overline{CBA}$?',
            ['$459$', '$484$', '$495$', '$540$'], 3, [
        '$\\overline{ABC}-\\overline{CBA}=99(A-C)$, so the result is a multiple of 99.',
        'Multiples of 99 up to 891 have middle digit 9, and their outer digits add up to 9: $198, 297, 396, 495, \\ldots$',
        '$459$, $484$ and $540$ do not have middle digit 9. $495=99\\cdot5$ ✓.',
        'Check: $A-C=5$, for example $621-126=495$ ✓.'])
    M.place_q(g2, ADV, after='solve-' + g1)
    _solution(M, g2, ["A number minus its reversal. Use the ninety-nine fact."], [
        ('Multiples of 99', [
            "ABC minus CBA is ninety-nine times A minus C.",
            D('Write "ABC − CBA = 99(A − C)"'),
            "So the answer must be a multiple of ninety-nine.",
            "Multiples of ninety-nine: middle digit nine, and the outer digits add up to nine.",
            D('Write "99k: 198, 297, 396, 495, …"'),
            "Four fifty-nine: middle digit five. Out. Four eighty-four: middle eight. Out. Five forty: middle four. Out.",
            D('Cross out choices 1, 2 and 4'),
            "Four ninety-five: middle nine, and four plus five is nine. It's ninety-nine times five.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Plug in to check', [
            "Check: A minus C must be five. Take six, two, one.",
            D('Write "621 − 126 = 495 ✓"'),
            "Six twenty-one minus one twenty-six: four ninety-five. It works. Choice three.",
        ]),
    ], after=g2)

    M.new_q(g3, TOPIC, 'A and B represent digits. Which of the following could be the value of $\\overline{A3}\\times\\overline{B7}$?',
            ['$91$', '$851$', '$857$', '$10{,}001$'], 2, [
        'Ones digit: only the ones digits decide. $3\\cdot7=21$, so the product ends in 1. Choice (3) is out.',
        'Size: the smallest product is $13\\cdot17=221$ and the largest is $93\\cdot97=9021$. So $91$ is too small and $10{,}001$ is too big.',
        'Only $851$ is left. Check: $23\\cdot37=690+161=851$ ✓.'])
    M.place_q(g3, ADV, after='solve-' + g2)
    _solution(M, g3, ["A product with letters. We don't need the letters — just two facts."], [
        ('Ones digit and size', [
            "Fact one: only the ones digits decide the ones digit.",
            D('Write "3 · 7 = 21 → ends in 1"'),
            "Three times seven is twenty-one. The product ends in one.",
            D('Cross out choice 3'),
            "Eight fifty-seven ends in seven. Out.",
            "Fact two: the size. Two-digit times two-digit gives three or four digits.",
            D('Write "13 · 17 = 221 (smallest)   93 · 97 = 9021 (largest)"'),
            "The smallest possible: thirteen times seventeen, two twenty-one. The largest: ninety-three times ninety-seven, about nine thousand.",
            D('Cross out choices 1 and 4'),
            "Ninety-one is too small. Ten thousand and one is too big — five digits.",
            D('Circle choice 2'),
            "Only eight fifty-one is left. Choice two.",
        ]),
        ('Check', [
            "Can we really get it? Try twenty-three times thirty-seven.",
            D('Write "23 · 37 = 690 + 161 = 851 ✓"'),
            "Twenty-three times thirty is six ninety. Twenty-three times seven, one sixty-one. Eight fifty-one. It's real.",
        ]),
    ], after=g3)


# =========================================================================================
# 5. Practice: rewrite every question, remove two, add seven, order easy -> hard
# =========================================================================================
def practice(M):
    S = M.set_q
    S('q-521', stem='A is a two-digit number and B is a four-digit number. Which of the following is true about $A+B$?',
      choices=['It can only be a four-digit number.', 'It can only be a five-digit number.',
               'It can be a three-digit or a four-digit number.', 'It can be a four-digit or a five-digit number.'], expl=[
        'Smallest sum: $10+1000=1010$ (four digits). Largest sum: $99+9999=10098$ (five digits).',
        'So $A+B$ can be a four-digit or a five-digit number.'])
    S('q-522', stem='A and B represent different nonzero digits. Given: $\\overline{AB}\\times2=\\overline{1B0}$\n$A-B=?$', expl=[
        'Ones column: $2\\times B$ ends in 0. B is not 0, so $B=5$.',
        'Then $\\overline{1B0}=150$, and $\\overline{AB}=150\\div2=75$. So $A=7$.',
        '$A-B=7-5=2$. Check: $75\\times2=150$ ✓.'])
    S('q-523', stem='A, B and C represent consecutive digits, and $A<B<C$. Given: $A+B+C=\\overline{1B}$\nWhat is $A+B+C$?', expl=[
        'Three consecutive digits: the sum is 3 times the middle one, $3B$.',
        '$\\overline{1B}=10+B$, so $3B=10+B$. Therefore $2B=10$ and $B=5$.',
        'The digits are 4, 5 and 6, and the sum is $15=\\overline{1B}$ ✓.',
        'Or plug in the choices: the sum ends in B and equals $3B$. Only $15=3\\cdot5$ works ($18\\ne3\\cdot8$, $12\\ne3\\cdot2$).'])
    S('q-524', stem='A and B represent nonzero digits. Given: $\\overline{AB}-\\overline{BA}=27$\n$A-B=?$', expl=[
        '$\\overline{AB}-\\overline{BA}=9(A-B)$.',
        '$9(A-B)=27$, so $A-B=3$. Check: $52-25=27$ ✓.'])
    S('q-525', stem='A and B represent nonzero digits. Given: $\\overline{AB}\\times B=\\overline{B4}$\n$A+B=?$', expl=[
        'Ones column: $B\\times B$ ends in 4. $2\\cdot2=4$ and $8\\cdot8=64$, so $B=2$ or $B=8$.',
        '$B=8$: $\\overline{A8}\\times8$ is at least $18\\times8=144$ — too big for a two-digit result. So $B=2$.',
        '$\\overline{A2}\\times2=24$, so $\\overline{A2}=12$ and $A=1$. $A+B=1+2=3$.'])
    S('q-526', stem='A, B and C represent consecutive digits, and $A<B<C$. Given: $\\overline{ABC}+\\overline{CCC}=\\overline{D00}$\n$A=?$', expl=[
        'Ones column: $C+C$ ends in 0, so $C=0$ or $C=5$. C is the largest of three consecutive digits, so $C=5$, and 1 carries.',
        'Then $B=4$ and $A=3$. Tens column: $4+5+1=10$, so it ends in 0 ✓.',
        'Check: $345+555=900$ ✓.'])
    S('q-527', stem='X is a four-digit number. X is the sum of four three-digit numbers. Which of the following could be the thousands digit of X?', expl=[
        'Four three-digit numbers add up to at most $4\\cdot999=3996$.',
        'So the thousands digit of X is 1, 2 or 3. Only 3 is a choice. Example: $999+999+999+999=3996$.',
        'The "leading digit 1" rule is only for the sum of two numbers.'])
    S('q-528', stem='A, B, C and D represent consecutive digits, and $A<B<C<D$. Given: $k=\\overline{AB}+\\overline{CD}+31$\nWhich of the following necessarily divides k?', expl=[
        'Plug in $A=1$: $k=12+34+31=77$. 77 is not divisible by 2, 3 or 9. Only 11 is left.',
        'Check with $A=2$: $23+45+31=99=11\\cdot9$ ✓.',
        'Algebraic form (always true): $\\overline{AB}=10A+(A+1)=11A+1$ and $\\overline{CD}=10(A+2)+(A+3)=11A+23$. So $k=22A+55=11(2A+5)$.'])
    S('q-529', expl=[
        'Largest: put as much as possible in the leftmost digit: $n=800$.',
        'Smallest: the hundreds digit is at least 1. Then the smallest tens digit, 0, and the rest in the ones: $m=107$.',
        '$n-m=800-107=693$.'])
    S('q-530', stem='X is a two-digit number whose ones digit is 5. When we reverse the order of its digits, we get $3(X+2)$. What is the sum of the digits of X?', expl=[
        'Plug in the choices. The digit sum minus 5 is the tens digit: choice (1) gives $X=15$, (2) gives $X=35$, (3) gives $X=55$, (4) gives $X=75$.',
        '$X=15$: the reversed number is 51, and $3(15+2)=51$ ✓.',
        'The others fail. For example, $X=35$: the reversed number is 53, but $3(35+2)=111$.'])
    S('q-531', stem='A, B and C represent nonzero digits. $\\frac{\\overline{AC}+\\overline{CB}+\\overline{BA}}{A+B+C}=?$', expl=[
        'Plug in $A=1$, $B=2$, $C=3$: $\\frac{13+32+21}{6}=\\frac{66}{6}=11$. Another try, $A=B=C=1$: $\\frac{33}{3}=11$.',
        'Algebraic form: each letter appears once in the tens and once in the ones. So the sum is $11A+11B+11C=11(A+B+C)$, and the quotient is always 11.'])
    S('q-532', stem='Two three-digit numbers are made of the same three digits, in a different order. Their tens digits are equal. In one of the numbers, the hundreds digit is 4 more than the ones digit. What is the difference between the two numbers?', expl=[
        'Same digits and the same tens digit, so the hundreds digit and the ones digit swap: the numbers are $\\overline{ABC}$ and $\\overline{CBA}$.',
        '$\\overline{ABC}-\\overline{CBA}=99(A-C)=99\\cdot4=396$.',
        'Example: $521-125=396$ ✓.'])
    S('q-533', stem='A and B represent different nonzero digits. Given: $\\overline{BA}+A=\\overline{AB}$\n$A=?$', expl=[
        'Tens column: B plus the carry gives A. A and B are different, so the carry is 1 and $A=B+1$.',
        'Ones column: $A+A=10+B$ (it carries 1). With $B=A-1$: $2A=10+A-1$, so $A=9$ and $B=8$.',
        'Check: $89+9=98$ ✓. (Or plug in the choices: only $A=9$ works.)'])
    S('q-534', stem='A, B and C represent digits. Given: $\\overline{ABC}-\\overline{BBB}=198$\n$A-C=?$', expl=[
        'Flip it into an addition: $\\overline{BBB}+198=\\overline{ABC}$.',
        'Tens column: $B+9$ must end in $B$. That works only with a carry of 1 from the ones: $B+9+1=B+10$ ✓, and 1 carries into the hundreds.',
        'Ones column: $B+8$ carries 1, so $C=B+8-10=B-2$. Hundreds column: $B+1+1=A$, so $A=B+2$.',
        '$A-C=(B+2)-(B-2)=4$. Check with $B=3$: $333+198=531$, and $5-1=4$ ✓.'])
    S('q-535', stem='A and B represent different digits. Given: $\\overline{1A}\\times B=\\overline{9B}$\nWhich of the following could be A?', expl=[
        'Plug in the choices. $A=9$: $19\\times B$ must be in the 90s, so $B=5$: $19\\times5=95=\\overline{9B}$ ✓.',
        '$A=7$: $17\\times5=85$ and $17\\times6=102$ — never in the 90s. $A=3$: $13\\times7=91$, which ends in 1, not in $B=7$. $A=4$: $14\\times7=98$, which ends in 8, not in $B=7$.'])
    S('q-536', stem='A, B and C represent digits. Given: $\\overline{AA}\\times\\overline{BB}=\\overline{ACA}$\nWhich of the following could be $\\overline{AA}$?', expl=[
        'Try each choice with the smallest BB, 11:',
        '$77\\times11=847$, $55\\times11=605$ and $66\\times11=726$: the first and last digits are different ✗. $33\\times11=363$ ✓ ($A=3$, $C=6$).',
        'A bigger BB does not help 55, 66 or 77: $55\\times22=1210$, $66\\times22=1452$ and $77\\times22=1694$ have four digits.'])
    S('q-537', stem='A and B represent different digits from 1 to 7. When $\\overline{AB}$ is divided by 11, the remainder is less than 3. Which of the following cannot be A?', expl=[
        'Plug in the choices. For $A=7$, $\\overline{AB}$ is one of 71, 72, 73, 74, 75, 76. $77=7\\cdot11$, so these leave the remainders 5, 6, 7, 8, 9, 10 — never less than 3. So A cannot be 7.',
        'The others work: $12=11+1$, $23=22+1$ and $67=66+1$ (remainder 1).'])
    S('q-538', stem='A and B represent nonzero digits. $\\overline{AB}$ is a two-digit prime number. The sum of its digits is 4 times its ones digit. $A+B=?$', expl=[
        '$A+B=4B$, so $A=3B$. The options are 31, 62 and 93.',
        '62 and 93 are not prime: $62=2\\cdot31$ and $93=3\\cdot31$. So $\\overline{AB}=31$ and $A+B=4$.'])
    S('q-539', stem='A and B represent digits, and $B\\ne0$. Given: $\\overline{BBBB}\\div\\overline{BB}=\\overline{A0A}$\n$A=?$', expl=[
        'Plug in $B=1$: $1111\\div11=101$. So $\\overline{A0A}=101$ and $A=1$.',
        'It works for every B: $\\overline{BBBB}=1111B$ and $\\overline{BB}=11B$, so the quotient is $\\frac{1111B}{11B}=101$. Check: $7777\\div77=101$ ✓.'])
    S('q-540', stem='A and B represent nonzero digits. Given: $\\overline{1AB}-\\overline{BA}=\\overline{B3}$\n$A+B=?$', expl=[
        'Flip it into an addition: $\\overline{BA}+\\overline{B3}=\\overline{1AB}$.',
        'Ones column: $A+3$ ends in $B$. If it carried, B would be 0, 1 or 2, and the tens $B+B$ could not reach 10. So nothing carries and $B=A+3$.',
        'Plug in the choices: $A+B=11$ gives $A=4$ and $B=7$. Check: $147-74=73=\\overline{B3}$ ✓.',
        'The others fail: $A=5$, $B=8$ gives $158-85=73\\ne83$. $A=6$, $B=9$ gives $169-96=73\\ne93$. $A+B=17$ would need $B=10$.'])

    X = 'alg-extra-unit-t18-3-'
    # Pass 2: the original question (the ratio A : B) is back; the A + B version is dropped
    S(X + '2', stem='A and B represent digits, and $A\\ne0$. Given: $\\overline{AB}=6(A+B)$\nWhat is the ratio $A:B$?',
      choices=['$2:3$', '$5:4$', '$4:5$', '$3:2$'], correct=2, expl=[
        'Algebraic form: $\\overline{AB}=10A+B$, so $10A+B=6A+6B$.',
        'Therefore $4A=5B$, and the ratio is $A:B=5:4$.',
        'Check: $A=5$, $B=4$: $54=6\\cdot(5+4)=6\\cdot9$ ✓.'])
    S(X + '3', stem='What is the ones digit of $38\\times47$?', choices=['$8$', '$6$', '$2$', '$4$'], expl=[
        'Only the ones digits decide the ones digit of a product: $8\\times7=56$, which ends in 6.',
        'Check: $38\\times47=1786$ ✓.'])
    S(X + '5', stem='A represents a nonzero digit. The three-digit number $\\overline{AAA}$ is necessarily divisible by which of the following?',
      choices=['$9$', '$37$', '$2$', '$5$'], expl=[
        '$\\overline{AAA}=111A=3\\cdot37\\cdot A$, so it is always divisible by 37 (and by 3).',
        'The others fail for $A=1$: 111 is not divisible by 9, 2 or 5.'])
    S(X + '6', stem='A two-digit number is 4 times the sum of its digits. Its tens digit is 2. What is its ones digit?', choices=['$4$', '$2$', '$6$', '$8$'], expl=[
        'Plug in the choices: $24=4\\cdot(2+4)$ ✓.',
        'The others fail: $22\\ne4\\cdot4$, $26\\ne4\\cdot8$, $28\\ne4\\cdot10$.',
        'Algebraic form: $20+b=4(2+b)$, so $12=3b$ and $b=4$.'])
    S(X + '7', stem='A and B represent digits. Given: $\\overline{4A}+\\overline{4A}=\\overline{9B}$\nWhat must A be at least?',
      choices=['$5$', '$2$', '$3$', '$4$'], expl=[
        'Tens column: $4+4=8$, but the tens digit of the result is 9. So 1 must carry from the ones column.',
        'Ones column: $A+A$ must be at least 10, so $A\\ge5$. $A=5$ works: $45+45=90$ ✓ ($B=0$).'])
    # Pass 2 (teacher's plan): both originals are back. X + '1' stays here; X + '4' (counting) moves to the T28 practice.
    S(X + '1', stem='A two-digit number has a digit sum of 11. When its digits are reversed, the new number is 27 smaller. What is the original number?',
      choices=['$74$', '$47$', '$65$', '$83$'], correct=1, expl=[
        'Call the tens digit A and the ones digit B:\n$\\begin{cases} A+B=11 \\\\ \\overline{AB}-\\overline{BA}=27 \\end{cases}$',
        '$\\overline{AB}-\\overline{BA}=9(A-B)=27$, so $A-B=3$.',
        'Add $A+B=11$ and $A-B=3$: $2A=14$, so $A=7$ and $B=4$. The number is 74.',
        'Check: $7+4=11$ and $74-47=27$ ✓.'])
    S(X + '4', stem='How many three-digit numbers can be made from the digits 2, 5 and 8, if no digit is repeated?',
      choices=['$9$', '$27$', '$6$', '$3$'], correct=3, expl=[
        'Hundreds digit: 3 options. Tens digit: 2 digits are left. Ones digit: 1 digit is left.',
        '$3\\cdot2\\cdot1=6$. The numbers: 258, 285, 528, 582, 825, 852.'])
    first28 = next(f['ref'] for f in M.D['flow'] if f['section'] == 'wp28-practice' and f['type'] == 'question')
    M.move(X + '4', 'wp28-practice', before=first28)

    # new exam-level practice
    P = {}
    P['04'] = ('A represents a digit. Given: $\\overline{A8}+\\overline{A8}+\\overline{A8}=\\overline{1A4}$\n$A=?$',
               ['$2$', '$4$', '$6$', '$9$'], 2, [
        'Ones column: $8+8+8=24$. Write 4 and carry 2 (three numbers can carry more than 1).',
        'Tens column: $A+A+A+2$ ends in $A$. So $2A+2$ ends in 0: $A=4$ or $A=9$.',
        '$A=9$: $27+2=29$ carries 2, so the hundreds digit would be 2, not 1 ✗. $A=4$: $12+2=14$, tens digit 4, carry 1 ✓.',
        'Check: $48+48+48=144$ ✓.'])
    P['05'] = ('A, B and C represent digits. Given: $\\overline{4AB}+\\overline{CB}=\\overline{5A0}$\n$B+C=?$',
               ['$5$', '$9$', '$10$', '$14$'], 4, [
        'Ones column: $B+B$ ends in 0, so $B=0$ or $B=5$.',
        '$B=0$: nothing carries, and the tens column says $A+C$ ends in $A$. Then $C=0$ — impossible, because C is a leading digit. So $B=5$, and 1 carries.',
        'Tens column: $A+C+1$ ends in $A$, so $C+1=10$ and $C=9$. Another 1 carries: hundreds $4+1=5$ ✓.',
        '$B+C=5+9=14$. Check with $A=2$: $425+95=520$ ✓.'])
    P['06'] = ('X is a three-digit number and Y is a two-digit number. How many digits can the product $X\\cdot Y$ have?',
               ['$4$ only', '$5$ only', '$4$ or $5$', '$5$ or $6$'], 3, [
        'Smallest product: $100\\cdot10=1000$ (4 digits). Largest product: $999\\cdot99=98901$ (5 digits).',
        'The rule: add the two counts ($3+2=5$), or one fewer (4).'])
    P['07'] = ('A, B and C represent digits. What is the ones digit of $\\overline{A7}\\times\\overline{B3}\\times\\overline{C9}$?',
               ['$1$', '$3$', '$9$', 'It cannot be determined from the information given.'], 3, [
        'Only the ones digits decide: $7\\cdot3=21$ ends in 1, and $1\\cdot9=9$.',
        'So the ones digit is 9, whatever A, B and C are. Check: $17\\cdot13\\cdot19=4199$ ✓.'])
    P['08'] = ('What is the ones digit of $2^{50}$?', ['$2$', '$4$', '$6$', '$8$'], 2, [
        'The ones digits of the powers of 2 repeat: $2, 4, 8, 6$, then $2, 4, 8, 6$ again ($2^5=32$). The cycle has 4 steps.',
        '$50=4\\cdot12+2$, so $2^{50}$ ends like $2^2=4$.'])
    P['09'] = ('A represents a nonzero digit. Given: $\\overline{AAA}\\div37=\\overline{1A}$\n$A=?$',
               ['$3$', '$4$', '$5$', '$6$'], 3, [
        '$\\overline{AAA}=111A=3\\cdot37\\cdot A$, so $\\overline{AAA}\\div37=3A$.',
        '$3A=\\overline{1A}=10+A$, so $2A=10$ and $A=5$.',
        'Check: $555\\div37=15$ ✓.'])
    P['10'] = ('A, B and C represent digits. $\\overline{ABC}$ and $\\overline{CBA}$ are three-digit numbers. Given:\n'
               '$\\begin{cases} \\overline{ABC}-\\overline{CBA}=693 \\\\ B=A+C \\end{cases}$\n$\\overline{ABC}=?$',
               ['$792$', '$891$', '$990$', '$781$'], 2, [
        '$\\overline{ABC}-\\overline{CBA}=99(A-C)=693$, so $A-C=7$.',
        'C is the leading digit of $\\overline{CBA}$, so $C\\ge1$. The options: $A=8$ and $C=1$, or $A=9$ and $C=2$.',
        '$B=A+C$ must be a digit: $8+1=9$ works, $9+2=11$ does not. So $\\overline{ABC}=891$.',
        'Check: $891-198=693$ ✓.'])
    for k, (stem, ch, cor, ex) in P.items():
        qid = 'q-r26-t18-' + k
        M.new_q(qid, TOPIC, stem, ch, cor, ex)
        M.place_q(qid, PRACTICE)

    N = lambda k: 'q-r26-t18-%02d' % k
    M.practice_order(PRACTICE, [
        X + '3', 'q-521', N(6), X + '5', 'q-524', X + '1', 'q-523', X + '6', 'q-539', 'q-522', 'q-525', X + '2',
        N(7), N(8), 'q-527', 'q-529', X + '7', 'q-531', 'q-528', 'q-530', 'q-538', 'q-532', N(9),
        'q-526', 'q-533', 'q-535', 'q-534', N(5), N(4), 'q-536', 'q-537', N(10), 'q-540'])


def apply(M):
    lesson(M)
    facts(M)
    guided_existing(M)
    guided_new(M)
    practice(M)
    summary(M)
    cut_repeats(M)   # 2026-10-05: last


# =========================================================================================
# Pass 2: summary lesson right before the practice (the topic has one practice section)
# =========================================================================================
def summary(M):
    sb = ['Letters are digits', 'The 4 steps', 'The ones column', 'Leading digit & size', 'Special digits',
          'Plug in', 'Algebraic form', 'Products & powers', 'Largest & smallest', 'Before you practice']
    C = lambda i, script: dict(title=sb[i], mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — all of letter puzzles in a few minutes.",
            "Every rule, every trap. Short and fast.",
        ]),
        C(0, [
            "First: what the letters mean.",
            A('AB = 10A + B appears', T('$\\overline{AB}=10A+B$', 48, gap=20)),
            A('ABC = 100A + 10B + C appears', T('$\\overline{ABC}=100A+10B+C$', 48, gap=40)),
            "A bar on top: the digits of ONE number. AB is not A times B.",
            A("'Same letter → same digit · leading digit ≠ 0' appears", T('Same letter $\\to$ same digit · leading digit $\\ne0$', 44, gap=40)),
            "The same letter is always the same digit. Different letters? Only if the question says so.",
            "And a leftmost digit is never zero.",
        ]),
        C(1, [
            "The technique — four steps, every time.",
            A('Step 1 appears', T('1 · Write it vertically', 44)),
            A('Step 2 appears', T('2 · Check the ones digit', 44)),
            A('Step 3 appears', T('3 · Check the leftmost digit and the size', 44)),
            A('Step 4 appears', T('4 · Plug in numbers — or the choices', 44)),
            "Write it vertically. Check the ones digit. Check the leftmost digit and the size. Then plug in.",
        ]),
        C(2, [
            "The ones column is special: nothing carries into it.",
            A("'Ones column: B + D ends in B → D = 0' appears", T('Ones column: $B+D$ ends in $B\\ \\to\\ D=0$', 44, gap=40)),
            A("'Other columns: X + Y ends in X → Y = 0 or 9' appears", T('Other columns: $X+Y$ ends in $X\\ \\to\\ Y=0$ or $9$', 44, gap=40)),
            "In any other column there may be a carry. Then Y can be nine: two X nine plus Y four — Y is nine.",
            A("'Carry: two numbers → 0 or 1' appears", T('Carry, two numbers: $0$ or $1$', 44, gap=20)),
            A("'Carry: three or four numbers → up to 2 or 3' appears", T('Carry, three or four numbers: up to $2$ or $3$', 44)),
            "Two numbers carry zero or one. Three or four numbers can carry more: seven plus seven plus nine — twenty-three, carry two.",
        ]),
        C(3, [
            "Now the leftmost digit.",
            A("'Two numbers, sum with more digits → leading digit 1' appears", T('Two numbers, sum with more digits $\\to$ leading digit $1$:  $87+68=155$', 40, gap=40)),
            "Add TWO numbers and get more digits? The leading digit is one.",
            A("'Three numbers: at most 3 · 999 = 2997' appears", T('Three three-digit numbers: at most $3\\cdot999=2997$', 42, gap=40)),
            "Only for two numbers. Three numbers can start with two.",
            A('23² = 529 and 28² = 784 appear', T('Estimate:  $23^2=529$,  $28^2=784$', 44)),
            "And estimate the size — it throws out choices fast.",
        ]),
        C(4, [
            "The special digits: zero, one, five and six.",
            A("'d · d ends in d: 0, 1, 5, 6' appears", T('$d\\cdot d$ ends in $d$:  $0,\\ 1,\\ 5,\\ 6$  ($15\\cdot15=225$, $16\\cdot16=256$)', 42, gap=40)),
            "Multiply one by itself — the ones digit stays. No other digit does that.",
            A("'5 × even ends in 0, 5 × odd ends in 5' appears", T('$5\\,\\times$ even ends in $0$;  $5\\,\\times$ odd ends in $5$', 44, gap=20)),
            A("'6 × even keeps its ones digit' appears", T('$6\\,\\times$ even keeps its ones digit:  $6\\cdot12=72$', 44)),
            "Five times even ends in zero, times odd ends in five. Six times an even number keeps its ones digit: six times twelve, seventy-two.",
        ]),
        C(5, [
            "Every letter question can be solved by plugging in.",
            A("'Asked for one letter? Plug in the choices, from the middle one' appears", T('One letter? Plug in the choices, from the middle one', 42, gap=40)),
            A("'Test numbers that are not alike' appears", T('"Always divisible by"? Test two numbers that are not alike', 42, gap=40)),
            "Two choices survive? Try a third number.",
            A("'Subtraction → addition · division → multiplication' appears", T('Subtraction $\\to$ addition · Division $\\to$ multiplication', 42)),
            "And flip a subtraction into an addition, a division into a multiplication. It's easier to see.",
        ]),
        C(6, [
            "The algebraic form gives facts that come back again and again.",
            A('AB − BA = 9(A − B) appears', T('$\\overline{AB}-\\overline{BA}=9(A-B)$', 44, gap=20)),
            A('AB + BA = 11(A + B) appears', T('$\\overline{AB}+\\overline{BA}=11(A+B)$', 44, gap=40)),
            A('ABC − CBA = 99(A − C) appears', T('$\\overline{ABC}-\\overline{CBA}=99(A-C)$:  $852-258=594$', 42, gap=40)),
            "A number minus its reversal: divisible by nine. With three digits, by ninety-nine — middle digit nine.",
            A('AAA = 111A = 3 · 37 · A appears', T('$\\overline{AAA}=111A=3\\cdot37\\cdot A$', 44, gap=20)),
            A('BBBB ÷ BB = 101 appears', T('$\\overline{BBBB}\\div\\overline{BB}=101$', 44)),
            "Triple digits: divisible by three and thirty-seven. And BBBB over BB is always one hundred one.",
        ]),
        C(7, [
            "Products and powers.",
            A("'Ones digit of a product: only the ones digits' appears", T('Ones digit of a product: $63\\cdot29\\to3\\cdot9=27\\to7$', 42, gap=40)),
            A("'Digits of a product: add the counts, or one fewer' appears", T('Digits of a product: add the counts, or one fewer', 42, gap=40)),
            "Two-digit times two-digit: four digits, or three.",
            A('The cycle of 2 appears', T('Ones digits of powers repeat:  $2,\\ 4,\\ 8,\\ 6,\\ 2,\\ 4,\\ \\ldots$', 42, gap=20)),
            A('The ones digit of 2⁴³ appears', T('$2^{43}$:  $43=4\\cdot10+3\\ \\to$ like $2^3$, ends in $8$', 42)),
            "The ones digits of powers repeat in a cycle. Find where you land in the cycle.",
        ]),
        C(8, [
            "Largest or smallest with a given digit sum.",
            A("'Digit sum 7: largest 700, smallest 106' appears", T('Digit sum $7$:  largest $700$ · smallest $106$', 48)),
            "Largest: big digits on the left. Smallest: one first, then zeros, the big digits on the right.",
        ]),
        C(9, [
            "Before you practice, always ask yourself:",
            A('Check 1', T('1. Must the letters be different digits?', 40)),
            A('Check 2', T('2. Which column am I in? Is there a carry?', 40)),
            A('Check 3', T('3. How many numbers are added? Does the size fit?', 40)),
            A('Check 4', T('4. One letter asked? Plug in the choices.', 40)),
            "The common traps: forgetting the carry, a leading zero, and the leading-digit-one rule with more than two numbers.",
            "And a matching last digit is not a full proof — check the size too. Go practice.",
        ]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    v = M.new_video('r26-t18-summary', TOPIC, 'Letter Puzzles: Summary', sb, slides, ADV, after=last)
    v['hybrid']['num'] = M.video(FACTS)['hybrid']['num'] or M.video(LESSON)['hybrid']['num']


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
    # ---- "Exercises with Letters" -> the Hebrew intro: the 4 steps + what the letters mean.
    #      Worked example -> Q1; carries -> Q10 (+ one line); leading digit -> Q1 (+ why, + the 4-numbers limit);
    #      special digits -> Q2 (+ the 5 and 6 facts); plug in -> Q3 (+ "choices from the middle" in Q8);
    #      minus -> plus -> Q5, Q7; algebraic form -> Q3, Q9 (+ ABC in Q3).
    _cr_cut(M, LESSON, ['The 4 steps in action', 'Carries', 'Leading digit', 'Special digits', 'Plug in numbers',
                        'Minus → plus', 'Algebraic form', 'Recap'])
    _cr_say(M, LESSON, 2, "Let's run it on an example", 'Each question that follows uses these steps — and teaches one more tool.')
    _cr_add(M, LESSON, 3, None, ['Three questions next. Try each one — then watch its solution.'])

    # Q1 (q-512): why the leading digit is one, and its limit
    _cr_add(M, 'solve-q-512', 2, 'More digits in the sum: the leading digit is one', [
        A("'Two numbers, more digits → leading digit 1' appears", T('Two numbers, more digits $\\to$ leading digit $1$:  $99+99=198$', size=36)),
        "Why? Even ninety-nine plus ninety-nine is only one ninety-eight. Careful — that's for TWO numbers. Four three-digit numbers can reach three thousand and more."])
    # Q2 (q-513): no lesson slide to "remember"; the two extra special-digit facts
    _cr_say(M, 'solve-q-513', 1, 'Remember the special digits?', 'The special digits — zero, one, five and six.')
    _cr_add(M, 'solve-q-513', 2, "that's a special digit", [
        A("'5 × even → 0, 5 × odd → 5, 6 × even keeps it' appears", T('$5\\times$ even $\\to0$ · $5\\times$ odd $\\to5$ · $6\\times$ even keeps its digit', size=34)),
        "Two more facts about them: five times an even number ends in zero, times an odd number in five. Six times an even digit keeps that digit — six times four, twenty-four."])
    # Q3 (q-514): three-digit algebraic form
    _cr_add(M, 'solve-q-514', 3, 'The algebraic form proves it', [
        A("'AB = 10A + B, ABC = 100A + 10B + C' appears", T('$\\overline{AB}=10A+B \\qquad \\overline{ABC}=100A+10B+C$', size=36)),
        "The algebraic form: AB is ten A plus B. ABC is a hundred A, plus ten B, plus C."])
    # Q8 (q-519): plugging in the choices, from the middle
    _cr_add(M, 'solve-q-519', 2, 'Classic trial and error', [
        "A tip for any question that asks for one letter: plug in the choices. When they are in order, start from the middle one — too big or too small tells you which way to go."])
    # Q10 (q-r26-t18-01): carries
    _cr_add(M, 'solve-q-r26-t18-01', 2, 'B plus one must be ten', [
        A("'Middle column: ends in the same digit → 0 or 9' appears", T('Middle column: "ends in the same digit" $\\to0$ or $9$', size=36)),
        "So in a middle column, \"ends in the same digit\" means zero or nine — check the carry. With two numbers a carry is at most one; three or four numbers can carry two or three."])

    # ---- "Number Facts for Letter Puzzles": reversals -> Q11 (+ why); products -> Q12. Kept: repdigits,
    #      powers' ones digit, largest/smallest (no question video teaches them).
    _cr_cut(M, FACTS, ['Reversals', 'Products', 'Recap'])
    _cr_say(M, FACTS, 1, 'A few patterns come back', 'A few patterns come back again and again on the exam. Three of them first — the questions teach the rest.')
    _cr_say(M, FACTS, 3, 'Fourth: the ones digit of a power.', 'Second: the ones digit of a power.')
    _cr_add(M, FACTS, 4, None, ['The next questions use these facts — and teach a few more. Try each one first — then watch.'])
    _cr_add(M, 'solve-q-r26-t18-02', 2, 'ABC minus CBA is ninety-nine times', [
        A("'ABC − CBA = 99(A − C)' appears", T('$(100A+10B+C)-(100C+10B+A)=99(A-C)$', size=36)),
        "Why? Write both in algebraic form. The middle digit cancels: ninety-nine A minus ninety-nine C."])


# =====================================================================================
# 2026-10-06 new exam methods: digit WORD equations ("the number is k times the sum of its digits") join the routine
# =====================================================================================
WORDS_T = T('Words, no columns? Write $10A+B$ and collect:  $10A+B=4(A+B)\\to6A=3B\\to B=2A$:  $12,\\ 24,\\ 36,\\ 48$', 36)


def add_methods(M):
    words = [
        A("'Words, no columns → write 10A + B and collect' appears", WORDS_T),
        "One more case: the puzzle comes in words, with no columns. \"The number is four times the sum of its digits.\"",
        "Then write the number as ten A plus B, and collect the A's on one side and the B's on the other.",
        "Ten A plus B equals four A plus four B. So six A equals three B — B is twice A.",
        "That ratio is the whole answer: twelve, twenty-four, thirty-six, forty-eight. Check one: twelve is four times three.",
    ]
    # lesson slide 2: after step 4, before the bracket
    _cr_add(M, LESSON, 2, 'Four: plug in numbers', words)
    # summary slide "The 4 steps"
    v = M.video('r26-t18-summary'); n = next(k for k, b in enumerate(v['beats'], 1) if b['title'] == 'The 4 steps')
    _cr_add(M, 'r26-t18-summary', n, None, [
        A("'Words, no columns → write 10A + B and collect' appears", WORDS_T),
        "Words, no columns? Write ten A plus B, and collect into a digit ratio."])
    # card
    for t in M.card('mem-letters')['tables']:
        if t['title'] == 'The four steps':
            t['rows'].append(['Words, no columns', 'Write $10A+B$ and collect into a digit ratio: '
                              '$10A+B=4(A+B)\\to6A=3B\\to B=2A$: $12,\\ 24,\\ 36,\\ 48$'])
    # Q9 (q-520) already uses it: name the move
    _cr_add(M, 'solve-q-520', 2, 'Cancel U from both sides', [
        "This is the move for digit puzzles in words: write the number as ten T plus U, then collect the letters on each side."],
        where='before')


_apply_before_add_methods = apply


def apply(M):
    _apply_before_add_methods(M)
    add_methods(M)   # 2026-10-06: runs last


# =====================================================================================
# 2026-10-06 practice: the new exam methods as an extra method in PRACTICE explanations
# (append only; the existing worked solution stays as it is). Runs last.
# =====================================================================================
PRACTICE_METHODS = {
    'alg-extra-unit-t18-3-6': [
        'Method 2 · Words, no columns: write the number as $10A+B$ and collect. $10A+B=4(A+B)$, so $6A=3B$ and $B=2A$. The tens digit is $2$, so the ones digit is $4$.',
    ],
    'q-530': [
        'Method 2 · Words, no columns: $X=10A+5$, and the reversed number is $50+A$. So $50+A=3(10A+5+2)=30A+21$, which gives $29A=29$ and $A=1$.',
        '$X=15$, and the sum of its digits is $6$.',
    ],
}


def practice_methods(M):
    for qid, lines in PRACTICE_METHODS.items():
        q = M.q(qid)
        M.set_q(qid, expl=list(q['explanation']) + lines)


_apply_before_practice_methods = apply


def apply(M):
    _apply_before_practice_methods(M)
    practice_methods(M)   # 2026-10-06 practice: runs last


# ======================================================================================================
# 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived item (guided q-512 .. q-520,
# practice q-521 .. q-540, the Hebrew lesson's own examples) gets new numbers / letters - same concept, same trap,
# same level, at least the same methods. Plus the approved practice clean-up.
# Nothing in topic 18 is recorded (no take in ~/Documents/Course.recordings). Runs last.
# ======================================================================================================
RN_RECORDED = set()


def _rn_lines(M, vid, n, pairs):
    """Exact substring replacements in one slide's spoken lines, draw cues and item labels/texts."""
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
    if qid not in RN_RECORDED: M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. The pre-loaded question stays."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script)


VERT = dict(x=1150, y=330)
LEAD_T = T('Two numbers, more digits $\\to$ leading digit $1$:  $99+99=198$', size=36)
SPECIAL_T = T('$5\\times$ even $\\to0$ · $5\\times$ odd $\\to5$ · $6\\times$ even keeps its digit', size=34)
FORM_T = T('$\\overline{AB}=10A+B \\qquad \\overline{ABC}=100A+10B+C$', size=36)


def rn_lessons(M):
    # "Exercises with Letters": the Hebrew lesson's sample numbers
    _rn_lines(M, LESSON, 1, [("instead of 32 plus 57", "instead of 46 plus 38")])
    _rn_lines(M, LESSON, 3, [("Like twenty-three.", "Like forty-seven."),
                             ("a different symbol for 2, a different symbol for 3. Still just 23.",
                              "a different symbol for 4, a different symbol for 7. Still just 47.")])
    c = M.card('mem-letters')
    for t in c['tables']:
        for r in t['rows']:
            if r[1] == '$27=10\\cdot2+7$': r[1] = '$47=10\\cdot4+7$'
    # Number-facts card: examples that were the Hebrew lesson's / questions' numbers
    c = M.card('mem-r26-t18-facts'); rows = c['tables'][0]['rows']; hit = 0
    for r in rows:
        if r[1] == '$52-25=27$, $\\ 52+25=77$': r[1] = '$73-37=36$, $\\ 73+37=110$'; hit += 1
        if r[1] == '$521-125=396=99\\cdot4$': r[1] = '$412-214=198=99\\cdot2$'; hit += 1
    assert hit == 2, hit
    c['tips'] = [x.replace('$24^2=576$, $27^2=729$', '$23^2=529$, $28^2=784$') for x in c['tips']]


def rn_guided(M):
    # ---------- Q1 q-512: AB + CB = DDB, A+C+D   ==>   BA + DA = CCA, B+C+D (letters moved, choices reordered)
    _rn_q(M, 'q-512', 'A, B, C and D represent digits. Given: $\\overline{BA}+\\overline{DA}=\\overline{CCA}$\n$B+C+D=?$',
          ['$10$', '$11$', '$13$', '$12$'], 4, [
        'Write it vertically. Ones column: $A+A$ ends in $A$. Nothing carries into the ones column, so $A=0$.',
        'Two two-digit numbers give a three-digit number, so the leading digit is 1: $C=1$.',
        'Tens column: $B+D$ (nothing carries in, because $0+0=0$) gives the tens digit 1 and carries 1 into the hundreds. So $B+D=11$.',
        '$B+C+D=11+1=12$. Check: $B=3$, $D=8$: $30+80=110$ ✓.'])
    _rn_video(M, 'q-512', [[
        "Step one: write it vertically.",
        A('The vertical layout appears: BA + DA = CCA', T(ARR('BA', '+\\ DA', 'CCA'), 50, **VERT)),
        "Step two: the ones. A plus A ends in A.",
        D('Circle the ones column; write "A = 0"'),
        "Add A to A and land back on A? This is the ones column — nothing carries in. Only zero does that. A is zero.",
        "Step three: the leftmost digit. Two two-digit numbers — and the result has three digits.",
        D('Circle the C in the hundreds; write "C = 1"'),
        "More digits in the sum: the leading digit is one. C is one.",
        A("'Two numbers, more digits → leading digit 1' appears", LEAD_T),
        "Why? Even ninety-nine plus ninety-nine is only one ninety-eight. Careful — that's for TWO numbers. Four three-digit numbers can reach three thousand and more.",
        "So the tens: B plus D gives eleven — the one stays in the tens, the other one carries into the hundreds.",
        D('Write "B + D = 11"'),
        "B plus D is eleven. Three and eight, four and seven — we don't know which, and we don't need to.",
        D('Write "B + C + D = 11 + 1 = 12" and circle choice 4'),
        "Eleven plus one: twelve. Choice four.",
    ], [
        "Step four — plug in to check. B is three, D is eight, A is zero.",
        D('Write "30 + 80 = 110"'),
        "Thirty plus eighty: a hundred ten. C, C, A — one, one, zero. It fits.",
        "Three plus one plus eight: twelve.",
        D('Circle choice 4'),
        "Twelve. Choice four.",
    ]])

    # ---------- Q2 q-513: BA x A = CA, A = 6 (16 x 6 = 96)   ==>   CB x B = AB, B = 5 (15 x 5 = 75)
    _rn_q(M, 'q-513', 'A, B and C represent digits. Given: $\\overline{CB}\\times B=\\overline{AB}$\nWhich of the following could be B?',
          ['$4$', '$0$', '$5$', '$7$'], 3, [
        'Ones column: $B\\times B$ ends in $B$. Only the special digits do this: $0, 1, 5, 6$ ($0\\cdot0=0$, $1\\cdot1=1$, $5\\cdot5=25$, $6\\cdot6=36$).',
        'Choices (1) and (4) fail: $4\\cdot4=16$ and $7\\cdot7=49$.',
        'Choice (2) fails: $B=0$ makes the product $0$, not a two-digit number.',
        'Choice (3): $B=5$ and $C=1$ give $15\\times5=75$ ✓.'])
    _rn_video(M, 'q-513', [[
        "Step one: vertically.",
        A('The vertical layout appears: CB × B = AB', T(ARR('CB', '\\times\\ \\ \\ B', 'AB'), 50, **VERT)),
        "Step two: the ones. B times B ends in B.",
        D('Circle the B in the ones column of every line'),
        "A digit times itself that keeps its ones digit — that's a special digit. Zero, one, five or six.",
        A("'5 × even → 0, 5 × odd → 5, 6 × even keeps it' appears", SPECIAL_T),
        "Two more facts about them: five times an even number ends in zero, times an odd number in five. Six times an even digit keeps that digit — six times four, twenty-four.",
        D('Write "B ∈ {0, 1, 5, 6}"'),
        D('Cross out choices 1 and 4'),
        "Four and seven aren't special. Four times four is sixteen. Seven times seven is forty-nine. Out.",
        "From the choices, that leaves five — or zero.",
        D('Cross out choice 2'),
        "Zero? Zero times anything is zero — not a two-digit number. Out.",
        D('Circle choice 3'),
        "So B is five. Choice three.",
    ], [
        "Quick check by plugging in. B is five — take C as one.",
        D('Write "15 · 5 = 75"'),
        "Fifteen times five: seventy-five. It ends in five, and A is seven. It works.",
        D('Circle choice 3'),
        "Choice three.",
    ]])

    # ---------- Q3 q-514: AB + BA divisible by 9/6/11/4, tests 51, 52   ==>   choices 3/11/4/10, tests 71, 72
    _rn_q(M, 'q-514', 'A and B represent nonzero digits. Which of the following necessarily divides $\\overline{AB}+\\overline{BA}$?',
          ['$3$', '$11$', '$4$', '$10$'], 2, [
        'Plug in two different numbers. $71+17=88$: it is not divisible by 3 or by 10, so choices (1) and (4) are out.',
        '$72+27=99$: it is not divisible by 4, so choice (3) is out. Only 11 is left.',
        'Why it always works: $\\overline{AB}+\\overline{BA}=(10A+B)+(10B+A)=11A+11B=11(A+B)$.'])
    _rn_video(M, 'q-514', [[
        "There's no result to work with. So: plug in numbers.",
        D('Write "71 + 17 = 88"'),
        "AB is seventy-one. Seventy-one plus seventeen: eighty-eight.",
        D('Cross out choices 1 and 4'),
        "Eighty-eight isn't divisible by three, or by ten. Those two are out. Four and eleven survive.",
        D('Write "72 + 27 = 99"'),
        "Next number, seventy-two. Seventy-two plus twenty-seven: ninety-nine.",
        D('Cross out choice 3'),
        "Ninety-nine isn't divisible by four.",
        D('Circle choice 2'),
        "Only eleven survives both. Choice two.",
        "And the pattern: AB plus BA — always eleven. AB minus BA — always nine.",
    ], [
        "The algebraic form proves it.",
        A("'AB = 10A + B, ABC = 100A + 10B + C' appears", FORM_T),
        "The algebraic form: AB is ten A plus B. ABC is a hundred A, plus ten B, plus C.",
        D('Write "(10A + B) + (10B + A) = 11A + 11B = 11(A + B)"'),
        "Ten A plus B, plus ten B plus A: eleven A plus eleven B. Eleven times A plus B.",
        D('Circle choice 2'),
        "Eleven times anything is divisible by eleven. Choice two.",
    ]])

    # ---------- Q4 q-515: ABC + AB = CCC, B = 0   ==>   BCA + BC = AAA, C = 0 (letters moved, choices reordered)
    _rn_q(M, 'q-515', 'A, B and C represent digits. Given: $\\overline{BCA}+\\overline{BC}=\\overline{AAA}$\n$C=?$',
          ['$0$', '$9$', '$1$', '$5$'], 1, [
        'Ones column: $A+C$ ends in $A$. Nothing carries into the ones column, so $C=0$.',
        'Check the tens: $C+B=0+B$, so $B=A$. For example: $303+30=333$ ✓.'])
    _rn_video(M, 'q-515', [[
        "Step one: vertical.",
        A('The vertical layout appears: BCA + BC = AAA', T(ARR('BCA', '+\\ \\ \\ BC', 'AAA'), 50, **VERT)),
        "It's already an addition — nothing to flip.",
        "The leftmost-digit rule? A three-digit number plus a two-digit number, still three digits. No new digit, so no free one this time.",
        "So go to the ones. A plus C ends in A.",
        D('Circle the ones column; write "C = 0"'),
        "A plus something, back to A. It's the ones column, so nothing carries in: that something is zero. C is zero.",
        D('Circle choice 1'),
        "C is zero — choice one.",
        "Quick check: nothing carries, so the tens are C plus B — just B. So B equals A.",
        D('Write "303 + 30 = 333 ✓"'),
        "Three-oh-three plus thirty: three-three-three. It fits.",
    ]])

    # ---------- Q5 q-516: AAA - 37 = BC -> 74, B+C = AA   ==>   AAA - 46 = BC -> 65, B+C = AA
    _rn_q(M, 'q-516', 'A, B and C represent digits. Given: $\\overline{AAA}-46=\\overline{BC}$\n$B+C=?$',
          ['$\\overline{BC}$', '$\\overline{AC}$', '$\\overline{AA}$', '$\\overline{AB}$'], 3, [
        'Flip the subtraction into an addition: $\\overline{BC}+46=\\overline{AAA}$.',
        'Two two-digit numbers give a three-digit number, so the leading digit is 1: $A=1$ and $\\overline{AAA}=111$.',
        '$111-46=65$, so $B=6$, $C=5$ and $B+C=11$.',
        '$A=1$, so $\\overline{AA}=11$. The other choices: $\\overline{BC}=65$, $\\overline{AC}=15$, $\\overline{AB}=16$.'])
    _rn_video(M, 'q-516', [[
        "Step one: vertical.",
        A('The vertical layout appears: AAA − 46 = BC', T(ARR('AAA', '-\\ \\ \\ 46', 'BC'), 50, **VERT)),
        "Subtraction is harder to read — flip it into addition.",
        A('The flipped layout appears: BC + 46 = AAA', T(ARR('BC', '+\\ 46', 'AAA'), 50, x=1360, y=330)),
        D('Draw an arrow from the first layout to the second'),
        "BC plus forty-six equals AAA.",
        "Two two-digit numbers make a three-digit number — so the leading digit is one. A is one.",
        D('Write "A = 1 → AAA = 111"'),
        "And AAA is one-one-one.",
        "Some students go digit by digit here — C plus six ends in one, so C is five, carry… Correct, but slow.",
        "Just calculate: a hundred eleven minus forty-six — sixty-five.",
        D('Write "111 − 46 = 65 → B = 6, C = 5"'),
        "B is six, C is five. B plus C: eleven.",
        "The choices are letters too. AA — A is one, so AA is eleven.",
        D('Circle choice 3'),
        "Choice three.",
    ]])

    # ---------- Q6 q-517: AB^2 = 6CB, B - A could be 4 (26^2)   ==>   AB^2 = 2CB, B - A could be 5 (16^2)
    _rn_q(M, 'q-517', 'A, B and C represent digits. Given: $\\overline{AB}\\times\\overline{AB}=\\overline{2CB}$\nWhich of the following could be $B-A$?',
          ['$6$', '$5$', '$7$', '$8$'], 2, [
        'Size first: $14^2=196$ is too small, and $18^2=324$ is too big. So $\\overline{AB}$ is 15, 16 or 17, and $A=1$.',
        'Ones column: $B\\times B$ ends in $B$, so B is a special digit. Here $B=5$ or $B=6$ ($17^2=289$ ends in 9, not in 7).',
        '$15^2=225$ ✓ gives $B-A=5-1=4$, which is not a choice. $16^2=256$ ✓ gives $B-A=6-1=5$.'])
    _rn_video(M, 'q-517', [[
        "Method one: the full math. First — estimate the size.",
        "AB times AB is AB squared, and it's two hundred and something.",
        D('Write "14² = 196, 15² = 225, 16² = 256, 17² = 289, 18² = 324"'),
        "Fourteen squared is one ninety-six — too small. Eighteen squared, three twenty-four — too big.",
        "So AB is fifteen, sixteen or seventeen. A is one.",
        "Now the ones: B times B ends in B — a special digit. Zero, one, five or six.",
        "Seven isn't special — seventeen squared ends in nine, not seven. So B is five or six.",
        D('Next to 225 write "B − A = 4"'),
        "B is five: fifteen squared, two twenty-five. B minus A is four — not offered. They asked what COULD be.",
        D('Next to 256 write "B − A = 5" and circle choice 2'),
        "B is six: sixteen squared, two fifty-six. Six minus one: five. Choice two.",
    ], [
        "Method two — the insight. B times B ends in B, so B is zero, one, five or six.",
        "The choices are five, six, seven, eight — fairly big. B minus something can't reach them if B is zero or one.",
        D('Write "B ≠ 0, 1"'),
        "B is five? Five minus A is at least five only if A is zero — and a leading digit is never zero. Out.",
        D('Write "B = 6"'),
        "So B is six. Six minus A: five needs A equal one; six needs A equal zero — not allowed.",
        D('Write "16² = 256 ✓"'),
        "Check: sixteen squared, two fifty-six. Two hundred and something, ending in six. It fits.",
        D('Write "6 − 1 = 5" and circle choice 2'),
        "Six minus one: five. Choice two.",
    ]])

    # ---------- Q7 q-518: CBA / AA = 13 -> 55 x 13 = 715   ==>   CBA / AA = 17 -> 55 x 17 = 935
    _rn_q(M, 'q-518', 'A, B and C represent digits. Given: $\\frac{\\overline{CBA}}{\\overline{AA}}=17$\n$A+B+C=?$',
          ['$17$', '$19$', '$15$', '$16$'], 1, [
        'Flip the division into a multiplication: $\\overline{AA}\\times17=\\overline{CBA}$.',
        'Ones column: $7\\times A$ ends in $A$. So $6A$ ends in 0: $A=0$ or $A=5$. $A=0$ is not possible, because $\\overline{AA}$ is a two-digit number. So $A=5$.',
        '$55\\times17=550+385=935$, so $C=9$, $B=3$ and $A=5$.',
        '$A+B+C=5+3+9=17$.'])
    _rn_video(M, 'q-518', [[
        "Division is awkward to work with. Just like subtraction flips to addition — division flips to multiplication.",
        A('The vertical layout appears: AA × 17 = CBA', T(ARR('AA', '\\times\\ 17', 'CBA'), 50, **VERT)),
        "AA times seventeen equals CBA.",
        "Step two: the ones digit. Seven times A ends in A.",
        "Seven A ending in A means six A ends in zero — so A is zero or five. Seven times five: thirty-five. It ends in five.",
        D('Write "7 · 5 = 35 → A = 5"'),
        "Zero would also work — but AA can't start with zero. So A is five.",
        "Now just multiply: fifty-five times seventeen.",
        D('Write "55 · 17 = 550 + 385 = 935"'),
        "Split it. Ten times fifty-five is five-fifty. Seven times fifty-five, three eighty-five. Nine thirty-five.",
        "C is nine, B is three, A is five — and the last digit really is five.",
        D('Write "5 + 3 + 9 = 17" and circle choice 1'),
        "Five plus three plus nine: seventeen. Choice one.",
    ]])

    # ---------- Q8 q-519: prime digits, AC + CD = BA (52 + 23 = 75), C = 2   ==>   AB + BC = CD (32 + 25 = 57), C = 5
    _rn_q(M, 'q-519', 'A, B, C and D represent different digits, and each of them is a prime number. Given: $\\overline{AB}+\\overline{BC}=\\overline{CD}$\n$C=?$',
          ['$7$', '$3$', '$5$', '$2$'], 3, [
        'The prime digits are 2, 3, 5 and 7. There are four different letters, so each prime digit is used once.',
        'Plug in the choices. $C=5$: in the tens column, $A+B$ (plus any carry) gives 5. Two different prime digits add up to at least $2+3=5$, so nothing carries, and A and B are 2 and 3. Ones column: $B+5=D$. $B=2$ gives $D=7$ ✓ ($B=3$ would give 8). So $A=3$. Check: $32+25=57$ ✓.',
        'The other choices fail. $C=2$ or $C=3$: the tens column needs $A+B$ to be 2 or 3, but two different prime digits add up to at least 5.',
        '$C=7$: the ones column is $B+7$. $B=2$ gives 9 and $B=3$ gives 10, but 9 and 0 are not prime. $B=5$ gives 12: $D=2$, 1 carries, and the tens $A+5+1=7$ make $A=1$, which is not prime.'])
    _rn_video(M, 'q-519', [[
        "First, take inventory: the prime digits are two, three, five and seven.",
        D('Write "2, 3, 5, 7"'),
        "Four letters, four different prime digits — every one gets used.",
        "Classic trial and error: plug in the answers. Choice three — C is five.",
        "A tip for any question that asks for one letter: plug in the choices. When they are in order, start from the middle one — too big or too small tells you which way to go.",
        A('The vertical layout appears: AB + BC = CD', T(ARR('AB', '+\\ BC', 'CD'), 50, **VERT)),
        "Tens: A plus B — plus any carry — gives five. The two smallest primes, two and three, already make five. So nothing carries, and A and B are two and three.",
        D('Write "C = 5 → A + B = 5 → 2 and 3"'),
        "Ones: B plus five gives D. B two: D is seven — a prime, and the last one left. B three would give eight.",
        D('Write "B = 2, D = 7, A = 3"'),
        D('Write "32 + 25 = 57 ✓"'),
        "Thirty-two plus twenty-five: fifty-seven — C, then D. It works!",
        D('Circle choice 3'),
        "On the exam: mark it and move on. Choice three.",
    ], [
        "In class, let's rule out the rest.",
        "C is two or three: the tens need A plus B to give two or three. But two different primes add up to at least five. Out.",
        D('Next to choices 2 and 4 write "A + B ≥ 5 ✗"'),
        "C is seven: the ones are B plus seven. B two gives nine, B three gives ten — nine and zero aren't prime.",
        "B five gives twelve: D is two, carry one. Then the tens: A plus five plus one is seven — A would be one. Not prime.",
        D('Next to choice 1 write "9 ✗  10 ✗  12 → A = 1 ✗"'),
        D('Cross out choices 1, 2 and 4'),
        "Only C equal five works. Choice three.",
    ]])

    # ---------- Q9 q-520: x = U^3 + (T + U) -> 33   ==>   x = U^3 + 4(T + U) -> 63
    _rn_q(M, 'q-520', 'x is a two-digit number. x is equal to the cube of its ones digit plus 4 times the sum of its digits. What is the tens digit of x?',
          ['$4$', '$7$', '$5$', '$6$'], 4, [
        'Plug in the choices for the tens digit T. Call the ones digit U, so $x=10T+U$.',
        '$T=6$: $60+U=U^3+4(6+U)$, so $U^3+3U=36$ and $U=3$. Check: $x=63$, and $3^3+4\\cdot(6+3)=27+36=63$ ✓.',
        'The other choices fail: $T=4$ gives $U^3+3U=24$, $T=7$ gives $42$, $T=5$ gives $30$. But $U^3+3U$ is $0, 4, 14, 36, 76, \\ldots$ — never one of them.',
        'Algebraic form: $10T+U=U^3+4T+4U$, so $6T=U^3+3U$ — the same test.'])
    _rn_video(M, 'q-520', [[
        "Method one: the math. x is a two-digit number — tens digit T, ones digit U.",
        D('Write "x = 10T + U"'),
        "The condition: x equals its ones digit cubed, plus four times the sum of its digits.",
        D('Write "10T + U = U³ + 4(T + U)"'),
        "This is the move for digit puzzles in words: write the number as ten T plus U, then collect the letters on each side.",
        "Open the bracket: four T plus four U. Take four T and one U away from both sides.",
        D('Write "6T = U³ + 3U"'),
        "Six T equals U cubed plus three U. Six T is at most fifty-four — so U is small.",
        "U one gives four. U two gives fourteen. Not multiples of six. U three: twenty-seven plus nine — thirty-six. U four: seventy-six — too big.",
        D('Write "U = 3 → 6T = 36 → T = 6" and circle choice 4'),
        "Six T is thirty-six, so T is six. The tens digit is six — choice four.",
    ], [
        "Method two: plug in the choices. They offer the tens digit — try each one as T.",
        D('Write "T = 6: 60 + U = U³ + 4(6 + U)"'),
        "Try six. The number is sixty plus U. The condition: U cubed, plus four times six plus U.",
        D('Write "→ U³ + 3U = 36 → U = 3"'),
        "Take twenty-four and four U away from both sides: U cubed plus three U is thirty-six. U is three — a real digit. It works.",
        D('Write "63: 27 + 4 · 9 = 63 ✓" and circle choice 4'),
        "Check: sixty-three. Three cubed is twenty-seven, plus four times nine, thirty-six. Sixty-three. Choice four.",
        D('Next to choices 1, 2 and 3 write "U³ + 3U = 24, 42, 30 ✗"'),
        "The others work the same way: four gives twenty-four, seven gives forty-two, five gives thirty. U cubed plus three U is four, fourteen, thirty-six — never one of those.",
    ]])


def rn_practice_questions(M):
    # q-521: two-digit + four-digit -> 4 or 5 digits   ==>   three-digit + five-digit -> 5 or 6 digits
    _rn_q(M, 'q-521', 'A is a three-digit number and B is a five-digit number. Which of the following is true about $A+B$?',
          ['It can only be a five-digit number.', 'It can be a five-digit or a six-digit number.',
           'It can only be a six-digit number.', 'It can be a four-digit or a five-digit number.'], 2, [
        'Smallest sum: $100+10{,}000=10{,}100$ (five digits). Largest sum: $999+99{,}999=100{,}998$ (six digits).',
        'So $A+B$ can be a five-digit or a six-digit number.'])
    # q-522: AB x 2 = 1B0 -> 75   ==>   AB x 6 = 4B0 -> 75
    _rn_q(M, 'q-522', 'A and B represent different nonzero digits. Given: $\\overline{AB}\\times6=\\overline{4B0}$\n$A-B=?$',
          ['$3$', '$1$', '$2$', '$5$'], 3, [
        'Ones column: $6\\times B$ ends in 0. B is not 0, so $B=5$ ($6\\cdot5=30$).',
        'Then $\\overline{4B0}=450$, and $\\overline{AB}=450\\div6=75$. So $A=7$.',
        '$A-B=7-5=2$. Check: $75\\times6=450$ ✓.'])
    # q-523: A<B<C consecutive, A+B+C = 1B   ==>   X<Y<Z, X+Y+Z = 1Y (letters, choice order)
    _rn_q(M, 'q-523', 'X, Y and Z represent consecutive digits, and $X<Y<Z$. Given: $X+Y+Z=\\overline{1Y}$\nWhat is $X+Y+Z$?',
          ['$12$', '$21$', '$15$', '$18$'], 3, [
        'Three consecutive digits: the sum is 3 times the middle one, $3Y$.',
        '$\\overline{1Y}=10+Y$, so $3Y=10+Y$. Therefore $2Y=10$ and $Y=5$.',
        'The digits are 4, 5 and 6, and the sum is $15=\\overline{1Y}$ ✓.',
        'Or plug in the choices: the sum ends in Y and equals $3Y$. Only $15=3\\cdot5$ works ($12\\ne3\\cdot2$, $21\\ne3\\cdot1$, $18\\ne3\\cdot8$).'])
    # q-524: AB - BA = 27 -> 3   ==>   AB - BA = 45 -> 5
    _rn_q(M, 'q-524', 'A and B represent nonzero digits. Given: $\\overline{AB}-\\overline{BA}=45$\n$A-B=?$',
          ['$4$', '$5$', '$6$', '$9$'], 2, [
        '$\\overline{AB}-\\overline{BA}=9(A-B)$.',
        '$9(A-B)=45$, so $A-B=5$. Check: $72-27=45$ ✓.'])
    # q-525: AB x B = B4 -> 12 x 2   ==>   AB x B = B9 -> 13 x 3
    _rn_q(M, 'q-525', 'A and B represent nonzero digits. Given: $\\overline{AB}\\times B=\\overline{B9}$\n$A+B=?$',
          ['$8$', '$4$', '$10$', '$5$'], 2, [
        'Ones column: $B\\times B$ ends in 9. $3\\cdot3=9$ and $7\\cdot7=49$, so $B=3$ or $B=7$.',
        '$B=7$: $\\overline{A7}\\times7$ is at least $17\\times7=119$ — too big for a two-digit result. So $B=3$.',
        '$\\overline{A3}\\times3=39$, so $\\overline{A3}=13$ and $A=1$. $A+B=1+3=4$.'])
    # q-526: ABC + CCC = D00 -> 345 + 555   ==>   ABC + AAA = D00 -> 456 + 444
    _rn_q(M, 'q-526', 'A, B and C represent consecutive digits, and $A<B<C$. D represents a digit. Given: $\\overline{ABC}+\\overline{AAA}=\\overline{D00}$\n$A=?$',
          ['$3$', '$5$', '$4$', '$6$'], 3, [
        'Ones column: $C+A$ ends in 0. $C=A+2$, so $2A+2$ ends in 0: $A=4$ or $A=9$. $A=9$ is not possible, because $C=A+2$ must be a digit. So $A=4$, and 1 carries.',
        'Then $B=5$ and $C=6$. Tens column: $5+4+1=10$, so it ends in 0 ✓, and 1 carries again. Hundreds column: $4+4+1=9$, so $D=9$.',
        'Check: $456+444=900$ ✓.'])
    # q-527: four three-digit numbers -> thousands digit 3   ==>   five three-digit numbers -> 4
    _rn_q(M, 'q-527', 'X is a four-digit number. X is the sum of five three-digit numbers. Which of the following could be the thousands digit of X?',
          ['$6$', '$5$', '$4$', '$7$'], 3, [
        'Five three-digit numbers add up to at most $5\\cdot999=4995$.',
        'So the thousands digit of X is 1, 2, 3 or 4. Only 4 is a choice. Example: $999+999+999+999+999=4995$.',
        'The "leading digit 1" rule is only for the sum of two numbers.'])
    # q-528: k = AB + CD + 31   ==>   k = AB + CD + 53
    _rn_q(M, 'q-528', 'A, B, C and D represent consecutive digits, and $A<B<C<D$. Given: $k=\\overline{AB}+\\overline{CD}+53$\nWhich of the following necessarily divides k?',
          ['$9$', '$3$', '$11$', '$7$'], 3, [
        'Plug in $A=1$: $k=12+34+53=99$. 99 is not divisible by 7, so choice (4) is out.',
        'Plug in $A=2$: $k=23+45+53=121=11\\cdot11$. It is not divisible by 9 or by 3. Only 11 is left.',
        'Algebraic form (always true): $\\overline{AB}=10A+(A+1)=11A+1$ and $\\overline{CD}=10(A+2)+(A+3)=11A+23$. So $k=22A+77=11(2A+7)$.'])
    # q-529: digit sum 8 -> 800 - 107   ==>   digit sum 9 -> 900 - 108
    _rn_q(M, 'q-529', 'n is the largest three-digit number whose digit sum is 9. m is the smallest three-digit number whose digit sum is 9. $n-m=?$',
          ['$720$', '$783$', '$792$', '$702$'], 3, [
        'Largest: put as much as possible in the leftmost digit: $n=900$.',
        'Smallest: the hundreds digit is at least 1. Then the smallest tens digit, 0, and the rest in the ones: $m=108$.',
        '$n-m=900-108=792$.'])
    # q-530: ones digit 5, reversal = 3(X + 2) -> 15   ==>   ones digit 8, reversal = 3(X + 9) -> 18 (keeps today's Method 2 line)
    _rn_q(M, 'q-530', 'X is a two-digit number whose ones digit is 8. When we reverse the order of its digits, we get $3(X+9)$. What is the sum of the digits of X?',
          ['$11$', '$9$', '$13$', '$15$'], 2, [
        'Plug in the choices. The digit sum minus 8 is the tens digit: choice (1) gives $X=38$, (2) gives $X=18$, (3) gives $X=58$, (4) gives $X=78$.',
        '$X=18$: the reversed number is 81, and $3(18+9)=81$ ✓.',
        'The others fail. For example, $X=38$: the reversed number is 83, but $3(38+9)=141$.',
        'Method 2 · Words, no columns: $X=10A+8$, and the reversed number is $80+A$. So $80+A=3(10A+8+9)=30A+51$, which gives $29A=29$ and $A=1$.',
        '$X=18$, and the sum of its digits is $9$.'])
    # q-531: (AC + CB + BA) / (A + B + C)   ==>   (BA + CB + AC) / (A + B + C) (letters, choice order)
    _rn_q(M, 'q-531', 'A, B and C represent nonzero digits. $\\frac{\\overline{BA}+\\overline{CB}+\\overline{AC}}{A+B+C}=?$',
          ['$22$', '$9$', '$11$', 'It cannot be determined from the information given.'], 3, [
        'Plug in $A=2$, $B=3$, $C=4$: $\\frac{32+43+24}{9}=\\frac{99}{9}=11$. Another try, $A=B=C=2$: $\\frac{66}{6}=11$.',
        'Algebraic form: each letter appears once in the tens and once in the ones. So the sum is $11A+11B+11C=11(A+B+C)$, and the quotient is always 11.'])
    # q-532: hundreds digit 4 more than ones -> 396   ==>   7 more -> 693
    _rn_q(M, 'q-532', 'Two three-digit numbers are made of the same three digits, in a different order. Their tens digits are equal. In one of the numbers, the hundreds digit is 7 more than the ones digit. What is the difference between the two numbers?',
          ['$707$', '$693$', '$594$', '$711$'], 2, [
        'Same digits and the same tens digit, so the hundreds digit and the ones digit swap: the numbers are $\\overline{ABC}$ and $\\overline{CBA}$.',
        '$\\overline{ABC}-\\overline{CBA}=99(A-C)=99\\cdot7=693$.',
        'Example: $841-148=693$ ✓.'])
    # q-533: BA + A = AB, A = 9   ==>   AB + B = BA, B = 9 (letters, choice order)
    _rn_q(M, 'q-533', 'A and B represent different nonzero digits. Given: $\\overline{AB}+B=\\overline{BA}$\n$B=?$',
          ['$8$', '$9$', '$5$', '$1$'], 2, [
        'Tens column: A plus the carry gives B. A and B are different, so the carry is 1 and $B=A+1$.',
        'Ones column: $B+B=10+A$ (it carries 1). With $A=B-1$: $2B=10+B-1$, so $B=9$ and $A=8$.',
        'Check: $89+9=98$ ✓. (Or plug in the choices: only $B=9$ works.)'])
    # q-534: ABC - BBB = 198 -> 4   ==>   ABC - BBB = 297 -> 6
    _rn_q(M, 'q-534', 'A, B and C represent digits. Given: $\\overline{ABC}-\\overline{BBB}=297$\n$A-C=?$',
          ['$5$', '$6$', '$3$', '$7$'], 2, [
        'Flip it into an addition: $\\overline{BBB}+297=\\overline{ABC}$.',
        'Tens column: $B+9$ must end in $B$. That works only with a carry of 1 from the ones: $B+9+1=B+10$ ✓, and 1 carries into the hundreds.',
        'Ones column: $B+7$ carries 1, so $C=B+7-10=B-3$. Hundreds column: $B+2+1=A$, so $A=B+3$.',
        '$A-C=(B+3)-(B-3)=6$. Check with $B=4$: $444+297=741$, and $7-1=6$ ✓.'])
    # q-535: 1A x B = 9B -> 19 x 5   ==>   1A x B = 8B -> 17 x 5
    _rn_q(M, 'q-535', 'A and B represent different digits. Given: $\\overline{1A}\\times B=\\overline{8B}$\nWhich of the following could be A?',
          ['$4$', '$9$', '$7$', '$3$'], 3, [
        'Plug in the choices. $A=7$: $17\\times B$ must be in the 80s, so $B=5$: $17\\times5=85=\\overline{8B}$ ✓.',
        '$A=9$: $19\\times4=76$ and $19\\times5=95$ — never in the 80s. $A=4$: $14\\times6=84$, which ends in 4, not in $B=6$. $A=3$: $13\\times6=78$ and $13\\times7=91$ — never in the 80s.'])
    # q-536: AA x BB = ACA, 33   ==>   44 (other choices)
    _rn_q(M, 'q-536', 'A, B and C represent digits. Given: $\\overline{AA}\\times\\overline{BB}=\\overline{ACA}$\nWhich of the following could be $\\overline{AA}$?',
          ['$55$', '$44$', '$88$', '$66$'], 2, [
        'Try each choice with the smallest BB, 11:',
        '$55\\times11=605$, $66\\times11=726$ and $88\\times11=968$: the first and last digits are different ✗. $44\\times11=484$ ✓ ($A=4$, $C=8$).',
        'A bigger BB does not help 55, 66 or 88: $55\\times22=1210$, $66\\times22=1452$ and $88\\times22=1936$ have four digits.'])
    # q-537: digits 1-7, remainder < 3, A cannot be 7   ==>   digits 1-8, remainder < 4, A cannot be 8
    _rn_q(M, 'q-537', 'A and B represent different digits from 1 to 8. When $\\overline{AB}$ is divided by 11, the remainder is less than 4. Which of the following cannot be A?',
          ['$2$', '$8$', '$5$', '$7$'], 2, [
        'Plug in the choices. For $A=8$, $\\overline{AB}$ is one of 81, 82, 83, 84, 85, 86, 87. $88=8\\cdot11$, so these leave the remainders 4, 5, 6, 7, 8, 9, 10 — never less than 4. So A cannot be 8.',
        'The others work: $23=22+1$, $56=55+1$ and $78=77+1$ (remainder 1).'])
    # q-538: digit sum = 4 x ones digit -> 31   ==>   5 x ones digit -> 41
    _rn_q(M, 'q-538', 'A and B represent nonzero digits. $\\overline{AB}$ is a two-digit prime number. The sum of its digits is 5 times its ones digit. $A+B=?$',
          ['$10$', '$5$', '$8$', '$12$'], 2, [
        '$A+B=5B$, so $A=4B$. The options are 41 and 82.',
        '82 is not prime: $82=2\\cdot41$. So $\\overline{AB}=41$ and $A+B=5$.'])
    # q-539: BBBB / BB = A0A (101)   ==>   BBBBBB / BBB = A00A (1001)
    _rn_q(M, 'q-539', 'A and B represent digits, and $B\\ne0$. Given: $\\overline{BBBBBB}\\div\\overline{BBB}=\\overline{A00A}$\n$A=?$',
          ['$0$', '$2$', '$1$', '$5$'], 3, [
        'Plug in $B=1$: $111{,}111\\div111=1001$. So $\\overline{A00A}=1001$ and $A=1$.',
        'It works for every B: $\\overline{BBBBBB}=111{,}111\\cdot B$ and $\\overline{BBB}=111\\cdot B$, so the quotient is always $1001$. Check: $444{,}444\\div444=1001$ ✓.'])
    # q-540: 1AB - BA = B3 -> 147 - 74   ==>   1AB - BA = B2 -> 168 - 86
    _rn_q(M, 'q-540', 'A and B represent nonzero digits. Given: $\\overline{1AB}-\\overline{BA}=\\overline{B2}$\n$A+B=?$',
          ['$12$', '$14$', '$16$', '$18$'], 2, [
        'Flip it into an addition: $\\overline{BA}+\\overline{B2}=\\overline{1AB}$.',
        'Ones column: $A+2$ ends in $B$. If it carried, B would be 0 or 1, and the tens $B+B+1$ could not reach 10. So nothing carries and $B=A+2$.',
        'Plug in the choices: $A+B=14$ gives $A=6$ and $B=8$. Check: $168-86=82=\\overline{B2}$ ✓.',
        'The others fail: $A=5$, $B=7$ gives $157-75=82\\ne72$. $A=7$, $B=9$ gives $179-97=82\\ne92$. $A+B=18$ would need $B=10$.'])
    # extra-bank warm-up kept: "4 times the digit sum, tens digit 2" was the lesson's own example (12, 24, 36, 48)
    _rn_q(M, 'alg-extra-unit-t18-3-6', 'A two-digit number is 7 times the sum of its digits. Its tens digit is 6. What is its ones digit?',
          ['$1$', '$3$', '$6$', '$9$'], 2, [
        'Plug in the choices: $63=7\\cdot(6+3)$ ✓.',
        'The others fail: $61\\ne7\\cdot7$, $66\\ne7\\cdot12$, $69\\ne7\\cdot15$.',
        'Algebraic form: $60+b=7(6+b)$, so $18=6b$ and $b=3$.',
        'Method 2 · Words, no columns: write the number as $10A+B$ and collect. $10A+B=7(A+B)$, so $3A=6B$ and $A=2B$. The tens digit is $6$, so the ones digit is $3$.'])


def rn_practice(M):
    """Approved clean-up: copies out, at most 3 extra-bank warm-ups, September items whose type the Hebrew covers out."""
    X = 'alg-extra-unit-t18-3-'; N = lambda k: 'q-r26-t18-' + k
    out = [
        # copies (practice_audit/copies_by_topic.txt, each checked)
        X + '1',      # digit sum 11, reversal 27 smaller: the same 9(A - B) = 27 as q-524
        N('08'),      # ones digit of 2^50: the worked example of the "Number Facts" lesson
        # extra-bank warm-ups beyond 3 (kept: X5 AAA divisible by 37, X6 k times the digit sum, X7 4A + 4A = 9B)
        X + '2',      # AB = 6(A + B): the same digit-word type as X6
        X + '3',      # ones digit of 38 x 47: the same type as the kept q-r26-t18-07
        # September items of a type the Hebrew practice covers
        N('05'),      # middle column -> 9 with a carry: q-534, q-540
        N('06'),      # how many digits a product has: q-521
        N('09'),      # AAA / 37: repdigits, q-539 (and the lesson's 555 = 37 x 15)
        N('10'),      # ABC - CBA = 693: q-532
    ]
    for qid in out:
        if qid in M.D['questions'] and any(f['ref'] == qid for f in M.D['flow']) and M.section_of(qid) == PRACTICE:
            M.unplace(qid)
    M.practice_order(PRACTICE, [
        X + '5', 'q-521', 'q-524', X + '6', 'q-523', 'q-539', 'q-522', 'q-525', 'q-529', X + '7', 'q-527', N('07'),
        'q-531', 'q-528', 'q-530', 'q-538', 'q-532', 'q-526', 'q-533', 'q-535', 'q-534', N('04'), 'q-536', 'q-537',
        'q-540'])


def rn_titles(M):
    """Solution videos: title and slide description show the new stems."""
    for f in M.D['flow']:
        if f['topic'] != TOPIC or f['type'] != 'video': continue
        v = M.video(f['ref']); qid = v.get('questionId')
        if not qid or qid not in M.D['questions'] or f['ref'].startswith('solve-q-r26') or f['ref'] in RN_RECORDED: continue
        stem = M.q(qid)['stem']
        v['title'] = v['navLabel'] = stem
        for b in v['beats']:
            if b['mode'] == 'question':
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, stem)
        M.touched_videos.add(f['ref'])


def renumber_pass(M):
    rn_lessons(M)
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_titles(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-06 Hebrew back-check. The renumber pass compared only with base-v18; the teacher's Hebrew VIDEO subtitles
# (01-Algebra-Original-Subtitles.txt, letters = lines 18204-18764) showed that q-517 had landed exactly on the Hebrew
# sample question (AB·AB = 2CB, B−A = 5, 16² = 256) and q-513 was the Hebrew lesson example with the letters renamed
# (BA·A = CA). New versions (same type, trap, level and methods). Card / summary examples that were the Hebrew
# lesson's own examples get other numbers. Nothing in topic 18 is recorded.
# ======================================================================================================
def _hb_deep(x, pairs, hits):
    if isinstance(x, str):
        for old, new in pairs:
            if old in x: x = x.replace(old, new); hits[old] = hits.get(old, 0) + 1
        return x
    if isinstance(x, list): return [_hb_deep(y, pairs, hits) for y in x]
    if isinstance(x, dict): return {k: _hb_deep(y, pairs, hits) for k, y in x.items()}
    return x


def hebrew_backcheck(M):
    # ---------- q-513: CB × B = AB (= Hebrew BA × A = CA, letters renamed)   ==>   CB × B = ACB, B = 5 (25 × 5 = 125)
    _rn_q(M, 'q-513', 'A, B and C represent digits. Given: $\\overline{CB}\\times B=\\overline{ACB}$\nWhich of the following could be B?',
          ['$7$', '$5$', '$0$', '$4$'], 2, [
        'Ones column: $B\\times B$ ends in $B$. Only the special digits do this: $0, 1, 5, 6$ ($0\\cdot0=0$, $1\\cdot1=1$, $5\\cdot5=25$, $6\\cdot6=36$).',
        'Choices (1) and (4) fail: $7\\cdot7=49$ and $4\\cdot4=16$.',
        'Choice (3) fails: $B=0$ makes the product $0$, not a three-digit number.',
        'Choice (2): $B=5$ and $C=2$ give $25\\times5=125$ ✓.'])
    _rn_video(M, 'q-513', [[
        "Step one: vertically.",
        A('The vertical layout appears: CB × B = ACB', T(ARR('CB', '\\times\\ \\ \\ B', 'ACB'), 50, **VERT)),
        "Step two: the ones. B times B ends in B.",
        D('Circle the B in the ones column of every line'),
        "A digit times itself that keeps its ones digit — that's a special digit. Zero, one, five or six.",
        A("'5 × even → 0, 5 × odd → 5, 6 × even keeps it' appears", SPECIAL_T),
        "Two more facts about them: five times an even number ends in zero, times an odd number in five. Six times an even number keeps its ones digit — six times fourteen, eighty-four.",
        D('Write "B ∈ {0, 1, 5, 6}"'),
        D('Cross out choices 1 and 4'),
        "Seven and four aren't special. Seven times seven is forty-nine. Four times four is sixteen. Out.",
        "From the choices, that leaves five — or zero.",
        D('Cross out choice 3'),
        "Zero? Zero times anything is zero — not a three-digit number. Out.",
        D('Circle choice 2'),
        "So B is five. Choice two.",
    ], [
        "Quick check by plugging in. B is five — try C as two.",
        D('Write "25 · 5 = 125"'),
        "Twenty-five times five: one hundred twenty-five. A is one, C is two, and it ends in five. It works.",
        D('Circle choice 2'),
        "Choice two.",
    ]])

    # ---------- q-517: AB·AB = 2CB, B − A could be 5 (= the Hebrew sample question)   ==>   CA·CA = 6BA, A − C could be 4
    _rn_q(M, 'q-517', 'A, B and C represent digits. Given: $\\overline{CA}\\times\\overline{CA}=\\overline{6BA}$\nWhich of the following could be $A-C$?',
          ['$6$', '$2$', '$4$', '$5$'], 3, [
        'Size first: $24^2=576$ is too small, and $27^2=729$ is too big. So $\\overline{CA}$ is 25 or 26, and $C=2$.',
        'Ones column: $A\\times A$ ends in $A$, so A is a special digit. Here $A=5$ or $A=6$.',
        '$25^2=625$ ✓ gives $A-C=5-2=3$, which is not a choice. $26^2=676$ ✓ gives $A-C=6-2=4$.'])
    _rn_video(M, 'q-517', [[
        "Method one: the full math. First — estimate the size.",
        "CA times CA is CA squared, and it's six hundred and something.",
        D('Write "24² = 576, 25² = 625, 26² = 676, 27² = 729"'),
        "Twenty-four squared is five seventy-six — too small. Twenty-seven squared, seven twenty-nine — too big.",
        "So CA is twenty-five or twenty-six. C is two.",
        "Now the ones: A times A ends in A — a special digit. Zero, one, five or six.",
        "Both fit: twenty-five squared ends in five, twenty-six squared ends in six.",
        D('Next to 625 write "A − C = 3"'),
        "A is five: twenty-five squared, six twenty-five. A minus C is three — not offered. They asked what COULD be.",
        D('Next to 676 write "A − C = 4" and circle choice 3'),
        "A is six: twenty-six squared, six seventy-six. Six minus two: four. Choice three.",
    ], [
        "Method two — the insight. A times A ends in A, so A is zero, one, five or six.",
        "Every choice is positive, and C is a leading digit — at least one. So A can't be zero or one.",
        D('Write "A ≠ 0, 1 → A = 5 or 6"'),
        "And C? Twenty squared is four hundred, thirty squared is nine hundred. Six hundred and something is in between.",
        D('Write "20² = 400, 30² = 900 → C = 2"'),
        "So CA is in the twenties: C is two.",
        "A minus C is five minus two or six minus two: three or four. Only four is offered.",
        D('Write "26² = 676 ✓" and circle choice 3'),
        "Check: twenty-six squared, six seventy-six. Six hundred and something, ending in six. It fits. Choice three.",
    ]])
    for qid in ['q-513', 'q-517']:
        v = M.video('solve-' + qid); q = M.q(qid)
        v['title'] = v['navLabel'] = q['stem']
        for b in v['beats']:
            if b.get('canvas', '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])

    # ---------- card examples that were the Hebrew lesson's own (08, 5 + 0, 5·4 = 20, 5·7 = 35, 6·8 = 48)
    c = M.card('mem-letters'); hits = {}
    pairs = [('we write $8$, not $08$', 'we write $7$, not $07$'), ('$5+0=5$', '$4+0=4$'),
             ('$5\\cdot4=20,\\ 5\\cdot7=35$', '$5\\cdot8=40,\\ 5\\cdot9=45$'), ('$6\\cdot8=48$', '$6\\cdot14=84$')]
    c['tables'] = _hb_deep(c['tables'], pairs, hits)
    for old, _ in pairs: assert hits.get(old), old
    # ---------- summary: 15² = 225, 16² = 256 are the Hebrew sample question's squares
    _rn_lines(M, 'r26-t18-summary', 6, [('$15\\cdot15=225$, $16\\cdot16=256$', '$35\\cdot35=1225$, $46\\cdot46=2116$')])


_apply_before_hebrew_backcheck = apply


def apply(M):
    _apply_before_hebrew_backcheck(M)
    hebrew_backcheck(M)   # 2026-10-06 Hebrew back-check: runs last


# =====================================================================================================================
# 2026-10-07 methods spread: the 2026-10-06 exam methods shown wherever they genuinely help (teacher: "I don't want the
# students to miss out on it"). (a) a written line appended to the explanation, (b) for a few UNRECORDED solution
# videos one short extra slide at the end. A recorded video is never changed: any video with a file in
# ~/Documents/Course.recordings is skipped at build time (its written line is still added). Runs LAST.
# =====================================================================================================================
import glob as _sp_glob, os as _sp_os, re as _sp_re


def _sp_recorded():
    out = set()
    for f in _sp_glob.glob(_sp_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = _sp_re.match(r'(.+)-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$', _sp_os.path.basename(f))
        # only takes recorded BEFORE the spread was first built (2026-10-07 12:55 local = 09:55Z) keep the old video;
        # later takes were recorded with the new slides, so the slides must stay
        if m and m.group(2) < '2026-10-07T09-55-00': out.add(m.group(1))
    return out

SPREAD_LINES = {
    # Write 10A + B and collect (the "Words, no columns" move of 2026-10-06), used here on column puzzles too.
    'q-r26-t18-01': [
        'Method 2 · Write 10A + B and collect: $206+10A+10B+8=304+10A$. $10A$ is on both sides and cancels, so $10B=90$ and $B=9$. No carry to forget.'],
    'q-533': [
        'Method 2 · Write 10A + B and collect: $(10A+B)+B=10B+A$, so $9A=8B$. Two different nonzero digits: $A=8$ and $B=9$.'],
    'q-535': [
        'Method 2 · Write 10A + B and collect: $(10+A)\\cdot B=80+B$, so $B(A+9)=80$. With digits: $5\\cdot16$ gives $A=7$, $B=5$ (and $8\\cdot10$ gives $A=1$, which is not a choice). The answer is $7$.'],
    'q-r26-t18-04': [
        'Method 2 · Write 10A + B and collect: $3(10A+8)=100+10A+4$, so $30A+24=104+10A$, $20A=80$ and $A=4$.'],
    'alg-extra-unit-t18-3-7': [
        'Method 2 · Write 10A + B and collect: $2(40+A)=90+B$, so $2A=10+B$. $B\\ge0$, so $2A\\ge10$ and $A\\ge5$.'],
    'q-526': [
        'Method 2 · Write 10A + B and collect: with $B=A+1$ and $C=A+2$, $\\overline{ABC}+\\overline{AAA}=(111A+12)+111A=222A+12$. It must be a whole hundred: $A=4$ gives $900$ (the others give $234$, $456$, $678$, …).'],
}

SPREAD_SLIDES = {
    'solve-q-r26-t18-01': ('Plug in to check', 'Method 2 · Write 10A + B and collect', [
        "Another way — no columns at all. Write each number by its digits.",
        A('206 + 10A + 10B + 8 = 304 + 10A appears', T(r'$206+10A+10B+8=304+10A$', size=40)),
        "Ten A is on both sides. It cancels — that's why A can be any digit.",
        A('10B = 304 − 214 = 90 → B = 9 appears', T(r'$10B=304-214=90\;\to\;B=9$', size=40)),
        "Ten B is ninety, so B is nine. No carry to forget.",
        D('Circle choice 4'),
        "Choice four.",
    ]),
}

SPREAD_SAY = {}


def spread_methods(M):
    for qid, lines in SPREAD_LINES.items():
        q = M.q(qid)
        if all(l not in q['explanation'] for l in lines):
            M.set_q(qid, expl=list(q['explanation']) + lines)
    rec = _sp_recorded()
    for vid, (after, title, script) in SPREAD_SLIDES.items():
        if vid in rec: continue   # recorded: never change it
        beats = M.video(vid)['beats']
        n = next(i for i, b in enumerate(beats, 1) if b['title'] == after)
        b = beats[n - 1]
        M.insert_slides(vid, n, [dict(mode='question', active=b['active'], title=title,
                                      pre=[dict(it) for it in b['items'][:b['pre']]], script=script)])
        for k, old, new in SPREAD_SAY.get(vid, []):
            sl = M.slide(vid, k)
            assert any(l.get('say') == old for l in sl['lines']), (vid, k, old)
            for l in sl['lines']:
                if l.get('say') == old: l['say'] = new
            M.touched_videos.add(vid)


_apply_before_spread_methods = apply


def apply(M):
    _apply_before_spread_methods(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


# ===================================================================================================================
# 2026-10-07 trim added repeats. Teacher: "My only concern is places where YOU added it. Where the original (Hebrew)
# course teaches something in multiple subjects, that's OK." Content we added that re-teaches something the student
# already learned earlier in the study plan is trimmed (helpers: _trim_repeats.py). Recorded videos are never changed
# (a take from before _trim_repeats.CUTOFF keeps the old video).
def _tr_load():
    import importlib.util, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_trim_repeats.py')
    spec = importlib.util.spec_from_file_location('_trim_repeats', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m


def trim_added_repeats(M):
    from dsl import T, A, D
    R = _tr_load()
    # r26-t18-facts "Powers: units digit": the cycle of units digits of powers was taught in topic 21 (Patterns &
    # Cycles) and topic 15 (More Remainder Tools). Removed; one reminder line.
    G = 'r26-t18-facts'
    if not R.recorded(G):
        R.drop_slide(M, G, 'Powers: ones digit')
        R.set_slide(M, G, 'Number Facts', [
            'Number facts for letter puzzles.',
            'A few patterns come back again and again on the exam. Two of them first — the questions teach the rest.',
            'And units digits of powers repeat in a cycle — as you learned in patterns.'])


_apply_before_trim_added_repeats = apply


def apply(M):
    _apply_before_trim_added_repeats(M)
    trim_added_repeats(M)   # 2026-10-07 trim added repeats: runs last


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
    _mn_load().method_names(M, 18)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 Hebrew points restored. The 2026-10-05 cut shortened "Exercises with Letters" to the Hebrew intro on the
# assumption that the questions teach the rest. Three points of the teacher's Hebrew lesson were lost (the questions only
# answered): the leftmost digit is never zero (only on the board, never said), WHY plugging in is the core of the
# technique (a computer would try everything; the steps only save plug-ins), and the teacher's remarks on q-514
# (AB ± BA comes back on the exam; algebraic form = the strong students' route, plugging in is usually faster).
# Nothing in topic 18 is recorded; HB.add_lines skips a video that has a take. See t18_CHANGES.md.
# =====================================================================================================================
import importlib.util as _ilu_hb, os as _os_hb
_s_hb = _ilu_hb.spec_from_file_location('_hebrew_back', _os_hb.path.join(_os_hb.path.dirname(_os_hb.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu_hb.module_from_spec(_s_hb); _s_hb.loader.exec_module(HB)


def hebrew_points_back(M):
    # lesson "Exercises with Letters" - why plugging in is step four (and the base of the whole technique)
    if not HB.add_lines(M, 'digit-puzzles', 'The 4 steps', 'Four: plug in numbers and see what fits', [
            'Here\'s the truth: every letter question can be solved by plugging in. A computer would just try every option.',
            'We\'re not computers. So steps one to three are shortcuts — they tell us what we no longer need to plug in.']):
        HB.add_expl(M, 'q-512', 'Every letter question can be solved by plugging in numbers; the first three steps only save plug-ins.')
    # lesson - the leftmost digit is never zero (the board shows A from 1 to 9; it was never said)
    if not HB.add_lines(M, 'digit-puzzles', 'What letters mean', 'Circle the 1', [
            'And the leftmost digit is never zero. Nobody writes oh-six — it\'s not a phone area code. It\'s just six.']):
        HB.add_expl(M, 'q-512', 'A leftmost digit is never zero.')
    # q-514: the pattern comes back on the exam
    if not HB.add_lines(M, 'solve-q-514', 'Plug in numbers', 'And the pattern: AB plus BA', [
            'Worth remembering — this pattern comes back on the exam.']):
        HB.add_expl(M, 'q-514', 'Worth remembering: this pattern comes back on the exam.')
    # q-514: which route the teacher recommends
    if not HB.add_lines(M, 'solve-q-514', 'Algebraic form', 'Eleven times anything is divisible by eleven', [
            'Some students who are strong in math like this route.',
            'My advice: on the exam, two quick numbers are usually faster. The algebra just shows why it always works.']):
        HB.add_expl(M, 'q-514', 'Strong math students may prefer the algebraic form; on the exam, plugging in two numbers is usually faster.')


_apply_before_hebrew_points_back = apply
def apply(M):
    _apply_before_hebrew_points_back(M)
    hebrew_points_back(M)   # 2026-10-08 Hebrew points restored: runs LAST


# =====================================================================================================================
# 2026-10-09 spoken labels -> speech (teacher: "take off words like 'notice:' that seem like I'm reading"): spoken
# lines that open with "Careful:", "Notice:", "Step one:", "The trap:"... are rewritten by hand in her spoken style, in
# place (same line count, cues unchanged). Data and rules: _spoken_labels.py (a video recorded before its CUTOFF keeps
# its old lines). Runs LAST.
# =====================================================================================================================
def _sl_load():
    import importlib.util, os, sys
    if '_spoken_labels' in sys.modules: return sys.modules['_spoken_labels']   # one copy: its WARN / CHANGED add up
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_spoken_labels.py')
    spec = importlib.util.spec_from_file_location('_spoken_labels', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); sys.modules['_spoken_labels'] = m
    return m


_apply_before_spoken_labels = apply


def apply(M):
    _apply_before_spoken_labels(M)
    _sl_load().spoken_labels(M, 18)   # 2026-10-09 spoken labels: runs LAST
