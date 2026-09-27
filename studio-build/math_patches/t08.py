"""Topic 8 - Exponent Laws, Fundamentals. Course review 2026-09 fixes (see t08_CHANGES.md)."""
from math_api import T, H, A, D, Q

TOPIC = 8
VID = 'exponents'
CORE = 'exponent-core'
PRACTICE = 'exponent-extra'
T9_PRACTICE = 'root-practice'
SOLVE_TITLE = 'Exponent Questions'


def _move_slide(M, vid, frm, to):
    """API has no 'move slide': move beat frm (1-based) so it becomes slide number `to`."""
    beats = M.video(vid)['beats']
    b = beats.pop(frm - 1)
    beats.insert(to - 1, b)
    M.touched_videos.add(vid)


def _replace_say(M, vid, n, old, new):
    def fn(lines):
        hit = False
        for l in lines:
            if l.get('say') == old:
                l['say'] = new; hit = True
        assert hit, (vid, n, old)
        return lines
    M.edit_lines(vid, n, fn)


# ----------------------------------------------------------------------------------------------------------------
# 1. Main lesson video: order fix, wrong rules, "copies" slide
# ----------------------------------------------------------------------------------------------------------------
def fix_lesson(M):
    # order: 1 title, 2 what a power is, 3 exponent 1 and 0, 4 negative exponents (was 5), 5 bases 1 and 0 (was 4) ...
    _move_slide(M, VID, 5, 4)

    # slide 3 - exponent 0 without the division law (not taught yet): the "divide by 5" staircase
    M.set_slide(VID, 3, title='Exponent 1 and 0', mode='concept', pre=[], script=[
        A('a¹ = a appears', T('$a^1=a$', size=58, gap=60)),
        "Any number to the power of one is itself. One copy of the base — that's it.",
        A('The staircase appears: 5³, 5², 5¹, 5⁰', T(r'$5^3=125 \qquad 5^2=25 \qquad 5^1=5 \qquad 5^0=\,?$', size=50, gap=60)),
        "Now watch the powers of five go down, one step at a time.",
        D('Draw an arrow "÷ 5" between each pair of neighbors'),
        "Each step down, there is one five fewer. So we divide by five.",
        "A hundred twenty-five, twenty-five, five. One more step: five divided by five.",
        D('Write "1" in place of the question mark'),
        "One. So five to the zero is one.",
        A('a⁰ = 1 (a ≠ 0) appears', T(r'$a^0=1\quad(a\ne0)$', size=58, gap=60)),
        "Any nonzero number to the power of zero is ONE.",
        A('(−7)⁰ and (3/7)⁰ appear', T(r'$(-7)^0 \qquad \left(\frac{3}{7}\right)^0$', size=58)),
        D('Write "= 1" after each one'),
        "Negative base, fraction base — doesn't matter. The whole bracket to the zero: one.",
    ])

    # slide 4 - negative exponents continue the staircase
    M.set_slide(VID, 4, title='Negative exponents', mode='concept', pre=[], script=[
        "Keep walking down the stairs. Five to the zero is one.",
        A('The staircase continues: 5⁰ = 1, 5⁻¹ = 1/5, 5⁻² = 1/25',
          T(r'$5^0=1 \qquad 5^{-1}=\frac{1}{5} \qquad 5^{-2}=\frac{1}{25}$', size=50, gap=60)),
        "One more step: divide by five again. One fifth. That's five to the minus one.",
        "Another step: one over twenty-five. Five to the minus two.",
        "A negative exponent does NOT make the number negative.",
        "It tells you: one over the power. Flip it.",
        A('2⁻³ appears', T('$2^{-3}$', size=62, gap=60)),
        D('Write "= 1/2³ = 1/8"'),
        "Two to the minus three: one over two cubed. One eighth.",
        A('(2/5)⁻³ appears', T(r'$\left(\frac{2}{5}\right)^{-3}$', size=66)),
        D('Write "= (5/2)³ = 125/8"'),
        "A fraction? Flip the fraction, and the minus in the exponent disappears.",
        "Five cubed over two cubed: a hundred twenty-five eighths. Positive.",
        'The minus in the exponent means "flip". A minus in the base decides the sign. Keep them apart.',
    ])

    # slide 5 (bases 1 and 0) - the reason now comes after negative exponents
    _replace_say(M, VID, 5, "A negative exponent means dividing by zero — undefined. Zero to the zero? Not defined in this course either.",
                 "Zero to a negative power means one over zero. You can't divide by zero — undefined.")
    M.edit_lines(VID, 5, lambda ls: ls[:-1] + [{'say': "Zero to the zero? Not defined in this course either."}] + ls[-1:])

    # slide 9 - "two sixteen"
    _replace_say(M, VID, 9, "Two times three, cubed — or two cubed times three cubed. Same thing: two sixteen. You'll use this a LOT.",
                 "Two times three, cubed — or two cubed times three cubed. Same thing: two hundred sixteen. You'll use this a LOT.")

    # slide 11 - b must be an even WHOLE number
    b11 = M.slide(VID, 11)
    b11['items'][2]['t'] = 'Option 2:  $a=-1$ — $b$ an even whole number'
    _replace_say(M, VID, 11, "Option two: a is negative one — but then b must be even.",
                 "Option two: a is negative one — but then b must be an even whole number. Two, four, minus two...")
    for l in b11['lines']:
        if l.get('label') == 'Option 2 appears: a = −1, b even': l['label'] = 'Option 2 appears: a = −1, b an even whole number'

    # slide 12 - the overclaim: only among POSITIVE WHOLE numbers
    M.set_slide(VID, 12, title='2⁴ = 4²', mode='concept', pre=[], script=[
        "Usually, swapping the base and the exponent changes the answer.",
        A('2³ and 3² appear', T(r'$2^3=8 \qquad 3^2=9$', size=60, gap=50)),
        "Two cubed is eight. Three squared is nine. Different.",
        A('2⁴ and 4² appear', T(r'$2^4=16 \qquad 4^2=16$', size=60, gap=50)),
        "But two to the fourth: sixteen. Four squared: sixteen. The same!",
        A("'Positive whole numbers: only 2 and 4' appears", T('Positive whole numbers: only $2$ and $4$', size=44)),
        D('Underline "Positive whole numbers"'),
        "Among positive whole numbers, two and four is the only pair of different numbers that works.",
        "With negative numbers or fractions, there are other pairs.",
        "So when the exam wants two and four, it says: positive integers. Just remember two and four.",
    ])

    # new slide 14 - adding copies of the same power (after "Splitting exponents")
    M.insert_slides(VID, 13, [dict(title='Adding equal powers', mode='concept', pre=[], script=[
        "One more thing about plus signs. There's no law for adding powers — but there IS a shortcut for copies.",
        A('2ⁿ + 2ⁿ = 2 · 2ⁿ = 2ⁿ⁺¹ appears', T(r'$2^n+2^n=2\cdot2^n=2^{n+1}$', size=54, gap=50)),
        "Two to the n, plus two to the n. Two copies of the same thing: two times two to the n.",
        D('Circle the "2 ·" and write "2 = 2¹" above it'),
        "And two is two to the one. Same base, multiplying: add the exponents. Two to the n plus one.",
        A('3ⁿ + 3ⁿ + 3ⁿ = 3ⁿ⁺¹ appears', T(r'$3^n+3^n+3^n=3\cdot3^n=3^{n+1}$', size=54, gap=50)),
        "Three copies of three to the n: three times three to the n. Three to the n plus one.",
        "Copies are counting. Count them, then write the count as a power of the base.",
        A('The trap appears: 2ⁿ + 2ⁿ ≠ 2²ⁿ', T(r'$2^n+2^n\ne2^{2n}$', size=54)),
        D('Cross out 2²ⁿ and write "n = 3: 8 + 8 = 16, but 2⁶ = 64"'),
        "The trap: two to the two n. Check with n equal to three. Eight plus eight is sixteen. Two to the sixth is sixty-four.",
        "Adding copies raises the exponent a little. It does not double it.",
    ])])

    # slide 15 - rules table: the question count changed
    _replace_say(M, VID, 15, "Ten core questions next. Match the right law to the right structure first. Speed comes later.",
                 "Core questions next. Match the right law to the right structure first. Speed comes later.")
    M.edit_lines(VID, 15, lambda ls: ls + [{'say': "After them, a short video on the exam traps."}])

    M.set_sidebar(VID, ['What a power is', 'Exponent 1 and 0', 'Negative exponents', 'Bases 1 and 0', 'Multiplying powers',
                        'Dividing powers', 'Power of a power', 'Same exponent', 'Negative bases', 'When aᵇ = 1', '2⁴ = 4²',
                        'Splitting exponents', 'Adding equal powers', 'The rules table'])
    for n, b in enumerate(M.video(VID)['beats'], 1):
        if n >= 2: b['active'] = n - 2


