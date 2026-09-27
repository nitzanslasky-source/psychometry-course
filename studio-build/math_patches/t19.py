"""Topic 19 - Defining a New Operation. Course review 2026-09 fixes.
See t19_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q
from math_api import _word

TOPIC = 19
LESSON = 'new-operation'
PATTERNS = 'operation-patterns'
CARD = 'mem-new-operation'
THEORY = 'new-operation-theory'
ADV = 'new-operation-advanced'
PRACTICE = 'unit-t19-3'
BL = '\\blacklozenge'
PIECE = '$\\blacklozenge(x)=\\begin{cases} 2x, & x \\text{ odd} \\\\ x^2-7, & x \\text{ even} \\end{cases}$'


def _solution(M, qid, group, intro, slides, after=None):
    """Guided-question solution video in the style of solve-q-541..556 (group = 'theory' | 'advanced')."""
    n = M.next_question_number(TOPIC)
    head = ['Question %s.' % _word(n)] + intro
    beats = [dict(mode='title', title='Question %d' % n, script=head)]
    for title, script in slides:
        beats.append(dict(mode='question', active=n - 1, title=title, pre=[Q(qid)], script=script))
    gt = 'Operation Questions' if group == 'theory' else 'Advanced Operations'
    v = M.new_video('solve-' + qid, TOPIC, gt, [], beats, M.section_of(qid), kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = gt
    v['hybrid']['num'] = 62 if group == 'theory' else 63
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
    """new = str (replace the line), list (replace with several lines) or None (delete)."""
    def fn(lines):
        out = []
        for l in lines:
            if l.get('say') == old:
                if new is None: continue
                for x in ([new] if isinstance(new, str) else new):
                    out.append({'say': x} if isinstance(x, str) else {'draw': x[1]})
            else:
                out.append(l)
        assert any(l.get('say') == old for l in lines), (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def apply(M):
    S = M.set_q
    # =====================================================================================
    # 1. Lesson video 1: Defining a New Operation
    # =====================================================================================
    # new slide 5: brackets on every input (after "Exam symbols")
    M.insert_slides(LESSON, 4, [dict(mode='concept', active=3, title='Brackets on every input', script=[
        "Now the most common exam move: put a negative number, or a whole expression, into the operation.",
        A('The definition appears: ◆(x) = x² − 2x', T('$\\blacklozenge(x)=x^2-2x$', size=52, gap=40)),
        "The rule: whatever goes in, goes in brackets. Every time.",
        A('◆(−3) appears', T('$\\blacklozenge(-3)$', size=48, gap=40)),
        D('Next to it write "= (−3)² − 2 · (−3) = 9 + 6 = 15"'),
        "Minus three, in brackets, squared: nine. Minus two times minus three: plus six. Fifteen.",
        "Without brackets you'd write minus three squared — that's minus nine. Wrong.",
        A('◆(x + 1) appears', T('$\\blacklozenge(x+1)$', size=48, gap=40)),
        D('Next to it write "= (x + 1)² − 2(x + 1)"'),
        "Now the input is x plus one. The whole thing goes where x was — in brackets.",
        D('Below write "= x² + 2x + 1 − 2x − 2 = x² − 1"'),
        "Open the brackets: x squared plus two x plus one, minus two x, minus two. x squared minus one.",
        D('Next to it write "x + 1² − 2x + 1" and cross it out'),
        "Here's the trap: no brackets. It looks similar — and it's completely wrong.",
    ])])
    # slides 6.. moved one down in the sidebar
    for n in range(6, 12):
        M.slide(LESSON, n)['active'] = n - 2
    M.set_sidebar(LESSON, ['A new symbol', 'The heart', 'Exam symbols', 'Brackets on every input', 'Operation first',
                           'Nested: inside out', 'Find the operation', 'Order can matter', 'Unknown input', 'Recap'])

    # slide 6: operation first - no "general precedence rule"
    M.set_slide(LESSON, 6, pre=[], script=[
        "Where does a new operation fit in a longer exercise?",
        A('The definition appears: ◆(x) = x²', T('$\\blacklozenge(x)=x^2$', size=56, gap=60)),
        "Let's say the diamond squares its input.",
        A('◆(3) + ◆(4) appears', T('$\\blacklozenge(3)+\\blacklozenge(4)$', size=56, gap=60)),
        "First turn every diamond into a plain number. Then do the rest of the exercise as usual.",
        D('Write "= 9 + 16 = 25"'),
        "The diamond of three is nine. The diamond of four is sixteen. Now add: twenty-five.",
        A('◆(3 + 4) appears', T('$\\blacklozenge(3+4)$', size=56, gap=40)),
        "Here the plus sits inside the diamond's own brackets. So first work out the input: seven.",
        D('Write "= ◆(7) = 7² = 49 ≠ 25"'),
        "The diamond of seven is forty-nine — a totally different number.",
        "And a symbol between two numbers, like a star b, inside a longer exercise? On the exam, brackets always show what comes first.",
    ])

    # slide 9: order can matter - the "always / not always" rule
    old = M.slide(LESSON, 9)['items'][0]
    M.set_slide(LESSON, 9, pre=[], script=[
        "One more thing about the star.",
        A('3 ⋆ 4 and 4 ⋆ 3 appear', dict(old, size=56, gap=50)),
        D('Under 3 ⋆ 4 write "6 + 16 = 22"; under 4 ⋆ 3 write "8 + 9 = 17"'),
        "Three star four: six plus sixteen, twenty-two. Four star three: eight plus nine, seventeen.",
        "Swap the inputs — a different answer. Never assume a new operation behaves like plus.",
        "So before you calculate, circle which number goes into which slot.",
        A("'Not always? One counterexample.' appears", T('"Not always"? One counterexample is enough.', size=40, gap=30)),
        "Now, a question may ask: is a star b always equal to b star a? To say no, one counterexample is enough — like three and four.",
        A("'Always? Swap the letters in the algebra.' appears", T('"Always"? Swap the letters in the algebra.', size=40, gap=30)),
        "To say yes, numbers are not enough. Write b star a with letters, and compare it to a star b.",
        "One warning: don't test with two equal numbers. Three star three equals three star three — for every operation. It proves nothing.",
    ])

    # slide 10: unknown input - work back from the answers
    M.edit_lines(LESSON, 10, lambda ls: ls + [
        {'say': "On the exam you can also work back from the answers: put each choice into the rule."},
        {'draw': 'Write "x = 7: 2 · 7 + 2² = 14 + 4 = 18 ✓"'},
        {'say': "Seven: fourteen plus four, eighteen. That's the one."},
    ])

    # slide 11: recap
    M.set_slide(LESSON, 11, pre=[], script=[
        "Let's lock it in.",
        A("'Read the definition, then substitute every letter' appears", T('Read the definition, then substitute every letter', size=40)),
        A("'Every input goes in brackets' appears", T('Every input goes in brackets: $\\blacklozenge(-3)=(-3)^2\\ldots$', size=40)),
        A("'First turn each operation into a number' appears", T('First turn each operation into a number', size=40)),
        A("'Nested? Inside out' appears", T('Nested? Inside out', size=40)),
        A("'Find the operation? Test each choice' appears", T('Find the operation? Test each choice', size=40)),
        A("'Always? Algebra. Not always? One example.' appears", T('"Always"? Algebra. "Not always"? One example.', size=40)),
        D('Underline "brackets"'),
        "Nothing complicated here — just follow the recipe faithfully.",
        "Five questions next. Then: more advanced operations.",
    ])

    # =====================================================================================
    # 2. Lesson video 2: Operation Patterns - an example on every board, two new types
    # =====================================================================================
    P = PATTERNS
    M.set_slide(P, 3, pre=[], script=[
        "Type two: conditions.",
        A('The definition with two rules appears', T(PIECE, size=44, gap=40)),
        "One rule for odd x, another rule for even x.",
        "Before you apply anything, check the input: odd or even?",
        A('◆(3) and ◆(4) appear', T('$\\blacklozenge(3)\\qquad\\qquad\\blacklozenge(4)$', size=48, gap=40)),
        D('Under ◆(3) write "3 odd → 2 · 3 = 6"; under ◆(4) write "4 even → 4² − 7 = 9"'),
        "Three is odd: two times three, six. Four is even: sixteen minus seven, nine.",
        "And check again at every step — the output of one step is the input of the next, and it can switch from odd to even.",
    ])
    M.insert_slides(P, 3, [dict(mode='concept', active=2, title='Conditions backwards', script=[
        "Now the other direction: they give you the result, and ask for the input.",
        A('The definition with two rules appears', T(PIECE, size=44, gap=40)),
        A('◆(x) = 9, x a positive integer, appears', T('$\\blacklozenge(x)=9$, $\\ x$ a positive integer.$\\ \\ x=\\ ?$', size=42, gap=30)),
        "You don't know which rule x used. So try both rules.",
        D('Write "odd rule: 2x = 9 → x = 4.5 ✗ (not an integer)"'),
        "Odd rule: two x is nine, so x is four and a half. That's not even an integer. Throw it out.",
        D('Write "even rule: x² − 7 = 9 → x² = 16 → x = 4 ✓ (4 is even)"'),
        "Even rule: x squared is sixteen, so x is four — it's positive. Four is even, so it really uses the even rule. Keep it.",
        "Always check: does the answer fit the rule you used? If not, throw it out.",
        "Or work back from the answers: put each choice into the operation, and see which one gives nine.",
    ])])
    M.set_slide(P, 5, pre=[], script=[
        "Type three: a circular operation — the operation appears inside its own definition.",
        A('A circular definition appears',
          T('$\\blacklozenge(x)=\\begin{cases} 3, & x=1 \\\\ 2\\cdot\\blacklozenge(x-1), & x>1 \\end{cases}$', size=44, gap=40)),
        "To know the diamond of x, you need the diamond of x minus one. And they give one start value: the diamond of one is three.",
        A('◆(3) = ? appears', T('$\\blacklozenge(3)=\\ ?$', size=48, gap=40)),
        D('Write "◆(3) = 2 · ◆(2)  →  ◆(2) = 2 · ◆(1)  →  ◆(1) = 3"'),
        "Keep substituting — down and down — until you reach the start value.",
        D('Write "◆(2) = 2 · 3 = 6  →  ◆(3) = 2 · 6 = 12"'),
        "Then climb back up with real numbers. Two times three: six. Two times six: twelve.",
    ])
    M.set_slide(P, 6, pre=[], script=[
        "Type four — very rare on the exam: the operation sits on both sides of an equation.",
        A('2 · ◆(x) + 1 = ◆(x) + x appears', T('$2\\cdot\\blacklozenge(x)+1=\\blacklozenge(x)+x$', size=50, gap=40)),
        "Treat the diamond of x as the unknown. Isolate it exactly like you'd isolate x.",
        D('Write "2◆(x) − ◆(x) = x − 1  →  ◆(x) = x − 1"'),
        "Two diamonds minus one diamond: one diamond. It equals x minus one.",
        "Once it's alone, it's a basic question again. For example, the diamond of five is four.",
    ])
    M.insert_slides(P, 6, [dict(mode='concept', active=5, title='Definition in words', script=[
        "Type five: the definition is in words, not in a formula.",
        A('[x] = the largest integer not bigger than x appears',
          T('$[x]$ = the largest integer that is not bigger than $x$', size=40, gap=40)),
        "A classic: the integer part of x. The largest integer that is not bigger than x.",
        "Words are easy to misread. So before you touch the choices, write two or three quick examples.",
        A('[3.7] = 3, [5] = 5, [−2.3] = ? appear', T('$[3.7]=3\\qquad[5]=5\\qquad[-2.3]=\\ ?$', size=46, gap=40)),
        "Three point seven: three. Five: five — it's already an integer.",
        D('Next to [−2.3] write "= −3, not −2"'),
        "Minus two point three? Not minus two — minus two is bigger than minus two point three. So it's minus three.",
        "Other definitions in words: the remainder of a division, the number of divisors, the sum of the digits. Same move: examples first.",
    ])])
    M.set_slide(P, 8, title='Must be true?', pre=[], script=[
        "Type six: \"which of the following must be true\" — sometimes they write \"necessarily true\" — with the operation inside every choice.",
        "It's the must question from Topic 1: plug in numbers, and break the wrong choices.",
        "Tip: skip it at first. Solve the rest of the section, then come back. It can eat your time.",
        A('◆(x) = x². Must ◆(2x) = 2 · ◆(x)? appears',
          T('$\\blacklozenge(x)=x^2$. Must $\\blacklozenge(2x)=2\\cdot\\blacklozenge(x)$?', size=44, gap=40)),
        D('Write "x = 0: 0 = 0 ✓ ?!"'),
        "Try zero: zero equals zero. It looks true!",
        D('Write "x = 2: 16 ≠ 8 ✗"'),
        "Try two: the diamond of four is sixteen. Two times the diamond of two is eight. False. Zero fooled us.",
        A("'Avoid 0, 1 and equal values' appears", T('Plug in $2$ or $3$ — avoid $0$, $1$ and equal values', size=40, gap=30)),
        "Zero, one, and two equal letters can make a false rule look true. Choose numbers like two or three.",
        A("'Two choices left? Try a second number.' appears", T('Two choices left? Try a second number.', size=40)),
        "And if two choices survive, try a second, different number.",
    ])
    M.set_slide(P, 9, pre=[], script=[
        "Let's lock it in.",
        A("'Expression input? Match the whole input' appears", T('Expression input? Match the whole input', size=38)),
        A("'Conditions? Check at every step' appears", T('Conditions? Check at every step', size=38)),
        A("'Result given? Try every rule, then check' appears", T('Result given? Try every rule, then check the answer', size=38)),
        A("'Circular? Down to the start value, then back up' appears", T('Circular? Down to the start value, then back up', size=38)),
        A("'Both sides? Isolate the operation' appears", T('Both sides? Isolate the operation', size=38)),
        A("'Words? Write examples first' appears", T('Definition in words? Write examples first', size=38)),
        A("'Must be true? Last — plug in 2 or 3' appears", T('Must be true? Last — plug in $2$ or $3$, not $0$ or $1$', size=38)),
        D('Tick each line'),
        "Those are the types that can show up. Now you know what to do with every one.",
        "Questions next — at least one for each type.",
    ])
    M.set_sidebar(P, ['Expression input', 'Conditions', 'Conditions backwards', 'Circular rules', 'Isolate the operation',
                      'Definition in words', 'Must be true?', 'Recap'])
    for n in range(2, 10):
        M.slide(P, n)['active'] = n - 2

    # =====================================================================================
    # 3. Existing solution videos: wrong or weak reasoning, colons, plug-in warnings
    # =====================================================================================
    # Q9 (q-549): x = 1 was lucky - say when to try a second number
    M.edit_lines('solve-q-549', 3, lambda ls: ls[:-1] + [
        {'say': "One warning. Zero or one can make a false rule look true. Here only choice one failed, so we're done."},
        {'say': "If two choices had survived, we'd try a second number, like two."},
        ls[-1]])
    _replace_say(M, 'solve-q-549', 2, "So on the exam: skip it, solve the rest of the section, and come back at the end.",
                 ["It's a must-be-true question — \"not always true\" means one choice can be broken.",
                  "So on the exam: skip it, solve the rest of the section, and come back at the end."])

    # Q12 (q-552): don't suggest stopping halfway without saying why
    M.set_slide('solve-q-552', 3, script=[
        "Now the recommended route: plug in a number.",
        "All the choices are plain numbers — so one substitution is enough. a is positive: take a equals one.",
        D('Write "◆(1, 1) = √(3 + 1) = 2"'),
        "Diamond of one, one: root of four. Two.",
        D('Top: write "◆(2, 1) = √(12 + 1) = √13"'),
        "Top: diamond of two and one. Two is in the first slot — it gets squared and tripled. Twelve plus one: root thirteen.",
        "Only choice two has thirteen on top. A strong hint — but one more line makes it sure.",
        D('Bottom: write "◆(1, 2) = √(3 + 4) = √7"'),
        "Bottom: diamond of one and two. Now two is in the second slot. Three plus four: root seven.",
        D('Write "√13 / √7 = √(13/7)" and circle choice 2'),
        "Root thirteen over root seven. Choice two.",
        "In operation questions with unknowns, plugging in is the recommended way.",
    ])

    # Q13 (q-553): a sound insight instead of "same power on both letters"
    M.set_slide('solve-q-553', 3, script=[
        "For students who see the algebra: the same two letters, just swapped.",
        "Top of the definition: x minus y, squared. a minus b and b minus a are opposites — and squared, they're equal.",
        D('Write "(a − b)² = (b − a)²"'),
        "So the tops cancel completely. Only the bottoms are left — and dividing flips the second one.",
        D('Write "= (b²a) / (a²b) = b/a"'),
        "b squared a, over a squared b. One a and one b cancel: b over a. One line.",
        D('Circle choice 2'),
        "Choice two.",
    ])
    _fix_draw(M, 'solve-q-553', 4, '(1/2) : (1/4) = 2', '(1/2) ÷ (1/4) = 2')

    # Q15 (q-555): no T11 slang
    _replace_say(M, 'solve-q-555', 2, "One over a, divided by one over b: b over a — not a over b. A negative power flips floors.",
                 "One over a, divided by one over b: b over a — not a over b. Dividing by a fraction is multiplying by its reciprocal.")
    _replace_say(M, 'solve-q-555', 2, "They ask what's NECESSARILY true for every positive a and b. We test each choice.",
                 "They ask what MUST be true for every positive a and b. We try to break each choice.")

    # Q16 (q-556): x = 1 is risky - say why it is safe here
    M.edit_lines('solve-q-556', 2, lambda ls: ls + [
        {'say': "One is a risky number — it can make a false rule look true. But here three choices failed and only one survived. Safe."}])

    # =====================================================================================
    # 4. Existing questions: TeX, no colons, stacked conditions, clear wording
    # =====================================================================================
    S('q-541', stem='The operation $\\blacklozenge$ is defined for every number $a$: $\\blacklozenge(a)=a^2-2a$. $\\blacklozenge(5)=?$',
      expl=['Substitute $a=5$ into the definition: $\\blacklozenge(5)=5^2-2\\cdot5=25-10=15$.',
            'Faster: factor first. $a^2-2a=a(a-2)$, so $\\blacklozenge(5)=5\\cdot3=15$.'])
    S('q-542', stem='The operation $\\blacklozenge$ is defined for every number $x$: $\\blacklozenge(x)=x^2$. $\\blacklozenge(\\blacklozenge(2))=?$',
      expl=['Work from the inside out: $\\blacklozenge(2)=2^2=4$.',
            'Then $\\blacklozenge(\\blacklozenge(2))=\\blacklozenge(4)=4^2=16$.',
            'Stopping at $4$ is the trap.'])
    S('q-543', stem='Given: $\\blacklozenge(2)=10$. Which of the following cannot be the definition of the operation $\\blacklozenge$?',
      expl=['Put $x=2$ into each choice. A choice that does not give $10$ cannot be the definition.',
            '(1) $2^3+2=10$ ✓. (2) $4\\cdot2+3=11$ ✗. (3) $2\\cdot(2\\cdot2+1)=2\\cdot5=10$ ✓. (4) $6\\cdot2-2=10$ ✓.',
            'Only choice (2) fails.'])
    S('q-544', stem='The operation $\\blacklozenge$ is defined for every number $x$: $\\blacklozenge(3x)=x+4$. $\\blacklozenge(12)=?$',
      expl=['The input of $\\blacklozenge$ is $3x$, not $x$. So find the $x$ with $3x=12$: $x=4$.',
            'Then $\\blacklozenge(12)=x+4=4+4=8$.',
            'The trap: putting $12$ straight into $x+4$ gives $16$.'])
    S('q-545', stem='The operation $\\blacklozenge$ is defined for every integer $x$:\n' + PIECE +
      '\n$\\blacklozenge(\\blacklozenge(\\blacklozenge(5)))=?$',
      expl=['$5$ is odd: $\\blacklozenge(5)=2\\cdot5=10$.',
            '$10$ is even: $\\blacklozenge(10)=10^2-7=93$.',
            '$93$ is odd: $\\blacklozenge(93)=2\\cdot93=186$.',
            'Check odd or even again before every step.'])
    S('q-546', stem='The operation $\\blacklozenge$ is defined for every even integer $x\\ge0$:\n'
      '$\\blacklozenge(x)=\\begin{cases} 0, & x=0 \\\\ 7-\\blacklozenge(x-2), & x\\ge2 \\end{cases}$\n$\\blacklozenge(6)=?$',
      expl=['Go down to the start value: $\\blacklozenge(6)=7-\\blacklozenge(4)$, $\\blacklozenge(4)=7-\\blacklozenge(2)$, $\\blacklozenge(2)=7-\\blacklozenge(0)$, and $\\blacklozenge(0)=0$.',
            'Climb back up: $\\blacklozenge(2)=7-0=7$, $\\blacklozenge(4)=7-7=0$, $\\blacklozenge(6)=7-0=7$.',
            'The values go $0, 7, 0, 7$ — they switch back and forth.'])
    S('q-547', stem='The operation $\\blacklozenge$ is defined for every positive integer $x$:\n'
      '$\\blacklozenge(x)=\\begin{cases} 6, & x=1 \\\\ \\blacklozenge(x-1), & x>1 \\end{cases}$\n$\\blacklozenge(5)=?$',
      expl=['$\\blacklozenge(5)=\\blacklozenge(4)=\\blacklozenge(3)=\\blacklozenge(2)=\\blacklozenge(1)=6$.',
            'Each value copies the one below it, so the start value $6$ passes all the way up.'])
    S('q-548', stem='For every number $x$: $3\\cdot\\blacklozenge(x)-4x=10+2\\cdot\\blacklozenge(x)$. $\\blacklozenge(3)=?$',
      expl=['Treat $\\blacklozenge(x)$ as one unknown and isolate it: $3\\cdot\\blacklozenge(x)-2\\cdot\\blacklozenge(x)=10+4x$, so $\\blacklozenge(x)=4x+10$.',
            'Then $\\blacklozenge(3)=4\\cdot3+10=22$.'])
    S('q-549', stem='For every number $t$: $\\blacklozenge(t)=t^2$. In the choices, $x\\ge0$. Which of the following is not always true?',
      expl=['(1) $\\blacklozenge(3x)=(3x)^2=9x^2$, but $3\\cdot\\blacklozenge(x)=3x^2$. With $x=1$: $9\\ne3$. Not always true — this is the answer.',
            '(2) $\\blacklozenge(\\sqrt x)=(\\sqrt x)^2=x$, so $\\blacklozenge(\\blacklozenge(\\sqrt x))=\\blacklozenge(x)$. Always true.',
            '(3) $\\blacklozenge(4x)=(4x)^2=16x^2=16\\cdot\\blacklozenge(x)$. Always true.',
            '(4) Opposite numbers have the same square, so $(x-5)^2=(5-x)^2$. Always true.',
            'Plugging in? Do not use $x=0$: with $x=0$ every choice looks true.'])
    S('q-550', stem='For every three numbers $x$, $y$, $z$: $\\blacklozenge(x, y, z)=x^{yz}+y^{xz}+z^{xy}$. $\\blacklozenge(1, 1, \\blacklozenge(1, 2, 2))=?$',
      expl=['Inner operation first, with $x=1$, $y=2$, $z=2$: $\\blacklozenge(1, 2, 2)=1^{4}+2^{2}+2^{2}=1+4+4=9$.',
            'Outer operation, with $x=1$, $y=1$, $z=9$: $\\blacklozenge(1, 1, 9)=1^{9}+1^{9}+9^{1}=1+1+9=11$.'])
    S('q-551', stem='For every two numbers $x$ and $y$, two operations are defined:\n'
      '$\\begin{cases} \\blacklozenge(x, y)=x^2-2xy+y^2 \\\\ \\#(x, y)=x^2+2xy+y^2 \\end{cases}$\n$\\#(\\blacklozenge(9, 6), \\blacklozenge(8, 6))=?$',
      expl=['Recognize the square formulas: $\\blacklozenge(x, y)=(x-y)^2$ and $\\#(x, y)=(x+y)^2$.',
            '$\\blacklozenge(9, 6)=(9-6)^2=9$ and $\\blacklozenge(8, 6)=(8-6)^2=4$.',
            '$\\#(9, 4)=(9+4)^2=13^2=169$.'])
    S('q-552', stem='For every two numbers $x$ and $y$: $\\blacklozenge(x, y)=\\sqrt{3x^2+y^2}$. Given: $a>0$. '
      '$\\frac{\\blacklozenge(\\blacklozenge(a, a), a)}{\\blacklozenge(a, \\blacklozenge(a, a))}=?$',
      expl=['Inner: $\\blacklozenge(a, a)=\\sqrt{3a^2+a^2}=\\sqrt{4a^2}=2a$.',
            'Top: $2a$ goes into the FIRST slot: $\\blacklozenge(2a, a)=\\sqrt{3\\cdot4a^2+a^2}=\\sqrt{13a^2}=a\\sqrt{13}$.',
            'Bottom: $2a$ goes into the SECOND slot: $\\blacklozenge(a, 2a)=\\sqrt{3a^2+4a^2}=\\sqrt{7a^2}=a\\sqrt7$.',
            '$\\frac{a\\sqrt{13}}{a\\sqrt7}=\\sqrt{\\frac{13}{7}}$.',
            'Or plug in $a=1$: $\\frac{\\blacklozenge(2, 1)}{\\blacklozenge(1, 2)}=\\frac{\\sqrt{13}}{\\sqrt7}$.'])
    S('q-553', stem='For every two numbers $x$ and $y$ that are not $0$: $\\blacklozenge(x, y)=\\frac{(x-y)^2}{x^2y}$. '
      'Given: $a$ and $b$ are two different numbers, and neither of them is $0$. $\\frac{\\blacklozenge(a, b)}{\\blacklozenge(b, a)}=?$',
      expl=['$\\blacklozenge(a, b)=\\frac{(a-b)^2}{a^2b}$ and $\\blacklozenge(b, a)=\\frac{(b-a)^2}{b^2a}$.',
            'The tops are equal, because $(b-a)^2=(a-b)^2$. They cancel:',
            '$\\frac{(a-b)^2}{a^2b}\\cdot\\frac{b^2a}{(a-b)^2}=\\frac{b^2a}{a^2b}=\\frac{b}{a}$.',
            'Check with $a=1$, $b=2$: $\\blacklozenge(1, 2)=\\frac12$ and $\\blacklozenge(2, 1)=\\frac14$, and $\\frac12\\div\\frac14=2=\\frac{b}{a}$ ✓.'])
    S('q-554', stem='$A$, $B$ and $C$ are digits from $1$ to $9$. For every three-digit number $ABC$, the operation $\\blacklozenge$ is defined: '
      '$\\blacklozenge(ABC)=A^4+B^3+C^2$. Which of the following is the smallest?',
      expl=['$\\blacklozenge(123)=1^4+2^3+3^2=1+8+9=18$.',
            '$\\blacklozenge(213)=2^4+1^3+3^2=16+1+9=26$.',
            '$\\blacklozenge(321)=3^4+2^3+1^2=81+8+1=90$.',
            '$\\blacklozenge(132)=1^4+3^3+2^2=1+27+4=32$.',
            'The smallest is $\\blacklozenge(123)=18$: the biggest power goes on the smallest digit.'])
    S('q-555', stem='For every number $x\\ne0$: $\\blacklozenge(x)=\\frac1x$. Which of the following must be true for all positive $a$ and $b$?',
      expl=['(4) $\\blacklozenge(a)\\cdot a=\\frac1a\\cdot a=1$ and $\\blacklozenge(b)\\cdot b=\\frac1b\\cdot b=1$. Both sides are always $1$ ✓.',
            '(1) $a=\\frac12$ gives $\\blacklozenge(a)=2$, which is not less than $1$ ✗.',
            '(2) $\\frac{\\blacklozenge(a)}{\\blacklozenge(b)}=\\frac1a\\div\\frac1b=\\frac1a\\cdot b=\\frac{b}{a}$, not $\\frac{a}{b}$ ✗ (for example $a=1$, $b=2$).',
            '(3) A bigger denominator gives a smaller fraction: $\\frac1a>\\frac1{a+2}$. For example $a=1$: $1>\\frac13$ ✗.'])
    S('q-556', stem='For every positive integer $x$, ⟦$x$⟧ is the number of times $3$ appears in the prime factorization of $x$. '
      'For example, $18=2\\cdot3\\cdot3$ has two 3s, so ⟦$18$⟧ is $2$. Which of the following must be true?',
      choices=['⟦$x+3$⟧ $=$ ⟦$x$⟧ $+1$', '⟦$3x$⟧ $=$ ⟦$x$⟧ $+1$', '⟦$3x$⟧ $=$ ⟦$x^2$⟧', '⟦$3x$⟧ $=3\\cdot$ ⟦$x$⟧'],
      expl=['Multiplying $x$ by $3$ adds exactly one more $3$ to its prime factorization. So ⟦$3x$⟧ $=$ ⟦$x$⟧ $+1$ always ✓.',
            'For example $x=18$: $54=2\\cdot3^3$, so ⟦$54$⟧ $=3=2+1$.',
            'The others break: (1) $x=3$: ⟦$6$⟧ $=1$, but ⟦$3$⟧ $+1=2$ ✗. (3) $x=2$: ⟦$6$⟧ $=1$, but ⟦$4$⟧ $=0$ ✗. (4) $x=3$: ⟦$9$⟧ $=2$, but $3\\cdot$ ⟦$3$⟧ $=3$ ✗.'])
    S('q-557', stem='For all $a$ and $b$ with $a\\ge b\\ge0$: $\\blacklozenge(a, b)=\\sqrt{\\sqrt a-\\sqrt b}$. $\\frac{\\blacklozenge(100, 36)}{\\blacklozenge(64, 49)}=?$',
      expl=['$\\blacklozenge(100, 36)=\\sqrt{\\sqrt{100}-\\sqrt{36}}=\\sqrt{10-6}=\\sqrt4=2$.',
            '$\\blacklozenge(64, 49)=\\sqrt{\\sqrt{64}-\\sqrt{49}}=\\sqrt{8-7}=\\sqrt1=1$.',
            '$\\frac21=2$.'])
    S('q-558', stem='For every two different numbers $x$ and $y$, two operations are defined:\n'
      '$\\blacklozenge(x, y)$ = the smaller of $x$ and $y$\n$\\#(x, y)$ = the larger of $x$ and $y$\n'
      '$\\#(\\blacklozenge(9, 6), \\blacklozenge(10, 3))=?$',
      expl=['$\\blacklozenge(9, 6)=6$ (the smaller) and $\\blacklozenge(10, 3)=3$.',
            'Then $\\#(6, 3)=6$ (the larger).'])
    S('q-559', stem='For every two numbers $x$ and $y$: $\\blacklozenge(x, y)=\\sqrt{x^2+y^2}$. $\\blacklozenge(\\blacklozenge(3, 2), 6)=?$',
      expl=['Inner: $\\blacklozenge(3, 2)=\\sqrt{9+4}=\\sqrt{13}$.',
            'Outer: $\\blacklozenge(\\sqrt{13}, 6)=\\sqrt{(\\sqrt{13})^2+6^2}=\\sqrt{13+36}=\\sqrt{49}=7$.'])
    S('q-560', stem='For every number $x$: $\\blacklozenge(x)=x(x-2)$. $\\blacklozenge(\\blacklozenge(3))=?$',
      expl=['Inner: $\\blacklozenge(3)=3\\cdot(3-2)=3\\cdot1=3$.',
            'Outer: $\\blacklozenge(3)=3$ again. The operation sends $3$ back to $3$.'])
    S('q-561', stem='For every positive integer $a$: $\\blacklozenge(a)=\\frac{a}{a+1}$. '
      '$\\blacklozenge(1)\\cdot\\blacklozenge(2)\\cdot\\blacklozenge(3)\\cdot\\blacklozenge(4)\\cdot\\blacklozenge(5)=?$',
      expl=['$\\frac12\\cdot\\frac23\\cdot\\frac34\\cdot\\frac45\\cdot\\frac56$.',
            'Each top cancels the bottom before it: $2$, $3$, $4$ and $5$ all cancel. What is left: $\\frac16$.'])
    S('q-562', stem='For every number $x$: $\\blacklozenge(x)=x(x-4)(x+1)$. For how many different values of $x$ is $\\blacklozenge(x)$ equal to $0$?',
      expl=['A product is $0$ exactly when one of its factors is $0$: $x=0$, or $x-4=0$, or $x+1=0$.',
            'So $x=0$, $x=4$ or $x=-1$. Three values.'])
    S('q-563', stem='For every number $a$: $\\blacklozenge(a^2)=|a|$. $\\blacklozenge\\left(\\frac19\\right)=?$',
      expl=['The input is $a^2$. Find $a$ with $a^2=\\frac19$: $a=\\frac13$ or $a=-\\frac13$.',
            'Either way $|a|=\\frac13$. So $\\blacklozenge\\left(\\frac19\\right)=\\frac13$.'])
    S('q-564', stem='For every number $a$: $\\blacklozenge(a)=a^7+a^6+a^5+a^4+a^3+a^2+a+1$. $\\blacklozenge(1)-\\blacklozenge(-1)=?$',
      expl=['$\\blacklozenge(1)$: all $8$ terms are $1$, so $\\blacklozenge(1)=8$.',
            '$\\blacklozenge(-1)=-1+1-1+1-1+1-1+1=0$.',
            '$8-0=8$.',
            'Shortcut: in $\\blacklozenge(1)-\\blacklozenge(-1)$ the even powers and the constant cancel. Only the $4$ odd powers are left, doubled: $2\\cdot4=8$.'])
    S('q-565', stem='For every two numbers $a$ and $b$:\n'
      '$a\\blacklozenge b=\\begin{cases} \\frac{a+b}{a-b}, & a\\ne b \\\\ 0, & a=b \\end{cases}$\n$(4\\blacklozenge2)\\blacklozenge3=?$',
      expl=['Inner: $4\\ne2$, so $4\\blacklozenge2=\\frac{4+2}{4-2}=\\frac62=3$.',
            'Outer: $3\\blacklozenge3$ has $a=b$, so the second rule gives $0$.'])
    S('q-566', stem='For every number $x$: $\\blacklozenge(x)+6=8x-\\blacklozenge(x)$. $\\blacklozenge(2)=?$',
      expl=['Collect the $\\blacklozenge(x)$ terms: $2\\cdot\\blacklozenge(x)=8x-6$, so $\\blacklozenge(x)=4x-3$.',
            '$\\blacklozenge(2)=4\\cdot2-3=5$.'])
    S('q-567', stem='For two positive integers $x$ and $y$, $x\\sim y$ is the number you get when you write the digits of $x$ '
      'and then the digits of $y$. For example: $45\\sim12=4512$. '
      'Which of the following is not always true for positive integers $x$, $y$ and $z$?',
      choices=['$x<5\\sim x$', '$x\\sim1=10x+1$', '$(x\\sim y)\\sim z=x\\sim(y\\sim z)$', '$x\\sim y=y\\sim x$'],
      expl=['One counterexample is enough: $45\\sim12=4512$, but $12\\sim45=1245$. So (4) is not always true.',
            'The others are always true. (1) $5\\sim x$ has one more digit than $x$, so it is bigger. '
            '(2) Writing the digit $1$ after $x$ moves every digit of $x$ one place to the left and adds $1$: for example $37\\sim1=371=10\\cdot37+1$. '
            '(3) Both sides are the digits of $x$, then $y$, then $z$, in that order.'])
    S('q-568', stem='For every number $x$: $\\blacklozenge(x)=x^4+5x^2+6x-9$. $\\blacklozenge(4)-\\blacklozenge(-4)=?$',
      expl=['$\\blacklozenge(4)=256+80+24-9=351$ and $\\blacklozenge(-4)=256+80-24-9=303$.',
            '$351-303=48$.',
            'Shortcut: the even powers and the constant are the same for $4$ and $-4$, so they cancel. Only $6x$ is left, doubled: $2\\cdot6\\cdot4=48$.'])
    S('q-569', stem='For every positive integer $n$:\n'
      '$\\blacklozenge(n)=\\begin{cases} 4, & n=1 \\\\ \\blacklozenge(n-1)+2, & n>1 \\end{cases}$\n$\\blacklozenge(6)=?$',
      expl=['Climb up from the start value: $\\blacklozenge(1)=4$, $\\blacklozenge(2)=6$, $\\blacklozenge(3)=8$, $\\blacklozenge(4)=10$, $\\blacklozenge(5)=12$, $\\blacklozenge(6)=14$.',
            'Or: five steps of $+2$ above the start value: $4+5\\cdot2=14$.'])
    S('q-570', stem='For every number $x$, two operations are defined:\n'
      '$\\begin{cases} \\blacklozenge(x)=x+3 \\\\ \\#(x)=x^2 \\end{cases}$\nGiven: $\\blacklozenge(\\#(a))=\\#(\\blacklozenge(a))$. $a=?$',
      choices=['$-1$', '$\\frac12$', '$-\\frac12$', '$0$'],
      expl=['Left side: $\\blacklozenge(\\#(a))=\\blacklozenge(a^2)=a^2+3$.',
            'Right side: $\\#(\\blacklozenge(a))=\\#(a+3)=(a+3)^2=a^2+6a+9$.',
            '$a^2+3=a^2+6a+9$, so $6a=-6$ and $a=-1$.',
            'Check: $\\blacklozenge(\\#(-1))=\\blacklozenge(1)=4$ and $\\#(\\blacklozenge(-1))=\\#(2)=4$ ✓.'])
    S('q-571', stem='For every integer $x$ from $1$ to $9$, $\\blacklozenge(x)$ is the number of two-digit numbers whose tens digit is $x$ '
      'and whose units digit is smaller than $x$. $\\blacklozenge(x)=?$',
      choices=['$x$', '$x-1$', '$10-x$', '$x+1$'],
      expl=['Examples first. $x=3$: the numbers $30$, $31$, $32$. Three numbers, so $\\blacklozenge(3)=3$.',
            'In general, the units digit can be $0, 1, \\ldots, x-1$: that is $x$ digits. So $\\blacklozenge(x)=x$.'])
    S('q-572', stem='For every two integers $a$ and $b$ that are not $0$: $\\blacklozenge(a, b)=\\frac{a}{b}-\\frac{b}{a}$. $\\blacklozenge(-1, 2)=?$',
      expl=['$\\blacklozenge(-1, 2)=\\frac{-1}{2}-\\frac{2}{-1}=-\\frac12+2=\\frac32$.',
            'Now the choices: $\\blacklozenge(2, 1)=2-\\frac12=\\frac32$ ✓.',
            'The others: $\\blacklozenge(1, 2)=\\frac12-2=-\\frac32$, $\\blacklozenge(-2, 1)=-2+\\frac12=-\\frac32$, $\\blacklozenge(2, -1)=-2+\\frac12=-\\frac32$.'])
    S('q-573', stem='For every number $x\\ne0$: $\\blacklozenge(x)=\\frac{x-2}{x}$. Which of the following must be true for all $a>2$ and $b>2$?',
      expl=['Rewrite: $\\blacklozenge(x)=1-\\frac2x$. For $x>2$, $0<\\frac2x<1$, so $0<\\blacklozenge(x)<1$.',
            '(1) Two numbers between $0$ and $1$ have a product smaller than $1$. Always true ✓.',
            '(2) As $x$ grows, $\\frac2x$ shrinks, so $\\blacklozenge(x)$ grows: $a<b$ gives $\\blacklozenge(a)<\\blacklozenge(b)$. The claim is the reverse ✗.',
            '(3) $a=4$: $2\\cdot\\blacklozenge(4)=2\\cdot\\frac12=1$, but $\\blacklozenge(8)=\\frac34$ ✗.',
            '(4) $a=4$: $(\\blacklozenge(4))^2=\\frac14$, but $\\blacklozenge(16)=\\frac78$ ✗.'])
    S('q-574', stem='For every number $x$: $\\blacklozenge(x)=x^2-4$. Given: $a>0$ and $b>0$. Which of the following must be true?',
      expl=['(4) Left side: $\\sqrt{a^2-4+4}=\\sqrt{a^2}=a$ ($a$ is positive). Right side: $\\frac{a^2-4}{a+2}+2=\\frac{(a-2)(a+2)}{a+2}+2=a-2+2=a$. Always equal ✓.',
            '(1) $a=3$: $\\blacklozenge(3)=5$ and $\\blacklozenge(5)=21\\ne3$ ✗.',
            '(2) $a=b=1$: $\\blacklozenge(2)=0$, but $\\blacklozenge(1)+\\blacklozenge(1)=-6$ ✗.',
            '(3) $b=9$: $\\blacklozenge(9)=77$, but $(9-2)\\cdot\\blacklozenge(3)=7\\cdot5=35$ ✗.'])
    S('q-575', stem='For every number $x$: $\\blacklozenge(x)=(x-3)(x+2)$. For how many values of $a$ is $\\blacklozenge(a)$ equal to $\\blacklozenge(a+5)$?',
      choices=['$1$', '$2$', '$3$', 'Infinitely many'],
      expl=['$\\blacklozenge(a)=(a-3)(a+2)=a^2-a-6$.',
            '$\\blacklozenge(a+5)=(a+5-3)(a+5+2)=(a+2)(a+7)=a^2+9a+14$.',
            '$a^2-a-6=a^2+9a+14$: the $a^2$ cancels, so $-20=10a$ and $a=-2$. Exactly one value.'])
    S('q-576', stem='For every two positive integers $a$ and $b$, $\\blacklozenge(a, b)$ is the remainder when $a$ is divided by $b$. '
      '$\\blacklozenge(\\blacklozenge(47, 9), \\blacklozenge(11, 4))=?$',
      expl=['$47=5\\cdot9+2$, so $\\blacklozenge(47, 9)=2$.',
            '$11=2\\cdot4+3$, so $\\blacklozenge(11, 4)=3$.',
            '$\\blacklozenge(2, 3)$: $2=0\\cdot3+2$, so the remainder is $2$.'])

    X = 'alg-extra-unit-t19-3-'
    S(X + '1', stem='For every two numbers $a$ and $b$: $a\\star b=2a-b$. $3\\star5=?$', choices=['$8$', '$1$', '$-7$', '$11$'],
      expl=['$3$ goes into $a$ and $5$ into $b$: $3\\star5=2\\cdot3-5=1$.'])
    S(X + '2', stem='For every two numbers $a$ and $b$: $a\\star b=a+b+ab$. $2\\star3=?$', choices=['$11$', '$5$', '$6$', '$10$'],
      expl=['$2\\star3=2+3+2\\cdot3=5+6=11$.'])
    S(X + '4', stem='For every two numbers $a$ and $b$: $a\\diamond b=3a+b$. Which of the following is true for all numbers $a$ and $b$?',
      expl=['$a\\diamond b=3a+b$ and $b\\diamond a=3b+a$.',
            '$a\\diamond b-b\\diamond a=(3a+b)-(3b+a)=2a-2b=2(a-b)$ ✓.',
            'The others break with $a=1$, $b=2$: $1\\diamond0=3\\ne0$; $1\\diamond2=5$ but $2\\diamond1=7$; $1+3\\cdot2=7\\ne5$.'])
    S(X + '5', stem='Given:\n$\\begin{cases} G(x)=2x+5 \\text{ for every number } x \\\\ G(t)=19 \\end{cases}$\n$t=?$', choices=['$8$', '$12$', '$7$', '$5$'],
      expl=['$2t+5=19$, so $2t=14$ and $t=7$.'])
    S(X + '7', stem='For every two numbers $a$ and $b$: $a\\circ b=(a-b)^2$. $(-2)\\circ3=?$', choices=['$1$', '$5$', '$-25$', '$25$'],
      expl=['$(-2)\\circ3=(-2-3)^2=(-5)^2=25$.'])
    # near-duplicates of Q2 / q-560 (nested one-letter operations)
    M.unplace(X + '3')
    M.unplace(X + '6')

    # =====================================================================================
    # 5. New guided questions (+ solution videos)
    # =====================================================================================
    g = ['q-r26-t19-%02d' % k for k in range(1, 6)]

    # G1 - brackets on an expression input; plug-in: 0 lets two choices survive
    M.new_q(g[0], TOPIC, 'For every number $x$: $\\blacklozenge(x)=x^2-2x$. $\\blacklozenge(x+1)=?$',
            ['$x^2-2x+1$', '$x^2-1$', '$x^2-2x-1$', '$x^2+3$'], 2, [
        'Put $x+1$ where $x$ was — in brackets, every time: $\\blacklozenge(x+1)=(x+1)^2-2(x+1)$.',
        'Open the brackets: $x^2+2x+1-2x-2=x^2-1$.',
        'Check with $x=2$: $\\blacklozenge(3)=9-6=3$, and $2^2-1=3$ ✓.',
        'The traps: $\\blacklozenge(x)+1=x^2-2x+1$ (choice 1), $(x+1)^2$ written as $x^2+1$ (choice 3), and $-2(x+1)$ written as $-2x+2$ (choice 4).'])
    M.place_q(g[0], THEORY, after='solve-q-543')
    _solution(M, g[0], 'theory', ["This time the input is an expression: x plus one."], [
        ('Method 1 · Brackets', [
            "The rule works on x. Now x plus one goes in — the whole thing, in brackets.",
            D('Write "◆(x + 1) = (x + 1)² − 2(x + 1)"'),
            "x plus one, squared. Minus two times x plus one.",
            D('Write "= x² + 2x + 1 − 2x − 2"'),
            "Open the brackets. x plus one squared: x squared plus two x plus one. Minus two times x plus one: minus two x, minus two.",
            D('Write "= x² − 1" and circle choice 2'),
            "Two x minus two x: gone. One minus two: minus one. x squared minus one. Choice two.",
            "The other choices are the traps: no brackets, or a lost minus.",
        ]),
        ('Method 2 · Plug in', [
            "Letters in the choices? Plug in a number. Let's try zero — it's easy.",
            D('Write "x = 0: ◆(1) = 1 − 2 = −1"'),
            "x is zero, so the input is one. One minus two: minus one.",
            D('Next to the choices write "1, −1, −1, 3"'),
            "The choices with x equals zero: one, minus one, minus one, three. Two choices survive!",
            "Zero is a lazy number — it wipes out whole terms. Try a second number: two.",
            D('Write "x = 2: ◆(3) = 9 − 6 = 3"; next to the choices write "1, 3, −1, 7"'),
            "Now the input is three. Nine minus six: three. The choices: one, three, minus one, seven.",
            D('Circle choice 2'),
            "Only choice two. Two choices left after one number? Always try a second one.",
        ]),
    ])

    # G2 - "always a*b = b*a?": one counterexample vs. algebra
    M.new_q(g[1], TOPIC, 'For which of the following operations is $a\\star b=b\\star a$ for all numbers $a$ and $b$?',
            ['$a\\star b=a^2b$', '$a\\star b=a(a+b)$', '$a\\star b=ab+a+b$', '$a\\star b=(a-b)^2+a$'], 3, [
        'To show "not always", one counterexample is enough. Take $a=1$ and $b=2$ (different, and not $0$).',
        '(1) $1\\star2=1^2\\cdot2=2$, but $2\\star1=2^2\\cdot1=4$ ✗.',
        '(2) $1\\star2=1\\cdot3=3$, but $2\\star1=2\\cdot3=6$ ✗.',
        '(4) $1\\star2=(1-2)^2+1=2$, but $2\\star1=(2-1)^2+2=3$ ✗.',
        '(3) To show "always", swap the letters in the algebra: $b\\star a=ba+b+a=ab+a+b=a\\star b$ ✓.',
        'Do not test with $a=b$: then both sides are $a\\star a$ for every operation.'])
    M.place_q(g[1], THEORY, after='solve-' + g[0])
    _solution(M, g[1], 'theory', ["Does the order of the inputs matter?"], [
        ('Method 1 · One counterexample', [
            "They ask: for which operation is a star b ALWAYS equal to b star a?",
            "To knock a choice out, one counterexample is enough. Take a equals one, b equals two.",
            "Not equal numbers — with a equals b, every operation looks fine.",
            D('Next to choice 1 write "1 ⋆ 2 = 2,  2 ⋆ 1 = 4 ✗"'),
            "Choice one: one squared times two is two. Two squared times one is four. Out.",
            D('Next to choice 2 write "1 ⋆ 2 = 3,  2 ⋆ 1 = 6 ✗"'),
            "Choice two: one times three is three. Two times three is six. Out.",
            D('Next to choice 4 write "1 ⋆ 2 = 2,  2 ⋆ 1 = 3 ✗"'),
            "Choice four: one plus one is two. One plus two is three. Out.",
            D('Circle choice 3'),
            "Choice three survives. Choice three.",
        ]),
        ('Method 2 · Swap the letters', [
            "Why is choice three always true? Numbers can't prove always. Algebra can.",
            D('Write "b ⋆ a = ba + b + a"'),
            "Swap the letters: b times a, plus b, plus a.",
            D('Write "= ab + a + b = a ⋆ b ✓"'),
            "b times a is a times b. And b plus a is a plus b. Exactly the same.",
            "So: not always — one example. Always — swap the letters.",
        ]),
    ])

    # G3 - conditions backwards: try both rules, reject answers that don't fit their rule
    M.new_q(g[2], TOPIC, 'The operation $\\blacklozenge$ is defined for every positive integer $x$:\n'
            '$\\blacklozenge(x)=\\begin{cases} 3x, & x \\text{ odd} \\\\ x^2-12, & x \\text{ even} \\end{cases}$\n'
            'Given: $\\blacklozenge(x)=24$. $x=?$',
            ['$8$', '$6$', '$6$ or $8$', 'There is no such $x$.'], 2, [
        'Try both rules, then check that each answer fits the rule it used.',
        'Odd rule: $3x=24$, so $x=8$. But $8$ is even, so it does not use the odd rule. Rejected.',
        'Even rule: $x^2-12=24$, so $x^2=36$ and $x=6$ ($x$ is positive). $6$ is even ✓.',
        'Check: $\\blacklozenge(6)=36-12=24$ ✓, but $\\blacklozenge(8)=64-12=52$. So $x=6$.'])
    M.place_q(g[2], THEORY, after='solve-q-545')
    _solution(M, g[2], 'theory', ["Conditions again — but backwards. They give the result."], [
        ('Method 1 · Try both rules', [
            "We don't know if x is odd or even. So try both rules.",
            D('Write "odd: 3x = 24 → x = 8"'),
            "Odd rule: three x is twenty-four, so x is eight.",
            D('Next to it write "8 is even ✗"'),
            "But wait — eight is even! An even number never uses the odd rule. Throw it out.",
            D('Write "even: x² − 12 = 24 → x² = 36 → x = 6 ✓"'),
            "Even rule: x squared is thirty-six. x is positive, so x is six. Six is even — it fits.",
            D('Circle choice 2'),
            "Choice two. And the trap is waiting: eight, and six or eight.",
        ]),
        ('Method 2 · Work back from the answers', [
            "Or put the choices into the operation.",
            D('Write "◆(8): 8 even → 64 − 12 = 52 ✗"'),
            "Eight is even: sixty-four minus twelve, fifty-two. Not twenty-four.",
            D('Write "◆(6): 6 even → 36 − 12 = 24 ✓"'),
            "Six is even: thirty-six minus twelve, twenty-four. Found it.",
            "Working back checks the condition for you — no fake answers.",
        ]),
    ])

    # G4 - definition in words: the integer part
    M.new_q(g[3], TOPIC, 'For every number $x$, $[x]$ is the largest integer that is not bigger than $x$. '
            'For example: $[3.7]=3,\\ \\ [5]=5$.\n$[-2.5]+[2.5]+[0.5]=?$',
            ['$2$', '$0$', '$-1$', '$1$'], 3, [
        'Examples first. For a positive number, drop the decimal part: $[2.5]=2$ and $[0.5]=0$.',
        'Negative numbers are the trap. $-2$ is bigger than $-2.5$, so it is not allowed. The largest integer not bigger than $-2.5$ is $-3$. So $[-2.5]=-3$.',
        '$-3+2+0=-1$.',
        'The trap answer $0$ comes from $[-2.5]=-2$.'])
    M.place_q(g[3], THEORY, after='solve-q-548')
    _solution(M, g[3], 'theory', ["A definition in words. Examples first."], [
        ('Examples first', [
            "The largest integer that is not bigger than x. Let's make it concrete.",
            D('Write "[3.7] = 3, [5] = 5"'),
            "They gave two examples: three point seven gives three. Five gives five.",
            D('Write "[2.5] = 2, [0.5] = 0"'),
            "Same for ours: two point five gives two. Zero point five gives zero.",
            "For a positive number, just drop the decimal part.",
        ]),
        ('The negative trap', [
            "Now minus two point five. Drop the decimals — minus two? Careful.",
            D('Draw a number line: −3, −2.5, −2'),
            "On the number line, minus two is to the RIGHT of minus two point five. It's bigger. Not allowed.",
            D('Write "[−2.5] = −3"'),
            "The largest integer not bigger than minus two point five is minus three.",
            D('Write "−3 + 2 + 0 = −1" and circle choice 3'),
            "Minus three plus two plus zero: minus one. Choice three.",
            "Choice two, zero, is exactly the trap: minus two instead of minus three.",
        ]),
    ])

    # G5 (advanced) - opposite inputs: only odd powers survive in f(k) - f(-k)
    M.new_q(g[4], TOPIC, 'For every number $x$: $\\blacklozenge(x)=x^5+3x^4-2x^3+x^2+4x-7$. $\\blacklozenge(2)-\\blacklozenge(-2)=?$',
            ['$0$', '$24$', '$48$', '$90$'], 3, [
        'Full calculation: $\\blacklozenge(2)=32+48-16+4+8-7=69$ and $\\blacklozenge(-2)=-32+48+16+4-8-7=21$. $69-21=48$.',
        'Shortcut: an even power, and the constant, give the same value for $2$ and $-2$, so they cancel in the subtraction. An odd power only changes its sign, so it is doubled.',
        'Only the odd terms are left: $2\\cdot(2^5-2\\cdot2^3+4\\cdot2)=2\\cdot(32-16+8)=2\\cdot24=48$.',
        'The trap $90$ is $\\blacklozenge(2)+\\blacklozenge(-2)$ — there only the even terms survive: $2\\cdot(48+4-7)=90$.'])
    M.place_q(g[4], ADV, after='solve-q-551')
    _solution(M, g[4], 'advanced', ["A long rule, a number and its opposite. There's a shortcut."], [
        ('Method 1 · Full calculation', [
            "The straight way: calculate both.",
            D('Write "◆(2) = 32 + 48 − 16 + 4 + 8 − 7 = 69"'),
            "Two to the fifth, thirty-two. Three times sixteen, forty-eight. Minus two times eight, minus sixteen. Plus four, plus eight, minus seven. Sixty-nine.",
            D('Write "◆(−2) = −32 + 48 + 16 + 4 − 8 − 7 = 21"'),
            "Minus two: the odd powers turn negative, the even powers stay. Twenty-one.",
            D('Write "69 − 21 = 48" and circle choice 3'),
            "Sixty-nine minus twenty-one: forty-eight. Choice three. It works — but it's slow, and easy to slip.",
        ]),
        ('Method 2 · Only odd powers survive', [
            "Look at each term when you put in two and minus two.",
            D('Write "even power, constant: same → cancel"'),
            "An even power — x to the fourth, x squared — and the plain number: the same for two and for minus two. In the subtraction they cancel.",
            D('Write "odd power: opposite → doubled"'),
            "An odd power just changes its sign. Something minus its opposite is twice that thing.",
            D('Write "2 · (32 − 16 + 8) = 2 · 24 = 48"'),
            "So keep only the odd terms at two: thirty-two, minus sixteen, plus eight. Twenty-four. Doubled: forty-eight.",
            "And with a plus sign instead — the diamond of two plus the diamond of minus two — only the even terms survive. That's the ninety in the choices.",
        ]),
    ])

    # solution-video titles follow the rewritten stems
    for f in M.D['flow']:
        if f['topic'] == TOPIC and f['type'] == 'video' and M.video(f['ref']).get('kind') == 'solution':
            v = M.video(f['ref']); v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']

    # sidebars of the two groups of solution videos (numbers as created; renumber_guided makes them 1, 2, 3 ...)
    for sec in (THEORY, ADV):
        sol = [f['ref'] for f in M.D['flow'] if f['section'] == sec and f['type'] == 'video'
               and M.video(f['ref']).get('kind') == 'solution']
        labels = [M.video(v)['beats'][0]['bigTitle'] for v in sol]
        for v in sol:
            M.set_sidebar(v, labels)
            mine = M.video(v)['beats'][0]['bigTitle']
            for b in M.video(v)['beats'][1:]:
                b['active'] = labels.index(mine)

    # =====================================================================================
    # 6. Memory card
    # =====================================================================================
    c = M.card(CARD)
    c['intro'] = 'Read the definition first. Then follow it exactly.'
    c['tables'] = [{'title': '', 'head': ['Type', 'What to do', 'Example'], 'rows': [
        ['Basic', 'substitute the input for every letter', '$a\\heartsuit b=3(a+b)$: $6\\heartsuit2=24$'],
        ['Negative or expression input', 'every input goes in brackets', '$\\blacklozenge(x)=x^2-2x$: $\\blacklozenge(x+1)=(x+1)^2-2(x+1)$'],
        ['Inside an exercise', 'first turn each operation into a number', '$\\blacklozenge(3)+\\blacklozenge(4)\\ne\\blacklozenge(7)$'],
        ['Nested', 'inside out', '$(2\\star3)\\star1=13\\star1=27$'],
        ['Find the operation', 'put the given input into each choice', '$\\blacklozenge(3)=24$'],
        ['Unknown input', 'equation — or work back from the answers', '$x\\star2=18\\Rightarrow x=7$'],
        ['Always $a\\star b=b\\star a$?', 'not always: one counterexample; always: swap the letters', '$3\\star4\\ne4\\star3$'],
        ['Input is an expression', 'match the whole input first', '$F(4t)$ with $4t=20$'],
        ['Conditions', 'check odd / even at every step', '$\\blacklozenge(3)=6$, $\\blacklozenge(4)=9$'],
        ['Conditions, result given', 'try every rule; keep an answer only if it fits its rule', '$\\blacklozenge(x)=9\\Rightarrow x=4$'],
        ['Circular', 'down to the start value, then back up', '$\\blacklozenge(x)=7-\\blacklozenge(x-2)$'],
        ['Operation on both sides', 'isolate it like an unknown', '$\\blacklozenge(x)=4x+10$'],
        ['Definition in words', 'write 2–3 examples first', '$[3.7]=3$, $[-2.3]=-3$'],
        ['$\\blacklozenge(k)-\\blacklozenge(-k)$', 'only the odd powers are left, doubled', '$x^4+6x$: $2\\cdot6\\cdot4=48$ for $k=4$'],
        ['Must be true', 'skip, come back last, plug in', '$x=2$, then $x=3$'],
    ]}]
    c['tips'] = ['A new operation need not behave like plus: $3\\star4\\ne4\\star3$.',
                 'Plugging in: avoid $0$, $1$ and equal values — they can make a false rule look true. If two choices survive, try a second number.',
                 '"Necessarily true" means "must be true" (Topic 1).']

    # =====================================================================================
    # 7. New practice questions
    # =====================================================================================
    PQ = {}
    PQ['06'] = ('For every number $x$: $\\blacklozenge(x)=x^2+3x$. $\\blacklozenge(-2)=?$', ['$-10$', '$-2$', '$10$', '$2$'], 2, [
        'Brackets on the input: $\\blacklozenge(-2)=(-2)^2+3\\cdot(-2)=4-6=-2$.',
        'The trap: without brackets, $-2^2=-4$, and $-4-6=-10$.'])
    PQ['07'] = ('For every number $x$: $\\blacklozenge(x)=2x^2-x$. $\\blacklozenge(x-1)=?$',
                ['$2x^2-5x+1$', '$2x^2-x-1$', '$2x^2-5x+3$', '$2x^2-3x+3$'], 3, [
        'Brackets on the input: $\\blacklozenge(x-1)=2(x-1)^2-(x-1)$.',
        '$2(x^2-2x+1)-x+1=2x^2-4x+2-x+1=2x^2-5x+3$.',
        'Check with $x=2$: $\\blacklozenge(1)=2-1=1$, and $8-10+3=1$ ✓. The other choices give $-1$, $5$ and $5$.'])
    PQ['08'] = ('For every number $x\\ne1$: $\\blacklozenge(x)=\\frac{x+1}{x-1}$. Given: $x$ is not $0$ and not $1$. $\\blacklozenge\\left(\\frac1x\\right)=?$',
                ['$\\frac{x+1}{x-1}$', '$\\frac{1+x}{1-x}$', '$\\frac{x-1}{x+1}$', '$-1$'], 2, [
        '$\\blacklozenge\\left(\\frac1x\\right)=\\frac{\\frac1x+1}{\\frac1x-1}$. Multiply the top and the bottom by $x$: $\\frac{1+x}{1-x}$.',
        'Check with $x=2$: $\\blacklozenge\\left(\\frac12\\right)=\\frac{1.5}{-0.5}=-3$, and $\\frac{1+2}{1-2}=-3$ ✓. Choice (1) gives $3$, choice (3) gives $\\frac13$.'])
    PQ['09'] = ('Given:\n$\\begin{cases} \\blacklozenge(3)=6 \\\\ \\blacklozenge(5)=20 \\end{cases}$\nWhich of the following could be the definition of $\\blacklozenge$?',
                ['$\\blacklozenge(x)=2x$', '$\\blacklozenge(x)=x^2-3$', '$\\blacklozenge(x)=x(x-1)$', '$\\blacklozenge(x)=3x-3$'], 3, [
        'Put $3$ into each choice: $2\\cdot3=6$, $9-3=6$, $3\\cdot2=6$, $9-3=6$. All four pass — so use the second condition.',
        'Put $5$ in: $2\\cdot5=10$ ✗, $25-3=22$ ✗, $5\\cdot4=20$ ✓, $15-3=12$ ✗.',
        'Only $\\blacklozenge(x)=x(x-1)$ gives both results.'])
    PQ['10'] = ('The operation $\\blacklozenge$ is defined for every positive integer $n$:\n'
                '$\\blacklozenge(n)=\\begin{cases} \\frac n2, & n \\text{ even} \\\\ 3n+1, & n \\text{ odd} \\end{cases}$\n'
                '$\\blacklozenge(\\blacklozenge(\\blacklozenge(\\blacklozenge(6))))=?$',
                ['$5$', '$16$', '$8$', '$4$'], 2, [
        'Inside out, checking odd or even every time:',
        '$6$ even: $\\frac62=3$. $3$ odd: $3\\cdot3+1=10$. $10$ even: $\\frac{10}{2}=5$. $5$ odd: $3\\cdot5+1=16$.',
        'Four steps: the answer is $16$. (Stopping one step early gives $5$.)'])
    PQ['11'] = ('The operation $\\blacklozenge$ is defined for every integer $x$:\n'
                '$\\blacklozenge(x)=\\begin{cases} x^2-5, & x\\ge0 \\\\ -2x, & x<0 \\end{cases}$\n'
                'For how many integers $x$ is $\\blacklozenge(x)$ equal to $4$?',
                ['$0$', '$1$', '$2$', '$3$'], 3, [
        'Try both rules, and keep only answers that fit their rule.',
        'First rule: $x^2-5=4$, so $x^2=9$: $x=3$ or $x=-3$. This rule is only for $x\\ge0$, so keep $x=3$ and reject $x=-3$.',
        'Second rule: $-2x=4$, so $x=-2$. $-2<0$ ✓.',
        'Two integers: $3$ and $-2$. (Check: $\\blacklozenge(-3)=-2\\cdot(-3)=6$, not $4$.)'])
    PQ['12'] = ('The operation $\\blacklozenge$ is defined for every positive integer $n$:\n'
                '$\\blacklozenge(n)=\\begin{cases} 2, & n=1 \\\\ 3\\cdot\\blacklozenge(n-1)-2, & n>1 \\end{cases}$\n$\\blacklozenge(4)=?$',
                ['$10$', '$28$', '$82$', '$12$'], 2, [
        'Climb up from the start value $\\blacklozenge(1)=2$:',
        '$\\blacklozenge(2)=3\\cdot2-2=4$, $\\blacklozenge(3)=3\\cdot4-2=10$, $\\blacklozenge(4)=3\\cdot10-2=28$.'])
    PQ['13'] = ('For every number $x\\ne1$: $\\blacklozenge(x)=\\frac{1}{1-x}$. $\\blacklozenge(\\blacklozenge(\\blacklozenge(2)))=?$',
                ['$-1$', '$\\frac12$', '$2$', '$-2$'], 3, [
        '$\\blacklozenge(2)=\\frac{1}{1-2}=-1$.',
        '$\\blacklozenge(-1)=\\frac{1}{1-(-1)}=\\frac12$.',
        '$\\blacklozenge\\left(\\frac12\\right)=\\frac{1}{1-\\frac12}=\\frac{1}{\\frac12}=2$.',
        'Three steps bring you back to $2$. So the pattern repeats every three steps: applying $\\blacklozenge$ $30$ times to $2$ also gives $2$.'])
    PQ['14'] = ('For every number $x$, $[x]$ is the largest integer that is not bigger than $x$. Given: $[x]=3$. Which of the following could be the value of $x$?',
                ['$2.9$', '$3.99$', '$4$', '$4.5$'], 2, [
        'Examples first: $[3]=3$, $[3.5]=3$, $[3.99]=3$, but $[4]=4$ and $[2.9]=2$.',
        'So $[x]=3$ means $3\\le x<4$. Only $3.99$ fits.'])
    PQ['15'] = ('For every positive integer $n$, $\\blacklozenge(n)$ is the sum of the digits of $n$. For example, $\\blacklozenge(47)=4+7=11$. '
                'For how many two-digit numbers $n$ is $\\blacklozenge(n)$ equal to $5$?',
                ['$4$', '$5$', '$6$', '$9$'], 2, [
        'Write them in order of the tens digit: $14$, $23$, $32$, $41$, $50$.',
        'The tens digit cannot be $0$ ($05$ is not a two-digit number). Five numbers.',
        'The trap $4$ forgets $50$.'])
    PQ['16'] = ('For every two numbers $a$ and $b$: $a\\star b=ab-a-b$. Which of the following must be true for all numbers $a$ and $b$?',
                ['$a\\star b=b\\star a$', '$a\\star0=a$', '$a\\star1=1$', '$a\\star b=(a-1)(b-1)$'], 1, [
        '(1) Swap the letters: $b\\star a=ba-b-a=ab-a-b=a\\star b$. Always true ✓.',
        '(2) $a\\star0=0-a-0=-a$. With $a=2$: $-2\\ne2$ ✗. (With $a=0$ it looks true — that is why we avoid $0$.)',
        '(3) $a\\star1=a-a-1=-1\\ne1$ ✗.',
        '(4) $(a-1)(b-1)=ab-a-b+1$, which is $1$ more than $a\\star b$ ✗.'])
    PQ['17'] = ('For every number $x$: $\\blacklozenge(x)=x^3$. Which of the following must be true for every number $x$?',
                ['$\\blacklozenge(x)+\\blacklozenge(x)=\\blacklozenge(2x)$', '$\\blacklozenge(x^2)=\\blacklozenge(x)\\cdot\\blacklozenge(x)$',
                 '$\\blacklozenge(x)=x\\cdot x$', '$\\blacklozenge(-x)=\\blacklozenge(x)$'], 2, [
        'With $x=0$ all four look true — $0$ proves nothing. Try $x=1$:',
        '(1) $1+1=2$, but $\\blacklozenge(2)=8$ ✗. (2) $1=1$ ✓. (3) $1=1$ ✓. (4) $-1\\ne1$ ✗.',
        'Two choices survive, so try a second number, $x=2$: (2) $\\blacklozenge(4)=64$ and $8\\cdot8=64$ ✓. (3) $8\\ne4$ ✗.',
        'Why (2) is always true: $(x^2)^3=x^6=(x^3)^2$.'])
    for k, (stem, ch, cor, ex) in PQ.items():
        M.new_q('q-r26-t19-' + k, TOPIC, stem, ch, cor, ex)
        M.place_q('q-r26-t19-' + k, PRACTICE)

    # =====================================================================================
    # 8. Practice order: easy -> hard
    # =====================================================================================
    R = 'q-r26-t19-'
    M.practice_order(PRACTICE, [
        X + '1', X + '2', X + '5', X + '7', R + '06', 'q-557', 'q-558', 'q-560', 'q-559', X + '4', R + '09',
        'q-563', R + '14', 'q-566', 'q-569', R + '10', 'q-565', 'q-561', 'q-562', 'q-576', R + '15',
        'q-564', 'q-568', R + '07', R + '12', 'q-571', 'q-572', 'q-570', 'q-575', 'q-567',
        R + '16', R + '17', R + '11', R + '08', R + '13', 'q-573', 'q-574'])
