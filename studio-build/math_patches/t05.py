"""Topic 5 (Expressions) - course review 2026-09 fixes. See t05_CHANGES.md."""
from math_api import T, H, A, D, Q

TOPIC = 5
ADV = 'expression-advanced'
SELF = 'expression-self'
BANK = 'unit-t5-1'


def _replace(M, vid, n, old, new):
    """Replace one spoken/drawn line (exact text). new = str (same kind), None (delete) or a list of script items."""
    def fn(lines):
        out, hit = [], False
        for l in lines:
            txt = l.get('say', l.get('draw'))
            if txt == old and not hit:
                hit = True
                if new is None: continue
                if isinstance(new, str):
                    out.append({'say': new} if 'say' in l else {'draw': new})
                else:
                    for x in new: out.append({'say': x} if isinstance(x, str) else {'draw': x[1]})
            else: out.append(l)
        assert hit, '%s #%d: line not found: %s' % (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _append(M, vid, n, extra):
    M.edit_lines(vid, n, lambda lines: lines + [{'say': x} if isinstance(x, str) else {'draw': x[1]} for x in extra])


def _cases(*rows):
    return '$\\begin{cases} ' + ' \\\\ '.join(rows) + ' \\end{cases}$'


# ---------------------------------------------------------------------------------------------------------------
# 1. Lesson video "Working with Expressions"
# ---------------------------------------------------------------------------------------------------------------
def lesson(M):
    vid = 'expression-strategy'
    # opposite brackets: a 5-second proof instead of "trust it"
    _replace(M, vid, 5, "You could prove it by taking a minus out of the bracket. But honestly? Trust it. It's always negative one.", [
        "Why? Take a minus out of the bracket: b minus a is minus, a minus b.",
        ('D', 'Write "b − a = −(a − b)"'),
        "Open it and check: minus a, plus b. The same thing.",
        "So the bottom is the top with a minus. Any number over its opposite — negative one."])
    # repeated bracket: pointer to "given a block"
    _append(M, vid, 6, ["And if a question GIVES you the value of a block — say, a plus b equals five — put the number in its place. You'll practise that after Question 14."])

    split = dict(title='Splitting a fraction', mode='concept', active=2, pre=[], script=[
        "So what CAN you do with one fraction?",
        A('Split rule appears: (a + b)/c = a/c + b/c', T('$\\frac{a+b}{c}=\\frac{a}{c}+\\frac{b}{c}$ ✓', size=56)),
        "A sum on TOP? You may split it.",
        "Each term on top gets its own copy of the bottom.",
        D('Next to it write "(10 + 4)/2 = 10/2 + 4/2 = 5 + 2 = 7"'),
        "Ten plus four is fourteen. Half of fourteen is seven. Five plus two — also seven. It works.",
        A('Trap appears: c/(a + b) ≠ c/a + c/b', T('$\\frac{c}{a+b}\\ne\\frac{c}{a}+\\frac{c}{b}$ ✗', size=56)),
        "A sum on the BOTTOM? No. You may not split it.",
        A('Numbers appear: 6/(1 + 2) = 2, but 6/1 + 6/2 = 9', T('$\\frac{6}{1+2}=2$, but $\\frac{6}{1}+\\frac{6}{2}=9$', size=44)),
        "Test it. Six over one plus two: six over three — two.",
        "Split it wrongly: six over one, plus six over two. Six plus three — nine. Not the same.",
        "This is the most common trap in algebra. Top: split. Bottom: never.",
    ])
    choose = dict(title='Choosing numbers', mode='concept', active=7, pre=[], script=[
        "Which numbers should you plug in?",
        "All ones is the fastest first try. It often works — you'll see it in Questions 3 and 4.",
        A('Rule appears: different letters, different values', T('Different letters → different values: $2$, $3$, $5$', size=40)),
        "But the safest choice: different letters get different small values. Two, three, five.",
        A('Warning appears: 0 and 1 cause ties', T('$0$ and $1$ often make choices tie: $1^2=1$, $0\\cdot b=0$', size=40)),
        "Zero and one are lazy numbers. One squared is one. Zero times anything is zero.",
        "So two different choices often give the same value. That's a tie.",
        A('Rule appears: obey every condition', T('Obey every condition: $a\\ne b$, $x>0$, "integer"', size=40)),
        "And obey every condition. a can't equal b? Don't make them equal. x is positive? No negatives, no zero.",
        "Does the question give an equation, like a minus b equals three? Pick numbers that make it true: a is three, b is zero.",
        A('Rule appears: a tie? new numbers for those choices', T('A tie? Keep only those choices — new numbers', size=40)),
        "A tie? Don't guess. Keep only the tied choices and plug in new numbers.",
    ])
    M.insert_slides(vid, 7, [choose])     # after "Plug in numbers" (slide 7 before the first insert)
    M.insert_slides(vid, 3, [split])      # after "No cancelling!"
    M.set_sidebar(vid, ["What's an expression?", "No cancelling!", "Splitting a fraction", "The main fraction bar",
                        "Opposite brackets", "A repeated bracket", "Plug in numbers", "Choosing numbers",
                        "Pick your method", "Recap"])
    # slides now: 1 title, 2 expr, 3 no cancel, 4 split, 5 main bar, 6 opposite, 7 repeated, 8 plug in, 9 choosing, 10 pick, 11 recap
    for n, act in [(5, 3), (6, 4), (7, 5), (8, 6), (10, 8), (11, 9)]:
        M.set_slide(vid, n, active=act)
    M.set_slide(vid, 11, script=[
        "Let's lock it in.",
        A("'Expression = ? · never cancel the denominator' appears", T('Expression $=\\ ?$ · never cancel the denominator', size=38)),
        A("'Split the top ✓ · never the bottom ✗' appears", T('Split a sum on top ✓ · never a sum on the bottom ✗', size=38)),
        A("'Main bar first — work from the inside out' appears", T('Main bar first — work from the inside out', size=38)),
        A("'(a − b)/(b − a) = −1' appears", T('$\\frac{a-b}{b-a}=-1$', size=48)),
        A("'Repeated bracket? Take it out front' appears", T('Repeated bracket? Take it out front', size=38)),
        A("'Plug in: eliminate three · a tie? new numbers' appears", T('Plug in: eliminate three · a tie? New numbers', size=38)),
        D('Circle the −1'),
        "Four guided questions next. Try each one first — then watch the solution.",
    ])


# ---------------------------------------------------------------------------------------------------------------
# 2. Guided questions 1-14: text, wrong tip, weak logic, used-before-taught
# ---------------------------------------------------------------------------------------------------------------
def guided_fixes(M):
    # Q1 - remove the false "answer 3 sits in slot 3" tip; no ":" for division
    M.set_q('q-135', expl=["Work from the inside out. Deepest layer: $\\frac{1}{3}+\\frac{1}{6}=\\frac{2}{6}+\\frac{1}{6}=\\frac{3}{6}=\\frac{1}{2}$.",
                           "Next layer: $1\\div\\frac{1}{2}=1\\cdot2=2$.",
                           "Main bar: $\\frac{12}{2}=6$. The answer is choice 2."])
    _replace(M, 'solve-q-135', 2, 'Write "1 : (1/2) = 2"', 'Write "1 ÷ 1/2 = 1 · 2 = 2"')
    _replace(M, 'solve-q-135', 2, 'Write "12 : 2 = 6" and circle choice 2', 'Write "12 ÷ 2 = 6" and circle choice 2')
    _replace(M, 'solve-q-135', 2, "A side tip about the exam: there are no visual traps in the choices. When an answer equals a choice NUMBER — say the answer is three — it sits in slot three.", None)

    # Q2
    M.set_q('q-136', expl=["Since $q-p=-(p-q)$, the fraction $\\frac{p-q}{q-p}$ equals $-1$.",
                           "Therefore the expression is $7-(-1)=7+1=8$. The answer is choice 2.",
                           "The trap is $6$ (choice 1): that is what you get if you treat the fraction as $+1$."])
    # Q3
    M.set_q('q-137', choices=['$2t(c+d)$', '$2(c+d+t)$', '$0$', '$c+d+t$'],
            expl=["Take out the common bracket: $(c+d)(t-3)+(c+d)(t+3)=(c+d)[(t-3)+(t+3)]$.",
                  "Inside: $-3$ and $+3$ cancel, therefore $(t-3)+(t+3)=2t$.",
                  "The expression equals $(c+d)\\cdot2t=2t(c+d)$. The answer is choice 1."])
    # Q4
    M.set_q('q-138', stem='$(a+b+c+d)^2-(a+b-c-d)^2=\\ ?$',
            expl=["Treat the expression as two blocks: $A=a+b$ and $B=c+d$. It becomes $(A+B)^2-(A-B)^2$.",
                  "$(A+B)^2-(A-B)^2=(A^2+2AB+B^2)-(A^2-2AB+B^2)=4AB$.",
                  "Put the blocks back: $4(a+b)(c+d)$. The answer is choice 2.",
                  "Check with $a=b=c=d=1$: $4^2-0^2=16$, and choice 2 gives $4\\cdot2\\cdot2=16$; the other choices give $2$, $0$ and $2$."])
    # Q5
    M.set_q('q-125', expl=["Take out a common factor in each bracket: $18^2-18=18(18-1)=18\\cdot17$ and $17^2+17=17(17+1)=17\\cdot18$.",
                           "The two brackets are the same number, therefore their difference is $0$. The answer is choice 2.",
                           "Direct calculation gives the same: $(324-18)-(289+17)=306-306=0$."])
    _append(M, 'solve-q-125', 1, ["Method one is plain calculation. Quick with squares? Skip ahead to Methods three and four — they're the fast ones."])
    # Q6
    M.set_q('q-126', expl=["No minus sign stands right in front of a bracket, therefore the brackets can be dropped without changing any sign: $p-q-r-s+q$.",
                           "$-q$ and $+q$ cancel, leaving $p-r-s$. The answer is choice 2.",
                           "Check with $p=10$, $q=2$, $r=3$, $s=4$: $\\{[(10-2)-3]-4+2\\}=3$, and choice 2 gives $10-3-4=3$."])
    # Q7 - factoring is taught in Topic 4; the video uses the choices (faster here)
    M.set_q('q-127', stem='Which of the following expressions is necessarily equal to $x^2+11x+24$?',
            expl=["Every choice has the form $(x+p)(x+q)=x^2+(p+q)x+pq$. In every choice $pq=24$, therefore the middle term decides: we need $p+q=11$.",
                  "The sums are $25$, $14$, $11$ and $10$. Only $8+3=11$. Therefore $x^2+11x+24=(x+8)(x+3)$. The answer is choice 3.",
                  "Check with $x=1$: $1+11+24=36$, and choice 3 gives $9\\cdot4=36$ (the others give $50$, $39$ and $35$)."])
    _replace(M, 'solve-q-127', 1, "We don't know how to factor this yet — so let the answers do the work.",
             "You know sum and product from Topic 4. But here, the choices can do the work even faster.")
    _replace(M, 'solve-q-127', 2, "We haven't learned to factor this kind of expression. No problem — the choices will help us. Open them up.",
             "Sum and product would work. But look — the choices help us too. Open them up.")
    # Q8 - condition first, value second (matches "If ___ then ... equals ___")
    M.set_q('q-128', choices=['$x>0$ ; $3$', '$x<0$ ; $4$', '$x<0$ ; $5$', '$x>0$ ; $7$'],
            expl=["If $x<0$, then $|x|=-x$, therefore $\\frac{|x|}{x}=\\frac{-x}{x}=-1$ and the expression equals $-1+5=4$. This is choice 2.",
                  "If $x>0$, then $\\frac{|x|}{x}=1$ and the expression equals $1+5=6$. No choice with $x>0$ says $6$, therefore choices 1 and 4 are out.",
                  "Check with $x=-1$: $\\frac{|-1|}{-1}+5=-1+5=4$ ✓."])
    # Q9 - clear stem; a real counterexample in Method 1; no geometry reference
    M.set_q('q-129', stem='Daniel claims that for every $A\\ne0$:\n$\\dfrac{A+B}{A}=1+\\dfrac{B}{A}$\n'
                          'Maya claims that for every $B\\ne0$ and $A\\ne-B$:\n$\\dfrac{A}{A+B}=1+\\dfrac{A}{B}$\n'
                          'Which of the following is true?',
            expl=["Daniel: a sum on top may be split: $\\frac{A+B}{A}=\\frac{A}{A}+\\frac{B}{A}=1+\\frac{B}{A}$. This is true for every $A\\ne0$.",
                  "Maya: test $A=1$, $B=2$. Left side: $\\frac{1}{1+2}=\\frac{1}{3}$. Right side: $1+\\frac{1}{2}=\\frac{3}{2}$. Not equal, therefore Maya's claim is false.",
                  "Only Daniel is right. The answer is choice 1."])
    _replace(M, 'solve-q-129', 2, 'Under Maya\'s claim write "1 + A/B = B/B + A/B = (B + A)/B ✗"',
             'Under Maya\'s claim write "1 + A/B = B/B + A/B = (B + A)/B"')
    _replace(M, 'solve-q-129', 2, "Same move: one is B over B. B plus A, over B. That's not what she started with.", [
        "Same move: one is B over B. The right side is B plus A, over B.",
        "Her left side is A over A plus B. They look different — but different-looking expressions can still be equal. So test numbers.",
        ('D', 'Write "A = 1, B = 2: 1/3 vs 3/2 ✗"'),
        "A is one, B is two. Left: one over three — one third. Right: three over two. Not equal."])
    M.set_slide('solve-q-129', 3, pre=[Q('q-129')], script=[
        "Could we shorten that? Yes — split the fraction.",
        "Remember the rule: a sum on the BOTTOM can't be split. But a sum on TOP can — each term gets its own copy of the bottom.",
        D('Under Daniel\'s claim write "(A + B)/A = A/A + B/A = 1 + B/A"'),
        "A over A is one. Plus B over A. Done — Daniel is right.",
        "Maya's fraction has the sum on the BOTTOM. Splitting it is exactly the classic trap — and the numbers in Method 1 showed she's wrong.",
        D('Circle choice 1'),
        "Split only the top, and the question becomes simple. Only Daniel — choice one.",
    ])
    # Q10
    M.set_q('q-130', expl=["The minus stands in front of the second bracket only: $(p-q)-(q-p)=p-q-q+p=2p-2q=2(p-q)$.",
                           "Divide by $p-q$ (not zero, because $p\\ne q$): $\\frac{2(p-q)}{p-q}=2$. The answer is choice 2."])
    _append(M, 'solve-q-130', 1, ["Method one is the standard route. Know it well? Skip ahead to Method two."])
    # Q11 - no negative exponents (taught only in Topic 8)
    M.set_q('q-131', stem='Given: $x\\ne0$.\n$\\left(\\frac{1}{x^2}+\\frac{4x^2}{x^4}\\right)\\cdot\\frac{1}{5}\\cdot\\frac{5}{\\frac{1}{x^2}}=\\ ?$',
            expl=["Cancel $x^2$ in the second fraction: $\\frac{4x^2}{x^4}=\\frac{4}{x^2}$. The bracket equals $\\frac{1}{x^2}+\\frac{4}{x^2}=\\frac{5}{x^2}$.",
                  "Dividing by a fraction means multiplying by its reciprocal: $\\frac{5}{\\frac{1}{x^2}}=5x^2$.",
                  "The expression is $\\frac{5}{x^2}\\cdot\\frac{1}{5}\\cdot5x^2=5$. The answer is choice 3.",
                  "Faster: the choices are numbers only, therefore one legal value is enough. With $x=1$: $(1+4)\\cdot\\frac{1}{5}\\cdot5=5$."])
    _replace(M, 'solve-q-131', 1, "Negative powers — and a plug-in that makes them disappear.",
             "Fractions inside fractions — and a plug-in that makes them disappear.")
    M.set_slide('solve-q-131', 2, script=[
        "Take it piece by piece.",
        D('Under 4x²/x⁴ write "= 4/x²"'),
        "Four x squared over x to the fourth. Cancel x squared from the top and the bottom. Four over x squared.",
        D('Under the bracket write "1/x² + 4/x² = 5/x²"'),
        "Same bottom — add the tops. Five over x squared.",
        D('Under the last fraction write "5 ÷ 1/x² = 5 · x² = 5x²"'),
        "The last part is five, divided by one over x squared. Dividing by a fraction: multiply by its reciprocal. Five x squared.",
        D('Write "= 5/x² · 1/5 · 5x²"'),
        D('Cancel the 5s and the x²; write "= 5"'),
        "Cancel everything that cancels. Five.",
        D('Circle choice 3'),
        "Choice three.",
    ])
    M.set_slide('solve-q-131', 3, script=[
        "Look at the choices — only numbers. No letters.",
        "That means the answer can't depend on x. So ONE legal number is enough.",
        "And the friendliest number for powers is one. One to any power is one.",
        D('Write "x = 1: (1 + 4) · 1/5 · 5/1"'),
        "One plus four is five. Times a fifth — one. Times five — five.",
        D('Write "= 5" and circle choice 3'),
        "Five. Choice three. Here, plugging in is much shorter — use it.",
    ])
    # Q12 - no a^0 / (-1)^a (exponents come in Topic 8)
    M.set_q('q-132', stem='Given: $a$ is a positive integer.\nWhich of the following expressions has a value that does not depend on $a$?',
            choices=['$(a+3a)-(3a-a)$', '$\\dfrac{(a+2)+(a+2)^2}{a+3}$', '$(a+1)^2-(a-1)^2$', '$\\dfrac{a^2-9}{a+3}-a$'], correct=4,
            expl=["(1): $4a-2a=2a$. It depends on $a$.",
                  "(2): take out $a+2$ on top: $(a+2)+(a+2)^2=(a+2)(1+a+2)=(a+2)(a+3)$. Cancel $a+3$: $a+2$. It depends on $a$.",
                  "(3): $(a^2+2a+1)-(a^2-2a+1)=4a$. It depends on $a$.",
                  "(4): $\\frac{a^2-9}{a+3}=\\frac{(a-3)(a+3)}{a+3}=a-3$, therefore the expression is $(a-3)-a=-3$ for every $a$. The answer is choice 4."])
    M.set_slide('solve-q-132', 2, script=[
        "We're hunting for the expression where a vanishes.",
        D('Next to choice 1 write "4a − 2a = 2a"'),
        "Choice one: a plus three a is four a. Three a minus a is two a. Four a minus two a: two a. Still has a. Out.",
        D('Cross out choice 1'),
        D('Next to choice 2 write "(a + 2) + (a + 2)² = (a + 2)(1 + a + 2) = (a + 2)(a + 3)"'),
        "Choice two: a plus two appears twice on top. Take it out: a plus two, times one plus a plus two. That's a plus three.",
        D('Write "(a + 2)(a + 3)/(a + 3) = a + 2" and cross out choice 2'),
        "Cancel a plus three. a plus two. It depends on a. Out.",
        D('Next to choice 3 write "(a² + 2a + 1) − (a² − 2a + 1) = 4a"'),
        "Choice three: open both squares. a squared cancels. One cancels. Two a, minus minus two a: four a. Out.",
        D('Cross out choice 3'),
        "Three out — choice four is our answer. On the exam, mark it and move on.",
        D('Next to choice 4 write "(a − 3)(a + 3)/(a + 3) − a = −3"'),
        "Proof, for the lesson: a squared minus nine is a minus three, times a plus three. Cancel. a minus three, minus a — minus three. Always.",
        D('Circle choice 4'),
        "Choice four.",
        "Quick check by plugging in: a equals one gives minus three, a equals two gives minus three. Same value.",
    ])
    # Q13
    M.set_q('q-133', expl=["Factor the fraction. Top: $4b^2+4ab=4b(b+a)$. Bottom: $a^2-b^2=(a-b)(a+b)$.",
                           "Cancel $a+b$ (not zero, because $a\\ne-b$): the fraction equals $\\frac{4b}{a-b}$.",
                           "Then $1+\\frac{4b}{a-b}=\\frac{a-b}{a-b}+\\frac{4b}{a-b}=\\frac{a+3b}{a-b}$. The answer is choice 4.",
                           "Check with $a=2$, $b=1$: $1+\\frac{4+8}{3}=5$, and choice 4 gives $\\frac{5}{1}=5$."])
    # Q14 - anchor on 63 · 500
    M.set_q('q-134', expl=["Estimate from a round choice: $63\\cdot500=31{,}500$. The top, $32{,}004$, is a little more, therefore the answer is a little more than $500$.",
                           "Check: $63\\cdot508=63\\cdot500+63\\cdot8=31{,}500+504=32{,}004$ ✓. The answer is choice 3."])
    _replace(M, 'solve-q-134', 2, 'Write "≈ 30,000 : 60 = 500"', 'Write "63 · 500 = 31,500"')
    _replace(M, 'solve-q-134', 2, "Round to friendly numbers. Thirty divides by six — five. So thirty thousand over sixty is five hundred.",
             "Anchor on a round choice. Sixty-three times five hundred: half of sixty-three thousand. Thirty-one thousand five hundred.")
    _replace(M, 'solve-q-134', 2, "The real top is a bit bigger, the real bottom a bit bigger too. The answer sits around five hundred.",
             "The top is thirty-two thousand and four — just a little more. So the answer is just a little more than five hundred.")
    _replace(M, 'solve-q-134', 2, "Three hundred, four hundred, six hundred — out. Five hundred eight. Choice three.",
             "Three hundred eight, four hundred eight, six hundred eight — too far. Five hundred eight. Choice three.")


# ---------------------------------------------------------------------------------------------------------------
# 3. New lesson video + four guided questions (Questions 15-18) + memory card
# ---------------------------------------------------------------------------------------------------------------
def shortcuts(M):
    vid = 'r26-t05-shortcuts'
    M.new_video(vid, TOPIC, 'Exam Shortcuts', ['Sum and product', 'Round numbers', 'Given a block', 'Recap'], [
        dict(mode='title', title='Exam Shortcuts', script=[
            "Exam shortcuts — tools strong students use.",
            "A quick reminder of sum and product. Then multiplying near a round number. And using a block they give you.",
            "Each one turns a long calculation into one line."]),
        dict(title='Sum and product', mode='concept', active=0, pre=[], script=[
            "First, a reminder from Topic 4: factoring a trinomial with sum and product.",
            A('x² + 9x + 20: product 20, sum 9 → 4 and 5 appears', T('$x^2+9x+20$: product $=20$, sum $=9$ → $4$ and $5$', size=44)),
            "x squared plus nine x plus twenty. Two numbers: product twenty, sum nine. Four and five.",
            A('= (x + 4)(x + 5) appears', T('$=(x+4)(x+5)$', size=50)),
            "x plus four, times x plus five. Signs, common factors first — all as in Topic 4.",
            "On the exam it often hides inside a fraction. Factor, then cancel. You'll see it in Question 15.",
        ]),
        dict(title='Round numbers', mode='concept', active=1, pre=[], script=[
            "No calculator on the exam. So look for a round number nearby.",
            A('99 · 41 = 100 · 41 − 41 = 4,059 appears', T('$99\\cdot41=100\\cdot41-41=4{,}059$', size=50)),
            "Ninety-nine is one hundred minus one. So ninety-nine forty-ones are one hundred forty-ones, minus one forty-one.",
            "Four thousand one hundred, minus forty-one: four thousand fifty-nine.",
            A('96 · 104 = (100 − 4)(100 + 4) appears', T('$96\\cdot104=(100-4)(100+4)$', size=50)),
            "Ninety-six times one hundred four. Both are four away from one hundred — one below, one above.",
            "That's sum times difference, from the last topic.",
            A('= 100² − 4² = 10,000 − 16 = 9,984 appears', T('$=100^2-4^2=10{,}000-16=9{,}984$', size=50)),
            "One hundred squared, minus four squared. Ten thousand minus sixteen: nine thousand nine hundred eighty-four.",
            "Two numbers the same distance from a round number? Think sum times difference.",
        ]),
        dict(title='Given a block', mode='concept', active=2, pre=[], script=[
            "Sometimes they give you the value of one expression and ask for another one.",
            A('Given: x + y = 5 appears', T('Given: $x+y=5$', size=50)),
            "x plus y equals five. You don't know x. You don't know y. And you don't need them.",
            A('3x + 3y + 1 = 3(x + y) + 1 appears', T('$3x+3y+1=3(x+y)+1$', size=50)),
            "Look for the block inside the question. Three x plus three y: take out three. Three times x plus y.",
            A('= 3 · 5 + 1 = 16 appears', T('$=3\\cdot5+1=16$', size=50)),
            "Put five in its place. Three times five, plus one: sixteen.",
            "The trap is trying to find x and y. You can't — and you don't have to.",
            "Check with numbers that obey the given: x is five, y is zero. Fifteen plus one — sixteen ✓.",
        ]),
        dict(title='Recap', mode='concept', active=3, pre=[], script=[
            "Let's lock it in.",
            A("'Trinomial? Sum and product' appears", T('Trinomial? Sum and product (Topic 4)', size=42)),
            A("'Near a round number' appears", T('Near a round number? $(100-1)\\cdot41$ · $(100-4)(100+4)$', size=40)),
            A("'Given a block? Put in its value' appears", T('Given a block? Find it and put in its value', size=42)),
            A("'Plug in numbers that obey the given' appears", T('Plugging in? Use numbers that obey the given', size=42)),
            "Four guided questions next — one for each tool, and one plug-in trap. Try each one first.",
        ]),
    ], ADV, after='solve-q-134')

    qn = M.next_question_number(TOPIC)   # 15
    sb = ['Question %d' % (qn + k) for k in range(4)]
    prev = vid

    def guided(k, qid, stem, choices, correct, expl, intro, slides):
        nonlocal prev
        M.new_q(qid, TOPIC, stem, choices, correct, expl)
        M.place_q(qid, ADV, after=prev)
        n = M.next_question_number(TOPIC)
        beats = [dict(mode='title', title='Question %d' % n, script=intro)]
        for title, script in slides:
            beats.append(dict(mode='question', active=k, title=title, pre=[Q(qid)], script=script))
        M.new_video('solve-' + qid, TOPIC, 'Exam Shortcuts', sb, beats, ADV, kind='solution', qid=qid)
        prev = 'solve-' + qid

    # Question 15 - sum and product
    guided(0, 'q-r26-t05-01', 'Given: $x\\ne5$.\n$\\dfrac{x^2-2x-15}{x-5}-x=\\ ?$',
           ['$-3$', '$3$', '$5$', '$2x+3$'], 2,
           ["Factor the top with sum and product: we need two numbers with product $-15$ and sum $-2$. They are $-5$ and $3$, therefore $x^2-2x-15=(x-5)(x+3)$.",
            "Cancel $x-5$ (not zero, because $x\\ne5$): $\\frac{(x-5)(x+3)}{x-5}=x+3$.",
            "Then $x+3-x=3$. The answer is choice 2.",
            "Check with $x=1$: $\\frac{1-2-15}{1-5}-1=\\frac{-16}{-4}-1=4-1=3$ ✓."],
           ["Question fifteen.", "A trinomial on top — let's factor it with sum and product."], [
            ('Method 1 · Sum and product', [
                "The top is x squared minus two x minus fifteen. We need two numbers: product negative fifteen, sum negative two.",
                D('Next to the top write "product −15, sum −2 → −5 and 3"'),
                "Negative five and three. Product: negative fifteen. Sum: negative two ✓.",
                D('Write "x² − 2x − 15 = (x − 5)(x + 3)"'),
                "So the top is x minus five, times x plus three.",
                D('Cancel (x − 5) on top and bottom; write "= x + 3"'),
                "Cancel x minus five. It isn't zero — x isn't five. We're left with x plus three.",
                D('Write "x + 3 − x = 3" and circle choice 2'),
                "Now the minus x at the end: x plus three, minus x. Three. Choice two.",
                "The trap: adding x instead of subtracting it gives two x plus three — choice four."]),
            ('Method 2 · Plug in', [
                "Plug-in version. x can't be five. Zero makes the top easy.",
                D('Write "x = 0: (−15)/(−5) − 0 = 3"'),
                "Negative fifteen over negative five: three. Minus zero: three.",
                D('Next to the choices write: −3, 3, 5, 3'),
                "Choice two gives three. But choice four — two times zero plus three — also gives three. A tie!",
                D('Cross out choices 1 and 3'),
                D('Write "x = 1: (1 − 2 − 15)/(1 − 5) − 1 = 4 − 1 = 3"; next to choice 4 write "5"'),
                "New number, only for the tied choices: x is one. The question: negative sixteen over negative four is four. Minus one — three. Choice four gives five. Out.",
                D('Circle choice 2'),
                "Choice two. See why zero can be a lazy number?"]),
        ])

    # Question 16 - round numbers
    guided(1, 'q-r26-t05-02', '$98\\cdot102-99\\cdot101=\\ ?$',
           ['$-5$', '$-3$', '$3$', '$5$'], 2,
           ["Both products are sum times difference around $100$: $98\\cdot102=(100-2)(100+2)=100^2-4$ and $99\\cdot101=(100-1)(100+1)=100^2-1$.",
            "Therefore the expression is $(100^2-4)-(100^2-1)=-4+1=-3$. The answer is choice 2.",
            "Check: $98\\cdot102=9{,}996$ and $99\\cdot101=9{,}999$; $9{,}996-9{,}999=-3$ ✓."],
           ["Question sixteen.", "Two big products — and no calculator. Look for a round number."], [
            ('Sum × difference', [
                "Ninety-eight and one hundred two: both are two away from one hundred.",
                D('Under 98 · 102 write "(100 − 2)(100 + 2) = 100² − 4"'),
                "Sum times difference: one hundred squared, minus two squared. Minus four.",
                D('Under 99 · 101 write "(100 − 1)(100 + 1) = 100² − 1"'),
                "Ninety-nine and one hundred one: one away. One hundred squared, minus one.",
                D('Write "(100² − 4) − (100² − 1) = −4 + 1 = −3"'),
                "Now subtract. One hundred squared cancels — you never even calculate it. Minus four, plus one: minus three.",
                D('Circle choice 2'),
                "Choice two.",
                "The trap is the minus before the second bracket. Minus, minus one, is PLUS one. Forget it and you land on minus five — choice one."]),
        ])

    # Question 17 - given a block
    guided(2, 'q-r26-t05-03', 'Given: $a-b=3$.\n$(b-a)^2+2a-2b=\\ ?$',
           ['$-3$', '$3$', '$9$', '$15$'], 4,
           ["Use the block $a-b$. Since $b-a=-(a-b)=-3$, we get $(b-a)^2=(-3)^2=9$.",
            "$2a-2b=2(a-b)=2\\cdot3=6$.",
            "Therefore the expression equals $9+6=15$. The answer is choice 4.",
            "Check with numbers that obey the given, $a=3$ and $b=0$: $(0-3)^2+6-0=9+6=15$ ✓."],
           ["Question seventeen.", "They give you a minus b. Don't hunt for a and b — use the block."], [
            ('Method 1 · Use the block', [
                "We know a minus b is three. We don't know a or b — and we don't need them.",
                D('Under (b − a)² write "= (−3)² = 9"'),
                "b minus a is the opposite of a minus b: minus three. Squared — nine. A square removes the minus.",
                D('Under 2a − 2b write "= 2(a − b) = 2 · 3 = 6"'),
                "Two a minus two b: take out two. Two times the block — six.",
                D('Write "9 + 6 = 15" and circle choice 4'),
                "Nine plus six: fifteen. Choice four.",
                "The traps: keep the minus after squaring and you get minus three. Flip the six and you get three."]),
            ('Method 2 · Plug in', [
                "Don't see the block? Plug in — but only numbers that obey the given.",
                "a minus b must be three. Easiest: a is three, b is zero.",
                D('Write "a = 3, b = 0: (0 − 3)² + 6 − 0 = 9 + 6 = 15"'),
                "Zero minus three, squared: nine. Two a is six. Two b is zero. Fifteen.",
                D('Circle choice 4'),
                "Choice four again. The choices are only numbers. One legal set of numbers settles it."]),
        ])

    # Question 18 - plug-in trap (tie)
    guided(3, 'q-r26-t05-04', 'Given:\n' + _cases('a\\ne0', 'b\\ne0') + '\n$\\dfrac{a^2b+ab^2}{ab}=\\ ?$',
           ['$ab$', '$a+b$', '$2ab$', '$a^2+b^2$'], 2,
           ["Algebra: take out $ab$ on top: $a^2b+ab^2=ab(a+b)$. Cancel $ab$ (not zero): the expression equals $a+b$. The answer is choice 2.",
            "Plug-in trap: with $a=b=1$ the expression is $\\frac{1+1}{1}=2$, and choices 2, 3 and 4 all give $2$ — a tie.",
            "With $a=2$, $b=3$: $\\frac{4\\cdot3+2\\cdot9}{6}=\\frac{30}{6}=5$. Choice 2 gives $5$, choice 3 gives $12$ and choice 4 gives $13$."],
           ["Question eighteen.", "A plug-in question with a trap. Watch what happens with ones."], [
            ('Method 1 · Plug in ones', [
                "Let's try the lazy numbers first: a and b are both one.",
                D('Write "a = b = 1: (1 + 1)/1 = 2"'),
                "One plus one, over one: two.",
                D('Next to the choices write: 1, 2, 2, 2'),
                "Choice one: one. Choice two: two. Choice three: two. Choice four: two.",
                D('Cross out choice 1'),
                "Three choices tie! With ones, a squared, b squared and a b are all equal to one.",
                "We knocked out only one choice. Keep the three tied ones — and pick new numbers."]),
            ('Method 2 · Different numbers', [
                "Different letters, different small values: a is two, b is three.",
                D('Write "a = 2, b = 3: (4 · 3 + 2 · 9)/6 = 30/6 = 5"'),
                "a squared b: four times three, twelve. a b squared: two times nine, eighteen. Thirty over six — five.",
                D('Next to choices 2, 3 and 4 write: 5, 12, 13'),
                "Choice two: five. Choice three: twelve. Choice four: thirteen.",
                D('Circle choice 2'),
                "Only choice two. That's why we avoid zero and one when the choices have powers or products."]),
            ('Method 3 · Common factor', [
                "And the algebra, in one line.",
                D('Write "a²b + ab² = ab(a + b)"'),
                "Both terms on top contain a and b. Take out a b: a b, times a plus b.",
                D('Cancel ab; write "= a + b" and circle choice 2'),
                "Cancel a b — it isn't zero. a plus b. Choice two."]),
        ])

    M.new_card('mem-r26-t05-expressions', TOPIC, ADV, {
        'title': 'Expressions — rules and methods',
        'intro': 'An expression ($=\\ ?$) has one side: simplify, factor or plug in — then match a choice.',
        'tables': [
            {'title': 'Rules', 'head': ['Rule', 'Example'], 'rows': [
                ['$\\frac{a+b}{c}=\\frac{a}{c}+\\frac{b}{c}$ ✓', '$\\frac{10+4}{2}=5+2=7$'],
                ['$\\frac{c}{a+b}\\ne\\frac{c}{a}+\\frac{c}{b}$ ✗', '$\\frac{6}{1+2}=2$, but $\\frac{6}{1}+\\frac{6}{2}=9$'],
                ['$\\frac{|x|}{x}=1$ if $x>0$; $\\frac{|x|}{x}=-1$ if $x<0$', '$\\frac{|-3|}{-3}=\\frac{3}{-3}=-1$'],
                ['Near a round number', '$99\\cdot41=4{,}100-41=4{,}059$'],
                ['Given a block? Put in its value', 'If $x+y=5$: $3x+3y+1=3\\cdot5+1=16$'],
            ]},
            {'title': 'Pick your method', 'head': ['You see', 'Try'], 'rows': [
                ['Small numbers', 'Calculate directly'],
                ['A repeated bracket or a common factor', 'Take it out front'],
                ['A square, sum × difference or $x^2+bx+c$', 'Factor (Topic 4 cards)'],
                ['Letters in the choices and you are stuck', 'Plug in numbers and eliminate three'],
                ['Only numbers in the choices', 'One legal substitution is enough'],
                ['Number choices far apart', 'Estimate'],
            ]},
        ],
        'tips': ['Main fraction bar first; work from the inside out.',
                 'Never cancel a denominator in an expression — only in an equation, from both sides.',
                 'Plug-in numbers: different letters get different values ($2$, $3$, $5$). $0$ and $1$ often cause ties. Obey every condition.',
                 'A tie? Keep only the tied choices and plug in new numbers.'],
    }, after=prev)


# ---------------------------------------------------------------------------------------------------------------
# 4. Practice: rewrite in TeX, remove clones, add exam-hard items, order easy -> hard
# ---------------------------------------------------------------------------------------------------------------
def practice(M):
    S = M.set_q
    S('q-expression-extra-01', stem='$\\frac{9}{\\frac{1}{\\frac{1}{2}+\\frac{1}{6}}}=\\ ?$', choices=['$3$', '$6$', '$9$', '$12$'],
      expl=["Inside out: $\\frac{1}{2}+\\frac{1}{6}=\\frac{3}{6}+\\frac{1}{6}=\\frac{4}{6}=\\frac{2}{3}$.",
            "Next layer: $1\\div\\frac{2}{3}=\\frac{3}{2}$.",
            "Main bar: $9\\div\\frac{3}{2}=9\\cdot\\frac{2}{3}=6$. The answer is choice 2."])
    S('q-expression-extra-04', stem='$(23^2-23)-(22^2+22)=\\ ?$', choices=['$1$', '$22$', '$23$', '$0$'],
      expl=["Take out a common factor: $23^2-23=23\\cdot22$ and $22^2+22=22\\cdot23$.",
            "The two products are equal, therefore the difference is $0$. The answer is choice 4.",
            "Direct calculation: $(529-23)-(484+22)=506-506=0$."])
    S('q-expression-extra-05', stem='Which of the following expressions is necessarily equal to $x^2+13x+40$?',
      choices=['$(x+4)(x+10)$', '$(x+5)(x+8)$', '$(x+2)(x+20)$', '$(x+1)(x+40)$'],
      expl=["Sum and product: we need two numbers with product $40$ and sum $13$. They are $5$ and $8$.",
            "Therefore $x^2+13x+40=(x+5)(x+8)$. The answer is choice 2.",
            "Check with $x=1$: $1+13+40=54$, and choice 2 gives $6\\cdot9=54$ (the others give $55$, $63$ and $82$)."])
    S('q-expression-extra-06', stem='Given: $x<0$.\n$\\frac{|x|}{x}+7=\\ ?$', choices=['$6$', '$7$', '$8$', '$-6$'],
      expl=["$x$ is negative, therefore $|x|=-x$ and $\\frac{|x|}{x}=\\frac{-x}{x}=-1$.",
            "The expression equals $-1+7=6$. The answer is choice 1.",
            "Check with $x=-2$: $\\frac{2}{-2}+7=-1+7=6$ ✓."])
    S('q-expression-extra-07', stem='Given: $a\\ne0$.\n$\\frac{a+4b}{a}=\\ ?$',
      choices=['$1+4b$', '$1+\\frac{4b}{a}$', '$a+\\frac{4b}{a}$', '$4+\\frac{b}{a}$'],
      expl=["A sum on top may be split: $\\frac{a+4b}{a}=\\frac{a}{a}+\\frac{4b}{a}=1+\\frac{4b}{a}$. The answer is choice 2.",
            "Check with $a=2$, $b=1$: $\\frac{2+4}{2}=3$. The choices give $5$, $3$, $4$ and $4\\frac{1}{2}$ — only choice 2 gives $3$."])
    S('q-expression-extra-09', stem='Given: $x\\ne0$.\n$\\left(\\frac{3}{x^2}-\\frac{x}{x^3}\\right)\\cdot\\frac{x^2}{2}=\\ ?$',
      choices=['$1$', '$2$', '$3$', '$x^2$'], correct=1,
      expl=["Cancel $x$ in the second fraction: $\\frac{x}{x^3}=\\frac{1}{x^2}$. The bracket is $\\frac{3}{x^2}-\\frac{1}{x^2}=\\frac{2}{x^2}$.",
            "Then $\\frac{2}{x^2}\\cdot\\frac{x^2}{2}=1$. The answer is choice 1.",
            "The choices are almost all numbers, therefore plugging in is fast: $x=2$ gives $\\left(\\frac{3}{4}-\\frac{2}{8}\\right)\\cdot\\frac{4}{2}=\\frac{1}{2}\\cdot2=1$, and choice 4 would give $4$."])
    S('q-expression-extra-10', stem='Given: $a>4$.\n$\\frac{a^2-16}{a+4}-a=\\ ?$', choices=['$-4$', '$4$', '$0$', '$a-4$'],
      expl=["$a^2-16=(a-4)(a+4)$. Cancel $a+4$: $a-4$. Then $a-4-a=-4$. The answer is choice 1.",
            "Check with $a=5$: $\\frac{25-16}{9}-5=1-5=-4$ ✓."])
    S('q-expression-extra-11', stem='Given: $a\\ne\\pm b$.\n$1+\\frac{2b^2+2ab}{a^2-b^2}=\\ ?$',
      choices=['$\\frac{a+b}{a-b}$', '$\\frac{a-b}{a+b}$', '$\\frac{2b}{a-b}$', '$1$'],
      expl=["Top: $2b^2+2ab=2b(b+a)$. Bottom: $a^2-b^2=(a-b)(a+b)$. Cancel $a+b$: the fraction is $\\frac{2b}{a-b}$.",
            "Then $1+\\frac{2b}{a-b}=\\frac{a-b+2b}{a-b}=\\frac{a+b}{a-b}$. The answer is choice 1.",
            "Check with $a=2$, $b=1$: $1+\\frac{2+4}{3}=3$, and choice 1 gives $\\frac{3}{1}=3$ (the others give $\\frac{1}{3}$, $2$ and $1$)."])
    S('q-expression-extra-12', stem='$\\frac{25{,}704}{63}=\\ ?$', choices=['$308$', '$408$', '$508$', '$608$'],
      expl=["Estimate from a round choice: $63\\cdot400=25{,}200$, a little less than $25{,}704$.",
            "The rest is $25{,}704-25{,}200=504=63\\cdot8$, therefore the answer is $400+8=408$. The answer is choice 2."])
    S('q-expression-extra-13', stem='$(a+b+c)^2-(a+b-c)^2=\\ ?$',
      choices=['$4c(a+b)$', '$2c(a+b)$', '$4ab$', '$c^2$'],
      expl=["Treat $a+b$ as one block $U$: $(U+c)^2-(U-c)^2=(U^2+2Uc+c^2)-(U^2-2Uc+c^2)=4Uc$.",
            "Put the block back: $4c(a+b)$. The answer is choice 1.",
            "Check with $a=1$, $b=2$, $c=3$: $6^2-0^2=36$, and choice 1 gives $4\\cdot3\\cdot3=36$ (the others give $18$, $8$ and $9$)."])
    S('q-expression-extra-14', stem='$(3x+2)^2-(3x-2)^2=\\ ?$', choices=['$12x$', '$24x$', '$36x^2$', '$8$'],
      expl=["Open both squares: $(9x^2+12x+4)-(9x^2-12x+4)=24x$. The answer is choice 2.",
            "Or sum times difference: $[(3x+2)-(3x-2)]\\cdot[(3x+2)+(3x-2)]=4\\cdot6x=24x$.",
            "Check with $x=1$: $25-1=24$ ✓ (choice 1 gives $12$)."])
    S('q-expression-extra-15', stem='Given: $x\\ne5$.\n$\\frac{x^2-10x+25}{x-5}=\\ ?$',
      expl=["The top is $(x-5)^2$. Cancel one factor $x-5$ (not zero): $x-5$. The answer is choice 2.",
            "Check with $x=6$: $\\frac{36-60+25}{1}=1$, and choice 2 gives $6-5=1$ ✓."])
    S('q-expression-extra-16', expl=["Inside the square bracket: $2a-(a-4)=2a-a+4=a+4$.",
                                     "Then $3(a+4)-2(a+1)=3a+12-2a-2=a+10$. The answer is choice 1.",
                                     "Check with $a=0$: $3\\cdot4-2=10$ ✓."])
    S('q-expression-extra-17', stem='Given: $x\\ne0$.\n$\\frac{6x^2+9x}{3x}=\\ ?$',
      expl=["Take out $3x$ on top: $6x^2+9x=3x(2x+3)$. Cancel $3x$: $2x+3$. The answer is choice 1.",
            "Or split the top: $\\frac{6x^2}{3x}+\\frac{9x}{3x}=2x+3$."])
    S('q-expression-extra-18', stem='Which of the following expressions has the same value for every $x>0$?',
      expl=["(1): $(x+1)^2-x^2=2x+1$. (3): $\\frac{x^2}{x}=x$. (4): $2x+1$. These depend on $x$.",
            "(2): $\\frac{x^2-1}{x+1}=\\frac{(x-1)(x+1)}{x+1}=x-1$, therefore the expression is $x-1-x=-1$ for every $x>0$. The answer is choice 2."])
    S('q-expression-extra-19', expl=["Use a round number: $99=100-1$, therefore $99\\cdot41=100\\cdot41-41=4{,}100-41=4{,}059$. The answer is choice 1."])
    S('q-expression-extra-20', stem='Given: $a+b\\ne0$.\n$\\frac{a^2-b^2}{a+b}+b=\\ ?$',
      expl=["$a^2-b^2=(a-b)(a+b)$. Cancel $a+b$ (not zero): $a-b$. Then $a-b+b=a$. The answer is choice 1.",
            "Check with $a=4$, $b=1$: $\\frac{16-1}{5}+1=3+1=4$ ✓."])
    S('q-122', expl=["Inside out: $\\frac{1}{2}+\\frac{1}{4}=\\frac{2}{4}+\\frac{1}{4}=\\frac{3}{4}$.",
                     "Next layer: $1\\div\\frac{3}{4}=\\frac{4}{3}$.",
                     "Main bar: $8\\div\\frac{4}{3}=8\\cdot\\frac{3}{4}=6$. The answer is choice 3."])
    S('q-123', expl=["$n-m=-(m-n)$, therefore $\\frac{m-n}{n-m}=-1$ for every $m\\ne n$.",
                     "The expression is $5-(-1)=5+1=6$. The answer is choice 2."])
    S('q-124', choices=['$2y(p+q)$', '$2(p+q+y)$', '$0$', '$p+q+y$'],
      expl=["Take out the common bracket: $(p+q)[(y-2)+(y+2)]$. Inside, $-2$ and $+2$ cancel: $2y$.",
            "The expression is $(p+q)\\cdot2y=2y(p+q)$. The answer is choice 1."])
    S('alg-extra-unit-t5-1-1', stem='$5x+7y-2x-3y=\\ ?$',
      expl=["Collect like terms: $5x-2x=3x$ and $7y-3y=4y$. The expression is $3x+4y$. The answer is choice 2."])
    S('alg-extra-unit-t5-1-2', stem='$5(x+4)-4(x+1)=\\ ?$',
      expl=["Open the brackets (the minus multiplies both terms): $5x+20-4x-4$.",
            "Collect like terms: $x+16$. The answer is choice 3."])
    S('alg-extra-unit-t5-1-3', stem='Which of the following expressions is necessarily equal to $x^2+12x+35$?',
      expl=["Sum and product: we need two numbers with product $35$ and sum $12$. They are $5$ and $7$.",
            "Therefore $x^2+12x+35=(x+5)(x+7)$. The answer is choice 2. Check: $(x+5)(x+7)=x^2+7x+5x+35$ ✓."])
    S('alg-extra-unit-t5-1-4', stem='Given: $x\\ne5$.\n$\\frac{x^2-25}{x-5}=\\ ?$',
      expl=["Sum times difference: $x^2-25=(x-5)(x+5)$. Cancel $x-5$ (not zero): $x+5$. The answer is choice 3.",
            "Check with $x=6$: $\\frac{36-25}{1}=11$, and choice 3 gives $11$ ✓."])
    S('alg-extra-unit-t5-1-5', stem='$95\\cdot105=\\ ?$', choices=['$9{,}990$', '$9{,}995$', '$9{,}975$', '$10{,}025$'],
      expl=["Both numbers are $5$ away from $100$: $95\\cdot105=(100-5)(100+5)=100^2-5^2=10{,}000-25=9{,}975$. The answer is choice 3."])

    # near-duplicates (repeated-bracket clones, copy of Q10, self/unit twins)
    for qid in ['q-expression-extra-02', 'q-expression-extra-03', 'q-expression-extra-08',
                'alg-extra-expression-self-1', 'alg-extra-expression-self-2', 'alg-extra-expression-self-3',
                'alg-extra-expression-self-4', 'alg-extra-expression-self-5', 'alg-extra-expression-self-6',
                'alg-extra-expression-self-7', 'alg-extra-unit-t5-1-6', 'alg-extra-unit-t5-1-7']:
        M.unplace(qid)

    new = [
        ('q-r26-t05-05', 'Given: $x-2y=4$.\n$3x-6y-(2y-x)^2=\\ ?$', ['$-28$', '$-4$', '$4$', '$28$'], 2,
         ["Use the block $x-2y$. $3x-6y=3(x-2y)=3\\cdot4=12$.",
          "$2y-x=-(x-2y)=-4$, therefore $(2y-x)^2=(-4)^2=16$.",
          "The expression equals $12-16=-4$. The answer is choice 2.",
          "Check with $x=4$, $y=0$: $12-0-(0-4)^2=12-16=-4$ ✓."]),
        ('q-r26-t05-06', 'Given: $\\frac{a}{b}=3$.\n$\\frac{a-b}{a+b}=\\ ?$', ['$\\frac{1}{2}$', '$\\frac{2}{3}$', '$2$', '$\\frac{1}{3}$'], 1,
         ["Plug in numbers that obey the given: $a=3$, $b=1$. Then $\\frac{3-1}{3+1}=\\frac{2}{4}=\\frac{1}{2}$. The answer is choice 1.",
          "Any other legal pair gives the same value, for example $a=6$, $b=2$: $\\frac{4}{8}=\\frac{1}{2}$.",
          "Algebra: $a=3b$, therefore $\\frac{a-b}{a+b}=\\frac{3b-b}{3b+b}=\\frac{2b}{4b}=\\frac{1}{2}$."]),
        ('q-r26-t05-07', 'Given: $x-\\frac{1}{x}=3$.\n$x^2+\\frac{1}{x^2}=\\ ?$', ['$9$', '$7$', '$11$', '$5$'], 3,
         ["Square the block: $\\left(x-\\frac{1}{x}\\right)^2=x^2-2\\cdot x\\cdot\\frac{1}{x}+\\frac{1}{x^2}=x^2-2+\\frac{1}{x^2}$.",
          "Therefore $x^2-2+\\frac{1}{x^2}=3^2=9$, and $x^2+\\frac{1}{x^2}=9+2=11$. The answer is choice 3.",
          "The traps: $9$ forgets the middle term; $7$ subtracts $2$ as in $\\left(x+\\frac{1}{x}\\right)^2$ — here the middle term is $-2$."]),
        ('q-r26-t05-08', '$999\\cdot25=\\ ?$', ['$24{,}925$', '$24{,}975$', '$24{,}995$', '$25{,}025$'], 2,
         ["Use a round number: $999=1{,}000-1$.",
          "Therefore $999\\cdot25=1{,}000\\cdot25-25=25{,}000-25=24{,}975$. The answer is choice 2."]),
        ('q-r26-t05-09', '$\\frac{101^2-99^2}{4}=\\ ?$', ['$1$', '$50$', '$100$', '$200$'], 3,
         ["Sum times difference: $101^2-99^2=(101-99)(101+99)=2\\cdot200=400$.",
          "Then $\\frac{400}{4}=100$. The answer is choice 3."]),
        ('q-r26-t05-10', 'Given: $x\\ne2$.\n$\\frac{x^2+4x-12}{x-2}=\\ ?$', ['$x-6$', '$x+2$', '$x+6$', '$x^2+6$'], 3,
         ["Sum and product: we need two numbers with product $-12$ and sum $4$. They are $6$ and $-2$.",
          "Therefore $x^2+4x-12=(x+6)(x-2)$. Cancel $x-2$ (not zero): $x+6$. The answer is choice 3.",
          "Check with $x=3$: $\\frac{9+12-12}{1}=9$, and choice 3 gives $9$ (choice 4 gives $15$). Careful: $x=0$ or $x=1$ makes choices 3 and 4 tie."]),
        ('q-r26-t05-11', 'Given: $x\\ne0$.\n$\\frac{x^3+x^2}{x}=\\ ?$', ['$2x$', '$x+1$', '$x^2+x$', '$2x^2$'], 3,
         ["Take out $x$ on top: $x^3+x^2=x(x^2+x)$. Cancel $x$: $x^2+x$. The answer is choice 3.",
          "Plug-in trap: with $x=1$ the expression is $2$, and ALL four choices give $2$.",
          "With $x=2$: $\\frac{8+4}{2}=6$. The choices give $4$, $3$, $6$ and $8$ — only choice 3."]),
        ('q-r26-t05-12', 'Given: $a\\ne b$.\n$\\frac{a^2-b^2}{a-b}-2b=\\ ?$', ['$a+b$', '$a-b$', '$a$', '$b-a$'], 2,
         ["$a^2-b^2=(a-b)(a+b)$. Cancel $a-b$ (not zero, because $a\\ne b$): $a+b$. Then $a+b-2b=a-b$. The answer is choice 2.",
          "Plug-in trap: $a=1$, $b=0$ gives $1$, and choices 1, 2 and 3 all give $1$.",
          "With $a=3$, $b=1$: $\\frac{9-1}{2}-2=4-2=2$. The choices give $4$, $2$, $3$ and $-2$ — only choice 2."]),
        ('q-r26-t05-13', 'For every $x>0$ and $y>0$, which of the following expressions is equal to $\\frac{6}{x+y}$?',
         ['$\\frac{6}{x}+\\frac{6}{y}$', '$\\frac{3}{x}+\\frac{3}{y}$', '$\\frac{12}{2x+2y}$', '$\\frac{12}{2x+y}$'], 3,
         ["Multiplying the top and the bottom by the same number keeps the value: $\\frac{6\\cdot2}{(x+y)\\cdot2}=\\frac{12}{2x+2y}$. The answer is choice 3.",
          "A sum on the bottom may not be split, therefore choices 1 and 2 are traps. With $x=y=1$: $\\frac{6}{2}=3$, but choice 1 gives $12$ and choice 2 gives $6$.",
          "Choice 4 multiplies only $x$ by $2$: with $x=y=1$ it gives $\\frac{12}{3}=4$."]),
        ('q-r26-t05-14', 'Given: $x<0<y$.\nWhich of the following expressions is necessarily positive?',
         ['$x+y$', '$xy$', '$y-x$', '$\\frac{x}{y}$'], 3,
         ["$x$ is negative, therefore $-x$ is positive, and $y-x=y+(-x)$ is a sum of two positive numbers: positive. The answer is choice 3.",
          "$xy$ and $\\frac{x}{y}$ are negative (the signs are different).",
          "$x+y$ can be negative: $x=-5$, $y=1$ gives $-4$."]),
        ('q-r26-t05-15', 'Given:\n' + _cases('x\\ne0', 'x\\ne-1') + '\n$\\frac{1}{1+\\frac{1}{x}}=\\ ?$',
         ['$\\frac{x+1}{x}$', '$\\frac{1}{x+1}$', '$\\frac{x}{x+1}$', '$1+x$'], 3,
         ["Inside out: $1+\\frac{1}{x}=\\frac{x}{x}+\\frac{1}{x}=\\frac{x+1}{x}$.",
          "Then $1\\div\\frac{x+1}{x}=\\frac{x}{x+1}$. The answer is choice 3.",
          "Plug-in trap: $x=1$ gives $\\frac{1}{2}$, and choices 2 and 3 both give $\\frac{1}{2}$. With $x=2$: $\\frac{1}{1+\\frac{1}{2}}=\\frac{2}{3}$; only choice 3 gives $\\frac{2}{3}$."]),
        ('q-r26-t05-16', 'Given: $a>2$.\n$\\frac{a^2+2a}{a}-\\frac{a^2-4}{a-2}=\\ ?$', ['$4$', '$0$', '$-4$', '$2a+4$'], 2,
         ["First fraction: $\\frac{a(a+2)}{a}=a+2$. Second fraction: $\\frac{(a-2)(a+2)}{a-2}=a+2$.",
          "Therefore the expression equals $(a+2)-(a+2)=0$. The answer is choice 2.",
          "Check with $a=3$: $\\frac{15}{3}-\\frac{5}{1}=5-5=0$ ✓."]),
    ]
    for qid, stem, ch, c, ex in new:
        M.new_q(qid, TOPIC, stem, ch, c, ex)
        M.place_q(qid, SELF)

    M.practice_order(SELF, [
        'q-expression-extra-16', 'q-expression-extra-06', 'q-expression-extra-17', 'q-expression-extra-07',
        'q-expression-extra-04', 'q-expression-extra-01', 'q-expression-extra-19', 'q-r26-t05-08',
        'q-expression-extra-12', 'q-expression-extra-05', 'q-expression-extra-15', 'q-expression-extra-10',
        'q-expression-extra-20', 'q-expression-extra-09', 'q-expression-extra-18', 'q-r26-t05-14',
        'q-r26-t05-13', 'q-r26-t05-11', 'q-r26-t05-12', 'q-expression-extra-13', 'q-expression-extra-14',
        'q-r26-t05-09', 'q-r26-t05-10', 'q-r26-t05-16', 'q-expression-extra-11', 'q-r26-t05-05',
        'q-r26-t05-06', 'q-r26-t05-15', 'q-r26-t05-07'])
    M.practice_order(BANK, ['alg-extra-unit-t5-1-1', 'alg-extra-unit-t5-1-2', 'q-123', 'q-124', 'q-122',
                            'alg-extra-unit-t5-1-5', 'alg-extra-unit-t5-1-4', 'alg-extra-unit-t5-1-3'])


def so_fixes(M):
    """'so' meaning 'therefore' mid-sentence -> separate sentences."""
    _replace(M, 'solve-q-136', 2, "And that's the rule: swap the order of the two terms and it's ALWAYS negative one — whatever numbers you plug in. p isn't equal to q, so we're safe from zero over zero.",
             "And that's the rule: swap the order of the two terms and it's ALWAYS negative one — whatever numbers you plug in. p isn't equal to q. Therefore we're safe from zero over zero.")
    _replace(M, 'solve-q-137', 3, "Why ones? You could use one, two, three — or ten, thirteen, seventy-two. Nothing says the letters must be different, so pick the easiest: all ones.",
             "Why ones? You could use one, two, three — or ten, thirteen, seventy-two. Nothing says the letters must be different. So pick the easiest: all ones.")
    _replace(M, 'solve-q-126', 3, "We usually plug in ones — but not here. We subtract q, r and s from p, so p equal to them gives a negative answer. And the choices would come out the same.",
             "We usually plug in ones — but not here. We subtract q, r and s from p. If p equals them, the answer is negative. And the choices would come out the same.")
    _replace(M, 'solve-q-134', 3, "The units-digit trick? Here it can't help — eight times three is twenty-four, so every choice times sixty-three ends in four. Same as the top.",
             "The units-digit trick? Here it can't help. Eight times three is twenty-four. Therefore every choice times sixty-three ends in four — same as the top.")


def apply(M):
    lesson(M)
    guided_fixes(M)
    shortcuts(M)
    practice(M)
    so_fixes(M)
