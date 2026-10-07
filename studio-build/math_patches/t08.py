"""Topic 8 - Exponent Laws, Fundamentals. Course review 2026-09 fixes (see t08_CHANGES.md)."""
from math_api import T, H, A, D, Q, rich_plain

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

    # slide 5 (bases 1 and 0) - now after negative exponents; its original line
    # "A negative exponent means dividing by zero — undefined. Zero to the zero? ..." is kept as it is (pass 2)

    # slide 7 (dividing powers) - pass 2: the original proof 5³/5³ = 5⁰ = 1 comes back as a second way,
    # here where the division law is taught
    b7 = M.slide(VID, 7)
    b7['items'].append({'k': 't', 't': r'$\frac{5^3}{5^3}$', 'size': 62})
    M.edit_lines(VID, 7, lambda ls: ls + [
        {'say': "Now a second way to see why five to the zero is one."},
        {'appear': len(b7['items']) - 1, 'label': '5³ / 5³ appears'},
        {'draw': 'Write "= 1"; then write "= 5³⁻³ = 5⁰"'},
        {'say': 'A number over itself is one. But subtracting the exponents gives five to the zero. So five to the zero has to be one.'}])

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
    # pass 2: the original question and choices are restored (text clean-up only)
    S('alg-extra-exponent-extra-6', stem=r'Which is greater: $2^{10}$ or $4^{4}$?',
      choices=['It cannot be determined from the information given.', 'The first power', 'The second power', 'They are equal'], correct=2,
      expl=[r'Make the bases the same: $4^4=\left(2^2\right)^4=2^8$.',
            r'Same base, bigger exponent, bigger number: $2^{10}>2^8$. The first power is greater.'])
    S('alg-extra-exponent-extra-1', stem=r'$\frac{2^{6}}{2^{3}}=?$', choices=['$8$', '$2$', '$4$', '$16$'], correct=1,
      expl=[r'Same base, dividing: subtract the exponents, top minus bottom.',
            r'$\frac{2^6}{2^3}=2^{6-3}=2^3=8$.'])

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
SIDEBAR = ['Question %d' % k for k in range(1, 7)]   # 6 T8 guided questions; apply() adds the ones moved in from T5


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
    sb = ['Between 0 and 1', 'Compare powers', 'Signs with letters', 'Check with a number']
    slides = [
        dict(mode='title', title='Exponent Traps', script=[
            "The laws are done. Now the traps the exam loves.",
            "Four short ideas. Questions come right after this video.",
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
        dict(mode='concept', active=2, title='Signs with letters', pre=[], script=[
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
        dict(mode='concept', active=3, title='Check with a number', pre=[], script=[
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


# pass 2 (teacher-approved plan): ordering 2^50, 3^30, 5^20 (-13) and counting digits (-16) are removed
REMOVED_PRACTICE = {'cmp-order', 'digits'}


def practice(M):
    ids = {}
    k = 6
    for key, stem, ch, c, ex in PRACTICE_Q:
        ids[key] = qid(k)
        if key not in REMOVED_PRACTICE:      # pass 2: ids stay stable, removed items are simply not created
            M.new_q(qid(k), TOPIC, stem, ch, c, ex)
            M.place_q(qid(k), PRACTICE)
        k += 1
    order = ['alg-extra-exponent-extra-1', 'q-228', 'q-229', 'q-230', 'alg-extra-exponent-extra-4', 'alg-extra-exponent-extra-5', 'alg-extra-exponent-extra-6',
             'alg-extra-exponent-extra-3', ids['dec-sq'], ids['copies-3'], ids['sign-odd'], ids['mix-1'], ids['mix-2'],
             ids['zeros-eq'], ids['dec-cube'], ids['cmp-base'], ids['sign-neg'], ids['copies-5'], ids['cmp-eq'], ids['mix-3'],
             ids['copies-eq'], ids['neg-01'], ids['sign-2'], 'q-232', ids['ab1']]
    M.practice_order(PRACTICE, order)


def apply(M):
    # section title said "ten core questions"; no API call for it - set it directly
    M.sections[CORE]['title'] = 'Rules, memory table, and core questions'
    fix_lesson(M)
    fix_card(M)
    fix_questions(M)
    # guided questions moved in from Topic 5 (q-131, q-132) are numbered after the T8 ones: widen the sidebar
    global SIDEBAR
    moved = sum(1 for f in M.D['flow'] if f['topic'] == TOPIC and f['type'] == 'video'
                and M.D['videos'].get(f['ref'], {}).get('kind') == 'solution')
    SIDEBAR = ['Question %d' % k for k in range(1, 7 + moved)]
    solution_videos_existing(M)     # Question 1-3: q-224, q-226, q-231
    traps_video(M)
    guided(M)
    guided_videos(M)                # Question 4-6
    practice(M)
    summary(M)
    new_numbers(M)                  # 2026-10-02: not identical to the Hebrew course
    order_changes(M)


# ----------------------------------------------------------------------------------------------------------------
# 7. Pass 2: summary video right before the practice section
# ----------------------------------------------------------------------------------------------------------------
def summary(M):
    sb = ['Exponents 1, 0, −n', 'The three laws', 'Same exponent', 'Negative bases', 'When aᵇ = 1',
          'Split and count', 'Compare powers', 'Before you practice']
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice, a quick summary of the exponent laws.",
            "Everything you need — in two minutes.",
        ]),
        dict(mode='concept', active=0, title='Exponents 1, 0, −n', pre=[], script=[
            A('a¹ = a and a⁰ = 1 appear', T(r'$a^1=a \qquad a^0=1\quad(a\ne0)$', size=50, gap=50)),
            "Power of one: the number itself. Power of zero: one — for any number except zero.",
            A('a⁻ⁿ = 1/aⁿ appears', T(r'$a^{-n}=\frac{1}{a^n} \qquad \left(\frac{3}{4}\right)^{-2}=\left(\frac{4}{3}\right)^2$', size=50)),
            "A negative exponent means flip. It does NOT make the number negative.",
        ]),
        dict(mode='concept', active=1, title='The three laws', pre=[], script=[
            A('The three laws appear', T(r'$a^m\cdot a^n=a^{m+n} \qquad \frac{a^m}{a^n}=a^{m-n} \qquad \left(a^m\right)^n=a^{mn}$', size=44, gap=50)),
            "Same base. Multiply: add the exponents. Divide: subtract, top minus bottom. Power of a power: multiply.",
            A('The trap 2³ + 2⁴ ≠ 2⁷ appears', T(r'$2^3+2^4=24\ne2^7$', size=50)),
            "A plus sign has no law. Check for the same base AND a multiplication sign.",
        ]),
        dict(mode='concept', active=2, title='Same exponent', pre=[], script=[
            A('(ab)ⁿ = aⁿbⁿ appears', T(r'$(ab)^n=a^n b^n \qquad \left(\frac{a}{b}\right)^n=\frac{a^n}{b^n}$', size=50, gap=50)),
            "Different bases, same exponent? Put them under one exponent.",
            A('4³ · 25³ = 100³ appears', T(r'$4^3\cdot25^3=100^3 \qquad (a+b)^2\ne a^2+b^2$', size=50)),
            "Four cubed times twenty-five cubed: a hundred cubed. But never over a plus or a minus.",
        ]),
        dict(mode='concept', active=3, title='Negative bases', pre=[], script=[
            A('(−2)⁴, (−2)³ and −2⁴ appear', T(r'$(-2)^4=16 \qquad (-2)^3=-8 \qquad -2^4=-16$', size=48, gap=50)),
            "Even power: the minus disappears. Odd power: the minus stays.",
            "No brackets? The power comes first, then the minus.",
            A("'Odd keeps the sign, even hides it' appears", T(r'Odd keeps the sign: $x^3<0 \Rightarrow x<0$. Even: $x^2\ge0$', size=40)),
            "Odd keeps the sign. Even hides it.",
        ]),
        dict(mode='concept', active=4, title='When aᵇ = 1', pre=[], script=[
            A('The three options appear', T(r'$a^b=1$: $\ a=1$ · $\ a=-1$ ($b$ even whole) · $\ b=0$ ($a\ne0$)', size=40, gap=50)),
            "a to the b is one in three cases. Check all three.",
            A('2⁴ = 4² appears', T(r'$2^4=4^2=16$', size=50)),
            "And one special pair: two and four. Among positive whole numbers, it's the only one.",
        ]),
        dict(mode='concept', active=5, title='Split and count', pre=[], script=[
            A('3ⁿ⁺² = 9 · 3ⁿ appears', T(r'$3^{n+2}=3^n\cdot3^2=9\cdot3^n$', size=50, gap=50)),
            "A sum in the exponent splits into a product.",
            A('4ⁿ + 4ⁿ + 4ⁿ + 4ⁿ = 4ⁿ⁺¹ appears', T(r'$4^n+4^n+4^n+4^n=4\cdot4^n=4^{n+1} \qquad \ne 4^{4n}$', size=44)),
            "Copies of the same power? Count them, and write the count as a power of the base.",
        ]),
        dict(mode='concept', active=6, title='Compare powers', pre=[], script=[
            A('25³ = 5⁶ < 5⁸ appears', T(r'$25^3=\left(5^2\right)^3=5^6<5^8$', size=50, gap=50)),
            "To compare, make the bases the same — or the exponents the same.",
            A('0.4² = 0.16 appears', T(r'$0<x<1:\ x^3<x^2<x \qquad 0.4^2=0.16$', size=46)),
            "Between zero and one, a higher power is SMALLER.",
        ]),
        dict(mode='concept', active=7, title='Before you practice', pre=[], script=[
            "Before every question, ask yourself:",
            A("'Same base? Multiplying — or adding?' appears", T('Same base? Multiplying — or adding?', size=40)),
            A("'Is the minus in the base or in the exponent?' appears", T('Is the minus in the base or in the exponent?', size=40)),
            A("'Brackets: what exactly is the base?' appears", T('Brackets: what exactly is the base?', size=40)),
            A("'A number between 0 and 1?' appears", T('A number between $0$ and $1$?', size=40)),
            A("'Letters in the answers? Check with a number.' appears", T('Letters in the answers? Check with a number.', size=40)),
            "The classic traps: adding exponents across a plus sign, and reading minus two to the fourth as sixteen.",
            "Now go practice.",
        ]),
    ]
    M.new_video('r26-t08-summary', TOPIC, 'Exponent Laws: Summary', sb, slides, CORE)


# ----------------------------------------------------------------------------------------------------------------
# 8. 2026-10-02: new numbers - the English course is not identical to the Hebrew one (same ideas, same methods)
# ----------------------------------------------------------------------------------------------------------------
def _sub(M, vid, n, pairs):
    """Exact substring replacements on one slide: board items ('t'), item labels, spoken and drawn lines."""
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = False
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit = True
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit = True
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    M.touched_videos.add(vid)


def new_numbers(M):
    # recorded by the teacher with the old numbers - question and video stay exactly as recorded (nothing yet)
    RECORDED = set()

    def S(qid, **kw):
        if qid in RECORDED: return
        q = M.set_q(qid, **kw)
        # set_q keeps a pre-loaded stem in sync, but not a pre-loaded copy of the choices
        for v in M.D['videos'].values():
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])

    def video(qid, slides, intro=None, stem_title=False):
        if qid in RECORDED: return
        vid = 'solve-' + qid
        for n, x in slides.items():
            title, script = x if isinstance(x, tuple) else (None, x)
            M.set_slide(vid, n, title=title, script=script)
        if intro: _sub(M, vid, 1, intro)
        if stem_title:                    # the moved Topic 5 videos are titled with their question's stem
            v = M.video(vid); v['title'] = v['navLabel'] = rich_plain(M.q(qid)['stemRich'])

    # ---------------- lesson "Exponent Laws": the Hebrew lesson's own examples -> new examples, same points
    if 'exponents' not in RECORDED:
        M.set_slide(VID, 1, script=[
            "Exponents first — roots come right after them.",
            "We learn the laws, and then we solve real exam questions.",
            "Exponents appear all over the exam: in algebra, and even inside geometry questions.",
            "You need to use these laws quickly, without stopping to think. Let's build them step by step.",
        ])
        _sub(M, VID, 3, [(r'\left(\frac{3}{7}\right)^0', r'\left(\frac{4}{9}\right)^0'),
                         ('(−7)⁰ and (3/7)⁰ appear', '(−7)⁰ and (4/9)⁰ appear')])
        _sub(M, VID, 4, [(r'\left(\frac{2}{5}\right)^{-3}', r'\left(\frac{5}{2}\right)^{-2}'),
                         ('(2/5)⁻³ appears', '(5/2)⁻² appears'),
                         ('Write "= (5/2)³ = 125/8"', 'Write "= (2/5)² = 4/25"'),
                         ('Five cubed over two cubed: a hundred twenty-five eighths. Positive.',
                          'Two squared over five squared: four twenty-fifths. Positive.')])
        _sub(M, VID, 5, [('One to any power is one. One times one times one — a million times — still one.',
                          'One to any power is one. Multiply one by itself as many times as you like — the answer stays one.')])
        _sub(M, VID, 9, [(r'$(2\cdot3)^3$', r'$(4\cdot5)^2$'),
                         ('(2·3)³ appears', '(4·5)² appears'),
                         ('Write "= 2³ · 3³ = 8 · 27 = 216"', 'Write "= 4² · 5² = 16 · 25 = 400"'),
                         ('Why? Two cubed times three cubed is three twos and three threes. Multiplication lets us reorder them into three pairs of two times three.',
                          'Why? Four squared times five squared is two fours and two fives. Multiplication lets us reorder them into two pairs of four times five.'),
                         ('Two times three, cubed — or two cubed times three cubed. Same thing: two hundred sixteen.',
                          'Four times five, squared — or four squared times five squared. Same thing: four hundred.')])
        M.set_slide(VID, 10, script=[
            A('(−2)⁶ appears', T('$(-2)^6$', size=62, gap=50)),
            D('Write "= 64"'),
            "A negative base to an EVEN power: the minuses pair off. Positive sixty-four.",
            A('(−10)³ appears', T('$(-10)^3$', size=62, gap=50)),
            D('Write "= −1,000"'),
            "An ODD power: one minus is left over. Negative one thousand.",
            A('−7² appears', T('$-7^2$', size=62, gap=50)),
            D('Write "= −(7²) = −49"'),
            "No brackets? The power comes first — the minus comes after. Seven squared is forty-nine, then the minus: negative forty-nine.",
            "Brackets decide what the base is. Plugging in a negative number yourself? Always put it in brackets.",
        ])
        # the three cases of a^b = 1: on-screen text reworded (it was a word-for-word copy of the Hebrew slide)
        M.set_slide(VID, 11, script=[
            "A rule the exam loves. When is a to the b equal to one?",
            A('aᵇ = 1 appears', T('$a^b=1$', size=62, gap=50)),
            A('Case 1 appears: base 1', T('Base $1$: $\\ 1^b=1$ for every $b$', size=46)),
            "Case one: the base is one. Then the exponent can be anything.",
            A('Case 2 appears: base −1, even whole exponent', T('Base $-1$: $\\ b$ is an even whole number', size=46)),
            "Case two: the base is negative one — and the exponent is an even whole number. Two, four, minus two...",
            A('Case 3 appears: exponent 0, base not 0', T('Exponent $0$: $\\ a$ is any number except $0$', size=46)),
            D('Box all three cases'),
            "Case three: the exponent is zero. Then the base doesn't matter — anything nonzero to the zero is one.",
            "When a question says a to the b equals one — check all three cases.",
        ])
        c = M.card('powers')
        c['tips'][1] = r'$(-7)^2=49$ but $-7^2=-49$: brackets decide the base.'

    # ---------------- core questions from the Hebrew study guide (self-practice, no Hebrew video)
    # q-218: 0^√2 + (√2)^1 = √2 (key 1)
    S('q-218', stem=r'$\left(\sqrt{3}\right)^{1}+0^{\sqrt{3}}=\ ?$',
      choices=[r'$0$', r'$1$', r'$\sqrt{3}+1$', r'$\sqrt{3}$'], correct=4, expl=[
        r'Any number to the power of one is itself: $\left(\sqrt{3}\right)^1=\sqrt{3}$.',
        r'Zero to any positive power is $0$. The exponent $\sqrt{3}$ is positive, therefore $0^{\sqrt{3}}=0$.',
        r'The sum: $\sqrt{3}+0=\sqrt{3}$. The answer is choice 4.',
        r'The trap is choice 3: zero to a power is not $1$. Only an exponent of zero gives $1$.'])
    # q-219: 1^√5 + (√5)^0 = 2 (key 3)
    S('q-219', stem=r'$\left(\sqrt{7}\right)^{0}+1^{\sqrt{7}}=\ ?$',
      choices=[r'$\sqrt{7}+1$', r'$2$', r'$1$', r'$\sqrt{7}$'], correct=2, expl=[
        r'Any nonzero number to the power of zero is $1$: $\left(\sqrt{7}\right)^0=1$.',
        r'One to any power is $1$: $1^{\sqrt{7}}=1$.',
        r'The sum: $1+1=2$. The answer is choice 2.'])
    # q-220: −(−4)³ = 64 (key 4)
    S('q-220', stem=r'$-\left(-2\right)^{5}=\ ?$',
      choices=[r'$10$', r'$-32$', r'$32$', r'$-10$'], correct=3, expl=[
        r'First the power in the brackets. An odd power keeps the minus: $(-2)^5=(-2)\cdot(-2)\cdot(-2)\cdot(-2)\cdot(-2)=-32$.',
        r'The minus in front changes the sign: $-(-32)=32$. The answer is choice 3.',
        r'The traps: $-32$ forgets the minus in front, and $\pm10$ multiplies the base by the exponent.'])
    # q-221: (2/5)^−3 = 125/8 (key 2)
    S('q-221', stem=r'$\left(\frac{2}{3}\right)^{-3}=\ ?$',
      choices=[r'$\frac{8}{27}$', r'$-\frac{27}{8}$', r'$\frac{27}{8}$', r'$-\frac{8}{27}$'], correct=3, expl=[
        r'A negative exponent means "flip": $\left(\frac{2}{3}\right)^{-3}=\left(\frac{3}{2}\right)^3$.',
        r'Cube the top and the bottom: $\frac{3^3}{2^3}=\frac{27}{8}$. The answer is positive: choice 3.',
        r'A negative exponent never makes the number negative, therefore choices 2 and 4 are out.'])
    # q-222: (−3)^−4 = 1/81 (key 4)
    S('q-222', stem=r'$\left(-5\right)^{-2}=\ ?$',
      choices=[r'$\frac{1}{25}$', r'$-25$', r'$-\frac{1}{25}$', r'$25$'], correct=1, expl=[
        r'A negative exponent means "one over": $(-5)^{-2}=\frac{1}{(-5)^2}$.',
        r'An even power removes the minus: $(-5)^2=25$.',
        r'Therefore $(-5)^{-2}=\frac{1}{25}$. The answer is choice 1.'])
    # q-223: 11^−7 · 11^12 · 11^−3 = 121 (key 3)
    S('q-223', stem=r'$7^{-5}\cdot7^{9}\cdot7^{-2}=\ ?$',
      choices=[r'$49$', r'$7^{6}$', r'$7$', r'$1$'], correct=1, expl=[
        r'Same base, multiplying: add the exponents. $-5+9+(-2)=2$.',
        r'$7^{-5}\cdot7^{9}\cdot7^{-2}=7^2=49$. The answer is choice 1.',
        r'The trap is choice 2: losing the minus of $-2$ gives $-5+9+2=6$.'])
    # q-224 (guided, Question 1): 5^(x+2) = 25 · 5^x (key 3)
    S('q-224', stem=r'$4^{x+2}=\ ?$',
      choices=[r'$16\cdot4^{x}$', r'$4+4^{x}$', r'$16+4^{x}$', r'$4\cdot4^{x}$'], correct=1, expl=[
        r'A sum in the exponent splits into a product: $4^{x+2}=4^x\cdot4^2=16\cdot4^x$. The answer is choice 1.',
        r'Check with a number: $x=1$ gives $4^{3}=64$. The choices give $16\cdot4=64$, $4+4=8$, $16+4=20$ and $4\cdot4=16$. Only choice 1 gives $64$.'])
    video('q-224', {
        2: [
            "A plus in the exponent. Split it into a product.",
            D('Write "4ˣ⁺² = 4ˣ · 4²"'),
            "Four to the x, times four squared.",
            D('Write "= 16 · 4ˣ"'),
            "Sixteen times four to the x.",
            D('Circle choice 1'),
            "Choice one.",
        ],
        3: [
            "Not sure about the rule? Pick an easy x. Say x equals one.",
            D('Write "x = 1: 4³ = 64"'),
            "Four cubed: sixty-four.",
            "Now put x equals one into every choice.",
            D('Write "(1) 16 · 4 = 64   (2) 4 + 4 = 8   (3) 16 + 4 = 20   (4) 4 · 4 = 16"'),
            "Only choice one gives sixty-four.",
            D('Circle choice 1'),
            "Choice one. Same answer, no rule needed.",
        ]})
    # q-225: 13^9 / 13^7 = 169 (key 3)
    S('q-225', stem=r'$\frac{12^{8}}{12^{6}}=\ ?$',
      choices=[r'$\frac{1}{144}$', r'$144$', r'$12^{14}$', r'$12$'], correct=2, expl=[
        r'Same base, dividing: subtract the exponents, top minus bottom.',
        r'$\frac{12^8}{12^6}=12^{8-6}=12^2=144$. The answer is choice 2.'])
    # q-226 (guided, Question 2): 2 · 2^−6 / 2^−10 = 32 (key 3)
    S('q-226', stem=r'$\frac{3\cdot3^{-5}}{3^{-8}}=\ ?$',
      choices=[r'$\frac{1}{81}$', r'$3^{-12}$', r'$27$', r'$81$'], correct=4, expl=[
        r'Write every factor as a power of $3$: $3=3^1$.',
        r'Top: $3^1\cdot3^{-5}=3^{1+(-5)}=3^{-4}$.',
        r'Divide: $\frac{3^{-4}}{3^{-8}}=3^{-4-(-8)}=3^{-4+8}=3^4=81$. The answer is choice 4.',
        r'The traps: choice 2 adds $-8$ instead of subtracting it ($3^{-12}$), and choice 3 forgets the lonely $3$ ($3^{-5-(-8)}=3^3=27$).'])
    video('q-226', {
        2: [
            "Everything is a power of three. Even the lonely three: it's three to the one.",
            D('Write "3 = 3¹"'),
            "Top: three to the one times three to the minus five. Multiplying: add the exponents.",
            D('Write "3¹ · 3⁻⁵ = 3¹⁺⁽⁻⁵⁾ = 3⁻⁴"'),
            "One plus minus five: minus four.",
            "Now divide by three to the minus eight. Dividing: subtract. Top minus bottom.",
            D('Write "3⁻⁴⁻⁽⁻⁸⁾ = 3⁻⁴⁺⁸ = 3⁴"'),
            "Here's the trap. Minus four, minus minus eight. Two minuses make a plus: minus four plus eight. Four.",
            D('Write "3⁴ = 81"'),
            "Three to the fourth: eighty-one.",
            D('Circle choice 4'),
            "Choice four.",
            "Choice two, three to the minus twelve? That's what you get if you add the minus eight instead of subtracting it.",
            "And choice three, twenty-seven? That's what you get if you forget the lonely three.",
        ]})
    # q-231 (guided, Question 3): a^b = 1, which is not possible: a = 0 (key 1)
    S('q-231', stem='Given: $m^{n}=1$.\nWhich of the following is not possible?',
      choices=[r'$n=5$', r'$m=-1$', r'$m=0$', r'$n=0$'], correct=3, expl=[
        r'$m^n=1$ in three cases: $m=1$ (any $n$); $m=-1$ ($n$ an even whole number); $n=0$ (any $m\ne0$).',
        r'Choice 1, $n=5$: possible, for example $1^5=1$.',
        r'Choice 2, $m=-1$: possible, for example $(-1)^2=1$.',
        r'Choice 3, $m=0$: not possible. Zero to a positive power is $0$, and zero to the power of zero or of a negative number is not defined.',
        r'Choice 4, $n=0$: possible, for example $5^0=1$. The answer is choice 3.'])
    video('q-231', {
        2: [
            "When is m to the n equal to one? Three cases.",
            D('Write "m = 1 (any n)   ·   m = −1 (n even)   ·   n = 0 (m ≠ 0)"'),
            "Choice one: n equals five. Take m equals one. One to the fifth is one. Possible.",
            D('Write "✓" next to choice 1'),
            "Choice two: m equals minus one. Take n equals two. Minus one squared is one. Possible.",
            D('Write "✓" next to choice 2'),
            "Choice three: m equals zero. Zero to a positive power is zero. Zero to the zero, or to a negative power, is not defined.",
            "It can never be one.",
            D('Write "✗" next to choice 3'),
            "Let's still check the last one. Choice four: n equals zero. Any m that is not zero works. Possible.",
            D('Write "✓" next to choice 4'),
            D('Circle choice 3'),
            "Choice three.",
        ]}, intro=[('Our three options from the lesson do the work.', 'Our three cases from the lesson do the work.')])

    # ---------------- practice from the Hebrew study guide
    # q-228: 2^4 · 5^4 = 10,000 (key 3)
    S('q-228', stem=r'$5^{5}\cdot2^{5}=\ ?$',
      choices=[r'$100{,}000$', r'$10{,}000$', r'$1{,}000{,}000$', r'$1{,}000$'], correct=1, expl=[
        r'Same exponent, different bases: put them under one exponent.',
        r'$5^5\cdot2^5=(5\cdot2)^5=10^5=100{,}000$. The answer is choice 1.'])
    # q-229: 6^4 / 2^4 = 81 (key 2)
    S('q-229', stem=r'$\frac{12^{3}}{4^{3}}=\ ?$',
      choices=[r'$64$', r'$3$', r'$1728$', r'$27$'], correct=4, expl=[
        r'Same exponent on the top and the bottom: divide the bases first.',
        r'$\frac{12^3}{4^3}=\left(\frac{12}{4}\right)^3=3^3=27$. The answer is choice 4.'])
    # q-230: 5^3 / 15^3 = 1/27 (key 1)
    S('q-230', stem=r'$\frac{7^{3}}{14^{3}}=\ ?$',
      choices=[r'$\frac{1}{2}$', r'$\frac{1}{8}$', r'$\frac{1}{14}$', r'$\frac{1}{4}$'], correct=2, expl=[
        r'Same exponent on the top and the bottom: divide the bases first.',
        r'$\frac{7^3}{14^3}=\left(\frac{7}{14}\right)^3=\left(\frac{1}{2}\right)^3=\frac{1}{8}$. The answer is choice 2.'])
    # q-232: a < b, a^b = b^a, a + b = 6 (key 3). The 2-and-4 fact stays (it is the point); new letters, m > n, asks m·n
    S('q-232', stem='Given: $m$ and $n$ are positive integers, and\n' + r'$\begin{cases} m>n \\ m^n=n^m \end{cases}$' + '\n$m\\cdot n=\\ ?$',
      choices=[r'$8$', r'$6$', r'$16$', r'$4$'], correct=1, expl=[
        r'Among positive whole numbers, the only pair of different numbers with $m^n=n^m$ is $2$ and $4$: $4^2=16=2^4$.',
        r'$m>n$, therefore $m=4$ and $n=2$.',
        r'$m\cdot n=4\cdot2=8$. The answer is choice 1.',
        r'The traps: $6$ is $m+n$, and $16$ is the value of $m^n$.'])

    # ---------------- moved in from Topic 5 (Hebrew Topic 5 video questions)
    # q-131 (medium). Hebrew video (x^−2 + 2x²/x⁴)·½·(2/x^−2) = 3; study guide (x^−2 + 4x²/x⁴)·⅕·(5/x^−2) = 5
    S('q-131', stem='Given: $x\\ne0$.\n' + r'$\left(x^{-3}+\frac{2x^3}{x^6}\right)\cdot\frac{1}{3}\cdot\frac{6}{x^{-3}}=\ ?$',
      choices=[r'$3$', r'$6$', r'$1$', r'$18$'], correct=2, expl=[
        r'A negative power flips: $x^{-3}=\frac{1}{x^3}$. Cancel $x^3$ in the second fraction: $\frac{2x^3}{x^6}=\frac{2}{x^3}$.',
        r'The bracket equals $\frac{1}{x^3}+\frac{2}{x^3}=\frac{3}{x^3}$.',
        r'The negative power in the denominator moves up: $\frac{6}{x^{-3}}=6x^3$.',
        r'The expression is $\frac{3}{x^3}\cdot\frac{1}{3}\cdot6x^3=6$. The answer is choice 2.',
        r'Faster: the choices are numbers only. With $x=1$: $(1+2)\cdot\frac{1}{3}\cdot6=6$.'])
    video('q-131', {
        2: [
            "A negative power flips the fraction.",
            D('Under x⁻³ write "1/x³"'),
            "x to the minus three is one over x cubed.",
            D('Under 2x³/x⁶ write "2/x³"'),
            "Two x cubed over x to the sixth: cancel x cubed — two over x cubed.",
            D('Under 6/x⁻³ write "6x³"'),
            "Six over x to the minus three: the negative power jumps upstairs. Six x cubed.",
            D('Write "= 3/x³ · 1/3 · 6x³"'),
            "The bracket: one over x cubed plus two over x cubed. Same denominator — add the tops. Three over x cubed.",
            D('Cancel the 3s and the x³; write "= 6"'),
            "Cancel everything that cancels. Six.",
            D('Circle choice 2'),
            "Choice two.",
        ],
        3: [
            "Look at the choices — only numbers. No letters.",
            "When that happens, ONE substitution always solves it.",
            "And the friendliest number for powers is one. One to any power is one.",
            D('Write "x = 1: (1 + 2) · 1/3 · 6"'),
            "One plus two is three. Times a third, times six.",
            D('Write "= 6" and circle choice 2'),
            "Six. Choice two. Here, plugging in is much shorter — use it.",
            "Choice one, three, is only the bracket. Choice four, eighteen, forgets the one third.",
        ]}, stem_title=True)
    # q-132 (medium+). Hebrew video (a+a)−(a−a), ((a+1)+(a+1)²)/(a+2), a⁰+(−1)^a, (a²−4)/(a+2)−a;
    # study guide the same with 3a, a+2, a+3, a²−9. New letter n, new numbers, the constant is now choice 3.
    S('q-132', stem='Given: $n$ is a positive integer.\nWhich of the following expressions is a constant number that does not depend on $n$?',
      choices=[r'$(n+4n)-(4n-n)$', r'$(-1)^n+n^0$', r'$\dfrac{n^2-25}{n+5}-n$', r'$\dfrac{(n+3)+(n+3)^2}{n+4}$'], correct=3, expl=[
        r'(1): brackets first: $5n-3n=2n$. It depends on $n$.',
        r'(2): $n^0=1$, but $(-1)^n$ is $1$ when $n$ is even and $-1$ when $n$ is odd. The expression is $2$ or $0$. It depends on $n$.',
        r'(4): take out $n+3$ on top: $(n+3)+(n+3)^2=(n+3)(1+n+3)=(n+3)(n+4)$. Cancel $n+4$: $n+3$. It depends on $n$.',
        r'(3): $\frac{n^2-25}{n+5}=\frac{(n-5)(n+5)}{n+5}=n-5$, therefore the expression is $(n-5)-n=-5$ for every $n$. The answer is choice 3.'])
    video('q-132', {
        2: [
            "We're hunting for the expression where n vanishes.",
            D('Next to choice 1 write "5n − 3n = 2n"'),
            "Choice one: brackets first. n plus four n is five n. Four n minus n is three n. Five n minus three n: two n. Still has n — n equals one gives two, n equals two gives four.",
            D('Cross out choice 1'),
            "Out.",
            D('Next to choice 2 write "(±1) + 1 → 0 or 2"'),
            "Choice two: n to the zero is always one. But minus one to the power n: one if n is even, minus one if n is odd. Zero or two. Depends on n.",
            D('Cross out choice 2'),
            "Out. Choice three looks heavier — skip it for now and check choice four first.",
            D('Next to choice 4 write "(n + 3)(n + 4)/(n + 4) = n + 3"'),
            "Choice four: n plus three appears twice on top — a common factor. Take it out: n plus three, times one plus n plus three. That's n plus four. Cancel n plus four. n plus three. Out.",
            D('Cross out choice 4'),
            "Three out — choice three is our answer. On the exam, mark it and move on. No need to prove it.",
            D('Next to choice 3 write "(n − 5)(n + 5)/(n + 5) − n = −5"'),
            "Proof, for the lesson: n squared minus twenty-five is n minus five, times n plus five. Cancel. n minus five, minus n — minus five. Always.",
            D('Circle choice 3'),
            "Choice three. Plugging in here would be long: two values of n for every choice, until three choices are out. The direct method wins.",
        ]}, intro=[("doesn't depend on a? Simplify until the a disappears.",  # review 2026-10-02: the letter is n now
                    "doesn't depend on n? Simplify until the n disappears.")], stem_title=True)
    # q-expression-extra-09: a companion of the Hebrew video question, (x^−2 + 2/x²)·x² = 3 (key 3)
    S('q-expression-extra-09', stem='Given: $x\\ne0$.\n' + r'$x^{3}\cdot\left(x^{-3}+\frac{4}{x^{3}}\right)=\ ?$',
      choices=[r'$5$', r'$4$', r'$x^{3}$', r'$1$'], correct=1, expl=[
        r'$x^{-3}=\frac{1}{x^3}$, therefore the bracket equals $\frac{1}{x^3}+\frac{4}{x^3}=\frac{5}{x^3}$.',
        r'Then $x^3\cdot\frac{5}{x^3}=5$. The answer is choice 1.',
        r'Or multiply each term by $x^3$: $x^3\cdot x^{-3}+x^3\cdot\frac{4}{x^3}=x^0+4=1+4=5$.'])


# ----------------------------------------------------------------------------------------------------------------
# 9. 2026-10-02 order changes (less like a copy of the Hebrew course; only where nothing is lost)
# ----------------------------------------------------------------------------------------------------------------
def _swap_slides(M, vid, a, b_):
    """Swap two neighbouring concept slides (a < b_) and their sidebar labels; fix the 'active' indexes."""
    v = M.video(vid); sb = v['hybrid']['sidebar']
    x, y = v['beats'][a - 1], v['beats'][b_ - 1]
    ia, ib = x['active'], y['active']
    sb[ia], sb[ib] = sb[ib], sb[ia]
    x['active'], y['active'] = ib, ia
    M.move_slide(vid, b_, a)
    M.set_sidebar(vid, sb)


def order_changes(M):
    # (1) lesson: "2⁴ = 4²" (a single fact) now comes before "When aᵇ = 1" (the rule the guided Question 3 uses).
    #     Neither slide refers to the other; aᵇ = 1 still comes after "Negative bases", which it needs.
    assert M.slide(VID, 11)['title'] == 'When aᵇ = 1' and M.slide(VID, 12)['title'] == '2⁴ = 4²'
    _swap_slides(M, VID, 11, 12)
    # (2) core questions in the order the lesson teaches them:
    #     (√7)⁰ + 1^√7 before (√3)¹ + 0^√3 (same level), (2/3)⁻³ (negative exponent, slide 4) before −(−2)⁵ (negative
    #     base, slide 10), and the plain division 12⁸/12⁶ before the split exponent 4^(x+2).
    M.move('q-219', CORE, before='q-218')
    M.move('q-221', CORE, before='q-220')
    M.move('q-225', CORE, before='q-224')


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
    # Exponent Traps: "Signs with letters" is taught in Question 6 (odd keeps the sign, even is never negative;
    # (-x)^2 and -x^2 are on the laws lesson's "Negative bases" slide). "Check with a number" is taught in
    # Question 1 (method 2), Question 4 (two choices tie -> try another n) and Question 5 (pick one half).
    L = 'r26-t08-traps'
    _cr_titles(M, L, ['Between 0 and 1', 'Compare powers'])
    M.set_slide(L, 1, script=[
        'The laws are done. Now the traps the exam loves.',
        'Two short ideas here. The other traps come inside the questions, right after this video.'])
    # slide 2: Question 5 teaches "between 0 and 1, each extra power is smaller"; the decimals stay (taught nowhere else)
    _cr_drop(M, L, 2, [r'\left(\frac{1}{2}\right)^1', 'Each extra power: smaller again.',
                       '0<x<1:\\quad x^3<x^2<x', 'So for a number between zero and one'])
    _cr_replace(M, L, 2, "Above one it's the opposite", [
        'Careful: a power makes a number smaller only between zero and one. Above one, it makes it bigger.'])


_apply_before_cut_repeats = apply


def apply(M):
    _apply_before_cut_repeats(M)
    cut_repeats(M)   # 2026-10-05: runs last


# ---------------------------------------------------------------- 2026-10-06 pen or click
# Teacher-approved split (2026-10-04/06): lessons - content appears by click, the pen only marks (circle, underline,
# arrow, cross out); solution videos - setup and mechanical lines by click, by hand only the one or two key steps
# plus the marks on the choices. Helper copied from t07.py (same behaviour).
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


def _pre_gap(M, vid, n, gap):
    """the item already on the slide kept a big gap for handwriting under it; that line is now a click item."""
    M.slide(vid, n)['items'][0]['gap'] = gap


def pen_or_click(M):
    L, S = 52, 42
    # ---- lesson: exponents (every written line becomes a click item; arrows, circles, underlines, boxes,
    #      cross-outs stay by hand)
    V = 'exponents'
    _pen_or_click_slide(M, V, 2, {
        'Write "= 4 · 4 · 4"': [A('= 4 · 4 · 4 appears', T(r'$=4\cdot4\cdot4$', size=56))],
        'Write "= 64"': [A('= 64 appears', T(r'$=64$', size=56))],
    })
    _pen_or_click_slide(M, V, 3, {
        'Write "1" in place of the question mark': [A('5⁰ = 1 appears', T(r'$5^0=1$', size=50))],
        'Write "= 1" after each one': [A('Both = 1 appears', T(r'Both $=1$', size=50))],
    })
    _pen_or_click_slide(M, V, 4, {
        'Write "= 1/2³ = 1/8"': [A('= 1/2³ = 1/8 appears', T(r'$=\frac{1}{2^3}=\frac{1}{8}$', size=56))],
        'Write "= (2/5)² = 4/25"': [A('= (2/5)² = 4/25 appears', T(r'$=\left(\frac{2}{5}\right)^2=\frac{4}{25}$', size=56))],
    })
    _pen_or_click_slide(M, V, 6, {
        'Under it write "(3·3)·(3·3·3·3)"': [A('(3·3)·(3·3·3·3) appears', T(r'$=(3\cdot3)\cdot(3\cdot3\cdot3\cdot3)$', size=L))],
        'Write "= 3²⁺⁴ = 3⁶"': [A('= 3²⁺⁴ = 3⁶ appears', T(r'$=3^{2+4}=3^6$', size=L))],
    })
    _pre_gap(M, V, 6, 50)
    _pen_or_click_slide(M, V, 7, {      # the cross-out of the fives stays by hand (a smaller gap under 5⁷/5³ stays)
        'Write "= 5⁷⁻³ = 5⁴"': [A('= 5⁷⁻³ = 5⁴ appears', T(r'$=5^{7-3}=5^4$', size=46))],
        'Write "= 1/5³ = 5⁻³"': [A('= 1/5³ = 5⁻³ appears', T(r'$=\frac{1}{5^3}=5^{-3}$', size=46))],
        'Write "= 1"; then write "= 5³⁻³ = 5⁰"': [A('= 1, and = 5³⁻³ = 5⁰ appears',
                                                    T(r'$=1 \qquad\text{and also}\qquad =5^{3-3}=5^0$', size=42))],
    })
    _pre_gap(M, V, 7, 90)
    for it in M.slide(V, 7)['items'][1:]: it['gap'] = min(it.get('gap', 44), 30)
    _pen_or_click_slide(M, V, 8, {
        'Under it write "2³ · 2³ · 2³ · 2³"': [A('2³ · 2³ · 2³ · 2³ appears', T(r'$=2^3\cdot2^3\cdot2^3\cdot2^3$', size=L))],
        'Write "= 2³ˣ⁴ = 2¹²"': [A('= 2³ˣ⁴ = 2¹² appears', T(r'$=2^{3\cdot4}=2^{12}$', size=L))],
        'Write "= 2⁷"': [A('= 2⁷ appears', T(r'$=2^7$', size=L))],
    })
    _pre_gap(M, V, 8, 50)
    _pen_or_click_slide(M, V, 9, {
        'Write "= 4² · 5² = 16 · 25 = 400"': [A('= 4² · 5² = 16 · 25 = 400 appears', T(r'$=4^2\cdot5^2=16\cdot25=400$', size=50))],
    })
    _pen_or_click_slide(M, V, 10, {
        'Write "= 64"': [A('= 64 appears', T(r'$=64$', size=50))],
        'Write "= −1,000"': [A('= −1,000 appears', T(r'$=-1{,}000$', size=50))],
        'Write "= −(7²) = −49"': [A('= −(7²) = −49 appears', T(r'$=-(7^2)=-49$', size=50))],
    })
    _pen_or_click_slide(M, V, 13, {
        'Write "= 2ⁿ · 2³ = 8 · 2ⁿ"': [A('= 2ⁿ · 2³ = 8 · 2ⁿ appears', T(r'$=2^n\cdot2^3=8\cdot2^n$', size=L))],
        'Write "= 8 · 2ⁿ − 1 · 2ⁿ = 7 · 2ⁿ"': [A('= 8 · 2ⁿ − 1 · 2ⁿ = 7 · 2ⁿ appears', T(r'$=8\cdot2^n-1\cdot2^n=7\cdot2^n$', size=L))],
    })
    _pre_gap(M, V, 13, 50)
    _pen_or_click_slide(M, V, 14, {
        'Circle the "2 ·" and write "2 = 2¹" above it': [D('Circle the "2 ·"'), A('2 = 2¹ appears', T(r'$2=2^1$', size=46))],
        'Cross out 2²ⁿ and write "n = 3: 8 + 8 = 16, but 2⁶ = 64"': [
            D('Cross out 2²ⁿ'), A('n = 3: 8 + 8 = 16, but 2⁶ = 64 appears', T(r'$n=3:\ \ 8+8=16$, but $2^6=64$', size=44))],
    })
    # ---- Question 1: q-224 - by hand: the split 4ˣ⁺² = 4ˣ · 4² (the idea), circles
    _pen_or_click_slide(M, 'solve-q-224', 2, {
        'Write "= 16 · 4ˣ"': [A('= 16 · 4ˣ appears', T(r'$=16\cdot4^x$', size=S))],
    }, room=['Write "4ˣ⁺² = 4ˣ · 4²"'])
    _pen_or_click_slide(M, 'solve-q-224', 3, {
        'Write "x = 1: 4³ = 64"': [A('x = 1: 4³ = 64 appears', T(r'$x=1:\ \ 4^3=64$', size=S))],
        'Write "(1) 16 · 4 = 64   (2) 4 + 4 = 8   (3) 16 + 4 = 20   (4) 4 · 4 = 16"': [
            A('The four choices at x = 1 appear', T(r'(1) $16\cdot4=64$ $\quad$ (2) $4+4=8$ $\quad$ (3) $16+4=20$ $\quad$ (4) $4\cdot4=16$', size=34))],
    })
    # ---- Question 2: q-226 - by hand: 3 = 3¹ (the lonely three), circle
    _pen_or_click_slide(M, 'solve-q-226', 2, {
        'Write "3¹ · 3⁻⁵ = 3¹⁺⁽⁻⁵⁾ = 3⁻⁴"': [A('3¹ · 3⁻⁵ = 3⁻⁴ appears', T(r'$3^1\cdot3^{-5}=3^{1+(-5)}=3^{-4}$', size=S))],
        'Write "3⁻⁴⁻⁽⁻⁸⁾ = 3⁻⁴⁺⁸ = 3⁴"': [A('3⁻⁴⁻⁽⁻⁸⁾ = 3⁴ appears', T(r'$3^{-4-(-8)}=3^{-4+8}=3^4$', size=S))],
        'Write "3⁴ = 81"': [A('3⁴ = 81 appears', T(r'$3^4=81$', size=S))],
    }, room=['Write "3 = 3¹"'])
    # ---- Question 3: q-231 - the three cases by click; ticks, cross and circle on the choices by hand
    _pen_or_click_slide(M, 'solve-q-231', 2, {
        'Write "m = 1 (any n)   ·   m = −1 (n even)   ·   n = 0 (m ≠ 0)"': [
            A('The three cases appear', T(r'$m=1$ (any $n$) $\ \cdot\ $ $m=-1$ ($n$ even) $\ \cdot\ $ $n=0$ ($m\ne0$)', size=36))],
    })
    # ---- lesson: Exponent Traps
    _pen_or_click_slide(M, 'r26-t08-traps', 2, {
        'Write "3 places" under 0.008 and "2 places" under 0.09': [
            A('3 places · 2 places appears', T(r'$0.008$: 3 places $\qquad 0.09$: 2 places', size=40))],
    })
    _pen_or_click_slide(M, 'r26-t08-traps', 3, {
        'Write "2¹⁰ > 2⁸"': [A('2¹⁰ > 2⁸ appears', T(r'$2^{10}>2^8$', size=46))],
        'Write "2³⁰ < 3²⁰"': [A('2³⁰ < 3²⁰ appears', T(r'$2^{30}<3^{20}$', size=46))],
        'Write "x = 3"': [A('x = 3 appears', T(r'$x=3$', size=46))],
    })
    for it in M.slide('r26-t08-traps', 3)['items']:      # 8 lines now: a bit smaller and closer
        it['size'] = min(it.get('size', 46), 44); it['gap'] = min(it.get('gap', 44), 16)
    # ---- Question 4: q-r26-t08-01 - by hand: = 4 · 2ⁿ (count the copies), circle
    _pen_or_click_slide(M, 'solve-q-r26-t08-01', 2, {
        'Write "= 2² · 2ⁿ = 2ⁿ⁺²"': [A('= 2² · 2ⁿ = 2ⁿ⁺² appears', T(r'$=2^2\cdot2^n=2^{n+2}$', size=S))],
    }, room=['Write "= 4 · 2ⁿ"'])
    _pen_or_click_slide(M, 'solve-q-r26-t08-01', 3, {
        'Write "n = 1: 8   (1) 16   (2) 8   (3) 8   (4) 32"': [
            A('n = 1: the sum and the four choices appear', T(r'$n=1$: $\ 8$ $\qquad$ (1) $16$ $\quad$ (2) $8$ $\quad$ (3) $8$ $\quad$ (4) $32$', size=38))],
        'Write "n = 2: 16   (2) 64   (3) 16"': [
            A('n = 2: the sum, choices 2 and 3 appear', T(r'$n=2$: $\ 16$ $\qquad$ (2) $64$ $\quad$ (3) $16$', size=38))],
    })
    # ---- Question 5: q-r26-t08-02 - plug-in lines by click, circle by hand
    _pen_or_click_slide(M, 'solve-q-r26-t08-02', 2, {
        'Write "x = ½"': [A('x = ½ appears', T(r'$x=\frac12$', size=S))],
        'Write "(1) ½   (2) ¼   (3) ⅛   (4) 2² = 4"': [
            A('The four choices at x = ½ appear', T(r'(1) $\frac12$ $\quad$ (2) $\frac14$ $\quad$ (3) $\frac18$ $\quad$ (4) $2^2=4$', size=S))],
    })
    # ---- Question 6: q-r26-t08-05 - by hand: x³ < 0 → x < 0 (the odd power keeps the sign), circle
    _pen_or_click_slide(M, 'solve-q-r26-t08-05', 2, {
        'Write "y² > 0"': [A('y² > 0 appears', T(r'$y^2>0$', size=S))],
    }, room=['Write "x³ < 0 → x < 0"'])


_apply_before_pen_or_click = apply


def apply(M):
    _apply_before_pen_or_click(M)
    pen_or_click(M)   # 2026-10-06 pen or click: runs last


# =====================================================================================
# 2026-10-07 practice clean-up (teacher-approved). Practice was 25: 4 Hebrew self-practice questions (q-228, q-229,
# q-230, q-232), 6 extra-bank warm-ups and 15 September-review items. Copies out, at most 3 warm-ups, review items
# whose type the Hebrew / guided questions already practise out (one of each other type kept). Kept: 4 Hebrew,
# 3 warm-ups, 5 review items. Runs LAST.
# =====================================================================================
CLEANUP_REMOVE = [
    # copies (practice_audit/copies_by_topic.txt, each checked against the current build)
    'alg-extra-exponent-extra-1',   # 2⁶/2³: guided q-225 (12⁸/12⁶)
    'q-r26-t08-06',                 # 3ⁿ + 3ⁿ + 3ⁿ: guided q-r26-t08-01 (2ⁿ four times)
    'q-r26-t08-11',                 # -1 < x < 0, largest of x ... x⁴: guided q-r26-t08-02
    'q-r26-t08-19',                 # x³y⁵ < 0: guided q-r26-t08-05 (x³y² < 0)
    # warm-up beyond the kept three
    'alg-extra-exponent-extra-6',   # 2¹⁰ vs 4⁴: kept q-r26-t08-12 is the same comparison (same base)
    # September items of a type the Hebrew / guided questions already practise
    'q-r26-t08-17',                 # x⁵ < 0 -> x < 0: guided q-r26-t08-05
    'q-r26-t08-18',                 # -x² necessarily negative: Hebrew q-220 / q-222 (signs of powers)
    'q-r26-t08-21',                 # (2³)² · 2⁻⁴ / 2²: Hebrew q-223 / q-226 (same base)
    'q-r26-t08-22',                 # 6⁵/(2⁵ · 3³): Hebrew q-228 ... q-230 (aⁿbⁿ = (ab)ⁿ)
    'q-r26-t08-15',                 # 2³ · 5⁶: Hebrew q-228 (5⁵ · 2⁵)
    'q-r26-t08-10',                 # 0.2³ · 10⁴: kept q-r26-t08-09 (decimal power)
    'q-r26-t08-08',                 # 2ⁿ⁺¹ + 2ⁿ⁺¹ = 32: kept q-r26-t08-07 (sum of equal powers) + q-r26-t08-14
    'q-r26-t08-20',                 # (x - 2)^(x + 3) = 1: guided q-231 (mⁿ = 1)
]
CLEANUP_ORDER = [
    'q-228', 'q-229', 'q-230', 'q-r26-t08-09', 'alg-extra-exponent-extra-4', 'alg-extra-exponent-extra-5',
    'alg-extra-exponent-extra-3', 'q-r26-t08-12', 'q-r26-t08-07', 'q-r26-t08-14', 'q-r26-t08-23', 'q-232']


def practice_cleanup(M):
    for qid in CLEANUP_REMOVE:
        assert M.section_of(qid) == PRACTICE, qid
        M.unplace(qid)
    order = list(CLEANUP_ORDER)
    # q-expression-extra-09 (Hebrew topic-5 original, x³(x⁻³ + 4/x³)) is moved here by the T5 patch: keep it,
    # after the other negative-exponent items
    if any(f['ref'] == 'q-expression-extra-09' and f['section'] == PRACTICE for f in M.D['flow']):
        order.insert(order.index('alg-extra-exponent-extra-5') + 1, 'q-expression-extra-09')
    M.practice_order(PRACTICE, order)
    got = [f['ref'] for f in M.D['flow'] if f['section'] == PRACTICE and f['type'] == 'question']
    assert got == order, got


_apply_before_practice_cleanup = apply


def apply(M):
    _apply_before_practice_cleanup(M)
    practice_cleanup(M)   # 2026-10-07 practice clean-up: runs last


# =====================================================================================
# 2026-10-07 methods spread: the 2026-10-06 exam methods added as an extra written line wherever they genuinely
# solve the question (append only; the existing solution stays). Methods taught in a later topic are phrased as a
# self-contained shortcut with a one-line why. No video changes. Runs LAST.
# =====================================================================================
SPREAD_METHODS = {
    'q-r26-t08-05': [
        'Shortcut: the mirror test. Put $-y$ in place of $y$: $x^3(-y)^2=x^3y^2$, so the given stays exactly the same, and anything necessarily true must stay true in the mirror.',
        "Choice 2 ($y<0$) turns into $y>0$, choice 3 ($xy<0$) into $xy>0$, and choice 4 ($x^2y>0$) into $x^2y<0$. Each turns into its opposite, and a statement and its opposite can't both always be true. All three are out with no numbers. Choice 1 doesn't change: it is the answer.",
    ],
}


def spread_methods(M):
    for qid, lines in SPREAD_METHODS.items():
        q = M.q(qid)
        M.set_q(qid, expl=list(q['explanation']) + lines)


_apply_before_spread_methods = apply


def apply(M):
    _apply_before_spread_methods(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last
