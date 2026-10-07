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
    # --- Absolute Value: the Hebrew lesson ends after the rules, then teaches the sign clues inside its first
    # question. Cut: sign clues (Question 1, slide 3 has all four), signs of a product (Question 1) and x/|x|
    # (Question 5), equations (Questions 2 and 6), inequalities - small side / big side (Questions 3 and 4),
    # negative right side (Question 7), plug in (Question 5), recap.
    L = 'absolute-value'
    _cr_titles(M, L, ['Distance from zero', 'Plus or minus inside', 'Whole expression', 'The rules', 'When is it equal?'])
    _cr_insert(M, L, 6, 'So: same signs — equal. Different signs — smaller.', [
        'Seven questions next — each one before its own video. Each question teaches one more tool.'])
    _cr_replace(M, 'solve-q-359', 1, 'You know the move', [
        'An equation with an absolute value. The move: two cases.'])
    _cr_replace(M, 'solve-q-362', 1, 'You know what that means', [
        'They ask what an expression equals. That means we may plug in a number.'])
    _cr_replace(M, 'solve-q-362', 3, "That's the tool from the lesson", [
        'A useful fact: x over its absolute value is one for every positive x — and minus one for every negative x.'])
    # moved into Question 7 (the cut slide said it for equations too)
    _cr_insert(M, 'solve-q-r26-t13-02', 2, 'Look at choices two and three', [
        A("'Bars = a negative number → no solution' appears", T(r'Bars $=$ a negative number $\to$ no solution', 38)),
        'The same for an equation: bars equal to a negative number — no solution.'])

    # --- Absolute Value - Exam Tools: square both sides (Question 15, method 2), letter on the right (Question 13),
    # add or cancel and |x + y| < |x − y| (Question 12). Kept: squares and bars, and distance (used in the practice,
    # no question video here teaches it). The other two sign readings move into Question 12.
    E = 'r26-t13-tools'
    _cr_titles(M, E, ['Squares and bars', 'Distance'])
    M.set_slide(E, 1, script=[
        'A few tools for the harder absolute-value questions.',
        'Two of them first. The others come inside the questions — right when you need them.'])
    _cr_insert(M, E, 3, 'Careful with a plus inside', [
        'Next: a card with the question wordings. Then the advanced questions.'])
    _cr_insert(M, 'solve-q-368', 3, 'The tool from the lesson', [
        A("'Bars on both sides → square both sides' appears", T(r'Bars on both sides $\to$ square both sides', 38))], before=True)
    _cr_replace(M, 'solve-q-368', 3, 'The tool from the lesson', [
        'A tool for bars on both sides: both sides are zero or positive. So we may square both sides. After squaring, the bars are gone.'])
    _cr_replace(M, 'solve-q-r26-t13-03', 1, 'Remember the tool', ['The tool: solve — then check every answer.'])
    _cr_insert(M, 'solve-q-r26-t13-03', 2, 'Choice three is the trap', [
        'So: a letter on the right side? Check every answer in the original equation.'])
    _cr_slide_after(M, 'solve-q-r26-t13-13', 2, 'Other wordings', [
        'Other wordings, same idea.',
        A("'|x + y| = |x| − |y| → opposite signs' appears", T(r'$|x+y|=|x|-|y| \;\to\;$ opposite signs, $|x|\ge|y|$', 40)),
        'The sizes subtract? That is cancelling — opposite signs. And x is the bigger one in size.',
        A("'|a + b| < |a| → opposite signs' appears", T(r'$|a+b|<|a| \;\to\;$ $b$ has the opposite sign of $a$', 40)),
        'The sum is smaller than one of its numbers? Adding b made it smaller — so they cancelled. Opposite signs.',
        'And b is less than twice a in size. A bigger b would overshoot past zero.'])


_apply_before_cut_repeats = apply


def apply(M):
    _apply_before_cut_repeats(M)
    cut_repeats(M)   # 2026-10-05: runs last


# ---------------------------------------------------------------- 2026-10-06 new exam methods
# THE MIRROR TEST (symmetry). Real exams: helps on 9 questions (2 solved with no numbers). Short lesson video right
# after Question 12 (reading the signs, "Other wordings"), then one guided question with its solution video.
MIRROR = 'r26-t13-mirror'


def add_methods(M):
    C = lambda k, title, script: dict(mode='concept', active=k, title=title, script=script)
    M.new_video(MIRROR, TOPIC, 'The Mirror Test', ['The idea', 'Flip all signs', 'Swap the letters', 'Limits'], [
        dict(mode='title', title='The Mirror Test', script=[
            "A tool for \"necessarily true\" questions with letters.",
        ]),
        C(0, 'The idea', [
            "Look at the given. Now change it in one of two ways.",
            A("'Flip all signs: x → −x, y → −y' appears", T('Flip all signs: $x\\to-x,\\ y\\to-y$', size=42, gap=24)),
            "One: flip every sign. x becomes minus x, and y becomes minus y.",
            A("'Swap the letters: x ↔ y' appears", T('Swap the letters: $x\\leftrightarrow y$', size=42, gap=40)),
            "Two: swap the letters. x becomes y, and y becomes x.",
            "If the given looks exactly the same after the change, the given is a mirror.",
            "Why does that help? Any numbers that fit the given — their mirror fits it too. So whatever is necessarily true stays necessarily true in the mirror.",
            A("'A choice that turns into its opposite → out' appears",
              T('A choice that turns into its opposite $\\to$ it can\'t be necessarily true', size=40)),
            "Now look at a choice. If the mirror turns it into its opposite, both can't always be true. Cross it out.",
            "The cue: a \"necessarily\" question, letters, and a given that looks balanced.",
        ]),
        C(1, 'Flip all signs', [
            A("'Given: |a + b| < |a| + |b|. Necessarily negative?' appears",
              T('Given: $|a+b|<|a|+|b|$. Which is necessarily negative?', size=40, gap=20)),
            A('The four choices appear', T('$a \\qquad b-a \\qquad a\\cdot b \\qquad a+b$', size=44, gap=40)),
            "An example. Which of these is necessarily negative?",
            "Step one: is the given a mirror? Flip all signs.",
            D('Write "a → −a, b → −b:  |−a − b| < |−a| + |−b|"'),
            "Minus a minus b has the same absolute value as a plus b. Bars on minus a and minus b give the same sizes. The given is the same — a mirror.",
            D('Write "a → −a ✗    b − a → a − b ✗    a + b → −(a + b) ✗"'),
            "a turns into minus a. If a were always negative, minus a would be always negative too. Impossible. Out.",
            "b minus a turns into a minus b. a plus b turns into its minus. Opposites — out.",
            D('Write "a · b → (−a)(−b) = a · b ✓"'),
            "a times b: minus times minus is plus. It doesn't change. The only survivor — that's the answer.",
            D('Write "a = 2, b = −1: |1| < 2 + 1 ✓, a · b = −2"'),
            "A quick check: a two, b minus one. One is less than three, and a times b is minus two. Negative.",
        ]),
        C(2, 'Swap the letters', [
            A("'Given: x² + y² = 13. Necessarily true?' appears",
              T('Given: $x^2+y^2=13$. Which is necessarily true?', size=40, gap=20)),
            A('The four choices appear', T('$x>0 \\qquad x<y \\qquad x+y>0 \\qquad x^2\\le13$', size=44, gap=40)),
            "Here both mirrors work. Flip the signs: minus x, squared, is x squared. The given doesn't change.",
            D('Write "flip:  x > 0 → x < 0 ✗    x + y > 0 → x + y < 0 ✗"'),
            "x positive turns into x negative. x plus y positive turns into x plus y negative. Both out.",
            "Now swap: y squared plus x squared is thirteen. The same given again.",
            D('Write "swap:  x < y → y < x ✗"'),
            "x less than y turns into y less than x. Opposites. Out.",
            "One choice is left: x squared is at most thirteen. And it's true: y squared is never negative, so x squared can't pass thirteen.",
            D('Write "x² ≤ 13 → y² ≤ 13: a twin, not an opposite"'),
            "Careful: in the swap it turns into y squared at most thirteen. That's a twin — not the opposite. Twins stay. Only opposites go out.",
        ]),
        C(3, 'Limits', [
            A("'No mirror in the given → no test' appears", T('The given changes in the mirror $\\to$ no test', size=40, gap=24)),
            "First, always check the given. Absolute a plus b, bigger than two b? Swap: bigger than two a. A different given. No mirror — no test.",
            A("'Simplify first: x − y + 2y = x + y' appears", T('Simplify first: $x-y+2y=x+y$', size=40, gap=24)),
            "Second: simplify a choice before you mirror it. x minus y plus two y looks lopsided — it's just x plus y. In \"which is NOT equal\" questions, equal choices often look lopsided like this.",
            A("'A formula for a quantity the mirror keeps → must not change' appears",
              T('Asked for a quantity the mirror keeps? A formula that changes isn\'t it', size=38, gap=24)),
            "The same idea works for formulas. If the mirror doesn't change what they ask for, a formula that changes can't be the answer.",
            "And if every choice survives the mirror, the test doesn't help. Go back to plugging in numbers.",
            A("'The rule' appears", T('Given unchanged in the mirror $\\to$ cross out every choice that turns into its opposite', size=36)),
            "The rule: if the given doesn't change in the mirror, a choice that turns into its opposite is not necessarily true.",
        ]),
    ], SEC2, after='solve-q-r26-t13-13')

    # --- guided question: a different given (a sum of squares), both mirrors
    g = qid(15)
    M.new_q(g, TOPIC, 'Given: $a^2+b^2=2ab+9$.\nWhich of the following is necessarily true?',
            ['$a-b=3$', '$a>b$', '$|a-b|=3$', '$a+b=3$'], 3, [
        'The mirror test. Swap $a$ and $b$: $b^2+a^2=2ba+9$, the same given. Flip all signs: $(-a)^2+(-b)^2=2(-a)(-b)+9$, '
        'also the same given. So the mirror of every pair that fits the given also fits it.',
        'Swap: $a-b=3$ turns into $b-a=3$, its opposite, so choice 1 is out. $a>b$ turns into $b>a$, so choice 2 is out.',
        'Flip: $a+b=3$ turns into $-a-b=3$, that is $a+b=-3$, so choice 4 is out.',
        '$|a-b|$ does not change in either mirror: $|b-a|=|a-b|$ and $|-a+b|=|a-b|$. Choice 3.',
        'Check with algebra: $a^2-2ab+b^2=9$, so $(a-b)^2=9$, and $a-b=3$ or $a-b=-3$. In both cases $|a-b|=3$.',
        'Choice 1 forgets the case $-3$: $a=0$, $b=3$ gives $0+9=0+9$ ✓ but $a-b=-3$.'])
    M.place_q(g, SEC2, after=MIRROR)
    n = M.next_question_number(TOPIC)
    old = 'Question %d' % (n - 1)            # q-r26-t13-13 (sign reading) - the new one comes right after it
    sb = None
    for v in M.D['videos'].values():
        s = (v.get('hybrid') or {}).get('sidebar') or []
        if v['topic'] == TOPIC and v.get('kind') == 'solution' and old in s:
            s.insert(s.index(old) + 1, 'Question %d' % n)
            for b in v['beats']:
                if b['mode'] == 'question' and b['active'] >= s.index('Question %d' % n): b['active'] += 1
            sb = s
    assert sb, 'sidebar with %s not found' % old
    _solution(M, g, 'Advanced Absolute Value', list(sb), 38, [
        "One given, two letters — and \"necessarily true\".",
        "A balanced given. A job for the mirror test.",
    ], [
        ('Method 1 · The mirror test', [
            "First: is the given a mirror? Swap a and b.",
            D('Write "swap: b² + a² = 2ba + 9 → the same given"'),
            "b squared plus a squared equals two b a plus nine. Exactly the same given.",
            "So for every pair that fits the given, the swapped pair fits it too.",
            D('Next to choice 1 write "b − a = 3 ✗"'),
            "Choice one: a minus b is three. Swap it: b minus a is three. That's the opposite sign. Both can't always be true. Out.",
            D('Next to choice 2 write "b > a ✗"'),
            "Choice two: a bigger than b. Swapped: b bigger than a. Opposites. Out.",
            "Now the second mirror: flip all signs. a to minus a, b to minus b.",
            D('Write "flip: (−a)² + (−b)² = 2(−a)(−b) + 9 → the same given"'),
            "Squares don't care about the sign. And minus a times minus b is a b. The same given again.",
            D('Next to choice 4 write "a + b = −3 ✗"'),
            "Choice four: a plus b is three. Flipped: minus a minus b is three. So a plus b is minus three. Opposite. Out.",
            D('Next to choice 3 write "swap ✓  flip ✓"'),
            "Choice three: the absolute value of a minus b. Swap or flip — the bars give the same number. It survives.",
            D('Circle choice 3'),
            "Choice three. And we didn't solve anything.",
        ]),
        ('Method 2 · Check with algebra', [
            "Want proof? Move the two a b to the left side.",
            D('Write "a² − 2ab + b² = 9 → (a − b)² = 9"'),
            "a squared minus two a b plus b squared — a shortcut formula. It's a minus b, squared. So that square is nine.",
            D('Write "a − b = 3  or  a − b = −3 → |a − b| = 3"'),
            "A square of nine: a minus b is three, or minus three. Either way, its absolute value is three.",
            D('Write "a = 0, b = 3: 0 + 9 = 0 + 9 ✓, a − b = −3"'),
            "Choice one is the trap. It forgets the minus three. a zero, b three: nine equals nine — and a minus b is minus three.",
            "The mirror test found it in seconds. The algebra proves it.",
        ]),
    ])
    q = M.q(g); v = M.video('solve-' + g)
    for b in v['beats']:
        if (b.get('canvas') or '').startswith('Pre-loaded — question'):
            b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (g, q['stem'])

    # --- q-368 (|x + 3y| = |3x + y|) is a swap mirror: one line at the end of its plug-in method
    _cr_insert(M, 'solve-q-368', len(M.video('solve-q-368')['beats']), 'Pick what suits you', [
        "And the mirror test sees part of it with no numbers: swap x and y — the given doesn't change. x less than y turns into y less than x. Choices three and four are out."],
        before=True)

    # --- memory card: one row
    for t in M.card('mem-absolute-value')['tables']:
        if t['title'] == 'Sign clues':
            t['rows'].append(['The given does not change when you flip all signs or swap the letters',
                              'mirror test: a choice that turns into its opposite is not necessarily true'])


_apply_before_add_methods = apply


def apply(M):
    _apply_before_add_methods(M)
    add_methods(M)   # 2026-10-06: runs last


# =====================================================================================
# 2026-10-06 practice: the new exam methods as an extra method in PRACTICE explanations
# (append only; the existing worked solution stays as it is). Runs last.
# =====================================================================================
PRACTICE_METHODS = {
    'q-r26-t13-14': [
        'Method 2 · Mirror test: swap $a$ and $b$. $|b-a|=|b|+|a|$ is the same given. Choice 1 ($a>b$) turns into $b>a$, and choice 2 ($|a|>|b|$) turns into $|b|>|a|$. Both turn into their opposites, so they are out.',
        'Flip all signs: $|-a+b|=|-a|+|-b|$ is the same given too. Choice 4 ($a+b>0$) turns into $a+b<0$, so it is out. Only choice 3 is left, with no numbers at all.',
    ],
    'q-381': [
        'Method 2 · Mirror test: flip all signs. $(-P)(-Q)=P\\cdot Q$ and $\\frac{-P}{-Q}=\\frac PQ$, so the given stays the same.',
        'Choice 2 ($Q<0<P$) turns into $P<0<Q$, choice 3 ($0<P+Q$) into $P+Q<0$, and choice 4 into $0<P+Q$. All three turn into their opposites, so they are out. Choice 1 ($|Q|<|P|$) does not change: it is the answer.',
    ],
    'q-375': [
        'Method 2 · The most precise range: $a=-5$ works ($b=10>9$), so choices 2 and 3 (which leave $-5$ out) are out. $a=-20$ works too ($b=25$), so choice 4 (which stops at $-14$) is out. The answer is choice 1.',
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


# =====================================================================================================================
# 2026-10-06 renumber pass: the English course must not look like the Hebrew one. Every Hebrew-derived question
# (guided q-358 ... q-370, practice q-371 ... q-385) gets new numbers / letters - same idea, same trap, same difficulty,
# same methods - and every guided solution video is rewritten to match. The Hebrew lesson's own examples get new
# numbers too (and the card / tools rows that came from the Hebrew lesson). Practice clean-up: 30 -> 20.
# Nothing in topic 13 is recorded (checked ~/Documents/Course.recordings on 2026-10-06). Runs last.
# =====================================================================================================================
def _nl_svg(c, r):
    """Number line -4 ... 8: the numbers less than r away from c (same style as NL_SVG)."""
    X = lambda n: 50 + (n + 4) * 45
    lo, hi = c - r, c + r
    f = 'font-family="DejaVu Sans,Arial,sans-serif"'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 150" role="img" aria-label="Number line: the numbers less than %d away from %d">'
            '<title>Within %d of %d</title>' % (r, c, r, c) +
            '<line x1="30" y1="95" x2="610" y2="95" stroke="#203344" stroke-width="2.5"/>'
            '<path d="M 612 95 l -10 -6 l 0 12 Z M 28 95 l 10 -6 l 0 12 Z" fill="#203344"/>'
            '<rect x="%d" y="88" width="%d" height="14" fill="#d5f1ed" stroke="#087f83" stroke-width="2"/>' % (X(lo), X(hi) - X(lo))
            + ''.join('<line x1="%d" y1="89" x2="%d" y2="101" stroke="#203344" stroke-width="2"/>'
                      '<text x="%d" y="128" text-anchor="middle" fill="#203344" %s font-size="18"%s>%s</text>'
                      % (X(n), X(n), X(n), f, ' font-weight="bold"' if n in (lo, c, hi) else '', ('−%d' % -n) if n < 0 else str(n))
                      for n in range(-4, 9))
            + '<circle cx="%d" cy="95" r="6" fill="#ffffff" stroke="#087f83" stroke-width="2.5"/>' % X(lo)
            + '<circle cx="%d" cy="95" r="6" fill="#ffffff" stroke="#087f83" stroke-width="2.5"/>' % X(hi)
            + '<circle cx="%d" cy="95" r="6" fill="#203344"/>' % X(c)
            + '<line x1="%d" y1="55" x2="%d" y2="55" stroke="#087f83" stroke-width="2.5"/><path d="M %d 55 l -12 -6 l 0 12 Z" fill="#087f83"/>' % (X(c), X(hi) - 4, X(hi))
            + '<text x="%d" y="42" text-anchor="middle" fill="#087f83" %s font-size="20" font-weight="bold">%d</text>' % ((X(c) + X(hi)) // 2, f, r)
            + '<line x1="%d" y1="55" x2="%d" y2="55" stroke="#087f83" stroke-width="2.5"/><path d="M %d 55 l 12 -6 l 0 12 Z" fill="#087f83"/>' % (X(c), X(lo) + 4, X(lo))
            + '<text x="%d" y="42" text-anchor="middle" fill="#087f83" %s font-size="20" font-weight="bold">%d</text>' % ((X(c) + X(lo)) // 2, f, r)
            + '<line x1="%d" y1="55" x2="%d" y2="89" stroke="#203344" stroke-width="1.5" stroke-dasharray="4 4"/>' % (X(c), X(c))
            + '</svg>')


def renumber(M):
    from math_api import rich_plain
    RECORDED = set()

    def S(qid_, **kw):
        if qid_ in RECORDED: return
        q = M.set_q(qid_, **kw)
        for v in M.D['videos'].values():   # keep any pre-loaded copy of the choices in sync
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid_ and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])

    def video(qid_, slides):
        if qid_ in RECORDED: return
        vid = 'solve-' + qid_
        for n, x in slides.items():
            title, script = x if isinstance(x, tuple) else (None, x)
            M.set_slide(vid, n, title=title, script=script)
        M.touched_videos.add(vid)

    def item(vid, n, k, t=None):
        it = dict(M.slide(vid, n)['items'][k])
        if t is not None: it['t'] = t
        return it

    # ---------------- lesson "Absolute Value": the Hebrew lesson's own examples -> new numbers, same points
    L = LESSON
    if L not in RECORDED:
        _dd_sub(M, L, 2, [('Draw an arc from 0 to 5 and write "5 units"', 'Draw an arc from 0 to 4 and write "4 units"'),
                          ('Five is five units away from zero.', 'Four is four units away from zero.'),
                          ('Draw an arc from 0 to −7 and write "7 units"', 'Draw an arc from 0 to −6 and write "6 units"'),
                          ('Negative seven? The number is negative — but its distance from zero is seven units.',
                           'Negative six? The number is negative — but its distance from zero is six units.'),
                          ("isn't minus three kilometers. It's three kilometers.", "isn't minus two kilometers. It's two kilometers.")])
        _dd_sub(M, L, 3, [('$|6|=6$', '$|8|=8$'), ('|6| = 6 appears', '|8| = 8 appears'),
                          ('Six is six units from zero.', 'Eight is eight units from zero.'),
                          ('$|-9|=9$', '$|-4|=4$'), ('|−9| = 9 appears', '|−4| = 4 appears'),
                          ('Negative nine is nine units away.', 'Negative four is four units away.'),
                          ('Circle the minus sign in −9 and cross it out', 'Circle the minus sign in −4 and cross it out')])
        _dd_sub(M, L, 4, [('$|5-11|$', '$|4-13|$'), ('|5 − 11| appears', '|4 − 13| appears'),
                          ('Write "= |−6| = 6"', 'Write "= |−9| = 9"'),
                          ('Five minus eleven is negative six. Its absolute value: six.', 'Four minus thirteen is negative nine. Its absolute value: nine.'),
                          ('Below, write "5 + 11 = 16" and cross it out', 'Below, write "4 + 13 = 17" and cross it out'),
                          ("turn the eleven positive first and add. That's sixteen", "turn the thirteen positive first and add. That's seventeen")])
        _dd_sub(M, L, 6, [('$|-2+(-5)| \\qquad |-2|+|-5|$', '$|-3+(-6)| \\qquad |-3|+|-6|$'),
                          ('|−2 + (−5)| and |−2| + |−5| appear', '|−3 + (−6)| and |−3| + |−6| appear'),
                          ('Under each, write "= 7" and put "=" between them', 'Under each, write "= 9" and put "=" between them'),
                          ('Same signs: negative two plus negative five is negative seven — absolute value seven. Separately: two plus five, seven. Equal.',
                           'Same signs: negative three plus negative six is negative nine — absolute value nine. Separately: three plus six, nine. Equal.'),
                          ('$|-2+5| \\qquad |-2|+|5|$', '$|-3+6| \\qquad |-3|+|6|$'),
                          ('|−2 + 5| and |−2| + |5| appear', '|−3 + 6| and |−3| + |6| appear'),
                          ('Under each, write "= 3" and "= 7", and put "<" between them', 'Under each, write "= 3" and "= 9", and put "<" between them'),
                          ('Different signs: negative two plus five is three. Separately: two plus five, seven.',
                           'Different signs: negative three plus six is three. Separately: three plus six, nine.')])
        for n in (2, 3, 4, 6): M.slide(L, n)['loads'] = ''
    # Exam Tools "Distance": the example |x - 2| < 4 came from the Hebrew lesson -> |x - 3| < 4 (new figure)
    if TOOLS not in RECORDED:
        b = M.slide(TOOLS, 3)
        vis = next(it for it in b['items'] if it.get('k') == 'vis'); vis['v'] = dict(vis['v'], svg=_nl_svg(3, 4))
        _dd_sub(M, TOOLS, 3, [('Number line: within 4 of 2 appears', 'Number line: within 4 of 3 appears'),
                              ('So the absolute value of x minus two, less than four, reads: x is less than four steps from two.',
                               'So the absolute value of x minus three, less than four, reads: x is less than four steps from three.'),
                              ('Start at two. Four steps left: negative two. Four steps right: six.',
                               'Start at three. Four steps left: negative one. Four steps right: seven.'),
                              ('Write "|x − 2| < 4 → −2 < x < 6"', 'Write "|x − 3| < 4 → −1 < x < 7"'),
                              ('x is between negative two and six.', 'x is between negative one and seven.'),
                              ('below negative two, or above six.', 'below negative one, or above seven.'),
                              ('$|x+5|=|x-(-5)|$ $\\to$ distance from $-5$', '$|x+6|=|x-(-6)|$ $\\to$ distance from $-6$'),
                              ('|x + 5| = distance from −5 appears', '|x + 6| = distance from −6 appears'),
                              ('x plus five is x minus negative five. So it\'s the distance from NEGATIVE five.',
                               'x plus six is x minus negative six. So it\'s the distance from NEGATIVE six.')])
    # memory card rows with the Hebrew lesson / question numbers
    for t in M.card('mem-absolute-value')['tables']:
        for r in t['rows']:
            if r[0] == '$|x+3|=8$': r[:] = ['$|x-4|=5$', '$x-4=5$ or $x-4=-5$']
            elif r[0] == '$|x-2|<4$ (small side)': r[:] = ['$|x-3|<4$ (small side)', '$-4<x-3<4$ → between: $-1<x<7$']
            elif r[0] == '$|x-2|>4$ (big side)': r[:] = ['$|x-3|>4$ (big side)', '$x-3>4$ or $x-3<-4$ → outside: $x>7$ or $x<-1$']
            elif r[0] == '$|x-a|$': r[1] = 'the distance between $x$ and $a$ ($|x+6|$: distance from $-6$)'

    # ============================== guided questions, Questions 1-7 (section 1)
    # q-358: ab < 0, a < |a| -> |b| = b   =>   xy < 0, y < |y| -> |x| = x (key 4)
    S('q-358', stem='Given:\n$\\begin{cases} x\\cdot y<0 \\\\ y<|y| \\end{cases}$\nWhich of the following is necessarily true?',
      choices=['$x<0$', '$\\left|x\\right| < \\left|y\\right|$', '$\\left|\\frac{y}{x}\\right| < 1$', '$\\left|x\\right| = x$'], correct=4, expl=[
        '$y<|y|$: a number is smaller than its absolute value only when it is negative. So $y<0$.',
        '$x\\cdot y<0$: the product is negative, so $x$ and $y$ have opposite signs. $y$ is negative, so $x>0$.',
        '$x$ is positive, so $|x|=x$ (choice 4). Choice 1 ($x<0$) is false.',
        'Choices 2 and 3 compare sizes, and the givens say nothing about sizes. $y=-3$, $x=8$: $|x|=8$ is bigger than $|y|=3$, so choice 2 fails. '
        '$y=-6$, $x=2$: $\\left|\\frac{y}{x}\\right|=3$, not less than $1$, so choice 3 fails.'])
    video('q-358', {2: [
        "Take the givens one at a time.",
        D('Underline "x · y < 0" and write "opposite signs"'),
        "x times y is negative. So they have opposite signs — one positive, one negative. We don't know which yet.",
        "If both were positive — or both negative — the product would be positive.",
        D('Underline "y < |y|" and write "y < 0"'),
        "Second given: y is smaller than its own absolute value. That means y is NEGATIVE.",
        "If y were positive, they'd be equal. Negative five is smaller than its absolute value, five.",
        D('Write "→ x > 0"'),
        "y is negative, and they have opposite signs. So x is the positive one.",
        D('Cross out choice 1'),
        "Choice one says x is negative. Out.",
        "Choice two: is x's absolute value smaller than y's? We don't know. y could be negative three and x could be eight — then it's bigger.",
        D('Cross out choice 2'),
        "Choice three has the same problem. y equals negative six, x equals two — the ratio is three, not less than one.",
        D('Cross out choice 3'),
        "Choice four: x is positive — and the absolute value of a positive number is the number itself.",
        D('Circle choice 4'),
        "Choice four."]})

    # q-359: |x + 3| = 8 -> -11   =>   |x + 7| = 9 -> -16 (key 3; trap -2)
    S('q-359', stem='Given: $|x+7|=9$. Which of the following could be the value of $x$?',
      choices=['$16$', '$-2$', '$-16$', '$6$'], correct=3, expl=[
        'Two cases. $x+7=9$, so $x=2$. Or $x+7=-9$, so $x=-16$.',
        'Only $-16$ is among the choices. Check: $|-16+7|=|-9|=9$ ✓.',
        'Choice 2 ($-2$) is a trap: it is not $2$.'])
    video('q-359', {2: [
        "Absolute value equation? Split it in two.",
        "The inside equals nine — or the inside equals negative nine. Either way, the bars give nine.",
        D('Write "x + 7 = 9 → x = 2"'),
        "First case: x plus seven equals nine. x is two.",
        D('Write "x + 7 = −9 → x = −16"'),
        "Second case: x plus seven equals negative nine. x is negative sixteen.",
        "Now the choices. Is two there? No. Negative two is there — careful, that's a trap. Not the same number.",
        D('Circle choice 3'),
        "Negative sixteen is choice three.",
        "Look at the wording: which could be the value of x. Two values work — two and negative sixteen. Only one of them is offered.",
        D('Next to it write "|−16 + 7| = |−9| = 9 ✓"'),
        "Quick check: negative sixteen plus seven is negative nine. Absolute value: nine. ✓"]})

    # q-360: |x + 5| < 8 -> 2   =>   |x + 3| < 7 -> 3 (key 3; trap 5 fits |x| < 7 but not the range)
    S('q-360', stem='Given: $|x+3|<7$. Which of the following could be the value of $x$?',
      choices=['$5$', '$-25$', '$3$', '$11$'], correct=3, expl=[
        'The bars are on the small side, so $x+3$ is between $-7$ and $7$: $-7<x+3<7$.',
        'Subtract $3$ from all three parts: $-10<x<4$.',
        'Only $3$ is in this range ($5$ and $11$ are too big, and $-25$ is too small). Check: $|3+3|=6<7$ ✓.',
        'With the distance picture: $|x+3|=|x-(-3)|$ is the distance from $x$ to $-3$. Less than $7$ from $-3$ means from $-10$ to $4$.'])
    video('q-360', {2: [
        "Where's the absolute value? On the SMALL side of the inequality.",
        "Small side means a closed range — x is trapped between two numbers.",
        D('Write "−7 < x + 3 < 7"'),
        "Put the seven on the right, and negative seven on the left.",
        D('Subtract 3 from all three parts: "−10 < x < 4"'),
        "Take three off everywhere. x is between negative ten and four.",
        "Now scan the choices. Three — inside the range. Five and eleven — too big. Negative twenty-five — too small.",
        D('Cross out choices 1, 2 and 4; circle choice 3'),
        "Only one choice fits. Choice three.",
        D('Next to it write "|3 + 3| = 6 < 7 ✓"'),
        "Check: three plus three is six, and six is less than seven. ✓",
        "Another way to see it — a distance picture. x plus three is x minus negative three.",
        D('Draw a number line: a dot at −3, arrows of 7 to −10 and to 4'),
        "So x is less than seven steps from negative three. Seven steps left: negative ten. Seven steps right: four."]})

    # q-361: 6 < |x + 3| cannot -> 2   =>   5 < |x + 2| cannot -> 1 (key 2; trap 5 fails |x| > 5 but fits)
    S('q-361', stem='Given: $5<|x+2|$. Which of the following cannot be the value of $x$?',
      choices=['$7$', '$1$', '$-8$', '$5$'], correct=2, expl=[
        'The bars are on the big side, so there are two cases. $x+2>5$, so $x>3$. Or $x+2<-5$, so $x<-7$.',
        '$7$ and $5$ are greater than $3$ ✓, and $-8$ is less than $-7$ ✓.',
        '$1$ is in neither range: $|1+2|=3$, and $3$ is not greater than $5$. So $x$ cannot be $1$.'])
    video('q-361', {2: [
        "The absolute value is on the BIG side. So the range is open — two separate cases.",
        D('Write "x + 2 > 5 → x > 3"'),
        "Either the inside is bigger than five — x is bigger than three.",
        D('Write "x + 2 < −5 → x < −7"'),
        "Or the inside is smaller than negative five — x is smaller than negative seven.",
        "They ask what x CANNOT be. So find the one that fits neither range.",
        D('Tick choices 1 and 4 (above 3) and choice 3 (below −7)'),
        "Seven — above three, fine. Five — above three, fine. Negative eight — below negative seven, fine.",
        D('Circle choice 2'),
        "One? It's not above three, and it's not below negative seven. It's stuck in the forbidden middle. Choice two.",
        "Check: one plus two is three — and three is not bigger than five.",
        "The distance picture says the same. x plus two: the distance from negative two.",
        D('Draw a number line: a dot at −2, marks at −7 and 3, shade outside them'),
        "More than five steps from negative two: beyond three, or below negative seven. One is only three steps away."]})

    # q-362: x < 0, 5 + 2x/|x| = 3   =>   10 + 4x/|x| = 6 (key 2; the first plug-in ties with -x)
    S('q-362', stem='Given: $x<0$. What is $10+\\frac{4x}{|x|}$?',
      choices=['$14$', '$6$', '$-x$', '$10-x$'], correct=2, expl=[
        '$x<0$, so $|x|=-x$.',
        '$\\frac{4x}{|x|}=\\frac{4x}{-x}=-4$ for every negative $x$.',
        'So $10+\\frac{4x}{|x|}=10-4=6$.',
        'Plugging in: $x=-2$ gives $10+\\frac{-8}{2}=6$. The choices at $x=-2$: $14$, $6$, $-x=2$ and $10-x=12$. Only choice 2 gives $6$.'])
    video('q-362', {
        2: ["It's an expression. So we're allowed to plug in a number. x just has to be negative.",
            D('Write "x = −6"'),
            "Take x equals negative six. Any negative number works — just not zero, one or minus one.",
            D('Write "10 + 4(−6)/|−6| = 10 + (−24)/6 = 10 − 4 = 6"'),
            "Four times negative six is negative twenty-four. Over six: negative four. Ten minus four — six.",
            D('Next to the choices write their values: 14, 6, 6, 16'),
            "Now the choices at x equals negative six. Fourteen — no. Six — yes. Negative x is… six. Yes too! Ten minus x is sixteen — no.",
            "Two survive. With other numbers, one plug-in would have killed three choices. Here negative six happens to make negative x equal six.",
            "So plug in again — a different negative.",
            D('Write "x = −2: 10 + (−8)/2 = 6"'),
            "x equals negative two: ten plus negative eight over two. Six again.",
            D('Next to choice 3 write "−x = 2 ✗" and circle choice 2'),
            "But negative x is now two. Out. Choice two."],
        3: ["The algebra is short too.",
            D('Write "x < 0 → |x| = −x"'),
            "x is negative. So its absolute value is negative x.",
            D('Write "4x / (−x) = −4"'),
            "Four x over negative x — the x's cancel. Negative four, whatever the negative number is.",
            "A useful fact: x over its absolute value is one for every positive x — and minus one for every negative x.",
            D('Write "10 − 4 = 6" and circle choice 2'),
            "Ten minus four: six. And that's why choices with an x in them can't be right — the x disappears. Choice two."]})

    # ============================== advanced guided questions (section 2)
    # q-363: |b| = a, b != a, 3c = a -> b < c < a   =>   |n| = m, n != m, 4k = m -> n < k < m (key 2)
    S('q-363', stem='Given:\n$\\begin{cases} |n|=m \\\\ n\\ne m \\\\ 4k=m \\end{cases}$\nWhich of the following is necessarily true?',
      choices=['$m<k<n$', '$n<k<m$', '$n<m<k$', '$k<n<m$'], correct=2, expl=[
        '$|n|=m$, so $n=m$ or $n=-m$. Since $n\\ne m$, $n=-m$.',
        '$m=|n|\\ge0$. If $m=0$, then $n=0=m$, which is not allowed. So $m>0$ and $n=-m<0$.',
        '$k=\\frac{m}{4}$: positive, but smaller than $m$. So $0<k<m$.',
        'The order is $n<k<m$. With numbers: $m=4$, $n=-4$, $k=1$.'])
    video('q-363', {
        2: ["Two approaches today: understanding first, then plugging in numbers.",
            "Given one: the absolute value of n equals m. Same distance from zero.",
            "Given two: but n and m are NOT equal.",
            D('Under the question write "|n| = m → m ≥ 0"'),
            "An absolute value is never negative. So m is zero or positive.",
            "Could m be zero? Then n is zero too — and they'd be equal. Not allowed.",
            D('Write "m > 0, n < 0"'),
            "So m is positive, and n is the negative number the same distance from zero.",
            D('Draw a number line: n left of 0, m right of 0, same distance'),
            "Given three: four k equals m. So k is a quarter of m.",
            D('Mark k between 0 and m'),
            "m is positive. So k is positive too, but smaller. It sits between zero and m.",
            "Biggest: m. Smallest: n. In the middle: k.",
            D('Circle choice 2'),
            "n, then k, then m. Choice two."],
        3: ["Now plug in numbers that obey every given.",
            D('Write "m = 4, n = 4"'),
            "Try m four, n four. The absolute value of n is m — fine.",
            "But they have to be different. Bad substitution. So change it.",
            D('Change it to "m = 4, n = −4"'),
            "n negative four. Absolute value four, equals m — and they're different. Now both givens work.",
            D('Write "4k = 4 → k = 1"'),
            "Four k equals four — k is one.",
            D('Circle choice 2'),
            "Negative four, one, four: n, k, m. Choice two again.",
            "Which way is better? I prefer understanding — but plugging in is an excellent backup."]})

    # q-364: p < q < 0 < r < s -> |q| < |p|   =>   a < b < 0 < c < d -> |b| < |a| (key 2)
    S('q-364', stem='Given: $a<b<0<c<d$. Which of the following is necessarily true?',
      choices=['$\\left|c\\right| < \\left|a\\right|$', '$\\left|b\\right| < \\left|a\\right|$',
               '$\\left|a\\right| < \\left|d\\right|$', '$\\left|b\\right| < \\left|d\\right|$'], correct=2, expl=[
        'The absolute value is the distance from $0$. $a$ and $b$ are both negative, and $a$ is farther left. So $a$ is farther from $0$: $|b|<|a|$ always.',
        'The other choices compare a negative number with a positive one, and the givens say nothing about that.',
        '$a=-3$, $b=-1$, $c=6$, $d=8$: $|c|>|a|$, so choice 1 fails. $a=-20$, $b=-10$, $c=1$, $d=2$: choices 3 and 4 fail.'])
    video('q-364', {2: [
        "Let's place the givens on the number line.",
        D('Draw a number line: a and b left of 0 (a further), c and d right of 0 (d further)'),
        "a and b are negative — a is further from zero. c and d are positive — d is further.",
        "Notice: every answer uses absolute value. Absolute value means distance from zero.",
        "So the question is really: who is further from zero?",
        "Two positives — d is always further than c. We don't know by how much, but always.",
        "Same for the negatives: a is always further than b.",
        "But a negative against a positive? The givens say nothing about that.",
        "Choice one: c against a — positive versus negative. c could be twenty. Out.",
        D('Cross out choice 1'),
        "Choice two compares two negatives. Leave it for the end.",
        D('Next to choice 3 write "a = −2, d = 2 → equal"'),
        "Choice three: a against d. a could be negative two and d two — equal. Or a could be negative twenty — bigger. Not necessarily.",
        D('Cross out choice 3'),
        "Choice four: b against d — again negative versus positive. b could be negative twenty. Out.",
        D('Cross out choice 4'),
        "Three out — on the exam, mark the one that's left and move on.",
        D('Circle choice 2'),
        "Here we'll check it anyway: b and a are both negative, same side of zero. a is further. Always. Choice two."]})

    # q-365: d < c < b, |b| < |c| -> not necessarily b != |b|   =>   z < y < x, |x| < |y| (key 3)
    S('q-365', stem='Given:\n$\\begin{cases} z<y<x \\\\ |x|<|y| \\end{cases}$\nWhich of the following is not necessarily true?',
      choices=['$\\left|y\\right| < \\left|z\\right|$', '$z \\ne  \\left|z\\right|$', '$x \\ne  \\left|x\\right|$',
               '$\\left|x\\right| < \\left|z\\right|$'], correct=3, expl=[
        '$y<x$, but $|y|>|x|$. If $y$ were $0$ or positive, then $x>y\\ge0$ and $|x|>|y|$. So $y<0$.',
        '$z<y<0$, so $z$ is negative too and farther from $0$: $|z|>|y|>|x|$. Choices 1, 2 and 4 are always true.',
        'The sign of $x$ is not fixed. $y=-4$, $z=-5$, $x=2$: all the givens hold, and $x=|x|$. So choice 3 ($x\\ne|x|$) is not necessarily true.'])
    video('q-365', {2: [
        "Given one: z is less than y, which is less than x. We don't know any signs yet.",
        "Given two: the absolute value of x is LESS than the absolute value of y.",
        "Look at that. Without bars, x is bigger than y. With bars, y suddenly jumps above x.",
        D('Under the question write "y < x but |y| > |x| → y < 0"'),
        "Only a negative number changes when you put bars on it. So y must be negative.",
        D('Write "z < y < 0 → z < 0"'),
        "z is even smaller than y. So z is negative too, and further from zero.",
        "And x? The givens can't pin it down. x could be negative, closer to zero than y — or x could be positive, as long as it's closer to zero than y.",
        D('Write "x = −2 or x = 2 (y = −4, z = −5)"'),
        "Example: y negative four, z negative five — x could be negative two, or x could be two.",
        "They want the statement that is NOT necessarily true.",
        "Choice three: x is not equal to its absolute value. That claims x must be negative.",
        "But x could be positive — then x equals its absolute value. Not necessarily true!",
        D('Circle choice 3'),
        "That's our answer — choice three. On the exam, mark it and move on.",
        "Let's check the others anyway — all must be always true.",
        "Choice one: y and z are both negative, z further left. So z is further from zero. Always true.",
        D('Cross out choice 1'),
        "Choice two: z is negative. So z is not equal to its absolute value. Always true.",
        D('Cross out choice 2'),
        "Choice four: z is further from zero than y, and y is further than x. So z is further than x. Always.",
        D('Cross out choice 4'),
        "Choice three it is."]})

    # q-366: 2 < |a + b|, possible but not necessarily -> |a+b| < |a|+|b|   =>   3 < |x + y| (key 2)
    S('q-366', stem='$x$ and $y$ are integers. Given: $3<|x+y|$. Which of the following is possible but not necessarily true?',
      choices=['$9 < {\\left(x + y\\right)}^{2}$', '$\\left|x + y\\right| < \\left|x\\right| + \\left|y\\right|$',
               '$\\left|x \\cdot  y\\right| < \\left|x\\right| \\cdot  \\left|y\\right|$', '$\\left|x + y\\right| < \\left|5\\,x + 5\\,y\\right|$'],
      correct=2, expl=[
        'Choice 1 is always true. Both sides of $3<|x+y|$ are positive, so we may square: $9<|x+y|^2=(x+y)^2$.',
        'Choice 3 is never true: $|x\\cdot y|=|x|\\cdot|y|$ always, so it is never smaller.',
        'Choice 4 is always true: $|5x+5y|=5|x+y|$, and $|x+y|<5|x+y|$ because $|x+y|>0$.',
        'Choice 2 is sometimes true. $x=6$, $y=-2$ gives $4<8$ ✓. But $x=4$, $y=1$ gives $5=5$, not "less than". So it is possible but not necessarily true.'])
    rule = item('solve-q-366', 2, 1, '$|x+y|\\le|x|+|y|$')
    video('q-366', {2: [
        "Read the question carefully: POSSIBLE, but NOT NECESSARILY true.",
        "So anything that's never true — out. Anything that's always true — out.",
        "We want the one that's sometimes true, sometimes not.",
        "Choice one looks like the given — brackets instead of bars, and a square.",
        D('Next to choice 1 write "|x+y| > 3 → |x+y|² > 9"'),
        "The technical way: both sides are positive. So square both sides. Three squared is nine.",
        D('Below it write "|x+y|² = (x+y)²  →  (x+y)² > 9"'),
        "And the absolute value of x plus y, squared, is the same as x plus y squared. A square doesn't care about the sign.",
        "So choice one is always true. Out.",
        D('Cross out choice 1'),
        "And a much simpler way to see it: absolute value behaves like an even power. What's true with bars is true with a square.",
        "Choice two — leave it for the end.",
        "Choice three: the absolute value of x times y.",
        "You can split bars over multiplication: the absolute value of x y IS the absolute value of x times the absolute value of y.",
        D('Next to choice 3 write "|xy| = |x|·|y|"'),
        "Always EQUAL — never less. Never true. Out.",
        D('Cross out choice 3'),
        "Choice four: take out the common factor five inside the bars.",
        D('Next to choice 4 write "|5(x+y)| = 5|x+y|"'),
        "Split the bars: five times the absolute value of x plus y.",
        "So it says: something is less than five times itself. That something is positive — divide it away: one is less than five. Always true. Out.",
        D('Cross out choice 4'),
        "Three out — on the exam, mark two. Here, let's see why it's right.",
        A('The rule appears: |x + y| ≤ |x| + |y|', rule),
        "That's a rule: the absolute value of a sum is less than or EQUAL to the sum of absolute values.",
        D('Write "x = 4, y = 1: 5 = 5"'),
        "Same signs — four and one: five equals five. Equal, not less.",
        D('Write "x = 6, y = −2: 4 < 8"'),
        "Opposite signs — six and negative two: four against eight. Less!",
        D('Circle choice 2'),
        "Sometimes true, sometimes not. Choice two.",
        "Know that rule, and you can mark this one instantly."]})

    # q-367: 3|x| + 6|y| = 27, x + 2|y| = 3 -> -3   =>   4|x| + 12|y| = 44, x + 3|y| = 1 -> -5 (key 2)
    S('q-367', stem='Given:\n$\\begin{cases} 4|x|+12|y|=44 \\\\ x+3|y|=1 \\end{cases}$\nWhat is $x$?',
      choices=['$-2$', '$-5$', '$5$', '$3$'], correct=2, expl=[
        'Divide the first equation by $4$: $|x|+3|y|=11$.',
        'Subtract the second equation: $|x|-x=11-1=10$, so $|x|=10+x$.',
        'Case $x=10+x$: $0=10$, impossible. Case $x=-(10+x)$: $2x=-10$, so $x=-5$.',
        'Check: $|-5|=5=10+(-5)$ ✓. Then $3|y|=1-(-5)=6$, so $|y|=2$, and $4\\cdot5+12\\cdot2=44$ ✓.'])
    video('q-367', {
        2: ["Method one: full algebra.",
            D('Under the first equation write "÷4: |x| + 3|y| = 11"'),
            "The first equation can be divided by four: absolute x plus three absolute y equals eleven.",
            "They want x. So we need to get rid of y. Subtract the equations.",
            D('Write "|x| − x = 11 − 1 = 10"'),
            "Three absolute y cancels. Absolute x minus x equals ten.",
            D('Write "|x| = 10 + x"'),
            "Move the x across: absolute x equals ten plus x.",
            "An absolute-value equation has two options: the sides are equal, or one is the opposite of the other.",
            D('Write "x = 10 + x → 0 = 10 ✗"'),
            "Option one: x equals ten plus x. Zero equals ten. False — no solution here.",
            D('Write "x = −(10 + x) → 2x = −10 → x = −5"'),
            "Option two: x equals minus ten minus x. Two x is negative ten. x is negative five.",
            "A letter on the right side. So check it. Ten plus negative five is five. Not negative. It works.",
            D('Circle choice 2'),
            "Choice two."],
        3: ["Method two: same algebra — until we reach the absolute-value equation.",
            D('Write "|x| = 10 + x"'),
            "Then, instead of solving it — plug in the answers. They're all numbers.",
            D('Next to choice 1 write "2 = 8? ✗"'),
            "x equals negative two: absolute value two. Ten plus negative two is eight. No.",
            D('Next to choice 2 write "5 = 5 ✓"'),
            "x equals negative five: absolute value five. Ten plus negative five: five. Yes!",
            D('Circle choice 2'),
            "Much quicker at that stage than finishing the algebra."],
        4: ["Method three: plug in the answers from the very start.",
            D('Next to choice 1 write "x = −2: −2 + 3|y| = 1 → |y| = 1"'),
            "Choice one, x equals negative two. Into the second equation: negative two plus three absolute y equals one. Absolute y is one.",
            D('Write "4·2 + 12·1 = 20 ≠ 44 ✗"'),
            "Check the first equation: eight plus twelve is twenty. Not forty-four. Out.",
            D('Next to choice 2 write "x = −5: −5 + 3|y| = 1 → |y| = 2"'),
            "Choice two, x is negative five. Negative five plus three absolute y equals one — absolute y is two.",
            D('Write "4·5 + 12·2 = 44 ✓"'),
            "First equation: twenty plus twenty-four — forty-four. It works!",
            D('Circle choice 2'),
            "Choice two. My picks: the shortened algebra, or plugging in the answers right away."]})

    # q-368: |x + 3y| = |3x + y| -> |x| = |y|   =>   |x + 4y| = |4x + y| (key 3)
    S('q-368', stem='Given: $|x+4y|=|4x+y|$. Which of the following is necessarily true?',
      choices=['$y < x$', '$x = y$', '$\\left|x\\right| = \\left|y\\right|$', '$x < y$'], correct=3, expl=[
        'Equal absolute values: the insides are equal or opposite.',
        'Equal: $x+4y=4x+y$, so $3y=3x$ and $x=y$.',
        'Opposite: $x+4y=-(4x+y)$, so $5x+5y=0$ and $x=-y$.',
        'In both cases $|x|=|y|$. But $x=y$ is not necessary: $x=2$, $y=-2$ gives $|-6|=|6|$ ✓ with $x\\ne y$.'])
    sq = item('solve-q-368', 3, 1)
    video('q-368', {
        2: ["An absolute-value equation: either the insides are equal, or one is the opposite of the other.",
            D('Write "x + 4y = 4x + y → y = x"'),
            "Option one: equal. Move terms across — y equals x.",
            D('Write "x + 4y = −4x − y → 5x = −5y → x = −y"'),
            "Option two: opposite. Open the bracket, move terms — x equals negative y.",
            "So x equals y, or x equals negative y.",
            D('Cross out choice 2'),
            "Choice two, x equals y — only partly true. x could be negative y. Not necessarily.",
            D('Circle choice 3'),
            "Choice three: equal or opposite — either way, same absolute value. Always true. Choice three."],
        3: [A("'Bars on both sides → square both sides' appears", sq),
            "A tool for bars on both sides: both sides are zero or positive. So we may square both sides. After squaring, the bars are gone.",
            D('Write "(x + 4y)² = (4x + y)²"'),
            D('Write "x² + 8xy + 16y² = 16x² + 8xy + y²"'),
            "Open with the first shortcut formula.",
            D('Cross out the two 8xy terms'),
            "Eight x y on both sides — cancel it.",
            D('Write "15y² = 15x² → y² = x²"'),
            "Move terms and divide by fifteen: y squared equals x squared.",
            "Remember: absolute value and an even power are basically the same. True with squares — true with bars.",
            D('Circle choice 3'),
            "Absolute x equals absolute y. Choice three."],
        4: ["Plugging in here isn't obvious — but it's the shortest.",
            D('Write "x = y = 2: |10| = |10| ✓"'),
            "Equal numbers — x two, y two. Ten on both sides. Works.",
            D('Cross out choices 1 and 4'),
            "So y less than x — no. x less than y — no. Choices one and four are out.",
            "Two and three both survive. The answers hint: equal, or equal in absolute value. Let's split them.",
            D('Write "x = 2, y = −2: |−6| = |6| ✓"'),
            "Opposite numbers: two and negative two. Absolute six equals absolute six. Works!",
            D('Cross out choice 2 and circle choice 3'),
            "So they don't have to be equal. Choice three.",
            "And the mirror test sees part of it with no numbers: swap x and y — the given doesn't change. y less than x turns into x less than y. Choices one and four are out.",
            "Three approaches. The third is hardest to spot — but shortest. Pick what suits you."]})

    # q-369: 11 < |2x + 1| < 13 -> -7 < x < -6   =>   7 < |2x - 1| < 9 -> -4 < x < -3 (key 3; traps: wrong-way +-1)
    S('q-369', stem='Given: $7<|2x-1|<9$. Which of the following ranges is possible for $x$?',
      choices=['$3 < x < 4$', '$5 < x < 6$', '$-4 < x < -3$', '$-5 < x < -4$'], correct=3, expl=[
        'Positive inside: $7<2x-1<9$. Add $1$: $8<2x<10$. Divide by $2$: $4<x<5$.',
        'Negative inside: $-9<2x-1<-7$. Add $1$: $-8<2x<-6$. Divide by $2$: $-4<x<-3$.',
        'Only $-4<x<-3$ is among the choices. Check $x=-3.5$: $|2\\cdot(-3.5)-1|=|-8|=8$ ✓.',
        'Choice 1 ($3<x<4$) is what you get if you subtract $1$ instead of adding it.'])
    video('q-369', {
        2: ["We've seen absolute-value inequalities before. A double one has an elegant route.",
            D('Draw a number line: shade 7 to 9 and −9 to −7'),
            "Two x minus one, in bars. If it's positive, it's between seven and nine. If negative — symmetrically, between negative nine and negative seven.",
            D('Write "7 < 2x − 1 < 9"'),
            "Positive band first. The unknown is in the middle — work on all three parts.",
            D('Write "8 < 2x < 10 → 4 < x < 5"'),
            "Add one: eight to ten. Halve: x between four and five.",
            "Peek at the choices — it isn't there. So on to the negative band.",
            D('Write "−9 < 2x − 1 < −7 → −8 < 2x < −6 → −4 < x < −3"'),
            "Negative nine to negative seven. Add one, halve: x between negative four and negative three.",
            D('Circle choice 3'),
            "Choice three.",
            "Three to four is the bait. That's what you get if you SUBTRACT the one instead of adding it."],
        3: ["Or — trial and error. Pick a convenient number inside each range.",
            D('Next to choice 1 write "x = 3.5: |6| = 6 ✗"'),
            "Choice one: three and a half. Two times it is seven, minus one — six. Not more than seven. Out.",
            D('Next to choice 2 write "x = 5.5: |10| = 10 ✗"'),
            "Choice two: five and a half. Eleven minus one — ten. Not less than nine. Out.",
            D('Next to choice 3 write "x = −3.5: |−8| = 8 ✓"'),
            "Choice three: negative three and a half. Negative seven minus one — negative eight. Absolute value eight. Between seven and nine!",
            D('Circle choice 3'),
            "Possible — choice three. No doubt: this way is much shorter."]})

    # q-370: x + |x| < 14 -> x < 7   =>   x + |x| < 12 -> x < 6 (key 3)
    S('q-370', stem='Given: $x+|x|<12$. What is the most precise domain for $x$?',
      choices=['$-6 < x < 6$', '$x < 0$', '$x < 6$', '$0 < x$'], correct=3, expl=[
        'Case $x\\ge0$: $|x|=x$, so $2x<12$ and $x<6$. This gives $0\\le x<6$.',
        'Case $x<0$: $|x|=-x$, so $x+|x|=x-x=0$, and $0<12$ is always true. Every negative $x$ works.',
        'Together: $x<6$.'])
    video('q-370', {
        2: ["As usual with absolute value — two cases.",
            "Case one: x is positive or zero. Then the bars do nothing.",
            D('Write "x ≥ 0: 2x < 12 → x < 6"'),
            "x plus x is less than twelve. Two x under twelve — x under six.",
            "Case two: x is negative.",
            D('Write "x = −4: −4 + 4 = 0"'),
            "Then the bars turn it into its opposite. Negative four plus four — zero. Negative one plus one — zero. Always zero.",
            D('Write "x < 0: 0 < 12 ✓ always"'),
            "Zero is less than twelve — always true. Every negative number works.",
            "So: every negative number, and positives only below six.",
            D('Circle choice 3'),
            "x less than six. Choice three."],
        3: ["Now plug numbers into the choices.",
            D('Next to choice 4 write "x = 1: 2 < 12 ✓, x = 10: 20 ✗"'),
            "Choice four says every positive works. One: two, fine. But ten: twenty — not less than twelve. Out.",
            D('Cross out choice 4'),
            "Choice two says only negatives. But one worked. So not only negatives. Out.",
            D('Cross out choice 2'),
            "One and three both stop at six on top. The difference is the bottom: negative six, or no limit.",
            D('Write "x = −10: −10 + 10 = 0 < 12 ✓"'),
            "A smart substitution to split them: negative ten. Zero — less than twelve. It works!",
            D('Cross out choice 1 and circle choice 3'),
            "So x doesn't stop at negative six. Choice three.",
            "Both approaches are excellent — pick what suits you."]})

    # ============================== practice (Hebrew study-guide questions)
    S('q-371', stem='Given:\n$\\begin{cases} q\\ne0 \\\\ |p+q|=|p-q| \\end{cases}$\nWhat is $p$?',
      choices=['$2\\,q$', '$0$', '$-q$', '$\\frac{-q}{2}$'], correct=2, expl=[
        'Equal absolute values: the insides are equal or opposite.',
        'Equal: $p+q=p-q$, so $2q=0$ and $q=0$. Not allowed, because $q\\ne0$.',
        'Opposite: $p+q=-(p-q)=-p+q$, so $2p=0$ and $p=0$.',
        'Check with $q=4$: $|0+4|=|0-4|=4$ ✓.'])
    S('q-372', stem='Given: $|x+4|<|x-4|$. Which of the following numbers satisfies the inequality?',
      choices=['$\\frac{1}{4}$', '$4$', '$-5$', '$0$'], correct=3, expl=[
        '$|x+4|=|x-(-4)|$ is the distance from $x$ to $-4$. $|x-4|$ is the distance from $x$ to $4$.',
        'So $x$ is closer to $-4$ than to $4$. The point in the middle is $0$, so $x<0$.',
        'Check $x=-5$: $|-1|=1$ and $|-9|=9$, and $1<9$ ✓.',
        'The others fail: $x=0$ gives $4<4$ ✗. $x=4$ gives $8<0$ ✗. $x=\\frac14$ gives $4.25<3.75$ ✗.'])
    S('q-373', stem='Given:\n$\\begin{cases} a>0 \\\\ b<0 \\end{cases}$\nWhat is $|a\\cdot b|$?',
      choices=['$b \\cdot  \\left|a\\right|$', '$a \\cdot  b$', '$a \\cdot  \\left|b\\right|$', '$-a \\cdot  \\left|b\\right|$'], correct=3, expl=[
        '$a\\cdot b$ is negative (positive times negative), so $|a\\cdot b|=-a\\cdot b$.',
        'Choice 3: $b<0$, so $|b|=-b$, and $a\\cdot|b|=a\\cdot(-b)=-a\\cdot b$. A match.',
        'Or plug in $a=3$, $b=-4$: $|a\\cdot b|=12$. Choice 1: $-4\\cdot3=-12$. Choice 2: $-12$. Choice 3: $3\\cdot4=12$ ✓. Choice 4: $-3\\cdot4=-12$.'])
    S('q-374', stem='Given: $|m+n|=|m-n|$. What is $m\\cdot n$?',
      choices=['$2$', '$0$', '$1$', 'It cannot be determined from the information given.'], correct=2, expl=[
        'Both sides are zero or positive, so we may square both sides: $(m+n)^2=(m-n)^2$.',
        'Expand: $m^2+2mn+n^2=m^2-2mn+n^2$, so $4mn=0$ and $m\\cdot n=0$.',
        'Check: $m=0$, $n=6$: $|6|=|-6|$ ✓.'])
    q = M.q('q-375'); extra = list(q['explanation'][3:])   # practice_methods line, rewritten below
    S('q-375', stem='$x$ is a negative number. Given:\n$\\begin{cases} |x|+3=y \\\\ y>10 \\end{cases}$\nWhat is the most precise range for $x$?',
      choices=['$-13 < x < 0$', '$x < -7$', '$x < -13$', '$-7 < x < 0$'], correct=2, expl=[
        'Put $y$ into the inequality: $|x|+3>10$, so $|x|>7$.',
        '$x$ is negative, so $|x|=-x$. Then $-x>7$, so $x<-7$.',
        'Check: $x=-8$ gives $y=11>10$ ✓. $x=-6$ gives $y=9$ ✗.',
        'Method 2 · The most precise range: $x=-8$ works ($y=11>10$), so choices 3 and 4 (which leave $-8$ out) are out. '
        '$x=-20$ works too ($y=23$), so choice 1 (which stops at $-13$) is out. The answer is choice 2.'])
    assert len(extra) == 1 and extra[0].startswith('Method 2'), extra
    S('q-376', stem='Given: $a^n\\ne|a|^n$, where $n$ is an integer. Which of the following is necessarily true?',
      choices=['$a>0$ or $n$ is even', '$a<0$ and $n<0$', '$a>0$ or $n<0$', '$a<0$ and $n$ is odd'], correct=4, expl=[
        'If $a\\ge0$, then $|a|=a$ and the two powers are equal. So $a<0$.',
        'If $a<0$ and $n$ is even, the even power hides the sign: $(-3)^2=9=|-3|^2$. So $n$ is odd.',
        'Check: $a=-3$, $n=3$: $(-3)^3=-27$, but $|-3|^3=27$ ✓. Choice 2 is not necessary: here $n=3$ is positive.'])
    S('q-377', stem='Given:\n$\\begin{cases} x<-3 \\\\ |x|=|y| \\end{cases}$\nWhich of the following is necessarily true?',
      choices=['$x + y = 0$', '$-3 < y$', '$9 < {y}^{2}$', '$\\frac{x}{y} = 1$'], correct=3, expl=[
        '$x<-3$, so $|x|>3$. Then $|y|=|x|>3$, and $y^2=|y|^2>9$. Choice 3 is always true.',
        '$y$ can be $x$ or $-x$. Take $x=-4$.',
        '$y=-4$: then $x+y=-8$ (choice 1 fails), and $y<-3$ (choice 2 fails).',
        '$y=4$: then $\\frac{x}{y}=-1$ (choice 4 fails).'])
    S('q-378', stem='Given:\n$\\begin{cases} |x|\\ne x \\\\ |-3x|\\ne-3x \\end{cases}$\nWhat is $x$?',
      choices=['$\\frac13$', '$0$', '$-\\frac13$', 'No number $x$ satisfies the conditions.'], correct=4, expl=[
        '$|x|\\ne x$ only when $x<0$.',
        '$|-3x|\\ne-3x$ only when $-3x<0$, so $x>0$.',
        'No number is both negative and positive. No number satisfies the conditions.',
        'For example, $x=-\\frac13$ gives $-3x=1$ and $|1|=1$, so the second condition fails.'])
    S('q-379', stem='Given: $(x-y)^2<9$. Which of the following is necessarily true?',
      choices=['$9 < {\\left(x + y\\right)}^{2}$', '$3 < \\left|x - y\\right|$', '$\\left|x - y\\right| < 3$', '${\\left(x + y\\right)}^{2} < 9$'],
      correct=3, expl=[
        '$(x-y)^2=|x-y|^2$. Both sides of $|x-y|^2<9$ are zero or positive, so take the root: $|x-y|<3$. Choice 2 is the opposite, so it is never true.',
        'The sum $x+y$ can be anything. $x=y=50$: $(x-y)^2=0<9$, but $(x+y)^2=10{,}000$, so choice 4 fails. $x=y=0$: $(x+y)^2=0$, so choice 1 fails.'])
    S('q-380', stem='Given:\n$\\begin{cases} |6x+9|=21 \\\\ |2x+3|=-2x-3 \\end{cases}$\nWhat is $x$?',
      choices=['$2$', '$-5$', '$5$', '$-2$'], correct=2, expl=[
        'First equation: $6x+9=21$, so $x=2$. Or $6x+9=-21$, so $x=-5$.',
        'Second equation: the right side is $-(2x+3)$. $|A|=-A$ only when $A\\le0$. So $2x+3\\le0$, and $x\\le-\\frac32$.',
        'Only $x=-5$ fits. Check: $|6\\cdot(-5)+9|=|-21|=21$ ✓ and $|2\\cdot(-5)+3|=|-7|=7=-2\\cdot(-5)-3$ ✓.'])
    S('q-381', stem='Given:\n$\\begin{cases} s\\cdot t<0 \\\\ \\frac{s}{t}<\\frac{t}{s} \\end{cases}$\nWhich of the following is necessarily true?',
      choices=['$s + t < 0$', '$t < 0 < s$', '$\\left|t\\right| < \\left|s\\right|$', '$0 < s + t$'], correct=3, expl=[
        'Move everything to one side: $\\frac{s}{t}-\\frac{t}{s}<0$, so $\\frac{s^2-t^2}{s\\cdot t}<0$.',
        'The bottom $s\\cdot t$ is negative. A fraction with a negative bottom is negative only when its top is positive: $s^2-t^2>0$.',
        'So $s^2>t^2$, which means $|s|>|t|$.',
        'Choices 1, 2 and 4 are not necessary. $s=-4$, $t=1$: $-4<-\\frac14$ ✓, but $t<0<s$ fails, and $s+t=-3$ (choice 4 fails). '
        '$s=4$, $t=-1$: $-4<-\\frac14$ ✓, and $s+t=3$ (choice 1 fails).',
        'Method 2 · Mirror test: flip all signs. $(-s)(-t)=s\\cdot t$ and $\\frac{-s}{-t}=\\frac st$, so the given stays the same.',
        'Choice 1 ($s+t<0$) turns into $0<s+t$, choice 2 ($t<0<s$) into $s<0<t$, and choice 4 ($0<s+t$) into $s+t<0$. '
        'All three turn into their opposites, so they are out. Choice 3 ($|t|<|s|$) does not change: it is the answer.'])
    S('q-382', stem='Given:\n$\\begin{cases} x\\ne y \\\\ x-y=|x+y| \\end{cases}$\nWhich of the following is necessarily true?',
      choices=['$x=-y$', '$x>0$ and $y>0$', '$x<0$ and $y<0$', '$x=0$ or $y=0$'], correct=4, expl=[
        'Case $x+y\\ge0$: $x-y=x+y$, so $2y=0$ and $y=0$.',
        'Case $x+y<0$: $x-y=-(x+y)=-x-y$, so $2x=0$ and $x=0$.',
        'Either way, $x=0$ or $y=0$.',
        'Check: $x=6$, $y=0$: $6-0=6=|6|$ ✓. This example also rules out choices 1, 2 and 3.'])
    S('q-383', stem='$x$ is an integer. Given: $|x+8|<5$. How many different values can $x$ have?',
      choices=['$10$', '$6$', '$9$', '$8$'], correct=3, expl=[
        '$-5<x+8<5$. Subtract $8$: $-13<x<-3$.',
        'The integers: $-12$, $-11$, $-10$, $-9$, $-8$, $-7$, $-6$, $-5$, $-4$. That is $9$ values.',
        'With the distance picture: less than $5$ from $-8$. The ends $-13$ and $-3$ are not included.'])
    S('q-384', stem='In which of the following cases is $|m|+|n|=|m+n|$ not necessarily true?',
      choices=['$m$ and $n$ are both negative', '$m$ and $n$ are integers', '$n=0$ or $m=0$', '$m$ and $n$ are both positive'], correct=2, expl=[
        '$|m+n|=|m|+|n|$ when $m$ and $n$ do not have opposite signs.',
        'Both positive ✓, both negative ✓, one of them $0$ ✓. In these cases it is always true.',
        '"Integers" says nothing about the signs: $m=5$, $n=-2$ gives $|5|+|-2|=7$, but $|5+(-2)|=3$. So choice 2.'])
    S('q-385', stem='Given: $a<b<|a\\cdot b\\cdot c|<c$. Which of the following is necessarily true?',
      choices=['$a < 0$', '$1 < c$', '$\\left|a \\cdot  b\\right| < 1$', '$\\left|a\\right| < \\left|c\\right|$'], correct=3, expl=[
        '$|a\\cdot b\\cdot c|\\ge0$ and $|a\\cdot b\\cdot c|<c$, so $c>0$ and $|c|=c$.',
        '$|a\\cdot b\\cdot c|=|a\\cdot b|\\cdot c<c$. Divide by the positive $c$: $|a\\cdot b|<1$.',
        'The others are not necessary. $a=-0.8$, $b=-0.5$, $c=0.4$: $|a\\cdot b\\cdot c|=0.16$, and $-0.8<-0.5<0.16<0.4$. Here $c<1$ (choice 2 fails) and $|a|>|c|$ (choice 4 fails).',
        '$a=0.02$, $b=0.03$, $c=100$: $|a\\cdot b\\cdot c|=0.06$, and $0.02<0.03<0.06<100$. Here $a>0$ (choice 1 fails).'])

    # ============================== practice clean-up (30 -> 20) and order easy -> hard
    E = 'alg-extra-unit-t13-3-%d'
    # extra warm-ups: keep 3 (|3 - 8|, |x| < 3, |x| = -x). Removed: |x - 3| = 5 sum (Questions 2, 6), x < 0: |x| - x
    # (Question 5), min |x - 3| + |x - 5| (q-r26-t13-10 keeps the distance-sum type), integers in |x - 3| <= 2 (q-383).
    # September items: keep q-r26-t13-10 (sum of distances) and -11 (bars <= 0) - types the Hebrew practice lacks.
    # Removed: -05 (true for every x; Question 7), -07 (x/|x|; Question 5), -08 (|2 - x| + |x|; q-373 type),
    # -09 (letter on the right; q-380), -12 (|x| = -x, |y| = y; q-378), -14 (|a - b| = |a| + |b|; q-384, mirror in q-381).
    for r in [E % 2, E % 3, E % 5, E % 7, qid(5), qid(7), qid(8), qid(9), qid(12), qid(14)]:
        M.unplace(r)
    M.practice_order(PRACT, [E % 1, E % 4, E % 6, qid(11), 'q-383', 'q-375', 'q-373', 'q-371', 'q-374', 'q-378',
                             'q-379', 'q-372', 'q-380', 'q-377', qid(10), 'q-376', 'q-384', 'q-382', 'q-381', 'q-385'])

    # video titles and canvas notes follow the new stems
    for vid, v in M.D['videos'].items():
        if v['topic'] != TOPIC or v.get('kind') != 'solution' or not v.get('questionId'): continue
        q = M.q(v['questionId'])
        v['title'] = v['navLabel'] = q['stem']
        for b in v['beats']:
            if (b.get('canvas') or '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (q['id'], q['stem'])
        M.touched_videos.add(vid)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber(M)   # 2026-10-06 renumber pass: runs last


# =====================================================================================================================
# 2026-10-06 Hebrew back-check: the renumbered questions / examples were compared with the teacher's HEBREW VIDEO
# subtitles (01-Algebra-Original-Subtitles.txt, lines 11081-13680). Where a new version had landed back on the Hebrew
# video's own numbers / letters / story, it gets new ones here (same type, trap, difficulty and methods).
# Nothing in topic 13 is recorded. Runs last. See t13_CHANGES.md ("2026-10-06 Hebrew back-check").
# =====================================================================================================================
def hebrew_backcheck(M):
    def S(qid_, **kw):
        q = M.set_q(qid_, **kw)
        v = M.video('solve-' + qid_)
        v['title'] = v['navLabel'] = q['stem']
        for b in v['beats']:
            if (b.get('canvas') or '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (q['id'], q['stem'])
        M.touched_videos.add(v['id'])

    # lesson: |8| = 8 and the "friend's house" distance story were the Hebrew lesson's own -> |11| = 11, bus stop
    _dd_sub(M, LESSON, 2, [("The way to my friend's house isn't minus two kilometers. It's two kilometers.",
                            "The walk to the bus stop isn't minus two kilometers. It's two kilometers.")])
    _dd_sub(M, LESSON, 3, [('$|8|=8$', '$|11|=11$'), ('|8| = 8 appears', '|11| = 11 appears'),
                           ('Eight is eight units from zero.', 'Eleven is eleven units from zero.')])

    # q-361: 5 < |x + 2| (x > 3 or x < -7; choices 7, 1, -8, 5) = the Hebrew video exactly -> 8 < |x + 1|
    S('q-361', stem='Given: $8<|x+1|$. Which of the following cannot be the value of $x$?',
      choices=['$9$', '$2$', '$-10$', '$11$'], correct=2, expl=[
        'The bars are on the big side, so there are two cases. $x+1>8$, so $x>7$. Or $x+1<-8$, so $x<-9$.',
        '$9$ and $11$ are greater than $7$ ✓, and $-10$ is less than $-9$ ✓.',
        '$2$ is in neither range: $|2+1|=3$, and $3$ is not greater than $8$. So $x$ cannot be $2$.'])
    M.set_slide('solve-q-361', 2, script=[
        "The absolute value is on the BIG side. So the range is open — two separate cases.",
        D('Write "x + 1 > 8 → x > 7"'),
        "Either the inside is bigger than eight — x is bigger than seven.",
        D('Write "x + 1 < −8 → x < −9"'),
        "Or the inside is smaller than negative eight — x is smaller than negative nine.",
        "They ask what x CANNOT be. So find the one that fits neither range.",
        D('Tick choices 1 and 4 (above 7) and choice 3 (below −9)'),
        "Nine — above seven, fine. Eleven — above seven, fine. Negative ten — below negative nine, fine.",
        D('Circle choice 2'),
        "Two? It's not above seven, and it's not below negative nine. It's stuck in the forbidden middle. Choice two.",
        "Check: two plus one is three — and three is not bigger than eight.",
        "The distance picture says the same. x plus one: the distance from negative one.",
        D('Draw a number line: a dot at −1, marks at −9 and 7, shade outside them'),
        "More than eight steps from negative one: beyond seven, or below negative nine. Two is only three steps away."])

    # q-364: a < b < 0 < c < d (the Hebrew letters and choices; video examples -2/2, -20/20 = the Hebrew video's)
    #        -> p < q < 0 < r < s, examples -5/5 and -40/40
    S('q-364', stem='Given: $p<q<0<r<s$. Which of the following is necessarily true?',
      choices=['$\\left|r\\right| < \\left|p\\right|$', '$\\left|q\\right| < \\left|p\\right|$',
               '$\\left|p\\right| < \\left|s\\right|$', '$\\left|q\\right| < \\left|s\\right|$'], correct=2, expl=[
        'The absolute value is the distance from $0$. $p$ and $q$ are both negative, and $p$ is farther left. So $p$ is farther from $0$: $|q|<|p|$ always.',
        'The other choices compare a negative number with a positive one, and the givens say nothing about that.',
        '$p=-3$, $q=-1$, $r=6$, $s=8$: $|r|>|p|$, so choice 1 fails. $p=-40$, $q=-30$, $r=1$, $s=2$: choices 3 and 4 fail.'])
    M.set_slide('solve-q-364', 2, script=[
        "Let's place the givens on the number line.",
        D('Draw a number line: p and q left of 0 (p further), r and s right of 0 (s further)'),
        "p and q are negative — p is further from zero. r and s are positive — s is further.",
        "Notice: every answer uses absolute value. Absolute value means distance from zero.",
        "So the question is really: who is further from zero?",
        "Two positives — s is always further than r. We don't know by how much, but always.",
        "Same for the negatives: p is always further than q.",
        "But a negative against a positive? The givens say nothing about that.",
        "Choice one: r against p — positive versus negative. r could be forty. Out.",
        D('Cross out choice 1'),
        "Choice two compares two negatives. Leave it for the end.",
        D('Next to choice 3 write "p = −5, s = 5 → equal"'),
        "Choice three: p against s. p could be negative five and s five — equal. Or p could be negative forty — bigger. Not necessarily.",
        D('Cross out choice 3'),
        "Choice four: q against s — again negative versus positive. q could be negative forty. Out.",
        D('Cross out choice 4'),
        "Three out — on the exam, mark the one that's left and move on.",
        D('Circle choice 2'),
        "Here we'll check it anyway: q and p are both negative, same side of zero. p is further. Always. Choice two."])

    # q-370: the video's plug-ins 1, 10, -10 and "negative one plus one" were the Hebrew video's -> 2, 9, -8, -9
    M.set_slide('solve-q-370', 2, script=[
        "As usual with absolute value — two cases.",
        "Case one: x is positive or zero. Then the bars do nothing.",
        D('Write "x ≥ 0: 2x < 12 → x < 6"'),
        "x plus x is less than twelve. Two x under twelve — x under six.",
        "Case two: x is negative.",
        D('Write "x = −4: −4 + 4 = 0"'),
        "Then the bars turn it into its opposite. Negative four plus four — zero. Negative nine plus nine — zero. Always zero.",
        D('Write "x < 0: 0 < 12 ✓ always"'),
        "Zero is less than twelve — always true. Every negative number works.",
        "So: every negative number, and positives only below six.",
        D('Circle choice 3'),
        "x less than six. Choice three."])
    M.set_slide('solve-q-370', 3, script=[
        "Now plug numbers into the choices.",
        D('Next to choice 4 write "x = 2: 4 < 12 ✓, x = 9: 18 ✗"'),
        "Choice four says every positive works. Two: four, fine. But nine: eighteen — not less than twelve. Out.",
        D('Cross out choice 4'),
        "Choice two says only negatives. But two worked. So not only negatives. Out.",
        D('Cross out choice 2'),
        "One and three both stop at six on top. The difference is the bottom: negative six, or no limit.",
        D('Write "x = −8: −8 + 8 = 0 < 12 ✓"'),
        "A smart substitution to split them: negative eight. Zero — less than twelve. It works!",
        D('Cross out choice 1 and circle choice 3'),
        "So x doesn't stop at negative six. Choice three.",
        "Both approaches are excellent — pick what suits you."])


_apply_before_hebrew_backcheck = apply


def apply(M):
    _apply_before_hebrew_backcheck(M)
    hebrew_backcheck(M)   # 2026-10-06 Hebrew back-check: runs last


# ---------------------------------------------------------------- 2026-10-07 pen or click
# Teacher-approved split (2026-10-04/06): lessons - content appears by click, the pen only marks (arc, circle, box,
# cross out, star); solution videos - setup and mechanical lines by click, by hand only the one or two key steps plus
# the marks on the choices (short notes next to a choice count as marks). Drawings (number-line sketches) stay by hand.
# Runs LAST (after renumbering, review, add_methods and hebrew_backcheck), on the final text. No topic 13 video is
# recorded. Helper copied from t10.py (same behaviour).
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


def _gaps(M, vid, n, gap):
    """the board no longer needs the empty rows that were kept for handwriting: close them."""
    for it in M.slide(vid, n)['items']:
        if it.get('k') == 't' and it.get('gap', 0) > gap: it['gap'] = gap


def pen_or_click(M):
    S = 38
    # ---- lesson: Absolute Value (written lines -> clicks; the arcs on the number line, circles, box, cross-out by hand)
    V = LESSON
    _pen_or_click_slide(M, V, 4, {
        'Write "= |−9| = 9"': [A('= |−9| = 9 appears', T(r'$=|-9|=9$', size=60))],
        'Below, write "4 + 13 = 17" and cross it out': [
            A('4 + 13 = 17 appears', T(r'$4+13=17$', size=52)), D('Cross out "4 + 13 = 17"')],
    })
    _gaps(M, V, 4, 24)
    _pen_or_click_slide(M, V, 6, {
        'Under each, write "= 9" and put "=" between them': [
            A('Same signs: 9 = 9 appears', T(r'Same signs: $\ 9=9$', size=46))],
        'Under each, write "= 3" and "= 9", and put "<" between them': [
            A('Different signs: 3 < 9 appears', T(r'Different signs: $\ 3<9$', size=46))],
    })
    _gaps(M, V, 6, 24)
    # ---- Q: q-358 - by hand: y < |y| -> y < 0 (the key), the marks on the choices
    _pen_or_click_slide(M, 'solve-q-358', 2, {
        'Underline "x · y < 0" and write "opposite signs"': [
            D('Underline "x · y < 0"'), A('x · y < 0 → opposite signs appears', T(r'$x\cdot y<0 \;\to\;$ opposite signs', size=S))],
        'Write "→ x > 0"': [A('y < 0 and opposite signs → x > 0 appears', T(r'$y<0$ and opposite signs $\;\to\; x>0$', size=S))],
    })
    # ---- Q: q-359 - by hand: the second case x + 7 = −9, circle
    _pen_or_click_slide(M, 'solve-q-359', 2, {
        'Write "x + 7 = 9 → x = 2"': [A('x + 7 = 9 → x = 2 appears', T(r'$x+7=9 \;\to\; x=2$', size=S))],
        'Next to it write "|−16 + 7| = |−9| = 9 ✓"': [A('check: |−16 + 7| = 9 ✓ appears', T(r'check: $|-16+7|=|-9|=9$ ✓', size=S))],
    }, room=['Write "x + 7 = −9 → x = −16"'], row=70)
    # ---- Q: q-360 - by hand: −7 < x + 3 < 7 (the closed range), marks, the number-line sketch
    _pen_or_click_slide(M, 'solve-q-360', 2, {
        'Subtract 3 from all three parts: "−10 < x < 4"': [A('−10 < x < 4 appears', T(r'$-3$ everywhere: $\ -10<x<4$', size=S))],
        'Next to it write "|3 + 3| = 6 < 7 ✓"': [A('check: |3 + 3| = 6 < 7 ✓ appears', T(r'check: $|3+3|=6<7$ ✓', size=S))],
    }, room=['Write "−7 < x + 3 < 7"'], row=70)
    # ---- Q: q-361 - by hand: the second case x + 1 < −8, ticks, circle, the number-line sketch
    _pen_or_click_slide(M, 'solve-q-361', 2, {
        'Write "x + 1 > 8 → x > 7"': [A('x + 1 > 8 → x > 7 appears', T(r'$x+1>8 \;\to\; x>7$', size=S))],
    })
    # ---- Q: q-362 - by hand: x = −6 (method 1), x < 0 -> |x| = −x (method 2), the values next to the choices, circles
    _pen_or_click_slide(M, 'solve-q-362', 2, {
        'Write "10 + 4(−6)/|−6| = 10 + (−24)/6 = 10 − 4 = 6"': [A('10 + 4(−6)/|−6| = 10 − 4 = 6 appears',
            T(r'$10+\frac{4(-6)}{|-6|}=10+\frac{-24}{6}=10-4=6$', size=S))],
        'Write "x = −2: 10 + (−8)/2 = 6"': [A('x = −2: 10 + (−8)/2 = 6 appears', T(r'$x=-2:\ \ 10+\frac{-8}{2}=6$', size=S))],
    }, room=['Write "x = −6"'], row=70)
    _pen_or_click_slide(M, 'solve-q-362', 3, {
        'Write "4x / (−x) = −4"': [A('4x / (−x) = −4 appears', T(r'$\frac{4x}{-x}=-4$', size=S))],
        'Write "10 − 4 = 6" and circle choice 2': [A('10 − 4 = 6 appears', T(r'$10-4=6$', size=S)), D('Circle choice 2')],
    }, room=['Write "x < 0 → |x| = −x"'], row=70)
    # ---- Q: q-r26-t13-01 - by hand: the second case 2x − 1 = −7, circle
    _pen_or_click_slide(M, 'solve-q-r26-t13-01', 2, {
        'Write "2x − 1 = 7 → 2x = 8 → x = 4"': [A('2x − 1 = 7 → 2x = 8 → x = 4 appears', T(r'$2x-1=7 \;\to\; 2x=8 \;\to\; x=4$', size=S))],
        'Write "|2 · 4 − 1| = 7 ✓   |2 · (−3) − 1| = |−7| = 7 ✓"': [A('check: both work appears',
            T(r'check: $|2\cdot4-1|=7$ ✓ $\qquad |2\cdot(-3)-1|=|-7|=7$ ✓', size=34))],
    }, room=['Write "2x − 1 = −7 → 2x = −6 → x = −3"'], row=70)
    # ---- lesson: Exam Tools (every written line -> click)
    V = TOOLS
    _pen_or_click_slide(M, V, 2, {
        'Write "x = −3: |−3|² = 9, (−3)² = 9"': [A('x = −3: |−3|² = 9, (−3)² = 9 appears', T(r'$x=-3:\ \ |-3|^2=9,\ \ (-3)^2=9$', size=40))],
        'Write "x = −3: √9 = 3 = |−3|"': [A('x = −3: √9 = 3 = |−3| appears', T(r'$x=-3:\ \ \sqrt9=3=|-3|$', size=40))],
        'Write "|2 − 7| = 5 = |7 − 2|"': [A('|2 − 7| = 5 = |7 − 2| appears', T(r'$|2-7|=5=|7-2|$', size=40))],
    })
    _gaps(M, V, 2, 16)
    _pen_or_click_slide(M, V, 3, {
        'Write "|7 − 2| = 5: from 2 to 7 is 5 steps"': [A('|7 − 2| = 5: from 2 to 7 is 5 steps appears', T(r'$|7-2|=5$: from $2$ to $7$ is $5$ steps', size=40))],
        'Write "|x − 3| < 4 → −1 < x < 7"': [A('|x − 3| < 4 → −1 < x < 7 appears', T(r'$|x-3|<4 \;\to\; -1<x<7$', size=40))],
    })
    _gaps(M, V, 3, 16)
    # ---- Q: q-363 - by hand: |n| = m -> m ≥ 0 (method 1), the bad try m = 4, n = 4 and its fix (method 2), the
    #      number-line sketch, marks
    _pen_or_click_slide(M, 'solve-q-363', 2, {
        'Write "m > 0, n < 0"': [A('m > 0, n < 0 appears', T(r'$m>0,\ \ n<0$', size=S))],
    }, room=['Under the question write "|n| = m → m ≥ 0"'], row=70)
    _pen_or_click_slide(M, 'solve-q-363', 3, {
        'Write "4k = 4 → k = 1"': [A('4k = 4 → k = 1 appears', T(r'$4k=4 \;\to\; k=1$', size=S))],
    }, room=['Write "m = 4, n = 4"'], row=70)
    # ---- Q: q-364 - unchanged: the number-line sketch, the counterexample next to choice 3 and the marks stay by hand
    # ---- Q: q-365 - by hand: y < x but |y| > |x| -> y < 0 (the key), marks
    _pen_or_click_slide(M, 'solve-q-365', 2, {
        'Write "z < y < 0 → z < 0"': [A('z < y < 0 → z < 0 appears', T(r'$z<y<0 \;\to\; z<0$', size=S))],
        'Write "x = −2 or x = 2 (y = −4, z = −5)"': [A('x = −2 or x = 2 appears', T(r'$x=-2$ or $x=2$ $\ (y=-4,\ z=-5)$', size=S))],
    }, room=['Under the question write "y < x but |y| > |x| → y < 0"'], row=70)
    # ---- Q: q-366 - by hand: the short notes on choices 3 and 4, x = 6, y = −2: 4 < 8 (the key example), marks
    _pen_or_click_slide(M, 'solve-q-366', 2, {
        'Next to choice 1 write "|x+y| > 3 → |x+y|² > 9"': [A('(1) |x+y| > 3 → |x+y|² > 9 appears', T(r'(1) $|x+y|>3 \;\to\; |x+y|^2>9$', size=34))],
        'Below it write "|x+y|² = (x+y)²  →  (x+y)² > 9"': [A('|x+y|² = (x+y)² → (x+y)² > 9 appears', T(r'$|x+y|^2=(x+y)^2 \;\to\; (x+y)^2>9$', size=34))],
        'Write "x = 4, y = 1: 5 = 5"': [A('x = 4, y = 1: 5 = 5 appears', T(r'$x=4,\ y=1:\ \ 5=5$', size=34))],
    })
    b = M.slide('solve-q-366', 2)        # the rule was placed at a fixed spot - now it follows the click lines
    for it in b['items'][1:]:
        it.pop('x', None); it.pop('y', None); it['gap'] = 14
    b['items'][-2]['size'] = 38
    # ---- Q: q-r26-t13-13 - by hand: the third given -> opposite signs (method 1), circle the two 4s (method 2), circles
    _pen_or_click_slide(M, 'solve-q-r26-t13-13', 2, {
        'Under the question write "same signs: 10   opposite signs: 4"': [A('same signs: 10, opposite signs: 4 appears',
            T(r'same signs: $10 \qquad$ opposite signs: $4$', size=S))],
        'Write "|a + b| = 7 − 3 = 4"': [A('|a + b| = 7 − 3 = 4 appears', T(r'$|a+b|=7-3=4$', size=S))],
    }, room=['Underline "|a + b| < |a − b|" and write "the sum cancels → opposite signs"'], row=70)
    _pen_or_click_slide(M, 'solve-q-r26-t13-13', 4, {
        'Write "a = 7, b = 3:  |10| < |4| ✗"': [A('a = 7, b = 3: |10| < |4| ✗ appears', T(r'$a=7,\ b=3:\ \ |10|<|4|$ ✗', size=S))],
        'Write "a = −7, b = −3:  |−10| < |−4| ✗"': [A('a = −7, b = −3: |−10| < |−4| ✗ appears', T(r'$a=-7,\ b=-3:\ \ |-10|<|-4|$ ✗', size=S))],
        'Write "a = 7, b = −3:  |4| < |10| ✓     a = −7, b = 3:  |−4| < |−10| ✓"': [A('opposite signs: both ✓ appears',
            T(r'$a=7,\ b=-3:\ \ |4|<|10|$ ✓ $\qquad a=-7,\ b=3:\ \ |-4|<|-10|$ ✓', size=32))],
    })
    # ---- lesson: The Mirror Test (every written line -> click)
    V = 'r26-t13-mirror'
    _pen_or_click_slide(M, V, 3, {
        'Write "a → −a, b → −b:  |−a − b| < |−a| + |−b|"': [A('flip: |−a − b| < |−a| + |−b| appears',
            T(r'$a\to-a,\ b\to-b:\ \ |-a-b|<|-a|+|-b|$', size=38))],
        'Write "a → −a ✗    b − a → a − b ✗    a + b → −(a + b) ✗"': [A('a, b − a, a + b flip → out appears',
            T(r'$a\to-a$ ✗ $\qquad b-a\to a-b$ ✗ $\qquad a+b\to-(a+b)$ ✗', size=36))],
        'Write "a · b → (−a)(−b) = a · b ✓"': [A('a · b → (−a)(−b) = a · b ✓ appears', T(r'$a\cdot b\to(-a)(-b)=a\cdot b$ ✓', size=38))],
        'Write "a = 2, b = −1: |1| < 2 + 1 ✓, a · b = −2"': [A('a = 2, b = −1 check appears',
            T(r'$a=2,\ b=-1:\ \ |1|<2+1$ ✓, $\ a\cdot b=-2$', size=38))],
    })
    _pen_or_click_slide(M, V, 4, {
        'Write "flip:  x > 0 → x < 0 ✗    x + y > 0 → x + y < 0 ✗"': [A('flip: x > 0, x + y > 0 out appears',
            T(r'flip: $\ x>0\to x<0$ ✗ $\qquad x+y>0\to x+y<0$ ✗', size=36))],
        'Write "swap:  x < y → y < x ✗"': [A('swap: x < y → y < x ✗ appears', T(r'swap: $\ x<y\to y<x$ ✗', size=38))],
        'Write "x² ≤ 13 → y² ≤ 13: a twin, not an opposite"': [A('x² ≤ 13 → y² ≤ 13: a twin appears',
            T(r'$x^2\le13\to y^2\le13$: a twin, not an opposite', size=38))],
    })
    # ---- Q: q-r26-t13-15 - by hand: the swap (method 1), (a − b)² = 9 (method 2), the short notes on the choices, circle
    _pen_or_click_slide(M, 'solve-q-r26-t13-15', 2, {
        'Write "flip: (−a)² + (−b)² = 2(−a)(−b) + 9 → the same given"': [A('flip: the same given appears',
            T(r'flip: $\ (-a)^2+(-b)^2=2(-a)(-b)+9 \;\to\;$ the same given', size=32))],
    }, room=['Write "swap: b² + a² = 2ba + 9 → the same given"'], row=64)
    _pen_or_click_slide(M, 'solve-q-r26-t13-15', 3, {
        'Write "a − b = 3  or  a − b = −3 → |a − b| = 3"': [A('a − b = ±3 → |a − b| = 3 appears',
            T(r'$a-b=3$ or $a-b=-3 \;\to\; |a-b|=3$', size=S))],
        'Write "a = 0, b = 3: 0 + 9 = 0 + 9 ✓, a − b = −3"': [A('a = 0, b = 3 check appears',
            T(r'$a=0,\ b=3:\ \ 0+9=0+9$ ✓, $\ a-b=-3$', size=S))],
    }, room=['Write "a² − 2ab + b² = 9 → (a − b)² = 9"'], row=70)
    # ---- Q: q-r26-t13-03 - by hand: the check that kills x = −1 (method 1), 3x ≥ 0 (method 2, unchanged), marks
    _pen_or_click_slide(M, 'solve-q-r26-t13-03', 2, {
        'Write "x + 4 = 3x → 4 = 2x → x = 2"': [A('x + 4 = 3x → x = 2 appears', T(r'$x+4=3x \;\to\; 4=2x \;\to\; x=2$', size=S))],
        'Write "x + 4 = −3x → 4x = −4 → x = −1"': [A('x + 4 = −3x → x = −1 appears', T(r'$x+4=-3x \;\to\; 4x=-4 \;\to\; x=-1$', size=S))],
        'Write "x = 2: |6| = 6 = 3 · 2 ✓"': [A('x = 2: |6| = 6 = 3 · 2 ✓ appears', T(r'$x=2:\ \ |6|=6=3\cdot2$ ✓', size=S))],
    })
    # ---- Q: q-367 - by hand: |x| − x = 10 (subtract the equations, method 1), the notes on choices 1 and 2 (method 2),
    #      4·5 + 12·2 = 44 ✓ (method 3), circles
    _pen_or_click_slide(M, 'solve-q-367', 2, {
        'Under the first equation write "÷4: |x| + 3|y| = 11"': [A('÷4: |x| + 3|y| = 11 appears', T(r'$\div4:\ \ |x|+3|y|=11$', size=34))],
        'Write "|x| = 10 + x"': [A('|x| = 10 + x appears', T(r'$|x|=10+x$', size=34))],
        'Write "x = 10 + x → 0 = 10 ✗"': [A('x = 10 + x → 0 = 10 ✗ appears', T(r'$x=10+x \;\to\; 0=10$ ✗', size=34))],
        'Write "x = −(10 + x) → 2x = −10 → x = −5"': [A('x = −(10 + x) → x = −5 appears', T(r'$x=-(10+x) \;\to\; 2x=-10 \;\to\; x=-5$', size=34))],
    }, room=['Write "|x| − x = 11 − 1 = 10"'], row=52)
    for k, it in enumerate(M.slide('solve-q-367', 2)['items'][1:]):
        it['size'] = 32
        if k: it['gap'] = 8
        else: it['gap'] = 8 + 52
    _pen_or_click_slide(M, 'solve-q-367', 3, {
        'Write "|x| = 10 + x"': [A('|x| = 10 + x appears', T(r'$|x|=10+x$', size=S))],
    })
    _pen_or_click_slide(M, 'solve-q-367', 4, {
        'Next to choice 1 write "x = −2: −2 + 3|y| = 1 → |y| = 1"': [A('(1) x = −2 → |y| = 1 appears', T(r'(1) $x=-2:\ \ -2+3|y|=1 \;\to\; |y|=1$', size=34))],
        'Write "4·2 + 12·1 = 20 ≠ 44 ✗"': [A('4·2 + 12·1 = 20 ≠ 44 ✗ appears', T(r'$4\cdot2+12\cdot1=20\ne44$ ✗', size=34))],
        'Next to choice 2 write "x = −5: −5 + 3|y| = 1 → |y| = 2"': [A('(2) x = −5 → |y| = 2 appears', T(r'(2) $x=-5:\ \ -5+3|y|=1 \;\to\; |y|=2$', size=34))],
    })
    # ---- Q: q-368 - by hand: the opposite case (method 1), (x + 4y)² = (4x + y)² (method 2), x = 2, y = −2 (method 3), marks
    _pen_or_click_slide(M, 'solve-q-368', 2, {
        'Write "x + 4y = 4x + y → y = x"': [A('x + 4y = 4x + y → y = x appears', T(r'$x+4y=4x+y \;\to\; y=x$', size=S))],
    })
    _pen_or_click_slide(M, 'solve-q-368', 3, {
        'Write "x² + 8xy + 16y² = 16x² + 8xy + y²"': [A('x² + 8xy + 16y² = 16x² + 8xy + y² appears', T(r'$x^2+8xy+16y^2=16x^2+8xy+y^2$', size=36))],
        'Write "15y² = 15x² → y² = x²"': [A('15y² = 15x² → y² = x² appears', T(r'$15y^2=15x^2 \;\to\; y^2=x^2$', size=36))],
    }, room=['Write "(x + 4y)² = (4x + y)²"'], row=64)
    _pen_or_click_slide(M, 'solve-q-368', 4, {
        'Write "x = y = 2: |10| = |10| ✓"': [A('x = y = 2: |10| = |10| ✓ appears', T(r'$x=y=2:\ \ |10|=|10|$ ✓', size=S))],
    })
    # ---- Q: q-369 - by hand: the two bands on the number line (the idea), circles
    _pen_or_click_slide(M, 'solve-q-369', 2, {
        'Write "7 < 2x − 1 < 9"': [A('7 < 2x − 1 < 9 appears', T(r'$7<2x-1<9$', size=S))],
        'Write "8 < 2x < 10 → 4 < x < 5"': [A('8 < 2x < 10 → 4 < x < 5 appears', T(r'$8<2x<10 \;\to\; 4<x<5$', size=S))],
        'Write "−9 < 2x − 1 < −7 → −8 < 2x < −6 → −4 < x < −3"': [A('−9 < 2x − 1 < −7 → −4 < x < −3 appears',
            T(r'$-9<2x-1<-7 \;\to\; -8<2x<-6 \;\to\; -4<x<-3$', size=S))],
    })
    _pen_or_click_slide(M, 'solve-q-369', 3, {
        'Next to choice 1 write "x = 3.5: |6| = 6 ✗"': [A('(1) x = 3.5: |6| = 6 ✗ appears', T(r'(1) $x=3.5:\ \ |6|=6$ ✗', size=S))],
        'Next to choice 2 write "x = 5.5: |10| = 10 ✗"': [A('(2) x = 5.5: |10| = 10 ✗ appears', T(r'(2) $x=5.5:\ \ |10|=10$ ✗', size=S))],
        'Next to choice 3 write "x = −3.5: |−8| = 8 ✓"': [A('(3) x = −3.5: |−8| = 8 ✓ appears', T(r'(3) $x=-3.5:\ \ |-8|=8$ ✓', size=S))],
    })
    # ---- Q: q-370 - by hand: x < 0: 0 < 12 always (method 1), x = −8 (method 2), marks
    _pen_or_click_slide(M, 'solve-q-370', 2, {
        'Write "x ≥ 0: 2x < 12 → x < 6"': [A('x ≥ 0: 2x < 12 → x < 6 appears', T(r'$x\ge0:\ \ 2x<12 \;\to\; x<6$', size=S))],
        'Write "x = −4: −4 + 4 = 0"': [A('x = −4: −4 + 4 = 0 appears', T(r'$x=-4:\ \ -4+4=0$', size=S))],
    })
    _pen_or_click_slide(M, 'solve-q-370', 3, {
        'Next to choice 4 write "x = 2: 4 < 12 ✓, x = 9: 18 ✗"': [A('(4) x = 2 ✓, x = 9 ✗ appears',
            T(r'(4) $x=2:\ \ 4<12$ ✓, $\ x=9:\ \ 18$ ✗', size=S))],
    })
    # ---- lesson: Summary
    _pen_or_click_slide(M, 'r26-t13-summary', 5, {
        'Write "x = 8 or x = −12"': [A('x = 8 or x = −12 appears', T(r'$x=8$ or $x=-12$', size=44))],
    })
    _gaps(M, 'r26-t13-summary', 5, 30)


_apply_before_pen_or_click = apply


def apply(M):
    _apply_before_pen_or_click(M)
    pen_or_click(M)   # 2026-10-07 pen or click: runs last



# =====================================================================================================================
# 2026-10-07 methods spread: the 2026-10-06 exam methods shown wherever they genuinely help (teacher: "I don't want the
# students to miss out on it"). (a) a written line appended to the explanation, (b) for a few UNRECORDED solution
# videos one short extra slide at the end. A recorded video is never changed: any video with a file in
# ~/Documents/Course.recordings is skipped at build time (its written line is still added). Runs LAST.
# =====================================================================================================================
import glob as _sp_glob, os as _sp_os, re as _sp_re


def _sp_recorded():
    out = set()
    for f in _sp_glob.glob(_sp_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = _sp_re.match(r'(.+)-\d{4}-\d\d-\d\dT[\d-]+Z\.(mp4|webm)$', _sp_os.path.basename(f))
        if m: out.add(m.group(1))
    return out


SPREAD_LINES = {
    'q-368': ['Method 2 · Mirror test: swap $x$ and $y$: $|y+4x|=|4y+x|$ is the same given. $y<x$ turns into $x<y$, its opposite, and $x<y$ turns into $y<x$, so choices 1 and 4 are out. Between 2 and 3: $x=2$, $y=-2$ fits ($|-6|=|6|$) with $x\\ne y$, so choice 2 is out. The answer is choice 3.'],
    'q-370': ['Method 2 · The most precise range: $x=-8$ works ($-8+8=0<12$), so choices 1 and 4 (which leave $-8$ out) are out. $x=2$ works ($4<12$), so choice 2 is out. The answer is choice 3.'],
    'q-371': ['Method 2 · Pick values that fit: $q\\ne0$, so take $q=4$ and solve $|p+4|=|p-4|$. $p$ is as far from $-4$ as from $4$, so $p=0$. The choices at $q=4$: $8$, $0$, $-4$, $-2$. Only choice 2 gives $0$.'],
    'q-374': ['Method 2 · Pick values that fit: take $n=1$. $|m+1|=|m-1|$ gives $m=0$, so $m\\cdot n=0$: choices 1 and 3 are out. Take $n=2$: again $m=0$ and $m\\cdot n=0$. The value does not change, so choice 4 is out too. The answer is choice 2.'],
}

SPREAD_SLIDES = {}

SPREAD_SAY = {}


def spread_methods(M):
    for qid, lines in SPREAD_LINES.items():
        q = M.q(qid)
        if all(l not in q['explanation'] for l in lines):
            M.set_q(qid, expl=list(q['explanation']) + lines)
    rec = _sp_recorded()
    for vid, (after, title, script) in SPREAD_SLIDES.items():
        if vid in rec: continue   # recorded: never change it
        beats = M.video(vid)['beats']
        n = next(i for i, b in enumerate(beats, 1) if b['title'] == after)
        b = beats[n - 1]
        M.insert_slides(vid, n, [dict(mode='question', active=b['active'], title=title,
                                      pre=[dict(it) for it in b['items'][:b['pre']]], script=script)])
        for k, old, new in SPREAD_SAY.get(vid, []):
            sl = M.slide(vid, k)
            assert any(l.get('say') == old for l in sl['lines']), (vid, k, old)
            for l in sl['lines']:
                if l.get('say') == old: l['say'] = new
            M.touched_videos.add(vid)


_apply_before_spread_methods = apply


def apply(M):
    _apply_before_spread_methods(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last
