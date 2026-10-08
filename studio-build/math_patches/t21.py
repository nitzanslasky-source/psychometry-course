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
    cut_repeats(M)


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


# =====================================================================================
# 2026-10-05 cut repeats: each lesson back to a short intro (Hebrew style); every idea a
# question video already teaches is cut from the lesson; ideas no question teaches stay or
# move as one line + board item into the question video that uses them.
# =====================================================================================
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
    """Keep only the slides `keep` (1-based, in order); set the sidebar; renumber 'active'."""
    v = M.video(vid)
    M.remove_slides(vid, [k for k in range(1, len(v['beats']) + 1) if k not in keep])
    a = 0
    for b in v['beats']:
        if b.get('mode') == 'concept':
            b['active'] = a; a += 1
    M.set_sidebar(vid, sidebar)


def cut_repeats(M):
    # ---- General Problems: keep title + "Try and err" (the Hebrew intro) -------------------
    vid = 'wp-003'
    _keep_slides(M, vid, [1, 2], ['Try and err'])
    _add_line(M, vid, 2, None, "Let's see two questions of this type.")
    # "Keep an order" + "Every condition" -> one line in Q2 (queue)
    _add_line(M, 'solve-wp21-g005', 2, 'At least one of each type',
              "Keep your tries in order, and make every try pass every condition.",
              T('Tries in order · every try passes every condition', 36),
              "'Tries in order · every try passes every condition' appears")
    # "Draw the story / split into routes" -> taught in Q1 (crystals); "test the choices" -> Q2.

    # ---- Minimum & Maximum: keep title + Ranges + recurring motif -------------------------
    vid = 'wp-006'
    _keep_slides(M, vid, [1, 2, 3], ['Ranges', 'A recurring motif'])
    _add_line(M, vid, 3, None, "Let's see a real question of this type.")
    # "Bold words" -> Q3 already circles the key word; add that it is printed in bold
    _fix_say(M, 'solve-wp21-g007', 2, 'Find the key word and circle it',
             'Find the key word — on the exam it is printed in bold — and circle it')
    # "Cheapest k different": Q3 method 2 gives the formula; move the "why" (pair the ends) there
    _add_line(M, 'solve-wp21-g007', 3, 'Seven people cost at least',
              "Why? Pair the ends of one to eight: one plus eight, two plus seven — four pairs of nine. Thirty-six.",
              T(r'$1+8=2+7=3+6=4+5=9 \;\to\; 4\times9=36$', 36),
              "'1 + 8 = 2 + 7 = 3 + 6 = 4 + 5 = 9 → 4 × 9 = 36' appears")
    # "Squeeze the others" -> Q3 ("give each one as little as possible"); "Balance the group" and
    # the 26 = 1 + 2 + 23 / 7 + 9 + 10 example -> still in "More Minimum & Maximum" (same numbers).

    # ---- Patterns: keep title + one short "two kinds" slide -------------------------------
    vid = 'wp-008'
    _keep_slides(M, vid, [1, 2], ['Two kinds'])
    M.set_slide(vid, 2, title='Two kinds', pre=[], script=[
        'Patterns come in two kinds.',
        A("'1 · Step by step → write the items one by one' appears", T(r'$1$ · Step by step $\to$ write the items one by one', 40)),
        'The first kind: step by step. The simplest, best way: write the items one at a time, exactly as the rule says, until you reach what they ask.',
        A("'2 · Sequences with n → plug in a number' appears", T(r'$2$ · Sequences with $n$ $\to$ plug in a number', 40)),
        'The second kind: a sequence with a formula in n. Rarer. We plug in a number and check the answers.',
        "One question of each kind — let's see them."])
    # "Keep the rule order" -> one line in Q4 (training rounds)
    _add_line(M, 'solve-wp21-g009', 2, 'Round two: half of forty-six',
              "Keep the rule's order: halve first, then subtract. And the drops won't be equal — so apply the rule every round.",
              T('Halve, then subtract — every round', 36),
              "'Halve, then subtract — every round' appears")
    # "Sequences" + "Plug in n = 3" -> taught in Q5 (crates); move "two survive? try n = 4" there
    _add_line(M, 'solve-wp21-g010', 3, None,
              "And if two choices still survive n equals three? Plug in four as well.",
              T(r'Two survive? Also try $n=4$', 36), "'Two survive? Also try n = 4' appears")

    # ---- Smart Trial & Error: keep title + "Why it matters" (the Hebrew motivation) -------
    vid = 'wp-012'
    _keep_slides(M, vid, [1, 2], ['Why it matters'])
    _add_line(M, vid, 2, None, "Now the techniques that make it faster — we'll learn them in the questions.")
    # "Work in order", "The skip", "Constant step" -> all taught in the token question (Q6)
    _add_line(M, 'solve-wp21-g013', 2, 'Now swap one four for a nine',
              "Only how many fours and nines matters — not which toss came first.")
    _add_line(M, 'solve-wp21-g013', 2, 'Circle choice 3',
              "Forty-one is inside the range — and still impossible. Inside the range is not enough.",
              T('Inside the range is NOT enough', 36), "'Inside the range is NOT enough' appears")
    # "Constant step": its second test (subtract the minimum) -> Q6 method 2
    _add_line(M, 'solve-wp21-g013', 3, 'Choice three — without listing',
              "Same test another way: subtract twenty-four. You need zero, five, ten — a multiple of five. Forty-one minus twenty-four is seventeen. Not a multiple of five.",
              T(r'$41-24=17$ — not a multiple of $5$ ✗', 36), "'41 − 24 = 17 — not a multiple of 5 ✗' appears")

    # ---- More Minimum & Maximum: keep title + the three rules -----------------------------
    vid = 'wp-016'
    _keep_slides(M, vid, [1, 2], ['Three min/max rules'])
    _add_line(M, vid, 2, None, "Now the nuances — in the questions.")
    # "At least" -> Q10 (quiz); "Worst luck + 1" -> Q9 (socks); "Prove, then build" -> Q9 board item
    _add_line(M, 'solve-q-r26-t21-01', 2, 'Both halves: six can fail',
              "That's the rule for every min or max: show nothing more extreme works — and build a real example.",
              T('Min or max: prove the bound · build an example', 36),
              "'Min or max: prove the bound · build an example' appears")

    # ---- Patterns & Cycles: keep title + Days and last digits (no question teaches it) ----
    vid = 'wp-022'
    _keep_slides(M, vid, [1, 5], ['Days and last digits'])
    _fix_say(M, vid, 2, 'The same remainder trick solves two exam favorites.',
             'One remainder trick solves two exam favorites.')
    _fix_say(M, vid, 2, 'Lamps, days, digits — same tool', 'Days, digits — and the lamps in the questions — same tool')
    _add_line(M, vid, 2, None, "Let's see patterns in real questions.")
    # "Term by term" + "Watch the edges" -> Q16 (files); "Repeating cycles" -> Q17 (lamps);
    # "Meeting times" -> Q18 (lights). "Items vs gaps" -> one line in Q18 (4 flashes = 3 gaps):
    _add_line(M, 'solve-wp21-g025', 3, 'Write "7:30 → 8:42',
              "Four flashes have only three gaps between them. Items and gaps are different counts.",
              T(r'$4$ flashes $\to$ $3$ gaps of $72$ min', 36), "'4 flashes → 3 gaps of 72 min' appears")


# ======================================================================================================
# 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived question (guided wp21-g004 ..
# g025, practice wp21-p01 .. p20) gets a new story (names, objects, setting) and new numbers - same concept, same trap,
# same level, at least the same methods - and every guided solution video is rewritten to match. wp21-g021 was the same
# question as wp21-g015 word for word (the Hebrew returns to its planters question); it is now a different question of
# the same type, so the "shortcut" video teaches the method on new numbers. g017 + g018 (easy) move before the socks
# question (medium). Practice clean-up: 35 -> 26. Nothing in topic 21 is recorded. Runs last.
# ======================================================================================================
RN_RECORDED = set()   # no take of any topic-21 video in ~/Documents/Course.recordings (checked 2026-10-06)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_item(M, vid, n, text):
    b = M.slide(vid, n)
    for l in b['lines']:
        if 'appear' in l and text in (b['items'][l['appear']].get('t') or ''):
            return A(l['label'], b['items'][l['appear']])
    raise AssertionError('%s #%d: no item %s' % (vid, n, text))


def _rn_video(M, qid, slides, intro=()):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. slides: [script] or
    [(title, script)]. intro: (old, new) substring swaps in the title slide's spoken lines."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for old, new in intro:
        _fix_say(M, vid, 1, old, new)
        assert any(new in (l.get('say') or '') for l in M.slide(vid, 1)['lines']), (vid, old)
    for n, sl in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        title, script = sl if isinstance(sl, tuple) else (None, sl)
        M.set_slide(vid, n, title=title, script=script)
    q = M.q(qid)
    v['title'] = v['navLabel'] = q['stem']


def _seq(values, labels):
    return {'k': 'vis', 'v': {'type': 'sequence', 'values': values, 'labels': labels}, 'w': 1000, 'h': 230}


def _table(headers, rows, **k):
    d = {'k': 'vis', 'v': {'type': 'table', 'headers': headers, 'rows': rows}}
    d.update(k)
    return d


