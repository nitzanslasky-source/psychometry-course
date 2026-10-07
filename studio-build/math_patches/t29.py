"""Topic 29 - Probability. Course review 2026-09 fixes.
Pass 2 (teacher-approved remove/restore plan): geometric probability, "unknown count" and the AND/OR size check are
removed; wp29-p03, wp29-p20 and the true original lines are restored; a summary video comes before the practice.
See t29_CHANGES.md for the plain-language list."""
import copy
import re
from dsl import T, H, A, D, Q
from math_api import VIS, _word

TOPIC = 29
LEARN, ADV, PRACTICE = 'wp29-learn', 'wp29-advanced', 'wp29-practice'
LESSON_VIDS = ['wp-146', 'wp-147-after', 'wp-151', 'wp-159']
MORE = 'r26-t29-more-rules'
LESSON_SB = ['Wanted over possible', 'Between 0 and 1', 'Possible first', 'Certain & impossible', 'And · Or',
             'OR with overlap', 'At least one', 'Exactly one', 'Two stages: a tree',
             'Dice symmetry', 'Recap']
# Guided numbers before renumbering: new ones get 18-20. renumber_guided() then numbers them in course order.
LEARN_SB = ['Question %d' % n for n in list(range(1, 12)) + [18, 19, 20, 12]]
ADV_SB = ['Question %d' % n for n in [13, 14, 15, 16, 17]]
GID = ['q-r26-t29-%02d' % k for k in range(1, 15)]

# ------------------------------------------------------------------------------------------------
# Figures (same style as the geometry topics: ink #203344, shaded #d5f1ed / #087f83, DejaVu 20)
# ------------------------------------------------------------------------------------------------
INK, TEAL = '#203344', '#087f83'


def _svg(label, body, vb='0 0 640 360'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, body))


def _t(x, y, s, italic=False, size=20, color=INK):
    return ('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" fill="%s" '
            'font-family="DejaVu Sans,Arial,sans-serif" font-size="%d"%s>%s</text>'
            % (x, y, color, size, ' font-style="italic"' if italic else '', s))


def _dot(cx, cy):
    return '<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (cx, cy, INK)


def _line(x1, y1, x2, y2, color=INK, w=1.8, dash=False):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, color, w, ' stroke-dasharray="6 5"' if dash else ''))



def _tree():
    b = ''
    edges = [((70, 180), (230, 95), '1/2', (140, 118)), ((70, 180), (230, 265), '1/2', (140, 242)),
             ((262, 95), (420, 45), '3/4', (338, 50)), ((262, 95), (420, 145), '1/4', (338, 140)),
             ((262, 265), (420, 215), '1/6', (338, 220)), ((262, 265), (420, 315), '5/6', (338, 310))]
    for (x1, y1), (x2, y2), lab, (lx, ly) in edges:
        red = lab in ('3/4', '1/6') or lab == '1/2'
        b += _line(x1, y1, x2, y2, TEAL if red else INK, 2.6 if red else 1.8)
        b += _t(lx, ly, lab, size=20, color=TEAL if red else INK)
    b += _dot(70, 180)
    b += _t(246, 95, 'A', size=22) + _t(246, 265, 'B', size=22)
    for y, s in [(45, 'red'), (145, 'blue'), (215, 'red'), (315, 'blue')]:
        b += _t(448, y, s, size=20)
    return _svg('A tree: choose bag A or B, then draw red or blue', b, vb='40 20 450 320')


FIG_TREE = _tree()


# ------------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------------
def _script_of(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _replace_say(M, vid, n, old, new):
    """Replace a whole spoken line (new=None deletes it)."""
    def fn(lines):
        out = []
        hit = False
        for l in lines:
            if l.get('say') == old:
                hit = True
                if new is None: continue
                l = dict(l, say=new)
            out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


US = [('colours', 'colors'), ('colour', 'color'), ('Colour', 'Color'), ('practise', 'practice'),
      ('neighbouring', 'neighboring'), ('In maths', 'In math'), ('favourable', 'favorable'), ('analysed', 'analyzed')]


def _american(M):
    for v in M.D['videos'].values():
        if v['topic'] != TOPIC: continue
        hit = False
        for b in v['beats']:
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k in l:
                        s = l[k]
                        for a, c in US: s = s.replace(a, c)
                        if s != l[k]: l[k] = s; hit = True
            for it in b['items']:
                if it.get('t'):
                    s = it['t']
                    for a, c in US: s = s.replace(a, c)
                    if s != it['t']: it['t'] = s; hit = True
        if hit: M.touched_videos.add(v['id'])


def _solution(M, qid, group, intro, slides):
    """Guided-question solution video in the style of the existing solve-wp29-* videos."""
    n = M.next_question_number(TOPIC)
    sb = LEARN_SB if group == 'learn' else ADV_SB
    act = sb.index('Question %d' % n)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % _word(n)] + intro)]
    for s in slides:
        title, script = s[0], s[1]
        pre = s[2] if len(s) > 2 else [Q(qid)]
        beats.append(dict(mode='question', active=act, title=title, pre=pre, script=script))
    v = M.new_video('solve-' + qid, TOPIC, 'Probability Questions', sb, beats, M.section_of(qid),
                    kind='solution', qid=qid)
    v['beats'][0]['title'] = 'Probability Questions' if group == 'learn' else 'Advanced Probability'
    v['hybrid']['num'] = 55 if group == 'learn' else 59
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


def _sync_stem_copies(M, qids):
    for qid in qids:
        q = M.q(qid)
        for v in M.D['videos'].values():
            if v.get('questionId') != qid: continue
            v['title'] = v['navLabel'] = q['stem']
            for b in v['beats']:
                if (b.get('canvas') or '').startswith('Pre-loaded — question'):
                    b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, q['stem'])


# ================================================================================================
def apply(M):
    _lessons(M)
    _existing_solution_videos(M)
    _existing_questions(M)
    _more_rules_block(M)
    _cards(M)
    _practice(M)
    _american(M)
    _summary(M)
    cut_repeats(M)
    add_methods(M)   # 2026-10-06 new exam methods (runs last)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)


# ------------------------------------------------------------------------------------------------
# 1. Lesson videos: wrong OR rule, sub-group, overlap slide, dice symmetry, recap
# ------------------------------------------------------------------------------------------------
def _lessons(M):
    for vid in LESSON_VIDS:
        M.set_sidebar(vid, LESSON_SB)

    # wp-146 slide 4: possible = the group they choose FROM
    M.set_slide('wp-146', 4, script=_script_of(M, 'wp-146', 4) + [
        "One more thing about the bottom: possible means the group they choose FROM.",
        A("'Chosen from a smaller group? Only that group is possible' appears",
          T('Chosen from a smaller group? Possible $=$ that group only', size=40, gap=40)),
        "Forty students, eighteen of them study music. A music student is chosen. The bottom is eighteen — not forty.",
    ])

    # wp-151 slide 2: OR -> add only separate cases
    M.set_slide('wp-151', 2, script=[
        "When there are several events, there are two kinds of connection.",
        A("'AND → multiply' appears", T('AND — both must happen $\\to$ multiply the probabilities', size=44, gap=50)),
        "One: I want the first event to happen AND the second one too. \"And\" — we multiply.",
        A("'OR → add the separate cases' appears",
          T('OR — either one is enough $\\to$ add the separate cases', size=44, gap=50)),
        "Two: I want the first event OR the second. \"Or\" — we add.",
        "But add only cases that can't happen together. A die shows a two OR a five? It can't show both at once.",
        D('Write "P(2 or 5) = 1/6 + 1/6 = 2/6 = 1/3"'),
        "One sixth plus one sixth. One third.",
        "If the two cases CAN happen together, adding counts the overlap twice. That's the next slide.",
        D('Circle "multiply" and "add"'),
        "By the way — \"or\" questions are much rarer on the exam. They're also the harder ones.",
        "Most of what you'll see is \"and\".",
    ])
    # wp-151 new slide 3: OR with overlap + size check
    M.insert_slides('wp-151', 2, [dict(mode='concept', active=5, title='OR with overlap', script=[
        "An OR where the two cases overlap. You know this from overlapping groups.",
        A("'A number from 1 to 30: divisible by 4 or by 6?' appears",
          T('A number from 1 to 30 is chosen at random. Divisible by 4 OR by 6?', size=40, gap=40)),
        "Possible first: thirty numbers.",
        D('Write "possible = 30"'),
        "Divisible by four: four, eight, and so on up to twenty-eight. Seven numbers.",
        D('Write "by 4: 7"'),
        "Divisible by six: six, twelve, and so on up to thirty. Five numbers.",
        D('Write "by 6: 5"'),
        "Seven plus five is twelve? No! Twelve and twenty-four are on both lists. We counted them twice.",
        D('Write "both: 12, 24 → 2"'),
        A("'OR = first + second − both' appears", T('OR $=$ first $+$ second $-$ both', size=48, gap=40)),
        "First plus second, minus both. The same rule as in overlapping groups.",
        D('Write "7 + 5 − 2 = 10 → 10/30 = 1/3"'),
        "Ten out of thirty. One third.",
    ])])

    # wp-159 slide 2: dice symmetry - keep the (true) opposite-faces remark, add the 7 - x argument and n + 1
    M.video('wp-159')['beats'][1]['active'] = 9
    M.edit_lines('wp-159', 2, lambda ls: ls + [
        {'say': "Why? Swap every face x for seven minus x. A one becomes a six, a two becomes a five, a three becomes a four."},
        {'draw': 'Write "(3, 6) → (4, 1): 9 → 5"'},
        {'say': "Then every pair with sum nine becomes a pair with sum five. Fourteen minus nine is five. Same number of pairs."},
        {'say': "Other dice? For two dice with n faces, the most likely sum is n plus one."},
        {'draw': 'Write "n faces → top sum n + 1 (6 → 7, 8 → 9)"'},
        {'say': "Six faces: seven. Eight faces: nine — not seven."},
    ])
    # wp-159 slide 3: recap
    M.set_slide('wp-159', 3, active=10, script=[
        "Let's lock in probability.",
        A("'wanted ÷ possible, always between 0 and 1' appears",
          T('$P=\\dfrac{\\text{wanted}}{\\text{possible}}$, always between $0$ and $1$', size=40)),
        A("'Possible first' appears", T('Possible first — then wanted', size=40)),
        A("'Complement: 1 − P · at least one = 1 − none' appears",
          T('Complement: $1-P$ $\\cdot$ at least one $=1-$ none', size=40)),
        A("'AND → multiply · OR → add, minus the overlap' appears",
          T('AND $\\to$ multiply $\\cdot$ OR $\\to$ add, minus the overlap', size=40)),
        A("'Two stages: multiply along, add the branches' appears",
          T('Two stages: multiply along a branch, add the branches', size=40)),
        A("'Two dice: sums are symmetric around 7' appears", T('Two dice: sums are symmetric around 7', size=40)),
        D('Underline "Possible first"'),
        "That's the whole toolkit. Next question — the symmetry in action.",
    ])


# ------------------------------------------------------------------------------------------------
# 2. Existing solution videos
# ------------------------------------------------------------------------------------------------
def _existing_solution_videos(M):
    for vid, v in M.D['videos'].items():
        if v['topic'] == TOPIC and v.get('kind') == 'solution':
            M.set_sidebar(vid, ADV_SB if M.section_of(vid) == ADV else LEARN_SB)

    # Q7: independent dice - "forced", not "dependent"
    _replace_say(M, 'solve-wp29-g154', 1, "Two dice, a target sum — and a dependent choice.",
                 "Two dice, a target sum — and a forced choice.")
    _replace_say(M, 'solve-wp29-g154', 3, "Second die: careful. It looks like five options — but it depends on the first die.",
                 "Second die: careful. It looks like five options — but only one number works with the first die.")
    _replace_say(M, 'solve-wp29-g154', 3, "One out of six — a dependent choice, just like in combinations.",
                 "One out of six — a forced choice: only one number works.")
    # Q8: six heads, not seven
    _replace_say(M, 'solve-wp29-g155', 2, "And Sam? Seven heads in a row — what are the chances?",
                 "And Sam? Six heads already — a seventh head in a row? What are the chances?")
    # Q9
    _replace_say(M, 'solve-wp29-g156', 2, "Second die: it has to match the first. Dependent choice again.",
                 "Second die: it has to match the first. A forced choice again.")
    # Q10: drawn together
    M.edit_lines('solve-wp29-g157', 2, lambda ls: ls[:2] + [
        {'say': "Even when a question says two are drawn together — think of them one after the other, without replacement."}
    ] + ls[2:])
    # Q12: 5 and 9 are the same distance from 7 (7 and 9 are not)
    _replace_say(M, 'solve-wp29-g160', 2,
                 "Sometimes it's worded as a story — one friend picks seven, another picks nine. Same idea.",
                 "Sometimes it's a story — one friend bets on a sum of five, another on nine. Same question.")

    # Q11: simple way first, then the two cases as a check (the complement moves to the "at least one" slide)
    _replace_say(M, 'solve-wp29-g158', 1, "The hard kind: an OR question.",
                 "Two tries to find a prize. Start with the simple way.")
    # Pass 2: the original slide "Method 2 · Complement" is restored (it comes back as the third method, slide 4)
    comp = copy.deepcopy(M.slide('solve-wp29-g158', 3))
    M.set_slide('solve-wp29-g158', 2, title='Method 1 · Count the lockers', script=[
        "Possible first: the prize can be in any of seven lockers. Seven equally likely places.",
        D('Write "possible = 7"'),
        "Wanted: the prize is in one of the two lockers you open. Two good places.",
        D('Write "wanted = 2 → 2/7"'),
        "Two out of seven.",
        D('Circle choice 1'),
        "Choice one.",
    ])
    M.set_slide('solve-wp29-g158', 3, title='Method 2 · Two cases', script=[
        "Let's check it step by step — an OR of two separate cases.",
        "Case one: the prize is in the first locker you open.",
        D('Write "case 1: 1/7"'),
        "One out of seven.",
        "Case two: the first locker is empty, AND the second one has it.",
        D('Write "case 2: 6/7 · 1/6 = 1/7"'),
        "Miss the first: six sevenths. Then six lockers are left, and one has it: one sixth. Multiply — one seventh.",
        "The two cases can't happen together. So add them.",
        D('Write "1/7 + 1/7 = 2/7"'),
        "Two sevenths — the same answer.",
        "The trap: \"one seventh on the first try, one sixth on the second\". But you only get a second try after you miss the first.",
        "Think of a driving test. You can't walk in and say: I'm here for my second test. First you have to fail the first one.",
    ])
    M.video('solve-wp29-g158')['beats'].insert(3, comp)
    M.set_slide('solve-wp29-g158', 4, title='Method 3 · Complement', script=[
        D('Write "miss both: 6/7 · 5/6 = 5/7 → 1 − 5/7 = 2/7"'),
        "Or: missing both is six sevenths times five sixths — five sevenths. The complement: two sevenths.",
    ])


