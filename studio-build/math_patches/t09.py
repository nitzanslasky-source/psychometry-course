"""Topic 9 — Roots — Fundamentals. Fixes from student_review/review_t9-10.md (see t09_CHANGES.md)."""
from dsl import T, H, A, D, Q

TOPIC = 9
VID = 'roots'
CORE = 'root-core'
PRAC = 'root-practice'
QT = 'Roots Questions'
QSIDEBAR = ['Question %d' % k for k in range(1, 7)]


def _script(M, vid, n):
    """current script of a slide in DSL form (so we can append to it)."""
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


# ---------------------------------------------------------------- main lesson video
def fix_lesson(M):
    # slide 1 — no longer "fifteen questions, no videos"
    s = _script(M, VID, 1)
    s[2] = "At the end there's a table to learn by heart. Then practice — some questions come with a solution video."
    M.set_slide(VID, 1, script=s)

    # slide 2 — domain of a square root
    s = _script(M, VID, 2) + [
        A('√(x − 3) appears', T('$\\sqrt{x-3}$', size=56)),
        "So when does root of x minus three exist?",
        D('Write "x − 3 ≥ 0 → x ≥ 3"'),
        "Only when x minus three is zero or more. That means x is three or more.",
    ]
    M.set_slide(VID, 2, script=s)

    # slide 3 — one example with x < 0
    s = _script(M, VID, 3) + [
        D('Write "x = −3: √((−3)²) = √9 = 3 = −x"'),
        "One example with a negative x. Take x equals negative three.",
        "Negative three squared is nine. Root nine is three.",
        "And three is minus x. So when x is negative, root of x squared is minus x.",
    ]
    M.set_slide(VID, 3, script=s)

    # slide 4 — pull out the LARGEST square
    s = _script(M, VID, 4) + [
        "One more tip: pull out the LARGEST square you can find.",
        D('Under √72 write "√72 = √(4 · 18) = 2√18"'),
        "If you pull out only four, you get two root eighteen.",
        "Look at what's left inside: eighteen. It is still divisible by nine. Not done yet.",
        D('Write "2√18 = 2 · 3√2 = 6√2"'),
        "Same answer — but the largest square gets you there in one step.",
        "So always check: is the number left inside still divisible by four, nine or twenty-five?",
    ]
    M.set_slide(VID, 4, script=s)

    # slide 6 — division: no colon; the "number over a root" shortcut (was only on the memory card)
    s = _script(M, VID, 6)
    s = [D('Write "= √(75 ÷ 3) = √25 = 5"') if (isinstance(x, tuple) and x[0] == 'D') else x for x in s]
    s += [
        A('6/√3 appears', T('$\\frac{6}{\\sqrt3}$', size=66)),
        "A number over a root? Here's a shortcut.",
        D('Write "6 ÷ 3 = 2 → 2√3"'),
        "Divide the number by what's under the root: six divided by three is two. Then keep the root. Two root three.",
        D('Write "6/√3 = (2 · √3 · √3) ÷ √3 = 2√3"'),
        "Why? Three is root three times root three. One root three cancels. One stays.",
    ]
    M.set_slide(VID, 6, script=s)

    # slide 10 — rules table: two new rows, new closing line
    s = [
        "Here's the table to learn by heart.",
        A('Rule: √(a²) = |a|, every a', T('$\\sqrt{a^2}=|a|$ — every $a$', size=40)),
        A('Rule: √(ab) = √a·√b, a, b ≥ 0', T('$\\sqrt{ab}=\\sqrt a\\sqrt b$ — $a\\ge0,\\ b\\ge0$', size=40)),
        A('Rule: √(a/b) = √a/√b, a ≥ 0, b > 0', T('$\\sqrt{\\frac ab}=\\frac{\\sqrt a}{\\sqrt b}$ — $a\\ge0,\\ b>0$', size=40)),
        A('Rule: a√b = √(a²b), a, b ≥ 0', T('$a\\sqrt b=\\sqrt{a^2b}$ — $a\\ge0,\\ b\\ge0$', size=40)),
        A('Rule: ⁿ√(aᵐ) = a^(m/n), a ≥ 0', T('$\\sqrt[n]{a^m}=a^{\\frac mn}$ — $a\\ge0$', size=40)),
        A('Rule: ∛(a³) = a, every a', T('$\\sqrt[3]{a^3}=a$ — every $a$', size=40)),
        A('Warning: √(a+b) ≠ √a + √b', T('$\\sqrt{a+b}\\ne\\sqrt a+\\sqrt b$', size=40)),
        D('Box the last line'),
        "Read the conditions — they're part of every rule.",
        "Now practice. Some questions have a solution video right after them. Simplify first, then combine.",
    ]
    M.set_slide(VID, 10, script=s, active=11)

    # new slides (insert from the end so the numbers above stay valid)
    root_eq = dict(title='Root equations', mode='concept', active=10, pre=[], script=[
        A('√(x − 2) = 4 appears', T('$\\sqrt{x-2}=4$', size=62, gap=60)),
        "An equation with x under a root? Square both sides.",
        D('Write "x − 2 = 16 → x = 18"'),
        "Root of x minus two is four. Square: x minus two is sixteen. x is eighteen.",
        D('Write "Check: √(18 − 2) = √16 = 4 ✓"'),
        "Always check in the ORIGINAL equation. Squaring can add a fake solution.",
        A('x = √(3x) appears', T('$x=\\sqrt{3x}$', size=62)),
        "Here x is on both sides.",
        D('Write "x² = 3x → x² − 3x = 0 → x(x − 3) = 0"'),
        "Square: x squared is three x. Don't divide by x — x can be zero! Move everything to one side and factor.",
        D('Write "x = 0 or x = 3"'),
        "x is zero or three. Check: root zero is zero. Root nine is three. Both work.",
        "Exam shortcut: there are four choices. Plug each one in. It's often faster — and a fake solution fails the check.",
    ])
    M.insert_slides(VID, 9, [root_eq])

    pow_in = dict(title='Powers inside roots', mode='concept', active=8, pre=[], script=[
        A('ⁿ√(aᵐ) = a^(m/n) appears', T('$\\sqrt[n]{a^m}=a^{\\frac mn}$', size=58, gap=40)),
        "Any root works the same way. The power inside goes on top. The root index goes on the bottom.",
        A('⁴√(3⁸) appears', T('$\\sqrt[4]{3^8}$', size=56, gap=40)),
        D('Write "= 3^(8/4) = 3² = 9"'),
        "Fourth root of three to the eighth: eight over four is two. Three squared — nine.",
        A('8^(2/3) appears', T('$8^{\\frac23}$', size=56, gap=40)),
        "It works backwards too. Eight to the two thirds.",
        D('Write "= (∛8)² = 2² = 4"'),
        "The bottom, three, is a cube root. Cube root of eight is two. The top, two, is a square. Two squared — four.",
        "Tip: take the root first. The numbers stay small.",
        A('√(√a) = ⁴√a appears', T('$\\sqrt{\\sqrt a}=\\sqrt[4]a$', size=52)),
        "And a root of a root? Multiply the indexes. Root of a root is a fourth root.",
        D('Write "√(√81) = √9 = 3"'),
        "Root eighty-one is nine. Root nine is three.",
    ])
    M.insert_slides(VID, 8, [pow_in])

    inside = dict(title='Bring a number inside', mode='concept', active=3, pre=[], script=[
        A('3√7 appears', T('$3\\sqrt7$', size=62, gap=50)),
        "Now the other direction: bring a number INTO the root.",
        "For a square root, the number goes in squared.",
        D('Write "= √9 · √7 = √63"'),
        "Three is root nine. Root nine times root seven — root sixty-three.",
        A('2∛5 appears', T('$2\\sqrt[3]5$', size=62, gap=50)),
        "For a cube root, the number goes in cubed.",
        D('Write "= ∛8 · ∛5 = ∛40"'),
        "Two is the cube root of eight. So two cube root five is the cube root of forty.",
        A('3√7 ? 8 appears', T('$3\\sqrt7\\quad ?\\quad 8$', size=56)),
        "Why is this useful? Comparing.",
        D('Write "3√7 = √63 < √64 = 8"'),
        "Three root seven is root sixty-three. Eight is root sixty-four. So eight is bigger.",
    ])
    M.insert_slides(VID, 4, [inside])

    # sidebar + active indexes of the old slides (now 6..9, 11)
    M.set_sidebar(VID, ['What a root is', 'Root of a square', 'Pull out squares', 'Bring a number inside', 'Adding roots',
                        'Multiply & divide', 'Odd & even roots', 'Roots as powers', 'Powers inside roots', 'Not for sums',
                        'Root equations', 'The rules table'])
    for n, act in ((6, 4), (7, 5), (8, 6), (9, 7), (11, 9)):
        M.set_slide(VID, n, active=act)


