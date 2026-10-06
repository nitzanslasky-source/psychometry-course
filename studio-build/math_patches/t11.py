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


# =====================================================================================================================
# 2026-10-06 renumber pass: the English course must not look like the Hebrew one. Every Hebrew-derived question
# (guided q-288..q-301, practice q-302..q-321) gets new numbers / letters / a small story change - same concept, same
# trap, same level, same methods. Solution videos are rewritten to match. Practice clean-up: the 7 extra-bank items
# (copies of the T8/T10 extra sets) and 3 September items whose type the Hebrew practice already has are removed.
# Nothing in topic 11 is recorded (scan of ~/Documents/Course.recordings, 2026-10-06). Runs last.
# =====================================================================================================================
RECORDED = set()          # a question id here keeps its question and video exactly


def _rn_title(M, vid, lines):
    """Spoken lines of a title slide (keeps the slide's own title and big title)."""
    b = M.slide(vid, 1); b['lines'] = [{'say': s} for s in lines]; M.touched_videos.add(vid)


def renumber_pass(M):
    from math_api import rich_plain

    def S(qid, **kw):
        if qid in RECORDED: return
        q = M.set_q(qid, **kw) or M.q(qid)
        for v in M.D['videos'].values():
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])

    def V(qid, title_lines, slides):
        """slides: {n: (title or None, script)}; the question stays pre-loaded on every slide."""
        if qid in RECORDED: return
        vid = 'solve-' + qid
        old_n = int(M.slide(vid, 1)['bigTitle'].split()[1])   # renumber_guided maps the base number to the final one
        _rn_title(M, vid, [t.replace('%s', _word(old_n)) for t in title_lines])
        for n, (title, script) in slides.items():
            M.set_slide(vid, n, title=title, script=script)
        v = M.video(vid); v['title'] = v['navLabel'] = rich_plain(M.q(qid)['stemRich'])

    # ------------------------------------------------------------------ Section A
    S('q-288', stem='Given: $x\\ne0$. $\\frac{(2x)^4\\cdot(7x)^3}{(14x^2)^3}\\cdot\\left(\\frac{1}{2}\\right)x=\\ ?$',
      choices=['$2x^2$', '$x^2$', '$\\left(\\frac{1}{2}\\right)x$', '$\\frac{7x}{2}$'], correct=2, expl=[
        'Write $14$ as $2\\cdot7$ before expanding: $(14x^2)^3=2^3\\cdot7^3\\cdot x^6$.',
        'Top: $(2x)^4\\cdot(7x)^3=2^4\\cdot7^3\\cdot x^7$.',
        '$\\frac{2^4\\cdot7^3\\cdot x^7}{2^3\\cdot7^3\\cdot x^6}=2x$. Then $2x\\cdot\\frac12x=x^2$.',
        'Check with $x=1$: $\\frac{2^4\\cdot7^3}{14^3}\\cdot\\frac12=2\\cdot\\frac12=1$. The choices give $2$, $1$, $\\frac12$ and $\\frac72$, so only $x^2$ fits.'])
    V('q-288', ['Question %s.', 'Two routes: the exponent laws first, then plugging in a number.'], {
        2: (None, [
            "Numerator first. Every factor inside a bracket gets the power.",
            D('Under (2x)⁴ write "2⁴x⁴"; under (7x)³ write "7³x³"'),
            "Two to the fourth, x to the fourth. Seven cubed, x cubed. Don't multiply them out.",
            "Now the bottom. Fourteen is two times seven — split it first.",
            D('Under the denominator write "(2 · 7 · x²)³ = 2³ · 7³ · x⁶"'),
            "Each factor gets the cube. And x squared, cubed — multiply the powers: x to the sixth.",
            "Now cancel. Seven cubed on top, seven cubed underneath — gone.",
            D('Cross out 7³ on top and on the bottom'),
            "Two to the fourth over two cubed — one two is left.",
            D('Cross out 2³ and leave one 2 on top'),
            "x to the fourth times x cubed is x to the seventh. Over x to the sixth — one x is left.",
            D('Write "= 2x"'),
            "So the big fraction is two x. Times one half x…",
            D('Write "2x · (1/2)x = x²" and circle choice 2'),
            "…the twos cancel. x squared. Choice two.",
        ]),
        3: (None, [
            "Now the psychometric route: plug in a number.",
            "With powers, the friendliest number is one — one to any power stays one.",
            "But first, check that the choices come out different when x is one.",
            D('Next to the choices write their values: 2, 1, 1/2, 7/2'),
            "Two, one, one half, seven halves. All different — so one substitution is enough.",
            D('In the question write "2⁴ · 7³ / 14³ · 1/2"'),
            "The question becomes: two to the fourth times seven cubed, over fourteen cubed, times a half.",
            "Split fourteen cubed into two cubed times seven cubed — same move as before.",
            D('Write "= 2 · 1/2 = 1"'),
            "Seven cubed cancels, one two is left. Two times a half: one.",
            D('Circle choice 2'),
            "Only choice two gives one.",
            "Which route? For most students, plugging in is faster — unless you're really strong with exponent laws.",
        ])})

    S('q-289', stem='Given: $p$, $q$, $r$ and $s$ are nonzero. $\\frac{p^3\\cdot q^{-4}}{r^{-2}\\cdot s^5}=\\ ?$',
      choices=['$\\frac{p^3\\cdot q^4}{r^2\\cdot s^5}$', '$\\frac{1}{p^3\\cdot q^4\\cdot r^2\\cdot s^5}$',
               '$\\frac{p^3\\cdot r^2}{q^4\\cdot s^5}$', '$\\frac{s^5\\cdot p^3}{r^2\\cdot q^4}$'], correct=3, expl=[
        'A negative exponent moves a factor to the other side of the fraction bar, with a positive exponent: $q^{-4}$ on top becomes $q^4$ at the bottom, and $r^{-2}$ at the bottom becomes $r^2$ on top.',
        '$p^3$ and $s^5$ stay where they are: $\\frac{p^3\\cdot r^2}{q^4\\cdot s^5}$.'])
    V('q-289', ['Advanced powers — question %s.',
                "The standard way works — but there's a shortcut that makes this a few-second question."], {
        2: (None, [
            "The standard way: rewrite every negative power as a fraction.",
            D('Under q⁻⁴ write "1/q⁴"; under r⁻² write "1/r²"'),
            "q to the minus four is one over q to the fourth. r to the minus two is one over r squared.",
            "Then multiply tops, multiply bottoms, and untangle the fraction. It works — but it's slow.",
        ]),
        3: (None, [
            "Here's the shortcut. A negative exponent just switches floors.",
            D('Draw an arrow taking q⁻⁴ down to the bottom, and write "q⁴" there'),
            "q to the minus four lives upstairs. It moves downstairs — and becomes q to the fourth.",
            D('Draw an arrow taking r⁻² up to the top, and write "r²" there'),
            "r to the minus two lives downstairs. It moves upstairs: r squared.",
            "p cubed and s to the fifth have positive powers. They stay where they are.",
            "So: p cubed and r squared on top. q to the fourth and s to the fifth underneath.",
            D('Circle choice 3'),
            "Choice three. And careful with choice four — it moves the wrong letters.",
        ])})

    S('q-291', stem='Given:\n$\\begin{cases} x>1,\\ y>1 \\\\ y^x=x^y \\\\ y=x^2 \\end{cases}$\n$x=?$',
      choices=['$4$', '$8$', '$2$', '$3$'], correct=3, expl=[
        'Put $y=x^2$ into $y^x=x^y$: $(x^2)^x=x^{x^2}$, so $x^{2x}=x^{x^2}$.',
        'Same base ($x>1$), so the exponents are equal: $2x=x^2$. Since $x\\ne0$, divide by $x$: $x=2$.',
        'Check: $y=4$, and $4^2=16=2^4$ ✓.',
        'Faster: the choices are whole numbers, so $y=x^2$ is a whole number too. For two different positive whole numbers, $a^b=b^a$ only for 2 and 4 (topic 8). $x=4$ gives $y=16$, so $x=2$.'])
    V('q-291', ['Question %s.', 'A long algebra route — and a one-line shortcut if you know the pattern.'], {
        2: (None, [
            "Two equations, two unknowns. We want x — so we get rid of y.",
            "The second equation says y is x squared. Put that into the first one.",
            D('Write "(x²)^x = x^(x²)"'),
            "x squared, to the power x — equals x to the power x squared.",
            D('Write "x^(2x) = x^(x²)"'),
            "Power of a power: multiply. x to the two x.",
            "Same base on both sides — so the exponents must be equal.",
            D('Write "2x = x²"'),
            "Two x equals x squared.",
            D('Write "x = 2"'),
            "x is bigger than one, so it isn't zero — we can divide by x. x equals two.",
            D('Circle choice 3'),
            "Choice three. Honestly — quite long.",
        ]),
        3: (None, [
            "Much shorter if you know the pattern: a to the b equals b to the a.",
            A('2⁴ = 4² = 16 appears', T('$2^4=4^2=16$', size=52)),
            "From topic eight: for two different positive whole numbers, this happens only with two and four.",
            "Here the choices are whole numbers. If x is a whole number, y — x squared — is one too. So they must be two and four.",
            D('Next to the question write "x = 2 or 4"'),
            "So x is two or four. Test four: then y is sixteen — not two, not four. Out.",
            D('Cross out choice 1'),
            D('Circle choice 3'),
            "x is two, y is four. Four squared is sixteen, two to the fourth is sixteen. Done in seconds.",
            "Careful: the pattern is only for whole numbers. With fractions there are other pairs — for example nine quarters and twenty-seven eighths.",
            "So use it when the choices are whole numbers.",
        ])})

    S('q-292', stem='Given:\n$\\begin{cases} 3^x\\cdot3^y=81 \\\\ 2xy=6 \\end{cases}$\n$x^2+y^2=?$',
      choices=['$13$', '$10$', '$16$', '$4$'], correct=2, expl=[
        '$3^x\\cdot3^y=3^{x+y}$ and $81=3^4$, so $x+y=4$.',
        '$(x+y)^2=x^2+y^2+2xy$: $16=x^2+y^2+6$, so $x^2+y^2=10$.',
        'There is no need to find $x$ and $y$ (for example, $x=1$ and $y=3$).'])
    V('q-292', ['Question %s.', 'It starts as an exponent equation — and ends as a multiplication-formula question.'], {
        2: (None, [
            "First given: three to the x times three to the y.",
            "Same base, multiplying — add the exponents.",
            D('Write "3^(x+y) = 3⁴"'),
            "And eighty-one is three to the fourth.",
            D('Write "x + y = 4"'),
            "Same base — compare the exponents. x plus y is four.",
            "Second given: two x y is six.",
            "Put them together and you've built the first contracted multiplication formula.",
            D('Write "(x + y)² = x² + y² + 2xy"'),
            D('Write "4² = x² + y² + 6"'),
            "x plus y is four — so four squared. And two x y is six.",
            D('Write "x² + y² = 16 − 6 = 10" and circle choice 2'),
            "Sixteen minus six: ten. Choice two.",
        ])})

    S('q-293', stem='Given: $4^x=4^y+4^y+4^y+4^y$. $x-y=\\ ?$', choices=['$4$', '$2$', '$1$', '$0$'], correct=3, expl=[
        'Four equal terms: $4^y+4^y+4^y+4^y=4\\cdot4^y=4^1\\cdot4^y=4^{y+1}$.',
        '$4^x=4^{y+1}$, so $x=y+1$ and $x-y=1$.',
        'Check with $y=1$: $4^x=4+4+4+4=16$, so $x=2$ and $x-y=1$ ✓.',
        '($4$ is the trap: it counts the copies. Four copies add $1$ to the exponent, because $4=4^1$.)'])
    V('q-293', ['Question %s.', 'Two ways: the math route, then plugging in a number.'], {
        2: (None, [
            "Four to the y, plus four to the y, plus four to the y, plus four to the y.",
            "You can't add exponents across a plus sign. But look — it's the same term, four times.",
            D('Write "= 4 · 4^y"'),
            "Just like y plus y is two y — four copies of four to the y is four times four to the y.",
            "And four is four to the one.",
            D('Write "= 4¹ · 4^y = 4^(y+1)"'),
            "Same base, multiplying — add the exponents: four to the y plus one.",
            D('Write "x = y + 1 → x − y = 1" and circle choice 3'),
            "Same base on both sides: x is y plus one. So x minus y is one. Choice three.",
            "Careful: four copies doesn't mean plus four. Choice one is the trap.",
        ]),
        3: (None, [
            "Now the psychometric way. It's an equation — so plug a number into one letter, then work out the other.",
            "Plug into y — it shows up four times.",
            D('Write "y = 1: 4^x = 4 + 4 + 4 + 4 = 16"'),
            "y is one: four plus four plus four plus four — sixteen.",
            D('Write "4^x = 16 → x = 2"'),
            "Four to the what is sixteen? Four squared. x is two.",
            D('Write "x − y = 2 − 1 = 1" and circle choice 3'),
            "Two minus one: one. The choices are plain numbers, so one substitution is enough. Choice three.",
            "Here the plug-in was much shorter for most students.",
        ])})

    # ------------------------------------------------------------------ Section B
    S('q-294', stem='$\\frac{\\sqrt{\\frac{1}{3}}\\cdot\\sqrt{45}\\cdot\\sqrt[6]{3^3}}{\\sqrt{5}}=\\ ?$',
      choices=['$\\sqrt3$', '$\\sqrt5$', '$3$', '$9$'], correct=3, expl=[
        'Write the sixth root as a power: $\\sqrt[6]{3^3}=3^{\\frac36}=3^{\\frac12}=\\sqrt3$.',
        'Now every root is a square root. Top: $\\sqrt{\\frac13\\cdot45\\cdot3}=\\sqrt{45}$.',
        '$\\frac{\\sqrt{45}}{\\sqrt5}=\\sqrt{\\frac{45}{5}}=\\sqrt9=3$.'])
    V('q-294', ['Advanced powers B — question %s.', 'Three different roots. First job: make them all the same kind.'], {
        2: (None, [
            "Look at the roots. Square roots on top, a square root underneath — and one sixth root.",
            "Before anything else, make every root the same order.",
            D('Under the sixth root write "= 3^(3/6)"'),
            "Turn the root into a power. The base stays three. The power goes on top, the root goes underneath: three over six.",
            "Little memory trick: the power is up in the sky, the root is down in the ground.",
            D('Write "= 3^(1/2) = √3"'),
            "Three sixths is a half. Three to the half — that's just root three.",
            "Shortcut: you're allowed to cancel the root's index with the power. Divide both by three — square root of three to the one.",
            "Now the whole top is square roots. Multiply them under ONE root.",
            D('Write "√(1/3 · 45 · 3)" over the top'),
            "Root of a third, times forty-five, times three.",
            D('Cancel the 1/3 with the 3; write "= √45"'),
            "A third and a three cancel. Root forty-five on top.",
            "Some students spot it even earlier — root a third and root three cancel straight away. Same result.",
            D('Write "√45 / √5 = √(45/5) = √9 = 3"'),
            "Same order on top and bottom — divide first, then take the root. Forty-five over five is nine. Root nine: three.",
            D('Circle choice 3'),
            "Three. Choice three.",
        ])})

    S('q-295', choices=['$2\\pi$', '$2\\sqrt{11}$', '$\\sqrt{41}$', '$\\sqrt{21}+\\sqrt{6}$'], correct=4, expl=[
        '$\\sqrt{41}$ is a little more than $\\sqrt{36}=6$ (about $6.4$). $2\\pi\\approx2\\cdot3.14=6.28$.',
        '$\\sqrt{21}+\\sqrt6\\approx4.6+2.4=7$. $2\\sqrt{11}=\\sqrt{44}<\\sqrt{49}=7$.',
        'To be sure the sum is more than 7: $(\\sqrt{21}+\\sqrt6)^2=27+2\\sqrt{126}$, and $\\sqrt{126}>11$ (because $11^2=121$). The square is more than $27+22=49$.',
        'The largest is $\\sqrt{21}+\\sqrt6$.'])
    V('q-295', ['Question %s.', 'Which one is biggest? Here we estimate — using perfect squares.'], {
        2: (None, [
            "We don't know these exactly. But we can estimate.",
            D('Next to 2π write "2 · 3.14 ≈ 6.28"'),
            "Choice one: two pi. Pi is about three point one four. Twice that: about six point two eight.",
            D('Next to √41 write "√36 = 6 → 6 plus"'),
            "Choice three: root forty-one. Root thirty-six is exactly six. So this is a little more than six.",
            "Both of these sit around six and a bit. Let's see if anything beats them.",
            D('Next to √21 + √6 write "≈ 4.6 + 2.4 ≈ 7"'),
            "Choice four. Root twenty-one: root twenty-five is five, so under five — about four point six. Root six is about two point four.",
            "Together: about seven. That beats choices one and three.",
            D('Cross out choices 1 and 3'),
            "Now choice two: two root eleven. Two ways.",
            D('Next to 2√11 write "2 · 3.3 ≈ 6.6"'),
            "Way one: root eleven is about three point three, times two — about six point six.",
            D('Below it write "= √(4 · 11) = √44"'),
            "Way two: bring the two inside the root. A number goes in squared — four times eleven, root forty-four.",
            "Root forty-four is less than root forty-nine, which is seven. So it's under seven.",
            D('Cross out choice 2 and circle choice 4'),
            "About seven wins. Choice four.",
            "Notice: choices one and three are too close to split quickly — and we didn't need to. Choice four beat them both.",
        ])})

    S('q-296', stem='$\\frac{5}{2\\sqrt{3}}+\\frac{\\sqrt{3}}{6}=\\ ?$',
      choices=['$\\frac{1}{3}$', '$\\frac{1}{2\\sqrt{3}}$', '$3$', '$\\sqrt{3}$'], correct=4, expl=[
        'Clear the root in the first denominator: $\\frac{5}{2\\sqrt3}\\cdot\\frac{\\sqrt3}{\\sqrt3}=\\frac{5\\sqrt3}{6}$.',
        'Now the denominators are the same: $\\frac{5\\sqrt3}{6}+\\frac{\\sqrt3}{6}=\\frac{6\\sqrt3}{6}=\\sqrt3$.'])
    V('q-296', ['Question %s.', 'Two fractions with roots. Three ways to add them.'], {
        2: (None, [
            "Fastest route: get the root out of the first denominator.",
            D('Next to 5/(2√3) write "· √3/√3 = 5√3/(2 · 3) = 5√3/6"'),
            "Multiply top and bottom by root three. Root three times root three is three — so the bottom is two times three, six.",
            "Now both fractions have six at the bottom.",
            D('Write "5√3/6 + √3/6 = 6√3/6 = √3"'),
            "Five root three plus one root three: six root three. Over six: root three.",
            D('Circle choice 4'),
            "Choice four.",
        ]),
        3: (None, [
            "Adding fractions — we need the same denominator.",
            "Method two: rewrite the second fraction so it matches the first.",
            D('Under √3/6 write "6 = 2 · 3 = 2 · √3 · √3"'),
            "Six is two times three — and three is root three times root three. So six is two, root three, root three.",
            D('Cancel one √3 and write "= 1/(2√3)"'),
            "Cancel one root three. The second fraction becomes one over two root three.",
            "Little tip: flip it and you know this one. Six over root three — ignore the root, six over three is two, put the root back: two root three. Now flip back: one over two root three.",
            D('Write "5/(2√3) + 1/(2√3) = 6/(2√3) = 3/√3"'),
            "Now the denominators match. Five plus one: six over two root three. That's three over root three.",
            D('Write "= √3"'),
            "Three over root three — ignore the root, three over three is one, put the root back: root three.",
            D('Circle choice 4'),
            "Root three. Choice four.",
        ]),
        4: (None, [
            "Method three: the most basic common denominator — multiply the two denominators.",
            D('Write "common denominator: 2√3 · 6 = 12√3"'),
            "Two root three times six: twelve root three.",
            D('Write "5 · 6 = 30" and "√3 · 2√3 = 6"'),
            "First fraction times six on top: thirty. Second fraction times two root three on top: root three times two root three is six.",
            D('Write "(30 + 6)/(12√3) = 36/(12√3) = 3/√3 = √3"'),
            "Thirty-six over twelve root three. That's three over root three — root three again.",
            D('Circle choice 4'),
            "Same answer. Pick the method you like.",
        ])})

    # review 2026-10-06: back to the Hebrew's steps (square root inside a square root, 4th root, plug in 16)
    S('q-297', stem='Given: $x>0$. $\\sqrt{x^2\\cdot\\sqrt{x}}=\\ ?$',
      choices=['$x^2$', '$x\\sqrt{x}$', '$\\sqrt[4]{x^5}$', '$\\sqrt[3]{x^2}$'], correct=3, expl=[
        'Bring $x^2$ inside the inner root (it goes in squared): $x^2\\sqrt x=\\sqrt{x^4\\cdot x}=\\sqrt{x^5}$.',
        'A root of a root: multiply the indices. $\\sqrt{\\sqrt{x^5}}=\\sqrt[4]{x^5}$.',
        'With exponents: $x^2\\cdot x^{\\frac12}=x^{\\frac52}$, and the outer root halves the exponent: $x^{\\frac54}=\\sqrt[4]{x^5}$.',
        'Check with $x=16$: $\\sqrt{256\\cdot4}=\\sqrt{1024}=32$, and $\\sqrt[4]{16^5}=2^5=32$ ✓.'])
    V('q-297', ['Question %s.', 'A root inside a root. Two ways: algebra, then plugging in.'], {
        2: (None, [
            "First step: bring the x squared inside the inner root.",
            "How does a factor go into a root? Raised to the root's index. Square root — so x squared goes in squared: x to the fourth.",
            D('Write "x² · √x = √(x⁴ · x) = √(x⁵)"'),
            "x to the fourth times x: x to the fifth. So inside we have root of x to the fifth.",
            D('Write "√(√(x⁵)) = ⁴√(x⁵)"'),
            "Now it's a root of a root. Just like a power of a power — multiply the indices. Two times two: a fourth root.",
            D('Circle choice 3'),
            "Fourth root of x to the fifth. Choice three.",
        ]),
        3: (None, [
            "Plug in a number. One is easy — but every choice would give one. Useless.",
            "Four is a favorite — but here four gives root thirty-two at the end. Not clean.",
            "So take sixteen. Its roots come out whole.",
            D('Next to the choices write: 256, 64, 32, ∛256'),
            "Choice one: sixteen squared, two hundred fifty-six. Choice two: sixteen times four, sixty-four. Choice three: fourth root of sixteen to the fifth — two to the fifth, thirty-two. Choice four: cube root of two hundred fifty-six — not a whole number.",
            D('In the question write "√16 = 4 → 256 · 4 = 1024 → √1024 = 32"'),
            "Now the question: root sixteen is four. Sixteen squared is two hundred fifty-six, times four: one thousand twenty-four. Root of that: thirty-two.",
            D('Circle choice 3'),
            "Thirty-two — choice three.",
            "Know both routes. Here too, plugging in is shorter for most students.",
        ])})

    S('q-298', stem='Given: $m>0$ and $n>0$. $\\dfrac{m-n}{\\sqrt{m}+\\sqrt{n}}=\\ ?$',
      choices=['$\\sqrt{m}-\\sqrt{n}$', '$m+n$', '$\\sqrt{m}+\\sqrt{n}$', '$0$'], correct=1, expl=[
        'Write the top as a difference of squares of roots: $m-n=(\\sqrt m+\\sqrt n)(\\sqrt m-\\sqrt n)$.',
        'Cancel $\\sqrt m+\\sqrt n$ (it is positive, so it is not 0). The result is $\\sqrt m-\\sqrt n$.',
        'Check with $m=4$, $n=1$: $\\frac{4-1}{2+1}=1$, and $\\sqrt4-\\sqrt1=1$ ✓.'])
    V('q-298', ['Question %s.', "Getting rid of that denominator isn't obvious — until you see the formula."], {
        2: (None, [
            "The choices have no denominator. So we need to get rid of it.",
            "No common factor on top. So what can we do? Spot the third contracted multiplication formula.",
            D('Write "m − n = (√m + √n)(√m − √n)"'),
            "m minus n is root m plus root n, times root m minus root n.",
            "Check: root m times root m is m. Root n times minus root n is minus n. The middle terms cancel.",
            "We're used to this formula with squares. It works just as well with square roots.",
            D('Cancel (√m + √n) top and bottom'),
            "Now the root m plus root n cancels with the denominator.",
            D('Circle choice 1'),
            "What's left: root m minus root n. Choice one.",
        ]),
        3: (None, [
            "Plug in. Pick numbers with clean roots: four and one.",
            "And plug in smart — m is four, n is one, so the top stays positive.",
            D('Next to the choices write: 1, 5, 3, 0'),
            "Check the choices: two minus one is one. Four plus one is five. Two plus one is three. Zero. All different — one substitution is enough.",
            D('In the question write "(4 − 1)/(2 + 1) = 1"'),
            "The question: four minus one is three. Root four plus root one: two plus one, three. Three over three: one.",
            D('Circle choice 1'),
            "One — choice one. The plug-in is the easy route for most students.",
        ])})

    S('q-299', stem='How many solutions does the equation $\\sqrt{x}\\cdot(\\sqrt{x}-6)=0$ have?',
      choices=['$0$', '$1$', '$2$', '$3$'], correct=3, expl=[
        'A product is 0 only when one of the factors is 0.',
        '$\\sqrt x=0$ gives $x=0$. $\\sqrt x-6=0$ gives $\\sqrt x=6$, so $x=36$.',
        'Both work, so there are 2 solutions. Do not divide by $\\sqrt x$: that loses $x=0$.'])
    V('q-299', ['Question %s.', "How many solutions? We'll solve it — and count."], {
        2: (None, [
            "To count the solutions, we have to solve it.",
            D('Write "√x · √x − 6√x = 0"'),
            "Open the brackets. Root x times root x.",
            D('Write "x − 6√x = 0 → x = 6√x"'),
            "Root x times root x is x. So x minus six root x is zero — x equals six root x.",
            "When does a number equal six times its own root?",
            D('Write "x = 0: 0 = 0 ✓" and "x = 36: 36 = 6 · 6 ✓"'),
            "Zero works: zero equals zero. Thirty-six works: thirty-six equals six times six.",
            D('Circle choice 3'),
            "Exactly two solutions. Choice three.",
            "Faster: it was already a product equal to zero — each factor can be zero.",
            "But never divide both sides by root x. That throws away x equals zero — and leaves you with only one solution. Wrong answer.",
        ]),
        3: (None, [
            "Method two — the fast one. Look at the left side: it's already a product. Root x, times root x minus six.",
            "A product is zero only when one of the factors is zero.",
            D('Write "√x = 0  or  √x − 6 = 0"'),
            "So root x is zero — or root x minus six is zero.",
            D('Write "√x = 0 → x = 0"'),
            "Root x is zero: x is zero.",
            D('Write "√x = 6 → x = 36"'),
            "Root x is six: x is thirty-six.",
            D('Circle choice 3'),
            "The same two solutions. Choice three.",
        ])})

    S('q-300', stem='Given:\n$\\begin{cases} 2x+y=\\sqrt{180} \\\\ x-y=\\sqrt{45} \\end{cases}$\n$x=?$',
      choices=['$9\\sqrt{5}$', '$\\sqrt{42}$', '$5$', '$3\\sqrt{5}$'], correct=4, expl=[
        'Simplify the roots: $\\sqrt{180}=\\sqrt{36}\\cdot\\sqrt5=6\\sqrt5$ and $\\sqrt{45}=\\sqrt9\\cdot\\sqrt5=3\\sqrt5$.',
        'Add the two equations to remove $y$: $3x=6\\sqrt5+3\\sqrt5=9\\sqrt5$, so $x=3\\sqrt5$.',
        'Quick check: $180=4\\cdot45$, so $\\sqrt{180}=2\\sqrt{45}$. Then $3x=3\\sqrt{45}$ and $x=\\sqrt{45}=3\\sqrt5$.',
        '($5$ is the trap: it adds the roots into one root, $\\sqrt{225}=15$.)'])
    V('q-300', ['Question %s.', 'A system of equations — with roots. Two ways: exact, then estimating.'], {
        2: (None, [
            "They want x. So we need to get rid of y.",
            D('Add the equations: write "3x = √180 + √45"'),
            "Add the equations — y cancels. Three x equals root one-eighty plus root forty-five.",
            D('Next to it write "≠ √225" and cross it out'),
            "What you must NOT do: add them into root two-twenty-five. That's wrong — and it leads straight to choice three, the trap.",
            "To add roots, we need a common root. Split each one into a number times a root.",
            D('Write "√180 = √36 · √5 = 6√5"'),
            "Does a hundred and eighty split into something with a clean root? Thirty-six times five. So six root five.",
            D('Write "√45 = √9 · √5 = 3√5"'),
            "Forty-five: nine times five. Three root five. Same root five — good.",
            D('Write "3x = 9√5 → x = 3√5"'),
            "Six root five plus three root five: nine root five. Divide by three: three root five.",
            D('Circle choice 4'),
            "Choice four.",
            D('Write "√180 = √(4 · 45) = 2√45 → 3x = 3√45 → x = √45 = 3√5"'),
            "An even faster way to see it: a hundred and eighty is four times forty-five. So root one-eighty is two root forty-five.",
            "Three x is three root forty-five. x is root forty-five — three root five. Same answer.",
        ]),
        3: (None, [
            "Can't split the roots? Estimate instead.",
            D('Write "√180 ≈ 13.4" and "√45 ≈ 6.7"'),
            "Root one-eighty: root one sixty-nine is thirteen, root one ninety-six is fourteen — about thirteen point four. Root forty-five: between six and seven, about six point seven.",
            D('Write "3x ≈ 20.1 → x ≈ 6.7"'),
            "Three x is about twenty point one. So x is about six point seven.",
            D('Next to the choices write: ≈ 20.1, ≈ 6.5, 5, ≈ 6.7'),
            "Nine root five: way too big. Root forty-two: about six point five. Five: too small. Three root five: three times two point two four, about six point seven.",
            "Careful — this one's tighter than usual. Six point five and six point seven are close, so keep one decimal place.",
            D('Circle choice 4'),
            "Six point seven matches. Choice four. Know the exact method — but estimating is a solid backup.",
        ])})

    S('q-301', stem='Given: $x^{-\\frac13}=2$. $x=?$',
      choices=['$\\frac{1}{6}$', '$8$', '$\\frac{1}{8}$', '$\\frac{1}{2}$'], correct=3, expl=[
        '$x^{-\\frac13}=\\frac1{\\sqrt[3]x}$, so $\\frac1{\\sqrt[3]x}=2$ and $\\sqrt[3]x=\\frac12$. Cube: $x=\\frac18$.',
        'Or raise both sides to the reciprocal power, $-3$: $x=2^{-3}=\\frac18$.',
        'Check: $\\left(\\frac18\\right)^{-\\frac13}=8^{\\frac13}=2$ ✓.'])
    V('q-301', ['Question %s.', 'Three ways to crack a negative fractional power.'], {
        2: ('Method 1 · Flip, then cube', [
            "Simplify the left side. A negative power flips the fraction.",
            D('Write "1 / x^(1/3) = 2"'),
            "One over x to the one third, equals two.",
            D('Write "1/∛x = 2"'),
            "A power of a third is a cube root. One over the cube root of x equals two.",
            D('Write "1 = 2∛x → ∛x = 1/2"'),
            "Multiply by the cube root of x: one equals two times the cube root of x. Divide by two: the cube root of x is a half.",
            D('Write "x = (1/2)³ = 1/8"'),
            "Cube both sides: x is one eighth.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        3: (None, [
            "The short, elegant route: isolate x by raising both sides to a power.",
            "Power of a power — we multiply. Minus a third times what gives one? Minus three.",
            D('Write "(x^(−1/3))^(−3) = 2^(−3)"'),
            "It's always the reciprocal of the power. So raise both sides to minus three.",
            D('Write "x = 2^(−3) = 1/8"'),
            "Left side: just x. Right side: two to the minus three — one over eight.",
            D('Circle choice 3'),
            "Straight to the answer. Choice three.",
        ]),
        4: (None, [
            "The psychometric route: plug in an answer. Start with the roundest one — eight.",
            D('Next to choice 2 write "8^(−1/3) = 1/∛8 = 1/2"'),
            "Eight to the minus a third: one over the cube root of eight — one half.",
            "We wanted two. We got a half. Wrong — but look: it's exactly the reciprocal.",
            "The minus sign flips the fraction. So try the reciprocal: one eighth.",
            D('Next to choice 3 write "(1/8)^(−1/3) = 8^(1/3) = 2 ✓"'),
            "One eighth to the minus a third: flip it — eight to the third. The cube root of eight: two. It works.",
            D('Circle choice 3'),
            "One eighth. Choice three.",
        ])})

    S('q-290', stem='Given: $n$ is an integer, and\n$\\begin{cases} m\\ne1 \\\\ m^{n-3}=1 \\end{cases}$\nWhich of the following is necessarily true?',
      choices=['$m=0$ or $n\\ne5$', '$m=0$', '$n=3$ or $m=-1$', '$m=0$ or $n\\ne3$'], correct=3, expl=[
        'A power equals 1 in three cases: the base is 1; the base is $-1$ and the exponent is even; the exponent is 0 and the base is not 0.',
        'Here $m\\ne1$. Therefore $n-3=0$ (that is, $n=3$), or $m=-1$ (with $n-3$ even).',
        'An "or" claim is necessarily true when every allowed case makes at least one part true. Choice (3) covers both cases.',
        'The others fail. (1): $m=-1$, $n=5$ gives $(-1)^2=1$, but $m\\ne0$ and $n=5$. (2): a power of 0 is never 1. (4): $m=5$, $n=3$ gives $5^0=1$, but $m\\ne0$ and $n=3$.'])
    V('q-290', ['Question %s.', 'Tricky one — both the given and the answer choices need care.',
                'It needs two ideas: when a power is one, and claims with the word "or".'], {
        2: (None, [
            "The given: m to the power n minus three equals one.",
            "A power that equals one — that should ring a bell. We know exactly when that happens.",
            A("'Base 1 — any exponent' appears", T('Base $1$ — any exponent', size=40, gap=24)),
            "Option one: the base is one. Any exponent works.",
            A("'Base −1 — even exponent' appears", T('Base $-1$ — even exponent', size=40, gap=24)),
            "Option two: the base is negative one — with an even exponent.",
            A("'Exponent 0 — any base except 0' appears", T('Exponent $0$ — any base except $0$', size=40, gap=24)),
            "Option three: the exponent is zero. Any base works — except zero. Zero to the zero is undefined.",
            "Now the extra given: m is not one.",
            D('Cross out the first option'),
            "So option one is gone.",
            "What's left? Either m is negative one and n minus three is even — or n minus three is zero, so n is three.",
            D('Next to the options write "m = −1" and "n = 3"'),
            'Now the choices. Each one is an "or" statement. It fails if one legal case makes both parts false.',
            "Choice one: m is zero, or n isn't five. Take m negative one, n five — negative one squared is one, legal. But m isn't zero, and n IS five. Both parts false.",
            D('Cross out choice 1'),
            "Choice two: m is zero? Zero to any power is never one. Out.",
            D('Cross out choice 2'),
            "Choice four: m is zero, or n isn't three. Take m equals five, n equals three — five to the zero is one, legal. Both parts false again.",
            D('Cross out choice 4 and circle choice 3'),
            "Choice three covers both cases that survive: n is three, or m is negative one. Choice three.",
        ])})

    # ------------------------------------------------------------------ order: Section A easy -> hard
    # Q2 (negative exponents, letters only) is the easiest -> first; counting copies (old Q5) and the (x+y)^2 question
    # (old Q4) before the 2-and-4 system (old Q3, the longest). None of them uses another's method.
    secA = M.section_of('q-288')
    M.move('q-289', secA, before='q-288'); M.move('solve-q-289', secA, after='q-289')
    M.move('q-293', secA, before='q-291'); M.move('solve-q-293', secA, after='q-293')
    M.move('q-292', secA, before='q-291'); M.move('solve-q-292', secA, after='q-292')

    # ------------------------------------------------------------------ practice (Hebrew q-302..q-321)
    S('q-302', stem='Given: $a>0$ and $b>0$. $\\sqrt{5a}\\cdot\\sqrt{20b}=\\ ?$',
      choices=['$10\\sqrt{ab}$', '$10ab$', '$100ab$', '$2ab\\sqrt{5}$'], correct=1, expl=[
        '$\\sqrt{5a}\\cdot\\sqrt{20b}=\\sqrt{100ab}=\\sqrt{100}\\cdot\\sqrt{ab}=10\\sqrt{ab}$.',
        'Method 2 · Power count: under the roots, $a\\cdot b$ has power $2$, and a root halves it. So the question has power $1$.',
        'Choices 2, 3 and 4 have power $2$, so they are out. Choice 1, $10\\sqrt{ab}$, has power $1$.'])
    S('q-303', stem='The equation $(x^a)^a=x^a\\cdot x^a\\cdot x^a\\cdot x^a$ is true for every number $x$. Which of the following could be the value of $a$?',
      choices=['$-1$', '$4$', '$\\frac{1}{4}$', '$2$'], correct=2, expl=[
        'Left: $(x^a)^a=x^{a^2}$. Right: $x^a\\cdot x^a\\cdot x^a\\cdot x^a=x^{4a}$.',
        'True for every $x$, so the exponents are equal: $a^2=4a$, $a(a-4)=0$, so $a=0$ or $a=4$.',
        '$a=0$ also solves $a^2=4a$, but it is not a choice. The answer is $4$. Check: $(x^4)^4=x^{16}=x^4\\cdot x^4\\cdot x^4\\cdot x^4$ ✓.'])
    S('q-304', stem='Given: $n>1$. $\\frac{5^n}{5n}=\\ ?$',
      choices=['$\\frac{5^{n-1}}{n}$', '$\\frac{1}{n}$', '$\\frac{5^{n-2}}{n}$', '$5^{n-2}$'], correct=1, expl=[
        'The bottom is $5^1\\cdot n$. Divide the powers of 5: $\\frac{5^n}{5^1}=5^{n-1}$. The $n$ stays at the bottom: $\\frac{5^{n-1}}{n}$.',
        'Check with $n=2$: $\\frac{25}{10}=\\frac52$, and $\\frac{5^1}{2}=\\frac52$ ✓. The other choices give $\\frac12$, $\\frac12$ and $1$.'])
    S('q-305', stem='$\\frac{6^x}{2^{x-1}\\cdot3^{x+1}}=\\ ?$',
      choices=['$\\frac{2^x}{3^x}$', '$\\frac{2}{3}$', '$1$', '$2^{x+1}\\cdot3^{x-1}$'], correct=2, expl=[
        'Split the top: $6^x=2^x\\cdot3^x$.',
        '$\\frac{2^x}{2^{x-1}}=2^1=2$ and $\\frac{3^x}{3^{x+1}}=3^{-1}=\\frac13$. The result is $2\\cdot\\frac13=\\frac23$.',
        'Check with $x=1$: $\\frac{6}{2^0\\cdot3^2}=\\frac69=\\frac23$. Choices (1) and (2) both give $\\frac23$, so try $x=2$: $\\frac{36}{2\\cdot27}=\\frac{36}{54}=\\frac23$, while $\\frac{2^2}{3^2}=\\frac49$. Choice (2).'])
    S('q-306', stem='Given: $k$ and $m$ are integers, and\n$\\begin{cases} 0<k<m \\\\ k^m=m^k \\end{cases}$\n$k^m=?$',
      choices=['$8$', '$16$', '$64$', '$4$'], correct=2, expl=[
        'For two different positive integers, $k^m=m^k$ only for 2 and 4 (topic 8): $2^4=16=4^2$.',
        '$k=2$ and $m=4$, so $k^m=2^4=16$.',
        'Numbers that are not whole have other pairs, for example $\\frac94$ and $\\frac{27}8$. That is why the question says "integers".',
        '($8$ is the trap: it is $k\\cdot m$, not $k^m$.)'])
    S('q-307', stem='A square garden bed has an area of $\\sqrt{6}$ m². What is the length of its side (in m)?',
      choices=['$\\sqrt{6}$', '$6^{\\frac{1}{4}}$', '$\\frac{1}{\\sqrt{6}}$', '$36$'], correct=2, expl=[
        'Area $=$ side², so side $=\\sqrt{\\sqrt6}$.',
        '$\\sqrt{\\sqrt6}=\\left(6^{\\frac12}\\right)^{\\frac12}=6^{\\frac14}$.',
        '($\\sqrt6$ is the trap: it is the area, not the side.)'])
    S('q-308', stem='$\\frac{\\sqrt{50}+\\sqrt{2}}{\\sqrt{50}-\\sqrt{2}}=\\ ?$',
      choices=['$2$', '$6$', '$\\frac{3}{2}$', '$\\frac{2}{3}$'], correct=3, expl=[
        '$\\sqrt{50}=\\sqrt{25}\\cdot\\sqrt2=5\\sqrt2$.',
        'Top: $5\\sqrt2+\\sqrt2=6\\sqrt2$. Bottom: $5\\sqrt2-\\sqrt2=4\\sqrt2$.',
        '$\\frac{6\\sqrt2}{4\\sqrt2}=\\frac64=\\frac32$.'])
    S('q-309', stem='$\\sqrt{7\\sqrt{7}}=\\ ?$',
      choices=['$\\frac{1}{(\\sqrt{7})^3}$', '$7^{\\frac{1}{2}}$', '$\\frac{1}{\\sqrt{7}}$', '$7^{\\frac{3}{4}}$'], correct=4, expl=[
        'Inside: $7\\sqrt7=7^1\\cdot7^{\\frac12}=7^{\\frac32}$.',
        'The outer root halves the exponent: $\\left(7^{\\frac32}\\right)^{\\frac12}=7^{\\frac34}$.'])
    # review 2026-10-06: back to the Hebrew's "+" form (only one case, one squaring), new letters and choice order
    S('q-310', stem='Given: $p\\ge0$ and $q\\ge0$. When is $\\sqrt{p}+\\sqrt{q}=\\sqrt{p+q}$ true?',
      choices=['Always', 'Only when $p=0$ or $q=0$', 'Only when $pq>0$', 'Only when $p-q=0$'], correct=2, expl=[
        'Both sides are not negative, so square them: $(\\sqrt p+\\sqrt q)^2=p+q+2\\sqrt{pq}$ and $(\\sqrt{p+q})^2=p+q$.',
        'They are equal only when $2\\sqrt{pq}=0$, that is $pq=0$: $p=0$ or $q=0$.',
        'Check: $p=9$, $q=16$: $3+4=7$, but $\\sqrt{25}=5\\ne7$. $p=0$, $q=16$: $0+4=4=\\sqrt{16}$ ✓.'])
    S('q-311', stem='$4^{n+1}-4^n=\\ ?$', choices=['$4$', '$3\\cdot4^n$', '$4^n$', '$4^{-n}$'], correct=2, expl=[
        'Take out the smaller power: $4^{n+1}=4\\cdot4^n$, so $4^{n+1}-4^n=4^n(4-1)=3\\cdot4^n$.',
        'Check with $n=1$: $16-4=12$, and $3\\cdot4^1=12$ ✓. The other choices give $4$, $4$ and $\\frac14$.'])
    S('q-312', stem='Given: $p^q=-1$. Which of the following is necessarily true?',
      choices=['$p=-q^2$', '$p=\\sqrt[3]{q}$', '$p=-1$', '$p=q-1$'], correct=3, expl=[
        '$p=-1$ is the only base whose power can be $-1$. A positive base gives a positive power, and 0 gives 0. Any other negative base gives a power whose size is not 1 (or exactly $+1$ when the exponent is 0).',
        'The exponent can change: $(-1)^5=-1$ and $(-1)^{\\frac15}=\\sqrt[5]{-1}=-1$. But $p$ is always $-1$.',
        'The other choices are not necessarily true: with $q=5$, $-q^2=-25$, $\\sqrt[3]5\\ne-1$ and $q-1=4$.'])
    S('q-313', stem='Which of the following ratios is not equal to the ratio $5:\\sqrt{5}$?',
      choices=['$\\sqrt{20}:2$', '$\\sqrt{5}:1$', '$25:\\sqrt{25}$', '$10:\\sqrt{20}$'], correct=3, expl=[
        'The ratio $5:\\sqrt5$ has the value $\\frac5{\\sqrt5}=\\sqrt5$.',
        '(1) $\\frac{\\sqrt{20}}{2}=\\frac{2\\sqrt5}{2}=\\sqrt5$ ✓. (2) $\\frac{\\sqrt5}{1}=\\sqrt5$ ✓. (4) $\\frac{10}{\\sqrt{20}}=\\frac{10}{2\\sqrt5}=\\frac5{\\sqrt5}=\\sqrt5$ ✓.',
        '(3) $\\frac{25}{\\sqrt{25}}=\\frac{25}5=5\\ne\\sqrt5$. This ratio is not equal. It only looks like the same pattern (a number to its root), but that ratio changes with the number.'])
    S('q-314', stem='Given: $0<n<m$. $\\frac{n-m}{\\sqrt{m+n}}\\cdot\\frac{m+n}{\\sqrt{m-n}}=\\ ?$',
      choices=['$n-m$', '$-\\sqrt{m^2-n^2}$', '$\\sqrt{m-n}$', '$m^2-n^2$'], correct=2, expl=[
        'Multiply the tops and the bottoms. Top: $(n-m)(m+n)=n^2-m^2=-(m^2-n^2)$. Bottom: $\\sqrt{m+n}\\cdot\\sqrt{m-n}=\\sqrt{m^2-n^2}$.',
        '$\\frac{-(m^2-n^2)}{\\sqrt{m^2-n^2}}=-\\sqrt{m^2-n^2}$, because a positive number over its root is its root.',
        'Check with $m=5$, $n=4$: $\\frac{-1}{\\sqrt9}\\cdot\\frac{9}{\\sqrt1}=-3$, and $-\\sqrt{25-16}=-3$ ✓.',
        'Method 2 · Power count: each fraction has power $1-\\frac12=\\frac12$, so the product has power $1$. Choice 3 (power $\\frac12$) and choice 4 (power $2$) are out.',
        'Choices 1 and 2 both have power $1$. With $m=5$, $n=4$ the question gives $-3$. Choice 1 gives $-1$, and choice 2 gives $-3$. The answer is choice 2.'])
    S('q-315', stem='Given: $\\left(\\frac{2^{4b}}{2^x}\\right)^x=2^{4b^2}$. $x=?$',
      choices=['$b$', '$2b$', '$4b$', '$b^2$'], correct=2, expl=[
        'Inside: $\\frac{2^{4b}}{2^x}=2^{4b-x}$. Power of a power: $2^{x(4b-x)}=2^{4bx-x^2}$.',
        'Equal exponents: $4bx-x^2=4b^2$, so $x^2-4bx+4b^2=0$, that is $(x-2b)^2=0$ and $x=2b$.'])
    S('q-316', stem='Given: $\\frac{\\sqrt{3}\\cdot\\sqrt{7}}{3}=\\left(\\frac{7}{3}\\right)^{2x}$. $x=?$',
      choices=['$\\frac{1}{2}$', '$\\frac{1}{4}$', '$1$', '$\\frac{1}{8}$'], correct=2, expl=[
        '$\\frac{\\sqrt3\\cdot\\sqrt7}{3}=\\frac{\\sqrt{21}}{\\sqrt9}=\\sqrt{\\frac{21}9}=\\sqrt{\\frac73}=\\left(\\frac73\\right)^{\\frac12}$.',
        'Same base, so the exponents are equal: $2x=\\frac12$ and $x=\\frac14$.'])
    S('q-317', stem='$\\frac{100^2\\cdot10^3}{2^8\\cdot5^6}=\\ ?$',
      choices=['$\\frac{5}{2}$', '$\\frac{2}{5}$', '$\\frac{5}{4}$', '$\\frac{1}{10}$'], correct=1, expl=[
        'Write everything with primes: $100^2=(10^2)^2=10^4$, so the top is $10^4\\cdot10^3=10^7=2^7\\cdot5^7$.',
        '$\\frac{2^7\\cdot5^7}{2^8\\cdot5^6}=2^{7-8}\\cdot5^{7-6}=2^{-1}\\cdot5=\\frac52$.'])
    S('q-318', stem='Given: $b$ is an integer, and\n$\\begin{cases} a>0,\\ b>0 \\\\ a^{5b}=a^{2b} \\end{cases}$\n$a^b+b^a=?$',
      choices=['$2b$', '$b+1$', '$b^2$', '$1$'], correct=2, expl=[
        'If $a\\ne1$: same base, so $5b=2b$ and $b=0$. But $b>0$, so this is impossible.',
        'Therefore $a=1$ (and $1^{5b}=1=1^{2b}$ ✓). Then $a^b+b^a=1^b+b^1=1+b$.'])
    S('q-319', stem='Given: $3\\sqrt{x}=9^{-1}$. $x=?$',
      choices=['$9^{3}$', '$9^{-2}$', '$9^{-3}$', '$9^{2}$'], correct=3, expl=[
        '$\\sqrt x=\\frac{9^{-1}}3=\\frac1{9\\cdot3}=\\frac1{27}$. Square: $x=\\frac1{729}$.',
        '$9^3=729$, so $x=9^{-3}$.',
        'With powers of 9 only: $3=9^{\\frac12}$, so $\\sqrt x=9^{-1}\\cdot9^{-\\frac12}=9^{-\\frac32}$ and $x=\\left(9^{-\\frac32}\\right)^2=9^{-3}$.'])
    S('q-320', stem='$\\left(\\frac{3^5-3^4}{2}\\right)^2=\\ ?$',
      choices=['$3^{8}$', '$\\left(\\frac{3}{2}\\right)^2$', '$\\left(\\frac{3^2}{2}\\right)^2$', '$3^{16}$'], correct=1, expl=[
        'Take out the smaller power: $3^5-3^4=3^4(3-1)=2\\cdot3^4$.',
        '$\\frac{2\\cdot3^4}{2}=3^4$, and $(3^4)^2=3^8$.'])
    S('q-321', stem='Given:\n$\\begin{cases} n\\ne0 \\\\ x>1 \\end{cases}$\n$\\frac{x^n-x^{\\frac{3n}{4}}}{x^{\\frac{n}{4}}-1}=\\ ?$',
      choices=['$x^{\\frac{3n}{4}}$', '$x^n-1$', '$x^{\\frac{n}{4}}-1$', '$x^n$'], correct=1, expl=[
        'Take out the smaller power on top: $x^n=x^{\\frac{3n}4}\\cdot x^{\\frac n4}$, so $x^n-x^{\\frac{3n}4}=x^{\\frac{3n}4}\\left(x^{\\frac n4}-1\\right)$.',
        'Cancel $x^{\\frac n4}-1$ (it is not 0, because $x>1$ and $n\\ne0$). The result is $x^{\\frac{3n}4}$.',
        'Check with $n=4$, $x=2$: $\\frac{16-8}{2-1}=8$, and $2^3=8$ ✓. The other choices give $15$, $1$ and $16$.'])

    # ------------------------------------------------------------------ practice clean-up
    # copies: the 7 extra-bank items repeat the T8 / T10 extra sets (same templates, other numbers)
    for k in range(1, 8): M.unplace('alg-extra-unit-t11-3-%d' % k)
    # September items whose type the Hebrew practice already has: 9^x*27^x (equal bases: q-316, q-319, q-315),
    # a^b = 1 "or" (q-312 and guided q-290), nested roots (q-309)
    for k in ('05', '09', '12'): M.unplace('q-r26-t11-' + k)
    M.practice_order('unit-t11-3', [
        'q-307', 'q-302', 'q-304', 'q-311', 'q-320', 'q-309', 'q-308', 'q-317', 'q-305', 'q-313', 'q-306',
        'q-r26-t11-04', 'q-316', 'q-319', 'q-303', 'q-r26-t11-10', 'q-312', 'q-318', 'q-315', 'q-r26-t11-08',
        'q-314', 'q-321', 'q-310', 'q-r26-t11-06', 'q-r26-t11-11'])

    # ------------------------------------------------------------------ memory card: examples that were Hebrew questions
    rows = M.card('mem-r26-t11-advanced')['tables'][0]['rows']
    new_ex = {
        'A factor in front of an inner root': '$\\sqrt{x^3\\sqrt x}=\\sqrt{\\sqrt{x^7}}=\\sqrt[4]{x^7}$',
        '$x$ with a fractional power': '$x^{-\\frac12}=6\\Rightarrow x=6^{-2}=\\frac1{36}$',
        'Product $=0$': '$\\sqrt x(\\sqrt x-7)=0\\Rightarrow x=0$ or $x=49$',
        'Power $=1$': '$a^{b+1}=1$, $a\\ne1\\Rightarrow b=-1$ or $a=-1$',
        '"A or B" necessarily true?': '$a=3$, $b=-1$ kills "$a=0$ or $b\\ne-1$"',
    }
    for r in rows:
        if r[0] in new_ex: r[2] = new_ex.pop(r[0])
    assert not new_ex, new_ex
    tips = M.card('mem-r26-t11-advanced')['tips']
    k = next(i for i, t in enumerate(tips) if '\\sqrt{39}' in t)
    tips[k] = 'Estimate roots with perfect squares: $\\sqrt{52}$ is a little more than $\\sqrt{49}=7$.'


_apply_before_renumber_pass = apply


def apply(M):
    _apply_before_renumber_pass(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# =====================================================================================================================
# 2026-10-06 Hebrew back-check: the renumber pass compared with base-v18 only. Compared again with the teacher's Hebrew
# VIDEO subtitles (01-Algebra-Original-Subtitles.txt, lines 6610-8727). Clear matches get new numbers (same type, trap,
# level and methods). Nothing in topic 11 is recorded. Runs last.
# =====================================================================================================================
def hebrew_backcheck(M):
    from math_api import rich_plain

    def S(qid, **kw):
        q = M.set_q(qid, **kw) or M.q(qid)
        for v in M.D['videos'].values():
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])

    def V(qid, slides):
        vid = 'solve-' + qid
        for n, script in slides.items():
            M.set_slide(vid, n, title=None, script=script)
        v = M.video(vid); v['title'] = v['navLabel'] = rich_plain(M.q(qid)['stemRich'])
        M.touched_videos.add(vid)

    # q-288: was exactly the Hebrew video question (2x)^4 (7x)^3 / (14x^2)^3 * x/2 -> 5, 2, 10
    S('q-288', stem='Given: $x\\ne0$. $\\frac{(5x)^4\\cdot(2x)^3}{(10x^2)^3}\\cdot\\left(\\frac{1}{5}\\right)x=\\ ?$',
      choices=['$5x^2$', '$x^2$', '$\\left(\\frac{1}{5}\\right)x$', '$\\frac{2x}{5}$'], correct=2, expl=[
        'Write $10$ as $5\\cdot2$ before expanding: $(10x^2)^3=5^3\\cdot2^3\\cdot x^6$.',
        'Top: $(5x)^4\\cdot(2x)^3=5^4\\cdot2^3\\cdot x^7$.',
        '$\\frac{5^4\\cdot2^3\\cdot x^7}{5^3\\cdot2^3\\cdot x^6}=5x$. Then $5x\\cdot\\frac15x=x^2$.',
        'Check with $x=1$: $\\frac{5^4\\cdot2^3}{10^3}\\cdot\\frac15=5\\cdot\\frac15=1$. The choices give $5$, $1$, $\\frac15$ and $\\frac25$, so only $x^2$ fits.'])
    V('q-288', {
        2: ["Numerator first. Every factor inside a bracket gets the power.",
            D('Under (5x)⁴ write "5⁴x⁴"; under (2x)³ write "2³x³"'),
            "Five to the fourth, x to the fourth. Two cubed, x cubed. Don't multiply them out.",
            "Now the bottom. Ten is five times two — split it first.",
            D('Under the denominator write "(5 · 2 · x²)³ = 5³ · 2³ · x⁶"'),
            "Each factor gets the cube. And x squared, cubed — multiply the powers: x to the sixth.",
            "Now cancel. Two cubed on top, two cubed underneath — gone.",
            D('Cross out 2³ on top and on the bottom'),
            "Five to the fourth over five cubed — one five is left.",
            D('Cross out 5³ and leave one 5 on top'),
            "x to the fourth times x cubed is x to the seventh. Over x to the sixth — one x is left.",
            D('Write "= 5x"'),
            "So the big fraction is five x. Times one fifth x…",
            D('Write "5x · (1/5)x = x²" and circle choice 2'),
            "…five times a fifth is one. x squared. Choice two."],
        3: ["Now the psychometric route: plug in a number.",
            "With powers, the friendliest number is one — one to any power stays one.",
            "But first, check that the choices come out different when x is one.",
            D('Next to the choices write their values: 5, 1, 1/5, 2/5'),
            "Five, one, one fifth, two fifths. All different — so one substitution is enough.",
            D('In the question write "5⁴ · 2³ / 10³ · 1/5"'),
            "The question becomes: five to the fourth times two cubed, over ten cubed, times a fifth.",
            "Split ten cubed into five cubed times two cubed — same move as before.",
            D('Write "= 5 · 1/5 = 1"'),
            "Two cubed cancels, one five is left. Five times a fifth: one.",
            D('Circle choice 2'),
            "Only choice two gives one.",
            "Which route is better? If the exponent laws feel slow, plug in — it's usually the quicker one."]})

    # q-294: kept the Hebrew's sqrt(1/3), base 3 and answer 3 -> base 5, sqrt 176 / sqrt 11, answer 4
    S('q-294', stem='$\\frac{\\sqrt{\\frac{1}{5}}\\cdot\\sqrt{176}\\cdot\\sqrt[6]{5^3}}{\\sqrt{11}}=\\ ?$',
      choices=['$\\sqrt5$', '$4$', '$\\sqrt{11}$', '$16$'], correct=2, expl=[
        'Write the sixth root as a power: $\\sqrt[6]{5^3}=5^{\\frac36}=5^{\\frac12}=\\sqrt5$.',
        'Now every root is a square root. Top: $\\sqrt{\\frac15\\cdot176\\cdot5}=\\sqrt{176}$.',
        '$\\frac{\\sqrt{176}}{\\sqrt{11}}=\\sqrt{\\frac{176}{11}}=\\sqrt{16}=4$.'])
    V('q-294', {
        2: ["Look at the roots. Square roots on top, a square root underneath — and one sixth root.",
            "Before anything else, make every root the same order.",
            D('Under the sixth root write "= 5^(3/6)"'),
            "Turn the root into a power. The base stays five. The power goes on top, the root goes underneath: three over six.",
            "Little memory trick: the power is up in the sky, the root is down in the ground.",
            D('Write "= 5^(1/2) = √5"'),
            "Three sixths is a half. Five to the half — that's just root five.",
            "Shortcut: you're allowed to cancel the root's index with the power. Divide both by three — square root of five to the one.",
            "Now the whole top is square roots. Multiply them under ONE root.",
            D('Write "√(1/5 · 176 · 5)" over the top'),
            "Root of a fifth, times a hundred seventy-six, times five.",
            D('Cancel the 1/5 with the 5; write "= √176"'),
            "A fifth and a five cancel. Root one seventy-six on top.",
            "Some students spot it even earlier — root a fifth and root five cancel straight away. Same result.",
            D('Write "√176 / √11 = √(176/11) = √16 = 4"'),
            "Same order on top and bottom — divide first, then take the root. A hundred seventy-six over eleven is sixteen. Root sixteen: four.",
            D('Circle choice 2'),
            "Four. Choice two."]})

    # q-298: the Hebrew form (+ in the bottom), key 1 and the plug-in 4 and 1 (values 1, 5, 3, 0) -> plug 9 and 1, key 3
    S('q-298', stem='Given: $m>0$ and $n>0$. $\\dfrac{m-n}{\\sqrt{m}+\\sqrt{n}}=\\ ?$',
      choices=['$m+n$', '$0$', '$\\sqrt{m}-\\sqrt{n}$', '$\\sqrt{m}+\\sqrt{n}$'], correct=3, expl=[
        'Write the top as a difference of squares of roots: $m-n=(\\sqrt m+\\sqrt n)(\\sqrt m-\\sqrt n)$.',
        'Cancel $\\sqrt m+\\sqrt n$ (it is positive, so it is not 0). The result is $\\sqrt m-\\sqrt n$.',
        'Check with $m=9$, $n=1$: $\\frac{9-1}{3+1}=2$, and $\\sqrt9-\\sqrt1=2$ ✓.'])
    V('q-298', {
        2: ["The choices have no denominator. So we need to get rid of it.",
            "No common factor on top. So what can we do? Spot the third contracted multiplication formula.",
            D('Write "m − n = (√m + √n)(√m − √n)"'),
            "m minus n is root m plus root n, times root m minus root n.",
            "Check: root m times root m is m. Root n times minus root n is minus n. The middle terms cancel.",
            "We're used to this formula with squares. It works just as well with square roots.",
            D('Cancel (√m + √n) top and bottom'),
            "Now the root m plus root n cancels with the denominator.",
            D('Circle choice 3'),
            "What's left: root m minus root n. Choice three."],
        3: ["Plug in. Pick numbers with clean roots: nine and one.",
            "And plug in smart — m is nine, n is one, so the top stays positive.",
            D('Next to the choices write: 10, 0, 2, 4'),
            "Check the choices: nine plus one is ten. Zero. Three minus one is two. Three plus one is four. All different — one substitution is enough.",
            D('In the question write "(9 − 1)/(3 + 1) = 2"'),
            "The question: nine minus one is eight. Root nine plus root one: three plus one, four. Eight over four: two.",
            D('Circle choice 3'),
            "Two — choice three. The plug-in is the easy route for most students."]})

    # memory card: a^(b+1) = 1 was the Hebrew x^(y+1) = 1 -> a^(b+4) = 1
    rows = M.card('mem-r26-t11-advanced')['tables'][0]['rows']
    new_ex = {'Power $=1$': '$a^{b+4}=1$, $a\\ne1\\Rightarrow b=-4$ or $a=-1$',
              '"A or B" necessarily true?': '$a=3$, $b=-4$ kills "$a=0$ or $b\\ne-4$"'}
    for r in rows:
        if r[0] in new_ex: r[2] = new_ex.pop(r[0])
    assert not new_ex, new_ex


_apply_before_hebrew_backcheck = apply


def apply(M):
    _apply_before_hebrew_backcheck(M)
    hebrew_backcheck(M)   # 2026-10-06 Hebrew back-check: runs last
