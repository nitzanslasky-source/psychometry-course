"""Topic 7 - Equations. Course review 2026-09 (see t07_CHANGES.md)."""
import re
from math_api import T, H, A, D, Q

TOPIC = 7


def CASES(*eqs):
    return '$\\begin{cases} ' + ' \\\\ '.join(eqs) + ' \\end{cases}$'


# ---------------------------------------------------------------- helpers
def _say_replace(M, vid, n, old, new):
    """Replace the spoken line (or draw note) that contains `old` on slide n."""
    def fn(lines):
        hit = False
        for l in lines:
            for k in ('say', 'draw'):
                if k in l and old in l[k]:
                    l[k] = l[k].replace(old, new) if new is not None else l[k]
                    hit = True
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
        return lines
    M.edit_lines(vid, n, fn)


def _set_line(M, vid, n, old, new):
    """Replace the whole spoken line containing `old` with `new`."""
    def fn(lines):
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = new
                return lines
        raise AssertionError('%s #%d: not found: %s' % (vid, n, old))
    M.edit_lines(vid, n, fn)


def _insert_after(M, vid, n, old, new_lines, before=False):
    """Insert spoken lines (str) / draw notes (('D', text)) after the line containing `old` (or before it)."""
    def conv(x):
        return {'say': x} if isinstance(x, str) else {'draw': x[1]}
    def fn(lines):
        for k, l in enumerate(lines):
            t = l.get('say') or l.get('draw') or ''
            if old in t:
                j = k if before else k + 1
                return lines[:j] + [conv(x) for x in new_lines] + lines[j:]
        raise AssertionError('%s #%d: not found: %s' % (vid, n, old))
    M.edit_lines(vid, n, fn)


def _global_text_fixes(M, vid):
    """American spelling, ', so' -> '. So', division colons in draw notes."""
    v = M.video(vid)
    for n in range(1, len(v['beats']) + 1):
        def fn(lines):
            for l in lines:
                if 'say' in l:
                    s = l['say']
                    s = re.sub(r'\bmaths\b', 'math', s)
                    s = s.replace('recognise', 'recognize')
                    s = re.sub(r', so ([a-z])', lambda m: '. So ' + m.group(1), s)
                    s = s.replace('one twenty-eight', 'one hundred twenty-eight')
                    l['say'] = s
            return lines
        M.edit_lines(vid, n, fn)


def _add_q(M, qid, stem, choices, correct, expl, section):
    M.new_q(qid, TOPIC, stem, choices, correct, expl)
    M.place_q(qid, section)


def _solution(M, qid, group_title, sidebar, intro, slides, section):
    n = M.next_question_number(TOPIC)
    label = 'Question %d' % n
    idx = sidebar.index(label)
    sl = [dict(mode='title', title=label, script=intro)]
    for title, script in slides:
        sl.append(dict(mode='question', title=title, active=idx, pre=[Q(qid)], script=script))
    M.new_video('solve-' + qid, TOPIC, group_title, sidebar, sl, section, kind='solution', qid=qid)
    return n


# ---------------------------------------------------------------- 1. main lesson
def fix_lesson(M):
    vid = 'equation-strategy'
    M.set_sidebar(vid, ['Dividing by x', 'Product equals zero', 'Squares: two roots', 'One eq, two unknowns',
                        'Build the expression', 'Which operation?', 'Hidden formula', 'Break it apart',
                        'Plug in numbers', 'Try the choices', 'Recap'])
    # slide 1 - title
    M.set_slide(vid, 1, script=[
        'Now we solve equations the way the exam wants them solved.',
        'Not just "find x" — but spotting the traps and the shortcuts.',
        'Dividing by an unknown, counting solutions, and calculating what they ask for — without finding every letter.',
        'And when the algebra gets long: plugging in numbers, and trying the answer choices.',
        "Let's go."])
    # slide 2 - add the "check x = 0 separately" habit
    _insert_after(M, vid, 2, 'If the question says x isn', [
        D('Under it write "Or: check x = 0 separately"'),
        'A fast exam habit: before you divide by x, test x equals zero on its own.',
        'Here x equals zero fits the equation. That branch is real — and dividing would have lost it.'])
    # slide 5 - one equation, two unknowns + mini example
    M.set_slide(vid, 5, active=3, script=[
        'One equation, two unknowns. Can we solve it?',
        A("'One equation, two unknowns → no values…' appears", T('One equation, two unknowns $\\to$ no values…', 42)),
        "No. We can't find the value of each letter.",
        A("'…but a relationship between them' appears", T('…but a relationship between them', 42)),
        D('Underline "relationship"'),
        'But we CAN find how they relate — which one is bigger, and by how much.',
        A('The example a + 3 = b → b − a = 3 appears', T('$a+3=b \\;\\to\\; b-a=3$', 50)),
        'For example: a plus three equals b.',
        "We don't know a. We don't know b. But b minus a is always three.",
        D('Next to it write "b > a in every case"'),
        'So b is bigger than a — in every case.',
        A("'Necessarily true = true in EVERY allowed case' appears", T('Necessarily true = true in EVERY allowed case', 40)),
        'That\'s exactly what "necessarily true" questions test. It has to hold in every case — and one legal counterexample kills a choice.'])
    # slide 6 - build the expression + mini example
    M.set_slide(vid, 6, active=4, script=[
        "Sometimes they don't ask for x or y. They ask for an expression.",
        A("'Asked for an expression? Don't find each letter.' appears", T("Asked for an expression? Don't find each letter.", 40)),
        "Then don't calculate every unknown separately. Calculate the expression directly.",
        'A quick example. They ask for x plus y.',
        A('The system x + 2y = 7, 2x + y = 8 appears', T(CASES('x+2y=7', '2x+y=8'), 46)),
        D('Draw a line under the two equations and write "+" next to it'),
        'Add the equations: three x plus three y equals fifteen.',
        A('3x + 3y = 15 → x + y = 5 appears', T('$3x+3y=15 \\;\\to\\; x+y=5$', 46)),
        'Divide by three: x plus y is five. We never found x or y.',
        A("'Add, subtract — or divide — the equations' appears", T('Add, subtract — or divide — the equations', 40)),
        D('Underline "Add", "subtract" and "divide"'),
        'Adding the equations, subtracting them, sometimes dividing them — look for the short route straight to what they want.',
        "How do you know which one? Practice. You'll start to recognize the patterns.",
        'And the next slide gives you a checklist to start with.'])
    # new slide 7 - which operation?
    M.insert_slides(vid, 6, [dict(title='Which operation?', mode='concept', active=5, pre=[], script=[
        'Which operation? Check the question against this list.',
        A("'Mirror coefficients → add' appears", T('Mirror coefficients ($3x+7y$, $7x+3y$) $\\to$ add or subtract', 36)),
        'Coefficients in mirror order — three and seven, then seven and three? Add the equations. You get the same coefficient on both letters.',
        A("'A letter missing from the answers → make it cancel' appears", T('A letter missing from the answers $\\to$ make it cancel', 36)),
        'Look at the answers. Is one letter missing from all four? Your job is to make that letter disappear.',
        A("'Products or ratios → multiply or divide' appears", T('Products or ratios ($xy$, $\\frac{x}{y}$) $\\to$ multiply or divide', 36)),
        D('Next to this line write "xy = 12, yz = 6 → xy ÷ yz = 12 ÷ 6 → x/z = 2"'),
        'Products or ratios? Multiply or divide the equations. x y is twelve, y z is six. Divide them: the y cancels, and x over z is two.',
        A("'Multiply one equation so the extra letter cancels' appears", T('Target with a strange mix? Multiply one equation first', 36)),
        'Sometimes you must multiply one equation first — by five, say — so the unwanted letter cancels. Question fourteen does exactly that.',
        A("'Nothing fits → plug in numbers' appears", T('Nothing fits? Plug in numbers', 36)),
        "Nothing fits? Plug in numbers. That's coming in a moment."])])
    # slide 8 (was 7) - hidden formula: both formulas, the triangle, numbers
    M.set_slide(vid, 8, active=6, script=[
        'A rarer type — but worth knowing: a multiplication formula hiding inside the question.',
        A('(x + y)² = x² + y² + 2xy appears', T('$(x+y)^2=x^2+y^2+2xy$', 48)),
        'The square of a sum: x squared plus y squared, plus two x y.',
        A('(x − y)² = x² + y² − 2xy appears', T('$(x-y)^2=x^2+y^2-2xy$', 48)),
        'The square of a difference: the same, but minus two x y.',
        'Notice I wrote the two x y at the end — just so the x squared plus y squared sit together.',
        A("'Know 2 of the 3 pieces → get the 3rd' appears", T('Know two of: $x \\pm y$, $\\ x^2+y^2$, $\\ xy$ $\\to$ get the third', 38)),
        D('Circle x ± y, x² + y² and xy in the formulas'),
        "See x minus y, x squared plus y squared, and x times y together? That's this formula — the square of a difference.",
        'Three pieces: x plus or minus y, x squared plus y squared, and x y. Know two pieces — get the third.',
        A('Example x + y = 5, xy = 6 appears', T('$x+y=5,\\ xy=6$: $\\ 25=x^2+y^2+12 \\;\\to\\; x^2+y^2=13$', 38)),
        'Example. x plus y is five, x y is six. Square the sum: twenty-five equals x squared plus y squared, plus twelve.',
        'So x squared plus y squared is thirteen. Check with two and three: four plus nine — thirteen.',
        'Find the right formula, plug in what you know, and isolate what they ask for.',
        'One famous version — x plus one over x — gets its own slide later in this topic.'])
    # slide 9 (was 8) - break it apart + mini example
    M.set_slide(vid, 9, active=7, script=[
        'The last type: lots of equations that look scary.',
        A("'Big equation? Break it into the small ones.' appears", T('Big equation? Break it into the small ones.', 40)),
        'You could isolate and substitute letter by letter — but it takes ages.',
        A('2a = a + a and 3b = b + b + b appear', T('$2a=a+a \\qquad 3b=b+b+b$', 46)),
        'Instead, split the big expression into pieces — and swap in the small equations one at a time.',
        'Mini example. a plus b is three, b plus c is five. What is a plus two b plus c?',
        A('The system a + b = 3, b + c = 5 appears', T(CASES('a+b=3', 'b+c=5'), 44)),
        A('a + 2b + c = (a + b) + (b + c) = 8 appears', T('$a+2b+c=(a+b)+(b+c)=3+5=8$', 42)),
        D('Draw brackets under (a + b) and (b + c)'),
        'Two b is b plus b. So split it: a plus b, plus b plus c. Three plus five — eight.',
        "You'll see a bigger one in question seven."])
    # new slides 10-11 - plug in numbers, try the choices
    M.insert_slides(vid, 9, [
        dict(title='Plug in numbers', mode='concept', active=8, pre=[], script=[
            "When the answers are full of letters, there's a strong-student trick: plug in numbers.",
            A("'Letters in the answers? Plug in numbers.' appears", T('Letters in the answers? Plug in numbers.', 40)),
            'Choose simple numbers for the letters. Work out what they ask for. Then find the choice that gives the same number.',
            A("'1. The numbers must fit ALL the givens' appears", T('1. The numbers must fit ALL the givens', 36)),
            'Rule one: the numbers must fit the given equation. If two x equals three y plus one, choose y first — y is one — then x is two.',
            A("'2. Avoid 0 and 1' appears", T('2. Avoid $0$ and $1$ — they often make choices equal', 36)),
            'Rule two: avoid zero and one. If m times n is one and you take m and n equal to one, every choice equals one. Useless.',
            A("'3. Check all four choices' appears", T('3. Check all four choices — not just the first match', 36)),
            "Rule three: check all four choices. Don't stop at the first one that matches.",
            A("'4. Two choices match? Plug in again' appears", T('4. Two choices match? Plug in new numbers', 36)),
            'Two choices give the right number? Plug in a second set of numbers. Only one choice survives both.',
            'You will see this in questions fourteen, sixteen, seventeen and eighteen.']),
        dict(title='Try the choices', mode='concept', active=9, pre=[], script=[
            'The mirror trick: the answers are numbers. Put each choice into the question and see which one works.',
            A("'Numbers in the answers? Try them in the question.' appears", T('Numbers in the answers? Try them in the question.', 40)),
            A('The example (x − 6)² = 16, try x = 10 appears', T('$(x-6)^2=16$: $\\ x=10 \\to 4^2=16$ ✓', 44)),
            'For example: x minus six, squared, is sixteen. Is x ten? Ten minus six is four. Four squared: sixteen. Yes.',
            A("'Start from a middle-sized choice' appears", T('Start from a middle-sized choice: too big or too small?', 36)),
            "Start with a middle-sized choice. If it's too big or too small, you know which way to go.",
            A("'A choice that works is A solution — maybe not the only one' appears", T('A choice that works is A solution — maybe not the only one', 36)),
            "Careful: it tells you a choice works — not that it's the only solution. For how many solutions, you still need the algebra.",
            'In question fifteen we do this with a sum and a difference.'])])
    # slide 12 - recap
    M.set_slide(vid, 12, active=10, script=[
        "Let's lock it in.",
        A("'Dividing by an unknown? Only if it can't be 0' appears", T("Dividing by an unknown? Only if it can't be $0$", 36)),
        A("'Power 2 and up: common factor → product = 0' appears", T('Power $2$ and up: common factor $\\to$ product $=0$', 36)),
        A("'Taking a root: plus AND minus' appears", T('Taking a root: plus AND minus', 36)),
        A("'Asked for an expression? Build it directly' appears", T('Asked for an expression? Build it directly — use the checklist', 36)),
        A("'Letters in the answers → plug in; numbers → try the choices' appears", T('Letters in the answers $\\to$ plug in; numbers $\\to$ try them', 36)),
        D('Tick each line'),
        'Every one of these shows up in the questions that follow. Try each one first.'])


# ---------------------------------------------------------------- 1b. existing solution videos
def fix_solution_videos(M):
    # Q16 - "Brainwave two" was false for negative numbers
    _set_line(M, 'solve-q-179', 4, 'Brainwave two',
              'Brainwave two: all three ratios are bigger than one. Multiply numbers bigger than one, and the result is bigger than one. So x over w is bigger than one.')
    # formula names instead of numbers
    _set_line(M, 'solve-q-187', 2, 'First short multiplication formula',
              'The square of a sum: a plus b, squared, is a squared plus two a b plus b squared.')
    _set_line(M, 'solve-q-178', 2, 'third short multiplication formula',
              'That second one is the difference of squares: a squared minus b squared equals a minus b, times a plus b.')
    _set_line(M, 'solve-q-178', 1, 'short multiplication formula', 'A word problem hiding a multiplication formula.')
    _set_line(M, 'solve-q-182', 2, 'with the first formula', 'Expand the left side with the square of a sum.')
    _set_line(M, 'solve-q-182', 3, 'short multiplication formula',
              'Shortcut: the right side IS the square of a difference.')
    _set_line(M, 'solve-q-181', 2, 'short multiplication formula',
              'Careful on the right. Many students write nine y squared plus one — wrong. The WHOLE three y plus one gets squared — the square of a sum.')
    # Q10 - reassure weak students
    _insert_after(M, 'solve-q-186', 3, 'Two tools that make this instant.', [
        'Method one is all you need for the exam. This is a bonus for fast students.'], before=True)
    # Q14 - plug-in with ones: say why it is safe here
    _insert_after(M, 'solve-q-190', 3, 'Choice one: three minus forty-five', [
        'We used ones — usually risky. Here the four choices still came out different, so it works.'])
    # Q20 - why "cannot be determined" is wrong; not the last question any more
    _set_line(M, 'solve-q-183', 1, 'Last question on equations.', 'Last question in this set.')
    _insert_after(M, 'solve-q-183', 2, 'So a is zero. Choice three.', [
        "Why not choice four? It cannot be determined means different cases give different values of a.",
        'Here every case gives the same value: a equals zero. So it IS determined.'])
    # draw notes: division, not ":"
    _say_replace(M, 'solve-q-184', 3, '22 : 11/15', '22 ÷ 11/15')
    _say_replace(M, 'solve-q-180', 2, 'm : 1/m', 'm ÷ (1/m)')
    _say_replace(M, 'solve-q-180', 3, '2 : 1/2', '2 ÷ 1/2')
    for vid in ['equation-strategy'] + ['solve-q-%d' % k for k in range(178, 198)]:
        _global_text_fixes(M, vid)