# ---------------------------------------------------------------- second lesson video: exam traps
def traps_video(M):
    sb = ['Between 0 and 1', 'Compare by squaring', 'Different roots', 'Conjugates', 'Square of a sum']
    slides = [
        dict(mode='title', title='Roots — Exam traps', script=[
            "Now the traps. The exam loves these.",
            "Numbers between zero and one, comparing roots, and a partner that removes roots.",
            "Let's go.",
        ]),
        dict(title='Between 0 and 1', mode='concept', active=0, pre=[], script=[
            A('0 < x < 1: x² < x < √x appears', T('$0<x<1:\\quad x^2<x<\\sqrt x$', size=54, gap=50)),
            "Here's the rule to remember. Between zero and one, the root is BIGGER than the number. And the square is smaller.",
            D('Write "x = 0.25:  0.0625 < 0.25 < 0.5"'),
            "Take x equals zero point two five. Squared: zero point zero six two five. Root: zero point five.",
            "Squaring makes it smaller. Taking a root makes it bigger.",
            A('x > 1: √x < x < x² appears', T('$x>1:\\quad \\sqrt x<x<x^2$', size=54, gap=50)),
            D('Write "x = 9:  3 < 9 < 81"'),
            "Above one, it's the other way. Root nine is three — smaller than nine.",
            "At zero and at one, all three are equal.",
            "In a 'which is the largest' question with x between zero and one: plug in a number like one quarter. Then compare.",
        ]),
        dict(title='Compare by squaring', mode='concept', active=1, pre=[], script=[
            A('4√3 ? 5√2 appears', T('$4\\sqrt3\\quad ?\\quad 5\\sqrt2$', size=58, gap=50)),
            "Which is bigger? Don't guess. Square both.",
            D('Write "(4√3)² = 16 · 3 = 48"'),
            "Four root three, squared: sixteen times three — forty-eight.",
            D('Write "(5√2)² = 25 · 2 = 50"'),
            "Five root two, squared: twenty-five times two — fifty.",
            "Fifty is bigger. So five root two is bigger.",
            "This works because both numbers are positive. Bigger square — bigger number.",
            A('√70 appears', T('$\\sqrt{70}$', size=58)),
            "To estimate one root: put it between two perfect squares.",
            D('Write "√64 < √70 < √81 → 8 < √70 < 9"'),
            "Seventy is between sixty-four and eighty-one. So root seventy is between eight and nine.",
        ]),
        dict(title='Different roots', mode='concept', active=2, pre=[], script=[
            A('√2 ? ∛3 appears', T('$\\sqrt2\\quad ?\\quad \\sqrt[3]3$', size=60, gap=60)),
            "A square root and a cube root. Squaring alone won't remove the cube root.",
            "Raise both to a power that removes both roots. Two times three: the sixth power.",
            D('Write "(√2)⁶ = 2³ = 8"'),
            "Root two to the sixth: two to the third — eight.",
            D('Write "(∛3)⁶ = 3² = 9"'),
            "Cube root of three to the sixth: three squared — nine.",
            "Nine is bigger. So the cube root of three is bigger than root two.",
            A('rule appears', T('Square root and cube root: raise both to the 6th power.', size=40)),
            "Square root and cube root? Use the sixth power. It clears both.",
        ]),
        dict(title='Conjugates', mode='concept', active=3, pre=[], script=[
            A('(√a + √b)(√a − √b) = a − b appears', T('$(\\sqrt a+\\sqrt b)(\\sqrt a-\\sqrt b)=a-b$', size=52, gap=50)),
            "Remember the difference of squares? It removes roots.",
            D('Write "(√5 + √3)(√5 − √3) = 5 − 3 = 2"'),
            "Root five plus root three, times root five minus root three. Five minus three. Two. No roots left.",
            A('1/(√2 − 1) appears', T('$\\frac{1}{\\sqrt2-1}$', size=60)),
            "That's how you remove a root from the bottom.",
            "Multiply the top and the bottom by the partner: root two PLUS one.",
            D('Write "= (√2 + 1) ÷ [(√2 − 1)(√2 + 1)] = (√2 + 1) ÷ (2 − 1) = √2 + 1"'),
            "The bottom is two minus one — one. The answer: root two plus one.",
        ]),
        dict(title='Square of a sum', mode='concept', active=4, pre=[], script=[
            A('(√a + √b)² = a + b + 2√(ab) appears', T('$(\\sqrt a+\\sqrt b)^2=a+b+2\\sqrt{ab}$', size=52, gap=50)),
            "Squaring a sum of roots: don't forget the middle term.",
            D('Write "(√2 + √3)² = 2 + 3 + 2√6 = 5 + 2√6"'),
            "Root two plus root three, squared. Two plus three — and two root six in the middle. Not five. Five plus two root six.",
            A('√3 + √5 ? √15 appears', T('$\\sqrt3+\\sqrt5\\quad ?\\quad \\sqrt{15}$', size=52)),
            "This is how you compare a sum of roots with a root. Square both.",
            D('Write "8 + 2√15  vs  15 → 2√15 vs 7 → √60 vs √49"'),
            "Left: three plus five plus two root fifteen — eight plus two root fifteen. Right: fifteen.",
            "Take eight from both: two root fifteen against seven. Bring the two inside: root sixty against root forty-nine.",
            "Root sixty is bigger. So root three plus root five is bigger than root fifteen.",
            "Now three questions with solution videos.",
        ]),
    ]
    M.new_video('r26-t09-traps', TOPIC, 'Roots — Exam traps', sb, slides, CORE, after='q-247')


