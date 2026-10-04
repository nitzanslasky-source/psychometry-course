"""Topic 17 - The Number Line. Course review 2026-09 fixes.
See t17_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q
from math_api import VIS

TOPIC = 17
L1 = 'number-line'
L2 = 'powers-on-number-line'
READ = 'r26-t17-reading-the-line'
CARD = 'mem-number-line'
CARD2 = 'mem-r26-t17-reading'
ADV_SIDEBAR = ['Question %d' % n for n in range(3, 15)]


# =========================================================================================
# Number-line figures (same style as the course's coordinate-plane figures)
# =========================================================================================
_AX = '#71818d'; _INK = '#203344'; _PT = '#087f83'; _FONT = 'DejaVu Sans,Arial,sans-serif'


def _txt(x, y, s, size=18, italic=False, weight=None):
    st = ' font-style="italic"' if italic else ''
    wt = ' font-weight="%s"' % weight if weight else ''
    return ('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" fill="%s" '
            'font-family="%s" font-size="%d"%s%s>%s</text>' % (x, y, _INK, _FONT, size, st, wt, s))


def nl_svg(title, marks, points, lo, hi):
    """marks: numbers drawn as ticks with the number below; points: (value, label) drawn as dots with the label above.
    Lowercase one-letter labels are variables (italic); capital letters are point names."""
    W, H_, y = 640, 160, 88
    X = lambda v: 60 + (v - lo) / float(hi - lo) * 520
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s"><title>%s</title>' % (W, H_, title, title)]
    s.append('<line x1="24" y1="%d" x2="616" y2="%d" stroke="%s" stroke-width="1.8"/>' % (y, y, _AX))
    s.append('<path d="M609 %d L616 %d L609 %d" fill="none" stroke="%s" stroke-width="1.8"/>' % (y - 4, y, y + 4, _AX))
    s.append('<path d="M31 %d L24 %d L31 %d" fill="none" stroke="%s" stroke-width="1.8"/>' % (y - 4, y, y + 4, _AX))
    for v in marks:
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.8"/>' % (X(v), y - 9, X(v), y + 9, _AX))
        lab = ('−%g' % -v) if v < 0 else '%g' % v
        s.append(_txt(X(v), y + 30, lab, 18))
    for v, lab in points:
        s.append('<circle cx="%.1f" cy="%d" r="5" fill="%s"/>' % (X(v), y, _PT))
        s.append(_txt(X(v), y - 28, lab, 21, italic=(len(lab) == 1 and lab.islower())))
    s.append('</svg>')
    return ''.join(s)


FIG_Q10 = nl_svg('Number line with a, b, c and d', [-1, 0, 1], [(-1.75, 'a'), (-0.45, 'b'), (0.4, 'c'), (1.7, 'd')], -2.2, 2.2)
FIG_Q11 = nl_svg('Number line with x and the points K, L, M and N', [0, 1],
                 [(-0.5, 'K'), (0.22, 'L'), (0.5, 'x'), (0.76, 'M'), (1.55, 'N')], -0.9, 1.9)
FIG_P1 = nl_svg('Number line with a and b', [-1, 0, 1], [(-0.55, 'a'), (1.6, 'b')], -1.6, 2.1)
FIG_P2 = nl_svg('Number line with x and y', [0], [(-1.7, 'x'), (-0.6, 'y')], -2.3, 0.9)
FIG_P3 = nl_svg('Number line with x and the points A, B, C and D', [-1, 0, 1],
                [(-1.55, 'A'), (-0.8, 'B'), (-0.5, 'x'), (-0.18, 'C'), (0.35, 'D')], -2.0, 1.4)
FIG_DEMO = nl_svg('Number line with a, b and c', [-1, 0, 1], [(-1.6, 'a'), (0.35, 'b'), (1.55, 'c')], -2.1, 2.1)


# =========================================================================================
# helpers
# =========================================================================================
def _solution(M, qid, intro, slides):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=n - 3, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Advanced Number Line', ADV_SIDEBAR, beats, M.section_of(qid),
                    kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Advanced Number Line'
    v['hybrid']['num'] = M.video('solve-q-495')['hybrid']['num']
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _replace_say(M, vid, n, old, new_lines):
    """Replace the spoken line containing `old` by one or more lines (str = say, ('D', x) = draw)."""
    def fn(lines):
        out = []
        hit = False
        for l in lines:
            if 'say' in l and old in l['say']:
                hit = True
                for x in new_lines:
                    out.append({'say': x} if isinstance(x, str) else {'draw': x[1]})
            else:
                out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Lesson 1 "The Number Line": true rules, one message on negative exponents
    # =====================================================================================
    # slide 4: no ":" for division; point ahead to negative multipliers
    M.set_slide(L1, 4, script=[
        "How do multiplying and dividing move a positive number?",
        A("'× more than 1' appears: 8 · 3 = 24", T('$\\times$ more than 1:  $8\\cdot3=24$', size=46)),
        D('Write "↑ bigger" next to it'),
        "Multiply by something bigger than one — you grow. Eight times three is twenty-four.",
        A("'÷ more than 1' appears: 12 ÷ 3 = 4", T('$\\div$ more than 1:  $12\\div3=4$', size=46)),
        D('Write "↓ smaller" next to it'),
        "Divide by something bigger than one — you shrink. Twelve divided by three is four.",
        A("'× a fraction' appears: 12 · ⅓ = 4", T('$\\times$ a fraction:  $12\\cdot\\frac13=4$', size=46)),
        D('Write "↓ smaller" next to it'),
        "Multiply by a fraction — you shrink too. You're only taking a third.",
        A("'÷ a fraction' appears: 12 ÷ ⅓ = 36", T('$\\div$ a fraction:  $12\\div\\frac13=12\\cdot3=36$', size=46)),
        D('Write "↑ bigger" next to it'),
        "Divide by a fraction — it flips: dividing by a third is multiplying by three. Thirty-six.",
        "One is the dividing line. And a negative number times a positive one? The same moves — mirrored: away from zero, or toward zero.",
        "Multiplying by a NEGATIVE number is different: it jumps to the other side of zero. You'll see it before the advanced questions.",
    ])

    # slide 5: hierarchy holds for positive powers and roots (odd ones for negatives)
    M.set_slide(L1, 5, script=[
        "Now: hierarchy.",
        "A number that lives in a range further right stays bigger — after any positive power or root.",
        A("'Positive powers and roots · negatives: odd ones only' appears",
          T('Positive powers and roots · for negatives: odd ones only', size=40, gap=50)),
        "One condition: for negative numbers, only odd powers and odd roots. An even power makes a negative number positive.",
        "And watch for the exceptional powers — we'll see them in a moment.",
        A('The fifth root of 9/8 and the square root of 5/6 appear', T('$\\sqrt[5]{\\frac98}\\quad ? \\quad \\sqrt{\\frac56}$', size=64, gap=60)),
        "Which is bigger? Calculating those roots is a nightmare. Don't.",
        D('Under 9/8 write "> 1"; under 5/6 write "fraction"'),
        "Nine eighths isn't really a fraction — the top beats the bottom, so it's more than one. Five sixths is a real fraction, less than one.",
        "A root of a number above one stays above one. A root of a positive fraction stays a positive fraction.",
        D('Write ">" between them'),
        "So the fifth root of nine eighths lives in the bigger family — it's bigger. Ignore the roots; look at the number itself.",
    ])

    # slide 6: negative exponent - say when to flip
    M.edit_lines(L1, 6, lambda ls: ls + [
        {'say': "Here we compare by RANGES — so flip first, and see which range the number lands in."},
        {'say': "In the next lesson you'll meet the arrows. With the arrows you may keep the minus. Both ways give the same answer."},
    ])

    # slide 7: "same operation - ignore it" only for positive numbers
    M.set_slide(L1, 7, script=[
        "When two positive numbers get exactly the same operation — just ignore the operation.",
        "Whoever was bigger without it is bigger with it — once any exceptional power is handled.",
        A('7⁻³ and 6⁻³ appear', T('$7^{-3}\\quad ? \\quad 6^{-3}$', size=62, gap=60)),
        "Exceptional power here — a minus in the exponent. Handle it first: flip.",
        D('Write "= (1/7)³" and "= (1/6)³" under them'),
        "One seventh cubed against one sixth cubed. Now both have the same power — ignore it.",
        D('Write "<" between the original two'),
        "Who's bigger: one sixth or one seventh? One sixth. So six to the minus three is bigger. No calculating.",
        A("'−3 < −2, but (−3)² > (−2)²' appears", T('$-3<-2\\quad$ but $\\quad(-3)^2>(-2)^2$', size=54)),
        "But careful — this works for positive numbers only. Minus three is smaller than minus two.",
        "Squared: nine against four. The order flipped. With negatives, don't ignore the power — use the arrows from the next lesson.",
    ])

    # slide 9: recap with the conditions
    M.set_slide(L1, 9, script=[
        "Let's lock it in.",
        A("'Four ranges: < −1 · −1 to 0 · 0 to 1 · > 1' appears", T('Four ranges: $x<-1$ · $-1<x<0$ · $0<x<1$ · $x>1$', size=40)),
        A("'Negatives mirror the positives' appears", T('Negatives mirror the positives', size=42)),
        A("'Higher range → bigger (positive powers and roots)' appears", T('Higher range $\\to$ bigger (positive powers and roots)', size=40)),
        A("'Exceptional powers first' appears", T('Exceptional powers first: even power of a negative · negative exponent (flip it)', size=38)),
        A("'Same operation? Ignore it (positive numbers) · Strong on strong' appears",
          T('Same operation? Ignore it (positive numbers only) · Strong on strong', size=38)),
        D('Circle "Exceptional powers first"'),
        "This understanding — how numbers grow, shrink and jump ranges — is what makes these questions fast.",
        "Next: a question, and then the number-line method for powers.",
    ])

    # =====================================================================================
    # 2. Lesson 2 "Powers on the Number Line": define "odd", same negative-exponent message
    # =====================================================================================
    _replace_say(M, L2, 2, 'Negative fractions: right.', ["Negative fractions: right — for odd powers."])

    M.set_slide(L2, 5, script=[
        A('−1 < x < 0 → x < x³ < x⁵ < 0 appears', T('$-1<x<0\\ \\Rightarrow\\ x<x^3<x^5<0$', size=54, gap=50)),
        "Negative fractions: the arrow points right. Bigger odd power — further right — bigger.",
        A('(−1/2)³ = −1/8 appears', T('$\\left(-\\frac12\\right)^3=-\\frac18$', size=56, gap=50)),
        D('Mark −1/2 and −1/8 on an imagined line and draw a right arrow'),
        "Negative one half cubed is negative one eighth. That's to the RIGHT of negative one half.",
        "Even powers are different — they turn positive. And every positive beats every negative.",
        A("'Odd: 3, 5, −1, −3, 1/3, 1/5' appears", T('Odd: $3,\\ 5,\\ {-1},\\ {-3},\\ \\frac13,\\ \\frac15$', size=48)),
        "What counts as odd? Any power that keeps the minus sign of a negative base.",
        "Odd powers: three, five. Their negatives: minus one, minus three. And odd roots: a cube root is a power of one third, a fifth root a power of one fifth.",
        "For a negative base, the arrows work for all of these. A square root of a negative number doesn't exist — so it never shows up here.",
    ])

    _replace_say(M, L2, 7, 'And a negative exponent?', [
        "And a negative exponent? With the arrows, keep it — minus one is just a small power on the line of powers.",
        "Without the arrows — comparing ranges, or the same operation — flip it first, as in the first lesson. Both ways give the same answer.",
    ])

    M.set_slide(L2, 9, script=[
        "Let's lock it in.",
        A('A number line from −2 to 2 appears', {'k': 'nl', 'min': -2, 'max': 2, 'y': 110}),
        A('The four arrows appear: ← → ← →', {'k': 'row', 'items': ['$\\leftarrow$', '$\\rightarrow$', '$\\leftarrow$', '$\\rightarrow$'],
                                               'size': 62, 'sp': 252, 'below': 0, 'x': 548, 'y': 250}),
        A("'Right = bigger · Left = smaller' appears", T('Arrow right = bigger power, bigger number · Arrow left = smaller', size=40, x=410, y=380)),
        A("'Exceptions → roots to powers → arrows' appears", T('Exceptions $\\to$ roots to powers $\\to$ arrows', size=40, x=410, y=450)),
        A("'Negative side: odd powers only · negative exponents: keep them' appears",
          T('Negative side: odd powers only · negative exponent: keep it', size=40, x=410, y=520)),
        D('Circle the arrow for negative fractions'),
        "Plugging in numbers always works — but it takes time. Understanding what each range does can solve these in seconds.",
        "Next: a question to try it on.",
    ])

    # =====================================================================================
    # 3. Existing solution videos
    # =====================================================================================
    # Q8: the "replace every ten with a two" trick changes the order - replace with a valid plug-in
    M.set_slide('solve-q-500', 3, script=[
        "Plug in? A half to the tenth power, the tenth root of a half… no calculator.",
        "So choose x with a clean tenth root.",
        D('Write "x = 1/1024 = (½)¹⁰"'),
        "Two to the tenth is one thousand twenty-four. So one over one thousand twenty-four is one half, to the tenth.",
        D('Next to the choices write "tiny, ½, 10/1024, 10240"'),
        "x to the tenth: tiny. The tenth root: one half. Ten x: ten over a thousand twenty-four — less than one. Ten over x: ten thousand two hundred forty.",
        D('Circle choice 4'),
        "By far the biggest. Choice four.",
        "One warning: change only x. Don't change the numbers in the question to make it easier — that can change the order of the choices.",
    ])
    for vid in ['solve-q-495', 'solve-q-496', 'solve-q-497', 'solve-q-498', 'solve-q-499', 'solve-q-500', 'solve-q-501']:
        M.set_sidebar(vid, ADV_SIDEBAR)

    # =====================================================================================
    # 4. Memory card: same messages, no ":" for division
    # =====================================================================================
    c = M.card(CARD)
    c['tables'][1] = {'title': 'Multiplying and dividing', 'head': ['By…', 'Multiply', 'Divide'], 'rows': [
        ['a number above 1', 'bigger: \\(8\\cdot3=24\\)', 'smaller: \\(12\\div3=4\\)'],
        ['a fraction (0 to 1)', 'smaller: \\(12\\cdot\\frac13=4\\)', 'bigger: \\(12\\div\\frac13=36\\)'],
        ['a negative number', 'other side of zero, the order flips: \\(2<5\\Rightarrow-2>-5\\)', 'the same: \\(12\\div(-3)=-4\\)']]}
    c['tables'][0]['rows'][2][1] = '\\(\\rightarrow\\) bigger (odd powers)'
    c['tips'] = [
        'Exceptions first: an even power of a negative number turns positive.',
        'Negative exponent: with the arrows, keep it (\\(-1\\) is just a small power). Comparing ranges or the same operation, flip it first: \\(\\left(\\frac25\\right)^{-2}=\\left(\\frac52\\right)^2>1\\).',
        'Negative base: the arrows work for odd powers and odd roots: \\(3,\\ 5,\\ -1,\\ -3,\\ \\frac13,\\ \\frac15\\).',
        'Higher range \\(\\to\\) bigger, after any positive power or root (for negatives: odd ones only).',
        'Negatives mirror the positives: \\(-12\\cdot\\frac13=-4\\) moves toward zero, so it gets bigger.',
        'Same operation on both? Ignore it — positive numbers only: \\(-3<-2\\) but \\((-3)^2>(-2)^2\\).',
        'Strong on strong, weak on weak (positive numbers).',
    ]

    # =====================================================================================
    # 5. Existing guided questions: TeX, nice numbers, correct reasons
    # =====================================================================================
    S('q-493', stem='Given: $1<a<b<c<d$. Which of the following statements is not correct?',
      choices=['$a\\cdot b<c\\cdot d$', '$a\\cdot c<b\\cdot d$', '$b<c\\cdot a$', '$a\\cdot d<c$'], expl=[
          'All four numbers are greater than 1.',
          '(1) $a<c$ and $b<d$, so $a\\cdot b<c\\cdot d$ (weak times weak is less than strong times strong). True.',
          '(2) $a<b$ and $c<d$, so $a\\cdot c<b\\cdot d$. True.',
          '(3) $c>b$, and multiplying $c$ by $a>1$ makes it even bigger: $c\\cdot a>c>b$. True.',
          '(4) $a>1$, so $a\\cdot d>d>c$. The statement $a\\cdot d<c$ is never true. This is the answer.'])
    S('q-494', stem='Given: $-1<t<0$. Which of the following expressions is the smallest?', expl=[
        'Step 1, exceptions: $t^6$ is an even power of a negative number, so it is positive. The other three are negative, so $t^6$ is not the smallest.',
        'Step 2, roots to powers: $\\sqrt[3]{t}=t^{\\frac13}$.',
        'Step 3, the arrows: for $-1<t<0$ and odd powers (5, $\\frac13$, $-1$), the arrow points right, so the smallest power gives the smallest number. The smallest power is $-1$: $t^{-1}$ is the smallest.',
        'Check with $t=-\\frac18$: $t^5$ is a tiny negative number, $\\sqrt[3]{t}=-\\frac12$ and $t^{-1}=-8$. The smallest is $-8$.'])
    S('q-495', stem='Given: $1<a<b<c$. Which of the following expressions is the smallest?',
      choices=['$b\\cdot c^2$', '$a\\cdot b^2$', '$b\\cdot a^2$', '$b^3$'], expl=[
          'Plug in $a=2$, $b=3$, $c=4$: $b\\cdot c^2=3\\cdot16=48$, $a\\cdot b^2=2\\cdot9=18$, $b\\cdot a^2=3\\cdot4=12$, $b^3=27$. The smallest is $b\\cdot a^2$.',
          'Why: $b\\cdot a^2=a\\cdot b\\cdot a$ and $a\\cdot b^2=a\\cdot b\\cdot b$. Both contain $a\\cdot b$; the third factor is $a$ against $b$, and $a<b$. So $b\\cdot a^2$ is smaller.',
          'The other two are even bigger: $b^3=b\\cdot b\\cdot b$ and $b\\cdot c^2$ use only larger factors.'])
    S('q-496', stem='Given: $0<p<q<1<r<s$. Which of the following statements is not necessarily true?',
      choices=['$q\\cdot s<s$', '$r-q<s-p$', '$r<\\frac rp$', '$r+q<s+p$'], expl=[
          '(1) $s>0$ and $q$ is a positive fraction. Multiplying by a positive fraction makes $s$ smaller: $q\\cdot s<s$. Always true.',
          '(2) $r<s$, and $p<q$ means $-q<-p$. Add the two inequalities: $r-q<s-p$. Always true.',
          '(3) Dividing $r>0$ by a positive fraction makes it bigger: $\\frac rp>r$. Always true.',
          '(4) Push the values to the edges: $p=0.1$, $q=0.9$, $r=1.1$, $s=1.2$. Then $r+q=2$ and $s+p=1.3$, so $r+q>s+p$. Not necessarily true.'])
    S('q-497', stem='Given: $-1<a<0<b<c<1$. Which of the following expressions is the largest?',
      choices=['$a\\cdot b\\cdot c$', '$a\\cdot c$', '$a\\cdot b$', '$a$'], expl=[
          'All four are negative ($a<0$; $b$ and $c$ are positive). On the negative side, the largest number is the one closest to zero.',
          'Multiplying by a positive fraction pulls a number toward zero. $a\\cdot b\\cdot c$ is $a$ multiplied by two fractions, so it is the closest to zero.',
          'Check with $a=-\\frac12$, $b=\\frac14$, $c=\\frac12$: $a\\cdot b\\cdot c=-\\frac1{16}$, $a\\cdot c=-\\frac14$, $a\\cdot b=-\\frac18$, $a=-\\frac12$. The largest is $-\\frac1{16}$.'])
    S('q-498', stem='Given: $x^6<x^5$. In which of the following ranges is $x$?',
      choices=['$x>1$', '$0<x<1$', '$-1<x<0$', '$x<-1$'], expl=[
          'If $x<0$, then $x^6>0$ and $x^5<0$, so $x^6<x^5$ is impossible. Therefore $x>0$.',
          'For $x>1$, a bigger power gives a bigger number: $x^6>x^5$. ✗',
          'For $0<x<1$, a bigger power gives a smaller number: $x^6<x^5$. ✓',
          'Check: $x=\\frac12$: $\\frac1{64}<\\frac1{32}$ ✓. $x=2$: $64>32$ ✗.'])
    S('q-499', stem='Given: $-1<x<0$. Which of the following orders of $x^5$, $x$, $\\sqrt[5]{x}$ and $x^{-5}$ is correct?',
      choices=['$x^{-5}<\\sqrt[5]{x}<x<x^5$', '$x<\\sqrt[5]{x}<x^5<x^{-5}$', '$\\sqrt[5]{x}<x^{-5}<x<x^5$', '$x^5<x^{-5}<\\sqrt[5]{x}<x$'], expl=[
          'For $-1<x<0$ and odd powers or odd roots, the arrow points right: a bigger power gives a bigger number.',
          'The powers: $x^{-5}$ (power $-5$), $\\sqrt[5]{x}=x^{\\frac15}$, $x=x^1$, $x^5$. Since $-5<\\frac15<1<5$, the order is $x^{-5}<\\sqrt[5]{x}<x<x^5$.',
          'Check with a number that has a clean fifth root, $x=-\\frac1{32}$: $\\sqrt[5]{x}=-\\frac12$, $x^{-5}=(-32)^5$ (a huge negative number), and $x^5$ is a tiny negative number. So $(-32)^5<-\\frac12<-\\frac1{32}<x^5$.'])
    S('q-500', stem='Given: $0<x<1$. Which of the following expressions is the largest?',
      choices=['$x^{10}$', '$\\sqrt[10]{x}$', '$10x$', '$\\frac{10}{x}$'], expl=[
          'Place each choice: $x^{10}$ is between $0$ and $x$. $\\sqrt[10]{x}$ is between $x$ and $1$. $10x<10$ (multiplying 10 by a fraction makes it smaller). $\\frac{10}x>10$ (dividing by a fraction makes it bigger).',
          'Only $\\frac{10}x$ is greater than 10, so it is the largest.',
          'Check with a number that has a clean tenth root, $x=\\frac1{1024}=\\left(\\frac12\\right)^{10}$: $\\sqrt[10]{x}=\\frac12$, $10x=\\frac{10}{1024}<1$, $\\frac{10}x=10240$.'])
    S('q-501', stem='Given: $a^2<a<c\\cdot b<b<c$. Which of the following statements is possible but not necessarily true?',
      choices=['$a\\cdot b<a+b$', '$a^2\\cdot b<a\\cdot c$', '$a+c<1$', '$a\\cdot b>1$'], expl=[
          'Decode the chain. $a^2<a$ happens only for $0<a<1$. So $a>0$, and every letter after it is positive.',
          '$c\\cdot b<b$: divide by $b>0$: $c<1$. So $0<a<b<c<1$.',
          '(1) $a\\cdot b<a<a+b$. Always true. (2) Divide by $a>0$: $a\\cdot b<c$. True, since $a\\cdot b<b<c$. (4) A product of two positive fractions is less than 1. Never true.',
          '(3) $a=0.1$, $b=0.3$, $c=0.5$ (then $c\\cdot b=0.15$, the chain holds): $a+c=0.6<1$ ✓. But $a=0.3$, $b=0.5$, $c=0.9$ (then $c\\cdot b=0.45$): $a+c=1.2>1$ ✗. Possible, but not necessarily true.'])

    # =====================================================================================
    # 6. Practice questions: TeX, nice numbers, one idea per line
    # =====================================================================================
    S('q-502', stem='Given: $0<x<y<1$. Which of the following is necessarily greater than 1?',
      choices=['$\\frac yx$', '$x\\cdot y$', '$x^y$', '$x+y$'], expl=[
          '$\\frac yx$ is a bigger positive number over a smaller one, so $\\frac yx>1$. Always.',
          'The others: $x\\cdot y<1$ (two positive fractions), $x^y<1$ (a positive fraction to a positive power), and $x+y$ can be less than 1: $x=\\frac14$, $y=\\frac12$ gives $\\frac34$.'])
    S('q-503', stem='Which of the following numbers is the largest?',
      choices=['$\\left(\\frac13\\right)^2$', '$\\left(\\frac13\\right)^{\\frac12}$', '$\\left(\\frac13\\right)^{-\\frac12}$', '$\\left(\\frac13\\right)^{-2}$'], expl=[
          'With the arrows: the base $\\frac13$ is between 0 and 1, so the smallest power gives the largest number. The smallest power is $-2$.',
          'Check by flipping: $\\left(\\frac13\\right)^{-2}=3^2=9$ and $\\left(\\frac13\\right)^{-\\frac12}=\\sqrt3<2$. The other two are less than 1: $\\left(\\frac13\\right)^2=\\frac19$ and $\\left(\\frac13\\right)^{\\frac12}=\\frac1{\\sqrt3}$.'])
    S('q-504', stem='Given: $b<a$. Which of the following changes necessarily increases $a-b$, the distance between $a$ and $b$ on the number line?',
      choices=['Subtract 2 from $a$ and subtract 2 from $b$.', 'Subtract 2 from $a$ and add 2 to $b$.',
               'Add 2 to $a$ and subtract 2 from $b$.', 'Add 2 to $a$ and add 2 to $b$.'], expl=[
          '$b<a$, so $a-b$ is the distance between them. To make it bigger, move $a$ to the right and $b$ to the left.',
          '(3): $(a+2)-(b-2)=a-b+4$. The distance grows by 4.',
          '(1) and (4) move both numbers the same way: $(a-2)-(b-2)=a-b$, no change. (2): $(a-2)-(b+2)=a-b-4$, smaller.'])
    S('q-506', stem='Given: $0<|b|<1$ and $w=b^4$. Which of the following is necessarily true?',
      choices=['$0<w<|b|$', '$|b|<w<1$', '$1<w<\\frac1{|b|}$', '$\\frac1{|b|}<w$'], expl=[
          '$w=b^4=|b|^4$, an even power, so $w>0$.',
          '$|b|$ is a positive fraction, and a bigger power makes a positive fraction smaller: $|b|^4<|b|$. So $0<w<|b|$.',
          'Check with $b=-\\frac12$: $w=\\frac1{16}$, and $0<\\frac1{16}<\\frac12$ ✓.'])
    S('q-507', stem='Given: $0<a<b<\\frac13$. Which of the following expressions is the largest?',
      choices=['$a^2+b^2$', '$3b$', '$a+b$', '$\\frac ba$'], expl=[
          'The first three are less than 1: $a^2+b^2<\\frac19+\\frac19=\\frac29$, $3b<3\\cdot\\frac13=1$, $a+b<\\frac13+\\frac13=\\frac23$.',
          '$\\frac ba$ is a bigger positive number over a smaller one, so $\\frac ba>1$. It is the largest.',
          'Check: $a=\\frac1{10}$, $b=\\frac15$: $\\frac ba=2$, while $3b=\\frac35$, $a+b=\\frac3{10}$ and $a^2+b^2=\\frac1{20}$.'])
    S('q-508', stem='Given: $-1<y<0$. Which of the following expressions is the largest?',
      choices=['$\\frac1y$', '$y^5$', '$5y$', '$y$'], expl=[
          'All four are negative, so the largest is the one closest to zero.',
          'For $-1<y<0$ and odd powers, the arrow points right: $y^5$ (power 5) $>y$ (power 1) $>\\frac1y$ (power $-1$).',
          '$5y$: multiplying by 5 moves $y$ away from zero, so $5y<y$.',
          'Check with $y=-\\frac12$: $\\frac1y=-2$, $y^5=-\\frac1{32}$, $5y=-\\frac52$, $y=-\\frac12$. The largest is $-\\frac1{32}$.'])
    S('q-509', stem='Given: $x^5<x<x^4$. In which of the following ranges must $x$ be?',
      choices=['$x>1$', '$0<x<1$', '$-1<x<0$', '$x<-1$'], expl=[
          'Test one number from each range: $2$, $\\frac12$, $-\\frac12$, $-2$.',
          '$x=2$: $x^5=32>2$ ✗. $x=\\frac12$: $x^4=\\frac1{16}<\\frac12$, so $x<x^4$ fails ✗. $x=-\\frac12$: $x^5=-\\frac1{32}>-\\frac12$, so $x^5<x$ fails ✗.',
          '$x=-2$: $x^5=-32$, $x=-2$, $x^4=16$, and $-32<-2<16$ ✓. So $x<-1$.'])
    S('q-510', stem='Given: $3a<x<a$. Which of the following expressions is the largest?',
      choices=['$a^2$', '$x^2$', '$(x-a)^3$', '$a^3$'], expl=[
          '$3a<a$: subtract $a$ from both sides: $2a<0$, so $a<0$.',
          '$x$ is between $3a$ and $a$, so $x<0$ and $x$ is further from zero than $a$. Therefore $x^2>a^2$.',
          '$x-a<0$, so $(x-a)^3<0$. Also $a^3<0$. Negative numbers are less than any square.',
          'Check: $a=-1$, $x=-2$ ($-3<-2<-1$): $a^2=1$, $x^2=4$, $(x-a)^3=-1$, $a^3=-1$. The largest is $x^2$.'])
    S('q-511', stem='Given: $-1<P<0<Q<1$. Which of the following is the smallest?',
      choices=['$0$', '$P\\cdot Q$', '$P^2\\cdot Q^2$', '$P^3\\cdot Q^3$'], expl=[
          '$P^2\\cdot Q^2>0$, so it is not the smallest. $P\\cdot Q<0$ and $P^3\\cdot Q^3=(P\\cdot Q)^3<0$.',
          '$P\\cdot Q$ is a negative fraction. For a negative fraction the arrow points right: the cube is bigger. So $P\\cdot Q<(P\\cdot Q)^3<0$.',
          'Check: $P=-\\frac12$, $Q=\\frac12$: $P\\cdot Q=-\\frac14$, $P^3\\cdot Q^3=-\\frac1{64}$, $P^2\\cdot Q^2=\\frac1{16}$. The smallest is $-\\frac14$.'])

    S('alg-extra-unit-t17-3-2', stem='Given: $0<x<1$. Which of the following orders is correct?', expl=[
        'For $0<x<1$, a bigger power gives a smaller number: $x^2$ (power 2) $<x$ (power 1) $<\\sqrt x$ (power $\\frac12$).',
        'Check with $x=\\frac14$: $\\frac1{16}<\\frac14<\\frac12$ ✓.'])
    S('alg-extra-unit-t17-3-3', stem='On a number line, what is the distance between $-8$ and $5$?',
      choices=['$8$', '$40$', '$13$', '$3$'], expl=[
          'Distance = the bigger number minus the smaller one: $5-(-8)=5+8=13$.',
          'On the line: 8 steps from $-8$ to $0$, and 5 more to $5$.'])
    S('alg-extra-unit-t17-3-4', stem='Given: $2<x<5$. Which of the following is necessarily true?',
      choices=['$\\frac15<\\frac1x<\\frac12$', '$\\frac12<\\frac1x<\\frac15$', '$2<\\frac1x<5$', '$0<\\frac1x<\\frac15$'], expl=[
          'For positive numbers, reciprocals reverse the order: $2<x<5$ gives $\\frac15<\\frac1x<\\frac12$.',
          'Check: $x=4$: $\\frac14$ is between $\\frac15$ and $\\frac12$ ✓.'])
    S('alg-extra-unit-t17-3-5', stem='Given: $a<-2$. Which of the following is necessarily true?',
      choices=['$a^2>4$', '$a^3>-8$', '$a>0$', '$a^2<4$'], expl=[
          '$a$ is further from zero than $-2$, so $a^2>(-2)^2=4$.',
          'The others are false: an odd power keeps the order, so $a^3<-8$; and $a<0$.',
          'Check: $a=-3$: $a^2=9>4$ ✓.'])
    S('alg-extra-unit-t17-3-6', stem='On a number line, what is the midpoint between $-9$ and $3$?',
      choices=['$0$', '$6$', '$-3$', '$-6$'], expl=[
          'The midpoint is the average of the two numbers: $\\frac{-9+3}{2}=\\frac{-6}{2}=-3$.',
          'Check: from $-9$ to $-3$ is 6, and from $-3$ to $3$ is also 6 ✓.'])
    S('alg-extra-unit-t17-3-7', stem='Given: $0<a<b$. Which of the following is necessarily positive?',
      choices=['$-a\\cdot b$', '$\\frac1a-\\frac1b$', '$a-b$', '$a^2-b^2$'], expl=[
          'For positive numbers, reciprocals reverse the order: $a<b$ gives $\\frac1a>\\frac1b$, so $\\frac1a-\\frac1b>0$.',
          'Or: $\\frac1a-\\frac1b=\\frac{b-a}{ab}$, and both $b-a$ and $ab$ are positive.',
          'The others are negative: $-a\\cdot b<0$, $a-b<0$, and $a^2<b^2$.'])

    # keep video titles / slide notes in sync with the rewritten stems
    for qid in ['q-493', 'q-494', 'q-495', 'q-496', 'q-497', 'q-498', 'q-499', 'q-500', 'q-501']:
        v = M.video('solve-' + qid); q = M.q(qid)
        v['title'] = v['navLabel'] = q['stem']
        for b in v['beats']:
            if b.get('canvas', '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])

    # =====================================================================================
    # 7. Practice: remove near-duplicates / trivial items
    # =====================================================================================
    # Pass 2 (teacher's plan): q-505 and alg-extra-unit-t17-3-1 are original questions - they stay (clean text only)
    S('q-505', stem='Given: $1<m<n$. Which of the following expressions is the largest?',
      choices=['$n^3$', '$m\\cdot n^2$', '$m^2\\cdot n$', '$m^3$'], correct=1, expl=[
          'Plug in $m=2$, $n=4$: $n^3=64$, $m\\cdot n^2=2\\cdot16=32$, $m^2\\cdot n=4\\cdot4=16$, $m^3=8$. The largest is $n^3$.',
          'Why: all the numbers are greater than 1. $n^3=n\\cdot n\\cdot n$ uses the strongest factor three times (strong on strong). Every other choice has $m<n$ in place of at least one $n$, so it is smaller.'])
    S('alg-extra-unit-t17-3-1', stem='Given: $-1<x<0$. Which of the following is the largest?',
      choices=['$x$', '$x^3$', '$-1$', '$x^2$'], correct=4, expl=[
          '$x^2$ is an even power of a negative number, so it is positive. $x$, $x^3$ and $-1$ are all negative.',
          'So $x^2$ is the largest. Check with $x=-\\frac12$: $x=-\\frac12$, $x^3=-\\frac18$, $-1$ and $x^2=\\frac14$. The largest is $\\frac14$.'])

    # =====================================================================================
    # 8. New lesson: negative multipliers, reciprocals, test numbers, must/could, pictures, distance
    # =====================================================================================
    sb = ['Times a negative', 'Reciprocals', 'Test numbers', 'Must or could?', 'Picture questions',
          'Distance & midpoint', 'Recap']
    v = M.new_video(READ, TOPIC, 'Reading the Number Line', sb, [
        dict(mode='title', title='Reading the Number Line', script=[
            "Reading the number line.",
            "Before the advanced questions: a few more tools.",
            "Negative multipliers, reciprocals, which numbers to test — and questions with a picture of the line.",
        ]),
        dict(mode='concept', active=0, title='Times a negative', script=[
            "So far we multiplied by positive numbers. Now: times a NEGATIVE number.",
            A('3 · (−2) = −6 and −3 · (−2) = 6 appear', T('$3\\cdot(-2)=-6 \\qquad {-3}\\cdot(-2)=6$', size=54, gap=50)),
            "Three times minus two: minus six. It jumped to the other side of zero.",
            "Minus three times minus two: plus six. It jumped too.",
            "Times a negative number — you always land on the other side of zero.",
            A('2 < 5 → −2 > −5 appears', T('$2<5\\ \\Rightarrow\\ -2>-5$', size=54, gap=50)),
            D('Mark 2 and 5, then −2 and −5, on a number line and draw the mirror arrows'),
            "And the order flips. Two is less than five. But minus two is MORE than minus five.",
            "It's the mirror again. The same rule as in inequalities: multiply by a minus — flip the sign.",
            A('−1 < a < 0 and b > 1 → a · b < a appears', T('$-1<a<0,\\ \\ b>1\\ \\Rightarrow\\ a\\cdot b<a$', size=50)),
            "One more: a negative fraction times a number above one.",
            "Times more than one — away from zero. On the negative side, away from zero means SMALLER.",
            D('Write "a = −½, b = 3: a · b = −3/2 < −½"'),
        ]),
        dict(mode='concept', active=1, title='Reciprocals', script=[
            "Next: the reciprocal — one over x. Where does it land?",
            A('x > 1 → 0 < 1/x < 1 appears', T('$x>1\\ \\Rightarrow\\ 0<\\frac1x<1$', size=44)),
            "Above one: two becomes one half. It drops to a positive fraction.",
            A('0 < x < 1 → 1/x > 1 appears', T('$0<x<1\\ \\Rightarrow\\ \\frac1x>1$', size=44)),
            "A positive fraction: one half becomes two. It jumps above one.",
            A('−1 < x < 0 → 1/x < −1 appears', T('$-1<x<0\\ \\Rightarrow\\ \\frac1x<-1$', size=44)),
            A('x < −1 → −1 < 1/x < 0 appears', T('$x<-1\\ \\Rightarrow\\ -1<\\frac1x<0$', size=44, gap=40)),
            "The negative side is the mirror. Minus one half becomes minus two. Minus two becomes minus one half.",
            "The sign never changes. Only the range: big and small swap.",
            A('2 < x < 5 → 1/5 < 1/x < 1/2 appears', T('$2<x<5\\ \\Rightarrow\\ \\frac15<\\frac1x<\\frac12$', size=48)),
            "And for numbers with the same sign, reciprocals flip the order. x between two and five: one over x is between one fifth and one half.",
            D('Write "x = 4: 1/4 ✓"'),
            "Check with four: one quarter. Yes — between a fifth and a half.",
        ]),
        dict(mode='concept', active=2, title='Test numbers', script=[
            "No range given, or you're not sure? Plug in. But which numbers?",
            A("'Test numbers: 2, 1/2, −1/2, −2' appears", T('Test numbers:  $2,\\ \\ \\frac12,\\ \\ {-\\frac12},\\ \\ {-2}$', size=54, gap=50)),
            "One from each range: two, one half, minus one half, minus two.",
            A("'Borders: −1, 0, 1 — if they are allowed' appears", T('Borders:  $-1,\\ \\ 0,\\ \\ 1$ — if they are allowed', size=46, gap=50)),
            "And the borders — minus one, zero, one — when the question allows them. They are the classic traps.",
            A("'Roots: 1/4 for √x · ±1/8 for ∛x · −1/32 for ⁵√x' appears",
              T('Roots:  $\\frac14$ for $\\sqrt{x}$  ·  $\\pm\\frac18$ for $\\sqrt[3]{x}$  ·  $-\\frac1{32}$ for $\\sqrt[5]{x}$', size=44)),
            "A root in the choices? Pick a number with a clean root.",
            "One quarter for a square root. One eighth for a cube root. One over thirty-two for a fifth root.",
            "Nice numbers — no calculator needed.",
        ]),
        dict(mode='concept', active=3, title='Must or could?', script=[
            "Many questions ask: which is NECESSARILY true? Or: which COULD be true?",
            A("'Necessarily true: one counter-example kills it' appears", T('Necessarily true: one counter-example kills it', size=46, gap=40)),
            "Necessarily true means: true for every number allowed. One example where it fails — and it's out.",
            A("'Could be true: one example proves it' appears", T('Could be true: one example proves it', size=46, gap=50)),
            "Could be true: one example where it works is enough.",
            "How do you find a counter-example? Push the values to the edges of their ranges.",
            A('0 < p < q < 1 < r < s: r + q < s + p? appears', T('$0<p<q<1<r<s$:  is $r+q<s+p$?', size=46)),
            D('Write "p = 0.1, q = 0.9, r = 1.1, s = 1.2 → 2 > 1.3 ✗"'),
            "p very small, q almost one, r and s close together. The claim breaks. So it's not necessarily true.",
            "You'll use this in the questions ahead.",
        ]),
        dict(mode='concept', active=4, title='Picture questions', script=[
            "On the exam, the number line often comes as a picture. Letters sit on the line.",
            A('A number line with a, b and c appears', VIS(FIG_DEMO, w=1000, h=250, gap=30)),
            "Step one: write the range of each letter under it.",
            D('Under a write "< −1", under b write "0 to 1", under c write "> 1"'),
            "a is below minus one. b is a positive fraction. c is above one.",
            A("'Trust the order, not the distances' appears", T('Not drawn to scale? Trust the order, not the distances.', size=42, gap=40)),
            "Step two: is the picture to scale? Unless the question says so, trust only the ORDER of the points — not the distances.",
            "b looks close to zero. It could still be zero point nine.",
            D('Write "b² < b,  1/b > 1,  a · c < a"'),
            "Now it's a normal question. b squared is less than b. One over b is above one. And a times c is less than a — times more than one, away from zero.",
        ]),
        dict(mode='concept', active=5, title='Distance & midpoint', script=[
            "Last tool: distance and midpoint.",
            A('Distance = bigger − smaller appears', T('Distance $=$ bigger $-$ smaller:  $5-(-8)=13$', size=46, gap=50)),
            "The distance between two numbers: the bigger one minus the smaller one.",
            "From minus eight to five: five minus minus eight. Thirteen. Eight steps to zero, five more to five.",
            A('Midpoint = (a + b)/2 appears', T('Midpoint $=\\frac{a+b}{2}$  ·  $\\frac{-9+3}{2}=-3$', size=46, gap=50)),
            "The midpoint is the average. Minus nine and three: minus six over two — minus three.",
            D('Write "check: −9 → −3 is 6, −3 → 3 is 6 ✓"'),
            "A third of the way? Take a third of the distance, and walk it from the starting point.",
            D('Write "from −7 to 5: distance 12, a third is 4 → −7 + 4 = −3"'),
        ]),
        dict(mode='concept', active=6, title='Recap', script=[
            "Let's lock it in.",
            A("'Times a negative: other side of zero, order flips' appears", T('Times a negative: other side of zero, the order flips', size=38)),
            A("'Reciprocal: same sign, big and small swap' appears", T('Reciprocal: same sign, big and small swap, the order flips', size=38)),
            A("'Test numbers' appears", T('Test numbers: $2,\\ \\frac12,\\ {-\\frac12},\\ {-2}$ and the borders', size=38)),
            A("'Necessarily: one counter-example · Could: one example' appears", T('Necessarily: one counter-example kills it · Could: one example', size=38)),
            A("'Picture: write each range, trust only the order' appears", T('Picture: write each range, trust only the order', size=38)),
            A("'Distance and midpoint' appears", T('Distance $=$ bigger $-$ smaller · Midpoint $=\\frac{a+b}{2}$', size=38)),
            D('Tick each line'),
            "Now the advanced questions. Try each one first — then watch.",
        ]),
    ], 'number-line-advanced', before='q-495')
    v['hybrid']['num'] = M.video(L2)['hybrid']['num']

    M.new_card(CARD2, TOPIC, 'number-line-advanced', {
        'title': 'Reading the number line',
        'intro': 'Negative multipliers, reciprocals, test numbers, pictures, distance.',
        'tables': [
            {'title': 'The reciprocal \\(\\frac1x\\) in each range', 'head': ['\\(x\\)', '\\(\\frac1x\\)', 'Example'], 'rows': [
                ['\\(x>1\\)', '\\(0<\\frac1x<1\\)', '\\(2\\to\\frac12\\)'],
                ['\\(0<x<1\\)', '\\(\\frac1x>1\\)', '\\(\\frac12\\to2\\)'],
                ['\\(-1<x<0\\)', '\\(\\frac1x<-1\\)', '\\(-\\frac12\\to-2\\)'],
                ['\\(x<-1\\)', '\\(-1<\\frac1x<0\\)', '\\(-2\\to-\\frac12\\)']]},
            {'title': 'Numbers to plug in', 'head': ['When', 'Try'], 'rows': [
                ['No range given', '\\(2,\\ \\frac12,\\ -\\frac12,\\ -2\\), and the borders \\(-1,\\ 0,\\ 1\\) if allowed'],
                ['Square root', '\\(x=\\frac14\\)'], ['Cube root', '\\(x=\\pm\\frac18\\)'],
                ['Fifth root', '\\(x=-\\frac1{32}\\)'], ['Tenth root', '\\(x=\\frac1{1024}\\)']]},
            {'title': 'Distance and midpoint', 'head': ['', 'Rule', 'Example'], 'rows': [
                ['Distance', 'bigger \\(-\\) smaller', '\\(5-(-8)=13\\)'],
                ['Midpoint', '\\(\\frac{a+b}{2}\\)', '\\(\\frac{-9+3}{2}=-3\\)'],
                ['A third of the way from \\(a\\)', '\\(a+\\frac13\\cdot\\)distance', '\\(-7+\\frac13\\cdot12=-3\\)']]},
        ],
        'tips': [
            'Times a negative number: jump to the other side of zero, and the order flips.',
            'Same sign: reciprocals flip the order: \\(2<x<5\\Rightarrow\\frac15<\\frac1x<\\frac12\\).',
            'Necessarily true: one counter-example kills it — push the values to the edges. Could be true: one example is enough.',
            'Picture of the line: write the range under each letter. Unless it says "drawn to scale", trust only the order.',
            'Change only the unknown when you plug in — never the numbers in the question.',
        ]}, after=READ)

    # =====================================================================================
    # 9. New guided questions 10-14 (end of the advanced section)
    # =====================================================================================
    g = ['q-r26-t17-%02d' % k for k in range(1, 6)]

    M.new_q(g[0], TOPIC, 'The figure shows the numbers $a$, $b$, $c$ and $d$ on a number line (the figure is not drawn to scale).\nWhich of the following is necessarily negative?',
            ['$\\frac ab$', '$b\\cdot c\\cdot d$', '$a+d$', '$b^3-b$'], 2, [
                'From the figure: $a<-1$, $-1<b<0$, $0<c<1$ and $d>1$.',
                '(1) A negative number over a negative number is positive, so $\\frac ab>0$.',
                '(2) One negative factor and two positive ones, so $b\\cdot c\\cdot d$ is always negative. ✓',
                '(3) $a+d$ depends on the distances, and the figure is not to scale: $a=-5$, $d=2$ gives $-3$, but $a=-2$, $d=5$ gives $3$.',
                '(4) For a negative fraction the cube is bigger (the arrow points right): $b^3>b$, so $b^3-b>0$.'],
            figure=FIG_Q10)
    M.place_q(g[0], 'number-line-advanced', after='solve-q-501')
    _solution(M, g[0], ["A picture question.", "Letters on the line — read the ranges first."], [
        ('Ranges first', [
            "Four letters on the line. Step one: the range of each letter.",
            D('Under a write "< −1", under b write "−1 to 0", under c write "0 to 1", under d write "> 1"'),
            "a is below minus one. b is a negative fraction. c is a positive fraction. d is above one.",
            "We want the one that is ALWAYS negative.",
            D('Next to choice 1 write "− ÷ − = +" and cross it out'),
            "Choice one: a over b. Negative over negative — positive. Out.",
            D('Next to choice 2 write "− · + · + = −"'),
            "Choice two: b times c times d. One negative, two positives — negative. Always.",
            "Let's check the others too.",
            D('Next to choice 3 write "a = −5, d = 2 → −3;  a = −2, d = 5 → 3" and cross it out'),
            "Choice three: a plus d. A negative plus a positive — it depends on the distances. And the picture is not to scale.",
            "Minus five plus two is negative. Minus two plus five is positive. Not necessarily. Out.",
            D('Next to choice 4 write "b³ > b → b³ − b > 0" and cross it out'),
            "Choice four: b cubed minus b. b is a negative fraction — the arrow points right, so b cubed is bigger than b.",
            "Bigger minus smaller — positive. Out.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
    ])

    M.new_q(g[1], TOPIC, 'The figure shows the number $x$ and the points K, L, M and N on a number line (the figure is not drawn to scale).\nWhich of the points could represent the number $\\sqrt{x}$?',
            ['K', 'L', 'M', 'N'], 3, [
                'From the figure: $0<x<1$.',
                '$\\sqrt x=x^{\\frac12}$. For a positive fraction, a smaller power gives a bigger number, so $\\sqrt x>x$. And the root of a positive number less than 1 is less than 1.',
                'So $x<\\sqrt x<1$. Only point M is between $x$ and $1$.',
                'Check: $x=\\frac14$ gives $\\sqrt x=\\frac12$, between $\\frac14$ and $1$ ✓. (L could be $x^2$, N could be $\\frac1x$, and K could be $-x$.)'],
            figure=FIG_Q11)
    M.place_q(g[1], 'number-line-advanced', after='solve-' + g[0])
    _solution(M, g[1], ["Another picture.", "This time: where does the root land?"], [
        ('Where does √x land?', [
            "x is between zero and one — a positive fraction.",
            "The square root is a power of one half. For a positive fraction, a smaller power means a bigger number.",
            D('Write "½ < 1 → √x > x"'),
            "So the root is bigger than x. But the root of a number below one stays below one.",
            D('Shade the part of the line between x and 1'),
            "Between x and one. Only one point sits there: M.",
            D('Circle choice 3'),
            "Choice three.",
            D('Write "x = ¼ → √x = ½"'),
            "Check: x is one quarter, the root is one half — to the right of x, still below one.",
            "The traps: L is where x squared would be. N is where one over x would be. K is minus x.",
        ]),
    ])

    M.new_q(g[2], TOPIC, 'Given: $-4<x<-2$. Which of the following is necessarily true?',
            ['$-24<\\frac6x<-12$', '$\\frac32<\\frac6x<3$', '$-3<\\frac6x<-\\frac32$', '$-\\frac23<\\frac6x<-\\frac13$'], 3, [
                'Reciprocals keep the sign and reverse the order of numbers with the same sign: $-4<x<-2$ gives $-\\frac12<\\frac1x<-\\frac14$.',
                'Multiply by 6 (a positive number, so the order stays): $-3<\\frac6x<-\\frac32$.',
                'Check the ends: $\\frac6{-4}=-\\frac32$ and $\\frac6{-2}=-3$ ✓.'])
    M.place_q(g[2], 'number-line-advanced', after='solve-' + g[1])
    _solution(M, g[2], ["Reciprocals — with negative numbers."], [
        ('Method 1 · Flip, then multiply', [
            "x is between minus four and minus two. Where is six over x?",
            "Six over x is six times one over x. Start with the reciprocal.",
            D('Write "−4 < x < −2 → −½ < 1/x < −¼"'),
            "Same sign — so the reciprocal flips the order. Minus four becomes minus a quarter. Minus two becomes minus a half. Now minus a half is the smaller end.",
            D('Write "× 6 → −3 < 6/x < −3/2"'),
            "Times six — a positive number — keeps the order. Minus three to minus three halves.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Method 2 · Test the ends', [
            "Faster: plug in the two ends.",
            D('Write "x = −4 → 6 ÷ (−4) = −3/2;  x = −2 → 6 ÷ (−2) = −3"'),
            "Six over minus four: minus one and a half. Six over minus two: minus three.",
            "So six over x is between minus three and minus one and a half. The smaller number goes on the left.",
            D('Circle choice 3'),
            "Choice three. The traps: choice one multiplied instead of dividing. Choice two lost the minus sign. Choice four is x over six.",
        ]),
    ])

    M.new_q(g[3], TOPIC, 'Given: $x<-1<y<0$. Which of the following is necessarily true?',
            ['$x\\cdot y>1$', '$x+y<-1$', '$x^2<y^2$', '$\\frac xy<1$'], 2, [
                'Test numbers at the edges: $x=-2$, $y=-\\frac12$.',
                '(1) $x\\cdot y=1$, which is not greater than 1. Not necessarily true.',
                '(2) $x<-1$ and $y<0$, so $x+y<-1$. Always true. ✓',
                '(3) $x^2>1$ and $y^2<1$, so $x^2>y^2$. Never true.',
                '(4) $\\frac xy$ is positive, and $x$ is further from zero than $y$, so $\\frac xy>1$. Never true.'])
    M.place_q(g[3], 'number-line-advanced', after='solve-' + g[2])
    _solution(M, g[3], ["Two letters, two different ranges.", "Which statement is ALWAYS true?"], [
        ('Test at the edges', [
            D('Under x write "< −1", under y write "−1 to 0"'),
            "x is below minus one. y is a negative fraction.",
            "Test numbers — pushed to the edges: x equals minus two, y equals minus one half.",
            D('Write "x = −2, y = −½"'),
            D('Next to choice 1 write "(−2) · (−½) = 1 > 1? ✗" and cross it out'),
            "Choice one: minus two times minus a half — exactly one. Not more than one. Not necessarily true.",
            D('Next to choice 2 write "(< −1) + (< 0) < −1 ✓"'),
            "Choice two: x plus y. x is already below minus one, and adding a negative y moves it further left. Always true.",
            D('Next to choice 3 write "x² > 1 > y²" and cross it out'),
            "Choice three: x squared is more than one; y squared is less than one. Never true.",
            D('Next to choice 4 write "(−2) ÷ (−½) = 4 > 1" and cross it out'),
            "Choice four: negative over negative is positive — and x is further from zero than y, so x over y is more than one. Never true.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
    ])

    M.new_q(g[4], TOPIC, 'On a number line, point A is at $-7$ and point B is at $5$. Point C is between A and B, and its distance from A is one third of the distance AB.\nWhat number is at point C?',
            ['$-1$', '$4$', '$-3$', '$1$'], 3, [
                'Distance AB: $5-(-7)=12$.',
                'One third of it: $\\frac13\\cdot12=4$.',
                'Start at A and move 4 to the right: $C=-7+4=-3$.',
                '($-1$ is the midpoint, $1$ is one third of the way from B, and $4$ is a distance, not a point.)'])
    M.place_q(g[4], 'number-line-advanced', after='solve-' + g[3])
    _solution(M, g[4], ["Last question of the set.", "Distance on the number line."], [
        ('Distance first', [
            "A is at minus seven, B at five. First: the distance.",
            D('Write "AB = 5 − (−7) = 12"'),
            "Bigger minus smaller: five minus minus seven. Twelve.",
            D('Write "⅓ · 12 = 4"'),
            "C is one third of the way from A. A third of twelve is four.",
            D('Write "C = −7 + 4 = −3"'),
            "Start at A and walk four steps to the right: minus three.",
            D('Circle choice 3'),
            "Choice three.",
            "The traps: minus one is the midpoint. Four is the distance, not the point. One is a third of the way from B.",
        ]),
    ])
    # old Q9 video said "That's the number line done."
    _replace_say(M, 'solve-q-501', 2, "That's the number line done", ["Five more questions — with pictures, reciprocals and distances."])

    # =====================================================================================
    # 10. New practice questions (exam level)
    # =====================================================================================
    P = ['q-r26-t17-%02d' % k for k in range(6, 16)]
    M.new_q(P[0], TOPIC, 'The figure shows the numbers $a$ and $b$ on a number line (the figure is not drawn to scale).\nWhich of the following is the smallest?',
            ['$a$', '$a\\cdot b$', '$\\frac ab$', '$a^2$'], 2, [
                'From the figure: $-1<a<0$ and $b>1$.',
                '$a^2>0$, so it is not the smallest. The other three are negative.',
                'Multiplying by $b>1$ moves $a$ away from zero; on the negative side that is smaller: $a\\cdot b<a$. Dividing by $b>1$ moves $a$ toward zero: $\\frac ab>a$.',
                'Check: $a=-\\frac12$, $b=2$: $a\\cdot b=-1$, $a=-\\frac12$, $\\frac ab=-\\frac14$, $a^2=\\frac14$. The smallest is $a\\cdot b$.'],
            figure=FIG_P1)
    M.new_q(P[1], TOPIC, 'The figure shows the numbers $x$ and $y$ on a number line (the figure is not drawn to scale).\nWhich of the following is necessarily positive?',
            ['$x+y$', '$x-y$', '$\\frac xy-1$', '$x\\cdot y-x^2$'], 3, [
                'From the figure: $x<y<0$, so $x$ is further from zero than $y$.',
                '$x+y<0$ (two negative numbers). $x-y<0$ ($x$ is to the left of $y$).',
                '$\\frac xy$: negative over negative is positive, and $x$ is further from zero, so $\\frac xy>1$ and $\\frac xy-1>0$. ✓',
                '$x\\cdot y-x^2=x(y-x)$: $x<0$ and $y-x>0$, so it is negative.',
                'Check: $x=-2$, $y=-1$: $\\frac xy-1=2-1=1$, while $x\\cdot y-x^2=2-4=-2$.'],
            figure=FIG_P2)
    M.new_q(P[2], TOPIC, 'The figure shows the number $x$ and the points A, B, C and D on a number line (the figure is not drawn to scale).\nWhich of the points could represent the number $x^3$?',
            ['A', 'B', 'C', 'D'], 3, [
                'From the figure: $-1<x<0$, a negative fraction.',
                'For a negative fraction the arrow points right: the cube is bigger than $x$, and an odd power stays negative. So $x<x^3<0$.',
                'Only C is between $x$ and $0$.',
                'Check: $x=-\\frac12$: $x^3=-\\frac18$, to the right of $-\\frac12$ and to the left of $0$ ✓.'],
            figure=FIG_P3)
    M.new_q(P[3], TOPIC, 'Given: $-2<x<-\\frac12$. Which of the following is necessarily true?',
            ['$\\frac12<\\frac1x<2$', '$-2<\\frac1x<-\\frac12$', '$-\\frac12<\\frac1x<0$', '$\\frac1x<-2$'], 2, [
                'Reciprocals keep the sign, and for numbers with the same sign they reverse the order.',
                '$x=-2$ gives $\\frac1x=-\\frac12$, and $x=-\\frac12$ gives $\\frac1x=-2$. So $-2<\\frac1x<-\\frac12$ — the same range as $x$.',
                'Check: $x=-1$ gives $\\frac1x=-1$ ✓.'])
    M.new_q(P[4], TOPIC, 'Given: $2<x<5$. Which of the following is necessarily true?',
            ['$7<1-3x<16$', '$-16<1-3x<-7$', '$-15<1-3x<-6$', '$-14<1-3x<-5$'], 4, [
                'Multiply by $-3$: the numbers jump to the other side of zero and the order flips: $-15<-3x<-6$.',
                'Add 1: $-14<1-3x<-5$.',
                'Check the ends: $x=2$ gives $1-6=-5$; $x=5$ gives $1-15=-14$ ✓.'])
    M.new_q(P[5], TOPIC, 'Given: $x^3<x$. Which of the following could be the value of $x$?',
            ['$-1$', '$-\\frac12$', '$1$', '$-2$'], 4, [
                'The borders fail: $x=-1$ gives $-1<-1$, false. $x=1$ gives $1<1$, false.',
                '$x=-\\frac12$: $\\left(-\\frac12\\right)^3=-\\frac18$, and $-\\frac18>-\\frac12$. False (for a negative fraction the cube is bigger).',
                '$x=-2$: $(-2)^3=-8<-2$ ✓.',
                'In general, $x^3<x$ for $x<-1$ and for $0<x<1$.'])
    M.new_q(P[6], TOPIC, 'On a number line, point A is at $-11$ and point B is at $7$. Point C is between A and B, and its distance from A is twice its distance from B.\nWhat number is at point C?',
            ['$-5$', '$-2$', '$1$', '$3$'], 3, [
                'Distance AB: $7-(-11)=18$.',
                'C splits AB into two parts, and the part next to A is twice the part next to B: $18=12+6$. So C is 12 to the right of A.',
                '$C=-11+12=1$.',
                'Check: from $-11$ to $1$ is 12, and from $1$ to $7$ is 6 ✓. ($-2$ is the midpoint; $-5$ is twice as far from B.)'])
    M.new_q(P[7], TOPIC, 'Given: $-1<a<0<b$. Which of the following could be equal to 1?',
            ['$-\\frac ba$', '$a^2$', '$a\\cdot b$', '$a-b$'], 1, [
                '$a^2$: $a$ is a negative fraction, so $0<a^2<1$. Never 1.',
                '$a\\cdot b<0$ and $a-b<0$. Never 1.',
                '$-\\frac ba$ is positive. Example: $a=-\\frac12$, $b=\\frac12$: $\\frac ba=-1$, so $-\\frac ba=1$ ✓. For "could be", one example is enough.'])
    M.new_q(P[8], TOPIC, 'Given: $0<x<1<y$. Which of the following is necessarily true?',
            ['$x\\cdot y>1$', '$\\frac xy<x$', '$x^2\\cdot y<x$', '$y-x>1$'], 2, [
                '(2) Dividing the positive number $x$ by $y>1$ makes it smaller: $\\frac xy<x$. Always true.',
                'The others fail when you push the values to the edges:',
                '(1) $x=\\frac12$, $y=\\frac32$: $x\\cdot y=\\frac34<1$. (3) $x=\\frac12$, $y=4$: $x^2\\cdot y=1>\\frac12$. (4) $x=0.9$, $y=1.1$: $y-x=0.2<1$.'])
    M.new_q(P[9], TOPIC, 'Given: $0<a<b<1$. Which of the following is the largest?',
            ['$\\frac1b$', '$\\frac ba$', '$\\sqrt b$', '$\\frac1a$'], 4, [
                '$\\sqrt b<1$. The other three are greater than 1.',
                'Reciprocals reverse the order: $a<b$ gives $\\frac1a>\\frac1b$.',
                '$\\frac ba=b\\cdot\\frac1a$, and multiplying by the fraction $b$ makes $\\frac1a$ smaller: $\\frac ba<\\frac1a$.',
                'Check: $a=\\frac19$, $b=\\frac14$: $\\frac1b=4$, $\\frac ba=\\frac94$, $\\sqrt b=\\frac12$, $\\frac1a=9$. The largest is $\\frac1a$.'])
    for qid in P:
        M.place_q(qid, 'unit-t17-3')

    # easy -> hard
    M.practice_order('unit-t17-3', [
        'alg-extra-unit-t17-3-3', 'alg-extra-unit-t17-3-6', 'alg-extra-unit-t17-3-1', 'alg-extra-unit-t17-3-5',
        'alg-extra-unit-t17-3-2', 'q-502', 'q-506', 'alg-extra-unit-t17-3-4', 'alg-extra-unit-t17-3-7', 'q-503', 'q-505',
        P[3], P[4], 'q-504',
        'q-508', 'q-509', P[2], P[0], 'q-507', P[7], P[5], 'q-510', 'q-511', P[1], P[8], P[9], P[6]])
    summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last


# =========================================================================================
# Pass 2: summary lesson right before the practice (the topic has one practice section)
# =========================================================================================
def summary(M):
    sb = ['Four ranges', 'Multiply & divide', 'Hierarchy', 'Exceptions first', 'The arrows', 'Reciprocals',
          'Test numbers', 'Must or could?', 'Distance & midpoint', 'Before you practice']
    C = lambda i, script: dict(title=sb[i], mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — the whole number line in a few minutes.",
            "Every rule, every trap. Short and fast.",
        ]),
        C(0, [
            "It all starts with four ranges.",
            A("'x < −1 · −1 < x < 0 · 0 < x < 1 · x > 1' appears", T('$x<-1\\quad\\ -1<x<0\\quad\\ 0<x<1\\quad\\ x>1$', size=50, gap=40)),
            "Below minus one, negative fractions, positive fractions, above one. Every number in a range behaves the same way.",
            A("'Borders: −1, 0, 1' appears", T('Borders: $-1,\\ 0,\\ 1$ — are they allowed?', size=44, gap=40)),
            "Watch the borders. And if they only say x is positive — it could be below one or above one.",
            A("'Negatives mirror the positives' appears", T('Negatives mirror the positives', size=44)),
            "The negative side is a mirror. Look at the positive side, then mirror the picture.",
        ]),
        C(1, [
            "What do multiplying and dividing do? One is the dividing line.",
            A("'× more than 1 or ÷ a fraction → bigger' appears", T('$\\times$ more than 1, $\\div$ a fraction $\\to$ bigger:  $20\\div\\frac14=80$', size=42, gap=40)),
            A("'÷ more than 1 or × a fraction → smaller' appears", T('$\\div$ more than 1, $\\times$ a fraction $\\to$ smaller:  $20\\cdot\\frac14=5$', size=42, gap=40)),
            "That's for positive numbers. A negative number makes the same moves — away from zero or toward zero.",
            A("'Times a negative: other side of zero, the order flips' appears", T('Times a negative: other side of zero, the order flips:  $3<7\\Rightarrow-3>-7$', size=40)),
            "And times a NEGATIVE number? You jump to the other side of zero — and the order flips.",
        ]),
        C(2, [
            "Hierarchy: a number in a higher range stays bigger — after any positive power or root.",
            A('The cube root of 7/6 and the square root of 3/4 appear', T('$\\sqrt[3]{\\frac76}>\\sqrt{\\frac34}$  (above 1 against a fraction)', size=46, gap=40)),
            "Seven sixths is above one; three quarters is a fraction. Don't calculate the roots.",
            "For negative numbers: odd powers and odd roots only.",
            A("'Same operation: ignore it (positive numbers only)' appears", T('Same operation on both? Ignore it — positive numbers only', size=42, gap=40)),
            A("'Strong on strong' appears", T('Strong on strong:  $0<a<b,\\ 0<c<d\\ \\Rightarrow\\ ac<bd$', size=42)),
            "Same operation on two positive numbers? Ignore it. And weak times weak loses to strong times strong.",
        ]),
        C(3, [
            "Exceptional powers move a number into another range. Handle them first.",
            A('(−4)² = 16 appears', T('Even power of a negative:  $(-4)^2=16$', size=46, gap=40)),
            "An even power of a negative number turns positive. Read the brackets: without them, minus four squared is minus sixteen.",
            A('(4/7)⁻² = (7/4)² appears', T('Negative exponent:  $\\left(\\frac47\\right)^{-2}=\\left(\\frac74\\right)^2>1$', size=46)),
            "A negative exponent: to compare ranges, flip it first. A fraction became a number above one.",
        ]),
        C(4, [
            "The arrows show what a bigger power does in each range.",
            A('The arrows of the positive side appear', T('$0<x<1:\\ \\leftarrow\\qquad x>1:\\ \\rightarrow$', size=48, gap=30)),
            A('The arrows of the negative side appear', T('$x<-1:\\ \\leftarrow\\qquad -1<x<0:\\ \\rightarrow$', size=48, gap=40)),
            "Right means bigger, left means smaller. On the negative side — odd powers only.",
            A('0 < x < 1 → x³ < x² < x < √x appears', T('$0<x<1:\\quad x^3<x^2<x<\\sqrt x$', size=48, gap=40)),
            "A positive fraction: a bigger power, a smaller number. The root goes the other way.",
            A("'Exceptions → roots to powers → arrows' appears", T('Exceptions $\\to$ roots to powers $\\to$ arrows', size=44)),
            "Three steps: exceptions, roots into powers, then the arrows. With the arrows you may keep a negative exponent.",
            "They give the order and ask for the range? Use the arrows backwards — or plug in.",
        ]),
        C(5, [
            "The reciprocal, one over x, keeps the sign — big and small swap.",
            A('0 < x < 1 → 1/x > 1 and x > 1 → 0 < 1/x < 1 appear', T('$0<x<1\\Rightarrow\\frac1x>1\\qquad x>1\\Rightarrow0<\\frac1x<1$', size=46, gap=40)),
            "A quarter becomes four. Four becomes a quarter. The negative side is the mirror.",
            A('4 < x < 10 → 1/10 < 1/x < 1/4 appears', T('$4<x<10\\ \\Rightarrow\\ \\frac1{10}<\\frac1x<\\frac14$', size=48)),
            "Numbers with the same sign: the reciprocal flips the order.",
        ]),
        C(6, [
            "Not sure? Plug in — one number from each allowed range.",
            A("'Test numbers: 2, 1/2, −1/2, −2' appears", T('Test numbers:  $2,\\ \\ \\frac12,\\ \\ {-\\frac12},\\ \\ {-2}$', size=50, gap=40)),
            A("'Roots: 1/4 for √x · ±1/8 for ∛x · −1/32 for ⁵√x' appears", T('Roots:  $\\frac14$ for $\\sqrt{x}$  ·  $\\pm\\frac18$ for $\\sqrt[3]{x}$  ·  $-\\frac1{32}$ for $\\sqrt[5]{x}$', size=42, gap=40)),
            "A root in the choices? Pick a number with a clean root.",
            A("'Change only x — never the numbers in the question' appears", T('Change only the unknown — never the numbers in the question', size=40)),
            "And change only the unknown. Changing the numbers in the question can change the answer.",
        ]),
        C(7, [
            "Read the question word: necessarily, or could?",
            A("'Necessarily: one counter-example kills it' appears", T('Necessarily true: one counter-example kills it', size=44, gap=40)),
            A("'Could be: one example is enough' appears", T('Could be true: one example is enough', size=44, gap=40)),
            "To find a counter-example, push the values to the edges of their ranges.",
            A("'Picture: write each range, trust only the order' appears", T('A picture of the line: write each range, trust only the order', size=40)),
            "A picture of the line? Write the range under each letter. Not drawn to scale — trust the order, not the distances.",
        ]),
        C(8, [
            "Last: distance and midpoint.",
            A('Distance = bigger − smaller appears', T('Distance $=$ bigger $-$ smaller:  $4-(-11)=15$', size=46, gap=40)),
            A('Midpoint = (a + b)/2 appears', T('Midpoint $=\\frac{a+b}{2}$:  $\\frac{-13+5}{2}=-4$', size=46)),
            "The midpoint is the average. A third of the way? Take a third of the distance and walk it from the start.",
        ]),
        C(9, [
            "Before you practice, always ask yourself:",
            A('Check 1', T('1. Which range am I in? Are the borders allowed?', size=40)),
            A('Check 2', T('2. Any exceptions? An even power of a negative, a negative exponent?', size=40)),
            A('Check 3', T('3. Positive or negative? Mirror, and flip for times a negative.', size=40)),
            A('Check 4', T('4. Necessarily, or could?', size=40)),
            "The common traps: ignoring an operation on negative numbers, forgetting that a positive x can be a fraction, and trusting the distances in a picture.",
            "You know all of this. Go practice.",
        ]),
    ]
    sec = 'number-line-advanced'
    last = [f['ref'] for f in M.D['flow'] if f['section'] == sec][-1]
    v = M.new_video('r26-t17-summary', TOPIC, 'The Number Line: Summary', sb, slides, sec, after=last)
    v['hybrid']['num'] = M.video(L2)['hybrid']['num']


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
    # Lesson "r26-t17-reading-the-line" slide 5 broke "r + q < s + p" for 0 < p < q < 1 < r < s - exactly the answer of
    # guided q-496 -> new lesson example with other letters and another claim.
    _dd_sub(M, 'r26-t17-reading-the-line', 5, [
        ('$0<p<q<1<r<s$:  is $r+q<s+p$?', '$0<a<b<1<c<d$:  is $d-c<b-a$?'),
        ('0 < p < q < 1 < r < s: r + q < s + p? appears', '0 < a < b < 1 < c < d: d − c < b − a? appears'),
        ('Write "p = 0.1, q = 0.9, r = 1.1, s = 1.2 → 2 > 1.3 ✗"', 'Write "a = 0.4, b = 0.5, c = 1.1, d = 3 → 1.9 > 0.1 ✗"'),
        ("p very small, q almost one, r and s close together. The claim breaks. So it's not necessarily true.",
         "a and b almost equal, d far to the right of c. Then d minus c is big, and b minus a is tiny. The claim breaks. So it's not necessarily true.")])
