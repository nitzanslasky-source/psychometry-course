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


# ---------------------------------------------------------------- 2026-10-06 pen or click
# Teacher-approved split (2026-10-04/06): lessons - content appears by click, the pen only marks (circle, cross out);
# solution videos - setup and mechanical lines by click, by hand only the one or two key steps plus the marks on the
# choices. Helper copied from t07.py (same behaviour).
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


def _tighten(M, vid, n, size, gap):
    """more lines on the board now: every item a bit smaller and closer, so nothing runs off."""
    for it in M.slide(vid, n)['items']:
        it['size'] = min(it.get('size', 46), size); it['gap'] = min(it.get('gap', 44), gap)


def pen_or_click(M):
    S = 40
    # ---- lesson: powers-techniques (written lines become click items; the cross-outs stay by hand)
    V = LESSON
    _pen_or_click_slide(M, V, 2, {
        'Write "= √(48 ÷ 3) = √16 = 4"': [A('= √(48 ÷ 3) = √16 = 4 appears', T(r'$=\sqrt{48\div3}=\sqrt{16}=4$', size=50))],
        'Below, write "√48 = √16 · √3"; cross out √3 top and bottom; write "= √16 = 4"': [
            A('√48 = √16 · √3 appears', T(r'$\sqrt{48}=\sqrt{16}\cdot\sqrt3$', size=50)),
            D('Cross out √3 top and bottom'),
            A('= √16 = 4 appears', T(r'$=\sqrt{16}=4$', size=50))],
    })
    _pen_or_click_slide(M, V, 3, {
        'Write "= (2 · 3) / √3"': [A('= (2 · 3) / √3 appears', T(r'$=\frac{2\cdot3}{\sqrt3}$', size=56))],
        'Write "= (2 · √3 · √3) / √3"': [A('= (2 · √3 · √3) / √3 appears', T(r'$=\frac{2\cdot\sqrt3\cdot\sqrt3}{\sqrt3}$', size=56))],
        'Cross out one √3 on top and the √3 on the bottom; write "= 2√3"': [
            D('Cross out one √3 on top and the √3 on the bottom'), A('= 2√3 appears', T(r'$=2\sqrt3$', size=50))],
        'Write "= (4 · √5 · √5) / √5 = 4√5"': [A('= (4 · √5 · √5) / √5 = 4√5 appears',
                                               T(r'$=\frac{4\cdot\sqrt5\cdot\sqrt5}{\sqrt5}=4\sqrt5$', size=56))],
        'Next to the question write "6 ÷ 3 = 2 → 2√3"': [A('6 ÷ 3 = 2 → 2√3 appears', T(r'$6\div3=2 \;\to\; 2\sqrt3$', size=42))],
        'Next to 20/√5 write "20 ÷ 5 = 4 → 4√5"': [A('20 ÷ 5 = 4 → 4√5 appears', T(r'$20\div5=4 \;\to\; 4\sqrt5$', size=42))],
    })
    _tighten(M, V, 3, 44, 4)
    # ---- Question 1: q-248 - by hand: 9⁶ = (3²)⁶ = 3¹² (method 1 key), the pairing (method 2 key), circle
    _pen_or_click_slide(M, 'solve-q-248', 2, {
        'Write "8⁻² = (2³)⁻² = 2⁻⁶"': [A('8⁻² = 2⁻⁶ appears', T(r'$8^{-2}=\left(2^3\right)^{-2}=2^{-6}$', size=36))],
        'Write "4⁻² = (2²)⁻² = 2⁻⁴"': [A('4⁻² = 2⁻⁴ appears', T(r'$4^{-2}=\left(2^2\right)^{-2}=2^{-4}$', size=36))],
        'Write "3: 12 − 8 = 4"': [A('3: 12 − 8 = 4 appears', T(r'$3:\ \ 12-8=4$', size=36))],
        'Write "2: −6 − (−4) = −2"': [A('2: −6 − (−4) = −2 appears', T(r'$2:\ \ -6-(-4)=-2$', size=36))],
    }, room=['Under the fraction write "9⁶ = (3²)⁶ = 3¹²"'], row=80)
    _pen_or_click_slide(M, 'solve-q-248', 3, {
        'Write "= 3⁴ · 2⁻²"': [A('= 3⁴ · 2⁻² appears', T(r'$=3^4\cdot2^{-2}$', size=S))],
    }, room=['Write "(9⁶ / 3⁸) · (8/4)⁻²"'])
    # ---- Question 2: q-249 - by hand: √27 = √9 · √3 (method 1 key), the common factor √3 (method 2 key), circles
    _pen_or_click_slide(M, 'solve-q-249', 2, {
        'Write "top: 3√3 + 3√3 = 6√3"': [A('top: 6√3 appears', T(r'top: $3\sqrt3+3\sqrt3=6\sqrt3$', size=36))],
        'Write "√48 = √16·√3 = 4√3,  √12 = √4·√3 = 2√3"': [A('√48 = 4√3, √12 = 2√3 appears',
            T(r'$\sqrt{48}=\sqrt{16}\cdot\sqrt3=4\sqrt3,\ \ \sqrt{12}=\sqrt4\cdot\sqrt3=2\sqrt3$', size=36))],
        'Write "bottom: 4√3 − 2√3 = 2√3"': [A('bottom: 2√3 appears', T(r'bottom: $4\sqrt3-2\sqrt3=2\sqrt3$', size=36))],
        'Write "6√3 / 2√3 = 3" and circle choice 3': [A('6√3 / 2√3 = 3 appears', T(r'$\frac{6\sqrt3}{2\sqrt3}=3$', size=36)),
                                                     D('Circle choice 3')],
    }, room=['Write "√27 = √9 · √3 = 3√3"'], row=80)
    for it in M.slide('solve-q-249', 2)['items'][2:]: it['gap'] = 16
    _pen_or_click_slide(M, 'solve-q-249', 3, {
        'Write "top = 2√27"': [A('top = 2√27 appears', T(r'top $=2\sqrt{27}$', size=S))],
        'Write "2√27 / 2√3 = √(27 ÷ 3) = √9 = 3"': [A('2√27 / 2√3 = √9 = 3 appears',
                                                    T(r'$\frac{2\sqrt{27}}{2\sqrt3}=\sqrt{27\div3}=\sqrt9=3$', size=S))],
    }, room=['Write "bottom = √3(√16 − √4) = √3(4 − 2) = 2√3"'])
    # ---- Question 3: q-250 - by hand: 4x = −12 + 6x (same base -> equal exponents), circle
    _pen_or_click_slide(M, 'solve-q-250', 2, {
        'Under 4^(2x) write "= (2²)^(2x) = 2^(4x)"': [A('4^(2x) = 2^(4x) appears', T(r'$4^{2x}=\left(2^2\right)^{2x}=2^{4x}$', size=S))],
        'Under (1/8)^(4−2x) write "= (2⁻³)^(4−2x) = 2^(−12+6x)"': [A('(1/8)^(4−2x) = 2^(−12+6x) appears',
            T(r'$\left(\frac18\right)^{4-2x}=\left(2^{-3}\right)^{4-2x}=2^{-12+6x}$', size=S))],
        'Write "12 = 2x → x = 6" and circle choice 3': [A('12 = 2x → x = 6 appears', T(r'$12=2x \;\to\; x=6$', size=S)),
                                                       D('Circle choice 3')],
    }, room=['Write "4x = −12 + 6x"'])
    _pen_or_click_slide(M, 'solve-q-250', 4, {
        'Write "4¹² = 2²⁴" and "(1/8)⁻⁸ = 8⁸ = 2²⁴"': [
            A('4¹² = 2²⁴ appears', T(r'$4^{12}=2^{24}$', size=S)),
            A('(1/8)⁻⁸ = 8⁸ = 2²⁴ appears', T(r'$\left(\frac18\right)^{-8}=8^8=2^{24}$', size=S))],
    })
    # ---- Question 4: q-251 - by hand: (√(x − 7))² = 3² (square both sides), circle
    _pen_or_click_slide(M, 'solve-q-251', 2, {
        'Write "x − 7 = 9"': [A('x − 7 = 9 appears', T(r'$x-7=9$', size=S))],
        'Write "x = 16"': [A('x = 16 appears', T(r'$x=16$', size=S))],
        'Write "check: √(16 − 7) = √9 = 3 ✓" and circle choice 4': [
            A('check: √(16 − 7) = 3 ✓ appears', T(r'check: $\sqrt{16-7}=\sqrt9=3$ ✓', size=S)), D('Circle choice 4')],
    }, room=['Write "(√(x − 7))² = 3²"'])
    # ---- Question 5: q-252 - by hand: (x√5)² = x² · 5 (square both sides), circle
    _pen_or_click_slide(M, 'solve-q-252', 2, {
        'Write "(5√x)² = 25x"': [A('(5√x)² = 25x appears', T(r'$(5\sqrt x)^2=25x$', size=32))],
        'Write "5x² = 25x"': [A('5x² = 25x → x² = 5x appears', T(r'$5x^2=25x \;\to\; x^2=5x$', size=32))],
        'Write "x² = 5x"': [],          # now the second part of the line above
        'Write "x = 5" and circle choice 2': [A('x = 5 appears', T(r'$x=5$', size=32)), D('Circle choice 2')],
        'Write "check: 5√5 = 5√5 ✓"': [A('check: 5√5 = 5√5 ✓ appears', T(r'check: $5\sqrt5=5\sqrt5$ ✓', size=32))],
        'Write "no x ≠ 0?  x² = 5x → x² − 5x = 0 → x(x − 5) = 0 → x = 0 or x = 5"': [
            A('No x ≠ 0? x² − 5x = 0 → x(x − 5) = 0 → x = 0 or 5 appears',
              T(r'No $x\ne0$? $\ x^2-5x=0 \;\to\; x(x-5)=0 \;\to\; x=0$ or $x=5$', size=30))],
    }, room=['Write "(x√5)² = x² · 5"'], row=60)
    for it in M.slide('solve-q-252', 2)['items'][1:]: it['gap'] = 6
    # ---- Question 6: q-r26-t10-01 - by hand: x ≥ 0 (a root is never negative); the tries on the choices are clicks,
    #      the cross-outs and circle by hand
    _pen_or_click_slide(M, 'solve-q-r26-t10-01', 2, {
        'Write "2x + 3 = x²  →  x² − 2x − 3 = 0"': [A('2x + 3 = x² → x² − 2x − 3 = 0 appears', T(r'$2x+3=x^2 \;\to\; x^2-2x-3=0$', size=36))],
        'Write "(x − 3)(x + 1) = 0  →  x = 3 or x = −1"': [A('(x − 3)(x + 1) = 0 → x = 3 or x = −1 appears',
            T(r'$(x-3)(x+1)=0 \;\to\; x=3 \ \text{ or } \ x=-1$', size=36))],
        'Write "x = 3: √9 = 3 ✓"': [A('x = 3: √9 = 3 ✓ appears', T(r'$x=3:\ \ \sqrt9=3$ ✓', size=36))],
        'Write "x = −1: √1 = 1 ≠ −1 ✗"': [A('x = −1: √1 = 1 ≠ −1 ✗ appears', T(r'$x=-1:\ \ \sqrt1=1\ne-1$ ✗', size=36))],
    }, room=['Write "x ≥ 0"'], row=96)
    for it in M.slide('solve-q-r26-t10-01', 2)['items'][2:]: it['gap'] = 14
    _pen_or_click_slide(M, 'solve-q-r26-t10-01', 3, {
        'Next to choice 1 write "√1 = 1 ≠ −1" and cross out choices 1 and 4': [
            A('(1) −1: √1 = 1 ≠ −1 appears', T(r'(1) $x=-1$: $\ \sqrt1=1\ne-1$', size=S)), D('Cross out choices 1 and 4')],
        'Next to choice 2 write "√5 ≠ 1" and cross it out': [
            A('(2) 1: √5 ≠ 1 appears', T(r'(2) $x=1$: $\ \sqrt5\ne1$', size=S)), D('Cross out choice 2')],
        'Next to choice 3 write "√9 = 3 ✓" and circle it': [
            A('(3) 3: √9 = 3 ✓ appears', T(r'(3) $x=3$: $\ \sqrt9=3$ ✓', size=S)), D('Circle choice 3')],
    })
    # ---- Question 7: q-r26-t10-02 - by hand: = 4 · 2¹⁰ (count the copies), circle
    _pen_or_click_slide(M, 'solve-q-r26-t10-02', 2, {
        'Write "4 = 2²  →  2² · 2¹⁰ = 2¹²"': [A('4 = 2² → 2² · 2¹⁰ = 2¹² appears', T(r'$4=2^2 \;\to\; 2^2\cdot2^{10}=2^{12}$', size=S))],
    }, room=['Write "= 4 · 2¹⁰"'])
    _pen_or_click_slide(M, 'solve-q-r26-t10-02', 3, {
        'Write "2¹ + 2¹ + 2¹ + 2¹ = 8 = 2³"': [A('2¹ + 2¹ + 2¹ + 2¹ = 8 = 2³ appears', T(r'$2^1+2^1+2^1+2^1=8=2^3$', size=S))],
    })
    # ---- Question 8: q-r26-t10-03 - by hand: 3ˣ(9 − 1) = 72 (take out the common factor), circle
    _pen_or_click_slide(M, 'solve-q-r26-t10-03', 2, {
        'Write "3ˣ⁺² = 3ˣ · 3² = 9 · 3ˣ"': [A('3ˣ⁺² = 3ˣ · 3² = 9 · 3ˣ appears', T(r'$3^{x+2}=3^x\cdot3^2=9\cdot3^x$', size=S))],
        'Write "3ˣ = 9 = 3²  →  x = 2"': [A('3ˣ = 9 = 3² → x = 2 appears', T(r'$3^x=9=3^2 \;\to\; x=2$', size=S))],
    }, room=['Write "3ˣ(9 − 1) = 72  →  8 · 3ˣ = 72"'])
    _pen_or_click_slide(M, 'solve-q-r26-t10-03', 3, {
        'Write "x = 2: 3⁴ − 3² = 81 − 9 = 72 ✓"': [A('x = 2: 3⁴ − 3² = 72 ✓ appears', T(r'$x=2:\ \ 3^4-3^2=81-9=72$ ✓', size=S))],
    })
    # ---- lesson: Summary
    _pen_or_click_slide(M, 'r26-t10-summary', 2, {
        'Write "28 ÷ 7 = 4 → 4√7"': [A('28 ÷ 7 = 4 → 4√7 appears', T(r'$28\div7=4 \;\to\; 4\sqrt7$', size=50))],
    })
    _pen_or_click_slide(M, 'r26-t10-summary', 5, {
        'Write "3x + 1 = 4 → x = 1"': [A('3x + 1 = 4 → x = 1 appears', T(r'$3x+1=4 \;\to\; x=1$', size=50))],
    })
    _pen_or_click_slide(M, 'r26-t10-summary', 6, {
        'Write "x = 5: √25 = 5 ✓    x = −4: √16 = 4 ≠ −4 ✗"': [A('x = 5 ✓, x = −4 ✗ appears',
            T(r'$x=5:\ \sqrt{25}=5$ ✓ $\qquad x=-4:\ \sqrt{16}=4\ne-4$ ✗', size=44))],
    })
    _pen_or_click_slide(M, 'r26-t10-summary', 7, {
        'Write "x² − 7x = 0 → x(x − 7) = 0 → x = 0 or x = 7"': [A('x² − 7x = 0 → x(x − 7) = 0 → x = 0 or 7 appears',
            T(r'$x^2-7x=0 \;\to\; x(x-7)=0 \;\to\; x=0 \ \text{ or } \ x=7$', size=46))],
    })
    _pen_or_click_slide(M, 'r26-t10-summary', 8, {
        'Write "x = 2: 4 + 4 = 8, but 4² = 16"': [A('x = 2: 4 + 4 = 8, but 4² = 16 appears', T(r'$x=2:\ \ 4+4=8$, but $4^2=16$', size=46))],
    })


