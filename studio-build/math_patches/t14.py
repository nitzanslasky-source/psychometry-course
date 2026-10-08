"""Topic 14 - Prime Numbers. Course review 2026-09 fixes.
See t14_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q
import math_api

TOPIC = 14
LESSON_A = 'primes'
LESSON_B = 'prime-tools'
TRICKS = 'r26-t14-more-tools'
G = ['q-r26-t14-%02d' % k for k in range(1, 5)]          # new guided questions
P = lambda k: 'q-r26-t14-%02d' % k                       # new practice questions (05..15)


def _word(n):
    return math_api._word(n)


def _solution(M, qid, group, num, intro, slides, section, after):
    """Guided-question solution video in the style of the topic's existing ones."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % _word(n)] + intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=0, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, group, [], beats, section, kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = num
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _fix_draw(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _replace_say(M, vid, n, old, new):
    """Replace a spoken line that contains `old` (new=None deletes it)."""
    def fn(lines):
        out = []
        for l in lines:
            if 'say' in l and old in l['say']:
                if new is None: continue
                l = dict(l, say=new)
            out.append(l)
        return out
    M.edit_lines(vid, n, fn)


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Theory A lesson "Prime Numbers"
    # =====================================================================================
    # slide 2: delete the false "times table" sentence
    _replace_say(M, LESSON_A, 2, 'times table', None)

    # slide 3: 0, 1 and negatives; 2 is the only even prime; parity of two primes
    M.set_slide(LESSON_A, 3, title='0, 1 and 2', script=[
        "Some special cases.",
        A("'0, 1 and negative numbers are not prime' appears", T('$0$, $1$ and negative numbers are not prime.', size=46)),
        "One is NOT prime. It has only one divisor — you can't break it into anything.",
        "Zero and negative numbers are not prime either. A prime is always a whole number bigger than one.",
        A("'2 is the only even prime' appears", T('$2$ is the only even prime.', size=46)),
        D('Circle "only even"'),
        "Two IS prime — its only divisors are one and two.",
        "And it's the only even one. Every other even number divides by two as well — twenty, eighteen… not prime.",
        A("'Two primes, odd sum or difference → one of them is 2' appears",
          T('Odd sum or difference of two primes $\\to$ one is $2$', size=44)),
        "This gives a strong exam tool. All the other primes are odd.",
        "Odd plus odd is even. Odd minus odd is even too.",
        "So if two primes give an ODD sum, or an ODD difference — one of them must be two.",
        D('Write "25 = 2 + 23"'),
        "Twenty-five is odd. As a sum of two primes, it must be two plus twenty-three.",
    ])

    # slide 4: point to the new test
    M.edit_lines(LESSON_A, 4, lambda ls: ls + [{'say': "Above forty? Don't guess. There's a quick test — next."}])

    # new slide 5: the square-root test and the fake primes
    M.insert_slides(LESSON_A, 4, [dict(mode='concept', active=3, title='Is it prime?', script=[
        "How do you check if a bigger number is prime?",
        A("'To test n: try the primes up to √n' appears", T('To test $n$: try the primes up to $\\sqrt{n}$', size=46, gap=40)),
        "Divide it by the primes up to its square root. No need to go further.",
        "Why? If n breaks into two factors, one of them is at most the square root. So you would find it.",
        A('91: √91 < 10 → try 2, 3, 5, 7 appears', T('$91$: $\\sqrt{91}<10\\ \\to$ try $2,\\ 3,\\ 5,\\ 7$', size=46, gap=40)),
        "Take ninety-one. Nine squared is eighty-one, ten squared is a hundred. So its root is less than ten.",
        "Try two, three, five and seven. That's all.",
        "Two? It's odd. Three? A quick test: add the digits. Nine plus one is ten — ten doesn't divide by three. So no.",
        "Five? It doesn't end in zero or five. Seven?",
        D('Write "91 ÷ 7 = 13  →  91 = 7 · 13  ✗"'),
        "Seven times thirteen is ninety-one. Not prime!",
        A('The fake primes appear', T('Fake primes: $51=3\\cdot17$,  $57=3\\cdot19$,  $87=3\\cdot29$,  $91=7\\cdot13$,  $119=7\\cdot17$', size=38)),
        "These look prime — but they're not. The exam loves them.",
        "Fifty-one, fifty-seven, eighty-seven: add the digits — all divide by three. Ninety-one and a hundred nineteen: both divide by seven.",
    ])])

    # slide 6 (was 5): ÷ instead of ":" on the board
    b = M.slide(LESSON_A, 6)
    b['items'][0]['t'] = '$20 \\div 4 = 5$'
    b['items'][1]['t'] = '$30 \\div 6 = 5$'
    for n, act in ((6, 4), (7, 5), (8, 6), (9, 7)):
        M.slide(LESSON_A, n)['active'] = act

    # recap
    M.set_slide(LESSON_A, 10, active=8, script=[
        "Let's lock it in.",
        A("'Prime: only 1 and itself; 0 and 1 are not prime; 2 is the only even prime' appears",
          T('Prime: only $1$ and itself · $0$ and $1$ are not prime · $2$ is the only even prime', size=36)),
        A("'Two primes, odd sum or difference → one of them is 2' appears",
          T('Two primes, odd sum or difference $\\to$ one of them is $2$', size=36)),
        A("'Know the primes up to 40 — and 97' appears", T('Know the primes up to $40$ — and $97$', size=36)),
        A("'Is n prime? Try the primes up to √n' appears", T('Is $n$ prime? Try the primes up to $\\sqrt{n}$', size=36)),
        A("'Divisor = factor' appears", T('Divisor = factor', size=36)),
        A("'Divides by every combination of its prime factors' appears",
          T('A number divides by every combination of its prime factors', size=36)),
        D('Underline "combination"'),
        "There's a memory card with the primes and these facts right after this video.",
        "Four questions next. Try each one — then watch the solution.",
    ])
    M.set_sidebar(LESSON_A, ['What a prime is', '0, 1 and 2', 'Know them by heart', 'Is it prime?', 'Divisor = factor',
                             'Prime factors', 'Break it down', 'Is it a divisor?', 'Recap'])

    # memory card "Prime numbers"
    c = M.card('mem-primes')
    c['tables'][0]['title'] = 'Primes up to 60'
    c['tables'][0]['rows'] += [['41–50', '$41,\\ 43,\\ 47$'], ['51–60', '$53,\\ 59$']]
    c['tables'][1]['rows'] = [
        ['$0$, $1$, negative numbers', 'are not prime'],
        ['$2$', 'is prime — the only even prime'],
        ['Two primes, odd sum or odd difference', 'one of them is $2$'],
        ['$97$', 'is the largest two-digit prime'],
        ['Is $n$ prime?', 'try the primes up to $\\sqrt{n}$'],
        ['Divisor', 'means the same as factor'],
    ]
    c['tables'].append({'title': 'Fake primes (they look prime, but are not)', 'head': ['Number', 'Breaks into'], 'rows': [
        ['$51$', '$3\\cdot17$'], ['$57$', '$3\\cdot19$'], ['$87$', '$3\\cdot29$'],
        ['$91$', '$7\\cdot13$'], ['$119$', '$7\\cdot17$'], ['$133$', '$7\\cdot19$']]})
    c['tips'] = [
        'A number divides by every combination of its prime factors: $12=2\\cdot2\\cdot3$, therefore $2$, $3$, $4$, $6$ and $12$ divide it.',
        'To test a divisor, check its prime ingredients — unpack non-prime bases like $6$ or $10^2$ first.',
        'Quick test for $3$: add the digits. $87$: $8+7=15$, and $15$ divides by $3$, therefore $87$ does too.',
    ]

    # =====================================================================================
    # 2. Theory B lesson "Factor Tools": GCD = lower power, LCM = higher power
    # =====================================================================================
    M.set_slide(LESSON_B, 1, script=[
        "Factor tools.",
        "There's a question type many students find hard: \"the greatest divisor\".",
        "It comes in two versions, and each has an official name. Let's make both of them simple.",
    ])
    M.set_slide(LESSON_B, 2, title='Greatest common (GCD)', script=[
        "Version one: the greatest COMMON divisor of two numbers. Its official name: GCD.",
        "The biggest number that divides both of them. Like taking out a common factor — you already know how.",
        A('72 = 2³ · 3² appears', T('$72=2^3\\cdot3^2$', size=54, gap=30)),
        A('90 = 2 · 3² · 5 appears', T('$90=2\\cdot3^2\\cdot5$', size=54, gap=80)),
        "Seventy-two and ninety. Which primes are in BOTH?",
        D('Circle the 2 and the 3² in both lines'),
        "Two and three. The five is only in ninety. Out.",
        "How many of each? Take the LOWER power.",
        D('Write "2: 2³ and 2¹ → 2¹"  and  "3: 3² and 3² → 3²"'),
        "Twos: three in seventy-two, only one in ninety. Take one — ninety has no more to give. Threes: two and two. Take two.",
        D('Underneath write "GCD = 2 · 3² = 18"'),
        "Two times three squared: eighteen.",
        "The rule: GCD — each shared prime, at its LOWER power.",
    ])
    M.set_slide(LESSON_B, 3, title='Greatest guaranteed (LCM)', script=[
        "Version two: the greatest GUARANTEED divisor. Now there's one number — and we don't know it.",
        "We only know that it divides by two numbers. What can we be SURE divides it?",
        A("'Divides by 2 and by 5' appears", T('Divides by $2$ and by $5$', size=48, gap=40)),
        D('Write "→ divides by 2 · 5 = 10 ✓"'),
        "It divides by two and by five? Then it divides by ten. They share no prime.",
        A("'Divides by 2 and by 6' appears", T('Divides by $2$ and by $6$', size=48, gap=40)),
        D('Write "2 · 6 = 12? ✗ — 6 itself works"'),
        "Two and six? Must it divide by twelve? No — six itself divides by two AND by six. The two is already inside the six.",
        "So don't just multiply. Break into primes, and take every prime at its HIGHER power.",
        A('72, 90 → 2³ · 3² · 5 = 360 appears', T('$72,\\ 90\\ \\to\\ 2^3\\cdot3^2\\cdot5=360$', size=48)),
        "Seventy-two and ninety. Twos: three and one — take three. Threes: two and two — take two. Fives: none and one — take one.",
        "Two cubed, times three squared, times five: three hundred sixty.",
        "Its official name: the least common multiple — LCM. The smallest number that both of them divide.",
        "So a number that divides by seventy-two and by ninety must divide by three hundred sixty. That's the greatest guaranteed divisor.",
    ])
    table = {'k': 'vis', 'w': 1000, 'h': 380, 'gap': 40, 'v': {'type': 'table',
             'headers': ['Prime', 'In 72', 'In 90', 'GCD: lower', 'LCM: higher'],
             'rows': [['2', '2³', '2¹', '2¹', '2³'], ['3', '3²', '3²', '3²', '3²'], ['5', '5⁰ (none)', '5¹', '5⁰', '5¹'],
                      ['Result', '72', '90', '18', '360']]}}
    M.insert_slides(LESSON_B, 3, [dict(mode='concept', active=2, title='GCD vs LCM', script=[
        "Here are both, side by side. The same two numbers.",
        A('The GCD / LCM table appears', table),
        "Each row is one prime. GCD: take the LOWER power. LCM: take the HIGHER power.",
        D('Circle the GCD column and write "lower"; circle the LCM column and write "higher"'),
        "Five is missing from seventy-two — that's five to the zero. The lower power is zero: no five in the GCD. The higher is one: one five in the LCM.",
        A("'GCD · LCM = a · b' appears", T('GCD $\\cdot$ LCM $=a\\cdot b$:  $18\\cdot360=72\\cdot90=6480$', size=40, gap=30)),
        "A bonus check: the GCD times the LCM equals the two numbers multiplied. Eighteen times three sixty is six thousand four hundred eighty. So is seventy-two times ninety.",
        "Know three of these four numbers? You can find the fourth.",
        A("'Trap: 72 · 90 is not the LCM' appears", T('Trap: $72\\cdot90$ is NOT the LCM', size=40)),
        "And the trap: multiplying the two numbers. That's too big whenever they share a prime.",
    ])])
    # break & build (now slide 5): name the plug-in method
    M.set_slide(LESSON_B, 5, active=3, script=[
        "This is the heart of the whole topic.",
        "With primes we can take any number apart — and put numbers together.",
        A("'Break apart: split into factor pairs' appears", T('Break apart: split a number into factor pairs', size=44)),
        A("'Build: multiply the pieces you're given' appears", T("Build: multiply the pieces you're given", size=44)),
        A("'Check: which prime is missing?' appears", T('Check: which prime is missing?', size=44)),
        D('Box "which prime is missing?"'),
        "Many questions dress it up with a long story. Underneath, they're just asking: can you break it — or can you build it?",
        A("'Letters as primes? Plug in 2, 3, 5, 7' appears", T('Letters as primes? Plug in $2,\\ 3,\\ 5,\\ 7$', size=44)),
        "And when the primes are letters — a, b, c — plug in the smallest primes: two, three, five, seven, in the right order.",
        "Then check EVERY choice. The numbers are only an example. Knock out the other three before you mark.",
    ])
    # symmetric divisors (now slide 6): odd number of divisors <-> perfect square
    M.set_slide(LESSON_B, 6, active=4, script=[
        "Most numbers split into divisors in pairs.",
        A('10 = 1 · 10 = 2 · 5 appears', T('$10=1\\cdot10=2\\cdot5$', size=50, gap=30)),
        A('12 = 1 · 12 = 2 · 6 = 3 · 4 appears', T('$12=1\\cdot12=2\\cdot6=3\\cdot4$', size=50, gap=50)),
        "Ten: one and ten, two and five. Twelve: one and twelve, two and six, three and four.",
        "Pairs — so an even number of divisors.",
        A("'Divisors of 9: 1, 3, 9' appears", T('Divisors of $9$:  $1,\\ 3,\\ 9$', size=46, gap=30)),
        D('Circle the 3'),
        "But nine? One, three, nine. The three sits in the middle — three times three. It has no partner.",
        A("'Divisors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36' appears",
          T('Divisors of $36$:  $1,\\ 2,\\ 3,\\ 4,\\ 6,\\ 9,\\ 12,\\ 18,\\ 36$', size=46)),
        D('Circle the 6'),
        "Thirty-six: nine divisors. Six times six — the six has no partner.",
        D('Write "odd number of divisors ↔ perfect square"'),
        "So an odd number of divisors means a perfect square — and every perfect square has an odd number of divisors.",
        D('Write "exactly 3 divisors → prime²"'),
        "The most common case: exactly three divisors. One, p, and p squared. That's a prime squared — like nine, or twenty-five.",
    ])
    _fix_draw(M, LESSON_B, 7, '2: 0,1,2,3 → 4 options', '2: 0, 1, 2, 3 → 4 options')
    _fix_draw(M, LESSON_B, 7, '5: 0,1,2 → 3 options', '5: 0, 1, 2 → 3 options')
    M.slide(LESSON_B, 7)['active'] = 5
    M.set_slide(LESSON_B, 8, active=6, script=[
        "Let's lock it in.",
        A("'GCD: shared primes, each at its LOWER power' appears", T('GCD: shared primes, each at its LOWER power', size=38)),
        A("'LCM = greatest guaranteed divisor: every prime at its HIGHER power' appears",
          T('LCM (guaranteed divisor): every prime at its HIGHER power', size=38)),
        A("'GCD · LCM = a · b' appears", T('GCD $\\cdot$ LCM $=a\\cdot b$', size=38)),
        A("'Odd number of divisors → a perfect square' appears",
          T('Odd number of divisors $\\to$ square;  exactly $3$ $\\to$ prime squared', size=38)),
        A("'Number of divisors: each exponent + 1, multiplied' appears",
          T('Number of divisors: each exponent $+1$, multiplied', size=38)),
        D('Underline "LOWER" and "HIGHER"'),
        "In my eyes, breaking and building numbers is the most important lesson in the whole primes topic.",
        "The factor tools card comes right after this video. Then seven questions.",
    ])
    M.set_sidebar(LESSON_B, ['GCD: lower power', 'LCM: higher power', 'GCD vs LCM', 'Break & build',
                             'Symmetric divisors', 'Counting divisors', 'Recap'])

    c = M.card('mem-factor-tools')
    c['intro'] = 'The two "greatest divisor" wordings, their official names, and the divisor facts.'
    c['tables'][0]['rows'] = [
        ['Greatest COMMON divisor (GCD) of two numbers', 'Primes in both, each at its LOWER power',
         '$72=2^3\\cdot3^2$, $90=2\\cdot3^2\\cdot5$ → $2\\cdot3^2=18$'],
        ['Greatest GUARANTEED divisor (divides by both) = least common multiple (LCM)', 'Every prime, each at its HIGHER power',
         '$72,\\ 90$ → $2^3\\cdot3^2\\cdot5=360$'],
        ['Check', 'GCD × LCM = the two numbers multiplied', '$18\\cdot360=72\\cdot90$'],
        ['Odd number of divisors', 'It is a perfect square', '$36$: $9$ divisors'],
        ['Exactly 3 divisors', 'It is a prime squared', 'divisors of $9$: $1$, $3$, $9$'],
        ['Number of divisors', 'Each exponent + 1, multiplied', '$2^3\\cdot5^2$ → $4\\cdot3=12$'],
    ]
    c['tips'] = [
        'Divides by $2$ and $5$ → by $10$. Divides by $2$ and $6$ → only $6$ is sure (the $2$ is inside the $6$).',
        'Trap: multiplying the two numbers. $8\\cdot12=96$, but the LCM of $8$ and $12$ is $24$, because they share the prime $2$.',
        'Letters as primes? Plug in the smallest primes $2$, $3$, $5$, $7$ in the right order, then check every choice.',
    ]

    # =====================================================================================
    # 3. Move Q4 (GCD) and Q5 (LCM) after the Factor Tools lesson
    # =====================================================================================
    M.move('q-389', 'primes-b', after='mem-factor-tools')
    M.move('solve-q-389', 'primes-b', after='q-389')
    M.move('q-390', 'primes-b', after='solve-q-389')
    M.move('solve-q-390', 'primes-b', after='q-390')
    for vid in ('solve-q-389', 'solve-q-390'):
        M.video(vid)['hybrid']['title'] = 'Factor Questions'
        M.video(vid)['hybrid']['num'] = M.video('solve-q-398')['hybrid']['num']
    M.set_slide('solve-q-389', 1, title='Question 4', script=["Question four.", "The greatest common divisor — the GCD."])
    M.set_slide('solve-q-389', 2, title='Lower power', script=[
        "The GCD: which primes are in BOTH numbers — and at what power?",
        "Each shared prime, at its LOWER power.",
        D('Circle a² in both x and y'),
        "a: x has a squared, y has a cubed. The lower power: a squared.",
        D('Cross out b'),
        "b: only in x. Not shared. Out.",
        D('Circle c² in both'),
        "c: c to the fourth and c squared. The lower: c squared.",
        D('Circle d in both'),
        "d: d and d squared. The lower: d.",
        D('Write "a² · c² · d" and circle choice 2'),
        "a squared, c squared, d. Choice two.",
        "Choice three is the trap — every prime at its HIGHER power. That's the LCM, not the GCD.",
    ])
    M.set_slide('solve-q-390', 1, title='Question 5', script=["Question five.", "The greatest GUARANTEED divisor — that's the LCM."])
    for vid in ('solve-q-389', 'solve-q-390'):
        M.slide(vid, 1)['title'] = 'Factor Questions'
    M.set_slide('solve-q-390', 2, title='Higher power', script=[
        "The number divides by eight and by twelve. What can we be SURE divides it?",
        "Break both into primes.",
        D('Write "8 = 2³" and "12 = 2² · 3"'),
        "Eight is two cubed. Twelve is two squared times three.",
        "Multiply them? Ninety-six? No! The twos in twelve may be the very same twos that are in eight.",
        "Take every prime at its HIGHER power.",
        D('Write "2: 2³ and 2² → 2³;   3: only 3¹ → 3"'),
        "Twos: three and two — take three. Threes: only in twelve — take one.",
        D('Write "2³ · 3 = 24" and circle choice 1'),
        "Two cubed times three: twenty-four. Choice one.",
        "Check: twenty-four itself divides by eight and by twelve. And forty-eight doesn't divide twenty-four. So we can't promise more.",
    ])
    _replace_say(M, 'solve-q-398', 1, 'number one', 'Factor questions. Question six.')

    # =====================================================================================
    # 4. Existing solution videos: small fixes
    # =====================================================================================
    _replace_say(M, 'solve-q-391', 1, 'First question', 'Advanced primes. Question eleven.')
    M.edit_lines('solve-q-391', 2, lambda ls: [
        dict(l, say="And the primes are almost all odd — except one. Two. The only even prime. We saw this rule at the start of the topic.")
        if l.get('say', '').startswith('And the primes are almost all odd') else l for l in ls])
    M.edit_lines('solve-q-395', 2, lambda ls: ls + [
        {'say': "One more word. Statement four is NEVER true."},
        {'say': "Never true is also \"not necessarily true\". So it's the answer."},
    ])
    M.edit_lines('solve-q-392', 3, lambda ls: [
        dict(l, say="On the exam — mark it. In the lesson, check fifteen too: fifteen is three times five. a would have to be five — and then b is three. But three divides fifteen AND thirty. Out.")
        if l.get('say', '').startswith('On the exam — mark it. In the lesson, check fifteen') else l for l in ls])

    # =====================================================================================
    # 5. Existing questions: TeX, no colons, stacked conditions, clearer wording
    # =====================================================================================
    S('q-386', stem='$x$ and $y$ are integers that are not prime, and $x<20<y$. Between $x$ and $20$ there are exactly $2$ prime numbers (not including $x$). Between $20$ and $y$ there are exactly $2$ prime numbers (not including $y$). What is the smallest possible value of $x\\cdot y$?',
      expl=['The primes near $20$: $11$, $13$, $17$, $19$, $23$, $29$, $31$.',
            'Below $20$: the two primes must be $17$ and $19$, and $13$ must stay out. Therefore $13\\le x<17$. $x$ is not prime, therefore $x$ is $14$, $15$ or $16$.',
            'Above $20$: the two primes must be $23$ and $29$, and $31$ must stay out. Therefore $29<y\\le31$. $y=31$ is prime (not allowed), therefore $y=30$.',
            'The smallest product: $14\\cdot30=420$.'])
    S('q-387', stem='Given: $x$ is a prime number, and $x^5$ is a two-digit number. $7x=?$',
      expl=['Test the smallest primes.', '$x=2$: $2^5=32$, two digits ✓.',
            '$x=3$: $3^5=243$, three digits ✗. Bigger primes give even bigger fifth powers.',
            'So $x=2$ and $7x=7\\cdot2=14$.'])
    S('q-388', stem='Given: $x=3\\cdot2^3\\cdot10^2$. Which of the following numbers does not divide $x$?',
      expl=['Break the non-prime factor into primes: $10^2=(2\\cdot5)^2=2^2\\cdot5^2$. Therefore $x=2^5\\cdot3\\cdot5^2$.',
            'Check each choice: $15=3\\cdot5$ ✓, $20=2^2\\cdot5$ ✓, $30=2\\cdot3\\cdot5$ ✓.',
            '$21=3\\cdot7$, and $x$ has no $7$. So $21$ does not divide $x$.'])
    S('q-389', stem='$a$, $b$, $c$, $d$ are different prime numbers.\nGiven:\n$\\begin{cases} x=a^2\\cdot b\\cdot c^4\\cdot d \\\\ y=a^3\\cdot c^2\\cdot d^2 \\end{cases}$\nWhat is the greatest common divisor (GCD) of $x$ and $y$?',
      choices=['$a\\cdot c\\cdot d$', '$a^2\\cdot c^2\\cdot d$', '$a^3\\cdot b\\cdot c^4\\cdot d^2$', '$a\\cdot b\\cdot c\\cdot d$'],
      expl=['GCD: take each prime that is in both numbers, at its LOWER power.',
            '$a$: $a^2$ and $a^3$ → $a^2$. $c$: $c^4$ and $c^2$ → $c^2$. $d$: $d$ and $d^2$ → $d$.',
            '$b$ is only in $x$, therefore it is not in the GCD.',
            'GCD $=a^2\\cdot c^2\\cdot d$. (Choice (3) takes the higher powers: that is the LCM.)'])
    S('q-390', stem='A number is divisible without remainder by both $8$ and $12$. What is the greatest number that is guaranteed to divide it?',
      expl=['Break into primes: $8=2^3$ and $12=2^2\\cdot3$.',
            'The number divides by both, therefore it divides by their least common multiple (LCM): every prime at its HIGHER power. $2^3\\cdot3=24$.',
            'Nothing bigger is guaranteed: the number could be $24$ itself, and $48$ does not divide $24$.',
            'The trap: $8\\cdot12=96$. The two numbers share the prime $2$, therefore their product is too big.'])
    S('q-398', stem='$x$ is a three-digit number made only of the digits $1$, $2$ and $3$ (a digit may repeat). Which of the following cannot be the product of the digits of $x$?',
      expl=['Each digit is $1$, $2$ or $3$, therefore the product is built only from the primes $2$ and $3$.',
            '$12=2\\cdot2\\cdot3$ (digits $2$, $2$, $3$) ✓. $9=1\\cdot3\\cdot3$ ✓. $6=1\\cdot2\\cdot3$ ✓.',
            '$10=2\\cdot5$ needs the prime $5$, and no digit gives it. So $10$ is impossible.'])
    S('q-399', stem='$x$ and $y$ are positive integers, and neither of them is $1$.\nGiven:\n$\\begin{cases} x\\cdot y=36 \\\\ A=|x-y| \\end{cases}$\nWhat is the difference between the greatest possible value of $A$ and the smallest possible value of $A$?',
      expl=['Break $36$ into pairs of factors (without $1$): $2\\cdot18$, $3\\cdot12$, $4\\cdot9$, $6\\cdot6$.',
            'The values of $A$: $18-2=16$, $12-3=9$, $9-4=5$, $6-6=0$.',
            'Greatest $A=16$, smallest $A=0$. The difference: $16-0=16$.'])
    S('q-400', stem='You multiply two or more of the numbers $2$, $3$ and $7$ (each number at most once). What is the sum of all the different products you can get?',
      expl=['Products of two numbers: $2\\cdot3=6$, $2\\cdot7=14$, $3\\cdot7=21$.',
            'Product of all three: $2\\cdot3\\cdot7=42$.',
            'Sum: $6+14+21+42=83$. (Forgetting $42$ gives $41$ — the trap.)'])
    S('q-401', stem='Given: $y^2$ is a prime number. Which of the following is necessarily true?',
      choices=['$y$ is odd', '$y$ is even', '$y$ is prime', '$y$ is not an integer'],
      expl=['If $y$ were an integer with $|y|>1$, then $y^2=y\\cdot y$ would break into two factors bigger than $1$. It would not be prime.',
            'If $y$ were $0$, $1$ or $-1$, then $y^2$ would be $0$ or $1$. These are not prime either.',
            'So $y$ is not an integer. Example: $y=\\sqrt3$ gives $y^2=3$, a prime.'])
    S('q-402', stem='$n$ is a positive integer with exactly $3$ different divisors (including $1$ and $n$).\nGiven: $B=\\sqrt{n}$.\nHow many divisors does $B$ have (including $1$ and $B$)?',
      choices=['$0$', '$n$', '$2$', '$1$'],
      expl=['Exactly $3$ divisors means $n=p^2$ for a prime $p$. Its divisors are $1$, $p$ and $p^2$.',
            '$B=\\sqrt{p^2}=p$, a prime.',
            'A prime has exactly $2$ divisors: $1$ and itself. Example: $n=49$, $B=7$, and the divisors of $7$ are $1$ and $7$.'])
    S('q-391', stem='$a$ and $b$ are prime numbers. Which of the following numbers cannot be $a+b$?',
      expl=['All four choices are odd. An odd sum of two primes needs one even prime, and the only even prime is $2$.',
            'So check whether the choice minus $2$ is prime.',
            '$25=2+23$ ✓. $33=2+31$ ✓. $45=2+43$ ✓ ($43$ is prime: $\\sqrt{43}<7$, and $2$, $3$, $5$ do not divide it).',
            '$27=2+25$, and $25=5^2$ is not prime ✗. So the sum cannot be $27$.'])
    S('q-392', stem='$a$ and $b$ are prime numbers.\nExactly two of the numbers $10$, $15$, $7$ are divisible by $a$.\nExactly one of the numbers $22$, $15$, $30$ is divisible by $b$.\n$a\\cdot b=?$',
      expl=['Break into primes: $10=2\\cdot5$, $15=3\\cdot5$, $7=7$. Only the prime $5$ is in exactly two of them. So $a=5$.',
            '$22=2\\cdot11$, $15=3\\cdot5$, $30=2\\cdot3\\cdot5$. The primes $2$, $3$ and $5$ are each in two of them. Only $11$ is in exactly one. So $b=11$.',
            '$a\\cdot b=5\\cdot11=55$.'])
    S('q-393', stem='$a$ and $b$ are positive integers.\nGiven:\n$\\begin{cases} a<b \\\\ a\\cdot b+2a=36 \\end{cases}$\nWhich of the following cannot be the value of $a+b$?',
      expl=['Take out the common factor $a$: $a(b+2)=36$.',
            'Go over the factor pairs of $36$. $a=1$: $b+2=36$, $b=34$, $a+b=35$. $a=2$: $b+2=18$, $b=16$, $a+b=18$.',
            '$a=3$: $b+2=12$, $b=10$, $a+b=13$. $a=4$: $b+2=9$, $b=7$, $a+b=11$.',
            '$a=6$: $b+2=6$, $b=4<a$ ✗. A bigger $a$ gives an even smaller $b$ ✗.',
            'The possible sums are $35$, $18$, $13$ and $11$. $15$ is not possible.'])
    S('q-394', stem='$a$, $b$, $c$, $d$ are prime numbers, and $a<b<c<d$.\nGiven: $y=a^d\\cdot b^c$.\nWhich of the following necessarily divides $y$?',
      choices=['$b^d$', '$c$', '$a^c\\cdot b^a$', '$d^b$'],
      expl=['$y$ is built from the prime $a$ ($d$ times) and the prime $b$ ($c$ times).',
            '$a^c$: $c<d$, therefore $y$ has enough $a$s ✓. $b^a$: $a<c$, therefore $y$ has enough $b$s ✓. So $a^c\\cdot b^a$ divides $y$.',
            '$b^d$: $y$ has only $c$ copies of $b$, and $c<d$ ✗. $c$ and $d^b$: the primes $c$ and $d$ are not factors of $y$ at all ✗.',
            'With the smallest primes: $a=2$, $b=3$, $c=5$, $d=7$ give $y=2^7\\cdot3^5$, and of the four choices only $2^5\\cdot3^2$ divides it.'])
    S('q-395', stem='$a$, $b$, $c$ are different positive integers.\nGiven: $x=a\\cdot b\\cdot c$ is divisible by $15$ without remainder.\nWhich of the following statements is not necessarily true?',
      choices=['At least one of $a$, $b$, $c$ is divisible by $5$.',
               'It is possible that exactly one of $a$, $b$, $c$ is divisible by $15$.',
               'If $a$ and $b$ are not divisible by $3$, then $c^2$ is divisible by $9$.',
               'The number of different prime divisors of $x^2$ is greater than that of $x$.'],
      expl=['(1) Always true: $5$ is prime and divides $a\\cdot b\\cdot c$, therefore it divides one of the factors.',
            '(2) Possible: $a=15$, $b=1$, $c=2$ ✓.',
            '(3) Always true: $3$ is prime and divides $a\\cdot b\\cdot c$. It does not divide $a$ or $b$, therefore it divides $c$. Then $c^2$ is divisible by $3^2=9$.',
            '(4) Never true: squaring doubles the exponents but adds no new prime. For example, $15=3\\cdot5$ and $225=3^2\\cdot5^2$ have the same two primes.',
            'Never true is also "not necessarily true", therefore the answer is (4).'])
    S('q-396', stem='$a$ and $b$ are positive integers. $a$ has exactly two prime factors: $2$ and $5$. $b$ has exactly two prime factors: $2$ and $7$.\nGiven: $b<a$.\nWhat is the smallest possible value of $\\frac{a\\cdot b}{35}$?',
      expl=['Numbers with exactly the prime factors $2$ and $5$: $10$, $20$, $40$, $50$, … Numbers with exactly the prime factors $2$ and $7$: $14$, $28$, $56$, …',
            'The expression is smallest when $a$ and $b$ are smallest. The smallest $b$ is $14$. Since $b<a$, $a=10$ is too small. The smallest $a$ is $20$.',
            '$\\frac{a\\cdot b}{35}=\\frac{20\\cdot14}{35}=\\frac{280}{35}=8$.'])
    S('q-397', stem='$a$ is an integer.\nGiven: $1<a<150$, and $a$ has exactly $3$ different divisors (including $1$ and $a$).\nHow many different values can $a$ have?',
      expl=['A number with exactly $3$ divisors is a prime squared: its divisors are $1$, $p$ and $p^2$.',
            'Prime squares below $150$: $2^2=4$, $3^2=9$, $5^2=25$, $7^2=49$, $11^2=121$. The next one, $13^2=169$, is too big.',
            'So there are $5$ values.'])

    # practice
    S('q-403', stem='Which of the following numbers has the greatest number of different divisors?',
      expl=['$13$ is prime: $2$ divisors.',
            '$66=2\\cdot3\\cdot11$: $(1+1)(1+1)(1+1)=8$ divisors.',
            '$55=5\\cdot11$: $2\\cdot2=4$ divisors. $87=3\\cdot29$ (a fake prime: $8+7=15$ divides by $3$): $4$ divisors.',
            'The answer is $66$.'])
    S('q-404', stem='$a$ and $b$ are prime numbers smaller than $20$, and $b<a$. What is the greatest possible value of $a-b$?',
      expl=['Take the greatest prime below $20$ and the smallest prime: $a=19$ and $b=2$.', '$a-b=19-2=17$.'])
    S('q-405', stem='A calculator shows the number $1$. Only two keys work: "$\\times2$" and "$\\times7$". You may press them as many times as you like. Which of the following numbers can you not reach?',
      expl=['Every number you can reach is built only from the primes $2$ and $7$.',
            '$28=2^2\\cdot7$ ✓, $56=2^3\\cdot7$ ✓, $49=7^2$ ✓.',
            '$42=2\\cdot3\\cdot7$ needs the prime $3$ ✗. So $42$ cannot be reached.'])
    S('q-406', stem='What is the sum of the greatest one-digit prime number and the greatest two-digit prime number?',
      expl=['The greatest one-digit prime is $7$ ($8$ and $9$ are not prime).',
            'The greatest two-digit prime is $97$ ($98$ is even and $99=9\\cdot11$).', '$7+97=104$.'])
    S('q-407', stem='Given: $x>44$. There are exactly $2$ prime numbers between $44$ and $x$ (not including $x$). Which of the following cannot be the value of $x$?',
      expl=['The primes above $44$: $47$, $53$, $59$. ($49=7^2$, $51=3\\cdot17$ and $57=3\\cdot19$ are not prime.)',
            'Exactly two primes: $47$ and $53$ are in, and $59$ is out. Therefore $53<x\\le59$.',
            '$54$, $56$ and $58$ work. $x=60$ puts $59$ inside too: three primes ✗.'])
    S('q-408', stem='$a$, $b$, $c$ are different positive integers, and $x=a\\cdot b^2\\cdot c^3$. Which of the following cannot be the value of $x$?',
      expl=['One of the numbers may be $1$.',
            '$24=6\\cdot2^2\\cdot1^3$ ✓ ($a=6$, $b=2$, $c=1$). $40=5\\cdot1^2\\cdot2^3$ ✓. $72=9\\cdot1^2\\cdot2^3$ ✓.',
            '$21=3\\cdot7$: if $c\\ge2$, then $c^3\\ge8$ must divide $21$ — impossible. So $c=1$.',
            'Then $b\\ne1$ (the numbers are different). $b^2$ must be $4$, $9$ or $16$ (bigger squares are more than $21$), and none of them divides $21$ ✗.',
            'So $x$ cannot be $21$.'])
    S('q-409', stem='$a$ is an odd one-digit prime, and $b$ is a two-digit prime smaller than $30$.\nGiven: $x=a\\cdot b$.\nWhich of the following gives the most precise range for $x$?',
      expl=['Odd one-digit primes: $3$, $5$, $7$. Two-digit primes below $30$: $11$, $13$, $17$, $19$, $23$, $29$.',
            'Smallest $x=3\\cdot11=33$. Greatest $x=7\\cdot29=203$.', 'So $33\\le x\\le203$.'])
    S('q-411', stem='Given: $x=2^2\\cdot5^3$. Which of the following numbers divides $x$ without remainder?',
      expl=['$75=3\\cdot5^2$: $x$ has no $3$ ✗.', '$8=2^3$: $x$ has only $2^2$ ✗.',
            '$50=2\\cdot5^2$: $x$ has $2^2$ and $5^3$ ✓.', '$200=2^3\\cdot5^2$: it needs $2^3$ ✗.'])
    S('q-412', stem='$p$ and $q$ are different prime numbers. Which of the following cannot be the difference between them?',
      expl=['All four choices are odd. An odd difference of two primes needs one even prime: $2$. So the bigger prime is the choice plus $2$.',
            '$21+2=23$ ✓, $9+2=11$ ✓, $15+2=17$ ✓ — all prime.',
            '$23+2=25=5^2$ is not prime ✗. So the difference cannot be $23$.'])
    S('q-413', stem='A number is called "interesting" if the sum of all the prime numbers from $2$ up to that number (including it) is a prime number. Which of the following numbers is "interesting"?',
      expl=['$4$: $2+3=5$, prime ✓.', '$5$ and $6$: $2+3+5=10$, not prime ✗.',
            '$11$: $2+3+5+7+11=28$, not prime ✗.', 'Only $4$ is "interesting".'])
    S('q-414', stem='$a$ and $b$ are integers.\nGiven: $a\\cdot b=75$.\nWhich of the following cannot be the value of $a-b$?',
      expl=['Pairs of factors of $75$: $1\\cdot75$, $3\\cdot25$, $5\\cdot15$.',
            'Their differences: $75-1=74$, $25-3=22$, $15-5=10$ (or the same numbers with a minus sign, if you swap the order).',
            'So $a-b$ can be $74$, $22$ or $10$, but not $15$.'])
    S('q-415', stem='$p$ and $q$ are prime numbers, and $p<q$. $p+q$ is also a prime number. Which of the following is necessarily true?',
      choices=['$p+q=13$', '$p=2$', '$p+7<q$', 'No such prime numbers exist.'],
      expl=['If $p$ and $q$ were both odd, $p+q$ would be even and bigger than $2$. It would not be prime.',
            'So one of them is the even prime $2$. Since $p<q$, $p=2$.',
            'Example: $p=2$, $q=3$, $p+q=5$. This rules out choice (1) ($5\\ne13$), choice (3) ($2+7>3$) and choice (4).'])
    S('q-417', stem='$n$ is a positive integer. The number of different positive divisors of $n$ (including $1$ and $n$) is odd. Which of the following is necessarily true?',
      choices=['$n$ is prime', '$n$ is odd', '$\\sqrt{n}$ is an integer', '$\\sqrt{n}$ is odd'],
      expl=['Divisors come in pairs: $d$ and $\\frac{n}{d}$. The count is odd only if one divisor is its own partner: $d=\\frac{n}{d}$, that is, $n=d^2$.',
            'So $n$ is a perfect square, and $\\sqrt{n}$ is an integer.',
            'The others are not necessarily true: $n=16$ has $5$ divisors, but $16$ is not prime, not odd, and $\\sqrt{16}=4$ is even.'])
    S('q-418', stem='Dana wrote a poem of $5$ lines. The first line has $20$ words. Each of the other lines has the smallest prime number of words that is greater than the number of words in the line before it. How many words are in the last line?',
      expl=['Line 1 has $20$ words. Line 2: the next prime after $20$ is $23$ ($21=3\\cdot7$, and $22$ is even).',
            'Line 3: $29$ ($25$ and $27$ are not prime). Line 4: $31$.',
            'Line 5: $37$ ($33$ and $35$ are not prime, and $32$, $34$, $36$ are even).'])
    S('q-419', stem='$n$ is a positive integer. The fraction $\\frac{n}{18}$ is in lowest terms (it cannot be reduced), and it is less than $1$. How many different values can $n$ have?',
      expl=['Less than $1$: $n<18$.',
            'Cannot be reduced: $n$ shares no prime with $18=2\\cdot3^2$. So $n$ is not divisible by $2$ or by $3$.',
            'From $1$ to $17$: $1$, $5$, $7$, $11$, $13$, $17$. That is $6$ values.'])
    S('q-421', stem='$n$ is a positive integer. $n^2$ has a divisor that is greater than $2n$ and different from $n^2$. What is the smallest possible value of $n$?',
      expl=['Check the choices, starting from the smallest.',
            '$n=4$: the divisors of $16$ are $1$, $2$, $4$, $8$, $16$. Only $16$ itself is greater than $8$ ✗.',
            '$n=5$: the divisors of $25$ are $1$, $5$, $25$. None fits ✗.',
            '$n=6$: the divisors of $36$ include $18$, and $18>12$ ✓. ($n=1$, $2$, $3$ fail like $4$ and $5$.)',
            'So the smallest $n$ is $6$.'])
    S('q-422', stem='Alan says: "Every number that is divisible by both $4$ and $6$ is also divisible by $24$."\nBeth says: "Every number that is divisible by both $4$ and $6$ is also divisible by $12$."\nWhich of the following is correct?',
      choices=['Only Alan is right.', 'Only Beth is right.', 'Both are right.', 'Both are wrong.'],
      expl=['$4=2^2$ and $6=2\\cdot3$. The LCM takes every prime at its higher power: $2^2\\cdot3=12$. So every such number divides by $12$: Beth is right.',
            'Alan is wrong: $12$ is divisible by $4$ and by $6$, but not by $24$.',
            '$24$ is just $4\\cdot6$. The product is too big because $4$ and $6$ share a factor of $2$.'])
    S('alg-extra-unit-t14-4-1', stem='What is the greatest common divisor (GCD) of $36$ and $54$?',
      choices=['$18$', '$9$', '$36$', '$108$'],
      expl=['$36=2^2\\cdot3^2$ and $54=2\\cdot3^3$.', 'GCD: each shared prime at its lower power: $2\\cdot3^2=18$.'])
    S('alg-extra-unit-t14-4-2', stem='What is the least common multiple (LCM) of $12$ and $18$?',
      choices=['$18$', '$72$', '$36$', '$6$'],
      expl=['$12=2^2\\cdot3$ and $18=2\\cdot3^2$.', 'LCM: every prime at its higher power: $2^2\\cdot3^2=36$.',
            'Check: $36=3\\cdot12=2\\cdot18$ ✓. ($72$ is a common multiple too, but not the least one.)'])
    S('alg-extra-unit-t14-4-3', stem='How many positive divisors does $2^3\\cdot3^2$ have?',
      choices=['$10$', '$12$', '$6$', '$8$'],
      expl=['Each exponent plus $1$, multiplied: $(3+1)(2+1)=4\\cdot3=12$.'])
    S('alg-extra-unit-t14-4-4', stem='Given: $p$ is an odd prime. What is the greatest common divisor of $p$ and $2p+1$?',
      choices=['$2$', '$3$', '$p$', '$1$'],
      expl=['The only divisors of the prime $p$ are $1$ and $p$.',
            '$2p+1$ divided by $p$ leaves a remainder of $1$, therefore $p$ does not divide $2p+1$.',
            'So the GCD is $1$. Check with $p=3$: the GCD of $3$ and $7$ is $1$ ✓.'])
    S('alg-extra-unit-t14-4-5', stem='Which of the following numbers is prime?',
      choices=['$29$', '$21$', '$27$', '$33$'],
      expl=['$21=3\\cdot7$, $27=3^3$, $33=3\\cdot11$.',
            '$29$: $\\sqrt{29}<6$, therefore try $2$, $3$, $5$. None of them divides $29$, therefore $29$ is prime.'])
    S('alg-extra-unit-t14-4-6', stem='What is the smallest positive integer $k$ such that $18k$ is a perfect square?',
      choices=['$2$', '$3$', '$6$', '$9$'],
      expl=['$18=2\\cdot3^2$. In a perfect square every exponent is even.',
            'The $2$ has exponent $1$, therefore it needs one more $2$: $k=2$.', 'Check: $18\\cdot2=36=6^2$ ✓.'])
    S('alg-extra-unit-t14-4-7', stem='$p$ and $q$ are prime numbers, and $p\\cdot q=91$. $p+q=?$',
      choices=['$21$', '$26$', '$20$', '$18$'],
      expl=['$91$ looks prime, but it is not: $\\sqrt{91}<10$, and $91=7\\cdot13$.',
            'So the primes are $7$ and $13$, and $7+13=20$.'])

    # =====================================================================================
    # 6. Originals restored in Pass 2 (they were removed as near-duplicates in pass 1)
    # =====================================================================================
    # Pass 2 (teacher-approved plan): the originals q-416, q-420 and q-410 are restored, with text clean-up only.
    S('q-416', stem='Given: $t>1$, and $t^2$ is a prime number. Which of the following is necessarily true about $t$?',
      choices=['$t$ is odd', '$t$ is even', '$t$ is not an integer', '$t$ is less than $5$'],
      expl=['If $t$ were an integer greater than $1$, then $t^2=t\\cdot t$ would break into two factors greater than $1$. It would not be prime.',
            'So $t$ is not an integer. Example: $t=\\sqrt2$ gives $t^2=2$, a prime.',
            '$t$ does not have to be small: $t=\\sqrt{97}$ gives $t^2=97$, a prime, and $\\sqrt{97}>9$. So choice 4 is not necessarily true.'])
    S('q-420', stem='$m$ is a positive integer. $m$ has exactly three different divisors (including $1$ and $m$). Which of the following is necessarily true about $\\sqrt{m}$?',
      choices=['$\\sqrt{m}$ is prime', '$\\sqrt{m}$ is even', '$\\sqrt{m}$ is divisible by $5$', '$\\sqrt{m}$ is not an integer'],
      expl=['Exactly three divisors means $m=p^2$ for a prime $p$. Its divisors are $1$, $p$ and $p^2$.',
            'Then $\\sqrt{m}=\\sqrt{p^2}=p$, a prime ✓.',
            'The others are not necessarily true: $m=9$ gives $\\sqrt{m}=3$, which is odd and not divisible by $5$. And $\\sqrt{m}=p$ is always an integer.'])
    S('q-410', stem='$p$, $q$, $r$ are different prime numbers.\nGiven:\n$\\begin{cases} M=p^2\\cdot q^3\\cdot r \\\\ N=p^3\\cdot q\\cdot r^2 \\end{cases}$\nWhat is the greatest common divisor (GCD) of $M$ and $N$?',
      choices=['$p\\cdot q\\cdot r$', '$p^2\\cdot q\\cdot r$', '$p^3\\cdot q^3\\cdot r^2$', '$p^2\\cdot q^3\\cdot r^2$'],
      expl=['GCD: take each prime that is in both numbers, at its LOWER power.',
            '$p$: $p^2$ and $p^3$ → $p^2$. $q$: $q^3$ and $q$ → $q$. $r$: $r$ and $r^2$ → $r$.',
            'GCD $=p^2\\cdot q\\cdot r$. (Choice 3 takes the higher powers: that is the LCM.)'])

    # =====================================================================================
    # 7. New guided question (section A): the square-root test
    # =====================================================================================
    M.new_q(G[0], TOPIC, 'Which of the following numbers is prime?', ['$91$', '$119$', '$113$', '$133$'], 3, [
        'Test each number with the primes up to its square root.',
        '$91=7\\cdot13$, $119=7\\cdot17$ and $133=7\\cdot19$. None of them is prime.',
        '$113$: $10^2=100<113<121=11^2$, therefore $\\sqrt{113}<11$. Try $2$, $3$, $5$, $7$.',
        '$113$ is odd. Its digit sum is $1+1+3=5$, therefore $3$ does not divide it. It does not end in $0$ or $5$. $113=7\\cdot16+1$, therefore $7$ does not divide it.',
        'No prime up to $\\sqrt{113}$ divides it, therefore $113$ is prime.'])
    M.place_q(G[0], 'primes-a', after='solve-q-388')
    _solution(M, G[0], 'Prime Questions', M.video('solve-q-386')['hybrid']['num'],
              ["Three of these are fakes. Only one is really prime."], [
        ('Test up to the root', [
            "Test each one: divide by the primes up to its square root.",
            D('Next to choice 1 write "91 = 7 · 13 ✗"'),
            "Ninety-one: seven times thirteen. A fake.",
            D('Next to choice 2 write "119 = 7 · 17 ✗"'),
            "A hundred nineteen: seven times seventeen. Another fake.",
            D('Next to choice 4 write "133 = 7 · 19 ✗"'),
            "A hundred thirty-three: seven times nineteen. Seven again!",
            D('Next to choice 3 write "√113 < 11 → try 2, 3, 5, 7"'),
            "A hundred thirteen. Ten squared is a hundred, eleven squared is a hundred twenty-one. So the root is less than eleven.",
            "Try two, three, five and seven.",
            D('Write "odd · 1 + 1 + 3 = 5 · no 0 or 5 · 113 = 7 · 16 + 1"'),
            "It's odd — not two. The digit sum is five — not three. It doesn't end in zero or five. Seven times sixteen is a hundred twelve — remainder one. Not seven.",
            D('Circle choice 3'),
            "No prime divides it. A hundred thirteen is prime. Choice three.",
            "Notice: all three fakes divided by seven. Never forget to try seven.",
        ]),
    ], 'primes-a', after=G[0])

    # =====================================================================================
    # 8. New lesson video (start of the advanced section): squares, prime equations, prime in a product
    # =====================================================================================
    first_adv = 'q-391'
    sb = ['Perfect squares', 'Prime equations', 'A prime in a product', 'Recap']
    v = M.new_video(TRICKS, TOPIC, 'More Factor Tools', sb, [
        dict(mode='title', title='More Factor Tools', script=[
            "More factor tools.",
            "Three quick tools the exam loves. Each one starts the same way: break the number into primes.",
        ]),
        dict(mode='concept', active=0, title='Perfect squares', script=[
            "When is a number a perfect square — a whole number times itself?",
            A('36 = 2² · 3² appears', T('$36=2^2\\cdot3^2$ — a square', size=48, gap=20)),
            "Thirty-six is two squared times three squared. Every exponent is even. That's a perfect square: six times six.",
            A('18 = 2 · 3² appears', T('$18=2\\cdot3^2$ — not a square', size=48, gap=30)),
            "Eighteen is two times three squared. The two has exponent one — odd. Not a square.",
            A("'Square: every exponent even' appears",
              T('Perfect square: every exponent is even', size=40, gap=30)),
            "The rule: in a perfect square every exponent is even.",
            "Classic question: the smallest k so that eighteen k is a perfect square.",
            D('Write "18k = 2 · 3² · k → k = 2 → 36 = 6² ✓"'),
            "The two is missing one copy. So k is two. Eighteen times two is thirty-six — six squared.",
        ]),
        dict(mode='concept', active=1, title='Prime equations', script=[
            "Every number breaks into primes in exactly ONE way. That solves equations.",
            A('2ᵃ · 3ᵇ = 72 appears', T('$2^a\\cdot3^b=72$   ($a$, $b$ integers)', size=50, gap=60)),
            D('Write "72 = 2³ · 3²  →  a = 3, b = 2"'),
            "Seventy-two is two cubed times three squared. There's no other way to build it. So a is three and b is two.",
            A('p² · q = 50 appears', T('$p$, $q$ primes:  $p^2\\cdot q=50$', size=50, gap=60)),
            D('Write "50 = 5² · 2  →  p = 5, q = 2"'),
            "Fifty is five squared times two. The squared prime is five. So p is five, and q is two.",
            "Careful with the order: p is the one that's squared. p equals two would give four times q — and fifty over four isn't whole.",
            "The method: break the number into primes, then match prime by prime, exponent by exponent.",
        ]),
        dict(mode='concept', active=2, title='A prime in a product', script=[
            "Last tool. If a PRIME divides a product, it divides one of the factors.",
            A("'7 divides a · b → 7 divides a or b' appears", T('$7$ divides $a\\cdot b$  $\\to$  $7$ divides $a$ or $b$', size=46, gap=60)),
            "Seven divides a times b? Then seven is inside a, or inside b. A prime can't be split between them.",
            A("'6 divides 4 · 9, but not 4 and not 9' appears", T('$6$ divides $4\\cdot9=36$, but not $4$ and not $9$', size=46, gap=40)),
            "This works only for primes. Six divides thirty-six, which is four times nine. But six divides neither four nor nine.",
            "The two came from the four, and the three came from the nine.",
            "So: with a prime, one of the factors must hold it. With a number that isn't prime, break it into primes first.",
        ]),
        dict(mode='concept', active=3, title='Recap', script=[
            "Let's lock it in.",
            A("'Square: all exponents even' appears",
              T('Perfect square: all exponents even', size=38)),
            A("'Only one way to break into primes → match the exponents' appears",
              T('Only one way to break into primes $\\to$ match the exponents', size=38)),
            A("'A prime divides a product → it divides one of the factors' appears",
              T('A prime divides a product $\\to$ it divides one of the factors', size=38)),
            D('Tick each line'),
            "There's a card with these three tools right after this video. Then the advanced questions. Try each one first — then watch.",
        ]),
    ], 'primes-advanced', before=first_adv)
    v['hybrid']['num'] = M.video('solve-q-391')['hybrid']['num']

    M.new_card('mem-r26-t14-more-tools', TOPIC, 'primes-advanced', {
        'title': 'More factor tools',
        'intro': 'Three tools. Each one starts with breaking the number into primes.',
        'tables': [{'title': '', 'head': ['Tool', 'Rule', 'Example'], 'rows': [
            ['Perfect square', 'every exponent is even', '$18k$ a square: $18=2\\cdot3^2$ → $k=2$ ($36=6^2$)'],
            ['Prime equation', 'break into primes, then match the exponents', '$2^a\\cdot3^b=72=2^3\\cdot3^2$ → $a=3$, $b=2$'],
            ['A prime divides a product', 'it divides one of the factors', '$7$ divides $a\\cdot b$ → $7$ divides $a$ or $b$'],
        ]}],
        'tips': ['Only for primes: $6$ divides $4\\cdot9=36$, but $6$ divides neither $4$ nor $9$.',
                 'In "not necessarily true" questions, a statement that is never true is also not necessarily true.'],
    }, after=TRICKS)

    # =====================================================================================
    # 9. New guided question (advanced section): prime equation
    #    (Pass 2: the cube and zeros guided questions q-r26-t14-02 / -04 were removed)
    # =====================================================================================
    adv_num = M.video('solve-q-391')['hybrid']['num']
    M.new_q(G[2], TOPIC, '$a$ and $b$ are positive integers.\nGiven: $2^a\\cdot3^b=108$.\n$a-b=?$', ['$1$', '$-1$', '$2$', '$5$'], 2, [
        'Break $108$ into primes: $108=4\\cdot27=2^2\\cdot3^3$.',
        'A number breaks into primes in only one way, therefore match the exponents: $2^a\\cdot3^b=2^2\\cdot3^3$ gives $a=2$ and $b=3$.',
        '$a-b=2-3=-1$. (Swapping $a$ and $b$ gives $1$ — the trap.)'])
    M.place_q(G[2], 'primes-advanced', after='mem-r26-t14-more-tools')
    _solution(M, G[2], 'Advanced Primes', adv_num, ["An equation with primes. Break, then match."], [
        ('Break and match', [
            "A number breaks into primes in only one way. So break a hundred eight.",
            D('Write "108 = 4 · 27 = 2² · 3³"'),
            "A hundred eight is four times twenty-seven. Two squared times three cubed.",
            D('Write "2ᵃ · 3ᵇ = 2² · 3³ → a = 2, b = 3"'),
            "Match prime by prime. The twos: a is two. The threes: b is three.",
            D('Write "a − b = 2 − 3 = −1"'),
            "a minus b: two minus three. Minus one.",
            D('Circle choice 2'),
            "Choice two. Choice one is the trap — it swaps a and b.",
        ]),
    ], 'primes-advanced', after=G[2])

    # =====================================================================================
    # 10. Sidebars and titles of all solution videos (numbers are renumbered in course order by the build)
    # =====================================================================================
    groupA = ['solve-q-386', 'solve-q-387', 'solve-q-388', 'solve-' + G[0]]
    groupB = ['solve-q-389', 'solve-q-390', 'solve-q-398', 'solve-q-399', 'solve-q-400', 'solve-q-401', 'solve-q-402']
    groupC = ['solve-' + G[2]] + ['solve-q-%d' % k for k in range(391, 398)]
    for grp in (groupA, groupB, groupC):
        labels = [M.video(v)['beats'][0]['bigTitle'] for v in grp]
        for k, vid in enumerate(grp):
            M.set_sidebar(vid, labels)
            for b in M.video(vid)['beats']:
                if b['mode'] != 'title': b['active'] = k
    for vid in groupA + groupB + groupC:
        V = M.video(vid); q = M.q(V['questionId'])
        V['title'] = V['navLabel'] = q['stem']
        for b in V['beats']:
            if b.get('canvas', '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (q['id'], q['stem'])

    M.section_title('primes-a', 'Prime numbers · theory A')
    M.section_title('primes-b', 'Factor tools · theory B')

    # =====================================================================================
    # 11. New practice questions
    # =====================================================================================
    NP = {}
    NP[5] = ('How many prime numbers are there between $80$ and $100$?', ['$2$', '$3$', '$4$', '$5$'], 2, [
        'Even numbers and numbers ending in $5$ are not prime. That leaves $81$, $83$, $87$, $89$, $91$, $93$, $97$, $99$.',
        'Fakes: $81=9^2$, $87=3\\cdot29$, $91=7\\cdot13$, $93=3\\cdot31$, $99=9\\cdot11$.',
        '$83$, $89$ and $97$: the root is less than $10$, and $2$, $3$, $5$, $7$ do not divide them. They are prime.',
        'So there are $3$ primes.'])
    NP[6] = ('What is the sum of all the prime numbers between $50$ and $60$?', ['$112$', '$163$', '$169$', '$220$'], 1, [
        'The odd numbers between $50$ and $60$ that do not end in $5$: $51$, $53$, $57$, $59$.',
        '$51=3\\cdot17$ and $57=3\\cdot19$ are fakes ($5+1=6$ and $5+7=12$ divide by $3$).',
        '$53$ and $59$: the root is less than $8$, and $2$, $3$, $5$, $7$ do not divide them. They are prime.',
        'Sum: $53+59=112$.'])
    NP[7] = ('$n$ is an integer, and $1<n<120$. $n$ is not divisible by $2$, $3$, $5$ or $7$. Which of the following is necessarily true?',
             ['$n$ is prime.', '$n<100$', 'The last digit of $n$ is $1$, $3$ or $7$.', '$n>11$'], 1, [
        'If $n$ were not prime, it would break into two factors, and the smaller one would be at most $\\sqrt{n}<\\sqrt{121}=11$.',
        'Then $n$ would have a prime factor smaller than $11$: $2$, $3$, $5$ or $7$. But none of them divides $n$. So $n$ is prime ✓.',
        'The others are not necessarily true: $n=113$ is not less than $100$; $n=19$ ends in $9$; $n=11$ is not greater than $11$.'])
    NP[9] = ('$p$ and $q$ are different prime numbers.\nGiven:\n$\\begin{cases} M=p^3\\cdot q \\\\ N=p^2\\cdot q^4 \\end{cases}$\nWhat is the least common multiple (LCM) of $M$ and $N$?',
             ['$p^2\\cdot q$', '$p^3\\cdot q^4$', '$p^5\\cdot q^5$', '$p^3\\cdot q$'], 2, [
        'LCM: every prime at its higher power.',
        '$p$: $p^3$ and $p^2$ → $p^3$. $q$: $q$ and $q^4$ → $q^4$.',
        'LCM $=p^3\\cdot q^4$. ($p^2\\cdot q$ is the GCD, and $p^5\\cdot q^5=M\\cdot N$ is too big.)'])
    NP[10] = ('$k$ is a positive integer, and $2^3\\cdot3^4\\cdot5\\cdot k$ is a perfect square. What is the smallest possible value of $k$?',
              ['$2$', '$5$', '$10$', '$30$'], 3, [
        'In a perfect square every exponent is even.',
        '$2^3$: odd exponent, needs one more $2$. $3^4$: even ✓. $5^1$: odd, needs one more $5$.',
        '$k=2\\cdot5=10$. Check: $2^4\\cdot3^4\\cdot5^2=(2^2\\cdot3^2\\cdot5)^2=180^2$ ✓.'])
    NP[12] = ('$p$ and $q$ are prime numbers.\nGiven: $p^2\\cdot q=75$.\n$p+q=?$', ['$8$', '$15$', '$28$', '$34$'], 1, [
        'Break $75$ into primes: $75=3\\cdot25=3\\cdot5^2$.',
        'The prime that is squared is $5$, therefore $p=5$ and $q=3$.',
        '$p+q=5+3=8$. (The trap: $p=3$ and $q=5$ give $3^2\\cdot5=45$, not $75$.)'])
    NP[13] = ('$x$ and $y$ are positive integers.\nGiven: $6^x\\cdot5^y=1080$.\n$x+y=?$', ['$3$', '$4$', '$5$', '$6$'], 2, [
        'Break into primes: $1080=8\\cdot135=8\\cdot27\\cdot5=2^3\\cdot3^3\\cdot5$.',
        '$6^x=2^x\\cdot3^x$, therefore $2^x\\cdot3^x\\cdot5^y=2^3\\cdot3^3\\cdot5^1$.',
        'Match the exponents: $x=3$ and $y=1$. So $x+y=4$.'])
    NP[15] = ('$a$ and $b$ are positive integers, and $a\\cdot b$ is divisible by $14$. Which of the following is necessarily true?',
              ['$a$ or $b$ is divisible by $7$.', '$a$ or $b$ is divisible by $14$.', '$a$ is even.', '$a\\cdot b$ is divisible by $28$.'], 1, [
        '$14=2\\cdot7$, and $7$ is prime. A prime that divides a product divides one of the factors. So $a$ or $b$ is divisible by $7$ ✓.',
        'The others are not necessarily true: $a=2$ and $b=7$ give $a\\cdot b=14$. Neither number is divisible by $14$, and $14$ is not divisible by $28$.',
        '$a=7$ and $b=2$ show that $a$ does not have to be even.'])
    for k, (stem, ch, cor, ex) in NP.items():
        M.new_q(P(k), TOPIC, stem, ch, cor, ex)
        M.place_q(P(k), 'unit-t14-4')

    # =====================================================================================
    # 12. Practice order: easy -> hard
    # =====================================================================================
    E = 'alg-extra-unit-t14-4-%d'
    M.practice_order('unit-t14-4', [
        E % 5, E % 3, E % 1, E % 2, E % 7, 'q-404', 'q-406', 'q-411', E % 6, 'q-405', P(5), P(6), 'q-409',
        'q-413', 'q-418', 'q-403', E % 4, 'q-412', 'q-410', P(9), P(12), P(10), 'q-414', 'q-419', 'q-407',
        P(13), P(15), 'q-415', 'q-416', 'q-420', 'q-417', 'q-422', P(7), 'q-408', 'q-421'])

    # =====================================================================================
    # 13. Pass 2: summary lesson right before the independent practice
    # =====================================================================================
    summary(M)

    # =====================================================================================
    # 14. 2026-10-05 cut repeats: lessons back to a short intro (see t14_CHANGES.md)
    # =====================================================================================
    cut_repeats(M)


SUMMARY_SB = ['What a prime is', 'Two primes, odd result', 'Is it prime?', 'Break it down', 'GCD and LCM',
              'Counting divisors', 'Squares and equations', 'A prime in a product', 'Before you practice']


def summary(M):
    def s(k, title, script):
        return dict(mode='concept', active=k, title=title, script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of primes and factors.",
            "Everything important, in a few minutes.",
        ]),
        s(0, 'What a prime is', [
            A("'Prime: only 1 and itself' appears", T('Prime: divides only by $1$ and itself', size=44, gap=30)),
            "A prime divides only by one and by itself.",
            A("'0, 1 and negatives are not prime' appears", T('$0$, $1$ and negative numbers are not prime', size=42, gap=20)),
            A("'2 is the only even prime' appears", T('$2$ is the only even prime', size=42, gap=30)),
            "One is not prime. Two is — and it's the only even prime.",
            A("'Know the primes up to 40 — and 97' appears", T('Know the primes up to $40$ — and $97$', size=44)),
            "Know them by heart: two, three, five, seven, eleven… up to thirty-seven. And ninety-seven, the largest two-digit prime.",
        ]),
        s(1, 'Two primes, odd result', [
            A("'Odd sum or difference → one of them is 2' appears", T('Two primes, odd sum or difference $\\to$ one of them is $2$', size=42, gap=40)),
            "All the other primes are odd. Odd plus odd is even. Odd minus odd is even too.",
            "So an odd sum or an odd difference means one of the primes is two.",
            D('Write "39 = 2 + 37"'),
            "Thirty-nine as a sum of two primes? Two plus thirty-seven.",
        ]),
        s(2, 'Is it prime?', [
            A("'Try the primes up to √n' appears", T('Is $n$ prime? Try the primes up to $\\sqrt{n}$', size=44, gap=30)),
            "To test a number, divide it by the primes up to its square root. No further.",
            A('The fake primes appear', T('Fake primes: $69=3\\cdot23$,   $77=7\\cdot11$,   $161=7\\cdot23$', size=40)),
            "Watch out for the fakes. For three, add the digits. And never forget to try seven.",
        ]),
        s(3, 'Break it down', [
            A('44 = 2 · 2 · 11 appears', T('$44=2\\cdot2\\cdot11$ $\;\\to\;$ divides by $2,\\ 4,\\ 11,\\ 22,\\ 44$', size=44, gap=30)),
            "Break every number into primes. It divides by every combination of its prime factors.",
            A("'Test a divisor: its prime ingredients' appears", T('Is it a divisor? Check its prime ingredients', size=44, gap=30)),
            "To test a divisor, break it into primes too. Unpack bases like six or ten squared first.",
            A("'Which prime is missing?' appears", T('Break apart · build · which prime is missing?', size=44)),
            "Most questions are just this: break a number apart, or build it — and look for the missing prime.",
        ]),
        s(4, 'GCD and LCM', [
            A('GCD rule appears', T('GCD: shared primes, each at its LOWER power', size=42, gap=20)),
            A('LCM rule appears', T('LCM (guaranteed divisor): every prime at its HIGHER power', size=40, gap=30)),
            D('Write "48 = 2⁴ · 3, 60 = 2² · 3 · 5 → GCD = 12, LCM = 240"'),
            "Forty-eight and sixty: the GCD is twelve, the LCM is two hundred forty.",
            A('GCD · LCM = a · b appears', T('GCD $\\cdot$ LCM $=a\\cdot b$', size=44)),
            "The trap: just multiplying the two numbers. That's too big when they share a prime.",
        ]),
        s(5, 'Counting divisors', [
            A("'Each exponent + 1, multiplied' appears", T('$2^4\\cdot3$ $\;\\to\;$ $(4+1)(1+1)=10$ divisors', size=44, gap=30)),
            "Number of divisors: add one to each exponent, and multiply.",
            A("'Odd number of divisors → a perfect square' appears", T('Odd number of divisors $\\to$ a perfect square', size=44, gap=30)),
            "Divisors come in pairs. Only a perfect square has one without a partner.",
            A("'Exactly 3 → a prime squared' appears", T('Exactly $3$ divisors $\\to$ a prime squared', size=44)),
            "Exactly three divisors: a prime squared, like four or one hundred twenty-one.",
        ]),
        s(6, 'Squares and equations', [
            A("'Perfect square: every exponent even' appears", T('Perfect square: every exponent even', size=42, gap=30)),
            "In a perfect square every exponent is even.",
            D('Write "20k a square: 20 = 2² · 5 → k = 5 → 100 = 10²"'),
            "Twenty is two squared times five — it needs one more five. k is five.",
            A('2ᵃ · 3ᵇ = 144 appears', T('$2^a\\cdot3^b=144=2^4\\cdot3^2$ $\;\\to\;$ $a=4$, $b=2$', size=42)),
            "A number breaks into primes in only one way. Break it, then match the exponents.",
        ]),
        s(7, 'A prime in a product', [
            A("'A prime divides a · b → it divides a or b' appears", T('A prime divides $a\\cdot b$ $\;\\to\;$ it divides $a$ or $b$', size=42, gap=30)),
            "A prime can't be split between two factors. One of them holds it.",
            A("'Letters as primes? Plug in 2, 3, 5, 7' appears", T('Letters as primes? Plug in $2,\\ 3,\\ 5,\\ 7$', size=42)),
            "And when the primes are letters, plug in the smallest primes — then check every choice.",
        ]),
        s(8, 'Before you practice', [
            "Before each question, ask yourself:",
            A("'Did I break it into primes?' appears", T('Did I break every number into primes?', size=42)),
            A("'Is it really prime?' appears", T('Is it really prime? Did I try up to the root — and $7$?', size=42)),
            A("'An odd sum of primes?' appears", T('An odd sum or difference? Then one prime is $2$.', size=42)),
            A("'GCD or LCM?' appears", T('GCD or LCM? Lower power or higher power?', size=42)),
            "The common traps: calling one a prime, forgetting two, and multiplying instead of taking the LCM.",
            "That's it. Now go practice.",
        ]),
    ]
    v = M.new_video('r26-t14-summary', TOPIC, 'Prime Numbers — Summary', SUMMARY_SB, slides,
                    'primes-advanced', after='solve-q-397')
    v['hybrid']['num'] = M.video('solve-q-397')['hybrid']['num']


