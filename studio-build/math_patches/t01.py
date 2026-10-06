"""Topic 1 — Algebraic Fundamentals. Course review 2026-09 fixes (see t01_CHANGES.md)."""
import copy
from math_api import T, H, A, D, Q

TOPIC = 1
NUM, ADD, MUL, ORD, FAST = 'numbers', 'add-subtract', 'multiply-divide', 'order-of-operations', 'fast-calculation'


# ----------------------------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------------------------
def script_of(M, vid, n):
    """Current script of a slide in DSL form (A items are the non-pre items)."""
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], dict(b['items'][l['appear']])))
        else: out.append(D(l['draw']))
    return out


def _txt(x):
    if isinstance(x, str): return x
    if x[0] == 'D': return x[1]
    return x[1]


def rep(script, old, new):
    """Replace the script element whose text is exactly `old` with `new` (str, tuple, or a list of elements)."""
    for k, x in enumerate(script):
        if _txt(x) == old:
            script[k:k + 1] = new if isinstance(new, list) else [new]
            return script
    raise KeyError('line not found: ' + old)


def ins_after(script, old, new):
    for k, x in enumerate(script):
        if _txt(x) == old:
            script[k + 1:k + 1] = new
            return script
    raise KeyError('line not found: ' + old)


def item_text(M, vid, n, old, new):
    b = M.slide(vid, n)
    for it in b['items']:
        if it.get('t') == old:
            it['t'] = new; M.touched_videos.add(vid); return
    raise KeyError('item not found: %s #%d %s' % (vid, n, old))


def fix_lines(M, vid, n, pairs):
    """Replace substrings in say/draw/label texts of one slide."""
    def fn(lines):
        out = []
        for l in lines:
            l = dict(l)
            for k in ('say', 'draw', 'label'):
                if k in l:
                    for o, nw in pairs: l[k] = l[k].replace(o, nw)
            out.append(l)
        return out
    M.edit_lines(vid, n, fn)


def shift_active(M, vid, from_n, delta):
    for b in M.video(vid)['beats'][from_n - 1:]:
        if b['mode'] != 'title' and b['active'] >= 0: b['active'] += delta
    M.touched_videos.add(vid)


def move_q(M, qid, section, after=None, before=None):
    """The API has no 'move': unplace() drops the question data, so keep a copy and put it back."""
    q = copy.deepcopy(M.q(qid))
    M.unplace(qid)
    M.D['questions'][qid] = q
    M.place_q(qid, section, after=after, before=before)


def guided(M, qid, section, sidebar, intro, slides, after=None, before=None):
    """Place a guided question and create its solution video. slides = [(title, script), ...]"""
    M.place_q(qid, section, after=after, before=before)
    n = M.next_question_number(TOPIC)
    sl = [dict(mode='title', title='Question %d' % n, script=['Question %d.' % n] + intro)]
    for k, (title, script) in enumerate(slides):
        sl.append(dict(mode='question', title=title, active=k, pre=[Q(qid)], script=script))
    M.new_video('solve-' + qid, TOPIC, 'Question %d' % n, sidebar, sl, section, kind='solution', qid=qid)


def qid(n): return 'q-r26-t01-%02d' % n


