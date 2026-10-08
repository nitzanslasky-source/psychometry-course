"""Topic 28 - Counting possibilities. Course review 2026-09 fixes.
See t28_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q
from math_api import VIS, rich_plain, _word

TOPIC = 28
LEARN, ADV, PRAC = 'wp28-learn', 'wp28-advanced', 'wp28-practice'
# New guided questions (all in the advanced section) get 18-23; renumber_guided() keeps course order.
SB_LEARN = ['Question %d' % n for n in range(1, 13)]
# 2026-10-01: + the factorial-algebra guided question (number 24, right after the Factorial Expressions lesson)
SB_ADV = ['Question %d' % n for n in range(13, 25)]
INK, TEAL = '#203344', '#087f83'


# ------------------------------------------------------------------------------------------------ helpers
def _sol(M, qid, adv, intro, slides, after=None):
    """Guided-question solution video in the style of solve-wp28-g124..g144."""
    n = M.next_question_number(TOPIC)
    sb = SB_ADV if adv else SB_LEARN
    group = 'Advanced Counting' if adv else 'Counting Questions'
    act = sb.index('Question %d' % n)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % _word(n)] + intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=act, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, group, sb, beats, M.section_of(qid), kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = 51 if adv else 45
    v['hybrid']['title'] = group
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _draw(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _say(M, vid, n, old, new):
    """Replace (part of) a spoken line; new=None deletes the line."""
    def fn(lines):
        out = []
        for l in lines:
            if 'say' in l and old in l['say']:
                if new is None:
                    continue
                l['say'] = l['say'].replace(old, new)
            out.append(l)
        return out
    M.edit_lines(vid, n, fn)


def _square():
    cells = [('A', 220, 70), ('B', 320, 70), ('C', 220, 170), ('D', 320, 170)]
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="A square split into '
         'four cells A, B, C and D"><title>A square split into four cells A, B, C and D</title>']
    for t, x, y in cells:
        s.append('<rect x="%d" y="%d" width="100" height="100" fill="%s" stroke="%s" stroke-width="2.5"/>'
                 % (x, y, 'white', INK))
        s.append('<text x="%d" y="%d" text-anchor="middle" dominant-baseline="middle" fill="%s" '
                 'font-family="DejaVu Sans,Arial,sans-serif" font-size="24">%s</text>' % (x + 50, y + 51, INK, t))
    s.append('</svg>')
    return ''.join(s)


def apply(M):
    S = M.set_q
    # =====================================================================================================
    # 1. Existing questions: TeX, numbers in every solution, no ":" for division, no mid-sentence "so"
    # =====================================================================================================
    S('wp28-g124', expl=[
        'List in order, smallest first. Hundreds digit $2$: $246$, $248$, $268$. Hundreds digit $4$: $468$. '
        'Hundreds digit $6$ or $8$: there are not enough bigger digits left.',
        'Total: $4$ numbers.',
        'Check: each number uses $3$ of the $4$ digits, in increasing order. So we only choose the $1$ digit that is '
        'left out: $4$ ways.'])
    S('wp28-g125', expl=[
        'Two stages: a filling ($4$ options) and a drink ($6$ options).',
        'Multiply: $4\\times6=24$ meals.',
        'Adding, $4+6=10$, counts menu items, not meals.'])
    S('wp28-g126', stem='A code has two digits, each from 0 to 9. The sum of the two digits must be 12. '
                        'How many codes are possible?', expl=[
        'First digit: it must be at least $3$ (otherwise the second digit would have to be more than $9$). '
        'So $3, 4, \\ldots, 9$: $7$ options.',
        'Second digit: it must be $12$ minus the first digit. It is forced: $1$ option.',
        '$7\\times1=7$ codes: $39$, $48$, $57$, $66$, $75$, $84$, $93$.'])
    S('wp28-g128', expl=[
        'Symbols may repeat, so the pool stays the same: $6$ options for each position.',
        '$6\\times6\\times6=216$. Codes like AAA and ABA are included.'])
    S('wp28-g129', expl=[
        'No symbol may repeat, so the pool shrinks: $6$, then $5$, then $4$.',
        '$6\\times5\\times4=120$.',
        'Compare with the previous question: the same symbols, but $6\\times6\\times6$ became $6\\times5\\times4$.'])
    S('wp28-g130', expl=[
        '$6$ photographs in a row: $6!=6\\times5\\times4\\times3\\times2\\times1=720$.',
        'The last place has only $1$ photograph left: it is forced.'])
    S('wp28-g132', expl=[
        'Count in order: the route leaves from one of $5$ islands and goes to one of the $4$ others: $5\\times4=20$.',
        'A route from A to B is the same route as from B to A, so every route was counted twice: $\\frac{20}{2}=10$.',
        'Check: $4+3+2+1=10$.'])
    S('wp28-g133', expl=[
        'From each vertex: $7-3=4$ diagonals (not to itself and not to its two neighbors).',
        'Every diagonal is counted from both of its ends: $\\frac{7\\times4}{2}=14$.',
        'Or: all lines between the vertices, $\\frac{7\\times6}{2}=21$, minus the $7$ sides: $21-7=14$.'])
    S('wp28-g135', expl=[
        'Case 1, cocoa: the snack must be a biscuit. $1\\times1=1$.',
        'Case 2, another drink: $4\\times4=16$.',
        'The cases do not overlap, so add them: $1+16=17$.',
        'Check: all pairs, $5\\times4=20$, minus the forbidden pairs (cocoa with the $3$ other snacks): $20-3=17$.'])
    S('wp28-g136', expl=[
        'All outcomes: $6\\times6=36$.',
        'Sum $5$: $(1,4)$, $(2,3)$, $(3,2)$, $(4,1)$. That is $4$ outcomes. The colors make $(1,4)$ and $(4,1)$ '
        'different.',
        'All minus forbidden: $36-4=32$.'])
    S('wp28-g138', expl=[
        'Choose Maya\'s $4$ children as if order mattered: $8\\times7\\times6\\times5$.',
        'The order inside the group does not matter, so divide by $4!=4\\times3\\times2\\times1$.',
        'Cancel: $\\frac{8\\times7\\times6\\times5}{4\\times3\\times2\\times1}=7\\times2\\times5=70$ '
        '($8$ cancels with $4\\times2$, and $6\\div3=2$).',
        'The other $4$ children go to Alex: $1$ option. The teachers have names, so we do not divide by $2$ again.'])
    S('wp28-g139', expl=[
        'Choosing $7$ of $8$ is the same as choosing the $1$ person who stays out: $8$ ways.',
        'The long way gives the same: $\\frac{8\\times7\\times6\\times5\\times4\\times3\\times2}{7!}=8$.'])
    S('wp28-g140', expl=[
        'The ratio is $\\frac{7!}{5!}=\\frac{7\\times6\\times5!}{5!}=7\\times6=42$.',
        'There is no need to calculate $7!=5040$ and $5!=120$ first.'])
    S('wp28-g141', expl=[
        'Most restricted position first: the hundreds digit. It is not $0$ and not more than $7$: $1$ to $7$, '
        'so $7$ options.',
        'Units digit: forced ($7$ minus the hundreds digit): $1$ option.',
        'Tens digit: free, $0$ to $9$: $10$ options.',
        '$7\\times10\\times1=70$.',
        'Check: the (hundreds, units) pairs are $(1,6)$, $(2,5)$, $(3,4)$, $(4,3)$, $(5,2)$, $(6,1)$, $(7,0)$. '
        'That is $7$ pairs, each with $10$ possible middle digits.'])
    S('wp28-g142', stem='The digits 3, 4, 7 and 8 go once each into a square: A and B on top, C and D below.\n'
                        'B is even.\n$C\\times D$ is even.\n'
                        'How many arrangements are possible?', expl=[
        'Most restricted first. B is even: $4$ or $8$, so $2$ options.',
        '$C\\times D$ is even only if C or D is even. The only other even digit must go to the bottom row, '
        'so A must be odd: $3$ or $7$, so $2$ options.',
        'The last two digits go into C and D in $2\\times1=2$ orders.',
        '$2\\times2\\times2\\times1=8$.',
        'Check: with B even there are $2\\times3!=12$ arrangements. The bad ones have the other even digit in A: '
        '$2\\times1\\times2=4$. $12-4=8$.'])
    S('wp28-g143', expl=[
        'With $n$ players, each pair plays once: $\\frac{n(n-1)}{2}=45$.',
        'Multiply by $2$: $n(n-1)=90$. Two consecutive numbers with product $90$: $10\\times9$. Therefore $n=10$.',
        'Check the other choices: $\\frac{12\\times11}{2}=66$, $\\frac{9\\times8}{2}=36$, $\\frac{8\\times7}{2}=28$.'])
    S('wp28-g144', expl=[
        'Choose the $1$ student who stays out: $7$ options.',
        'The other $6$ stand from tallest to shortest: only $1$ order.',
        '$7\\times1=7$. We do not multiply by $6!$: the height order is forced.'])

    # practice
    S('wp28-p01', expl=['Each of the $6$ teams has $5$ opponents: $6\\times5=30$.',
                        'Every game was counted twice (once from each team): $\\frac{30}{2}=15$.'])
    S('wp28-p02', expl=['$2!=2$, $3!=2\\times3$, $5!=2^3\\times3\\times5$.',
                        'Add the exponents of each prime: $2^{1+1+3}\\times3^{1+1}\\times5=2^5\\times3^2\\times5$.'])
    S('wp28-p03', expl=['Two green kinds: $\\frac{4\\times3}{2}=6$. Two red kinds: $\\frac{3\\times2}{2}=3$.',
                        'A salad is green or red (two separate cases), so add: $6+3=9$.'])
    S('wp28-p05', expl=['Symbols may repeat: $5\\times5\\times5=125$.'])
    S('wp28-p06', stem='A group of $n$ different performers can line up in 120 different orders. What is $n$?',
      expl=['$n$ performers in a row: $n!$ orders.', '$5!=5\\times4\\times3\\times2\\times1=120$, so $n=5$.'])
    S('wp28-p08', expl=['Hat: $4$ colors. Shirt: a different color, $3$ options. Trousers: $2$ colors left.',
                        '$4\\times3\\times2=24$.'])
    S('wp28-p09', expl=['Symbol: $5$ options. Three different digits in order: $7\\times6\\times5=210$.',
                        'Total: $5\\times210=1050$.'])
    S('wp28-p10', expl=['First place: $5$ options, second: $4$, third: $3$. $5\\times4\\times3=60$.',
                        'The order of the other two swimmers does not matter.'])
    S('wp28-p11', expl=['Two separate cases. Trousers outfits: $3\\times2\\times3=18$. Dress outfits: $2\\times3=6$.',
                        'Add: $18+6=24$.'])
    S('wp28-p12', expl=['With $n$ people: $\\frac{n(n-1)}{2}=55$, so $n(n-1)=110=11\\times10$. Therefore $n=11$.',
                        'Check the other choices: $9$ people give $36$, $10$ give $45$, $12$ give $66$.'])
    S('wp28-p14', expl=['Actors in the left block: $4!=24$ orders. Musicians in the right block: $3!=6$ orders.',
                        'The blocks cannot change sides, so $24\\times6=144$.'])
    S('wp28-p15', expl=[
        'Gaps: place the $4$ blue beads first. They make $5$ gaps: before, between and after them.',
        'No two red beads may touch, so each red bead needs its own gap. $5$ red beads and $5$ gaps: '
        'every gap gets one red bead.',
        'The blue beads are identical, so the only freedom is the order of the red beads: $5!=120$.'])
    S('wp28-p16', stem='A code has $x$ positions. Each position is filled by a digit from 1 to 9, and digits may '
                       'repeat. The number of possible codes is $3^{4n}$. What is $x$?',
      expl=['Each position has $9$ options, so there are $9^x$ codes.',
            '$9^x=(3^2)^x=3^{2x}$. So $3^{2x}=3^{4n}$, $2x=4n$ and $x=2n$.'])
    S('wp28-p17', expl=[
        'The $4$ digits after the 4 must be bigger than $4$ and all different: they come from $5$, $6$, $7$, $8$, $9$. '
        'Once they are chosen, the increasing order is forced.',
        'Choosing $4$ of $5$ is the same as choosing the $1$ digit that stays out: $5$ ways.'])
    S('wp28-p18', stem='Two dice have 8 faces each, numbered 1 to 8. Both dice are rolled, and you are told only the '
                       'sum of the two results. For how many of the possible sums can you know exactly which two '
                       'numbers came up (in any order)?',
      expl=['Sum $2$: only $1+1$. Sum $3$: only $1+2$. Sum $15$: only $7+8$. Sum $16$: only $8+8$.',
            'Every sum from $4$ to $14$ can be made in at least two ways, for example $4=1+3=2+2$ and '
            '$14=6+8=7+7$.',
            'So there are $4$ such sums.'])
    S('wp28-p19', expl=[
        'First digit: $9$ options. It forces the last digit: $1$ option.',
        'Second digit: $1$, $2$, $3$ or $4$ (twice it must still be a digit from $1$ to $9$): $4$ options. '
        'It forces the third digit: $1$ option.',
        '$9\\times4\\times1\\times1=36$.'])
    S('wp28-p20', stem='An eight-digit password uses exactly two different digits, and each of them appears four '
                       'times. The password may start with 0. The sum of its digits must be divisible by 10. How many '
                       'different pairs of digits can be used? (The order of the two digits does not matter.)',
      expl=['If the digits are $a$ and $b$, the sum is $4a+4b=4(a+b)$. It is divisible by $10$ only if $a+b$ is '
            'divisible by $5$.',
            '$a+b=5$: $0$ and $5$, $1$ and $4$, $2$ and $3$ ($3$ pairs).',
            '$a+b=10$: $1$ and $9$, $2$ and $8$, $3$ and $7$, $4$ and $6$ ($4$ pairs; $5$ and $5$ are not two '
            'different digits).',
            '$a+b=15$: $6$ and $9$, $7$ and $8$ ($2$ pairs).',
            'Total: $3+4+2=9$.'])
    S('wp28-p21', stem='A café offers 4 drinks and 6 snacks. One particular drink cannot be served with two of the '
                       'snacks. How many allowed drink-and-snack pairs are there?',
      expl=['All pairs: $4\\times6=24$. Forbidden pairs: $2$.', 'All minus forbidden: $24-2=22$.'])
    S('wp28-p22', expl=['In order: $7\\times6\\times5=210$.',
                        'Every committee appears in $3!=6$ orders: $\\frac{210}{6}=35$.'])
    S('wp28-p23', expl=['Glue the two named books into one block. Now there are $4$ items: $4!=24$ orders.',
                        'Inside the block there are $2$ orders: $24\\times2=48$.'])
    S('wp28-p24', stem='How many three-digit even numbers can be formed from the digits 1, 2, 3, 4 and 5 if no digit '
                       'may repeat?',
      expl=['Most restricted first: the units digit must be even, $2$ or $4$: $2$ options.',
            'Hundreds digit: $4$ digits left. Tens digit: $3$ left.', '$2\\times4\\times3=24$.'])
    S('wp28-p25', stem='How many different arrangements of all the letters of the word LEVEL are there? '
                       '(An arrangement does not have to be a real word.)',
      expl=['If all $5$ letters were different: $5!=120$.',
            'Swapping the two Ls, or the two Es, does not make a new arrangement: divide by $2!\\times2!=4$.',
            '$\\frac{120}{4}=30$.'])
    S('wp28-p26', expl=['Fix one person\'s seat (turning everyone gives the same arrangement).',
                        'The other $7$ sit around them in order: $7!=5040$.'])
    S('wp28-p27', expl=['Choose $3$ of the $6$ for Cedar: $\\frac{6\\times5\\times4}{3!}=\\frac{120}{6}=20$. '
                        'The rest go to Maple.',
                        'The teams have names, so we do not divide by $2$.'])

    # restored originals (pass 2): text clean-up only
    S('wp28-p04', expl=['The first position has $6$ options, then $5$ remain, then $4$, $3$, $2$ and $1$.',
                        'Multiply: $6\\times5\\times4\\times3\\times2\\times1=720$.'])
    S('wp28-p07', stem='Four different prizes are given to four finalists, one prize per finalist. In how many different '
                       'ways can this be done?',
      expl=['The first prize has $4$ possible recipients. $3$ remain for the next prize, then $2$, then $1$.',
            'The product is $4\\times3\\times2\\times1=24$.'])
    S('wp28-p13', expl=['The first cupboard may need $6$ tests before it opens.',
                        'Then $5$ unmatched keys remain for the next cupboard, then $4$, $3$, $2$ and $1$.',
                        'Add them: $6+5+4+3+2+1=21$.'])

    # =====================================================================================================
    # 2. Lesson videos: wording, naming, "rare"
    # =====================================================================================================
    _say(M, 'wp-123', 4, 'organised', 'organized')
    _say(M, 'solve-wp28-g141', 2, 'organised', 'organized')
    _say(M, 'solve-wp28-g142', 3, 'organised', 'organized')
    _say(M, 'solve-wp28-g136', 2, 'The colours matter', 'The colors matter')

    # one name: "Mutual Action"
    v = M.video('wp-131')
    v['title'] = v['navLabel'] = v['hybrid']['title'] = 'Mutual Action'
    v['beats'][0]['title'] = v['beats'][0]['bigTitle'] = 'Mutual Action'
    M.set_slide('wp-131', 1, title='Mutual Action')
    _say(M, 'wp-131', 1, 'Mutual action.', 'Mutual action — like a two-way connection.')

    # Add or Subtract Cases: the original (true) "rare" lines stay; one line links it to probability
    M.edit_lines('wp-134', 2, lambda ls: ls[:-1] + [
        {'say': "So don't panic. But know the idea — probability, the next topic, uses it all the time."}])
    M.edit_lines('wp-134', 4, lambda ls: ls + [
        {'say': "Watch for the words \"not\" and \"at least one\". They almost always mean: all minus forbidden."}])

    # Choosing a Group: general complement rule and the checklist (the original "very rare" line stays)
    M.set_slide('wp-137', 4, title='Who stays out', script=[
        "The second type is simpler than it looks: choose who stays OUT.",
        A("'Choose n − 1 out of n → n ways' appears", T('Choose $n-1$ out of $n$ $\\to$ $n$ ways', size=46)),
        A("'9 out of 10 → 10 ways' appears", T('$9$ out of $10\\ \\to\\ 10$ ways', size=46)),
        "Choose all but one — and the answer is simply the total.",
        D('Next to it write "pick who stays OUT"'),
        "Why? Instead of choosing nine, choose the one who stays out. Ten people — ten choices.",
        A("'Choose k of n = choose the n − k who stay out' appears",
          T('Choose $k$ of $n$ = choose the $n-k$ who stay out', size=42)),
        "And it works for any number. Choosing eight of ten is the same as choosing the two who stay out.",
        D('Write "8 of 10 = 2 of 10 = (10 × 9) ÷ 2 = 45"'),
        "Two of ten: ten times nine, over two. Forty-five. Much faster than dividing by eight factorial.",
        "Always count the smaller side.",
    ])
    M.insert_slides('wp-137', 4, [
        dict(mode='concept', active=3, title='The checklist', script=[
            "Now you have the main tools. Here's the order to think in — for every counting question.",
            A("Step 1 appears", T('1 · Does order matter? Row, code: yes. Group: no', size=36)),
            "One: does order matter? A row or a code — yes. A group — no, so we'll divide by k factorial.",
            A("Step 2 appears", T('2 · Repetition? The pool stays full — or shrinks', size=36)),
            "Two: may items repeat? Then the pool stays full. If not, it shrinks.",
            A("Step 3 appears", T('3 · A restriction? Most restricted first; forced $=1$', size=36)),
            "Three: is there a restriction? Start with the most restricted position. A forced position gets one.",
            A("Step 4 appears", T('4 · Counted twice? $\\div2$ or $\\div k!$', size=36)),
            "Four: did I count the same thing twice? Divide by two — or by k factorial.",
            A("Step 5 appears", T('5 · Cases: add. "Not", "at least one": all $-$ forbidden', size=36)),
            "Five: one count, or cases? Separate cases — add. \"Not\" or \"at least one\" — all minus forbidden.",
            D('Tick each line'),
            "It's on your memory card. Use it on every question.",
        ]),
    ])
    M.set_slide('wp-137', 6, active=4, script=[
        A("Recap line 1 appears", T('A group: ordered count $\\div\\ k!$', size=44)),
        A("Recap line 2 appears", T('Choose $k$ of $n$ = choose the $n-k$ who stay out', size=44)),
        "Two questions next — one of each. Try each one with the checklist.",
    ])
    M.set_sidebar('wp-137', ["Order doesn't matter", 'Divide by k!', 'Who stays out', 'The checklist', 'Recap'])

    # =====================================================================================================
    # 3. Existing solution videos
    # =====================================================================================================
    _draw(M, 'solve-wp28-g132', 2, '20 : 2 = 10', '20 ÷ 2 = 10')
    _draw(M, 'solve-wp28-g133', 3, '7 × 6 : 2 = 21', '7 × 6 ÷ 2 = 21')
    _draw(M, 'solve-wp28-g133', 5, '7 × (7 − 3) : 2 = 7 × 4 : 2 = 14', '7 × (7 − 3) ÷ 2 = 7 × 4 ÷ 2 = 14')

    # Q11: cancel one step at a time, on a fraction
    M.set_slide('solve-wp28-g138', 2, script=[
        "Split eight children into two groups of four — each group with a different teacher.",
        "Choose Maya's four as usual — as if order mattered.",
        D('Write "8 × 7 × 6 × 5"'),
        "First child: eight options. Then seven, six, five.",
        "But picking Dana first and Tal second — or Tal first — it's the same group.",
        "So divide by the internal arrangements of four children: four factorial.",
        D('Write the fraction "(8 × 7 × 6 × 5) / (4 × 3 × 2 × 1)"'),
        "Put it as a fraction. Now cancel — one step at a time.",
        D('Cross out 8 on top and 4 × 2 on the bottom'),
        "Four times two is eight. Eight over eight is one. Cross them out.",
        D('Cross out 6 on top and 3 on the bottom; write 2 above the 6'),
        "Six over three is two.",
        D('Write "= 7 × 2 × 5 = 70"'),
        "What's left: seven times two times five. Seventy.",
        "And Alex's group? No choice left — the four remaining children go to Alex.",
        D('Circle choice 4'),
        "Seventy. Choice four.",
    ])

    # Q14: most restricted position first (hundreds), not the free tens digit
    M.set_slide('solve-wp28-g141', 2, script=[
        "Three-digit numbers — so three positions: hundreds, tens, units.",
        "Tip: above each position write how many options it has; below, list what they are. Keeps you organized.",
        "Most restricted position first. The condition talks about the hundreds and the units. Start with the hundreds digit.",
        "Can it be anything? No. Hundreds plus units must be seven, so it can't go above seven.",
        "And it can't be zero — a number can't start with zero. There's no such number as zero-seven-six.",
        D('Above the hundreds position write "7" and below it "1–7"'),
        "So one to seven: seven options.",
        "Now the units digit. Here's the important idea: dependency.",
        "Once the hundreds digit is chosen, the units digit is already decided. It has to complete the sum to seven.",
        D('Above the units position write "1"'),
        "Hundreds is seven — units must be zero. Hundreds is two — units must be five. One option every time.",
        "And the tens digit? The condition doesn't mention it. It's free: zero to nine. Ten options.",
        D('Above the tens position write "10"'),
        D('Write "7 × 10 × 1 = 70" and circle choice 3'),
        "Seven times ten times one: seventy. Choice three.",
        "These questions aren't simple — and understanding that dependency is the key. More on it in a moment.",
    ])

    # Q17: clear check sentence, "stays out"
    _say(M, 'solve-wp28-g144', 1, 'Last question of the set.', 'Question seventeen.')
    _say(M, 'solve-wp28-g144', 2, "Worried you missed one? Six is fewer than we've already found. Forty-two — or seven "
         "hundred twenty, six factorial — would need dozens more rows, and our list ran out of options.",
         "We found seven. Choice six is too few. Forty-two and seven hundred twenty would need many more rows — "
         "and there are no more.")
    _say(M, 'solve-wp28-g144', 3, '…choose the ONE who stays in place.', '…choose the ONE who stays out.')

    # =====================================================================================================
    # 5. New lesson video A (advanced section): at least one, objects into boxes, checks
    # =====================================================================================================
    VA = 'r26-t28-cases'
    sbA = ['At least one', 'Which is the base?', 'Quick checks', 'Recap']
    M.new_video(VA, TOPIC, 'Boxes and "At Least One"', sbA, [
        dict(mode='title', title='Boxes and "At Least One"', script=[
            "Two question types the exam loves.",
            "\"At least one\" — and objects into boxes.",
        ]),
        dict(mode='concept', active=0, title='At least one', script=[
            "Now three words the exam loves: at least one.",
            A("'At least one = all − none' appears", T('At least one $=$ all $-$ none', size=52)),
            "At least one means one, or two, or three... Many cases. Too many.",
            "The opposite of at least one is none. And none is usually one easy count.",
            A('The example appears', T('Three-digit codes (digits $0$ to $9$) with at least one repeated digit', size=38)),
            "Example: three-digit codes — zero may come first — where at least one digit repeats.",
            D('Write "all: 10 × 10 × 10 = 1000"'),
            "All codes: ten times ten times ten. One thousand.",
            D('Write "no repeats: 10 × 9 × 8 = 720"'),
            "No repeats — all different: ten, nine, eight. Seven hundred twenty.",
            D('Write "1000 − 720 = 280"'),
            "All minus none: two hundred eighty.",
            "You'll use this again and again in probability.",
        ]),
        dict(mode='concept', active=1, title='Which is the base?', script=[
            A("'4 letters into 3 mailboxes' appears", T('$4$ different letters into $3$ mailboxes', size=48)),
            "Four different letters go into three mailboxes. Any mailbox can get any number of letters.",
            "Is it three to the fourth, or four to the third? Ask: who chooses?",
            "Every letter chooses a mailbox. Letter one: three options. Letter two: three options. Letter three, letter four: three each.",
            D('Write "3 × 3 × 3 × 3 = 3⁴ = 81"'),
            "Four stages — one for each letter. Three options each. Three to the fourth: eighty-one.",
            "The trap is four to the third, sixty-four. That would be each mailbox choosing one letter — but a mailbox can get two letters, or none.",
            A("'Each object chooses a box' appears", T('Each object chooses: one stage per object', size=44)),
        ]),
        dict(mode='concept', active=2, title='Quick checks', script=[
            "Two quick checks that save points.",
            A('Check 1 appears', T('1 · Test a formula on a small case', size=42)),
            "One: not sure about a formula? Test it on a small case you can draw.",
            D('Draw 4 dots in a square, join every two of them, and write "4 × 3 ÷ 2 = 6 ✓"'),
            "Four people shaking hands: the formula says four times three over two — six. Draw four dots and join them: six lines. The formula works.",
            A('Check 2 appears', T('2 · Order matters? The bigger answer. A group? Divide', size=42)),
            "Two: look at the choices. They often differ by a factor — like two hundred ten and thirty-five.",
            D('Write "7 × 6 × 5 = 210 with roles  →  210 ÷ 3! = 35 as a group"'),
            "Seven people, choose three: two hundred ten with roles, thirty-five as a group. Both will be in the choices.",
            "So ask the checklist question first: does order matter?",
        ]),
        dict(mode='concept', active=3, title='Recap', script=[
            A('Recap line 1 appears', T('At least one $=$ all $-$ none', size=40)),
            A('Recap line 2 appears', T('Objects into boxes: each object chooses', size=40)),
            A('Recap line 3 appears', T('Not sure? Test on a small case', size=40)),
            "Two questions next — one of each.",
        ]),
    ], ADV, after='solve-wp28-g144')
    M.video(VA)['hybrid']['num'] = 54

    g4, g5 = ['q-r26-t28-%02d' % k for k in (4, 5)]
    M.new_q(g4, TOPIC, 'A code has 4 digits. Each digit is from 0 to 9, digits may repeat, and the code may start with '
                       '0. How many codes contain the digit 5 at least once?', ['$4000$', '$3439$', '$6561$', '$2916$'], 2, [
        'At least one $=$ all $-$ none.',
        'All codes: $10^4=10000$.',
        'Codes with no 5: each digit has $9$ options: $9^4=6561$.',
        '$10000-6561=3439$.'])
    M.place_q(g4, ADV, after=VA)
    _sol(M, g4, True, ["At least once."], [
        ('Method 1 · All minus none', [
            "\"At least once.\" That's the signal: all minus none.",
            D('Write "all: 10⁴ = 10000"'),
            "All codes: ten options for each of four digits. Ten thousand.",
            D('Write "no 5: 9⁴ = 6561"'),
            "No five at all: nine options for each digit. Nine to the fourth.",
            "Nine squared is eighty-one. Eighty-one squared is six thousand five hundred sixty-one.",
            D('Write "10000 − 6561 = 3439"'),
            "All minus none: three thousand four hundred thirty-nine.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
        ('The traps', [
            "Why not count directly? Put a five in the first place: then ten, ten, ten. Four places — four thousand.",
            D('Next to choice 1 write "4 × 1000 ✗"'),
            "But the code five-five-zero-zero was counted twice: once for the five in the first place, once for the second place.",
            D('Next to choice 4 write "exactly one 5: 4 × 9³"'),
            "And two thousand nine hundred sixteen is four times nine cubed: exactly one five. At least once also includes two, three and four fives.",
        ]),
    ])

    M.new_q(g5, TOPIC, 'Five different letters are put into 3 mailboxes. A mailbox may get any number of letters, or '
                       'none. In how many different ways can the letters be put into the mailboxes?',
            ['$125$', '$15$', '$243$', '$60$'], 3, [
        'Each letter chooses a mailbox: $3$ options for each of the $5$ letters.',
        '$3\\times3\\times3\\times3\\times3=3^5=243$.',
        'The trap $5^3=125$ lets each mailbox choose one letter, but a mailbox may get several letters, or none.'])
    M.place_q(g5, ADV, after='solve-' + g4)
    _sol(M, g5, True, ["Which is the base?"], [
        ('Method 1 · Every letter chooses', [
            "Three to the fifth, or five cubed? Ask: who chooses?",
            "Every letter must go somewhere. Letter one chooses a mailbox: three options. Letter two: three options — a mailbox can take more than one.",
            D('Write "3 × 3 × 3 × 3 × 3 = 3⁵"'),
            "Five letters — five stages. Three options each.",
            D('Write "3⁵ = 243"'),
            "Three, nine, twenty-seven, eighty-one, two hundred forty-three.",
            D('Circle choice 3'),
            "Choice three.",
            "The trap is five cubed, one hundred twenty-five: every mailbox choosing one letter. But a mailbox can get two letters, or none.",
        ]),
        ('Method 2 · Check a small case', [
            "Not sure which is the base? Try two letters and two mailboxes.",
            D('Write "letter 1, letter 2 → boxes: (1,1) (1,2) (2,1) (2,2) = 4 = 2²"'),
            "Both in box one. Both in box two. Or split — two ways. Four. That's two squared: boxes to the power of letters.",
        ]),
    ])

    # =====================================================================================================
    # 6. New lesson video B: together, not together, gaps, identical items, round table
    # =====================================================================================================
    VB = 'r26-t28-arrange'
    sbB = ['Together: glue', 'Not together', 'No two side by side', 'Identical items', 'Round table', 'Recap']
    M.new_video(VB, TOPIC, 'Together, Apart and Repeats', sbB, [
        dict(mode='title', title='Together, Apart and Repeats', script=[
            "Rows with a rule.",
            "People who must stand together — or apart. Items that repeat. And a round table.",
        ]),
        dict(mode='concept', active=0, title='Together: glue', script=[
            A('The example appears', T('$5$ people in a row. Dana and Eli must stand together', size=42)),
            "Five people in a row. Dana and Eli must stand together. How many rows?",
            "The trick: glue them. Tie Dana and Eli into one block.",
            D('Draw a box around "D E" and write "block + 3 others = 4 items"'),
            "Now there are four items: the block and three other people.",
            D('Write "4! = 24"'),
            "Four items in a row: four factorial, twenty-four.",
            "But inside the block, the order can be Dana-Eli or Eli-Dana. Two orders.",
            D('Write "24 × 2 = 48"'),
            "Twenty-four times two: forty-eight.",
            "Three people together? Glue three — and inside the block, three factorial.",
        ]),
        dict(mode='concept', active=1, title='Not together', script=[
            "Now the opposite: Dana and Eli must NOT stand together.",
            A("'Not together = all − together' appears", T('Not together $=$ all $-$ together', size=50)),
            "Don't count this directly. Count all, then remove the rows where they are together.",
            D('Write "all: 5! = 120"'),
            "All rows: five factorial, one hundred twenty.",
            D('Write "120 − 48 = 72"'),
            "Together: forty-eight — we just found it. So seventy-two rows where they're apart.",
        ]),
        dict(mode='concept', active=2, title='No two side by side', script=[
            "With more people, \"apart\" gets harder: no two girls side by side.",
            A('The example appears', T('$4$ boys and $3$ girls in a row. No two girls side by side', size=40)),
            "The trick: gaps. First place the people with no rule — the boys.",
            D('Write "_ B _ B _ B _ B _"'),
            "Four boys: four factorial, twenty-four orders. They make five gaps: before, between and after them.",
            D('Write "boys: 4! = 24"'),
            "Now each girl goes into her own gap. Then no two girls can touch.",
            D('Write "girls: 5 × 4 × 3 = 60"'),
            "First girl: five gaps. Second: four left. Third: three.",
            D('Write "24 × 60 = 1440"'),
            "Twenty-four times sixty: one thousand four hundred forty.",
        ]),
        dict(mode='concept', active=3, title='Identical items', script=[
            "What if some items are the same?",
            A("'AAB, ABA, BAA' appears", T('A, A, B: $\\quad AAB,\\ ABA,\\ BAA$', size=46)),
            "The letters A, A and B. If the two A's were different, we'd have three factorial: six orders.",
            "But swapping the two A's changes nothing. Every arrangement was counted twice.",
            D('Write "3! ÷ 2! = 6 ÷ 2 = 3"'),
            "Six over two: three. And there they are.",
            A("'Divide by the factorial of each repeat' appears", T('Repeats: $n!\\ \\div$ (the factorial of each repeat)', size=42)),
            "The rule: arrange as if all were different — then divide by the factorial of each repeat.",
            D('Write "BOOK: 4! ÷ 2! = 24 ÷ 2 = 12"'),
            "BOOK: four letters, O twice. Twenty-four over two: twelve.",
        ]),
        dict(mode='concept', active=4, title='Round table', script=[
            "Last one: a round table.",
            A('The example appears', T('$4$ people around a round table', size=46)),
            "Four people around a table. Everyone moves one seat to the right — and nobody's neighbors changed. It's the same arrangement.",
            "So the row count, twenty-four, counts every table arrangement four times.",
            D('Write "4! ÷ 4 = 3! = 6"'),
            "The fast way: fix one person in her seat. Then arrange the others around her: three factorial, six.",
            A("'n people around a table: (n − 1)!' appears", T('$n$ people around a table: $(n-1)!$', size=46)),
            "n people around a table: n minus one, factorial.",
        ]),
        dict(mode='concept', active=5, title='Recap', script=[
            A('Recap line 1 appears', T('Together: glue, then $\\times$ the order inside', size=40)),
            A('Recap line 2 appears', T('Not together $=$ all $-$ together', size=40)),
            A('Recap line 3 appears', T('No two side by side: the others first, then the gaps', size=40)),
            A('Recap line 4 appears', T('Repeats: divide by the factorial of each repeat', size=40)),
            A('Recap line 5 appears', T('Round table: fix one person, $(n-1)!$', size=40)),
            "Four questions next.",
        ]),
    ], ADV, after='solve-' + g5)
    M.video(VB)['hybrid']['num'] = 55

    g6, g7, g8, g9 = ['q-r26-t28-%02d' % k for k in (6, 7, 8, 9)]
    M.new_q(g6, TOPIC, 'Six different books are placed on a shelf in a row. The 3 math books among them must stand '
                       'together, in any order. How many arrangements are possible?',
            ['$24$', '$144$', '$36$', '$720$'], 2, [
        'Glue the $3$ math books into one block. Now there are $4$ items: the block and the $3$ other books. '
        '$4!=24$ orders.',
        'Inside the block, the math books can stand in $3!=6$ orders.',
        '$24\\times6=144$.'])
    M.place_q(g6, ADV, after=VB)
    _sol(M, g6, True, ["Books that must stand together."], [
        ('Method 1 · Glue, then the order inside', [
            "Together? Glue.",
            D('Write "[M M M] + 3 books = 4 items"'),
            "Tie the three math books into one block. The block plus three other books: four items.",
            D('Write "4! = 24"'),
            "Four items in a row: twenty-four.",
            D('Write "inside: 3! = 6"'),
            "Inside the block: three math books in any order. Three factorial, six.",
            D('Write "24 × 6 = 144"'),
            "Twenty-four times six: one hundred forty-four.",
            D('Circle choice 2'),
            "Choice two. Twenty-four is the trap — it forgets the order inside the block.",
        ]),
    ])

    M.new_q(g7, TOPIC, 'Three boys and two girls stand in a row. All five are different people. The two girls may not '
                       'stand next to each other. How many orders are possible?', ['$48$', '$72$', '$36$', '$12$'], 2, [
        'Gaps: first place the boys: $3!=6$ orders. They make $4$ gaps: before, between and after them.',
        'Each girl goes into a different gap: $4\\times3=12$.',
        '$6\\times12=72$.',
        'Check with all minus together: all orders $5!=120$. Girls together (glue): $4!\\times2=48$. $120-48=72$.'])
    M.place_q(g7, ADV, after='solve-' + g6)
    _sol(M, g7, True, ["Two girls who may not stand side by side."], [
        ('Method 1 · Gaps', [
            "No two side by side: place the others first.",
            D('Write "_ B _ B _ B _"'),
            "The three boys: three factorial, six orders. They make four gaps.",
            D('Write "boys: 3! = 6"'),
            D('Write "girls: 4 × 3 = 12"'),
            "The first girl picks one of four gaps. The second girl: one of the three other gaps. Twelve.",
            D('Write "6 × 12 = 72"'),
            "Six times twelve: seventy-two.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
        ('Method 2 · All minus together', [
            "With only two girls, \"not next to each other\" is simply \"not together\".",
            D('Write "all: 5! = 120"'),
            "All rows: one hundred twenty.",
            D('Write "together: 4! × 2 = 48"'),
            "Girls together: glue them. Four items, twenty-four orders, times two inside. Forty-eight.",
            D('Write "120 − 48 = 72"'),
            "One hundred twenty minus forty-eight: seventy-two. Forty-eight is the trap — that's the \"together\" count.",
        ]),
    ])

    M.new_q(g8, TOPIC, 'How many different arrangements of all the letters of the word BANANA are there? '
                       '(An arrangement does not have to be a real word.)', ['$720$', '$120$', '$60$', '$360$'], 3, [
        'If all $6$ letters were different: $6!=720$.',
        'A appears $3$ times: swapping the As gives nothing new, so divide by $3!=6$. N appears $2$ times: '
        'divide by $2!=2$.',
        '$\\frac{720}{3!\\times2!}=\\frac{720}{12}=60$.'])
    M.place_q(g8, ADV, after='solve-' + g7)
    _sol(M, g8, True, ["Letters that repeat."], [
        ('Method 1 · Divide by the repeats', [
            "Six letters: B, A, N, A, N, A.",
            D('Write "6! = 720"'),
            "If all six were different: six factorial, seven hundred twenty.",
            D('Under the As write "A × 3 → ÷ 3! = 6"'),
            "But A appears three times. Swapping the As changes nothing. Divide by three factorial, six.",
            D('Under the Ns write "N × 2 → ÷ 2! = 2"'),
            "N appears twice. Divide by two.",
            D('Write "720 ÷ (6 × 2) = 720 ÷ 12 = 60"'),
            "Seven hundred twenty over twelve: sixty.",
            D('Circle choice 3'),
            "Choice three. One hundred twenty and three hundred sixty are the traps — each forgets one of the repeats.",
        ]),
    ])

    M.new_q(g9, TOPIC, 'Six people sit around a round table. Two arrangements are the same if one is a rotation of the '
                       'other. Dana and Eli must sit next to each other. How many arrangements are possible?',
            ['$240$', '$120$', '$24$', '$48$'], 4, [
        'Glue Dana and Eli into one block. Now there are $5$ items around the table.',
        'Round table: fix one item and arrange the others: $(5-1)!=4!=24$.',
        'Inside the block: $2$ orders (Dana on the left or on the right of Eli). $24\\times2=48$.',
        'Check: fix Dana\'s seat. Eli sits in one of the $2$ seats next to her, and the other $4$ people fill the '
        'other seats in $4!=24$ ways: $2\\times24=48$.'])
    M.place_q(g9, ADV, after='solve-' + g8)
    _sol(M, g9, True, ["A round table — with a pair that must sit together."], [
        ('Method 1 · Glue, then fix one', [
            "Two rules at once: together, and a round table. One at a time.",
            D('Write "[D E] + 4 others = 5 items"'),
            "Together: glue Dana and Eli. Now five items sit around the table.",
            D('Write "round: (5 − 1)! = 4! = 24"'),
            "Round table: fix one item, arrange the other four. Twenty-four.",
            D('Write "24 × 2 = 48"'),
            "Inside the block: Dana on the left, or on the right. Times two: forty-eight.",
            D('Circle choice 4'),
            "Choice four.",
            "The traps: two hundred forty treats the table like a row. Twenty-four forgets the order inside the block.",
        ]),
        ('Method 2 · Fix Dana', [
            "A check. Fix Dana in her seat.",
            D('Write "Eli: 2 seats × others: 4! = 2 × 24 = 48"'),
            "Eli must sit next to her: two seats. The other four fill the rest in twenty-four ways. Forty-eight again.",
        ]),
    ])

    # 2026-10-01 elite comparison: factorials as algebra (lesson slides + guided question)
    elite_factorials(M)

    # advanced card goes to the end of the section, with the new methods
    M.move('mem-counting-advanced', ADV)

    # sidebars of all guided solution videos (learn / advanced groups)
    for vid in ['solve-wp28-g%d' % k for k in (124, 125, 126, 128, 129, 130, 132, 133, 135, 136, 138, 139)]:
        M.set_sidebar(vid, SB_LEARN)
    for vid in ['solve-wp28-g%d' % k for k in (140, 141, 142, 143, 144)]:
        M.set_sidebar(vid, SB_ADV)

    # =====================================================================================================
    # 7. Memory cards
    # =====================================================================================================
    c = M.card('mem-counting')
    c['tables'].insert(0, {'title': 'The 5-step checklist', 'head': ['Step', 'Ask', 'Then'], 'rows': [
        ['1', 'Does order matter?', 'a row or a code: yes · a group: no (divide by \\(k!\\))'],
        ['2', 'Repetition allowed?', 'yes: the pool stays full · no: the pool shrinks'],
        ['3', 'A restriction?', 'most restricted position first; a forced position \\(=1\\)'],
        ['4', 'Counted twice?', 'divide by \\(2\\) (mutual action) or by \\(k!\\) (a group)'],
        ['5', 'One count or cases?', 'separate cases: add · "not", "at least one": all \\(-\\) forbidden'],
    ]})
    rows = c['tables'][1]['rows']
    rows.append(['\\(k\\) out of \\(n\\)', 'choose the \\(n-k\\) who stay out',
                 '8 of 10: \\(\\frac{10\\times9}{2}=45\\)'])
    c['tips'] += ['Not sure about a formula? Test it on a small case you can draw: 4 people, '
                  '\\(\\frac{4\\times3}{2}=6\\) handshakes.',
                  'Choices that differ by a factor (\\(210\\) and \\(35\\))? Order matters: the bigger one. '
                  'A group: divide.']

    c = M.card('mem-counting-advanced')
    c['tables'].insert(1, {'title': 'More methods', 'head': ['Situation', 'Method', 'Example'], 'rows': [
        ['At least one', 'all \\(-\\) none', '\\(10^4-9^4=3439\\)'],
        ['Objects into boxes', 'each object chooses a box', '5 letters, 3 boxes: \\(3^5=243\\)'],
        ['Must be together', 'glue into one block, \\(\\times\\) the order inside', '\\(4!\\times3!=144\\)'],
        ['Must not be together', 'all \\(-\\) together', '\\(5!-4!\\times2=72\\)'],
        ['No two side by side', 'place the others, then fill the gaps', '\\(3!\\times4\\times3=72\\)'],
        ['Identical items', 'divide by the factorial of each repeat', 'BANANA: \\(\\frac{6!}{3!\\times2!}=60\\)'],
        ['Round table', 'fix one person: \\((n-1)!\\)', '4 people: \\(3!=6\\)'],
    ]})
    c['intro'] = 'The shortcuts from the advanced counting questions and the two method videos.'

    # =====================================================================================================
    # 8. New practice questions
    # =====================================================================================================
    P = {}
    P['14'] = ('A committee of 3 is chosen from 5 men and 4 women. How many committees include at least one woman?',
               ['$84$', '$40$', '$74$', '$80$'], 3, [
        'At least one $=$ all $-$ none.',
        'All committees: $\\frac{9\\times8\\times7}{3!}=\\frac{504}{6}=84$.',
        'No women (only men): $\\frac{5\\times4\\times3}{3!}=10$.',
        '$84-10=74$.'])
    P['15'] = ('A 4-digit PIN uses the digits 0 to 9, and it may start with 0. How many PINs have at least one digit '
               'that appears more than once?', ['$5040$', '$4960$', '$3439$', '$9000$'], 2, [
        'At least one repeat $=$ all $-$ no repeats.',
        'All PINs: $10^4=10000$. All digits different: $10\\times9\\times8\\times7=5040$.',
        '$10000-5040=4960$.'])
    P['16'] = ('Each of 4 students chooses one of 3 after-school clubs. In how many different ways can the students '
               'choose?', ['$64$', '$81$', '$12$', '$24$'], 2, [
        'Each student chooses: $3$ options for each of the $4$ students.',
        '$3\\times3\\times3\\times3=3^4=81$. ($4^3=64$ is the trap: the clubs do not choose the students.)'])
    P['17'] = ('A test has 5 questions, and each question has 4 answer choices. A student answers every question. In '
               'how many different ways can the answer sheet be filled?', ['$625$', '$20$', '$1024$', '$120$'], 3, [
        'Each question gets one of $4$ choices: $4\\times4\\times4\\times4\\times4=4^5=1024$.'])
    P['18'] = ('Seven people stand in a row. Three of them are sisters, and the sisters must stand together, in any '
               'order. How many orders are possible?', ['$720$', '$120$', '$144$', '$5040$'], 1, [
        'Glue the $3$ sisters into one block: the block and $4$ other people make $5$ items. $5!=120$ orders.',
        'Inside the block: $3!=6$ orders.', '$120\\times6=720$.'])
    P['19'] = ('Six different books are placed on a shelf in a row. Two particular books may not stand next to each '
               'other. How many arrangements are possible?', ['$480$', '$240$', '$600$', '$360$'], 1, [
        'Not together $=$ all $-$ together.',
        'All: $6!=720$. Together (glue the two books): $5!\\times2=240$.',
        '$720-240=480$.'])
    P['20'] = ('There are 7 chairs in a row. Three different people sit on three of the chairs, so that no two of them '
               'sit next to each other. In how many ways can this be done?', ['$60$', '$210$', '$10$', '$120$'], 1, [
        'Gaps: start with the $4$ empty chairs. They make $5$ gaps: before, between and after them.',
        'Each person takes a different gap, so no two of them are side by side: $5\\times4\\times3=60$.',
        'The empty chairs are all the same, so there is nothing more to arrange.'])
    P['21'] = ('How many different five-digit numbers can be formed using all of the digits 1, 1, 2, 2, 2?',
               ['$120$', '$20$', '$10$', '$60$'], 3, [
        'If all $5$ digits were different: $5!=120$.',
        'The digit 1 repeats $2$ times and the digit 2 repeats $3$ times: $\\frac{120}{2!\\times3!}=\\frac{120}{12}=10$.'])
    P['22'] = ('How many different four-digit numbers can be formed using all of the digits 0, 3, 3 and 5?',
               ['$12$', '$24$', '$9$', '$6$'], 3, [
        'All orders of $0$, $3$, $3$, $5$: $\\frac{4!}{2!}=\\frac{24}{2}=12$.',
        'Orders that start with $0$ are not four-digit numbers: the other three digits $3$, $3$, $5$ in '
        '$\\frac{3!}{2!}=3$ orders.',
        'All minus forbidden: $12-3=9$.'])
    P['23'] = ('Five friends sit around a round table. Two arrangements are the same if one is a rotation of the '
               'other. Adi and Ben may not sit next to each other. How many arrangements are possible?',
               ['$12$', '$24$', '$72$', '$6$'], 1, [
        'All arrangements: fix one person, $(5-1)!=4!=24$.',
        'Adi and Ben together: glue them, $4$ items around the table: $(4-1)!\\times2=6\\times2=12$.',
        'Not together: $24-12=12$.'])
    P['26'] = ('In how many different ways can 8 players be chosen from 10 players for a trip?',
               ['$90$', '$10$', '$45$', '$80$'], 3, [
        'Choosing $8$ of $10$ is the same as choosing the $2$ who stay out.',
        '$2$ of $10$: $\\frac{10\\times9}{2}=45$.'])
    P['27'] = ('A 4-letter code is made from the letters A, B, C, D and E, and no letter may repeat. How many codes '
               'contain the letter A?', ['$96$', '$24$', '$48$', '$120$'], 1, [
        'All codes: $5\\times4\\times3\\times2=120$. Codes without A: $4\\times3\\times2\\times1=24$.',
        'All minus none: $120-24=96$.',
        'Check: A takes one of $4$ positions, and the other $3$ positions are filled in $4\\times3\\times2=24$ ways: '
        '$4\\times24=96$.'])
    for k, (stem, ch, cor, ex) in P.items():
        M.new_q('q-r26-t28-' + k, TOPIC, stem, ch, cor, ex)
        M.place_q('q-r26-t28-' + k, PRAC)

    n = lambda k: 'q-r26-t28-' + k
    p = lambda k: 'wp28-p' + k
    M.practice_order(PRAC, [
        'alg-extra-unit-t18-3-4', p('07'), p('05'), p('06'), p('04'), p('01'), p('08'), p('10'), p('21'), p('22'),
        p('14'), p('09'), p('11'), p('03'), p('24'), p('12'), n('16'), n('17'), n('26'), p('16'), p('02'), p('27'),
        p('17'), p('19'), p('23'), n('18'), n('21'), p('25'), p('13'), n('14'), n('27'), n('15'), n('19'), p('26'),
        n('23'), p('15'), n('20'), n('22'), p('18'), p('20')])

    # =====================================================================================================
    # 8b. Summary lesson right before the practice (pass 2)
    # =====================================================================================================
    sbS = ['Stages: multiply', 'Repetition and rows', 'Counted twice?', 'Who stays out', 'Cases', 'Objects into boxes',
           'Together and apart', 'Before you practice']
    M.new_video('r26-t28-summary', TOPIC, 'Summary', sbS, [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of counting.",
            "Everything important, in a few minutes.",
        ]),
        dict(mode='concept', active=0, title='Stages: multiply', script=[
            A("'Stages → multiply' appears", T('Stages of choice $\\to$ multiply: $3\\times5=15$', size=44)),
            "Work in stages. How many options at each stage? Multiply.",
            A("'Most restricted first' appears", T('Most restricted position first; a forced position $=1$', size=40)),
            "A restriction? Start with the most restricted position. A position that is already decided gets one.",
            "Three shirts and five hats: fifteen outfits. Not eight — adding counts items, not outfits.",
            "A short list with no pattern? Just list and count.",
        ]),
        dict(mode='concept', active=1, title='Repetition and rows', script=[
            A("'With repetition' appears", T('Repeats allowed: the pool stays full, $8\\times8\\times8=512$', size=40)),
            A("'Without repetition' appears", T('No repeats: the pool shrinks, $8\\times7\\times6=336$', size=40)),
            "May items repeat? The pool stays full. If not, it shrinks by one each stage.",
            A("'n in a row: n!' appears", T('$n$ items in a row: $n!$ $\\quad\\frac{9!}{7!}=9\\times8=72$', size=40)),
            "n items in a row: n factorial. And with factorials, expand only until they cancel.",
        ]),
        dict(mode='concept', active=2, title='Counted twice?', script=[
            A("'Mutual action ÷ 2' appears", T('Handshakes, games, routes: $\\frac{n(n-1)}{2}$', size=42)),
            "Handshakes, games, two-way routes: each pair was counted twice. Divide by two.",
            A("'Diagonals' appears", T('Diagonals of an $n$-gon: $\\frac{n(n-3)}{2}$', size=42)),
            A("'A group ÷ k!' appears", T('A group: ordered count $\\div\\ k!$', size=42)),
            "A group, where order doesn't matter: count in order, then divide by k factorial.",
        ]),
        dict(mode='concept', active=3, title='Who stays out', script=[
            A("'Choose k of n = choose n − k' appears", T('Choose $k$ of $n$ $=$ choose the $n-k$ who stay out', size=42)),
            "Choosing many? Choose who stays out instead.",
            A('The example appears', T('$6$ of $7\\to7$ ways $\\qquad 7$ of $9=2$ of $9=\\frac{9\\times8}{2}=36$', size=40)),
            "Six of seven: seven ways. Seven of nine: the two who stay out — thirty-six. Always count the smaller side.",
        ]),
        dict(mode='concept', active=4, title='Cases', script=[
            A("'Separate cases: add' appears", T('Separate cases (no overlap): add', size=42)),
            "Can't count in one go? Split into cases that don't overlap — and add.",
            A("'Allowed = all − forbidden' appears", T('Allowed $=$ all $-$ forbidden', size=42)),
            A("'At least one = all − none' appears", T('At least one $=$ all $-$ none: $10^3-9^3=271$', size=42)),
            "\"Not\" or \"at least one\"? Count all, subtract the forbidden ones.",
            "Three-digit codes with at least one seven: all one thousand, minus the seven hundred twenty-nine with no seven.",
        ]),
        dict(mode='concept', active=5, title='Objects into boxes', script=[
            A("'Each object chooses' appears", T('Each object chooses a box: $(\\text{boxes})^{\\text{objects}}$', size=42)),
            "Objects into boxes: each object chooses. Four friends, two buses: two to the fourth.",
            A("'Test on a small case' appears", T('Not sure? Test it on a small case you can draw', size=42)),
            "Not sure about a formula? Test it on a tiny case.",
        ]),
        dict(mode='concept', active=6, title='Together and apart', script=[
            A("'Together: glue' appears", T('Together: glue into a block, $\\times$ the order inside', size=38)),
            A("'Not together' appears", T('Not together $=$ all $-$ together', size=38)),
            "Together? Glue them, then multiply by the order inside. Not together? All minus together.",
            A("'Gaps' appears", T('No two side by side: place the others, then use the gaps', size=38)),
            A("'Repeats and round table' appears", T('Repeats: $\\div$ each repeat\'s factorial $\\quad$ Round table: $(n-1)!$', size=38)),
            "Repeated items: divide by the factorial of each repeat. A round table: fix one person — n minus one, factorial.",
        ]),
        dict(mode='concept', active=7, title='Before you practice', script=[
            "Before every question, ask yourself:",
            A('Check 1 appears', T('Does order matter? A row or a code: yes. A group: no', size=38)),
            A('Check 2 appears', T('May items repeat?', size=38)),
            A('Check 3 appears', T('Which position is the most restricted?', size=38)),
            A('Check 4 appears', T('Did I count the same thing twice?', size=38)),
            A('Check 5 appears', T('One count — or cases?', size=38)),
            "The traps: adding when you should multiply. Dividing without a reason. And a zero that can't lead a number.",
            "Good luck. Let's practice.",
        ]),
    ], ADV, after='mem-counting-advanced')

    # 2026-10-01 elite comparison: factorial practice, card rows, summary slide
    elite_factorials_late(M)

    # =====================================================================================================
    # 9. Keep the slide notes of all guided solution videos in sync (and no "−" inside words)
    # =====================================================================================================
    for vid, v in M.D['videos'].items():
        if v.get('topic') != TOPIC or v.get('kind') != 'solution' or not v.get('questionId'):
            continue
        qid = v['questionId']
        if qid not in M.D['questions']:
            continue
        stem = rich_plain(M.q(qid)['stemRich']).replace('\\times', '×')
        v['title'] = v['navLabel'] = stem
        for b in v['beats']:
            if (b.get('canvas') or '').startswith('Pre-loaded — question'):
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, stem)
    cut_repeats(M)
    add_methods(M)   # 2026-10-06 new exam methods (runs last)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)
    renumber_pass(M)   # 2026-10-06 renumber pass (runs last)


# =========================================================================================================
# 2026-10-01 elite comparison: factorials as algebra. Real exams: 2020 winter I-19, 2022 autumn I-17,
# 2020 autumn I-4, 2024 winter II-17, 2019 winter II-16, 2021 autumn II-5, 2021 spring I-5, 2022 winter II-7,
# 2025 winter I-7, 2025 spring I-14, 2026 spring II-18.
# =========================================================================================================
FL = 'wp-140-after'


def elite_factorials(M):
    # Factorial Expressions: 1 title, 2 stop early, 3-4 plug in / math, 5 not one factorial, 6 recap
    M.insert_slides(FL, 5, [
        dict(mode='concept', active=4, title='Know them by sight', script=[
            A('3!, 4!, 5! appear', T('$3!=6 \\qquad 4!=24 \\qquad 5!=120$', size=50, gap=30)),
            A('6!, 7! appear', T('$6!=720 \\qquad 7!=5040$', size=50, gap=110)),
            "Know these by sight. Each one is the one before, times the next number.",
            D('Write "5! × 6 = 720     6! × 7 = 5040"'),
            "One hundred twenty times six: seven hundred twenty. Times seven: five thousand forty.",
            "See 120, 720 or 5040 in a question? Think: five, six or seven factorial.",
            A('a! = 6 · 20 appears', T('$a!=6\\cdot20 \;\\to\; 120=5! \;\\to\; a=5$', size=46)),
            "Multiply it out — and recognize the number. Six times twenty is one hundred twenty. That's five factorial.",
        ]),
        dict(mode='concept', active=5, title='A run of neighbors', script=[
            A('b!/a! = a run appears', T('$\\dfrac{b!}{a!}=(a+1)(a+2)\\cdots b$', size=50, gap=40)),
            "A big factorial over a smaller one: everything from a down to one cancels.",
            "What's left is a run of neighbors — whole numbers in a row, from a plus one up to b.",
            D('Write "8! ÷ 5! = 8 · 7 · 6 = 336"'),
            A('b! = 56 · a! appears', T('$b!=56\\cdot a! \;\\to\; \\dfrac{b!}{a!}=56=7\\cdot8$', size=46, gap=60)),
            "Now backwards. b factorial over a factorial is fifty-six. Split fifty-six into neighbors: seven times eight.",
            D('Write "a = 6, b = 8"'),
            "The run starts right after a — so a is six, not seven. It ends at b: b is eight.",
            "The exam usually limits the numbers — say, below ten — so the run has two or more neighbors.",
            A('n!/(n − 1)! = n appears', T('$\\dfrac{n!}{(n-1)!}=n \\qquad \\dfrac{n!}{(n-2)!}=n(n-1)$', size=46)),
            "A run can be short. One step apart: just n. Two steps apart: n times n minus one.",
        ]),
        dict(mode='concept', active=6, title='Sums: take out the smaller', script=[
            "A sum of factorials? Don't calculate. Take out the smaller factorial — like a common factor.",
            A('5! + 6! = 5! · 7 appears', T('$5!+6!=5!\\cdot(1+6)=5!\\cdot7$', size=48, gap=40)),
            "Six factorial is six times five factorial. Take out five factorial: one plus six stays inside.",
            "Don't forget the one. It's the five factorial itself.",
            A('6! + 8! = 6! · 57 appears', T('$6!+8!=6!\\cdot(1+7\\cdot8)=6!\\cdot57$', size=48, gap=40)),
            "Two steps apart? Eight factorial is eight times seven times six factorial. One plus fifty-six: fifty-seven.",
            A('8! − 7! = 7! · 7 appears', T('$8!-7!=7!\\cdot(8-1)=7\\cdot7!$', size=48)),
            "A minus works the same way. Then it cancels with what's on the other side of the fraction.",
            "And the trap: eight factorial minus seven factorial is NOT one factorial. We never subtract inside the exclamation mark.",
        ]),
        dict(mode='concept', active=7, title='Factorials and primes', script=[
            "A divisibility question about a factorial? Break every factor into primes.",
            A('7! written out appears', T('$7!=7\\cdot6\\cdot5\\cdot4\\cdot3\\cdot2$', size=48, gap=110)),
            D('Under the factors write "7    2·3    5    2²    3    2"'),
            A('7! = 2⁴ · 3² · 5 · 7 appears', T('$7!=2^4\\cdot3^2\\cdot5\\cdot7$', size=48, gap=40)),
            "Count the twos: one in six, two in four, one in two. Four twos. Two threes, one five, one seven.",
            "Is seven factorial divisible by sixteen — two to the fourth? Yes. By thirty-two? No. There are only four twos.",
            "Divisible by twenty-five? No — there is only one five.",
            A("'Count the 2s, not the even numbers' appears", T('Count the $2$s — not the even numbers', size=44)),
            "The trap: counting the even numbers. There are three even numbers — but four twos. Four hides two of them.",
        ]),
    ])
    M.set_slide(FL, 10, script=[
        "Let's lock it in.",
        A("'n! = n · (n − 1)!' appears", T('$n!=n\\cdot(n-1)!$ — expand only until you match, then cancel', size=38)),
        A("'Letters? Plug in a small legal value' appears", T('Letters? Plug in a small legal value', size=38)),
        A("'Know 5!, 6!, 7!' appears", T('$5!=120 \\quad 6!=720 \\quad 7!=5040$', size=38)),
        A("'b!/a! = a run of neighbors' appears", T('$\\dfrac{b!}{a!}$ = a run of neighbors, from $a+1$ to $b$', size=38)),
        A("'Sum: take out the smaller factorial' appears", T('Sum or difference: take out the smaller factorial', size=38)),
        A("'Divisible? Break into primes' appears", T('Divisible? Break every factor into primes', size=38)),
        "A factorial is a number times the factorial just below it. Everything on this list comes from that.",
        D('Circle "Plug in"'),
        "Plugging in is fast. The math tells you why. Use both.",
    ])
    M.set_sidebar(FL, ['Stop early', 'Plug in first', 'The math', 'Not one factorial', 'Know them by sight',
                       'A run of neighbors', 'Sums of factorials', 'Factorials and primes', 'Recap'])
    M.slide(FL, 10)['active'] = 8

    # guided question
    g = 'q-r26-t28-28'
    M.new_q(g, TOPIC, '$\\dfrac{10!-9!}{8!}=?$', ['$9$', '$81$', '$90$', '$\\frac{1}{8!}$'], 2, [
        'Take out the smaller factorial: $10!=10\\cdot9!$, so $10!-9!=9!\\cdot(10-1)=9\\cdot9!$.',
        '$\\frac{9\\cdot9!}{8!}=9\\cdot\\frac{9!}{8!}=9\\cdot9=81$.',
        'Or write both in terms of $8!$: $10!=90\\cdot8!$ and $9!=9\\cdot8!$. So $\\frac{90\\cdot8!-9\\cdot8!}{8!}=90-9=81$.',
        'The traps: $90=\\frac{10!}{8!}$ forgets the $-9!$. $\\frac{1}{8!}$ comes from the wrong rule $10!-9!=(10-9)!$.'])
    M.place_q(g, ADV, after=FL)
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=[
        "Factorials with a minus sign. Don't calculate them.",
        "Take out the smaller one."])]
    for title, script in [
        ('Method 1 · Take out the smaller factorial', [
            "Ten factorial minus nine factorial. The smaller one is nine factorial.",
            D('Write "10! = 10 · 9!"'),
            "Ten factorial is ten times nine factorial.",
            D('Write "10! − 9! = 9! · (10 − 1) = 9 · 9!"'),
            "Take out nine factorial. Ten minus one stays inside: nine.",
            D('Write "9 · 9! ÷ 8! = 9 · 9 = 81"'),
            "Now divide by eight factorial. Nine factorial over eight factorial is just nine. Nine times nine: eighty-one.",
            D('Circle choice 2'),
            "Choice two.",
            "Ninety forgets the minus nine factorial. And one over eight factorial comes from subtracting inside the exclamation mark — never do that.",
        ]),
        ('Method 2 · Everything in eight factorials', [
            "Another way: write everything with eight factorial.",
            D('Write "10! = 10 · 9 · 8! = 90 · 8!     9! = 9 · 8!"'),
            "Ten factorial is ninety eight-factorials. Nine factorial is nine of them.",
            D('Write "(90 − 9) · 8! ÷ 8! = 81"'),
            "Ninety minus nine: eighty-one eight-factorials. Divide by eight factorial: eighty-one.",
        ])]:
        beats.append(dict(mode='question', active=SB_ADV.index('Question %d' % n), title=title, pre=[Q(g)], script=script))
    v = M.new_video('solve-' + g, TOPIC, 'Advanced Counting', SB_ADV, beats, ADV, kind='solution', qid=g)
    v['beats'][0]['title'] = 'Advanced Counting'
    v['hybrid']['num'] = 51
    v['hybrid']['title'] = 'Advanced Counting'
    v['title'] = v['navLabel'] = M.q(g)['stem']


def elite_factorials_late(M):
    R = 'q-r26-t28-'
    M.new_q(R + '31', TOPIC, '$\\dfrac{720+5040}{6!}=?$', ['$7$', '$8$', '$13$', '$42$'], 2, [
        'Know them by sight: $720=6!$ and $5040=7!=7\\cdot6!$.',
        'Take out $6!$: $\\frac{6!\\cdot(1+7)}{6!}=1+7=8$.',
        'The trap $7$ forgets the $1$ (the $6!$ itself).'])
    M.new_q(R + '29', TOPIC, '$x$ and $y$ are positive integers, and $x>y$.\nGiven: $\\frac{x!}{y!}=110$.\n'
            'Which of the following could be the value of $x+y$?', ['$21$', '$20$', '$19$', '$22$'], 2, [
        '$\\frac{x!}{y!}$ is a run of neighbors, from $y+1$ up to $x$.',
        '$110=10\\cdot11$: the run is $10$, $11$. It starts right after $y$, so $y=9$, and it ends at $x=11$. $x+y=20$.',
        'Check: $\\frac{11!}{9!}=11\\cdot10=110$ ✓. (A run of one number also works: $x=110$ and $y=109$, but $219$ is not among the choices.)',
        'The trap $21$ takes $y=10$. The run starts AFTER $y$.'])
    M.new_q(R + '30', TOPIC, 'What is the largest integer $k$ for which $9!$ is divisible by $2^k$?',
            ['$4$', '$5$', '$7$', '$8$'], 3, [
        '$9!=9\\cdot8\\cdot7\\cdot6\\cdot5\\cdot4\\cdot3\\cdot2\\cdot1$. Count the 2s in each factor.',
        '$8=2^3$: three. $6=2\\cdot3$: one. $4=2^2$: two. $2$: one. In all, $3+1+2+1=7$.',
        'So $9!=2^7\\cdot2835$, and $2835$ is odd. $9!$ is divisible by $2^7$, but not by $2^8$.',
        'The trap $4$ counts the even numbers, not the 2s.'])
    M.place_q(R + '31', PRAC, after='wp28-p02')
    M.place_q(R + '29', PRAC, after=R + '31')
    M.place_q(R + '30', PRAC, after=R + '29')

    # advanced card: factorial algebra rows
    rows = M.card('mem-counting-advanced')['tables'][0]['rows']
    k = next(i for i, r in enumerate(rows) if r[0] == 'Factorial') + 1
    rows[k:k] = [
        ['Know by sight', '$5!=120$, $6!=720$, $7!=5040$', '$a!=6\\cdot20=120\\to a=5$'],
        ['Run of neighbors', '$\\frac{b!}{a!}=(a+1)\\cdots b$', '$\\dfrac{b!}{a!}=56=7\\cdot8$: $a=6$, $b=8$'],
        ['Sum of factorials', 'take out the smaller factorial', '$6!+8!=6!\\cdot(1+56)=6!\\cdot57$'],
        ['Primes in $n!$', 'break every factor into primes, count each prime', '$7!=2^4\\cdot3^2\\cdot5\\cdot7$'],
    ]

    # summary: one slide after 'Repetition and rows'
    V = 'r26-t28-summary'
    M.insert_slides(V, 3, [dict(mode='concept', active=2, title='Factorial algebra', script=[
        A('5!, 6!, 7! appear', T('$5!=120 \\qquad 6!=720 \\qquad 7!=5040$', size=44, gap=20)),
        "Know them by sight. See 720? Think six factorial.",
        A('b!/a! = run appears', T('$\\dfrac{b!}{a!}=(a+1)\\cdots b \\qquad \\dfrac{9!}{6!}=7\\cdot8\\cdot9$', size=44, gap=20)),
        "A big factorial over a small one: a run of neighbors.",
        A('Sum appears', T('$7!+8!=7!\\cdot(1+8)=7!\\cdot9$', size=44, gap=20)),
        "A sum or a difference: take out the smaller factorial. Don't forget the one.",
        A('Primes appear', T('$6!=2^4\\cdot3^2\\cdot5$', size=44)),
        "Divisible by? Break every factor into primes, and count.",
    ])])
    sb = list(M.video(V)['hybrid']['sidebar'])
    sb.insert(2, 'Factorial algebra')
    M.set_sidebar(V, sb)
    for n in range(2, len(M.video(V)['beats']) + 1):
        M.slide(V, n)['active'] = n - 2


# =========================================================================================================
# 2026-10-05 cut repeats: each lesson back to a short intro (Hebrew style); every idea a question video
# right after it already teaches is cut from the lesson; ideas no question teaches stay, or move as one
# line + board item into the question video that uses them.
# =========================================================================================================
def _add_line(M, vid, n, before_say, line, item=None, label=None):
    """Insert one spoken line (+ optional board item) right before the line containing `before_say`
    (before_say=None: at the end of the slide)."""
    b = M.slide(vid, n); script = []; hit = False
    add = ([A(label, item)] if item is not None else []) + [line]
    for l in b['lines']:
        if before_say is not None and not hit and before_say in (l.get('say') or l.get('draw') or l.get('label') or ''):
            script += add; hit = True
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        else: script.append(D(l['draw']))
    if before_say is None:
        script += add; hit = True
    assert hit, '%s #%d: not found: %s' % (vid, n, before_say)
    M.set_slide(vid, n, script=script)


def _keep_slides(M, vid, keep, sidebar):
    """Keep only the slides `keep` (1-based); set the sidebar; renumber 'active' of the non-title slides."""
    v = M.video(vid)
    M.remove_slides(vid, [k for k in range(1, len(v['beats']) + 1) if k not in keep])
    a = 0
    for b in v['beats']:
        if b.get('mode') != 'title':
            b['active'] = a; a += 1
    M.set_sidebar(vid, sidebar)


def _short_intro(M, vid, title_lines, title, item, label, lines):
    """Hebrew-style short intro: title slide with 1-2 framing lines + one concept slide (one board item)."""
    M.set_slide(vid, 1, script=title_lines)
    M.insert_slides(vid, 1, [dict(mode='concept', title=title, active=0, pre=[],
                                  script=[A(label, item)] + lines)])
    M.set_sidebar(vid, [title])


def cut_repeats(M):
    # ---- Counting Possibilities: title + "Different results" + "Type 1: list it" ---------------
    _keep_slides(M, 'wp-123', [1, 3, 4], ['Different results', 'Type 1: list it'])
    # "What is counting?" repeated the title slide; Recap cut.

    # ---- Multiply the Choices: title only (Hebrew teaches it inside the meal question) ----------
    vid = 'wp-124-after'
    _keep_slides(M, vid, [1], [])
    _short_intro(M, vid, [
        "In most counting questions on the exam we won't list and count.",
        "We use a faster technique: multiplying the possibilities."],
        'Stages of choice', T(r'Count the options at each stage $\to$ multiply', 40),
        "'Count the options at each stage → multiply' appears",
        ["A stage of choice is simply a moment where you have to pick something.",
         "Let's see how it works in two questions."])
    # Stages / why multiply / order doesn't matter -> Q2 meal; dependent choices (x 1) -> Q3 code.

    # ---- With or Without Repetition: title + "The pool" (the Hebrew intro) ---------------------
    vid = 'wp-127'
    _keep_slides(M, vid, [1, 2], ['The pool'])
    _add_line(M, vid, 2, None, "Three questions next: a code with repeats, a code without, and a row.")
    _add_line(M, 'solve-wp28-g128', 2, None,
              "Same with numbers: a three-digit number may repeat digits — four four four counts.",
              T('$444$ is a three-digit number', 36), "'444 is a three-digit number' appears")
    _add_line(M, 'solve-wp28-g130', 2, 'Six items in a row: six factorial ways',
              "The exclamation mark is called factorial: the number times every whole number below it, down to one.",
              T(r'$n!=n\cdot(n-1)\cdots2\cdot1$', 36), "'n! = n · (n − 1) ⋯ 2 · 1' appears")

    # ---- Mutual Action: title only (the Hebrew intro) ----------------------------------------
    vid = 'wp-131'
    _keep_slides(M, vid, [1], [])
    _short_intro(M, vid, [
        "Mutual action: an action between two things at the same time — like a handshake.",
        "It's quite common on the exam, so understand it well."],
        'Mutual action', T(r'$A$–$B$ is the same link as $B$–$A$', 40),
        "'A–B is the same link as B–A' appears",
        ["When A shakes B's hand, B shakes A's hand. One handshake — and it's easy to count it twice.",
         "Let's see it in two questions."])
    _add_line(M, 'solve-wp28-g132', 2, None,
              "Spot it on the exam: handshakes, two-way routes, games between two, diagonals.",
              T('Handshakes · routes · games · diagonals', 36), "'Handshakes · routes · games · diagonals' appears")
    _add_line(M, 'solve-wp28-g132', 2, None,
              "But with roles — a president and a secretary — A-then-B and B-then-A really are different. Then don't halve.",
              T("Different roles? Don't halve", 36), "'Different roles? Don't halve' appears")
    _add_line(M, 'solve-wp28-g133', 2, 'The simplest way: draw it and count.',
              "A diagonal joins two vertices that are not next to each other.")

    # ---- Factorial Expressions (elite addition): cut only "Sums" and Recap ----------------------
    vid = 'wp-140-after'
    _keep_slides(M, vid, [1, 2, 3, 4, 5, 6, 7, 9],
                 ['Stop early', 'Plug in first', 'The math', 'Not one factorial', 'Know them by sight',
                  'A run of neighbors', 'Factorials and primes'])
    _add_line(M, vid, 8, None, "Next, a question with a minus sign: take out the smaller factorial.")
    _add_line(M, 'solve-q-r26-t28-28', 2, 'Now divide by eight factorial',
              "Same with a plus: five factorial plus six factorial is five factorial times one plus six. Don't forget the one.",
              T(r'$5!+6!=5!\cdot(1+6)$', 36), "'5! + 6! = 5! · (1 + 6)' appears")

    # ---- Forced Digits: the two worked examples stay (no question teaches them); Recap cut ------
    _keep_slides(M, 'wp-141-after', [1, 2, 3], ['All digits the same', 'First = last'])
    _add_line(M, 'wp-141-after', 3, None, "Count each free choice once. Give every forced position a one.")

    # ---- Boxes and "At Least One": title + "Quick checks" ---------------------------------------
    vid = 'r26-t28-cases'
    _keep_slides(M, vid, [1, 4], ['Quick checks'])
    _add_line(M, vid, 2, None, "Two questions next — at least once, and objects into boxes.")
    _add_line(M, 'solve-q-r26-t28-04', 2, 'Write "all: 10',
              "Why? The opposite of 'at least once' is 'none' — and none is one easy count.")

    # ---- Together, Apart and Repeats: title only -----------------------------------------------
    vid = 'r26-t28-arrange'
    _keep_slides(M, vid, [1], [])
    _short_intro(M, vid, ["Rows with a rule.", "Each rule changes how we count — and each one has its own trick."],
        'Four rules', T('Together · apart · repeats · round table', 40),
        "'Together · apart · repeats · round table' appears",
        ["People who must stand together — or apart. Items that repeat. And a round table.",
         "Four questions — one for each."])
    _add_line(M, 'solve-q-r26-t28-09', 2, 'Round table: fix one item',
              "Why? Turning the whole table changes no one's neighbors. So n items around a table: n minus one, factorial.",
              T(r'$n$ around a table: $(n-1)!$', 36), "'n around a table: (n − 1)!' appears")


# =====================================================================================
# 2026-10-06 new exam methods (teacher-approved). Nothing in topic 28 is recorded.
# 1. Pointer slide in the intro: "at most / at least / necessarily / impossible" = the Topic 21 min/max method.
# 2. Groups with no names (pairs): card row + one practice question. (The Pass-2 slide/guided question stay removed.)
# =====================================================================================
def add_methods(M):
    vid = 'wp-123'
    M.insert_slides(vid, 2, [dict(mode='concept', active=1, title='At most? At least?', script=[
        'Before we start — a warning that saves time.',
        A("'At most · at least · necessarily · impossible → Topic 21' appears",
          T(r'"At most", "at least", "necessarily", "impossible" $\to$ the Topic 21 min/max method', size=40, gap=50)),
        'About half of the exam\'s counting questions ask: at most how many? At least how many? What must be true? What is impossible?',
        'Those are not counting. They are the minimum and maximum questions from Topic 21: push to the extreme.',
        A("'8 friends, 30 candies' appears", T(r'$8$ friends share $30$ candies. Each gets at least $2$. At most how many can one friend get?', size=38, gap=50)),
        'To make one share as big as possible, give the others as little as possible.',
        D('Write "others: 7 × 2 = 14 → one friend: 30 − 14 = 16"'),
        'Seven friends get two each — fourteen. Sixteen are left for one friend.',
        'See those words? Use the Topic 21 method. Everything else — we count.'])])
    sb = M.video(vid)['hybrid']['sidebar']
    M.set_sidebar(vid, [sb[0], 'At most? At least?'] + sb[1:])
    for b in M.video(vid)['beats'][3:]:
        if b['mode'] == 'concept': b['active'] += 1

    # ---- groups with no names: card row ----
    c = M.card('mem-counting')
    rows = next(t for t in c['tables'] if t.get('title') == 'Which rule?')['rows']
    k = next(i for i, r in enumerate(rows) if r[0].startswith('A group, order')) + 1
    rows.insert(k, ['Groups with no names (pairs, unnamed teams)',
                    'count as if the groups had names, then $\\div$ (number of groups)$!$ · pairs: fix one person, choose her partner',
                    '4 girls into 2 pairs: $\\frac{6}{2!}=3$ (not $6$) · 6 players into 3 pairs: $5\\cdot3\\cdot1=15$'])

    # ---- practice question ----
    qid = 'q-r26-t28-41'
    M.new_q(qid, TOPIC,
            'A coach splits 8 runners into 4 pairs for training. The pairs have no names and no order. '
            'In how many different ways can the coach split the runners?',
            ['28', '105', '420', '2,520'], 2,
            ['Fix one runner and choose her partner: $7$ options. Take the next runner without a partner: $5$ options. Then $3$, then $1$.',
             '$7\\times5\\times3\\times1=105$.',
             'Check: with names (pair 1, pair 2, pair 3, pair 4): $\\frac{8\\times7}{2}\\times\\frac{6\\times5}{2}\\times\\frac{4\\times3}{2}\\times1=28\\times15\\times6=2{,}520$. '
             'The pairs have no names, so divide by $4!=24$: $\\frac{2{,}520}{24}=105$.',
             'Traps: $2{,}520$ treats the pairs as named; $28$ counts only one pair.'])
    M.place_q(qid, 'wp28-practice', after='wp28-p27')


# =====================================================================================
# 2026-10-06 practice: new methods (runs LAST). Extra method lines appended to practice
# explanations, using the course names of the 2026-10-06 methods.
# =====================================================================================

def _pm_add(M, qid, lines):
    """Append extra-method lines to a PRACTICE question explanation (existing lines kept)."""
    sec = M.section_of(qid)
    assert sec.endswith("-practice"), (qid, sec)
    ex = list(M.q(qid).get("explanation") or [])
    if any(l in ex for l in lines): return
    M.set_q(qid, expl=ex + list(lines))


def practice_methods(M):
    _pm_add(M, 'wp28-p13', [r'"At most" → this is the Topic 21 min/max method, not a counting formula. Worst luck: every cupboard opens only with the last key still possible: $6+5+4+3+2+1=21$ tests.'])
    _pm_add(M, 'wp28-p27', [r'Groups with no names? Here the teams DO have names (Cedar and Maple), therefore we do not divide. With two unnamed teams it would be $20\div2!=10$, the trap in choice 4.'])


# =====================================================================================
# 2026-10-06 renumber pass (runs LAST). The English course must not look like the Hebrew one:
# every Hebrew-derived question (guided wp28-g124 ... g144, practice wp28-p01 ... p20) gets new
# numbers and a new story; idea, trap, level and methods stay. Solution videos rewritten to match.
# Hebrew-derived lesson examples renumbered. Safe reorder. Practice clean-up (copies, extras, Sept).
# Nothing in Topic 28 is recorded (checked ~/Documents/Course.recordings 2026-10-06).
# =====================================================================================
RN_RECORDED = set()   # recorded question / video ids would go here and keep their old version


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED or qid not in M.D['questions']:
        return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, intro, slides):
    """Rewrite a guided solution video: title-slide lines + every question slide (2, 3, ...)."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED or qid in RN_RECORDED:
        return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']), len(slides))
    t0 = v['beats'][0]['title']
    M.set_slide(vid, 1, script=list(intro))
    v['beats'][0]['title'] = t0
    for n, (title, script) in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, title=title, script=script)


