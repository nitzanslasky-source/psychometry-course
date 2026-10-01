"""Topic 3 - Comparing Fractions: course review 2026-09 fixes (see t03_CHANGES.md)."""
import re
from math_api import T, H, A, D, Q

TOPIC = 3
LESSON = 'compare-fractions'
LEARN = 'fraction-theory'
PRACTICE = 'unit-t3-1'


def script_of(M, vid, n):
    """Current script of a slide in DSL form (so it can be edited and passed back to set_slide)."""
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def replace_line(script, old, new):
    """Replace one spoken line / draw note (exact match). new may be a str, a list (several entries) or None (delete)."""
    for k, x in enumerate(script):
        txt = x if isinstance(x, str) else (x[1] if x[0] == 'D' else None)
        if txt == old:
            rep = [] if new is None else (new if isinstance(new, list) else [new])
            return script[:k] + rep + script[k + 1:]
    raise KeyError('line not found: ' + old)


def insert_after(script, old, new):
    for k, x in enumerate(script):
        txt = x if isinstance(x, str) else x[1]
        if txt == old: return script[:k + 1] + list(new) + script[k + 1:]
    raise KeyError('line not found: ' + old)


# ------------------------------------------------------------------ lesson video
def fix_lesson(M):
    V = LESSON
    # slide 5 - cross-multiply: show WHY (common denominator 88) and the condition "both bottoms positive"
    s = script_of(M, V, 5)
    s = replace_line(s, "Big numbers? Don't panic — it still works. It's secretly a common denominator, comparing the tops.", [
        "Why does it work? It's secretly a common denominator.",
        A('55/88 and 56/88 appear', T(r'$\frac{5}{8}=\frac{55}{88}\qquad \frac{7}{11}=\frac{56}{88}$', size=50, y=390)),
        "Five eighths is fifty-five eighty-eighths. Seven elevenths is fifty-six eighty-eighths.",
        "Same bottom — now we just compare the tops. And the tops are exactly our two products.",
        A('The condition appears', T('Condition: both bottoms positive', size=40, y=490)),
        "One condition: both bottoms must be positive. A negative bottom breaks the method — you'll see it in a moment.",
    ])
    s = replace_line(s, "One method that always works beats five you half-remember.",
                     "With positive bottoms, one method you trust beats five you half-remember.")
    M.set_slide(V, 5, script=s)

    # slide 6 - decimals: no "always works"; show the decimals to know
    s = script_of(M, V, 6)
    s = insert_after(s, "Zero point four is bigger.", [
        A('Decimals to know, row 1', T(r'$\frac{1}{2}=0.5\quad \frac{1}{4}=0.25\quad \frac{1}{5}=0.2\quad \frac{1}{8}=0.125$', size=40, y=400)),
        A('Decimals to know, row 2', T(r'$\frac{1}{3}\approx 0.33\quad \frac{1}{6}\approx 0.17\quad \frac{1}{7}\approx 0.14\quad \frac{1}{9}\approx 0.11$', size=40, y=470)),
        "These are the decimals to know by heart. They're on your memory card.",
    ])
    s = replace_line(s, "But remember what always works?", "But remember cross-multiplying? Both bottoms are positive here.")
    M.set_slide(V, 6, script=s)

    # slide 7 - distance from 1: add fractions above 1
    s = script_of(M, V, 7)
    s += [
        "Above one? Same idea — look at the extra part.",
        A('7/6 and 19/16 written as 1 + extra', T(r'$\frac{7}{6}=1+\frac{1}{6}\qquad \frac{19}{16}=1+\frac{3}{16}$', size=50, y=420)),
        "Seven sixths is one plus one sixth. Nineteen sixteenths is one plus three sixteenths.",
        "Compare only the extras. One sixth against three sixteenths: cross-multiply, sixteen against eighteen.",
        D('Write "<" between 7/6 and 19/16'),
        "Three sixteenths is the bigger extra. Bigger extra, bigger number. Seven sixths is the smaller one.",
    ]
    M.set_slide(V, 7, script=s)

    # slide 8 - squaring: only for positive numbers
    s = script_of(M, V, 8)
    s = replace_line(s, "The bigger one stays bigger after squaring. Three over root ten wins.", [
        "Both fractions are positive. For positive numbers, the bigger one stays bigger after squaring. Three over root ten wins.",
        A('The squaring condition appears', T(r'Square only positive numbers: $-3<2$, but $9>4$', size=38, y=470)),
        "Careful: only for positive numbers. Negative three is less than two — but nine is more than four.",
    ])
    M.set_slide(V, 8, script=s)

    # slide 10 - flip: only when both have the same sign
    s = script_of(M, V, 10)
    s += [
        A('The flip condition appears', T(r'Flip reverses the order only for the same sign: $-2<3$ and $-\frac{1}{2}<\frac{1}{3}$', size=36, y=500)),
        "One condition: both numbers must have the same sign.",
        "Negative two is less than three. Flip them: negative one half is still less than one third. No reversal.",
    ]
    M.set_slide(V, 10, script=s)

    # slide 11 - recap without "always works"
    M.set_slide(V, 11, pre=[], script=[
        "Let's sum it up.",
        A("'Cross-multiply: bottoms positive' appears", T('Cross-multiply: both bottoms positive — products above the numerators', size=40)),
        D('Circle "both bottoms positive"'),
        "Cross-multiplication is the method I recommend most. It's simple, and it works for any two fractions with positive bottoms.",
        A('The shortcuts appear', T('Shortcuts: benchmark ½ · match tops or bottoms · distance from 1 · add to top and bottom · square (positives only) · flip (same sign only)', size=34)),
        "The others are shortcuts for when the numbers invite them.",
        A('Signs first appears', T('Letters? Signs first: a minus goes to the top · unknown sign → plug in, also a negative', size=34)),
        "With letters, check the signs first. A negative bottom? Move the minus to the top. Unknown sign? Plug in numbers — and try a negative too.",
        "Next: real exam-style questions. Try each one first — then watch its solution.",
    ])

    # new slides (inserted from the bottom up so the original numbers stay valid)
    M.insert_slides(V, 9, [dict(title='Which numbers?', mode='concept', script=[
        "Which numbers should you plug in? A few rules.",
        A('Rule 1 appears', T('1. Legal values only — check every given condition', size=38, gap=16)),
        "One: legal values only. If x is negative, a positive x proves nothing.",
        A('Rule 2 appears', T('2. Avoid 0 and 1 — they make many choices equal', size=38, gap=16)),
        "Two: avoid zero and one. One squared is one, one over one is one. Many choices come out equal — and you learn nothing.",
        A('Rule 3 appears', T('3. Two choices survive? Plug in a different kind of number: a negative, a fraction, a big number', size=38, gap=40)),
        "Three: if two choices survive, don't guess. Plug in a different kind of number.",
        A('"Necessarily true" appears', T('"Necessarily true": true for EVERY legal value — one counterexample kills a choice', size=36, gap=16)),
        "Read the question word. \"Necessarily true\" means true for every legal value. One counterexample is enough to kill a choice.",
        A('"Could be true" appears', T('"Could be true": one example is enough', size=36)),
        "\"Could be true\" is the opposite: one good example is enough.",
    ])])
    M.insert_slides(V, 8, [dict(title='x, x² or 1/x?', mode='concept', script=[
        "A favorite exam question: x is between zero and one. Which is bigger — x, x squared, root x, or one over x?",
        "Don't memorize blindly. Plug in a number from the range.",
        A('The order for 0 < x < 1 appears', T(r'$0<x<1:\quad x^2<x<\sqrt{x}<1<\frac{1}{x}$', size=48, y=110)),
        D('Under it write "x = 1/4: 1/16 < 1/4 < 1/2 < 1 < 4"'),
        "Take one quarter. x squared: one sixteenth. Root x: one half. One over x: four.",
        "Between zero and one, squaring makes a number smaller, and the root makes it bigger.",
        A('The order for x > 1 appears', T(r'$x>1:\quad \frac{1}{x}<1<\sqrt{x}<x<x^2$', size=48, y=320)),
        D('Under it write "x = 4: 1/4 < 1 < 2 < 4 < 16"'),
        "Above one, the order flips. Take four: one quarter, two, four, sixteen.",
        A('The order for −1 < x < 0 appears', T(r'$-1<x<0:\quad \frac{1}{x}<x<0<x^2$', size=48, y=530)),
        D('Under it write "x = −1/2: −2 < −1/2 < 0 < 1/4"'),
        "Negative? Take negative one half. One over x is negative two. x squared is one quarter — positive.",
        "Not sure which row? Plug in one number from the range. Ten seconds.",
    ])])
    M.insert_slides(V, 7, [dict(title='Add to top and bottom', mode='concept', script=[
        "Here's a classic exam trick: add the same number to the top and the bottom.",
        A('3/5 → 4/6 → 5/7 → 6/8 appears', T(r'$\frac{3}{5}\;\to\;\frac{4}{6}\;\to\;\frac{5}{7}\;\to\;\frac{6}{8}$', size=60, y=120)),
        "Three fifths, four sixths, five sevenths, six eighths. Each time: one more on top, one more on the bottom.",
        D('Under them write "0.6, 0.67, 0.71, 0.75"'),
        "Zero point six, about zero point six seven, zero point seven one, zero point seven five. It grows.",
        "Why? Distance from one: two fifths missing, then two sixths, two sevenths, two eighths. The missing part shrinks.",
        A('The rule below 1 appears', T('Below 1: add the same positive number to top and bottom → closer to 1 → bigger', size=36, y=400)),
        A('The rule above 1 appears', T('Above 1: add the same positive number → closer to 1 → smaller', size=36, y=470)),
        "Above one, it goes the other way. Seven fifths is one and two fifths. Eight sixths is one and two sixths — smaller.",
        "The rule: the fraction moves toward one. For positive numbers only.",
    ])])
    M.insert_slides(V, 5, [dict(title='Negatives', mode='concept', script=[
        "Now the trap. What if a bottom is negative?",
        A('1/(−2) ? 1/3 appears', T(r'$\frac{1}{-2}\quad ? \quad \frac{1}{3}$', size=66, y=150)),
        "Cross-multiply blindly: three times one, three — above the first. Negative two times one, negative two — above the second.",
        D('Above 1/(−2) write "3", above 1/3 write "−2"'),
        "Three beats negative two. So the first is bigger? No!",
        "One over negative two is negative one half. One third is positive. A negative number is always smaller than a positive one.",
        D('Write "<" between the fractions'),
        "With one negative bottom, the products point the wrong way.",
        A('The fix appears', T(r'Fix: move the minus to the top: $\frac{1}{-2}=-\frac{1}{2}$', size=40, y=360)),
        "The fix: move the minus sign to the top. Now the bottom is positive — and you can compare safely.",
        A('−2/3 ? −3/4 appears', T(r'$-\frac{2}{3}\quad ? \quad -\frac{3}{4}$', size=66, y=470)),
        "Two negative fractions? Compare them without the minus — then reverse.",
        D('Under them write "2/3 < 3/4 (8 < 9)"'),
        "Without the minus: two thirds against three quarters. Eight against nine — two thirds is smaller.",
        D('Write ">" between −2/3 and −3/4'),
        "With the minus, the order reverses. Negative two thirds is closer to zero — it's bigger.",
        "My tip: signs first. Negative is less than positive — no calculation needed.",
    ])])

    # sidebar + active index for every slide
    sb = ['Benchmark ½', 'Same top or bottom', 'Make them match', 'Cross-multiply', 'Negatives', 'To decimals',
          'Distance from 1', 'Add to top and bottom', 'Roots? Square it', 'x, x² or 1/x?', 'Plug in numbers',
          'Which numbers?', 'Flip them', 'Recap']
    M.set_sidebar(V, sb)
    for n in range(2, len(M.video(V)['beats']) + 1):
        M.slide(V, n)['active'] = n - 2
    assert len(M.video(V)['beats']) == 15


