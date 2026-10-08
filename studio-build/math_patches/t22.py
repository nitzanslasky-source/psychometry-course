"""Topic 22 - General word problems and ratios. Course review 2026-09 fixes.
See t22_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q

TOPIC = 22
LEARN, ADV, PRAC = 'wp22-learn', 'wp22-advanced', 'wp22-practice'
G_LEARN = 'Word Problem Questions'
G_ADV = 'Advanced General Problems'
CANNOT = 'It cannot be determined from the information given.'


def _word(n):
    import math_api
    return math_api._word(n)


def _solution(M, qid, group, num, intro, slides, after=None):
    """Guided-question solution video in the style of the topic's existing solve-wp22-* videos."""
    n = M.next_question_number(TOPIC)
    beats = [dict(mode='title', title='Question %d' % n, script=['Question %s.' % _word(n)] + intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=0, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, group, ['Question %d' % n], beats, M.section_of(qid),
                    kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = num
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
    """Replace a spoken line that contains `old` (new=None deletes it)."""
    def fn(lines):
        out = []
        for l in lines:
            if 'say' in l and old in l['say']:
                if new is None: continue
                l = dict(l, say=new)
            out.append(l)
        return out
    M.edit_lines(vid, n, fn)


def _insert_after(M, vid, n, marker, new_lines):
    """Insert line dicts after the (first) line containing `marker`."""
    def fn(lines):
        for k, l in enumerate(lines):
            if marker in (l.get('say') or l.get('draw') or ''):
                return lines[:k + 1] + new_lines + lines[k + 1:]
        raise KeyError(marker)
    M.edit_lines(vid, n, fn)


_BRIT = [('Organise', 'Organize'), ('organise', 'organize'), ('colour', 'color'), ('Colour', 'Color'),
         ('Practise', 'Practice'), ('practise', 'practice'), ('centre', 'center'), ('programme', 'program'),
         ('metre', 'meter'), ('litre', 'liter'), ('neighbour', 'neighbor')]


def _us(t):
    for a, b in _BRIT: t = t.replace(a, b)
    return t


def _so(t):
    """'..., so x' / '... — so x' (so = therefore) -> '... . So, x'."""
    def r(mo):
        return '. So, ' + mo.group(2)
    return re.sub(r'(,| —) so (?!that\b|often\b|much\b|many\b|far\b)(\w)', r, t)


def _cleanup_videos(M):
    vids = [f['ref'] for f in M.D['flow'] if f['topic'] == TOPIC and f['type'] == 'video']
    for vid in vids:
        v = M.video(vid)
        v['title'] = _us(v['title']); v['navLabel'] = _us(v.get('navLabel', ''))
        v['hybrid']['title'] = _us(v['hybrid'].get('title', ''))
        v['hybrid']['sidebar'] = [_us(x) for x in v['hybrid'].get('sidebar', [])]
        for b in v['beats']:
            b['title'] = _us(b['title'])
            for key in ('canvas', 'loads'):
                if b.get(key): b[key] = re.sub(r'(?<=\w)−(?=[a-z])', '-', _us(b[key]))
            for it in b['items']:
                if it.get('stem'): it['stem'] = re.sub(r'(?<=\w)−(?=[a-z])', '-', it['stem'])
            if b.get('bigTitle'): b['bigTitle'] = _us(b['bigTitle'])
            for it in b['items']:
                if it.get('t'): it['t'] = _us(it['t'])
            for l in b['lines']:
                if 'say' in l: l['say'] = _so(_us(l['say']))
                if 'draw' in l:
                    d = _us(l['draw'])
                    if 'ratio' not in d:
                        d = re.sub(r'(?<=[\d)x]) : (?=[\d(])', ' ÷ ', d)
                        d = re.sub(r'"\s*:(\d)', r'"÷\1', d)
                    l['draw'] = d
                if 'label' in l: l['label'] = _us(l['label'])
        M.touched_videos.add(vid)
        if v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = M.q(v['questionId'])['stem']


def _fix_sidebars(M):
    """Every solution video of a section lists all the section's guided questions (renumbered later)."""
    for sec in (LEARN, ADV):
        vids = [f['ref'] for f in M.D['flow'] if f['section'] == sec and f['type'] == 'video'
                and M.video(f['ref']).get('kind') == 'solution']
        labels = [M.video(v)['beats'][0]['bigTitle'] for v in vids]
        for v in vids:
            M.set_sidebar(v, labels)


def apply(M):
    S = M.set_q
    # =====================================================================================
    # 1. Equal Ratios lesson (wp-028): no ":" for division, name the method, inverse proportion
    # =====================================================================================
    _draw(M, 'wp-028', 3, '8 × 15 : 6', '8 × 15 ÷ 6')
    _draw(M, 'wp-028', 3, '8 × 5 : 2 = 20', '8 × 5 ÷ 2 = 20')
    _insert_after(M, 'wp-028', 3, 'So we use the triangle value.', [
        {'say': 'You may also hear it called "cross-multiply and divide". It is the same thing.'}])
    M.edit_lines('wp-028', 3, lambda ls: ls + [
        {'say': "Sense check: eight minutes is a bit more than six. The answer must be a bit more than fifteen. Twenty fits."}])
    M.insert_slides('wp-028', 4, [dict(mode='concept', active=3, title='Inverse proportion', script=[
        "One warning before you use the ratio table on everything.",
        A("'6 workers finish a job in 10 days. 4 workers?' appears",
          T('6 workers finish a job in 10 days. How many days for 4 workers?', size=42, gap=60)),
        "Six workers need ten days. How many days for four workers?",
        "Ask first: more or less? Fewer workers — the job takes LONGER.",
        "Four is less than six, but the days go up. The ratio table can't work here.",
        A("'Same job: workers × days stays the same' appears", T('Same job: workers $\\times$ days stays the same', size=44, gap=50)),
        D('Write "6 × 10 = 60 worker-days"'),
        "Six workers for ten days: sixty worker-days of work. That amount doesn't change.",
        D('Write "4 × ? = 60 → ? = 15"'),
        "Four workers still need sixty worker-days. Sixty divided by four: fifteen days.",
        "The trap: the triangle value gives four times ten, divided by six. Six and two thirds days. Fewer days with fewer workers? Impossible.",
        A("'One goes up, the other goes down? Multiply.' appears", T('One goes up, the other goes down? Multiply the pair.', size=42)),
        "The rule: when one amount goes up and the other goes down, the product stays the same.",
        "Workers and days. Speed and time. People and the days a food supply lasts.",
    ])])
    M.set_slide('wp-028', 6, active=4, script=[
        "Let's lock it in.",
        A("'Across or down is whole? Use that multiplier.' appears", T('Across or down is a whole number? Use that multiplier.', size=42)),
        A("'Not whole? Triangle value: diagonal ×, then ÷ the rest.' appears", T('Not whole? Triangle value: diagonal $\\times$, then $\\div$ the rest.', size=42)),
        A("'One goes up, one goes down? The product stays the same.' appears", T('One up, one down? Inverse: the product stays the same.', size=42)),
        A("'First: bigger or smaller?' appears", T('Before you calculate: bigger or smaller?', size=42)),
        D('Circle "Triangle value"'),
        "If it hasn't clicked yet — that's fine. Practice it.",
        "We'll use this all the time — geometry, word problems, algebra. It will become automatic.",
    ])
    M.set_sidebar('wp-028', ['The ratio table', 'Triangle value', 'Cross-multiply', 'Inverse proportion', 'Recap'])

    # =====================================================================================
    # 2. Read, Organize, Calculate (wp-031): teach "or part of" on a real slide
    # =====================================================================================
    v = M.video('wp-031')
    v['title'] = v['navLabel'] = v['hybrid']['title'] = 'Read, Organize, Calculate'
    M.set_slide('wp-031', 1, title='Read, Organize, Calculate')
    M.insert_slides('wp-031', 3, [dict(mode='concept', active=2, title='Or part of: round up', script=[
        A("'50 people. A van carries at most 12. How many vans?' appears",
          T('50 people. A van carries at most 12 people. How many vans?', size=42, gap=60)),
        "Fifty people. Each van takes at most twelve. How many vans do we need?",
        D('Write "50 ÷ 12 = 4, and 2 people are left"'),
        "Four vans hold forty-eight people. Two people are left.",
        "Those two can't stay home. They need one more van.",
        D('Write "→ 5 vans"'),
        "Five vans. Not four — and not four point two.",
        A("'Every hour or part of an hour → round UP' appears", T('"Every hour or part of an hour" $\\to$ round UP', size=44)),
        "Prices work the same way. Every hour or part of an hour: two hours and ten minutes are paid as three hours.",
        D('Write "2 h 10 min → pay for 3 hours"'),
        "Whole vans, whole blocks, whole hours? Round up — even for one extra person or one extra minute.",
    ])])
    M.set_slide('wp-031', 5, active=3)
    M.set_sidebar('wp-031', ['Reading, not algebra', 'Label every cost', 'Or part of', 'Recap'])

    # =====================================================================================
    # 3. Ratios lesson (wp-034): order matters, three-part ratios, changing a ratio
    # =====================================================================================
    _say(M, 'wp-034', 3, "don't worry about being tricked",
         "Always match names to numbers in order. The exam does test this: swap them, and you land on a trap answer.")
    _draw(M, 'wp-034', 3, 'Write ":4" under both 12 and 20', 'Write "÷4" under both 12 and 20')
    _say(M, 'wp-034', 6, 'Tip: give the plain x', None)
    _draw(M, 'wp-034', 6, 'Write "×2 → 3 : 4 → A = 3x, B = 4x"', 'Write "×2 → ratio 3 : 4 → A = 3x, B = 4x"')
    _draw(M, 'wp-034', 7, 'Write "N = 5,  P = 3 → N : P = 5 : 3"', 'Write "N = 5,  P = 3 → ratio N : P = 5 : 3"')
    M.insert_slides('wp-034', 8, [
        dict(mode='concept', active=7, title='Three-part ratios', script=[
            "Now a favorite exam type: two ratios that share one name.",
            A("'A : B = 2 : 3 and B : C = 4 : 5' appears", T('$A:B=2:3$ and $B:C=4:5$', size=54, gap=60)),
            "A to B is two to three. B to C is four to five.",
            "B is in both — but it's three in one ratio and four in the other. The units don't match yet.",
            "Make the shared letter the same number. Three and four can both become twelve.",
            D('Write the ratio "A : B = 2 : 3 = 8 : 12"  (times 4)'),
            "Two to three, times four: eight to twelve.",
            D('Write the ratio "B : C = 4 : 5 = 12 : 15"  (times 3)'),
            "Four to five, times three: twelve to fifteen.",
            D('Write the ratio "A : B : C = 8 : 12 : 15"'),
            "Now B is twelve in both. A to B to C is eight to twelve to fifteen.",
            "From here it's the usual: eight x, twelve x, fifteen x.",
            "The trap: writing two to three to five. The three and the four are not the same B.",
        ]),
        dict(mode='concept', active=8, title='Changing a ratio', script=[
            "Another classic: something is added to ONE part, and the ratio changes.",
            A("'Red : blue = 3 : 5. Add 6 red → 3 : 4' appears",
              T('Red : blue $=3:5$. Add 6 red beads. Now red : blue $=3:4$. How many blue?', size=40, gap=60)),
            "Red to blue is three to five. Six red beads are added. Now it's three to four.",
            "What didn't change? The blue. Nobody touched it.",
            "Make the blue the same number in both ratios. Five and four can both become twenty.",
            D('Write the ratios "before 3 : 5 = 12 : 20" and "after 3 : 4 = 15 : 20"'),
            "Before: twelve to twenty. After: fifteen to twenty.",
            D('Write "15 − 12 = 3 units = 6 beads → 1 unit = 2"'),
            "The red went up by three units. That's the six new beads. One unit is two beads.",
            D('Write "blue = 20 × 2 = 40"'),
            "Blue is twenty units: forty beads.",
            "The rule: find the part that doesn't change. Make it the same number in both ratios, then compare.",
        ]),
    ])
    M.set_slide('wp-034', 11, active=9, script=[
        "Let's lock it in.",
        A("'A ratio is a fraction: expand, reduce, read in order' appears", T('A ratio is a fraction: expand, reduce, read in order', size=40)),
        A("'No amounts from a ratio alone — use 2x, 5x' appears", T('No amounts from a ratio alone — use $2x,\\ 5x$', size=40)),
        A("'The units tell you what divides by what' appears", T('The units tell you what divides by what', size=40)),
        A("'Shared letter? Make it the same number' appears", T('Two ratios, one shared letter? Make it the same number', size=40)),
        A("'One part changes? Fix the part that stays' appears", T('One part changes? Make the unchanged part equal', size=40)),
        D('Underline "No amounts"'),
        "Four questions next — watch the ratio units do all the work.",
    ])
    M.set_sidebar('wp-034', ['What a ratio tells you', 'A ratio is a fraction', 'No amounts!', 'Part of a whole',
                             'Fractions in a ratio', 'Reversed: "costs as"', 'Units and divisibility',
                             'Three-part ratios', 'Changing a ratio', 'Recap'])

    # =====================================================================================
    # 4. Give It to the Little Guy (wp-039): the "plain x to the smaller one" tip lives here now
    # =====================================================================================
    _insert_after(M, 'wp-039', 2, 'Give it to the little guy.', [
        {'draw': 'Write "A is twice B → B = x, A = 2x"'},
        {'say': "Same with letters. A is twice B. Give the plain x to the little guy: B is x, A is two x."},
        {'say': "No fractions, no dividing later."},
    ])

    # =====================================================================================
    # 5. Memory cards
    # =====================================================================================
    c = M.card('mem-ratios')
    c['tables'][0]['rows'].append(['One goes up, the other goes down (workers and days)',
                                   'inverse: the product stays the same, $6\\cdot10=4\\cdot15$'])
    c['tables'][1]['rows'] += [
        ['Two ratios, one shared letter', '$2:3=8:12$ and $4:5=12:15$ $\\to$ $A:B:C=8:12:15$'],
        ['One part changes', 'make the unchanged part equal: $3:5=12:20$, $3:4=15:20$'],
    ]
    c['tables'][1]['rows'][0][1] = '$3:5=\\frac35$'
    c['tips'] = ['Read in order: the first name goes with the first number. The exam tests this.',
                 'Before you calculate: should the answer be bigger or smaller?',
                 'Counting people? The total must divide by the sum of the ratio numbers.']

    c = M.card('mem-general-advanced')
    rows = c['tables'][0]['rows']
    rows[2][2] = 'the ratio $A:S=3:5$, A out of all $=\\frac38$'
    rows[5][2] = 'ratios $3:1$ and $2:1$ → total divides by 4 and by 3'
    rows[6][2] = '4 tasks $=112$ → $\\frac{112}{4}=28$ each'
    rows[7][2] = '$8\\to10$ and $12\\to15$: $\\times1.25$'
    rows += [
        ['Choose numbers', 'letters in the choices', '$x=2,\\ y=3$ → keep the choices that give the same result'],
        ['Assume all the same', 'two kinds, a known total', 'all motorcycles: $30\\cdot2=60$ wheels; each car adds 2'],
        ['One equation, two unknowns', 'asked for a combination', 'only a multiple of the equation can be found'],
    ]
    c['tips'] = ['Plug in the answers? Start with the case that has fewer items — easier to calculate.',
                 'Found x? Check it is what they asked before you circle.',
                 'One thing is twice another? The $\\times2$ goes on the smaller side: $B=x$, $A=2x$.',
                 'Choose numbers: not 0, not 1, and different for each letter.']

    # =====================================================================================
    # 6. Existing solution videos: wording and methods
    # =====================================================================================
    # Q12: the colon is a ratio - say so
    _draw(M, 'solve-wp22-g044', 2, 'Write "A : S = 3 : 5"', 'Write the ratio "A : S = 3 : 5"')
    # Q14 method 2: a real size estimate
    M.set_slide('solve-wp22-g046', 3, script=[
        "Now the psychometric way. We don't even care which pile is which.",
        D('Write "9 + 20 = 29 left"'),
        "Twenty-nine tiles are left.",
        "Each pile lost a quarter or a sixth. All together, she gave away at most a quarter of the tiles — and at least a sixth.",
        D('Write "at most ¼ gone: 29 ≥ ¾ · start → start ≤ 29 · 4/3 ≈ 38.7"'),
        "At most a quarter gone: twenty-nine is at least three quarters of the start. The start is at most about thirty-eight.",
        D('Write "at least ⅙ gone: 29 ≤ ⅚ · start → start ≥ 29 · 6/5 = 34.8"'),
        "At least a sixth gone: twenty-nine is at most five sixths of the start. The start is at least about thirty-five.",
        D('Write "35 ≤ start ≤ 38"'),
        D('Cross out choices 1, 2 and 4'),
        "Fifty-eight, eighty-seven and thirty are all outside. Only thirty-six is between thirty-five and thirty-eight.",
        D('Circle choice 3'),
        "Choice three.",
    ])
    # Q16: lead with "what changed?"
    M.move_slide('solve-wp22-g048', 4, 2)
    M.set_slide('solve-wp22-g048', 2, title='Method 1 · What changed?', script=[
        "Start with the quickest idea.",
        "What's the difference between the two months?",
        D('Write "10 − 6 = 4 tasks"'),
        "Four more tasks.",
        D('Write "320 − 208 = 112"'),
        "And a hundred twelve more credits.",
        D('Write "112 ÷ 4 = 28"'),
        "Four tasks earned a hundred twelve extra. One task: twenty-eight.",
        D('Circle choice 4'),
        "Choice four. The fixed part is the same in both months — it just disappears.",
    ])
    M.set_slide('solve-wp22-g048', 3, title='Method 2 · Two equations')
    M.set_slide('solve-wp22-g048', 4, title='Method 3 · Plug in the answers')
    _say(M, 'solve-wp22-g048', 1, 'Three ways:', "Three ways: first the quick insight, then an equation, then plugging in the answers.")
    # Q18 is no longer the last question of the set
    _say(M, 'solve-wp22-g050', 1, 'Last question of the set.', 'Question eighteen.')

    # =====================================================================================
    # 7. Existing questions: TeX, no ":" for division, numbers in every solution
    # =====================================================================================
    S('wp22-g029', expl=['Across in the ratio table: $\\frac{42}{6}=7$ biscuits per tray.',
                         '15 trays: $15\\cdot7=105$ biscuits.'])
    S('wp22-g030', expl=['Across and down are not whole numbers. Triangle value: $\\frac{14\\cdot12}{8}=\\frac{14\\cdot3}{2}=21$.',
                         'Sense check: 14 minutes is less than twice 8 minutes. The answer must be less than $2\\cdot12=24$ ✓.'])
    S('wp22-g032', expl=['Pastry: $3\\cdot6=18$. Filling: $2\\cdot9=18$. Berries: $4\\cdot\\frac12=2$.',
                         'Ingredient cost: $18+18+2=38$ credits.',
                         'Selling price minus cost: $58-38=20$ credits. (38 is the cost — not what they asked.)'])
    S('wp22-g033', expl=['Company A: 11.5 minutes are paid as 12 minutes ("or part of a minute"): $12\\cdot3=36$ credits.',
                         'Company B: two blocks cover only 10 minutes. 11.5 minutes need 3 blocks: $3\\cdot14=42$ credits.',
                         'Difference: $42-36=6$ credits.'])
    S('wp22-g035', expl=['Boys $=3x$ and all $=8x$. Girls $=8x-3x=5x$.',
                         'Difference: $5x-3x=2x$. It must be even.',
                         'Only 18 is even. Check: $x=9$ gives 27 boys and 45 girls, and $45-27=18$ ✓.'])
    S('wp22-g036', stem='The prices of a scooter and a small car are in the ratio $3:8$. The car costs 15,000 credits more. What is their combined price?',
      expl=['Scooter $=3x$, car $=8x$. Difference: $8x-3x=5x=15{,}000$, therefore $x=3{,}000$.',
            'Combined: $3x+8x=11x=33{,}000$ credits.'])
    S('wp22-g038', stem='A center plans to put the same number of students in each of 6 rooms. One room becomes a storeroom. Each of the 5 remaining rooms must then hold 3 more students. How many students per room were originally planned?',
      expl=['Planned students per room $=x$. The number of students does not change: $6x=5(x+3)$.',
                         '$6x=5x+15$, therefore $x=15$.',
                         'They asked for the planned number: 15. (18 is the new number per room.)'])
    S('wp22-g039', expl=[
        'Leo now $=x$, Iris now $=x+6$. Write a row for each time:',
        '$\\begin{array}{l|c|c} & \\text{Leo} & \\text{Iris} \\\\ \\hline \\text{now} & x & x+6 \\\\ \\text{4 years ago} & x-4 & x+2 \\end{array}$',
        'Four years ago Iris was twice Leo. The $\\times2$ goes on the smaller side: $2(x-4)=x+2$.',
        '$2x-8=x+2$, therefore $x=10$. Check: four years ago they were 6 and 12 ✓.'])
    S('wp22-g040', expl=['Price $=p$. Enough for 5: $5p\\le84$, therefore $p\\le16.8$.',
                         'Not enough for 6: $6p>84$, therefore $p>14$.',
                         'Only 16 is in $14<p\\le16.8$. Check: $5\\cdot16=80\\le84$ ✓ and $6\\cdot16=96>84$ ✓.'])
    S('wp22-g042', expl=['Oranges: 1 credit buys 2, therefore 6 oranges cost 3 credits. Plums: 8 plums cost 1 credit.',
                         'Pears: $\\frac{5\\cdot1}{3.5}=\\frac{10}{7}$ credits (multiply top and bottom by 2, not by 10).',
                         'Total: $3+1+\\frac{10}{7}=\\frac{38}{7}$ credits.'])
    S('wp22-g043', expl=['Round 1: $144\\cdot\\frac56=120$. Round 2 acts on 120: $120\\cdot\\frac56=100$.',
                         'Or write it all first: $144\\cdot\\frac56\\cdot\\frac56=144\\cdot\\frac{25}{36}=4\\cdot25=100$.'])
    S('wp22-g044', expl=['The ratio of apprentices to supervisors is $3:5$.',
                         'Plug in: 5 supervisors and 3 apprentices, 8 people in all.',
                         'Apprentices are $\\frac38$ of all the people. ($\\frac35$ compares them with the supervisors only.)'])
    S('wp22-g045', expl=['Only a fraction is asked. Plug in: 3 market pears and $4\\cdot3=12$ shop pears.',
                         'Rejected: $\\frac14\\cdot12=3$ and $\\frac13\\cdot3=1$. In all, 4 out of 15.',
                         'The fraction rejected is $\\frac4{15}$. Check: it is between $\\frac14$ and $\\frac13$ ✓.'])
    S('wp22-g046', expl=['Red left $=\\frac34$ of the red tiles, a whole number of quarters times 3. It must divide by 3: 9 can be red, 20 cannot.',
                         'Red: $\\frac34R=9$, therefore $R=12$. Blue: $\\frac56B=20$, therefore $B=24$.',
                         'At first: $12+24=36$ tiles.'])
    S('wp22-g047', expl=['B $=x$, A $=3x$. After the move: B has $x+3$, A has $3x-3$.',
                         'B is half of A: $2(x+3)=3x-3$, therefore $2x+6=3x-3$ and $x=9$.',
                         'Total: $x+3x=4x=36$. (The move does not change the total.)'])
    S('wp22-g048', expl=['What changed? $10-6=4$ more tasks and $320-208=112$ more credits.',
                         'Per task: $\\frac{112}{4}=28$ credits. The fixed payment is the same in both months, and it cancels.'])
    S('wp22-g049', expl=['$8\\to10$ and $12\\to15$: both counts are multiplied by $\\frac54$.',
                         'Every part grows by the same factor. The weight grows the same way: $1{,}000\\cdot\\frac54=1{,}250$ g.',
                         'We cannot find one block alone (one equation, two unknowns), but we do not need to.'])
    S('wp22-g050', expl=['The total stays 60. Equal at the end: 30 and 30.',
                         'Go back: Ari had $30+9=39$ and Bea had $30-9=21$.',
                         '$\\frac{39}{21}=\\frac{13}{7}$.'])

    # --- practice ---
    S('wp22-p01', expl=['Three times the small price is $3x$: $\\frac{x^2+32}{x}=3x$.',
                        'A price is positive. Multiply both sides by $x$: $x^2+32=3x^2$.',
                        'Therefore $2x^2=32$, $x^2=16$ and $x=4$ (a price cannot be $-4$).'])
    S('wp22-p02', expl=['Orange $=x$, green $=2x$, blue $=3\\cdot2x=6x$.',
                        'Total: $x+2x+6x=9x$. The total must divide by 9.',
                        'Only $27=9\\cdot3$ works.'])
    S('wp22-p03', expl=['Extra load: $113-80=33$ g.', 'Lost range: $33\\cdot4=132$ km.', 'Range: $540-132=408$ km.'])
    S('wp22-p04', expl=['Total people: $3+4+5=12$.', 'Per person: $\\frac{660}{12}=55$ credits.',
                        'The three-person team pays $3\\cdot55=165$ credits.'])
    S('wp22-p05', stem='Mira has $n$ whole plums. She eats 4, gives half of the remaining plums to a neighbor, and uses 3 whole plums for a dessert. Which of the following could be the value of $n$?',
      expl=['After eating 4, she has $n-4$ plums. Half of them must be a whole number. Therefore $n-4$ is even, and $n$ is even.',
            'Only 12 is even. Check: $12-4=8$. She gives away 4, keeps 4 and uses 3 ✓.'])
    S('wp22-p06', expl=['Notebook $=n$, reference book $=n+18$.',
                        'Four reference books cost the same as six notebooks: $4(n+18)=6n$.',
                        '$4n+72=6n$, therefore $2n=72$ and $n=36$. Reference book: $36+18=54$ credits.'])
    S('wp22-p07', expl=['Before spending 180 credits she had $720+180=900$.',
                        'That is the $\\frac34$ left after the donation: $\\frac34E=900$, therefore $E=900\\cdot\\frac43=1{,}200$.'])
    S('wp22-p08', expl=['Pots: $x\\cdot x=x^2$. Seedlings: $2\\cdot x^2=2x^2$.',
                        'Check with $x=3$: 3 trays of 3 pots is 9 pots and 18 seedlings. $2\\cdot3^2=18$ ✓.'])
    S('wp22-p09', expl=['Plug in: a small battery stores 4 units, a large battery stores 5 units ($\\frac54$ of 4).',
                        '(1) $4\\cdot5+4\\cdot4=36$. (2) $6\\cdot5+2\\cdot4=38$. (3) $7\\cdot5=35$. (4) $9\\cdot4=36$.',
                        'Choice (2), 6 large and 2 small, stores the most: 38 units.'])
    S('wp22-p10', expl=['Pencil $=1$ unit, folder $=3$ units.',
                        'Five sketchpads $=2\\cdot3+6\\cdot1=12$ units. Ten sketchpads $=24$ units.',
                        'Folders: $\\frac{24}{3}=8$.'])
    S('wp22-p11', expl=['$6\\left(\\frac{x}{8}-3\\right)+18=\\frac{6x}{8}-18+18=\\frac34x$.',
                        '$\\frac34x=x$, therefore $\\frac14x=0$ and $x=0$.'])
    S('wp22-p12', expl=['One crest $=8$ sparks $=\\frac25$ crown.',
                        '$\\frac15$ crown $=\\frac82=4$ sparks. One crown $=5\\cdot4=20$ sparks.'])
    S('wp22-p13', expl=['After the first sale, $1-\\frac25=\\frac35$ of the batch is left. One third of it: $\\frac13\\cdot\\frac35=\\frac15$.',
                        'Sold: $\\frac25+\\frac15=\\frac35$ of the batch, for 360 credits.',
                        'Whole batch: $360\\cdot\\frac53=600$ credits.'])
    S('wp22-p14', expl=['Cocoa: $\\frac{18}{120}=0.15$ credits a spoonful. Sugar: $\\frac{12}{300}=0.04$ credits a spoonful.',
                        'Drink: $2\\cdot0.15+3\\cdot0.04=0.30+0.12=0.42$ credits.'])
    S('wp22-p15', stem='For 6 days, a camper gathers 25 berries a day and eats $x$ of them each day. The saved berries then last 18 days at 5 berries a day. What is $x$?',
      expl=['Saved berries: $18\\cdot5=90$.', 'Gathered: $6\\cdot25=150$. Eaten in 6 days: $150-90=60$.',
            '$x=\\frac{60}{6}=10$.'])
    S('wp22-p16', stem='An older dog is 6 years older than a younger dog. The ratio of their ages now is $4:1$. What will the ratio of the older dog\u2019s age to the younger dog\u2019s age be in 2 years?',
      choices=['$3:1$', '$2:1$', '$5:2$', '$4:1$'],
      expl=['Older $=4u$, younger $=u$. The gap: $4u-u=3u=6$, therefore $u=2$.',
            'Now: 8 and 2. In 2 years: 10 and 4.', 'The ratio is $10:4=5:2$.'])
    S('wp22-p17', stem='One meter of silk costs $x$ credits, and one meter of cotton costs $y$ credits. The two prices add up to 17 credits, and silk costs 5 credits more than cotton. A shop sells $x$ meters of silk (as many meters as the price of one meter) and buys $y$ meters of cotton. What is the difference between the money received and the money spent?',
      expl=['Write the two conditions:\n$\\begin{cases} x+y=17 \\\\ x-y=5 \\end{cases}$\nAdd them: $2x=22$, therefore $x=11$ and $y=6$.',
            'Received: $11\\cdot11=121$. Spent: $6\\cdot6=36$.', 'Difference: $121-36=85$ credits.'])
    S('wp22-p18', expl=['Rows equal and columns equal:\n$\\begin{cases} a+b=c+d \\\\ a+c=b+d \\end{cases}$',
                        'Subtract the second equation from the first: $b-c=c-b$, therefore $2b=2c$ and $b=c$.',
                        'Put $b=c$ into $a+b=c+d$: $a=d$.'])
    S('wp22-p19', expl=['Each month $\\frac34$ of what is there stays.',
                        'After three months: $\\frac34\\cdot\\frac34\\cdot\\frac34=\\frac{27}{64}$.',
                        'Not $1-3\\cdot\\frac14=\\frac14$: each quarter is taken from a smaller supply.'])
    S('wp22-p20', expl=['Manual: $\\frac{48{,}000}{40}=1{,}200$ words per diagram. Leaflet: $\\frac{3{,}000}{15}=200$ words per diagram.',
                        '$\\frac{1{,}200}{200}=6$.'])
    S('wp22-p21', expl=['Assume all 42 items are stools: $42\\cdot3=126$.',
                        'Missing: $146-126=20$. Each cart adds $4-3=1$.',
                        'Carts: 20. Check: $22\\cdot3+20\\cdot4=66+80=146$ ✓.'])
    S('wp22-p23', stem='Ada starts work at 9 a.m. on each of five days. On three of those days she takes an unpaid one-hour break. She finishes at the same time every day and works 32 paid hours in total. When does she finish?',
      choices=['4:24 p.m.', '4 p.m.', '3:24 p.m.', '3:36 p.m.'],
      expl=['Time at work: $32+3=35$ hours (32 paid hours and three unpaid breaks).',
            'Each day: $\\frac{35}{5}=7$ hours.', 'Seven hours after 9 a.m. is 4 p.m.'])
    S('wp22-p24', choices=['$9:1$', '$12:1$', '$3:2$', '$6:1$'],
      expl=['The large kite is $L$ long and the small one $S$: $\\frac38L=9\\cdot\\frac14S$.',
            'Multiply by 8: $3L=18S$, therefore $L=6S$.', 'The ratio of the total lengths is $L:S=6:1$.'])
    S('wp22-p26', expl=['Repaid with rice: $\\frac34\\cdot\\frac25=\\frac3{10}$ of the loan.',
                        'Still owed: $\\frac7{10}$ of the loan $=8.40$.',
                        '$\\frac1{10}$ of the loan $=\\frac{8.40}{7}=1.20$. The loan: $10\\cdot1.20=12$ credits.'])
    S('wp22-p27', expl=['Unchanged score: $\\frac35x+24=x$, therefore $\\frac25x=24$ and $x=60$.',
                        'Score goes down: $\\frac35x+24<x$, therefore $24<\\frac25x$ and $x>60$.',
                        'Check: $x=100$ gives $60+24=84<100$ ✓. $x=40$ gives $24+24=48>40$.'])
    S('wp22-p29', expl=['Call the number of brushes $B$. First studio: $\\frac{B}{8}$ each. Second studio: $\\frac{B}{24}$ each.',
                        '$\\frac{B}{8}=3\\cdot\\frac{B}{24}$ is true for every $B$. The last sentence gives no new information.',
                        'Nothing fixes $B$. It cannot be determined.'])
    # p30: two readings gave two keys - say exactly when we count
    S('wp22-p30', stem='There are $n$ players in a room, where $n\\ge5$. Each player starts with $2n$ tokens. The players leave the room one at a time. Just before leaving, a player gives 2 tokens to every other player still in the room. How many tokens does the fifth player to leave have left after giving out his tokens, as he leaves?',
      expl=['The first four players each give the fifth player 2 tokens: $+8$. Before he gives, he has $2n+8$.',
            'When he leaves, $n-5$ other players are still in the room. He gives each of them 2 tokens: $-2(n-5)$.',
            '$2n+8-2(n-5)=2n+8-2n+10=18$.',
            'Check with $n=5$: he starts with 10, gets 8, and gives nothing (nobody is left): 18 ✓.'])
    S('wp22-p31', stem='A school orders blue and white folders in the ratio $5:7$. After 18 blue folders are added, the two colors have equal counts. How many folders were in the original order?',
      expl=['Blue $=5x$, white $=7x$. After adding 18 blue: $5x+18=7x$, therefore $2x=18$ and $x=9$.',
                        'Original order: $12x=12\\cdot9=108$.'])
    S('wp22-p32', expl=['Number of items $=n$: $8+3n=5n$, therefore $2n=8$ and $n=4$.',
                        'Check: $8+3\\cdot4=20=5\\cdot4$ ✓.'])
    S('wp22-p33', expl=['$\\frac45-\\frac35=\\frac15$ of the tank is 28 liters.', 'Capacity: $5\\cdot28=140$ liters.'])
    S('wp22-p34', expl=['Shrub now $=s$, tree now $=2s$. Four years ago: $s-4$ and $2s-4$.',
                        'The tree was 3 times as old. The $\\times3$ goes on the smaller side: $2s-4=3(s-4)$.',
                        '$2s-4=3s-12$, therefore $s=8$. Check: four years ago 4 and 12 ✓.'])
    S('wp22-p35', stem='A blend uses 3 parts juice and 5 parts water. How many liters of water must be added to 24 liters of the blend to make the ratio of juice to water $1:3$?',
      expl=['Juice: $\\frac38\\cdot24=9$ liters. Water: $24-9=15$ liters.',
                        'For the ratio $1:3$, the water must be $3\\cdot9=27$ liters.',
                        'Add $27-15=12$ liters of water.'])
    S('wp22-p36', expl=['Bus ticket $=b$, train ticket $=b+7$.',
                        'Assume all five tickets cost $b$: the bill is $3\\cdot7=21$ lower, $81-21=60$.',
                        '$5b=60$, therefore $b=12$. Check: $3\\cdot19+2\\cdot12=57+24=81$ ✓.'])
    S('wp22-p37', expl=['7 child tickets cost the same as 4 adult tickets.',
                        'Two adults and seven children cost the same as $2+4=6$ adult tickets: $6A=84$.',
                        '$A=\\frac{84}{6}=14$ credits.'])

    # Pass 2: p22, p25 and p28 are original questions and stay (plan: RESTORE); text clean-up only
    S('wp22-p22', expl=['Plug in: 6 residents and $\\frac56\\cdot6=5$ visitors.',
                        'All the people: $6+5=11$.',
                        'Visitors out of all the people: $\\frac5{11}$. (The denominator must include both groups.)'])
    S('wp22-p25', choices=['$11:4$', '$3:2$', '$4:1$', '$13:17$'],
      expl=['After the transfer the total is still 30, and Owen has 4 more than Iris.',
            'Iris $=x$, Owen $=x+4$: $x+(x+4)=30$, therefore $2x=26$ and $x=13$. Iris has 13 and Owen has 17.',
            'Go back: Iris had $13+9=22$ and Owen had $17-9=8$.',
            'The ratio is $22:8=11:4$.'])
    S('wp22-p28', expl=['What is left of the first pile is $\\frac34$ of it, therefore it must divide by 3. 18 divides by 3, 25 does not.',
                        'First pile: $\\frac34F=18$, therefore $F=18\\cdot\\frac43=24$.',
                        'Second pile: $\\frac56G=25$, therefore $G=25\\cdot\\frac65=30$.',
                        'In the box: $24+30=54$ beads.'])

    # =====================================================================================
    # 8. New guided questions in "Learn and try"
    # =====================================================================================
    g = {k: 'q-r26-t22-%02d' % k for k in range(1, 20)}

    # --- inverse proportion (after Q2) ---
    M.new_q(g[2], TOPIC, 'Six workers paint a hall in 10 days. All the workers work at the same rate. How many days would 4 workers need to paint the same hall?',
            ['$6\\frac23$', '12', '15', '8'], 3, [
        'Fewer workers need more days. The answer must be more than 10.',
        'The work stays the same: $6\\cdot10=60$ worker-days.',
        '$4\\cdot d=60$, therefore $d=\\frac{60}{4}=15$ days.',
        'The trap: the ratio table gives $\\frac{4\\cdot10}{6}=6\\frac23$ — fewer days with fewer workers, which is impossible.'])
    M.place_q(g[2], LEARN, after='solve-wp22-g030')
    _solution(M, g[2], G_LEARN, 12, ["Workers and days. Careful — this is not a normal ratio table."], [
        ('More or less?', [
            "Six workers, ten days. Four workers — how many days?",
            "First: more days or fewer? Fewer workers — the job takes longer. More than ten days.",
            D('Cross out choices 1 and 4'),
            "Six and two thirds and eight are less than ten. Out.",
        ]),
        ('Workers × days', [
            "Same job. The workers times the days stays the same.",
            D('Write "6 × 10 = 60 worker-days"'),
            "Six workers for ten days: sixty worker-days.",
            D('Write "4 × d = 60 → d = 15"'),
            "Four workers: sixty divided by four. Fifteen days.",
            D('Circle choice 3'),
            "Choice three.",
            "Six and two thirds is the ratio-table trap. Twelve adds the two missing workers as two days. Neither makes sense.",
        ]),
    ])

    # --- three-part ratio (after Q6) ---
    M.new_q(g[1], TOPIC, 'In a choir, the ratio of sopranos to altos is $2:3$, and the ratio of altos to tenors is $4:5$. There are 30 tenors. How many singers are in the choir?',
            ['35', '60', '70', '84'], 3, [
        'Make the altos the same number in both ratios: $2:3=8:12$ and $4:5=12:15$.',
        'The ratio of sopranos to altos to tenors is $8:12:15$.',
        'Tenors: $15x=30$, therefore $x=2$.',
        'Total: $8x+12x+15x=35x=35\\cdot2=70$.',
        'The trap: the ratio $2:3:5$ is wrong, because the 3 and the 4 are not the same altos. It gives 60.'])
    M.place_q(g[1], LEARN, after='solve-wp22-g036')
    _solution(M, g[1], G_LEARN, 12, ["Two ratios with one shared name. Match it first."], [
        ('Match the shared letter', [
            "Two ratios. The altos are in both.",
            D('Write the ratio "S : A = 2 : 3 = 8 : 12"'),
            "The altos are three in one ratio and four in the other. Make both twelve. Two to three, times four: eight to twelve.",
            D('Write the ratio "A : T = 4 : 5 = 12 : 15"'),
            "Four to five, times three: twelve to fifteen.",
            D('Write the ratio "S : A : T = 8 : 12 : 15"'),
            "Sopranos, altos, tenors: eight, twelve, fifteen.",
            D('Write "15x = 30 → x = 2"'),
            "The tenors are fifteen x. That's thirty. x is two.",
            D('Write "total = 35x = 70"'),
            "The whole choir: eight plus twelve plus fifteen, thirty-five x. Seventy.",
            D('Circle choice 3'),
            "Choice three.",
            "The trap: two to three to five. Then five units are thirty tenors, and the choir is sixty. Choice two — wrong, because the altos don't match.",
        ]),
    ])

    # --- changing a ratio (after the three-part question) ---
    M.new_q(g[3], TOPIC, 'In a club, the ratio of boys to girls is $5:4$. Then 10 boys leave the club, and the ratio of boys to girls becomes $5:6$. How many members did the club have at first?',
            ['44', '27', '54', '45'], 3, [
        'The girls do not change. Make them the same number in both ratios: $5:4=15:12$ and $5:6=10:12$.',
        'The boys went down by $15-10=5$ units. These are the 10 boys who left, therefore 1 unit $=2$.',
        'At first: $15+12=27$ units $=27\\cdot2=54$ members.',
        'With an equation: boys $5x$, girls $4x$. $\\frac{5x-10}{4x}=\\frac56$ gives $30x-60=20x$, therefore $x=6$ and $9x=54$.'])
    M.place_q(g[3], LEARN, after='solve-' + g[1])
    _solution(M, g[3], G_LEARN, 12, ["The ratio changes. Find the part that doesn't."], [
        ('Method 1 · Keep the fixed part', [
            "Ten boys leave. What doesn't change? The girls.",
            "Make the girls the same number in both ratios. Four and six can both become twelve.",
            D('Write the ratios "before 5 : 4 = 15 : 12" and "after 5 : 6 = 10 : 12"'),
            "Before: fifteen to twelve. After: ten to twelve.",
            D('Write "15 − 10 = 5 units = 10 boys → 1 unit = 2"'),
            "The boys dropped by five units. That's the ten boys who left. One unit is two.",
            D('Write "at first: 15 + 12 = 27 units = 54"'),
            "At first: fifteen plus twelve, twenty-seven units. Times two: fifty-four.",
            D('Circle choice 3'),
            "Choice three.",
            "Twenty-seven is the units, not the people. Forty-four is the club AFTER the boys left.",
        ]),
        ('Method 2 · Equation', [
            D('Write "boys 5x, girls 4x"'),
            "Or with x: boys five x, girls four x.",
            D('Write "(5x − 10) / 4x = 5/6"'),
            "After: five x minus ten boys, and still four x girls. Their ratio is five sixths.",
            D('Write "6(5x − 10) = 5 · 4x → 30x − 60 = 20x → x = 6"'),
            "Cross-multiply: thirty x minus sixty equals twenty x. x is six.",
            D('Write "9x = 54"'),
            "The club at first: nine x. Fifty-four. Same answer.",
        ]),
    ])

    # =====================================================================================
    # 9. "Further guided examples": a short shortcuts video first
    # =====================================================================================
    M.new_video('r26-t22-shortcuts', TOPIC, 'Shortcuts Ahead', ['Four shortcuts', 'Three more'], [
        dict(mode='title', title='Shortcuts Ahead', script=[
            "The next nine questions each show a shortcut.",
            "Here they are in one minute. Then you will recognize them when they come.",
        ]),
        dict(mode='concept', active=0, title='Four shortcuts', script=[
            A("'Several stages? Write the whole exercise first' appears", T('Several stages? Write the whole exercise first: $144\\cdot\\frac56\\cdot\\frac56$', size=38)),
            "Several stages? Don't calculate as you go. Write it all first — the numbers usually cancel.",
            A("'Only a fraction asked? Plug in easy numbers' appears", T('Only a fraction is asked? Plug in easy numbers', size=38)),
            "They ask only for a fraction? Choose your own numbers — numbers that every fraction divides.",
            A("'Size estimate' appears", T('Size estimate: cross out choices that are too big or too small', size=38)),
            "Before you calculate, ask: roughly how big? Cross out what can't be.",
            A("'Ratios before and after? The total divides by both' appears", T('Ratios before and after? The total divides by both', size=38)),
            "A ratio before and a ratio after, with the same total? The total divides by both sums of parts.",
        ]),
        dict(mode='concept', active=1, title='Three more', script=[
            A("'Fixed amount + per item? What changed?' appears", T('A fixed amount plus a price per item? Ask: what changed?', size=38)),
            "A fixed amount plus a price per item? Compare the two cases. The fixed part cancels.",
            A("'Same factor on every part? Scale the total' appears", T('Every part grows by the same factor? Scale the total', size=38)),
            "Every count grows by the same factor? The total grows by it too.",
            A("'Simple ending? Start from the end' appears", T('A simple ending? Start from the end', size=38)),
            "The ending is simple — equal, or zero? Start there and go back.",
            "Now the questions. Try each one first — then watch.",
        ]),
    ], ADV, before='wp22-g042')

    # =====================================================================================
    # 10. New lesson video: letters in the choices, assume all the same, one equation two unknowns
    # =====================================================================================
    TOOLS = 'r26-t22-exam-tools'
    M.new_video(TOOLS, TOPIC, 'Three Exam Tools',
                ['Letters in the choices', 'Assume all the same', 'Two unknowns', 'Recap'], [
        dict(mode='title', title='Three Exam Tools', script=[
            "Three more tools the exam loves.",
            "Letters in the answers, a fast trick for two kinds of items — and knowing when you CAN'T find the answer.",
        ]),
        dict(mode='concept', active=0, title='Letters in the choices', script=[
            "Some answers aren't numbers. They're expressions with letters.",
            A("'n rows, k chairs in each, 3 removed from each row' appears",
              T('There are $n$ rows with $k$ chairs in each row. 3 chairs are removed from every row. How many chairs are left?', size=38, gap=50)),
            "You could build the expression. But there's a safer way: choose numbers.",
            D('Write "n = 4, k = 10"'),
            "Pick easy numbers. Not zero, not one — and a different number for each letter. Say four rows, ten chairs.",
            D('Write "4 rows × 7 chairs = 28"'),
            "Three chairs go from each row: seven are left in each. Four rows of seven: twenty-eight.",
            A("'Test every choice: n(k − 3) = 4 · 7 = 28 ✓, nk − 3 = 37 ✗' appears", T('Test every choice: $n(k-3)=4\\cdot7=28$ ✓  $nk-3=37$ ✗', size=40)),
            "Now put four and ten into every choice. Keep only the ones that give twenty-eight.",
            "Two choices give the same result? Choose new numbers and test only those two.",
            "It's the same idea as n equals three in sequences: numbers instead of letters.",
        ]),
        dict(mode='concept', active=1, title='Assume all the same', script=[
            A("'20 tickets: adult 5, child 3, total 76' appears",
              T('20 tickets: adult 5 credits, child 3 credits. Total 76 credits. How many adult tickets?', size=38, gap=50)),
            "Twenty tickets. Adults pay five, children pay three. Together: seventy-six. How many adults?",
            "Pretend they are ALL child tickets.",
            D('Write "20 × 3 = 60"'),
            "Twenty times three: sixty. But the real total is seventy-six.",
            D('Write "76 − 60 = 16 missing"'),
            "Sixteen is missing. Where does it come from? Every adult ticket costs two more than a child ticket.",
            D('Write "16 ÷ 2 = 8 adult tickets"'),
            "Sixteen divided by two: eight adult tickets.",
            D('Write "check: 8 × 5 + 12 × 3 = 40 + 36 = 76 ✓"'),
            "Check: forty plus thirty-six. Seventy-six.",
            "No equations, no x. Assume they're all the same — then fix the difference.",
            "Tip: assume they're all the OTHER kind. Then the count you find is the one they asked for.",
        ]),
        dict(mode='concept', active=2, title='One equation, two unknowns', script=[
            "Last tool: knowing when you CAN'T find the answer.",
            A("'2a + 3p = 13' appears", T('$2a+3p=13$', size=56, gap=40)),
            "One equation, two unknowns. You can't find a and p alone. Many pairs work.",
            D('Write "a = 2, p = 3   or   a = 5, p = 1"'),
            "a two, p three. Or a five, p one. Both fit.",
            A("'Asked for 4a + 6p? = 2(2a + 3p) = 26' appears", T('Asked for $4a+6p$? $=2(2a+3p)=26$ ✓', size=42)),
            "But four a plus six p is exactly double the equation. Twenty-six — that you CAN find.",
            A("'Asked for 3a + 2p? Cannot be determined' appears", T('Asked for $3a+2p$? It cannot be determined.', size=42)),
            "Three a plus two p is not a multiple of it. With the first pair it's twelve, with the second it's seventeen.",
            "The rule: one equation, two unknowns — you can find only a multiple of that equation.",
        ]),
        dict(mode='concept', active=3, title='Recap', script=[
            "Let's lock it in.",
            A("'Letters in the choices? Choose numbers' appears", T('Letters in the choices? Choose numbers, test every choice', size=40)),
            A("'Two kinds, known total? Assume all the same' appears", T('Two kinds, a known total? Assume all the same', size=40)),
            A("'One equation, two unknowns: only a multiple' appears", T('One equation, two unknowns: only a multiple of it', size=40)),
            D('Tick each line'),
            "Two questions next.",
        ]),
    ], ADV, after='solve-wp22-g050')

    M.new_q(g[4], TOPIC, 'A pen costs $x$ credits. A notebook costs 3 credits more than a pen. How much do $y$ pens and $y$ notebooks cost altogether?',
            ['$2xy+3$', '$y(2x+3)$', '$y(x+3)$', '$2y(x+3)$'], 2, [
        'Choose numbers: $x=2$, $y=3$. A pen costs 2 and a notebook costs 5.',
        'Three pens and three notebooks: $3\\cdot2+3\\cdot5=6+15=21$.',
        'Test the choices: (1) $2\\cdot2\\cdot3+3=15$ ✗. (2) $3(4+3)=21$ ✓. (3) $3\\cdot5=15$ ✗. (4) $6\\cdot5=30$ ✗.',
        'Or build it: one pen and one notebook cost $x+(x+3)=2x+3$. Then $y$ of each cost $y(2x+3)$.'])
    M.place_q(g[4], ADV, after=TOOLS)
    _solution(M, g[4], G_ADV, 17, ["Letters in the choices. Choose numbers."], [
        ('Method 1 · Choose numbers', [
            D('Write "x = 2, y = 3"'),
            "x is two, y is three. Not zero, not one, not equal.",
            D('Write "pen 2, notebook 5"'),
            "A pen costs two. A notebook costs three more: five.",
            D('Write "3 × 2 + 3 × 5 = 6 + 15 = 21"'),
            "Three pens: six. Three notebooks: fifteen. Twenty-one.",
            "Now test every choice with x two and y three.",
            D('Next to choice 1 write "12 + 3 = 15 ✗"'),
            "Choice one: twelve plus three, fifteen. Out.",
            D('Next to choice 2 write "3(4 + 3) = 21 ✓"'),
            "Choice two: three times seven. Twenty-one. Keep it.",
            D('Next to choices 3 and 4 write "15 ✗" and "30 ✗"'),
            "Choice three: three times five, fifteen. Choice four: six times five, thirty. Both out.",
            D('Circle choice 2'),
            "Only choice two gives twenty-one. Choice two.",
        ]),
        ('Method 2 · Build it', [
            "Or build the expression, step by step.",
            D('Write "pen x, notebook x + 3"'),
            D('Write "one of each: x + x + 3 = 2x + 3"'),
            "One pen and one notebook: two x plus three.",
            D('Write "y of each: y(2x + 3)"'),
            "We buy y of each — y pairs. y times two x plus three. Choice two.",
            "The trap is choice one: it forgets to multiply the three by y.",
        ]),
    ])

    M.new_q(g[5], TOPIC, 'A parking lot has 30 vehicles: cars and motorcycles. Each car has 4 wheels, and each motorcycle has 2 wheels. There are 96 wheels in total. How many motorcycles are in the parking lot?',
            ['18', '12', '15', '24'], 2, [
        'Assume all 30 are motorcycles: $30\\cdot2=60$ wheels.',
        'Missing: $96-60=36$ wheels. Each car adds $4-2=2$ wheels, therefore there are $\\frac{36}{2}=18$ cars.',
        'Motorcycles: $30-18=12$. Check: $18\\cdot4+12\\cdot2=72+24=96$ ✓.',
        'Faster: assume all are cars ($120$ wheels). $120-96=24$ too many, and each motorcycle removes 2: $\\frac{24}{2}=12$ motorcycles.'])
    M.place_q(g[5], ADV, after='solve-' + g[4])
    _solution(M, g[5], G_ADV, 17, ["Two kinds of vehicles, one total. Assume they're all the same."], [
        ('Method 1 · Assume all the same', [
            "Thirty vehicles, ninety-six wheels. Assume they're all motorcycles.",
            D('Write "30 × 2 = 60 wheels"'),
            "Thirty motorcycles: sixty wheels. We need ninety-six.",
            D('Write "96 − 60 = 36 missing"'),
            "Thirty-six wheels are missing.",
            "Swap one motorcycle for a car: two more wheels.",
            D('Write "36 ÷ 2 = 18 cars"'),
            "Thirty-six divided by two: eighteen cars.",
            D('Write "30 − 18 = 12 motorcycles"'),
            "They asked for motorcycles: thirty minus eighteen. Twelve.",
            D('Circle choice 2'),
            "Choice two. Eighteen is the trap — those are the cars.",
        ]),
        ('Method 2 · Assume the other kind', [
            "Faster: assume the kind they DON'T ask about. All cars.",
            D('Write "30 × 4 = 120 → 120 − 96 = 24 too many"'),
            "Thirty cars: a hundred twenty wheels. Twenty-four too many.",
            D('Write "24 ÷ 2 = 12 motorcycles ✓"'),
            "Each motorcycle has two fewer wheels. Twenty-four divided by two: twelve motorcycles. Straight to the answer.",
        ]),
    ])

    # =====================================================================================
    # 11. New practice questions
    # =====================================================================================
    P = {}
    P[6] = ('The ratio of $A$ to $B$ is $3:4$, and the ratio of $B$ to $C$ is $6:5$. What is the ratio of $A$ to $C$?',
            ['$3:5$', '$9:10$', '$10:9$', '$1:2$'], 2, [
        'Make $B$ the same number in both ratios: $3:4=9:12$ and $6:5=12:10$.',
        'The ratio $A:B:C=9:12:10$, therefore $A:C=9:10$.',
        'The trap: the ratio $3:5$ puts two different $B$ numbers together.'])
    P[7] = ('A bag has red, green and blue marbles. The ratio of red to green marbles is $5:2$. There are 1.5 times as many blue marbles as green marbles, and 12 more red marbles than blue marbles. How many marbles are in the bag?',
            ['36', '48', '60', '90'], 3, [
        'Blue is 1.5 times green: the ratio of green to blue is $2:3$.',
        'Green is 2 in both ratios. The ratio of red to green to blue is $5:2:3$.',
        'Red minus blue: $5x-3x=2x=12$, therefore $x=6$.',
        'Total: $5x+2x+3x=10x=60$.'])
    P[8] = ('A food supply lasts 30 hikers for 12 days. Six more hikers join at the start, and everyone eats the same amount each day. How many days will the supply last?',
            ['14.4', '10', '6', '15'], 2, [
        'More hikers, fewer days. The answer is less than 12.',
        'The supply: $30\\cdot12=360$ hiker-days.',
        '$36\\cdot d=360$, therefore $d=10$ days.'])
    P[9] = ('Eight identical machines can finish a job in 15 hours. All eight start together. After 3 hours, 2 of the machines break down, and the others finish the job. How many hours does the whole job take?',
            ['16', '18', '19', '20'], 3, [
        'The job: $8\\cdot15=120$ machine-hours.',
        'First 3 hours: $8\\cdot3=24$ machine-hours are done. Left: $120-24=96$.',
        'Six machines: $\\frac{96}{6}=16$ more hours. Whole job: $3+16=19$ hours.',
        'The trap 20: $\\frac{120}{6}$ forgets that all eight machines worked for the first 3 hours.'])
    P[10] = ('A club has $m$ members. Each member pays 20 credits. The club uses this money to pay a hall fee of 150 credits. How much money is left per member?',
             ['$20m-150$', '$20-\\frac{150}{m}$', '$\\frac{20-150}{m}$', '$\\frac{20m}{150}$'], 2, [
        'Choose a number: $m=10$. The club collects $10\\cdot20=200$ and pays 150. Left: 50, that is 5 per member.',
        'Test with $m=10$: (1) $50$ ✗. (2) $20-15=5$ ✓. (3) $\\frac{-130}{10}$ ✗. (4) $\\frac{200}{150}$ ✗.',
        'Built directly: $\\frac{20m-150}{m}=20-\\frac{150}{m}$.'])
    P[11] = ('A shop has $n$ boxes with $k$ pencils in each box. It sells 3 full boxes and 5 single pencils from another box. How many pencils are left in the shop?',
             ['$nk-8$', '$(n-3)(k-5)$', '$k(n-3)-5$', '$k(n-8)$'], 3, [
        'Choose numbers: $n=5$, $k=10$. The shop has 50 pencils and sells $3\\cdot10+5=35$. Left: 15.',
        'Test: (1) $50-8=42$ ✗. (2) $2\\cdot5=10$ ✗. (3) $10\\cdot2-5=15$ ✓. (4) $10\\cdot(-3)$ ✗.',
        'Built directly: $nk-3k-5=k(n-3)-5$.'])
    P[12] = ('A test has 25 questions, and Dana answers all of them. A correct answer gives 4 points, and a wrong answer takes away 1 point. Dana scores 70 points. How many of her answers are correct?',
             ['6', '18', '19', '21'], 3, [
        'Assume all 25 are correct: $25\\cdot4=100$ points.',
        'Each wrong answer changes $+4$ into $-1$: it costs 5 points. Lost: $100-70=30$, therefore $\\frac{30}{5}=6$ wrong answers.',
        'Correct: $25-6=19$. Check: $19\\cdot4-6=76-6=70$ ✓.'])
    P[13] = ('In a club, the ratio of boys to girls is $4:3$. Then 6 more girls join, and the numbers of boys and girls become equal. How many members does the club have now?',
             ['42', '48', '24', '54'], 2, [
        'The boys do not change. The ratio is $4:3$ before and $4:4$ after.',
        'The girls went up by 1 unit. That is the 6 new girls, therefore 1 unit $=6$.',
        'Now: $4+4=8$ units $=48$ members (24 boys and 24 girls).'])
    P[14] = ('130 students and 9 teachers go on a trip. A bus carries at most 45 people and costs 800 credits to rent. What is the lowest possible cost of the buses?',
             ['2,400', '3,200', '3,600', '4,000'], 2, [
        'People: $130+9=139$.',
        '$3\\cdot45=135<139$. Three buses are not enough, therefore they need 4 buses.',
        'Cost: $4\\cdot800=3{,}200$ credits.'])
    P[15] = ('A parking garage charges 12 credits for the first hour or part of it, and 8 credits for every additional half-hour or part of it. How much does it cost to park for 2 hours and 50 minutes?',
             ['36', '40', '44', '48'], 3, [
        'First hour: 12 credits.',
        'Time left: 1 hour 50 minutes $=110$ minutes. $\\frac{110}{30}=3\\frac23$, and part of a half-hour is paid in full: 4 half-hours.',
        'Total: $12+4\\cdot8=12+32=44$ credits.'])
    P[16] = ('3 notebooks and 2 pens cost 17 credits together. All notebooks cost the same, and all pens cost the same. How much do 2 notebooks and 3 pens cost?',
             ['17', '15', '12', CANNOT], 4, [
        'One equation, two unknowns: $3n+2p=17$.',
        '$n=3$, $p=4$ fits, and then $2n+3p=18$. $n=5$, $p=1$ also fits, and then $2n+3p=13$.',
        '$2n+3p$ is not a multiple of $3n+2p$. It cannot be determined.'])
    P[17] = ('4 notebooks and 6 pens cost 50 credits together. All notebooks cost the same, and all pens cost the same. How much do 6 notebooks and 9 pens cost?',
             ['60', '75', '100', CANNOT], 2, [
        'One equation: $4n+6p=50$. Divide by 2: $2n+3p=25$.',
        '$6n+9p=3(2n+3p)=3\\cdot25=75$ credits.',
        'We cannot find $n$ or $p$ alone, but this combination is a multiple of the equation.'])
    P[18] = ('In a box, the ratio of red balls to blue balls is $5:6$. Then 4 red balls are taken out and 4 blue balls are put in. Now the ratio of red balls to blue balls is $1:2$. How many red balls were in the box at first?',
             ['11', '12', '15', '18'], 3, [
        'Red $=5x$, blue $=6x$. After the change: red $5x-4$, blue $6x+4$.',
        'Blue is twice red: $2(5x-4)=6x+4$, therefore $10x-8=6x+4$ and $x=3$.',
        'Red at first: $5\\cdot3=15$. Check: $15-4=11$ and $18+4=22$, and the ratio $11:22=1:2$ ✓.'])
    P[19] = ('Three partners share a profit of 5,500 credits in the ratio of their investments. A invested twice as much as B, and B invested 1.5 times as much as C. How much does C get?',
             ['500', '1,000', '1,500', '3,000'], 2, [
        'Give the plain unit to the smallest: C $=2$ units, B $=1.5\\cdot2=3$ units, A $=2\\cdot3=6$ units.',
        'The ratio of A to B to C is $6:3:2$, in all 11 units. One unit: $\\frac{5{,}500}{11}=500$.',
        'C gets $2\\cdot500=1{,}000$ credits.'])
    for k, (stem, ch, cor, ex) in sorted(P.items()):
        M.new_q(g[k], TOPIC, stem, ch, cor, ex)
        M.place_q(g[k], PRAC)

    # practice: easy -> hard
    p = lambda n: 'wp22-p%02d' % n
    M.practice_order(PRAC, [
        p(3), p(4), p(8), p(12), p(33), p(32), p(7), p(14), p(37), g[14], g[6], g[8], p(6), p(2), p(10),
        p(22), p(16), p(31), g[13], p(25), p(15), p(20), p(21), g[12], p(36), g[10], p(19), p(13), p(35), g[17], p(1),
        p(5), p(9), p(11), p(23), p(34), p(17), g[16], p(29), g[19], g[7], g[9], g[11], g[15], g[18],
        p(26), p(28), p(24), p(27), p(18), p(30)])

    # =====================================================================================
    # 12. Whole-topic text pass, sidebars
    # =====================================================================================
    give_gap(M)
    _cleanup_videos(M)
    _fix_sidebars(M)
    summary(M)
    cut_repeats(M)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)


# =====================================================================================
# Pass 2: summary lesson right before the practice
# =====================================================================================
def summary(M):
    sb = ['Three stages', 'Words to math', 'Equal ratios', 'Inverse proportion', 'Ratios: use x',
          'The part that stays', 'Build the equation', 'Ranges and rounding', 'Exam shortcuts', 'Before you practice']
    C = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of word problems and ratios.",
            "Everything important, one idea at a time."]),
        C(0, [
            A("'Translate → solve → answer what they asked' appears",
              T('Translate $\\to$ solve $\\to$ answer what they asked', size=44)),
            "Every word problem has three stages: translate the words, solve, and answer what they ASKED.",
            A("'x = 7, asked for 2x → 14' appears", T('$x=7$, but they ask for $2x$ $\\to$ $14$', size=46)),
            "x is seven, and they ask for twice the number? The answer is fourteen.",
            "Tip: let x be the thing they ask for."]),
        C(1, [
            A("'8 more: A = B + 8' appears", T('$A$ is $8$ more than $B$: $\\ A=B+8$', size=44)),
            "More and less: plus and minus.",
            A("'4 times: A = 4B' appears", T('$A$ is $4$ times $B$: $\\ A=4B$', size=44)),
            "Four times is not four more.",
            A("'One fifth less than n: 4/5 n · \"of\" = ×' appears",
              T('One fifth less than $n$: $\\ \\frac45n$ ("of" means $\\times$)', size=44)),
            "Of means times. A fifth less leaves four fifths.",
            A("'4 mugs cost the same as 3 plates: 4M = 3P' appears",
              T('$4$ mugs cost the same as $3$ plates: $4M=3P$', size=42)),
            "Is, makes up, costs the same as: all equals signs. Translate one phrase at a time."]),
        C(2, [
            A("'Across or down is whole? Use that multiplier' appears",
              T('Across or down is a whole number? Use that multiplier', size=40)),
            "Put the data in a ratio table. Across or down is a whole number? Use that multiplier.",
            A("'Triangle value: 10 · 9 ÷ 6 = 15' appears",
              T('Not whole? Triangle value: $\\frac{10\\cdot9}{6}=15$', size=46)),
            "Not whole? The triangle value: multiply along the diagonal, then divide by what's left.",
            "Or cross-multiply — the same answer.",
            "And a sense check first: should the answer be bigger or smaller?"]),
        C(3, [
            A("'Workers × days stays the same' appears", T('Same job: workers $\\times$ days stays the same', size=44)),
            "One goes up and the other goes down? That's inverse. The product stays the same.",
            A("'8 · 9 = 72 = 6 · 12' appears", T('$8\\cdot9=72=6\\cdot12$', size=54)),
            "Eight workers, nine days: seventy-two worker-days. Six workers need twelve days.",
            "The ratio table here gives fewer days with fewer workers. Impossible — so ask: more or less?"]),
        C(4, [
            A("'Ratio 4 : 7 → 4x and 7x' appears", T('Ratio $4:7$ $\\to$ $4x$ and $7x$', size=48)),
            "A ratio is a fraction. Read it in order: the first name goes with the first number.",
            "A ratio alone gives no amounts. Write four x and seven x.",
            A("'5/9 of all → part 5x, all 9x' appears", T('$\\frac59$ of all $\\to$ part $5x$, all $9x$', size=46)),
            "Five ninths of all? The part is five x, and all of them is nine x.",
            A("'4M = 3P → ratio M : P = 3 : 4' appears", T('$4M=3P$ $\\to$ ratio $M:P=3:4$ (reversed)', size=44)),
            "Costs the same as? Reversed: mug to plate is three to four.",
            "Counting people? x is a whole number — the total divides by the sum of the ratio numbers."]),
        C(5, [
            A("'Ratio A : B = 3 : 2 = 15 : 10, B : C = 5 : 7 = 10 : 14' appears",
              T('Ratios $A:B=3:2=15:10$ and $B:C=5:7=10:14$', size=42)),
            "Two ratios share a letter? Make it the same number in both. A to B to C: fifteen, ten, fourteen.",
            "Not three to two to seven — the two and the five are not the same B.",
            A("'One part changes? Make the unchanged part equal' appears",
              T('One part changes? Make the unchanged part equal', size=42)),
            "Something is added to one part? Find the part nobody touched. Make it equal in both ratios, then compare the units."]),
        C(6, [
            A("'Changes? Write the new amounts first' appears", T('Changes? Write the new amounts first', size=42)),
            "Something changes? Write the new amounts before you write the equation. Moved between groups? The total stays.",
            A("'Twice? The ×2 goes on the smaller side: B = x, A = 2x' appears",
              T('Twice? The $\\times2$ goes on the smaller side: $B=x$, $A=2x$', size=40)),
            "One is twice the other? Give it to the little guy.",
            A("'Ages: the gap stays, the ratio changes' appears", T('Ages: the gap stays, the ratio changes', size=42)),
            "Ages: a row for every time in the story. Or test the answers: run each choice through the story."]),
        C(7, [
            A("'Enough for 3, not for 4: 3B ≤ 36 and 4B > 36' appears",
              T('Enough for $3$, not for $4$: $\\ 3B\\le36$ and $4B>36$', size=42)),
            "Enough — but not enough? Two inequalities. The answer is a range: more than nine, at most twelve.",
            A("'\"Or part of\" → round UP' appears", T('"Or part of" $\\to$ round UP: $40$ people, boats of $9$ $\\to$ $5$ boats', size=40)),
            "Or part of? Round up. Four people left over still need a boat.",
            "And label every number: price per kilogram is not per gram, and a fixed fee is paid once."]),
        C(8, [
            A("'Letters in the choices? Choose numbers' appears",
              T('Letters in the choices? Choose numbers — not $0$, not $1$', size=40)),
            "Letters in the answers? Choose numbers and test every choice.",
            A("'Two kinds, a known total? Assume all the same' appears", T('Two kinds, a known total? Assume all the same', size=40)),
            "Two kinds with a known total? Pretend they're all one kind, then fix the difference.",
            A("'One equation, two unknowns: only a multiple of it' appears", T('One equation, two unknowns: only a multiple of it', size=40)),
            "One equation, two unknowns? You can find only a multiple of it. Anything else cannot be determined.",
            A("'Several stages? Write it all first · What changed?' appears",
              T('Several stages? Write it all first · A fixed part? What changed?', size=38)),
            "Several stages? Write the whole exercise first. A fixed amount plus a price per item? Compare the two cases."]),
        C(9, [
            "Before you start, always ask yourself:",
            A("'Check 1' appears", T('What exactly did they ask: $x$, $2x$ or $x-1$?', size=40)),
            A("'Check 2' appears", T('Bigger or smaller? Direct or inverse?', size=40)),
            A("'Check 3' appears", T('Which part stays the same?', size=40)),
            A("'Check 4' appears", T('Where does the $\\times2$ go? On the smaller side.', size=40)),
            A("'Check 5' appears", T('Can it really be found — or only a multiple?', size=40)),
            "And the traps: a ratio read in the wrong order, the ratio table on workers and days, and units instead of people.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t22-summary', TOPIC, 'Summary: Word Problems and Ratios', sb, slides, ADV, after=last)


# =====================================================================================
# 2026-10-01 elite comparison: one person GIVES k to another -> the gap changes by 2k; equal -> give half the gap.
# Real exam: 2024_spring_q2_03, 2020_spring_q2_07 (their distractors use "the gap changes by k" and miss the flip).
# =====================================================================================
GIVE_TABLE = {'k': 'vis', 'v': {'type': 'table', 'headers': ['', 'Dan', 'Noa', 'Gap'],
                                'rows': [['Start', '30', '20', 'Dan +10'],
                                         ['Dan gives 3', '27', '23', 'Dan +4'],
                                         ['Dan gives 5', '25', '25', '0'],
                                         ['Dan gives 7', '23', '27', 'Noa +4']]},
              'w': 900, 'h': 250, 'gap': 40}


def give_gap(M):
    # "Build the Equation" (wp-037): 1 title, 2 equations everywhere, 3 choose x, 4 before and after, 5 recap
    M.insert_slides('wp-037', 4, [dict(mode='concept', title='Giving: the gap changes twice', script=[
        "One more kind of change: one person GIVES something to another.",
        "Dan has thirty cards. Noa has twenty. Dan is ten ahead.",
        A('The table appears: start 30 and 20; Dan gives 3, 5, 7', GIVE_TABLE),
        "Dan gives Noa three cards. Dan loses three — and Noa gains three.",
        "So the gap shrinks by three, twice. Ten minus six: four.",
        A("'A gives k to B → the gap changes by 2k' appears",
          T('$A$ gives $k$ to $B$ $\\to$ the gap changes by $2k$', size=44, gap=30)),
        "That's the rule: give k, and the gap changes by two k. Not by k — that's the trap.",
        A("'To make them equal: give half the gap' appears", T('To make them equal: give half the gap', size=44)),
        "To make them equal? Give half the gap. Half of ten is five: twenty-five and twenty-five.",
        D('Circle "Noa +4" in the last row'),
        "Give more than half — seven — and Noa is now ahead by four. The gap goes past zero and turns around.",
        "So ask: who is ahead now?",
    ])])
    M.set_slide('wp-037', 6, script=[
        A("'Build it piece by piece — don't run ahead' appears", T("Build it piece by piece — don't run ahead", size=44)),
        A("'Changes? Write the new amounts first' appears", T('Changes? Write the new amounts first', size=44)),
        A("'Gives k → the gap changes by 2k' appears", T('Gives $k$ $\\to$ the gap changes by $2k$', size=44)),
        "Next: a question where a room disappears. Watch the equation build itself.",
    ])
    M.set_sidebar('wp-037', ['Equations everywhere', 'Choose x wisely', 'Before and after', 'Giving changes the gap',
                             'Recap'])
    k = 0
    for b in M.video('wp-037')['beats']:
        if b['mode'] == 'concept': b['active'] = k; k += 1

    # new guided question, right after the rooms question
    qid = 'q-r26-t22-20'
    M.new_q(qid, TOPIC, 'Shelf A has 26 more books than shelf B. Some books are moved from shelf A to shelf B. After the '
                        'move, shelf B has 6 more books than shelf A. How many books were moved?',
            ['10', '13', '16', '32'], 3, [
        'Every book that is moved changes the gap by 2: A loses it and B gains it.',
        'The gap goes from "A ahead by 26" through 0 to "B ahead by 6": it changes by $26+6=32$.',
        'Books moved: $\\frac{32}{2}=16$.',
        'Check: B $=x$, A $=x+26$. After the move: A $=x+10$ and B $=x+16$. B has 6 more ✓.',
        'Traps: 32 forgets that the gap changes twice; 13 only makes them equal; 10 forgets that the gap turns around.'])
    M.place_q(qid, LEARN, after='solve-wp22-g038')
    _solution(M, qid, G_LEARN, 12, ["Books move from one shelf to the other. Watch the gap."], [
        ('Method 1 · The gap', [
            "Each book that moves: A loses one, B gains one. The gap changes by two.",
            D('Draw a number line: "A +26" on the right, "0" in the middle, "B +6" on the left'),
            "At the start, A is twenty-six ahead. At the end, B is six ahead.",
            "The gap goes down to zero, then turns around and grows to six.",
            D('Write "26 + 6 = 32"'),
            "In all, the gap changes by twenty-six plus six: thirty-two.",
            D('Write "32 ÷ 2 = 16 books"'),
            "Each book changes it by two. Thirty-two divided by two: sixteen books.",
            D('Circle choice 3'),
            "Choice three.",
        ]),
        ('Method 2 · Before and after', [
            "Or build it with a before-and-after table. Give the plain x to the little guy: B.",
            D('Write "before: B = x, A = x + 26"'),
            D('Write "after (move k): A = x + 26 − k, B = x + k"'),
            "Move k books. A loses k, B gains k.",
            D('Write "(x + k) − (x + 26 − k) = 6  →  2k − 26 = 6  →  k = 16"'),
            "B is six more than A. The x cancels: two k minus twenty-six is six. k is sixteen.",
            D('Next to choices 4, 2 and 1 write "gap by k", "equal", "no turn"'),
            "The traps: thirty-two changes the gap by k, not two k. Thirteen only makes them equal. Ten forgets that B ends up ahead.",
        ]),
    ])

    # wp22-p25 (already restored in the practice): add the gap method to its solution
    M.set_q('wp22-p25', expl=[
        'The gap: every counter Iris gives changes the gap by 2. She gives 9, therefore the gap moves $2\\cdot9=18$ toward Owen.',
        'After the transfer Owen is 4 ahead. Before it, Iris was $18-4=14$ ahead.',
        'Together 30, Iris 14 more: Iris $\\frac{30+14}{2}=22$ and Owen $30-22=8$.',
        'With an equation: after the transfer Iris $=x$ and Owen $=x+4$. $2x+4=30$, $x=13$: 13 and 17. Before: $13+9=22$ '
        'and $17-9=8$.',
        'The ratio is $22:8=11:4$.'])


# =====================================================================================
# 2026-10-05 cut repeats: each lesson back to a short intro (Hebrew style); every idea a
# question video right after it already teaches is cut from the lesson; ideas no question
# teaches stay, or move as one line + board item into the question video that uses them.
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


def _set_say(M, vid, n, old, new):
    """Replace the whole spoken line containing `old`."""
    def fn(lines):
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = new
                return lines
        raise AssertionError('%s #%d: not found: %s' % (vid, n, old))
    M.edit_lines(vid, n, fn)


def _keep_slides(M, vid, keep, sidebar):
    """Keep only the slides `keep` (1-based); set the sidebar; renumber 'active'."""
    v = M.video(vid)
    M.remove_slides(vid, [k for k in range(1, len(v['beats']) + 1) if k not in keep])
    a = 0
    for b in v['beats']:
        if b.get('mode') in ('concept', 'question'):
            b['active'] = a; a += 1
    M.set_sidebar(vid, sidebar)


def cut_repeats(M):
    # ---- Equal Ratios: title only (Hebrew: "easiest to just see an example") -------------
    vid = 'wp-028'
    _keep_slides(M, vid, [1], [])
    _set_say(M, vid, 1, "Let's learn it on an easy example.", "The easiest way to learn it: on the questions.")
    # "The ratio table" (same 6 / 42 / 15 numbers) -> Q1 trays
    _say(M, 'solve-wp22-g029', 1, 'Equal ratios — straight from the lesson.', 'Equal ratios — we learn it on this question.')
    _add_line(M, 'solve-wp22-g029', 2, 'Draw an arrow from 6 to 42',
              "Put the data in a ratio table: trays in one column, biscuits in the other. Six is to forty-two as fifteen is to the missing number.")
    _set_say(M, 'solve-wp22-g029', 3, 'The triangle value gives the same thing',
             "The triangle value gives the same thing: multiply along the diagonal, fifteen times forty-two, and divide by what's left, six.")
    # "Triangle value" + "Cross-multiply" -> Q2 (exercises); keep the other name
    _set_say(M, 'solve-wp22-g030', 2, 'So: triangle value.',
             'So: the triangle value — also called "cross-multiply and divide".')
    # "Inverse proportion" -> Q3 (workers); move the general rule there
    _add_line(M, 'solve-q-r26-t22-02', 3, None,
              "The rule: one goes up, the other goes down — the product stays the same. Workers and days, speed and time.",
              T('One up, one down? The product stays the same', 36),
              "'One up, one down? The product stays the same' appears")

    # ---- Read, Organize, Calculate: keep title + "Reading, not algebra" (Hebrew intro) --
    vid = 'wp-031'
    _keep_slides(M, vid, [1, 2], ['Reading, not algebra'])
    _add_line(M, vid, 2, None, "Two questions next. They check that you notice every detail.")
    # "Label every cost" -> Q4 tart (selling price minus cost); move the label rule there
    _add_line(M, 'solve-wp22-g032', 2, 'Pastry: three hundred grams',
              "Label every number: a price per hundred grams is not a price per gram, and a fixed fee is paid once.",
              T('Label every number · per 100 g ≠ per g · a fixed fee is paid once', 34),
              "'Label every number · per 100 g ≠ per g · a fixed fee is paid once' appears")
    # "Or part of: round up" -> Q5 hire (or part of a minute / block); move the vans example
    _add_line(M, 'solve-wp22-g033', 2, None,
              "Same with people: fifty people, vans of twelve. Four vans and two people left — they need a fifth van.",
              T(r'$50$ people, vans of $12$ $\to$ $5$ vans (round UP)', 36),
              "'50 people, vans of 12 → 5 vans (round UP)' appears")

    # ---- Ratios: keep slides 1-7 (the Hebrew ratio lesson); cut 8-11 --------------------
    vid = 'wp-034'
    _keep_slides(M, vid, [1, 2, 3, 4, 5, 6, 7], ['What a ratio tells you', 'A ratio is a fraction', 'No amounts!',
                                                  'Part of a whole', 'Fractions in a ratio', 'Reversed: "costs as"'])
    _add_line(M, vid, 7, None, "Four questions next. Watch the ratio units do all the work.")
    # "Units and divisibility" -> Q6 (difference 2x → even; boys ÷3, girls ÷5, class ÷8)
    # "Three-part ratios" -> Q8 choir; "Changing a ratio" -> Q9 club. Recap cut.

    # ---- Build the Equation: keep title + "Equations everywhere" (Hebrew intro) ----------
    vid = 'wp-037'
    _keep_slides(M, vid, [1, 2], ['Equations everywhere'])
    _add_line(M, vid, 2, None, "Let's see it in the questions.")
    # "Choose x wisely" -> Q10 rooms (x = what they ask; 18 is the new number = trap)
    # "Before and after" -> Q10 (total unchanged) + Q11 table; move the moved/removed/added rule
    _add_line(M, 'solve-wp22-g038', 2, "The number of students didn't change",
              "Moved between groups? The total stays. Removed? It drops. Added from outside? It grows.",
              T(r'Moved $\to$ total stays · removed $\to$ drops · added $\to$ grows', 34),
              "'Moved → total stays · removed → drops · added → grows' appears")
    # "Giving: the gap changes twice" -> Q11 shelves (gap changes by 2 per book, turns around);
    # move "to make them equal, give half the gap"
    _add_line(M, 'solve-q-r26-t22-20', 3, 'The traps: thirty-two',
              "To make them equal, you give half the gap: thirteen. Here B must end up ahead, so we need more.",
              T('Equal? Give half the gap', 36), "'Equal? Give half the gap' appears")

    # ---- Give It to the Little Guy: title only (Hebrew teaches it inside the age question) -
    vid = 'wp-039'
    _keep_slides(M, vid, [1], [])
    _add_line(M, vid, 1, None, "Let's see it in two questions: an age question and a budget question.")
    # "Equal sides" -> Q12 ages ("think of four and eight — you double the four"); move the warning
    _add_line(M, 'solve-wp22-g039', 2, "Not Iris. Think of four and eight",
              "Lots of students double the bigger one. That's backwards: the times two goes on the smaller side.",
              T(r'Twice? The $\times2$ goes on the smaller side', 36),
              "'Twice? The ×2 goes on the smaller side' appears")
    # "Ages: gaps stay" -> Q12 (row for each time); move the rule
    _add_line(M, 'solve-wp22-g039', 2, "Iris was TWICE Leo",
              "Notice: the gap is still six. Everyone ages the same — the gap stays, only the ratio changes.")
    # "Test the answers" -> Q12 / Q13 method 2; "Enough, not enough" -> Q13 notebooks. Recap cut.

    # ---- Shortcuts Ahead: title only (Hebrew advanced intro); each shortcut is taught in its question
    vid = 'r26-t22-shortcuts'
    _keep_slides(M, vid, [1], [])
    M.edit_lines(vid, 1, lambda ls: [
        {'say': "Advanced questions: no single formula here."},
        {'say': "We build an equation, or we understand and calculate — and each question shows a shortcut."},
        {'say': "Try each one first — then watch."}])

    # ---- Three Exam Tools: keep title + "One equation, two unknowns" (no question after it teaches it)
    vid = 'r26-t22-exam-tools'
    _keep_slides(M, vid, [1, 4], ['Two unknowns'])
    M.edit_lines(vid, 1, lambda ls: [
        {'say': "Three more tools the exam loves."},
        {'say': "First: knowing when you CAN'T find the answer."},
        {'say': "The other two — letters in the answers, and a fast trick for two kinds of items — we'll learn in the questions."}])
    _add_line(M, vid, 2, None, "Two questions next.")
    # "Letters in the choices" -> Q23 pens (choose numbers, not 0/1, test every choice); move the tie-break
    _add_line(M, 'solve-q-r26-t22-04', 2, 'Only choice two gives twenty-one',
              "Two choices give the same result? Choose new numbers and test only those two.",
              T('Two choices tie? New numbers, test only those two', 34),
              "'Two choices tie? New numbers, test only those two' appears")
    # "Assume all the same" -> Q24 parking lot (both "all motorcycles" and "the other kind"). Recap cut.

    # ---- follow-up (coordinator): no idea lost; no title-only lessons -----------------------
    # Equal Ratios: title + one short intro slide (Hebrew B32)
    vid = 'wp-028'
    M.edit_lines(vid, 1, lambda ls: [
        {'say': "Equal ratios. A short lesson — and one of the most important in the whole course."}])
    M.insert_slides(vid, 1, [dict(mode='concept', title='Same rate, two cases', active=0, pre=[], script=[
        "This technique follows you everywhere: word problems, geometry, algebra.",
        A("'Same rate in both cases → equal ratios' appears", T(r'Same rate in both cases $\to$ equal ratios', 40)),
        "Many questions rest on one idea: the same rate in two cases. The easiest way to learn it: on an example."])])
    M.set_sidebar(vid, ['Same rate, two cases'])
    # the name "triangle value" (was in the cut slide) -> Q1 trays, slide 3
    _add_line(M, 'solve-wp22-g029', 3, 'Write "15 × 42 ÷ 6"',
              "Diagonal times, divide by the rest. The three numbers make a triangle — hence the name.")
    # the teacher's preference (was in "Cross-multiply") -> Q2 exercises, method 2
    _add_line(M, 'solve-wp22-g030', 3, 'Sense check: fourteen minutes',
              "Triangle value or cross-multiplying — pick whichever feels natural. The triangle value writes the answer straight away, without isolating x.")
    # inverse examples: add the food supply (was in "Inverse proportion") -> Q3 workers
    _set_say(M, 'solve-q-r26-t22-02', 3, 'The rule: one goes up, the other goes down',
             "The rule: one goes up, the other goes down — the product stays the same. Workers and days, speed and time, people and the days a food supply lasts.")

    # Give It to the Little Guy: title + one short intro slide (Hebrew B43: a technique for building equations)
    vid = 'wp-039'
    M.edit_lines(vid, 1, lambda ls: [
        {'say': "A technique that sounds funny — and saves points, even for strong students."},
        {'say': "We call it: give it to the little guy."}])
    M.insert_slides(vid, 1, [dict(mode='concept', title='Where it helps', active=0, pre=[], script=[
        A("'Building an equation: twice · three times · ages' appears", T('Building an equation: twice · three times · ages', 40)),
        "We use it when we build an equation — with 'twice', 'three times', and in age questions.",
        "Let's see it in two questions: an age question and a budget question."])])
    M.set_sidebar(vid, ['Where it helps'])
    # "A is twice B → B = x, A = 2x: no fractions" (was in "Equal sides") -> Q19 clubs, method 1
    _set_say(M, 'solve-wp22-g047', 2, 'B is x, A is three x.',
             "Give the plain x to the little guy: B is x, A is three x. No fractions, no dividing later.")

    # Shortcuts Ahead: title + one short intro slide (Hebrew B45: general problems, no formula)
    vid = 'r26-t22-shortcuts'
    M.edit_lines(vid, 1, lambda ls: [{'say': "Advanced questions: general problems."}])
    M.insert_slides(vid, 1, [dict(mode='concept', title='No formula here', active=0, pre=[], script=[
        "Not motion, not percents, not work — no formula to guide you.",
        A("'Build an equation · or understand and calculate' appears", T('Build an equation · or understand and calculate', 40)),
        "We deal with each question by what's in it. And each question shows a shortcut — try it first, then watch."])])
    M.set_sidebar(vid, ['No formula here'])
    # Q14 opened with the same sentence -> keep only its own line
    M.edit_lines('solve-wp22-g042', 1, lambda ls: [l for l in ls if 'No single formula here' not in (l.get('say') or '')])

    # Three Exam Tools: slide 2 opened with "Last tool:" though it is now the only one here
    M.edit_lines('r26-t22-exam-tools', 2, lambda ls: [l for l in ls if not (l.get('say') or '').startswith('Last tool:')])


# =====================================================================================
# 2026-10-06 practice: new methods (runs LAST). Extra method lines appended to practice
# explanations. Pick values that fit is taught later (topic 51 Case 4) -> self-contained shortcut with its why.
# =====================================================================================

def _pm_add(M, qid, lines):
    """Append extra-method lines to a PRACTICE question explanation (existing lines kept)."""
    sec = M.section_of(qid)
    assert sec.endswith("-practice"), (qid, sec)
    ex = list(M.q(qid).get("explanation") or [])
    if any(l in ex for l in lines): return
    M.set_q(qid, expl=ex + list(lines))


def practice_methods(M):
    _pm_add(M, 'q-r26-t22-17', [r'Shortcut · Pick values that fit: one equation and two prices, but the question expects one answer, therefore any prices that fit the equation give it. Take $p=0$: $4n=50$ and $n=12.5$. Then $6n+9p=6\cdot12.5+0=75$ ✓.'])
    _pm_add(M, 'wp22-p29', [r'Shortcut · Pick values that fit: $B=24$ gives $3$ and $1$ brushes per artist ✓, and $B=48$ gives $6$ and $2$ ✓. Two different numbers fit everything, therefore it cannot be determined.'])
    _pm_add(M, 'wp22-p18', [r'Shortcut · Pick values that fit: two equations and four letters, therefore numbers that fit the givens are enough to test the choices. $a=1$, $b=2$, $c=2$, $d=1$: rows $1+2=2+1$ ✓, columns $1+2=2+1$ ✓. Choice 1: $1=2$ ✗. Choice 2: $ad=1$ but $bc=4$ ✗. Choice 3: $a+d=2$ but $b+c=4$ ✗. Only choice 4 is left.'])


# ======================================================================================================
# 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived item (the 18 guided
# wp22-g0NN questions, the 30 Hebrew practice questions wp22-p01 .. p30 and the Hebrew lessons' own examples) gets new
# numbers, and every word problem a new story (names, objects, setting) - same structure, same kind of condition,
# same trap, same level, at least the same methods. Plus the approved practice clean-up.
# Nothing in topic 22 is recorded (no take in ~/Documents/Course.recordings). Runs last, after practice_methods.
# ======================================================================================================
RN_RECORDED = set()


def _rn_sub(M, vid, n, pairs):
    """Exact substring replacements on one slide: board items, item labels, spoken lines, draw cues."""
    if vid in RN_RECORDED: return
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = 0
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit += 1
        for l in b['lines']:
            for key in ('say', 'draw', 'label'):
                if key in l and old in l[key]: l[key] = l[key].replace(old, new); hit += 1
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    M.touched_videos.add(vid)


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid not in RN_RECORDED: M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides, intro=None):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. Titles and the pre-loaded question stay."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script)
    if intro:
        old, new = intro
        _rn_sub(M, vid, 1, [(old, new)])


def _tbl(headers, rows, w, h):
    return dict(k='vis', v={'type': 'table', 'headers': headers, 'rows': rows}, w=w, h=h)


def rn_lessons(M):
    # ---- From Words to Equations (wp-027) ----
    L = 'wp-027'
    # slide 3: x4 + 18 = 6x, twice -> 18   ==>   x3 + 24 = 7x, twice -> 12
    _rn_sub(M, L, 3, [
        ('A number is multiplied by 4, and then 18 is added. The result is 6 times the original number.',
         'A number is multiplied by 3, and then 24 is added. The result is 7 times the original number.'),
        ('"Multiplied by four" — four x. "And then eighteen is added" — plus eighteen.',
         '"Multiplied by three" — three x. "And then twenty-four is added" — plus twenty-four.'),
        ('Write "4x + 18"', 'Write "3x + 24"'),
        ('"Six times the original number" — six x.', '"Seven times the original number" — seven x.'),
        ('Write "= 6x"', 'Write "= 7x"'),
        ('a number, times four, plus eighteen, equals six times the number.',
         'a number, times three, plus twenty-four, equals seven times the number.'),
        ('Take four x from both sides.', 'Take three x from both sides.'),
        ('Write "18 = 2x → x = 9"', 'Write "24 = 4x → x = 6"'),
        ('Eighteen equals two x. x is nine.', 'Twenty-four equals four x. x is six.'),
        ('write "2x = 18"', 'write "2x = 12"'),
        ("Eighteen. That's the answer — not nine.", "Twelve. That's the answer — not six.")])
    # slide 4: 6 more, 9 less  ==>  7 more, 4 less
    _rn_sub(M, L, 4, [
        ('A is 6 more than B:  $A=B+6$', 'A is 7 more than B:  $A=B+7$'),
        ('A is 6 more than B:  A = B + 6', 'A is 7 more than B:  A = B + 7'),
        ('A is six more than B. Start with B, add six — you reach A. A equals B plus six.',
         'A is seven more than B. Start with B, add seven — you reach A. A equals B plus seven.'),
        ('A is 9 less than B:  $A=B-9$', 'A is 4 less than B:  $A=B-4$'),
        ('A is 9 less than B:  A = B − 9', 'A is 4 less than B:  A = B − 4'),
        ('A is nine less than B. Start with B, take away nine. A equals B minus nine.',
         'A is four less than B. Start with B, take away four. A equals B minus four.'),
        ('write "B = A + 9"', 'write "B = A + 4"'),
        ('B is A plus nine.', 'B is A plus four.'),
        ('if B is twenty, A is eleven. Not negative eleven.', 'if B is twenty, A is sixteen. Not negative sixteen.')])
    # slide 5: three times, B = 7 -> 21 not 10  ==>  five times, B = 4 -> 20 not 9
    _rn_sub(M, L, 5, [
        ('A is three times B:  $A=3B$', 'A is five times B:  $A=5B$'),
        ('A is three times B:  A = 3B', 'A is five times B:  A = 5B'),
        ('A is three times B: A equals three B.', 'A is five times B: A equals five B.'),
        ("Don't mix up three TIMES as much with three MORE.", "Don't mix up five TIMES as much with five MORE."),
        ('Next to A = 3B write "B = 7 → 21, not 10"', 'Next to A = 5B write "B = 4 → 20, not 9"'),
        ('If B is seven: three times is twenty-one. Three more would be ten.',
         'If B is four: five times is twenty. Five more would be nine.')])
    # slide 6: two fifths / one quarter less  ==>  three fifths / one third less
    _rn_sub(M, L, 6, [
        ('Two fifths of $n$:  $\\frac25n$', 'Three fifths of $n$:  $\\frac35n$'),
        ('Two fifths of n:  2/5 n', 'Three fifths of n:  3/5 n'),
        ('Two fifths of n is two fifths times n.', 'Three fifths of n is three fifths times n.'),
        ('One quarter less than $n$:  $\\frac34n$', 'One third less than $n$:  $\\frac23n$'),
        ('One quarter less than n:  3/4 n', 'One third less than n:  2/3 n'),
        ('One quarter less than n: take all of n, remove a quarter of it — three quarters of n are left.',
         'One third less than n: take all of n, remove a third of it — two thirds of n are left.'),
        ('write "n − ¼n = ¾n"', 'write "n − ⅓n = ⅔n"'),
        ('The quarter is a quarter OF n.', 'The third is a third OF n.')])
    # slide 7: difference 12  ==>  15
    _rn_sub(M, L, 7, [
        ('The difference between A and B is 12:  $|A-B|=12$', 'The difference between A and B is 15:  $|A-B|=15$'),
        ('The difference between A and B is 12:  |A − B| = 12', 'The difference between A and B is 15:  |A − B| = 15'),
        ('"The difference between A and B is twelve."', '"The difference between A and B is fifteen."'),
        ('write "A − B = 12  or  B − A = 12"', 'write "A − B = 15  or  B − A = 15"'),
        ('If A is bigger, A minus B is twelve. If B is bigger, B minus A is twelve.',
         'If A is bigger, A minus B is fifteen. If B is bigger, B minus A is fifteen.')])
    # slide 8: makes up 2/3, 3N = 5P  ==>  makes up 3/4, 2N = 7P (review: 2N = 5P echoed the Hebrew '2 pens : 5 pencils')
    _rn_sub(M, L, 8, [
        ('A is (makes up) $\\frac23$ of B:  $A=\\frac23B$', 'A is (makes up) $\\frac34$ of B:  $A=\\frac34B$'),
        ('A is 2/3 of B:  A = 2/3 B', 'A is 3/4 of B:  A = 3/4 B'),
        ('"A makes up two thirds of B". Just swap it for "is": A is two thirds of B.',
         '"A makes up three quarters of B". Just swap it for "is": A is three quarters of B.'),
        ('3 notebooks cost the same as 5 pens:  $3N=5P$', '2 notebooks cost the same as 7 pens:  $2N=7P$'),
        ('3 notebooks cost the same as 5 pens:  3N = 5P', '2 notebooks cost the same as 7 pens:  2N = 7P'),
        ('Three notebooks: three N. Five pens: five P. Three N equals five P.',
         'Two notebooks: two N. Seven pens: seven P. Two N equals seven P.')])
    # slide 9: ratio 2 : 3  ==>  3 : 7
    _rn_sub(M, L, 9, [
        ('The ratio of A to B is $2:3$', 'The ratio of A to B is $3:7$'),
        ('The ratio of A to B is 2 : 3', 'The ratio of A to B is 3 : 7'),
        ('The ratio of A to B is two to three.', 'The ratio of A to B is three to seven.'),
        ('For every two A, there are three B.', 'For every three A, there are seven B.'),
        ('Write "A = 2x,  B = 3x"', 'Write "A = 3x,  B = 7x"'),
        ('So we write them as two x and three x.', 'So we write them as three x and seven x.')])
    rows = M.card('mem-word-phrases')['tables'][0]['rows']
    new = [['A is 7 more than B', '$A=B+7$'], ['A is 4 less than B', '$A=B-4$'], ['A is 5 times B', '$A=5B$'],
           ['Twice / double', 'always $\\times2$'], ['Three fifths of $n$ ("of" = times)', '$\\frac35n$'],
           ['One third less than $n$', '$\\frac23n$'], ['A is (makes up) $\\frac34$ of B', '$A=\\frac34B$'],
           ['The difference between A and B is 15', '$|A-B|=15$'], ['2 notebooks cost the same as 7 pens', '$2N=7P$'],
           ['The ratio of A to B is $3:7$', '$A=3x,\\ B=7x$']]
    assert len(rows) == len(new) and rows[3][0] == 'Twice / double', rows
    rows[:] = new

    # ---- Ratios (wp-034): blue : orange 3 : 5  ==>  3 : 7 ----
    L = 'wp-034'
    for it in M.slide(L, 2)['items']:
        if it.get('k') == 'vis' and it['v'].get('type') == 'bars': it['v']['values'] = [3, 7]
    _rn_sub(M, L, 2, [
        ('blue 3 units, orange 5 units', 'blue 3 units, orange 7 units'),
        ('The ratio of blue to orange is three to five. For every three blue, there are five orange.',
         'The ratio of blue to orange is three to seven. For every three blue, there are seven orange.'),
        ('five thirds as much. One and two thirds times.', 'seven thirds as much. Two and a third times.')])
    _rn_sub(M, L, 3, [
        ('Blue : orange $=3:5=\\frac35$', 'Blue : orange $=3:7=\\frac37$'),
        ('Blue : orange = 3 : 5 = 3/5', 'Blue : orange = 3 : 7 = 3/7'),
        ('Three to five is three fifths — three divided by five.', 'Three to seven is three sevenths — three divided by seven.'),
        ('Blue three, orange five.', 'Blue three, orange seven.'),
        ('$12:20=3:5$', '$12:28=3:7$'), ('12 : 20 = 3 : 5', '12 : 28 = 3 : 7'),
        ('under both 12 and 20', 'under both 12 and 28'),
        ('Twelve to twenty is three to five.', 'Twelve to twenty-eight is three to seven.')])
    _rn_sub(M, L, 4, [
        ('$3:5$ could be $3\\ \\&\\ 5$,  $6\\ \\&\\ 10$,  $30\\ \\&\\ 50$, …', '$3:7$ could be $3\\ \\&\\ 7$,  $6\\ \\&\\ 14$,  $30\\ \\&\\ 70$, …'),
        ('3 : 5 could be 3 & 5, 6 & 10, 30 & 50, …', '3 : 7 could be 3 & 7, 6 & 14, 30 & 70, …'),
        ('Three and five? Six and ten? Thirty and fifty?', 'Three and seven? Six and fourteen? Thirty and seventy?'),
        ('Blue $=3x$,  orange $=5x$', 'Blue $=3x$,  orange $=7x$'), ('Blue = 3x,  orange = 5x', 'Blue = 3x,  orange = 7x'),
        ('three x and five x.', 'three x and seven x.'),
        ('Write "3x/5x = 3/5"', 'Write "3x/7x = 3/7"'),
        ('the ratio is still three to five', 'the ratio is still three to seven')])
    _rn_sub(M, L, 5, [
        ('Blue is $\\frac38$ of all the items', 'Blue is $\\frac{3}{10}$ of all the items'),
        ('Blue is 3/8 of all the items', 'Blue is 3/10 of all the items'),
        ('Blue is three eighths of all the items. Three out of eight.', 'Blue is three tenths of all the items. Three out of ten.'),
        ('Write "blue = 3x,  all = 8x"', 'Write "blue = 3x,  all = 10x"'),
        ('ALL of them is eight x.', 'ALL of them is ten x.'),
        ('Write "orange = 8x − 3x = 5x"', 'Write "orange = 10x − 3x = 7x"'),
        ("Orange is whatever's left: five x.", "Orange is whatever's left: seven x.")])
    _rn_sub(M, L, 6, [
        ('$A:B=1.5:2$', '$A:B=2.5:3$'), ('A : B = 1.5 : 2', 'A : B = 2.5 : 3'),
        ('one and a half to two.', 'two and a half to three.'),
        ('Write "×2 → ratio 3 : 4 → A = 3x, B = 4x"', 'Write "×2 → ratio 5 : 6 → A = 5x, B = 6x"'),
        ('three to four. Three x and four x', 'five to six. Five x and six x')])
    _rn_sub(M, L, 7, [
        ('3 notebooks cost the same as 5 pens', '2 notebooks cost the same as 7 pens'),
        ('Write "3N = 5P"', 'Write "2N = 7P"'),
        ('Three N equals five P.', 'Two N equals seven P.'),
        ('Pick a number both sides can reach — fifteen.', 'Pick a number both sides can reach — fourteen.'),
        ('Write "N = 5,  P = 3 → ratio N : P = 5 : 3"', 'Write "N = 7,  P = 2 → ratio N : P = 7 : 2"'),
        ('Three notebooks make fifteen if each costs five. Five pens make fifteen if each costs three.',
         'Two notebooks make fourteen if each costs seven. Seven pens make fourteen if each costs two.'),
        ('So notebook to pen is five to three', 'So notebook to pen is seven to two')])
    rows = M.card('mem-ratios')['tables'][1]['rows']
    fix = {'A ratio is a fraction': '$3:7=\\frac37$', 'Expand / reduce like a fraction': '$12:28=3:7$',
           'No amounts from a ratio alone': 'write $3x$ and $7x$', 'Part of a whole': '$\\frac{3}{10}$ of all → part $3x$, whole $10x$',
           '"Costs the same as" is reversed': '$2N=7P \\to N:P=7:2$'}
    for r in rows:
        if r[0] in fix: r[1] = fix.pop(r[0])
    assert not fix, fix

    # ---- toolkit card: the guided questions' new numbers ----
    rows = M.card('mem-general-advanced')['tables'][0]['rows']
    fix = {'Same ratios': ('a rate like "1 credit buys 1.5 pineapples"', '$\\frac{2\\cdot1}{1.5}=\\frac{4}{3}$ (expand ×2, not ×10)'),
           'Write the whole exercise first': (None, '$160\\cdot\\frac34\\cdot\\frac34=160\\cdot\\frac{9}{16}=90$'),
           'Ratio units': ('"A is $\\frac58$ of B"', 'the ratio $C:T=5:8$, C out of all $=\\frac{5}{13}$'),
           'Divisibility of the total': (None, 'ratios $4:1$ and $2:1$ → total divides by 5 and by 3'),
           'Subtract the equations': (None, '3 hours $=135$ → $\\frac{135}{3}=45$ each'),
           'Scale everything': (None, '$9\\to12$ and $6\\to8$: $\\times\\frac43$'),
           'Start from the end': (None, 'equal at the end: 35 and 35')}
    for r in rows:
        if r[0] in fix:
            when, ex = fix.pop(r[0])
            if when: r[1] = when
            r[2] = ex
    assert not fix, fix


def rn_guided(M):
    MOVE = A("'Moved → total stays · removed → drops · added → grows' appears",
             T('Moved $\\to$ total stays · removed $\\to$ drops · added $\\to$ grows', 34))
    TWICE = A("'Twice? The ×2 goes on the smaller side' appears", T('Twice? The $\\times2$ goes on the smaller side', 36))

    # ---------- Q1 wp22-g029: 6 trays / 42 biscuits, 15 trays -> 105   ==>   8 vases / 56 roses, 12 vases -> 84
    _rn_q(M, 'wp22-g029', 'Eight vases hold 56 roses. With the same number of roses in each vase, how many roses are in 12 vases?',
          ['77', '91', '84', '96'], 3, [
        'Across in the ratio table: $\\frac{56}{8}=7$ roses per vase.',
        '12 vases: $12\\cdot7=84$ roses.',
        'Triangle value: $\\frac{12\\cdot56}{8}=12\\cdot7=84$.'])
    _rn_video(M, 'wp22-g029', [[
        'Eight vases, fifty-six roses. Twelve vases?',
        'The same number in every vase — equal ratios. Ratio table.',
        A('A ratio table appears: Vases | Roses — 8 | 56 and 12 | ?', _tbl(['Vases', 'Roses'], [['8', '56'], ['12', '?']], 520, 170)),
        'Put the data in a ratio table: vases in one column, roses in the other. Eight is to fifty-six as twelve is to the missing number.',
        D('Draw an arrow from 8 to 56 and write "×7"'),
        'Across: eight to fifty-six — times seven.',
        D('Draw an arrow from 12 to the ? and write "×7 = 84"'),
        'Twelve times seven: eighty-four.',
        D('Circle choice 3'),
        'Choice three.',
        'Down would be times one and a half — also fine, but across is whole. So, across is easier.',
    ], [
        "The triangle value gives the same thing: multiply along the diagonal, twelve times fifty-six, and divide by what's left, eight.",
        'Diagonal times, divide by the rest. The three numbers make a triangle — hence the name.',
        D('Write "12 × 56 ÷ 8"'),
        'Cancel fifty-six with eight: seven.',
        D('Write "= 12 × 7 = 84"'),
        'Twelve sevens — eighty-four. Same answer.',
    ]])

    # ---------- Q2 wp22-g030: 12 exercises in 8 min, 14 min -> 21   ==>   18 potatoes in 12 min, 20 min -> 30
    _rn_q(M, 'wp22-g030', 'Working at a steady pace, a cook peels 18 potatoes in 12 minutes. How many potatoes does he peel in 20 minutes?',
          ['30', '36', '24', '27'], 1, [
        'Across and down are not whole numbers. Triangle value: $\\frac{20\\cdot18}{12}=\\frac{20\\cdot3}{2}=30$.',
        'Sense check: 20 minutes is less than twice 12 minutes. The answer must be less than $2\\cdot18=36$ ✓.'])
    _rn_video(M, 'wp22-g030', [[
        'Twelve minutes, eighteen potatoes. Twenty minutes?',
        A('A ratio table appears: Minutes | Potatoes — 12 | 18 and 20 | ?', _tbl(['Minutes', 'Potatoes'], [['12', '18'], ['20', '?']], 520, 170)),
        'Across: twelve to eighteen — one and a half. Down: twelve to twenty — one and two thirds. Neither is whole.',
        'So: the triangle value — also called "cross-multiply and divide".',
        D('Draw the diagonal from 20 to 18 and write "20 × 18 ÷ 12"'),
        'Diagonal: twenty times eighteen. Divide by the rest: twelve.',
        D('Cancel 18 and 12 by 6 (3 and 2), then write "= 20 × 3 ÷ 2 = 30"'),
        'Eighteen and twelve share a six: three and two. Twenty times three, over two. Thirty.',
        D('Circle choice 1'),
        'Choice one.',
    ], [
        'Or cross-multiply: the diagonal products are equal.',
        D('Write "12x = 20 · 18 = 360 → x = 30"'),
        'Twelve x equals twenty times eighteen — three hundred and sixty. x is thirty.',
        'Triangle value or cross-multiplying — pick whichever feels natural. The triangle value writes the answer straight away, without isolating x.',
        'Sense check: twenty minutes is less than double twelve. So, fewer than thirty-six potatoes. Thirty fits.',
    ]])

    # ---------- Q4 wp22-g032: tart 58, pastry/filling/berries -> 20   ==>   sandwich 47, bread/cheese/olives -> 12
    _rn_q(M, 'wp22-g032', 'A café sells a sandwich for 47 credits. Making it uses 200 g of bread at 4 credits per 100 g, 300 g of cheese '
          'at 8 credits per 100 g, and 6 olives at half a credit each. Ignoring other costs, what is the selling price minus the ingredient cost?',
          ['15', '35', '12', '9'], 3, [
        'Bread: $2\\cdot4=8$. Cheese: $3\\cdot8=24$. Olives: $6\\cdot\\frac12=3$.',
        'Ingredient cost: $8+24+3=35$ credits.',
        'Selling price minus cost: $47-35=12$ credits. (35 is the cost — not what they asked.)'])
    _rn_video(M, 'wp22-g032', [[
        'Step one: what does it cost to make one sandwich?',
        A("'Label every number · per 100 g ≠ per g · a fixed fee is paid once' appears", T('Label every number · per 100 g ≠ per g · a fixed fee is paid once', 34)),
        'Label every number: a price per hundred grams is not a price per gram, and a fixed fee is paid once.',
        'Bread: two hundred grams. A hundred grams costs four.',
        D('Write "Bread: 100 g → 4,  200 g → ×2 → 8"'),
        'A hundred to two hundred is times two. So, four times two, eight. Equal ratios again.',
        D('Write "Cheese: 300 g → ×3 → 24"'),
        'Cheese: three hundred grams at eight per hundred. Times three — twenty-four.',
        D('Write "Olives: 6 × ½ = 3"'),
        'Olives: six at half a credit. Three.',
        D('Write "Cost = 8 + 24 + 3 = 35"'),
        'Total cost: thirty-five.',
        'Step two: what did they ask? Selling price minus ingredient cost.',
        D('Write "47 − 35 = 12" and circle choice 3'),
        'Forty-seven minus thirty-five: twelve. Choice three.',
        "Careful — thirty-five is in the choices too. That's the cost, not what they asked.",
    ]])

    # ---------- Q5 wp22-g033: 3/min vs 14 per 5-min block, 11.5 min -> 6   ==>   4/hour vs 17 per 4-hour block, 9.5 h -> 11
    _rn_q(M, 'wp22-g033', 'Bike shop A charges 4 credits for every hour or part of an hour. Bike shop B charges 17 credits for every '
          '4-hour block or part of a block. What is the difference between the two charges for a 9.5-hour rental?',
          ['15', '13', '6', '11'], 4, [
        'Shop A: 9.5 hours are paid as 10 hours ("or part of an hour"): $10\\cdot4=40$ credits.',
        'Shop B: two blocks cover only 8 hours. 9.5 hours need 3 blocks: $3\\cdot17=51$ credits.',
        'Difference: $51-40=11$ credits.'])
    _rn_video(M, 'wp22-g033', [[
        'The catch is two little words: "or part".',
        D('Underline both "or part of"'),
        'Shop A: four credits an hour. Nine hours: thirty-six.',
        D('Write "A: 9 h → 36"'),
        "Then there's half an hour left. Half an hour, a quarter, one minute — you still pay the full four.",
        D('Write "+ ½ h → + 4 = 40"'),
        'Forty.',
        D('Write "B: 8 h = 2 blocks → 34"'),
        'Shop B: seventeen per four-hour block. Eight hours — two blocks, thirty-four.',
        D('Write "+ 1.5 h → 1 more block → 51"'),
        "An hour and a half left. That's part of a block. So, it's a whole block. Fifty-one.",
        D('Write "51 − 40 = 11" and circle choice 4'),
        'The difference: eleven. Choice four.',
        A("'50 people, vans of 12 → 5 vans (round UP)' appears", T('$50$ people, vans of $12$ $\\to$ $5$ vans (round UP)', 36)),
        'Same with people: fifty people, vans of twelve. Four vans and two people left — they need a fifth van.',
    ]])

    # ---------- Q6 wp22-g035: boys 3/8 of the class, difference -> even (18)   ==>   swimmers 5/12 of the camp -> even (22)
    _rn_q(M, 'wp22-g035', 'At a sports camp, swimmers make up $\\frac{5}{12}$ of all the campers, and the rest are runners. '
          'Which could be the difference between the numbers of runners and swimmers?',
          ['21', '22', '15', '19'], 2, [
        'Swimmers $=5x$ and all $=12x$. Runners $=12x-5x=7x$.',
        'Difference: $7x-5x=2x$. It must be even.',
        'Only 22 is even. Check: $x=11$ gives 55 swimmers and 77 runners, and $77-55=22$ ✓.'])
    _rn_video(M, 'wp22-g035', [[
        'Swimmers are five out of twelve.',
        D('Write "swimmers = 5x,  camp = 12x"'),
        'So swimmers are five x — and the whole camp is twelve x.',
        D('Write "runners = 12x − 5x = 7x"'),
        "The runners are what's left: seven x.",
        D('Write "difference = 7x − 5x = 2x"'),
        'The difference between runners and swimmers: two x.',
        'Two x. So, the difference must divide by two. It has to be even.',
        D('Cross out choices 1, 3 and 4; circle choice 2'),
        'Twenty-one, fifteen, nineteen — all odd. Out. Twenty-two. Choice two.',
        'Bonus: the swimmers divide by five, the runners by seven, and the whole camp by twelve.',
    ]])

    # ---------- Q7 wp22-g036: scooter : car 3 : 8, 15,000 more -> 33,000   ==>   sofa : piano 3 : 10, 14,000 more -> 26,000
    _rn_q(M, 'wp22-g036', 'The prices of a sofa and a piano are in the ratio $3:10$. The piano costs 14,000 credits more '
          'than the sofa. What is their combined price?',
          ['20,000', '26,000', '14,000', '28,000'], 2, [
        'Sofa $=3x$, piano $=10x$. Difference: $10x-3x=7x=14{,}000$, therefore $x=2{,}000$.',
        'Combined: $3x+10x=13x=26{,}000$ credits.'])
    _rn_video(M, 'wp22-g036', [[
        'Sofa to piano: three to ten.',
        D('Write "sofa = 3x,  piano = 10x"'),
        'Sofa three x, piano ten x.',
        D('Write "10x − 3x = 7x = 14,000 → x = 2,000"'),
        'The piano costs seven x more. Seven x is fourteen thousand. So, x is two thousand.',
        'They want the combined price — the sum: thirteen x.',
        D('Write "13x = 26,000" and circle choice 2'),
        'Twenty-six thousand. Choice two.',
        "Notice: even if you'd mixed up which is three and which is ten — the difference is still seven x and the sum is still thirteen x. Same answer.",
    ]])

    # ---------- Q10 wp22-g038: 6 rooms, one a storeroom, +3 -> 15   ==>   8 rows of chairs, one removed, +3 -> 21
    _rn_q(M, 'wp22-g038', 'A hall manager plans to set out the same number of chairs in each of 8 rows. One row must be removed to make '
          'room for a stage. Each of the 7 remaining rows must then hold 3 more chairs. How many chairs per row were originally planned?',
          ['24', '21', '18', '27'], 2, [
        'Planned chairs per row $=x$. The number of chairs does not change: $8x=7(x+3)$.',
        '$8x=7x+21$, therefore $x=21$.',
        'They asked for the planned number: 21. (24 is the new number per row.)'])
    _rn_video(M, 'wp22-g038', [[
        'They ask how many per row in the plan. So x is exactly that.',
        D('Write "plan: 8 rows × x = 8x"'),
        'The plan: eight rows, x chairs each. Eight x.',
        D('Write "actual: 7 rows × (x + 3) = 7(x + 3)"'),
        'In reality one row was removed. Seven rows left — and each got three more. Seven times x plus three.',
        MOVE,
        'Moved between groups? The total stays. Removed? It drops. Added from outside? It grows.',
        "The number of chairs didn't change. So the two are equal.",
        D('Write "8x = 7(x + 3)"'),
        D('Write "8x = 7x + 21 → x = 21"'),
        'Eight x equals seven x plus twenty-one. x is twenty-one.',
        "What's x? Chairs per row in the plan — exactly what they asked.",
        D('Circle choice 2'),
        "Choice two. Twenty-four is a trap — that's the NEW number per row.",
    ]])

    # ---------- Q12 wp22-g039: Iris 6 older, 4 years ago twice -> Leo 10   ==>   Maya 9 older, 5 years ago twice -> Tom 14
    _rn_q(M, 'wp22-g039', 'Maya is 9 years older than her cousin Tom. Five years ago, Maya was twice Tom’s age. How old is Tom now?',
          ['9', '12', '14', '18'], 3, [
        'Tom now $=x$, Maya now $=x+9$. Write a row for each time:',
        '$\\begin{array}{l|c|c} & \\text{Tom} & \\text{Maya} \\\\ \\hline \\text{now} & x & x+9 \\\\ \\text{5 years ago} & x-5 & x+4 \\end{array}$',
        'Five years ago Maya was twice Tom. The $\\times2$ goes on the smaller side: $2(x-5)=x+4$.',
        '$2x-10=x+4$, therefore $x=14$. Check: five years ago they were 9 and 18 ✓.'])
    _rn_video(M, 'wp22-g039', [[
        "They ask for Tom's age now. So, Tom is x.",
        A('An age table appears: Now / 5 years ago for Tom and Maya',
          _tbl(['', 'Tom', 'Maya'], [['Now', 'x', 'x + 9'], ['5 years ago', '', '']], 700, 170)),
        'Now: Tom x, Maya x plus nine. Maya is the bigger one. So, no minus signs.',
        "Here's where lots of students jump straight to the equation. Stop. First fill in the row for five years ago.",
        D('In the table write "x − 5" and "x + 4"'),
        'Five years ago: Tom x minus five. Maya x plus nine minus five — x plus four.',
        'Notice: the gap is still nine. Everyone ages the same — the gap stays, only the ratio changes.',
        'Maya was TWICE Tom. So who gets the times two?',
        TWICE,
        "Lots of students double the bigger one. That's backwards: the times two goes on the smaller side.",
        'Not Maya. Think of four and eight — you double the four. The little guy. Tom.',
        D('Write "2(x − 5) = x + 4"'),
        D('Write "2x − 10 = x + 4 → x = 14"'),
        'Open the brackets: two x minus ten equals x plus four. x is fourteen.',
        D('Circle choice 3'),
        'x is Tom now — exactly what they asked. Choice three.',
    ], [
        'You can also test the answers.',
        D('Next to choice 1 write "4 → 8: gap 4 ✗"'),
        'Tom nine now: five years ago he was four, Maya double — eight. The gap is four, not nine. Out.',
        D('Next to choice 2 write "7 → 14: gap 7 ✗"'),
        'Twelve now: seven then, Maya fourteen. Gap seven. Out.',
        D('Next to choice 4 write "13 → 26: gap 13 ✗"'),
        'Eighteen now: thirteen then, Maya twenty-six. Gap thirteen. Out.',
        D('Next to choice 3 write "9 → 18: gap 9 ✓"'),
        'Fourteen now: nine then, Maya eighteen. Gap nine. It fits.',
        'And for the sharp-eyed: a gap of nine AND double — that can only be nine and eighteen. Add five years: Tom is fourteen.',
        'Careful: nine is Tom five years ago — not now.',
    ]])

    # ---------- Q13 wp22-g040: 84 credits, 5 but not 6 notebooks -> 16   ==>   105 credits, 6 but not 7 tickets -> 17
    _rn_q(M, 'wp22-g040', 'Dana has 105 credits. That is enough for 6 identical movie tickets but not enough for 7. '
          'Which could be the price of one ticket?',
          ['15', '17', '18', '20'], 2, [
        'Price $=p$. Enough for 6: $6p\\le105$, therefore $p\\le17.5$.',
        'Not enough for 7: $7p>105$, therefore $p>15$.',
        'Only 17 is in $15<p\\le17.5$. Check: $6\\cdot17=102\\le105$ ✓ and $7\\cdot17=119>105$ ✓.'])
    _rn_video(M, 'wp22-g040', [[
        'Call the price p.',
        D('Write "6p ≤ 105"'),
        'A hundred and five is enough for six tickets. So six p is at most a hundred and five — exactly a hundred and five still counts as enough.',
        D('Write "p ≤ 17.5" and cross out choices 3 and 4'),
        'Divide by six: p is at most seventeen and a half. Eighteen and twenty — out.',
        D('Write "7p > 105 → p > 15" and cross out choice 1'),
        'Not enough for seven: seven p is more than a hundred and five. p is more than fifteen. Fifteen is out.',
        D('Circle choice 2'),
        'Seventeen. Choice two.',
        "Just like building an equation — we built inequalities and knocked out what didn't fit.",
    ], [
        'Or test the answers.',
        D('Next to choice 1 write "6 × 15 = 90 ✓   7 × 15 = 105 ✗"'),
        'Fifteen: six cost ninety — fine. But seven cost exactly a hundred and five. So, she CAN buy seven. Out.',
        D('Next to choice 2 write "6 × 17 = 102 ✓   7 × 17 = 119 ✓"'),
        'Seventeen: six cost a hundred and two — enough. Seven cost a hundred and nineteen — not enough. Both conditions hold.',
        'Equation or testing — practice both and use whichever comes more easily.',
    ]])

    # ---------- Q14 wp22-g042: 2 oranges / 3.5 pears / 8 plums -> 38/7   ==>   4 kiwis / 1.5 pineapples / 5 limes -> 13/3
    _rn_q(M, 'wp22-g042', 'One credit buys 4 kiwis, 1.5 pineapples, or 5 limes, with costs proportional to quantity. '
          'What is the cost of 8 kiwis, 2 pineapples, and 5 limes? Fractional credits may be paid.',
          ['$\\frac{13}{3}$ credits', '3 credits', '5 credits', '6 credits'], 1, [
        'Kiwis: 1 credit buys 4, therefore 8 kiwis cost 2 credits. Limes: 5 limes cost 1 credit.',
        'Pineapples: $\\frac{2\\cdot1}{1.5}=\\frac{4}{3}$ credits (multiply top and bottom by 2, not by 10).',
        'Total: $2+1+\\frac{4}{3}=\\frac{13}{3}$ credits.'])
    _rn_video(M, 'wp22-g042', [[
        'Start with the easy groups.',
        D('Next to "8 kiwis" write "= 2 credits"'),
        'One credit buys four kiwis. Eight kiwis — two credits.',
        D('Next to "5 limes" write "= 1 credit"'),
        'One credit buys five limes. Five limes — exactly one credit.',
        'Now the awkward one: pineapples.',
        D('Write "1 credit — 1.5 pineapples" and under it "? — 2 pineapples"'),
        'One credit, one and a half pineapples. How many credits for two pineapples? Same ratio.',
        D('Write "? = 2 · 1 / 1.5"'),
        "Cross-multiply, divide by what's left: two times one, over one and a half.",
        'A decimal in the bottom — get rid of it. Times ten works… but it just makes the numbers bigger.',
        D('Write "×2" on top and bottom, then "= 4/3"'),
        'Times two is enough: four thirds.',
        D('Write "2 + 4/3 + 1 = 13/3" and circle choice 1'),
        'Two, plus four thirds, plus one: thirteen thirds. Choice one.',
    ], [
        'Now psychometric thinking — a size estimate saves the fraction work.',
        'Kiwis and limes: three credits. That part is easy.',
        'Pineapples: one credit buys one and a half. We need two. So more than one credit.',
        D('Write "total > 4" and cross out choice 2'),
        'Three plus more than one: more than four. Choice two — three credits — is out.',
        'Upper limit: two credits already buy three pineapples. We only need two.',
        D('Write "pineapples < 2  →  total < 5"'),
        'So the pineapples cost less than two credits, and the total is under five.',
        D('Cross out choices 3 and 4, circle choice 1'),
        'Five and six are out. Only thirteen thirds — about four and a third — is left. Choice one.',
    ]])

    # ---------- Q15 wp22-g043: 144 applicants, 5/6 stay, two rounds -> 100   ==>   160 players, 3/4 stay, two levels -> 90
    _rn_q(M, 'wp22-g043', 'A video game starts with 160 players. At the end of each level, $\\frac34$ of the players who began that level '
          'are still in the game. How many players are still in the game after two levels?',
          ['120', '80', '90', '100'], 3, [
        'Level 1: $160\\cdot\\frac34=120$. Level 2 acts on 120: $120\\cdot\\frac34=90$.',
        'Or write it all first: $160\\cdot\\frac34\\cdot\\frac34=160\\cdot\\frac{9}{16}=10\\cdot9=90$.',
        'The trap 80 takes both quarters from 160.'])
    _rn_video(M, 'wp22-g043', [[
        "A hundred sixty start. After each level, three quarters of that level's starters are still in.",
        A('A bar cut into 4 equal parts appears, 3 shaded', dict(k='bar', n=3, d=4, w=720, h=70, gap=40)),
        'Picture the group as a bar cut into four equal parts. Three of them stay.',
        D('Next to the bar write "160 ÷ 4 = 40"'),
        'One quarter of a hundred sixty. Half is eighty, half again — forty.',
        D('Write "40 · 3 = 120"'),
        'Three quarters: a hundred twenty. They start level two.',
        'Level two acts on a hundred twenty — not on a hundred sixty.',
        D('Write "120 ÷ 4 = 30 → 30 · 3 = 90"'),
        'One quarter of a hundred twenty: thirty. Three quarters: ninety.',
        D('Circle choice 3'),
        'Ninety. Choice three.',
        'Eighty is the trap — it takes both quarters from the hundred sixty.',
    ], [
        "A small trick for several stages: don't calculate as you go. Write the whole thing first.",
        D('Write "160 · 3/4 · 3/4"'),
        'A hundred sixty, times three quarters, times three quarters.',
        D('Write "= 160 · 9/16"'),
        'Four times four on the bottom: sixteen. Three times three on top: nine.',
        D('Write "160 ÷ 16 = 10  →  10 · 9 = 90"'),
        "And now it's obvious: a hundred sixty over sixteen is ten. Ten times nine — ninety.",
        'When a question has stages, write the full exercise first. The numbers usually cancel.',
    ]])

    # ---------- Q16 wp22-g044: 3/5 as many apprentices as supervisors -> 3/8   ==>   5/8 as many coaches as trainees -> 5/13
    _rn_q(M, 'wp22-g044', 'At a training center, there are $\\frac58$ as many coaches as trainees. What fraction of all the people are coaches?',
          ['$\\frac{5}{8}$', '$\\frac{3}{8}$', '$\\frac{8}{13}$', '$\\frac{5}{13}$'], 4, [
        'The ratio of coaches to trainees is $5:8$.',
        'Plug in: 8 trainees and 5 coaches, 13 people in all.',
        'Coaches are $\\frac{5}{13}$ of all the people. ($\\frac58$ compares them with the trainees only.)'])
    _rn_video(M, 'wp22-g044', [[
        'Coaches equal five eighths of the trainees.',
        D('Write "C = 5/8 · T"'),
        'As an equation: C equals five eighths of T.',
        D('Write "C / T = 5/8"'),
        'Divide by T: coaches over trainees is five eighths. A ratio is just a fraction.',
        'Or match the units directly: the numerator goes to the first thing, the denominator to the second.',
        D('Write the ratio "C : T = 5 : 8"'),
        'Five coaches for every eight trainees.',
        "But careful — they didn't ask coaches out of trainees. They asked out of everyone.",
    ], [
        'So plug in. Say there are eight trainees.',
        D('Write "T = 8  →  C = 5"'),
        'Five eighths of eight: five coaches.',
        D('Write "total = 13  →  5/13"'),
        'Everyone together: thirteen. Coaches: five out of thirteen.',
        D('Circle choice 4'),
        'Five thirteenths. Choice four.',
        'Five eighths is sitting there as a trap — that compares coaches with trainees, not with everyone.',
    ]])

    # ---------- Q17 wp22-g045: 4 times, 1/4 and 1/3 rejected -> 4/15   ==>   twice, 1/2 and 1/5 whole-wheat -> 2/5
    _rn_q(M, 'wp22-g045', 'A bakery sends twice as many loaves to supermarkets as to cafés. One half of the supermarket loaves and '
          'one fifth of the café loaves are whole-wheat. What fraction of all the loaves is whole-wheat?',
          ['$\\frac{2}{5}$', '$\\frac{1}{2}$', '$\\frac{7}{10}$', '$\\frac{1}{6}$'], 1, [
        'Only a fraction is asked. Plug in: 5 café loaves and $2\\cdot5=10$ supermarket loaves.',
        'Whole-wheat: $\\frac12\\cdot10=5$ and $\\frac15\\cdot5=1$. In all, 6 out of 15.',
        'The fraction that is whole-wheat is $\\frac{6}{15}=\\frac25$. Check: it is between $\\frac15$ and $\\frac12$ ✓.'])
    _rn_video(M, 'wp22-g045', [[
        'Two groups: supermarkets and cafés. Twice as many to the supermarkets.',
        'We could write x and two x. But plugging in numbers is more comfortable.',
        D('Write "cafés 1, supermarkets 2"'),
        'Try one loaf for the cafés, two for the supermarkets. Twice — good.',
        'Supermarkets: half are whole-wheat. Half of two is one. Fine.',
        "Cafés: a fifth are whole-wheat. A fifth of one loaf? That's no good.",
        "No problem — it's our substitution. We can change it.",
        'The cafés need a number a fifth can come out of: five.',
        A('A table appears: Cafés / Supermarkets — loaves, whole-wheat (blank)',
          _tbl(['', 'Loaves', 'Whole-wheat'], [['Cafés', '', ''], ['Supermarkets', '', ''], ['Total', '', '']], 760, 220)),
        D('Fill in: cafés 5 → 1 whole-wheat; supermarkets 10 → 5 whole-wheat'),
        'Cafés five, supermarkets ten — still twice. A fifth of five: one. Half of ten: five.',
        D('Fill in the total row: 15 loaves, 6 whole-wheat'),
        'Fifteen loaves, six whole-wheat.',
        D('Write "6/15 = 2/5" and circle choice 1'),
        'Six fifteenths — two fifths. Choice one.',
    ], [
        'Now psychometric thinking.',
        'If both groups were half whole-wheat, the whole lot would be a half.',
        'But one group is only a fifth — less than a half. So overall: less than a half.',
        D('Write "< 1/2" and cross out choices 2 and 3'),
        "Seven tenths is more than a half. A half itself isn't possible either. Both out.",
        'The other end: if both groups were a fifth whole-wheat, the whole would be a fifth.',
        'But one group is more — a half. So overall: more than a fifth.',
        D('Write "> 1/5" and cross out choice 4'),
        'One sixth is less than a fifth. Out.',
        D('Circle choice 1'),
        'Only two fifths is between a fifth and a half. Choice one.',
    ]], intro=('Two groups, two different rejection rates.', 'Two groups, two different fractions.'))

    # ---------- Q18 wp22-g046: 1/4 and 1/6 given away, 9 and 20 left -> 36   ==>   1/3 and 1/6 sold, 10 and 14 left -> 33
    _rn_q(M, 'wp22-g046', 'A baker has chocolate and vanilla cupcakes. She sells $\\frac13$ of the chocolate cupcakes and $\\frac16$ of the '
          'vanilla cupcakes, always selling whole cupcakes. The cupcakes left are 10 of one flavor and 14 of the other, in an unknown '
          'order. How many cupcakes did she have at first?',
          ['48', '26', '72', '33'], 4, [
        'Vanilla left $=\\frac56$ of the vanilla cupcakes: 5 times a whole number of sixths, therefore divisible by 5. 10 can be vanilla, 14 cannot.',
        'Vanilla: $\\frac56V=10$, therefore $V=12$. Chocolate: $\\frac23C=14$, therefore $C=21$.',
        'At first: $12+21=33$ cupcakes.'])
    _rn_video(M, 'wp22-g046', [[
        "Ten and fourteen are left — but which is chocolate and which is vanilla? We'll just test it.",
        'Suppose fourteen vanilla cupcakes are left.',
        D('Write "vanilla: 14 = 5/6 → 14 ÷ 5 = ?"'),
        'She sold a sixth of the vanilla. So, fourteen is five sixths. Each sixth would be fourteen over five.',
        "Not a whole number. But she sold whole cupcakes. So fourteen can't be the vanilla.",
        'Swap them: ten vanilla, fourteen chocolate.',
        D('Write "vanilla: 10 = 5/6 → 1/6 = 2 → 12"'),
        'Ten is five sixths. One sixth: two cupcakes. Give back the sixth — twelve vanilla.',
        D('Write "chocolate: 14 = 2/3 → 1/3 = 7 → 21"'),
        'Fourteen is two thirds. One third: seven cupcakes. Give it back — twenty-one chocolate.',
        D('Write "12 + 21 = 33" and circle choice 4'),
        'Twelve plus twenty-one: thirty-three. Choice four.',
    ], [
        "Now the psychometric way. We don't even care which pile is which.",
        D('Write "10 + 14 = 24 left"'),
        'Twenty-four cupcakes are left.',
        'Each flavor lost a third or a sixth. All together, she sold at most a third of the cupcakes — and at least a sixth.',
        D('Write "at most ⅓ gone: 24 ≥ ⅔ · start → start ≤ 24 · 3/2 = 36"'),
        'At most a third gone: twenty-four is at least two thirds of the start. The start is at most thirty-six.',
        D('Write "at least ⅙ gone: 24 ≤ ⅚ · start → start ≥ 24 · 6/5 = 28.8"'),
        'At least a sixth gone: twenty-four is at most five sixths of the start. The start is at least about twenty-nine.',
        D('Write "29 ≤ start ≤ 36"'),
        D('Cross out choices 1, 2 and 3'),
        'Forty-eight, twenty-six and seventy-two are all outside. Only thirty-three is between twenty-nine and thirty-six.',
        D('Circle choice 4'),
        'Choice four.',
    ]], intro=('which leftover belongs to which color.', 'which leftover belongs to which flavor.'))

    # ---------- Q19 wp22-g047: clubs 3 : 1, 3 move, then 2 : 1 -> 36   ==>   buses 4 : 1, 6 move, then 2 : 1 -> 45
    _rn_q(M, 'wp22-g047', 'A school has two buses. Bus A carries 4 times as many students as bus B. Six students move from bus A to bus B. '
          'Afterwards, bus B carries half as many students as bus A. How many students are on the two buses altogether?',
          ['40', '45', '48', '50'], 2, [
        'B $=x$, A $=4x$. After the move: B has $x+6$, A has $4x-6$.',
        'B is half of A: $2(x+6)=4x-6$, therefore $2x+12=4x-6$ and $x=9$.',
        'Total: $x+4x=5x=45$. (The move does not change the total.)'])
    _rn_video(M, 'wp22-g047', [[
        'Bus A has four times bus B.',
        D('Write "B = x,  A = 4x"'),
        'Give the plain x to the little guy: B is x, A is four x. No fractions, no dividing later.',
        'Six students move from A to B.',
        D('Write "B: x + 6,  A: 4x − 6"'),
        'Take six from A, add six to B.',
        'Now B is half of A.',
        D('Write "x + 6 = ½(4x − 6)"'),
        'x plus six equals half of — brackets! — four x minus six.',
        D('Write "2x + 12 = 4x − 6  →  x = 9"'),
        'Times two: two x plus twelve equals four x minus six. x is nine.',
        "Don't circle nine! That's not what they asked.",
        D('Write "total = 5x = 45" and circle choice 2'),
        'Both buses together: x plus four x — five x. Forty-five. Choice two.',
    ], [
        'Now the psychometric shortcut — understanding divisibility.',
        'Four times as many: four parts and one part. Five parts in total.',
        D('Write "total ÷ 5" and cross out choice 3'),
        "So the total must divide by five. Forty-eight doesn't. Out.",
        'After the move: B is half of A. One part and two parts — three parts.',
        D('Write "total ÷ 3" and cross out choices 1 and 4'),
        "So the total must also divide by three. Forty doesn't. Fifty doesn't.",
        D('Circle choice 2'),
        'Three answers gone without calculating anything. Forty-five. Choice two.',
    ]])

    # ---------- Q20 wp22-g048: fixed + per task, 10 -> 320, 6 -> 208 -> 28   ==>   fee + per hour, 7 h -> 385, 4 h -> 250 -> 45
    _rn_q(M, 'wp22-g048', 'A plumber charges a fixed call-out fee plus the same amount for each hour of work. A 7-hour job costs 385 credits, '
          'and a 4-hour job costs 250 credits. What is the charge per hour?',
          ['35', '45', '65', '50'], 2, [
        'What changed? $7-4=3$ more hours and $385-250=135$ more credits.',
        'Per hour: $\\frac{135}{3}=45$ credits. The fixed fee is the same in both jobs, and it cancels.'])
    _rn_video(M, 'wp22-g048', [[
        'Start with the quickest idea.',
        "What's the difference between the two jobs?",
        D('Write "7 − 4 = 3 hours"'),
        'Three more hours.',
        D('Write "385 − 250 = 135"'),
        'And a hundred thirty-five more credits.',
        D('Write "135 ÷ 3 = 45"'),
        'Three hours earned a hundred thirty-five extra. One hour: forty-five.',
        D('Circle choice 2'),
        'Choice two. The fixed fee is the same in both jobs — it just disappears.',
    ], [
        'A fixed fee, plus a fixed charge per hour.',
        D('Write "f + 7h = 385" and under it "f + 4h = 250"'),
        'Job one: fee plus seven hours, three-eighty-five. Job two: fee plus four hours, two-fifty.',
        D('Subtract: write "3h = 135"'),
        'Subtract the equations. The fee cancels. Three h equals a hundred thirty-five.',
        D('Write "h = 45" and circle choice 2'),
        'Divide by three: forty-five per hour. Choice two.',
    ], [
        "Can't see the equation? Plug in the answers.",
        'Use the job with fewer hours — four. Easier to calculate.',
        D('Next to choice 3 write "65 · 4 = 260 > 250" and cross it out'),
        'Sixty-five an hour: four hours already make two-sixty. But the whole bill was two-fifty. Impossible.',
        D('Next to choice 4 write "50 · 4 = 200 → fee 50"'),
        'Fifty: four hours, two hundred. Fee: fifty. Check the other job.',
        D('Write "50 · 7 = 350 → fee 35" and cross out choice 4'),
        "Seven hours: three-fifty — fee thirty-five. Thirty-five isn't fifty. Out.",
        D('Next to choice 2 write "45 · 4 = 180 → fee 70"'),
        'Forty-five: four hours, one-eighty. Fee: seventy.',
        D('Write "45 · 7 = 315 → fee 70 ✓" and circle choice 2'),
        'Seven hours: three-fifteen. Fee: seventy again. Same in both jobs — choice two.',
    ]])

    # ---------- Q21 wp22-g049: 8 large + 12 small = 1,000 g, 10 + 15 -> 1,250   ==>   9 large + 6 small = 240 kg, 12 + 8 -> 320
    _rn_q(M, 'wp22-g049', 'Nine large crates and six small crates weigh 240 kg altogether. All large crates weigh the same, and all small '
          'crates weigh the same. How much do twelve large and eight small crates weigh?',
          ['300', '320', '280', '360'], 2, [
        '$9\\to12$ and $6\\to8$: both counts are multiplied by $\\frac43$.',
        'Every part grows by the same factor. The weight grows the same way: $240\\cdot\\frac43=320$ kg.',
        'We cannot find one crate alone (one equation, two unknowns), but we do not need to.'])
    _rn_video(M, 'wp22-g049', [[
        'If a large and a small crate weigh something together — can we know each one alone? No. Many options.',
        'But double both of them? Then the weight doubles too. That we can know.',
        "Change only one of them — then we can't.",
        'So the question is: did both counts grow by the same factor?',
        D('Write "9 → 12: ×4/3"'),
        'Nine to twelve: a third of nine is three. Up by a third — times one and a third.',
        D('Write "6 → 8: ×4/3"'),
        'Six to eight: a third of six is two. Same factor.',
        'Both grew the same way. So, the weight grows the same way.',
        D('Write "240 · 4/3 = 320" and circle choice 2'),
        'Two-forty, plus a third of it — eighty more: three-twenty. Choice two.',
    ], [
        'Prefer whole numbers? Shrink the equation first — all of it.',
        D('Write "9L + 6S = 240" then "÷3 → 3L + 2S = 80"'),
        'Everything divided by three: three large and two small weigh eighty.',
        D('Write "×4 → 12L + 8S = 320"'),
        'Times four: twelve large and eight small. Eighty times four — three-twenty.',
        "Same ratio on both sides. So, it's allowed.",
    ]])

    # ---------- Q22 wp22-g050: 60 counters, gives 9, equal -> 13/7   ==>   70 stickers, gives 15, equal -> 5/2
    _rn_q(M, 'wp22-g050', 'Noa and Eli have 70 stickers altogether. Noa gives Eli 15 stickers, and then they have the same number. '
          'What was Noa’s original number of stickers divided by Eli’s original number?',
          ['$\\frac{10}{7}$', '$\\frac{2}{5}$', '$\\frac{5}{2}$', '$2$'], 3, [
        'The total stays 70. Equal at the end: 35 and 35.',
        'Go back: Noa had $35+15=50$ and Eli had $35-15=20$.',
        '$\\frac{50}{20}=\\frac52$.'])
    _rn_video(M, 'wp22-g050', [[
        'Noa and Eli have seventy together.',
        D('Write "n + e = 70"'),
        "Noa gives Eli fifteen — then they're equal.",
        D('Write "n − 15 = e + 15  →  n − e = 30"'),
        'Noa minus fifteen equals Eli plus fifteen. Move terms: n minus e is thirty.',
        D('Add the equations: write "2n = 100 → n = 50, e = 20"'),
        'Add the two equations: two n is a hundred. Noa: fifty. Eli: twenty.',
        D('Write "50/20 = 5/2" and circle choice 3'),
        'Fifty over twenty — divide both by ten: five halves. Choice three.',
    ], [
        "Now the psychometric way. It's easier to start from the end.",
        "What happens at the end? They're equal — and the total is still seventy.",
        D('Write "end: 35 and 35"'),
        "So at the end: thirty-five and thirty-five. That's the only way.",
        'Now go back in time. Give Noa back her fifteen.',
        D('Write "start: 35 + 15 = 50,  35 − 15 = 20"'),
        'Noa had fifty. Eli had fifteen fewer: twenty.',
        D('Write "5/2" and circle choice 3'),
        'Five halves. Choice three.',
        'Some questions are easier from the end. When the ending is simple — start there.',
    ]])


def rn_practice_questions(M):
    S = lambda *a: _rn_q(M, *a)
    P = lambda n: 'wp22-p%02d' % n
    S(P(3), 'A cargo boat can sail 900 km while carrying 50 tons. Each extra ton reduces its range by 6 km. '
      'What is its range when carrying 87 tons?',
      ['522', '678', '222', '378'], 2, [
        'Extra load: $87-50=37$ tons.', 'Lost range: $37\\cdot6=222$ km.', 'Range: $900-222=678$ km.'])
    S(P(4), 'Three families of 2, 5, and 6 people share a 780-credit cabin rental in proportion to family size. '
      'How much does the five-person family pay?',
      ['260', '300', '360', '156'], 2, [
        'Total people: $2+5+6=13$.', 'Per person: $\\frac{780}{13}=60$ credits.',
        'The five-person family pays $5\\cdot60=300$ credits.'])
    S(P(8), 'An office has $n$ cabinets. Each cabinet has $n$ drawers, and each drawer holds 3 folders. How many folders are there?',
      ['$n^3$', '$3n$', '$n^2+3$', '$3n^2$'], 4, [
        'Drawers: $n\\cdot n=n^2$. Folders: $3\\cdot n^2=3n^2$.',
        'Check with $n=2$: 2 cabinets of 2 drawers is 4 drawers and 12 folders. $3\\cdot2^2=12$ ✓.'])
    S(P(12), 'One gold coin equals 6 silver coins. One gold coin is worth $\\frac34$ of a platinum coin. '
      'How many silver coins are worth one platinum coin?',
      ['8', '2', '24', '12'], 1, [
        'One gold coin $=6$ silver coins $=\\frac34$ platinum coin.',
        '$\\frac14$ platinum coin $=\\frac63=2$ silver coins. One platinum coin $=4\\cdot2=8$ silver coins.'])
    S(P(7), 'Omer puts $\\frac25$ of his bonus into savings, then spends 150 credits on a jacket. He has 450 credits left. '
      'What was his bonus?',
      ['840', '600', '1,000', '1,500'], 3, [
        'Before buying the jacket he had $450+150=600$ credits.',
        'That is the $\\frac35$ left after the savings: $\\frac35B=600$, therefore $B=600\\cdot\\frac53=1{,}000$.'])
    S(P(14), 'A bottle of syrup holds 50 portions and costs 15 credits. A bag of coffee holds 400 portions and costs 24 credits. '
      'What is the ingredient cost of an iced coffee made with 2 portions of syrup and 3 portions of coffee?',
      ['1.02 credits', '0.36 credits', '0.66 credits', '0.78 credits'], 4, [
        'Syrup: $\\frac{15}{50}=0.30$ credits a portion. Coffee: $\\frac{24}{400}=0.06$ credits a portion.',
        'Drink: $2\\cdot0.30+3\\cdot0.06=0.60+0.18=0.78$ credits.'])
    S(P(6), 'A large pizza costs 12 credits more than a small pizza. Three large pizzas cost the same as five small pizzas. '
      'What does one large pizza cost?',
      ['18', '36', '30', '24'], 3, [
        'Small pizza $=s$, large pizza $=s+12$.',
        'Three large pizzas cost the same as five small ones: $3(s+12)=5s$.',
        '$3s+36=5s$, therefore $2s=36$ and $s=18$. Large pizza: $18+12=30$ credits.'])
    S(P(2), 'A garden has roses, tulips, and lilies. There are 4 times as many roses as tulips, and 3 times as many tulips as lilies. '
      'Which could be the total number of flowers?',
      ['36', '40', '48', '56'], 3, [
        'Lilies $=x$, tulips $=3x$, roses $=4\\cdot3x=12x$.',
        'Total: $x+3x+12x=16x$. The total must divide by 16.',
        'Only $48=16\\cdot3$ works. (40 and 56 come from adding $1+3+4=8$ — the 4 is times the tulips, not times the lilies.)'])
    S(P(10), 'Four coats cost as much as three jackets and eight scarves. A jacket costs 4 times as much as a scarf. '
      'How many jackets cost as much as twelve coats?',
      ['20', '9', '17', '15'], 4, [
        'Scarf $=1$ unit, jacket $=4$ units.',
        'Four coats $=3\\cdot4+8\\cdot1=20$ units. Twelve coats $=60$ units.',
        'Jackets: $\\frac{60}{4}=15$.'])
    S(P(22), 'At a concert, there are $\\frac78$ as many adults as children. What fraction of the audience are adults?',
      ['$\\frac{8}{15}$', '$\\frac{7}{15}$', '$\\frac{7}{8}$', '$\\frac{1}{8}$'], 2, [
        'Plug in: 8 children and $\\frac78\\cdot8=7$ adults.',
        'The whole audience: $8+7=15$.',
        'Adults out of the audience: $\\frac{7}{15}$. (The denominator must include both groups.)'])
    S(P(16), 'A father is 30 years older than his daughter. The ratio of their ages now is $6:1$. '
      'What will the ratio of the father’s age to the daughter’s age be in 9 years?',
      ['$6:1$', '$3:2$', '$3:1$', '$4:1$'], 3, [
        'Father $=6u$, daughter $=u$. The gap: $6u-u=5u=30$, therefore $u=6$.',
        'Now: 36 and 6. In 9 years: 45 and 15.',
        'The ratio is $45:15=3:1$.'])
    S(P(25), 'Gal and Ron have 40 marbles altogether. Gal gives Ron 7 marbles and then has 6 fewer than Ron. '
      'What was the ratio of Gal’s marbles to Ron’s before the transfer?',
      ['$17:23$', '$2:3$', '$3:2$', '$5:3$'], 3, [
        'The gap: every marble Gal gives changes the gap by 2. She gives 7, therefore the gap moves $2\\cdot7=14$ toward Ron.',
        'After the transfer Ron is 6 ahead. Before it, Gal was $14-6=8$ ahead.',
        'Together 40, Gal 8 more: Gal $\\frac{40+8}{2}=24$ and Ron $40-24=16$.',
        'With an equation: after the transfer Gal $=x$ and Ron $=x+6$. $2x+6=40$, $x=17$: 17 and 23. Before: $17+7=24$ and $23-7=16$.',
        'The ratio is $24:16=3:2$.'])
    S(P(15), 'For 8 days, a squirrel collects 30 nuts a day and eats $x$ of them each day. The nuts it saves then last 16 days '
      'at 5 nuts a day. What is $x$?',
      ['10', '20', '5', '16'], 2, [
        'Saved nuts: $16\\cdot5=80$.',
        'Collected: $8\\cdot30=240$. Eaten in 8 days: $240-80=160$.',
        '$x=\\frac{160}{8}=20$.'])
    S(P(20), 'A textbook has 72,000 words and 60 pictures. A brochure has 3,000 words and 20 pictures. '
      'The word-to-picture ratio of the textbook is how many times that of the brochure?',
      ['3', '24', '8', '6'], 3, [
        'Textbook: $\\frac{72{,}000}{60}=1{,}200$ words per picture. Brochure: $\\frac{3{,}000}{20}=150$ words per picture.',
        '$\\frac{1{,}200}{150}=8$.'])
    S(P(21), 'A furniture shop has 45 three-legged stools and four-legged chairs altogether. Together they have 158 legs. '
      'How many chairs are there?',
      ['22', '23', '26', '19'], 2, [
        'Assume all 45 are stools: $45\\cdot3=135$ legs.',
        'Missing: $158-135=23$. Each chair adds $4-3=1$.',
        'Chairs: 23. Check: $22\\cdot3+23\\cdot4=66+92=158$ ✓.'])
    S(P(19), 'At the end of each of 3 days, a water tank loses $\\frac15$ of the water that is in it. '
      'What fraction of the starting water is left after the third day?',
      ['$\\frac{2}{5}$', '$\\frac{16}{25}$', '$\\frac{64}{125}$', '$\\frac{4}{5}$'], 3, [
        'Each day $\\frac45$ of the water that is there stays.',
        'After three days: $\\frac45\\cdot\\frac45\\cdot\\frac45=\\frac{64}{125}$.',
        'Not $1-3\\cdot\\frac15=\\frac25$: each fifth is taken from a smaller amount.'])
    S(P(13), 'A farmer sells $\\frac14$ of her melons, then $\\frac23$ of the melons left. Every melon has the same price. '
      'These sales bring in 480 credits. How much would selling all the melons bring in?',
      ['720', '640', '960', '600'], 2, [
        'After the first sale, $1-\\frac14=\\frac34$ of the melons are left. Two thirds of them: $\\frac23\\cdot\\frac34=\\frac12$.',
        'Sold: $\\frac14+\\frac12=\\frac34$ of the melons, for 480 credits.',
        'All the melons: $480\\cdot\\frac43=640$ credits.'])
    S(P(1), 'A small bottle costs $x$ credits. A large bottle costs $\\frac{x^2+45}{x}$ credits. The large bottle costs 6 times '
      'as much as the small one. How much does the small bottle cost?',
      ['9', '3', '5', '6'], 2, [
        'Six times the small price is $6x$: $\\frac{x^2+45}{x}=6x$.',
        'A price is positive. Multiply both sides by $x$: $x^2+45=6x^2$.',
        'Therefore $5x^2=45$, $x^2=9$ and $x=3$ (a price cannot be $-3$).'])
    S(P(5), 'Yael has $n$ whole cookies. She eats 5, gives half of the remaining cookies to her brother, and packs 4 whole cookies '
      'in a lunch box. Which of the following could be the value of $n$?',
      ['14', '16', '15', '12'], 3, [
        'After eating 5, she has $n-5$ cookies. Half of them must be a whole number. Therefore $n-5$ is even, and $n$ is odd.',
        'Only 15 is odd. Check: $15-5=10$. She gives away 5, keeps 5 and packs 4 ✓.'])
    S(P(9), 'One large jug holds $\\frac43$ as much water as one small jug. Which set of jugs holds the most water?',
      ['5 large and 3 small', '7 large', '4 large and 5 small', '10 small'], 3, [
        'Plug in: a small jug holds 3 units, a large jug holds 4 units ($\\frac43$ of 3).',
        '(1) $5\\cdot4+3\\cdot3=29$. (2) $7\\cdot4=28$. (3) $4\\cdot4+5\\cdot3=31$. (4) $10\\cdot3=30$.',
        'Choice (3), 4 large and 5 small, holds the most: 31 units.'])
    S(P(11), 'Tamar chooses a real number $x$, divides it by 6, subtracts 5, multiplies by 4, and adds 20. '
      'The result is $x$ again. What is $x$?',
      ['0', '6', '30', '12'], 1, [
        '$4\\left(\\frac{x}{6}-5\\right)+20=\\frac{4x}{6}-20+20=\\frac23x$.',
        '$\\frac23x=x$, therefore $\\frac13x=0$ and $x=0$.'])
    S(P(23), 'Ben starts work at 7 a.m. on each of four days. On two of those days he takes an unpaid half-hour break. '
      'He finishes at the same time every day and works 31 paid hours in total. When does he finish?',
      ['2:45 p.m.', '3:15 p.m.', '3 p.m.', '3:30 p.m.'], 3, [
        'Time at work: $31+1=32$ hours (31 paid hours and two unpaid half-hour breaks).',
        'Each day: $\\frac{32}{4}=8$ hours.',
        'Eight hours after 7 a.m. is 3 p.m.'])
    S(P(17), 'One kilogram of coffee costs $x$ credits, and one kilogram of tea costs $y$ credits. The two prices add up to 20 credits, '
      'and coffee costs 4 credits more than tea. A shop sells $x$ kilograms of coffee (as many kilograms as the price of one kilogram) '
      'and buys $y$ kilograms of tea. What is the difference between the money received and the money spent?',
      ['144', '80', '96', '48'], 2, [
        'Write the two conditions:\n$\\begin{cases} x+y=20 \\\\ x-y=4 \\end{cases}$\nAdd them: $2x=24$, therefore $x=12$ and $y=8$.',
        'Received: $12\\cdot12=144$. Spent: $8\\cdot8=64$.',
        'Difference: $144-64=80$ credits.'])
    S(P(29), 'Two schools receive the same number of tablets. One school shares its tablets equally among 6 classes, and the other '
      'among 30 classes. Each class in the first school receives 5 times as many tablets as each class in the second. '
      'How many tablets does each school receive?',
      ['60', CANNOT, '30', '150'], 2, [
        'Call the number of tablets $t$. First school: $\\frac{t}{6}$ per class. Second school: $\\frac{t}{30}$ per class.',
        '$\\frac{t}{6}=5\\cdot\\frac{t}{30}$ is true for every $t$. The last sentence gives no new information.',
        'Nothing fixes $t$. It cannot be determined.',
        'Shortcut · Pick values that fit: $t=30$ gives $5$ and $1$ tablets per class ✓, and $t=60$ gives $10$ and $2$ ✓. '
        'Two different numbers fit everything, therefore it cannot be determined.'])
    S(P(26), 'Rina borrows some money and spends $\\frac38$ of it on flour. She repays her lender with $\\frac23$ of that flour at its '
      'purchase value. She still owes 7.50 credits. How much did she borrow?',
      ['12', '8', '10', '15'], 3, [
        'Repaid with flour: $\\frac23\\cdot\\frac38=\\frac14$ of the loan.',
        'Still owed: $\\frac34$ of the loan $=7.50$.',
        '$\\frac14$ of the loan $=\\frac{7.50}{3}=2.50$. The loan: $4\\cdot2.50=10$ credits.'])
    S(P(28), 'A teacher splits a box of pencils between two classes. Class A uses $\\frac15$ of its pencils, and class B uses '
      '$\\frac14$ of its pencils. The two classes have 16 and 21 pencils left, in an unknown order. How many pencils were in the box?',
      ['37', '44', '48', '52'], 3, [
        'What is left in class B is $\\frac34$ of its pencils, therefore it must be divisible by 3. 21 is divisible by 3, 16 is not.',
        'Class B: $\\frac34B=21$, therefore $B=21\\cdot\\frac43=28$.',
        'Class A: $\\frac45A=16$, therefore $A=16\\cdot\\frac54=20$.',
        'In the box: $20+28=48$ pencils.'])
    S(P(24), 'A tall candle has a red stripe that is $\\frac25$ of its length. A short candle has a red stripe that is $\\frac13$ of '
      'its length. The tall candle’s stripe is 6 times as long as the short candle’s stripe. What is the ratio of the candles’ lengths?',
      ['$6:1$', '$5:1$', '$6:5$', '$36:5$'], 2, [
        'The tall candle is $L$ long and the short one $S$: $\\frac25L=6\\cdot\\frac13S$.',
        'Multiply by 15: $6L=30S$, therefore $L=5S$.',
        'The ratio of the lengths is $L:S=5:1$.'])
    S(P(27), 'A teacher changes every grade by multiplying it by $\\frac34$ and then adding 20. Lior’s grade goes down. '
      'Which of the following is necessarily true of her original grade?',
      ['It was less than 80', 'It was greater than 80', 'It was less than 20', 'It was exactly 80'], 2, [
        'Unchanged grade: $\\frac34x+20=x$, therefore $\\frac14x=20$ and $x=80$.',
        'Grade goes down: $\\frac34x+20<x$, therefore $20<\\frac14x$ and $x>80$.',
        'Check: $x=100$ gives $75+20=95<100$ ✓. $x=60$ gives $45+20=65>60$.'])
    S(P(18), 'Four positive numbers are arranged in a square of two rows and two columns: $p$ and $q$ in the top row, $r$ and $s$ in '
      'the bottom row, with $p$ above $r$. The two row totals are equal, and the two column totals are equal. '
      'Which of the following statements is necessarily true?',
      ['$p=s\\text{ and }q=r$', '$p=q=r=s$', '$ps=qr$', '$p+s=q+r$'], 1, [
        'Rows equal and columns equal:\n$\\begin{cases} p+q=r+s \\\\ p+r=q+s \\end{cases}$',
        'Subtract the second equation from the first: $q-r=r-q$, therefore $2q=2r$ and $q=r$.',
        'Put $q=r$ into $p+q=r+s$: $p=s$.',
        'Shortcut · Pick values that fit: two equations and four letters, therefore numbers that fit the givens are enough to test '
        'the choices. $p=1$, $q=2$, $r=2$, $s=1$: rows $1+2=2+1$ ✓, columns $1+2=2+1$ ✓. Choice 2: $1=2$ ✗. '
        'Choice 3: $ps=1$ but $qr=4$ ✗. Choice 4: $p+s=2$ but $q+r=4$ ✗. Only choice 1 is left.'])
    S(P(30), 'There are $n$ children in a room, where $n\\ge4$. Each child starts with $3n$ stickers. The children leave the room '
      'one at a time. Just before leaving, a child gives 3 stickers to every other child still in the room. How many stickers '
      'does the fourth child to leave have left after giving out his stickers, as he leaves?',
      ['$3n+9$', '12', '21', '$3n-12$'], 3, [
        'The first three children each give the fourth child 3 stickers: $+9$. Before he gives, he has $3n+9$.',
        'When he leaves, $n-4$ other children are still in the room. He gives each of them 3 stickers: $-3(n-4)$.',
        '$3n+9-3(n-4)=3n+9-3n+12=21$.',
        'Check with $n=4$: he starts with 12, gets 9, and gives nothing (nobody is left): 21 ✓.'])


def rn_practice(M):
    """Approved clean-up: copies out, at most 3 extra-bank warm-ups, September items whose type the Hebrew covers out."""
    N = lambda k: 'q-r26-t22-' + k
    P = lambda n: 'wp22-p%02d' % n
    out = [
        # copy (practice_audit/copies_by_topic.txt, checked): same story and structure as the kept N('16') (notebooks and
        # pens, one equation, asked another combination); the "it is a multiple" case is the lesson's own example (4a + 6p)
        N('17'),
        # extra-bank warm-ups beyond 3 (kept: p34 ages "3 times then 2 times", p35 blend - the unchanged part,
        # p37 "4 adult tickets cost as 7 child tickets" - costs-the-same-as substitution)
        P(31),              # ratio 5 : 7, 18 added, equal: one part changes - p35 and guided Q9
        P(32),              # two price plans equal: build an equation - p06, guided Q10
        P(33),              # tank 3/5 -> 4/5 after 28 L: part of a whole - p13, p07
        P(36),              # train / bus +7, assume all the same - p21, guided Q24
        # September items of a type the Hebrew practice (or a kept item) already covers
        N('07'),            # 5 : 2 and 1.5 times, shared letter - kept N('06'), guided Q8
        N('09'),            # machines break down: inverse proportion - kept N('08'), guided Q3
        N('10'),            # letters in the choices (m members) - p08, p30
        N('11'),            # letters in the choices (n boxes of k) - p08, p30
        N('12'),            # test scoring, assume all the same - p21
        N('13'),            # ratio 4 : 3, girls join, equal - p35, guided Q9
        N('14'),            # buses, round up - kept N('15') ("or part of")
        N('18'),            # ratio 5 : 6 -> 1 : 2, both parts change - p16, p25
        N('19'),            # profit shared 6 : 3 : 2 from "times" - p02
    ]
    for qid in out:
        if qid in M.D['questions'] and any(f['ref'] == qid for f in M.D['flow']) and M.section_of(qid) == PRAC:
            M.unplace(qid)
    M.practice_order(PRAC, [
        P(3), P(4), P(8), P(12), P(7), P(14), P(37), N('08'), N('06'), P(6), P(2), P(10), P(22), P(16), P(25),
        P(15), P(20), P(21), P(19), P(13), P(35), N('15'), P(1), P(5), P(9), P(11), P(23), P(34), P(17), N('16'),
        P(29), P(26), P(28), P(24), P(27), P(18), P(30)])


def rn_titles(M):
    """Solution videos: title and slide description show the new stems."""
    for f in M.D['flow']:
        if f['topic'] != TOPIC or f['type'] != 'video': continue
        v = M.video(f['ref']); qid = v.get('questionId')
        if not qid or not qid.startswith('wp22-g') or f['ref'] in RN_RECORDED: continue
        stem = M.q(qid)['stem']
        v['title'] = v['navLabel'] = stem
        for b in v['beats']:
            if b['mode'] == 'question':
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (qid, stem)
        M.touched_videos.add(f['ref'])


def renumber_pass(M):
    rn_lessons(M)
    rn_guided(M)
    rn_practice_questions(M)
    rn_practice(M)
    rn_titles(M)


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
    # ---- Power count (topic 5) ----
    _sp_line(M, 'wp22-p08', r'Method 2 · Power count: $n$ cabinets times $n$ drawers times $3$ folders has power $2$ (the number $3$ does not count). The choices: $n^3$ has power $3$, $3n$ power $1$, and $n^2+3$ is mixed. Only $3n^2$ has power $2$.')
    # ---- Two moves (topic 12) ----
    _sp_line(M, 'wp22-p27', r'Method 2 · Two moves: endpoint $\frac34x+20=x$ gives $x=80$. Direction: the grade goes down means $\frac34x+20<x$. Test $x=0$: $20<0$ is false, therefore the answer is the side without $0$: $x>80$.')
    # ---- later-topic methods, written as self-contained shortcuts ----
    _sp_line(M, 'wp22-g045', r'Shortcut · Percent shares as weights: $\frac23$ of the loaves (the supermarket ones) are $\frac12$ whole-wheat, and $\frac13$ are $\frac15$ whole-wheat. The mix moves $\frac23$ of the way from $\frac15$ toward $\frac12$: $\frac15+\frac23\cdot\left(\frac12-\frac15\right)=\frac15+\frac15=\frac25$.')
    _sp_line(M, 'wp22-p24', r'Shortcut · Flip rule: $\frac25$ of $L$ is the same length as $6\cdot\frac13=2$ times $S$. The same part, therefore the wholes are in the flipped ratio: $L:S=2:\frac25=5:1$. A small fraction needs a big whole.')
    _sp_line(M, 'wp22-p20', r'Shortcut · Compare by factors: the textbook has $\frac{72{,}000}{3{,}000}=24$ times the words (the words-per-picture grows the same way) and $\frac{60}{20}=3$ times the pictures (the opposite way, therefore divide). $24\div3=8$.')


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
    # Topic 22 (day 12) comes before topic 5 (power count, day 13) and topic 12 (two moves, day 20) in the plan.
    _po_line(M, 'wp22-p08', 'Method 2 · Power count:', "Shortcut · Power count: the power of an expression is how many letters are multiplied in it (a number in front counts $0$). The answer is the same expression as the story, so it must have the story's power. $n$ cabinets times $n$ drawers times $3$ folders has power $2$. The choices: $n^3$ has power $3$, $3n$ power $1$, and $n^2+3$ is mixed (powers $2$ and $0$). Only $3n^2$ has power $2$.")
    _po_line(M, 'wp22-p27', 'Method 2 · Two moves:', "Shortcut · Two moves: an inequality's answer is everything on one side of a point. Find the point (where the two sides are equal), then test one easy number to see which side. Point: $\\frac34x+20=x$ gives $x=80$. Side: the grade goes down means $\\frac34x+20<x$. Test $x=0$: $20<0$ is false, therefore the answer is the side without $0$: $x>80$.")
    # "Pick values that fit" is taught in topic 51 (day 6), before topic 22: a normal method line.
    _po_relabel(M, 'wp22-p18', 'Shortcut · Pick values that fit:', 'Pick values that fit')
    _po_relabel(M, 'wp22-p29', 'Shortcut · Pick values that fit:', 'Pick values that fit')


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
    _mn_load().method_names(M, 22)   # 2026-10-07 method names: runs last


# =====================================================================================================================
# 2026-10-08 Hebrew points restored. The 2026-10-05 cut kept only short intros; two points of the teacher's Hebrew
# lessons were no longer taught: the general tip "let x be what they ask" (Hebrew "בניית משוואה") and the closing
# remark of "יחסים זהים" (if the triangle value hasn't sunk in yet - fine, we use it so much it will). Runs LAST.
# Helpers: _hebrew_back.py (a video recorded before its CUTOFF is not changed). See t22_CHANGES.md.
# =====================================================================================================================
import importlib.util as _ilu_hb, os as _os_hb
_s_hb = _ilu_hb.spec_from_file_location('_hebrew_back', _os_hb.path.join(_os_hb.path.dirname(_os_hb.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu_hb.module_from_spec(_s_hb); _s_hb.loader.exec_module(HB)


def hebrew_points_back(M):
    # lesson "Build the Equation" (wp-037): x = what they ask (most questions are built that way)
    if not HB.add_lines(M, 'wp-037', 'Equations everywhere', 'The method never changes', [
            A("'Tip: let x be what they ask' appears", T('Tip: let $x$ be what they ask', size=40)),
            "A small tip: in most cases, let x be the thing they ask for. Not always — but most questions are built that way. Then when you find x, you have the answer."]):
        HB.add_expl(M, 'wp22-g038', 'Tip: in most cases, let $x$ be what they ask. Most questions are built so that $x$ is then the final answer.')
    # Q2 (g030), end of "Cross-multiply": the reassurance that closes the Hebrew equal-ratios lesson
    if not HB.add_lines(M, 'solve-wp22-g030', 'Cross-multiply', 'Triangle value or cross-multiplying', [
            "Hasn't it sunk in yet? That's fine. We'll use it so often — in word problems, geometry and algebra — that it will."]):
        HB.add_expl(M, 'wp22-g030', 'The triangle value comes back all through the course — word problems, geometry and algebra.')


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
    # #46 (Hebrew 1701-1718): "the ratio between A and B" - keep the lesson (the English exam uses this wording),
    # but no claim that the exam tests it as a deliberate trap (teacher decision 2026-10-08)
    _cf_replace(M, 'wp-034', 'A ratio is a fraction', 'The exam does test this',
                "The exam uses this wording — so always match the names to the numbers in order.")
    c = M.card('mem-ratios')
    k = [i for i, t in enumerate(c['tips']) if t.startswith('Read in order:')]
    assert len(k) == 1, k
    c['tips'][k[0]] = 'Read in order: match the names to the numbers in order. The first name goes with the first number.'


_apply_before_coverage_fixes = apply


def apply(M):
    _apply_before_coverage_fixes(M)
    coverage_fixes(M)   # 2026-10-08 coverage fixes: runs LAST