def rn_guided_learn(M):
    # ---------- g004: crystals 2 large, large -> 4 small, 3 breaks -> 7  ==>  bubbles, large -> 5 small, 3 pops -> 9
    _rn_q(M, 'wp21-g004', 'A phone game starts with 2 large bubbles on the screen. Popping a large bubble splits it into 5 small '
          'bubbles. Popping a small bubble makes it disappear. After exactly 3 pops, how many bubbles can be on the screen?',
          ['5', '6', '9', '10'], 3, [
        'Pop 1 must hit a large bubble (there are no small ones yet): $2-1+5=6$ bubbles ($1$ large, $5$ small).',
        'Pop 2 on the other large bubble: $6-1+5=10$, all small. Pop 3 removes one small bubble: $10-1=9$.',
        'The other route: pop 2 on a small bubble gives $6-1=5$. Then pop 3 gives $5-1+5=9$ or $5-1=4$.',
        'The only possible totals are $4$ and $9$. Of the choices, only $9$ appears. Choice 3.'])
    lab = ['Start', 'Pop 1', 'Pop 2', 'Pop 3']
    _rn_video(M, 'wp21-g004', [[
        "General problem. No hint what to pop first — so we just follow the game.",
        A('A row of boxes appears: Start 2 · Pop 1 · Pop 2 · Pop 3', _seq(['2', '?', '?', '?'], lab)),
        "We start with two large bubbles.",
        "Pop one: there are no small bubbles yet — so it has to hit a large one.",
        D('Under Pop 1 write 6 (1 large + 5 small)'),
        "One large disappears, five small appear. One large plus five small: six.",
        "Now the road splits. Let's take one road: pop the other large bubble.",
        D('Under Pop 2 write 10'),
        "It turns into five more small ones. Ten small bubbles.",
        "Pop three: only small ones left. One disappears.",
        D('Under Pop 3 write 9, then circle choice 3'),
        "Nine — and nine is in the choices. Lucky on the first road. That's this type: sometimes the first try just works.",
    ], [
        "What if we'd taken the other road?",
        A('A second row appears: Start 2 · Pop 1 6 · Pop 2 · Pop 3', _seq(['2', '6', '?', '?'], lab)),
        "Same first pop: six. But now pop a small bubble instead.",
        D('Under Pop 2 write 5'),
        "One large, four small: five.",
        "Pop three: pop the large one — four small plus five new small: nine again.",
        "Or pop a small one — one large, three small: four.",
        D('Under Pop 3 write "9 or 4"'),
        "Four isn't in the choices. If this had been your first road, you'd simply try again. Try — and err.",
        D('Circle choice 3'),
        "Every road ends at nine or four. The only one on the list: nine. Choice three.",
    ], [
        "One more way to check it — the net change.",
        "A large pop: lose one, gain five — net plus four. A small pop: minus one.",
        D('Write 2 + 4 + 4 − 1 = 9'),
        "Two large pops and one small: two, plus four, plus four, minus one. Nine.",
    ]], intro=[('a crystal game', 'a bubble game')])

    # ---------- g005: van 5 m, scooter 2 m, gap 1 m -> 10 impossible  ==>  truck 10 m, car 4 m, gap 2 m -> 20 impossible
    _rn_q(M, 'wp21-g005', 'A line of vehicles waits at a traffic light. It has at least one truck 10 m long and at least one car '
          '4 m long. There is a 2 m gap between neighboring vehicles, and no gap at either end of the line. '
          'Which total length of the line is impossible?',
          ['16', '20', '22', '28'], 2, [
        'One truck, one car and the gap between them: $10+2+4=16$ m. Therefore $16$ is possible.',
        'Each extra car adds its length and one more gap: $4+2=6$ m. Each extra truck adds $10+2=12$ m.',
        'From $16$: $16+6=22$ and $22+6=28$. Both are possible.',
        'The smallest step is $6$. From $16$ we jump straight to $22$, and $20$ is skipped. Therefore $20$ is impossible. Choice 2.',
        'Faster: give each vehicle the gap after it (truck $12$, car $6$) and remove the last gap: $L=12t+6c-2$. '
        'Therefore $L+2$ is always a multiple of $6$, but $20+2=22$ is not.'])
    _rn_video(M, 'wp21-g005', [[
        "Again, no shortcut. We build lines and test the answers.",
        _rn_item(M, 'solve-wp21-g005', 2, 'Tries in order'),
        "Keep your tries in order, and make every try pass every condition.",
        "At least one of each type — so we have no choice: start with one truck and one car.",
        D('Write 10 + 2 + 4 = 16'),
        "Truck ten meters, gap two, car four. Sixteen.",
        D('Cross out choice 1'),
        "Sixteen is possible — and they want the impossible one. Out.",
        "Quick-calculation tip: group the numbers into convenient chunks instead of adding one by one. "
        "Here, glue each extra vehicle to its gap. Car plus gap: six. Truck plus gap: twelve.",
        D('Write "+6" (car) and "+12" (truck)'),
        "Add a car: sixteen plus six, twenty-two. Possible.",
        D('Cross out choice 3'),
        "Twenty-eight: sixteen plus six plus six. Possible too.",
        D('Cross out choice 4'),
        "Now twenty. From sixteen, even the smallest addition — a car and its gap — jumps straight to twenty-two. We fly past twenty.",
        D('Circle choice 2'),
        "Twenty can't be built. That's our answer.",
        "Had you tested twenty first, you'd have found it right away — then it's worth checking the others, just to be sure.",
    ], [
        "A shorter check.",
        "Give every vehicle the gap after it: truck twelve, car six. But the last vehicle has no gap after it — minus two.",
        D('Write L = 12t + 6c − 2'),
        "So the length plus two is always a multiple of six.",
        D('Next to choice 2 write "20 + 2 = 22 ✗"'),
        "Twenty plus two is twenty-two — not a multiple of six. Twenty is impossible. Choice two.",
    ]], intro=[('a queue of vehicles', 'a line at a traffic light')])

    # ---------- g007: 32 pins, different amounts -> 7  ==>  42 postcards -> 8
    _rn_q(M, 'wp21-g007', 'Noa shares $42$ postcards among her friends. Each friend receives a different number of postcards '
          '(a positive integer), and all the postcards are given out. What is the largest possible number of friends?',
          ['7', '8', '9', '10'], 2, [
        'To have as many friends as possible, give each one as little as possible: $1, 2, 3, \\ldots$',
        'Eight friends need at least $1+2+3+4+5+6+7+8=\\frac{8\\cdot9}{2}=36$ postcards. Nine need at least $36+9=45$, '
        'and $45>42$. Therefore nine is impossible.',
        'Eight works: $1, 2, 3, 4, 5, 6, 7, 14$. The $42-36=6$ spare postcards go to the one who has the most. '
        'The sum is $42$, and all the amounts are different. Choice 2.'])
    pair_item = _rn_item(M, 'solve-wp21-g007', 3, '4\\times9=36')
    _rn_video(M, 'wp21-g007', [[
        "Find the key word — on the exam it is printed in bold — and circle it: the LARGEST possible number of friends.",
        "In theory she could give all forty-two postcards to one friend. Legal — but we want the most people.",
        "The key: to share among as many as possible, give each one as LITTLE as possible.",
        A('A table appears: friends 1–9, postcards and running total',
          _table(['Friend'] + [str(k) for k in range(1, 10)], [['Cards'] + [''] * 9, ['Total'] + [''] * 9], w=1130, h=160)),
        "Each gets at least one postcard — and all amounts are different.",
        D('Fill in the cards: 1, 2, 3, 4, 5, 6, 7, 8'),
        "One to the first. The second would love just one — but amounts must differ. Two. Then three, four, five, six, seven, eight.",
        D('Fill in the totals: 1, 3, 6, 10, 15, 21, 28, 36'),
        "Running total: thirty-six. Six postcards left.",
        "A ninth friend needs at least nine. We only have six. Goodbye, friend number nine.",
        D('Put ✗ under 9; change the 8 to 14'),
        "The six leftovers go to someone who already has postcards — the one with eight gets fourteen. Everything still different, everything used.",
        D('Circle choice 2'),
        "Eight friends. Choice two.",
    ], [
        "A shortcut for the same idea: the cheapest k different amounts cost k times k plus one, over two.",
        D('Write 8·9/2 = 36 ≤ 42 < 45 = 9·10/2'),
        pair_item,
        "Why? Pair the ends of one to eight: one plus eight, two plus seven — four pairs of nine. Thirty-six.",
        "Eight people cost at least thirty-six. Nine cost at least forty-five. Forty-two sits in between — eight.",
    ]], intro=[('sharing pins', 'sharing postcards')])

    # ---------- g009: 46 reps, halve then -1, round 4 -> 4  ==>  78 loaves on Monday, Thursday -> 8
    _rn_q(M, 'wp21-g009', 'A bakery bakes 78 loaves of bread on Monday. On each later day, it bakes half the number of loaves '
          'of the day before, minus 1. How many loaves does it bake on Thursday?',
          ['3', '8', '9', '18'], 2, [
        'Monday is given: $78$. Do not apply the rule to it.',
        'Tuesday: $78\\div2=39$, then $39-1=38$. Wednesday: $38\\div2=19$, then $19-1=18$. '
        'Thursday: $18\\div2=9$, then $9-1=8$. Choice 2.',
        'Keep the order: halve first, then subtract $1$. Don\'t subtract first: $78-1=77$ and then $77\\div2$ is the wrong order.',
        'From Monday to Thursday there are only three steps. $18$ is Wednesday, and a fourth step would give Friday ($3$).'])
    _rn_video(M, 'wp21-g009', [[
        "Patterns — the step-by-step kind. We just write the days.",
        A('A table appears: Monday to Thursday, 78 loaves on Monday',
          _table(['Day', 'Mon', 'Tue', 'Wed', 'Thu'], [['Loaves', '78', '', '', '']], w=760, h=110)),
        "Monday: seventy-eight. That's given — don't apply the rule to it.",
        D('Under Tue write 38'),
        A("'Halve, then subtract — every day' appears", T('Halve, then subtract — every day', 36)),
        "Keep the rule's order: halve first, then subtract. And the drops won't be equal — so apply the rule every day.",
        "Tuesday: half of seventy-eight is thirty-nine, minus one: thirty-eight.",
        D('Under Wed write 18'),
        "Wednesday: half of thirty-eight is nineteen, minus one: eighteen.",
        D('Under Thu write 8'),
        "Thursday: half of eighteen is nine, minus one: eight.",
        D('Circle choice 2'),
        "Eight loaves. Choice two.",
        "On the exam — no table. Just write the days and the numbers.",
    ], [
        "Want to be sure? Undo the rule in reverse: add one, then double.",
        D('Write 8 → 18 → 38 → 78'),
        "Eight, eighteen, thirty-eight, seventy-eight. Back where we started — and exactly three steps from Monday to Thursday.",
    ]], intro=[('training rounds', "a bakery's bread")])

    # ---------- g010: 3 crates doubling, total through day n -> 3(2^n - 1)  ==>  5 downloads -> 5(2^n - 1)
    _rn_q(M, 'wp21-g010', 'A new app is downloaded 5 times on day 1. On every later day, it is downloaded twice as many times '
          'as on the day before. How many times is it downloaded in total through day $n$?',
          ['$5(2^n-1)$', '$5n^2$', '$2^n+5$', '$5\\times2^n$'], 1, [
        'Plug in $n=3$. The days give $5$, $10$ and $20$ downloads. Total: $5+10+20=35$.',
        'Put $n=3$ into each choice: $5(2^3-1)=5\\cdot7=35$, $5\\cdot3^2=45$, $2^3+5=13$, $5\\cdot2^3=40$. Only choice 1 gives $35$.',
        'With $n=1$ the total is $5$, and both $5(2^n-1)$ and $5n^2$ give $5$. That is why we use $n=3$.'])
    _rn_video(M, 'wp21-g010', [[
        "Patterns — the sequence kind. A formula with n in every choice.",
        "No school formulas. We plug in n equals three.",
        D('Write 5 + 10 + 20 = 35'),
        "Day one: five downloads. Day two: twice that, ten. Day three: twenty. Total through day three: thirty-five.",
        "Now put n equals three into every choice. We're looking for thirty-five.",
        D('Next to the choices write 35, 45, 13, 40'),
        "Five times seven: thirty-five. Five times nine: forty-five. Eight plus five: thirteen. Five times eight: forty.",
        D('Circle choice 1'),
        "Only choice one gives thirty-five. That's the answer.",
    ], [
        "Why three and not one? One is quicker…",
        D('Write "n = 1: total 5 → 5, 5, 7, 10"'),
        "With n equals one, the total is five. Choice one gives five — and choice two gives five too. Two survivors.",
        "That's exactly how these questions are often built.",
        "Three is small enough to calculate, and big enough to separate the choices.",
        _rn_item(M, 'solve-wp21-g010', 3, 'Two survive'),
        "And if two choices still survive n equals three? Plug in four as well.",
    ]], intro=[('crates that keep doubling', 'downloads that keep doubling')])


