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


# ---------------------------------------------------------------- 7. pass 2: summary video before the practice
def summary(M):
    sb = ["Don't divide by x", 'Plus AND minus', 'Quadratics', 'Fraction = 0', 'Build the expression',
          'Hidden formulas', 'Two unknowns', 'Plug in or try', 'Before you practice']
    slides = [
        dict(mode='title', title='Summary', script=[
            'Before you practice, a quick summary of equations.',
            'The rules, the shortcuts and the traps — in three minutes.']),
        dict(mode='concept', title="Don't divide by x", active=0, pre=[], script=[
            A('x³ = x²y → x²(x − y) = 0 appears', T('$x^3=x^2y \;\\to\; x^2(x-y)=0 \;\\to\; x=0$ or $x=y$', 44)),
            "Dividing by x? Only if x can't be zero.",
            'Otherwise: everything to one side, take out the common factor, and split the product.']),
        dict(mode='concept', title='Plus AND minus', active=1, pre=[], script=[
            A('(x − 6)² = 16 → x − 6 = 4 or −4 appears', T('$(x-6)^2=16 \;\\to\; x-6=4$ or $x-6=-4$', 44)),
            'Taking a root to solve? Plus AND minus.',
            A('a² = b² → a = b or a = −b appears', T('$a^2=b^2 \;\\to\; a=b$ or $a=-b$', 46)),
            'Two equal squares: the numbers are equal — or opposite. Check both cases.']),
        dict(mode='concept', title='Quadratics', active=2, pre=[], script=[
            A('x² − 5x + 6 = (x − 2)(x − 3) = 0 appears', T('$x^2-5x+6=(x-2)(x-3)=0$', 48)),
            'Everything to one side, zero on the other. Two numbers: product c, sum b.',
            A('x = 2 or x = 3 appears', T('$x=2$ or $x=3$ — the sign flips', 44)),
            'Each factor equals zero. Watch the sign: x minus two gives two.',
            'Two solutions, one — like x minus three, squared — or none, like x squared equals minus four.']),
        dict(mode='concept', title='Fraction = 0', active=3, pre=[], script=[
            A("'Numerator = 0, denominator ≠ 0' appears", T('Fraction $=0$: numerator $=0$, denominator $\\ne 0$', 42)),
            'A fraction is zero when the top is zero — and the bottom is not.',
            A('(x² − 9)/(x − 3) = 0 → x = −3 appears', T('$\\frac{x^2-9}{x-3}=0 \;\\to\; x=-3$ only', 46)),
            'Three makes the bottom zero. Throw it out.']),
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
            A('a + 2b + c = (a + b) + (b + c) appears', T('$a+2b+c=(a+b)+(b+c)$', 44)),
            'A big equation? Break it into the small ones.']),
        dict(mode='concept', title='Two unknowns', active=6, pre=[], script=[
            A("'One equation, two unknowns → a relationship' appears", T('One equation, two unknowns $\\to$ a relationship', 40)),
            "One equation, two unknowns: no values — but a relationship. a plus three equals b means b is bigger.",
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