# ------------------------------------------------------------------------------------------------
# 3. Existing questions: stems, TeX, solutions with numbers
# ------------------------------------------------------------------------------------------------
def _existing_questions(M):
    S = M.set_q
    for qid, q in M.D['questions'].items():            # stray spaces around stems
        if q['topic'] == TOPIC and q['stemRich'] != q['stemRich'].strip():
            S(qid, stem=q['stemRich'].strip())

    S('wp29-g147', expl=['Possible: the dice has 8 equally likely faces.',
                         'Wanted: the even faces 2, 4, 6 and 8 — that is 4 faces.',
                         '$P=\\frac48=\\frac12$.'])
    S('wp29-g148', stem='A bag contains 5 green counters and 4 orange counters. One counter is drawn at random. What is the probability that it is green?',
      expl=['Possible: $5+4=9$ counters, all equally likely.',
            'Wanted: any of the 5 green counters (not 1 — every green counter is good).',
            '$P(\\text{green})=\\frac59$.'])
    S('wp29-g149', expl=['The three purple beads are already out, so update the bag first.',
                         'Possible: $13-3=10$ beads. Wanted: $8-3=5$ purple beads.',
                         '$P=\\frac5{10}=\\frac12$. Do not multiply by the chance of the earlier draws — they already happened.'])
    S('wp29-g150', stem='A box contains 28 tokens. Each token is either gold or silver. When a token is drawn at random, the probability that it is gold is $\\frac37$. How many silver tokens are in the box?',
      expl=['Complement: $P(\\text{silver})=1-\\frac37=\\frac47$.',
            'Silver tokens out of 28: $\\frac x{28}=\\frac47$, so $7x=4\\cdot28$ and $x=16$.',
            'Or find the gold first: $\\frac37\\cdot28=12$ gold, so $28-12=16$ silver.'])
    S('wp29-g152', stem='A fair coin is tossed, and a fair eight-sided dice numbered 1 through 8 is rolled. What is the probability of getting heads and a 5?',
      expl=['$P(\\text{heads})=\\frac12$ and $P(5)=\\frac18$.',
            'We need both (AND), so multiply: $\\frac12\\cdot\\frac18=\\frac1{16}$.',
            'Check by counting: $2\\cdot8=16$ equally likely pairs, and only one of them is heads with a 5.'])
    S('wp29-g153', stem='A fair coin is tossed four times. What is the probability of getting tails on all four tosses?',
      expl=['Each toss gives tails with probability $\\frac12$.',
            'Tails AND tails AND tails AND tails: $\\left(\\frac12\\right)^4=\\frac1{16}$.'])
    S('wp29-g154', stem='A fair six-sided dice is rolled twice. What is the probability that the sum of the two results is 8?',
      expl=['Possible: $6\\cdot6=36$ ordered pairs.',
            'Wanted: a sum of 8 — $(2, 6)$, $(3, 5)$, $(4, 4)$, $(5, 3)$, $(6, 2)$. That is 5 pairs. $(2, 6)$ and $(6, 2)$ are different results, and $(4, 4)$ is counted once.',
            'Roll by roll: the first roll must not be 1 ($\\frac56$), and then exactly one number works on the second roll ($\\frac16$): $\\frac56\\cdot\\frac16=\\frac5{36}$.'])
    S('wp29-g155', expl=['A fair coin has no memory. Each new toss gives heads with probability $\\frac12$.',
                         'Rosa: $\\frac12$. Sam: $\\frac12$. The probabilities are equal.'])
    S('wp29-g156', expl=['The first dice can show anything: probability $\\frac88=1$.',
                         'The second dice must show the same number: 1 good face out of 8, so $\\frac18$.',
                         '$1\\cdot\\frac18=\\frac18$. Check by counting: 8 doubles out of $8\\cdot8=64$ pairs, and $\\frac8{64}=\\frac18$.'])
    S('wp29-g157', stem='A bag contains 4 red counters and 4 yellow counters. Two counters are drawn at random, without replacement. What is the probability that they are different colors?',
      expl=['The first counter can be any color: probability 1.',
            'Without replacement, 7 counters are left, and 4 of them are the other color: $\\frac47$.',
            '$1\\cdot\\frac47=\\frac47$. Check with the two orders: red then yellow, OR yellow then red: $\\frac48\\cdot\\frac47+\\frac48\\cdot\\frac47=\\frac27+\\frac27=\\frac47$.'])
    S('wp29-g158', expl=['Possible: the prize is in one of 7 equally likely lockers. Wanted: it is in one of the 2 lockers you open.',
                         '$P=\\frac27$.',
                         'Check with two separate cases: the prize is in the first locker, $\\frac17$, OR the first is empty and the second has it, $\\frac67\\cdot\\frac16=\\frac17$. Add: $\\frac17+\\frac17=\\frac27$.'])
    S('wp29-g160', stem='Two fair six-sided dice are rolled. $A$ is the probability that the sum is 9, and $B$ is the probability that the sum is 5. Which of the following is correct?',
      choices=['$A=B$', '$A<B$', '$A>B$', 'It cannot be determined from the information given.'],
      expl=['A sum of 9: $(3, 6)$, $(4, 5)$, $(5, 4)$, $(6, 3)$ — 4 pairs. A sum of 5: $(1, 4)$, $(2, 3)$, $(3, 2)$, $(4, 1)$ — 4 pairs.',
            'Both probabilities are $\\frac4{36}$, so $A=B$.',
            'Faster: 9 and 5 are the same distance from 7. Swap every face $x$ for $7-x$: each pair with sum 9 becomes a pair with sum 5.'])
    S('wp29-g161', stem='Lina chooses one of the 26 letters of the English alphabet at random. Independently, Noah chooses one of the four letters of the name NOAH at random. What is the probability that they choose the same letter?',
      expl=['Let Noah choose first. Any of his 4 letters is fine (they are all English letters): probability 1.',
            'Lina must then choose that one letter out of 26: $\\frac1{26}$.',
            'The long way gives the same: Lina picks one of N, O, A, H ($\\frac4{26}$), and then Noah matches it ($\\frac14$): $\\frac4{26}\\cdot\\frac14=\\frac1{26}$.'])
    S('wp29-g162', stem='A workshop has $r$ groups, and each group has $s$ participants of different ages. One participant is chosen at random from each group, independently. What is the probability that the oldest participant is chosen in every group?',
      expl=['In each group exactly one participant is the oldest: probability $\\frac1s$.',
            'All $r$ groups must succeed (AND): $\\left(\\frac1s\\right)^r=\\frac1{s^r}=s^{-r}$.',
            'Check with numbers: $r=2$ and $s=3$ give $\\frac13\\cdot\\frac13=\\frac19$. Only $s^{-r}=3^{-2}=\\frac19$ fits (the others give $\\frac18$, $\\frac16$ and $\\frac23$).'])
    S('wp29-g163', stem='Factory A makes 800 buttons a day, and 40 of them are blue. Factory B makes 400 buttons a day, and 110 of them are blue. One button is chosen at random from the buttons both factories make in one day. What is the probability that it is not blue?',
      expl=['Total: $800+400=1{,}200$ buttons. Blue: $40+110=150$.',
            '$P(\\text{blue})=\\frac{150}{1{,}200}=\\frac18$, so $P(\\text{not blue})=1-\\frac18=\\frac78$.',
            'Directly: not blue $=760+290=1{,}050$, and $\\frac{1{,}050}{1{,}200}=\\frac78$.'])
    S('wp29-g164', stem='A music app offers five genres. Each day, Tia chooses at random one of the four genres she did not choose the day before. On Monday she chose jazz. What is the probability that she chooses folk on Wednesday?',
      expl=['Monday (jazz) is given, so it has probability 1.',
            'Tuesday: 4 genres are allowed (not jazz). Folk on Tuesday would block folk on Wednesday, so Tuesday must be one of the other 3: $\\frac34$.',
            'Wednesday: 4 genres are allowed (all but Tuesday\'s genre), and folk is one of them: $\\frac14$.',
            '$\\frac34\\cdot\\frac14=\\frac3{16}$.'])
    S('wp29-g165', stem='A jar contains 6 red sweets and 1 blue sweet. The sweets are drawn at random one at a time, without replacement, until the jar is empty. What is the probability that the fifth sweet drawn is blue?',
      expl=['The first four sweets must be red, and then the blue one comes: $\\frac67\\cdot\\frac56\\cdot\\frac45\\cdot\\frac34\\cdot\\frac13$.',
            'Everything cancels: $\\frac17$.',
            'Faster (symmetry): the blue sweet is equally likely to be in any of the 7 places, so $P(\\text{fifth})=\\frac17$.'])

    # ---- practice ----
    S('wp29-p01', expl=['After one red token is removed: $12-1=11$ red tokens and $20-1=19$ tokens in all.',
                        '$P(\\text{red})=\\frac{11}{19}$.'])
    S('wp29-p02', expl=['Equal probabilities mean equal numbers of white and black tokens, say $w$ of each.',
                        'Orange $=14-2w$. This is an even number, so it can be 6 (with $w=4$), but not 5, 7 or 9.'])
    S('wp29-p04', stem='Factory A makes 200 bulbs, and 20 of them are faulty. Factory B makes 100 bulbs, and 25 of them are faulty. One bulb is chosen at random from all the bulbs of both factories. What is the probability that it is not faulty?',
      expl=['Total: $200+100=300$ bulbs. Faulty: $20+25=45$.',
            '$P(\\text{faulty})=\\frac{45}{300}=\\frac3{20}$, so $P(\\text{not faulty})=1-\\frac3{20}=\\frac{17}{20}$.'])
    S('wp29-p05', stem='Two fair eight-sided dice, numbered 1 through 8, are rolled. Which of the following sums is the most likely?',
      expl=['For two dice with $n$ faces, the most likely sum is $n+1$. Here $8+1=9$.',
            'Count: a sum of 9 has 8 pairs, from $(1, 8)$ to $(8, 1)$. A sum of 7 has 6 pairs, and sums of 3 and 15 have 2 pairs each.',
            '9 is the most likely. (7 is the trap — it is the top only for six-sided dice.)'])
    S('wp29-p06', expl=['Green: $\\frac15\\cdot30=6$. Yellow: $\\frac13\\cdot30=10$.', 'Blue: $30-6-10=14$.'])
    S('wp29-p07', stem='A bag contains 6 tokens of each of three colors. Four tokens of one color are removed and not returned. What is the probability that the next token drawn at random is of that same color?',
      expl=['That color has $6-4=2$ tokens left. The bag has $18-4=14$ tokens left.',
            '$P=\\frac2{14}=\\frac17$. It does not matter which color was removed.'])
    S('wp29-p08', expl=['Each roll is odd or even with probability $\\frac12$.',
                        'Four results in a fixed order (AND): $\\left(\\frac12\\right)^4=\\frac1{16}$.'])
    S('wp29-p09', stem='A bag has the same number of tokens in each of five colors. A token is drawn at random and returned to the bag. This is done four times. What is the probability that all four tokens drawn are blue?',
      expl=['Each draw is blue with probability $\\frac15$, and the token is returned each time.',
            '$\\left(\\frac15\\right)^4=\\frac1{625}$.'])
    S('wp29-p10', stem='Bag A contains 8 red tokens and 4 blue tokens. Bag B contains 2 red tokens and 8 blue tokens. One of the bags is chosen at random (each with probability $\\frac12$), and then one token is drawn at random from it. What is the probability that the token is red?',
      expl=['Tree: bag A OR bag B, $\\frac12$ each. Multiply along each branch, then add the branches.',
            'A and red: $\\frac12\\cdot\\frac8{12}=\\frac13$. B and red: $\\frac12\\cdot\\frac2{10}=\\frac1{10}$.',
            '$\\frac13+\\frac1{10}=\\frac{10}{30}+\\frac3{30}=\\frac{13}{30}$. (Pouring both bags together, $\\frac{10}{22}=\\frac5{11}$, is the trap.)'])
    S('wp29-p11', stem='Four people each roll a fair six-sided dice once. What is the probability that Nina rolls a six and the other three do not?',
      expl=['Nina rolls a six: $\\frac16$. Each of the other three does not: $\\frac56$ each.',
            'AND: $\\frac16\\cdot\\left(\\frac56\\right)^3=\\frac16\\cdot\\frac{125}{216}=\\frac{125}{1296}$.'])
    S('wp29-p12', stem='A traveler chooses a sock color at random from 4 colors and, independently, a shoe color at random from 3 colors. Each of the 3 shoe colors is also one of the 4 sock colors. What is the probability that the socks and the shoes are the same color?',
      expl=['There are $4\\cdot3=12$ equally likely sock-and-shoe pairs.',
            'Each of the 3 shoe colors matches exactly one sock color: 3 matching pairs.',
            '$P=\\frac3{12}=\\frac14$. Faster: choose the shoe first (any shoe is fine), and then the sock must match it: $\\frac14$.'])
    S('wp29-p13', expl=['The first four rolls are not 8: $\\frac78$ each. The fifth roll is 8: $\\frac18$.',
                        '$\\left(\\frac78\\right)^4\\cdot\\frac18=\\frac{7^4}{8^5}=\\frac{2401}{32768}$.'])
    S('wp29-p14', stem='A device chooses an integer from 0 through 11 at random (all equally likely). If the number is less than 6, the device adds 2 to it; otherwise, it subtracts 2 from it. Then it displays the result. The device runs twice, independently. What is the probability that the first result is 5 and the second result is not 5?',
      expl=['The result is 5 for the number 3 ($3+2$) or the number 7 ($7-2$): 2 numbers out of 12, so $P(5)=\\frac2{12}=\\frac16$.',
            'Not 5: $1-\\frac16=\\frac56$.',
            'First 5 AND second not 5: $\\frac16\\cdot\\frac56=\\frac5{36}$.'])
    S('wp29-p15', stem='A student owns four badges of different colors. Each day she chooses at random one of the three badges she did not wear the day before. On Monday she wears blue. What is the probability that she wears red on Wednesday?',
      expl=['Tree. Tuesday: 3 badges are allowed (not blue), each with probability $\\frac13$.',
            'If Tuesday is red, Wednesday cannot be red — this branch gives 0.',
            'If Tuesday is one of the other two colors ($\\frac23$), red is one of the 3 allowed badges on Wednesday ($\\frac13$).',
            '$\\frac23\\cdot\\frac13=\\frac29$.'])
    S('wp29-p16', stem='A fair eight-sided dice numbered 1 through 8 is rolled once. A fair coin with 0 on one side and 1 on the other is tossed three times. What is the probability that the sum of the three coin results is greater than the dice result?',
      expl=['The coin sum is 0, 1, 2 or 3. Sums 0 and 1 can never be greater than the dice result (it is at least 1).',
            'Coin sum 2: 3 of the 8 coin sequences ($\\frac38$). It is greater only than a dice result of 1 ($\\frac18$): $\\frac38\\cdot\\frac18=\\frac3{64}$.',
            'Coin sum 3: 1 sequence ($\\frac18$). It is greater than dice results 1 and 2 ($\\frac28$): $\\frac18\\cdot\\frac28=\\frac2{64}$.',
            'Add the separate cases: $\\frac3{64}+\\frac2{64}=\\frac5{64}$.'])
    S('wp29-p17', stem='Five different gifts, two of them books, are given out at random to five friends, one gift each. What is the probability that two particular friends, Ada and Ben, both receive books?',
      expl=['Ada gets a book: $\\frac25$. Then 1 book is left among 4 gifts, so Ben gets it: $\\frac14$.',
            '$\\frac25\\cdot\\frac14=\\frac1{10}$.',
            'Or by symmetry: the two books go to 2 of the 5 friends, and all $\\frac{5\\cdot4}2=10$ pairs of friends are equally likely. Only 1 pair is Ada and Ben: $\\frac1{10}$.'])
    S('wp29-p18', stem='For a biased coin, the probability of heads is $\\frac25$ of the probability of tails. What is the probability of heads?',
      expl=['Heads and tails are in the ratio $2:5$. Together they make $2+5=7$ parts, and together the probabilities make 1.',
            'Heads: $\\frac27$. Check: tails is $\\frac57$, and $\\frac25\\cdot\\frac57=\\frac27$ ✓.'])
    S('wp29-p19', stem='A fair coin has 2 on one side and 3 on the other. It is tossed five times, and the results are added. What is the probability that the total is even?',
      expl=['Look at the last toss. Whatever the first four tosses add up to, adding 2 keeps the total even or odd, and adding 3 changes it.',
            'Exactly one of the two faces of the last toss makes the total even: $P=\\frac12$.'])
    S('wp29-p21', expl=['At least one six $=1-$ no six at all.',
                        'No six: $\\frac56\\cdot\\frac56=\\frac{25}{36}$.',
                        '$1-\\frac{25}{36}=\\frac{11}{36}$. (Adding $\\frac16+\\frac16=\\frac{12}{36}$ counts the double six twice.)'])
    S('wp29-p22', stem='A bag contains 5 red tokens and 4 blue tokens. Two tokens are drawn together at random. What is the probability that they are different colors?',
      expl=['Drawn together $=$ one after the other, without replacement. Different colors: red then blue, OR blue then red.',
            'Red then blue: $\\frac59\\cdot\\frac48=\\frac{20}{72}=\\frac5{18}$. Blue then red: $\\frac49\\cdot\\frac58=\\frac5{18}$.',
            'Add the two orders: $\\frac5{18}+\\frac5{18}=\\frac{10}{18}=\\frac59$.'])
    S('wp29-p23', expl=['One order, for example HHTT: $\\left(\\frac12\\right)^4=\\frac1{16}$.',
                        'Number of orders: choose which 2 of the 4 tosses are heads: $\\frac{4\\cdot3}2=6$ (HHTT, HTHT, HTTH, THHT, THTH, TTHH).',
                        '$6\\cdot\\frac1{16}=\\frac6{16}=\\frac38$.'])
    S('wp29-p24', stem='A number is chosen at random from the integers 1 through 30. What is the probability that it is divisible by 4 or by 6?',
      expl=['Multiples of 4: 4, 8, …, 28 — 7 numbers. Multiples of 6: 6, 12, …, 30 — 5 numbers.',
            '12 and 24 are on both lists, so subtract them once: $7+5-2=10$.',
            '$P=\\frac{10}{30}=\\frac13$. (Adding without subtracting gives $\\frac{12}{30}=\\frac25$ — the trap.)'])
    S('wp29-p25', stem='A box contains 3 red tokens and 7 blue tokens. A token is drawn at random and returned, and then a second token is drawn. What is the probability that exactly one of the two tokens is red?',
      expl=['Exactly one red: red then blue, OR blue then red.',
            'Each order: $\\frac3{10}\\cdot\\frac7{10}=\\frac{21}{100}$.',
            'Add the two orders: $\\frac{42}{100}=\\frac{21}{50}$.'])
    S('wp29-p26', expl=['The student is chosen from the music students only, so possible $=18$ (not 40).',
                        'Wanted: music students who also study art — 10.',
                        '$P=\\frac{10}{18}=\\frac59$.'])
    S('wp29-p27', expl=['At least one fails $=1-$ none fails (all three succeed).',
                        'All succeed: $0.9^3=0.729=72.9\\%$.',
                        '$100\\%-72.9\\%=27.1\\%$.'])

    _sync_stem_copies(M, [q for q in M.D['questions'] if q.startswith('wp29-g')])

    # Pass 2 (plan): the original p03 and p20 stay (text clean-up only)
    S('wp29-p03', stem='Two fair eight-sided dice, each numbered 1 through 8, are rolled. What is the probability that they show the same number?',
      expl=['The first dice can show anything: probability 1.',
            'The second dice must show the same number: 1 good face out of 8, so $\\frac18$.',
            '$1\\cdot\\frac18=\\frac18$. Check by counting: 8 doubles out of $8\\cdot8=64$ pairs, and $\\frac8{64}=\\frac18$.'])
    S('wp29-p20', stem='There are $k$ boxes, and each box contains cards numbered 1 through $m$ ($m\\ge2$). One card is drawn at random from each box, independently. What is the probability that every card drawn is numbered 2?',
      expl=['In each box exactly one card is numbered 2: probability $\\frac1m$.',
            'All $k$ boxes must succeed (AND): $\\left(\\frac1m\\right)^k=\\frac1{m^k}$.',
            'Check with numbers: $k=2$ and $m=3$ give $\\frac13\\cdot\\frac13=\\frac19$. Only $\\frac1{m^k}=\\frac1{3^2}=\\frac19$ fits (the others give $\\frac23$, $\\frac18$ and $\\frac16$).'])