# ---------------------------------------------------------------- guided questions
def guided(M, qid, stem, choices, correct, expl, after, sol_slides, intro):
    M.new_q(qid, TOPIC, stem, choices, correct, expl)
    M.place_q(qid, CORE, after=after)
    n = M.next_question_number(TOPIC)
    slides = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in sol_slides:
        slides.append(dict(mode='question', title=title, active=n - 1, pre=[Q(qid)], script=script))
    M.new_video('solve-' + qid, TOPIC, QT, QSIDEBAR, slides, CORE, kind='solution', qid=qid)
    return 'solve-' + qid


def add_guided(M):
    # Q1 — power inside a root
    guided(M, 'q-r26-t09-01', '$\\sqrt[4]{9^{6}} = ?$', ['$81$', '$27$', '$729$', '$9$'], 2, [
        'The power inside goes on top, the root index goes on the bottom: $\\sqrt[4]{9^6}=9^{\\frac64}=9^{\\frac32}$.',
        'Take the root first: $9^{\\frac32}=\\left(\\sqrt9\\right)^3=3^3=27$.',
        'Another way: $9^6=\\left(3^2\\right)^6=3^{12}$, and $\\sqrt[4]{3^{12}}=3^{\\frac{12}{4}}=3^3=27$.',
        'The trap: $6-4=2$ gives $9^2=81$. Divide the exponents, don\'t subtract them.'],
        after='q-234', intro=["Question one.", "A fourth root of a power. Use the new rule: power over index."],
        sol_slides=[
            ('Method 1 · Power over index', [
                "The power inside, six, goes on top. The root index, four, goes on the bottom.",
                D('Write "⁴√(9⁶) = 9^(6/4) = 9^(3/2)"'),
                "Six over four is three over two. Nine to the three halves.",
                D('Write "9^(3/2) = (√9)³ = 3³ = 27"'),
                "The bottom, two, is a square root. Root nine is three. The top, three, is a cube. Three cubed — twenty-seven.",
                D('Circle choice 2'),
                "Twenty-seven. Choice two.",
                "Here's the trap: six minus four is two, and nine squared is eighty-one. That's choice one. Divide — don't subtract.",
            ]),
            ('Method 2 · Break into primes', [
                "A second way: write nine as three squared.",
                D('Write "9⁶ = (3²)⁶ = 3¹²"'),
                "Three squared, to the sixth — three to the twelfth.",
                D('Write "⁴√(3¹²) = 3^(12/4) = 3³ = 27"'),
                "Twelve over four is three. Three cubed — twenty-seven. Same answer. Choice two.",
            ]),
        ])

    # Q2 — bring inside to compare (after q-244)
    guided(M, 'q-r26-t09-02', 'Which of the following is the largest?',
           ['$5.2$', '$3\\sqrt{3}$', '$2\\sqrt{7}$', '$\\sqrt{26}$'], 3, [
        'All four numbers are positive. Compare their squares (this is the same as bringing each number inside the root).',
        '$5.2^2=27.04$, $\\left(3\\sqrt3\\right)^2=9\\cdot3=27$, $\\left(2\\sqrt7\\right)^2=4\\cdot7=28$, $\\left(\\sqrt{26}\\right)^2=26$.',
        'The largest square is $28$. Therefore $2\\sqrt7=\\sqrt{28}$ is the largest.'],
        after='q-244', intro=["Question two.", "Four numbers, and they all look close. Bring everything inside a root."],
        sol_slides=[
            ('Bring every number inside', [
                "The numbers are close. Estimating is risky. So bring every number inside the root — that means squaring it.",
                D('Write "(3√3)² = 9 · 3 = 27"'),
                "Three root three: three squared is nine, times three — twenty-seven.",
                D('Write "(2√7)² = 4 · 7 = 28"'),
                "Two root seven: four times seven — twenty-eight.",
                D('Write "(√26)² = 26"'),
                "Root twenty-six squared is just twenty-six.",
                D('Write "5.2² = 27.04"'),
                "And five point two squared: twenty-seven point zero four.",
                "The largest square is twenty-eight. So two root seven is the largest.",
                D('Circle choice 3'),
                "Choice three.",
                "The trap: five point two looks big. But its square is only twenty-seven point zero four.",
            ]),
        ])

    # Q3 — root equation, plug in the answers (before q-247)
    guided(M, 'q-r26-t09-03', 'Given: $\\sqrt{x+6}=x$\nWhat is $x$?',
           ['$-2$', '$3$', '$-2$ or $3$', '$6$'], 2, [
        'Plug in the choices. $x=-2$: $\\sqrt{-2+6}=\\sqrt4=2\\ne-2$. Not a solution.',
        '$x=3$: $\\sqrt{3+6}=\\sqrt9=3$. A solution.',
        '$x=6$: $\\sqrt{12}\\ne6$. Not a solution. Choice 3 includes $-2$, which is not a solution.',
        'Why is $-2$ a trap? After squaring we get $x+6=x^2$, and $-2$ solves that: $(-2)^2=4=-2+6$. But a square root is never negative. Therefore, $\\sqrt{x+6}=-2$ is impossible. Only $x=3$ works.'],
        after='q-246', intro=["Question three.", "A root equation with four choices. Let's plug them in."],
        sol_slides=[
            ('Plug in the answers', [
                "x is under the root and outside it. We have four choices — just try them.",
                D('Write "x = −2: √4 = 2 ≠ −2 ✗"'),
                "Negative two: root of four is two. Two is not negative two. Out.",
                D('Write "x = 3: √9 = 3 ✓"'),
                "Three: root nine is three. It works.",
                D('Write "x = 6: √12 ≠ 6 ✗"'),
                "Six: root twelve is less than four. Not six. Out.",
                "Choice three says negative two or three. But negative two failed. So only three.",
                D('Circle choice 2'),
                "Choice two.",
            ]),
            ('Why −2 is a trap', [
                "Why is negative two in the choices at all?",
                D('Write "x + 6 = x²  →  (−2)² = 4 = −2 + 6"'),
                "If you square both sides, you get x plus six equals x squared. Negative two solves that equation.",
                "But the original says a root equals x. A root is never negative. So negative two is a fake solution.",
                "Squaring can add fake solutions. Always check in the original equation.",
            ]),
        ])

    traps_video(M)

    # Q4 — between 0 and 1
    guided(M, 'q-r26-t09-04', 'Given: $0<x<1$\nWhich of the following is the largest?',
           ['$x^2$', '$x$', '$\\sqrt{x}$', '$x^3$'], 3, [
        'Plug in an easy number between $0$ and $1$: $x=\\frac14$.',
        '$x^2=\\frac1{16}$, $x=\\frac14$, $\\sqrt x=\\frac12$, $x^3=\\frac1{64}$. The largest is $\\sqrt x=\\frac12$.',
        'The rule: for $0<x<1$, $x^3<x^2<x<\\sqrt x$.'],
        after='r26-t09-traps', intro=["Question four.", "x is between zero and one. Plug in a number."],
        sol_slides=[
            ('Plug in x = 1/4', [
                "x is between zero and one. Choose an easy number: one quarter. Its root is nice — one half.",
                D('Write "x² = 1/16,  x = 1/4,  √x = 1/2,  x³ = 1/64"'),
                "x squared: one sixteenth. x: one quarter. Root x: one half. x cubed: one sixty-fourth.",
                "The largest is one half — root x.",
                D('Circle choice 3'),
                "Choice three.",
                "And the rule: between zero and one, powers make it smaller, and the root makes it bigger.",
            ]),
        ])

    # Q5 — different indices
    guided(M, 'q-r26-t09-05', 'Which of the following is the largest?',
           ['$\\sqrt{3}$', '$\\sqrt[6]{28}$', '$\\sqrt[3]{5}$', '$\\sqrt[6]{26}$'], 2, [
        'The roots have indexes $2$, $3$ and $6$. Raise every number to the $6$th power.',
        '$\\left(\\sqrt3\\right)^6=3^3=27$, $\\left(\\sqrt[6]{28}\\right)^6=28$, $\\left(\\sqrt[3]5\\right)^6=5^2=25$, $\\left(\\sqrt[6]{26}\\right)^6=26$.',
        'The largest is $28$. Therefore $\\sqrt[6]{28}$ is the largest.'],
        after='solve-q-r26-t09-04', intro=["Question five.", "Square roots, cube roots, sixth roots. One power clears them all."],
        sol_slides=[
            ('Raise all to the 6th power', [
                "Square root, cube root and sixth roots. The sixth power clears all of them.",
                D('Write "(√3)⁶ = 3³ = 27"'),
                "Root three to the sixth: three cubed — twenty-seven.",
                D('Write "(∛5)⁶ = 5² = 25"'),
                "Cube root of five to the sixth: five squared — twenty-five.",
                D('Write "(⁶√28)⁶ = 28,  (⁶√26)⁶ = 26"'),
                "The sixth roots just give back twenty-eight and twenty-six.",
                "The largest is twenty-eight. So the sixth root of twenty-eight is the largest.",
                D('Circle choice 2'),
                "Choice two.",
            ]),
        ])

    # Q6 — conjugate
    guided(M, 'q-r26-t09-06', '$\\frac{1}{\\sqrt{3}-\\sqrt{2}} = ?$',
           ['$1$', '$\\sqrt{3}+\\sqrt{2}$', '$\\sqrt{3}-\\sqrt{2}$', '$5+2\\sqrt{6}$'], 2, [
        'Multiply the top and the bottom by the partner $\\sqrt3+\\sqrt2$.',
        'The bottom: $\\left(\\sqrt3-\\sqrt2\\right)\\left(\\sqrt3+\\sqrt2\\right)=3-2=1$. The top: $\\sqrt3+\\sqrt2$.',
        'Therefore $\\frac{1}{\\sqrt3-\\sqrt2}=\\frac{\\sqrt3+\\sqrt2}{1}=\\sqrt3+\\sqrt2$.',
        'Check from the answers: $\\left(\\sqrt3+\\sqrt2\\right)\\left(\\sqrt3-\\sqrt2\\right)=1$. Therefore, $\\sqrt3+\\sqrt2$ is exactly $1$ divided by $\\sqrt3-\\sqrt2$.',
        'The trap: $\\sqrt3-\\sqrt2$ is not $\\sqrt1$. Roots do not split over a minus.'],
        after='solve-q-r26-t09-05', intro=["Question six.", "A root difference on the bottom. Call in the partner."],
        sol_slides=[
            ('Method 1 · Multiply by the partner', [
                "Roots on the bottom. Multiply the top and the bottom by the partner: root three PLUS root two.",
                D('Write "Bottom: (√3 − √2)(√3 + √2) = 3 − 2 = 1"'),
                "The bottom is a difference of squares: three minus two — one.",
                D('Write "Top: 1 · (√3 + √2) = √3 + √2"'),
                "The top is root three plus root two. Divided by one — it stays.",
                D('Circle choice 2'),
                "Root three plus root two. Choice two.",
                "The trap: root three minus root two is NOT root one. That's choice one.",
            ]),
            ('Method 2 · Work back from the answers', [
                "Second way: check a choice. The answer is one over the bottom. So, the choice times the bottom must give one.",
                D('Write "(√3 + √2)(√3 − √2) = 3 − 2 = 1 ✓"'),
                "Root three plus root two, times root three minus root two: one. So it fits. Choice two.",
            ]),
        ])


