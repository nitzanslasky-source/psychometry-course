"""Topic 24 - Overlapping groups. Fixes from student_review/review_t23-24.md (Topic 24 part) and PLAN.md.
See t24_CHANGES.md for the plain-language list."""
import re
from dsl import T, H, A, D, Q
from math_api import _word, rich_plain

TOPIC = 24
L1, L2, L3 = 'wp-067', 'wp-068', 'wp-069'
LEARN, ADV, PRAC = 'wp24-learn', 'wp24-advanced', 'wp24-practice'
STRIP_SE = {'k': 'vis', 'v': {'type': 'table', 'headers': ['Neither', 'Spanish only', 'Both', 'French only'],
                              'rows': [['4', '5', '5', '4']]}, 'w': 1000, 'h': 120}
# advanced-group sidebar; 'Question 9' is the new guided question placed after Question 5
# (renumber_guided turns this into Question 4..9 in course order)
ADV_SIDEBAR = ['Question 4', 'Question 5', 'Question 9', 'Question 6', 'Question 7', 'Question 8']
US = [('organiser', 'organizer'), ('Organiser', 'Organizer'), ('flavours', 'types'), ('recognise', 'recognize'),
      ('torch', 'flashlight'), ('Torch', 'Flashlight')]


def _script(M, vid, n):
    b = M.slide(vid, n); out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _shift_active(M, vid, first_n, by=1):
    v = M.video(vid)
    for b in v['beats'][first_n - 1:]:
        if b['active'] >= 0: b['active'] += by
    M.touched_videos.add(vid)


def _solution(M, qid, group, sidebar, intro, slides, after=None):
    n = M.next_question_number(TOPIC)
    label = 'Question %d' % n
    idx = sidebar.index(label)
    beats = [dict(mode='title', title=label, script=['Question %s.' % _word(n)] + intro)]
    for title, script in slides:
        beats.append(dict(mode='question', active=idx, title=title, pre=[Q(qid)], script=script))
    v = M.new_video('solve-' + qid, TOPIC, group, sidebar, beats, M.section_of(qid), kind='solution', qid=qid, after=after)
    v['beats'][0]['title'] = group
    v['hybrid']['num'] = 26
    v['title'] = v['navLabel'] = M.q(qid)['stem']
    return n


# =====================================================================================================
# 1. Lesson videos
# =====================================================================================================
def fix_lesson1(M):
    s = _script(M, L1, 1)
    s[2] = "They come in two types on the exam. Let's learn both."
    M.set_slide(L1, 1, script=s)


def fix_ranges(M):
    # slide 4: max(8, 7) -> 7 was wrong notation (max(8, 7) = 8)
    def fn(lines):
        for l in lines:
            if l.get('draw') == 'Write max(8, 7) → 7': l['draw'] = 'Write "the smaller of 8 and 7 → 7"'
        return lines
    M.edit_lines(L2, 4, fn)

    # new slide 7: the other regions (union, neither, only) - find the overlap range first
    M.insert_slides(L2, 6, [dict(mode='concept', active=5, title='Other regions', script=[
        'So far, they asked about both. The exam also asks about the other regions.',
        'Same twelve students: eight music, seven sport. The overlap goes from three to seven.',
        A("'Both: from 3 to 7' appears", T('Both: from $3$ to $7$', size=40)),
        'Everything else depends on the overlap. So, find its range first.',
        A("'At least one = A + B − both: from 8 to 12' appears",
          T('At least one $=A+B-\\text{both}$: from $8$ to $12$', size=40)),
        'At least one — the union — is A plus B minus both. Big overlap, small union.',
        D('Write "15 − 7 = 8 · 15 − 3 = 12"'),
        'Overlap seven: union eight — just the larger group. Overlap three: union twelve — everyone.',
        'So, the union goes from the larger group up to A plus B. But never more than the total.',
        A("'Neither = total − at least one: from 0 to 4' appears",
          T('Neither $=\\text{total}-\\text{at least one}$: from $0$ to $4$', size=40)),
        'Neither is the total minus the union. Neither is big when the union is small.',
        D('Write "12 − 12 = 0 · 12 − 8 = 4"'),
        A("'Music only = A − both: from 1 to 5' appears", T('Music only $=A-\\text{both}$: from $1$ to $5$', size=40)),
        'Music only is music minus both. Here it works backwards: the BIGGER the overlap, the SMALLER music only.',
        D('Write "8 − 7 = 1 · 8 − 3 = 5"'),
        'Music only: from one to five. Its minimum uses the MAXIMUM overlap.',
    ])])

    # slide 8 (was 7): "at most / at least" belongs to the thing they ask about, not to "both"
    M.set_slide(L2, 8, script=[
        'How do you recognize a range question?',
        A("'at most / greatest → the largest value of what they ask' appears",
          T('"at most" · "greatest" → the largest value of what they ask', size=40)),
        '"At most", "greatest" — they want the largest possible value.',
        A("'at least / smallest → the smallest value of what they ask' appears",
          T('"at least" · "smallest" → the smallest value of what they ask', size=40)),
        '"At least", "smallest" — the smallest value it can have.',
        'But careful: the largest or smallest of WHAT? Of the thing they ask about. Not always of both.',
        A("'Ask: to make THIS small, what must the overlap be?' appears",
          T('Ask: to make THIS small, what must the overlap be?', size=40)),
        '"At least how many play music only?" Music only is small when the overlap is big. So, use the MAXIMUM overlap.',
        D('Write "at least … music only → max both → 8 − 7 = 1"'),
        '"At most how many do neither?" Neither is big when the union is small — again the maximum overlap.',
        A("'could be / choices like between 3 and 9 → a range' appears",
          T('"could be" · choices like "between 3 and 9" → a range', size=40)),
        '"What could be" — no single answer. And sometimes the choices themselves give it away.',
        D('Underline "THIS"'),
        'Spot the words. Decide what they ask about. Then choose the overlap that makes it big or small.',
    ])

    # recap (now slide 11)
    M.set_slide(L2, 11, script=[
        "Let's lock it in.",
        A("'Max overlap = the smaller group' appears", T('Max overlap $=$ the smaller group', size=42)),
        A("'Min overlap = (A + B) − total, or 0' appears", T('Min overlap $=(A+B)-\\text{total}$ — or $0$', size=42)),
        A("'Other regions: find the overlap range first' appears",
          T('Union, neither, only: find the overlap range first', size=42)),
        A("'at most / at least → of the thing they ask' appears",
          T('"at most" / "at least" → of the thing they ask', size=42)),
        D('Circle "or 0"'),
        'Next: exact overlap — when the question gives us one more fact.',
    ])
    _shift_active(M, L2, 8)
    M.set_sidebar(L2, ['Missing data → range', 'Place them one by one', 'Max = smaller group', 'Min = the excess',
                       'When min is 0', 'Other regions', 'Spot the wording', 'Worked example', 'Fractions too', 'Recap'])


