"""Topic 29 - Probability. Course review 2026-09 fixes (+ geometric probability, missing from the whole course).
See t29_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q
from math_api import VIS, _word

TOPIC = 29
LEARN, ADV, PRACTICE = 'wp29-learn', 'wp29-advanced', 'wp29-practice'
LESSON_VIDS = ['wp-146', 'wp-147-after', 'wp-151', 'wp-159']
MORE = 'r26-t29-more-rules'
GEO = 'r26-t29-geometric'
LESSON_SB = ['Wanted over possible', 'Between 0 and 1', 'Possible first', 'Certain & impossible', 'And · Or',
             'OR with overlap', 'At least one', 'Exactly one', 'Two stages: a tree', 'Unknown count',
             'Dice symmetry', 'Recap']
# Guided numbers before renumbering: new ones get 18-22. renumber_guided() then numbers them in course order.
LEARN_SB = ['Question %d' % n for n in list(range(1, 12)) + [18, 19, 20, 21, 12]]
ADV_SB = ['Question %d' % n for n in [13, 14, 15, 16, 17, 22]]
GID = ['q-r26-t29-%02d' % k for k in range(1, 15)]

# ------------------------------------------------------------------------------------------------
# Figures (same style as the geometry topics: ink #203344, shaded #d5f1ed / #087f83, DejaVu 20)
# ------------------------------------------------------------------------------------------------
INK, TEAL, FILL = '#203344', '#087f83', '#d5f1ed'


def _svg(label, body, vb='0 0 640 360'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"><title>%s</title>%s</svg>'
            % (vb, label, label, body))


def _t(x, y, s, italic=False, size=20, color=INK):
    return ('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" fill="%s" '
            'font-family="DejaVu Sans,Arial,sans-serif" font-size="%d"%s>%s</text>'
            % (x, y, color, size, ' font-style="italic"' if italic else '', s))


def _poly(pts, shade=False):
    p = ' '.join('%.1f,%.1f' % xy for xy in pts)
    if shade:
        return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (p, FILL, TEAL)
    return '<polygon points="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (p, INK)


def _rect(x0, y0, x1, y1, shade=False):
    return _poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], shade)


def _circle(cx, cy, r, fill='none', stroke=INK):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="2.5"/>' % (cx, cy, r, fill, stroke)


def _dot(cx, cy):
    return '<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (cx, cy, INK)


def _line(x1, y1, x2, y2, color=INK, w=1.8, dash=False):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, color, w, ' stroke-dasharray="6 5"' if dash else ''))


def _crop(svg, vb):
    return re.sub(r'viewBox="[^"]*"', 'viewBox="%s"' % vb, svg, count=1)


# guided question: square 6, circle radius 2 at the center, shaded = square outside the circle
FIG_GUIDED = _svg('A square with a circle at its center; the region outside the circle is shaded',
                  _rect(200, 60, 440, 300, shade=True) + _circle(320, 180, 80, fill='white') +
                  _line(320, 180, 400, 180) + _dot(320, 180) + _t(360, 166, '2') + _t(320, 324, '6'))
# practice: rectangle 8 by 5 with a shaded triangle on the bottom side
FIG_P_TRI = _svg('A rectangle with a shaded triangle whose base is the bottom side',
                 _rect(160, 80, 480, 280) + _poly([(160, 280), (480, 280), (400, 80)], shade=True) +
                 _rect(160, 80, 480, 280) + _t(320, 304, '8') + _t(142, 180, '5'))
# practice: target radius 10 with a small circle of radius 2 at the same center
FIG_P_TARGET = _svg('A round target with a small circle at its center',
                    _circle(320, 180, 150) + _circle(320, 180, 40, fill=FILL, stroke=TEAL) +
                    _line(320, 180, 442.9, 94.0) + _line(320, 180, 280, 180) + _dot(320, 180) +
                    _t(372, 122, '10') + _t(300, 166, '2'))
# practice: large square side 10 with a small shaded square side x in a corner (not to scale)
FIG_P_SQ = _svg('A large square with a small shaded square in its corner',
                _rect(200, 60, 440, 300) + _rect(200, 180, 320, 300, shade=True) + _rect(200, 60, 440, 300) +
                _t(462, 180, '10') + _t(260, 322, 'x', italic=True))
# lesson figures
FIG_S_AREA = _svg('A 10 by 10 square with a shaded 4 by 5 rectangle inside',
                  _rect(200, 60, 440, 300) + _rect(250, 110, 346, 230, shade=True) +
                  _t(320, 324, '10') + _t(462, 180, '10') + _t(298, 248, '4') + _t(234, 170, '5'), vb='170 40 320 300')
FIG_S_CIRC = _svg('A circle that fits exactly inside a square',
                  _rect(200, 60, 440, 300) + _circle(320, 180, 120, fill=FILL, stroke=TEAL) +
                  _line(320, 180, 440, 180) + _dot(320, 180) + _t(380, 164, 'r', italic=True) +
                  _t(320, 324, '2r', italic=True), vb='170 40 320 300')
FIG_S_TRI = _svg('A rectangle with a shaded triangle on its bottom side',
                 _poly([(160, 280), (480, 280), (260, 80)], shade=True) + _rect(160, 80, 480, 280) +
                 _line(260, 80, 260, 280, TEAL, 1.8, dash=True) +
                 _t(320, 304, 'a', italic=True) + _t(142, 180, 'h', italic=True), vb='120 55 400 270')


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
    _geometric_block(M)
    _cards(M)
    _practice(M)
    _american(M)


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
        "Most of what you'll see on the exam is \"and\". \"Or\" questions are rarer — and harder.",
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
        A("'Size check: AND → smaller, OR → bigger' appears",
          T('Size check: AND $\\to$ smaller $\\cdot$ OR $\\to$ bigger', size=42)),
        "A quick size check. AND gives a smaller chance than each event alone. OR gives a bigger chance than each event alone.",
        "Use it to cross out choices fast.",
    ])])

    # wp-159 slide 2: dice symmetry - replace the opposite-faces remark with the 7 - x argument, add n + 1
    M.video('wp-159')['beats'][1]['active'] = 10
    _replace_say(M, 'wp-159', 2,
                 "By the way — opposite faces of a die always add to seven: six and one, five and two, four and three.",
                 None)
    M.edit_lines('wp-159', 2, lambda ls: ls + [
        {'say': "Why? Swap every face x for seven minus x. A one becomes a six, a two becomes a five, a three becomes a four."},
        {'draw': 'Write "(3, 6) → (4, 1): 9 → 5"'},
        {'say': "Then every pair with sum nine becomes a pair with sum five. Fourteen minus nine is five. Same number of pairs."},
        {'say': "Other dice? For two dice with n faces, the most likely sum is n plus one."},
        {'draw': 'Write "n faces → top sum n + 1 (6 → 7, 8 → 9)"'},
        {'say': "Six faces: seven. Eight faces: nine — not seven."},
    ])
    # wp-159 slide 3: recap
    M.set_slide('wp-159', 3, active=11, script=[
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

    # near-duplicates: p03 = Q9 (two 8-sided dice match); p20 = Q14 with new letters
    M.unplace('wp29-p03')
    M.unplace('wp29-p20')


# ------------------------------------------------------------------------------------------------
# 4. New lesson part after Q11 + four guided questions (overlap, at least one, tree, unknown count)
# ------------------------------------------------------------------------------------------------
def _more_rules_block(M):
    v = M.new_video(MORE, TOPIC, 'Probability', LESSON_SB, [
        dict(mode='title', title='At Least One & Trees', script=[
            "Four more tools. These are the harder exam questions.",
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
        dict(mode='concept', active=9, title='Unknown count', script=[
            "Sometimes the number of tokens is the unknown.",
            A("'5 red and some blue, P(red) = 1/3. How many blue?' appears",
              T('5 red and some blue. $P(\\text{red})=\\frac13$. How many blue?', size=44, gap=50)),
            "Call the blue ones x. Careful: the bottom is the TOTAL — five plus x.",
            D('Write "5/(5 + x) = 1/3"'),
            D('Write "15 = 5 + x → x = 10"'),
            "Cross-multiply: fifteen equals five plus x. x is ten.",
            "Check: five red out of fifteen — one third. Yes.",
            A("'Faster: work back from the answers' appears", T('Faster: work back from the answers', size=44)),
            "On the exam, the fastest way is often to work back from the answers. Put each choice into the fraction.",
            "And watch the trap: when tokens are added, the total grows too.",
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
    last = 'solve-' + g

    # ---- guided D: unknown count ----
    g = GID[3]
    M.new_q(g, TOPIC, 'A bag contains 5 red marbles and 7 blue marbles. How many red marbles must be added to the bag so that the probability of drawing a red marble at random is $\\frac34$?',
            ['$4$', '$9$', '$16$', '$21$'], 3, [
        'Add $x$ red marbles. Red: $5+x$. Total: $12+x$ (the total grows too).',
        '$\\frac{5+x}{12+x}=\\frac34$, so $4(5+x)=3(12+x)$: $20+4x=36+3x$ and $x=16$.',
        'Check: $\\frac{21}{28}=\\frac34$ ✓.',
        'Working back from the answers is often faster: 4 gives $\\frac9{16}$, 9 gives $\\frac{14}{21}=\\frac23$, and 16 gives $\\frac{21}{28}=\\frac34$ ✓.'])
    M.place_q(g, LEARN, after=last)
    _solution(M, g, 'learn', ["An unknown number of marbles."], [
        ('Method 1 · Equation', [
            "Add x red marbles. Careful: the red count grows — AND the total grows.",
            D('Write "red: 5 + x · total: 12 + x"'),
            D('Write "(5 + x)/(12 + x) = 3/4"'),
            "Five plus x, over twelve plus x, equals three quarters.",
            D('Write "4(5 + x) = 3(12 + x) → 20 + 4x = 36 + 3x → x = 16"'),
            "Cross-multiply: twenty plus four x equals thirty-six plus three x. x is sixteen.",
            D('Circle choice 3'),
            "Choice three.",
            "The trap: keeping the total at twelve. Three quarters of twelve is nine red — add four. That's choice one.",
        ]),
        ('Method 2 · Work back from the answers', [
            "Faster on the exam: work back from the answers. Put each choice into the fraction.",
            D('Write "4: 9/16 ✗"'),
            "Add four: nine red out of sixteen. Not three quarters.",
            D('Write "9: 14/21 = 2/3 ✗"'),
            "Add nine: fourteen out of twenty-one — two thirds. Still too small.",
            D('Write "16: 21/28 = 3/4 ✓"'),
            "Add sixteen: twenty-one out of twenty-eight. Three quarters. Found it.",
            "Tip: start with a middle choice. Too small? Go up. Too big? Go down.",
        ]),
    ])


# ------------------------------------------------------------------------------------------------
# 5. Geometric probability: short lesson + guided question (end of the advanced section)
# ------------------------------------------------------------------------------------------------
def _geometric_block(M):
    sb = ['Area over area', 'Areas you need', 'Circle in a square', 'Triangle in a rectangle']
    v = M.new_video(GEO, TOPIC, 'Geometric Probability', sb, [
        dict(mode='title', title='Geometric Probability', script=[
            "Geometric probability.",
            "The same idea as always — wanted over possible. But now we measure areas instead of counting.",
        ]),
        dict(mode='concept', active=0, title='Area over area', script=[
            "A point is chosen at random inside a shape. Every spot is equally likely.",
            A("A 10 by 10 square with a shaded 4 by 5 rectangle appears", VIS(FIG_S_AREA, w=560, h=420)),
            "There are endless points, so we can't count them. We compare areas.",
            A("'P = wanted area ÷ total area' appears",
              T('$P=\\dfrac{\\text{wanted area}}{\\text{total area}}$', size=48)),
            "Possible first: the whole square. Ten times ten — a hundred.",
            D('Write "total = 10 · 10 = 100"'),
            "Wanted: the shaded rectangle. Four times five — twenty.",
            D('Write "wanted = 4 · 5 = 20 → 20/100 = 1/5"'),
            "Twenty out of a hundred: one fifth.",
            "Where the rectangle sits doesn't matter. Only its area.",
        ]),
        dict(mode='concept', active=1, title='Areas you need', script=[
            "You need only three areas for these questions.",
            A("'Rectangle: length × width' appears", T('Rectangle: $a\\cdot b$ $\\quad$ (square: $a^2$)', size=48, gap=40)),
            "Rectangle: length times width. A square: side times side.",
            A("'Triangle: base × height ÷ 2' appears", T('Triangle: $\\dfrac{\\text{base}\\cdot\\text{height}}{2}$', size=48, gap=40)),
            "Triangle: base times height, over two.",
            A("'Circle: πr²' appears", T('Circle: $\\pi r^2$', size=48)),
            "Circle: pi r squared. Radius three? Nine pi.",
            "You'll learn them fully in geometry. For now, these three are enough.",
        ]),
        dict(mode='concept', active=2, title='Circle in a square', script=[
            "A circle fits exactly inside a square. Its radius is r.",
            A("A circle inside a square appears", VIS(FIG_S_CIRC, w=560, h=420)),
            "The side of the square is the diameter: two r.",
            D('Write "square: (2r)² = 4r² · circle: πr²"'),
            A("'P = πr² ÷ 4r² = π/4' appears", T('$P=\\dfrac{\\pi r^2}{4r^2}=\\dfrac{\\pi}{4}$', size=48)),
            "Pi r squared over four r squared. The r squared cancels: pi over four.",
            "Yes, a probability can have pi in it. It's just a number — about zero point seven eight. The circle fills most of the square.",
            "And outside the circle? The complement: one minus pi over four.",
        ]),
        dict(mode='concept', active=3, title='Triangle in a rectangle', script=[
            "One more shape that comes up a lot.",
            A("A rectangle with a shaded triangle on its bottom side appears", VIS(FIG_S_TRI, w=600, h=400)),
            "The triangle's base is the bottom side of the rectangle. Its top vertex is on the top side.",
            "So the triangle's height is the rectangle's height.",
            D('Write "triangle = a · h ÷ 2 · rectangle = a · h"'),
            A("'P = 1/2' appears", T('$P=\\dfrac{a\\cdot h\\div2}{a\\cdot h}=\\dfrac12$', size=48)),
            "The triangle is always half of the rectangle. Probability one half — wherever the top vertex is.",
            "Now try a question.",
        ]),
    ], ADV, after='solve-wp29-g165')
    v['hybrid']['num'] = 59

    g = GID[4]
    M.new_q(g, TOPIC, 'The figure shows a square with side 6 and a circle with radius 2. The center of the circle is the center of the square. A point is chosen at random inside the square. What is the probability that the point is in the shaded region?',
            ['$\\frac{\\pi}9$', '$1-\\frac{\\pi}{18}$', '$1-\\frac{\\pi}9$', '$1-\\frac{\\pi}6$'], 3, [
        'Geometric probability: $P=\\frac{\\text{wanted area}}{\\text{total area}}$.',
        'Total: the square, $6^2=36$. Circle: $\\pi\\cdot2^2=4\\pi$. Shaded: $36-4\\pi$.',
        '$P=\\frac{36-4\\pi}{36}=1-\\frac{4\\pi}{36}=1-\\frac{\\pi}9$.',
        'Or with the complement: $P(\\text{circle})=\\frac{4\\pi}{36}=\\frac{\\pi}9$, so $P(\\text{shaded})=1-\\frac{\\pi}9$.'],
            figure=FIG_GUIDED)
    M.place_q(g, ADV, after=GEO)
    fig = {'type': 'geometry', 'svg': _crop(FIG_GUIDED, '180 40 280 300')}
    pre = lambda: [Q(g, fig=fig, figw=0.56, figalign='left')]
    _solution(M, g, 'adv', ["A random point in a square — geometric probability."], [
        ('Area over area', [
            "Possible first: the whole square. Six times six — thirty-six.",
            A("'Total: 6² = 36' appears", T('Total: $6^2=36$', size=38, x=1060, y=300, w=470)),
            "The shaded region is the square minus the circle. Circle: pi times two squared — four pi.",
            A("'Circle: π · 2² = 4π' appears", T('Circle: $\\pi\\cdot2^2=4\\pi$', size=38, x=1060, y=370, w=470)),
            A("'Shaded: 36 − 4π' appears", T('Shaded: $36-4\\pi$', size=38, x=1060, y=440, w=470)),
            "Shaded: thirty-six minus four pi.",
            A("'P = 1 − π/9' appears", T('$P=\\frac{36-4\\pi}{36}=1-\\frac{\\pi}9$', size=40, x=1060, y=520, w=470)),
            "Split the fraction: thirty-six over thirty-six is one. Four pi over thirty-six is pi over nine.",
            D('Circle choice 3'),
            "One minus pi over nine. Choice three.",
        ], pre()),
        ('The traps', [
            "Look at what the other choices did.",
            D('Next to choice 1 write "circle, not shaded"'),
            "Pi over nine is the chance of the CIRCLE. Read what is shaded.",
            D('Next to choice 2 write "π · 2 = 2π ✗"'),
            "One minus pi over eighteen: the radius wasn't squared. The area is pi r SQUARED.",
            D('Next to choice 4 write "4π/24: lengths ✗"'),
            "One minus pi over six compares the circumference, four pi, with the perimeter, twenty-four. Probability compares areas, not lengths.",
        ], pre()),
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
        ['OR, separate cases', 'add', 'a 2 or a 5 on a dice: \\(\\frac16+\\frac16=\\frac13\\)'],
        ['OR, cases overlap', 'first + second − both', '1 to 30, divisible by 4 or 6: \\(\\frac{7+5-2}{30}=\\frac13\\)'],
        ['At least one', '\\(1-P(\\text{none})\\)', 'two dice, at least one six: \\(1-\\frac{25}{36}=\\frac{11}{36}\\)'],
        ['Exactly one / exactly k', 'one order × number of orders', '3 tosses, exactly 1 head: \\(3\\cdot\\frac18=\\frac38\\)'],
        ['Two stages (tree)', 'multiply along a branch, add the branches', '\\(\\frac12\\cdot\\frac34+\\frac12\\cdot\\frac16=\\frac{11}{24}\\)'],
        ['Unknown count', 'the total changes too — or work back from the answers', '\\(\\frac5{5+x}=\\frac13\\Rightarrow x=10\\)'],
        ["First pick doesn't matter", 'that stage has probability 1', 'double: \\(1\\cdot\\frac18\\)'],
        ['Without replacement', 'update the bag before the next draw', '8 counters → 7 left'],
        ['History', "past results don't change a fair coin or dice", 'next toss: always \\(\\frac12\\)'],
    ]
    c['tips'] = [
        'Two sums the same distance from 7 have the same probability (swap each face \\(x\\) for \\(7-x\\)).',
        'Two dice with \\(n\\) faces: the most likely sum is \\(n+1\\) (8 faces: 9).',
        'Size check: AND makes the chance smaller, OR makes it bigger.',
        'Two drawn together = one after the other, without replacement.',
        'A second try only happens after a first miss.',
    ]
    M.new_card('mem-r26-t29-geometric', TOPIC, ADV, {
        'title': 'Geometric probability',
        'intro': 'A point chosen at random: compare areas.',
        'tables': [{'title': 'Area over area', 'head': ['Situation', 'Probability', 'Example'], 'rows': [
            ['Random point in a shape', '$\\frac{\\text{wanted area}}{\\text{total area}}$', '$4\\cdot5$ inside $10\\cdot10$: $\\frac{20}{100}=\\frac15$'],
            ['Circle that fits in a square', '$\\frac{\\pi r^2}{(2r)^2}=\\frac{\\pi}4$', 'outside the circle: $1-\\frac{\\pi}4$'],
            ['Triangle on a side of a rectangle, top vertex on the opposite side', 'always $\\frac12$', 'base 8, height 5: $\\frac{20}{40}$'],
            ['Areas', 'rectangle $a\\cdot b$ · triangle $\\frac{\\text{base}\\cdot\\text{height}}2$ · circle $\\pi r^2$', 'radius 3: $9\\pi$'],
        ]}],
        'tips': ['Compare areas, not lengths: radius 2 inside radius 10 gives $\\frac{4\\pi}{100\\pi}=\\frac1{25}$, not $\\frac2{10}$.',
                 'Shaded outside a shape? Use the complement: $1-P(\\text{shape})$.'],
    }, after='solve-' + GID[4])


# ------------------------------------------------------------------------------------------------
# 7. New practice questions + order easy -> hard
# ------------------------------------------------------------------------------------------------
def _practice(M):
    P = {}
    P[5] = ('A bag contains 6 red balls and some blue balls. The probability of drawing a red ball at random is $\\frac25$. How many blue balls are in the bag?',
            ['$4$', '$15$', '$9$', '$10$'], 3, [
        'Let $x$ be the number of blue balls. Total: $6+x$.',
        '$\\frac6{6+x}=\\frac25$, so $2(6+x)=30$: $6+x=15$ and $x=9$.',
        'Check: $\\frac6{15}=\\frac25$ ✓. (15 is the total, not the number of blue balls.)'], None)
    P[6] = ('A drawer contains 10 socks, some black and the rest white. Two black socks are added to the drawer. Now the probability of drawing a black sock at random is $\\frac12$. How many black socks were in the drawer at first?',
            ['$5$', '$6$', '$4$', '$3$'], 3, [
        'After adding: $b+2$ black socks out of $10+2=12$ socks.',
        '$\\frac{b+2}{12}=\\frac12$, so $b+2=6$ and $b=4$.',
        'Work back from the answers: 4 black at first gives $\\frac{4+2}{12}=\\frac12$ ✓. (6 is the number of black socks after adding; 5 forgets that the total grew.)'], None)
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
    P[11] = ('In the figure, a rectangle measures 8 by 5. The base of the shaded triangle is the bottom side of the rectangle, and its third vertex is on the top side. A point is chosen at random inside the rectangle. What is the probability that the point is in the shaded triangle?',
             ['$\\frac14$', '$\\frac12$', '$\\frac25$', '$\\frac58$'], 2, [
        'Rectangle: $8\\cdot5=40$. Triangle: base 8 and height 5 (the distance between the top and bottom sides): $\\frac{8\\cdot5}2=20$.',
        '$P=\\frac{20}{40}=\\frac12$.',
        'This is always $\\frac12$, wherever the third vertex is on the top side.'], FIG_P_TRI)
    P[12] = ('A round target has a radius of 10 cm. At its center there is a small circle with a radius of 2 cm (the circles have the same center). An arrow hits a random point on the target. What is the probability that the arrow hits the small circle?',
             ['$\\frac15$', '$\\frac1{25}$', '$\\frac1{10}$', '$\\frac4{25}$'], 2, [
        'Target: $\\pi\\cdot10^2=100\\pi$. Small circle: $\\pi\\cdot2^2=4\\pi$.',
        '$P=\\frac{4\\pi}{100\\pi}=\\frac1{25}$. The $\\pi$ cancels.',
        'Trap: $\\frac2{10}=\\frac15$ compares the radii, not the areas.'], FIG_P_TARGET)
    P[13] = ('A square with side 10 contains a smaller square with side $x$, as in the figure. A point is chosen at random inside the large square. The probability that the point is inside the small square is $0.36$. $x=?$',
             ['$3.6$', '$6$', '$0.6$', '$36$'], 2, [
        '$P=\\frac{x^2}{10^2}=\\frac{x^2}{100}=0.36$, so $x^2=36$ and $x=6$.',
        'Check: $\\frac{6^2}{100}=\\frac{36}{100}=0.36$ ✓. (3.6 compares the sides instead of the areas.)'], FIG_P_SQ)
    for k, (stem, ch, cor, ex, fig) in P.items():
        M.new_q(GID[k], TOPIC, stem, ch, cor, ex, figure=fig)
        M.place_q(GID[k], PRACTICE)

    g = GID
    M.practice_order(PRACTICE, [
        'wp29-p01', 'wp29-p06', 'wp29-p07', 'wp29-p09', 'wp29-p08', 'wp29-p04', 'wp29-p02', g[5], g[11], g[12],
        'wp29-p26', 'wp29-p12', 'wp29-p05', 'wp29-p18', g[6],
        'wp29-p21', 'wp29-p27', 'wp29-p22', 'wp29-p25', 'wp29-p24', g[9], g[7], 'wp29-p10', g[8], 'wp29-p15',
        'wp29-p11', 'wp29-p14', 'wp29-p23', g[13], 'wp29-p19',
        'wp29-p17', g[10], 'wp29-p13', 'wp29-p16'])
