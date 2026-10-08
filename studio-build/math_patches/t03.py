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
          'Flip them', 'Recap']
    M.set_sidebar(V, sb)
    for n in range(2, len(M.video(V)['beats']) + 1):
        M.slide(V, n)['active'] = n - 2
    # teacher 2026-10-02: "Plug in numbers" stays exactly as in the original (Hebrew) lesson - one worked example;
    # the general plug-in rules belong to topic 1 (Test numbers), topic 5 and topic 51, not here
    pb = next(b for b in M.video(V)['beats'] if b['title'] == 'Plug in numbers')
    if len(pb['items']) == 3 and 'LEGAL' in pb['items'][2]['t']:
        pb['items'].pop(2)
        pb['lines'] = [l for l in pb['lines'] if l.get('appear') != 2 and not (l.get('say') or '').startswith('On a real question')]
    assert len(M.video(V)['beats']) == 14


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
            ['Plug in numbers', 'letters: pick legal values and compare the numbers', r'$x$ a fraction, $y>1$: try $x=\frac12$, $y=2$'],
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
    """2026-10-02 (teacher): a review of the MAIN ideas of the whole fractions unit (topics 2 and 3) before the mixed
    practice. The basics (r26-t02-summary) are not repeated. One rule + one mini example (fresh numbers) per concept."""
    # trimmed (teacher: "a bit long — take off what is not so used in the exam"): kept what the real exams use most —
    # signs / flipping with the same sign, x by range, plug-in with legal values, letters in fractions, quick comparing;
    # dropped telescoping chains, squaring roots, add-to-top-and-bottom and the many-fractions tournament (rare on the exam)
    sb = ['Cross-multiply', 'Quick shortcuts', 'Letters in fractions', 'Ranges and signs', 'Plug in numbers',
          'Before you practice']
    C = lambda i, title, script: dict(title=title, mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Fractions: Summary', script=[
            "We've finished fractions. Before the mixed practice, a short review.",
            'The basic moves you already reviewed. Now: what the exam asks most, with one quick example each.']),
        C(0, 'Cross-multiply, signs first', [
            A('Cross-multiply', T(r'$\frac{4}{9}\;?\;\frac{3}{7}\qquad 7\cdot 4=28\;>\;27=9\cdot 3\quad\Rightarrow\quad\frac{4}{9}>\frac{3}{7}$', size=44)),
            'Our main method: cross-multiply. Each product goes above ITS fraction. Both bottoms must be positive.',
            A('Signs first', T(r'Signs first: $\frac{4}{-9}\;?\;-\frac{3}{7}\quad\Rightarrow\quad -\frac{4}{9}<-\frac{3}{7}$ (reverse)', size=42)),
            'Negative bottom? Move the minus to the top. Two negatives? Compare without the minus, then reverse.',
            A('Flip: same sign only', T(r'Flip: $\frac{4}{17}<\frac{5}{21}$ because $\frac{17}{4}>\frac{21}{5}$ — same sign only', size=40)),
            'Flipping reverses the order. Only when both numbers have the same sign.']),
        C(1, 'Quick shortcuts', [
            'Sometimes the numbers invite a shortcut.',
            A('Benchmark 1/2', T(r'Benchmark $\frac{1}{2}$: $\frac{6}{13}<\frac{1}{2}<\frac{10}{19}$', size=42)),
            'One below a half, one above. Done.',
            A('Same top', T(r'Same top: $\frac{4}{7}=\frac{8}{14}>\frac{8}{15}$', size=42)),
            'Same top? The smaller bottom wins.']),
        C(2, 'Letters in fractions', [
            A('Cancel, then add the tops', T(r'$\frac{a}{c}\cdot\frac{b}{a}+\frac{d}{c}=\frac{b+d}{c}$', size=44)),
            'Letters cancel just like numbers. Same bottom: add the tops.',
            A('Not necessarily equal', T(r'$\frac{x}{y}=\frac{4x}{4y}$ ✓ $\qquad \frac{x^2}{y^2}$, $\frac{x+4}{y+4}$ ✗', size=42)),
            'The same factor on top and bottom keeps the value. Squaring, or adding to both, does not.']),
        C(3, 'Ranges and signs', [
            A('x by range', T(r'$0<x<1:\quad x^2<x<1<\frac{1}{x}$', size=44)),
            'Between zero and one, squaring makes a number smaller, and one over x is bigger than one.',
            A('Between 0 and 1', T(r'$0<\frac{p}{q}<1$: same sign, $q$ farther from 0', size=42)),
            'A fraction between zero and one: same sign, and the bottom is farther from zero.',
            A('Negatives', T(r'$p=-2,\ q=-5$: $\;\frac{p}{q}=\frac{2}{5}$, but $q<p$', size=40)),
            'Careful: with two negatives, the bottom is the SMALLER number.']),
        C(4, 'Plug in numbers', [
            'Letters in the question? You can always plug in numbers.',
            A('Legal values', T(r'$0<x<1$: try $x=\frac{1}{3}$ $\quad$ $-1<x<0$: try $x=-\frac{1}{2}$', size=42)),
            'Only legal values — the range decides. Three out, mark the fourth.',
            'Two choices survive? Plug in again, with a different kind of number.']),
        C(5, 'Before you practice', [
            'Before you practice, ask yourself:',
            A('Check 1', T('1. Signs first: negative or positive?', size=42)),
            A('Check 2', T('2. Both bottoms positive before I cross-multiply?', size=42)),
            A('Check 3', T('3. With letters: which values are legal?', size=42)),
            'That is the whole unit. You know this. Go practice.']),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == LEARN][-1]
    M.new_video('r26-t03-summary', TOPIC, 'Fractions: Summary', sb, slides, LEARN, after=last)