def fix_exact(M):
    # slide 3: the strip is the circles unrolled
    s = _script(M, L3, 3)
    s[0] = 'With bigger numbers, use the squares method.'
    s.insert(1, "It's the same four regions as the circles — just unrolled into one line.")
    M.set_slide(L3, 3, script=s)

    # new slide 6: exactly one
    M.insert_slides(L3, 5, [dict(mode='concept', active=4, title='Exactly one', pre=[
        T('18 members · 10 Spanish · 9 French · 5 both', size=44, gap=40), dict(STRIP_SE)], script=[
        'One more region the exam loves: exactly one.',
        'Exactly one means Spanish only or French only — not both.',
        D("Circle the boxes 'Spanish only' and 'French only'"),
        'From the strip: five plus four — nine.',
        A("'Exactly one = A + B − 2 · both' appears", T('Exactly one $=A+B-2\\cdot\\text{both}$', size=46)),
        'Without the strip: add the two groups, and take both away TWICE — it sits inside each group once.',
        D('Write "10 + 9 − 2 · 5 = 9"'),
        'Ten plus nine is nineteen. Minus ten — nine. Same answer.',
        'Or: fourteen speak at least one language, five speak both. Fourteen minus five — nine again.',
    ])])
    M.set_slide(L3, 9, script=[
        "Let's lock it in.",
        A("'Strip: neither · A only · both · B only' appears", T('Strip: neither · A only · both · B only', size=42)),
        A("'The two brackets share the middle box' appears", T('The two brackets share the middle box', size=42)),
        A("'At least one = A + B − both' appears", T('At least one $=A+B-\\text{both}$', size=42)),
        A("'Exactly one = A + B − 2 · both' appears", T('Exactly one $=A+B-2\\cdot\\text{both}$', size=42)),
        D('Box the word "share"'),
        'Put the data in the boxes, and fill them like a sudoku.',
        'Three questions next — try each one first.',
    ])
    _shift_active(M, L3, 7)
    M.set_sidebar(L3, ['One more fact', 'The squares method', 'Given both → neither', 'Start from any box',
                       'Exactly one', 'Fractions of overlap', 'Union ≠ population', 'Recap'])