# ---------------------------------------------------------------- 2. text of every existing question
def fix_questions(M):
    S = M.set_q
    NOTDET = 'It cannot be determined from the information given.'
    # --- guided: theory
    S('q-191', stem='Given: $x^7 = x^6 y$. $y = ?$', choices=['$x$', '$x^6$', '$0$', NOTDET], correct=4, expl=[
        'If $x \\ne 0$, divide both sides by $x^6$: $y = x$.',
        'But if $x = 0$, the equation reads $0 = 0$, which is true for every $y$.',
        'Different cases give different values of $y$. Therefore $y$ cannot be determined.'])
    S('q-192', stem='Given: $x^4 - 16x^2 = 0$. The number of solutions of the given equation is —',
      choices=['$4$', '$3$', '$2$', '$1$'], correct=2, expl=[
        'Take out the common factor: $x^2(x^2 - 16) = 0$.',
        'A product is $0$ when one factor is $0$: $x^2 = 0$ gives $x = 0$, and $x^2 = 16$ gives $x = 4$ or $x = -4$.',
        'Three different solutions: $0$, $4$ and $-4$.'])
    S('q-193', stem='Given: $(x - 6)^2 = 49$. How many different values can $x$ take?',
      choices=['$1$', '$2$', '$3$', '$0$'], correct=2, expl=[
        'Something squared is $49$. Therefore $x - 6 = 7$ or $x - 6 = -7$.',
        'Therefore $x = 13$ or $x = -1$: two different values.'])
    S('q-194', stem='Given: $\\frac{a - 5b}{4} = 1 - b$. Which of the following statements is necessarily true?',
      choices=['$a < b$', '$b < a$', '$a = b$', '$a = 4b$'], correct=2, expl=[
        'Multiply both sides by $4$: $a - 5b = 4 - 4b$.',
        'Add $5b$ to both sides: $a = b + 4$.',
        'Therefore $a$ is always $4$ more than $b$, and $b < a$ in every case.'])
    S('q-195', stem='Given:\n' + CASES('3x + 7y = 23', '7x + 3y = 27') + '\n$x + y = ?$',
      choices=['$5$', '$7$', '$12$', '$10$'], correct=1, expl=[
        'Add the two equations: $10x + 10y = 50$.',
        'Divide by $10$: $x + y = 5$.'])
    S('q-196', stem='Given:\n' + CASES('x - y = 5', 'x^2 + y^2 = 73') + '\n$xy = ?$',
      choices=['$24$', '$30$', '$48$', '$15$'], correct=1, expl=[
        'Use the square of a difference: $(x - y)^2 = x^2 + y^2 - 2xy$.',
        'Substitute: $5^2 = 73 - 2xy$, that is, $25 = 73 - 2xy$.',
        'Therefore $2xy = 48$ and $xy = 24$. (Check: $8$ and $3$.)'])
    S('q-197', stem='Given:\n' + CASES('2a + 3b + 3c = 23', 'a + b = 3', '2b + c = 4', 'a + c = 10') + '\n$c = ?$',
      choices=['$6$', '$8$', '$5$', '$4$'], correct=1, expl=[
        'Split the big left side into the small ones: $2a + 3b + 3c = (a + b) + (2b + c) + (a + c) + c$.',
        'Substitute the values: $3 + 4 + 10 + c = 23$.',
        'Therefore $17 + c = 23$ and $c = 6$.'])
    # --- guided: advanced A
    S('q-184', stem='Given: $22 - \\frac{2}{5}x = \\frac{1}{3}x$. $x = ?$',
      choices=['$15$', '$45$', '$22$', '$30$'], correct=4, expl=[
        'Multiply every term by $15$: $22 \\cdot 15 - 6x = 5x$.',
        'Therefore $11x = 22 \\cdot 15$, and $x = \\frac{22 \\cdot 15}{11} = 2 \\cdot 15 = 30$.',
        'Estimation check: $\\frac{1}{3}x + \\frac{2}{5}x = \\frac{11}{15}x = 22$. A part of $x$ equals $22$. Therefore $x$ is a bit more than $22$, and only $30$ fits.'])
    S('q-185', stem='Given: $x \\ne 0$ and $\\pi x^2 + x^3 = 2x^2$. $x = ?$',
      choices=['$\\pi$', '$\\pi^2$', '$2 + \\pi$', '$2 - \\pi$'], correct=4, expl=[
        'Every term contains $x^2$, and $x \\ne 0$. Divide every term by $x^2$: $\\pi + x = 2$.',
        'Therefore $x = 2 - \\pi$.'])
    S('q-186', stem='Given: $a \\ne 0$, $b \\ne 0$, $c \\ne 0$, $d \\ne 0$ and $\\frac{a}{b} = \\frac{c}{d}$. Which of the following statements is not necessarily true?',
      choices=['$a = \\frac{bc}{d}$', '$d = \\frac{bc}{a}$', '$\\frac{d}{b} = \\frac{c}{a}$', '$\\frac{c}{b} = \\frac{d}{a}$'], correct=4, expl=[
        'Cross-multiply the given equation: $ad = bc$.',
        'Choices 1, 2 and 3 each cross-multiply back to $ad = bc$. They are always true.',
        'Choice 4 cross-multiplies to $ac = bd$, which is a different equation.',
        'Counterexample: $a = 1$, $b = 2$, $c = 3$, $d = 6$. Then $\\frac{a}{b} = \\frac{c}{d} = \\frac{1}{2}$, but $\\frac{c}{b} = \\frac{3}{2}$ and $\\frac{d}{a} = 6$.'])
    S('q-187', expl=[
        'Call the numbers $a$ and $b$: $a^2 + b^2 = (a + b)^2 = a^2 + 2ab + b^2$.',
        'Subtract $a^2 + b^2$ from both sides: $0 = 2ab$, therefore $ab = 0$.',
        'A product is $0$ only when a factor is $0$: $a = 0$ or $b = 0$.'])
    S('q-188', stem='Given:\n' + CASES('2x + 3y + z = 15', '3x - 3y + 2z = 16', '4x + 3z = 26') + '\n$x = ?$',
      choices=['$4$', '$5$', '$6$', '$7$'], correct=2, expl=[
        'Add the first two equations. The $y$ terms cancel: $5x + 3z = 31$.',
        'Subtract the third equation: $(5x + 3z) - (4x + 3z) = 31 - 26$.',
        'Therefore $x = 5$.'])
    S('q-189', stem='Given:\n' + CASES('1\\frac{1}{4}x + 2\\frac{1}{3}y = 2a', '2\\frac{3}{4}x + 1\\frac{2}{3}y = 2b') + '\n$x + y = ?$',
      choices=['$\\frac{2}{a + b}$', '$\\frac{a + b}{2}$', '$\\frac{a + b}{4}$', '$\\frac{4}{a + b}$'], correct=2, expl=[
        'Add the equations. The $x$ coefficients: $1\\frac{1}{4} + 2\\frac{3}{4} = 4$. The $y$ coefficients: $2\\frac{1}{3} + 1\\frac{2}{3} = 4$.',
        'Therefore $4x + 4y = 2a + 2b$, that is, $4(x + y) = 2(a + b)$.',
        'Divide by $4$: $x + y = \\frac{a + b}{2}$.'])
    S('q-190', stem='Given:\n' + CASES('a + b + c = x', 'a + 3b + 5c = z') + '\n$4a + 2b = ?$',
      choices=['$x - 5z$', '$2x - 4z$', '$5x - z$', '$3x - 2z$'], correct=3, expl=[
        'The answers have no $c$. Make $c$ cancel: multiply the first equation by $5$: $5a + 5b + 5c = 5x$.',
        'Subtract the second equation: $(5a + 5b + 5c) - (a + 3b + 5c) = 5x - z$.',
        'Therefore $4a + 2b = 5x - z$.',
        'Plug-in check: $a = b = c = 1$ gives $x = 3$, $z = 9$ and $4a + 2b = 6$. Only choice 3 gives $5 \\cdot 3 - 9 = 6$.'])
    # --- guided: advanced B
    S('q-178', expl=[
        'Call the numbers $a$ and $b$: $a - b = 4$ and $a^2 - b^2 = 72$.',
        'Difference of squares: $a^2 - b^2 = (a - b)(a + b)$. Therefore $4(a + b) = 72$.',
        'Divide by $4$: $a + b = 18$. (Check: $11$ and $7$ give $121 - 49 = 72$.)'])
    S('q-179', stem='Given: $x, y, z, w \\ne 0$ and\n' + CASES('\\frac{x}{y} = 2', '\\frac{y}{z} = 6', '\\frac{z}{w} = 3') + '\n$\\frac{x}{w} = ?$',
      choices=['$\\frac{1}{36}$', '$\\frac{3}{11}$', '$36$', '$11$'], correct=3, expl=[
        'Multiply the three equations: $\\frac{x}{y} \\cdot \\frac{y}{z} \\cdot \\frac{z}{w} = 2 \\cdot 6 \\cdot 3$.',
        'The $y$ and the $z$ cancel: $\\frac{x}{w} = 36$.'])
    S('q-180', stem='Given: $m \\ne 0$, $n \\ne 0$ and $mn = 1$. $\\frac{m}{n} = ?$',
      choices=['$\\frac{1}{m^2}$', '$\\frac{1}{m}$', '$m$', '$m^2$'], correct=4, expl=[
        'From $mn = 1$: $n = \\frac{1}{m}$.',
        'Therefore $\\frac{m}{n} = m \\div \\frac{1}{m} = m \\cdot m = m^2$.',
        'Plug-in check: $m = 2$, $n = \\frac{1}{2}$. Then $\\frac{m}{n} = 4 = m^2$.'])
    S('q-181', stem='Given: $2x = 3y + 1$. $2x^2 - 4\\frac{1}{2}y^2 = ?$',
      choices=['$1$', '$0.5 + 3y$', '$2x + 3y$', '$3x$'], correct=2, expl=[
        'Square both sides: $(2x)^2 = (3y + 1)^2$, that is, $4x^2 = 9y^2 + 6y + 1$.',
        'Move $9y^2$ to the left: $4x^2 - 9y^2 = 6y + 1$.',
        'Divide by $2$: $2x^2 - 4\\frac{1}{2}y^2 = 3y + 0.5$.',
        'Plug-in check: $y = 1$, $x = 2$. The expression is $8 - 4.5 = 3.5$, and choice 2 gives $0.5 + 3 = 3.5$.'])
    S('q-182', stem='Given: for every $x$ and $y$, $(ax + by)^2 = 4x^2 + 9y^2 - 12xy$. $|a - b| = ?$',
      choices=['$1$', '$5$', '$6$', '$0$'], correct=2, expl=[
        'Expand the left side: $a^2x^2 + 2abxy + b^2y^2$.',
        'The two sides are equal for every $x$ and $y$. Therefore the coefficients match: $a^2 = 4$, $b^2 = 9$ and $2ab = -12$.',
        'Therefore $a = \\pm 2$, $b = \\pm 3$ and $ab = -6$ (opposite signs): $(a, b) = (2, -3)$ or $(-2, 3)$.',
        'In both cases $|a - b| = 5$.'])
    S('q-183', stem='Given: $a^2 + b^2 = \\frac{1}{3}b^2$. $a = ?$',
      choices=['$1$', '$3$', '$0$', NOTDET], correct=3, expl=[
        'Multiply by $3$: $3a^2 + 3b^2 = b^2$, therefore $3a^2 + 2b^2 = 0$.',
        'A square is never negative: $3a^2 \\ge 0$ and $2b^2 \\ge 0$. Their sum is $0$ only if both are $0$.',
        'Therefore $a = 0$ (and $b = 0$).',
        'Why not "cannot be determined"? Every case that fits the equation gives the same value, $a = 0$.'])
    # --- practice: unit-t7-5
    S('q-198', stem='Given:\n' + CASES('x + y = 5', 'x^2 + y^2 = 25') + '\n$xy = ?$',
      choices=['$5$', '$10$', '$0$', '$12.5$'], correct=3, expl=[
        'Square the sum: $(x + y)^2 = x^2 + y^2 + 2xy$.',
        'Substitute: $25 = 25 + 2xy$. Therefore $2xy = 0$ and $xy = 0$.'])
    S('q-199', stem='Given: $x \\ne 0$ and $\\frac{x}{x + y} = 5x$. $x + y = ?$',
      choices=['$\\frac{1}{10}$', '$\\frac{1}{5}$', '$\\frac{1}{2}$', '$1$'], correct=2, expl=[
        'Divide both sides by $x$ (allowed, since $x \\ne 0$): $\\frac{1}{x + y} = 5$.',
        'Therefore $x + y = \\frac{1}{5}$.'])
    S('q-200', stem='Given:\n' + CASES('x + y + z = 10', 'y + z = 13', 'y + z + w = -4') + '\n$x + y + z + w = ?$',
      choices=['$-3$', '$19$', '$-7$', '$7$'], correct=3, expl=[
        'Subtract the second equation from the third: $w = -4 - 13 = -17$.',
        'Therefore $x + y + z + w = (x + y + z) + w = 10 + (-17) = -7$.'])
    S('q-201', stem='Given: $x \\ne 0$, $y \\ne -3$ and $\\frac{x}{y + 3} = \\frac{9}{x}$. $y = ?$',
      choices=['$\\frac{x^2}{9} - \\frac{1}{3}$', '$\\frac{x^2}{9} - 3$', '$3$', '$\\frac{x^2}{3}$'], correct=2, expl=[
        'Cross-multiply: $x^2 = 9(y + 3) = 9y + 27$.',
        'Therefore $9y = x^2 - 27$ and $y = \\frac{x^2}{9} - 3$.'])
    S('q-202', stem='Given: $p^2 + q^2 = (p + q)^2$ and $q \\ne 0$. Which of the following is necessarily true?',
      choices=['$q = 3p$', '$p = 0$', '$p = q - 2$', '$q = 5$'], correct=2, expl=[
        'Expand: $(p + q)^2 = p^2 + 2pq + q^2$.',
        'Cancel $p^2 + q^2$ on both sides: $0 = 2pq$, therefore $pq = 0$.',
        'Since $q \\ne 0$, $p = 0$.'])
    S('q-203', stem='Given: $m > 0$, $n > 0$ and $\\frac{(m - n)^2 + (m + n)^2}{2} = 2n^2$. $m = ?$',
      choices=['$n$', '$2n$', '$\\frac{n^2}{2}$', '$m^2 - 2$'], correct=1, expl=[
        'Expand: $(m - n)^2 + (m + n)^2 = 2m^2 + 2n^2$ (the $2mn$ terms cancel).',
        'Half of it: $m^2 + n^2 = 2n^2$, therefore $m^2 = n^2$.',
        'Then $m = n$ or $m = -n$. Both numbers are positive. Therefore $m = n$.'])
    S('q-204', stem='Given: $x > 0$, $a > 0$ and $\\frac{16a}{x + 3} = \\frac{a}{x}$. $x = ?$',
      choices=['$3a$', '$5$', '$\\frac{1}{5}$', '$\\frac{1}{3a}$'], correct=3, expl=[
        'Cross-multiply: $16ax = a(x + 3)$.',
        'Divide by $a$ (allowed, since $a > 0$): $16x = x + 3$.',
        'Therefore $15x = 3$ and $x = \\frac{1}{5}$.'])
    S('q-205', stem='Given: $c$ and $d$ are numbers. The equation $cx + d = 0$ (the unknown is $x$) has no solution. Which of the following is necessarily true?',
      choices=['$c = 0$ and $d \\ne 0$', '$c \\ne 0$ and $d = 0$', '$c = 1$ and $d \\ne 0$', '$c = 1$ and $d = 0$'], correct=1, expl=[
        'If $c \\ne 0$, then $x = -\\frac{d}{c}$ is a solution. Therefore $c = 0$.',
        'With $c = 0$ the equation reads $d = 0$. For no solution, this must be false: $d \\ne 0$.'])
    S('q-206', stem='Given: $y \\ne 0$ and\n' + CASES('k = x - \\frac{y}{2}', 'x + y = 2k') + '\n$\\frac{x}{y} = ?$',
      choices=['$1$', '$2$', '$3$', '$\\frac{1}{2}$'], correct=2, expl=[
        'Multiply the first equation by $2$: $2k = 2x - y$.',
        'The second equation says $2k = x + y$. Therefore $2x - y = x + y$, and $x = 2y$.',
        'Therefore $\\frac{x}{y} = 2$.'])
    S('q-207', stem='Given: for every $x$ and $y$, $(ax + y)(x + by) = x^2 - y^2$. $a - b = ?$',
      choices=['$0$', '$-1$', '$2$', '$1$'], correct=3, expl=[
        'Expand: $(ax + y)(x + by) = ax^2 + (ab + 1)xy + by^2$.',
        'Match the coefficients with $x^2 - y^2$: $a = 1$ and $b = -1$. Check the $xy$ term: $ab + 1 = -1 + 1 = 0$ ✓.',
        'Therefore $a - b = 1 - (-1) = 2$.'])
    S('q-208', stem='Given:\n' + CASES('a = 3b = 4c = 5d', 'a + b = c + d') + '\n$d = ?$',
      choices=['$1$', '$0$', '$\\frac{4}{5}$', '$\\frac{1}{20}$'], correct=2, expl=[
        'Call the common value $k$: $a = k$, $b = \\frac{k}{3}$, $c = \\frac{k}{4}$, $d = \\frac{k}{5}$.',
        'Then $a + b = c + d$ reads $k + \\frac{k}{3} = \\frac{k}{4} + \\frac{k}{5}$, that is, $\\frac{4}{3}k = \\frac{9}{20}k$.',
        'Multiply by $60$: $80k = 27k$. Therefore $53k = 0$ and $k = 0$.',
        'Therefore $d = \\frac{k}{5} = 0$.'])
    S('q-209', stem='Given:\n' + CASES('x^2 - y^2 = 0', 'x - y = 3') + '\n$x = ?$',
      choices=['$-\\frac{3}{4}$', '$\\frac{3}{2}$', '$3$', '$-3$'], correct=2, expl=[
        'Factor: $x^2 - y^2 = (x - y)(x + y) = 0$.',
        'Since $x - y = 3 \\ne 0$, the other factor is $0$: $x + y = 0$.',
        'Add $x - y = 3$ and $x + y = 0$: $2x = 3$. Therefore $x = \\frac{3}{2}$.'])
    S('q-210', stem='Given: $x \\ne 0$ and $x^3 + x^4 = bx^3$. $x = ?$',
      choices=['$b$', '$\\sqrt{b}$', '$b - 1$', '$b^2$'], correct=3, expl=[
        'Divide every term by $x^3$ (allowed, since $x \\ne 0$): $1 + x = b$.',
        'Therefore $x = b - 1$.'])
    S('q-211', stem='Given: $x > 0$ and $x^3 = 5x$. $x = ?$',
      choices=['$\\sqrt[3]{5}$', '$\\sqrt{5}$', '$5$', '$1$'], correct=2, expl=[
        'Divide by $x$ (allowed, since $x > 0$): $x^2 = 5$.',
        'Therefore $x = \\sqrt{5}$ or $x = -\\sqrt{5}$. Since $x > 0$, $x = \\sqrt{5}$.'])
    S('q-212', stem='Given:\n' + CASES('4x + 3y = a', '3x + 4y = c') + '\n$x + y = ?$',
      choices=['$\\frac{a + c}{7}$', '$\\frac{a + c}{12}$', '$\\frac{4}{a} + \\frac{3}{c}$', '$\\frac{7}{a} + \\frac{7}{c}$'], correct=1, expl=[
        'Add the equations: $7x + 7y = a + c$.',
        'Divide by $7$: $x + y = \\frac{a + c}{7}$.'])
    S('q-213', stem='Given:\n' + CASES('p + q = r', 'p + r = q') + '\nHow many different values can $p$ take?',
      choices=['$1$', '$2$', '$3$', '$p$ cannot take any value.'], correct=1, expl=[
        'Add the two equations: $2p + q + r = q + r$. Therefore $2p = 0$ and $p = 0$.',
        'For example, $q = r = 5$ fits both equations with $p = 0$. Therefore $p$ takes exactly one value: $0$.'])
    S('q-214', stem='Given: $4x + 3y = 10$. Which of the following is necessarily true?',
      choices=['$x > 1$ or $y > 1$ (or both)', '$x < 0$ or $y < 0$ (or both)', '$x < y$', '$x < 10$'], correct=1, expl=[
        'Suppose choice 1 is false: $x \\le 1$ and $y \\le 1$.',
        'Then $4x + 3y \\le 4 + 3 = 7 < 10$. This contradicts $4x + 3y = 10$. Therefore choice 1 is always true.',
        'The others can fail: $x = y = \\frac{10}{7}$ breaks choices 2 and 3, and $x = 100$, $y = -130$ breaks choice 4.'])
    S('q-215', stem='Given: $(a + 3)(a - 3) - (b + 3)(b - 3) = a^2 - b^2$. Which of the following pairs of numbers cannot be the pair $(a, b)$?',
      choices=['$(-2, 2)$', '$(1, 4)$', '$(5, 0)$', 'Any pair of numbers can be $(a, b)$.'], correct=4, expl=[
        '$(a + 3)(a - 3) = a^2 - 9$ and $(b + 3)(b - 3) = b^2 - 9$.',
        'The left side is $(a^2 - 9) - (b^2 - 9) = a^2 - b^2$, exactly the right side.',
        'The equation is true for every $a$ and $b$. No pair is excluded.'])
    S('q-216', stem='Given: the ratio $P : Q$ equals the ratio $Q : R$. The ratio $P : R$ equals —',
      choices=['$1 : 1$', '$R : P$', '$Q : R^2$', '$Q^2 : R^2$'], correct=4, expl=[
        'Write the ratios as fractions: $\\frac{P}{Q} = \\frac{Q}{R}$.',
        'Cross-multiply: $PR = Q^2$. Therefore $P = \\frac{Q^2}{R}$.',
        'Then $\\frac{P}{R} = \\frac{Q^2}{R^2}$, that is, the ratio $P : R$ equals the ratio $Q^2 : R^2$.'])
    S('q-217', stem='Given: $m \\ne 0$, $m \\ne 1$, $c \\ne 0$, $c \\ne 1$ and\n' + CASES('x = \\frac{1}{c} - \\frac{m}{c}', 'y = x + 1 - m') + '\n$\\frac{y}{x} = ?$',
      choices=['$\\frac{1 + c}{m}$', '$\\frac{1 - c}{m}$', '$1 - c$', '$1 + c$'], correct=4, expl=[
        'Write $x$ as one fraction: $x = \\frac{1 - m}{c}$. Therefore $1 - m = xc$.',
        'Substitute into $y$: $y = x + xc = x(1 + c)$.',
        'Since $m \\ne 1$, $x \\ne 0$. Divide: $\\frac{y}{x} = 1 + c$.'])
    S('alg-extra-unit-t7-5-1', stem='Given: $6x + 8 = 68$. $x = ?$', choices=['$11$', '$10$', '$8$', '$9$'], correct=2, expl=[
        'Subtract $8$ from both sides: $6x = 60$.', 'Divide by $6$: $x = 10$.'])
    S('alg-extra-unit-t7-5-2', stem='Given:\n' + CASES('x + y = 15', 'x - y = 3') + '\n$x = ?$',
      choices=['$6$', '$7$', '$8$', '$9$'], correct=4, expl=[
        'Add the equations. The $y$ terms cancel: $2x = 18$.', 'Therefore $x = 9$.'])
    S('alg-extra-unit-t7-5-3', stem='Given:\n' + CASES('2x + 3y = 36', '3x + 2y = 34') + '\n$x + y = ?$',
      choices=['$13$', '$15$', '$16$', '$14$'], correct=4, expl=[
        'Add the equations: $5x + 5y = 70$.', 'Divide by $5$: $x + y = 14$.'])
    S('alg-extra-unit-t7-5-4', stem='Given:\n' + CASES('x + y = 14', 'xy = 48') + '\n$x^2 + y^2 = ?$',
      choices=['$102$', '$98$', '$100$', '$196$'], correct=3, expl=[
        'Square the sum: $(x + y)^2 = x^2 + y^2 + 2xy$.',
        'Substitute: $196 = x^2 + y^2 + 96$.',
        'Therefore $x^2 + y^2 = 100$. (Check: $6$ and $8$ give $36 + 64 = 100$.)'])
    S('alg-extra-unit-t7-5-5', stem='Given: $\\frac{x - 6}{x + 8} = \\frac{1}{2}$. $x = ?$',
      choices=['$21$', '$19$', '$20$', '$14$'], correct=3, expl=[
        'The denominator cannot be $0$: $x \\ne -8$.',
        'Cross-multiply: $2(x - 6) = x + 8$, that is, $2x - 12 = x + 8$.',
        'Therefore $x = 20$. Check: $\\frac{14}{28} = \\frac{1}{2}$ ✓.'])
    S('alg-extra-unit-t7-5-6', stem='Given: $x(x - 6) = 0$. What is the sum of all the solutions of the equation?',
      choices=['$-6$', '$12$', '$6$', '$0$'], correct=3, expl=[
        'A product is $0$ when one factor is $0$: $x = 0$ or $x - 6 = 0$.',
        'The solutions are $0$ and $6$. Their sum is $6$.'])
    S('alg-extra-unit-t7-5-7', stem='For which value of $k$ does the equation $(6 - k)x = 8$ have no solution?',
      choices=['$5$', '$7$', '$0$', '$6$'], correct=4, expl=[
        'If $6 - k \\ne 0$, then $x = \\frac{8}{6 - k}$ is a solution.',
        'If $k = 6$, the equation reads $0 \\cdot x = 8$, that is, $0 = 8$. This is never true: no solution.'])
    # --- unit-t7-1: additional source-bank variants
    S('q-172', stem='Given: $x^5 = x^4 y$. $y = ?$', choices=['$x$', '$x^4$', '$0$', NOTDET], correct=4, expl=[
        'If $x \\ne 0$, divide both sides by $x^4$: $y = x$.',
        'But if $x = 0$, the equation reads $0 = 0$, which is true for every $y$.',
        'Different cases give different values of $y$. Therefore $y$ cannot be determined.'])
    S('q-173', stem='Given: $x^4 - 9x^2 = 0$. The number of solutions of the given equation is —',
      choices=['$4$', '$3$', '$2$', '$1$'], correct=2, expl=[
        'Take out the common factor: $x^2(x^2 - 9) = 0$.',
        '$x^2 = 0$ gives $x = 0$, and $x^2 = 9$ gives $x = 3$ or $x = -3$.',
        'Three different solutions: $0$, $3$ and $-3$.'])
    S('q-174', stem='Given: $(x - 5)^2 = 36$. How many different values can $x$ take?',
      choices=['$1$', '$2$', '$3$', '$0$'], correct=2, expl=[
        'Something squared is $36$. Therefore $x - 5 = 6$ or $x - 5 = -6$.',
        'Therefore $x = 11$ or $x = -1$: two different values.'])
    S('q-175', stem='Given: $\\frac{a - 4b}{3} = 2 - b$. Which of the following statements is necessarily true?',
      choices=['$a < b$', '$b < a$', '$a = b$', '$a = 3b$'], correct=2, expl=[
        'Multiply both sides by $3$: $a - 4b = 6 - 3b$.',
        'Add $4b$ to both sides: $a = b + 6$.',
        'Therefore $a$ is always $6$ more than $b$, and $b < a$ in every case.'])
    S('q-176', stem='Given:\n' + CASES('3x + 5y = 19', '5x + 3y = 21') + '\n$x + y = ?$',
      choices=['$5$', '$8$', '$12$', '$10$'], correct=1, expl=[
        'Add the equations: $8x + 8y = 40$.', 'Divide by $8$: $x + y = 5$.'])
    S('q-177', stem='Given:\n' + CASES('x - y = 3', 'x^2 + y^2 = 89') + '\n$xy = ?$',
      choices=['$40$', '$30$', '$24$', '$15$'], correct=1, expl=[
        'Use the square of a difference: $(x - y)^2 = x^2 + y^2 - 2xy$.',
        'Substitute: $9 = 89 - 2xy$. Therefore $2xy = 80$ and $xy = 40$.'])
    # pass 2: the original variants alg-extra-unit-t7-1-1 ... -7 are restored (text clean-up only)
    S('alg-extra-unit-t7-1-1', stem='Given: $7x + 9 = 86$. $x = ?$', choices=['$11$', '$9$', '$10$', '$12$'], correct=1, expl=[
        'Subtract $9$ from both sides: $7x = 77$.', 'Divide by $7$: $x = 11$.'])
    S('alg-extra-unit-t7-1-2', stem='Given:\n' + CASES('x + y = 17', 'x - y = 3') + '\n$x = ?$',
      choices=['$9$', '$10$', '$7$', '$8$'], correct=2, expl=[
        'Add the equations. The $y$ terms cancel: $2x = 20$.', 'Therefore $x = 10$.'])
    S('alg-extra-unit-t7-1-3', stem='Given:\n' + CASES('2x + 3y = 41', '3x + 2y = 39') + '\n$x + y = ?$',
      choices=['$17$', '$18$', '$16$', '$15$'], correct=3, expl=[
        'Add the equations: $5x + 5y = 80$.', 'Divide by $5$: $x + y = 16$.'])
    S('alg-extra-unit-t7-1-4', stem='Given:\n' + CASES('x + y = 16', 'xy = 63') + '\n$x^2 + y^2 = ?$',
      choices=['$130$', '$256$', '$132$', '$128$'], correct=1, expl=[
        'Square the sum: $(x + y)^2 = x^2 + y^2 + 2xy$.',
        'Substitute: $256 = x^2 + y^2 + 126$.',
        'Therefore $x^2 + y^2 = 130$. (Check: $7$ and $9$ give $49 + 81 = 130$.)'])
    S('alg-extra-unit-t7-1-5', stem='Given: $\\frac{x - 7}{x + 9} = \\frac{1}{2}$. $x = ?$',
      choices=['$23$', '$16$', '$24$', '$22$'], correct=1, expl=[
        'The denominator cannot be $0$: $x \\ne -9$.',
        'Cross-multiply: $2(x - 7) = x + 9$, that is, $2x - 14 = x + 9$.',
        'Therefore $x = 23$. Check: $\\frac{16}{32} = \\frac{1}{2}$ ✓.'])
    S('alg-extra-unit-t7-1-6', stem='Given: $x(x - 7) = 0$. What is the sum of all the solutions of the equation?',
      choices=['$7$', '$0$', '$-7$', '$14$'], correct=1, expl=[
        'A product is $0$ when one factor is $0$: $x = 0$ or $x - 7 = 0$.',
        'The solutions are $0$ and $7$. Their sum is $7$.'])
    S('alg-extra-unit-t7-1-7', stem='For which value of $k$ does the equation $(7 - k)x = 9$ have no solution?',
      choices=['$8$', '$0$', '$7$', '$6$'], correct=3, expl=[
        'If $7 - k \\ne 0$, then $x = \\frac{9}{7 - k}$ is a solution.',
        'If $k = 7$, the equation reads $0 \\cdot x = 9$, that is, $0 = 9$. This is never true: no solution.'])


# ---------------------------------------------------------------- 3. new lesson: more equation tools + guided Q21-22
def more_tools(M):
    sec = 'equation-b'
    title = 'More Equation Tools'
    M.new_video('r26-t07-more-tools', TOPIC, title, ['Multiply or divide', 'x + 1/x', 'Recap'], [
        dict(mode='title', title=title, script=[
            'Two more tools for equation questions.',
            'Multiplying or dividing equations, and the famous x plus one over x.']),
        dict(mode='concept', title='Multiply or divide', active=0, script=[
            'We add and subtract equations all the time. We can also multiply or divide them.',
            A("'Products or ratios? Multiply or divide the equations.' appears", T('Products or ratios? Multiply or divide the equations.', 40)),
            'When? When the equations are products or ratios.',
            A('The system xy = 12, yz = 6 appears', T(CASES('xy=12', 'yz=6'), 46)),
            'x y is twelve, y z is six. They ask for x over z.',
            A('xy/yz = 12/6 → x/z = 2 appears', T('$\\frac{xy}{yz}=\\frac{12}{6} \\;\\to\\; \\frac{x}{z}=2$', 48)),
            'Divide the first by the second. Left side by left side, right side by right side. The y cancels.',
            'x over z is twelve over six — two. We never found x, y or z.',
            A("'x/y · y/z = x/z' appears", T('$\\frac{x}{y}\\cdot\\frac{y}{z}=\\frac{x}{z}$: multiplying cancels too', 40)),
            'Ratios work with multiplying: x over y, times y over z, is x over z. The middle letter cancels.',
            "That's how we solved question sixteen."]),
        dict(mode='concept', title='x + 1/x', active=1, script=[
            'A favorite on the exam: x plus one over x.',
            "It's the square of a sum — with a gift inside.",
            A('(x + 1/x)² = x² + 2 + 1/x² appears', T('$\\left(x+\\frac{1}{x}\\right)^2=x^2+2+\\frac{1}{x^2}$', 50)),
            'Square it: x squared, plus two times x times one over x, plus one over x squared.',
            A("'x · 1/x = 1: the middle term is just 2' appears", T('$x\\cdot\\frac{1}{x}=1$: the middle term is just $2$', 40)),
            'x times one over x is one. So the middle term is just two. No letters.',
            A('Example x + 1/x = 3 appears', T('$x+\\frac{1}{x}=3 \\;\\to\\; 9=x^2+\\frac{1}{x^2}+2 \\;\\to\\; x^2+\\frac{1}{x^2}=7$', 36)),
            'Example: x plus one over x is three. Square both sides: nine. Take away two: x squared plus one over x squared is seven.',
            'With a minus — x minus one over x — the middle term is minus two. Then you add two instead.']),
        dict(mode='concept', title='Recap', active=2, script=[
            "Let's lock it in.",
            A("'Products or ratios → multiply or divide' appears", T('Products or ratios $\\to$ multiply or divide the equations', 38)),
            A('(x ± 1/x)² = x² + 1/x² ± 2 appears', T('$\\left(x \\pm \\frac{1}{x}\\right)^2 = x^2+\\frac{1}{x^2} \\pm 2$', 44)),
            D('Tick each line'),
            'Two questions now — one for each tool. Try each one before you watch.'])], sec)

    sb = ['Question %d' % (M.next_question_number(TOPIC) + k) for k in range(2)]
    # Q21 - dividing equations
    q = 'q-r26-t07-01'
    _add_q(M, q, 'Given:\n' + CASES('x^2y = 18', 'xy^2 = 12') + '\n$\\frac{x}{y} = ?$',
           ['$\\frac{2}{3}$', '$\\frac{3}{2}$', '$6$', '$\\frac{9}{4}$'], 2, [
               'Divide the first equation by the second: $\\frac{x^2y}{xy^2} = \\frac{18}{12}$.',
               'One $x$ and one $y$ cancel: $\\frac{x}{y} = \\frac{3}{2}$.',
               'Check: $x = 3$ and $y = 2$ give $9 \\cdot 2 = 18$ and $3 \\cdot 4 = 12$ ✓.'], sec)
    _solution(M, q, title, sb, ['Question twenty-one.', 'Two equations — and each one is a product.'], [
        ('Divide the equations', [
            'They want x over y. Not x, not y — a ratio.',
            "Both equations are products. That's the signal: multiply or divide them.",
            D('Write "x²y ÷ xy² = 18 ÷ 12"'),
            'Divide the first equation by the second. Left side by left side, right side by right side.',
            D('Cancel one x and one y; write "x/y = 18/12 = 3/2"'),
            "x squared y over x y squared: one x and one y cancel. What's left: x over y.",
            'Eighteen over twelve — three halves.',
            D('Circle choice 2'),
            'Choice two.',
            'Choice one — two thirds — is the upside-down trap. Keep the same order on both sides.']),
        ('Check with numbers', [
            'Quick check. Three halves: try x equals three, y equals two.',
            D('Write "x = 3, y = 2: 9 · 2 = 18 ✓, 3 · 4 = 12 ✓"'),
            'Nine times two — eighteen. Three times four — twelve. Both fit.',
            'Divide the equations — one line, no solving.'])], sec)
    # Q22 - x + 1/x
    q = 'q-r26-t07-02'
    _add_q(M, q, 'Given: $x + \\frac{1}{x} = 3$. $x^2 + \\frac{1}{x^2} = ?$',
           ['$9$', '$7$', '$11$', '$5$'], 2, [
               'Square both sides: $\\left(x + \\frac{1}{x}\\right)^2 = 9$.',
               'Expand: $x^2 + 2 \\cdot x \\cdot \\frac{1}{x} + \\frac{1}{x^2} = x^2 + 2 + \\frac{1}{x^2}$. The middle term is just $2$.',
               'Therefore $x^2 + \\frac{1}{x^2} + 2 = 9$, and $x^2 + \\frac{1}{x^2} = 7$.'], sec)
    _solution(M, q, title, sb, ['Question twenty-two.', 'x plus one over x. A classic.'], [
        ('Square both sides', [
            'They give x plus one over x. They want x squared plus one over x squared.',
            'Squares in the target, no squares in the given? Square the given.',
            D('Write "(x + 1/x)² = 3² = 9"'),
            'x plus one over x, squared — nine.',
            D('Write "x² + 2 · x · (1/x) + 1/x² = 9"'),
            'Square of a sum: x squared, plus two times x times one over x, plus one over x squared.',
            'Look at the middle: x times one over x is one. So the middle term is just two.',
            D('Write "x² + 2 + 1/x² = 9 → x² + 1/x² = 7"'),
            'Take away two: seven.',
            D('Circle choice 2'),
            'Choice two.',
            'The trap: squaring each part and forgetting the middle term. That gives nine — choice one.'])], sec)


