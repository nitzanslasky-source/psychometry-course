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


# =====================================================================================
# 2026-10-06 practice: the new exam methods as an extra method in PRACTICE explanations
# (append only; the existing worked solution stays as it is). Runs last.
# =====================================================================================
PRACTICE_METHODS = {
    'q-r26-t15-07': [
        'Method 2 · Tag it, with different letters for different numbers: $a=9k+3$ and $b=9m+7$. Then $a-b=9(k-m)-4=9(k-m-1)+5$, so the remainder is $5$.',
        'With the same letter for both ($9k+3$ and $9k+7$), $a$ would be smaller than $b$. Different numbers need different letters.',
    ],
    'q-453': [
        'Method 2 · Tag it: $a=6k+3$, so $a+2=6k+5$. The tag $6k$ is not always a multiple of $4$ ($6$, $12$, $18$, …), so the remainder by $4$ moves.',
        '$k=0$ gives $5$, remainder $1$. $k=1$ gives $11$, remainder $3$. So it cannot be determined (choice 4).',
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


# =====================================================================================================================
# 2026-10-06 renumber pass: the English course must not look like the Hebrew one. Every Hebrew-derived question
# (guided q-423 ... q-436, practice q-437 ... q-456) gets new numbers (and a changed story where there is one) - same
# idea, same trap, same methods - and every guided solution video is rewritten to match. The Hebrew lesson examples
# (376, 330, 2,745, 417, 765, 3,524, 6,320, 162, 715, 121/132, 4 ÷ 7, the bottle shop, x ÷ 5) get new numbers too.
# Practice clean-up: copies removed, extra warm-ups down to 3, September items kept only where the Hebrew practice
# lacks the type. Nothing in topic 15 is recorded (checked ~/Documents/Course.recordings on 2026-10-06). Runs last.
# =====================================================================================================================
def renumber(M):
    from math_api import rich_plain
    RECORDED = set()

    def S(qid, **kw):
        if qid in RECORDED: return
        q = M.set_q(qid, **kw)
        for v in M.D['videos'].values():   # keep any pre-loaded copy of the choices in sync
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])

    def video(qid, slides):
        if qid in RECORDED: return
        vid = 'solve-' + qid
        for n, x in slides.items():
            title, script = x if isinstance(x, tuple) else (None, x)
            M.set_slide(vid, n, title=title, script=script)
        v = M.video(vid); v['title'] = v['navLabel'] = rich_plain(M.q(qid)['stemRich']).replace('\n', ' ')
        M.touched_videos.add(vid)

    def item(vid, n, k):
        return dict(M.slide(vid, n)['items'][k])

    def intro(qid, line):   # title slide: keep "Question N." (renumbered at build), replace the second spoken line
        if qid in RECORDED: return
        def fn(lines):
            says = [l for l in lines if 'say' in l]; assert len(says) == 2, (qid, says)
            says[1]['say'] = line; return lines
        M.edit_lines('solve-' + qid, 1, fn)

    def lesson_slide(vid, title):
        ns = [k for k, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title]
        assert len(ns) == 1, (vid, title); return ns[0]

    # ================================================================ lesson "Division & Remainder"
    L = 'divisibility'
    n = lesson_slide(L, 'By 2, 5 and 10')
    M.set_slide(L, n, pre=[], script=[
        "Start with the obvious ones — the ones you already know.",
        A("'Divisible by 2: the last digit is even' appears", T('Divisible by $2$: the last digit is even', size=44)),
        A('538 appears', T('$538$', size=60, gap=40)),
        D('Circle the 8'),
        "Five thirty-eight ends in eight. Even. Divisible by two.",
        A("'Divisible by 5: the last digit is 0 or 5' appears", T('Divisible by $5$: the last digit is $0$ or $5$', size=44)),
        A('460 and 3,815 appear', dict(k='row', items=['$460$', '$3{,}815$'], sp=320, below=40)),
        D('Circle the 0 in 460 and the 5 in 3,815'),
        "Four sixty ends in zero. Three thousand eight hundred fifteen ends in five. Both are divisible by five.",
        A("'Divisible by 10: the last digit is 0' appears", T('Divisible by $10$: the last digit is $0$', size=44)),
        "And ten? Ends in zero. That's it.",
    ])
    n = lesson_slide(L, 'By 3 and 9')
    M.set_slide(L, n, pre=[], script=[
        "Now the new ones.",
        A("'Divisible by 3: the digit sum is divisible by 3' appears", T('Divisible by $3$: the digit sum is divisible by $3$', size=44)),
        A('942 appears', T('$942$', size=60, gap=70)),
        D('Under it write "9 + 4 + 2 = 15"'),
        "Add the digits. Nine plus four is thirteen, plus two — fifteen.",
        D('Next to 15 write "÷3 ✓"'),
        "Fifteen is divisible by three — so the whole number, nine forty-two, is divisible by three.",
        A("'Divisible by 9: the digit sum is divisible by 9' appears", T('Divisible by $9$: the digit sum is divisible by $9$', size=44)),
        A('846 appears', T('$846$', size=60, gap=70)),
        D('Under it write "8 + 4 + 6 = 18 ✓"'),
        "Nine — exactly the same idea. Eight plus four is twelve, plus six — eighteen. Eighteen is divisible by nine. So is eight forty-six.",
    ])
    n = lesson_slide(L, 'By 4 and 8')
    M.set_slide(L, n, pre=[], script=[
        "Four and eight are a bit trickier.",
        A("'Divisible by 4: check the last two digits' appears", T('Divisible by $4$: check the last two digits', size=44)),
        A('2,716 appears', T('$2{,}716$', size=60, gap=70)),
        D('Underline the 16'),
        "Look only at the last two digits: sixteen. Sixteen is divisible by four — so the whole number is.",
        D('Under it write "= 2,700 + 16"'),
        "Why? Split it: two thousand seven hundred, plus sixteen. A hundred is divisible by four — so every hundred, every thousand is too.",
        "Only the tens and the ones are left to check.",
        A("'Divisible by 8: check the last three digits' appears", T('Divisible by $8$: check the last three digits', size=44)),
        A('7,240 appears', T('$7{,}240$', size=60, gap=40)),
        D('Underline the 240 and write "7,000 + 240"'),
        "Eight: the same idea with the last three digits. Two-forty is divisible by eight — thirty eights. A thousand is divisible by eight, so the thousands don't matter.",
        "Honestly? Division by eight is rare on the exam. When it shows up, the numbers are friendly — one-sixty, two-forty, five-sixty.",
    ])
    n = lesson_slide(L, 'Build a divisor')
    M.set_slide(L, n, pre=[], script=[
        "Six is a strange bird. It has no sign of its own.",
        A('Divisible by 6: by 2 AND by 3 appears', T('Divisible by $6$: by $2$ AND by $3$', size=44)),
        "But six is two times three. So a number that is divisible by two AND by three is divisible by six.",
        A('234 appears', T('$234$', size=60, gap=50)),
        D('Under it write "even ✓   2 + 3 + 4 = 9 ✓"'),
        "Two thirty-four: even — two ✓. Digit sum nine — three ✓. So it is divisible by six.",
        "Same trick for bigger numbers — with one condition.",
        A('Split into parts with no common factor appears', T('Bigger divisors: split into parts with no common factor', size=42)),
        A('12 = 3·4, 15 = 3·5, 18 = 2·9, 24 = 3·8 appears',
          T('$12=3\\cdot4\\qquad15=3\\cdot5\\qquad18=2\\cdot9\\qquad24=3\\cdot8$', size=46)),
        "Twelve is three times four. Fifteen: three times five. Eighteen: two times nine. Twenty-four: three times eight.",
        A('Trap: 12 = 2·6 appears', T('Trap: $12=2\\cdot6$ ✗', size=46)),
        "Why not two times six? Look at six itself.",
        D('Write "6: ÷2 ✓  ÷6 ✓  but ÷12 ✗"'),
        "Six is divisible by two, and by six — but not by twelve. Two and six share a two, so the check fails.",
        "So the parts must share no factor. Three and four share nothing — that works.",
    ])
    n = lesson_slide(L, 'By 11')
    M.set_slide(L, n, pre=[], script=[
        "Eleven — the hardest one.",
        "Two-digit? No wisdom needed: twenty-two, thirty-three, fifty-five, ninety-nine.",
        A('Alternate + − + − appears', T('Alternate $+\\ -\\ +\\ -$ → a multiple of $11$ ($0$, $11$, $-11$)', size=42)),
        "Longer numbers: go digit by digit — plus, minus, plus, minus.",
        A('836 appears', T('$836$:  $8-3+6=11$ ✓', size=50)),
        "Eight thirty-six: eight, minus three, plus six — eleven. So it is divisible by eleven.",
        "For three digits, that's just the outer digits minus the middle one.",
        A('1,331 appears', T('$1{,}331$:  $1-3+3-1=0$ ✓', size=50)),
        "Four digits, same idea. One thousand three hundred thirty-one: one, minus three, plus three, minus one — zero.",
        "Zero counts. Zero is divisible by eleven — so the number is.",
        A('482 appears', T('$482$:  $4-8+2=-2$ ✗', size=50)),
        "Four eighty-two: four, minus eight, plus two — minus two.",
        "A negative result is fine to get. But minus two isn't zero, eleven or minus eleven. So four eighty-two isn't divisible by eleven.",
        "Most exam numbers are simple — one forty-three, one sixty-five. But be ready.",
    ])
    n = lesson_slide(L, 'The remainder trap')
    M.set_slide(L, n, pre=[], script=[
        "Here's where students go wrong.",
        A('5 ÷ 8 appears', T('$5\\div8$', size=60, gap=40)),
        "What's the remainder of five divided by eight?",
        D('Next to it write "r = 5" (not 3!)'),
        "Five. NOT three. It's not the difference between them.",
        "Picture a bakery. Every sandwich costs eight shekels.",
        A("'35 shekels, sandwiches cost 8' appears", T('$35$ shekels · sandwiches cost $8$', size=46, gap=40)),
        D('Write "8, 16, 24, 32 → 3 left"'),
        "Thirty-five shekels: eight, sixteen, twenty-four, thirty-two — four sandwiches. Three shekels stay in your hand. That's the remainder.",
        A("'5 shekels, sandwiches cost 8' appears", T('$5$ shekels · sandwiches cost $8$', size=46, gap=40)),
        D('Write "0 sandwiches → 5 left"'),
        "Now walk in with five shekels. Not enough for a single sandwich. Zero sandwiches — and five shekels still in your hand.",
        "The remainder is what's left in your hand after buying as many as you can.",
    ])
    n = lesson_slide(L, 'Biggest remainder')
    M.set_slide(L, n, pre=[], script=[
        "What's the remainder of x divided by four? We don't know x — so let's try.",
        A('A row of x values appears: 1 to 6', dict(k='row', items=['$1$', '$2$', '$3$', '$4$', '$5$', '$6$'], sp=150, below=100)),
        D('Under each write its remainder when divided by 4: 1, 2, 3, 0, 1, 2'),
        "One shekel, a four-shekel drink: remainder one. Two: two. Three: three.",
        "Four? Divides exactly — no remainder. Five? Back to one. Six: two.",
        A("'Biggest remainder = divisor − 1' appears", T('Biggest remainder $=$ divisor $-\\ 1$', size=48)),
        "So the biggest remainder is always one less than what you divide by. One more — and it divides again.",
        "Divide by twelve? The biggest remainder is eleven.",
    ])
    n = lesson_slide(L, 'Change the divisor')
    M.set_slide(L, n, pre=[], script=[
        "What if the question changes the divisor?",
        A('x leaves 4 when divided by 15. By 5? appears', T('$x$ leaves $4$ when divided by $15$. By $5$?', size=44)),
        D('Write "x = 15k + 4 = 5 · 3k + 4 → r4"'),
        "x is fifteen k plus four. Fifteen k is five times three k — full fives. So x divided by five leaves four.",
        A('x leaves 13 when divided by 15. By 5? appears', T('$x$ leaves $13$ when divided by $15$. By $5$?', size=44)),
        D('Write "13 = 10 + 3 → r3"'),
        "If the old remainder is too big, divide it again. Thirteen divided by five leaves three.",
        A('x leaves 2 when divided by 8. By 6? appears', T('$x$ leaves $2$ when divided by $8$. By $6$?', size=44)),
        D('Write "x = 2 → r2,   x = 10 → r4   → can\'t know"'),
        "By six? Try: two leaves two. Ten leaves four. Two different answers — you can't know.",
        A('Only if the new divisor divides the old one appears', T('Works only if the new divisor divides the old one', size=42)),
        "The rule: five divides fifteen, so it works. Six doesn't divide eight — so it doesn't.",
    ])
    for b in M.video(L)['beats']: b['loads'] = ''   # canvas descriptions are rebuilt from the new items

    c = M.card('mem-divisibility')
    c['tables'][0]['rows'] = [
        ['$2$', 'last digit is even', '$538$'],
        ['$5$', 'last digit is $0$ or $5$', '$460$, $3{,}815$'],
        ['$10$', 'last digit is $0$', '$460$'],
        ['$3$', 'digit sum is divisible by $3$', '$942 \\to 15$'],
        ['$9$', 'digit sum is divisible by $9$', '$846 \\to 18$'],
        ['$4$', 'last two digits are divisible by $4$', '$2{,}716 \\to 16$'],
        ['$8$', 'last three digits are divisible by $8$', '$7{,}240 \\to 240$'],
        ['$6$', 'divisible by $2$ AND by $3$', '$234$'],
        ['$12$, $15$, $18$, $24$', 'split into parts with no common factor: $3\\cdot4$, $3\\cdot5$, $2\\cdot9$, $3\\cdot8$',
         'NOT $12=2\\cdot6$: $6$ is divisible by $2$ and by $6$, but not by $12$'],
        ['$11$', 'alternate $+\\,-\\,+\\,-$; the result is $0$ or $\\pm11$', '$836$: $8-3+6=11$; $1{,}331$: $1-3+3-1=0$'],
    ]
    rows = c['tables'][1]['rows']
    for r in rows:
        if r[0] == '$0 \\le r < d$': r[1] = '$5\\div8$ leaves $5$ (not $3$)'
        if r[0] == 'Biggest remainder $= d - 1$': r[1] = 'dividing by $4$: at most $3$'
        if r[0].startswith('New divisor'): r[1] = 'leaves $13$ by $15$ → leaves $3$ by $5$; by $8$ → by $6$: unknown'
    c['tables'][2]['rows'] = [['A fraction of a fraction', 'build from the inside and multiply the denominators',
                               '$\\frac12$ of $\\frac17$: $k\\to7k\\to14k$; $\\frac12$ of $\\frac14$: divisible by $8$']]

    # ---- "More Remainder Tools": the units-digit example was the old q-433 (12a, a = 286)
    def tools_fix(lines):
        for l in lines:
            if l.get('draw', '').startswith('Write "12 · 286'): l['draw'] = 'Write "16 · 327 → 6 · 7 = 42 → ends in 2"'
            if l.get('say', '').startswith('Twelve times two eighty-six'):
                l['say'] = "Sixteen times three twenty-seven. You don't need the full product. Six times seven is forty-two — so it ends in two."
        return lines
    M.edit_lines(TOOLS, lesson_slide(TOOLS, 'Units digit'), tools_fix)
    assert not M.find_text('286', [TOPIC]) or all(x[1] != TOOLS for x in M.find_text('286', [TOPIC]))
    tc = M.card('mem-r26-t15-tools')
    for r in tc['tables'][0]['rows']:
        if r[0] == 'How many multiples of $d$?':
            r[2] = 'three-digit multiples of $16$: $112=16\\cdot7$ to $992=16\\cdot62$ → $56$'
    tc['tips'] = [t.replace('$A(A+4)(A+8)$ with $A=2$ gives $120$', '$A(A+4)(A+20)$ with $A=2$ gives $264$') for t in tc['tips']]
    assert any('264' in t for t in tc['tips'])

    # ================================================================ guided questions 1-4 (Remainder Questions)
    # q-423: chess girls 1/3, piano 1/4 of those -> 12k; now basketball boys 1/5, guitar 1/3 of those -> 15k
    S('q-423', stem='In Daniel\'s class, $\\frac{1}{5}$ of the students are boys who play basketball, and among those, $\\frac{1}{3}$ also play the guitar. What could be the number of students in the class?',
      choices=['$35$', '$45$', '$42$', '$32$'], correct=2, expl=[
        'A fifth of the class are basketball boys, so the class is divisible by 5. A third of the basketball boys play the guitar, so the basketball group is divisible by 3.',
        'Build it from the inside: guitar players $k$, basketball boys $3k$, the class $5\\cdot3k=15k$. The class is divisible by 15.',
        'Only $45=15\\cdot3$ works: $45\\div5=9$ and $9\\div3=3$ ✓.',
        '$35\\div5=7$, but 7 is not divisible by 3. 42 and 32 are not divisible by 5.'])
    rule = item('solve-q-423', 3, 1); rule['t'] = 'A fraction of a fraction $\\to$ multiply the denominators: $5\\cdot3=15$'
    video('q-423', {
        2: ['"What COULD be the number?" We can\'t know it exactly. So we eliminate what it can\'t be.',
            "A fifth of the class are basketball boys. There's no such thing as a fifth of a kid — so the class is divisible by five.",
            D('Next to each choice write "÷5": 35 ✓, 45 ✓, 42 ✗, 32 ✗'),
            "Thirty-five ends in five ✓. Forty-five ends in five ✓. Forty-two and thirty-two don't ✗.",
            D('Cross out choices 3 and 4'),
            "And a third of those play the guitar. So the basketball group is divisible by three — together, the class is divisible by fifteen.",
            D('Write "35 ÷ 5 = 7 → 7 ÷ 3 ✗"'),
            "Thirty-five gives seven basketball boys. A third of seven? Doesn't exist.",
            D('Write "45 ÷ 5 = 9 → 9 ÷ 3 = 3 ✓" and circle choice 2'),
            "Forty-five gives nine — and a third of nine is three. Choice two."],
        3: ["Quick check from the inside out.",
            D('Write "k → 3k → 15k"'),
            "Call the guitar players k. The basketball boys are three k. The class is five times that — fifteen k.",
            A("'A fraction of a fraction → multiply the denominators' appears", rule),
            "The rule: a fraction of a fraction — multiply the denominators. Half of a quarter? It must be divisible by eight, not just by four.",
            D('Circle choice 2'),
            "A multiple of fifteen. Only forty-five. Choice two."]})

    # q-424: rows of 4 -> 3 left, rows of 5 -> 2 left (27); now rows of 5 -> 4 left, rows of 3 -> 1 left (34)
    S('q-424', stem='Tamar is putting her stamps into an album. If she arranges them in rows of 5 with an equal number in each row, 4 stamps are left over. If she arranges them in rows of 3 with an equal number in each row, 1 stamp is left over. What could be the number of stamps Tamar has?',
      choices=['$28$', '$40$', '$34$', '$16$'], correct=3, expl=[
        'We need a number that leaves remainder 4 when divided by 5 and remainder 1 when divided by 3. Test the choices.',
        '$28=5\\cdot5+3$: remainder 3, not 4 ✗. $40=5\\cdot8$: remainder 0 ✗.',
        '$34=5\\cdot6+4$ ✓ and $34=3\\cdot11+1$ ✓. Both conditions hold.',
        '$16=5\\cdot3+1$ ✗.'])
    video('q-424', {
        2: ['"What could it be?" — so we test the answers.',
            "We need: divided by five, remainder four. Divided by three, remainder one.",
            D('Next to choice 1 write "28 ÷ 5 = 5 r3 ✗"'),
            "Twenty-eight: five fits five times, up to twenty-five. Remainder three. Not four — out.",
            D('Cross out choice 1'),
            D('Next to choice 2 write "40 ÷ 5 = 8 r0 ✗"'),
            "Forty: five fits exactly eight times. No remainder at all — out.",
            D('Cross out choice 2'),
            D('Next to choice 3 write "34 ÷ 5 = 6 r4 ✓"'),
            "Thirty-four: six fives are thirty. Remainder four ✓.",
            D('Next to it write "34 ÷ 3 = 11 r1 ✓"'),
            "Now the second condition. Eleven threes are thirty-three. Remainder one ✓.",
            D('Circle choice 3'),
            "Both fit — mark it and move on. There's only one correct answer, so no need to check the rest. Choice three."],
        3: ["Another way: list the numbers that leave one when divided by three.",
            D('Write "1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, …"'),
            "One, four, seven, ten, thirteen, sixteen… a hop of three each time.",
            D('Circle 16, 28, 34 and 40 in the list'),
            "Sixteen, twenty-eight, thirty-four, forty are all on it. So test them against the five.",
            D('Circle choice 3'),
            "Only thirty-four leaves four when divided by five. Choice three."]})

    # q-425: remainders by 7 and by 4 -> 6 · 3 = 18 (trap 28); now by 8 and by 3 -> 7 · 2 = 14 (trap 24)
    S('q-425', stem='$a$ and $b$ are positive integers. $x$ is the remainder when $a$ is divided by 8, and $y$ is the remainder when $b$ is divided by 3. What is the greatest possible value of $x\\cdot y$?',
      choices=['$7$', '$2$', '$14$', '$24$'], correct=3, expl=[
        'The biggest remainder is one less than the divisor: $x\\le8-1=7$ and $y\\le3-1=2$.',
        'Both are possible, for example $a=7$ and $b=2$. So the greatest value is $7\\cdot2=14$.',
        '24 is the trap: $8\\cdot3$. A remainder is always smaller than the divisor.'])
    video('q-425', {
        2: ["x is the remainder of a divided by eight. y is the remainder of b divided by three.",
            "We want x times y as big as possible — so each one as big as possible.",
            D('Write "max x = 8 − 1 = 7"'),
            "Dividing by eight, the biggest remainder is seven. Eight would already divide again.",
            D('Write "max y = 3 − 1 = 2"'),
            "Dividing by three, the biggest remainder is two.",
            D('Write "7 · 2 = 14" and circle choice 3'),
            "Seven times two: fourteen. Choice three.",
            "Twenty-four is the trap — that's eight times three, the divisors themselves. A remainder never reaches the divisor."]})

    # q-426: remainder 1 by 3 -> (3x + 4)²; now remainder 4 by 5 -> (5x + 2)²
    S('q-426', stem='A number leaves a remainder of 4 when divided by 5. Which of the following expressions could represent the number ($x$ is an integer)?',
      choices=['$5x+7$', '$(5x+2)^2$', '$10x+8$', '$(5x+5)^2$'], correct=2, expl=[
        'A multiple of 5 plus a number: only that number decides the remainder.',
        '(1) $5x+7=5(x+1)+2$, so the remainder is 2 ✗.',
        '(2) $(5x+2)^2=25x^2+20x+4=5(5x^2+4x)+4$, so the remainder is 4 ✓.',
        '(3) $10x+8=5(2x+1)+3$, so the remainder is 3 ✗.',
        '(4) $(5x+5)^2=25(x+1)^2$, so the remainder is 0 ✗.',
        'Faster: plug in $x=0$: $7$, $4$, $8$, $25$ leave $2$, $4$, $3$, $0$. Here $x=0$ is safe, because each expression leaves the same remainder for every $x$.'])
    video('q-426', {
        2: ["Remainder four when divided by five — call it five x plus four. But the choices are written differently. So check each.",
            D('Next to choice 1 write "5x ✓, 7 → r2 ✗"'),
            "Five x plus seven: five x is always divisible by five. Seven leaves two. Out.",
            D('Next to choice 2 write "= 25x² + 20x + 4"'),
            "Five x plus two, squared — open the formula: twenty-five x squared, plus twenty x, plus four.",
            D('Underline 25x² and 20x; write "4 → r4 ✓"'),
            "Twenty-five x squared and twenty x are both divisible by five. Four leaves four ✓.",
            "Shortcut: the five x part already divides — so everything built from it divides too. Just check two squared.",
            D('Next to choice 3 write "10x ✓, 8 → r3 ✗"'),
            "Ten x plus eight: ten x is divisible by five. Eight leaves three. Out.",
            D('Next to choice 4 write "5² = 25 → r0 ✗"'),
            "Choice four — five squared is twenty-five. No remainder. Out.",
            D('Circle choice 2'),
            "Choice two."],
        3: ["Even faster: x is any whole number — so plug one in. Zero is the most convenient.",
            D('Next to the choices write "x = 0: 7, 4, 8, 25"'),
            "Seven, four, eight, twenty-five.",
            D('Write their remainders: r2, r4, r3, r0'),
            "Divided by five: two, four, three, zero.",
            D('Circle choice 2'),
            "Only four leaves four. Choice two. For this type, plugging in is usually the quickest route.",
            "And here zero is safe: each choice leaves the same remainder for every x.",
            "In a \"necessarily divisible\" question it's different — zero is divisible by everything, so never plug in a value that gives zero."]})

    # ================================================================ advanced guided questions
    # q-427: 60% French -> 3k (480); now 30% tennis -> 3k (540)
    S('q-427', stem='$30\\%$ of the members of a sports club play tennis. Which of the following numbers could be the number of members who play tennis?',
      choices=['$530$', '$540$', '$550$', '$560$'], correct=2, expl=[
        '$30\\%=\\frac{30}{100}=\\frac{3}{10}$. Build it from the inside: the club has $10k$ members, and $3k$ of them play tennis.',
        'So the number of tennis players is divisible by 3. Digit sums: $530\\to8$ ✗, $540\\to9$ ✓, $550\\to10$ ✗, $560\\to11$ ✗.',
        'Only 540 (for example, a club of 1,800 members).'])
    video('q-427', {
        2: ("Percent → fraction → divisible by 3", [
            "This is a divisibility story. First, turn the percentage into a fraction.",
            D('Next to the question write "30% = 30/100 = 3/10"'),
            "Thirty percent is thirty over a hundred — three tenths.",
            "Build it from the inside, like the basketball class. Call a tenth of the club k.",
            D('Write "club = 10k → tennis = 3k"'),
            "The club has ten k members. Three k of them play tennis. So the number of tennis players must be divisible by three.",
            "How do we test for three? The digit sum must be divisible by three.",
            D('Next to the choices write the digit sums: 8, 9, 10, 11'),
            "Five thirty: eight — no.",
            "Five forty: nine — nine is divisible by three.",
            D('Circle choice 2'),
            "Choice two. In the exam, circle it and move on. Five fifty and five sixty? Ten and eleven — out anyway."])})

    # q-428: 85X, 15 shekels (by 2 and by 3) -> X = 2, 8; now 61X, 12 tokens -> X = 2, 8 (612, 618)
    S('q-428', stem='A game machine shows a three-digit number. Its hundreds digit is 6, its tens digit is 1, and its units digit is $X$.\nThe machine pays:\n4 tokens if the number is divisible by 2 but not by 3;\n8 tokens if it is divisible by 3 but not by 2;\n12 tokens if it is divisible by both 2 and 3.\nNoa played once and won 12 tokens. How many different values can $X$ have?',
      choices=['$3$', '$1$', '$2$', '$0$'], correct=3, expl=[
        '12 tokens means the number is divisible by 2 and by 3.',
        'By 3: the digit sum $6+1+X=7+X$ is divisible by 3, so $X=2$, $5$ or $8$.',
        'By 2: $X$ is even, so $X=2$ or $X=8$ (612 and 618). Two values.'])
    video('q-428', {
        2: ["Noa won twelve tokens. What does twelve mean? Divisible by two AND by three.",
            "Start with three: the digit sum must be divisible by three.",
            D('Write "6 + 1 = 7"'),
            "Six plus one is seven. Together with X, we need a multiple of three.",
            "The first multiple of three above seven is nine — so X can be two.",
            D('Write "612" and tick it'),
            "Six one two: divisible by three — and it's even, so it is divisible by two. That fits.",
            "Next multiple of three? Just add three: six one five.",
            D('Write "615" and cross it out'),
            "Divisible by three — but it ends in five. Odd. Not divisible by two. Out.",
            "Add three again: six one eight.",
            D('Write "618" and tick it'),
            "Even, and divisible by three. That fits too.",
            "Two values: two and eight.",
            D('Circle choice 3'),
            "Choice three."]})

    intro('q-428', "A game machine — and a digit we have to find.")

    # q-429: not divisible by 12 (3,224); new numbers, answer 3,152
    S('q-429', stem='Which of the following numbers is not divisible by 12?',
      choices=['$1{,}428$', '$3{,}152$', '$5{,}172$', '$2{,}316$'], correct=2, expl=[
        '$12=3\\cdot4$, and 3 and 4 have no common factor. So check 4 (last two digits) and 3 (digit sum). Not $2\\cdot6$: 6 is divisible by 2 and by 6, but not by 12.',
        'Last two digits: 28, 52, 72 and 16 are all divisible by 4.',
        'Digit sums: $1{,}428\\to15$ ✓, $3{,}152\\to11$ ✗, $5{,}172\\to15$ ✓, $2{,}316\\to12$ ✓.',
        'Only $3{,}152$ is not divisible by 3, so it is not divisible by 12.'])
    video('q-429', {
        2: ["If they asked about three or four, this would be easy — we have a sign for each.",
            "There's no sign for twelve. Option one: long-divide every choice. Slow.",
            "Option two — the one the question wants: build twelve from signs we know. Remember six? Two and three.",
            "Try twelve as two times six.",
            D('Write "2 · 6 ?"'),
            "But is every number divisible by two and by six divisible by twelve? Six is. Eighteen is. Thirty is. None of them are divisible by twelve.",
            D('Cross out "2 · 6"'),
            "It fails because six already contains a two. The two parts must not share a prime factor.",
            D('Write "3 · 4 ✓"'),
            "Three and four share nothing. Divisible by three AND four means divisible by twelve.",
            "Four first: look at the last two digits. Twenty-eight, fifty-two, seventy-two, sixteen — all are divisible by four.",
            D('Next to the choices write the digit sums: 15, 11, 15, 12'),
            "Now three: digit sums. Fifteen — yes. Eleven — no!",
            D('Circle choice 2'),
            "Three thousand one hundred fifty-two is divisible by four — but not by three. Not by twelve. Choice two.",
            "In the lesson, check the other two: digit sums fifteen and twelve — both divisible by three. So those two are divisible by twelve.",
            "Same trick for fifteen: check five and three."]})

    # q-430: 10 vs 11, 12 vs 14 (both right); now 15 vs 17, 18 vs 20 (both right, as in the Hebrew)
    S('q-430', stem='Yoav claims: "There are more three-digit numbers divisible by both 3 and 5 than three-digit numbers divisible by 17."\nMichal claims: "There are more three-digit numbers divisible by both 2 and 9 than three-digit numbers divisible by both 4 and 5."\nWhich of the following is correct?',
      choices=['Only Yoav is right.', 'Only Michal is right.', 'Both are right.', 'Both are wrong.'], correct=3, expl=[
        'Count the multiples: write the first and the last as $d\\cdot k$, then count $=$ last $k-$ first $k+1$.',
        'By 3 and 5, that is by 15: from $105=15\\cdot7$ to $990=15\\cdot66$, so $66-7+1=60$ numbers. By 17: from $102=17\\cdot6$ to $986=17\\cdot58$, so $58-6+1=53$. Since $60>53$, Yoav is right.',
        'By 2 and 9, that is by 18: from $108=18\\cdot6$ to $990=18\\cdot55$, so $55-6+1=50$. By 4 and 5, that is by 20: from $100=20\\cdot5$ to $980=20\\cdot49$, so $49-5+1=45$. Since $50>45$, Michal is right too.',
        'Both are right.'])
    cnt = item('solve-q-430', 2, 1)
    video('q-430', {
        2: ["Two claims about how many numbers are divisible by something. Let's count — first and last multiple.",
            "Yoav first. Divisible by both three and five: they have no common factor, so that's divisible by fifteen.",
            D('Under Yoav write "15: 105 = 15·7 … 990 = 15·66 → 66 − 7 + 1 = 60"'),
            "The first three-digit multiple of fifteen is fifteen times seven. The last is fifteen times sixty-six. Sixty-six minus seven, plus one: sixty.",
            A("'Count = last k − first k + 1' appears", cnt),
            "Don't forget the plus one — both ends count. From three to seven there are five numbers, not four.",
            D('Write "17: 102 = 17·6 … 986 = 17·58 → 58 − 6 + 1 = 53"'),
            "Seventeen: from seventeen times six to seventeen times fifty-eight. Fifty-three.",
            "Sixty beats fifty-three. Yoav is right.",
            D('Cross out choices 2 and 4'),
            "Michal. Two and nine — no common factor — so divisible by eighteen. Four and five — divisible by twenty.",
            D('Under Michal write "18: 108 = 18·6 … 990 = 18·55 → 55 − 6 + 1 = 50"'),
            "Eighteen: from eighteen times six to eighteen times fifty-five. Fifty-five minus six, plus one: fifty.",
            D('Write "20: 100 = 20·5 … 980 = 20·49 → 49 − 5 + 1 = 45"'),
            "Twenty: from twenty times five to twenty times forty-nine. Forty-five.",
            "Fifty beats forty-five. Michal is right too.",
            D('Circle choice 3'),
            "Both are right. Choice three."],
        3: ["On the exam, there's a faster way to compare.",
            D('Write "1/15 > 1/17    1/18 > 1/20"'),
            "Every fifteenth number is divisible by fifteen. Every seventeenth is divisible by seventeen. One fifteenth is more than one seventeenth.",
            "Same for Michal: one eighteenth beats one twentieth.",
            "The smaller the number, the more numbers are divisible by it.",
            "But be careful: this works here because the range is long — nine hundred numbers. In a short range the estimate can be off by one. Then count exactly."]})

    # q-431: c = 5a, a = b/3 (5, 3, 9; 16 fails); now c = 4a, a = b/5 (4, 5, 10; 12 fails)
    S('q-431', stem='Given:\n$\\begin{cases} c=4a \\\\ a=\\frac{b}{5} \\end{cases}$\n$a$, $b$ and $c$ are positive integers. Which claim is not necessarily true?',
      choices=['$c$ is divisible by $4$', '$b$ is divisible by $5$', '$a+b$ is divisible by $12$', '$a+b+c$ is divisible by $10$'], correct=3, expl=[
        'Write everything with $a$: $b=5a$ and $c=4a$.',
        '$c=4a$ is divisible by 4 ✓. $b=5a$ is divisible by 5 ✓. $a+b+c=a+5a+4a=10a$ is divisible by 10 ✓.',
        '$a+b=6a$. For $a=1$: $a+b=6$, which is not divisible by 12. So claim (3) is not necessarily true.'])
    video('q-431', {
        2: ["Claim one: c is divisible by four. c equals four times a — four is one of its factors. Always true.",
            D('Cross out choice 1'),
            "Claim two: a equals b over five. b divided by five gives a positive integer — so b is divisible by five.",
            D('Write "b = 5a" and cross out choice 2'),
            "Multiply by five and you see it: b is five times a.",
            "Claim three: write the sum with one letter only.",
            D('Write "a + b = a + 5a = 6a"'),
            "a plus five a — six a. Always divisible by six — but twelve? Not necessarily.",
            "Claim four, to be sure: all three letters.",
            D('Write "a + 5a + 4a = 10a" and cross out choice 4'),
            "a plus five a plus four a — ten a. Always divisible by ten.",
            D('Circle choice 3'),
            "Choice three."],
        3: ["Now the psychometric way: plug in numbers. Start with the tricky one.",
            "b over five must be whole — so b must be divisible by five. Take b equals five.",
            D('Write "b = 5 → a = 1 → c = 4"'),
            "Then a is one, and c is four times one — four.",
            D('Next to the choices write: 4 ✓, 5 ✓, 6 ✗, 10 ✓'),
            "c is divisible by four — yes. b by five — yes. a plus b is six — not by twelve. The sum of all three is ten — divisible by ten.",
            D('Circle choice 3'),
            "Choice three. Here plugging in is perfect: we look for the claim that can fail, and one example where it fails is proof.",
            "The three claims that worked with b equals five? One example doesn't prove them — the algebra does."]})

    # q-432: 3a³ − 3a -> 18; now 5a³ − 5a -> 30
    S('q-432', stem='Given: $x=5a^3-5a$ ($a$ is a positive integer). $x$ is necessarily divisible by:',
      choices=['$60$', '$40$', '$30$', '$20$'], correct=3, expl=[
        'Factor: $x=5a(a^2-1)=5(a-1)a(a+1)$.',
        '$(a-1)a(a+1)$ is three numbers in a row, so it is divisible by 6. Therefore $x$ is divisible by $5\\cdot6=30$.',
        'Check with $a=2$: $x=5\\cdot8-5\\cdot2=30$. It is not divisible by 60, 40 or 20, so only 30 is certain.'])
    video('q-432', {
        2: ["Take out the common factor: five a.",
            D('Write "x = 5a(a² − 1)"'),
            "a squared minus one — that's the third contracted multiplication formula.",
            D('Write "= 5(a − 1)a(a + 1)"'),
            "Reorder it: a minus one, a, a plus one. Three consecutive integers!",
            D('Underline (a − 1)a(a + 1)'),
            "Three numbers in a row: one is divisible by three, and at least one is even. So the product is divisible by six.",
            D('Write "5 · 6 = 30"'),
            "Times the five in front — x is always divisible by thirty.",
            D('Circle choice 3'),
            "Choice three."],
        3: ["Plug-in version. Careful — don't plug in one.",
            "a equals one gives zero. Zero is divisible by everything — no answer can be eliminated.",
            D('Write "a = 2: x = 5·8 − 5·2 = 30"'),
            "So take a equals two. Five times eight is forty, minus ten — thirty.",
            D('Next to the choices write: ✗, ✗, ✓, ✗'),
            "Divisible by sixty? No. Forty? No. Thirty? Yes. Twenty? No.",
            D('Circle choice 3'),
            "Only choice three survives — so it must be the answer.",
            "If two choices had survived, we'd try a second value, like a equals three."]})

    # q-433: 12a + 8 divisible by 10 -> a = 286; now 14a + 6 -> a = 346
    S('q-433', stem='Given: $x=14a+6$ ($a$ is a positive integer), and $x$ is divisible by 10. Which of the following could be the value of $a$?',
      choices=['$343$', '$344$', '$345$', '$346$'], correct=4, expl=[
        '$x$ is divisible by 10, so $x$ ends in 0. Since $x=14a+6$, $14a$ ends in 4.',
        'The units digit of $14a$ depends only on $4\\cdot$(the units digit of $a$): $4\\cdot3=12$, $4\\cdot4=16$, $4\\cdot5=20$, $4\\cdot6=24$ ✓.',
        'So $a=346$. Check: $14\\cdot346+6=4{,}844+6=4{,}850$ ✓.'])
    video('q-433', {
        2: ["x is divisible by ten with no remainder. So x must end in zero.",
            D('Write "x ends in 0"'),
            "Now the equation: fourteen a plus six. Some product, plus six, must end in zero.",
            "So fourteen a must end in four — four plus six is ten.",
            D('Write "14a ends in 4"'),
            "Now test the choices — and only the units digits matter: four times a's last digit.",
            D('Next to the choices write: 4·3 = 12 ✗, 4·4 = 16 ✗, 4·5 = 20 ✗, 4·6 = 24 ✓'),
            "Three forty-three: four times three ends in two — add six, x ends in eight. Out.",
            "Three forty-four: four times four ends in six — plus six, x ends in two. Out.",
            "Three forty-five: four times five ends in zero — plus six, x ends in six. Out.",
            "Three forty-six: four times six ends in four — plus six, zero. That works!",
            D('Circle choice 4'),
            "Choice four.",
            "Check: fourteen times three forty-six plus six is four thousand eight hundred fifty. Ends in zero."]})

    # q-434: casino, 500 tokens, lost x, 2x, 3x -> 20 left; now amusement-park card, 700 points -> 40 left
    S('q-434', stem='Yael loaded 700 points onto an amusement-park card. The first ride cost $x$ points, the second ride cost $2x$ points, and the third ride cost $3x$ points. Which of the following could be the number of points left on her card after the three rides?',
      choices=['$25$', '$40$', '$20$', '$50$'], correct=2, expl=[
        'She paid $x+2x+3x=6x$ points, so the number of points she paid is divisible by 6 (by 2 and by 3).',
        'For each choice, find what she paid: $700-25=675$ (digit sum 18, but odd ✗), $700-40=660$ (even ✓, digit sum 12 ✓), $700-20=680$ (digit sum 14 ✗), $700-50=650$ (digit sum 11 ✗).',
        'So 40 points are left, and $x=660\\div6=110$.'])
    video('q-434', {
        2: ("Build the expression, then test", [
            "Write what's left as an expression.",
            D('Write "paid: x + 2x + 3x = 6x"'),
            "She paid x, then two x, then three x — six x in total. Left: seven hundred minus six x.",
            "Could that be twenty-five? Seven hundred minus twenty-five is six seventy-five — that must equal six x.",
            "x is a whole number of points, so six seventy-five must be divisible by six.",
            "Divisible by six means divisible by two AND three.",
            D('Next to choice 1 write "675: sum 18 ✓, odd ✗"'),
            "Digit sum eighteen — three is fine. But it's odd — not divisible by two. Out. That's the trap: checking only the three.",
            "Faster: for each choice, just ask how much she PAID — complete it to seven hundred.",
            D('Next to choice 2 write "660: even ✓, sum 12 ✓"'),
            "Forty left means she paid six sixty. Even, digit sum twelve — divisible by six. x is one hundred ten.",
            D('Circle choice 2'),
            "Choice two. In the lesson: twenty left means six eighty paid — digit sum fourteen. Fifty left means six fifty — digit sum eleven. Both out."])})

    intro('q-434', "An amusement park, points on a card — and a divisibility test.")

    # q-435: x leaves 3 by 6; 2x by 6, x by 3, x by 9 -> only Gal wrong; now x leaves 4 by 8; 2x by 8, x by 4, x by 12
    S('q-435', stem='When $x$ is divided by 8, the remainder is 4.\nYuval claims: "$2x$ is necessarily divisible by 8."\nNoga claims: "$x$ is necessarily divisible by 4."\nItay claims: "$x$ is necessarily divisible by 12."\nWhich of the following is correct?',
      choices=['Only Yuval is right.', 'Only Itay is wrong.', 'All three are right.', 'All three are wrong.'], correct=2, expl=[
        'Write $x=8k+4$.',
        'Yuval: $2x=16k+8=8(2k+1)$ is divisible by 8 ✓.',
        'Noga: $x=8k+4=4(2k+1)$ is divisible by 4 ✓. (4 divides 8, so a remainder by 8 also gives the remainder by 4.)',
        'Itay: $k=0$ gives $x=4$, which is not divisible by 12 ✗. (12 does not divide 8, so a remainder by 8 says nothing about 12.)',
        'Only Itay is wrong.'])
    video('q-435', {
        2: ["Write the given as an expression: x equals eight k plus four.",
            D('Write "x = 8k + 4"'),
            "Eight times some whole number, plus the remainder four.",
            "Yuval: two x is divisible by eight?",
            D('Write "2x = 16k + 8"'),
            "Sixteen k is divisible by eight, eight is divisible by eight. No remainder — Yuval is right.",
            "Faster with understanding: the question and the claim both talk about eight. So only look at the remainder: four times two is eight. Divisible by eight.",
            "Noga: x is divisible by four? Four is contained in eight — whatever is divisible by eight is divisible by four. So only check the remainder: four over four, no remainder. Noga is right.",
            "Itay: x is divisible by twelve? Twelve does NOT divide eight. From a remainder by eight, you can't know the remainder by twelve.",
            D('Write "k = 0 → x = 4"'),
            "Proof: k zero gives x equals four. Four isn't divisible by twelve. Itay is wrong.",
            D('Circle choice 2'),
            "Only Itay is wrong — choice two."],
        3: ["Plugging in works — but remember what it can prove.",
            "Two numbers with remainder four when divided by eight: twelve, and four.",
            D('Write "x = 12, x = 4"'),
            "Yuval: twenty-four and eight — both are divisible by eight. Probably right.",
            "Noga: twelve and four — both are divisible by four. Probably right.",
            "Itay: twelve is divisible by twelve… but four isn't. Itay is wrong.",
            D('Circle choice 2'),
            "Choice two. The example x equals four proves Itay wrong.",
            "For Yuval and Noga, two examples that work are not proof. Method one proves them."]})

    # q-436: sum of three integers divisible by 3 (Hebrew: 1+4+7, 6+4+2); still by 3, new numbers and claim order
    S('q-436', stem='The sum of three integers is divisible by 3. Which of the following statements is not necessarily true?',
      choices=['When one of the numbers is divided by $3$, the greatest possible remainder is $2$.',
               'If one of the numbers is divisible by $3$, then the other two are too.',
               'All three numbers can leave remainder $2$ when divided by $3$.',
               'If two of the numbers are divisible by $3$, then the third is too.'], correct=2, expl=[
        'Think in remainders: the remainders of the three numbers must add up to a multiple of 3.',
        '(1) True: dividing by 3, the remainder is 0, 1 or 2.',
        '(2) Not necessarily: $9+5+7=21$. 9 is divisible by 3, but 5 and 7 are not.',
        '(3) Possible: $5+8+11=24$, and each number leaves remainder 2.',
        '(4) True: two numbers leave 0 and the sum leaves 0, so the third leaves 0.'])
    video('q-436', {
        2: ["When you add numbers, you can just add their remainders.",
            "Claim one: the largest remainder when dividing by three is two. Always true — the largest remainder is one less than the divisor.",
            D('Cross out choice 1'),
            "Three leaves zero, four leaves one, five leaves two, six leaves zero again. A remainder of three? Then three would fit in again.",
            "Claim two: one of them is divisible by three — so the other two must be too?",
            D('Next to choice 2 write "9 + 5 + 7 = 21"'),
            "Nine, five, seven. The sum is twenty-one — divisible by three. Nine is divisible by three — but five and seven aren't. Their remainders, two and one, add up to three.",
            D('Circle choice 2'),
            "That claim can fail — choice two. In the exam, mark it and move on. In the lesson, let's check the other two.",
            "Claim three: all three leave remainder two? Two plus two plus two is six — divisible by three. Possible.",
            D('Next to choice 3 write "5 + 8 + 11 = 24 ✓"'),
            "Five, eight, eleven — each leaves remainder two — sum twenty-four.",
            "Claim four: two of them are divisible by three — then the third must be too. Those two add no remainder, the total has none — so the third can't bring one.",
            D('Cross out choice 4'),
            "Choice two. And that's division and remainder — done!"]})

    intro('q-436', "Three integers, a sum divisible by three — which claim can fail?")

    # ================================================================ practice (Hebrew-derived): new numbers / stories
    S('q-437', stem='A guide splits a group of hikers into teams of 4. Then she splits them into teams of 5. Each time, there is exactly one team with only 3 hikers. Which of the following could be the number of hikers in the group?',
      choices=['$27$', '$43$', '$38$', '$29$'], correct=2, expl=[
        'The number leaves remainder 3 when divided by 4 and when divided by 5.',
        'Take away the remainder: $n-3$ is divisible by 4 and by 5, so by 20.',
        'Only $43-3=40$ works. ($27-3=24$, $38-3=35$ and $29-3=26$ are not divisible by 20.)'])
    S('q-438', stem='A grandmother has $x$ stickers. She divides them equally among her 3 grandchildren. The eldest grandchild divides her share equally among 2 friends, and the second grandchild divides her share equally among 7 friends, with nothing left over. What is the smallest possible value of $x$?',
      choices=['$21$', '$42$', '$14$', '$84$'], correct=2, expl=[
        'Each grandchild gets $\\frac{x}{3}$ stickers. This share is divisible by 2 and by 7. They have no common factor, so it is divisible by 14.',
        'So $x=3\\cdot14k=42k$. The smallest value is $x=42$: each grandchild gets 14, and $14\\div2=7$, $14\\div7=2$ ✓.',
        '14 and 21 fail: $\\frac{14}{3}$ is not a whole number, and $\\frac{21}{3}=7$ is not divisible by 2. 84 works, but it is not the smallest.'])
    S('q-439', stem='$75\\%$ of the employees of a certain company come to work by train. Which of the following could be the total number of employees in the company?',
      choices=['$238$', '$412$', '$326$', '$315$'], correct=2, expl=[
        '$75\\%=\\frac34$. Build it from the inside: the company has $4k$ employees, and $3k$ of them come by train. So the total is divisible by 4.',
        'Last two digits: $238\\to38$ ✗, $412\\to12$ ✓, $326\\to26$ ✗, and $315$ is odd ✗.',
        'So 412 ($\\frac34\\cdot412=309$ come by train).'])
    S('q-440', stem='Which of the following numbers is divisible by 11?',
      choices=['$562$', '$719$', '$374$', '$948$'], correct=3, expl=[
        'Alternate plus and minus: $3-7+4=0$, so 374 is divisible by 11 ($374=11\\cdot34$).',
        'The others: $562$: $5-6+2=1$ ✗; $719$: $7-1+9=15$ ✗; $948$: $9-4+8=13$ ✗.'])
    S('q-441', stem='When the positive integer $x$ is divided by 14, the remainder is 4. What will be the remainder if $x$ is divided by 7?',
      choices=['$0$', '$3$', '$4$', 'It cannot be determined from the information given.'], correct=3, expl=[
        '$x=14k+4=7\\cdot2k+4$. The part $14k$ is made of full sevens.',
        'So the remainder by 7 is 4. (7 divides 14, so the remainder carries over.)',
        'Trap: $7-4=3$ is a difference, not a remainder.'])
    S('q-442', stem='$x$ is a positive integer. $18+6x$ is not necessarily divisible by:',
      choices=['$2$', '$4$', '$6$', '$3$'], correct=2, expl=[
        '$18+6x=6(3+x)$, so it is always divisible by 6, and therefore by 2 and by 3.',
        'By 4? Try $x=2$: $18+12=30$, and 30 is not divisible by 4. So 4 is not necessarily a divisor.'])
    S('q-443', stem='When the positive integer $x$ is divided by 8, the remainder is 5. What will be the remainder if $3x$ is divided by 8?',
      choices=['$5$', '$7$', '$3$', '$0$'], correct=2, expl=[
        'Multiply the remainder: $3\\cdot5=15$, and 15 divided by 8 leaves 7.',
        'With algebra: $3x=3(8k+5)=24k+15=8(3k+1)+7$. Check: $x=5$ gives $3x=15=8+7$ ✓.'])
    S('q-444', stem='$A$ is an even positive integer. Given: $n=A^3+24A^2+80A$. $n$ is necessarily divisible by:',
      choices=['$132$', '$16$', '$48$', '$24$'], correct=4, expl=[
        'Factor: $n=A(A^2+24A+80)=A(A+4)(A+20)$.',
        'Write $A=2m$: $n=2m(2m+4)(2m+20)=8\\cdot m(m+2)(m+10)$.',
        'One of $m$, $m+2$, $m+10$ is divisible by 3: if $m$ leaves 0, it is $m$; if $m$ leaves 1, then $m+2$ leaves $1+2=3$, that is 0; if $m$ leaves 2, then $m+10$ leaves $2+10=12$, that is 0. So $n$ is divisible by $8\\cdot3=24$.',
        'Knock out the others with examples: $A=2$ gives $n=2\\cdot6\\cdot22=264$, which is not divisible by 16 or 48. $A=4$ gives $n=4\\cdot8\\cdot24=768$, which is not divisible by 132.',
        'Trap: the smallest case (264) is not the answer. It only gives the biggest possible divisor.'])
    S('q-445', stem='Ron has 90 light bulbs, numbered 1 to 90, and all of them are off. In round 1 he turns on every bulb. In round 2 he changes the state of every second bulb (2, 4, 6, …): a bulb that is on is turned off, and a bulb that is off is turned on. In round 3 he changes the state of every third bulb, and so on, up to round 90 (in which he changes only bulb 90). Which of the following bulbs is on at the end?',
      choices=['$50$', '$72$', '$64$', '$88$'], correct=3, expl=[
        'Bulb $k$ changes state once in every round $d$ where $d$ divides $k$. So it changes state as many times as $k$ has divisors.',
        'It starts off, so it ends on only after an odd number of changes.',
        'Divisors come in pairs ($d$ and $\\frac{k}{d}$), except when $d\\cdot d=k$. So only perfect squares have an odd number of divisors.',
        '$64=8^2$ (divisors 1, 2, 4, 8, 16, 32, 64: seven changes, so it ends on). 50, 72 and 88 are not squares, so they end off.'])
    S('q-446', stem='Gil, Hila and Ido each have the same number $N$ of toy bricks. Gil built 7 towers of equal height, using all his bricks. Hila built 2 towers whose heights differ by exactly 1, using all her bricks. Ido built 3 towers of different heights, using all his bricks, and his tallest tower has 9 bricks. What is the value of $N$?',
      choices=['$15$', '$21$', '$28$', '$35$'], correct=2, expl=[
        'Gil: $N$ is divisible by 7. Hila: $N=h+(h+1)=2h+1$, so $N$ is odd. That leaves 21 and 35.',
        'Ido: $N=a+b+9$ with $a<b<9$. The most is $7+8+9=24$, so $N\\ne35$.',
        '$N=21$ works: for example, $4+8+9=21$.'])
    S('q-447', stem='$n$ is a two-digit positive integer, and $n^2-n$ is divisible by 10. What could be the units digit of $n$?',
      choices=['$4$', '$2$', '$0$', '$9$'], correct=3, expl=[
        '$n^2-n=n(n-1)$: two numbers in a row, so it is always even.',
        'For 10 it also needs a 5: $n$ or $n-1$ is divisible by 5. So $n$ ends in 0 or 5, or $n-1$ ends in 0 or 5 ($n$ ends in 1 or 6).',
        'Among the choices, only 0. Check: $n=30$: $900-30=870$ ✓. (Trap: 4 makes $n+1$ a multiple of 5, but the expression has $n-1$.)'])
    S('q-448', stem='Given: $y=17x+3$ ($x$ is a positive integer), and $y$ is divisible by 10. Which of the following could be the value of $x$?',
      choices=['$248$', '$263$', '$251$', '$239$'], correct=3, expl=[
        '$y$ ends in 0, so $17x$ ends in 7 (because $7+3=10$).',
        'The units digit of $17x$ depends only on $7\\cdot$(the units digit of $x$). $7\\cdot1=7$ ends in 7, so $x$ ends in 1.',
        'Only 251 ends in 1. Check: $17\\cdot251+3=4{,}267+3=4{,}270$ ✓.'])
    S('q-449', stem='$n$ is a positive integer divisible by 3. What is the greatest number that necessarily divides $n(n+3)$?',
      choices=['$9$', '$18$', '$27$', '$36$'], correct=2, expl=[
        'Write $n=3k$: $n(n+3)=3k(3k+3)=9\\cdot k(k+1)$.',
        '$k$ and $k+1$ are two numbers in a row, so $k(k+1)$ is even. Therefore $n(n+3)$ is divisible by $9\\cdot2=18$.',
        'Nothing bigger is certain: $n=3$ gives $3\\cdot6=18$, which is not divisible by 27 or 36.'])
    S('q-450', stem='A coach has $x$ balls. He tries to divide them equally among 5 teams, but 2 balls are left over. Then he decides that one team will get exactly twice as many balls as each of the other four teams. This time all the balls are given out. What is the smallest possible value of $x$?',
      choices=['$42$', '$12$', '$30$', '$22$'], correct=2, expl=[
        'First condition: $x$ leaves remainder 2 when divided by 5.',
        'Second condition: four teams get $s$ balls each and the fifth gets $2s$, so $x=s+s+s+s+2s=6s$. $x$ is divisible by 6.',
        'Multiples of 6: $6=5+1$ leaves 1 ✗; $12=10+2$ leaves 2 ✓. So $x=12$ (shares 2, 2, 2, 2 and 4).',
        '42 also works, but it is not the smallest. 30 leaves 0, and 22 is not divisible by 6.'])
    S('q-451', stem='Given:\n$\\begin{cases} b=2a \\\\ c=2b \\\\ d=2c \\end{cases}$\n($a$ is a positive integer). $a+b+c+d$ is necessarily divisible by:',
      choices=['$2$', '$15$', '$8$', '$4$'], correct=2, expl=[
        'Write everything with $a$: $b=2a$, $c=4a$, $d=8a$.',
        '$a+b+c+d=a+2a+4a+8a=15a$, so it is always divisible by 15.',
        'It is not necessarily divisible by 2, 4 or 8: for $a=1$ the sum is 15.'])
    S('q-452', stem="A pizzeria's phone number has 7 identical digits (for example, 5555555). Its delivery line is the phone number plus 1. What will be the remainder if the sum of the digits of the delivery-line number is divided by 7?",
      choices=['$0$', '$6$', '$1$', '$2$'], correct=3, expl=[
        'Call the repeated digit $d$.',
        'If $d\\le8$, adding 1 changes only the last digit: the digits are $d$ six times and then $d+1$. Their sum is $7d+1$, which leaves remainder 1.',
        'If $d=9$: $9{,}999{,}999+1=10{,}000{,}000$. The digit sum is 1, so the remainder is 1 again.',
        'Example: $5{,}555{,}555\\to5{,}555{,}556$, digit sum $36=7\\cdot5+1$ ✓.'])
    S('q-453', stem='When the positive integer $a$ is divided by 9, the remainder is 2. What will be the remainder if $a+1$ is divided by 6?',
      choices=['$3$', '$0$', '$1$', 'It cannot be determined from the information given.'], correct=4, expl=[
        '6 does not divide 9, so the remainder by 9 does not give the remainder by 6. Check with numbers.',
        '$a=2$: $a+1=3$, remainder 3. $a=11$: $a+1=12$, remainder 0.',
        'Two different remainders, so it cannot be determined. (Trap: $2+1=3$ keeps the old remainder.)',
        'Method 2 · Tag it: $a=9k+2$, so $a+1=9k+3$. The tag $9k$ is not always a multiple of $6$ ($9$, $18$, $27$, …), so the remainder by $6$ moves.',
        '$k=0$ gives $3$, remainder $3$. $k=1$ gives $12$, remainder $0$. So it cannot be determined (choice 4).'])
    S('q-454', stem='How many odd numbers between 0 and 80 leave a remainder of 3 when divided by 5?',
      choices=['$16$', '$7$', '$8$', '$15$'], correct=3, expl=[
        'The numbers that leave 3: $3, 8, 13, 18, \\ldots, 78$. They go up by 5, so they alternate odd, even.',
        'The odd ones end in 3: $3, 13, 23, 33, 43, 53, 63, 73$. That is 8 numbers.',
        'Trap: 16 counts all the numbers that leave 3, odd and even.'])
    S('q-455', stem='Given: $y=\\frac{\\sqrt2\\cdot x}{3}$, and $y$ is an integer divisible by 4. What is the greatest number that necessarily divides $x^2$?',
      choices=['$18$', '$72$', '$8$', '$36$'], correct=2, expl=[
        'Solve for $x$: $x=\\frac{3y}{\\sqrt2}$, so $x^2=\\frac{9y^2}{2}$.',
        'Write $y=4k$: $x^2=\\frac{9\\cdot16k^2}{2}=72k^2$. So $x^2$ is always divisible by 72.',
        'Nothing bigger is certain: $k=1$ gives $x^2=72$.'])
    S('q-456', stem='$x$, $y$ and $z$ are integers, and $x+y+z$ is divisible by 4. Which of the following statements is necessarily not correct?',
      choices=['$x$ and $y$ each leave remainder $1$ when divided by $4$, and $z$ leaves remainder $2$.',
               '$x$, $y$ and $z$ are all even.',
               '$x$ leaves remainder $3$ when divided by $4$, and $y+z$ leaves remainder $1$ when divided by $4$.',
               '$x+y$ leaves remainder $3$ when divided by $4$, and $z$ is divisible by $4$.'], correct=4, expl=[
        'Add the remainders. In (4): $3+0=3$, so $x+y+z$ would leave 3. That contradicts the given, so (4) is never correct.',
        'The others can happen: (1) $1+5+2=8$ ✓; (2) $2+4+6=12$ ✓; (3) $x=3$, $y=2$, $z=3$: $y+z=5$ leaves 1, and $3+2+3=8$ ✓.'])

    # ================================================================ practice clean-up (37 -> 25)
    # copies: q-r26-t15-07 (= guided Q5, a - b remainders), q-r26-t15-13 (units digit of a power = warm-up 3-2),
    # warm-up 3-4 (= guided Q2, two leftover conditions). Warm-ups kept (3): 3-7 (N = dq + r), 3-3 (digit sum ->
    # remainder by 9), 3-2 (units digit of a power). September items kept where the Hebrew practice lacks the type:
    # 06 (count the multiples in a range) and 09 (18 = 2·9, not 3·6).
    for qid in ['q-r26-t15-07', 'q-r26-t15-13', 'alg-extra-unit-t15-3-4',
                'alg-extra-unit-t15-3-1', 'alg-extra-unit-t15-3-5', 'alg-extra-unit-t15-3-6',
                'q-r26-t15-05', 'q-r26-t15-08', 'q-r26-t15-10', 'q-r26-t15-11', 'q-r26-t15-12', 'q-r26-t15-14']:
        M.unplace(qid)
    X = 'alg-extra-unit-t15-3-'
    M.practice_order(PRACTICE, [
        X + '7', 'q-441', 'q-439', X + '3', X + '2', 'q-454', 'q-442', 'q-443', 'q-437', 'q-440',
        'q-r26-t15-09', 'q-r26-t15-06', 'q-438', 'q-450', 'q-451', 'q-452', 'q-453', 'q-448', 'q-447', 'q-446',
        'q-456', 'q-449', 'q-444', 'q-455', 'q-445'])

    # ================================================================ sidebars, titles, canvas notes in sync
    for sec in (THEORY, ADV):
        vids = [f['ref'] for f in M.D['flow'] if f['section'] == sec and f['type'] == 'video'
                and M.video(f['ref']).get('kind') == 'solution']
        nums = [int(M.video(v)['beats'][0]['bigTitle'].split()[1]) for v in vids]
        for v, k in zip(vids, nums):
            M.set_sidebar(v, ['Question %d' % j for j in nums])
            V = M.video(v); q = M.q(V['questionId'])
            V['title'] = V['navLabel'] = rich_plain(q['stemRich']).replace('\n', ' ')
            for b in V['beats']:
                if b['mode'] == 'question': b['active'] = nums.index(k)
                if b.get('canvas', '').startswith('Pre-loaded — question'):
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (q['id'], q['stem'])


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber(M)   # 2026-10-06 renumber pass: runs last


