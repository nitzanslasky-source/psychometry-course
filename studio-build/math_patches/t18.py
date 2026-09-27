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
            "In any other column there may be a carry. Then Y can be nine: one X seven plus Y five — Y is nine.",
            A("'Carry: two numbers → 0 or 1' appears", T('Carry, two numbers: $0$ or $1$', 44, gap=20)),
            A("'Carry: three or four numbers → up to 2 or 3' appears", T('Carry, three or four numbers: up to $2$ or $3$', 44)),
            "Two numbers carry zero or one. Three or four numbers can carry more: eight plus eight plus eight — carry two.",
        ]),
        C(3, [
            "Now the leftmost digit.",
            A("'Two numbers, sum with more digits → leading digit 1' appears", T('Two numbers, sum with more digits $\\to$ leading digit $1$:  $99+99=198$', 40, gap=40)),
            "Add TWO numbers and get more digits? The leading digit is one.",
            A("'Four numbers: at most 4 · 999 = 3996' appears", T('Four three-digit numbers: at most $4\\cdot999=3996$', 42, gap=40)),
            "Only for two numbers. Four numbers can start with two or three.",
            A('24² = 576 and 27² = 729 appear', T('Estimate:  $24^2=576$,  $27^2=729$', 44)),
            "And estimate the size — it throws out choices fast.",
        ]),
        C(4, [
            "The special digits: zero, one, five and six.",
            A("'d · d ends in d: 0, 1, 5, 6' appears", T('$d\\cdot d$ ends in $d$:  $0,\\ 1,\\ 5,\\ 6$  ($5\\cdot5=25$, $6\\cdot6=36$)', 42, gap=40)),
            "Multiply one by itself — the ones digit stays. No other digit does that.",
            A("'5 × even ends in 0, 5 × odd ends in 5' appears", T('$5\\,\\times$ even ends in $0$;  $5\\,\\times$ odd ends in $5$', 44, gap=20)),
            A("'6 × even keeps its digit' appears", T('$6\\,\\times$ an even digit keeps it:  $6\\cdot8=48$', 44)),
            "Five times even ends in zero, times odd ends in five. Six times an even digit keeps that digit: six times eight, forty-eight.",
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
            A('ABC − CBA = 99(A − C) appears', T('$\\overline{ABC}-\\overline{CBA}=99(A-C)$:  $521-125=396$', 42, gap=40)),
            "A number minus its reversal: divisible by nine. With three digits, by ninety-nine — middle digit nine.",
            A('AAA = 111A = 3 · 37 · A appears', T('$\\overline{AAA}=111A=3\\cdot37\\cdot A$', 44, gap=20)),
            A('BBBB ÷ BB = 101 appears', T('$\\overline{BBBB}\\div\\overline{BB}=101$', 44)),
            "Triple digits: divisible by three and thirty-seven. And BBBB over BB is always one hundred one.",
        ]),
        C(7, [
            "Products and powers.",
            A("'Ones digit of a product: only the ones digits' appears", T('Ones digit of a product: $38\\cdot47\\to8\\cdot7=56\\to6$', 42, gap=40)),
            A("'Digits of a product: add the counts, or one fewer' appears", T('Digits of a product: add the counts, or one fewer', 42, gap=40)),
            "Two-digit times two-digit: four digits, or three.",
            A('The cycle of 2 appears', T('Ones digits of powers repeat:  $2,\\ 4,\\ 8,\\ 6,\\ 2,\\ 4,\\ \\ldots$', 42, gap=20)),
            A('The ones digit of 2⁵⁰ appears', T('$2^{50}$:  $50=4\\cdot12+2\\ \\to$ like $2^2$, ends in $4$', 42)),
            "The ones digits of powers repeat in a cycle. Find where you land in the cycle.",
        ]),
        C(8, [
            "Largest or smallest with a given digit sum.",
            A("'Digit sum 8: largest 800, smallest 107' appears", T('Digit sum $8$:  largest $800$ · smallest $107$', 48)),
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
