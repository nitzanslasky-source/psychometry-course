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
    _cleanup_videos(M)
    _fix_sidebars(M)
    summary(M)


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
            A("'x = 9, asked for 2x → 18' appears", T('$x=9$, but they ask for $2x$ $\\to$ $18$', size=46)),
            "x is nine, and they ask for twice the number? The answer is eighteen.",
            "Tip: let x be the thing they ask for."]),
        C(1, [
            A("'6 more: A = B + 6' appears", T('$A$ is $6$ more than $B$: $\\ A=B+6$', size=44)),
            "More and less: plus and minus.",
            A("'3 times: A = 3B' appears", T('$A$ is $3$ times $B$: $\\ A=3B$', size=44)),
            "Three times is not three more.",
            A("'One quarter less than n: 3/4 n · \"of\" = ×' appears",
              T('One quarter less than $n$: $\\ \\frac34n$ ("of" means $\\times$)', size=44)),
            "Of means times. A quarter less leaves three quarters.",
            A("'3 notebooks cost the same as 5 pens: 3N = 5P' appears",
              T('$3$ notebooks cost the same as $5$ pens: $3N=5P$', size=42)),
            "Is, makes up, costs the same as: all equals signs. Translate one phrase at a time."]),
        C(2, [
            A("'Across or down is whole? Use that multiplier' appears",
              T('Across or down is a whole number? Use that multiplier', size=40)),
            "Put the data in a ratio table. Across or down is a whole number? Use that multiplier.",
            A("'Triangle value: 8 · 15 ÷ 6 = 20' appears",
              T('Not whole? Triangle value: $\\frac{8\\cdot15}{6}=20$', size=46)),
            "Not whole? The triangle value: multiply along the diagonal, then divide by what's left.",
            "Or cross-multiply — the same answer.",
            "And a sense check first: should the answer be bigger or smaller?"]),
        C(3, [
            A("'Workers × days stays the same' appears", T('Same job: workers $\\times$ days stays the same', size=44)),
            "One goes up and the other goes down? That's inverse. The product stays the same.",
            A("'6 · 10 = 60 = 4 · 15' appears", T('$6\\cdot10=60=4\\cdot15$', size=54)),
            "Six workers, ten days: sixty worker-days. Four workers need fifteen days.",
            "The ratio table here gives fewer days with fewer workers. Impossible — so ask: more or less?"]),
        C(4, [
            A("'Ratio 3 : 5 → 3x and 5x' appears", T('Ratio $3:5$ $\\to$ $3x$ and $5x$', size=48)),
            "A ratio is a fraction. Read it in order: the first name goes with the first number.",
            "A ratio alone gives no amounts. Write three x and five x.",
            A("'3/8 of all → part 3x, all 8x' appears", T('$\\frac38$ of all $\\to$ part $3x$, all $8x$', size=46)),
            "Three eighths of all? The part is three x, and all of them is eight x.",
            A("'3N = 5P → ratio N : P = 5 : 3' appears", T('$3N=5P$ $\\to$ ratio $N:P=5:3$ (reversed)', size=44)),
            "Costs the same as? Reversed: notebook to pen is five to three.",
            "Counting people? x is a whole number — the total divides by the sum of the ratio numbers."]),
        C(5, [
            A("'Ratio A : B = 2 : 3 = 8 : 12, B : C = 4 : 5 = 12 : 15' appears",
              T('Ratios $A:B=2:3=8:12$ and $B:C=4:5=12:15$', size=42)),
            "Two ratios share a letter? Make it the same number in both. A to B to C: eight, twelve, fifteen.",
            "Not two to three to five — the three and the four are not the same B.",
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
            A("'Enough for 4, not for 5: 4B ≤ 50 and 5B > 50' appears",
              T('Enough for $4$, not for $5$: $\\ 4B\\le50$ and $5B>50$', size=42)),
            "Enough — but not enough? Two inequalities. The answer is a range: more than ten, at most twelve and a half.",
            A("'\"Or part of\" → round UP' appears", T('"Or part of" $\\to$ round UP: $50$ people, vans of $12$ $\\to$ $5$ vans', size=40)),
            "Or part of? Round up. Two people left over still need a van.",
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