# ---------------------------------------------------------------- 4. new lesson: quadratic equations + guided Q23-25
def _new_section(M, sid, title, after_sec):
    """The API cannot create sections; add one right after `after_sec` (same topic, kind 'learn')."""
    sec = {'id': sid, 'topic': TOPIC, 'title': title, 'kind': 'learn', 'questionCount': 0, 'items': []}
    lst = M.D['sections']
    lst.insert(next(k for k, s in enumerate(lst) if s['id'] == after_sec) + 1, sec)
    M.sections[sid] = sec
    top = next(t for t in M.D['topics'] if t['id'] == TOPIC)
    top['sections'].insert(top['sections'].index(after_sec) + 1, sid)


def quadratics(M):
    sec = 'r26-t07-quadratic'
    _new_section(M, sec, 'Quadratic equations', 'equation-b')
    title = 'Quadratic Equations'
    M.new_video('r26-t07-quadratic', TOPIC, title,
                ['What it looks like', 'Factor', 'Two solutions', 'Special cases', 'The trap: a² = b²',
                 'Try the choices', 'Fraction = 0', 'Recap'], [
        dict(mode='title', title=title, script=[
            'Quadratic equations.',
            'An x squared, an x, and a number — like x squared minus five x plus six equals zero.',
            "The exam doesn't need a big formula. You factor — or you try the choices.",
            "Let's see how."]),
        dict(mode='concept', title='What it looks like', active=0, script=[
            'A quadratic equation has x squared, maybe an x term, and a number.',
            A('x² + bx + c = 0 appears', T('$x^2+bx+c=0$', 64)),
            'The standard form: x squared plus b x plus c equals zero.',
            A('x² − 5x + 6 = 0 appears', T('$x^2-5x+6=0$', 56)),
            'Our example: x squared minus five x plus six equals zero.',
            A("'Step 1: everything to one side, 0 on the other' appears", T('Step 1: everything to one side, $0$ on the other', 40)),
            'Step one, always: move everything to one side. Zero on the other side.',
            'Why zero? Because a product equal to zero is the one thing we know how to split.',
            A("'Common number? Divide it out first' appears", T('Common number? Divide it out: $2x^2-10x+12=0 \\to x^2-5x+6=0$', 34)),
            'Every term has a common number? Divide it out first. Two x squared minus ten x plus twelve — divide by two.']),
        dict(mode='concept', title='Factor', active=1, script=[
            'Now factor. Look for two numbers.',
            A("'Two numbers: product = c, sum = b' appears", T('Find two numbers: product $= c$, sum $= b$', 42)),
            'Their product is the number c. Their sum is b — the number in front of x.',
            A("'x² − 5x + 6: product 6, sum −5' appears", T('$x^2-5x+6$: product $6$, sum $-5$', 44)),
            'Here: product six, sum negative five.',
            'Positive product, negative sum — both numbers are negative.',
            A('(−2)·(−3) = 6, (−2) + (−3) = −5 appears', T('$(-2)\\cdot(-3)=6 \\qquad (-2)+(-3)=-5$', 44)),
            'Negative two and negative three. Times: six. Plus: negative five.',
            A('x² − 5x + 6 = (x − 2)(x − 3) appears', T('$x^2-5x+6=(x-2)(x-3)$', 50)),
            "So it's x minus two, times x minus three.",
            D('Expand (x − 2)(x − 3) to check: x² − 3x − 2x + 6'),
            'Check by opening the brackets: x squared, minus five x, plus six. Correct.']),
        dict(mode='concept', title='Two solutions', active=2, script=[
            'Now use the rule we already know: a product is zero when one factor is zero.',
            A('(x − 2)(x − 3) = 0 appears', T('$(x-2)(x-3)=0$', 56)),
            A("'x − 2 = 0 or x − 3 = 0' appears", T('$x-2=0$ or $x-3=0$', 48)),
            'Either x minus two is zero, or x minus three is zero.',
            A("'x = 2 or x = 3' appears", T('$x=2$ or $x=3$', 52)),
            'x is two, or x is three. Two solutions.',
            D('Write "x = 2: 4 − 10 + 6 = 0 ✓"'),
            'Check two: four minus ten plus six — zero.',
            'Watch the signs. The factor is x minus two, but the solution is plus two. The sign flips.']),
        dict(mode='concept', title='Special cases', active=3, script=[
            'Three special cases.',
            A("'No number term' appears", T('No number: $x^2=5x \\to x(x-5)=0 \\to x=0$ or $x=5$', 38)),
            'No number term? Take out x. Never divide by x — you lose the zero. Solutions: zero and five.',
            A("'No x term' appears", T('No $x$ term: $x^2=9 \\to x=3$ or $x=-3$', 38)),
            'No x term? Take a root — plus AND minus. Three or negative three.',
            A("'Perfect square' appears", T('Same two numbers: $x^2-6x+9=(x-3)^2=0 \\to x=3$ only', 38)),
            'Sometimes both numbers are the same: negative three and negative three. Only ONE solution: three.',
            A("'x² = −4 → no solution' appears", T('$x^2=-4$ $\\to$ no solution', 38)),
            'And x squared equals negative four? No number squared is negative. No solution.',
            'So a quadratic can have two solutions, one solution — or none.']),
        dict(mode='concept', title='The trap: a² = b²', active=4, script=[
            'Now the most common trap.',
            A("'a² = b² → a = b or a = −b' appears", T('$a^2=b^2 \\;\\to\\; a=b$ or $a=-b$', 52)),
            'Two squares are equal. Are the numbers equal? Not necessarily. They can be equal — or opposite.',
            A("'3² = (−3)² but 3 ≠ −3' appears", T('$3^2=(-3)^2$, but $3 \\ne -3$', 44)),
            'Three squared is nine. Negative three squared is nine. Same square, different numbers.',
            A('The example (x + 1)² = (x − 3)² appears', T('$(x+1)^2=(x-3)^2$', 48)),
            'Example: x plus one, squared, equals x minus three, squared.',
            D('Write "x + 1 = x − 3 → 1 = −3 ✗"'),
            'Case one: x plus one equals x minus three. That says one equals negative three — impossible.',
            D('Write "x + 1 = −(x − 3) → 2x = 2 → x = 1 ✓"'),
            'Case two: x plus one equals minus x plus three. Two x equals two — x is one.',
            'Students who check only the first case answer no solution. Always check both cases.']),
        dict(mode='concept', title='Try the choices', active=5, script=[
            "Short on time? You don't have to factor.",
            A("'Numbers in the answers? Put each one in.' appears", T('Numbers in the answers? Put each one in.', 42)),
            'If the answers are numbers, put each choice into the equation. The one that fits is a solution.',
            A('x² − 5x + 6 = 0: x = 2 → 4 − 10 + 6 = 0 appears', T('$x^2-5x+6=0$: $\\ x=2 \\to 4-10+6=0$ ✓', 42)),
            'Two: four minus ten plus six. Zero. It works.',
            'This is great for "which of the following could be x" questions.',
            A("'How many solutions? → factor, don't guess' appears", T("How many solutions? $\\to$ factor, don't guess", 40)),
            "But a choice that works is ONE solution — maybe not the only one. For how many solutions, factor."]),
        dict(mode='concept', title='Fraction = 0', active=6, script=[
            'One more trap: a fraction equal to zero.',
            A("'Fraction = 0: numerator = 0, denominator ≠ 0' appears", T('Fraction $=0$: numerator $=0$, denominator $\\ne 0$', 42)),
            'The top must be zero. The bottom must NOT be zero.',
            A('(x² − 9)/(x − 3) = 0 appears', T('$\\frac{x^2-9}{x-3}=0$', 56)),
            'x squared minus nine, over x minus three.',
            'Top zero: x squared is nine. Three or negative three.',
            A("'x = 3 or x = −3, but x ≠ 3 → x = −3' appears", T('$x=3$ or $x=-3$, but $x \\ne 3$ $\\to$ $x=-3$', 44)),
            'But three makes the bottom zero. Throw it out. Only negative three.',
            'After you solve, always check that no denominator becomes zero.']),
        dict(mode='concept', title='Recap', active=7, script=[
            "Let's lock it in.",
            A("'1. Everything to one side, = 0' appears", T('1. Everything to one side, $=0$', 38)),
            A("'2. Product c, sum b → factor' appears", T('2. Product $c$, sum $b$ $\\to$ factor', 38)),
            A("'3. Each factor = 0 — the sign flips' appears", T('3. Each factor $=0$ — the sign flips', 38)),
            A("'a² = b² → a = b or a = −b' appears", T('$a^2=b^2 \\to a=b$ or $a=-b$', 38)),
            A("'Fraction: denominator ≠ 0' appears", T('Fraction: the denominator $\\ne 0$', 38)),
            D('Tick each line'),
            'Three questions now. Try each one before you watch.'])], sec, after='solve-q-r26-t07-02')

    sb = ['Question %d' % (M.next_question_number(TOPIC) + k) for k in range(3)]
    # Q23 - factor a trinomial
    q = 'q-r26-t07-04'
    _add_q(M, q, 'Given: $x^2 - 2x = 15$. Which of the following could be the value of $x$?',
           ['$-5$', '$-3$', '$3$', '$15$'], 2, [
               'Move everything to one side: $x^2 - 2x - 15 = 0$.',
               'Two numbers with product $-15$ and sum $-2$: $-5$ and $3$. Therefore $(x - 5)(x + 3) = 0$.',
               'Therefore $x = 5$ or $x = -3$. Only $-3$ is among the choices.',
               'Check: $(-3)^2 - 2 \\cdot (-3) = 9 + 6 = 15$ ✓.'], sec)
    _solution(M, q, title, sb, ['Question twenty-three.', 'An x squared and an x. A quadratic.'], [
        ('Everything to one side', [
            'Tempting: x times x minus two is fifteen — so x is fifteen? No!',
            'A product equal to ZERO splits into cases. A product equal to fifteen does not.',
            D('Write "x² − 2x − 15 = 0"'),
            'First, everything to one side. Zero on the right.',
            'Now two numbers: product negative fifteen, sum negative two.',
            D('Write "(−5) · 3 = −15,  (−5) + 3 = −2"'),
            'Negative five and three. Product: negative fifteen. Sum: negative two.',
            D('Write "(x − 5)(x + 3) = 0"'),
            'So the equation is x minus five, times x plus three, equals zero.',
            D('Write "x = 5 or x = −3"'),
            'x minus five is zero: x is five. x plus three is zero: x is negative three.',
            "Five isn't among the choices. Negative three is.",
            D('Circle choice 2'),
            'Choice two.']),
        ('Method 2 · Try the choices', [
            'Numbers in the answers? Try them in x squared minus two x.',
            D('Next to the choices write "35, 15 ✓, 3, 195"'),
            'Negative five: twenty-five plus ten — thirty-five. Negative three: nine plus six — fifteen. Yes.',
            'Three: nine minus six — three. Fifteen: far too big.',
            'Choice two again. For "which could be" questions, trying the choices is very fast.'])], sec)
    # Q24 - the a^2 = b^2 trap
    q = 'q-r26-t07-05'
    _add_q(M, q, 'Given: $(x + 1)^2 = (x - 3)^2$. $x = ?$',
           ['$-1$', '$1$', '$3$', 'No number satisfies the equation.'], 2, [
               'If $a^2 = b^2$, then $a = b$ or $a = -b$.',
               'Case 1: $x + 1 = x - 3$, that is, $1 = -3$. This is impossible.',
               'Case 2: $x + 1 = -(x - 3) = -x + 3$. Therefore $2x = 2$ and $x = 1$.',
               'Check: $(1 + 1)^2 = 4$ and $(1 - 3)^2 = 4$ ✓.'], sec)
    _solution(M, q, title, sb, ['Question twenty-four.', 'Two equal squares. Here comes the trap.'], [
        ('Plus or minus', [
            'The tempting move: the squares are equal, so the insides are equal.',
            D('Write "x + 1 = x − 3 → 1 = −3 ✗"'),
            'x plus one equals x minus three? Then one equals negative three. Impossible.',
            "Many students stop here and pick choice four: no solution. That's the trap.",
            'Two numbers with the same square are equal — or opposite.',
            D('Write "a² = b² → a = b or a = −b"'),
            "So there's a second case.",
            D('Write "x + 1 = −(x − 3) = −x + 3 → 2x = 2 → x = 1"'),
            'x plus one equals negative x plus three. Two x is two. x is one.',
            D('Write "x = 1: 2² = 4, (−2)² = 4 ✓"'),
            'Check: one plus one is two, squared — four. One minus three is negative two, squared — four.',
            D('Circle choice 2'),
            'Choice two.']),
        ('Method 2 · Expand', [
            'Or open both squares.',
            D('Write "x² + 2x + 1 = x² − 6x + 9"'),
            'Square of a sum on the left, square of a difference on the right.',
            D('Write "8x = 8 → x = 1"'),
            'The x squared cancels. Eight x equals eight. x is one.',
            'Same answer. Choice two.'])], sec)
    # Q25 - fraction = 0, extraneous solution; try the choices
    q = 'q-r26-t07-06'
    _add_q(M, q, 'Given: $\\frac{x^2 - 7x + 12}{x - 3} = 0$. $x = ?$',
           ['$3$', '$4$', '$3$ or $4$', '$-4$'], 2, [
               'A fraction is $0$ when its numerator is $0$ and its denominator is not $0$.',
               'Numerator: two numbers with product $12$ and sum $-7$: $-3$ and $-4$. Therefore $(x - 3)(x - 4) = 0$, and $x = 3$ or $x = 4$.',
               'But $x = 3$ makes the denominator $0$, which is not allowed. Therefore $x = 4$ only.',
               'Trying the choices: $x = 3$ gives $\\frac{0}{0}$, which is not a number. $x = 4$ gives $\\frac{0}{1} = 0$ ✓. $x = -4$ gives $\\frac{56}{-7} = -8$.'], sec)
    _solution(M, q, title, sb, ['Question twenty-five.', 'A fraction equal to zero. Watch the denominator.'], [
        ('Top zero, bottom not', [
            'A fraction is zero when the top is zero — and the bottom is not.',
            D('Write "x² − 7x + 12 = 0"'),
            'Top first. Two numbers: product twelve, sum negative seven.',
            D('Write "(x − 3)(x − 4) = 0 → x = 3 or x = 4"'),
            'Negative three and negative four. So x is three or four.',
            'Now the bottom: x minus three.',
            D('Next to "x = 3" write "bottom = 0 ✗"'),
            "x equals three makes the bottom zero. You can't divide by zero. Throw it out.",
            D('Circle choice 2'),
            'Only four. Choice two.',
            'Choice three — three or four — is the trap. It forgets the denominator.']),
        ('Method 2 · Try the choices', [
            D('Next to choice 1 write "0/0 ✗"'),
            'Try three: zero over zero. Not a number. Out.',
            D('Next to choice 2 write "0/1 = 0 ✓"'),
            'Try four: sixteen minus twenty-eight plus twelve — zero. Over one. Zero. Yes.',
            D('Next to choice 4 write "56/(−7) = −8 ✗"'),
            'Try negative four: fifty-six over negative seven. Not zero.',
            'Choice two.'])], sec)


# ---------------------------------------------------------------- 5. practice
NEW_PRACTICE = [
    # id suffix, stem, choices, correct, expl
    ('07', 'Given: $x^2 - 6x + 8 = 0$. What are the solutions of the equation?',
     ['$2$ and $4$', '$-2$ and $-4$', '$1$ and $8$', '$-2$ and $4$'], 1, [
         'Two numbers with product $8$ and sum $-6$: $-2$ and $-4$. Therefore $(x - 2)(x - 4) = 0$.',
         'Therefore $x = 2$ or $x = 4$. (The signs flip: the factor $x - 2$ gives the solution $2$.)']),
    ('08', 'Given: $2x^2 = 8x$. The number of solutions of the given equation is —',
     ['$0$', '$1$', '$2$', '$3$'], 3, [
         'Do not divide by $x$. Move everything to one side: $2x^2 - 8x = 0$.',
         'Take out $2x$: $2x(x - 4) = 0$. Therefore $x = 0$ or $x = 4$.',
         'Two solutions. (Dividing by $x$ would lose $x = 0$.)']),
    ('09', 'Given: $x^2 = y^2$. Which of the following is necessarily true?',
     ['$x = y$', '$x = -y$', '$|x| = |y|$', '$x = 0$ or $y = 0$'], 3, [
         '$x^2 = y^2$ means $x = y$ or $x = -y$. We do not know which.',
         'Example: $x = 2$, $y = -2$ fits, but $x \\ne y$. Example: $x = y = 2$ fits, but $x \\ne -y$ and neither number is $0$.',
         'In every case $x$ and $y$ have the same size: $|x| = |y|$.']),
    ('10', 'Given: $\\frac{x^2 - 9}{x - 3} = 0$. $x = ?$',
     ['$3$', '$-3$', '$3$ or $-3$', 'No number satisfies the equation.'], 2, [
         'The numerator must be $0$: $x^2 = 9$. Therefore $x = 3$ or $x = -3$.',
         'The denominator cannot be $0$: $x \\ne 3$.',
         'Therefore $x = -3$ only. Check: $\\frac{9 - 9}{-3 - 3} = \\frac{0}{-6} = 0$ ✓.']),
    ('11', 'Given: $x^2 - 10x + 25 = 0$. How many different values can $x$ take?',
     ['$0$', '$1$', '$2$', '$4$'], 2, [
         'Two numbers with product $25$ and sum $-10$: $-5$ and $-5$. Therefore $(x - 5)^2 = 0$.',
         'A square is $0$ only when the number is $0$: $x - 5 = 0$, and $x = 5$.',
         'Only one value.']),
    ('12', 'Given: $x > 0$ and $(2x - 1)^2 = (x + 4)^2$. $x = ?$',
     ['$-1$', '$1$', '$3$', '$5$'], 4, [
         '$a^2 = b^2$ means $a = b$ or $a = -b$.',
         'Case 1: $2x - 1 = x + 4$. Therefore $x = 5$.',
         'Case 2: $2x - 1 = -x - 4$. Therefore $3x = -3$ and $x = -1$. But $x > 0$.',
         'Therefore $x = 5$. Check: $9^2 = 81$ and $9^2 = 81$ ✓.']),
    ('13', 'Given: $x - \\frac{1}{x} = 4$. $x^2 + \\frac{1}{x^2} = ?$',
     ['$14$', '$16$', '$18$', '$20$'], 3, [
         'Square both sides: $\\left(x - \\frac{1}{x}\\right)^2 = 16$.',
         'Expand: $x^2 - 2 + \\frac{1}{x^2} = 16$. The middle term is $-2$.',
         'Therefore $x^2 + \\frac{1}{x^2} = 18$.']),
    ('14', 'Given: $x > 0$ and $x^2 + \\frac{1}{x^2} = 14$. $x + \\frac{1}{x} = ?$',
     ['$\\sqrt{12}$', '$4$', '$\\sqrt{14}$', '$16$'], 2, [
         '$\\left(x + \\frac{1}{x}\\right)^2 = x^2 + 2 + \\frac{1}{x^2} = 14 + 2 = 16$.',
         'Therefore $x + \\frac{1}{x} = 4$ or $x + \\frac{1}{x} = -4$.',
         'Since $x > 0$, $x + \\frac{1}{x} > 0$. Therefore $x + \\frac{1}{x} = 4$.']),
    ('15', 'Given:\n' + CASES('xy = 12', 'yz = 6') + '\n$\\frac{x}{z} = ?$',
     ['$2$', '$\\frac{1}{2}$', '$6$', '$72$'], 1, [
         'Divide the first equation by the second: $\\frac{xy}{yz} = \\frac{12}{6}$.',
         'The $y$ cancels ($y \\ne 0$, since $xy = 12$): $\\frac{x}{z} = 2$.']),
    ('16', 'Given: $x > 0$, $y > 0$, $z > 0$ and\n' + CASES('xy = 12', 'yz = 6', 'xz = 8') + '\n$xyz = ?$',
     ['$24$', '$26$', '$48$', '$576$'], 1, [
         'Multiply the three equations: $xy \\cdot yz \\cdot xz = 12 \\cdot 6 \\cdot 8$, that is, $(xyz)^2 = 576$.',
         'Therefore $xyz = 24$ or $xyz = -24$. All three numbers are positive. Therefore $xyz = 24$.',
         'Check: $x = 4$, $y = 3$, $z = 2$ ✓.']),
    ('19', 'Given: $x = 2y + 3$. $4y = ?$',
     ['$2x - 6$', '$2x - 3$', '$\\frac{x - 3}{2}$', '$x - 6$'], 1, [
         'Plug in: $y = 1$ gives $x = 5$ and $4y = 4$.',
         'The choices give $2 \\cdot 5 - 6 = 4$, then $7$, $1$ and $-1$. Only choice 1 gives $4$.',
         'Algebra: $2y = x - 3$. Therefore $4y = 2(x - 3) = 2x - 6$.']),
    ('20', 'Given:\n' + CASES('x + y = k', 'x - y = 2') + '\n$xy = ?$',
     ['$\\frac{k^2 - 4}{4}$', '$\\frac{k^2 - 4}{2}$', '$\\frac{k^2}{4} - 2$', '$\\frac{(k - 2)^2}{4}$'], 1, [
         'Plug in: $x = 3$ and $y = 1$ fit $x - y = 2$. Then $k = 4$ and $xy = 3$.',
         'With $k = 4$ the choices give $3$, $6$, $2$ and $1$. Only choice 1 gives $3$.',
         'Algebra: $x = \\frac{k + 2}{2}$ and $y = \\frac{k - 2}{2}$. Therefore $xy = \\frac{(k + 2)(k - 2)}{4} = \\frac{k^2 - 4}{4}$.']),
    ('21', 'Given: $\\frac{3}{4}x + \\frac{1}{5}x = 38$. $x = ?$',
     ['$30$', '$36$', '$40$', '$57$'], 3, [
         'Estimate first: $\\frac{3}{4} + \\frac{1}{5}$ is a bit less than $1$. A bit less than all of $x$ is $38$. Therefore $x$ is a bit more than $38$. Only $40$ fits.',
         'Exact: $\\frac{3}{4} + \\frac{1}{5} = \\frac{15}{20} + \\frac{4}{20} = \\frac{19}{20}$. Therefore $\\frac{19}{20}x = 38$ and $x = 38 \\cdot \\frac{20}{19} = 40$.']),
]


def practice(M):
    sec = 'unit-t7-5'
    for suf, stem, ch, c, ex in NEW_PRACTICE:
        _add_q(M, 'q-r26-t07-' + suf, stem, ch, c, ex, sec)
    n = lambda s: 'q-r26-t07-' + s
    a = lambda k: 'alg-extra-unit-t7-5-%d' % k
    M.practice_order(sec, [
        a(1), a(2), a(3), a(6), n('07'), a(5), a(4), a(7), 'q-198', 'q-212', 'q-199', n('15'), n('19'), n('08'),
        n('10'), n('21'), 'q-200', 'q-210', 'q-211', 'q-201', 'q-202', 'q-204', 'q-205', 'q-206', n('09'), n('13'),
'q-209', 'q-203', 'q-207', 'q-213', 'q-216', 'q-217', n('11'), n('20'), n('14'), n('12'), n('16'),
        'q-215', 'q-208', 'q-214'])