# =====================================================================================================================
# 2026-10-06 Hebrew back-check: three questions had landed back on the numbers of the teacher's Hebrew VIDEOS
# (01-Algebra-Original-Subtitles.txt). New numbers - same type, trap, level and methods. Nothing in topic 15 is recorded.
def hebrew_backcheck(M):
    from math_api import rich_plain

    def S(qid, **kw):
        q = M.set_q(qid, **kw)
        for v in M.D['videos'].values():   # keep any pre-loaded copy of the choices in sync
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])

    def sync(qid):   # video title and slide descriptions show the new stem
        V = M.video('solve-' + qid); q = M.q(qid)
        V['title'] = V['navLabel'] = rich_plain(q['stemRich']).replace('\n', ' ')
        for b in V['beats']:
            if b.get('canvas', '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])
        M.touched_videos.add('solve-' + qid)

    def sub(vid, n, pairs):
        b = M.slide(vid, n)
        for old, new in pairs:
            hit = 0
            for l in b['lines']:
                for key in ('say', 'draw', 'label'):
                    if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit += 1
            assert hit, (vid, n, old)
        M.touched_videos.add(vid)

    # ---- q-430: Michal's claim was the Hebrew's "2 and 9 (18) vs 4 and 5 (20)"; now "3 and 7 (21) vs 2 and 13 (26)"
    S('q-430', stem='Yoav claims: "There are more three-digit numbers divisible by both 3 and 5 than three-digit numbers divisible by 17."\nMichal claims: "There are more three-digit numbers divisible by both 3 and 7 than three-digit numbers divisible by both 2 and 13."\nWhich of the following is correct?',
      choices=['Only Yoav is right.', 'Only Michal is right.', 'Both are right.', 'Both are wrong.'], correct=3, expl=[
        'Count the multiples: write the first and the last as $d\\cdot k$, then count $=$ last $k-$ first $k+1$.',
        'By 3 and 5, that is by 15: from $105=15\\cdot7$ to $990=15\\cdot66$, so $66-7+1=60$ numbers. By 17: from $102=17\\cdot6$ to $986=17\\cdot58$, so $58-6+1=53$. Since $60>53$, Yoav is right.',
        'By 3 and 7, that is by 21: from $105=21\\cdot5$ to $987=21\\cdot47$, so $47-5+1=43$. By 2 and 13, that is by 26: from $104=26\\cdot4$ to $988=26\\cdot38$, so $38-4+1=35$. Since $43>35$, Michal is right too.',
        'Both are right.'])
    sub('solve-q-430', 2, [
        ('Michal. Two and nine — no common factor — so divisible by eighteen. Four and five — divisible by twenty.',
         'Michal. Three and seven — no common factor — so divisible by twenty-one. Two and thirteen — divisible by twenty-six.'),
        ('18: 108 = 18·6 … 990 = 18·55 → 55 − 6 + 1 = 50', '21: 105 = 21·5 … 987 = 21·47 → 47 − 5 + 1 = 43'),
        ('Eighteen: from eighteen times six to eighteen times fifty-five. Fifty-five minus six, plus one: fifty.',
         'Twenty-one: from twenty-one times five to twenty-one times forty-seven. Forty-seven minus five, plus one: forty-three.'),
        ('20: 100 = 20·5 … 980 = 20·49 → 49 − 5 + 1 = 45', '26: 104 = 26·4 … 988 = 26·38 → 38 − 4 + 1 = 35'),
        ('Twenty: from twenty times five to twenty times forty-nine. Forty-five.',
         'Twenty-six: from twenty-six times four to twenty-six times thirty-eight. Thirty-five.'),
        ('Fifty beats forty-five. Michal is right too.', 'Forty-three beats thirty-five. Michal is right too.')])
    sub('solve-q-430', 3, [
        ('1/15 > 1/17    1/18 > 1/20', '1/15 > 1/17    1/21 > 1/26'),
        ('Same for Michal: one eighteenth beats one twentieth.', 'Same for Michal: one twenty-first beats one twenty-sixth.')])
    sync('q-430')

    # ---- q-434: was the Hebrew's 700 with x, 2x, 3x and 25/40/20/50 left; now 900 points and 15/24/26/32 left
    S('q-434', stem='Yael loaded 900 points onto an amusement-park card. The first ride cost $x$ points, the second ride cost $2x$ points, and the third ride cost $3x$ points. Which of the following could be the number of points left on her card after the three rides?',
      choices=['$15$', '$24$', '$26$', '$32$'], correct=2, expl=[
        'She paid $x+2x+3x=6x$ points, so the number of points she paid is divisible by 6 (by 2 and by 3).',
        'For each choice, find what she paid: $900-15=885$ (digit sum 21, but odd ✗), $900-24=876$ (even ✓, digit sum 21 ✓), $900-26=874$ (digit sum 19 ✗), $900-32=868$ (digit sum 22 ✗).',
        'So 24 points are left, and $x=876\\div6=146$.'])
    M.set_slide('solve-q-434', 2, script=[
        "Write what's left as an expression.",
        D('Write "paid: x + 2x + 3x = 6x"'),
        "She paid x, then two x, then three x — six x in total. Left: nine hundred minus six x.",
        "Could that be fifteen? Nine hundred minus fifteen is eight eighty-five — that must equal six x.",
        "x is a whole number of points, so eight eighty-five must be divisible by six.",
        "Divisible by six means divisible by two AND three.",
        D('Next to choice 1 write "885: sum 21 ✓, odd ✗"'),
        "Digit sum twenty-one — three is fine. But it's odd — not divisible by two. Out. That's the trap: checking only the three.",
        "Faster: for each choice, just ask how much she PAID — complete it to nine hundred.",
        D('Next to choice 2 write "876: even ✓, sum 21 ✓"'),
        "Twenty-four left means she paid eight seventy-six. Even, digit sum twenty-one — divisible by six. x is one hundred forty-six.",
        D('Circle choice 2'),
        "Choice two. In the lesson: twenty-six left means eight seventy-four paid — digit sum nineteen. Thirty-two left means eight sixty-eight — digit sum twenty-two. Both out."])
    sync('q-434')

    # ---- q-436: was the Hebrew's question itself (sum divisible by 3, the same four claims); now divisible by 6
    S('q-436', stem='The sum of three integers is divisible by 6. Which of the following statements is not necessarily true?',
      choices=['When one of the numbers is divided by $6$, the greatest possible remainder is $5$.',
               'If one of the numbers is divisible by $6$, then the other two are too.',
               'All three numbers can leave remainder $4$ when divided by $6$.',
               'If two of the numbers are divisible by $6$, then the third is too.'], correct=2, expl=[
        'Think in remainders: the remainders of the three numbers must add up to a multiple of 6.',
        '(1) True: dividing by 6, the remainder is 0, 1, 2, 3, 4 or 5.',
        '(2) Not necessarily: $12+5+7=24$. 12 is divisible by 6, but 5 and 7 are not.',
        '(3) Possible: $10+16+22=48$, and each number leaves remainder 4.',
        '(4) True: two numbers leave 0 and the sum leaves 0, so the third leaves 0.'])
    M.set_slide('solve-q-436', 2, script=[
        "When you add numbers, you can just add their remainders.",
        "Claim one: the largest remainder when dividing by six is five. Always true — the largest remainder is one less than the divisor.",
        D('Cross out choice 1'),
        "Six leaves zero, seven leaves one, and so on up to eleven, which leaves five. Twelve leaves zero again. A remainder of six? Then six would fit in again.",
        "Claim two: one of them is divisible by six — so the other two must be too?",
        D('Next to choice 2 write "12 + 5 + 7 = 24"'),
        "Twelve, five, seven. The sum is twenty-four — divisible by six. Twelve is divisible by six — but five and seven aren't. Their remainders, five and one, add up to six.",
        D('Circle choice 2'),
        "That claim can fail — choice two. In the exam, mark it and move on. In the lesson, let's check the other two.",
        "Claim three: all three leave remainder four? Four plus four plus four is twelve — divisible by six. Possible.",
        D('Next to choice 3 write "10 + 16 + 22 = 48 ✓"'),
        "Ten, sixteen, twenty-two — each leaves remainder four — sum forty-eight.",
        "Claim four: two of them are divisible by six — then the third must be too. Those two add no remainder, the total has none — so the third can't bring one.",
        D('Cross out choice 4'),
        "Choice two. And that's division and remainder — done!"])
    def fn(lines):
        for l in lines:
            if l.get('say') == "Three integers, a sum divisible by three — which claim can fail?":
                l['say'] = "Three integers, a sum divisible by six — which claim can fail?"
        return lines
    assert any(l.get('say') == "Three integers, a sum divisible by three — which claim can fail?" for l in M.slide('solve-q-436', 1)['lines'])
    M.edit_lines('solve-q-436', 1, fn)
    sync('q-436')


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

# Tag it: q-r26-t15-01 (line + slide). The other remainder / divisibility questions already solve with tags
# (q-423, q-427, q-431, q-434, q-435, q-441, q-443, q-438, q-450, q-451, q-449, q-444, q-455, q-r26-t15-15) or got
# their Tag it line on 2026-10-06 (q-r26-t15-07, q-453).
SPREAD_LINES = {
    'q-r26-t15-01': [
        'Method 2 · Tag it: $a=7k+2$ and $b=7m+5$ (different letters, because $a$ and $b$ are different numbers). '
        '$a-b=7k-7m-3=7(k-m-1)+4$. Whatever $k$ and $m$ are, the remainder is $4$, so choice 4 ("cannot be determined") is out too.',
    ],
}

SPREAD_SLIDES = {
    'solve-q-r26-t15-01': ('Method 2 · Check with numbers', 'Method 3 · Tag it', [
        "Two examples can't cover every pair. Tag it, and you know for sure.",
        A('a = 7k + 2, b = 7m + 5 appears', T(r'$a=7k+2,\qquad b=7m+5$', size=40)),
        "a is a multiple of seven, plus two. b is a multiple of seven, plus five. Different letters — they're different numbers.",
        A('a − b = 7(k − m) − 3 = 7(k − m − 1) + 4 appears', T(r'$a-b=7(k-m)-3=7(k-m-1)+4$', size=40)),
        "Subtract: sevens, minus three. Borrow one seven from the sevens — sevens, plus four.",
        D('Circle choice 2'),
        "Every pair leaves four. Choice two — and choice four, cannot be determined, is out.",
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
    # r26-t15-remainder-tools "Units digit": the units digit of a product is topic 1 (Multiplication & Division,
    # Last digit); powers repeating in a cycle of four is topic 21 (Patterns & Cycles, Days and last digits).
    # Removed; one reminder line on the title slide.
    G = 'r26-t15-remainder-tools'
    if not R.recorded(G):
        R.drop_slide(M, G, 'Units digit')
        R.set_slide(M, G, 'More Remainder Tools', [
            'Before the advanced questions: three short tools.',
            'Units digits work as you learned them: only the last digits count, and powers repeat in a cycle.',
            "The other tools you'll meet inside the questions themselves."])


_apply_before_trim_added_repeats = apply


def apply(M):
    _apply_before_trim_added_repeats(M)
    trim_added_repeats(M)   # 2026-10-07 trim added repeats: runs last