# =====================================================================================================
# 2. Existing guided questions and their videos
# =====================================================================================================
def fix_guided(M):
    S = M.set_q
    S('wp24-g070', stem='Of 45 campers, 28 bring a flashlight, 23 bring a map, and 16 bring both. How many bring neither?',
      expl=['Both is $16$, therefore map only is $23-16=7$.',
            'At least one item: the whole flashlight group plus map only, $28+7=35$.',
            'Neither: $45-35=10$.',
            'In one line: $45-(28+23-16)=45-35=10$.'])
    S('wp24-g071', stem='A workshop has 22 machines. Of them, 14 cut, 12 polish, and 3 do neither. '
                        'How many machines both cut and polish?',
      expl=['$3$ machines do neither, therefore $22-3=19$ do at least one job.',
            'The two jobs add to $14+12=26$. That is $26-19=7$ more than $19$. These $7$ machines were counted twice, '
            'so $7$ do both.'])
    S('wp24-g072', expl=[
        'Call the overlap $x$. It is $\\frac16$ of the photography students, therefore there are $6x$ photography students. '
        'It is $\\frac14$ of the volunteers, therefore there are $4x$ volunteers.',
        'Photography only: $6x-x=5x$. Volunteers only: $4x-x=3x$.',
        'The ratio is $5x:3x=5:3$. The group that does neither is not needed.'])
    S('wp24-g074', expl=[
        '$35\\%+80\\%=115\\%$, but the guests are only $100\\%$. So, at least $115\\%-100\\%=15\\%$ know both.',
        '$15\\%$ of $240$: $10\\%$ is $24$ and $5\\%$ is $12$: $24+12=36$.',
        'This minimum is possible: all $20\\%$ who do not know the host are in the organizer group, and the other '
        '$35\\%-20\\%=15\\%$ of the organizer group know the host.'])
    S('wp24-g075', stem='A class has 48 students. Of them, 21 work in the greenhouse and 11 work in the orchard. '
                        'Which of the following could be the number of students who work in neither place?',
      expl=['Neither $=48-\\text{union}$, where the union is everyone who works in at least one place.',
            'Smallest union: all $11$ orchard workers also work in the greenhouse, therefore the union is $21$. '
            'Largest union: no overlap, $21+11=32$ (less than $48$, therefore it fits).',
            'Neither goes from $48-32=16$ to $48-21=27$. Only $18$ is in this range. It happens when the overlap is $2$: '
            'the union is $21+11-2=30$, and $48-30=18$.'])
    S('wp24-g076', expl=[
        '"At least one is in both groups" must be true only when the two groups add up to more than the whole.',
        'Choice 1: non-juniors and non-coders, $\\frac45+\\frac35=\\frac75>1$ — forced. '
        'Choice 3: $\\frac25+\\frac45=\\frac65>1$ — forced. '
        'Choice 4: trainees and non-coders, $\\frac12+\\frac35=\\frac{11}{10}>1$ — forced.',
        'Choice 2: juniors and remote workers, $\\frac15+\\frac45=1$ exactly. This does not force an overlap. '
        'Out of $10$ employees, the $2$ juniors can work on site and the other $8$ remotely. '
        'So, choice 2 is not necessarily true.'])
    S('wp24-g077', expl=[
        '$\\frac1{10}$ of the staff is $8$ people, therefore the staff is $8\\cdot10=80$.',
        'Soup: $\\frac25\\cdot80=32$. Salad: $\\frac14\\cdot80=20$. At least one: $32+20-8=44$.',
        'Neither: $80-44=36$.'])
    S('wp24-g078', stem='Two researchers photograph butterflies. One photographs 31 butterflies and the other photographs 22. '
                        'Together, their photographs show 40 different butterflies. '
                        'How many butterflies appear in both collections?',
      expl=['The $40$ butterflies are the ones in at least one collection (the union), therefore neither is $0$.',
            'The first researcher has $31$ of the $40$. The other $40-31=9$ appear only in the second collection.',
            'Both: $22-9=13$. Check: $31+22-13=40$.'])

    # Q2 video: the easier route (through the union) first
    M.move_slide('solve-wp24-g071', 3, 2)
    M.set_slide('solve-wp24-g071', 2, title='Method 1 · Through the union', script=[
        'Neither is given — three. We want both.',
        D('Write 22 − 3 = 19'),
        'Three do neither — nineteen do at least one job.',
        D('Write 14 + 12 − 19 = 7'),
        'The two jobs add to twenty-six — seven more than nineteen. Those seven were counted twice: they do both.',
        D('Circle choice 2'),
        'Seven. Choice two.',
    ])
    s = _script(M, 'solve-wp24-g071', 3)
    s[0] = 'The same answer on the strip.'
    s = [x for x in s if x not in (D('Circle choice 2'),)]
    s[-1] = 'Seven again.'
    M.set_slide('solve-wp24-g071', 3, title='Method 2 · The squares', script=s)

    # Q3 video: the ratio colon is a real ratio - say so
    def fn(lines):
        for l in lines:
            if l.get('draw', '').startswith('Write 18 − 3 = 15'):
                l['draw'] = 'Write 18 − 3 = 15, 12 − 3 = 9 → ratio 15 : 9 = 5 : 3'
        return lines
    M.edit_lines('solve-wp24-g072', 3, fn)

    # Q5 video: the simpler route (neither = total - union) first
    V5 = 'solve-wp24-g075'
    M.insert_slides(V5, 1, [dict(mode='question', active=1, title='Method 1 · Through the union', pre=[Q('wp24-g075')], script=[
        'Neither in a range question. Go through the union — the students in at least one place.',
        D('Write "union: smallest 21 · largest 21 + 11 = 32"'),
        'Smallest union: all eleven orchard workers also work in the greenhouse. Twenty-one.',
        "Largest union: no overlap at all. Twenty-one plus eleven — thirty-two. That's less than forty-eight — it fits.",
        D('Write "neither = 48 − union: from 48 − 32 = 16 to 48 − 21 = 27"'),
        'Neither is forty-eight minus the union. Big union, small neither.',
        'So, neither goes from sixteen to twenty-seven.',
        D('Cross out choices 1, 2 and 3'),
        'Fourteen is too small. Thirty and thirty-five are too big.',
        D('Circle choice 4'),
        'Eighteen. Choice four.',
    ])])
    s = _script(M, V5, 3)
    s[0] = 'For strong students — another way to see it.'
    M.set_slide(V5, 3, title='Method 2 · Complements', script=s)
    s = _script(M, V5, 4)
    s[0] = 'The fast way. The maximum alone kills two choices.'
    M.set_slide(V5, 4, title='Method 3 · The insight', script=s)

    for vid in ['solve-wp24-g074', V5, 'solve-wp24-g076', 'solve-wp24-g077', 'solve-wp24-g078']:
        M.set_sidebar(vid, ADV_SIDEBAR)
        for b in M.video(vid)['beats']:
            if b['active'] >= 0: b['active'] = ADV_SIDEBAR.index(b['bigTitle'] if b.get('bigTitle') else
                                                                  M.video(vid)['beats'][0]['bigTitle'])


# =====================================================================================================
# 3. New guided question: "at least ... only" (the at-least trap)
# =====================================================================================================
def guided_only(M):
    qid = 'q-r26-t24-01'
    M.new_q(qid, TOPIC, 'A club has 50 members. Of them, 32 swim and 27 run. '
                        'At least how many members swim but do not run?',
            ['$0$', '$5$', '$9$', '$23$'], 2, [
                'Swim but not run (swim only) $=32-\\text{both}$. It is smallest when "both" is largest.',
                'Largest overlap: the smaller group — all $27$ runners also swim. Then swim only is $32-27=5$.',
                'Check: $27$ both, $5$ swim only, $0$ run only, and $50-32=18$ do neither. Every number fits.',
                'Trap: the minimum overlap $32+27-50=9$ gives $32-9=23$. That is the MOST swim only, not the least.'])
    M.place_q(qid, ADV, after='solve-wp24-g075')
    _solution(M, qid, 'Advanced Overlap', ADV_SIDEBAR, ['"At least" — but not about both. Careful here.'], [
        ('Method 1 · What makes it small', [
            "They ask about swimmers who don't run — swim only.",
            D('Write "swim only = 32 − both"'),
            'Swim only is thirty-two minus both. To make it SMALL, make both as BIG as possible.',
            D('Write "max both = the smaller group = 27"'),
            'The biggest overlap: all twenty-seven runners also swim.',
            D('Write "32 − 27 = 5"'),
            "Thirty-two minus twenty-seven: five swimmers who don't run. That's the least.",
            D('Circle choice 2'),
            'Five. Choice two.',
            'The trap: "at least" makes you think of the minimum overlap. Fifty-nine minus fifty — nine.',
            D('Write "32 − 9 = 23 → the MOST swim only"'),
            "Thirty-two minus nine is twenty-three. That's the most swim only can be — the opposite of the question.",
        ]),
        ('Method 2 · Check on the strip', [
            "Let's see it on the strip.",
            D('Draw the strip: Neither · Swim only · Both · Run only'),
            D("Write 27 in 'Both', 0 in 'Run only', 5 in 'Swim only'"),
            'Twenty-seven both, zero run only, five swim only. Thirty-two swimmers, twenty-seven runners.',
            D("Write 50 − 32 = 18 in 'Neither'"),
            'Fifty minus thirty-two: eighteen do neither. Every number fits.',
            'Could swim only be less than five? Only with more than twenty-seven in both. '
            'But there are only twenty-seven runners.',
        ]),
    ])