def rn_guided_adv(M):
    # ---------- g013: token 4/9, 6 tosses, 41 impossible  ==>  chip 2/6, 7 tosses, 32 impossible
    _rn_q(M, 'wp21-g013', 'A plastic game chip has 2 written on one side and 6 on the other. It is tossed exactly 7 times, and the '
          'numbers that land face up are added. Which total is impossible?',
          ['38', '32', '14', '30'], 2, [
        'All seven tosses show $2$: $7\\times2=14$. Changing one $2$ to a $6$ adds $4$.',
        'The possible totals: $14, 18, 22, 26, 30, 34, 38, 42$.',
        '$14$, $30$ and $38$ are in the list. $32$ is skipped: from $30$ we jump to $34$. Choice 2.',
        'Faster: every total leaves remainder $2$ when divided by $4$. $32=8\\times4$ leaves remainder $0$.'])
    vid = 'solve-wp21-g013'
    inside = _rn_item(M, vid, 2, 'Inside the range')
    _rn_video(M, 'wp21-g013', [[
        "They ask what's impossible. So we find the possible totals and eliminate three.",
        "Work in order. Start from the minimum: all seven tosses show two.",
        D('Write "2×7 = 14" and cross out choice 3'),
        "Fourteen. It's possible — so choice three is out.",
        "Only how many twos and sixes matters — not which toss came first.",
        "Now swap one two for a six. That's plus four.",
        D('Write "→ 18 → 22 → 26 → 30" and cross out choice 4'),
        "Eighteen, twenty-two, twenty-six, thirty. Thirty is possible — so choice four is out.",
        D('Write "→ 34" and circle the jump from 30 to 34'),
        "Next swap: thirty-four. We just jumped from thirty to thirty-four — and skipped thirty-two!",
        inside,
        "Thirty-two is inside the range — and still impossible. Inside the range is not enough.",
        D('Circle choice 2'),
        "That's the skip. Thirty-two can never happen. Choice two — we can stop right here.",
        "For practice: two more swaps give thirty-eight — choice one — so it really is possible.",
    ], [
        "Now the fast way. Every swap adds four, so all the totals follow one pattern.",
        D('Write "14, 18, 22, 26, 30, 34, 38, 42 → remainder 2 when ÷ 4"'),
        "Divide any of them by four — remainder two, every time.",
        D('Next to 32 write "32 ÷ 4 → remainder 0 ✗"'),
        "Thirty-two leaves remainder zero. It breaks the pattern.",
        D('Circle choice 2'),
        A("'32 − 14 = 18 — not a multiple of 4 ✗' appears", T('$32-14=18$ — not a multiple of $4$ ✗', 36)),
        "Same test another way: subtract fourteen. You need zero, four, eight — a multiple of four. "
        "Thirty-two minus fourteen is eighteen. Not a multiple of four.",
        "Choice two — without listing a single toss.",
    ]])

    # ---------- g014: festival, dancers = 3 x singers, actors > dancers, 70 -> 27  ==>  choir, sopranos = 3 x altos, 63 -> 24
    _rn_q(M, 'wp21-g014', 'A choir has only sopranos, altos and tenors. There are $3$ times as many sopranos as altos, and there '
          'are more tenors than sopranos. The choir has $63$ singers in total. Which of the following can be the number of sopranos?',
          ['27', '30', '24', '26'], 3, [
        'There are $3$ times as many sopranos as altos. Therefore the number of sopranos must be divisible by $3$. $26$ is not. Choice 4 is out.',
        'Try $27$ sopranos: $27\\div3=9$ altos and $63-27-9=27$ tenors. The tenors must be MORE than the sopranos, but $27=27$. It fails.',
        'More sopranos means fewer tenors. Therefore $30$ fails too.',
        'Try $24$: $24\\div3=8$ altos and $63-24-8=31$ tenors. $31>24$ ✓. Choice 3.'])
    _rn_video(M, 'wp21-g014', [[
        "Why 'which number can it be' and not an exact number? Because the data only gives a range.",
        "Four answers — just test them. But start from the middle, with a convenient one: twenty-seven.",
        D('Write "27 sopranos → 9 altos → 63 − 36 = 27 tenors"'),
        "Twenty-seven sopranos means nine altos. That leaves twenty-seven tenors.",
        "But the tenors must be MORE than the sopranos. Twenty-seven equals twenty-seven — not more. Fails.",
        D('Cross out choices 1 and 2'),
        "And more sopranos only means fewer tenors — so thirty fails too. One plug, two answers gone.",
        "That's why we plug from the middle: it tells us which direction to go.",
        D('Write "24 → 8 altos → 31 tenors ✓"'),
        "Try twenty-four: eight altos, thirty-one tenors. Thirty-one is more than twenty-four. It works.",
        D('Circle choice 3'),
        "Numbers in the answers? The moment one works, mark it. There can't be two possible answers. Choice three.",
    ], [
        "There's an even faster cut.",
        "Three times as many sopranos as altos — so the number of sopranos MUST be divisible by three.",
        D('Next to choice 4 write "26 ÷ 3 ✗" and cross it out'),
        "Twenty-six isn't divisible by three. Gone, without any story.",
        "If something is twice another number — it must be even. Three times — divisible by three.",
        D('Circle choice 3'),
        "Together with the middle plug, that leaves twenty-four. Choice three.",
    ]])

    # ---------- g015: 24 boxes, 86 markers, >= 3 each -> 9 impossible  ==>  22 baskets, 80 apples -> 7 impossible
    _rn_q(M, 'wp21-g015', 'Twenty-two baskets hold 80 apples altogether. Every basket holds at least 3 apples. Which number '
          'cannot be the number of baskets holding exactly 3 apples?',
          ['8', '11', '15', '7'], 4, [
        'Test each choice. Put that many baskets at exactly $3$, and check that every other basket can have at least $4$.',
        '$8$ baskets: $8\\times3=24$. $80-24=56$ apples for $14$ baskets: $14\\times4=56$ ✓.',
        '$11$ baskets: $11\\times3=33$. $80-33=47$ apples for $11$ baskets: $10\\times4+7=47$ ✓.',
        '$15$ baskets: $15\\times3=45$. $80-45=35$ apples for $7$ baskets: $6\\times4+11=35$ ✓.',
        '$7$ baskets: $7\\times3=21$. The other $15$ baskets need at least $15\\times4=60$, and $21+60=81>80$ ✗. Choice 4.'])
    _rn_video(M, 'wp21-g015', [[
        "Twenty-two baskets, eighty apples, at least three in each. Where do you even start?",
        "Some people try and wonder. Some just stare. Don't. Start plugging in the answers.",
        "They ask what CANNOT be — so we find what can, and eliminate. Start with the easy one: eight.",
        D('Write "8×3 = 24 → 56 left for 14 baskets = 4 each ✓" and cross out choice 1'),
        "Eight baskets of three: twenty-four apples. Fifty-six left for fourteen baskets — exactly four each. Works.",
        D('Write "11×3 = 33 → 47 left for 11 baskets ✓" and cross out choice 2'),
        "Eleven baskets: thirty-three. Forty-seven left for eleven baskets — that's more than four each. More than four is fine!",
        "Ten baskets of four, and the last one gets seven. Works.",
        D('Write "15×3 = 45 → 35 left for 7 baskets ✓" and cross out choice 3'),
        "Fifteen baskets: forty-five. Thirty-five left for seven baskets — again more than four each. Works.",
        D('Circle choice 4'),
        "Three gone — choice four, seven. On the exam you stop here.",
        "Just to understand it: seven baskets of three is twenty-one. Fifty-nine left for fifteen baskets — LESS than four each.",
        "So another basket would be forced down to three. Seven can't work.",
        "Long? A minute or two. That's fine — the quick questions buy you the time. We'll come back to this type with a shortcut.",
    ]])

    # ---------- g017: quiz 12-20 questions, 16 students, >= 1/4 -> 48 and 320  ==>  test 10-25 words, 14 students, >= 1/5 -> 28 and 350
    _rn_q(M, 'wp21-g017', 'A spelling test has between $10$ and $25$ words (inclusive). Each of $14$ students spells at least '
          '$\\frac15$ of the words correctly. What are the smallest and the largest possible totals of correctly spelled words in the class?',
          ['70 and 350', '28 and 140', '28 and 350', '70 and 140'], 3, [
        'Smallest: the shortest test ($10$ words) and the smallest share: $\\frac15\\times10=2$ correct words each. $14\\times2=28$.',
        'Largest: the longest test ($25$ words), and every student spells all $25$ correctly. "At least $\\frac15$" allows more. $14\\times25=350$.',
        '$28$ and $350$. Choice 3.'])
    _rn_video(M, 'wp21-g017', [[
        "Start with one student. Smallest possible number of correct words?",
        "The shortest test — ten words — and the smallest share, one fifth.",
        D('Write "10 ÷ 5 = 2 → 14 × 2 = 28"'),
        "Two correct each. Fourteen students: twenty-eight.",
        D('Cross out choices 1 and 4'),
        "Choices one and four start with seventy. Gone.",
        "Now the maximum: the longest test — twenty-five words. And 'at least a fifth' means they can get ALL of them right.",
        D('Write "14 × 25 = 350" and circle choice 3'),
        "Fourteen times twenty-five: three hundred fifty. Choice three.",
    ], [
        "The last-digit trick — and where it stops.",
        D('Write "2 × 4 → ends in 8"'),
        "Two times fourteen: look only at the last digit. Two times four is eight — it ends in eight.",
        "Twenty-eight ends in eight. Seventy ends in zero — gone.",
        D('Cross out choices 1 and 4'),
        "For the maximum, three hundred fifty and one hundred forty both end in zero. The last digit can't split them.",
        D('Write "14 × 25 = 350" and circle choice 3'),
        "So here we simply multiply: fourteen times twenty-five, three hundred fifty. Choice three.",
        "The trick helps only when the choices end in different digits.",
    ]])

    # ---------- g018: 9 jars, 6 .. 42, >= 3 more, 5th jar -> 18 to 30  ==>  8 piggy banks, 5 .. 47, >= 4 more, 4th -> 17 to 31
    _rn_q(M, 'wp21-g018', 'Eight piggy banks stand in a row. The first holds 5 coins and the last holds 47. Each piggy bank holds '
          'at least 4 more coins than the one before it. What is the exact range for the fourth piggy bank?',
          ['17 to 31', '21 to 31', '17 to 35', '13 to 31'], 1, [
        'Smallest fourth piggy bank: from the first one, add the minimum $4$ each time: $5, 9, 13, 17$.',
        'Largest fourth piggy bank: from the last (eighth) one, go back $4$ each time: $47, 43, 39, 35, 31$.',
        'Both ends really happen: $5, 9, 13, 17, 21, 25, 29, 47$ and $5, 9, 13, 31, 35, 39, 43, 47$. Choice 1.'])
    _rn_video(M, 'wp21-g018', [[
        "For the smallest fourth piggy bank, give every one before it the minimum.",
        D('Write "5 → 9 → 13 → 17"'),
        "Five, then at least four more each time: nine, thirteen, seventeen.",
        "Can it be less? No — every gap needs at least four.",
        D('Cross out choices 2 and 4'),
        "Minimum seventeen. Choices two and four don't start with seventeen.",
        "For the largest, work backwards from the last piggy bank — keep every gap as small as possible.",
        "From the eighth back to the fourth is four steps.",
        D('Write "47 → 43 → 39 → 35 → 31"'),
        "Forty-seven, forty-three, thirty-nine, thirty-five, thirty-one.",
        D('Cross out choice 3 and circle choice 1'),
        "Maximum thirty-one. Seventeen to thirty-one — choice one.",
    ]])

    # ---------- g019: 17 campers, 4-6 + 2-5 - (1-3) -> 51 and 170  ==>  23 children, 3-5 + 2-4 - (1-3) -> 46 and 184
    _rn_q(M, 'wp21-g019', 'At a fair, each of 23 children gets 3 to 5 tickets at the first booth and 2 to 4 tickets at the second '
          'booth. Each child then uses 1 to 3 tickets on a ride. What are the smallest and the largest possible numbers of tickets '
          'left with all the children together?',
          ['69 and 184', '46 and 184', '46 and 207', '69 and 207'], 2, [
        'One child gets between $3+2=5$ and $5+4=9$ tickets.',
        'Fewest left: get the least and use the most: $5-3=2$. Most left: get the most and use the least: $9-1=8$.',
        'Twenty-three children: $23\\times2=46$ and $23\\times8=184$. Choice 2.'])
    _rn_video(M, 'wp21-g019', [[
        "First, what does each child get in total? Three to five, plus two to four.",
        D('Write "received: 5 to 9"'),
        "Five to nine tickets.",
        "Fewest left: get the least, use the most.",
        D('Write "min: 5 − 3 = 2"'),
        "Five minus three: two tickets.",
        "Most left: get the most, use the least.",
        D('Write "max: 9 − 1 = 8"'),
        "Nine minus one: eight.",
        D('Write "23 × 2 = 46" and cross out choices 1 and 4'),
        "Twenty-three children: forty-six at least. Choices one and four are out.",
        D('Write "23 × 8 = 184" and circle choice 2'),
        "And one hundred eighty-four at most. Choice two.",
    ], [
        "The last-digit shortcut from before.",
        D('Write "3 × 2 → ends in 6"'),
        "Twenty-three times two: three times two is six — ends in six. Forty-six, not sixty-nine.",
        D('Write "3 × 8 → ends in 4"'),
        "Twenty-three times eight: three times eight is twenty-four — ends in four. One hundred eighty-four, not two hundred seven.",
        D('Circle choice 2'),
        "Choice two — with barely any multiplication. It saves time, and it saves silly mistakes.",
    ]])

    # ---------- g020: Amir/Beth/Cara, 30 counters -> 11 and 27  ==>  Lior/Maya/Noam, 36 cards -> 13 and 33
    _rn_q(M, 'wp21-g020', 'Lior, Maya and Noam share 36 cards. Their numbers of cards are different positive integers, with Lior '
          'having the most and Noam the fewest. What are the smallest and the largest possible numbers of cards Lior has?',
          ['12 and 34', '12 and 33', '13 and 34', '13 and 33'], 4, [
        'Largest for Lior: give the others the least. Noam $1$, Maya $2$, Lior $36-1-2=33$. $34$ fails: it leaves $2$ cards, '
        'and $1+1$ are not different.',
        'Smallest for Lior: keep the three close. If Lior had $12$, the others could have at most $11$ and $10$: $12+11+10=33<36$ ✗.',
        'Lior $13$ works: $13+12+11=36$. Choice 4.'])
    _rn_video(M, 'wp21-g020', [[
        "The minimum is either twelve or thirteen. They ask for the smallest — so plug in the SMALLER one first.",
        "If twelve works, it beats thirteen. If it doesn't — the answer is thirteen.",
        D('Write "Lior 12 → Maya 11, Noam 10 → 33"'),
        "Lior twelve. The others must be less and different: eleven and ten, at most. That's only thirty-three — not thirty-six.",
        D('Cross out choices 1 and 2'),
        "Twelve fails. The minimum is thirteen — choices one and two are gone.",
        "Maximum: thirty-three or thirty-four. They ask for the largest — so plug in the BIGGER one first.",
        D('Write "Lior 34 → 2 left → 1 and 1 ✗"'),
        "Lior thirty-four leaves two cards: one each. But their numbers must be different. Fails.",
        D('Cross out choice 3 and circle choice 4'),
        "Choice four.",
    ], [
        "Now by understanding. Maximum first — it's easier.",
        "To maximize Lior, give the others the minimum.",
        D('Write "Noam 1, Maya 2 → Lior 36 − 3 = 33"'),
        "Noam one — at least one each. Maya must be more: two. Lior gets the rest: thirty-three.",
        "Minimum is trickier. The biggest of three must be MORE than a third.",
        D('Write "12, 12, 12 ✗"'),
        "Twelve each is exactly a third — but then they're equal. Not allowed.",
        D('Write "→ 11, 12, 13 ✓"'),
        "Move one card from Noam to Lior: eleven, twelve, thirteen. Different, and thirty-six in total.",
        D('Circle choice 4'),
        "Thirteen to thirty-three. Choice four.",
    ]])

    # ---------- g021: was a word-for-word copy of g015 (24 boxes, 86 markers). Now the same TYPE with new numbers:
    #            26 children, 90 stickers, >= 3 each -> at least 14 get exactly 3; 13 impossible
    _rn_q(M, 'wp21-g021', 'Ninety stickers are shared among 26 children, and every child gets at least 3 stickers. Which number '
          'cannot be the number of children who get exactly 3 stickers?',
          ['17', '13', '20', '14'], 2, [
        'The same type as the apple baskets, now with a shortcut.',
        'Give every child $3$ stickers: $26\\times3=78$. Spare stickers: $90-78=12$.',
        'A child gets more than $3$ only with at least one spare sticker. Therefore at most $12$ children get more than $3$, '
        'and at least $26-12=14$ children get exactly $3$.',
        '$13$ is below $14$. Therefore $13$ is impossible. Choice 2.',
        'Every count from $14$ to $25$ is possible: each spare sticker lifts one child, and the count can change by $1$ at a time. '
        'This is NOT true in every min–max question. When the values change in fixed jumps (the $2$-or-$6$ chip: $+4$ each time), '
        'there are holes.'])
    _rn_video(M, 'wp21-g021', [('Method 1 · Count the spare stickers', [
        "Fill every child to the minimum first.",
        D('Write "26 × 3 = 78 → 90 − 78 = 12 spare"'),
        "Three stickers each: seventy-eight. Twelve are spare.",
        "A child gets more than three only with at least one spare sticker.",
        D('Write "at most 12 children rise → at least 26 − 12 = 14 stay at 3"'),
        "Twelve spares can lift at most twelve children. So at least fourteen children get exactly three.",
        D('Circle choice 2'),
        "Thirteen is below fourteen. Impossible. Choice two — in one line of work.",
    ]), [
        "Now let's see ALL the possible values.",
        D('Write "possible: 14, 15, 16, …, 25"'),
        "At least fourteen children with three — we just saw that. At most twenty-five: twenty-five children get three, "
        "and the last child gets fifteen.",
        "And every count in between works. Why? Each spare sticker lifts one child. Move one sticker — the count changes by exactly one.",
        D('Write "changes by 1 at a time → no holes"'),
        "When the value can change by one at a time, the range has no holes. Then the impossible choice must be at an end.",
        D('Write "13, 14, 17, 20 → only 13 or 20 can be out"'),
        "Sort the choices: thirteen, fourteen, seventeen, twenty. Only thirteen or twenty can be outside.",
        "Twenty works: sixty stickers, and thirty left for six children — at least four each. So it's thirteen.",
        "But careful! This is NOT a general rule.",
        D('Write "chip 2 or 6: 14, 18, 22, … → holes!"'),
        "Remember the chip — two or six? The totals jump by four: fourteen, eighteen, twenty-two. Plenty of holes.",
        "Fixed jumps leave holes. No holes only when you can move by one.",
    ]], intro=[('The boxes again — the same question as Question eight, with the same numbers.',
                'Stickers this time — the same type as the apple baskets, with new numbers.')])

    # ---------- g023: 58 files, double, -16 at day end, day 3 before deletion -> 368  ==>  40 bacteria, -30 -> 140
    _rn_q(M, 'wp21-g023', 'A lab dish has 40 bacteria at the start of day 1. During each day the number of bacteria doubles, and at '
          'the end of each day 30 bacteria are removed for testing. How many bacteria are in the dish on day 3, just before that '
          'day’s removal?',
          ['110', '140', '220', '320'], 2, [
        'Day 1: $40\\times2=80$, then $80-30=50$.',
        'Day 2: $50\\times2=100$, then $100-30=70$.',
        'Day 3: $70\\times2=140$. Stop here: they ask for the number BEFORE the day 3 removal. Choice 2.',
        '$140-30=110$ is the trap: that is the number after the removal.'])
    _rn_video(M, 'wp21-g023', [[
        "Pattern questions: no formula. We write it out, day by day.",
        A('A table appears: Day | Start | After doubling | After removal',
          _table(['Day', 'Start', 'After doubling', 'After removal'], [['1', '40', '', ''], ['2', '', '', ''], ['3', '', '', '']],
                 x=410, y=300, w=1000, h=260)),
        D('Fill day 1: 80, then 50'),
        "Day one starts with forty. Doubles to eighty. Minus thirty: fifty.",
        D('Fill day 2: 50, 100, 70'),
        "Day two: fifty, doubles to one hundred, minus thirty: seventy.",
        D('Fill day 3: 70, 140'),
        "Day three: seventy, doubles to one hundred forty.",
        "Now — careful. The edges are where these questions bite.",
        "They ask for day three BEFORE the removal. So we don't subtract the thirty.",
        D('Circle 140 and circle choice 2'),
        "One hundred forty. Choice two. One hundred ten is the trap — that's after the removal.",
        "Always ask: does 'start' include this step? Does 'end' include that one?",
    ]])

    # ---------- g024: 56 lamps, one blue in every 4, lamp 2 blue -> 38  ==>  60 flags, one red in every 5, flag 3 red -> 43
    _rn_q(M, 'wp21-g024', 'Sixty flags hang in a row along a street. In every group of five neighboring flags, exactly one is red. '
          'Flag 3 is red. Which flag can also be red?',
          ['41', '42', '43', '44'], 3, [
        'Compare flags $1$ to $5$ with flags $2$ to $6$. They share flags $2$ to $5$, and each group has exactly one red flag. '
        'Therefore flag $6$ is red exactly when flag $1$ is red. The pattern repeats every $5$ flags.',
        'Flag $3$ is red. Therefore the red flags are $3, 8, 13, 18, \\ldots$: the numbers that leave remainder $3$ when divided by $5$.',
        '$43=40+3$ leaves remainder $3$ ✓. $41$, $42$ and $44$ leave remainders $1$, $2$ and $4$. Choice 3.'])
    _rn_video(M, 'wp21-g024', [[
        "Every five flags in a row contain exactly one red — and that's EVERY five in a row, not separate blocks.",
        "So flag six must match flag one, flag eight matches flag three — the pattern repeats every five.",
        "We don't draw flags. A circle for red, a line for not red.",
        A('The pattern appears: − − ● − −  − − ● − −  …',
          T('−  −  ●  −  −   −  −  ●  −  −   −  −  ●  −  −   …', size=48, x=410, y=320)),
        D('Number the circles 3, 8, 13, 18 …'),
        "Flag three is red — so eight, thirteen, eighteen, and on it goes.",
        D('Keep counting by fives: 23, 28, 33, 38, 43'),
        "Twenty-three, twenty-eight, thirty-three, thirty-eight, forty-three.",
        D('Circle choice 3'),
        "Forty-three is red. Choice three. Once you get it, it takes ten seconds.",
    ], [
        "A fixed cycle means a mathematical pattern.",
        D('Write "3, 8, 13, 18 … → remainder 3 when ÷ 5"'),
        "Every red flag leaves remainder three when you divide by five.",
        D('Write "43 = 40 + 3 ✓"'),
        "Forty-three is forty plus three. Remainder three.",
        "Forty-one, forty-two, forty-four — remainders one, two, four.",
        D('Circle choice 3'),
        "Choice three — no drawing at all.",
    ]])

    # ---------- g025: lights every 18 / 24 min from 07:30, 4th joint flash -> 11:06  ==>  buses every 16 / 20 min from 06:40 -> 10:40
    _rn_q(M, 'wp21-g025', 'Two buses leave a station together at 06:40. Line 5 leaves every 16 minutes and line 9 leaves every '
          '20 minutes. Counting 06:40 as the first time they leave together, when do they leave together for the fourth time?',
          ['08:40', '09:20', '10:40', '12:00'], 3, [
        'The buses leave together at every common multiple of $16$ and $20$. Jump along the bigger number: $20, 40, 60, 80$. '
        '$80=5\\times16$ ✓. They leave together every $80$ minutes.',
        '06:40 is the first time. Second: 08:00. Third: 09:20. Fourth: 10:40. Choice 3.',
        'Four departures have only three gaps: $3\\times80=240$ minutes, which is $4$ hours after 06:40.'])
    _rn_video(M, 'wp21-g025', [[
        "Work in order: write both schedules.",
        D('Write "every 16 min → 6:40, 6:56, 7:12, 7:28 …"'),
        "Every sixteen minutes: six forty, six fifty-six, seven twelve…",
        D('Write "every 20 min → 6:40, 7:00, 7:20, 7:40 …"'),
        "Every twenty: six forty, seven o'clock, seven twenty…",
        "It works — but it takes forever to find every match. There's a shortcut.",
    ], [
        "When do two repeating things meet? At a common multiple of the two gaps.",
        "The easy way: take the BIGGER number and jump along its multiples.",
        D('Write "20, 40, 60, 80 ← divisible by 16 ✓"'),
        "Twenty, forty, sixty, eighty. Eighty is divisible by sixteen. They leave together every eighty minutes.",
        "Why the bigger one? Fewer jumps.",
        "Now the edge: six forty already counts as the FIRST time.",
        A("'4 departures → 3 gaps of 80 min' appears", T('$4$ departures $\\to$ $3$ gaps of $80$ min', 36)),
        "Four departures have only three gaps between them. Items and gaps are different counts.",
        D('Write "6:40 → 8:00 → 9:20 → 10:40"'),
        "Second at eight o'clock, third at nine twenty, fourth at ten forty.",
        D('Circle choice 3'),
        "Choice three. Nine twenty is the trap — that's only the third.",
    ]])