# ------------------------------------------------------------------------------------------------
# 4. New lesson part after Q11 + three guided questions (overlap, at least one, tree)
# ------------------------------------------------------------------------------------------------
def _more_rules_block(M):
    v = M.new_video(MORE, TOPIC, 'Probability', LESSON_SB, [
        dict(mode='title', title='At Least One & Trees', script=[
            "Three more tools. These are the harder exam questions.",
        ]),
        dict(mode='concept', active=6, title='At least one', script=[
            "\"At least one\" means one, two, or more. That's a lot of cases.",
            "The opposite is only one case: none at all.",
            A("'P(at least one) = 1 − P(none)' appears",
              T('$P(\\text{at least one})=1-P(\\text{none})$', size=52, gap=50)),
            "Two dice. What's the chance of at least one six?",
            "None: the first dice isn't a six — five sixths. AND the second isn't a six — five sixths.",
            D('Write "none: 5/6 · 5/6 = 25/36"'),
            D('Write "at least one: 1 − 25/36 = 11/36"'),
            "One minus twenty-five thirty-sixths: eleven thirty-sixths.",
            D('Write "not 1/6 + 1/6 = 12/36"'),
            "The trap: one sixth plus one sixth. That counts the double six twice — twelve thirty-sixths instead of eleven.",
        ]),
        dict(mode='concept', active=7, title='Exactly one', script=[
            "Exactly one red in two draws. Which draw is the red one — the first or the second?",
            "Two orders. They can't happen together, so add them.",
            A("'Exactly one = RB + BR' appears", T('Exactly one $=$ RB $+$ BR', size=50, gap=50)),
            "A bag with two red and eight blue. Two draws, with replacement.",
            D('Write "RB: 2/10 · 8/10 = 16/100"'),
            D('Write "BR: 8/10 · 2/10 = 16/100"'),
            D('Write "16/100 + 16/100 = 32/100 = 8/25"'),
            "Sixteen hundredths each. Together: thirty-two hundredths — eight twenty-fifths.",
            A("'Exactly k: one order × number of orders' appears",
              T('Exactly $k$: one order $\\times$ number of orders', size=44, gap=40)),
            "More draws? Every order has the same chance. Find one order, then count the orders.",
            "A coin, three tosses, exactly one head. One order: head, tail, tail. One eighth.",
            D('Write "HTT: (1/2)³ = 1/8"'),
            "How many orders? The head can be first, second or third. Three orders.",
            D('Write "HTT, THT, TTH → 3 · 1/8 = 3/8"'),
            "Three times one eighth: three eighths.",
            A("'Drawn together = one after the other, without replacement' appears",
              T('Drawn together $=$ one after the other, without replacement', size=38)),
            "And when a question says \"two are drawn together\" — treat it as one after the other, without replacement.",
        ]),
        dict(mode='concept', active=8, title='Two stages: a tree', script=[
            "Two stages: first choose a bag, then draw a token from it.",
            "Bag A: three red, one blue. Bag B: one red, five blue. A coin chooses the bag.",
            A("A tree appears: A or B (1/2 each), then red or blue", VIS(FIG_TREE, w=640, h=420)),
            "Draw a tree. First the bag: A or B, one half each.",
            "Then the token. From bag A, red is three quarters. From bag B, red is one sixth.",
            A("'Multiply along a branch · add the branches' appears",
              T('Multiply along a branch $\\cdot$ add the branches', size=42)),
            "Along a branch it's AND: multiply.",
            D('Write "A and red: 1/2 · 3/4 = 3/8"'),
            D('Write "B and red: 1/2 · 1/6 = 1/12"'),
            "The two branches can't happen together — there's only one bag. So it's OR: add.",
            D('Write "3/8 + 1/12 = 9/24 + 2/24 = 11/24"'),
            "Eleven twenty-fourths.",
            "The trap: pour both bags together — four red out of ten. Wrong. The bags aren't the same size, so the tokens don't have equal chances.",
        ]),
    ], LEARN, after='solve-wp29-g158')
    v['hybrid']['num'] = 57
    last = MORE

    # ---- guided A: OR with overlap ----
    g = GID[0]
    M.new_q(g, TOPIC, 'In a class of 30 students, 12 play soccer, 10 play chess, and 4 play both. One student is chosen at random. What is the probability that the student plays soccer or chess?',
            ['$\\frac{11}{15}$', '$\\frac35$', '$\\frac7{15}$', '$\\frac25$'], 2, [
        'Possible: 30 students.',
        'Soccer or chess: $12+10-4=18$ (the 4 students who play both were counted twice).',
        '$P=\\frac{18}{30}=\\frac35$.',
        'Adding without subtracting, $\\frac{22}{30}=\\frac{11}{15}$, is the trap.'])
    M.place_q(g, LEARN, after=last)
    _solution(M, g, 'learn', ["An OR question — and the groups overlap."], [
        ('Add, then subtract the overlap', [
            "Possible first: thirty students.",
            D('Write "possible = 30"'),
            "Soccer: twelve. Chess: ten. Twelve plus ten is twenty-two — but wait.",
            "Four students play both. They are in the twelve AND in the ten. We counted them twice.",
            D('Write "12 + 10 − 4 = 18"'),
            "Subtract them once: eighteen students play soccer or chess.",
            D('Write "18/30 = 3/5" and circle choice 2'),
            "Eighteen out of thirty: three fifths. Choice two.",
            "Twenty-two thirtieths — eleven fifteenths — is choice one. That's the trap.",
        ]),
        ('Method 2 · Two circles', [
            "Or draw two circles, like in overlapping groups.",
            D('Draw two overlapping circles; write 4 in the middle, 8 in "soccer only", 6 in "chess only"'),
            "Both: four. Soccer only: twelve minus four, eight. Chess only: ten minus four, six.",
            D('Write "8 + 4 + 6 = 18"'),
            "Eight plus four plus six: eighteen. The same answer.",
            "The other twelve students play neither. They are not wanted.",
        ]),
    ])
    last = 'solve-' + g

    # ---- guided B: at least one ----
    g = GID[1]
    M.new_q(g, TOPIC, 'Dan answers 3 multiple-choice questions by guessing. Each question has 4 choices, and exactly one of them is correct. What is the probability that Dan answers at least one question correctly?',
            ['$\\frac34$', '$\\frac{27}{64}$', '$\\frac{37}{64}$', '$\\frac1{64}$'], 3, [
        'At least one correct $=1-$ none correct.',
        'Each question is wrong with probability $\\frac34$. All three wrong: $\\left(\\frac34\\right)^3=\\frac{27}{64}$.',
        '$1-\\frac{27}{64}=\\frac{37}{64}$.',
        'Adding $\\frac14+\\frac14+\\frac14=\\frac34$ is the trap: it counts the cases with two or three correct answers more than once.'])
    M.place_q(g, LEARN, after=last)
    _solution(M, g, 'learn', ["At least one — count the opposite."], [
        ('1 minus none', [
            "At least one correct: one, two, or three. Too many cases.",
            "The opposite is one case: none correct.",
            D('Write "at least one = 1 − none"'),
            "One question wrong: three wrong choices out of four. Three quarters.",
            D('Write "none: 3/4 · 3/4 · 3/4 = 27/64"'),
            "All three wrong — AND — multiply: twenty-seven sixty-fourths.",
            D('Write "1 − 27/64 = 37/64" and circle choice 3'),
            "One minus that: thirty-seven sixty-fourths. Choice three.",
        ]),
        ('The traps', [
            "Two traps in the choices.",
            D('Next to choice 2 write "none"'),
            "Twenty-seven sixty-fourths is the chance of NONE. You still have to subtract it from one.",
            D('Next to choice 1 write "1/4 + 1/4 + 1/4"'),
            "Three quarters: one quarter plus one quarter plus one quarter. That adds cases that overlap.",
            "Size check: with five questions, that way gives five quarters — more than one. Impossible.",
        ]),
    ])
    last = 'solve-' + g

    # ---- guided C: two stages (tree) ----
    g = GID[2]
    M.new_q(g, TOPIC, 'Box A contains 2 red balls and 3 white balls. Box B contains 3 red balls and 1 white ball. A fair coin is tossed: on heads, a ball is drawn at random from box A; on tails, a ball is drawn at random from box B. What is the probability that the ball is red?',
            ['$\\frac59$', '$\\frac{23}{40}$', '$\\frac3{10}$', '$\\frac38$'], 2, [
        'Two stages: the box, then the ball. Tree: heads (box A) $\\frac12$, tails (box B) $\\frac12$.',
        'Multiply along each branch: A and red, $\\frac12\\cdot\\frac25=\\frac15$. B and red, $\\frac12\\cdot\\frac34=\\frac38$.',
        'The branches cannot happen together, so add: $\\frac15+\\frac38=\\frac8{40}+\\frac{15}{40}=\\frac{23}{40}$.',
        'Pouring both boxes together ($\\frac59$) is the trap: the boxes have different sizes, so the balls are not equally likely.'])
    M.place_q(g, LEARN, after=last)
    _solution(M, g, 'learn', ["Two stages: first a box, then a ball."], [
        ('Draw a tree', [
            "Stage one: the coin. Heads — box A. Tails — box B. One half each.",
            D('Draw a tree: two branches "A 1/2" and "B 1/2"'),
            "Stage two: the ball. Box A has two red out of five. Box B has three red out of four.",
            D('From A draw "red 2/5"; from B draw "red 3/4"'),
            "Multiply along each branch.",
            D('Write "A and red: 1/2 · 2/5 = 1/5"'),
            D('Write "B and red: 1/2 · 3/4 = 3/8"'),
            "One fifth, and three eighths.",
            "The ball comes from A OR from B — never both. Add the branches.",
            D('Write "1/5 + 3/8 = 8/40 + 15/40 = 23/40" and circle choice 2'),
            "Twenty-three fortieths. Choice two.",
        ]),
        ("Don't pour the boxes together", [
            "The trap: put all nine balls in one box. Five red out of nine — choice one.",
            D('Next to choice 1 write "5/9 ✗"'),
            "Why is it wrong? Box B has only four balls, but it gets half the chances. Each ball in B is more likely to be drawn than a ball in A.",
            "Pouring works only when the boxes are the same size. Use the tree — it always works.",
        ]),
    ])