# ---------------------------------------------------------------- existing questions: text
def fix_questions(M):
    M.set_q('q-233', expl=[
        'Find each cube root: $\\sqrt[3]{8}=2$, $\\sqrt[3]{0}=0$ and $\\sqrt[3]{-1}=-1$ (odd roots of negative numbers exist).',
        'Then $2-0-(-1)=2+1=3$.'])
    M.set_q('q-234', expl=[
        'A $6$th root is an even root. Any real number to the $6$th power is zero or positive. Therefore, no number to the $6$th power gives $-64$.',
        'So, $\\sqrt[6]{-64}$ has no real value. (Careful: $2^6=64$, not $-64$.)'])
    M.set_q('q-235', expl=[
        'The power inside goes on top, the root index on the bottom: $\\sqrt[3]{5^6}=5^{\\frac63}=5^2=25$.'])
    M.set_q('q-236', expl=[
        'A power of $\\frac14$ is a fourth root: $81^{\\frac14}=\\sqrt[4]{81}=3$, because $3^4=81$.'])
    M.set_q('q-237', expl=['Put the product under one root: $\\sqrt{27}\\cdot\\sqrt{3}=\\sqrt{27\\cdot3}=\\sqrt{81}=9$.'])
    M.set_q('q-238', expl=['A square root times itself gives the number under the root: $\\sqrt{31}\\cdot\\sqrt{31}=\\sqrt{31\\cdot31}=31$.'])
    M.set_q('q-240', expl=['Put the quotient under one root: $\\frac{\\sqrt{50}}{\\sqrt2}=\\sqrt{\\frac{50}{2}}=\\sqrt{25}=5$.'])
    M.set_q('q-241', expl=['Put the quotient under one root: $\\frac{\\sqrt3}{\\sqrt{48}}=\\sqrt{\\frac{3}{48}}=\\sqrt{\\frac{1}{16}}=\\frac14$.'])
    # q-239: original (restored in pass 2), text clean-up only
    M.set_q('q-239', stem='$\\sqrt[3]{9}\\cdot\\sqrt[3]{9}\\cdot\\sqrt[3]{9} = ?$', expl=[
        'Three copies of a cube root multiply back to the number under it: $\\sqrt[3]{9}\\cdot\\sqrt[3]{9}\\cdot\\sqrt[3]{9}=\\left(\\sqrt[3]{9}\\right)^3=9$.',
        'Or put everything under one root: $\\sqrt[3]{9\\cdot9\\cdot9}=\\sqrt[3]{729}=9$, because $9^3=729$.'])
    # q-242: the original question (restored in pass 2), text clean-up only
    M.set_q('q-242', stem='$\\sqrt[2.5]{\\sqrt{243}} = ?$\n(The root index $2.5$ means the power $\\frac{1}{2.5}$: $\\sqrt[2.5]{\\sqrt{243}}=\\left(\\sqrt{243}\\right)^{\\frac{1}{2.5}}$.)',
            choices=['$9$', '$27$', '$3$', '$1$'], correct=3, expl=[
        'Write both roots as powers: $\\sqrt{243}=243^{\\frac12}$, and the root index $2.5$ is the power $\\frac{1}{2.5}=\\frac25$.',
        'Power of a power: multiply the exponents. $\\left(243^{\\frac12}\\right)^{\\frac25}=243^{\\frac12\\cdot\\frac25}=243^{\\frac15}=\\sqrt[5]{243}$.',
        '$243=3^5$, therefore $\\sqrt[5]{243}=3$.'])
    M.set_q('q-243', expl=['Bring the $3$ inside the root by squaring it: $3\\sqrt7=\\sqrt9\\cdot\\sqrt7=\\sqrt{9\\cdot7}=\\sqrt{63}$.'])
    M.set_q('q-244', expl=['To go inside a cube root, the $3$ is cubed: $3\\sqrt[3]{2}=\\sqrt[3]{27}\\cdot\\sqrt[3]{2}=\\sqrt[3]{27\\cdot2}=\\sqrt[3]{54}$.'])
    M.set_q('q-245', expl=[
        'Estimate each number. $\\sqrt7$ is between $\\sqrt4=2$ and $\\sqrt9=3$: about $2.65$.',
        '$\\sqrt[3]{30}$ is a little more than $\\sqrt[3]{27}=3$: about $3.1$. And $\\pi\\approx3.14$.',
        'Order: $\\sqrt7<3<\\sqrt[3]{30}<\\pi$. The smallest is $\\sqrt7$.'])
    M.set_q('q-246', expl=[
        '$\\sqrt3\\approx1.73$. The distance to $1.7$ is about $0.03$, and the distance to $1.8$ is about $0.07$. The closest is $1.7$.',
        'Check without the estimate: the middle between $1.7$ and $1.8$ is $1.75$, and $1.75^2=3.0625>3$. Therefore, $\\sqrt3<1.75$, closer to $1.7$.'])
    M.set_q('q-247', stem='How many solutions does the equation $x=\\sqrt{5x}$ have?', expl=[
        'Square both sides: $x^2=5x$. Do not divide by $x$ ($x$ can be $0$). Move everything to one side and factor: $x^2-5x=0$, $x(x-5)=0$.',
        'Therefore $x=0$ or $x=5$.',
        'Check both in the original equation: $0=\\sqrt0$ and $5=\\sqrt{25}$. Both work. Therefore, there are $2$ solutions.'])

    # extra practice 1-7
    M.set_q('alg-extra-root-practice-1', stem='$\\sqrt{144}-\\sqrt{49} = ?$', choices=['$11$', '$19$', '$5$', '$7$'],
            expl=['$\\sqrt{144}=12$ and $\\sqrt{49}=7$. Therefore $12-7=5$.',
                  'The trap is $\\sqrt{144-49}=\\sqrt{95}$: a root does not split over a minus.'])
    M.set_q('alg-extra-root-practice-2', stem='$\\sqrt{72} = ?$', choices=['$8\\sqrt2$', '$36$', '$6\\sqrt2$', '$3\\sqrt8+1$'],
            expl=['Pull out the largest square: $72=36\\cdot2$. Therefore, $\\sqrt{72}=\\sqrt{36}\\cdot\\sqrt2=6\\sqrt2$.'])
    M.set_q('alg-extra-root-practice-3', stem='Given: $x<0$\n$\\sqrt{x^2} = ?$', choices=['$x^2$', '$-x^2$', '$-x$', '$x$'],
            expl=['$\\sqrt{x^2}=|x|$. For $x<0$, $|x|=-x$.',
                  'Example: $x=-3$. $\\sqrt{(-3)^2}=\\sqrt9=3$, and $3=-x$.'])
    M.set_q('alg-extra-root-practice-4', stem='$\\sqrt[3]{-125} = ?$', choices=['$5$', '$-25$', '$25$', '$-5$'],
            expl=['An odd root keeps the minus sign: $(-5)^3=-125$. Therefore, $\\sqrt[3]{-125}=-5$.'])
    M.set_q('alg-extra-root-practice-5', stem='Given: $\\sqrt{x+7}=5$\nWhat is $x$?', choices=['$18$', '$12$', '$25$', '$32$'],
            expl=['Square both sides: $x+7=25$. Therefore, $x=18$.', 'Check: $\\sqrt{18+7}=\\sqrt{25}=5$.'])
    M.set_q('alg-extra-root-practice-6', stem='$\\sqrt{12}\\cdot\\sqrt{27} = ?$', choices=['$18$', '$9$', '$36$', '$324$'],
            expl=['Put the product under one root: $\\sqrt{12}\\cdot\\sqrt{27}=\\sqrt{12\\cdot27}=\\sqrt{324}=18$.',
                  'Or simplify first: $2\\sqrt3\\cdot3\\sqrt3=6\\cdot3=18$.'])
    M.set_q('alg-extra-root-practice-7', stem='Between which two consecutive whole numbers is $\\sqrt{70}$?',
            choices=['$9$ and $10$', '$6$ and $7$', '$8$ and $9$', '$7$ and $8$'],
            expl=['Put $70$ between two perfect squares: $64<70<81$.', 'Therefore $\\sqrt{64}<\\sqrt{70}<\\sqrt{81}$, that is, $8<\\sqrt{70}<9$.'])


