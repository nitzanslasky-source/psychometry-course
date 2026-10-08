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
        A("'Definition in words? Write 2–3 examples first' appears",
          T('Definition in words? Write $2$–$3$ examples first', size=44, gap=50)),
        "Words are easy to misread. So before you touch the choices, write two or three quick examples.",
        A("'the remainder · the number of divisors · the sum of the digits' appears",
          T('the remainder · the number of divisors · the sum of the digits', size=40)),
        "Definitions in words you may meet: the remainder of a division, the number of divisors, the sum of the digits. Same move: examples first.",
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
    # Pass 2: the two original nested questions are restored (plan), cleaned up.
    S(X + '3', stem='For every number $x$: $F(x)=x^2-3$. $F(F(2))=?$', choices=['$1$', '$13$', '$-2$', '$-1$'], correct=3,
      expl=['Inside out: $F(2)=2^2-3=4-3=1$.',
            'Then $F(F(2))=F(1)=1^2-3=1-3=-2$.'])
    S(X + '6', stem='For every positive number $x$: $H(x)=\\frac1x$. $H(H(4))=?$',
      choices=['$\\frac{1}{16}$', '$\\frac14$', '$16$', '$4$'], correct=4,
      expl=['Inside out: $H(4)=\\frac14$.',
            'Then $H\\left(\\frac14\\right)=1\\div\\frac14=1\\cdot4=4$.',
            'The reciprocal of the reciprocal is the number itself: $H(H(x))=x$.'])

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

    # (Pass 2: G4, the integer part [x] question q-r26-t19-04, was removed - plan: not on the exam.)

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

    # 2026-10-01 elite comparison: property questions (lesson slides, card rows, guided question)
    elite_property(M)

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
        ['Definition in words', 'write 2–3 examples first', 'remainder of $47\\div9$: $47=5\\cdot9+2$, so $2$'],
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
        X + '1', X + '2', X + '3', X + '5', X + '7', X + '6', R + '06', 'q-557', 'q-558', 'q-560', 'q-559', X + '4', R + '09',
        'q-563', 'q-566', 'q-569', R + '10', 'q-565', 'q-561', 'q-562', 'q-576', R + '15',
        'q-564', 'q-568', R + '07', R + '12', 'q-571', 'q-572', 'q-570', 'q-575', 'q-567',
        R + '16', R + '17', R + '11', R + '08', R + '13', 'q-573', 'q-574'])

    elite_property_practice(M)
    summary(M)
    elite_property_summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last
    cut_repeats(M)       # 2026-10-05: after that


def _b(label, tex, size=44):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summary(M):
    """Pass 2: a summary lesson right before the independent practice (end of the advanced section)."""
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    sb = ['Read, then substitute', 'Brackets on every input', 'One step at a time', 'Match the whole input',
          'Missing pieces', 'Conditions', 'Circular · both sides', 'Always? Must?', 'Before you practice']
    M.new_video('r26-t19-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            "A quick summary before you practice on your own.",
            "Everything we learned about new operations — in about three minutes."]),
        dict(mode='concept', active=0, title='Read, then substitute', script=[
            _b('a ♥ b = 4(a + b): 5 ♥ 3 = 4(5 + 3) = 32', '$a\\heartsuit b=4(a+b):\\quad 5\\heartsuit3=4(5+3)=32$'),
            "A new operation is just a definition. Read it first — then follow the whole recipe.",
            "Whatever sits before the symbol goes into a. Whatever sits after it goes into b.",
            _b('2 ⋆ 5 ≠ 5 ⋆ 2', 'Order can matter: $\\ 2\\star5\\ne5\\star2$'),
            "And don't assume it behaves like plus. Swap the inputs — you can get a different answer.",
            "So circle which number goes into which slot."]),
        dict(mode='concept', active=1, title='Brackets on every input', script=[
            _b('◆(x) = x² − 3x', '$\\blacklozenge(x)=x^2-3x$'),
            _b('◆(−4) = (−4)² − 3 · (−4) = 16 + 12 = 28', '$\\blacklozenge(-4)=(-4)^2-3\\cdot(-4)=16+12=28$', size=42),
            "Whatever goes in, goes in brackets. Every time.",
            "Minus four, squared, in brackets: sixteen. Without brackets you'd get minus sixteen.",
            _b('◆(x + 1) = (x + 1)² − 3(x + 1) = x² − x − 2', '$\\blacklozenge(x+1)=(x+1)^2-3(x+1)=x^2-x-2$', size=42),
            "An expression goes in the same way: the whole thing, in brackets, then open them."]),
        dict(mode='concept', active=2, title='One step at a time', script=[
            _b('◆(2) + ◆(6) = 4 + 36 = 40 ≠ ◆(8)', '$\\blacklozenge(x)=x^2:\\quad \\blacklozenge(2)+\\blacklozenge(6)=4+36=40\\ne\\blacklozenge(8)$', size=40),
            "Inside a longer exercise: first turn every operation into a plain number. Then do the rest.",
            _b('(5 ⋆ 3) ⋆ 4 = 17 ⋆ 4 = 33', '$a\\star b=a+4b:\\quad (5\\star3)\\star4=17\\star4=33$', size=40),
            "An operation inside an operation? Inside out.",
            "The result of the inside becomes the input of the outside. Don't stop halfway — the halfway number is waiting in the choices."]),
        dict(mode='concept', active=3, title='Match the whole input', script=[
            _b('F(3t) = t + 7. F(18) = ?', '$F(3t)=t+7.\\quad F(18)=\\ ?$'),
            "Here the rule works on three t — not on t.",
            _b('3t = 18 → t = 6 → F(18) = 6 + 7 = 13', '$3t=18\\ \\to\\ t=6\\ \\to\\ F(18)=6+7=13$'),
            "So first match the whole input: three t is eighteen, t is six. Then the rule: thirteen.",
            "Put eighteen straight into t, and you're really calculating F of fifty-four."]),
        dict(mode='concept', active=4, title='Missing pieces', script=[
            _b('◆(4) = 20. Which cannot be ◆?', '$\\blacklozenge(4)=20$. Which definition cannot be $\\blacklozenge$?', size=42),
            "No definition at all? Put the given input into each choice. The one that doesn't give the result is out.",
            "Found it? Mark it and move on.",
            _b('x ⋆ 3 = 20 → x + 12 = 20 → x = 8', '$x\\star3=20\\ \\to\\ x+12=20\\ \\to\\ x=8$'),
            "An unknown input? Write the definition — and it's an ordinary equation.",
            "Or work back from the answers: put each choice into the rule."]),
        dict(mode='concept', active=5, title='Conditions', script=[
            _b('◆(x) = x + 6 (x odd), x² − 6 (x even)', '$\\blacklozenge(x)=\\begin{cases} x+6, & x \\text{ odd} \\\\ x^2-6, & x \\text{ even} \\end{cases}$'),
            "Two rules? Check the input first: odd or even?",
            "And check again at every step. The output of one step is the next input — and it can switch.",
            _b('◆(x) = 94: odd → x = 88 ✗ · even → x = 10 ✓', '$\\blacklozenge(x)=94$: odd rule $x=88$ ✗ $\\quad$ even rule $x=10$ ✓', size=40),
            "The result is given? Try every rule. Keep an answer only if it fits the rule you used."]),
        dict(mode='concept', active=6, title='Circular · both sides', script=[
            _b('◆(1) = 5, ◆(x) = 3 · ◆(x − 1): ◆(3) = 45', '$\\blacklozenge(1)=5,\\ \\ \\blacklozenge(x)=3\\cdot\\blacklozenge(x-1):\\quad \\blacklozenge(3)=3\\cdot15=45$', size=40),
            "The operation inside its own definition? Go down to the start value. Then climb back up with real numbers.",
            _b('3 · ◆(x) − 4 = ◆(x) + 2x → ◆(x) = x + 2', '$3\\cdot\\blacklozenge(x)-4=\\blacklozenge(x)+2x\\ \\to\\ \\blacklozenge(x)=x+2$', size=40),
            "The operation on both sides? Treat it as the unknown, and isolate it.",
            "Definition in words? Write two or three examples first."]),
        dict(mode='concept', active=7, title='Always? Must?', script=[
            _b('"Not always"? One counterexample.', '"Not always"? One counterexample is enough.', size=40),
            _b('"Always"? Swap the letters.', '"Always"? Swap the letters in the algebra: $b\\star a=a\\star b$?', size=40),
            "To say no — one example. To say yes — algebra.",
            _b('Must be true: plug in 2 or 3, not 0 or 1', 'Must be true: plug in $2$ or $3$ — not $0$, $1$ or equal values', size=40),
            "Zero, one and equal values can make a false rule look true. Two choices left? Try a second number.",
            "And a must-be-true question can eat your time. Skip it, and come back at the end.",
            _b('◆(k) − ◆(−k): odd powers, doubled', '$\\blacklozenge(k)-\\blacklozenge(-k)$: only the odd powers are left, doubled', size=40),
            "One shortcut from the advanced questions: a number minus its opposite — the even powers cancel."]),
        dict(mode='concept', active=8, title='Before you practice', script=[
            "Before every question, ask yourself:",
            _b('Which number goes into which slot?', 'Which number goes into which slot?', size=40),
            _b('Did every input get brackets?', 'Did every input get brackets?', size=40),
            _b('Odd or even — at this step?', 'Conditions: which rule — at this step?', size=40),
            _b('Does my answer fit the rule I used?', 'Does my answer fit the rule I used?', size=40),
            _b('Traps: no brackets · stopping halfway · 18 straight into t', 'Traps: $-4^2$ without brackets · stopping halfway · $18$ straight into $t$', size=38),
            "The traps: minus four squared without brackets, stopping halfway in a nested operation, and putting the number straight into t.",
            "Read the definition, and follow it faithfully. Good luck."]),
    ], ADV, after=last)