# ------------------------------------------------------------------------------------------------
# 6. Memory cards
# ------------------------------------------------------------------------------------------------
def _cards(M):
    c = M.card('mem-probability')
    c['intro'] = 'Possible first, then wanted.'
    c['tables'][0]['rows'] = [
        ['\\(P=\\frac{\\text{wanted}}{\\text{possible}}\\)', 'count equally likely outcomes', '5 green, 4 orange: \\(P(\\text{green})=\\frac59\\)'],
        ['\\(0\\le P\\le1\\)', '0 = impossible, 1 = certain', 'no red counters: \\(P(\\text{red})=0\\)'],
        ['Chosen from a smaller group', 'possible = that group only', '10 of the 18 music students study art: \\(\\frac{10}{18}=\\frac59\\)'],
        ['Complement', '\\(P(\\text{not }A)=1-P(A)\\)', 'gold \\(\\frac37\\) → silver \\(\\frac47\\)'],
        ['AND', 'multiply the probabilities', 'heads and a 5 (8-sided): \\(\\frac12\\cdot\\frac18=\\frac1{16}\\)'],
        ['OR, separate cases', 'add', 'a 2 or a 5 on a dice: \\(\\frac16+\\frac16=\\frac13\\) · second try: \\(\\frac17+\\frac67\\cdot\\frac16=\\frac27\\)'],
        ['OR, cases overlap', 'first + second − both', '1 to 30, divisible by 4 or 6: \\(\\frac{7+5-2}{30}=\\frac13\\)'],
        ['At least one', '\\(1-P(\\text{none})\\)', 'two dice, at least one six: \\(1-\\frac{25}{36}=\\frac{11}{36}\\)'],
        ['Exactly one / exactly k', 'one order × number of orders', '3 tosses, exactly 1 head: \\(3\\cdot\\frac18=\\frac38\\)'],
        ['Two stages (tree)', 'multiply along a branch, add the branches', '\\(\\frac12\\cdot\\frac34+\\frac12\\cdot\\frac16=\\frac{11}{24}\\)'],
        ["First pick doesn't matter", 'that stage has probability 1', 'double: \\(1\\cdot\\frac18\\)'],
        ['Without replacement', 'update the bag before the next draw', '8 counters → 7 left'],
        ['History', "past results don't change a fair coin or dice", 'next toss: always \\(\\frac12\\)'],
    ]
    c['tips'] = [
        'Two sums the same distance from 7 have the same probability (swap each face \\(x\\) for \\(7-x\\)).',
        'Two dice with \\(n\\) faces: the most likely sum is \\(n+1\\) (8 faces: 9).',
        'Two drawn together = one after the other, without replacement.',
        '"Or" questions are rare — and a second try only happens after a first miss.',
    ]


# ------------------------------------------------------------------------------------------------
# 7. New practice questions + order easy -> hard
# ------------------------------------------------------------------------------------------------
def _practice(M):
    P = {}
    P[7] = ('In a raffle there are 5 tickets, and 2 of them are winning tickets. Roni draws 2 tickets together at random. What is the probability that at least one of Roni\'s tickets is a winning ticket?',
            ['$\\frac25$', '$\\frac45$', '$\\frac3{10}$', '$\\frac7{10}$'], 4, [
        'At least one winner $=1-$ no winner.',
        'No winner: both tickets are from the 3 losing tickets (without replacement): $\\frac35\\cdot\\frac24=\\frac6{20}=\\frac3{10}$.',
        '$1-\\frac3{10}=\\frac7{10}$. (Adding $\\frac25+\\frac25=\\frac45$ is the trap.)'], None)
    P[8] = ('On any given day, the probability of rain is $\\frac13$. On a rainy day, Maya walks to school with probability $\\frac14$. On a day without rain, she walks to school with probability $\\frac45$. What is the probability that Maya walks to school on a given day?',
            ['$\\frac{21}{40}$', '$\\frac8{15}$', '$\\frac{37}{60}$', '$\\frac1{12}$'], 3, [
        'Tree: rain $\\frac13$ or no rain $\\frac23$, and then walk or not.',
        'Rain and walk: $\\frac13\\cdot\\frac14=\\frac1{12}$. No rain and walk: $\\frac23\\cdot\\frac45=\\frac8{15}$.',
        'Add the branches: $\\frac1{12}+\\frac8{15}=\\frac5{60}+\\frac{32}{60}=\\frac{37}{60}$.'], None)
    P[9] = ('A club has 50 members. 20 of them speak French, 18 speak Spanish, and 22 speak neither language. One member is chosen at random. What is the probability that the member speaks both French and Spanish?',
            ['$\\frac15$', '$\\frac{19}{25}$', '$\\frac{14}{25}$', '$\\frac{11}{25}$'], 1, [
        'Neither: 22, so at least one of the languages: $50-22=28$.',
        'French or Spanish $=$ French $+$ Spanish $-$ both: $28=20+18-\\text{both}$, so both $=10$.',
        '$P=\\frac{10}{50}=\\frac15$.'], None)
    P[10] = ('Three of the 10 students in a class are chosen at random for a committee. Dana and Tal are two of the students. What is the probability that both Dana and Tal are on the committee?',
             ['$\\frac9{100}$', '$\\frac1{45}$', '$\\frac1{15}$', '$\\frac1{120}$'], 3, [
        'Every student has the same chance to be chosen: $P(\\text{Dana})=\\frac3{10}$.',
        'If Dana is chosen, 2 places are left for the other 9 students: $P(\\text{Tal})=\\frac29$.',
        '$\\frac3{10}\\cdot\\frac29=\\frac6{90}=\\frac1{15}$.',
        'By counting: committees with both of them — choose the third member, 8 ways. All committees: $\\frac{10\\cdot9\\cdot8}{3\\cdot2\\cdot1}=120$. $\\frac8{120}=\\frac1{15}$.'], None)
    for k, (stem, ch, cor, ex, fig) in P.items():
        M.new_q(GID[k], TOPIC, stem, ch, cor, ex, figure=fig)
        M.place_q(GID[k], PRACTICE)

    g = GID
    M.practice_order(PRACTICE, [
        'wp29-p01', 'wp29-p06', 'wp29-p07', 'wp29-p09', 'wp29-p08', 'wp29-p03', 'wp29-p04', 'wp29-p02',
        'wp29-p26', 'wp29-p12', 'wp29-p05', 'wp29-p18',
        'wp29-p21', 'wp29-p27', 'wp29-p22', 'wp29-p25', 'wp29-p24', g[9], g[7], 'wp29-p10', g[8], 'wp29-p15',
        'wp29-p11', 'wp29-p20', 'wp29-p14', 'wp29-p23', 'wp29-p19',
        'wp29-p17', g[10], 'wp29-p13', 'wp29-p16'])


# ------------------------------------------------------------------------------------------------
# 8. Pass 2: summary lesson right before the practice (end of "Further guided examples")
# ------------------------------------------------------------------------------------------------
def _summary(M):
    sb = ['Wanted over possible', 'Possible first', 'The complement', 'AND · OR', 'At least one · exactly one',
          'Two stages: a tree', 'Shortcuts', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of probability.",
            "Everything important, one idea at a time."]),
        S(0, [
            A("'P = wanted ÷ possible' appears", T('$P=\\dfrac{\\text{wanted}}{\\text{possible}}$', size=54, gap=40)),
            "Probability is wanted over possible. Count outcomes that are equally likely.",
            A("'3 red, 7 yellow: P(red) = 3/10' appears", T('3 red, 7 yellow: $\\ P(\\text{red})=\\frac{3}{10}$', size=44, gap=40)),
            "Three red out of ten counters: three tenths.",
            A("'0 ≤ P ≤ 1 · 0 = impossible · 1 = certain' appears",
              T('$0\\le P\\le1$ — $0$: impossible, $1$: certain', size=44)),
            "A probability is always between zero and one. Bigger than one? Something went wrong."]),
        S(1, [
            A("'Possible first — then wanted' appears", T('Possible first — then wanted', size=48, gap=40)),
            "Always start from the bottom: what CAN happen?",
            A("'Chosen from a smaller group? Possible = that group only' appears",
              T('Chosen from a smaller group? Possible $=$ that group only', size=40, gap=40)),
            "A student from the choir is chosen? The bottom is the fifteen choir students — not all thirty-two students.",
            A("'Without replacement: update the bag' appears", T('Without replacement: update the bag first', size=42, gap=40)),
            "Something was already taken out? Count the bag as it is now.",
            A("'A coin has no memory' appears", T('A fair coin or dice has no memory: next toss $\\frac12$', size=40)),
            "And past results don't change a fair coin. Four heads in a row — the next toss is still one half."]),
        S(2, [
            A("'P(not A) = 1 − P(A)' appears", T('$P(\\text{not }A)=1-P(A)$', size=54, gap=40)),
            "The complement. Something happens or it doesn't — together, one.",
            A("'red 5/12 → blue 7/12' appears", T('red $\\frac{5}{12}\\ \\to\\ $ blue $\\frac{7}{12}$', size=46, gap=40)),
            "Red is five twelfths? Then blue is seven twelfths.",
            "Sometimes the opposite is easier to count. Late trains: one fifth. So on time: four fifths.",
            "But answer what they asked. One fifth is the late trap."]),
        S(3, [
            A("'AND → multiply' appears", T('AND — both happen $\\to$ multiply', size=46, gap=40)),
            "AND: multiply. Heads and a three on a dice: one half times one sixth — one twelfth.",
            A("'OR, separate cases → add' appears", T('OR, separate cases $\\to$ add', size=46, gap=40)),
            "OR: add — but only cases that can't happen together. A one or a four: one sixth plus one sixth.",
            A("'OR, overlap: first + second − both' appears", T('OR, cases overlap: first $+$ second $-$ both', size=44, gap=40)),
            "Can they happen together? Subtract the overlap once. From one to thirty, divisible by three or five: ten plus six minus two.",
            A("'Second try: 1/5 + 4/5 · 1/4 = 2/5' appears", T('Second try: $\\frac15+\\frac45\\cdot\\frac14=\\frac25$', size=44)),
            "And a second try only happens after a first miss."]),
        S(4, [
            A("'At least one = 1 − none' appears", T('At least one $=1-P(\\text{none})$', size=48, gap=40)),
            "At least one? Too many cases. Count the opposite — none — and subtract from one.",
            A("'Two coins, at least one head: 1 − 1/4 = 3/4' appears",
              T('Two coins, at least one head: $\\ 1-\\frac14=\\frac34$', size=42, gap=40)),
            "Not one half plus one half — that counts two heads twice.",
            A("'Exactly k: one order × number of orders' appears",
              T('Exactly $k$: one order $\\times$ number of orders', size=42, gap=40)),
            "Exactly one head in four tosses: one order is one sixteenth. Four orders: four sixteenths — one quarter.",
            A("'Drawn together = one after the other, without replacement' appears",
              T('Drawn together $=$ one after the other, without replacement', size=38)),
            "Two drawn together? Treat it as one after the other."]),
        S(5, [
            A("'Multiply along a branch · add the branches' appears",
              T('Multiply along a branch $\\cdot$ add the branches', size=44, gap=40)),
            "Two stages — first a bag, then a token? Draw a tree.",
            A("'1/2 · 1/3 + 1/2 · 1/5 = 4/15' appears",
              T('$\\frac12\\cdot\\frac13+\\frac12\\cdot\\frac15=\\frac{4}{15}$', size=48, gap=40)),
            "Along a branch it's AND — multiply. Different branches are OR — add.",
            "Don't pour the bags together. Different sizes mean different chances.",
            A("'One stage can change the next one' appears", T('One stage can change the next stage', size=42)),
            "And watch the stages that depend on each other. Whoever wins the first prize cannot win the second."]),
        S(6, [
            A("'A stage that can't go wrong = 1' appears", T("A stage that can't go wrong: probability $1$", size=42, gap=40)),
            "Three coins all land the same way? The first can be anything — one. The other two must match: one half times one half — one quarter.",
            "You may choose the order. Start with the stage that can't go wrong.",
            A("'Symmetry: every place is equally likely' appears", T('Symmetry: the red marble is third? $\\frac19$', size=42, gap=40)),
            "One red marble out of nine. First, third or last — always one ninth.",
            A("'Two dice: sums symmetric around 7 · n faces → n + 1' appears",
              T('Two dice: symmetric around $7$ · $n$ faces: top sum $n+1$', size=40, gap=40)),
            "Ten and four are the same distance from seven — same probability. Dice with n faces? The top sum is n plus one.",
            A("'Letters in the choices: plug in numbers' appears", T('Letters in the choices: plug in numbers', size=42)),
            "Letters in the choices? Plug in small numbers. First check that the four choices come out different."]),
        S(7, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('What is possible — everyone, or a smaller group?', size=40, gap=30)),
            A('Check 2 appears', T('AND or OR — multiply or add?', size=40, gap=30)),
            A('Check 3 appears', T('OR: can the cases happen together?', size=40, gap=30)),
            A('Check 4 appears', T('"At least one"? Use $1-$ none.', size=40, gap=30)),
            A('Check 5 appears', T('Did the bag change after a draw?', size=40)),
            "And the traps: adding when you should use one minus none, pouring two bags together, and giving the complement instead of what they asked.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t29-summary', TOPIC, 'Summary: Probability', sb, slides, ADV, after=last)


# =====================================================================================
# 2026-10-05 cut repeats: a lesson slide whose idea a question video teaches is cut;
# ideas no question teaches stay, or move as one line + board item into the question video.
# =====================================================================================
def _add_line(M, vid, n, before_say, line, item=None, label=None):
    """Insert one spoken line (+ optional board item) before the line containing `before_say` (None: at the end)."""
    script = []; hit = False
    add = ([A(label, item)] if item is not None else []) + ([line] if line else [])
    for x in _script_of(M, vid, n):
        if before_say is not None and not hit and before_say in str(x):
            script += add; hit = True
        script.append(x)
    if before_say is None:
        script += add; hit = True
    assert hit, (vid, n, before_say)
    M.set_slide(vid, n, script=script)


def cut_repeats(M):
    LESSONS = ['wp-146', 'wp-147-after', 'wp-151', MORE, 'wp-159']
    old_sb = list(M.video('wp-146')['hybrid']['sidebar'])
    # ---- "And · Or": cut "OR with overlap" -> taught in Q12 (soccer or chess) ----------
    M.remove_slides('wp-151', [3])
    _replace_say(M, 'wp-151', 2, "If the two cases CAN happen together, adding counts the overlap twice. That's the next slide.",
                 "If the two cases CAN happen together, adding counts the overlap twice. We'll see that in a question soon.")
    _add_line(M, 'solve-q-r26-t29-01', 2, 'Subtract them once',
              None, T(r'OR $=$ first $+$ second $-$ both', 38), "'OR = first + second − both' appears")
    # the cut slide's other idea: sometimes YOU find "both" (divisible by 4 or 6 -> both = 12, 24)
    _add_line(M, 'solve-q-r26-t29-01', 3, None,
              "Sometimes you find the overlap yourself. From one to thirty, divisible by four or by six: twelve and twenty-four are on both lists.",
              T(r'$1$–$30$, by $4$ or by $6$: $7+5-2=10$', 38), "'1–30, by 4 or by 6: 7 + 5 − 2 = 10' appears")

    # ---- More rules: keep title + "Exactly one" (no question teaches "one order × number of orders") ----
    M.remove_slides(MORE, [4, 2])          # "Two stages: a tree" -> Q14; "At least one" -> Q13
    M.set_slide(MORE, 1, title='Exactly One', script=[
        'More tools for the harder exam questions.',
        'One of them here: exactly one. The others — OR with overlap, at least one, and two stages — we learn in the questions.'])
    sc = _script_of(M, MORE, 2)            # "drawn together" is already taught in Q10 (g157)
    k = next(i for i, x in enumerate(sc) if not isinstance(x, str) and 'Drawn together' in str(x))
    M.set_slide(MORE, 2, script=sc[:k] + ["Let's see the other tools in the questions."])

    # ---- Dice symmetry: cut the Recap (the card and the summary keep it) ----------------
    M.remove_slides('wp-159', [3])
    _add_line(M, 'wp-159', 2, None, "Next question — the symmetry in action.")

    # ---- one shared sidebar for the five lesson parts --------------------------------
    gone = ['OR with overlap', 'At least one', 'Two stages: a tree', 'Recap']
    new_sb = [x for x in old_sb if x not in gone]
    for vid in LESSONS:
        for b in M.video(vid)['beats']:
            if b.get('mode') == 'concept':
                b['active'] = new_sb.index(old_sb[b['active']])
        M.set_sidebar(vid, new_sb)


