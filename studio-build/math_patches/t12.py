"""Topic 12 - Inequalities. Course review 2026-09 fixes.
See t12_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q

TOPIC = 12
L1 = 'inequalities'
L2 = 'inequality-systems'
SIGNS = 'r26-t12-signs'
COMBINE = 'r26-t12-combining'
ADV = 'inequalities-advanced'
PRACTICE = 'unit-t12-3'
# advanced solution videos: old numbers 9-16 plus the new guided questions 17-20 (renumbered in course order at build)
ADV_SIDEBAR = ['Question %d' % n for n in range(9, 21)]


def cases(*rows):
    return '$\\begin{cases} ' + ' \\\\ '.join(rows) + ' \\end{cases}$'


def given(rows, ask, pre=''):
    return pre + 'Given:\n' + cases(*rows) + '\n' + ask


def _fix_draw(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _replace_say(M, vid, n, old, new):
    """Replace a whole spoken line (matched by a substring). new=None deletes it."""
    def fn(lines):
        out = []
        for l in lines:
            if 'say' in l and old in l['say']:
                if new is None: continue
                l = dict(l, say=new)
            out.append(l)
        return out
    M.edit_lines(vid, n, fn)


def _insert_after(M, vid, n, match, new_lines):
    def fn(lines):
        for k, l in enumerate(lines):
            if match in (l.get('say') or l.get('draw') or ''):
                return lines[:k + 1] + new_lines + lines[k + 1:]
        raise KeyError(match)
    M.edit_lines(vid, n, fn)


def _solution(M, qid, intro, slides, after=None):
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=ADV_SIDEBAR.index('Question %d' % n), title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Advanced Inequalities', ADV_SIDEBAR, beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = 'Advanced Inequalities'
    v['hybrid']['num'] = 35
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def apply(M):
    # =====================================================================================
    # 1. Lesson 1 "Inequalities"
    # =====================================================================================
    # slide 4: Pass 2 - the original demo and advice come back (only ":" becomes "÷"); the x example is a kept
    # addition and gets its own slide right after it (inserted below, after the slide-5/7 edits).
    _fix_draw(M, L1, 4, '":(−4)"', '"÷(−4)"')
    _fix_draw(M, L1, 4, '":4"', '"÷4"')
    _fix_draw(M, L1, 5, '":2"', '"÷ 2"')
    rec = M.slide(L1, 7)
    rec['items'][1]['t'] = '$\\times$ or $\\div$ by a negative $\\to$ flip the sign'
    M.touched_videos.add(L1)
    M.insert_slides(L1, 4, [dict(mode='concept', active=M.slide(L1, 4)['active'], title='The same with x', script=[
        "Now the same with x.",
        A('−2x < 6 appears', T('$-2x<6$', size=64, gap=40)),
        "Negative two x is less than six.",
        D('Write "÷(−2):  x > −3"'),
        "Way one: divide by negative two — and flip. x is greater than negative three.",
        D('Write "−6 < 2x", then "−3 < x"'),
        "Way two: move the terms across, like in an equation. Negative two x goes right and becomes two x. Six goes left and becomes negative six.",
        "Negative six is less than two x. Divide by two — positive, no flip. Negative three is less than x.",
        "Same answer. And the sign never had to flip. That's the way I recommend.",
        D('Write "x = 0: 0 < 6 ✓"'),
        "Quick check: x equals zero. Zero is less than six — and zero is greater than negative three. It fits.",
    ])])

    # =====================================================================================
    # 2. Lesson 2 "Systems of Inequalities"
    # =====================================================================================
    s6 = M.slide(L2, 6)
    rule = dict(s6['items'][1])
    M.set_slide(L2, 6, script=[
        "Second-degree inequalities: x squared.",
        "First, get rid of the fractions. Multiply both sides by six — a positive number, so nothing flips.",
        D('Write "2(5x² − 3) < 3(2x² + 10)"'),
        "Six over three is two, six over two is three. Two times the left top, three times the right top.",
        D('Write "10x² − 6 < 6x² + 30", then "4x² < 36", then "x² < 9"'),
        "Open the brackets, x's left, numbers right: four x squared less than thirty-six. x squared less than nine.",
        A('The x² rule appears', rule),
        "The rule: x squared on the SMALL side — x is trapped between the roots. On the BIG side — it's outside them.",
        D('Write "−3 < x < 3"'),
        "Root of nine is three. So x is between negative three and three.",
        "Why? Two squared is four — fine. Four squared is sixteen — too big. And negative two squared is four too. It's symmetric.",
        "Now the big side.",
        D('Write "−2x² ≤ −32  →  ÷(−2), flip:  x² ≥ 16"'),
        "Negative two x squared, less than or equal to negative thirty-two. Divide by negative two — and flip. x squared is at least sixteen.",
        D('Write "x ≥ 4  or  x ≤ −4"'),
        "x squared on the BIG side — x is outside the roots. x is at least four, or at most negative four.",
        "Check: negative five squared is twenty-five — at least sixteen. It works. Two squared is four — too small.",
    ])
    r8 = M.slide(L2, 8)
    r8['items'][3]['t'] = '$x^2$ small side: between the roots · big side: outside'
    M.touched_videos.add(L2)

    # =====================================================================================
    # 3. Existing solution videos
    # =====================================================================================
    _fix_draw(M, 'solve-q-322', 2, '":2"', '"÷ 2"')
    # Q5: explain the x^4 < x^5 remark
    _replace_say(M, 'solve-q-326', 2, 'Chaining tip',
                 "Another way: x to the fourth is less than x to the fifth. Divide by x to the fourth — it's positive — and x is bigger than one. That kills the negatives in one step.")
    # Q7: no "cross-multiply"
    M.set_slide('solve-q-328', 2, title='Multiply by 6, then the rule')
    _replace_say(M, 'solve-q-328', 2, 'Cross-multiply', "Fractions first. Multiply both sides by six — positive, so no flip.")
    _replace_say(M, 'solve-q-328', 2, 'Two times the left top',
                 "Six over three is two, six over two is three. Two times the left top, three times the right top.")
    # Q9: multiply by a positive number, and why the pattern works
    _fix_draw(M, 'solve-q-330', 2, 'Cross-multiply the first: write', 'Multiply both sides by 2(x + 1): write')
    _fix_draw(M, 'solve-q-330', 2, 'Cross-multiply the second: write', 'Multiply both sides by 8(x + 1): write')
    _replace_say(M, 'solve-q-330', 2, 'Cross-multiply: x plus one',
                 "Multiply both sides by two times x plus one — a positive number. x plus one is less than two x. So x is bigger than one.")
    _insert_after(M, 'solve-q-330', 3, 'Consecutive numbers.', [
        {'say': "And x over x plus one grows as x grows: one half, two thirds, three quarters — each one closer to one."}])
    # Q11: point to the sign table
    _insert_after(M, 'solve-q-332', 2, "long and exhausting", [
        {'say': "A shorter way to write it: the sign table. Mark three and nine on the line, and test one number in each part."}])
    # Q13: number line
    _insert_after(M, 'solve-q-334', 2, 'One long chain', [
        {'draw': 'Draw a number line and mark, from left to right: c + b, a, c, b'},
        {'say': "Put it on a number line: c plus b, then a, then c, then b. Left to right."}])
    # Q16: the list of numbers to try
    M.edit_lines('solve-q-337', 3, lambda ls: ls + [
        {'draw': 'Write "Try: 0, 1, −1, ½, a big number"'},
        {'say': "Your list for these questions: zero, one, negative one, one half, and a big number."}])
    for vid in ['solve-q-%d' % n for n in range(330, 338)]:
        M.set_sidebar(vid, ADV_SIDEBAR)

    # =====================================================================================
    # 4. Existing questions: TeX, stacked conditions, full solutions
    # =====================================================================================
    S = M.set_q
    S('q-322', stem='Given: $3+x<15+3x$. For which values of $x$ does the inequality hold?', expl=[
        'Move the $x$ terms to the side with more $x$ (the right): $3-15<3x-x$, so $-12<2x$.',
        'Divide by $2$ (positive, so no flip): $-6<x$.',
        'Check: $x=0$ gives $3<15$ ✓, and only choice (3) includes $0$.'])
    S('q-323', stem='Given: $3(4-3x)-7<8-9x$. For which values of $x$ does the inequality hold?',
      choices=['$0$', '$12$', '$1$', 'Any value'], expl=[
        'Open the brackets: $12-9x-7<8-9x$, so $5-9x<8-9x$.',
        'Add $9x$ to both sides: $5<8$. The $x$ is gone, and $5<8$ is always true.',
        'Therefore the inequality holds for every value of $x$.'])
    S('q-324', stem='Given: $2x-5<x+3<3x-9$. Which of the following is the most precise range for $x$?', expl=[
        'Split the chain into two inequalities.',
        'Left part: $2x-5<x+3$, so $x<8$.',
        'Right part: $x+3<3x-9$. Move the $x$ terms right: $12<2x$, so $6<x$.',
        'Both must hold: $6<x<8$.'])
    S('q-325', stem='Given: $3x+30<12+6x<30$. For which values of $x$ does the inequality hold?',
      choices=['$6<x$', '$x<3$', 'For no value of $x$', '$0<x$'], expl=[
        'Left part: $3x+30<12+6x$, so $18<3x$ and $x>6$.',
        'Right part: $12+6x<30$, so $6x<18$ and $x<3$.',
        'No number is both greater than $6$ and less than $3$. Therefore no value of $x$ satisfies the inequality.'])
    S('q-326', stem='$x$ is an integer, and $x^4<90<x^5$. What is $x$?', expl=[
        'If $x<0$, then $x^5<0$, and a negative number cannot be greater than $90$. Choices (1) and (4) are out.',
        '$x=3$: $3^4=81<90$ ✓ and $3^5=243>90$ ✓.',
        '$x=2$: $2^5=32$, and $32>90$ is false ✗.',
        'Therefore $x=3$.'])
    S('q-327', stem=given(['x<y+2', '2y-2<x'], 'Which of the following is necessarily true?'), expl=[
        'Chain the two inequalities through $x$: $2y-2<x<y+2$.',
        'Ignore the middle: $2y-2<y+2$, so $y<4$.',
        '$x<y$ and $y<x$ are both possible. With $y=1$ the givens say $0<x<3$: $x=0.5$ gives $x<y$, and $x=2.5$ gives $y<x$.'])
    S('q-328', stem='Given: $\\frac{5x^2-2}{3}<\\frac{2x^2+20}{2}$. Which of the following is correct?', expl=[
        'Multiply both sides by $6$ (positive, so no flip): $2(5x^2-2)<3(2x^2+20)$.',
        'Open the brackets: $10x^2-4<6x^2+60$, so $4x^2<64$ and $x^2<16$.',
        '$x^2$ is on the small side, so $x$ is between the roots: $-4<x<4$.'])
    S('q-329', stem=given(['a+b=c', 'a<c<b'], 'Which of the following is necessarily true?'),
      choices=['$ab<0$', '$ab=0$', '$0<c$', '$c<0$'], expl=[
        'Substitute $c=a+b$: $a<a+b<b$.',
        'Left part: $a<a+b$, so $0<b$. Right part: $a+b<b$, so $a<0$.',
        '$a$ is negative and $b$ is positive, so $ab<0$.',
        'The sign of $c$ is not fixed: $a=-1$, $b=3$ gives $c=2$, and $a=-3$, $b=1$ gives $c=-2$.'])
    S('q-330', stem='$x$ is a positive integer, and $\\frac{40}{80}<\\frac{x}{x+1}<\\frac{70}{80}$. How many values can $x$ have?', expl=[
        'Simplify: $\\frac{40}{80}=\\frac12$ and $\\frac{70}{80}=\\frac78$.',
        '$x$ is positive, so $x+1$ is positive. We can multiply by it without flipping.',
        'Left part: $\\frac12<\\frac{x}{x+1}$ gives $x+1<2x$, so $1<x$.',
        'Right part: $\\frac{x}{x+1}<\\frac78$ gives $8x<7x+7$, so $x<7$.',
        'Therefore $1<x<7$: $x=2, 3, 4, 5, 6$. That is five values.'])
    S('q-331', stem='Given: $(ab)^2<ab^2$. Which of the following is the most precise range for $a$?', expl=[
        '$(ab)^2=a^2b^2$, so $a^2b^2<ab^2$.',
        'If $b=0$, both sides are $0$, and $0<0$ is false. Therefore $b\\ne0$ and $b^2>0$.',
        'Divide both sides by $b^2$ (positive, so no flip): $a^2<a$.',
        '$a^2\\ge0$ and $a>a^2$, so $a>0$. Divide by $a$ (positive): $a<1$.',
        'Therefore $0<a<1$.'])
    S('q-332', stem='Given: $\\frac{x-3}{9-x}<0$, and $x\\ne9$. Which of the following ranges does not satisfy the inequality?', expl=[
        'Try one number from each range.',
        'Choice (1), $x=0$: $\\frac{-3}{9}<0$ ✓.',
        'Choice (2), $x=6$: $\\frac{3}{3}=1$, which is not negative ✗.',
        'Choices (3) and (4): $x=10$ gives $\\frac{7}{-1}=-7<0$ ✓, and $x=15$ gives $\\frac{12}{-6}=-2<0$ ✓.',
        'With a sign table: the top is $0$ at $x=3$ and the bottom is $0$ at $x=9$. The fraction is negative for $x<3$ or $x>9$. Therefore the range $3<x<9$ does not satisfy it.'])
    S('q-333', stem=given(['(x+y)^2=100', 'x-3>0'], 'Which of the following is necessarily true?',
                          pre='$x$ and $y$ are positive integers.\n'), expl=[
        '$x$ and $y$ are positive, so $x+y>0$. From $(x+y)^2=100$: $x+y=10$.',
        'From $x-3>0$: $x>3$.',
        'Substitute $x=10-y$: $10-y>3$, so $y<7$. Also $y>0$.',
        'Therefore $0<y<7$.',
        'Choices (3) and (4) are not necessary: $x=9$, $y=1$ breaks (3), and $x=4$, $y=6$ breaks (4).'])
    S('q-334', stem=given(['c+b<a', 'a<c<b'], 'Which of the following is not necessarily true?'), expl=[
        'Chain: $c+b<a<c<b$.',
        'From $c+b<c$: $b<0$. From $c+b<b$: $c<0$. From $a<c$: $a<0$.',
        'So (1), (2) and (3) are all true.',
        '$c+b$ is a sum of two negative numbers, so it is negative. Therefore $0<c+b$ is never true — it is the answer.'])
    S('q-335', stem='$x$ is an integer, and $2\\le x^2-2\\le34$. How many values can $x$ have?', expl=[
        'Add $2$ to all three parts: $4\\le x^2\\le36$.',
        'For positive $x$: $2\\le x\\le6$. The negatives are a mirror image: $-6\\le x\\le-2$.',
        'The integers: $\\pm2, \\pm3, \\pm4, \\pm5, \\pm6$. That is $10$ values.'])
    S('q-336', stem=given(['-4<x<10', '-30<y<6'], 'What is the range of the product $xy$?'), expl=[
        'Negative numbers are involved, so check all four corners: $(-4)(-30)=120$, $(-4)\\cdot6=-24$, $10\\cdot(-30)=-300$, $10\\cdot6=60$.',
        'The largest is $120$ and the smallest is $-300$.',
        'Therefore $-300<xy<120$.'])
    S('q-337', stem='Given: $x<y$. Which of the following is necessarily true?', expl=[
        '$y<y+5$, so $x<y<y+5$. Therefore $x<y+5$ always.',
        'Counterexamples for the others:',
        '(1) $x=-10$, $y=-9$: $5y=-45$, and $-10<-45$ is false.',
        '(2) $x=1$, $y=2$: $x+5=6$, and $6<2$ is false.',
        '(3) $x=1$, $y=2$: $5x=5$, and $5<2$ is false.'])
    S('q-338', stem='$m$ is a negative integer, and $m=x+y-8$. Which of the following is necessarily true about $x+y$?',
      choices=['It is an integer smaller than $8$.', 'It is an integer greater than $8$.',
               'It is an integer smaller than $0$.', 'It is an integer greater than $0$.'], expl=[
        '$x+y=m+8$.',
        '$m$ is a negative integer, so $m\\le-1$. Therefore $x+y\\le7$, which is smaller than $8$. An integer plus $8$ is an integer.',
        '$x+y$ does not have to be negative: $m=-1$ gives $x+y=7$. It does not have to be positive: $m=-10$ gives $x+y=-2$.'])
    S('q-339', stem=given(['2x+5<0', 'x^2<15'], 'What is $x$?', pre='$x$ is an integer.\n'), expl=[
        'From $2x+5<0$: $x<-2.5$.',
        'From $x^2<15$: $-\\sqrt{15}<x<\\sqrt{15}$. Since $3^2=9<15<16=4^2$, the integer $x$ is between $-3$ and $3$.',
        'The only integer that is less than $-2.5$ and not less than $-3$ is $x=-3$.',
        'Check: $2(-3)+5=-1<0$ ✓ and $(-3)^2=9<15$ ✓.'])
    S('q-341', stem='$x$ is an integer, and $x^3<x^2<3$. What is $x$?', expl=[
        'Try the choices.',
        '$x=-1$: $x^3=-1$ and $x^2=1$, and $-1<1<3$ ✓.',
        '$x=0$: $0<0$ is false. $x=1$: $1<1$ is false.',
        '$x=-2$: $x^2=4$, and $4<3$ is false.',
        'Therefore $x=-1$.'])
    S('q-342', stem='Given: $6<x<7$. Which of the following is necessarily true?', expl=[
        'Simplify each choice.',
        '(1) $x+6<2x$ means $6<x$. This is given, so it is always true.',
        '(2) $x+7<2x$ means $7<x$: never true here.',
        '(3) $13<2x$ means $6.5<x$: not always (take $x=6.2$).',
        '(4) $14<2x$ means $7<x$: never true here.'])
    S('q-343', stem=given(['p<q', 'r<s', 'q<s'], 'Which of the following cannot be true?'), expl=[
        'Chain: $p<q<s$, so $p<s$ always. Therefore $s<p$ cannot be true.',
        'The others can be true, because $r$ only has to be below $s$. Take $p=1$, $q=2$, $s=5$: $r=3$ gives $q<r$, and $r=0$ gives $r<q$ and $r<p$.'])
    S('q-344', stem='Given: $x-3<6$. How many positive integers $x$ satisfy the inequality?', expl=[
        'Add $3$: $x<9$.',
        'The positive integers below $9$ are $1, 2, 3, 4, 5, 6, 7, 8$. That is $8$ numbers.'])
    S('q-345', stem='Given: $-2x^2\\le-32$. Which of the following values of $x$ does not satisfy the inequality?', expl=[
        'Divide by $-2$ and flip the sign: $x^2\\ge16$. (Or move the terms across with no flip: $32\\le2x^2$, so $16\\le x^2$.)',
        '$x^2$ is on the big side, so $x$ is outside the roots: $x\\le-4$ or $x\\ge4$.',
        '$-6$, $4$ and $100$ satisfy it. $x=-2$ gives $x^2=4<16$, so $-2$ does not.'])
    S('q-346', stem='Given: $a+4<\\frac{a}{2}$. Which of the following is correct?', expl=[
        'Multiply both sides by $2$ (positive, so no flip): $2a+8<a$.',
        'Subtract $a$: $a+8<0$, so $a<-8$.',
        'Check: $a=-10$ gives $-6<-5$ ✓.'])
    S('q-347', stem=given(['0<x<1', '5y=2x'], 'Which of the following is correct?'), expl=[
        '$y=\\frac{2x}{5}$. Since $0<x<1$: $0<y<\\frac25$.',
        'The square of a number between $0$ and $1$ is even smaller: $0<y^2<\\frac{4}{25}$, and $\\frac{4}{25}<1$.',
        'Therefore $y^2<1$.'])
    S('q-348', stem=given(['a+b=17', 'b<a'], 'Which of the following is necessarily true?',
                          pre='$a$ and $b$ are positive integers.\n'), expl=[
        '$b<a$, so $2b<a+b=17$ and $b<8.5$. $b$ is an integer, so $b\\le8<9$.',
        'Counterexamples for the others: $a=9$, $b=8$ breaks (1). $a=16$, $b=1$ breaks (2) and (4).'])
    S('q-349', stem='Given: $3y<x<-3y$. Which of the following is correct?', expl=[
        'Ignore the middle: $3y<-3y$.',
        'Add $3y$: $6y<0$, so $y<0$.',
        'Check: $y=-1$ gives $-3<x<3$, which has solutions. $y=0$ gives $0<x<0$, which is impossible.'])
    S('q-350', stem=given(['0<a-b', 'a+b<0'], 'Which of the following is necessarily true?'), expl=[
        'From the first: $b<a$. From the second: $a<-b$.',
        'Chain: $b<a<-b$, so $b<-b$ and $2b<0$. Therefore $b<0$.',
        'Or add two inequalities in the same direction: $b-a<0$ and $a+b<0$ give $2b<0$.',
        'The sign of $a$ is not fixed: $a=1$, $b=-2$ and $a=-1$, $b=-2$ both fit.'])
    S('q-351', stem=given(['5x+2y=0', 'x>2'], 'Which of the following is necessarily true?'), expl=[
        '$2y=-5x$.',
        '$x>2$, so $5x>10$. Multiply by $-1$ and flip: $-5x<-10$.',
        'Therefore $2y<-10$ and $y<-5$.',
        'Check: $x=4$ gives $y=-10$, which is less than $-5$ ✓ and is outside choice (2).'])
    S('q-352', stem='Given: $0<3x-9x^2$. Which of the following is necessarily true?',
      choices=['$x<-\\frac13$', '$-\\frac13<x<0$', '$0<x<\\frac13$', '$\\frac13<x$'], expl=[
        'Take out a common factor: $3x-9x^2=3x(1-3x)$.',
        'Sign table: the product is $0$ at $x=0$ and at $x=\\frac13$. Test one number in each part.',
        '$x=-1$: $3(-1)(1+3)=-12<0$ ✗. $x=\\frac16$: $\\frac12\\cdot\\frac12=\\frac14>0$ ✓. $x=1$: $3\\cdot(-2)=-6<0$ ✗.',
        'Therefore $0<x<\\frac13$.'])
    S('q-353', stem=given(['x<0', '3<x^2-6<19'], 'Which of the following is correct?'), expl=[
        'Add $6$ to all three parts: $9<x^2<25$.',
        'For positive $x$: $3<x<5$. For negative $x$: $-5<x<-3$.',
        '$x<0$, so $-5<x<-3$.'])
    S('q-354', stem='Given: $\\frac{3+n}{3-n}>0$, and $n\\ne3$. What is the most precise range for $n$?', expl=[
        'Sign table: the top is $0$ at $n=-3$, and the bottom is $0$ at $n=3$.',
        '$n=-4$: $\\frac{-1}{7}<0$ ✗. $n=0$: $\\frac33=1>0$ ✓. $n=4$: $\\frac{7}{-1}=-7<0$ ✗.',
        'Therefore $-3<n<3$.'])
    S('q-355', stem=given(['x>0', '\\frac14<\\frac{x}{x+1}<\\frac34'], 'What is the most precise range for $x$?'), expl=[
        '$x>0$, so $x+1>0$. We can multiply by it without flipping.',
        'Left part: $\\frac14<\\frac{x}{x+1}$ gives $x+1<4x$, so $1<3x$ and $x>\\frac13$.',
        'Right part: $\\frac{x}{x+1}<\\frac34$ gives $4x<3x+3$, so $x<3$.',
        'Therefore $\\frac13<x<3$.'])
    S('q-356', stem=given(['x^2y^2=(xy-2)^2', 'x>1'], 'Which of the following is necessarily true?'), expl=[
        '$x^2y^2=(xy)^2$. Two numbers with equal squares are equal or opposite.',
        'Equal: $xy=xy-2$ gives $0=-2$, which is impossible.',
        'Opposite: $xy=-(xy-2)$, so $2xy=2$ and $xy=1$.',
        'Therefore $y=\\frac1x$. Since $x>1$: $0<y<1$.',
        'Check with $x=2$, $y=\\frac12$: $x^2y^2=1$ and $(1-2)^2=1$ ✓.'])
    S('q-357', stem=given(['y^2a+y^2c<(a+c)^2', 'a+c=y'], 'Which of the following cannot be the value of $y$?'),
      choices=['$2$', '$\\frac13$', '$-\\frac13$', '$-2$'], expl=[
        'Take out $y^2$: $y^2(a+c)<(a+c)^2$.',
        'Substitute $a+c=y$: $y^3<y^2$.',
        'So $y^2(y-1)<0$. This needs $y\\ne0$, and then $y^2>0$, so $y-1<0$ and $y<1$.',
        '$\\frac13$, $-\\frac13$ and $-2$ are all less than $1$. But $y=2$ gives $8<4$, which is false. Therefore $y$ cannot be $2$.'])
    # the easy extras
    X = 'alg-extra-unit-t12-3-'
    S(X + '1', stem='Given: $-3x>9$. Which of the following is correct?', expl=[
        'Divide by $-3$ and flip the sign: $x<-3$.',
        'Or move the terms across with no flip: $-9>3x$, so $-3>x$. Same answer.'])
    S(X + '2', stem='How many integers $x$ satisfy $-3<x<5$?', choices=['$6$', '$7$', '$8$', '$9$'], expl=[
        'The integers are $-2, -1, 0, 1, 2, 3, 4$. The ends $-3$ and $5$ are not included.',
        'That is $7$ integers.'])
    S(X + '3', stem='Given: $0<x<1$. Which of the following is necessarily true?', expl=[
        'Multiply $x<1$ by $x$ (positive, so no flip): $x^2<x$.',
        'Check: $x=\\frac12$ gives $\\frac14<\\frac12$ ✓.'])
    S(X + '4', stem='Given: $2x+3\\le13$. Which of the following is correct?', expl=[
        'Subtract $3$: $2x\\le10$.',
        'Divide by $2$ (positive, so no flip): $x\\le5$.'])
    S(X + '5', stem='Given: $x>2$. Which of the following is necessarily true?', expl=[
        '$x$ and $2$ are both positive, so the reciprocals flip the sign: $\\frac1x<\\frac12$.',
        'Check: $x=4$ gives $\\frac14<\\frac12$ ✓.'])
    S(X + '6', stem=given(['x>3', 'x\\le5'], 'Which of the following describes all the values of $x$?'), expl=[
        'The overlap of $x>3$ and $x\\le5$ is $3<x\\le5$.',
        '$3$ is not included (the sign is $>$), and $5$ is included (the sign is $\\le$).'])
    S(X + '7', stem='Given: $a<b<0$. Which of the following is necessarily true?', expl=[
        '$a$ and $b$ have the same sign, so the reciprocals flip the sign: $\\frac1a>\\frac1b$.',
        'Check: $a=-4$, $b=-2$: $\\frac1a=-\\frac14$ and $\\frac1b=-\\frac12$, and $-\\frac14>-\\frac12$ ✓.',
        'The others: $a^2=16>4=b^2$, and $ab=8>0$.'])

    # Pass 2: q-340 is an original practice question and stays (text clean-up only)
    S('q-340', stem=given(['x^2<25', '3x+9<0'], 'What is $x$?', pre='$x$ is an integer.\n'), expl=[
        'From $x^2<25$: $-5<x<5$.',
        'From $3x+9<0$: $3x<-9$, so $x<-3$.',
        'The integers that satisfy both are strictly between $-5$ and $-3$: $x=-4$.',
        'Check: $(-4)^2=16<25$ ✓ and $3(-4)+9=-3<0$ ✓.'])

    # =====================================================================================
    # 5. New lesson video: signs, numbers between 0 and 1, reciprocals, must / could / cannot
    #    (start of the advanced section - Q10, Q11, Q13, Q16 and the practice need it)
    # =====================================================================================
    sb = ['Between 0 and 1', 'Reciprocals', 'Sign table', 'Must, could, cannot', 'Recap']
    M.new_video(SIGNS, TOPIC, 'Signs, Fractions & Must-Be-True', sb, [
        dict(mode='title', title='Signs, Fractions & Must-Be-True', script=[
            "Before the advanced questions — four tools.",
            "Numbers between zero and one, reciprocals, signs of a product, and the words must, could and cannot.",
        ]),
        dict(mode='concept', active=0, title='Between 0 and 1', script=[
            "Numbers between zero and one behave strangely.",
            A('0 < x < 1 order appears', T('$0<x<1:\\quad x^2<x<\\sqrt x<1<\\frac1x$', size=50, gap=50)),
            "Squaring makes them SMALLER. The root makes them BIGGER. And one over x is bigger than one.",
            A('x = 1/4 appears', T('$x=\\frac14:\\quad \\frac1{16}<\\frac14<\\frac12<1<4$', size=50, gap=50)),
            "Test it with one quarter. Squared: one sixteenth. Root: one half. One over it: four.",
            A('x > 1 order appears', T('$x>1:\\quad \\frac1x<1<\\sqrt x<x<x^2$', size=50, gap=50)),
            "Above one, the order turns around. Try four: one quarter, two, four, sixteen.",
            "Negative numbers? Don't memorize. Plug in negative one half and look.",
            D('Write "x = −½:  x² = ¼,  x³ = −⅛,  1/x = −2"'),
            "Negative one half squared is one quarter — positive. Cubed, it stays negative: negative one eighth. One over it: negative two.",
        ]),
        dict(mode='concept', active=1, title='Reciprocals', script=[
            "Now, one over a number: the reciprocal.",
            A('2 < 3 → 1/2 > 1/3 appears', T('$2<3\\ \\Rightarrow\\ \\frac12>\\frac13$', size=54, gap=50)),
            "Two is less than three. But one half is MORE than one third. The sign flips.",
            A('−3 < −2 → −1/3 > −1/2 appears', T('$-3<-2\\ \\Rightarrow\\ -\\frac13>-\\frac12$', size=54, gap=50)),
            "Both negative? It still flips. Negative one third is bigger than negative one half.",
            A('−2 < 3 → −1/2 < 1/3 appears', T('$-2<3\\ \\Rightarrow\\ -\\frac12<\\frac13$', size=54, gap=50)),
            "But one negative and one positive? No flip. The negative one stays smaller.",
            D('Write "same sign → flip;  different signs → no flip"'),
            "So: same sign — flip. Different signs — no flip.",
        ]),
        dict(mode='concept', active=2, title='Sign table', script=[
            "When is a product positive? When both factors have the same sign. Negative? Opposite signs.",
            "A fraction follows the same rule — and its bottom can't be zero.",
            A('3x(1 − 3x) > 0 appears', T('$3x(1-3x)>0$', size=60, gap=50)),
            "Instead of two long cases, use a sign table.",
            A('Zeros appear', T('Zeros: $x=0$ and $x=\\frac13$', size=46, gap=40)),
            "Step one: find where each factor is zero. Zero, and one third. Mark them on the number line.",
            "They cut the line into three parts. Step two: test one number in each part.",
            A('Tests appear', T('$x=-1$: $-12$ ✗ · $x=\\frac16$: $\\frac14$ ✓ · $x=1$: $-6$ ✗', size=40, gap=40)),
            "Negative one: three times negative one, times four. Negative twelve. No.",
            "One sixth: one half times one half. One quarter — positive. Yes.",
            "One: three times negative two. Negative six. No.",
            A('0 < x < 1/3 appears', T('$0<x<\\frac13$', size=60)),
            "So only the middle part works: x between zero and one third.",
        ]),
        dict(mode='concept', active=3, title='Must, could, cannot', script=[
            "Three question words — three different jobs.",
            A("'Necessarily true' appears", T('Necessarily true: one counterexample kills it', size=44, gap=36)),
            "Necessarily true: it must hold for EVERY number. Find one number where it fails — and it's out.",
            A("'Could be true' appears", T('Could be true: one example keeps it', size=44, gap=36)),
            "Could be true: find just ONE number where it works — and it's in.",
            A("'Cannot be true' appears", T('Cannot be true: it breaks the givens', size=44, gap=36)),
            "Cannot be true: it contradicts what you're given. No number makes it work.",
            A('Numbers to try appear', T('Try: $0$, $1$, $-1$, $\\frac12$, a big number', size=46)),
            "Which numbers to try? Zero, one, negative one, one half — and a big number.",
            "Most traps hide in the negatives and the fractions. Don't stop at two and three.",
        ]),
        dict(mode='concept', active=4, title='Recap', script=[
            "Let's lock it in.",
            A("'Between 0 and 1' appears", T('$0<x<1$: $x^2<x<\\sqrt x$ and $\\frac1x>1$', size=40)),
            A("'Reciprocals' appears", T('Reciprocals: same sign $\\to$ flip; different signs $\\to$ no flip', size=40)),
            A("'Sign table' appears", T('Product or fraction: zeros on the line, test each part', size=40)),
            A("'Must, could, cannot' appears", T('Must: find a counterexample · Could: find an example', size=40)),
            A("'Try' appears", T('Try $0$, $1$, $-1$, $\\frac12$ and a big number', size=40)),
            D('Tick each line'),
            "Two questions on these tools next. Try each one first — then watch.",
        ]),
    ], ADV, before='q-330')
    M.video(SIGNS)['hybrid']['num'] = 35

    # ---- guided question: numbers between -1 and 0
    g1 = 'q-r26-t12-01'
    M.new_q(g1, TOPIC, 'Given: $-1<x<0$. Which of the following is the greatest?',
            ['$x$', '$x^2$', '$x^3$', '$\\frac1x$'], 2, [
        'Plug in a number from the range: $x=-\\frac12$.',
        '$x=-\\frac12$, $x^2=\\frac14$, $x^3=-\\frac18$, $\\frac1x=-2$.',
        'Only $x^2$ is positive. Therefore $x^2$ is the greatest.',
        'Why: an even power of a negative number is positive. An odd power and the reciprocal stay negative.'])
    M.place_q(g1, ADV, after=SIGNS)
    _solution(M, g1, ["Question seventeen.", "A negative number between minus one and zero. Plug one in."], [
        ('Plug in a number', [
            "x is between negative one and zero. Pick a friendly number: negative one half.",
            D('Write "x = −½"'),
            D('Next to the choices write "−½,  ¼,  −⅛,  −2"'),
            "x itself: negative one half. x squared: one quarter. x cubed: negative one eighth. One over x: negative two.",
            "Three of them are negative. Only one is positive.",
            D('Circle choice 2'),
            "x squared. Choice two.",
            "Why? An even power kills the minus. An odd power and one over x keep it.",
        ]),
    ])

    # ---- guided question: sign table
    g2 = 'q-r26-t12-02'
    M.new_q(g2, TOPIC, 'Given: $(x-2)(x+5)<0$. Which of the following is correct?',
            ['$x<-5$ or $x>2$', '$-5<x<2$', '$-2<x<5$', '$x<2$'], 2, [
        'Sign table: the product is $0$ at $x=2$ and at $x=-5$. Mark them on the number line.',
        'Test one number in each part. $x=-6$: $(-8)(-1)=8>0$ ✗. $x=0$: $(-2)\\cdot5=-10<0$ ✓. $x=3$: $1\\cdot8=8>0$ ✗.',
        'Therefore $-5<x<2$.'])
    M.place_q(g2, ADV, after='solve-' + g1)
    _solution(M, g2, ["Question eighteen.", "A product that must be negative. Use the sign table."], [
        ('Sign table', [
            "A product less than zero: the two factors have opposite signs.",
            "Step one: where is each factor zero?",
            D('Write "x − 2 = 0 → x = 2;   x + 5 = 0 → x = −5"'),
            "x minus two is zero at two. x plus five is zero at negative five.",
            D('Draw a number line and mark −5 and 2'),
            "Three parts: left of negative five, between, and right of two.",
            D('Write "x = −6: (−8)(−1) = 8 ✗"'),
            "Negative six: negative eight times negative one. Eight — positive. No.",
            D('Write "x = 0: (−2)(5) = −10 ✓"'),
            "Zero: negative two times five. Negative ten. Yes.",
            D('Write "x = 3: (1)(8) = 8 ✗"'),
            "Three: one times eight. Positive. No.",
            D('Circle choice 2'),
            "Only the middle: between negative five and two. Choice two.",
            "Choice three is the trap — it flips the signs of the zeros. The zeros are two and negative five.",
        ]),
    ])

    # =====================================================================================
    # 6. New lesson video: combining inequalities and ranges (right before Q15, the xy range)
    # =====================================================================================
    sb = ['Add them', 'Never subtract', 'Multiply', 'Range of x²', 'Recap']
    M.new_video(COMBINE, TOPIC, 'Combining Inequalities & Ranges', sb, [
        dict(mode='title', title='Combining Inequalities & Ranges', script=[
            "Two inequalities — can we add them? Subtract them? Multiply them?",
            "The exam loves this. One move is safe. The others are traps.",
        ]),
        dict(mode='concept', active=0, title='Add them', script=[
            A('1 < a < 3 appears', T('$1<a<3$', size=58, gap=30)),
            A('2 < b < 5 appears', T('$2<b<5$', size=58, gap=30)),
            "a is between one and three. b is between two and five. What about a plus b?",
            A('3 < a + b < 8 appears', T('$3<a+b<8$', size=58, gap=50)),
            "Add them, part by part: one plus two is three. Three plus five is eight.",
            "Adding is safe — as long as both point the SAME way.",
            A('a > b and c > d appears', T('$a>b$ and $c>d$ $\\Rightarrow$ $a+c>b+d$ ✓', size=46)),
            "a bigger than b, c bigger than d: a plus c is bigger than b plus d. Always.",
        ]),
        dict(mode='concept', active=1, title='Never subtract', pre=[T('$1<a<3 \\qquad 2<b<5$', size=54, gap=50)], script=[
            "Now a minus b. Here's the trap.",
            D('Write "1 − 2 < a − b < 3 − 5  →  −1 < a − b < −2 ✗"'),
            "Subtract end from end? You get negative one less than a minus b less than negative two. That's nonsense.",
            "Think instead: when is a minus b the BIGGEST? a big, b small.",
            A('max appears', T('Biggest: $3-2=1$ $\\qquad$ Smallest: $1-5=-4$', size=46, gap=40)),
            "Biggest: three minus two. One. Smallest: a small, b big. One minus five. Negative four.",
            A('−4 < a − b < 1 appears', T('$-4<a-b<1$', size=58, gap=40)),
            "So a minus b is between negative four and one.",
            A('Rule appears', T('$a-b$: biggest $a$ minus smallest $b$', size=46)),
            "The rule: biggest minus smallest. Or flip b first — negative five less than minus b less than negative two — and then add.",
        ]),
        dict(mode='concept', active=2, title='Multiply', script=[
            A('All positive appears', T('$1<a<3,\\ 2<b<5\\ \\Rightarrow\\ 2<ab<15$', size=48, gap=50)),
            "Multiplying? Safe only when everything is positive. One times two is two. Three times five is fifteen.",
            A('With negatives appears', T('$-1<a<3,\\ 2<b<5$', size=48, gap=40)),
            "With a negative number inside, end-by-end breaks. Check all four corners.",
            A('Corners appear', T('$(-1)\\cdot2=-2 \\quad (-1)\\cdot5=-5 \\quad 3\\cdot2=6 \\quad 3\\cdot5=15$', size=42, gap=40)),
            "Negative one times two. Negative one times five. Three times two. Three times five.",
            A('−5 < ab < 15 appears', T('$-5<ab<15$', size=58)),
            "Smallest corner: negative five. Biggest: fifteen.",
            "Dividing works the same way: check the corners — and make sure the bottom can't be zero.",
        ]),
        dict(mode='concept', active=3, title='Range of x²', script=[
            A('−3 < x < 2 appears', T('$-3<x<2$', size=60, gap=50)),
            "What are the possible values of x squared?",
            A('Trap appears', T('Trap: $4<x^2<9$ ✗', size=50, gap=50)),
            "The trap: square the ends — four and nine. Wrong.",
            "Zero is inside the range. x can be zero — so x squared can be zero. That's the smallest.",
            "The biggest square comes from the end farthest from zero: negative three. Nine.",
            A('0 ≤ x² < 9 appears', T('$0\\le x^2<9$', size=60)),
            "So x squared is at least zero and less than nine.",
        ]),
        dict(mode='concept', active=4, title='Recap', script=[
            "Let's lock it in.",
            A("'Add' appears", T('Same direction: add them ✓', size=42)),
            A("'Subtract' appears", T('Never subtract: $a-b$ = biggest $a$ minus smallest $b$', size=42)),
            A("'Multiply' appears", T('Multiply: all positive, or check the four corners', size=42)),
            A("'x²' appears", T('$x^2$ range: $0$ inside? Then it starts at $0$', size=42)),
            D('Tick each line'),
            "Two questions on this next — then question fifteen, a product of two ranges.",
        ]),
    ], ADV, before='q-336')
    M.video(COMBINE)['hybrid']['num'] = 35

    g3 = 'q-r26-t12-03'
    M.new_q(g3, TOPIC, given(['a>b', 'c>d'], 'Which of the following is necessarily true?'),
            ['$a+c>b+d$', '$a-c>b-d$', '$ac>bd$', '$\\frac{a}{c}>\\frac{b}{d}$'], 1, [
        'Two inequalities in the same direction can be added: $a+c>b+d$ ✓.',
        'Counterexamples for the others:',
        '(2) $a=2$, $b=1$, $c=5$, $d=0$: $a-c=-3$ and $b-d=1$, and $-3>1$ is false.',
        '(3) $a=-1$, $b=-2$, $c=-1$, $d=-2$: $ac=1$ and $bd=4$, and $1>4$ is false.',
        '(4) $a=2$, $b=1$, $c=4$, $d=1$: $\\frac24=\\frac12$ and $\\frac11=1$, and $\\frac12>1$ is false.'])
    M.place_q(g3, ADV, after=COMBINE)
    _solution(M, g3, ["Question nineteen.", "Two inequalities. Which move is always safe?"], [
        ('Add — the safe move', [
            "Both inequalities point the same way. So we may add them.",
            D('Write "a + c > b + d ✓"'),
            D('Circle choice 1'),
            "a plus c is bigger than b plus d. Choice one.",
        ]),
        ('Counterexamples', [
            "Necessarily true — so for the others, one counterexample each.",
            D('Next to choice 2 write "a = 2, b = 1, c = 5, d = 0:  −3 > 1 ✗"'),
            "Subtracting: a is two, b is one, c is five, d is zero. a minus c is negative three. b minus d is one. Out.",
            D('Next to choice 3 write "a = −1, b = −2, c = −1, d = −2:  1 > 4 ✗"'),
            "Multiplying with negatives: negative one is bigger than negative two, twice. ac is one. bd is four. Out.",
            D('Next to choice 4 write "a = 2, b = 1, c = 4, d = 1:  ½ > 1 ✗"'),
            "Dividing: two over four is one half. One over one is one. Out.",
            "Only adding survives.",
        ]),
    ])

    g4 = 'q-r26-t12-04'
    M.new_q(g4, TOPIC, given(['-2<x<5', '1<y<4'], 'What is the range of $x-y$?'),
            ['$-6<x-y<4$', '$-3<x-y<1$', '$-1<x-y<9$', '$-6<x-y<1$'], 1, [
        'Do not subtract the inequalities end from end. To make $x-y$ big, take $x$ big and $y$ small.',
        'Biggest: $5-1=4$. Smallest: $-2-4=-6$.',
        'Therefore $-6<x-y<4$.',
        'Another way: $1<y<4$ gives $-4<-y<-1$. Now add: $-2+(-4)<x-y<5+(-1)$.',
        'Choice (2) is the trap: it subtracts end from end ($-2-1$ and $5-4$). Choice (3) adds the ranges.'])
    M.place_q(g4, ADV, after='solve-' + g3)
    _solution(M, g4, ["Question twenty.", "The range of a difference. Don't subtract end from end."], [
        ('Biggest minus smallest', [
            "When is x minus y the biggest? x as big as possible, y as small as possible.",
            D('Write "biggest: 5 − 1 = 4"'),
            "Five minus one. Four.",
            D('Write "smallest: −2 − 4 = −6"'),
            "The smallest: x small, y big. Negative two minus four. Negative six.",
            D('Write "−6 < x − y < 4"'),
            D('Circle choice 1'),
            "Between negative six and four. Choice one.",
            "Choice two is the trap: negative two minus one, and five minus four. End from end.",
            D('Write "−4 < −y < −1  →  add"'),
            "Want a check? Flip y: minus y is between negative four and negative one. Now add to x — same answer.",
        ]),
    ])

    for vid in ['solve-' + g for g in (g1, g2, g3, g4)]:
        M.set_sidebar(vid, ADV_SIDEBAR)

    # =====================================================================================
    # 7. Memory cards
    # =====================================================================================
    c = M.card('mem-inequalities')
    c['tables'][0]['rows'][3] = ['Tip: move x to the side where it stays positive ($-2x<6 \\Rightarrow -6<2x$)', 'no flip needed']
    c['tables'][0]['rows'].append(['Multiply by an unknown', 'only if you know its sign'])
    c['tables'][1]['rows'][3] = ['$x^2>a$', '$x>\\sqrt a$ or $x<-\\sqrt a$ (outside the roots). Example: $x^2\\ge16 \\Rightarrow x\\ge4$ or $x\\le-4$']
    M.new_card('mem-r26-t12-traps', TOPIC, ADV, {
        'title': 'Inequality traps',
        'intro': 'Combining inequalities, ranges, signs and the three question words.',
        'tables': [
            {'title': 'Combining and ranges', 'head': ['Situation', 'Rule', 'Example'], 'rows': [
                ['Add two inequalities', 'allowed if they point the same way', '$1<a<3$, $2<b<5 \\Rightarrow 3<a+b<8$'],
                ['Range of $a-b$', 'never subtract end from end: biggest $a$ minus smallest $b$', '$-4<a-b<1$'],
                ['Range of $ab$', 'all positive: multiply the ends; else check the four corners', '$-1<a<3$, $2<b<5 \\Rightarrow -5<ab<15$'],
                ['Range of $x^2$', 'if $0$ is inside, $x^2$ starts at $0$', '$-3<x<2 \\Rightarrow 0\\le x^2<9$'],
            ]},
            {'title': 'Signs and special numbers', 'head': ['Situation', 'Rule', 'Example'], 'rows': [
                ['$0<x<1$', '$x^2<x<\\sqrt x<1<\\frac1x$', '$x=\\frac14$: $\\frac1{16}<\\frac14<\\frac12<4$'],
                ['$x>1$', '$\\frac1x<1<\\sqrt x<x<x^2$', '$x=4$: $\\frac14<2<4<16$'],
                ['Reciprocals', 'same sign: flip; different signs: no flip', '$2<3 \\Rightarrow \\frac12>\\frac13$'],
                ['Product or fraction $>0$ or $<0$', 'sign table: zeros on the line, test one number in each part', '$3x(1-3x)>0 \\Rightarrow 0<x<\\frac13$'],
            ]},
            {'title': 'Question words', 'head': ['They ask', 'You do'], 'rows': [
                ['Necessarily true', 'find one counterexample to kill a choice'],
                ['Could be true', 'find one example to keep a choice'],
                ['Cannot be true', 'find the choice that breaks the givens'],
            ]},
        ],
        'tips': ['Numbers to try: $0$, $1$, $-1$, $\\frac12$ and a big number.',
                 'Trap: $a>b$ and $c>d$ do NOT give $a-c>b-d$ or $ac>bd$.']},
        after='solve-q-337')

    # =====================================================================================
    # 8. New practice questions (exam level)
    # =====================================================================================
    P = {}
    P['05'] = (given(['3<a<7', '-4<b<-1'], 'What is the range of $a-b$?'),
               ['$7<a-b<8$', '$4<a-b<11$', '$-1<a-b<6$', '$4<a-b<8$'], 2, [
        'Biggest $a-b$: biggest $a$ minus smallest $b$: $7-(-4)=11$.',
        'Smallest $a-b$: smallest $a$ minus biggest $b$: $3-(-1)=4$.',
        'Therefore $4<a-b<11$.'])
    P['06'] = ('Given: $-3<x<2$. Which of the following gives all the possible values of $x^2$?',
               ['$4<x^2<9$', '$0\\le x^2<9$', '$0\\le x^2<4$', '$-9<x^2<4$'], 2, [
        '$0$ is inside the range, so $x^2$ can be $0$ (at $x=0$). That is the smallest value.',
        'The biggest square comes from the end farthest from $0$: when $x$ is close to $-3$, $x^2$ is close to $9$.',
        'Therefore $0\\le x^2<9$. Choice (1) is the trap: it only squares the ends.'])
    P['07'] = (given(['x+y>10', 'x-y>4'], 'Which of the following is necessarily true?'),
               ['$y>3$', '$x>7$', '$x>14$', '$y<3$'], 2, [
        'Same direction, so add the inequalities: $(x+y)+(x-y)>10+4$, so $2x>14$ and $x>7$.',
        'You cannot subtract them to learn about $y$. $x=20$, $y=5$ fits ($25>10$ and $15>4$), and $x=20$, $y=-5$ fits too ($15>10$ and $25>4$). So neither (1) nor (4) is necessary.',
        '(3): $x=10$, $y=1$ fits ($11>10$ and $9>4$), but $10>14$ is false.'])
    P['08'] = ('Given: $x>1$. Which of the following is the smallest?',
               ['$\\frac1x$', '$\\frac1{x^2}$', '$\\sqrt x$', '$x$'], 2, [
        'Plug in $x=4$: $\\frac14$, $\\frac1{16}$, $2$, $4$. The smallest is $\\frac1{x^2}$.',
        'Why: for $x>1$, $x^2>x$, so $\\frac1{x^2}<\\frac1x<1$, while $\\sqrt x$ and $x$ are bigger than $1$.'])
    P['09'] = ('Given: $\\frac{x+1}{x-4}<0$. How many integers $x$ satisfy the inequality?',
               ['$3$', '$4$', '$5$', '$6$'], 2, [
        'Sign table: the top is $0$ at $x=-1$, and the bottom is $0$ at $x=4$.',
        '$x=-2$: $\\frac{-1}{-6}>0$ ✗. $x=0$: $\\frac{1}{-4}<0$ ✓. $x=5$: $\\frac61>0$ ✗.',
        'Therefore $-1<x<4$. ($x=-1$ gives $0$, which is not less than $0$, and $x=4$ is not allowed.)',
        'The integers are $0, 1, 2, 3$. That is $4$.'])
    P['10'] = ('Given: $x<y<0$. Which of the following could be true?',
               ['$xy<0$', '$x+y>0$', '$x^2<y^2$', '$x<2y$'], 4, [
        '(1) Two negative numbers: $xy>0$. Cannot be true.',
        '(2) Two negative numbers: $x+y<0$. Cannot be true.',
        '(3) $x$ is farther from $0$ than $y$, so $x^2>y^2$. Cannot be true.',
        '(4) One example is enough: $x=-3$, $y=-1$ gives $2y=-2$, and $-3<-2$ ✓. So it could be true.'])
    P['11'] = (given(['-2<a<1', '-2<b<1'], 'What is the range of $ab$?'),
               ['$-2<ab<1$', '$-2<ab<4$', '$1<ab<4$', '$-4<ab<1$'], 2, [
        'Negative numbers are involved, so check all four corners: $(-2)(-2)=4$, $(-2)\\cdot1=-2$, $1\\cdot(-2)=-2$, $1\\cdot1=1$.',
        'The largest is $4$ and the smallest is $-2$. Therefore $-2<ab<4$.',
        'Choice (3) multiplies end by end. Choice (1) forgets that two negatives give a positive.'])
    P['12'] = ('Given: $a>b>0$. Which of the following cannot be true?',
               ['$\\frac1a>\\frac1b$', '$a^2>b^2$', '$a-b<1$', '$ab<1$'], 1, [
        '$a$ and $b$ are both positive, so the reciprocals flip: $\\frac1a<\\frac1b$. Therefore (1) cannot be true.',
        'The others can be true: $a=0.5$, $b=0.4$ gives $a^2=0.25>0.16=b^2$, $a-b=0.1<1$ and $ab=0.2<1$.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t12-' + k, TOPIC, stem, ch, cor, ex)
        M.place_q('q-r26-t12-' + k, PRACTICE)

    # =====================================================================================
    # 9. Practice order: easy -> hard
    # =====================================================================================
    M.practice_order(PRACTICE, [
        X + '4', X + '1', X + '6', X + '2', 'q-344', 'q-346', 'q-342', X + '3', X + '5', X + '7',
        'q-338', 'q-341', 'q-339', 'q-340', 'q-345', 'q-347', 'q-348', 'q-343', 'q-349', 'q-351',
        'q-r26-t12-07', 'q-r26-t12-05', 'q-r26-t12-06', 'q-r26-t12-08', 'q-r26-t12-12',
        'q-353', 'q-354', 'q-352', 'q-r26-t12-09', 'q-350', 'q-r26-t12-10', 'q-r26-t12-11',
        'q-355', 'q-356', 'q-357'])

    add_summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last


# ------------------------------------------------------------------ Pass 2: summary video before the practice
def add_summary(M):
    sb = ['Same moves', 'x disappears', 'Systems', 'x² inequalities', 'Test the choices',
          'Signs and fractions', 'Combining ranges', 'Must, could, cannot', 'Before you practice']
    C = lambda i, title, script: dict(title=title, mode='concept', active=i, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice, let's review the whole topic in three minutes.",
            "Every rule, every trap. Short and fast."]),
        C(0, 'Same moves', [
            "An inequality is solved like an equation — the same moves, on both sides.",
            A('Flip', T('$\\times$ or $\\div$ by a negative $\\to$ flip the sign', size=46)),
            "One difference: multiply or divide by a negative number, and the sign flips.",
            A('No flip', T('$-4x<20\\ \\Rightarrow\\ -20<4x\\ \\Rightarrow\\ -5<x$', size=50)),
            "My tip: don't divide by a minus at all. Move the terms across, so x stays positive. Then nothing flips."]),
        C(1, 'x disappears', [
            "Sometimes x cancels out.",
            A('True', T('$2-7x<6-7x\\ \\Rightarrow\\ 2<6$: every $x$', size=46)),
            "What's left is true? Every x works.",
            A('False', T('Left with something false: no $x$ works', size=46)),
            "What's left is false? No x works."]),
        C(2, 'Systems', [
            "Two inequalities: solve each one, then take the overlap.",
            A('Overlap', T('$x<12$ and $x>4\\ \\Rightarrow\\ 4<x<12$', size=48)),
            "It's AND, not OR. No overlap — no solution.",
            A('Chain', T('$3y-2<x<y+4\\ \\Rightarrow\\ 3y-2<y+4$', size=48)),
            "A shared side? Chain them, and ignore the middle.",
            "An equation too? Substitute — just like with two equations."]),
        C(3, 'x² inequalities', [
            "x squared on one side, a number on the other.",
            A('Small side', T('$x^2<25\\ \\Rightarrow\\ -5<x<5$', size=50)),
            "x squared on the small side: x is between the roots.",
            A('Big side', T('$x^2\\ge49\\ \\Rightarrow\\ x\\ge7$ or $x\\le-7$', size=50)),
            "On the big side: x is outside the roots. Don't forget the negative root."]),
        C(4, 'Test the choices', [
            "Hard to solve? Plug in the choices.",
            A('Plug in', T('$x^4<200<x^5$: $x=3$: $81<200<243$ ✓', size=48)),
            "First ask: can x be negative? Here no — a negative x to the fifth is negative.",
            "Then plug in. Once one choice works, you can move on."]),
        C(5, 'Signs and fractions', [
            "Numbers between zero and one behave strangely.",
            A('0 < x < 1', T('$0<x<1:\\quad x^2<x<\\sqrt x<1<\\frac1x$', size=46)),
            "Squaring makes them smaller. Above one, the order turns around.",
            A('Reciprocals', T('Reciprocals: same sign $\\to$ flip; different signs $\\to$ no flip', size=40)),
            "One over a number: same sign — flip. Different signs — no flip.",
            A('Sign table', T('Sign table: zeros on the line, test one number in each part', size=40)),
            "A product or a fraction above or below zero? Mark the zeros, and test each part."]),
        C(6, 'Combining ranges', [
            "Two ranges together.",
            A('Add', T('Add: $2<a<4,\\ 1<b<6\\ \\Rightarrow\\ 3<a+b<10$', size=44)),
            "Adding is safe — when both point the same way.",
            A('Subtract', T('$a-b$: biggest $a$ minus smallest $b$: $-4<a-b<3$', size=44)),
            "Never subtract end from end. Biggest minus smallest, smallest minus biggest.",
            A('Corners', T('Multiply: all positive, or check the four corners', size=44)),
            "Multiplying with a negative inside? Check the four corners.",
            "And x squared: if zero is inside the range, x squared starts at zero."]),
        C(7, 'Must, could, cannot', [
            "Three question words, three jobs.",
            A('Must', T('Necessarily true: one counterexample kills it', size=44)),
            A('Could', T('Could be true: one example keeps it', size=44)),
            A('Cannot', T('Cannot be true: it breaks the givens', size=44)),
            "Which numbers to try? Zero, one, negative one, one half — and a big number."]),
        C(8, 'Before you practice', [
            "Before you practice, always ask yourself:",
            A('Check 1', T('1. Am I dividing by a negative? Then flip — or move the terms', size=40)),
            A('Check 2', T('2. Is it AND? Then take the overlap', size=40)),
            A('Check 3', T('3. Can x be negative, zero, or a fraction?', size=40)),
            A('Check 4', T('4. Can I just plug in the choices?', size=40)),
            "And watch the traps: the forgotten flip, the negative root of x squared, and subtracting ranges end from end.",
            "You know all of this. Go practice."]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t12-summary', TOPIC, 'Inequalities: Summary', sb, slides, ADV, after=last)


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
    # q-r26-t12-06 was the lesson example -3 < x < 2 of "r26-t12-combining" slide 5 -> new numbers.
    M.set_q('q-r26-t12-06', stem=r'Given: $-4<x<3$. Which of the following gives all the possible values of $x^2$?',
            choices=[r'$9<x^2<16$', r'$0\le x^2<16$', r'$0\le x^2<9$', r'$-16<x^2<9$'], correct=2,
            expl=[r'$0$ is inside the range, so $x^2$ can be $0$ (at $x=0$). That is the smallest value.',
                  r'The biggest square comes from the end farthest from $0$: when $x$ is close to $-4$, $x^2$ is close to $16$.',
                  r'Therefore $0\le x^2<16$. Choice (1) is the trap: it only squares the ends.'])


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
    # --- Inequalities: "x to the plus side" (5 + x < 13 + 3x) and "Every x works" (4(3 − 2x) − 5 < 9 − 8x) are the
    # Hebrew lesson's own examples, and Questions 1 and 2 (3 + x < 15 + 3x, 3(4 − 3x) − 7 < 8 − 9x) teach them again.
    L = 'inequalities'
    _cr_titles(M, L, ['Four signs', 'Same moves', 'A minus flips it', 'The same with x'])
    _cr_insert(M, L, 5, 'Same answer. And the sign never had to flip.', [
        'Now two questions. Try each one first — then watch.'])
    _cr_replace(M, 'solve-q-322', 1, 'and the tip from the lesson', [
        'One inequality — and a tip that saves you on the exam.'])
    _cr_insert(M, 'solve-q-322', 2, 'The right side has three x', [
        A("'Move x to the side with MORE x' appears", T('Tip: move $x$ to the side with MORE $x$ — it stays positive', 36)),
        "The tip: move x to the side where there are MORE x's. Then x stays positive, and nothing flips."], before=True)
    # moved into Question 2 (taught only on the cut slide): x disappears and the result is FALSE
    _cr_slide_after(M, 'solve-q-323', 2, 'True or false?', [
        A("'x disappears: true → every x · false → no x' appears", T(r'$x$ disappears: true $\to$ every $x$ $\cdot$ false $\to$ no $x$', 40)),
        'And if x disappears and you are left with something FALSE — like nine less than two — then no x works.'])

    # --- Systems of Inequalities: the Hebrew intro is one minute: "solve each one, then find where they overlap".
    # Its six example slides are near-twins of Questions 3-8: overlap (Q3), no overlap (Q4), test the choices
    # x⁴ < 20 < x⁵ (Q5: x⁴ < 90 < x⁵), chain them (Q6), x² inequalities (Q7), plus an equation (Q8).
    S = 'inequality-systems'
    M.remove_slides(S, list(range(2, len(M.video(S)['beats']) + 1)))
    M.set_slide(S, 1, script=[
        'Systems of inequalities.',
        'Now it gets more interesting — more than one inequality at once.',
        'Some of these questions are simple. Some can eat your time. Each question that follows shows one type — and how to crack it.'])
    M.insert_slides(S, 1, [dict(mode='concept', title='Solve each, overlap', active=0, pre=[], script=[
        'Two inequalities — or one double inequality. The same rule.',
        A("'Solve each one → find the overlap' appears", T(r'Solve each one separately $\to$ find where they overlap', 40)),
        'Solve each one separately. Then find where they overlap. That overlap is the answer.',
        'Six questions next. Try each one first — then watch the solution.'])])
    M.set_sidebar(S, ['Solve each, overlap'])
    # Question 7: the rule for both sides (the big side was taught only on the cut slide; new numbers, not q-345's)
    _cr_replace(M, 'solve-q-328', 1, 'Remember the rule.', ['A second-degree inequality — and its rule.'])
    _cr_slide_after(M, 'solve-q-328', 2, 'Small side, big side', [
        A("'x² < a → between the roots' appears", T(r'$x^2<a \;\Rightarrow\; -\sqrt a<x<\sqrt a$', 44)),
        'The rule: x squared on the SMALL side — x is trapped between the roots.',
        A("'x² > a → outside the roots' appears", T(r'$x^2>a \;\Rightarrow\; x>\sqrt a$ or $x<-\sqrt a$', 44)),
        'On the BIG side — x is outside them. x squared bigger than nine: x is bigger than three, or less than negative three.'])

    # --- Signs, Fractions & Must-Be-True: the sign table is taught in Question 10; negatives between −1 and 0 in
    # Question 9 (same numbers); the list of numbers to try is on the board in Question 20.
    G = 'r26-t12-signs'
    _cr_titles(M, G, ['Between 0 and 1', 'Reciprocals', 'Must, could, cannot'])
    M.set_slide(G, 1, script=[
        'Before the advanced questions — three short tools.',
        'Numbers between zero and one, reciprocals, and the words must, could and cannot.',
        'The rest — like the sign table — comes inside the questions.'])
    _cr_drop(M, G, 2, ["Negative numbers? Don't memorize", 'x = −½:  x² = ¼', 'Negative one half squared'])
    _cr_drop(M, G, 4, ['Try: $0$', 'Which numbers to try?', 'Most traps hide in the negatives'])
    _cr_insert(M, G, 4, 'Cannot be true: it contradicts', [
        'Now the questions. Try each one first — then watch.'])

    # --- Combining Inequalities & Ranges: add (Question 17), never subtract (Question 18), multiply - the corners
    # (Question 19). Kept: the range of x² (no question video teaches it).
    C = 'r26-t12-combining'
    _cr_titles(M, C, ['Range of x²'])
    M.set_slide(C, 1, script=[
        'Two inequalities — can we add them? Subtract them? Multiply them?',
        'The exam loves this. One move is safe. The others are traps. The questions show which is which.',
        'First, one trap of its own: the range of x squared.'])
    _cr_insert(M, C, 2, 'So x squared is at least zero and less than nine.', [
        'Now the questions. Try each one first — then watch.'])
    # moved: adding ranges part by part -> Question 17; multiplying end by end only when all positive -> Question 19
    _cr_slide_after(M, 'solve-q-r26-t12-03', 2, 'Ranges add too', [
        A("'1 < a < 3, 2 < b < 5 → 3 < a + b < 8' appears", T(r'$1<a<3,\ \ 2<b<5 \;\to\; 3<a+b<8$', 44)),
        'Ranges add the same way, part by part: one plus two is three, three plus five is eight.'])
    _cr_insert(M, 'solve-q-336', 2, "We'll solve it the psychometric way", [
        A("'All positive? End by end. Negatives? The corners' appears", T(r'All positive? Multiply end by end. Negatives inside? Check the corners', 34)),
        'Multiplying ranges end by end works only when everything is positive. With negatives inside, check the corners — and when dividing, make sure the bottom cannot be zero.'])


_apply_before_cut_repeats = apply


def apply(M):
    _apply_before_cut_repeats(M)
    cut_repeats(M)   # 2026-10-05: runs last


# ---------------------------------------------------------------------------------------------------------------
# 2026-10-06: new exam methods (found by solving real exams). Topic 12 is not recorded.
#   (a) RANGES IN TWO MOVES: endpoint (pretend "=", solve), then direction (test one easy legal number);
#       for "the most precise range": test a number inside one choice and outside another.
#   (b) range of a/b (positive ranges) on the traps card.
# ---------------------------------------------------------------------------------------------------------------
def add_methods(M):
    global ADV_SIDEBAR
    # ---- (a) one named slide in lesson 1, after "The same with x"
    L = L1
    _replace_say(M, L, 5, 'Now two questions. Try each one first', None)
    sb = list(M.video(L)['hybrid']['sidebar']) + ['Ranges in two moves']
    M.set_sidebar(L, sb)
    M.insert_slides(L, 5, [dict(mode='concept', title='Ranges in two moves', active=len(sb) - 1, pre=[], script=[
        "One more tool. It works on almost every \"for which values of x\" question — and you never have to think about flipping.",
        "I call it ranges in two moves.",
        A("'1. Endpoint: pretend = and solve' appears", T('1. Endpoint: pretend it is $=$ and solve', size=44)),
        "Move one: the endpoint. Pretend the inequality sign is an equals sign, and solve.",
        A('5 − 2x = x − 4 → x = 3 appears', T('$5-2x>x-4$: $\\ 5-2x=x-4 \\Rightarrow x=3$', size=46)),
        "Five minus two x, greater than x minus four. As an equation: nine equals three x. x is three.",
        "Why? The two sides swap which one is bigger only where they are equal. So three is the border of the answer.",
        A("'2. Direction: test one easy legal number' appears", T('2. Direction: test one easy legal number, like $0$', size=44)),
        "Move two: the direction. Which side of three? Test one easy number. Zero is the easiest.",
        A('x = 0: 5 > −4 ✓ → x < 3 appears', T('$x=0$: $\\ 5>-4$ ✓ $\\ \\Rightarrow\\ x<3$', size=46)),
        "x equals zero: five is greater than negative four. True. So zero is in the answer — and zero is below three. x is less than three.",
        "No sign flipping at all. The test number tells you the direction.",
        A("'Most precise range? test one number' appears", T('Most precise range? Test a number inside one choice and outside another', size=36)),
        "And when the choices are ranges, and they ask for the most precise one, test a number that some choices contain and others don't.",
        "It works? Then the answer must contain it. Every choice that leaves it out is wrong.",
        "It fails? Then the answer can't contain it. Every choice that contains it is wrong.",
        "Two limits. Test only legal numbers. And if x is in a denominator, the number that makes the bottom zero is a border too — so test a number on each side.",
        "The rule: endpoint first, then one test number for the direction.",
        "Now two questions. Try each one first — then watch."])])

    # ---- guided Question 1 (q-322) shows the two moves: its "Quick check" slide becomes Method 2
    M.set_slide('solve-q-322', 3, title='Method 2 · Two moves', script=[
        "Now the same question in two moves — the way that works on every range question.",
        D('Write "Endpoint: 3 + x = 15 + 3x → −12 = 2x → x = −6"'),
        "Move one, the endpoint. Pretend it's an equals sign: three plus x equals fifteen plus three x. Negative twelve equals two x. x is negative six.",
        "The answer must start at negative six. Choices one, two and four start at twelve, six and three. They're already out.",
        D('Write "Direction: x = 0: 3 < 15 ✓ → −6 < x"'),
        "Move two, the direction. Test zero: three is less than fifteen. True. So zero is in the answer — and zero is above negative six.",
        D('Circle choice 3'),
        "x is greater than negative six. Choice three — and nothing ever had to flip."])

    q = M.q('q-322')
    M.set_q('q-322', expl=list(q['explanation']) + [
        'Two moves: endpoint $3+x=15+3x$ gives $x=-6$; direction: $x=0$ works, and $0$ is above $-6$, so $-6<x$.'])

    # ---- new guided question: the most precise range, by testing numbers
    ADV_SB = ADV_SIDEBAR + ['Question %d' % (int(ADV_SIDEBAR[-1].split()[1]) + 1)]
    for v in M.D['videos'].values():
        if v['topic'] == TOPIC and (v.get('hybrid') or {}).get('sidebar') == ADV_SIDEBAR:
            M.set_sidebar(v['id'], ADV_SB)
    g = 'q-r26-t12-13'
    # review 2026-10-06: no trinomial (teacher: quadratic trinomials are not worth it) -> a two-sided linear range
    M.new_q(g, TOPIC, 'Given: $-7\\le3-2x<5$. Which of the following is the most precise range for $x$?',
            ['$x\\le5$', '$-5\\le x<1$', '$-1<x\\le5$', '$x>-1$'], 3, [
        'Test numbers that some choices contain and others leave out.',
        '$x=-3$: $3-2\\cdot(-3)=9$, and $9<5$ ✗. $-3$ fails, so every choice that contains $-3$ is wrong: choices 1 and 2 are out.',
        '$x=6$: $3-12=-9$, and $-7\\le-9$ ✗. $6$ fails, so choice 4 (it contains $6$) is out. The answer is choice 3.',
        'Two moves: the endpoints solve $3-2x=5$ and $3-2x=-7$, so $x=-1$ and $x=5$. $x=0$ gives $-7\\le3<5$ ✓, so the answer is the part between them: $-1<x\\le5$ ($x=5$ gives $-7\\le-7$ ✓, $x=-1$ gives $5<5$ ✗).',
        'Choice 2 is the trap: the right endpoints with the wrong signs ($-2x<2$ gives $x>-1$, not $x<1$).'])
    M.place_q(g, ADV, after='solve-q-r26-t12-02')
    _old, ADV_SIDEBAR = ADV_SIDEBAR, ADV_SB
    _solution(M, g, ["Question twenty-one.", "Choices that are ranges, and they want the most precise one. Test numbers."], [
        ('Method 1 · Test a number', [
            "The cue: four ranges in the choices, and the words \"most precise range\".",
            "The rule: a number that works must be inside the answer. A number that fails must be outside it.",
            "So pick numbers where the choices disagree. Negative three: choices one and two contain it, choices three and four don't.",
            D('Write "x = −3: 3 + 6 = 9 < 5 ✗"'),
            "Three minus two times negative three: three plus six, nine. Less than five? No. Negative three fails.",
            D('Cross out choices 1 and 2'),
            "So the answer can't contain negative three. Choices one and two contain it. Both out.",
            "Choices three and four disagree about six: choice four contains it, choice three doesn't.",
            D('Write "x = 6: 3 − 12 = −9 ≥ −7 ✗"'),
            "Three minus twelve: negative nine. Is it at least negative seven? No. It fails.",
            D('Cross out choice 4 and circle choice 3'),
            "Choice four contains six — out. Choice three. We never solved anything."]),
        ('Method 2 · Two moves', [
            "The two-move way gives the same answer.",
            D('Write "3 − 2x = 5 → x = −1;  3 − 2x = −7 → x = 5"'),
            "Endpoints: pretend each side is equals. Three minus two x is five: x is negative one. Three minus two x is negative seven: x is five.",
            D('Write "x = 0: −7 ≤ 3 < 5 ✓ → −1 < x ≤ 5"'),
            "Direction: test zero. Negative seven, three, five — it works. Zero is between the endpoints, so the answer is the part between them.",
            "Five is allowed — three minus ten is exactly negative seven. Negative one isn't — five is not less than five.",
            "Negative one less than x, x at most five. Choice three.",
            "Choice two is the trap: the endpoints with the wrong signs. Minus two x less than two means x is greater than negative one."]),
    ])
    ADV_SIDEBAR = _old

    # ---- cards
    rows = M.card('mem-inequalities')['tables'][1]['rows']
    rows.insert(0, ['"For which values of $x$?" (ranges in two moves)',
                    'Endpoint: pretend it is $=$ and solve. Direction: test one easy legal number (like $0$). '
                    'Example: $5-2x>x-4$: endpoint $3$; $x=0$ works, so $x<3$'])
    rows.insert(1, ['"The most precise range" (choices are ranges)',
                    'Test a number inside one choice and outside another. Works: every choice that leaves it out is wrong. '
                    'Fails: every choice that contains it is wrong'])
    rows = M.card('mem-r26-t12-traps')['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0] == 'Range of $ab$')
    rows.insert(k + 1, ['Range of $\\frac{a}{b}$ (all positive)',
                        'smallest $=$ smallest top $\\div$ largest bottom; largest $=$ largest top $\\div$ smallest bottom',
                        '$2<a<6$, $1<b<3 \\Rightarrow \\frac23<\\frac ab<6$'])


_apply_before_add_methods = apply


def apply(M):
    _apply_before_add_methods(M)
    add_methods(M)   # 2026-10-06: runs last


# =====================================================================================
# 2026-10-06 practice: the new exam methods as an extra method in PRACTICE explanations
# (append only; the existing worked solution stays as it is). Runs last.
# =====================================================================================
PRACTICE_METHODS = {
    'alg-extra-unit-t12-3-1': [
        'Method 2 · Two moves: endpoint $-3x=9$ gives $x=-3$. Direction: $x=0$ gives $0>9$, which is false. So the answer is the side without $0$: $x<-3$. Nothing had to flip.',
    ],
    'q-346': [
        'Method 2 · Two moves: endpoint $a+4=\\frac a2$ gives $a=-8$. Direction: $a=0$ gives $4<0$, which is false. $0$ is above $-8$, so the answer is below it: $a<-8$.',
    ],
    'q-355': [
        'Method 2 · The most precise range: test numbers where the choices disagree. $x=2$: $\\frac23$ is between $\\frac14$ and $\\frac34$ ✓. A number that works kills every choice that leaves it out: choices 1 and 3.',
        '$x=\\frac12$: $\\frac{1/2}{3/2}=\\frac13$ ✓. Choice 4 leaves $\\frac12$ out, so it is out too. The answer is choice 2.',
    ],
    'q-354': [
        'Method 2 · The most precise range: $n=1$ gives $\\frac42=2>0$ ✓, so choices 2 and 4 (which leave $1$ out) are out. $n=-1$ gives $\\frac24>0$ ✓, so choice 1 is out. The answer is choice 3.',
    ],
    'q-353': [
        'Method 2 · The most precise range: test $x=-4$. $16-6=10$, and $3<10<19$ ✓. A number that works kills every choice that leaves it out: choices 1, 2 and 3. The answer is choice 4.',
    ],
    'q-r26-t12-06': [
        'Method 2 · The most precise range: test values. $x=0$ gives $x^2=0$, so choice 1 (which leaves $0$ out) is out. $x=-3.5$ gives $x^2=12.25$, so choices 3 and 4 (both stop at $9$) are out. The answer is choice 2.',
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
# (guided q-322 ... q-337, practice q-338 ... q-357) gets new numbers / letters - same idea, same trap, same methods -
# and every guided solution video is rewritten to match. The Hebrew lesson examples get new numbers too.
# Practice clean-up: extra warm-ups down to 3, September items kept only where the Hebrew practice lacks the type.
# Nothing in topic 12 is recorded (checked ~/Documents/Course.recordings on 2026-10-06). Runs last.
# =====================================================================================================================
def renumber(M):
    from math_api import rich_plain
    RECORDED = set()

    def S(qid, **kw):
        if qid in RECORDED: return
        q = M.set_q(qid, **kw)
        for v in M.D['videos'].values():   # keep any pre-loaded copy of the choices in sync
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'choices' in it:
                        it['choices'] = list(q['choicesRich']); M.touched_videos.add(v['id'])

    def video(qid, slides):
        if qid in RECORDED: return
        vid = 'solve-' + qid
        for n, x in slides.items():
            title, script = x if isinstance(x, tuple) else (None, x)
            M.set_slide(vid, n, title=title, script=script)
        v = M.video(vid); v['title'] = v['navLabel'] = rich_plain(M.q(qid)['stemRich']).replace('\n', ' ')
        M.touched_videos.add(vid)

    def item(vid, n, k):
        return dict(M.slide(vid, n)['items'][k])

    # ---------------- lesson "Inequalities": the Hebrew lesson's own examples -> new numbers, same points
    if 'inequalities' not in RECORDED:
        L = 'inequalities'
        _dd_sub(M, L, 2, [('$x\\le5$', '$x\\le4$'), ('x ≤ 5 appears', 'x ≤ 4 appears'),
                          ('x less than or equal to five: x can be five itself', 'x less than or equal to four: x can be four itself'),
                          ('Next to x ≤ 5 write "5, 4.5, 3, −7 ✓"', 'Next to x ≤ 4 write "4, 3.5, 1, −6 ✓"'),
                          ('Five. Four and a half. Three. Negative seven. All fine.', 'Four. Three and a half. One. Negative six. All fine.'),
                          ('Put dots on −8 and −3, and write "−8 < −3" above them', 'Put dots on −7 and −2, and write "−7 < −2" above them'),
                          ("Negative eight is less than negative three — it's farther left.", "Negative seven is less than negative two — it's farther left.")])
        _dd_sub(M, L, 3, [('$x+5<14$', '$x+6<11$'), ('Write "−5" under both sides', 'Write "−6" under both sides'),
                          ('Take five from both sides.', 'Take six from both sides.'), ('Write "x < 9"', 'Write "x < 5"'),
                          ("x is less than nine. The sign didn't move.", "x is less than five. The sign didn't move.")])
        _dd_sub(M, L, 4, [('$-12<-4$', '$-10<-2$'),
                          ("Negative twelve is less than negative four. True — it's farther left.",
                           "Negative ten is less than negative two. True — it's farther left."),
                          ('Write "÷(−4)" under both sides, then "3 > 1"', 'Write "÷(−2)" under both sides, then "5 > 1"'),
                          ("Divide both sides by negative four: three and one.", "Divide both sides by negative two: five and one."),
                          ('Move each number to the other side: write "4 < 12"', 'Move each number to the other side: write "2 < 10"'),
                          ('Negative four goes left and becomes four. Negative twelve goes right and becomes twelve.',
                           'Negative two goes left and becomes two. Negative ten goes right and becomes ten.'),
                          ('−12 < −4 appears again below', '−10 < −2 appears again below'),
                          ('Write "÷4" and then "1 < 3"', 'Write "÷2" and then "1 < 5"'),
                          ('Divide by four: one is less than three. Same answer — three greater than one',
                           'Divide by two: one is less than five. Same answer — five greater than one')])
        for it in M.slide(L, 4)['items']: assert '-12' not in it.get('t', '')
        for n in (3, 4): M.slide(L, n)['loads'] = ''   # the canvas description is rebuilt from the new items
    # cards: examples that were the Hebrew questions' numbers
    rows = M.card('mem-inequalities')['tables'][1]['rows']
    k = next(i for i, r in enumerate(rows) if r[0] == '$x^2>a$')
    rows[k] = ['$x^2>a$', '$x>\\sqrt a$ or $x<-\\sqrt a$ (outside the roots). Example: $x^2\\ge81 \\Rightarrow x\\ge9$ or $x\\le-9$']
    rows = M.card('mem-r26-t12-traps')['tables'][1]['rows']
    k = next(i for i, r in enumerate(rows) if r[0].startswith('Product or fraction'))
    rows[k][2] = '$x(2-x)>0 \\Rightarrow 0<x<2$'

    # ============================== guided questions (Questions 1-8, then the advanced set)
    # q-322: 3 + x < 15 + 3x -> -6 < x (key 3)
    S('q-322', stem='Given: $4+x<18+3x$. For which values of $x$ does the inequality hold?',
      choices=['$7<x$', '$-7<x$', '$14<x$', '$4<x$'], correct=2, expl=[
        'Move the $x$ terms to the side with more $x$ (the right): $4-18<3x-x$, so $-14<2x$.',
        'Divide by $2$ (positive, so no flip): $-7<x$.',
        'Check: $x=0$ gives $4<18$ ✓, and only choice (2) includes $0$.',
        'Two moves: endpoint $4+x=18+3x$ gives $x=-7$; direction: $x=0$ works, and $0$ is above $-7$, so $-7<x$.'])
    tip = item('solve-q-322', 2, 1)
    video('q-322', {
        2: ["Same moves as an equation. But I want x to stay positive.",
            A("'Move x to the side with MORE x' appears", tip),
            "The tip: move x to the side where there are MORE x's. Then x stays positive, and nothing flips.",
            "The right side has three x, the left has one x. So the x's go RIGHT.",
            D('Write "4 − 18 < 3x − x"'),
            "x moves right, eighteen moves left.",
            D('Write "−14 < 2x"'),
            "Negative fourteen is less than two x.",
            D('Write "÷ 2" and then "−7 < x"'),
            "Divide by two — positive, nothing flips. x is greater than negative seven.",
            D('Circle choice 2'),
            "Choice two.",
            "The other way, you'd get negative two x, divide by a minus and flip. Same answer — just more chances to slip."],
        3: ["Now the same question in two moves — the way that works on every range question.",
            D('Write "Endpoint: 4 + x = 18 + 3x → −14 = 2x → x = −7"'),
            "Move one, the endpoint. Pretend it's an equals sign: four plus x equals eighteen plus three x. Negative fourteen equals two x. x is negative seven.",
            "The answer must start at negative seven. Choices one, three and four start at seven, fourteen and four. They're already out.",
            D('Write "Direction: x = 0: 4 < 18 ✓ → −7 < x"'),
            "Move two, the direction. Test zero: four is less than eighteen. True. So zero is in the answer — and zero is above negative seven.",
            D('Circle choice 2'),
            "x is greater than negative seven. Choice two — and nothing ever had to flip."]})

    # q-323: 3(4 - 3x) - 7 < 8 - 9x -> 5 < 8, any value (key 4)
    S('q-323', stem='Given: $5(2-3x)-4<7-15x$. For which values of $x$ does the inequality hold?',
      choices=['$0$', '$6$', 'Any value', '$1$'], correct=3, expl=[
        'Open the brackets: $10-15x-4<7-15x$, so $6-15x<7-15x$.',
        'Add $15x$ to both sides: $6<7$. The $x$ is gone, and $6<7$ is always true.',
        'Therefore the inequality holds for every value of $x$.'])
    video('q-323', {
        2: ["First, open the brackets.",
            D('Write "10 − 15x − 4 < 7 − 15x"'),
            "Five times two is ten. Five times negative three x is negative fifteen x. Then minus four.",
            D('Cross out −15x on both sides, then write "6 < 7"'),
            "Minus fifteen x on both sides — they cancel. Ten minus four is six. Six less than seven.",
            "Is six less than seven? Always. x is gone — it doesn't matter.",
            D('Circle choice 3'),
            "So any value works. Choice three."]})

    # q-324: 2x - 5 < x + 3 < 3x - 9 -> 6 < x < 8 (key 4)
    S('q-324', stem='Given: $3x-4<2x+5<4x-5$. Which of the following is the most precise range for $x$?',
      choices=['$3<x<5$', '$5<x<9$', '$6<x$', '$x<10$'], correct=2, expl=[
        'Split the chain into two inequalities.',
        'Left part: $3x-4<2x+5$, so $x<9$.',
        'Right part: $2x+5<4x-5$. Move the $x$ terms right: $10<2x$, so $5<x$.',
        'Both must hold: $5<x<9$.'])
    video('q-324', {
        2: ["One thing we know right away: the right expression is bigger than the left one — it's bigger than the middle, which is bigger than the left.",
            "Now split it and solve each part separately.",
            D('Under the left half write "3x − 4 < 2x + 5 → x < 9"'),
            "Left part: three x minus four less than two x plus five. x's left, numbers right: x less than nine.",
            D('Under the right half write "10 < 2x → 5 < x"'),
            "Right part: two x plus five less than four x minus five. The x's go to the side with MORE x — the right. Ten less than two x. x greater than five.",
            D('Write "5 < x < 9"'),
            "x is greater than five and less than nine. The overlap: between five and nine.",
            D('Circle choice 2'),
            "Choice two."]})

    # q-325: 3x + 30 < 12 + 6x < 30 -> no x (key 3)
    S('q-325', stem='Given: $2x+28<8+6x<20$. For which values of $x$ does the inequality hold?',
      choices=['$5<x$', 'For no value of $x$', '$x<2$', '$0<x$'], correct=2, expl=[
        'Left part: $2x+28<8+6x$, so $20<4x$ and $x>5$.',
        'Right part: $8+6x<20$, so $6x<12$ and $x<2$.',
        'No number is both greater than $5$ and less than $2$. Therefore no value of $x$ satisfies the inequality.'])
    video('q-325', {
        2: ["Split it in two.",
            D('Under the left part write "20 < 4x → 5 < x"'),
            "First part: two x plus twenty-eight less than eight plus six x. x's to the right: twenty less than four x. x greater than five.",
            D('Under the right part write "6x < 12 → x < 2"'),
            "Second part: eight plus six x less than twenty. Six x less than twelve. x less than two.",
            "Now: x greater than five — AND less than two.",
            "It's not OR. It has to be both at the same time. There's no such number.",
            D('Circle choice 2'),
            "No overlap — no solution. The empty set. Choice two."]})

    # q-326: x^4 < 90 < x^5 -> 3 (key 2)
    S('q-326', stem='$x$ is an integer, and $x^4<300<x^5$. What is $x$?',
      choices=['$-4$', '$3$', '$4$', '$-3$'], correct=3, expl=[
        'If $x<0$, then $x^5<0$, and a negative number cannot be greater than $300$. Choices (1) and (4) are out.',
        '$x=4$: $4^4=256<300$ ✓ and $4^5=1{,}024>300$ ✓.',
        '$x=3$: $3^5=243$, and $243>300$ is false ✗.',
        'Therefore $x=4$.'])
    video('q-326', {
        2: ["First: can x be negative?",
            "A negative number to an odd power is negative. x to the fifth would be negative — and it can't be bigger than three hundred.",
            D('Cross out choices 1 and 4'),
            "So negative four and negative three are out.",
            "Two left: three and four. Plug in.",
            D('Next to choice 3 write "256 < 300 < 1,024 ✓"'),
            "Four to the fourth is two hundred fifty-six — less than three hundred. Four to the fifth is one thousand twenty-four — more. It works.",
            D('Circle choice 3'),
            "Only one answer is right — so you can mark it and move on. Choice three.",
            D('Next to choice 2 write "81 < 300 < 243 ✗"'),
            "Just for the exercise: three to the fifth is two hundred forty-three — not more than three hundred. No good.",
            "Another way: x to the fourth is less than x to the fifth. Divide by x to the fourth — it's positive — and x is bigger than one. That kills the negatives in one step."]})

    # q-327: x < y + 2, 2y - 2 < x -> y < 4 (key 3)
    S('q-327', stem=given(['a<b+5', '3b-1<a'], 'Which of the following is necessarily true?'),
      choices=['$b<a$', '$b<3$', '$3<b$', '$a<b$'], correct=2, expl=[
        'Chain the two inequalities through $a$: $3b-1<a<b+5$.',
        'Ignore the middle: $3b-1<b+5$, so $2b<6$ and $b<3$.',
        '$a<b$ and $b<a$ are both possible. With $b=0$ the givens say $-1<a<5$: $a=-0.5$ gives $a<b$, and $a=4$ gives $b<a$.'])
    video('q-327', {
        1: ["Question six.", "Two inequalities that share an a. Chain them."],
        2: ["a is less than something, and something is less than a. They share a.",
            D('Write "3b − 1 < a < b + 5"'),
            "Chain them: three b minus one, less than a, less than b plus five.",
            "Now ignore the middle.",
            D('Cross out the a, then write "3b − 1 < b + 5"'),
            "a is gone. One unknown.",
            D('Write "2b < 6 → b < 3"'),
            "b's to the left, numbers to the right: two b less than six. b less than three.",
            D('Circle choice 2'),
            "Choice two. And a less than b, or b less than a? Nothing forces either one."]})

    # q-328: (5x^2 - 2)/3 < (2x^2 + 20)/2 -> -4 < x < 4 (key 4)
    S('q-328', stem='Given: $\\frac{4x^2-9}{5}<\\frac{x^2+18}{2}$. Which of the following is correct?',
      choices=['$-6<x<6$', '$6<x$', '$36<x$', '$x<-36$'], correct=1, expl=[
        'Multiply both sides by $10$ (positive, so no flip): $2(4x^2-9)<5(x^2+18)$.',
        'Open the brackets: $8x^2-18<5x^2+90$, so $3x^2<108$ and $x^2<36$.',
        '$x^2$ is on the small side, so $x$ is between the roots: $-6<x<6$.'])
    video('q-328', {
        2: ('Multiply by 10, then the rule', [
            "Fractions first. Multiply both sides by ten — positive, so no flip.",
            D('Write "2(4x² − 9) < 5(x² + 18)"'),
            "Ten over five is two, ten over two is five. Two times the left top, five times the right top.",
            D('Write "8x² − 18 < 5x² + 90"'),
            "Open the brackets: eight x squared minus eighteen, less than five x squared plus ninety.",
            D('Write "3x² < 108 → x² < 36"'),
            "x's left, numbers right: three x squared less than a hundred and eight. x squared less than thirty-six.",
            "x squared is on the SMALL side — so x is trapped between the roots.",
            D('Write "−6 < x < 6"'),
            "Root of thirty-six is six. x is between negative six and six.",
            D('Circle choice 1'),
            "Choice one. Don't write just x less than six — negative seven squared is forty-nine. Too big. It's symmetric."])})

    # q-329: a + b = c, a < c < b -> ab < 0 (key 1)
    S('q-329', stem=given(['p+q=r', 'q<r<p'], 'Which of the following is necessarily true?'),
      choices=['$0<r$', '$pq<0$', '$r<0$', '$pq=0$'], correct=2, expl=[
        'Substitute $r=p+q$: $q<p+q<p$.',
        'Left part: $q<p+q$, so $0<p$. Right part: $p+q<p$, so $q<0$.',
        '$p$ is positive and $q$ is negative, so $pq<0$.',
        'The sign of $r$ is not fixed: $p=3$, $q=-1$ gives $r=2$, and $p=1$, $q=-3$ gives $r=-2$.'])
    video('q-329', {
        2: ["We're given that r is p plus q. So put p plus q where r is.",
            D('Write "q < p + q < p"'),
            "Now it's a double inequality. Split it.",
            D('Write "q < p + q → p > 0"'),
            "First part: q less than p plus q. Cancel the q — p is greater than zero.",
            D('Write "p + q < p → q < 0"'),
            "Second part: p plus q less than p. Cancel the p — q is less than zero.",
            D('Write "p positive, q negative → pq < 0"'),
            "p positive, q negative — their product is negative.",
            D('Circle choice 2'),
            "Choice two. And r? We know nothing about its sign. And the product can't be zero — neither of them is zero."]})

    # q-330: 40/80 < x/(x+1) < 70/80 -> 5 values (key 2)
    S('q-330', stem='$x$ is a positive integer, and $\\frac{60}{90}<\\frac{x}{x+1}<\\frac{81}{90}$. How many values can $x$ have?',
      choices=['$5$', '$7$', '$6$', '$0$'], correct=3, expl=[
        'Simplify: $\\frac{60}{90}=\\frac23$ and $\\frac{81}{90}=\\frac{9}{10}$.',
        '$x$ is positive, so $x+1$ is positive. We can multiply by it without flipping.',
        'Left part: $\\frac23<\\frac{x}{x+1}$ gives $2(x+1)<3x$, so $2<x$.',
        'Right part: $\\frac{x}{x+1}<\\frac{9}{10}$ gives $10x<9x+9$, so $x<9$.',
        'Therefore $2<x<9$: $x=3, 4, 5, 6, 7, 8$. That is six values.'])
    video('q-330', {
        2: ["x is a positive integer. How many values fit between these two fractions?",
            "First — simplify. Sixty ninetieths reduces by thirty: two thirds.",
            D('Under 60/90 write "= 2/3"'),
            "Eighty-one ninetieths reduces by nine: nine tenths.",
            D('Under 81/90 write "= 9/10"'),
            "A double inequality is really two inequalities. Split it into a left part and a right part.",
            D('Write "2/3 < x/(x+1)" and "x/(x+1) < 9/10" on two lines'),
            "Now we want to multiply by x plus one — an unknown. Careful!",
            "Multiply by a negative and the sign flips. So ask: is x plus one positive?",
            "x is a positive integer — so x plus one is positive too. No flip.",
            D('Multiply both sides by 3(x + 1): write "2x + 2 < 3x → 2 < x"'),
            "Multiply both sides by three times x plus one — a positive number. Two x plus two is less than three x. So x is bigger than two.",
            D('Multiply both sides by 10(x + 1): write "10x < 9x + 9 → x < 9"'),
            "Second one: ten x is less than nine x plus nine. So x is less than nine.",
            D('Write "2 < x < 9 → 3, 4, 5, 6, 7, 8"'),
            "Bigger than two, smaller than nine, positive integers: three, four, five, six, seven, eight.",
            D('Circle choice 3'),
            "Six values. Choice three."],
        3: ["Now the psychometric flash of insight.",
            "After simplifying, look closely: in x over x plus one, the bottom is one more than the top. Consecutive numbers.",
            "And x over x plus one grows as x grows: one half, two thirds, three quarters — each one closer to one.",
            "Two thirds and nine tenths are built exactly the same way: two over three, nine over ten.",
            "So just try values. x equals two gives two thirds — equal, not bigger. Out.",
            D('Next to the question write "3/4, 4/5, 5/6, 6/7, 7/8, 8/9"'),
            "Three: three quarters. Four: four fifths. Then five sixths, six sevenths, seven eighths, eight ninths — all fit.",
            "Nine gives nine tenths — equal again, not smaller. Out.",
            D('Circle choice 3'),
            "Six values — choice three.",
            "The shortcut is faster. But the technique from method one — check the sign before you multiply by an unknown — you'll need again and again."]})

    # q-331: (ab)^2 < ab^2 -> 0 < a < 1 (key 3)
    S('q-331', stem='Given: $(xy)^2<x^2y$. Which of the following is the most precise range for $y$?',
      choices=['$0<x<1$', '$-1<y<1$', '$-1<x<1$', '$0<y<1$'], correct=4, expl=[
        '$(xy)^2=x^2y^2$, so $x^2y^2<x^2y$.',
        'If $x=0$, both sides are $0$, and $0<0$ is false. Therefore $x\\ne0$ and $x^2>0$.',
        'Divide both sides by $x^2$ (positive, so no flip): $y^2<y$.',
        '$y^2\\ge0$ and $y>y^2$, so $y>0$. Divide by $y$ (positive): $y<1$.',
        'Therefore $0<y<1$.'])
    video('q-331', {
        2: ["Step one: simplify the left side. x y, squared, is x squared times y squared.",
            D('Under the question write "x²y² < x²y"'),
            "Step two: we'd like to cancel x squared from both sides. But that's dividing by an unknown.",
            "Is x squared positive, zero, or negative? It can't be negative — it's a square.",
            "Could it be zero? Then both sides would be zero — equal. But the question says less than. So x squared is positive.",
            D('Cross out x² on both sides; write "y² < y"'),
            "Cancel it — no flip. y squared is less than y.",
            "Now we'd like to cancel y. So: what's the sign of y?",
            "y squared is zero or positive. And y is bigger than it. So y must be positive.",
            D('Write "y > 0"'),
            "Positive — so we cancel without flipping.",
            D('Write "y < 1"'),
            "y is less than one.",
            D('Write "0 < y < 1" and circle choice 4'),
            "Positive and less than one: between zero and one. Choice four.",
            "And x? Anything but zero — that's why the x choices are traps."]})

    # q-332: (x - 3)/(9 - x) < 0 -> not satisfied on 3 < x < 9 (key 2)
    S('q-332', stem='Given: $\\frac{x+1}{7-x}<0$, and $x\\ne7$. Which of the following ranges does not satisfy the inequality?',
      choices=['$-5<x<-1$', '$7<x<10$', '$-1<x<7$', '$10<x<14$'], correct=3, expl=[
        'Try one number from each range.',
        'Choice (1), $x=-2$: $\\frac{-1}{9}<0$ ✓.',
        'Choice (2), $x=8$: $\\frac{9}{-1}=-9<0$ ✓.',
        'Choice (3), $x=0$: $\\frac{1}{7}$, which is not negative ✗.',
        'Choice (4), $x=12$: $\\frac{13}{-5}<0$ ✓.',
        'With a sign table: the top is $0$ at $x=-1$ and the bottom is $0$ at $x=7$. The fraction is negative for $x<-1$ or $x>7$. Therefore the range $-1<x<7$ does not satisfy it.'])
    video('q-332', {
        2: ["We'd love to get rid of the denominator — but we don't know if it's positive or negative.",
            "And unlike the last questions, nothing here tells us the sign of x.",
            "So think: when is a fraction negative? Two situations.",
            D('Under the question write "top + / bottom −" and "top − / bottom +"'),
            "Top positive and bottom negative — or exactly the reverse.",
            "Case one: top positive, bottom negative.",
            D('Write "x + 1 > 0 → x > −1" and "7 − x < 0 → x > 7"'),
            "x plus one positive: x bigger than negative one. Seven minus x negative: x bigger than seven.",
            D('Write "→ x > 7"'),
            "Both together: x bigger than seven.",
            D('Cross out choices 2 and 4'),
            "Every number above seven satisfies it. Choices two and four — out.",
            "Case two: top negative, bottom positive.",
            D('Write "x < −1" and "x < 7 → x < −1"'),
            "x less than negative one, and x less than seven. Together: x less than negative one.",
            D('Cross out choice 1'),
            "Choice one lies below negative one — it satisfies. Out.",
            D('Circle choice 3'),
            "What's left: between negative one and seven. Choice three.",
            "That works. But it's long and exhausting.",
            "A shorter way to write it: the sign table. Mark negative one and seven on the line, and test one number in each part."],
        3: ["The psychometric way: trial and error. Plug in a number from each range.",
            "Choice one: pick a comfortable number between negative five and negative one. Negative two.",
            D('Next to choice 1 write "x = −2: −1/9 < 0 ✓"'),
            "Negative two plus one, over seven minus negative two: negative one ninth. Negative — it satisfies. Out.",
            D('Cross out choice 1'),
            "Choice two: eight is comfortable.",
            D('Next to choice 2 write "x = 8: 9/(−1) = −9 ✓"'),
            "Eight plus one, over seven minus eight: nine over negative one. Negative nine — it satisfies. Out.",
            D('Cross out choice 2'),
            "Choice three: zero is comfortable.",
            D('Next to choice 3 write "x = 0: 1/7"'),
            "Zero plus one, over seven minus zero: one seventh. Not negative!",
            D('Circle choice 3'),
            "That range does NOT satisfy it. Choice three — no need to check the rest.",
            "On the exam, this is the route I recommend."]})

    # q-333: (x + y)^2 = 100, x - 3 > 0 -> 0 < y < 7 (key 1)
    S('q-333', stem=given(['(x+y)^2=144', 'x-4>0'], 'Which of the following is necessarily true?',
                          pre='$x$ and $y$ are positive integers.\n'),
      choices=['$4<x<8$', '$0<y<8$', '$8<y<12$', '$8<x<12$'], correct=2, expl=[
        '$x$ and $y$ are positive, so $x+y>0$. From $(x+y)^2=144$: $x+y=12$.',
        'From $x-4>0$: $x>4$.',
        'Substitute $x=12-y$: $12-y>4$, so $y<8$. Also $y>0$.',
        'Therefore $0<y<8$.',
        'Choices (1) and (4) are not necessary: $x=11$, $y=1$ breaks (1), and $x=5$, $y=7$ breaks (4).'])
    video('q-333', {
        2: ["x and y are positive integers. We get an equation and an inequality.",
            "Simplify the equation first. Take the square root.",
            D('Write "x + y = ±12"'),
            "x plus y is plus or minus twelve. But both are positive — together they can't be negative twelve.",
            D('Cross out the minus, leaving "x + y = 12"'),
            "So x plus y is twelve.",
            D('Write "x > 4"'),
            "Now simplify the inequality: move the four across. x is bigger than four.",
            "Combine them. The inequality has x — so isolate x from the equation and plug it in.",
            D('Write "x = 12 − y → 4 < 12 − y → y < 8"'),
            "x is twelve minus y. So four is less than twelve minus y. Move things across: y is less than eight.",
            "And y is positive.",
            D('Write "0 < y < 8" and circle choice 2'),
            "Between zero and eight. Choice two."],
        3: ["Same idea — in your head.",
            "Simplify the inequality first: x is bigger than four.",
            "Both numbers are positive and add up to twelve — so y completes x to twelve.",
            D('Write "x = 5 → y = 7, x = 6 → y = 6"'),
            "x is five? y is seven. x is six? y is six. The bigger x gets, the smaller y gets.",
            "x is more than four — so y is less than eight. And it's positive.",
            D('Circle choice 2'),
            "Choice two. If you can think it this way, do — it saves the writing."]})

    # q-334: c + b < a, a < c < b -> not necessarily: 0 < c + b (key 4)
    S('q-334', stem=given(['z+y<x', 'x<z<y'], 'Which of the following is not necessarily true?'),
      choices=['$y<0$', '$0<z+y$', '$x<0$', '$z<0$'], correct=2, expl=[
        'Chain: $z+y<x<z<y$.',
        'From $z+y<z$: $y<0$. From $z+y<y$: $z<0$. From $x<z$: $x<0$.',
        'So (1), (3) and (4) are all true.',
        '$z+y$ is a sum of two negative numbers, so it is negative. Therefore $0<z+y$ is never true — it is the answer.'])
    video('q-334', {
        2: ["They ask which statement is NOT necessarily true.",
            "One side: z plus y is less than x. The other: x is less than z, less than y.",
            "x sits in both — so chain them.",
            D('Under the question write "z + y < x < z < y"'),
            "One long chain: z plus y, less than x, less than z, less than y.",
            D('Draw a number line and mark, from left to right: z + y, x, z, y'),
            "Put it on a number line: z plus y, then x, then z, then y. Left to right.",
            "How do you work a chain with lots of letters? Find two spots with the same letter.",
            D('Draw an arc linking "z + y" and "z"'),
            "z plus y is less than z. The z's cancel…",
            D('Write "y < 0"'),
            "…so y is negative.",
            "The other pair works too: z plus y is less than y — cancel the y's, and z is negative.",
            "And x is less than z — so x is negative as well.",
            D('Write "z < 0, x < 0"'),
            "z plus y: negative plus negative — negative.",
            D('Cross out choices 1, 3 and 4'),
            "Now the choices. y negative? True — out. x negative? True — out. z negative? True — out.",
            D('Circle choice 2'),
            "z plus y positive? No — it's negative. That's the one. Choice two."]})

    # q-335: 2 <= x^2 - 2 <= 34 -> 10 integers (key 2)
    S('q-335', stem='$x$ is an integer, and $5\\le x^2-4\\le60$. How many values can $x$ have?',
      choices=['$6$', '$10$', '$12$', '$17$'], correct=3, expl=[
        'Add $4$ to all three parts: $9\\le x^2\\le64$.',
        'For positive $x$: $3\\le x\\le8$. The negatives are a mirror image: $-8\\le x\\le-3$.',
        'The integers: $\\pm3, \\pm4, \\pm5, \\pm6, \\pm7, \\pm8$. That is $12$ values.'])
    nl = dict(item('solve-q-335', 2, 1), min=-9, max=9)
    video('q-335', {
        2: ["x is an integer. How many values satisfy the double inequality?",
            "We could split it into a left part and a right part. But here there's a much simpler way.",
            "The unknown sits only in the middle. So we can isolate it in one move.",
            D('Write "+4" under all three parts, then "9 ≤ x² ≤ 64"'),
            "Add four to every part: nine, x squared, sixty-four.",
            "Now it's a second-degree inequality. Take the root — but first assume x is positive.",
            D('Write "3 ≤ x ≤ 8"'),
            "Root of nine: three. Root of sixty-four: eight. x between three and eight — both included.",
            A('A number line from −9 to 9 appears', nl),
            D('On the number line, mark 3 to 8, then mirror it: −8 to −3'),
            "If it's true for the positives, it's true for the negatives — like a mirror. Negative eight to negative three.",
            "But they asked how many VALUES — and x is an integer.",
            D('Write "±3, ±4, ±5, ±6, ±7, ±8"'),
            "Three, four, five, six, seven, eight — six values. Mirror them — six more.",
            D('Circle choice 3'),
            "Twelve values. Choice three."]})

    # q-336: -4 < x < 10, -30 < y < 6 -> -300 < xy < 120 (key 2)
    S('q-336', stem=given(['-5<x<8', '-20<y<4'], 'What is the range of the product $xy$?'),
      choices=['$-160<xy<32$', '$-100<xy<100$', '$-100<xy<32$', '$-160<xy<100$'], correct=4, expl=[
        'Negative numbers are involved, so check all four corners: $(-5)(-20)=100$, $(-5)\\cdot4=-20$, $8\\cdot(-20)=-160$, $8\\cdot4=32$.',
        'The largest is $100$ and the smallest is $-160$.',
        'Therefore $-160<xy<100$.'])
    corners = item('solve-q-336', 2, 1)
    video('q-336', {
        2: ["We'll solve it the psychometric way: plug in the edge numbers.",
            A("'All positive? End by end. Negatives? The corners' appears", corners),
            "Multiplying ranges end by end works only when everything is positive. With negatives inside, check the corners — and when dividing, make sure the bottom cannot be zero.",
            "x can't actually be eight — but treat it as eight, and remember the real value is just under.",
            "When is the product biggest? When it's positive. Two ways: both positive, or both negative.",
            D('Write "8 · 4 = 32" and "(−5)(−20) = 100"'),
            "Both positive: eight times four, thirty-two. Both negative: negative five times negative twenty — a hundred.",
            "So the maximum is a hundred.",
            D('Cross out choices 1 and 3'),
            "Choices one and three stop at thirty-two. Out.",
            "Now the minimum. A negative product: one positive, one negative.",
            D('Write "8 · (−20) = −160"'),
            "x positive, y negative: eight times negative twenty. Negative one hundred sixty.",
            "That's already smaller than negative one hundred.",
            D('Cross out choice 2 and circle choice 4'),
            "So choice two is too narrow. Choice four.",
            "To finish the job: x negative, y positive — negative five times four, negative twenty. Not the smallest.",
            "A hard question — but all it took was the cases and the edges."]})

    # q-337: x < y -> x < y + 5 (key 4)
    S('q-337', stem='Given: $a<b$. Which of the following is necessarily true?',
      choices=['$a<b+3$', '$3a<b$', '$a<3b$', '$a+3<b$'], correct=1, expl=[
        '$b<b+3$, so $a<b<b+3$. Therefore $a<b+3$ always.',
        'Counterexamples for the others:',
        '(2) $a=1$, $b=2$: $3a=3$, and $3<2$ is false.',
        '(3) $a=-4$, $b=-3$: $3b=-9$, and $-4<-9$ is false.',
        '(4) $a=1$, $b=2$: $a+3=4$, and $4<2$ is false.'])
    video('q-337', {
        2: ["a is less than b. Which statement MUST be true?",
            "Look at choice one: b plus three is even bigger than b.",
            D('Write "a < b < b + 3"'),
            "a is below b, and b is below b plus three. So a is below b plus three — always.",
            D('Circle choice 1'),
            "Choice one."],
        3: ["Now knock out the others — one counterexample each.",
            D('Next to choice 4 write "a = 1, b = 2: 4 < 2 ✗"'),
            "Choice four: a is one, b is two. One plus three is four — not less than two. Out.",
            D('Next to choice 2 write "3 < 2 ✗"'),
            "Choice two: three times one is three — not less than two. Out.",
            "Choice three looks safe with positive numbers. So try negatives.",
            D('Next to choice 3 write "a = −4, b = −3: −4 < −9 ✗"'),
            "a is negative four, b is negative three. Three b is negative nine. Is negative four less than that? No. Out.",
            D('Circle choice 1'),
            "Only choice one survives. Negatives are the classic trap — always try them.",
            D('Write "Try: 0, 1, −1, ½, a big number"'),
            "Your list for these questions: zero, one, negative one, one half, and a big number."]})

    # ============================== practice from the Hebrew study guide
    # q-338: m = x + y - 8, m negative integer -> x + y < 8 (key 1)
    S('q-338', stem='$k$ is a negative integer, and $k=a+b-6$. Which of the following is necessarily true about $a+b$?',
      choices=['It is an integer greater than $6$.', 'It is an integer smaller than $0$.',
               'It is an integer smaller than $6$.', 'It is an integer greater than $0$.'], correct=3, expl=[
        '$a+b=k+6$.',
        '$k$ is a negative integer, so $k\\le-1$. Therefore $a+b\\le5$, which is smaller than $6$. An integer plus $6$ is an integer.',
        '$a+b$ does not have to be negative: $k=-1$ gives $a+b=5$. It does not have to be positive: $k=-10$ gives $a+b=-4$.'])
    # q-339: 2x + 5 < 0, x^2 < 15 -> -3 (key 2)
    S('q-339', stem=given(['2x+7<0', 'x^2<20'], 'What is $x$?', pre='$x$ is an integer.\n'),
      choices=['$-3$', '$-5$', '$0$', '$-4$'], correct=4, expl=[
        'From $2x+7<0$: $x<-3.5$.',
        'From $x^2<20$: $-\\sqrt{20}<x<\\sqrt{20}$. Since $4^2=16<20<25=5^2$, the integer $x$ is between $-4$ and $4$.',
        'The only integer that is less than $-3.5$ and not less than $-4$ is $x=-4$.',
        'Check: $2(-4)+7=-1<0$ ✓ and $(-4)^2=16<20$ ✓.'])
    # q-340: x^2 < 25, 3x + 9 < 0 -> -4 (key 3)
    S('q-340', stem=given(['x^2<36', '2x+8<0'], 'What is $x$?', pre='$x$ is an integer.\n'),
      choices=['$-6$', '$-5$', '$-4$', '$-3$'], correct=2, expl=[
        'From $x^2<36$: $-6<x<6$.',
        'From $2x+8<0$: $2x<-8$, so $x<-4$.',
        'The integers that satisfy both are strictly between $-6$ and $-4$: $x=-5$.',
        'Check: $(-5)^2=25<36$ ✓ and $2(-5)+8=-2<0$ ✓.'])
    # q-341: x^3 < x^2 < 3 -> -1 (key 3)
    S('q-341', stem='$x$ is an integer, and $x^3<x^2<4$. What is $x$?',
      choices=['$1$', '$0$', '$-2$', '$-1$'], correct=4, expl=[
        'Try the choices.',
        '$x=-1$: $x^3=-1$ and $x^2=1$, and $-1<1<4$ ✓.',
        '$x=0$: $0<0$ is false. $x=1$: $1<1$ is false.',
        '$x=-2$: $x^2=4$, and $4<4$ is false.',
        'Therefore $x=-1$.'])
    # review 2026-10-06: "< 7" let both -1 and -2 fit (the question asks for one x); "< 4" keeps -1 the only integer, like the Hebrew
    # q-342: 6 < x < 7 -> x + 6 < 2x (key 1)
    S('q-342', stem='Given: $8<x<9$. Which of the following is necessarily true?',
      choices=['$17<2x$', '$x+8<2x$', '$18<2x$', '$x+9<2x$'], correct=2, expl=[
        'Simplify each choice.',
        '(1) $17<2x$ means $8.5<x$: not always (take $x=8.2$).',
        '(2) $x+8<2x$ means $8<x$. This is given, so it is always true.',
        '(3) $18<2x$ means $9<x$: never true here.',
        '(4) $x+9<2x$ means $9<x$: never true here.'])
    # q-343: p < q, r < s, q < s -> s < p cannot be true (key 4)
    S('q-343', stem=given(['a<b', 'c<d', 'b<d'], 'Which of the following cannot be true?'),
      choices=['$c<a$', '$d<a$', '$b<c$', '$c<b$'], correct=2, expl=[
        'Chain: $a<b<d$, so $a<d$ always. Therefore $d<a$ cannot be true.',
        'The others can be true, because $c$ only has to be below $d$. Take $a=1$, $b=2$, $d=5$: $c=3$ gives $b<c$, and $c=0$ gives $c<b$ and $c<a$.'])
    # q-344: x - 3 < 6 -> 8 positive integers (key 4)
    S('q-344', stem='Given: $x-2<5$. How many positive integers $x$ satisfy the inequality?',
      choices=['$7$', '$3$', '$6$', '$5$'], correct=3, expl=[
        'Add $2$: $x<7$.',
        'The positive integers below $7$ are $1, 2, 3, 4, 5, 6$. That is $6$ numbers.'])
    # q-345: -2x^2 <= -32 -> -2 does not satisfy (key 1)
    S('q-345', stem='Given: $-4x^2\\le-100$. Which of the following values of $x$ does not satisfy the inequality?',
      choices=['$-7$', '$5$', '$-3$', '$60$'], correct=3, expl=[
        'Divide by $-4$ and flip the sign: $x^2\\ge25$. (Or move the terms across with no flip: $100\\le4x^2$, so $25\\le x^2$.)',
        '$x^2$ is on the big side, so $x$ is outside the roots: $x\\le-5$ or $x\\ge5$.',
        '$-7$, $5$ and $60$ satisfy it. $x=-3$ gives $x^2=9<25$, so $-3$ does not.'])
    # q-346: a + 4 < a/2 -> a < -8 (key 4)
    S('q-346', stem='Given: $a+6<\\frac{a}{3}$. Which of the following is correct?',
      choices=['$a<-9$', '$-9<a<0$', '$6<a$', '$0<a<6$'], correct=1, expl=[
        'Multiply both sides by $3$ (positive, so no flip): $3a+18<a$.',
        'Subtract $a$: $2a+18<0$, so $2a<-18$ and $a<-9$.',
        'Check: $a=-12$ gives $-6<-4$ ✓.',
        'Method 2 · Two moves: endpoint $a+6=\\frac a3$ gives $a=-9$. Direction: $a=0$ gives $6<0$, which is false. $0$ is above $-9$, so the answer is below it: $a<-9$.'])
    # q-347: 0 < x < 1, 5y = 2x -> y^2 < 1 (key 4)
    S('q-347', stem=given(['0<x<1', '4y=3x'], 'Which of the following is correct?'),
      choices=['$1<y$', '$y^2<1$', '$y<0$', '$2<y^2$'], correct=2, expl=[
        '$y=\\frac{3x}{4}$. Since $0<x<1$: $0<y<\\frac34$.',
        'The square of a number between $0$ and $1$ is even smaller: $0<y^2<\\frac{9}{16}$, and $\\frac{9}{16}<1$.',
        'Therefore $y^2<1$.'])
    # q-348: a + b = 17, b < a -> b < 9 (key 3)
    S('q-348', stem=given(['a+b=21', 'b<a'], 'Which of the following is necessarily true?',
                          pre='$a$ and $b$ are positive integers.\n'),
      choices=['$14<a$', '$b<11$', '$a<20$', '$6<b$'], correct=2, expl=[
        '$b<a$, so $2b<a+b=21$ and $b<10.5$. $b$ is an integer, so $b\\le10<11$.',
        'Counterexamples for the others: $a=11$, $b=10$ breaks (1). $a=20$, $b=1$ breaks (3) and (4).'])
    # q-349: 3y < x < -3y -> y < 0 (key 1)
    S('q-349', stem='Given: $4m<n<-4m$. Which of the following is correct?',
      choices=['$m=0$', '$0<m<1$', '$m<0$', '$1<m$'], correct=3, expl=[
        'Ignore the middle: $4m<-4m$.',
        'Add $4m$: $8m<0$, so $m<0$.',
        'Check: $m=-1$ gives $-4<n<4$, which has solutions. $m=0$ gives $0<n<0$, which is impossible.'])
    # q-350: 0 < a - b, a + b < 0 -> b < 0 (key 4)
    S('q-350', stem=given(['0<y-x', 'x+y<0'], 'Which of the following is necessarily true?'),
      choices=['$x<0$', '$0<y$', '$y<0$', '$0<x$'], correct=1, expl=[
        'From the first: $x<y$. From the second: $y<-x$.',
        'Chain: $x<y<-x$, so $x<-x$ and $2x<0$. Therefore $x<0$.',
        'Or add two inequalities in the same direction: $x-y<0$ and $x+y<0$ give $2x<0$.',
        'The sign of $y$ is not fixed: $x=-2$, $y=1$ and $x=-2$, $y=-1$ both fit.'])
    # q-351: 5x + 2y = 0, x > 2 -> y < -5 (key 1)
    S('q-351', stem=given(['3x+2y=0', 'x>4'], 'Which of the following is necessarily true?'),
      choices=['$6<y$', '$-12<y<-4$', '$y<-6$', '$4<y<12$'], correct=3, expl=[
        '$2y=-3x$.',
        '$x>4$, so $3x>12$. Multiply by $-1$ and flip: $-3x<-12$.',
        'Therefore $2y<-12$ and $y<-6$.',
        'Check: $x=10$ gives $y=-15$, which is less than $-6$ ✓ and is outside choice (2).'])
    # q-352: 0 < 3x - 9x^2 -> 0 < x < 1/3 (key 3)
    S('q-352', stem='Given: $0<2x-8x^2$. Which of the following is necessarily true?',
      choices=['$-\\frac14<x<0$', '$0<x<\\frac14$', '$x<-\\frac14$', '$\\frac14<x$'], correct=2, expl=[
        'Take out a common factor: $2x-8x^2=2x(1-4x)$.',
        'Sign table: the product is $0$ at $x=0$ and at $x=\\frac14$. Test one number in each part.',
        '$x=-1$: $2(-1)(1+4)=-10<0$ ✗. $x=\\frac18$: $\\frac14\\cdot\\frac12=\\frac18>0$ ✓. $x=1$: $2\\cdot(-3)=-6<0$ ✗.',
        'Therefore $0<x<\\frac14$.'])
    # q-353: x < 0, 3 < x^2 - 6 < 19 -> -5 < x < -3 (key 4)
    S('q-353', stem=given(['x<0', '5<x^2-11<38'], 'Which of the following is correct?'),
      choices=['$-7<x<-4$', 'No $x$ satisfies the given conditions', '$-4<x$', '$x<-7$'], correct=1, expl=[
        'Add $11$ to all three parts: $16<x^2<49$.',
        'For positive $x$: $4<x<7$. For negative $x$: $-7<x<-4$.',
        '$x<0$, so $-7<x<-4$.',
        'Method 2 · The most precise range: test $x=-5$. $25-11=14$, and $5<14<38$ ✓. A number that works kills every choice that leaves it out: choices 2, 3 and 4. The answer is choice 1.'])
    # q-354: (3 + n)/(3 - n) > 0 -> -3 < n < 3 (key 3)
    S('q-354', stem='Given: $\\frac{2+n}{6-n}>0$, and $n\\ne6$. What is the most precise range for $n$?',
      choices=['$-2<n<0$', '$6<n$', '$0<n$', '$-2<n<6$'], correct=4, expl=[
        'Sign table: the top is $0$ at $n=-2$, and the bottom is $0$ at $n=6$.',
        '$n=-3$: $\\frac{-1}{9}<0$ ✗. $n=0$: $\\frac26>0$ ✓. $n=7$: $\\frac{9}{-1}=-9<0$ ✗.',
        'Therefore $-2<n<6$.',
        'Method 2 · The most precise range: $n=1$ gives $\\frac35>0$ ✓, so choices 1 and 2 (which leave $1$ out) are out. $n=-1$ gives $\\frac17>0$ ✓, so choice 3 is out. The answer is choice 4.'])
    # q-355: x > 0, 1/4 < x/(x+1) < 3/4 -> 1/3 < x < 3 (key 2)
    S('q-355', stem=given(['x>0', '\\frac13<\\frac{x}{x+1}<\\frac45'], 'What is the most precise range for $x$?'),
      choices=['$\\frac13<x<\\frac45$', '$0<x<1$', '$\\frac12<x<4$', '$\\frac32<x<5$'], correct=3, expl=[
        '$x>0$, so $x+1>0$. We can multiply by it without flipping.',
        'Left part: $\\frac13<\\frac{x}{x+1}$ gives $x+1<3x$, so $1<2x$ and $x>\\frac12$.',
        'Right part: $\\frac{x}{x+1}<\\frac45$ gives $5x<4x+4$, so $x<4$.',
        'Therefore $\\frac12<x<4$.',
        'Method 2 · The most precise range: test numbers where the choices disagree. $x=2$: $\\frac23$ is between $\\frac13$ and $\\frac45$ ✓. A number that works kills every choice that leaves it out: choices 1 and 2.',
        '$x=1$: $\\frac12$ is between $\\frac13$ and $\\frac45$ ✓. Choice 4 leaves $1$ out, so it is out too. The answer is choice 3.'])
    # q-356: x^2y^2 = (xy - 2)^2, x > 1 -> 0 < y < 1 (key 1)
    S('q-356', stem=given(['a^2b^2=(ab-6)^2', 'a>3'], 'Which of the following is necessarily true?'),
      choices=['$b<-1$', '$0<b<1$', '$\\frac12<b$', '$3<b$'], correct=2, expl=[
        '$a^2b^2=(ab)^2$. Two numbers with equal squares are equal or opposite.',
        'Equal: $ab=ab-6$ gives $0=-6$, which is impossible.',
        'Opposite: $ab=-(ab-6)$, so $2ab=6$ and $ab=3$.',
        'Therefore $b=\\frac3a$. Since $a>3$: $0<b<1$.',
        'Check with $a=6$, $b=\\frac12$: $a^2b^2=9$ and $(3-6)^2=9$ ✓.'])
    # q-357: y^2a + y^2c < (a + c)^2, a + c = y -> y cannot be 2 (key 1)
    S('q-357', stem=given(['k^2m+k^2n<(m+n)^2', 'm+n=k'], 'Which of the following cannot be the value of $k$?'),
      choices=['$-3$', '$\\frac12$', '$3$', '$-\\frac12$'], correct=3, expl=[
        'Take out $k^2$: $k^2(m+n)<(m+n)^2$.',
        'Substitute $m+n=k$: $k^3<k^2$.',
        'So $k^2(k-1)<0$. This needs $k\\ne0$, and then $k^2>0$, so $k-1<0$ and $k<1$.',
        '$-3$, $\\frac12$ and $-\\frac12$ are all less than $1$. But $k=3$ gives $27<9$, which is false. Therefore $k$ cannot be $3$.'])

    # ============================== order: the chain question (two inequalities sharing a side) right after the two
    # double inequalities; the plug-in question x^4 < 300 < x^5 follows it. Neither video refers to the other.
    if not RECORDED & {'q-326', 'q-327'}:
        sec = M.section_of('q-326')
        M.move('q-327', sec, before='q-326'); M.move('solve-q-327', sec, after='q-327')
        # (title slides and the spoken "Question five / six" are renumbered in course order at build)

    # ============================== practice clean-up (35 -> 27)
    # extra warm-ups: keep 3 (the flip, the overlap with <= ends, reciprocals); drop the plain 2x + 3 <= 13 and the
    # integer count (q-344 practises both), 0 < x < 1 -> x^2 < x (the lesson board itself; q-347), and a < b < 0
    # reciprocals (a copy of the Topic 3 question q-r26-t03-06).
    for qid in ['alg-extra-unit-t12-3-4', 'alg-extra-unit-t12-3-2', 'alg-extra-unit-t12-3-3', 'alg-extra-unit-t12-3-7']:
        M.unplace(qid)
    # September items: keep the types the Hebrew practice lacks (range of a - b, range of x^2, "could be true", range
    # of ab); drop adding inequalities (q-350), x > 1 powers order (q-341 / q-347; also a copy of q-r26-t03-05),
    # fraction sign (q-354) and reciprocals "cannot be true" (warm-up 3-5, q-343 / q-357).
    for k in ['07', '08', '09', '12']:
        M.unplace('q-r26-t12-' + k)
    X = 'alg-extra-unit-t12-3-'
    M.practice_order(PRACTICE, [
        X + '6', X + '1', 'q-344', 'q-346', 'q-342', X + '5', 'q-338', 'q-341', 'q-339', 'q-340',
        'q-345', 'q-347', 'q-348', 'q-343', 'q-349', 'q-351', 'q-r26-t12-05', 'q-r26-t12-06',
        'q-353', 'q-354', 'q-352', 'q-350', 'q-r26-t12-10', 'q-r26-t12-11', 'q-355', 'q-356', 'q-357'])


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber(M)   # 2026-10-06 renumber pass: runs last


# =====================================================================================================================
# 2026-10-06 Hebrew back-check: the renumber pass compared with base-v18 only. Compared again with the teacher's Hebrew
# VIDEO subtitles (01-Algebra-Original-Subtitles.txt, lines 8730-11078). Clear matches get new numbers / letters (same
# type, trap, level and methods). Nothing in topic 12 is recorded. Runs last.
# =====================================================================================================================
def hebrew_backcheck(M):
    from math_api import rich_plain

    def video(qid, slides):
        vid = 'solve-' + qid
        for n, script in slides.items():
            M.set_slide(vid, n, title=None, script=script)
        v = M.video(vid); v['title'] = v['navLabel'] = rich_plain(M.q(qid)['stemRich']).replace('\n', ' ')
        M.touched_videos.add(vid)

    # lesson "Inequalities" slide 4: -10 < -2, divide by -2 kept the Hebrew's -10 and -2 -> -18 < -3, divide by -3
    _dd_sub(M, L1, 4, [('$-10<-2$', '$-18<-3$'),
                       ("Negative ten is less than negative two. True — it's farther left.",
                        "Negative eighteen is less than negative three. True — it's farther left."),
                       ('Write "÷(−2)" under both sides, then "5 > 1"', 'Write "÷(−3)" under both sides, then "6 > 1"'),
                       ("Divide both sides by negative two: five and one.", "Divide both sides by negative three: six and one."),
                       ('Move each number to the other side: write "2 < 10"', 'Move each number to the other side: write "3 < 18"'),
                       ('Negative two goes left and becomes two. Negative ten goes right and becomes ten.',
                        'Negative three goes left and becomes three. Negative eighteen goes right and becomes eighteen.'),
                       ('−10 < −2 appears again below', '−18 < −3 appears again below'),
                       ('Write "÷2" and then "1 < 5"', 'Write "÷3" and then "1 < 6"'),
                       ('Divide by two: one is less than five. Same answer — five greater than one',
                        'Divide by three: one is less than six. Same answer — six greater than one')])
    M.slide(L1, 4)['loads'] = ''

    # q-334: the Hebrew's own letters and givens (z + y < x, x < z < y) -> m + n < p, p < n < m; key 2 -> 3
    M.set_q('q-334', stem=given(['m+n<p', 'p<n<m'], 'Which of the following is not necessarily true?'),
            choices=['$n<0$', '$p<0$', '$0<m+n$', '$m<0$'], correct=3, expl=[
                'Chain: $m+n<p<n<m$.',
                'From $m+n<n$: $m<0$. From $m+n<m$: $n<0$. From $p<n$: $p<0$.',
                'So (1), (2) and (4) are all true.',
                '$m+n$ is a sum of two negative numbers, so it is negative. Therefore $0<m+n$ is never true — it is the answer.'])
    video('q-334', {
        2: ["They ask which statement is NOT necessarily true.",
            "One side: m plus n is less than p. The other: p is less than n, less than m.",
            "p sits in both — so chain them.",
            D('Under the question write "m + n < p < n < m"'),
            "One long chain: m plus n, less than p, less than n, less than m.",
            D('Draw a number line and mark, from left to right: m + n, p, n, m'),
            "Put it on a number line: m plus n, then p, then n, then m. Left to right.",
            "How do you work a chain with lots of letters? Find two spots with the same letter.",
            D('Draw an arc linking "m + n" and "n"'),
            "m plus n is less than n. The n's cancel…",
            D('Write "m < 0"'),
            "…so m is negative.",
            "The other pair works too: m plus n is less than m — cancel the m's, and n is negative.",
            "And p is less than n — so p is negative as well.",
            D('Write "n < 0, p < 0"'),
            "m plus n: negative plus negative — negative.",
            D('Cross out choices 1, 2 and 4'),
            "Now the choices. n negative? True — out. p negative? True — out. m negative? True — out.",
            D('Circle choice 3'),
            "m plus n positive? No — it's negative. That's the one. Choice three."]})

    # q-336: kept the Hebrew's -5 and -20 (and its maximum 100) -> -6 < x < 9, -15 < y < 3
    M.set_q('q-336', stem=given(['-6<x<9', '-15<y<3'], 'What is the range of the product $xy$?'),
            choices=['$-135<xy<27$', '$-90<xy<90$', '$-90<xy<27$', '$-135<xy<90$'], correct=4, expl=[
                'Negative numbers are involved, so check all four corners: $(-6)(-15)=90$, $(-6)\\cdot3=-18$, $9\\cdot(-15)=-135$, $9\\cdot3=27$.',
                'The largest is $90$ and the smallest is $-135$.',
                'Therefore $-135<xy<90$.'])
    corners = dict(M.slide('solve-q-336', 2)['items'][1])
    video('q-336', {
        2: ["We'll solve it the psychometric way: plug in the edge numbers.",
            A("'All positive? End by end. Negatives? The corners' appears", corners),
            "Multiplying ranges end by end works only when everything is positive. With negatives inside, check the corners — and when dividing, make sure the bottom cannot be zero.",
            "x can't actually be nine — but treat it as nine, and remember the real value is just under.",
            "When is the product biggest? When it's positive. Two ways: both positive, or both negative.",
            D('Write "9 · 3 = 27" and "(−6)(−15) = 90"'),
            "Both positive: nine times three, twenty-seven. Both negative: negative six times negative fifteen — ninety.",
            "So the maximum is ninety.",
            D('Cross out choices 1 and 3'),
            "Choices one and three stop at twenty-seven. Out.",
            "Now the minimum. A negative product: one positive, one negative.",
            D('Write "9 · (−15) = −135"'),
            "x positive, y negative: nine times negative fifteen. Negative one hundred thirty-five.",
            "That's already smaller than negative ninety.",
            D('Cross out choice 2 and circle choice 4'),
            "So choice two is too narrow. Choice four.",
            "To finish the job: x negative, y positive — negative six times three, negative eighteen. Not the smallest.",
            "A hard question — but all it took was the cases and the edges."]})


_apply_before_hebrew_backcheck = apply


def apply(M):
    _apply_before_hebrew_backcheck(M)
    hebrew_backcheck(M)   # 2026-10-06 Hebrew back-check: runs last


# ---------------------------------------------------------------- 2026-10-07 pen or click
# Teacher-approved split (2026-10-04/06): lessons - content appears by click, the pen only marks (circle, cross out,
# dots); solution videos - setup and mechanical lines by click, by hand only the one or two key steps plus the marks on
# the choices. Helper copied from t10.py / t07.py (same behaviour). Works on the FINAL text (after add_methods,
# renumber and hebrew_backcheck). No topic 12 video is recorded.
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


def _fit(M, vid, n, size, gap, start=1):
    """more lines on the board now: click items a bit smaller and closer (rows kept for handwriting stay)."""
    for it in M.slide(vid, n)['items'][start:]:
        if it.get('k') != 't': continue
        it['size'] = min(it.get('size', 46), size)
        if it.get('gap', 44) <= 60: it['gap'] = min(it.get('gap', 44), gap)


def pen_or_click(M):
    P = _pen_or_click_slide
    S = 40
    # ---- lesson: inequalities - every written line is a click; the dots on the number line stay by hand
    P(M, L1, 2, {
        'Next to x ≤ 4 write "4, 3.5, 1, −6 ✓"': [A('4, 3.5, 1, −6 ✓ appears', T(r'$4,\ \ 3.5,\ \ 1,\ \ -6$ ✓', size=46, gap=60))],
        'Put dots on −7 and −2, and write "−7 < −2" above them': [
            D('Put dots on −7 and −2'), A('−7 < −2 appears', T(r'$-7<-2$', size=50))],
    })
    M.slide(L1, 2)['items'][1]['gap'] = 24
    P(M, L1, 3, {
        'Write "−6" under both sides': [A('x + 6 − 6 < 11 − 6 appears', T(r'$x+6-6<11-6$', size=56))],
        'Write "x < 5"': [A('x < 5 appears', T(r'$x<5$', size=64))],
    })
    P(M, L1, 4, {
        'Write "÷(−3)" under both sides, then "6 > 1"': [A('÷(−3): 6 > 1 appears', T(r'$\div(-3):\quad 6>1$', size=56, gap=70))],
        'Move each number to the other side: write "3 < 18"': [A('3 < 18 appears', T(r'$3<18$', size=56))],
        'Write "÷3" and then "1 < 6"': [A('÷3: 1 < 6 appears', T(r'$\div3:\quad 1<6$', size=56))],
    })
    M.slide(L1, 4)['items'][0]['gap'] = 30
    P(M, L1, 5, {
        'Write "÷(−2):  x > −3"': [A('÷(−2): x > −3 appears', T(r'$\div(-2):\quad x>-3$', size=56))],
        'Write "−6 < 2x", then "−3 < x"': [A('−6 < 2x → −3 < x appears', T(r'$-6<2x \;\to\; -3<x$', size=56))],
        'Write "x = 0: 0 < 6 ✓"': [A('x = 0: 0 < 6 ✓ appears', T(r'$x=0$: $\ 0<6$ ✓', size=56))],
    })
    # ---- lesson: signs - the rule line is a click
    P(M, SIGNS, 3, {
        'Write "same sign → flip;  different signs → no flip"': [
            A('same sign → flip; different signs → no flip appears', T(r'same sign $\to$ flip; $\ $ different signs $\to$ no flip', size=44))],
    })
    # ---- Q1 q-322 - by hand: 4 − 18 < 3x − x (x to the side with more x), circles
    P(M, 'solve-q-322', 2, {
        'Write "−14 < 2x"': [A('−14 < 2x appears', T(r'$-14<2x$', size=S))],
        'Write "÷ 2" and then "−7 < x"': [A('÷2: −7 < x appears', T(r'$\div2:\quad -7<x$', size=S))],
    }, room=['Write "4 − 18 < 3x − x"'])
    P(M, 'solve-q-322', 3, {
        'Write "Endpoint: 4 + x = 18 + 3x → −14 = 2x → x = −7"': [
            A('Endpoint: x = −7 appears', T(r'Endpoint: $4+x=18+3x \;\to\; -14=2x \;\to\; x=-7$', size=36))],
        'Write "Direction: x = 0: 4 < 18 ✓ → −7 < x"': [
            A('Direction: x = 0 ✓ → −7 < x appears', T(r'Direction: $x=0$: $\ 4<18$ ✓ $\;\to\; -7<x$', size=36))],
    })
    # ---- Q2 q-323 - by hand: cross out −15x on both sides, circle
    P(M, 'solve-q-323', 2, {
        'Write "10 − 15x − 4 < 7 − 15x"': [A('10 − 15x − 4 < 7 − 15x appears', T(r'$10-15x-4<7-15x$', size=S))],
        'Cross out −15x on both sides, then write "6 < 7"': [D('Cross out −15x on both sides'), A('6 < 7 appears', T(r'$6<7$', size=S))],
    })
    # ---- Q3 q-324 - by hand: 5 < x < 9 (the overlap), circle
    P(M, 'solve-q-324', 2, {
        'Under the left half write "3x − 4 < 2x + 5 → x < 9"': [A('left: x < 9 appears', T(r'left: $3x-4<2x+5 \;\to\; x<9$', size=S))],
        'Under the right half write "10 < 2x → 5 < x"': [A('right: 10 < 2x → 5 < x appears', T(r'right: $10<2x \;\to\; 5<x$', size=S))],
    })
    # ---- Q4 q-325 - the two halves by click; circle by hand
    P(M, 'solve-q-325', 2, {
        'Under the left part write "20 < 4x → 5 < x"': [A('left: 20 < 4x → 5 < x appears', T(r'left: $20<4x \;\to\; 5<x$', size=S))],
        'Under the right part write "6x < 12 → x < 2"': [A('right: 6x < 12 → x < 2 appears', T(r'right: $6x<12 \;\to\; x<2$', size=S))],
    })
    # ---- Q5 q-327 - by hand: 3b − 1 < a < b + 5 (chain), cross out the a, circle
    P(M, 'solve-q-327', 2, {
        'Cross out the a, then write "3b − 1 < b + 5"': [D('Cross out the a'), A('3b − 1 < b + 5 appears', T(r'$3b-1<b+5$', size=S))],
        'Write "2b < 6 → b < 3"': [A('2b < 6 → b < 3 appears', T(r'$2b<6 \;\to\; b<3$', size=S))],
    }, room=['Write "3b − 1 < a < b + 5"'])
    # ---- Q6 q-326 - by hand: the cross-out and circle; the two tries are clicks
    P(M, 'solve-q-326', 2, {
        'Next to choice 3 write "256 < 300 < 1,024 ✓"': [A('(3) x = 4: 256 < 300 < 1,024 ✓ appears', T(r'(3) $x=4$: $\ 256<300<1{,}024$ ✓', size=S))],
        'Next to choice 2 write "81 < 300 < 243 ✗"': [A('(2) x = 3: 81 < 300 < 243 ✗ appears', T(r'(2) $x=3$: $\ 81<300<243$ ✗', size=S))],
    })
    # ---- Q7 q-328 - by hand: −6 < x < 6 (between the roots), circle
    P(M, 'solve-q-328', 2, {
        'Write "2(4x² − 9) < 5(x² + 18)"': [A('2(4x² − 9) < 5(x² + 18) appears', T(r'$2(4x^2-9)<5(x^2+18)$', size=S))],
        'Write "8x² − 18 < 5x² + 90"': [A('8x² − 18 < 5x² + 90 appears', T(r'$8x^2-18<5x^2+90$', size=S))],
        'Write "3x² < 108 → x² < 36"': [A('3x² < 108 → x² < 36 appears', T(r'$3x^2<108 \;\to\; x^2<36$', size=S))],
    })
    # ---- Q8 q-329 - by hand: q < p + q < p (substitute), circle
    P(M, 'solve-q-329', 2, {
        'Write "q < p + q → p > 0"': [A('q < p + q → p > 0 appears', T(r'$q<p+q \;\to\; p>0$', size=S))],
        'Write "p + q < p → q < 0"': [A('p + q < p → q < 0 appears', T(r'$p+q<p \;\to\; q<0$', size=S))],
        'Write "p positive, q negative → pq < 0"': [A('p positive, q negative → pq < 0 appears', T(r'$p$ positive, $q$ negative $\;\to\; pq<0$', size=S))],
    }, room=['Write "q < p + q < p"'], row=70)
    _fit(M, 'solve-q-329', 2, 34, 12)
    # ---- Q9 q-r26-t12-01 - by hand: x = −½ (the number we pick), circle
    P(M, 'solve-q-r26-t12-01', 2, {
        'Next to the choices write "−½,  ¼,  −⅛,  −2"': [
            A('choices −½, ¼, −⅛, −2 appears', T(r'(1) $-\frac12\quad$(2) $\frac14\quad$(3) $-\frac18\quad$(4) $-2$', size=S))],
    }, room=['Write "x = −½"'])
    # ---- Q10 q-r26-t12-02 - by hand: the number line with −5 and 2 (sign table), circle
    P(M, 'solve-q-r26-t12-02', 2, {
        'Write "x − 2 = 0 → x = 2;   x + 5 = 0 → x = −5"': [
            A('zeros: x = 2, x = −5 appears', T(r'$x-2=0 \;\to\; x=2;\qquad x+5=0 \;\to\; x=-5$', size=36))],
        'Write "x = −6: (−8)(−1) = 8 ✗"': [A('x = −6: 8 ✗ appears', T(r'$x=-6$: $\ (-8)(-1)=8$ ✗', size=36))],
        'Write "x = 0: (−2)(5) = −10 ✓"': [A('x = 0: −10 ✓ appears', T(r'$x=0$: $\ (-2)(5)=-10$ ✓', size=36))],
        'Write "x = 3: (1)(8) = 8 ✗"': [A('x = 3: 8 ✗ appears', T(r'$x=3$: $\ (1)(8)=8$ ✗', size=36))],
    }, room=['Draw a number line and mark −5 and 2'], row=90)
    _fit(M, 'solve-q-r26-t12-02', 2, 36, 12)
    # ---- Q11 q-r26-t12-13 - by hand: the cross-outs and circle; the tests and the two moves are clicks
    P(M, 'solve-q-r26-t12-13', 2, {
        'Write "x = −3: 3 + 6 = 9 < 5 ✗"': [A('x = −3: 9 < 5 ✗ appears', T(r'$x=-3$: $\ 3+6=9<5$ ✗', size=S))],
        'Write "x = 6: 3 − 12 = −9 ≥ −7 ✗"': [A('x = 6: −9 ≥ −7 ✗ appears', T(r'$x=6$: $\ 3-12=-9\ge-7$ ✗', size=S))],
    })
    P(M, 'solve-q-r26-t12-13', 3, {
        'Write "3 − 2x = 5 → x = −1;  3 − 2x = −7 → x = 5"': [
            A('endpoints x = −1, x = 5 appears', T(r'$3-2x=5 \;\to\; x=-1;\qquad 3-2x=-7 \;\to\; x=5$', size=36))],
        'Write "x = 0: −7 ≤ 3 < 5 ✓ → −1 < x ≤ 5"': [
            A('x = 0 ✓ → −1 < x ≤ 5 appears', T(r'$x=0$: $\ -7\le3<5$ ✓ $\;\to\; -1<x\le5$', size=36))],
    })
    # ---- Q12 q-330 - by hand: = 2/3 and = 9/10 under the fractions, 2x + 2 < 3x (multiply by the positive 3(x + 1)), circles
    P(M, 'solve-q-330', 2, {
        'Write "2/3 < x/(x+1)" and "x/(x+1) < 9/10" on two lines': [
            A('2/3 < x/(x+1) and x/(x+1) < 9/10 appears', T(r'$\frac23<\frac{x}{x+1}\qquad$ and $\qquad\frac{x}{x+1}<\frac9{10}$', size=36))],
        'Multiply both sides by 10(x + 1): write "10x < 9x + 9 → x < 9"': [
            A('10x < 9x + 9 → x < 9 appears', T(r'$\cdot10(x+1)$: $\ 10x<9x+9 \;\to\; x<9$', size=36))],
        'Write "2 < x < 9 → 3, 4, 5, 6, 7, 8"': [A('2 < x < 9 → 3, …, 8 appears', T(r'$2<x<9 \;\to\; 3,4,5,6,7,8$', size=36))],
    }, room=['Under 60/90 write "= 2/3"', 'Multiply both sides by 3(x + 1): write "2x + 2 < 3x → 2 < x"'], row=50)
    _fit(M, 'solve-q-330', 2, 36, 14)
    P(M, 'solve-q-330', 3, {
        'Next to the question write "3/4, 4/5, 5/6, 6/7, 7/8, 8/9"': [
            A('3/4, 4/5, …, 8/9 appears', T(r'$\frac34,\ \frac45,\ \frac56,\ \frac67,\ \frac78,\ \frac89$', size=S))],
    })
    # ---- Q13 q-331 - by hand: cross out x², y > 0 (the sign of y), circle
    P(M, 'solve-q-331', 2, {
        'Under the question write "x²y² < x²y"': [A('x²y² < x²y appears', T(r'$x^2y^2<x^2y$', size=S))],
        'Cross out x² on both sides; write "y² < y"': [D('Cross out x² on both sides'), A('y² < y appears', T(r'$y^2<y$', size=S))],
        'Write "y < 1"': [A('y < 1 appears', T(r'$y<1$', size=S))],
        'Write "0 < y < 1" and circle choice 4': [A('0 < y < 1 appears', T(r'$0<y<1$', size=S)), D('Circle choice 4')],
    }, room=['Write "y > 0"'], row=60)
    _fit(M, 'solve-q-331', 2, 36, 12)
    # ---- Q14 q-332 - by hand: "top + / bottom −" and "top − / bottom +" (the two cases), cross-outs, circles
    P(M, 'solve-q-332', 2, {
        'Write "x + 1 > 0 → x > −1" and "7 − x < 0 → x > 7"': [
            A('x > −1 and x > 7 appears', T(r'$x+1>0 \;\to\; x>-1;\qquad 7-x<0 \;\to\; x>7$', size=34))],
        'Write "→ x > 7"': [A('→ x > 7 appears', T(r'$\to\; x>7$', size=34))],
        'Write "x < −1" and "x < 7 → x < −1"': [A('x < −1 and x < 7 → x < −1 appears', T(r'$x<-1$ and $x<7 \;\to\; x<-1$', size=34))],
    }, room=['Under the question write "top + / bottom −" and "top − / bottom +"'], row=70)
    _fit(M, 'solve-q-332', 2, 34, 12)
    P(M, 'solve-q-332', 3, {
        'Next to choice 1 write "x = −2: −1/9 < 0 ✓"': [A('(1) x = −2: −1/9 < 0 ✓ appears', T(r'(1) $x=-2$: $\ -\frac19<0$ ✓', size=S))],
        'Next to choice 2 write "x = 8: 9/(−1) = −9 ✓"': [A('(2) x = 8: −9 ✓ appears', T(r'(2) $x=8$: $\ \frac9{-1}=-9$ ✓', size=S))],
        'Next to choice 3 write "x = 0: 1/7"': [A('(3) x = 0: 1/7 appears', T(r'(3) $x=0$: $\ \frac17$', size=S))],
    })
    # ---- Q15 q-333 - by hand: x + y = ±12 and crossing out the minus, circles
    P(M, 'solve-q-333', 2, {
        'Write "x > 4"': [A('x > 4 appears', T(r'$x>4$', size=S))],
        'Write "x = 12 − y → 4 < 12 − y → y < 8"': [A('x = 12 − y → 4 < 12 − y → y < 8 appears', T(r'$x=12-y \;\to\; 4<12-y \;\to\; y<8$', size=S))],
        'Write "0 < y < 8" and circle choice 2': [A('0 < y < 8 appears', T(r'$0<y<8$', size=S)), D('Circle choice 2')],
    }, room=['Write "x + y = ±12"'])
    _fit(M, 'solve-q-333', 2, 36, 16)
    P(M, 'solve-q-333', 3, {
        'Write "x = 5 → y = 7, x = 6 → y = 6"': [A('x = 5 → y = 7, x = 6 → y = 6 appears', T(r'$x=5 \;\to\; y=7,\qquad x=6 \;\to\; y=6$', size=S))],
    })
    # ---- Q16 q-334 - by hand: the chain m + n < p < n < m, the number line, the arc, cross-outs, circle
    P(M, 'solve-q-334', 2, {
        'Write "m < 0"': [A('m < 0 appears', T(r'$m<0$', size=36))],
        'Write "n < 0, p < 0"': [A('n < 0, p < 0 appears', T(r'$n<0,\ \ p<0$', size=36))],
    }, room=['Under the question write "m + n < p < n < m"', 'Draw a number line and mark, from left to right: m + n, p, n, m'], row=60)
    # ---- Q17 q-335 - by hand: the marks on the number line, circle
    P(M, 'solve-q-335', 2, {
        'Write "+4" under all three parts, then "9 ≤ x² ≤ 64"': [A('+4: 9 ≤ x² ≤ 64 appears', T(r'$+4$:$\quad 9\le x^2\le64$', size=36))],
        'Write "3 ≤ x ≤ 8"': [A('3 ≤ x ≤ 8 appears', T(r'$3\le x\le8$', size=36))],
        'Write "±3, ±4, ±5, ±6, ±7, ±8"': [A('±3, …, ±8 appears', T(r'$\pm3,\ \pm4,\ \pm5,\ \pm6,\ \pm7,\ \pm8$', size=36))],
    })
    for it in M.slide('solve-q-335', 2)['items']:
        if it.get('k') == 'nl': it.pop('y', None)   # the number line now follows the two click lines
    _fit(M, 'solve-q-335', 2, 34, 10)
    # ---- Q18 q-r26-t12-03 - by hand: a + c > b + d (add - the safe move), circle; the counterexamples are clicks
    P(M, 'solve-q-r26-t12-03', 4, {
        'Next to choice 2 write "a = 2, b = 1, c = 5, d = 0:  −3 > 1 ✗"': [
            A('(2) a = 2, b = 1, c = 5, d = 0: −3 > 1 ✗ appears', T(r'(2) $a=2,\ b=1,\ c=5,\ d=0$: $\ -3>1$ ✗', size=36))],
        'Next to choice 3 write "a = −1, b = −2, c = −1, d = −2:  1 > 4 ✗"': [
            A('(3) a = −1, b = −2, c = −1, d = −2: 1 > 4 ✗ appears', T(r'(3) $a=-1,\ b=-2,\ c=-1,\ d=-2$: $\ 1>4$ ✗', size=36))],
        'Next to choice 4 write "a = 2, b = 1, c = 4, d = 1:  ½ > 1 ✗"': [
            A('(4) a = 2, b = 1, c = 4, d = 1: ½ > 1 ✗ appears', T(r'(4) $a=2,\ b=1,\ c=4,\ d=1$: $\ \frac12>1$ ✗', size=36))],
    })
    # ---- Q19 q-r26-t12-04 - by hand: biggest: 5 − 1 = 4 (biggest minus smallest), circle
    P(M, 'solve-q-r26-t12-04', 2, {
        'Write "smallest: −2 − 4 = −6"': [A('smallest: −2 − 4 = −6 appears', T(r'smallest: $-2-4=-6$', size=S))],
        'Write "−6 < x − y < 4"': [A('−6 < x − y < 4 appears', T(r'$-6<x-y<4$', size=S))],
        'Write "−4 < −y < −1  →  add"': [A('−4 < −y < −1 → add appears', T(r'check: $-4<-y<-1 \;\to\;$ add', size=S))],
    }, room=['Write "biggest: 5 − 1 = 4"'], row=60)
    _fit(M, 'solve-q-r26-t12-04', 2, 34, 12)
    # ---- Q20 q-336 - the corners by click; the cross-outs and circle by hand
    P(M, 'solve-q-336', 2, {
        'Write "9 · 3 = 27" and "(−6)(−15) = 90"': [A('9 · 3 = 27, (−6)(−15) = 90 appears', T(r'$9\cdot3=27,\qquad (-6)(-15)=90$', size=S))],
        'Write "9 · (−15) = −135"': [A('9 · (−15) = −135 appears', T(r'$9\cdot(-15)=-135$', size=S))],
    })
    # ---- Q21 q-337 - by hand: a < b < b + 3 (method 1), circles; the counterexamples and the list are clicks
    P(M, 'solve-q-337', 3, {
        'Next to choice 4 write "a = 1, b = 2: 4 < 2 ✗"': [A('(4) a = 1, b = 2: 4 < 2 ✗ appears', T(r'(4) $a=1,\ b=2$: $\ 4<2$ ✗', size=S))],
        'Next to choice 2 write "3 < 2 ✗"': [A('(2) 3 < 2 ✗ appears', T(r'(2) $3<2$ ✗', size=S))],
        'Next to choice 3 write "a = −4, b = −3: −4 < −9 ✗"': [A('(3) a = −4, b = −3: −4 < −9 ✗ appears', T(r'(3) $a=-4,\ b=-3$: $\ -4<-9$ ✗', size=S))],
        'Write "Try: 0, 1, −1, ½, a big number"': [A('Try: 0, 1, −1, ½, a big number appears', T(r'Try: $0,\ 1,\ -1,\ \frac12,$ a big number', size=S))],
    })


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
        m = _sp_re.match(r'(.+)-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$', _sp_os.path.basename(f))
        # only takes recorded BEFORE the spread was first built (2026-10-07 12:55 local = 09:55Z) keep the old video;
        # later takes were recorded with the new slides, so the slides must stay
        if m and m.group(2) < '2026-10-07T09-55-00': out.add(m.group(1))
    return out


SPREAD_LINES = {
    'q-324': ['Method 2 · The most precise range: test numbers where the choices disagree. $x=7$: $17<19<23$ ✓, so choice 1 (which leaves $7$ out) is out. $x=0$: $-4<5<-5$ ✗, so choice 4 (it contains $0$) is out. $x=10$: $26<25$ ✗, so choice 3 is out. The answer is choice 2.'],
    'q-325': ['Method 2 · The most precise range: $x=6$ gives $40<44$, but $44<20$ ✗. $6$ fails, so choices 1 and 4 (they contain $6$) are out. $x=0$ gives $28<8$ ✗, so choice 3 is out too. Only choice 2 is left.'],
    'q-328': ['Method 2 · The most precise range: test $x=0$: $-\\frac95<9$ ✓. $0$ works, so every choice that leaves $0$ out (choices 2, 3 and 4) is out. The answer is choice 1, with no algebra.'],
    'q-r26-t12-02': ['Method 2 · The most precise range: $x=0$ works ($-10<0$), so choice 1 (which leaves $0$ out) is out. $x=3$ fails ($8$ is not negative), so choice 3 is out. $x=-6$ fails ($8$ again), so choice 4 is out. The answer is choice 2.'],
    'q-331': ['Method 2 · The most precise range: $x=2$, $y=\\frac12$ fits ($1<2$), so choices 1 and 3 (they keep $x$ below $1$) are out. $y=-\\frac12$ never fits: $\\frac{x^2}4<-\\frac{x^2}2$ is false for every $x$. So choice 2 (it contains $-\\frac12$) is out. The answer is choice 4.'],
    'q-347': ['Method 2 · Pick values that fit: $x=\\frac12$ gives $y=\\frac38$ and $y^2=\\frac{9}{64}$. Choices 1, 3 and 4 fail for these values, so they are not necessarily true. Only choice 2 is left.'],
    'q-349': ['Method 2 · The most precise range: $m=-1$ works ($n=0$: $-4<0<4$ ✓). So every choice that leaves $-1$ out (choices 1, 2 and 4) is out. The answer is choice 3.'],
    'q-352': ['Method 2 · The most precise range: $x=\\frac18$ works ($\\frac14-\\frac18=\\frac18>0$). Every choice that leaves $\\frac18$ out (choices 1, 3 and 4) is out. The answer is choice 2.'],
}

SPREAD_SLIDES = {
    'solve-q-325': ('Split — and no overlap', 'Method 2 · Test a number', [
        "Or don't solve at all — test numbers. Six is in choices one and four.",
        A('x = 6 test appears', T(r'$x=6$: $\ 40<44<20$ ✗', size=40)),
        "Forty is less than forty-four. But forty-four less than twenty? No. Six fails — so every choice that contains six is out.",
        D('Cross out choices 1 and 4'),
        A('x = 0 test appears', T(r'$x=0$: $\ 28<8$ ✗', size=40)),
        "Zero is in choice three. Twenty-eight less than eight? No. Out as well.",
        D('Cross out choice 3 and circle choice 2'),
        "Only choice two is left: no value works.",
    ]),
    'solve-q-328': ('Multiply by 10, then the rule', 'Method 2 · Test a number', [
        "And a shortcut with no algebra: test one number. Zero is the easiest.",
        A('x = 0 test appears', T(r'$x=0$: $\ -\frac95<\frac{18}{2}=9$ ✓', size=40)),
        "Minus nine over five is negative. Less than nine. True — so zero must be in the answer.",
        D('Cross out choices 2, 3 and 4'),
        "Choices two, three and four leave zero out. Only choice one is left.",
    ]),
}

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


# =====================================================================================================================
# 2026-10-07 shaded number lines (teacher idea): in a few videos the answer range appears as a shaded number line -
# one figure + one short spoken line, right after the range is found. Method, numbers and answers unchanged.
# Recorded videos are never touched (_shaded_nl.recorded: takes from before the cutoff keep the old video).
# =====================================================================================================================
def _snl():
    import importlib.util, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_shaded_nl.py')
    spec = importlib.util.spec_from_file_location('_shaded_nl', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m


def _snl_n(M, vid, title):
    ns = [i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title]
    assert len(ns) == 1, (vid, title, ns); return ns[0]


def number_lines(M):
    S = _snl(); fig = S.fig
    todo = [
        # q-325: x > 5 AND x < 2 - two rays that never meet
        ('solve-q-325', 'Split — and no overlap', "It's not OR. It has to be both at the same time.",
         fig(-2, 9, [(0, '0'), (2, '2'), (5, '5')], [], bars=[(None, 2, False, False, 'x < 2'), (5, None, False, False, 'x > 5')],
             title='x less than 2 and x greater than 5: no overlap'),
         'Number line: x < 2 and x > 5, no overlap appears',
         "On the number line: one ray goes left from two, the other goes right from five. They never meet.", 900),
        # q-328: x² < 36 - a segment between the roots
        ('solve-q-328', 'Multiply by 10, then the rule', 'Root of thirty-six is six.',
         fig(-9, 9, [(-6, '−6'), (0, '0'), (6, '6')], [(-6, 6, False, False)], title='x squared less than 36: between −6 and 6'),
         'Number line: −6 < x < 6 shaded appears',
         "On the number line: one segment, from negative six to six. Open circles — six itself doesn't work.", 900),
        # q-r26-t12-13: the most precise range -1 < x <= 5
        ('solve-q-r26-t12-13', 'Method 2 · Two moves', 'Negative one less than x, x at most five.',
         fig(-4, 8, [(-1, '−1'), (0, None), (5, '5')], [(-1, 5, False, True)], title='−1 < x ≤ 5'),
         'Number line: −1 < x ≤ 5 shaded appears',
         "On the number line: an open circle at negative one, a full circle at five — five is included.", 900),
        # q-331: 0 < y < 1
        ('solve-q-331', 'Check the sign, then cancel', 'Positive and less than one: between zero and one.',
         fig(-2, 2, [(-1, '−1'), (0, '0'), (1, '1')], [(0, 1, False, False)], title='0 < y < 1'),
         'Number line: 0 < y < 1 shaded appears',
         "On the number line: y lives in the short segment between zero and one.", 800),
        # q-332: the sign table - minus, plus, minus; the fraction is negative on the two outer rays
        ('solve-q-332', 'Method 1 · Two cases', 'A shorter way to write it: the sign table.',
         fig(-4, 10, [(-1, '−1'), (0, None), (7, '7')], [(None, -1, False, False), (7, None, False, False)],
             signs=[(-2.7, '−'), (3, '+'), (8.7, '−')], title='(x + 1)/(7 − x) < 0: x < −1 or x > 7'),
         'Number line: sign table − + −, x < −1 or x > 7 shaded appears',
         "Minus, plus, minus. The fraction is negative on the two outer rays — the middle is what does NOT satisfy it.", 900),
        # summary: x² < 25 a segment, x² >= 49 two rays
        ('r26-t12-summary', 'x² inequalities', "On the big side: x is outside the roots.",
         S.two(dict(lo=-10, hi=10, ticks=[(-5, '−5'), (0, '0'), (5, '5')], segs=[(-5, 5, False, False)], cap='x² < 25'),
               dict(lo=-10, hi=10, ticks=[(-7, '−7'), (0, '0'), (7, '7')], segs=[(None, -7, False, True), (7, None, True, False)], cap='x² ≥ 49'),
               title='x² < 25: a segment; x² ≥ 49: two rays'),
         'Number lines: x² < 25 segment, x² ≥ 49 two rays appear',
         "On the number line: small side — one segment between the roots. Big side — two rays going outward.", 1000),
    ]
    for vid, title, after, svg, label, say, w in todo:
        if S.recorded(vid): continue   # recorded: never change it
        S.add(M, vid, _snl_n(M, vid, title), after, svg, label, say, w=w)


_apply_before_number_lines = apply


def apply(M):
    _apply_before_number_lines(M)
    number_lines(M)   # 2026-10-07 shaded number lines: runs last


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
    # r26-t12-signs: "Between 0 and 1" was taught in topic 8 (Exponent Traps) and topic 3 (x, x² or 1/x?);
    # reciprocals in topics 1 and 2; must / could / cannot in topic 1 (Must, Could, Cannot) and topic 21.
    # Only the reciprocal rule for an INEQUALITY is new: one short slide + a one-line reminder.
    G = 'r26-t12-signs'
    if not R.recorded(G):
        R.drop_slide(M, G, 'Between 0 and 1')
        R.drop_slide(M, G, 'Must, could, cannot')
        R.retitle(M, G, 'Reciprocals in Inequalities')
        R.set_slide(M, G, 'Reciprocals in Inequalities', ['One new rule before the advanced questions.'])
        R.set_slide(M, G, 'Reciprocals', [
            'One over both sides of an inequality — what happens to the sign?',
            A('2 < 3 → 1/2 > 1/3 appears', T(r'$2<3\ \Rightarrow\ \frac12>\frac13$')),
            'Two is less than three. But one half is MORE than one third. The sign flips.',
            A('−3 < −2 → −1/3 > −1/2 appears', T(r'$-3<-2\ \Rightarrow\ -\frac13>-\frac12$')),
            'Both negative? It still flips.',
            A('−2 < 3 → −1/2 < 1/3 appears', T(r'$-2<3\ \Rightarrow\ -\frac12<\frac13$')),
            'One negative and one positive? No flip. The negative one stays smaller.',
            A('same sign → flip; different signs → no flip appears', T(r'same sign $\to$ flip; $\ $ different signs $\to$ no flip')),
            'So: same sign — flip. Different signs — no flip.',
            'Numbers between zero and one, and must, could and cannot, work exactly as you learned them.',
            'Now the questions. Try each one first — then watch.'],
            new_title='Reciprocals in inequalities')
        R.set_sidebar_label(M, G, 'Reciprocals', 'Reciprocals in inequalities')


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
    _mn_load().method_names(M, 12)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 Hebrew points restored. The 2026-10-05 cut assumed the question videos teach what the lesson taught;
# here they only answered the questions, and a few of the teacher's Hebrew lesson points were lost. Each point is put
# back as a few spoken lines. These videos were recorded: the teacher decided (2026-10-08) to re-record / continue
# them, so each one is listed in _rerecord.RERECORD (option 1 = re-record the whole video, option 2 = new last slide,
# "Continue a take"). See tNN_CHANGES.md ("2026-10-08 Hebrew points restored"). Runs LAST.
# =====================================================================================================================
import importlib.util as _ilu_hb, os as _os_hb
_s_hb = _ilu_hb.spec_from_file_location('_hebrew_back', _os_hb.path.join(_os_hb.path.dirname(_os_hb.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu_hb.module_from_spec(_s_hb); _s_hb.loader.exec_module(HB)


def _hb_last_slide(M, vid, title, script):
    """option 2: one new slide at the END of the video (same question on the board, same sidebar item)."""
    b = M.video(vid)['beats'][-1]
    HB.append_slides(M, vid, [dict(mode=b['mode'], title=title, active=b['active'],
                                   pre=[dict(it) for it in b['items'][:b['pre']]], script=script)])


def hebrew_points_back(M):
    # Q6 (q-326): the Hebrew lesson's exam remark on trial-and-error inequality questions (very common, often early in
    # the section, look easy, hard by algebra - simple by plugging in)
    _hb_last_slide(M, 'solve-q-326', 'Trial and error', [
        A("'Trial and error → plug in the choices or numbers' appears", T('Trial and error $\\to$ plug in the choices, or numbers', size=40)),
        'A word about this type. Trial-and-error questions are very common in inequalities.',
        'Often they come early in the section. They look easy — and by algebra alone they are really hard.',
        'Plug in the choices, or numbers — and they become simple.'])
    # Q7 (q-328): "second-degree inequalities: rare on the exam, but important to know"; the hardest part of the
    # lesson - check it with numbers (why the range is symmetric)
    _hb_last_slide(M, 'solve-q-328', 'Rare — but know it', [
        'Second-degree inequalities are rare on the exam — but important to know. This is the hardest part of this topic.',
        'Not sure yet? Test a few numbers yourself.',
        A("'5² = 25 ✓, (−5)² = 25 ✓, (±7)² = 49 ✗' appears",
          T('$5^2=25<36$ ✓ $\\quad (-5)^2=25<36$ ✓ $\\quad (\\pm7)^2=49$ ✗', size=40)),
        'Five squared is twenty-five — under thirty-six, so five is in. Negative five too: its square is also twenty-five.',
        "Seven, or negative seven? Forty-nine — too big. That's why the answer is symmetric: from negative six to six."])


_apply_before_hebrew_points_back = apply


def apply(M):
    _apply_before_hebrew_points_back(M)
    hebrew_points_back(M)   # 2026-10-08 Hebrew points restored: runs LAST
