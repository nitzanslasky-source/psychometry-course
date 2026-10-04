"""Topic 13 - Absolute Value. Course review 2026-09 fixes.
See t13_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q
from math_api import VIS

TOPIC = 13
LESSON = 'absolute-value'
TOOLS = 'r26-t13-tools'
SEC1 = 'absolute-value-theory'
SEC2 = 'absolute-value-advanced'
PRACT = 'unit-t13-3'


def qid(n): return 'q-r26-t13-%02d' % n


# Guided-question numbers BEFORE renumbering (renumber_guided() in math_api puts them in course order).
# New solution videos get 14, 15, 16 in the order they are created below.
# (Pass 2: guided q-r26-t13-04 'from a range to bars' was removed.)
SB1 = ['Question %d' % n for n in (1, 2, 3, 4, 5, 14, 15)]
# 2026-10-01: the sign-reading guided question (created last, so number 17) sits right after Q9 (q-366).
SB2 = ['Question %d' % n for n in (6, 7, 8, 9, 17, 16, 10, 11, 12, 13)]

# number line: |x - 2| < 4  ->  within 4 of 2
NL_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 150" role="img" aria-label="Number line: the numbers less than 4 away from 2">'
          '<title>Within 4 of 2</title>'
          '<line x1="30" y1="95" x2="610" y2="95" stroke="#203344" stroke-width="2.5"/>'
          '<path d="M 612 95 l -10 -6 l 0 12 Z M 28 95 l 10 -6 l 0 12 Z" fill="#203344"/>'
          '<rect x="140" y="88" width="360" height="14" fill="#d5f1ed" stroke="#087f83" stroke-width="2"/>'
          + ''.join('<line x1="%d" y1="89" x2="%d" y2="101" stroke="#203344" stroke-width="2"/>'
                    '<text x="%d" y="128" text-anchor="middle" fill="#203344" font-family="DejaVu Sans,Arial,sans-serif" font-size="18"%s>%s</text>'
                    % (50 + (n + 4) * 45, 50 + (n + 4) * 45, 50 + (n + 4) * 45,
                       ' font-weight="bold"' if n in (-2, 2, 6) else '', ('−%d' % -n) if n < 0 else str(n)) for n in range(-4, 9))
          + '<circle cx="140" cy="95" r="6" fill="#ffffff" stroke="#087f83" stroke-width="2.5"/>'
          '<circle cx="500" cy="95" r="6" fill="#ffffff" stroke="#087f83" stroke-width="2.5"/>'
          '<circle cx="320" cy="95" r="6" fill="#203344"/>'
          '<line x1="320" y1="55" x2="496" y2="55" stroke="#087f83" stroke-width="2.5"/><path d="M 500 55 l -12 -6 l 0 12 Z" fill="#087f83"/>'
          '<text x="410" y="42" text-anchor="middle" fill="#087f83" font-family="DejaVu Sans,Arial,sans-serif" font-size="20" font-weight="bold">4</text>'
          '<line x1="320" y1="55" x2="144" y2="55" stroke="#087f83" stroke-width="2.5"/><path d="M 140 55 l 12 -6 l 0 12 Z" fill="#087f83"/>'
          '<text x="230" y="42" text-anchor="middle" fill="#087f83" font-family="DejaVu Sans,Arial,sans-serif" font-size="20" font-weight="bold">4</text>'
          '<line x1="320" y1="55" x2="320" y2="89" stroke="#203344" stroke-width="1.5" stroke-dasharray="4 4"/>'
          '</svg>')


# ------------------------------------------------------------------ helpers
def _lines(M, vid, n, fn):
    M.edit_lines(vid, n, fn)


def _replace(M, vid, n, old, new, key=None):
    """Replace the whole text of the first say/draw line that contains `old`."""
    def fn(ls):
        for l in ls:
            for k in ([key] if key else ['say', 'draw']):
                if k in l and old in l[k]:
                    l[k] = new if new is not None else l[k]
                    return ls
        raise KeyError('%s #%d: %r not found' % (vid, n, old))
    _lines(M, vid, n, fn)


def _insert_after(M, vid, n, old, new_lines):
    """Insert line dicts after the first line whose text contains `old`."""
    def fn(ls):
        for k, l in enumerate(ls):
            if old in (l.get('say') or l.get('draw') or ''):
                return ls[:k + 1] + new_lines + ls[k + 1:]
        raise KeyError('%s #%d: %r not found' % (vid, n, old))
    _lines(M, vid, n, fn)


def _drop(M, vid, n, old):
    _lines(M, vid, n, lambda ls: [l for l in ls if old not in (l.get('say') or l.get('draw') or '')])


def _solution(M, qid_, group, sidebar, num, intro, slides, after=None):
    n = M.next_question_number(TOPIC)
    active = sidebar.index('Question %d' % n)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=active, title=title, pre=[Q(qid_)], script=script))
    v = M.new_video('solve-' + qid_, TOPIC, group, sidebar, beats, M.section_of(qid_), kind='solution', qid=qid_, after=after)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = num
    v['title'] = v['navLabel'] = M.q(qid_)['stem']
    return n


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Main lesson video - fix wrong / risky teaching, add sign tools and negative right side
    #    (edit existing slides first, then insert new ones from the bottom up)
    # =====================================================================================
    _replace(M, LESSON, 2, 'kilometres',
             "And a distance can't be negative. The way to my friend's house isn't minus three kilometers. It's three kilometers.")

    # slide 3: "the minus just drops off" - only for numbers; warning for letters
    M.set_slide(LESSON, 3, script=[
        "So what do the bars do?",
        A('|6| = 6 appears', T('$|6|=6$', size=52)),
        "A positive number stays exactly the same. Six is six units from zero.",
        A('|−9| = 9 appears', T('$|-9|=9$', size=52)),
        "A negative number becomes the same number — positive. Negative nine is nine units away.",
        D('Circle the minus sign in −9 and cross it out'),
        "With a plain number? The minus just drops off.",
        A('|0| = 0 appears', T('$|0|=0$', size=52)),
        "And zero? Zero isn't far from zero at all. It's right there. The absolute value of zero is zero.",
        A("'Letters: careful!' appears", T('Letters: if $x=-3$, then $-x=3$ and $|x|=3\\ne x$', size=42)),
        "But careful with LETTERS. A letter hides its sign.",
        "If x is negative three, then minus x is plus three. And the absolute value of x is three — not x.",
        "So with letters, the minus does NOT just drop off. First ask: is the letter positive or negative?",
    ])

    # slide 5: rule two also for a fraction; American spelling
    M.set_slide(LESSON, 5, script=[
        "Three rules.",
        A('Rule 1 appears: |x| ≥ 0', T('$|x|\\ge 0$', size=54)),
        D('Box the ≥ 0'),
        "Rule one — the most important one, it's really the definition. An absolute value is never negative.",
        "It can be zero. It can be positive. See bars — think: zero or positive.",
        A('Rule 2 appears: |a · b| = |a| · |b| and |a/b| = |a|/|b|',
          T('$|a\\cdot b|=|a|\\cdot|b| \\qquad \\left|\\frac{a}{b}\\right|=\\frac{|a|}{|b|}$', size=54)),
        "Rule two: for a product, you can take the bars on the whole thing or on each factor. Same result.",
        "The same is true for a fraction: bars on the top, bars on the bottom.",
        A('Rule 3 appears: |a + b| ≤ |a| + |b|', T('$|a+b|\\le|a|+|b|$', size=54)),
        "Rule three is for a sum. Keep it in mind — in the advanced part it becomes a tool for reading signs.",
    ])

    # slide 7: sign clues - add |x| = -x -> x <= 0 (zero works too)
    M.set_slide(LESSON, 7, script=[
        "Now the understanding questions. These come up again and again on the exam.",
        "Compare a number with its own absolute value — and you instantly know its sign.",
        A('Clue 1 appears: |x| > x → x < 0', T('$|x|>x \\;\\to\\;$ $x<0$', size=46)),
        "The absolute value is bigger than the number? Then the number is negative. The absolute value of negative five is five — bigger.",
        A('Clue 2 appears: |x| = x → x ≥ 0', T('$|x|=x \\;\\to\\;$ $x\\ge0$ (zero or positive)', size=46)),
        "They're equal? The number is positive — or zero. Don't forget the zero.",
        A('Clue 3 appears: |x| = −x → x ≤ 0', T('$|x|=-x \\;\\to\\;$ $x\\le0$ (zero or negative)', size=46)),
        "The absolute value equals MINUS the number? Then the number is negative — or zero. Minus zero is zero, so zero works too.",
        D('Circle the "≤" in clue 3'),
        "On the exam the right choice is \"x is less than or equal to zero\" — not \"x is less than zero\". The zero is the trap.",
        A('Clue 4 appears: x > |x| → impossible', T('$x>|x| \\;\\to\\;$ impossible', size=46)),
        D('Draw a big ✗ next to the fourth clue'),
        "The number bigger than its absolute value? Can't happen. A positive number would be equal, and a negative one is smaller.",
        "Behind all of them: for a negative x, the absolute value is minus x — and minus x is positive.",
    ])

    # slide 9: inequalities - explain with the board example, not with a number that isn't there
    _replace(M, LESSON, 9, 'Take the absolute value of x bigger than five',
             "Why? Look at the first one. The inside, x minus two, must be MORE than four away from zero: "
             "four and a half, five, six… or negative four and a half, negative five, negative six…")
    _replace(M, LESSON, 9, 'The absolute value on the SMALL side?',
             "The absolute value on the SMALL side? Then the inside must stay LESS than four away from zero: "
             "three and a half, two, zero, negative two, negative three and a half… The range is CLOSED — trapped in the middle.")

    # slide 10: plug in - which numbers to avoid
    M.set_slide(LESSON, 10, script=[
        "And like almost every topic — some absolute value questions fall to trial and error.",
        A("'An expression = ? → plug in a number' appears", T('An expression $=\\ ?$ $\\;\\to\\;$ plug in a number', size=46)),
        "When they ask what an expression equals — you're allowed to plug in a number that fits the conditions.",
        A("'Avoid 0, 1, −1 and numbers in the choices' appears", T('Avoid $0$, $1$, $-1$ and numbers from the choices', size=44)),
        "Which number? Not a special one. Zero, one and minus one make many expressions look the same.",
        "Numbers that appear in the choices can fool you too.",
        A("'Eliminate three choices' appears", T('Eliminate three choices — then mark the fourth.', size=46)),
        D('Underline "three"'),
        "Same rule as always: you're done only when three choices are gone.",
        "Two choices still survive? Plug in a second number.",
    ])

    # slide 11: recap
    M.set_slide(LESSON, 11, script=[
        "Let's lock it in.",
        A("'|x| = distance from 0 → never negative' appears", T('$|x|$ = distance from $0$ $\\;\\to\\;$ never negative', size=42)),
        A("'Sign clues' appears", T('$|x|>x\\to x<0$ · $|x|=x\\to x\\ge0$ · $|x|=-x\\to x\\le0$', size=40)),
        A("'Equation → two cases' appears", T('Equation $\\to$ two cases: $+$ and $-$', size=42)),
        A("'Small side → between · Big side → outside' appears", T('Small side $\\to$ between · Big side $\\to$ outside', size=42)),
        A("'Negative right side? Look before you solve' appears", T('Negative right side? Look before you solve.', size=42)),
        D('Circle "two cases"'),
        "Absolute value can appear in an expression, an equation or an inequality. Inequalities are the hardest — and the rarest.",
        "Not sure about them yet? Rewind and watch that part again.",
        "Seven questions next — each one before its own video.",
    ])

    # new slide after 9: negative (or zero) right side in an inequality
    M.insert_slides(LESSON, 9, [dict(mode='concept', active=8, title='Negative right side', script=[
        "One more trap: a negative number on the right side of an inequality.",
        A('|x + 1| < −3 appears', T('$|x+1|<-3$ $\\;\\to\\;$ no solution', size=48)),
        "Bars are never negative. Can they be less than negative three? Never. No solution.",
        A('|x + 1| > −3 appears', T('$|x+1|>-3$ $\\;\\to\\;$ every $x$', size=48)),
        "Now flip it. Bars bigger than negative three? Always. Zero or positive is always bigger than a negative number. Every x works.",
        A('|x + 1| ≤ 0 appears', T('$|x+1|\\le0$ $\\;\\to\\;$ $x=-1$', size=48)),
        "And zero on the right. Bars at most zero? Bars can't go below zero — so they must BE zero.",
        D('Write "x + 1 = 0 → x = −1"'),
        "The inside is zero: x is negative one. One solution.",
        "Before any algebra, look at the right side. Sometimes it answers the question for you.",
    ])])

    # new slide after 7: signs of a product, x/|x|
    M.insert_slides(LESSON, 7, [dict(mode='concept', active=5, title='Signs of a product', script=[
        "Two more sign tools. You'll need them in the first question.",
        A('a · b > 0 → same signs appears', T('$a\\cdot b>0 \\;\\to\\;$ same signs', size=48)),
        "A product is positive? The two numbers have the same sign. Plus times plus, or minus times minus.",
        A('a · b < 0 → opposite signs appears', T('$a\\cdot b<0 \\;\\to\\;$ opposite signs', size=48)),
        "A product is negative? Opposite signs: one positive, one negative.",
        A('x/|x| = 1 or −1 appears', T('$\\frac{x}{|x|}=1$ if $x>0$ $\\qquad \\frac{x}{|x|}=-1$ if $x<0$', size=48)),
        "And a number divided by its own absolute value? Same size — only the sign is left.",
        D('Write "x = 5: 5 ÷ 5 = 1     x = −5: −5 ÷ 5 = −1"'),
        "Positive: one. Negative: minus one. And x can't be zero — you can't divide by zero.",
    ])])

    M.set_sidebar(LESSON, ['Distance from zero', 'Plus or minus inside', 'Whole expression', 'The rules', 'Sign clues',
                           'Signs of a product', 'Equations', 'Inequalities', 'Negative right side', 'Plug in', 'Recap'])
    # slides now: 1 title, 2-4 (0-2), 5-6 rules (3), 7 clues (4), 8 product (5), 9 equations, 10 inequalities,
    # 11 negative right side (8), 12 plug in, 13 recap
    for n, a in ((9, 6), (10, 7), (12, 9), (13, 10)):
        M.slide(LESSON, n)['active'] = a

    # =====================================================================================
    # 2. Memory card - sign clue x <= 0, new rules, new tools
    # =====================================================================================
    card = M.card('mem-absolute-value')
    card['tables'] = [
        {'title': 'Rules', 'head': ['Rule', 'Meaning'], 'rows': [
            ['$|x|\\ge0$', 'Zero or positive — never negative'],
            ['$|x|=x$ if $x\\ge0$ · $|x|=-x$ if $x<0$', 'For a negative $x$, $-x$ is positive. With letters the minus does not just drop off.'],
            ['$|a\\cdot b|=|a|\\cdot|b|$ · $\\left|\\frac{a}{b}\\right|=\\frac{|a|}{|b|}$', 'Bars on a product or a fraction can go on each part'],
            ['$|a+b|\\le|a|+|b|$', 'Equal for same signs, smaller for different signs'],
            ['$|a-b|=|b-a|$', 'Opposite numbers have the same absolute value'],
            ['$|x|^2=x^2$ · $\\sqrt{x^2}=|x|$', 'Bars and an even power both remove the sign'],
        ]},
        {'title': 'Sign clues', 'head': ['If…', 'then…'], 'rows': [
            ['$|x|>x$', '$x<0$'],
            ['$|x|=x$', '$x\\ge0$ (zero or positive)'],
            ['$|x|=-x$', '$x\\le0$ (zero or negative)'],
            ['$x>|x|$', 'impossible'],
            ['$a\\cdot b>0$ · $a\\cdot b<0$', 'same signs · opposite signs'],
            ['$\\frac{x}{|x|}$', '$1$ if $x>0$, $-1$ if $x<0$'],
        ]},
        {'title': 'Solving', 'head': ['Form', 'Solution'], 'rows': [
            ['$|x+3|=8$', '$x+3=8$ or $x+3=-8$'],
            ['$|x-2|<4$ (small side)', '$-4<x-2<4$ → between: $-2<x<6$'],
            ['$|x-2|>4$ (big side)', '$x-2>4$ or $x-2<-4$ → outside: $x>6$ or $x<-2$'],
            ['$|x+1|<-3$ · $|x+1|>-3$ · $|x+1|\\le0$', 'no solution · every $x$ · only $x=-1$'],
            ['$|x-6|=2x$ (letter on the right)', 'solve both cases, then check each answer: only $x=2$'],
            ['$|x-1|=|x+3|$ (bars on both sides)', 'both sides $\\ge0$, so square both sides'],
        ]},
        {'title': 'Distance tools', 'head': ['Form', 'Meaning'], 'rows': [
            ['$|x-a|$', 'the distance between $x$ and $a$ ($|x+5|$: distance from $-5$)'],
            ['$|x-a|<r$', '$x$ is less than $r$ from $a$: $a-r<x<a+r$'],
        ]},
    ]
    card['tips'] = [
        'Expression inside the bars? Calculate the whole inside first.',
        'Right side negative or zero? Look before you solve.',
        'Letter on the right side? Check every answer in the original equation.',
        'Plug in? Avoid $0$, $1$, $-1$ and numbers from the choices. Two choices left? Plug in again.',
    ]

    # =====================================================================================
    # 3. New lesson video at the start of the advanced section: exam tools
    # =====================================================================================
    M.new_video(TOOLS, TOPIC, 'Absolute Value — Exam Tools',
                ['Squares and bars', 'Square both sides', 'Letter on the right', 'Distance', 'Recap'], [
        dict(mode='title', title='Absolute Value — Exam Tools', script=[
            "Four tools for the harder absolute-value questions.",
            "Each one saves time on the exam.",
        ]),
        dict(mode='concept', active=0, title='Squares and bars', script=[
            "First: a square doesn't care about the sign. Neither do bars.",
            A('|x|² = x² appears', T('$|x|^2=x^2$', size=56, gap=70)),
            D('Write "x = −3: |−3|² = 9, (−3)² = 9"'),
            "Negative three: bars give three, and three squared is nine. Negative three squared — also nine.",
            A('√(x²) = |x| appears', T('$\\sqrt{x^2}=|x|$', size=56, gap=70)),
            "The other way around: the root of x squared is the absolute value of x. Not x.",
            D('Write "x = −3: √9 = 3 = |−3|"'),
            "x is negative three: root nine is three. That's the absolute value, not x itself.",
            A('|a − b| = |b − a| appears', T('$|a-b|=|b-a|$', size=56, gap=70)),
            "And a minus b, b minus a — opposite numbers. Same distance from zero.",
            D('Write "|2 − 7| = 5 = |7 − 2|"'),
        ]),
        dict(mode='concept', active=1, title='Square both sides', script=[
            "This gives a tool for bars on both sides.",
            A('|x − 1| = |x + 3| appears', T('$|x-1|=|x+3|$', size=58, gap=300)),
            "Both sides are zero or positive. So you may square both sides — the bars disappear.",
            D('Write "(x − 1)² = (x + 3)²"'),
            D('Write "x² − 2x + 1 = x² + 6x + 9"'),
            "Open both with the shortcut formulas. x squared cancels.",
            D('Write "−8x = 8 → x = −1"'),
            "Minus eight x equals eight. x is negative one.",
            D('Write "check: |−2| = 2 = |2| ✓"'),
            "Check: negative two in bars, two in bars. Equal.",
            A("'Both sides ≥ 0 → you may square' appears", T('Both sides $\\ge0$ $\\;\\to\\;$ you may square', size=46)),
            "Remember why it's allowed: both sides are never negative.",
        ]),
        dict(mode='concept', active=2, title='Letter on the right', script=[
            "Now a letter on the right side.",
            A('|x − 6| = 2x appears', T('$|x-6|=2x$', size=58, gap=380)),
            "Careful. Bars can't give a negative, so the right side can't be negative either.",
            D('Under it write "2x ≥ 0 → x ≥ 0"'),
            "Solve the two cases as usual.",
            D('Write "x − 6 = 2x → x = −6"'),
            "First case: x minus six equals two x. x is negative six.",
            D('Write "x − 6 = −2x → 3x = 6 → x = 2"'),
            "Second case: x minus six equals minus two x. Three x is six. x is two.",
            "Now check each answer in the ORIGINAL equation.",
            D('Write "x = −6: |−12| = 12, but 2x = −12 ✗"'),
            "Negative six: the left side is twelve, the right side is negative twelve. Fake. Throw it out. And we knew — x can't be negative.",
            D('Write "x = 2: |−4| = 4 = 2 · 2 ✓"'),
            "Two: four on the left, four on the right. It works. Only x equals two.",
            A("'Letter on the right? Check your answers.' appears", T('Letter on the right? Check your answers.', size=46)),
            "So: a letter on the right side? Check every answer. The trap choice keeps both.",
        ]),
        dict(mode='concept', active=3, title='Distance', script=[
            "Absolute value is distance from zero. Now: distance from ANY number.",
            A('|x − a| = distance between x and a appears', T('$|x-a|$ = the distance between $x$ and $a$', size=46, gap=80)),
            D('Write "|7 − 2| = 5: from 2 to 7 is 5 steps"'),
            "Seven minus two in bars: five. From two to seven is five steps.",
            A('Number line: within 4 of 2 appears', VIS(NL_SVG, w=1000, h=250, gap=80)),
            "So the absolute value of x minus two, less than four, reads: x is less than four steps from two.",
            "Start at two. Four steps left: negative two. Four steps right: six.",
            D('Write "|x − 2| < 4 → −2 < x < 6"'),
            "x is between negative two and six. The same answer as the algebra — in one step.",
            "More than four? Then x is farther than four steps: below negative two, or above six.",
            A('|x + 5| = distance from −5 appears', T('Plus inside: $|x+5|=|x-(-5)|$ $\\to$ distance from $-5$', size=42)),
            "Careful with a plus inside. x plus five is x minus negative five. So it's the distance from NEGATIVE five.",
        ]),
        dict(mode='concept', active=4, title='Recap', script=[
            "Let's lock it in.",
            A("'|x|² = x², √(x²) = |x|' appears", T('$|x|^2=x^2$ · $\\sqrt{x^2}=|x|$ · $|a-b|=|b-a|$', size=42)),
            A("'Bars on both sides → square' appears", T('Bars on both sides $\\to$ square both sides', size=42)),
            A("'Letter on the right → check' appears", T('Letter on the right $\\to$ check every answer', size=42)),
            A("'|x − a| = distance' appears", T('$|x-a|$ = distance between $x$ and $a$', size=42)),
            "Next: a card with the question wordings. Then the advanced questions.",
        ]),
    ], SEC2, before='q-363')

    # wordings card (must / could / cannot from topic 1, plus the exam's "not necessarily" forms)
    M.new_card('mem-r26-t13-wordings', TOPIC, SEC2, dict(
        title='Question wordings',
        intro='Circle the question word before you read the choices. You met must, could and cannot in topic 1.',
        tables=[dict(title='', head=['The question asks…', 'The right choice is…', 'How to find it'], rows=[
            ['necessarily true (must be true)', 'true for every allowed value', 'break each wrong choice with one example'],
            ['could be true (possible)', 'true for at least one allowed value', 'find one example that works'],
            ['cannot be true', 'true for no allowed value', 'examples that work knock out the wrong choices'],
            ['not necessarily true', 'false for at least one allowed value', 'find one example where it fails'],
            ['possible but not necessarily true', 'sometimes true, sometimes false', 'throw out the "always" and the "never" choices'],
        ])],
        tips=['A choice that is never true is also "not necessarily true".',
              'Test only allowed numbers. With absolute value, always try $0$ and a negative number.']),
        after=TOOLS)

    # =====================================================================================
    # 4. Existing solution videos
    # =====================================================================================
    for q in ('q-358', 'q-359', 'q-360', 'q-361', 'q-362'):
        M.set_sidebar('solve-' + q, SB1)
    for q in ('q-363', 'q-364', 'q-365', 'q-366', 'q-367', 'q-368', 'q-369', 'q-370'):
        M.set_sidebar('solve-' + q, SB2)
        v = M.video('solve-' + q)
        for b in v['beats']:
            if b['active'] >= 0:
                b['active'] = SB2.index('Question %d' % (int(v['beats'][0]['bigTitle'].split()[1])))

    # Q1: the sign clues, now with |x| = -x -> x <= 0
    M.set_slide('solve-q-358', 3, title='The sign clues', script=[
        "Notice what cracked it: comparing a number with its absolute value.",
        A('Clues 1 and 2 appear', T('$|x|>x \\to$ negative $\\quad$ $|x|=x \\to$ zero or positive', size=40)),
        A('Clues 3 and 4 appear', T('$|x|=-x \\to$ zero or negative $\\quad$ $x>|x| \\to$ impossible', size=40)),
        D("Put a star next to clue 1 — that's the one in this question"),
        "Bigger absolute value — negative. Equal — zero or positive. Equal to minus the number — zero or negative. The number bigger — that can't happen.",
        "This comes up on the exam again and again. The moment you see it, it tells you the sign.",
    ])

    # Q3, Q4: the distance picture as a second look
    _insert_after(M, 'solve-q-360', 2, 'seven is less than eight', [
        {'say': "Another way to see it — a distance picture. x plus five is x minus negative five."},
        {'draw': 'Draw a number line: a dot at −5, arrows of 8 to −13 and to 3'},
        {'say': "So x is less than eight steps from negative five. Eight steps left: negative thirteen. Eight steps right: three."},
    ])
    _insert_after(M, 'solve-q-361', 2, 'five is not bigger than six', [
        {'say': "The distance picture says the same. x plus three: the distance from negative three."},
        {'draw': 'Draw a number line: a dot at −3, marks at −9 and 3, shade outside them'},
        {'say': "More than six steps from negative three: beyond three, or below negative nine. Two is only five steps away."},
    ])

    # Q5: second plug-in avoids -1; add x/|x| = -1
    _replace(M, 'solve-q-362', 2, 'Take x equals negative three. Why negative three?',
             "Take x equals negative three. Any negative number works — just not zero, one or minus one.")
    _replace(M, 'solve-q-362', 2, 'x = −1: 5 + (−2)/1 = 3', 'Write "x = −2: 5 + (−4)/2 = 3"')
    _replace(M, 'solve-q-362', 2, 'x equals negative one: five plus negative two over one',
             "x equals negative two: five plus negative four over two. Three again.")
    _replace(M, 'solve-q-362', 2, '−x = 1 ✗', 'Next to choice 3 write "−x = 2 ✗" and circle choice 2')
    _replace(M, 'solve-q-362', 2, 'But negative x is now one', "But negative x is now two. Out. Choice two.")
    _insert_after(M, 'solve-q-362', 3, 'Two x over negative x', [
        {'say': "That's the tool from the lesson: x over its absolute value is minus one for every negative x."},
    ])

    _replace(M, 'solve-q-362', 1, 'Last question.', "Question five.")

    # Q9: the wording, and the broken chain on the board
    _replace(M, 'solve-q-366', 1, 'the wording is new',
             "Unlike the last ones, this is a TECHNIQUE question. And look at the wording — it's the last row of the wordings card.")
    _replace(M, 'solve-q-366', 2, 'POSSIBLE, but NOT NECESSARILY correct',
             "Read the question carefully: POSSIBLE, but NOT NECESSARILY true.")
    _replace(M, 'solve-q-366', 2, '|a+b|² > 4 = (a+b)² > 4', 'Next to choice 1 write "|a+b| > 2 → |a+b|² > 4"')
    _replace(M, 'solve-q-366', 2, 'The technical way: square both sides',
             "The technical way: both sides are positive, so square both sides. Two squared is four.")
    _insert_after(M, 'solve-q-366', 2, 'The technical way', [
        {'draw': 'Below it write "|a+b|² = (a+b)²  →  (a+b)² > 4"'},
        {'say': "And the absolute value of a plus b, squared, is the same as a plus b squared. A square doesn't care about the sign."},
    ])

    # Q10: check that the right side 6 + x is not negative
    _insert_after(M, 'solve-q-367', 2, 'Two x is negative six', [
        {'say': "A letter on the right side — so check it. Six plus negative three is three. Not negative. It works."},
    ])

    # Q11: squaring both sides is a lesson tool
    _replace(M, 'solve-q-368', 3, 'Some students get rid of the bars',
             "The tool from the lesson: both sides are zero or positive, so we may square both sides. After squaring, the bars are gone.")

    # Q12: the "bait" sentence was wrong (6 < x < 7 comes from ADDING 1)
    _replace(M, 'solve-q-369', 2, 'Six to seven is the bait',
             "Six to seven is the bait. That's what you get if you ADD the one instead of subtracting it.")

    # Q8: American spelling
    M.slide('solve-q-365', 2)['title'] = 'Method 1 · Analyze the givens'

    # "— so" / ", so" meaning "therefore" in the middle of a sentence
    for vid, v in M.D['videos'].items():
        if v['topic'] != TOPIC: continue
        ch = False
        for b in v['beats']:
            for l in b['lines']:
                if 'say' in l and re.search(r'(—|,) so ', l['say']):
                    l['say'] = re.sub(r'\s*(—|,) so ', '. So ', l['say']); ch = True
        if ch: M.touched_videos.add(vid)

    # =====================================================================================
    # 5. Existing questions: TeX, stacked conditions, no colons, worked solutions
    # =====================================================================================
    S('q-358', stem='Given:\n$\\begin{cases} a\\cdot b<0 \\\\ a<|a| \\end{cases}$\nWhich of the following is necessarily true?', expl=[
        '$a<|a|$: a number is smaller than its absolute value only when it is negative. So $a<0$.',
        '$a\\cdot b<0$: the product is negative, so $a$ and $b$ have opposite signs. $a$ is negative, so $b>0$.',
        '$b$ is positive, so $|b|=b$ (choice 2). Choice 3 ($b<0$) is false.',
        'Choices 1 and 4 compare sizes, and the givens say nothing about sizes. $a=-2$, $b=7$: $|b|=7$ is bigger than $|a|=2$, so choice 1 fails. '
        '$a=-4$, $b=1$: $\\left|\\frac{a}{b}\\right|=4$, not less than $1$, so choice 4 fails.'])
    S('q-359', stem='Given: $|x+3|=8$. Which of the following could be the value of $x$?', expl=[
        'Two cases. $x+3=8$, so $x=5$. Or $x+3=-8$, so $x=-11$.',
        'Only $-11$ is among the choices. Check: $|-11+3|=|-8|=8$ ✓.',
        'Choice 3 ($-5$) is a trap: it is not $5$.'])
    S('q-360', stem='Given: $|x+5|<8$. Which of the following could be the value of $x$?', expl=[
        'The bars are on the small side, so $x+5$ is between $-8$ and $8$: $-8<x+5<8$.',
        'Subtract $5$ from all three parts: $-13<x<3$.',
        'Only $2$ is in this range ($4$ and $10$ are too big, and $-30$ is too small). Check: $|2+5|=7<8$ ✓.',
        'With the distance picture: $|x+5|=|x-(-5)|$ is the distance from $x$ to $-5$. Less than $8$ from $-5$ means from $-13$ to $3$.'])
    S('q-361', stem='Given: $6<|x+3|$. Which of the following cannot be the value of $x$?', expl=[
        'The bars are on the big side, so there are two cases. $x+3>6$, so $x>3$. Or $x+3<-6$, so $x<-9$.',
        '$6$ and $8$ are greater than $3$ ✓, and $-10$ is less than $-9$ ✓.',
        '$2$ is in neither range: $|2+3|=5$, and $5$ is not greater than $6$. So $x$ cannot be $2$.'])
    S('q-362', stem='Given: $x<0$. What is $5+\\frac{2x}{|x|}$?', expl=[
        '$x<0$, so $|x|=-x$.',
        '$\\frac{2x}{|x|}=\\frac{2x}{-x}=-2$ for every negative $x$.',
        'So $5+\\frac{2x}{|x|}=5-2=3$.',
        'Plugging in: $x=-2$ gives $5+\\frac{-4}{2}=3$. The choices at $x=-2$: $7$, $3$, $-x=2$ and $5-x=7$. Only choice 2 gives $3$.'])
    S('q-363', stem='Given:\n$\\begin{cases} |b|=a \\\\ b\\ne a \\\\ 3c=a \\end{cases}$\nWhich of the following is necessarily true?', expl=[
        '$|b|=a$, so $b=a$ or $b=-a$. Since $b\\ne a$, $b=-a$.',
        '$a=|b|\\ge0$. If $a=0$, then $b=0=a$, which is not allowed. So $a>0$ and $b=-a<0$.',
        '$c=\\frac{a}{3}$: positive, but smaller than $a$. So $0<c<a$.',
        'The order is $b<c<a$. With numbers: $a=3$, $b=-3$, $c=1$.'])
    S('q-364', stem='Given: $p<q<0<r<s$. Which of the following is necessarily true?', expl=[
        '$|x|$ is the distance from $0$. $p$ and $q$ are both negative, and $p$ is farther left. So $p$ is farther from $0$: $|q|<|p|$ always.',
        'The other choices compare a negative number with a positive one, and the givens say nothing about that.',
        '$p=-100$, $q=-50$, $r=1$, $s=2$: choices 1 and 2 fail. $p=-2$, $q=-1$, $r=5$, $s=6$: choice 3 fails.'])
    S('q-365', stem='Given:\n$\\begin{cases} d<c<b \\\\ |b|<|c| \\end{cases}$\nWhich of the following is not necessarily true?', expl=[
        '$c<b$, but $|c|>|b|$. If $c$ were $0$ or positive, then $b>c\\ge0$ and $|b|>|c|$. So $c<0$.',
        '$d<c<0$, so $d$ is negative too and farther from $0$: $|d|>|c|>|b|$. Choices 2, 3 and 4 are always true.',
        'The sign of $b$ is not fixed. $c=-2$, $d=-3$, $b=1$: all the givens hold, and $b=|b|$. So choice 1 ($b\\ne|b|$) is not necessarily true.'])
    S('q-366', stem='$a$ and $b$ are integers. Given: $2<|a+b|$. Which of the following is possible but not necessarily true?', expl=[
        'Choice 1 is always true. Both sides of $2<|a+b|$ are positive, so we may square: $4<|a+b|^2=(a+b)^2$.',
        'Choice 2 is never true: $|a\\cdot b|=|a|\\cdot|b|$ always, so it is never smaller.',
        'Choice 3 is always true: $|3a+3b|=3|a+b|$, and $|a+b|<3|a+b|$ because $|a+b|>0$.',
        'Choice 4 is sometimes true. $a=5$, $b=-2$ gives $3<7$ ✓. But $a=2$, $b=1$ gives $3=3$, not "less than". So it is possible but not necessarily true.'])
    S('q-367', stem='Given:\n$\\begin{cases} 3|x|+6|y|=27 \\\\ x+2|y|=3 \\end{cases}$\nWhat is $x$?', expl=[
        'Divide the first equation by $3$: $|x|+2|y|=9$.',
        'Subtract the second equation: $|x|-x=9-3=6$, so $|x|=6+x$.',
        'Case $x=6+x$: $0=6$, impossible. Case $x=-(6+x)$: $2x=-6$, so $x=-3$.',
        'Check: $|-3|=3=6+(-3)$ ✓. Then $2|y|=3-(-3)=6$, so $|y|=3$, and $3\\cdot3+6\\cdot3=27$ ✓.'])
    S('q-368', stem='Given: $|x+3y|=|3x+y|$. Which of the following is necessarily true?', expl=[
        'Equal absolute values: the insides are equal or opposite.',
        'Equal: $x+3y=3x+y$, so $2y=2x$ and $x=y$.',
        'Opposite: $x+3y=-(3x+y)$, so $4x+4y=0$ and $x=-y$.',
        'In both cases $|x|=|y|$. But $x=y$ is not necessary: $x=1$, $y=-1$ gives $|-2|=|2|$ ✓ with $x\\ne y$.'])
    S('q-369', stem='Given: $11<|2x+1|<13$. Which of the following ranges is possible for $x$?', expl=[
        'Positive inside: $11<2x+1<13$. Subtract $1$: $10<2x<12$. Divide by $2$: $5<x<6$.',
        'Negative inside: $-13<2x+1<-11$. Subtract $1$: $-14<2x<-12$. Divide by $2$: $-7<x<-6$.',
        'Only $-7<x<-6$ is among the choices. Check $x=-6.5$: $|2\\cdot(-6.5)+1|=|-12|=12$ ✓.',
        'Choice 1 ($6<x<7$) is what you get if you add $1$ instead of subtracting it.'])
    S('q-370', stem='Given: $x+|x|<14$. What is the most precise domain for $x$?', expl=[
        'Case $x\\ge0$: $|x|=x$, so $2x<14$ and $x<7$. This gives $0\\le x<7$.',
        'Case $x<0$: $|x|=-x$, so $x+|x|=x-x=0$, and $0<14$ is always true. Every negative $x$ works.',
        'Together: $x<7$.'])
    S('q-371', stem='Given:\n$\\begin{cases} d\\ne0 \\\\ |c+d|=|c-d| \\end{cases}$\nWhat is $c$?', expl=[
        'Equal absolute values: the insides are equal or opposite.',
        'Equal: $c+d=c-d$, so $2d=0$ and $d=0$. Not allowed, because $d\\ne0$.',
        'Opposite: $c+d=-(c-d)=-c+d$, so $2c=0$ and $c=0$.',
        'Check with $d=5$: $|0+5|=|0-5|=5$ ✓.'])
    S('q-372', stem='Given: $|x+2|<|x-2|$. Which of the following numbers satisfies the inequality?', expl=[
        '$|x+2|=|x-(-2)|$ is the distance from $x$ to $-2$. $|x-2|$ is the distance from $x$ to $2$.',
        'So $x$ is closer to $-2$ than to $2$. The point in the middle is $0$, so $x<0$.',
        'Check $x=-3$: $|-1|=1$ and $|-5|=5$, and $1<5$ ✓.',
        'The others fail: $x=0$ gives $2<2$ ✗. $x=2$ gives $4<0$ ✗. $x=\\frac12$ gives $2.5<1.5$ ✗.'])
    S('q-373', stem='Given:\n$\\begin{cases} m<0 \\\\ n>0 \\end{cases}$\nWhat is $|m\\cdot n|$?', expl=[
        '$m\\cdot n$ is negative (negative times positive), so $|m\\cdot n|=-m\\cdot n$.',
        'Choice 1: $m<0$, so $|m|=-m$, and $n\\cdot|m|=n\\cdot(-m)=-m\\cdot n$. A match.',
        'Or plug in $m=-2$, $n=3$: $|m\\cdot n|=6$. Choice 1: $3\\cdot2=6$ ✓. Choice 2: $-2\\cdot3=-6$. Choice 3: $-6$. Choice 4: $-3\\cdot2=-6$.'])
    S('q-374', stem='Given: $|a+b|=|a-b|$. What is $a\\cdot b$?', expl=[
        'Both sides are zero or positive, so we may square both sides: $(a+b)^2=(a-b)^2$.',
        'Expand: $a^2+2ab+b^2=a^2-2ab+b^2$, so $4ab=0$ and $a\\cdot b=0$.',
        'Check: $a=0$, $b=5$: $|5|=|-5|$ ✓.'])
    S('q-375', stem='$a$ is a negative number. Given:\n$\\begin{cases} |a|+5=b \\\\ b>9 \\end{cases}$\nWhat is the most precise range for $a$?', expl=[
        'Put $b$ into the inequality: $|a|+5>9$, so $|a|>4$.',
        '$a$ is negative, so $|a|=-a$. Then $-a>4$, so $a<-4$.',
        'Check: $a=-5$ gives $b=10>9$ ✓. $a=-3$ gives $b=8$ ✗.'])
    S('q-376', stem='Given: $b^m\\ne|b|^m$, where $m$ is an integer. Which of the following is necessarily true?',
      choices=['$b<0$ and $m<0$', '$b<0$ and $m$ is odd', '$b>0$ or $m$ is even', '$b>0$ or $m<0$'], expl=[
        'If $b\\ge0$, then $|b|=b$ and the two powers are equal. So $b<0$.',
        'If $b<0$ and $m$ is even, the even power hides the sign: $(-2)^2=4=|-2|^2$. So $m$ is odd.',
        'Check: $b=-2$, $m=3$: $(-2)^3=-8$, but $|-2|^3=8$ ✓. Choice 1 is not necessary: here $m=3$ is positive.'])
    S('q-377', stem='Given:\n$\\begin{cases} x<-2 \\\\ |x|=|y| \\end{cases}$\nWhich of the following is necessarily true?', expl=[
        '$x<-2$, so $|x|>2$. Then $|y|=|x|>2$, and $y^2=|y|^2>4$. Choice 1 is always true.',
        '$y$ can be $x$ or $-x$. Take $x=-3$.',
        '$y=-3$: then $y<-2$ (choice 2 fails), and $x+y=-6$ (choice 3 fails).',
        '$y=3$: then $\\frac{x}{y}=-1$ (choice 4 fails).'])
    S('q-378', stem='Given:\n$\\begin{cases} |x|\\ne x \\\\ |-5x|\\ne-5x \\end{cases}$\nWhat is $x$?',
      choices=['$0$', '$\\frac15$', '$-\\frac15$', 'No number $x$ satisfies the conditions.'], expl=[
        '$|x|\\ne x$ only when $x<0$.',
        '$|-5x|\\ne-5x$ only when $-5x<0$, so $x>0$.',
        'No number is both negative and positive. No number satisfies the conditions.',
        'For example, $x=-\\frac15$ gives $-5x=1$ and $|1|=1$, so the second condition fails.'])
    S('q-379', stem='Given: $(a-b)^2<4$. Which of the following is necessarily true?', expl=[
        '$(a-b)^2=|a-b|^2$. Both sides of $|a-b|^2<4$ are zero or positive, so take the root: $|a-b|<2$.',
        'The sum $a+b$ can be anything. $a=b=100$: $(a-b)^2=0<4$, but $(a+b)^2=40{,}000$, so choice 3 fails. $a=b=0$: $(a+b)^2=0$, so choice 4 fails.'])
    S('q-380', stem='Given:\n$\\begin{cases} |4x+2|=10 \\\\ |2x+1|=-2x-1 \\end{cases}$\nWhat is $x$?', expl=[
        'First equation: $4x+2=10$, so $x=2$. Or $4x+2=-10$, so $x=-3$.',
        'Second equation: the right side is $-(2x+1)$. $|A|=-A$ only when $A\\le0$. So $2x+1\\le0$, and $x\\le-\\frac12$.',
        'Only $x=-3$ fits. Check: $|4\\cdot(-3)+2|=|-10|=10$ ✓ and $|2\\cdot(-3)+1|=|-5|=5=-2\\cdot(-3)-1$ ✓.'])
    S('q-381', stem='Given:\n$\\begin{cases} P\\cdot Q<0 \\\\ \\frac{P}{Q}<\\frac{Q}{P} \\end{cases}$\nWhich of the following is necessarily true?', expl=[
        'Move everything to one side: $\\frac{P}{Q}-\\frac{Q}{P}<0$, so $\\frac{P^2-Q^2}{P\\cdot Q}<0$.',
        'The bottom $P\\cdot Q$ is negative. A fraction with a negative bottom is negative only when its top is positive: $P^2-Q^2>0$.',
        'So $P^2>Q^2$, which means $|P|>|Q|$.',
        'Choices 2 to 4 are not necessary. $P=-3$, $Q=1$: $-3<-\\frac13$ ✓, but $Q<0<P$ fails, and $P+Q=-2$ (choice 3 fails). '
        '$P=3$, $Q=-1$: $-3<-\\frac13$ ✓, and $P+Q=2$ (choice 4 fails).'])
    S('q-382', stem='Given:\n$\\begin{cases} a\\ne b \\\\ a-b=|a+b| \\end{cases}$\nWhich of the following is necessarily true?',
      choices=['$a<0$ and $b<0$', '$a=0$ or $b=0$', '$a=-b$', '$a>0$ and $b>0$'], expl=[
        'Case $a+b\\ge0$: $a-b=a+b$, so $2b=0$ and $b=0$.',
        'Case $a+b<0$: $a-b=-(a+b)=-a-b$, so $2a=0$ and $a=0$.',
        'Either way, $a=0$ or $b=0$.',
        'Check: $a=5$, $b=0$: $5-0=5=|5|$ ✓. This example also rules out choices 1, 3 and 4.'])
    S('q-383', stem='$x$ is an integer. Given: $|x+6|<4$. How many different values can $x$ have?', expl=[
        '$-4<x+6<4$. Subtract $6$: $-10<x<-2$.',
        'The integers: $-9$, $-8$, $-7$, $-6$, $-5$, $-4$, $-3$. That is $7$ values.',
        'With the distance picture: less than $4$ from $-6$. The ends $-10$ and $-2$ are not included.'])
    S('q-384', stem='In which of the following cases is $|c|+|d|=|c+d|$ not necessarily true?',
      choices=['$c$ and $d$ are both positive', '$c$ and $d$ are both negative', '$c$ and $d$ are integers', '$d=0$ or $c=0$'], expl=[
        '$|c+d|=|c|+|d|$ when $c$ and $d$ do not have opposite signs.',
        'Both positive ✓, both negative ✓, one of them $0$ ✓. In these cases it is always true.',
        '"Integers" says nothing about the signs: $c=3$, $d=-4$ gives $|3|+|-4|=7$, but $|3+(-4)|=1$. So choice 3.'])
    S('q-385', stem='Given: $p<q<|p\\cdot q\\cdot r|<r$. Which of the following is necessarily true?', expl=[
        '$|p\\cdot q\\cdot r|\\ge0$ and $|p\\cdot q\\cdot r|<r$, so $r>0$ and $|r|=r$.',
        '$|p\\cdot q\\cdot r|=|p\\cdot q|\\cdot r<r$. Divide by the positive $r$: $|p\\cdot q|<1$.',
        'The others are not necessary. $p=-0.9$, $q=-0.5$, $r=0.3$: $|p\\cdot q\\cdot r|=0.135$, and $-0.9<-0.5<0.135<0.3$. Here $r<1$ (choice 2 fails) and $|p|>|r|$ (choice 3 fails).',
        '$p=0.01$, $q=0.02$, $r=200$: $|p\\cdot q\\cdot r|=0.04$, and $0.01<0.02<0.04<200$. Here $p>0$ (choice 4 fails).'])

    E = 'alg-extra-unit-t13-3-%d'
    S(E % 1, stem='$|3-8|=?$', choices=['$-5$', '$3$', '$8$', '$5$'], expl=[
        'Inside first: $3-8=-5$.', 'The distance of $-5$ from zero is $5$: $|-5|=5$.',
        'Choice 1 forgets the bars. An absolute value is never negative.'])
    S(E % 2, stem='Given: $|x-3|=5$. What is the sum of all the possible values of $x$?',
      choices=['$6$', '$3$', '$5$', '$10$'], expl=[
        'Two cases: $x-3=5$, so $x=8$. Or $x-3=-5$, so $x=-2$.', 'The sum: $8+(-2)=6$.'])
    S(E % 3, stem='Given: $x<0$. $|x|-x=?$', expl=[
        '$x<0$, so $|x|=-x$.', '$|x|-x=-x-x=-2x$.',
        'Check: $x=-3$: $|-3|-(-3)=3+3=6$, and $-2\\cdot(-3)=6$ ✓.'])
    S(E % 4, stem='Which of the following gives all the solutions of $|x|<3$?', expl=[
        'The distance of $x$ from $0$ is less than $3$: $-3<x<3$.',
        'The ends are not included: $|3|=3$ is not less than $3$. So choice 2 (with $\\le$) is wrong.'])
    S(E % 5, stem='What is the smallest possible value of $|x-3|+|x-5|$?', choices=['$3$', '$2$', '$0$', '$8$'], expl=[
        '$|x-3|$ is the distance from $x$ to $3$, and $|x-5|$ is the distance from $x$ to $5$.',
        'If $x$ is between $3$ and $5$, the two distances add up to the gap from $3$ to $5$, which is $2$. For example, $x=4$: $1+1=2$.',
        'If $x$ is outside, the sum is bigger. For example, $x=6$: $3+1=4$. So the smallest value is $2$.'])
    S(E % 6, stem='Given: $|x|=-x$. Which of the following is necessarily true?', expl=[
        '$|x|=-x$ holds for every negative $x$: $|-4|=4=-(-4)$ ✓.',
        'It also holds for $x=0$: $|0|=0=-0$ ✓.',
        'So $x\\le0$. Choice 1 ($x<0$) forgets the zero.'])
    S(E % 7, stem='How many integers $x$ satisfy $|x-3|\\le2$?', choices=['$4$', '$6$', '$5$', '$3$'], expl=[
        '$-2\\le x-3\\le2$. Add $3$: $1\\le x\\le5$.',
        'The ends are included: $1$, $2$, $3$, $4$, $5$. There are $5$ integers.'])

    # =====================================================================================
    # 6. New guided questions with solution videos
    # =====================================================================================
    G1 = 'Absolute Value Questions'
    G2 = 'Advanced Absolute Value'

    # --- G1 (section 1, after Q5): a medium bridge equation
    M.new_q(qid(1), TOPIC, 'Given: $|2x-1|=7$. Which of the following gives all the possible values of $x$?',
            ['$4$ only', '$4$ or $-4$', '$4$ or $-3$', '$3$ or $-4$'], 3, [
        'Two cases. $2x-1=7$, so $2x=8$ and $x=4$.',
        'Or $2x-1=-7$, so $2x=-6$ and $x=-3$.',
        'Check: $|2\\cdot4-1|=7$ ✓ and $|2\\cdot(-3)-1|=|-7|=7$ ✓. So $x=4$ or $x=-3$.',
        'Choice 1 forgets the second case. Choice 2 just flips the sign of $4$, but the $-1$ inside breaks that symmetry.'])
    M.place_q(qid(1), SEC1, after='solve-q-362')
    _solution(M, qid(1), G1, SB1, 37, [
        "A medium one before the advanced part.",
        "An equation with a number in front of x.",
    ], [
        ('Two cases', [
            "Bars equal seven. So the inside is seven — or negative seven.",
            D('Write "2x − 1 = 7 → 2x = 8 → x = 4"'),
            "First case: two x minus one is seven. Two x is eight. x is four.",
            D('Write "2x − 1 = −7 → 2x = −6 → x = −3"'),
            "Second case: two x minus one is negative seven. Two x is negative six. x is negative three.",
            D('Write "|2 · 4 − 1| = 7 ✓   |2 · (−3) − 1| = |−7| = 7 ✓"'),
            "Check both. Eight minus one is seven. Negative six minus one is negative seven, and the bars give seven. Both work.",
            D('Circle choice 3'),
            "Four or negative three. Choice three.",
            "Choice one forgets the second case. Choice two just flips the sign of four — but the minus one inside breaks the symmetry.",
        ]),
    ])

    # --- G2 (section 1): negative right side
    M.new_q(qid(2), TOPIC, 'Which of the following has no solution?',
            ['$|x-3|=0$', '$|x+2|<-1$', '$|x+2|>-1$', '$|x|\\le1$'], 2, [
        'Look at the right side of each one.',
        'Choice 1: bars equal to $0$ means the inside is $0$: $x=3$.',
        'Choice 2: bars are never negative, so they are never less than $-1$. No solution.',
        'Choice 3: bars are always greater than $-1$. Every $x$ is a solution.',
        'Choice 4: $x=0$ gives $|0|=0\\le1$ ✓.'])
    M.place_q(qid(2), SEC1, after='solve-' + qid(1))
    _solution(M, qid(2), G1, SB1, 37, [
        "Which one has no solution?",
        "No algebra needed. Look at the right side.",
    ], [
        ('Look at the right side', [
            "Choice one: bars equal zero. That's possible — when the inside is zero.",
            D('Next to choice 1 write "x = 3" and cross it out'),
            "x is three. A solution. Out.",
            "Choice two: bars less than negative one. Bars are never negative — so they're never below negative one.",
            D('Next to choice 2 write "never"'),
            "No solution at all. Keep it.",
            "Choice three: bars bigger than negative one. Always true — every x works.",
            D('Next to choice 3 write "every x" and cross it out'),
            "Choice four: x within one of zero. Zero works.",
            D('Next to choice 4 write "x = 0 ✓" and cross it out'),
            D('Circle choice 2'),
            "Choice two.",
            "Look at choices two and three: the same numbers, a different sign. One is never true — the other is always true.",
        ]),
    ])

    # --- G3 (section 2, before Q10): letter on the right side
    M.new_q(qid(3), TOPIC, 'Given: $|x+4|=3x$. Which of the following gives all the possible values of $x$?',
            ['$2$ only', '$-1$ only', '$2$ or $-1$', 'There is no such number $x$.'], 1, [
        'Case 1: $x+4=3x$, so $4=2x$ and $x=2$. Case 2: $x+4=-3x$, so $4x=-4$ and $x=-1$.',
        'Check in the original equation. $x=2$: $|6|=6=3\\cdot2$ ✓. $x=-1$: $|3|=3$, but $3\\cdot(-1)=-3$ ✗.',
        'Only $x=2$.',
        'Faster: the bars are never negative, so $3x\\ge0$ and $x\\ge0$. That rules out $-1$ at once.'])
    M.place_q(qid(3), SEC2, after='solve-q-366')
    _solution(M, qid(3), G2, SB2, 38, [
        "A letter on the right side.",
        "Remember the tool: solve — then check.",
    ], [
        ('Method 1 · Two cases, then check', [
            "Two cases, as usual.",
            D('Write "x + 4 = 3x → 4 = 2x → x = 2"'),
            "Case one: x plus four equals three x. Four equals two x. x is two.",
            D('Write "x + 4 = −3x → 4x = −4 → x = −1"'),
            "Case two: x plus four equals minus three x. Four x is negative four. x is negative one.",
            D('Write "x = 2: |6| = 6 = 3 · 2 ✓"'),
            "Check two: six on the left, six on the right. It works.",
            D('Write "x = −1: |3| = 3, but 3 · (−1) = −3 ✗"'),
            "Check negative one: three on the left, negative three on the right. Fake.",
            D('Circle choice 1'),
            "Only two. Choice one. Choice three is the trap — it keeps the fake answer.",
        ]),
        ('Method 2 · The right side is never negative', [
            "Faster: bars are never negative. So three x can't be negative.",
            D('Write "3x ≥ 0 → x ≥ 0"'),
            "x is zero or positive. Negative one is out at once — and choices two and three go with it.",
            D('Cross out choices 2 and 3'),
            "Now just check two: six equals six. So there IS a solution. Choice four is out too.",
            D('Cross out choice 4 and circle choice 1'),
            "Choice one.",
        ]),
    ])

    # =====================================================================================
    # 7. New practice questions
    # =====================================================================================
    P = {}
    P[5] = ('Which of the following is true for every number $x$?',
            ['$|x-1|>0$', '$|x|>x$', '$|x+1|>|x|$', '$|x-1|\\ge-1$'], 4, [
        'Choice 4: an absolute value is never negative, so it is always greater than $-1$. True for every $x$.',
        'The others fail for some $x$. Choice 1: $x=1$ gives $0>0$ ✗. Choice 2: $x=5$ gives $5>5$ ✗. Choice 3: $x=-5$ gives $4>5$ ✗.'])
    P[7] = ('Given: $x<0<y$. $\\frac{|x|}{x}+\\frac{2y}{|y|}=?$', ['$3$', '$-1$', '$1$', '$-3$'], 3, [
        '$x<0$, so $|x|=-x$ and $\\frac{|x|}{x}=\\frac{-x}{x}=-1$.',
        '$y>0$, so $|y|=y$ and $\\frac{2y}{|y|}=2$.',
        '$-1+2=1$.',
        'Check: $x=-4$, $y=5$: $\\frac{4}{-4}+\\frac{10}{5}=-1+2=1$ ✓.'])
    P[8] = ('Given: $x>2$. $|2-x|+|x|=?$', ['$2$', '$2x-2$', '$2x+2$', '$-2$'], 2, [
        '$x>2$, so $2-x<0$ and $|2-x|=x-2$. Also $|x|=x$.',
        '$|2-x|+|x|=x-2+x=2x-2$.',
        'Check with a number: $x=5$ gives $|-3|+5=8$, and $2\\cdot5-2=8$ ✓. Choice 1 comes from the mistake $|2-x|=2-x$.'])
    P[9] = ('Given: $|x-2|=2x+1$. Which of the following gives all the possible values of $x$?',
            ['$-3$ or $\\frac13$', '$\\frac13$ only', '$-3$ only', 'There is no such number $x$.'], 2, [
        'Case 1: $x-2=2x+1$, so $x=-3$. Case 2: $x-2=-(2x+1)$, so $3x=1$ and $x=\\frac13$.',
        'Check $x=-3$: $|-5|=5$, but $2\\cdot(-3)+1=-5$ ✗. A fake solution.',
        'Check $x=\\frac13$: $\\left|\\frac13-2\\right|=\\frac53$ and $\\frac23+1=\\frac53$ ✓.',
        'Faster: the right side cannot be negative, so $2x+1\\ge0$ and $x\\ge-\\frac12$. That rules out $-3$.'])
    P[10] = ('$x$ is an integer. Given: $|x-1|+|x-7|=6$. How many different values can $x$ have?',
             ['$2$', '$6$', '$7$', 'Infinitely many'], 3, [
        '$|x-1|$ is the distance from $x$ to $1$, and $|x-7|$ is the distance from $x$ to $7$.',
        'The gap from $1$ to $7$ is $6$. For every $x$ from $1$ to $7$ (ends included), the two distances add up to exactly $6$. For example, $x=3$: $2+4=6$ ✓.',
        'Outside, the sum is more than $6$. For example, $x=8$: $7+1=8$.',
        'The integers from $1$ to $7$: $7$ values. Choice 1 counts only the two ends.'])
    P[11] = ('Given: $|3x-6|\\le0$. What is $x$?', ['$-2$', '$2$', '$0$', 'There is no such number $x$.'], 2, [
        'An absolute value is never negative. It can be at most $0$ only if it is exactly $0$.',
        '$3x-6=0$, so $x=2$.',
        'Choice 4 is the trap: "$\\le0$" includes "$=0$".'])
    P[12] = ('Given:\n$\\begin{cases} |x|=-x \\\\ |y|=y \\end{cases}$\nWhich of the following is necessarily true?',
             ['$x<y$', '$x\\cdot y<0$', '$x+y\\ge0$', '$x\\le y$'], 4, [
        '$|x|=-x$, so $x\\le0$. $|y|=y$, so $y\\ge0$. Therefore $x\\le0\\le y$, and $x\\le y$.',
        'The zero is the trap. $x=y=0$ satisfies both givens. Then $x<y$ fails, and $x\\cdot y=0$ is not negative.',
        'Choice 3: $x=-5$, $y=1$ gives $x+y=-4$ ✗.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q(qid(k), TOPIC, stem, ch, cor, ex)
        M.place_q(qid(k), PRACT)

    # =====================================================================================
    # 8. Practice order: warm-up extras first, then easy -> exam-hard
    # =====================================================================================
    M.practice_order(PRACT, [
        E % 1, E % 4, E % 2, E % 3, E % 6, E % 7, qid(11), qid(5), 'q-383', 'q-375', 'q-373', qid(8), qid(7),
        'q-371', 'q-374', 'q-378', 'q-379', qid(12), 'q-372', E % 5, qid(9), 'q-380', 'q-377', qid(10),
        'q-376', 'q-384', 'q-382', 'q-381', 'q-385'])

    # =====================================================================================
    # 8b. 2026-10-01 elite comparison: the sum rule as a sign-reading tool
    # =====================================================================================
    elite_signs(M)

    # =====================================================================================
    # 9. Keep video titles and slide notes in sync with the rewritten stems
    # =====================================================================================
    for vid, v in M.D['videos'].items():
        if v['topic'] != TOPIC or v.get('kind') != 'solution' or not v.get('questionId'): continue
        q = M.q(v['questionId'])
        v['title'] = v['navLabel'] = q['stem']
        for b in v['beats']:
            if (b.get('canvas') or '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (q['id'], q['stem'])

    # =====================================================================================
    # 10. Pass 2: summary lesson right before the independent practice
    # =====================================================================================
    summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last


def elite_signs(M):
    """2026-10-01 elite comparison: |a+b| vs |a|+|b| read as a sign tool (same signs add, opposite signs cancel).
    Real exams: 2021 autumn II-15, 2024 spring II-18, 2025 spring I-19, 2020 autumn II-13."""
    # --- Exam Tools video: five tools now, two new slides before the recap
    M.edit_lines(TOOLS, 1, lambda ls: [{'say': "Five tools for the harder absolute-value questions."} if l.get('say', '').startswith('Four tools') else l for l in ls])
    M.insert_slides(TOOLS, 5, [
        dict(mode='concept', active=4, title='Add or cancel', script=[
            "The last tool reads signs. It comes from the sum rule.",
            A('|−3 + (−5)| = 8 appears', T('$|-3+(-5)|=8=3+5$', size=50, gap=40)),
            "Same signs: both numbers pull the same way. The sizes add up.",
            A('|−3 + 5| = 2 appears', T('$|-3+5|=2=5-3$', size=50, gap=40)),
            "Opposite signs: they pull against each other. They cancel.",
            "What's left is the bigger size minus the smaller one.",
            A("'Same signs → add · opposite signs → cancel' appears",
              T('Same signs $\\to$ add $\\qquad$ Opposite signs $\\to$ cancel', size=44)),
            D('Write "|x| = 9, |y| = 2:  |x + y| = 11 or 7"'),
            "Example: x is nine away from zero, y is two away.",
            "Same signs: eleven. Opposite signs: nine minus two, seven. Only two possible values.",
        ]),
        dict(mode='concept', active=5, title='Read the signs', script=[
            "Now read it backwards: from the sizes to the signs.",
            "Remember, x minus y is x plus negative y. The minus flips the sign of y.",
            A('|x + y| < |x − y| → x · y < 0 appears', T('$|x+y|<|x-y| \;\\to\; x\\cdot y<0$', size=48, gap=40)),
            "In one of these two, the sizes add. In the other one, they cancel.",
            "The sum is the smaller one? Then the sum is where they cancel. Opposite signs — a negative product.",
            D('Write "x = 4, y = −1:  |3| < |5| ✓"'),
            A('|x + y| = |x| − |y| → opposite signs appears',
              T('$|x+y|=|x|-|y| \;\\to\;$ opposite signs, $|x|\\ge|y|$', size=44, gap=40)),
            "The sizes subtract? That's cancelling. Opposite signs again.",
            "And x is the bigger one in size — the left side can't be negative.",
            A('|a + b| < |a| → opposite signs appears', T('$|a+b|<|a| \;\\to\;$ $b$ has the opposite sign of $a$', size=44)),
            "The sum is smaller than one of its numbers? Adding b made it smaller. So they cancelled — opposite signs.",
            "And b is less than twice a in size. A bigger b would overshoot past zero.",
            "On the exam the numbers are usually not zero. A zero adds nothing and cancels nothing.",
        ]),
    ])
    M.set_slide(TOOLS, 8, script=[
        "Let's lock it in.",
        A("'|x|² = x², √(x²) = |x|' appears", T('$|x|^2=x^2$ · $\\sqrt{x^2}=|x|$ · $|a-b|=|b-a|$', size=40)),
        A("'Bars on both sides → square' appears", T('Bars on both sides $\\to$ square both sides', size=40)),
        A("'Letter on the right → check' appears", T('Letter on the right $\\to$ check every answer', size=40)),
        A("'|x − a| = distance' appears", T('$|x-a|$ = distance between $x$ and $a$', size=40)),
        A("'Same signs add, opposite signs cancel' appears", T('Same signs $\\to$ sizes add · opposite signs $\\to$ cancel', size=40)),
        "Next: a card with the question wordings. Then the advanced questions.",
    ])
    M.set_sidebar(TOOLS, ['Squares and bars', 'Square both sides', 'Letter on the right', 'Distance',
                          'Add or cancel', 'Read the signs', 'Recap'])
    M.slide(TOOLS, 8)['active'] = 6

    # --- memory card: the sign-reading rows
    card = M.card('mem-absolute-value')
    for t in card['tables']:
        if t['title'] == 'Rules':
            for r in t['rows']:
                if r[0] == '$|a+b|\\le|a|+|b|$':
                    r[1] = 'Same signs: the sizes add (equal). Opposite signs: they cancel (smaller).'
        if t['title'] == 'Sign clues':
            t['rows'] += [
                ['$|x+y|<|x-y|$', 'opposite signs: $x\\cdot y<0$'],
                ['$|x+y|=|x|-|y|$', 'opposite signs, and $|x|\\ge|y|$'],
                ['$|a+b|<|a|$', '$b$ has the opposite sign of $a$, and $|b|<2|a|$'],
            ]

    # --- guided question: read the signs, then add or cancel the sizes
    g = qid(13)
    M.new_q(g, TOPIC, 'Given:\n$\\begin{cases} |a|=7 \\\\ |b|=3 \\\\ |a+b|<|a-b| \\end{cases}$\nWhat is $|a+b|$?',
            ['$10$', '$4$', '$-4$', 'It cannot be determined from the given information.'], 2, [
        '$|a+b|<|a-b|$: in one of the two the sizes add, and in the other they cancel. The sum is the smaller one, '
        'so in the sum they cancel. So $a$ and $b$ have opposite signs.',
        'Opposite signs cancel: $|a+b|$ is the bigger size minus the smaller one: $7-3=4$.',
        'Check all four sign options. $a=7$, $b=-3$: $|4|<|10|$ ✓. $a=-7$, $b=3$: $|-4|<|-10|$ ✓. '
        '$a=7$, $b=3$: $|10|<|4|$ ✗. $a=-7$, $b=-3$: $|-10|<|-4|$ ✗. Both allowed options give $|a+b|=4$.',
        'Choice 1 ($10$) is the same-signs case, which the third given rules out. Choice 3 forgets that an absolute value '
        'is never negative. Choice 4 is right only if you ignore the third given.'])
    M.place_q(g, SEC2, after='solve-q-366')
    _solution(M, g, 'Advanced Absolute Value', SB2, 38, [
        "Three givens. The first two give sizes.",
        "The third one tells you the signs.",
    ], [
        ('Method 1 · Read the signs', [
            "a is seven away from zero. b is three away. The signs — we don't know yet.",
            "So a plus b is ten — or four. Same signs add, opposite signs cancel.",
            D('Under the question write "same signs: 10   opposite signs: 4"'),
            "Now the third given. a plus b, against a minus b.",
            "In one of them the sizes add. In the other, they cancel.",
            D('Underline "|a + b| < |a − b|" and write "the sum cancels → opposite signs"'),
            "The sum is the smaller one. So the sum is where they cancel. a and b have opposite signs.",
            D('Write "|a + b| = 7 − 3 = 4"'),
            "Opposite signs: the bigger size minus the smaller. Seven minus three — four.",
            D('Circle choice 2'),
            "Choice two.",
            "Ten is the same-signs case — the third given throws it out. Negative four? Bars are never negative.",
            "And \"cannot be determined\" is the trap for anyone who skips the third given.",
        ]),
        ('Method 2 · Try the four sign cases', [
            "Not sure about the tool? There are only four sign options. Try them all.",
            D('Write "a = 7, b = 3:  |10| < |4| ✗"'),
            "Both positive: ten is not less than four. Out.",
            D('Write "a = −7, b = −3:  |−10| < |−4| ✗"'),
            "Both negative: ten and four again. Out.",
            D('Write "a = 7, b = −3:  |4| < |10| ✓     a = −7, b = 3:  |−4| < |−10| ✓"'),
            "Opposite signs: four is less than ten. Both work.",
            D('Circle the two 4s'),
            "And in both, the absolute value of a plus b is four. Choice two.",
        ]),
    ])

    # --- practice question: the minus flips the sign
    p = qid(14)
    M.new_q(p, TOPIC, '$a$ and $b$ are numbers different from $0$.\nGiven: $|a-b|=|a|+|b|$.\nWhich of the following is necessarily true?',
            ['$a>b$', '$|a|>|b|$', '$a\\cdot b<0$', '$a+b>0$'], 3, [
        '$a-b=a+(-b)$. The sizes add, so $a$ and $-b$ have the same sign.',
        'So $a$ and $b$ have opposite signs, and $a\\cdot b<0$ (choice 3).',
        'The others are not necessary. $a=2$, $b=-5$: $|7|=7=2+5$ ✓, but $|a|<|b|$ (choice 2 fails) and $a+b=-3$ (choice 4 fails).',
        '$a=-2$, $b=5$: $|-7|=7=2+5$ ✓, but $a<b$ (choice 1 fails).'])
    M.place_q(p, PRACT, after='q-384')


SUMMARY_SB = ['Distance from zero', 'The rules', 'Sign clues', 'Equations', 'Inequalities',
              'Negative right side', 'Distance', 'Plug in', 'Before you practice']


def summary(M):
    def s(k, title, script):
        return dict(mode='concept', active=k, title=title, script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of absolute value.",
            "Everything important, in a few minutes.",
        ]),
        s(0, 'Distance from zero', [
            A('|x| = distance from 0 appears', T('$|x|$ = the distance from $0$ $\;\\to\;$ never negative', size=44, gap=40)),
            "Absolute value is distance from zero. It is zero or positive — never negative.",
            A('|−10| = 10, |0| = 0 appears', T('$|3|=3 \\qquad |-10|=10 \\qquad |0|=0$', size=48, gap=40)),
            "With a plain number, the minus just drops off.",
            A("'Letters hide their sign' appears", T('Letters: if $x=-7$, then $|x|=7=-x$', size=44)),
            "But a letter hides its sign. First ask: is it positive or negative?",
            "And an expression inside the bars? Calculate the whole inside first.",
        ]),
        s(1, 'The rules', [
            A('Product and fraction rules appear', T('$|a\\cdot b|=|a|\\cdot|b| \\qquad \\left|\\frac{a}{b}\\right|=\\frac{|a|}{|b|}$', size=46, gap=30)),
            "A product or a fraction: the bars can go on each part.",
            A('|a + b| ≤ |a| + |b| appears', T('$|a+b|\\le|a|+|b|$', size=46, gap=30)),
            "A sum: same signs — the sizes add. Opposite signs — they cancel, so it's smaller.",
            "And read it backwards: if the sizes cancelled, the signs were opposite.",
            A('Squares and roots appear', T('$|x|^2=x^2 \\qquad \\sqrt{x^2}=|x| \\qquad |a-b|=|b-a|$', size=44)),
            "A square and the bars both remove the sign. The root of x squared is the absolute value of x — not x.",
        ]),
        s(2, 'Sign clues', [
            A('Sign clues appear', T('$|x|>x \\to x<0 \\qquad |x|=x \\to x\\ge0$', size=44, gap=20)),
            A('More sign clues appear', T('$|x|=-x \\to x\\le0 \\qquad x>|x| \\to$ impossible', size=44, gap=40)),
            "Compare a number with its absolute value, and you know its sign.",
            D('Circle the "≥" and the "≤"'),
            "Don't forget the zero. It's the favorite trap.",
            A('Product signs and x/|x| appear', T('$a\\cdot b>0 \\to$ same signs $\\qquad \\frac{x}{|x|}=\\pm1$', size=44)),
            "A positive product: same signs. A negative product: opposite signs. And x over its absolute value is one or minus one.",
        ]),
        s(3, 'Equations', [
            A('|x + 2| = 10 appears', T('$|x+2|=10 \;\\to\; x+2=10$ or $x+2=-10$', size=44, gap=30)),
            "Bars equal a number? Two cases: plus and minus.",
            D('Write "x = 8 or x = −12"'),
            "x is eight or negative twelve. Keep both.",
            A("'Letter on the right → check' appears", T('Letter on the right $\\to$ check every answer', size=44, gap=30)),
            "A letter on the right side? The right side can't be negative. Check each answer in the original equation.",
            A("'Bars on both sides → square' appears", T('Bars on both sides $\\to$ square both sides', size=44)),
            "Bars on both sides? Both sides are zero or positive, so you may square them.",
        ]),
        s(4, 'Inequalities', [
            A('Small side appears', T('$|x-5|<3 \;\\to\; 2<x<8$  (between)', size=44, gap=40)),
            "Bars on the small side: the answer is trapped in the middle — between.",
            A('Big side appears', T('$|x-5|>3 \;\\to\; x>8$ or $x<2$  (outside)', size=44)),
            "Bars on the big side: two ranges — outside.",
        ]),
        s(5, 'Negative right side', [
            "Look at the right side before any algebra.",
            A('|x − 4| < −2 appears', T('$|x-4|<-2$ $\\;\\to\\;$ no solution', size=46, gap=30)),
            "Bars less than a negative number? Never. No solution.",
            A('|x − 4| > −2 appears', T('$|x-4|>-2$ $\\;\\to\\;$ every $x$', size=46, gap=30)),
            "Bars bigger than a negative number? Always. Every x works.",
            A('|x − 4| ≤ 0 appears', T('$|x-4|\\le0$ $\\;\\to\\;$ $x=4$', size=46)),
            "Bars at most zero: the inside must be zero. One solution.",
        ]),
        s(6, 'Distance', [
            A('|x − a| = distance appears', T('$|x-a|$ = the distance between $x$ and $a$', size=44, gap=30)),
            "The absolute value of x minus a is the distance between x and a.",
            A('|x + 6| = distance from −6 appears', T('$|x+6|$ = the distance from $-6$', size=44)),
            "Careful with a plus inside: x plus six is the distance from NEGATIVE six.",
        ]),
        s(7, 'Plug in', [
            A("'Plug in a number that fits' appears", T('An expression $=\\ ?$ $\;\\to\;$ plug in a number that fits', size=44, gap=30)),
            "Asked what an expression equals? Plug in a number that fits the conditions.",
            A("'Avoid 0, 1, −1 and numbers from the choices' appears", T('Avoid $0$, $1$, $-1$ and numbers from the choices', size=44)),
            "Avoid the special numbers. Eliminate three choices. Two survive? Plug in again.",
        ]),
        s(8, 'Before you practice', [
            "Before each question, ask yourself:",
            A("'Is the letter positive or negative?' appears", T('Is the letter positive, negative — or zero?', size=42)),
            A("'Did I keep both cases?' appears", T('Equation or inequality: did I keep both cases?', size=42)),
            A("'Right side negative or zero?' appears", T('Is the right side negative or zero?', size=42)),
            A("'Letter on the right: did I check?' appears", T('Letter on the right: did I check every answer?', size=42)),
            A("'What does the question ask?' appears", T('Must, could, cannot, or not necessarily?', size=42)),
            "The common traps: forgetting the zero, losing the second case, and keeping a fake answer.",
            "That's it. Now go practice.",
        ]),
    ]
    v = M.new_video('r26-t13-summary', TOPIC, 'Absolute Value — Summary', SUMMARY_SB, slides,
                    SEC2, after='solve-q-370')
    v['hybrid']['num'] = M.video('solve-q-370')['hybrid']['num']


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
    # Lesson "absolute-value" slide 9 solved |x + 3| = 8, the same as guided q-359 -> new lesson example |x + 4| = 6.
    _dd_sub(M, 'absolute-value', 9, [
        ('$|x+3|=8$', '$|x+4|=6$'),
        ('|x + 3| = 8 appears', '|x + 4| = 6 appears'),
        ('Underneath write two branches: "x + 3 = 8" and "x + 3 = −8"', 'Underneath write two branches: "x + 4 = 6" and "x + 4 = −6"'),
        ('Why both? Because if x plus three were negative eight, the bars would still turn it into eight.',
         'Why both? Because if x plus four were negative six, the bars would still turn it into six.'),
        ('Solve both: "x = 5" and "x = −11"', 'Solve both: "x = 2" and "x = −10"'),
        ('First case: x is five. Second case: x is negative eleven. Two solutions.',
         'First case: x is two. Second case: x is negative ten. Two solutions.')])