# ------------------------------------------------------------------ memory card
def fix_card(M):
    c = M.card('mem-compare')
    c['intro'] = 'Cross-multiplication works whenever both bottoms are positive — the rest are shortcuts. Signs first!'
    c['tables'] = [
        {'title': '', 'head': ['Method', 'When', 'Example'], 'rows': [
            ['Cross-multiply', 'both bottoms positive (move a minus to the top first); write each product above its numerator',
             r'$\frac58=\frac{55}{88}<\frac{56}{88}=\frac7{11}$'],
            ['Signs first', 'negative < positive; two negatives: compare without the minus, then reverse',
             r'$-\frac23>-\frac34$ because $\frac23<\frac34$'],
            ['Benchmark ½', 'one is above half, one below', r'$\frac5{13}<\frac12<\frac8{15}$'],
            ['Same bottom / same top', 'bigger top wins / smaller bottom wins (positive numbers)', r'$\frac5{13}<\frac5{11}$'],
            ['Distance from 1', 'both close to 1; above 1 compare the extras', r'$\frac89<\frac{11}{12}$, $\frac76=1+\frac16<1+\frac3{16}=\frac{19}{16}$'],
            ['Add to top and bottom', 'same positive number added: the fraction moves toward 1', r'$\frac35<\frac46<\frac57$;  $\frac75>\frac86$'],
            ['Square them', 'roots in the fractions — both positive only', r'$\frac3{\sqrt{10}}>\frac2{\sqrt5}$ because $\frac9{10}>\frac45$'],
            ['Flip them', 'same sign only — flipping reverses the order', r'$\frac{19}{3}>\frac{25}{4}$, so $\frac3{19}<\frac4{25}$'],
            ['Plug in numbers', 'letters: legal values, avoid 0 and 1; two survive → a negative or a fraction', '"necessarily" = true for every legal value'],
        ]},
        {'title': 'x by range (plug in one number to check)', 'head': ['Range', 'Order (small → big)', 'Try'], 'rows': [
            [r'$0<x<1$', r'$x^2<x<\sqrt{x}<1<\frac1x$', r'$x=\frac14$: $\frac1{16}, \frac14, \frac12, 4$'],
            [r'$x>1$', r'$\frac1x<1<\sqrt{x}<x<x^2$', r'$x=4$: $\frac14, 2, 4, 16$'],
            [r'$-1<x<0$', r'$\frac1x<x<0<x^2$', r'$x=-\frac12$: $-2, -\frac12, \frac14$'],
        ]},
        {'title': 'Decimals to know', 'head': ['Fraction', r'$\frac12$', r'$\frac13$', r'$\frac14$', r'$\frac15$', r'$\frac16$', r'$\frac17$', r'$\frac18$', r'$\frac19$'],
         'rows': [['Decimal', '0.5', '0.33', '0.25', '0.2', '0.17', '0.14', '0.125', '0.11']]},
    ]
    c['tips'] = [
        'Cross-multiplying, squaring and flipping all have a sign condition. Check the signs before you use them.',
        'A negative bottom: move the minus to the top. Then cross-multiply.',
        '"Necessarily true" needs every legal value; "could be true" needs one example.',
    ]


