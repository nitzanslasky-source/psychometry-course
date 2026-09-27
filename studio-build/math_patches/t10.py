"""Topic 10 - Laws of Exponents & Roots (techniques). Course review 2026-09 fixes.
See t10_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q

TOPIC = 10
LESSON = 'powers-techniques'
TRAPS = 'r26-t10-power-traps'
QSIDEBAR = ['Question %d' % n for n in range(1, 11)]


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

    # slide 9: root equations - a complete example with a fake solution
    M.set_slide(LESSON, 9, pre=[T('$\\sqrt{x+2}=x$', size=66, gap=60)], script=[
        "An equation with a root? Get rid of the root: square both sides.",
        "But first — a root is never negative. So the other side can't be negative either.",
        D('Under it write "x ≥ 0"'),
        "Here the other side is x. So x can't be negative.",
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

    # new slide 10: method 2 for root equations - try the choices
    M.insert_slides(LESSON, 9, [dict(mode='concept', active=8, title='Try the choices', script=[
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

    M.sections['power-theory']['title'] = 'Ten guided questions'

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
    S('alg-extra-unit-t10-2-6', stem='Which is greater: $2^{12}$ or $4^5$?',
      choices=['They are equal.', 'It cannot be determined from the information given.', '$2^{12}$', '$4^5$'],
      expl=['Same base: $4^5=(2^2)^5=2^{10}$.', '$2^{12}>2^{10}$, so $2^{12}$ is greater.'])
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

    for qid in ['q-251', 'q-252']:              # stems changed: keep video title and slide notes in sync
        v = M.video('solve-' + qid); q = M.q(qid)
        v['title'] = v['navLabel'] = q['stem']
        for b in v['beats']:
            if b.get('canvas', '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])

    # =====================================================================================
    # 4. Practice: remove the duplicate extra set and near-duplicates
    # =====================================================================================
    for k in range(1, 8):
        M.unplace('alg-extra-unit-t10-3-%d' % k)       # same 7 templates as extra set 2
    for qid in ['q-263', 'q-283', 'q-277']:            # plain "simplify a root" x3; x = y = 8 trivial
        M.unplace(qid)

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
    # 6. New lesson video: sums of powers, same exponent, comparing, bases between 0 and 1
    # =====================================================================================
    sb = ['Sums of equal powers', 'Common factor', 'Same exponent', 'Compare powers',
          'Bases between 0 and 1', 'When is aˣ = bˣ?', 'Recap']
    M.new_video(TRAPS, TOPIC, 'Exponent Traps — Sums & Comparisons', sb, [
        dict(mode='title', title='Exponent Traps — Sums & Comparisons', script=[
            "Now the exponent traps the exam loves.",
            "Adding powers, comparing powers, and bases smaller than one.",
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
        dict(mode='question', active=3, title='Compare powers', pre=[T('$2^{30}\\quad ?\\quad 3^{20}$', size=72, gap=60)], script=[
            "Which is bigger: two to the thirtieth, or three to the twentieth?",
            "No common base here. Two and three are different primes.",
            "So turn the idea around: make the EXPONENTS equal.",
            "Thirty and twenty — both divide by ten.",
            D('Under 2³⁰ write "= (2³)¹⁰ = 8¹⁰"'),
            "Two to the thirtieth is two cubed, to the tenth. Eight to the tenth.",
            D('Under 3²⁰ write "= (3²)¹⁰ = 9¹⁰"'),
            "Three to the twentieth is three squared, to the tenth. Nine to the tenth.",
            D('Write "8¹⁰ < 9¹⁰  →  2³⁰ < 3²⁰"'),
            "Same exponent, so the bigger base wins. Nine beats eight: three to the twentieth is bigger.",
            "So the bigger exponent does NOT always win.",
            D('Write "same base → compare exponents;  same exponent → compare bases"'),
            "The rule: same base, compare the exponents. Same exponent, compare the bases.",
        ]),
        dict(mode='concept', active=4, title='Bases between 0 and 1', script=[
            "One more trap: a base between zero and one.",
            A('(1/2)² = 1/4, (1/2)³ = 1/8 appears', T('$\\left(\\frac12\\right)^2=\\frac14\\qquad\\left(\\frac12\\right)^3=\\frac18$', size=58, gap=50)),
            "One half squared is one quarter. One half cubed is one eighth.",
            "The exponent went UP — and the number went DOWN.",
            "Each time you multiply by one half, the number gets smaller.",
            A('(1/2)ˣ > (1/2)ʸ → x < y appears', T('$\\left(\\frac12\\right)^x>\\left(\\frac12\\right)^y\\ \\Rightarrow\\ x<y$', size=58)),
            "So with a base between zero and one, the order flips.",
            "If one half to the x is bigger than one half to the y, then x is SMALLER than y.",
            D('Write "base > 1: bigger exponent → bigger number;  0 < base < 1: bigger exponent → smaller number"'),
            "Base bigger than one: bigger exponent, bigger number. Base between zero and one: bigger exponent, smaller number.",
            "Decimals too: zero point two is one fifth. Zero point five is one half.",
        ]),
        dict(mode='concept', active=5, title='When is aˣ = bˣ?', script=[
            "Last one.",
            A('2ˣ = 3ˣ appears', T('$2^x=3^x$', size=66, gap=50)),
            "Two to the x equals three to the x. What's x?",
            "Different bases, so we can't make the bases equal.",
            "Think: when do two different positive bases give the same result? Only when both results are one.",
            D('Write "x = 0: 2⁰ = 1 = 3⁰ ✓"'),
            "Any number to the zero is one. So x equals zero — and that's the only answer.",
            A('5ˣ⁺¹ = 7ˣ⁺¹ appears', T('$5^{x+1}=7^{x+1}$', size=66)),
            D('Write "x + 1 = 0 → x = −1"'),
            "Same idea here: the exponent must be zero. x plus one is zero, so x is minus one.",
        ]),
        dict(mode='concept', active=6, title='Recap', script=[
            "Let's lock it in.",
            A("'Equal powers: count the copies' appears", T('Equal powers: count the copies — $2^x+2^x=2^{x+1}$', size=38)),
            A("'Different exponents: take out the smallest power' appears", T('Different exponents: take out the smallest power', size=38)),
            A("'Same exponent: multiply the bases' appears", T('Same exponent: $a^x\\cdot b^x=(ab)^x$', size=38)),
            A("'Compare: equal bases or equal exponents' appears", T('Compare: make the bases or the exponents equal', size=38)),
            A("'Base between 0 and 1: the order flips' appears", T('Base between 0 and 1: the order flips', size=38)),
            A("'Different bases, equal powers: exponent is 0' appears", T('$a^x=b^x$ with different positive bases: $x=0$', size=38)),
            D('Tick each line'),
            "Four questions next. Try each one first — then watch.",
        ]),
    ], 'power-theory', after='solve-' + g1)

    # =====================================================================================
    # 7. Guided questions 7-10
    # =====================================================================================
    g2, g3, g4, g5 = ['q-r26-t10-%02d' % k for k in (2, 3, 4, 5)]
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

    M.new_q(g4, TOPIC, 'Given:\n$\\begin{cases} a=2^{45} \\\\ b=3^{30} \\\\ c=5^{15} \\end{cases}$\nWhich of the following is correct?',
            ['$a<b<c$', '$c<b<a$', '$c<a<b$', '$a<c<b$'], 3, [
        'The exponents 45, 30 and 15 all divide by 15. Make the exponents equal:',
        '$a=2^{45}=(2^3)^{15}=8^{15}$, $b=3^{30}=(3^2)^{15}=9^{15}$, $c=5^{15}$.',
        'Same exponent, so compare the bases: $5<8<9$. Therefore $c<a<b$.'])
    M.place_q(g4, 'power-theory', after='solve-' + g3)
    _solution(M, g4, ["Question nine.", "Three powers. Different bases, different exponents. Which order?"], [
        ('Equal exponents', [
            "No common base: two, three and five are all primes.",
            "So make the exponents equal. Forty-five, thirty, fifteen — all divide by fifteen.",
            D('Write "a = 2⁴⁵ = (2³)¹⁵ = 8¹⁵"'),
            "a: two cubed is eight. Eight to the fifteenth.",
            D('Write "b = 3³⁰ = (3²)¹⁵ = 9¹⁵"'),
            "b: three squared is nine. Nine to the fifteenth.",
            D('Write "c = 5¹⁵"'),
            "c is already five to the fifteenth.",
            D('Write "5 < 8 < 9  →  c < a < b"'),
            "Same exponent, so compare the bases: five, eight, nine. c, then a, then b.",
            D('Circle choice 3'),
            "Choice three.",
            "The trap is choice two — \"the biggest exponent wins\". It doesn't.",
        ]),
    ])

    M.new_q(g5, TOPIC, 'Given: $\\left(\\frac13\\right)^x>\\frac1{27}$. Which of the following is necessarily true?',
            ['$x>3$', '$x<3$', '$x>-3$', '$x<-3$'], 2, [
        '$\\frac1{27}=\\left(\\frac13\\right)^3$, so $\\left(\\frac13\\right)^x>\\left(\\frac13\\right)^3$.',
        'The base is between 0 and 1, so a bigger exponent gives a smaller number. The order flips: $x<3$.',
        'Check: $x=0$ gives $1>\\frac1{27}$ ✓, and $x=4$ gives $\\frac1{81}<\\frac1{27}$ ✗.',
        'Choices (3) and (4) are not necessarily true: $x=-4$ works ($81>\\frac1{27}$) but is not greater than $-3$; $x=0$ works but is not less than $-3$.'])
    M.place_q(g5, 'power-theory', after='solve-' + g4)
    _solution(M, g5, ["Question ten.", "A base between zero and one. Watch the direction."], [
        ('Same base, then flip', [
            "Make the bases equal. One twenty-seventh is one third, cubed.",
            D('Write "1/27 = (1/3)³"'),
            D('Write "(1/3)ˣ > (1/3)³"'),
            "Now: one third to the x is bigger than one third cubed.",
            "The base is between zero and one. Bigger exponent, smaller number. So the order flips.",
            D('Write "x < 3"'),
            "To get a bigger number, x must be SMALLER than three.",
            D('Circle choice 2'),
            "Choice two. Choice one is the trap — it forgets to flip.",
        ]),
        ('Check with numbers', [
            "Quick check with easy numbers.",
            D('Write "x = 0: 1 > 1/27 ✓"'),
            "x equals zero: one is bigger than one twenty-seventh. It works — and zero is less than three.",
            D('Write "x = 4: 1/81 < 1/27 ✗"'),
            "x equals four: one eighty-first is smaller. It fails — and four is not less than three. The rule holds.",
            "Choices three and four? x equals zero works, but it's not less than minus three. And x equals minus four works, but it's not greater than minus three. Not necessarily true.",
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
            ['Comparing powers', 'make the bases or the exponents equal', '$2^{30}=8^{10}<9^{10}=3^{20}$'],
            ['Base between 0 and 1', 'bigger exponent, smaller number', '$\\left(\\frac12\\right)^x>\\left(\\frac12\\right)^y\\Rightarrow x<y$'],
            ['Power equation', 'equal bases, then equal exponents', '$3^{2x-1}=3^3\\Rightarrow x=2$'],
            ['$a^x=b^x$, $a\\ne b$ (positive)', 'the exponent is 0', '$2^x=3^x\\Rightarrow x=0$'],
            ['Root equation', 'square, solve, check in the original', '$\\sqrt{x+2}=x\\Rightarrow x=2$ only'],
        ]}],
        'tips': [
            'Trap: $2^x+2^x\\ne4^x$. Check with $x=3$: $8+8=16$, but $4^3=64$.',
            'Mixed bases in a fraction? Pair the families: $\\frac{9^6\\cdot8^{-2}}{3^8\\cdot4^{-2}}=\\frac{9^6}{3^8}\\cdot\\left(\\frac84\\right)^{-2}$.',
            'Four choices? Try them. It is often faster, and it throws out fake solutions of root equations.',
            'If $x\\ne0$ is NOT given, factor — don\'t divide by $x$: $x^2=5x\\Rightarrow x(x-5)=0$.',
            'Expression choices? Choose an easy value ($x=2$ or $x=3$). If two choices match, try another number.',
        ]}, after='solve-' + g5)

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
    P['13'] = ('Given: $5^{x-2}=7^{x-2}$. $x=?$', ['$0$', '$2$', '$7$', 'There is no such number $x$.'], 2, [
        'Different positive bases give the same result only when the exponent is 0 (both sides equal 1).',
        '$x-2=0$, so $x=2$. Check: $5^0=1=7^0$ ✓.'])
    P['14'] = ('For which values of $x$ is $\\left(\\frac12\\right)^{2x-1}<\\frac18$?', ['$x<2$', '$x>2$', '$x<1$', '$x>1$'], 2, [
        '$\\frac18=\\left(\\frac12\\right)^3$, so $\\left(\\frac12\\right)^{2x-1}<\\left(\\frac12\\right)^3$.',
        'The base is between 0 and 1, so the order flips: $2x-1>3$, so $2x>4$ and $x>2$.',
        'Check: $x=3$ gives $\\left(\\frac12\\right)^5=\\frac1{32}<\\frac18$ ✓. $x=1.5$ gives $\\left(\\frac12\\right)^2=\\frac14>\\frac18$ ✗, so $x>1$ is not enough.'])
    P['15'] = ('Which of the following is the greatest?', ['$2^{40}$', '$3^{30}$', '$4^{20}$', '$5^{20}$'], 2, [
        'All exponents divide by 10. Make the exponents equal:',
        '$2^{40}=(2^4)^{10}=16^{10}$, $3^{30}=(3^3)^{10}=27^{10}$, $4^{20}=(4^2)^{10}=16^{10}$, $5^{20}=(5^2)^{10}=25^{10}$.',
        'The biggest base is 27, so $3^{30}$ is the greatest. (The biggest exponent, $2^{40}$, is the trap.)'])
    P['16'] = ('Given: $3^{20}+3^{20}+3^{20}=9^n$. $n=?$', ['$10$', '$10.5$', '$21$', '$30$'], 2, [
        'Left side: $3\\cdot3^{20}=3^{21}$. Right side: $9^n=(3^2)^n=3^{2n}$.',
        'Equal exponents: $2n=21$, so $n=10.5$.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t10-' + k, TOPIC, stem, ch, cor, ex)
    for k in ['06', '07', '08']:
        M.place_q('q-r26-t10-' + k, 'unit-t10-2')
    for k in ['09', '10', '11', '12', '13', '14', '15', '16']:
        M.place_q('q-r26-t10-' + k, 'unit-t10-3')

    # =====================================================================================
    # 10. Practice order: easy -> hard
    # =====================================================================================
    M.practice_order('unit-t10-2', [
        'alg-extra-unit-t10-2-1', 'q-254', 'alg-extra-unit-t10-2-3', 'q-256', 'q-262', 'q-264', 'q-265',
        'alg-extra-unit-t10-2-7', 'q-260', 'q-261', 'q-257', 'q-258', 'q-259', 'q-253', 'q-255',
        'alg-extra-unit-t10-2-4', 'alg-extra-unit-t10-2-5', 'alg-extra-unit-t10-2-2', 'alg-extra-unit-t10-2-6',
        'q-266', 'q-267', 'q-r26-t10-06', 'q-r26-t10-08', 'q-r26-t10-07'])
    M.practice_order('unit-t10-3', [
        'q-276', 'q-274', 'q-268', 'q-270', 'q-278', 'q-279', 'q-272', 'q-271', 'q-273', 'q-269', 'q-280',
        'q-275', 'q-282', 'q-285', 'q-286', 'q-281', 'q-r26-t10-11', 'q-r26-t10-09', 'q-r26-t10-10',
        'q-r26-t10-13', 'q-r26-t10-12', 'q-r26-t10-14', 'q-r26-t10-15', 'q-r26-t10-16', 'q-284', 'q-287'])