# =====================================================================================================
# 4. New lesson: two-way tables (+ guided question)
# =====================================================================================================
def two_way(M):
    vid = 'r26-t24-two-way'
    empty = {'k': 'vis', 'v': {'type': 'table', 'headers': ['', 'Glasses', 'No glasses', 'Total'],
                               'rows': [['Women', '', '', ''], ['Men', '', '', ''], ['Total', '', '', '']]},
             'w': 1000, 'h': 330}
    full = {'k': 'vis', 'v': {'type': 'table', 'headers': ['', 'Glasses', 'No glasses', 'Total'],
                              'rows': [['Women', '12', '48', '60'], ['Men', '12', '28', '40'], ['Total', '24', '76', '100']]},
            'w': 1000, 'h': 330}
    M.new_video(vid, TOPIC, 'Two-Way Tables', ['Two traits', 'Fill the table', 'Percent of what?', 'Recap'], [
        dict(mode='title', title='Two-Way Tables', script=[
            'Two-way tables.',
            'Sometimes every person has two yes-or-no traits. Woman or man. Glasses or no glasses.',
            'The strip gets messy here. A table is cleaner.']),
        dict(mode='concept', title='Two traits', active=0, script=[
            "Here's a classic.",
            A("'60% are women' appears", T('$60\\%$ of the employees are women', size=42)),
            'Sixty percent of the employees are women.',
            A("'20% of the women and 30% of the men wear glasses' appears",
              T('$20\\%$ of the women and $30\\%$ of the men wear glasses', size=42)),
            'Twenty percent of the WOMEN wear glasses. Thirty percent of the MEN wear glasses.',
            A("'What percent of all employees wear glasses?' appears",
              T('What percent of all employees wear glasses?', size=42)),
            'The trap: these two percents are of different groups. You cannot add them. You cannot just average them.',
            D('Write "20% + 30% = 50% ✗ · average 25% ✗"'),
            'We need one whole. Plug in one hundred employees.']),
        dict(mode='concept', title='Fill the table', active=1, script=[
            A('An empty table appears: rows Women · Men · Total, columns Glasses · No glasses · Total', empty),
            'Rows: women and men. Columns: glasses and no glasses. And a total for every row and every column.',
            D("Write 100 in 'Total · Total', 60 in 'Women · Total', 40 in 'Men · Total'"),
            'One hundred employees. Sixty women — and forty men.',
            D("Write 12 in 'Women · Glasses', then 60 − 12 = 48 in 'Women · No glasses'"),
            'Twenty percent of the sixty women wear glasses: twelve. The other forty-eight do not.',
            D("Write 12 in 'Men · Glasses', then 40 − 12 = 28 in 'Men · No glasses'"),
            'Thirty percent of the forty men: twelve. The other twenty-eight do not.',
            D("Write 12 + 12 = 24 in 'Total · Glasses' and 48 + 28 = 76 in 'Total · No glasses'"),
            'Add down the glasses column: twelve plus twelve — twenty-four.',
            'Twenty-four out of a hundred: twenty-four percent wear glasses.',
            "Every row adds across. Every column adds down. It's the same sudoku as the strip."]),
        dict(mode='concept', title='Percent of what?', active=2, pre=[full], script=[
            A("'What percent of the people with glasses are women?' appears",
              T('What percent of the people with glasses are women?', size=40)),
            'Now the question turns around. Of the people WITH glasses — what percent are women?',
            'Of the people with glasses — then the whole is the glasses column. Twenty-four. Not one hundred.',
            D('Circle the Glasses column'),
            D('Write "12 out of 24 = 1/2 = 50%"'),
            'Twelve of the twenty-four are women. Half — fifty percent.',
            'The words after "of" tell you the whole. "Of the women" — that row. '
            '"Of the people with glasses" — that column. "Of all" — the hundred.']),
        dict(mode='concept', title='Recap', active=3, script=[
            "Let's lock it in.",
            A("'Two yes/no traits → a table with totals' appears", T('Two yes/no traits → a table with totals', size=42)),
            A("'Percents? Plug in 100' appears", T('Percents? Plug in $100$', size=42)),
            A("'Rows add across, columns add down' appears", T('Rows add across · columns add down', size=42)),
            A("'Of the ... → that row or column is the whole' appears",
              T('"of the …" → that row or column is the whole', size=42)),
            D('Underline "of the"'),
            'Your turn. A guided question next — try it first.']),
    ], ADV, after='solve-wp24-g078')
    M.video(vid)['hybrid']['num'] = 26

    qid = 'q-r26-t24-02'
    M.new_q(qid, TOPIC, 'In a school, $40\\%$ of the students are in the upper grades and the rest are in the lower grades. '
                        '$30\\%$ of the upper-grade students and $60\\%$ of the lower-grade students walk to school. '
                        'What percent of the students who walk to school are in the upper grades?',
            ['$12\\%$', '$25\\%$', '$33\\frac13\\%$', '$40\\%$'], 2, [
                'Plug in $100$ students: $40$ in the upper grades and $60$ in the lower grades.',
                'Upper grades who walk: $30\\%$ of $40$ is $12$. Lower grades who walk: $60\\%$ of $60$ is $36$. '
                'Walkers: $12+36=48$.',
                '"Of the students who walk" means the whole is $48$: $\\frac{12}{48}=\\frac14=25\\%$.'])
    M.place_q(qid, ADV, after=vid)
    _solution(M, qid, 'Two-Way Tables', ['Question 10'], ['Two traits of the same students: grade and walking. A table.'], [
        ('Method 1 · The table', [
            'Plug in one hundred students.',
            D("Draw a table: rows Upper · Lower · Total, columns Walk · Don't walk · Total"),
            "Rows: upper and lower grades. Columns: walk and don't walk.",
            D("Write 40 in 'Upper · Total' and 60 in 'Lower · Total'"),
            'Forty percent upper grades — forty students. That leaves sixty in the lower grades.',
            D("Write 30% of 40 = 12 in 'Upper · Walk'"),
            'Thirty percent of the forty upper-grade students walk: twelve.',
            D("Write 60% of 60 = 36 in 'Lower · Walk'"),
            'Sixty percent of the sixty lower-grade students: thirty-six.',
            D("Write 12 + 36 = 48 in 'Total · Walk'"),
            'Forty-eight students walk.',
            'Now read the question: of the students who WALK. The whole is the walk column — forty-eight.',
            D('Write "12 out of 48 = 1/4 = 25%"'),
            'Twelve out of forty-eight: a quarter. Twenty-five percent.',
            D('Circle choice 2'),
            'Choice two.']),
        ('The traps', [
            'Each wrong choice is a real mistake.',
            D('Next to choice 1 write "12 out of 100"'),
            'Twelve percent: twelve out of all one hundred students. The wrong whole.',
            D('Next to choice 3 write "12 out of 36"'),
            'Thirty-three and a third: twelve compared to the thirty-six lower-grade walkers. The wrong whole again.',
            D('Next to choice 4 write "upper grades of ALL students"'),
            'Forty percent: the upper grades out of everyone. It ignores walking.',
            "Always ask: percent of WHAT? That's the row or column you divide by."]),
    ])