# ----------------------------------------------------------------------------------------------------------------
# 2. Memory card
# ----------------------------------------------------------------------------------------------------------------
def fix_card(M):
    c = M.card('powers')
    laws = c['tables'][0]['rows']
    laws.insert(len(laws) - 1, [r'$a^n+a^n=2a^n$', r'copies: $2^n+2^n=2^{n+1}$, $3^n+3^n+3^n=3^{n+1}$'])
    laws.append([r'$(-1)^n$', r'$1$ if $n$ is even, $-1$ if $n$ is odd'])
    c['tables'].insert(2, {'title': 'More powers to know', 'head': ['Power', 'Value'], 'rows': [
        [r'$2^9$, $2^{10}$', r'$512$, $1024$'],
        [r'$10^n$', r'$1$ followed by $n$ zeros: $10^3=1000$'],
        [r'$10^{-n}$', r'$n$ decimal places: $10^{-3}=0.001$'],
    ]})
    c['tables'].append({'title': 'Exam traps', 'head': ['Trap', 'Rule'], 'rows': [
        ['Between $0$ and $1$', r'a higher power is smaller: $0.3^2=0.09$, $0.2^3=0.008$'],
        ['Compare powers', r'same base or same exponent: $2^{30}=8^{10}<9^{10}=3^{20}$'],
        ['Zeros at the end', r'pair each $2$ with a $5$: $2^5\cdot5^3=4\cdot10^3$ (zeros = smaller exponent)'],
        ['Signs', r'odd power keeps the sign ($x^3<0\Rightarrow x<0$); even power is never negative'],
    ]})
    c['tips'] = [
        r'Among positive whole numbers, $2^4=4^2=16$ is the only pair of different numbers where swapping base and exponent gives the same number.',
        r'$(-3)^2=9$ but $-3^2=-9$: brackets decide the base.',
        r'Different bases? Rewrite with the smallest prime base: $8=2^3$, $9=3^2$. You will use this a lot later in the course.',
        r'Letters in the answers? Check with a number, for example $x=2$. If two choices give the same value, try another number.',
    ]