def rn_order_and_refs(M):
    """g017 + g018 (easy+) move before the socks question (medium); renumber_guided() renumbers the titles.
    Lesson / card lines that named the old lamps follow the new flags."""
    M.move('wp21-g017', ADV, before='q-r26-t21-01')
    M.move('solve-wp21-g017', ADV, after='wp21-g017')
    M.move('wp21-g018', ADV, after='solve-wp21-g017')
    M.move('solve-wp21-g018', ADV, after='wp21-g018')
    _fix_say(M, 'wp-022', 2, 'and the lamps in the questions', 'and the flags in the questions')
    c = M.card('mem-trial-toolkit')
    n = 0
    for r in c['tables'][0]['rows']:
        if r[1].startswith('Use the remainder: lamps'):
            r[1] = r[1].replace('lamps', 'flags in a row'); n += 1
    assert n == 1, 'toolkit row'


def rn_practice_questions(M):
    S = _rn_q
    # p01: 120 pieces, circles = squares > triangles -> 34  ==>  150 beads, red = blue > green -> 46
    S(M, 'wp21-p01', 'A bag holds 150 beads: red, blue and green only. There are as many red beads as blue beads, and there are '
      'more red beads than green beads. Which could be the number of green beads?', ['52', '33', '46', '60'], 3, [
        'Test the choices. With $46$ green beads, $150-46=104$ beads are left: $104\\div2=52$ red and $52$ blue. $52>46$ ✓.',
        '$33$: $150-33=117$ is odd and cannot split into two equal groups. $52$: $98\\div2=49<52$ ✗. $60$: $90\\div2=45<60$ ✗. Choice 3.'])
    # p02: Nora / Sam sketchbooks and cases  ==>  Ella / Ben stamps and postcards
    S(M, 'wp21-p02', 'Ella has 5–11 stamps and fewer than 4 postcards. Ben has fewer than 9 stamps and 2–7 postcards. A count can be '
      'zero unless a lower bound is given. What are the exact ranges of their stamps together and of their postcards together?',
      ['5–20 stamps; 2–11 postcards', '5–19 stamps; 2–10 postcards', '6–19 stamps; 3–10 postcards', '5–11 stamps; 2–7 postcards'], 2, [
        'Fewer than $9$ means at most $8$. Fewer than $4$ means at most $3$.',
        'Stamps: smallest $5+0=5$, largest $11+8=19$.',
        'Postcards: smallest $0+2=2$, largest $3+7=10$. Choice 2.'])
    # p03: four vouchers of 2, 7, 12 -> 31 impossible  ==>  three stamps of 3, 7, 11 cents -> 23 impossible
    S(M, 'wp21-p03', 'Dan puts exactly three stamps on a letter. Each stamp is worth 3, 7 or 11 cents. Which total postage is impossible?',
      ['17', '29', '23', '33'], 3, [
        'Three $3$-cent stamps: $3\\times3=9$. Changing a $3$ to a $7$ adds $4$. Changing a $3$ to an $11$ adds $8$.',
        'Every total is $9$ plus a multiple of $4$: $9, 13, 17, 21, 25, 29, 33$.',
        'Check: $17-9=8$ ✓, $29-9=20$ ✓, $33-9=24$ ✓, $23-9=14$ ✗ (not a multiple of $4$). Choice 3.'])
    # p04: passes 120 / 60 / 30, 8 passes, exactly 3 museum  ==>  tickets 90 / 50 / 20, 7 tickets, exactly 2 theater
    S(M, 'wp21-p04', 'Concert tickets cost 90 dollars, theater tickets 50 dollars and movie tickets 20 dollars. A club buys seven '
      'tickets, exactly two of them theater tickets. What are the smallest and the largest possible total costs?',
      ['140–550 dollars', '350–550 dollars', '200–630 dollars', '200–550 dollars'], 4, [
        'Two theater tickets: $2\\times50=100$. There are $7-2=5$ more tickets.',
        'Cheapest: five movie tickets, $5\\times20=100$. Total: $100+100=200$.',
        'Most expensive: five concert tickets, $5\\times90=450$. Total: $100+450=550$. Choice 4.'])
    # p05: card shop, sells half, +3 per card sold, 24 -> 192  ==>  pet shop, sells half, +2 per fish sold, 32 -> 108
    S(M, 'wp21-p05', 'A pet shop sells half of its fish each day. At closing, it adds 2 new fish for every fish sold that day. It '
      'starts Monday with 32 fish. How many fish does it have at the end of Wednesday?', ['72', '96', '108', '162'], 3, [
        'Monday: start $32$ → sell $16$, keep $16$ → add $2\\times16=32$ → end $16+32=48$.',
        'Tuesday: start $48$ → sell $24$, keep $24$ → add $2\\times24=48$ → end $24+48=72$.',
        'Wednesday: start $72$ → sell $36$, keep $36$ → add $2\\times36=72$ → end $36+72=108$. Choice 3.'])
    # p06: 1, 1/3, 1/9, 1/27 (each / 3)  ==>  2, 1/2, 1/8, 1/32 (each / 4); choices reordered
    S(M, 'wp21-p06', 'The sequence is $2,\\ \\frac12,\\ \\frac18,\\ \\frac1{32},\\ldots$ Which of the following statements is NOT true?',
      ['Some term is negative', 'Every term is four times the following term', 'The gap between neighboring terms gets smaller',
       'Each term after the first is smaller than the previous term'], 1, [
        'Each term is the one before it divided by $4$: $2\\div4=\\frac12$, $\\frac12\\div4=\\frac18$, and so on.',
        'Statement 2: $\\frac12=4\\times\\frac18$ ✓. Statement 4: the terms get smaller ✓. Statement 3: the gaps are '
        '$\\frac32, \\frac38, \\frac3{32}, \\ldots$, and they get smaller ✓.',
        'Statement 1: a positive number divided by $4$ stays positive. No term is negative. Statement 1 is not true. Choice 1.'])
    # p07: 28 badges, n teams, different amounts -> 8 impossible  ==>  21 medals -> 7 impossible
    S(M, 'wp21-p07', 'Twenty-one medals are shared among $n$ teams. Each team receives a different positive number of medals. '
      'Which value of $n$ is impossible?', ['$5$', '$7$', '$2$', '$6$'], 2, [
        '$n$ teams need at least $1+2+\\ldots+n=\\frac{n(n+1)}{2}$ medals.',
        '$n=7$: $\\frac{7\\cdot8}{2}=28>21$ ✗. $n=6$: $\\frac{6\\cdot7}{2}=21$ ✓ (the teams get $1$ to $6$).',
        '$n=5$ and $n=2$ also work, for example $1+2+3+4+11$ and $1+20$. Choice 2.'])
    # p08: seats 1-270, every 6th and every 9th -> 15  ==>  pages 1-240, every 8th and every 12th -> 10
    S(M, 'wp21-p08', 'A book has 240 pages, numbered 1 to 240. Every eighth page has a picture, and every twelfth page has a puzzle. '
      'How many pages have both a picture and a puzzle?', ['20', '24', '10', '30'], 3, [
        'A page with both has a number divisible by $8$ and by $12$. The smallest common multiple of $8$ and $12$ is $24$ '
        '(jump along $12$: $12, 24$ ✓).',
        'Pages $24, 48, \\ldots, 240$: $240\\div24=10$ pages. Choice 3.'])
    # p09: 6 musicians (2 posters) + 8 actors (4), exactly 9 attend -> 24-34  ==>  7 parents (3 cakes) + 5 teachers (1), 10 come -> 20-24
    S(M, 'wp21-p09', 'A class invites 7 parents and 5 teachers to help at a fair. Exactly 10 of them come. Each parent bakes 3 cakes '
      'and each teacher bakes 1 cake. What is the exact range of the total number of cakes?', ['10–30', '20–30', '20–24', '22–24'], 3, [
        'At most $5$ of the $10$ helpers are teachers. Therefore at least $10-5=5$ are parents. At most $7$ are parents, '
        'and therefore at least $3$ are teachers.',
        'Fewest cakes: $5$ parents and $5$ teachers: $5\\times3+5\\times1=15+5=20$.',
        'Most cakes: $7$ parents and $3$ teachers: $7\\times3+3\\times1=21+3=24$. Choice 3.'])
    # p10: 48 questions, +3 / -2, answers 42 -> 116  ==>  40 questions, +4 / -2, answers 35 -> 128
    S(M, 'wp21-p10', 'A test has 40 questions. A correct answer earns 4 points, a wrong answer loses 2 points, and a blank earns 0. '
      'Omer answers exactly 35 questions. Which could be his score?', ['131', '125', '124', '128'], 4, [
        '$35$ correct answers: $35\\times4=140$. Changing one correct answer to a wrong one: lose $4$, and lose $2$ more: $-6$.',
        'Possible scores: $140, 134, 128, 122, \\ldots$ They all leave remainder $2$ when divided by $6$.',
        '$128$ is in the list ✓. $131$, $125$ and $124$ are not. Choice 4.'])
    # p11: card 5 / 2, seven draws, divisible by 8 -> 32  ==>  spinner 4 / 1, six spins, divisible by 7 -> 21
    S(M, 'wp21-p11', 'A spinner has two equal parts, marked 4 and 1. It is spun 6 times, and the results are added. The total is '
      'divisible by 7. What is the total?', ['7', '14', '21', '28'], 3, [
        'Six $1$s: $6\\times1=6$. Each $4$ instead of a $1$ adds $3$.',
        'Possible totals: $6, 9, 12, 15, 18, 21, 24$.',
        'The only one divisible by $7$ is $21=3\\times7$. Choice 3.'])
    # p12: 18 robots, at least half move, >= 4 blue stay -> 0-14  ==>  24 students, glasses, >= 5 stay -> 0-19
    S(M, 'wp21-p12', 'There are $24$ students in a classroom, and any of them may wear glasses. At least half of the students go to '
      'the library. At least $5$ of the students who stay in the classroom wear glasses. What are the smallest and the largest '
      'possible numbers of students with glasses who go to the library?', ['0–24', '5–19', '0–19', '12–19'], 3, [
        'Smallest: $0$. Let $12$ students without glasses go to the library. The $12$ students who stay all wear glasses ✓.',
        'Largest: at least $5$ students with glasses must stay. Therefore at most $24-5=19$ students go, and all $19$ can wear '
        'glasses ($19\\ge12$ ✓). Choice 3.'])
    # p13: packages 2/4/6/8 kg at 3/6/8/10, 28 kg in 5 -> 36  ==>  boxes 3/6/9/12 kg at 4/7/10/12, 42 kg in 5 -> 44
    S(M, 'wp21-p13', 'A shipping company sends boxes of exactly 3, 6, 9 or 12 kg, costing 4, 7, 10 or 12 dollars respectively. '
      'A store must ship 42 kg in exactly five boxes. What is the lowest possible cost, in dollars?', ['45', '43', '46', '44'], 4, [
        'List the mixes of $5$ boxes that make $42$ kg, by the number of $12$-kg boxes. Four $12$s already weigh $48$ kg: too much.',
        'Three $12$s: the other two make $6$ kg: $3+3$. Cost: $3\\times12+2\\times4=44$.',
        'Two $12$s: the other three make $18$ kg: $3+6+9$ (cost $45$) or $6+6+6$ (cost $45$).',
        'One $12$: the other four make $30$ kg: $3+9+9+9$ (cost $46$) or $6+6+9+9$ (cost $46$).',
        'No $12$s: $6+9+9+9+9$ (cost $47$).',
        'The lowest cost is $44$. Choice 4.'])
    # p14: 4 players, 5-min rounds, ends at 4 wins -> 65  ==>  5 friends, 4-min rounds, ends at 3 wins -> 44
    S(M, 'wp21-p14', 'Five friends play a board game. Each round takes 4 minutes and has exactly one winner. The game ends as soon '
      'as one player has won 3 rounds. What is the longest the game can last, in minutes?', ['44', '40', '60', '48'], 1, [
        'Worst luck $+\\,1$: the game lasts longest when every player gets as many wins as possible without ending it: $2$ wins each.',
        '$5\\times2=10$ rounds, and still no one has $3$ wins. Round $11$ must give someone a third win.',
        '$11\\times4=44$ minutes. Choice 1.'])
    # p15: 3-9 yellow, 5-8 black -> 9/14  ==>  4-11 red pens, 6-9 blue pens -> 11/17
    S(M, 'wp21-p15', 'A box contains 4 to 11 red pens and 6 to 9 blue pens, and no other pens. What is the greatest possible '
      'fraction of the pens that are red?', ['$\\frac{11}{20}$', '$\\frac{2}{5}$', '$\\frac{11}{17}$', '$\\frac{4}{13}$'], 3, [
        'The red share $\\frac{R}{R+B}$ is largest with the most red and the fewest blue: $R=11$ and $B=6$.',
        '$\\frac{11}{11+6}=\\frac{11}{17}$. Choice 3.'])
    # p16: 148-m fence, 3-m stripes, 2-m gaps -> 30  ==>  116-m wall, 4-m stripes, 3-m gaps -> 17
    S(M, 'wp21-p16', 'A $116$-meter wall is painted in $4$-meter stripes, with $3$-meter unpainted gaps between the stripes. The '
      'stripes must be complete. What is the greatest possible number of painted stripes?', ['16', '17', '18', '19'], 2, [
        '$n$ stripes have $n-1$ gaps between them. Length: $4n+3(n-1)=7n-3$.',
        '$n=17$: $7\\times17-3=116$ ✓. $n=18$: $7\\times18-3=123>116$ ✗. Choice 2.'])
    # p17: ribbons 18, 10, 5, 3 -> 7 impossible  ==>  ropes 20, 12, 7, 3 -> 8 impossible
    S(M, 'wp21-p17', 'A sailor has four ropes: $20$, $12$, $7$ and $3$ meters long. Each rope may be used once, either at its full '
      'length or folded once to half its length. Any of the ropes may be joined together; a joined rope cannot be folded. Which '
      'length cannot be made?', ['$\\frac{27}{2}$', '20', '32', '8'], 4, [
        'Check the choices. $32=20+12$ ✓. $20$: the $20$-m rope alone ✓. $\\frac{27}{2}=13.5=12+1.5$ (the $3$-m rope folded) ✓.',
        '$8$: the $20$-m rope is too long even folded ($10$). The $12$-m rope can only be used folded: $6$.',
        'Without it, the $7$-m rope ($7$ or $3.5$) and the $3$-m rope ($3$ or $1.5$) give only $1.5$, $3$, $3.5$, $5$, $6.5$, $7$, '
        '$8.5$ and $10$. No $8$.',
        'With the $6$ from the $12$-m rope, we need $2$ more, and nothing gives exactly $2$. Therefore $8$ cannot be made. Choice 4.'])
    # p18: four 7-credit + three 1-credit tokens -> 19  ==>  five 5-cent + three 1-cent coins -> 23
    S(M, 'wp21-p18', 'A wallet holds five 5-cent coins and three 1-cent coins. How many different positive amounts can be paid '
      'exactly using some of these coins?', ['24', '23', '18', '28'], 2, [
        'An amount is $5a+b$, with $a$ from $0$ to $5$ (five-cent coins) and $b$ from $0$ to $3$ (one-cent coins).',
        'The amounts form blocks: $0$–$3$, $5$–$8$, $10$–$13$, $15$–$18$, $20$–$23$, $25$–$28$. Each block ends before the next '
        'one starts. No amount is counted twice.',
        '$6\\times4=24$ amounts, minus the amount $0$: $23$. Choice 2.'])
    # p19: 27 volunteers, 1/3 remote, remote < editors < translators -> 14-17  ==>  33 workers, 1/3 at night -> 17-21
    S(M, 'wp21-p19', 'A store has 33 workers, and each of them is either a cashier or a stocker. One third of the workers work at '
      'night. There are more cashiers than night workers, but fewer cashiers than stockers. What is the exact range of the number '
      'of stockers?', ['17–21', '12–16', '17–22', '16–21'], 1, [
        'Night workers: $\\frac13\\times33=11$. Cashiers are more than $11$: at least $12$.',
        'Cashiers are fewer than stockers, and together they are $33$. $16$ cashiers and $17$ stockers works; $17$ cashiers and '
        '$16$ stockers does not. Therefore there are at most $16$ cashiers.',
        'Stockers $=33-$ cashiers: from $33-16=17$ to $33-12=21$. Choice 1.'])
    # p20: 8 parcels/h alone, +3 per extra volunteer, 7 volunteers -> 182  ==>  12 boxes/h, +2 per extra worker, 6 workers -> 132
    S(M, 'wp21-p20', 'A worker alone packs 12 boxes per hour. For this job, each additional worker increases every worker’s rate by '
      '2 boxes per hour. Six workers work together for one hour. How many boxes do they pack?', ['132', '144', '110', '72'], 1, [
        'Six workers means $5$ ADDITIONAL workers, not $6$.',
        'Each rate: $12+5\\times2=12+10=22$ boxes per hour.',
        'Total: $6\\times22=132$. Choice 1.'])