# =====================================================================================================
# 5. New lesson: three groups (+ guided question)
# =====================================================================================================
def three_groups(M):
    vid = 'r26-t24-three-groups'
    M.new_video(vid, TOPIC, 'Three Groups', ['Count who is missing', 'Can it be zero?', 'Recap'], [
        dict(mode='title', title='Three Groups', script=[
            'Three groups.',
            'Sometimes the exam adds a third group — and asks how many MUST be in all three.',
            "Same idea as before: count what doesn't fit."]),
        dict(mode='concept', title='Count who is missing', active=0, script=[
            A("'50 employees · English 40 · French 35 · German 30' appears",
              T('$50$ employees · English $40$ · French $35$ · German $30$', size=40)),
            'Fifty employees. Forty speak English, thirty-five French, thirty German. '
            'At least how many speak all three?',
            'Turn it around. Who is NOT in all three? Someone who is missing at least one language.',
            D('Write "no English: 50 − 40 = 10 · no French: 50 − 35 = 15 · no German: 50 − 30 = 20"'),
            "Ten don't speak English. Fifteen don't speak French. Twenty don't speak German.",
            "Even if they are all different people, that's only ten plus fifteen plus twenty — forty-five.",
            D('Write "10 + 15 + 20 = 45 → 50 − 45 = 5"'),
            'At most forty-five miss a language. The other five MUST speak all three.',
            A("'Min in all three = total − (all who miss a group)' appears",
              T('Min in all three $=$ total minus everyone who misses a group', size=38)),
            "That's the rule: the total, minus everyone who could be missing something.",
            A("'Same as A + B + C − 2 · total' appears", T('Same as: $A+B+C-2\\cdot\\text{total}$', size=40)),
            D('Write "40 + 35 + 30 − 2 · 50 = 5"'),
            'The same number in one line: add the three groups, subtract the total twice. Five again.',
            'Two groups: the sum minus the total once. Three groups: minus the total twice.']),
        dict(mode='concept', title='Can it be zero?', active=1, script=[
            A("'100 readers · fiction 70 · history 65 · science 60' appears",
              T('$100$ readers · fiction $70$ · history $65$ · science $60$', size=40)),
            'A hundred readers. Seventy read fiction, sixty-five history, sixty science.',
            D('Write "30 + 35 + 40 = 105 → more than 100"'),
            "Missing: thirty, thirty-five, forty. That's a hundred and five — more than a hundred readers.",
            'The rule gives a negative number. Just like with two groups: then the minimum is zero.',
            'Is zero really possible? Show one way.',
            A("'35 fiction + history · 30 fiction + science · 30 history + science · 5 fiction only' appears",
              T('$35$ fiction + history · $30$ fiction + science\n$30$ history + science · $5$ fiction only', size=36)),
            D('Write "fiction 35 + 30 + 5 = 70 · history 35 + 30 = 65 · science 30 + 30 = 60"'),
            'Every group has the right size. One hundred people in total — and nobody reads all three.',
            'And the maximum in all three? The smallest group — here sixty.']),
        dict(mode='concept', title='Recap', active=2, script=[
            "Let's lock it in.",
            A("'Min in all three = total − everyone who misses a group, or 0' appears",
              T('Min in all three $=$ total minus the missing ones — or $0$', size=40)),
            A("'One line: A + B + C − 2 · total' appears", T('One line: $A+B+C-2\\cdot\\text{total}$', size=40)),
            A("'Max in all three = the smallest group' appears", T('Max in all three $=$ the smallest group', size=40)),
            D('Circle "or 0"'),
            'Your turn — a guided question.']),
    ], ADV, after='solve-q-r26-t24-02')
    M.video(vid)['hybrid']['num'] = 26

    qid = 'q-r26-t24-03'
    M.new_q(qid, TOPIC, 'In a survey, $80\\%$ of the people own a phone, $75\\%$ own a laptop, and $70\\%$ own a tablet. '
                        'At least what percent of the people own all three?',
            ['$0\\%$', '$25\\%$', '$55\\%$', '$70\\%$'], 2, [
                'Plug in $100$ people. No phone: $20$. No laptop: $25$. No tablet: $30$.',
                'At most $20+25+30=75$ people miss at least one item. So, at least $100-75=25$ own all three: $25\\%$.',
                'In one line: $80+75+70-2\\cdot100=25$.',
                'Traps: $55\\%$ uses only two groups ($80+75-100$), and $70\\%$ is the maximum (the smallest group).'])
    M.place_q(qid, ADV, after=vid)
    _solution(M, qid, 'Three Groups', ['Question 11'], ['Three groups, and "at least" about all three.'], [
        ('Method 1 · Who is missing', [
            'Plug in a hundred people — the percents become people.',
            D('Write "no phone 20 · no laptop 25 · no tablet 30"'),
            'Twenty have no phone. Twenty-five have no laptop. Thirty have no tablet.',
            D('Write "20 + 25 + 30 = 75"'),
            'At most seventy-five people miss something — if they are all different people.',
            D('Write "100 − 75 = 25"'),
            'The other twenty-five MUST own all three.',
            D('Circle choice 2'),
            'Twenty-five percent. Choice two.']),
        ('Method 2 · One line', [
            D('Write "80 + 75 + 70 − 2 · 100 = 25"'),
            'Or add the three groups — two hundred twenty-five — and subtract the total twice. Twenty-five.',
            D('Next to choice 3 write "two groups only" and next to choice 4 write "the maximum"'),
            'The traps: fifty-five percent uses only two groups, phone and laptop.',
            'And seventy percent is the MAXIMUM — the smallest group. They asked for the least.']),
    ])

    M.new_card('mem-r26-t24-more', TOPIC, ADV, dict(
        title='Two-way tables and three groups',
        intro='Two traits of the same people → a table. Three groups → count who is missing.',
        tables=[
            {'title': 'Two-way table', 'head': ['', 'B', 'not B', 'Total'],
             'rows': [['A', '', '', 'A total'], ['not A', '', '', 'not-A total'], ['Total', 'B total', 'not-B total', 'all']]},
            {'title': 'Three groups', 'head': ['What', 'Rule', 'Example'],
             'rows': [['Min in all three', 'total $-$ (missing A $+$ missing B $+$ missing C), or $0$',
                       '$50-(10+15+20)=5$'],
                      ['Same in one line', '$A+B+C-2\\cdot\\text{total}$', '$40+35+30-100=5$'],
                      ['Max in all three', 'the smallest group', '$30$']]}],
        tips=['Percents in a table? Plug in $100$.',
              '"Of the …" tells you the whole: that row or that column.',
              'Rows add across, columns add down.']), after='solve-q-r26-t24-03')