# ----------------------------------------------------------------------------------------------------------------
# 3. Existing questions: text, solutions, moves
# ----------------------------------------------------------------------------------------------------------------
def fix_questions(M):
    S = M.set_q
    S('q-218', expl=[r'Zero to any positive power is $0$. The exponent $\sqrt{2}$ is positive, therefore $0^{\sqrt{2}}=0$.',
                     r'Any number to the power of one is itself: $\left(\sqrt{2}\right)^1=\sqrt{2}$.',
                     r'The sum: $0+\sqrt{2}=\sqrt{2}$.'])
    S('q-219', expl=[r'One to any power is $1$: $1^{\sqrt{5}}=1$.',
                     r'Any nonzero number to the power of zero is $1$: $\left(\sqrt{5}\right)^0=1$.',
                     r'The sum: $1+1=2$.'])
    S('q-220', expl=[r'First the power in the brackets. An odd power keeps the minus: $(-4)^3=(-4)\cdot(-4)\cdot(-4)=-64$.',
                     r'The minus in front changes the sign: $-(-64)=64$.'])
    S('q-221', expl=[r'A negative exponent means "flip": $\left(\frac{2}{5}\right)^{-3}=\left(\frac{5}{2}\right)^3$.',
                     r'Cube the top and the bottom: $\frac{5^3}{2^3}=\frac{125}{8}$. The answer is positive.'])
    S('q-222', expl=[r'A negative exponent means "one over": $(-3)^{-4}=\frac{1}{(-3)^4}$.',
                     r'An even power removes the minus: $(-3)^4=81$.',
                     r'Therefore $(-3)^{-4}=\frac{1}{81}$.'])
    S('q-223', expl=[r'Same base, multiplying: add the exponents. $-7+12+(-3)=2$.',
                     r'$11^{-7}\cdot11^{12}\cdot11^{-3}=11^2=121$.'])
    S('q-224', expl=[r'A sum in the exponent splits into a product: $5^{x+2}=5^x\cdot5^2=25\cdot5^x$.',
                     r'Check with a number: $x=1$ gives $5^{3}=125$. The choices give $5+5=10$, $5\cdot5=25$, $25\cdot5=125$ and $25+5=30$. Only choice 3 gives $125$.'])
    S('q-225', expl=[r'Same base, dividing: subtract the exponents, top minus bottom.',
                     r'$\frac{13^9}{13^7}=13^{9-7}=13^2=169$.'])
    S('q-226', expl=[r'Write every factor as a power of $2$: $2=2^1$.',
                     r'Top: $2^1\cdot2^{-6}=2^{1+(-6)}=2^{-5}$.',
                     r'Divide: $\frac{2^{-5}}{2^{-10}}=2^{-5-(-10)}=2^{-5+10}=2^5=32$.',
                     r'The trap is choice 1: adding $-10$ instead of subtracting it gives $2^{-15}$.'])
    S('q-228', expl=[r'Same exponent, different bases: put them under one exponent.',
                     r'$2^4\cdot5^4=(2\cdot5)^4=10^4=10{,}000$.'])
    S('q-229', expl=[r'Same exponent on the top and the bottom: divide the bases first.',
                     r'$\frac{6^4}{2^4}=\left(\frac{6}{2}\right)^4=3^4=81$.'])
    S('q-230', expl=[r'Same exponent on the top and the bottom: divide the bases first.',
                     r'$\frac{5^3}{15^3}=\left(\frac{5}{15}\right)^3=\left(\frac{1}{3}\right)^3=\frac{1}{27}$.'])
    S('q-231', expl=[r'$a^b=1$ in three cases: $a=1$ (any $b$); $a=-1$ ($b$ an even whole number); $b=0$ (any $a\ne0$).',
                     r'Choice 2, $b=7$: possible, for example $1^7=1$.',
                     r'Choice 3, $b=0$: possible, for example $5^0=1$.',
                     r'Choice 4, $a=-1$: possible, for example $(-1)^2=1$.',
                     r'Choice 1, $a=0$: not possible. Zero to a positive power is $0$, and zero to the power of zero or of a negative number is not defined.'])
    S('q-232', stem='Given: $a$ and $b$ are positive integers, and\n' + r'$\begin{cases} a<b \\ a^b=b^a \end{cases}$' + '\n$a+b=?$',
      expl=[r'Among positive whole numbers, the only pair of different numbers with $a^b=b^a$ is $2$ and $4$: $2^4=16=4^2$.',
            r'$a<b$, therefore $a=2$ and $b=4$.',
            r'$a+b=2+4=6$.'])
    S('alg-extra-exponent-extra-3', stem=r'Given: $3^{x+1}=3^{4}$.' + '\n$x=?$', choices=['$9$', '$3$', '$2$', '$4$'],
      expl=[r'Same base on both sides, therefore the exponents are equal: $x+1=4$.', r'$x=3$.'])
    S('alg-extra-exponent-extra-4', stem=r'$2^{-3}+2^{-2}=?$',
      expl=[r'A negative exponent means "one over": $2^{-3}=\frac{1}{8}$ and $2^{-2}=\frac{1}{4}$.',
            r'Common denominator $8$: $\frac{1}{8}+\frac{2}{8}=\frac{3}{8}$.'])
    S('alg-extra-exponent-extra-5', stem=r'Given: $x\ne0$.' + '\n' + r'$\frac{(2x)^3}{4x^2}=?$',
      expl=[r'Same exponent over a product: $(2x)^3=2^3x^3=8x^3$.',
            r'Divide the numbers and the powers separately: $\frac{8x^3}{4x^2}=\frac{8}{4}\cdot x^{3-2}=2x$.'])
    S('alg-extra-exponent-extra-6', stem='Which of the following is true?',
      choices=[r'$2^{10}>4^{4}$', r'$2^{10}=4^{4}$', r'$2^{10}<4^{4}$', r'$2^{10}=2\cdot4^{4}$'], correct=1,
      expl=[r'Make the bases the same: $4^4=\left(2^2\right)^4=2^8$.',
            r'Same base, bigger exponent, bigger number: $2^{10}>2^8$. Choice 1 is true.',
            r'Choice 4 is false: $2\cdot4^4=2\cdot2^8=2^9$, not $2^{10}$.'])

    # used before taught (fractional exponents, roots) -> T9 practice; near-duplicate of q-225 removed
    M.set_q('q-227', expl=[r'A power of a power: multiply the exponents. $3\cdot\frac{2}{3}=2$.',
                           r'$\left(7^3\right)^{\frac{2}{3}}=7^2=49$.'])
    M.set_q('alg-extra-exponent-extra-2', stem=r'$27^{\frac{2}{3}}=?$', choices=['$27$', '$9$', '$3$', '$6$'],
            expl=[r'$27=3^3$, therefore $27^{\frac{2}{3}}=\left(3^3\right)^{\frac{2}{3}}=3^{3\cdot\frac{2}{3}}=3^2=9$.'])
    M.set_q('alg-extra-exponent-extra-7', stem=r'$\sqrt{50}+\sqrt{8}=?$',
            expl=[r'Take out the square factors: $\sqrt{50}=\sqrt{25\cdot2}=5\sqrt{2}$ and $\sqrt{8}=\sqrt{4\cdot2}=2\sqrt{2}$.',
                  r'Add like roots: $5\sqrt{2}+2\sqrt{2}=7\sqrt{2}$.'])
    for qid in ('q-227', 'alg-extra-exponent-extra-2', 'alg-extra-exponent-extra-7'):
        flow = M.D['flow']
        for f in [f for f in flow if f['ref'] == qid]:          # unplace() would drop the question data - move by hand
            flow.remove(f); sec = M.sections[f['section']]
            if f['id'] in sec['items']: sec['items'].remove(f['id'])
            sec['questionCount'] = sum(1 for g in flow if g['section'] == f['section'] and g['type'] == 'question')
        M.q(qid)['topic'] = 9
        M.place_q(qid, T9_PRACTICE)
    M.unplace('alg-extra-exponent-extra-1')      # 2^6/2^3: same as core q-225

    # q-231 needs a solution video -> it becomes a guided question in the core section, right after q-226
    flow = M.D['flow']
    for f in [f for f in flow if f['ref'] == 'q-231']:
        flow.remove(f); sec = M.sections[f['section']]
        if f['id'] in sec['items']: sec['items'].remove(f['id'])
        sec['questionCount'] = sum(1 for g in flow if g['section'] == f['section'] and g['type'] == 'question')
    M.place_q('q-231', CORE, after='q-226')