# ------------------------------------------------------------------ 2026-10-02: Hebrew check of the solution videos
# Every method, step and tip of the teacher's original (Hebrew) sample-question videos must also be in the English
# solution videos. Only what was missing is added here; everything else stays as it is.
def hebrew_check(M):
    def edit(vid, n, *ops):
        s = script_of(M, vid, n)
        for op, old, new in ops:
            s = replace_line(s, old, new) if op == 'rep' else insert_after(s, old, new)
        M.set_slide(vid, n, script=s)

    # (1 - 1/2)(1 - 1/3)(1 - 1/4): the long way first, "shortcut one / shortcut two", how fractions multiply
    edit('solve-q-091', 2,
         ('ins', 'Three brackets, each one minus a fraction.', [
             'The long way: a common denominator. One is three thirds. Three thirds minus one third — two thirds.',
             "That works. But on the exam we need speed."]),
         ('rep', "Don't hunt for common denominators. Complete to one in your head.",
          'Shortcut one: complete to one, in your head. No common denominators.'),
         ('rep', 'Now multiply — but cancel first.', [
             'Now multiply. Fractions multiply top times top, bottom times bottom.',
             "But don't multiply yet. Shortcut two: cancel first."]))

    # 4.5 · 0.2 ÷ 30: decimal places and "a bottom of 100" spelled out, as in the original
    edit('solve-q-092', 2,
         ('rep', 'Four point five is nine halves. Zero point two is two tenths — one fifth.', [
             'Four point five is four and a half — nine halves.',
             'Zero point two: one place after the point — two tenths. That is one fifth.']),
         ('rep', 'The choices are decimals, so: zero point zero three. Choice one.', [
             'The choices are decimals. To turn a fraction into a decimal, make the bottom one hundred.',
             'Ours already is: three hundredths. Two places after the point — zero point zero three. Choice one.']))
    edit('solve-q-092', 3,
         ('rep', 'Ignore the points: forty-five times two, ninety. Two decimal places in total — zero point nine zero. Zero point nine.', [
             'Ignore the points: forty-five times two is ninety.',
             'Now count the places after the point: one in four point five, one in zero point two. Two in total.',
             'Ninety with two places: zero point nine zero. Zero point nine.']))

    # P, Q, R, S: why the choices are checked first; which way is recommended
    edit('solve-q-093', 3,
         ('ins', 'But first check that the choices come out DIFFERENT with those values.', [
             'Why the choices first? If two choices gave the same number, one plug-in could not decide between them.']),
         ('ins', 'Two — choice one.', [
             'Two ways. But here the recommended one is the math: cancel, then add.',
             'Plugging in is for practice, or for a moment of panic. Make sure you master these basics.']))

    # X/Y: "equal only if X = Y", cancel if you don't see the expansion, which way to choose
    edit('solve-q-094', 2,
         ('ins', "Choice two: the top gets multiplied by X, the bottom by Y. Two DIFFERENT factors. That's not expanding.", [
             'Could it still be equal? Only if X equals Y. Possible — but not necessarily.']),
         ('ins', 'Choice three: X times Y over Y squared — top and bottom both times Y. Equal.', [
             "Don't see it? Cancel one Y from the top and the bottom. X over Y."]))
    edit('solve-q-094', 3,
         ('ins', "They asked for the one that's NOT necessarily equal — and we just found it fail. Choice two.", [
             "Which way is better? Both are good. Use the one you're comfortable with."]))

    # a = (b - 0.25)/(b - 1): the plug-in goes choice by choice and eliminates three; which way is better
    s = script_of(M, 'solve-q-095', 3)
    s = replace_line(s, 'Cross out choices 2, 3 and 4; circle choice 1', [
        'Choice one: is one point seven five more than one? Yes. We cannot cross it out.',
        'Choice two: between zero and one? No — it is more than one. Out.',
        D('Cross out choice 2'),
        'Choices three and four: negative? No. Out.',
        D('Cross out choices 3 and 4; circle choice 1')])
    s = replace_line(s, 'Not between zero and one. Not negative. Only choice one survives.', [
        'Three choices are out. Only choice one survives.',
        'Which way is better? Understanding the top and the bottom is important. But plugging in is an excellent way too.'])
    M.set_slide('solve-q-095', 3, script=s)

    # 0 < x/y < 1: why plug in first, WHICH second plug-in (not 2 and 3 again), number line, choice 3 in method 2
    s = script_of(M, 'solve-q-096', 2)
    s = ['Two ways: plugging in, or understanding. The understanding here is a bit harder. So we start with plugging in.'] + s
    s = insert_after(s, "Two choices survive. Don't guess! We need another substitution — a DIFFERENT kind of number.", [
        'But which one? Two and three? Three and four? One and three?',
        "They won't help. They are all positive — the same case we already tested."])
    s = insert_after(s, "Choice two: is negative one less than negative two? No — negative one is closer to zero. So it's bigger. Out.", [
        'Remember: with negative numbers, the closer to zero, the bigger.',
        'Choice four: negative two over negative one is two. More than one again.'])
    M.set_slide('solve-q-096', 2, script=s)
    edit('solve-q-096', 3,
         ('ins', 'Either way, the bottom is bigger in absolute value — further from zero than the top.', [
             D('Draw a number line with 0 in the middle: on the right mark x, then y; on the left mark y, then x'),
             'On a number line: if both are positive, y is to the right of x. If both are negative, y is to the left of x — like negative two and negative one.']),
         ('ins', 'That\'s why "x is less than y" only works when they\'re positive, and "y is less than x" only when they\'re negative. Possible — not necessary.', [
             'And x times y equals one? Our first plug-in gave two. Not necessarily true.']))

    # largest of four: why a tournament, three comparisons; squaring needs no exact values; which way
    edit('solve-q-097', 2,
         ('rep', "Four fractions to compare. Let's run a tournament: two semi-finals, then a final.", [
             'In the lesson we compared two fractions. Here there are four. What do we do?',
             'Run a tournament. Find pairs that are easy to compare — here, pairs with the same bottom.',
             'Two semi-finals, then a final. Three comparisons, and we have the answer.']))
    edit('solve-q-097', 3,
         ('ins', 'Two squared over two: two. Forty-nine over two: twenty-four and a half. Four sevenths: under one. Forty-nine over seven: seven.', [
             'No need for exact values. We only need to see which one is the biggest.']))
    edit('solve-q-097', 4,
         ('ins', 'Third approach — understanding. A fraction is biggest with the biggest top and the smallest bottom.', [
             'Here the tops repeat — two and seven. The bottoms repeat too — root two and root seven.']),
         ('ins', 'Choice two. Three seconds.', [
             'Three ways. Which one is best? Pick the one that feels comfortable.']))

    # 0 < p < 1 < q: tops positive too, "order doesn't matter in addition", why not q = 2
    edit('solve-q-098', 2,
         ('ins', 'Semi-final one: choices one and two share the bottom — p plus q, which is positive.', [
             'The tops are positive too: q is bigger than p, therefore q minus p is positive.']),
         ('rep', 'The final. Different tops, different bottoms. Look closer.', [
             'The final. Different tops, different bottoms. Now what?',
             'Open your eyes and look closer.']),
         ('ins', 'Choice two: q plus p over p plus q. The same thing on top and bottom — exactly one.', [
             'Order does not matter when you add: q plus p equals p plus q.',
             'Now: is choice four bigger or smaller than one?']))
    edit('solve-q-098', 3,
         ('rep', 'Plug-in version. p has to be a fraction — take one half.', [
             'Second way: plug in. Letters in the question? You can always plug in numbers.',
             'p has to be a fraction between zero and one. Take one half — the easiest fraction.']),
         ('rep', 'For q, choose smart: one and a half. Plus or minus a half, it gives whole numbers.', [
             'For q, we would usually take a whole number, like two.',
             'But every choice adds p to q, or subtracts p from q. Two plus a half is two and a half — messy.',
             'Choose smart: one and a half. Plus or minus a half, it gives whole numbers.']),
         ('ins', 'One and a half is the biggest. Choice four.', ['Two ways — both excellent.']))

    # 3/16, 4/21, 5/26: the full order is asked; why a common bottom is out; cross-multiplying needs only two checks
    edit('solve-q-099', 2,
         ('rep', 'Big, awkward bottoms. But look at the tops: five, four, three. Tiny.', [
             'Careful: they want the full order — biggest, middle and smallest. Not just the biggest.',
             'The basic way is a common bottom. But for sixteen, twenty-one and twenty-six it runs into the thousands.',
             'No calculator on the exam. That way is off the table.',
             'But look at the tops: five, four, three. Tiny.']))
    edit('solve-q-099', 3,
         ('rep', "Cross-multiplication works too. Don't compare every pair — take two fractions, then use the choices.", [
             'Cross-multiplication works too. But comparing every pair takes three comparisons.',
             'Smarter: compare any two fractions, then use the choices. Two comparisons may be enough.']))