# =====================================================================================================
# 6. Memory card
# =====================================================================================================
def fix_card(M):
    c = M.card('mem-overlap')
    c['intro'] = 'Two question types: a range (min and max) or an exact overlap.'
    c['tables'] = [
        {'title': 'Range questions — the overlap', 'head': ['What', 'Rule', 'Example ($12$ students: $8$ and $7$)'],
         'rows': [['Maximum overlap', 'the smaller group', '$7$'],
                  ['Minimum overlap', '$(A+B)-\\text{total}$, or $0$ if that is not positive', '$8+7-12=3$']]},
        {'title': 'Range questions — other regions (find the overlap range first)', 'head': ['Region', 'Rule', 'Example'],
         'rows': [['At least one (union)', '$A+B-\\text{both}$: from the larger group to $A+B$ (at most the total)', '$8$ to $12$'],
                  ['Neither', '$\\text{total}-\\text{union}$: big when the union is small', '$0$ to $4$'],
                  ['A only', '$A-\\text{both}$: its minimum uses the MAXIMUM overlap', '$8-7=1$ to $8-3=5$']]},
        {'title': 'Exact questions — the squares method', 'head': ['Neither', 'A only', 'Both', 'B only'],
         'rows': [['outside both', 'A bracket →', '← shared →', '← B bracket']]},
        {'title': 'Formulas', 'head': ['What', 'Formula'],
         'rows': [['Everyone once', '$A+B-\\text{both}+\\text{neither}=\\text{total}$'],
                  ['Exactly one', '$A+B-2\\cdot\\text{both}$']]}]
    c['tips'] = ['"At most" / "at least" is about the thing they ask. Ask: to make THIS small, what must the overlap be?',
                 'Two shares adding to exactly the whole do NOT force an overlap; more than the whole does.',
                 'Percents? Stay in percent and change to people only at the end.',
                 '"Different items in either collection" is the union — neither is $0$.']