# ----------------------------------------------------------------------------------------------------------------
# 4. Solution videos
# ----------------------------------------------------------------------------------------------------------------
SIDEBAR = ['Question %d' % k for k in range(1, 9)]


def solve(M, qid, intro, slides):
    n = M.next_question_number(TOPIC)
    out = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        out.append(dict(mode='question', active=n - 1, title=title, pre=[Q(qid)], script=script))
    M.new_video('solve-' + qid, TOPIC, SOLVE_TITLE, SIDEBAR, out, M.section_of(qid), kind='solution', qid=qid)


def solution_videos_existing(M):
    solve(M, 'q-224', ["A letter in the exponent — and letters in the answers.", "Two ways to be sure."], [
        ('Method 1 · Split the exponent', [
            "A plus in the exponent. Split it into a product.",
            D('Write "5ˣ⁺² = 5ˣ · 5²"'),
            "Five to the x, times five squared.",
            D('Write "= 25 · 5ˣ"'),
            "Twenty-five times five to the x.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Method 2 · Check with a number', [
            "Not sure about the rule? Pick an easy x. Say x equals one.",
            D('Write "x = 1: 5³ = 125"'),
            "Five cubed: a hundred twenty-five.",
            "Now put x equals one into every choice.",
            D('Write "(1) 5 + 5 = 10   (2) 5 · 5 = 25   (3) 25 · 5 = 125   (4) 25 + 5 = 30"'),
            "Only choice three gives a hundred twenty-five.",
            D('Circle choice 3'),
            "Choice three. Same answer, no rule needed.",
        ]),
    ])
    solve(M, 'q-226', ["Negative exponents on the top and the bottom.", "Here's where the minus signs bite."], [
        ('One base, then the laws', [
            "Everything is a power of two. Even the lonely two: it's two to the one.",
            D('Write "2 = 2¹"'),
            "Top: two to the one times two to the minus six. Multiplying: add the exponents.",
            D('Write "2¹ · 2⁻⁶ = 2¹⁺⁽⁻⁶⁾ = 2⁻⁵"'),
            "One plus minus six: minus five.",
            "Now divide by two to the minus ten. Dividing: subtract. Top minus bottom.",
            D('Write "2⁻⁵⁻⁽⁻¹⁰⁾ = 2⁻⁵⁺¹⁰ = 2⁵"'),
            "Here's the trap. Minus five, minus minus ten. Two minuses make a plus: minus five plus ten. Five.",
            D('Write "2⁵ = 32"'),
            "Two to the fifth: thirty-two.",
            D('Circle choice 3'),
            "Choice three.",
            "Choice one, two to the minus fifteen? That's what you get if you add the minus ten instead of subtracting it.",
        ]),
    ])
    solve(M, 'q-231', ['"Not possible" — so test every choice.', "Our three options from the lesson do the work."], [
        ('Test each choice', [
            "When is a to the b equal to one? Three options.",
            D('Write "a = 1 (any b)   ·   a = −1 (b even)   ·   b = 0 (a ≠ 0)"'),
            "Choice two: b equals seven. Take a equals one. One to the seventh is one. Possible.",
            D('Write "✓" next to choice 2'),
            "Choice three: b equals zero. Any a that is not zero works. Possible.",
            D('Write "✓" next to choice 3'),
            "Choice four: a equals minus one. Take b equals two. Minus one squared is one. Possible.",
            D('Write "✓" next to choice 4'),
            "Choice one: a equals zero. Zero to a positive power is zero. Zero to the zero, or to a negative power, is not defined.",
            "It can never be one.",
            D('Circle choice 1'),
            "Choice one.",
        ]),
    ])


