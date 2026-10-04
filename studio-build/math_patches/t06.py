"""Topic 6 — Equations: Fundamentals. Course review 2026-09 fixes (see t06_CHANGES.md)."""
from math_api import T, H, A, D, Q, rich_plain

TOPIC = 6
LE, SY = 'linear-equations', 'systems'


def cases(*eqs):
    return r'$\begin{cases} ' + r' \\ '.join(eqs) + r' \end{cases}$'


def given_sys(*eqs, ask='x'):
    return 'Given:\n' + cases(*eqs) + '\n$%s = ?$' % ask


def given_eq(eq, ask='x', pre='Given: '):
    return pre + '$' + eq + '$\n$%s = ?$' % ask


def draw_fix(old, new):
    def fn(lines):
        out = []
        for l in lines:
            l = dict(l)
            for k in ('say', 'draw'):
                if k in l and old in l[k]: l[k] = l[k].replace(old, new)
            out.append(l)
        return out
    return fn


def apply(M):
    # =====================================================================================
    # 1. Existing questions: text (TeX, stacked equations, full worked solutions)
    # =====================================================================================
    S = M.set_q
    # --- guided ---
    S('q-171', stem='Given: $x \\ne 2$ and $x \\ne 4$.\n$\\frac{3}{x-4}=\\frac{1}{x-2}$\n$x = ?$',
      choices=['$1$', '$31$', '$21$', '$2$'], correct=1,   # pass 2: original distractors 31 and 21 restored
      expl=['The restrictions are $x \\ne 2$ and $x \\ne 4$.',
            'One fraction equals one fraction, so cross-multiply: $3(x-2)=1\\cdot(x-4)$.',
            '$3x-6=x-4 \\to 2x=2 \\to x=1$.',
            '$1$ is not a forbidden value. Check: $\\frac{3}{-3}=-1$ and $\\frac{1}{-1}=-1$. The answer is choice 1.'])
    S('q-164', stem=given_sys('6x+3y=36', 'x+y=7'),
      expl=['Divide the first equation by $3$: $2x+y=12$.',
            'Subtract the second equation: $(2x+y)-(x+y)=12-7$, so $x=5$.',
            'Check: $y=2$, and $6\\cdot5+3\\cdot2=36$. The answer is choice 1.'])
    S('q-165', stem=given_sys('2x+y=19', '3x+2y=31'),
      expl=['They ask for $x$, so match the $y$ terms. Multiply the first equation by $2$: $4x+2y=38$.',
            'Subtract the second equation: $(4x+2y)-(3x+2y)=38-31$, so $x=7$.',
            'Check: $y=19-14=5$, and $3\\cdot7+2\\cdot5=31$. The answer is choice 1.'])

    # --- single-equation practice ---
    S('q-166', stem=given_eq('4x+9=1'),
      expl=['Subtract $9$ from both sides: $4x=-8$.', 'Divide by $4$: $x=-2$.'])
    S('q-167', stem=given_eq('4(3-x)=3(x-3)'),
      expl=['Open the brackets: $12-4x=3x-9$.', 'Move the $x$ terms to the right and the numbers to the left: $12+9=3x+4x$, so $21=7x$ and $x=3$.'])
    S('q-168', stem=given_eq('\\frac{4(x-3)}{5}=4'),
      expl=['Multiply both sides by $5$: $4(x-3)=20$.', 'Divide by $4$: $x-3=5$, so $x=8$.'])
    S('q-169', stem=given_eq('\\frac{8x+12}{4}=\\frac{6x+9}{3}'),
      choices=['$x$ can be any number', '$3$', '$2$', '$0$'],
      expl=['Simplify each side: $\\frac{8x+12}{4}=2x+3$ and $\\frac{6x+9}{3}=2x+3$.',
            'The equation is $2x+3=2x+3$. Take $2x$ off both sides: $3=3$, which is always true.',
            'So every $x$ is a solution (infinitely many solutions).'])
    S('q-170', stem=given_eq('\\frac{4(x+3)}{2}=2x+5'),
      choices=['No value of $x$ satisfies the equation', '$-\\frac{5}{2}$', '$3$', '$0$'],
      expl=['Left side: $\\frac{4(x+3)}{2}=2(x+3)=2x+6$.',
            'The equation becomes $2x+6=2x+5$. Take $2x$ off both sides: $6=5$, which is false.',
            'So no $x$ satisfies the equation.'])
    S('alg-extra-unit-t6-4-4', stem=given_eq('3x+8=x+20'), choices=['$8$', '$6$', '$5$', '$7$'],
      expl=['Subtract $x$ from both sides: $2x+8=20$.', 'Subtract $8$: $2x=12$, so $x=6$.'])
    S('alg-extra-unit-t6-4-6', stem=given_eq('5(x+1)-2x=29'), choices=['$7$', '$9$', '$10$', '$8$'],
      expl=['Open the bracket: $5x+5-2x=29$.', 'Collect: $3x+5=29$, so $3x=24$ and $x=8$.'])
    S('alg-extra-unit-t6-4-7', stem='Given: $x \\ne -2$ and\n$\\frac{x-7}{x+2}=\\frac{2}{11}$\n$x = ?$',
      choices=['$10$', '$11$', '$9$', '$8$'],
      expl=['One fraction equals one fraction, so cross-multiply: $11(x-7)=2(x+2)$.',
            '$11x-77=2x+4 \\to 9x=81 \\to x=9$.',
            '$9$ is allowed ($9 \\ne -2$). Check: $\\frac{2}{11}=\\frac{2}{11}$.'])

    # --- systems practice ---
    S('q-159', stem=given_sys('3x+2y=-2', 'x=-2', ask='y'),
      expl=['Put $x=-2$ into the first equation: $3\\cdot(-2)+2y=-2$.', '$-6+2y=-2 \\to 2y=4 \\to y=2$.'])
    S('q-160', stem=given_sys('2x+y=15', 'x+y=9'),
      expl=['Same $y$ in both equations, so subtract: $(2x+y)-(x+y)=15-9$.', 'The $y$ terms cancel: $x=6$.'])
    S('q-161', stem=given_sys('2x-2y=0', 'x+2y=6'),
      expl=['From the first equation: $2x=2y$, so $x=y$.', 'Put $y$ in place of $x$ in the second equation: $y+2y=6 \\to 3y=6 \\to y=2$.', 'So $x=2$.'])
    S('q-162', stem=given_sys('x+y=24', 'x-y=6', ask='y'),
      expl=['Subtract the second equation from the first. Keep it in brackets: $(x+y)-(x-y)=24-6$.',
            '$x+y-x+y=18 \\to 2y=18 \\to y=9$.',
            'Shortcut: $y$ is half the difference: $\\frac{24-6}{2}=9$.'])
    S('q-163', stem=given_sys('2(x+2)-y=10+y', 'x+y=5'),
      expl=['Tidy the first equation: $2x+4-y=10+y \\to 2x-2y=6 \\to x-y=3$.',
            'Add $x+y=5$: $2x=8$, so $x=4$.'])
    S('alg-extra-unit-t6-2-3', stem=given_sys('2x+3y=29', '3x+2y=26', ask='x+y'),
      choices=['$10$', '$12$', '$13$', '$11$'],
      expl=['They ask for $x+y$, so add the equations: $(2x+3y)+(3x+2y)=29+26$.',
            '$5x+5y=55$, so $5(x+y)=55$ and $x+y=11$.',
            'No need to find $x$ and $y$ separately.'])
    S('alg-extra-unit-t6-2-4', stem=given_sys('2x+3y=34', '3x+2y=31', ask='x-y'),
      choices=['$-2$', '$-1$', '$-3$', '$-4$'],
      expl=['They ask for $x-y$, so subtract the first equation from the second: $(3x+2y)-(2x+3y)=31-34$.',
            '$x-y=-3$.',
            'Careful with the order: subtracting the other way gives $-x+y=3$, which is $y-x$, not $x-y$.'])

    # --- mixed practice ---
    S('q-139', stem=given_eq('2x-9=x+3'),
      expl=['Move the $x$ terms to the left and the numbers to the right: $2x-x=3+9$.', 'So $x=12$.'])
    S('q-140', stem=given_eq('3(x-7)=15'),
      expl=['Divide both sides by $3$: $x-7=5$.', 'So $x=12$.'])
    S('q-142', stem=given_eq('\\frac{3x+3}{3}=6'),
      expl=['Multiply both sides by $3$: $3x+3=18$.', '$3x=15$, so $x=5$.',
            'Or divide the whole numerator by $3$ first: $x+1=6$.'])
    S('q-143', stem=given_eq('\\frac{6x+4}{5}-\\frac{x+3}{3}=\\frac{2x+18}{10}'),
      expl=['The common denominator of $5$, $3$ and $10$ is $30$. Multiply every term by $30$ and put each numerator in brackets:',
            '$6(6x+4)-10(x+3)=3(2x+18)$.',
            'The minus hits the whole bracket: $36x+24-10x-30=6x+54$.',
            '$26x-6=6x+54 \\to 20x=60 \\to x=3$.'])
    S('q-144', stem=given_sys('4x+y=29', 'y=5'),
      expl=['Put $y=5$ into the first equation: $4x+5=29$.', '$4x=24$, so $x=6$.'])
    S('q-145', stem=given_sys('x+2y=13', '2x=10', ask='y'),
      expl=['From $2x=10$: $x=5$.', 'Put it into the first equation: $5+2y=13 \\to 2y=8 \\to y=4$.'])
    S('q-146', stem=given_sys('2x+y=22', 'x-y=2'),
      expl=['Opposite $y$ terms, so add the equations: $(2x+y)+(x-y)=22+2$.', '$3x=24$, so $x=8$.'])
    S('q-147', stem=given_sys('x+3y=11', 'x+y=5', ask='y'),
      expl=['Same $x$ in both, so subtract: $(x+3y)-(x+y)=11-5$.', '$2y=6$, so $y=3$.'])
    S('q-148', stem=given_sys('x+y=18', 'x-y=8'),
      expl=['Add the two equations: the $y$ terms cancel, and $2x=26$.', 'So $x=13$.',
            'Shortcut: $x$ is half the sum: $\\frac{18+8}{2}=13$.'])
    S('q-149', stem=given_sys('4x+3y=18', '5x-y=13'),
      expl=['In the second equation $y$ has coefficient $1$, so isolate it: $y=5x-13$.',
            'Substitute: $4x+3(5x-13)=18 \\to 4x+15x-39=18 \\to 19x=57$.', 'So $x=3$.'])
    S('q-150', stem=given_sys('3x+2y=12', '2x+4y=16'),
      expl=['They ask for $x$, so match the $y$ terms. Double the first equation: $6x+4y=24$.',
            'Subtract the second: $(6x+4y)-(2x+4y)=24-16 \\to 4x=8$.', 'So $x=2$.'])
    S('q-151', stem=given_sys('4x+3y=18', '3x-2y=22'),
      expl=['Match the $y$ terms: multiply the first equation by $2$ and the second by $3$.',
            '$8x+6y=36$ and $9x-6y=66$.',
            'Add: $17x=102$, so $x=6$.'])
    S('q-152', stem=given_eq('\\frac{\\frac{1}{x}}{3}=5'),
      expl=['Multiply both sides by $3$: $\\frac{1}{x}=15$.',
            'If $\\frac{1}{x}=15$, then $x$ is the reciprocal of $15$: $x=\\frac{1}{15}$.',
            'Check: $\\frac{1}{x}=15$ and $\\frac{15}{3}=5$.'])
    S('q-153', stem='Given: $x > 0$ and $y > 0$, and\n' + cases('xy=18', '\\frac{x}{y}=2') + '\n$x+y = ?$',
      expl=['Multiply the two equations: $xy\\cdot\\frac{x}{y}=18\\cdot2$, so $x^2=36$.',
            '$x$ is positive, so $x=6$. Then $6y=18$, so $y=3$.',
            '$x+y=9$.',
            'Or substitute: $\\frac{x}{y}=2$ gives $x=2y$, so $2y\\cdot y=18$, $y^2=9$ and $y=3$.'])
    S('q-154', stem='Given: $x \\ne -1$ and $x \\ne -3$.\n$\\frac{1}{x+3}=\\frac{2}{x+1}$\n$x = ?$',
      expl=['One fraction equals one fraction, so cross-multiply: $1\\cdot(x+1)=2(x+3)$.',
            '$x+1=2x+6$, so $x=-5$.',
            '$-5$ is allowed. Check: $\\frac{1}{-2}=\\frac{2}{-4}$.'])
    S('q-155', stem='Given: $x \\ne 0$ and\n' + cases('x^2=4y', 'y=3x') + '\n$x = ?$',
      expl=['Put $y=3x$ into the first equation: $x^2=4\\cdot3x=12x$.',
            'Do not divide by something that could be $0$. Here we are told $x \\ne 0$, so we may divide by $x$: $x=12$.'])
    S('q-156', stem='How many solutions does the equation $x=7x$ have?',
      choices=['One', 'Two', 'Seven', 'The equation has no solution'], correct=1,   # pass 2: original choices
      expl=['Move everything to one side: $7x-x=0$, so $6x=0$ and $x=0$.',
            'One solution: $x=0$. The answer is choice 1.',
            'The trap: dividing both sides by $x$ gives $1=7$ and "no solution". But $x$ may be $0$, so we may not divide by it.'])
    S('q-157', stem='Given:\n' + cases('(m+1)(n+1)=5', 'mn=-3') + '\n$m+n = ?$',
      expl=['Open the brackets: $(m+1)(n+1)=mn+m+n+1$.',
            'So $mn+m+n+1=5$. Put in $mn=-3$: $-3+(m+n)+1=5$.',
            '$m+n-2=5$, so $m+n=7$.'])
    S('q-158', stem='Given: $x \\ne -1$ and\n$\\frac{(x-2)-(2-x)}{1+x}=1$\n$x = ?$',
      expl=['Numerator: $(x-2)-(2-x)=x-2-2+x=2x-4$.',
            'So $\\frac{2x-4}{1+x}=1$. Multiply both sides by $1+x$: $2x-4=1+x$.',
            'So $x=5$. It is allowed ($5 \\ne -1$).'])
    S('alg-extra-unit-t6-1-4', stem=given_sys('x+y=12', 'xy=35', ask='x^2+y^2'),
      choices=['$76$', '$72$', '$74$', '$144$'],
      expl=['Square the sum: $(x+y)^2=x^2+2xy+y^2$.',
            'So $x^2+y^2=(x+y)^2-2xy=12^2-2\\cdot35=144-70=74$.'])
    S('alg-extra-unit-t6-1-5', stem='Given: $x \\ne -7$ and\n$\\frac{x-5}{x+7}=\\frac{1}{2}$\n$x = ?$',
      choices=['$18$', '$16$', '$17$', '$12$'],
      expl=['One fraction equals one fraction, so cross-multiply: $2(x-5)=1\\cdot(x+7)$.',
            '$2x-10=x+7$, so $x=17$.',
            'Check: $\\frac{12}{24}=\\frac{1}{2}$.'])
    S('alg-extra-unit-t6-1-6', stem='Given: $x(x-5)=0$\nWhat is the sum of all the solutions of the equation?',
      choices=['$5$', '$0$', '$-5$', '$10$'],
      expl=['A product is $0$ when one of the factors is $0$: $x=0$ or $x-5=0$.',
            'So $x=0$ or $x=5$. The sum is $0+5=5$.',
            'The trap: dividing by $x$ loses the solution $x=0$ (here the sum would still be $5$, but on other questions it matters).'])
    S('alg-extra-unit-t6-1-7', stem='For what value of $k$ does the equation $(5-k)x=7$ have no solution?',
      choices=['$5$', '$4$', '$6$', '$0$'],
      expl=['If $k=5$, the equation becomes $0\\cdot x=7$, which is $0=7$. That is false for every $x$, so there is no solution.',
            'For any other $k$ we can divide by $5-k$ and get one solution.'])

    # =====================================================================================
    # 2. Pass 2: the 13 original practice items are restored (plan), with TeX and full numeric solutions
    # =====================================================================================
    S('alg-extra-unit-t6-4-1', stem=given_eq('2x-5=1'), choices=['$3$', '$2$', '$4$', '$5$'],
      expl=['Add $5$ to both sides: $2x=6$.', 'Divide by $2$: $x=3$. The answer is choice 1.'])
    S('alg-extra-unit-t6-4-2', stem=given_eq('3(x-2)=6'), choices=['$5$', '$6$', '$4$', '$3$'],
      expl=['Divide both sides by $3$: $x-2=2$.', 'Add $2$: $x=4$. The answer is choice 3.'])
    S('alg-extra-unit-t6-4-3', stem=given_eq('\\frac{x+7}{4}=\\frac{12}{4}'), choices=['$4$', '$6$', '$7$', '$5$'],
      expl=['Same denominator on both sides: multiply both sides by $4$. Then $x+7=12$.',
            'Subtract $7$: $x=5$. The answer is choice 4.'])
    S('alg-extra-unit-t6-4-5', stem=given_eq('\\frac{x}{2}+9=\\frac{25}{2}'), choices=['$8$', '$9$', '$7$', '$6$'],
      expl=['Multiply every term by $2$: $x+18=25$.', 'Subtract $18$: $x=7$. The answer is choice 3.'])
    S('alg-extra-unit-t6-2-1', stem=given_sys('2x+3y=19', '3x+2y=16'), choices=['$4$', '$2$', '$1$', '$3$'],
      expl=['Match the $x$ terms: multiply the first equation by $3$ and the second by $2$: $6x+9y=57$ and $6x+4y=32$.',
            'Subtract: $5y=25$, therefore $y=5$.',
            'Put it into the first equation: $2x+15=19 \\to 2x=4 \\to x=2$. The answer is choice 2.'])
    S('alg-extra-unit-t6-2-2', stem=given_sys('2x+3y=24', '3x+2y=21', ask='y'), choices=['$8$', '$6$', '$5$', '$7$'],
      expl=['Match the $x$ terms: multiply the first equation by $3$ and the second by $2$: $6x+9y=72$ and $6x+4y=42$.',
            'Subtract: $5y=30$, therefore $y=6$. The answer is choice 2.',
            'Check: $2x+18=24$ gives $x=3$, and $3\\cdot3+2\\cdot6=21$.'])
    S('alg-extra-unit-t6-2-5', stem=given_sys('2x+3y=39', '3x+2y=36', ask='2x+y'), choices=['$21$', '$20$', '$22$', '$23$'],
      expl=['Multiply the first equation by $3$ and the second by $2$: $6x+9y=117$ and $6x+4y=72$.',
            'Subtract: $5y=45$, therefore $y=9$. Then $2x+27=39$, therefore $x=6$.',
            '$2x+y=12+9=21$. The answer is choice 1.'])
    S('alg-extra-unit-t6-2-6', stem=given_sys('2x+3y=44', '3x+2y=41', ask='xy'), choices=['$70$', '$69$', '$71$', '$72$'],
      expl=['Multiply the first equation by $3$ and the second by $2$: $6x+9y=132$ and $6x+4y=82$.',
            'Subtract: $5y=50$, therefore $y=10$. Then $2x+30=44$, therefore $x=7$.',
            '$xy=7\\cdot10=70$. The answer is choice 1.'])
    S('alg-extra-unit-t6-2-7', stem=given_sys('2x+3y=49', '3x+2y=46', ask='x^2+y^2'), choices=['$187$', '$185$', '$184$', '$186$'],
      expl=['Multiply the first equation by $3$ and the second by $2$: $6x+9y=147$ and $6x+4y=92$.',
            'Subtract: $5y=55$, therefore $y=11$. Then $2x+33=49$, therefore $x=8$.',
            '$x^2+y^2=64+121=185$. The answer is choice 2.'])
    S('q-141', stem=given_eq('\\frac{x+3}{4}=5'),
      expl=['Multiply both sides by $4$: $x+3=20$.', 'Subtract $3$: $x=17$. The answer is choice 2.'])
    S('alg-extra-unit-t6-1-1', stem=given_eq('5x+7=52'), choices=['$7$', '$8$', '$10$', '$9$'],
      expl=['Subtract $7$ from both sides: $5x=45$.', 'Divide by $5$: $x=9$. The answer is choice 4.'])
    S('alg-extra-unit-t6-1-2', stem=given_sys('x+y=13', 'x-y=3'), choices=['$5$', '$6$', '$7$', '$8$'],
      expl=['Add the two equations: the $y$ terms cancel, and $2x=16$.', 'Therefore $x=8$. The answer is choice 4.',
            'Shortcut: $x$ is half the sum: $\\frac{13+3}{2}=8$.'])
    S('alg-extra-unit-t6-1-3', stem=given_sys('2x+3y=31', '3x+2y=29', ask='x+y'), choices=['$12$', '$11$', '$13$', '$14$'],
      expl=['They ask for $x+y$, therefore add the equations: $(2x+3y)+(3x+2y)=31+29$.',
            '$5x+5y=60$, therefore $5(x+y)=60$ and $x+y=12$. The answer is choice 1.'])

    # =====================================================================================
    # 3. Lesson 1: Equations — Fundamentals
    # =====================================================================================
    M.edit_lines(LE, 2, draw_fix('Write ":4" on both sides', 'Write "÷4" on both sides'))

    cross = dict(title='Cross-multiply', mode='question', active=4,
                 pre=[T('$\\frac{3}{x+1}=\\frac{2}{x-1}$', size=72, gap=40)],
                 script=[
                     'When the equation is one fraction equal to one fraction, there is a shortcut: cross-multiply.',
                     D('Next to it write "x ≠ −1, x ≠ 1"'),
                     'But first, as always, the restriction. x can\'t be negative one, and it can\'t be one.',
                     D('Draw two crossing arrows: 3 to (x − 1), and 2 to (x + 1)'),
                     'Top left times bottom right equals top right times bottom left.',
                     D('Write "3(x − 1) = 2(x + 1)"'),
                     'Three times x minus one equals two times x plus one.',
                     D('Write "3x − 3 = 2x + 2 → x = 5"'),
                     'Three x minus three equals two x plus two. x equals five.',
                     D('Write "3/6 = 1/2,  2/4 = 1/2 ✓"'),
                     'Five is allowed. Three sixths is a half. Two quarters is a half. It checks.',
                     'This is the same as multiplying both sides by both denominators. It is just faster.',
                     A('Condition appears', T('Only when: one fraction $=$ one fraction', size=42)),
                     'One condition: exactly one fraction on each side, and nothing else.',
                     'If there is a plus or a minus outside the fractions, don\'t cross-multiply yet. Use a common denominator.',
                 ])
    forbidden = dict(title='Forbidden answer', mode='question', active=5,
                     pre=[T('$\\frac{x}{x-2}=\\frac{2}{x-2}$', size=72, gap=40)],
                     script=[
                         'Now watch what happens when the answer is forbidden.',
                         D('Next to it write "x ≠ 2"'),
                         'Restriction first: x can\'t be two.',
                         D('Cross out both denominators; write "x = 2"'),
                         'Same denominator on both sides. Cancel it. We get x equals two.',
                         D('Circle "x ≠ 2" and write a big ✗ next to "x = 2"'),
                         'But two is forbidden! At x equals two, both denominators are zero.',
                         D('Write "no solution"'),
                         'So this equation has NO solution.',
                         'On the test, two will be one of the choices. It is the trap.',
                         'That\'s why we write the restriction first: so we notice.',
                     ])
    M.insert_slides(LE, 5, [cross, forbidden])          # new slides 6, 7; old 6 -> 8, 7 -> 9, 8 -> 10
    M.set_slide(LE, 8, active=6)
    minus = dict(title='Minus before a fraction', mode='question', active=7,
                 pre=[T('$\\frac{x+1}{2}-\\frac{x-3}{5}=2$', size=68, gap=40)],
                 script=[
                     'Two fractions, with a minus between them. This is where most sign mistakes happen.',
                     'The common denominator of two and five is ten. Multiply EVERY term by ten.',
                     D('Write "5(x + 1) − 2(x − 3) = 20"'),
                     'Ten over two is five: five times x plus one. Ten over five is two: two times x minus three. And two times ten is twenty.',
                     'See the brackets? Put every numerator in brackets before you multiply.',
                     D('Circle "− 2(x − 3)" and write "= −2x + 6"'),
                     'Here\'s the trap. The minus hits the WHOLE numerator. Minus two times minus three is PLUS six.',
                     D('Write "5x + 5 − 2x + 6 = 20 → 3x + 11 = 20 → x = 3"'),
                     'Five x plus five, minus two x, plus six, equals twenty. Three x plus eleven is twenty. x equals three.',
                     D('Write "4/2 − 0/5 = 2 ✓"'),
                     'Check: four over two is two, minus zero. It works.',
                     'Write minus six there instead, and you get x equals seven. That wrong answer will be one of the choices.',
                 ])
    M.insert_slides(LE, 8, [minus])                     # new 9; don't-divide -> 10, recap -> 11
    M.set_slide(LE, 10, active=8)
    test = dict(title='Test the choices', mode='question', active=9,
                pre=[T('$\\frac{6}{x-1}=x-2$', size=68, gap=40)],
                script=[
                    'One more tool. On the test, it is often the fastest one.',
                    'The answers are numbers. So put each choice into the equation, and see which one works.',
                    A('Choices appear', T('(1) $1$  (2) $2$  (3) $3$  (4) $4$', size=50)),
                    D('Cross out choice 1; write "x ≠ 1"'),
                    'Choice one: x equals one makes the denominator zero. Forbidden. Out, with no work.',
                    D('Next to choice 2 write "6/1 = 6,  2 − 2 = 0 ✗"'),
                    'Choice two: six over one is six. Two minus two is zero. Not equal.',
                    D('Next to choice 3 write "6/2 = 3,  3 − 2 = 1 ✗"'),
                    'Choice three: three against one. No.',
                    D('Next to choice 4 write "6/3 = 2,  4 − 2 = 2 ✓"'),
                    'Choice four: two and two. That\'s the answer.',
                    'We never solved the equation. We don\'t even know how to solve this one yet. The choices still gave us the answer.',
                    'Tip: start with the choice that is easiest to compute. And skip any forbidden value.',
                ])
    M.insert_slides(LE, 10, [test])                     # new 11; recap -> 12
    M.set_slide(LE, 12, active=10, script=[
        'Let\'s lock it in.',
        A("'Same operation on both sides' appears", T('Same operation on both sides', size=40)),
        A("'x cancels' appears", T('$x$ cancels: true $\\to$ infinitely many solutions, false $\\to$ none', size=38)),
        A("'restriction first' appears", T('$x$ in the denominator $\\to$ restriction first; a forbidden answer is out', size=38)),
        A("'cross-multiply' appears", T('One fraction $=$ one fraction $\\to$ cross-multiply', size=38)),
        A("'minus before a fraction' appears", T('Minus before a fraction $\\to$ numerator in brackets', size=38)),
        A("'never divide by 0' appears", T('Never divide by something that could be $0$', size=38)),
        A("'test the choices' appears", T('Number choices $\\to$ you can test them', size=38)),
        D('Underline "both sides"'),
        'Next: three questions. Try each one first. Then watch the solution.',
    ])
    M.set_sidebar(LE, ['Isolate x', 'Every x works', 'No solution', 'x in the denominator', 'Cross-multiply',
                       'Forbidden answer', 'Fractions & brackets', 'Minus before a fraction', "Don't divide by x",
                       'Test the choices', 'Recap'])

    # =====================================================================================
    # 4. Lesson 2: Systems of Equations
    # =====================================================================================
    M.set_slide(SY, 2, script=[
        A('x + y = 11 appears', T(cases('x+y=11', '2x-y=7'), size=62, gap=40)),
        'Two unknowns, two equations. We need values that make BOTH true at the same time.',
        'The first one alone has endless pairs. The second one narrows it down to one.',
        D('Next to them write "2 unknowns, 2 equations"'),
        'Rule of thumb: as many equations as unknowns, and USUALLY you can solve it.',
        'Usually, not always. In the next topic you\'ll see systems with no solution, or with endless solutions.',
        'Two main methods: substitution, and elimination. Same answer either way.',
    ])
    for n in (3, 4):
        M.set_slide(SY, n, pre=[T(cases('x+y=11', '2x-y=7'), size=62, gap=40)])
    M.edit_lines(SY, 4, lambda ls: [l for l in ls if not l.get('say', '').startswith('Same sign instead of opposite')])
    M.edit_lines(SY, 4, lambda ls: ls + [{'say': 'Same sign instead of opposite signs? Then subtract. The next slide shows how.'}])
    M.set_slide(SY, 5, pre=[T(cases('2x+3y=19', '3x+2y=16'), size=60, gap=40)])
    addsub = dict(title='Add and subtract', mode='question', active=3,
                  pre=[T(cases('x+y=10', 'x-y=4'), size=62, gap=40)],
                  script=[
                      'A very common pair: x plus y, and x minus y.',
                      D('Write "(x + y) + (x − y) = 10 + 4 → 2x = 14 → x = 7"'),
                      'Add them. The y terms cancel. Two x is fourteen. x is seven.',
                      D('Write "(x + y) − (x − y) = 10 − 4"'),
                      'Now subtract, to get y. Put the WHOLE second equation in brackets.',
                      D('Under it write "x + y − x + y = 6 → 2y = 6 → y = 3"'),
                      'The minus flips both signs inside the bracket: minus x, and PLUS y.',
                      'So y minus negative y is two y. Two y is six. y is three.',
                      'Without the brackets you would write y minus y, get zero, and get stuck.',
                      A('Shortcut appears', T('$x=\\dfrac{\\text{sum}}{2}$, $\\ y=\\dfrac{\\text{difference}}{2}$', size=44)),
                      'The shortcut: x is half the sum of the two numbers. y is half the difference.',
                      'Ten plus four, halved: seven. Ten minus four, halved: three.',
                  ])
    M.insert_slides(SY, 4, [addsub])                    # new 5; match -> 6, ask -> 7, recap -> 8
    M.set_slide(SY, 6, active=4)
    M.set_slide(SY, 7, active=5)
    direct = dict(title='Get x + y directly', mode='question', active=6,
                  pre=[T(cases('3x+y=17', 'x+3y=11'), size=62, gap=40)],
                  script=[
                      'Say they ask for x plus y.',
                      D('Write "(3x + y) + (x + 3y) = 17 + 11"'),
                      'Add the equations: left to left, right to right.',
                      D('Write "4x + 4y = 28 → x + y = 7"'),
                      'Four x plus four y is twenty-eight. Divide by four: x plus y is seven. Done.',
                      'And if they ask for x minus y?',
                      D('Write "(3x + y) − (x + 3y) = 17 − 11 → 2x − 2y = 6 → x − y = 3"'),
                      'Subtract: two x minus two y is six. So x minus y is three.',
                      'We never found x or y. We did not need them.',
                      'When the numbers look symmetric like this, try adding and subtracting first.',
                  ])
    mult = dict(title='Multiply equations', mode='question', active=7,
                pre=[T('$x>0,\\ y>0$', size=44, gap=20), T(cases('xy=12', '\\frac{x}{y}=3'), size=62, gap=40)],
                script=[
                    'A product and a quotient. Adding won\'t help here. But multiplying will.',
                    D('Write "xy · (x/y) = 12 · 3"'),
                    'Multiply the equations: left times left, right times right.',
                    D('Write "x² = 36 → x = 6"'),
                    'The y cancels. x squared is thirty-six. x is positive, so x is six.',
                    D('Write "xy ÷ (x/y) = 12 ÷ 3 → y² = 4 → y = 2"'),
                    'Or divide them: x y divided by x over y is y squared. Twelve divided by three is four. y is two.',
                    D('Write "6 · 2 = 12 ✓,  6/2 = 3 ✓"'),
                    'Check: six times two is twelve. Six over two is three.',
                    'Why do they tell us x and y are positive? Because negative six also squares to thirty-six.',
                ])
    M.insert_slides(SY, 7, [direct, mult])              # new 8, 9; recap -> 10
    M.set_slide(SY, 10, active=8, script=[
        'Let\'s lock it in. Which method when?',
        A("'coefficient 1' appears", T('A letter with coefficient $1$ $\\to$ substitution', size=40)),
        A("'same or opposite' appears", T('Same or opposite coefficients $\\to$ subtract or add', size=40)),
        A("'multiply WHOLE' appears", T('No match $\\to$ multiply WHOLE equations to match coefficients', size=40)),   # pass 2: original line
        A("'combination' appears", T('They ask for $x+y$ or $x-y$ $\\to$ add or subtract first', size=40)),
        A("'product' appears", T('$xy$ and $\\frac{x}{y}$ $\\to$ multiply or divide the equations', size=40)),
        D('Underline "WHOLE"'),
        'Four system questions next. Try each one. Then watch how we solve it.',
    ])
    M.set_sidebar(SY, ['Two equations', 'Substitution', 'Elimination', 'Add and subtract', 'Match coefficients',
                       'Ask what they want', 'Get x + y directly', 'Multiply equations', 'Recap'])

    # --- existing solution videos ---
    M.edit_lines('solve-q-164', 2, draw_fix('as many equations as unknowns, so we can solve it',
                                            'as many equations as unknowns, so we can usually solve it'))
    M.edit_lines('solve-q-164', 3, draw_fix('":3 → 2x + y = 12"', '"÷3 → 2x + y = 12"'))

    # =====================================================================================
    # 5. New guided questions + solution videos
    # =====================================================================================
    def guided(qid, section, after, stem, choices, correct, expl, intro, slides, group, sidebar, active):
        M.new_q(qid, TOPIC, stem, choices, correct, expl)
        M.place_q(qid, section, after=after)
        n = M.next_question_number(TOPIC)
        sl = [dict(mode='title', title='Question %d' % n, script=intro)]
        for title, script in slides:
            sl.append(dict(mode='question', active=active, title=title, pre=[Q(qid)], script=script))
        v = M.new_video('solve-' + qid, TOPIC, group, sidebar or [], sl, section, kind='solution', qid=qid)
        v['title'] = v['navLabel'] = rich_plain(stem)
        v['beats'][0]['title'] = group   # like the base videos; keeps renumbering single-pass (bigTitle shows the number)
        return n

    q1 = 'q-r26-t06-01'
    n1 = guided(q1, 'single-equation', 'solve-q-171',
                given_eq('\\frac{x+2}{3}-\\frac{x-4}{6}=\\frac{x}{2}'),
                ['$0$', '$2$', '$4$', '$8$'], 3,
                ['The common denominator of $3$, $6$ and $2$ is $6$. Multiply every term by $6$ and put each numerator in brackets:',
                 '$2(x+2)-(x-4)=3x$.',
                 'The minus hits the whole bracket: $2x+4-x+4=3x$.',
                 '$x+8=3x \\to 8=2x \\to x=4$.',
                 'Check: $\\frac{6}{3}-\\frac{0}{6}=2$ and $\\frac{4}{2}=2$. The answer is choice 3.',
                 'The trap: writing $-x-4$ gives $x=0$ (choice 1).'],
                ['A fraction equation, with a minus in front of a fraction.', 'This is where most points are lost. Watch the signs.'],
                [('Method 1 · Common denominator', [
                    'The denominators are three, six and two. The smallest number all three go into is six.',
                    D('Write "×6" next to every term'),
                    'Multiply every term by six.',
                    D('Write "2(x + 2) − (x − 4) = 3x"'),
                    'Six over three is two: two times x plus two. Six over six is one: minus ONE times x minus four. Six over two is three: three x.',
                    'Look at the middle term. The minus belongs to the whole bracket.',
                    D('Write "2x + 4 − x + 4 = 3x"'),
                    'Minus times minus four is PLUS four.',
                    D('Write "x + 8 = 3x → 8 = 2x → x = 4"'),
                    'x plus eight equals three x. Eight equals two x. x equals four.',
                    D('Circle choice 3'),
                    'Choice three.',
                    'If you wrote minus four there, you got x equals zero. That\'s choice one: the trap.',
                ]), ('Method 2 · Test the choices', [
                    'Or test the choices. Choice three, x equals four, is quick: x minus four becomes zero.',
                    D('Next to choice 3 write "6/3 − 0/6 = 2,  4/2 = 2 ✓"'),
                    'Six over three is two, minus zero. Right side: four over two is two. Equal.',
                    D('Circle choice 3'),
                    'Choice three again. A choice that makes a term zero is fast to test, so try it first.',
                ])],
                'Equation Questions', None, 1)
    q2 = 'q-r26-t06-02'
    n2 = guided(q2, 'single-equation', 'solve-' + q1,
                given_eq('\\frac{2x+1}{x-2}=\\frac{x+3}{x-2}'),
                ['$-2$', '$2$', '$4$', 'No value of $x$ satisfies the equation'], 4,
                ['$x$ is in the denominator, so first the restriction: $x \\ne 2$.',
                 'Both sides have the same denominator, so cancel it: $2x+1=x+3$, so $x=2$.',
                 'But $x=2$ is forbidden (both denominators would be $0$). So no value of $x$ satisfies the equation. The answer is choice 4.',
                 'Testing the choices gives the same result: $x=-2$ gives $\\frac{3}{4} \\ne -\\frac{1}{4}$, and $x=4$ gives $\\frac{9}{2} \\ne \\frac{7}{2}$.'],
                ['A short equation. But read the choices carefully.'],
                [('Method 1 · Restriction first', [
                    'x is in the denominator. So first: the restriction.',
                    D('Next to the equation write "x ≠ 2"'),
                    'x minus two can\'t be zero. So x can\'t be two.',
                    D('Cross out both denominators; write "2x + 1 = x + 3"'),
                    'Same denominator on both sides. Cancel it.',
                    D('Write "x = 2"'),
                    'Two x plus one equals x plus three. x equals two.',
                    D('Cross out choice 2'),
                    'But two is forbidden! Both denominators would be zero.',
                    D('Circle choice 4'),
                    'The algebra gave only one number, and it is forbidden. So there is no solution. Choice four.',
                    'Choice two is the trap. It is exactly the number the algebra gives you.',
                ]), ('Method 2 · Test the choices', [
                    D('Cross out choice 2'),
                    'Choice two: forbidden. Out.',
                    D('Next to choice 1 write "(−3)/(−4) = 3/4,  1/(−4) = −1/4 ✗"'),
                    'Choice one, x equals negative two. Left side: three quarters. Right side: negative one quarter. Not equal.',
                    D('Next to choice 3 write "9/2 ≠ 7/2 ✗"'),
                    'Choice three, x equals four. Nine halves against seven halves. No.',
                    D('Circle choice 4'),
                    'No number works. Choice four.',
                ])],
                'Equation Questions', None, 2)
    sb1 = ['Question 1', 'Question %d' % n1, 'Question %d' % n2]
    for vid in ('solve-q-171', 'solve-' + q1, 'solve-' + q2):
        M.set_sidebar(vid, sb1)
        M.video(vid)['hybrid']['title'] = 'Equation Questions'
        M.video(vid)['hybrid']['num'] = M.video('solve-q-171')['hybrid']['num']

    q3 = 'q-r26-t06-03'
    n3 = guided(q3, 'systems-study', 'solve-q-165',
                given_sys('5x+3y=41', '3x+5y=39', ask='x+y'),
                ['$1$', '$8$', '$10$', '$80$'], 3,
                ['They ask for $x+y$, so add the equations: $(5x+3y)+(3x+5y)=41+39$.',
                 '$8x+8y=80$, so $8(x+y)=80$ and $x+y=10$. The answer is choice 3.',
                 'Solving fully works too, but it is slow: $x=5.5$ and $y=4.5$.',
                 'Traps: $80$ (forgot to divide by $8$), and $1$ (that is $x-y$, from subtracting).'],
                ['They ask for x plus y. Circle it, before anything else.'],
                [('Method 1 · Add the equations', [
                    D('Circle "x + y"'),
                    'They want x plus y. Not x, and not y.',
                    D('Write "(5x + 3y) + (3x + 5y) = 41 + 39"'),
                    'Add the two equations. Left to left, right to right.',
                    D('Write "8x + 8y = 80"'),
                    'Five x plus three x: eight x. Three y plus five y: eight y. Forty-one plus thirty-nine: eighty.',
                    D('Write "8(x + y) = 80 → x + y = 10"'),
                    'Take out the eight: eight times x plus y is eighty. So x plus y is ten.',
                    D('Circle choice 3'),
                    'Choice three.',
                    'Choice four is eighty. That\'s what you get if you forget to divide by eight.',
                ]), ('Method 2 · The long way', [
                    'Could we find x and y? Yes. But look how long it takes.',
                    D('Write "×3: 15x + 9y = 123   ×5: 15x + 25y = 195"'),
                    'Match the x terms: the first equation times three, the second times five.',
                    D('Write "16y = 72 → y = 4.5"'),
                    'Subtract: sixteen y is seventy-two. y is four and a half.',
                    D('Write "5x + 13.5 = 41 → x = 5.5 → x + y = 10"'),
                    'Back in: five x is twenty-seven and a half. x is five and a half. Add them: ten.',
                    D('Circle choice 3'),
                    'Same answer. But big numbers and decimals. Adding first took one line.',
                ])],
                'Systems Questions', None, 2)
    q4 = 'q-r26-t06-04'
    n4 = guided(q4, 'systems-study', 'solve-' + q3,
                'Given: $x > 0$ and $y > 0$, and\n' + cases('xy=20', '\\frac{x}{y}=5') + '\n$x-y = ?$',
                ['$2$', '$4$', '$8$', '$10$'], 3,
                ['Multiply the two equations: $xy\\cdot\\frac{x}{y}=20\\cdot5$, so $x^2=100$.',
                 '$x$ is positive, so $x=10$. Then $10y=20$, so $y=2$.',
                 '$x-y=10-2=8$. The answer is choice 3.',
                 'Or substitute: $\\frac{x}{y}=5$ gives $x=5y$, so $5y^2=20$, $y^2=4$ and $y=2$.'],
                ['A product and a quotient. There is a shortcut here.'],
                [('Method 1 · Multiply the equations', [
                    'Look at the two left sides: x times y, and x over y.',
                    D('Write "xy · (x/y) = 20 · 5"'),
                    'Multiply the equations: left times left, right times right.',
                    D('Write "x² = 100 → x = 10"'),
                    'The y cancels. x squared is one hundred. x is positive, so x is ten.',
                    D('Write "10y = 20 → y = 2"'),
                    'Back into x y equals twenty: y is two.',
                    D('Write "x − y = 10 − 2 = 8" and circle choice 3'),
                    'x minus y is eight. Choice three.',
                ]), ('Method 2 · Substitution', [
                    D('Write "x/y = 5 → x = 5y"'),
                    'Or: x over y is five, so x is five y.',
                    D('Write "5y · y = 20 → y² = 4 → y = 2"'),
                    'Put it into the product: five y squared is twenty. y squared is four. y is positive, so y is two.',
                    D('Write "x = 10,  x − y = 8" and circle choice 3'),
                    'x is ten, and x minus y is eight. Choice three.',
                    'Why are we told that x and y are positive? Because x squared equals one hundred also allows negative ten.',
                ])],
                'Systems Questions', None, 3)
    sb2 = ['Question 2', 'Question 3', 'Question %d' % n3, 'Question %d' % n4]
    for vid in ('solve-q-164', 'solve-q-165', 'solve-' + q3, 'solve-' + q4):
        M.set_sidebar(vid, sb2)
        M.video(vid)['hybrid']['num'] = M.video('solve-q-164')['hybrid']['num']
    for vid in ('solve-' + q3, 'solve-' + q4):
        M.video(vid)['hybrid']['title'] = 'Systems Questions'
    for vid, q in (('solve-q-171', 'q-171'), ('solve-q-164', 'q-164'), ('solve-q-165', 'q-165')):
        M.video(vid)['title'] = M.video(vid)['navLabel'] = rich_plain(M.q(q)['stemRich'])

    # =====================================================================================
    # 6. New practice questions
    # =====================================================================================
    def P(k, section, stem, choices, correct, expl):
        qid = 'q-r26-t06-%02d' % k
        M.new_q(qid, TOPIC, stem, choices, correct, expl)
        M.place_q(qid, section)
        return qid

    NA = 'No value of $x$ satisfies the equation'
    # single-equation practice
    p05 = P(5, 'unit-t6-4', 'Given: $x \\ne -2$ and $x \\ne 2$.\n$\\frac{5}{x+2}=\\frac{3}{x-2}$\n$x = ?$',
            ['$-8$', '$2$', '$4$', '$8$'], 4,
            ['One fraction equals one fraction, so cross-multiply: $5(x-2)=3(x+2)$.',
             '$5x-10=3x+6 \\to 2x=16 \\to x=8$.',
             'Check: $\\frac{5}{10}=\\frac{1}{2}$ and $\\frac{3}{6}=\\frac{1}{2}$.',
             'The trap: multiplying straight across ($5(x+2)=3(x-2)$) gives $-8$.'])
    p06 = P(6, 'unit-t6-4', given_eq('\\frac{x}{2}-\\frac{x-6}{4}=3'),
            ['$3$', '$6$', '$12$', '$18$'], 2,
            ['Multiply every term by $4$ and put each numerator in brackets: $2x-(x-6)=12$.',
             'The minus hits the whole bracket: $2x-x+6=12$, so $x+6=12$ and $x=6$.',
             'Check: $\\frac{6}{2}-\\frac{0}{4}=3$.',
             'The trap: $2x-x-6=12$ gives $x=18$.'])
    p07 = P(7, 'unit-t6-4', 'Which of the following numbers is a solution of the equation $\\frac{12}{x}=x+1$?',
            ['$0$', '$2$', '$3$', '$4$'], 3,
            ['Test the choices in the equation.',
             '$x=0$ is forbidden (it makes the denominator $0$).',
             '$x=2$: $\\frac{12}{2}=6$ and $2+1=3$. Not equal.',
             '$x=3$: $\\frac{12}{3}=4$ and $3+1=4$. Equal, so the answer is choice 3.',
             '($x=4$: $\\frac{12}{4}=3$ and $4+1=5$. Not equal.)'])
    p08 = P(8, 'unit-t6-4', 'For what value of $a$ does the equation $3(x+a)=3x+12$ have infinitely many solutions?',
            ['$3$', '$4$', '$12$', 'For every value of $a$'], 2,
            ['Open the bracket: $3x+3a=3x+12$.',
             'Take $3x$ off both sides: $3a=12$.',
             'If $a=4$, this is $12=12$: always true, so every $x$ is a solution.',
             'For any other $a$ it is false, and there is no solution.'])
    p09 = P(9, 'unit-t6-4', given_eq('\\frac{x}{x-3}=2+\\frac{3}{x-3}'),
            ['$0$', '$3$', '$5$', NA], 4,
            ['Restriction: $x \\ne 3$.',
             'There is a $+2$ outside the fractions, so do not cross-multiply. Multiply every term by $x-3$: $x=2(x-3)+3$.',
             '$x=2x-6+3 \\to x=2x-3 \\to x=3$.',
             'But $x=3$ is forbidden. So no value of $x$ satisfies the equation. The answer is choice 4.'])
    p10 = P(10, 'unit-t6-4', given_eq('\\frac{x-1}{3}-\\frac{x+1}{2}=\\frac{x}{6}-1'),
            ['$-2$', '$\\frac{1}{2}$', '$\\frac{7}{2}$', '$5$'], 2,
            ['Multiply every term by $6$ (including the $-1$) and put each numerator in brackets: $2(x-1)-3(x+1)=x-6$.',
             'The minus hits the whole bracket: $2x-2-3x-3=x-6$.',
             '$-x-5=x-6 \\to 1=2x \\to x=\\frac{1}{2}$.',
             'Traps: writing $-3x+3$ gives $\\frac{7}{2}$. Forgetting to multiply the $-1$ by $6$ gives $-2$.'])
    # systems practice
    p11 = P(11, 'unit-t6-2', given_sys('x+y=15', 'x-y=-3', ask='y'),
            ['$3$', '$6$', '$9$', '$12$'], 3,
            ['Subtract the second equation from the first. Keep it in brackets: $(x+y)-(x-y)=15-(-3)$.',
             '$2y=18$, so $y=9$.',
             'Shortcut: $y$ is half the difference: $\\frac{15-(-3)}{2}=9$.',
             'The trap: $15-3=12$ gives $y=6$, which is really $x$.'])
    p12 = P(12, 'unit-t6-2', given_sys('3x+2y=20', 'x+y=7', ask='2x+y'),
            ['$6$', '$7$', '$13$', '$27$'], 3,
            ['They ask for $2x+y$. Subtract the second equation from the first: $(3x+2y)-(x+y)=20-7$.',
             '$2x+y=13$.',
             'Check: $x=6$ and $y=1$ satisfy both equations, and $2\\cdot6+1=13$.'])
    p13 = P(13, 'unit-t6-2', given_sys('x(y+2)=24', 'x(y-1)=12', ask='y'),
            ['$2$', '$3$', '$4$', '$6$'], 3,
            ['Divide the first equation by the second: $\\frac{y+2}{y-1}=\\frac{24}{12}=2$.',
             'Multiply by $y-1$: $y+2=2y-2$, so $y=4$.',
             'Or subtract the equations: $x(y+2)-x(y-1)=3x=12$, so $x=4$, and $4(y+2)=24$ gives $y=4$.'])
    # mixed practice
    p14 = P(14, 'unit-t6-1', 'Given: $x \\ne y$, $y \\ne 0$ and\n$\\frac{x+y}{x-y}=3$\n$\\frac{x}{y} = ?$',
            ['$\\frac{1}{2}$', '$2$', '$3$', '$4$'], 2,
            ['Multiply both sides by $x-y$: $x+y=3(x-y)=3x-3y$.',
             'Collect: $4y=2x$, so $x=2y$.',
             '$\\frac{x}{y}=2$.',
             'Check with numbers: $x=2$, $y=1$ gives $\\frac{3}{1}=3$.'])
    p15 = P(15, 'unit-t6-1', 'How many solutions does the equation $\\frac{x-1}{x-1}=1$ have?',
            ['None', 'Exactly one: $x=1$', 'Every number except $1$', 'Every number'], 3,
            ['Restriction: $x \\ne 1$.',
             'For any other $x$, the numerator equals the denominator (and it is not $0$), so the fraction equals $1$. The equation is true.',
             'So every number except $1$ is a solution.'])
    p16 = P(16, 'unit-t6-1', 'Given: $3x-2y=5$\n$6x-4y+1 = ?$',
            ['$6$', '$10$', '$11$', 'Cannot be determined from the given information'], 3,
            ['We cannot find $x$ and $y$, but we do not need them.',
             '$6x-4y=2(3x-2y)=2\\cdot5=10$.',
             'So $6x-4y+1=11$.'])
    p17 = P(17, 'unit-t6-1', 'Given: $x$, $y$ and $z$ are positive, and\n' + cases('xy=6', 'yz=10', 'xz=15') + '\n$xyz = ?$',
            ['$15$', '$30$', '$31$', '$900$'], 2,
            ['Multiply the three equations: $(xy)(yz)(xz)=6\\cdot10\\cdot15$.',
             'The left side is $x^2y^2z^2=(xyz)^2$, and the right side is $900$.',
             '$xyz$ is positive, so $xyz=30$.',
             'Check: $x=3$, $y=2$, $z=5$.'])

    # =====================================================================================
    # 7. Practice order (easy -> hard)
    # =====================================================================================
    M.practice_order('unit-t6-4', ['alg-extra-unit-t6-4-1', 'q-166', 'alg-extra-unit-t6-4-2', 'alg-extra-unit-t6-4-4', 'q-167',
                                   'alg-extra-unit-t6-4-3', 'alg-extra-unit-t6-4-5', 'alg-extra-unit-t6-4-6', 'q-168',
                                   'q-169', 'q-170', 'alg-extra-unit-t6-4-7', p05, p06, p07, p08, p09, p10])
    M.practice_order('unit-t6-2', ['q-159', 'q-160', 'q-162', 'q-161', p11, 'q-163', 'alg-extra-unit-t6-2-1',
                                   'alg-extra-unit-t6-2-2', 'alg-extra-unit-t6-2-3', 'alg-extra-unit-t6-2-4',
                                   'alg-extra-unit-t6-2-5', 'alg-extra-unit-t6-2-6', 'alg-extra-unit-t6-2-7', p12, p13])
    M.practice_order('unit-t6-1', ['alg-extra-unit-t6-1-1', 'q-139', 'q-140', 'q-141', 'q-142', 'q-144', 'q-145',
                                   'alg-extra-unit-t6-1-2', 'q-146', 'q-147', 'q-148', 'q-149',
                                   'q-150', 'q-151', 'alg-extra-unit-t6-1-3', 'alg-extra-unit-t6-1-6', 'q-156', 'q-152', 'q-154',
                                   'alg-extra-unit-t6-1-5', 'q-155', 'q-158', p16, 'q-157', 'alg-extra-unit-t6-1-4',
                                   'q-153', p14, 'alg-extra-unit-t6-1-7', p15, 'q-143', p17])

    # =====================================================================================
    # 8. Memory cards
    # =====================================================================================
    M.new_card('mem-r26-t06-single', TOPIC, 'single-equation', {
        'title': 'Solving one equation',
        'intro': 'The moves that solve a linear equation, and the traps to watch.',
        'tables': [{'title': 'Moves', 'head': ['You see', 'Do this'], 'rows': [
            ['Numbers and $x$ on both sides', 'same operation on both sides; $x$ terms to one side, numbers to the other'],
            ['Brackets', 'multiply everything inside: $3(x-2)=3x-6$'],
            ['A number under a fraction', 'multiply every term by the common denominator'],
            ['Minus before a fraction', 'numerator in brackets: $\\frac{x+1}{2}-\\frac{x-3}{5}=2 \\to 5(x+1)-2(x-3)=20$'],
            ['$x$ in the denominator', 'write the restriction first; an answer that breaks it is out'],
            ['One fraction $=$ one fraction', 'cross-multiply: $\\frac{a}{b}=\\frac{c}{d} \\to ad=bc$'],
            ['$x$ cancels', 'true ($6=6$) $\\to$ infinitely many solutions; false ($6=9$) $\\to$ no solution'],
            ['A product $=0$', 'one of the factors is $0$; never divide by $x$'],
            ['Number choices', 'test them in the original equation; skip forbidden values'],
        ]}],
        'tips': ['Check your answer in the ORIGINAL equation.',
                 'Cross-multiply only when each side is one fraction and nothing else.',
                 '$-2(x-3)=-2x+6$, not $-2x-6$.'],
    }, after=LE)
    M.new_card('mem-r26-t06-systems', TOPIC, 'systems-study', {
        'title': 'Systems of equations: which method?',
        'intro': 'Look at the equations and at what they ask for. Then choose.',
        'tables': [{'title': 'Methods', 'head': ['You see', 'Do this'], 'rows': [
            ['A letter with coefficient $1$', 'substitution: isolate it, plug it in (in brackets)'],
            ['Same or opposite coefficients', 'subtract or add the equations'],
            ['$x+y=a$ and $x-y=b$', '$x=\\frac{a+b}{2}$, $y=\\frac{a-b}{2}$'],
            ['No matching coefficients', 'multiply WHOLE equations to match the letter they do not ask for'],
            ['They ask for $x+y$, $x-y$, $2x+y$ …', 'add or subtract first; you may not need $x$ and $y$'],
            ['$xy$ and $\\frac{x}{y}$', 'multiply or divide the equations'],
        ]}],
        'tips': ['Subtracting an equation: put the whole equation in brackets: $(x+y)-(x-y)=2y$.',
                 'As many equations as unknowns usually, but not always, gives one solution.'],
    }, after=SY)

    summaries(M)
    new_numbers(M)
    order_changes(M)
    dedupe_examples(M)   # 2026-10-04: runs last


# =====================================================================================
# 9. Pass 2: a summary lesson right before each practice block
# =====================================================================================
def _summary(M, vid, section, title, sb, bodies, intro):
    slides = [dict(mode='title', title='Summary', script=intro)]
    for k, script in enumerate(bodies):
        slides.append(dict(title=sb[k], mode='concept', active=k, pre=[], script=script))
    last = [f['ref'] for f in M.D['flow'] if f['section'] == section][-1]
    M.new_video(vid, TOPIC, title, sb, slides, section, after=last)


def summaries(M):
    # --- before "Single-equation practice": everything in "Equations — Fundamentals" ---
    _summary(M, 'r26-t06-summary', 'single-equation', 'Summary: One Equation',
             ['Same on both sides', 'Brackets and fractions', 'Minus before a fraction', 'x cancels',
              'x in the denominator', 'Cross-multiply', "Don't divide by x", 'Test the choices', 'Before you practice'], [
        [A('3x + 8 = 35 appears', T('$3x+8=35 \\to 3x=27 \\to x=9$', size=50)),
         'The golden rule: whatever you do to one side, do to the other.',
         'Get x alone. Minus eight on both sides, then divide both sides by three.',
         A('Check appears', T('Check: $3\\cdot9+8=35$ ✓', size=46)),
         'Then check your answer in the ORIGINAL equation.'],
        [A('Brackets appear', T('$4(x-5)=4x-20$', size=52)),
         'The number before a bracket multiplies EVERYTHING inside.',
         A('Fraction appears', T('$\\frac{x+5}{3}=4 \\to x+5=12 \\to x=7$', size=50)),
         'A number under a fraction? Multiply every term by the common denominator.',
         'The three divides the WHOLE top. x plus five is twelve — not x plus fifteen.'],
        [A('Minus rule appears', T('$\\frac{x+4}{3}-\\frac{x-2}{4}=1 \\to 4(x+4)-3(x-2)=12$', size=42)),
         'A minus before a fraction? Put the numerator in brackets first.',
         A('Sign appears', T('$-3(x-2)=-3x+6$', size=52)),
         'The minus hits the whole numerator. Minus times minus is plus.'],
        [A('True appears', T('$4=4$ → infinitely many solutions', size=46)),
         'Sometimes x cancels out. Look at what is left.',
         'Always true? Every x works — infinitely many solutions.',
         A('False appears', T('$4=7$ → no solution', size=46)),
         'Always false? No x works — no solution.'],
        [A('Restriction appears', T('$\\frac{x+1}{x-4}=3$, $x\\ne4$', size=52)),
         'x in the denominator? Write the restriction FIRST.',
         'The denominator can never be zero.',
         A('Forbidden appears', T('A forbidden answer is out → maybe no solution', size=44)),
         'If the algebra gives a forbidden number, throw it out. If nothing is left — no solution.'],
        [A('Cross-multiply appears', T('$\\frac{a}{b}=\\frac{c}{d} \\to ad=bc$', size=54)),
         'One fraction equals one fraction? Cross-multiply.',
         A('Condition appears', T('Only when: one fraction $=$ one fraction', size=44)),
         'A plus or a minus outside the fractions? Use a common denominator instead.'],
        [A('x(x − 8) = 0 appears', T('$x(x-8)=0 \\to x=0$ or $x=8$', size=50)),
         'Never divide by something that could be zero.',
         'A product is zero when one of the factors is zero. Keep both solutions.'],
        [A('Test appears', T('Number choices → put each one into the equation', size=44)),
         'The choices are numbers? You can test them.',
         'Start with the easiest one. Skip any forbidden value — it is out without any work.'],
        ['Before you start, always ask yourself:',
         A('Check 1 appears', T('Is $x$ in a denominator? What is forbidden?', size=42)),
         A('Check 2 appears', T('Is there a minus before a bracket or a fraction?', size=42)),
         A('Check 3 appears', T('One fraction on each side? Then cross-multiply.', size=42)),
         A('Check 4 appears', T('Did I check the answer in the original equation?', size=42)),
         'The common traps: a lost minus, a forbidden answer, and dividing by x.',
         "Now it's your turn. Good luck!"],
    ], ['Before you practice — a quick summary of solving one equation.', 'The moves, and the traps.'])

    # --- before "Systems practice": everything in "Systems of Equations" ---
    _summary(M, 'r26-t06-summary-2', 'systems-study', 'Summary: Systems of Equations',
             ['Two equations', 'Substitution', 'Add or subtract', 'Match coefficients', 'Ask what they want',
              'Multiply equations', 'Before you practice'], [
        [A('System appears', T(cases('x+y=8', '3x-y=12'), size=56, gap=30)),
         'Two unknowns, two equations. We need values that make BOTH true.',
         'As many equations as unknowns — usually, not always, one solution.'],
        [A('Substitution appears', T('$y=8-x \\to 3x-(8-x)=12$', size=50)),
         'A letter with coefficient one? Isolate it and put it into the other equation.',
         'Put the WHOLE expression in brackets. The minus hits both terms.'],
        [A('Add appears', T(cases('x+y=16', 'x-y=2'), size=56, gap=30)),
         'Opposite coefficients? Add the equations. The same coefficients? Subtract.',
         A('Shortcut appears', T('$x=\\frac{16+2}{2}=9$, $\\ y=\\frac{16-2}{2}=7$', size=48)),
         'x plus y and x minus y: x is half the sum, y is half the difference.',
         'Subtracting? Put the whole second equation in brackets.'],
        [A('Match appears', T('×3 and ×2 → $6x+15y=72$, $\\ 6x+8y=44$', size=46)),
         'Nothing cancels? Multiply WHOLE equations to match coefficients.',
         'Every term gets multiplied — the right side too.',
         'Match the letter they do NOT ask for. Use the smallest multipliers.'],
        [A('Combination appears', T('$(4x+y)+(x+4y)=14+11 \\to x+y=5$', size=46)),
         'Circle what they ask for — before you start.',
         'They ask for x plus y, or x minus y? Add or subtract first. You may not need x and y at all.'],
        [A('Multiply appears', T('$xy\\cdot\\frac{x}{y}=27\\cdot3 \\to x^2=81$', size=50)),
         'A product and a quotient? Multiply or divide the equations.',
         'x squared is eighty-one. x is positive — therefore x is nine.'],
        ['Before you start, always ask yourself:',
         A('Check 1 appears', T('What do they ask for: $x$, $y$ or a combination?', size=42)),
         A('Check 2 appears', T('A coefficient $1$? Same or opposite coefficients?', size=42)),
         A('Check 3 appears', T('Did I multiply the WHOLE equation?', size=42)),
         A('Check 4 appears', T('Did I use brackets when I subtracted?', size=42)),
         'The common traps: a lost minus when you subtract, and forgetting the right side.',
         "Now it's your turn. Good luck!"],
    ], ['Before you practice — a quick summary of systems of equations.', 'Which method, and when.'])