# =====================================================================================================
# 7. Practice
# =====================================================================================================
def fix_practice(M):
    S = M.set_q
    S('wp24-p01', expl=['$65\\%+55\\%=120\\%$ of the winners, but there are only $100\\%$. '
                        'So, at least $120\\%-100\\%=20\\%$ are in both groups.', '$20\\%$ of $150$ is $30$.'])
    S('wp24-p03', expl=['$\\frac35$ of the employees is $72$, therefore $\\frac15$ is $72\\div3=24$ and the total is $24\\cdot5=120$.',
                        'Personal tablets: $\\frac12\\cdot120=60$.', 'Minimum overlap: $72+60-120=12$.'])
    S('wp24-p05', expl=['Two groups must overlap only when they add up to more than the whole.',
                        'Under 50 and pet owners: $\\frac45+\\frac25=\\frac65>1$ — forced.',
                        'The others: cyclists and vegetable growers, $\\frac35+\\frac14=\\frac{17}{20}<1$. '
                        'Aged at least 50 and vegetable growers, $\\frac15+\\frac14=\\frac{9}{20}<1$. '
                        'Cyclists and pet owners, $\\frac35+\\frac25=1$ — not more than $1$. '
                        'These groups can be separate.'])
    S('wp24-p06', stem='Each of 60 trainees gets a score from 0 to 12. Of them, 26 score from 9 to 12, 24 score from 7 to 10, '
                       'and 20 score below 7. How many trainees score from 9 to 10? (All ranges include both ends.)',
      expl=['Together, the bands "9 to 12" and "7 to 10" cover every score from 7 to 12. Everyone who does not score '
            'below 7 is in at least one band: $60-20=40$.',
            'The two bands share the scores 9 to 10. That is the overlap: $26+24-40=10$.'])
    S('wp24-p07', expl=['Neither $=250-\\text{union}$. Neither is greatest when the union is smallest.',
                        'The union is at least the larger group, $205$. It is exactly $205$ when all $190$ musicians '
                        'also enjoy chess.',
                        'Neither: $250-205=45$, and $\\frac{45}{250}=\\frac{18}{100}=18\\%$.'])
    S('wp24-p08', expl=['Everyone is in at least one group, therefore neither is $0$.',
                        'Both: $\\frac34+\\frac58-1=\\frac68+\\frac58-\\frac88=\\frac38$.'])
    S('wp24-p09', stem='A class has 48 students. Of them, 28 swim and 24 cycle. Three quarters of the cyclists also swim. '
                       'How many students do neither activity?',
      expl=['Both: $\\frac34\\cdot24=18$.', 'At least one: $28+24-18=34$. Neither: $48-34=14$.'])
    S('wp24-p10', expl=['Blue without zips: $\\frac23-\\frac12=\\frac16$. Zipped but not blue: $\\frac34-\\frac12=\\frac14$.',
                        'The ratio is $\\frac16:\\frac14$. Multiply both parts by $12$: the ratio is $2:3$.'])
    S('wp24-p11', stem='A survey of 90 people finds that 48 use buses and 57 use trains. '
                       'What is the range of possible numbers of people who use both?',
      expl=['Minimum: $48+57-90=15$.', 'Maximum: the smaller group, $48$ (all bus users also use trains).',
            'So, the number is from $15$ to $48$.'])
    S('wp24-p12', expl=['At least one: $64-12=52$. Both: $39+31-52=18$.',
                        'Exactly one $=\\text{union}-\\text{both}=52-18=34$.'])
    S('wp24-p13', expl=[
        'Count who misses a group: no fiction $100-70=30$, no history $100-65=35$, no science $100-60=40$.',
        '$30+35+40=105$ — more than the $100$ readers. So, no one is forced into all three '
        '($70+65+60-2\\cdot100=-5$ is negative), and the minimum can be $0$.',
        'Check that $0$ really works: $35$ read fiction and history, $30$ read fiction and science, $30$ read history and '
        'science, and $5$ read fiction only. Fiction: $35+30+5=70$. History: $35+30=65$. Science: $30+30=60$. '
        'Total: $35+30+30+5=100$, and nobody reads all three.'])
    S('wp24-p14', stem='A school has 80 pupils: 50 study French, 40 study German, and 25 study both. '
                       'Of the pupils who study French, what fraction also study German?',
      expl=['"Of the pupils who study French" means the whole is the $50$ French pupils.',
            '$25$ of them also study German: $\\frac{25}{50}=\\frac12$.'])
    S('wp24-p15', expl=['$20\\%$ do neither, therefore $100\\%-20\\%=80\\%$ do at least one.',
                        'Both: $55\\%+45\\%-80\\%=20\\%$.',
                        'Note: $55\\%+45\\%=100\\%$ alone does not force an overlap. '
                        'The extra fact "$20\\%$ do neither" is what forces it.'])
    S('wp24-p16', stem='A bag contains 72 badges: 48 are round and 30 are metal. '
                       'At least how many round badges are not metal?',
      expl=['Round but not metal $=48-\\text{both}$. It is smallest when "both" is largest.',
            'Largest overlap: all $30$ metal badges are round. Then $48-30=18$ round badges are not metal.'])
    S('wp24-p17', expl=['Remote only: $90-60=30$. Flexible only: $75-60=15$.',
                        'Exactly one: $30+15=45$. In one line: $90+75-2\\cdot60=45$.'])

    # near-duplicates of guided Q1 / Q8 and of p08
    M.unplace('wp24-p04')
    M.unplace('wp24-p02')

    new = [
        ('q-r26-t24-04', 'A class has 30 students, and 18 of them are girls. 12 students wear glasses, and 5 of those are boys. '
                         'How many girls do not wear glasses?',
         ['$6$', '$7$', '$11$', '$13$'], 3,
         ['Girls who wear glasses: $12-5=7$.', 'Girls who do not wear glasses: $18-7=11$.']),
        ('q-r26-t24-05', 'At a factory, $70\\%$ of the workers work the day shift and the rest work the night shift. '
                         '$10\\%$ of the day-shift workers and $40\\%$ of the night-shift workers are new. '
                         'What percent of all the workers are new?',
         ['$12\\%$', '$19\\%$', '$25\\%$', '$50\\%$'], 2,
         ['Plug in $100$ workers: $70$ day shift and $30$ night shift.',
          'New workers: $10\\%$ of $70$ is $7$, and $40\\%$ of $30$ is $12$. Together $7+12=19$, which is $19\\%$.',
          'The average of $10\\%$ and $40\\%$ ($25\\%$) is wrong: the two percents are of groups of different sizes.']),
        ('q-r26-t24-06', 'In a group, $\\frac35$ of the people are adults and the rest are children. '
                         '$\\frac14$ of the adults and $\\frac12$ of the children play chess. '
                         'What fraction of the chess players are children?',
         ['$\\frac15$', '$\\frac25$', '$\\frac37$', '$\\frac47$'], 4,
         ['Plug in $20$ people: $12$ adults and $8$ children.',
          'Chess players: $\\frac14\\cdot12=3$ adults and $\\frac12\\cdot8=4$ children, $7$ in all.',
          '"Of the chess players" means the whole is $7$: $\\frac47$ are children.']),
        ('q-r26-t24-07', 'Of 80 guests, 50 drink coffee and 45 drink tea. '
                         'What is the greatest possible number of guests who drink neither?',
         ['$0$', '$15$', '$30$', '$35$'], 3,
         ['Neither $=80-\\text{union}$. It is greatest when the union is smallest.',
          'The smallest union is the larger group, $50$: all $45$ tea drinkers also drink coffee.',
          'Neither: $80-50=30$. (Using the smaller group, $80-45=35$, is a trap: the $50$ coffee drinkers are '
          'never in neither.)']),
        ('q-r26-t24-08', 'Of 60 students, 42 take chemistry and 35 take biology. '
                         'What is the greatest possible number of students who take exactly one of these two subjects?',
         ['$7$', '$17$', '$43$', '$60$'], 3,
         ['Exactly one $=42+35-2\\cdot\\text{both}=77-2\\cdot\\text{both}$. It is greatest when "both" is smallest.',
          'Smallest overlap: $42+35-60=17$.',
          'Exactly one: $77-2\\cdot17=77-34=43$. (With the largest overlap, $35$, exactly one is only $77-70=7$.)']),
        ('q-r26-t24-09', 'Of 60 students, 45 study math, 40 study art, and 50 study music. '
                         'What is the smallest possible number of students who study all three?',
         ['$0$', '$15$', '$25$', '$40$'], 2,
         ['Count who misses a subject: no math $60-45=15$, no art $60-40=20$, no music $60-50=10$.',
          'At most $15+20+10=45$ students miss a subject. So, at least $60-45=15$ study all three.',
          'In one line: $45+40+50-2\\cdot60=135-120=15$.']),
        ('q-r26-t24-10', 'A club has 90 members. Of them, 60 play tennis and 45 play golf. '
                         'What is the greatest possible number of members who play tennis but not golf?',
         ['$15$', '$30$', '$45$', '$60$'], 3,
         ['Tennis only $=60-\\text{both}$. It is greatest when "both" is smallest.',
          'Smallest overlap: $60+45-90=15$.',
          'Tennis only: $60-15=45$. ($60$ is impossible: at least $15$ tennis players also play golf.)']),
        ('q-r26-t24-11', 'Of 40 workers, 18 speak Arabic and 15 speak Russian. Which of the following could be the number '
                         'of workers who speak at least one of these two languages?',
         ['$15$', '$30$', '$36$', '$40$'], 2,
         ['At least one $=18+15-\\text{both}=33-\\text{both}$.',
          'Largest overlap $15$: at least one is $18$ (the larger group). No overlap: at least one is $33$ '
          '(less than $40$, therefore it fits).',
          'So, the number is from $18$ to $33$. Only $30$ is in this range (overlap $3$).']),
    ]
    for qid, stem, ch, cor, ex in new:
        M.new_q(qid, TOPIC, stem, ch, cor, ex)
        M.place_q(qid, PRAC)

    M.practice_order(PRAC, ['wp24-p17', 'wp24-p14', 'wp24-p12', 'q-r26-t24-04', 'wp24-p09', 'wp24-p01', 'wp24-p08',
                            'wp24-p11', 'wp24-p15', 'q-r26-t24-11', 'q-r26-t24-07', 'wp24-p16', 'wp24-p03', 'wp24-p06',
                            'wp24-p07', 'wp24-p10', 'q-r26-t24-05', 'q-r26-t24-10', 'wp24-p05', 'q-r26-t24-08',
                            'q-r26-t24-06', 'q-r26-t24-09', 'wp24-p13'])


