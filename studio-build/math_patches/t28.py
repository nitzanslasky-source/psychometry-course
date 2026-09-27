"""Topic 28 - Counting possibilities. Course review 2026-09 fixes.
See t28_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q
from math_api import VIS, rich_plain, _word

TOPIC = 28
LEARN, ADV, PRAC = 'wp28-learn', 'wp28-advanced', 'wp28-practice'
# Provisional numbers: the new learn question is created first (18), then the advanced ones (19-26).
# renumber_guided() renumbers everything in course order after all patches ran.
SB_LEARN = ['Question %d' % n for n in list(range(1, 13)) + [18]]
SB_ADV = ['Question %d' % n for n in list(range(13, 18)) + list(range(19, 27))]
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


def _roads(label, towns, roads):
    """Road map in the course SVG style. roads = [(town1, town2, number of roads)]."""
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="%s"><title>%s</title>'
           % (label, label)]
    for a, b, k in roads:
        (x1, y1), (x2, y2) = towns[a], towns[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        px, py = -dy / L, dx / L
        for i in range(k):
            off = (i - (k - 1) / 2) * 26
            cx, cy = mx + px * off * 2, my + py * off * 2
            out.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="2.4"/>'
                       % (x1, y1, cx, cy, x2, y2, TEAL))
    for t, (x, y) in towns.items():
        out.append('<circle cx="%d" cy="%d" r="19" fill="white" stroke="%s" stroke-width="2.5"/>' % (x, y, INK))
        out.append('<text x="%d" y="%d" text-anchor="middle" dominant-baseline="middle" fill="%s" '
                   'font-family="DejaVu Sans,Arial,sans-serif" font-size="20">%s</text>' % (x, y + 1, INK, t))
    out.append('</svg>')
    return ''.join(out)


TOWNS = {'A': (80, 180), 'B': (320, 58), 'C': (560, 180), 'D': (320, 302)}
ROADS_LESSON = _roads('Roads between towns A, B, C and D', TOWNS,
                      [('A', 'B', 3), ('B', 'C', 2), ('A', 'D', 2), ('D', 'C', 4)])
ROADS_Q = _roads('Roads between towns A, B, C and D', TOWNS,
                 [('A', 'B', 4), ('B', 'C', 3), ('A', 'D', 2), ('D', 'C', 5), ('A', 'C', 1)])


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

    # near-duplicates / off-topic puzzle
    for qid in ['wp28-p04', 'wp28-p07', 'wp28-p13']:
        M.unplace(qid)

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

    # Add or Subtract Cases: not "rare"
    M.set_slide('wp-134', 2, title='Why learn it', script=[
        "First thing to know: on their own, these questions are less common on the exam.",
        A("'Less common · needed for probability' appears", T('Less common $\\cdot$ needed for probability', size=46)),
        "But the idea is everywhere. Probability — the next topic — uses it all the time.",
        "And the harder counting questions near the end of the section need it too.",
        D('Underline "needed"'),
        "So learn it well.",
    ])
    _say(M, 'wp-134', 4, 'Subtracting possibilities is even rarer.', 'Subtracting possibilities: all minus forbidden.')
    M.edit_lines('wp-134', 4, lambda ls: ls + [
        {'say': "Watch for the words \"not\" and \"at least one\". They almost always mean: all minus forbidden."}])
    M.set_sidebar('wp-134', ['Why learn it', 'Adding cases', 'Subtracting', 'Recap'])

    # Choosing a Group: drop "very hard, very rare", general complement rule, unlabelled groups, checklist
    _say(M, 'wp-137', 2, 'Choosing a group — first, know these are edge questions. Very hard, and very rare.',
         "Choosing a group. On its own it's less common — but probability needs it all the time.")
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
        dict(mode='concept', active=3, title='Groups with no names', script=[
            "One more trap: groups that have no names.",
            A("'6 people into two groups of 3' appears", T('$6$ people into two groups of $3$', size=46)),
            "If the groups have names — team red and team blue — choose three for red. The rest go to blue.",
            D('Write "named: (6 × 5 × 4) ÷ 3! = 120 ÷ 6 = 20"'),
            "Six times five times four, over three factorial: twenty.",
            "But if the groups have no names, A, B, C against D, E, F is the same split as D, E, F against A, B, C.",
            D('Write "ABC | DEF = DEF | ABC"'),
            "Every split was counted twice.",
            D('Write "no names: 20 ÷ 2 = 10"'),
            "Divide by two: ten.",
            "Names — keep the count. No names — halve it.",
        ]),
        dict(mode='concept', active=4, title='The checklist', script=[
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
    M.set_slide('wp-137', 7, active=5, script=[
        A("Recap line 1 appears", T('A group: ordered count $\\div\\ k!$', size=44)),
        A("Recap line 2 appears", T('Choose $k$ of $n$ = choose the $n-k$ who stay out', size=44)),
        A("Recap line 3 appears", T('Groups with no names: $\\div\\ 2$', size=44)),
        "Three questions next. Try each one with the checklist.",
    ])
    M.set_sidebar('wp-137', ["Order doesn't matter", 'Divide by k!', 'Who stays out', 'Groups with no names',
                             'The checklist', 'Recap'])

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
    _say(M, 'solve-wp28-g139', 1, 'Last question of the set.', 'Question twelve.')

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
    # 4. New guided question in "Learn and try": groups with no names
    # =====================================================================================================
    g = 'q-r26-t28-01'
    M.new_q(g, TOPIC, 'Six friends are split into two groups of 3 to play a game. The groups have no names. In how '
                      'many different ways can the split be done?', ['$20$', '$10$', '$40$', '$120$'], 2, [
        'If the groups had names (group 1 and group 2): choose $3$ of the $6$ for group 1: '
        '$\\frac{6\\times5\\times4}{3!}=\\frac{120}{6}=20$. The rest go to group 2.',
        'The groups have no names, so A, B, C against D, E, F is the same split as D, E, F against A, B, C. '
        'Every split was counted twice: $\\frac{20}{2}=10$.',
        'Check: follow one friend. Choose her $2$ partners from the other $5$: $\\frac{5\\times4}{2}=10$.'])
    M.place_q(g, LEARN, after='solve-wp28-g139')
    _sol(M, g, False, ["Groups with no names."], [
        ('Method 1 · Named, then halve', [
            "Checklist: does order matter inside a group? No. Do the groups have names? No — that's the key.",
            "First pretend the groups have names: group one and group two.",
            D('Write "group 1: (6 × 5 × 4) ÷ 3! = 120 ÷ 6 = 20"'),
            "Choose three for group one: six times five times four, over three factorial. Twenty. The rest go to group two.",
            "But the groups have no names. A, B, C against D, E, F is the same split as D, E, F against A, B, C.",
            D('Write "ABC | DEF = DEF | ABC"'),
            "Every split was counted twice.",
            D('Write "20 ÷ 2 = 10"'),
            "Twenty over two: ten.",
            D('Circle choice 2'),
            "Choice two. Twenty is the trap — that's the answer for named groups.",
        ]),
        ('Method 2 · Follow one friend', [
            "A check. Take one friend — call her A. She is in some group.",
            "Who are her two partners? Choose two of the other five.",
            D('Write "(5 × 4) ÷ 2 = 10"'),
            "Five times four, over two: ten. The other three form the second group. Ten again.",
        ]),
    ])

    # =====================================================================================================
    # 5. New lesson video A (advanced section): roads, zero digits, at least one, objects into boxes, checks
    # =====================================================================================================
    VA = 'r26-t28-cases'
    sbA = ['Road maps', 'The zero trap', 'At least one', 'Which is the base?', 'Quick checks', 'Recap']
    M.new_video(VA, TOPIC, 'Roads, Zeros and "At Least One"', sbA, [
        dict(mode='title', title='Roads, Zeros and "At Least One"', script=[
            "Four question types the exam loves.",
            "Road maps, the zero in digit questions, \"at least one\" — and objects into boxes.",
        ]),
        dict(mode='concept', active=0, title='Road maps', script=[
            "First: road maps. A very typical exam drawing.",
            A('The road map appears', VIS(ROADS_LESSON, w=760, h=380)),
            "From A to C you can go through B — or through D.",
            "Through B: three roads to B, then two roads to C. Each road to B goes with each road to C.",
            D('Write "via B: 3 × 2 = 6"'),
            "Along one path, the roads are stages of choice. And — multiply. Six.",
            D('Write "via D: 2 × 4 = 8"'),
            "Through D: two roads, then four. Eight.",
            "But you go through B OR through D — never both. Those are separate cases.",
            D('Write "6 + 8 = 14"'),
            "Or — add. Fourteen routes.",
            D('Write "and → ×   or → +"'),
            "The rule: \"and\" along a path — multiply. \"Or\" between paths — add.",
        ]),
        dict(mode='concept', active=1, title='The zero trap', script=[
            "Digit questions have one classic trap: the zero.",
            A('The example appears', T('Even three-digit numbers from $0, 1, 2, 3, 4, 5$, no digit repeats: how many?',
                                       size=40)),
            "Most restricted first: the units digit must be even. Zero, two or four.",
            "But if the units digit is zero, zero is used up — and the hundreds digit has more options.",
            "If the units digit is two or four, the hundreds digit still can't be zero.",
            "The number of options depends on the case. So split into cases.",
            D('Write "Case 1: units = 0 → 5 × 4 × 1 = 20"'),
            "Case one: the units digit is zero. Hundreds: any of the other five. Tens: four left. Twenty.",
            D('Write "Case 2: units = 2 or 4 → 4 × 4 × 2 = 32"'),
            "Case two: the units digit is two or four — two options. Hundreds: not zero and not the units digit — four options.",
            "Tens: four left — and now zero is allowed. Four times four times two: thirty-two.",
            D('Write "20 + 32 = 52"'),
            "Add the cases: fifty-two.",
            "The trap answer is sixty: three even digits, times five, times four. It forgets that zero can't lead.",
        ]),
        dict(mode='concept', active=2, title='At least one', script=[
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
        dict(mode='concept', active=3, title='Which is the base?', script=[
            A("'4 letters into 3 mailboxes' appears", T('$4$ different letters into $3$ mailboxes', size=48)),
            "Four different letters go into three mailboxes. Any mailbox can get any number of letters.",
            "Is it three to the fourth, or four to the third? Ask: who chooses?",
            "Every letter chooses a mailbox. Letter one: three options. Letter two: three options. Letter three, letter four: three each.",
            D('Write "3 × 3 × 3 × 3 = 3⁴ = 81"'),
            "Four stages — one for each letter. Three options each. Three to the fourth: eighty-one.",
            "The trap is four to the third, sixty-four. That would be each mailbox choosing one letter — but a mailbox can get two letters, or none.",
            A("'Each object chooses a box' appears", T('Each object chooses: one stage per object', size=44)),
        ]),
        dict(mode='concept', active=4, title='Quick checks', script=[
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
        dict(mode='concept', active=5, title='Recap', script=[
            A('Recap line 1 appears', T('Road map: $\\times$ along a path, $+$ between paths', size=40)),
            A('Recap line 2 appears', T('Zero among the digits? Split into cases', size=40)),
            A('Recap line 3 appears', T('At least one $=$ all $-$ none', size=40)),
            A('Recap line 4 appears', T('Objects into boxes: each object chooses', size=40)),
            A('Recap line 5 appears', T('Not sure? Test on a small case', size=40)),
            "Four questions next — one of each.",
        ]),
    ], ADV, after='solve-wp28-g144')
    M.video(VA)['hybrid']['num'] = 54

    g2, g3, g4, g5 = ['q-r26-t28-%02d' % k for k in (2, 3, 4, 5)]
    M.new_q(g2, TOPIC, 'The figure shows all the roads between four towns: A, B, C and D. A route from A to C may not '
                       'pass through the same town twice. How many different routes lead from A to C?',
            ['$14$', '$22$', '$23$', '$120$'], 3, [
        'Through B: $4$ roads, then $3$ roads: $4\\times3=12$ routes ("and" along a path: multiply).',
        'Through D: $2\\times5=10$ routes.',
        'Directly: $1$ route.',
        'A route goes through B, or through D, or directly: separate cases, so add. $12+10+1=23$.'], figure=ROADS_Q)
    M.place_q(g2, ADV, after=VA)
    _sol(M, g2, True, ["A road map."], [
        ('Method 1 · Multiply along, add between', [
            "Checklist step five: cases. A route goes through B, or through D, or straight to C.",
            D('Write "via B: 4 × 3 = 12"'),
            "Through B: count the roads. Four from A to B, three from B to C. Four times three: twelve.",
            D('Write "via D: 2 × 5 = 10"'),
            "Through D: two, then five. Ten.",
            D('Write "direct: 1"'),
            "And one direct road. Don't miss it.",
            D('Write "12 + 10 + 1 = 23"'),
            "Three separate cases — add. Twenty-three.",
            D('Circle choice 3'),
            "Choice three.",
            "The traps: forgetting the direct road gives twenty-two. Multiplying all the numbers gives one hundred twenty.",
        ]),
    ])

    M.new_q(g3, TOPIC, 'How many four-digit even numbers can be formed from the digits 0, 1, 2, 3 and 4 if no digit '
                       'may repeat?', ['$72$', '$36$', '$60$', '$48$'], 3, [
        'The units digit must be even: $0$, $2$ or $4$. Zero changes the count for the first digit, so split into cases.',
        'Case 1, units digit $0$: thousands $4$ options, hundreds $3$, tens $2$: $4\\times3\\times2\\times1=24$.',
        'Case 2, units digit $2$ or $4$ ($2$ options): the thousands digit is not $0$ and not the units digit: '
        '$3$ options. Then hundreds $3$ and tens $2$: $3\\times3\\times2\\times2=36$.',
        'Add: $24+36=60$.',
        'Check: all four-digit numbers with different digits: $4\\times4\\times3\\times2=96$. Odd ones (units $1$ or $3$): '
        '$3\\times3\\times2\\times2=36$. $96-36=60$.'])
    M.place_q(g3, ADV, after='solve-' + g2)
    _sol(M, g3, True, ["Digits — with a zero among them."], [
        ('Method 1 · Split by the units digit', [
            "Checklist: order matters — it's a number. No repeats. A restriction: the units digit is even. Most restricted first.",
            "The units digit: zero, two or four. But zero is special — it can't lead. So split.",
            D('Write "Case 1: units = 0 → 4 × 3 × 2 × 1 = 24"'),
            "Case one: units digit zero. The thousands digit: any of the other four. Then three, then two. Twenty-four.",
            D('Write "Case 2: units = 2 or 4 → 3 × 3 × 2 × 2 = 36"'),
            "Case two: units digit two or four — two options. Thousands: not zero, and not the units digit. Three options.",
            "Hundreds: three left — zero is back in. Tens: two. Thirty-six.",
            D('Write "24 + 36 = 60"'),
            "Add: sixty.",
            D('Circle choice 3'),
            "Choice three.",
            "The trap is seventy-two: three even digits, times four, times three, times two. It forgets that zero can't lead.",
        ]),
        ('Method 2 · All minus odd', [
            "A check from the other side.",
            D('Write "all: 4 × 4 × 3 × 2 = 96"'),
            "All four-digit numbers with different digits: the first digit is not zero — four options. Then four, three, two. Ninety-six.",
            D('Write "odd: 3 × 3 × 2 × 2 = 36"'),
            "Odd ones: units one or three — two options. First digit: not zero, not the units digit — three. Then three, two. Thirty-six.",
            D('Write "96 − 36 = 60"'),
            "Ninety-six minus thirty-six: sixty again.",
        ]),
    ])

    M.new_q(g4, TOPIC, 'A code has 4 digits. Each digit is from 0 to 9, digits may repeat, and the code may start with '
                       '0. How many codes contain the digit 5 at least once?', ['$4000$', '$3439$', '$6561$', '$2916$'], 2, [
        'At least one $=$ all $-$ none.',
        'All codes: $10^4=10000$.',
        'Codes with no 5: each digit has $9$ options: $9^4=6561$.',
        '$10000-6561=3439$.'])
    M.place_q(g4, ADV, after='solve-' + g3)
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

    # advanced card goes to the end of the section, with the new methods
    M.move('mem-counting-advanced', ADV)

    # sidebars of all guided solution videos (learn / advanced groups)
    for vid in ['solve-wp28-g%d' % k for k in (124, 125, 126, 128, 129, 130, 132, 133, 135, 136, 138, 139)]:
        M.set_sidebar(vid, SB_LEARN)
    for vid in ['solve-wp28-g%d' % k for k in (140, 141, 142, 143, 144)]:
        M.set_sidebar(vid, SB_ADV)
    M.set_sidebar('solve-' + g, SB_LEARN)

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
    rows.append(['Groups with no names', 'count as if named, then divide by \\(2\\)',
                 '6 into two groups of 3: \\(\\frac{20}{2}=10\\)'])
    c['tips'] += ['Not sure about a formula? Test it on a small case you can draw: 4 people, '
                  '\\(\\frac{4\\times3}{2}=6\\) handshakes.',
                  'Choices that differ by a factor (\\(210\\) and \\(35\\))? Order matters: the bigger one. '
                  'A group: divide.']

    c = M.card('mem-counting-advanced')
    c['tables'].insert(1, {'title': 'More methods', 'head': ['Situation', 'Method', 'Example'], 'rows': [
        ['Road map', '\\(\\times\\) along a path, \\(+\\) between paths', '\\(4\\times3+2\\times5+1=23\\)'],
        ['A zero among the digits', 'split into cases: units digit \\(0\\) or not',
         'even, from \\(0\\)–\\(5\\): \\(20+32=52\\)'],
        ['At least one', 'all \\(-\\) none', '\\(10^4-9^4=3439\\)'],
        ['Objects into boxes', 'each object chooses a box', '5 letters, 3 boxes: \\(3^5=243\\)'],
        ['Must be together', 'glue into one block, \\(\\times\\) the order inside', '\\(4!\\times3!=144\\)'],
        ['Must not be together', 'all \\(-\\) together', '\\(5!-4!\\times2=72\\)'],
        ['No two side by side', 'place the others, then fill the gaps', '\\(3!\\times4\\times3=72\\)'],
        ['Identical items', 'divide by the factorial of each repeat', 'BANANA: \\(\\frac{6!}{3!\\times2!}=60\\)'],
        ['Round table', 'fix one person: \\((n-1)!\\)', '4 people: \\(3!=6\\)'],
    ]})
    c['intro'] = 'The shortcuts from the advanced counting questions and the two method videos.'
    c['tips'] += ['A route may use the direct road too — count every path from start to end.',
                  'Digits with a zero: the leading digit is never 0, so split by where the 0 goes.']

    # =====================================================================================================
    # 8. New practice questions
    # =====================================================================================================
    P = {}
    P['10'] = ('From town A to town B there are 3 roads, and from town B to town C there are 4 roads. There is also '
               '1 direct road from A to C. Dan drives from A to C and back to A. On the way back he does not use any '
               'road he used on the way there. How many different round trips are possible?',
               ['$169$', '$156$', '$96$', '$84$'], 3, [
        'Split by the way there.',
        'Case 1, the direct road there ($1$ way): back through B on any roads: $4\\times3=12$. Total $1\\times12=12$.',
        'Case 2, through B there ($3\\times4=12$ ways): back by the direct road ($1$ way), or through B on two new '
        'roads ($3\\times2=6$ ways): $1+6=7$ ways back. Total $12\\times7=84$.',
        'Add: $12+84=96$.'])
    P['11'] = ('From her home, Noa can walk to bus stop P by 2 paths, or to bus stop R by 2 paths. From stop P, '
               '3 bus lines go to school. From stop R, 4 bus lines go to school. Noa uses exactly one bus stop. In how '
               'many different ways can she get from home to school?', ['$14$', '$48$', '$11$', '$28$'], 1, [
        'Through P: $2\\times3=6$. Through R: $2\\times4=8$.',
        'She goes through P or through R (separate cases): $6+8=14$.'])
    P['12'] = ('How many three-digit odd numbers can be formed from the digits 0, 1, 2, 3, 4 and 5 if no digit may '
               'repeat?', ['$60$', '$48$', '$36$', '$52$'], 2, [
        'Most restricted first: the units digit is odd: $1$, $3$ or $5$, so $3$ options.',
        'Hundreds digit: not $0$ and not the units digit: $4$ options.',
        'Tens digit: $4$ digits are left (now $0$ is allowed): $4$ options.',
        '$3\\times4\\times4=48$.'])
    P['13'] = ('How many three-digit numbers with all digits different can be formed from the digits 0, 2, 5, 7 and 8 '
               'if the number must be divisible by 5?', ['$24$', '$21$', '$12$', '$18$'], 2, [
        'Divisible by $5$: the units digit is $0$ or $5$. The zero changes the count, so split into cases.',
        'Case 1, units digit $0$: hundreds $4$ options, tens $3$: $4\\times3=12$.',
        'Case 2, units digit $5$: hundreds not $0$ and not $5$: $3$ options. Tens: $3$ left (including $0$): '
        '$3\\times3=9$.',
        'Add: $12+9=21$.'])
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
    P['24'] = ('Eight players are split into two teams of 4. The teams have no names. In how many different ways can '
               'the split be done?', ['$70$', '$35$', '$140$', '$1680$'], 2, [
        'As if the teams had names: choose $4$ of $8$ for team 1: $\\frac{8\\times7\\times6\\times5}{4!}=\\frac{1680}{24}=70$.',
        'No names: every split was counted twice. $\\frac{70}{2}=35$.'])
    P['25'] = ('Six students are split into 3 pairs for a project. The pairs have no names. In how many different ways '
               'can this be done?', ['$15$', '$90$', '$30$', '$45$'], 1, [
        'Follow one student: choose her partner from the other $5$: $5$ ways.',
        'Take one of the $4$ students left: choose his partner from the other $3$: $3$ ways. The last $2$ form '
        'the third pair: $1$ way.',
        '$5\\times3\\times1=15$.'])
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
        p('05'), p('06'), p('01'), p('08'), p('10'), p('21'), p('22'), p('14'), p('09'), p('11'), p('03'), n('11'),
        p('24'), p('12'), n('16'), n('17'), n('26'), p('16'), p('02'), p('27'), n('24'), n('12'), p('17'), p('19'),
        p('23'), n('18'), n('21'), p('25'), n('13'), n('14'), n('27'), n('15'), n('25'), n('19'), p('26'), n('23'),
        p('15'), n('20'), n('22'), n('10'), p('18'), p('20')])

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
