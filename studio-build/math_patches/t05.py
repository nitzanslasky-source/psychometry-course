"""Topic 5 (Expressions) - course review 2026-09 fixes. See t05_CHANGES.md."""
import re
from math_api import T, H, A, D, Q, rich_plain

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
        "So the bottom is the top with a minus. Any number over its opposite — negative one.",
        "Honestly? Trust it. It's always negative one."])     # pass 2: original line restored (it is true)
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
    # Q11 and Q12 (pass 2): the ORIGINAL questions are restored (negative exponents, a^0) and move to Topic 8 -
    # see restore_moved(). Their original solution videos are no longer edited here.

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
# 3. New lesson video + three guided questions (Questions 15-17) + memory card
# ---------------------------------------------------------------------------------------------------------------
def shortcuts(M):
    vid = 'r26-t05-shortcuts'
    M.new_video(vid, TOPIC, 'Exam Shortcuts', ['Sum and product', 'Round numbers', 'Given a block', 'Recap'], [
        dict(mode='title', title='Exam Shortcuts', script=[
            "Exam shortcuts — tools strong students use.",
            "A quick reminder on factoring x squared plus b x plus c. Then multiplying near a round number. And using a block they give you.",
            "Each one turns a long calculation into one line."]),
        dict(title='Sum and product', mode='concept', active=0, pre=[], script=[
            A('Need to factor x² + bx + c? appears', T('Need to factor $x^2+bx+c$? Open the choices and check with a number', size=40)),
            "Need to factor x squared plus b x plus c? Open the choices and check with a number.",
            "Or the quick way: two numbers with that sum and product.",
            A('x² + 9x + 20: product 20, sum 9 → 4 and 5 appears', T('$x^2+9x+20$: product $=20$, sum $=9$ → $4$ and $5$', size=44)),
            "x squared plus nine x plus twenty. Two numbers: product twenty, sum nine. Four and five.",
            A('= (x + 4)(x + 5) appears', T('$=(x+4)(x+5)$', size=50)),
            "x plus four, times x plus five. Open the brackets to check: nine x in the middle, twenty at the end.",
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
            A("'x² + bx + c? Check with a number' appears", T('$x^2+bx+c$? Check with a number, or sum and product', size=42)),
            A("'Near a round number' appears", T('Near a round number? $(100-1)\\cdot41$ · $(100-4)(100+4)$', size=40)),
            A("'Given a block? Put in its value' appears", T('Given a block? Find it and put in its value', size=42)),
            A("'Plug in numbers that obey the given' appears", T('Plugging in? Use numbers that obey the given', size=42)),
            "Three guided questions next — round numbers, a given block, and one plug-in trap. Try each one first.",
        ]),
    ], ADV, after='solve-q-134')

    qn = M.next_question_number(TOPIC)   # 15
    sb = ['Question %d' % (qn + k) for k in range(3)]
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
        M.video('solve-' + qid)['beats'][0]['title'] = 'Exam Shortcuts'   # like the base videos; keeps renumbering single-pass
        prev = 'solve-' + qid

    # (2026-10-04) The old Question 15, q-r26-t05-01 (x^2-2x-15 over x-5, sum and product with signs), and its solution
    # video were removed: they needed the sign rules of the removed Topic 4 trinomial lesson (0 real exam questions).

    # Question 15 - round numbers
    guided(0, 'q-r26-t05-02', '$98\\cdot102-99\\cdot101=\\ ?$',
           ['$-5$', '$-3$', '$3$', '$5$'], 2,
           ["Both products are sum times difference around $100$: $98\\cdot102=(100-2)(100+2)=100^2-4$ and $99\\cdot101=(100-1)(100+1)=100^2-1$.",
            "Therefore the expression is $(100^2-4)-(100^2-1)=-4+1=-3$. The answer is choice 2.",
            "Check: $98\\cdot102=9{,}996$ and $99\\cdot101=9{,}999$; $9{,}996-9{,}999=-3$ ✓."],
           ["Question fifteen.", "Two big products — and no calculator. Look for a round number."], [
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

    # Question 16 - given a block
    guided(1, 'q-r26-t05-03', 'Given: $a-b=3$.\n$(b-a)^2+2a-2b=\\ ?$',
           ['$-3$', '$3$', '$9$', '$15$'], 4,
           ["Use the block $a-b$. Since $b-a=-(a-b)=-3$, we get $(b-a)^2=(-3)^2=9$.",
            "$2a-2b=2(a-b)=2\\cdot3=6$.",
            "Therefore the expression equals $9+6=15$. The answer is choice 4.",
            "Check with numbers that obey the given, $a=3$ and $b=0$: $(0-3)^2+6-0=9+6=15$ ✓."],
           ["Question sixteen.", "They give you a minus b. Don't hunt for a and b — use the block."], [
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

    # Question 17 - plug-in trap (tie)
    guided(2, 'q-r26-t05-04', 'Given:\n' + _cases('a\\ne0', 'b\\ne0') + '\n$\\dfrac{a^2b+ab^2}{ab}=\\ ?$',
           ['$ab$', '$a+b$', '$2ab$', '$a^2+b^2$'], 2,
           ["Algebra: take out $ab$ on top: $a^2b+ab^2=ab(a+b)$. Cancel $ab$ (not zero): the expression equals $a+b$. The answer is choice 2.",
            "Plug-in trap: with $a=b=1$ the expression is $\\frac{1+1}{1}=2$, and choices 2, 3 and 4 all give $2$ — a tie.",
            "With $a=2$, $b=3$: $\\frac{4\\cdot3+2\\cdot9}{6}=\\frac{30}{6}=5$. Choice 2 gives $5$, choice 3 gives $12$ and choice 4 gives $13$."],
           ["Question seventeen.", "A plug-in question with a trap. Watch what happens with ones."], [
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
                ['A square or sum × difference', 'Factor (Topic 4)'],
                ['$x^2+bx+c$ and factored choices', 'Check with a number, or sum and product'],
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
      expl=["Open the choices. Each one is $(x+p)(x+q)=x^2+(p+q)x+pq$. In every choice $pq=40$, therefore the last number always fits. Compare the middle numbers: we need $p+q=13$.",
            "The sums are $4+10=14$, $5+8=13$, $2+20=22$ and $1+40=41$. Only choice 2 fits: $x^2+13x+40=(x+5)(x+8)$. The answer is choice 2.",
            "Check with a number, $x=1$: $1+13+40=54$, and choice 2 gives $6\\cdot9=54$ (the others give $55$, $63$ and $82$).",
            "The quick way (sum and product): two numbers with sum $13$ and product $40$ are $5$ and $8$."])
    S('q-expression-extra-06', stem='Given: $x<0$.\n$\\frac{|x|}{x}+7=\\ ?$', choices=['$6$', '$7$', '$8$', '$-6$'],
      expl=["$x$ is negative, therefore $|x|=-x$ and $\\frac{|x|}{x}=\\frac{-x}{x}=-1$.",
            "The expression equals $-1+7=6$. The answer is choice 1.",
            "Check with $x=-2$: $\\frac{2}{-2}+7=-1+7=6$ ✓."])
    S('q-expression-extra-07', stem='Given: $a\\ne0$.\n$\\frac{a+4b}{a}=\\ ?$',
      choices=['$1+4b$', '$1+\\frac{4b}{a}$', '$a+\\frac{4b}{a}$', '$4+\\frac{b}{a}$'],
      expl=["A sum on top may be split: $\\frac{a+4b}{a}=\\frac{a}{a}+\\frac{4b}{a}=1+\\frac{4b}{a}$. The answer is choice 2.",
            "Check with $a=2$, $b=1$: $\\frac{2+4}{2}=3$. The choices give $5$, $3$, $4$ and $4\\frac{1}{2}$ — only choice 2 gives $3$."])
    # q-expression-extra-09: original restored and moved to Topic 8 (pass 2) - see restore_moved()
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
      expl=["Open the choices. Each one is $(x+p)(x+q)=x^2+(p+q)x+pq$: the middle number is $p+q$, the last number is $pq$. We need $p+q=12$ and $pq=35$.",
            "Choice 1: $1+35=36$. Choice 3: $4+8=12$, but $4\\cdot8=32$. Choice 4: $(-5)+(-7)=-12$. Choice 2: $5+7=12$ and $5\\cdot7=35$. The answer is choice 2: $x^2+12x+35=(x+5)(x+7)$.",
            "Check with a number, $x=1$: $1+12+35=48$. The choices give $2\\cdot36=72$, $6\\cdot8=48$, $5\\cdot9=45$ and $(-4)(-6)=24$. Only choice 2 gives $48$.",
            "The quick way (sum and product): two numbers with sum $12$ and product $35$ are $5$ and $7$."])
    S('alg-extra-unit-t5-1-4', stem='Given: $x\\ne5$.\n$\\frac{x^2-25}{x-5}=\\ ?$',
      expl=["Sum times difference: $x^2-25=(x-5)(x+5)$. Cancel $x-5$ (not zero): $x+5$. The answer is choice 3.",
            "Check with $x=6$: $\\frac{36-25}{1}=11$, and choice 3 gives $11$ ✓."])
    S('alg-extra-unit-t5-1-5', stem='$95\\cdot105=\\ ?$', choices=['$9{,}990$', '$9{,}995$', '$9{,}975$', '$10{,}025$'],
      expl=["Both numbers are $5$ away from $100$: $95\\cdot105=(100-5)(100+5)=100^2-5^2=10{,}000-25=9{,}975$. The answer is choice 3."])

    # pass 2: the 12 original practice items are restored (plan), with TeX and full numeric solutions
    S('q-expression-extra-02', stem='Given: $a\\ne b$.\n$4-\\frac{a-b}{b-a}=\\ ?$', choices=['$3$', '$4$', '$5$', '$-5$'],
      expl=["Since $b-a=-(a-b)$, the fraction $\\frac{a-b}{b-a}$ equals $-1$.",
            "Therefore the expression is $4-(-1)=4+1=5$. The answer is choice 3.",
            "Check with $a=5$, $b=2$: $4-\\frac{3}{-3}=4+1=5$ ✓."])
    S('q-expression-extra-03', stem='$(u+v)(t-5)+(u+v)(t+5)=\\ ?$',
      choices=['$2t(u+v)$', '$10(u+v)$', '$2t+u+v$', '$0$'],
      expl=["Take out the common bracket: $(u+v)[(t-5)+(t+5)]$. Inside, $-5$ and $+5$ cancel: $2t$.",
            "The expression is $(u+v)\\cdot2t=2t(u+v)$. The answer is choice 1."])
    S('q-expression-extra-08', stem='Given: $p\\ne q$.\n$\\frac{(p-q)-(q-p)}{p-q}=\\ ?$', choices=['$0$', '$1$', '$2$', '$p-q$'],
      expl=["The minus stands in front of the second bracket only: $(p-q)-(q-p)=p-q-q+p=2p-2q=2(p-q)$.",
            "Cancel $p-q$ (not zero, because $p\\ne q$): $\\frac{2(p-q)}{p-q}=2$. The answer is choice 3."])
    S('alg-extra-expression-self-1', stem='$4x+6y-2x-3y=\\ ?$',
      expl=["Collect like terms: $4x-2x=2x$ and $6y-3y=3y$. The expression is $2x+3y$. The answer is choice 3."])
    S('alg-extra-expression-self-2', stem='$4(x+4)-3(x+1)=\\ ?$',
      expl=["Open the brackets (the minus multiplies both terms): $4x+16-3x-3$.",
            "Collect like terms: $x+13$. The answer is choice 2."])
    S('alg-extra-expression-self-3', stem='Which of the following expressions is necessarily equal to $x^2+10x+24$?',
      expl=["Open the choices. Each one is $(x+p)(x+q)=x^2+(p+q)x+pq$: the middle number is $p+q$, the last number is $pq$. We need $p+q=10$ and $pq=24$.",
            "Choice 1: $(-4)+(-6)=-10$. Choice 2: $1+24=25$. Choice 4: $3+7=10$, but $3\\cdot7=21$. Choice 3: $4+6=10$ and $4\\cdot6=24$. The answer is choice 3: $x^2+10x+24=(x+4)(x+6)$.",
            "Check with a number, $x=1$: $1+10+24=35$. The choices give $(-3)(-5)=15$, $2\\cdot25=50$, $5\\cdot7=35$ and $4\\cdot8=32$. Only choice 3 gives $35$.",
            "The quick way (sum and product): two numbers with sum $10$ and product $24$ are $4$ and $6$."])
    S('alg-extra-expression-self-4', stem='Given: $x\\ne4$.\n$\\frac{x^2-16}{x-4}=\\ ?$',
      expl=["Sum times difference: $x^2-16=(x-4)(x+4)$. Cancel $x-4$ (not zero): $x+4$. The answer is choice 3.",
            "Check with $x=5$: $\\frac{25-16}{1}=9$, and choice 3 gives $9$ ✓."])
    S('alg-extra-expression-self-5', stem='$96\\cdot104=\\ ?$', choices=['$9{,}996$', '$9{,}984$', '$10{,}016$', '$9{,}992$'],
      expl=["Both numbers are $4$ away from $100$: $96\\cdot104=(100-4)(100+4)=100^2-4^2=10{,}000-16=9{,}984$. The answer is choice 2."])
    S('alg-extra-expression-self-6', stem='$(u+v)(w-4)+(u+v)(w+4)=\\ ?$',
      expl=["Take out the common bracket: $(u+v)[(w-4)+(w+4)]$. Inside, $-4$ and $+4$ cancel: $2w$.",
            "The expression is $(u+v)\\cdot2w=2w(u+v)$. The answer is choice 1."])
    S('alg-extra-expression-self-7', stem='Given: $x\\ne0$.\n$\\frac{4x^2+24x}{4x}=\\ ?$',
      expl=["Take out $4x$ on top: $4x^2+24x=4x(x+6)$. Cancel $4x$ (not zero): $x+6$. The answer is choice 2.",
            "Or split the top: $\\frac{4x^2}{4x}+\\frac{24x}{4x}=x+6$."])
    S('alg-extra-unit-t5-1-6', stem='$(u+v)(w-5)+(u+v)(w+5)=\\ ?$',
      expl=["Take out the common bracket: $(u+v)[(w-5)+(w+5)]$. Inside, $-5$ and $+5$ cancel: $2w$.",
            "The expression is $(u+v)\\cdot2w=2w(u+v)$. The answer is choice 4."])
    S('alg-extra-unit-t5-1-7', stem='Given: $x\\ne0$.\n$\\frac{5x^2+35x}{5x}=\\ ?$',
      expl=["Take out $5x$ on top: $5x^2+35x=5x(x+7)$. Cancel $5x$ (not zero): $x+7$. The answer is choice 3.",
            "Or split the top: $\\frac{5x^2}{5x}+\\frac{35x}{5x}=x+7$."])

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
        'alg-extra-expression-self-1', 'alg-extra-expression-self-2', 'q-expression-extra-16', 'q-expression-extra-06',
        'q-expression-extra-02', 'q-expression-extra-17', 'alg-extra-expression-self-7', 'q-expression-extra-07',
        'q-expression-extra-03', 'alg-extra-expression-self-6', 'q-expression-extra-08', 'q-expression-extra-04',
        'q-expression-extra-01', 'q-expression-extra-19', 'alg-extra-expression-self-5', 'q-r26-t05-08',
        'q-expression-extra-12', 'alg-extra-expression-self-3', 'q-expression-extra-05', 'alg-extra-expression-self-4',
        'q-expression-extra-15', 'q-expression-extra-10', 'q-expression-extra-20', 'q-expression-extra-18', 'q-r26-t05-14',
        'q-r26-t05-13', 'q-r26-t05-11', 'q-r26-t05-12', 'q-expression-extra-13', 'q-expression-extra-14',
        'q-r26-t05-09', 'q-r26-t05-16', 'q-expression-extra-11', 'q-r26-t05-05',
        'q-r26-t05-06', 'q-r26-t05-15', 'q-r26-t05-07'])
    M.practice_order(BANK, ['alg-extra-unit-t5-1-1', 'alg-extra-unit-t5-1-2', 'q-123', 'q-124', 'alg-extra-unit-t5-1-6',
                            'alg-extra-unit-t5-1-7', 'q-122', 'alg-extra-unit-t5-1-5', 'alg-extra-unit-t5-1-4',
                            'alg-extra-unit-t5-1-3'])


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


# ---------------------------------------------------------------------------------------------------------------
# 5. Pass 2: restore the originals q-131, q-132, q-expression-extra-09 and move them to Topic 8 (after `exponents`)
# ---------------------------------------------------------------------------------------------------------------
T8_CORE, T8_PRACTICE = 'exponent-core', 'exponent-extra'
MOVED_SOLVE = ('solve-q-131', 'solve-q-132')


def restore_moved(M):
    # original stems/choices/keys, text clean-up only (TeX, no ':' division, numbers in the solutions)
    M.set_q('q-131', stem='Given: $x\\ne0$.\n$\\left(x^{-2}+\\frac{4x^2}{x^4}\\right)\\cdot\\frac{1}{5}\\cdot\\frac{5}{x^{-2}}=\\ ?$',
            expl=["A negative power flips: $x^{-2}=\\frac{1}{x^2}$. Cancel $x^2$ in the second fraction: $\\frac{4x^2}{x^4}=\\frac{4}{x^2}$.",
                  "The bracket equals $\\frac{1}{x^2}+\\frac{4}{x^2}=\\frac{5}{x^2}$.",
                  "The negative power in the denominator moves up: $\\frac{5}{x^{-2}}=5x^2$.",
                  "The expression is $\\frac{5}{x^2}\\cdot\\frac{1}{5}\\cdot5x^2=5$. The answer is choice 3.",
                  "Faster: the choices are numbers only. With $x=1$: $(1+4)\\cdot\\frac{1}{5}\\cdot5=5$."])
    M.set_q('q-132', choices=['$(a+3a)-(3a-a)$', '$\\dfrac{(a+2)+(a+2)^2}{a+3}$', '$a^0+(-1)^a$', '$\\dfrac{a^2-9}{a+3}-a$'], correct=4,
            expl=["(1): $4a-2a=2a$. It depends on $a$.",
                  "(2): take out $a+2$ on top: $(a+2)+(a+2)^2=(a+2)(1+a+2)=(a+2)(a+3)$. Cancel $a+3$: $a+2$. It depends on $a$.",
                  "(3): $a^0=1$, but $(-1)^a$ is $1$ when $a$ is even and $-1$ when $a$ is odd. The expression is $2$ or $0$. It depends on $a$.",
                  "(4): $\\frac{a^2-9}{a+3}=\\frac{(a-3)(a+3)}{a+3}=a-3$, therefore the expression is $(a-3)-a=-3$ for every $a$. The answer is choice 4."])
    M.set_q('q-expression-extra-09', stem='Given: $x\\ne0$.\n$\\left(x^{-2}+\\frac{2}{x^2}\\right)\\cdot x^2=\\ ?$',
            choices=['$1$', '$2$', '$3$', '$x^2$'], correct=3,
            expl=["$x^{-2}=\\frac{1}{x^2}$, therefore the bracket equals $\\frac{1}{x^2}+\\frac{2}{x^2}=\\frac{3}{x^2}$.",
                  "Then $\\frac{3}{x^2}\\cdot x^2=3$. The answer is choice 3.",
                  "Or multiply each term by $x^2$: $x^{-2}\\cdot x^2+\\frac{2}{x^2}\\cdot x^2=x^0+2=1+2=3$."])
    for q in ('q-131', 'q-132'):
        v = M.video('solve-' + q); v['title'] = v['navLabel'] = rich_plain(M.q(q)['stemRich'])
    # the Advanced Expressions sidebars no longer list Questions 11 and 12 (renumbering happens after all patches)
    for f in M.D['flow']:
        if f['section'] == ADV and f['type'] == 'video' and f['ref'].startswith('solve-q-1'):
            hy = M.video(f['ref'])['hybrid']
            hy['sidebar'] = [x for x in hy.get('sidebar', []) if x not in ('Question 11', 'Question 12')]
    # move to Topic 8: guided pair into the core section (after the T8 guided questions), extra-09 into T8 practice
    M.move('q-131', T8_CORE); M.move('solve-q-131', T8_CORE, after='q-131')
    M.move('q-132', T8_CORE, after='solve-q-131'); M.move('solve-q-132', T8_CORE, after='q-132')
    M.move('q-expression-extra-09', T8_PRACTICE)
    M.touched_videos.update(MOVED_SOLVE)
    # Topic 8's patch runs after this one: finish the move once every patch has run
    fin = M.finish
    def finish():
        _t8_fixup(M)
        fin()
    M.finish = finish


def _t8_fixup(M):
    D, flow = M.D, M.D['flow']
    def is_sol(ref):
        v = D['videos'].get(ref) or {}
        return v.get('kind') == 'solution' and bool(v.get('beats')) and re.match(r'Question \d+$', v['beats'][0].get('bigTitle') or '')
    others = [f['ref'] for f in flow if f['section'] == T8_CORE and f['type'] == 'video' and f['ref'] not in MOVED_SOLVE and is_sol(f['ref'])]
    if others:                          # after the last Topic 8 guided question
        M.move('q-131', T8_CORE, after=others[-1]); M.move('solve-q-131', T8_CORE, after='q-131')
        M.move('q-132', T8_CORE, after='solve-q-131'); M.move('solve-q-132', T8_CORE, after='q-132')
    prac = [f['ref'] for f in flow if f['section'] == T8_PRACTICE]
    for anchor in ('alg-extra-exponent-extra-4', 'q-230'):     # next to the other negative-exponent item
        if anchor in prac:
            M.move('q-expression-extra-09', T8_PRACTICE, after=anchor); break
    for vid in MOVED_SOLVE: D['videos'][vid]['topic'] = 8
    # one sidebar for all Topic 8 guided questions (old numbers; renumber_guided maps them afterwards)
    sols = [f['ref'] for f in flow if f['topic'] == 8 and f['type'] == 'video' and is_sol(f['ref'])]
    labels = ['Question %s' % D['videos'][v]['beats'][0]['bigTitle'].split()[1] for v in sols]
    ref = D['videos'][others[0]]['hybrid'] if others else None
    for v in sols:
        hy = D['videos'][v].setdefault('hybrid', {})
        if v in MOVED_SOLVE or all(re.match(r'Question \d+$', x) for x in hy.get('sidebar', [])):
            hy['sidebar'] = list(labels); M.touched_videos.add(v)
            k = sols.index(v)
            for b in D['videos'][v]['beats']:
                if b.get('mode') != 'title': b['active'] = k
        if v in MOVED_SOLVE and ref:
            hy['title'] = ref.get('title', hy.get('title')); hy['num'] = ref.get('num', hy.get('num'))


# ---------------------------------------------------------------------------------------------------------------
# 6. Pass 2: summary lesson right before the practice
# ---------------------------------------------------------------------------------------------------------------
def summary(M):
    sb = ['Expression or equation?', 'Splitting a fraction', 'The main fraction bar', 'Opposite brackets',
          'Take it out front', 'Round numbers', 'Given a block', 'Plug in numbers', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of expressions.",
            "Everything you need, one idea at a time."]),
        S(0, [
            A('Expression: = ? appears', T('Expression: something $=\\ ?$ · one side', size=46)),
            "An expression has one side. Something equals a question mark.",
            A('1/a + 1/b = (a + b)/ab appears', T('$\\frac{1}{a}+\\frac{1}{b}=\\frac{a+b}{ab}$', size=56)),
            "So the denominator stays. You may never just wipe it away.",
            "Only in an equation can you clear a denominator — from both sides."]),
        S(1, [
            A('Split rule appears', T('$\\frac{a+b}{c}=\\frac{a}{c}+\\frac{b}{c}$ ✓', size=56)),
            "A sum on top? You may split it.",
            A('Trap appears', T('$\\frac{c}{a+b}\\ne\\frac{c}{a}+\\frac{c}{b}$ ✗', size=56)),
            "A sum on the bottom? Never.",
            "Twelve over one plus three is three. Split it wrongly and you get sixteen."]),
        S(2, [
            A('Main bar rule appears', T('Main bar first · work from the inside out', size=46)),
            "Many fraction bars? Find the longest one — the main bar.",
            "Then start from the deepest layer and work outward. One layer at a time.",
            A('Example appears', T('$3\\div\\frac{3}{4}=3\\cdot\\frac{4}{3}=4$', size=50)),
            "And dividing by a fraction means multiplying by its reciprocal."]),
        S(3, [
            A('(a − b)/(b − a) = −1 appears', T('$\\frac{a-b}{b-a}=-1$, when $a\\ne b$', size=54)),
            "Same two letters, opposite order: always negative one.",
            A('b − a = −(a − b) appears', T('$b-a=-(a-b)$', size=50)),
            "Because b minus a is minus, a minus b.",
            "Watch the minus in front of a bracket. It flips every sign inside."]),
        S(4, [
            A('Repeated bracket appears', T('$(x-y)(m+3)+(x-y)(m-3)=(x-y)\\cdot2m$', size=44)),
            "A bracket that repeats? Treat it as one object and take it out front.",
            A('Sum and product appears', T('$x^2+11x+28=(x+4)(x+7)$', size=50)),
            "A trinomial? Sum and product, from Topic 4. Product twenty-eight, sum eleven: four and seven.",
            "Factor first — then cancel what cancels."]),
        S(5, [
            A('99 · 53 appears', T('$99\\cdot53=100\\cdot53-53=5{,}247$', size=50)),
            "No calculator. Look for a round number nearby.",
            A('93 · 107 appears', T('$93\\cdot107=100^2-7^2=9{,}951$', size=50)),
            "Two numbers the same distance from a round number? Sum times difference."]),
        S(6, [
            A('Given: x + y = 4 appears', T('Given: $x+y=4$', size=50)),
            A('5x + 5y − 3 = 5 · 4 − 3 = 17 appears', T('$5x+5y-3=5(x+y)-3=5\\cdot4-3=17$', size=46)),
            "They give you a block? Find it inside the question and put in its value.",
            "Don't hunt for x and y. You can't find them — and you don't need them."]),
        S(7, [
            A('Plug-in rules appear', T('Only for $=\\ ?$ · obey every condition', size=46)),
            "Stuck? Plug in numbers — but only in an expression, and only legal numbers.",
            A('Different letters appear', T('Different letters → different values: $2$, $3$, $5$', size=44)),
            "Zero and one are lazy numbers. They often make choices tie.",
            A('Eliminate three appears', T('Eliminate three · a tie? New numbers', size=46)),
            "You are knocking out three wrong choices. A tie? New numbers, only for the tied choices.",
            "Only numbers in the choices? Then one legal substitution is enough."]),
        S(8, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('Expression or equation? Can I cancel this?', size=42)),
            A('Check 2 appears', T('A sum on top or on the bottom?', size=42)),
            A('Check 3 appears', T('Is there a repeated bracket or a block I know?', size=42)),
            A('Check 4 appears', T('Did my numbers obey every condition?', size=42)),
            "And the traps: cancelling a denominator, splitting a sum on the bottom, and a lost minus before a bracket.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t05-summary', TOPIC, 'Summary: Expressions', sb, slides, ADV, after=last)


# ---------------------------------------------------------------------------------------------------------------
# 7. 2026-10-02: new numbers - the English course is not identical to the Hebrew one (same ideas, same methods)
# ---------------------------------------------------------------------------------------------------------------
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

    def video(qid, slides, intro=None):
        if qid in RECORDED: return
        vid = 'solve-' + qid
        for n, x in slides.items():
            title, script = x if isinstance(x, tuple) else (None, x)
            M.set_slide(vid, n, title=title, script=script)
        if intro: _sub(M, vid, 1, intro)
        q, v = M.q(qid), M.video(vid)
        v['title'] = ' %s ' % q['stem'].strip(); v['navLabel'] = q['navLabel']

    # ---------------- lesson "Working with Expressions" (Hebrew lesson examples -> new examples, same points)
    if 'q-135' not in RECORDED:
        L = 'expression-strategy'
        _sub(M, L, 2, [('Expression: something $=\\ ?$', 'Expression: one side, $\\ldots=\\ ?$'),
                       ('Equation: something $=$ something', 'Equation: two sides, $\\ldots=\\ldots$'),
                       ("'Expression: something = ?' appears", "'Expression: one side, … = ?' appears"),
                       ("'Equation: something = something' appears", "'Equation: two sides, … = …' appears")])
        _sub(M, L, 3, [('$\\frac{a}{b}+\\frac{b}{a}$', '$\\frac{x}{y}+\\frac{2y}{x}$'),
                       ('a/b + b/a appears', 'x/y + 2y/x appears'),
                       ("It's a times b.", "It's x times y."),
                       ('Write "= (a·a + b·b) / ab"', 'Write "= (x·x + 2y·y) / xy"'),
                       ('The first fraction needs times a, top and bottom. The second needs times b.',
                        'The first fraction needs times x, top and bottom. The second needs times y.'),
                       ('Write "= (a² + b²) / ab"', 'Write "= (x² + 2y²) / xy"'),
                       ('a squared plus b squared, over a b.', 'x squared plus two y squared, over x y.'),
                       ('Draw a big ✗ next to the ab', 'Draw a big ✗ next to the xy')])
        _sub(M, L, 5, [('$\\dfrac{12}{\\dfrac{1}{\\frac{1}{3}+\\frac{1}{6}}}$', '$\\dfrac{10}{\\dfrac{1}{\\frac{1}{2}+\\frac{1}{5}}}$'),
                       ('12 over 1 over (1/3 + 1/6)', '10 over 1 over (1/2 + 1/5)')])
        _sub(M, L, 6, [('Fifteen and negative fifteen.', 'Eight and negative eight.'),
                       ('a equals seven, b equals two.', 'a equals ten, b equals four.'),
                       ('Write "(7 − 2)/(2 − 7) = 5/−5 = −1"', 'Write "(10 − 4)/(4 − 10) = 6/−6 = −1"'),
                       ('Top: five. Bottom: negative five.', 'Top: six. Bottom: negative six.')])
        _sub(M, L, 7, [('$(a+b)(u-4)+(a+b)(u+4)$', '$(x+2)(y-5)+(x+2)(y+5)$'),
                       ('(a + b)(u − 4) + (a + b)(u + 4) appears', '(x + 2)(y − 5) + (x + 2)(y + 5) appears'),
                       ('Underline both (a + b) brackets', 'Underline both (x + 2) brackets'),
                       ('Look — a plus b appears in both parts.', 'Look — x plus two appears in both parts.'),
                       ('Write "= (a + b)[(u − 4) + (u + 4)]"', 'Write "= (x + 2)[(y − 5) + (y + 5)]"'),
                       ("What's left: u minus four, plus u plus four.", "What's left: y minus five, plus y plus five."),
                       ('Cross out the −4 and the +4', 'Cross out the −5 and the +5'),
                       ('Minus four and plus four cancel.', 'Minus five and plus five cancel.'),
                       ('Write "= (a + b)(2u)"', 'Write "= (x + 2)(2y)"'),
                       ("u plus u: two u. So it's a plus b, times two u.", "y plus y: two y. So it's x plus two, times two y.")])
        _sub(M, L, 8, [('1 · Only an expression ($=\\ ?$) — not an equation.', '1 · Only for $=\\ ?$ (one side) — never for an equation.'),
                       ('2 · Pick legal, easy values — obey every condition.', '2 · Choose simple values that keep every condition.'),
                       ("3 · Eliminate three choices — don't stop at the first match.", '3 · Knock out three wrong choices — one match is not enough.'),
                       ('4 · Two still match? Plug in different numbers.', '4 · Still a tie? New numbers, only for the tied choices.')])

    # ---------------- theory: guided questions 1-4
    # Q1 main fraction bar. Study guide 12 over 1 over (1/3 + 1/6) = 6; Hebrew video 4 over 1 over (1/2 + 1/4) = 3;
    # lesson example (recorded) 10 over 1 over (1/2 + 1/5) = 7; practice q-122 15 over 1 over (1/3 + 1/5) = 8
    S('q-135', stem=r'$\dfrac{6}{\dfrac{1}{\frac{1}{2}+\frac{1}{3}}}=\ ?$',
      choices=[r'$\frac{1}{5}$', r'$\frac{6}{5}$', r'$5$', r'$\frac{36}{5}$'], correct=3, expl=[
        r'Work from the inside out. Deepest layer: $\frac{1}{2}+\frac{1}{3}=\frac{3}{6}+\frac{2}{6}=\frac{5}{6}$.',
        r'Next layer: $1\div\frac{5}{6}=1\cdot\frac{6}{5}=\frac{6}{5}$.',
        r'Main bar: $6\div\frac{6}{5}=6\cdot\frac{5}{6}=5$. The answer is choice 3.',
        r'The traps: $\frac{6}{5}$ stops one layer too early, $\frac{36}{5}$ multiplies by $\frac{6}{5}$ instead of dividing, and $\frac{1}{5}$ turns the main bar upside down ($\frac{6}{5}\div6$).'])
    video('q-135', {2: [
        "Fraction on a fraction on a fraction. The main bar is the long one — six over everything else.",
        "So we need the bottom first. And inside the bottom — the deepest layer.",
        D('Next to the question write "1/2 + 1/3 = 3/6 + 2/6 = 5/6"'),
        "One half is three sixths. One third is two sixths. Together: five sixths.",
        D('Write "1 ÷ 5/6 = 1 · 6/5 = 6/5"'),
        "Next layer up: one divided by five sixths. Multiply by the reciprocal — six fifths.",
        D('Write "6 ÷ 6/5 = 6 · 5/6 = 5" and circle choice 3'),
        "And the main bar: six divided by six fifths. Six times five over six. The sixes cancel — five. Choice three.",
        "The traps: stop one floor early and you get six fifths. Multiply instead of divide and you get thirty-six fifths. Turn the main bar upside down and you get one fifth.",
        "Deepest level first, then climb out floor by floor. Never all the bars at once.",
        "A side tip about the exam: there are no visual traps in the choices. When an answer equals a choice NUMBER — say the answer is three — it sits in slot three."]})

    # Q2 opposite brackets. Study guide 7 − (p−q)/(q−p) = 8; Hebrew video 2 − (a−b)/(b−a) = 3
    S('q-136', stem=r'Given: $x\ne y$.' + '\n' + r'$10-\frac{y-x}{x-y}=\ ?$',
      choices=[r'$11$', r'$9$', r'$10$', r'$-11$'], correct=1, expl=[
        r'Since $x-y=-(y-x)$, the fraction $\frac{y-x}{x-y}$ equals $-1$.',
        r'Therefore the expression is $10-(-1)=10+1=11$. The answer is choice 1.',
        r'The trap is $9$ (choice 2): that is what you get if you treat the fraction as $+1$.'])
    video('q-136', {2: [
        "Look at the fraction: y minus x, over x minus y. Same letters, opposite order — the pattern the exam loves.",
        "Let's just pick two numbers and plug in: x equals six, y equals one.",
        D('Write "(1 − 6)/(6 − 1) = −5/5 = −1"'),
        "Negative five over five. The same number — one negative, one positive. Negative one.",
        D('Circle the fraction and write "= −1"'),
        "And that's the rule: swap the order of the two terms and it's ALWAYS negative one — whatever numbers you plug in. x isn't equal to y. Therefore we're safe from zero over zero.",
        D('Write "10 − (−1) = 10 + 1 = 11"'),
        "So ten minus negative one. Minus a negative — plus. Eleven.",
        D('Circle choice 1'),
        "Choice one.",
        "Watch the trap: nine is what you get if you treat that fraction as PLUS one."]})

    # Q3 repeated bracket. Study guide (c+d)(t−3) + (c+d)(t+3); Hebrew video (a+b)(x−1) + (a+b)(x+1)
    S('q-137', stem=r'$(m+2n)(k-6)+(m+2n)(k+6)=\ ?$',
      choices=[r'$0$', r'$2k(m+2n)$', r'$m+2n+k$', r'$2(m+2n+k)$'], correct=2, expl=[
        r'Take out the common bracket: $(m+2n)(k-6)+(m+2n)(k+6)=(m+2n)[(k-6)+(k+6)]$.',
        r'Inside: $-6$ and $+6$ cancel, therefore $(k-6)+(k+6)=2k$.',
        r'The expression equals $(m+2n)\cdot2k=2k(m+2n)$. The answer is choice 2.',
        r'Check with $m=n=k=1$: $3\cdot(-5)+3\cdot7=6$. The choices give $0$, $6$, $4$ and $8$ — only choice 2.'])
    video('q-137', {2: [
        "m plus two n appears in both parts. That's our common factor.",
        D('Underline both (m + 2n) brackets'),
        D('Write "= (m + 2n)[(k − 6) + (k + 6)]"'),
        "Take it out front. Inside: k minus six, plus k plus six.",
        D('Cross out the −6 and the +6'),
        "Minus six and plus six cancel.",
        D('Write "= (m + 2n)(2k) = 2k(m + 2n)"'),
        "k plus k: two k. Two k, times m plus two n.",
        D('Circle choice 2'),
        "Choice two."],
        3: [
        "Letters scary? In an expression you can plug in numbers.",
        "Why ones? You could use two, five, seven — or eleven, twenty, sixty-four. Nothing says the letters must be different. So pick the easiest: all ones.",
        D('Write "m = n = k = 1"'),
        D('Write "3 · (−5) + 3 · 7 = −15 + 21 = 6"'),
        "m plus two n is three. One minus six is negative five. Three times negative five, plus three times seven. Six.",
        D('Next to choice 1 write "0" and cross it out'),
        "Choice one: zero. Out.",
        D('Next to choice 2 write "2 · 1 · 3 = 6"'),
        "Choice two: two times one times three — six. A match! But here's the catch: DON'T circle it yet.",
        "When you plug in, you're not hunting for the right answer. You're knocking out wrong ones.",
        D('Next to choices 3 and 4 write "4" and "8", and cross them out'),
        "Choice three: four. Choice four: eight. Both out.",
        D('Circle choice 2'),
        "Three knocked out — NOW choice two."]},
        intro=[('Four letters, two brackets — and it all collapses.', 'Three letters, two brackets — and it all collapses.')])

    # Q4 two blocks. Study guide (a+b+c+d)² − (a+b−c−d)²; Hebrew video (x+y+z+w)² − (x+y−z−w)²
    S('q-138', stem=r'$(p+q+r+s)^2-(p-q+r-s)^2=\ ?$',
      choices=[r'$4(p+r)(q+s)$', r'$p^2+r^2$', r'$2(pr-qs)$', r'$q^2+s^2$'], correct=1, expl=[
        r'Regroup into two blocks: $A=p+r$ and $B=q+s$. Then $p+q+r+s=A+B$ and $p-q+r-s=A-B$.',
        r'$(A+B)^2-(A-B)^2=(A^2+2AB+B^2)-(A^2-2AB+B^2)=4AB$.',
        r'Put the blocks back: $4(p+r)(q+s)$. The answer is choice 1.',
        r'Check with $p=q=r=s=1$: $4^2-0^2=16$, and choice 1 gives $4\cdot2\cdot2=16$; the other choices give $2$, $0$ and $2$.'])
    video('q-138', {2: [
        "Strong algebra students might expand this. It takes a minute or more.",
        "For the rest of us: it's an expression. Plug in numbers.",
        "Nothing says the letters must be different — so make them all one.",
        D('Write "p = q = r = s = 1"'),
        D('Write "4² − 0² = 16 − 0 = 16"'),
        "One plus one plus one plus one: four. Squared — sixteen. One minus one plus one minus one: zero. Sixteen minus zero — sixteen.",
        D('Next to choice 1 write "4 · 2 · 2 = 16"'),
        "Choice one: four times two times two — sixteen. A match! But DON'T circle it yet.",
        D('Next to choices 2, 3 and 4 write "2", "0" and "2", and cross them out'),
        "Choice two: one plus one — two. Choice three: zero. Choice four: two. All out.",
        D('Circle choice 1'),
        "NOW we've eliminated three. Choice one.",
        "And if two choices had both given sixteen? Change one number — make s two — and test only those two."],
        3: [
        "Want proof it wasn't luck? Same question, different simple numbers: three, zero, one, two.",
        D('Write "p = 3, q = 0, r = 1, s = 2"'),
        D('Write "6² − 2² = 36 − 4 = 32"'),
        "Three plus zero plus one plus two: six. Squared — thirty-six. Three minus zero plus one minus two: two. Squared — four. Thirty-two.",
        D('Next to the choices write their values: 32, 10, 6, 4'),
        "Choice one: four times four times two — thirty-two. Choice two: nine plus one — ten. Choice three: two times three minus zero — six. Choice four: zero plus four — four.",
        D('Circle choice 1'),
        "Choice one again. Any legal numbers — same winner.",
        "So when may you plug in? Only in an EXPRESSION — something equals a question mark. Two sides? Not allowed.",
        "Eliminate three — never grab the first match. A tie? New numbers.",
        "It's a safety net. What you can solve with algebra, solve with algebra."],
        4: [
        "For the algebra fans: it's really just two blocks — once you regroup.",
        D('Write "A = p + r, B = q + s"'),
        "Gather p and r: call them A. Gather q and s: call them B.",
        "The first bracket is A plus B. The second: p plus r, minus q, minus s — that's A minus B.",
        D('Write "(A + B)² − (A − B)² = 4AB"'),
        "Then it's A plus B squared, minus A minus B squared. That always collapses to four A B.",
        D('Write "= 4(p + r)(q + s)" and circle choice 1'),
        "Swap the blocks back: four, times p plus r, times q plus s. Choice one.",
        "Know the algebra? Great. Don't? Plugging in got you there just as surely."]},
        intro=[('This one actually appeared on an exam — and it scares everyone.', 'A real exam favorite — and it scares everyone.')])

    # ---------------- advanced: guided questions 5-12
    # Q5 four ways. Study guide (18² − 18) − (17² + 17); Hebrew video (15² − 15) − (14² + 14)
    S('q-125', stem=r'$\left(13^2-13\right)-\left(12^2+12\right)=\ ?$',
      choices=[r'$12$', r'$1$', r'$0$', r'$13$'], correct=3, expl=[
        r'Take out a common factor in each bracket: $13^2-13=13(13-1)=13\cdot12$ and $12^2+12=12(12+1)=12\cdot13$.',
        r'The two brackets are the same number, therefore their difference is $0$. The answer is choice 3.',
        r'Direct calculation gives the same: $(169-13)-(144+12)=156-156=0$.'])
    video('q-125', {2: [
        "Method one: simply calculate. The numbers aren't big.",
        "And squares like these you should know by heart.",
        D('Under the first bracket write "169 − 13 = 156"'),
        "Thirteen squared: one hundred sixty-nine. Minus thirteen: one hundred fifty-six.",
        D('Under the second bracket write "144 + 12 = 156"'),
        "Twelve squared: one hundred forty-four. Plus twelve: also one hundred fifty-six.",
        D('Write "156 − 156 = 0" and circle choice 3'),
        "One fifty-six minus one fifty-six: zero. Choice three."],
        3: [
        "But even the calculation can be shortened — with psychometric thinking: the units digit.",
        D('Above 13² write "…9"; above 12² write "…4"'),
        "Thirteen squared ends in nine — three times three is nine. Twelve squared ends in four — two times two.",
        D('Under the first bracket write "…9 − …3 → ends in 6"'),
        "Ends in nine, minus thirteen: it ends in six.",
        D('Under the second bracket write "…4 + …2 → ends in 6"'),
        "Ends in four, plus twelve: also ends in six.",
        "Six minus six — the answer ends in zero.",
        D('Circle choice 3'),
        "Only one choice ends in zero. Choice three.",
        "This works because all four choices end in different digits. If they didn't, we'd need another method."],
        4: [
        "Method three: pull out a common factor. Yes — you can do that with plain numbers too.",
        D('Write "13² − 13 = 13(13 − 1) = 13 · 12"'),
        "Thirteen squared minus thirteen: take out thirteen. Thirteen times twelve.",
        D('Write "12² + 12 = 12(12 + 1) = 12 · 13"'),
        "Twelve squared plus twelve: take out twelve. Twelve times thirteen.",
        D('Write "13 · 12 − 12 · 13 = 0"'),
        "Same product both times — order doesn't matter in multiplication. So: zero.",
        D('Circle choice 3'),
        "Choice three."],
        5: ('Method 4 · Count the copies', [
        "And the fastest way — no pen needed.",
        "Thirteen squared is thirteen thirteens. Take one thirteen away: twelve thirteens.",
        "Twelve squared is twelve twelves. Add one twelve: thirteen twelves.",
        "Twelve thirteens minus thirteen twelves — exactly the same thing.",
        D('Write "= 0" and circle choice 3'),
        "Zero. Pick whichever route you like on the exam — they're all correct."])})

    # Q6 minus after a bracket. Study guide {[(p−q)−r]−s+q}; Hebrew video {[(a−b)−c]−d+b}
    S('q-126', stem=r'$\left\{\left[\left(w-x\right)+y\right]-z+x\right\}=\ ?$',
      choices=[r'$w-y+z$', r'$w+y-z$', r'$w+y+z$', r'$w-2x+y-z$'], correct=2, expl=[
        r'No minus sign stands right in front of a bracket, therefore the brackets can be dropped without changing any sign: $w-x+y-z+x$.',
        r'$-x$ and $+x$ cancel, leaving $w+y-z$. The answer is choice 2.',
        r'Check with $w=20$, $x=3$, $y=4$, $z=5$: $\{[(20-3)+4]-5+3\}=19$, and choice 2 gives $20+4-5=19$ (the others give $21$, $29$ and $13$).'])
    video('q-126', {2: [
        "The whole question is about one thing: when does a minus sign affect a bracket?",
        "Not sure? Always test with numbers.",
        D('Write "(12 − 2) − 3 = 10 − 3 = 7" and next to it "12 − 2 − 3 = 7"'),
        "Twelve minus two, in brackets, minus three: ten minus three, seven. Without the brackets: also seven.",
        "So a minus AFTER a bracket doesn't touch it. Only a minus right in FRONT of a bracket flips the signs inside.",
        "Look: every minus here is inside a bracket or after one. Nothing sits in front of a bracket.",
        D('Cross out every bracket'),
        "So we can simply drop all the brackets.",
        D('Write "= w − x + y − z + x"'),
        "w minus x, plus y, minus z, plus x.",
        D('Cross out −x and +x'),
        "Minus x and plus x cancel out.",
        D('Write "= w + y − z" and circle choice 2'),
        "w plus y minus z. Choice two."],
        3: [
        "Not sure about the signs? Plug in numbers. But choose smartly.",
        "We usually plug in ones — but not here. With all ones, choices one and two both give one. A tie — one substitution can't decide.",
        "So: w is a round, bigger number — twenty — so we stay with positive numbers. And x, y and z are different small numbers: three, four, five.",
        D('Write "w = 20, x = 3, y = 4, z = 5"'),
        D('Next to the choices write their values: 21, 19, 29, 13'),
        "The choices give twenty-one, nineteen, twenty-nine and thirteen. All different — one substitution is enough.",
        D('Work the question from the inside out: 20 − 3 = 17, 17 + 4 = 21, 21 − 5 = 16, 16 + 3 = 19'),
        "Innermost bracket first: twenty minus three, seventeen. Plus four, twenty-one. Minus five, sixteen. Plus three — nineteen.",
        D('Circle choice 2'),
        "Nineteen. Choice two.",
        "Which route? Here the direct method is much shorter. Plugging in always works for expressions with letters — it's your default backup when you're stuck."]})

    # Q7 open the choices. Study guide x² + 11x + 24; Hebrew video x² + 9x + 18
    S('q-127', stem=r'Which of the following expressions is necessarily equal to $x^2+15x+36$?',
      choices=[r'$(x+18)(x+2)$', r'$(x+36)(x+1)$', r'$(x+12)(x+3)$', r'$(x+8)(x+4.5)$'], correct=3, expl=[
        r'Every choice has the form $(x+p)(x+q)=x^2+(p+q)x+pq$. In every choice $pq=36$, therefore the middle term decides: we need $p+q=15$.',
        r'The sums are $20$, $37$, $15$ and $12.5$. Only $12+3=15$. Therefore $x^2+15x+36=(x+12)(x+3)$. The answer is choice 3.',
        r'Check with $x=1$: $1+15+36=52$, and choice 3 gives $13\cdot4=52$ (the others give $57$, $74$ and $9\cdot5.5=49.5$ — not a whole number, so choice 4 is out without calculating).'])
    video('q-127', {2: [
        "Sum and product would work. But look — the choices help us too. Open them up.",
        D('Next to choice 1 write "x² + 2x + 18x + 36 = x² + 20x + 36"'),
        "Choice one: x times x, x squared. x times two, two x. Eighteen times x, eighteen x. Eighteen times two, thirty-six.",
        "x squared plus twenty x plus thirty-six. The x squared matches, the thirty-six matches — but twenty x doesn't.",
        D('Cross out choice 1'),
        "Now notice: every choice starts with x times x — x squared.",
        D('Next to each choice, multiply the two numbers: 36, 36, 36, 36'),
        "And the numbers multiply to thirty-six every single time.",
        "So the only thing that decides it is the middle term: we need fifteen x.",
        D('Next to each choice write the sum of the two numbers: 20, 37, 15, 12.5'),
        "Eighteen plus two: twenty x. Thirty-six plus one: thirty-seven x. Twelve plus three: fifteen x. Eight plus four and a half: twelve and a half x.",
        D('Circle choice 3'),
        "Fifteen x — choice three."],
        3: [
        "Plug-in version. x equals one.",
        D('Next to the choices write: 19·3 = 57, 37·2 = 74, 13·4 = 52, 9·5.5 → not whole'),
        "The choices give fifty-seven, seventy-four, fifty-two — and choice four: nine times five and a half.",
        "Don't calculate that one. Just notice: it's not a whole number. If the expression also comes out not whole, that's our answer. If not — it's out, and we saved the calculation.",
        "So: all four are different. One plug-in is enough.",
        D('In the question write "1 + 15 + 36 = 52"'),
        "The expression: one plus fifteen plus thirty-six — fifty-two.",
        D('Circle choice 3'),
        "Fifty-two. Choice three. Here, plugging in is actually the faster route."]})

    # Q8 identical and opposite numbers. Study guide |x|/x + 5; Hebrew video 3 + |x|/x
    S('q-128', stem=r'If ___ then the value of the expression $\frac{x}{|x|}+8$ equals ___.',
      choices=[r'$x>0$ ; $7$', r'$x<0$ ; $9$', r'$x<0$ ; $7$', r'$x>0$ ; $10$'], correct=3, expl=[
        r'If $x<0$, then $|x|=-x$, therefore $\frac{x}{|x|}=\frac{x}{-x}=-1$ and the expression equals $-1+8=7$. This is choice 3.',
        r'If $x>0$, then $\frac{x}{|x|}=1$ and the expression equals $1+8=9$. No choice with $x>0$ says $9$, therefore choices 1 and 4 are out. Choice 2 pairs $9$ with $x<0$ — out.',
        r'Check with $x=-2$: $\frac{-2}{|-2|}+8=-1+8=7$ ✓.'])
    video('q-128', {2: [
        "A number divided by itself is one. A number divided by its opposite is minus one.",
        "x over the absolute value of x. If x is positive — say four — the absolute value doesn't change it: four over four, one.",
        D('Write "x > 0: x/|x| = 1 → 1 + 8 = 9"'),
        "One. Plus eight — nine.",
        "Now look at the choices that say x is positive: choice one says seven, choice four says ten.",
        D('Cross out choices 1 and 4'),
        "Neither says nine. Both out.",
        "If x is negative — say negative two — the top stays negative two, and the bottom becomes positive two. Opposite numbers.",
        D('Write "x < 0: x/|x| = −1 → −1 + 8 = 7"'),
        "Minus one. Plus eight — seven.",
        D('Cross out choice 2 and circle choice 3'),
        "Choice two says nine — out. Choice three says seven with a negative x. That's it.",
        "Remember this pattern. It also shows up as x minus y over y minus x — opposite numbers again."]})

    # Q9 two claims. Study guide / Hebrew video: (A+B)/A = 1 + B/A (true), A/(A+B) = 1 + A/B (false).
    # New story: Tom and Dana; a difference instead of a sum, the false claim first, the key moves to choice 2.
    S('q-129', stem='Tom and Dana each make a claim:\n'
                    r'$\begin{array}{ll} \text{Tom:} & \dfrac{B}{A-B}=\dfrac{B}{A}-1 \\[8pt] \text{Dana:} & \dfrac{A-B}{B}=\dfrac{A}{B}-1 \end{array}$'
                    '\nEach claim is about all the values of $A$ and $B$ for which both sides are defined.\nWhich of the following is true?',
      choices=['Only Tom is right', 'Only Dana is right', 'Both Tom and Dana are wrong', 'Both Tom and Dana are right'], correct=2, expl=[
        r'Dana: a difference on top may be split: $\frac{A-B}{B}=\frac{A}{B}-\frac{B}{B}=\frac{A}{B}-1$. This is true for every $B\ne0$.',
        r'Tom: test $A=3$, $B=1$. Left side: $\frac{1}{3-1}=\frac{1}{2}$. Right side: $\frac{1}{3}-1=-\frac{2}{3}$. Not equal, therefore Tom\'s claim is false.',
        'Only Dana is right. The answer is choice 2.'])
    video('q-129', {2: [
        "Tom says: B over A minus B equals B over A, minus one.",
        "Can we just split that bottom? Let's not guess. Work backwards from the side we know how to handle.",
        D('Under Tom\'s claim write "B/A − 1 = B/A − A/A = (B − A)/A"'),
        "B over A minus one: a fraction minus a whole. Write one as A over A — same denominator — subtract the tops. B minus A, over A.",
        "His left side is B over A minus B. They look different — but different-looking expressions can still be equal. So test numbers.",
        D('Write "A = 3, B = 1: 1/2 vs −2/3 ✗"'),
        "A is three, B is one. Left: one over two — one half. Right: one third minus one — negative two thirds. Not equal. Tom is wrong.",
        D('Cross out choices 1 and 4'),
        "So \"only Tom\" and \"both right\" are out.",
        "Dana says: A minus B, over B, equals A over B, minus one.",
        D('Under Dana\'s claim write "A/B − 1 = A/B − B/B = (A − B)/B ✓"'),
        "Same move: one is B over B. Subtract the tops: A minus B, over B. Exactly her left side. Dana is right.",
        D('Circle choice 2'),
        "Only Dana is right — choice two."],
        3: [
        "Could we shorten that? Yes — split the fraction.",
        "Remember the rule: a sum or a difference on the BOTTOM can't be split. On TOP it can — each term gets its own copy of the bottom.",
        D('Under Dana\'s claim write "(A − B)/B = A/B − B/B = A/B − 1"'),
        "A over B, minus B over B. B over B is one. Done — Dana is right.",
        "Tom's fraction has the difference on the BOTTOM. Splitting it is exactly the classic trap — and the numbers in Method 1 showed he's wrong.",
        A('(180 − α)/2 = 90 − α/2 appears', T(r'$\frac{180-\alpha}{2}=90-\frac{\alpha}{2}$', size=46, x=410, y=420)),
        "You already know this from geometry: one-eighty minus alpha, over two, is ninety minus alpha over two. A difference on top — split it.",
        D('Circle choice 2'),
        "Split only the top, and the question becomes simple. Only Dana — choice two."],
        4: [
        "Plug-in version. A is three, B is one.",
        D('Write "A = 3, B = 1"'),
        D('Under Tom\'s claim write "1/2 vs 1/3 − 1 = −2/3 ✗"'),
        "Tom: one over two is one half. One third minus one is negative two thirds. Not equal.",
        D('Under Dana\'s claim write "2/1 = 2 and 3 − 1 = 2 ✓"'),
        "Dana: two over one is two. Three minus one is two. Equal.",
        D('Circle choice 2'),
        "One counterexample is enough to prove a claim wrong. Tom fails, Dana holds — only Dana is right. Choice two."]})

    # Q10 opposite brackets on top. Study guide [(p−q) − (q−p)]/(p−q); Hebrew video [(x−y) − (y−x)]/(x−y)
    S('q-130', stem=r'Given: $m\ne n$.' + '\n' + r'$\frac{3(m-n)-(n-m)}{m-n}=\ ?$',
      choices=[r'$2$', r'$4m$', r'$4$', r'$4n$'], correct=3, expl=[
        r'The minus stands in front of the second bracket only: $3(m-n)-(n-m)=3m-3n-n+m=4m-4n=4(m-n)$.',
        r'Divide by $m-n$ (not zero, because $m\ne n$): $\frac{4(m-n)}{m-n}=4$. The answer is choice 3.',
        r'The trap is $2$ (choice 1): that is what you get if you read $n-m$ as $m-n$ (then $3-1=2$), or if you forget the 3.'])
    video('q-130', {2: [
        "The minus sits in front of the second bracket only. So only the second bracket flips.",
        D('On top write "3m − 3n − n + m"'),
        "First open the three: three m minus three n. Then minus n, plus m.",
        D('Write "= 4m − 4n = 4(m − n)"'),
        "Four m minus four n. Take out the common factor: four, times m minus n.",
        D('Cancel (m − n) on top and bottom; write "= 4"'),
        "m minus n on top and on the bottom — cancel. Four.",
        D('Circle choice 3'),
        "Choice three."],
        3: [
        "Here's a sharper route. Split the top over the bottom.",
        D('Write "3(m − n)/(m − n) − (n − m)/(m − n)"'),
        "The first part: three times m minus n, over m minus n. Three.",
        "The second part: n minus m over m minus n — the same numbers, reversed. Swap the order and you always get opposites: seven minus four is three, four minus seven is minus three. Minus one.",
        D('Write "= 3 − (−1) = 4" and circle choice 3'),
        "Three minus minus one: four. Choice three.",
        "Read n minus m as if it were m minus n, and you get three minus one — two. Choice one is that trap."],
        4: [
        "A third route. The two brackets look alike — just in reverse order.",
        D('Under (n − m) write "= −(m − n)"'),
        "Take a minus out of the second one: n minus m is minus, m minus n. Open it and check — same thing.",
        D('On top write "3(m − n) + (m − n) = 4(m − n)"'),
        "Minus a minus: plus. So it's three of m minus n, plus one more. Like three basketballs and one more basketball — four of them.",
        D('Cancel (m − n); write "= 4" and circle choice 3'),
        "Four, times m minus n, over m minus n. Cancel. Four — choice three.",
        "Route one is the standard. Routes two and three are the sharper ones."],
        5: [
        "Plug in. But careful: m equals one would make four m equal four, the same as choice three.",
        "So pick m bigger than n, and not one: m is five, n is three.",
        D('Next to the choices write: 2, 20, 4, 12'),
        "Choices: two, twenty, four, twelve. All different.",
        D('In the question write "(3 · 2 − (−2))/2 = 8/2 = 4"'),
        "Five minus three is two. Three times two: six. Three minus five is minus two. Six minus minus two — eight. Over two: four.",
        D('Circle choice 3'),
        "Choice three."]})

    # Q11 factor or combine. Study guide 1 + (4b² + 4ab)/(a² − b²); Hebrew video 1 + (2y² + 2xy)/(x² − y²)
    S('q-133', stem=r'Given: $a\ne\pm b$.' + '\n' + r'$1+\frac{6b^2+6ab}{a^2-b^2}=\ ?$',
      choices=[r'$\frac{a+b}{a-b}$', r'$\frac{a-5b}{a+b}$', r'$\frac{a+5b}{a-b}$', r'$\frac{a+5b}{a+b}$'], correct=3, expl=[
        r'Factor the fraction. Top: $6b^2+6ab=6b(b+a)$. Bottom: $a^2-b^2=(a-b)(a+b)$.',
        r'Cancel $a+b$ (not zero, because $a\ne-b$): the fraction equals $\frac{6b}{a-b}$.',
        r'Then $1+\frac{6b}{a-b}=\frac{a-b}{a-b}+\frac{6b}{a-b}=\frac{a+5b}{a-b}$. The answer is choice 3.',
        r'Check with $a=2$, $b=1$: $1+\frac{6+12}{3}=7$, and choice 3 gives $\frac{7}{1}=7$ (the others give $3$, $-1$ and $\frac{7}{3}$).'])
    video('q-133', {2: [
        "Simplify the fraction first.",
        D('Under the top write "6b(b + a)"'),
        "The top: six b squared plus six ab. Take out six b: six b, times b plus a.",
        D('Under the bottom write "(a − b)(a + b)"'),
        "The bottom: a squared minus b squared — difference of squares. a minus b, times a plus b.",
        D('Cancel (a + b); write "= 1 + 6b/(a − b)"'),
        "Cancel a plus b. One plus six b over a minus b.",
        D('Write "= (a − b + 6b)/(a − b) = (a + 5b)/(a − b)"'),
        "Write one as a minus b over a minus b, and add the tops. a plus five b, over a minus b.",
        D('Circle choice 3'),
        "Choice three."],
        3: [
        "Another route: add the one BEFORE simplifying.",
        D('Write "(a² − b² + 6b² + 6ab)/(a² − b²)"'),
        "Write one with the same bottom and add the tops.",
        D('Write "= (a² + 6ab + 5b²)/((a − b)(a + b))"'),
        "Minus b squared plus six b squared is five b squared.",
        D('Write "= (a + b)(a + 5b)/((a − b)(a + b)) = (a + 5b)/(a − b)"'),
        "The top factors to a plus b, times a plus five b. Cancel a plus b. Same answer — choice three."],
        4: [
        "Now the route I recommend for most students: plug in.",
        "a can't equal b or minus b. So: a is two, b is one.",
        D('Next to the choices write: 3, −1, 7, 7/3'),
        "The choices give three, minus one, seven and seven thirds. All different.",
        D('In the question write "1 + (6 + 12)/3 = 1 + 6 = 7"'),
        "Six b squared is six. Six ab is twelve. Eighteen over three is six. One plus six — seven.",
        D('Circle choice 3'),
        "Seven. Choice three."]})

    # Q12 estimate. Study guide 32,004 ÷ 63 = 508; Hebrew video 42,944 ÷ 61 = 704 (units digit eliminates two choices)
    S('q-134', stem=r'$\frac{33{,}046}{41}=\ ?$',
      choices=[r'$406$', r'$508$', r'$602$', r'$806$'], correct=4, expl=[
        r'Estimate with friendly numbers: $\frac{33{,}046}{41}\approx\frac{32{,}000}{40}=800$. Only $806$ is close.',
        r'Units digit: $41$ ends in 1, so $41\cdot508$ ends in 8 and $41\cdot602$ ends in 2 — but the top ends in 6. And $41\cdot406$ is only about $16{,}000$.',
        r'Check: $41\cdot806=41\cdot800+41\cdot6=32{,}800+246=33{,}046$ ✓. The answer is choice 4.'])
    video('q-134', {2: [
        "No calculator — so how are we meant to do this? Long division works, but it's slow.",
        "What they're really testing: are you rigid? Like a job interview asking how many gas stations there are in the country. Nobody expects exact — they expect an estimate.",
        "And look: the choices are far apart.",
        D('Write "≈ 32,000 ÷ 40 = 800"'),
        "Round to friendly numbers. Thirty-two divides by four — eight. So thirty-two thousand over forty is eight hundred.",
        "The real top is a bit bigger, and the real bottom is a bit bigger too. The answer sits around eight hundred.",
        D('Cross out choices 1, 2 and 3; circle choice 4'),
        "Four hundred six, five hundred eight, six hundred two — too far. Eight hundred six. Choice four."],
        3: [
        "Another way: start from the choices and multiply back.",
        D('Next to choice 1 write "40 · 400 = 16,000"'),
        "Forty times four hundred: sixteen thousand. Nowhere near thirty-three thousand. Out.",
        D('Next to choices 2 and 3 write "8 · 1 = 8 ✗" and "2 · 1 = 2 ✗"'),
        "Now the units digit. Forty-one ends in one. So five hundred eight times forty-one ends in eight, and six hundred two times forty-one ends in two. But the top ends in six. Both out.",
        D('Write "41 · 806 = 32,800 + 246 = 33,046 ✓" and circle choice 4'),
        "Only choice four is left. Check: forty-one times eight hundred six is thirty-three thousand forty-six. Choice four."]})

    # ---------------- self-practice from the Hebrew study guide (+ two letter-only copies of Hebrew video questions)
    S('q-122', stem=r'$\frac{15}{\frac{1}{\frac{1}{3}+\frac{1}{5}}}=\ ?$',
      choices=[r'$\frac{8}{15}$', r'$\frac{15}{8}$', r'$8$', r'$\frac{225}{8}$'], correct=3, expl=[
        r'Inside out: $\frac{1}{3}+\frac{1}{5}=\frac{5}{15}+\frac{3}{15}=\frac{8}{15}$.',
        r'Next layer: $1\div\frac{8}{15}=\frac{15}{8}$.',
        r'Main bar: $15\div\frac{15}{8}=15\cdot\frac{8}{15}=8$. The answer is choice 3.'])
    S('q-123', stem=r'Given: $c\ne d$.' + '\n' + r'$\frac{d-c}{c-d}-4=\ ?$',
      choices=[r'$-3$', r'$-5$', r'$5$', r'$-4$'], correct=2, expl=[
        r'$c-d=-(d-c)$, therefore $\frac{d-c}{c-d}=-1$ for every $c\ne d$.',
        r'The expression is $-1-4=-5$. The answer is choice 2.',
        r'The trap is $-3$ (choice 1): that is what you get if you treat the fraction as $+1$.'])
    S('q-124', stem=r'$(3a+b)(z+7)+(3a+b)(z-7)=\ ?$',
      choices=[r'$0$', r'$2(3a+b+z)$', r'$2z(3a+b)$', r'$3a+b+z$'], correct=3, expl=[
        r'Take out the common bracket: $(3a+b)[(z+7)+(z-7)]$. Inside, $+7$ and $-7$ cancel: $2z$.',
        r'The expression is $(3a+b)\cdot2z=2z(3a+b)$. The answer is choice 3.',
        r'Check with $a=b=z=1$: $4\cdot8+4\cdot(-6)=8$. The choices give $0$, $10$, $8$ and $5$.'])
    # letters-only copy of the Hebrew video question [(x−y) − (y−x)]/(x−y): new coefficient, reversed bottom
    S('q-expression-extra-08', stem=r'Given: $x\ne y$.' + '\n' + r'$\frac{(x-y)-2(y-x)}{y-x}=\ ?$',
      choices=[r'$-3$', r'$-1$', r'$1$', r'$3$'], correct=1, expl=[
        r'Open the brackets on top: $(x-y)-2(y-x)=x-y-2y+2x=3x-3y=3(x-y)$.',
        r'The bottom is $y-x=-(x-y)$. Therefore $\frac{3(x-y)}{-(x-y)}=-3$. The answer is choice 1.',
        r'Or split: $\frac{x-y}{y-x}-\frac{2(y-x)}{y-x}=-1-2=-3$.'])
    # letters-only copy of the Hebrew video question 1 + (2y² + 2xy)/(x² − y²): now a minus
    S('q-expression-extra-11', stem=r'Given: $a\ne\pm b$.' + '\n' + r'$1-\frac{2b^2+2ab}{a^2-b^2}=\ ?$',
      choices=[r'$\frac{a-3b}{a-b}$', r'$\frac{a+3b}{a-b}$', r'$\frac{a-b}{a+b}$', r'$1$'], correct=1, expl=[
        r'Top: $2b^2+2ab=2b(b+a)$. Bottom: $a^2-b^2=(a-b)(a+b)$. Cancel $a+b$: the fraction is $\frac{2b}{a-b}$.',
        r'Then $1-\frac{2b}{a-b}=\frac{a-b-2b}{a-b}=\frac{a-3b}{a-b}$. The answer is choice 1.',
        r'Check with $a=2$, $b=1$: $1-\frac{2+4}{3}=-1$, and choice 1 gives $\frac{-1}{1}=-1$ (the others give $5$, $\frac{1}{3}$ and $1$).'])


# ---------------------------------------------------------------------------------------------------------------
# 2026-10-02 order changes (less like a copy of the Hebrew course; only where nothing is lost)
# Spoken "Question N" lines use the numbers from before renumbering; renumber_guided maps them to the new order.
# ---------------------------------------------------------------------------------------------------------------
def _script(b):
    """beat -> script list (same items, lines and appear order)."""
    out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _swap_slides(M, vid, a, b_):
    """Swap two neighbouring concept slides (a < b_) and their sidebar labels; fix the 'active' indexes."""
    v = M.video(vid); sb = v['hybrid']['sidebar']
    x, y = v['beats'][a - 1], v['beats'][b_ - 1]
    ia, ib = x['active'], y['active']
    sb[ia], sb[ib] = sb[ib], sb[ia]
    x['active'], y['active'] = ib, ia
    M.move_slide(vid, b_, a)
    M.set_sidebar(vid, sb)


def _choices(M, qid, order, expl_pairs):
    """New choice order (old 1-based positions). expl_pairs: exact substring replacements in the written solution."""
    q = M.q(qid); old = list(q['choicesRich']); key = q['correct'][0] + 1
    ex = list(q['explanation'])
    for o, n in expl_pairs:
        assert sum(o in e for e in ex) == 1, (qid, o)
        ex = [e.replace(o, n) for e in ex]
    q = M.set_q(qid, choices=[old[k - 1] for k in order], correct=order.index(key) + 1, expl=ex)
    for v in M.D['videos'].values():
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                    it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])