# =========================================================================================================
# 2026-10-01 elite comparison: "property" questions (put each rule on trial; rules that undo themselves; inverse)
# Real exams: 2020 autumn I-9, 2023 spring I-20, 2024 winter II-20, 2022 autumn II-14, 2024 autumn I-18.
# =========================================================================================================
def elite_property(M):
    P = PATTERNS
    # Operation Patterns: slides 1 title, 2-8 types one to six, 9 recap -> three new slides before the recap
    M.insert_slides(P, 8, [
        dict(mode='concept', active=7, title='Property questions', script=[
            "Type seven: a property question. No definition — only a property the operation has.",
            A('◆(◆(x)) = x appears', T('$\\blacklozenge(\\blacklozenge(x))=x$ for every $x>0$', size=46, gap=170)),
            "Do the diamond twice — and you're back where you started. Which rule could it be?",
            "Put each rule on trial. Plug in a test value, and see if the property holds.",
            D('Write "x²: 3 → 9 → 81 ✗"'),
            "x squared: three goes to nine, and nine goes to eighty-one. Not back to three. Out.",
            D('Write "10 − x: 3 → 7 → 3 ✓"'),
            "Ten minus x: three goes to seven, and seven goes back to three. It passes.",
            "Don't test with zero or one. One squared is one — x squared would look fine.",
            A('◆(x + 1) = 3 · ◆(x) appears', T('$\\blacklozenge(x+1)=3\\cdot\\blacklozenge(x)$', size=46, gap=30)),
            "A step property: one step up in the input, and the result is three times bigger.",
            "Test two neighbors: x is two, and x is three.",
            D('Write "3x: ◆(2) = 6, ◆(3) = 9 ✗     3ˣ: ◆(2) = 9, ◆(3) = 27 ✓"'),
            "Three x: six, then nine — not three times bigger. Three to the x: nine, then twenty-seven. It passes.",
        ]),
        dict(mode='concept', active=8, title='Rules that undo themselves', script=[
            "Some rules always undo themselves. Two families keep coming up. Know them by sight.",
            A('c − x appears', T('$c-x$: $\\quad 10-x:\\ \\ 3\\to7\\to3$', size=46, gap=30)),
            "c minus x, for any number c. Ten minus x: three, seven, three.",
            "Minus x is in this family too — c is zero.",
            A('c/x appears', T('$\\frac{c}{x}$: $\\quad \\frac{12}{x}:\\ \\ 3\\to4\\to3$', size=46, gap=30)),
            "c over x. Twelve over x: three goes to four, and four goes back to three.",
            "One over x is in this family too — and so is x to the minus one. It's the same thing.",
            A('Never: x², √x, 2x, x + 5 appears', T('Never: $\\ x^2,\\ \\ \\sqrt{x},\\ \\ 2x,\\ \\ x+5$', size=46)),
            "Squares, roots, doubling, adding a number: do them twice, and you don't get back.",
        ]),
        dict(mode='concept', active=9, title='Inverse operation', script=[
            "The inverse operation undoes the diamond. Put in the result — get back x.",
            A('◆(x) = 2x + 3 appears', T('$\\blacklozenge(x)=2x+3$', size=48, gap=30)),
            "Read the steps of the diamond: first times two, then plus three.",
            A('Undo in reverse order appears', T('Undo: $-3$, then $\\div2$ $\;\\to\;$ $\\#(y)=\\frac{y-3}{2}$', size=46, gap=110)),
            "Undo them in reverse order. The last step comes off first: minus three. Then divide by two.",
            D('Write "x = 4 → ◆(4) = 11 → #(11) = 8 ÷ 2 = 4 ✓"'),
            "Check with a number: four goes to eleven. Eleven minus three is eight. Over two — four. Back to the start.",
            "The trap choice undoes the steps in the wrong order: y over two, minus three.",
            A("'Check: x → ◆(x) → back to x?' appears", T('Check: $\\ x\\to\\blacklozenge(x)\\to$ back to $x$?', size=44)),
        ]),
    ])
    M.set_slide(P, 12, script=[
        "Let's lock it in.",
        A("'Expression input? Match the whole input' appears", T('Expression input? Match the whole input', size=34)),
        A("'Conditions? Check at every step' appears", T('Conditions? Check at every step', size=34)),
        A("'Result given? Try every rule, then check' appears", T('Result given? Try every rule, then check the answer', size=34)),
        A("'Circular? Down to the start value, then back up' appears", T('Circular? Down to the start value, then back up', size=34)),
        A("'Both sides? Isolate the operation' appears", T('Both sides? Isolate the operation', size=34)),
        A("'Words? Write examples first' appears", T('Definition in words? Write examples first', size=34)),
        A("'Must be true? Last — plug in 2 or 3' appears", T('Must be true? Last — plug in $2$ or $3$, not $0$ or $1$', size=34)),
        A("'Property? Put each rule on trial' appears", T('Property? Put each rule on trial · inverse: undo in reverse order', size=34)),
        D('Tick each line'),
        "Those are the types that can show up. Now you know what to do with every one.",
        "Questions next — at least one for each type.",
    ])
    M.set_sidebar(P, ['Expression input', 'Conditions', 'Conditions backwards', 'Circular rules', 'Isolate the operation',
                      'Definition in words', 'Must be true?', 'Property questions', 'Undo themselves', 'Inverse operation',
                      'Recap'])
    for n in range(2, 13):
        M.slide(P, n)['active'] = n - 2

    # guided question: which rule undoes itself
    g = 'q-r26-t19-18'
    M.new_q(g, TOPIC, 'The operation $\\blacklozenge$ is defined for every positive number $x$.\n'
            'It is known that for every positive $x$: $\\blacklozenge(\\blacklozenge(x))=x$.\n'
            'Which of the following can be the definition of the operation $\\blacklozenge$?',
            ['$\\blacklozenge(x)=6x$', '$\\blacklozenge(x)=x+6$', '$\\blacklozenge(x)=\\frac{x}{6}$', '$\\blacklozenge(x)=\\frac{6}{x}$'], 4, [
        'Put each rule on trial with $x=2$: apply it twice and see if you get back to $2$.',
        '(1) $2\\to12\\to72$ ✗. (2) $2\\to8\\to14$ ✗. (3) $2\\to\\frac13\\to\\frac1{18}$ ✗.',
        '(4) $2\\to3\\to2$ ✓. In general: $\\blacklozenge(\\blacklozenge(x))=\\frac{6}{\\frac{6}{x}}=x$ for every positive $x$.',
        '$\\frac{c}{x}$ always undoes itself. $\\frac{x}{6}$ looks similar, but it keeps getting smaller.'])
    M.place_q(g, THEORY, after='solve-q-549')
    beats = [dict(mode='title', title='Question %d' % M.next_question_number(TOPIC), script=[
        "A property question. No definition — just a property.",
        "So we put each rule on trial."])]
    for title, script in [
        ('Method 1 · Put each rule on trial', [
            "Do the diamond twice — you must get back to x.",
            "Pick a test value. Not zero, not one. Take two.",
            D('Next to choice 1 write "2 → 12 → 72 ✗"'),
            "Six x: two goes to twelve, twelve goes to seventy-two. Not two. Out.",
            D('Next to choice 2 write "2 → 8 → 14 ✗"'),
            "x plus six: eight, then fourteen. Out.",
            D('Next to choice 3 write "2 → 1/3 → 1/18 ✗"'),
            "x over six: one third, then one eighteenth. Smaller and smaller. Out.",
            D('Next to choice 4 write "2 → 3 → 2 ✓" and circle choice 4'),
            "Six over x: two goes to three, three goes back to two. Choice four.",
        ]),
        ('Method 2 · Know the family', [
            "Faster: you know the families that undo themselves. c minus x, and c over x.",
            D('Write "6 ÷ (6 ÷ x) = x"'),
            "Six over x is c over x. Six over six-over-x — that's x again. For every x.",
            "Watch choice three — x over six. It looks close, but the x is on top. It just keeps shrinking.",
            "So: spot the family — and check with one number to be sure.",
        ])]:
        beats.append(dict(mode='question', active=0, title=title, pre=[Q(g)], script=script))
    v = M.new_video('solve-' + g, TOPIC, 'Operation Questions', [], beats, THEORY, kind='solution', qid=g)
    v['beats'][0]['title'] = 'Operation Questions'
    v['hybrid']['num'] = 62
    v['title'] = v['navLabel'] = M.q(g)['stem']


def elite_property_practice(M):
    # memory card rows
    rows = M.card(CARD)['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0] == 'Must be true')
    rows[k:k] = [
        ['Property given', 'put each rule on trial with a test value (not $0$ or $1$) · a step property: two neighbors',
         '$\\blacklozenge(\\blacklozenge(x))=x$: $\\ 10-x:\\ 3\\to7\\to3$'],
        ['Undoes itself', '$c-x$ and $\\frac{c}{x}$ (also $-x$, $\\frac1x=x^{-1}$) · never $x^2$, $\\sqrt x$, $2x$', '$\\frac{12}{x}:\\ 3\\to4\\to3$'],
        ['Inverse operation', 'undo the steps in reverse order, then check with a number', '$2x+3\\ \\to\\ \\frac{y-3}{2}$'],
    ]

    R = 'q-r26-t19-'
    M.new_q(R + '19', TOPIC, 'The operation $\\blacklozenge$ is defined for every positive integer $x$.\n'
            'It is known that for every positive integer $x$: $\\blacklozenge(x+1)=\\blacklozenge(x)+3$.\n'
            'Which of the following can be the definition of the operation $\\blacklozenge$?',
            ['$\\blacklozenge(x)=x+3$', '$\\blacklozenge(x)=3x$', '$\\blacklozenge(x)=3^x$', '$\\blacklozenge(x)=x^3$'], 2, [
        'A step property: test two neighbors, $x=2$ and $x=3$. The second result must be $3$ more than the first.',
        '(1) $5$ and $6$: only $1$ more ✗. (2) $6$ and $9$: $3$ more ✓. (3) $9$ and $27$ ✗. (4) $8$ and $27$ ✗.',
        'In general: $3(x+1)=3x+3$ ✓. The trap is choice 1: "plus $3$" in the property does not mean "plus $3$" in the rule.'])
    M.new_q(R + '20', TOPIC, 'The operation $\\#$ is the inverse operation of $\\blacklozenge$. For every positive number $x$:\n'
            '$\\begin{cases} \\blacklozenge(x)=\\sqrt{x}+4 \\\\ \\#(\\blacklozenge(x))=x \\end{cases}$\n'
            'What is $\\#(y)$?',
            ['$\\#(y)=y^2-4$', '$\\#(y)=(y-4)^2$', '$\\#(y)=\\sqrt{y}-4$', '$\\#(y)=(y+4)^2$'], 2, [
        'The steps of $\\blacklozenge$: first take the root, then add $4$.',
        'Undo them in reverse order: first subtract $4$, then square. $\\#(y)=(y-4)^2$.',
        'Check with $x=9$: $\\blacklozenge(9)=3+4=7$, and $\\#(7)=(7-4)^2=9$ ✓. The other choices give $45$, $\\sqrt7-4$ and $121$.',
        'Choice 1 undoes the steps in the wrong order.'])
    M.place_q(R + '19', PRACTICE, after=R + '09')
    M.place_q(R + '20', PRACTICE, after=R + '19')


def elite_property_summary(M):
    V = 'r26-t19-summary'
    # slides: 1 title, 2-5, 6 'Missing pieces', ... -> new slide after 'Missing pieces'
    M.insert_slides(V, 6, [dict(mode='concept', active=5, title='Property questions', script=[
        _b('◆(◆(x)) = x: 10 − x: 3 → 7 → 3', '$\\blacklozenge(\\blacklozenge(x))=x$: $\\quad 10-x:\\ 3\\to7\\to3$ ✓', size=42),
        "Only a property? Put each rule on trial with a test value — not zero or one.",
        "A step property? Test two neighbors.",
        _b('Undo themselves: c − x, c/x', 'Undo themselves: $\\ c-x\\ $ and $\\ \\frac{c}{x}$', size=42),
        "Two families undo themselves: c minus x, and c over x. Squares and doubling never do.",
        _b('Inverse: undo the steps in reverse order', 'Inverse: undo the steps in reverse order', size=42),
        "An inverse operation? Undo the steps in reverse order — then check with one number.",
    ])])
    sb = ['Read, then substitute', 'Brackets on every input', 'One step at a time', 'Match the whole input',
          'Missing pieces', 'Property questions', 'Conditions', 'Circular · both sides', 'Always? Must?', 'Before you practice']
    M.set_sidebar(V, sb)
    for n in range(2, len(M.video(V)['beats']) + 1):
        M.slide(V, n)['active'] = n - 2


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
    # Lesson "new-operation" slide 5 worked out ◆(x + 1) for ◆(x) = x² − 2x, the same as guided q-r26-t19-01
    # -> the lesson now puts in x + 2 (same definition, same trap).
    _dd_sub(M, 'new-operation', 5, [
        (r'$\blacklozenge(x+1)$', r'$\blacklozenge(x+2)$'),
        ('◆(x + 1) appears', '◆(x + 2) appears'),
        ('Next to it write "= (x + 1)² − 2(x + 1)"', 'Next to it write "= (x + 2)² − 2(x + 2)"'),
        ('Now the input is x plus one.', 'Now the input is x plus two.'),
        ('Below write "= x² + 2x + 1 − 2x − 2 = x² − 1"', 'Below write "= x² + 4x + 4 − 2x − 4 = x² + 2x"'),
        ('Open the brackets: x squared plus two x plus one, minus two x, minus two. x squared minus one.',
         'Open the brackets: x squared plus four x plus four, minus two x, minus four. x squared plus two x.'),
        ('Next to it write "x + 1² − 2x + 1" and cross it out', 'Next to it write "x + 2² − 2x + 2" and cross it out')])


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
    new_sb = [lab for k, lab in enumerate(sb) if not (k in gone and k not in keep_used)]
    for b in v['beats']:
        if 0 <= b['active'] < len(sb): b['active'] = new_sb.index(sb[b['active']])
    M.set_sidebar(vid, new_sb)


def cut_repeats(M):
    # ---- "Operation Patterns": each type is taught by the question right after it -> keep the intro + the inverse
    #      operation (no question video teaches it). Expression input -> Q6; conditions -> Q7; backwards -> Q8;
    #      circular -> Q9, Q10; isolate -> Q11; must be true -> Q12; property + undo themselves -> Q13 (+ the step
    #      property in one line); definition in words -> one line in Q21 (q-556).
    _cr_cut(M, PATTERNS, ['Operation on an expression', 'Conditions', 'Conditions backwards', 'Circular rules',
                          'Isolate the operation', 'Definition in words', 'Must be true?', 'Property questions',
                          'Rules that undo themselves', 'Recap'])
    M.set_slide(PATTERNS, 1, script=[
        'Last time we saw what a new operation is — with the basic questions.',
        'Now: the more advanced types. Still not complicated — just a little different.',
        'Each question that follows shows one type. First, one type that only the practice has: the inverse operation.'])
    _cr_add(M, PATTERNS, 2, None, ['Now the questions — one for each of the other types.'])
    # Q13: the step property (used in the practice)
    _cr_add(M, 'solve-q-r26-t19-18', 3, 'So: spot the family', [
        A("'Step property? Test two neighbors' appears", T('Step property, like $\\blacklozenge(x+1)=3\\cdot\\blacklozenge(x)$? Test two neighbors', size=34)),
        "Other property questions work the same way. A step property — one step up in the input, three times the result? Test two neighbors, like two and three."])
    # Q21: definitions in words
    _cr_add(M, 'solve-q-556', 2, 'First, understand the operation through its example', [
        A("'Definition in words? Write 2–3 examples first' appears", T('Definition in words? Write $2$–$3$ examples first', size=36)),
        "A definition in words — a remainder, the number of divisors, the sum of the digits — is easy to misread. Write two or three quick examples first."], where='after')


# ======================================================================================================
# 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived item (the 36 study-guide
# questions q-541 .. q-576 and the Hebrew lesson's own examples) gets new numbers / letters - same rule structure,
# same kind of question, same trap, same level, at least the same methods. Plus the approved practice clean-up.
# Nothing in topic 19 is recorded (no take in ~/Documents/Course.recordings). Runs last, after cut_repeats.
# ======================================================================================================
RN_RECORDED = set()


def _rn_sub(M, vid, n, pairs):
    """Exact substring replacements on one slide: board items, item labels, spoken lines, draw cues."""
    if vid in RN_RECORDED: return
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = 0
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit += 1
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit += 1
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    M.touched_videos.add(vid)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid not in RN_RECORDED: M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. Titles and the pre-loaded question stay."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script)


def rn_lessons(M):
    L = LESSON
    # slide 2: 4 · 6 and 4²  ->  3 · 7 and 5²
    _rn_sub(M, L, 2, [
        ('$4\\cdot6$', '$3\\cdot7$'), ('4 · 6 appears', '3 · 7 appears'),
        ("what's four dot six?", "what's three dot seven?"),
        ('Next to it write "= 4 × 6 = 24"', 'Next to it write "= 3 × 7 = 21"'),
        ('the dot means times — easy. Twenty-four.', 'the dot means times — easy. Twenty-one.'),
        ('$4^2$', '$5^2$'), ('4² appears', '5² appears'),
        ('Next to it write "= 4 × 4 = 16"', 'Next to it write "= 5 × 5 = 25"')])
    # slide 3: the heart  a ♥ b = 3(a + b), 6 ♥ 2  ->  a ♥ b = 2(a + b), 7 ♥ 3
    _rn_sub(M, L, 3, [
        ('$6\\heartsuit2$', '$7\\heartsuit3$'), ('6 ♥ 2 appears', '7 ♥ 3 appears'),
        ("What's six heart two?", "What's seven heart three?"),
        ('$a\\heartsuit b=3(a+b)$', '$a\\heartsuit b=2(a+b)$'), ('a ♥ b = 3(a + b)', 'a ♥ b = 2(a + b)'),
        ('then multiply the sum by three.', 'then multiply the sum by two.'),
        ('Under 6 ♥ 2 write "= 3(6 + 2) = 3 · 8 = 24"', 'Under 7 ♥ 3 write "= 2(7 + 3) = 2 · 10 = 20"'),
        ('Six goes into a, two goes into b. Six plus two is eight. Times three: twenty-four.',
         'Seven goes into a, three goes into b. Seven plus three is ten. Times two: twenty.'),
        ('Next to it write "6 · 3 + 2 = 20" and cross it out', 'Next to it write "7 · 2 + 3 = 17" and cross it out'),
        ("Six times three, plus two, is twenty — that's a different rule.",
         "Seven times two, plus three, is seventeen — that's a different rule.")])
    # slide 6: operation first  ◆(3) + ◆(4) = 25 vs ◆(7) = 49  ->  ◆(5) + ◆(1) = 26 vs ◆(6) = 36
    _rn_sub(M, L, 6, [
        ('$\\blacklozenge(3)+\\blacklozenge(4)$', '$\\blacklozenge(5)+\\blacklozenge(1)$'), ('◆(3) + ◆(4) appears', '◆(5) + ◆(1) appears'),
        ('Write "= 9 + 16 = 25"', 'Write "= 25 + 1 = 26"'),
        ('The diamond of three is nine. The diamond of four is sixteen. Now add: twenty-five.',
         'The diamond of five is twenty-five. The diamond of one is one. Now add: twenty-six.'),
        ('$\\blacklozenge(3+4)$', '$\\blacklozenge(5+1)$'), ('◆(3 + 4) appears', '◆(5 + 1) appears'),
        ('So first work out the input: seven.', 'So first work out the input: six.'),
        ('Write "= ◆(7) = 7² = 49 ≠ 25"', 'Write "= ◆(6) = 6² = 36 ≠ 26"'),
        ('The diamond of seven is forty-nine — a totally different number.', 'The diamond of six is thirty-six — a totally different number.')])
    # slide 7: nested  a ⋆ b = 2a + b², (2 ⋆ 3) ⋆ 1 = 27  ->  a ⋆ b = 3a + b², (1 ⋆ 2) ⋆ 3 = 30
    _rn_sub(M, L, 7, [
        ('$a\\star b=2a+b^2$', '$a\\star b=3a+b^2$'), ('a ⋆ b = 2a + b²', 'a ⋆ b = 3a + b²'),
        ('Two times the first, plus the square of the second.', 'Three times the first, plus the square of the second.'),
        ('$(2\\star3)\\star1$', '$(1\\star2)\\star3$'), ('(2 ⋆ 3) ⋆ 1 appears', '(1 ⋆ 2) ⋆ 3 appears'),
        ('Under the brackets write "2 ⋆ 3 = 4 + 9 = 13"', 'Under the brackets write "1 ⋆ 2 = 3 + 4 = 7"'),
        ('Two star three: four plus nine — thirteen.', 'One star two: three plus four — seven.'),
        ('Write "13 ⋆ 1 = 26 + 1 = 27"', 'Write "7 ⋆ 3 = 21 + 9 = 30"'),
        ('Put thirteen in its place. Thirteen star one: twenty-six plus one — twenty-seven.',
         'Put seven in its place. Seven star three: twenty-one plus nine — thirty.')])
    # slide 8: find the operation  ◆(3) = 24, 8x  ->  ◆(5) = 30, 6x
    _rn_sub(M, L, 8, [
        ('$\\blacklozenge(3)=24$', '$\\blacklozenge(5)=30$'), ('◆(3) = 24 appears', '◆(5) = 30 appears'),
        ('They took three, did the operation, and got twenty-four.', 'They took five, did the operation, and got thirty.'),
        ('Below write "◆(x) = 8x → 8 · 3 = 24 ✓"', 'Below write "◆(x) = 6x → 6 · 5 = 30 ✓"'),
        ('For example: eight x. Eight times three is twenty-four.', 'For example: six x. Six times five is thirty.'),
        ("Put three in each — the one that doesn't give twenty-four is the answer.",
         "Put five in each — the one that doesn't give thirty is the answer.")])
    # slide 9: order can matter (same star, now 3a + b²)  3 ⋆ 4 / 4 ⋆ 3  ->  2 ⋆ 4 / 4 ⋆ 2
    _rn_sub(M, L, 9, [
        ('$3\\star4\\qquad 4\\star3$', '$2\\star4\\qquad 4\\star2$'), ('3 ⋆ 4 and 4 ⋆ 3 appear', '2 ⋆ 4 and 4 ⋆ 2 appear'),
        ('Under 3 ⋆ 4 write "6 + 16 = 22"; under 4 ⋆ 3 write "8 + 9 = 17"', 'Under 2 ⋆ 4 write "6 + 16 = 22"; under 4 ⋆ 2 write "12 + 4 = 16"'),
        ('Three star four: six plus sixteen, twenty-two. Four star three: eight plus nine, seventeen.',
         'Two star four: six plus sixteen, twenty-two. Four star two: twelve plus four, sixteen.'),
        ('one counterexample is enough — like three and four.', 'one counterexample is enough — like two and four.'),
        ('Three star three equals three star three — for every operation.', 'Four star four equals four star four — for every operation.')])
    # slide 10: unknown input  x ⋆ 2 = 18 -> x = 7  ->  x ⋆ 4 = 25 -> x = 3
    _rn_sub(M, L, 10, [
        ('$x\\star2=18$', '$x\\star4=25$'), ('x ⋆ 2 = 18 appears', 'x ⋆ 4 = 25 appears'),
        ('Write "2x + 4 = 18 → 2x = 14 → x = 7"', 'Write "3x + 16 = 25 → 3x = 9 → x = 3"'),
        ('Two x plus four equals eighteen. Two x is fourteen. x is seven.', 'Three x plus sixteen equals twenty-five. Three x is nine. x is three.'),
        ('Write "x = 7: 2 · 7 + 2² = 14 + 4 = 18 ✓"', 'Write "x = 3: 3 · 3 + 4² = 9 + 16 = 25 ✓"'),
        ("Seven: fourteen plus four, eighteen. That's the one.", "Three: nine plus sixteen, twenty-five. That's the one.")])
    # memory card: the lesson's examples and the Hebrew questions' numbers
    c = M.card(CARD)
    new_ex = {
        'Basic': '$a\\heartsuit b=2(a+b)$: $7\\heartsuit3=20$',
        'Inside an exercise': '$\\blacklozenge(5)+\\blacklozenge(1)\\ne\\blacklozenge(6)$',
        'Nested': '$(1\\star2)\\star3=7\\star3=30$',
        'Find the operation': '$\\blacklozenge(5)=30$',
        'Unknown input': '$x\\star4=25\\Rightarrow x=3$',
        'Always $a\\star b=b\\star a$?': '$2\\star4\\ne4\\star2$',
        'Input is an expression': '$F(5t)$ with $5t=35$',
        'Conditions': 'odd $3x$, even $\\frac{x}{2}$: $\\blacklozenge(5)=15$, $\\blacklozenge(8)=4$',
        'Circular': '$\\blacklozenge(x)=2\\cdot\\blacklozenge(x-1)$, $\\blacklozenge(1)=3$',
        'Operation on both sides': '$3\\cdot\\blacklozenge(x)=\\blacklozenge(x)+4x\\Rightarrow\\blacklozenge(x)=2x$',
        'Definition in words': 'remainder of $29\\div4$: $29=7\\cdot4+1$, so $1$',
        '$\\blacklozenge(k)-\\blacklozenge(-k)$': '$x^4+3x$: $2\\cdot3\\cdot5=30$ for $k=5$',
    }
    rows = c['tables'][0]['rows']
    for r in rows:
        if r[0] in new_ex: r[2] = new_ex.pop(r[0])
    assert not new_ex, new_ex
    c['tips'][0] = 'A new operation need not behave like plus: $2\\star4\\ne4\\star2$.'


def rn_guided(M):
    B = '\\blacklozenge'
    # ---------- Q1 q-541: ◆(a) = a² − 2a, ◆(5) = 15   ==>   ◆(a) = a² − 4a, ◆(6) = 12
    _rn_q(M, 'q-541', 'The operation $\\blacklozenge$ is defined for every number $a$: $\\blacklozenge(a)=a^2-4a$. $\\blacklozenge(6)=?$',
          ['$36$', '$12$', '$60$', '$24$'], 2, [
        'Substitute $a=6$ into the definition: $\\blacklozenge(6)=6^2-4\\cdot6=36-24=12$.',
        'Faster: factor first. $a^2-4a=a(a-4)$, so $\\blacklozenge(6)=6\\cdot2=12$.'])
    _rn_video(M, 'q-541', [[
        "The diamond of a is: a squared, minus four a.",
        "Every time we do the diamond on a number — that number takes a's place. Everywhere.",
        D('Write "◆(6) = 6² − 4 · 6"'),
        "Same template, six instead of a.",
        D('Write "= 36 − 24 = 12"'),
        "Thirty-six minus twenty-four: twelve.",
        D('Circle choice 2'),
        "Choice two.",
    ], [
        "A quicker route: factor the rule before you substitute.",
        D('Write "a² − 4a = a(a − 4)"'),
        "a squared minus four a is a times a minus four.",
        D('Write "◆(6) = 6 · 2 = 12" and circle choice 2'),
        "Six times two: twelve. Same answer.",
    ]])

    # ---------- Q2 q-542: ◆(x) = x², ◆(◆(2)) = 16   ==>   ◆(◆(3)) = 81
    _rn_q(M, 'q-542', 'The operation $\\blacklozenge$ is defined for every number $x$: $\\blacklozenge(x)=x^2$. $\\blacklozenge(\\blacklozenge(3))=?$',
          ['$9$', '$27$', '$81$', '$3$'], 3, [
        'Work from the inside out: $\\blacklozenge(3)=3^2=9$.',
        'Then $\\blacklozenge(\\blacklozenge(3))=\\blacklozenge(9)=9^2=81$.',
        'Stopping at $9$ is the trap.'])
    _rn_video(M, 'q-542', [[
        "A diamond inside a diamond. Like any brackets — start from the inside.",
        D('Underline the inner ◆(3)'),
        "First: the diamond of three.",
        D('Write "◆(3) = 3² = 9"'),
        "The diamond squares — three squared is nine.",
        D('Write "◆(◆(3)) = ◆(9)"'),
        "Now put nine in its place. The outer diamond works on nine.",
        D('Write "= 9² = 81" and circle choice 3'),
        "Nine squared: eighty-one. Choice three.",
        "Stopping at nine is the trap — and nine is waiting among the choices.",
    ], [
        "Or think about the rule itself: squaring, then squaring again.",
        D('Write "(x²)² = x⁴ → 3⁴ = 81"'),
        "That's x to the fourth. Three to the fourth: eighty-one.",
    ]])

    # ---------- Q3 q-543: ◆(2) = 10, which cannot be ◆   ==>   ◆(3) = 21
    _rn_q(M, 'q-543', 'Given: $\\blacklozenge(3)=21$. Which of the following cannot be the definition of the operation $\\blacklozenge$?',
          ['$\\blacklozenge(x)=x^3-6$', '$\\blacklozenge(x)=x(x+4)$', '$\\blacklozenge(x)=5x+5$', '$\\blacklozenge(x)=8x-3$'], 3, [
        'Put $x=3$ into each choice. A choice that does not give $21$ cannot be the definition.',
        '(1) $3^3-6=27-6=21$ ✓. (2) $3\\cdot(3+4)=3\\cdot7=21$ ✓. (3) $5\\cdot3+5=20$ ✗. (4) $8\\cdot3-3=21$ ✓.',
        'Only choice (3) fails.'])
    _rn_video(M, 'q-543', [[
        "They took three, did the diamond — and got twenty-one. We don't know the rule.",
        "It could be infinitely many things. Seven x, for example: seven times three is twenty-one.",
        "So: which definition can NOT be it? Put three into each choice.",
        D('Next to choice 1 write "27 − 6 = 21 ✓"'),
        "Choice one: three cubed minus six — twenty-one. It could be the rule. Out.",
        D('Cross out choice 1'),
        D('Next to choice 2 write "3 · 7 = 21 ✓"'),
        "Choice two: three times seven — twenty-one again. Out.",
        D('Cross out choice 2'),
        D('Next to choice 3 write "15 + 5 = 20 ✗"'),
        "Choice three: five times three plus five — twenty. Not twenty-one!",
        D('Circle choice 3'),
        "This one can't be the definition. On the exam: mark it and move on.",
        "Just for practice, let's check the last one.",
        D('Next to choice 4 write "24 − 3 = 21 ✓"'),
        "Twenty-four minus three: twenty-one. Possible. Choice three it is.",
    ]])

    # ---------- Q6 q-544: ◆(3x) = x + 4, ◆(12) = 8   ==>   ◆(2x) = x + 5, ◆(14) = 12
    _rn_q(M, 'q-544', 'The operation $\\blacklozenge$ is defined for every number $x$: $\\blacklozenge(2x)=x+5$. $\\blacklozenge(14)=?$',
          ['$12$', '$19$', '$33$', '$7$'], 1, [
        'The input of $\\blacklozenge$ is $2x$, not $x$. So find the $x$ with $2x=14$: $x=7$.',
        'Then $\\blacklozenge(14)=x+5=7+5=12$.',
        'The trap: putting $14$ straight into $x+5$ gives $19$.'])
    _rn_video(M, 'q-544', [[
        "Look closely: the diamond works on two x — not on x.",
        "So fourteen is not x. Fourteen is two x.",
        D('Write "2x = 14 → x = 7"'),
        "Two x is fourteen, so x is seven.",
        D('Write "◆(14) = x + 5 = 7 + 5 = 12"'),
        "The rule says x plus five. Seven plus five: twelve.",
        D('Circle choice 1'),
        "Choice one.",
        "Put fourteen straight into x plus five? Nineteen — and that trap is waiting in the choices.",
    ]])

    # ---------- Q7 q-545: odd 2x / even x² − 7, ◆◆◆(5) = 186   ==>   odd 2x / even x² − 3, ◆◆◆(3) = 66
    _rn_q(M, 'q-545', 'The operation $\\blacklozenge$ is defined for every integer $x$:\n'
          '$\\blacklozenge(x)=\\begin{cases} 2x, & x \\text{ odd} \\\\ x^2-3, & x \\text{ even} \\end{cases}$\n'
          '$\\blacklozenge(\\blacklozenge(\\blacklozenge(3)))=?$',
          ['$33$', '$12$', '$66$', '$6$'], 3, [
        '$3$ is odd: $\\blacklozenge(3)=2\\cdot3=6$.',
        '$6$ is even: $\\blacklozenge(6)=6^2-3=33$.',
        '$33$ is odd: $\\blacklozenge(33)=2\\cdot33=66$.',
        'Check odd or even again before every step.'])
    _rn_video(M, 'q-545', [[
        "Two rules: one for odd x, one for even x.",
        "Three diamonds — so, as always, start from the inside.",
        D('Write "◆(3): 3 odd → 2 · 3 = 6"'),
        "Three is odd. The odd rule: two x. Six.",
        D('Write "◆(6): 6 even → 6² − 3 = 33"'),
        "Now six goes in. Six is even — switch rules! Six squared minus three: thirty-three.",
        D('Write "◆(33): 33 odd → 2 · 33 = 66"'),
        "Thirty-three is odd again. Times two: sixty-six.",
        D('Circle choice 3'),
        "Choice three.",
        "Check the parity every single time — the output can switch sides.",
    ]])

    # ---------- Q9 q-546: ◆(0) = 0, ◆(x) = 7 − ◆(x − 2), ◆(6) = 7   ==>   ◆(0) = 2, ◆(x) = 9 − ◆(x − 2), ◆(6) = 7
    _rn_q(M, 'q-546', 'The operation $\\blacklozenge$ is defined for every even integer $x\\ge0$:\n'
          '$\\blacklozenge(x)=\\begin{cases} 2, & x=0 \\\\ 9-\\blacklozenge(x-2), & x\\ge2 \\end{cases}$\n$\\blacklozenge(6)=?$',
          ['$2$', '$6$', '$7$', '$3$'], 3, [
        'Go down to the start value: $\\blacklozenge(6)=9-\\blacklozenge(4)$, $\\blacklozenge(4)=9-\\blacklozenge(2)$, $\\blacklozenge(2)=9-\\blacklozenge(0)$, and $\\blacklozenge(0)=2$.',
        'Climb back up: $\\blacklozenge(2)=9-2=7$, $\\blacklozenge(4)=9-7=2$, $\\blacklozenge(6)=9-2=7$.',
        'The values go $2, 7, 2, 7$ — they switch back and forth.'])
    _rn_video(M, 'q-546', [[
        "The diamond of x uses the diamond of x minus two. And they gave us one start value: the diamond of zero is two.",
        D('Write "◆(6) = 9 − ◆(4)"'),
        "Diamond of six: nine minus the diamond of four. But we don't know that yet — keep going.",
        D('Write "◆(4) = 9 − ◆(2)"'),
        "Diamond of four: nine minus the diamond of two.",
        D('Write "◆(2) = 9 − ◆(0)"'),
        "Diamond of two: nine minus the diamond of zero.",
        D('Write "◆(0) = 2"'),
        "And the diamond of zero — given. Two. Now only numbers are left.",
        D('Climb back up: write "◆(2) = 7, ◆(4) = 2, ◆(6) = 7"'),
        "Nine minus two: seven. Nine minus seven: two. Nine minus two: seven.",
        D('Circle choice 3'),
        "Choice three.",
    ], [
        "Notice what happened: two, seven, two, seven.",
        D('Write "2 → 7 → 2 → 7"'),
        "It flips back and forth. So even the diamond of a hundred would be instant.",
    ]])

    # ---------- Q10 q-547: ◆(1) = 6, ◆(x) = ◆(x − 1), ◆(5) = 6   ==>   ◆(1) = 9, ◆(7) = 9
    _rn_q(M, 'q-547', 'The operation $\\blacklozenge$ is defined for every positive integer $x$:\n'
          '$\\blacklozenge(x)=\\begin{cases} 9, & x=1 \\\\ \\blacklozenge(x-1), & x>1 \\end{cases}$\n$\\blacklozenge(7)=?$',
          ['$7$', '$1$', '$0$', '$9$'], 4, [
        '$\\blacklozenge(7)=\\blacklozenge(6)=\\blacklozenge(5)=\\blacklozenge(4)=\\blacklozenge(3)=\\blacklozenge(2)=\\blacklozenge(1)=9$.',
        'Each value copies the one below it, so the start value $9$ passes all the way up.'])
    _rn_video(M, 'q-547', [[
        "If x is bigger than one, the diamond of x is the diamond of x minus one. If x is one — nine.",
        D('Write "◆(7) = ◆(6)"'),
        "Seven is bigger than one: the diamond of seven is the diamond of six.",
        D('Write "= ◆(5) = ◆(4) = ◆(3) = ◆(2) = ◆(1)"'),
        "Six, five, four, three, two — each one just passes to the one below.",
        "And now x is one. One is not bigger than one — so the start value applies.",
        D('Write "◆(1) = 9"'),
        "The diamond of one is nine.",
        D('Circle choice 4'),
        "So the diamond of seven is nine. Choice four.",
    ]])

    # ---------- Q11 q-548: 3◆(x) − 4x = 10 + 2◆(x), ◆(3) = 22   ==>   5◆(x) − 3x = 8 + 4◆(x), ◆(4) = 20
    _rn_q(M, 'q-548', 'For every number $x$: $5\\cdot\\blacklozenge(x)-3x=8+4\\cdot\\blacklozenge(x)$. $\\blacklozenge(4)=?$',
          ['$12$', '$20$', '$4$', '$28$'], 2, [
        'Treat $\\blacklozenge(x)$ as one unknown and isolate it: $5\\cdot\\blacklozenge(x)-4\\cdot\\blacklozenge(x)=8+3x$, so $\\blacklozenge(x)=3x+8$.',
        'Then $\\blacklozenge(4)=3\\cdot4+8=20$.'])
    _rn_video(M, 'q-548', [[
        "The diamond of x appears on both sides of the equation.",
        "So treat it exactly like an unknown — and isolate it.",
        D('Write "5◆(x) − 4◆(x) = 8 + 3x"'),
        "Move the four diamonds to the left — minus. Move the minus three x to the right — plus.",
        D('Write "◆(x) = 3x + 8"'),
        "Five diamonds minus four diamonds: one diamond. Now it's a normal definition.",
        D('Write "◆(4) = 12 + 8 = 20"'),
        "Diamond of four: three times four plus eight. Twenty.",
        D('Circle choice 2'),
        "Choice two. Once it's isolated, it's a basic question.",
    ]])

    # ---------- Q12 q-549: ◆(t) = t², not always true: ◆(3x) = 3◆(x)   ==>   ◆(5x) = 5◆(x) (now choice 3)
    _rn_q(M, 'q-549', 'For every number $t$: $\\blacklozenge(t)=t^2$. In the choices, $x\\ge0$. Which of the following is not always true?',
          ['$\\blacklozenge(3x)=9\\cdot\\blacklozenge(x)$', '$\\blacklozenge(x)=\\blacklozenge(\\blacklozenge(\\sqrt{x}))$',
           '$\\blacklozenge(5x)=5\\cdot\\blacklozenge(x)$', '$\\blacklozenge(x-2)=\\blacklozenge(2-x)$'], 3, [
        '(3) $\\blacklozenge(5x)=(5x)^2=25x^2$, but $5\\cdot\\blacklozenge(x)=5x^2$. With $x=1$: $25\\ne5$. Not always true — this is the answer.',
        '(1) $\\blacklozenge(3x)=(3x)^2=9x^2=9\\cdot\\blacklozenge(x)$. Always true.',
        '(2) $\\blacklozenge(\\sqrt x)=(\\sqrt x)^2=x$, so $\\blacklozenge(\\blacklozenge(\\sqrt x))=\\blacklozenge(x)$. Always true.',
        '(4) Opposite numbers have the same square, so $(x-2)^2=(2-x)^2$. Always true.',
        'Plugging in? Do not use $x=0$: with $x=0$ every choice looks true.'])
    _rn_video(M, 'q-549', [[
        "The diamond appears in every choice — twice! That's lots of work.",
        "It's a must-be-true question — \"not always true\" means one choice can be broken.",
        "So on the exam: skip it, solve the rest of the section, and come back at the end.",
        "Now let's check. The diamond squares its input.",
        D('Next to choice 1 write "(3x)² = 9x² ✓"'),
        "Choice one: three x, squared, is nine x squared. Nine times x squared — the same. True.",
        D('Next to choice 3 write "(5x)² = 25x² vs 5x² ✗"'),
        "Choice three: five x, squared, is twenty-five x squared. Five times x squared is only five x squared. Not equal!",
        D('Circle choice 3'),
        "We solved it mathematically — so we can mark it right away.",
        "Just to see: choice two: the root, squared — it cancels. True. Choice four: x minus two and two minus x are opposites — squared, they're equal. True.",
    ], [
        "The faster way: plug in x equals one.",
        D('Next to choice 1 write "◆(3) = 9, 9 · ◆(1) = 9 ✓"'),
        "Choice one: the diamond of three is nine. Nine times the diamond of one: nine. Equal.",
        D('Next to choice 2 write "1 = 1 ✓"'),
        "Choice two: one equals one.",
        D('Next to choice 3 write "◆(5) = 25, 5 · ◆(1) = 5 ✗"'),
        "Choice three: the diamond of five is twenty-five. Five times the diamond of one is five. Not equal — found it.",
        D('Next to choice 4 write "1 = 1 ✓"'),
        "Choice four: one minus two is minus one, two minus one is one — both squared give one.",
        D('Circle choice 3'),
        "One warning. Zero or one can make a false rule look true. Here only choice three failed, so we're done.",
        "If two choices had survived, we'd try a second number, like two.",
        "So: skip it at first — and when you come back, plug in. Much faster than opening everything.",
    ]])

    # ---------- Q14 q-550: ◆(1, 1, ◆(1, 2, 2)) = 11   ==>   ◆(1, 1, ◆(2, 1, 3)) = 20
    _rn_q(M, 'q-550', 'For every three numbers $x$, $y$, $z$: $\\blacklozenge(x, y, z)=x^{yz}+y^{xz}+z^{xy}$. $\\blacklozenge(1, 1, \\blacklozenge(2, 1, 3))=?$',
          ['$2$', '$18$', '$20$', '$36$'], 3, [
        'Inner operation first, with $x=2$, $y=1$, $z=3$: $\\blacklozenge(2, 1, 3)=2^{3}+1^{6}+3^{2}=8+1+9=18$.',
        'Outer operation, with $x=1$, $y=1$, $z=18$: $\\blacklozenge(1, 1, 18)=1^{18}+1^{18}+18^{1}=1+1+18=20$.'])
    _rn_video(M, 'q-550', [[
        "A brand-new operation — but only numbers here, no unknowns.",
        "The diamond appears twice. So we'll run the operation twice.",
        "Always start with the inner one.",
        D('Under the inner diamond write "x = 2, y = 1, z = 3"'),
        "Inner diamond: x is two, y is one, z is three.",
        "The rule: each number to the power of the product of the other two.",
        D('Write "2³ + 1⁶ + 3² = 8 + 1 + 9 = 18"'),
        "Two to the power one-times-three: eight. One to the power two-times-three: one. Three to the power two-times-one: nine. Eighteen.",
        D('Write "◆(1, 1, 18)" next to the outer diamond'),
        "Now the outer diamond: one, one, eighteen.",
        D('Write "1¹⁸ + 1¹⁸ + 18¹ = 1 + 1 + 18 = 20"'),
        "One to any power is one. One again. Eighteen to the power one-times-one: eighteen.",
        D('Circle choice 3'),
        "One plus one plus eighteen: twenty. Choice three.",
    ], [
        "Now the psychometric shortcut: look at the OUTER diamond before calculating anything.",
        "Sometimes a zero in the outer call makes the inner value irrelevant. Here there's no zero — but the two ones do something similar.",
        D('Under the outer diamond write "1ᶻ + 1ᶻ + z¹ = 2 + z"'),
        "One to any power is one — twice. And the last number goes to the power one times one: it stays itself.",
        "So the outer diamond is just two plus whatever sits in the third slot.",
        D('Write "2 + 18 = 20" and circle choice 3'),
        "The inner value is eighteen — so two plus eighteen: twenty. Choice three.",
        "Shorter — but only if you spot it under exam pressure. If not, Method 1 always works.",
    ]])

    # ---------- Q15 q-551: #(◆(9, 6), ◆(8, 6)) = 169   ==>   #(◆(10, 6), ◆(5, 4)) = 289
    _rn_q(M, 'q-551', 'For every two numbers $x$ and $y$, two operations are defined:\n'
          '$\\begin{cases} \\blacklozenge(x, y)=x^2-2xy+y^2 \\\\ \\#(x, y)=x^2+2xy+y^2 \\end{cases}$\n$\\#(\\blacklozenge(10, 6), \\blacklozenge(5, 4))=?$',
          ['$256$', '$289$', '$324$', '$361$'], 2, [
        'Recognize the square formulas: $\\blacklozenge(x, y)=(x-y)^2$ and $\\#(x, y)=(x+y)^2$.',
        '$\\blacklozenge(10, 6)=(10-6)^2=16$ and $\\blacklozenge(5, 4)=(5-4)^2=1$.',
        '$\\#(16, 1)=(16+1)^2=17^2=289$.'])
    _rn_video(M, 'q-551', [[
        "Two definitions: the diamond and the hash.",
        "The diamond appears twice inside the brackets — left and right. Then the hash acts on both results.",
        "So three calculations. Start with the left diamond.",
        D('Under ◆(10, 6) write "100 − 120 + 36 = 16"'),
        "Ten squared: a hundred. Minus two times ten times six: minus a hundred twenty. Plus six squared: thirty-six. Sixteen.",
        D('Under ◆(5, 4) write "25 − 40 + 16 = 1"'),
        "Right diamond: twenty-five, minus forty, plus sixteen. One.",
        D('Write "#(16, 1) = 256 + 32 + 1 = 289"'),
        "Now the hash on sixteen and one: two fifty-six, plus two times sixteen times one — thirty-two — plus one.",
        D('Circle choice 2'),
        "Two hundred eighty-nine. Choice two.",
    ], [
        "The psychometric shortcut: recognize the contracted multiplication formulas.",
        D('Next to the diamond\'s definition write "= (x − y)²"'),
        "x squared minus two x y plus y squared — that's x minus y, squared.",
        D('Next to the hash\'s definition write "= (x + y)²"'),
        "And the hash is x plus y, squared.",
        D('Write "◆(10, 6) = 4² = 16,  ◆(5, 4) = 1² = 1"'),
        "Ten minus six, squared: sixteen. Five minus four, squared: one.",
        D('Write "#(16, 1) = 17² = 289" and circle choice 2'),
        "Sixteen plus one, squared: seventeen squared. Two eighty-nine. Choice two.",
        "Much shorter — and the exam rewards those of you who can see it.",
    ]])

    # ---------- Q17 q-552: ◆(x, y) = √(3x² + y²), answer √(13/7)   ==>   √(8x² + y²), answer √(73/17)
    _rn_q(M, 'q-552', 'For every two numbers $x$ and $y$: $\\blacklozenge(x, y)=\\sqrt{8x^2+y^2}$. Given: $a>0$. '
          '$\\frac{\\blacklozenge(\\blacklozenge(a, a), a)}{\\blacklozenge(a, \\blacklozenge(a, a))}=?$',
          ['$1$', '$\\sqrt{\\frac{17}{73}}$', '$\\sqrt{\\frac{73}{17}}$', '$\\sqrt{\\frac{9}{8}}$'], 3, [
        'Inner: $\\blacklozenge(a, a)=\\sqrt{8a^2+a^2}=\\sqrt{9a^2}=3a$.',
        'Top: $3a$ goes into the FIRST slot: $\\blacklozenge(3a, a)=\\sqrt{8\\cdot9a^2+a^2}=\\sqrt{73a^2}=a\\sqrt{73}$.',
        'Bottom: $3a$ goes into the SECOND slot: $\\blacklozenge(a, 3a)=\\sqrt{8a^2+9a^2}=\\sqrt{17a^2}=a\\sqrt{17}$.',
        '$\\frac{a\\sqrt{73}}{a\\sqrt{17}}=\\sqrt{\\frac{73}{17}}$.',
        'Or plug in $a=1$: $\\frac{\\blacklozenge(3, 1)}{\\blacklozenge(1, 3)}=\\frac{\\sqrt{73}}{\\sqrt{17}}$.'])
    _rn_video(M, 'q-552', [[
        "Four diamonds here — but diamond of a, a appears both on top and on the bottom.",
        "So three calculations. Start with the inner one.",
        D('Write "◆(a, a) = √(8a² + a²) = √(9a²) = 3a"'),
        "x is a, y is a: root of eight a squared plus a squared. Root of nine a squared: three a.",
        D('Top: write "◆(3a, a) = √(72a² + a²) = a√73"'),
        "Top: three a goes in the FIRST slot. Squared: nine a squared. Times eight: seventy-two a squared. Plus a squared: root of seventy-three a squared — a root seventy-three.",
        D('Bottom: write "◆(a, 3a) = √(8a² + 9a²) = a√17"'),
        "Bottom: now three a is in the SECOND slot. Eight a squared plus nine a squared: a root seventeen.",
        D('Write "a√73 / a√17 = √(73/17)" and circle choice 3'),
        "Cancel the a's. Root seventy-three over root seventeen — same order of root, so one root: seventy-three seventeenths. Choice three.",
    ], [
        "Now the recommended route: plug in a number.",
        "All the choices are plain numbers — so one substitution is enough. a is positive: take a equals one.",
        D('Write "◆(1, 1) = √(8 + 1) = 3"'),
        "Diamond of one, one: root of nine. Three.",
        D('Top: write "◆(3, 1) = √(72 + 1) = √73"'),
        "Top: diamond of three and one. Three is in the first slot — it gets squared and multiplied by eight. Seventy-two plus one: root seventy-three.",
        "Only choice three has seventy-three on top. A strong hint — but one more line makes it sure.",
        D('Bottom: write "◆(1, 3) = √(8 + 9) = √17"'),
        "Bottom: diamond of one and three. Now three is in the second slot. Eight plus nine: root seventeen.",
        D('Write "√73 / √17 = √(73/17)" and circle choice 3'),
        "Root seventy-three over root seventeen. Choice three.",
        "In operation questions with unknowns, plugging in is the recommended way.",
    ]])

    # ---------- Q18 q-553: (x − y)²/(x²y), answer b/a   ==>   (x − y)²/(xy³), answer a²/b²
    _rn_q(M, 'q-553', 'For every two numbers $x$ and $y$ that are not $0$: $\\blacklozenge(x, y)=\\frac{(x-y)^2}{xy^3}$. '
          'Given: $a$ and $b$ are two different numbers, and neither of them is $0$. $\\frac{\\blacklozenge(a, b)}{\\blacklozenge(b, a)}=?$',
          ['$\\frac{a}{b}$', '$1$', '$\\frac{a^2}{b^2}$', '$\\frac{b^2}{a^2}$'], 3, [
        '$\\blacklozenge(a, b)=\\frac{(a-b)^2}{ab^3}$ and $\\blacklozenge(b, a)=\\frac{(b-a)^2}{ba^3}$.',
        'The tops are equal, because $(b-a)^2=(a-b)^2$. They cancel:',
        '$\\frac{(a-b)^2}{ab^3}\\cdot\\frac{ba^3}{(a-b)^2}=\\frac{ba^3}{ab^3}=\\frac{a^2}{b^2}$.',
        'Check with $a=1$, $b=2$: $\\blacklozenge(1, 2)=\\frac18$ and $\\blacklozenge(2, 1)=\\frac12$, and $\\frac18\\div\\frac12=\\frac14=\\frac{a^2}{b^2}$ ✓.'])
    _rn_video(M, 'q-553', [[
        "Top: diamond of a, b. x is a, y is b.",
        D('Write "◆(a, b) = (a − b)² / (ab³)"'),
        "a minus b, squared, over a times b cubed.",
        D('Write "◆(b, a) = (b − a)² / (ba³)"'),
        "Bottom: diamond of b, a. b minus a, squared, over b times a cubed.",
        D('Write "= (a − b)²/(ab³) · (ba³)/(b − a)²"'),
        "Dividing by a fraction: multiply by its reciprocal.",
        "Tip: don't open the squared brackets yet — they might cancel. And they do.",
        D('Cancel the squared brackets, one a and one b; write "= a²/b²"'),
        "The squares match. One a cancels, one b cancels. a squared over b squared.",
        D('Circle choice 3'),
        "Choice three.",
    ], [
        "For students who see the algebra: the same two letters, just swapped.",
        "Top of the definition: x minus y, squared. a minus b and b minus a are opposites — and squared, they're equal.",
        D('Write "(a − b)² = (b − a)²"'),
        "So the tops cancel completely. Only the bottoms are left — and dividing flips the second one.",
        D('Write "= (ba³) / (ab³) = a²/b²"'),
        "b times a cubed, over a times b cubed. One a and one b cancel: a squared over b squared. One line.",
        D('Circle choice 3'),
        "Choice three.",
    ], [
        "The standard psychometric route: plug in numbers.",
        "Letters in the answers too — so first make sure the choices come out DIFFERENT.",
        "a and b can't be equal, and can't be zero. Try a equals one, b equals two.",
        D('Next to the choices write their values: 1/2, 1, 1/4, 4'),
        "One half, one, one quarter, four. All different — one substitution is enough.",
        D('Write "◆(1, 2) = 1/8,  ◆(2, 1) = 1/2"'),
        "Top: one minus two, squared, is one — over one times two cubed, eight. One eighth. Bottom: one — over two times one. One half.",
        D('Write "(1/8) ÷ (1/2) = 1/4" and circle choice 3'),
        "One eighth divided by one half: one eighth times two. One quarter. Choice three.",
        "Strong at algebra? Use the insight. Everyone else: just plug in.",
    ]])

    # ---------- Q19 q-554: A⁴ + B³ + C², digits 1, 2, 3   ==>   same rule A⁴ + B³ + C², digits 1, 2, 4
    # (review 2026-10-06: the renumber pass had lowered the powers to A³ + B² + C; the Hebrew powers 4, 3, 2 are kept now)
    _rn_q(M, 'q-554', '$A$, $B$ and $C$ are digits from $1$ to $9$. For every three-digit number $ABC$, the operation $\\blacklozenge$ is defined: '
          '$\\blacklozenge(ABC)=A^4+B^3+C^2$. Which of the following is the smallest?',
          ['$\\blacklozenge(214)$', '$\\blacklozenge(142)$', '$\\blacklozenge(412)$', '$\\blacklozenge(124)$'], 4, [
        '$\\blacklozenge(214)=2^4+1^3+4^2=16+1+16=33$.',
        '$\\blacklozenge(142)=1^4+4^3+2^2=1+64+4=69$.',
        '$\\blacklozenge(412)=4^4+1^3+2^2=256+1+4=261$.',
        '$\\blacklozenge(124)=1^4+2^3+4^2=1+8+16=25$.',
        'The smallest is $\\blacklozenge(124)=25$: the biggest power goes on the smallest digit.'])
    _rn_video(M, 'q-554', [[
        "Every choice contains the operation — so we have to evaluate the choices.",
        "The hundreds digit goes to the fourth power, the tens to the third, the units to the second.",
        D('Next to choice 1 write "16 + 1 + 16 = 33"'),
        "Two-one-four: two to the fourth, sixteen. One cubed, one. Four squared, sixteen. Thirty-three.",
        D('Next to choice 2 write "1 + 64 + 4 = 69"'),
        "One-four-two: one, sixty-four, four. Sixty-nine. Bigger — choice two is out.",
        D('Next to choice 3 write "256 + 1 + 4 = 261"'),
        "Four-one-two: two hundred fifty-six, one, four. Two hundred sixty-one. Out.",
        D('Next to choice 4 write "1 + 8 + 16 = 25"'),
        "One-two-four: one, eight, sixteen. Twenty-five. Smaller than thirty-three — so choice one is out too.",
        D('Circle choice 4'),
        "Smallest: twenty-five. Choice four.",
    ], [
        "The psychometric shortcut: think minimum and maximum.",
        "Every choice uses the same digits: one, two, four.",
        "The biggest power — the fourth — goes on the hundreds digit. So that digit must be as small as possible.",
        D('Cross out choices 1 and 3'),
        "Only choices two and four start with one.",
        "Next biggest power — the cube — sits on the tens digit. That one should be the smaller of what's left.",
        D('Circle choice 4'),
        "Two in the tens beats four in the tens. One-two-four. Choice four — without a single full calculation.",
    ]])

    # ---------- Q20 q-555: ◆(x) = 1/x, must be true: ◆(a)·a = ◆(b)·b   ==>   ◆(x) = 3/x, same idea (now choice 2)
    _rn_q(M, 'q-555', 'For every number $x\\ne0$: $\\blacklozenge(x)=\\frac3x$. Which of the following must be true for all positive $a$ and $b$?',
          ['$\\blacklozenge(a)<3$', '$\\blacklozenge(a)\\cdot a=\\blacklozenge(b)\\cdot b$',
           '$\\frac{\\blacklozenge(a)}{\\blacklozenge(b)}=\\frac{a}{b}$', '$\\blacklozenge(a)<\\blacklozenge(a+1)$'], 2, [
        '(2) $\\blacklozenge(a)\\cdot a=\\frac3a\\cdot a=3$ and $\\blacklozenge(b)\\cdot b=\\frac3b\\cdot b=3$. Both sides are always $3$ ✓.',
        '(1) $a=\\frac12$ gives $\\blacklozenge(a)=6$, which is not less than $3$ ✗.',
        '(3) $\\frac{\\blacklozenge(a)}{\\blacklozenge(b)}=\\frac3a\\div\\frac3b=\\frac3a\\cdot\\frac{b}{3}=\\frac{b}{a}$, not $\\frac{a}{b}$ ✗ (for example $a=1$, $b=2$).',
        '(4) A bigger denominator gives a smaller fraction: $\\frac3a>\\frac3{a+1}$. For example $a=1$: $3>\\frac32$ ✗.'])
    _rn_video(M, 'q-555', [[
        "The operation takes a number and gives three over it.",
        "They ask what MUST be true for every positive a and b. We try to break each choice.",
        "Choice one: three over a is less than three?",
        D('Next to choice 1 write "a = 1/2 → 6"'),
        "Technically: multiply both sides by a — it's positive, no flip — and divide by three. You get one less than a. True only when a is above one.",
        "Two, three, four — yes: one and a half, one, three quarters. But a equals one gives exactly three. And a could be a half — then three over a is six. Not always true.",
        D('Cross out choice 1'),
        "On to the second claim.",
        D('Next to choice 2 write "(3/a) · a = 3 = (3/b) · b ✓"'),
        "Choice two: three over a, times a — the a cancels. Three. Three over b, times b — also three. Three equals three, for every a and b. Keep it — and break the others to be sure.",
        D('Next to choice 3 write "(3/a) ÷ (3/b) = b/a"'),
        "Choice three: three over a, divided by three over b: b over a — not a over b. Dividing by a fraction is multiplying by its reciprocal.",
        D('Cross out choice 3'),
        "Choice four: three over a less than three over a plus one?",
        D('Next to choice 4 write "a + 1 < a → 1 < 0 ✗"'),
        "Both sides positive, so cross-multiply without flipping, and divide by three: a plus one less than a. One less than zero — never true.",
        "Or by understanding: a bigger denominator makes a SMALLER fraction. a equals two: three halves is not less than one.",
        D('Cross out choice 4 and circle choice 2'),
        "Three out, and choice two holds every time. Choice two.",
    ]])

    # ---------- Q21 q-556: ⟦x⟧ = number of 3s in the prime factorization   ==>   number of 5s (key now choice 4)
    _rn_q(M, 'q-556', 'For every positive integer $x$, ⟦$x$⟧ is the number of times $5$ appears in the prime factorization of $x$. '
          'For example, $50=2\\cdot5\\cdot5$ has two 5s, so ⟦$50$⟧ is $2$. Which of the following must be true?',
          ['⟦$5x$⟧ $=$ ⟦$x^2$⟧', '⟦$x+5$⟧ $=$ ⟦$x$⟧ $+1$', '⟦$5x$⟧ $=5\\cdot$ ⟦$x$⟧', '⟦$5x$⟧ $=$ ⟦$x$⟧ $+1$'], 4, [
        'Multiplying $x$ by $5$ adds exactly one more $5$ to its prime factorization. So ⟦$5x$⟧ $=$ ⟦$x$⟧ $+1$ always ✓.',
        'For example $x=50$: $250=2\\cdot5^3$, so ⟦$250$⟧ $=3=2+1$.',
        'The others break: (1) $x=2$: ⟦$10$⟧ $=1$, but ⟦$4$⟧ $=0$ ✗. (2) $x=5$: ⟦$10$⟧ $=1$, but ⟦$5$⟧ $+1=2$ ✗. (3) $x=5$: ⟦$25$⟧ $=2$, but $5\\cdot$ ⟦$5$⟧ $=5$ ✗.'])
    _rn_video(M, 'q-556', [[
        "First, understand the operation through its example.",
        A("'Definition in words? Write 2–3 examples first' appears", T('Definition in words? Write $2$–$3$ examples first', size=36)),
        "A definition in words — a remainder, the number of divisors, the sum of the digits — is easy to misread. Write two or three quick examples first.",
        D('Under the example write "50 = 2 · 5 · 5 → two 5s"'),
        "Fifty breaks into two, five, five. The factor five appears twice. So the answer is two.",
        "Understanding here isn't simple — so plug in first. The simplest value: x equals one. No fives inside at all.",
        D('Next to choice 1 write "⟦5⟧ = 1 ≠ ⟦1⟧ = 0"'),
        "Choice one: five times one is five — one five. One squared is one — no fives. One versus zero. False.",
        D('Cross out choice 1'),
        D('Next to choice 2 write "⟦6⟧ = 0 ≠ 1"'),
        "Choice two: one plus five is six — no fives. Zero. But zero plus one is one. False.",
        D('Cross out choice 2'),
        D('Next to choice 3 write "1 ≠ 5 · 0"'),
        "Choice three: one versus five times zero. False.",
        D('Next to choice 4 write "⟦5⟧ = 1 = 0 + 1"'),
        "Choice four: five times one is five — one five. And zero plus one: one. True.",
        D('Cross out choice 3 and circle choice 4'),
        "Three eliminated. Choice four.",
        "One is a risky number — it can make a false rule look true. But here three choices failed and only one survived. Safe.",
    ], [
        "Now why choice four is always true.",
        "Multiply x by five — you add exactly one more five to its factors. So the count goes up by exactly one.",
        "Choice two ADDS five. Adding doesn't tell you anything about the factors.",
        "Choice one squares x — squaring DOUBLES the number of fives.",
        D('Next to choice 3 write "x = 5³: 4 ≠ 15"'),
        "Choice three multiplies the COUNT by five. Take x as five cubed: times five gives four fives — not fifteen.",
        D('Circle choice 4'),
        "Only choice four holds every time.",
    ]])


def rn_practice_questions(M):
    S = lambda *a: _rn_q(M, *a)
    S('q-557', 'For all $a$ and $b$ with $a\\ge b\\ge0$: $\\blacklozenge(a, b)=\\sqrt{\\sqrt a-\\sqrt b}$. $\\frac{\\blacklozenge(169, 16)}{\\blacklozenge(36, 25)}=?$',
      ['$\\sqrt3$', '$9$', '$3$', '$1$'], 3, [
        '$\\blacklozenge(169, 16)=\\sqrt{\\sqrt{169}-\\sqrt{16}}=\\sqrt{13-4}=\\sqrt9=3$.',
        '$\\blacklozenge(36, 25)=\\sqrt{\\sqrt{36}-\\sqrt{25}}=\\sqrt{6-5}=\\sqrt1=1$.',
        '$\\frac31=3$. (Forgetting the outer root gives $9$.)'])
    S('q-558', 'For every two different numbers $x$ and $y$, two operations are defined:\n'
      '$\\blacklozenge(x, y)$ = the smaller of $x$ and $y$\n$\\#(x, y)$ = the larger of $x$ and $y$\n'
      '$\\#(\\blacklozenge(8, 5), \\blacklozenge(12, 2))=?$',
      ['$2$', '$5$', '$8$', '$12$'], 2, [
        '$\\blacklozenge(8, 5)=5$ (the smaller) and $\\blacklozenge(12, 2)=2$.',
        'Then $\\#(5, 2)=5$ (the larger).'])
    S('q-559', 'For every two numbers $x$ and $y$: $\\blacklozenge(x, y)=\\sqrt{x^2+y^2}$. $\\blacklozenge(\\blacklozenge(4, 1), 8)=?$',
      ['$9$', '$17$', '$8$', '$5$'], 1, [
        'Inner: $\\blacklozenge(4, 1)=\\sqrt{16+1}=\\sqrt{17}$.',
        'Outer: $\\blacklozenge(\\sqrt{17}, 8)=\\sqrt{(\\sqrt{17})^2+8^2}=\\sqrt{17+64}=\\sqrt{81}=9$.'])
    S('q-560', 'For every number $x$: $\\blacklozenge(x)=x(x-3)$. $\\blacklozenge(\\blacklozenge(4))=?$',
      ['$1$', '$3$', '$4$', '$16$'], 3, [
        'Inner: $\\blacklozenge(4)=4\\cdot(4-3)=4\\cdot1=4$.',
        'Outer: $\\blacklozenge(4)=4$ again. The operation sends $4$ back to $4$.'])
    S('q-561', 'For every positive integer $a$: $\\blacklozenge(a)=\\frac{a}{a+1}$. '
      '$\\blacklozenge(2)\\cdot\\blacklozenge(3)\\cdot\\blacklozenge(4)\\cdot\\blacklozenge(5)\\cdot\\blacklozenge(6)\\cdot\\blacklozenge(7)=?$',
      ['$\\frac{1}{8}$', '$\\frac{1}{4}$', '$\\frac{7}{8}$', '$\\frac{1}{7}$'], 2, [
        '$\\frac23\\cdot\\frac34\\cdot\\frac45\\cdot\\frac56\\cdot\\frac67\\cdot\\frac78$.',
        'Each top cancels the bottom before it: $3$, $4$, $5$, $6$ and $7$ all cancel. What is left: $\\frac28=\\frac14$.',
        'The trap $\\frac18$ forgets that the product starts at $\\blacklozenge(2)$, so the first top is $2$, not $1$.'])
    S('q-562', 'For every number $x$: $\\blacklozenge(x)=x(x+5)(x-2)$. For how many different values of $x$ is $\\blacklozenge(x)$ equal to $0$?',
      ['$1$', '$2$', '$0$', '$3$'], 4, [
        'A product is $0$ exactly when one of its factors is $0$: $x=0$, or $x+5=0$, or $x-2=0$.',
        'So $x=0$, $x=-5$ or $x=2$. Three values.'])
    S('q-563', 'For every number $a$: $\\blacklozenge(a^2)=|a|$. $\\blacklozenge\\left(\\frac1{16}\\right)=?$',
      ['$\\frac{1}{16}$', '$\\frac{1}{32}$', '$\\frac{1}{4}$', '$\\frac{1}{256}$'], 3, [
        'The input is $a^2$. Find $a$ with $a^2=\\frac1{16}$: $a=\\frac14$ or $a=-\\frac14$.',
        'Either way $|a|=\\frac14$. So $\\blacklozenge\\left(\\frac1{16}\\right)=\\frac14$.'])
    S('q-564', 'For every number $a$: $\\blacklozenge(a)=a^5+a^4+a^3+a^2+a+1$. $\\blacklozenge(1)-\\blacklozenge(-1)=?$',
      ['$6$', '$3$', '$0$', '$1$'], 1, [
        '$\\blacklozenge(1)$: all $6$ terms are $1$, so $\\blacklozenge(1)=6$.',
        '$\\blacklozenge(-1)=-1+1-1+1-1+1=0$.',
        '$6-0=6$.',
        'Shortcut: in $\\blacklozenge(1)-\\blacklozenge(-1)$ the even powers and the constant cancel. Only the $3$ odd powers are left, doubled: $2\\cdot3=6$.'])
    S('q-565', 'For every two numbers $a$ and $b$:\n'
      '$a\\blacklozenge b=\\begin{cases} \\frac{a+b}{a-b}, & a\\ne b \\\\ 0, & a=b \\end{cases}$\n$(5\\blacklozenge3)\\blacklozenge4=?$',
      ['$4$', '$1$', '$0$', '$-1$'], 3, [
        'Inner: $5\\ne3$, so $5\\blacklozenge3=\\frac{5+3}{5-3}=\\frac82=4$.',
        'Outer: $4\\blacklozenge4$ has $a=b$, so the second rule gives $0$.'])
    S('q-566', 'For every number $x$: $\\blacklozenge(x)+2=10x-\\blacklozenge(x)$. $\\blacklozenge(3)=?$',
      ['$16$', '$14$', '$28$', '$13$'], 2, [
        'Collect the $\\blacklozenge(x)$ terms: $2\\cdot\\blacklozenge(x)=10x-2$, so $\\blacklozenge(x)=5x-1$.',
        '$\\blacklozenge(3)=5\\cdot3-1=14$.'])
    S('q-567', 'For two positive integers $x$ and $y$, $x\\sim y$ is the number you get when you write the digits of $x$ '
      'and then the digits of $y$. For example: $36\\sim7=367$. '
      'Which of the following is not always true for positive integers $x$, $y$ and $z$?',
      ['$x\\sim y=y\\sim x$', '$x<2\\sim x$', '$x\\sim3=10x+3$', '$(x\\sim y)\\sim z=x\\sim(y\\sim z)$'], 1, [
        'One counterexample is enough: $36\\sim7=367$, but $7\\sim36=736$. So (1) is not always true.',
        'The others are always true. (2) $2\\sim x$ has one more digit than $x$, so it is bigger. '
        '(3) Writing the digit $3$ after $x$ moves every digit of $x$ one place to the left and adds $3$: for example $58\\sim3=583=10\\cdot58+3$. '
        '(4) Both sides are the digits of $x$, then $y$, then $z$, in that order.'])
    S('q-568', 'For every number $x$: $\\blacklozenge(x)=x^4+2x^2+7x-5$. $\\blacklozenge(3)-\\blacklozenge(-3)=?$',
      ['$42$', '$0$', '$230$', '$84$'], 1, [
        '$\\blacklozenge(3)=81+18+21-5=115$ and $\\blacklozenge(-3)=81+18-21-5=73$.',
        '$115-73=42$.',
        'Shortcut: the even powers and the constant are the same for $3$ and $-3$, so they cancel. Only $7x$ is left, doubled: $2\\cdot7\\cdot3=42$.'])
    S('q-569', 'For every positive integer $n$:\n'
      '$\\blacklozenge(n)=\\begin{cases} 7, & n=1 \\\\ \\blacklozenge(n-1)+3, & n>1 \\end{cases}$\n$\\blacklozenge(5)=?$',
      ['$22$', '$16$', '$19$', '$15$'], 3, [
        'Climb up from the start value: $\\blacklozenge(1)=7$, $\\blacklozenge(2)=10$, $\\blacklozenge(3)=13$, $\\blacklozenge(4)=16$, $\\blacklozenge(5)=19$.',
        'Or: four steps of $+3$ above the start value: $7+4\\cdot3=19$.'])
    S('q-570', 'For every number $x$, two operations are defined:\n'
      '$\\begin{cases} \\blacklozenge(x)=x+5 \\\\ \\#(x)=x^2 \\end{cases}$\nGiven: $\\blacklozenge(\\#(a))=\\#(\\blacklozenge(a))$. $a=?$',
      ['$2$', '$-2$', '$0$', '$-5$'], 2, [
        'Left side: $\\blacklozenge(\\#(a))=\\blacklozenge(a^2)=a^2+5$.',
        'Right side: $\\#(\\blacklozenge(a))=\\#(a+5)=(a+5)^2=a^2+10a+25$.',
        '$a^2+5=a^2+10a+25$, so $10a=-20$ and $a=-2$.',
        'Check: $\\blacklozenge(\\#(-2))=\\blacklozenge(4)=9$ and $\\#(\\blacklozenge(-2))=\\#(3)=9$ ✓.'])
    S('q-571', 'For every integer $n$ from $1$ to $9$, $\\blacklozenge(n)$ is the number of two-digit numbers whose tens digit is $n$ '
      'and whose units digit is smaller than $n$. $\\blacklozenge(n)=?$',
      ['$10-n$', '$n+1$', '$n$', '$n-1$'], 3, [
        'Examples first. $n=4$: the numbers $40$, $41$, $42$, $43$. Four numbers, so $\\blacklozenge(4)=4$.',
        'In general, the units digit can be $0, 1, \\ldots, n-1$: that is $n$ digits. So $\\blacklozenge(n)=n$.'])
    S('q-572', 'For every two integers $a$ and $b$ that are not $0$: $\\blacklozenge(a, b)=\\frac{a}{b}-\\frac{b}{a}$. $\\blacklozenge(-1, 3)=?$',
      ['$\\blacklozenge(1, 3)$', '$\\blacklozenge(-3, 1)$', '$\\blacklozenge(3, 1)$', '$\\blacklozenge(3, -1)$'], 3, [
        '$\\blacklozenge(-1, 3)=\\frac{-1}{3}-\\frac{3}{-1}=-\\frac13+3=\\frac83$.',
        'Now the choices: $\\blacklozenge(3, 1)=3-\\frac13=\\frac83$ ✓.',
        'The others: $\\blacklozenge(1, 3)=\\frac13-3=-\\frac83$, $\\blacklozenge(-3, 1)=-3+\\frac13=-\\frac83$, $\\blacklozenge(3, -1)=-3+\\frac13=-\\frac83$.'])
    S('q-573', 'For every number $x\\ne0$: $\\blacklozenge(x)=\\frac{x-3}{x}$. Which of the following must be true for all $a>3$ and $b>3$?',
      ['if $a<b$ then $\\blacklozenge(b)<\\blacklozenge(a)$', '$2\\cdot\\blacklozenge(a)=\\blacklozenge(2a)$',
       '$\\blacklozenge(a)\\cdot\\blacklozenge(b)<1$', '$(\\blacklozenge(a))^2=\\blacklozenge(a^2)$'], 3, [
        'Rewrite: $\\blacklozenge(x)=1-\\frac3x$. For $x>3$, $0<\\frac3x<1$, so $0<\\blacklozenge(x)<1$.',
        '(3) Two numbers between $0$ and $1$ have a product smaller than $1$. Always true ✓.',
        '(1) As $x$ grows, $\\frac3x$ shrinks, so $\\blacklozenge(x)$ grows: $a<b$ gives $\\blacklozenge(a)<\\blacklozenge(b)$. The claim is the reverse ✗.',
        '(2) $a=6$: $2\\cdot\\blacklozenge(6)=2\\cdot\\frac12=1$, but $\\blacklozenge(12)=\\frac34$ ✗.',
        '(4) $a=6$: $(\\blacklozenge(6))^2=\\frac14$, but $\\blacklozenge(36)=\\frac{11}{12}$ ✗.'])
    S('q-574', 'For every number $x$: $\\blacklozenge(x)=x^2-9$. Given: $a>0$ and $b>0$. Which of the following must be true?',
      ['$\\blacklozenge(a+b)=\\blacklozenge(a)+\\blacklozenge(b)$', '$\\sqrt{\\blacklozenge(a)+9}=\\frac{\\blacklozenge(a)}{a+3}+3$',
       '$\\blacklozenge(\\blacklozenge(a))=a$', '$\\blacklozenge(b)=(b-3)\\cdot\\blacklozenge(\\sqrt{b})$'], 2, [
        '(2) Left side: $\\sqrt{a^2-9+9}=\\sqrt{a^2}=a$ ($a$ is positive). Right side: $\\frac{a^2-9}{a+3}+3=\\frac{(a-3)(a+3)}{a+3}+3=a-3+3=a$. Always equal ✓.',
        '(1) $a=b=1$: $\\blacklozenge(2)=-5$, but $\\blacklozenge(1)+\\blacklozenge(1)=-16$ ✗.',
        '(3) $a=4$: $\\blacklozenge(4)=7$ and $\\blacklozenge(7)=40\\ne4$ ✗.',
        '(4) $b=16$: $\\blacklozenge(16)=247$, but $(16-3)\\cdot\\blacklozenge(4)=13\\cdot7=91$ ✗.'])
    S('q-575', 'For every number $x$: $\\blacklozenge(x)=(x-4)(x+1)$. For how many values of $a$ is $\\blacklozenge(a)$ equal to $\\blacklozenge(a+4)$?',
      ['$2$', '$1$', 'Infinitely many', '$3$'], 2, [
        '$\\blacklozenge(a)=(a-4)(a+1)=a^2-3a-4$.',
        '$\\blacklozenge(a+4)=(a+4-4)(a+4+1)=a(a+5)=a^2+5a$.',
        '$a^2-3a-4=a^2+5a$: the $a^2$ cancels, so $-4=8a$ and $a=-\\frac12$. Exactly one value.'])
    S('q-576', 'For every two positive integers $a$ and $b$, $\\blacklozenge(a, b)$ is the remainder when $a$ is divided by $b$. '
      '$\\blacklozenge(\\blacklozenge(38, 7), \\blacklozenge(23, 6))=?$',
      ['$2$', '$0$', '$3$', '$1$'], 3, [
        '$38=5\\cdot7+3$, so $\\blacklozenge(38, 7)=3$.',
        '$23=3\\cdot6+5$, so $\\blacklozenge(23, 6)=5$.',
        '$\\blacklozenge(3, 5)$: $3=0\\cdot5+3$, so the remainder is $3$. (A smaller number divided by a bigger one leaves itself.)'])


def rn_practice(M):
    """Approved clean-up: copies out, at most 3 extra-bank warm-ups, September items whose type the Hebrew covers out."""
    X = 'alg-extra-unit-t19-3-'; N = lambda k: 'q-r26-t19-' + k
    out = [
        # copies (practice_audit/copies_by_topic.txt, each checked)
        X + '3',            # F(F(2)) with x^2 - 3: nested-and-stop-halfway, as guided Q2 and q-559 / q-560
        X + '6',            # H(H(4)) with 1/x: "c/x undoes itself", the idea of guided Q13
        # extra-bank warm-ups beyond 3 (kept: X1 a*b = 2a - b, X5 G(t) = 19 unknown input, X7 (-2)o3 brackets)
        X + '2',            # a + b + ab at (2, 3): same move as X1
        X + '4',            # a◇b - b◇a: the swap-the-letters check of guided Q5 and q-567
        # September items of a type the Hebrew practice (or a kept item) already covers
        N('06'),            # x^2 + 3x at -2: brackets on a negative input - X7, q-572
        N('08'),            # (x+1)/(x-1) at 1/x: expression input - kept N('07')
        N('09'),            # find the operation from two values: guided Q3 (q-543)
        N('10'),            # nested odd/even rule: q-565, guided Q7
        N('12'),            # circular rule: q-569, guided Q9 and Q10
        N('13'),            # nested 1/(1-x) three times: q-559, q-560
        N('15'),            # sum of the digits (definition in words): q-571, q-576
        N('16'),            # a*b = ab - a - b, "always" (swap the letters): q-567, guided Q5
        N('17'),            # must be true with x^3: q-573, q-574
    ]
    for qid in out:
        if qid in M.D['questions'] and any(f['ref'] == qid for f in M.D['flow']) and M.section_of(qid) == PRACTICE:
            M.unplace(qid)
    M.practice_order(PRACTICE, [
        X + '1', X + '7', X + '5', 'q-558', 'q-557', 'q-559', 'q-560', N('07'), 'q-563', 'q-566', 'q-569', 'q-565',
        'q-561', 'q-562', 'q-576', 'q-571', 'q-564', 'q-568', N('11'), 'q-572', 'q-570', 'q-575', N('19'), N('20'),
        'q-567', 'q-573', 'q-574'])


def rn_titles(M):
    """Solution videos: title and slide description show the new stems."""
    for f in M.D['flow']:
        if f['topic'] != TOPIC or f['type'] != 'video': continue
        v = M.video(f['ref']); qid = v.get('questionId')
        if not qid or qid not in M.D['questions'] or f['ref'].startswith('solve-q-r26') or f['ref'] in RN_RECORDED: continue
        stem = M.q(qid)['stem']
        v['title'] = v['navLabel'] = stem
        for b in v['beats']:
            if b['mode'] == 'question':
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, stem)
        M.touched_videos.add(f['ref'])


def renumber_pass(M):
    rn_lessons(M)
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_titles(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-06 Hebrew back-check: the renumber pass above was compared with base-v18 only. Checked again against the
# teacher's Hebrew VIDEO subtitles (01-Algebra-Original-Subtitles.txt, lines 18765-19911): these items had landed
# back on the Hebrew videos' numbers / definitions, so they get new numbers once more (same type, trap, level,
# methods). Nothing in topic 19 is recorded. Runs LAST.
# ======================================================================================================
def hebrew_backcheck(M):
    B = '\\blacklozenge'
    # ---------- lesson slide 3: heart a ♥ b = 2(a + b) (= the Hebrew definition)  ==>  a ♥ b = 5(a + b), 7 ♥ 3 = 50
    _rn_sub(M, LESSON, 3, [
        ('$a\\heartsuit b=2(a+b)$', '$a\\heartsuit b=5(a+b)$'), ('a ♥ b = 2(a + b)', 'a ♥ b = 5(a + b)'),
        ('then multiply the sum by two.', 'then multiply the sum by five.'),
        ('Under 7 ♥ 3 write "= 2(7 + 3) = 2 · 10 = 20"', 'Under 7 ♥ 3 write "= 5(7 + 3) = 5 · 10 = 50"'),
        ('Seven plus three is ten. Times two: twenty.', 'Seven plus three is ten. Times five: fifty.'),
        ('Next to it write "7 · 2 + 3 = 17" and cross it out', 'Next to it write "7 · 5 + 3 = 38" and cross it out'),
        ("Seven times two, plus three, is seventeen — that's a different rule.",
         "Seven times five, plus three, is thirty-eight — that's a different rule.")])
    for r in M.card(CARD)['tables'][0]['rows']:
        if r[0] == 'Basic': r[2] = '$a\\heartsuit b=5(a+b)$: $7\\heartsuit3=50$'

    # ---------- q-542: ◆(x) = x², ◆(◆(3)) = 81 (= the Hebrew lesson example)  ==>  ◆(◆(5)) = 625
    _rn_q(M, 'q-542', 'The operation $\\blacklozenge$ is defined for every number $x$: $\\blacklozenge(x)=x^2$. $\\blacklozenge(\\blacklozenge(5))=?$',
          ['$25$', '$125$', '$625$', '$5$'], 3, [
        'Work from the inside out: $\\blacklozenge(5)=5^2=25$.',
        'Then $\\blacklozenge(\\blacklozenge(5))=\\blacklozenge(25)=25^2=625$.',
        'Stopping at $25$ is the trap.'])
    _rn_video(M, 'q-542', [[
        "A diamond inside a diamond. Like any brackets — start from the inside.",
        D('Underline the inner ◆(5)'),
        "First: the diamond of five.",
        D('Write "◆(5) = 5² = 25"'),
        "The diamond squares — five squared is twenty-five.",
        D('Write "◆(◆(5)) = ◆(25)"'),
        "Now put twenty-five in its place. The outer diamond works on twenty-five.",
        D('Write "= 25² = 625" and circle choice 3'),
        "Twenty-five squared: six hundred twenty-five. Choice three.",
        "Stopping at twenty-five is the trap — and twenty-five is waiting among the choices.",
    ], [
        "Or think about the rule itself: squaring, then squaring again.",
        D('Write "(x²)² = x⁴ → 5⁴ = 625"'),
        "That's x to the fourth. Five to the fourth: six hundred twenty-five.",
    ]])

    # ---------- q-545: odd 2x / even x² − 3, ◆◆◆(3) = 66 (Hebrew: 2x / x² − 5 from 3)  ==>  odd 4x / even x² − 9, ◆◆◆(1) = 28
    _rn_q(M, 'q-545', 'The operation $\\blacklozenge$ is defined for every integer $x$:\n'
          '$\\blacklozenge(x)=\\begin{cases} 4x, & x \\text{ odd} \\\\ x^2-9, & x \\text{ even} \\end{cases}$\n'
          '$\\blacklozenge(\\blacklozenge(\\blacklozenge(1)))=?$',
          ['$7$', '$16$', '$28$', '$4$'], 3, [
        '$1$ is odd: $\\blacklozenge(1)=4\\cdot1=4$.',
        '$4$ is even: $\\blacklozenge(4)=4^2-9=7$.',
        '$7$ is odd: $\\blacklozenge(7)=4\\cdot7=28$.',
        'Check odd or even again before every step.'])
    _rn_video(M, 'q-545', [[
        "Two rules: one for odd x, one for even x.",
        "Three diamonds — so, as always, start from the inside.",
        D('Write "◆(1): 1 odd → 4 · 1 = 4"'),
        "One is odd. The odd rule: four x. Four.",
        D('Write "◆(4): 4 even → 4² − 9 = 7"'),
        "Now four goes in. Four is even — switch rules! Four squared minus nine: seven.",
        D('Write "◆(7): 7 odd → 4 · 7 = 28"'),
        "Seven is odd again. Times four: twenty-eight.",
        D('Circle choice 3'),
        "Choice three.",
        "Check the parity every single time — the output can switch sides.",
    ]])

    # ---------- q-549: choices ◆(3x) = 9◆(x), ◆(x) = ◆(◆(√x)) (= the Hebrew choices)  ==>  ◆(6x) = 36◆(x), ◆(√x)·◆(√x) = ◆(x),
    #            ◆(x − 7) = ◆(7 − x); the answer ◆(5x) = 5◆(x) stays choice 3
    _rn_q(M, 'q-549', 'For every number $t$: $\\blacklozenge(t)=t^2$. In the choices, $x\\ge0$. Which of the following is not always true?',
          ['$\\blacklozenge(6x)=36\\cdot\\blacklozenge(x)$', '$\\blacklozenge(\\sqrt{x})\\cdot\\blacklozenge(\\sqrt{x})=\\blacklozenge(x)$',
           '$\\blacklozenge(5x)=5\\cdot\\blacklozenge(x)$', '$\\blacklozenge(x-7)=\\blacklozenge(7-x)$'], 3, [
        '(3) $\\blacklozenge(5x)=(5x)^2=25x^2$, but $5\\cdot\\blacklozenge(x)=5x^2$. With $x=1$: $25\\ne5$. Not always true — this is the answer.',
        '(1) $\\blacklozenge(6x)=(6x)^2=36x^2=36\\cdot\\blacklozenge(x)$. Always true.',
        '(2) $\\blacklozenge(\\sqrt x)=(\\sqrt x)^2=x$, so $\\blacklozenge(\\sqrt x)\\cdot\\blacklozenge(\\sqrt x)=x\\cdot x=x^2=\\blacklozenge(x)$. Always true.',
        '(4) Opposite numbers have the same square, so $(x-7)^2=(7-x)^2$. Always true.',
        'Plugging in? Do not use $x=0$: with $x=0$ every choice looks true.'])
    _rn_video(M, 'q-549', [[
        "The diamond appears in every choice — two or three times! That's lots of work.",
        "It's a must-be-true question — \"not always true\" means one choice can be broken.",
        "So on the exam: skip it, solve the rest of the section, and come back at the end.",
        "Now let's check. The diamond squares its input.",
        D('Next to choice 1 write "(6x)² = 36x² ✓"'),
        "Choice one: six x, squared, is thirty-six x squared. Thirty-six times x squared — the same. True.",
        D('Next to choice 3 write "(5x)² = 25x² vs 5x² ✗"'),
        "Choice three: five x, squared, is twenty-five x squared. Five times x squared is only five x squared. Not equal!",
        D('Circle choice 3'),
        "We solved it mathematically — so we can mark it right away.",
        "Just to see: choice two: the root, squared, is x — and x times x is x squared. True. Choice four: x minus seven and seven minus x are opposites — squared, they're equal. True.",
    ], [
        "The faster way: plug in x equals one.",
        D('Next to choice 1 write "◆(6) = 36, 36 · ◆(1) = 36 ✓"'),
        "Choice one: the diamond of six is thirty-six. Thirty-six times the diamond of one: thirty-six. Equal.",
        D('Next to choice 2 write "1 · 1 = 1 ✓"'),
        "Choice two: one times one equals one.",
        D('Next to choice 3 write "◆(5) = 25, 5 · ◆(1) = 5 ✗"'),
        "Choice three: the diamond of five is twenty-five. Five times the diamond of one is five. Not equal — found it.",
        D('Next to choice 4 write "◆(−6) = 36 = ◆(6) ✓"'),
        "Choice four: one minus seven is minus six, seven minus one is six — both squared give thirty-six.",
        D('Circle choice 3'),
        "One warning. Zero or one can make a false rule look true. Here only choice three failed, so we're done.",
        "If two choices had survived, we'd try a second number, like two.",
        "So: skip it at first — and when you come back, plug in. Much faster than opening everything.",
    ]])

    # ---------- q-550: inner ◆(2, 1, 3) = 18 (= the Hebrew inner value, digits 1, 2, 3)  ==>  ◆(1, 1, ◆(2, 1, 4)) = 35
    _rn_q(M, 'q-550', 'For every three numbers $x$, $y$, $z$: $\\blacklozenge(x, y, z)=x^{yz}+y^{xz}+z^{xy}$. $\\blacklozenge(1, 1, \\blacklozenge(2, 1, 4))=?$',
          ['$2$', '$33$', '$35$', '$66$'], 3, [
        'Inner operation first, with $x=2$, $y=1$, $z=4$: $\\blacklozenge(2, 1, 4)=2^{4}+1^{8}+4^{2}=16+1+16=33$.',
        'Outer operation, with $x=1$, $y=1$, $z=33$: $\\blacklozenge(1, 1, 33)=1^{33}+1^{33}+33^{1}=1+1+33=35$.'])
    _rn_video(M, 'q-550', [[
        "A brand-new operation — but only numbers here, no unknowns.",
        "The diamond appears twice. So we'll run the operation twice.",
        "Always start with the inner one.",
        D('Under the inner diamond write "x = 2, y = 1, z = 4"'),
        "Inner diamond: x is two, y is one, z is four.",
        "The rule: each number to the power of the product of the other two.",
        D('Write "2⁴ + 1⁸ + 4² = 16 + 1 + 16 = 33"'),
        "Two to the power one-times-four: sixteen. One to the power two-times-four: one. Four to the power two-times-one: sixteen. Thirty-three.",
        D('Write "◆(1, 1, 33)" next to the outer diamond'),
        "Now the outer diamond: one, one, thirty-three.",
        D('Write "1³³ + 1³³ + 33¹ = 1 + 1 + 33 = 35"'),
        "One to any power is one. One again. Thirty-three to the power one-times-one: thirty-three.",
        D('Circle choice 3'),
        "One plus one plus thirty-three: thirty-five. Choice three.",
    ], [
        "Now the psychometric shortcut: look at the OUTER diamond before calculating anything.",
        "Sometimes a zero in the outer call makes the inner value irrelevant. Here there's no zero — but the two ones do something similar.",
        D('Under the outer diamond write "1ᶻ + 1ᶻ + z¹ = 2 + z"'),
        "One to any power is one — twice. And the last number goes to the power one times one: it stays itself.",
        "So the outer diamond is just two plus whatever sits in the third slot.",
        D('Write "2 + 33 = 35" and circle choice 3'),
        "The inner value is thirty-three — so two plus thirty-three: thirty-five. Choice three.",
        "Shorter — but only if you spot it under exam pressure. If not, Method 1 always works.",
    ]])
    rn_titles(M)   # video titles / slide descriptions show the new stems


_apply_before_hebrew = apply


def apply(M):
    _apply_before_hebrew(M)
    hebrew_backcheck(M)   # 2026-10-06 Hebrew back-check: runs last


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
    # new-operation "Brackets on every input": a negative number goes into brackets was taught in topic 8 (Exponent
    # Laws, Negative bases) and topic 4. That part becomes one line; the whole-expression input (x + 2) stays.
    G = 'new-operation'
    if not R.recorded(G):
        s = R.lines_of(M, G, 'Brackets on every input')
        s = R.drop_lines(s, "Without brackets you'd write")
        s = R.replace_line(s, 'Next to it write "= (−3)²', D('Next to it write "= (−3)² − 2 · (−3) = 15"'))
        s = R.replace_line(s, 'Minus three, in brackets, squared', 'A negative goes in brackets — as always with powers. Nine plus six: fifteen.')
        R.set_slide(M, G, 'Brackets on every input', s)


_apply_before_trim_added_repeats = apply


def apply(M):
    _apply_before_trim_added_repeats(M)
    trim_added_repeats(M)   # 2026-10-07 trim added repeats: runs last


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
    _mn_load().method_names(M, 19)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 coverage fixes. A full check compared the teacher's Hebrew course with the English course; the points
# found WEAK / MISSING here are put back as a few short spoken lines (board items by click) in UNRECORDED videos, or -
# when the video is recorded - in the written solution / memory card. Helpers: _cov_fix_a.py (time-gated: a take
# recorded before its CUTOFF keeps the video as recorded). See tNN_CHANGES.md ("2026-10-08 coverage fixes"). Runs LAST.
# =====================================================================================================================
import importlib.util as _ilu_cf, os as _os_cf
_s_cf = _ilu_cf.spec_from_file_location('_cov_fix_a', _os_cf.path.join(_os_cf.path.dirname(_os_cf.path.abspath(__file__)), '_cov_fix_a.py'))
CF = _ilu_cf.module_from_spec(_s_cf); _s_cf.loader.exec_module(CF)


def coverage_fixes(M):
    # Hebrew 19305-19319 (teacher 2026-10-08: two lines + a mini example, don't change the question): a 0 in the outer
    # call makes the inner value irrelevant - anything^0 = 1, 0^positive = 0, 1^anything = 1
    CF.replace_line(M, 'solve-q-550', 'Method 2 · Insight', 'Sometimes a zero in the outer call', [
        'Sometimes a zero in the outer call makes the inner value irrelevant.',
        A("'◆(◆(5, 3, 2), 0, 1) = (…)⁰ + 0^(…) + 1⁰ = 2' appears",
          T('$\\blacklozenge(\\blacklozenge(5,3,2),\\,0,\\,1)=(\\ldots)^0+0^{(\\ldots)}+1^0=1+0+1=2$', size=36)),
        'Say the outer call were: the inner diamond, zero, one. The inner value to the power zero: one. Zero to a positive power: zero. One to any power: one.',
        'Two — whatever positive number sits inside. No need to calculate it.',
        "Here there's no zero — but the two ones do something similar."])
    CF.add_expl(M, 'q-550', 'Shortcut: look at the outer operation first. $\\blacklozenge(1, 1, z)=1^{z}+1^{z}+z^{1}=2+z$, so the '
                'answer is $2+33=35$. A zero in the outer call can make the inner value irrelevant: '
                '$\\blacklozenge(w, 0, 1)=w^0+0^w+1^0=2$ for every positive $w$.')
    # Hebrew 19756-19768: 3/x = 3·x^(-1); removing a negative power flips the fraction
    CF.add_lines(M, 'solve-q-555', 'Choice by choice', 'Dividing by a fraction is multiplying by its reciprocal', [
        'Another way to see it: three over x is three times x to the minus one. A minus power means flip — the reciprocal.'])


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST
