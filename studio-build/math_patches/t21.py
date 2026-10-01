"""Topic 21 - Trial, limits and patterns. Course review 2026-09 fixes.
See t21_CHANGES.md for the plain-language list."""
from dsl import T, H, A, D, Q

TOPIC = 21
LEARN, ADV, PRAC = 'wp21-learn', 'wp21-advanced', 'wp21-practice'
ADV_SOLUTIONS = ['solve-wp21-g0%d' % k for k in (13, 14, 15, 17, 18, 19, 20, 21, 23, 24, 25)]
ADV_SIDEBAR = ['Question %d' % n for n in range(6, 19)]   # 6-16 existing + 17, 18 new (renumbered at build)


def _solution(M, qid, intro, slides, after=None):
    """Guided-question solution video in the style of the 'Advanced Trial & Error' videos."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=ADV_SIDEBAR.index('Question %d' % n), title=title,
                          pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Advanced Trial & Error', ADV_SIDEBAR, beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = 'Advanced Trial & Error'
    v['hybrid']['num'] = 7
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _fix_draw(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'draw' in l and old in l['draw']:
                l['draw'] = l['draw'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _fix_say(M, vid, n, old, new):
    def fn(lines):
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = l['say'].replace(old, new)
        return lines
    M.edit_lines(vid, n, fn)


def _item(M, vid, n, k=0):
    return dict(M.slide(vid, n)['items'][k])


def apply(M):
    S = M.set_q
    # =====================================================================================
    # 1. Wrong rule: "min/max values form a continuous range, no holes" (Q13 video + card)
    # =====================================================================================
    Q13 = 'solve-wp21-g021'
    M.edit_lines(Q13, 1, lambda ls: [
        {'say': "Question thirteen."},
        {'say': "The boxes again — the same question as Question eight, with the same numbers."},
        {'say': "I promised a shortcut. Here it is."}])
    M.set_slide(Q13, 2, title='Method 1 · Count the spare markers', script=[
        "Fill every box to the minimum first.",
        D('Write "24 × 3 = 72 → 86 − 72 = 14 spare"'),
        "Three in every box: seventy-two markers. Fourteen are spare.",
        "A box rises above three only if it gets at least one spare marker.",
        D('Write "at most 14 boxes rise → at least 24 − 14 = 10 stay at 3"'),
        "Fourteen spares can lift at most fourteen boxes. So at least ten boxes stay at exactly three.",
        D('Circle choice 3'),
        "Nine is below ten. Impossible. Choice three — in one line of work.",
    ])
    M.set_slide(Q13, 3, title='Method 2 · Only the ends?', script=[
        "Now let's see ALL the possible values.",
        D('Write "possible: 10, 11, 12, …, 23"'),
        "At least ten boxes of three — we just saw that. At most twenty-three: twenty-three boxes of three, and the last box gets seventeen.",
        "And every count in between works. Why? Each spare marker lifts one box. Move one marker — the count changes by exactly one.",
        D('Write "changes by 1 at a time → no holes"'),
        "When the value can change by one at a time, the range has no holes. Then the impossible choice must be at an end.",
        D('Write "9, 10, 12, 15 → only 9 or 15 can be out"'),
        "Sort the choices: nine, ten, twelve, fifteen. Only nine or fifteen can be outside. Fifteen works — so it's nine.",
        "But careful! This is NOT a general rule.",
        D('Write "token 4 or 9: 24, 29, 34, … → holes!"'),
        "Remember the token — four or nine? The totals jump by five: twenty-four, twenty-nine, thirty-four. Plenty of holes.",
        "Fixed jumps leave holes. No holes only when you can move by one.",
    ])
    M.remove_slides(Q13, [4])
    S('wp21-g021', expl=[
        'The same boxes as the earlier question, now with a shortcut.',
        'Put $3$ markers in every box: $24\\times3=72$. Spare markers: $86-72=14$.',
        'A box rises above $3$ only if it gets at least one spare marker. Therefore at most $14$ boxes rise above $3$, '
        'and at least $24-14=10$ boxes stay at exactly $3$.',
        '$9$ is below $10$. Therefore $9$ is impossible. Choice 3.',
        'Every count from $10$ to $23$ is possible: each spare marker lifts one box, and the count can change by $1$ at a time. '
        'This is NOT true in every min–max question. When the values change in fixed jumps (the $4$-or-$9$ token: $+5$ each time), '
        'there are holes.'])

    tk = M.card('mem-trial-toolkit')
    tk['tables'][0]['rows'] = [
        ["Two values that swap (coin, tickets)", "Work in order from the minimum; each swap is a constant step — watch for the skip"],
        ["Constant step", "Test by remainder: all totals leave the same remainder"],
        ["Numbers in the answers", "Plug in from the middle; the first one that works is the answer"],
        ["\"Three times as many…\"", "The count must divide by 3 — eliminate the others"],
        ["Max of one / min of the largest / min of one",
         "Give the others the least / share as equally as possible / give the others the most"],
        ["Smallest or largest asked, two options left", "Plug in the smaller / the bigger option first"],
        ["Everyone has a minimum (at least 3 in each box)", "Fill everyone to the minimum, then count the spare units"],
        ["\"Cannot be\" in a min–max question",
         "Sort the choices: the odd one is at an end ONLY if the value can change by 1 at a time. Fixed jumps (+5, +3…) leave holes"],
        ["\"To be sure…\"", "Worst luck + 1 (see Algebraic Understanding)"],
        ["\"Must be true\" (Topics 1 and 20)", "One counterexample removes a choice; then prove the one that is left"],
        ["Multiplying for a total", "Check the last digit of the choices (only helps if they end differently)"],
        ["Sequence with a rule", "Write it term by term; check both edges"],
        ["Repeating cycle", "Use the remainder: lamps, days of the week (÷ 7), last digits of powers"],
        ["Two schedules meeting", "Common multiple — jump with the bigger number"],
    ]

    # =====================================================================================
    # 2. First lesson videos (learn section)
    # =====================================================================================
    # wp-001 slide 4: point back to T20; slide 5 shorter
    ex4 = _item(M, 'wp-001', 4, 0)
    M.set_slide('wp-001', 4, title='Must or could', script=[
        "One reminder from Topics 1 and 20: must, could, cannot.",
        A("'Two positive integers, sum 14' appears", ex4),
        "Two positive integers add to fourteen. Pick one — the other is fixed.",
        A("'Could be true → one example · Must be true → every allowed case' appears",
          T('Could be true $\\to$ one example is enough · Must be true $\\to$ every allowed case', size=40)),
        "Could be true? One legal example proves it. Must be true? You need a reason — or one counterexample kills it.",
        "Read which one they ask before you start trying.",
    ])
    sb1 = M.video('wp-001')['hybrid']['sidebar']
    M.set_sidebar('wp-001', [x if x != 'Possible vs must' else 'Must or could' for x in sb1])
    M.set_slide('wp-001', 5, script=[
        "How to use this chapter: every guided question comes BEFORE its video. Try it on paper first.",
        "Stuck? Write what you do know — the first two cases. Then watch, and compare.",
        "Let's start with type one.",
    ])

    # wp-006 (Minimum & Maximum, part 1): drop "recurring motif", fix "bold words", teach k(k+1)/2
    W6 = 'wp-006'
    bold = _item(M, W6, 4)
    push = _item(M, W6, 2)
    M.set_slide(W6, 2, script=[
        A("'Know which way to push → fewer tries' appears", push),
        "Minimum-maximum questions are about ranges. What's the smallest possible value? The largest?",
        "Unlike general problems, you're not trying blindly.",
        "You can work out which way to push — which direction takes you to the minimum, and which to the maximum.",
    ])
    M.set_slide(W6, 4, script=[
        "On the exam, the key words are printed in bold.",
        A("'LARGEST · SMALLEST · CANNOT' appears", bold),
        "They're there so you don't mix up the largest with the smallest.",
        D('Circle LARGEST and SMALLEST'),
        "In our questions, find that word yourself and circle it — before you push in any direction.",
    ])
    # Pass 2: the original slide 3 "A recurring motif" stays (plan: RESTORE)
    # now: 1 title, 2 Ranges, 3 A recurring motif, 4 Bold words, 5 Squeeze, 6 Balance, 7 Recap
    M.insert_slides(W6, 6, [dict(mode='concept', active=5, title='Cheapest k different', script=[
        "One formula worth knowing here.",
        A('1 + 2 + … + k = k(k + 1)/2 appears', T('$1+2+3+\\ldots+k=\\frac{k(k+1)}{2}$', size=58, gap=50)),
        "The cheapest way to give k people DIFFERENT positive amounts: one, two, three, up to k.",
        D('Write "1 + 8 = 2 + 7 = 3 + 6 = 4 + 5 = 9"'),
        "Why the formula? Take one to eight. Pair the ends: one plus eight, two plus seven — every pair makes nine.",
        D('Write "4 pairs × 9 = 36 = (8 × 9) ÷ 2"'),
        "Four pairs of nine: thirty-six. That's eight times nine, over two.",
        "So k people with different amounts need at least k times k plus one, over two.",
    ])])
    M.set_slide(W6, 8, script=[
        A("'Max of one part → squeeze the others' appears", T('Max of one part $\\to$ squeeze the others', size=42)),
        A("'Min of the largest → balance' appears", T('Min of the largest $\\to$ balance the group', size=42)),
        A("'k different amounts → at least k(k+1)/2' appears",
          T('$k$ different amounts $\\to$ at least $\\frac{k(k+1)}{2}$', size=42)),
        "Maximum of one part: squeeze everything else down. Minimum of the largest: balance the group.",
        "Different amounts? Start from one, two, three — the cheapest list.",
        "And always show both halves: nothing better fits — and your value really works.",
        "Now a real question of this type.",
    ])
    for n, a in zip(range(2, 9), range(0, 7)):
        M.set_slide(W6, n, active=a)
    M.set_sidebar(W6, ['Ranges', 'A recurring motif', 'Bold words', 'Squeeze the others', 'Balance the group', 'Cheapest k different', 'Recap'])

    # Q3 video: no bold print in our stems
    _fix_say(M, 'solve-wp21-g007', 2, 'Read the bold word: the LARGEST', 'Find the key word and circle it: the LARGEST')

    # wp-008 (Patterns): n = 3, then n = 4 if two survive; n = 1 only as a quick check
    W8 = 'wp-008'
    it4 = _item(M, W8, 4)
    M.set_slide(W8, 4, script=[
        "Which number do we plug in? Usually three.",
        A("'n = 3: small enough to calculate, big enough to separate' appears", it4),
        "Why not one? It's shorter to calculate…",
        "But the exam is often built so that n equals one leaves you with two possible answers.",
        D('Underline "big enough to separate"'),
        "Three is small enough to calculate easily, and big enough to tell the answers apart.",
        A("'Two survive? Try n = 4 too' appears", T('Two choices survive? Also try $n=4$', size=44)),
        "Still two choices left? Plug in four as well.",
        "And n equals one? Fine as a quick extra check — never as your only check.",
    ])
    M.set_slide(W8, 6, script=[
        A("'Step by step → write 1, 2, 3, 4 · Sequences → plug in n = 3' appears",
          T('Step by step $\\to$ write $1,2,3,4$ · Sequences $\\to$ plug in $n=3$ (then $n=4$)', size=42)),
        "Step by step: write the items one by one, keeping the rule order.",
        "Sequences: plug in three, test every choice. Two survive? Try four.",
        "Two questions next — one of each kind.",
    ])
    mc = M.card('mem-trial-error')
    mc['tips'] = ["Could be true → one legal example is enough. Must be true / cannot → you need a reason (Topics 1 and 20).",
                  "\\(n=3\\), not \\(n=1\\): one often leaves two choices standing."]
    mc['tables'][0]['rows'] = [
        ["General problems", "nothing tells you what to try first",
         "draw the story, follow it, split into routes, or test each answer"],
        ["Minimum & maximum", "the largest / smallest possible value",
         "max of one part: squeeze the others · min of the largest: balance"],
        ["Different positive amounts", "each person gets a different number",
         "start from \\(1, 2, 3, \\ldots\\): \\(k\\) people need at least \\(\\frac{k(k+1)}{2}\\)"],
        ["Patterns · step by step", "a rule repeated round after round",
         "write the items one by one, keeping the rule order"],
        ["Patterns · sequences", "a formula with \\(n\\) in the choices",
         "plug in \\(n=3\\) and check every choice; two survive? also try \\(n=4\\)"],
    ]

    # Q4 solution text (review: unclear "halving forty-five")
    # (video is fine)

    # =====================================================================================
    # 3. Advanced section videos
    # =====================================================================================
    # wp-012 slide 2: shorter "why it matters"
    b12 = _item(M, 'wp-012', 2)
    M.set_slide('wp-012', 2, script=[
        "Why does the exam love these questions?",
        "They test one thing: when there's no equation — do you freeze, or do you start?",
        A("'Don't stare. Start trying.' appears", b12),
        D('Underline "Start trying"'),
        "Try, check, adjust. You'll use this all through the quantitative section.",
    ])

    # wp-016 (Minimum & Maximum, part 2): one board with all three rules, worst case + 1
    W16 = 'wp-016'
    v16 = M.video(W16)
    v16['title'] = v16['navLabel'] = v16['hybrid']['title'] = 'More Minimum & Maximum'
    M.set_slide(W16, 1, title='More Minimum & Maximum', script=[
        "Trial and error, part two: more minimum and maximum.",
        "Understand min and max — and you need far fewer tries.",
    ])
    M.set_slide(W16, 2, title='Three min/max rules', script=[
        "Here's the key idea — three rules on one board.",
        A("'Max of one → give the others the least' appears", T('Max of one $\\to$ give the others the least', size=40)),
        "Want one number as big as possible? Give everything else the least you're allowed.",
        D('Write "3 different positive numbers, total 26: 1 + 2 + 23"'),
        "Three different positive numbers, total twenty-six: one, two — and twenty-three.",
        A("'Min of the largest → share as equally as possible' appears",
          T('Min of the largest $\\to$ share as equally as possible', size=40)),
        "Want the LARGEST as small as possible? Share as equally as you can.",
        D('Write "7 + 9 + 10 = 26"'),
        "Seven, nine, ten. The largest can't go below ten.",
        A("'Min of one → give the others the most' appears", T('Min of one $\\to$ give the others the most', size=40)),
        "Want one number as small as possible? Give everything else the MOST you're allowed.",
        D('Write "3 scores, each at most 10, total 26: 10 + 10 + 6"'),
        "Three scores, each at most ten, total twenty-six. The others take ten and ten — the smallest is at least six.",
        "Rules two and three sound opposite. They aren't: in rule two we shrink the LARGEST, so the others can't pass it.",
    ])
    _fix_draw(M, W16, 3, '28 : 4 = 7', '28 ÷ 4 = 7')
    M.insert_slides(W16, 3, [dict(mode='concept', active=2, title='Worst luck + 1', script=[
        "One more min-max idea you met in Algebraic Understanding: to be SURE, imagine the worst luck — then add one.",
        A("'To be sure → worst luck + 1' appears", T('To be sure $\\to$ worst luck $+\\,1$', size=46)),
        "It's a maximum question in disguise: how long can the bad luck last? The next one must break it.",
        A("'4 players; the game ends when someone wins 3 rounds. Most rounds?' appears",
          T('$4$ players. The game ends when someone wins $3$ rounds. Most rounds?', size=40)),
        D('Write "worst luck: 2 wins each → 4 × 2 = 8 rounds"'),
        "Worst luck for ending the game: every player wins two. Eight rounds — and still no winner.",
        D('Write "8 + 1 = 9"'),
        "The ninth round gives someone a third win. At most nine rounds.",
    ])])
    # slides: 1 title, 2 rules, 3 At least, 4 Worst case, 5 Prove, 6 Recap
    M.set_slide(W16, 5, active=3)
    M.set_slide(W16, 6, active=4, script=[
        "Let's lock it in.",
        A("'Max one → min the rest · min one → max the rest' appears",
          T('Max one $\\to$ least for the rest · Min one $\\to$ most for the rest', size=40)),
        A("'Min of the largest → share equally' appears", T('Min of the largest $\\to$ share equally', size=40)),
        A("'To be sure → worst luck + 1' appears", T('To be sure $\\to$ worst luck $+\\,1$', size=40)),
        A("'Prove the bound, then build it' appears", T('Prove the bound, then build it', size=40)),
        D('Underline "worst luck + 1"'),
        "Next: a \"to be sure\" question.",
        "And one more trick you'll see soon: when you multiply for a total, check the last digit of the choices.",
    ])
    M.set_sidebar(W16, ['Three min/max rules', 'At least', 'Worst luck + 1', 'Prove, then build', 'Recap'])

    # Q9 video: ÷ instead of ":", honest "last digit" slide
    _fix_draw(M, 'solve-wp21-g017', 2, '12 : 4 = 3', '12 ÷ 4 = 3')
    M.set_slide('solve-wp21-g017', 3, title='Method 2 · Last digit — and its limit', script=[
        "The last-digit trick — and where it stops.",
        D('Write "3 × 6 → ends in 8"'),
        "Three times sixteen: look only at the last digit. Three times six is eighteen — it ends in eight.",
        "Forty-eight ends in eight. Sixty-four ends in four — gone.",
        D('Cross out choices 3 and 4'),
        "For the maximum, three hundred and three hundred twenty both end in zero. The last digit can't split them.",
        D('Write "16 × 20 = 320" and circle choice 1'),
        "So here we simply multiply: sixteen times twenty, three hundred twenty. Choice one.",
        "The trick helps only when the choices end in different digits.",
    ])

    # Q12 video: they ask for the smallest / largest (not "at least" / "at most")
    _fix_say(M, 'solve-wp21-g020', 2, "They ask 'at least' — so plug in", "They ask for the smallest — so plug in")
    _fix_say(M, 'solve-wp21-g020', 2, "'At most' — so plug in", "They ask for the largest — so plug in")

    # Q16 video: labels without "18:" colons
    _fix_draw(M, 'solve-wp21-g025', 2, '"18: 7:30', '"every 18 min → 7:30')
    _fix_draw(M, 'solve-wp21-g025', 2, '"24: 7:30', '"every 24 min → 7:30')

    # wp-022 (Patterns & Cycles): days of the week and last digits
    W22 = 'wp-022'
    M.insert_slides(W22, 4, [dict(mode='concept', active=3, title='Days and last digits', script=[
        "The same remainder trick solves two exam favorites.",
        A("'Today is Tuesday. What day is it in 30 days?' appears",
          T('Today is Tuesday. What day is it in $30$ days?', size=42)),
        "Days of the week repeat every seven.",
        D('Write "30 = 28 + 2 → remainder 2"'),
        "Thirty is four full weeks — twenty-eight days — plus two. Four full weeks bring us back to Tuesday.",
        D('Write "Tuesday + 2 → Thursday"'),
        "Two more days: Thursday.",
        A("'Units digit of 3²²?' appears", T('Units digit of $3^{22}$?', size=42)),
        "Last digits of powers repeat too. Write the first few.",
        D('Write "3, 9, 27, 81, 243 → last digits 3, 9, 7, 1, 3, …"'),
        "Three, nine, twenty-seven, eighty-one: last digits three, nine, seven, one. Then three again. A cycle of four.",
        D('Write "22 = 20 + 2 → 2nd in the cycle → 9"'),
        "Twenty-two is five full cycles plus two. The second digit in the cycle: nine.",
        "Remainder zero? Then it's the LAST one in the cycle.",
        "Lamps, days, digits — same tool: divide by the cycle length and look at the remainder.",
    ])])
    for n, a in zip(range(6, 9), range(4, 7)):
        M.set_slide(W22, n, active=a)
    M.set_slide(W22, 8, script=[
        A("'Write it term by term' appears", T('Write it term by term', size=40)),
        A("'Check both edges' appears", T('Check both edges', size=40)),
        A("'Items ≠ gaps' appears", T('Items $\\ne$ gaps', size=40)),
        A("'Cycle → remainder' appears", T('Cycle $\\to$ remainder (days: $\\div\\,7$, last digits: find the cycle)', size=40)),
        A("'Meet again → jump with the bigger number' appears", T('Meet again $\\to$ jump with the bigger number', size=40)),
        "Let's lock it in.",
        D('Underline "edges"'),
        "Next: patterns in real questions.",
    ])
    M.set_sidebar(W22, ['Term by term', 'Watch the edges', 'Repeating cycles', 'Days and last digits',
                        'Meeting times', 'Items vs gaps', 'Recap'])

    for vid in ADV_SOLUTIONS:
        M.set_sidebar(vid, ADV_SIDEBAR)
    for qid in ('wp21-g007', 'wp21-g014', 'wp21-g017'):
        v = M.video('solve-' + qid)
        v['title'] = v['navLabel'] = M.q(qid)['stem']

    # =====================================================================================
    # 4. New guided questions: worst case + 1, must be true
    # =====================================================================================
    g1, g2 = 'q-r26-t21-01', 'q-r26-t21-02'
    M.new_q(g1, TOPIC,
            'A drawer holds $10$ red, $8$ blue and $6$ green socks. In the dark, Dana takes out socks one at a time. '
            'What is the smallest number of socks she must take out to be sure she has $3$ socks of the same color?',
            ['$4$', '$9$', '$7$', '$17$'], 3, [
                'To be sure, imagine the worst luck, then add one. Dana wants $3$ of one color. The worst luck is $2$ of each color: '
                '$2+2+2=6$ socks, and still no color has $3$.',
                'The next sock is red, blue or green. Whatever it is, that color now has $3$: $6+1=7$.',
                '$6$ is not enough ($2$ red, $2$ blue, $2$ green), and $7$ always works. Choice 3.',
                'Traps: $4=3+1$ is the answer for a PAIR. $17=8+6+3$ is the answer for $3$ RED socks.'])
    M.place_q(g1, ADV, after=W16)
    _solution(M, g1, ["Question seventeen.", "A \"to be sure\" question. Think about the worst luck."], [
        ('Method 1 · Worst luck + 1', [
            "They ask what she must take to be SURE. So we imagine the worst luck, then add one — as in Algebraic Understanding.",
            "She wants three of one color. How long can she avoid that?",
            D('Write "2 red + 2 blue + 2 green = 6 → no 3 of a color"'),
            "Two red, two blue, two green. Six socks — and still no color has three.",
            D('Write "6 + 1 = 7"'),
            "The seventh sock is red, blue or green. Whatever it is, that color reaches three.",
            D('Circle choice 3'),
            "Seven. Choice three.",
            "Both halves: six can fail — we just built it. And seven always works.",
        ]),
        ('Method 2 · Spot the traps', [
            "Look at the wrong choices — each one answers a different question.",
            D('Next to choice 1 write "a pair: 3 + 1"'),
            "Four is the answer for a PAIR — the socks question from Algebraic Understanding.",
            D('Next to choice 4 write "3 RED: 8 + 6 + 3"'),
            "Seventeen is for three RED socks: all eight blue and all six green come first, then three red.",
            D('Next to choice 2 write "3 of each"'),
            "Nine is three of every color — more than we need.",
            "Read what must be sure: the same color, any color. Seven.",
        ]),
    ])

    M.new_q(g2, TOPIC, 'Five different positive integers have a sum of $20$. Which of the following must be true?',
            ['One of the numbers is $1$.', 'The largest number is at most $9$.',
             'At least two of the numbers are even.', 'The largest number is at least $6$.'], 4, [
                '"Must be true" means true in every allowed case. One counterexample removes a choice.',
                'Choice 1: $2+3+4+5+6=20$ has no $1$ ✗. Choice 2: $1+2+3+4+10=20$, and the largest is $10$ ✗. '
                'Choice 3: $1+3+4+5+7=20$ has only one even number ✗.',
                'Choice 4: if the largest were at most $5$, the five different numbers would be $1, 2, 3, 4, 5$, '
                'with sum $15\\ne20$. Therefore the largest is at least $6$ ✓. Choice 4.'])
    M.place_q(g2, ADV, after=Q13)
    _solution(M, g2, ["Question eighteen.", "A \"must be true\" question. One counterexample is enough to kill a choice."], [
        ('Method 1 · Hunt for counterexamples', [
            "Must be true means: in EVERY allowed case. So we build cases and try to break each choice.",
            D('Write "1 + 2 + 3 + 4 + 5 = 15 → 5 spare"'),
            "Start from the cheapest list: one to five. That's fifteen. Five are spare.",
            D('Write "1, 2, 3, 4, 10" and cross out choice 2'),
            "Put all five spares on the largest: one, two, three, four, ten. The largest is ten — not at most nine. Choice two is out.",
            D('Write "2, 3, 4, 5, 6" and cross out choice 1'),
            "Share the spares: two, three, four, five, six. No one here. Choice one is out.",
            D('Write "1, 3, 4, 5, 7" and cross out choice 3'),
            "One, three, four, five, seven: twenty, and only one even number. Choice three is out.",
            D('Circle choice 4'),
            "Choice four is left.",
        ]),
        ('Method 2 · Prove the survivor', [
            "On the exam you can stop there. But let's see WHY choice four must be true.",
            "It's a min-max question: how small can the largest be?",
            D('Write "largest ≤ 5 → only 1, 2, 3, 4, 5 → 15 ≠ 20 ✗"'),
            "If the largest were five or less, the only five different numbers are one to five. Their sum is fifteen, not twenty.",
            D('Write "2, 3, 4, 5, 6 → largest 6 ✓"'),
            "So the largest is at least six — and six really happens. Choice four.",
        ]),
    ])

    # =====================================================================================
    # 5. Existing questions: text, TeX, full solutions with numbers
    # =====================================================================================
    S('wp21-g004', expl=[
        'Break 1 must hit a large crystal (there are no small ones yet): $2-1+4=5$ crystals ($1$ large, $4$ small).',
        'Break 2 on the other large crystal: $5-1+4=8$, all small. Break 3 removes one small crystal: $8-1=7$.',
        'The other route: break 2 on a small crystal gives $5-1=4$. Then break 3 gives $4-1+4=7$ or $4-1=3$.',
        'The only possible totals are $3$ and $7$. Of the choices, only $7$ appears. Choice 4.'])
    S('wp21-g005', expl=[
        'One van, one scooter and the gap between them: $5+1+2=8$ m. So $8$ is possible.',
        'Each extra scooter adds its length and one more gap: $2+1=3$ m. Each extra van adds $5+1=6$ m.',
        'From $8$: $8+3=11$ and $11+3=14$. Both are possible.',
        'The smallest step is $3$. From $8$ we jump straight to $11$, and $10$ is skipped. Therefore $10$ is impossible. Choice 4.',
        'Faster: give each vehicle the gap after it (van $6$, scooter $3$) and remove the last gap: $L=6v+3s-1$. '
        'So $L+1$ is always a multiple of $3$, but $10+1=11$ is not.'])
    S('wp21-g007', stem='A mentor shares $32$ pins among apprentices. Each apprentice receives a different number of pins '
                        '(a positive integer), and all the pins are given out. What is the largest possible number of apprentices?',
      expl=[
          'To have as many apprentices as possible, give each one as little as possible: $1, 2, 3, \\ldots$',
          'Seven apprentices need at least $1+2+3+4+5+6+7=\\frac{7\\cdot8}{2}=28$ pins. '
          'Eight need at least $28+8=36$, and $36>32$. Therefore eight is impossible.',
          'Seven works: $1, 2, 3, 4, 5, 6, 11$. The $32-28=4$ spare pins go to the one who has the most. '
          'The sum is $32$, and all the amounts are different. Choice 4.'])
    S('wp21-g009', expl=[
        'Round 1 is given: $46$. Do not apply the rule to it.',
        'Round 2: $46\\div2=23$, then $23-1=22$. Round 3: $22\\div2=11$, then $11-1=10$. '
        'Round 4: $10\\div2=5$, then $5-1=4$. Choice 2.',
        'Keep the order: halve first, then subtract $1$. Don\'t subtract first: $46-1=45$ and then $45\\div2$ is the wrong order.',
        'From round 1 to round 4 there are only three steps. A fourth step would give round 5.'])
    S('wp21-g010', expl=[
        'Plug in $n=3$. The days give $3$, $6$ and $12$ crates. Total: $3+6+12=21$.',
        'Put $n=3$ into each choice: $3\\cdot3^2=27$, $3\\cdot2^3=24$, $2^3+3=11$, $3(2^3-1)=3\\cdot7=21$. '
        'Only choice 4 gives $21$.',
        'With $n=1$ the total is $3$, and both $3n^2$ and $3(2^n-1)$ give $3$. That is why we use $n=3$.'])
    S('wp21-g013', expl=[
        'All six tosses show $4$: $6\\times4=24$. Changing one $4$ to a $9$ adds $5$.',
        'The possible totals: $24, 29, 34, 39, 44, 49, 54$.',
        '$24$, $39$ and $49$ are in the list. $41$ is skipped: from $39$ we jump to $44$. Choice 3.',
        'Faster: every total leaves remainder $4$ when divided by $5$. $41=40+1$ leaves remainder $1$.'])
    S('wp21-g014', stem='At a festival there are only dancers, singers and actors. There are $3$ times as many dancers as singers, '
                        'and there are more actors than dancers. There are $70$ performers in total. '
                        'Which of the following can be the number of dancers?',
      expl=[
          'There are $3$ times as many dancers as singers. Therefore the number of dancers must divide by $3$. '
          '$28$ does not. Choice 2 is out.',
          'Try $30$ dancers: $30\\div3=10$ singers and $70-30-10=30$ actors. The actors must be MORE than the dancers, '
          'but $30=30$. It fails.',
          'More dancers means fewer actors. Therefore $33$ fails too.',
          'Try $27$: $27\\div3=9$ singers and $70-27-9=34$ actors. $34>27$ ✓. Choice 1.'])
    S('wp21-g015', expl=[
        'Test each choice. Put that many boxes at exactly $3$, and check that every other box can have at least $4$.',
        '$10$ boxes: $10\\times3=30$. $86-30=56$ markers for $14$ boxes: $14\\times4=56$ ✓.',
        '$12$ boxes: $12\\times3=36$. $86-36=50$ markers for $12$ boxes: $11\\times4+6=50$ ✓.',
        '$15$ boxes: $15\\times3=45$. $86-45=41$ markers for $9$ boxes: $8\\times4+9=41$ ✓.',
        '$9$ boxes: $9\\times3=27$. The other $15$ boxes need at least $15\\times4=60$, and $27+60=87>86$ ✗. Choice 3.'])
    S('wp21-g017', stem='A quiz has between $12$ and $20$ questions (inclusive). Each of $16$ students answers at least '
                        '$\\frac14$ of the quiz correctly. What are the smallest and the largest possible totals of '
                        'correct answers in the class?',
      expl=[
          'Smallest: the shortest quiz ($12$ questions) and the smallest share: $\\frac14\\times12=3$ correct answers each. '
          '$16\\times3=48$.',
          'Largest: the longest quiz ($20$ questions), and every student answers all $20$ correctly. '
          '"At least $\\frac14$" allows more. $16\\times20=320$.',
          '$48$ and $320$. Choice 1.'])
    S('wp21-g018', expl=[
        'Smallest fifth jar: from the first jar, add the minimum $3$ each time: $6, 9, 12, 15, 18$.',
        'Largest fifth jar: from the last jar, go back $3$ each time: $42, 39, 36, 33, 30$.',
        'Both ends really happen: $6, 9, 12, 15, 18, 21, 24, 27, 42$ and $6, 9, 12, 15, 30, 33, 36, 39, 42$. Choice 3.'])
    S('wp21-g019', expl=[
        'One camper receives between $4+2=6$ and $6+5=11$ stickers.',
        'Fewest left: receive the least and give away the most: $6-3=3$. Most left: receive the most and give away the least: $11-1=10$.',
        'Seventeen campers: $17\\times3=51$ and $17\\times10=170$. Choice 4.'])
    S('wp21-g020', expl=[
        'Largest for Amir: give the others the least. Cara $1$, Beth $2$, Amir $30-1-2=27$. '
        '$28$ fails: it leaves $2$ counters, and $1+1$ are not different.',
        'Smallest for Amir: keep the three close. If Amir had $10$, the others could have at most $9$ and $8$: '
        '$10+9+8=27<30$ ✗.',
        'Amir $11$ works: $11+10+9=30$. Choice 2.'])
    S('wp21-g023', expl=[
        'Day 1: $58\\times2=116$, then $116-16=100$.',
        'Day 2: $100\\times2=200$, then $200-16=184$.',
        'Day 3: $184\\times2=368$. Stop here: they ask for the count BEFORE the day 3 deletion. Choice 1.',
        '$368-16=352$ is the trap: that is the count after the deletion.'])
    S('wp21-g024', expl=[
        'Compare lamps $1$ to $4$ with lamps $2$ to $5$. They share lamps $2$, $3$ and $4$, and each group has exactly one blue lamp. '
        'Therefore lamp $5$ is blue exactly when lamp $1$ is blue. The pattern repeats every $4$ lamps.',
        'Lamp $2$ is blue. Therefore the blue lamps are $2, 6, 10, 14, \\ldots$: the numbers that leave remainder $2$ when divided by $4$.',
        '$38=36+2$ leaves remainder $2$ ✓. $35$, $36$ and $37$ leave remainders $3$, $0$ and $1$. Choice 4.'])
    S('wp21-g025', expl=[
        'The lights flash together at every common multiple of $18$ and $24$. Jump along the bigger number: $24, 48, 72$. '
        '$72=4\\times18$ ✓. They flash together every $72$ minutes.',
        '07:30 is the first joint flash. Second: 08:42. Third: 09:54. Fourth: 11:06. Choice 1.',
        'Four flashes have only three gaps: $3\\times72=216$ minutes, which is $3$ hours and $36$ minutes after 07:30.'])

    # practice
    S('wp21-p01', expl=[
        'Test the choices. With $34$ triangles, $120-34=86$ pieces are left: $86\\div2=43$ circles and $43$ squares. $43>34$ ✓.',
        '$21$: $120-21=99$ is odd and cannot split into two equal groups. '
        '$44$: $76\\div2=38<44$ ✗. $50$: $70\\div2=35<50$ ✗. Choice 4.'])
    S('wp21-p02', expl=[
        'Fewer than $7$ means at most $6$. Fewer than $6$ means at most $5$.',
        'Sketchbooks: smallest $8+0=8$, largest $14+6=20$.',
        'Brush cases: smallest $0+3=3$, largest $5+9=14$. Choice 1.'])
    S('wp21-p03', expl=[
        'Four $2$-credit vouchers: $4\\times2=8$. Changing a $2$ to a $7$ adds $5$. Changing a $2$ to a $12$ adds $10$.',
        'Every price is $8$ plus a multiple of $5$: $8, 13, 18, 23, 28, 33, 38, \\ldots$',
        'Check: $38-8=30$ ✓, $18-8=10$ ✓, $28-8=20$ ✓, $31-8=23$ ✗ (not a multiple of $5$). Choice 2.'])
    S('wp21-p04', expl=[
        'Three museum passes: $3\\times60=180$. There are $8-3=5$ more passes.',
        'Cheapest: five film passes, $5\\times30=150$. Total: $180+150=330$.',
        'Most expensive: five workshop passes, $5\\times120=600$. Total: $180+600=780$. Choice 2.'])
    S('wp21-p05', expl=[
        'Monday: start $24$ → sell $12$, keep $12$ → add $3\\times12=36$ → end $12+36=48$.',
        'Tuesday: start $48$ → sell $24$, keep $24$ → add $3\\times24=72$ → end $24+72=96$.',
        'Wednesday: start $96$ → sell $48$, keep $48$ → add $3\\times48=144$ → end $48+144=192$. Choice 4.'])
    S('wp21-p06', stem='The sequence is $1,\\ \\frac13,\\ \\frac19,\\ \\frac1{27},\\ldots$ Which of the following statements is NOT true?',
      expl=[
          'Each term is the one before it divided by $3$: $1\\div3=\\frac13$, $\\frac13\\div3=\\frac19$, and so on.',
          'Statement 1: $\\frac13=3\\times\\frac19$ ✓. Statement 2: the terms get smaller ✓. '
          'Statement 3: the gaps are $\\frac23, \\frac29, \\frac2{27}, \\ldots$, and they get smaller ✓.',
          'Statement 4: a positive number divided by $3$ stays positive. No term is negative. '
          'Statement 4 is not true. Choice 4.'])
    S('wp21-p07', stem='Twenty-eight badges are divided among $n$ teams. Each team receives a different positive number of badges. '
                       'Which value of $n$ is impossible?',
      choices=['$8$', '$3$', '$4$', '$7$'],
      expl=[
          '$n$ teams need at least $1+2+\\ldots+n=\\frac{n(n+1)}{2}$ badges.',
          '$n=8$: $\\frac{8\\cdot9}{2}=36>28$ ✗. $n=7$: $\\frac{7\\cdot8}{2}=28$ ✓ (the teams get $1$ to $7$).',
          '$n=3$ and $n=4$ also work, for example $1+2+25$ and $1+2+3+22$. Choice 1.'])
    S('wp21-p08', expl=[
        'A seat with both labels has a number divisible by $6$ and by $9$. The smallest common multiple of $6$ and $9$ is $18$ '
        '(jump along $9$: $9, 18$ ✓).',
        'Seats $18, 36, \\ldots, 270$: $270\\div18=15$ seats. Choice 4.'])
    S('wp21-p09', expl=[
        'At most $6$ of the $9$ guests are musicians. Therefore at least $9-6=3$ are actors.',
        'Fewest posters: $6$ musicians and $3$ actors: $6\\times2+3\\times4=12+12=24$.',
        'Most posters: $8$ actors and $1$ musician: $8\\times4+1\\times2=32+2=34$. Choice 3.'])
    S('wp21-p10', expl=[
        '$42$ correct answers: $42\\times3=126$. Changing one correct answer to a wrong one: lose $3$, and lose $2$ more: $-5$.',
        'Possible scores: $126, 121, 116, 111, \\ldots$ They all leave remainder $1$ when divided by $5$.',
        '$116$ is in the list ✓. $114$, $118$ and $120$ are not. Choice 1.'])
    S('wp21-p11', expl=[
        'Seven $2$-point results: $7\\times2=14$. Each $5$ instead of a $2$ adds $3$.',
        'Possible totals: $14, 17, 20, 23, 26, 29, 32, 35$.',
        'The only one divisible by $8$ is $32=4\\times8$. Choice 4.'])
    S('wp21-p12', stem='There are $18$ robots in room A, and any of them may be blue. At least half of the robots move to room B. '
                       'At least four of the robots that stay in room A are blue. What are the smallest and the largest possible '
                       'numbers of blue robots that move to room B?',
      expl=[
          'Smallest: $0$. Let $9$ robots that are not blue move to B. The $9$ robots that stay are all blue ✓.',
          'Largest: at least $4$ blue robots must stay in A. Therefore at most $18-4=14$ robots move, '
          'and all $14$ can be blue ($14\\ge9$ ✓). Choice 2.'])
    S('wp21-p13', expl=[
        'List the mixes of $5$ packages that make $28$ kg, by the number of $8$-kg packages. '
        'Four $8$s already weigh $32$ kg: too much.',
        'Three $8$s: the other two make $4$ kg: $2+2$. Cost: $3\\times10+2\\times3=36$.',
        'Two $8$s: the other three make $12$ kg: $2+4+6$ (cost $37$) or $4+4+4$ (cost $38$).',
        'One $8$: the other four make $20$ kg: $2+6+6+6$ (cost $37$) or $4+4+6+6$ (cost $38$).',
        'No $8$s: $4+6+6+6+6$ (cost $38$).',
        'The lowest cost is $36$. Choice 2.'])
    S('wp21-p14', expl=[
        'Worst luck $+\\,1$: the game lasts longest when every player gets as many wins as possible without ending it: $3$ wins each.',
        '$4\\times3=12$ rounds, and still no one has $4$ wins. Round $13$ must give someone a fourth win.',
        '$13\\times5=65$ minutes. Choice 3.'])
    S('wp21-p15', expl=[
        'The yellow share $\\frac{Y}{Y+B}$ is largest with the most yellow and the fewest black: $Y=9$ and $B=5$.',
        '$\\frac{9}{9+5}=\\frac{9}{14}$. Choice 2.'])
    S('wp21-p16', stem='A $148$-meter fence is painted in $3$-meter stripes, with $2$-meter unpainted gaps between the stripes. '
                       'The stripes must be complete. What is the greatest possible number of painted stripes?',
      expl=[
          '$n$ stripes have $n-1$ gaps between them. Length: $3n+2(n-1)=5n-2$.',
          '$n=30$: $5\\times30-2=148$ ✓. $n=31$: $5\\times31-2=153>148$ ✗. Choice 4.'])
    S('wp21-p17', stem='A craft workshop has four ribbons: $18$, $10$, $5$ and $3$ meters long. Each ribbon may be used once, '
                       'either at its full length or folded once to half its length. Any of the ribbons may be joined together; '
                       'a joined ribbon cannot be folded. Which length cannot be made?',
      expl=[
          'Check the choices. $28=18+10$ ✓. $18$: the $18$-m ribbon alone ✓. $\\frac{23}{2}=11.5=10+1.5$ '
          '(the $3$-m ribbon folded) ✓.',
          '$7$: the $18$-m ribbon is too long even folded ($9$). The $10$-m ribbon can only be used folded: $5$.',
          'Without it, the $5$-m ribbon ($5$ or $2.5$) and the $3$-m ribbon ($3$ or $1.5$) give only '
          '$1.5$, $2.5$, $3$, $4$, $5$, $5.5$, $6.5$ and $8$. No $7$.',
          'With the $5$ from the $10$-m ribbon, we need $2$ more, and nothing gives exactly $2$. '
          'Therefore $7$ cannot be made. Choice 2.'])
    S('wp21-p18', expl=[
        'A total is $7a+b$, with $a$ from $0$ to $4$ (sevens) and $b$ from $0$ to $3$ (ones).',
        'The totals form blocks: $0$–$3$, $7$–$10$, $14$–$17$, $21$–$24$, $28$–$31$. '
        'Each block ends before the next one starts. No total is counted twice.',
        '$5\\times4=20$ totals, minus the total $0$: $19$. Choice 3.'])
    S('wp21-p19', expl=[
        'Remote volunteers: $\\frac13\\times27=9$. Editors are more than $9$: at least $10$.',
        'Editors are fewer than translators, and together they are $27$. $13$ editors and $14$ translators works; '
        '$14$ editors and $13$ translators does not. Therefore there are at most $13$ editors.',
        'Translators $=27-$ editors: from $27-13=14$ to $27-10=17$. Choice 4.'])
    S('wp21-p20', expl=[
        'Seven volunteers means $6$ ADDITIONAL volunteers, not $7$.',
        'Each rate: $8+6\\times3=8+18=26$ parcels per hour.',
        'Total: $7\\times26=182$. Choice 3.'])
    S('wp21-p21', expl=[
        'Each cycle: $-3+5=+2$ cards.',
        'Six cycles: $6\\times2=12$. $35+12=47$. Choice 4.'])
    S('wp21-p22', expl=[
        'The lights flash together at every common multiple of $8$ and $14$. Jump along the bigger number: '
        '$14, 28, 42, 56$. $56=7\\times8$ ✓.',
        'Joint flashes: $0, 56, 112, 168$. Time $0$ is the first. The fourth is at $3\\times56=168$ seconds. Choice 2.'])
    S('wp21-p24', stem='In a row of $52$ lockers, every group of four neighboring lockers contains exactly one red locker. '
                       'Locker $2$ is red. Which locker must also be red?',
      expl=[
          'Moving from lockers $1$ to $4$ to lockers $2$ to $5$ removes locker $1$ and adds locker $5$. '
          'Both groups have exactly one red locker. Therefore locker $5$ has the same color as locker $1$: '
          'the pattern repeats every $4$.',
          'Red lockers: $2, 6, 10, \\ldots$, the numbers that leave remainder $2$ when divided by $4$.',
          '$46=44+2$ ✓. $43$, $45$ and $48$ leave remainders $3$, $1$ and $0$. Choice 1.'])
    S('wp21-p25', expl=[
        'Fill every box to the minimum: $16\\times3=48$. Spare pencils: $58-48=10$.',
        'Each spare pencil can lift one box above $3$. At most $10$ boxes rise.',
        'At least $16-10=6$ boxes stay at exactly $3$. Choice 4.'])
    S('wp21-p27', expl=[
        'To make the highest score as large as possible, give the other four the least: $1+2+3+4=10$.',
        'The highest score: $43-10=33$. It is different from $1, 2, 3, 4$ ✓. Choice 2.'])

    # Pass 2: p23 and p26 are original questions and stay (plan: RESTORE); text clean-up only
    S('wp21-p23', stem='Thirty-six stickers are given to children. Each child receives a different positive whole number of stickers. '
                       'What is the greatest possible number of children?',
      expl=['To have as many children as possible, give each child as few stickers as possible: $1, 2, 3, \\ldots$',
            'Eight children: $1+2+3+\\ldots+8=\\frac{8\\cdot9}{2}=36$ ✓. All $36$ stickers are given out.',
            'Nine children would need at least $36+9=45>36$ ✗. Choice 4.'])
    S('wp21-p26', expl=[
        'Six small packs: $6\\times4=24$ markers. Changing a small pack to a large one adds $9-4=5$.',
        'The possible totals: $24, 29, 34, 39, 44, 49, 54$.',
        '$24$, $39$ and $54$ are in the list. $42$ is skipped: from $39$ we jump to $44$. Choice 4.'])

    # =====================================================================================
    # 6. New practice: worst case, must be true, formula sequences, days of the week, last digits
    # =====================================================================================
    NEW = [
        ('03', 'A box holds $5$ white, $7$ black and $9$ gray balls. You take balls out without looking. '
               'What is the smallest number of balls you must take out to be sure you have at least $2$ black balls?',
         ['$4$', '$15$', '$16$', '$21$'], 3, [
             'Worst luck: all the balls that are not black come out first: $5+9=14$.',
             'Then $2$ black balls: $14+2=16$. Choice 3.',
             '$15$ is not enough: $14$ balls that are not black and only $1$ black ball.',
             '$4=3+1$ answers a different question: $2$ balls of the SAME color.']),
        ('04', 'A box has $20$ cards, numbered $1$ to $20$. What is the smallest number of cards you must draw '
               'to be sure that two of your cards add up to $21$?',
         ['$10$', '$11$', '$20$', '$21$'], 2, [
             'The pairs that add up to $21$: $1+20$, $2+19$, $\\ldots$, $10+11$. That is $10$ pairs.',
             'Worst luck: one card from every pair, for example $1$ to $10$. That is $10$ cards, and no two of them add up to $21$.',
             'The next card completes a pair: $10+1=11$. Choice 2.']),
        ('05', 'A class has $30$ students. Which of the following must be true?',
         ['At least $2$ students were born in January.', 'At least $3$ students were born in the same month.',
          'At least $4$ students were born in the same month.', 'No month has more than $3$ of the students\' birthdays.'], 2, [
             'Worst luck: spread the birthdays as evenly as possible. $12$ months with $2$ students each is only $12\\times2=24$ students.',
             '$30>24$. Therefore some month has at least $3$ students ✓. Choice 2.',
             'The others are not certain. Choice 1: all $30$ may be born in March. Choice 4: the same example breaks it. '
             'Choice 3: $6$ months with $3$ and $6$ months with $2$ gives $18+12=30$, and no month has $4$.']),
        ('06', 'Three friends share $25$ marbles. Each friend gets a different number of marbles, and each gets at least one. '
               'Which of the following must be true?',
         ['The largest share is at least $10$.', 'The smallest share is at most $6$.',
          'At least one share is an even number.', 'The largest share is at most $20$.'], 1, [
             'Look for counterexamples. $7+8+10=25$: the smallest share is $7$ (choice 2 ✗). '
             '$1+3+21=25$: all shares are odd (choice 3 ✗) and the largest is $21$ (choice 4 ✗).',
             'Choice 1: if the largest share were at most $9$, the other two would be at most $8$ and $7$: '
             '$9+8+7=24<25$ ✗. Therefore the largest share is at least $10$ ✓. Choice 1.']),
        ('07', 'The first term of a sequence is $5$, and each term is $4$ more than the term before it. '
               'Which expression gives the $n$-th term of the sequence?',
         ['$5n$', '$4n+1$', '$4n+5$', '$n+4$'], 2, [
             'Plug in $n=3$. The terms are $5$, $9$, $13$. The third term is $13$.',
             'Put $n=3$ into each choice: $5\\cdot3=15$, $4\\cdot3+1=13$, $4\\cdot3+5=17$, $3+4=7$. Only choice 2 gives $13$.',
             'With $n=1$ both $5n$ and $4n+1$ give $5$. That is why we use $n=3$.']),
        ('09', 'Which expression is equal to the sum of the first $n$ even positive numbers, $2+4+6+\\ldots+2n$?',
         ['$2n^2$', '$n^2$', '$n(n+1)$', '$n(n+2)$'], 3, [
             'Plug in $n=3$: $2+4+6=12$.',
             'Put $n=3$ into each choice: $2\\cdot9=18$, $9$, $3\\cdot4=12$, $3\\cdot5=15$. Only choice 3 gives $12$.',
             'With $n=1$ the sum is $2$, and both $2n^2$ and $n(n+1)$ give $2$. $n=1$ is not enough.']),
        ('10', 'Today is Monday. What day of the week will it be $100$ days from today?',
         ['Tuesday', 'Thursday', 'Wednesday', 'Friday'], 3, [
             'The days of the week repeat every $7$ days. $100=14\\times7+2$.',
             'After $14\\times7=98$ days it is Monday again. Two more days: Wednesday. Choice 3.',
             'Tuesday is the trap: it counts today as day $1$.']),
        ('11', 'What is the units digit of $7^{50}$?',
         ['$1$', '$3$', '$7$', '$9$'], 4, [
             'The last digits of the powers of $7$: $7^1=7$, $7^2=49$, $7^3=343$, $7^4=2401$. '
             'The last digits $7, 9, 3, 1$ repeat every $4$.',
             '$50=12\\times4+2$. Remainder $2$: the second digit in the cycle, $9$. Choice 4.']),
    ]
    for k, stem, ch, cor, ex in NEW:
        qid = 'q-r26-t21-' + k
        M.new_q(qid, TOPIC, stem, ch, cor, ex)
        M.place_q(qid, PRAC)

    P = lambda k: 'q-r26-t21-' + k
    M.practice_order(PRAC, [
        'wp21-p21', 'wp21-p02', 'wp21-p04', 'wp21-p01', 'wp21-p08', 'wp21-p22', 'wp21-p27', 'wp21-p07', 'wp21-p16',
        'wp21-p11', 'wp21-p10', 'wp21-p23', P('07'), P('10'), P('11'), P('03'), 'wp21-p05', 'wp21-p09', 'wp21-p15', 'wp21-p20',
        'wp21-p03', 'wp21-p26', 'wp21-p25', 'wp21-p14', 'wp21-p19', 'wp21-p24', 'wp21-p06', P('09'), P('05'), P('06'),
        'wp21-p12', P('04'), 'wp21-p13', 'wp21-p17', 'wp21-p18'])

    summary(M)


# =====================================================================================
# Pass 2: summary lesson right before the practice
# =====================================================================================
def summary(M):
    sb = ['Three types', 'Try in order', 'The skip', 'Push the right way', 'Different amounts',
          'Worst luck + 1', 'Patterns', 'Cycles', 'Before you practice']
    C = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of trial, limits and patterns.",
            "Everything important, one idea at a time."]),
        C(0, [
            A("'General · Minimum & maximum · Patterns' appears", T('General · Minimum & maximum · Patterns', size=46)),
            "Trial and error comes in three types.",
            "General problems: nothing tells you what to try first. So you try.",
            "Minimum and maximum: a little understanding tells you which way to push.",
            "Patterns: write it out, or plug in a number."]),
        C(1, [
            A("'Draw → follow → split into routes → test the choices' appears",
              T('Draw $\\to$ follow $\\to$ split into routes $\\to$ test the choices', size=40)),
            "Draw the story and follow it. It can go two ways? Split it into two routes.",
            "Often the fastest try: test the answer choices, one by one.",
            A("'Keep an order: no 5s, one 5, two 5s, …' appears", T('Keep an order: no $5$s, one $5$, two $5$s, $\\ldots$', size=42)),
            "Keep your tries in order. Then you know your list is complete.",
            "And every try must pass EVERY condition — including the question itself."]),
        C(2, [
            A("'3 parcels of 6 or 13 kg: 18, 25, 32, 39' appears",
              T('$3$ parcels of $6$ or $13$ kg: $\\ 18,\\ 25,\\ 32,\\ 39$', size=44)),
            "Two values that swap? Start from the minimum. Each swap is a constant step — here, plus seven.",
            A("'30? Remainder 2 when ÷ 7 — skipped' appears", T('$30$? $30\\div7$ leaves remainder $2$, not $4$ ✗', size=42)),
            "Thirty is inside the range — but it gets skipped. Inside the range is NOT enough.",
            "Test by remainder: every possible total leaves the same remainder."]),
        C(3, [
            A("'Max of one → give the others the least' appears", T('Max of one $\\to$ give the others the least', size=40)),
            A("'Min of the largest → share as equally as possible' appears",
              T('Min of the largest $\\to$ share as equally as possible', size=40)),
            A("'Min of one → give the others the most' appears", T('Min of one $\\to$ give the others the most', size=40)),
            "Three rules. Max of one: give the others the least. Min of the largest: share as equally as you can. Min of one: give the others the most.",
            A("'Prove the bound, then build it' appears", T('Prove the bound, then build it', size=40)),
            "Then two jobs: show nothing better fits — and build one real example that reaches it."]),
        C(4, [
            A("'1 + 2 + … + k = k(k+1)/2' appears", T('$1+2+3+\\ldots+k=\\frac{k(k+1)}{2}$', size=56)),
            "Everyone gets a DIFFERENT positive amount? The cheapest list is one, two, three, up to k.",
            A("'9 people need 45, 10 people need 55' appears",
              T('$50$ cards: $\\frac{9\\cdot10}{2}=45\\le50$ ✓ · $\\frac{10\\cdot11}{2}=55>50$ ✗', size=42)),
            "Fifty cards: nine people need at least forty-five — fine. Ten need fifty-five — too many.",
            A("'At least 2 in each box? Fill to the minimum, count the spares' appears",
              T('At least $2$ in each box? Fill to the minimum, then count the spares', size=40)),
            "Everyone has a minimum? Fill everyone to the minimum first. Then count what is spare."]),
        C(5, [
            A("'To be sure → worst luck + 1' appears", T('To be sure $\\to$ worst luck $+\\,1$', size=50)),
            "To be SURE? Imagine the worst luck — then add one.",
            A("'4 pens of one color: 3 + 3 + 3 = 9, then 9 + 1 = 10' appears",
              T('$4$ pens of one color, $3$ colors: $3+3+3=9$, then $9+1=10$', size=42)),
            "Four pens of one color: the worst luck is three of each. Nine pens, and still nothing. The tenth must do it.",
            "It's a maximum question in disguise: how long can the bad luck last?"]),
        C(6, [
            A("'Step by step → write 1, 2, 3, 4 in the rule order' appears",
              T('Step by step $\\to$ write $1,\\ 2,\\ 3,\\ 4$ in the rule order', size=42)),
            "A rule repeated round after round? Write the items one by one. Halve, then subtract — not the other way round.",
            A("'Sequences → plug in n = 3 · two survive? n = 4' appears",
              T('Sequences $\\to$ plug in $n=3$ · two survive? Also $n=4$', size=42)),
            "A formula with n in the choices? Plug in three and test every choice. n equals one often leaves two standing.",
            A("'Check both edges · items ≠ gaps' appears", T('Check both edges · items $\\ne$ gaps', size=42)),
            "And check the edges. Does the first step count? The last? Ten posts in a row have nine gaps."]),
        C(7, [
            A("'Cycle → divide by its length, use the remainder' appears",
              T('Cycle $\\to$ divide by its length, use the remainder', size=42)),
            "A repeating cycle? Divide by the cycle length and look at the remainder.",
            A("'Friday + 40 days: 40 = 35 + 5 → Wednesday' appears",
              T('Friday $+\\ 40$ days: $40=5\\cdot7+5\\to$ Wednesday', size=42)),
            "Days repeat every seven. Last digits of powers repeat too — write the first few and find the cycle.",
            "Remainder zero? Then it's the LAST one in the cycle.",
            A("'Every 8 and every 14 → jump with 14: 14, 28, 42, 56' appears",
              T('Every $8$ and every $14$ $\\to$ jump with $14$: $\\ 14,\\ 28,\\ 42,\\ 56$', size=40)),
            "Two things meeting again? A common multiple. Jump along the bigger number: fifty-six is the first one divisible by eight."]),
        C(8, [
            "Before you start, always ask yourself:",
            A("'Check 1' appears", T('Which type: general, min–max or pattern?', size=40)),
            A("'Check 2' appears", T('Which way do I push — and does my example really work?', size=40)),
            A("'Check 3' appears", T('Must or could? One counterexample kills "must".', size=40)),
            A("'Check 4' appears", T('Constant step? Is this choice skipped?', size=40)),
            A("'Check 5' appears", T('The edges: the first step, the last step, items or gaps?', size=40)),
            "And the traps: \"inside the range\" is not enough, n equals one alone is not enough, and \"at least\" is a floor — not the answer for a maximum.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t21-summary', TOPIC, 'Summary: Trial, Limits and Patterns', sb, slides, ADV, after=last)
