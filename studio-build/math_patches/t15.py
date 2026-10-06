"""Topic 15 - Division & Remainder. Course review 2026-09 fixes.
See t15_CHANGES.md for the plain-language list.
Topic order is unchanged (T15 still comes before T16), so the products of consecutive integers are taught here."""
import re
from dsl import T, H, A, D, Q
from math_api import _word

TOPIC = 15
LESSON = 'divisibility'
TOOLS = 'r26-t15-remainder-tools'
THEORY = 'divisibility-theory'
ADV = 'divisibility-advanced'
PRACTICE = 'unit-t15-3'
GROUP = {THEORY: ('Remainder Questions', 45), ADV: ('Advanced Remainders', 46)}


# ----------------------------------------------------------------------------------------- helpers
def _solution(M, qid, section, intro, slides):
    """Guided-question solution video in the style of solve-q-423..436 (numbers are fixed by renumber_guided)."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % _word(n)] + intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=0, title=title, pre=[Q(qid)], script=script))
    group, num = GROUP[section]
    v = M.new_video('solve-' + qid, TOPIC, group, ['Question %d' % n], beats, section, kind='solution', qid=qid)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = num
    return n


def _say(M, vid, n, old, new):
    """Replace the spoken line that contains `old` with `new` (str, or a list of script items)."""
    def fn(lines):
        out, hit = [], False
        for l in lines:
            if not hit and 'say' in l and old in l['say']:
                hit = True
                for x in (new if isinstance(new, list) else [new]):
                    out.append({'say': x} if isinstance(x, str) else {'draw': x[1]})
            else:
                out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _colon_draws(M, vid):
    """Teacher notes: '45 : 3 = 15' -> '45 ÷ 3 = 15'."""
    for n in range(1, len(M.video(vid)['beats']) + 1):
        def fn(lines):
            for l in lines:
                if 'draw' in l: l['draw'] = re.sub(r'(\d) : (\d)', r'\1 ÷ \2', l['draw'])
            return lines
        M.edit_lines(vid, n, fn)


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Main lesson "Division & Remainder"
    # =====================================================================================
    # slide 5: the "same trick for any bigger number" rule was wrong (12 = 2·6). Parts must share no factor.
    M.set_slide(LESSON, 5, title='Build a divisor', pre=[], script=[
        "Six is a strange bird. It has no sign of its own.",
        A('Divisible by 6: by 2 AND by 3 appears', T('Divisible by $6$: by $2$ AND by $3$', size=44)),
        "But six is two times three. So a number that divides by two AND by three divides by six.",
        A('162 appears', T('$162$', size=60, gap=50)),
        D('Under it write "even ✓   1 + 6 + 2 = 9 ✓"'),
        "One sixty-two: even — two ✓. Digit sum nine — three ✓. So it divides by six.",
        "Same trick for bigger numbers — with one condition.",
        A('Split into parts with no common factor appears', T('Bigger divisors: split into parts with no common factor', size=42)),
        A('12 = 3·4, 15 = 3·5, 18 = 2·9, 24 = 3·8 appears',
          T('$12=3\\cdot4\\qquad15=3\\cdot5\\qquad18=2\\cdot9\\qquad24=3\\cdot8$', size=46)),
        "Twelve is three times four. Fifteen: three times five. Eighteen: two times nine. Twenty-four: three times eight.",
        A('Trap: 12 = 2·6 appears', T('Trap: $12=2\\cdot6$ ✗', size=46)),
        "Why not two times six? Look at six itself.",
        D('Write "6: ÷2 ✓  ÷6 ✓  but ÷12 ✗"'),
        "Six divides by two, and by six — but not by twelve. Two and six share a two, so the check fails.",
        "So the parts must share no factor. Three and four share nothing — that works.",
    ])

    # slide 6: one rule for 11 (alternate + and −), any length, negative results explained
    M.set_slide(LESSON, 6, pre=[], script=[
        "Eleven — the hardest one.",
        "Two-digit? No wisdom needed: forty-four, sixty-six, seventy-seven, eighty-eight.",
        A('Alternate + − + − appears', T('Alternate $+\\ -\\ +\\ -$ → a multiple of $11$ ($0$, $11$, $-11$)', size=42)),
        "Longer numbers: go digit by digit — plus, minus, plus, minus.",
        A('715 appears', T('$715$:  $7-1+5=11$ ✓', size=50)),
        "Seven fifteen: seven, minus one, plus five — eleven. So it divides by eleven.",
        "For three digits, that's just the outer digits minus the middle one.",
        A('1,331 appears', T('$1{,}331$:  $1-3+3-1=0$ ✓', size=50)),
        "Four digits, same idea. One thousand three hundred thirty-one: one, minus three, plus three, minus one — zero.",
        "Zero counts. Zero divides by eleven — so the number does.",
        A('482 appears', T('$482$:  $4-8+2=-2$ ✗', size=50)),
        "Four eighty-two: four, minus eight, plus two — minus two.",
        "A negative result is fine to get. But minus two isn't zero, eleven or minus eleven. So four eighty-two doesn't divide by eleven.",
        "Most exam numbers are simple — one twenty-one, one thirty-two. But be ready.",
    ])

    # slide 7: nested fractions - multiply the denominators (the old "÷4 and ÷5" rule was wrong in general)
    M.set_slide(LESSON, 7, pre=[T('$\\frac{1}{4}$ of the zebras wear pajamas. Of those, $\\frac{1}{5}$ love to sleep late.', size=42, gap=60)], script=[
        "Why do we need all this? For divisibility stories — word problems solved with these signs.",
        "How many zebras could there be? We can't know exactly.",
        "But we CAN know what's impossible. There's no such thing as a quarter of a zebra.",
        "Build it from the inside out. Call the late sleepers k.",
        D('Under the story write "k → 5k → 20k"'),
        "The pajama zebras are five times that: five k. All the zebras are four times the pajama zebras: twenty k.",
        A('Multiply the denominators: 4·5 = 20 appears', T('Multiply the denominators: $4\\cdot5=20$', size=44)),
        "So the number must divide by four times five — twenty.",
        "Careful: it's not just \"by four and by five\". Take half of a quarter.",
        D('Write "½ of ¼: k → 2k → 8k → ÷8"'),
        "k, two k, eight k. It must divide by eight.",
        "Four divides by two and by four. But a quarter of four zebras is one zebra — and half a zebra doesn't exist.",
        "\"What could it be?\" really means: eliminate what it can't be.",
        "You'll do exactly this in the first question after the lesson.",
    ])

    # slides 8 and 9: division written with ÷, not ":"
    M.slide(LESSON, 8)['items'][0]['t'] = '$53\\div7$'
    M.slide(LESSON, 9)['items'][0]['t'] = '$4\\div7$'
    M.touched_videos.add(LESSON)

    # slide 12: combine remainders - add the difference and "d | a, d | a+b -> d | b"
    M.set_slide(LESSON, 12, active=11, pre=[T('$a$ leaves $4$, $b$ leaves $5$ (dividing by $7$)', size=44, gap=60)], script=[
        "One quick bonus — and the exam uses it a lot.",
        D('Write "a + b: 4 + 5 = 9 → 2"'),
        "Their sum? Add the remainders: nine. Nine divided by seven leaves two.",
        D('Write "a · b: 4 · 5 = 20 → 6"'),
        "Their product? Multiply the remainders: twenty. Twenty divided by seven leaves six.",
        D('Write "a − b: 4 − 5 = −1 → −1 + 7 = 6"'),
        "Their difference, when a is bigger? Subtract: four minus five is minus one.",
        A('Negative? Add the divisor appears', T('Negative? Add the divisor: $-1+7=6$', size=44)),
        "A remainder can't be negative. So add seven: six.",
        D('Write "check: a = 18, b = 12 → 18 − 12 = 6 ✓"'),
        "Check: eighteen leaves four, twelve leaves five. Eighteen minus twelve is six. Right.",
        "The complete sevens never matter. Only the leftovers do.",
        A('a and a + b divide by d → b divides by d appears', T('$a$ and $a+b$ divide by $d$ → $b$ divides by $d$', size=44)),
        "And one more. If a divides by seven, and a plus b divides by seven — then b divides by seven too.",
        "a brings no remainder, the sum has none — so b can't bring one either.",
    ])

    # new slide after 12: change the divisor (q-441, q-453 and the Q13 claims need it)
    M.insert_slides(LESSON, 12, [dict(mode='concept', active=12, title='Change the divisor', script=[
        "What if the question changes the divisor?",
        A('x leaves 3 when divided by 10. By 5? appears', T('$x$ leaves $3$ when divided by $10$. By $5$?', size=44)),
        D('Write "x = 10k + 3 = 5 · 2k + 3 → r3"'),
        "x is ten k plus three. Ten k is five times two k — full fives. So x divided by five leaves three.",
        A('x leaves 8 when divided by 10. By 5? appears', T('$x$ leaves $8$ when divided by $10$. By $5$?', size=44)),
        D('Write "8 = 5 + 3 → r3"'),
        "If the old remainder is too big, divide it again. Eight divided by five leaves three.",
        A('x leaves 3 when divided by 6. By 4? appears', T('$x$ leaves $3$ when divided by $6$. By $4$?', size=44)),
        D('Write "x = 3 → r3,   x = 9 → r1   → can\'t know"'),
        "By four? Try: three leaves three. Nine leaves one. Two different answers — you can't know.",
        A('Only if the new divisor divides the old one appears', T('Works only if the new divisor divides the old one', size=42)),
        "The rule: five divides ten, so it works. Three divides six, so it works. Four doesn't divide six — so it doesn't.",
    ])])

    # new slide after 11: the digit sum gives the remainder by 3 or 9
    M.insert_slides(LESSON, 11, [dict(mode='concept', active=10, title='Digit sum → remainder', script=[
        "One more gift from the digit sum.",
        A('Same remainder as the digit sum appears', T('Dividing by $3$ or $9$: same remainder as the digit sum', size=42)),
        A('5,432 appears', T('$5{,}432$', size=60, gap=50)),
        D('Under it write "5 + 4 + 3 + 2 = 14"'),
        "Five thousand four hundred thirty-two. Digit sum: fourteen.",
        D('Write "14 ÷ 9 → r5   so   5,432 ÷ 9 → r5"'),
        "Fourteen divided by nine leaves five. So five thousand four hundred thirty-two divided by nine leaves five too.",
        D('Write "14 ÷ 3 → r2   so   5,432 ÷ 3 → r2"'),
        "By three: fourteen leaves two. So the big number leaves two.",
        "Only for three and nine! The digit sum tells you nothing about the remainder by four, or by seven.",
    ])])

    # recap (now slide 15)
    M.set_slide(LESSON, 15, active=13, pre=[], script=[
        "Honestly? There's not much to memorize here.",
        A('2, 5, 10 / 3, 9 appears', T('$2, 5, 10$: last digit · $3, 9$: digit sum', size=42)),
        A('4 / 8 appears', T('$4$: last two digits · $8$: last three digits', size=42)),
        A('Parts with no common factor appears', T('Bigger divisors: parts with no common factor — $12=3\\cdot4$', size=42)),
        A('11 appears', T('$11$: $+\\,-\\,+\\,-$ → $0$ or $\\pm11$', size=42)),
        A('Remainder < divisor appears', T('Remainder $<$ divisor · biggest $=$ divisor $-\\ 1$', size=42)),
        A('Combine remainders appears', T('Combine remainders: add, multiply, subtract', size=42)),
        "Two, five and ten you knew. Three and nine — one idea.",
        D('Circle "biggest = divisor − 1"'),
        "Eleven is the odd one out — a little practice and you've got it.",
        "Now five questions. Come in focused — remainders are the part that confuses people.",
    ])
    M.set_sidebar(LESSON, ['By 2, 5 and 10', 'By 3 and 9', 'By 4 and 8', 'Build a divisor', 'By 11',
                           'Divisibility stories', 'What a remainder is', 'The remainder trap', 'Biggest remainder',
                           'Algebraic form', 'Digit sum → remainder', 'Combine remainders', 'Change the divisor', 'Recap'])

    # memory card of the lesson
    c = M.card('mem-divisibility')
    c['tables'] = [
        {'title': 'Divisibility signs', 'head': ['Divisible by', 'Check', 'Example'], 'rows': [
            ['$2$', 'last digit is even', '$376$'],
            ['$5$', 'last digit is $0$ or $5$', '$330$, $2{,}745$'],
            ['$10$', 'last digit is $0$', '$330$'],
            ['$3$', 'digit sum divides by $3$', '$417 \\to 12$'],
            ['$9$', 'digit sum divides by $9$', '$765 \\to 18$'],
            ['$4$', 'last two digits divide by $4$', '$3{,}524 \\to 24$'],
            ['$8$', 'last three digits divide by $8$', '$6{,}320 \\to 320$'],
            ['$6$', 'divisible by $2$ AND by $3$', '$162$'],
            ['$12$, $15$, $18$, $24$', 'split into parts with no common factor: $3\\cdot4$, $3\\cdot5$, $2\\cdot9$, $3\\cdot8$',
             'NOT $12=2\\cdot6$: $6$ divides by $2$ and by $6$, but not by $12$'],
            ['$11$', 'alternate $+\\,-\\,+\\,-$; the result is $0$ or $\\pm11$', '$715$: $7-1+5=11$; $1{,}331$: $1-3+3-1=0$'],
        ]},
        {'title': 'Remainders', 'head': ['Fact', 'Example'], 'rows': [
            ['$N = d\\cdot q + r$', '$53 = 7\\cdot7 + 4$'],
            ['$0 \\le r < d$', '$4\\div7$ leaves $4$ (not $3$)'],
            ['Biggest remainder $= d - 1$', 'dividing by $5$: at most $4$'],
            ['Remainder $r$ when dividing by $d$: $N = dk + r$', '$6k+2$: $2, 8, 14, 20, \\ldots$'],
            ['By $3$ or $9$: same remainder as the digit sum', '$5{,}432 \\to 14$: leaves $5$ by $9$, $2$ by $3$'],
            ['Sum, product: add or multiply the remainders', 'leave $4$ and $5$ by $7$: sum $9\\to2$, product $20\\to6$'],
            ['Difference: subtract; if negative, add the divisor', '$4-5=-1 \\to -1+7=6$'],
            ['$a$ and $a+b$ divide by $d$ → $b$ divides by $d$', '$3$ divides $6$ and $6+b$ → $3$ divides $b$'],
            ['New divisor that divides the old one: keep the remainder (divide it again if too big)',
             'leaves $8$ by $10$ → leaves $3$ by $5$; by $6$ → by $4$: unknown'],
        ]},
        {'title': 'Divisibility stories', 'head': ['Situation', 'Method', 'Example'], 'rows': [
            ['A fraction of a fraction', 'build from the inside and multiply the denominators',
             '$\\frac14$ of $\\frac15$: $k\\to5k\\to20k$; $\\frac12$ of $\\frac14$: divisible by $8$'],
        ]},
    ]
    c['tips'] = ['"What could the number be?" → eliminate what it can\'t be.',
                 '"Which expression could be the number?" → plugging in $x = 0$ is safe and fast (each choice keeps its remainder).',
                 '"Necessarily divisible by?" → never plug in a value that gives $0$: zero divides by everything.']

    # =====================================================================================
    # 2. Learn section 1: existing guided questions 1-4
    # =====================================================================================
    _colon_draws(M, 'solve-q-423')
    _colon_draws(M, 'solve-q-424')
    _say(M, 'solve-q-426', 3, 'For this type, plugging in', [
        "Only sixteen leaves one. Choice three. For this type, plugging in is usually the quickest route.",
        "And here zero is safe: each choice leaves the same remainder for every x.",
        "In a \"necessarily divisible\" question it's different — zero divides by everything, so never plug in a value that gives zero.",
    ])

    S('q-423', expl=[
        'A third of the class are chess girls, so the class divides by 3. A quarter of the chess girls play the piano, so the chess group divides by 4.',
        'Build it from the inside: piano players $k$, chess girls $4k$, the class $3\\cdot4k=12k$. The class divides by 12.',
        'Only $48=12\\cdot4$ works: $48\\div3=16$ and $16\\div4=4$ ✓.',
        '$45\\div3=15$, but 15 does not divide by 4. 40 and 26 do not divide by 3.'])
    S('q-424', expl=[
        'We need a number that leaves remainder 3 when divided by 4 and remainder 2 when divided by 5. Test the choices.',
        '$42=4\\cdot10+2$: remainder 2, not 3 ✗.',
        '$27=4\\cdot6+3$ ✓ and $27=5\\cdot5+2$ ✓. Both conditions hold.',
        '$22=4\\cdot5+2$ ✗ and $12=4\\cdot3+0$ ✗.'])
    S('q-425', stem='$a$ and $b$ are positive integers. $x$ is the remainder when $a$ is divided by 7, and $y$ is the remainder when $b$ is divided by 4. What is the greatest possible value of $x\\cdot y$?',
      expl=['The biggest remainder is one less than the divisor: $x\\le7-1=6$ and $y\\le4-1=3$.',
            'Both are possible, for example $a=6$ and $b=3$. So the greatest value is $6\\cdot3=18$.',
            '28 is the trap: $7\\cdot4$. A remainder is always smaller than the divisor.'])
    S('q-426', stem='A number leaves a remainder of 1 when divided by 3. Which of the following expressions could represent the number ($x$ is an integer)?',
      expl=['A multiple of 3 plus a number: only that number decides the remainder.',
            '(1) $3x+5=3(x+1)+2$, so the remainder is 2 ✗.',
            '(2) $6x+8=3(2x+2)+2$, so the remainder is 2 ✗.',
            '(3) $(3x+4)^2=9x^2+24x+16=3(3x^2+8x+5)+1$, so the remainder is 1 ✓.',
            '(4) $(3x+6)^2=9(x+2)^2$, so the remainder is 0 ✗.',
            'Faster: plug in $x=0$: $5$, $8$, $16$, $36$ leave $2$, $2$, $1$, $0$. Here $x=0$ is safe, because each expression leaves the same remainder for every $x$.'])

    # =====================================================================================
    # 3. New guided question 5: remainder of a difference
    # =====================================================================================
    g1 = 'q-r26-t15-01'
    M.new_q(g1, TOPIC, '$a$ and $b$ are positive integers, and $a>b$. When $a$ is divided by 7, the remainder is 2. When $b$ is divided by 7, the remainder is 5. What will be the remainder if $a-b$ is divided by 7?',
            ['$3$', '$4$', '$5$', 'It cannot be determined from the information given.'], 2, [
        'Subtract the remainders: $2-5=-3$.',
        'A remainder cannot be negative, so add the divisor: $-3+7=4$.',
        'Check: $a=9$, $b=5$: $9-5=4$ ✓. $a=23$, $b=12$: $23-12=11=7+4$ ✓.',
        'Trap: $5-2=3$ subtracts in the wrong order.'])
    M.place_q(g1, THEORY, after='solve-q-426')
    _solution(M, g1, THEORY, ["The remainder of a difference."], [
        ('Method 1 · Subtract the remainders', [
            "a leaves two, b leaves five — both when divided by seven. What does a minus b leave?",
            D('Write "a − b: 2 − 5 = −3"'),
            "Subtract the remainders: two minus five. Minus three.",
            "A remainder can't be negative. So add the divisor, seven.",
            D('Write "−3 + 7 = 4"'),
            "Minus three plus seven: four.",
            D('Circle choice 2'),
            "Choice two. Choice one is the trap: five minus two — the wrong order.",
        ]),
        ('Method 2 · Check with numbers', [
            "Not sure? Build real numbers.",
            D('Write "a = 9, b = 5 → 9 − 5 = 4 ✓"'),
            "Nine leaves two. Five leaves five. Nine minus five: four.",
            D('Write "a = 23, b = 12 → 11 → r4 ✓"'),
            "One more: twenty-three and twelve. The difference is eleven. Eleven divided by seven leaves four.",
            "Both examples agree with method one. Choice two.",
        ]),
    ])

    # =====================================================================================
    # 4. New lesson video at the start of the advanced section: five tools
    #    (take away the remainder, counting multiples, units digit, numbers in a row, plugging in)
    # =====================================================================================
    sb = ['Take away the remainder', 'Counting multiples', 'Units digit', 'Numbers in a row', 'Plugging in: the rule', 'Recap']
    M.new_video(TOOLS, TOPIC, 'More Remainder Tools', sb, [
        dict(mode='title', title='More Remainder Tools', script=[
            "Before the advanced questions: five short tools.",
            "Each one turns a hard-looking question into a quick one.",
        ]),
        dict(mode='concept', active=0, title='Take away the remainder', script=[
            "First tool. Take away the remainder — and what's left divides exactly.",
            A('N leaves r → N − r divides by d appears', T('$N$ leaves $r$ → $N-r$ divides by $d$', size=46)),
            D('Write "53 = 7 · 7 + 4  →  53 − 4 = 49 = 7 · 7"'),
            "Fifty-three divided by seven leaves four. Take away the four: forty-nine. Seven times seven — no remainder.",
        ]),
        dict(mode='concept', active=1, title='Counting multiples', script=[
            "Second tool: how many multiples are there in a range?",
            A('How many three-digit numbers divide by 11? appears', T('How many three-digit numbers divide by $11$?', size=44)),
            "The trick: find the first one and the last one.",
            D('Write "first: 110 = 11 · 10"'),
            "The first three-digit multiple of eleven: one hundred ten. Eleven times ten.",
            D('Write "last: 990 = 11 · 90"'),
            "The last: nine hundred ninety. Eleven times ninety.",
            A('Count = last k − first k + 1 appears', T('Write both as $11\\cdot k$: count $=$ last $k\\,-$ first $k\\,+\\,1$', size=42)),
            D('Write "90 − 10 + 1 = 81"'),
            "So we count the numbers from ten to ninety. Ninety minus ten, plus one: eighty-one.",
            "Don't forget the plus one — both ends count.",
            D('Write "3 to 7: 3, 4, 5, 6, 7 → 7 − 3 + 1 = 5"'),
            "Not sure? Check it small. From three to seven there are five numbers, not four.",
        ]),
        dict(mode='concept', active=2, title='Units digit', script=[
            "Third tool: the units digit.",
            A('Units digit of a product appears', T('The units digit of a product depends only on the units digits', size=42)),
            D('Write "12 · 286 → 2 · 6 = 12 → ends in 2"'),
            "Twelve times two eighty-six. You don't need the full product. Two times six is twelve — so it ends in two.",
            "Sums work the same way: add only the units digits.",
            A('Powers repeat: 7, 9, 3, 1 appears', T('Powers repeat: $7,\\ 9,\\ 3,\\ 1,\\ 7,\\ 9,\\ \\ldots$', size=46)),
            D('Write "7¹ → 7,  7² = 49 → 9,  7³ → 9 · 7 = 63 → 3,  7⁴ → 3 · 7 = 21 → 1"'),
            "Powers of seven. Seven. Seven times seven is forty-nine: nine. Nine times seven is sixty-three: three. Three times seven is twenty-one: one.",
            "Then seven again. Only the last digit gets multiplied each time — so the pattern repeats every four steps.",
            D('Write "7²⁰: 20 ÷ 4 = 5, no remainder → ends like 7⁴ → 1"'),
            "Seven to the twentieth? Twenty divides by four exactly — so it ends like seven to the fourth: in one.",
        ]),
        dict(mode='concept', active=3, title='Numbers in a row', script=[
            "Fourth tool — the harder questions need it: consecutive integers, numbers in a row.",
            A('Two in a row: divides by 2 appears', T('Two in a row: one is even → divides by $2$', size=44)),
            D('Write "7 · 8 = 56    12 · 13 = 156"'),
            "Two numbers in a row: one of them is always even. So their product divides by two.",
            A('Three in a row: divides by 6 appears', T('Three in a row: divides by $2\\cdot3=6$', size=44)),
            D('Write "4 · 5 · 6 = 120    7 · 8 · 9 = 504 = 6 · 84"'),
            "Three in a row: one of them divides by three — every third number does. And at least one is even.",
            "Two and three have no common factor. So the product divides by six.",
            A('Hidden: a³ − a = (a − 1)a(a + 1) appears', T('Hidden: $a^3-a=(a-1)\\,a\\,(a+1)$', size=44)),
            "Watch for them in disguise. a cubed minus a: take out a, and a squared minus one is a minus one, times a plus one. Three in a row.",
            "And n squared minus n is n times n minus one. Two in a row — always even.",
            D('Write "n(n + 2):  1 · 3 = 3,  but 2 · 4 = 8 ✗"'),
            "Only numbers IN A ROW. n times n plus two? One times three is three — but two times four is eight. No three there.",
        ]),
        dict(mode='concept', active=4, title='Plugging in: the rule', script=[
            "Last tool: plugging in numbers. It's fast — but know what it can and can't do.",
            A('One value that fails knocks out a choice appears', T('One value that fails → the choice is out', size=44)),
            "\"Necessarily divisible by?\" One number that fails knocks out a choice. That's proof.",
            A('Values that work prove nothing appears', T('Values that work prove nothing', size=44)),
            "But a number that works proves nothing. Maybe the next one fails.",
            A('Avoid 0 appears', T('Avoid values that give $0$ — zero divides by everything', size=42)),
            "And never plug in a value that gives zero. Zero divides by every number, so it knocks out nothing.",
            A('n(n + 1)(n + 2) appears', T('$n(n+1)(n+2)$ is necessarily divisible by: $6$? $12$? $24$?', size=42)),
            D('Write "n = 2: 2 · 3 · 4 = 24 → 6 ✓ 12 ✓ 24 ✓"'),
            "Try it. n equals two gives twenty-four. All three choices survive!",
            D('Write "n = 1: 1 · 2 · 3 = 6 → 6 ✓ 12 ✗ 24 ✗"'),
            "So try a second value. n equals one gives six. Twelve and twenty-four are out. The answer is six.",
            "The rule: keep plugging in until only one choice is left.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            "Let's lock it in.",
            A('Take away the remainder appears', T('Leaves $r$ → $N-r$ divides by $d$', size=40)),
            A('Counting multiples appears', T('Count multiples: last $k\\,-$ first $k\\,+\\,1$', size=40)),
            A('Units digit appears', T('Units digit: use only the units digits', size=40)),
            A('Numbers in a row appears', T('In a row: two → by $2$, three → by $6$', size=40)),
            A('Plugging in appears', T('Plug in to knock out — not to prove. Avoid $0$.', size=40)),
            D('Tick each line'),
            "Now the advanced questions. Try each one first — then watch.",
        ]),
    ], ADV, before='q-427')

    M.new_card('mem-r26-t15-tools', TOPIC, ADV, {
        'title': 'More remainder tools',
        'intro': 'The tools of the advanced questions, each with one example.',
        'tables': [{'title': 'Tools', 'head': ['Situation', 'Method', 'Example'], 'rows': [
            ['Known remainder', '$N-r$ divides by $d$', '$53\\div7$ leaves $4$ → $53-4=49=7\\cdot7$'],
            ['How many multiples of $d$?', 'write the first and last as $d\\cdot k$; count $=$ last $k-$ first $k+1$',
             'three-digit multiples of $11$: $110=11\\cdot10$ to $990=11\\cdot90$ → $81$'],
            ['Units digit', 'multiply or add only the units digits; powers repeat', '$7, 9, 3, 1, 7, \\ldots$; $7^{20}$ ends in $1$'],
            ['Numbers in a row', 'two → divides by $2$; three → divides by $6$', '$a^3-a=(a-1)a(a+1)$; $n^2-n=n(n-1)$'],
            ['Not in a row', 'no guarantee', '$n(n+2)$: $1\\cdot3=3$, $2\\cdot4=8$'],
        ]}],
        'tips': ['Plugging in: one value that fails knocks out a choice. Values that work prove nothing — keep going until one choice is left.',
                 'Never plug in a value that gives $0$ in a "necessarily divisible" question.',
                 'The smallest case gives the biggest POSSIBLE divisor, not the answer: $A(A+4)(A+8)$ with $A=2$ gives $120$, but only $24$ is certain.'],
    }, after=TOOLS)

    # =====================================================================================
    # 5. Advanced section: existing guided questions
    # =====================================================================================
    # Q (q-427): no ratio (taught only in T22) - use the fraction 3/5
    M.set_slide('solve-q-427', 2, title='Percent → fraction → divisible by 3', script=[
        "This is a divisibility story. First, turn the percentage into a fraction.",
        D('Next to the question write "60% = 60/100 = 3/5"'),
        "Sixty percent is sixty over a hundred — three fifths.",
        "Build it from the inside, like the zebras. Call a fifth of the school k.",
        D('Write "school = 5k → French = 3k"'),
        "The school has five k students. Three k of them study French. So the number of French students must divide by three.",
        "How do we test for three? The digit sum must divide by three.",
        D('Next to the choices write the digit sums: 10, 11, 12, 13'),
        "Four sixty: ten — no. Four seventy: eleven — no.",
        "Four eighty: twelve — twelve divides by three.",
        D('Circle choice 3'),
        "Choice three. In the exam, circle it and move on. Four ninety? Thirteen — out anyway.",
    ])

    # Q (q-430): count exactly (first and last multiple), then the estimate with its limit
    M.set_slide('solve-q-430', 2, title='Method 1 · Count exactly', script=[
        "Two claims about how many numbers divide by something. Let's count — first and last multiple.",
        "Eitan first. Divisible by both two and five: they have no common factor, so that's divisible by ten.",
        D('Under Eitan write "10: 100 = 10·10 … 990 = 10·99 → 99 − 10 + 1 = 90"'),
        "The first three-digit multiple of ten is ten times ten. The last is ten times ninety-nine. Ninety-nine minus ten, plus one: ninety.",
        D('Write "11: 110 = 11·10 … 990 = 11·90 → 90 − 10 + 1 = 81"'),
        "Eleven: from eleven times ten to eleven times ninety. Eighty-one.",
        "Ninety beats eighty-one. Eitan is right.",
        D('Cross out choices 2 and 3'),
        "Dana. Three and four — no common factor — so divisible by twelve. Two and seven — divisible by fourteen.",
        D('Under Dana write "12: 108 = 12·9 … 996 = 12·83 → 83 − 9 + 1 = 75"'),
        "Twelve: from twelve times nine to twelve times eighty-three. Eighty-three minus nine, plus one: seventy-five.",
        D('Write "14: 112 = 14·8 … 994 = 14·71 → 71 − 8 + 1 = 64"'),
        "Fourteen: from fourteen times eight to fourteen times seventy-one. Sixty-four.",
        "Seventy-five beats sixty-four. Dana is right too.",
        D('Circle choice 4'),
        "Both are right. Choice four.",
    ])
    M.insert_slides('solve-q-430', 2, [dict(mode='question', active=M.slide('solve-q-430', 2)['active'],
                                            title='Method 2 · Estimate', pre=[Q('q-430')], script=[
        "On the exam, there's a faster way to compare.",
        D('Write "1/10 > 1/11    1/12 > 1/14"'),
        "Every tenth number divides by ten. Every eleventh divides by eleven. One tenth is more than one eleventh.",
        "Same for Dana: one twelfth beats one fourteenth.",
        "The smaller the number, the more numbers divide by it.",
        "But be careful: this works here because the range is long — nine hundred numbers. In a short range the estimate can be off by one. Then count exactly.",
    ])])

    # Q (q-431): plugging in is right here because we look for the claim that can FAIL
    _say(M, 'solve-q-431', 3, 'Here plugging in is much shorter', [
        "Choice four. Here plugging in is perfect: we look for the claim that can fail, and one example where it fails is proof.",
        "The three claims that worked with b equals three? One example doesn't prove them — the algebra does.",
    ])

    # Q (q-432): link to the tools video; one clear plug-in rule
    _say(M, 'solve-q-432', 2, 'A product of three consecutive integers',
         "Three numbers in a row: one divides by three, and at least one is even. So the product divides by six.")
    _say(M, 'solve-q-432', 3, 'Only choice two survives', [
        "Only choice two survives — so it must be the answer.",
        "If two choices had survived, we'd try a second value, like a equals three.",
    ])

    # Q (q-435): two methods, one plug-in rule, the change-the-divisor rule
    _say(M, 'solve-q-435', 1, 'three ways to decide', 'Three claims about a remainder — two ways to decide.')
    _say(M, 'solve-q-435', 2, 'Gal: x divides by nine?',
         "Gal: x divides by nine? Nine does NOT divide six. From a remainder by six, you can't know the remainder by nine.")
    _say(M, 'solve-q-435', 2, 'Understanding is the recommended route', 'Only Gal is wrong — choice three.')
    _say(M, 'solve-q-435', 3, "Plugging in works — but here", "Plugging in works — but remember what it can prove.")
    _say(M, 'solve-q-435', 3, 'Use plugging in only if', [
        "Choice three. The example x equals three proves Gal wrong.",
        "For Adam and Ben, two examples that work are not proof. Method one proves them.",
    ])

    # ----- stems and solutions of the advanced guided questions
    S('q-427', stem='$60\\%$ of the students in a school study French. Which of the following numbers could be the number of students who study French?',
      expl=['$60\\%=\\frac{60}{100}=\\frac35$. Build it from the inside: the school has $5k$ students, and $3k$ of them study French.',
            'So the number of French students divides by 3. Digit sums: $460\\to10$ ✗, $470\\to11$ ✗, $480\\to12$ ✓, $490\\to13$ ✗.',
            'Only 480 (for example, a school of 800 students).'])
    S('q-428', stem='A slot machine shows a three-digit number. Its hundreds digit is 8, its tens digit is 5, and its units digit is $X$.\nThe machine pays:\n5 shekels if the number is divisible by 2 but not by 3;\n10 shekels if it is divisible by 3 but not by 2;\n15 shekels if it is divisible by both 2 and 3.\nMaya played once and won 15 shekels. How many different values can $X$ have?',
      expl=['15 shekels means the number is divisible by 2 and by 3.',
            'By 3: the digit sum $8+5+X=13+X$ divides by 3, so $X=2$, $5$ or $8$.',
            'By 2: $X$ is even, so $X=2$ or $X=8$ (852 and 858). Two values.'])
    S('q-429', expl=[
        '$12=3\\cdot4$, and 3 and 4 have no common factor. So check 4 (last two digits) and 3 (digit sum). Not $2\\cdot6$: 6 divides by 2 and by 6, but not by 12.',
        'Last two digits: 36, 48, 24 and 44 all divide by 4.',
        'Digit sums: $1{,}236\\to12$ ✓, $2{,}148\\to15$ ✓, $3{,}224\\to11$ ✗, $4{,}344\\to15$ ✓.',
        'Only $3{,}224$ is not divisible by 3, so it is not divisible by 12.'])
    S('q-430', stem='Eitan claims: "There are more three-digit numbers divisible by both 2 and 5 than three-digit numbers divisible by 11."\nDana claims: "There are more three-digit numbers divisible by both 3 and 4 than three-digit numbers divisible by both 2 and 7."\nWhich of the following is correct?',
      choices=['Only Eitan is right.', 'Only Dana is right.', 'Both are wrong.', 'Both are right.'],
      expl=['Count the multiples: write the first and the last as $d\\cdot k$, then count $=$ last $k-$ first $k+1$.',
            'By 2 and 5, that is by 10: from $100=10\\cdot10$ to $990=10\\cdot99$, so $99-10+1=90$ numbers. By 11: from $110=11\\cdot10$ to $990=11\\cdot90$, so $90-10+1=81$. Since $90>81$, Eitan is right.',
            'By 3 and 4, that is by 12: from $108=12\\cdot9$ to $996=12\\cdot83$, so $83-9+1=75$. By 2 and 7, that is by 14: from $112=14\\cdot8$ to $994=14\\cdot71$, so $71-8+1=64$. Since $75>64$, Dana is right too.'])
    S('q-431', stem='Given:\n$\\begin{cases} c=5a \\\\ a=\\frac{b}{3} \\end{cases}$\n$a$, $b$ and $c$ are positive integers. Which claim is not necessarily true?',
      choices=['$c$ is divisible by $5$', '$b$ is divisible by $3$', '$a+b+c$ is divisible by $9$', '$a+b$ is divisible by $16$'],
      expl=['Write everything with $a$: $b=3a$ and $c=5a$.',
            '$c=5a$ divides by 5 ✓. $b=3a$ divides by 3 ✓. $a+b+c=a+3a+5a=9a$ divides by 9 ✓.',
            '$a+b=4a$. For $a=1$: $a+b=4$, which is not divisible by 16. So claim (4) is not necessarily true.'])
    S('q-432', stem='Given: $x=3a^3-3a$ ($a$ is a positive integer). $x$ is necessarily divisible by:',
      expl=['Factor: $x=3a(a^2-1)=3(a-1)a(a+1)$.',
            '$(a-1)a(a+1)$ is three numbers in a row, so it divides by 6. Therefore $x$ divides by $3\\cdot6=18$.',
            'Check with $a=2$: $x=3\\cdot8-3\\cdot2=18$. It is not divisible by 12, 24 or 36, so only 18 is certain.'])
    S('q-433', stem='Given: $x=12a+8$ ($a$ is a positive integer), and $x$ is divisible by 10. Which of the following could be the value of $a$?',
      expl=['$x$ divides by 10, so $x$ ends in 0. Since $x=12a+8$, $12a$ ends in 2.',
            'The units digit of $12a$ depends only on $2\\cdot$(the units digit of $a$): $2\\cdot5=10$, $2\\cdot6=12$ ✓, $2\\cdot7=14$, $2\\cdot8=16$.',
            'So $a=286$. Check: $12\\cdot286+8=3{,}432+8=3{,}440$ ✓.'])
    S('q-434', stem='Omar entered a casino with 500 tokens. In round 1 he lost $x$ tokens, in round 2 he lost $2x$ tokens, and in round 3 he lost $3x$ tokens. Which of the following could be the number of tokens he had left after the three rounds?',
      expl=['He lost $x+2x+3x=6x$ tokens, so the number of tokens he lost divides by 6 (by 2 and by 3).',
            'For each choice, find what he lost: $500-10=490$ (digit sum 13 ✗), $500-30=470$ (11 ✗), $500-20=480$ (12 ✓, even ✓), $500-45=455$ (odd ✗).',
            'So 20 tokens are left, and $x=480\\div6=80$.'])
    S('q-435', stem='When $x$ is divided by 6, the remainder is 3.\nAdam claims: "$2x$ is necessarily divisible by 6."\nBen claims: "$x$ is necessarily divisible by 3."\nGal claims: "$x$ is necessarily divisible by 9."\nWhich of the following is correct?',
      choices=['All three are wrong.', 'Only Adam is right.', 'Only Gal is wrong.', 'All three are right.'],
      expl=['Write $x=6k+3$.',
            'Adam: $2x=12k+6=6(2k+1)$ divides by 6 ✓.',
            'Ben: $x=6k+3=3(2k+1)$ divides by 3 ✓. (3 divides 6, so a remainder by 6 also gives the remainder by 3.)',
            'Gal: $k=0$ gives $x=3$, which is not divisible by 9 ✗. (9 does not divide 6, so a remainder by 6 says nothing about 9.)',
            'Only Gal is wrong.'])
    S('q-436', stem='The sum of three integers is divisible by 3. Which of the following statements is not necessarily true?',
      choices=['All three numbers can leave remainder $1$ when divided by $3$.',
               'When one of the numbers is divided by $3$, the greatest possible remainder is $2$.',
               'If two of the numbers are divisible by $3$, then the third is too.',
               'If one of the numbers is divisible by $3$, then the other two are too.'],
      expl=['Think in remainders: the remainders of the three numbers must add up to a multiple of 3.',
            '(1) Possible: $1+4+7=12$, and each number leaves remainder 1.',
            '(2) True: dividing by 3, the remainder is 0, 1 or 2.',
            '(3) True: two numbers leave 0 and the sum leaves 0, so the third leaves 0.',
            '(4) Not necessarily: $6+4+2=12$. 6 divides by 3, but 4 and 2 do not.'])

    # =====================================================================================
    # 7. Practice: text, fixed solutions, removed near-duplicates
    # =====================================================================================
    # Pass 2: the originals alg-extra-unit-t15-3-4 and -3-6 are restored (text clean-up only, see below)

    S('q-437', stem='A class is divided into groups of 3 students. Then it is divided into groups of 5 students. Each time, there is exactly one group with only 2 students. Which of the following could be the number of students in the class?',
      expl=['The number leaves remainder 2 when divided by 3 and when divided by 5.',
            'Take away the remainder: $n-2$ divides by 3 and by 5, so by 15.',
            'Only $32-2=30$ works. ($35-2=33$, $27-2=25$ and $25-2=23$ do not divide by 15.)'])
    S('q-438', stem='Tom has $x$ marbles. He divides them equally among his 4 children. The eldest child divides his share equally among 3 friends, and the second child divides his share equally among 5 friends, with nothing left over. What is the smallest possible value of $x$?',
      expl=['Each child gets $\\frac{x}{4}$ marbles. This share divides by 3 and by 5. They have no common factor, so it divides by 15.',
            'So $x=4\\cdot15k=60k$. The smallest value is $x=60$: each child gets 15, and $15\\div3=5$, $15\\div5=3$ ✓.',
            '20 and 40 fail: $\\frac{20}{4}=5$ and $\\frac{40}{4}=10$ do not divide by 3.'])
    S('q-439', stem='$25\\%$ of the students in a certain college ride bicycles. Which of the following could be the total number of students in the college?',
      expl=['$25\\%=\\frac14$, and the number of riders is a whole number. So the total divides by 4.',
            'Last two digits: $106\\to06$ ✗, $214\\to14$ ✗, $316\\to16$ ✓, and $217$ is odd ✗.',
            'So 316 ($\\frac{316}{4}=79$ riders).'])
    S('q-440', expl=['Alternate plus and minus: $6-9+3=0$, so 693 is divisible by 11 ($693=11\\cdot63$).',
                     'The others: $482$: $4-8+2=-2$ ✗; $925$: $9-2+5=12$ ✗; $997$: $9-9+7=7$ ✗.'])
    S('q-441', stem='When the positive integer $x$ is divided by 10, the remainder is 3. What will be the remainder if $x$ is divided by 5?',
      choices=['$3$', '$1$', '$0$', 'It cannot be determined from the information given.'],
      expl=['$x=10k+3=5\\cdot2k+3$. The part $10k$ is made of full fives.',
            'So the remainder by 5 is 3. (5 divides 10, so the remainder carries over.)'])
    S('q-442', stem='$x$ is a positive integer. $30+10x$ is not necessarily divisible by:',
      expl=['$30+10x=10(3+x)$, so it always divides by 10, and therefore by 2 and by 5.',
            'By 4? Try $x=2$: $30+20=50$, and 50 is not divisible by 4. So 4 is not necessarily a divisor.'])
    S('q-443', stem='When the positive integer $x$ is divided by 9, the remainder is 7. What will be the remainder if $2x$ is divided by 9?',
      expl=['Multiply the remainder: $2\\cdot7=14$, and 14 divided by 9 leaves 5.',
            'With algebra: $2x=2(9k+7)=18k+14=9(2k+1)+5$. Check: $x=7$ gives $2x=14=9+5$ ✓.'])
    S('q-444', stem='$A$ is an even positive integer. Given: $n=A^3+12A^2+32A$. $n$ is necessarily divisible by:',
      expl=['Factor: $n=A(A^2+12A+32)=A(A+4)(A+8)$.',
            'Write $A=2m$: $n=2m(2m+4)(2m+8)=8\\cdot m(m+2)(m+4)$.',
            'One of $m$, $m+2$, $m+4$ divides by 3: if $m$ leaves 0, it is $m$; if $m$ leaves 1, then $m+2$ leaves $1+2=3$, that is 0; if $m$ leaves 2, then $m+4$ leaves $2+4=6$, that is 0. So $n$ divides by $8\\cdot3=24$.',
            'Knock out the others with examples: $A=2$ gives $n=2\\cdot6\\cdot10=120$, which is not divisible by 18 or 32. $A=14$ gives $n=14\\cdot18\\cdot22=5{,}544$, which is not divisible by 60.',
            'Trap: the smallest case (120) is not the answer. It only gives the biggest possible divisor.'])
    S('q-445', stem='Lior has 80 lockers, numbered 1 to 80, and all of them are closed. In round 1 he opens every locker. In round 2 he changes the state of every second locker (2, 4, 6, …): an open locker is closed, and a closed locker is opened. In round 3 he changes the state of every third locker, and so on, up to round 80 (in which he changes only locker 80). Which of the following lockers is open at the end?',
      expl=['Locker $k$ changes state once in every round $d$ where $d$ divides $k$. So it changes state as many times as $k$ has divisors.',
            'It starts closed, so it ends open only after an odd number of changes.',
            'Divisors come in pairs ($d$ and $\\frac{k}{d}$), except when $d\\cdot d=k$. So only perfect squares have an odd number of divisors.',
            '$49=7^2$ (divisors 1, 7, 49: three changes, so it ends open). 50, 55 and 78 are not squares, so they end closed.'])
    S('q-446', stem='Ann, Ben and Carl each have the same number $N$ of building cubes. Ann built 5 towers of equal height, using all her cubes. Ben built 2 towers whose heights differ by exactly 1, using all his cubes. Carl built 3 towers of different heights, using all his cubes, and his tallest tower has 8 cubes. What is the value of $N$?',
      expl=['Ann: $N$ divides by 5. Ben: $N=h+(h+1)=2h+1$, so $N$ is odd. That leaves 15 and 25.',
            'Carl: $N=a+b+8$ with $a<b<8$. The most is $6+7+8=21$, so $N\\ne25$.',
            '$N=15$ works: for example, $3+4+8=15$.'])
    S('q-447', stem='$n$ is a two-digit positive integer, and $n^2-n$ is divisible by 10. What could be the units digit of $n$?',
      expl=['$n^2-n=n(n-1)$: two numbers in a row, so it is always even.',
            'For 10 it also needs a 5: $n$ or $n-1$ divides by 5. So $n$ ends in 0 or 5, or $n-1$ ends in 0 or 5 ($n$ ends in 1 or 6).',
            'Among the choices, only 5. Check: $n=25$: $625-25=600$ ✓.'])
    S('q-448', stem='Given: $y=13x+9$ ($x$ is a positive integer), and $y$ is divisible by 10. Which of the following could be the value of $x$?',
      expl=['$y$ ends in 0, so $13x$ ends in 1 (because $1+9=10$).',
            'The units digit of $13x$ depends only on $3\\cdot$(the units digit of $x$). $3\\cdot7=21$ ends in 1, so $x$ ends in 7.',
            'Only 187 ends in 7. Check: $13\\cdot187+9=2{,}431+9=2{,}440$ ✓.'])
    S('q-449', stem='$n$ is a positive integer divisible by 4. What is the greatest number that necessarily divides $n(n+4)$?',
      expl=['Write $n=4k$: $n(n+4)=4k(4k+4)=16\\cdot k(k+1)$.',
            '$k$ and $k+1$ are two numbers in a row, so $k(k+1)$ is even. Therefore $n(n+4)$ divides by $16\\cdot2=32$.',
            'Nothing bigger is certain: $n=4$ gives $4\\cdot8=32$, which is not divisible by 64.'])
    S('q-450', stem='A mother has $x$ candies. She tries to divide them equally among her 3 children, but 1 candy is left over. Then she decides that the eldest child will get exactly three times as many candies as each of the other two children. This time all the candies are given out. What is the smallest possible value of $x$?',
      expl=['First condition: $x$ leaves remainder 1 when divided by 3.',
            'Second condition: each younger child gets $s$ candies and the eldest gets $3s$, so $x=s+s+3s=5s$. $x$ divides by 5.',
            'Multiples of 5: $5=3+2$ leaves 2 ✗; $10=9+1$ leaves 1 ✓. So $x=10$ (shares 2, 2 and 6).'])
    S('q-451', stem='Given:\n$\\begin{cases} b=3a \\\\ c=3b \\\\ d=3c \\end{cases}$\n($a$ is a positive integer). $a+b+c+d$ is necessarily divisible by:',
      expl=['Write everything with $a$: $b=3a$, $c=9a$, $d=27a$.',
            '$a+b+c+d=a+3a+9a+27a=40a$, so it always divides by 40.',
            'It is not necessarily divisible by 3, 9 or 27: for $a=1$ the sum is 40.'])
    S('q-452', stem="A taxi company's phone number has 5 identical digits (for example, 33333). The company's fax number is the phone number plus 1. What will be the remainder if the sum of the digits of the fax number is divided by 5?",
      expl=['Call the repeated digit $d$.',
            'If $d\\le8$, adding 1 changes only the last digit: the fax digits are $d, d, d, d, d+1$. Their sum is $5d+1$, which leaves remainder 1.',
            'If $d=9$: $99{,}999+1=100{,}000$. The digit sum is 1, so the remainder is 1 again.',
            'Example: $33{,}333\\to33{,}334$, digit sum $16=5\\cdot3+1$ ✓.'])
    S('q-453', stem='When the positive integer $a$ is divided by 6, the remainder is 3. What will be the remainder if $a+2$ is divided by 4?',
      expl=['4 does not divide 6, so the remainder by 6 does not give the remainder by 4. Check with numbers.',
            '$a=3$: $a+2=5$, remainder 1. $a=9$: $a+2=11$, remainder 3.',
            'Two different remainders, so it cannot be determined.'])
    S('q-454', expl=['The numbers that leave 4: $4, 9, 14, 19, \\ldots, 59$. They go up by 5, so they alternate even, odd.',
                     'The even ones end in 4: $4, 14, 24, 34, 44, 54$. That is 6 numbers.'])
    S('q-455', stem='Given: $y=\\frac{\\sqrt3\\cdot x}{2}$, and $y$ is an integer divisible by 6. What is the greatest number that necessarily divides $x^2$?',
      expl=['Solve for $x$: $x=\\frac{2y}{\\sqrt3}$, so $x^2=\\frac{4y^2}{3}$.',
            'Write $y=6k$: $x^2=\\frac{4\\cdot36k^2}{3}=48k^2$. So $x^2$ always divides by 48.',
            'Nothing bigger is certain: $k=1$ gives $x^2=48$.'])
    S('q-456', stem='$x$, $y$ and $z$ are integers, and $x+y+z$ is divisible by 3. Which of the following statements is necessarily not correct?',
      choices=['$x+y$ leaves remainder $2$ when divided by $3$, and $z$ is divisible by $3$.',
               '$x$, $y$ and $z$ each leave remainder $1$ when divided by $3$.',
               '$x$, $y$ and $z$ are all even.',
               '$x$ leaves remainder $2$ when divided by $3$, and $y+z$ leaves remainder $1$ when divided by $3$.'],
      expl=['Add the remainders. In (1): $2+0=2$, so $x+y+z$ would leave 2. That contradicts the given, so (1) is never correct.',
            'The others can happen: (2) $1+4+7=12$ ✓; (3) $2+4+6=12$ ✓; (4) $x=2$, $y=3$, $z=1$: $y+z=4$ leaves 1, and $2+3+1=6$ ✓.'])

    E = 'alg-extra-unit-t15-3-%d'
    S(E % 1, stem='The positive integer $n$ leaves remainder 3 when divided by 5. What will be the remainder if $n+5$ is divided by 5?',
      choices=['$1$', '$3$', '$4$', '$0$'],
      expl=['$n=5k+3$, so $n+5=5k+5+3=5(k+1)+3$.', 'Adding 5 adds one more full five. The remainder stays 3.'])
    S(E % 2, stem='What is the units digit of $7^4$?', choices=['$7$', '$9$', '$1$', '$3$'],
      expl=['Multiply only the units digits: $7\\cdot7=49\\to9$, $9\\cdot7=63\\to3$, $3\\cdot7=21\\to1$.',
            'So $7^4$ ends in 1 (indeed, $7^4=2{,}401$).'])
    S(E % 3, stem='What will be the remainder if $12{,}345$ is divided by 9?', choices=['$6$', '$0$', '$3$', '$5$'],
      expl=['Digit sum: $1+2+3+4+5=15$, and 15 divided by 9 leaves 6.',
            'A number leaves the same remainder by 9 as its digit sum, so the answer is 6.'])
    S(E % 4, stem='A positive integer leaves remainder 3 when divided by 4 and remainder 2 when divided by 5. What is the smallest such number?',
      choices=['$3$', '$12$', '$17$', '$7$'],
      expl=['The numbers that leave 2 when divided by 5 are $2, 7, 12, 17, \\ldots$',
            'Test them in order with 4: $2=4\\cdot0+2$ ✗, $7=4\\cdot1+3$ ✓.',
            'So the smallest number is 7. The other choices: $3=5\\cdot0+3$ ✗, $12=4\\cdot3+0$ ✗, $17=4\\cdot4+1$ ✗.'])
    S(E % 6, stem='What is the smallest positive integer that is divisible by both 8 and 12?',
      choices=['$48$', '$24$', '$16$', '$36$'],
      expl=['This is the least common multiple of 8 and 12. Break into primes: $8=2^3$ and $12=2^2\\cdot3$.',
            'Take each prime with its highest power: $2^3\\cdot3=24$.',
            'Check: $24\\div8=3$ and $24\\div12=2$ ✓. 48 also divides by both, but it is not the smallest. $16\\div12$ and $36\\div8$ are not whole numbers.'])
    S(E % 5, stem='$n$ is an integer. Which of the following expressions is necessarily divisible by 6?',
      expl=['$n(n+1)(n+2)$ is three numbers in a row: one divides by 3, and at least one is even. So the product divides by 6.',
            'The others fail for $n=1$: $1\\cdot3=3$, $1^2+1=2$, $3\\cdot1+1=4$.'])
    S(E % 7, stem='When a positive integer is divided by 9, the quotient is 7 and the remainder is 4. What is the integer?',
      choices=['$63$', '$71$', '$76$', '$67$'],
      expl=['Number $=$ divisor $\\cdot$ quotient $+$ remainder: $9\\cdot7+4=67$.'])

    # =====================================================================================
    # 8. New practice questions (the new methods + exam-level items)
    # =====================================================================================
    new = [
        ('q-r26-t15-05', 'How many integers from 50 to 150 (inclusive) are divisible by 8?',
         ['$11$', '$12$', '$13$', '$18$'], 2,
         ['First: $56=8\\cdot7$. Last: $144=8\\cdot18$.',
          'Count: $18-7+1=12$.',
          'Trap: $18-7=11$ forgets the $+1$.']),
        ('q-r26-t15-06', 'How many three-digit numbers are divisible by both 3 and 8?',
         ['$36$', '$37$', '$38$', '$41$'], 2,
         ['3 and 8 have no common factor, so the numbers divide by 24.',
          'First: $120=24\\cdot5$ ($96=24\\cdot4$ has two digits). Last: $984=24\\cdot41$ ($24\\cdot42=1{,}008$ has four digits).',
          'Count: $41-5+1=37$.']),
        ('q-r26-t15-07', '$a$ and $b$ are positive integers, and $a>b$. When $a$ is divided by 9, the remainder is 3. When $b$ is divided by 9, the remainder is 7. What will be the remainder if $a-b$ is divided by 9?',
         ['$4$', '$5$', '$6$', 'It cannot be determined from the information given.'], 2,
         ['Subtract the remainders: $3-7=-4$. A remainder cannot be negative, so add 9: $-4+9=5$.',
          'Check: $a=12$, $b=7$: $12-7=5$ ✓. $a=21$, $b=16$: $21-16=5$ ✓.',
          'Trap: $7-3=4$ subtracts in the wrong order.']),
        ('q-r26-t15-08', 'When the positive integer $x$ is divided by 5, the remainder is 3. What will be the remainder if $x^2-2x$ is divided by 5?',
         ['$0$', '$1$', '$3$', '$4$'], 3,
         ['Work with the remainder 3: $x^2$ leaves $3\\cdot3=9$, that is 4. $2x$ leaves $2\\cdot3=6$, that is 1.',
          'The difference leaves $4-1=3$.',
          'Check with $x=8$: $64-16=48=5\\cdot9+3$ ✓.']),
        ('q-r26-t15-09', 'Which of the following numbers is divisible by 18?',
         ['$2{,}346$', '$5{,}445$', '$3{,}258$', '$1{,}356$'], 3,
         ['$18=2\\cdot9$, and 2 and 9 have no common factor. (Not $3\\cdot6$: 3 and 6 share a 3.)',
          'Check "even" and "digit sum divides by 9": $2{,}346$: sum 15 ✗. $5{,}445$: sum 18, but odd ✗. $3{,}258$: even, sum 18 ✓. $1{,}356$: sum 15 ✗.',
          'Trap: $2{,}346$ and $1{,}356$ divide by 3 and by 6, but not by 18.']),
        ('q-r26-t15-10', 'The sum of the digits of a positive integer is 40. What will be the remainder if the number is divided by 9?',
         ['$0$', '$3$', '$4$', 'It cannot be determined from the information given.'], 3,
         ['A number leaves the same remainder by 9 as its digit sum.',
          '$40=9\\cdot4+4$, so the remainder is 4.',
          'Example: $99{,}994$ has digit sum 40, and $99{,}994=9\\cdot11{,}110+4$ ✓.']),
        ('q-r26-t15-11', '$\\frac23$ of the members of a club are women, and $\\frac34$ of the women are over 30 years old. Which of the following could be the number of members in the club?',
         ['$15$', '$16$', '$18$', '$20$'], 3,
         ['Build it from the inside. Women over 30: $3k$. All the women: $4k$ (because $\\frac34$ of them is $3k$).',
          'The women are $\\frac23$ of the club, so the club has $\\frac32\\cdot4k=6k$ members. The number divides by 6.',
          'Only 18: 12 women, and 9 of them are over 30 ✓.',
          '15 gives 10 women, and $\\frac34\\cdot10$ is not a whole number. 16 and 20 do not divide by 3.']),
        ('q-r26-t15-12', '$n$ is an odd positive integer. $n^2-1$ is necessarily divisible by:',
         ['$3$', '$6$', '$8$', '$16$'], 3,
         ['$n^2-1=(n-1)(n+1)$. $n$ is odd, so $n-1$ and $n+1$ are two even numbers in a row.',
          'Write $n-1=2m$: $(n-1)(n+1)=2m(2m+2)=4\\cdot m(m+1)$. $m$ and $m+1$ are in a row, so $m(m+1)$ is even. The product divides by $4\\cdot2=8$.',
          'Knock out the others with $n=3$: $3^2-1=8$, which is not divisible by 3, 6 or 16.']),
        ('q-r26-t15-13', 'What is the units digit of $3^{25}$?',
         ['$1$', '$3$', '$7$', '$9$'], 2,
         ['Multiply only the units digits: $3$, $3\\cdot3=9$, $9\\cdot3=27\\to7$, $7\\cdot3=21\\to1$. Then it repeats: $3, 9, 7, 1, \\ldots$',
          'The pattern repeats every 4 powers. $25=4\\cdot6+1$, so $3^{25}$ ends like $3^1$: in 3.']),
        ('q-r26-t15-14', 'A positive integer greater than 1 leaves remainder 1 when divided by 2, by 3, by 4 and by 5. What is the smallest such number?',
         ['$31$', '$41$', '$61$', '$121$'], 3,
         ['Take away the remainder: $n-1$ divides by 2, 3, 4 and 5.',
          'Split into parts with no common factor: $3\\cdot4\\cdot5=60$ (4 already covers 2). So $n-1$ divides by 60.',
          'The smallest: $n-1=60$, so $n=61$. 121 also works, but it is not the smallest.',
          '31 leaves 3 when divided by 4, and 41 leaves 2 when divided by 3.']),
    ]
    for qid, stem, ch, cor, ex in new:
        M.new_q(qid, TOPIC, stem, ch, cor, ex)
        M.place_q(qid, PRACTICE)

    # easy -> hard
    P = lambda k: 'q-r26-t15-%02d' % k
    M.practice_order(PRACTICE, [
        E % 7, E % 1, 'q-441', 'q-439', E % 3, E % 2, E % 6, 'q-454', P(10), E % 5, 'q-442', 'q-443', E % 4, 'q-437',
        P(5), P(7), P(9), 'q-440', 'q-438', 'q-450', 'q-451', 'q-452', 'q-453',
        P(11), P(14), P(6), P(8), 'q-448', 'q-447', 'q-446', 'q-456', P(13), 'q-449', P(12), 'q-444',
        'q-455', 'q-445'])

    # =====================================================================================
    # 9. Solution videos: titles, pre-loaded stem notes and sidebars in sync
    # =====================================================================================
    for sec in (THEORY, ADV):
        vids = [f['ref'] for f in M.D['flow'] if f['section'] == sec and f['type'] == 'video'
                and M.video(f['ref']).get('kind') == 'solution']
        nums = [int(M.video(v)['beats'][0]['bigTitle'].split()[1]) for v in vids]
        for v, n in zip(vids, nums):
            M.set_sidebar(v, ['Question %d' % k for k in nums])
            V = M.video(v); q = M.q(V['questionId'])
            V['title'] = V['navLabel'] = q['stem']
            for b in V['beats']:
                if b['mode'] == 'question':
                    b['active'] = nums.index(n)
                if b.get('canvas', '').startswith('Pre-loaded — question'):
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (q['id'], q['stem'])

    summary(M)
    cut_repeats(M)   # 2026-10-05: last


# ======================================================================================================
# Pass 2: summary video right before the practice (end of the advanced section)
# ======================================================================================================
def summary(M):
    sb = ['Divisibility signs', 'Build a divisor', 'Divisibility stories', 'Remainder basics', 'Combine remainders',
          'Change the divisor', 'Counting and units digits', 'Numbers in a row', 'Before you practice']
    C = lambda i, title, script: dict(title=title, mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice, a quick review of the whole topic.",
            "The signs, the remainder rules, the tools — and the traps."]),
        C(0, 'Divisibility signs', [
            "Know when a number divides — without dividing.",
            A('2, 5, 10', T('$2,\\ 5,\\ 10$: look at the last digit', size=44)),
            A('3, 9', T('$3,\\ 9$: the digit sum divides by $3$ or $9$', size=44)),
            A('4, 8', T('$4$: last two digits · $8$: last three digits', size=44)),
            A('11', T('$11$: $+\\,-\\,+\\,-$ gives $0$ or $\\pm11$ · $913$: $9-1+3=11$', size=42)),
            "Eleven: alternate plus and minus, digit by digit."]),
        C(1, 'Build a divisor', [
            "A bigger divisor? Split it into parts with no common factor.",
            A('Six', T('$6$: by $2$ AND by $3$', size=46)),
            A('Parts', T('$20=4\\cdot5\\qquad36=4\\cdot9\\qquad45=5\\cdot9$', size=46)),
            A('Trap', T('Trap: $24=4\\cdot6$ ✗ — $12$ divides by $4$ and $6$, not by $24$', size=42)),
            "Four and six share a two. So that check proves nothing."]),
        C(2, 'Divisibility stories', [
            "A fraction of a fraction? Build it from the inside.",
            A('Fraction of a fraction', T('$\\frac13$ of $\\frac16$: $k\\to6k\\to18k$', size=48)),
            "Multiply the denominators. The number divides by eighteen.",
            A('Eliminate', T('"What could it be?" → eliminate what it can\'t be', size=44)),
            "There's no such thing as a third of a student."]),
        C(3, 'Remainder basics', [
            "The remainder is always smaller than the divisor.",
            A('Form', T('$N=d\\cdot q+r \\qquad 0\\le r<d$', size=48)),
            A('Biggest', T('Biggest remainder $=d-1$', size=46)),
            "Dividing by nine? The remainder is at most eight.",
            A('Algebraic form', T('Leaves $3$ by $8$: $N=8k+3$ → $3,\\ 11,\\ 19,\\ 27,\\ \\ldots$', size=44)),
            A('Digit sum', T('By $3$ or $9$: same remainder as the digit sum', size=44)),
            "Four thousand eight hundred twenty-six: digit sum twenty, so it leaves two by nine."]),
        C(4, 'Combine remainders', [
            "Only the leftovers matter.",
            A('Setup', T('$a$ leaves $5$, $b$ leaves $7$ (dividing by $8$)', size=44)),
            A('Sum and product', T('$a+b$: $5+7=12\\to4$ · $ab$: $5\\cdot7=35\\to3$', size=44)),
            A('Difference', T('$a-b$: $5-7=-2\\to-2+8=6$', size=44)),
            "Add, multiply, or subtract the remainders. Negative? Add the divisor.",
            A('Take away', T('$N$ leaves $r$ → $N-r$ divides by $d$', size=44)),
            "Take away the remainder, and what's left divides exactly."]),
        C(5, 'Change the divisor', [
            "A new divisor? Check that it divides the old one.",
            A('Works', T('Leaves $11$ by $12$ → by $4$: $11\\to3$', size=46)),
            "Four divides twelve. Keep the remainder — and divide it again if it's too big.",
            A('Unknown', T('Leaves $2$ by $10$ → by $4$: $2\\to2$, but $12\\to0$', size=46)),
            "Four doesn't divide ten. Two answers — you can't know."]),
        C(6, 'Counting and units digits', [
            "How many multiples? First and last.",
            A('Count', T('$14=7\\cdot2$ to $98=7\\cdot14$: $14-2+1=13$', size=44)),
            "Don't forget the plus one — both ends count.",
            A('Units digit', T('Units digit: multiply only the units digits', size=44)),
            A('Powers', T('$2,\\ 4,\\ 8,\\ 6,\\ 2,\\ \\ldots$ → $2^{22}$ ends in $4$', size=46)),
            "Powers repeat every four steps."]),
        C(7, 'Numbers in a row', [
            "Numbers in a row hide everywhere.",
            A('Two', T('Two in a row → divides by $2$', size=46)),
            A('Three', T('Three in a row → divides by $6$', size=46)),
            A('Hidden', T('$a^3-a=(a-1)\\,a\\,(a+1)$', size=46)),
            "Only IN A ROW. n times n plus two is not.",
            A('Plugging in', T('Plug in to knock out — not to prove. Avoid $0$.', size=44)),
            "One value that fails knocks out a choice. Values that work prove nothing."]),
        C(8, 'Before you practice', [
            "Before each question, always ask yourself:",
            A('Check 1', T('1. Parts with no common factor?', size=42)),
            A('Check 2', T('2. Is my remainder smaller than the divisor?', size=42)),
            A('Check 3', T('3. Negative remainder? Add the divisor.', size=42)),
            A('Check 4', T('4. Does the new divisor divide the old one?', size=42)),
            A('Check 5', T('5. Plugging in: did I avoid values that give $0$?', size=42)),
            "And the traps: twenty-four is not four times six, and counting forgets the plus one.",
            "You know all of this. Go practice."]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t15-summary', TOPIC, 'Division & Remainder: Summary', sb, slides, ADV, after=last)


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
    # ---- "Division & Remainder": the signs and the remainder basics stay (Hebrew has them as theory too).
    #      Cut: divisibility stories -> Q1 (q-423); algebraic form -> Q4 (q-426), Q14 (q-435);
    #      combine remainders -> Q5 (q-r26-t15-01) + one line, Q15 (q-436).
    _cr_cut(M, LESSON, ['Divisibility stories', 'Algebraic form', 'Combine remainders'])
    _cr_drop_item(M, LESSON, len(M.video(LESSON)['beats']), 'Combine remainders')
    # Q1: the "multiply the denominators" rule, at the moment it is used
    _cr_add(M, 'solve-q-423', 3, 'Call the piano-players k', [
        A("'A fraction of a fraction → multiply the denominators' appears", T('A fraction of a fraction $\\to$ multiply the denominators: $3\\cdot4=12$', size=38)),
        "The rule: a fraction of a fraction — multiply the denominators. Half of a quarter? It must divide by eight, not just by four."])
    # Q5: sum and product of remainders were only in the lesson
    _cr_add(M, 'solve-q-r26-t15-01', 2, 'Subtract the remainders', [
        A("'Sum, product, difference → work with the remainders' appears", T('Sum, product, difference $\\to$ add, multiply, subtract the remainders', size=38)),
        "Only the leftovers matter. For a sum, add the remainders. For a product, multiply them. For a difference, subtract them."], where='before')
    # Q6 pointed back to the zebras (lesson slide cut)
    _cr_say(M, 'solve-q-427', 2, 'like the zebras', "Build it from the inside, like the chess class. Call a fifth of the school k.")

    # ---- "More Remainder Tools": counting multiples -> Q9 (q-430) + one line; plugging in -> Q4, Q10, Q11, Q14.
    #      Kept: take away the remainder, units digit (powers repeat), numbers in a row (not fully taught in Q11).
    _cr_cut(M, TOOLS, ['Counting multiples', 'Plugging in: the rule', 'Recap'])
    M.set_slide(TOOLS, 1, script=["Before the advanced questions: three short tools.",
                                  "The other tools you'll meet inside the questions themselves."])
    _cr_say(M, TOOLS, 3, 'Third tool: the units digit.', 'Second tool: the units digit.')
    _cr_say(M, TOOLS, 4, 'Fourth tool', 'Third tool — the harder questions need it: consecutive integers, numbers in a row.')
    _cr_add(M, TOOLS, 4, None, ['Now the advanced questions. Try each one first — then watch.'])
    _cr_add(M, 'solve-q-430', 2, 'Ninety-nine minus ten, plus one', [
        A("'Count = last k − first k + 1' appears", T('Count $=$ last $k\\,-$ first $k\\,+\\,1$', size=38)),
        "Don't forget the plus one — both ends count. From three to seven there are five numbers, not four."])


# =====================================================================================
# 2026-10-06 new exam methods: TAG IT (guaranteed factors). Real exams: helps on 15 questions
# ("necessarily divisible", "largest certain divisor", "necessarily an integer"). One slide in "More Remainder
# Tools", one guided question with its solution video (after Question 10, letters and factors), one card row.
# =====================================================================================
def add_methods(M):
    v = M.video(TOOLS); n = len(v['beats'])
    assert v['beats'][n - 1]['title'] == 'Numbers in a row', [b['title'] for b in v['beats']]
    _cr_say_drop = [x for x in _cr_script(M, TOOLS, n) if not (isinstance(x, str) and x.startswith('Now the advanced questions'))]
    M.set_slide(TOOLS, n, script=_cr_say_drop)
    M.set_slide(TOOLS, 1, script=["Before the advanced questions: four short tools.",
                                  "The other tools you'll meet inside the questions themselves."])
    sb = list(v['hybrid']['sidebar']) + ['Tag it']
    M.insert_slides(TOOLS, n, [dict(mode='concept', active=len(sb) - 1, title='Tag it', script=[
        "Fourth tool: tag it. Use it when they ask \"necessarily divisible by\", \"the largest number it must divide\", or \"necessarily an integer\".",
        A("'a multiple of 6 → 6k · b multiple of 10 → 10m' appears", T('$a$ multiple of $6\\to a=6k$;  $b$ multiple of $10\\to b=10m$', size=36, gap=16)),
        "Write each condition as a tag. a is a multiple of six: a is six k. b is a multiple of ten: b is ten m.",
        "k and m are unknown whole numbers — one, seven, a hundred. They guarantee nothing. Only the numbers in front are certain.",
        A("'Multiply: 6k · 10m = 60km → 60' appears", T('Multiply: $6k\\cdot10m=60km\\ \\to\\ 60$', size=36, gap=16)),
        "Multiply: the tags multiply. Six k times ten m is sixty k m. Always divisible by sixty.",
        A("'Add: 6k + 10m = 2(3k + 5m) → only 2' appears", T('Add: $6k+10m=2(3k+5m)\\ \\to$ only $2$', size=36, gap=16)),
        "Add: only the shared factor comes out. Take two out of six k plus ten m. Inside: three k plus five m.",
        "Why not more? Three k plus five m is unknown — it can be eight, or eleven. So nothing inside is certain. Only the two.",
        A("'Divide: ab/15 = 4km ✓ · a/4 = 3k/2 ✗' appears", T('Divide: $\\frac{ab}{15}=\\frac{60km}{15}=4km$ ✓;  $\\frac{a}{4}=\\frac{6k}{4}=\\frac{3k}{2}$ ✗', size=36, gap=16)),
        "Divide: every factor of the bottom must be in the tags on top. a b over fifteen: sixty over fifteen is four — a whole number. a over four: six k has only one two. Three k over two — not always whole.",
        A("'By 4 and by 6 → tag 12k (LCM), not 24k' appears", T('Divisible by $4$ and by $6\\to$ tag $12k$ (the LCM), not $24k$', size=36, gap=16)),
        "Divisible by four and by six? The tag is the smallest number both go into: twelve. Not twenty-four — twelve itself isn't divisible by twenty-four.",
        A("'Plug in? Different values for different letters' appears", T('Plugging in? Different values for different letters', size=36)),
        "Prefer to plug in? Give different letters different values. a and b both thirty: the sum is sixty — and sixty looks certain. But six plus ten is sixteen.",
        "The rule: tag each condition, do the operation, read the number in front.",
        "Now the advanced questions. Try each one first — then watch.",
    ])])
    M.set_sidebar(TOOLS, sb)

    # --- guided question (a different pair than the slide)
    g = 'q-r26-t15-15'
    M.new_q(g, TOPIC, '$x$ and $y$ are positive integers. $x$ is divisible by $6$, and $y$ is divisible by $9$.\n'
                      'What is the largest number that $x+y$ is necessarily divisible by?',
            ['$18$', '$15$', '$9$', '$3$'], 4, [
        'Tag each condition: $x=6k$ and $y=9m$, where $k$ and $m$ are unknown positive integers.',
        'Add: $x+y=6k+9m=3(2k+3m)$. Only the shared factor $3$ comes out. $2k+3m$ is unknown, so it guarantees nothing more.',
        'So $x+y$ is always divisible by $3$. Nothing bigger is certain: $x=6$, $y=9$ gives $15$ (not divisible by $9$ or $18$), '
        'and $x=12$, $y=9$ gives $21$ (not divisible by $15$).',
        'Trap: $x=y=18$ gives $36$, which is divisible by $18$ and by $9$. Different letters need different values.'])
    M.place_q(g, ADV, after='solve-q-431')
    _solution(M, g, ADV, ["A sum of two multiples — and the largest certain divisor."], [
        ('Method 1 · Tag it', [
            "Tag each condition. x is divisible by six: x is six k. y is divisible by nine: y is nine m.",
            D('Write "x = 6k,  y = 9m"'),
            "k and m are unknown whole numbers. They guarantee nothing.",
            D('Write "x + y = 6k + 9m = 3(2k + 3m)"'),
            "We add — so only the shared factor comes out. Six and nine share a three. Take it out: three times two k plus three m.",
            "Two k plus three m? Unknown. It can be five, or seven. So the only certain number is the three in front.",
            D('Circle choice 4'),
            "Choice four: three.",
            D('Write "x = 6, y = 9 → 15: not by 9, not by 18.   x = 12, y = 9 → 21: not by 15"'),
            "Nothing bigger is certain. Six plus nine is fifteen — not divisible by nine or eighteen. Twelve plus nine is twenty-one — not by fifteen.",
        ]),
        ('The trap · Equal values', [
            "Here's how students fall into choice one.",
            D('Write "x = y = 18 → 36 → divisible by 18?"'),
            "They take one number that fits both: eighteen and eighteen. The sum is thirty-six — divisible by eighteen. Looks certain.",
            "But x and y are different letters. Nothing says they're equal. Equal values hide the trap.",
            D('Write "different letters → different values"'),
            "Plugging in? Give each letter its own value. Better still: tag it, and read the number in front.",
        ]),
    ])
    q = M.q(g)
    for b in M.video('solve-' + g)['beats']:
        if b.get('canvas', '').startswith('Pre-loaded — question'):
            b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (g, q['stem'])

    # --- card row
    M.card('mem-r26-t15-tools')['tables'][0]['rows'].append([
        'Necessarily divisible by…?',
        'Tag it: write each condition as $d\\cdot k$. Multiply → tags multiply; add → only the shared factor; '
        'divide → every factor of the bottom must be in the tags; "by $a$ and by $b$" → the LCM. $k$, $m$ guarantee nothing.',
        '$6k\\cdot10m=60km$; $\\ 6k+10m=2(3k+5m)\\to2$'])


_apply_before_add_methods = apply


def apply(M):
    _apply_before_add_methods(M)
    add_methods(M)   # 2026-10-06: runs last
