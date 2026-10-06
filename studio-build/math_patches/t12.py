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
    M.new_q(g, TOPIC, 'Given: $x^2+3x<10$. Which of the following is the most precise range for $x$?',
            ['$x<2$', '$-2<x<5$', '$-5<x<2$', '$x>-5$'], 3, [
        'Test numbers that some choices contain and others leave out.',
        '$x=3$: $9+9=18<10$ ✗. $3$ fails, so every choice that contains $3$ is wrong: choices 2 and 4 are out.',
        '$x=-6$: $36-18=18<10$ ✗. $-6$ fails, so choice 1 (it contains $-6$) is out. The answer is choice 3.',
        'Two moves: the endpoints solve $x^2+3x=10$, that is $(x+5)(x-2)=0$, so $x=-5$ or $x=2$. $x=0$ gives $0<10$ ✓, so the answer is the part between them: $-5<x<2$.'])
    M.place_q(g, ADV, after='solve-q-r26-t12-02')
    _old, ADV_SIDEBAR = ADV_SIDEBAR, ADV_SB
    _solution(M, g, ["Question twenty-one.", "Choices that are ranges, and they want the most precise one. Test numbers."], [
        ('Method 1 · Test a number', [
            "The cue: four ranges in the choices, and the words \"most precise range\".",
            "The rule: a number that works must be inside the answer. A number that fails must be outside it.",
            "So pick numbers where the choices disagree. Three: choices two and four contain it, choices one and three don't.",
            D('Write "x = 3: 9 + 9 = 18 < 10 ✗"'),
            "Three squared is nine, plus nine: eighteen. Less than ten? No. Three fails.",
            D('Cross out choices 2 and 4'),
            "So the answer can't contain three. Choices two and four contain it. Both out.",
            "Choices one and three disagree about negative six: choice one contains it, choice three doesn't.",
            D('Write "x = −6: 36 − 18 = 18 < 10 ✗"'),
            "Negative six squared: thirty-six. Minus eighteen: eighteen. Less than ten? No. It fails.",
            D('Cross out choice 1 and circle choice 3'),
            "Choice one contains negative six — out. Choice three. We never solved anything."]),
        ('Method 2 · Two moves', [
            "The two-move way gives the same answer.",
            D('Write "x² + 3x = 10 → (x + 5)(x − 2) = 0 → x = −5, x = 2"'),
            "Endpoints: pretend it's equals. Two numbers with product negative ten and sum three: five and negative two. x is negative five or two.",
            D('Write "x = 0: 0 < 10 ✓ → −5 < x < 2"'),
            "Direction: test zero. Zero is less than ten — it works. Zero is between the endpoints, so the answer is the part between them.",
            "Negative five less than x less than two. Choice three.",
            "Choice two is the trap: the endpoints with the wrong signs."]),
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