# ------------------------------------------------------------------ 2026-10-02: new numbers (not identical to the Hebrew course)
# Teacher: "the same concept but with different numbers". Every question taken from the Hebrew course (study guide q-081 ..
# q-099) gets new numbers; the guided ones also differ from the Hebrew sample-question videos. Same method(s), same trap,
# same difficulty, same answer type. The solution videos keep every slide and teaching step - only the numbers change.
def new_numbers(M):
    # already RECORDED by the teacher with the old numbers (2026-10-02) - question and video stay exactly as recorded
    RECORDED = {'q-091', 'q-092', 'q-093', 'q-094'}

    def S(qid, **kw):
        if qid not in RECORDED: M.set_q(qid, **kw)

    def video(qid, slides):
        if qid in RECORDED: return
        vid = 'solve-' + qid
        for n, x in slides.items():
            title, script = x if isinstance(x, tuple) else (None, x)
            M.set_slide(vid, n, title=title, script=script)
        q, v = M.q(qid), M.video(vid)
        v['title'] = ' %s ' % q['stem'].strip(); v['navLabel'] = q['navLabel']

    # ---------------- guided questions + their solution videos
    # Q2 telescoping product. Study guide (1-1/2)(1-1/3)(1-1/4) = 1/4; Hebrew video (1-1/3)(1-1/4)(1-1/5) = 2/5
    S('q-091', stem=r'$\left(1 - \frac{1}{4}\right)\left(1 - \frac{1}{5}\right)\left(1 - \frac{1}{6}\right) = ?$',
      choices=[r'$\frac{1}{2}$', r'$\frac{1}{3}$', r'$\frac{3}{4}$', r'$\frac{5}{6}$'], correct=1, expl=[
        r'Complete each bracket to one: $1-\frac{1}{4}=\frac{3}{4}$, $1-\frac{1}{5}=\frac{4}{5}$, $1-\frac{1}{6}=\frac{5}{6}$.',
        r'Multiply and cancel: $\frac{3}{4}\cdot\frac{4}{5}\cdot\frac{5}{6}=\frac{3\cdot 4\cdot 5}{4\cdot 5\cdot 6}=\frac{3}{6}=\frac{1}{2}$. The 4s and the 5s cancel.',
        'Choice 1.'])
    video('q-091', {2: [
        "Three brackets, each one minus a fraction.",
        "The long way: a common denominator. One is four quarters. Four quarters minus one quarter — three quarters.",
        "That works. But on the exam we need speed.",
        "Shortcut one: complete to one, in your head. No common denominators.",
        D('Under the brackets write 3/4, 4/5, 5/6'),
        "One minus a quarter: three quarters. One minus a fifth: four fifths. One minus a sixth: five sixths.",
        "Now multiply. Fractions multiply top times top, bottom times bottom.",
        "But don't multiply yet. Shortcut two: cancel first.",
        D('Cancel the 4s and the 5s diagonally'),
        "The four on the bottom cancels the four on top. Same for the five.",
        D('Write "= 3/6 = 1/2" and circle choice 1'),
        "All that's left: three on top, six on the bottom. Three sixths — one half. Choice one.",
        "Everything in the middle collapsed. That's called a telescoping product — you'll see it again."]})

    # Q3 decimals. Study guide 4.5 · 0.2 ÷ 30 = 0.03; Hebrew video 2.5 · 0.2 ÷ 25 = 0.02
    S('q-092', stem=r'$5.5 \cdot 0.2 \div 22 = ?$', choices=[r'$0.05$', r'$0.5$', r'$0.11$', r'$1.1$'], correct=1, expl=[
        'Multiplication and division: left to right.',
        r'$5.5\cdot 0.2=1.1$',
        r'$1.1\div 22=\frac{1.1}{22}=\frac{11}{220}=\frac{1}{20}=\frac{5}{100}=0.05$',
        'Choice 1.'])
    video('q-092', {2: [
        "Multiplication and division share a level. So we go left to right.",
        "Method one: switch to ordinary fractions.",
        D('Under 5.5 write "11/2"; under 0.2 write "1/5"'),
        "Five point five is five and a half — eleven halves.",
        "Zero point two: one place after the point — two tenths. That is one fifth.",
        D('Write "= 11/2 · 1/5 · 1/22"'),
        "Dividing by twenty-two is multiplying by one twenty-second.",
        D('Cancel 11 with 22 (1 and 2), then write "= 1/20"'),
        "Eleven and twenty-two share an eleven: one and two. One over two times five times two — one twentieth.",
        D('Write "= 5/100 = 0.05" and circle choice 1'),
        "The choices are decimals. To turn a fraction into a decimal, make the bottom one hundred.",
        "Twenty times five is a hundred. Times five on top too: five hundredths. Two places after the point — zero point zero five. Choice one."],
        3: [
        "Method two: stay in decimals the whole way.",
        D('Write "55 · 2 = 110 → 1.10 = 1.1"'),
        "Ignore the points: fifty-five times two is a hundred and ten.",
        "Now count the places after the point: one in five point five, one in zero point two. Two in total.",
        "A hundred and ten with two places: one point one zero. One point one.",
        D('Write "1.1 ÷ 22 = 0.05"'),
        "Now one point one divided by twenty-two. A hundred and ten hundredths divided by twenty-two: five hundredths.",
        D('Circle choice 1'),
        "Zero point zero five. Same answer.",
        "Watch the traps: zero point five is one decimal hop from the answer. Zero point one one is one hop from one point one."]})

    # Q4 cancel, then add. Study guide S/Q · P/S + R/Q; Hebrew video D/A · B/D + C/A
    S('q-093', stem=r'Given: x, y, z and w are positive numbers. $\frac{2z}{y} \cdot \frac{x}{z} + \frac{w}{y} = ?$',
      choices=[r'$\frac{2x + w}{y}$', r'$\frac{2x + w}{2y}$', r'$\frac{x + w}{y}$', r'$\frac{z + w}{2y}$'], correct=1, expl=[
        r"The product first. The z's cancel: $\frac{2z}{y}\cdot\frac{x}{z}=\frac{2x}{y}$.",
        r'Same bottom, add the tops: $\frac{2x}{y}+\frac{w}{y}=\frac{2x+w}{y}$.',
        r'Check with $x=y=z=w=1$: the expression is $2\cdot 1+1=3$, and choice 1 gives $\frac{2+1}{1}=3$. Choice 1.'])
    video('q-093', {2: [
        "The product first: two z over y, times x over z.",
        D("Cross out both z's"),
        "z on top, z on the bottom — cancel it.",
        D('Write "= 2x/y + w/y"'),
        "Two x over y, plus w over y.",
        D('Write "= (2x + w)/y" and circle choice 1'),
        "Same denominator — add the tops. Two x plus w, over y. Choice one.",
        "This is the recommended route. Two moves. It's one of the first questions in a section — it should feel quick."],
        3: [
        "Not comfortable with letters? Plug in numbers. Easiest move: make them all one.",
        "But first check that the choices come out DIFFERENT with those values.",
        "Why the choices first? If two choices gave the same number, one plug-in could not decide between them.",
        D('Next to the choices write their values: 3, 3/2, 2, 1'),
        "Three, three halves, two, one. All different. So one substitution is enough.",
        D('In the question write "2 · 1 + 1 = 3"'),
        "The expression: two times one, plus one — three.",
        D('Circle choice 1'),
        "Three — choice one.",
        "Two ways. But here the recommended one is the math: cancel, then add.",
        "Plugging in is for practice, or for a moment of panic. Make sure you master these basics."]})

    # Q5 not necessarily equal. Study guide X/Y with 7X/7Y; Hebrew video A/B with 5A/5B
    S('q-094', stem=r'Given: $m\ne 0$ and $n\ne 0$. Which of the following expressions is not necessarily equal to $\frac{m}{n}$?',
      choices=[r'$\frac{4m}{4n}$', r'$m \cdot \frac{n}{n^{2}}$', r'$\frac{m^{2}}{n^{2}}$', r'$\frac{m^{2}}{n \cdot m}$'], correct=3, expl=[
        r'Choice 1: $\frac{4m}{4n}=\frac{m}{n}$ (top and bottom times 4).',
        r'Choice 2: $m\cdot\frac{n}{n^2}=\frac{mn}{n^2}=\frac{m}{n}$ (top and bottom times n).',
        r'Choice 4: $\frac{m^2}{n\cdot m}=\frac{m}{n}$ (top and bottom times m).',
        r'Choice 3 multiplies the top by m and the bottom by n — two different factors. With $m=1$ and $n=2$: $\frac{m}{n}=\frac{1}{2}$, but $\frac{m^2}{n^2}=\frac{1}{4}$. Not necessarily equal: choice 3.'])
    video('q-094', {2: [
        "Four fractions. Three of them are m over n in disguise. One isn't.",
        "Choice one: top and bottom both times four. That's just expanding. Equal.",
        D('Cross out choice 1'),
        "Choice two: m times n over n squared — top and bottom both times n. Equal.",
        "Don't see it? Cancel one n from the top and the bottom. m over n.",
        D('Cross out choice 2'),
        "Choice three: the top gets multiplied by m, the bottom by n. Two DIFFERENT factors. That's not expanding.",
        "Could it still be equal? Only if m equals n. Possible — but not necessarily.",
        D('Put a question mark next to choice 3'),
        "Spot that in the exam? Mark it and move on. Not sure? Eliminate the others.",
        "Choice four: top and bottom both times m. Equal.",
        D('Cross out choice 4 and circle choice 3'),
        "Three are out. Choice three."],
        3: [
        "Or plug in. m equals one, n equals two. So m over n is one half.",
        D('Write "m = 1, n = 2 → 1/2"'),
        "Choice one: four over eight — a half. It matches.",
        "Choice two: one times two over four — two quarters. A half again. It matches.",
        D('Next to choice 3 write "1/4 ≠ 1/2"'),
        "Choice three: one squared over two squared — one quarter. Not a half!",
        D('Circle choice 3'),
        "They asked for the one that's NOT necessarily equal — and we just found it fail. Choice three.",
        "Which way is better? Both are good. Use the one you're comfortable with."]})

    # Q6 top vs bottom. Study guide b > 1, a = (b - 0.25)/(b - 1); Hebrew video a = (b - 1/2)/(b - 1)
    S('q-095', stem='Given:\n' + r'$\begin{cases} b>2 \\ a=\frac{b-1.5}{b-2} \end{cases}$' + '\nWhich of the following is necessarily true?', expl=[
        r'$b>2$, therefore the bottom $b-2$ is positive, and the top $b-1.5$ is positive too. Therefore $a>0$. Choices 3 and 4 are out.',
        r'The top loses only 1.5. The bottom loses 2. Therefore the top is bigger than the bottom, and a positive fraction with a bigger top is more than 1: $a>1$.',
        r'Check with $b=3$: $a=\frac{3-1.5}{3-2}=1.5>1$. Choice 1.'])
    video('q-095', {2: [
        "b is bigger than two. So b minus two is positive — and b minus one and a half is bigger still. Both positive.",
        D('Under the fraction write "+ / +"'),
        "Positive over positive — a is positive. Choices three and four are out.",
        D('Cross out choices 3 and 4'),
        "Now compare the top and the bottom. Same b — but the top loses only one and a half, the bottom loses a whole two.",
        D('Write "top > bottom"'),
        "So the top is bigger than the bottom. And a positive fraction with a bigger top is more than one.",
        D('Circle choice 1'),
        "a is bigger than one. Choice one."],
        3: [
        "Or plug in. b has to be bigger than two — take b equals three.",
        D('Write "b = 3: a = (3 − 1.5)/(3 − 2) = 1.5"'),
        "Three minus one and a half: one and a half. Over one. One and a half.",
        "Choice one: is one and a half more than one? Yes. We cannot cross it out.",
        "Choice two: between zero and one? No — it is more than one. Out.",
        D('Cross out choice 2'),
        "Choices three and four: negative? No. Out.",
        D('Cross out choices 3 and 4; circle choice 1'),
        "Three choices are out. Only choice one survives.",
        "Which way is better? Understanding the top and the bottom is important. But plugging in is an excellent way too."]})

    # Q7 two kinds of numbers. Study guide 0 < x/y < 1 (x·y = 1, 1 < y/x); Hebrew video 0 < a/b < 1.
    # Same condition (0 to 1) and the same four ideas; new letters m, n and a new choice order.
    S('q-096', stem=r'Given: $0 < \frac{m}{n} < 1$. Which of the following is necessarily true?',
      choices=[r'$m \cdot n = 1$', r'$n < m$', r'$1 < \frac{n}{m}$', r'$m < n$'], correct=3, expl=[
        r'Plug in $m=1$, $n=3$ (then $\frac{m}{n}=\frac{1}{3}$, between 0 and 1). Choice 1: $1\cdot 3=3\ne 1$ — false. Choice 2: $3<1$ — false. Choices 3 and 4 survive.',
        r'Plug in a different kind of number: $m=-1$, $n=-3$ (again $\frac{m}{n}=\frac{1}{3}$). Choice 3: $\frac{n}{m}=3>1$ — true. Choice 4: $-1<-3$ — false.',
        r'Why choice 3 is always true: $\frac{m}{n}$ is positive, therefore $\frac{n}{m}$ is positive too. Flipping a positive fraction smaller than 1 gives a number bigger than 1: $0<\frac{m}{n}<1 \Rightarrow \frac{n}{m}>1$.',
        'Choice 3.'])
    video('q-096', {2: [
        "Two ways: plugging in, or understanding. The understanding here is a bit harder. So we start with plugging in.",
        "Let's plug in. m over n is one third: m equals one, n equals three.",
        D('Write "m = 1, n = 3"'),
        "Choice one: one times three is three — not one.",
        D('Cross out choice 1'),
        "Choice two: is three less than one? No.",
        D('Cross out choice 2'),
        "Choice three: three over one is three — more than one. Yes.",
        "Can we circle it? No — when you plug in, you must eliminate three.",
        "Choice four: is one less than three? Yes.",
        "Two choices survive. Don't guess! We need another substitution — a DIFFERENT kind of number.",
        "But which one? Two and five? One and four? Three and seven?",
        "They won't help. They are all positive — the same case we already tested.",
        "A positive ratio can also come from two negatives.",
        D('Write "m = −1, n = −3"'),
        "m is negative one, n is negative three. Still one third.",
        "Choice three: negative three over negative one is three. More than one again.",
        D('Cross out choice 4'),
        "Choice four: is negative one less than negative three? No — negative one is closer to zero. So it's bigger. Out.",
        "Remember: with negative numbers, the closer to zero, the bigger.",
        D('Circle choice 3'),
        "Choice three survives both. That's the answer."],
        3: [
        "So why is choice three always true?",
        "A positive ratio means the signs match — both positive, or both negative.",
        "Either way, the bottom is bigger in absolute value — further from zero than the top.",
        D('Draw a number line with 0 in the middle: on the right mark m, then n; on the left mark n, then m'),
        "On a number line: if both are positive, n is to the right of m. If both are negative, n is to the left of m — like negative three and negative one.",
        'That\'s why "m is less than n" only works when they\'re positive, and "n is less than m" only when they\'re negative. Possible — not necessary.',
        "And m times n equals one? Our first plug-in gave three. Not necessarily true.",
        "But flip any positive fraction smaller than one — you get something bigger than one. Always.",
        D('Write "0 < m/n < 1 → n/m > 1"'),
        "So n over m is always more than one. Choice three — in every case."]})
    # Q8 largest of four. Study guide 2, 7 over √2, √7; Hebrew video 3, 5 over √3, √5
    S('q-097', choices=[r'$\frac{4}{\sqrt{2}}$', r'$\frac{9}{\sqrt{2}}$', r'$\frac{4}{\sqrt{6}}$', r'$\frac{9}{\sqrt{6}}$'], correct=2, expl=[
        r'All four numbers are positive. Same bottom $\sqrt{2}$: $\frac{9}{\sqrt{2}}>\frac{4}{\sqrt{2}}$. Same bottom $\sqrt{6}$: $\frac{9}{\sqrt{6}}>\frac{4}{\sqrt{6}}$.',
        r'Final: same top 9, the smaller bottom wins. $\sqrt{2}<\sqrt{6}$, therefore $\frac{9}{\sqrt{2}}>\frac{9}{\sqrt{6}}$.',
        r'Check by squaring (all positive): $\frac{16}{2}=8$, $\frac{81}{2}=40.5$, $\frac{16}{6}<3$, $\frac{81}{6}=13.5$. The largest is $\frac{9}{\sqrt{2}}$. Choice 2.'])
    video('q-097', {2: [
        "In the lesson we compared two fractions. Here there are four. What do we do?",
        "Run a tournament. Find pairs that are easy to compare — here, pairs with the same bottom.",
        "Two semi-finals, then a final. Three comparisons, and we have the answer.",
        "Semi-final one: choices one and two. Same bottom — root two. Bigger top wins.",
        D('Cross out choice 1'),
        "Nine over root two goes through.",
        "Semi-final two: choices three and four. Same bottom — root six. Bigger top wins.",
        D('Cross out choice 3'),
        "Nine over root six goes through.",
        "The final: same top — nine. Now the SMALLER bottom wins. Root two is smaller than root six.",
        D('Cross out choice 4 and circle choice 2'),
        "Nine over root two. Choice two."],
        3: [
        "Second approach: roots everywhere. So square every choice and the roots disappear.",
        D('Next to the choices write: 16/2 = 8, 81/2 = 40.5, 16/6 < 3, 81/6 = 13.5'),
        "Sixteen over two: eight. Eighty-one over two: forty and a half. Sixteen sixths: less than three. Eighty-one over six: thirteen and a half.",
        "No need for exact values. We only need to see which one is the biggest.",
        "Forty and a half beats them all. All four numbers are positive, and for positive numbers squaring keeps the order.",
        D('Circle choice 2'),
        "Choice two again."],
        4: [
        "Third approach — understanding. A fraction is biggest with the biggest top and the smallest bottom.",
        "Here the tops repeat — four and nine. The bottoms repeat too — root two and root six.",
        D('Underline the 9s and the √2s'),
        "Biggest top: nine. Smallest bottom: root two. Only one choice has both.",
        D('Circle choice 2'),
        "Choice two. Three seconds.",
        "Three ways. Which one is best? Pick the one that feels comfortable."]})

    # Q9 tournament with letters. Study guide 0 < p < 1 < q; Hebrew video 0 < x < 1 < y.
    # Same condition (a fraction and a number above 1) and the same tournament; new letters a, b and a new choice order.
    S('q-098', stem=r'Given: $0 < a < 1 < b$. Which of the following expressions is the largest?',
      choices=[r'$\frac{a}{b - a}$', r'$\frac{b}{b - a}$', r'$\frac{b - a}{a + b}$', r'$\frac{b + a}{a + b}$'], correct=2, expl=[
        r'Given $0<a<1<b$, all the bottoms are positive: $b-a>0$ and $a+b>0$.',
        r'Choices 1 and 2 have the same bottom $b-a$, and $b>a$. Choice 2 wins.',
        r'Choices 3 and 4 have the same bottom $a+b$, and the top $b+a$ is bigger than $b-a$. Choice 4 wins. Choice 4 is exactly 1.',
        r'Choice 2: the top b is bigger than the bottom $b-a$. Therefore choice 2 is more than 1, and it beats choice 4.',
        r'Check with $a=\frac{1}{2}$, $b=\frac{5}{2}$: the choices are $\frac{1}{4}$, $\frac{5}{4}$, $\frac{2}{3}$, $1$. Choice 2.'])
    video('q-098', {2: [
        "Four expressions. Tournament time.",
        "Semi-final one: choices one and two share the bottom — b minus a. b is bigger than a. So that's positive.",
        "Tops: a against b. b is bigger.",
        D('Cross out choice 1'),
        "Choice two goes through.",
        "Semi-final two: choices three and four share the bottom — a plus b, which is positive.",
        "The tops are positive too: b is bigger than a, therefore b minus a is positive.",
        "Tops: b minus a, against b plus a. Adding beats subtracting.",
        D('Cross out choice 3'),
        "Choice four goes through.",
        "The final. Different tops, different bottoms. Now what?",
        "Open your eyes and look closer.",
        D('Next to choice 4 write "= 1"'),
        "Choice four: b plus a over a plus b. The same thing on top and bottom — exactly one.",
        "Order does not matter when you add: b plus a equals a plus b.",
        "Now: is choice two bigger or smaller than one?",
        D('Next to choice 2 write "top > bottom → more than 1"'),
        "Choice two: the top is b, the bottom is b minus something. The top is bigger. So it's more than one.",
        D('Circle choice 2'),
        "More than one beats exactly one. Choice two."],
        3: [
        "Second way: plug in. Letters in the question? You can always plug in numbers.",
        "The letter a has to be a fraction between zero and one. Take one half — the easiest fraction.",
        "For b, we would usually take a whole number, like three.",
        "But every choice adds a to b, or subtracts a from b. Three plus a half is three and a half — messy.",
        "Choose smart: two and a half. Plus or minus a half, it gives whole numbers.",
        D('Write "a = 1/2, b = 2.5"'),
        D('Next to the choices write their values: 1/4, 5/4, 2/3, 1'),
        "Choice one: a half over two — a quarter. Choice two: two and a half over two — one and a quarter. Choice three: two over three — two thirds. Choice four: three over three — exactly one.",
        D('Circle choice 2'),
        "One and a quarter is the biggest. Choice two.",
        "Two ways — both excellent."]})
    # Q10 full order of three. Study guide 5/26, 4/21, 3/16 (toward 1/5); Hebrew video 2/11, 3/17, 4/23
    S('q-099', stem=r'Given: the three fractions $\frac{6}{19}$, $\frac{5}{16}$, $\frac{4}{13}$. Which of the following inequalities is correct?',
      choices=[r'$\frac{4}{13} < \frac{5}{16} < \frac{6}{19}$', r'$\frac{6}{19} < \frac{5}{16} < \frac{4}{13}$',
               r'$\frac{4}{13} < \frac{6}{19} < \frac{5}{16}$', r'$\frac{5}{16} < \frac{4}{13} < \frac{6}{19}$'], correct=1, expl=[
        r'Make the tops equal to 60: $\frac{6}{19}=\frac{60}{190}$, $\frac{5}{16}=\frac{60}{192}$, $\frac{4}{13}=\frac{60}{195}$.',
        r'Same top: the smaller bottom wins. Therefore $\frac{4}{13}<\frac{5}{16}<\frac{6}{19}$.',
        r'Check by cross-multiplying: $4\cdot 16=64<65=5\cdot 13$ and $5\cdot 19=95<96=6\cdot 16$. Choice 1.'])
    video('q-099', {2: [
        "Careful: they want the full order — biggest, middle and smallest. Not just the biggest.",
        "The basic way is a common bottom. But for nineteen, sixteen and thirteen it runs into the thousands.",
        "No calculator on the exam. That way is off the table.",
        "But look at the tops: six, five, four. Tiny.",
        "So let's make the TOPS equal. Six, five and four all go into sixty.",
        D('Under the fractions write 60/190, 60/192, 60/195'),
        "Six nineteenths times ten: sixty over a hundred ninety. Five sixteenths times twelve: sixty over a hundred ninety-two. Four thirteenths times fifteen: sixty over a hundred ninety-five.",
        "Same tops. Now the SMALLEST bottom wins.",
        D('Mark 6/19 "biggest" and 4/13 "smallest"'),
        "Six nineteenths is the biggest. Four thirteenths is the smallest.",
        D('Circle choice 1'),
        "Smallest to biggest: four thirteenths, five sixteenths, six nineteenths. Choice one."],
        3: [
        "Cross-multiplication works too. But comparing every pair takes three comparisons.",
        "Smarter: compare any two fractions, then use the choices. Two comparisons may be enough.",
        D('Write "4 · 16 = 64 < 65 = 5 · 13"'),
        "Four thirteenths against five sixteenths: sixty-four against sixty-five. Four thirteenths is smaller.",
        D('Cross out choices 2 and 4'),
        "Any choice that says otherwise is out: two and four.",
        D('Write "5 · 19 = 95 < 96 = 6 · 16"'),
        "One more comparison between what's left: five sixteenths against six nineteenths. Ninety-five, ninety-six — five sixteenths is smaller.",
        D('Cross out choice 3 and circle choice 1'),
        "Choice three says the opposite. Choice one."],
        4: [
        "And for the creative ones: flip them.",
        D('Under the fractions write 19/6 = 3⅙, 16/5 = 3⅕, 13/4 = 3¼'),
        "Nineteen sixths: three and a sixth. Sixteen fifths: three and a fifth. Thirteen quarters: three and a quarter.",
        "Three and a quarter is the biggest flip. So four thirteenths is the smallest original.",
        D('Circle choice 1'),
        "All three are positive — and flipping positive numbers reverses the order. Choice one, a third time."],
        5: ('Method 4 · Pieces of 1/3', [
        "One more way — for strong students. Look at how the list is built.",
        D('Write "4/13 → 5/16 → 6/19: +1 on top, +3 on the bottom"'),
        "From four thirteenths to five sixteenths: one more on top, three more on the bottom. Then again.",
        "Each step mixes in a piece worth one third. Tops together, bottoms together — the result always lands between the two fractions.",
        D('Write "4/13 < 1/3 (12 < 13)"'),
        "Four thirteenths is less than one third: twelve against thirteen.",
        "So every step pulls the fraction up toward one third.",
        D('Write "4/13 < 5/16 < 6/19 < 1/3" and circle choice 1'),
        "The list climbs. Choice one — a fourth time."])})

    # ---------------- self-practice from the Hebrew study guide
    S('q-081', stem=r'$\frac{\frac{1}{6} + \frac{1}{10}}{\frac{16}{15}} = ?$',
      choices=[r'$\frac{1}{2}$', r'$\frac{1}{4}$', r'$\frac{1}{3}$', r'$\frac{3}{4}$'], correct=2, expl=[
        r'Top first: $\frac{1}{6}+\frac{1}{10}=\frac{5}{30}+\frac{3}{30}=\frac{8}{30}=\frac{4}{15}$.',
        r'Dividing by $\frac{16}{15}$ means multiplying by $\frac{15}{16}$: $\frac{4}{15}\cdot\frac{15}{16}=\frac{4}{16}=\frac{1}{4}$.',
        r'Another way: multiply the top and the bottom of the big fraction by 30. The top becomes $5+3=8$, and the bottom becomes $32$: $\frac{8}{32}=\frac{1}{4}$.',
        'Choice 2.'])
    S('q-082', stem=r'Given: a, b, c and d are nonzero. $\frac{\frac{2b}{d} \cdot \frac{c}{b}}{\frac{d}{a} \cdot \frac{b}{d}} = ?$',
      choices=[r'$\frac{2bc}{ad}$', r'$\frac{2ac}{bd}$', r'$\frac{2c^{2}}{d^{2}}$', r'$\frac{bd}{2ac}$'], correct=2, expl=[
        r"Top: $\frac{2b}{d}\cdot\frac{c}{b}=\frac{2c}{d}$ (the b's cancel).",
        r"Bottom: $\frac{d}{a}\cdot\frac{b}{d}=\frac{b}{a}$ (the d's cancel).",
        r'Divide: $\frac{2c}{d}\div\frac{b}{a}=\frac{2c}{d}\cdot\frac{a}{b}=\frac{2ac}{bd}$. Choice 2.',
        r'Another way: dividing by the bottom product means multiplying by its flip: $\frac{2b}{d}\cdot\frac{c}{b}\cdot\frac{a}{d}\cdot\frac{d}{b}$. Cancel one b and one d from the top and the bottom: $\frac{2ac}{bd}$. Choice 2 again.'])
    S('q-083', stem=r'$\frac{1}{8} + \frac{1}{6} - \frac{1}{4} = ?$',
      choices=[r'$\frac{1}{8}$', r'$\frac{1}{12}$', r'$\frac{1}{48}$', r'$\frac{1}{24}$'], correct=4, expl=[
        r'The common denominator of 8, 6 and 4 is 24: $\frac{1}{8}=\frac{3}{24}$, $\frac{1}{6}=\frac{4}{24}$, $\frac{1}{4}=\frac{6}{24}$.',
        r'$\frac{3}{24}+\frac{4}{24}-\frac{6}{24}=\frac{1}{24}$. Choice 4.',
        r'Another way: combine the first and the last fractions first: $\frac{1}{8}-\frac{1}{4}=-\frac{1}{8}$. Then add $\frac{1}{6}$: $\frac{1}{6}-\frac{1}{8}=\frac{4}{24}-\frac{3}{24}=\frac{1}{24}$.'])
    S('q-084', choices=[r'$\frac{16}{17}$', r'$\frac{17}{18}$', r'$\frac{18}{19}$', r'$\frac{19}{20}$'], correct=4, expl=[
        r'Each fraction is 1 minus a small piece: $\frac{16}{17}=1-\frac{1}{17}$, $\frac{17}{18}=1-\frac{1}{18}$, $\frac{18}{19}=1-\frac{1}{19}$, $\frac{19}{20}=1-\frac{1}{20}$.',
        r'The smallest missing piece is $\frac{1}{20}$. Therefore $\frac{19}{20}$ is the largest. Choice 4.',
        r'Another way: put all four fractions over one common bottom and compare the tops. It works, but here the common bottom is 58,140 — far too long without a calculator. The distance from 1 is the smart way.'])
    S('q-085', stem=r'Given: $L = \frac{4}{9} - M$. For which value of M will L be the smallest?',
      choices=[r'$\frac{1}{3}$', r'$\frac{13}{36}$', r'$\frac{7}{18}$', r'$\frac{11}{28}$'], correct=4, expl=[
        'L gets smaller when M gets bigger. We need the largest M.',
        r'$\frac{1}{3}=\frac{12}{36}<\frac{13}{36}$, and $\frac{13}{36}<\frac{14}{36}=\frac{7}{18}$.',
        r'$\frac{7}{18}$ against $\frac{11}{28}$: cross-multiply, $7\cdot 28=196<198=18\cdot 11$. Therefore $\frac{11}{28}$ is bigger.',
        r'The largest M is $\frac{11}{28}$. Choice 4.'])
    S('q-086', stem=r'The value of which of the following expressions is not equal to $\frac{2}{3}$?',
      choices=[r'$-1 + \frac{5}{3}$', r'$3 - \frac{7}{3}$', r'$\frac{14}{21}$', r'$\frac{4}{9}$'], correct=4, expl=[
        r'Choice 1: $-1+\frac{5}{3}=-\frac{3}{3}+\frac{5}{3}=\frac{2}{3}$.',
        r'Choice 2: $3-\frac{7}{3}=\frac{9}{3}-\frac{7}{3}=\frac{2}{3}$.',
        r'Choice 3: $\frac{14}{21}=\frac{2}{3}$ (divide the top and the bottom by 7).',
        r'Choice 4: $\frac{2}{3}=\frac{6}{9}\ne\frac{4}{9}$. Choice 4 is not equal.'])
    S('q-087', choices=[r'$2 < m - n$', r'$0 < m - n < 2$', r'$2 < \frac{n}{m}$', r'$0 < \frac{n}{m} < 1$'], correct=4, expl=[
        r'm and n are positive and different. Therefore $\frac{m}{n}$ is a positive integer other than 1: $\frac{m}{n}\ge 2$.',
        r'Flip (both positive): $0<\frac{n}{m}\le\frac{1}{2}$. Choice 4 is always true, and choice 3 is always false.',
        r'Choice 1 fails for small numbers: $m=1$, $n=0.5$ gives $\frac{m}{n}=2$ and $m-n=0.5$, which is not more than 2.',
        r'Choice 2 fails for big numbers: $m=6$, $n=2$ gives $\frac{m}{n}=3$ and $m-n=4$, which is not between 0 and 2.',
        'Choice 4.'])
    S('q-088', stem='Given:\n' + r'$\begin{cases} a>2 \\ x\ne a \end{cases}$' + '\n' + r'For which of the following values of x will the value of $\frac{a+x}{a-x}$ be the smallest?',
      choices=[r'$x=2$', r'$x=\frac{1}{3}$', r'$x=-\frac{1}{3}$', r'$x=-\frac{2}{3}$'], correct=4, expl=[
        r'All four values of x are at most 2, and $a>2$. Therefore the bottom $a-x$ is positive.',
        r'When x gets smaller, the top $a+x$ gets smaller and the bottom $a-x$ gets bigger. Both changes make the fraction smaller. Therefore the smallest x gives the smallest value: $x=-\frac{2}{3}$.',
        r'Check with $a=3$: $x=-\frac{2}{3}$ gives $\frac{3-\frac{2}{3}}{3+\frac{2}{3}}=\frac{7}{11}\approx 0.64$; $x=-\frac{1}{3}$ gives $\frac{8}{10}=0.8$; $x=\frac{1}{3}$ gives $\frac{10}{8}=1.25$; $x=2$ gives $\frac{5}{1}=5$. Choice 4.'])
    S('q-089', choices=[r'$\frac{13}{12}$', r'$\frac{11}{9}$', r'$\frac{25}{21}$', r'$\frac{25}{23}$'], correct=1, expl=[
        r'Each number is 1 plus an extra: $\frac{13}{12}=1+\frac{1}{12}$, $\frac{11}{9}=1+\frac{2}{9}$, $\frac{25}{21}=1+\frac{4}{21}$, $\frac{25}{23}=1+\frac{2}{23}$.',
        r'Compare $\frac{1}{12}$ with the other extras by cross-multiplying: $9<24$, $21<48$, $23<24$. Therefore $\frac{1}{12}$ is the smallest extra.',
        r'Check with decimals: $\frac{13}{12}\approx 1.083$, $\frac{11}{9}\approx 1.222$, $\frac{25}{21}\approx 1.190$, $\frac{25}{23}\approx 1.087$.',
        r'The smallest number is $\frac{13}{12}$. Choice 1.'])
    S('q-090', stem=r'Given: the three fractions $\frac{3}{25}$, $\frac{4}{31}$, $\frac{5}{41}$. Which of the following inequalities is correct?',
      choices=[r'$\frac{3}{25} < \frac{4}{31} < \frac{5}{41}$', r'$\frac{5}{41} < \frac{4}{31} < \frac{3}{25}$',
               r'$\frac{3}{25} < \frac{5}{41} < \frac{4}{31}$', r'$\frac{4}{31} < \frac{3}{25} < \frac{5}{41}$'], correct=3, expl=[
        r'All positive: cross-multiply pairs. $\frac{3}{25}$ against $\frac{5}{41}$: $3\cdot 41=123<125=25\cdot 5$. Therefore $\frac{3}{25}<\frac{5}{41}$.',
        r'$\frac{5}{41}$ against $\frac{4}{31}$: $5\cdot 31=155<164=41\cdot 4$. Therefore $\frac{5}{41}<\frac{4}{31}$.',
        r'The order is $\frac{3}{25}<\frac{5}{41}<\frac{4}{31}$. Choice 3. (Decimals: 0.12, about 0.122, about 0.129.)'])