# ------------------------------------------------------------------ existing questions: text + solutions
def fix_questions(M):
    S = M.set_q
    S('q-fraction-compare', expl=[
        r'Half of 15 is 7.5, and $7<7.5$. Therefore $\frac{7}{15}<\frac{1}{2}$.',
        r'Half of 17 is 8.5, and $9>8.5$. Therefore $\frac{9}{17}>\frac{1}{2}$.',
        r'Check by cross-multiplying with $\frac{1}{2}$: $2\cdot 7=14<15$ and $2\cdot 9=18>17$.',
        r'The order is $\frac{7}{15}<\frac{1}{2}<\frac{9}{17}$. Choice 1.'])
    S('q-091', expl=[
        r'Complete each bracket to one: $1-\frac{1}{2}=\frac{1}{2}$, $1-\frac{1}{3}=\frac{2}{3}$, $1-\frac{1}{4}=\frac{3}{4}$.',
        r'Multiply and cancel: $\frac{1}{2}\cdot\frac{2}{3}\cdot\frac{3}{4}=\frac{1\cdot 2\cdot 3}{2\cdot 3\cdot 4}=\frac{1}{4}$. The 2s and the 3s cancel.',
        'Choice 1.'])
    S('q-092', stem=r'$4.5 \cdot 0.2 \div 30 = ?$', expl=[
        'Multiplication and division: left to right.',
        r'$4.5\cdot 0.2=0.9$',
        r'$0.9\div 30=\frac{0.9}{30}=\frac{9}{300}=\frac{3}{100}=0.03$',
        'Choice 1.'])
    S('q-093', stem=r'Given: P, Q, R and S are positive numbers. $\frac{S}{Q} \cdot \frac{P}{S} + \frac{R}{Q} = ?$', expl=[
        r"The product first. The S's cancel: $\frac{S}{Q}\cdot\frac{P}{S}=\frac{P}{Q}$.",
        r'Same bottom, add the tops: $\frac{P}{Q}+\frac{R}{Q}=\frac{P+R}{Q}$.',
        r'Check with $P=Q=R=S=1$: the expression is $1\cdot 1+1=2$, and choice 1 gives $\frac{1+1}{1}=2$. Choice 1.'])
    S('q-094', stem=r'Given: $X\ne 0$ and $Y\ne 0$. Which of the following expressions is not necessarily equal to $\frac{X}{Y}$?', expl=[
        r'Choice 1: $\frac{7X}{7Y}=\frac{X}{Y}$ (top and bottom times 7).',
        r'Choice 3: $X\cdot\frac{Y}{Y^2}=\frac{XY}{Y^2}=\frac{X}{Y}$ (top and bottom times Y).',
        r'Choice 4: $\frac{X^2}{Y\cdot X}=\frac{X}{Y}$ (top and bottom times X).',
        r'Choice 2 multiplies the top by X and the bottom by Y — two different factors. With $X=1$ and $Y=2$: $\frac{X}{Y}=\frac{1}{2}$, but $\frac{X^2}{Y^2}=\frac{1}{4}$. Not necessarily equal: choice 2.'])
    S('q-095', stem='Given:\n' + r'$\begin{cases} b>1 \\ a=\frac{b-0.25}{b-1} \end{cases}$' + '\nWhich of the following is necessarily true?', expl=[
        r'$b>1$, therefore the top $b-0.25$ and the bottom $b-1$ are both positive, and $a>0$. Choices 3 and 4 are out.',
        r'The top loses only 0.25. The bottom loses 1. Therefore the top is bigger than the bottom, and a positive fraction with a bigger top is more than 1: $a>1$.',
        r'Check with $b=2$: $a=\frac{2-0.25}{2-1}=1.75>1$. Choice 1.'])
    S('q-096', expl=[
        r'Plug in $x=1$, $y=2$ (then $\frac{x}{y}=\frac{1}{2}$). Choice 1: $2<1$ — false. Choice 3: $1\cdot 2=2\ne 1$ — false. Choices 2 and 4 survive.',
        r'Plug in a different kind of number: $x=-1$, $y=-2$ (again $\frac{x}{y}=\frac{1}{2}$). Choice 2: $-1<-2$ — false. Choice 4: $\frac{y}{x}=2>1$ — true.',
        r'Why choice 4 is always true: $\frac{x}{y}$ is positive, therefore $\frac{y}{x}$ is positive too. Flipping a positive fraction smaller than 1 gives a number bigger than 1: $0<\frac{x}{y}<1 \Rightarrow \frac{y}{x}>1$.',
        'Choice 4.'])
    S('q-097', expl=[
        r'All four numbers are positive. Same bottom $\sqrt{2}$: $\frac{7}{\sqrt{2}}>\frac{2}{\sqrt{2}}$. Same bottom $\sqrt{7}$: $\frac{7}{\sqrt{7}}>\frac{2}{\sqrt{7}}$.',
        r'Final: same top 7, the smaller bottom wins. $\sqrt{2}<\sqrt{7}$, therefore $\frac{7}{\sqrt{2}}>\frac{7}{\sqrt{7}}$.',
        r'Check by squaring (all positive): $\frac{4}{2}=2$, $\frac{49}{2}=24.5$, $\frac{4}{7}$, $\frac{49}{7}=7$. The largest is $\frac{7}{\sqrt{2}}$. Choice 2.'])
    S('q-098', expl=[
        r'Given $0<p<1<q$, all the bottoms are positive: $p+q>0$ and $q-p>0$.',
        r'Choices 1 and 2 have the same bottom, and the top $q+p$ is bigger than $q-p$. Choice 2 wins. Choice 2 is exactly 1.',
        r'Choices 3 and 4 have the same bottom $q-p$, and $q>p$. Choice 4 wins.',
        r'Choice 4: the top q is bigger than the bottom $q-p$. Therefore choice 4 is more than 1, and it beats choice 2.',
        r'Check with $p=\frac{1}{2}$, $q=\frac{3}{2}$: the choices are $\frac{1}{2}$, $1$, $\frac{1}{2}$, $\frac{3}{2}$. Choice 4.'])
    S('q-099', expl=[
        r'Make the tops equal to 60: $\frac{5}{26}=\frac{60}{312}$, $\frac{4}{21}=\frac{60}{315}$, $\frac{3}{16}=\frac{60}{320}$.',
        r'Same top: the smaller bottom wins. Therefore $\frac{3}{16}<\frac{4}{21}<\frac{5}{26}$.',
        r'Check by cross-multiplying: $3\cdot 21=63<64=4\cdot 16$ and $4\cdot 26=104<105=5\cdot 21$. Choice 1.'])
    # practice
    S('q-081', expl=[
        r'Top first: $\frac{1}{4}+\frac{1}{6}=\frac{3}{12}+\frac{2}{12}=\frac{5}{12}$.',
        r'Dividing by $\frac{25}{12}$ means multiplying by $\frac{12}{25}$: $\frac{5}{12}\cdot\frac{12}{25}=\frac{5}{25}=\frac{1}{5}$.',
        'Choice 2.'])
    S('q-082', expl=[
        r"Top: $\frac{a}{c}\cdot\frac{d}{a}=\frac{d}{c}$ (the a's cancel).",
        r"Bottom: $\frac{c}{b}\cdot\frac{a}{c}=\frac{a}{b}$ (the c's cancel).",
        r'Divide: $\frac{d}{c}\div\frac{a}{b}=\frac{d}{c}\cdot\frac{b}{a}=\frac{bd}{ac}$. Choice 2.'])
    S('q-083', expl=[
        r'The common denominator of 6, 4 and 3 is 12: $\frac{1}{6}=\frac{2}{12}$, $\frac{1}{4}=\frac{3}{12}$, $\frac{1}{3}=\frac{4}{12}$.',
        r'$\frac{2}{12}+\frac{3}{12}-\frac{4}{12}=\frac{1}{12}$. Choice 4.'])
    S('q-084', expl=[
        r'Each fraction is 1 minus a small piece: $\frac{6}{7}=1-\frac{1}{7}$, $\frac{7}{8}=1-\frac{1}{8}$, $\frac{8}{9}=1-\frac{1}{9}$, $\frac{9}{10}=1-\frac{1}{10}$.',
        r'The smallest missing piece is $\frac{1}{10}$. Therefore $\frac{9}{10}$ is the largest. Choice 4.'])
    S('q-085', expl=[
        'L gets smaller when M gets bigger. We need the largest M.',
        r'$\frac{2}{7}=\frac{8}{28}<\frac{9}{28}$, and $\frac{9}{28}<\frac{10}{28}=\frac{5}{14}$.',
        r'$\frac{5}{14}$ against $\frac{13}{35}$: cross-multiply, $5\cdot 35=175<182=14\cdot 13$. Therefore $\frac{13}{35}$ is bigger.',
        r'The largest M is $\frac{13}{35}$. Choice 4.'])
    S('q-086', expl=[
        r'Choice 1: $-1+\frac{7}{4}=-\frac{4}{4}+\frac{7}{4}=\frac{3}{4}$.',
        r'Choice 2: $2-\frac{5}{4}=\frac{8}{4}-\frac{5}{4}=\frac{3}{4}$.',
        r'Choice 3: $\frac{21}{28}=\frac{3}{4}$ (divide the top and the bottom by 7).',
        r'Choice 4: $\frac{3}{4}=\frac{12}{16}\ne\frac{9}{16}$. Choice 4 is not equal.'])
    S('q-087', stem=r'Given: m and n are different positive numbers, and $\frac{m}{n}$ is an integer. Which of the following is necessarily true?', expl=[
        r'm and n are positive and different. Therefore $\frac{m}{n}$ is a positive integer other than 1: $\frac{m}{n}\ge 2$.',
        r'Flip (both positive): $0<\frac{n}{m}\le\frac{1}{2}$. Choice 4 is always true, and choice 3 is always false.',
        r'Choice 1 fails for small numbers: $m=0.4$, $n=0.2$ gives $\frac{m}{n}=2$ and $m-n=0.2$, which is not more than 1.',
        r'Choice 2 fails for big numbers: $m=4$, $n=2$ gives $\frac{m}{n}=2$ and $m-n=2$, which is not between 0 and 1.',
        'Choice 4.'])
    S('q-088', stem='Given:\n' + r'$\begin{cases} a>1 \\ x\ne a \end{cases}$' + '\n' + r'For which of the following values of x will the value of $\frac{a+x}{a-x}$ be the smallest?',
      choices=[r'$x=1$', r'$x=\frac{2}{5}$', r'$x=-\frac{2}{5}$', r'$x=-\frac{4}{5}$'], expl=[
        r'All four values of x are at most 1, and $a>1$. Therefore the bottom $a-x$ is positive.',
        r'When x gets smaller, the top $a+x$ gets smaller and the bottom $a-x$ gets bigger. Both changes make the fraction smaller. Therefore the smallest x gives the smallest value: $x=-\frac{4}{5}$.',
        r'Check with $a=2$: $x=-\frac{4}{5}$ gives $\frac{1.2}{2.8}\approx 0.43$; $x=-\frac{2}{5}$ gives $\frac{1.6}{2.4}\approx 0.67$; $x=\frac{2}{5}$ gives $\frac{2.4}{1.6}=1.5$; $x=1$ gives $\frac{3}{1}=3$. Choice 4.'])
    S('q-089', expl=[
        r'Each number is 1 plus an extra: $\frac{7}{6}=1+\frac{1}{6}$, $\frac{9}{7}=1+\frac{2}{7}$, $\frac{19}{15}=1+\frac{4}{15}$, $\frac{19}{16}=1+\frac{3}{16}$.',
        r'Compare $\frac{1}{6}$ with the other extras by cross-multiplying: $7<12$, $15<24$, $16<18$. Therefore $\frac{1}{6}$ is the smallest extra.',
        r'The smallest number is $\frac{7}{6}$. Choice 1.'])
    S('q-090', expl=[
        r'All positive: cross-multiply pairs. $\frac{6}{50}$ against $\frac{4}{33}$: $6\cdot 33=198<200=50\cdot 4$. Therefore $\frac{6}{50}<\frac{4}{33}$.',
        r'$\frac{4}{33}$ against $\frac{5}{38}$: $4\cdot 38=152<165=33\cdot 5$. Therefore $\frac{4}{33}<\frac{5}{38}$.',
        r'The order is $\frac{6}{50}<\frac{4}{33}<\frac{5}{38}$. Choice 3. (Decimals: 0.12, about 0.121, about 0.132.)'])

    # Pass 2 (PLAN_REMOVE_RESTORE): the original extra items come back in their original form (stem, choices, key),
    # with the usual clean-up only (TeX, full numeric solutions).
    S('alg-extra-unit-t3-1-1', stem=r'Which is greater: $\frac{3}{7}$ or $\frac{5}{9}$?',
      choices=['The first fraction', 'They are equal', 'It depends on a missing value', 'The second fraction'], correct=4, expl=[
        r'Compare each fraction with one half: halve the bottom, then check the top.',
        r'$\frac{3}{7}$: half of 7 is 3.5, and $3<3.5$. Therefore $\frac{3}{7}<\frac{1}{2}$.',
        r'$\frac{5}{9}$: half of 9 is 4.5, and $5>4.5$. Therefore $\frac{5}{9}>\frac{1}{2}$.',
        r'Check by cross-multiplying: $3\cdot 9=27<35=7\cdot 5$. The second fraction is greater. Choice 4.'])
    S('alg-extra-unit-t3-1-2', stem='Which is largest?',
      choices=[r'$\frac{15}{16}$', r'$\frac{4}{5}$', r'$\frac{7}{8}$', r'$\frac{10}{11}$'], correct=1, expl=[
        r'Each fraction is 1 minus a small piece: $\frac{15}{16}=1-\frac{1}{16}$, $\frac{4}{5}=1-\frac{1}{5}$, $\frac{7}{8}=1-\frac{1}{8}$, $\frac{10}{11}=1-\frac{1}{11}$.',
        r'The smallest missing piece is $\frac{1}{16}$ (the biggest bottom). Therefore $\frac{15}{16}$ is the largest. Choice 1.'])
    S('alg-extra-unit-t3-1-3', stem=r'Given: $x>0$. Which is greater: $\frac{7}{x+2}$ or $\frac{7}{x+5}$?',
      choices=['They are equal', 'It cannot be determined from the information given.', 'The first fraction', 'The second fraction'], correct=3, expl=[
        r'$x>0$, therefore both bottoms are positive, and $x+2<x+5$.',
        r'Same top 7: the smaller bottom wins. Therefore $\frac{7}{x+2}>\frac{7}{x+5}$ for every $x>0$.',
        r'Check with $x=1$: $\frac{7}{3}\approx 2.33$ and $\frac{7}{6}\approx 1.17$. The first fraction is greater. Choice 3.'])
    S('alg-extra-unit-t3-1-4', stem=r'Which is greater: $\frac{3}{\sqrt{10}}$ or $\frac{2}{\sqrt{5}}$?',
      choices=['Neither is real', 'The first expression', 'The second expression', 'They are equal'], correct=2, expl=[
        'Both numbers are positive. Therefore we can square them and keep the order.',
        r'$\left(\frac{3}{\sqrt{10}}\right)^2=\frac{9}{10}$ and $\left(\frac{2}{\sqrt{5}}\right)^2=\frac{4}{5}=\frac{8}{10}$.',
        r'$\frac{9}{10}>\frac{8}{10}$, therefore $\frac{3}{\sqrt{10}}>\frac{2}{\sqrt{5}}$. The first expression is greater. Choice 2.'])
    S('alg-extra-unit-t3-1-5', stem=r'Given: $0<x<1$. Which of the following is the largest?', expl=[
        r'Plug in $x=\frac{1}{2}$: $x=\frac{1}{2}$, $x^2=\frac{1}{4}$, $\frac{1}{x}=2$. The largest is $\frac{1}{x}$.',
        r'The rule: for $0<x<1$, $x^2<x<1<\frac{1}{x}$. Choice 4.'])
    S('alg-extra-unit-t3-1-6', stem=r'Which is smaller: $\frac{3}{5}$ or $\frac{4}{6}$?',
      choices=['The first fraction', 'The second fraction', 'They are equal', 'It cannot be determined from the information given.'], correct=1, expl=[
        r'Both bottoms are positive. Cross-multiply: $6\cdot 3=18$ goes above $\frac{3}{5}$, and $5\cdot 4=20$ goes above $\frac{4}{6}$.',
        r'$18<20$, therefore $\frac{3}{5}<\frac{4}{6}$. Check with decimals: $0.6$ and about $0.67$.',
        'The first fraction is smaller. Choice 1.'])
    S('alg-extra-unit-t3-1-7', stem=r'Given: $c>1$. For which of the following values of x is the value of $\frac{c+x}{c-x}$ the smallest?',
      choices=[r'$-1$', r'$0$', r'$\frac{1}{2}$', r'$1$'], correct=1, expl=[
        r'All four values of x are at most 1, and $c>1$. Therefore the bottom $c-x$ is positive.',
        r'When x gets smaller, the top $c+x$ gets smaller and the bottom $c-x$ gets bigger. Both changes make the fraction smaller. Therefore the smallest x gives the smallest value: $x=-1$.',
        r'Check with $c=2$: $x=-1$ gives $\frac{1}{3}$; $x=0$ gives $1$; $x=\frac{1}{2}$ gives $\frac{2.5}{1.5}\approx 1.67$; $x=1$ gives $\frac{3}{1}=3$. Choice 1.'])


