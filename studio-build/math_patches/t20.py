"""Topic 20 - Algebraic Understanding. Course review 2026-09 fixes.
See t20_CHANGES.md for the plain-language list.

Note on question numbers: new guided questions get the next free number (5, 6, 7, 8) when they are created.
renumber_guided() then numbers all guided questions in course order, so spoken "Question five" in a new video
becomes "Question one" (G1 and G2 come before the old Q1). Numbers in this file use the pre-renumber numbering."""
from dsl import T, H, A, D, Q

TOPIC = 20
LESSON = 'algebraic-understanding'
COUNT = 'r26-t20-counting'
SEC = 'understanding'
PRAC = 'unit-t20-2'
QSIDEBAR = ['Question %d' % n for n in range(1, 9)]


def _solution(M, qid, intro, slides, after=None):
    """Guided-question solution video in the style of solve-q-577..580."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=n - 1, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Understanding Questions', QSIDEBAR, beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = 'Understanding Questions'
    v['hybrid']['num'] = 65
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _sync_video(M, qid):
    """Keep video title and 'Pre-loaded' slide notes in sync with a rewritten stem."""
    v = M.video('solve-' + qid); q = M.q(qid)
    v['title'] = v['navLabel'] = q['stem']
    for b in v['beats']:
        if b.get('canvas', '').startswith('Pre-loaded — question'):
            b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Main lesson: rebuilt around the three tools, plug-in regions, gaps, scaling
    # =====================================================================================
    M.remove_slides(LESSON, [2, 3, 4, 5, 6, 7])
    M.insert_slides(LESSON, 1, [
        dict(mode='concept', active=0, title='Three tools', script=[
            "This topic mixes ideas from all of algebra.",
            "Now the honest truth: it's a fairly small part of the exam — and the questions don't repeat themselves.",
            "There's no repeating principle I can hand you that solves them all.",
            "But this lesson, and the practice after it, give you tools that open your head for questions like these.",
            "Three tools open almost all of them.",
            A("'1 · Plug in numbers' appears", T('1 · Plug in numbers')),
            "One: plug in numbers. Small, simple, allowed numbers.",
            A("'2 · Test the answers' appears", T('2 · Test the answers')),
            "Two: test the answers. Put each choice into the question.",
            A("'3 · Algebra and understanding' appears", T('3 · Algebra and understanding')),
            "Three: algebra — and understanding what the givens really say.",
            D('Put a box around the three numbers'),
            "Try them in this order. Numbers first — they're fast and safe. Algebra when the numbers don't decide.",
        ]),
        dict(mode='concept', active=1, title='Must, could, cannot', script=[
            "You met these three words in Topic 1. A quick reminder — then we go deeper.",
            A("'Must be true — every allowed case' appears", T('Must be true — every allowed case', size=44)),
            "Must: true in every case the givens allow. One case that fails — and it's out.",
            A("'Could be true — at least one allowed case' appears", T('Could be true — at least one allowed case', size=44)),
            "Could: one allowed example is enough.",
            A("'Cannot be true — no allowed case' appears", T('Cannot be true — no allowed case', size=44)),
            "Cannot: no allowed case at all. Every choice you can make happen is out.",
            A("'Not necessarily true — fails in at least one case' appears",
              T('Not necessarily true — fails in at least one case', size=44)),
            "The exam also asks: which is NOT necessarily true? That's the one that fails in at least one allowed case.",
            D('Write "must / could / cannot / not necessarily" in a corner and circle one'),
            "Write the word down before you touch the choices. Under pressure, the directions flip.",
        ]),
        dict(mode='concept', active=2, title='Which numbers?', script=[
            "In Topic 1 you got a short list to test: zero, one, minus one, one half, ten.",
            "Now: which of them to use, and when.",
            A("'1 · Read the conditions: which numbers are allowed?' appears",
              T('1 · Read the conditions: which numbers are allowed?', size=40)),
            "Step one: the conditions. Positive? Integer? Different from each other? Test only numbers they allow.",
            A("'2 · One number from each region' appears",
              T('2 · One number from each region: $x>1$;  $0<x<1$;  $-1<x<0$;  $x<-1$', size=40)),
            "Step two: think in regions. Numbers bigger than one behave one way. Numbers between zero and one behave another way.",
            "The negatives split the same way.",
            D('Under it write "x > 0 → try 2 and ½"'),
            "So if x can be any positive number, try one number from each region: two, and one half.",
            A("'3 · Letters may be equal? Try a = b too.' appears", T('3 · Letters may be equal? Try $a=b$ too.', size=40)),
            "Step three: if the letters may be equal, try equal values too. If they must be different — don't.",
            A("'4 · Two choices survive? Try a second number.' appears", T('4 · Two choices survive? Try a second number.', size=40)),
            "And if two choices survive your first number — don't guess. Try a number from another region.",
        ]),
        dict(mode='concept', active=3, title='Between 0 and 1', script=[
            "Numbers between zero and one are the favorite trap.",
            A("'0 < x < 1: x² < x < √x < 1 < 1/x' appears",
              T('$0<x<1:\\quad x^2<x<\\sqrt{x}<1<\\frac{1}{x}$', size=54, gap=40)),
            "Squaring makes them smaller. The root makes them bigger. And one over x is bigger than one.",
            D('Under it write "x = ¼: x² = 1/16, √x = ½, 1/x = 4"'),
            "Check with one quarter. Squared: one sixteenth. The root: one half. One over it: four.",
            A("'Negatives: −5 < −2' appears", T('Negatives: $-5<-2$ — farther from $0$ means smaller', size=42, gap=40)),
            "And negatives: the farther from zero, the SMALLER the number. Minus five is less than minus two.",
            A("'Which is largest for x in a range? One number decides.' appears",
              T('"Which is the largest?" for every $x$ in a range: one number from the range decides', size=40)),
            "A question asks which is the largest — for every x in a range?",
            "The right choice must win for every x in that range. So one number from the range shows it.",
            "Pick an easy one from the middle, like one half, or minus one half.",
        ]),
        dict(mode='concept', active=4, title='Integer gaps', script=[
            "Integers leave gaps. Start with strictness.",
            A("'Integer and < 12 → ≤ 11' appears", T('Integer and $<12\\ \\to\\ \\le11$', size=46, gap=40)),
            "An integer strictly less than twelve is at most eleven.",
            A("'a > b > c integers → a ≥ b + 1, c ≤ b − 1' appears",
              T('$a>b>c$ integers $\\to$ $a\\ge b+1$, $\\ c\\le b-1$', size=46, gap=40)),
            "If a is bigger than b, it's bigger by at least one.",
            D('Under it write "→ a ≥ c + 2"'),
            "Chain two gaps, and a is at least two above c.",
            A("'n increasing integers: last ≥ first + (n − 1)' appears",
              T('$n$ increasing integers: last $\\ge$ first $+\\ (n-1)$', size=44)),
            "In general: n integers, each one bigger than the one before. The last is at least the first, plus n minus one.",
            "Those gaps give you the biggest or smallest possible value — without listing every case.",
            "And in a cannot question with a hidden maximum or minimum, test the most extreme choices first.",
        ]),
        dict(mode='concept', active=5, title='Scaling', script=[
            A("x² = a³ and 'a × 16 → x × ?' appear",
              T('$x^2=a^3,\\quad x,a>0$ $\\qquad a\\times16\\ \\to\\ x\\times\\ ?$', size=46, gap=60)),
            "One variable gets multiplied — what happens to the other?",
            D('Write "a = 1, x = 1 → a = 16: x² = 16³ = 4096, x = 64"'),
            "Start from one and one. The new a is sixteen. Then x squared is sixteen cubed — four thousand ninety-six. x is sixty-four.",
            "Positive, because the question says so.",
            A("'x changes by (factor) to the power 3/2' appears",
              T('$x^2=a^3\\ \\to\\ x$ changes by $(\\text{factor})^{\\frac{3}{2}}$', size=44)),
            "The general rule: x squared equals a cubed. So x changes by the factor of a, to the power three halves.",
            D('Write "16^(3/2) = (√16)³ = 4³ = 64"'),
            "Sixteen to the three halves: root sixteen is four. Four cubed is sixty-four. Same answer.",
            "You'll see this idea again in question two.",
        ]),
        dict(mode='concept', active=6, title='Connect topics', script=[
            "Sometimes the key is a structure you know from another place.",
            A("'c² = a² + b², all positive → c > a and c > b' appears",
              T('$c^2=a^2+b^2$, all positive $\\to$ $c>a$ and $c>b$', size=46, gap=50)),
            "c squared equals a squared plus b squared, and all three are positive.",
            "Then c squared is bigger than b squared. Therefore c is bigger than b — and bigger than a.",
            "In geometry you'll meet this again, as Pythagoras.",
            A("'x/y · y/z · z/x = 1' appears", T('$\\frac{x}{y}\\cdot\\frac{y}{z}\\cdot\\frac{z}{x}=1$', size=54)),
            "A cycle of ratios cancels to one. So the three fractions can't all be bigger than one.",
            "But the connection must come from the givens. Lengths must be positive; cancelling needs nonzero values. Check before you use it.",
        ]),
        dict(mode='concept', active=7, title='Recap', script=[
            "Let's lock in the last algebra lesson.",
            A("'Tools: plug in → test the answers → algebra' appears", T('Tools: plug in $\\to$ test the answers $\\to$ algebra', size=40)),
            A("'Write the word: must · could · cannot' appears", T('Write the word: must · could · cannot', size=40)),
            A("'Plug in: one number from each region' appears", T('Plug in: one number from each region', size=40)),
            A("'0 < x < 1: x² < x < √x' appears", T('$0<x<1$: $\\ x^2<x<\\sqrt{x}$', size=40)),
            A("'Integers leave gaps — use them for max and min' appears", T('Integers leave gaps — use them for max and min', size=40)),
            D('Underline "plug in"'),
            "Two questions on plugging in first. Then four questions, each with more than one way in.",
            "After that, a short lesson on counting — and practice on your own.",
        ]),
    ])
    M.set_sidebar(LESSON, ['Three tools', 'Must, could, cannot', 'Which numbers?', 'Between 0 and 1',
                           'Integer gaps', 'Scaling', 'Connect topics', 'Recap'])

    # =====================================================================================
    # 2. Memory card of the lesson (could, plug-in regions, facts)
    # =====================================================================================
    c = M.card('mem-understanding')
    c['title'] = 'Algebraic understanding'
    c['intro'] = 'Must, could, cannot (Topic 1) — and the tools to answer them.'
    c['tables'] = [
        {'title': 'The question word', 'head': ['They ask', 'You need', 'A choice is out when'], 'rows': [
            ['Must be true / necessarily true', 'true in every allowed case', 'one allowed example breaks it'],
            ['Could be true / possible', 'one allowed example', 'no allowed example exists'],
            ['Cannot be true / impossible', 'no allowed case at all', 'one allowed example makes it happen'],
            ['Not necessarily true', 'one allowed case where it fails', 'it is always true']]},
        {'title': 'Which numbers to plug in', 'head': ['The condition', 'Try'], 'rows': [
            ['$x>0$', '$2$ and $\\frac12$'],
            ['$x$ can be any number', '$2$, $\\frac12$, $-\\frac12$, $-2$ (and $0$)'],
            ['the letters may be equal', 'also $a=b$'],
            ['a range, like $-1<x<0$', 'one easy number from the range: $-\\frac12$'],
            ['two choices survive', 'a second number, from another region']]},
        {'title': 'Facts to know', 'head': ['Range', 'Order'], 'rows': [
            ['$0<x<1$', '$x^2<x<\\sqrt x<1<\\frac1x$'],
            ['$-1<x<0$', '$\\frac1x<-1<x<x^3<0<x^2$'],
            ['negative numbers', 'farther from $0$ means smaller: $-5<-2$']]},
    ]
    c['tips'] = [
        'Tools, in this order: plug in numbers, test the answers, then algebra.',
        'Integers leave gaps: $a>b>c\\to a\\ge c+2$. $n$ increasing integers: last $\\ge$ first $+(n-1)$.',
        'An integer less than $12$ is at most $11$.',
        'A "cannot" question with a hidden maximum or minimum? Test the most extreme choices first.',
        'Scaling: $x^2=a^3$, so $x$ changes by $(\\text{factor})^{\\frac32}$. For example, $9^{\\frac32}=27$.',
        '$\\frac xy\\cdot\\frac yz\\cdot\\frac zx=1$: the three fractions cannot all be greater than $1$.',
    ]

    # =====================================================================================
    # 3. Two new guided questions before the old Q1 (plug-in regions; which is smallest)
    # =====================================================================================
    g1, g2, g3, g4 = ['q-r26-t20-%02d' % k for k in (1, 2, 3, 4)]
    M.new_q(g1, TOPIC, 'Given: $x$ and $y$ are positive numbers, and $x>y$. Which of the following must be true?',
            ['$x^2>x$', '$xy>y$', '$x^2>y^2$', '$\\frac{x}{y}>x$'], 3, [
        'Plug in $x=3$ and $y=2$: (1) $9>3$ ✓, (2) $6>2$ ✓, (3) $9>4$ ✓, (4) $\\frac32>3$ ✗. Three choices survive.',
        'Try the other region, numbers between $0$ and $1$: $x=\\frac12$ and $y=\\frac14$. (1) $\\frac14>\\frac12$ ✗, (2) $\\frac18>\\frac14$ ✗, (3) $\\frac14>\\frac1{16}$ ✓.',
        'Only (3) survives. It is always true: $x^2-y^2=(x-y)(x+y)$, and both brackets are positive.'])
    M.place_q(g1, SEC, before='q-577')
    _solution(M, g1, ["Question five.", "A must-be-true question. Our tool: plug in numbers — from more than one region."], [
        ('Plug in 3 and 2', [
            "x and y are positive, and x is bigger than y. Which must be true?",
            "Positive numbers have two regions: bigger than one, and between zero and one. Start with easy whole numbers.",
            D('Under the question write "x = 3, y = 2"'),
            D('Next to choice 1 write "9 > 3 ✓"'),
            "Choice one: three squared is nine. Nine is bigger than three. It holds.",
            D('Next to choice 2 write "6 > 2 ✓"'),
            "Choice two: three times two is six. Bigger than two. It holds.",
            D('Next to choice 3 write "9 > 4 ✓"'),
            "Choice three: nine is bigger than four. It holds.",
            D('Next to choice 4 write "3/2 > 3 ✗" and cross it out'),
            "Choice four: three over two is one and a half. That's not bigger than three. Out.",
            "Three choices survive. One number was not enough.",
        ]),
        ('Now a fraction', [
            "Now the other region: numbers between zero and one.",
            D('Under the question write "x = ½, y = ¼"'),
            "x is one half, y is one quarter. Both positive, and x is still bigger.",
            D('Next to choice 1 write "¼ > ½ ✗" and cross it out'),
            "Choice one: one half squared is one quarter. That's smaller than one half. Out.",
            D('Next to choice 2 write "⅛ > ¼ ✗" and cross it out'),
            "Choice two: one half times one quarter is one eighth. Smaller than one quarter. Out.",
            D('Next to choice 3 write "¼ > 1/16 ✓"'),
            "Choice three: one quarter against one sixteenth. It still holds.",
            D('Circle choice 3'),
            "Only choice three survives. Choice three.",
            D('Write "x² − y² = (x − y)(x + y) > 0"'),
            "Why is it always true? x squared minus y squared is x minus y, times x plus y. Both brackets are positive.",
        ]),
    ])

    M.new_q(g2, TOPIC, 'Given: $-1<x<0$. Which of the following is the smallest?',
            ['$x^3$', '$x$', '$-x^2$', '$\\frac{1}{x}$'], 4, [
        'The right choice must be the smallest for every $x$ in the range. Therefore one number from the range decides: $x=-\\frac12$.',
        '$x^3=-\\frac18$, $x=-\\frac12$, $-x^2=-\\frac14$, $\\frac1x=-2$.',
        'With negative numbers, farther from $0$ means smaller: $-2<-\\frac12<-\\frac14<-\\frac18$. The smallest is $\\frac1x$.',
        'Why always: $\\frac1x<-1$ for every $x$ in the range, while $x$, $x^3$ and $-x^2$ are all between $-1$ and $0$.'])
    M.place_q(g2, SEC, after='solve-' + g1)
    _solution(M, g2, ["Question six.", "Which is the smallest — for every x in a range."], [
        ('One number from the range', [
            "x is between minus one and zero. Which choice is the smallest?",
            "The right choice must be the smallest for every x in the range. So one number from the range decides.",
            D('Under the question write "x = −½"'),
            "Take minus one half. Easy to work with.",
            D('Next to choice 1 write "−⅛"'),
            "Choice one: minus one half, cubed. Minus times minus times minus is minus. Minus one eighth.",
            D('Next to choice 2 write "−½"'),
            "Choice two: x itself. Minus one half.",
            D('Next to choice 3 write "−¼"'),
            "Choice three: x squared is one quarter. With the minus in front: minus one quarter.",
            D('Next to choice 4 write "−2"'),
            "Choice four: one over minus one half is minus two.",
        ]),
        ('Order the negatives', [
            "Now put them in order. With negatives, the farther from zero, the smaller the number.",
            D('Write "−2 < −½ < −¼ < −⅛"'),
            "Minus two is the farthest from zero. It's the smallest.",
            D('Circle choice 4'),
            "Choice four.",
            "The trap is choice one. Cubing a number between minus one and zero brings it closer to zero. So it gets BIGGER.",
            "And one over x is always below minus one here. One divided by a small negative number is a big negative number.",
        ]),
    ])

    # =====================================================================================
    # 4. Existing guided questions: text, and the videos
    # =====================================================================================
    S('q-577', stem='Given: $a$, $b$ and $c$ are integers, and\n$\\begin{cases} c<b<a \\\\ a+b<12 \\end{cases}$\nWhich of the following cannot be the value of $b+c$?',
      expl=['The numbers are integers. Therefore $a+b<12$ means $a+b\\le11$.',
            'Also $c\\le b-1$ and $b\\le a-1$. Therefore $c\\le a-2$, and $a-c\\ge2$.',
            '$b+c=(a+b)-(a-c)\\le11-2=9$. The biggest possible value of $b+c$ is $9$ (for example $a=6$, $b=5$, $c=4$). Therefore $b+c=10$ is impossible.',
            'The other values are possible: $(a,b,c)=(2,1,0)$ gives $1$; $(1,0,-1)$ gives $-1$; $(1,0,-10)$ gives $-10$.'])
    M.set_slide('solve-q-577', 2, script=[
        "Three integers, c below b below a. And a plus b is less than twelve.",
        "They ask what b plus c CANNOT be. So let's find the biggest b plus c can ever be.",
        D('Under the question write "a + b ≤ 11"'),
        "a and b are integers. Less than twelve means at most eleven.",
        "Now compare. a plus b is the two biggest numbers. b plus c is the two smallest. The difference between them is a minus c.",
        D('Write "c ≤ a − 2 → a − c ≥ 2"'),
        "c is at least one below b, and b is at least one below a. Therefore c is at least two below a.",
        D('Write "b + c = (a + b) − (a − c) ≤ 11 − 2 = 9"'),
        "b plus c is a plus b, minus the difference a minus c. At most eleven, minus at least two: at most nine.",
        D('Circle choice 3'),
        "Ten goes past the maximum. It can't happen. Choice three.",
    ])
    M.set_slide('solve-q-577', 3, script=[
        "Second way: plug in numbers that make b plus c as big as possible.",
        "We want b as big as it can be — then c can be big too.",
        D('Write "a = 6, b = 5 → a + b = 11 ✓"'),
        "Six and five: eleven, still under twelve. That's the biggest b we can get.",
        D('Write "c = 4 → b + c = 9"'),
        "Push a up to seven, and b drops to four — worse. So the biggest c is four, and the biggest b plus c is nine.",
        D('Circle choice 3'),
        "Again — ten is out of reach. Choice three.",
    ])
    M.set_slide('solve-q-577', 4, script=[
        "Third way: test the answers. Which value can't b plus c be?",
        "A maximum is hidden here. So start with the most extreme choices: ten and minus ten.",
        D('Next to choice 3 write "b = 6, c = 4, a ≥ 7 → a + b ≥ 13 ✗"'),
        "Ten: b is bigger than c. The smallest b is six, with c four. Then a is at least seven — and a plus b is at least thirteen. Too big.",
        D('Circle choice 3'),
        "Found it. Choice three.",
        "Want to be safe? The other choices are easy to make.",
        D('Next to choice 4 write "(a, b, c) = (1, 0, −10) ✓", next to choice 1 "(2, 1, 0) ✓", next to choice 2 "(1, 0, −1) ✓"'),
        "Minus ten: a one, b zero, c minus ten. One: a two, b one, c zero. Minus one: a one, b zero, c minus one. All allowed.",
        "Three methods, all excellent. Pick the one that's comfortable for you.",
    ])

    S('q-578', stem='Given:\n$\\begin{cases} a>0,\\ x>0 \\\\ x^2=a^3 \\end{cases}$\nIf $a$ is multiplied by $9$, by what factor is $x$ multiplied?',
      expl=['Plug in: $a=1$ gives $x^2=1$ and $x=1$ (because $x>0$).',
            'Multiply $a$ by $9$: $a=9$ gives $x^2=9^3=729$ and $x=27$. $x$ went from $1$ to $27$: it was multiplied by $27$.',
            'Algebra: $(kx)^2=(9a)^3$ gives $k^2x^2=729a^3$. Since $x^2=a^3$, $k^2=729$ and $k=27$.',
            'General rule: $x=a^{\\frac32}$. Therefore $x$ is multiplied by $9^{\\frac32}=(\\sqrt9)^3=27$.'])
    M.edit_lines('solve-q-578', 2, lambda ls: [
        {'say': "Didn't spot it? Put a equal to one: x squared is one. x is plus or minus one — and x is positive. So x is one."}
        if l.get('say', '').startswith("Didn't spot it") else
        {'say': "x squared is seven twenty-nine. x is twenty-seven. Positive again."}
        if l.get('say', '').startswith('x squared is seven twenty-nine') else l for l in ls])
    M.edit_lines('solve-q-578', 3, lambda ls: [
        {'say': "But x squared equals a cubed. They cancel."} if l.get('say', '').startswith('But x squared') else
        {'say': "k squared is seven twenty-nine. k is twenty-seven. Choice three."} if l.get('say', '').startswith('k squared is') else l
        for l in ls] + [
        {'draw': 'Write "x = a^(3/2) → 9^(3/2) = (√9)³ = 3³ = 27"'},
        {'say': "The general rule from the lesson: x changes by the factor to the power three halves. Root nine is three. Three cubed is twenty-seven."},
    ])

    S('q-579', stem='Given: $a$, $b$ and $c$ are different positive integers, and $\\frac{c^2}{ab}=\\frac{a}{b}+\\frac{b}{a}$. Which of the following is not necessarily true?',
      expl=['Common denominator: $\\frac ab+\\frac ba=\\frac{a^2}{ab}+\\frac{b^2}{ab}=\\frac{a^2+b^2}{ab}$. Therefore $c^2=a^2+b^2$.',
            '(3) and (4) are always true: $c^2=a^2+b^2>b^2$, and all the numbers are positive. Therefore $c>b$. In the same way, $c>a$.',
            '(1) is always true: $(a+b)^2=a^2+2ab+b^2=c^2+2ab>c^2$. Therefore $a+b>c$.',
            '(2) is not necessarily true: $(a,b,c)=(3,4,5)$ fits ($9+16=25$) and gives $c=5<6$. But $(6,8,10)$ also fits ($36+64=100$) and gives $c=10$.'])
    M.edit_lines('solve-q-579', 1, lambda ls: [{'say': 'Question three.'},
                                               {'say': 'A hard one. Simplify first — then test each choice.'}])
    M.set_slide('solve-q-579', 2, title='Simplify', script=[
        "Step one: simplify the equation.",
        D('Write "a/b = a²/(ab),  b/a = b²/(ab)"'),
        "Common denominator: a times b. a over b is a squared over a b. b over a is b squared over a b.",
        D('Write "c²/(ab) = (a² + b²)/(ab) → c² = a² + b²"'),
        "Both sides are over a b. So c squared equals a squared plus b squared.",
        "Read the question carefully: which statement is NOT necessarily true?",
        "Anything that's always true — we cross out. We're hunting for the one that can fail.",
    ])
    M.insert_slides('solve-q-579', 2, [dict(mode='question', active=2, title='Test each choice', pre=[Q('q-579')], script=[
        D('Next to choice 3 write "c² = a² + b² > b² → c > b" and cross it out'),
        "Choice three: c squared is b squared plus something positive. So c squared is bigger than b squared.",
        "All the numbers are positive. Therefore c is bigger than b. Always. Out.",
        D('Cross out choice 4'),
        "Choice four: the same with a. Always. Out.",
        D('Next to choice 1 write "(a + b)² = c² + 2ab > c²" and cross it out'),
        "Choice one: a plus b, squared, is a squared plus two a b plus b squared. That's c squared plus two a b — bigger than c squared.",
        "So a plus b is bigger than c. Always. Out.",
        "Choice two: c is less than six. Look for integers that fit.",
        D('Next to choice 2 write "3, 4, 5: 9 + 16 = 25 → c = 5  |  6, 8, 10: 36 + 64 = 100 → c = 10"'),
        "Three, four, five: nine plus sixteen is twenty-five. c is five — less than six.",
        "Now double them: six, eight, ten. Thirty-six plus sixty-four is a hundred. c is ten — not less than six.",
        D('Circle choice 2'),
        "Sometimes true, sometimes not. Not necessarily true. Choice two.",
        "In geometry you'll meet c squared equals a squared plus b squared again, as Pythagoras.",
        "And choice one becomes a rule there: the sum of any two sides of a triangle is longer than the third.",
    ])])

    S('q-580', stem="A plant's growth rate is given by a formula. The rate increases when the plant gets more sunlight ($S$) and more water ($W$), and decreases when there are more weeds ($D$) around it. $S$, $W$ and $D$ are all greater than $1$. Which of the following expressions cannot give the plant's growth rate?",
      expl=['A valid formula must grow when $S$ grows, grow when $W$ grows, and shrink when $D$ grows.',
            'In (1), $\\frac{S^W}{D}$, a bigger $S$ or $W$ makes the top bigger (because $S>1$), and a bigger $D$ makes the fraction smaller ✓.',
            '(2) $S\\cdot W-D$ and (3) $S-D+W$: $S$ and $W$ are multiplied or added, and $D$ is subtracted ✓.',
            'In (4), $S\\cdot W\\cdot D$, a bigger $D$ makes the product BIGGER. More weeds would mean faster growth — the opposite of the rule. Therefore (4) cannot give the growth rate.'])
    M.edit_lines('solve-q-580', 1, lambda ls: [{'say': 'Question four.'}] + [{'say': 'A question about a formula.'} if l.get('say') == 'Last question of algebra.' else l for l in ls])
    M.edit_lines('solve-q-580', 2, lambda ls: [
        {'say': "Next: a short lesson on counting whole numbers."} if 'last question in algebraic understanding' in l.get('say', '') else l
        for l in ls])

    for vid in ['solve-q-577', 'solve-q-578', 'solve-q-579', 'solve-q-580']:
        M.set_sidebar(vid, QSIDEBAR)
    for qid in ['q-577', 'q-578', 'q-579', 'q-580']:
        _sync_video(M, qid)

    # =====================================================================================
    # 5. New lesson: counting integers in a range + pigeonhole
    # =====================================================================================
    M.new_video(COUNT, TOPIC, 'Counting Integers & Pigeonhole',
                ['From a to b', 'Strictly between', 'Only odd or even', 'Pigeonhole', 'To be sure', 'Recap'], [
        dict(mode='title', title='Counting Integers & Pigeonhole', script=[
            "Two more tools the exam loves.",
            "Counting the whole numbers in a range — and the pigeonhole principle.",
        ]),
        dict(mode='concept', active=0, title='From a to b', script=[
            A("'From a to b, both included: b − a + 1' appears", T('From $a$ to $b$, both included: $\\ b-a+1$', size=46, gap=50)),
            "How many whole numbers from one to ten? Ten. Easy.",
            D('Write "1, 2, …, 10 → 10 − 1 + 1 = 10"'),
            "Ten minus one is nine — but there are ten numbers. We add one, because both ends count.",
            D('Write "5 to 12: 12 − 5 + 1 = 8"'),
            "Five to twelve: twelve minus five is seven. Plus one — eight numbers.",
            "Five, six, seven, eight, nine, ten, eleven, twelve. Eight.",
            "Subtracting counts the jumps between the numbers. There is always one more number than jumps.",
        ]),
        dict(mode='concept', active=1, title='Strictly between', script=[
            A("'Strictly between a and b: b − a − 1' appears", T('Strictly between $a$ and $b$: $\\ b-a-1$', size=46, gap=50)),
            "Strictly between five and twelve: both ends are out.",
            D('Write "6, 7, 8, 9, 10, 11 → 12 − 5 − 1 = 6"'),
            "Six numbers. Twelve minus five, minus one.",
            A("'One end included: b − a' appears", T('One end included: $\\ b-a$', size=46)),
            "One end in, one end out: just b minus a. Here, seven.",
            "Not sure which rule? Count a small case on your fingers. It takes five seconds.",
        ]),
        dict(mode='concept', active=2, title='Only odd or even', script=[
            A("'Every second number: (last − first)/2 + 1' appears",
              T('Every second number: $\\ \\frac{\\text{last}-\\text{first}}{2}+1$', size=46, gap=50)),
            "Only odd numbers, or only even numbers? Now you jump by two.",
            "Find the first and the last number that count. Then: last minus first, divided by two, plus one.",
            D('Write "odd, 5 to 15: 5, 7, 9, 11, 13, 15 → (15 − 5) ÷ 2 + 1 = 6"'),
            "Odd numbers from five to fifteen. Fifteen minus five is ten. Half of it: five jumps. Plus one: six numbers.",
            A("'Letters in the choices? Plug in small numbers and count.' appears",
              T('Letters in the choices? Plug in small numbers and count.', size=40)),
            "And if the answers have letters — plug in small numbers, count by hand, and see which formula gives your count.",
            "If two formulas match, try a second number.",
        ]),
        dict(mode='concept', active=3, title='Pigeonhole', script=[
            A("'More items than boxes → one box gets two' appears", T('More items than boxes $\\to$ one box gets two', size=46, gap=50)),
            "Now the pigeonhole principle. Four pigeons, three holes — some hole gets two pigeons.",
            "Thirteen people, twelve months. At least two of them were born in the same month.",
            A("'13 numbers, ÷ 12: only 12 remainders (0 to 11)' appears",
              T('$13$ numbers, $\\div\\,12$: only $12$ remainders ($0$ to $11$)', size=44, gap=50)),
            "The exam version uses remainders. Divide any number by twelve: the remainder is zero to eleven. Twelve options.",
            "Take thirteen numbers. Two of them must have the same remainder.",
            D('Write "17 = 12 + 5,  41 = 36 + 5 → 41 − 17 = 24 = 2 · 12"'),
            "And two numbers with the same remainder? Their difference divides by twelve.",
            "Seventeen and forty-one: both have remainder five. The difference is twenty-four — two times twelve.",
        ]),
        dict(mode='concept', active=4, title='To be sure', script=[
            A("'To be sure: worst luck first, then one more' appears", T('"To be sure": worst luck first, then one more', size=46, gap=50)),
            "A classic question: how many must you take to be SURE?",
            "Imagine the worst luck. One item in every box — and nothing matches yet.",
            "Then one more item. Now something must match.",
            D('Write "4 colors → 4 socks can all differ → 5 socks = a sure pair"'),
            "Four sock colors: four socks can all be different. The fifth one must match one of them.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            "Let's lock it in.",
            A("'From a to b: b − a + 1' appears", T('From $a$ to $b$: $\\ b-a+1$', size=40)),
            A("'Strictly between: b − a − 1' appears", T('Strictly between: $\\ b-a-1$', size=40)),
            A("'Every second number: (last − first)/2 + 1' appears", T('Every second number: $\\ \\frac{\\text{last}-\\text{first}}{2}+1$', size=40)),
            A("'Pigeonhole: more items than boxes' appears", T('Pigeonhole: more items than boxes', size=40)),
            A("'To be sure: worst luck, then one more' appears", T('To be sure: worst luck, then one more', size=40)),
            D('Tick each line'),
            "Two questions next. Then practice on your own — and you've finished algebra.",
        ]),
    ], SEC, after='solve-q-580')

    M.new_q(g3, TOPIC, 'How many odd numbers are there between $20$ and $80$?', ['$29$', '$30$', '$31$', '$60$'], 2, [
        'The first odd number is $21$ and the last is $79$.',
        'Every second number: $\\frac{79-21}{2}+1=29+1=30$.',
        'Another way: from $21$ to $80$ there are $80-21+1=60$ numbers. They alternate odd, even, and exactly half of them are odd: $60\\div2=30$.'])
    M.place_q(g3, SEC, after=COUNT)
    _solution(M, g3, ["Question seven.", "Counting odd numbers — without listing them."], [
        ('Method 1 · First and last', [
            "Odd numbers between twenty and eighty. Twenty and eighty are even — they don't count anyway.",
            D('Under the question write "first: 21, last: 79"'),
            "The first odd number is twenty-one. The last is seventy-nine.",
            D('Write "(79 − 21) ÷ 2 + 1 = 29 + 1 = 30"'),
            "Jump by twos. Seventy-nine minus twenty-one is fifty-eight. Half of that: twenty-nine jumps. Plus one for the first number: thirty.",
            D('Circle choice 2'),
            "Choice two. The trap is twenty-nine — forgetting the plus one.",
        ]),
        ('Method 2 · Half of the numbers', [
            "Another way. Count all the numbers from twenty-one to eighty.",
            D('Write "21 to 80: 80 − 21 + 1 = 60 numbers"'),
            "Eighty minus twenty-one, plus one: sixty numbers.",
            "They alternate: odd, even, odd, even. The first is odd and the last is even — so exactly half are odd.",
            D('Write "60 ÷ 2 = 30"'),
            "Sixty divided by two: thirty. Same answer. Choice four, sixty, forgets to halve.",
        ]),
    ])

    M.new_q(g4, TOPIC, 'A drawer holds $5$ red socks, $7$ blue socks and $9$ green socks. Dana takes socks out of the drawer without looking. What is the smallest number of socks she must take out to be sure she has two socks of the same color?',
            ['$2$', '$3$', '$4$', '$10$'], 3, [
        'Think of the worst luck. The first $3$ socks can all be different: one red, one blue, one green.',
        'The $4$th sock is red, blue or green. It must match one of them.',
        'Pigeonhole: $3$ colors are $3$ boxes. $4$ socks in $3$ boxes put two socks in one box. With $3$ socks a pair is not sure, so the answer is $4$.'])
    M.place_q(g4, SEC, after='solve-' + g3)
    _solution(M, g4, ["Question eight.", "To be sure — think of the worst luck."], [
        ('Worst luck', [
            "Three colors. With the worst luck, the first three socks are all different.",
            D('Under the question write "red, blue, green → no pair yet"'),
            "One red, one blue, one green. Three socks — and still no pair.",
            D('Write "4th sock → it matches one of them"'),
            "The fourth sock is red, blue or green. Whatever it is, it matches a sock we already have.",
            D('Circle choice 3'),
            "Four. Choice three.",
            "This is the pigeonhole principle. Three colors are three boxes. Four socks in three boxes — one box gets two.",
            "The numbers five, seven and nine don't matter here. Choice four, ten, is the biggest pile plus one — a different question.",
            "And with that — you've finished algebra.",
        ]),
    ])

    M.new_card('mem-r26-t20-counting', TOPIC, SEC, {
        'title': 'Counting integers and pigeonhole',
        'intro': 'Count the whole numbers in a range without listing them.',
        'tables': [{'title': '', 'head': ['Count', 'Rule', 'Example'], 'rows': [
            ['From $a$ to $b$, both included', '$b-a+1$', '$5$ to $12$: $8$ numbers'],
            ['Strictly between $a$ and $b$', '$b-a-1$', 'between $5$ and $12$: $6$ numbers'],
            ['One end included', '$b-a$', '$5<x\\le12$: $7$ numbers'],
            ['Only odd or only even', '$\\frac{\\text{last}-\\text{first}}{2}+1$', 'odd, $21$ to $79$: $30$ numbers'],
            ['Pigeonhole', 'more items than boxes: one box gets two', '$13$ numbers, only $12$ remainders'],
            ['"To be sure"', 'worst luck (one in each box), then one more', '$3$ colors: $4$ socks']]}],
        'tips': ['Not sure about $+1$ or $-1$? Count a small case by hand.',
                 'Letters in the choices? Plug in small numbers and count. If two choices match, try a second number.',
                 'Two numbers with the same remainder when divided by $n$: their difference divides by $n$.'],
    }, after='solve-' + g4)

    # =====================================================================================
    # 6. Practice: text of every question
    # =====================================================================================
    S('q-581', stem='Given: $a$, $b$ and $c$ are integers, and $0<c<b<a$. Which of the following cannot be true?',
      expl=['(4) cannot be true: $b=1$ needs an integer $c$ with $0<c<1$, and there is none.',
            'The others can happen: (1) $c=1$, $b=3$, $a=4$; (2) $c=2$, $b=3$, $a=4$; (3) $0<2<3<6$ ✓.'])
    S('q-582', stem='Given: $a$, $b$ and $c$ are different even numbers, and\n$\\begin{cases} a<b<c \\\\ c-a<8 \\end{cases}$\n$x=b-a$. Which of the following could be the value of $x$?',
      expl=['The difference of two even numbers is even. Therefore $x\\ne1$.',
            'Even numbers leave gaps of $2$: $c\\ge b+2$. Therefore $c-a\\ge x+2$.',
            'Also $c-a$ is even and less than $8$. Therefore $c-a\\le6$, and $x+2\\le6$ gives $x\\le4$. This rules out $6$ and $8$.',
            '$x=2$ works: $(a,b,c)=(2,4,6)$ gives $c-a=4<8$ ✓.'])
    S('q-583', stem='Nadia chose $13$ different positive integers. Among them there must be two numbers whose difference is divisible by —',
      expl=['Pigeonhole: when you divide by $12$, there are only $12$ possible remainders ($0$ to $11$). With $13$ numbers, two of them have the same remainder.',
            'Two numbers with the same remainder have a difference divisible by $12$. For example, $17$ and $41$ both leave remainder $5$, and $41-17=24=2\\cdot12$.',
            'For $13$, $14$ and $15$ this is not sure: Nadia could choose $1, 2, \\ldots, 13$. Their differences are at most $12$, so none of them is divisible by $13$, $14$ or $15$.'])
    S('q-584', stem='Given: $a$, $b$ and $c$ are different positive integers, and\n$\\begin{cases} a<b<c \\\\ a+b+c=12 \\end{cases}$\nWhat is the smallest possible value of $c-a$?',
      expl=['Test the answers, starting from the smallest. $c-a=1$ is impossible: there is no integer $b$ between $a$ and $a+1$.',
            '$c-a=2$ means three numbers in a row: $a$, $a+1$, $a+2$. Their sum is $3a+3=12$. Therefore $a=3$, and the numbers are $3$, $4$, $5$ ✓.',
            'The smallest value of $c-a$ is $2$.'])
    S('q-585', stem='Given: $x$, $y$ and $z$ are different positive integers. Look at the three fractions $\\frac{x}{y}$, $\\frac{y}{z}$ and $\\frac{z}{x}$. Which of the following cannot be true?',
      choices=['Exactly one of the fractions is smaller than $1$.', 'Exactly two of the fractions are smaller than $1$.',
               'The sum of the three fractions is greater than $1$.', 'Each of the three fractions is greater than $1$.'],
      expl=['Multiply the three fractions: $\\frac xy\\cdot\\frac yz\\cdot\\frac zx=1$. Everything cancels.',
            'If each fraction were greater than $1$, their product would be greater than $1$. Therefore (4) cannot be true.',
            'The others can happen. $x=3$, $y=2$, $z=1$ give $\\frac32$, $2$, $\\frac13$: exactly one is smaller than $1$, and the sum is greater than $1$. $x=1$, $y=2$, $z=3$ give $\\frac12$, $\\frac23$, $3$: exactly two are smaller than $1$.'])
    S('q-586', stem='Given: $x$ is an odd number, $y$ is an even number, and $x<y$. How many odd numbers are greater than $x$ and smaller than $y$?',
      expl=['Plug in $x=1$ and $y=6$. The odd numbers between them are $3$ and $5$: two numbers.',
            'Put $x=1$, $y=6$ into the choices: (1) $\\frac52$ ✗, (2) $\\frac32$ ✗, (3) $\\frac62+1=4$ ✗, (4) $\\frac{6-1-1}{2}=2$ ✓.',
            'With the counting rule: the first odd number is $x+2$ and the last is $y-1$. Their count is $\\frac{(y-1)-(x+2)}{2}+1=\\frac{y-x-1}{2}$.'])
    S('q-587', stem='Given: $a$, $b$ and $c$ are three different integers, and $a+b+c=25$. Which of the following is necessarily true?',
      choices=['$b$ is not equal to the average of $a$ and $c$.', 'The smallest of the three numbers is odd.', '$c\\ne5$',
               'The sum of any two of the numbers is greater than the third.'],
      expl=['Break the wrong choices with examples. For (2), $(a,b,c)=(2,3,20)$ has smallest number $2$, even ✗. For (3), $(3,17,5)$ has $c=5$ ✗. For (4), $(1,2,22)$ has $1+2<22$ ✗.',
            'Why (1) is always true: if $b$ were the average of $a$ and $c$, then $a+c=2b$ and $a+b+c=3b=25$. But $25$ is not divisible by $3$.'])
    S('q-588', stem='Given: $a$ and $x$ are positive integers, and $a<x<3a$. For a fixed value of $a$, how many different values can $x$ take?',
      expl=['Plug in $a=2$: $2<x<6$. The values of $x$ are $3$, $4$ and $5$: three values.',
            'Only $2a-1$ gives $3$. The others give $2a=4$, $2a+1=5$ and $a-1=1$.',
            'With the counting rule: strictly between $a$ and $3a$ there are $3a-a-1=2a-1$ integers.'])
    S('q-589', stem='Given: $a$ is a positive number, and $y=a^a$. If $a$ is multiplied by $3$, by what factor is $y$ multiplied?',
      expl=['The new value is $(3a)^{3a}=3^{3a}\\cdot a^{3a}$.',
            'Divide by the old value: $\\frac{3^{3a}\\cdot a^{3a}}{a^a}=3^{3a}\\cdot a^{2a}$.',
            'Check with $a=1$: $y=1$ becomes $3^3=27$. Only (4) gives $27$: $3^3\\cdot1^2=27$.'])
    S('q-590', stem='On a board there are $13$ different positive integers. Each of them begins with the digit $5$ and ends with the digit $2$. Which of the following cannot be true?',
      choices=['All the numbers use only the digits $5$ and $2$.', 'All the numbers have at most $3$ digits.',
               'All the numbers have at least $5$ digits.', 'All the numbers are divisible by $9$.'],
      expl=['Count the numbers with at most $3$ digits that begin with $5$ and end with $2$: $52$, and $502, 512, \\ldots, 592$ (ten numbers). That is only $11$ numbers.',
            'You cannot choose $13$ different numbers from $11$. Therefore (2) cannot be true.',
            'The others can happen, because there are endless numbers of each kind. For example: (1) $52, 522, 552, 5222, \\ldots$; (4) $522=9\\cdot58$, and $5022$ and $5112$ also have digit sum $9$.'])

    S('alg-extra-unit-t20-2-1', stem='Three different positive integers have a sum of $23$. What is the greatest possible value of the largest of them?',
      choices=['$21$', '$20$', '$18$', '$19$'],
      expl=['To make the largest number big, make the other two as small as possible: $1$ and $2$.',
            'The largest is $23-1-2=20$. The numbers $1$, $2$, $20$ fit ✓.'])
    S('alg-extra-unit-t20-2-2', stem='Given: $a$ and $b$ are positive numbers, and $a+b=12$. What is the greatest possible value of $ab$?',
      choices=['$36$', '$24$', '$30$', '$48$'],
      expl=['Test pairs with sum $12$: $4\\cdot8=32$, $5\\cdot7=35$, $6\\cdot6=36$. The closer the two numbers, the bigger the product.',
            '$48$ is too big, and $24$ and $30$ are possible but not the greatest. The answer is $36$.',
            'Algebra: $(a-b)^2\\ge0$ gives $(a+b)^2\\ge4ab$. Therefore $144\\ge4ab$ and $ab\\le36$.'])
    S('alg-extra-unit-t20-2-3', stem='Given: $x^2+y^2=0$. Which of the following must be true?',
      expl=['A square is never negative: $x^2\\ge0$ and $y^2\\ge0$.',
            'Two numbers that are not negative add up to $0$ only if both are $0$. Therefore $x=y=0$.'])
    S('alg-extra-unit-t20-2-4', stem='$a$ and $b$ are two different positive integers. Which of the following is not necessarily true?',
      choices=['Their sum is odd.', 'Their sum is at least $3$.', 'Their product is positive.', 'Their difference is not $0$.'],
      expl=['Plug in $a=1$ and $b=3$: the sum is $4$, even. Therefore (1) is not necessarily true.',
            'The others are always true: the smallest sum is $1+2=3$; a positive number times a positive number is positive; different numbers have a difference that is not $0$.'])
    S('alg-extra-unit-t20-2-5', stem='Given: $n$ is a positive integer, and $4<n<9$. Which of the following cannot be the value of $n^2$?',
      choices=['$36$', '$49$', '$37$', '$25$'],
      expl=['The possible values of $n$ are $5$, $6$, $7$, $8$. Their squares are $25$, $36$, $49$, $64$.',
            '$37$ is not on the list.'])
    S('alg-extra-unit-t20-2-7', stem='Given:\n$\\begin{cases} x+y=9 \\\\ x-y=3 \\end{cases}$\nWhich of the following gives $xy$ without finding $x$ and $y$ first?',
      expl=['$(x+y)^2-(x-y)^2=4xy$. Therefore $xy=\\frac{9^2-3^2}{4}=\\frac{81-9}{4}=18$.',
            'Check: $x=6$ and $y=3$ give $x+y=9$, $x-y=3$ and $xy=18$ ✓.'])
    # Pass 2: the original is restored (plan), cleaned up.
    S('alg-extra-unit-t20-2-6', stem='Given: $a$ and $b$ are numbers, and $a^2=b^2$. Which of the following is necessarily true?',
      expl=['$a^2-b^2=0$, so $(a-b)(a+b)=0$. Therefore $a=b$ or $a=-b$. In both cases $|a|=|b|$.',
            'The others are not necessarily true: $a=2$, $b=-2$ gives $a\\ne b$; $a=b=2$ gives $a\\ne-b$ and $a+b=4\\ne0$.'])

    # =====================================================================================
    # 7. New practice questions (exam level)
    # =====================================================================================
    P = {}
    P['05'] = ('Given: $0<x<1$. Which of the following is the smallest?',
               ['$x$', '$\\frac{1}{x}$', '$\\sqrt{x}$', '$x^2$'], 4, [
        'Plug in one number from the range: $x=\\frac14$.',
        '$x=\\frac14$, $\\frac1x=4$, $\\sqrt x=\\frac12$, $x^2=\\frac1{16}$. The smallest is $x^2$.',
        'Rule: for $0<x<1$, $x^2<x<\\sqrt x<1<\\frac1x$.'])
    P['06'] = ('Given: $x<y<0$. Which of the following must be true?',
               ['$xy<0$', '$\\frac{x}{y}<1$', '$x^2>y^2$', '$x+y>0$'], 3, [
        'Plug in $x=-3$ and $y=-2$: (1) $xy=6$ ✗, (2) $\\frac xy=\\frac32$ ✗, (3) $9>4$ ✓, (4) $x+y=-5$ ✗.',
        'Why (3) is always true: $x$ is farther from $0$ than $y$. Therefore $x^2>y^2$.'])
    P['07'] = ('How many integers $x$ satisfy $10<x^2<100$?', ['$6$', '$12$', '$14$', '$89$'], 2, [
        'The squares between $10$ and $100$ are $16, 25, 36, 49, 64, 81$. They come from $x=4, 5, 6, 7, 8, 9$.',
        'Negative numbers work too: $(-4)^2=16$, $(-5)^2=25$, … Therefore $x$ can also be $-4, -5, \\ldots, -9$.',
        'In total $6+6=12$ integers. The trap $6$ forgets the negative numbers.'])
    P['08'] = ('Given: $n$ is a positive integer. How many even numbers are there from $2n$ to $8n$, both included?',
               ['$3n$', '$3n+1$', '$6n+1$', '$4n$'], 2, [
        'Plug in $n=1$: the even numbers from $2$ to $8$ are $2, 4, 6, 8$: four numbers. Both $3n+1$ and $4n$ give $4$.',
        'Two choices survive. Try a second number: $n=2$ gives $4, 6, 8, \\ldots, 16$: seven numbers. $3n+1=7$ ✓ and $4n=8$ ✗.',
        'With the counting rule: $\\frac{8n-2n}{2}+1=3n+1$.'])
    P['09'] = ('A drawer holds $5$ red socks, $7$ blue socks and $9$ green socks. Ron takes socks out of the drawer without looking. What is the smallest number of socks he must take out to be sure he has two blue socks?',
               ['$4$', '$9$', '$16$', '$21$'], 3, [
        'Worst luck: all the socks that are not blue come out first. That is $5+9=14$ socks.',
        'Then the next two socks must both be blue: $14+2=16$.',
        'With $15$ socks he could still have only one blue sock. Therefore $16$ is the smallest number.'])
    P['10'] = ('Given:\n$\\begin{cases} x>0,\\ y>0 \\\\ x^3=y^2 \\end{cases}$\nIf $y$ is multiplied by $8$, by what factor is $x$ multiplied?',
               ['$2$', '$4$', '$8$', '$64$'], 2, [
        'Plug in $x=1$ and $y=1$. Multiply $y$ by $8$: $y=8$ gives $x^3=64$ and $x=4$.',
        'Algebra: $y^2$ is multiplied by $8^2=64$. Therefore $x^3$ is multiplied by $64$, and $x$ by $\\sqrt[3]{64}=4$.'])
    P['11'] = ('The price each passenger pays for a shared taxi ride is given by a formula. The price increases when the distance ($d$) increases, and decreases when the number of passengers ($n$) increases. $d$ and $n$ are both greater than $1$. Which of the following expressions cannot give the price?',
               ['$\\frac{d}{n}$', '$\\frac{n}{d}$', '$d-n$', '$\\frac{d^2}{n}$'], 2, [
        'A valid formula must grow when $d$ grows and shrink when $n$ grows.',
        '(1) $\\frac dn$ and (4) $\\frac{d^2}{n}$: $d$ is on top and $n$ is on the bottom ✓. (3) $d-n$: $d$ is added and $n$ is subtracted ✓.',
        'In (2), $\\frac nd$, a bigger $d$ makes the fraction SMALLER, and a bigger $n$ makes it BIGGER. Both are the opposite of the rule. Therefore (2) cannot give the price.'])
    P['12'] = ('Given: $x^2<x$. Which of the following must be true?',
               ['$x^3<x^2$', '$\\frac{1}{x}<2$', '$\\sqrt{x}<x$', '$x<\\frac12$'], 1, [
        'First find the allowed numbers. For $x\\le0$ or $x\\ge1$, $x^2\\ge x$. Only $0<x<1$ gives $x^2<x$ (for example $x=\\frac12$: $\\frac14<\\frac12$).',
        'Plug in numbers from the range. $x=\\frac14$: (2) $\\frac1x=4$ ✗, (3) $\\sqrt x=\\frac12>\\frac14$ ✗. $x=\\frac34$: (4) ✗.',
        '(1) is always true: $x^3=x\\cdot x^2$ is $x^2$ times a number smaller than $1$. Therefore $x^3<x^2$.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t20-' + k, TOPIC, stem, ch, cor, ex)
        M.place_q('q-r26-t20-' + k, PRAC)

    # =====================================================================================
    # 8. Practice order: easy -> hard
    # =====================================================================================
    M.practice_order(PRAC, [
        'alg-extra-unit-t20-2-5', 'alg-extra-unit-t20-2-1', 'alg-extra-unit-t20-2-4', 'alg-extra-unit-t20-2-3', 'alg-extra-unit-t20-2-6',
        'alg-extra-unit-t20-2-2', 'alg-extra-unit-t20-2-7', 'q-581', 'q-r26-t20-05', 'q-582', 'q-584',
        'q-r26-t20-06', 'q-588', 'q-r26-t20-11', 'q-586', 'q-r26-t20-08', 'q-587', 'q-r26-t20-10', 'q-585',
        'q-r26-t20-07', 'q-583', 'q-r26-t20-09', 'q-r26-t20-12', 'q-589', 'q-590'])

    summary(M)
    cut_repeats(M)   # 2026-10-05: last


def _b(label, tex, size=44):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summary(M):
    """Pass 2: a summary lesson right before the independent practice (end of the 'understanding' section)."""
    last = [f['ref'] for f in M.D['flow'] if f['section'] == SEC][-1]
    sb = ['Three tools', 'Must, could, cannot', 'Which numbers?', 'Between 0 and 1', 'Integer gaps', 'Scaling',
          'Connect topics', 'Counting integers', 'Pigeonhole', 'Before you practice']
    M.new_video('r26-t20-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            "A quick summary before you practice on your own.",
            "Everything from algebraic understanding — in about three minutes."]),
        dict(mode='concept', active=0, title='Three tools', script=[
            _b('Plug in → test the answers → algebra', 'Plug in numbers $\\to$ test the answers $\\to$ algebra'),
            "No fixed recipe here — but three tools open almost every question.",
            "Numbers first: fast and safe. Then the answers. Algebra when the numbers don't decide."]),
        dict(mode='concept', active=1, title='Must, could, cannot', script=[
            _b('Must — every allowed case', 'Must be true — every allowed case', size=40),
            _b('Could — one allowed case', 'Could be true — at least one allowed case', size=40),
            _b('Cannot — no allowed case', 'Cannot be true — no allowed case', size=40),
            _b('Not necessarily — fails once', 'Not necessarily true — fails in at least one case', size=40),
            "Must: one case that fails, and it's out. Could: one example is enough.",
            "Write the word down before you touch the choices. Under pressure, the directions flip."]),
        dict(mode='concept', active=2, title='Which numbers?', script=[
            _b('Regions: x > 1 · 0 < x < 1 · −1 < x < 0 · x < −1', 'One number from each region: $x>1$;  $0<x<1$;  $-1<x<0$;  $x<-1$', size=40),
            "Read the conditions first. Test only numbers they allow.",
            "Then one number from each region. For x positive: two, and one half.",
            _b('Letters may be equal? Try a = b too.', 'Letters may be equal? Try $a=b$ too.', size=40),
            _b('Two choices survive? A second number.', 'Two choices survive? Try a second number.', size=40),
            "Two choices left? Don't guess — try a number from another region."]),
        dict(mode='concept', active=3, title='Between 0 and 1', script=[
            _b('0 < x < 1: x² < x < √x < 1 < 1/x', '$0<x<1:\\quad x^2<x<\\sqrt{x}<1<\\frac{1}{x}$', size=50),
            "Between zero and one, squaring makes a number smaller, and the root makes it bigger.",
            _b('Negatives: −7 < −3', 'Negatives: $-7<-3$ — farther from $0$ means smaller', size=40),
            "With negatives, the farther from zero, the smaller.",
            "Which is the largest for every x in a range? One easy number from the range decides."]),
        dict(mode='concept', active=4, title='Integer gaps', script=[
            _b('Integer and < 20 → ≤ 19', 'Integer and $<20\\ \\to\\ \\le19$', size=44),
            _b('a > b > c integers → a ≥ c + 2', '$a>b>c$ integers $\\to$ $a\\ge b+1\\ge c+2$', size=44),
            "Integers leave gaps. Bigger means bigger by at least one.",
            "Use the gaps to find the biggest or smallest possible value.",
            "A cannot question with a hidden maximum? Test the most extreme choices first."]),
        dict(mode='concept', active=5, title='Scaling', script=[
            _b('x² = a³, a × 4 → x × 8', '$x^2=a^3:\\quad a\\times4\\ \\to\\ x\\times4^{\\frac32}=x\\times8$', size=44),
            "One variable is multiplied — what happens to the other?",
            "Start from one and one, then put in the new value. Four cubed is sixty-four. Its root: eight.",
            "Or the rule: x changes by the factor to the power three halves."]),
        dict(mode='concept', active=6, title='Connect topics', script=[
            _b('c² = a² + b², all positive → c > a, c > b', '$c^2=a^2+b^2$, all positive $\\to$ $c>a$ and $c>b$', size=42),
            "A structure from another topic can be the key.",
            _b('x/y · y/z · z/x = 1', '$\\frac{x}{y}\\cdot\\frac{y}{z}\\cdot\\frac{z}{x}=1$', size=50),
            "A cycle of ratios cancels to one — so the three can't all be bigger than one.",
            "Check the givens before you use it: positive values, nothing equal to zero."]),
        dict(mode='concept', active=7, title='Counting integers', script=[
            _b('From a to b: b − a + 1', 'From $a$ to $b$, both included: $\\ b-a+1$', size=42),
            _b('Strictly between: b − a − 1', 'Strictly between: $\\ b-a-1\\quad$ One end: $\\ b-a$', size=42),
            _b('Every second number: (last − first)/2 + 1', 'Only odd or even: $\\ \\frac{\\text{last}-\\text{first}}{2}+1$', size=42),
            "Both ends in: plus one. Both ends out: minus one. One end: just subtract.",
            "Only odd or only even numbers: find the first and the last that count, then jump by two.",
            "Not sure? Count a small case on your fingers."]),
        dict(mode='concept', active=8, title='Pigeonhole', script=[
            _b('More items than boxes → one box gets two', 'More items than boxes $\\to$ one box gets two', size=42),
            "Eight numbers, but only seven remainders when you divide by seven. Two of them share a remainder — and their difference is divisible by seven.",
            _b('To be sure: worst luck, then one more', '"To be sure": worst luck first, then one more', size=42),
            "To be sure? Imagine the worst luck — one in every box. Then one more."]),
        dict(mode='concept', active=9, title='Before you practice', script=[
            "Before every question, ask yourself:",
            _b('Must, could or cannot?', 'Must, could or cannot? Did I write the word?', size=40),
            _b('Which numbers are allowed?', 'Which numbers are allowed? Did I try every region?', size=40),
            _b('Integers? Where are the gaps?', 'Integers? Where are the gaps?', size=40),
            _b('Both ends included?', 'Counting: are the ends included?', size=40),
            _b('Traps: 0 < x < 1 · negatives · +1', 'Traps: numbers between $0$ and $1$ · negatives · the $+1$', size=38),
            "The traps: numbers between zero and one, negative numbers, and the forgotten plus one.",
            "Then practice on your own — and you've finished algebra. Good luck."]),
    ], SEC, after=last)


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
    # ---- "Algebraic Understanding" -> the Hebrew intro (what the topic is + the three tools).
    #      Must/could/cannot -> Topic 1 + Q1, Q3, Q5 (+ "write the word" in Q1); which numbers -> Q1 (+ equal letters);
    #      between 0 and 1 -> Q1, Q2; integer gaps -> Q3 (+ the general rule); scaling -> Q4 (its lesson example was
    #      the same question with x16); connect topics -> Q5 (+ the cycle of ratios).
    _cr_cut(M, LESSON, ['Must, could, cannot', 'Which numbers?', 'Between 0 and 1', 'Integer gaps', 'Scaling',
                        'Connect topics', 'Recap'])
    _cr_say(M, LESSON, 2, 'But this lesson, and the practice after it',
            'But the questions, and the practice after them, give you tools that open your head for questions like these.')
    _cr_add(M, LESSON, 2, None, ['As usual, we start with sample questions. Two on plugging in first — then four with more than one way in.'])
    q1 = 'solve-q-r26-t20-01'
    _cr_add(M, q1, 2, 'x and y are positive, and x is bigger than y', [
        D('Write "MUST" in a corner and circle it'),
        "First habit: write the word — must, could, cannot. Under pressure, the directions flip."])
    _cr_add(M, q1, 3, 'Both brackets are positive', [
        A("'Letters may be equal? Try a = b too' appears", T('Letters may be equal? Try equal values too', size=36)),
        "One more rule for plugging in: if the letters may be equal, try equal values too. Here x is bigger than y — so they can't be."])
    _cr_add(M, 'solve-q-577', 2, 'Therefore c is at least two below a', [
        A("'n increasing integers: last ≥ first + (n − 1)' appears", T('$n$ increasing integers: last $\\ge$ first $+\\,(n-1)$', size=36)),
        "In general: n integers, each bigger than the one before — the last is at least the first, plus n minus one."])
    _cr_say(M, 'solve-q-578', 3, 'The general rule from the lesson',
            'The general rule: x changes by the factor to the power three halves. Root nine is three. Three cubed is twenty-seven.')
    _cr_add(M, 'solve-q-579', 3, None, [
        A("'x/y · y/z · z/x = 1' appears", T('$\\frac{x}{y}\\cdot\\frac{y}{z}\\cdot\\frac{z}{x}=1$ — not all three can be $>1$', size=36)),
        "One more structure from another place: a cycle of ratios cancels to one — so the three fractions can't all be bigger than one. Check the givens first: no letter may be zero."])

    # ---- "Counting Integers & Pigeonhole": only odd or even -> Q7; to be sure -> Q8.
    #      Kept: from a to b, strictly between (+ the letters tip), pigeonhole (the remainder version is not in Q8).
    _cr_cut(M, COUNT, ['Only odd or even', 'To be sure', 'Recap'])
    _cr_add(M, COUNT, 3, None, [
        A("'Letters in the choices? Plug in small numbers and count' appears", T('Letters in the choices? Plug in small numbers and count', size=38)),
        "And if the answers have letters — plug in small numbers, count by hand, and see which formula gives your count."])
    _cr_add(M, COUNT, 4, None, ['Two questions next — counting odd numbers, and being sure. Then practice on your own — and you\'ve finished algebra.'])


# =====================================================================================
# 2026-10-06 practice: the new exam methods as an extra method in PRACTICE explanations
# (append only; the existing worked solution stays as it is). Runs last.
# =====================================================================================
PRACTICE_METHODS = {
    'q-r26-t20-10': [
        'Method 2 · Given power, asked power: the given is $x^3=y^2$, and the asked power of $x$ is $1$. So $r=\\frac13$: raise both sides to $\\frac13$, and $x=y^{\\frac23}$.',
        'Multiply $y$ by $8$, and $x$ is multiplied by $8^{\\frac23}=\\left(\\sqrt[3]{8}\\right)^2=4$.',
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


# ======================================================================================================
# 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived question (guided q-577 .. q-580,
# practice q-581 .. q-590) gets new numbers / letters / story - same concept, same trap, same level, at least the same
# methods - and every guided solution video is rewritten to match. The Hebrew lesson's own examples were already cut
# (cut_repeats); the card tips that still quoted the Hebrew numbers (12 -> 11, 9^(3/2) = 27) and the card examples that
# equalled a guided question get new numbers. q-580 (no calculation) moves before q-577 (easy -> hard).
# Plus the approved practice clean-up (25 -> 15). Nothing in topic 20 is recorded. Runs last.
# ======================================================================================================
RN_RECORDED = set()   # no take of any topic-20 video in ~/Documents/Course.recordings (checked 2026-10-06)


def _rn_item(M, vid, n, text):
    """An existing pop-in board item of a slide (to keep it when the slide's script is rewritten)."""
    b = M.slide(vid, n)
    for l in b['lines']:
        if 'appear' in l and text in (b['items'][l['appear']].get('t') or ''):
            return A(l['label'], b['items'][l['appear']])
    raise AssertionError('%s #%d: no item %s' % (vid, n, text))


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. The pre-loaded question stays."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script)
    _sync_video(M, qid)


def rn_guided(M):
    # ---------- q-577: c<b<a integers, a+b<12, b+c cannot be 1, -1, 10, -10 (10)
    #            ==>  a+b<16, b+c cannot be 2, -2, -14, 14 (14; the maximum is 13)
    _rn_q(M, 'q-577', 'Given: $a$, $b$ and $c$ are integers, and\n$\\begin{cases} c<b<a \\\\ a+b<16 \\end{cases}$\nWhich of the following cannot be the value of $b+c$?',
          ['$2$', '$-2$', '$-14$', '$14$'], 4, [
        'The numbers are integers. Therefore $a+b<16$ means $a+b\\le15$.',
        'Also $c\\le b-1$ and $b\\le a-1$. Therefore $c\\le a-2$, and $a-c\\ge2$.',
        '$b+c=(a+b)-(a-c)\\le15-2=13$. The biggest possible value of $b+c$ is $13$ (for example $a=8$, $b=7$, $c=6$). Therefore $b+c=14$ is impossible.',
        'The other values are possible: $(a,b,c)=(3,2,0)$ gives $2$; $(1,0,-2)$ gives $-2$; $(1,0,-14)$ gives $-14$.'])
    gap_item = _rn_item(M, 'solve-q-577', 2, 'increasing integers')
    _rn_video(M, 'q-577', [[
        "Three integers, c below b below a. And a plus b is less than sixteen.",
        "They ask what b plus c CANNOT be. So let's find the biggest b plus c can ever be.",
        D('Under the question write "a + b ≤ 15"'),
        "a and b are integers. Less than sixteen means at most fifteen.",
        "Now compare. a plus b is the two biggest numbers. b plus c is the two smallest. The difference between them is a minus c.",
        D('Write "c ≤ a − 2 → a − c ≥ 2"'),
        "c is at least one below b, and b is at least one below a. Therefore c is at least two below a.",
        gap_item,
        "In general: n integers, each bigger than the one before — the last is at least the first, plus n minus one.",
        D('Write "b + c = (a + b) − (a − c) ≤ 15 − 2 = 13"'),
        "b plus c is a plus b, minus the difference a minus c. At most fifteen, minus at least two: at most thirteen.",
        D('Circle choice 4'),
        "Fourteen goes past the maximum. It can't happen. Choice four.",
    ], [
        "Second way: plug in numbers that make b plus c as big as possible.",
        "We want b as big as it can be — then c can be big too.",
        D('Write "a = 8, b = 7 → a + b = 15 ✓"'),
        "Eight and seven: fifteen, still under sixteen. That's the biggest b we can get.",
        D('Write "c = 6 → b + c = 13"'),
        "Push a up to nine, and b drops to six — worse. So the biggest c is six, and the biggest b plus c is thirteen.",
        D('Circle choice 4'),
        "Again — fourteen is out of reach. Choice four.",
    ], [
        "Third way: test the answers. Which value can't b plus c be?",
        "A maximum is hidden here. So start with the most extreme choices: fourteen and minus fourteen.",
        D('Next to choice 4 write "b = 8, c = 6, a ≥ 9 → a + b ≥ 17 ✗"'),
        "Fourteen: b is bigger than c. The smallest b is eight, with c six. Then a is at least nine — and a plus b is at least seventeen. Too big.",
        D('Circle choice 4'),
        "Found it. Choice four.",
        "Want to be safe? The other choices are easy to make.",
        D('Next to choice 3 write "(a, b, c) = (1, 0, −14) ✓", next to choice 1 "(3, 2, 0) ✓", next to choice 2 "(1, 0, −2) ✓"'),
        "Minus fourteen: a one, b zero, c minus fourteen. Two: a three, b two, c zero. Minus two: a one, b zero, c minus two. All allowed.",
        "Three methods, all excellent. Pick the one that's comfortable for you.",
    ]])

    # ---------- q-578: x^2 = a^3, a x 9 -> x x 27 (36, 18, 27, 9)  ==>  y^2 = b^3, b x 25 -> y x 125 (125, 50, 100, 25)
    _rn_q(M, 'q-578', 'Given:\n$\\begin{cases} b>0,\\ y>0 \\\\ y^2=b^3 \\end{cases}$\nIf $b$ is multiplied by $25$, by what factor is $y$ multiplied?',
          ['$125$', '$50$', '$100$', '$25$'], 1, [
        'Plug in: $b=1$ gives $y^2=1$ and $y=1$ (because $y>0$).',
        'Multiply $b$ by $25$: $b=25$ gives $y^2=25^3=(5^2)^3=5^6$ and $y=5^3=125$. $y$ went from $1$ to $125$: it was multiplied by $125$.',
        'Algebra: $(ky)^2=(25b)^3$ gives $k^2y^2=25^3b^3$. Since $y^2=b^3$, $k^2=25^3=5^6$ and $k=5^3=125$.',
        'General rule: $y=b^{\\frac32}$. Therefore $y$ is multiplied by $25^{\\frac32}=(\\sqrt{25})^3=5^3=125$.'])
    _rn_video(M, 'q-578', [[
        "y squared equals b cubed, both positive. b gets multiplied by twenty-five. What happens to y?",
        "Plug in two numbers that satisfy the equation. The simplest pair: one and one.",
        D('Write "b = 1 → y² = 1 → y = 1"'),
        "Didn't spot it? Put b equal to one: y squared is one. y is plus or minus one — and y is positive. So y is one.",
        D('Write "b = 25 → y² = 25³ = (5²)³ = 5⁶"'),
        "Now multiply b by twenty-five. The new b is twenty-five. Twenty-five is five squared — so twenty-five cubed is five to the sixth.",
        D('Write "y = 5³ = 125"'),
        "What squared gives five to the sixth? Five cubed: a hundred twenty-five. Positive again.",
        D('Circle choice 1'),
        "y went from one to a hundred twenty-five. It grew a hundred twenty-five times. Choice one.",
    ], [
        "Now the mathematical solution.",
        "Multiply b by twenty-five. The right side becomes twenty-five b, all cubed.",
        "To keep the equation balanced, y must grow too. By how much? Call it k.",
        D('Write "(ky)² = (25b)³"'),
        D('Write "k²·y² = 25³·b³"'),
        "Open the brackets with the power rules: k squared y squared equals twenty-five cubed b cubed.",
        D('Cross out y² and b³ (they are equal)'),
        "But y squared equals b cubed. They cancel.",
        D('Write "k² = 25³ = 5⁶ → k = 5³ = 125"'),
        "k squared is twenty-five cubed — five to the sixth. k is five cubed: a hundred twenty-five. Choice one.",
        "Strong algebra students see it in their head: the right side grows twenty-five cubed times. What squared gives that? Twenty-five times five — a hundred twenty-five.",
        "For most students, though, plugging in is the simpler route here.",
        D('Write "y = b^(3/2) → 25^(3/2) = (√25)³ = 5³ = 125"'),
        "The general rule: y changes by the factor to the power three halves. Root twenty-five is five. Five cubed is a hundred twenty-five.",
    ]])

    # ---------- q-579: c^2/(ab) = a/b + b/a; not necessarily: c<a+b, c<6, b<c, a<c (c<6)
    #            ==>  r^2/(pq) = p/q + q/p; q<r, r<p+q, r<8, p<r (r<8)
    _rn_q(M, 'q-579', 'Given: $p$, $q$ and $r$ are different positive integers, and $\\frac{r^2}{pq}=\\frac{p}{q}+\\frac{q}{p}$. Which of the following is not necessarily true?',
          ['$q<r$', '$r<p+q$', '$r<8$', '$p<r$'], 3, [
        'Common denominator: $\\frac pq+\\frac qp=\\frac{p^2}{pq}+\\frac{q^2}{pq}=\\frac{p^2+q^2}{pq}$. Therefore $r^2=p^2+q^2$.',
        '(1) and (4) are always true: $r^2=p^2+q^2>q^2$, and all the numbers are positive. Therefore $r>q$. In the same way, $r>p$.',
        '(2) is always true: $(p+q)^2=p^2+2pq+q^2=r^2+2pq>r^2$. Therefore $p+q>r$.',
        '(3) is not necessarily true: $(p,q,r)=(3,4,5)$ fits ($9+16=25$) and gives $r=5<8$. But $(6,8,10)$ also fits ($36+64=100$) and gives $r=10$.'])
    ratio_item = _rn_item(M, 'solve-q-579', 3, 'frac{x}{y}')
    _rn_video(M, 'q-579', [[
        "Step one: simplify the equation.",
        D('Write "p/q = p²/(pq),  q/p = q²/(pq)"'),
        "Common denominator: p times q. p over q is p squared over p q. q over p is q squared over p q.",
        D('Write "r²/(pq) = (p² + q²)/(pq) → r² = p² + q²"'),
        "Both sides are over p q. So r squared equals p squared plus q squared.",
        "Read the question carefully: which statement is NOT necessarily true?",
        "Anything that's always true — we cross out. We're hunting for the one that can fail.",
    ], [
        D('Next to choice 1 write "r² = p² + q² > q² → r > q" and cross it out'),
        "Choice one: r squared is q squared plus something positive. So r squared is bigger than q squared.",
        "All the numbers are positive. Therefore r is bigger than q. Always. Out.",
        D('Cross out choice 4'),
        "Choice four: the same with p. Always. Out.",
        D('Next to choice 2 write "(p + q)² = r² + 2pq > r²" and cross it out'),
        "Choice two: p plus q, squared, is p squared plus two p q plus q squared. That's r squared plus two p q — bigger than r squared.",
        "So p plus q is bigger than r. Always. Out.",
        "Choice three: r is less than eight. Look for integers that fit.",
        D('Next to choice 3 write "3, 4, 5: 9 + 16 = 25 → r = 5  |  6, 8, 10: 36 + 64 = 100 → r = 10"'),
        "Three, four, five: nine plus sixteen is twenty-five. r is five — less than eight.",
        "Now double them: six, eight, ten. Thirty-six plus sixty-four is a hundred. r is ten — not less than eight.",
        D('Circle choice 3'),
        "Sometimes true, sometimes not. Not necessarily true. Choice three.",
        "In geometry you'll meet r squared equals p squared plus q squared again, as Pythagoras.",
        "And choice two becomes a rule there: the sum of any two sides of a triangle is longer than the third.",
        ratio_item,
        "One more structure from another place: a cycle of ratios cancels to one — so the three fractions can't all be bigger than one. Check the givens first: no letter may be zero.",
        "Next: a short lesson on counting whole numbers.",
    ]])

    # ---------- q-580: plant growth: sunlight S, water W up; weeds D down; S^W/D, SW-D, S-D+W, SWD (SWD)
    #            ==>  game score: coins C, stars S up; mistakes M down; C+S-M, CSM, C^S/M, CS-M (CSM)
    _rn_q(M, 'q-580', "A player's score in a computer game is given by a formula. The score increases when the player collects more coins ($C$) and more stars ($S$), and decreases when the player makes more mistakes ($M$). $C$, $S$ and $M$ are all greater than $1$. Which of the following expressions cannot give the player's score?",
          ['$C+S-M$', '$C\\cdot S\\cdot M$', '$\\frac{C^S}{M}$', '$C\\cdot S-M$'], 2, [
        'A valid formula must grow when $C$ grows, grow when $S$ grows, and shrink when $M$ grows.',
        '(1) $C+S-M$ and (4) $C\\cdot S-M$: $C$ and $S$ are added or multiplied, and $M$ is subtracted ✓.',
        'In (3), $\\frac{C^S}{M}$, a bigger $C$ or $S$ makes the top bigger (because $C>1$), and a bigger $M$ makes the fraction smaller ✓.',
        'In (2), $C\\cdot S\\cdot M$, a bigger $M$ makes the product BIGGER. More mistakes would mean a higher score — the opposite of the rule. Therefore (2) cannot give the score.'])
    _rn_video(M, 'q-580', [[
        "Go back to the rule they defined.",
        D('Under the question write "C↑ → ↑, S↑ → ↑, M↑ → ↓"'),
        "More coins — the score goes up. More stars — up. More mistakes — down.",
        "Now test each expression against all three.",
        D('Next to choice 1 write "✓" and cross it out'),
        "Choice one: C plus S minus M. C and S add, M subtracts. More mistakes, smaller score. It fits. Out.",
        "Choice three: C to the power S, over M.",
        "In a fraction, a bigger top gives a bigger result, a bigger bottom a smaller one.",
        D('Next to choice 3 write "C ✓ S ✓ M ✓" and cross it out'),
        "C grows — the top grows. S grows — C times itself more times, and C is above one — the top grows. M grows — the bottom grows, the result shrinks. It fits. Out.",
        D('Next to choice 4 write "✓" and cross it out'),
        "Choice four: C times S, minus M. Both positive, multiplied — bigger C or S, bigger result. Minus M — more mistakes, smaller score. Out.",
        "Three eliminated — you can mark choice two. But let's check it anyway.",
        D('Next to choice 2 write "M↑ → ↑ ✗" and circle choice 2'),
        "C times S times M. C and S are fine. The problem is M: more mistakes make the score BIGGER. That's the opposite of the rule. Choice two.",
    ]])


def rn_order(M):
    """q-580 (no calculation) moves before q-577: easy -> hard. renumber_guided() renumbers the titles."""
    M.move('q-580', SEC, before='q-577')
    M.move('solve-q-580', SEC, after='q-580')
    _cr_say(M, LESSON, 2, 'As usual, we start with sample questions',
            'As usual, we start with sample questions. Two on plugging in first, then one on reading a formula — and three with more than one way in.')


def rn_cards(M):
    c = M.card('mem-understanding')
    c['tips'] = [t.replace('An integer less than $12$ is at most $11$.', 'An integer less than $20$ is at most $19$.')
                  .replace('For example, $9^{\\frac32}=27$.', 'For example, $4^{\\frac32}=8$.') for t in c['tips']]
    assert any('$20$' in t for t in c['tips']) and any('4^{\\frac32}=8' in t for t in c['tips']), c['tips']
    c = M.card('mem-r26-t20-counting')
    rows = c['tables'][0]['rows']
    for r in rows:
        if r[2] == 'odd, $21$ to $79$: $30$ numbers': r[2] = 'odd, $15$ to $41$: $14$ numbers'
        if r[2] == '$3$ colors: $4$ socks': r[2] = '$4$ colors: $5$ socks'
    assert not any(r[2] in ('odd, $21$ to $79$: $30$ numbers', '$3$ colors: $4$ socks') for r in rows), rows


def rn_practice_questions(M):
    # q-581: 0<c<b<a integers; b=1 and a=3 impossible  ==>  new values, impossible one is choice 2
    _rn_q(M, 'q-581', 'Given: $a$, $b$ and $c$ are integers, and $0<c<b<a$. Which of the following cannot be true?',
          ['$c=3$ and $b=5$', '$b=1$ and $a=4$', '$b=5$ and $a=6$', '$c=3$ and $b=5$ and $a=8$'], 2, [
        '(2) cannot be true: $b=1$ needs an integer $c$ with $0<c<1$, and there is none.',
        'The others can happen: (1) $c=3$, $b=5$, $a=6$; (3) $c=4$, $b=5$, $a=6$; (4) $0<3<5<8$ ✓.'])
    # q-582: even a<b<c, c-a<8, x=b-a could be 1, 2, 6, 8 (2)  ==>  c-a<10: 3, 6, 8, 12 (6)
    _rn_q(M, 'q-582', 'Given: $a$, $b$ and $c$ are different even numbers, and\n$\\begin{cases} a<b<c \\\\ c-a<10 \\end{cases}$\n$x=b-a$. Which of the following could be the value of $x$?',
          ['$3$', '$6$', '$8$', '$12$'], 2, [
        'The difference of two even numbers is even. Therefore $x\\ne3$.',
        'Even numbers leave gaps of $2$: $c\\ge b+2$. Therefore $c-a\\ge x+2$.',
        'Also $c-a$ is even and less than $10$. Therefore $c-a\\le8$, and $x+2\\le8$ gives $x\\le6$. This rules out $8$ and $12$.',
        '$x=6$ works: $(a,b,c)=(2,8,10)$ gives $c-a=8<10$ ✓.'])
    # q-583: 13 numbers -> difference divisible by 12 (12, 13, 14, 15)  ==>  9 numbers -> 8 (8, 9, 10, 11)
    _rn_q(M, 'q-583', 'Yoni chose $9$ different positive integers. Among them there must be two numbers whose difference is divisible by —',
          ['$8$', '$9$', '$10$', '$11$'], 1, [
        'Pigeonhole: when you divide by $8$, there are only $8$ possible remainders ($0$ to $7$). With $9$ numbers, two of them have the same remainder.',
        'Two numbers with the same remainder have a difference divisible by $8$. For example, $13$ and $45$ both leave remainder $5$, and $45-13=32=4\\cdot8$.',
        'For $9$, $10$ and $11$ this is not sure: Yoni could choose $1, 2, \\ldots, 9$. Their differences are at most $8$, so none of them is divisible by $9$, $10$ or $11$.'])
    # q-584: a<b<c distinct positive, sum 12, smallest c-a (2)  ==>  x<y<z, sum 18 (2)
    _rn_q(M, 'q-584', 'Given: $x$, $y$ and $z$ are different positive integers, and\n$\\begin{cases} x<y<z \\\\ x+y+z=18 \\end{cases}$\nWhat is the smallest possible value of $z-x$?',
          ['$1$', '$2$', '$3$', '$4$'], 2, [
        'Test the answers, starting from the smallest. $z-x=1$ is impossible: there is no integer $y$ between $x$ and $x+1$.',
        '$z-x=2$ means three numbers in a row: $x$, $x+1$, $x+2$. Their sum is $3x+3=18$. Therefore $x=5$, and the numbers are $5$, $6$, $7$ ✓.',
        'The smallest value of $z-x$ is $2$.'])
    # q-585: x/y, y/z, z/x (letters only)  ==>  a/b, b/c, c/a; choices reordered
    _rn_q(M, 'q-585', 'Given: $a$, $b$ and $c$ are different positive integers. Look at the three fractions $\\frac{a}{b}$, $\\frac{b}{c}$ and $\\frac{c}{a}$. Which of the following cannot be true?',
          ['Each of the three fractions is greater than $1$.', 'Exactly one of the fractions is smaller than $1$.',
           'The sum of the three fractions is greater than $1$.', 'Exactly two of the fractions are smaller than $1$.'], 1, [
        'Multiply the three fractions: $\\frac ab\\cdot\\frac bc\\cdot\\frac ca=1$. Everything cancels.',
        'If each fraction were greater than $1$, their product would be greater than $1$. Therefore (1) cannot be true.',
        'The others can happen. $a=4$, $b=2$, $c=1$ give $2$, $2$, $\\frac14$: exactly one is smaller than $1$, and the sum is greater than $1$. $a=1$, $b=2$, $c=4$ give $\\frac12$, $\\frac12$, $4$: exactly two are smaller than $1$.'])
    # q-586: x odd < y even, odd numbers strictly between: (y-x-1)/2  ==>  m odd < n even; choices reordered
    _rn_q(M, 'q-586', 'Given: $m$ is an odd number, $n$ is an even number, and $m<n$. How many odd numbers are greater than $m$ and smaller than $n$?',
          ['$\\frac{n-m-1}{2}$', '$\\frac{n-m}{2}$', '$\\frac{n-m+1}{2}+1$', '$\\frac{n-m}{2}-1$'], 1, [
        'Plug in $m=3$ and $n=10$. The odd numbers between them are $5$, $7$ and $9$: three numbers.',
        'Put $m=3$, $n=10$ into the choices: (1) $\\frac{10-3-1}{2}=3$ ✓, (2) $\\frac72$ ✗, (3) $\\frac82+1=5$ ✗, (4) $\\frac72-1=\\frac52$ ✗.',
        'With the counting rule: the first odd number is $m+2$ and the last is $n-1$. Their count is $\\frac{(n-1)-(m+2)}{2}+1=\\frac{n-m-1}{2}$.'])
    # q-587: three different integers, sum 25; necessarily: b is not the average of a and c  ==>  sum 32, c != 7; reordered
    _rn_q(M, 'q-587', 'Given: $a$, $b$ and $c$ are three different integers, and $a+b+c=32$. Which of the following is necessarily true?',
          ['$c\\ne7$', 'The sum of any two of the numbers is greater than the third.',
           '$b$ is not equal to the average of $a$ and $c$.', 'The smallest of the three numbers is odd.'], 3, [
        'Break the wrong choices with examples. For (1), $(a,b,c)=(3,22,7)$ has $c=7$ ✗. For (2), $(1,2,29)$ has $1+2<29$ ✗. For (4), $(2,3,27)$ has smallest number $2$, even ✗.',
        'Why (3) is always true: if $b$ were the average of $a$ and $c$, then $a+c=2b$ and $a+b+c=3b=32$. But $32$ is not divisible by $3$.'])
    # q-588: a<x<3a, how many x: 2a-1  ==>  n<k<4n: 3n-1
    _rn_q(M, 'q-588', 'Given: $n$ and $k$ are positive integers, and $n<k<4n$. For a fixed value of $n$, how many different values can $k$ take?',
          ['$3n$', '$3n-1$', '$n-1$', '$3n+1$'], 2, [
        'Plug in $n=2$: $2<k<8$. The values of $k$ are $3$, $4$, $5$, $6$ and $7$: five values.',
        'Only $3n-1$ gives $5$. The others give $3n=6$, $n-1=1$ and $3n+1=7$.',
        'With the counting rule: strictly between $n$ and $4n$ there are $4n-n-1=3n-1$ integers.'])
    # q-589: y = a^a, a x 3 -> 3^(3a) a^(2a)  ==>  y = b^b, b x 4 -> 4^(4b) b^(3b)
    _rn_q(M, 'q-589', 'Given: $b$ is a positive number, and $y=b^b$. If $b$ is multiplied by $4$, by what factor is $y$ multiplied?',
          ['$4^{4b}\\cdot b^{3b}$', '$b^b$', '$4^b\\cdot b^b$', '$b^4$'], 1, [
        'The new value is $(4b)^{4b}=4^{4b}\\cdot b^{4b}$.',
        'Divide by the old value: $\\frac{4^{4b}\\cdot b^{4b}}{b^b}=4^{4b}\\cdot b^{3b}$.',
        'Check with $b=1$: $y=1$ becomes $4^4=256$. Only (1) gives $256$: $4^4\\cdot1^3=256$. The others give $1$, $4$ and $1$.'])
    # q-590: 13 numbers, begin with 5 and end with 2  ==>  12 numbers, begin with 7 and end with 4; reordered
    _rn_q(M, 'q-590', 'On a board there are $12$ different positive integers. Each of them begins with the digit $7$ and ends with the digit $4$. Which of the following cannot be true?',
          ['All the numbers have at least $5$ digits.', 'All the numbers are divisible by $9$.',
           'All the numbers have at most $3$ digits.', 'All the numbers use only the digits $7$ and $4$.'], 3, [
        'Count the numbers with at most $3$ digits that begin with $7$ and end with $4$: $74$, and $704, 714, \\ldots, 794$ (ten numbers). That is only $11$ numbers.',
        'You cannot choose $12$ different numbers from $11$. Therefore (3) cannot be true.',
        'The others can happen, because there are endless numbers of each kind. For example: (1) $70004, 70014, 70024, \\ldots$; (2) $774=9\\cdot86$, and $7074$ and $7164$ also have digit sum $18$; (4) $74, 744, 774, 7444, \\ldots$'])


def rn_practice(M):
    """Approved clean-up: copies out, at most 3 extra-bank warm-ups, September items whose type the Hebrew covers out."""
    X = 'alg-extra-unit-t20-2-'; N = lambda k: 'q-r26-t20-' + k
    out = [
        # copies (practice_audit/copies_by_topic.txt, each checked)
        N('05'),          # 0 < x < 1, which is the smallest: the same question as Topic 8's q-r26-t08-02 (and guided Q2)
        N('09'),          # the same drawer (5 red, 7 blue, 9 green) as guided Q8
        X + '6',          # a^2 = b^2 -> |a| = |b|: taught and practised with the roots / absolute value
        # extra-bank warm-ups beyond 3 (kept: X5 cannot be n^2, X1 largest of three with a fixed sum, X4 not necessarily)
        X + '3', X + '2', X + '7',
        # September items of a type the Hebrew practice covers
        N('06'),          # x < y < 0, must be true: the regions plug-in of N12 and guided Q1 / Q2
        N('07'),          # count integers with 10 < x^2 < 100: counting, as q-586 / q-588 and guided Q7
        N('08'),          # count even numbers from 2n to 8n (letters): q-586, q-588
        N('10'),          # scaling x^3 = y^2: q-589 and guided Q5
    ]
    for qid in out:
        assert M.section_of(qid) == PRAC, qid
        M.unplace(qid)
    M.practice_order(PRAC, [
        X + '5', X + '1', X + '4', 'q-581', 'q-582', 'q-584', 'q-588', 'q-586', N('11'), 'q-587', N('12'), 'q-585',
        'q-583', 'q-589', 'q-590'])


def renumber_pass(M):
    rn_guided(M)
    rn_order(M)
    rn_cards(M)
    rn_practice_questions(M)
    rn_practice(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-06 Hebrew back-check: compared with the teacher's Hebrew VIDEO subtitles (01-Algebra-Original-Subtitles.txt,
# lines 19912-20234). The summary's scaling example (x² = a³, a × 4 → x × 8) and the card tip (4^(3/2) = 8) were
# exactly the Hebrew sample question's numbers  ==>  a × 9 → x × 27. Nothing in topic 20 is recorded. Runs LAST.
# ======================================================================================================
def _hb_sub(M, vid, n, pairs):
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


def hebrew_backcheck(M):
    _hb_sub(M, 'r26-t20-summary', 7, [
        ('$x^2=a^3:\\quad a\\times4\\ \\to\\ x\\times4^{\\frac32}=x\\times8$', '$x^2=a^3:\\quad a\\times9\\ \\to\\ x\\times9^{\\frac32}=x\\times27$'),
        ('x² = a³, a × 4 → x × 8', 'x² = a³, a × 9 → x × 27'),
        ('Four cubed is sixty-four. Its root: eight.', 'Nine cubed is three to the sixth. Its root: three cubed — twenty-seven.')])
    c = M.card('mem-understanding')
    i = [k for k, t in enumerate(c['tips']) if t.startswith('Scaling:')]
    assert len(i) == 1
    c['tips'][i[0]] = 'Scaling: $x^2=a^3$, so $x$ changes by $(\\text{factor})^{\\frac32}$. For example, $9^{\\frac32}=27$.'


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
    # r26-t20-counting "From a to b": counting the integers from a to b (b − a + 1) was taught in topic 16 (Sums of
    # Consecutive Integers, Counting integers). The slide becomes one reminder line on "Strictly between".
    G = 'r26-t20-counting'
    if not R.recorded(G):
        R.drop_slide(M, G, 'From a to b')
        s = R.lines_of(M, G, 'Strictly between')
        R.set_slide(M, G, 'Strictly between', [
            A("'From a to b, both included: b − a + 1' appears", T(r'From $a$ to $b$, both included: $\ b-a+1$')),
            'From a to b, both ends in: b minus a, plus one — you know it.'] + s)


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
    _mn_load().method_names(M, 20)   # 2026-10-07 method names: runs last


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
    # Hebrew 20138-20148: whole numbers that fit r² = p² + q² are Pythagorean triples; the smallest is 3-4-5
    if not CF.add_lines(M, 'solve-q-579', 'Test each choice', 'as Pythagoras', [
            'Whole numbers that fit it are called Pythagorean triples. The smallest is three, four, five — so here r is at least five.']):
        pass
    CF.add_expl(M, 'q-579', 'Whole numbers that fit $r^2=p^2+q^2$ are called Pythagorean triples; the smallest is $3, 4, 5$, so $r\\ge5$.')


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST


# =====================================================================================================================
# 2026-10-09 spoken labels -> speech (teacher: "take off words like 'notice:' that seem like I'm reading"): spoken
# lines that open with "Careful:", "Notice:", "Step one:", "The trap:"... are rewritten by hand in her spoken style, in
# place (same line count, cues unchanged). Data and rules: _spoken_labels.py (a video recorded before its CUTOFF keeps
# its old lines). Runs LAST.
# =====================================================================================================================
def _sl_load():
    import importlib.util, os, sys
    if '_spoken_labels' in sys.modules: return sys.modules['_spoken_labels']   # one copy: its WARN / CHANGED add up
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_spoken_labels.py')
    spec = importlib.util.spec_from_file_location('_spoken_labels', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); sys.modules['_spoken_labels'] = m
    return m


_apply_before_spoken_labels = apply


def apply(M):
    _apply_before_spoken_labels(M)
    _sl_load().spoken_labels(M, 20)   # 2026-10-09 spoken labels: runs LAST


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
    _co_load().choice_order(M, 20)   # 2026-10-09 choice order: runs LAST