def apply(M):
    S = M.set_q

    # ============================================================================================================
    # 1. Existing questions: TeX, no ":" for division, full worked solutions with numbers
    # ============================================================================================================
    S('q-001', expl=['Ones: $4+8=12$. Write $2$ and carry $1$.',
                     'Tens: $3+4+1=8$. The sum is $82$.'])
    S('q-002', expl=['Two minus signs touching become a plus: $73-(-46)=73+46=119$.',
                     'The trap $27$ comes from $73-46$: the sign flip was ignored.'])
    S('q-005', expl=['Both parts are negative. They pile up on the negative side of zero.',
                     'Add the sizes: $62+25=87$. The answer is $-87$.'])
    S('q-006', expl=['A bigger number is subtracted from a smaller one. The answer is negative.',
                     'The difference is $58-31=27$. Therefore $31-58=-27$.'])
    S('q-007', expl=['Ones: $8+5=13$. Write $3$ and carry $1$.',
                     'Tens: $6+8+1=15$. Write $5$ and carry $1$.',
                     'Hundreds: $4+1=5$. The sum is $553$. Estimate: $470+85\\approx 555$.'])
    S('q-008', expl=['Ones: $6+5=11$. Write $1$ and carry $1$.',
                     'Tens: $6+5+1=12$. Write $2$ and carry $1$.',
                     'Hundreds: $6+5+1=12$. Write $2$ and carry $1$.',
                     'The last carry is the thousands digit $1$. Total: $1{,}221$.'])
    S('q-009', expl=['$994$ is $6$ less than $1{,}000$. Subtract $1{,}000$, then give the $6$ back.',
                     '$8{,}003-1{,}000=7{,}003$, and $7{,}003+6=7{,}009$.'])
    S('q-010', expl=['Subtract in two pieces, $606=600+6$.',
                     '$5{,}005-600=4{,}405$, then $4{,}405-6=4{,}399$.'])
    S('q-011', stem='$\\left(-64\\right) \\div \\left(-8\\right) = ?$',
      expl=['Same signs give a positive answer.', 'Sizes: $64\\div 8=8$. The answer is $8$.'])
    S('q-012', expl=['Split $13$ into $10+3$: $9\\cdot 10=90$ and $9\\cdot 3=27$.',
                     'Then $9\\cdot 13=90+27=117$.',
                     'Faster check: the last digit comes from $9\\cdot 3=27$. The answer ends in $7$, and only $117$ and $97$ are left. '
                     'Also $9\\cdot 13$ is more than $9\\cdot 12=108$. That rules out $97$.'])
    S('q-013', expl=['Split $14$ into $10+4$: $12\\cdot 10=120$ and $12\\cdot 4=48$.',
                     'Then $12\\cdot 14=120+48=168$.'])
    S('q-014', stem='$666 \\times 11 = ?$',
      expl=['Times $11$ is times $10$ plus one more copy.',
            '$666\\times 10=6{,}660$, and $6{,}660+666=7{,}326$.'])
    S('q-015', stem='$320 \\div 5 = ?$',
      expl=['Split $320$ into $300+20$: $300\\div 5=60$ and $20\\div 5=4$.', 'Then $320\\div 5=60+4=64$.'])
    S('q-016', stem='$192 \\div 4 = ?$',
      expl=['Split $192$ into $160+32$. Both parts divide by $4$: $160\\div 4=40$ and $32\\div 4=8$.',
            'Then $192\\div 4=40+8=48$.'])
    S('q-017', stem='$3{,}618 \\div 18 = ?$',
      expl=['Split $3{,}618$ into $3{,}600+18$: $3{,}600\\div 18=200$ and $18\\div 18=1$.',
            'The answer is $201$. Check: $18\\cdot 201=3{,}600+18=3{,}618$.'])
    # Pass 2 (plan): q-018 is restored in its original fraction form and moves to the Topic 2 practice (see the end of
    # apply()). Its quotient-and-remainder version stays in Topic 1 as a new question, q-r26-t01-25.
    S('q-018', stem='$200 \\div 6 = ?$',
      choices=['$33\\,\\frac{1}{6}$', '$33\\,\\frac{1}{3}$', '$33\\,\\frac{2}{3}$', '$33\\,\\frac{5}{6}$'], correct=2,
      expl=['$6\\cdot 33=198$, therefore $200\\div 6=33$ with remainder $2$.',
            'The remainder becomes the fraction $\\frac{2}{6}$, which reduces to $\\frac{1}{3}$. The answer is $33\\,\\frac{1}{3}$.'])
    M.new_q('q-r26-t01-25', TOPIC, 'What are the quotient and the remainder when $200$ is divided by $6$?',
      ['quotient $33$, remainder $1$', 'quotient $33$, remainder $2$',
       'quotient $32$, remainder $8$', 'quotient $34$, remainder $2$'], 2,
      ['$6\\cdot 33=198$, and $200-198=2$. The quotient is $33$ and the remainder is $2$.',
       'Choice 3 is a trap: $6\\cdot 32+8=200$ is true, but $8$ is bigger than $6$. Another $6$ still fits. '
       'The remainder must be smaller than the number you divide by.',
       'Choice 4 is too big: $6\\cdot 34=204$, which is more than $200$.'])
    M.place_q('q-r26-t01-25', 'unit-t1-1', after='q-018')
    # Pass 2 (plan): restored drill questions, cleaned up
    S('q-003', stem='$84 - 36 = ?$',
      expl=['Ones: $6$ is bigger than $4$. Borrow a ten: $14-6=8$.',
            'Tens: the $8$ became $7$, and $7-3=4$. The answer is $48$. Check: $48+36=84$.'])
    S('q-004', stem='$95 + \\left(-38\\right) = ?$',
      expl=['Adding a negative number is the same as subtracting: $95+(-38)=95-38=57$.',
            'The trap $133$ comes from adding $38$ instead of subtracting it.'])
    S('q-033', stem='$63 - 27 = ?$',
      expl=['Ones: $3-7$ does not work. Borrow a ten: $13-7=6$.',
            'Tens: the $6$ became $5$, and $5-2=3$. The answer is $36$. Check: $36+27=63$.'])
    S('q-019', stem='$18 \\div \\left(8 - 2\\right) - \\left(-4\\right) \\cdot 3 = ?$',
      expl=['Parentheses first: $8-2=6$.',
            'Then divide and multiply: $18\\div 6=3$ and $(-4)\\cdot 3=-12$.',
            'Last, subtract: $3-(-12)=3+12=15$.'])
    S('q-020', stem='$12 \\div \\left(-4\\right) - \\left(-6\\right) \\cdot \\left(-2\\right) = ?$',
      expl=['Divide and multiply first: $12\\div(-4)=-3$ and $(-6)\\cdot(-2)=12$.',
            'Then subtract: $-3-12=-15$.'])
    S('q-021', expl=['Multiplication comes before addition: $6\\cdot 5=30$. Then $4+30=34$.',
                     'The trap $50$ comes from adding first: $(4+6)\\cdot 5=50$.'])
    S('q-022', stem='$6 \\cdot \\left(2 - 5\\right) \\div \\left(-3\\right) = ?$',
      expl=['Parentheses first: $2-5=-3$.',
            'Then left to right: $6\\cdot(-3)=-18$, and $-18\\div(-3)=6$.'])
    S('q-023', stem='$5 - \\left(9 - 6 \\div 3\\right) = ?$',
      expl=['Inside the parentheses, division comes first: $6\\div 3=2$. The bracket is $9-2=7$.',
            'Then $5-7=-2$.',
            'Or open the brackets. The minus in front flips every sign inside: $5-9+2=-2$.'])
    S('q-024', expl=['First bracket: $12+(-7)=5$. Second bracket: $(-6)-(-6)=-6+6=0$.',
                     'The product is $5\\cdot 0=0$, and $0-(-2)=0+2=2$.'])
    S('q-025', stem='$24 \\div \\left[2 \\cdot \\left(7 - 4\\right) \\div 3\\right] = ?$',
      expl=['Innermost parentheses first: $7-4=3$.',
            'Inside the square brackets, left to right: $2\\cdot 3=6$, then $6\\div 3=2$.',
            'Finally $24\\div 2=12$.'])
    S('q-026', stem='$\\left(-63\\right) \\div 9 = ?$',
      expl=['Different signs give a negative answer.', 'Sizes: $63\\div 9=7$. The answer is $-7$.'])
    S('q-027', expl=['Split $14$ into $10+4$: $10\\cdot 6=60$ and $4\\cdot 6=24$.', 'Then $14\\cdot 6=60+24=84$.'])
    S('q-028', stem='$91 \\div 7 = ?$',
      expl=['Split $91$ into $70+21$: $70\\div 7=10$ and $21\\div 7=3$.', 'Then $91\\div 7=10+3=13$.'])
    S('q-029', stem='$75 \\div 5 = ?$',
      expl=['Split $75$ into $50+25$: $50\\div 5=10$ and $25\\div 5=5$.', 'Then $75\\div 5=10+5=15$.'])
    S('q-030', stem='$3{,}366 \\div 11 = ?$',
      expl=['Split $3{,}366$ into $3{,}300+66$: $3{,}300\\div 11=300$ and $66\\div 11=6$.',
            'The answer is $306$. Check: $11\\cdot 306=3{,}300+66=3{,}366$.'])
    S('q-031', expl=['Ones: $3-6$ does not work. Borrow a ten: $13-6=7$.',
                     'Tens: the $9$ became $8$, and $8-4=4$. The answer is $47$. Check: $47+46=93$.'])
    S('q-032', expl=['Adding a negative is subtracting: $68+(-25)=68-25=43$.',
                     'The trap $93$ comes from adding $25$.'])
    S('q-034', expl=['Ones: $3+6=9$. Tens: $5+7=12$. Write $2$ and carry $1$.',
                     'Hundreds: $8+1=9$. Thousands: $4$. Total: $4{,}929$.'])
    S('q-035', expl=['Ones: borrow, $13-7=6$.',
                     'Tens: the $4$ became $3$. Borrow again: $13-4=9$.',
                     'Hundreds: the $7$ became $6$, and $6-3=3$. The answer is $396$. Check: $396+347=743$.'])
    S('q-036', expl=['The two-digit primes start $11$, $13$, $17$, $19$, ...',
                     'The two smallest are $11$ and $13$. Their product is $11\\cdot 13=110+33=143$.',
                     'The trap $121=11\\cdot 11$ uses the same prime twice. The question asks for two different primes.'])
    S('q-037', choices=['It is an odd number', 'It is a prime number', 'It is a natural number',
                        'It is a divisor of every integer'],
      expl=['$1$ is odd: true. $1$ is a natural number: true. $1$ divides every integer: true.',
            'But $1$ is not prime. A prime has exactly two different divisors, and $1$ has only one.',
            'The false statement is choice 2.'])
    S('q-038', expl=['Opposite numbers add up to zero. For example, $m=9$ and $n=-9$: $9+(-9)=0$.',
                     'This is true for every pair of opposites. The answer is $0$.'])
    S('q-039', expl=['The smallest two-digit prime is $11$.',
                     '$11=4\\cdot 2+3$. The remainder is $3$.'])
    S('q-040', expl=['Reciprocal numbers multiply to one. For example, $p=5$ and $q=\\frac{1}{5}$: $5\\cdot\\frac{1}{5}=1$.',
                     'This is true for every pair of reciprocals. The answer is $1$.'])

    E = 'alg-extra-unit-t1-1-%d'
    S(E % 1, stem='$297 + 68 = ?$', choices=['$465$', '$365$', '$355$', '$375$'],
      expl=['$297$ is $3$ less than $300$. Move $3$ from $68$ to $297$.',
            '$297+68=300+65=365$.'])
    S(E % 2, stem='$804 - 297 = ?$', choices=['$607$', '$507$', '$497$', '$517$'],
      expl=['Subtract a round $300$: $804-300=504$.',
            'We took away $3$ too many. Add $3$ back: $504+3=507$.'])
    S(E % 3, stem='$25 \\times 28 = ?$', choices=['$725$', '$675$', '$800$', '$700$'],
      expl=['$25$ is a quarter of $100$. Times $25$ is times $100$, divided by $4$.',
            '$28\\div 4=7$, and $7\\times 100=700$.'])
    S(E % 4, stem='$48 \\times 15 = ?$', choices=['$710$', '$770$', '$720$', '$730$'],
      expl=['Split $15=10+5$. $48\\times 10=480$.',
            'Times $5$ is half of times $10$: $480\\div 2=240$.',
            'Total: $480+240=720$.'])
    S(E % 5, stem='$72 \\div 12 = ?$', choices=['$5$', '$7$', '$12$', '$6$'],
      expl=['From the times table: $12\\cdot 6=72$. Therefore $72\\div 12=6$.',
            'Another way: $12=3\\cdot 4$. Divide in two steps: $72\\div 3=24$, then $24\\div 4=6$.'])
    S(E % 6, stem='$-3 - \\left(-11\\right) + 5 = ?$', choices=['$13$', '$-3$', '$3$', '$19$'],
      expl=['Two minus signs touching become a plus: $-3-(-11)=-3+11=8$.',
            'Then $8+5=13$.'])
    S(E % 7, stem='$3 \\cdot \\left(5 + 2\\right) - 3 \\cdot 5 = ?$', choices=['$3$', '$10$', '$15$', '$6$'],
      expl=['Parentheses first: $5+2=7$.',
            'Then the products: $3\\cdot 7=21$ and $3\\cdot 5=15$.',
            'Last, subtract: $21-15=6$.'])

    F = 'fast-practice-%d'
    S(F % 1, stem='$98 \\times 37 = ?$', choices=['$3{,}526$', '$3{,}726$', '$3{,}666$', '$3{,}626$'],
      expl=['$98$ is $2$ less than $100$. $100\\times 37=3{,}700$.',
            'That is two copies of $37$ too many: $3{,}700-74=3{,}626$.'])
    S(F % 2, stem='$32 \\times 125 = ?$', choices=['$3{,}600$', '$4{,}200$', '$4{,}000$', '$3{,}200$'],
      expl=['$8\\times 125=1{,}000$, and $32=4\\times 8$.',
            'Then $32\\times 125=4\\times 1{,}000=4{,}000$.'])
    S(F % 3, stem='$702 - 398 = ?$', choices=['$294$', '$314$', '$404$', '$304$'],
      expl=['Add $2$ to both numbers. The difference does not change.',
            '$702-398=704-400=304$.'])
    S(F % 4, stem='$39 \\times 41 = ?$', choices=['$1{,}591$', '$1{,}601$', '$1{,}619$', '$1{,}599$'],
      expl=['$39$ and $41$ sit evenly around $40$, with a gap of $1$.',
            'The product is $40^2-1^2=40\\times 40-1\\times 1=1{,}600-1=1{,}599$.'])
    S(F % 5, stem='$\\frac{54\\times 28}{21\\times 12} = ?$', choices=['$3$', '$9$', '$12$', '$6$'],
      expl=['Cancel before you multiply.',
            '$54$ and $12$ share $6$: $\\frac{54}{12}=\\frac{9}{2}$. $28$ and $21$ share $7$: $\\frac{28}{21}=\\frac{4}{3}$.',
            'The value is $\\frac{9\\times 4}{2\\times 3}=\\frac{36}{6}=6$.'])
    S(F % 6, stem='What is $16\\%$ of $75$?', choices=['$14$', '$16$', '$12$', '$10$'],
      expl=['$16\\%$ of $75$ is $\\frac{16\\times 75}{100}$. That is the same as $75\\%$ of $16$.',
            '$75\\%$ is three quarters. A quarter of $16$ is $4$, and three quarters is $3\\times 4=12$.'])
    S(F % 7, stem='$85^2 = ?$', choices=['$7{,}325$', '$7{,}225$', '$7{,}025$', '$7{,}125$'],
      expl=['$85^2$ means $85\\times 85$.',
            'Front part $8$, times the next number $9$: $8\\times 9=72$. Then write $25$ at the end: $7{,}225$.'])

    # ============================================================================================================
    # 2. Existing videos: wrong or unclear rules, ":" for division, "so" mid-sentence, squares/percent before taught
    # ============================================================================================================
    # --- The Language of Algebra ---
    item_text(M, NUM, 5, 'Nonnegative: $x\\ge 0$', 'Nonnegative: $x\\ge 0$ · Nonzero: $x\\ne 0$')
    sc = script_of(M, NUM, 5)
    ins_after(sc, 'Nonnegative means zero OR positive. That little line lets zero in.',
              ['And nonzero means any number except zero. It can be positive or negative.',
               'So nonzero is NOT the same as positive.'])
    M.set_slide(NUM, 5, script=sc)
    item_text(M, NUM, 8, '$10:3$', '$10\\div 3$')
    item_text(M, NUM, 8, '$12:5$', '$12\\div 5$')
    fix_lines(M, NUM, 8, [('10 : 3', '10 ÷ 3'), ('12 : 5', '12 ÷ 5')])
    sc = script_of(M, NUM, 9)
    rep(sc, 'An even number is an integer that divides by two with no remainder. Every even number can be written as two k.',
        'An even number is an integer that divides by two with no remainder. Every even number can be written as two times k — where k is an integer.')
    rep(sc, 'Odd is two k plus one — one more than an even number.',
        'Odd is two k plus one — one more than an even number. Again, k is an integer.')
    M.set_slide(NUM, 9, script=sc)
    sc = script_of(M, NUM, 12)
    rep(sc, 'Whole numbers too. Eight is eight over one, so its reciprocal is one eighth.',
        'Whole numbers too. Eight is eight over one. Its reciprocal is one eighth.')
    M.set_slide(NUM, 12, script=sc)
    sc = script_of(M, NUM, 13)
    ins_after(sc, 'Most of this you already knew. The surprises — zero is even, one isn\'t prime — are exactly where the traps are.',
              ['Here\'s proof. Three of these facts are printed in the general comments at the start of every quantitative section.',
               'Zero is neither positive nor negative. Zero is an even number. One is not a prime number.',
               'The exam prints them because it tests them.'])
    rep(sc, 'Five questions next. Don\'t rush them. Miss one? Go find the word you skipped.',
        'Next: a short video on the English words the exam uses — sum, product, digit, and more. Then your first questions.')
    rep(sc, 'Next lessons: the real basics — addition, subtraction, multiplication, division.',
        'After that: must, could, cannot — the way the exam really asks about these words. Then the real basics: addition, subtraction, multiplication, division.')
    M.set_slide(NUM, 13, script=sc)

    # --- Addition & Subtraction ---
    sc = script_of(M, ADD, 1)
    ins_after(sc, 'But when a longer calculation does show up, you want a method that never fails.',
              ['Already fast and sure with this? Try the questions after this lesson first. All correct? Jump ahead to the traps in the recap — and to Fast Calculation.'])
    M.set_slide(ADD, 1, script=sc)
    sc = script_of(M, ADD, 3)
    rep(sc, 'Two of the same sign side by side — minus, minus — become a plus.',
        'Two of the same sign touching — minus, minus, with no number between them — become a plus.')
    rep(sc, 'So the rule: same signs side by side — write plus. Different signs — write minus.',
        'So the rule for two signs touching: same signs — write plus. Different signs — write minus.')
    M.set_slide(ADD, 3, script=sc)
    sc = script_of(M, ADD, 4)
    ins_after(sc, 'Here we\'ve got two minus signs — and the answer is firmly negative.',
              ['Look closely: these two minus signs don\'t touch. One belongs to the eight, one to the six.',
               'The "minus, minus becomes plus" rule is only for two signs touching — like six minus negative four.'])
    M.set_slide(ADD, 4, script=sc)
    sc = script_of(M, ADD, 8)
    rep(sc, 'But that\'s two too many — so give two back.', 'But that\'s two too many. Give two back.')
    rep(sc, 'Subtract too much, and the result\'s too small — so you fix it by adding.',
        'Subtract too much, and the result\'s too small. You fix it by adding.')
    M.set_slide(ADD, 8, script=sc)
    sc = script_of(M, ADD, 9)
    rep(sc, 'Same signs side by side — plus. Different signs — minus.',
        'Two signs touching: same signs — plus. Different signs — minus.')
    rep(sc, 'Five questions next — no video between them. Take your time, then check the written solutions.',
        'Questions next — no video between them. Take your time, then check the written solutions.')
    M.set_slide(ADD, 9, script=sc)

    # --- Multiplication & Division ---
    fix_lines(M, MUL, 2, [('"× and :"', '"× and ÷"')])
    item_text(M, MUL, 3, '$0:9$', '$0\\div 9$')
    item_text(M, MUL, 3, '$9:0$', '$9\\div 0$')
    fix_lines(M, MUL, 3, [('0 : 9', '0 ÷ 9'), ('9 : 0', '9 ÷ 0'), ('24 : 6', '24 ÷ 6')])
    sc = script_of(M, MUL, 3)
    sc.append('Some books write division with a colon — twenty-four colon six. It means the same thing.')
    sc.append('In this course we write the division sign, or a fraction bar.')
    M.set_slide(MUL, 3, script=sc)
    sc = script_of(M, MUL, 5)
    rep(sc, 'Remember when we called it "times"? Seventeen times eight means seventeen eights.',
        'Seventeen times eight means seventeen eights.')
    M.set_slide(MUL, 5, script=sc)
    item_text(M, MUL, 7, '$576:8$', '$576\\div 8$')
    fix_lines(M, MUL, 7, [('560 : 8 + 16 : 8', '560 ÷ 8 + 16 ÷ 8'),
                          ('Seven eights are fifty-six — so seventy eights are five hundred sixty.',
                           'Seven eights are fifty-six. That means seventy eights are five hundred sixty.')])
    sc = script_of(M, MUL, 9)
    rep(sc, 'Five questions next. Written or mental — whatever\'s clearest. Just make sure you could explain any shortcut you use.',
        'Questions next. Written or mental — whatever\'s clearest. Just make sure you could explain any shortcut you use.')
    M.set_slide(MUL, 9, script=sc)

    # --- Order of Operations ---
    item_text(M, ORD, 3, '$24:6\\cdot2$', '$24\\div 6\\cdot 2$')
    fix_lines(M, ORD, 3, [('24 : 6', '24 ÷ 6'), ('24 : 12', '24 ÷ 12')])
    fix_lines(M, ORD, 5, [('12 : 6', '12 ÷ 6')])
    sc = script_of(M, ORD, 5)
    sc.append(D('Below, write "(20 + 8)/4 = 20/4 + 8/4 = 5 + 2 = 7 ✓"'))
    sc.append('The top may be split: twenty plus eight, over four, is five plus two. Seven — the same as twenty-eight over four.')
    M.set_slide(ORD, 5, script=sc)
    item_text(M, ORD, 6, 'Grouped $\\to$ powers $\\to$ $\\times\\ :$ $\\to$ $+\\ -$',
              'Grouped $\\to$ powers $\\to$ $\\times\\ \\div$ $\\to$ $+\\ -$')
    sc = script_of(M, ORD, 6)
    rep(sc, 'Five questions next, then mixed practice on everything in this unit.',
        'Questions next, then mixed practice on everything in this unit.')
    M.set_slide(ORD, 6, script=sc)

    # --- Fast Calculation ---
    fix_lines(M, FAST, 6, [('44 : 4', '44 ÷ 4'), ('24 : 8', '24 ÷ 8')])
    sc = script_of(M, FAST, 10)
    ins_after(sc, 'When two numbers sit evenly around a centre, the product is the centre squared minus the gap squared.',
              ['Squared means times itself. Fifty squared is fifty times fifty.'])
    M.set_slide(FAST, 10, script=sc)
    sc = script_of(M, FAST, 11)
    ins_after(sc, 'A number ending in five, squared.', ['Sixty-five squared means sixty-five times sixty-five.'])
    M.set_slide(FAST, 11, script=sc)
    sc = script_of(M, FAST, 12)
    ins_after(sc, 'Percentages get their own chapter later — but here\'s a gem for now.',
              ['Percent means out of a hundred. Twenty-four percent of seventy-five is twenty-four times seventy-five, over a hundred.'])
    rep(sc, 'Both are the same product over a hundred, so you\'re allowed to swap.',
        'Both are the same product over a hundred. That\'s why you\'re allowed to swap.')
    M.set_slide(FAST, 12, script=sc)
    sc = script_of(M, FAST, 14)
    rep(sc, 'Seven questions next. Write down the route you chose — not just the answer.',
        'Questions next. Write down the route you chose — not just the answer.')
    M.set_slide(FAST, 14, script=sc)

    # ============================================================================================================
    # 3. New slides inside existing lessons (insert from the back so slide numbers stay valid)
    # ============================================================================================================
    # Fast Calculation: x9 and x11 (the card listed it, q-014 used it, no slide taught it)
    M.insert_slides(FAST, 4, [dict(title='×9 and ×11', mode='concept', active=3, script=[
        A('47 × 11 appears', T('$47\\times11$', size=64, gap=150)),
        'Two splits worth knowing by heart: times eleven and times nine.',
        'Eleven is ten plus one. Times eleven is times ten, plus one more copy.',
        D('Write "= 470 + 47 = 517"'),
        'Four seventy plus forty-seven: five seventeen.',
        A('47 × 9 appears', T('$47\\times9$', size=64)),
        'Nine is ten minus one. Times ten, then take one copy away.',
        D('Write "= 470 − 47 = 423"'),
        'Four seventy minus forty-seven: four twenty-three.',
        'Check the size: times nine must be a little less than times ten. Four twenty-three is just under four seventy. Good.'])])
    shift_active(M, FAST, 6, 1)
    sb = list(M.video(FAST)['hybrid']['sidebar']); sb.insert(3, '×9 and ×11'); M.set_sidebar(FAST, sb)

    # Order of Operations: a minus before brackets
    M.insert_slides(ORD, 4, [dict(title='Minus before brackets', mode='concept', active=3, script=[
        A('5 − (9 − 2) appears', T('$5-(9-2)$', size=64, gap=150)),
        'One more bracket rule. A minus sign right before brackets.',
        D('Under it write "= 5 − 7 = −2"'),
        'The safe way: bracket first. Nine minus two, seven. Five minus seven: negative two.',
        'Now the other way — open the brackets. The minus in front hits every number inside.',
        D('Write "= 5 − 9 + 2 = −2"'),
        'Minus nine. And minus negative two becomes plus two. Negative two again.',
        A('10 − (3 + 4 − 1) = 10 − 3 − 4 + 1 appears', T('$10-(3+4-1)=10-3-4+1$', size=56)),
        'Every sign inside flips. Plus becomes minus. Minus becomes plus.',
        D('Circle the three flipped signs'),
        'Ten minus three minus four plus one: four. Check with the bracket: three plus four minus one is six. Ten minus six: four.',
        'The classic mistake: flipping only the first number. Flip them all.'])])
    shift_active(M, ORD, 6, 1)
    sb = list(M.video(ORD)['hybrid']['sidebar']); sb.insert(3, 'Minus before brackets'); M.set_sidebar(ORD, sb)
    sc = script_of(M, ORD, 7)
    sc.insert(next(k for k, x in enumerate(sc) if _txt(x).startswith('Questions next')), A('\'Minus before brackets: flip every sign inside\' appears',
                             T('Minus before brackets? Flip every sign inside.', size=50)))
    M.set_slide(ORD, 7, script=sc)

    # Multiplication & Division: last digit + estimate to knock out choices
    M.insert_slides(MUL, 8, [dict(title='Last digit', mode='concept', active=7, script=[
        A('8 · 47 = ? appears', T('$8\\cdot 47=?$', size=64, gap=80)),
        'A multiple-choice trick. Before you multiply — look at the choices.',
        A('The four choices appear: 336, 376, 382, 476', T('$336\\qquad 376\\qquad 382\\qquad 476$', size=56, gap=80)),
        'The last digit of a product comes only from the last digits.',
        D('Write "8 · 7 = 56 → ends in 6"'),
        'Eight times seven is fifty-six. The answer ends in six.',
        D('Cross out 382'),
        'Three eighty-two ends in two. Gone — without multiplying.',
        'Now estimate. Eight times fifty is four hundred. Forty-seven is three less than fifty.',
        D('Write "8 · 50 = 400 → 400 − 3 · 8 = 376"'),
        'The answer is three eights — twenty-four — below four hundred.',
        D('Cross out 476 and 336'),
        'Four seventy-six is too big. Three thirty-six is too small. Three seventy-six.',
        'Last digit first, then a quick estimate. On the exam, that often leaves just one choice.'])])
    shift_active(M, MUL, 10, 1)
    sb = list(M.video(MUL)['hybrid']['sidebar']); sb.insert(7, 'Last digit'); M.set_sidebar(MUL, sb)

    # ============================================================================================================
    # 4. New lesson: Exam Words (vocabulary) — section 1, right after the Number words card
    # ============================================================================================================
    EW = 'r26-t01-exam-words'
    M.new_video(EW, TOPIC, 'Exam Words',
                ['Four results', 'Multiples & divisors', 'Digits', 'Distinct · at least', 'Consecutive even/odd', 'Recap'], [
        dict(mode='title', title='Exam Words', script=[
            'Before the first questions — a few English words.',
            'The exam uses them all the time. Read one word wrong, and you answer a different question.',
            'Let\'s learn them once, properly.']),
        dict(title='Four results', active=0, script=[
            A('\'Sum: 12 + 3 = 15\' appears', T('Sum: $12+3=15$')),
            'Sum — the result of adding. The sum of twelve and three is fifteen.',
            A('\'Difference: 12 − 3 = 9\' appears', T('Difference: $12-3=9$')),
            'Difference — the result of subtracting. Nine.',
            A('\'Product: 12 · 3 = 36\' appears', T('Product: $12\\cdot 3=36$')),
            'Product — the result of multiplying. Thirty-six.',
            A('\'Quotient: 12 ÷ 3 = 4\' appears', T('Quotient: $12\\div 3=4$')),
            'Quotient — the result of dividing. Four.',
            D('Circle "Product" and "Quotient"'),
            'These two get mixed up the most. Product: times. Quotient: divided by.']),
        dict(title='Multiples & divisors', active=1, script=[
            A('\'Multiples of 6\' appears', T('Multiples of $6$: $\\ 6,\\ 12,\\ 18,\\ 24,\\ \\ldots$')),
            'A multiple of six is six times an integer. Six, twelve, eighteen, and on.',
            'Zero is a multiple too — six times zero. And so are negative six, negative twelve.',
            A('\'Divisors of 12\' appears', T('Divisors of $12$: $\\ 1,\\ 2,\\ 3,\\ 4,\\ 6,\\ 12$')),
            'A divisor of twelve divides it with no remainder. Another name for a divisor: a factor.',
            A('\'12 is divisible by 3\' appears', T('$12$ is divisible by $3$')),
            'Twelve is divisible by three — three goes into twelve exactly. Four times.',
            D('Draw an arrow from 3 to 12 and write "3 is a divisor of 12 · 12 is a multiple of 3"'),
            'Same fact, two directions. Three is a divisor of twelve. Twelve is a multiple of three.']),
        dict(title='Digits', active=2, script=[
            A('\'Digits: 0, 1, 2, …, 9\' appears', T('Digits: $\\ 0,\\ 1,\\ 2,\\ \\ldots,\\ 9$')),
            'Digits are the ten symbols we write numbers with. Zero to nine.',
            A('\'507 — a three-digit number\' appears', T('$507$ — a three-digit number')),
            'Five hundred seven is a number. It is written with three digits: five, zero, seven.',
            D('Label the digits: "hundreds 5, tens 0, ones 7"'),
            'Its tens digit is zero. Zero counts as a digit.',
            A('\'Sum of the digits: 5 + 0 + 7 = 12\' appears', T('Sum of the digits: $5+0+7=12$')),
            'The sum of its digits is twelve. Not five hundred seven.',
            'One more rule: a three-digit number can\'t start with zero. Zero seventy-five is just seventy-five — a two-digit number.']),
        dict(title='Distinct · at least', active=3, script=[
            A('\'Distinct = different\' appears', T('Distinct $=$ different: $\\ 3,\\ 5,\\ 8$ ✓ $\\qquad 3,\\ 3,\\ 8$ ✗')),
            'Distinct means different from each other. Three distinct numbers — no repeats.',
            A('\'At least 3\' appears', T('At least $3$: $\\ x\\ge 3$')),
            'At least three: three or more. Three itself is allowed.',
            A('\'At most 3\' appears', T('At most $3$: $\\ x\\le 3$')),
            'At most three: three or less. Again, three is allowed.',
            D('Circle the little lines under ≥ and ≤'),
            'Both include the number itself. "More than three" and "less than three" do not.']),
        dict(title='Consecutive even / odd', active=4, script=[
            A('\'Consecutive even: 4, 6, 8\' appears', T('Consecutive even: $\\ 4,\\ 6,\\ 8$', size=50, gap=90)),
            'Consecutive even numbers: even numbers in a row. Four, six, eight.',
            D('Draw a "+2" hop between each pair'),
            'Each one is two more than the one before — not one.',
            A('\'Consecutive odd: −3, −1, 1\' appears', T('Consecutive odd: $\\ {-3},\\ {-1},\\ 1$', size=50, gap=90)),
            D('Draw a "+2" hop between each pair'),
            'Consecutive odd numbers work the same way — steps of two. Negatives count too.',
            'Plain consecutive numbers go up by one. Add the word even or odd, and the step becomes two.']),
        dict(title='Recap', active=5, script=[
            'Let\'s lock it in.',
            A('\'Product: × · Quotient: ÷\' appears', T('Product: $\\times$ · Quotient: $\\div$')),
            A('\'3 is a divisor of 12 · 12 is a multiple of 3\' appears', T('$3$ is a divisor of $12$ · $12$ is a multiple of $3$')),
            A('\'Digit ≠ number · distinct = different\' appears', T('Digit $\\ne$ number · distinct $=$ different')),
            A('\'Consecutive even / odd: steps of 2\' appears', T('Consecutive even / odd: steps of $2$')),
            'All of it is on the memory card.',
            'Questions next. Read every word — each one changes the answer.'])],
        'intro-numbers', after='mem-definitions')
    M.new_card('mem-r26-t01-exam-words', TOPIC, 'intro-numbers', dict(
        title='Exam words', intro='The English words the exam uses for results and for kinds of numbers.',
        tables=[dict(title='', head=['Word', 'Means', 'Example'], rows=[
            ['Sum', 'the result of adding', '$12+3=15$'],
            ['Difference', 'the result of subtracting', '$12-3=9$'],
            ['Product', 'the result of multiplying', '$12\\cdot 3=36$'],
            ['Quotient', 'the result of dividing', '$12\\div 3=4$'],
            ['Multiple of $n$', '$n$ times an integer', 'multiples of $6$: $0,\\ 6,\\ 12,\\ 18,\\ \\ldots$'],
            ['Divisor (factor) of $n$', 'divides $n$ with no remainder', 'divisors of $12$: $1,\\ 2,\\ 3,\\ 4,\\ 6,\\ 12$'],
            ['Divisible by', 'divides with no remainder', '$12$ is divisible by $3$'],
            ['Digit', 'one of the symbols $0$ to $9$', '$507$ has the digits $5$, $0$, $7$'],
            ['Distinct', 'different from each other', '$3,\\ 5,\\ 8$ are distinct'],
            ['At least / at most', '$\\ge$ / $\\le$ (the number itself is allowed)', 'at least $3$: $x\\ge 3$'],
            ['Consecutive even / odd', 'even (odd) numbers in a row: steps of $2$', '$4,\\ 6,\\ 8$ · $-3,\\ -1,\\ 1$']])],
        tips=['$3$ is a divisor of $12$ means the same as $12$ is a multiple of $3$.',
              'The sum of the digits of $507$ is $5+0+7=12$, not $507$.',
              'A three-digit number cannot start with $0$.']), after=EW)

    # ============================================================================================================
    # 5. New questions — section 1 (number words)
    # ============================================================================================================
    N = M.new_q
    N(qid(1), TOPIC, 'What is the sum of the digits of the smallest three-digit number whose digits are all distinct?',
      ['$1$', '$3$', '$6$', '$102$'], 2,
      ['The smallest three-digit number is $100$, but its digits are not distinct: it has two zeros.',
       'Build the number from the left. The first digit cannot be $0$: use $1$. Then the smallest digits not used yet: $0$, then $2$. The number is $102$.',
       'The sum of its digits is $1+0+2=3$.',
       'Traps: $1$ comes from $100$ (digits not distinct). $6$ comes from $123$ (forgetting that $0$ is a digit). $102$ is the number, not the sum of its digits.'])
    guided(M, qid(1), 'intro-numbers', ['Read the words', 'Build the number'],
           ['Three exam words in one sentence: digits, distinct, sum.'], [
        ('Read the words', [
            'The smallest three-digit number whose digits are all distinct. Then the sum of its digits.',
            D('Underline "digits", "distinct" and "sum"'),
            'Digits are the symbols zero to nine. Distinct means all different.',
            'The smallest three-digit number is one hundred. But it has two zeros — not distinct.',
            D('Write "100 ✗"')]),
        ('Build the number', [
            'Build it from the left. The first digit can\'t be zero. The smallest it can be is one.',
            D('Write "1 _ _"'),
            'Next, the smallest digit not used yet: zero.',
            D('Write "1 0 _"'),
            'Then the smallest one left: two.',
            D('Write "102"'),
            'Now the question: the SUM of its digits. Not the number.',
            D('Write "1 + 0 + 2 = 3"'),
            'Three.',
            D('Circle choice 2'),
            'Choice two. Choice four is the trap — that\'s the number itself, not the sum of its digits.'])],
           before='q-036')
    N(qid(2), TOPIC, 'Which of the following numbers is a multiple of $6$ and also a divisor of $60$?',
      ['$3$', '$12$', '$18$', '$120$'], 2,
      ['A multiple of $6$ is $6$ times an integer: $6$, $12$, $18$, ... A divisor of $60$ divides $60$ with no remainder.',
       '$12=6\\cdot 2$ is a multiple of $6$, and $60\\div 12=5$. Both conditions hold.',
       '$3$ is a divisor of $6$, not a multiple of it. $18$ is a multiple of $6$, but $60\\div 18$ leaves a remainder of $6$. '
       '$120$ is a multiple of $60$, not a divisor of it.'])
    N(qid(3), TOPIC, 'The sum of $12$ and $8$ is divided by the difference between $12$ and $8$. What is the result?',
      ['$\\frac{1}{5}$', '$5$', '$24$', '$80$'], 2,
      ['Sum: $12+8=20$. Difference: $12-8=4$.',
       'The quotient: $20\\div 4=5$.',
       'Traps: $\\frac{1}{5}$ divides the other way ($4\\div 20$). $24$ is the product divided by the difference ($96\\div 4$). '
       '$80$ is the sum times the difference.'])
    N(qid(4), TOPIC, '$a$, $b$ and $c$ are three consecutive odd numbers, and $a<b<c$. What is $c-a$?',
      ['$2$', '$3$', '$4$', '$6$'], 3,
      ['Consecutive odd numbers go up by $2$: for example $7$, $9$, $11$.',
       'Then $c-a=11-7=4$. In general, $b=a+2$ and $c=a+4$. That gives $c-a=4$.',
       'The trap $2$ comes from steps of $1$ ($7$, $8$, $9$). But $8$ is not odd.'])
    for q in (qid(2), qid(3), qid(4)): M.place_q(q, 'intro-numbers')

    # ============================================================================================================
    # 6. New lesson: Must, Could, Cannot (plug-in numbers) — end of section 1
    # ============================================================================================================
    MC = 'r26-t01-must-could'
    M.new_video(MC, TOPIC, 'Must, Could, Cannot',
                ['Three questions', 'One example', 'Test numbers', 'Could it?', 'Exam strategy', 'Recap'], [
        dict(mode='title', title='Must, Could, Cannot', script=[
            'Now the way the exam really asks about number words.',
            'Not "what is an integer?" — but: "x is a negative integer. Which of the following must be true?"',
            'Three little words decide the whole question: must, could, cannot.']),
        dict(title='Three questions', active=0, script=[
            A('\'Must be true — for every allowed number\' appears', T('Must be true — for every allowed number')),
            'Must be true: it works for every number the question allows. No exceptions.',
            A('\'Could be true — for at least one\' appears', T('Could be true — for at least one')),
            'Could be true: one allowed example is enough.',
            A('\'Cannot be true — for none\' appears', T('Cannot be true — for none')),
            'Cannot be true: no allowed number makes it work.',
            D('Write "must / could / cannot" in the corner and circle one'),
            'Before you touch the choices — circle the word. It\'s easy to flip under pressure.']),
        dict(title='One example', active=1, script=[
            A('\'n is an integer. Must 2n > n?\' appears', T('$n$ is an integer. Must $2n>n$?', size=50, gap=70)),
            'Here\'s one. n is an integer. Must two n be bigger than n?',
            A('\'n = 5: 10 > 5 ✓\' appears', T('$n=5$: $\\ 10>5$ ✓')),
            'Try five. Ten is bigger than five. It works.',
            'Does that prove it? No. For must, one example that works proves nothing.',
            A('\'n = 0: 0 > 0 ✗\' appears', T('$n=0$: $\\ 0>0$ ✗')),
            'Try zero. Zero is not bigger than zero. It fails.',
            D('Cross out "Must"'),
            'One example that fails — and must is dead.',
            'But could two n be bigger than n? Yes — five showed it. One good example proves could.']),
        dict(title='Test numbers', active=2, script=[
            A('\'Test: 0, 1, −1, ½, 10\' appears', T('Test: $\\ 0,\\ \\ 1,\\ \\ {-1},\\ \\ \\frac{1}{2},\\ \\ 10$', size=54, gap=70)),
            'Which numbers do you try? Not random ones. The troublemakers.',
            'Zero — it\'s neither positive nor negative, and anything times zero is zero.',
            'One — it\'s its own reciprocal. Negative one — negatives flip signs.',
            'One half — numbers between zero and one get smaller when you multiply them by themselves.',
            'And a big number, like ten.',
            A('\'x positive. Must x · x > x?\' appears', T('$x$ is positive. Must $x\\cdot x>x$?', size=50)),
            D('Write "x = 10: 100 > 10 ✓   x = ½: ¼ > ½ ✗"'),
            'x is positive. Must x times x be bigger than x? Ten says yes. One half says no — half of a half is a quarter. Dead.',
            A('\'Only numbers the question allows!\' appears', T('Only numbers the question allows!', size=46)),
            'One rule: test only numbers the question allows. If x is a positive integer, zero, negative one and one half are off the list.']),
        dict(title='Could it?', active=3, script=[
            A('\'p is prime. Could p + 1 be prime?\' appears', T('$p$ is prime. Could $p+1$ be prime?', size=50, gap=70)),
            'Now a could question. p is prime. Could p plus one also be prime?',
            'Most people say no: a prime is odd, and odd plus one is even.',
            A('\'p = 2: 2 + 1 = 3 ✓\' appears', T('$p=2$: $\\ 2+1=3$ ✓')),
            'But two is prime — the only even prime. Two plus one is three. Prime.',
            'One example is enough. It could be prime.',
            A('\'Could 2 · p be prime? Never.\' appears', T('Could $2\\cdot p$ be prime? Never.')),
            'Could two times p be prime? Two times p is at least four, and it divides by two.',
            'Even and bigger than two — never prime. That one is a cannot.']),
        dict(title='Exam strategy', active=4, script=[
            'On the exam, exactly one choice is right. Use that.',
            A('\'Must? Break the wrong choices.\' appears', T('Must? Break the wrong choices.')),
            'Must be true? For each choice, look for one example that breaks it. The choice that survives is the answer.',
            A('\'Could? One example that works.\' appears', T('Could? One example that works.')),
            'Could be true? Find one allowed example that works. Done.',
            A('\'Cannot? Examples that work knock choices out.\' appears', T('Cannot? Examples that work knock choices out.')),
            'Cannot be true? Every choice you can make happen is out. The last one standing is the answer.',
            'And if you have time — ask why the survivor always works. That\'s how you catch a mistake.']),
        dict(title='Recap', active=5, script=[
            'Let\'s lock it in.',
            A('\'Circle the word: must · could · cannot\' appears', T('Circle the word: must · could · cannot')),
            A('\'Test 0, 1, −1, ½, 10 — only allowed numbers\' appears', T('Test $0,\\ 1,\\ {-1},\\ \\frac{1}{2},\\ 10$ — only allowed numbers')),
            A('\'One failing example kills must\' appears', T('One failing example kills "must".')),
            A('\'One working example proves could\' appears', T('One working example proves "could".')),
            'Two guided questions next, then practice.',
            'Later in the course, a whole chapter builds on this. Now you have the basics.'])],
        'intro-numbers')
    M.new_card('mem-r26-t01-must-could', TOPIC, 'intro-numbers', dict(
        title='Must, could, cannot', intro='Number-word questions ask which statement must, could or cannot be true.',
        tables=[dict(title='', head=['Word', 'Means', 'How to answer'], rows=[
                    ['Must be true', 'true for every allowed number', 'find one example that breaks each wrong choice'],
                    ['Could be true', 'true for at least one allowed number', 'find one example that works'],
                    ['Cannot be true', 'true for no allowed number', 'examples that work knock out the wrong choices']]),
                dict(title='Numbers to test', head=['Number', 'Why'], rows=[
                    ['$0$', 'neither positive nor negative; anything times $0$ is $0$'],
                    ['$1$ and $-1$', '$1$ is its own reciprocal; negatives flip signs'],
                    ['$\\frac{1}{2}$', 'between $0$ and $1$: $\\frac{1}{2}\\cdot\\frac{1}{2}=\\frac{1}{4}$ is smaller'],
                    ['a big number, like $10$', 'shows what happens far from $0$'],
                    ['$2$', 'the only even prime']])],
        tips=['Circle the word (must / could / cannot) before you read the choices.',
              'Test only numbers the question allows: "positive integer" rules out $0$, $-1$ and $\\frac{1}{2}$.',
              'Examples can kill a "must" choice, but only a reason proves one. When you have time, ask why the survivor always works.']),
        after=MC)

    N(qid(5), TOPIC, '$x$ is a negative integer and $y$ is a positive number. Which of the following must be true?',
      ['$x\\cdot y$ is an integer', '$x+y<0$', '$x-y<0$', '$x\\cdot y<-1$'], 3,
      ['Plug in allowed numbers and try to break each choice. $x$ is a negative integer. $y$ can be any positive number, even a fraction.',
       'Choice 1: $x=-1$ and $y=\\frac{1}{2}$ give $x\\cdot y=-\\frac{1}{2}$, not an integer. Out.',
       'Choice 2: $x=-1$ and $y=5$ give $x+y=4$, not negative. Out.',
       'Choice 4: $x=-1$ and $y=\\frac{1}{2}$ give $x\\cdot y=-\\frac{1}{2}$, which is bigger than $-1$. Out.',
       'Choice 3 is always true: start at a negative number and subtract a positive one. You move further left of zero. For example, $-1-5=-6$.'])
    guided(M, qid(5), 'intro-numbers', ['Break the choices', 'The survivor'],
           ['Our first must-be-true question. The plan: try to break every choice.'], [
        ('Break the choices', [
            'x is a negative integer. y is any positive number — it can be a fraction.',
            D('Under the question write "x: −1, −2, …   y: ½, 1, 5, …"'),
            'Must be true means true for every allowed pair. One example that fails — and the choice is out.',
            D('Next to choice 1 write "x = −1, y = ½ → −½ ✗"'),
            'Choice one. Negative one times one half is negative one half. Not an integer. Out.',
            D('Next to choice 2 write "x = −1, y = 5 → 4 ✗"'),
            'Choice two. Negative one plus five is four. Not negative. Out.',
            D('Next to choice 4 write "x = −1, y = ½ → −½ ✗"'),
            'Choice four. Negative one half is bigger than negative one. Out.']),
        ('The survivor', [
            'Only choice three is left. Let\'s see why it always works.',
            D('Next to choice 3 write "(−) − (+) → further left"'),
            'Start at a negative number. Subtract a positive one. You move further left of zero.',
            'Negative one minus five: negative six. Negative two minus one half: negative two and a half. Always negative.',
            D('Circle choice 3'),
            'Choice three. Look at the numbers we used: negative one, one half, five. Small, simple — and chosen to break things.'])])
    N(qid(6), TOPIC, '$p$ is a prime number and $q$ is an even number. Which of the following cannot be true?',
      ['$p+q$ is even', '$p\\cdot q$ is odd', '$p\\cdot q=0$', '$p-q<0$'], 2,
      ['For "cannot", one example that works knocks a choice out.',
       'Choice 1: $p=2$ and $q=4$ give $p+q=6$, even. Possible. Out.',
       'Choice 3: $q=0$ is allowed, because $0$ is an even number. Then $p\\cdot q=0$. Possible. Out.',
       'Choice 4: $p=3$ and $q=4$ give $p-q=-1$, less than $0$. Possible. Out.',
       'Choice 2 is impossible: $q$ is even, $q=2k$ for an integer $k$. Then $p\\cdot q=2\\cdot(p\\cdot k)$ is even, never odd.'])
    guided(M, qid(6), 'intro-numbers', ['Find examples', 'Why it cannot'],
           ['Now the word is cannot. That flips the job.'], [
        ('Find examples', [
            'Cannot be true. One example where a choice IS true — and that choice is out.',
            'p is prime: two, three, five, and on. q is even — and remember, zero and negatives count.',
            D('Next to choice 1 write "p = 2, q = 4 → 6 even ✓"'),
            'Choice one. Two plus four is six, even. It can happen. Out.',
            D('Next to choice 3 write "q = 0 → p · q = 0 ✓"'),
            'Choice three. Zero is even. Any prime times zero is zero. It can happen. Out.',
            D('Next to choice 4 write "p = 3, q = 4 → −1 ✓"'),
            'Choice four. Three minus four is negative one. Out.']),
        ('Why it cannot', [
            'Choice two is left. Can a prime times an even number be odd?',
            D('Write "q = 2k → p · q = 2 · (p · k)"'),
            'An even number is two times an integer. Multiply it by any integer — the factor of two is still there.',
            'The product is always even. Never odd.',
            D('Circle choice 2'),
            'Choice two. The trap was zero: forget that zero is even, and choice three looks impossible.'])])
    N(qid(7), TOPIC, '$n$ is a positive integer. Which of the following must be an even number?',
      ['$n+1$', '$2n+1$', '$n\\cdot(n+1)$', '$3n$'], 3,
      ['Try $n=1$ and $n=2$ on each choice.',
       'Choice 1: $n=2$ gives $3$, odd. Out. Choice 2: $2n$ is even, and one more is odd, always. Out. Choice 4: $n=1$ gives $3$, odd. Out.',
       'Choice 3: $n$ and $n+1$ are consecutive integers. Of two consecutive integers, one is even. A product with an even factor is even.',
       'Check: $n=1$ gives $1\\cdot 2=2$, and $n=2$ gives $2\\cdot 3=6$.'])
    N(qid(8), TOPIC, '$x$ is a positive number. Which of the following could be true?',
      ['$x+1<x$', '$x\\cdot x<x$', '$x-x>0$', '$2x<x$'], 2,
      ['Test $x=\\frac{1}{2}$: $x\\cdot x=\\frac{1}{2}\\cdot\\frac{1}{2}$ is half of a half, $\\frac{1}{4}$. And $\\frac{1}{4}<\\frac{1}{2}$. Choice 2 could be true.',
       'Choice 1: adding $1$ always makes a number bigger. Never. Choice 3: $x-x=0$, and $0$ is not greater than $0$. Never. '
       'Choice 4: $2x=x+x$, and adding a positive $x$ makes it bigger. Never.',
       'With $x=10$, choice 2 fails ($100>10$). That is why you test $\\frac{1}{2}$ too, not only whole numbers.'])
    N(qid(9), TOPIC, '$m$ and $n$ are opposite numbers, and $m\\ne 0$. Which of the following must be true?',
      ['$m>n$', '$m\\cdot n<0$', '$m\\cdot n=-1$', '$m-n=0$'], 2,
      ['Opposites: $n=-m$. Try $m=3$, $n=-3$ and also $m=-3$, $n=3$.',
       'Choice 1: $m=-3$, $n=3$ gives $m<n$. Out.',
       'Choice 3: $m=3$ gives $3\\cdot(-3)=-9$, not $-1$. (Product $1$ is the rule for reciprocals, not opposites.) Out.',
       'Choice 4: $m=3$ gives $3-(-3)=6$. Out.',
       'Choice 2: $m$ and $n$ are not zero and have different signs. Different signs give a negative product, every time.'])
    N(qid(10), TOPIC, '$p$ and $q$ are reciprocal numbers. Which of the following cannot be true?',
      ['$p=q$', '$p<0$', '$p=0$', '$p>q$'], 3,
      ['Reciprocals multiply to $1$: $p\\cdot q=1$.',
       'Choice 1: $p=q=1$, and $1\\cdot 1=1$. Possible. Out. Choice 2: $p=-2$, $q=-\\frac{1}{2}$. Possible. Out. '
       'Choice 4: $p=2$, $q=\\frac{1}{2}$. Possible. Out.',
       'Choice 3: if $p=0$, then $p\\cdot q=0$ for every $q$, never $1$. Zero has no reciprocal.'])
    for q in (qid(7), qid(8), qid(9), qid(10)): M.place_q(q, 'intro-numbers')

    # ============================================================================================================
    # 7. New questions — multiplication (created before section 8 so question numbers follow the course order) (last digit + estimate)
    # ============================================================================================================
    N(qid(15), TOPIC, '$23\\cdot 47=?$', ['$881$', '$1{,}081$', '$1{,}084$', '$1{,}381$'], 2,
      ['Method 1 · last digit and estimate. The last digit comes only from $3\\cdot 7=21$. The answer ends in $1$: choice 3 is out.',
       'Estimate: $23\\cdot 47$ is more than $20\\cdot 47=940$. Choice 1 is too small. '
       'It is less than $25\\cdot 50=1{,}250$. Choice 4 is too big. Only choice 2 is left.',
       'Method 2 · split: $23\\cdot 47=20\\cdot 47+3\\cdot 47=940+141=1{,}081$.'])
    guided(M, qid(15), 'intro-mult', ['Last digit', 'Estimate'],
           ['We could just multiply. But look at the choices first.'], [
        ('Last digit', [
            'The last digit of a product depends only on the last digits.',
            D('Write "3 · 7 = 21 → ends in 1"'),
            'Three times seven is twenty-one. The answer ends in one.',
            D('Cross out choice 3'),
            'One thousand eighty-four ends in four. Out.']),
        ('Estimate', [
            'Three choices end in one. Now estimate.',
            D('Write "20 · 47 = 940"'),
            'Twenty times forty-seven is nine hundred forty. The real answer is bigger than that.',
            D('Cross out choice 1'),
            'Eight eighty-one is too small. Out.',
            D('Write "25 · 50 = 1,250"'),
            'And twenty-three times forty-seven is less than twenty-five times fifty — twelve hundred fifty.',
            D('Cross out choice 4'),
            'Thirteen eighty-one is too big. Out.',
            D('Circle choice 2'),
            'Choice two. Check by splitting: nine forty plus three forty-sevens, one forty-one. One thousand eighty-one.'])])
    N(qid(16), TOPIC, '$38\\cdot 12=?$', ['$446$', '$456$', '$458$', '$546$'], 2,
      ['Split: $38\\cdot 12=38\\cdot 10+38\\cdot 2=380+76=456$.',
       'Check with the last digit: $8\\cdot 2=16$. The answer ends in $6$, and $458$ is out. '
       '$38\\cdot 12$ is less than $40\\cdot 12=480$, and $546$ is out.'])
    M.place_q(qid(16), 'intro-mult')

    # ============================================================================================================
    # 8. New questions — order of operations (minus before brackets, fraction bar)
    # ============================================================================================================
    N(qid(11), TOPIC, '$20-(8-3+6)-(4-9)=?$', ['$-4$', '$2$', '$4$', '$14$'], 4,
      ['Method 1 · brackets first: $8-3+6=11$ and $4-9=-5$. Then $20-11-(-5)=20-11+5=14$.',
       'Method 2 · open the brackets. A minus before brackets flips every sign inside: $20-8+3-6-4+9=14$.',
       'Traps: $2$ comes from flipping only the first number in each bracket ($20-8-3+6-4-9$). '
       '$-4$ comes from forgetting to flip the $-9$. $4$ comes from $20-11-5$: the two minus signs in $-(-5)$ were not turned into a plus.'])
    N(qid(12), TOPIC, '$15-(6-10)=?$', ['$-1$', '$11$', '$19$', '$31$'], 3,
      ['Brackets first: $6-10=-4$. Then $15-(-4)=15+4=19$.',
       'Or open the brackets and flip both signs: $15-6+10=19$.',
       'The trap $-1$ comes from $15-6-10$: only the $6$ was flipped.'])
    N(qid(13), TOPIC, '$\\frac{36}{3+6}=?$', ['$4$', '$9$', '$12$', '$18$'], 1,
      ['The fraction bar groups the whole bottom. Bottom first: $3+6=9$.',
       'Then $36\\div 9=4$.',
       'The trap $18$ comes from splitting the denominator: $\\frac{36}{3}+\\frac{36}{6}=12+6=18$. That is not allowed.'])
    N(qid(14), TOPIC, 'Which of the following is equal to $\\frac{20+8}{4}$?',
      ['$\\frac{20}{4}+8$', '$\\frac{20}{4}+\\frac{8}{4}$', '$20+\\frac{8}{4}$', '$\\frac{20}{2}+\\frac{8}{2}$'], 2,
      ['A numerator may be split: every part of the top is divided by the whole bottom.',
       '$\\frac{20+8}{4}=\\frac{20}{4}+\\frac{8}{4}=5+2=7$. Check: $\\frac{28}{4}=7$.',
       'The other choices give $5+8=13$, $20+2=22$ and $10+4=14$.'])
    M.place_q(qid(13), 'order', after='q-021')
    M.place_q(qid(14), 'order', after=qid(13))
    guided(M, qid(11), 'order', ['Brackets first', 'Open the brackets'],
           ['A minus in front of brackets. Two ways — and one trap.'], [
        ('Brackets first', [
            'Way one: work out each bracket first.',
            D('Under the first bracket write "8 − 3 + 6 = 11"'),
            'Eight minus three is five. Plus six: eleven.',
            D('Under the second bracket write "4 − 9 = −5"'),
            'Four minus nine: negative five.',
            D('Write "20 − 11 − (−5) = 20 − 11 + 5 = 14"'),
            'Twenty minus eleven, minus negative five. Two minus signs touching — plus. Fourteen.']),
        ('Open the brackets', [
            'Way two: open the brackets. A minus in front flips every sign inside — not just the first one.',
            D('Write "20 − 8 + 3 − 6 − 4 + 9"'),
            'Minus eight, plus three, minus six. Then minus four, plus nine.',
            D('Write "= 14"'),
            'Twenty minus eight is twelve. Plus three, fifteen. Minus six, nine. Minus four, five. Plus nine: fourteen.',
            D('Circle choice 4'),
            'Choice four. Flip only the first sign in each bracket, and you get two — choice two is waiting for you.'])],
           after='q-023')
    M.place_q(qid(12), 'order', after='solve-' + qid(11))

    # ============================================================================================================
    # 9. Mixed practice: exam-level number-word, bracket and fraction-bar questions
    # ============================================================================================================
    N(qid(17), TOPIC, '$a$ and $b$ are two consecutive integers. Which of the following must be true?',
      ['$a+b$ is odd', '$a\\cdot b>0$', '$a+b>0$', '$a$ or $b$ is a prime number'], 1,
      ['Test numbers that include zero and negatives.',
       'Choice 2: $a=0$, $b=1$ gives $a\\cdot b=0$, not positive. Out. Choice 3: $a=-2$, $b=-1$ gives $a+b=-3$. Out. '
       'Choice 4: $a=8$, $b=9$. Neither is prime. Out.',
       'Choice 1: of two consecutive integers, one is even and one is odd. Even plus odd is odd. Check: $0+1=1$, $-2+(-1)=-3$, $8+9=17$.'])
    N(qid(18), TOPIC, 'Given: $-1<x<0$.\nWhich of the following is the largest?',
      ['$x$', '$x\\cdot x$', '$-x$', '$\\frac{1}{x}$'], 3,
      ['Plug in a number in the range: $x=-\\frac{1}{2}$.',
       '$x=-\\frac{1}{2}$. $x\\cdot x=\\frac{1}{4}$ (negative times negative is positive, and half of a half is a quarter). '
       '$-x=\\frac{1}{2}$. $\\frac{1}{x}=-2$ (the reciprocal keeps the sign).',
       'The largest is $-x=\\frac{1}{2}$.',
       'Check another value, $x=-\\frac{1}{10}$: $x\\cdot x=\\frac{1}{100}$ and $-x=\\frac{1}{10}$. $-x$ is still the largest.'])
    N(qid(19), TOPIC, '$k$ is a positive integer. Which of the following cannot be a prime number?',
      ['$k+2$', '$2k$', '$6k$', '$2k+1$'], 3,
      ['Choice 1: $k=1$ gives $3$, a prime. Out. Choice 2: $k=1$ gives $2$, a prime (the only even prime). Out. '
       'Choice 4: $k=1$ gives $3$, a prime. Out.',
       'Choice 3: $6k=2\\cdot 3\\cdot k$ is at least $6$ and divides by $2$ and by $3$. A prime has only two divisors, $1$ and itself. Therefore $6k$ is never prime.',
       'The trap: many students cross out choice 2 as "always even". But $2\\cdot 1=2$ is prime.'])
    N(qid(20), TOPIC, 'The product of two distinct positive integers is $36$. Which of the following cannot be their sum?',
      ['$13$', '$12$', '$20$', '$37$'], 2,
      ['List the pairs of positive integers with product $36$: $1\\cdot 36$, $2\\cdot 18$, $3\\cdot 12$, $4\\cdot 9$, $6\\cdot 6$.',
       'The two numbers must be distinct (different). The pair $6\\cdot 6$ is not allowed.',
       'Sums: $1+36=37$, $2+18=20$, $3+12=15$, $4+9=13$. The sum $12=6+6$ is not possible.'])
    N(qid(21), TOPIC, '$\\frac{5\\cdot 8-4}{12-3\\cdot 2}=?$', ['$2$', '$6$', '$12$', '$36$'], 2,
      ['The fraction bar groups the top and the bottom.',
       'Top: $5\\cdot 8-4=40-4=36$. Bottom: multiply first, $3\\cdot 2=6$, then $12-6=6$.',
       'The value is $36\\div 6=6$.',
       'The trap $2$ comes from working the bottom left to right: $(12-3)\\cdot 2=18$, and $36\\div 18=2$.'])
    N(qid(22), TOPIC, '$-(4-7)-(-2-5)=?$', ['$-10$', '$-4$', '$4$', '$10$'], 4,
      ['Brackets first: $4-7=-3$ and $-2-5=-7$.',
       'Then $-(-3)-(-7)=3+7=10$.',
       'Or open the brackets, flipping every sign inside: $-4+7+2+5=10$.'])
    U = 'unit-t1-1'
    for n in range(17, 23): M.place_q(qid(n), U)

    # questions that used tricks taught later (Pass 2: q-003, q-004 and q-033 are no longer removed)
    for q in ('q-014', E % 3, E % 4): move_q(M, q, 'fast-practice')

    M.practice_order(U, ['q-001', 'q-003', 'q-006', 'q-002', 'q-004', 'q-005', E % 1, E % 2, 'q-007', 'q-008', 'q-009', 'q-010', E % 6,
                         'q-011', E % 5, 'q-015', 'q-016', 'q-012', 'q-013', 'q-017', qid(25), E % 7, 'q-019', 'q-020',
                         qid(22), qid(21), qid(17), qid(20), qid(19), qid(18)])
    # Pass 2 (plan): the original q-018 (200 ÷ 6 = 33 1/3) needs fractions -> Topic 2 practice (ordered by t02.py)
    M.move('q-018', 'unit-t2-1')

    # ============================================================================================================
    # 10. Fast-calculation practice: x9 question, exam-level estimate, easy -> hard
    # ============================================================================================================
    N(qid(23), TOPIC, '$86\\times 9=?$', ['$764$', '$774$', '$784$', '$854$'], 2,
      ['Times $9$ is times $10$ minus one copy.',
       '$86\\times 10=860$, and $860-86=774$.',
       'The trap $854$ comes from subtracting $6$ instead of $86$.'])
    N(qid(24), TOPIC, 'Which of the following is closest to $\\frac{398\\times 51}{99}$?',
      ['$150$', '$200$', '$250$', '$400$'], 2,
      ['Round each number: $398\\approx 400$, $51\\approx 50$, $99\\approx 100$.',
       '$\\frac{400\\times 50}{100}=4\\times 50=200$.',
       'Each number moved only a little. The value stays close to $200$ (the exact value is about $205$), far from $150$ and $250$.'])
    for n in (23, 24): M.place_q(qid(n), 'fast-practice')
    M.practice_order('fast-practice', [F % 3, F % 2, F % 1, qid(23), 'q-014', E % 3, E % 4, F % 6, F % 4, F % 7, F % 5, qid(24)])

    # ============================================================================================================
    # 11. Memory cards
    # ============================================================================================================
    c = M.card('mem-definitions')
    rows = c['tables'][0]['rows']
    for r in rows:
        if r[0] == 'Remainder': r[2] = '$10\\div 3 \\to$ remainder $1$'
        if r[0] == 'Even / odd': r[1] = 'integers only: $2k$ / $2k+1$ ($k$ an integer)'
        if r[0] == 'Consecutive': r[1] = 'integers that differ by exactly 1 (consecutive even / odd: by 2)'
    k = [r[0] for r in rows].index('Nonnegative')
    rows.insert(k + 1, ['Nonzero', 'any number except $0$ (positive or negative)', '$-3,\\ \\frac{1}{2},\\ 7$'])
    c['tips'].append('The exam prints three of these in the general comments of every quantitative section: '
                     '"0" is neither a positive nor a negative number. "0" is an even number. "1" is not a prime number.')

    c = M.card('mem-times')
    for r in c['tables'][0]['rows']:
        if r[0] == 'Two signs side by side': r[0] = 'Two signs touching'
    c['tips'].append('Last digit check: the last digit of a product comes only from the last digits. $8\\cdot 47$ ends in $6$, because $8\\cdot 7=56$.')
    c['tips'].append('Estimate to knock out choices that are too big or too small: $8\\cdot 47$ is a little less than $8\\cdot 50=400$.')

    c = M.card('order')
    c['tips'] = ['$24\\div 6\\cdot 2=4\\cdot 2=8$, not $24\\div 12$.',
                 'A minus before brackets flips every sign inside: $5-(9-2)=5-9+2=-2$.',
                 'You may split a numerator, never a denominator: $\\frac{20+8}{4}=\\frac{20}{4}+\\frac{8}{4}$, but $\\frac{12}{2+4}\\ne\\frac{12}{2}+\\frac{12}{4}$.']

    c = M.card('mem-fast')
    for r in c['tables'][0]['rows']:
        if r[0] == 'Times 5 / 25 / 125': r[1] = '$\\times10\\div2$ / $\\times100\\div4$ / $\\times1000\\div8$'
        if r[0] == 'Times 9 / 11': r[2] = '$47\\times11=517$ · $47\\times9=423$'
    c['tips'] = ['$65^2$ means $65\\times 65$ (a number times itself).',
                 'Percent means out of a hundred: $24\\%$ of $75$ is $\\frac{24\\times 75}{100}$.']

    # ============================================================================================================
    # 12. Pass 2: summary lessons right before each practice section
    # ============================================================================================================
    summaries(M)
    dedupe_examples(M)   # 2026-10-04: runs last