# ------------------------------------------------------------------ existing solution videos
def fix_solution_videos(M):
    # "so" meaning "therefore" mid-sentence -> new sentence, in all topic-3 videos
    for vid, v in M.D['videos'].items():
        if v['topic'] != TOPIC: continue
        for n, b in enumerate(v['beats'], 1):
            if any('say' in l and re.search(r'( —|,) so ', l['say']) for l in b['lines']):
                def fx(lines):
                    for l in lines:
                        if 'say' in l: l['say'] = re.sub(r'( —|,) so ', '. So ', l['say'])
                    return lines
                M.edit_lines(vid, n, fx)

    def say(vid, n, old, new):
        def fx(lines):
            for l in lines:
                if l.get('say') == old: l['say'] = new; return lines
            raise KeyError('%s #%d: %s' % (vid, n, old))
        M.edit_lines(vid, n, fx)

    def draw(vid, n, old, new):
        def fx(lines):
            for l in lines:
                if l.get('draw') == old: l['draw'] = new; return lines
            raise KeyError('%s #%d: %s' % (vid, n, old))
        M.edit_lines(vid, n, fx)

    draw('solve-q-092', 3, 'Write "0.9 : 30 = 0.03"', 'Write "0.9 ÷ 30 = 0.03"')
    say('solve-q-097', 3, 'Twenty-four and a half beats them all — and squaring keeps the order.',
        'Twenty-four and a half beats them all. All four numbers are positive, and for positive numbers squaring keeps the order.')
    say('solve-q-099', 4, 'Flipping reverses the order. Choice one, a third time.',
        'All three are positive — and flipping positive numbers reverses the order. Choice one, a third time.')
    # Q10: fourth method - the "pieces of 1/5" (mediant) idea
    M.insert_slides('solve-q-099', 4, [dict(title='Method 4 · Pieces of 1/5', mode='question', active=9, pre=[Q('q-099')], script=[
        "One more way — for strong students. Look at how the list is built.",
        D('Write "3/16 → 4/21 → 5/26: +1 on top, +5 on the bottom"'),
        "From three sixteenths to four twenty-firsts: one more on top, five more on the bottom. Then again.",
        "Each step mixes in a piece worth one fifth. Tops together, bottoms together — the result always lands between the two fractions.",
        D('Write "3/16 < 1/5 (15 < 16)"'),
        "Three sixteenths is less than one fifth: fifteen against sixteen.",
        "So every step pulls the fraction up toward one fifth.",
        D('Write "3/16 < 4/21 < 5/26 < 1/5" and circle choice 1'),
        "The list climbs. Choice one — a fourth time.",
    ])])