# ---------------------------------------------------------------- 6. memory card
def card(M):
    M.new_card('mem-r26-t07-equations', TOPIC, 'equation-theory', {
        'title': 'Equations: traps and shortcuts',
        'intro': 'Check this list before you calculate.',
        'tables': [
            {'title': 'Traps', 'head': ['You see', 'Do this'], 'rows': [
                ['$x^3 = x^2y$', 'Divide by $x$ only if $x \\ne 0$. Otherwise factor: $x^2(x - y) = 0$'],
                ['$(x - 6)^2 = 16$', 'Plus AND minus: $x - 6 = 4$ or $x - 6 = -4$'],
                ['$a^2 = b^2$', '$a = b$ or $a = -b$ (not only $a = b$)'],
                ['A fraction $= 0$', 'Numerator $= 0$ and denominator $\\ne 0$ — throw out bad solutions'],
                ['"Cannot be determined"', 'Only if different allowed cases give different answers']]},
            {'title': 'Which operation?', 'head': ['You see', 'Do this'], 'rows': [
                ['Mirror coefficients: $3x + 7y$, $7x + 3y$', 'Add (or subtract) the equations'],
                ['A letter missing from the answers', 'Make that letter cancel'],
                ['Products or ratios: $xy = 12$, $yz = 6$', 'Multiply or divide the equations: $\\frac{x}{z} = 2$'],
                ['$x \\pm y$, $x^2 + y^2$, $xy$', '$(x \\pm y)^2 = x^2 + y^2 \\pm 2xy$ — know two, get the third'],
                ['$x \\pm \\frac{1}{x}$', '$\\left(x \\pm \\frac{1}{x}\\right)^2 = x^2 + \\frac{1}{x^2} \\pm 2$'],
                ['Letters in the answers', 'Plug in numbers (not $0$ or $1$) and check all four choices'],
                ['Numbers in the answers', 'Try the choices in the question']]},
            {'title': 'Quadratic equations', 'head': ['Step', 'Example'], 'rows': [
                ['1. Everything to one side, $= 0$', '$x^2 - 5x = -6 \\to x^2 - 5x + 6 = 0$'],
                ['2. Two numbers: product $= 6$, sum $= -5$', '$-2$ and $-3$'],
                ['3. Factor', '$(x - 2)(x - 3) = 0$'],
                ['4. Each factor $= 0$ (the sign flips)', '$x = 2$ or $x = 3$']]}],
        'tips': [
            '$x^2 = 9$ has two solutions ($3$ and $-3$). $(x - 5)^2 = 0$ has one ($5$). $x^2 = -4$ has none.',
            '"Necessarily true": one legal counterexample kills a choice.']},
        after='equation-strategy')


def apply(M):
    fix_lesson(M)
    fix_solution_videos(M)
    fix_questions(M)
    more_tools(M)
    quadratics(M)
    practice(M)
    card(M)
    summary(M)
    new_numbers(M)
    order_changes(M)
    dedupe_examples(M)   # 2026-10-04
    pen_or_click(M)      # 2026-10-05
    hebrew_intro(M)      # 2026-10-05: runs last


# ---------------------------------------------------------------- 7. pass 2: summary video before the practice
def summary(M):
    sb = ["Don't divide by x", 'Plus AND minus', 'Quadratics', 'Fraction = 0', 'Build the expression',
          'Hidden formulas', 'Two unknowns', 'Plug in or try', 'Before you practice']
    slides = [
        dict(mode='title', title='Summary', script=[
            'Before you practice, a quick summary of equations.',
            'The rules, the shortcuts and the traps — in three minutes.']),
        dict(mode='concept', title="Don't divide by x", active=0, pre=[], script=[
            A('x³ = 3x² → x²(x − 3) = 0 appears', T('$x^3=3x^2 \;\\to\; x^2(x-3)=0 \;\\to\; x=0$ or $x=3$', 44)),
            "Dividing by x? Only if x can't be zero.",
            'Otherwise: everything to one side, take out the common factor, and split the product.']),
        dict(mode='concept', title='Plus AND minus', active=1, pre=[], script=[
            A('(x + 2)² = 25 → x + 2 = 5 or −5 appears', T('$(x+2)^2=25 \;\\to\; x+2=5$ or $x+2=-5$', 44)),
            'Taking a root to solve? Plus AND minus.',
            A('a² = b² → a = b or a = −b appears', T('$a^2=b^2 \;\\to\; a=b$ or $a=-b$', 46)),
            'Two equal squares: the numbers are equal — or opposite. Check both cases.']),
        dict(mode='concept', title='Quadratics', active=2, pre=[], script=[
            A('x² − 8x + 15 = (x − 3)(x − 5) = 0 appears', T('$x^2-8x+15=(x-3)(x-5)=0$', 48)),
            'Everything to one side, zero on the other. Two numbers: product c, sum b.',
            A('x = 3 or x = 5 appears', T('$x=3$ or $x=5$ — the sign flips', 44)),
            'Each factor equals zero. Watch the sign: x minus three gives three.',
            'Two solutions, one — like x minus seven, squared — or none, like x squared equals minus nine.']),
        dict(mode='concept', title='Fraction = 0', active=3, pre=[], script=[
            A("'Numerator = 0, denominator ≠ 0' appears", T('Fraction $=0$: numerator $=0$, denominator $\\ne 0$', 42)),
            'A fraction is zero when the top is zero — and the bottom is not.',
            A('(x² − 25)/(x + 5) = 0 → x = 5 appears', T('$\\frac{x^2-25}{x+5}=0 \;\\to\; x=5$ only', 46)),
            'Minus five makes the bottom zero. Throw it out.']),
        dict(mode='concept', title='Build the expression', active=4, pre=[], script=[
            A("'Asked for an expression? Build it directly' appears", T('Asked for an expression? Build it directly', 40)),
            "Don't find every letter. Add, subtract — or divide — the equations.",
            A("'Mirror coefficients → add' appears", T('Mirror coefficients $\\to$ add', 36)),
            'Mirror coefficients? Add.',
            A("'A letter missing from the answers → make it cancel' appears", T('A letter missing from the answers $\\to$ make it cancel', 36)),
            'A letter missing from the answers? Make it cancel.',
            A("'Products or ratios → multiply or divide' appears", T('Products or ratios $\\to$ multiply or divide', 36)),
            'Products or ratios? Multiply or divide.']),
        dict(mode='concept', title='Hidden formulas', active=5, pre=[], script=[
            A('(x ± y)² = x² + y² ± 2xy appears', T('$(x\\pm y)^2=x^2+y^2\\pm 2xy$', 46)),
            'x plus or minus y, x squared plus y squared, and x y: know two, get the third.',
            A('(x ± 1/x)² = x² + 1/x² ± 2 appears', T('$\\left(x\\pm\\frac{1}{x}\\right)^2=x^2+\\frac{1}{x^2}\\pm 2$', 46)),
            'x plus one over x: the middle term is just two.',
            A('2a + b + c = (a + b) + (a + c) appears', T('$2a+b+c=(a+b)+(a+c)$', 44)),
            'A big equation? Break it into the small ones.']),
        dict(mode='concept', title='Two unknowns', active=6, pre=[], script=[
            A("'One equation, two unknowns → a relationship' appears", T('One equation, two unknowns $\\to$ a relationship', 40)),
            "One equation, two unknowns: no values — but a relationship. a plus five equals b means b is bigger.",
            A("'Necessarily true = true in EVERY allowed case' appears", T('Necessarily true = true in EVERY allowed case', 38)),
            'One legal counterexample kills a choice.',
            '"Cannot be determined" only when different allowed cases give different answers.']),
        dict(mode='concept', title='Plug in or try', active=7, pre=[], script=[
            A("'Letters in the answers → plug in numbers' appears", T('Letters in the answers $\\to$ plug in numbers', 40)),
            'Numbers that fit all the givens. Avoid zero and one. Check all four choices.',
            A("'Numbers in the answers → try them' appears", T('Numbers in the answers $\\to$ try them in the question', 40)),
            'A choice that works is A solution — maybe not the only one.']),
        dict(mode='concept', title='Before you practice', active=8, pre=[], script=[
            'Before every question, ask yourself:',
            A("'Am I dividing by something that could be 0?' appears", T('Am I dividing by something that could be $0$?', 38)),
            A("'Did I take plus AND minus?' appears", T('Did I take plus AND minus?', 38)),
            A("'Does a solution make a denominator 0?' appears", T('Does a solution make a denominator $0$?', 38)),
            A("'Do I need each letter — or just the expression?' appears", T('Do I need each letter — or just the expression?', 38)),
            'The classic traps: losing x equals zero, forgetting the negative root, and keeping a solution that breaks the denominator.',
            'Now go practice.'])]
    M.new_video('r26-t07-summary', TOPIC, 'Equations: Summary', sb, slides, 'r26-t07-quadratic', after='solve-q-r26-t07-06')


# ======================================================================================================
# 2026-10-02 new numbers (teacher: the English course must not look identical to the Hebrew one - same ideas,
# same methods and tips, same psychometric style). Every question from the Hebrew course (guided q-178 .. q-197,
# self-practice q-198 .. q-217 and the study-guide variants q-172 .. q-177) and every lesson example that is the
# Hebrew lesson's own example gets new numbers / letters / coefficients / choice order. Same idea, same trap, same
# difficulty level, same answer type. Every number below was re-checked in python.
# ======================================================================================================
NOTDET = 'It cannot be determined from the information given.'


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
    # already RECORDED by the teacher with the old numbers - question and video stay exactly as recorded.
    # Nothing in topic 7 is recorded yet (2026-10-02); add ids here (e.g. 'q-191') to protect a recording.
    RECORDED = set()

    def S(qid, **kw):
        if qid in RECORDED: return
        q = M.set_q(qid, **kw)
        for v in M.D['videos'].values():   # pre-loaded copies of the choices (set_q syncs only the stem)
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
        q, v = M.q(qid), M.video(vid)
        t = re.sub(r'\\begin\{cases\}(.*?)\\end\{cases\}', lambda m: ', '.join(x.strip() for x in m.group(1).split('\\\\')) + '.', q['stemRich'], flags=re.S)
        v['title'] = ' %s ' % re.sub(r'\s+', ' ', t.replace('$', '')).strip(); v['navLabel'] = v['title'].strip()[:120]

    # ---------------- lesson "Solving Equations Smarter": the Hebrew lesson's own examples -> new examples
    if 'q-191' not in RECORDED:
        L = 'equation-strategy'
        # Hebrew x^3 = x^2 y  ->  p^3 = p^2 q (same trap: cancelling p^2 loses p = 0)
        M.set_slide(L, 2, pre=[T('$p^3=p^2q$', size=68, gap=40)], script=[
            'Looks obvious, right? q equals p.',
            'Cancel p squared on both sides — done. Or is it?',
            'You may divide both sides by something — but only if it is not zero.',
            'And nobody told us p is not zero.',
            D('Beside the equation write "p = 0 → 0 = 0"'),
            'Put p equals zero: zero equals zero. True for ANY q.',
            'So the safe move: everything to one side, then factor.',
            D('Below write "p²(p − q) = 0"'),
            'A product equals zero when at least one factor is zero.',
            D('Write "p = 0  or  q = p"'),
            'Either p is zero — or q equals p. Two branches. Dividing would have killed one of them.',
            "If the question says p isn't zero, cancel away. If it doesn't — split into cases.",
            D('Under it write "Or: check p = 0 separately"'),
            'A fast exam habit: before you divide by a letter, test that letter equal to zero on its own.',
            'Here p equals zero fits the equation. That branch is real — and dividing would have lost it.'])
        # Hebrew x^4 - 4x^2 = 0  ->  x^4 - 49x^2 = 0 (common factor, three solutions)
        M.set_slide(L, 3, pre=[T('$x^4-49x^2=0$', size=68, gap=40)], script=[
            "A power of two or more? Don't divide. Take out a common factor.",
            D('Write "x²(x² − 49) = 0"'),
            "x squared is common. What's left: x squared minus forty-nine.",
            "Now it's a product equal to zero — so one factor must be zero.",
            D('Write "x² = 0 → x = 0"'),
            "x squared is zero: x is zero. That's one.",
            D('Write "x² = 49 → x = 7 or x = −7"'),
            'x squared is forty-nine: seven — or negative seven.',
            D('Circle the three values and write "3 solutions"'),
            'Three different solutions: zero, seven, negative seven.',
            'And notice — dividing by x squared at the start would have erased the zero.'])
        # Hebrew (x - 7)^2 = 25  ->  (x - 2)^2 = 36 (two roots)
        M.set_slide(L, 4, pre=[T('$(x-2)^2=36$', size=68, gap=40)], script=[
            'Something squared is thirty-six. What could that something be?',
            'Six — or negative six. Both give thirty-six when you square them.',
            D('Write "x − 2 = 6  or  x − 2 = −6"'),
            'So split into two cases.',
            D('Write "x = 8  or  x = −4"'),
            'x minus two is six: x is eight. x minus two is negative six: x is negative four.',
            'Two solutions.',
            'Careful: the symbol root of thirty-six, on its own, means just six. But when YOU take a root to solve an equation, take both signs.'])
        # on-screen text that was a word-for-word translation of the Hebrew slides -> reworded
        _sub(M, L, 5, [('One equation, two unknowns $\\to$ no values…', 'Two unknowns, one equation $\\to$ no single values…'),
                       ("'One equation, two unknowns → no values…' appears", "'Two unknowns, one equation → no single values…' appears"),
                       ('…but a relationship between them', '…but you can still compare them'),
                       ('Underline "relationship"', 'Underline "compare"'),
                       ('But we CAN find how they relate — which one is bigger, and by how much.',
                        'But we CAN often compare them — which one is bigger, and by how much.')])
        _sub(M, L, 6, [("Asked for an expression? Don't find each letter.", 'They want an expression? Aim straight for it.'),
                       ("Then don't calculate every unknown separately. Calculate the expression directly.",
                        "You don't need every letter on its own. Go straight for the expression."),
                       ("How do you know which one? Practice. You'll start to recognize the patterns.",
                        "Which one to use? That comes with practice — after a few questions, you'll see the patterns.")])
        _sub(M, L, 7, [('($3x+7y$, $7x+3y$)', '($3x+8y$, $8x+3y$)'),
                       ('Coefficients in mirror order — three and seven, then seven and three?',
                        'Coefficients in mirror order — three and eight, then eight and three?'),
                       ('by five, say', 'by four, say')])
        _sub(M, L, 8, [('Notice I wrote the two x y at the end — just so the x squared plus y squared sit together.',
                        'I put the two x y last on purpose — this way x squared plus y squared stay side by side.'),
                       ('Find the right formula, plug in what you know, and isolate what they ask for.',
                        'Pick the matching formula, put in the values you know, and solve for the piece they want.')])
        _sub(M, L, 9, [('You could isolate and substitute letter by letter — but it takes ages.',
                        'Solving for one letter at a time works — but it takes ages.')])
        _sub(M, L, 10, [('If two x equals three y plus one, choose y first — y is one — then x is two.',
                         'If two x equals y plus three, choose y first — y is one — then x is two.'),
                        ('If m times n is one and you take m and n equal to one, every choice equals one.',
                         'If p times q is one and you take p and q equal to one, every choice equals one.')])
        _sub(M, L, 11, [('$(x-6)^2=16$: $\\ x=10 \\to 4^2=16$ ✓', '$(x-2)^2=36$: $\\ x=8 \\to 6^2=36$ ✓'),
                        ('The example (x − 6)² = 16, try x = 10 appears', 'The example (x − 2)² = 36, try x = 8 appears'),
                        ('For example: x minus six, squared, is sixteen. Is x ten? Ten minus six is four. Four squared: sixteen. Yes.',
                         'For example: x minus two, squared, is thirty-six. Is x eight? Eight minus two is six. Six squared: thirty-six. Yes.')])
        # memory card: the same examples as the lesson
        c = M.card('mem-r26-t07-equations')
        c['tables'][0]['rows'][0] = ['$p^3 = p^2q$', 'Divide by $p$ only if $p \\ne 0$. Otherwise factor: $p^2(p - q) = 0$']
        c['tables'][0]['rows'][1] = ['$(x - 2)^2 = 36$', 'Plus AND minus: $x - 2 = 6$ or $x - 2 = -6$']
        c['tables'][1]['rows'][0] = ['Mirror coefficients: $3x + 8y$, $8x + 3y$', 'Add (or subtract) the equations']

    # ================= theory: guided questions 1-7 (Hebrew lesson examples / study guide)
    # Q1. Hebrew x^3 = x^2 y; study guide x^7 = x^6 y. Now m^5 = m^4 n. Same trap (m = 0 -> any n), key "cannot be determined".
    S('q-191', stem='Given: $m^5 = m^4 n$. $n = ?$', choices=['$m$', '$0$', '$m^4$', NOTDET], correct=4, expl=[
        'If $m \\ne 0$, divide both sides by $m^4$: $n = m$.',
        'But if $m = 0$, the equation reads $0 = 0$, which is true for every $n$.',
        'Different cases give different values of $n$. Therefore $n$ cannot be determined (choice 4).'])
    video('q-191', {
        2: [
            'At first glance: n equals m. Then both sides are m to the fifth.',
            "Let's test that with a number. m equals two.",
            D('Write "m = 2: 32 = 16n → n = 2"'),
            'Two to the fifth is thirty-two. Two to the fourth is sixteen. So n is two — the same as m. So far, so good.',
            'Now try m equals zero.',
            D('Write "m = 0: 0 = 0 · n"'),
            "Zero equals zero times n. That's true for every n — three, seven, a million.",
            'So n might equal m… or it might be any number at all.',
            D('Circle choice 4'),
            "We can't pin it down. Choice four."],
        3: [
            'Where does the shortcut go wrong? Dividing both sides by m to the fourth.',
            D('Cross out the m⁴ on both sides and write "only if m ≠ 0"'),
            "You may divide only by something that isn't zero — and the question never says m isn't zero.",
            D('Write "m⁴(m − n) = 0 → m = 0 or n = m"'),
            'Factor instead: m to the fourth, times m minus n, equals zero. Two branches — so n has no single value.',
            'Choice four.']})

    # Q2. Hebrew x^4 - 4x^2 = 0; study guide x^4 - 16x^2. Now x^4 - 25x^2 = 0: 0, 5, -5 -> 3 solutions (key moved 2 -> 3).
    S('q-192', stem='Given: $x^4 - 25x^2 = 0$. The number of solutions of the given equation is —',
      choices=['$1$', '$2$', '$3$', '$4$'], correct=3, expl=[
        'Take out the common factor: $x^2(x^2 - 25) = 0$.',
        'A product is $0$ when one factor is $0$: $x^2 = 0$ gives $x = 0$, and $x^2 = 25$ gives $x = 5$ or $x = -5$.',
        'Three different solutions: $0$, $5$ and $-5$ (choice 3).',
        'Choice 2 is the trap: dividing by $x^2$ at the start loses the solution $x = 0$.'])
    video('q-192', {2: [
        'How many different values can x take?',
        'Power four and power two — take out a common factor.',
        D('Write "x²(x² − 25) = 0"'),
        'x squared, times x squared minus twenty-five.',
        'A product equals zero — so one of the factors is zero.',
        D('Write "x² = 0 → x = 0"'),
        'First case: x is zero.',
        D('Write "x² = 25 → x = 5 or x = −5"'),
        'Second case: x squared is twenty-five — five, or negative five.',
        D('Circle choice 3'),
        'Zero, five, negative five. Three solutions — choice three.',
        'Divide by x squared at the start, and you find only two — choice two. That is the trap.']})

    # Q3. Hebrew (x - 7)^2 = 25 (key 2); study guide (x - 6)^2 = 49. Now (x + 4)^2 = 81: 5 or -13 -> 2 values (key 3).
    S('q-193', stem='Given: $(x + 4)^2 = 81$. How many different values can $x$ take?',
      choices=['$0$', '$1$', '$2$', '$3$'], correct=3, expl=[
        'Something squared is $81$. Therefore $x + 4 = 9$ or $x + 4 = -9$.',
        'Therefore $x = 5$ or $x = -13$: two different values (choice 3).'])
    video('q-193', {2: [
        'Take a root of both sides.',
        "The root of eighty-one is nine. But inside an equation, it's plus OR minus nine.",
        D('Write "x + 4 = 9  or  x + 4 = −9"'),
        'Two cases.',
        D('Write "x = 5  or  x = −13"'),
        'Plus nine: x is five. Minus nine: x is negative thirteen.',
        D('Circle choice 3'),
        'Two different values. Choice three.',
        'The symbol root of eighty-one means just nine. But when you solve an equation by taking a root, take both signs.']})

    # Q4. Hebrew (a - 3b)/2 = 1 - b; study guide (a - 5b)/4 = 1 - b. Now (a - 6b)/5 = 1 - b -> a = b + 5, b < a (key 4).
    S('q-194', stem='Given: $\\frac{a - 6b}{5} = 1 - b$. Which of the following statements is necessarily true?',
      choices=['$a = b$', '$a < b$', '$a = 5b$', '$b < a$'], correct=4, expl=[
        'Multiply both sides by $5$: $a - 6b = 5 - 5b$.',
        'Add $6b$ to both sides: $a = b + 5$.',
        'Therefore $a$ is always $5$ more than $b$, and $b < a$ in every case (choice 4).'])
    video('q-194', {2: [
        "Two letters, one equation. We won't find a and b.",
        "But we can find how they're related.",
        D('Write "×5: a − 6b = 5 − 5b"'),
        'Multiply both sides by five — the denominator is gone.',
        D('Write "a = 5 + b"'),
        "Move the b's across: a equals five plus b.",
        'So a is always exactly five more than b.',
        D('Write "a − b = 5 > 0"'),
        D('Circle choice 4'),
        'b is smaller than a. Choice four.',
        'Choice three, a equals five b, is the trap. The five is added to b — not multiplied.']})

    # Q5. Hebrew 2x + 4y = 17, 5x + 3y = 11 (add -> 7x + 7y); study guide 3x + 7y, 7x + 3y. Now 4x + 9y = 30, 9x + 4y = 35.
    S('q-195', stem='Given:\n' + CASES('4x + 9y = 30', '9x + 4y = 35') + '\n$x + y = ?$',
      choices=['$1$', '$5$', '$13$', '$65$'], correct=2, expl=[
        'Add the two equations: $13x + 13y = 65$.',
        'Divide by $13$: $x + y = 5$ (choice 2).',
        'Choice 1 is $x - y$: subtracting the equations gives $5x - 5y = 5$. Choice 4 forgets to divide by $13$.'])
    video('q-195', {2: [
        "Don't solve for x and y separately. Keep them together.",
        'Look at the coefficients: four and nine, then nine and four. Mirror images.',
        D('Write "13x + 13y = 65" under the equations'),
        'Add the two equations. Four x plus nine x: thirteen x. Nine y plus four y: thirteen y. Thirty plus thirty-five: sixty-five.',
        D('Write "13(x + y) = 65"'),
        "Take out the thirteen — and there's our x plus y.",
        D('Write "x + y = 5" and circle choice 2'),
        'Divide by thirteen: five. Choice two.',
        'Why add? We want x and y with the same coefficient. Adding gave us exactly that.',
        "Subtract instead, and you get x minus y — that's one, choice one. Not what they asked."]})

    # Q6. Hebrew x - y = 4, x^2 + y^2 = 106; study guide 5 and 73. Now x - y = 7, x^2 + y^2 = 85 -> xy = 18 (9 and 2).
    S('q-196', stem='Given:\n' + CASES('x - y = 7', 'x^2 + y^2 = 85') + '\n$xy = ?$',
      choices=['$-18$', '$36$', '$18$', '$39$'], correct=3, expl=[
        'Use the square of a difference: $(x - y)^2 = x^2 + y^2 - 2xy$.',
        'Substitute: $7^2 = 85 - 2xy$, that is, $49 = 85 - 2xy$.',
        'Therefore $2xy = 36$ and $xy = 18$ (choice 3). (Check: $9$ and $2$.)',
        'The traps: $36$ forgets to halve, $39$ forgets to square the $7$, and $-18$ uses the square of a sum.'])
    video('q-196', {2: [
        "We could isolate x and substitute — that's a quadratic and a few minutes.",
        'Instead: x minus y, x squared plus y squared, x times y. Those three pieces belong to one formula.',
        'Which formula has x squared plus y squared AND x minus y? The square of a difference.',
        D('Write "(x − y)² = x² + y² − 2xy"'),
        D('Under it write "7² = 85 − 2xy"'),
        'Put in what we know: x minus y is seven, squared is forty-nine. x squared plus y squared is eighty-five.',
        D('Write "2xy = 36 → xy = 18"'),
        "Eighty-five minus forty-nine: thirty-six. That's two x y. So x y is eighteen.",
        D('Circle choice 3'),
        'Choice three — and we never found x or y.',
        'Quick check: nine and two. Difference seven. Squares: eighty-one plus four — eighty-five. Product: eighteen.',
        'The traps: forget to square the seven, and you get thirty-nine. Forget to halve, and you get thirty-six.']})

    # Q7. Hebrew 2a + 3b + 3c = 22 with a + b, 2b + c, a + c; study guide 23 / 3, 4, 10. Now 3a + 2b + 3c = 24 with
    #     a + b = 4, 2a + c = 7, b + c = 8: (a + b) + (2a + c) + (b + c) + c -> 19 + c = 24 -> c = 5 (a = 1, b = 3).
    S('q-197', stem='Given:\n' + CASES('3a + 2b + 3c = 24', 'a + b = 4', '2a + c = 7', 'b + c = 8') + '\n$c = ?$',
      choices=['$3$', '$5$', '$7$', '$19$'], correct=2, expl=[
        'Split the big left side into the small ones: $3a + 2b + 3c = (a + b) + (2a + c) + (b + c) + c$.',
        'Substitute the values: $4 + 7 + 8 + c = 24$.',
        'Therefore $19 + c = 24$ and $c = 5$ (choice 2).'])
    video('q-197', {2: [
        'Three unknowns, four equations. Solving for every letter would take forever.',
        'Instead, break the big equation into the small ones.',
        D('Under the big equation write "(a + b) + (2a + c) + (b + c) + c"'),
        "Three a, two b, three c: that's a plus b, plus two a plus c, plus b plus c — and one more c.",
        D('Under each bracket write its value: 4, 7, 8'),
        'Now swap in the values: four, seven, eight.',
        D('Write "4 + 7 + 8 + c = 24"'),
        'Four plus seven plus eight plus c equals twenty-four.',
        D('Write "19 + c = 24 → c = 5" and circle choice 2'),
        'Nineteen plus c is twenty-four. c is five. Choice two.',
        'Choice four — nineteen — is what you get if you stop before the last c.']})

    # ================= advanced A
    # Q8 (easy). Hebrew 39 - 3/7 x = 0.5x -> 13/14 x = 39 -> 42 (key 4); study guide 22 - 2/5 x = 1/3 x -> 30.
    #     Now 33 - 2/3 x = 1/4 x -> 11/12 x = 33 -> 36 (keep 33·12, 33 and 11 cancel; estimation: a bit more than 33).
    S('q-184', stem='Given: $33 - \\frac{2}{3}x = \\frac{1}{4}x$. $x = ?$',
      choices=['$36$', '$22$', '$30$', '$48$'], correct=1, expl=[
        'Multiply every term by $12$: $33 \\cdot 12 - 8x = 3x$.',
        'Therefore $11x = 33 \\cdot 12$, and $x = \\frac{33 \\cdot 12}{11} = 3 \\cdot 12 = 36$ (choice 1).',
        'Estimation check: $\\frac{1}{4}x + \\frac{2}{3}x = \\frac{11}{12}x = 33$. Almost all of $x$ equals $33$. Therefore $x$ is a bit more than $33$: $22$ and $30$ are too small, and $48$ is too big ($\\frac{11}{12} \\cdot 48 = 44$).'])
    video('q-184', {
        2: [
            'Fractions of x on both sides. Clear them all at once.',
            'Thirds and quarters — the common denominator is twelve.',
            D('Write "×12" next to each side'),
            "Multiply every term by twelve. But leave thirty-three times twelve as it is — don't work it out yet.",
            D('Write "33·12 − 8x = 3x"'),
            'Two thirds of x, times twelve: eight x. A quarter of x, times twelve: three x.',
            D('Write "33·12 = 11x"'),
            'Move the eight x across: eleven x.',
            D('Cancel 33 with 11 (3 and 1); write "x = 3·12 = 36"'),
            'This is why we waited: thirty-three and eleven cancel. Three times twelve — thirty-six.',
            D('Circle choice 1'),
            'Thirty-six. Choice one.'],
        3: [
            'Or: gather the x terms first.',
            D('Write "33 = 1/4 x + 2/3 x = 11/12 x"'),
            'Move two thirds of x across. A quarter plus two thirds — three twelfths plus eight twelfths: eleven twelfths.',
            "Stop and look. Eleven twelfths of x is thirty-three. That's almost all of x.",
            'So x must be close to thirty-three — and a little MORE than it.',
            D('Cross out choices 2 and 3'),
            "Twenty-two and thirty are smaller than thirty-three. A part of them can't reach thirty-three. Out.",
            D('Next to choice 4 write "too big" and cross it out'),
            'Forty-eight? Eleven twelfths of it is forty-four — too much. We want something just above thirty-three.',
            D('Circle choice 1'),
            'Thirty-six is left. Estimation did the work.',
            D('Write "33 ÷ 11/12 = 33 · 12/11 = 36"'),
            'Want the full math? Dividing by eleven twelfths means multiplying by twelve elevenths. Thirty-three and eleven cancel: thirty-six.',
            'Two good routes — a common denominator, or adding the fractions first. Use whichever feels natural.']})

    # Q9 (medium). Hebrew pi x^2 + x^3 = x^2 -> 1 - pi (key 4); study guide = 2x^2 -> 2 - pi. Now x^3 + 3x^2 = pi x^2 -> pi - 3.
    S('q-185', stem='Given: $x \\ne 0$ and $x^3 + 3x^2 = \\pi x^2$. $x = ?$',
      choices=['$3 - \\pi$', '$\\pi - 3$', '$\\pi$', '$\\frac{\\pi}{3}$'], correct=2, expl=[
        'Every term contains $x^2$, and $x \\ne 0$. Divide every term by $x^2$: $x + 3 = \\pi$.',
        'Therefore $x = \\pi - 3$ (choice 2). Choice 1 has the wrong sign.'])
    video('q-185', {
        2: [
            'Both terms on the left have x squared in them. Take it out.',
            D('Write "x²(x + 3) = πx²"'),
            'x squared times the bracket — x plus three.',
            "x isn't zero, and x squared multiplies both sides. So we may cancel it.",
            D('Cross out x² on both sides; write "x + 3 = π"'),
            'x plus three equals pi.',
            D('Write "x = π − 3" and circle choice 2'),
            'x is pi minus three. Choice two.',
            'Choice one, three minus pi, is the sign trap. Pi is about three point one four — so x is a small positive number.'],
        3: [
            'Shorter: divide EVERY term by x squared straight away.',
            D('Under each term write its result: x, 3, π'),
            'x cubed — x. Three x squared — three. Pi x squared — pi.',
            D('Write "x + 3 = π → x = π − 3"'),
            'Same equation, one step faster. Choice two.',
            "Just remember why it's allowed: x is not zero."]})

    # Q10 (medium). Hebrew x/y = z/w; study guide a/b = c/d. Now p/q = r/s, other choice forms; the false one stays
    #     LAST (the tip "three are gone -> mark the fourth"). Number check 1/2 = 3/6 -> 2/3 = 4/6.
    S('q-186', stem='Given: $p \\ne 0$, $q \\ne 0$, $r \\ne 0$, $s \\ne 0$ and $\\frac{p}{q} = \\frac{r}{s}$. Which of the following statements is not necessarily true?',
      choices=['$s = \\frac{qr}{p}$', '$\\frac{s}{q} = \\frac{r}{p}$', '$q = \\frac{ps}{r}$', '$\\frac{r}{q} = \\frac{s}{p}$'], correct=4, expl=[
        'Cross-multiply the given equation: $ps = qr$.',
        'Choices 1, 2 and 3 each cross-multiply back to $ps = qr$. They are always true.',
        'Choice 4 cross-multiplies to $pr = qs$, which is a different equation.',
        'Counterexample: $p = 1$, $q = 2$, $r = 3$, $s = 6$. Then $\\frac{p}{q} = \\frac{r}{s} = \\frac{1}{2}$, but $\\frac{r}{q} = \\frac{3}{2}$ and $\\frac{s}{p} = 6$.'])
    video('q-186', {
        2: [
            'First, clear the denominators in the given equation.',
            D('Next to the question write "ps = qr"'),
            "Cross-multiply: p s equals q r. That's our reference.",
            "Now do the same to every choice — and look for the one that's different.",
            D('Next to choice 1 write "ps = qr ✓" and cross it out'),
            'Choice one: multiply by p — s p equals q r. Same. Out.',
            D('Next to choice 2 write "ps = qr ✓" and cross it out'),
            'Choice two: cross-multiply — s p equals r q. Same again. Out.',
            D('Next to choice 3 write "ps = qr ✓" and cross it out'),
            'Choice three: multiply by r — q r equals p s. Out.',
            D('Next to choice 4 write "pr = qs ✗" and circle choice 4'),
            "Three are gone — on the exam, mark the fourth and move on. Here, let's check it anyway: p r equals q s. Different. That's the answer."],
        3: [
            'Method one is all you need for the exam. This is a bonus for fast students.',
            'Two tools that make this instant.',
            'Tool one: to isolate a letter, multiply across the diagonal and divide by the one left.',
            D('Next to choices 1 and 3 write "diagonal ÷ leftover ✓"'),
            's equals q r over p. q equals p s over r. Both fine.',
            'Tool two: in a proportion, only DIAGONAL partners can swap places.',
            A('A number check appears: 2/3 = 4/6', T('$\\frac{2}{3}=\\frac{4}{6}$', 52, x=1150, y=330)),
            D('On 2/3 = 4/6, draw arrows linking 2 with 6, and 3 with 4'),
            'Two thirds equals four sixths. Swap the two and the six: six thirds and four halves — two and two. Still equal.',
            'Swap the three and the four: two quarters and three sixths — a half and a half. Diagonal partners can swap.',
            'Choice two swaps p and s — diagonal partners. Fine.',
            D('Circle choice 4'),
            "Choice four moves three letters around — p drops to the bottom, r and s both shift. That's not a diagonal swap. Choice four."]})

    # Q11 (medium). Hebrew/study guide: sum of squares = square of the sum (key 4). Story tweak: square of the
    #     DIFFERENCE = sum of squares -> -2ab = 0 -> one number is 0 (key 2). Same idea: formula, then product = 0.
    S('q-187', stem='The square of the difference of two integers equals the sum of their squares. Which of the following is necessarily true?',
      choices=['The two numbers are equal to each other', 'One of the numbers equals zero',
               'The sum of the numbers equals zero', 'The two numbers are reciprocals of each other'], correct=2, expl=[
        'Call the numbers $a$ and $b$: $(a - b)^2 = a^2 + b^2$, that is, $a^2 - 2ab + b^2 = a^2 + b^2$.',
        'Subtract $a^2 + b^2$ from both sides: $-2ab = 0$, therefore $ab = 0$.',
        'A product is $0$ only when a factor is $0$: $a = 0$ or $b = 0$ (choice 2).'])
    video('q-187', {2: [
        'Two integers. Call them a and b.',
        D('Write "(a − b)²"'),
        'The square of their difference: a minus b, all squared.',
        D('Write "= a² + b²"'),
        'Equals the sum of their squares: a squared plus b squared.',
        D('Expand: write "a² − 2ab + b² = a² + b²"'),
        'The square of a difference: a squared, minus two a b, plus b squared.',
        D('Cross out a² and b² on both sides; write "−2ab = 0"'),
        'The squares cancel. Minus two a b equals zero.',
        'When is a product zero? Only when one of its factors is zero.',
        D('Write "a = 0 or b = 0" and circle choice 2'),
        'So one of the numbers is zero. Choice two.']})

    # Q12 (easy+). Hebrew: add eq1 + eq2 (y cancels), subtract eq3 (z cancels) -> x = 6 (key 2); study guide x = 5.
    #     Now 3x + 2y - z = 12, x - 2y + 4z = 10, 3x + 3z = 18: 4x + 3z = 22, minus 3x + 3z = 18 -> x = 4 (y = 1, z = 2).
    S('q-188', stem='Given:\n' + CASES('3x + 2y - z = 12', 'x - 2y + 4z = 10', '3x + 3z = 18') + '\n$x = ?$',
      choices=['$2$', '$3$', '$4$', '$6$'], correct=3, expl=[
        'Add the first two equations. The $y$ terms cancel: $4x + 3z = 22$.',
        'Subtract the third equation: $(4x + 3z) - (3x + 3z) = 22 - 18$.',
        'Therefore $x = 4$ (choice 3).'])
    video('q-188', {2: [
        "Lots of equations, lots of unknowns — that's a signal. There's almost always a short route.",
        'The clues: what they ask for — and which letters are missing from the answers. And most of these are solved by adding, subtracting, or both.',
        'They only ask for x. So get rid of y and z.',
        'Look at y: plus two y in the first, minus two y in the second.',
        D('Write "eq1 + eq2: 4x + 3z = 22"'),
        "Add them — the y's vanish. Four x plus three z equals twenty-two.",
        'The third equation has three z too: three x plus three z equals eighteen.',
        D('Write "− (3x + 3z = 18)" and "x = 4"'),
        "Subtract — the z's vanish. x equals four.",
        D('Circle choice 3'),
        'Four. Choice three.',
        "No solving for y, no solving for z. Find the shortcut — don't work hard."]})

    # Q13 (hard). Hebrew mixed numbers adding to 6 -> (a+b)/3 (key 3); study guide adding to 4 -> (a+b)/2.
    #     Now 3 1/5 + 4 4/5 = 8 and 5 1/4 + 2 3/4 = 8 -> 8(x + y) = 2(a + b) -> (a + b)/4 (key 1); every choice has a + b.
    S('q-189', stem='Given:\n' + CASES('3\\frac{1}{5}x + 5\\frac{1}{4}y = 2a', '4\\frac{4}{5}x + 2\\frac{3}{4}y = 2b') + '\n$x + y = ?$',
      choices=['$\\frac{a + b}{4}$', '$\\frac{4}{a + b}$', '$\\frac{a + b}{2}$', '$\\frac{a + b}{8}$'], correct=1, expl=[
        'Add the equations. The $x$ coefficients: $3\\frac{1}{5} + 4\\frac{4}{5} = 8$. The $y$ coefficients: $5\\frac{1}{4} + 2\\frac{3}{4} = 8$.',
        'Therefore $8x + 8y = 2a + 2b$, that is, $8(x + y) = 2(a + b)$.',
        'Divide by $8$: $x + y = \\frac{2(a + b)}{8} = \\frac{a + b}{4}$ (choice 1).'])
    video('q-189', {2: [
        'Two equations, four letters — and they want x plus y.',
        'To get x plus y, we need x and y with the SAME coefficient.',
        A('A quick example appears: x + 3y = 12 vs 3x + 3y = 12', T('$x+3y=12\\ \\ ✗ \\qquad 3x+3y=12\\ \\ ✓$', 38)),
        "Look: x plus three y equals twelve — no way to get x plus y. But three x plus three y equals twelve? Divide by three: x plus y is four. We still don't know x or y — but we know their sum.",
        'Clue from the choices: every one has a plus b. So — add the equations.',
        D('Write "3⅕ + 4⅘ = 8" under the x terms'),
        'The x coefficients: three and a fifth plus four and four fifths. Eight.',
        D('Write "5¼ + 2¾ = 8" under the y terms'),
        'The y coefficients: five and a quarter plus two and three quarters. Eight again.',
        D('Write "8x + 8y = 2a + 2b"'),
        'Eight x plus eight y equals two a plus two b.',
        D('Write "8(x + y) = 2(a + b) → x + y = (a + b)/4"'),
        'Take out the eight and the two. Then divide by eight: two eighths is a quarter. x plus y is a plus b, over four.',
        D('Circle choice 1'),
        "Choice one. Solve for x and y separately? You'd burn precious minutes."]})

    # Q14 (hard). Hebrew a + b + c = x, a + 2b + 4c = z, 3a + 2b = 4x - z (key 4); study guide 4a + 2b = 5x - z.
    #     Now a + b + c = x, 3a + 2b + 4c = z, a + 2b = 4x - z (key 2). Plug-in with ones: x = 3, z = 9, target 3;
    #     the three wrong choices are negative (-33, -3, -9) - the Hebrew "kill by sign" still works.
    S('q-190', stem='Given:\n' + CASES('a + b + c = x', '3a + 2b + 4c = z') + '\n$a + 2b = ?$',
      choices=['$x - 4z$', '$4x - z$', '$z - 4x$', '$3x - 2z$'], correct=2, expl=[
        'The answers have no $c$. Make $c$ cancel: multiply the first equation by $4$: $4a + 4b + 4c = 4x$.',
        'Subtract the second equation: $(4a + 4b + 4c) - (3a + 2b + 4c) = 4x - z$.',
        'Therefore $a + 2b = 4x - z$ (choice 2).',
        'Plug-in check: $a = b = c = 1$ gives $x = 3$, $z = 9$ and $a + 2b = 3$. The choices give $-33$, $3$, $-3$ and $-9$. Only choice 2 gives $3$.'])
    video('q-190', {
        2: [
            "Clues: they ask about a and b. The answers use x and z. And c? It's gone.",
            'So our job is to make c disappear.',
            'The first equation has one c, the second has four. Multiply the first by four.',
            D('Write "4a + 4b + 4c = 4x"'),
            'Four a plus four b plus four c equals four x.',
            D('Subtract the second equation; write "a + 2b = 4x − z"'),
            "Now subtract the second. The c's cancel. Four a minus three a — a. Four b minus two b — two b.",
            'Exactly the expression they asked for: four x minus z.',
            D('Circle choice 2'),
            'Choice two.',
            'Choice three, z minus four x, is the same subtraction done the wrong way round.'],
        3: [
            'Lots of letters? Plug in numbers. Make a, b and c all one.',
            D('Write "a = b = c = 1 → x = 3, z = 9"'),
            'One plus one plus one: x is three. Three plus two plus four: z is nine.',
            D('Write "a + 2b = 3"'),
            "The target: one plus two — three. We're hunting for three.",
            D('Next to the choices write: negative, 3, negative, negative'),
            'Choice one: three minus thirty-six — negative. Choice three: nine minus twelve — negative. Choice four: nine minus eighteen — negative.',
            'We used ones — usually risky. Here the four choices still came out different. So it works.',
            D('Circle choice 2'),
            'Only choice two can make three: twelve minus nine. Choice two.',
            'Two approaches — the math and the plug-in. In this question, both are excellent.']})

    # ================= advanced B
    # Q15 (medium). Hebrew difference 3, squares 51 -> 17 (key 2); study guide 4, 72 -> 18. Now 5, 65 -> 13 (9 and 4, key 3).
    S('q-178', stem='The difference between two integers is 5. The difference between the squares of the numbers is 65. What is their sum?',
      choices=['$11$', '$15$', '$13$', '$17$'], correct=3, expl=[
        'Call the numbers $a$ and $b$: $a - b = 5$ and $a^2 - b^2 = 65$.',
        'Difference of squares: $a^2 - b^2 = (a - b)(a + b)$. Therefore $5(a + b) = 65$.',
        'Divide by $5$: $a + b = 13$ (choice 3). (Check: $9$ and $4$ give $81 - 16 = 65$.)'])
    video('q-178', {
        2: [
            'Translate. Call the numbers a and b.',
            D('Write "a − b = 5" and "a² − b² = 65"'),
            'Their difference is five. The difference of their squares is sixty-five.',
            'That second one is the difference of squares: a squared minus b squared equals a minus b, times a plus b.',
            D('Write "(a − b)(a + b) = 65"'),
            'a minus b, times a plus b.',
            D('Replace (a − b) with 5: write "5(a + b) = 65"'),
            'And we know a minus b is five.',
            D('Write "a + b = 13" and circle choice 3'),
            'Divide by five: the sum is thirteen. Choice three.'],
        3: [
            'Or hunt for the numbers. Two integers, five apart.',
            'Where to start? Six and one: thirty-six minus one — thirty-five. Too small. We need bigger squares.',
            D('Write "7, 2 → 49 − 4 = 45"'),
            'Seven and two: forty-nine minus four — forty-five. Still too small.',
            D('Write "8, 3 → 64 − 9 = 55"'),
            'Eight and three: fifty-five. Closer — each step adds ten.',
            D('Write "9, 4 → 81 − 16 = 65 ✓"'),
            'Nine and four: sixty-five. There it is.',
            D('Circle choice 3'),
            'Nine plus four — thirteen. Choice three.',
            "Both routes work. I'd pick the formula — but the plug-in is great too."],
        4: [
            'You can also plug in using the answers.',
            D('Next to choice 1 write "11 → 8, 3: 64 − 9 = 55 ✗"'),
            'A sum of eleven and a difference of five: take away five, halve it — three and eight. Squares: fifty-five. Not sixty-five.',
            D('Next to choice 2 write "15 → 10, 5: 100 − 25 = 75 ✗"'),
            'Fifteen: ten and five — seventy-five. Too big. So the sum is between eleven and fifteen.',
            D('Next to choice 3 write "13 → 9, 4: 81 − 16 = 65 ✓"'),
            'Thirteen: thirteen minus five is eight, halve it — four and nine. Sixty-five!',
            D('Circle choice 3'),
            'Choice three, a third way.']})

    # Q16 (medium+). Hebrew 3, 5, 4 -> 60 (key 3); study guide 2, 6, 3 -> 36. Now 3, 4, 2 -> 24 (key 2).
    #     Choices: as in the Hebrew, only ONE choice is > 1, so "x/w > 1" alone finds it (review 2026-10-02: 9 -> 1/9).
    S('q-179', stem='Given: $x, y, z, w \\ne 0$ and\n' + CASES('\\frac{x}{y} = 3', '\\frac{y}{z} = 4', '\\frac{z}{w} = 2') + '\n$\\frac{x}{w} = ?$',
      choices=['$\\frac{1}{24}$', '$24$', '$\\frac{3}{8}$', '$\\frac{1}{9}$'], correct=2, expl=[
        'Multiply the three equations: $\\frac{x}{y} \\cdot \\frac{y}{z} \\cdot \\frac{z}{w} = 3 \\cdot 4 \\cdot 2$.',
        'The $y$ and the $z$ cancel: $\\frac{x}{w} = 24$ (choice 2).',
        'Quick check: all three ratios are bigger than $1$, so $\\frac{x}{w}$ is bigger than $1$. Only choice 2 is bigger than $1$.'])
    video('q-179', {
        2: [
            'Write each letter in terms of the next one.',
            D('Write "x = 3y"'),
            'x over y is three. So x is three y.',
            D('Write "y = 4z → x = 12z"'),
            'y is four z. So x is twelve z.',
            D('Write "z = 2w → x = 24w"'),
            'z is two w. So x is twenty-four w.',
            D('Write "x/w = 24" and circle choice 2'),
            'x over w: twenty-four. Choice two.'],
        3: [
            'Plug in. Start at the end: w equals one.',
            D('Write "w = 1 → z = 2 → y = 8 → x = 24"'),
            'z over w is two. So z is two. y is four times that — eight. x is three times that — twenty-four.',
            D('Circle choice 2'),
            'Twenty-four over one. Choice two.'],
        4: [
            "Brainwave one: you're allowed to MULTIPLY equations.",
            D('Write "(x/y)·(y/z)·(z/w) = x/w" and cancel y and z'),
            "Multiply the three ratios. The y's cancel, the z's cancel. What's left: x over w.",
            D('Write "= 3 · 4 · 2 = 24"'),
            'Three times four times two: twenty-four. One line.',
            'Brainwave two: all three ratios are bigger than one. Multiply numbers bigger than one, and the result is bigger than one. So x over w is bigger than one.',
            D('Cross out choices 1, 3 and 4; circle choice 2'),
            'That kills one twenty-fourth, three eighths and one ninth straight away. Only one choice is bigger than one: choice two.',
            "A wide range of routes — and honestly, they're all excellent. Whichever one you found is a great way."]})

    # Q17 (medium+). Hebrew ab = 1, a/b = a^2 (key 4); study guide mn = 1, m/n. Now pq = 1, q/p = 1/p^2 (key 2).
    #     Plug-in trap kept: p = q = 1 makes every choice 1; p = 2, q = 1/2 gives 4, 1/4, 1/2, 2.
    S('q-180', stem='Given: $p \\ne 0$, $q \\ne 0$ and $pq = 1$. $\\frac{q}{p} = ?$',
      choices=['$p^2$', '$\\frac{1}{p^2}$', '$\\frac{1}{p}$', '$p$'], correct=2, expl=[
        'From $pq = 1$: $q = \\frac{1}{p}$.',
        'Therefore $\\frac{q}{p} = \\frac{1}{p} \\div p = \\frac{1}{p} \\cdot \\frac{1}{p} = \\frac{1}{p^2}$ (choice 2).',
        'Plug-in check: $p = 2$, $q = \\frac{1}{2}$. Then $\\frac{q}{p} = \\frac{1}{4} = \\frac{1}{p^2}$. (Do not use $p = q = 1$: then every choice equals $1$.)'])
    video('q-180', {
        1: ['Question seventeen.', 'One equation, two unknowns — and every answer is written with p.'],
        2: ('Method 1 · Write q with p', [
            "One equation, two unknowns — we can't find them. But we can write one using the other.",
            'The answers only use p. So get rid of q.',
            D('Write "q = 1/p"'),
            'p times q is one — so q is one over p.',
            D('Write "q/p = (1/p) ÷ p = (1/p) · (1/p) = 1/p²"'),
            'One over p, divided by p: multiply by the reciprocal — one over p, times one over p.',
            D('Circle choice 2'),
            'One over p squared. Choice two.',
            "Choice one, p squared, is the upside-down trap — that's p over q."]),
        3: [
            'Careful with the plug-in here. p and q both equal to one works — but then EVERY choice is one.',
            'We need values whose product is one — without being one. Take p equals two, q equals one half.',
            D('Next to the choices write their values: 4, 1/4, 1/2, 2'),
            'Four, a quarter, a half, two. All different. One substitution is enough.',
            D('Write "q/p = 1/2 ÷ 2 = 1/4"'),
            'A half divided by two: a quarter.',
            D('Circle choice 2'),
            'A quarter — choice two.',
            "Two routes. Here the math was short. So it's the better choice — but plugging in is perfectly fine too."]})

    # Q18 (hard). Hebrew 3x = 2y + 1, 4.5x^2 - 2y^2 = 2y + 1/2 (key 2); study guide 2x = 3y + 1. Now 2x = y + 3,
    #     2x^2 - 1/2 y^2 = 3y + 4.5 (key 4). Trap kept: (y + 3)^2 is not y^2 + 9 (that gives choice 1, 4.5).
    #     Plug-in y = 1, x = 2: choices 4.5, 7, 15, 7.5 - all different; the target is 7.5.
    S('q-181', stem='Given: $2x = y + 3$. $2x^2 - \\frac{1}{2}y^2 = ?$',
      choices=['$4.5$', '$2x + 3y$', '$6y + 9$', '$3y + 4.5$'], correct=4, expl=[
        'Square both sides: $(2x)^2 = (y + 3)^2$, that is, $4x^2 = y^2 + 6y + 9$.',
        'Move $y^2$ to the left: $4x^2 - y^2 = 6y + 9$.',
        'Divide by $2$: $2x^2 - \\frac{1}{2}y^2 = 3y + 4.5$ (choice 4).',
        'Plug-in check: $y = 1$, $x = 2$. The expression is $8 - 0.5 = 7.5$, and choice 4 gives $3 + 4.5 = 7.5$. The other choices give $4.5$, $7$ and $15$.'])
    video('q-181', {
        2: [
            "One equation, two unknowns. And the answers mix x and y — so isolating one letter won't help.",
            "If the answers had only x, we'd isolate y and substitute. Only y? Isolate x. But with both — we don't know which route, and the wrong one burns time.",
            "So use the clue in the question. They want x squared and y squared. The given equation has no squares.",
            'So — square both sides.',
            D('Write "(2x)² = (y + 3)²"'),
            'Careful on the right. Many students write y squared plus nine — wrong. The WHOLE y plus three gets squared — the square of a sum.',
            D('Write "4x² = y² + 6y + 9"'),
            'Four x squared equals y squared, plus six y, plus nine.',
            D('Write "4x² − y² = 6y + 9"'),
            "Move the y squared across. That's exactly double what they asked for.",
            D('Divide by 2: write "2x² − ½y² = 3y + 4.5"'),
            'Divide by two: three y plus four and a half.',
            D('Circle choice 4'),
            'Choice four.',
            'Choice one, four and a half, is what the wrong square gives — it loses the six y.'],
        3: [
            'Plug-in is easier here. Find x and y that fit the equation.',
            D('Write "y = 1 → 2x = 4 → x = 2"'),
            'y equals one: two x is four. So x is two.',
            D('Next to the choices write their values: 4.5, 7, 15, 7.5'),
            'Check the choices are all different: four and a half, seven, fifteen, seven and a half. Good.',
            D('Write "2·4 − ½·1 = 7.5"'),
            'The expression: two times four, minus a half — seven and a half.',
            D('Circle choice 4'),
            'Choice four. For most students, this route is the one to pick.']})

    # Q19 (hard). Hebrew x^2 + y^2 - 2xy -> |a - b| = 2 (key 2); study guide 4x^2 + 9y^2 - 12xy -> 5.
    #     Now 9x^2 + y^2 - 6xy: a = ±3, b = ±1, ab = -3 -> |a - b| = 4 (key 3); trap 2 = same signs.
    S('q-182', stem='Given: for every $x$ and $y$, $(ax + by)^2 = 9x^2 + y^2 - 6xy$. $|a - b| = ?$',
      choices=['$2$', '$0$', '$4$', '$3$'], correct=3, expl=[
        'Expand the left side: $a^2x^2 + 2abxy + b^2y^2$.',
        'The two sides are equal for every $x$ and $y$. Therefore the coefficients match: $a^2 = 9$, $b^2 = 1$ and $2ab = -6$.',
        'Therefore $a = \\pm 3$, $b = \\pm 1$ and $ab = -3$ (opposite signs): $(a, b) = (3, -1)$ or $(-3, 1)$.',
        'In both cases $|a - b| = 4$ (choice 3). Choice 1 ($2$) forgets that the signs are opposite.'])
    video('q-182', {
        2: [
            'Expand the left side with the square of a sum.',
            D('Write "a²x² + 2abxy + b²y²"'),
            'a squared x squared, plus two a b x y, plus b squared y squared.',
            'It equals the right side for every x and y. So matching terms need matching coefficients.',
            D('Write "a² = 9 → a = ±3"'),
            'x squared: a squared is nine. a is three or negative three.',
            D('Write "b² = 1 → b = ±1"'),
            'y squared: b squared is one. b is one or negative one.',
            D('Write "2ab = −6 → ab = −3"'),
            'x y: two a b is negative six. So a b is negative three — opposite signs.',
            D('Write "(3, −1) or (−3, 1) → |a − b| = 4"'),
            'Three and negative one, or negative three and one. Either way, the gap is four.',
            D('Circle choice 3'),
            'Choice three.',
            'Choice one, two, is the trap: three minus one. It forgets that the signs must be opposite.'],
        3: [
            'Shortcut: the right side IS the square of a difference.',
            D('Write "9x² − 6xy + y² = (3x − y)²"'),
            'Nine x squared, minus six x y, plus y squared: three x minus y, squared.',
            D('Write "a = 3, b = −1 → |3 − (−1)| = 4"'),
            'So a is three, b is negative one. Three minus negative one — four.',
            D('Circle choice 3'),
            'Choice three. The full method matters, though — some coefficient questions hide a second option you must not miss.']})

    # Q20 (hard). Hebrew a^2 + b^2 = 0.5 b^2 -> a = 0; study guide 1/3 b^2. Now a^2 + 2b^2 = 1/4 a^2 -> 3a^2 + 8b^2 = 0
    #     -> b = 0 (key 1). Same trap: "cannot be determined" (choice 4).
    S('q-183', stem='Given: $a^2 + 2b^2 = \\frac{1}{4}a^2$. $b = ?$',
      choices=['$0$', '$2$', '$4$', NOTDET], correct=1, expl=[
        'Multiply by $4$: $4a^2 + 8b^2 = a^2$, therefore $3a^2 + 8b^2 = 0$.',
        'A square is never negative: $3a^2 \\ge 0$ and $8b^2 \\ge 0$. Their sum is $0$ only if both are $0$.',
        'Therefore $b = 0$ (and $a = 0$). The answer is choice 1.',
        'Why not "cannot be determined"? Every case that fits the equation gives the same value, $b = 0$.'])
    video('q-183', {2: [
        'First, clear the fraction. Multiply everything by four.',
        D('Write "4a² + 8b² = a²"'),
        'Four a squared plus eight b squared equals a squared.',
        D('Write "3a² + 8b² = 0"'),
        'Move a squared across: three a squared plus eight b squared equals zero.',
        "Looks strange. You might want to say: impossible — or 'can't be determined.'",
        'Not so fast. A square is never negative… but it CAN be zero.',
        D('Under the terms write "≥ 0" and "≥ 0"'),
        'Something at least zero, plus something at least zero, equals zero. The only way: both are zero.',
        D('Write "a = 0, b = 0" and circle choice 1'),
        'So b is zero. Choice one.',
        'Why not choice four? It cannot be determined means different cases give different values of b.',
        'Here every case gives the same value: b equals zero. So it IS determined.',
        'An understanding question — not a technical one.']})

    # ================= self-practice from the Hebrew study guide (q-198 .. q-217): new numbers, same idea
    S('q-198', stem='Given:\n' + CASES('x + y = 7', 'x^2 + y^2 = 49') + '\n$xy = ?$',
      choices=['$7$', '$24.5$', '$49$', '$0$'], correct=4, expl=[
        'Square the sum: $(x + y)^2 = x^2 + y^2 + 2xy$.',
        'Substitute: $49 = 49 + 2xy$. Therefore $2xy = 0$ and $xy = 0$ (choice 4).'])
    S('q-199', stem='Given: $x \\ne 0$ and $\\frac{x}{x + y} = 4x$. $x + y = ?$',
      choices=['$\\frac{1}{8}$', '$\\frac{1}{2}$', '$\\frac{1}{4}$', '$4$'], correct=3, expl=[
        'Divide both sides by $x$ (allowed, since $x \\ne 0$): $\\frac{1}{x + y} = 4$.',
        'Therefore $x + y = \\frac{1}{4}$ (choice 3).'])
    S('q-200', stem='Given:\n' + CASES('x + y + z = 8', 'y + z = 11', 'y + z + w = -3') + '\n$x + y + z + w = ?$',
      choices=['$5$', '$-14$', '$6$', '$-6$'], correct=4, expl=[
        'Subtract the second equation from the third: $w = -3 - 11 = -14$.',
        'Therefore $x + y + z + w = (x + y + z) + w = 8 + (-14) = -6$ (choice 4).'])
    S('q-201', stem='Given: $x \\ne 0$, $y \\ne -2$ and $\\frac{x}{y + 2} = \\frac{4}{x}$. $y = ?$',
      choices=['$\\frac{x^2}{4} - 2$', '$\\frac{x^2}{4} - \\frac{1}{2}$', '$\\frac{x^2}{2}$', '$2$'], correct=1, expl=[
        'Cross-multiply: $x^2 = 4(y + 2) = 4y + 8$.',
        'Therefore $4y = x^2 - 8$ and $y = \\frac{x^2}{4} - 2$ (choice 1).'])
    S('q-202', stem='Given: $m^2 + n^2 = (m + n)^2$ and $m \\ne 0$. Which of the following is necessarily true?',
      choices=['$m = 3n$', '$n = m - 2$', '$m = 5$', '$n = 0$'], correct=4, expl=[
        'Expand: $(m + n)^2 = m^2 + 2mn + n^2$.',
        'Cancel $m^2 + n^2$ on both sides: $0 = 2mn$, therefore $mn = 0$.',
        'Since $m \\ne 0$, $n = 0$ (choice 4).'])
    S('q-203', stem='Given: $a > 0$, $b > 0$ and $\\frac{(a + b)^2 + (a - b)^2}{2} = 5b^2$. $a = ?$',
      choices=['$b$', '$4b$', '$2b$', '$b^2 - 2$'], correct=3, expl=[
        'Expand: $(a + b)^2 + (a - b)^2 = 2a^2 + 2b^2$ (the $2ab$ terms cancel).',
        'Half of it: $a^2 + b^2 = 5b^2$, therefore $a^2 = 4b^2$.',
        'Then $a = 2b$ or $a = -2b$. Both numbers are positive. Therefore $a = 2b$ (choice 3).'])
    S('q-204', stem='Given: $x > 0$, $a > 0$ and $\\frac{9a}{x + 4} = \\frac{a}{x}$. $x = ?$',
      choices=['$4a$', '$\\frac{1}{2}$', '$2$', '$\\frac{1}{4a}$'], correct=2, expl=[
        'Cross-multiply: $9ax = a(x + 4)$.',
        'Divide by $a$ (allowed, since $a > 0$): $9x = x + 4$.',
        'Therefore $8x = 4$ and $x = \\frac{1}{2}$ (choice 2).'])
    S('q-205', stem='Given: $m$ and $n$ are numbers. The equation $mx + n = 0$ (the unknown is $x$) has no solution. Which of the following is necessarily true?',
      choices=['$m \\ne 0$ and $n = 0$', '$m = 1$ and $n = 0$', '$m = 0$ and $n \\ne 0$', '$m = 1$ and $n \\ne 0$'], correct=3, expl=[
        'If $m \\ne 0$, then $x = -\\frac{n}{m}$ is a solution. Therefore $m = 0$.',
        'With $m = 0$ the equation reads $n = 0$. For no solution, this must be false: $n \\ne 0$ (choice 3).'])
    S('q-206', stem='Given: $y \\ne 0$ and\n' + CASES('k = x - \\frac{y}{3}', 'x + 2y = 3k') + '\n$\\frac{x}{y} = ?$',
      choices=['$1$', '$\\frac{2}{3}$', '$\\frac{3}{2}$', '$3$'], correct=3, expl=[
        'Multiply the first equation by $3$: $3k = 3x - y$.',
        'The second equation says $3k = x + 2y$. Therefore $3x - y = x + 2y$, and $2x = 3y$.',
        'Therefore $\\frac{x}{y} = \\frac{3}{2}$ (choice 3).'])
    S('q-207', stem='Given: for every $x$ and $y$, $(ax + 2y)(x + by) = x^2 - 4y^2$. $a - b = ?$',
      choices=['$-1$', '$0$', '$1$', '$3$'], correct=4, expl=[
        'Expand: $(ax + 2y)(x + by) = ax^2 + (ab + 2)xy + 2by^2$.',
        'Match the coefficients with $x^2 - 4y^2$: $a = 1$ and $2b = -4$, so $b = -2$. Check the $xy$ term: $ab + 2 = -2 + 2 = 0$ ✓.',
        'Therefore $a - b = 1 - (-2) = 3$ (choice 4).'])
    S('q-208', stem='Given:\n' + CASES('x = 2y = 4z = 5w', 'x + y = z + w') + '\n$w = ?$',
      choices=['$\\frac{1}{10}$', '$1$', '$\\frac{2}{5}$', '$0$'], correct=4, expl=[
        'Call the common value $k$: $x = k$, $y = \\frac{k}{2}$, $z = \\frac{k}{4}$, $w = \\frac{k}{5}$.',
        'Then $x + y = z + w$ reads $k + \\frac{k}{2} = \\frac{k}{4} + \\frac{k}{5}$, that is, $\\frac{3}{2}k = \\frac{9}{20}k$.',
        'Multiply by $20$: $30k = 9k$. Therefore $21k = 0$ and $k = 0$.',
        'Therefore $w = \\frac{k}{5} = 0$ (choice 4).'])
    S('q-209', stem='Given:\n' + CASES('x^2 - y^2 = 0', 'x - y = 5') + '\n$x = ?$',
      choices=['$5$', '$-\\frac{5}{2}$', '$-5$', '$\\frac{5}{2}$'], correct=4, expl=[
        'Factor: $x^2 - y^2 = (x - y)(x + y) = 0$.',
        'Since $x - y = 5 \\ne 0$, the other factor is $0$: $x + y = 0$.',
        'Add $x - y = 5$ and $x + y = 0$: $2x = 5$. Therefore $x = \\frac{5}{2}$ (choice 4).'])
    S('q-210', stem='Given: $x \\ne 0$ and $2x^2 + x^3 = kx^2$. $x = ?$',
      choices=['$k - 2$', '$\\sqrt{k}$', '$k + 2$', '$k^2$'], correct=1, expl=[
        'Divide every term by $x^2$ (allowed, since $x \\ne 0$): $2 + x = k$.',
        'Therefore $x = k - 2$ (choice 1).'])
    S('q-211', stem='Given: $x > 0$ and $x^3 = 7x$. $x = ?$',
      choices=['$7$', '$-\\sqrt{7}$', '$\\sqrt[3]{7}$', '$\\sqrt{7}$'], correct=4, expl=[
        'Divide by $x$ (allowed, since $x > 0$): $x^2 = 7$.',
        'Therefore $x = \\sqrt{7}$ or $x = -\\sqrt{7}$. Since $x > 0$, $x = \\sqrt{7}$ (choice 4).'])
    S('q-212', stem='Given:\n' + CASES('6x + 5y = a', '5x + 6y = c') + '\n$x + y = ?$',
      choices=['$\\frac{11}{a + c}$', '$\\frac{a + c}{11}$', '$\\frac{a - c}{11}$', '$a + c - 11$'], correct=2, expl=[
        'Add the equations: $11x + 11y = a + c$.',
        'Divide by $11$: $x + y = \\frac{a + c}{11}$ (choice 2).'])
    S('q-213', stem='Given:\n' + CASES('m + n = k', 'm + k = n') + '\nHow many different values can $m$ take?',
      choices=['$2$', '$1$', '$3$', '$m$ cannot take any value.'], correct=2, expl=[
        'Add the two equations: $2m + n + k = n + k$. Therefore $2m = 0$ and $m = 0$.',
        'For example, $n = k = 5$ fits both equations with $m = 0$. Therefore $m$ takes exactly one value: $0$ (choice 2).'])
    S('q-214', stem='Given: $3x + 2y = 12$. Which of the following is necessarily true?',
      choices=['$x < y$', '$x < 0$ or $y < 0$ (or both)', '$x > 2$ or $y > 2$ (or both)', '$x < 12$'], correct=3, expl=[
        'Suppose choice 3 is false: $x \\le 2$ and $y \\le 2$.',
        'Then $3x + 2y \\le 6 + 4 = 10 < 12$. This contradicts $3x + 2y = 12$. Therefore choice 3 is always true.',
        'The others can fail: $x = y = 2.4$ breaks choices 1 and 2, and $x = 100$, $y = -144$ breaks choice 4.'])
    S('q-215', stem='Given: $(a + 5)(a - 5) - (b + 5)(b - 5) = a^2 - b^2$. Which of the following pairs of numbers cannot be the pair $(a, b)$?',
      choices=['$(3, -3)$', '$(0, 6)$', '$(2, 7)$', 'Any pair of numbers can be $(a, b)$.'], correct=4, expl=[
        '$(a + 5)(a - 5) = a^2 - 25$ and $(b + 5)(b - 5) = b^2 - 25$.',
        'The left side is $(a^2 - 25) - (b^2 - 25) = a^2 - b^2$, exactly the right side.',
        'The equation is true for every $a$ and $b$. No pair is excluded (choice 4).'])
    S('q-216', stem='Given: the ratio $A : B$ equals the ratio $B : C$. The ratio $A : C$ equals —',
      choices=['$B^2 : C^2$', '$1 : 1$', '$C : A$', '$B : C^2$'], correct=1, expl=[
        'Write the ratios as fractions: $\\frac{A}{B} = \\frac{B}{C}$.',
        'Cross-multiply: $AC = B^2$. Therefore $A = \\frac{B^2}{C}$.',
        'Then $\\frac{A}{C} = \\frac{B^2}{C^2}$, that is, the ratio $A : C$ equals the ratio $B^2 : C^2$ (choice 1).'])
    S('q-217', stem='Given: $k \\ne 0$, $t \\ne 0$, $t \\ne 2$ and\n' + CASES('x = \\frac{2}{k} - \\frac{t}{k}', 'y = x + 2 - t') + '\n$\\frac{y}{x} = ?$',
      choices=['$\\frac{1 + k}{t}$', '$1 + k$', '$1 - k$', '$\\frac{1 - k}{t}$'], correct=2, expl=[
        'Write $x$ as one fraction: $x = \\frac{2 - t}{k}$. Therefore $2 - t = xk$.',
        'Substitute into $y$: $y = x + xk = x(1 + k)$.',
        'Since $t \\ne 2$, $x \\ne 0$. Divide: $\\frac{y}{x} = 1 + k$ (choice 2).'])

    # ================= study-guide variants of the theory questions (q-172 .. q-177): new numbers, not equal to Q1-Q6
    S('q-172', stem='Given: $a^4 = a^3 b$. $b = ?$', choices=['$a^3$', '$a$', '$0$', NOTDET], correct=4, expl=[
        'If $a \\ne 0$, divide both sides by $a^3$: $b = a$.',
        'But if $a = 0$, the equation reads $0 = 0$, which is true for every $b$.',
        'Different cases give different values of $b$. Therefore $b$ cannot be determined (choice 4).'])
    S('q-173', stem='Given: $x^3 - 16x = 0$. The number of solutions of the given equation is —',
      choices=['$3$', '$2$', '$1$', '$4$'], correct=1, expl=[
        'Take out the common factor: $x(x^2 - 16) = 0$.',
        '$x = 0$, or $x^2 = 16$, which gives $x = 4$ or $x = -4$.',
        'Three different solutions: $0$, $4$ and $-4$ (choice 1).'])
    S('q-174', stem='Given: $(x - 3)^2 = 64$. How many different values can $x$ take?',
      choices=['$2$', '$1$', '$0$', '$3$'], correct=1, expl=[
        'Something squared is $64$. Therefore $x - 3 = 8$ or $x - 3 = -8$.',
        'Therefore $x = 11$ or $x = -5$: two different values (choice 1).'])
    S('q-175', stem='Given: $\\frac{b - 4a}{3} = 2 - a$. Which of the following statements is necessarily true?',
      choices=['$a < b$', '$b < a$', '$a = b$', '$b = 3a$'], correct=1, expl=[
        'Multiply both sides by $3$: $b - 4a = 6 - 3a$.',
        'Add $4a$ to both sides: $b = a + 6$.',
        'Therefore $b$ is always $6$ more than $a$, and $a < b$ in every case (choice 1).'])
    S('q-176', stem='Given:\n' + CASES('2x + 5y = 23', '5x + 2y = 26') + '\n$x + y = ?$',
      choices=['$1$', '$49$', '$7$', '$14$'], correct=3, expl=[
        'Add the equations: $7x + 7y = 49$.', 'Divide by $7$: $x + y = 7$ (choice 3).'])
    S('q-177', stem='Given:\n' + CASES('x - y = 2', 'x^2 + y^2 = 34') + '\n$xy = ?$',
      choices=['$30$', '$-15$', '$17$', '$15$'], correct=4, expl=[
        'Use the square of a difference: $(x - y)^2 = x^2 + y^2 - 2xy$.',
        'Substitute: $4 = 34 - 2xy$. Therefore $2xy = 30$ and $xy = 15$ (choice 4).'])


# ======================================================================================================
# 2026-10-02 order changes (less like a copy of the Hebrew course; only where nothing is lost)
# Spoken "Question N" lines use the numbers from before renumbering; renumber_guided maps them to the new order.
# ======================================================================================================
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
    RECORDED = set()   # nothing in topic 7 is recorded yet (2026-10-02)
    L = 'equation-strategy'
    # (1) Lesson: "Break it apart" (combining equations) now comes right after "Which operation?", and the hidden
    #     multiplication formula follows it, just before "Plug in numbers". Guided Q6/Q7 swap with it.
    if not RECORDED & {'equation-strategy', 'q-196', 'q-197'}:
        assert M.slide(L, 8)['title'] == 'Hidden formula' and M.slide(L, 9)['title'] == 'Break it apart'
        _sub(M, L, 9, [('The last type: lots of equations that look scary.', 'Another type: lots of equations that look scary.')])
        _swap_slides(M, L, 8, 9)
        M.move('q-197', 'equation-theory', before='q-196'); M.move('solve-q-197', 'equation-theory', after='q-197')
        _sub(M, 'solve-q-197', 1, [('Last question of the set.', 'Question seven.')])
        _sub(M, 'solve-q-196', 1, [('Question six.', 'Last question of the set.')])
    # (2) Advanced A: two medium-level questions swap - the word problem (product = 0) right after the x^2-cancel
    #     question, then the proportion question.
    if not RECORDED & {'q-186', 'q-187'}:
        sec = M.section_of('q-186')
        M.move('q-187', sec, before='q-186'); M.move('solve-q-187', sec, after='q-187')


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
    # 1) Lesson "r26-t07-more-tools" slide 3 used x + 1/x = 3, the same as q-r26-t04-04 (solution video RECORDED) and
    #    q-r26-t07-02. The lesson example becomes x + 1/x = 5, the topic-7 question x + 1/x = 6 (q-r26-t04-10 uses 4).
    _dd_sub(M, 'r26-t07-more-tools', 3, [
        (r'$x+\frac{1}{x}=3 \;\to\; 9=x^2+\frac{1}{x^2}+2 \;\to\; x^2+\frac{1}{x^2}=7$',
         r'$x+\frac{1}{x}=5 \;\to\; 25=x^2+\frac{1}{x^2}+2 \;\to\; x^2+\frac{1}{x^2}=23$'),
        ('Example x + 1/x = 3 appears', 'Example x + 1/x = 5 appears'),
        ('Example: x plus one over x is three. Square both sides: nine. Take away two: x squared plus one over x squared is seven.',
         'Example: x plus one over x is five. Square both sides: twenty-five. Take away two: x squared plus one over x squared is twenty-three.')])
    M.set_q('q-r26-t07-02', stem=r'Given: $x + \frac{1}{x} = 6$.' + '\n' + r'$x^2 + \frac{1}{x^2} = ?$',
            choices=['$36$', '$34$', '$38$', '$32$'], correct=2,
            expl=[r'Square both sides: $\left(x + \frac{1}{x}\right)^2 = 36$.',
                  r'Expand: $x^2 + 2 \cdot x \cdot \frac{1}{x} + \frac{1}{x^2} = x^2 + 2 + \frac{1}{x^2}$. The middle term is just $2$.',
                  r'Therefore $x^2 + \frac{1}{x^2} + 2 = 36$, and $x^2 + \frac{1}{x^2} = 34$.'])
    _dd_sub(M, 'solve-q-r26-t07-02', 2, [
        ('Write "(x + 1/x)² = 3² = 9"', 'Write "(x + 1/x)² = 6² = 36"'),
        ('x plus one over x, squared — nine.', 'x plus one over x, squared — thirty-six.'),
        ('Write "x² + 2 · x · (1/x) + 1/x² = 9"', 'Write "x² + 2 · x · (1/x) + 1/x² = 36"'),
        ('Write "x² + 2 + 1/x² = 9 → x² + 1/x² = 7"', 'Write "x² + 2 + 1/x² = 36 → x² + 1/x² = 34"'),
        ('Take away two: seven.', 'Take away two: thirty-four.'),
        ('That gives nine — choice one.', 'That gives thirty-six — choice one.')])
    # 2) Lesson "r26-t07-quadratic" slide 6 solved (x + 1)² = (x − 3)², the same as guided q-r26-t07-05 -> new lesson example.
    _dd_sub(M, 'r26-t07-quadratic', 6, [
        ('$(x+1)^2=(x-3)^2$', '$(x+3)^2=(x-1)^2$'),
        ('The example (x + 1)² = (x − 3)² appears', 'The example (x + 3)² = (x − 1)² appears'),
        ('Example: x plus one, squared, equals x minus three, squared.', 'Example: x plus three, squared, equals x minus one, squared.'),
        ('Write "x + 1 = x − 3 → 1 = −3 ✗"', 'Write "x + 3 = x − 1 → 3 = −1 ✗"'),
        ('Case one: x plus one equals x minus three. That says one equals negative three — impossible.',
         'Case one: x plus three equals x minus one. That says three equals negative one — impossible.'),
        ('Write "x + 1 = −(x − 3) → 2x = 2 → x = 1 ✓"', 'Write "x + 3 = −(x − 1) → 2x = −2 → x = −1 ✓"'),
        ('Case two: x plus one equals minus x plus three. Two x equals two — x is one.',
         'Case two: x plus three equals minus x plus one. Two x equals negative two — x is negative one.')])
    # 3) q-r26-t07-10 was the lesson example (x² − 9)/(x − 3) = 0 of "r26-t07-quadratic" slide 8 -> new numbers.
    M.set_q('q-r26-t07-10', stem=r'Given: $\frac{x^2 - 36}{x - 6} = 0$. $x = ?$',
            choices=['$6$', '$-6$', '$6$ or $-6$', 'No number satisfies the equation.'], correct=2,
            expl=[r'The numerator must be $0$: $x^2 = 36$. Therefore $x = 6$ or $x = -6$.',
                  r'The denominator cannot be $0$: $x \ne 6$.',
                  r'Therefore $x = -6$ only. Check: $\frac{36 - 36}{-6 - 6} = \frac{0}{-12} = 0$ ✓.'])
    # 4) q-r26-t07-15 was the lesson example xy = 12, yz = 6 of "r26-t07-more-tools" slide 2 -> new numbers.
    M.set_q('q-r26-t07-15', stem='Given:\n' + r'$\begin{cases} xy = 24 \\ yz = 8 \end{cases}$' + '\n' + r'$\frac{x}{z} = ?$',
            choices=['$3$', r'$\frac{1}{3}$', '$16$', '$192$'], correct=1,
            expl=[r'Divide the first equation by the second: $\frac{xy}{yz} = \frac{24}{8}$.',
                  r'The $y$ cancels ($y \ne 0$, since $xy = 24$): $\frac{x}{z} = 3$.'])


# ---------------------------------------------------------------- 2026-10-05 pen vs clicks trial
# "Pen for the thinking, clicks for the copying": mechanical / copied lines become board items that appear on NEXT;
# the key idea of each method and all marks (circle, underline) stay as pen cues.
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


def pen_or_click(M):
    S = 42
    # ---- lesson equation-strategy (only the worked board slides; marks stay by hand)
    _pen_or_click_slide(M, 'equation-strategy', 2, {
        'Write "p = 0  or  q = p"':
            [A('p = 0 or q = p appears', T(r'$p=0 \quad \text{or} \quad q=p$', size=44))],
        'Under it write "Or: check p = 0 separately"':
            [A('Or: check p = 0 separately appears', T(r'Or: check $p=0$ separately', size=38))],
    }, room=['Below write "p²(p − q) = 0"'])
    _pen_or_click_slide(M, 'equation-strategy', 3, {
        'Write "x² = 0 → x = 0"':
            [A('x² = 0 → x = 0 appears', T(r'$x^2=0 \;\to\; x=0$', size=44))],
        'Write "x² = 49 → x = 7 or x = −7"':
            [A('x² = 49 → x = 7 or x = −7 appears', T(r'$x^2=49 \;\to\; x=7 \ \text{ or } \ x=-7$', size=44))],
    }, room=['Write "x²(x² − 49) = 0"'])
    _pen_or_click_slide(M, 'equation-strategy', 4, {
        'Write "x = 8  or  x = −4"':
            [A('x = 8 or x = −4 appears', T(r'$x=8 \quad \text{or} \quad x=-4$', size=44))],
    }, room=['Write "x − 2 = 6  or  x − 2 = −6"'])
    _pen_or_click_slide(M, 'equation-strategy', 7, {
        'Next to this line write "xy = 12, yz = 6 → xy ÷ yz = 12 ÷ 6 → x/z = 2"':
            [A('Example: xy = 12, yz = 6 → x/z = 2 appears',
               T(r'$xy=12,\ yz=6 \;\to\; \frac{xy}{yz}=\frac{12}{6} \;\to\; \frac{x}{z}=2$', size=34))],
    })
    # ---- guided solutions after the lesson
    _pen_or_click_slide(M, 'solve-q-191', 2, {
        'Write "m = 2: 32 = 16n → n = 2"':
            [A('m = 2: 32 = 16n → n = 2 appears', T(r'$m=2:\ \ 32=16n \;\to\; n=2$', size=S))],
    })
    _pen_or_click_slide(M, 'solve-q-191', 3, {
        'Write "m⁴(m − n) = 0 → m = 0 or n = m"':
            [A('m⁴(m − n) = 0 → m = 0 or n = m appears', T(r'$m^4(m-n)=0 \;\to\; m=0 \ \text{ or } \ n=m$', size=S))],
    })
    _pen_or_click_slide(M, 'solve-q-192', 2, {
        'Write "x² = 0 → x = 0"':
            [A('x² = 0 → x = 0 appears', T(r'$x^2=0 \;\to\; x=0$', size=S))],
        'Write "x² = 25 → x = 5 or x = −5"':
            [A('x² = 25 → x = 5 or x = −5 appears', T(r'$x^2=25 \;\to\; x=5 \ \text{ or } \ x=-5$', size=S))],
    }, room=['Write "x²(x² − 25) = 0"'])
    _pen_or_click_slide(M, 'solve-q-193', 2, {
        'Write "x = 5  or  x = −13"':
            [A('x = 5 or x = −13 appears', T(r'$x=5 \quad \text{or} \quad x=-13$', size=S))],
    }, room=['Write "x + 4 = 9  or  x + 4 = −9"'])
    _pen_or_click_slide(M, 'solve-q-194', 2, {
        'Write "×5: a − 6b = 5 − 5b"':
            [A('×5: a − 6b = 5 − 5b appears', T(r'$\times5:\ \ a-6b=5-5b$', size=S))],
        'Write "a − b = 5 > 0"':
            [A('a − b = 5 > 0 appears', T(r'$a-b=5>0$', size=S))],
    }, room=['Write "a = 5 + b"'])
    _pen_or_click_slide(M, 'solve-q-195', 2, {
        'Write "x + y = 5" and circle choice 2':
            [A('x + y = 5 appears', T(r'$x+y=5$', size=S)), D('Circle choice 2')],
    }, room=['Write "13x + 13y = 65" under the equations', 'Write "13(x + y) = 65"'])
    _pen_or_click_slide(M, 'solve-q-197', 2, {
        'Write "4 + 7 + 8 + c = 24"':
            [A('4 + 7 + 8 + c = 24 appears', T(r'$4+7+8+c=24$', size=S))],
        'Write "19 + c = 24 → c = 5" and circle choice 2':
            [A('19 + c = 24 → c = 5 appears', T(r'$19+c=24 \;\to\; c=5$', size=S)), D('Circle choice 2')],
    }, room=['Under the big equation write "(a + b) + (2a + c) + (b + c) + c"'])
    _pen_or_click_slide(M, 'solve-q-196', 2, {
        'Write "(x − y)² = x² + y² − 2xy"':
            [A('(x − y)² = x² + y² − 2xy appears', T(r'$(x-y)^2=x^2+y^2-2xy$', size=S))],
        'Write "2xy = 36 → xy = 18"':
            [A('2xy = 36 → xy = 18 appears', T(r'$2xy=36 \;\to\; xy=18$', size=S))],
    }, room=['Under it write "7² = 85 − 2xy"'])


# ---------------------------------------------------------------- 2026-10-05 lesson back to the Hebrew short intro
# The Hebrew section "Equations - theory" opens with a ~1 minute intro (techniques for the exam's equations; dividing
# by an unknown only if it is not 0) and then teaches each idea inside its own question video. equation-strategy
# becomes that short intro (same id, same place); each idea the old lesson slides taught is now stated in its question.
def _add_rule(M, vid, n, before_say, line, item, label):
    """Insert one spoken line + one board item right before the spoken line (or item label) containing `before_say`.
    If the item before it had extra room for handwriting (pen_or_click), that room moves to the new item."""
    b = M.slide(vid, n); script = []; hit = False
    prev = b['pre'] - 1
    for l in b['lines']:
        if before_say in (l.get('say') or l.get('label') or '') and not hit:
            script += [A(label, item), line]; hit = True; at = prev
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']])); prev = l['appear'] if not hit else prev
        else: script.append(D(l['draw']))
    assert hit, '%s #%d: not found: %s' % (vid, n, before_say)
    room = b['items'][at].get('gap')
    M.set_slide(vid, n, script=script)
    b = M.slide(vid, n)
    new = next(k for k, it in enumerate(b['items']) if it.get('t') == item['t'])
    if room and room > 44 and new == at + 1:
        b['items'][new]['gap'] = room; b['items'][at].pop('gap', None)


def hebrew_intro(M):
    vid = 'equation-strategy'
    M.remove_slides(vid, list(range(2, len(M.video(vid)['beats']) + 1)))
    M.set_slide(vid, 1, script=[
        'In this section: different techniques for solving the equations we get on the exam.',
        'Each question that follows teaches one of them.'])
    M.insert_slides(vid, 1, [
        dict(mode='concept', title='Dividing by an unknown', active=0, pre=[], script=[
            'The first technique: dividing by an unknown.',
            A("'Same operation on both sides: allowed' appears", T('Same operation on both sides: allowed', 40)),
            'We may do the same operation on both sides of an equation.',
            'So we may also divide both sides by x.',
            A("'Divide both sides by x? Only if x is not 0' appears", T(r'Divide both sides by $x$? Only if $x \ne 0$', 40)),
            'But only if x is not zero.',
            A("'x = 0 → dividing by 0: undefined' appears", T(r'$x=0 \;\to\;$ dividing by $0$: undefined', 40)),
            'If x is zero, we are dividing by zero — and that is undefined.',
            "Let's see it in the questions."])])
    M.set_sidebar(vid, ['Dividing by an unknown'])

    # q-191: the trap is taught; add the rule for powers of two and up (Hebrew video 1 ends with it)
    _add_rule(M, 'solve-q-191', 3, 'm⁴(m − n) = 0 → m = 0 or n = m appears',
              'The rule for a power of two and up: take out a common factor. You get a product equal to zero — and then at least one factor is zero.',
              T(r'Power $2$ and up: common factor $\to$ product $=0$', 38),
              "'Power 2 and up: common factor → product = 0' appears")
    _say_replace(M, 'solve-q-191', 3, 'Factor instead: m to the fourth', 'Here: m to the fourth')
    # q-195: "calculate an expression" (Hebrew intro before video 5)
    _add_rule(M, 'solve-q-195', 2, "Don't solve for x and y separately",
              'They ask for an expression? Build it straight from the equations — add them or subtract them.',
              T('Asked for an expression? Add or subtract the equations', 36),
              "'Asked for an expression? Add or subtract the equations' appears")


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


def _cr_intro_only(M, vid, title_script, ahead_script, label="What's ahead"):
    """Lesson -> title slide + one short 'what's ahead' slide (the questions teach the rest)."""
    v = M.video(vid)
    M.remove_slides(vid, list(range(2, len(v['beats']) + 1)))
    M.set_slide(vid, 1, script=title_script)
    M.insert_slides(vid, 1, [dict(mode='concept', title=label, active=0, pre=[], script=ahead_script)])
    M.set_sidebar(vid, [label])


def cut_repeats(M):
    # --- More Equation Tools: Q21 teaches multiply/divide the equations, Q22 teaches x + 1/x
    _cr_intro_only(M, 'r26-t07-more-tools', [
        'Two more tools for equation questions.',
        'Each one gets its own question — and you learn it right there.'], [
        A("'Products or ratios? Multiply or divide' appears", T('Products or ratios? Multiply or divide the equations', 40)),
        'Equations that are products or ratios? We can multiply or divide them.',
        A("'x + 1/x' appears", T(r'$x+\frac{1}{x}$: a favorite on the exam', 40)),
        'And x plus one over x — a favorite on the exam.',
        'Two questions now — one for each tool. Try each one before you watch.'])
    # moved into Q22 (taught only on the cut slide): the minus version
    _cr_slide_after(M, 'solve-q-r26-t07-02', 2, 'With a minus', [
        A("'(x − 1/x)² = x² + 1/x² − 2' appears", T(r'$\left(x-\frac{1}{x}\right)^2=x^2+\frac{1}{x^2}-2$', 40)),
        'One more thing. With a minus — x minus one over x — the middle term is minus two. Then you add two instead.'])

    # --- Quadratic Equations: Q23 factors and tries the choices, Q24 is the a² = b² trap, Q25 is fraction = 0
    L = 'r26-t07-quadratic'
    _cr_titles(M, L, ['What it looks like', 'Special cases'])
    # slide 2: "everything to one side" is taught in Q23; the example x² − 5x + 6 belonged to the cut factor slide
    _cr_drop(M, L, 2, ['$x^2-5x+6=0$', 'Our example', 'Step 1: everything', 'Step one, always',
                       'Why zero? Because a product'])
    # slide 3 (special cases): the "same two numbers" case no longer leans on the cut factor slide
    _cr_replace(M, L, 3, 'Same two numbers', [
        A('x² − 6x + 9 = (x − 3)² = 0 → x = 3 only appears',
          T(r'A perfect square: $x^2-6x+9=(x-3)^2=0 \to x=3$ only', 40))])
    _cr_replace(M, L, 3, 'Sometimes both numbers are the same', [
        'Sometimes it is a perfect square: x minus three, squared, equals zero. Only ONE solution: three.'])
    _cr_insert(M, L, 3, 'So a quadratic can have two solutions', [
        'Three questions now. Each one teaches one more tool. Try each one before you watch.'])
    # moved into Q23: the factor rule (product = c, sum = b) and "a choice that works is one solution"
    _cr_insert(M, 'solve-q-r26-t07-04', 2, 'Write "x² − 2x − 15 = 0"', [
        A("'Factor: product = c, sum = b' appears", T(r'One side $=0$, then factor: product $=c$, sum $=b$', 36)),
        'The method: everything to one side, then factor. Find two numbers: their product is c, the number. Their sum is b, the number in front of x.'],
        before=True)
    _cr_insert(M, 'solve-q-r26-t07-04', 3, 'Choice two again.', [
        A("'A choice that works = ONE solution' appears", T('A choice that works is ONE solution. How many? Factor.', 36)),
        'But a choice that works is one solution — maybe not the only one. For "how many solutions", factor.'])


_apply_before_cut_repeats = apply


def apply(M):
    _apply_before_cut_repeats(M)
    cut_repeats(M)   # 2026-10-05: runs last