def _grid(rows, cols):
    return {'k': 'vis', 'v': {'type': 'choiceGrid', 'rows': rows, 'cols': cols}, 'w': 1000, 'h': 300, 'y': 300}


def rn_guided(M):
    S = lambda qid, stem, ch, cor, ex: _rn_q(M, qid, stem, ch, cor, ex)
    V = lambda qid, intro, slides: _rn_video(M, qid, intro, slides)
    Q_ = lambda qid: M.q(qid)

    # ---- g124: digits 2, 4, 6, 8 increasing  ==>  3, 5, 6, 9 increasing (4)
    S('wp28-g124', 'How many three-digit numbers can be made from the digits 3, 5, 6 and 9 if the hundreds digit is '
                   'smaller than the tens digit and the tens digit is smaller than the units digit?',
      ['6', '24', '4', '12'], 3, [
          'List in order, smallest first. Hundreds digit $3$: $356$, $359$, $369$. Hundreds digit $5$: $569$. '
          'Hundreds digit $6$ or $9$: there are not enough bigger digits left.',
          'Total: $4$ numbers.',
          'Check: each number uses $3$ of the $4$ digits, in increasing order. So we only choose the $1$ digit that is '
          'left out: $4$ ways.'])
    V('wp28-g124', ["Our first counting question.", "Trial and error. Let's list."], [
        ('Method 1 · List and check', [
            "No formula needed. We simply check.",
            "We only have the digits three, five, six and nine — and each digit must be bigger than the one before.",
            D('Write "356"'),
            "Start with three in front. Three five six: five is bigger than three, six bigger than five. Works.",
            D('Write "359" and "369"'),
            "Three five nine. Three six nine. Both work.",
            D('Write "569"'),
            "Five in front: only five six nine.",
            "Six or nine in front? Not enough bigger digits left to finish.",
            D('Circle choice 3'),
            "Four numbers. Choice three. What did we do? We counted and checked.",
        ]),
        ('Method 2 · Leave one digit out', [
            "Here's a neat check. Any three of the four digits can go up in exactly one way.",
            "So choosing the number is the same as choosing the one digit that's left out.",
            D('Write "4 digits to leave out → 4"'),
            "Four digits to leave out — four numbers.",
        ]),
    ])

    # ---- g125: café 4 fillings x 6 drinks  ==>  food truck 7 soups x 3 breads (21)
    S('wp28-g125', 'A food truck offers 7 soups and 3 kinds of bread. A lunch contains one soup and one kind of bread. '
                   'How many different lunches are possible?',
      ['10', '21', '49', '9'], 2, [
          'Two stages: a soup ($7$ options) and a bread ($3$ options).',
          'Multiply: $7\\times3=21$ lunches.',
          'Adding, $7+3=10$, counts menu items, not lunches.'])
    Q_('wp28-g125')['solutionVisual'] = {'type': 'choiceGrid', 'rows': 7, 'cols': 3, 'rowLabel': 'Soup', 'colLabel': 'Bread'}
    V('wp28-g125', ["Stages of choice — then multiply."], [
        ('Method 1 · Multiply the stages', [
            "Two stages of choice. Stage one: a soup.",
            D('Write "soup: 7"'),
            "Seven soups — seven options. Write the number of options for each stage.",
            D('Write "bread: 3"'),
            "Stage two: the bread — three options.",
            D('Write "7 × 3 = 21"'),
            "Multiply: twenty-one.",
            "Why multiply? Pick the first soup — it goes with any of the three breads: three lunches. "
            "The second soup, three more. Three for each of the seven soups.",
            D('Circle choice 2'),
            "Twenty-one. Choice two.",
        ]),
        ('Method 2 · The grid', [
            "The same count as a picture: one row per soup, one column per bread.",
            A('A 7 × 3 choice grid appears', _grid(7, 3)),
            "Every lunch is exactly one cell — one soup, one bread.",
            D('Shade one cell and write "1 lunch"'),
            "Seven rows of three — or three columns of seven. Soup first or bread first, the order doesn't matter. Twenty-one.",
            "Adding seven plus three would count menu items, not lunches.",
        ]),
    ])

    # ---- g126: two-digit code, digit sum 12 (7)  ==>  locker number, digit sum 14 (5)
    S('wp28-g126', 'A locker number has two digits, each from 0 to 9. The sum of the two digits must be 14. '
                   'How many locker numbers are possible?',
      ['10', '25', '5', '4'], 3, [
          'First digit: it must be at least $5$ (otherwise the second digit would have to be more than $9$). '
          'So $5, 6, 7, 8, 9$: $5$ options.',
          'Second digit: it must be $14$ minus the first digit. It is forced: $1$ option.',
          '$5\\times1=5$ locker numbers: $59$, $68$, $77$, $86$, $95$.'])
    V('wp28-g126', ["Careful — here one choice depends on another."], [
        ('Method 1 · Stages, with dependence', [
            "Two stages: a first digit and a second digit. Digits zero to nine, and they must add up to fourteen.",
            "First digit: can it be zero? Zero plus what makes fourteen? Fourteen — that's not a digit, it's a number.",
            D('Write "0 ✗  1 ✗  2 ✗  3 ✗  4 ✗"'),
            "One would need thirteen. Two, twelve. Three, eleven. Four, ten. Not digits. "
            "So the first digit is five up to nine.",
            D('Write "first: 5 options"'),
            "Five options.",
            "Now say we picked six. What completes it to fourteen? Only eight. Picked nine? Only five.",
            D('Write "second: 1 option"'),
            "Whatever we picked first, exactly one digit completes it. The second choice depends on the first.",
            D('Write "5 × 1 = 5"'),
            "Five times one: five.",
            D('Circle choice 3'),
            "Choice three.",
            "This is where people slip: they say five options, then five again — twenty-five. "
            "No — the second stage has one option.",
        ]),
        ('Method 2 · List them', [
            "Short enough to check by listing.",
            D('Write "59, 68, 77, 86, 95"'),
            "Fifty-nine and ninety-five are different locker numbers — position matters. "
            "Seventy-seven is allowed and counted once.",
            "Five locker numbers.",
        ]),
    ])

    # ---- g128 / g129: symbols A-F, 3 positions (216 / 120)  ==>  suitcase lock, digits 1-9, 3 wheels (729 / 504)
    S('wp28-g128', 'A suitcase lock has three wheels. Each wheel shows one of the digits 1 to 9, and digits may repeat. '
                   'How many codes are possible?',
      ['504', '729', '27', '81'], 2, [
          'Digits may repeat, so the pool stays the same: $9$ options for each wheel.',
          '$9\\times9\\times9=729$. Codes like $777$ and $373$ are included.'])
    V('wp28-g128', ["With repetition — or without?"], [
        ('Method 1 · The pool stays full', [
            "The pool: nine digits, one to nine. And digits may repeat.",
            D('Under the question write "9 × 9 × 9"'),
            "First wheel: nine options. Say we picked four. It goes right back into the pool.",
            "Second wheel: nine options again. Third: nine again.",
            D('Write "= 729"'),
            "Nine times nine is eighty-one, times nine — seven hundred twenty-nine.",
            D('Circle choice 2'),
            "Choice two. And codes like seven-seven-seven are included.",
            A("'444 is a three-digit number' appears", T('$444$ is a three-digit number', size=36)),
            "Same with numbers: a three-digit number may repeat digits — four four four counts.",
        ]),
    ])
    S('wp28-g129', 'A suitcase lock has three wheels. Each wheel shows one of the digits 1 to 9, and no digit may '
                   'appear twice. How many codes are possible?',
      ['729', '84', '27', '504'], 4, [
          'No digit may repeat, so the pool shrinks: $9$, then $8$, then $7$.',
          '$9\\times8\\times7=504$.',
          'Compare with the previous question: the same digits, but $9\\times9\\times9$ became $9\\times8\\times7$.',
          'We do not divide by anything: $123$ and $213$ are different codes ($\\frac{504}{6}=84$ is the trap).'])
    V('wp28-g129', ["The same question — with one change."], [
        ('Method 1 · The pool shrinks', [
            "Exactly the same lock — but now no digit may appear twice.",
            "First wheel: nine options. Say we picked four. Four is out — it doesn't come back.",
            D('Under the question write "9 × 8 × 7"'),
            "Second wheel: eight left. Third wheel: seven left.",
            D('Write "= 504"'),
            "Nine times eight is seventy-two, times seven — five hundred four.",
            D('Circle choice 4'),
            "Choice four.",
            "Compare with the last question: same digits, but here the pool shrinks after every pick. "
            "Nine-nine-nine became nine-eight-seven.",
            "And we don't divide by anything — one-two-three and two-one-three are different codes.",
        ]),
    ])

    # ---- g130: 6 photographs in a row (720)  ==>  7 trophies in a glass cabinet (5040)
    S('wp28-g130', 'In how many different ways can 7 different trophies be placed in a row in a glass cabinet?',
      ['720', '5040', '2520', '49'], 2, [
          '$7$ trophies in a row: $7!=7\\times6\\times5\\times4\\times3\\times2\\times1=5040$.',
          'The last place has only $1$ trophy left: it is forced.'])
    V('wp28-g130', ["Items in a row."], [
        ('Method 1 · Stage by stage', [
            "Seven trophies, seven places in the row — seven stages.",
            D('Under the question write "7 × 6 × 5 × 4 × 3 × 2 × 1"'),
            "First place: any of the seven. That trophy is placed — it's out. Second place: six left. "
            "Then five, four, three, two.",
            "The last place: one trophy left. No choice at all.",
            D('Write "= 5040"'),
            "Seven times six, forty-two. Times five, two hundred ten. Times four, eight hundred forty. "
            "Times three, two thousand five hundred twenty. Times two, five thousand forty.",
            D('Next to it write "= 7!"'),
            A("'n! = n · (n − 1) ⋯ 2 · 1' appears", T('$n!=n\\cdot(n-1)\\cdots2\\cdot1$', size=36)),
            "The exclamation mark is called factorial: the number times every whole number below it, down to one.",
            "That's seven factorial. Seven items in a row: seven factorial ways.",
            D('Circle choice 2'),
            "Choice two.",
        ]),
    ])

    # ---- g132: 5 islands, ferry routes (10)  ==>  6 towns, bus lines (15)
    S('wp28-g132', 'Six towns are connected so that every pair of towns has exactly one direct two-way bus line. '
                   'How many bus lines are there?',
      ['15', '30', '12', '6'], 1, [
          'Count in order: the line leaves from one of $6$ towns and goes to one of the $5$ others: $6\\times5=30$.',
          'A line from A to B is the same line as from B to A, so every line was counted twice: $\\frac{30}{2}=15$.',
          'Check: $5+4+3+2+1=15$.'])
    Q_('wp28-g132')['solutionVisual'] = {'type': 'network', 'nodes': 6}
    V('wp28-g132', ["Mutual action."], [
        ('Method 1 · Count, then halve', [
            "A bus line is two-way. Let's count as usual.",
            "Stage one: the town it leaves from — six options.",
            D('Write "from: 6"'),
            "Stage two: where it arrives — not the same town. Five options.",
            D('Write "to: 5" and "6 × 5 = 30"'),
            "Thirty. It's even among the choices — but something's off.",
            "A to B and B to A — that's the same line, just there and back. We counted every line twice.",
            D('Write "30 ÷ 2 = 15"'),
            "Mutual action: divide by two. Fifteen.",
            D('Circle choice 1'),
            "Choice one.",
            A("'Handshakes · routes · games · diagonals' appears", T('Handshakes · routes · games · diagonals', size=36)),
            "Spot it on the exam: handshakes, two-way routes, games between two, diagonals.",
            A("'Different roles? Don't halve' appears", T("Different roles? Don't halve", size=36)),
            "But with roles — a president and a secretary — A-then-B and B-then-A really are different. Then don't halve.",
        ]),
        ('Method 2 · Descending list', [
            "A check. Draw all the lines between towns A to F.",
            A('A six-town network appears', {'k': 'vis', 'v': {'type': 'network', 'nodes': 6}, 'w': 1000, 'h': 380, 'y': 250}),
            D('Next to the picture write "5 + 4 + 3 + 2 + 1"'),
            "A has five lines. B adds four new ones — its line to A is already counted. C adds three, D two, E one.",
            D('Write "= 15"'),
            "Fifteen lines again.",
        ]),
    ])

    # ---- g133: heptagon (14)  ==>  octagon (20)
    S('wp28-g133', 'How many diagonals does an eight-sided polygon have?',
      ['28', '20', '8', '40'], 2, [
          'From each vertex: $8-3=5$ diagonals (not to itself and not to its two neighbors).',
          'Every diagonal is counted from both of its ends: $\\frac{8\\times5}{2}=20$.',
          'Or: all lines between the vertices, $\\frac{8\\times7}{2}=28$, minus the $8$ sides: $28-8=20$.'])
    Q_('wp28-g133')['solutionVisual'] = {'type': 'polygon', 'sides': 8, 'diagonals': True}
    V('wp28-g133', ["Diagonals — four ways."], [
        ('Method 1 · Draw and count', [
            "A diagonal joins two vertices that are not next to each other.",
            "The simplest way: draw it and count.",
            A('An eight-sided polygon with its diagonals appears',
              {'k': 'vis', 'v': {'type': 'polygon', 'sides': 8, 'diagonals': True}, 'w': 1000, 'h': 380, 'y': 230}),
            D('Number the gold diagonals one by one'),
            "Twenty. With eight sides it's already crowded — so let's see faster ways.",
        ]),
        ('Method 2 · All lines minus sides', [
            "Eight vertices. Lines between them are a mutual action.",
            D('Write "8 × 7 ÷ 2 = 28"'),
            "Pick a vertex — eight options. Draw a line to another — seven options. Divide by two: twenty-eight lines.",
            "But eight of those lines are the sides of the polygon, not diagonals.",
            D('Write "28 − 8 = 20"'),
            "Twenty-eight minus eight: twenty.",
        ]),
        ('Method 3 · Descending sum', [
            "From the first vertex: seven lines. From the next: six new ones. Then five, four, three, two, one.",
            D('Write "7 + 6 + 5 + 4 + 3 + 2 + 1 = 28"'),
            "Each time one fewer — that line already came from the vertex before. Twenty-eight.",
            D('Write "28 − 8 = 20"'),
            "Minus the eight sides: twenty again.",
        ]),
        ('Method 4 · The formula', [
            "And the formula: n times n minus three, over two.",
            D('Write "8 × (8 − 3) ÷ 2 = 8 × 5 ÷ 2 = 20"'),
            "Eight times five is forty. Over two: twenty.",
            "Forty is the trap — it counts every diagonal from both of its ends.",
            D('Circle choice 2'),
            "Four ways, one answer. Choice two.",
        ]),
    ])

    # ---- g135: 5 drinks, 4 snacks, cocoa -> biscuit (17)  ==>  6 hot drinks, 5 pastries, espresso -> croissant (26)
    S('wp28-g135', 'A breakfast stand offers 6 hot drinks and 5 pastries. A customer chooses one of each. If the drink '
                   'is espresso, the pastry must be a croissant; with any other drink, any pastry is allowed. '
                   'How many choices are possible?',
      ['25', '21', '26', '30'], 3, [
          'Case 1, espresso: the pastry must be a croissant. $1\\times1=1$.',
          'Case 2, another drink: $5\\times5=25$.',
          'The cases do not overlap, so add them: $1+25=26$.',
          'Check: all pairs, $6\\times5=30$, minus the forbidden pairs (espresso with the $4$ other pastries): $30-4=26$.'])
    V('wp28-g135', ["Adding possibilities — split into cases."], [
        ('Method 1 · Two cases, then add', [
            "Espresso forces a croissant. Any other drink — any pastry. So split into two cases.",
            D('Write "Case 1: espresso"'),
            "Case one: espresso. One option for the drink. And then the pastry must be a croissant — one option.",
            D('Write "1 × 1 = 1"'),
            "One possibility.",
            D('Write "Case 2: not espresso"'),
            "Case two: any other drink. Six drinks, minus espresso — five options. "
            "And any pastry — croissant included — five options.",
            D('Write "5 × 5 = 25"'),
            "Twenty-five.",
            D('Write "1 + 25 = 26"'),
            "Add the cases: twenty-six.",
            D('Circle choice 3'),
            "Choice three.",
            "Careful: the rule works one way. Espresso needs a croissant — but a croissant still goes with any other drink.",
        ]),
        ('Method 2 · All minus forbidden', [
            "Check it the other way. With no rule: six times five, thirty.",
            D('Write "6 × 5 = 30"'),
            "Forbidden: espresso with any of the four pastries that aren't croissants.",
            D('Write "30 − 4 = 26"'),
            "Thirty minus four: twenty-six.",
        ]),
    ])

    # ---- g136: red/blue dice, sum not 5 (32)  ==>  green/yellow dice, sum not 8 (31)
    S('wp28-g136', 'A green dice and a yellow dice each show a number from 1 to 6. How many ordered outcomes have a sum '
                   'different from 8?',
      ['33', '32', '31', '30'], 3, [
          'All outcomes: $6\\times6=36$.',
          'Sum $8$: $(2,6)$, $(3,5)$, $(4,4)$, $(5,3)$, $(6,2)$. That is $5$ outcomes. The colors make $(2,6)$ and '
          '$(6,2)$ different; $(4,4)$ is one outcome.',
          'All minus forbidden: $36-5=31$.'])
    V('wp28-g136', ["Subtracting possibilities."], [
        ('Method 1 · All minus forbidden', [
            "We could list every outcome whose sum isn't eight — long and messy. Much easier to work backwards.",
            D('Write "6 × 6 = 36"'),
            "All outcomes: six for the green die, six for the yellow. Thirty-six.",
            "Forbidden: sum eight. Two-six, three-five, four-four, five-three, six-two.",
            A('The dice grid appears with sum 8 highlighted',
              {'k': 'vis', 'v': {'type': 'dice', 'sides': 6, 'target': 8}, 'w': 1000, 'h': 300, 'y': 290}),
            D('Circle the five highlighted cells'),
            "Five outcomes. The colors matter: two on green, six on yellow is different from six on green, two on yellow. "
            "Four-four is just one outcome.",
            D('Write "36 − 5 = 31"'),
            "All minus forbidden: thirty-one allowed.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Method 2 · Count directly', [
            "A direct check. Green one: no yellow value makes eight — all six are fine.",
            D('Write "1 × 6 + 5 × 5 = 31"'),
            "Green two to six: exactly one yellow value makes eight — so five good ones each. Six plus twenty-five: thirty-one.",
        ]),
    ])

    # ---- g138: 8 children, teachers Maya / Alex, 4 each (70)  ==>  10 hikers, guides Lena / Omar, 5 each (252)
    S('wp28-g138', 'Ten hikers are split between two guides, Lena and Omar, with five hikers assigned to each guide. '
                   'How many different splits are possible?',
      ['126', '252', '504', '30,240'], 2, [
          'Choose Lena\'s $5$ hikers as if order mattered: $10\\times9\\times8\\times7\\times6$.',
          'The order inside the group does not matter, so divide by $5!=5\\times4\\times3\\times2\\times1$.',
          'Cancel: $\\frac{10\\times9\\times8\\times7\\times6}{5\\times4\\times3\\times2\\times1}=3\\times2\\times7\\times6=252$ '
          '($10$ cancels with $5\\times2$, $9\\div3=3$ and $8\\div4=2$).',
          'The other $5$ hikers go to Omar: $1$ option. The guides have names, so we do not divide by $2$ again '
          '($126$ is that trap).'])
    V('wp28-g138', ["Choosing a group — order doesn't matter.", "The last question of the set."], [
        ('Method 1 · Choose, then divide by 5!', [
            "Split ten hikers into two groups of five — each group with a different guide.",
            "Choose Lena's five as usual — as if order mattered.",
            D('Write "10 × 9 × 8 × 7 × 6"'),
            "First hiker: ten options. Then nine, eight, seven, six.",
            "But picking Rita first and Ben second — or Ben first — it's the same group.",
            "So divide by the internal arrangements of five hikers: five factorial.",
            D('Write the fraction "(10 × 9 × 8 × 7 × 6) / (5 × 4 × 3 × 2 × 1)"'),
            "Put it as a fraction. Now cancel — one step at a time.",
            D('Cross out 10 on top and 5 × 2 on the bottom'),
            "Five times two is ten. Ten over ten is one. Cross them out.",
            D('Cross out 9 on top and 3 on the bottom; write 3 above the 9'),
            "Nine over three is three.",
            D('Cross out 8 on top and 4 on the bottom; write 2 above the 8'),
            "Eight over four is two.",
            D('Write "= 3 × 2 × 7 × 6 = 252"'),
            "What's left: three times two times seven times six. Two hundred fifty-two.",
            "And Omar's group? No choice left — the five remaining hikers go to Omar.",
            D('Circle choice 2'),
            "Two hundred fifty-two. Choice two.",
        ]),
        ('Method 2 · No extra ÷2', [
            "Should we divide by two again? No.",
            "The guides have names. Hikers one to five with Lena is different from hikers one to five with Omar.",
            D('Write "named guides → keep 252"'),
            "Only if the two groups had no labels would swapping them change nothing — and then we'd halve, "
            "to one hundred twenty-six.",
        ]),
    ])

    # ---- g139: 7 of 8 (8)  ==>  11 of 12 (12)
    S('wp28-g139', 'In how many different ways can a team of 11 players be chosen from a squad of 12 players?',
      ['1', '12', '11', '66'], 2, [
          'Choosing $11$ of $12$ is the same as choosing the $1$ player who stays out: $12$ ways.',
          'The long way gives the same: $\\frac{12\\times11\\times10\\times\\cdots\\times2}{11!}=12$.'])
    V('wp28-g139', ["Choosing almost everyone.", "Complementary choice."], [
        ('Method 1 · Choose who stays out', [
            "Eleven out of twelve — that's n minus one out of n.",
            "Instead of choosing eleven players, choose the one who stays out.",
            D('Write "who stays out: 12 options"'),
            "Twelve players — twelve ways to leave one out. Each gives a different team.",
            D('Circle choice 2'),
            "Twelve. Choice two.",
        ]),
        ('Method 2 · The long way', [
            "The group method gives the same thing.",
            D('Write "12 × 11 × 10 × … × 2 ÷ 11!"'),
            "Choose eleven the usual way, then divide by eleven factorial — the internal arrangements.",
            D('Cancel 11 × 10 × … × 2 with 11! and write "= 12"'),
            "Everything from eleven down cancels. Twelve.",
            "Once you spot n minus one out of n, skip all this: the answer is n.",
        ]),
    ])

    # ---- g140: 7! / 5! (42)  ==>  9! / 7! (72)
    S('wp28-g140', 'What is the ratio of the number of row arrangements of 9 distinct objects to the number of row '
                   'arrangements of 7 distinct objects?',
      ['81', '72', '16', '63'], 2, [
          'The ratio is $\\frac{9!}{7!}=\\frac{9\\times8\\times7!}{7!}=9\\times8=72$.',
          'There is no need to calculate $9!=362{,}880$ and $7!=5040$ first.'])
    V('wp28-g140', ["The first advanced counting question.", "An easy one — and a quick refresh on factorials."], [
        ('Method 1 · Write it all out', [
            "Rows of nine objects, over rows of seven objects.",
            "How many ways to arrange n objects in a row? n factorial. We remember that.",
            D('Under the question write "9! / 7!"'),
            "So it's nine factorial over seven factorial.",
            "A factorial starts at the number and goes down by one each time, all the way to one.",
            D('Write "9·8·7·6·5·4·3·2·1" on top and "7·6·5·4·3·2·1" underneath'),
            "Nine, eight, seven, and on down to one — over seven, six, and on down to one.",
            D('Cross out 7·6·5·4·3·2·1 on top and bottom'),
            "Cancel everything the two share.",
            D('Write "= 9 · 8 = 72" and circle choice 2'),
            "Left with nine times eight: seventy-two. Choice two.",
        ]),
        ('Method 2 · Expand only as far as needed', [
            "Some students don't write all that. They shorten it — by understanding what a factorial is.",
            "Seven, six, five, and on down to one — that tail is just seven factorial.",
            D('Write "9! = 9 · 8 · 7!"'),
            "So nine factorial is nine, times eight, times seven factorial. Stop there.",
            D("Cross out the two 7!'s"),
            "Now the seven factorials cancel in one move.",
            D('Write "= 72" and circle choice 2'),
            "Nine times eight. Seventy-two — no need to calculate three hundred sixty-two thousand eight hundred eighty.",
        ]),
    ])

    # ---- g141: hundreds + units = 7 (70)  ==>  = 8 (80)
    S('wp28-g141', 'How many three-digit numbers have a hundreds digit and a units digit whose sum is 8?',
      ['90', '80', '8', '72'], 2, [
          'Most restricted position first: the hundreds digit. It is not $0$ and not more than $8$: $1$ to $8$, '
          'so $8$ options.',
          'Units digit: forced ($8$ minus the hundreds digit): $1$ option.',
          'Tens digit: free, $0$ to $9$: $10$ options.',
          '$8\\times10\\times1=80$.',
          'Check: the (hundreds, units) pairs are $(1,7)$, $(2,6)$, $(3,5)$, $(4,4)$, $(5,3)$, $(6,2)$, $(7,1)$, '
          '$(8,0)$. That is $8$ pairs, each with $10$ possible middle digits. ($90$ wrongly lets the number start with $0$.)'])
    V('wp28-g141', ["A digits question — and a really important idea hiding inside it."], [
        ('Method 1 · Option counts per digit', [
            "Three-digit numbers — so three positions: hundreds, tens, units.",
            "Tip: above each position write how many options it has; below, list what they are. Keeps you organized.",
            "Most restricted position first. The condition talks about the hundreds and the units. Start with the hundreds digit.",
            "Can it be anything? No. Hundreds plus units must be eight, so it can't go above eight.",
            "And it can't be zero — a number can't start with zero. There's no such number as zero-five-eight.",
            D('Above the hundreds position write "8" and below it "1–8"'),
            "So one to eight: eight options.",
            "Now the units digit. Here's the important idea: dependency.",
            "Once the hundreds digit is chosen, the units digit is already decided. It has to complete the sum to eight.",
            D('Above the units position write "1"'),
            "Hundreds is eight — units must be zero. Hundreds is three — units must be five. One option every time.",
            "And the tens digit? The condition doesn't mention it. It's free: zero to nine. Ten options.",
            D('Above the tens position write "10"'),
            D('Write "8 × 10 × 1 = 80" and circle choice 2'),
            "Eight times ten times one: eighty. Choice two.",
            "These questions aren't simple — and understanding that dependency is the key. More on it in a moment.",
        ]),
        ('Method 2 · List the outside pairs', [
            "Quick check from the other side.",
            D('Write the pairs "(1,7) (2,6) (3,5) (4,4) (5,3) (6,2) (7,1) (8,0)"'),
            "Hundreds and units pairs: one-seven, two-six, three-five, four-four, five-three, six-two, seven-one, "
            "eight-zero. Eight pairs.",
            "Zero-eight is out — it would only be a two-digit number. Counting it gives the trap, ninety.",
            D('Write "8 × 10 = 80"'),
            "Put any of ten digits in the middle of each pair. Eighty again.",
        ]),
    ])

    # ---- g142: 3, 4, 7, 8; B even  ==>  2, 5, 6, 9; A even (8)
    S('wp28-g142', 'The digits 2, 5, 6 and 9 go once each into a square: A and B on top, C and D below.\n'
                   'A is even.\n$C\\times D$ is even.\nHow many arrangements are possible?',
      ['12', '4', '8', '16'], 3, [
          'Most restricted first. A is even: $2$ or $6$, so $2$ options.',
          '$C\\times D$ is even only if C or D is even. The only other even digit must go to the bottom row, '
          'so B must be odd: $5$ or $9$, so $2$ options.',
          'The last two digits go into C and D in $2\\times1=2$ orders.',
          '$2\\times2\\times2\\times1=8$.',
          'Check: with A even there are $2\\times3!=12$ arrangements. The bad ones have the other even digit in B: '
          '$2\\times1\\times2=4$. $12-4=8$.'])
    Q_('wp28-g142')['solutionVisual'] = {'type': 'table', 'headers': ['A · even', 'B · odd'],
                                        'rows': [['C', 'D · bottom product even']]}
    V('wp28-g142', ["A hard one: digits in a square, with two conditions."], [
        ('Method 1 · Options per position', [
            A('The square appears: A B on top, C D underneath',
              {'k': 'vis', 'v': {'type': 'table', 'headers': ['A', 'B'], 'rows': [['C', 'D']]}, 'w': 520, 'h': 150}),
            "Four digits — two, five, six, nine — each used once.",
            "A is even. How many even digits do we have? Two: two and six.",
            D('Next to A write "2"'),
            "Two options for A.",
            "The bottom product can't be odd. When is a product odd? Only when BOTH factors are odd.",
            "So at least one of C and D must be even. And the other even digit is already up in A.",
            "Some students get stuck here — which bottom square gets the even one?",
            "Easier conclusion: B must be odd.",
            D('Next to B write "2"'),
            "B is odd: five or nine. Two options.",
            D('Next to C write "2" and next to D write "1"'),
            "Two digits left — no more restrictions. Two options, then one.",
            D('Write "2 × 2 × 2 × 1 = 8" and circle choice 3'),
            "Two times two times two times one: eight. Choice three.",
            "Notice: it's a square, not a row. Doesn't matter. Count the options at each stage and multiply.",
        ]),
        ('Method 2 · Trial and error', [
            "Not sure what to do? Try, and list — in an organized way.",
            A('An arrangements table appears with A = 2 filled in',
              {'k': 'vis', 'v': {'type': 'table', 'headers': ['A', 'B', 'C', 'D'],
                                 'rows': [['2', '', '', ''], ['2', '', '', ''], ['2', '', '', ''], ['2', '', '', '']]},
               'w': 640, 'h': 260}),
            "Anchor A at two. B must be odd.",
            D('Fill row 1: 2, 5, 6, 9 — row 2: 2, 5, 9, 6'),
            "B is five: six-nine, or swap to nine-six. Change as little as possible each time.",
            D('Fill row 3: 2, 9, 5, 6 — row 4: 2, 9, 6, 5'),
            "B is nine: five-six, or six-five. Four arrangements.",
            D('Next to the table write "A = 6 → 4 more"'),
            "Now swap A to six — exactly the same four patterns again. No need to draw them.",
            D('Write "4 × 2 = 8" and circle choice 3'),
            "Four plus four: eight.",
        ]),
        ('Method 3 · Subtract the failures', [
            "One more route: count with A even, then remove what breaks the bottom rule.",
            D('Write "2 × 3! = 12"'),
            "A in two ways, the other three digits in six orders: twelve.",
            D('Write "bad: other even in B → 2 × 2 = 4"'),
            "It fails only when the other even digit sits in B — then both bottom digits are odd. That's four arrangements.",
            D('Write "12 − 4 = 8"'),
            "Twelve minus four: eight. Same answer.",
        ]),
    ])

    # ---- g143: chess, 45 games (10)  ==>  table-tennis league, 66 matches (12)
    S('wp28-g143', 'In a table-tennis league, each pair of players plays exactly one match. There are 66 matches '
                   'altogether. How many players take part?',
      ['11', '13', '12', '9'], 3, [
          'With $n$ players, each pair plays once: $\\frac{n(n-1)}{2}=66$.',
          'Multiply by $2$: $n(n-1)=132$. Two consecutive numbers with product $132$: $12\\times11$. Therefore $n=12$.',
          'Check the other choices: $\\frac{13\\times12}{2}=78$, $\\frac{11\\times10}{2}=55$, $\\frac{9\\times8}{2}=36$.'])
    tot = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]
    Q_('wp28-g143')['solutionVisual'] = {'type': 'table', 'headers': ['Players', 'Matches'],
                                        'rows': [[str(k), str(t)] for k, t in zip(range(2, 13), tot)]}
    V('wp28-g143', ["Three ways to solve this one."], [
        ('Method 1 · The mutual-action formula', [
            "Each pair of players plays once. Does that remind you of something? Mutual action.",
            "Two teams playing each other, two people shaking hands — it's the same action seen from both sides.",
            "Choose the first player: n options. The opponent: n minus one.",
            "But when red plays black, black is playing red at the same time — same match, counted twice. So divide by two.",
            D('Write "n(n−1)/2 = 66"'),
            "Here we go backwards: they give the matches and ask for the players.",
            D('Write "n(n−1) = 132"'),
            "Multiply by two: n times n minus one is one hundred thirty-two.",
            "n and n minus one are consecutive. Which consecutive numbers multiply to one hundred thirty-two?",
            D('Write "12 · 11 = 132 → n = 12" and circle choice 3'),
            "Twelve and eleven. So twelve players. Choice three.",
        ]),
        ('Method 2 · Test the answers', [
            "The psychometric way: plug in the answers — still with the mutual-action formula.",
            D('Next to 13 write "13·12/2 = 78 ✗"'),
            "Thirteen players: thirteen times twelve over two — seventy-eight. Too many.",
            D('Next to 12 write "12·11/2 = 66 ✓" and circle choice 3'),
            "Twelve players: twelve times eleven over two — sixty-six. That's it.",
            "By the way, you can start from the middle to save a test: eleven gives fifty-five — too few — "
            "so nine is out too.",
            "But with numbers this friendly, just test them.",
        ]),
        ('Method 3 · A growing sequence', [
            "A less-known way — but it really shows what mutual action means.",
            A("A table appears: players 2 to 12, with 'new matches' and 'total' to fill",
              {'k': 'vis', 'v': {'type': 'table', 'headers': ['n'] + [str(k) for k in range(2, 13)],
                                 'rows': [['New'] + [''] * 11, ['Total'] + [''] * 11]}, 'w': 1000, 'h': 160}),
            "The top row, n, is the number of players. One player alone? No matches. Two players: one match.",
            D('Fill the table: new matches 1, 2, 3 … 11 and totals 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66'),
            "A third player adds two matches — one against each player already there. Total three.",
            "A fourth adds three: total six. Every newcomer plays everyone who was there before.",
            "Keep going… the twelfth player adds eleven matches. Total sixty-six.",
            D('Circle the 12 in the last column'),
            "Careful: the last added number is eleven, but it comes from the TWELFTH player. Twelve players. Choice three.",
            "On the exam, just write one plus two plus three… across the page. Whatever's comfortable for you.",
        ]),
    ])

    # ---- g144: 7 students, 6 tallest-to-shortest (7)  ==>  8 children, 7 shortest-to-tallest (8)
    S('wp28-g144', 'Eight children all have different heights. A photographer chooses seven of them and places them '
                   'in a row from shortest to tallest. How many different rows can be formed?',
      ['7', '5040', '8', '56'], 3, [
          'Choose the $1$ child who stays out: $8$ options.',
          'The other $7$ stand from shortest to tallest: only $1$ order.',
          '$8\\times1=8$. We do not multiply by $7!$: the height order is forced.'])
    V('wp28-g144', ["Medium-plus, maybe even hard. Two ways in."], [
        ('Method 1 · Trial and error', [
            "Label the heights one to eight — one the shortest.",
            "Now build rows of seven, always shortest to tallest. Work in order: only change the right end.",
            D('Write "1 2 3 4 5 6 7" and underneath "1 2 3 4 5 6 8"'),
            "One, two, three, four, five, six, seven. Then swap the seven for an eight.",
            "Keep moving the gap one place left each time…",
            A('The full list appears', T('$1234567,\\ 1234568,\\ 1234578,\\ 1234678,\\ 1235678,\\ 1245678,\\ '
                                         '1345678,\\ 2345678$', size=30)),
            D('Number the rows 1 to 8'),
            "No more options. Eight rows.",
            "We found eight. Seven is too few. Fifty-six and five thousand forty would need many more rows — "
            "and there are no more.",
            D('Circle choice 3'),
            "Eight. Choice three.",
        ]),
        ('Method 2 · Choose who stays out', [
            "There's a smarter way — a flash of insight: the complementary event.",
            "You're the photographer. Instead of choosing seven children and arranging them…",
            "…choose the ONE who stays out.",
            "\"You stay — everyone else, come here.\" And they line up shortest to tallest. Only one way.",
            D('Write "who stays out? 8 options"'),
            "Any of the eight children can be the one left out. Eight options.",
            D('Circle choice 3'),
            "Eight. Choice three.",
            "Complementary events aren't magic — they're a technique worth knowing. They'll help in plenty of questions.",
        ]),
    ])


def rn_lessons(M):
    # ---- Choosing a Group (wp-137) #2: "4 children out of 10, Danny / Yossi" (the Hebrew's) ==> 3 of 9, Lior / Sam
    M.set_slide('wp-137', 2, script=[
        "Choosing a group — first, know these are edge questions. Very hard, and very rare.",
        "We pick a smaller group from a bigger one. Three children out of nine, say.",
        "Picked Lior first and Sam second — or Sam first? They're both in the group either way.",
        A('The six orders of A, B, C appear', T('$ABC,\\ ACB,\\ BAC,\\ BCA,\\ CAB,\\ CBA$', size=50, gap=60)),
        D('Bracket all six and write "= 1 group"'),
        "Six different picking orders — one and the same group. That's a doubling we must remove.",
    ])
    # #4: "9 out of 10 -> 10 ways" (the Hebrew's) ==> 14 out of 15 -> 15 ways
    b = M.slide('wp-137', 4)
    assert '$9$ out of $10' in b['items'][1]['t'], b['items'][1]
    M.set_slide('wp-137', 4, script=[
        "The second type is simpler than it looks: choose who stays OUT.",
        A("'Choose n − 1 out of n → n ways' appears", T('Choose $n-1$ out of $n$ $\\to$ $n$ ways', size=46)),
        A("'14 out of 15 → 15 ways' appears", T('$14$ out of $15\\ \\to\\ 15$ ways', size=46)),
        "Choose all but one — and the answer is simply the total.",
        D('Next to it write "pick who stays OUT"'),
        "Why? Instead of choosing fourteen, choose the one who stays out. Fifteen people — fifteen choices.",
        A("'Choose k of n = choose the n − k who stay out' appears",
          T('Choose $k$ of $n$ = choose the $n-k$ who stay out', size=42)),
        "And it works for any number. Choosing eight of ten is the same as choosing the two who stay out.",
        D('Write "8 of 10 = 2 of 10 = (10 × 9) ÷ 2 = 45"'),
        "Two of ten: ten times nine, over two. Forty-five. Much faster than dividing by eight factorial.",
        "Always count the smaller side.",
    ])

    # ---- Forced Digits (wp-141-after): the Hebrew's "all digits the same" / "units = hundreds" ==> five-digit versions
    M.set_slide('wp-141-after', 2, pre=[T('Five-digit numbers whose digits are all the same: how many?', size=42, gap=80)],
                script=[
        "Five-digit numbers whose digits are all identical. How many?",
        "First digit: nine options. Anything but zero.",
        D('Above the first position write "9"'),
        "Second digit — nine options too? Well, it could be one in one-one-one-one-one, two in two-two-two-two-two…",
        "But that's not really true. Once the first digit is chosen, the rest MUST match it.",
        D('Above the other four positions write "1", "1", "1", "1"'),
        "Pick five first — the rest are five, five, five, five. One option each.",
        D('Write "9 × 1 × 1 × 1 × 1 = 9"'),
        "Nine numbers: one-one-one-one-one, two-two-two-two-two, up to nine-nine-nine-nine-nine. Not nine to the fifth.",
    ])
    M.set_slide('wp-141-after', 3, title='Mirror digits',
                pre=[T('Five-digit numbers that read the same both ways (first = last, second = fourth): how many?',
                       size=40, gap=80)],
                script=[
        "One more. The first digit equals the last, and the second equals the fourth. The middle digit is free.",
        D('Above the positions write "9", "10", "10", "1", "1"'),
        "First digit: nine. Second digit: no restriction at all — ten, including zero. The middle digit: ten more.",
        "The fourth must copy the second. The fifth must copy the first. One option each.",
        "Choosing the first digit really chooses two digits at once.",
        D('Write "9 × 10 × 10 × 1 × 1 = 900"'),
        "Nine hundred. And one-zero-zero-zero-one counts — so don't drop zero from the middle.",
        "Count each free choice once. Give every forced position a one.",
    ])
    M.set_sidebar('wp-141-after', ['All digits the same', 'Mirror digits'])

    # ---- Factorial Expressions: the first line quoted the old Q13 (7! = 7 · 6 · 5!) ==> the new one (9! = 9 · 8 · 7!)
    _say(M, 'wp-140-after', 2, 'seven factorial is seven times six times five factorial',
         'nine factorial is nine times eight times seven factorial')

    # ---- Summary: "3 x 5 = 15, shirts and hats" (the Hebrew's 3 salads x 5 drinks) ==> 5 x 4 = 20;
    #      "9!/7! = 72" is now Q13's answer ==> 8!/6! = 56 (the run-of-neighbors lesson example)
    V = 'r26-t28-summary'
    b = M.slide(V, 2)
    assert '3\\times5=15' in b['items'][0]['t']
    b['items'][0]['t'] = 'Stages of choice $\\to$ multiply: $5\\times4=20$'
    _say(M, V, 2, "Three shirts and five hats: fifteen outfits. Not eight",
         "Five shirts and four hats: twenty outfits. Not nine")
    b = M.slide(V, 3)
    assert '\\frac{9!}{7!}=9\\times8=72' in b['items'][2]['t']
    b['items'][2]['t'] = '$n$ items in a row: $n!$ $\\quad\\frac{8!}{6!}=8\\times7=56$'

    # ---- memory cards: examples follow the new numbers
    c = M.card('mem-counting')
    new_ex = {
        'Short list, no pattern': '$356,\\ 359,\\ 369,\\ 569$',
        'Stages of choice': '$7\\times3=21$',
        'Later choice depends on an earlier one': '$5\\times1=5$',
        'With repetition': '$9\\times9\\times9=729$',
        'Without repetition': '$9\\times8\\times7=504$',
        '$n$ items in a row': '$7!=5040$',
        'Mutual action (handshakes, routes, games)': '$\\frac{6\\times5}{2}=15$',
        'Diagonals of an $n$-gon': '$\\frac{8\\times5}{2}=20$',
        'Separate cases': '$1+25=26$',
        'A small forbidden set': '$36-5=31$',
        'A group, order does not matter': '$\\frac{10\\times9\\times8\\times7\\times6}{5!}=252$',
        '$n-1$ out of $n$': '$11$ of $12\\to12$',
    }
    rows = next(t for t in c['tables'] if t.get('title') == 'Which rule?')['rows']
    hit = set()
    for r in rows:
        if r[0] in new_ex:
            r[2] = new_ex[r[0]]; hit.add(r[0])
    assert hit == set(new_ex), set(new_ex) - hit
    c = M.card('mem-counting-advanced')
    new_ex = {
        'Factorial': '$\\frac{9!}{7!}=9\\cdot8=72$',
        'Forced position': 'digit sum 8: $8\\times10\\times1=80$',
        'Mutual action': '$12$ players $\\to66$ matches',
        'Complement': '7 of 8 in height order: $8$',
    }
    hit = set()
    for r in c['tables'][0]['rows']:
        if r[0] in new_ex:
            r[2] = new_ex[r[0]]; hit.add(r[0])
    assert hit == set(new_ex), set(new_ex) - hit
    t = next(t for t in c['tables'] if t.get('title', '').startswith('Pairs among n'))
    t['head'] = ['$n$'] + [str(k) for k in range(2, 13)]
    t['rows'] = [['Pairs'] + [str(k * (k - 1) // 2) for k in range(2, 13)]]


def rn_order(M):
    # Learn: the easy "11 of 12" before the hard group split (both taught in the lesson right before them).
    M.move('wp28-g139', LEARN, before='wp28-g138')
    M.move('solve-wp28-g139', LEARN, after='wp28-g139')
    # Advanced, after the Forced Digits lesson: medium-plus (games), medium-plus (heights), then the hard square.
    M.move('wp28-g143', ADV, before='wp28-g142')
    M.move('solve-wp28-g143', ADV, after='wp28-g143')
    M.move('wp28-g144', ADV, before='wp28-g142')
    M.move('solve-wp28-g144', ADV, after='wp28-g144')


def rn_practice_questions(M):
    S = lambda qid, stem, ch, cor, ex: _rn_q(M, qid, stem, ch, cor, ex)
    S('wp28-p01', 'Seven chess clubs hold a league. Each club plays every other club once. How many games are played?',
      ['21', '42', '14', '28'], 1, [
          'Each of the $7$ clubs has $6$ opponents: $7\\times6=42$.',
          'Every game was counted twice (once from each club): $\\frac{42}{2}=21$.'])
    S('wp28-p02', 'What is the prime-factor form of $3!\\times4!\\times5!$?',
      ['$2^6\\times3^3\\times5$', '$2^7\\times3^3\\times5$', '$2^7\\times3^2\\times5$', '$2^8\\times3^3$'], 2, [
          '$3!=2\\times3$, $4!=2^3\\times3$, $5!=2^3\\times3\\times5$.',
          'Add the exponents of each prime: $2^{1+3+3}\\times3^{1+1+1}\\times5=2^7\\times3^3\\times5$.'])
    S('wp28-p03', 'A florist has 5 kinds of white flower and 4 kinds of yellow flower. A bouquet uses two different '
                  'kinds of the same color. How many bouquets are possible?',
      ['16', '20', '36', '9'], 1, [
          'Two white kinds: $\\frac{5\\times4}{2}=10$. Two yellow kinds: $\\frac{4\\times3}{2}=6$.',
          'A bouquet is white or yellow (two separate cases), so add: $10+6=16$.'])
    S('wp28-p04', 'A gym gives each locker a different code made from the letters A, B, C, D and E, using each letter '
                  'exactly once. At most how many lockers can receive a code?',
      ['3125', '120', '60', '25'], 2, [
          'The first position has $5$ options, then $4$ remain, then $3$, $2$ and $1$.',
          'Multiply: $5\\times4\\times3\\times2\\times1=120$.'])
    S('wp28-p05', 'A signal is made of 3 flags in a row. Each flag is one of 7 colors, and colors may repeat. '
                  'How many signals are possible?',
      ['21', '210', '343', '2187'], 3, [
          'Colors may repeat: $7\\times7\\times7=343$.'])
    S('wp28-p06', 'A group of $n$ different dancers can line up in 24 different orders. What is $n$?',
      ['3', '4', '6', '12'], 2, [
          '$n$ dancers in a row: $n!$ orders.', '$4!=4\\times3\\times2\\times1=24$, so $n=4$.'])
    S('wp28-p07', 'Six different awards are given to six volunteers, one award per volunteer. In how many different '
                  'ways can this be done?',
      ['36', '30', '720', '120'], 3, [
          'The first award has $6$ possible volunteers. $5$ remain for the next award, then $4$, $3$, $2$ and $1$.',
          'The product is $6\\times5\\times4\\times3\\times2\\times1=720$.'])
    S('wp28-p08', 'A sports kit has a cap, a jersey and socks. Each item comes in 5 colors. A player chooses one of '
                  'each, with all three items in different colors. How many kits are possible?',
      ['15', '125', '60', '20'], 3, [
          'Cap: $5$ colors. Jersey: a different color, $4$ options. Socks: $3$ colors left.',
          '$5\\times4\\times3=60$.'])
    S('wp28-p09', 'A ticket code is one of 4 letters, followed by 3 different digits chosen from 1 to 8, in order. '
                  'How many ticket codes are possible?',
      ['336', '1344', '2048', '224'], 2, [
          'Letter: $4$ options. Three different digits in order: $8\\times7\\times6=336$.',
          'Total: $4\\times336=1344$.'])
    S('wp28-p10', 'Six cyclists finish a race with no ties. How many different ordered podiums of first, second and '
                  'third place are possible?',
      ['720', '20', '120', '216'], 3, [
          'First place: $6$ options, second: $5$, third: $4$. $6\\times5\\times4=120$.',
          'The order of the other three cyclists does not matter.'])
    S('wp28-p11', 'A lunch is either a main course, a side dish and a drink, or a soup and a drink. There are 4 main '
                  'courses, 3 side dishes, 3 soups and 2 drinks. How many different lunches are possible?',
      ['24', '144', '12', '30'], 4, [
          'Two separate cases. Main-course lunches: $4\\times3\\times2=24$. Soup lunches: $3\\times2=6$.',
          'Add: $24+6=30$.'])
    S('wp28-p12', 'At a reunion, every two guests shake hands once. There are 36 handshakes. How many guests are there?',
      ['8', '9', '18', '10'], 2, [
          'With $n$ guests: $\\frac{n(n-1)}{2}=36$, so $n(n-1)=72=9\\times8$. Therefore $n=9$.',
          'Check the other choices: $8$ guests give $28$, $10$ give $45$, $18$ give $153$.'])
    S('wp28-p13', 'Seven different keys each open exactly one of seven lockers in a gym. The matches are unknown. Using '
                  'information from failed tests and putting each used key aside, at most how many key tests are '
                  'needed to open every locker, counting each successful opening as a test?',
      ['21', '49', '28', '27'], 3, [
          'The first locker may need $7$ tests before it opens.',
          'Then $6$ unmatched keys remain for the next locker, then $5$, $4$, $3$, $2$ and $1$.',
          'Add them: $7+6+5+4+3+2+1=28$.',
          '"At most" → this is the Topic 21 min/max method, not a counting formula. Worst luck: every locker opens '
          'only with the last key still possible: $7+6+5+4+3+2+1=28$ tests.'])
    S('wp28-p14', 'Five singers must stand in the left part of a row, and three drummers in the right part. Everyone '
                  'is different. How many orders are possible?',
      ['720', '120', '1440', '40320'], 1, [
          'Singers in the left part: $5!=120$ orders. Drummers in the right part: $3!=6$ orders.',
          'The parts cannot change sides, so $120\\times6=720$.'])
    S('wp28-p15', 'Five identical white beads and six different colored beads are strung in a row. No two colored '
                  'beads may be next to each other. How many arrangements are possible?',
      ['120', '1440', '360', '720'], 4, [
          'Gaps: place the $5$ white beads first. They make $6$ gaps: before, between and after them.',
          'No two colored beads may touch, so each colored bead needs its own gap. $6$ colored beads and $6$ gaps: '
          'every gap gets one colored bead.',
          'The white beads are identical, so the only freedom is the order of the colored beads: $6!=720$.'])
    S('wp28-p16', 'A light signal has $x$ lamps in a row. Each lamp shows one of 4 colors, and colors may repeat. The '
                  'number of possible signals is $2^{6n}$. What is $x$?',
      ['$6n$', '$2n$', '$3n$', '$n+4$'], 3, [
          'Each lamp has $4$ options, so there are $4^x$ signals.',
          '$4^x=(2^2)^x=2^{2x}$. So $2^{2x}=2^{6n}$, $2x=6n$ and $x=3n$.'])
    S('wp28-p17', 'A six-digit code begins with 3. Each following digit is strictly larger than the previous one. '
                  'How many codes are possible?',
      ['5', '15', '6', '720'], 3, [
          'The $5$ digits after the 3 must be bigger than $3$ and all different: they come from $4$, $5$, $6$, $7$, '
          '$8$, $9$. Once they are chosen, the increasing order is forced.',
          'Choosing $5$ of $6$ is the same as choosing the $1$ digit that stays out: $6$ ways.'])
    S('wp28-p18', 'Two ordinary dice are rolled, and you are told only the sum of the two results. For how many of the '
                  'possible sums can you know exactly which two numbers came up (in any order)?',
      ['2', '4', '11', '6'], 2, [
          'Sum $2$: only $1+1$. Sum $3$: only $1+2$. Sum $11$: only $5+6$. Sum $12$: only $6+6$.',
          'Every sum from $4$ to $10$ can be made in at least two ways, for example $4=1+3=2+2$ and $10=4+6=5+5$.',
          'So there are $4$ such sums.'])
    S('wp28-p19', 'A four-digit door code uses no zero. Its first and last digits are equal, and its third digit is '
                  'three times its second. How many codes are possible?',
      ['81', '36', '27', '18'], 3, [
          'First digit: $9$ options. It forces the last digit: $1$ option.',
          'Second digit: $1$, $2$ or $3$ (three times it must still be a digit from $1$ to $9$): $3$ options. '
          'It forces the third digit: $1$ option.',
          '$9\\times3\\times1\\times1=27$.'])
    S('wp28-p20', 'A six-digit code uses exactly two different digits, and each of them appears three times. The code '
                  'may start with 0. The sum of its digits must be divisible by 12. How many different pairs of digits '
                  'can be used? (The order of the two digits does not matter.)',
      ['14', '4', '10', '9'], 3, [
          'If the digits are $a$ and $b$, the sum is $3a+3b=3(a+b)$. It is divisible by $12$ only if $a+b$ is '
          'divisible by $4$.',
          '$a+b=4$: $0$ and $4$, $1$ and $3$ ($2$ pairs; $2$ and $2$ are not two different digits).',
          '$a+b=8$: $0$ and $8$, $1$ and $7$, $2$ and $6$, $3$ and $5$ ($4$ pairs).',
          '$a+b=12$: $3$ and $9$, $4$ and $8$, $5$ and $7$ ($3$ pairs).',
          '$a+b=16$: $7$ and $9$ ($1$ pair).',
          'Total: $2+4+3+1=10$.'])


def rn_practice(M):
    # copies (practice_audit): LEVEL = the guided BANANA question; t18-3-4 = a copy (moved in by the T18 patch)
    # extra-bank items beyond 3: p21 (= guided Q9 method), p22 (= the Quick-checks lesson 7 choose 3),
    # p27 (named teams of 3 = the Hebrew's 6 children / 3 + 3 lesson numbers; q-41 + guided Q12 cover named/unnamed)
    # September items whose type the Hebrew practice already covers (or that repeat a guided question):
    #   15, 27 (at least one: q-14 kept) · 17 (pool stays full: p05) · 18 (together: p23 kept) · 20 (gaps: p15)
    #   22 (repeats: q-21 kept) · 23 (round table: p26 kept) · 26 (who stays out: p17) · 30 (primes in n!: p02)
    cut = ['wp28-p25', 'alg-extra-unit-t18-3-4', 'wp28-p21', 'wp28-p22', 'wp28-p27'] + \
          ['q-r26-t28-%02d' % k for k in (15, 17, 18, 20, 22, 23, 26, 27, 30)]
    for qid in cut:
        if qid in M.D['questions'] and any(f['ref'] == qid and f['section'] == PRAC for f in M.D['flow']):
            M.unplace(qid)
    n = lambda k: 'q-r26-t28-' + k
    p = lambda k: 'wp28-p' + k
    M.practice_order(PRAC, [
        p('07'), p('05'), p('06'), p('04'), p('01'), p('08'), p('10'), p('24'), p('14'), p('09'), p('11'), p('03'),
        p('12'), n('16'), p('16'), p('02'), n('31'), n('29'), p('17'), p('19'), p('23'), n('19'), n('21'), p('13'),
        n('14'), p('26'), n('41'), p('15'), p('18'), p('20')])


def rn_sync(M):
    """Video titles, pre-loaded question text and slide notes follow the new stems."""
    for vid, v in M.D['videos'].items():
        if v.get('topic') != TOPIC or v.get('kind') != 'solution' or not v.get('questionId'):
            continue
        qid = v['questionId']
        if qid not in M.D['questions']:
            continue
        stem = rich_plain(M.q(qid)['stemRich']).replace('\\times', '×')
        v['title'] = v['navLabel'] = stem
        for b in v['beats']:
            if b['mode'] == 'question' and b['pre']:
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, stem)
                if not b.get('loads'):
                    b['loads'] = 'The question with its four answer choices is already on the canvas.'


def renumber_pass(M):
    rn_guided(M)
    rn_lessons(M)
    rn_order(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_sync(M)


# ======================================================================================================
# 2026-10-07 methods spread (runs last)
# The 2026-10-06 exam methods, shown wherever they genuinely help: one extra written line on the question
# (guided or practice; existing lines kept), and on the clearest guided videos one extra "Method N" slide.
# Nothing in topics 21-29 is recorded (checked ~/Documents/Course.recordings 2026-10-07).
# ======================================================================================================
SPREAD_RECORDED = set()


def _sp_line(M, qid, line):
    """Append one method line to a question's written solution (existing lines kept)."""
    ex = list(M.q(qid).get("explanation") or [])
    if line in ex: return
    M.set_q(qid, expl=ex + [line])


def _sp_slide(M, qid, after_n, title, script):
    """One extra method slide in the guided solution video of qid, after slide after_n. Sidebar unchanged."""
    vid = "solve-" + qid
    if vid in SPREAD_RECORDED: return
    assert M.video(vid)["questionId"] == qid, vid
    act = M.slide(vid, 2)["active"]
    M.insert_slides(vid, after_n, [dict(mode="question", active=act, title=title, pre=[Q(qid)], script=script)])


def spread_methods(M):
    # Few topic-28 questions fit the new methods: most are pure counting, and the "no names" and "at most" cases
    # already carry their line (wp28-g138, q-r26-t28-41, wp28-p13). Practice: one written line.
    _sp_line(M, 'wp28-p16', r'Shortcut · Pick values that fit: one equation with two letters, and the question expects one answer, therefore any values that fit give it. Take $n=1$: $4^x=2^6=64$, therefore $x=3$. Only $3n$ gives $3$ (the others give $6$, $2$ and $5$).')


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


# =====================================================================================
# 2026-10-07 study-plan order: students meet the topics in the STUDY PLAN order (src/lib/planData.ts ORDER), not
# by topic number. A named method used before the topic that teaches it (in the plan) becomes a self-contained
# "Shortcut · <name>: <why>" line; a "Shortcut" whose method the plan already taught becomes a normal
# "Method N · <name>" line. Unrecorded videos only. Runs LAST.
# =====================================================================================

def _po_line(M, qid, start, new):
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(start)]
    assert len(k) == 1, (qid, start, k)
    ex[k[0]] = new
    M.set_q(qid, expl=ex)


def _po_relabel(M, qid, old, name):
    import re as _re
    ex = list(M.q(qid)['explanation'])
    k = [i for i, l in enumerate(ex) if l.startswith(old)]
    assert len(k) == 1, (qid, old, k)
    used = [int(n) for l in ex for n in _re.findall(r'^Method (\d+) ·', l)]
    rest = ex[k[0]][len(old):].lstrip()
    if _re.match(r'[A-Z][a-z]', rest): rest = rest[0].lower() + rest[1:]
    ex[k[0]] = 'Method %d · %s: %s' % (max(used) + 1 if used else 2, name, rest)
    M.set_q(qid, expl=ex)


def _po_say(M, vid, n, old, new):
    """Replace the spoken line `old` (exact) on slide n with `new` (a string, or a list of strings)."""
    b = M.slide(vid, n)
    k = [i for i, l in enumerate(b['lines']) if l.get('say') == old]
    assert len(k) == 1, (vid, n, old)
    M.edit_lines(vid, n, lambda ls: ls[:k[0]] + [{'say': s} for s in ([new] if isinstance(new, str) else new)] + ls[k[0] + 1:])


def plan_order_fix(M):
    # "Pick values that fit" is taught in topic 51 (day 6), before topic 28: a normal method line.
    _po_relabel(M, 'wp28-p16', 'Shortcut · Pick values that fit:', 'Pick values that fit')


_apply_before_plan_order_fix = apply


def apply(M):
    _apply_before_plan_order_fix(M)
    plan_order_fix(M)   # 2026-10-07 study-plan order: runs last


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
    _mn_load().method_names(M, 28)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 Hebrew points restored: the 2026-10-05 cut shortened "With or Without Repetition" and "Mutual Action".
# Two points of the teacher's Hebrew lessons were no longer said anywhere: a row of n items = n! in general (and that
# factorial comes back later for groups), and "diagonal questions are rare but do show up". Runs LAST.
# =====================================================================================================================
import importlib.util as _ilu_hb, os as _os_hb
_s_hb = _ilu_hb.spec_from_file_location('_hebrew_back', _os_hb.path.join(_os_hb.path.dirname(_os_hb.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu_hb.module_from_spec(_s_hb); _s_hb.loader.exec_module(HB)


def hebrew_points_back(M):
    # Q6 trophies in a row: the general rule n items in a row -> n!, and factorial is needed again later (groups)
    if not HB.add_lines(M, 'solve-wp28-g130', 'Method 1 · Counting in stages', 'Seven items in a row: seven factorial ways', [
            'Any n different items in a row: n factorial ways.',
            "Keep factorial in mind — we'll use it again later, when we choose groups."]):
        HB.add_expl(M, 'wp28-g130', 'In general: $n$ different items in a row can be arranged in $n!$ ways. Factorial comes back later, when we choose groups.')
    # Q8 diagonals: exam-frequency remark from the Hebrew lesson
    if not HB.add_lines(M, 'solve-wp28-g133', 'Counting Questions', 'Diagonals — four ways.', [
            "A rare question type — but it does show up on the exam: the diagonals of a polygon."], where='before'):
        HB.add_expl(M, 'wp28-g133', 'Diagonal questions are rare on the exam, but they do show up.')


_apply_before_hebrew_points_back = apply


def apply(M):
    _apply_before_hebrew_points_back(M)
    hebrew_points_back(M)   # 2026-10-08 Hebrew points restored: runs LAST