# ------------------------------------------------------------------ new guided questions (Q11-Q13)
SOLVE_SIDEBAR = ['Question %d' % k for k in range(1, 14)]


def guided(M, qid, stem, choices, correct, expl, intro, slides, after):
    M.new_q(qid, TOPIC, stem, choices, correct, expl)
    M.place_q(qid, LEARN, after=after)
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', title=title, active=n - 1, pre=[Q(qid)], script=script))
    M.new_video('solve-' + qid, TOPIC, 'Fraction Questions', SOLVE_SIDEBAR, beats, LEARN, kind='solution', qid=qid)
    return 'solve-' + qid


def add_guided(M):
    v = guided(M, 'q-r26-t03-01', r'Given: $a<0<b$. Which of the following is necessarily true?',
               [r'$\frac{1}{a}<\frac{1}{b}$', r'$\frac{1}{b}<\frac{1}{a}$', r'$a^2<b^2$', r'$\frac{b}{a}<\frac{a}{b}$'], 1, [
        r'$a<0<b$, therefore $\frac{1}{a}$ is negative and $\frac{1}{b}$ is positive. A negative number is less than a positive number: $\frac{1}{a}<\frac{1}{b}$ is always true.',
        r'Check the others with $a=-3$, $b=2$. Choice 2: $\frac{1}{2}<-\frac{1}{3}$ — false. Choice 3: $9<4$ — false. Choice 4: $-\frac{2}{3}<-\frac{3}{2}$ — false.',
        'Choice 1.'],
        ["Question eleven — medium-plus.", "Signs matter here. Look at them before you calculate."],
        [('Method 1 · Signs first', [
            "a is negative. b is positive.",
            "One over a negative number is negative. One over a positive number is positive.",
            D('Under 1/a write "−", under 1/b write "+"'),
            "Negative is always less than positive. Choice one is always true.",
            D('Circle choice 1'),
            "Choice two is the flip trap. Flipping reverses the order only when both numbers have the same sign. Here they don't.",
            "Choice three is the squaring trap. Squaring keeps the order only for positive numbers.",
            "Choice one."]),
         ('Method 2 · Plug in', [
            "Let's check with numbers. a is negative, b is positive: a is negative three, b is two.",
            D('Write "a = −3, b = 2"'),
            "Choice one: negative one third, less than one half. True.",
            "Choice two: one half, less than negative one third? No.",
            D('Cross out choice 2'),
            "Choice three: nine, less than four? No.",
            D('Cross out choice 3'),
            "Choice four: b over a is negative two thirds. a over b is negative three halves.",
            "Is negative two thirds less than negative three halves? No — it's closer to zero. It's bigger.",
            D('Cross out choice 4 and circle choice 1'),
            "One pair of numbers, three choices out. Choice one."])],
        after='solve-q-099')

    v = guided(M, 'q-r26-t03-02', r'Given: $0<a<b$. Which of the following is the largest?',
               [r'$\frac{a}{b}$', r'$\frac{a+1}{b+1}$', r'$\frac{a+5}{b+5}$', r'$\frac{5a}{5b}$'], 3, [
        r'$0<a<b$, therefore $\frac{a}{b}$ is a positive fraction less than 1.',
        r'Choice 4: $\frac{5a}{5b}=\frac{a}{b}$. Multiplying the top and the bottom by 5 does not change the value.',
        r'Adding the same positive number to the top and the bottom of a positive fraction below 1 moves it toward 1: it gets bigger. $\frac{a+5}{b+5}$ is $\frac{a+1}{b+1}$ with 4 more added to the top and the bottom, therefore it is bigger still.',
        r'Check with $a=1$, $b=2$: $\frac{1}{2}$, $\frac{2}{3}$, $\frac{6}{7}$, $\frac{1}{2}$. Choice 3.'],
        ["Question twelve — medium.", "One fraction, four makeovers. Which one grows the most?"],
        [('Method 1 · Toward 1', [
            "a is smaller than b, and both are positive. So a over b is a fraction below one.",
            "Choice four first: five a over five b. Times five, top and bottom — that's just expanding.",
            D('Next to choices 1 and 4 write "= a/b"'),
            "Choices one and four are equal. There's only one largest — so neither of them can be it.",
            D('Cross out choices 1 and 4'),
            "Choices two and three add the same number to the top and the bottom. Below one, that moves the fraction toward one. It grows.",
            "Adding five is adding one — and then four more. More steps toward one.",
            D('Circle choice 3'),
            "Choice three."]),
         ('Method 2 · Plug in', [
            "Plug in: a is one, b is two. Legal — a is smaller than b.",
            D('Next to the choices write: 1/2, 2/3, 6/7, 1/2'),
            "One half. Two thirds. Six sevenths. One half.",
            D('Circle choice 3'),
            "Six sevenths is the biggest. Choice three."])],
        after=v)

    guided(M, 'q-r26-t03-03', r'Given: $0<x<1$. Which of the following is correct?',
           [r'$x^2<x<\sqrt{x}<\frac{1}{x}$', r'$x<x^2<\sqrt{x}<\frac{1}{x}$', r'$\sqrt{x}<x<x^2<\frac{1}{x}$', r'$\frac{1}{x}<\sqrt{x}<x<x^2$'], 1, [
        r'Plug in a number from the range with an easy root: $x=\frac{1}{4}$.',
        r'$x^2=\frac{1}{16}$, $x=\frac{1}{4}$, $\sqrt{x}=\frac{1}{2}$, $\frac{1}{x}=4$.',
        r'Therefore $x^2<x<\sqrt{x}<\frac{1}{x}$. Choice 1.',
        r'Choice 4 is the order for $x>1$ — a trap.'],
        ["Question thirteen — medium.", "The x-range table — in a real question."],
        [('Method 1 · Plug in', [
            "x is between zero and one. Pick a number with an easy root: one quarter.",
            D('Write "x = 1/4"'),
            "x squared: one sixteenth. Root x: one half. One over x: four.",
            D('Write "1/16 < 1/4 < 1/2 < 4"'),
            "Smallest to biggest: x squared, x, root x, one over x.",
            D('Circle choice 1'),
            "Choice one.",
            "Why one quarter and not one half? The root of one half is not a nice number. Choose numbers that make the work easy."]),
         ('Method 2 · Know the table', [
            "Or just know the table. Between zero and one, squaring makes a number smaller, and the root makes it bigger.",
            "And one over x is bigger than one.",
            "Choice four is the order for x bigger than one. It's the trap for students who memorize without the range.",
            D('Cross out choice 4'),
            "Choice one."])],
        after='solve-q-r26-t03-02')

    # every Topic-3 solution video shows the same sidebar (Question 1-13)
    for vid, vv in M.D['videos'].items():
        if vv['topic'] == TOPIC and vv.get('kind') == 'solution':
            M.set_sidebar(vid, SOLVE_SIDEBAR)


# ------------------------------------------------------------------ new practice questions
def add_practice(M):
    P = lambda qid, *a: (M.new_q(qid, TOPIC, *a), M.place_q(qid, PRACTICE))
    P('q-r26-t03-04', r'Given: $x>0$. Which of the following is necessarily true?',
      [r'$\frac{7+x}{9+x}<\frac{7}{9}$', r'$\frac{7}{9}<\frac{7+x}{9+x}<1$', r'$\frac{7+x}{9+x}=\frac{7}{9}$', r'$1<\frac{7+x}{9+x}$'], 2, [
        r'$\frac{7}{9}$ is below 1. Adding the same positive number x to the top and the bottom moves it toward 1: it gets bigger.',
        r'It stays below 1, because the top $7+x$ is still smaller than the bottom $9+x$.',
        r'Check with $x=1$: $\frac{8}{10}=0.8$, and $\frac{7}{9}\approx 0.78$. Therefore $\frac{7}{9}<0.8<1$. Choice 2.'])
    P('q-r26-t03-05', r'Given: $x>1$. Which of the following is the smallest?',
      [r'$\frac{1}{\sqrt{x}}$', r'$\frac{1}{x}$', r'$\sqrt{x}$', r'$\frac{1}{x^2}$'], 4, [
        r'Plug in $x=4$: $\frac{1}{\sqrt{4}}=\frac{1}{2}$, $\frac{1}{4}$, $\sqrt{4}=2$, $\frac{1}{16}$.',
        r'The smallest is $\frac{1}{16}=\frac{1}{x^2}$. Choice 4.',
        r'The rule: for $x>1$, $\sqrt{x}<x<x^2$. Flipping positive numbers reverses the order: $\frac{1}{x^2}<\frac{1}{x}<\frac{1}{\sqrt{x}}$.'])
    P('q-r26-t03-06', r'Given: $a<b<0$. Which of the following is necessarily true?',
      [r'$\frac{1}{a}<\frac{1}{b}$', r'$\frac{1}{b}<\frac{1}{a}$', r'$a^2<b^2$', r'$\frac{a}{b}<1$'], 2, [
        r'Plug in $a=-3$, $b=-2$.',
        r'Choice 1: $-\frac{1}{3}<-\frac{1}{2}$ — false ($-\frac{1}{3}$ is closer to 0). Choice 2: $-\frac{1}{2}<-\frac{1}{3}$ — true.',
        r'Choice 3: $9<4$ — false. Choice 4: $\frac{-3}{-2}=\frac{3}{2}<1$ — false.',
        'Why choice 2 is always true: a and b have the same sign, and flipping two numbers with the same sign reverses their order. Choice 2.'])
    P('q-r26-t03-07', 'Which of the following numbers is the largest?',
      [r'$\frac{5}{-8}$', r'$-\frac{7}{12}$', r'$\frac{3}{-4}$', r'$-\frac{2}{3}$'], 2, [
        r'Move each minus to the top. All four numbers are negative: $-\frac{5}{8}$, $-\frac{7}{12}$, $-\frac{3}{4}$, $-\frac{2}{3}$.',
        'Among negative numbers, the largest is the one closest to 0: the one that is smallest without the minus.',
        r'Without the minus: $\frac{7}{12}\approx 0.58$, $\frac{5}{8}=0.625$, $\frac{2}{3}\approx 0.67$, $\frac{3}{4}=0.75$. The smallest is $\frac{7}{12}$ (check: $7\cdot 8=56<60=12\cdot 5$).',
        r'The largest number is $-\frac{7}{12}$. Choice 2.'])
    P('q-r26-t03-08', 'Given:\n' + r'$\begin{cases} b<0<d \\ \frac{a}{b}<\frac{c}{d} \end{cases}$' + '\nWhich of the following is necessarily true?',
      [r'$ad<bc$', r'$ad>bc$', r'$a<c$', r'$a>c$'], 2, [
        r'Plug in legal values: $a=1$, $b=-1$, $c=1$, $d=1$. Check the condition: $\frac{1}{-1}=-1<1=\frac{1}{1}$.',
        r'Choice 1: $ad=1$ and $bc=-1$, and $1<-1$ is false. Choice 3: $1<1$ — false. Choice 4: $1>1$ — false. Only choice 2 survives.',
        r'Why: one bottom is negative. With one negative bottom, the cross products point the wrong way (the trap from the lesson): $\frac{a}{b}<\frac{c}{d}$ gives $ad>bc$.',
        'Choice 2.'])

    # Pass 2: the fixers' new versions of t3-1-2, -4 and -7 test kept methods -> they stay under new ids
    P('q-r26-t03-09', 'Which of the following numbers is the smallest?',
      [r'$\frac{22}{20}$', r'$\frac{24}{22}$', r'$\frac{21}{19}$', r'$\frac{23}{21}$'], 2, [
        r'All four are above 1. Each one is the one before it with 1 added to the top and to the bottom: $\frac{21}{19}\to\frac{22}{20}\to\frac{23}{21}\to\frac{24}{22}$.',
        'Above 1, adding the same positive number to the top and the bottom moves the fraction down toward 1.',
        r'Or compare the extras: $1+\frac{2}{19}$, $1+\frac{2}{20}$, $1+\frac{2}{21}$, $1+\frac{2}{22}$. Same top 2: the biggest bottom gives the smallest extra.',
        r'The smallest is $\frac{24}{22}$. Choice 2.'])
    P('q-r26-t03-10', 'Which of the following numbers is the largest?',
      [r'$\frac{3}{\sqrt{2}}$', r'$\frac{4}{\sqrt{3}}$', r'$\frac{5}{\sqrt{5}}$', r'$\frac{6}{\sqrt{7}}$'], 2, [
        'All four numbers are positive. Therefore we can square them and keep the order.',
        r'$\frac{9}{2}=4.5$, $\frac{16}{3}\approx 5.33$, $\frac{25}{5}=5$, $\frac{36}{7}\approx 5.14$.',
        r'The largest square is $\frac{16}{3}$. Therefore the largest number is $\frac{4}{\sqrt{3}}$. Choice 2.'])
    P('q-r26-t03-11', r'Given: $-1<x<0$. Which of the following is the largest?',
      [r'$x$', r'$x^2$', r'$x^3$', r'$\frac{1}{x}$'], 2, [
        r'Plug in $x=-\frac{1}{2}$: $x=-\frac{1}{2}$, $x^2=\frac{1}{4}$, $x^3=-\frac{1}{8}$, $\frac{1}{x}=-2$.',
        r'$x^2$ is the only positive one. Choice 2.',
        r'The rule: for $-1<x<0$, $\frac{1}{x}<x<x^3<0<x^2$.'])

    M.practice_order(PRACTICE, [
        'q-083', 'q-086', 'q-081', 'q-082',                               # fraction operations (review)
        'alg-extra-unit-t3-1-6', 'alg-extra-unit-t3-1-1', 'q-084', 'alg-extra-unit-t3-1-2', 'alg-extra-unit-t3-1-3',
        'q-085', 'q-089', 'alg-extra-unit-t3-1-5', 'alg-extra-unit-t3-1-4', 'q-r26-t03-05', 'q-r26-t03-07',
        'q-r26-t03-09', 'q-r26-t03-10', 'q-090', 'q-r26-t03-04',
        'q-r26-t03-11', 'alg-extra-unit-t3-1-7', 'q-087', 'q-088', 'q-r26-t03-06', 'q-r26-t03-08'])


# ------------------------------------------------------------------ Pass 2: summary video before the practice
def add_summary(M):
    sb = ['Cross-multiply', 'Signs first', 'Quick shortcuts', 'Distance from 1', 'Add to top and bottom',
          'Square or flip', 'x by range', 'Plug in numbers', 'Before you practice']
    C = lambda i, title, script: dict(title=title, mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice, let's review the whole topic in two minutes.",
            'Every method, every trap. Short and fast.']),
        C(0, 'Cross-multiply', [
            'Method number one: cross-multiply.',
            A('4/7 ? 6/11 with the products', T(r'$\frac{4}{7}\;?\;\frac{6}{11}\qquad 11\cdot 4=44 \;>\; 42=7\cdot 6$', size=50)),
            'Each product goes above ITS numerator. Forty-four against forty-two: four sevenths is bigger.',
            A('The condition appears', T('Condition: both bottoms positive', size=42)),
            'One condition: both bottoms must be positive.']),
        C(1, 'Signs first', [
            'Signs first. Always.',
            A('Negative < positive', T(r'negative $<$ positive: $\frac{2}{-5}<\frac{1}{6}$', size=46)),
            'A negative number is smaller than any positive number. No calculation needed.',
            A('Move the minus to the top', T(r'A negative bottom? $\frac{2}{-5}=-\frac{2}{5}$', size=46)),
            'A negative bottom? Move the minus to the top. Then cross-multiply.',
            A('Two negatives', T(r'$\frac{5}{6}<\frac{6}{7}\;\Rightarrow\;-\frac{5}{6}>-\frac{6}{7}$', size=46)),
            'Two negatives? Compare them without the minus, then reverse.']),
        C(2, 'Quick shortcuts', [
            'Sometimes the numbers invite a shortcut.',
            A('Benchmark 1/2', T(r'Benchmark $\frac{1}{2}$: $\frac{4}{9}<\frac{1}{2}<\frac{7}{13}$', size=44)),
            'Halve the bottom, then check the top.',
            A('Same top or bottom', T(r'Same bottom: bigger top wins. Same top: $\frac{9}{14}<\frac{9}{11}$', size=40)),
            'Same bottom: the bigger top wins. Same top: the SMALLER bottom wins.',
            A('Make them match', T(r'Make them match: $\frac{3}{7}=\frac{12}{28}>\frac{12}{29}$', size=44)),
            'No match? Expand one fraction until they match.',
            A('Decimals to know', T(r'$\frac{1}{4}=0.25\quad \frac{1}{8}=0.125\quad \frac{1}{3}\approx 0.33\quad \frac{1}{7}\approx 0.14$', size=40)),
            'And know the basic decimals by heart.']),
        C(3, 'Distance from 1', [
            'Both fractions close to one? Look at what is missing.',
            A('Below 1', T(r'$\frac{12}{13}=1-\frac{1}{13}\;<\;1-\frac{1}{15}=\frac{14}{15}$', size=48)),
            'The smaller missing piece wins. Fourteen fifteenths is bigger.',
            A('Above 1', T(r'$\frac{9}{8}=1+\frac{1}{8}\;<\;1+\frac{2}{13}=\frac{15}{13}$', size=48)),
            'Above one, compare the extras. The bigger extra wins.']),
        C(4, 'Add to top and bottom', [
            'Add the same positive number to the top and the bottom. The fraction moves toward one.',
            A('Below 1', T(r'Below 1: $\frac{3}{10}<\frac{4}{11}<\frac{5}{12}$ (it grows)', size=46)),
            'Below one, it grows.',
            A('Above 1', T(r'Above 1: $\frac{11}{7}>\frac{12}{8}$ (it shrinks)', size=46)),
            'Above one, it shrinks. Positive numbers only.']),
        C(5, 'Square or flip', [
            'Two more tools, and each one has a sign condition.',
            A('Square', T(r'Roots? Square: $\frac{3}{\sqrt{13}}>\frac{2}{\sqrt{6}}$ because $\frac{9}{13}>\frac{4}{6}$', size=42)),
            'Roots in the fractions? Square them. Only when both numbers are positive.',
            A('Flip', T(r'Flip: $\frac{17}{5}>\frac{10}{3}\;\Rightarrow\;\frac{5}{17}<\frac{3}{10}$', size=42)),
            'Flipping reverses the order. Only when both numbers have the same sign.']),
        C(6, 'x by range', [
            'x, x squared, root x, one over x: the order depends on the range.',
            A('0 < x < 1', T(r'$0<x<1:\quad x^2<x<\sqrt{x}<1<\frac{1}{x}$', size=46)),
            'Between zero and one, squaring makes a number smaller.',
            A('x > 1', T(r'$x>1:\quad \frac{1}{x}<1<\sqrt{x}<x<x^2$', size=46)),
            'Above one, the order flips.',
            A('−1 < x < 0', T(r'$-1<x<0:\quad \frac{1}{x}<x<0<x^2$', size=46)),
            'Not sure? Plug in one number from the range: one quarter, four, or negative one half.']),
        C(7, 'Plug in numbers', [
            'Letters in the question? Plug in numbers.',
            A('Rule 1', T('Legal values only — check every condition', size=42)),
            A('Rule 2', T('Avoid 0 and 1', size=42)),
            A('Rule 3', T('Two choices survive? Try a negative or a fraction', size=42)),
            'Legal values only. Avoid zero and one. Two choices survive? Plug in a different kind of number.',
            A('Necessarily / could be', T('"Necessarily": every legal value · "Could be": one example', size=40)),
            '"Necessarily true" must work for every legal value. One counterexample kills a choice.']),
        C(8, 'Before you practice', [
            'Before you practice, always ask yourself:',
            A('Check 1', T('1. What are the signs? Negative or positive?', size=42)),
            A('Check 2', T('2. Are both bottoms positive before I cross-multiply?', size=42)),
            A('Check 3', T('3. Do the numbers invite a shortcut?', size=42)),
            A('Check 4', T('4. With letters: which numbers are legal?', size=42)),
            'And watch the traps: a product written under the wrong fraction, squaring negatives, flipping numbers with different signs.',
            'You know all of this. Go practice.']),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    M.new_video('r26-t03-summary', TOPIC, 'Comparing Fractions: Summary', sb, slides, LEARN, after=last)


def apply(M):
    fix_lesson(M)
    fix_card(M)
    fix_questions(M)
    fix_solution_videos(M)
    add_guided(M)
    add_practice(M)
    add_summary(M)