# =====================================================================================
# 2026-10-06 new exam methods (teacher-approved). Nothing in topic 29 is recorded.
# "Which door?" — COUNT / PATH / SYMMETRY: a table at the top of the memory card + one summary slide.
# =====================================================================================
def add_methods(M):
    c = M.card('mem-probability')
    c['tables'].insert(0, {'title': 'Which door? Decide first', 'head': ['Door', 'When', 'Do', 'Example'], 'rows': [
        ['COUNT', 'equally likely outcomes you can list (dice, a bag)', 'wanted $\\div$ all',
         'two dice, sum $7$: $\\frac{6}{36}=\\frac16$'],
        ['PATH', 'the story happens in steps (draws one after another, rounds)', 'multiply along the path, add the paths',
         '3 red, 2 blue, 2 red in a row: $\\frac35\\cdot\\frac24=\\frac{3}{10}$'],
        ['SYMMETRY', 'nothing makes one person or place special', 'everyone has the same chance: $\\frac1n$',
         '5 people in a random line, Dana last: $\\frac15$']]})

    vid = 'r26-t29-summary'
    v = M.video(vid)
    k = next(i for i, b in enumerate(v['beats'], 1) if b['title'] == 'Before you practice')
    M.insert_slides(vid, k - 1, [dict(mode='concept', active=k - 2, title='Which door?', script=[
        'Before you practice — pick the door first.',
        A("'COUNT' appears", T(r'COUNT: equally likely outcomes $\to$ wanted $\div$ all', size=36, gap=40)),
        'Door one, count: every outcome is equally likely and easy to list — dice, a bag. Wanted over all.',
        A("'two dice, sum 7' appears", T(r'two dice, sum $7$: $\frac{6}{36}=\frac16$', size=32, gap=20)),
        'Two dice, sum seven: six pairs out of thirty-six.',
        A("'PATH' appears", T(r'PATH: the story in steps $\to$ multiply along the path, add the paths', size=36, gap=40)),
        'Door two, path: the story happens in steps. Multiply along the path. Several paths to what you want? Add them.',
        A("'3 red, 2 blue' appears", T(r'3 red, 2 blue, two reds in a row: $\frac35\cdot\frac24=\frac{3}{10}$', size=32, gap=20)),
        'Three fifths, then two quarters — one red is already gone. Three tenths.',
        A("'SYMMETRY' appears", T(r'SYMMETRY: everyone has the same chance $\to$ $\frac1n$', size=36, gap=40)),
        'Door three, symmetry: nobody is special, so the chance splits equally.',
        A("'Dana last' appears", T(r'5 people in a random line, Dana last: $\frac15$', size=32, gap=20)),
        'Dana is last with chance one fifth. First or third — the same. No counting at all.',
        'Three doors — and most of the exam\'s probability questions go through one of them.'])])
    sb = list(v['hybrid']['sidebar'])
    M.set_sidebar(vid, sb[:k - 2] + ['Which door?'] + sb[k - 2:])
    v['beats'][k]['active'] = k - 1   # "Before you practice" moves down one


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
    _pm_add(M, 'q-r26-t29-11', [r'Door: SYMMETRY — no pair of students is special. There are $\frac{10\cdot9}{2}=45$ pairs, the committee holds $3$ of them, and every pair has the same chance: $\frac{3}{45}=\frac1{15}$.'])
    _pm_add(M, 'wp29-p22', [r'Door: COUNT — every pair of tokens is equally likely: $\frac{9\cdot8}{2}=36$ pairs, and $5\cdot4=20$ of them have one red and one blue token. $\frac{20}{36}=\frac59$.'])
    _pm_add(M, 'q-r26-t29-08', [r'Door: COUNT — all $\frac{5\cdot4}{2}=10$ pairs of tickets are equally likely. Pairs with no winner: $\frac{3\cdot2}{2}=3$. Pairs with a winner: $10-3=7$. $P=\frac7{10}$.'])
    _pm_add(M, 'wp29-p21', [r'Door: COUNT — $36$ equally likely pairs. A six on the first dice: $6$ pairs. A six on the second: $6$ pairs. The pair (6, 6) is in both: $6+6-1=11$. $P=\frac{11}{36}$.'])
    _pm_add(M, 'wp29-p10', [r'Door: PATH, not COUNT — the $22$ tokens are not equally likely. Each token in bag A has $\frac12\cdot\frac1{12}=\frac1{24}$, and each token in bag B has $\frac12\cdot\frac1{10}=\frac1{20}$. That is why pouring the bags together ($\frac5{11}$) is wrong.'])
    _pm_add(M, 'wp29-p16', [r'Door: COUNT — $8$ dice results times $8$ coin sequences: $64$ equally likely outcomes. Good ones: coin sum $2$ ($3$ sequences) with dice $1$: $3$. Coin sum $3$ ($1$ sequence) with dice $1$ or $2$: $2$. $P=\frac{3+2}{64}=\frac5{64}$.'])


# ======================================================================================================
# 2026-10-06 renumber pass (runs LAST). The English course must not look like the Hebrew one: every Hebrew-derived
# question (guided wp29-g147 … g165, practice wp29-p01 … p20) gets new numbers and a new story; idea, trap, level and
# methods stay. Every guided solution video is rewritten to match. 8-sided dice are gone (dice are always 6-sided):
# where the old item needed other numbers it uses a spinner with equal sections or numbered cards. The summary, the
# card and the dice-symmetry lesson lose the examples that landed on the Hebrew numbers (heads and a 3 = 1/12, five
# doors 1/5 + 4/5 · 1/4, sums 10 and 4, four heads in a row, pass 2/3 / fail 1/3). Practice clean-up 31 -> 24.
# Nothing in topic 29 is recorded (checked ~/Documents/Course.recordings 2026-10-06).
# ======================================================================================================
RN_RECORDED = set()


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides, titles=None):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. The pre-loaded question stays."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        t = (titles or {}).get(n)
        M.set_slide(vid, n, script=script, title=t)


def _rn_item(M, vid, n, k):
    return copy.deepcopy(M.slide(vid, n)['items'][k])


def _rn_sub(M, vid, n, pairs):
    """Exact substring replacements in one slide's spoken / drawn lines, labels and board items (each must hit)."""
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = False
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit = True
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit = True
        assert hit, (vid, n, old)
    M.touched_videos.add(vid)


def _rn_slide_no(M, vid, title):
    return next(i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title)


def rn_guided(M):
    # ---------- g147: 8-sided die, even -> 1/2  ==>  spinner with 10 equal sections, even -> 5/10 = 1/2
    g = 'wp29-g147'
    _rn_q(M, g, 'A spinner is divided into 10 equal sections numbered 1 through 10. The spinner is spun once. '
                'What is the probability that it stops on an even number?',
          ['$\\frac1{10}$', '$\\frac12$', '$\\frac25$', '$\\frac35$'], 2, [
        'Possible: the spinner has 10 equally likely sections.',
        'Wanted: the even numbers 2, 4, 6, 8 and 10 — that is 5 sections.',
        '$P=\\frac5{10}=\\frac12$.'])
    _rn_video(M, g, [[
        "Possible first. Ten equal sections: ten results.",
        D('Write "possible = 10"'),
        "So the bottom is ten.",
        "Now the wanted: an even number.",
        D('Write "wanted: 2, 4, 6, 8, 10 → 5"'),
        "Two, four, six, eight, ten. Five good results.",
        D('Write "5/10 = 1/2" and circle choice 2'),
        "Five out of ten — reduce it: one half. Choice two.",
        "A question this easy won't be on the exam. But the routine — possible, then wanted — is exactly what you'll use.",
    ], [
        "A quick extra way to see it.",
        D('Pair the sections: (1, 2) (3, 4) (5, 6) (7, 8) (9, 10)'),
        "Pair the numbers. Every pair has one odd and one even.",
        "So exactly half the sections are even. One half.",
    ]])

    # ---------- g148: 5 green, 4 orange -> 5/9  ==>  7 green, 4 yellow marbles (review: the Hebrew had 5 blue, 4 white) -> 7/11 (trap: wanted = 1)
    g = 'wp29-g148'
    _rn_q(M, g, 'A box contains 7 green marbles and 4 yellow marbles. One marble is drawn at random. '
                'What is the probability that it is green?',
          ['$\\frac4{11}$', '$\\frac1{11}$', '$\\frac7{11}$', '$\\frac74$'], 3, [
        'Possible: $7+4=11$ marbles, all equally likely.',
        'Wanted: any of the 7 green marbles (not 1 — every green marble is good).',
        '$P(\\text{green})=\\frac7{11}$.'])
    _rn_video(M, g, [[
        "Possible first: all the marbles. Seven plus four — eleven.",
        D('Write "possible = 11"'),
        "Now the wanted: green.",
        "Here's the classic mistake. Students say: we're drawing ONE marble, so the wanted is one.",
        D('Write "wanted = 1" and cross it out'),
        "No! We draw one marble — but there are seven green marbles, and every one of them is good for us.",
        D('Write "wanted = 7"'),
        "Picture all eleven marbles. Any of the seven green ones — success.",
        D('Write "7/11" and circle choice 3'),
        "Seven out of eleven. Choice three.",
    ]])

    # ---------- g149: 8 purple, 5 white, 3 purple out -> 5/10  ==>  11 orange, 7 white, 4 orange out -> 7/14 = 1/2
    g = 'wp29-g149'
    _rn_q(M, g, 'A bag initially contains 11 orange beads and 7 white beads. Four orange beads have already been removed '
                'and not replaced. What is the probability that the next bead drawn at random is orange?',
          ['$\\frac12$', '$\\frac{11}{14}$', '$\\frac7{18}$', '$\\frac{11}{18}$'], 1, [
        'The four orange beads are already out, so update the bag first.',
        'Possible: $18-4=14$ beads. Wanted: $11-4=7$ orange beads.',
        '$P=\\frac7{14}=\\frac12$. Do not multiply by the chance of the earlier draws — they already happened.'])
    _rn_video(M, g, [[
        "Possible first. There were eighteen beads — but four were already taken out.",
        D('Write "possible = 18 − 4 = 14"'),
        "Fourteen beads left in the bag. That's the bottom.",
        "The wanted: orange. There were eleven — four already came out.",
        D('Write "wanted = 11 − 4 = 7"'),
        "That already happened. It's the past — it doesn't interest us. Seven orange left.",
        D('Write "7/14 = 1/2" and circle choice 1'),
        "Seven out of fourteen. One half. Choice one.",
        "Don't multiply by the chance of those first four draws — they're a given fact, not part of the question.",
    ], [
        "Quick check.",
        D('Write "7 orange · 7 white"'),
        "Seven orange, seven white. Equal groups — so each color has half the chance.",
    ]])

    # ---------- g150: 28 tokens, gold 3/7 -> silver 16  ==>  36 tokens, red 4/9 -> blue 20 (trap: red 16)
    g = 'wp29-g150'; vid = 'solve-' + g
    rule = _rn_item(M, vid, 2, 1)
    _rn_q(M, g, 'A box contains 36 tokens. Each token is either red or blue. When a token is drawn at random, the '
                'probability that it is red is $\\frac49$. How many blue tokens are in the box?',
          ['24', '16', '30', '20'], 4, [
        'Complement: $P(\\text{blue})=1-\\frac49=\\frac59$.',
        'Blue tokens out of 36: $\\frac x{36}=\\frac59$, so $9x=5\\cdot36$ and $x=20$.',
        'Or find the red first: $\\frac49\\cdot36=16$ red, so $36-16=20$ blue.'])
    _rn_video(M, g, [[
        A('The complement rule appears', rule),
        "All the probabilities together always make one.",
        "If my chance of passing an exam is three quarters, my chance of failing is one quarter. Pass or fail — there's no third option.",
        "A coin: heads one half, tails one half. Together — one.",
        "Now the question. Red has probability four ninths.",
        D('Write "blue = 1 − 4/9 = 5/9"'),
        "So blue completes it to one: five ninths.",
        "And what is that probability? Blue tokens out of all thirty-six tokens.",
        D('Write "x/36 = 5/9"'),
        "x blue out of thirty-six equals five ninths.",
        D('Cross-multiply: write "9x = 5 · 36 → x = 20"'),
        "Cross-multiply: nine x equals five times thirty-six. x is twenty.",
        D('Circle choice 4'),
        "Twenty blue tokens. Choice four.",
    ], [
        "Or find the red first.",
        D('Write "4/9 of 36 = 16 → 36 − 16 = 20"'),
        "Four ninths of thirty-six: sixteen red. Thirty-six minus sixteen — twenty blue.",
        "Careful: sixteen is the red count. They asked for blue.",
    ]], titles={3: 'Method 2 · Red first'})

    # ---------- g152: coin + 8-sided die, heads and 5 -> 1/16  ==>  coin + spinner (5 sections), tails and 4 -> 1/10
    g = 'wp29-g152'
    _rn_q(M, g, 'A fair coin is tossed, and a spinner divided into 5 equal sections numbered 1 through 5 is spun. '
                'What is the probability of getting tails and a 4?',
          ['$\\frac7{10}$', '$\\frac15$', '$\\frac1{10}$', '$\\frac12$'], 3, [
        '$P(\\text{tails})=\\frac12$ and $P(4)=\\frac15$.',
        'We need both (AND), so multiply: $\\frac12\\cdot\\frac15=\\frac1{10}$.',
        'Check by counting: $2\\cdot5=10$ equally likely pairs, and only one of them is tails with a 4.'])
    _replace_say(M, 'solve-' + g, 1, "Two events: a coin and a die.", "Two events: a coin and a spinner.")
    _rn_video(M, g, [[
        "We want tails AND a four. \"And\" — multiply.",
        D('Write "P(tails) = 1/2"'),
        "Tails: one half.",
        D('Write "P(4) = 1/5"'),
        "A four on a spinner with five equal sections: one good result out of five.",
        D('Write "1/2 · 1/5 = 1/10" and circle choice 3'),
        "One half times one fifth: one tenth. Choice three.",
    ], [
        "Check it by counting.",
        D('Write "2 · 5 = 10 pairs, 1 good"'),
        "Two coin results times five spinner results — ten equally likely pairs. Exactly one is tails-and-four.",
    ]])

    # ---------- g153: 4 tosses, all tails -> 1/16  ==>  5 tosses, all tails -> 1/32
    g = 'wp29-g153'
    _rn_q(M, g, 'A fair coin is tossed five times. What is the probability of getting tails on all five tosses?',
          ['$\\frac1{16}$', '$\\frac1{32}$', '$\\frac12$', '$\\frac18$'], 2, [
        'Each toss gives tails with probability $\\frac12$.',
        'Tails AND tails AND tails AND tails AND tails: $\\left(\\frac12\\right)^5=\\frac1{32}$.'])
    _rn_video(M, g, [[
        "Tails on the first toss — one half.",
        "Tails on the second — also one half. The third, the fourth, the fifth — one half each.",
        D('Write "1/2 · 1/2 · 1/2 · 1/2 · 1/2"'),
        "We want tails on the first AND the second AND the third AND the fourth AND the fifth. \"And\" — multiply.",
        D('Write "= 1/32" and circle choice 2'),
        "One thirty-second. Choice two.",
    ], [
        D('Write "2⁵ = 32 sequences, only TTTTT"'),
        "Two times two times two times two times two: thirty-two sequences. Only one is all tails.",
    ]])

    # ---------- g154: two dice, sum 8 -> 5/36  ==>  sum 5 -> 4/36 = 1/9 (traps: 1/18 unordered, 1/6 sum 7)
    g = 'wp29-g154'; vid = 'solve-' + g
    grid = _rn_item(M, vid, 3, 1); grid['v'] = dict(grid['v'], target=5); grid.update(x=660, w=900)
    _rn_q(M, g, 'A fair six-sided dice is tossed twice. What is the probability that the sum of the two results is 5?',
          ['$\\frac1{18}$', '$\\frac16$', '$\\frac19$', '$\\frac5{36}$'], 3, [
        'Possible: $6\\cdot6=36$ ordered pairs.',
        'Wanted: a sum of 5 — $(1, 4)$, $(2, 3)$, $(3, 2)$, $(4, 1)$. That is 4 pairs: $\\frac4{36}=\\frac19$. '
        '$(1, 4)$ and $(4, 1)$ are different results.',
        'Toss by toss: the first toss must be 1, 2, 3 or 4 ($\\frac46$), and then exactly one number works on the second '
        'toss ($\\frac16$): $\\frac46\\cdot\\frac16=\\frac4{36}=\\frac19$.'])
    _rn_video(M, g, [[
        "Let's lay it out so we can see it. When is the sum five?",
        D('Write "1+4, 2+3, 3+2, 4+1"'),
        "First die one — second must be four. Two — three. Three — two. Four — one.",
        "Four options. Two dice give six times six — thirty-six possibilities. Four out of thirty-six — we could stop here.",
        "But let's practice the method we'll use on harder questions: each die on its own, then multiply.",
    ], [
        "First die: what can it show? One, two, three or four. A five or a six is already too big.",
        D('Write "first die: 4/6"'),
        "Four good results out of six.",
        "Second die: careful. It looks like four options — but only one number works with the first die.",
        "Got a one first? You MUST get a four. Got a three? You MUST get a two. Only one good result.",
        D('Write "second die: 1/6"'),
        "One out of six — a forced choice: only one number works.",
        D('Write "4/6 · 1/6 = 4/36 = 1/9" and circle choice 3'),
        "We want the first AND the second: multiply. Four thirty-sixths — one ninth. Choice three.",
        A('The grid of 36 pairs appears, sum 5 highlighted', grid),
        "And here's the full grid — four highlighted cells out of thirty-six.",
        "One eighteenth is the trap: it counts one-four and four-one as one result. They are two different results.",
    ]])

    # ---------- g155: Rosa / Sam, six in a row  ==>  Omar / Kate, seven in a row (still equal)
    g = 'wp29-g155'
    _rn_q(M, g, 'Omar has tossed a fair coin and obtained tails seven times in a row. Kate has tossed another fair coin and '
                'obtained heads seven times in a row. All tosses are independent. How do their probabilities of heads '
                'on the next toss compare?',
          ['They are equal', 'Kate’s probability is greater', 'Omar’s probability is greater',
           'The probabilities cannot be compared'], 1, [
        'A fair coin has no memory. Each new toss gives heads with probability $\\frac12$.',
        'Omar: $\\frac12$. Kate: $\\frac12$. The probabilities are equal.'])
    _rn_video(M, g, [[
        "At first glance it looks like Omar should get heads now. Seven tails in a row — heads has to come!",
        "And Kate? Seven heads already — an eighth head in a row? What are the chances?",
        "It only looks that way. What happened in the past doesn't affect the future.",
        D('Write "Omar: 1/2 · Kate: 1/2"'),
        "The coin doesn't know what came before. Every toss: heads one half, tails one half.",
        "Think of a roulette table. People wait for eight reds in a row — then bet on black. It means nothing. Still one half.",
        "And someone who just walked up to the table doesn't know the history. The chance can't be different for them.",
        D('Circle choice 1'),
        "The chances are equal. Choice one.",
        "This one is rare on the exam — but when it shows up, it's meant to trick you.",
    ]])

    # ---------- g156: two 8-sided dice match -> 1/8  ==>  two spinners with 5 equal sections match -> 1/5
    g = 'wp29-g156'; vid = 'solve-' + g
    grid = _rn_item(M, vid, 3, 1); grid['v'] = dict(grid['v'], sides=5); grid.update(x=660, y=300, w=900)
    _rn_q(M, g, 'Two spinners are each divided into 5 equal sections numbered 1 through 5. Both spinners are spun, '
                'independently. What is the probability that they show the same number?',
          ['$\\frac45$', '$\\frac15$', '$\\frac1{25}$', '$\\frac25$'], 2, [
        'The first spinner can show anything: probability $\\frac55=1$.',
        'The second spinner must show the same number: 1 good section out of 5, so $\\frac15$.',
        '$1\\cdot\\frac15=\\frac15$. Check by counting: 5 matching pairs out of $5\\cdot5=25$ pairs, and $\\frac5{25}=\\frac15$.'])
    _replace_say(M, vid, 1, "A double — the same number on both dice.", "A match — the same number on both spinners.")
    _rn_video(M, g, [[
        "First spinner: the result doesn't matter. One, three, five — whatever.",
        D('Write "first spinner: 5/5 = 1"'),
        "All five results are good. Five out of five — one.",
        "Second spinner: it has to match the first. A forced choice again.",
        "Got a four? You need a four. Got a two? You need a two. One good result.",
        D('Write "second spinner: 1/5"'),
        D('Write "1 · 1/5 = 1/5" and circle choice 2'),
        "One times one fifth — one fifth. Choice two.",
    ], [
        A('The 5 × 5 grid appears with its diagonal highlighted', grid),
        D('Write "5 matches / 25 = 1/5"'),
        "You could count directly: five matching pairs out of twenty-five. One fifth.",
        "But my tip: work out each event separately, like we did first. Counting everything at once is where mistakes happen.",
    ]], titles={2: "First spinner doesn't matter", 3: 'Method 2 · Count the matches'})

    # ---------- g157: 4 red, 4 yellow, different colors -> 4/7  ==>  6 green, 6 white -> 6/11 (trap 5/11 = same color)
    g = 'wp29-g157'
    _rn_q(M, g, 'A bag contains 6 green counters and 6 white counters. Two counters are drawn at random, without '
                'replacement. What is the probability that they are different colors?',
          ['$\\frac12$', '$\\frac5{11}$', '$\\frac6{11}$', '$\\frac14$'], 3, [
        'The first counter can be any color: probability 1.',
        'Without replacement, 11 counters are left, and 6 of them are the other color: $\\frac6{11}$.',
        '$1\\cdot\\frac6{11}=\\frac6{11}$. Check with the two orders: green then white, OR white then green: '
        '$\\frac6{12}\\cdot\\frac6{11}+\\frac6{12}\\cdot\\frac6{11}=\\frac3{11}+\\frac3{11}=\\frac6{11}$.'])
    _rn_video(M, g, [[
        "Remember from combinations: with or without replacement? Here — without. A counter that comes out stays out.",
        "And we draw one at a time — first counter, then second.",
        "Even when a question says two are drawn together — think of them one after the other, without replacement.",
        "First counter: its color doesn't matter. We just need the second to be different.",
        D('Write "first: 12/12 = 1"'),
        "Second counter: now only eleven are left in the bag.",
        D('Write "possible = 11"'),
        "Drew a green first? Six whites are still there. Drew a white? Six greens are still there.",
        D('Write "wanted = 6 → 6/11"'),
        D('Write "1 · 6/11 = 6/11" and circle choice 3'),
        "One times six elevenths. Choice three.",
    ], [
        D('Write "6/12 · 6/11 + 6/12 · 6/11 = 6/11"'),
        "Green then white, or white then green. Two separate orders — add them. Same six elevenths.",
    ]])

    # ---------- g158: 7 lockers, open 2 -> 2/7  ==>  8 boxes, open 2 -> 2/8 = 1/4 (trap 1/8 + 1/7 = 15/56)
    g = 'wp29-g158'
    _rn_q(M, g, 'A prize is equally likely to be in any of 8 closed boxes. You may open 2 different boxes, choosing '
                'without any extra information. What is the probability that you find the prize?',
          ['$\\frac18$', '$\\frac{15}{56}$', '$\\frac14$', '$\\frac2{15}$'], 3, [
        'Possible: the prize is in one of 8 equally likely boxes. Wanted: it is in one of the 2 boxes you open.',
        '$P=\\frac28=\\frac14$.',
        'Check with two separate cases: the prize is in the first box, $\\frac18$, OR the first is empty and the second '
        'has it, $\\frac78\\cdot\\frac17=\\frac18$. Add: $\\frac18+\\frac18=\\frac14$.'])
    _rn_video(M, g, [[
        "Possible first: the prize can be in any of eight boxes. Eight equally likely places.",
        D('Write "possible = 8"'),
        "Wanted: the prize is in one of the two boxes you open. Two good places.",
        D('Write "wanted = 2 → 2/8 = 1/4"'),
        "Two out of eight — one quarter.",
        D('Circle choice 3'),
        "Choice three.",
    ], [
        "Let's check it step by step — an OR of two separate cases.",
        "Case one: the prize is in the first box you open.",
        D('Write "case 1: 1/8"'),
        "One out of eight.",
        "Case two: the first box is empty, AND the second one has it.",
        D('Write "case 2: 7/8 · 1/7 = 1/8"'),
        "Miss the first: seven eighths. Then seven boxes are left, and one has it: one seventh. Multiply — one eighth.",
        "The two cases can't happen together. So add them.",
        D('Write "1/8 + 1/8 = 2/8 = 1/4"'),
        "One quarter — the same answer.",
        "The trap: \"one eighth on the first try, one seventh on the second\" — that's choice two. But you only get a second try after you miss the first.",
        "Think of a driving test. You can't walk in and say: I'm here for my second test. First you have to fail the first one.",
    ], [
        D('Write "miss both: 7/8 · 6/7 = 6/8 = 3/4 → 1 − 3/4 = 1/4"'),
        "Or: missing both is seven eighths times six sevenths — three quarters. The complement: one quarter.",
    ]], titles={2: 'Method 1 · Count the boxes'})

    # ---------- g160: sums 9 and 5  ==>  sums 8 and 6 (same distance from 7 -> A = B)
    g = 'wp29-g160'
    _rn_q(M, g, 'Two fair six-sided dice are tossed. $A$ is the probability that the sum is 8, and $B$ is the probability '
                'that the sum is 6. Which of the following is correct?',
          ['$A>B$', '$A=B$', '$A<B$', 'It cannot be determined from the information given.'], 2, [
        'A sum of 8: $(2, 6)$, $(3, 5)$, $(4, 4)$, $(5, 3)$, $(6, 2)$ — 5 pairs. A sum of 6: $(1, 5)$, $(2, 4)$, $(3, 3)$, '
        '$(4, 2)$, $(5, 1)$ — 5 pairs.',
        'Both probabilities are $\\frac5{36}$, so $A=B$.',
        'Faster: 8 and 6 are the same distance from 7. Swap every face $x$ for $7-x$: each pair with sum 8 becomes a pair '
        'with sum 6.'])
    _rn_video(M, g, [[
        "They're asking which probability is bigger: a sum of eight, or a sum of six.",
        "Sometimes it's a story — one friend bets on a sum of six, another on eight. Same question.",
        D('Write "7 + 1 = 8 · 7 − 1 = 6"'),
        "Eight is one above seven. Six is one below seven.",
        "Same distance from seven — so by symmetry, the same probability.",
        D('Circle choice 2'),
        "A equals B. Choice two. No counting needed — and no chance to get confused counting.",
    ], [
        D('Write "8: (2,6)(3,5)(4,4)(5,3)(6,2) · 6: (1,5)(2,4)(3,3)(4,2)(5,1)"'),
        "If you want proof: five ways each. Five out of thirty-six for both.",
    ]])

    # ---------- g161: 26 letters / NOAH -> 1/26  ==>  7 days of the week / the 2 weekend days -> 1/7 (trap 2/7)
    g = 'wp29-g161'
    _rn_q(M, g, 'Ella chooses one of the 7 days of the week at random. Independently, Omar chooses one of the 2 weekend '
                'days, Saturday or Sunday, at random. What is the probability that they choose the same day?',
          ['$\\frac27$', '$\\frac1{14}$', '$\\frac12$', '$\\frac17$'], 4, [
        'Let Omar choose first. Either of his 2 days is fine (both are days of the week): probability 1.',
        'Ella must then choose that one day out of 7: $\\frac17$.',
        'The long way gives the same: Ella picks Saturday or Sunday ($\\frac27$), and then Omar matches it ($\\frac12$): '
        '$\\frac27\\cdot\\frac12=\\frac17$.'])
    _rn_video(M, g, [[
        "Start with the regular math. Let Ella choose first.",
        "Seven days. Which ones are good for us? Only Omar's two days — Saturday and Sunday.",
        D('Write "Ella: 2/7"'),
        "So Ella picks a good day with probability two out of seven.",
        "Now Omar. Is every one of his days good? No! Only the day Ella already chose.",
        "Say Ella picked Sunday. Now Omar must pick Sunday — one day out of his two.",
        D('Write "Omar: 1/2"'),
        "One half. And it doesn't matter which of the two Ella picked — Omar always needs that one.",
        "Ella AND Omar — an \"and\" connection means multiply.",
        D('Write "2/7 · 1/2", cancel the 2s, write "= 1/7"'),
        "Cancel the twos: one seventh.",
        D('Circle choice 4'),
        "Choice four. And careful — two sevenths is only Ella's step. It's sitting there as a trap.",
    ], [
        "Now a small psychometric flash. Faster — almost no calculation.",
        "The order doesn't matter. They just need the same day. So let Omar go first.",
        "Which of Omar's days are good for us? Both of them! Saturday and Sunday are on Ella's list too.",
        D('Write "Omar: 2/2 = 1"'),
        "Two out of two. Probability one. Omar's choice doesn't interest us at all.",
        "Say he picks Saturday. Now Ella must pick Saturday — one day out of seven.",
        D('Write "Ella: 1/7" and circle choice 4'),
        "One seventh. That's already the answer. Choice four.",
        "When one stage can't go wrong — skip it. Look straight at the stage that can.",
    ]], titles={2: 'Method 1 · Ella first', 3: 'Method 2 · Omar first'})

    # ---------- g162: r groups of s, oldest -> s^(-r), plug r = 2, s = 3  ==>  m rounds of n envelopes -> n^(-m),
    #            plug m = 3, n = 2 (the Hebrew plugged 2 classes / 3 students)
    g = 'wp29-g162'
    _rn_q(M, g, 'A game has $m$ rounds. In each round there are $n$ closed envelopes, and exactly one of them holds a prize. '
                'In each round the player opens one envelope at random. What is the probability that the player wins a '
                'prize in every round?',
          ['$\\frac mn$', '$m^{-n}$', '$n^{-m}$', '$\\frac1{mn}$'], 3, [
        'In each round exactly one envelope holds a prize: probability $\\frac1n$.',
        'All $m$ rounds must succeed (AND): $\\left(\\frac1n\\right)^m=\\frac1{n^m}=n^{-m}$.',
        'Check with numbers: $m=3$ and $n=2$ give $\\frac12\\cdot\\frac12\\cdot\\frac12=\\frac18$. Only $n^{-m}=2^{-3}=\\frac18$ '
        'fits (the others give $\\frac32$, $\\frac19$ and $\\frac16$).'])
    _rn_video(M, g, [[
        "We don't know how many rounds — m of them. We don't know how many envelopes — n in each round.",
        "But in every round, only ONE envelope holds a prize.",
        D('Next to the question write "one round: 1/n"'),
        "So in each round, the chance of opening the prize envelope is one out of n.",
        "We want a prize in this round AND this one AND this one — all m rounds.",
        D('Write "1/n · 1/n · … (m times) = (1/n)^m"'),
        "\"And\" means multiply. One over n, m times: one over n, to the power m.",
        "Is that in the choices? Not in that form. They added some exponent technique.",
        D('Write "= 1/n^m = n^(−m)"'),
        "A fraction to a power: one to the m is just one, and n to the m goes underneath. One over n to the m — and a negative exponent flips it: n to the minus m.",
        D('Circle choice 3'),
        "Choice three.",
    ], [
        "The psychometric way: the choices have letters — so plug in easy numbers.",
        "Try one round with one envelope? The prize is found for sure.",
        "But look at the choices: with ones, every choice becomes one. Useless.",
        "Two and two? Check the choices first: three of them come out one quarter. Useless again.",
        "So here's the rule: when you plug in, check the choices FIRST — make sure they're all different. You'd have to plug into them anyway.",
        D('Write "m = 3, n = 2" and next to the choices write 3/2, 1/9, 1/8, 1/6'),
        "Three rounds, two envelopes each: three halves, one ninth, one eighth, one sixth. All different — good numbers.",
        D('Write "1/2 · 1/2 · 1/2 = 1/8"'),
        "Now the question: one half in each of the three rounds. Multiply — one eighth.",
        D('Circle choice 3'),
        "One eighth — choice three. Plugging in makes a letters question a numbers question.",
    ]])

    # ---------- g163: buttons 800/40 + 400/110 -> 7/8  ==>  eggs 600/25 + 300/50 -> 825/900 = 11/12
    g = 'wp29-g163'
    _rn_q(M, g, 'Farm A packs 600 eggs a day, and 25 of them are cracked. Farm B packs 300 eggs a day, and 50 of them are '
                'cracked. One egg is chosen at random from the eggs both farms pack in one day. What is the probability '
                'that it is not cracked?',
          ['$\\frac1{12}$', '$\\frac{43}{48}$', '$\\frac{11}{12}$', '$\\frac56$'], 3, [
        'Total: $600+300=900$ eggs. Cracked: $25+50=75$.',
        '$P(\\text{cracked})=\\frac{75}{900}=\\frac1{12}$, so $P(\\text{not cracked})=1-\\frac1{12}=\\frac{11}{12}$.',
        'Directly: not cracked $=575+250=825$, and $\\frac{825}{900}=\\frac{11}{12}$.'])
    _rn_video(M, g, [[
        "Probability: what we want, over everything there is.",
        "The egg comes from BOTH farms together. Picture one big basket with all the eggs of both farms.",
        D('Under the question write "total: 600 + 300 = 900"'),
        "Six hundred plus three hundred: nine hundred eggs. That's the bottom.",
        "What do we want? NOT cracked.",
        D('Write "A: 600 − 25 = 575" and "B: 300 − 50 = 250"'),
        "Farm A: five seventy-five not cracked. Farm B: two fifty not cracked.",
        D('Write "575 + 250 = 825", then "825/900 = 11/12"'),
        "Eight twenty-five out of nine hundred. Divide both by seventy-five — eleven twelfths.",
        D('Circle choice 3'),
        "Choice three.",
    ], [
        "Now let's shorten the calculation with the complementary probability.",
        "Same basket, nine hundred eggs. But instead of counting the good ones — count the cracked ones.",
        D('Write "cracked: 25 + 50 = 75", then "75/900 = 1/12"'),
        "Twenty-five plus fifty: seventy-five. Seventy-five out of nine hundred — one twelfth. That's easy.",
        "But one twelfth is the chance of CRACKED. Cracked and not cracked must add up to one.",
        D('Write "1 − 1/12 = 11/12" and circle choice 3'),
        "So not cracked is eleven twelfths. Choice three.",
        "It's like percentages: sometimes the complement is simpler — then subtract it from the whole.",
        "And one twelfth is choice one — the cracked trap. Answer the question they asked.",
    ]])

    # ---------- g164: 5 genres, Mon jazz -> Wed folk 3/16  ==>  6 gym classes, Thu yoga -> Sat boxing 4/5 · 1/5 = 4/25
    g = 'wp29-g164'
    _rn_q(M, g, 'A gym offers six types of classes. Each day, Ben chooses at random one of the five types he did not choose '
                'the day before. On Thursday he chose yoga. What is the probability that he chooses boxing on Saturday?',
          ['$\\frac15$', '$\\frac1{25}$', '$\\frac4{25}$', '$\\frac16$'], 3, [
        'Thursday (yoga) is given, so it has probability 1.',
        'Friday: 5 types are allowed (not yoga). Boxing on Friday would block boxing on Saturday, so Friday must be one '
        'of the other 4: $\\frac45$.',
        "Saturday: 5 types are allowed (all but Friday's type), and boxing is one of them: $\\frac15$.",
        '$\\frac45\\cdot\\frac15=\\frac4{25}$.'])
    _rn_video(M, g, [[
        "Thursday he chose yoga. We want boxing on Saturday.",
        "Do we calculate anything for Thursday? No. It's given — it already happened. Its probability is one.",
        D('Under the question write "Thu: yoga = 1"'),
        "Now Friday. He can't repeat yoga, so he has five options.",
        "But wait — are all five good for us? No! If he picks boxing on Friday, he can't pick boxing on Saturday.",
        D('Write "Fri: 4/5 (not boxing)"'),
        "So four good options out of five: four fifths. Two neighboring days depend on each other.",
        "Saturday. Yoga is back in the pool — it's not the day before anymore. Boxing is allowed.",
        D('Write "Sat: boxing = 1/5"'),
        "Five allowed types, we want boxing: one fifth.",
        D('Write "4/5 · 1/5 = 4/25" and circle choice 3'),
        "Friday AND Saturday — multiply. Four twenty-fifths. Choice three.",
        "What matters here: one stage's choice changes the next stage's options. Take the dependence into account.",
    ]])

    # ---------- g165: 6 red + 1 blue, fifth is blue -> 1/7  ==>  7 blank + 1 prize ticket, sixth is the prize -> 1/8 (review: candies were the Hebrew object)
    g = 'wp29-g165'
    _rn_q(M, g, 'A hat contains 7 blank tickets and 1 prize ticket. The tickets are drawn at random one at a time, '
                'without replacement, until the hat is empty. What is the probability that the sixth ticket drawn is '
                'the prize ticket?',
          ['$\\frac16$', '$\\frac18$', '$\\frac38$', '$\\frac1{56}$'], 2, [
        'The first five tickets must be blank, and then the prize ticket comes: '
        '$\\frac78\\cdot\\frac67\\cdot\\frac56\\cdot\\frac45\\cdot\\frac34\\cdot\\frac13$.',
        'Everything cancels: $\\frac18$.',
        'Faster (symmetry): the prize ticket is equally likely to be in any of the 8 places, so $P(\\text{sixth})=\\frac18$.'])
    _rn_video(M, g, [[
        "For the sixth ticket to be the prize, the first five must all be blank.",
        D('Write "7/8"'),
        "First ticket blank: seven blank out of eight.",
        D('Write "· 6/7 · 5/6 · 4/5 · 3/4"'),
        "Second blank: six out of seven. Third: five out of six. Fourth: four out of five. Fifth: three out of four.",
        "Now three tickets are left — two blank, one prize. We want the prize.",
        D('Write "· 1/3"'),
        "One out of three.",
        "Blank five times AND then the prize — multiply. But before you calculate, look how it cancels.",
        D('Cancel the diagonal pairs and write "= 1/8"'),
        "Seven with seven, six with six, five with five, four with four, three with three. One eighth.",
        D('Circle choice 2'),
        "Choice two.",
    ], [
        "Now the flash — no calculation. Symmetry.",
        "In Denmark there's the \"law of Jante\" — nobody is better than anybody else. Everyone's equal.",
        "Easy question first: what's the chance the FIRST ticket is the prize? One out of eight. Everyone knows that.",
        "Why? One of the eight must come out first — and no ticket has priority over another.",
        "The last one? Same logic. One of them must stay last. All equal — one out of eight.",
        D('Next to the question write "any position: 1/8"'),
        "And the sixth? One of the eight must be sixth. The prize ticket has the same chance as every other ticket.",
        D('Circle choice 2'),
        "One eighth — choice two. First, sixth, last — it doesn't matter.",
        "Symmetry comes back in hard questions: three players, who wins round three? All equal.",
    ]])

    # review 2026-10-06: the questions' own solutionVisual still had the old grids (sum 8; 8 × 8)
    M.q('wp29-g154')['solutionVisual'] = {'type': 'dice', 'sides': 6, 'target': 5}
    M.q('wp29-g156')['solutionVisual'] = {'type': 'dice', 'sides': 5, 'diagonal': True}
    _sync_stem_copies(M, [q for q in M.D['questions'] if q.startswith('wp29-g')])


def rn_practice_questions(M):
    S = _rn_q
    # p01: 12 red 8 blue, one red out -> 11/19  ==>  15 yellow 9 green -> 14/23
    S(M, 'wp29-p01', 'A bag contains 15 yellow tokens and 9 green tokens. A yellow token is removed and not replaced. What is '
                     'the probability that the next token drawn at random is yellow?',
      ['$\\frac58$', '$\\frac{14}{23}$', '$\\frac{15}{23}$', '$\\frac7{12}$'], 2, [
        'After one yellow token is removed: $15-1=14$ yellow tokens and $24-1=23$ tokens in all.',
        '$P(\\text{yellow})=\\frac{14}{23}$.'])
    # p02: 14 tokens, white = black -> orange even (6)  ==>  20 balls, red = green -> yellow even (8)
    S(M, 'wp29-p02', 'A bag has 20 balls colored red, green, or yellow. The probabilities of drawing red and green are equal. '
                     'Which number of yellow balls is possible?',
      ['7', '11', '8', '9'], 3, [
        'Equal probabilities mean equal numbers of red and green balls, say $r$ of each.',
        'Yellow $=20-2r$. This is an even number, so it can be 8 (with $r=6$), but not 7, 9 or 11.'])
    # p04: bulbs 200/20 + 100/25 -> 17/20  ==>  phones 300/20 + 100/12 -> 23/25 (trap: averaging the two rates 68/75)
    S(M, 'wp29-p04', 'Warehouse A holds 300 phones, and 20 of them are faulty. Warehouse B holds 100 phones, and 12 of them are '
                     'faulty. One phone is chosen at random from all the phones in both warehouses. What is the probability '
                     'that it is not faulty?',
      ['$\\frac2{25}$', '$\\frac{68}{75}$', '$\\frac{21}{25}$', '$\\frac{23}{25}$'], 4, [
        'Total: $300+100=400$ phones. Faulty: $20+12=32$.',
        '$P(\\text{faulty})=\\frac{32}{400}=\\frac2{25}$, so $P(\\text{not faulty})=1-\\frac2{25}=\\frac{23}{25}$.'])
    # p05: two 8-sided dice, most likely sum 9  ==>  two boxes of cards 1-10, most likely sum 11 (trap 7)
    S(M, 'wp29-p05', 'Two boxes each contain 10 cards numbered 1 through 10. One card is drawn at random from each box. Which '
                     'of the following sums of the two cards is the most likely?',
      ['11', '7', '3', '19'], 1, [
        'For one card from each of two sets numbered 1 through $n$, the most likely sum is $n+1$. Here $10+1=11$.',
        'Count: a sum of 11 has 10 pairs, from $(1, 10)$ to $(10, 1)$. A sum of 7 has 6 pairs, and sums of 3 and 19 have '
        '2 pairs each.',
        '11 is the most likely. (7 is the trap — it is the top only for two dice.)'])
    # p06: 30 tokens, 1/5 and 1/3 -> 14  ==>  36 tokens, 1/4 and 1/3 -> 15
    S(M, 'wp29-p06', 'A bag has 36 tokens. The probability of red is $\\frac14$, and the probability of white is $\\frac13$. '
                     'All other tokens are black. How many black tokens are there?',
      ['12', '15', '21', '18'], 2, [
        'Red: $\\frac14\\cdot36=9$. White: $\\frac13\\cdot36=12$.', 'Black: $36-9-12=15$.'])
    # p07: 6 of each of 3 colors, 4 out -> 2/14  ==>  7 of each of 4 colors, 3 out -> 4/25
    S(M, 'wp29-p07', 'A bag contains 7 tokens of each of four colors. Three tokens of one color are removed and not returned. '
                     'What is the probability that the next token drawn at random is of that same color?',
      ['$\\frac4{25}$', '$\\frac17$', '$\\frac14$', '$\\frac3{25}$'], 1, [
        'That color has $7-3=4$ tokens left. The bag has $28-3=25$ tokens left.',
        '$P=\\frac4{25}$. It does not matter which color was removed.'])
    # p08: odd, odd, even, odd  ==>  even, even, odd, even (still four tosses -> 1/16)
    S(M, 'wp29-p08', 'A fair six-sided dice is tossed four times. What is the probability that the results are even, even, '
                     'odd, even in that order?',
      ['$\\frac14$', '$\\frac3{16}$', '$\\frac1{16}$', '$\\frac18$'], 3, [
        'Each toss is even or odd with probability $\\frac12$.',
        'Four results in a fixed order (AND): $\\left(\\frac12\\right)^4=\\frac1{16}$.'])
    # p09: 5 colors, 4 draws with replacement all blue -> 1/625  ==>  3 colors, all green -> 1/81
    S(M, 'wp29-p09', 'A bag has the same number of tokens in each of three colors. A token is drawn at random and returned to '
                     'the bag. This is done four times. What is the probability that all four tokens drawn are green?',
      ['$\\frac1{12}$', '$\\frac1{81}$', '$\\frac1{27}$', '$\\frac23$'], 2, [
        'Each draw is green with probability $\\frac13$, and the token is returned each time.',
        '$\\left(\\frac13\\right)^4=\\frac1{81}$.'])
    # p10: A 8r 4b, B 2r 8b -> 13/30  ==>  A 3 white 6 black, B 6 white 2 black -> 13/24 (pour trap 9/17)
    S(M, 'wp29-p10', 'Bag A contains 3 white balls and 6 black balls. Bag B contains 6 white balls and 2 black balls. One of '
                     'the bags is chosen at random (each with probability $\\frac12$), and then one ball is drawn at random '
                     'from it. What is the probability that the ball is white?',
      ['$\\frac12$', '$\\frac{11}{24}$', '$\\frac{13}{24}$', '$\\frac9{17}$'], 3, [
        'Tree: bag A OR bag B, $\\frac12$ each. Multiply along each branch, then add the branches.',
        'A and white: $\\frac12\\cdot\\frac39=\\frac16$. B and white: $\\frac12\\cdot\\frac68=\\frac38$.',
        '$\\frac16+\\frac38=\\frac4{24}+\\frac9{24}=\\frac{13}{24}$. (Pouring both bags together, $\\frac9{17}$, is the trap.)',
        'Door: PATH, not COUNT — the $17$ balls are not equally likely. Each ball in bag A has $\\frac12\\cdot\\frac19=\\frac1{18}$, '
        'and each ball in bag B has $\\frac12\\cdot\\frac18=\\frac1{16}$. That is why pouring the bags together ($\\frac9{17}$) is wrong.'])
    # p11: 4 people, Nina six, others not -> 125/1296  ==>  5 friends, Maya a 1, others not -> 625/7776
    S(M, 'wp29-p11', 'Five friends each toss a fair six-sided dice once. What is the probability that Maya gets a 1 and the '
                     'other four do not?',
      ['$\\frac16$', '$\\frac{625}{7776}$', '$\\frac{3125}{7776}$', '$\\frac1{7776}$'], 2, [
        'Maya gets a 1: $\\frac16$. Each of the other four does not: $\\frac56$ each.',
        'AND: $\\frac16\\cdot\\left(\\frac56\\right)^4=\\frac16\\cdot\\frac{625}{1296}=\\frac{625}{7776}$.'])
    # p12: socks 4, shoes 3 -> 1/4  ==>  cups 6, plates 4 -> 1/6
    S(M, 'wp29-p12', 'A child chooses a cup color at random from 6 colors and, independently, a plate color at random from 4 '
                     'colors. Each of the 4 plate colors is also one of the 6 cup colors. What is the probability that the cup '
                     'and the plate are the same color?',
      ['$\\frac14$', '$\\frac1{24}$', '$\\frac16$', '$\\frac25$'], 3, [
        'There are $6\\cdot4=24$ equally likely cup-and-plate pairs.',
        'Each of the 4 plate colors matches exactly one cup color: 4 matching pairs.',
        '$P=\\frac4{24}=\\frac16$. Faster: choose the plate first (any plate is fine), and then the cup must match it: $\\frac16$.'])
    # p13: 8-sided die until an 8, exactly five rolls  ==>  six-sided die until a 6, exactly four tosses -> 125/1296
    S(M, 'wp29-p13', 'A fair six-sided dice is tossed again and again until a 6 appears. What is the probability that exactly '
                     'four tosses are needed?',
      ['$\\frac{125}{1296}$', '$\\frac14$', '$\\frac1{1296}$', '$\\frac16$'], 1, [
        'The first three tosses are not 6: $\\frac56$ each. The fourth toss is 6: $\\frac16$.',
        '$\\left(\\frac56\\right)^3\\cdot\\frac16=\\frac{125}{1296}$.'])
    # p14: 0-11, <6 add 2 else -2, first 5 / second not 5 -> 5/36  ==>  0-15, <8 add 3 else -3, 7 / not 7 -> 7/64
    S(M, 'wp29-p14', 'A device chooses an integer from 0 through 15 at random (all equally likely). If the number is less than '
                     '8, the device adds 3 to it; otherwise, it subtracts 3 from it. Then it displays the result. The device '
                     'runs twice, independently. What is the probability that the first result is 7 and the second result is not 7?',
      ['$\\frac1{64}$', '$\\frac18$', '$\\frac{49}{64}$', '$\\frac7{64}$'], 4, [
        'The result is 7 for the number 4 ($4+3$) or the number 10 ($10-3$): 2 numbers out of 16, so $P(7)=\\frac2{16}=\\frac18$.',
        'Not 7: $1-\\frac18=\\frac78$.',
        'First 7 AND second not 7: $\\frac18\\cdot\\frac78=\\frac7{64}$.'])
    # p15: 4 badges (3 allowed), blue Mon -> red Wed 2/9  ==>  7 soups (6 allowed), tomato Mon -> lentil Wed 5/36
    S(M, 'wp29-p15', 'A cook knows seven different soups. Each day he cooks at random one of the six soups he did not cook the '
                     'day before. On Monday he cooks tomato soup. What is the probability that he cooks lentil soup on Wednesday?',
      ['$\\frac17$', '$\\frac1{36}$', '$\\frac5{36}$', '$\\frac16$'], 3, [
        'Tree. Tuesday: 6 soups are allowed (not tomato), each with probability $\\frac16$.',
        'If Tuesday is lentil, Wednesday cannot be lentil — this branch gives 0.',
        'If Tuesday is one of the other five soups ($\\frac56$), lentil is one of the 6 allowed soups on Wednesday ($\\frac16$).',
        '$\\frac56\\cdot\\frac16=\\frac5{36}$.'])
    # p16: 8-sided die + 0/1 coin three times -> 5/64  ==>  six-sided die + 0/1 coin three times -> 5/48
    S(M, 'wp29-p16', 'A fair six-sided dice is tossed once. A fair coin with 0 on one side and 1 on the other is tossed three '
                     'times. What is the probability that the sum of the three coin results is greater than the dice result?',
      ['$\\frac1{16}$', '$\\frac5{48}$', '$\\frac1{12}$', '$\\frac18$'], 2, [
        'The coin sum is 0, 1, 2 or 3. Sums 0 and 1 can never be greater than the dice result (it is at least 1).',
        'Coin sum 2: 3 of the 8 coin sequences ($\\frac38$). It is greater only than a dice result of 1 ($\\frac16$): '
        '$\\frac38\\cdot\\frac16=\\frac3{48}$.',
        'Coin sum 3: 1 sequence ($\\frac18$). It is greater than dice results 1 and 2 ($\\frac26$): $\\frac18\\cdot\\frac26=\\frac2{48}$.',
        'Add the separate cases: $\\frac3{48}+\\frac2{48}=\\frac5{48}$.',
        'Door: COUNT — $6$ dice results times $8$ coin sequences: $48$ equally likely outcomes. Good ones: coin sum $2$ '
        '($3$ sequences) with dice $1$: $3$. Coin sum $3$ ($1$ sequence) with dice $1$ or $2$: $2$. $P=\\frac{3+2}{48}=\\frac5{48}$.'])
    # p17: 5 gifts, 2 books, Ada & Ben -> 1/10  ==>  6 prizes, 2 movie tickets, Noa & Eli -> 1/15
    S(M, 'wp29-p17', 'Six different prizes, two of them movie tickets, are given out at random to six friends, one prize each. '
                     'What is the probability that two particular friends, Noa and Eli, both receive movie tickets?',
      ['$\\frac16$', '$\\frac1{15}$', '$\\frac13$', '$\\frac1{30}$'], 2, [
        'Noa gets a ticket: $\\frac26$. Then 1 ticket is left among 5 prizes, so Eli gets it: $\\frac15$.',
        '$\\frac26\\cdot\\frac15=\\frac2{30}=\\frac1{15}$.',
        'Door: SYMMETRY — the two tickets go to 2 of the 6 friends, and all $\\frac{6\\cdot5}2=15$ pairs of friends are '
        'equally likely. Only 1 pair is Noa and Eli: $\\frac1{15}$.'])
    # p18: heads = 2/5 of tails -> 2/7  ==>  tails = 3/4 of heads -> 3/7
    S(M, 'wp29-p18', 'For a biased coin, the probability of tails is $\\frac34$ of the probability of heads. What is the '
                     'probability of tails?',
      ['$\\frac47$', '$\\frac34$', '$\\frac37$', '$\\frac14$'], 3, [
        'Tails and heads are in the ratio $3:4$. Together they make $3+4=7$ parts, and together the probabilities make 1.',
        'Tails: $\\frac37$. Check: heads is $\\frac47$, and $\\frac34\\cdot\\frac47=\\frac37$ ✓.'])
    # p19: coin 2/3, five tosses, total even -> 1/2  ==>  coin 4/7, six tosses, total even -> 1/2
    S(M, 'wp29-p19', 'A fair coin has 4 on one side and 7 on the other. It is tossed six times, and the results are added. '
                     'What is the probability that the total is even?',
      ['$\\frac1{64}$', '$\\frac12$', '$\\frac14$', '$\\frac5{16}$'], 2, [
        'Look at the last toss. Whatever the first five tosses add up to, adding 4 keeps the total even or odd, and adding 7 changes it.',
        'Exactly one of the two faces of the last toss makes the total even: $P=\\frac12$.'])
    # p20: k boxes, cards 1..m, all 2 -> 1/m^k (plug k = 2, m = 3)  ==>  k bags, balls 1..t, all 1 -> 1/t^k (plug k = 3, t = 4)
    S(M, 'wp29-p20', 'There are $k$ bags, and each bag contains balls numbered 1 through $t$ ($t\\ge2$). One ball is drawn at '
                     'random from each bag, independently. What is the probability that every ball drawn is numbered 1?',
      ['$\\frac1{kt}$', '$\\frac kt$', '$\\frac1{k^t}$', '$\\frac1{t^k}$'], 4, [
        'In each bag exactly one ball is numbered 1: probability $\\frac1t$.',
        'All $k$ bags must succeed (AND): $\\left(\\frac1t\\right)^k=\\frac1{t^k}$.',
        'Check with numbers: $k=3$ and $t=4$ give $\\frac14\\cdot\\frac14\\cdot\\frac14=\\frac1{64}$. Only '
        '$\\frac1{t^k}=\\frac1{4^3}=\\frac1{64}$ fits (the others give $\\frac1{12}$, $\\frac34$ and $\\frac1{81}$).'])