# =====================================================================================
# 2026-10-05 cut repeats
# =====================================================================================
def _script_of(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _add_line(M, vid, n, anchor, new, where='after'):
    """Insert script entries `new` before/after the spoken line containing `anchor` (None = at the end)."""
    sc = _script_of(M, vid, n); out = []; hit = anchor is None
    for x in sc:
        if not hit and isinstance(x, str) and anchor in x:
            hit = True
            out += ([x] + new) if where == 'after' else (new + [x]); continue
        out.append(x)
    if anchor is None: out += new
    assert hit, '%s #%d: not found: %s' % (vid, n, anchor)
    M.set_slide(vid, n, script=out)


def _set_say(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = new; return lines
        raise AssertionError('%s #%d: not found: %s' % (vid, n, old))
    M.edit_lines(vid, n, fn)


def cut_repeats(M):
    # ---- "Factor Tools": keep the intro, "Break & build" (the frame of the section) and "Counting divisors"
    #      (no question video teaches it). GCD, LCM, GCD vs LCM, symmetric divisors -> taught in Q5, Q6, Q11.
    vid = LESSON_B
    titles = [b['title'] for b in M.video(vid)['beats']]
    assert titles[1:] == ['Greatest common (GCD)', 'Greatest guaranteed (LCM)', 'GCD vs LCM', 'Break & build',
                          'Symmetric divisors', 'Counting divisors', 'Recap'], titles
    M.remove_slides(vid, [2, 3, 4, 6, 8])
    M.set_slide(vid, 1, script=[
        'Factor tools.',
        'In this section: questions about the factors of a number.',
        'The greatest common divisor, the greatest guaranteed divisor — and long stories that hide a simple factor question.',
        'Each question that follows teaches one tool.'])
    M.set_slide(vid, 2, active=0)
    M.set_slide(vid, 3, active=1)
    _set_say(M, vid, 3, 'One more tool: counting ALL', 'One tool no question here uses — but the practice does: counting ALL the divisors.')
    _add_line(M, vid, 3, None, ['The factor tools card comes right after this video. Then seven questions.'])
    M.set_sidebar(vid, ['Break & build', 'Counting divisors'])

    # Q5 (q-389): say what the GCD is (was only in the lesson)
    _set_say(M, 'solve-q-389', 2, 'The GCD: which primes are in BOTH',
             'The GCD is the biggest number that divides both. Which primes are in BOTH numbers — and at what power?')
    # Q6 (q-390): the official name LCM + GCD · LCM = a · b (was only in the lesson)
    _set_say(M, 'solve-q-390', 1, "that's the LCM",
             'The greatest GUARANTEED divisor. Its official name: the least common multiple — LCM.')
    _add_line(M, 'solve-q-390', 2, 'Check: twenty-four itself', [
        A("'GCD · LCM = a · b' appears", T('GCD $\\cdot$ LCM $=a\\cdot b$:  $4\\cdot24=8\\cdot12=96$', size=40)),
        'A bonus fact: the GCD times the LCM equals the two numbers multiplied. The GCD here is four — four times twenty-four is ninety-six.'])
    # Q11 (q-402): no lesson slide to point back to; give the general rule in one line
    _set_say(M, 'solve-q-402', 1, 'Remember the symmetric divisors?', 'Divisors come in pairs — here is where that pays off.')
    _add_line(M, 'solve-q-402', 2, 'Three divisors means one sits in the middle', [
        A("'Odd number of divisors → perfect square' appears", T('Odd number of divisors $\\to$ a perfect square', size=40)),
        'In general: an odd number of divisors means a perfect square — the middle divisor times itself.'])

    # ---- "More Factor Tools": prime equations -> taught in Q12; a prime in a product -> Q17 (one line added).
    #      Perfect squares stays (no question video teaches it).
    vid = TRICKS
    titles = [b['title'] for b in M.video(vid)['beats']]
    assert titles[1:] == ['Perfect squares', 'Prime equations', 'A prime in a product', 'Recap'], titles
    M.remove_slides(vid, [3, 4, 5])
    M.set_slide(vid, 1, script=[
        'More factor tools.',
        'In this section: harder prime questions. Almost every one starts the same way: break the number into primes.',
        "First, one tool that no question here teaches: perfect squares."])
    # the lesson example must not equal practice question alg-extra-unit-t14-4-6 (18k): use 12k
    def fn(lines):
        for l in lines:
            if l.get('say', '').startswith('Classic question: the smallest k so that eighteen k'):
                l['say'] = 'Classic question: the smallest k so that twelve k is a perfect square.'
            if l.get('say', '').startswith('The two is missing one copy.'):
                l['say'] = 'The three is missing one copy. So k is three. Twelve times three is thirty-six — six squared.'
            if l.get('draw', '').startswith('Write "18k = 2'):
                l['draw'] = 'Write "12k = 2² · 3 · k → k = 3 → 36 = 6² ✓"'
        return lines
    M.edit_lines(vid, 2, fn)
    _add_line(M, vid, 2, None, ['There\'s a card with the factor tools right after this video. Then the advanced questions. Try each one first — then watch.'])
    M.set_sidebar(vid, ['Perfect squares'])
    M.card('mem-r26-t14-more-tools')['tables'][0]['rows'][0][2] = '$12k$ a square: $12=2^2\\cdot3$ → $k=3$ ($36=6^2$)'
    # Q17 (q-395): the "prime in a product" rule, at the moment it is used
    _add_line(M, 'solve-q-395', 2, 'So at least one of them brings the three', [
        A("'A prime divides a · b → it divides a or b' appears", T('A prime divides a product $\\to$ it divides one of the factors', size=38)),
        "That's the rule: a prime can't be split between factors — one of them holds it. Fifteen isn't prime, so its three and its five may come from different numbers."], where='after')


# =====================================================================================================================
# 2026-10-06 renumber pass: the English course must not look like the Hebrew one. Every Hebrew-derived question
# (guided q-386 ... q-402, practice q-403 ... q-422) gets new numbers / letters / a tweaked story - same idea, same
# trap, same methods - and every guided solution video is rewritten to match. The Hebrew lesson examples get new
# numbers too (lesson "Prime Numbers", lesson "Factor Tools", the two memory cards).
# Order: theory A easy -> hard (q-387, q-r26-t14-01, q-388, q-386); advanced: q-396 before q-394.
# Practice clean-up: the copy alg-extra-unit-t14-4-5 out, extra warm-ups down to 2, September items kept only where
# the Hebrew practice lacks the type. Nothing in topic 14 is recorded (checked ~/Documents/Course.recordings
# 2026-10-06). Runs last. See t14_CHANGES.md ("2026-10-06 renumber pass") for the old -> new table.
# =====================================================================================================================
def _sub(M, vid, n, pairs):
    """Replace exact text on one slide (board items, row items, spoken lines, draw cues, labels). Every pair must hit."""
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = 0
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit += 1
            if it.get('items'):
                for k, x in enumerate(it['items']):
                    if old in x: it['items'][k] = x.replace(old, new); hit += 1
        for l in b['lines']:
            for k in ('say', 'draw', 'label'):
                if k in l and old in l[k]: l[k] = l[k].replace(old, new); hit += 1
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    b['loads'] = ''; b['canvas'] = ''
    M.touched_videos.add(vid)


def renumber(M):
    RECORDED = set()   # nothing in topic 14 is recorded

    def S(qid, **kw):
        if qid in RECORDED: return
        M.set_q(qid, **kw)

    def video(qid, slides):
        if qid in RECORDED: return
        vid = 'solve-' + qid
        b0 = M.slide(vid, 1); keep = (b0['title'], b0['bigTitle'])
        for n, script in slides.items(): M.set_slide(vid, n, script=script)
        b0 = M.slide(vid, 1); b0['title'], b0['bigTitle'] = keep   # group name stays the slide title
        v = M.video(vid); v['title'] = v['navLabel'] = M.q(qid)['stem']
        M.touched_videos.add(vid)

    def qword(vid):   # the spoken "Question N" uses the video's current number; renumber_guided maps it at build
        return _word(int(M.video(vid)['beats'][0]['bigTitle'].split()[1]))

    # ============================== lesson "Prime Numbers": the Hebrew lesson's own examples -> new numbers
    L = LESSON_A
    _sub(M, L, 2, [('$13$', '$17$'), ('$14$', '$15$'), ('13 and 14', '17 and 15'),
                   ('Under 13 write "can\'t break"; under 14 write "= 2 · 7"', 'Under 17 write "can\'t break"; under 15 write "= 3 · 5"'),
                   ('Thirteen? You can\'t break it. Prime.', 'Seventeen? You can\'t break it. Prime.'),
                   ('Fourteen? Two times seven. It breaks — not prime.', 'Fifteen? Three times five. It breaks — not prime.'),
                   ('Same with ten — two times five. Eight — two times four, or two times two times two. Six — two times three. They all break.',
                    'Same with nine — three times three. Twelve — three times four, or two times two times three. Four — two times two. They all break.'),
                   ('Seven, five, three, two — none of them break either. All prime.',
                    'Thirteen, eleven, seven — none of them break either. All prime.')])
    _sub(M, L, 4, [('the primes between thirty and forty', 'the primes between twenty and thirty'),
                   ('Next to 31 and 37, tick them; write "32–36, 38, 39 ✗"', 'Next to 23 and 29, tick them; write "21, 22, 24–28 ✗"'),
                   ('Thirty-one yes. Thirty-two, three, four, five, six — no. Thirty-seven yes. Thirty-eight, thirty-nine — no.',
                    'Twenty-one, twenty-two — no. Twenty-three yes. Twenty-four up to twenty-eight — no. Twenty-nine yes.')])
    _sub(M, L, 6, [('$20 \\div 4 = 5$', '$24 \\div 3 = 8$'), ('$30 \\div 6 = 5$', '$35 \\div 7 = 5$'),
                   ("'20 divides by 4' appears", "'24 divides by 3' appears"), ("'30 divides by 6' appears", "'35 divides by 7' appears"),
                   ('"4 is a factor of 20"', '"3 is a factor of 24"'), ('"6 is a factor of 30"', '"7 is a factor of 35"'),
                   ('Twenty divides by four — so four is a factor of twenty. A divisor of twenty.',
                    'Twenty-four divides by three — so three is a factor of twenty-four. A divisor of twenty-four.'),
                   ('Thirty divides by six — six is a factor of thirty.', 'Thirty-five divides by seven — seven is a factor of thirty-five.')])
    b = M.slide(L, 7)
    assert b['items'][1]['items'] == ['$2$', '$3$', '$4$', '$6$', '$12$'], b['items'][1]
    b['items'][1]['items'] = ['$2$', '$3$', '$6$', '$9$', '$18$']
    _sub(M, L, 7, [('$12=2\\cdot2\\cdot3$', '$18=2\\cdot3\\cdot3$'), ('12 = 2 · 2 · 3 appears', '18 = 2 · 3 · 3 appears'),
                   ('The divisors of 12 appear: 2, 3, 4, 6, 12', 'The divisors of 18 appear: 2, 3, 6, 9, 18'),
                   ('Twelve breaks into two times two times three.', 'Eighteen breaks into two times three times three.'),
                   ('But twelve also divides by four, by six, by twelve.', 'But eighteen also divides by six, by nine, by eighteen.'),
                   ('Under 4 write "2·2"; under 6 write "2·3"; under 12 write "2·2·3"', 'Under 6 write "2·3"; under 9 write "3·3"; under 18 write "2·3·3"'),
                   ('Four is two times two. Six is two times three. Twelve is all of them.', 'Six is two times three. Nine is three times three. Eighteen is all of them.')])
    _sub(M, L, 8, [('$126$', '$150$'), ('126 appears', '150 appears'), ('Take one hundred twenty-six.', 'Take one hundred fifty.'),
                   ('126 → 2 and 63; 63 → 3 and 21; 21 → 3 and 7', '150 → 2 and 75; 75 → 3 and 25; 25 → 5 and 5'),
                   ('Two times sixty-three. Sixty-three is three times twenty-one. Twenty-one is three times seven.',
                    'Two times seventy-five. Seventy-five is three times twenty-five. Twenty-five is five times five.'),
                   ("Twenty-one isn't a leaf yet — seven is.", "Twenty-five isn't a leaf yet — five is."),
                   ('"126 = 2 · 3² · 7"', '"150 = 2 · 3 · 5²"'),
                   ('So one hundred twenty-six is two, times three squared, times seven.', 'So one hundred fifty is two, times three, times five squared.'),
                   ('Start with six times twenty-one instead?', 'Start with ten times fifteen instead?')])
    b = M.slide(L, 9)
    assert b['items'][1]['items'] == ['$18=2\\cdot3^2$', '$12=2^2\\cdot3$'], b['items'][1]
    b['items'][1]['items'] = ['$50=2\\cdot5^2$', '$20=2^2\\cdot5$']
    _sub(M, L, 9, [('$126=2\\cdot3^2\\cdot7$', '$150=2\\cdot3\\cdot5^2$'), ('126 = 2 · 3² · 7 appears', '150 = 2 · 3 · 5² appears'),
                   ('18 = 2 · 3² and 12 = 2² · 3', '50 = 2 · 5² and 20 = 2² · 5'), ('Tick 18; cross 12 and circle the 2²', 'Tick 50; cross 20 and circle the 2²'),
                   ('Eighteen needs one two and two threes — all in stock.', 'Fifty needs one two and two fives — all in stock.'),
                   ('Twelve needs TWO twos. One twenty-six has only one. Twelve does not divide it.',
                    'Twenty needs TWO twos. One fifty has only one. Twenty does not divide it.')])
    M.card('mem-primes')['tips'][0] = ('A number divides by every combination of its prime factors: $18=2\\cdot3\\cdot3$, therefore $2$, $3$, '
                                       '$6$, $9$ and $18$ divide it.')

    # ============================== lesson "Factor Tools" + its card
    _sub(M, LESSON_B, 3, [('$n=2^3\\cdot5^2$', '$n=3^3\\cdot5^2$'), ('n = 2³ · 5² appears', 'n = 3³ · 5² appears'),
                          ('how many twos and how many fives', 'how many threes and how many fives'),
                          ('"2: 0, 1, 2, 3 → 4 options"', '"3: 0, 1, 2, 3 → 4 options"'),
                          ('Twos: zero, one, two or three — four options.', 'Threes: zero, one, two or three — four options.')])
    c = M.card('mem-factor-tools')
    rows = c['tables'][0]['rows']
    assert rows[0][2].startswith('$72=') and rows[1][2].startswith('$72,') and rows[2][2] == '$18\\cdot360=72\\cdot90$', rows
    rows[0][2] = '$45=3^2\\cdot5$, $75=3\\cdot5^2$ → $3\\cdot5=15$'
    rows[1][2] = '$45,\\ 75$ → $3^2\\cdot5^2=225$'
    rows[2][2] = '$15\\cdot225=45\\cdot75$'
    rows[4][2] = 'divisors of $4$: $1$, $2$, $4$'
    rows[5][2] = '$3^3\\cdot5^2$ → $4\\cdot3=12$'
    c['tips'][0] = 'Divisible by $3$ and $7$ → by $21$. Divisible by $3$ and $9$ → only $9$ is sure (the $3$ is inside the $9$).'
    c['tips'][1] = 'Trap: multiplying the two numbers. $6\\cdot10=60$, but the LCM of $6$ and $10$ is $30$, because they share the prime $2$.'

    # ============================== theory A guided questions
    # q-387: x^5 two-digit, 7x (x = 2, 14) -> x^6 two-digit, 9x (x = 2, 18)
    S('q-387', stem='Given: $x$ is a prime number, and $x^6$ is a two-digit number. $9x=?$',
      choices=['$27$', '$18$', '$63$', '$45$'], correct=2, expl=[
        'Test the smallest primes.', '$x=2$: $2^6=64$, two digits ✓.',
        '$x=3$: $3^6=729$, three digits ✗. Bigger primes give even bigger sixth powers.',
        'So $x=2$ and $9x=9\\cdot2=18$.'])
    video('q-387', {
        1: ['Question %s.' % qword('solve-q-387'), "Prime questions can be solved by trial and error."],
        2: ["Just check numbers against the conditions — and see what fits.",
            "Start with the smallest prime: two.",
            D('Write "2⁶ = 64 ✓ two digits"'),
            "Two to the sixth is sixty-four. Two digits — it fits.",
            D('Write "3⁶ = 729 ✗"'),
            "Three to the sixth: seven hundred twenty-nine. Three digits. Too big.",
            "And every bigger prime only gets bigger. So x must be two.",
            D('Write "9x = 9 · 2 = 18" and circle choice 2'),
            "Nine times two: eighteen. Choice two."]})

    # q-388: x = 3·2³·10², not a divisor 21 -> x = 5·3²·6², not a divisor 35
    S('q-388', stem='Given: $x=5\\cdot3^2\\cdot6^2$. Which of the following numbers does not divide $x$?',
      choices=['$12$', '$35$', '$45$', '$18$'], correct=2, expl=[
        'Break the non-prime factor into primes: $6^2=(2\\cdot3)^2=2^2\\cdot3^2$. Therefore $x=2^2\\cdot3^4\\cdot5$.',
        'Check each choice: $12=2^2\\cdot3$ ✓, $45=3^2\\cdot5$ ✓, $18=2\\cdot3^2$ ✓.',
        '$35=5\\cdot7$, and $x$ has no $7$. So $35$ does not divide $x$.'])
    video('q-388', {
        2: ["Not a divisor means: it's not a factor of x. You can't build it from x's primes.",
            "So check each answer: does it need a prime that x doesn't have?",
            "But first — six isn't a prime. Unpack it.",
            D('Under x write "6² = 2² · 3²  →  x = 2² · 3⁴ · 5"'),
            "Six squared is two squared times three squared. So x has two twos, four threes, and a five.",
            D('Next to choice 1 write "2² · 3 ✓"'),
            "Twelve: two twos and a three. In stock.",
            D('Next to choice 3 write "3² · 5 ✓"'),
            "Forty-five: two threes and a five. All there.",
            D('Next to choice 4 write "2 · 3² ✓"'),
            "Eighteen: a two and two threes. It divides.",
            D('Next to choice 2 write "5 · 7 — no 7!" and circle choice 2'),
            "Thirty-five: five times seven. There's no seven anywhere in x. Choice two."]})

    # q-386: around 20 (x 14-16, y = 30, 420) -> around 40 (x = 30, y 44-46, 1320)
    S('q-386', stem='$x$ and $y$ are integers that are not prime, and $x<40<y$. Between $x$ and $40$ there are exactly $2$ prime numbers (not including $x$). Between $40$ and $y$ there are exactly $2$ prime numbers (not including $y$). What is the smallest possible value of $x\\cdot y$?',
      choices=['$1200$', '$1276$', '$1320$', '$1380$'], correct=3, expl=[
        'The primes near $40$: $29$, $31$, $37$, $41$, $43$, $47$.',
        'Below $40$: the two primes must be $31$ and $37$, and $29$ must stay out. Therefore $29\\le x<31$. $x=29$ is prime (not allowed), therefore $x=30$.',
        'Above $40$: the two primes must be $41$ and $43$, and $47$ must stay out. Therefore $43<y\\le47$. $y=47$ is prime (not allowed), therefore $y$ is $44$, $45$ or $46$.',
        'The smallest product: $30\\cdot44=1320$.'])
    nl = dict(M.slide('solve-q-386', 2)['items'][1]); assert nl.get('k') == 'nl', nl
    nl['min'], nl['max'] = 26, 48
    video('q-386', {
        1: ['Question %s.' % qword('solve-q-386'), "The trick: draw it on a number line."],
        2: ["First — which primes are near forty? Write out the whole numbers.",
            A('A number line from 26 to 48 appears', nl),
            D('Circle the primes on the line: 29, 31, 37, 41, 43, 47'),
            "Twenty-nine, thirty-one, thirty-seven… then forty-one, forty-three, forty-seven.",
            "Between x and forty: exactly two primes. So thirty-one and thirty-seven are in — twenty-nine must stay out.",
            D('Shade 30 on the left, and cross out 29'),
            "x can't be below twenty-nine — then there'd be three primes. So x is twenty-nine or thirty.",
            "And twenty-nine is prime. Not allowed. x is thirty.",
            "Between forty and y: exactly two primes — forty-one and forty-three. Forty-seven must stay out.",
            D('Shade 44, 45, 46 on the right'),
            "So y is forty-four, forty-five or forty-six. Forty-seven is prime — not allowed anyway.",
            "We want the SMALLEST product. Take the smallest x and the smallest y.",
            D('Write "30 · 44 = 1320" and circle choice 3'),
            "Thirty times forty-four: one thousand three hundred twenty. Choice three.",
            "If they'd asked for the largest — take the largest y: thirty times forty-six."]})

    # order: easy -> hard, in the order the lesson teaches (trial and error, root test, divisors, number line)
    G0 = 'q-r26-t14-01'
    M.move('q-387', 'primes-a', after='mem-primes'); M.move('solve-q-387', 'primes-a', after='q-387')
    M.move(G0, 'primes-a', after='solve-q-387'); M.move('solve-' + G0, 'primes-a', after=G0)
    M.move('q-388', 'primes-a', after='solve-' + G0); M.move('solve-q-388', 'primes-a', after='q-388')
    M.move('q-386', 'primes-a', after='solve-q-388'); M.move('solve-q-386', 'primes-a', after='q-386')

    # ============================== theory B guided questions
    # q-389: GCD of a²·b·c⁴·d and a³·c²·d² -> letters p, q, r, s with new powers; LCM trap kept
    S('q-389', stem='$p$, $q$, $r$, $s$ are different prime numbers.\nGiven:\n$\\begin{cases} x=p^3\\cdot q^2\\cdot s \\\\ y=p\\cdot q^5\\cdot r\\cdot s^2 \\end{cases}$\nWhat is the greatest common divisor (GCD) of $x$ and $y$?',
      choices=['$p\\cdot q\\cdot r\\cdot s$', '$p^3\\cdot q^5\\cdot r\\cdot s^2$', '$p\\cdot q^2\\cdot s$', '$p\\cdot q\\cdot s$'], correct=3, expl=[
        'GCD: take each prime that is in both numbers, at its LOWER power.',
        '$p$: $p^3$ and $p$ → $p$. $q$: $q^2$ and $q^5$ → $q^2$. $s$: $s$ and $s^2$ → $s$.',
        '$r$ is only in $y$, therefore it is not in the GCD.',
        'GCD $=p\\cdot q^2\\cdot s$. (Choice (2) takes the higher powers: that is the LCM.)'])
    video('q-389', {
        2: ["The GCD is the biggest number that divides both. Which primes are in BOTH numbers — and at what power?",
            "Each shared prime, at its LOWER power.",
            D('Circle p in both x and y'),
            "p: x has p cubed, y has just p. The lower power: p.",
            D('Circle q² in both'),
            "q: q squared and q to the fifth. The lower: q squared.",
            D('Cross out r'),
            "r: only in y. Not shared. Out.",
            D('Circle s in both'),
            "s: s and s squared. The lower: s.",
            D('Write "p · q² · s" and circle choice 3'),
            "p, q squared, s. Choice three.",
            "Choice two is the trap — every prime at its HIGHER power. That's the LCM, not the GCD."]})

    # q-390: divisible by 8 and 12 -> 24 (trap 96) -> divisible by 10 and 25 -> 50 (trap 250)
    S('q-390', stem='A number is divisible without remainder by both $10$ and $25$. What is the greatest number that is guaranteed to divide it?',
      choices=['$25$', '$100$', '$50$', '$250$'], correct=3, expl=[
        'Break into primes: $10=2\\cdot5$ and $25=5^2$.',
        'The number is divisible by both, therefore it is divisible by their least common multiple (LCM): every prime at its HIGHER power. $2\\cdot5^2=50$.',
        'Nothing bigger is guaranteed: the number could be $50$ itself, and $100$ does not divide $50$.',
        'The trap: $10\\cdot25=250$. The two numbers share the prime $5$, therefore their product is too big.'])
    video('q-390', {
        2: ["The number is divisible by ten and by twenty-five. What can we be SURE divides it?",
            "Break both into primes.",
            D('Write "10 = 2 · 5" and "25 = 5²"'),
            "Ten is two times five. Twenty-five is five squared.",
            "Multiply them? Two hundred fifty? No! The five in ten may be the very same five that is in twenty-five.",
            "Take every prime at its HIGHER power.",
            D('Write "2: only 2¹ → 2;   5: 5¹ and 5² → 5²"'),
            "Twos: only in ten — take one. Fives: one and two — take two.",
            D('Write "2 · 5² = 50" and circle choice 3'),
            "Two times five squared: fifty. Choice three.",
            "Check: fifty itself is divisible by ten and by twenty-five. And a hundred doesn't divide fifty. So we can't promise more.",
            A("'GCD · LCM = a · b' appears", T('GCD $\\cdot$ LCM $=a\\cdot b$:  $5\\cdot50=10\\cdot25=250$', size=40)),
            "A bonus fact: the GCD times the LCM equals the two numbers multiplied. The GCD here is five — five times fifty is two hundred fifty."]})

    # q-398: three-digit number, digits 1, 2, 3, product cannot be 10 -> lock code, digits 1, 3, 5, cannot be 30
    S('q-398', stem='A lock code has three digits, and each digit is $1$, $3$ or $5$ (a digit may repeat). Which of the following cannot be the product of the three digits?',
      choices=['$45$', '$30$', '$25$', '$15$'], correct=2, expl=[
        'Each digit is $1$, $3$ or $5$, therefore the product is built only from the primes $3$ and $5$.',
        '$45=3\\cdot3\\cdot5$ (digits $3$, $3$, $5$) ✓. $25=1\\cdot5\\cdot5$ ✓. $15=1\\cdot3\\cdot5$ ✓.',
        '$30=2\\cdot3\\cdot5$ needs the prime $2$, and no digit gives it. So $30$ is impossible.'])
    video('q-398', {
        2: ["Each digit of the code is one, three or five. Multiply the three digits.",
            "Check each answer: can it be built from ones, threes and fives? Or does it need another prime?",
            D('Next to choice 1 write "3 · 3 · 5 → 335 ✓"'),
            "Forty-five: three, three, five. The code could be three-three-five.",
            D('Next to choice 3 write "1 · 5 · 5 → 155 ✓"'),
            "Twenty-five: one, five, five. One-five-five works.",
            D('Next to choice 4 write "1 · 3 · 5 → 135 ✓"'),
            "Fifteen: one, three, five. One-three-five.",
            D('Next to choice 2 write "2 · 3 · 5 — no 2!" and circle choice 2'),
            "Thirty: two times three times five. Two isn't one of the digits. It can't be the product. Choice two."]})

    # q-399: x·y = 36 -> x·y = 100 (answer 48; trap 33 = forgetting 10·10)
    S('q-399', stem='$x$ and $y$ are positive integers, and neither of them is $1$.\nGiven:\n$\\begin{cases} x\\cdot y=100 \\\\ A=|x-y| \\end{cases}$\nWhat is the difference between the greatest possible value of $A$ and the smallest possible value of $A$?',
      choices=['$33$', '$21$', '$48$', '$15$'], correct=3, expl=[
        'Break $100$ into pairs of factors (without $1$): $2\\cdot50$, $4\\cdot25$, $5\\cdot20$, $10\\cdot10$.',
        'The values of $A$: $50-2=48$, $25-4=21$, $20-5=15$, $10-10=0$.',
        'Greatest $A=48$, smallest $A=0$. The difference: $48-0=48$. (Forgetting $10\\cdot10$ gives $48-15=33$ — the trap.)'])
    video('q-399', {
        2: ["x times y is a hundred. A is the difference between them.",
            "So take a hundred and break it into every pair you can. One isn't allowed.",
            D('Write the pairs: 2·50 → 48, 4·25 → 21, 5·20 → 15, 10·10 → 0'),
            "Two and fifty: difference forty-eight. Four and twenty-five: twenty-one. Five and twenty: fifteen. Ten and ten: zero.",
            "The biggest difference: forty-eight. The smallest: zero.",
            D('Write "48 − 0 = 48" and circle choice 3'),
            "Forty-eight minus zero: forty-eight. Choice three.",
            "Forgot ten times ten? You'd take fifteen as the smallest and get thirty-three — it's right there in the choices.",
            "All the rest — the max of A, the min of A — is just reading comprehension to make it look harder."]})

    # q-400: products of 2, 3, 7 (83, trap 41) -> Dan's cards 2, 5, 7 (129, trap 59)
    S('q-400', stem='Dan has three cards with the numbers $2$, $5$ and $7$. He picks two or more of the cards and multiplies their numbers. What is the sum of all the different products he can get?',
      choices=['$129$', '$70$', '$14$', '$59$'], correct=1, expl=[
        'Products of two cards: $2\\cdot5=10$, $2\\cdot7=14$, $5\\cdot7=35$.',
        'Product of all three: $2\\cdot5\\cdot7=70$.',
        'Sum: $10+14+35+70=129$. (Forgetting $70$ gives $59$ — the trap.)'])
    video('q-400', {
        2: ["Two or more of the cards two, five and seven. Build every product.",
            D('Write "2 · 5 = 10", "2 · 7 = 14", "5 · 7 = 35"'),
            "Two times five: ten. Two times seven: fourteen. Five times seven: thirty-five.",
            D('Write "2 · 5 · 7 = 70"'),
            "And don't forget — he can take all three cards. Seventy.",
            "Now add them. It's easier starting from the big one.",
            D('Write "70 + 35 + 14 + 10 = 129" and circle choice 1'),
            "Seventy plus thirty-five: a hundred five. Plus fourteen: a hundred nineteen. Plus ten: a hundred twenty-nine. Choice one.",
            "Forgot the seventy? You'd get fifty-nine — and it's sitting right there in the choices."]})

    # q-401: y² prime -> m² prime (letters + choice order; both methods kept)
    S('q-401', stem='Given: $m^2$ is a prime number. Which of the following is necessarily true?',
      choices=['$m$ is prime', '$m$ is not an integer', '$m$ is even', '$m$ is odd'], correct=2, expl=[
        'If $m$ were an integer with $|m|>1$, then $m^2=m\\cdot m$ would break into two factors bigger than $1$. It would not be prime.',
        'If $m$ were $0$, $1$ or $-1$, then $m^2$ would be $0$ or $1$. These are not prime either.',
        'So $m$ is not an integer. Example: $m=\\sqrt5$ gives $m^2=5$, a prime.'])
    video('q-401', {
        2: ["m squared is prime. A prime can't be broken into anything.",
            "So m can't be a whole number — a whole m would make m squared equal m times m. That breaks.",
            D('Write "m² = m · m → breaks"'),
            "Zero and one? Their squares are zero and one — not prime either.",
            D('Circle choice 2'),
            "m is not an integer. Choice two."],
        3: ["Hard to see? Plug in numbers.",
            "m squared is prime — take five.",
            D('Write "m² = 5 → m = √5"'),
            "Then m is root five. Not a whole number.",
            D('Write "m² = 2 → m = √2"'),
            "Take two: m is root two. Not whole either.",
            D('Circle choice 2'),
            "Choice two. The trap: seeing \"prime\" and deciding m is prime too. It's m SQUARED that's prime — m is its square root."]})

    # q-402: n with 3 divisors, B = √n -> k with 3 divisors, C = √k (example 25 instead of 49)
    S('q-402', stem='$k$ is a positive integer with exactly $3$ different divisors (including $1$ and $k$).\nGiven: $C=\\sqrt{k}$.\nHow many divisors does $C$ have (including $1$ and $C$)?',
      choices=['$1$', '$k$', '$0$', '$2$'], correct=4, expl=[
        'Exactly $3$ divisors means $k=p^2$ for a prime $p$. Its divisors are $1$, $p$ and $p^2$.',
        '$C=\\sqrt{p^2}=p$, a prime.',
        'A prime has exactly $2$ divisors: $1$ and itself. Example: $k=25$, $C=5$, and the divisors of $5$ are $1$ and $5$.'])
    video('q-402', {
        2: ["k has exactly three divisors.",
            "Most numbers have divisors in pairs — an even count. Three is odd.",
            D('Write "3 divisors → k = p²"'),
            "Three divisors means one sits in the middle with no partner. So k is a prime squared.",
            A("'Odd number of divisors → perfect square' appears", T('Odd number of divisors $\\to$ a perfect square', size=40)),
            "In general: an odd number of divisors means a perfect square — the middle divisor times itself.",
            D('Write "C = √k = p → prime"'),
            "C is the root of k — so C is that prime.",
            D('Write "divisors of C: 1, p → 2" and circle choice 4'),
            "A prime has exactly two divisors: one and itself. Choice four.",
            "Example: k is twenty-five — one, five, twenty-five. C is five: one and five. Two."]})

    # ============================== advanced guided questions
    # q-391: which cannot be a+b (25, 27, 33, 45 -> 27) -> p+q (15, 31, 51, 43 -> 51); "25 = 2 + 23" is a lesson example
    S('q-391', stem='$p$ and $q$ are prime numbers. Which of the following numbers cannot be $p+q$?',
      choices=['$15$', '$31$', '$51$', '$43$'], correct=3, expl=[
        'All four choices are odd. An odd sum of two primes needs one even prime, and the only even prime is $2$.',
        'So check whether the choice minus $2$ is prime.',
        '$15=2+13$ ✓. $31=2+29$ ✓. $43=2+41$ ✓ ($41$ is prime: $\\sqrt{41}<7$, and $2$, $3$, $5$ do not divide it).',
        '$51=2+49$, and $49=7^2$ is not prime ✗. So the sum cannot be $51$.'])
    video('q-391', {
        2: ["Two primes, and a sum. Which choice can NOT be their sum?",
            "Trial and error? Split fifteen into two primes, then thirty-one… that takes forever.",
            "On the psychometric there's almost always one simple idea. Once it clicks, the answer falls out.",
            "Look at the choices. Every single one is odd.",
            D('Write "odd" next to each choice'),
            "When is a sum odd? Even plus even — even. Odd plus odd — even.",
            "Only one even and one odd give an odd sum.",
            "And the primes are almost all odd — except one. Two. The only even prime. We saw this rule at the start of the topic.",
            D('Write "= 2 + ?" next to the stem'),
            "So one of the primes MUST be two. Take two off each choice and check what's left.",
            D('Next to 15 write "2 + 13 ✓"'),
            "Fifteen: two plus thirteen. Thirteen is prime. Possible.",
            D('Next to 31 write "2 + 29 ✓"'),
            "Thirty-one: two plus twenty-nine. Twenty-nine is prime. Possible too.",
            D('Cross out choices 1 and 2'),
            D('Next to 51 write "2 + 49 = 7 · 7 ✗"'),
            "Fifty-one: two plus forty-nine. Forty-nine is seven times seven — not prime.",
            D('Circle choice 3'),
            "So fifty-one can't be the sum. On the exam — mark it and move on.",
            "In the lesson we check the last one. Forty-three: two plus forty-one — prime.",
            D('Cross out choice 4'),
            "The whole question was one fact: two is the only even prime. The exam loves it."]})

    # q-392: 10, 15, 7 / 22, 15, 30 -> a·b = 55  ->  14, 21, 5 / 26, 21, 42 -> a·b = 91
    S('q-392', stem='$a$ and $b$ are prime numbers.\nExactly two of the numbers $14$, $21$, $5$ are divisible by $a$.\nExactly one of the numbers $26$, $21$, $42$ is divisible by $b$.\n$a\\cdot b=?$',
      choices=['$39$', '$26$', '$91$', '$21$'], correct=3, expl=[
        'Break into primes: $14=2\\cdot7$, $21=3\\cdot7$, $5=5$. Only the prime $7$ is in exactly two of them. So $a=7$.',
        '$26=2\\cdot13$, $21=3\\cdot7$, $42=2\\cdot3\\cdot7$. The primes $2$, $3$ and $7$ are each in two of them. Only $13$ is in exactly one. So $b=13$.',
        '$a\\cdot b=7\\cdot13=91$.'])
    video('q-392', {
        2: ["The idea: break every number into its prime factors.",
            D('Under 14, 21 and 5 write "2·7", "3·7", "5"'),
            "Fourteen is two times seven. Twenty-one is three times seven. Five is prime.",
            "Exactly two of them are divisible by a. Which prime shows up in exactly two?",
            D('Circle both 7s'),
            "Seven. So a equals seven.",
            D('Under 26, 21 and 42 write "2·13", "3·7", "2·3·7"'),
            "Second group. Twenty-six: two times thirteen. Twenty-one: three times seven. Forty-two: two, three and seven.",
            "Only ONE of these is divisible by b. Two appears twice. Three — twice. Seven — twice. Thirteen — only once.",
            D('Circle the 13'),
            "So b is thirteen.",
            D('Write "a · b = 7 · 13 = 91" and circle choice 3'),
            "Seven times thirteen: ninety-one. Choice three. This is the recommended route."],
        3: ["Some students plug in the answers instead.",
            "Choice one: thirty-nine is three times thirteen. Could a be three? Only twenty-one is divisible by three — not two numbers.",
            "Could a be thirteen? None of fourteen, twenty-one, five is divisible by thirteen.",
            D('Cross out choice 1'),
            "Choice two: twenty-six is two times thirteen. a equals two? Only fourteen. a equals thirteen? None.",
            D('Cross out choice 2'),
            "Choice three: ninety-one is seven times thirteen. a equals seven — fourteen and twenty-one, exactly two. b equals thirteen — only twenty-six. It fits.",
            D('Circle choice 3'),
            "On the exam — mark it. In the lesson, check twenty-one too: twenty-one is three times seven. a would have to be seven — and then b is three. But three divides twenty-one AND forty-two. Out.",
            D('Cross out choice 4'),
            "Two approaches. The recommended one: break the numbers into primes. Stuck? Plugging in answers works too."]})

    # q-393: a·b + 2a = 36 (cannot be 15) -> a·b + 4a = 48 (cannot be 17)
    S('q-393', stem='$a$ and $b$ are positive integers.\nGiven:\n$\\begin{cases} a<b \\\\ a\\cdot b+4a=48 \\end{cases}$\nWhich of the following cannot be the value of $a+b$?',
      choices=['$45$', '$15$', '$17$', '$12$'], correct=3, expl=[
        'Take out the common factor $a$: $a(b+4)=48$.',
        'Go over the factor pairs of $48$. $a=1$: $b+4=48$, $b=44$, $a+b=45$. $a=2$: $b+4=24$, $b=20$, $a+b=22$.',
        '$a=3$: $b+4=16$, $b=12$, $a+b=15$. $a=4$: $b+4=12$, $b=8$, $a+b=12$.',
        '$a=6$: $b+4=8$, $b=4<a$ ✗. A bigger $a$ gives an even smaller $b$ ✗.',
        'The possible sums are $45$, $22$, $15$ and $12$. $17$ is not possible.'])
    video('q-393', {
        2: ["We've got an equation. And a appears in both terms — so take it out as a common factor.",
            D('Under the stem write "a(b + 4) = 48"'),
            "a times b-plus-four equals forty-eight. A product of two things.",
            "So break forty-eight into two factors — not necessarily primes. a is the smaller one.",
            D('Write "1 × 48 → b = 44, a + b = 45"'),
            "a equals one: the bracket is forty-eight, so b is forty-four. Sum: forty-five.",
            D('Cross out choice 1'),
            D('Write "2 × 24 → b = 20, a + b = 22"'),
            "a equals two: the bracket is twenty-four, b is twenty. Sum twenty-two — not a choice. Keep going.",
            D('Write "3 × 16 → b = 12, a + b = 15"'),
            "a equals three: the bracket is sixteen, b is twelve. Sum fifteen.",
            D('Cross out choice 2'),
            D('Write "4 × 12 → b = 8, a + b = 12"'),
            "a equals four: the bracket is twelve, b is eight. Still bigger than a. Sum twelve.",
            D('Cross out choice 4'),
            "Three choices eliminated — mark the one that's left.",
            D('Circle choice 3'),
            "Seventeen can't be the sum. Choice three.",
            "The tools: take out a common factor, then break the number into factors that aren't necessarily prime."]})

    # q-394: y = a^d·b^c (a<b<c<d) -> z = p^r·q^s (p<q<r<s); new letters, new choice order, both methods kept
    S('q-394', stem='$p$, $q$, $r$, $s$ are prime numbers, and $p<q<r<s$.\nGiven: $z=p^r\\cdot q^s$.\nWhich of the following necessarily divides $z$?',
      choices=['$r$', '$p^q\\cdot q^r$', '$p^s$', '$s^q$'], correct=2, expl=[
        '$z$ is built from the prime $p$ ($r$ times) and the prime $q$ ($s$ times).',
        '$p^q$: $q<r$, therefore $z$ has enough $p$s ✓. $q^r$: $r<s$, therefore $z$ has enough $q$s ✓. So $p^q\\cdot q^r$ divides $z$.',
        '$p^s$: $z$ has only $r$ copies of $p$, and $r<s$ ✗. $r$ and $s^q$: the primes $r$ and $s$ are not factors of $z$ at all ✗.',
        'With the smallest primes: $p=2$, $q=3$, $r=5$, $s=7$ give $z=2^5\\cdot3^7$, and of the four choices only $2^3\\cdot3^5$ divides it.'])
    video('q-394', {
        2: ["This is a factors question. What is z actually built from?",
            D('Under z write "p … r times, q … s times"'),
            "z contains the prime p — r times. And the prime q — s times.",
            "Is z divisible by p? Of course. By q? Of course. By r or s? No — those primes aren't in z at all.",
            "First look at the choices — what can we kill fast?",
            D('Cross out choice 1'),
            "Choice one, r. Out immediately. r only shows up as an exponent — it's how MANY times p appears, not a factor of z.",
            D('Cross out choice 4'),
            "Choice four, s to the q. z has no factor s. Out.",
            "Choice three: p to the s. z has p only r times — and s is bigger than r. Not enough p's.",
            D('Cross out choice 3'),
            "Three are out — on the exam, mark the one that's left.",
            D('Circle choice 2'),
            "In the lesson — why it works. p to the q: z has p r times, and q is less than r. Enough. q to the r: z has q s times, and r is less than s. Enough. Choice two."],
        3: ["Hard to follow with letters? Same idea — with numbers.",
            "Smallest primes, in order: p is two, q is three, r is five, s is seven.",
            D('Write "z = 2⁵ · 3⁷"'),
            "z is two to the fifth times three to the seventh.",
            D('Next to choice 1 write "5 ✗"'),
            "Choice one: five. z is built only from twos and threes. Out.",
            D('Next to choice 2 write "2³ · 3⁵ ✓"'),
            "Choice two: two cubed times three to the fifth. Two three times — z has five. Three five times — z has seven. It fits.",
            "But we're plugging in — so we must knock out three choices before marking. It might only work for these numbers.",
            D('Next to choice 3 write "2⁷ ✗"'),
            "Choice three: two to the seventh. z only has two five times. Too many. Out.",
            D('Next to choice 4 write "7³ ✗"'),
            "Choice four: seven cubed. No seven in z at all. Out.",
            D('Circle choice 2'),
            "Choice two. Strong without numbers? Great. If not — plugging in is an excellent route."]})

    # q-395: a·b·c divisible by 15, x² (answer 4) -> divisible by 35, x² (review: kept x² as in the Hebrew), statements reordered (answer 2)
    S('q-395', stem='$a$, $b$, $c$ are different positive integers.\nGiven: $x=a\\cdot b\\cdot c$ is divisible by $35$ without remainder.\nWhich of the following statements is not necessarily true?',
      choices=['It is possible that exactly one of $a$, $b$, $c$ is divisible by $35$.',
               'The number of different prime divisors of $x^2$ is greater than that of $x$.',
               'If $b$ and $c$ are not divisible by $7$, then $a^2$ is divisible by $49$.',
               'At least one of $a$, $b$, $c$ is divisible by $5$.'], correct=2, expl=[
        '(1) Possible: $a=35$, $b=1$, $c=2$ ✓.',
        '(2) Never true: squaring doubles the exponents but adds no new prime. For example, $35=5\\cdot7$ and $35^2=1225=5^2\\cdot7^2$ have the same two primes.',
        '(3) Always true: $7$ is prime and divides $a\\cdot b\\cdot c$. It does not divide $b$ or $c$, therefore it divides $a$. Then $a^2$ is divisible by $7^2=49$.',
        '(4) Always true: $5$ is prime and divides $a\\cdot b\\cdot c$, therefore it divides one of the factors.',
        'Never true is also "not necessarily true", therefore the answer is (2).'])
    video('q-395', {
        2: ["First, the given. x is divisible by thirty-five — so x must contain the primes five and seven.",
            D('Next to the stem write "35 = 5 · 7"'),
            "x is a times b times c. So at least one of them brings the five, and at least one brings the seven.",
            A("'A prime divides a · b → it divides a or b' appears", T('A prime divides a product $\\to$ it divides one of the factors', size=38)),
            "That's the rule: a prime can't be split between factors — one of them holds it. Thirty-five isn't prime, so its five and its seven may come from different numbers.",
            "Statement four: at least one of them is divisible by five. Someone had to bring the five. True for sure.",
            "Maybe one number brings both — thirty-five, one, two. Maybe they split the job — five, seven, one. Either way, someone holds the five.",
            D('Cross out choice 4'),
            "Statement one: it's possible that exactly one is divisible by thirty-five. Sure — thirty-five, one and two.",
            D('Write "35, 1, 2 ✓" and cross out choice 1'),
            "Possible. Out.",
            "Statement three: if b and c aren't divisible by seven — who brought the seven? a must have.",
            D('Next to choice 3 write "7 | a → 49 | a²"'),
            "Square a, and the seven appears twice. So a squared is divisible by forty-nine.",
            "Numbers: seven, five, one — a squared is forty-nine. Or fourteen, five, one — a hundred ninety-six. Both are divisible by forty-nine.",
            D('Cross out choice 3'),
            "Three statements out — on the exam you mark the one that's left. This is probably the last question in the section anyway.",
            D('Circle choice 2'),
            "In the lesson, let's learn from statement two. Notice the word: DIFFERENT prime divisors.",
            D('Write "35 = 5·7 → 35² = 5²·7²"'),
            "Square x, and the same primes just appear twice as often. No NEW prime shows up.",
            "So the number of different prime divisors stays exactly the same — never greater. Choice two.",
            "One more word. Statement two is NEVER true.",
            "Never true is also \"not necessarily true\". So it's the answer."]})

    # q-396: a from {2, 5}, b from {2, 7} -> 8 (trap 4) -> a from {3, 5}, b from {3, 7} -> 27 (trap 9)
    S('q-396', stem='$a$ and $b$ are positive integers. $a$ has exactly two prime factors: $3$ and $5$. $b$ has exactly two prime factors: $3$ and $7$.\nGiven: $b<a$.\nWhat is the smallest possible value of $\\frac{a\\cdot b}{35}$?',
      choices=['$27$', '$9$', '$81$', '$45$'], correct=1, expl=[
        'Numbers with exactly the prime factors $3$ and $5$: $15$, $45$, $75$, … Numbers with exactly the prime factors $3$ and $7$: $21$, $63$, …',
        'The expression is smallest when $a$ and $b$ are smallest. The smallest $b$ is $21$. Since $b<a$, $a=15$ is too small. The smallest $a$ above $21$ is $45$.',
        '$\\frac{a\\cdot b}{35}=\\frac{45\\cdot21}{35}=\\frac{945}{35}=27$. (With $a=15$, ignoring $b<a$, you get $9$ — the trap.)'])
    video('q-396', {
        2: ["When is the expression smallest? When a is smallest and b is smallest.",
            "a is built from threes and fives only — but from BOTH. Smallest: one three, one five.",
            D('Write "a = 3 · 5 = 15"'),
            "Fifteen.",
            D('Write "b = 3 · 7 = 21"'),
            "b is built from threes and sevens. Smallest: twenty-one.",
            "But wait — a must be bigger than b. Fifteen isn't bigger than twenty-one.",
            "So we have to grow a. By how much? a may only contain threes and fives — so times three, or times five.",
            D('Write "a = 3² · 5 = 45"'),
            "Keep it as small as possible: times three. a becomes forty-five. Bigger than twenty-one — good.",
            D('Write "(3² · 5)(3 · 7) / (5 · 7)"'),
            "Now plug in. Forty-five times twenty-one, over thirty-five.",
            D('Cancel the 5s and the 7s; write "= 3³ = 27"'),
            "The five and the seven cancel with thirty-five. Three cubed — twenty-seven.",
            D('Circle choice 1'),
            "Choice one."]})

    # q-397: 1 < a < 150 with 3 divisors (5 values) -> 1 < a < 200 (6 values)
    S('q-397', stem='$a$ is an integer.\nGiven: $1<a<200$, and $a$ has exactly $3$ different divisors (including $1$ and $a$).\nHow many different values can $a$ have?',
      choices=['$5$', '$7$', '$6$', '$4$'], correct=3, expl=[
        'A number with exactly $3$ divisors is a prime squared: its divisors are $1$, $p$ and $p^2$.',
        'Prime squares below $200$: $2^2=4$, $3^2=9$, $5^2=25$, $7^2=49$, $11^2=121$, $13^2=169$. The next one, $17^2=289$, is too big.',
        'So there are $6$ values.'])
    video('q-397', {
        2: ["Which numbers have exactly three different divisors?",
            D('Write "prime → 2 divisors"'),
            "A prime has exactly two: itself and one. Two has one and two.",
            D('Write "6 = 2 · 3 → 1, 2, 3, 6"'),
            "Two different primes multiplied — like six — give four: one, two, three and six.",
            D('Write "4 = 2² → 1, 2, 4"'),
            "Three divisors? A prime squared. Four has one, two and four — only one prime built it.",
            "So a is a prime, squared. And a is less than two hundred.",
            D('Write "p² < 200 → p ≤ 14"'),
            "Then the prime must be fourteen or less — fifteen squared is already two hundred twenty-five.",
            D('Write "2, 3, 5, 7, 11, 13 → 4, 9, 25, 49, 121, 169"'),
            "Primes up to fourteen: two, three, five, seven, eleven, thirteen. Six of them.",
            D('Circle choice 3'),
            "Six values. Choice three. If you know this principle, the question is simple."],
        3: ["Don't remember the principle? Then trial and error: run through the numbers, and find the pattern.",
            D('Write "1 → 1", "2, 3 → 2 divisors"'),
            "One has one divisor. Two and three are prime — two divisors each.",
            D('Write "4 → 1, 2, 4 ✓"'),
            "Four: one, two, four. The first that fits!",
            "Five is prime. Six has four divisors. Seven is prime. Eight: one, two, four, eight — four.",
            D('Write "9 → 1, 3, 9 ✓"'),
            "Nine: one, three, nine. Fits.",
            "Stop and look for the pattern. Four is two squared. Nine is three squared.",
            D('Write "25, 49, 121, 169"'),
            "So the next ones are prime squares: twenty-five, forty-nine, a hundred twenty-one, a hundred sixty-nine — all under two hundred.",
            D('Circle choice 3'),
            "Six numbers. Choice three. That's primes — on to the summary."]})

    # order: the minimum question (q-396) before the two hard letter questions (q-394, q-395)
    M.move('q-396', 'primes-advanced', after='solve-q-393'); M.move('solve-q-396', 'primes-advanced', after='q-396')
    grp = [f['ref'] for f in M.D['flow'] if f['section'] == 'primes-advanced' and f['type'] == 'video'
           and M.video(f['ref']).get('kind') == 'solution']
    labels = [M.video(v)['beats'][0]['bigTitle'] for v in grp]
    for k, vid in enumerate(grp):
        M.set_sidebar(vid, labels)
        for b in M.video(vid)['beats']:
            if b['mode'] != 'title': b['active'] = k
    grpA = [f['ref'] for f in M.D['flow'] if f['section'] == 'primes-a' and f['type'] == 'video'
            and M.video(f['ref']).get('kind') == 'solution']
    labels = [M.video(v)['beats'][0]['bigTitle'] for v in grpA]
    for k, vid in enumerate(grpA):
        M.set_sidebar(vid, labels)
        for b in M.video(vid)['beats']:
            if b['mode'] != 'title': b['active'] = k

    # ============================== practice: Hebrew-derived questions -> new numbers / letters / stories
    S('q-403', choices=['$57$', '$17$', '$70$', '$65$'], correct=3, expl=[
        '$17$ is prime: $2$ divisors.',
        '$70=2\\cdot5\\cdot7$: $(1+1)(1+1)(1+1)=8$ divisors.',
        '$65=5\\cdot13$: $2\\cdot2=4$ divisors. $57=3\\cdot19$ (a fake prime: $5+7=12$ is divisible by $3$): $4$ divisors.',
        'The answer is $70$.'])
    S('q-404', stem='$a$ and $b$ are prime numbers smaller than $30$, and $b<a$. What is the greatest possible value of $a-b$?',
      choices=['$26$', '$27$', '$22$', '$24$'], correct=2, expl=[
        'Take the greatest prime below $30$ and the smallest prime: $a=29$ and $b=2$.',
        '$a-b=29-2=27$. (Forgetting that $2$ is prime gives $29-3=26$.)'])
    S('q-405', stem='A machine shows the number $1$. It has two buttons: one multiplies the number on the screen by $2$, and the other multiplies it by $5$. You may press them as many times as you like. Which of the following numbers can the machine not show?',
      choices=['$50$', '$30$', '$80$', '$40$'], correct=2, expl=[
        'Every number the machine can show is built only from the primes $2$ and $5$.',
        '$50=2\\cdot5^2$ ✓, $80=2^4\\cdot5$ ✓, $40=2^3\\cdot5$ ✓.',
        '$30=2\\cdot3\\cdot5$ needs the prime $3$ ✗. So $30$ cannot be shown.'])
    S('q-406', stem='What is the difference between the greatest two-digit prime number and the greatest one-digit prime number?',
      choices=['$88$', '$92$', '$90$', '$86$'], correct=3, expl=[
        'The greatest two-digit prime is $97$ ($98$ is even and $99=9\\cdot11$).',
        'The greatest one-digit prime is $7$ ($8$ is even and $9=3\\cdot3$).',
        '$97-7=90$. (Taking $9$ as a prime gives $88$; taking $99$ gives $92$.)'])
    S('q-407', stem='Given: $x>74$. There are exactly $2$ prime numbers between $74$ and $x$ (not including $x$). Which of the following cannot be the value of $x$?',
      choices=['$86$', '$90$', '$84$', '$88$'], correct=2, expl=[
        'The primes above $74$: $79$, $83$, $89$. ($77=7\\cdot11$, $81=9^2$ and $87=3\\cdot29$ are not prime.)',
        'Exactly two primes: $79$ and $83$ are in, and $89$ is out. Therefore $83<x\\le89$.',
        '$84$, $86$ and $88$ work. $x=90$ puts $89$ inside too: three primes ✗.'])
    S('q-408', stem='$k$, $m$, $n$ are different positive integers, and $x=k\\cdot m^2\\cdot n^3$. Which of the following cannot be the value of $x$?',
      choices=['$36$', '$56$', '$54$', '$15$'], correct=4, expl=[
        'One of the numbers may be $1$.',
        '$36=9\\cdot2^2\\cdot1^3$ ✓ ($k=9$, $m=2$, $n=1$). $56=7\\cdot1^2\\cdot2^3$ ✓. $54=2\\cdot1^2\\cdot3^3$ ✓.',
        '$15=3\\cdot5$: if $n\\ge2$, then $n^3\\ge8$ must divide $15$ — impossible. So $n=1$.',
        'Then $m\\ne1$ (the numbers are different). $m^2$ must be $4$ or $9$ (bigger squares are more than $15$), and neither of them divides $15$ ✗.',
        'So $x$ cannot be $15$.'])
    S('q-409', stem='$a$ is an odd one-digit prime, and $b$ is a two-digit prime smaller than $40$.\nGiven: $x=a\\cdot b$.\nWhich of the following gives the most precise range for $x$?',
      choices=['$22\\le x\\le259$', '$33\\le x\\le259$', '$3\\le x\\le37$', '$33\\le x\\le333$'], correct=2, expl=[
        'Odd one-digit primes: $3$, $5$, $7$. Two-digit primes smaller than $40$: $11$, $13$, $17$, $19$, $23$, $29$, $31$, $37$.',
        'Smallest $x=3\\cdot11=33$. Greatest $x=7\\cdot37=259$.', 'So $33\\le x\\le259$.'])
    S('q-410', stem='$a$, $b$, $c$ are different prime numbers.\nGiven:\n$\\begin{cases} K=a^3\\cdot b^2\\cdot c^4 \\\\ L=a^2\\cdot b^5\\cdot c \\end{cases}$\nWhat is the greatest common divisor (GCD) of $K$ and $L$?',
      choices=['$a^2\\cdot b^5\\cdot c^4$', '$a\\cdot b\\cdot c$', '$a^3\\cdot b^5\\cdot c^4$', '$a^2\\cdot b^2\\cdot c$'], correct=4, expl=[
        'GCD: take each prime that is in both numbers, at its LOWER power.',
        '$a$: $a^3$ and $a^2$ → $a^2$. $b$: $b^2$ and $b^5$ → $b^2$. $c$: $c^4$ and $c$ → $c$.',
        'GCD $=a^2\\cdot b^2\\cdot c$. (Choice 3 takes the higher powers: that is the LCM.)'])
    S('q-411', stem='Given: $x=3^2\\cdot5^3$. Which of the following numbers divides $x$ without remainder?',
      choices=['$45$', '$27$', '$675$', '$30$'], correct=1, expl=[
        '$45=3^2\\cdot5$: $x$ has $3^2$ and $5^3$ ✓.', '$27=3^3$: $x$ has only $3^2$ ✗.',
        '$675=3^3\\cdot5^2$: it needs $3^3$ ✗.', '$30=2\\cdot3\\cdot5$: $x$ has no $2$ ✗.'])
    S('q-412', stem='$m$ and $n$ are different prime numbers. Which of the following cannot be the difference between them?',
      choices=['$17$', '$33$', '$27$', '$39$'], correct=2, expl=[
        'All four choices are odd. An odd difference of two primes needs one even prime: $2$. So the bigger prime is the choice plus $2$.',
        '$17+2=19$ ✓, $27+2=29$ ✓, $39+2=41$ ✓ — all prime.',
        '$33+2=35=5\\cdot7$ is not prime ✗. So the difference cannot be $33$.'])
    S('q-413', stem='A number is called "lucky" if the sum of all the prime numbers from $2$ up to that number (including it) is a prime number. Which of the following numbers is "lucky"?',
      choices=['$12$', '$9$', '$6$', '$18$'], correct=2, expl=[
        '$6$: $2+3+5=10$, not prime ✗.', '$9$: $2+3+5+7=17$, prime ✓.',
        '$12$: $2+3+5+7+11=28$, not prime ✗.', '$18$: $28+13+17=58$, not prime ✗.', 'Only $9$ is "lucky".'])
    S('q-414', stem='$a$ and $b$ are integers.\nGiven: $a\\cdot b=98$.\nWhich of the following cannot be the value of $a-b$?',
      choices=['$47$', '$7$', '$97$', '$14$'], correct=4, expl=[
        'Pairs of factors of $98$: $1\\cdot98$, $2\\cdot49$, $7\\cdot14$.',
        'Their differences: $98-1=97$, $49-2=47$, $14-7=7$ (or the same numbers with a minus sign, if you swap the order).',
        'So $a-b$ can be $97$, $47$ or $7$, but not $14$.'])
    S('q-415', stem='$r$ and $s$ are prime numbers, and $s<r$. $r+s$ is also a prime number. Which of the following is necessarily true?',
      choices=['$r+s=19$', '$s+5<r$', '$s=2$', 'No such prime numbers exist.'], correct=3, expl=[
        'If $r$ and $s$ were both odd, $r+s$ would be even and bigger than $2$. It would not be prime.',
        'So one of them is the even prime $2$. Since $s<r$, $s=2$.',
        'Example: $s=2$, $r=3$, $r+s=5$. This rules out choice (1) ($5\\ne19$), choice (2) ($2+5>3$) and choice (4).'])
    S('q-416', stem='Given: $w>1$, and $w^2$ is a prime number. Which of the following is necessarily true about $w$?',
      choices=['$w$ is less than $6$', '$w$ is odd', '$w$ is even', '$w$ is not an integer'], correct=4, expl=[
        'If $w$ were an integer greater than $1$, then $w^2=w\\cdot w$ would break into two factors greater than $1$. It would not be prime.',
        'So $w$ is not an integer. Example: $w=\\sqrt3$ gives $w^2=3$, a prime.',
        '$w$ does not have to be small: $w=\\sqrt{89}$ gives $w^2=89$, a prime, and $\\sqrt{89}>9$. So choice 1 is not necessarily true.'])
    S('q-417', stem='$k$ is a positive integer. The number of different positive divisors of $k$ (including $1$ and $k$) is odd. Which of the following is necessarily true?',
      choices=['$\\sqrt{k}$ is odd', '$k$ is odd', '$k$ is prime', '$\\sqrt{k}$ is an integer'], correct=4, expl=[
        'Divisors come in pairs: $d$ and $\\frac{k}{d}$. The count is odd only if one divisor is its own partner: $d=\\frac{k}{d}$, that is, $k=d^2$.',
        'So $k$ is a perfect square, and $\\sqrt{k}$ is an integer.',
        'The others are not necessarily true: $k=4$ has $3$ divisors, but $4$ is not prime, not odd, and $\\sqrt{4}=2$ is even.'])
    S('q-418', stem='Maya reads a book for $5$ days. On the first day she reads $30$ pages. On each of the other days she reads the smallest prime number of pages that is greater than the number of pages she read the day before. How many pages does she read on the fifth day?',
      choices=['$41$', '$37$', '$43$', '$47$'], correct=3, expl=[
        'Day 1: $30$ pages. Day 2: the next prime after $30$ is $31$.',
        'Day 3: $37$ ($32$, $34$, $36$ are even, $33=3\\cdot11$ and $35=5\\cdot7$). Day 4: $41$ ($38$ and $40$ are even, and $39=3\\cdot13$).',
        'Day 5: $43$ ($42$ is even).'])
    S('q-419', stem='$n$ is a positive integer. The fraction $\\frac{n}{20}$ is in lowest terms (it cannot be reduced), and it is less than $1$. How many different values can $n$ have?',
      choices=['$7$', '$8$', '$9$', '$10$'], correct=2, expl=[
        'Less than $1$: $n<20$.',
        'Cannot be reduced: $n$ shares no prime with $20=2^2\\cdot5$. So $n$ is not divisible by $2$ or by $5$.',
        'From $1$ to $19$: $1$, $3$, $7$, $9$, $11$, $13$, $17$, $19$. That is $8$ values.'])
    S('q-420', stem='$t$ is a positive integer. $t$ has exactly three different divisors (including $1$ and $t$). Which of the following is necessarily true about $\\sqrt{t}$?',
      choices=['$\\sqrt{t}$ is odd', '$\\sqrt{t}$ is not an integer', '$\\sqrt{t}$ is prime', '$\\sqrt{t}$ is divisible by $3$'], correct=3, expl=[
        'Exactly three divisors means $t=p^2$ for a prime $p$. Its divisors are $1$, $p$ and $p^2$.',
        'Then $\\sqrt{t}=\\sqrt{p^2}=p$, a prime ✓.',
        'The others are not necessarily true: $t=4$ gives $\\sqrt{t}=2$, which is even and not divisible by $3$. And $\\sqrt{t}=p$ is always an integer.'])
    S('q-421', stem='$n$ is a positive integer. $n^2$ has a divisor that is greater than $3n$ and different from $n^2$. What is the smallest possible value of $n$?',
      choices=['$9$', '$6$', '$10$', '$8$'], correct=4, expl=[
        'Check the choices, starting from the smallest.',
        '$n=6$: the divisors of $36$ are $1$, $2$, $3$, $4$, $6$, $9$, $12$, $18$, $36$. Only $36$ itself is greater than $18$ ✗.',
        '$n=8$: the divisors of $64$ include $32$, and $32>24$ ✓. ($n=1$ to $5$ and $n=7$ fail too: for example, the divisors of $49$ are only $1$, $7$ and $49$.)',
        'So the smallest $n$ is $8$.'])
    S('q-422', stem='Tom says: "Every number that is divisible by both $6$ and $9$ is also divisible by $54$."\nRina says: "Every number that is divisible by both $6$ and $9$ is also divisible by $18$."\nWhich of the following is correct?',
      choices=['Both are right.', 'Only Tom is right.', 'Only Rina is right.', 'Both are wrong.'], correct=3, expl=[
        '$6=2\\cdot3$ and $9=3^2$. The LCM takes every prime at its higher power: $2\\cdot3^2=18$. So every such number is divisible by $18$: Rina is right.',
        'Tom is wrong: $18$ is divisible by $6$ and by $9$, but not by $54$.',
        '$54$ is just $6\\cdot9$. The product is too big because $6$ and $9$ share a factor of $3$.'])

    # ============================== practice clean-up (approved): copy out, 2 warm-ups, September items only for new types
    E = 'alg-extra-unit-t14-4-%d'
    for qid in [E % 5,                              # copy of the guided "which is prime" question
                E % 3, E % 4, E % 6, E % 7,         # extra warm-ups beyond the kept ones
                P(5), P(6), P(9), P(13)]:           # September items whose type the practice already has
        M.unplace(qid)
    M.practice_order('unit-t14-4', [
        E % 1, E % 2, 'q-404', 'q-406', 'q-411', 'q-405', 'q-409', 'q-413', 'q-418', 'q-403', 'q-412', 'q-410',
        P(10), P(12), 'q-414', 'q-419', 'q-407', P(15), 'q-415', 'q-416', 'q-420', 'q-417', 'q-422', P(7),
        'q-408', 'q-421'])


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber(M)   # 2026-10-06 renumber pass: runs last


# =====================================================================================================================
# 2026-10-06 Hebrew back-check: the renumbered questions / examples were compared with the teacher's HEBREW VIDEO
# subtitles (01-Algebra-Original-Subtitles.txt, lines 13683-14768). Where a new version had landed back on the Hebrew
# video's own numbers / letters / wording, it gets new ones here (same type, trap, difficulty and methods).
# Nothing in topic 14 is recorded. Runs last. See t14_CHANGES.md ("2026-10-06 Hebrew back-check").
# =====================================================================================================================
def hebrew_backcheck(M):
    def S(qid, **kw):
        q = M.set_q(qid, **kw)
        v = M.D['videos'].get('solve-' + qid)
        if v:
            v['title'] = v['navLabel'] = q['stem']; M.touched_videos.add(v['id'])

    # lesson "Prime Numbers": "twenty, eighteen" (even, not prime) was the Hebrew lesson's pair
    _sub(M, LESSON_A, 3, [('twenty, eighteen…', 'fourteen, thirty…')])
    # summary: "39 = 2 + 37" was a choice of the Hebrew sample question (31, 37, 33, 39)
    _sub(M, 'r26-t14-summary', 3, [('Write "39 = 2 + 37"', 'Write "73 = 2 + 71"'),
                                    ('Thirty-nine as a sum of two primes? Two plus thirty-seven.',
                                     'Seventy-three as a sum of two primes? Two plus seventy-one.')])

    # q-388: x = 5·3²·6², "35 does not divide" = the Hebrew video's answer (x = 2·5³·6², 35) -> x = 3·5²·10², 22
    S('q-388', stem='Given: $x=3\\cdot5^2\\cdot10^2$. Which of the following numbers does not divide $x$?',
      choices=['$20$', '$22$', '$75$', '$60$'], correct=2, expl=[
        'Break the non-prime factor into primes: $10^2=(2\\cdot5)^2=2^2\\cdot5^2$. Therefore $x=2^2\\cdot3\\cdot5^4$.',
        'Check each choice: $20=2^2\\cdot5$ ✓, $75=3\\cdot5^2$ ✓, $60=2^2\\cdot3\\cdot5$ ✓.',
        '$22=2\\cdot11$, and $x$ has no $11$. So $22$ does not divide $x$.'])
    M.set_slide('solve-q-388', 2, script=[
        "Not a divisor means: it's not a factor of x. You can't build it from x's primes.",
        "So check each answer: does it need a prime that x doesn't have?",
        "But first — ten isn't a prime. Unpack it.",
        D('Under x write "10² = 2² · 5²  →  x = 2² · 3 · 5⁴"'),
        "Ten squared is two squared times five squared. So x has two twos, a three, and four fives.",
        D('Next to choice 1 write "2² · 5 ✓"'),
        "Twenty: two twos and a five. Both twos come from the ten squared. In stock.",
        D('Next to choice 3 write "3 · 5² ✓"'),
        "Seventy-five: a three and two fives. All there.",
        D('Next to choice 4 write "2² · 3 · 5 ✓"'),
        "Sixty: two twos, a three and a five. It divides.",
        D('Next to choice 2 write "2 · 11 — no 11!" and circle choice 2'),
        "Twenty-two: two times eleven. The two is there — but there's no eleven anywhere in x. Choice two."])

    # q-391: choice 31 (= 2 + 29) was a choice of the Hebrew video, with the same split -> 21 (= 2 + 19)
    S('q-391', choices=['$15$', '$21$', '$51$', '$43$'], correct=3, expl=[
        'All four choices are odd. An odd sum of two primes needs one even prime, and the only even prime is $2$.',
        'So check whether the choice minus $2$ is prime.',
        '$15=2+13$ ✓. $21=2+19$ ✓. $43=2+41$ ✓ ($41$ is prime: $\\sqrt{41}<7$, and $2$, $3$, $5$ do not divide it).',
        '$51=2+49$, and $49=7^2$ is not prime ✗. So the sum cannot be $51$.'])
    _sub(M, 'solve-q-391', 2, [('Split fifteen into two primes, then thirty-one…', 'Split fifteen into two primes, then twenty-one…'),
                               ('Next to 31 write "2 + 29 ✓"', 'Next to 21 write "2 + 19 ✓"'),
                               ('Thirty-one: two plus twenty-nine. Twenty-nine is prime. Possible too.',
                                'Twenty-one: two plus nineteen. Nineteen is prime. Possible too.')])

    # q-394: z = p^r·q^s with p, q, r, s = 2, 3, 5, 7 gave z = 2⁵·3⁷, 2³·3⁵, 7 ... = the Hebrew video's numbers
    #        -> z = p^s·q^r (z = 2⁷·3⁵), answer p^r·q^q (2⁵·3³)
    S('q-394', stem='$p$, $q$, $r$, $s$ are prime numbers, and $p<q<r<s$.\nGiven: $z=p^s\\cdot q^r$.\nWhich of the following necessarily divides $z$?',
      choices=['$r$', '$p^r\\cdot q^q$', '$q^s$', '$s^q$'], correct=2, expl=[
        '$z$ is built from the prime $p$ ($s$ times) and the prime $q$ ($r$ times).',
        '$p^r$: $r<s$, therefore $z$ has enough $p$s ✓. $q^q$: $q<r$, therefore $z$ has enough $q$s ✓. So $p^r\\cdot q^q$ divides $z$.',
        '$q^s$: $z$ has only $r$ copies of $q$, and $r<s$ ✗. $r$ and $s^q$: the primes $r$ and $s$ are not factors of $z$ at all ✗.',
        'With the smallest primes: $p=2$, $q=3$, $r=5$, $s=7$ give $z=2^7\\cdot3^5$, and of the four choices only $2^5\\cdot3^3$ divides it.'])
    M.set_slide('solve-q-394', 2, script=[
        "This is a factors question. What is z actually built from?",
        D('Under z write "p … s times, q … r times"'),
        "z contains the prime p — s times. And the prime q — r times.",
        "Is z divisible by p? Of course. By q? Of course. By r or s? No — those primes aren't in z at all.",
        "First look at the choices — what can we kill fast?",
        D('Cross out choice 1'),
        "Choice one, r. Out immediately. r only shows up as an exponent — it's how MANY times q appears, not a factor of z.",
        D('Cross out choice 4'),
        "Choice four, s to the q. z has no factor s. Out.",
        "Choice three: q to the s. z has q only r times — and s is bigger than r. Not enough q's.",
        D('Cross out choice 3'),
        "Three are out — on the exam, mark the one that's left.",
        D('Circle choice 2'),
        "In the lesson — why it works. p to the r: z has p s times, and r is less than s. Enough. q to the q: z has q r times, and q is less than r. Enough. Choice two."])
    M.set_slide('solve-q-394', 3, script=[
        "Hard to follow with letters? Same idea — with numbers.",
        "Smallest primes, in order: p is two, q is three, r is five, s is seven.",
        D('Write "z = 2⁷ · 3⁵"'),
        "z is two to the seventh times three to the fifth.",
        D('Next to choice 1 write "5 ✗"'),
        "Choice one: five. z is built only from twos and threes. Out.",
        D('Next to choice 2 write "2⁵ · 3³ ✓"'),
        "Choice two: two to the fifth times three cubed. Two five times — z has seven. Three three times — z has five. It fits.",
        "But we're plugging in — so we must knock out three choices before marking. It might only work for these numbers.",
        D('Next to choice 3 write "3⁷ ✗"'),
        "Choice three: three to the seventh. z only has three five times. Too many. Out.",
        D('Next to choice 4 write "7³ ✗"'),
        "Choice four: seven cubed. No seven in z at all. Out.",
        D('Circle choice 2'),
        "Choice two. Strong without numbers? Great. If not — plugging in is an excellent route."])

    # q-395: statement (4) "at least one of a, b, c is divisible by 5" was word for word the Hebrew video's statement
    #        -> the 5 and the 7 swap roles in statements (3) and (4)
    S('q-395', choices=['It is possible that exactly one of $a$, $b$, $c$ is divisible by $35$.',
                        'The number of different prime divisors of $x^2$ is greater than that of $x$.',
                        'If $b$ and $c$ are not divisible by $5$, then $a^2$ is divisible by $25$.',
                        'At least one of $a$, $b$, $c$ is divisible by $7$.'], correct=2, expl=[
        '(1) Possible: $a=35$, $b=1$, $c=2$ ✓.',
        '(2) Never true: squaring doubles the exponents but adds no new prime. For example, $35=5\\cdot7$ and $35^2=1225=5^2\\cdot7^2$ have the same two primes.',
        '(3) Always true: $5$ is prime and divides $a\\cdot b\\cdot c$. It does not divide $b$ or $c$, therefore it divides $a$. Then $a^2$ is divisible by $5^2=25$.',
        '(4) Always true: $7$ is prime and divides $a\\cdot b\\cdot c$, therefore it divides one of the factors.',
        'Never true is also "not necessarily true", therefore the answer is (2).'])
    M.set_slide('solve-q-395', 2, script=[
        "First, the given. x is divisible by thirty-five — so x must contain the primes five and seven.",
        D('Next to the stem write "35 = 5 · 7"'),
        "x is a times b times c. So at least one of them brings the five, and at least one brings the seven.",
        A("'A prime divides a · b → it divides a or b' appears", T('A prime divides a product $\\to$ it divides one of the factors', size=38)),
        "That's the rule: a prime can't be split between factors — one of them holds it. Thirty-five isn't prime, so its five and its seven may come from different numbers.",
        "Statement four: at least one of them is divisible by seven. Someone had to bring the seven. True for sure.",
        "Maybe one number brings both — thirty-five, one, two. Maybe they split the job — five, seven, one. Either way, someone holds the seven.",
        D('Cross out choice 4'),
        "Statement one: it's possible that exactly one is divisible by thirty-five. Sure — thirty-five, one and two.",
        D('Write "35, 1, 2 ✓" and cross out choice 1'),
        "Possible. Out.",
        "Statement three: if b and c aren't divisible by five — who brought the five? a must have.",
        D('Next to choice 3 write "5 | a → 25 | a²"'),
        "Square a, and the five appears twice. So a squared is divisible by twenty-five.",
        "Numbers: five, seven, one — a squared is twenty-five. Or ten, seven, one — a hundred. Both are divisible by twenty-five.",
        D('Cross out choice 3'),
        "Three statements out — on the exam you mark the one that's left. This is probably the last question in the section anyway.",
        D('Circle choice 2'),
        "In the lesson, let's learn from statement two. Notice the word: DIFFERENT prime divisors.",
        D('Write "35 = 5·7 → 35² = 5²·7²"'),
        "Square x, and the same primes just appear twice as often. No NEW prime shows up.",
        "So the number of different prime divisors stays exactly the same — never greater. Choice two.",
        "One more word. Statement two is NEVER true.",
        "Never true is also \"not necessarily true\". So it's the answer."])

    # q-396: primes {3, 5} / {3, 7}, b < a, ab/35 -> 27 = the Hebrew video exactly -> {2, 3} / {2, 5}, ab/15 -> 8
    S('q-396', stem='$a$ and $b$ are positive integers. $a$ has exactly two prime factors: $2$ and $3$. $b$ has exactly two prime factors: $2$ and $5$.\nGiven: $b<a$.\nWhat is the smallest possible value of $\\frac{a\\cdot b}{15}$?',
      choices=['$8$', '$4$', '$16$', '$12$'], correct=1, expl=[
        'Numbers with exactly the prime factors $2$ and $3$: $6$, $12$, $18$, $24$, … Numbers with exactly the prime factors $2$ and $5$: $10$, $20$, $40$, …',
        'The expression is smallest when $a$ and $b$ are smallest. The smallest $b$ is $10$. Since $b<a$, $a=6$ is too small. The smallest $a$ above $10$ is $12$.',
        '$\\frac{a\\cdot b}{15}=\\frac{12\\cdot10}{15}=\\frac{120}{15}=8$. (With $a=6$, ignoring $b<a$, you get $4$ — the trap.)'])
    M.set_slide('solve-q-396', 2, script=[
        "When is the expression smallest? When a is smallest and b is smallest.",
        "a is built from twos and threes only — but from BOTH. Smallest: one two, one three.",
        D('Write "a = 2 · 3 = 6"'),
        "Six.",
        D('Write "b = 2 · 5 = 10"'),
        "b is built from twos and fives. Smallest: ten.",
        "But wait — a must be bigger than b. Six isn't bigger than ten.",
        "So we have to grow a. By how much? a may only contain twos and threes — so times two, or times three.",
        D('Write "a = 2² · 3 = 12"'),
        "Keep it as small as possible: times two. a becomes twelve. Bigger than ten — good.",
        D('Write "(2² · 3)(2 · 5) / (3 · 5)"'),
        "Now plug in. Twelve times ten, over fifteen.",
        D('Cancel the 3s and the 5s; write "= 2³ = 8"'),
        "The three and the five cancel with fifteen. Two cubed — eight.",
        D('Circle choice 1'),
        "Choice one."])

    # practice q-412: 17, 33, 27, 39 -> 33 (33 + 2 = 35) shared 33, 39 and the key 35 with the Hebrew video -> 85 (87)
    S('q-412', choices=['$17$', '$85$', '$27$', '$45$'], correct=2, expl=[
        'All four choices are odd. An odd difference of two primes needs one even prime: $2$. So the bigger prime is the choice plus $2$.',
        '$17+2=19$ ✓, $27+2=29$ ✓, $45+2=47$ ✓ — all prime.',
        '$85+2=87=3\\cdot29$ is not prime (a fake prime: $8+7=15$ is divisible by $3$) ✗. So the difference cannot be $85$.'])
    # practice q-416: same choices / answer position / example (√3) as the Hebrew video -> new order, example √13
    S('q-416', choices=['$w$ is even', '$w$ is not an integer', '$w$ is odd', '$w$ is less than $6$'], correct=2, expl=[
        'If $w$ were an integer greater than $1$, then $w^2=w\\cdot w$ would break into two factors greater than $1$. It would not be prime.',
        'So $w$ is not an integer. Example: $w=\\sqrt{13}$ gives $w^2=13$, a prime.',
        '$w$ does not have to be small: $w=\\sqrt{89}$ gives $w^2=89$, a prime, and $\\sqrt{89}>9$. So choice 4 is not necessarily true.'])


_apply_before_hebrew_backcheck = apply


def apply(M):
    _apply_before_hebrew_backcheck(M)
    hebrew_backcheck(M)   # 2026-10-06 Hebrew back-check: runs last


# ---------------------------------------------------------------- 2026-10-07 pen or click
# Teacher-approved split (2026-10-04/06): lessons - content appears by click, the pen only marks (circle, tick, box,
# underline, cross out); solution videos - setup and mechanical lines by click, by hand only the one or two key steps
# plus the marks on the choices (very short notes next to a choice count as marks). The factor tree and the marks on
# the number line stay by hand. Runs LAST (after renumber and hebrew_backcheck), on the final text. No topic 14 video
# is recorded. Helper copied from t10.py (same behaviour).
def _pen_or_click_slide(M, vid, n, repl, room=(), row=106):
    """repl: pen cue text -> script entries replacing it. room: pen cues kept by hand that need their own row on the
    board - the item above them gets a bigger gap, so the click items below leave space for the handwriting."""
    b = M.slide(vid, n); script = []; done = set()
    for l in b['lines']:
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        elif l['draw'] in repl: script.extend(repl[l['draw']]); done.add(l['draw'])
        else: script.append(D(l['draw']))
    missing = (set(repl) - done) | (set(room) - {l.get('draw') for l in b['lines']})
    assert not missing, '%s #%d: draw cue not found: %s' % (vid, n, missing)
    M.set_slide(vid, n, script=script)
    b = M.slide(vid, n); last = b['pre'] - 1
    for l in b['lines']:
        if 'appear' in l: last = l['appear']
        elif l.get('draw') in room: b['items'][last]['gap'] = b['items'][last].get('gap', 44) + row


def _gaps(M, vid, n, gap):
    """the board no longer needs the empty rows that were kept for handwriting: close them."""
    for it in M.slide(vid, n)['items']:
        if it.get('k') == 't' and it.get('gap', 0) > gap: it['gap'] = gap


def pen_or_click(M):
    S = 38
    # ---- lesson: Prime Numbers (written lines -> clicks; circle, ticks, factor tree, underline by hand)
    V = LESSON_A
    _pen_or_click_slide(M, V, 2, {
        'Under 17 write "can\'t break"; under 15 write "= 3 · 5"': [A('can\'t break / = 3 · 5 appear under 17 and 15',
            dict(k='row', items=["can't break", '$=3\\cdot5$'], sp=300, size=40, below=40))],
    })
    M.slide(V, 2)['items'][1]['below'] = 16
    _pen_or_click_slide(M, V, 3, {
        'Write "25 = 2 + 23"': [A('25 = 2 + 23 appears', T(r'$25=2+23$', size=46))],
    })
    _pen_or_click_slide(M, V, 4, {
        'Next to 23 and 29, tick them; write "21, 22, 24–28 ✗"': [
            D('Tick 23 and 29'), A('Between 20 and 30: 23, 29 appears',
                                   T(r'Between $20$ and $30$: $\ 23,\ 29$ $\quad$ ($21,\ 22,\ 24$–$28$ ✗)', size=42))],
    })
    _gaps(M, V, 4, 30)
    _pen_or_click_slide(M, V, 5, {
        'Write "91 ÷ 7 = 13  →  91 = 7 · 13  ✗"': [A('91 ÷ 7 = 13 → 91 = 7 · 13 ✗ appears', T(r'$91\div7=13 \;\to\; 91=7\cdot13$ ✗', size=46))],
    })
    _pen_or_click_slide(M, V, 6, {
        'Next to it write "3 is a factor of 24"': [A('3 is a factor of 24 appears', T(r'$3$ is a factor of $24$', size=44))],
        'Next to it write "7 is a factor of 35"': [A('7 is a factor of 35 appears', T(r'$7$ is a factor of $35$', size=44))],
    })
    _gaps(M, V, 6, 24)
    _pen_or_click_slide(M, V, 7, {
        'Under 6 write "2·3"; under 9 write "3·3"; under 18 write "2·3·3"': [A('2·3, 3·3, 2·3·3 appear under 6, 9, 18',
            dict(k='row', items=['', '', '$2\\cdot3$', '$3\\cdot3$', '$2\\cdot3\\cdot3$'], sp=180, size=38, below=30))],
    })
    M.slide(V, 7)['items'][1]['below'] = 12
    _pen_or_click_slide(M, V, 8, {
        'Next to the tree write "150 = 2 · 3 · 5²"': [A('150 = 2 · 3 · 5² appears', T(r'$150=2\cdot3\cdot5^2$', size=50))],
    })
    M.slide(V, 8)['items'][0]['gap'] = 330    # the whole factor tree fits above the click line
    # ---- Q: q-387 - by hand: 3⁶ = 729 ✗ (every bigger prime is too big), circle
    _pen_or_click_slide(M, 'solve-q-387', 2, {
        'Write "2⁶ = 64 ✓ two digits"': [A('2⁶ = 64 ✓ two digits appears', T(r'$2^6=64$ ✓ two digits', size=S))],
        'Write "9x = 9 · 2 = 18" and circle choice 2': [A('9x = 9 · 2 = 18 appears', T(r'$9x=9\cdot2=18$', size=S)), D('Circle choice 2')],
    }, room=['Write "3⁶ = 729 ✗"'], row=70)
    # ---- Q: q-r26-t14-01 - by hand: √113 < 11 -> try 2, 3, 5, 7 (next to choice 3), circle
    _pen_or_click_slide(M, 'solve-q-r26-t14-01', 2, {
        'Next to choice 1 write "91 = 7 · 13 ✗"': [A('(1) 91 = 7 · 13 ✗ appears', T(r'(1) $91=7\cdot13$ ✗', size=S))],
        'Next to choice 2 write "119 = 7 · 17 ✗"': [A('(2) 119 = 7 · 17 ✗ appears', T(r'(2) $119=7\cdot17$ ✗', size=S))],
        'Next to choice 4 write "133 = 7 · 19 ✗"': [A('(4) 133 = 7 · 19 ✗ appears', T(r'(4) $133=7\cdot19$ ✗', size=S))],
        'Write "odd · 1 + 1 + 3 = 5 · no 0 or 5 · 113 = 7 · 16 + 1"': [A('113: odd, digit sum 5, no 0 or 5, 7 · 16 + 1 appears',
            T(r'$113$: odd $\cdot\ 1+1+3=5\ \cdot$ no $0$ or $5$ $\cdot\ 113=7\cdot16+1$', size=34))],
    })
    # ---- Q: q-388 - by hand: unpack 10² (x = 2² · 3 · 5⁴), "2 · 11 — no 11!" on choice 2, circle
    _pen_or_click_slide(M, 'solve-q-388', 2, {
        'Next to choice 1 write "2² · 5 ✓"': [A('(1) 20 = 2² · 5 ✓ appears', T(r'(1) $20=2^2\cdot5$ ✓', size=S))],
        'Next to choice 3 write "3 · 5² ✓"': [A('(3) 75 = 3 · 5² ✓ appears', T(r'(3) $75=3\cdot5^2$ ✓', size=S))],
        'Next to choice 4 write "2² · 3 · 5 ✓"': [A('(4) 60 = 2² · 3 · 5 ✓ appears', T(r'(4) $60=2^2\cdot3\cdot5$ ✓', size=S))],
    }, room=['Under x write "10² = 2² · 5²  →  x = 2² · 3 · 5⁴"'], row=70)
    # ---- Q: q-386 - by hand: circle the primes, shade, cross out on the number line, circle
    _pen_or_click_slide(M, 'solve-q-386', 2, {
        'Write "30 · 44 = 1320" and circle choice 3': [A('30 · 44 = 1320 appears', T(r'$30\cdot44=1320$', size=S)), D('Circle choice 3')],
    })
    # ---- lesson: Factor Tools (written lines -> clicks; the box by hand)
    V = LESSON_B
    _pen_or_click_slide(M, V, 3, {
        'Write "3: 0, 1, 2, 3 → 4 options" and "5: 0, 1, 2 → 3 options"': [
            A('3: 0, 1, 2, 3 → 4 options appears', T(r'$3$: $\ 0,\ 1,\ 2,\ 3 \;\to\; 4$ options', size=46)),
            A('5: 0, 1, 2 → 3 options appears', T(r'$5$: $\ 0,\ 1,\ 2 \;\to\; 3$ options', size=46))],
        'Write "4 · 3 = 12 divisors"': [A('4 · 3 = 12 divisors appears', T(r'$4\cdot3=12$ divisors', size=46))],
    })
    _gaps(M, V, 3, 24)
    # ---- Q: q-389 - by hand: the circles on the shared primes, cross out r, circle
    _pen_or_click_slide(M, 'solve-q-389', 2, {
        'Write "p · q² · s" and circle choice 3': [A('p · q² · s appears', T(r'$p\cdot q^2\cdot s$', size=S)), D('Circle choice 3')],
    })
    # ---- Q: q-390 - by hand: each prime at its HIGHER power, circle
    _pen_or_click_slide(M, 'solve-q-390', 2, {
        'Write "10 = 2 · 5" and "25 = 5²"': [A('10 = 2 · 5, 25 = 5² appears', T(r'$10=2\cdot5 \qquad 25=5^2$', size=S))],
        'Write "2 · 5² = 50" and circle choice 3': [A('2 · 5² = 50 appears', T(r'$2\cdot5^2=50$', size=S)), D('Circle choice 3')],
    }, room=['Write "2: only 2¹ → 2;   5: 5¹ and 5² → 5²"'], row=64)
    # ---- Q: q-398 - by hand: "2 · 3 · 5 — no 2!" on choice 2, circle
    _pen_or_click_slide(M, 'solve-q-398', 2, {
        'Next to choice 1 write "3 · 3 · 5 → 335 ✓"': [A('(1) 45 = 3 · 3 · 5 → 335 ✓ appears', T(r'(1) $45=3\cdot3\cdot5 \;\to\; 335$ ✓', size=S))],
        'Next to choice 3 write "1 · 5 · 5 → 155 ✓"': [A('(3) 25 = 1 · 5 · 5 → 155 ✓ appears', T(r'(3) $25=1\cdot5\cdot5 \;\to\; 155$ ✓', size=S))],
        'Next to choice 4 write "1 · 3 · 5 → 135 ✓"': [A('(4) 15 = 1 · 3 · 5 → 135 ✓ appears', T(r'(4) $15=1\cdot3\cdot5 \;\to\; 135$ ✓', size=S))],
    })
    # ---- Q: q-399 - by hand: 48 − 0 = 48 (the 10 · 10 pair gives 0), circle
    _pen_or_click_slide(M, 'solve-q-399', 2, {
        'Write the pairs: 2·50 → 48, 4·25 → 21, 5·20 → 15, 10·10 → 0': [A('The four pairs and their differences appear',
            T(r'$50-2=48 \qquad 25-4=21 \qquad 20-5=15 \qquad 10-10=0$', size=S))],
    })
    # ---- Q: q-400 - by hand: 2 · 5 · 7 = 70 (don't forget all three cards), circle
    _pen_or_click_slide(M, 'solve-q-400', 2, {
        'Write "2 · 5 = 10", "2 · 7 = 14", "5 · 7 = 35"': [A('2 · 5 = 10, 2 · 7 = 14, 5 · 7 = 35 appear',
            T(r'$2\cdot5=10 \qquad 2\cdot7=14 \qquad 5\cdot7=35$', size=S))],
        'Write "70 + 35 + 14 + 10 = 129" and circle choice 1': [A('70 + 35 + 14 + 10 = 129 appears',
            T(r'$70+35+14+10=129$', size=S)), D('Circle choice 1')],
    }, room=['Write "2 · 5 · 7 = 70"'], row=70)
    # ---- Q: q-401 - by hand: m² = m · m -> breaks (method 1, unchanged), m² = 5 -> m = √5 (method 2), circles
    _pen_or_click_slide(M, 'solve-q-401', 3, {
        'Write "m² = 2 → m = √2"': [A('m² = 2 → m = √2 appears', T(r'$m^2=2 \;\to\; m=\sqrt2$', size=S))],
    }, room=['Write "m² = 5 → m = √5"'], row=70)
    # ---- Q: q-402 - by hand: 3 divisors -> k = p², circle
    _pen_or_click_slide(M, 'solve-q-402', 2, {
        'Write "C = √k = p → prime"': [A('C = √k = p → prime appears', T(r'$C=\sqrt k=p \;\to\;$ prime', size=S))],
        'Write "divisors of C: 1, p → 2" and circle choice 4': [A('divisors of C: 1, p → 2 appears',
            T(r'divisors of $C$: $\ 1,\ p \;\to\; 2$', size=S)), D('Circle choice 4')],
    }, room=['Write "3 divisors → k = p²"'], row=50)
    its = M.slide('solve-q-402', 2)['items']          # (+ the row for k = p²) the rule, C = √k, divisors of C
    for it, g in zip(its[0:], (44 + 50, 10, 10, 10)): it['gap'] = g
    for it in its[1:]: it['size'] = min(it.get('size', 46), 34)
    # ---- lesson: More Factor Tools
    _pen_or_click_slide(M, TRICKS, 2, {
        'Write "12k = 2² · 3 · k → k = 3 → 36 = 6² ✓"': [A('12k = 2² · 3 · k → k = 3 → 36 = 6² ✓ appears',
            T(r'$12k=2^2\cdot3\cdot k \;\to\; k=3 \;\to\; 36=6^2$ ✓', size=44))],
    })
    # ---- Q: q-r26-t14-03 - by hand: 108 = 4 · 27 = 2² · 3³ (break it), circle
    _pen_or_click_slide(M, 'solve-q-r26-t14-03', 2, {
        'Write "2ᵃ · 3ᵇ = 2² · 3³ → a = 2, b = 3"': [A('2ᵃ · 3ᵇ = 2² · 3³ → a = 2, b = 3 appears', T(r'$2^a\cdot3^b=2^2\cdot3^3 \;\to\; a=2,\ b=3$', size=S))],
        'Write "a − b = 2 − 3 = −1"': [A('a − b = 2 − 3 = −1 appears', T(r'$a-b=2-3=-1$', size=S))],
    }, room=['Write "108 = 4 · 27 = 2² · 3³"'], row=70)
    # ---- Q: q-391 - by hand: "odd" next to each choice, "= 2 + ?" next to the stem, cross-outs, circle
    _pen_or_click_slide(M, 'solve-q-391', 2, {
        'Next to 15 write "2 + 13 ✓"': [A('(1) 15 = 2 + 13 ✓ appears', T(r'(1) $15=2+13$ ✓', size=S))],
        'Next to 21 write "2 + 19 ✓"': [A('(2) 21 = 2 + 19 ✓ appears', T(r'(2) $21=2+19$ ✓', size=S))],
        'Next to 51 write "2 + 49 = 7 · 7 ✗"': [A('(3) 51 = 2 + 49, 49 = 7 · 7 ✗ appears', T(r'(3) $51=2+49$, $\ 49=7\cdot7$ ✗', size=S))],
    })
    # ---- Q: q-392 - by hand: the primes written under the numbers of the stem, the circles; method 2 unchanged
    _pen_or_click_slide(M, 'solve-q-392', 2, {
        'Write "a · b = 7 · 13 = 91" and circle choice 3': [A('a · b = 7 · 13 = 91 appears', T(r'$a\cdot b=7\cdot13=91$', size=S)), D('Circle choice 3')],
    })
    # ---- Q: q-393 - by hand: a(b + 4) = 48 (common factor), cross-outs, circle
    _pen_or_click_slide(M, 'solve-q-393', 2, {
        'Write "1 × 48 → b = 44, a + b = 45"': [A('1 × 48 → b = 44, a + b = 45 appears', T(r'$1\times48 \;\to\; b=44,\ a+b=45$', size=34))],
        'Write "2 × 24 → b = 20, a + b = 22"': [A('2 × 24 → b = 20, a + b = 22 appears', T(r'$2\times24 \;\to\; b=20,\ a+b=22$', size=34))],
        'Write "3 × 16 → b = 12, a + b = 15"': [A('3 × 16 → b = 12, a + b = 15 appears', T(r'$3\times16 \;\to\; b=12,\ a+b=15$', size=34))],
        'Write "4 × 12 → b = 8, a + b = 12"': [A('4 × 12 → b = 8, a + b = 12 appears', T(r'$4\times12 \;\to\; b=8,\ a+b=12$', size=34))],
    }, room=['Under the stem write "a(b + 4) = 48"'], row=60)
    for it in M.slide('solve-q-393', 2)['items'][2:]: it['gap'] = 10
    # ---- Q: q-396 - by hand: grow a: a = 2² · 3 = 12, cancel, circle
    _pen_or_click_slide(M, 'solve-q-396', 2, {
        'Write "a = 2 · 3 = 6"': [A('a = 2 · 3 = 6 appears', T(r'$a=2\cdot3=6$', size=S))],
        'Write "b = 2 · 5 = 10"': [A('b = 2 · 5 = 10 appears', T(r'$b=2\cdot5=10$', size=S))],
        'Write "(2² · 3)(2 · 5) / (3 · 5)"': [A('(2² · 3)(2 · 5) / (3 · 5) appears', T(r'$\frac{(2^2\cdot3)(2\cdot5)}{3\cdot5}$', size=S))],
        'Cancel the 3s and the 5s; write "= 2³ = 8"': [D('Cancel the 3s and the 5s'), A('= 2³ = 8 appears', T(r'$=2^3=8$', size=S))],
    }, room=['Write "a = 2² · 3 = 12"'], row=64)
    its = M.slide('solve-q-396', 2)['items']          # a = 6, b = 10 (+ the row for a = 12), the fraction, = 8
    for it, g in zip(its[1:], (12, 12 + 64, 12, 12)): it['gap'] = g
    # ---- Q: q-394 - by hand: what z is built from (method 1, unchanged), the short marks on the choices, circles
    _pen_or_click_slide(M, 'solve-q-394', 3, {
        'Write "z = 2⁷ · 3⁵"': [A('z = 2⁷ · 3⁵ appears', T(r'$z=2^7\cdot3^5$', size=S))],
    })
    # ---- Q: q-395 - by hand: "35, 1, 2 ✓" on choice 1, 5 | a -> 25 | a² on choice 3 (the key), cross-outs, circle
    _pen_or_click_slide(M, 'solve-q-395', 2, {
        'Next to the stem write "35 = 5 · 7"': [A('35 = 5 · 7 appears', T(r'$35=5\cdot7$', size=S))],
        'Write "35 = 5·7 → 35² = 5²·7²"': [A('35 = 5·7 → 35² = 5²·7² appears', T(r'$35=5\cdot7 \;\to\; 35^2=5^2\cdot7^2$', size=S))],
    })
    # ---- Q: q-397 - by hand: 4 = 2² -> 1, 2, 4 (method 1), the pattern 25, 49, 121, 169 (method 2), circles
    _pen_or_click_slide(M, 'solve-q-397', 2, {
        'Write "prime → 2 divisors"': [A('prime → 2 divisors appears', T(r'prime $\;\to\; 2$ divisors', size=34))],
        'Write "6 = 2 · 3 → 1, 2, 3, 6"': [A('6 = 2 · 3 → 1, 2, 3, 6 appears', T(r'$6=2\cdot3 \;\to\; 1,\ 2,\ 3,\ 6$', size=34))],
        'Write "p² < 200 → p ≤ 14"': [A('p² < 200 → p ≤ 14 appears', T(r'$p^2<200 \;\to\; p\le14$', size=34))],
        'Write "2, 3, 5, 7, 11, 13 → 4, 9, 25, 49, 121, 169"': [A('2, 3, 5, 7, 11, 13 → 4, 9, 25, 49, 121, 169 appears',
            T(r'$2,\ 3,\ 5,\ 7,\ 11,\ 13 \;\to\; 4,\ 9,\ 25,\ 49,\ 121,\ 169$', size=34))],
    }, room=['Write "4 = 2² → 1, 2, 4"'], row=48)
    its = M.slide('solve-q-397', 2)['items']          # prime, 6 (+ the row for 4 = 2²), p² < 200, the list
    for it, g in zip(its[1:], (6, 6 + 48, 6, 6)): it['gap'] = g; it['size'] = 32
    _pen_or_click_slide(M, 'solve-q-397', 3, {
        'Write "1 → 1", "2, 3 → 2 divisors"': [A('1 → 1, 2 and 3 → 2 divisors appears', T(r'$1 \;\to\; 1 \qquad 2,\ 3 \;\to\; 2$ divisors', size=S))],
        'Write "4 → 1, 2, 4 ✓"': [A('4 → 1, 2, 4 ✓ appears', T(r'$4 \;\to\; 1,\ 2,\ 4$ ✓', size=S))],
        'Write "9 → 1, 3, 9 ✓"': [A('9 → 1, 3, 9 ✓ appears', T(r'$9 \;\to\; 1,\ 3,\ 9$ ✓', size=S))],
    })
    # ---- lesson: Summary
    V = 'r26-t14-summary'
    _pen_or_click_slide(M, V, 3, {
        'Write "73 = 2 + 71"': [A('73 = 2 + 71 appears', T(r'$73=2+71$', size=44))],
    })
    _gaps(M, V, 3, 30)
    _pen_or_click_slide(M, V, 6, {
        'Write "48 = 2⁴ · 3, 60 = 2² · 3 · 5 → GCD = 12, LCM = 240"': [A('48 and 60: GCD = 12, LCM = 240 appears',
            T(r'$48=2^4\cdot3,\ \ 60=2^2\cdot3\cdot5 \;\to\;$ GCD $=12$, LCM $=240$', size=40))],
    })
    _gaps(M, V, 6, 30)
    _pen_or_click_slide(M, V, 8, {
        'Write "20k a square: 20 = 2² · 5 → k = 5 → 100 = 10²"': [A('20k a square → k = 5 appears',
            T(r'$20k$ a square: $\ 20=2^2\cdot5 \;\to\; k=5 \;\to\; 100=10^2$', size=40))],
    })
    _gaps(M, V, 8, 30)


_apply_before_pen_or_click = apply


def apply(M):
    _apply_before_pen_or_click(M)
    pen_or_click(M)   # 2026-10-07 pen or click: runs last


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
    _mn_load().method_names(M, 14)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 Hebrew points restored. The 2026-10-05 cut took the "Factor Tools" lesson down to a short intro; the
# question videos only ANSWER the GCD / LCM questions. Points of the teacher's Hebrew lesson "המחלק הגדול ביותר" that
# were lost come back as a few spoken lines (helpers in _hebrew_back.py; a video recorded before its CUTOFF is left as
# recorded and gets the point in the question's written solution instead). See t14_CHANGES.md.
# =====================================================================================================================
import importlib.util as _ilu_hb, os as _os_hb
_s_hb = _ilu_hb.spec_from_file_location('_hebrew_back', _os_hb.path.join(_os_hb.path.dirname(_os_hb.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu_hb.module_from_spec(_s_hb); _s_hb.loader.exec_module(HB)


def hebrew_points_back(M):
    # lesson "Factor Tools": the exam remark - these questions feel hard, but they are simple
    if not HB.add_lines(M, 'prime-tools', 'Factor Tools', 'The greatest common divisor, the greatest guaranteed divisor', [
            "Many students find these 'greatest divisor' questions hard. You'll see — they're a lot simpler than they look."]):
        pass   # lesson only; no question to carry it
    # Q (q-389): the GCD is just taking out a common factor
    new = ["Read the word divisor as factor: the greatest common factor.",
           "And in practice, that's just taking out a common factor. Picture x plus y — what can you take out of both, in front of brackets? That's the GCD. And that you already know how to do."]
    if not HB.add_lines(M, 'solve-q-389', 'Lower power', 'The GCD is the biggest number that divides both', new):
        HB.add_expl(M, 'q-389', 'Why it works: the GCD is just the common factor you would take out of $x+y$ in front of brackets.')
    # Q (q-390): WHY you can't just multiply - numbers that share nothing vs a number hidden inside the other
    new = ["Why not just multiply? Divisible by three and by seven — then surely by twenty-one. They share nothing.",
           "But divisible by three and by nine? Not necessarily by twenty-seven — nine itself works. The three is already inside the nine."]
    if not HB.add_lines(M, 'solve-q-390', 'Higher power', 'Multiply them?', new, where='before'):
        HB.add_expl(M, 'q-390', 'Why not multiply? Divisible by $3$ and by $7$ → surely by $21$ (they share nothing). Divisible by $3$ and by $9$ → not necessarily by $27$: $9$ itself works, the $3$ is inside the $9$. A shared prime counts once.')


_apply_before_hebrew_points_back = apply


def apply(M):
    _apply_before_hebrew_points_back(M)
    hebrew_points_back(M)   # 2026-10-08 Hebrew points restored: runs LAST


# =====================================================================================================================
# 2026-10-08 clearer scripts. Teacher (recording topic 13): "Make the script of the slides of what I'm doing now and the
# next topic a bit more informative. Sometimes I feel stuck and reading what you wrote isn't enough to understand."
# Spoken lines only, in the UNRECORDED videos (any take before _clearer.CUTOFF -> untouched): say what we do and why,
# what a result means, the rule by name, why a choice is out, the missing middle step, and the terms defined once
# (prime = exactly two divisors, prime factorization, LCM). Same methods, numbers, board items and pen/click split.
# =====================================================================================================================
import importlib.util as _ilu_cl, os as _os_cl
_s_cl = _ilu_cl.spec_from_file_location('_clearer', _os_cl.path.join(_os_cl.path.dirname(_os_cl.path.abspath(__file__)), '_clearer.py'))
CL = _ilu_cl.module_from_spec(_s_cl); _s_cl.loader.exec_module(CL)


def clearer_scripts(M):
    E = CL.edit
    # ---- the lesson
    v = 'primes'
    E(M, v, 'What a prime is', [
        ('after', "Sounds weird? It's what you remember from school",
         ["In other words: a prime has exactly two divisors — one and itself."]),
    ])
    E(M, v, 'Is it prime?', [
        ('replace', 'Why? If n breaks into two factors',
         ["Why? If n breaks into two factors, they can't both be bigger than its square root — then their product would be bigger than n.",
          "So one factor is at most the root — and we'd find it."]),
    ])
    E(M, v, 'Break it down', [
        ('after', 'Start with a divisor you recognise',
         ["It's even — so two is an easy start."]),
        ('after', 'So one hundred fifty is two, times three, times five squared',
         ["Writing a number as a product of primes like this is called its prime factorization."]),
    ])
    E(M, v, 'Is it a divisor?', [
        ('after', 'Now: is a number a divisor? Check its ingredients',
         ["A number divides one fifty only if each of its primes is in one fifty — at least as many times."]),
    ])
    # ---- q-387: x prime, x⁶ two digits
    v = 'solve-q-387'
    E(M, v, 'Trial and error', [
        ('replace', 'Start with the smallest prime: two', "x is a prime — so we only try primes. Start with the smallest: two."),
        ('after', 'So x must be two', ["But they ask for nine x, not x. So multiply by nine."]),
    ])
    # ---- q-r26-t14-01: which is prime
    v = 'solve-q-r26-t14-01'
    E(M, v, 'Test up to the root', [
        ('after', 'Test each one: divide by the primes up to its square root',
         ["If one of those primes divides it, the number breaks — a fake, not prime."]),
        ('replace', 'No prime divides it. A hundred thirteen is prime',
         "No prime up to the root divides it — so nothing breaks it. A hundred thirteen is prime. Choice three."),
    ])
    # ---- q-388: x = 3 · 5² · 10²
    v = 'solve-q-388'
    E(M, v, 'The missing prime', [
        ('replace', 'Ten squared is two squared times five squared. So x has',
         ["Ten squared is two squared times five squared.",
          "Together with the five squared already there — x has two twos, a three, and four fives."]),
        ('replace', 'Twenty-two: two times eleven',
         "Twenty-two: two times eleven. The two is there — but there's no eleven anywhere in x. A missing prime — so it can't divide x. Choice two."),
    ])
    # ---- q-386: primes around 40
    v = 'solve-q-386'
    E(M, v, 'Number line', [
        ('replace', 'Between x and forty: exactly two primes. So thirty-one',
         ["Between x and forty: exactly two primes. Counting down from forty: thirty-seven, thirty-one.",
          "So those two are in — twenty-nine must stay out."]),
        ('replace', 'And twenty-nine is prime. Not allowed',
         "But x must not be prime — the question says so. Twenty-nine is prime. So x is thirty."),
        ('before', 'So y is forty-four, forty-five or forty-six',
         ["So y must come after forty-three — and can't go past forty-seven."]),
        ('replace', 'We want the SMALLEST product',
         "We want the SMALLEST product. x has to be thirty. Take the smallest y: forty-four."),
    ])
    # ---- Factor tools lesson
    v = 'prime-tools'
    E(M, v, 'Break & build', [
        ('after', 'plug in the smallest primes: two, three, five, seven',
         ["Why the smallest? Any primes in the right order fit — and small ones are the easiest to calculate with."]),
    ])
    E(M, v, 'Counting divisors', [
        ('before', 'A divisor chooses how many threes',
         ["Why does this work? A divisor of n is built only from n's primes — threes and fives — and never more of each than n has."]),
        ('before', 'Four times three: twelve divisors',
         ["Any choice of threes goes with any choice of fives — so we multiply the options."]),
    ])
    # ---- q-389: GCD
    v = 'solve-q-389'
    E(M, v, 'Lower power', [
        ('after', 'Each shared prime, at its LOWER power',
         ["Why the lower? y has only one p — so a number with two p's can't divide y."]),
        ('replace', 'r: only in y. Not shared. Out.', "r: only in y. x has no r — so r can't divide x. Out."),
        ('after', "That's the LCM, not the GCD",
         ["The LCM — the least common multiple — is the next question."]),
    ])
    # ---- q-390: LCM
    v = 'solve-q-390'
    E(M, v, 'Factor Questions', [
        ('after', 'Its official name: the least common multiple',
         ["It's the smallest number that both ten and twenty-five divide."]),
    ])
    E(M, v, 'Higher power', [
        ('after', 'Take every prime at its HIGHER power',
         ["The number must contain all of ten AND all of twenty-five. Twenty-five alone needs two fives."]),
        ('replace', 'Check: fifty itself is divisible by ten and by twenty-five',
         ["Check: fifty itself is divisible by ten and by twenty-five. So the number might be just fifty.",
          "And a hundred doesn't divide fifty. So we can't promise more."]),
        ('replace', 'The GCD here is five — five times fifty',
         "A bonus fact: the GCD times the LCM equals the two numbers multiplied. The GCD here is five — the one five they share. Five times fifty is two hundred fifty."),
    ])
    # ---- q-398: lock code digits 1, 3, 5
    v = 'solve-q-398'
    E(M, v, 'Which prime is missing?', [
        ('replace', 'Thirty: two times three times five',
         ["Thirty: two times three times five. Two isn't one of the digits.",
          "And thirty always breaks into the same primes — two, three, five. No digit brings a two. It can't be the product. Choice two."]),
    ])
    # ---- q-399: x · y = 100
    v = 'solve-q-399'
    E(M, v, 'Break it every way', [
        ('after', 'A is the difference between them',
         ["The bars make it positive: the bigger one minus the smaller one."]),
        ('replace', 'So take a hundred and break it into every pair you can',
         "So take a hundred and break it into every pair you can. One isn't allowed — so no one times a hundred."),
    ])
    # ---- q-400: products of cards
    v = 'solve-q-400'
    E(M, v, 'Build every product', [
        ('after', 'Build every product', ["First every pair of cards, then all three together."]),
    ])
    # ---- q-401: m² prime
    v = 'solve-q-401'
    E(M, v, 'Method 1 · Understanding', [
        ('replace', 'So m can\'t be a whole number — a whole m',
         ["Suppose m were a whole number, like three. Then m squared is three times three — it breaks. Not prime.",
          "So m can't be a whole number — a whole m makes m squared equal m times m. That breaks."]),
        ('after', 'Zero and one? Their squares are zero and one',
         ["Prime, even, odd — those words describe whole numbers only. So choices one, three and four are out."]),
    ])
    # ---- q-402: exactly 3 divisors
    v = 'solve-q-402'
    E(M, v, 'Three divisors → prime squared', [
        ('replace', 'Most numbers have divisors in pairs',
         ["Divisors come in pairs that multiply to the number. Twelve: one and twelve, two and six, three and four.",
          "So most numbers have an even count. Three is odd."]),
        ('after', 'So k is a prime squared',
         ["Why? The middle one times itself is k. And anything that divides it divides k too — so it has only one and itself: a prime."]),
    ])
    # ---- More factor tools lesson
    v = 'r26-t14-more-tools'
    E(M, v, 'Perfect squares', [
        ('after', "That's a perfect square: six times six",
         ["Why even? Each six brings one two and one three. So every prime comes in pairs."]),
        ('replace', 'The three is missing one copy. So k is three.',
         ["Twelve is two squared times three. The two's exponent is even — fine. The three's is one — odd.",
          "So the three is missing one copy. k is three."]),
    ])
    # ---- q-r26-t14-03: 2^a · 3^b = 108
    v = 'solve-q-r26-t14-03'
    E(M, v, 'Break and match', [
        ('replace', 'A hundred eight is four times twenty-seven',
         "A hundred eight is four times twenty-seven. Four is two squared, twenty-seven is three cubed."),
        ('replace', 'Match prime by prime',
         ["Both sides are the same number, written in primes — so the exponents must match.",
          "The twos: a is two. The threes: b is three."]),
    ])
    # ---- q-391: p + q
    v = 'solve-q-391'
    E(M, v, 'The only even prime', [
        ('after', 'Forty-nine is seven times seven — not prime',
         ["And without a two, both primes are odd — their sum would be even, not fifty-one. So no pair works."]),
    ])
    # ---- q-392: a, b primes
    v = 'solve-q-392'
    E(M, v, 'Method 1 · Prime factorization', [
        ('replace', 'Seven. So a equals seven.',
         "Two is only in fourteen, three only in twenty-one, five only in five. Seven is in two of them. So a equals seven."),
    ])
    # ---- q-393: a(b + 4) = 48
    v = 'solve-q-393'
    E(M, v, 'Common factor, then factor pairs', [
        ('after', 'not necessarily primes. a is the smaller one',
         ["Why smaller? b is bigger than a — so b plus four is surely bigger than a."]),
        ('after', 'Cross out choice 4',
         ["a equals six? The bracket is eight, b is four — smaller than a. Not allowed. So no more options."]),
    ])
    # ---- q-396: smallest a·b/15
    v = 'solve-q-396'
    E(M, v, 'Build the smallest a and b', [
        ('after', 'When a is smallest and b is smallest',
         ["a and b are both on top of the fraction — the smaller they are, the smaller the result."]),
        ('after', "Six isn't bigger than ten", ["And b can't get smaller than ten."]),
        ('replace', 'Choice one.', "Eight. Choice one."),
    ])
    # ---- q-394: z = p^s · q^r
    v = 'solve-q-394'
    E(M, v, 'Method 1 · Understanding', [
        ('after', 'First look at the choices — what can we kill fast',
         ["The rule: a power of a prime divides z only if z has that prime at least as many times."]),
    ])
    # ---- q-397: exactly 3 divisors below 200
    v = 'solve-q-397'
    E(M, v, 'Method 1 · Understanding', [
        ('after', 'Three divisors? A prime squared',
         ["Why? A prime p, squared, has just one, p, and p squared — exactly three."]),
    ])


_apply_before_clearer_scripts = apply


def apply(M):
    _apply_before_clearer_scripts(M)
    clearer_scripts(M)   # 2026-10-08 clearer scripts: runs LAST