# =====================================================================================================
# 8. Text clean-up over all topic videos (US spelling, "−" inside words, pre-loaded question text)
# =====================================================================================================
def tidy(M):
    for vid, v in M.D['videos'].items():
        if v['topic'] != TOPIC: continue
        for b in v['beats']:
            for l in b['lines']:
                for k in ('say', 'draw', 'label'):
                    if k in l:
                        for a, z in US: l[k] = l[k].replace(a, z)
            for it in b['items']:
                if it.get('t'):
                    for a, z in US: it['t'] = it['t'].replace(a, z)
                if it.get('k') == 'vis' and isinstance(it.get('v'), dict) and it['v'].get('headers'):
                    it['v']['headers'] = [h.replace('Organiser', 'Organizer') for h in it['v']['headers']]
            qs = [it for it in b['items'][:b['pre']] if it.get('k') == 'q']
            if b['mode'] == 'question' and qs:
                qid = qs[0]['qid']
                sb = v.get('hybrid', {}).get('sidebar', [])
                lab = sb[b['active']] if 0 <= b['active'] < len(sb) else b['title']
                b['loads'] = 'Sidebar with "%s" highlighted; the items listed are already on the canvas.' % lab
                b['canvas'] = 'Pre-loaded — question %s with its four answer choices — "%s"' % (
                    qid, rich_plain(M.q(qid)['stemRich']))
            for k in ('canvas', 'loads'):
                if b.get(k): b[k] = re.sub(r'(?<=[A-Za-z])−(?=[A-Za-z])', '-', b[k])
        if v.get('kind') == 'solution' and v.get('questionId') in M.D['questions']:
            v['title'] = v['navLabel'] = rich_plain(M.q(v['questionId'])['stemRich']).replace('\\%', '%')
        M.touched_videos.add(vid)


def apply(M):
    fix_lesson1(M)
    fix_ranges(M)
    fix_exact(M)
    fix_guided(M)
    guided_only(M)
    two_way(M)
    three_groups(M)
    fix_card(M)
    fix_practice(M)
    M.section_title(ADV, 'More methods and guided examples')
    for qid in ('wp24-g074', 'wp24-g076', 'wp24-p05'):          # stray spaces around the stem
        M.set_q(qid, stem=M.q(qid)['stemRich'].strip())
    tidy(M)