def rn_practice(M):
    """Approved clean-up (31 -> 24): the copy p03 (= guided g156); 4 of the 7 English extras (keep p22, p23, p25);
    the September items whose type the Hebrew practice already has (q-09 tree = p10 / p15, q-11 both chosen = p17)."""
    out = ['wp29-p03',    # copy of guided g156 (two dice show the same number)
           'wp29-p21',    # at least one six: the card example; at least one is in q-08 and guided q-02
           'wp29-p24',    # 1-30 divisible by 4 or 6: the example on the guided q-01 video board and the card
           'wp29-p26',    # 40 students, 18 music: the lesson "Possible first" example
           'wp29-p27',    # at least one fails (percent): q-08 and guided q-02 drill at least one
           'q-r26-t29-09',  # tree (rain / walk): Hebrew p10 and p15
           'q-r26-t29-11']  # both on a committee: Hebrew p17
    for qid in out:
        assert M.section_of(qid) == PRACTICE, qid
        M.unplace(qid)
    N = lambda k: 'q-r26-t29-' + k
    M.practice_order(PRACTICE, [
        'wp29-p01', 'wp29-p06', 'wp29-p07', 'wp29-p09', 'wp29-p08', 'wp29-p04', 'wp29-p02', 'wp29-p12', 'wp29-p05',
        'wp29-p18', 'wp29-p22', 'wp29-p25', 'wp29-p23', N('10'), N('08'), 'wp29-p10', 'wp29-p15', 'wp29-p11',
        'wp29-p20', 'wp29-p14', 'wp29-p19', 'wp29-p17', 'wp29-p13', 'wp29-p16'])


def rn_lessons_cards(M):
    # ---- dice-symmetry lesson: no n-sided dice (dice are always 6-sided) -> two boxes of cards numbered 1 to n
    _rn_sub(M, 'wp-159', 2, [
        ("Other dice? For two dice with n faces, the most likely sum is n plus one.",
         "Not dice? One card from each of two boxes, cards numbered 1 to n: the most likely sum is n plus one."),
        ('n faces → top sum n + 1 (6 → 7, 8 → 9)', 'cards 1 to n → top sum n + 1 (1–6 → 7, 1–8 → 9)'),
        ("Six faces: seven. Eight faces: nine — not seven.", "Numbers one to six: seven. One to eight: nine — not seven."),
    ])
    # ---- summary: examples that landed on the Hebrew numbers
    vid = 'r26-t29-summary'
    _rn_sub(M, vid, _rn_slide_no(M, vid, 'Possible first'), [
        ("Four heads in a row — the next toss is still one half.", "Five heads in a row — the next toss is still one half.")])
    n = _rn_slide_no(M, vid, 'AND · OR')
    _rn_sub(M, vid, n, [
        ("Heads and a three on a dice: one half times one sixth — one twelfth.",
         "Tails, and a number above four on a dice: one half times two sixths — one sixth."),
        ('Second try: $\\frac15+\\frac45\\cdot\\frac14=\\frac25$', 'Second try: $\\frac16+\\frac56\\cdot\\frac15=\\frac13$'),
        ('Second try: 1/5 + 4/5 · 1/4 = 2/5', 'Second try: 1/6 + 5/6 · 1/5 = 1/3')])
    n = _rn_slide_no(M, vid, 'Shortcuts')
    _rn_sub(M, vid, n, [
        ('Two dice: symmetric around $7$ · $n$ faces: top sum $n+1$', 'Two dice: symmetric around $7$ · cards $1$ to $n$: top sum $n+1$'),
        ('n faces → n + 1', 'cards 1 to n → n + 1'),
        ("Ten and four are the same distance from seven — same probability. Dice with n faces? The top sum is n plus one.",
         "Eleven and three are the same distance from seven — same probability. Cards numbered one to n, one from each of two boxes? The top sum is n plus one.")])

    # ---- memory card: examples were the old questions' numbers (and two Hebrew ones)
    c = M.card('mem-probability')
    rules = next(t for t in c['tables'] if t['title'] == 'Rules')
    new = {
        '\\(P=\\frac{\\text{wanted}}{\\text{possible}}\\)': '2 red, 5 green: \\(P(\\text{red})=\\frac27\\)',
        'Complement': 'win \\(\\frac38\\) → lose \\(\\frac58\\)',
        'AND': 'tails and a number above 4: \\(\\frac12\\cdot\\frac26=\\frac16\\)',
        'OR, separate cases': 'a 2 or a 5 on a dice: \\(\\frac16+\\frac16=\\frac13\\) · second try: \\(\\frac16+\\frac56\\cdot\\frac15=\\frac13\\)',
        "First pick doesn't matter": 'three coins land the same: \\(1\\cdot\\frac12\\cdot\\frac12=\\frac14\\)',
        'Without replacement': '9 counters → 8 left',
    }
    for row in rules['rows']:
        if row[0] in new: row[2] = new.pop(row[0])
    assert not new, new
    c['tips'] = [t.replace('Two dice with \\(n\\) faces: the most likely sum is \\(n+1\\) (8 faces: 9).',
                           'One card from each of two sets numbered 1 to \\(n\\): the most likely sum is \\(n+1\\) (1 to 8: 9).')
                 for t in c['tips']]
    assert any('1 to 8: 9' in t for t in c['tips'])


def renumber_pass(M):
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_lessons_cards(M)


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last


def spinner_label(M):
    """g156 is about two spinners: its grid says 'Matching sections', not the dice default 'Matching faces'."""
    q = M.q('wp29-g156')
    if isinstance(q.get('solutionVisual'), dict) and q['solutionVisual'].get('type') == 'dice':
        q['solutionVisual']['label'] = 'Matching sections'
    for b in M.D['videos']['solve-wp29-g156']['beats']:
        for it in b.get('items', []):
            v = it.get('v') if isinstance(it, dict) else None
            if isinstance(v, dict) and v.get('type') == 'dice' and v.get('diagonal'):
                v['label'] = 'Matching sections'


_apply_before_spinner_label = apply


def apply(M):
    _apply_before_spinner_label(M)
    spinner_label(M)


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
    # Most topic-29 questions already show their door (COUNT / PATH / SYMMETRY), several via the 2026-10-06
    # practice lines. Q10 comes before the card that names the doors, therefore its line is a self-contained shortcut.
    _sp_line(M, 'wp29-g157', r'Shortcut · Which door? COUNT — every pair of counters is equally likely, therefore $P=$ good pairs $\div$ all pairs. All pairs: $\frac{12\cdot11}{2}=66$. Pairs with two colors: $6\cdot6=36$. $P=\frac{36}{66}=\frac6{11}$.')


_apply_before_spread = apply


def apply(M):
    _apply_before_spread(M)
    spread_methods(M)   # 2026-10-07 methods spread: runs last


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
    _mn_load().method_names(M, 29)   # 2026-10-07 method names: runs last