def rn_practice(M):
    """Approved clean-up: copies out, at most 3 extra-bank warm-ups, September items whose type the Hebrew covers out."""
    N = lambda k: 'q-r26-t21-' + k
    out = [
        # copies (practice_audit/copies_by_topic.txt, each checked)
        'wp21-p26',   # six packs of 4 or 9 markers: the same question as guided Q6 (token 4/9, six tosses)
        'wp21-p23',   # 36 stickers, different amounts: the same question as guided Q3
        N('11'),      # units digit of 7^50: the same as Topic 15 (3^25, 7^4) and Topic 18 (2^50)
        # extra-bank warm-ups beyond 3 (kept: p21 printer, p27 largest of five scores, p25 spare pencils)
        'wp21-p22',   # lights every 8 and 14 s, 4th joint flash: guided Q18 and the summary's 8-and-14 example
        'wp21-p24',   # 52 lockers, one red in every 4, locker 2: the same as the old guided lamps question
        # September items of a type the Hebrew practice covers
        N('03'), N('04'),   # "to be sure": worst luck + 1, practised by p14 (and guided Q9)
        N('05'),      # 30 birthdays, must be true: worst luck (p14) + must be true (kept -06)
        N('09'),      # sum of the first n even numbers: plug in n = 3, as kept -07 and guided Q5
    ]
    for qid in out:
        assert M.section_of(qid) == PRAC, qid
        M.unplace(qid)
    N7, N10, N6 = N('07'), N('10'), N('06')
    M.practice_order(PRAC, [
        'wp21-p21', 'wp21-p02', 'wp21-p04', 'wp21-p01', 'wp21-p08', 'wp21-p27', 'wp21-p07', 'wp21-p16', 'wp21-p11', 'wp21-p10',
        N7, N10, 'wp21-p05', 'wp21-p09', 'wp21-p15', 'wp21-p20', 'wp21-p03', 'wp21-p25', 'wp21-p14', 'wp21-p19', 'wp21-p06',
        N6, 'wp21-p12', 'wp21-p13', 'wp21-p17', 'wp21-p18'])