# =====================================================================================
# 2026-10-06 practice: the new exam methods as an extra method in PRACTICE explanations
# (append only; the existing worked solution stays as it is). Runs last.
# =====================================================================================
PRACTICE_METHODS = {
    'q-212': [
        'Method 2 · Power count: $x+y$ has power $1$, and so do $a$ and $c$ ($a=6x+5y$). Choice 1 has power $-1$ and choice 4 ($a+c-11$) is mixed, so both are out.',
        'Choices 2 and 3 are left. Pick $x=y=1$: $a=c=11$ and $x+y=2$. Choice 2 gives $\\frac{22}{11}=2$ and choice 3 gives $0$. The answer is choice 2.',
    ],
    'q-206': [
        'Shortcut: pick values that fit. Three letters, two equations, one value asked. $y\\ne0$, so set $y=2$: $k=x-\\frac23$, and $x+4=3k=3x-2$, so $x=3$. Then $\\frac xy=\\frac32$. One value is asked, so every set of values that fits the given gives that same value. Take the easiest one.',
    ],
    'q-175': [
        'Shortcut: pick values that fit. Set $a=0$: $\\frac b3=2$, so $b=6$. Test the choices with $a=0$, $b=6$: $0<6$ ✓, $6<0$ ✗, $0=6$ ✗, $6=0$ ✗. Only choice 1 is left.',
        'Why one pair is enough here: a "necessarily true" choice holds for every pair that fits, so a choice that fails for one fitting pair is out.',
    ],
    'q-202': [
        'Shortcut: pick values that fit. $m\\ne0$, so set $m=1$: $1+n^2=1+2n+n^2$, so $n=0$. With $m=1$ and $n=0$, choices 1, 2 and 3 fail ($1\\ne0$, $0\\ne-1$, $1\\ne5$). Only choice 4 holds.',
    ],
    'q-172': [
        'Shortcut: pick values that fit. $a=1$ gives $1=b$. Choice 3 is out, but choices 1 and 2 also give $1$: a tie.',
        'Tie, so take a second set: $a=0$ gives $0=0$, true for every $b$ (say $b=7$), while choices 1 and 2 give $0$. Two fitting sets give different values of $b$, so $b$ cannot be determined (choice 4).',
    ],
    'q-r26-t07-15': [
        'Shortcut: pick values that fit. $y$ cannot be $0$ (because $xy=24$), so set $y=1$: $x=24$ and $z=8$. Then $\\frac xz=\\frac{24}{8}=3$. One value is asked, so every set of values that fits the given gives that same value. Take the easiest one.',
    ],
    'q-199': [
        'Shortcut: pick values that fit. Set $x=1$ ($x\\ne0$): $\\frac{1}{1+y}=4$, so $1+y=\\frac14$. That is exactly $x+y$, so $x+y=\\frac14$. One value is asked, so every set of values that fits the given gives that same value. Take the easiest one.',
    ],
    'q-204': [
        'Shortcut: pick values that fit. $a$ is any positive number, so set $a=1$: $\\frac{9}{x+4}=\\frac1x$, so $9x=x+4$ and $x=\\frac12$. One value is asked, so every set of values that fits the given gives that same value. Take the easiest one.',
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


# =====================================================================================
# 2026-10-06 pen or click: the rest of topic 7 (all unrecorded videos). Same approved rule as the trial above:
# setup and mechanical lines appear on click; by hand only the one or two key steps + marks on the choices; no long
# text by hand. Runs last (after cut_repeats / practice_methods, which add items to Q21-Q25).
# =====================================================================================
def pen_or_click_rest(M):
    S = 42; s = 38   # s: crowded boards
    P = _pen_or_click_slide
    # ---- Q8 solve-q-184 (33 − 2/3 x = 1/4 x)
    P(M, 'solve-q-184', 2, {
        'Write "33·12 − 8x = 3x"': [A('33·12 − 8x = 3x appears', T(r'$33\cdot12-8x=3x$', size=S))],
        'Write "33·12 = 11x"': [A('33·12 = 11x appears', T(r'$33\cdot12=11x$', size=S))],
        'Cancel 33 with 11 (3 and 1); write "x = 3·12 = 36"':
            [D('Cancel 33 with 11 (3 and 1)'), A('x = 3·12 = 36 appears', T(r'$x=3\cdot12=36$', size=S))],
    })
    P(M, 'solve-q-184', 3, {
        'Write "33 = 1/4 x + 2/3 x = 11/12 x"':
            [A('33 = 1/4 x + 2/3 x = 11/12 x appears', T(r'$33=\frac14x+\frac23x=\frac{11}{12}x$', size=S))],
        'Write "33 ÷ 11/12 = 33 · 12/11 = 36"':
            [A('33 ÷ 11/12 = 33 · 12/11 = 36 appears', T(r'$33\div\frac{11}{12}=33\cdot\frac{12}{11}=36$', size=S))],
    })
    # ---- Q9 solve-q-185 (x³ + 3x² = πx²)
    P(M, 'solve-q-185', 2, {
        'Cross out x² on both sides; write "x + 3 = π"':
            [D('Cross out x² on both sides'), A('x + 3 = π appears', T(r'$x+3=\pi$', size=S))],
        'Write "x = π − 3" and circle choice 2':
            [A('x = π − 3 appears', T(r'$x=\pi-3$', size=S)), D('Circle choice 2')],
    }, room=['Write "x²(x + 3) = πx²"'])
    P(M, 'solve-q-185', 3, {
        'Write "x + 3 = π → x = π − 3"': [A('x + 3 = π → x = π − 3 appears', T(r'$x+3=\pi \;\to\; x=\pi-3$', size=S))],
    })
    # ---- Q10 solve-q-187 (square of the difference = sum of the squares)
    P(M, 'solve-q-187', 2, {
        'Expand: write "a² − 2ab + b² = a² + b²"':
            [A('a² − 2ab + b² = a² + b² appears', T(r'$a^2-2ab+b^2=a^2+b^2$', size=S))],
        'Cross out a² and b² on both sides; write "−2ab = 0"':
            [D('Cross out a² and b² on both sides'), A('−2ab = 0 appears', T(r'$-2ab=0$', size=S))],
        'Write "a = 0 or b = 0" and circle choice 2':
            [A('a = 0 or b = 0 appears', T(r'$a=0 \ \text{ or } \ b=0$', size=S)), D('Circle choice 2')],
    }, room=['Write "(a − b)²"'])
    # ---- Q11 solve-q-186 (p/q = r/s, not necessarily true)
    P(M, 'solve-q-186', 2, {
        'Next to choice 1 write "ps = qr ✓" and cross it out':
            [A('Choice 1: sp = qr ✓ appears', T(r'(1) $\ sp=qr$ ✓', size=34, gap=16)), D('Cross out choice 1')],
        'Next to choice 2 write "ps = qr ✓" and cross it out':
            [A('Choice 2: sp = rq ✓ appears', T(r'(2) $\ sp=rq$ ✓', size=34, gap=16)), D('Cross out choice 2')],
        'Next to choice 3 write "ps = qr ✓" and cross it out':
            [A('Choice 3: qr = ps ✓ appears', T(r'(3) $\ qr=ps$ ✓', size=34, gap=16)), D('Cross out choice 3')],
        'Next to choice 4 write "pr = qs ✗" and circle choice 4':
            [A('Choice 4: pr = qs ✗ appears', T(r'(4) $\ pr=qs$ ✗', size=34)), D('Circle choice 4')],
    })
    P(M, 'solve-q-186', 3, {
        'Next to choices 1 and 3 write "diagonal ÷ leftover ✓"':
            [A("'Isolate a letter: diagonal ÷ leftover' appears", T(r'Isolate a letter: diagonal product $\div$ the one left', size=34)),
             D('Tick choices 1 and 3')],
    })
    # ---- Q12 solve-q-188 (three equations, x = ?)
    P(M, 'solve-q-188', 2, {
        'Write "− (3x + 3z = 18)" and "x = 4"':
            [A('− (3x + 3z = 18) → x = 4 appears', T(r'$-\,(3x+3z=18) \;\to\; x=4$', size=S))],
    }, room=['Write "eq1 + eq2: 4x + 3z = 22"'])
    # ---- Q13 solve-q-189 (mixed-number coefficients, x + y)
    P(M, 'solve-q-189', 2, {
        'Write "8x + 8y = 2a + 2b"': [A('8x + 8y = 2a + 2b appears', T(r'$8x+8y=2a+2b$', size=s))],
        'Write "8(x + y) = 2(a + b) → x + y = (a + b)/4"':
            [A('8(x + y) = 2(a + b) → x + y = (a + b)/4 appears', T(r'$8(x+y)=2(a+b) \;\to\; x+y=\frac{a+b}{4}$', size=s))],
    })
    # ---- Q14 solve-q-190 (a + 2b in x and z)
    P(M, 'solve-q-190', 2, {
        'Subtract the second equation; write "a + 2b = 4x − z"':
            [A('a + 2b = 4x − z appears', T(r'$a+2b=4x-z$', size=S))],
    }, room=['Write "4a + 4b + 4c = 4x"'])
    P(M, 'solve-q-190', 3, {
        'Write "a = b = c = 1 → x = 3, z = 9"':
            [A('a = b = c = 1 → x = 3, z = 9 appears', T(r'$a=b=c=1 \;\to\; x=3,\ z=9$', size=S))],
        'Write "a + 2b = 3"': [A('a + 2b = 3 appears', T(r'$a+2b=3$', size=S))],
    })
    # ---- Q15 solve-q-178 (difference 5, difference of squares 65)
    P(M, 'solve-q-178', 2, {
        'Write "a − b = 5" and "a² − b² = 65"':
            [A('a − b = 5, a² − b² = 65 appears', T(r'$a-b=5 \qquad a^2-b^2=65$', size=S))],
        'Replace (a − b) with 5: write "5(a + b) = 65"': [A('5(a + b) = 65 appears', T(r'$5(a+b)=65$', size=S))],
        'Write "a + b = 13" and circle choice 3':
            [A('a + b = 13 appears', T(r'$a+b=13$', size=S)), D('Circle choice 3')],
    }, room=['Write "(a − b)(a + b) = 65"'])
    P(M, 'solve-q-178', 3, {
        'Write "7, 2 → 49 − 4 = 45"': [A('7, 2 → 49 − 4 = 45 appears', T(r'$7,\,2 \;\to\; 49-4=45$', size=s))],
        'Write "8, 3 → 64 − 9 = 55"': [A('8, 3 → 64 − 9 = 55 appears', T(r'$8,\,3 \;\to\; 64-9=55$', size=s))],
        'Write "9, 4 → 81 − 16 = 65 ✓"': [A('9, 4 → 81 − 16 = 65 ✓ appears', T(r'$9,\,4 \;\to\; 81-16=65$ ✓', size=s))],
    })
    P(M, 'solve-q-178', 4, {
        'Next to choice 1 write "11 → 8, 3: 64 − 9 = 55 ✗"':
            [A('Choice 1: 11 → 8, 3: 55 ✗ appears', T(r'(1) $\ 11 \;\to\; 8,\,3:\ 64-9=55$ ✗', size=s)), D('Cross out choice 1')],
        'Next to choice 2 write "15 → 10, 5: 100 − 25 = 75 ✗"':
            [A('Choice 2: 15 → 10, 5: 75 ✗ appears', T(r'(2) $\ 15 \;\to\; 10,\,5:\ 100-25=75$ ✗', size=s)), D('Cross out choice 2')],
        'Next to choice 3 write "13 → 9, 4: 81 − 16 = 65 ✓"':
            [A('Choice 3: 13 → 9, 4: 65 ✓ appears', T(r'(3) $\ 13 \;\to\; 9,\,4:\ 81-16=65$ ✓', size=s))],
    })
    # ---- Q16 solve-q-179 (x/y = 3, y/z = 4, z/w = 2)
    P(M, 'solve-q-179', 2, {
        'Write "x = 3y"': [A('x = 3y appears', T(r'$x=3y$', size=36, gap=24))],
        'Write "z = 2w → x = 24w"': [A('z = 2w → x = 24w appears', T(r'$z=2w \;\to\; x=24w$', size=36, gap=24))],
        'Write "x/w = 24" and circle choice 2':
            [A('x/w = 24 appears', T(r'$\frac{x}{w}=24$', size=36)), D('Circle choice 2')],
    }, room=['Write "y = 4z → x = 12z"'], row=70)
    P(M, 'solve-q-179', 3, {
        'Write "w = 1 → z = 2 → y = 8 → x = 24"':
            [A('w = 1 → z = 2 → y = 8 → x = 24 appears', T(r'$w=1 \;\to\; z=2 \;\to\; y=8 \;\to\; x=24$', size=S))],
    })
    P(M, 'solve-q-179', 4, {
        'Write "(x/y)·(y/z)·(z/w) = x/w" and cancel y and z':
            [A('(x/y)·(y/z)·(z/w) = x/w appears', T(r'$\frac{x}{y}\cdot\frac{y}{z}\cdot\frac{z}{w}=\frac{x}{w}$', size=S)),
             D('Cancel y and z')],
        'Write "= 3 · 4 · 2 = 24"': [A('= 3 · 4 · 2 = 24 appears', T(r'$=3\cdot4\cdot2=24$', size=S))],
    })
    # ---- Q17 solve-q-180 (pq = 1, q/p)
    P(M, 'solve-q-180', 2, {
        'Write "q/p = (1/p) ÷ p = (1/p) · (1/p) = 1/p²"':
            [A('q/p = (1/p) ÷ p = (1/p)·(1/p) = 1/p² appears',
               T(r'$\frac{q}{p}=\frac1p\div p=\frac1p\cdot\frac1p=\frac{1}{p^2}$', size=S))],
    }, room=['Write "q = 1/p"'])
    P(M, 'solve-q-180', 3, {
        'Write "q/p = 1/2 ÷ 2 = 1/4"': [A('q/p = 1/2 ÷ 2 = 1/4 appears', T(r'$\frac{q}{p}=\frac12\div2=\frac14$', size=S))],
    })
    # ---- Q18 solve-q-181 (2x = y + 3)
    P(M, 'solve-q-181', 2, {
        'Write "4x² = y² + 6y + 9"': [A('4x² = y² + 6y + 9 appears', T(r'$4x^2=y^2+6y+9$', size=s))],
        'Write "4x² − y² = 6y + 9"': [A('4x² − y² = 6y + 9 appears', T(r'$4x^2-y^2=6y+9$', size=s))],
        'Divide by 2: write "2x² − ½y² = 3y + 4.5"':
            [A('÷2: 2x² − ½y² = 3y + 4.5 appears', T(r'$\div2:\ \ 2x^2-\frac12y^2=3y+4.5$', size=s))],
    }, room=['Write "(2x)² = (y + 3)²"'], row=90)
    P(M, 'solve-q-181', 3, {
        'Write "y = 1 → 2x = 4 → x = 2"': [A('y = 1 → 2x = 4 → x = 2 appears', T(r'$y=1 \;\to\; 2x=4 \;\to\; x=2$', size=S))],
        'Write "2·4 − ½·1 = 7.5"': [A('2·4 − ½·1 = 7.5 appears', T(r'$2\cdot4-\frac12\cdot1=7.5$', size=S))],
    })
    # ---- Q19 solve-q-182 ((ax + by)² = 9x² + y² − 6xy)
    P(M, 'solve-q-182', 2, {
        'Write "a²x² + 2abxy + b²y²"': [A('a²x² + 2abxy + b²y² appears', T(r'$(ax+by)^2=a^2x^2+2abxy+b^2y^2$', size=s, gap=30))],
        'Write "a² = 9 → a = ±3"': [A('a² = 9 → a = ±3 appears', T(r'$a^2=9 \;\to\; a=\pm3$', size=s, gap=30))],
        'Write "b² = 1 → b = ±1"': [A('b² = 1 → b = ±1 appears', T(r'$b^2=1 \;\to\; b=\pm1$', size=s, gap=30))],
        'Write "(3, −1) or (−3, 1) → |a − b| = 4"':
            [A('(3, −1) or (−3, 1) → |a − b| = 4 appears', T(r'$(3,-1)$ or $(-3,1) \;\to\; |a-b|=4$', size=s))],
    }, room=['Write "2ab = −6 → ab = −3"'], row=70)
    P(M, 'solve-q-182', 3, {
        'Write "a = 3, b = −1 → |3 − (−1)| = 4"':
            [A('a = 3, b = −1 → |3 − (−1)| = 4 appears', T(r'$a=3,\ b=-1 \;\to\; |3-(-1)|=4$', size=S))],
    }, room=['Write "9x² − 6xy + y² = (3x − y)²"'])
    # ---- Q20 solve-q-183 (a² + 2b² = ¼a²)
    P(M, 'solve-q-183', 2, {
        'Write "4a² + 8b² = a²"': [A('4a² + 8b² = a² appears', T(r'$4a^2+8b^2=a^2$', size=S))],
        'Write "3a² + 8b² = 0"': [A('3a² + 8b² = 0 appears', T(r'$3a^2+8b^2=0$', size=S))],
        'Write "a = 0, b = 0" and circle choice 1':
            [A('a = 0, b = 0 appears', T(r'$a=0,\ \ b=0$', size=S)), D('Circle choice 1')],
    }, room=['Under the terms write "≥ 0" and "≥ 0"'], row=60)
    # ---- Q21 solve-q-r26-t07-01 (divide the equations)
    P(M, 'solve-q-r26-t07-01', 2, {
        'Cancel one x and one y; write "x/y = 18/12 = 3/2"':
            [D('Cancel one x and one y'), A('x/y = 18/12 = 3/2 appears', T(r'$\frac{x}{y}=\frac{18}{12}=\frac32$', size=S))],
    }, room=['Write "x²y ÷ xy² = 18 ÷ 12"'])
    P(M, 'solve-q-r26-t07-01', 3, {
        'Write "x = 3, y = 2: 9 · 2 = 18 ✓, 3 · 4 = 12 ✓"':
            [A('x = 3, y = 2: 9·2 = 18 ✓, 3·4 = 12 ✓ appears', T(r'$x=3,\ y=2:\ \ 9\cdot2=18$ ✓$,\ \ 3\cdot4=12$ ✓', size=S))],
    })
    # ---- Q22 solve-q-r26-t07-02 (x + 1/x = 6)
    P(M, 'solve-q-r26-t07-02', 2, {
        'Write "x² + 2 · x · (1/x) + 1/x² = 36"':
            [A('x² + 2·x·(1/x) + 1/x² = 36 appears', T(r'$x^2+2\cdot x\cdot\frac1x+\frac{1}{x^2}=36$', size=s))],
        'Write "x² + 2 + 1/x² = 36 → x² + 1/x² = 34"':
            [A('x² + 2 + 1/x² = 36 → x² + 1/x² = 34 appears', T(r'$x^2+2+\frac{1}{x^2}=36 \;\to\; x^2+\frac{1}{x^2}=34$', size=s))],
    }, room=['Write "(x + 1/x)² = 6² = 36"'])
    # ---- Q23 solve-q-r26-t07-04 (x(x − 2) = 15)
    P(M, 'solve-q-r26-t07-04', 2, {
        'Write "x² − 2x − 15 = 0"': [A('x² − 2x − 15 = 0 appears', T(r'$x^2-2x-15=0$', size=s, gap=30))],
        'Write "(x − 5)(x + 3) = 0"': [A('(x − 5)(x + 3) = 0 appears', T(r'$(x-5)(x+3)=0$', size=s, gap=30))],
        'Write "x = 5 or x = −3"': [A('x = 5 or x = −3 appears', T(r'$x=5 \ \text{ or } \ x=-3$', size=s))],
    }, room=['Write "(−5) · 3 = −15,  (−5) + 3 = −2"'], row=70)
    # ---- Q24 solve-q-r26-t07-05 ((x + 1)² = (x − 3)²)
    P(M, 'solve-q-r26-t07-05', 2, {
        'Write "x + 1 = x − 3 → 1 = −3 ✗"':
            [A('x + 1 = x − 3 → 1 = −3 ✗ appears', T(r'$x+1=x-3 \;\to\; 1=-3$ ✗', size=s, gap=26))],
        'Write "a² = b² → a = b or a = −b"':
            [A('a² = b² → a = b or a = −b appears', T(r'$a^2=b^2 \;\to\; a=b \ \text{ or } \ a=-b$', size=s, gap=26))],
        'Write "x + 1 = −(x − 3) = −x + 3 → 2x = 2 → x = 1"':
            [D('Write "x + 1 = −(x − 3)"'),
             A('x + 1 = −x + 3 → 2x = 2 → x = 1 appears', T(r'$x+1=-x+3 \;\to\; 2x=2 \;\to\; x=1$', size=s, gap=26))],
        'Write "x = 1: 2² = 4, (−2)² = 4 ✓"':
            [A('x = 1: 2² = 4, (−2)² = 4 ✓ appears', T(r'$x=1:\ \ 2^2=4,\ \ (-2)^2=4$ ✓', size=s))],
    })
    # the hand-written second case needs its own row: the item above it gets the room
    b = M.slide('solve-q-r26-t07-05', 2)
    k = next(l['appear'] for l in b['lines'] if l.get('label') == 'a² = b² → a = b or a = −b appears')
    b['items'][k]['gap'] = b['items'][k].get('gap', 44) + 64
    P(M, 'solve-q-r26-t07-05', 3, {
        'Write "x² + 2x + 1 = x² − 6x + 9"':
            [A('x² + 2x + 1 = x² − 6x + 9 appears', T(r'$x^2+2x+1=x^2-6x+9$', size=S))],
    }, room=['Write "8x = 8 → x = 1"'])
    # ---- Q25 solve-q-r26-t07-06 ((x² − 7x + 12)/(x − 3) = 0)
    P(M, 'solve-q-r26-t07-06', 2, {
        'Write "x² − 7x + 12 = 0"': [A('x² − 7x + 12 = 0 appears', T(r'$x^2-7x+12=0$', size=S))],
        'Write "(x − 3)(x − 4) = 0 → x = 3 or x = 4"':
            [A('(x − 3)(x − 4) = 0 → x = 3 or x = 4 appears', T(r'$(x-3)(x-4)=0 \;\to\; x=3 \ \text{ or } \ x=4$', size=S))],
    })


_apply_before_pen_or_click_rest = apply


def apply(M):
    _apply_before_pen_or_click_rest(M)
    pen_or_click_rest(M)   # 2026-10-06 pen or click: runs last


# ---------------------------------------------------------------- 2026-10-06 practice trimmed
# Practice was 53 questions (Independent practice 40 + "Additional source-bank variants" 13); the Hebrew course has 20.
# Keep all 20 Hebrew self-practice questions (q-198 ... q-217), 3 warm-ups and 6 review questions that practise a type
# the Hebrew 20 do not cover. Remove clones and the old English "retry" set. One practice section is left.
TRIM_REMOVE = (
    # alg-extra t7-1-x: same 7 templates as t7-5-x, only the numbers shifted (clones)
    ['alg-extra-unit-t7-1-%d' % k for k in range(1, 8)]
    # alg-extra t7-5-x warm-ups that are topic-6 level or repeat a Hebrew practice question
    + ['alg-extra-unit-t7-5-1', 'alg-extra-unit-t7-5-2', 'alg-extra-unit-t7-5-5', 'alg-extra-unit-t7-5-7']
    # q-172 ... q-177: Q1-Q6 of the theory section again with other numbers (old English retry set, not in the Hebrew course)
    + ['q-%d' % n for n in range(172, 178)]
    # review questions whose type is already practised by a kept question
    + ['q-r26-t07-' + s for s in ('07', '09', '13', '16', '19', '20', '21')])

TRIM_ORDER = [
    'alg-extra-unit-t7-5-3', 'alg-extra-unit-t7-5-6', 'alg-extra-unit-t7-5-4',
    'q-198', 'q-212', 'q-199', 'q-r26-t07-15', 'q-r26-t07-08', 'q-r26-t07-10',
    'q-200', 'q-210', 'q-211', 'q-201', 'q-202', 'q-204', 'q-205', 'q-206',
    'q-209', 'q-203', 'q-207', 'q-213', 'q-216', 'q-217',
    'q-r26-t07-11', 'q-r26-t07-14', 'q-r26-t07-12',
    'q-215', 'q-208', 'q-214']


def trim_practice(M):
    for qid in TRIM_REMOVE:
        M.unplace(qid)
    sec = 'unit-t7-5'
    M.practice_order(sec, TRIM_ORDER)
    # the second practice section is now empty: drop it (the API cannot remove sections)
    old = 'unit-t7-1'
    assert not M.sections[old]['items'], M.sections[old]['items']
    M.D['sections'] = [s for s in M.D['sections'] if s['id'] != old]
    M.sections.pop(old)
    top = next(t for t in M.D['topics'] if t['id'] == TOPIC)
    top['sections'].remove(old)
    got = [f['ref'] for f in M.D['flow'] if f['section'] == sec and f['type'] == 'question']
    assert got == TRIM_ORDER, got


_apply_before_trim_practice = apply


def apply(M):
    _apply_before_trim_practice(M)
    trim_practice(M)   # 2026-10-06 practice trimmed: runs last


# =====================================================================================
# 2026-10-06 quadratics removed (teacher): real exams (~1,000 questions checked) have essentially no x² + bx + c = 0
# solved by factoring a trinomial (topic 4 dropped "Factoring Trinomials" for the same reason). What is common stays:
# x² = k → ±, common factor → product = 0, difference of squares, a² = b². Runs last.
# The lesson r26-t07-quadratic was already recorded (17:08); the teacher decided to remove it anyway (file stays).
# =====================================================================================
def remove_quadratics(M):
    adv = 'equation-b'; old = 'r26-t07-quadratic'
    # 1) out of the course: the lesson, guided Q23 (x² − 2x = 15) and Q25 ((x² − 7x + 12)/(x − 3) = 0) with their
    #    videos, and practice q-r26-t07-11 (x² − 10x + 25 = 0, a trinomial = 0). unplace() drops a question's video.
    M.unplace(old); M.D['videos'].pop(old, None)
    for qid in ('q-r26-t07-04', 'q-r26-t07-06', 'q-r26-t07-11'):
        M.unplace(qid)
    # 2) Q24 ((x + 1)² = (x − 3)², the a² = b² trap) and the summary move to the end of Advanced study B, after Q22
    M.move('q-r26-t07-05', adv, after='solve-q-r26-t07-02')
    M.move('solve-q-r26-t07-05', adv, after='q-r26-t07-05')
    M.move('r26-t07-summary', adv, after='solve-q-r26-t07-05')
    v = M.video('solve-q-r26-t07-05')   # same group title as Q21/Q22 (their videos are recorded: not touched)
    v['title'] = v['navLabel'] = v['hybrid']['title'] = 'More Equation Tools'
    M.set_sidebar('solve-q-r26-t07-05', ['Question 21', 'Question 22', 'Question 24'])   # renumber_guided -> 23
    for b in v['beats'][1:]: b['active'] = 2
    # the empty section goes (the API cannot remove sections)
    assert not M.sections[old]['items'], M.sections[old]['items']
    M.D['sections'] = [s for s in M.D['sections'] if s['id'] != old]
    M.sections.pop(old)
    next(t for t in M.D['topics'] if t['id'] == TOPIC)['sections'].remove(old)
    # 3) summary: the "Quadratics" slide (x² − 8x + 15 = (x − 3)(x − 5)) goes; "Fraction = 0" stays
    S = 'r26-t07-summary'
    assert M.slide(S, 4)['title'] == 'Quadratics' and M.slide(S, 5)['title'] == 'Fraction = 0'
    M.remove_slides(S, [4])
    sb = M.video(S)['hybrid']['sidebar']; q = sb.index('Quadratics')
    M.set_sidebar(S, sb[:q] + sb[q + 1:])
    for b in M.video(S)['beats']:
        if b['active'] > q: b['active'] -= 1
    # 4) memory card: the "Quadratic equations" table (product c, sum b, factor)
    c = M.card('mem-r26-t07-equations')
    c['tables'] = [t for t in c['tables'] if t['title'] != 'Quadratic equations']
    got = [f['ref'] for f in M.D['flow'] if f['section'] == adv]
    assert got[-5:] == ['q-r26-t07-02', 'solve-q-r26-t07-02', 'q-r26-t07-05', 'solve-q-r26-t07-05', 'r26-t07-summary'], got


_apply_before_remove_quadratics = apply


def apply(M):
    _apply_before_remove_quadratics(M)
    remove_quadratics(M)   # 2026-10-06 quadratics removed: runs last


# =====================================================================================
# 2026-10-07 methods spread: the 2026-10-06 exam methods added as an extra written line wherever they genuinely
# solve the question (append only; the existing solution stays). Methods taught in a later topic are phrased as a
# self-contained shortcut with a one-line why. No video changes. Runs LAST.
# =====================================================================================
SPREAD_METHODS = {
    'q-194': [
        'Shortcut: pick values that fit. Set $b=0$: $\\frac a5=1$, so $a=5$. Test the choices with $a=5$, $b=0$: $5=0$ ✗, $5<0$ ✗, $5=0$ ✗, $0<5$ ✓. Only choice 4 is left.',
        'Why one set is enough here: a necessarily true choice holds for every set of values that fits, so a choice that fails for one fitting set is out.',
    ],
    'q-187': [
        'Shortcut: pick values that fit. Try $0$ first: $a=0$, $b=5$ gives $(0-5)^2=25=0^2+5^2$ ✓. With this pair the numbers are not equal, their sum is $5$, and $0\\cdot5\\ne1$, so choices 1, 3 and 4 are out. Only choice 2 is left.',
        'Why one set is enough here: a necessarily true choice holds for every set of values that fits, so a choice that fails for one fitting set is out.',
    ],
    'q-216': [
        'Shortcut: pick values that fit. $A=4$, $B=2$, $C=1$ fit the given (the ratio $4:2$ equals the ratio $2:1$). Then the ratio $A:C$ is $4:1$.',
        'With these values the choices give the ratios $4:1$, $1:1$, $1:4$ and $2:1$. Only choice 1. The right choice must be true for every set of values that fits, so one set is enough to knock out the others.',
    ],
    'q-217': [
        'Shortcut: pick values that fit. Set $k=1$ and $t=3$ (both allowed): $x=2-3=-1$ and $y=-1+2-3=-2$, so $\\frac yx=2$.',
        'With $k=1$, $t=3$ the choices give $\\frac23$, $2$, $0$ and $0$. Only choice 2. The right choice equals $\\frac yx$ for every allowed $k$ and $t$, so it must give $2$ here. (Avoid $t=1$: then choices 1 and 2 tie.)',
    ],
    'q-201': [
        'Shortcut: pick values that fit. Set $x=2$: $\\frac{2}{y+2}=\\frac42=2$, so $y+2=1$ and $y=-1$.',
        'With $x=2$ the choices give $-1$, $\\frac12$, $2$ and $2$. Only choice 1. The right choice gives $y$ for every allowed $x$, so it must give $-1$ at $x=2$.',
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


# =====================================================================================
# 2026-10-07 study-plan order: students meet the topics in the STUDY PLAN order (src/lib/planData.ts ORDER), not
# by topic number. A named method used before the topic that teaches it (in the plan) becomes a self-contained
# "Shortcut · <name>: <why>" line; a "Shortcut" whose method the plan already taught becomes a normal
# "Method N · <name>" line. Unrecorded videos only. Runs LAST.
# =====================================================================================

def _po_line(M, qid, start, new):
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(start)]
    assert len(k) == 1, (qid, start, k)
    ex[k[0]] = new
    M.set_q(qid, expl=ex)


def _po_relabel(M, qid, old, name):
    import re as _re
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(old)]
    assert len(k) == 1, (qid, old, k)
    used = [int(n) for l in ex for n in _re.findall(r'^Method (\d+) ·', l)]
    rest = ex[k[0]][len(old):].lstrip()
    if _re.match(r'[A-Z][a-z]', rest): rest = rest[0].lower() + rest[1:]
    ex[k[0]] = 'Method %d · %s: %s' % (max(used) + 1 if used else 2, name, rest)
    M.set_q(qid, expl=ex)


def _po_say(M, vid, n, old, new):
    """Replace the spoken line `old` (exact) on slide n with `new` (a string, or a list of strings)."""
    b = M.slide(vid, n)
    k = [i for i, l in enumerate(b['lines']) if l.get('say') == old]
    assert len(k) == 1, (vid, n, old)
    M.edit_lines(vid, n, lambda ls: ls[:k[0]] + [{'say': s} for s in ([new] if isinstance(new, str) else new)] + ls[k[0] + 1:])


def plan_order_fix(M):
    # "Pick values that fit" is taught in topic 51 (day 6), before topic 7 in the plan: a normal method line.
    _po_relabel(M, 'q-187', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-194', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-199', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-201', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-202', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-204', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-206', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-216', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-217', 'Shortcut: pick values that fit.', 'Pick values that fit')
    _po_relabel(M, 'q-r26-t07-15', 'Shortcut: pick values that fit.', 'Pick values that fit')


_apply_before_plan_order_fix = apply


def apply(M):
    _apply_before_plan_order_fix(M)
    plan_order_fix(M)   # 2026-10-07 study-plan order: runs last


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
    # r26-t07-more-tools announced two "new" tools that were already taught: multiplying / dividing equations (topic 6,
    # Systems of Equations, Multiply equations) and x + 1/x (topic 4, Contracted Multiplication Formulas). Now a reminder.
    G = 'r26-t07-more-tools'
    if not R.recorded(G):
        R.set_slide(M, G, 'More Equation Tools', ['Two tools you already know come back in equation questions.'])
        s = R.lines_of(M, G, "What's ahead")
        s = R.replace_line(s, 'Equations that are products or ratios?', 'Equations that are products or ratios? Multiply or divide them — as in systems of equations.')
        s = R.replace_line(s, 'And x plus one over x', 'And x plus one over x — square it, as you learned with the formulas.')
        R.set_slide(M, G, "What's ahead", s)


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
    _mn_load().method_names(M, 7)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 Hebrew points restored. The 2026-10-05 cut assumed the question videos teach what the lesson taught;
# here they only answered the questions, and a few of the teacher's Hebrew lesson points were lost. Each point is put
# back as a few spoken lines. These videos were recorded: the teacher decided (2026-10-08) to re-record / continue
# them, so each one is listed in _rerecord.RERECORD (option 1 = re-record the whole video, option 2 = new last slide,
# "Continue a take"). See tNN_CHANGES.md ("2026-10-08 Hebrew points restored"). Runs LAST.
# =====================================================================================================================
import importlib.util as _ilu_hb, os as _os_hb
_s_hb = _ilu_hb.spec_from_file_location('_hebrew_back', _os_hb.path.join(_os_hb.path.dirname(_os_hb.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu_hb.module_from_spec(_s_hb); _s_hb.loader.exec_module(HB)


def _hb_last_slide(M, vid, title, script):
    """option 2: one new slide at the END of the video (same question on the board, same sidebar item)."""
    b = M.video(vid)['beats'][-1]
    HB.append_slides(M, vid, [dict(mode=b['mode'], title=title, active=b['active'],
                                   pre=[dict(it) for it in b['items'][:b['pre']]], script=script)])


def hebrew_points_back(M):
    # Q5 (q-195): the Hebrew lesson's "how did I know to add, not subtract or divide?" - not common, a matter of practice,
    # aim for the move that gives both letters the same coefficient (taken out as a common factor).
    _hb_last_slide(M, 'solve-q-195', 'Add or subtract?', [
        A("'Which move? The one that gives x and y the same coefficient' appears",
          T('Which move? The one that gives $x$ and $y$ the same coefficient', size=40)),
        'How did I know to add — and not subtract, or divide?',
        "Honestly, there's nothing to memorize. These questions aren't very common, and it's a matter of practice.",
        'Ask yourself: which move gives x and y the same number in front? Then you take it out as a common factor.',
        "After a few questions, you'll start to see the patterns."])
    # Q7 (q-196): "a rare type, but worth knowing" + why the 2xy is written last
    assert HB.add_lines(M, 'solve-q-196', 'Hidden formula', 'Which formula has x squared plus y squared', [
        'A rare type on the exam — but worth knowing.'], where='before')
    assert HB.add_lines(M, 'solve-q-196', 'Hidden formula', 'Which formula has x squared plus y squared', [
        'Look how I write it: the two x y goes LAST, not in the middle. That way x squared plus y squared stay side by side — exactly the piece the question gives us.'])


_apply_before_hebrew_points_back = apply


def apply(M):
    _apply_before_hebrew_points_back(M)
    hebrew_points_back(M)   # 2026-10-08 Hebrew points restored: runs LAST


# =====================================================================================================================
# 2026-10-09 choice order like the real exam (teacher: "if the answer can be 1 it will be in choice number 1, same with
# 2 3 4, and also same with 1/2 1/4 1/3"): a choice 1/2/3/4 (or 1/2, 1/3, 1/4) sits in its own place; the correct
# answer and every spoken / drawn / written choice position follow. Data and rules: _choice_order.py (a question whose
# video was recorded before its CUTOFF keeps its old order). Runs LAST.
# =====================================================================================================================
def _co_load():
    import importlib.util, os, sys
    if '_choice_order' in sys.modules: return sys.modules['_choice_order']   # one copy: its WARN / CHANGED add up
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_choice_order.py')
    spec = importlib.util.spec_from_file_location('_choice_order', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); sys.modules['_choice_order'] = m
    return m


_apply_before_choice_order = apply


def apply(M):
    _apply_before_choice_order(M)
    _co_load().choice_order(M, 7)   # 2026-10-09 choice order: runs LAST