def apply(M):
    fix_lesson(M)
    fix_card(M)
    fix_questions(M)
    fix_solution_videos(M)
    add_guided(M)
    add_practice(M)
    add_summary(M)
    hebrew_check(M)
    new_numbers(M)
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
    # alg-extra-unit-t3-1-4 was the lesson example 3/sqrt10 vs 2/sqrt5 of "compare-fractions" (RECORDED) -> new numbers.
    M.set_q('alg-extra-unit-t3-1-4', stem=r'Which is greater: $\frac{3}{\sqrt{6}}$ or $\frac{2}{\sqrt{3}}$?',
            expl=['Both numbers are positive. Therefore we can square them and keep the order.',
                  r'$\left(\frac{3}{\sqrt{6}}\right)^2=\frac{9}{6}$ and $\left(\frac{2}{\sqrt{3}}\right)^2=\frac{4}{3}=\frac{8}{6}$.',
                  r'$\frac{9}{6}>\frac{8}{6}$, therefore $\frac{3}{\sqrt{6}}>\frac{2}{\sqrt{3}}$. The first expression is greater. Choice 2.'])


# =========================================================================================
# 2026-10-06 review (renumber pass, topics 17-20): course-wide duplicate scan
# =========================================================================================
def review_dups(M):
    # q-r26-t03-11 was the same question as guided q-r26-t12-01 (-1<x<0, largest of x, x^2, x^3, 1/x)
    # and close to q-r26-t08-11 (largest of x..x^4). It now asks for the SMALLEST of the same four.
    M.set_q('q-r26-t03-11', stem=r'Given: $-1<x<0$. Which of the following is the smallest?',
            choices=[r'$x$', r'$x^2$', r'$x^3$', r'$\frac{1}{x}$'], correct=4,
            expl=[r'Plug in $x=-\frac{1}{2}$: $x=-\frac{1}{2}$, $x^2=\frac{1}{4}$, $x^3=-\frac{1}{8}$, $\frac{1}{x}=-2$.',
                  r'The smallest is $-2$, that is $\frac{1}{x}$. Choice 4.',
                  r'The rule: for $-1<x<0$, $\frac{1}{x}<x<x^3<0<x^2$.'])


_apply_before_review = apply


def apply(M):
    _apply_before_review(M)
    review_dups(M)


# =========================================================================================
# 2026-10-06 Hebrew back-check: items that had landed on the numbers of the teacher's Hebrew VIDEOS
# =========================================================================================
def hebrew_backcheck(M):
    # q-fraction-compare (solution video NOT recorded): 9/17 "half of 17 is 8.5, 9 > 8.5" is the Hebrew lesson's own
    # benchmark-1/2 example (5/11 vs 9/17). 9/17 -> 11/21 (half of 21 is 10.5, 11 > 10.5). Same type, same trap.
    A_, B_ = r'\frac{7}{15}', r'\frac{11}{21}'
    ch = ['$%s<\\frac{1}{2}<%s$' % (A_, B_), '$%s<\\frac{1}{2}<%s$' % (B_, A_),
          '$\\frac{1}{2}<%s<%s$' % (A_, B_), '$%s<%s<\\frac{1}{2}$' % (A_, B_)]
    M.set_q('q-fraction-compare', choices=ch, correct=1, expl=[
        r'Half of 15 is 7.5, and $7<7.5$. Therefore $\frac{7}{15}<\frac{1}{2}$.',
        r'Half of 21 is 10.5, and $11>10.5$. Therefore $\frac{11}{21}>\frac{1}{2}$.',
        r'Check by cross-multiplying with $\frac{1}{2}$: $2\cdot 7=14<15$ and $2\cdot 11=22>21$.',
        r'The order is $\frac{7}{15}<\frac{1}{2}<\frac{11}{21}$. Choice 1.'])
    vid = 'solve-q-fraction-compare'
    for b in M.video(vid)['beats']:
        for it in b['items']:
            if it.get('k') == 'q' and it.get('qid') == 'q-fraction-compare': it['choices'] = list(ch)
    _dd_sub(M, vid, 2, [
        ('one half, nine seventeenths.', 'one half, eleven twenty-firsts.'),
        ('½ of 17 = 8.5 → 9 > 8.5', '½ of 21 = 10.5 → 11 > 10.5'),
        ('Half of seventeen is eight and a half. Nine is more.', 'Half of twenty-one is ten and a half. Eleven is more.'),
        ('then one half, then nine seventeenths.', 'then one half, then eleven twenty-firsts.'),
        ('Two times nine is eighteen — more than seventeen.', 'Two times eleven is twenty-two — more than twenty-one.')])

    # Memory card "Square them": 3/sqrt10 vs 2/sqrt5 is exactly the Hebrew lesson example -> 4/sqrt19 vs 3/sqrt11
    # (squares 16/19 > 9/11, since 16*11 = 176 > 171 = 9*19). The recorded lesson slide keeps its numbers.
    for cid, c in M.D['references'].items():
        for tb in c.get('tables') or []:
            for row in tb.get('rows') or []:
                for k, cell in enumerate(row):
                    if isinstance(cell, str) and r'\frac3{\sqrt{10}}>\frac2{\sqrt5}' in cell:
                        row[k] = r'$\frac4{\sqrt{19}}>\frac3{\sqrt{11}}$ because $\frac{16}{19}>\frac9{11}$'
                        M.log.append('card %s: square-them example renumbered' % cid)


_apply_before_hebrew = apply


def apply(M):
    _apply_before_hebrew(M)
    hebrew_backcheck(M)


# =====================================================================================
# 2026-10-07 practice clean-up (teacher-approved). Practice was 25: the 10 Hebrew self-practice questions
# (q-081 ... q-090), 7 extra-bank warm-ups and 8 September-review items. Copies out, at most 3 warm-ups, review
# items whose type the Hebrew / guided questions already practise out. Kept: all 10 Hebrew, 2 warm-ups, 3 review
# items of types the Hebrew does not have. Runs LAST.
# =====================================================================================
CLEANUP_REMOVE = [
    # copies (practice_audit/copies_by_topic.txt, each checked against the current build)
    'alg-extra-unit-t3-1-6',   # 3/5 vs 4/6: same as warm-up alg-extra-unit-t3-1-1 (two plain fractions)
    'alg-extra-unit-t3-1-2',   # largest of 15/16, 4/5, 7/8, 10/11: same as Hebrew q-084 (distance from 1)
    'q-r26-t03-09',            # smallest of 22/20 ... 24/22: same as Hebrew q-089 (fractions above 1)
    'q-r26-t03-10',            # largest of k/sqrt(m): same as guided q-097
    'q-r26-t03-11',            # -1 < x < 0, smallest of x, x², x³, 1/x: guided q-r26-t12-01 / q-r26-t08-02 type
    # warm-ups beyond the kept ones
    'alg-extra-unit-t3-1-4',   # 3/sqrt6 vs 2/sqrt3: guided q-097 type (square them)
    'alg-extra-unit-t3-1-7',   # (c + x)/(c - x) smallest: same as Hebrew q-088
    'alg-extra-unit-t3-1-5',   # 0 < x < 1, largest of x, x², 1, 1/x: guided q-r26-t03-03 type
    # September items of a type the Hebrew / guided questions already practise
    'q-r26-t03-07',            # largest of four negative fractions: comparing fractions = Hebrew q-084 / q-089 / q-090
    'q-r26-t03-04',            # (7 + x)/(9 + x) vs 7/9: guided q-r26-t03-02 with other numbers
]
CLEANUP_ORDER = [
    'q-083', 'q-086', 'q-081', 'q-082', 'alg-extra-unit-t3-1-1', 'q-084', 'alg-extra-unit-t3-1-3',
    'q-085', 'q-089', 'q-r26-t03-05', 'q-090', 'q-087', 'q-088', 'q-r26-t03-06', 'q-r26-t03-08']


def practice_cleanup(M):
    for qid in CLEANUP_REMOVE:
        assert M.section_of(qid) == PRACTICE, qid
        M.unplace(qid)
    M.practice_order(PRACTICE, CLEANUP_ORDER)
    got = [f['ref'] for f in M.D['flow'] if f['section'] == PRACTICE and f['type'] == 'question']
    assert got == CLEANUP_ORDER, got


_apply_before_practice_cleanup = apply


def apply(M):
    _apply_before_practice_cleanup(M)
    practice_cleanup(M)   # 2026-10-07 practice clean-up: runs last


# =====================================================================================
# 2026-10-07 methods spread: the 2026-10-06 exam methods added as an extra written line wherever they genuinely
# solve the question (append only; the existing solution stays). Methods taught in a later topic are phrased as a
# self-contained shortcut with a one-line why. No video changes. Runs LAST.
# =====================================================================================
SPREAD_METHODS = {
    'q-096': [
        'Shortcut: the mirror test. Put $-m$ and $-n$ in place of $m$ and $n$. Then $\\frac{-m}{-n}=\\frac mn$, so the given stays exactly the same, and anything necessarily true must stay true in the mirror too.',
        "Choice 2 ($n<m$) turns into $-n<-m$, that is $m<n$, its opposite. A statement and its opposite can't both always be true, so choice 2 is out, and choice 4 the same way. Choice 1 fails with $m=1$, $n=3$ ($1\\cdot3\\ne1$). The answer is choice 3.",
    ],
}