def renumber_pass(M):
    rn_guided_learn(M)
    rn_guided_adv(M)
    rn_order_and_refs(M)
    rn_practice_questions(M)
    rn_practice(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


# ======================================================================================================
# 2026-10-07 methods spread (runs last). The 2026-10-06 exam methods are added wherever they genuinely solve a
# question: one written line at the end of the solution (existing lines kept), and on the clearest guided videos
# one extra "Method N" slide (board lines by click, pen only for marks). Methods taught in a later topic are
# written as a self-contained "Shortcut · <name>" line. Nothing in this topic is recorded (checked 2026-10-07).
# ======================================================================================================
SPREAD_RECORDED = set()


def _sp_line(M, qid, line):
    ex = list(M.q(qid).get('explanation') or [])
    if line in ex: return
    M.set_q(qid, expl=ex + [line])


def _sp_slide(M, qid, after_n, title, script):
    vid = 'solve-' + qid
    if vid in SPREAD_RECORDED: return
    assert M.video(vid)['questionId'] == qid, vid
    act = M.slide(vid, 2)['active']
    M.insert_slides(vid, after_n, [dict(mode='question', active=act, title=title, pre=[Q(qid)], script=script)])


def spread_methods(M):
    # ---- The most precise range (topic 12): test a number inside one choice and outside another ----
    _sp_line(M, 'wp21-g018', r'Method 2 · The most precise range: test a number inside one choice and outside another. $13$: the fourth holds at least $5+3\cdot4=17$ ✗, therefore choice 4 is out. $35$: four more steps need at least $35+4\cdot4=51>47$ ✗, therefore choice 3 is out. $17$: $5, 9, 13, 17, 21, 25, 29, 47$ ✓, therefore choice 2, which leaves $17$ out, is out. Choice 1.')
    _sp_line(M, 'wp21-p09', r'Method 2 · The most precise range: test a number inside one choice and outside another. $20$ cakes: $5$ parents and $5$ teachers ✓, therefore choice 4 (from $22$) is out. $26$ cakes: $p$ parents bake $3p+(10-p)=2p+10=26$, therefore $p=8$, but only $7$ parents were invited ✗. Choices 1 and 2 contain $26$, therefore they are out. Choice 3.')
    _sp_line(M, 'wp21-p19', r'Method 2 · The most precise range: test a number inside one choice and outside another. $22$ stockers leave $11$ cashiers, not more than the $11$ night workers ✗: choice 3 is out. $16$ stockers leave $17$ cashiers, more than the stockers ✗: choices 2 and 4 are out. Choice 1.')
    vid = 'solve-wp21-g018'
    if vid not in SPREAD_RECORDED:
        M.set_slide(vid, 2, title='Method 1 · Min front, max back')
    _sp_slide(M, 'wp21-g018', 2, 'Method 2 · The most precise range', [
        "The choices are ranges. So test a number that some choices contain and others don't.",
        A("'13? at least 5 + 3 · 4 = 17 ✗' appears", T(r'$13$? The fourth is at least $5+3\cdot4=17$ ✗', size=40)),
        D('Cross out choice 4'),
        'Thirteen? The fourth holds at least seventeen. Choice four is out.',
        A("'35? 35 + 4 · 4 = 51 > 47 ✗' appears", T(r'$35$? Then the last needs $35+4\cdot4=51>47$ ✗', size=40)),
        D('Cross out choice 3'),
        'Thirty-five? Four more steps would need fifty-one. Too many. Choice three is out.',
        A("'17? 5, 9, 13, 17, …, 47 ✓' appears", T(r'$17$? $\ 5, 9, 13, 17, 21, 25, 29, 47$ ✓', size=40)),
        D('Cross out choice 2 and circle choice 1'),
        'Seventeen works. Choice two leaves it out, so it goes too. Choice one.'])


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
    # Topic 21 (day 8) comes before topic 12 (the most precise range, day 20) in the plan.
    old = 'Method 2 · The most precise range: test a number inside one choice and outside another.'
    new = 'Shortcut · The most precise range: the right range holds every value that can happen and no value that cannot. So test a number inside one choice and outside another: a choice that holds an impossible value, or leaves out a possible one, is out.'
    for qid in ('wp21-p09', 'wp21-p19', 'wp21-g018'):
        line = next(l for l in M.q(qid)['explanation'] if l.startswith(old))
        _po_line(M, qid, old, new + line[len(old):])
    v = 'solve-wp21-g018'   # not recorded
    assert M.slide(v, 3)['title'] == 'Method 2 · The most precise range'
    M.slide(v, 3)['title'] = 'Shortcut · The most precise range'
    _po_say(M, v, 3, "The choices are ranges. So test a number that some choices contain and others don't.", [
        "A faster way. The choices are ranges — and the right range holds every value that can happen, and nothing that can't.",
        "So test a number that some choices contain and others don't."])
    # solve-q-r26-t21-01 (not recorded): "Algebraic Understanding" is topic 20, near the END of the plan.
    v = 'solve-q-r26-t21-01'
    _po_say(M, v, 2, "They ask what she must take to be SURE. So we imagine the worst luck, then add one — as in Algebraic Understanding.",
            "They ask what she must take to be SURE. So we imagine the worst luck, then add one.")
    _po_say(M, v, 3, "Four is the answer for a PAIR — the socks question from Algebraic Understanding.",
            "Four is the answer for a PAIR: one sock of each color, then one more.")
    # the toolkit card pointed to topic 20 (Algebraic Understanding), which comes near the END of the plan
    c = M.card('mem-trial-toolkit'); hit = 0
    for tb in c['tables']:
        for r in tb['rows']:
            if r[1] == 'Worst luck + 1 (see Algebraic Understanding)':
                r[1] = 'Worst luck + 1: build the worst case that still fails, then add one'; hit += 1
            if r[0] == '"Must be true" (Topics 1 and 20)':
                r[0] = '"Must be true" (Topic 1)'; hit += 1
    assert hit == 2, hit
    mc = M.card('mem-trial-error')
    k = [i for i, t in enumerate(mc['tips']) if '(Topics 1 and 20)' in t]
    assert len(k) == 1, k
    mc['tips'][k[0]] = mc['tips'][k[0]].replace('(Topics 1 and 20)', '(Topic 1)')
    _po_say(M, 'wp-001', 4, 'One reminder from Topics 1 and 20: must, could, cannot.', 'One reminder from Topic 1: must, could, cannot.')   # not recorded


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
    _mn_load().method_names(M, 21)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 Hebrew points restored. The 2026-10-05 cut kept only short intros; two points of the teacher's Hebrew
# lessons were no longer taught anywhere: WHY school sequence formulas are useless here (+ "understanding is rare"),
# and WHY the exam loves trial-and-error questions (school spoon-feeds, university doesn't). Runs LAST.
# Helpers: _hebrew_back.py (a video recorded before its CUTOFF is not changed). See t21_CHANGES.md.
# =====================================================================================================================
import importlib.util as _ilu_hb, os as _os_hb
_s_hb = _ilu_hb.spec_from_file_location('_hebrew_back', _os_hb.path.join(_os_hb.path.dirname(_os_hb.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu_hb.module_from_spec(_s_hb); _s_hb.loader.exec_module(HB)


def hebrew_points_back(M):
    # lesson "Patterns" (wp-008): Hebrew "חוקיות" - don't use school sequence formulas, they won't work; understanding is rare
    if not HB.add_lines(M, 'wp-008', 'Two kinds', 'The second kind: a sequence with a formula in n', [
            "If you remember arithmetic or geometric sequence formulas from school — leave them. These aren't the sequences you know, and those formulas won't work here.",
            "Solving it by pure understanding is possible — but every question is different, and very few students manage it."]):
        HB.add_expl(M, 'wp21-g010', "Don't use the school formulas for arithmetic or geometric sequences — these are not the sequences you know. Plugging in is the simple, reliable way.")
    # lesson "Smart Trial & Error" (wp-012): Hebrew advanced intro - why the exam tests this (school vs university)
    if not HB.add_lines(M, 'wp-012', 'Why it matters', 'Why does the exam love these questions?', [
            "The exam is meant to predict how you'll do in your first year at university.",
            "At school you're spoon-fed: here's the material, here are the exact questions. At university, a lot is up to you — nobody tells you exactly what to do."]):
        HB.add_expl(M, 'wp21-g013', "Why the exam loves these questions: it predicts how you'll do at university, where nobody tells you exactly what to do. Don't stare — start trying.")


_apply_before_hebrew_points_back = apply


def apply(M):
    _apply_before_hebrew_points_back(M)
    hebrew_points_back(M)   # 2026-10-08 Hebrew points restored: runs LAST


# =====================================================================================================================
# 2026-10-08 coverage fixes (teacher approved "go ahead"). A full check of the teacher's Hebrew course against this
# topic found points that were taught only WEAKLY or were MISSING; each one goes back as one or two short spoken lines
# in an unrecorded video (or, for a video recorded before CF.CUTOFF, into the written solution / card). Runs LAST.
# Helpers: _hebrew_back.py loaded as its own copy with this pass's CUTOFF. See tNN_CHANGES.md "2026-10-08 coverage fixes".
# =====================================================================================================================
import importlib.util as _ilu_cf, os as _os_cf
_s_cf = _ilu_cf.spec_from_file_location('_hebrew_back_cf', _os_cf.path.join(_os_cf.path.dirname(_os_cf.path.abspath(__file__)), '_hebrew_back.py'))
CF = _ilu_cf.module_from_spec(_s_cf); _s_cf.loader.exec_module(CF)
CF.CUTOFF = '2026-10-08T08-43-14'   # UTC, when this pass finished: a take recorded before it keeps its video unchanged


def _cf_replace(M, vid, title, sub, new):
    """replace the one line containing sub (spoken / drawn / item) on slide `title` by new (line or list). False if recorded."""
    if CF.recorded(vid): return False
    CF.set_slide(M, vid, title, CF.replace_line(CF.lines_of(M, vid, title), sub, new))
    return True


def coverage_fixes(M):
    # #40 (Hebrew 410, 421): don't get stuck - start plugging in, OR skip the question and move on
    if not CF.add_lines(M, 'solve-wp21-g015', 'Plug in the answers', 'Some people try and wonder.', [
            "Or skip it, move on, and come back at the end. Just don't sit and stare."]):
        CF.add_expl(M, 'wp21-g015', "Stuck? Start plugging in the answers, or skip the question and come back at the end. Just don't sit and stare.")
    # #54 (Hebrew 659-660): the biggest share is more than half of two, more than a third of three
    if not CF.add_lines(M, 'solve-wp21-g020', 'Method 2 · Understanding', 'The biggest of three must be MORE than a third.', [
            "Same idea with two people: if one has more, he has more than half."]):
        CF.add_expl(M, 'wp21-g020', "The biggest of two different shares is more than half; the biggest of three is more than a third.")
    # #57 (min-max range has no holes): the English keeps its qualified version (teacher decision 2026-10-08) - no change


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST
