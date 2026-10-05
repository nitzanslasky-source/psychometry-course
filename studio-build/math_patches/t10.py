"""Topic 10 - Laws of Exponents & Roots (techniques). Course review 2026-09 fixes.
See t10_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q

TOPIC = 10
LESSON = 'powers-techniques'
TRAPS = 'r26-t10-power-traps'
QSIDEBAR = ['Question %d' % n for n in range(1, 9)]


def _solution(M, qid, intro, slides, after=None):
    """Guided-question solution video in the style of solve-q-248..252."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=n - 1, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Exponents & Roots Questions', QSIDEBAR, beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = 'Exponents & Roots Questions'
    v['hybrid']['num'] = 28
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _fix_draw(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def summary(M):
    """Pass 2: summary lesson right before the first practice section."""
    sb = ['Dividing roots', 'Same prime base', 'Adding roots', 'Power equations', 'Root equations',
          "Don't divide by x", 'Sums of powers', 'Common factor', 'Before you practice']
    slides = [
        dict(mode='title', title='Summary', script=[
            "Exponents and roots — a quick summary before you practice.",
            "All the techniques from this topic, one at a time.",
        ]),
        dict(title='Dividing roots', mode='concept', active=0, pre=[], script=[
            A('√108 / √3 = 6 appears', T('$\\frac{\\sqrt{108}}{\\sqrt3}=\\sqrt{36}=6$', size=56, gap=50)),
            "Dividing roots? Put them under one root, or split the top and cancel.",
            A('28 / √7 = 4√7 appears', T('$\\frac{28}{\\sqrt7}=4\\sqrt7$', size=56)),
            "A number over a root: ignore the root, then put it back.",
            D('Write "28 ÷ 7 = 4 → 4√7"'),
            "Twenty-eight divided by seven is four. Put the root back: four root seven.",
        ]),
        dict(title='Same prime base', mode='concept', active=1, pre=[], script=[
            A('4⁹ = 2¹⁸ = 8⁶ appears', T('$4^9=\\left(2^2\\right)^9=2^{18}=\\left(2^3\\right)^6=8^6$', size=50, gap=50)),
            "Different bases? Break every base down to the smallest prime. Two, not four, not eight.",
            A('5³ · 7⁻² = 5³ / 7² appears', T('$5^3\\cdot7^{-2}=\\frac{5^3}{7^2}$', size=54)),
            "A negative exponent means: flip. The factor goes to the bottom.",
            "Subtracting negative exponents? Minus minus is plus.",
        ]),
        dict(title='Adding roots', mode='concept', active=2, pre=[], script=[
            A('√44 + √99 = 5√11 appears', T('$\\sqrt{44}+\\sqrt{99}=2\\sqrt{11}+3\\sqrt{11}=5\\sqrt{11}$', size=50, gap=50)),
            "Method one: split each root so one part comes out whole.",
            A('√11(√4 + √9) appears', T('$\\sqrt{44}+\\sqrt{99}=\\sqrt{11}\\left(\\sqrt4+\\sqrt9\\right)=5\\sqrt{11}$', size=50)),
            "Method two: take out a common factor. No trial and error.",
            "Use whichever feels easier. You land in the same place.",
        ]),
        dict(title='Power equations', mode='concept', active=3, pre=[], script=[
            A('2^(3x+1) = 16 appears', T('$2^{3x+1}=16=2^4$', size=58, gap=50)),
            "The unknown is in the exponent? Make the bases equal, then make the exponents equal.",
            D('Write "3x + 1 = 4 → x = 1"'),
            "Three x plus one is four. x is one.",
            "Or put each choice into the exponent and see which one works.",
        ]),
        dict(title='Root equations', mode='concept', active=4, pre=[], script=[
            A('√(x + 20) = x appears', T('$\\sqrt{x+20}=x$', size=58, gap=50)),
            "A root is never negative. So the other side can't be negative either.",
            "Square both sides, solve, and check every answer in the ORIGINAL equation.",
            D('Write "x = 5: √25 = 5 ✓    x = −4: √16 = 4 ≠ −4 ✗"'),
            "Squaring can sneak in a fake solution. Minus four fails. Only five.",
            "Faster: try the choices. Fake solutions fail on their own.",
        ]),
        dict(title="Don't divide by x", mode='concept', active=5, pre=[], script=[
            A('x² = 7x appears', T('$x^2=7x$', size=58, gap=50)),
            "Can you divide by x? Only if the question says x isn't zero.",
            D('Write "x² − 7x = 0 → x(x − 7) = 0 → x = 0 or x = 7"'),
            "If it doesn't, move everything to one side and factor. Then you keep both answers: zero and seven.",
        ]),
        dict(title='Sums of powers', mode='concept', active=6, pre=[], script=[
            A('2ˣ + 2ˣ = 2ˣ⁺¹ appears', T('$2^x+2^x=2\\cdot2^x=2^{x+1}$', size=56, gap=50)),
            "There's no law for adding powers. Count the copies.",
            A('2ˣ + 2ˣ ≠ 4ˣ appears', T('Trap: $2^x+2^x\\ne4^x$', size=50)),
            "Two copies of two to the x is two times two to the x. Two to the x plus one. Not four to the x.",
            D('Write "x = 2: 4 + 4 = 8, but 4² = 16"'),
            "Not sure? Put in a number.",
        ]),
        dict(title='Common factor', mode='concept', active=7, pre=[], script=[
            A('5^(x+1) − 5ˣ = 4 · 5ˣ appears', T('$5^{x+1}-5^x=5^x\\left(5-1\\right)=4\\cdot5^x$', size=50, gap=50)),
            "Same base, different exponents? Take out the SMALLEST power.",
            A('aˣ · bˣ = (ab)ˣ appears', T('$a^x\\cdot b^x=(ab)^x\\qquad 3^x\\cdot5^x=15^x$', size=50)),
            "Different bases, same exponent? Multiply the bases.",
            "Same base? Add the exponents. Don't mix up the two laws.",
        ]),
        dict(title='Before you practice', mode='concept', active=8, pre=[], script=[
            "Before each question, ask yourself:",
            A('check 1 appears', T('Can I write every base as the same prime?', size=36, gap=24)),
            A('check 2 appears', T('Is it a sum of powers? Count the copies, or take out the smallest power.', size=36, gap=24)),
            A('check 3 appears', T('Did I check my answer in the original equation?', size=36, gap=24)),
            A('check 4 appears', T('Am I dividing by $x$? Is $x\\ne0$ given?', size=36, gap=24)),
            A('check 5 appears', T('Four choices? Try them.', size=36)),
            "The common traps: two to the x plus two to the x is not four to the x, and the fake solution of a root equation.",
            "You know all of this. Now practice.",
        ]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == 'power-theory'][-1]
    M.new_video('r26-t10-summary', TOPIC, 'Exponents & Roots — Summary', sb, slides, 'power-theory', after=last)


def apply(M):
    # =====================================================================================
    # 1. Main lesson video (powers-techniques)
    # =====================================================================================
    _fix_draw(M, LESSON, 2, '√(48 : 3)', '√(48 ÷ 3)')
    _fix_draw(M, LESSON, 3, '6 : 3 = 2', '6 ÷ 3 = 2')
    _fix_draw(M, LESSON, 3, '20 : 5 = 4', '20 ÷ 5 = 4')

    # slide 5: negative exponents - add the division example (minus minus is plus)
    M.set_slide(LESSON, 5, script=[
        "One more thing you'll need with these answers.",
        A('2⁻³ appears', T('$2^{-3}$', size=66, gap=50)),
        "A negative exponent means: flip the base.",
        D('Write "= (1/2)³ = 1/2³"'),
        "The reciprocal of two is one half. One half cubed — one over two cubed. The minus is gone.",
        A('3⁴ · 2⁻³ appears', T('$3^4\\cdot2^{-3}$', size=66, gap=50)),
        D('Write "= 3⁴ / 2³"'),
        "So a factor with a negative exponent really lives on the bottom of the fraction.",
        "Why does that matter? The same answer can show up in the choices written either way. Recognize both.",
        A('2⁻⁶ over 2⁻⁴ appears', T('$\\frac{2^{-6}}{2^{-4}}$', size=76)),
        "Dividing? Subtract the exponents, top minus bottom. Careful with the signs.",
        D('Write "= 2^(−6 − (−4)) = 2^(−6 + 4) = 2⁻²"'),
        "Minus six, minus minus four. Minus minus is plus: minus six plus four is minus two.",
        "Two to the minus two. That's one over four.",
    ])

    # slide 8: power equations - mention trying the choices
    M.set_slide(LESSON, 8, script=[
        "An exponential equation: the unknown sits up in the exponent.",
        "The method: make the bases equal — then make the exponents equal.",
        D('Write "27 = 3³" and "3^(2x−1) = 3³"'),
        "Twenty-seven is three cubed. Now both sides have base three.",
        D('Write "2x − 1 = 3 → x = 2"'),
        "Same base, so the exponents must be equal. Two x minus one equals three. x is two.",
        "One restriction: this works for a positive base that isn't one. One to any power is one — that tells you nothing.",
        "And remember: on the exam you have four choices. You can also put each choice into the exponent and see which one works.",
    ])

    # slide 9 (root equations): the original slide with sqrt(x+7) = x - 1 stays as it is (pass 2).
    # new slide after it: a complete example with a fake solution
    solved = dict(mode='question', active=7, title='Root equations: an example', pre=[T('$\\sqrt{x+2}=x$', size=66, gap=60)], script=[
        "Let's solve one all the way.",
        "First — a root is never negative. Here the other side is x. So x can't be negative.",
        D('Under it write "x ≥ 0"'),
        "Now square both sides. The square cancels the root: x plus two equals x squared. Move everything to one side.",
        D('Write "x + 2 = x²  →  x² − x − 2 = 0"'),
        D('Write "(x − 2)(x + 1) = 0  →  x = 2 or x = −1"'),
        "Two numbers that multiply to minus two and add to minus one: minus two and plus one. So x is two, or x is minus one.",
        "Now the important part. Squaring can sneak in fake solutions. Check each one in the ORIGINAL equation.",
        D('Write "x = 2: √4 = 2 ✓"'),
        "x equals two: root four is two. It works.",
        D('Write "x = −1: √1 = 1 ≠ −1 ✗"'),
        "x equals minus one: root one is one — not minus one. Fake. Throw it out. And we knew it: x can't be negative.",
        D('Write "x = 2 only"'),
        "Only one answer: x equals two. On the exam, the trap choice will be \"two or minus one\".",
    ])

    # slide 10: recap - last line mentions trying the choices; six questions now
    M.set_slide(LESSON, 10, active=9, script=[
        "Let's lock it in.",
        A("'Number over a root: ignore the root, then put it back' appears", T('Number over a root: ignore it, then put it back', size=42)),
        A("'Different bases → smallest prime base' appears", T('Different bases $\\to$ smallest prime base', size=42)),
        A("'Add roots: split into factors or take a common factor' appears", T('Add roots: split into factors, or take a common factor', size=42)),
        A("'Power equation: equal bases → equal exponents' appears", T('Power equation: equal bases $\\to$ equal exponents', size=42)),
        A("'Root equation: square, solve, check — or try the choices' appears", T('Root equation: square, solve, check — or try the choices', size=42)),
        D('Tick each line'),
        "Six questions next. Each one uses one of these techniques. Try it — then watch.",
    ])

    # new slides 10-11: the solved example, then method 2 for root equations - try the choices
    M.insert_slides(LESSON, 9, [solved, dict(mode='concept', active=8, title='Try the choices', script=[
        "Method two — often faster on the exam. You have four choices. Try them.",
        A('√(x + 2) = x appears', T('$\\sqrt{x+2}=x$', size=62, gap=50)),
        A('The four choices appear', T('(1) $-1$  (2) $1$  (3) $2$  (4) $-1$ or $2$', size=46)),
        "Minus one: root of one is one. Not minus one. Out.",
        D('Cross out choice 1'),
        "One: root three isn't one. Out.",
        D('Cross out choice 2'),
        "Two: root four is two. It works.",
        D('Circle choice 3'),
        "And choice four includes minus one — which already failed. Out.",
        D('Cross out choice 4'),
        "Trying the choices throws out the fake solutions for you.",
        "It works for power equations too: put each choice into the exponent.",
    ])])
    M.set_sidebar(LESSON, ['Dividing roots', 'Number over a root', 'Same prime base', 'Negative exponents',
                           'Adding roots: split', 'Adding roots: factor', 'Power equations', 'Root equations',
                           'Try the choices', 'Recap'])

    # =====================================================================================
    # 2. Existing solution videos
    # =====================================================================================
    for vid in ['solve-q-248', 'solve-q-249', 'solve-q-250', 'solve-q-251', 'solve-q-252']:
        M.set_sidebar(vid, QSIDEBAR)
    # Q2: delete the "answer sits in its own position" remark
    M.edit_lines('solve-q-249', 2, lambda ls: [l for l in ls if 'its own position' not in l.get('say', '')])
    _fix_draw(M, 'solve-q-249', 3, '√(27 : 3)', '√(27 ÷ 3)')
    # Q5: link to "factor - don't divide" when x != 0 is not given
    M.edit_lines('solve-q-252', 2, lambda ls: ls + [
        {'say': "One warning. We divided by x only because the question says x isn't zero."},
        {'draw': 'Write "no x ≠ 0?  x² = 5x → x² − 5x = 0 → x(x − 5) = 0 → x = 0 or x = 5"'},
        {'say': "If that's NOT given, don't divide — factor. Then you keep both answers: zero and five."},
    ])

    M.sections['power-theory']['title'] = 'Eight guided questions'

    # =====================================================================================
    # 3. Existing questions: text in TeX, no colons, stacked conditions
    # =====================================================================================
    S = M.set_q
    S('q-248', expl=[
        'Write every base as a prime: $9^6=(3^2)^6=3^{12}$, $8^{-2}=(2^3)^{-2}=2^{-6}$, $4^{-2}=(2^2)^{-2}=2^{-4}$.',
        'The fraction becomes $\\frac{3^{12}\\cdot2^{-6}}{3^8\\cdot2^{-4}}=3^{12-8}\\cdot2^{-6-(-4)}=3^4\\cdot2^{-2}$.'])
    S('q-249', expl=[
        'Simplify each root: $\\sqrt{27}=3\\sqrt3$, $\\sqrt{48}=4\\sqrt3$, $\\sqrt{12}=2\\sqrt3$.',
        'Numerator: $3\\sqrt3+3\\sqrt3=6\\sqrt3$. Denominator: $4\\sqrt3-2\\sqrt3=2\\sqrt3$.',
        '$\\frac{6\\sqrt3}{2\\sqrt3}=3$.'])
    S('q-250', expl=[
        'Write both sides with base 2: $4^{2x}=(2^2)^{2x}=2^{4x}$, and $\\frac18=2^{-3}$, so $\\left(\\frac18\\right)^{4-2x}=2^{-3(4-2x)}=2^{-12+6x}$.',
        'Equal bases, so the exponents are equal: $4x=-12+6x$. Therefore $2x=12$ and $x=6$.'])
    S('q-251', stem='Given: $\\sqrt{x-7}=3$. $x=?$', expl=[
        'Square both sides: $x-7=9$, so $x=16$.', 'Check: $\\sqrt{16-7}=\\sqrt9=3$ ✓.'])
    S('q-252', stem='Given:\n$\\begin{cases} x\\ne0 \\\\ x\\sqrt5=5\\sqrt x \\end{cases}$\n$x=?$', expl=[
        'Square both sides: $(x\\sqrt5)^2=(5\\sqrt x)^2$, so $5x^2=25x$.',
        'Divide by 5: $x^2=5x$. Since $x\\ne0$, divide by $x$: $x=5$.',
        'Check: $5\\sqrt5=5\\sqrt5$ ✓.',
        'If $x\\ne0$ were not given, factor instead of dividing: $x(x-5)=0$, so $x=0$ or $x=5$.'])
    S('q-253', expl=['$15^2=(3\\cdot5)^2=3^2\\cdot5^2$.',
                     '$\\frac{3^5}{3^2\\cdot5^2}=\\frac{3^3}{5^2}=\\frac{27}{25}$.'])
    S('q-254', expl=['$9^3=(3^2)^3=3^6$, so $3^2\\cdot3^6=3^{2+6}=3^8$.'])
    S('q-255', expl=['All bases are powers of 2: $16^3=2^{12}$, $8^2=2^6$, $4^4=2^8$.',
                     'Numerator: $2^{12}\\cdot2^6=2^{18}$. Denominator: $2^8\\cdot2^6=2^{14}$.',
                     '$\\frac{2^{18}}{2^{14}}=2^{18-14}=2^4$.'])
    S('q-256', stem='Given: $7^2=7^{x+6}$. $x=?$', expl=['Equal bases, so the exponents are equal: $x+6=2$. Therefore $x=-4$.'])
    S('q-257', stem='Given: $2^8=4^{x-1}$. $x=?$', expl=[
        '$4=2^2$, so $4^{x-1}=2^{2(x-1)}=2^{2x-2}$.', 'Equal exponents: $2x-2=8$, so $2x=10$ and $x=5$.'])
    S('q-258', stem='Given: $8^5=4^4\\cdot2^x$. $x=?$', expl=[
        'Base 2 everywhere: $8^5=2^{15}$ and $4^4=2^8$.', '$2^{15}=2^8\\cdot2^x=2^{8+x}$, so $8+x=15$ and $x=7$.'])
    S('q-259', stem='Given: $\\left(\\frac15\\right)^3=5^{x-7}$. $x=?$', expl=[
        '$\\frac15=5^{-1}$, so $\\left(\\frac15\\right)^3=5^{-3}$.', 'Equal exponents: $x-7=-3$, so $x=4$.'])
    S('q-260', expl=['Ignore the root: $10\\div5=2$. Put the root back on the answer: $2\\sqrt5$.',
                     'Why it works: $10=2\\cdot\\sqrt5\\cdot\\sqrt5$, so $\\frac{2\\cdot\\sqrt5\\cdot\\sqrt5}{\\sqrt5}=2\\sqrt5$.'])
    S('q-261', expl=['Split the denominator: $\\sqrt{15}=\\sqrt3\\cdot\\sqrt5$.',
                     'Cancel $\\sqrt3$: $\\frac{5\\sqrt3}{\\sqrt3\\cdot\\sqrt5}=\\frac5{\\sqrt5}$.',
                     'Number over a root: $5\\div5=1$, then put the root back: $\\sqrt5$.'])
    S('q-262', expl=['Pull out the largest square: $18=9\\cdot2$, so $\\sqrt{18}=\\sqrt9\\cdot\\sqrt2=3\\sqrt2$.'])
    S('q-264', expl=['$\\sqrt{27}=\\sqrt9\\cdot\\sqrt3=3\\sqrt3$.', '$\\sqrt3+3\\sqrt3=4\\sqrt3$.'])
    S('q-265', expl=['$\\sqrt{80}=\\sqrt{16}\\cdot\\sqrt5=4\\sqrt5$ and $\\sqrt{20}=\\sqrt4\\cdot\\sqrt5=2\\sqrt5$.',
                     '$4\\sqrt5-2\\sqrt5=2\\sqrt5$.'])
    S('q-266', expl=['Square both sides: $2x+9=25$, so $2x=16$ and $x=8$.', 'Check: $\\sqrt{2\\cdot8+9}=\\sqrt{25}=5$ ✓.'])
    S('q-267', expl=['Square both sides: $4x+6=70$, so $4x=64$ and $x=16$.'])

    # extra set 2 (kept): NITE-style stems, TeX choices, solutions with numbers
    S('alg-extra-unit-t10-2-1', stem='$\\frac{3^7}{3^4}=?$', choices=['$3$', '$9$', '$81$', '$27$'],
      expl=['Same base: subtract the exponents. $\\frac{3^7}{3^4}=3^{7-4}=3^3=27$.'])
    S('alg-extra-unit-t10-2-2', stem='$64^{\\frac23}=?$', choices=['$8$', '$48$', '$16$', '$4$'],
      expl=['$64^{\\frac23}=\\left(\\sqrt[3]{64}\\right)^2=4^2=16$.'])
    S('alg-extra-unit-t10-2-3', stem='Given: $3^{x+1}=3^5$. $x=?$', choices=['$3$', '$5$', '$12$', '$4$'],
      expl=['Equal bases, so the exponents are equal: $x+1=5$. Therefore $x=4$.'])
    S('alg-extra-unit-t10-2-4', stem='$3^{-3}+3^{-2}=?$',
      expl=['$3^{-3}=\\frac1{27}$ and $3^{-2}=\\frac19=\\frac3{27}$.', '$\\frac1{27}+\\frac3{27}=\\frac4{27}$.'])
    S('alg-extra-unit-t10-2-5', stem='Given: $x\\ne0$. $\\frac{(3x)^3}{9x^2}=?$',
      expl=['$(3x)^3=27x^3$.', '$\\frac{27x^3}{9x^2}=\\frac{27}{9}\\cdot x^{3-2}=3x$.'])
    # choices: the original ones (restored in pass 2)
    S('alg-extra-unit-t10-2-6', stem='Which is greater: $2^{12}$ or $4^5$?',
      choices=['They are equal', 'It cannot be determined from the information given.', 'The first power', 'The second power'],
      correct=3, expl=['Same base: $4^5=(2^2)^5=2^{10}$.', '$2^{12}>2^{10}$, therefore the first power, $2^{12}$, is greater.'])
    S('alg-extra-unit-t10-2-7', stem='$\\sqrt{72}+\\sqrt{18}=?$',
      expl=['$\\sqrt{72}=\\sqrt{36}\\cdot\\sqrt2=6\\sqrt2$ and $\\sqrt{18}=\\sqrt9\\cdot\\sqrt2=3\\sqrt2$.',
            '$6\\sqrt2+3\\sqrt2=9\\sqrt2$.'])

    S('q-268', stem='Given: $x>0$. $x^{x+3}\\cdot x^{-x-2}=?$', choices=['$\\frac1x$', '$x$', '$0$', '$1$'], expl=[
        'Same base: add the exponents. $(x+3)+(-x-2)=1$, so the product is $x^1=x$.',
        'Faster: choose an easy value, $x=2$: $2^5\\cdot2^{-4}=2^1=2$. Only choice (2) gives $2$ ($\\frac1x=\\frac12$, and the others are $0$ and $1$).'])
    S('q-269', stem='Given: $\\sqrt{x^2}=5$. Which of the following could be the value of $x$?', expl=[
        '$\\sqrt{x^2}=|x|$, so $|x|=5$: $x=5$ or $x=-5$.', 'Only $-5$ is among the choices.'])
    S('q-270', stem='Given: $a>0$. $\\frac{a^{a+2}}{a^2}=?$', expl=[
        'Same base: subtract the exponents. $\\frac{a^{a+2}}{a^2}=a^{a+2-2}=a^a$.',
        'With easy values: $a=2$ gives $\\frac{2^4}{2^2}=4$, but two choices give $4$ ($a^a$ and $a+2$). Try another number: $a=3$ gives $\\frac{3^5}{3^2}=27$, and only $a^a=27$ fits.'])
    S('q-271', expl=['Write every base as a power of 2: $16^x=2^{4x}$, $4^x=2^{2x}$.',
                     'Add the exponents: $4x+2x+x=7x$, so the product is $2^{7x}$.'])
    S('q-272', expl=['Base 3 everywhere: $9^3=3^6$ and $81=3^4$.',
                     '$\\frac{3^6\\cdot3^4}{3^4}=3^6$.'])
    S('q-273', expl=['$36=6^2$, so $36^4=(6^2)^4=6^8$.',
                     'The others: $216^2=(6^3)^2=6^6$, $(6^2)^8=6^{16}$, and $72^2=(2\\cdot36)^2=4\\cdot6^4$. None of them is $6^8$.'])
    S('q-274', expl=['$64=2^6$, so $n+1=6$ and $n=5$.'])
    S('q-275', expl=['Power of a power: multiply the exponents. $(-\\sqrt3)\\cdot(-\\sqrt3)=(\\sqrt3)^2=3$.',
                     'So the expression is $5^3=125$.'])
    S('q-276', stem='$7^x\\cdot7^{-x}=?$', expl=['Add the exponents: $x+(-x)=0$, so the product is $7^0=1$.'])
    S('q-278', stem='Given: $a>0$ and $c>0$. $\\frac{5a^8c^6}{a^2c^3}=?$', expl=[
        'Handle each base on its own and subtract the exponents: $a^{8-2}=a^6$ and $c^{6-3}=c^3$.',
        'The 5 does not change: $5a^6c^3$.'])
    S('q-279', stem='$(3^4)^3\\cdot3^{-14}=?$', expl=['$(3^4)^3=3^{12}$.',
                     '$3^{12}\\cdot3^{-14}=3^{-2}=\\frac1{3^2}=\\frac19$.'])
    S('q-280', stem='Given: $x>0$. $x^{\\frac34}\\cdot x^{\\frac43}=?$', choices=['$1$', '$x$', '$x^{\\frac{12}{25}}$', '$x^{\\frac{25}{12}}$'],
      expl=['Same base: add the exponents. $\\frac34+\\frac43=\\frac9{12}+\\frac{16}{12}=\\frac{25}{12}$.',
            'So the product is $x^{\\frac{25}{12}}$.'])
    S('q-281', expl=['Same exponent, so multiply the bases: $3^x\\cdot4^x\\cdot5^x=(3\\cdot4\\cdot5)^x=60^x$.',
                     '$\\sqrt[3]{60}=60^{\\frac13}$. Equal bases, so $x=\\frac13$.'])
    S('q-282', expl=['$3^x\\cdot3^y\\cdot3^z=3^{x+y+z}=3^5=243$.',
                     'We do not need $x$, $y$ and $z$ one by one — only their sum, and it is given.'])
    S('q-284', stem='The numbers $a$ and $b$ are such that $x^a\\cdot x^b=x^{ab}$ for every $x>1$. Which of the following is necessarily true?',
      expl=['Same base: $x^a\\cdot x^b=x^{a+b}$ always.',
            'This equals $x^{ab}$ for every $x>1$, so the exponents are equal: $a+b=ab$.',
            'Choices (1) and (3) are not necessarily true. For example, $a=3$ and $b=\\frac32$: $a+b=ab=4.5$, but $a+b\\ne0$ and $3^{1.5}\\approx5.2\\ne4.5$.'])
    S('q-285', expl=['$\\sqrt[4]{5^6}=5^{\\frac64}=5^{\\frac32}=5^1\\cdot5^{\\frac12}=5\\sqrt5$.'])
    S('q-286', stem='Given:\n$\\begin{cases} x>0 \\\\ \\sqrt{48x}=\\sqrt3\\cdot x \\end{cases}$\n$x=?$', expl=[
        'Square both sides: $48x=3x^2$.',
        'Since $x>0$, divide by $3x$: $16=x$.',
        'Check: $\\sqrt{48\\cdot16}=\\sqrt{256\\cdot3}=16\\sqrt3$ and $\\sqrt3\\cdot16=16\\sqrt3$ ✓.'])
    S('q-287', stem='Dana says: $7>\\sqrt5+\\sqrt{20}$.\nYoav says: $4\\sqrt3>5\\sqrt2$.\nWhich of the following is correct?',
      choices=['Only Dana is right.', 'Only Yoav is right.', 'Both are wrong.', 'Both are right.'], expl=[
        'Dana: $\\sqrt{20}=2\\sqrt5$, so $\\sqrt5+\\sqrt{20}=3\\sqrt5$. Square both: $(3\\sqrt5)^2=45$ and $7^2=49$. Since $45<49$, Dana is right.',
        'Yoav: square both: $(4\\sqrt3)^2=48$ and $(5\\sqrt2)^2=50$. Since $48<50$, $4\\sqrt3<5\\sqrt2$ and Yoav is wrong.',
        'Only Dana is right.'])

    # pass 2: original questions restored (they were removed as near-duplicates) - text clean-up only
    S('q-263', stem='$\\sqrt{63}=?$', expl=['$63=9\\cdot7$, therefore $\\sqrt{63}=\\sqrt9\\cdot\\sqrt7=3\\sqrt7$.'])
    S('q-283', stem='$\\sqrt{98}=?$', expl=['$98=49\\cdot2$, therefore $\\sqrt{98}=\\sqrt{49}\\cdot\\sqrt2=7\\sqrt2$.'])
    S('q-277', stem='Given: $x=y=8$. $x^{y-x}\\cdot y^{x-y}=?$', expl=[
        'Since $x=y=8$, both exponents are zero: $y-x=8-8=0$ and $x-y=8-8=0$.',
        'Therefore the product is $8^0\\cdot8^0=1\\cdot1=1$.'])
    S('alg-extra-unit-t10-3-1', stem='$\\frac{4^8}{4^5}=?$', choices=['$64$', '$4$', '$16$', '$256$'],
      expl=['Same base: subtract the exponents. $\\frac{4^8}{4^5}=4^{8-5}=4^3=64$.'])
    S('alg-extra-unit-t10-3-2', stem='$125^{\\frac23}=?$', choices=['$75$', '$25$', '$5$', '$10$'],
      expl=['$125^{\\frac23}=\\left(\\sqrt[3]{125}\\right)^2=5^2=25$.'])
    S('alg-extra-unit-t10-3-3', stem='Given: $3^{x+1}=3^6$. $x=?$', choices=['$15$', '$5$', '$4$', '$6$'],
      expl=['Equal bases, so the exponents are equal: $x+1=6$. Therefore $x=5$.'])
    S('alg-extra-unit-t10-3-4', stem='$4^{-3}+4^{-2}=?$',
      expl=['$4^{-3}=\\frac1{64}$ and $4^{-2}=\\frac1{16}=\\frac4{64}$.', '$\\frac1{64}+\\frac4{64}=\\frac5{64}$.'])
    S('alg-extra-unit-t10-3-5', stem='Given: $x\\ne0$. $\\frac{(4x)^3}{16x^2}=?$',
      expl=['$(4x)^3=64x^3$.', '$\\frac{64x^3}{16x^2}=\\frac{64}{16}\\cdot x^{3-2}=4x$.'])
    S('alg-extra-unit-t10-3-6', stem='Which is greater: $2^{14}$ or $4^6$?',
      expl=['Same base: $4^6=(2^2)^6=2^{12}$.', '$2^{14}>2^{12}$, therefore the first power, $2^{14}$, is greater.'])
    S('alg-extra-unit-t10-3-7', stem='$\\sqrt{98}+\\sqrt{32}=?$',
      expl=['$\\sqrt{98}=\\sqrt{49}\\cdot\\sqrt2=7\\sqrt2$ and $\\sqrt{32}=\\sqrt{16}\\cdot\\sqrt2=4\\sqrt2$.',
            '$7\\sqrt2+4\\sqrt2=11\\sqrt2$.'])

    for qid in ['q-251', 'q-252']:              # stems changed: keep video title and slide notes in sync
        v = M.video('solve-' + qid); q = M.q(qid)
        v['title'] = v['navLabel'] = q['stem']
        for b in v['beats']:
            if b.get('canvas', '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])

    # =====================================================================================
    # 5. Guided question 6 (root equation with a fake solution), right after Q5
    # =====================================================================================
    g1 = 'q-r26-t10-01'
    M.new_q(g1, TOPIC, 'Given: $\\sqrt{2x+3}=x$. $x=?$', ['$-1$', '$1$', '$3$', '$-1$ or $3$'], 3, [
        'The root is never negative, so $x\\ge0$.',
        'Square both sides: $2x+3=x^2$, so $x^2-2x-3=0$ and $(x-3)(x+1)=0$: $x=3$ or $x=-1$.',
        'Check in the original: $x=3$: $\\sqrt9=3$ ✓. $x=-1$: $\\sqrt1=1\\ne-1$ ✗ (fake solution).',
        'Only $x=3$. Faster: try the choices — $-1$ fails, $1$ fails ($\\sqrt5\\ne1$), $3$ works.'])
    M.place_q(g1, 'power-theory', after='solve-q-252')
    _solution(M, g1, ["Question six.", "A root equation — and a trap in the choices."], [
        ('Method 1 · Square and check', [
            "First: a root is never negative. So x can't be negative.",
            D('Write "x ≥ 0"'),
            "Now square both sides.",
            D('Write "2x + 3 = x²  →  x² − 2x − 3 = 0"'),
            "Two x plus three equals x squared. Everything to one side: x squared minus two x minus three equals zero.",
            D('Write "(x − 3)(x + 1) = 0  →  x = 3 or x = −1"'),
            "Two numbers that multiply to minus three and add to minus two: minus three and plus one. So x is three, or minus one.",
            D('Write "x = 3: √9 = 3 ✓"'),
            "Check three: two times three plus three is nine. Root nine is three. It works.",
            D('Write "x = −1: √1 = 1 ≠ −1 ✗"'),
            "Check minus one: root one is one — not minus one. Fake. And it's negative, so we knew.",
            D('Circle choice 3'),
            "Only three. Choice three. Choice four is the trap.",
        ]),
        ('Method 2 · Try the choices', [
            "Faster: try the choices.",
            D('Next to choice 1 write "√1 = 1 ≠ −1" and cross out choices 1 and 4'),
            "Minus one: root one is one. Not minus one. Out — and that also kills choice four.",
            D('Next to choice 2 write "√5 ≠ 1" and cross it out'),
            "One: root five isn't one. Out.",
            D('Next to choice 3 write "√9 = 3 ✓" and circle it'),
            "Three: root nine is three. Choice three.",
        ]),
    ])

    # =====================================================================================
    # 6. New lesson video: sums of powers, common factor, same exponent
    # =====================================================================================
    sb = ['Sums of equal powers', 'Common factor', 'Same exponent', 'Recap']
    M.new_video(TRAPS, TOPIC, 'Exponent Traps — Sums of Powers', sb, [
        dict(mode='title', title='Exponent Traps — Sums of Powers', script=[
            "Now the exponent traps the exam loves.",
            "Adding powers, taking out a common factor, and powers with the same exponent.",
        ]),
        dict(mode='concept', active=0, title='Sums of equal powers', script=[
            "The number one trap: adding powers.",
            "There's no law for adding powers. But there IS a trick.",
            A('2¹⁰ + 2¹⁰ appears', T('$2^{10}+2^{10}$', size=62, gap=50)),
            "Two to the tenth plus two to the tenth. Like x plus x: two times x.",
            D('Write "= 2 · 2¹⁰ = 2¹ · 2¹⁰ = 2¹¹"'),
            "Two times two to the tenth. Two is two to the first — add the exponents: two to the eleventh.",
            "Not two to the twentieth. Not four to the tenth. Two to the eleventh.",
            A('3ˣ + 3ˣ + 3ˣ appears', T('$3^x+3^x+3^x$', size=62, gap=50)),
            D('Write "= 3 · 3ˣ = 3ˣ⁺¹"'),
            "Three copies of three to the x: three times three to the x. That's three to the x plus one.",
            "So: count the copies. If you can write the count as a power of the same base, add the exponents.",
            A('2ˣ + 2ˣ ≠ 4ˣ appears', T('Trap: $2^x+2^x\\ne4^x$', size=50)),
            "And the classic wrong answer: two to the x plus two to the x is NOT four to the x.",
            D('Write "2ˣ + 2ˣ = 2 · 2ˣ = 2ˣ⁺¹"'),
            "It's two times two to the x: two to the x plus one.",
            D('Write "x = 3: 8 + 8 = 16, but 4³ = 64"'),
            "Not sure? Put in a number. x equals three: eight plus eight is sixteen. Four cubed is sixty-four. Not equal.",
        ]),
        dict(mode='concept', active=1, title='Common factor', script=[
            "Same base, but different exponents? Same trick as with roots: take out a common factor.",
            "Take out the SMALLEST power.",
            A('2ˣ⁺² − 2ˣ appears', T('$2^{x+2}-2^x$', size=62, gap=50)),
            "Two to the x plus two is two to the x times two squared.",
            D('Write "= 2ˣ · 2² − 2ˣ = 2ˣ(4 − 1) = 3 · 2ˣ"'),
            "Take out two to the x. Inside: four minus one. Three times two to the x.",
            A('2ˣ⁺³ + 2ˣ appears', T('$2^{x+3}+2^x$', size=62)),
            D('Write "= 2ˣ(2³ + 1) = 2ˣ(8 + 1) = 9 · 2ˣ"'),
            "Same move. Two cubed is eight, plus one: nine times two to the x.",
            D('Write "x = 1: 16 + 2 = 18 and 9 · 2 = 18 ✓"'),
            "Check with x equals one: sixteen plus two is eighteen. Nine times two is eighteen. It works.",
        ]),
        dict(mode='concept', active=2, title='Same exponent', script=[
            "Different bases, but the SAME exponent? Then you can multiply the bases.",
            A('aˣ · bˣ = (ab)ˣ appears', T('$a^x\\cdot b^x=(ab)^x$', size=62, gap=50)),
            "a to the x times b to the x is a times b, to the x.",
            A('2ˣ · 5ˣ = 10ˣ appears', T('$2^x\\cdot5^x=10^x$', size=62, gap=50)),
            "Two to the x times five to the x: ten to the x.",
            A('6ˣ over 3ˣ = 2ˣ appears', T('$\\frac{6^x}{3^x}=2^x$', size=62)),
            "Division works too: six over three is two. Two to the x.",
            "Careful: this works only when the EXPONENTS are the same. Two cubed times two to the fifth is the other law — same base, add the exponents.",
        ]),
        dict(mode='concept', active=3, title='Recap', script=[
            "Let's lock it in.",
            A("'Equal powers: count the copies' appears", T('Equal powers: count the copies — $2^x+2^x=2^{x+1}$', size=38)),
            A("'Different exponents: take out the smallest power' appears", T('Different exponents: take out the smallest power', size=38)),
            A("'Same exponent: multiply the bases' appears", T('Same exponent: $a^x\\cdot b^x=(ab)^x$', size=38)),
            D('Tick each line'),
            "Two questions next. Try each one first — then watch.",
        ]),
    ], 'power-theory', after='solve-' + g1)

    # =====================================================================================
    # 7. Guided questions 7-8
    # =====================================================================================
    g2, g3 = ['q-r26-t10-%02d' % k for k in (2, 3)]
    M.new_q(g2, TOPIC, '$2^{10}+2^{10}+2^{10}+2^{10}=?$', ['$8^{10}$', '$2^{12}$', '$2^{40}$', '$8^{40}$'], 2, [
        'Four equal powers: $2^{10}+2^{10}+2^{10}+2^{10}=4\\cdot2^{10}$.',
        '$4=2^2$, so $4\\cdot2^{10}=2^2\\cdot2^{10}=2^{12}$.',
        'Adding the exponents ($2^{40}$) or adding the bases ($8^{10}$) is the trap: there is no law for adding powers.'])
    M.place_q(g2, 'power-theory', after=TRAPS)
    _solution(M, g2, ["Question seven.", "Four powers added together. Don't fall for the trap."], [
        ('Count the copies', [
            "Four copies of the same thing: two to the tenth.",
            D('Write "= 4 · 2¹⁰"'),
            "Like x plus x plus x plus x: four x. So four times two to the tenth.",
            D('Write "4 = 2²  →  2² · 2¹⁰ = 2¹²"'),
            "Four is two squared. Same base — add the exponents: two to the twelfth.",
            D('Circle choice 2'),
            "Choice two.",
            "The traps: adding the exponents gives two to the fortieth. Adding the bases gives eight to the tenth. Both wrong.",
        ]),
        ('Check it small', [
            "Not sure? Try the same thing with small numbers.",
            D('Write "2¹ + 2¹ + 2¹ + 2¹ = 8 = 2³"'),
            "Four copies of two to the first: two plus two plus two plus two is eight. Two cubed.",
            "The exponent went up by two — because four is two squared. Same as our answer.",
        ]),
    ])

    M.new_q(g3, TOPIC, 'Given: $3^{x+2}-3^x=72$. $x=?$', ['$1$', '$2$', '$3$', '$4$'], 2, [
        'Take out the smallest power: $3^{x+2}-3^x=3^x(3^2-1)=8\\cdot3^x$.',
        '$8\\cdot3^x=72$, so $3^x=9=3^2$ and $x=2$.',
        'Check: $3^4-3^2=81-9=72$ ✓.'])
    M.place_q(g3, 'power-theory', after='solve-' + g2)
    _solution(M, g3, ["Question eight.", "Two powers with the same base, but different exponents."], [
        ('Method 1 · Common factor', [
            "Take out the smallest power: three to the x.",
            D('Write "3ˣ⁺² = 3ˣ · 3² = 9 · 3ˣ"'),
            "Three to the x plus two is three to the x times nine.",
            D('Write "3ˣ(9 − 1) = 72  →  8 · 3ˣ = 72"'),
            "Take out three to the x: nine minus one is eight. Eight times three to the x is seventy-two.",
            D('Write "3ˣ = 9 = 3²  →  x = 2"'),
            "Divide by eight: three to the x is nine. Nine is three squared. x is two.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
        ('Method 2 · Try the choices', [
            "Or try the choices. Start in the middle, with two.",
            D('Write "x = 2: 3⁴ − 3² = 81 − 9 = 72 ✓"'),
            "Three to the fourth is eighty-one. Minus three squared, nine. Seventy-two. Found it.",
            "Tip: if the result is too big, try a smaller choice. Too small, try a bigger one.",
        ]),
    ])

    # =====================================================================================
    # 8. Memory card for the topic
    # =====================================================================================
    M.new_card('mem-r26-t10-techniques', TOPIC, 'power-theory', {
        'title': 'Exponent and root techniques',
        'intro': 'The methods of this topic, each with one example.',
        'tables': [{'title': 'Techniques', 'head': ['Situation', 'Method', 'Example'], 'rows': [
            ['Number over a root', 'ignore the root, then put it back', '$\\frac6{\\sqrt3}=2\\sqrt3$'],
            ['Different bases', 'write every base as the smallest prime', '$8^4=2^{12}=16^3$'],
            ['Negative exponent', 'flip the base', '$3^4\\cdot2^{-3}=\\frac{3^4}{2^3}$'],
            ['Adding roots', 'split, or take a common factor', '$\\sqrt8+\\sqrt{18}=5\\sqrt2$'],
            ['Equal powers added', 'count the copies', '$2^x+2^x=2\\cdot2^x=2^{x+1}$'],
            ['Same base, different exponents', 'take out the smallest power', '$2^{x+2}-2^x=3\\cdot2^x$'],
            ['Same exponent', 'multiply the bases', '$2^x\\cdot5^x=10^x$'],
            ['Power equation', 'equal bases, then equal exponents', '$3^{2x-1}=3^3\\Rightarrow x=2$'],
            ['Root equation', 'square, solve, check in the original', '$\\sqrt{x+2}=x\\Rightarrow x=2$ only'],
        ]}],
        'tips': [
            'Trap: $2^x+2^x\\ne4^x$. Check with $x=3$: $8+8=16$, but $4^3=64$.',
            'Mixed bases in a fraction? Pair the families: $\\frac{9^6\\cdot8^{-2}}{3^8\\cdot4^{-2}}=\\frac{9^6}{3^8}\\cdot\\left(\\frac84\\right)^{-2}$.',
            'Four choices? Try them. It is often faster, and it throws out fake solutions of root equations.',
            'If $x\\ne0$ is NOT given, factor — don\'t divide by $x$: $x^2=5x\\Rightarrow x(x-5)=0$.',
            'Expression choices? Choose an easy value ($x=2$ or $x=3$). If two choices match, try another number.',
        ]}, after='solve-' + g3)

    # =====================================================================================
    # 9. New practice questions (exam level)
    # =====================================================================================
    P = {}
    P['06'] = ('$3^x+3^x+3^x=?$', ['$9^x$', '$3^{3x}$', '$3^{x+1}$', '$9^{3x}$'], 3, [
        'Three equal powers: $3^x+3^x+3^x=3\\cdot3^x=3^1\\cdot3^x=3^{x+1}$.',
        'If you check with a number, avoid $x=1$ (then $9^x=9$ too). With $x=2$: $9+9+9=27=3^3$, while $9^2=81$.'])
    P['07'] = ('Given: $0.2^x=25$. $x=?$', ['$2$', '$-2$', '$\\frac12$', '$-\\frac12$'], 2, [
        '$0.2=\\frac15=5^{-1}$, so $0.2^x=5^{-x}$. Also $25=5^2$.',
        'Equal exponents: $-x=2$, so $x=-2$.', 'Check: $0.2^{-2}=5^2=25$ ✓.'])
    P['08'] = ('Given: $4^x\\cdot25^x=10^6$. $x=?$', ['$2$', '$3$', '$6$', '$12$'], 2, [
        'Same exponent, so multiply the bases: $4^x\\cdot25^x=100^x$.',
        '$100^x=(10^2)^x=10^{2x}$, so $2x=6$ and $x=3$.'])
    P['09'] = ('Given: $\\sqrt{x+12}=x$. $x=?$', ['$-3$', '$4$', '$-3$ or $4$', '$3$'], 2, [
        'Square both sides: $x+12=x^2$, so $x^2-x-12=0$ and $(x-4)(x+3)=0$: $x=4$ or $x=-3$.',
        'Check: $x=4$: $\\sqrt{16}=4$ ✓. $x=-3$: $\\sqrt9=3\\ne-3$ ✗ (fake solution).',
        'Only $x=4$. Trying the choices gives the same result: $3$ fails too ($\\sqrt{15}\\ne3$).'])
    P['10'] = ('Given: $x\\sqrt3=\\sqrt{3x}$. Which of the following gives all the possible values of $x$?',
               ['$1$ only', '$0$ only', '$0$ or $1$', '$3$ only'], 3, [
        'Square both sides: $3x^2=3x$, so $x^2=x$.',
        '$x\\ne0$ is NOT given, so do not divide by $x$. Factor: $x^2-x=0$, $x(x-1)=0$: $x=0$ or $x=1$.',
        'Check: $x=0$: $0=\\sqrt0$ ✓. $x=1$: $\\sqrt3=\\sqrt3$ ✓. Both work.'])
    P['11'] = ('$\\frac{5^{n+1}-5^n}{4}=?$', ['$5$', '$5^n$', '$5^{n-1}$', '$\\frac54$'], 2, [
        'Take out the smallest power: $5^{n+1}-5^n=5^n(5-1)=4\\cdot5^n$.',
        '$\\frac{4\\cdot5^n}{4}=5^n$.'])
    P['12'] = ('Given: $2^x+2^x=4^x$. $x=?$', ['$0$', '$1$', '$2$', 'Every number $x$ satisfies the equation.'], 2, [
        'Left side: $2^x+2^x=2\\cdot2^x=2^{x+1}$. Right side: $4^x=2^{2x}$.',
        'Equal exponents: $x+1=2x$, so $x=1$.',
        'Check: $2+2=4=4^1$ ✓. With $x=2$: $4+4=8\\ne16$, so choice (4) is the trap $2^x+2^x=4^x$.'])
    P['16'] = ('Given: $3^{20}+3^{20}+3^{20}=9^n$. $n=?$', ['$10$', '$10.5$', '$21$', '$30$'], 2, [
        'Left side: $3\\cdot3^{20}=3^{21}$. Right side: $9^n=(3^2)^n=3^{2n}$.',
        'Equal exponents: $2n=21$, so $n=10.5$.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t10-' + k, TOPIC, stem, ch, cor, ex)
    for k in ['06', '07', '08']:
        M.place_q('q-r26-t10-' + k, 'unit-t10-2')
    for k in ['09', '10', '11', '12', '16']:
        M.place_q('q-r26-t10-' + k, 'unit-t10-3')

    # =====================================================================================
    # 10. Practice order: easy -> hard
    # =====================================================================================
    M.practice_order('unit-t10-2', [
        'alg-extra-unit-t10-2-1', 'q-254', 'alg-extra-unit-t10-2-3', 'q-256', 'q-262', 'q-264', 'q-265',
        'q-263', 'alg-extra-unit-t10-2-7', 'q-260', 'q-261', 'q-257', 'q-258', 'q-259', 'q-253', 'q-255',
        'alg-extra-unit-t10-2-4', 'alg-extra-unit-t10-2-5', 'alg-extra-unit-t10-2-2', 'alg-extra-unit-t10-2-6',
        'q-266', 'q-267', 'q-r26-t10-06', 'q-r26-t10-08', 'q-r26-t10-07'])
    M.practice_order('unit-t10-3', [
        'alg-extra-unit-t10-3-1', 'q-276', 'q-277', 'alg-extra-unit-t10-3-3', 'q-283', 'q-274', 'alg-extra-unit-t10-3-7',
        'q-268', 'q-270', 'q-278', 'q-279', 'alg-extra-unit-t10-3-4', 'alg-extra-unit-t10-3-5', 'alg-extra-unit-t10-3-2',
        'alg-extra-unit-t10-3-6', 'q-272', 'q-271', 'q-273', 'q-269', 'q-280',
        'q-275', 'q-282', 'q-285', 'q-286', 'q-281', 'q-r26-t10-11', 'q-r26-t10-09', 'q-r26-t10-10',
        'q-r26-t10-12', 'q-r26-t10-16', 'q-284', 'q-287'])

    summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last


# ---------------- 2026-10-04: a question must not be a lesson example the student just watched ----------------
def _dd_sub(M, vid, n, pairs):
    """Replace exact text on one slide (board items, spoken lines, draw cues, labels). Every pair must match."""
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = 0
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit += 1
        for l in b['lines']:
            for k in ('say', 'draw', 'label'):
                if k in l and old in l[k]: l[k] = l[k].replace(old, new); hit += 1
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    M.touched_videos.add(vid)

def dedupe_examples(M):
    # q-262 (sqrt18) was worked on the board in "powers-techniques" slide 6 -> new numbers.
    M.set_q('q-262', stem=r'$\sqrt{28} = ?$',
            choices=[r'$7\,\sqrt{2}$', r'$2\,\sqrt{7}$', r'$4\,\sqrt{7}$', r'$2\,\sqrt{14}$'], correct=2,
            expl=[r'Pull out the largest square: $28=4\cdot7$, so $\sqrt{28}=\sqrt4\cdot\sqrt7=2\sqrt7$.'])
    # q-r26-t10-06 was the lesson example 3^x + 3^x + 3^x of "r26-t10-power-traps" slide 2 -> new numbers.
    M.set_q('q-r26-t10-06', stem=r'$5^x+5^x+5^x+5^x+5^x=?$',
            choices=[r'$25^x$', r'$5^{5x}$', r'$5^{x+1}$', r'$25^{5x}$'], correct=3,
            expl=[r'Five equal powers: $5^x+5^x+5^x+5^x+5^x=5\cdot5^x=5^1\cdot5^x=5^{x+1}$.',
                  r'If you check with a number, avoid $x=1$ (then $25^x=25$ too). With $x=2$: $5\cdot25=125=5^3$, while $25^2=625$.'])
    # q-r26-t10-09 was the lesson example sqrt(x + 12) = x of "r26-t09-summary" slide 10 -> new numbers
    # (sqrt(x + 6) = x is q-r26-t09-03 and sqrt(x + 20) = x is in "r26-t10-summary").
    M.set_q('q-r26-t10-09', stem=r'Given: $\sqrt{x+30}=x$. $x=?$',
            choices=['$-5$', '$6$', '$-5$ or $6$', '$5$'], correct=2,
            expl=[r'Square both sides: $x+30=x^2$, so $x^2-x-30=0$ and $(x-6)(x+5)=0$: $x=6$ or $x=-5$.',
                  r'Check: $x=6$: $\sqrt{36}=6$ ✓. $x=-5$: $\sqrt{25}=5\ne-5$ ✗ (fake solution).',
                  r'Only $x=6$. Trying the choices gives the same result: $5$ fails too ($\sqrt{35}\ne5$).'])


# ---------------------------------------------------------------- 2026-10-05 cut repeats
# The teacher: a long lesson that pre-teaches every question, then question videos that teach it again, is
# repetition. Lessons become a short intro (like the Hebrew course); a lesson slide is cut only where a question
# video in the same section teaches the same idea. Anything taught nowhere else stays, or moves into the question
# video where it is used (one spoken line + one board item). Runs last.
def _cr_script(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _cr_txt(x):
    if isinstance(x, str): return x
    if x[0] == 'A': return x[1] + ' ' + str(x[2].get('t', ''))
    return x[1]


def _cr_find(s, anchor, vid, n):
    ks = [k for k, x in enumerate(s) if anchor in _cr_txt(x)]
    assert len(ks) == 1, '%s #%d: anchor %r matches %d lines' % (vid, n, anchor, len(ks))
    return ks[0]


def _cr_insert(M, vid, n, anchor, new, before=False):
    """Insert script entries right after (or before) the line / item / draw containing `anchor`."""
    s = _cr_script(M, vid, n); k = _cr_find(s, anchor, vid, n) + (0 if before else 1)
    M.set_slide(vid, n, script=s[:k] + list(new) + s[k:])


def _cr_drop(M, vid, n, anchors):
    """Remove the lines / items / draws containing each anchor."""
    s = _cr_script(M, vid, n)
    for a in anchors: s.pop(_cr_find(s, a, vid, n))
    M.set_slide(vid, n, script=s)


def _cr_replace(M, vid, n, anchor, new):
    """Replace the entry containing `anchor` with the list `new`."""
    s = _cr_script(M, vid, n); k = _cr_find(s, anchor, vid, n)
    M.set_slide(vid, n, script=s[:k] + list(new) + s[k + 1:])


def _cr_titles(M, vid, keep):
    """Keep only the slides whose titles are in `keep` (title slide = slide 1 always kept); set the sidebar to the
    kept slides' old sidebar labels in order and re-point each kept slide's `active`."""
    v = M.video(vid); old = v.get('hybrid', {}).get('sidebar') or []
    drop = [n for n, b in enumerate(v['beats'], 1) if n > 1 and b['title'] not in keep]
    assert len(v['beats']) - len(drop) == len(keep) + 1, '%s: kept titles not found' % vid
    M.remove_slides(vid, drop)
    labels = []
    for b in v['beats'][1:]:
        lab = old[b['active']] if 0 <= b['active'] < len(old) else b['title']
        if lab not in labels: labels.append(lab)
        b['active'] = labels.index(lab)
    M.set_sidebar(vid, labels)


def _cr_slide_after(M, vid, n, title, script):
    """A short extra question slide right after slide n (same question on the board, same sidebar item), so a
    moved board item never lands on the teacher's handwriting."""
    b = M.slide(vid, n)
    M.insert_slides(vid, n, [dict(mode=b['mode'], title=title, active=b['active'],
                                  pre=[dict(it) for it in b['items'][:b['pre']]], script=script)])


def cut_repeats(M):
    # Exponents & Roots - Techniques: the Hebrew lesson teaches only dividing roots and a number over a root, then the
    # questions teach the rest. Cut: same prime base and negative exponents (Question 1), adding roots - split and
    # common factor (Question 2), power equations (Question 3, try the choices for them: Question 8), root equations,
    # the worked example and trying the choices (Questions 4 and 6), recap.
    L = 'powers-techniques'
    _cr_titles(M, L, ['Dividing roots', 'Number over a root'])
    _cr_insert(M, L, 3, 'Twenty over root five: no root', [
        'Now the questions. Each one teaches one more technique. Try it — then watch.'])
    # Question 3 no longer refers back to the lesson; the restriction from the cut slide moves here
    _cr_replace(M, 'solve-q-250', 1, 'You know the method', [
        'The unknown is up in the exponent. The method: equal bases — then equal exponents.'])
    _cr_slide_after(M, 'solve-q-250', 2, 'When it works', [
        A("'Positive base, not 1' appears", T('Equal bases $\\to$ equal exponents: for a positive base that is not $1$', 38)),
        "This works for a positive base that isn't one. One to any power is one — that tells you nothing."])

    # Exponent Traps - Sums of Powers: sums of equal powers -> Question 7; common factor -> Question 8.
    # Kept: same exponent, a^x b^x = (ab)^x (no question video here teaches it).
    T2 = 'r26-t10-power-traps'
    _cr_titles(M, T2, ['Same exponent'])
    M.set_slide(T2, 1, script=[
        'Now the exponent traps the exam loves.',
        'Adding powers and taking out a common factor — the two questions teach those.',
        'First, one reminder: powers with the same exponent.'])
    _cr_insert(M, T2, 2, 'Careful: this works only when the EXPONENTS', [
        'Two questions next. Try each one first — then watch.'])


_apply_before_cut_repeats = apply


def apply(M):
    _apply_before_cut_repeats(M)
    cut_repeats(M)   # 2026-10-05: runs last
