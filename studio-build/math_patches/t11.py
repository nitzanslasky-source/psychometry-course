"""Topic 11 - Laws of Exponents & Roots (Advanced). Course review 2026-09 fixes.
See t11_CHANGES.md for the plain-language list.
Sums of powers, comparing powers and bases between 0 and 1 are taught in T8/T10 (and T9 for roots); this patch
only points back to them and adds the advanced tools Section B uses."""
from dsl import T, H, A, D, Q
from math_api import _word

TOPIC = 11
LESSON = 'advanced-powers'
TOOLS = 'r26-t11-tools'
NQ = 16                                    # guided questions in the topic after this patch
QSIDEBAR = ['Question %d' % k for k in range(1, NQ + 1)]
GROUP_B = 'Advanced Powers B'


def _solution(M, qid, intro, slides, after=None):
    """Guided-question solution video in the style of solve-q-294..301 (Section B)."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % _word(n)] + intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=n - 1, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, GROUP_B, QSIDEBAR, beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = GROUP_B
    v['hybrid']['num'] = 31
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _sync(M, qid):
    """Question text changed: keep the solution video's title and 'Pre-loaded' notes in sync."""
    v = M.video('solve-' + qid); q = M.q(qid)
    v['title'] = v['navLabel'] = q['stem']
    for b in v['beats']:
        if b.get('canvas', '').startswith('Pre-loaded — question'):
            b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])


def apply(M):
    S = M.set_q

    # =====================================================================================
    # 1. Section A lesson: "no new rules" -> point back to T8-T10; patterns slide
    # =====================================================================================
    M.set_slide(LESSON, 1, script=[
        "Advanced exponents and roots.",
        "Most rules here you already know — from topics eight, nine and ten. These questions combine them.",
        "The hard part is choosing the right form. Let's see how.",
    ])
    # Pass 2: the original slide 3 "Laws + identities" stays; "Patterns to spot" is an added slide after it
    # (its (x+y)^2 pattern is on the original slide, so it holds the other two patterns).
    M.insert_slides(LESSON, 3, [dict(mode='concept', active=2, title='Patterns to spot', script=[
        "Two more patterns you already know. Spot them, and the question gets short.",
        A("'aᵇ = bᵃ: only 2 and 4' appears", T('Different positive whole numbers: $a^b=b^a$ only for $2$ and $4$', size=40, gap=40)),
        "Pattern one, from topic eight: a to the b equals b to the a.",
        "For two different positive whole numbers, the only pair is two and four.",
        "Only whole numbers! With fractions there are other pairs. So check what the question gives you.",
        A('copies appear', T('$2^y+2^y+2^y+2^y=4\\cdot2^y=2^{y+2}$', size=48)),
        "Pattern two, from topics eight and ten: equal powers added. Count the copies.",
        "Four copies of two to the y is four times two to the y — two to the y plus two.",
    ])])
    M.video(LESSON)['beats'][4]['active'] = 3; M.video(LESSON)['beats'][5]['active'] = 4   # Choose a method, Recap shift down
    M.set_slide(LESSON, 6, script=[
        "Let's lock it in.",
        A("'Translate before calculating' appears", T('Translate before calculating', size=46)),
        A("'Look for a known pattern' appears", T('Look for a known pattern', size=46)),
        A("'Two routes: the laws, or plug in' appears", T('Two routes: the laws, or plug in', size=46)),
        D('Tick each line'),
        "Five questions next. Try each one first — then watch its solution.",
    ])
    M.set_sidebar(LESSON, ['Translate first', 'Laws + identities', 'Patterns to spot', 'Choose a method', 'Recap'])

    # =====================================================================================
    # 2. Q4 video: "only 2 and 4" needs "positive whole numbers"
    # =====================================================================================
    M.set_slide('solve-q-291', 3, script=[
        "Much shorter if you know the pattern: a to the b equals b to the a.",
        A('2⁴ = 4² = 16 appears', T('$2^4=4^2=16$', size=52)),
        "From topic eight: for two different positive whole numbers, this happens only with two and four.",
        "Here the choices are whole numbers. If y is a whole number, x — y squared — is one too. So they must be two and four.",
        D('Next to the question write "y = 2 or 4"'),
        "So y is two or four. Test four: then x is sixteen — not two, not four. Out.",
        D('Cross out choice 4'),
        D('Circle choice 2'),
        "y is two, x is four. Four squared is sixteen, two to the fourth is sixteen. Done in seconds.",
        "Careful: the pattern is only for whole numbers. With fractions there are other pairs — for example nine quarters and twenty-seven eighths.",
        "So use it when the choices are whole numbers.",
    ])

    # =====================================================================================
    # 3. Other existing solution videos
    # =====================================================================================
    # Q10 (solve-q-297 slide 3): Pass 2 keeps the original line "The lesson's favourite is four ..."

    # Q9: rationalize first (fastest), then the original two methods (match / multiply the denominators)
    M.insert_slides('solve-q-296', 1, [dict(mode='question', active=M.slide('solve-q-296', 2)['active'],
                                            title='Method 1 · Clear the root', pre=[Q('q-296')], script=[
        "Fastest route: get the root out of the first denominator.",
        D('Next to 3/(2√2) write "· √2/√2 = 3√2/(2 · 2) = 3√2/4"'),
        "Multiply top and bottom by root two. Root two times root two is two — so the bottom is two times two, four.",
        "Now both fractions have four at the bottom.",
        D('Write "3√2/4 + √2/4 = 4√2/4 = √2"'),
        "Three root two plus one root two: four root two. Over four: root two.",
        D('Circle choice 2'),
        "Choice two.",
    ])])
    M.set_slide('solve-q-296', 3, title='Method 2 · Match the denominators')
    M.edit_lines('solve-q-296', 3, lambda ls: [
        {'say': "Method two: rewrite the second fraction so it matches the first."} if 'Method one' in l.get('say', '') else l
        for l in ls])
    M.set_slide('solve-q-296', 4, title='Method 3 · Multiply the denominators')
    M.edit_lines('solve-q-296', 4, lambda ls: [
        dict(l, say=l['say'].replace('Method two:', 'Method three:')) if 'say' in l else l for l in ls])
    M.edit_lines('solve-q-296', 1, lambda ls: [
        {'say': 'Two fractions with roots. Three ways to add them.'} if l.get('say', '').startswith('Two fractions with roots') else l
        for l in ls])

    # Q12: the original "Open the brackets" first, then "Product equals zero" as the second method
    M.set_slide('solve-q-299', 2, title='Method 1 · Open the brackets')
    M.insert_slides('solve-q-299', 2, [dict(mode='question', active=M.slide('solve-q-299', 2)['active'],
                                            title='Method 2 · Product equals zero', pre=[Q('q-299')], script=[
        "Method two — the fast one. Look at the left side: it's already a product. Root x, times root x minus three.",
        "A product is zero only when one of the factors is zero.",
        D('Write "√x = 0  or  √x − 3 = 0"'),
        "So root x is zero — or root x minus three is zero.",
        D('Write "√x = 0 → x = 0"'),
        "Root x is zero: x is zero.",
        D('Write "√x = 3 → x = 9"'),
        "Root x is three: x is nine.",
        D('Circle choice 2'),
        "The same two solutions. Choice two.",
    ])])

    # Q13: quick check - 108 = 4 * 27
    M.edit_lines('solve-q-300', 2, lambda ls: ls + [
        {'draw': 'Write "√108 = √(4 · 27) = 2√27 → 3x = 3√27 → x = √27 = 3√3"'},
        {'say': "An even faster way to see it: a hundred and eight is four times twenty-seven. So root one-oh-eight is two root twenty-seven."},
        {'say': "Three x is three root twenty-seven. x is root twenty-seven — three root three. Same answer."},
    ])

    # Q14: no longer the last question; Method 3 gets an explicit check
    M.edit_lines('solve-q-301', 1, lambda ls: [{'say': 'Question fourteen.'} if l.get('say') == 'Last question.' else l for l in ls])
    def q14(ls):
        out = []
        for l in ls:
            if l.get('say', '').startswith('The minus sign flips things'):
                out += [{'say': "The minus sign flips the fraction. So try the reciprocal: one sixteenth."},
                        {'draw': 'Next to choice 4 write "(1/16)^(−1/2) = 16^(1/2) = 4 ✓"'},
                        {'say': "One sixteenth to the minus a half: flip it — sixteen to the half. Root sixteen: four. It works."}]
            else:
                out.append(l)
        return out
    M.edit_lines('solve-q-301', 4, q14)

    # =====================================================================================
    # 4. Existing questions: TeX, no colons, stacked conditions, plug-in checks
    # =====================================================================================
    S('q-288', expl=[
        'Write $15$ as $3\\cdot5$ before expanding: $(15x^2)^3=3^3\\cdot5^3\\cdot x^6$.',
        'Top: $(3x)^4\\cdot(5x)^3=3^4\\cdot5^3\\cdot x^7$.',
        '$\\frac{3^4\\cdot5^3\\cdot x^7}{3^3\\cdot5^3\\cdot x^6}=3x$. Then $3x\\cdot\\frac13x=x^2$.',
        'Check with $x=1$: $\\frac{3^4\\cdot5^3}{15^3}\\cdot\\frac13=3\\cdot\\frac13=1$. The choices give $\\frac13$, $3$, $\\frac53$ and $1$, so only $x^2$ fits.'])
    S('q-289', expl=[
        'A negative exponent moves a factor to the other side of the fraction bar, with a positive exponent: $a^{-2}$ on top becomes $a^2$ at the bottom, and $d^{-5}$ at the bottom becomes $d^5$ on top.',
        '$b^3$ and $c^4$ stay where they are: $\\frac{d^5\\cdot b^3}{c^4\\cdot a^2}$.'])
    S('q-290', stem='Given: $y$ is an integer, and\n$\\begin{cases} x\\ne1 \\\\ x^{y+2}=1 \\end{cases}$\nWhich of the following is necessarily true?',
      expl=[
        'A power equals 1 in three cases: the base is 1; the base is $-1$ and the exponent is even; the exponent is 0 and the base is not 0.',
        'Here $x\\ne1$. Therefore $y+2=0$ (that is, $y=-2$), or $x=-1$ (with $y+2$ even).',
        'An "or" claim is necessarily true when every allowed case makes at least one part true. Choice (2) covers both cases.',
        'The others fail. (1): $x=5$, $y=-2$ gives $5^0=1$, but $x\\ne0$ and $y=-2$. (3): $x=-1$, $y=0$ gives $(-1)^2=1$, but $x\\ne0$ and $y=0$. (4): a power of 0 is never 1.'])
    S('q-291', stem='Given:\n$\\begin{cases} x>1,\\ y>1 \\\\ x^y=y^x \\\\ x=y^2 \\end{cases}$\n$y=?$', expl=[
        'Put $x=y^2$ into $x^y=y^x$: $(y^2)^y=y^{y^2}$, so $y^{2y}=y^{y^2}$.',
        'Same base ($y>1$), so the exponents are equal: $2y=y^2$. Since $y\\ne0$, divide by $y$: $y=2$.',
        'Check: $x=4$, and $4^2=16=2^4$ ✓.',
        'Faster: the choices are whole numbers, so $x=y^2$ is a whole number too. For two different positive whole numbers, $a^b=b^a$ only for 2 and 4 (topic 8). $y=4$ gives $x=16$, so $y=2$.'])
    S('q-292', stem='Given:\n$\\begin{cases} 5^x\\cdot5^y=125 \\\\ 2xy=4 \\end{cases}$\n$x^2+y^2=?$', expl=[
        '$5^x\\cdot5^y=5^{x+y}$ and $125=5^3$, so $x+y=3$.',
        '$(x+y)^2=x^2+y^2+2xy$: $9=x^2+y^2+4$, so $x^2+y^2=5$.',
        'There is no need to find $x$ and $y$ (for example, $x=1$ and $y=2$).'])
    S('q-293', expl=[
        'Four equal terms: $2^y+2^y+2^y+2^y=4\\cdot2^y=2^2\\cdot2^y=2^{y+2}$.',
        '$2^x=2^{y+2}$, so $x=y+2$ and $x-y=2$.',
        'Check with $y=1$: $2^x=2+2+2+2=8$, so $x=3$ and $x-y=2$ ✓.'])
    S('q-294', expl=[
        'Write the eighth root as a power: $\\sqrt[8]{2^4}=2^{\\frac48}=2^{\\frac12}=\\sqrt2$.',
        'Now every root is a square root. Top: $\\sqrt{\\frac12\\cdot40\\cdot2}=\\sqrt{40}$.',
        '$\\frac{\\sqrt{40}}{\\sqrt{10}}=\\sqrt{\\frac{40}{10}}=\\sqrt4=2$.'])
    S('q-295', expl=[
        '$\\sqrt{39}$ is a little more than $\\sqrt{36}=6$. $2\\pi\\approx2\\cdot3.14=6.28$.',
        '$\\sqrt{23}+\\sqrt5\\approx4.8+2.2=7$. $3\\sqrt5=\\sqrt{45}<\\sqrt{49}=7$.',
        'To be sure the sum is more than 7: $(\\sqrt{23}+\\sqrt5)^2=28+2\\sqrt{115}$, and $\\sqrt{115}>10.5$ (because $10.5^2=110.25$). The square is more than $28+21=49$.',
        'The largest is $\\sqrt{23}+\\sqrt5$.'])
    S('q-296', expl=[
        'Clear the root in the first denominator: $\\frac{3}{2\\sqrt2}\\cdot\\frac{\\sqrt2}{\\sqrt2}=\\frac{3\\sqrt2}{4}$.',
        'Now the denominators are the same: $\\frac{3\\sqrt2}{4}+\\frac{\\sqrt2}{4}=\\frac{4\\sqrt2}{4}=\\sqrt2$.'])
    S('q-297', stem='Given: $x>0$. $\\sqrt{x\\cdot\\sqrt{x}}=?$', choices=['$x$', '$\\sqrt{x}$', '$\\sqrt[3]{x}$', '$\\sqrt[4]{x^3}$'], expl=[
        'Bring $x$ inside the inner root: $x\\sqrt x=\\sqrt{x^2\\cdot x}=\\sqrt{x^3}$.',
        'A root of a root: multiply the indices. $\\sqrt{\\sqrt{x^3}}=\\sqrt[4]{x^3}$.',
        'With exponents: $x\\cdot x^{\\frac12}=x^{\\frac32}$, and the outer root halves the exponent: $x^{\\frac34}=\\sqrt[4]{x^3}$.',
        'Check with $x=16$: $\\sqrt{16\\cdot4}=\\sqrt{64}=8$, and $\\sqrt[4]{16^3}=2^3=8$ ✓.'])
    S('q-298', stem='Given:\n$\\begin{cases} a>0,\\ b>0 \\\\ a\\ne b \\end{cases}$\n$\\dfrac{a-b}{\\sqrt{a}-\\sqrt{b}}=?$', expl=[
        'Write the top as a difference of squares of roots: $a-b=(\\sqrt a-\\sqrt b)(\\sqrt a+\\sqrt b)$.',
        'Cancel $\\sqrt a-\\sqrt b$ (it is not 0, because $a\\ne b$). The result is $\\sqrt a+\\sqrt b$.',
        'Check with $a=4$, $b=1$: $\\frac{4-1}{2-1}=3$, and $\\sqrt4+\\sqrt1=3$ ✓.'])
    S('q-299', stem='How many solutions does the equation $\\sqrt{x}\\cdot(\\sqrt{x}-3)=0$ have?', expl=[
        'A product is 0 only when one of the factors is 0.',
        '$\\sqrt x=0$ gives $x=0$. $\\sqrt x-3=0$ gives $\\sqrt x=3$, so $x=9$.',
        'Both work, so there are 2 solutions. Do not divide by $\\sqrt x$: that loses $x=0$.'])
    S('q-300', stem='Given:\n$\\begin{cases} 2x+y=\\sqrt{108} \\\\ x-y=\\sqrt{27} \\end{cases}$\n$x=?$', expl=[
        'Simplify the roots: $\\sqrt{108}=\\sqrt{36}\\cdot\\sqrt3=6\\sqrt3$ and $\\sqrt{27}=\\sqrt9\\cdot\\sqrt3=3\\sqrt3$.',
        'Add the two equations to remove $y$: $3x=6\\sqrt3+3\\sqrt3=9\\sqrt3$, so $x=3\\sqrt3$.',
        'Quick check: $108=4\\cdot27$, so $\\sqrt{108}=2\\sqrt{27}$. Then $3x=3\\sqrt{27}$ and $x=\\sqrt{27}=3\\sqrt3$.'])
    S('q-301', stem='Given: $x^{-\\frac12}=4$. $x=?$', expl=[
        '$x^{-\\frac12}=\\frac1{\\sqrt x}$, so $\\frac1{\\sqrt x}=4$ and $\\sqrt x=\\frac14$. Square: $x=\\frac1{16}$.',
        'Or raise both sides to the reciprocal power, $-2$: $x=4^{-2}=\\frac1{16}$.',
        'Check: $\\left(\\frac1{16}\\right)^{-\\frac12}=16^{\\frac12}=4$ ✓.'])

    # --- practice ---
    S('q-302', stem='Given: $a>0$ and $b>0$. $\\sqrt{13a}\\cdot\\sqrt{13b}=?$', expl=[
        '$\\sqrt{13a}\\cdot\\sqrt{13b}=\\sqrt{169ab}=\\sqrt{169}\\cdot\\sqrt{ab}=13\\sqrt{ab}$.'])
    S('q-303', stem='The equation $(x^a)^a=x^a\\cdot x^a\\cdot x^a$ is true for every number $x$. Which of the following could be the value of $a$?', expl=[
        'Left: $(x^a)^a=x^{a^2}$. Right: $x^a\\cdot x^a\\cdot x^a=x^{3a}$.',
        'True for every $x$, so the exponents are equal: $a^2=3a$, $a(a-3)=0$, so $a=0$ or $a=3$.',
        '$a=0$ also solves $a^2=3a$, but it is not a choice. The answer is $3$. Check: $(x^3)^3=x^9=x^3\\cdot x^3\\cdot x^3$ ✓.'])
    S('q-304', stem='Given: $n>1$. $\\frac{3^n}{3n}=?$', expl=[
        'The bottom is $3^1\\cdot n$. Divide the powers of 3: $\\frac{3^n}{3^1}=3^{n-1}$. The $n$ stays at the bottom: $\\frac{3^{n-1}}{n}$.',
        'Check with $n=2$: $\\frac{9}{6}=\\frac32$, and $\\frac{3^1}{2}=\\frac32$ ✓. The other choices give $\\frac12$, $1$ and $\\frac12$.'])
    S('q-305', expl=[
        'Split the top: $10^x=2^x\\cdot5^x$.',
        '$\\frac{2^x}{2^{x+1}}=2^{-1}=\\frac12$ and $\\frac{5^x}{5^{x-1}}=5^1=5$. The result is $\\frac12\\cdot5=\\frac52$.',
        'Check with $x=1$: $\\frac{10}{2^2\\cdot5^0}=\\frac{10}4=\\frac52$. Choices (3) and (4) both give $\\frac52$, so try $x=2$: $\\frac{100}{2^3\\cdot5}=\\frac{100}{40}=\\frac52$, while $\\frac{5^2}{2^2}=\\frac{25}4$. Choice (3).'])
    S('q-306', stem='Given: $a$ and $c$ are integers, and\n$\\begin{cases} 0<a<c \\\\ a^c=c^a \\end{cases}$\n$c-a=?$', expl=[
        'For two different positive integers, $a^c=c^a$ only for 2 and 4 (topic 8): $2^4=16=4^2$.',
        '$a=2$ and $c=4$, so $c-a=2$.',
        'Numbers that are not whole have other pairs, for example $\\frac94$ and $\\frac{27}8$. That is why the question says "integers".'])
    S('q-307', expl=['Area $=$ side², so side $=\\sqrt{\\sqrt5}$.',
                     '$\\sqrt{\\sqrt5}=\\left(5^{\\frac12}\\right)^{\\frac12}=5^{\\frac14}$.'])
    S('q-308', expl=['$\\sqrt{18}=\\sqrt9\\cdot\\sqrt2=3\\sqrt2$.',
                     'Top: $3\\sqrt2+\\sqrt2=4\\sqrt2$. Bottom: $3\\sqrt2-\\sqrt2=2\\sqrt2$.',
                     '$\\frac{4\\sqrt2}{2\\sqrt2}=2$.'])
    S('q-309', expl=['Inside: $3\\sqrt3=3^1\\cdot3^{\\frac12}=3^{\\frac32}$.',
                     'The outer root halves the exponent: $\\left(3^{\\frac32}\\right)^{\\frac12}=3^{\\frac34}$.'])
    S('q-310', stem='Given: $a\\ge0$ and $b\\ge0$. When is $\\sqrt{a}+\\sqrt{b}=\\sqrt{a+b}$ true?',
      choices=['Only when $a-b=0$', 'Only when $ab>0$', 'Only when $a=0$ or $b=0$', 'Always'], correct=3, expl=[
        'Both sides are not negative, so square them: $(\\sqrt a+\\sqrt b)^2=a+b+2\\sqrt{ab}$ and $(\\sqrt{a+b})^2=a+b$.',
        'They are equal only when $2\\sqrt{ab}=0$, that is $ab=0$: $a=0$ or $b=0$.',
        'Check: $a=4$, $b=9$: $2+3=5$, but $\\sqrt{13}\\ne5$. $a=0$, $b=9$: $0+3=3=\\sqrt9$ ✓.'])
    S('q-311', stem='$3^n-3^{n-1}=?$', expl=[
        'Take out the smaller power: $3^n=3\\cdot3^{n-1}$, so $3^n-3^{n-1}=3^{n-1}(3-1)=2\\cdot3^{n-1}$.',
        'Check with $n=1$: $3-1=2$, and $2\\cdot3^0=2$ ✓. The other choices give $\\frac13$, $3$ and $1$.'])
    S('q-312', stem='Given: $a^b=-1$. Which of the following is necessarily true?',
      choices=['$a=-1$', '$a=-b^2$', '$a=b-1$', '$a=\\sqrt[3]{b}$'], expl=[
        '$a=-1$ is the only base whose power can be $-1$. A positive base gives a positive power, and 0 gives 0. Any other negative base gives a power whose size is not 1 (or exactly $+1$ when the exponent is 0).',
        'The exponent can change: $(-1)^3=-1$ and $(-1)^{\\frac13}=\\sqrt[3]{-1}=-1$. But $a$ is always $-1$.',
        'The other choices are not necessarily true: with $b=3$, $-b^2=-9$, $b-1=2$ and $\\sqrt[3]3\\ne-1$.'])
    S('q-313', stem='Which of the following ratios is not equal to the ratio $3:\\sqrt{3}$?',
      choices=['$\\sqrt{3}:1$', '$\\sqrt{27}:3$', '$9:\\sqrt{27}$', '$81:\\sqrt{81}$'], expl=[
        'The ratio $3:\\sqrt3$ has the value $\\frac3{\\sqrt3}=\\sqrt3$.',
        '(1) $\\frac{\\sqrt3}{1}=\\sqrt3$ ✓. (2) $\\frac{\\sqrt{27}}{3}=\\frac{3\\sqrt3}{3}=\\sqrt3$ ✓. (3) $\\frac9{\\sqrt{27}}=\\frac9{3\\sqrt3}=\\frac3{\\sqrt3}=\\sqrt3$ ✓.',
        '(4) $\\frac{81}{\\sqrt{81}}=\\frac{81}9=9\\ne\\sqrt3$. This ratio is not equal.'])
    S('q-314', expl=[
        'Multiply the tops and the bottoms. Top: $(x-y)(x+y)=x^2-y^2=-(y^2-x^2)$. Bottom: $\\sqrt{y+x}\\cdot\\sqrt{y-x}=\\sqrt{y^2-x^2}$.',
        '$\\frac{-(y^2-x^2)}{\\sqrt{y^2-x^2}}=-\\sqrt{y^2-x^2}$, because a positive number over its root is its root.',
        'Check with $x=3$, $y=5$: $\\frac{-2}{\\sqrt8}\\cdot\\frac{8}{\\sqrt2}=\\frac{-16}{4}=-4$, and $-\\sqrt{25-9}=-4$ ✓.'])
    S('q-315', stem='Given: $\\left(\\frac{3^{2b}}{3^x}\\right)^x=3^{b^2}$. $x=?$', choices=['$2$', '$b$', '$2b$', '$b^2$'], expl=[
        'Inside: $\\frac{3^{2b}}{3^x}=3^{2b-x}$. Power of a power: $3^{x(2b-x)}=3^{2bx-x^2}$.',
        'Equal exponents: $2bx-x^2=b^2$, so $x^2-2bx+b^2=0$, that is $(x-b)^2=0$ and $x=b$.'])
    S('q-316', expl=[
        '$\\frac{\\sqrt2\\cdot\\sqrt5}{2}=\\frac{\\sqrt{10}}{\\sqrt4}=\\sqrt{\\frac{10}4}=\\sqrt{\\frac52}=\\left(\\frac52\\right)^{\\frac12}$.',
        'Same base, so the exponents are equal: $3x=\\frac12$ and $x=\\frac16$.'])
    S('q-317', choices=['$\\frac{4}{3}$', '$\\frac{2}{3}$', '$\\frac{2}{6}$', '$\\frac{1}{6}$'], expl=[
        'Write everything with primes: $36^2=(6^2)^2=6^4$, so the top is $6^4\\cdot6^4=6^8=2^8\\cdot3^8$.',
        '$\\frac{2^8\\cdot3^8}{3^9\\cdot2^7}=2^{8-7}\\cdot3^{8-9}=2\\cdot3^{-1}=\\frac23$.'])
    S('q-318', stem='Given: $y$ is an integer, and\n$\\begin{cases} x>0,\\ y>0 \\\\ x^{3y}=x^y \\end{cases}$\n$y^x=?$',
      choices=['$y$', '$\\frac{1}{y}$', '$\\frac{1}{y^2}$', '$y^2$'], expl=[
        'If $x\\ne1$: same base, so $3y=y$ and $y=0$. But $y>0$, so this is impossible.',
        'Therefore $x=1$ (and $1^{3y}=1=1^y$ ✓). Then $y^x=y^1=y$.'])
    S('q-319', expl=[
        '$\\sqrt x=\\frac{4^{-2}}2=\\frac1{16\\cdot2}=\\frac1{32}$. Square: $x=\\frac1{1024}$.',
        '$4^5=1024$, so $x=4^{-5}$.',
        'With powers of 4 only: $2=4^{\\frac12}$, so $\\sqrt x=4^{-2}\\cdot4^{-\\frac12}=4^{-\\frac52}$ and $x=\\left(4^{-\\frac52}\\right)^2=4^{-5}$.'])
    S('q-320', expl=['Take out the smaller power: $5^4-5^3=5^3(5-1)=4\\cdot5^3$.',
                     '$\\frac{4\\cdot5^3}{4}=5^3$, and $(5^3)^2=5^6$.'])
    S('q-321', stem='Given:\n$\\begin{cases} n\\ne0 \\\\ x>1 \\end{cases}$\n$\\frac{x^n-x^{\\frac{2n}{3}}}{x^{\\frac{n}{3}}-1}=?$', expl=[
        'Take out the smaller power on top: $x^n=x^{\\frac{2n}3}\\cdot x^{\\frac n3}$, so $x^n-x^{\\frac{2n}3}=x^{\\frac{2n}3}\\left(x^{\\frac n3}-1\\right)$.',
        'Cancel $x^{\\frac n3}-1$ (it is not 0, because $x>1$ and $n\\ne0$). The result is $x^{\\frac{2n}3}$.',
        'Check with $n=3$, $x=2$: $\\frac{8-4}{2-1}=4$, and $2^2=4$ ✓. The other choices give $7$, $8$ and $1$.'])

    # extra set: keep 3 as a warm-up (the other 4 repeat T10's extra set), NITE-style stems
    S('alg-extra-unit-t11-3-2', stem='$216^{\\frac23}=?$', choices=['$108$', '$36$', '$6$', '$12$'],
      expl=['$216^{\\frac23}=\\left(\\sqrt[3]{216}\\right)^2=6^2=36$.'])
    S('alg-extra-unit-t11-3-4', stem='$5^{-3}+5^{-2}=?$',
      expl=['$5^{-3}=\\frac1{125}$ and $5^{-2}=\\frac1{25}=\\frac5{125}$.', '$\\frac1{125}+\\frac5{125}=\\frac6{125}$.'])
    S('alg-extra-unit-t11-3-7', stem='$\\sqrt{128}+\\sqrt{50}=?$',
      expl=['$\\sqrt{128}=\\sqrt{64}\\cdot\\sqrt2=8\\sqrt2$ and $\\sqrt{50}=\\sqrt{25}\\cdot\\sqrt2=5\\sqrt2$.',
            '$8\\sqrt2+5\\sqrt2=13\\sqrt2$ (not $\\sqrt{178}$: roots do not add under one root).'])
    # Pass 2: the other four extras are original items and come back (text clean-up only)
    S('alg-extra-unit-t11-3-1', stem='$\\frac{5^9}{5^6}=?$', choices=['$5$', '$25$', '$625$', '$125$'],
      expl=['Same base: subtract the exponents. $\\frac{5^9}{5^6}=5^{9-6}=5^3=125$.'])
    S('alg-extra-unit-t11-3-3', stem='Given: $3^{x+1}=3^7$. $x=?$', choices=['$18$', '$6$', '$5$', '$7$'],
      expl=['Same base, so the exponents are equal: $x+1=7$, so $x=6$.'])
    S('alg-extra-unit-t11-3-5', stem='Given: $x\\ne0$. $\\frac{(5x)^3}{25x^2}=?$', choices=['$x$', '$125x$', '$5x$', '$5x^2$'],
      expl=['$(5x)^3=5^3\\cdot x^3=125x^3$.', '$\\frac{125x^3}{25x^2}=\\frac{125}{25}\\cdot x^{3-2}=5x$.'])
    S('alg-extra-unit-t11-3-6', stem='Which is greater: $2^{16}$ or $4^7$?',
      expl=['Same base: $4^7=(2^2)^7=2^{14}$.', '$2^{16}>2^{14}$, so the first power, $2^{16}$, is greater.'])

    # =====================================================================================
    # 5. New Section B lesson: the tools the solution videos used without teaching
    # =====================================================================================
    sb = ['Root of a root', 'Undo a power', 'Conjugates', 'Product = 0', '"Or" claims', 'Recap']
    v = M.new_video(TOOLS, TOPIC, 'Advanced Tools — Roots & Powers', sb, [
        dict(mode='title', title='Advanced Tools — Roots & Powers', script=[
            "Section B uses a few tools we haven't used yet. Here they are, one by one.",
            "The basics are in topics eight, nine and ten: sums of powers, comparing powers, numbers between zero and one. Look back if you need them.",
        ]),
        dict(mode='concept', active=0, title='Root of a root', script=[
            "Tool one: a root inside a root.",
            A('√√x = ⁴√x appears', T('$\\sqrt{\\sqrt{x}}=\\sqrt[4]{x}$', size=60, gap=40)),
            "Just like a power of a power — multiply. Here we multiply the indices. Two times two: a fourth root.",
            A('√(x√x) appears', T('$\\sqrt{x\\sqrt{x}}$ $\\quad(x>0)$', size=56, gap=40)),
            "A number in front of the inner root? Bring it inside first. It goes in squared.",
            D('Write "x√x = √(x² · x) = √(x³)"'),
            "x squared times x: x cubed.",
            D('Write "√(√(x³)) = ⁴√(x³)"'),
            "Now it's a root of a root: the fourth root of x cubed.",
            "Or use exponents: x times x to the half is x to the three halves. The outer root halves it: x to the three quarters. Same thing.",
        ]),
        dict(mode='concept', active=1, title='Undo a power', script=[
            "Tool two: x has a strange power, and you want x alone.",
            A('x^(−1/2) = 4 appears', T('$x^{-\\frac12}=4$', size=60, gap=40)),
            "Raise both sides to the reciprocal power. Minus a half, times what, is one? Minus two.",
            D('Write "(x^(−1/2))^(−2) = 4^(−2)  →  x = 1/16"'),
            "Power of a power: minus a half times minus two is one. So x is four to the minus two: one sixteenth.",
            D('Write "check: (1/16)^(−1/2) = 16^(1/2) = 4 ✓"'),
            "Check it: the minus flips one sixteenth to sixteen. Sixteen to the half: four. It works.",
            A('x^(2/3) = 9 appears', T('$x^{\\frac23}=9,\\ x>0\\ \\Rightarrow\\ x=9^{\\frac32}=27$', size=46)),
            "Same move here: raise both sides to three halves. Nine to the three halves: root nine is three, and three cubed is twenty-seven.",
        ]),
        dict(mode='concept', active=2, title='Conjugates', script=[
            "Tool three: the difference of squares — with roots.",
            A('a − b = (√a − √b)(√a + √b) appears', T('$a-b=(\\sqrt a-\\sqrt b)(\\sqrt a+\\sqrt b)$', size=48)),
            "For a and b that aren't negative: a minus b is root a minus root b, times root a plus root b.",
            "You met this in topic nine. Here we use it both ways.",
            A('(a − b)/(√a − √b) appears', T('$\\dfrac{a-b}{\\sqrt a-\\sqrt b}=\\sqrt a+\\sqrt b$', size=48)),
            "Way one: split the top — then cancel with the bottom.",
            A('1/(√5 − 2) appears', T('$\\dfrac{1}{\\sqrt5-2}=\\dfrac{\\sqrt5+2}{(\\sqrt5-2)(\\sqrt5+2)}=\\dfrac{\\sqrt5+2}{5-4}=\\sqrt5+2$', size=40)),
            "Way two: a root difference at the bottom? Multiply the top and the bottom by the same pair — with a plus.",
            "The bottom becomes five minus four: one. The pair with the other sign is called the conjugate.",
        ]),
        dict(mode='concept', active=3, title='Product = 0', script=[
            "Tool four: an equation that is already a product equal to zero.",
            A('√x(√x − 3) = 0 appears', T('$\\sqrt{x}\\cdot(\\sqrt{x}-3)=0$', size=56, gap=40)),
            "A product is zero only when one of the factors is zero.",
            D('Write "√x = 0 → x = 0" and "√x = 3 → x = 9"'),
            "Root x is zero, or root x is three. So x is zero or nine.",
            A("'Never divide by √x' appears", T('Never divide by $\\sqrt{x}$ — it can be $0$', size=46)),
            "Don't divide both sides by root x. It can be zero — and then you lose the answer x equals zero.",
        ]),
        dict(mode='concept', active=4, title='"Or" claims', script=[
            "Tool five: answer choices with the word \"or\".",
            A('when a power is 1 appears', T('$a^b=1$: base $1$; base $-1$, $b$ even; $b=0$, $a\\ne0$', size=40)),
            "First, from topic eight: when is a power equal to one? Base one. Base minus one with an even exponent. Or exponent zero — with a base that isn't zero.",
            A("'A or B' rule appears", T('"A or B" is necessarily true: every allowed case makes A or B true', size=38)),
            "Now the logic. \"A or B\" is necessarily true if in every allowed case, at least one of the two parts is true.",
            A("'To kill it' appears", T('To kill it: one allowed case where A and B are both false', size=38)),
            "To kill it, find one allowed case where both parts are false.",
            D('Write "a ≠ 1, aᵇ = 1  →  b = 0 or a = −1"'),
            "Example: a isn't one, and a to the b is one. Then b is zero — or a is minus one. Every case gives one of the two. So that \"or\" claim is necessarily true.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            "Let's lock it in.",
            A("'Root of a root: multiply the indices' appears", T('Root of a root: multiply the indices', size=42)),
            A("'Undo a power: raise to the reciprocal' appears", T('Undo a power: raise to the reciprocal power', size=42)),
            A("'Conjugates' appears", T('$a-b=(\\sqrt a-\\sqrt b)(\\sqrt a+\\sqrt b)$', size=42)),
            A("'Product = 0' appears", T('Product $=0$: each factor $=0$. Never divide by $\\sqrt x$', size=42)),
            A("'Or claims' appears", T('"A or B": kill it with one case where both are false', size=42)),
            D('Tick each line'),
            "Eleven questions next. Try each one first — then watch its solution.",
        ]),
    ], 'power-b', before='q-294')
    v['hybrid']['num'] = 31

    # =====================================================================================
    # 6. New guided questions (Section B) + move Q3 (needs "or" logic) to the end of Section B
    # =====================================================================================
    g1 = 'q-r26-t11-01'
    M.new_q(g1, TOPIC, '$\\dfrac{1}{\\sqrt5-2}-\\dfrac{1}{\\sqrt5+2}=?$', ['$0$', '$-4$', '$2\\sqrt5$', '$4$'], 4, [
        'The key product: $(\\sqrt5-2)(\\sqrt5+2)=5-4=1$.',
        'So $\\frac1{\\sqrt5-2}=\\frac{\\sqrt5+2}{1}=\\sqrt5+2$ and $\\frac1{\\sqrt5+2}=\\frac{\\sqrt5-2}{1}=\\sqrt5-2$.',
        '$(\\sqrt5+2)-(\\sqrt5-2)=4$.',
        'Estimate to check: $\\sqrt5\\approx2.24$, so $\\frac1{0.24}-\\frac1{4.24}\\approx4.2-0.24\\approx4$. ($2\\sqrt5\\approx4.5$ is the trap: it adds instead of subtracting.)'])
    M.place_q(g1, 'power-b', after='solve-q-298')
    _solution(M, g1, ["Two fractions with a root difference at the bottom. Call in the conjugates."], [
        ('Method 1 · Conjugates', [
            "Clear each denominator with its conjugate.",
            D('Write "(√5 − 2)(√5 + 2) = 5 − 4 = 1"'),
            "First, the key product: root five minus two, times root five plus two. Root five squared is five, minus four: one.",
            D('Write "1/(√5 − 2) = (√5 + 2)/1 = √5 + 2"'),
            "So for one over root five minus two, multiply the top and the bottom by root five plus two. The bottom is one. It's just root five plus two.",
            D('Write "1/(√5 + 2) = (√5 − 2)/1 = √5 − 2"'),
            "Same for the second fraction: root five minus two.",
            D('Write "(√5 + 2) − (√5 − 2) = 4"'),
            "Now subtract. Root five minus root five is gone. Two minus minus two: four.",
            D('Circle choice 4'),
            "Choice four. Choice three is the trap — it adds the roots instead of subtracting them.",
        ]),
        ('Method 2 · Estimate', [
            "No time? Estimate.",
            D('Write "√5 ≈ 2.24"'),
            "Root five is about two point two four.",
            D('Write "1/0.24 ≈ 4.2" and "1/4.24 ≈ 0.24"'),
            "First fraction: one over zero point two four — about four point two. Second: one over four point two four — about zero point two four.",
            D('Write "4.2 − 0.24 ≈ 4"'),
            "The difference is about four. Two root five is about four point five — too big. Choice four.",
        ]),
    ])

    g2 = 'q-r26-t11-02'
    M.new_q(g2, TOPIC, 'Given:\n$\\begin{cases} x>0 \\\\ \\sqrt[3]{x\\sqrt{x}}=2 \\end{cases}$\n$x=?$', ['$2$', '$4$', '$8$', '$64$'], 2, [
        'Write the roots as powers: $x\\sqrt x=x^1\\cdot x^{\\frac12}=x^{\\frac32}$.',
        'The cube root is the power $\\frac13$: $\\left(x^{\\frac32}\\right)^{\\frac13}=x^{\\frac12}=\\sqrt x$.',
        '$\\sqrt x=2$, so $x=4$.',
        'Check: $4\\cdot\\sqrt4=8$ and $\\sqrt[3]8=2$ ✓. ($8$ is the trap: it is the value of $x\\sqrt x$, not of $x$.)'])
    M.place_q(g2, 'power-b', after='solve-q-301')
    _solution(M, g2, ["A cube root over a square root. Turn them all into powers."], [
        ('Method 1 · Exponents', [
            "Write every root as a power.",
            D('Write "x√x = x¹ · x^(1/2) = x^(3/2)"'),
            "x times root x: x to the one, times x to the half. Add the exponents: x to the three halves.",
            D('Write "∛(x^(3/2)) = x^(3/2 · 1/3) = x^(1/2)"'),
            "The cube root is the power one third. Three halves times one third: one half.",
            D('Write "√x = 2 → x = 4"'),
            "So root x is two. x is four.",
            D('Circle choice 2'),
            "Choice two. Choice three, eight, is the trap — that's x root x, not x.",
        ]),
        ('Method 2 · Try the choices', [
            "Or try the choices. The number under the cube root must come out as a perfect cube.",
            D('Next to choice 2 write "4 · √4 = 8 → ∛8 = 2 ✓"'),
            "x equals four: four times root four is eight. The cube root of eight is two. It works.",
            "One choice works — that's enough. Choice two.",
        ]),
    ])

    # Q3 needs "when is a power 1" + "or" logic -> after the tools lesson, at the end of Section B
    M.move('q-290', 'power-b', after='solve-' + g2)
    M.move('solve-q-290', 'power-b', after='q-290')
    v290 = M.video('solve-q-290')
    v290['hybrid']['title'] = GROUP_B; v290['hybrid']['num'] = 31
    v290['beats'][0]['title'] = GROUP_B
    M.edit_lines('solve-q-290', 1, lambda ls: ls + [
        {'say': "It uses two tools from the start of this section: when a power is one, and \"or\" claims."}])

    # one sidebar for every guided solution video (renumber_guided reorders it)
    for f in [f for f in M.D['flow'] if f['topic'] == TOPIC and f['type'] == 'video']:
        vv = M.video(f['ref'])
        if vv.get('kind') == 'solution':
            M.set_sidebar(f['ref'], QSIDEBAR)
    for qid in ['q-290', 'q-291', 'q-292', 'q-297', 'q-298', 'q-299', 'q-300', 'q-301']:
        _sync(M, qid)

    # =====================================================================================
    # 7. Memory card (the topic had none)
    # =====================================================================================
    M.new_card('mem-r26-t11-advanced', TOPIC, 'power-b', {
        'title': 'Advanced exponents and roots',
        'intro': 'The tools of this topic. The rules from topics 8 to 10 are in the second table.',
        'tables': [
            {'title': 'Tools', 'head': ['Situation', 'Method', 'Example'], 'rows': [
                ['Root of a root', 'multiply the indices', '$\\sqrt{\\sqrt[3]{x}}=\\sqrt[6]{x}$'],
                ['A factor in front of an inner root', 'bring it inside first (squared)', '$\\sqrt{x\\sqrt x}=\\sqrt{\\sqrt{x^3}}=\\sqrt[4]{x^3}$'],
                ['$x$ with a fractional power', 'raise both sides to the reciprocal power', '$x^{-\\frac12}=4\\Rightarrow x=4^{-2}=\\frac1{16}$'],
                ['$a-b$ over $\\sqrt a-\\sqrt b$', 'split the top', '$\\frac{a-b}{\\sqrt a-\\sqrt b}=\\sqrt a+\\sqrt b$'],
                ['Root difference at the bottom', 'multiply by the conjugate', '$\\frac1{\\sqrt5-2}=\\frac{\\sqrt5+2}{5-4}=\\sqrt5+2$'],
                ['Product $=0$', 'each factor $=0$; never divide by $\\sqrt x$', '$\\sqrt x(\\sqrt x-3)=0\\Rightarrow x=0$ or $x=9$'],
                ['Power $=1$', 'base 1; base $-1$ with an even exponent; exponent 0 (base $\\ne0$)', '$x^{y+2}=1$, $x\\ne1\\Rightarrow y=-2$ or $x=-1$'],
                ['"A or B" necessarily true?', 'look for one allowed case where both are false', '$x=5$, $y=-2$ kills "$x=0$ or $y\\ne-2$"'],
                ['$a^b=b^a$, different positive whole numbers', 'only 2 and 4', '$2^4=4^2=16$'],
            ]},
            {'title': 'From topics 8 to 10', 'head': ['Topic', 'Tool', 'Example'], 'rows': [
                ['8, 10', 'equal powers added: count the copies', '$2^x+2^x=2^{x+1}$'],
                ['8, 9', 'between 0 and 1', '$x^3<x^2<x<\\sqrt x$'],
                ['9', 'different roots: raise to a common power', '$\\sqrt2$ vs $\\sqrt[3]3$: $8<9$'],
                ['9', 'square of a sum of roots', '$(\\sqrt a+\\sqrt b)^2=a+b+2\\sqrt{ab}$'],
                ['10', 'power equation: same base, then equal exponents', '$4^x=8^{x-1}\\Rightarrow2x=3x-3\\Rightarrow x=3$'],
            ]},
        ],
        'tips': [
            'Two routes for every question: the laws, or plug in a number / try the choices.',
            'Before you trust one number, check that the choices give different values. If two match, try another number.',
            '$\\sqrt a+\\sqrt b\\ne\\sqrt{a+b}$ (unless $a=0$ or $b=0$).',
            'Estimate roots with perfect squares: $\\sqrt{39}$ is a little more than $\\sqrt{36}=6$.',
        ]}, after='solve-q-290')

    # =====================================================================================
    # 8. New practice questions (exam level)
    # =====================================================================================
    P = {}
    P['04'] = ('$\\frac{2}{\\sqrt7+\\sqrt5}=?$', ['$\\sqrt7+\\sqrt5$', '$2(\\sqrt7-\\sqrt5)$', '$\\sqrt7-\\sqrt5$', '$\\frac{\\sqrt7-\\sqrt5}{2}$'], 3, [
        'Multiply the top and the bottom by the conjugate $\\sqrt7-\\sqrt5$.',
        'Bottom: $(\\sqrt7+\\sqrt5)(\\sqrt7-\\sqrt5)=7-5=2$.',
        '$\\frac{2(\\sqrt7-\\sqrt5)}{2}=\\sqrt7-\\sqrt5$.'])
    P['05'] = ('Given: $9^x\\cdot27^x=\\frac13$. $x=?$', ['$\\frac15$', '$-\\frac15$', '$-\\frac16$', '$-5$'], 2, [
        'Same base 3: $9^x=3^{2x}$, $27^x=3^{3x}$ and $\\frac13=3^{-1}$.',
        '$3^{2x}\\cdot3^{3x}=3^{5x}$ (add the exponents), so $5x=-1$ and $x=-\\frac15$.',
        '$-\\frac16$ is the trap: it multiplies the exponents ($2\\cdot3=6$) instead of adding them.'])
    P['06'] = ('Given:\n$\\begin{cases} a>0,\\ b>0 \\\\ a+b=10 \\\\ ab=9 \\end{cases}$\n$\\sqrt a+\\sqrt b=?$', ['$\\sqrt{10}$', '$4$', '$16$', '$\\sqrt{19}$'], 2, [
        'Square the sum: $(\\sqrt a+\\sqrt b)^2=a+b+2\\sqrt{ab}=10+2\\sqrt9=10+6=16$.',
        '$\\sqrt a+\\sqrt b$ is positive, so it is $\\sqrt{16}=4$.',
        'Check: $a=1$, $b=9$ fit the givens, and $\\sqrt1+\\sqrt9=4$ ✓. ($\\sqrt{10}$ is the trap $\\sqrt a+\\sqrt b=\\sqrt{a+b}$.)'])
    P['08'] = ('Given: $0<x<1$. Which of the following is the largest?', ['$\\sqrt[3]{x}$', '$x^{-\\frac12}$', '$x^{-2}$', '$x^3$'], 3, [
        'Choose a number between 0 and 1: $x=\\frac14$.',
        '$\\sqrt[3]{\\frac14}<1$, $\\left(\\frac14\\right)^{-\\frac12}=4^{\\frac12}=2$, $\\left(\\frac14\\right)^{-2}=4^2=16$, $\\left(\\frac14\\right)^3=\\frac1{64}$.',
        'The largest is $x^{-2}$. This is true for every $0<x<1$: a negative exponent flips $x$ to $\\frac1x>1$, and a bigger power of a number above 1 is bigger.'])
    P['09'] = ('Given:\n$\\begin{cases} a\\ne1 \\\\ a^b=1 \\end{cases}$\nWhich of the following is necessarily true?',
               ['$b=0$', '$a=-1$', '$b=0$ or $a=-1$', '$a=-1$ and $b$ is even'], 3, [
        'A power equals 1 when the base is 1 (not allowed here), when the base is $-1$ and the exponent is even, or when the exponent is 0 (base not 0).',
        'Every allowed case has $b=0$ or $a=-1$, so choice (3) is necessarily true.',
        'The others fail: $a=-1$, $b=2$ kills (1). $a=5$, $b=0$ kills (2) and (4).'])
    P['10'] = ('Given: $x\\sqrt{x}=4\\sqrt{x}$. Which of the following gives all the possible values of $x$?',
               ['$4$ only', '$16$ only', '$0$ or $4$', '$0$ or $16$'], 3, [
        'Do not divide by $\\sqrt x$ — it can be 0. Move everything to one side and factor: $x\\sqrt x-4\\sqrt x=\\sqrt x(x-4)=0$.',
        'A product is 0 when a factor is 0: $\\sqrt x=0$, so $x=0$; or $x-4=0$, so $x=4$.',
        'Check: $x=0$: $0=0$ ✓. $x=4$: $4\\cdot2=8=4\\cdot2$ ✓.'])
    P['11'] = ('$\\frac{1}{1+\\sqrt2}+\\frac{1}{\\sqrt2+\\sqrt3}+\\frac{1}{\\sqrt3+2}=?$', ['$\\sqrt3-1$', '$1$', '$3$', '$2+\\sqrt3$'], 2, [
        'Clear each denominator with its conjugate. The two numbers under the roots differ by 1 each time, so each bottom becomes 1:',
        '$\\frac1{1+\\sqrt2}=\\frac{\\sqrt2-1}{2-1}=\\sqrt2-1$, $\\frac1{\\sqrt2+\\sqrt3}=\\sqrt3-\\sqrt2$, $\\frac1{\\sqrt3+2}=\\frac{2-\\sqrt3}{4-3}=2-\\sqrt3$.',
        'Add: $(\\sqrt2-1)+(\\sqrt3-\\sqrt2)+(2-\\sqrt3)=2-1=1$.'])
    P['12'] = ('$\\sqrt{2\\sqrt{2\\sqrt{2}}}=?$', ['$2^{\\frac78}$', '$2^{\\frac34}$', '$2^{\\frac{15}{16}}$', '$\\sqrt[8]{2}$'], 1, [
        'Work from the inside out with exponents. $2\\sqrt2=2^1\\cdot2^{\\frac12}=2^{\\frac32}$.',
        '$2\\sqrt{2^{\\frac32}}=2^1\\cdot2^{\\frac34}=2^{\\frac74}$.',
        '$\\sqrt{2^{\\frac74}}=2^{\\frac78}$.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t11-' + k, TOPIC, stem, ch, cor, ex)
        M.place_q('q-r26-t11-' + k, 'unit-t11-3')

    # =====================================================================================
    # 9. Practice order: warm-up first, easy -> hard
    # =====================================================================================
    M.practice_order('unit-t11-3', [
        'alg-extra-unit-t11-3-1', 'alg-extra-unit-t11-3-3', 'alg-extra-unit-t11-3-2', 'alg-extra-unit-t11-3-4',
        'alg-extra-unit-t11-3-5', 'alg-extra-unit-t11-3-6', 'alg-extra-unit-t11-3-7',
        'q-302', 'q-304', 'q-311', 'q-320', 'q-305', 'q-317', 'q-308', 'q-307', 'q-309', 'q-313',
        'q-306', 'q-r26-t11-04', 'q-316', 'q-319', 'q-r26-t11-05', 'q-303', 'q-312',
        'q-318', 'q-315', 'q-314', 'q-321', 'q-310', 'q-r26-t11-06', 'q-r26-t11-10', 'q-r26-t11-12',
        'q-r26-t11-08', 'q-r26-t11-09', 'q-r26-t11-11'])

    add_summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last


# ------------------------------------------------------------------ Pass 2: summary video before the practice
def add_summary(M):
    sb = ['Translate first', 'Hidden formulas', 'Root of a root', 'Undo a power', 'Conjugates',
          'Product = 0', 'Power = 1 and "or"', 'Two routes', 'Before you practice']
    C = lambda i, title, script: dict(title=title, mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice, let's review the whole topic in three minutes.",
            "Every tool, every trap. Short and fast."]),
        C(0, 'Translate first', [
            "Before any arithmetic — translate.",
            A('Prime bases', T('Big power $\\to$ prime bases: $49^3=(7^2)^3=7^6$', size=44)),
            "A big power? Break the base into primes. Equal bases start cancelling.",
            A('Fractional exponent', T('Nested root $\\to$ fractional exponent: $\\sqrt{\\sqrt5}=5^{\\frac14}$', size=44)),
            "A root inside a root? Turn it into a fractional exponent.",
            "Don't compute giant numbers just because you can."]),
        C(1, 'Hidden formulas', [
            "Some questions hide a pattern you already know.",
            A('(x+y)²', T('$(x+y)^2=x^2+y^2+2xy$', size=48)),
            "You know x plus y and x times y? Build x squared plus y squared directly. No need to find x and y.",
            A('2 and 4', T('Different positive whole numbers: $a^b=b^a$ only for $2$ and $4$', size=40)),
            "a to the b equals b to the a: only two and four — and only for whole numbers.",
            A('Copies', T('$3^y+3^y+3^y=3\\cdot3^y=3^{y+1}$', size=46)),
            "Equal powers added? Count the copies."]),
        C(2, 'Root of a root', [
            "A root inside a root: multiply the indices.",
            A('Root of a root', T('$\\sqrt{\\sqrt{x}}=\\sqrt[4]{x}$', size=54)),
            "Two times two: a fourth root.",
            A('Factor inside', T('$\\sqrt{x^2\\sqrt x}=\\sqrt{\\sqrt{x^5}}=\\sqrt[4]{x^5}$', size=50)),
            "A factor in front of the inner root? Bring it inside first — squared."]),
        C(3, 'Undo a power', [
            "x has a strange power, and you want x alone?",
            A('Reciprocal power', T('$x^{-\\frac12}=5\\ \\Rightarrow\\ x=5^{-2}=\\frac1{25}$', size=52)),
            "Raise both sides to the reciprocal power. Minus a half times minus two is one.",
            "Then check it: one twenty-fifth to the minus a half is twenty-five to the half. Five. It works."]),
        C(4, 'Conjugates', [
            "The difference of squares, with roots.",
            A('Conjugates', T('$a-b=(\\sqrt a-\\sqrt b)(\\sqrt a+\\sqrt b)$', size=50)),
            "a minus b over root a minus root b? Split the top and cancel.",
            A('Clear the bottom', T('$\\dfrac{1}{\\sqrt{10}-3}=\\dfrac{\\sqrt{10}+3}{10-9}=\\sqrt{10}+3$', size=48)),
            "A root difference at the bottom? Multiply the top and the bottom by the conjugate."]),
        C(5, 'Product = 0', [
            "An equation that is already a product equal to zero:",
            A('Product = 0', T('$\\sqrt{x}\\cdot(\\sqrt{x}-5)=0\\ \\Rightarrow\\ x=0$ or $x=25$', size=48)),
            "Each factor can be zero. Root x is zero, or root x is five.",
            A('Never divide', T('Never divide by $\\sqrt{x}$ — it can be $0$', size=46)),
            "Never divide by root x. You lose x equals zero."]),
        C(6, 'Power = 1 and "or"', [
            "When is a power equal to one?",
            A('Power = 1', T('$a^b=1$: base $1$; base $-1$, $b$ even; $b=0$, $a\\ne0$', size=42)),
            "Base one. Base minus one with an even exponent. Or exponent zero — with a base that isn't zero.",
            A('Or claims', T('"A or B" is killed by one allowed case where both are false', size=40)),
            "An \"or\" claim is necessarily true if every allowed case makes one part true. To kill it, find one case where both parts are false."]),
        C(7, 'Two routes', [
            "Every question has two routes.",
            A('Two routes', T('Route 1: the laws · Route 2: plug in numbers', size=44)),
            "The laws, step by step. Or plug in numbers — or try the choices.",
            A('Choices differ', T('Check that the choices give different values', size=44)),
            "Before you trust one number, check that the choices give different values. If two tie — try another number.",
            "Pick a number whose roots come out clean — like eighty-one."]),
        C(8, 'Before you practice', [
            "Before you practice, always ask yourself:",
            A('Check 1', T('1. Can I write it with prime bases or the same base?', size=40)),
            A('Check 2', T('2. Is there a known pattern or formula here?', size=40)),
            A('Check 3', T('3. Can the thing I divide by be $0$?', size=40)),
            A('Check 4', T('4. Do the choices give different values for my number?', size=40)),
            "And watch the traps: root a plus root b is NOT root of a plus b. Two and four only for whole numbers. And never divide by root x.",
            "You know all of this. Go practice."]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == 'power-b'][-1]
    M.new_video('r26-t11-summary', TOPIC, 'Advanced Exponents & Roots: Summary', sb, slides, 'power-b', after=last)


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
    # Lesson "r26-t11-tools" slide 3 solved x^(-1/2) = 4, the same as guided q-301 -> new lesson example x^(-1/2) = 3
    # (the summary already uses 5).
    _dd_sub(M, 'r26-t11-tools', 3, [
        (r'$x^{-\frac12}=4$', r'$x^{-\frac12}=3$'),
        ('x^(−1/2) = 4 appears', 'x^(−1/2) = 3 appears'),
        ('Write "(x^(−1/2))^(−2) = 4^(−2)  →  x = 1/16"', 'Write "(x^(−1/2))^(−2) = 3^(−2)  →  x = 1/9"'),
        ('So x is four to the minus two: one sixteenth.', 'So x is three to the minus two: one ninth.'),
        ('Write "check: (1/16)^(−1/2) = 16^(1/2) = 4 ✓"', 'Write "check: (1/9)^(−1/2) = 9^(1/2) = 3 ✓"'),
        ('Check it: the minus flips one sixteenth to sixteen. Sixteen to the half: four. It works.',
         'Check it: the minus flips one ninth to nine. Nine to the half: three. It works.')])
    # Lesson "r26-t11-tools" slide 5 solved sqrt(x)(sqrt(x) − 3) = 0, the same as guided q-299 -> new lesson example
    # (the summary already uses sqrt(x) − 5).
    _dd_sub(M, 'r26-t11-tools', 5, [
        (r'$\sqrt{x}\cdot(\sqrt{x}-3)=0$', r'$\sqrt{x}\cdot(\sqrt{x}-2)=0$'),
        ('√x(√x − 3) = 0 appears', '√x(√x − 2) = 0 appears'),
        ('Write "√x = 0 → x = 0" and "√x = 3 → x = 9"', 'Write "√x = 0 → x = 0" and "√x = 2 → x = 4"'),
        ('Root x is zero, or root x is three. So x is zero or nine.', 'Root x is zero, or root x is two. So x is zero or four.')])


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


def _cr_intro_only(M, vid, title_script, ahead_script, label="What's ahead"):
    """Lesson -> title slide + one short 'what's ahead' slide (the questions teach the rest)."""
    v = M.video(vid)
    M.remove_slides(vid, list(range(2, len(v['beats']) + 1)))
    M.set_slide(vid, 1, script=title_script)
    M.insert_slides(vid, 1, [dict(mode='concept', title=label, active=0, pre=[], script=ahead_script)])
    M.set_sidebar(vid, [label])


def cut_repeats(M):
    # The Hebrew topic 11 has no lesson at all - only questions. Both lessons become a short intro.
    # Section A: prime bases -> Q1; (x+y)^2 inside an exponent question -> Q4; the 2-and-4 pattern -> Q3;
    # counting copies -> Q5; two routes + "check that the choices differ" -> Q1 (method 2); "or" claims -> Q16.
    _cr_intro_only(M, 'advanced-powers', [
        'Advanced exponents and roots.',
        'Most rules here you already know — from topics eight, nine and ten. These questions combine them.'], [
        A("'Big powers → prime bases' appears", T(r'Big powers $\to$ prime bases', 40)),
        'The hard part is choosing the right form. Big powers? Break the bases into primes.',
        A("'Two routes' appears", T('Two routes: the laws, or plug in numbers', 40)),
        'And every question gets two routes: the exponent laws, or plugging in numbers.',
        'Five questions next. Try each one first — then watch its solution.'])
    # Section B: root of a root -> Q9 (same example); undo a power -> Q14 (method 2); conjugates -> Q10 and Q11
    # (same example); product = 0 -> Q12; power = 1 and "or" claims -> Q16.
    _cr_intro_only(M, 'r26-t11-tools', [
        'Section B: roots and powers together.',
        'The basics are in topics eight, nine and ten: sums of powers, comparing powers, numbers between zero and one. Look back if you need them.'], [
        A("'Root of a root · undo a power · conjugates' appears", T(r'Root of a root $\cdot$ undo a power $\cdot$ conjugates', 40)),
        'A root inside a root. A strange power on x. A root difference at the bottom of a fraction.',
        A("'Product = 0 · \"or\" claims' appears", T(r'Product $=0$ $\cdot$ "or" claims', 40)),
        'An equation that is already a product equal to zero. And answer choices with the word "or".',
        'Each question teaches its tool — right when you need it.',
        'Eleven questions next. Try each one first — then watch its solution.'])
    # remaining videos that pointed back to the cut slides
    _cr_replace(M, 'solve-q-290', 1, 'It uses two tools from the start of this section', [
        'It needs two ideas: when a power is one, and claims with the word "or".'])
    _cr_replace(M, 'solve-q-297', 3, "The lesson's favourite is four", [
        'Four is a favorite — but here four gives root eight at the end. Not clean.'])


_apply_before_cut_repeats = apply


def apply(M):
    _apply_before_cut_repeats(M)
    cut_repeats(M)   # 2026-10-05: runs last


# ---------------------------------------------------------------------------------------------------------------
# 2026-10-06: new exam method (found by solving real exams): GIVEN POWER -> ASKED POWER.
# Generalizes "raise both sides to the reciprocal power" (Question 14, q-301): one card row + one guided question.
# ---------------------------------------------------------------------------------------------------------------
def add_methods(M):
    g = 'q-r26-t11-13'
    M.new_q(g, TOPIC, 'Given:\n$\\begin{cases} x>0 \\\\ \\sqrt[4]{x^3}=8 \\end{cases}$\n$\\sqrt{x^3}=\\ ?$',
            ['$16$', '$32$', '$64$', '$512$'], 3, [
        'Write both as powers of $x$: the given is $x^{\\frac34}=8$, and the question asks for $x^{\\frac32}$.',
        'Asked exponent ÷ given exponent: $\\frac32\\div\\frac34=\\frac32\\cdot\\frac43=2$. So raise the given to the power $2$.',
        '$\\left(x^{\\frac34}\\right)^2=x^{\\frac32}$, so $\\sqrt{x^3}=8^2=64$. The answer is choice 3.',
        'Check the long way: $x=8^{\\frac43}=16$, and $\\sqrt{16^3}=\\sqrt{4{,}096}=64$ ✓. ($16$ is the trap: it is $x$ itself.)'])
    M.place_q(g, 'power-b', after='solve-q-r26-t11-02')
    _solution(M, g, ["They give one power of x and ask for a different one. Don't find x — jump from power to power."], [
        ('Method 1 · Given power to asked power', [
            "The cue: they give you something about x, and they ask about a DIFFERENT power of x. Not x itself.",
            "First, write both as powers.",
            D('Write "given: x^(3/4) = 8     asked: x^(3/2)"'),
            "The fourth root of x cubed is x to the three quarters. The square root of x cubed is x to the three halves.",
            "Now one question: what power turns three quarters into three halves?",
            D('Write "r = (3/2) ÷ (3/4) = 2"'),
            "Divide the asked exponent by the given exponent. Three halves divided by three quarters: three halves times four thirds. Two.",
            D('Write "(x^(3/4))² = x^(3/2)  →  8² = 64"'),
            "So square both sides of the given. Power of a power: multiply. Three quarters times two is three halves — exactly what they asked.",
            "And the right side: eight squared, sixty-four.",
            D('Circle choice 3'),
            "Choice three. We never found x.",
            "Why does it work? Raising both sides of an equation to the same power keeps them equal. We just choose the power that lands on the question.",
        ]),
        ('Method 2 · The long way', [
            "The long way, to compare: find x first.",
            D('Write "x = 8^(4/3) = 2⁴ = 16"'),
            "Reciprocal power, four thirds. The cube root of eight is two, to the fourth: sixteen. That's x.",
            D('Next to choice 1 write "x — trap"'),
            "Sixteen is choice one — the trap. It's x, not what they asked.",
            D('Write "√(16³) = √4,096 = 64"'),
            "Sixteen cubed is four thousand ninety-six. Its root: sixty-four. Same answer — with much bigger numbers.",
            "The rule: asked exponent divided by given exponent. Raise the given to that power. It doesn't work when the unknown is IN the exponent and you must solve for it — then use equal bases or try the choices.",
        ]),
    ])
    # the sidebar of every guided solution video gets one more question
    qsb = ['Question %d' % k for k in range(1, NQ + 2)]
    for f in [f for f in M.D['flow'] if f['topic'] == TOPIC and f['type'] == 'video']:
        if M.video(f['ref']).get('kind') == 'solution':
            M.set_sidebar(f['ref'], qsb)
    _cr_replace(M, 'r26-t11-tools', 2, 'Eleven questions next.', [
        'Twelve questions next. Try each one first — then watch its solution.'])

    # card row, right after "x with a fractional power"
    rows = M.card('mem-r26-t11-advanced')['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0].startswith('$x$ with a fractional power'))
    rows.insert(k + 1, ['Given one power of $b$, asked a DIFFERENT power of $b$',
                        "don't find $b$: $r=$ asked exponent $\\div$ given exponent; raise the given to $r$ "
                        "(not when the unknown is in the exponent and must be solved)",
                        '$\\sqrt[3]b=5\\Rightarrow b^{\\frac23}=\\left(b^{\\frac13}\\right)^2=25$'])


_apply_before_add_methods = apply


def apply(M):
    _apply_before_add_methods(M)
    add_methods(M)   # 2026-10-06: runs last


# =====================================================================================
# 2026-10-06 practice: the new exam methods as an extra method in PRACTICE explanations
# (append only; the existing worked solution stays as it is). Runs last.
# =====================================================================================
PRACTICE_METHODS = {
    'q-302': [
        'Method 2 · Power count: under the roots, $a\\cdot b$ has power $2$, and a root halves it. So the question has power $1$.',
        'Choices 1, 2 and 4 have power $2$, so they are out. Choice 3, $13\\sqrt{ab}$, has power $1$.',
    ],
    'q-314': [
        'Method 2 · Power count: each fraction has power $1-\\frac12=\\frac12$, so the product has power $1$. Choice 1 (power $2$) and choice 2 (power $\\frac12$) are out.',
        'Choices 3 and 4 both have power $1$. With $x=3$, $y=5$ the question gives $-4$. Choice 3 gives $-2$, and choice 4 gives $-4$. The answer is choice 4.',
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