def _last_item(M, section):
    return [f['ref'] for f in M.D['flow'] if f['section'] == section][-1]


def _b(label, tex, size=44):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summaries(M):
    # ---- 1. everything taught in sections 1-4, right before "Mixed arithmetic practice"
    sb = ['Number words', 'Opposites · reciprocals', 'Exam words', 'Must · could · cannot', 'Adding signed numbers',
          'Multiplying signs', 'Calculating by hand', 'Order of operations', 'Before you practice']
    M.new_video('r26-t01-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            'A quick summary before the mixed practice.',
            'Everything important from the first four lessons — in about three minutes.']),
        dict(title='Number words', active=0, script=[
            _b('Integer: negative, zero or positive', 'Integer: negative, $0$ or positive'),
            '"Integer" lets in negatives and zero. Don\'t read it as "positive integer."',
            _b('Positive ≠ integer · nonzero ≠ positive', 'Positive $\\ne$ integer · Nonzero $\\ne$ positive'),
            'Positive can be a fraction. Nonzero can be negative.',
            _b('0: integer · even · neither + nor −', '$0$: integer · even · neither $+$ nor $-$'),
            _b('1 is not prime · 2 is the only even prime', '$1$ is not prime · $2$ is the only even prime'),
            'One is not prime. Two is the only even prime.',
            'And even or odd? Only integers. One half is neither.']),
        dict(title='Opposites · reciprocals', active=1, script=[
            _b('Opposites: sum 0 · Reciprocals: product 1', 'Opposites: sum $0$ · Reciprocals: product $1$'),
            'Opposites add up to zero. Reciprocals multiply to one.',
            _b('−x is the opposite of x', 'The opposite of $x$ is $-x$: $\\ x=-7 \\to -x=7$'),
            'Minus x is not "a negative number." If x is negative, minus x is positive.',
            _b('17 ÷ 5 → remainder 2', '$17\\div 5$: $\\ 5\\cdot 3=15$, remainder $2$'),
            'And a remainder is always smaller than the number you divide by.']),
        dict(title='Exam words', active=2, script=[
            _b('Sum + · Difference − · Product × · Quotient ÷', 'Sum $+$ · Difference $-$ · Product $\\times$ · Quotient $\\div$'),
            'Product is times. Quotient is divided by. Don\'t mix them up.',
            _b('4 is a divisor of 28 · 28 is a multiple of 4', '$4$ is a divisor of $28$ · $28$ is a multiple of $4$'),
            _b('Distinct = different · at least 5: x ≥ 5', 'Distinct $=$ different · At least $5$: $x\\ge 5$'),
            'At least and at most include the number itself.',
            _b('Consecutive even / odd: steps of 2', 'Consecutive even / odd: steps of $2$'),
            'A digit is one symbol. The sum of the digits of six hundred nine is fifteen.']),
        dict(title='Must · could · cannot', active=3, script=[
            _b('Circle the word: must · could · cannot', 'Circle the word: must · could · cannot'),
            'First, circle the word. It decides everything.',
            _b('One failing example kills "must"', 'One failing example kills "must".'),
            _b('One working example proves "could"', 'One working example proves "could".'),
            _b('Test 0, 1, −1, 1/2, 10', 'Test $0,\\ 1,\\ {-1},\\ \\frac{1}{2},\\ 10$ — only allowed numbers'),
            'Test the troublemakers. But only numbers the question allows.']),
        dict(title='Adding signed numbers', active=4, script=[
            _b('−(−a) = +a and +(−a) = −a', 'Two signs touching: $-(-a)=+a \\qquad +(-a)=-a$'),
            'Two signs touching: same signs — plus. Different signs — minus.',
            _b('6 + (−15) = 6 − 15 = −9', '$6+(-15)=6-15=-9$'),
            'Different signs? Take the difference. The bigger one decides the sign.',
            _b('−9 − 4 = −13', '$-9-4=-13$'),
            'These two minus signs don\'t touch. Both push left: minus thirteen.',
            'Name the operation first. Then use its sign rule.']),
        dict(title='Multiplying signs', active=5, script=[
            _b('× and ÷: same signs +, different signs −', '$\\times$ and $\\div$: same signs $\\to +$ · different signs $\\to -$'),
            'Decide the sign first. Then do the numbers.',
            _b('Even number of negatives +, odd −', 'Even number of negatives $\\to +$ · odd $\\to -$'),
            _b('a · 0 = 0 · 7 ÷ 0 is undefined', '$a\\cdot 0=0 \\qquad 0\\div 7=0 \\qquad 7\\div 0$ undefined'),
            'Anything times zero is zero. Dividing by zero means nothing.']),
        dict(title='Calculating by hand', active=6, script=[
            _b('19 · 6 = 60 + 54 = 114', 'Split a factor: $19\\cdot 6=60+54=114$'),
            'Splitting is usually the fastest way.',
            _b('595 ÷ 7 = 560 ÷ 7 + 35 ÷ 7 = 85', '$595\\div 7=\\frac{560}{7}+\\frac{35}{7}=80+5=85$'),
            'Split the number you divide. Never the divisor.',
            _b('6 · 38: ends in 8, a bit less than 240', '$6\\cdot 38$: ends in $8$ · a little less than $6\\cdot 40=240$'),
            'On the exam, look at the choices. Last digit first, then a quick estimate.',
            'Columns? Line them up, track every carry and borrow — and estimate to check.']),
        dict(title='Order of operations', active=7, script=[
            _b('Grouped → powers → × ÷ → + −', 'Grouped $\\to$ powers $\\to$ $\\times\\ \\div$ $\\to$ $+\\ -$'),
            _b('36 ÷ 4 · 3 = 9 · 3 = 27', 'Same level? Left to right: $36\\div 4\\cdot 3=9\\cdot 3=27$'),
            'Same level — left to right. Not thirty-six over twelve.',
            _b('4 − (10 − 3) = 4 − 10 + 3 = −3', 'Minus before brackets: $4-(10-3)=4-10+3=-3$'),
            'A minus before brackets flips every sign inside.',
            _b('Split a numerator, never a denominator', 'A fraction bar is brackets. Split the top — never the bottom.'),
            'The fraction bar groups the whole top and the whole bottom. Work them out first.']),
        dict(title='Before you practice', active=8, script=[
            'Before you practice, ask yourself these questions.',
            _b('Which word? integer · positive · distinct · must', 'Which word? integer · positive · distinct · must'),
            'What exactly does each word allow — and rule out?',
            _b('Which operation? Then which sign rule?', 'Which operation? Then which sign rule?'),
            _b('What goes first?', 'What goes first? Brackets, $\\times\\ \\div$, left to right'),
            _b('Does the size make sense?', 'Does the size of my answer make sense?'),
            'And the traps: two minus signs that don\'t touch, thirty-six divided by four times three, and a minus before brackets.',
            'Take your time. Good luck.'])],
        'order', after=_last_item(M, 'order'))

    # ---- 2. fast calculation, right before "Fast-calculation practice"
    sb = ['Sums and differences', 'Split a factor', 'Double, halve, ×25', 'Near a round number', 'Pairs and cancelling',
          'Special products', 'Percent and estimates', 'Before you practice']
    M.new_video('r26-t01-summary-fast', TOPIC, 'Summary: Fast Calculation', sb, [
        dict(mode='title', title='Summary', script=[
            'A quick summary of the fast-calculation toolkit.',
            'Every trick finds an easier calculation with exactly the same answer.']),
        dict(title='Sums and differences', active=0, script=[
            _b('397 + 85 = 400 + 82 = 482', 'Sum: move an amount across: $397+85=400+82=482$'),
            'A sum stays the same when you move an amount from one part to the other.',
            _b('802 − 395 = 807 − 400 = 407', 'Difference: shift both: $802-395=807-400=407$'),
            'A difference stays the same when you add the same amount to both numbers.',
            'Don\'t mix them up. That\'s the trap.']),
        dict(title='Split a factor', active=1, script=[
            _b('28 × 15 = 280 + 140 = 420', '$28\\times 15=28\\times(10+5)=280+140=420$'),
            'Split one factor into easy pieces.',
            _b('63 × 11 = 630 + 63 = 693', '$\\times 11$: $\\ 63\\times 11=630+63=693$'),
            _b('63 × 9 = 630 − 63 = 567', '$\\times 9$: $\\ 63\\times 9=630-63=567$'),
            'Times eleven: times ten plus one copy. Times nine: times ten minus one copy.']),
        dict(title='Double, halve, ×25', active=2, script=[
            _b('14 × 45 = 7 × 90 = 630', 'Double and halve: $14\\times 45=7\\times 90=630$'),
            'Halve one factor, double the other. The product doesn\'t move.',
            'Fourteen halves to seven. Forty-five doubles to ninety. Seven nineties: six thirty.',
            _b('×25 = ×100 ÷ 4 · ×125 = ×1000 ÷ 8', '$\\times 25=\\times 100\\div 4 \\qquad \\times 125=\\times 1000\\div 8$'),
            _b('36 × 25 = 9 × 100 = 900', '$36\\times 25=9\\times 100=900$'),
            'Divide first, and the numbers stay small.']),
        dict(title='Near a round number', active=3, script=[
            _b('98 × 36 = 3,600 − 72 = 3,528', '$98\\times 36=(100-2)\\times 36=3{,}600-72=3{,}528$'),
            'Round to a hundred, then correct.',
            'A hundred thirty-sixes is thirty-six hundred. That is two thirty-sixes too many — seventy-two.',
            'Rounded up? The easy product is too big — subtract. Rounded down? Add.']),
        dict(title='Pairs and cancelling', active=4, script=[
            _b('4 × 53 × 25 = 100 × 53', 'Friendly pairs: $4\\times 53\\times 25=100\\times 53=5{,}300$'),
            'Look for pairs that make a round number: four and twenty-five, eight and one twenty-five, two and fifty, five and twenty.',
            _b('Products over products: cancel first', 'Products over products: cancel first: $\\frac{45\\times 28}{14\\times 15}=6$'),
            'Cancel only when the top and the bottom are products. A plus on top? No cancelling.']),
        dict(title='Special products', active=5, script=[
            _b('37 × 43 = 40² − 3² = 1,591', 'Around a centre: $37\\times 43=40^2-3^2=1{,}591$'),
            'Evenly around a centre: the centre squared minus the gap squared. The gaps must be equal.',
            _b('35² = 1,225', 'Square ending in $5$: $\\ 35^2$: $\\ 3\\times 4=12 \\to 1{,}225$'),
            'Front digit times the next number, then twenty-five on the end. Only for squares.']),
        dict(title='Percent and estimates', active=6, script=[
            _b('44% of 25 = 25% of 44 = 11', '$44\\%$ of $25=25\\%$ of $44=11$'),
            'You may swap the two numbers. Pick the easier one.',
            _b('61 × 29 ≈ 1,800', 'Estimate: $61\\times 29\\approx 60\\times 30=1{,}800$'),
            'Use exactly as much precision as the choices need. One choice left? Stop.']),
        dict(title='Before you practice', active=7, script=[
            'Before you practice, ask yourself these questions.',
            _b('Is there an easier calculation with the same answer?', 'Is there an easier calculation with the same answer?'),
            _b('Can I say why the trick works?', 'Can I say why the trick works?'),
            _b('Sum: move across · difference: shift both', 'Sum: move across · Difference: shift both'),
            _b('How precise do the choices need me to be?', 'How precise do the choices need me to be?'),
            'The traps: shifting a sum the wrong way, cancelling across a plus, and using the centre trick with unequal gaps.',
            'Nothing looks easier? A clean written calculation is a great answer too.'])],
        'fast-calculation', after=_last_item(M, 'fast-calculation'))


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
    # q-r26-t01-14 was the lesson example (20 + 8)/4 of "order-of-operations" (RECORDED) -> new numbers in the question.
    M.set_q('q-r26-t01-14', stem=r'Which of the following is equal to $\frac{24+8}{4}$?',
            choices=[r'$\frac{24}{4}+8$', r'$\frac{24}{4}+\frac{8}{4}$', r'$24+\frac{8}{4}$', r'$\frac{24}{2}+\frac{8}{2}$'], correct=2,
            expl=['A numerator may be split: every part of the top is divided by the whole bottom.',
                  r'$\frac{24+8}{4}=\frac{24}{4}+\frac{8}{4}=6+2=8$. Check: $\frac{32}{4}=8$.',
                  r'The other choices give $6+8=14$, $24+2=26$ and $12+4=16$.'])


# ---------------- 2026-10-06: new exam methods (found by solving real exams) ----------------
def add_methods(M):
    # "number" (no "integer") = any number, fractions included. Card only: topic 1 is recorded.
    rows = M.card('mem-definitions')['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0] == 'Integer')
    rows.insert(k + 1, ['"Number" (the word "integer" is missing)',
                        'any number, fractions included; only "integer" means a whole number',
                        'numbers $x$ with $4<x<6$ and $3x$ whole: $3x=13,\\ 14,\\ 15,\\ 16,\\ 17$, so five numbers '
                        '($4\\frac13,\\ 4\\frac23,\\ 5,\\ 5\\frac13,\\ 5\\frac23$), not just $5$'])


_apply_before_add_methods = apply


def apply(M):
    _apply_before_add_methods(M)
    add_methods(M)   # 2026-10-06: runs last