# ---------------------------------------------------------------- new practice (exam level)
NEW_PRACTICE = [
    ('q-r26-t09-09', 'Which of the following is true?',
     ['$0.5^2<0.5<\\sqrt{0.5}$', '$\\sqrt{0.5}<0.5<0.5^2$', '$0.5<0.5^2<\\sqrt{0.5}$', '$0.5^2<\\sqrt{0.5}<0.5$'], 1, [
        '$0.5$ is between $0$ and $1$. Squaring makes it smaller, and a root makes it bigger.',
        '$0.5^2=0.25$ and $\\sqrt{0.5}\\approx0.71$. Therefore $0.5^2<0.5<\\sqrt{0.5}$.']),
    ('q-r26-t09-10', '$8^{\\frac{2}{3}} = ?$', ['$\\frac{16}{3}$', '$4$', '$2$', '$64$'], 2, [
        'The bottom, $3$, is a cube root. The top, $2$, is a square.',
        '$8^{\\frac23}=\\left(\\sqrt[3]8\\right)^2=2^2=4$.']),
    ('q-r26-t09-11', 'Given: $x>0$\n$\\sqrt[4]{x^8} = ?$', ['$x^2$', '$x^4$', '$x^{12}$', '$x^{32}$'], 1, [
        'The power inside goes on top, the root index on the bottom: $\\sqrt[4]{x^8}=x^{\\frac84}=x^2$.']),
    ('q-r26-t09-12', 'What are all the values of $x$ for which $\\sqrt{2-x}$ is defined?', ['$x\\le2$', '$x\\ge2$', '$x<2$', '$x\\ge-2$'], 1, [
        'The number inside a square root cannot be negative: $2-x\\ge0$.',
        'Therefore $x\\le2$. ($x=2$ is allowed: $\\sqrt0=0$.)']),
    ('q-r26-t09-13', 'Given: $\\sqrt{2x+3}=3$\nWhat is $x$?', ['$0$', '$3$', '$4.5$', '$6$'], 2, [
        'Square both sides: $2x+3=9$. Therefore, $2x=6$ and $x=3$.',
        'Check: $\\sqrt{2\\cdot3+3}=\\sqrt9=3$.']),
    ('q-r26-t09-14', 'Which of the following is the largest?', ['$2\\sqrt{11}$', '$3\\sqrt{5}$', '$\\sqrt{43}$', '$6.5$'], 2, [
        'All the numbers are positive. Compare their squares.',
        '$\\left(2\\sqrt{11}\\right)^2=4\\cdot11=44$, $\\left(3\\sqrt5\\right)^2=9\\cdot5=45$, $\\left(\\sqrt{43}\\right)^2=43$, $6.5^2=42.25$.',
        'The largest square is $45$. Therefore $3\\sqrt5$ is the largest.']),
    ('q-r26-t09-15', 'Which of the following is the smallest?',
     ['$\\sqrt[3]{4}$', '$\\sqrt[6]{15}$', '$\\sqrt{2}$', '$\\sqrt[6]{17}$'], 3, [
        'The indexes are $2$, $3$ and $6$. Raise every number to the $6$th power.',
        '$\\left(\\sqrt[3]4\\right)^6=4^2=16$, $\\left(\\sqrt[6]{15}\\right)^6=15$, $\\left(\\sqrt2\\right)^6=2^3=8$, $\\left(\\sqrt[6]{17}\\right)^6=17$.',
        'The smallest is $8$. Therefore $\\sqrt2$ is the smallest.']),
    ('q-r26-t09-16', '$(\\sqrt{7}+\\sqrt{5})(\\sqrt{7}-\\sqrt{5}) = ?$', ['$\\sqrt{2}$', '$12$', '$2$', '$\\sqrt{12}$'], 3, [
        'Difference of squares: $(\\sqrt a+\\sqrt b)(\\sqrt a-\\sqrt b)=a-b$.',
        'Therefore $(\\sqrt7+\\sqrt5)(\\sqrt7-\\sqrt5)=7-5=2$.']),
    ('q-r26-t09-17', '$(\\sqrt{5}+1)^2 = ?$', ['$6$', '$6+\\sqrt{5}$', '$6+2\\sqrt{5}$', '$5+2\\sqrt{5}$'], 3, [
        '$(a+b)^2=a^2+2ab+b^2$ with $a=\\sqrt5$ and $b=1$.',
        '$(\\sqrt5+1)^2=5+2\\sqrt5+1=6+2\\sqrt5$.',
        'The trap is $6$: it forgets the middle term $2\\sqrt5$.']),
    ('q-r26-t09-18', '$\\frac{4}{\\sqrt{5}-1} = ?$', ['$\\sqrt{5}+1$', '$\\sqrt{5}-1$', '$4\\sqrt{5}+4$', '$1$'], 1, [
        'Multiply the top and the bottom by the partner $\\sqrt5+1$.',
        'The bottom: $(\\sqrt5-1)(\\sqrt5+1)=5-1=4$. The top: $4(\\sqrt5+1)$.',
        'Therefore $\\frac{4(\\sqrt5+1)}{4}=\\sqrt5+1$.',
        'Check from the answers: $(\\sqrt5+1)(\\sqrt5-1)=4$. Correct.']),
    ('q-r26-t09-19', 'Which of the following is true?',
     ['$\\sqrt{3}+\\sqrt{5}>\\sqrt{15}$', '$\\sqrt{3}+\\sqrt{5}=\\sqrt{15}$', '$\\sqrt{3}+\\sqrt{5}<\\sqrt{15}$', '$\\sqrt{3}+\\sqrt{5}=\\sqrt{8}$'], 1, [
        'Both sides are positive. Compare their squares.',
        'Left: $(\\sqrt3+\\sqrt5)^2=3+5+2\\sqrt{15}=8+2\\sqrt{15}$. Right: $(\\sqrt{15})^2=15$.',
        'Subtract $8$ from both: $2\\sqrt{15}$ against $7$. Bring the $2$ inside: $\\sqrt{60}$ against $\\sqrt{49}$.',
        '$\\sqrt{60}>\\sqrt{49}$. Therefore $\\sqrt3+\\sqrt5>\\sqrt{15}$.',
        'Choice 4 is the trap: a root does not split over a plus.']),
]


def add_practice(M):
    for qid, stem, ch, c, ex in NEW_PRACTICE:
        M.new_q(qid, TOPIC, stem, ch, c, ex); M.place_q(qid, PRAC)
    p = 'alg-extra-root-practice-'
    # (pass 2: q-239 and alg-extra-root-practice-6 are original questions and stay in the course)
    # q-227, alg-extra-exponent-extra-2 and -7 are moved here by the T8 patch
    M.practice_order(PRAC, [p + '1', p + '4', p + '2', p + '6', p + '3', 'alg-extra-exponent-extra-7', p + '7', p + '5',
                            'q-r26-t09-13', 'q-r26-t09-12', 'q-r26-t09-10', 'alg-extra-exponent-extra-2', 'q-227',
                            'q-r26-t09-11', 'q-r26-t09-16', 'q-r26-t09-09', 'q-r26-t09-17', 'q-r26-t09-14',
                            'q-r26-t09-18', 'q-r26-t09-15', 'q-r26-t09-19'])


# ---------------------------------------------------------------- memory card
def fix_card(M):
    c = M.card('roots')
    rows = c['tables'][0]['rows']
    rows[1][1] = '\\(a\\ge0,\\ b\\ge0\\)'
    rows.insert(4, ['\\(\\sqrt[n]{a^m}=a^{\\frac mn}\\)', 'power on top, root index on the bottom: \\(\\sqrt[3]{5^6}=5^2\\)'])
    rows.insert(5, ['\\(a\\sqrt b=\\sqrt{a^2b}\\)', '\\(a\\ge0,\\ b\\ge0\\): \\(3\\sqrt7=\\sqrt{63}\\), \\(2\\sqrt[3]5=\\sqrt[3]{40}\\)'])
    rows.insert(6, ['\\(\\sqrt{\\sqrt a}=\\sqrt[4]a\\)', 'root of a root: multiply the indexes'])
    c['tables'].append({'title': 'Exam traps', 'head': ['Rule', 'Example'], 'rows': [
        ['\\(0<x<1:\\ x^2<x<\\sqrt x\\)', '\\(x=\\frac14:\\ \\frac1{16}<\\frac14<\\frac12\\)'],
        ['compare by squaring (positive numbers)', '\\(4\\sqrt3=\\sqrt{48}<\\sqrt{50}=5\\sqrt2\\)'],
        ['square root vs cube root: 6th power', '\\((\\sqrt2)^6=8<9=(\\sqrt[3]3)^6\\)'],
        ['\\((\\sqrt a+\\sqrt b)(\\sqrt a-\\sqrt b)=a-b\\)', '\\(\\frac1{\\sqrt2-1}=\\sqrt2+1\\)'],
        ['\\((\\sqrt a+\\sqrt b)^2=a+b+2\\sqrt{ab}\\)', '\\((\\sqrt2+\\sqrt3)^2=5+2\\sqrt6\\)'],
    ]})
    c['tips'] = [
        'Pull out the largest square: \\(\\sqrt{72}=\\sqrt{36\\cdot2}=6\\sqrt2\\).',
        'Number over a root: divide by the number under the root, keep the root. \\(\\frac6{\\sqrt3}=(6\\div3)\\sqrt3=2\\sqrt3\\).',
        'Inside a square root: never negative. \\(\\sqrt{x-3}\\) exists only for \\(x\\ge3\\).',
        'Root equations: square both sides, then check in the original equation. Or plug in the choices.',
        'Estimate a root between two perfect squares: \\(8<\\sqrt{70}<9\\).',
    ]