# ----------------------------------------------------------------------------------------------------------------
# 5. New lesson video: exam traps
# ----------------------------------------------------------------------------------------------------------------
def traps_video(M):
    sb = ['Between 0 and 1', 'Compare powers', 'Counting zeros', 'Signs with letters', 'Check with a number']
    slides = [
        dict(mode='title', title='Exponent Traps', script=[
            "The laws are done. Now the traps the exam loves.",
            "Five short ideas. Questions on each one come right after this video.",
        ]),
        dict(mode='concept', active=0, title='Between 0 and 1', pre=[], script=[
            "Most people think a power makes a number bigger. Not always.",
            A('0.5² = 0.25 appears', T(r'$0.5^2=0.25$', size=58, gap=40)),
            "Zero point five squared is zero point two five. Smaller! Half of a half is a quarter.",
            A('Powers of one half appear', T(r'$\left(\frac{1}{2}\right)^1=\frac{1}{2} \qquad \left(\frac{1}{2}\right)^2=\frac{1}{4} \qquad \left(\frac{1}{2}\right)^3=\frac{1}{8}$', size=48, gap=40)),
            "Each extra power: smaller again.",
            A('Decimal powers appear: 0.2³ = 0.008 · 0.3² = 0.09', T(r'$0.2^3=0.008 \qquad 0.3^2=0.09$', size=54, gap=40)),
            D('Write "3 places" under 0.008 and "2 places" under 0.09'),
            "Decimals: multiply the digits, then count the decimal places.",
            "Two times two times two is eight. One place, three times: three places. Zero point zero zero eight.",
            "Zero point three squared: nine, with two places. Zero point zero nine — not zero point nine.",
            A('The rule appears: 0 < x < 1 → x³ < x² < x', T(r'$0<x<1:\quad x^3<x^2<x$', size=54)),
            "So for a number between zero and one: the higher the power, the smaller the number.",
            "Above one it's the opposite: the higher the power, the bigger the number.",
        ]),
        dict(mode='concept', active=1, title='Compare powers', pre=[], script=[
            "Which is bigger? There are two ways.",
            A('2¹⁰ ? 4⁴ appears', T(r'$2^{10}\quad ? \quad 4^4$', size=54, gap=30)),
            "Way one: make the bases the same. Four is two squared.",
            A('4⁴ = (2²)⁴ = 2⁸ appears', T(r'$4^4=\left(2^2\right)^4=2^8$', size=50, gap=40)),
            D('Write "2¹⁰ > 2⁸"'),
            "Now both are powers of two. Same base, bigger than one: the bigger exponent wins.",
            A('2³⁰ ? 3²⁰ appears', T(r'$2^{30}\quad ? \quad 3^{20}$', size=54, gap=30)),
            "Way two: make the exponents the same. Thirty and twenty are both multiples of ten.",
            A('8¹⁰ and 9¹⁰ appear', T(r'$\left(2^3\right)^{10}=8^{10} \qquad \left(3^2\right)^{10}=9^{10}$', size=50, gap=40)),
            D('Write "2³⁰ < 3²⁰"'),
            "Eight to the tenth against nine to the tenth. Same exponent: the bigger base wins.",
            "Three to the twentieth is bigger — with the smaller exponent!",
            A('3ˣ⁺¹ = 3⁴ appears', T(r'$3^{x+1}=3^4 \;\Rightarrow\; x+1=4$', size=50)),
            D('Write "x = 3"'),
            "Same idea in equations. The same positive base, not one, on both sides? Then the exponents are equal. x is three.",
            "Later in the course you'll do this all the time: write every base as a power of the smallest prime.",
        ]),
        dict(mode='concept', active=2, title='Counting zeros', pre=[], script=[
            "Two times five is ten. That's where the zeros at the end of a number come from.",
            A('2⁴ · 5⁴ = 10⁴ appears', T(r'$2^4\cdot5^4=(2\cdot5)^4=10^4$', size=54, gap=50)),
            "Same exponent: pair them up. Ten to the fourth. Ten thousand — four zeros.",
            A('2⁵ · 5³ appears', T(r'$2^5\cdot5^3$', size=58, gap=30)),
            "Uneven exponents? Five twos, three fives. Make as many pairs as you can: three pairs.",
            A('= 2² · (2 · 5)³ = 4 · 10³ = 4000 appears', T(r'$=2^2\cdot(2\cdot5)^3=4\cdot10^3=4000$', size=52)),
            "Three tens, and two twos left over. Four thousand.",
            D('Circle the exponent 3'),
            "The number of zeros at the end is the smaller exponent. The leftovers make the digits in front.",
        ]),
        dict(mode='concept', active=3, title='Signs with letters', pre=[], script=[
            "Letters hide the sign. Powers can tell you — or not.",
            A('Odd power keeps the sign appears', T(r'Odd power keeps the sign: $x^3<0\;\Rightarrow\;x<0$', size=46, gap=50)),
            "An odd power keeps the sign. x cubed is negative, therefore x is negative.",
            A('Even power is never negative appears', T(r'Even power is never negative: $x^2\ge0$', size=46, gap=50)),
            "An even power is never negative. If x squared is positive, you only know that x is not zero.",
            "x could be three. x could be minus three.",
            A('(−x)² = x² and −x² ≤ 0 appear', T(r'$(-x)^2=x^2 \qquad -x^2\le0$', size=54)),
            "Brackets again. Minus x, in brackets, squared: the same as x squared.",
            "Minus x squared: first the square, then the minus. It is never positive.",
            "Say it to yourself: odd keeps the sign, even hides it.",
        ]),
        dict(mode='concept', active=4, title='Check with a number', pre=[], script=[
            "Letters in the answers? You can check with a number.",
            A('3ˣ⁺¹ = ? appears', T(r'$3^{x+1}=\;?$', size=58, gap=40)),
            "The law says: three times three to the x. But let's check it.",
            A('x = 1: 3² = 9 appears', T(r'$x=1:\quad 3^{2}=9$', size=54, gap=40)),
            "Pick an easy x. x equals one. Three squared is nine.",
            A('The choices with x = 1 appear', T(r'$3\cdot3^x=9\ \checkmark \qquad 3+3^x=6 \qquad 3^x+1=4$', size=48)),
            "Put the same x into each choice. Only three times three to the x gives nine.",
            "Two choices give the same number? Pick another x, and test only those two.",
            "The number must also fit the question. If it says x is between zero and one, pick one half.",
        ]),
    ]
    M.new_video('r26-t08-traps', TOPIC, 'Exponent Traps', sb, slides, CORE, after='solve-q-231')


# ----------------------------------------------------------------------------------------------------------------
# 6. New guided questions (with solution videos) and practice
# ----------------------------------------------------------------------------------------------------------------
def qid(k): return 'q-r26-t08-%02d' % k


def guided(M):
    after = 'r26-t08-traps'
    G = [
        (1, r'$2^{n}+2^{n}+2^{n}+2^{n}=?$', [r'$2^{4n}$', r'$8^{n}$', r'$2^{n+2}$', r'$2^{n+4}$'], 3,
         [r'Four copies of the same power: $2^n+2^n+2^n+2^n=4\cdot2^n$.',
          r'Write $4$ as a power of $2$: $4\cdot2^n=2^2\cdot2^n=2^{n+2}$.',
          r'Check with $n=2$: $4+4+4+4=16$ and $2^{2+2}=16$. Choice 2 gives $8^2=64$.']),
        (2, r'Given: $0<x<1$.' + '\nWhich of the following is the smallest?', [r'$x$', r'$x^{2}$', r'$x^{3}$', r'$x^{-2}$'], 3,
         [r'Plug in a number between $0$ and $1$: $x=\frac{1}{2}$.',
          r'$x=\frac{1}{2}$, $x^2=\frac{1}{4}$, $x^3=\frac{1}{8}$, $x^{-2}=2^2=4$.',
          r'The smallest is $x^3$. A negative exponent does not make the number negative: $x^{-2}$ is the largest here.']),
        (3, 'Which of the following is the largest?', [r'$2^{40}$', r'$3^{30}$', r'$5^{20}$', r'$10^{10}$'], 2,
         [r'Make the exponents the same. All the exponents are multiples of $10$.',
          r'$2^{40}=\left(2^4\right)^{10}=16^{10}$, $3^{30}=\left(3^3\right)^{10}=27^{10}$, $5^{20}=\left(5^2\right)^{10}=25^{10}$, and $10^{10}$.',
          r'Same exponent: the biggest base wins. $27^{10}=3^{30}$ is the largest.']),
        (4, r'How many zeros are there at the end of the number $2^{7}\cdot5^{4}$?', [r'$3$', r'$4$', r'$7$', r'$11$'], 2,
         [r'Pair each $5$ with a $2$. There are $4$ fives, therefore $4$ pairs: $2^7\cdot5^4=2^3\cdot(2\cdot5)^4=8\cdot10^4$.',
          r'$8\cdot10^4=80{,}000$: $4$ zeros at the end.']),
        (5, r'Given: $x^{3}y^{2}<0$.' + '\nWhich of the following is necessarily true?', [r'$x<0$', r'$y<0$', r'$xy<0$', r'$x^{2}y>0$'], 1,
         [r'$y^2$ is an even power, therefore $y^2\ge0$. It is not $0$, because then the product would be $0$. Therefore $y^2>0$.',
          r'Therefore $x^3<0$. An odd power keeps the sign: $x<0$. Choice 1 is necessarily true.',
          r'The sign of $y$ is unknown. For example, $x=-1$, $y=1$ and $x=-1$, $y=-1$ both fit. Therefore choices 2, 3 and 4 are not necessarily true.']),
    ]
    for k, stem, ch, c, ex in G:
        M.new_q(qid(k), TOPIC, stem, ch, c, ex)
        M.place_q(qid(k), CORE, after=after)
        after = qid(k)


def guided_videos(M):
    solve(M, qid(1), ["Four copies of the same power.", "Adding copies is counting."], [
        ('Count the copies', [
            "Four copies of two to the n. Adding copies is counting them.",
            D('Write "= 4 · 2ⁿ"'),
            "Four times two to the n. Now write four as a power of two.",
            D('Write "= 2² · 2ⁿ = 2ⁿ⁺²"'),
            "Two squared times two to the n. Same base, multiplying: add the exponents. n plus two.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Check with a number', [
            "Let's check. n equals one: two plus two plus two plus two is eight.",
            D('Write "n = 1: 8   (1) 16   (2) 8   (3) 8   (4) 32"'),
            "Choice two AND choice three give eight. Two choices match — so try another n.",
            D('Write "n = 2: 16   (2) 64   (3) 16"'),
            "n equals two: the sum is sixteen. Eight squared is sixty-four. Two to the fourth is sixteen.",
            "Choice three. Choice two added the bases — bases never add.",
        ]),
    ])
    solve(M, qid(2), ["A number between zero and one.", "Pick one, and look."], [
        ('Plug in one half', [
            "x is between zero and one. Pick an easy number there: one half.",
            D('Write "x = ½"'),
            D('Write "(1) ½   (2) ¼   (3) ⅛   (4) 2² = 4"'),
            "One half, one quarter, one eighth.",
            "x to the minus two: flip it. Two squared. Four — not negative! It's the biggest one here.",
            "The smallest is one eighth.",
            D('Circle choice 3'),
            "Choice three. Between zero and one, each extra power makes the number smaller.",
        ]),
    ])
    solve(M, qid(3), ["Four powers. Different bases, different exponents.", "Make one of them the same."], [
        ('Same exponent', [
            "The exponents are forty, thirty, twenty, ten. All multiples of ten. Make every exponent ten.",
            D('Write "2⁴⁰ = (2⁴)¹⁰ = 16¹⁰"'),
            D('Write "3³⁰ = (3³)¹⁰ = 27¹⁰"'),
            D('Write "5²⁰ = (5²)¹⁰ = 25¹⁰"'),
            "Ten to the tenth stays as it is.",
            "Now the exponents match. The biggest base wins: twenty-seven.",
            D('Circle choice 2'),
            "Choice two.",
            "Notice: the biggest exponent, forty, did not win. The biggest base, ten, did not win either.",
        ]),
    ])
    solve(M, qid(4), ["How many zeros at the end?", "Every zero is a two times a five."], [
        ('Pair twos with fives', [
            "Seven twos, four fives. Every two with a five makes a ten.",
            D('Write "2⁷ · 5⁴ = 2³ · 2⁴ · 5⁴"'),
            "Split off as many twos as there are fives: four.",
            D('Write "= 2³ · (2 · 5)⁴ = 8 · 10⁴ = 80,000"'),
            "Eight, followed by four zeros.",
            D('Circle choice 2'),
            "Four zeros. Choice two.",
            "The trap: seven, the bigger exponent. The extra twos only make the eight.",
        ]),
    ])
    solve(M, qid(5), ["A product with powers is negative.", "Odd keeps the sign, even hides it."], [
        ('Odd and even powers', [
            "y squared: an even power. It is never negative.",
            "And it's not zero — then the whole product would be zero.",
            D('Write "y² > 0"'),
            "So the minus comes from x cubed.",
            D('Write "x³ < 0 → x < 0"'),
            "An odd power keeps the sign. x cubed is negative, therefore x is negative.",
            D('Circle choice 1'),
            "Choice one — necessarily true.",
            "The others? y can be positive or negative. So y less than zero, and x y less than zero, are only possible.",
            "x squared times y has the sign of y. Also only possible.",
        ]),
    ])


PRACTICE_Q = [
    # (key, stem, choices, correct, explanation)
    ('copies-3', r'$3^{n}+3^{n}+3^{n}=?$', [r'$9^{n}$', r'$3^{3n}$', r'$3^{n+1}$', r'$3^{n+3}$'], 3,
     [r'Three copies: $3^n+3^n+3^n=3\cdot3^n=3^1\cdot3^n=3^{n+1}$.']),
    ('copies-5', r'$\frac{5^{12}+5^{12}+5^{12}+5^{12}+5^{12}}{5^{10}}=?$', [r'$25$', r'$125$', r'$625$', r'$5^{50}$'], 2,
     [r'Five copies on the top: $5\cdot5^{12}=5^{13}$.', r'$\frac{5^{13}}{5^{10}}=5^{3}=125$.']),
    ('copies-eq', r'Given: $2^{n+1}+2^{n+1}=32$.' + '\n$n=?$', [r'$2$', r'$3$', r'$4$', r'$5$'], 2,
     [r'Two copies: $2^{n+1}+2^{n+1}=2\cdot2^{n+1}=2^{n+2}$.', r'$32=2^5$, therefore $n+2=5$ and $n=3$.',
      r'Check: $2^4+2^4=16+16=32$.']),
    ('dec-sq', r'$0.3^{2}=?$', [r'$0.9$', r'$0.09$', r'$0.6$', r'$0.009$'], 2,
     [r'Multiply the digits: $3\cdot3=9$. One decimal place, two times: two places.', r'$0.3^2=0.09$.']),
    ('dec-cube', r'$0.2^{3}\cdot10^{4}=?$', [r'$8$', r'$80$', r'$800$', r'$0.8$'], 2,
     [r'$0.2^3$: $2\cdot2\cdot2=8$, with three decimal places: $0.008$.',
      r'Multiplying by $10^4$ moves the decimal point four places to the right: $0.008\cdot10{,}000=80$.']),
    ('neg-01', r'Given: $-1<x<0$.' + '\nWhich of the following is the largest?', [r'$x$', r'$x^{2}$', r'$x^{3}$', r'$x^{4}$'], 2,
     [r'Plug in $x=-\frac{1}{2}$: $x=-\frac{1}{2}$, $x^2=\frac{1}{4}$, $x^3=-\frac{1}{8}$, $x^4=\frac{1}{16}$.',
      r'Odd powers are negative, even powers are positive. Between $0$ and $1$, a higher power is smaller: $\frac{1}{4}>\frac{1}{16}$.',
      r'The largest is $x^2$.']),
    ('cmp-base', 'Which of the following is the largest?', [r'$16^{2}$', r'$8^{3}$', r'$2^{12}$', r'$4^{5}$'], 3,
     [r'Write every base as a power of $2$: $16^2=2^8$, $8^3=2^9$, $2^{12}$, $4^5=2^{10}$.',
      r'Same base: the biggest exponent wins. $2^{12}$ is the largest.']),
    ('cmp-order', 'Which of the following is true?',
     [r'$2^{50}<3^{30}<5^{20}$', r'$5^{20}<3^{30}<2^{50}$', r'$3^{30}<5^{20}<2^{50}$', r'$5^{20}<2^{50}<3^{30}$'], 2,
     [r'Make every exponent $10$: $2^{50}=\left(2^5\right)^{10}=32^{10}$, $3^{30}=\left(3^3\right)^{10}=27^{10}$, $5^{20}=\left(5^2\right)^{10}=25^{10}$.',
      r'Same exponent: compare the bases. $25<27<32$, therefore $5^{20}<3^{30}<2^{50}$.']),
    ('cmp-eq', r'Given: $4^{x}=8^{4}$.' + '\n$x=?$', [r'$2$', r'$3$', r'$6$', r'$12$'], 3,
     [r'Write both sides with base $2$: $4^x=\left(2^2\right)^x=2^{2x}$ and $8^4=\left(2^3\right)^4=2^{12}$.',
      r'Same base, therefore $2x=12$ and $x=6$.']),
    ('zeros-eq', r'$2^{3}\cdot5^{6}=?$', [r'$1{,}000{,}000$', r'$1{,}000$', r'$125{,}000$', r'$15{,}625$'], 3,
     [r'Three twos, therefore three pairs: $2^3\cdot5^6=(2\cdot5)^3\cdot5^3=10^3\cdot125$.', r'$125\cdot1000=125{,}000$.']),
    ('digits', r'How many digits does the number $4^{5}\cdot5^{8}$ have?', [r'$8$', r'$9$', r'$10$', r'$13$'], 2,
     [r'$4^5=\left(2^2\right)^5=2^{10}$.', r'$2^{10}\cdot5^8=2^2\cdot(2\cdot5)^8=4\cdot10^8=400{,}000{,}000$.',
      r'A $4$ followed by $8$ zeros: $9$ digits.']),
    ('sign-odd', r'Given: $x^{5}<0$.' + '\nWhich of the following is necessarily true?', [r'$x^{2}<0$', r'$x<0$', r'$x^{4}<0$', r'$-x<0$'], 2,
     [r'An odd power keeps the sign: $x^5<0$, therefore $x<0$.',
      r'$x^2$ and $x^4$ are even powers, never negative. $-x$ is positive when $x<0$.']),
    ('sign-neg', r'Given: $x\ne0$.' + '\nWhich of the following is necessarily negative?', [r'$(-x)^{2}$', r'$-x^{2}$', r'$-x^{3}$', r'$(-x)^{3}$'], 2,
     [r'$-x^2$: first the square, $x^2>0$, then the minus. Always negative.',
      r'$(-x)^2=x^2>0$. $-x^3$ and $(-x)^3$ are equal, and their sign depends on $x$: for $x=-1$ they are $1$, for $x=1$ they are $-1$.']),
    ('sign-2', r'Given: $x^{3}y^{5}<0$.' + '\nWhich of the following is necessarily true?', [r'$x<0$', r'$y<0$', r'$xy<0$', r'$x^{2}y<0$'], 3,
     [r'Odd powers keep the sign: $x^3$ has the sign of $x$, and $y^5$ has the sign of $y$.',
      r'Therefore $x^3y^5<0$ means $x$ and $y$ have opposite signs: $xy<0$.',
      r'Which one is negative is unknown: $x=-1$, $y=1$ and $x=1$, $y=-1$ both fit. Therefore choices 1, 2 and 4 are not necessarily true.']),
    ('ab1', r'Given: $x$ is an integer, and $(x-2)^{x+3}=1$.' + '\nHow many values can $x$ have?', [r'$1$', r'$2$', r'$3$', r'$4$'], 3,
     [r'Check the three options for $a^b=1$.',
      r'Base $1$: $x-2=1$, $x=3$. Check: $1^6=1$.',
      r'Base $-1$ with an even exponent: $x-2=-1$, $x=1$. The exponent is $4$, even. Check: $(-1)^4=1$.',
      r'Exponent $0$ with a base that is not $0$: $x+3=0$, $x=-3$. The base is $-5$. Check: $(-5)^0=1$.',
      r'Three values: $3$, $1$ and $-3$.']),
    ('mix-1', r'$\frac{\left(2^{3}\right)^{2}\cdot2^{-4}}{2^{2}}=?$', [r'$\frac{1}{2}$', r'$1$', r'$16$', r'$64$'], 2,
     [r'Power of a power: $\left(2^3\right)^2=2^6$.', r'Multiplying: $2^6\cdot2^{-4}=2^{2}$.', r'Dividing: $\frac{2^2}{2^2}=2^0=1$.']),
    ('mix-2', r'$\frac{6^{5}}{2^{5}\cdot3^{3}}=?$', [r'$3$', r'$9$', r'$27$', r'$\frac{1}{9}$'], 2,
     [r'Same exponent: $6^5=(2\cdot3)^5=2^5\cdot3^5$.', r'$\frac{2^5\cdot3^5}{2^5\cdot3^3}=3^{5-3}=3^2=9$.']),
    ('mix-3', r'$\frac{9^{4}\cdot27^{2}}{3^{12}}=?$', [r'$1$', r'$3$', r'$9$', r'$27$'], 3,
     [r'Write every base as a power of $3$: $9^4=\left(3^2\right)^4=3^8$ and $27^2=\left(3^3\right)^2=3^6$.',
      r'$\frac{3^8\cdot3^6}{3^{12}}=\frac{3^{14}}{3^{12}}=3^2=9$.']),
]


def practice(M):
    ids = {}
    k = 6
    for key, stem, ch, c, ex in PRACTICE_Q:
        ids[key] = qid(k)
        M.new_q(qid(k), TOPIC, stem, ch, c, ex)
        M.place_q(qid(k), PRACTICE)
        k += 1
    order = ['q-228', 'q-229', 'q-230', 'alg-extra-exponent-extra-4', 'alg-extra-exponent-extra-5', 'alg-extra-exponent-extra-6',
             'alg-extra-exponent-extra-3', ids['dec-sq'], ids['copies-3'], ids['sign-odd'], ids['mix-1'], ids['mix-2'],
             ids['zeros-eq'], ids['dec-cube'], ids['cmp-base'], ids['sign-neg'], ids['copies-5'], ids['cmp-eq'], ids['mix-3'],
             ids['digits'], ids['copies-eq'], ids['neg-01'], ids['cmp-order'], ids['sign-2'], 'q-232', ids['ab1']]
    M.practice_order(PRACTICE, order)


def apply(M):
    # section title said "ten core questions"; no API call for it - set it directly
    M.sections[CORE]['title'] = 'Rules, memory table, and core questions'
    fix_lesson(M)
    fix_card(M)
    fix_questions(M)
    solution_videos_existing(M)     # Question 1-3: q-224, q-226, q-231
    traps_video(M)
    guided(M)
    guided_videos(M)                # Question 4-8
    practice(M)