# =====================================================================================
# 10. 2026-10-02: new numbers - the English course is not identical to the Hebrew one (same ideas, same methods)
# =====================================================================================
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

    def video(qid, slides):
        if qid in RECORDED: return
        vid = 'solve-' + qid
        for n, x in slides.items():
            title, script = x if isinstance(x, tuple) else (None, x)
            M.set_slide(vid, n, title=title, script=script)
        v = M.video(vid)
        v['title'] = v['navLabel'] = rich_plain(M.q(qid)['stemRich'])

    NA = 'No value of $x$ satisfies the equation'

    # ---------------- lesson "Equations — Fundamentals": the Hebrew's own examples get new numbers
    # Hebrew: 2x² + 6 = 2(x² + 3) (every x) and 4x − 5 = 2x + 2(x − 3) (no solution); English had 2(x+3) = 2x+6 / 2x+9.
    # The two slides also swap places (no solution first) - see order_changes; here only the numbers.
    if 'linear-equations' not in RECORDED:
        M.set_slide(LE, 3, title='No solution', active=1, pre=[T('$5(x+2)=5x+7$', size=68, gap=40)], script=[
            'Not every equation gives you one neat answer.',
            D('Open the bracket: write "5x + 10 = 5x + 7"'),
            'Open the bracket: five x plus ten equals five x plus seven.',
            D('Cross out 5x on both sides; write "10 = 7" and a big ✗'),
            'Take five x off both sides: ten equals seven.',
            "We know that's false. That's a contradiction.",
            "No matter which x you try, you'll hit that contradiction. So this equation has NO solution."])
        M.set_slide(LE, 4, title='Every x works', active=2, pre=[T('$5(x+2)=5x+10$', size=68, gap=40)], script=[
            'Now the opposite situation. Same left side, one number changed on the right.',
            D('Open the bracket: write "5x + 10 = 5x + 10"'),
            'Open the bracket: five x plus ten. And the right side? Five x plus ten. The exact same thing.',
            D('Cross out 5x on both sides; write "10 = 10"'),
            'Take five x off both sides: ten equals ten. Always true.',
            "x disappeared. It doesn't matter what you plug in — the two sides are always equal.",
            D('Write "infinitely many solutions"'),
            "That's called infinitely many solutions. x can be any number."])
        # "Fractions & brackets": (x+3)/4 = 5 was the Hebrew practice question q-141
        _sub(M, LE, 8, [('$\\frac{x+3}{4}=5$', '$\\frac{x-4}{5}=3$'),
                        ('(x + 3)/4 = 5 appears', '(x − 4)/5 = 3 appears'),
                        ('Write "5 = 20/4", then cross out both 4s: "x + 3 = 20"', 'Write "3 = 15/5", then cross out both 5s: "x − 4 = 15"'),
                        ('Five is twenty quarters. Same denominator on both sides — cancel it. The four divided the WHOLE top, so we get x plus three equals twenty. Not x plus twelve!',
                         'Three is fifteen fifths. Same denominator on both sides — cancel it. The five divided the WHOLE top, so we get x minus four equals fifteen. Not x minus twenty!'),
                        ('Write "x = 17"', 'Write "x = 19"'),
                        ('x equals seventeen.', 'x equals nineteen.')])
        M.card('mem-r26-t06-single')['tables'][0]['rows'][6] = \
            ['$x$ cancels', 'false ($10=7$) $\\to$ no solution; true ($10=10$) $\\to$ infinitely many solutions']

    # ---------------- guided Q1 (Hebrew 2/(x−2) = 1/(x−1) → 0; study guide 3/(x−4) = 1/(x−2) → 1)
    S('q-171', stem='Given: $x \\ne 2$ and $x \\ne 3$.\n$\\frac{4}{x-2}=\\frac{3}{x-3}$\n$x = ?$',
      choices=['$-1$', '$6$', '$18$', '$3$'], correct=2,
      expl=['The restrictions are $x \\ne 2$ and $x \\ne 3$.',
            'One fraction equals one fraction, so cross-multiply: $4(x-3)=3(x-2)$.',
            '$4x-12=3x-6 \\to x=6$.',
            '$6$ is not a forbidden value. Check: $\\frac{4}{4}=1$ and $\\frac{3}{3}=1$. The answer is choice 2.',
            'The traps: multiplying straight across ($4(x-2)=3(x-3)$) gives $-1$, and $3$ is forbidden.'])
    video('q-171', {
        2: [
            'First, look at the conditions: x is not two, and not three.',
            'Why? Because either one would make a denominator zero — and dividing by zero is undefined.',
            D('Circle "x ≠ 2, x ≠ 3"'),
            "Now the method: a common denominator for both sides. Here it's x minus two, times x minus three.",
            D('Write "4(x − 3)/[(x − 2)(x − 3)] = 3(x − 2)/[(x − 3)(x − 2)]"'),
            'Left side: four times x minus three on top. Right side: three times x minus two on top.',
            D('Cross out the common denominator on both sides; write "4(x − 3) = 3(x − 2)"'),
            "Same denominator on both sides of an equation — cancel it. That's really multiplying both sides by it.",
            "Notice: we could have jumped straight here with cross-multiplication. When fraction equals fraction, that's allowed.",
            D('Write "4x − 12 = 3x − 6"'),
            'Open the brackets: four x minus twelve equals three x minus six.',
            D('Write "x = 6"'),
            'x terms left, numbers right: x equals six.',
            D('Write "6 ≠ 2, 6 ≠ 3 ✓" and circle choice 2'),
            "Six isn't two and isn't three — allowed. Choice two.",
            'Careful: multiply straight across — four times x minus two — and you get negative one. That is choice one, the trap.'],
        3: [
            'Or test the choices in the original equation.',
            D('Cross out choice 4'),
            'Choice four, x equals three? Forbidden — it makes a denominator zero. Out.',
            D('Next to choice 1 write "4/(−3) ≠ 3/(−4) ✗"'),
            'Choice one, x equals negative one: four over negative three, against three over negative four. Not equal.',
            D('Next to choice 2 write "4/4 = 1,  3/3 = 1 ✓"'),
            'Choice two, x equals six: four over four is one. Three over three is one. Equal!',
            D('Circle choice 2'),
            'Choice two. Same answer.']})

    # ---------------- systems guided Q (Hebrew 6x+3y = 27, x+y = 5 → 4; study guide 6x+3y = 36, x+y = 7 → 5)
    S('q-164', stem=given_sys('8x+4y=44', 'x+y=9'),
      choices=['$4$', '$2$', '$7$', '$11$'], correct=2,
      expl=['Divide the first equation by $4$: $2x+y=11$.',
            'Subtract the second equation: $(2x+y)-(x+y)=11-9$, so $x=2$.',
            'Check: $y=7$, and $8\\cdot2+4\\cdot7=16+28=44$. The answer is choice 2.',
            'Or substitute: $y=9-x$, so $8x+4(9-x)=44 \\to 4x+36=44 \\to x=2$.'])
    video('q-164', {
        2: [
            'Two equations, two unknowns — as many equations as unknowns, so we can usually solve it.',
            "They want x. So isolate the OTHER letter — y. Then y disappears, and we're left with exactly the letter we want.",
            D('Under x + y = 9 write "y = 9 − x"'),
            'From the second equation: y equals nine minus x.',
            D('Write "8x + 4(9 − x) = 44"'),
            'Plug that into the first equation, in place of y.',
            D('Write "8x + 36 − 4x = 44 → 4x = 8 → x = 2"'),
            'Four times nine is thirty-six, minus four x. Four x plus thirty-six is forty-four. Four x is eight. x is two.',
            D('Circle choice 2'),
            'Choice two.'],
        3: [
            'Now the shortcut. Look at eight, four and forty-four — they all divide by four.',
            D('Next to the first equation write "÷4 → 2x + y = 11"'),
            'Divide the whole equation by four: two x plus y equals eleven.',
            D('Write "(2x + y) − (x + y) = 11 − 9"'),
            "Now subtract the second equation. The y's cancel.",
            D('Write "x = 2" and circle choice 2'),
            'x equals two. Choice two — in two lines.',
            'Careful: eleven is two x plus y, not x. Stop there, and you pick choice four.']})

    # ---------------- systems guided Q (Hebrew 3x+y = 25, 2x+3y = 33 → 6; study guide 2x+y = 19, 3x+2y = 31 → 7)
    S('q-165', stem=given_sys('4x+y=22', '3x+2y=24'),
      choices=['$6$', '$5$', '$4$', '$20$'], correct=3,
      expl=['They ask for $x$, so match the $y$ terms. Multiply the first equation by $2$: $8x+2y=44$.',
            'Subtract the second equation: $(8x+2y)-(3x+2y)=44-24$, so $5x=20$ and $x=4$.',
            'Check: $y=22-16=6$, and $3\\cdot4+2\\cdot6=24$. The answer is choice 3.',
            'The traps: $20$ is $5x$ (not divided by $5$), and $6$ is $y$.'])
    video('q-165', {
        2: [
            "They want x. So let's make the y's match — and cancel them.",
            "We could match the x's instead — times three and times four, making twelve x. But they want x, so match the y's.",
            'The first equation has one y, the second has two. Multiply the first equation by two.',
            D('Under the first equation write "×2 → 8x + 2y = 44"'),
            'Every term: eight x plus two y equals forty-four.',
            D('Write "(8x + 2y) − (3x + 2y) = 44 − 24"'),
            'Subtract the second equation. Two y minus two y — gone.',
            D('Write "5x = 20 → x = 4" and circle choice 3'),
            'Eight x minus three x is five x. Forty-four minus twenty-four is twenty. Five x is twenty, so x equals four. Choice three.',
            'Stop at twenty, and you pick choice four. Divide by five.'],
        3: [
            'Substitution works too. In the first equation, y has coefficient one — easy to isolate.',
            D('Write "y = 22 − 4x"'),
            'y equals twenty-two minus four x.',
            D('Write "3x + 2(22 − 4x) = 24 → 3x + 44 − 8x = 24"'),
            'Into the second: three x plus forty-four minus eight x equals twenty-four.',
            D('Write "−5x = −20 → x = 4"'),
            'Negative five x equals negative twenty. x is four.',
            D('Write "y = 6: 16 + 6 = 22 ✓, 12 + 12 = 24 ✓"'),
            'And y is six. Both equations check. Choice three.']})

    # ---------------- single-equation practice (Hebrew self-practice q-166 … q-170)
    S('q-166', stem=given_eq('3x+11=2'),
      choices=['$\\frac{13}{3}$', '$3$', '$-3$', '$-9$'], correct=3,
      expl=['Subtract $11$ from both sides: $3x=-9$.', 'Divide by $3$: $x=-3$. The answer is choice 3.'])
    S('q-167', stem=given_eq('5(4-x)=2(x-4)'),
      choices=['$-4$', '$0$', '$2$', '$4$'], correct=4,
      expl=['Open the brackets: $20-5x=2x-8$.',
            'Move the $x$ terms to the right and the numbers to the left: $20+8=2x+5x$, so $28=7x$ and $x=4$.',
            'Check: both brackets are $0$, so both sides are $0$. The answer is choice 4.'])
    S('q-168', stem=given_eq('\\frac{3(x-2)}{7}=3'),
      choices=['$3$', '$5$', '$7$', '$9$'], correct=4,
      expl=['Multiply both sides by $7$: $3(x-2)=21$.', 'Divide by $3$: $x-2=7$, so $x=9$. The answer is choice 4.'])
    # review 2026-10-02: numeric choices 0 / 2 / 4 all satisfied the identity -> statement choices, exactly one true
    S('q-169', stem='Given: $\\frac{12x+8}{4}=\\frac{6x+4}{2}$\nWhich of the following statements is true?',
      choices=['The only solution is $x=0$', 'The only solution is $x=2$', NA, 'Every value of $x$ satisfies the equation'], correct=4,
      expl=['Simplify each side: $\\frac{12x+8}{4}=3x+2$ and $\\frac{6x+4}{2}=3x+2$.',
            'The equation is $3x+2=3x+2$. Take $3x$ off both sides: $2=2$, which is always true.',
            'So every $x$ is a solution (infinitely many solutions). The answer is choice 4.',
            'The trap: $x=0$ and $x=2$ do work, but they are not the only solutions.'])
    S('q-170', stem=given_eq('\\frac{9(x+2)}{3}=3x+4'),
      choices=['$-\\frac{2}{3}$', '$0$', '$2$', NA], correct=4,
      expl=['Left side: $\\frac{9(x+2)}{3}=3(x+2)=3x+6$.',
            'The equation becomes $3x+6=3x+4$. Take $3x$ off both sides: $6=4$, which is false.',
            'So no $x$ satisfies the equation. The answer is choice 4.'])
    # newExtension near-copy of the Hebrew lesson example 2x − 5 = 3
    S('alg-extra-unit-t6-4-1', stem=given_eq('3x-4=11'), choices=['$5$', '$4$', '$6$', '$3$'], correct=1,
      expl=['Add $4$ to both sides: $3x=15$.', 'Divide by $3$: $x=5$. The answer is choice 1.'])

    # ---------------- systems practice (Hebrew self-practice q-159 … q-163)
    S('q-159', stem=given_sys('5x+3y=-1', 'x=-2', ask='y'),
      choices=['$4$', '$3$', '$2$', '$1$'], correct=2,
      expl=['Put $x=-2$ into the first equation: $5\\cdot(-2)+3y=-1$.', '$-10+3y=-1 \\to 3y=9 \\to y=3$. The answer is choice 2.'])
    S('q-160', stem=given_sys('x+2y=16', 'x+y=9', ask='y'),
      choices=['$2$', '$5$', '$7$', '$9$'], correct=3,
      expl=['Same $x$ in both equations, so subtract: $(x+2y)-(x+y)=16-9$.', 'The $x$ terms cancel: $y=7$. The answer is choice 3.'])
    S('q-161', stem=given_sys('3x-3y=0', '2x+y=9'),
      choices=['$1$', '$3$', '$\\frac{9}{2}$', '$9$'], correct=2,
      expl=['From the first equation: $3x=3y$, so $x=y$.',
            'Put $x$ in place of $y$ in the second equation: $2x+x=9 \\to 3x=9 \\to x=3$. The answer is choice 2.'])
    S('q-162', stem=given_sys('x+y=30', 'x-y=8', ask='y'),
      choices=['$19$', '$11$', '$15$', '$8$'], correct=2,
      expl=['Subtract the second equation from the first. Keep it in brackets: $(x+y)-(x-y)=30-8$.',
            '$x+y-x+y=22 \\to 2y=22 \\to y=11$. The answer is choice 2.',
            'Shortcut: $y$ is half the difference: $\\frac{30-8}{2}=11$. ($19$ is $x$.)'])
    S('q-163', stem=given_sys('3(x-1)-2y=6+y', 'x+y=7'),
      choices=['$2$', '$3$', '$5$', '$7$'], correct=3,
      expl=['Tidy the first equation: $3x-3-2y=6+y \\to 3x-3y=9 \\to x-y=3$.',
            'Add $x+y=7$: $2x=10$, so $x=5$. The answer is choice 3.'])

    # ---------------- mixed practice (Hebrew summary practice q-139 … q-158)
    S('q-139', stem=given_eq('3x-8=2x+5'), choices=['$13$', '$-13$', '$3$', '$-3$'], correct=1,
      expl=['Move the $x$ terms to the left and the numbers to the right: $3x-2x=5+8$.', 'So $x=13$. The answer is choice 1.'])
    S('q-140', stem=given_eq('4(x-3)=20'), choices=['$-2$', '$2$', '$\\frac{23}{4}$', '$8$'], correct=4,
      expl=['Divide both sides by $4$: $x-3=5$.', 'So $x=8$. The answer is choice 4.'])
    S('q-141', stem=given_eq('\\frac{x+5}{2}=7'), choices=['$19$', '$14$', '$12$', '$9$'], correct=4,
      expl=['Multiply both sides by $2$: $x+5=14$.', 'Subtract $5$: $x=9$. The answer is choice 4.'])
    S('q-142', stem=given_eq('\\frac{5x+10}{5}=6'), choices=['$-4$', '$4$', '$8$', '$20$'], correct=2,
      expl=['Multiply both sides by $5$: $5x+10=30$.', '$5x=20$, so $x=4$. The answer is choice 2.',
            'Or divide the whole numerator by $5$ first: $x+2=6$.'])
    S('q-143', stem=given_eq('\\frac{4x+2}{5}-\\frac{x+2}{3}=\\frac{2x+8}{10}'),
      choices=['$5$', '$4$', '$2$', '$-1$'], correct=2,
      expl=['The common denominator of $5$, $3$ and $10$ is $30$. Multiply every term by $30$ and put each numerator in brackets:',
            '$6(4x+2)-10(x+2)=3(2x+8)$.',
            'The minus hits the whole bracket: $24x+12-10x-20=6x+24$.',
            '$14x-8=6x+24 \\to 8x=32 \\to x=4$. The answer is choice 2.',
            'The trap: writing $-10x+20$ gives $x=-1$.'])
    S('q-144', stem=given_sys('5x+y=38', 'y=3'), choices=['$8$', '$7$', '$6$', '$5$'], correct=2,
      expl=['Put $y=3$ into the first equation: $5x+3=38$.', '$5x=35$, so $x=7$. The answer is choice 2.'])
    S('q-145', stem=given_sys('x+3y=17', '3x=6', ask='y'), choices=['$15$', '$5$', '$3$', '$2$'], correct=2,
      expl=['From $3x=6$: $x=2$.', 'Put it into the first equation: $2+3y=17 \\to 3y=15 \\to y=5$. The answer is choice 2.'])
    S('q-146', stem=given_sys('3x+y=19', 'x-y=1'), choices=['$20$', '$9$', '$5$', '$4$'], correct=3,
      expl=['Opposite $y$ terms, so add the equations: $(3x+y)+(x-y)=19+1$.', '$4x=20$, so $x=5$. The answer is choice 3.'])
    S('q-147', stem=given_sys('x+4y=18', 'x+y=6', ask='y'), choices=['$4$', '$2$', '$6$', '$12$'], correct=1,
      expl=['Same $x$ in both, so subtract: $(x+4y)-(x+y)=18-6$.', '$3y=12$, so $y=4$. The answer is choice 1.'])
    S('q-148', stem=given_sys('x+y=22', 'x-y=6'), choices=['$8$', '$11$', '$14$', '$16$'], correct=3,
      expl=['Add the two equations: the $y$ terms cancel, and $2x=28$.', 'So $x=14$. The answer is choice 3.',
            'Shortcut: $x$ is half the sum: $\\frac{22+6}{2}=14$.'])
    S('q-149', stem=given_sys('2x+5y=24', '3x-y=2'), choices=['$5$', '$4$', '$3$', '$2$'], correct=4,
      expl=['In the second equation $y$ has coefficient $1$, so isolate it: $y=3x-2$.',
            'Substitute: $2x+5(3x-2)=24 \\to 2x+15x-10=24 \\to 17x=34$.', 'So $x=2$. The answer is choice 4.'])
    S('q-150', stem=given_sys('3x+5y=29', '2x+10y=46'), choices=['$3$', '$4$', '$6$', '$12$'], correct=1,
      expl=['They ask for $x$, so match the $y$ terms. Double the first equation: $6x+10y=58$.',
            'Subtract the second: $(6x+10y)-(2x+10y)=58-46 \\to 4x=12$.', 'So $x=3$. The answer is choice 1.'])
    S('q-151', stem=given_sys('2x+3y=4', '3x-2y=19'), choices=['$-2$', '$3$', '$4$', '$5$'], correct=4,
      expl=['Match the $y$ terms: multiply the first equation by $2$ and the second by $3$.',
            '$4x+6y=8$ and $9x-6y=57$.',
            'Add: $13x=65$, so $x=5$. The answer is choice 4.'])
    S('q-152', stem=given_eq('\\frac{\\frac{1}{x}}{4}=2'),
      choices=['$\\frac{1}{8}$', '$\\frac{1}{2}$', '$2$', '$8$'], correct=1,
      expl=['Multiply both sides by $4$: $\\frac{1}{x}=8$.',
            'If $\\frac{1}{x}=8$, then $x$ is the reciprocal of $8$: $x=\\frac{1}{8}$. The answer is choice 1.',
            'Check: $\\frac{1}{x}=8$ and $\\frac{8}{4}=2$. The trap is $8$: that is $\\frac{1}{x}$, not $x$.'])
    S('q-153', stem='Given: $x > 0$ and $y > 0$, and\n' + cases('xy=32', '\\frac{x}{y}=2') + '\n$x+y = ?$',
      choices=['$32$', '$16$', '$12$', '$10$'], correct=3,
      expl=['Multiply the two equations: $xy\\cdot\\frac{x}{y}=32\\cdot2$, so $x^2=64$.',
            '$x$ is positive, so $x=8$. Then $8y=32$, so $y=4$.',
            '$x+y=12$. The answer is choice 3.',
            'Or substitute: $\\frac{x}{y}=2$ gives $x=2y$, so $2y\\cdot y=32$, $y^2=16$ and $y=4$.'])
    S('q-154', stem='Given: $x \\ne -2$ and $x \\ne -4$.\n$\\frac{1}{x+2}=\\frac{3}{x+4}$\n$x = ?$',
      choices=['$1$', '$-1$', '$-2$', '$-5$'], correct=2,
      expl=['One fraction equals one fraction, so cross-multiply: $1\\cdot(x+4)=3(x+2)$.',
            '$x+4=3x+6$, so $-2=2x$ and $x=-1$.',
            '$-1$ is allowed. Check: $\\frac{1}{1}=1$ and $\\frac{3}{3}=1$. The answer is choice 2.',
            'The traps: multiplying straight across gives $-5$, and $-2$ is forbidden.'])
    S('q-155', stem='Given: $x \\ne 0$ and\n' + cases('x^2=2y', 'y=5x') + '\n$x = ?$',
      choices=['$2$', '$5$', '$10$', '$50$'], correct=3,
      expl=['Put $y=5x$ into the first equation: $x^2=2\\cdot5x=10x$.',
            'Do not divide by something that could be $0$. Here we are told $x \\ne 0$, so we may divide by $x$: $x=10$.',
            'The answer is choice 3. ($50$ is $y$.)'])
    S('q-156', stem='How many solutions does the equation $4x=9x$ have?',
      choices=['The equation has no solution', 'One', 'Two', 'Nine'], correct=2,
      expl=['Move everything to one side: $9x-4x=0$, so $5x=0$ and $x=0$.',
            'One solution: $x=0$. The answer is choice 2.',
            'The trap: dividing both sides by $x$ gives $4=9$ and "no solution". But $x$ may be $0$, so we may not divide by it.'])
    S('q-157', stem='Given:\n' + cases('(a+1)(b+1)=6', 'ab=-4') + '\n$a+b = ?$',
      choices=['$-9$', '$1$', '$9$', '$10$'], correct=3,
      expl=['Open the brackets: $(a+1)(b+1)=ab+a+b+1$.',
            'So $ab+a+b+1=6$. Put in $ab=-4$: $-4+(a+b)+1=6$.',
            '$a+b-3=6$, so $a+b=9$. The answer is choice 3.',
            'The traps: forgetting the $+1$ gives $10$, and using $+4$ instead of $-4$ gives $1$.'])
    S('q-158', stem='Given: $x \\ne -2$ and\n$\\frac{(x-3)-(3-x)}{2+x}=1$\n$x = ?$',
      choices=['$-8$', '$3$', '$4$', '$8$'], correct=4,
      expl=['Numerator: $(x-3)-(3-x)=x-3-3+x=2x-6$.',
            'So $\\frac{2x-6}{2+x}=1$. Multiply both sides by $2+x$: $2x-6=2+x$.',
            'So $x=8$. It is allowed ($8 \\ne -2$). The answer is choice 4.',
            'The trap: forgetting that the minus hits the whole bracket $(3-x)$ gives the numerator $-6$ and $x=-8$.'])


# =====================================================================================
# 11. 2026-10-02 order changes (less like a copy of the Hebrew course; only where nothing is lost)
# =====================================================================================
def order_changes(M):
    # (1) Lesson: "No solution" now comes before "Every x works" (the slides themselves are rebuilt in new_numbers;
    #     here the sidebar, the recap line and the summary video follow the same order).
    sb = M.video(LE)['hybrid']['sidebar']
    assert sb[1] == 'Every x works' and sb[2] == 'No solution'
    sb[1], sb[2] = 'No solution', 'Every x works'
    M.set_sidebar(LE, sb)
    _sub(M, LE, 12, [('$x$ cancels: true $\\to$ infinitely many solutions, false $\\to$ none',
                      '$x$ cancels: false $\\to$ no solution, true $\\to$ infinitely many solutions')])
    SUM = 'r26-t06-summary'
    assert M.slide(SUM, 5)['title'] == 'x cancels'
    M.set_slide(SUM, 5, pre=[], script=[
        A('False appears', T('$4=7$ → no solution', size=46)),
        'Sometimes x cancels out. Look at what is left.',
        'Always false? No x works — no solution.',
        A('True appears', T('$4=4$ → infinitely many solutions', size=46)),
        'Always true? Every x works — infinitely many solutions.'])

    # (2) Guided questions after the first lesson, in the lesson's own slide order and easy -> hard:
    #     cross-multiply (q-171) -> forbidden answer (q-r26-t06-02, short) -> minus before a fraction (q-r26-t06-01, LCD).
    M.move('q-r26-t06-02', 'single-equation', after='solve-q-171')
    M.move('solve-q-r26-t06-02', 'single-equation', after='q-r26-t06-02')


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
    # alg-extra-unit-t6-2-1 was the lesson example of "systems" slide 6 (2x + 3y = 19, 3x + 2y = 16) -> new numbers.
    M.set_q('alg-extra-unit-t6-2-1', stem='Given:\n' + r'$\begin{cases} 2x+3y=13 \\ 3x+2y=17 \end{cases}$' + '\n$x = ?$',
            choices=['$1$', '$5$', '$6$', '$4$'], correct=2,
            expl=[r'They ask for $x$, so make the $y$ terms cancel: multiply the first equation by $2$ and the second by $3$: $4x+6y=26$ and $9x+6y=51$.',
                  r'Subtract the first from the second: $5x=25$, therefore $x=5$. The answer is choice 2.',
                  r'Check: $y=1$ ($2\cdot5+3=13$ ✓, $3\cdot5+2=17$ ✓). Choice 1 is $y$, not $x$.'])
    # alg-extra-unit-t6-1-6 was the lesson example x(x - 5) = 0 of "linear-equations" slide 10 -> new numbers.
    M.set_q('alg-extra-unit-t6-1-6', stem='Given: $x(x+4)=0$\nWhat is the sum of all the solutions of the equation?',
            choices=['$-4$', '$0$', '$4$', '$-8$'], correct=1,
            expl=[r'A product is $0$ when one of the factors is $0$: $x=0$ or $x+4=0$.',
                  r'So $x=0$ or $x=-4$. The sum is $0+(-4)=-4$.',
                  r'The traps: the factor is $x+4$, but the solution is $-4$ (choice 3 forgets the sign). And dividing by $x$ loses the solution $x=0$.'])