# ---------------------------------------------------------------- pass 2: summary lesson before the practice
def summary(M):
    sb = ['What a root is', 'Simplify roots', 'Multiply & divide', 'Roots as powers', 'Not for sums',
          'Comparing roots', 'Between 0 and 1', 'Conjugates', 'Root equations', 'Before you practice']
    slides = [
        dict(mode='title', title='Summary', script=[
            "Roots — a quick summary before you practice.",
            "Everything important from this topic, one idea at a time.",
        ]),
        dict(title='What a root is', mode='concept', active=0, pre=[], script=[
            A('√169 = 13 and x² = 169 → x = ±13 appear', T('$\\sqrt{169}=13\\qquad x^2=169\\ \\Rightarrow\\ x=\\pm13$', size=50, gap=50)),
            "A root is never negative. Root one hundred sixty-nine is just thirteen.",
            "But the equation x squared equals one hundred sixty-nine has two solutions: thirteen and negative thirteen.",
            A('√(x²) = |x| appears', T('$\\sqrt{x^2}=|x|$', size=56, gap=50)),
            "Root of x squared is the absolute value of x. If x is negative, it's minus x.",
            A('never negative inside appears', T('Inside a square root: never negative.', size=40)),
            "And the number inside a square root can't be negative.",
        ]),
        dict(title='Simplify roots', mode='concept', active=1, pre=[], script=[
            A('√80 = 4√5 appears', T('$\\sqrt{80}=\\sqrt{16\\cdot5}=4\\sqrt5$', size=54, gap=50)),
            "Pull out the LARGEST square you can find.",
            "Then look at what's left inside. Still divisible by four, nine or twenty-five? Keep going.",
            A('√80 + √20 = 6√5 appears', T('$\\sqrt{80}+\\sqrt{20}=4\\sqrt5+2\\sqrt5=6\\sqrt5$', size=48)),
            "Roots add like letters, but only the same root. So simplify first, then add.",
        ]),
        dict(title='Multiply & divide', mode='concept', active=2, pre=[], script=[
            A('product and quotient rules appear', T('$\\sqrt a\\cdot\\sqrt b=\\sqrt{ab}\\qquad \\frac{\\sqrt a}{\\sqrt b}=\\sqrt{\\frac ab}$', size=50, gap=40)),
            "Multiplying or dividing? Put everything under one root.",
            A('22/√11 = 2√11 appears', T('$\\frac{22}{\\sqrt{11}}=2\\sqrt{11}$', size=54, gap=40)),
            "A number over a root: divide by the number under the root, and keep the root. Twenty-two divided by eleven is two. Two root eleven.",
            A('3√6 = √54 appears', T('$3\\sqrt6=\\sqrt{54}$', size=54)),
            "To bring a number inside a square root, square it. For a cube root, cube it.",
        ]),
        dict(title='Roots as powers', mode='concept', active=3, pre=[], script=[
            A('ⁿ√(aᵐ) = a^(m/n) appears', T('$\\sqrt[n]{a^m}=a^{\\frac mn}$', size=58, gap=50)),
            "A root is a fractional power. The power inside goes on top. The root index goes on the bottom.",
            A('27^(2/3) = 9 appears', T('$27^{\\frac23}=\\left(\\sqrt[3]{27}\\right)^2=3^2=9$', size=52, gap=50)),
            "Take the root first. The numbers stay small.",
            "A root of a root? Multiply the indexes. Root of a root is a fourth root.",
            "And odd roots of negative numbers exist. Even roots of negative numbers don't.",
        ]),
        dict(title='Not for sums', mode='concept', active=4, pre=[], script=[
            A('√(a + b) ≠ √a + √b appears', T('$\\sqrt{a+b}\\ne\\sqrt a+\\sqrt b$', size=58, gap=50)),
            "The big trap. A root does not split over a plus or a minus.",
            D('Write "√(36 + 64) = √100 = 10, but √36 + √64 = 6 + 8 = 14"'),
            "Root of one hundred is ten. Six plus eight is fourteen. Not equal.",
            A('(√a + √b)² appears', T('$(\\sqrt a+\\sqrt b)^2=a+b+2\\sqrt{ab}$', size=52)),
            "And when you square a sum of roots, don't forget the middle term.",
        ]),
        dict(title='Comparing roots', mode='concept', active=5, pre=[], script=[
            A('7√2 ? 4√6 appears', T('$7\\sqrt2\\ \\ ?\\ \\ 4\\sqrt6\\quad\\to\\quad 98>96$', size=52, gap=50)),
            "Positive numbers? Square both. Bigger square, bigger number. It's the same as bringing the numbers inside the root.",
            "To estimate one root, put it between two perfect squares. Root forty is between six and seven.",
            A('√5 ? ∛11 appears', T('$\\sqrt5\\ \\ ?\\ \\ \\sqrt[3]{11}\\quad\\to\\quad 125>121$', size=52)),
            "A square root and a cube root? Raise both to the sixth power. That clears both roots.",
        ]),
        dict(title='Between 0 and 1', mode='concept', active=6, pre=[], script=[
            A('0 < x < 1: x² < x < √x appears', T('$0<x<1:\\quad x^2<x<\\sqrt x$', size=54, gap=50)),
            "Between zero and one, squaring makes a number smaller. The root makes it bigger.",
            D('Write "x = 1/9:  1/81 < 1/9 < 1/3"'),
            "Not sure? Plug in one ninth. Its square is one eighty-first. Its root is one third.",
            "Above one, it's the other way around.",
        ]),
        dict(title='Conjugates', mode='concept', active=7, pre=[], script=[
            A('(√a + √b)(√a − √b) = a − b appears', T('$(\\sqrt a+\\sqrt b)(\\sqrt a-\\sqrt b)=a-b$', size=52, gap=50)),
            "The partner removes roots. It's the difference of squares.",
            A('1/(√6 − √5) = √6 + √5 appears', T('$\\frac{1}{\\sqrt6-\\sqrt5}=\\sqrt6+\\sqrt5$', size=56)),
            "A root difference on the bottom? Multiply the top and the bottom by the partner.",
            "The bottom becomes six minus five. One. No roots left.",
        ]),
        dict(title='Root equations', mode='concept', active=8, pre=[], script=[
            A('√(x + 12) = x appears', T('$\\sqrt{x+12}=x$', size=58, gap=50)),
            "Square both sides and solve. Then check every answer in the ORIGINAL equation.",
            D('Write "x = 4: √16 = 4 ✓    x = −3: √9 = 3 ≠ −3 ✗"'),
            "Squaring can add a fake solution. Negative three fails: a root is never negative.",
            "x on both sides? Don't divide by x. Move everything to one side and factor.",
            "Or plug in the four choices. A fake solution fails on its own.",
        ]),
        dict(title='Before you practice', mode='concept', active=9, pre=[], script=[
            "Before each question, ask yourself:",
            A('check 1 appears', T('Is there a plus or a minus under the root? It does not split.', size=36, gap=24)),
            A('check 2 appears', T('Is this the largest square I can pull out?', size=36, gap=24)),
            A('check 3 appears', T('Is $x$ negative? Then $\\sqrt{x^2}=-x$, not $x$.', size=36, gap=24)),
            A('check 4 appears', T('Did I check my answer in the original equation?', size=36, gap=24)),
            A('check 5 appears', T('Comparing? Square both, or use the 6th power.', size=36)),
            "The common traps: splitting a root over a plus, forgetting the middle term, and keeping a fake solution.",
            "You know all of this. Now practice.",
        ]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == CORE][-1]
    M.new_video('r26-t09-summary', TOPIC, 'Roots — Summary', sb, slides, CORE, after=last)


def apply(M):
    fix_lesson(M)
    fix_questions(M)
    add_guided(M)
    add_practice(M)
    fix_card(M)
    summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last


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
    # alg-extra-root-practice-2 was the lesson example sqrt72 of "roots" slide 4 -> new numbers.
    M.set_q('alg-extra-root-practice-2', stem=r'$\sqrt{45} = ?$',
            choices=[r'$9\sqrt5$', '$15$', r'$3\sqrt5$', r'$5\sqrt3$'], correct=3,
            expl=[r'Pull out the largest square: $45=9\cdot5$. Therefore, $\sqrt{45}=\sqrt{9}\cdot\sqrt5=3\sqrt5$.'])
    # alg-extra-root-practice-7 was the lesson example sqrt70 of "r26-t09-traps" slide 3 -> new numbers.
    M.set_q('alg-extra-root-practice-7', stem=r'Between which two consecutive whole numbers is $\sqrt{55}$?',
            choices=['$8$ and $9$', '$5$ and $6$', '$7$ and $8$', '$6$ and $7$'], correct=3,
            expl=[r'Put $55$ between two perfect squares: $49<55<64$.',
                  r'Therefore $\sqrt{49}<\sqrt{55}<\sqrt{64}$, that is, $7<\sqrt{55}<8$.'])


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
    # Roots - Exam traps: "Between 0 and 1" is taught in Question 4, "Different roots" (6th power) in Question 5,
    # "Conjugates" in Question 6, comparing by squaring in Question 2. Kept: estimating one root between perfect
    # squares, and the square of a sum of roots (no question video teaches them).
    L = 'r26-t09-traps'
    _cr_titles(M, L, ['Compare by squaring', 'Square of a sum'])
    M.set_slide(L, 1, script=[
        'Now the traps. The exam loves these.',
        'Two short ideas first: estimating a root, and squaring a sum of roots. The other traps come inside the questions.'])
    M.set_slide(L, 2, title='Estimate a root', script=[
        'Comparing two roots? Square both — like in the earlier question. It works because both numbers are positive: bigger square, bigger number.']
        + _cr_script(M, L, 2)[_cr_find(_cr_script(M, L, 2), r'$\sqrt{70}$', L, 2):])
    M.video(L)['hybrid']['sidebar'][0] = 'Estimate a root'
    # moved into Question 4: the rule on the board, and "above one it's the other way around"
    Q4 = 'solve-q-r26-t09-04'
    _cr_drop(M, Q4, 2, ['And the rule: between zero and one'])
    _cr_slide_after(M, Q4, 2, 'The rule', [
        A('0 < x < 1: x² < x < √x appears', T(r'$0<x<1:\quad x^2<x<\sqrt x$', 44)),
        'The rule: between zero and one, powers make it smaller, and the root makes it bigger.',
        A('x > 1: √x < x < x² appears', T(r'$x>1:\quad \sqrt x<x<x^2$', 44)),
        "Above one, it's the other way around: root nine is three — smaller than nine."])


_apply_before_cut_repeats = apply


def apply(M):
    _apply_before_cut_repeats(M)
    cut_repeats(M)   # 2026-10-05: runs last
