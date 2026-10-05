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