def order_changes(M):
    L, SUM, TH = 'expression-strategy', 'r26-t05-summary', 'expression-theory'
    # (1) Theory: opposite brackets (one step) before the layered fraction (three steps) - lesson, guided questions
    #     and summary in the same new order.
    assert M.slide(L, 5)['title'] == 'The main fraction bar' and M.slide(L, 6)['title'] == 'Opposite brackets'
    _replace(M, L, 5, 'This exact one is Question 1 — so try it yourself first.',
             "You'll meet this exact one in the guided questions — so try it yourself first.")
    _swap_slides(M, L, 5, 6)
    rc = _script(M.slide(L, 11))
    i = next(k for k, x in enumerate(rc) if not isinstance(x, str) and x[0] == 'A' and 'Main bar first' in x[1])
    assert 'b − a' in rc[i + 1][1]
    rc[i], rc[i + 1] = rc[i + 1], rc[i]
    M.set_slide(L, 11, script=rc)
    assert M.slide(SUM, 4)['title'] == 'The main fraction bar' and M.slide(SUM, 5)['title'] == 'Opposite brackets'
    _swap_slides(M, SUM, 4, 5)
    M.move('q-136', TH, before='q-135'); M.move('solve-q-136', TH, after='q-136')
    _replace(M, 'solve-q-136', 1, 'Question two.', 'First guided question.')
    _replace(M, 'solve-q-135', 1, 'First guided question.', 'Question one.')

    # (2) Advanced expressions: easy -> hard by the teacher's own levels (easy+, medium, medium+, hard).
    #     13^2-13 ... (easy+), 33,046/41 (easy+, uses the units digit right after it is taught), x^2+15x+36 (easy+),
    #     x/|x| (easy+), 3(m-n)-(n-m) (medium), nested brackets (medium+), Tom and Dana (medium+), 1+(6b^2+6ab)/(a^2-b^2) (hard).
    M.move('q-134', ADV, after='solve-q-125'); M.move('solve-q-134', ADV, after='q-134')
    M.move('q-130', ADV, after='solve-q-128'); M.move('solve-q-130', ADV, after='q-130')
    M.move('q-126', ADV, after='solve-q-130'); M.move('solve-q-126', ADV, after='q-126')
    _replace(M, 'solve-q-134', 1, 'Last question.', 'Question fourteen.')
    _replace(M, 'solve-q-134', 1, "No calculator, a big division — and they're testing whether you'll get stuck calculating.",
             "Plain numbers again. No calculator, a big division — and they're testing whether you'll get stuck calculating.")
    # the "given a block" pointer goes to the tools that now follow the last advanced question (old number 13)
    _replace(M, L, 7, "And if a question GIVES you the value of a block — say, a plus b equals five — put the number in its place. You'll practise that after Question 14.",
             "And if a question GIVES you the value of a block — say, a plus b equals five — put the number in its place. You'll practise that after Question 13.")

    # (3) Answer positions that were still the same as in the Hebrew course
    # q-126: key 2 -> 1 (w+y-z, w-y+z, w+y+z, w-2x+y-z). With all ones choices 1 and 2 still tie.
    _choices(M, 'q-126', [2, 1, 3, 4], [('The answer is choice 2.', 'The answer is choice 1.'),
                                         ('and choice 2 gives $20+4-5=19$', 'and choice 1 gives $20+4-5=19$')])
    _replace(M, 'solve-q-126', 2, 'Write "= w + y − z" and circle choice 2', 'Write "= w + y − z" and circle choice 1')
    _replace(M, 'solve-q-126', 2, 'w plus y minus z. Choice two.', 'w plus y minus z. Choice one.')
    _replace(M, 'solve-q-126', 3, 'Next to the choices write their values: 21, 19, 29, 13', 'Next to the choices write their values: 19, 21, 29, 13')
    _replace(M, 'solve-q-126', 3, 'The choices give twenty-one, nineteen, twenty-nine and thirteen. All different — one substitution is enough.',
             'The choices give nineteen, twenty-one, twenty-nine and thirteen. All different — one substitution is enough.')
    _replace(M, 'solve-q-126', 3, 'Circle choice 2', 'Circle choice 1')
    _replace(M, 'solve-q-126', 3, 'Nineteen. Choice two.', 'Nineteen. Choice one.')
    # q-127: key 3 -> 2 ((x+18)(x+2), (x+12)(x+3), (x+36)(x+1), (x+8)(x+4.5)); the not-whole choice stays choice 4.
    _choices(M, 'q-127', [1, 3, 2, 4], [('The sums are $20$, $37$, $15$ and $12.5$.', 'The sums are $20$, $15$, $37$ and $12.5$.'),
                                         ('The answer is choice 3.', 'The answer is choice 2.'),
                                         ('choice 3 gives $13\\cdot4=52$', 'choice 2 gives $13\\cdot4=52$')])
    _replace(M, 'solve-q-127', 2, 'Next to each choice write the sum of the two numbers: 20, 37, 15, 12.5',
             'Next to each choice write the sum of the two numbers: 20, 15, 37, 12.5')
    _replace(M, 'solve-q-127', 2, 'Eighteen plus two: twenty x. Thirty-six plus one: thirty-seven x. Twelve plus three: fifteen x. Eight plus four and a half: twelve and a half x.',
             'Eighteen plus two: twenty x. Twelve plus three: fifteen x. Thirty-six plus one: thirty-seven x. Eight plus four and a half: twelve and a half x.')
    _replace(M, 'solve-q-127', 2, 'Circle choice 3', 'Circle choice 2')
    _replace(M, 'solve-q-127', 2, 'Fifteen x — choice three.', 'Fifteen x — choice two.')
    _replace(M, 'solve-q-127', 3, 'Next to the choices write: 19·3 = 57, 37·2 = 74, 13·4 = 52, 9·5.5 → not whole',
             'Next to the choices write: 19·3 = 57, 13·4 = 52, 37·2 = 74, 9·5.5 → not whole')
    _replace(M, 'solve-q-127', 3, 'The choices give fifty-seven, seventy-four, fifty-two — and choice four: nine times five and a half.',
             'The choices give fifty-seven, fifty-two, seventy-four — and choice four: nine times five and a half.')
    _replace(M, 'solve-q-127', 3, 'Circle choice 3', 'Circle choice 2')
    _replace(M, 'solve-q-127', 3, 'Fifty-two. Choice three. Here, plugging in is actually the faster route.',
             'Fifty-two. Choice two. Here, plugging in is actually the faster route.')


def apply(M):
    lesson(M)
    guided_fixes(M)
    shortcuts(M)
    practice(M)
    so_fixes(M)
    restore_moved(M)
    summary(M)
    new_numbers(M)
    order_changes(M)