_apply_before_pen_or_click = apply


def apply(M):
    _apply_before_pen_or_click(M)
    pen_or_click(M)   # 2026-10-06 pen or click: runs last


# ---------------------------------------------------------------- 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived question (guided q-248..252,
# practice q-253..287) and the Hebrew lesson's own examples get new numbers - same concept, same trap, same level, same
# methods; solution videos rewritten to match (after pen_or_click, so the click items are rewritten here too). Practice
# clean-up: copies removed, September-review items whose type the Hebrew practice already covers removed.
RECORDED = set()     # nothing in topic 10 is recorded (checked ~/Documents/Course.recordings on 2026-10-06)


def _rn_slide(M, vid, n, script, pre=None, room=(), row=None):
    """Rebuild one slide (pre items kept unless given). room: {hand cue: gap} - the item right above a hand-written
    line keeps an empty row for the handwriting (same as pen_or_click)."""
    if vid in RECORDED: return
    M.set_slide(vid, n, script=script, pre=pre)
    b = M.slide(vid, n); last = b['pre'] - 1
    for l in b['lines']:
        if 'appear' in l: last = l['appear']
        elif l.get('draw') in dict(room or {}) and last >= 0: b['items'][last]['gap'] = dict(room)[l['draw']]


def renumber(M):
    from math_api import rich_plain

    def S(qid, **kw):
        if qid in RECORDED: return
        q = M.set_q(qid, **kw)
        for v in M.D['videos'].values():
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])
        v = M.D['videos'].get('solve-' + qid)
        if v: v['title'] = v['navLabel'] = rich_plain(q['stemRich'])

    # ============ lesson "Exponents & Roots — Techniques": the Hebrew lesson's examples -> new examples, same points
    L = LESSON
    _rn_slide(M, L, 2, pre=[T(r'$\frac{\sqrt{150}}{\sqrt6}$', size=76, gap=60)], script=[
        'Root one hundred fifty over root six. Two ways — both by the root rules.',
        'Way one: put them under the same root.',
        A('= √(150 ÷ 6) = √25 = 5 appears', T(r'$=\sqrt{150\div6}=\sqrt{25}=5$', size=50)),
        'One hundred fifty over six is twenty-five. Root twenty-five: five.',
        'Way two: split the top.',
        A('√150 = √25 · √6 appears', T(r'$\sqrt{150}=\sqrt{25}\cdot\sqrt6$', size=50)),
        D('Cross out √6 top and bottom'),
        A('= √25 = 5 appears', T(r'$=\sqrt{25}=5$', size=50)),
        'Root one hundred fifty is root twenty-five times root six. Now cancel root six, top and bottom. Five again.',
        'Same answer, of course. Personally? I prefer splitting.',
        'When a question has several roots and different terms to cancel, splitting is usually the easier road.',
    ])
    s = dict(size=44, gap=4)
    _rn_slide(M, L, 3, pre=[T(r'$\frac{10}{\sqrt2}$', **s)], script=[
        "Now a whole number over a root. The ten isn't under a root — so how do we cancel?",
        'Actually, you could put it under one: ten is root one hundred. Root one hundred over root two — one big root. That works.',
        "But it's easier to split the ten: ten is five times two.",
        A('= (5 · 2) / √2 appears', T(r'$=\frac{5\cdot2}{\sqrt2}$', **s)),
        'And two is root two times root two.',
        A('= (5 · √2 · √2) / √2 appears', T(r'$=\frac{5\cdot\sqrt2\cdot\sqrt2}{\sqrt2}$', **s)),
        'Because root two times root two is root two squared — and the square cancels the root.',
        D('Cross out one √2 on top and the √2 on the bottom'),
        A('= 5√2 appears', T(r'$=5\sqrt2$', **s)),
        'Cancel. Five root two.',
        A('18/√6 appears', T(r'$\frac{18}{\sqrt6}$', **s)),
        'Another one. Eighteen could be nine times two — or three times six.',
        "There's a six underneath, so choose three times six. Then six is root six times root six.",
        A('= (3 · √6 · √6) / √6 = 3√6 appears', T(r'$=\frac{3\cdot\sqrt6\cdot\sqrt6}{\sqrt6}=3\sqrt6$', **s)),
        'Cancel root six with root six: three root six.',
        'This comes up a LOT — especially in geometry, with the special right triangles, where you divide by root two or root three.',
        "So here's the one-second shortcut.",
        A('The shortcut appears: 1) ignore the root  2) add the root to the answer',
          T('Shortcut: ① ignore the root  ② put the root on the answer', size=42, gap=4)),
        A('10 ÷ 2 = 5 → 5√2 appears', T(r'$10\div2=5 \;\to\; 5\sqrt2$', size=42, gap=4)),
        "Pretend the root isn't there: ten over two is five. Then put the root back on the answer: five root two. Done — zero mistakes.",
        A('18 ÷ 6 = 3 → 3√6 appears', T(r'$18\div6=3 \;\to\; 3\sqrt6$', size=42, gap=4)),
        'Eighteen over root six: no root — eighteen over six is three. Add the root: three root six. Simple — worth mastering.',
        'Now the questions. Each one teaches one more technique. Try it — then watch.',
    ])

    # ============ guided Question 1: q-248  (9⁶·8⁻²)/(3⁸·4⁻²) = 3⁴·2⁻²  ->  (4⁵·27⁻²)/(2⁷·9⁻²) = 2³·3⁻²
    S('q-248', stem=r'$\frac{4^{5}\cdot27^{-2}}{2^{7}\cdot9^{-2}}=?$',
      choices=[r'$2^{-2}\cdot3^{3}$', r'$2^{3}\cdot3^{-2}$', r'$\frac{3^{2}}{2^{3}}$', r'$\frac{2^{3}}{3^{10}}$'], correct=2, expl=[
        r'Write every base as a prime: $4^5=(2^2)^5=2^{10}$, $27^{-2}=(3^3)^{-2}=3^{-6}$, $9^{-2}=(3^2)^{-2}=3^{-4}$.',
        r'The fraction becomes $\frac{2^{10}\cdot3^{-6}}{2^7\cdot3^{-4}}=2^{10-7}\cdot3^{-6-(-4)}=2^3\cdot3^{-2}$.',
        r'The trap is choice 4: $-6-(-4)$ is $-2$, not $-10$ (minus minus is plus).'])
    if 'q-248' not in RECORDED:
        V = 'solve-q-248'
        _rn_slide(M, V, 1, script=['Question one.',
                                   "Powers everywhere — four, twenty-seven, two, nine. Let's make them talk to each other."])
        _rn_slide(M, V, 2, script=[
            'Different bases. So break every base down to its primes — the smallest base possible.',
            D('Under the fraction write "4⁵ = (2²)⁵ = 2¹⁰"'),
            'Four is two squared. Two squared to the fifth: multiply the exponents — two to the tenth.',
            A('27⁻² = 3⁻⁶ appears', T(r'$27^{-2}=\left(3^3\right)^{-2}=3^{-6}$', size=36)),
            'Twenty-seven is three cubed. Times negative two: three to the minus six.',
            A('9⁻² = 3⁻⁴ appears', T(r'$9^{-2}=\left(3^2\right)^{-2}=3^{-4}$', size=36)),
            'On the bottom, two to the seventh stays. Nine is three squared: three to the minus four.',
            A('2: 10 − 7 = 3 appears', T(r'$2:\ \ 10-7=3$', size=36)),
            'Now subtract exponents, top minus bottom. Twos: ten minus seven — two cubed.',
            A('3: −6 − (−4) = −2 appears', T(r'$3:\ \ -6-(-4)=-2$', size=36)),
            'Threes: minus six, minus minus four. Minus minus is plus — minus two. Three to the minus two.',
            D('Circle choice 2'),
            'Two cubed times three to the minus two. Choice two.',
            'Careful — this could also show up in the choices as two cubed over three squared. The negative exponent just moves it to the bottom.',
            'And choice four is the trap: minus six plus minus four. Minus minus is plus.',
        ])
        _rn_slide(M, V, 3, script=[
            'A quick second look: pair up the families.',
            D('Write "(4⁵ / 2⁷) · (27/9)⁻²"'),
            'Fours with twos, twenty-sevens with nines.',
            A('= 2³ · 3⁻² appears', T(r'$=2^3\cdot3^{-2}$', size=40)),
            'Four to the fifth is two to the tenth, over two to the seventh: two cubed. Twenty-seven over nine is three — to the minus two.',
            'Same answer. Choice two.',
        ])

    # ============ guided Question 2: q-249  (√27+√27)/(√48−√12) = 3  ->  (√50+√50)/(√32−√8) = 5
    S('q-249', stem=r'$\frac{\sqrt{50}+\sqrt{50}}{\sqrt{32}-\sqrt{8}}=?$',
      choices=[r'$5\sqrt2$', r'$25$', r'$\sqrt5$', r'$5$'], correct=4, expl=[
        r'Simplify each root: $\sqrt{50}=5\sqrt2$, $\sqrt{32}=4\sqrt2$, $\sqrt8=2\sqrt2$.',
        r'Numerator: $5\sqrt2+5\sqrt2=10\sqrt2$. Denominator: $4\sqrt2-2\sqrt2=2\sqrt2$.',
        r'$\frac{10\sqrt2}{2\sqrt2}=5$.',
        r'Or with a common factor: the top is $2\sqrt{50}$, the bottom is $\sqrt2(\sqrt{16}-\sqrt4)=2\sqrt2$, and $\frac{2\sqrt{50}}{2\sqrt2}=\sqrt{25}=5$.'])
    if 'q-249' not in RECORDED:
        V = 'solve-q-249'
        _rn_slide(M, V, 2, script=[
            "We can't cancel yet — there's adding and subtracting. So first, simplify every root.",
            D('Write "√50 = √25 · √2 = 5√2"'),
            'Root fifty: root twenty-five times root two. Why twenty-five? Because it comes out whole. Five root two.',
            A('top: 10√2 appears', T(r'top: $5\sqrt2+5\sqrt2=10\sqrt2$', size=36)),
            'Top: five root two plus five root two — ten root two.',
            A('√32 = 4√2, √8 = 2√2 appears', T(r'$\sqrt{32}=\sqrt{16}\cdot\sqrt2=4\sqrt2,\ \ \sqrt{8}=\sqrt4\cdot\sqrt2=2\sqrt2$', size=36, gap=16)),
            'Root thirty-two: sixteen times two — four root two. Root eight: four times two — two root two.',
            A('bottom: 2√2 appears', T(r'bottom: $4\sqrt2-2\sqrt2=2\sqrt2$', size=36, gap=16)),
            'Bottom: four root two minus two root two — two root two. Like four x minus two x.',
            A('10√2 / 2√2 = 5 appears', T(r'$\frac{10\sqrt2}{2\sqrt2}=5$', size=36, gap=16)),
            D('Circle choice 4'),
            'Root two cancels. Ten over two: five. Choice four.',
        ])
        _rn_slide(M, V, 3, script=[
            'Now with a common factor.',
            A('top = 2√50 appears', T(r'top $=2\sqrt{50}$', size=40, gap=150)),
            'The top is root fifty plus root fifty. Like x plus x: two root fifty.',
            D('Write "bottom = √2(√16 − √4) = √2(4 − 2) = 2√2"'),
            'Bottom: thirty-two and eight share a two. Take out root two — inside, root sixteen minus root four. Four minus two: two. Two root two.',
            A('2√50 / 2√2 = √25 = 5 appears', T(r'$\frac{2\sqrt{50}}{2\sqrt2}=\sqrt{50\div2}=\sqrt{25}=5$', size=40)),
            'The twos cancel. Root fifty over root two: root twenty-five. Five.',
            D('Circle choice 4'),
            'Same answer — choice four. Pick whichever method feels easier.',
        ])

    # ============ guided Question 3: q-250  4^(2x) = (1/8)^(4−2x), x = 6  ->  9^(3x) = (1/27)^(2−3x), x = 2
    S('q-250', stem=r'Given: $9^{3x}=\left(\frac{1}{27}\right)^{2-3x}$. $x=?$',
      choices=[r'$1$', r'$\frac25$', r'$3$', r'$2$'], correct=4, expl=[
        r'Write both sides with base 3: $9^{3x}=(3^2)^{3x}=3^{6x}$, and $\frac1{27}=3^{-3}$, so $\left(\frac1{27}\right)^{2-3x}=3^{-3(2-3x)}=3^{-6+9x}$.',
        r'Equal bases, so the exponents are equal: $6x=-6+9x$. Therefore $3x=6$ and $x=2$.',
        r'Check: $9^6=3^{12}$ and $\left(\frac1{27}\right)^{-4}=27^4=3^{12}$ ✓. The trap $\frac25$ forgets the minus of the fraction.'])
    if 'q-250' not in RECORDED:
        V = 'solve-q-250'
        _rn_slide(M, V, 2, room={'Write "6x = −6 + 9x"': 150}, script=[
            'An exponential equation. Step one: make the bases equal.',
            'Nine and one twenty-seventh — both are powers of three.',
            A('9^(3x) = 3^(6x) appears', T(r'$9^{3x}=\left(3^2\right)^{3x}=3^{6x}$', size=40)),
            'Nine is three squared. Times three x: three to the six x.',
            "One twenty-seventh? Quick tip: ignore that it's a fraction — twenty-seven is three cubed. And because it's a fraction, add a minus.",
            A('(1/27)^(2−3x) = 3^(−6+9x) appears', T(r'$\left(\frac{1}{27}\right)^{2-3x}=\left(3^{-3}\right)^{2-3x}=3^{-6+9x}$', size=40)),
            'Three to the minus three. Multiply exponents: minus three times two — minus six. Minus three times minus three x — plus nine x.',
            D('Write "6x = −6 + 9x"'),
            'Same base on both sides. So the exponents are equal.',
            A('6 = 3x → x = 2 appears', T(r'$6=3x \;\to\; x=2$', size=40)),
            D('Circle choice 4'),
            'Move the six x across: six equals three x. x is two. Choice four.',
            'Forget the minus of the fraction, and you get two fifths — choice two, the trap.',
            'And always go to the SMALLEST base. Three — not nine, not twenty-seven.',
        ])
        _rn_slide(M, V, 4, script=[
            'Want to be sure? Plug two back in.',
            A('9⁶ = 3¹² appears', T(r'$9^{6}=3^{12}$', size=40)),
            A('(1/27)⁻⁴ = 27⁴ = 3¹² appears', T(r'$\left(\frac{1}{27}\right)^{-4}=27^4=3^{12}$', size=40)),
            'Left: nine to the sixth — three to the twelfth. Right: one twenty-seventh to the minus four — twenty-seven to the fourth — also three to the twelfth.',
            'They match. Two it is.',
        ])

    # ============ guided Question 4: q-251  √(x − 7) = 3, x = 16  ->  √(x − 6) = 5, x = 31
    S('q-251', stem=r'Given: $\sqrt{x-6}=5$. $x=?$', choices=[r'$11$', r'$19$', r'$31$', r'$25$'], correct=3, expl=[
        r'Square both sides: $x-6=25$, so $x=31$.', r'Check: $\sqrt{31-6}=\sqrt{25}=5$ ✓.',
        r'The traps: $11$ forgets to square the $5$, and $25$ forgets to move the $6$.'])
    if 'q-251' not in RECORDED:
        _rn_slide(M, 'solve-q-251', 2, script=[
            "Don't overthink it. Square both sides.",
            D('Write "(√(x − 6))² = 5²"'),
            'The square cancels the root.',
            A('x − 6 = 25 appears', T(r'$x-6=25$', size=40)),
            'Left: just x minus six. Right: five squared is twenty-five.',
            A('x = 31 appears', T(r'$x=31$', size=40)),
            'Move the six across: x is thirty-one.',
            A('check: √(31 − 6) = 5 ✓ appears', T(r'check: $\sqrt{31-6}=\sqrt{25}=5$ ✓', size=40)),
            D('Circle choice 3'),
            'Check in the original: root twenty-five is five. It works. Choice three.',
        ])

    # ============ guided Question 5: q-252  x√5 = 5√x, x ≠ 0 -> 5  ->  x√6 = 6√x, x ≠ 0 -> 6
    S('q-252', stem='Given:\n$\\begin{cases} x\\ne0 \\\\ x\\sqrt6=6\\sqrt x \\end{cases}$\n$x=?$',
      choices=[r'$\sqrt6$', r'$1$', r'$36$', r'$6$'], correct=4, expl=[
        r'Square both sides: $(x\sqrt6)^2=(6\sqrt x)^2$, so $6x^2=36x$.',
        r'Divide by 6: $x^2=6x$. Since $x\ne0$, divide by $x$: $x=6$.',
        r'Check: $6\sqrt6=6\sqrt6$ ✓.',
        r'If $x\ne0$ were not given, factor instead of dividing: $x(x-6)=0$, so $x=0$ or $x=6$.'])
    if 'q-252' not in RECORDED:
        s = dict(size=32, gap=6)
        _rn_slide(M, 'solve-q-252', 2, script=[
            "A lot of students rush to push the numbers INSIDE the roots. That works — but it's easier to just square both sides.",
            D('Write "(x√6)² = x² · 6"'),
            'Left side squared: x squared, times root six squared — which is just six. Six x squared.',
            A('(6√x)² = 36x appears', T(r'$(6\sqrt x)^2=36x$', **s)),
            'Right side: six squared is thirty-six, root x squared is x. Thirty-six x.',
            A('6x² = 36x → x² = 6x appears', T(r'$6x^2=36x \;\to\; x^2=6x$', **s)),
            'Now step by step. Divide both sides by six.',
            'x squared equals six x.',
            "Now divide by x — allowed, because the question tells us x isn't zero.",
            A('x = 6 appears', T(r'$x=6$', **s)),
            D('Circle choice 4'),
            'x is six. Choice four.',
            A('check: 6√6 = 6√6 ✓ appears', T(r'check: $6\sqrt6=6\sqrt6$ ✓', **s)),
            'Check: six root six on both sides. Perfect.',
            "One warning. We divided by x only because the question says x isn't zero.",
            A('No x ≠ 0? x² − 6x = 0 → x(x − 6) = 0 → x = 0 or 6 appears',
              T(r'No $x\ne0$? $\ x^2-6x=0 \;\to\; x(x-6)=0 \;\to\; x=0$ or $x=6$', size=30, gap=6)),
            "If that's NOT given, don't divide — factor. Then you keep both answers: zero and six.",
        ])

    # ============ memory card: examples that quoted the Hebrew lesson / Hebrew guided questions
    c = M.card('mem-r26-t10-techniques')
    c['tables'][0]['rows'][0][2] = r'$\frac{10}{\sqrt2}=5\sqrt2$'
    c['tips'][1] = (r'Mixed bases in a fraction? Pair the families: '
                    r'$\frac{4^5\cdot27^{-2}}{2^7\cdot9^{-2}}=\frac{4^5}{2^7}\cdot\left(\frac{27}{9}\right)^{-2}$.')
    c['tips'][3] = r"If $x\ne0$ is NOT given, factor — don't divide by $x$: $x^2=6x\Rightarrow x(x-6)=0$."

    # ============ practice from the Hebrew study guide: new numbers (same idea, trap and level)
    P = {
        # old: 3⁵/15² = 27/25
        'q-253': (r'$\frac{2^7}{6^2}=?$', [r'$\frac{32}{3}$', r'$\frac{16}{9}$', r'$\frac{16}{3}$', r'$\frac{32}{9}$'], 4, [
            r'$6^2=(2\cdot3)^2=2^2\cdot3^2$.', r'$\frac{2^7}{2^2\cdot3^2}=\frac{2^5}{3^2}=\frac{32}{9}$.']),
        # old: 3²·9³ = 3⁸
        'q-254': (r'$2^3\cdot4^4=?$', [r'$2^{7}$', r'$2^{9}$', r'$2^{11}$', r'$2^{12}$'], 3, [
            r'$4^4=(2^2)^4=2^8$, so $2^3\cdot2^8=2^{3+8}=2^{11}$.']),
        # old: (16³·8²)/(4⁴·2⁶) = 2⁴
        'q-255': (r'$\frac{9^4\cdot27^2}{81\cdot3^6}=?$', [r'$3^{4}$', r'$3^{5}$', r'$3^{3}$', r'$3^{6}$'], 1, [
            r'All bases are powers of 3: $9^4=3^8$, $27^2=3^6$, $81=3^4$.',
            r'Numerator: $3^8\cdot3^6=3^{14}$. Denominator: $3^4\cdot3^6=3^{10}$.',
            r'$\frac{3^{14}}{3^{10}}=3^{14-10}=3^4$.']),
        # old: 7² = 7^(x+6), x = −4
        'q-256': (r'Given: $5^3=5^{x+8}$. $x=?$', [r'$-5$', r'$5$', r'$-11$', r'$11$'], 1, [
            r'Equal bases, so the exponents are equal: $x+8=3$. Therefore $x=-5$.']),
        # old: 2⁸ = 4^(x−1), x = 5
        'q-257': (r'Given: $3^{10}=9^{x-2}$. $x=?$', [r'$12$', r'$7$', r'$6$', r'$5$'], 2, [
            r'$9=3^2$, so $9^{x-2}=3^{2(x-2)}=3^{2x-4}$.', r'Equal exponents: $2x-4=10$, so $2x=14$ and $x=7$.']),
        # old: 8⁵ = 4⁴·2ˣ, x = 7
        'q-258': (r'Given: $27^4=9^3\cdot3^x$. $x=?$', [r'$1$', r'$3$', r'$6$', r'$12$'], 3, [
            r'Base 3 everywhere: $27^4=3^{12}$ and $9^3=3^6$.', r'$3^{12}=3^6\cdot3^x=3^{6+x}$, so $6+x=12$ and $x=6$.']),
        # old: (1/5)³ = 5^(x−7), x = 4
        'q-259': (r'Given: $\left(\frac13\right)^4=3^{x-6}$. $x=?$', [r'$10$', r'$-2$', r'$-10$', r'$2$'], 4, [
            r'$\frac13=3^{-1}$, so $\left(\frac13\right)^4=3^{-4}$.', r'Equal exponents: $x-6=-4$, so $x=2$.']),
        # old: 10/√5 = 2√5
        'q-260': (r'$\frac{21}{\sqrt3}=?$', [r'$3\sqrt7$', r'$7\sqrt3$', r'$7\sqrt7$', r'$3\sqrt3$'], 2, [
            r'Ignore the root: $21\div3=7$. Put the root back on the answer: $7\sqrt3$.',
            r'Why it works: $21=7\cdot\sqrt3\cdot\sqrt3$, so $\frac{7\cdot\sqrt3\cdot\sqrt3}{\sqrt3}=7\sqrt3$.']),
        # old: 5√3/√15 = √5
        'q-261': (r'$\frac{7\sqrt2}{\sqrt{14}}=?$', [r'$\sqrt2$', r'$1$', r'$7$', r'$\sqrt7$'], 4, [
            r'Split the denominator: $\sqrt{14}=\sqrt2\cdot\sqrt7$.',
            r'Cancel $\sqrt2$: $\frac{7\sqrt2}{\sqrt2\cdot\sqrt7}=\frac7{\sqrt7}$.',
            r'Number over a root: $7\div7=1$, then put the root back: $\sqrt7$.']),
        # q-262: √18 already became √28 = 2√7 on 2026-10-04 (kept)
        # old: √63 = 3√7 (also the reverse of the Topic 9 lesson example 3√7 = √63)
        'q-263': (r'$\sqrt{117}=?$', [r'$13\sqrt3$', r'$4\sqrt3$', r'$9\sqrt{13}$', r'$3\sqrt{13}$'], 4, [
            r'$117=9\cdot13$, therefore $\sqrt{117}=\sqrt9\cdot\sqrt{13}=3\sqrt{13}$.']),  # review: √45 was the T9 warm-up alg-extra-root-practice-2
        # old: √3 + √27 = 4√3
        'q-264': (r'$\sqrt2+\sqrt{32}=?$', [r'$3\sqrt2$', r'$4\sqrt2$', r'$5\sqrt2$', r'$6\sqrt2$'], 3, [
            r'$\sqrt{32}=\sqrt{16}\cdot\sqrt2=4\sqrt2$.', r'$\sqrt2+4\sqrt2=5\sqrt2$.']),
        # old: √80 − √20 = 2√5
        'q-265': (r'$\sqrt{75}-\sqrt{12}=?$', [r'$7\sqrt3$', r'$\sqrt{63}$', r'$2\sqrt3$', r'$3\sqrt3$'], 4, [
            r'$\sqrt{75}=\sqrt{25}\cdot\sqrt3=5\sqrt3$ and $\sqrt{12}=\sqrt4\cdot\sqrt3=2\sqrt3$.',
            r'$5\sqrt3-2\sqrt3=3\sqrt3$.',
            r'The trap $\sqrt{63}$ subtracts under the root, but $\sqrt{75}-\sqrt{12}\ne\sqrt{75-12}$.']),
        # old: √(2x + 9) = 5, x = 8
        'q-266': (r'Given: $\sqrt{3x+1}=4$. $x=?$', [r'$1$', r'$\frac{17}{3}$', r'$5$', r'$3$'], 3, [
            r'Square both sides: $3x+1=16$, so $3x=15$ and $x=5$.', r'Check: $\sqrt{3\cdot5+1}=\sqrt{16}=4$ ✓.']),
        # old: √(4x + 6) = √70, x = 16
        'q-267': (r'Given: $\sqrt{5x-4}=\sqrt{66}$. $x=?$', [r'$14$', r'$12$', r'$15$', r'$13$'], 1, [
            r'Square both sides: $5x-4=66$, so $5x=70$ and $x=14$.']),
        # old: x^(x+3)·x^(−x−2) = x
        'q-268': (r'Given: $y>0$. $y^{y+4}\cdot y^{-y-5}=?$', [r'$1$', r'$\frac1y$', r'$y$', r'$0$'], 2, [
            r'Same base: add the exponents. $(y+4)+(-y-5)=-1$, so the product is $y^{-1}=\frac1y$.',
            r'Faster: choose an easy value, $y=2$: $2^6\cdot2^{-7}=2^{-1}=\frac12$. Only choice (2) gives $\frac12$ (the others are $1$, $2$ and $0$).']),
        # old: √(x²) = 5, could be −5
        'q-269': (r'Given: $\sqrt{x^2}=7$. Which of the following could be the value of $x$?',
                  [r'$49$', r'$\frac17$', r'$-1$', r'$-7$'], 4, [
            r'$\sqrt{x^2}=|x|$, so $|x|=7$: $x=7$ or $x=-7$.', r'Only $-7$ is among the choices.']),
        # old: a^(a+2)/a² = aᵃ (with a = 2 two choices tie)
        'q-270': (r'Given: $b>0$. $\frac{b^{b+3}}{b^3}=?$', [r'$b^b$', r'$(b+3)^b$', r'$2b$', r'$b^{b+6}$'], 1, [
            r'Same base: subtract the exponents. $\frac{b^{b+3}}{b^3}=b^{b+3-3}=b^b$.',
            r'With easy values: $b=2$ gives $\frac{2^5}{2^3}=4$, but two choices give $4$ ($b^b$ and $2b$). Try another number: $b=3$ gives $\frac{3^6}{3^3}=27$, and only $b^b=27$ fits.']),
        # old: 16ˣ·4ˣ·2ˣ = 2^(7x)
        'q-271': (r'$27^x\cdot9^x\cdot3^x=?$', [r'$3^{4x}$', r'$3^{6x}$', r'$3^{3x}$', r'$27^{3x}$'], 2, [
            r'Write every base as a power of 3: $27^x=3^{3x}$, $9^x=3^{2x}$.',
            r'Add the exponents: $3x+2x+x=6x$, so the product is $3^{6x}$.']),
        # old: (9³·3⁴)/81 = 3⁶
        'q-272': (r'$\frac{8^3\cdot2^5}{32}=?$', [r'$2$', r'$2^{4}$', r'$2^{14}$', r'$2^{9}$'], 4, [
            r'Base 2 everywhere: $8^3=2^9$ and $32=2^5$.', r'$\frac{2^9\cdot2^5}{2^5}=2^9$.']),
        # old: 36⁴ = 6⁸ (216², (6²)⁸, 72²)
        'q-273': (r'$25^4=?$', [r'$125^{2}$', r'$50^{2}$', r'$5^{8}$', r'$\left(5^2\right)^{8}$'], 3, [
            r'$25=5^2$, so $25^4=(5^2)^4=5^8$.',
            r'The others: $125^2=(5^3)^2=5^6$, $(5^2)^8=5^{16}$, and $50^2=(2\cdot25)^2=4\cdot5^4$. None of them is $5^8$.']),
        # old: 2^(n+1) = 64, n = 5
        'q-274': (r'Given: $3^{n+2}=243$. $n=?$', [r'$5$', r'$1$', r'$3$', r'$7$'], 3, [
            r'$243=3^5$, so $n+2=5$ and $n=3$.']),
        # old: (5^(−√3))^(−√3) = 125
        'q-275': (r'$\left(2^{-\sqrt5}\right)^{-\sqrt5}=?$', [r'$2^{\sqrt5}$', r'$2$', r'$32$', r'$4^{\sqrt5}$'], 3, [
            r'Power of a power: multiply the exponents. $(-\sqrt5)\cdot(-\sqrt5)=(\sqrt5)^2=5$.',
            r'So the expression is $2^5=32$.']),
        # old: 7ˣ·7⁻ˣ = 1
        'q-276': (r'$6^x\cdot6^{-x}=?$', [r'$1$', r'$36$', r'$\frac16$', r'$6$'], 1, [
            r'Add the exponents: $x+(-x)=0$, so the product is $6^0=1$.']),
        # old: x = y = 8, x^(y−x)·y^(x−y) = 1
        'q-277': (r'Given: $m=n=6$. $m^{n-m}\cdot n^{m-n}=?$', [r'$36$', r'$1$', r'$0$', r'$6$'], 2, [
            r'Since $m=n=6$, both exponents are zero: $n-m=6-6=0$ and $m-n=6-6=0$.',
            r'Therefore the product is $6^0\cdot6^0=1\cdot1=1$.']),
        # old: 5a⁸c⁶/(a²c³) = 5a⁶c³
        'q-278': (r'Given: $x>0$ and $y>0$. $\frac{3x^9y^4}{x^3y^2}=?$',
                  [r'$3x^6y^2$', r'$3x^3y^2$', r'$3x^{12}y^6$', r'$3x^9y^4$'], 1, [
            r'Handle each base on its own and subtract the exponents: $x^{9-3}=x^6$ and $y^{4-2}=y^2$.',
            r'The 3 does not change: $3x^6y^2$.']),
        # old: (3⁴)³·3⁻¹⁴ = 1/9
        'q-279': (r'$\left(2^3\right)^4\cdot2^{-15}=?$', [r'$-8$', r'$\frac{1}{256}$', r'$\frac{1}{8}$', r'$-\frac{1}{8}$'], 3, [
            r'Power of a power: multiply the exponents. $(2^3)^4=2^{12}$.',
            r'$2^{12}\cdot2^{-15}=2^{-3}=\frac1{2^3}=\frac18$.',
            r'The traps: adding $3+4$ gives $2^{-8}=\frac1{256}$, and a negative exponent never makes the number negative.']),
        # old: x^(3/4)·x^(4/3) = x^(25/12)
        'q-280': (r'Given: $x>0$. $x^{\frac25}\cdot x^{\frac52}=?$',
                  [r'$x^{\frac{29}{10}}$', r'$1$', r'$x^{\frac{10}{29}}$', r'$x$'], 1, [
            r'Same base: add the exponents. $\frac25+\frac52=\frac4{10}+\frac{25}{10}=\frac{29}{10}$.',
            r'So the product is $x^{\frac{29}{10}}$. (Multiplying the exponents gives $x^1=x$ — the trap.)']),
        # old: 3ˣ·4ˣ·5ˣ = ∛60, x = 1/3
        'q-281': (r'Given: $2^x\cdot3^x\cdot7^x=\sqrt{42}$. $x=?$', [r'$2$', r'$\frac13$', r'$1$', r'$\frac12$'], 4, [
            r'Same exponent, so multiply the bases: $2^x\cdot3^x\cdot7^x=(2\cdot3\cdot7)^x=42^x$.',
            r'$\sqrt{42}=42^{\frac12}$. Equal bases, so $x=\frac12$.']),
        # old: x + y + z = 5, 3ˣ·3ʸ·3ᶻ = 243
        'q-282': (r'Given: $a+b+c=4$. $2^a\cdot2^b\cdot2^c=?$',
                  [r'$8$', r'$16$', r'$64$', 'It cannot be determined from the information given.'], 2, [
            r'$2^a\cdot2^b\cdot2^c=2^{a+b+c}=2^4=16$.',
            r'We do not need $a$, $b$ and $c$ one by one — only their sum, and it is given.']),
        # old: √98 = 7√2
        'q-283': (r'$\sqrt{112}=?$', [r'$16\sqrt7$', r'$7\sqrt2$', r'$2\sqrt{14}$', r'$4\sqrt7$'], 4, [
            r'$112=16\cdot7$, therefore $\sqrt{112}=\sqrt{16}\cdot\sqrt7=4\sqrt7$.']),
        # old: letters a, b; key a·b = a + b in position 2
        'q-284': (r'The numbers $m$ and $n$ are such that $x^m\cdot x^n=x^{mn}$ for every $x>1$. Which of the following is necessarily true?',
                  [r'$m+n=0$', r'$m^n=m+n$', r'$m\cdot n=m+n$', 'None of the above is necessarily true.'], 3, [
            r'Same base: $x^m\cdot x^n=x^{m+n}$ always.',
            r'This equals $x^{mn}$ for every $x>1$, so the exponents are equal: $m+n=mn$.',
            r'Choices (1) and (2) are not necessarily true. For example, $m=3$ and $n=\frac32$: $m+n=mn=4.5$, but $m+n\ne0$ and $3^{1.5}\approx5.2\ne4.5$.']),
        # old: ⁴√(5⁶) = 5√5
        'q-285': (r'$\sqrt[4]{7^6}=?$', [r'$7^2$', r'$7\sqrt7$', r'$\sqrt7$', r'$\sqrt[4]7$'], 2, [
            r'$\sqrt[4]{7^6}=7^{\frac64}=7^{\frac32}=7^1\cdot7^{\frac12}=7\sqrt7$.']),
        # old: x > 0, √(48x) = √3·x, x = 16
        'q-286': ('Given:\n$\\begin{cases} x>0 \\\\ \\sqrt{50x}=\\sqrt2\\cdot x \\end{cases}$\n$x=?$',
                  [r'$25$', r'$5$', r'$\sqrt2$', r'$2$'], 1, [
            r'Square both sides: $50x=2x^2$.', r'Since $x>0$, divide by $2x$: $25=x$.',
            r'Check: $\sqrt{50\cdot25}=\sqrt{625\cdot2}=25\sqrt2$ and $\sqrt2\cdot25=25\sqrt2$ ✓.']),
        # old: Dana 7 > √5 + √20 (right), Yoav 4√3 > 5√2 (wrong)
        'q-287': ('Noa says: $8>\\sqrt7+\\sqrt{28}$.\nEthan says: $3\\sqrt5>4\\sqrt3$.\nWhich of the following is correct?',
                  ['Both are right.', 'Only Ethan is right.', 'Only Noa is right.', 'Both are wrong.'], 3, [
            r'Noa: $\sqrt{28}=2\sqrt7$, so $\sqrt7+\sqrt{28}=3\sqrt7$. Square both: $(3\sqrt7)^2=63$ and $8^2=64$. Since $63<64$, Noa is right.',
            r'Ethan: square both: $(3\sqrt5)^2=45$ and $(4\sqrt3)^2=48$. Since $45<48$, $3\sqrt5<4\sqrt3$ and Ethan is wrong.',
            'Only Noa is right.']),
        # English item, but (5^(n+1) − 5ⁿ)/4 was nearly the summary lesson's example 5^(x+1) − 5ˣ = 4·5ˣ
        'q-r26-t10-11': (r'$\frac{7^{n+1}-7^n}{6}=?$', [r'$7$', r'$7^n$', r'$7^{n-1}$', r'$\frac76$'], 2, [
            r'Take out the smallest power: $7^{n+1}-7^n=7^n(7-1)=6\cdot7^n$.', r'$\frac{6\cdot7^n}{6}=7^n$.']),
    }
    for qid, (stem, ch, cor, ex) in P.items():
        S(qid, stem=stem, choices=ch, correct=cor, expl=ex)

    # ============ practice clean-up (teacher-approved 2026-10-06)
    # copies: the two extra banks repeat each other and Topic 8/9 extras; q-r26-t10-09 repeats guided Question 6
    for qid in (['alg-extra-unit-t10-2-%d' % k for k in range(1, 8)] + ['alg-extra-unit-t10-3-%d' % k for k in range(1, 8)]
                + ['q-r26-t10-09']):
        M.unplace(qid)
    # September-review items whose type the Hebrew practice already covers: 0.2ˣ = 25 (q-259, a reciprocal base),
    # 4ˣ·25ˣ = 10⁶ (q-281, same exponent -> multiply the bases)
    for qid in ['q-r26-t10-07', 'q-r26-t10-08']:
        M.unplace(qid)
    # order: one root first, then adding roots, a number over a root, root equations, then power equations
    M.practice_order('unit-t10-2', ['q-254', 'q-256', 'q-262', 'q-263', 'q-264', 'q-265', 'q-260', 'q-261',
                                    'q-266', 'q-267', 'q-257', 'q-258', 'q-259', 'q-253', 'q-255', 'q-r26-t10-06'])


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber(M)   # 2026-10-06 renumber pass: runs last