def spread_methods(M):
    for qid, lines in SPREAD_METHODS.items():
        q = M.q(qid)
        M.set_q(qid, expl=list(q['explanation']) + lines)


_apply_before_spread_methods = apply


def apply(M):
    _apply_before_spread_methods(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


# ===================================================================================================================
# 2026-10-07 no decimal estimates. Teacher: a student can't estimate roots or π to one decimal place. Estimates use
# whole-number benchmarks only (perfect squares, squaring, a factor into the root, 3 < π < 3.5) or another method.
# Recorded videos are never changed (any take in ~/Documents/Course.recordings).
import glob as _nd_glob, os as _nd_os, re as _nd_re


def _nd_recorded(vid):
    # only takes recorded BEFORE this change was first built (2026-10-07 12:40Z) keep the old video; takes recorded
    # later were made with the rewritten slides, so the rewrite must stay
    pat = _nd_re.compile(_nd_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _nd_glob.glob(_nd_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_nd_os.path.basename(f))
        if m and m.group(1) < '2026-10-07T12-40-00': return True
    return False


def _nd_n(M, vid, title):
    ns = [i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title]
    assert len(ns) == 1, (vid, title, ns)
    return ns[0]


def _nd_lines(M, vid, title, subs):
    """subs: [(kind, old, new)], kind 'say' or 'draw'; new is a str or a list of str of the same kind."""
    n = _nd_n(M, vid, title)

    def fn(ls):
        ls = list(ls)
        for kind, old, new in subs:
            k = [i for i, l in enumerate(ls) if l.get(kind) == old]
            assert len(k) == 1, (vid, title, old)
            ls[k[0]:k[0] + 1] = [{kind: x} for x in ([new] if isinstance(new, str) else new)]
        return ls
    M.edit_lines(vid, n, fn)


def _nd_item(M, vid, title, old_t, new_t, label=None):
    n = _nd_n(M, vid, title); b = M.slide(vid, n)
    k = [i for i, it in enumerate(b['items']) if it.get('t') == old_t]
    assert len(k) == 1, (vid, title, old_t)
    b['items'][k[0]]['t'] = new_t
    if label is not None:
        for l in b['lines']:
            if l.get('appear') == k[0]: l['label'] = label
    M.touched_videos.add(vid)


def _nd_expl(M, qid, subs):
    """subs: [(index, old_start, new)]; new None drops the paragraph."""
    ex = list(M.q(qid)['explanation'])
    for i, start, new in sorted(subs, key=lambda x: -x[0]):
        assert ex[i].startswith(start), (qid, i, ex[i][:70])
        if new is None: ex.pop(i)
        else: ex[i] = new
    M.set_q(qid, expl=ex)


def no_decimal_estimates(M):
    _nd_expl(M, 'q-088', [(2, 'Check with $a=3$:',
             'Check with $a=3$: $x=-\\frac{2}{3}$ gives $\\frac{3-\\frac{2}{3}}{3+\\frac{2}{3}}=\\frac{7}{11}$; $x=-\\frac{1}{3}$ gives $\\frac{8}{10}$; '
             '$x=\\frac{1}{3}$ gives $\\frac{10}{8}$; $x=2$ gives $\\frac{5}{1}=5$. Only the first two are less than 1, and '
             '$\\frac{7}{11}<\\frac{8}{10}$ ($70<88$). Choice 4.')])
    _nd_expl(M, 'q-089', [(2, 'Check with decimals:', None)])   # 1.083 vs 1.087: not something a student can do
    q = M.q('q-090'); old = ' (Decimals: 0.12, about 0.122, about 0.129.)'
    assert q['explanation'][2].endswith(old), 'q-090 changed'
    _nd_expl(M, 'q-090', [(2, 'The order is', q['explanation'][2][:-len(old)])])
    _nd_expl(M, 'alg-extra-unit-t3-1-3', [(2, 'Check with $x=1$:',
             'Check with $x=1$: $\\frac{7}{3}=2\\frac13$ and $\\frac{7}{6}=1\\frac16$. The first fraction is greater. Choice 3.')])


_apply_before_no_decimal_estimates = apply


def apply(M):
    _apply_before_no_decimal_estimates(M)
    no_decimal_estimates(M)   # 2026-10-07 no decimal estimates: runs last


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
    # Hebrew compare lesson (lines 1530-1536, 1558): don't fear bigger numbers when you cross-multiply - split them;
    # and the exam's fractions are usually small. All topic-3 lesson videos are recorded -> memory card tip.
    c = M.card('mem-compare')
    tip = ('Bigger numbers when you cross-multiply? Split them: $18\\cdot7=10\\cdot7+8\\cdot7=126$. '
           'And on the exam the fractions are usually small, like $\\frac45$ and $\\frac56$.')
    if tip not in c['tips']: c['tips'].append(tip)


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST
