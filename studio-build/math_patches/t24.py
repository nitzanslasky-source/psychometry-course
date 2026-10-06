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

    # Pass 2: the two original questions stay (restored), with the usual text clean-up
    S('wp24-p02', choices=['$56$', '$34$', '$30$', '$45$'],
      expl=['Adding $26$ and $19$ counts the $11$ students who study both twice. Remove one copy: $26+19-11=34$.',
            'Or split into separate groups: art only $26-11=15$, music only $19-11=8$, both $11$. '
            'Total: $15+8+11=34$.'])
    S('wp24-p04', choices=['$15$', '$16$', '$23$', '$31$'],
      expl=['At least one item: $54+82-31=105$.', 'Neither: $120-105=15$.'])

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

    M.practice_order(PRAC, ['wp24-p02', 'wp24-p17', 'wp24-p14', 'wp24-p04', 'wp24-p12', 'q-r26-t24-04', 'wp24-p09', 'wp24-p01', 'wp24-p08',
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
    pairs_given(M)
    M.section_title(ADV, 'More methods and guided examples')
    for qid in ('wp24-g074', 'wp24-g076', 'wp24-p05'):          # stray spaces around the stem
        M.set_q(qid, stem=M.q(qid)['stemRich'].strip())
    summary(M)
    tidy(M)
    cut_repeats(M)
    add_methods(M)
    practice_methods(M)   # 2026-10-06 practice: new methods (runs last)


# =====================================================================================================
# 9. Pass 2: summary lesson right before the practice
# =====================================================================================================
def summary(M):
    sb = ['Four regions', 'Count each once', 'Maximum overlap', 'Minimum overlap', 'Other regions',
          'The squares method', 'Two-way tables', 'Three groups', 'Before you practice']
    S = lambda k, script: dict(title=sb[k], mode='concept', active=k, pre=[], script=script)
    slides = [
        dict(mode='title', title='Summary', script=[
            "Before you practice — a quick summary of overlapping groups.",
            "Everything important, one idea at a time."]),
        S(0, [
            A("'A only · both · B only · neither' appears", T('A only · both · B only · neither', size=48, gap=40)),
            "Two groups make four regions. Every person lands in exactly one of them.",
            A("'A full group = its only-region + both' appears", T('A full group $=$ its only-region $+$ both', size=46)),
            "Careful: \"music students\" means the WHOLE circle — music only plus both."]),
        S(1, [
            A("'A + B − both + neither = total' appears", T('$A+B-\\text{both}+\\text{neither}=\\text{total}$', size=52, gap=40)),
            "Add both groups — the middle is counted twice. Subtract it once. Then add the ones outside.",
            A("'40 tourists: 22 + 19 − 9 + neither = 40' appears", T('$22+19-9+\\text{neither}=40\\ \\to\\ \\text{neither}=8$', size=46)),
            "Forty tourists. Twenty-two plus nineteen minus nine is thirty-two. Neither: eight."]),
        S(2, [
            A("'Maximum overlap = the smaller group' appears", T('Maximum overlap $=$ the smaller group', size=48, gap=40)),
            "Range questions: a fact is missing, so the overlap is not one number.",
            "The biggest it can be? Put the small group inside the big one.",
            A("'9 and 6 → max 6' appears", T('$9$ and $6$ $\\to$ max $6$', size=48)),
            "Nine and six: six. Nothing to calculate."]),
        S(3, [
            A("'Minimum overlap = (A + B) − total, or 0' appears", T('Minimum overlap $=(A+B)-\\text{total}$, or $0$', size=46, gap=40)),
            "The smallest it must be: how far do the groups go over the total?",
            A("'11 students: 9 + 6 − 11 = 4' appears", T('$11$ students: $\\ 9+6-11=4$', size=48, gap=40)),
            "Fifteen for eleven students: four must be in both.",
            "The sum doesn't pass the total? Then nobody is forced. The minimum is zero, never negative.",
            A("'Fractions: the whole is 1 · Percents: the whole is 100%' appears",
              T('Fractions: the whole is $1$ · Percents: $100\\%$', size=44)),
            "Three quarters plus a third minus one: at least a twelfth."]),
        S(4, [
            A("'Union = A + B − both · Neither = total − union' appears",
              T('Union $=A+B-\\text{both}$ · Neither $=\\text{total}-\\text{union}$', size=42, gap=30)),
            A("'A only = A − both' appears", T('A only $=A-\\text{both}$', size=44, gap=40)),
            "Asked about another region? Find the overlap range first.",
            "Big overlap, small union — and then neither is big. Big overlap, small A only.",
            A("'\"at most\" / \"at least\" → of the thing they ask' appears",
              T('"at most" / "at least" $\\to$ of the thing they ask', size=42)),
            "At least, at most — of WHAT? Ask: to make THIS small, what must the overlap be?"]),
        S(5, [
            A('The strip appears: neither 3 · piano only 6 · both 4 · guitar only 7',
              {'k': 'vis', 'v': {'type': 'table', 'headers': ['Neither', 'Piano only', 'Both', 'Guitar only'],
                                 'rows': [['3', '6', '4', '7']]}, 'w': 1000, 'h': 120, 'gap': 40}),
            "Exact questions: one more fact fixes every region. Use the squares method.",
            "One strip, four boxes. The two brackets share the middle box — the overlap.",
            "Put in the data and fill the boxes like a sudoku. Start from any box they give you.",
            A("'Exactly one = A + B − 2 · both' appears", T('Exactly one $=A+B-2\\cdot\\text{both}$', size=46)),
            "Exactly one: take both away TWICE — it sits inside each group once."]),
        S(6, [
            A("'Two yes/no traits → a table with totals' appears", T('Two yes/no traits $\\to$ a table with totals', size=44, gap=40)),
            "The same people with two traits? Draw a table. Percents? Plug in a hundred.",
            A("'Rows add across · columns add down' appears", T('Rows add across · columns add down', size=44, gap=40)),
            A("'\"of the …\" → that row or column is the whole' appears", T('"of the …" $\\to$ that row or column is the whole', size=44)),
            "Ten percent of the teachers and forty percent of the parents: don't add them, don't average them. Fill the table.",
            "\"Of the people who wear hats\"? Then the hats column is the whole."]),
        S(7, [
            A("'Min in all three = total − the missing ones, or 0' appears",
              T('Min in all three $=$ total $-$ the missing ones, or $0$', size=42, gap=40)),
            "Three groups? Count who misses a group. Everyone else MUST be in all three.",
            A("'A + B + C − 2 · total' appears", T('$A+B+C-2\\cdot\\text{total}$: $\\ 25+24+22-2\\cdot30=11$', size=44, gap=40)),
            "In one line: add the three groups and subtract the total twice.",
            A("'Max in all three = the smallest group' appears", T('Max in all three $=$ the smallest group', size=44, gap=30)),
            "And the most in all three? The smallest group.",
            A("'Pairs given? Max in all three = the smallest pair overlap' appears",
              T('Pairs given? Max in all three $=$ the smallest pair overlap', size=42)),
            "They also give what each pair shares? Then the most in all three is the smallest pair overlap."]),
        S(8, [
            "Before you start, always ask yourself:",
            A('Check 1 appears', T('Range or exact? Is a fact missing?', size=40, gap=30)),
            A('Check 2 appears', T('Which region do they ask about?', size=40, gap=30)),
            A('Check 3 appears', T('To make THIS big or small, what must the overlap be?', size=38, gap=30)),
            A('Check 4 appears', T('"Of the …" — who is the whole?', size=40)),
            "And the traps: \"music students\" is the whole circle, a negative minimum is really zero, and percents of different groups can't be added.",
            "Now it's your turn. Good luck!"]),
    ]
    last = [f['ref'] for f in M.D['flow'] if f['section'] == ADV][-1]
    M.new_video('r26-t24-summary', TOPIC, 'Summary: Overlapping Groups', sb, slides, ADV, after=last)


# =====================================================================================================
# 2026-10-01 elite comparison: three groups when every PAIR overlap is given -> max in all three = the smallest pair
# overlap (the "smallest group" rule stays as the first step). Real exam: 2023_autumn_q2_20.
# =====================================================================================================
def pairs_given(M):
    vid = 'r26-t24-three-groups'     # 1 title, 2 count who is missing, 3 can it be zero?, 4 recap
    M.insert_slides(vid, 3, [dict(mode='concept', title='Pairs given', active=2, script=[
        "One more step. Sometimes they also tell you what each PAIR of groups shares.",
        A("'Chess 40 · drama 35 · music 30; pairs 12, 9, 15' appears",
          T('Chess $40$ · drama $35$ · music $30$\nChess + drama $12$ · chess + music $9$ · drama + music $15$', size=38, gap=40)),
        "Three clubs: forty in chess, thirty-five in drama, thirty in music.",
        "Twelve are in both chess and drama. Nine in chess and music. Fifteen in drama and music.",
        "At most how many are in all three?",
        "Someone in all three is in every pair too. So the all-three group fits inside each pair.",
        D('Circle "9"'),
        "It can't be bigger than the smallest pair: nine.",
        A("'Pairs given? Max in all three = the smallest pair overlap' appears",
          T('Pairs given? Max in all three $=$ the smallest pair overlap', size=40, gap=40)),
        "Not thirty. The smallest group is the ceiling when you know only the groups. The pairs bring it down to nine.",
        D('Write "12 + 9 = 21 ≤ 40 · 12 + 15 = 27 ≤ 35 · 9 + 15 = 24 ≤ 30 → min 0"'),
        "And the least? Here it can be zero: the twelve, the nine and the fifteen can all be different people. Every club has room for them.",
        "So here: from zero to nine.",
    ])])
    M.set_slide(vid, 5, active=3, script=[
        "Let's lock it in.",
        A("'Min in all three = total − everyone who misses a group, or 0' appears",
          T('Min in all three $=$ total minus the missing ones — or $0$', size=40)),
        A("'One line: A + B + C − 2 · total' appears", T('One line: $A+B+C-2\\cdot\\text{total}$', size=40)),
        A("'Max in all three = the smallest group' appears", T('Max in all three $=$ the smallest group', size=40)),
        A("'Pairs given? Max = the smallest pair overlap' appears",
          T('Pairs given? Max $=$ the smallest pair overlap', size=40)),
        D('Circle "or 0"'),
        'Your turn — a guided question.'])
    M.set_sidebar(vid, ['Count who is missing', 'Can it be zero?', 'Pairs given', 'Recap'])

    c = M.card('mem-r26-t24-more')
    c['tables'][1]['rows'].append(['Max in all three, pairs given', 'the smallest pair overlap',
                                   'pairs $12, 9, 15\\to9$'])

    qid = 'q-r26-t24-12'
    M.new_q(qid, TOPIC, 'In a school, 50 students sing in the choir, 45 play in the band, and 40 are in the drama club. '
                        '14 students are in both the choir and the band, 11 are in both the choir and the drama club, '
                        'and 16 are in both the band and the drama club. What is the greatest possible number of students '
                        'who are in all three?',
            ['40', '11', '41', '16'], 2, [
        'A student in all three is also in each of the three pairs. Therefore the number in all three is at most the '
        'smallest pair overlap: $11$.',
        '$11$ is possible: put the $11$ choir and drama students in the band too. Then choir and band only $=14-11=3$, '
        'band and drama only $=16-11=5$. Every group has room: choir $11+3=14\\le50$, band $11+3+5=19\\le45$, '
        'drama $11+5=16\\le40$.',
        'Traps: $40$ is the smallest group (the ceiling only when the pairs are not given), $16$ is the largest pair, '
        'and $41=14+11+16$ adds the pairs.'])
    M.place_q(qid, PRAC, after='wp24-p13')


# =====================================================================================================
# 2026-10-05 cut repeats: the two new lessons back to a short intro; what the guided question right after
# teaches is cut from the lesson; what no question teaches stays (zero case, pairs given, largest <= smallest group).
# =====================================================================================================
def _fix_say(M, vid, n, old, new):
    def fn(lines):
        hit = False
        for l in lines:
            if 'say' in l and old in l['say']:
                l['say'] = l['say'].replace(old, new); hit = True
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
        return lines
    M.edit_lines(vid, n, fn)


def _add_line(M, vid, n, before_say, line, item=None, label=None):
    """Insert one spoken line (+ optional board item) right before the line containing `before_say`."""
    b = M.slide(vid, n); script = []; hit = False
    add = ([A(label, item)] if item is not None else []) + [line]
    for l in b['lines']:
        if not hit and before_say in (l.get('say') or l.get('draw') or l.get('label') or ''):
            script += add; hit = True
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        else: script.append(D(l['draw']))
    assert hit, '%s #%d: not found: %s' % (vid, n, before_say)
    M.set_slide(vid, n, script=script)


def cut_repeats(M):
    # ---- Two-Way Tables: title + one short "Two traits" slide; the glasses example, "Fill the table",
    #      "Percent of what?" and the recap are taught by Question 10 (table, plug in 100, "of the walkers").
    vid = 'r26-t24-two-way'
    M.remove_slides(vid, [3, 4, 5])
    M.set_slide(vid, 2, title='Two traits', active=0, pre=[], script=[
        "Here's the trap with two traits.",
        A("'Percents of different groups: don't add, don't average' appears",
          T("Percents of different groups: don't add, don't average", 40)),
        "Say twenty percent of the women and thirty percent of the men wear glasses.",
        "These percents are of different groups. You cannot add them. You cannot just average them.",
        A("'Plug in 100 → a table with totals' appears", T(r'Plug in $100$ $\to$ a table with totals', 40)),
        "Instead: plug in one hundred, and fill a table — with a total for every row and every column.",
        "Let's see it in a guided question. Try it first."])
    M.set_sidebar(vid, ['Two traits'])
    # "rows add across, columns add down" (cut recap) -> said where Question 10 adds the walk column
    _fix_say(M, 'solve-q-r26-t24-02', 2, 'Forty-eight students walk.',
             'Rows add across, columns add down. Add down the walk column: forty-eight students walk.')
    # follow-up: the recap's board line comes back as a board item at that moment in Question 10
    b = M.slide('solve-q-r26-t24-02', 2); script = []
    for l in b['lines']:
        if 'say' in l and l['say'].startswith('Rows add across'):
            script.append(A("'Rows add across · columns add down' appears", T('Rows add across · columns add down', 36)))
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        else: script.append(D(l['draw']))
    M.set_slide('solve-q-r26-t24-02', 2, script=script)

    # ---- Three Groups: the worked 50-employee example = Question 11 (same two methods) -> cut, keep the rule
    #      in two lines; keep "Can it be zero?" (zero case + max = smallest group) and "Pairs given"
    #      (teacher-approved, no question video teaches them); cut the recap.
    vid = 'r26-t24-three-groups'
    M.remove_slides(vid, [5])
    M.set_slide(vid, 2, title='Count who is missing', active=0, pre=[], script=[
        "At least how many are in ALL three? Turn it around: who is NOT in all three?",
        "Someone who misses at least one group.",
        A("'Min in all three = total minus everyone who misses a group' appears",
          T('Min in all three $=$ total minus everyone who misses a group', 38)),
        "Count the ones missing each group — as if they are all different people. Everyone else MUST be in all three.",
        A("'Same as: A + B + C − 2 · total' appears", T(r'Same as: $A+B+C-2\cdot\text{total}$', 40)),
        "Two groups: the sum minus the total once. Three groups: minus the total twice."])
    _fix_say(M, vid, 4, 'So here: from zero to nine.', "So here: from zero to nine. Now a guided question — try it first.")
    M.set_sidebar(vid, ['Count who is missing', 'Can it be zero?', 'Pairs given'])


# =====================================================================================================
# 2026-10-06 new exam methods (teacher-approved): the hidden total. Card line only. Runs last.
# =====================================================================================================
def add_methods(M):
    c = M.card('mem-overlap')
    k = next(i for i, t in enumerate(c['tips']) if t.startswith('Percents? Stay in percent'))
    c['tips'].insert(k + 1, 'No total given? Look for a natural one: $24$ hours, $7$ days, $100\\%$. '
                            'Awake $18$ hours, at work $10$ hours → both for at least $18+10-24=4$ hours.')


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
    _pm_add(M, 'wp24-p08', [r'Hidden total: no club size is given, but the whole club is a natural total, $1$ ($100\%$). Spanish $+$ Italian $-$ total: $\frac34+\frac58-1=\frac38$. Everyone speaks at least one of the languages, therefore this overlap is exact, not only a minimum.'])
    _pm_add(M, 'wp24-p05', [r'Hidden total: the size of the town is never given. The whole town is $1$. Under 50 and pet owners overlap by at least $\frac45+\frac25-1=\frac15$ of the town, therefore they surely share residents.'])


# ======================================================================================================
# 2026-10-06 renumber pass
# The English course must not look like the teacher's Hebrew course: every Hebrew-derived question (guided wp24-g070 ..
# g078, practice wp24-p01 .. p10) gets a new story (names, groups, setting) and new numbers - same concept, same trap,
# same level, at least the same methods - and every guided solution video is rewritten to match. The Hebrew lesson
# examples (pizza 8/5/4, 12 students 8 and 7, 65% and 55%, 2/3 + 1/2, the 18-member club, 1/5 and 1/3) and the card
# example get new numbers. Order: the two exact questions (g078, g077) move to the start of the advanced group (they
# continue the exact lesson; the range questions follow). Practice clean-up 26 -> 16. Nothing in topic 24 is recorded.
# Runs last.
# ======================================================================================================
RN_RECORDED = set()   # no take of any topic-24 video in ~/Documents/Course.recordings (checked 2026-10-06)


def _rn_strip(cols, row=('', '', '', ''), label='The four-box strip appears'):
    return A(label, {'k': 'vis', 'v': {'type': 'table', 'headers': list(cols), 'rows': [list(row)]}, 'w': 1000, 'h': 120})


def _rn_q(M, qid, stem, choices, correct, expl):
    if qid in RN_RECORDED: return
    M.set_q(qid, stem=stem, choices=choices, correct=correct, expl=expl)


def _rn_video(M, qid, slides):
    """Rewrite the question slides (2, 3, ...) of a guided question's solution video. The pre-loaded question stays."""
    vid = 'solve-' + qid
    if vid in RN_RECORDED: return
    v = M.video(vid)
    assert len(v['beats']) == len(slides) + 1, (vid, len(v['beats']))
    for n, script in enumerate(slides, 2):
        assert v['beats'][n - 1]['mode'] == 'question', (vid, n)
        M.set_slide(vid, n, script=script)


def rn_lessons(M):
    # ---- wp-067 #4 pizza: 8 slices, mushrooms 5, tomatoes 4 (1 to 4)  ==>  6 slices, mushrooms 4, olives 3 (1 to 3)
    M.set_slide(L1, 4, script=[
        "You've all ordered pizza. Six slices.",
        A('The setup appears: 6 slices, mushrooms on 4, olives on 3', T('6 slices · mushrooms on 4 · olives on 3', size=42, gap=30)),
        A('Two pizzas appear, each with 4 mushroom slices shaded', {'k': 'pie', 'fr': [[4, 6], [4, 6]], 'r': 110, 'gap2': 140}),
        'Mushrooms go on four slices — the shaded ones.',
        'Pizza one: put all three olive toppings on mushroom slices.',
        D('On the left pizza, write O on three shaded slices'),
        "Three slices with both. That's the most — there are only three olive toppings.",
        'Pizza two: someone hates mushrooms. Olives go on the plain slices first.',
        D('On the right pizza, write O on the two unshaded slices'),
        'Two used — one olive topping left. And no plain slice is left.',
        D('Write the last O on a shaded slice'),
        'It MUST go on a mushroom slice. At least one slice has both — no way around it.',
        "And a topping is a topping: you can't put olives on the same slice twice.",
        "So: at least one, at most three. That's a range."])

    # ---- wp-068: 12 students, 8 music, 7 sport  ==>  15 students, 10 art, 9 drama
    M.set_slide(L2, 2, script=[
        "In a range question we can't find the exact overlap.",
        'What we CAN find: the maximum possible — and the minimum that must be.',
        A('The example appears: 15 students · 10 take art · 9 take drama', T('15 students · 10 take art · 9 take drama', size=46)),
        'Fifteen students. Ten take art, nine take drama.',
        "How many could take both? Let's hand things out and see."])
    grid = {'k': 'grid', 'rows': 1, 'cols': 15, 'tr': 1, 'tc': 10, 'cell': 64}
    M.set_slide(L2, 3, script=[
        A('Fifteen boxes appear, the first 10 shaded as art students', dict(grid, gap=90)),
        'Fifteen students. The ten shaded ones take art.',
        "Minimum first: we DON'T want drama on art students — so drama goes to the others first.",
        D('Write D in the 5 unshaded boxes'),
        'Five used. Four drama students left — and everyone left takes art.',
        D('Write D in 4 of the shaded boxes'),
        'No choice: four must take both. Minimum — four.',
        A('A second row of fifteen boxes appears', dict(grid)),
        'Now the maximum: make every drama student an art student too.',
        D('Write D in 9 shaded boxes'),
        "Nine both. Can't go higher — there are only nine drama students.",
        'So the overlap is somewhere from four to nine.'])
    s = _script(M, L2, 4)
    s = [D('Write "the smaller of 10 and 9 → 9"') if x == D('Write "the smaller of 8 and 7 → 7"') else x for x in s]
    s = [{'Eight and seven: seven. Nothing to calculate.': 'Ten and nine: nine. Nothing to calculate.',
          'Equal groups? Five and five — the maximum is five.': 'Equal groups? Six and six — the maximum is six.'}.get(x, x)
         if isinstance(x, str) else x for x in s]
    assert D('Write "the smaller of 10 and 9 → 9"') in s and 'Ten and nine: nine. Nothing to calculate.' in s, s
    M.set_slide(L2, 4, script=s)
    M.set_slide(L2, 5, script=[
        A("'Minimum overlap = (A + B) − total' appears", T('Minimum overlap $=(A+B)-\\text{total}$', size=48, gap=80)),
        'The minimum: how far do the two groups go over the total?',
        D('Write 10 + 9 = 19'),
        'Ten plus nine is nineteen.',
        'But there are only fifteen students.',
        D('Write 19 − 15 = 4'),
        'Four too many. Those four have no choice — they must take both.',
        'Picture nineteen places for fifteen students: four students end up holding two.'])
    M.set_slide(L2, 6, script=[
        "What if the groups don't go over the total?",
        A('6 + 9 = 15 appears', T('$6+9=15$ students', size=50, gap=70)),
        'Six art, nine drama, fifteen students. Six plus nine — exactly fifteen.',
        'Hand everything to different students. Nobody has to take both.',
        D('Next to it write "min = 0"'),
        'Minimum zero. Not minus anything.',
        "If the sum doesn't pass the total, no overlap is forced."])
    M.set_slide(L2, 7, script=[
        'So far, they asked about both. The exam also asks about the other regions.',
        'Same fifteen students: ten art, nine drama. The overlap goes from four to nine.',
        A("'Both: from 4 to 9' appears", T('Both: from $4$ to $9$', size=40)),
        'Everything else depends on the overlap. So, find its range first.',
        A("'At least one = A + B − both: from 10 to 15' appears",
          T('At least one $=A+B-\\text{both}$: from $10$ to $15$', size=40)),
        'At least one — the union — is A plus B minus both. Big overlap, small union.',
        D('Write "19 − 9 = 10 · 19 − 4 = 15"'),
        'Overlap nine: union ten — just the larger group. Overlap four: union fifteen — everyone.',
        'So, the union goes from the larger group up to A plus B. But never more than the total.',
        A("'Neither = total − at least one: from 0 to 5' appears",
          T('Neither $=\\text{total}-\\text{at least one}$: from $0$ to $5$', size=40)),
        'Neither is the total minus the union. Neither is big when the union is small.',
        D('Write "15 − 15 = 0 · 15 − 10 = 5"'),
        A("'Art only = A − both: from 1 to 6' appears", T('Art only $=A-\\text{both}$: from $1$ to $6$', size=40)),
        'Art only is art minus both. Here it works backwards: the BIGGER the overlap, the SMALLER art only.',
        D('Write "10 − 9 = 1 · 10 − 4 = 6"'),
        'Art only: from one to six. Its minimum uses the MAXIMUM overlap.'])
    def fn8(lines):
        hit = 0
        for l in lines:
            if l.get('say', '').startswith('"At least how many play music only?"'):
                l['say'] = ('"At least how many take art only?" Art only is small when the overlap is big. '
                            'So, use the MAXIMUM overlap.'); hit += 1
            if l.get('draw') == 'Write "at least … music only → max both → 8 − 7 = 1"':
                l['draw'] = 'Write "at least … art only → max both → 10 − 9 = 1"'; hit += 1
        assert hit == 2, hit
        return lines
    M.edit_lines(L2, 8, fn8)
    M.set_slide(L2, 9, script=[
        "Let's run both rules on one example.",
        A('60% have one property · 50% have another', T('60% have property A · 50% have property B', size=44, gap=70)),
        D('Write max = 50%'),
        'Max: the smaller group — fifty percent.',
        D('Write 60 + 50 − 100 = 10 → min = 10%'),
        'Min: sixty plus fifty is a hundred ten. Ten percent over — so at least ten percent have both.',
        "Or reason it out: forty percent don't have A. Give them B first.",
        D('Write 50 − 40 = 10'),
        'Fifty minus forty: ten percent left, and they must double up. Same answer.',
        'Formula or logic — use whichever feels natural. Most students find the formula — sum minus total — the easiest.'])
    M.set_slide(L2, 10, script=[
        'Fractions work the same way. The whole is one.',
        A('3/5 + 2/3 − 1 = 4/15 appears', T('$\\frac35+\\frac23-1=\\frac{4}{15}$', size=56, gap=60)),
        'Three fifths plus two thirds is nineteen fifteenths — four fifteenths too many. At least four fifteenths are in both.',
        D('Next to it write "max = 3/5"'),
        'And the maximum? The smaller group — three fifths.'])

    # ---- wp-069: 18 members, 10 Spanish, 9 French, 4 neither, 5 both  ==>  25 members, 13 tennis, 11 squash, 5 neither, 4 both
    H4 = ['Neither', 'Tennis only', 'Both', 'Squash only']
    M.set_slide(L3, 2, script=[
        A('The club appears: 25 members · 13 tennis · 11 squash · 5 play neither',
          T('25 members · 13 tennis · 11 squash · 5 play neither', size=44, gap=70)),
        'Twenty-five members. Thirteen play tennis, eleven play squash — and exactly five play neither.',
        'That last fact is what makes it exact.',
        D('Write 25 − 5 = 20'),
        'Five are outside both groups. So the other twenty play at least one sport.',
        D('Write 20 − 13 = 7'),
        'Thirteen of them play tennis. The other seven play no tennis — so they MUST be squash only.',
        D('Write 11 − 7 = 4'),
        'Squash is eleven. Seven are squash only — so four play both.',
        'Four. No choice about it.'])
    M.set_slide(L3, 3, script=[
        'With bigger numbers, use the squares method.',
        "It's the same four regions as the circles — just unrolled into one line.",
        _rn_strip(H4, label='A strip of four boxes appears: Neither · Tennis only · Both · Squash only'),
        'One long strip, four boxes: neither, tennis only, both, squash only.',
        D("Draw a bracket over 'Tennis only' + 'Both' and write 13"),
        'The tennis bracket covers two boxes: tennis only and both.',
        D("Draw a bracket under 'Both' + 'Squash only' and write 11"),
        "Squash covers both and squash only. The two brackets MUST share the middle box — that's the overlap.",
        'All four boxes together make the total — twenty-five.',
        D("Write 5 in 'Neither'"),
        "Now it's sudoku. Neither is five.",
        D("Write 7 in 'Squash only'"),
        'Five plus the whole tennis bracket, thirteen, is eighteen. Twenty-five total — so squash only is seven.',
        D("Write 4 in 'Both' and 9 in 'Tennis only'"),
        'Squash is eleven: seven only, so four both. Tennis only: thirteen minus four, nine.',
        'Check: five, nine, four, seven — twenty-five.'])
    M.set_slide(L3, 4, script=[
        'Same club — but this time they tell us both, and ask for neither.',
        A('The data appears: 25 members · 13 tennis · 11 squash · 4 play both',
          T('25 members · 13 tennis · 11 squash · 4 play both', size=44, gap=40)),
        _rn_strip(H4),
        D("Write 4 in 'Both'"),
        'Both is four.',
        D("Write 7 in 'Squash only'"),
        'Squash is eleven — four both, so seven squash only.',
        'We want neither — so keep moving left.',
        D("Write 13 + 7 = 20, then 5 in 'Neither'"),
        'The tennis bracket is thirteen, plus seven — twenty. Twenty-five total: neither is five.',
        'We never needed tennis only. Fill only the boxes on your path.'])
    M.set_slide(L3, 5, script=[
        'You can start from whichever box the question hands you.',
        A('The data appears: 25 members · 13 tennis · 11 squash · 7 squash only',
          T('25 members · 13 tennis · 11 squash · 7 squash only', size=44, gap=40)),
        _rn_strip(H4),
        D("Write 7 in 'Squash only', then 4 in 'Both'"),
        'Squash only is seven — so both is eleven minus seven, four.',
        D("Write 9 in 'Tennis only', then 5 in 'Neither'"),
        'Tennis only: thirteen minus four, nine. Then nine plus four plus seven is twenty — neither is five.',
        "Same diagram, different starting box. That's why the strip is so powerful."])
    M.set_slide(L3, 6, pre=[T('25 members · 13 tennis · 11 squash · 4 both', size=44, gap=40),
                            {'k': 'vis', 'v': {'type': 'table', 'headers': H4, 'rows': [['5', '9', '4', '7']]},
                             'w': 1000, 'h': 120}], script=[
        'One more region the exam loves: exactly one.',
        'Exactly one means tennis only or squash only — not both.',
        D("Circle the boxes 'Tennis only' and 'Squash only'"),
        'From the strip: nine plus seven — sixteen.',
        A("'Exactly one = A + B − 2 · both' appears", T('Exactly one $=A+B-2\\cdot\\text{both}$', size=46)),
        'Without the strip: add the two groups, and take both away TWICE — it sits inside each group once.',
        D('Write "13 + 11 − 2 · 4 = 16"'),
        'Thirteen plus eleven is twenty-four. Minus eight — sixteen. Same answer.',
        'Or: twenty play at least one sport, four play both. Twenty minus four — sixteen again.'])
    M.set_slide(L3, 7, script=[
        'Now a question that scares a lot of students.',
        A('The overlap is 1/10 of group A and 1/4 of group B',
          T('The overlap is $\\frac1{10}$ of group A and $\\frac14$ of group B', size=42, gap=40)),
        'The overlap is a tenth of group A — and a quarter of group B. How many times bigger is A only than B only?',
        _rn_strip(['Neither', 'A only', 'Both', 'B only'], label='The strip appears'),
        D("Write x in 'Both'"),
        'Call the overlap x. You could even call it one.',
        D("Write 10x over the A bracket, then 9x in 'A only'"),
        "It's a tenth of A — so A is ten x. Take away the overlap: A only is nine x.",
        D("Write 4x under the B bracket, then 3x in 'B only'"),
        "It's a quarter of B — so B is four x. B only is three x.",
        'Nine x against three x — three times as big. A ratio of three to one.',
        'Scary wording. Simple once it\'s in the boxes.'])
    _fix_say(M, L3, 8, 'show forty DIFFERENT items', 'show sixty DIFFERENT items')
    _fix_say(M, L3, 8, 'forty is everyone in at least one', 'sixty is everyone in at least one')

    # ---- memory card example (was the lesson's 12 students: 8 and 7)
    c = M.card('mem-overlap')
    t0, t1 = c['tables'][0], c['tables'][1]
    t0['head'][2] = 'Example ($15$ students: $10$ and $9$)'
    t0['rows'] = [['Maximum overlap', 'the smaller group', '$9$'],
                  ['Minimum overlap', '$(A+B)-\\text{total}$, or $0$ if that is not positive', '$10+9-15=4$']]
    t1['rows'][0][2] = '$10$ to $15$'
    t1['rows'][1][2] = '$0$ to $5$'
    t1['rows'][2][2] = '$10-9=1$ to $10-4=6$'


def rn_guided(M):
    # ---------- g070: 45 campers, flashlight 28, map 23, both 16 -> neither 10
    #            ==>  52 hotel guests, pool 31, gym 26, both 17 -> neither 12
    _rn_q(M, 'wp24-g070', 'Of 52 hotel guests, 31 use the pool, 26 use the gym, and 17 use both. How many use neither?',
          ['$5$', '$14$', '$12$', '$17$'], 3, [
        'Both is $17$, therefore gym only is $26-17=9$.',
        'At least one: the whole pool group plus gym only, $31+9=40$.',
        'Neither: $52-40=12$.',
        'In one line: $52-(31+26-17)=52-40=12$.'])
    _rn_video(M, 'wp24-g070', [[
        'Two groups — pool and gym — and they tell us how many use both.',
        _rn_strip(['Neither', 'Pool only', 'Both', 'Gym only']),
        D("Bracket 'Pool only' + 'Both' → 31; bracket 'Both' + 'Gym only' → 26"),
        D("Write 17 in 'Both'"),
        'Seventeen both.',
        D("Write 9 in 'Gym only'"),
        'Gym is twenty-six: seventeen both, so nine gym only.',
        'Neither is on the far side — move left past the whole pool bracket.',
        D("Write 31 + 9 = 40, then 52 − 40 = 12 in 'Neither'"),
        'Pool bracket, thirty-one, plus nine — forty use at least one. Fifty-two guests: twelve use neither.',
        D('Circle choice 3'),
        'Twelve. Choice three.',
    ], [
        'Or all in one line.',
        D('Write 52 − (31 + 26 − 17) = 12'),
        'Add both groups: fifty-seven. The seventeen in the middle were counted twice — subtract them once: forty.',
        'Fifty-two minus forty. Twelve, again.',
    ]])

    # ---------- g071: 22 machines, cut 14, polish 12, neither 3 -> both 7
    #            ==>  27 printers, color 16, posters 13, neither 3 -> both 5
    _rn_q(M, 'wp24-g071', 'A print shop has 27 printers. Of them, 16 print in color, 13 print large posters, and 3 do neither. '
                          'How many printers both print in color and print large posters?',
          ['$10$', '$8$', '$2$', '$5$'], 4, [
        '$3$ printers do neither, therefore $27-3=24$ do at least one job.',
        'The two jobs add to $16+13=29$. That is $29-24=5$ more than $24$. These $5$ printers were counted twice, '
        'so $5$ do both.'])
    _rn_video(M, 'wp24-g071', [[
        'Neither is given — three. We want both.',
        D('Write 27 − 3 = 24'),
        'Three do neither — twenty-four do at least one job.',
        D('Write 16 + 13 − 24 = 5'),
        'The two jobs add to twenty-nine — five more than twenty-four. Those five were counted twice: they do both.',
        D('Circle choice 4'),
        'Five. Choice four.',
    ], [
        'The same answer on the strip.',
        _rn_strip(['Neither', 'Color only', 'Both', 'Poster only']),
        D("Write 3 in 'Neither'"),
        'Three printers do neither.',
        D("Bracket 'Both' + 'Poster only' → 13"),
        'The poster bracket is thirteen. Neither plus the whole poster bracket: sixteen.',
        D("Write 27 − 16 = 11 in 'Color only'"),
        'Twenty-seven printers, so the last box — color only — is eleven.',
        D("Write 16 − 11 = 5 in 'Both'"),
        'Color is sixteen. Eleven color only — so five do both.',
        'Five again.',
    ]])

    # ---------- g072: both = 1/6 of photography, 1/4 of volunteers -> 5:3
    #            ==>  both = 1/9 of the chess club, 1/4 of the robotics club -> 8:3
    #            (2026-10-06 review: was 1/5 and 1/8 -> 4:7; the Hebrew had 1/5 of the first group -> 4x)
    _rn_q(M, 'wp24-g072', 'The students who are in both the chess club and the robotics club make up $\\frac19$ of the chess club '
                          'and $\\frac14$ of the robotics club. What is the ratio of chess club students who are not in the '
                          'robotics club to robotics club students who are not in the chess club?',
          ['4:9', '8:3', '9:4', '3:8'], 2, [
        'Call the overlap $x$. It is $\\frac19$ of the chess club, therefore the chess club has $9x$ students. '
        'It is $\\frac14$ of the robotics club, therefore the robotics club has $4x$ students.',
        'Chess only: $9x-x=8x$. Robotics only: $4x-x=3x$.',
        'The ratio is $8x:3x=8:3$. The group that does neither is not needed.'])
    _rn_video(M, 'wp24-g072', [[
        'The students in both are a ninth of the chess club — and a quarter of the robotics club.',
        _rn_strip(['Neither', 'Chess only', 'Both', 'Robotics only']),
        D("Write x in 'Both'"),
        'Call the overlap x.',
        D("Write 9x over the chess bracket, then 8x in 'Chess only'"),
        'A ninth of chess — so chess is nine x. Chess only: eight x.',
        D("Write 4x under the robotics bracket, then 3x in 'Robotics only'"),
        'A quarter of robotics — so robotics is four x. Robotics only: three x.',
        'Chess only to robotics only: eight to three.',
        D('Circle choice 2'),
        'Choice two. We never needed the neither group at all.',
        'Watch the trap: nine to four compares the whole clubs — a different question.',
    ], [
        'Prefer numbers? Say two students are in both.',
        D('Write both = 2 → chess 18, robotics 8'),
        'Then eighteen in chess and eight in robotics.',
        D('Write 18 − 2 = 16, 8 − 2 = 6 → ratio 16 : 6 = 8 : 3'),
        'Sixteen chess only, six robotics only. Sixteen to six is eight to three.',
    ]])

    # ---------- g074: 240 guests, 35% organizer, 80% host -> min 15% = 36
    #            ==>  360 guests at a gallery opening, 45% artist, 70% gallery owner -> min 15% = 54
    #            (2026-10-06 review: was a wedding, bride / groom - the Hebrew's own setting)
    _rn_q(M, 'wp24-g074', 'At a gallery opening with 360 guests, 45% know the artist and 70% know the gallery owner. '
                          'What is the minimum number of guests who know both?',
          ['$54$', '$162$', '$108$', '$36$'], 1, [
        '$45\\%+70\\%=115\\%$, but the guests are only $100\\%$. So, at least $115\\%-100\\%=15\\%$ know both.',
        '$15\\%$ of $360$: $10\\%$ is $36$ and $5\\%$ is $18$: $36+18=54$.',
        'This minimum is possible: all $30\\%$ who do not know the owner are in the artist group, and the other '
        '$45\\%-30\\%=15\\%$ of the artist group know the owner.'])
    _rn_video(M, 'wp24-g074', [[
        A('The data appears: total 360 · artist 45% · owner 70%', T('Total 360 · artist 45% · owner 70%', size=42)),
        'First, tidy up the data.',
        'Forty-five percent of three sixty: ten percent is thirty-six, five percent is eighteen. Four times thirty-six, plus eighteen — a hundred sixty-two.',
        D('Write 45% → 144 + 18 = 162'),
        'Seventy percent? Easier through the complement: thirty percent is a hundred eight — so two fifty-two.',
        D('Write 70% → 360 − 108 = 252'),
        'A free reminder: the maximum overlap is the smaller group — a hundred sixty-two. Not needed here, but it costs nothing.',
        'The minimum: how far do the groups go over the total?',
        D('Write 162 + 252 = 414 → 414 − 360 = 54'),
        'Four fourteen against three sixty — fifty-four too many. They must know both.',
        D('Circle choice 1'),
        'Fifty-four. Choice one.',
    ], [
        'Now step back. Why calculate all those counts?',
        D('Write 45 + 70 = 115% → 15% too many'),
        'Forty-five plus seventy: a hundred fifteen percent. Fifteen percent over.',
        D('Write 15% of 360 = 36 + 18 = 54'),
        'Ten percent is thirty-six, five percent is eighteen — fifty-four.',
        'One small calculation. This is the exam way.',
    ], [
        "Let's see it — and review ranges on the way.",
        _rn_strip(['Neither', 'Artist only', 'Both', 'Owner only']),
        D("Write 15% in 'Both', 30% in 'Artist only', 55% in 'Owner only', 0 in 'Neither'"),
        'At the minimum: fifteen both, thirty artist only, fifty-five owner only. Exactly a hundred.',
        "Must it be fifteen? No — that's only the minimum.",
        D('Below the strip write: both 20% → 25% · 50% · neither 5%'),
        'Twenty percent both: then twenty-five artist only and fifty owner only — ninety-five. The last five percent know neither of them.',
        D('Below that write: both 45% → 0% · 25% · neither 30%'),
        'The maximum: the whole artist group inside the owner group — forty-five percent.',
        'So the overlap runs from fifteen to forty-five percent. They asked for the minimum.',
    ]])

    # ---------- g075: 48 students, greenhouse 21, orchard 11, neither could be 14/30/35/18 (18; range 16..27)
    #            ==>  52 students, library 24, kitchen 13, neither could be 36/13/19/31 (19; range 15..28)
    _rn_q(M, 'wp24-g075', 'A class has 52 students. Of them, 24 help in the library and 13 help in the kitchen. '
                          'Which of the following could be the number of students who help in neither place?',
          ['$36$', '$13$', '$19$', '$31$'], 3, [
        'Neither $=52-\\text{union}$, where the union is everyone who helps in at least one place.',
        'Smallest union: all $13$ kitchen helpers also help in the library, therefore the union is $24$. '
        'Largest union: no overlap, $24+13=37$ (less than $52$, therefore it fits).',
        'Neither goes from $52-37=15$ to $52-24=28$. Only $19$ is in this range. It happens when the overlap is $4$: '
        'the union is $24+13-4=33$, and $52-33=19$.'])
    _rn_video(M, 'wp24-g075', [[
        'Neither in a range question. Go through the union — the students in at least one place.',
        D('Write "union: smallest 24 · largest 24 + 13 = 37"'),
        'Smallest union: all thirteen kitchen helpers also help in the library. Twenty-four.',
        "Largest union: no overlap at all. Twenty-four plus thirteen — thirty-seven. That's less than fifty-two — it fits.",
        D('Write "neither = 52 − union: from 52 − 37 = 15 to 52 − 24 = 28"'),
        'Neither is fifty-two minus the union. Big union, small neither.',
        'So, neither goes from fifteen to twenty-eight.',
        D('Cross out choices 1, 2 and 4'),
        'Thirteen is too small. Thirty-six and thirty-one are too big.',
        D('Circle choice 3'),
        'Nineteen. Choice three.',
    ], [
        'For strong students — another way to see it.',
        'Flip it: neither means NOT library and NOT kitchen. An overlap of the two complements.',
        D('Write not library: 52 − 24 = 28 · not kitchen: 52 − 13 = 39'),
        'Twenty-eight not in the library. Thirty-nine not in the kitchen.',
        'Now the range rules — on these two groups.',
        D('Write max = 28'),
        'Max: the smaller group — twenty-eight.',
        D('Cross out choices 1 and 4'),
        'Thirty-six and thirty-one — too big. Out.',
        D('Write 28 + 39 − 52 = 15 → min = 15'),
        'Min: sixty-seven minus fifty-two — fifteen.',
        D('Cross out choice 2'),
        'Thirteen — too small. Out.',
        D('Circle choice 3'),
        'Nineteen sits between fifteen and twenty-eight. Choice three.',
    ], [
        'The fast way. The maximum alone kills two choices.',
        'Two are left — and only one answer can be right.',
        'So one of them is inside the range, and the other is too small.',
        'Which one is too small? The smaller one.',
        D('Cross out 13 and circle 19'),
        'Nineteen — without calculating the minimum at all.',
        'Not trivial — but with practice, it saves you time.',
    ]])

    # ---------- g076: company 2/5 code, 4/5 remote, 1/5 juniors, 1/2 training; not necessarily: juniors & remote (=1)
    #            ==>  hospital nurses 3/10 nights, 3/4 drive, 1/4 new, 1/2 part time; not necessarily: new & drive (=1)
    _rn_q(M, 'wp24-g076', "Of a hospital's nurses, $\\frac{3}{10}$ work night shifts, $\\frac34$ drive to work, $\\frac14$ are new, "
                          "and $\\frac12$ work part time. Which statement is not necessarily true?",
          ['At least one nurse who is not new does not work night shifts', 'At least one night-shift nurse drives to work',
           'At least one new nurse drives to work', 'At least one part-time nurse does not work night shifts'], 3, [
        '"At least one is in both groups" must be true only when the two groups add up to more than the whole.',
        'Choice 1: nurses who are not new and nurses who do not work nights, $\\frac34+\\frac{7}{10}=\\frac{29}{20}>1$ — forced. '
        'Choice 2: $\\frac{3}{10}+\\frac34=\\frac{21}{20}>1$ — forced. '
        'Choice 4: part time and not nights, $\\frac12+\\frac{7}{10}=\\frac65>1$ — forced.',
        'Choice 3: new nurses and nurses who drive, $\\frac14+\\frac34=1$ exactly. This does not force an overlap. '
        'Out of $20$ nurses, the $5$ new nurses can come by bus and the other $15$ drive. '
        'So, choice 3 is not necessarily true.'])
    _rn_video(M, 'wp24-g076', [[
        'Each choice claims an overlap MUST exist. It must — if the two groups add up to more than one whole.',
        D('Choice 1: not new 3/4 + not nights 7/10 = 29/20'),
        'Choice one: nurses who are not new are three quarters, no night shifts seven tenths. Twenty-nine twentieths — more than one. Forced.',
        D('Cross out choice 1'),
        "That statement is true — so it's not our answer.",
        D('Choice 2: nights 3/10 + drive 3/4 = 21/20'),
        'Choice two: three tenths plus three quarters — twenty-one twentieths. More than one. Forced.',
        D('Cross out choice 2'),
        D('Choice 3: new 1/4 + drive 3/4 = 1'),
        'Choice three: a quarter plus three quarters — exactly one.',
        'Exactly one does NOT force an overlap. The groups can sit side by side.',
        D('Circle choice 3'),
        D('Write 20 nurses: 5 new come by bus · 15 not new drive'),
        'Picture twenty nurses: the five new nurses come by bus, the other fifteen drive. Every fraction holds — and no new nurse drives.',
        "So choice three is NOT necessarily true. That's the answer.",
        'And if two groups add up to LESS than one? Even more so — no overlap is forced. The minimum is zero, never negative.',
        'Just to check: choice four — a half plus seven tenths, forced.',
    ], [
        'On the exam, do it in percent. Much faster than adding fractions.',
        D('Write nights 30 · drive 75 · new 25 · part time 50 · not nights 70 · not new 75'),
        'Nights thirty, drive seventy-five, new twenty-five, part time fifty. Not nights seventy, not new seventy-five.',
        D('Choice 1: 75 + 70 = 145 · Choice 2: 30 + 75 = 105 · Choice 3: 25 + 75 = 100'),
        'Choice one: a hundred forty-five — forced. Choice two: a hundred five — forced. Choice three: exactly a hundred — not forced.',
        D('Circle choice 3'),
        'Choice three, again. This is the way to do it on the exam — percent is much faster than fractions.',
    ]])

    # ---------- g077: staff 2/5 soup, 1/4 salad, 1/10 both = 8 people -> 80, neither 36
    #            ==>  conference 1/4 morning, 1/6 evening, 1/12 both = 4 people -> 48, neither 32
    #            (2026-10-06 review: was 1/3, 1/5, 1/12 = 5 -> 60; the Hebrew had 1/3, 1/5 and 60 people)
    _rn_q(M, 'wp24-g077', 'At a conference, $\\frac14$ of the participants attend the morning workshop, $\\frac16$ attend the '
                          'evening workshop, and $\\frac1{12}$ attend both. Exactly 4 participants attend both. '
                          'How many participants attend neither workshop?',
          ['$16$', '$32$', '$12$', '$28$'], 2, [
        '$\\frac1{12}$ of the participants is $4$ people, therefore there are $4\\cdot12=48$ participants.',
        'Morning: $\\frac14\\cdot48=12$. Evening: $\\frac16\\cdot48=8$. At least one: $12+8-4=16$.',
        'Neither: $48-16=32$.'])
    _rn_video(M, 'wp24-g077', [[
        'Squares method, with fractions this time. The whole is one.',
        _rn_strip(['Neither', 'Morning only', 'Both', 'Evening only']),
        D("Write 1/12 in 'Both'"),
        'Both: a twelfth.',
        D("Write 1/6 − 1/12 = 1/12 in 'Evening only'"),
        'Evening is a sixth. A sixth minus a twelfth — two twelfths minus one twelfth: one twelfth.',
        'We want neither, so keep moving left. Not morning is three quarters.',
        D("Write 3/4 − 1/12 = 8/12 in 'Neither'"),
        'Three quarters is nine twelfths. Minus one — eight twelfths.',
        'But the answers are people. A twelfth is four people.',
        D('Write 1/12 = 4 people → 8/12 = 8 · 4 = 32'),
        'Eight twelfths: eight times four — thirty-two people.',
        D('Circle choice 2'),
        'Thirty-two. Choice two.',
    ], [
        'Better: skip the fractions altogether.',
        D('Write 1/12 = 4 → total 48'),
        'A twelfth is four people — so there are forty-eight participants.',
        D('Write morning 12 · evening 8 · not morning 36'),
        'Morning: a quarter of forty-eight, twelve. Evening: a sixth, eight. Not morning: thirty-six.',
        D('Write 8 − 4 = 4 evening only · 36 − 4 = 32 neither'),
        'Evening only: eight minus four, four. Neither: thirty-six minus four — thirty-two.',
        'This is how I want you working on the exam: find the people, then fill the boxes.',
    ]])

    # ---------- g078: butterflies 31 and 22, 40 different -> both 13
    #            ==>  movies 34 and 27, 45 different -> both 16 (2026-10-06 review: was bird species; the Hebrew had owls)
    _rn_q(M, 'wp24-g078', 'Two friends list the movies they watched this year. One lists 34 movies and the other lists 27. '
                          'Together, their lists show 45 different movies. How many movies appear on both lists?',
          ['$16$', '$11$', '$7$', '$18$'], 1, [
        'The $45$ movies are the ones on at least one list (the union), therefore neither is $0$.',
        'The first friend has $34$ of the $45$. The other $45-34=11$ appear only on the second list.',
        'Both: $27-11=16$. Check: $34+27-16=45$.'])
    _rn_video(M, 'wp24-g078', [[
        'Forty-five different movies — watched by at least one of them.',
        "They didn't say forty-five movies came out this year. They said the lists show forty-five.",
        D('Write neither = 0'),
        "So no movie is in neither. Neither is zero — it's implied.",
        D('Write 45 − 34 = 11'),
        'The first friend covers thirty-four of the forty-five. The other eleven are only on the second list.',
        D('Write 27 − 11 = 16'),
        'The second list has twenty-seven: eleven new, so sixteen shared.',
        D('Circle choice 1'),
        'Sixteen. Choice one.',
    ], [
        'Same thing on the strip.',
        _rn_strip(['Neither', 'First only', 'Both', 'Second only'], ('0', '', '', ''),
                  label='The four-box strip appears, neither = 0'),
        D("Write 45 − 34 = 11 under 'Neither' + 'Second only'"),
        "Not on the first list: forty-five minus thirty-four — eleven. That's neither plus second only.",
        D("Write 11 in 'Second only', then 27 − 11 = 16 in 'Both'"),
        'Neither is zero, so second only is eleven — and both is sixteen.',
        "When neither is zero, that's the box you start from. Watch for it in the wording.",
    ]])


def rn_order(M):
    """The two exact questions (g078 reading trap, g077 fractions) open the advanced group: they continue the exact lesson
    that ends just before; the range questions (g074, g075, the at-least trap, g076) follow. renumber_guided() renumbers."""
    for ref in ('wp24-g078', 'solve-wp24-g078', 'wp24-g077', 'solve-wp24-g077'):
        M.move(ref, ADV, before='wp24-g074')


def rn_practice_questions(M):
    # p01: 150 winners, 65% nearby, 55% train -> min 20% = 30  ==>  160 buyers, 72% students, 53% card -> 25% = 40
    _rn_q(M, 'wp24-p01', 'At a book fair, 160 different visitors each buy one book. Of the buyers, 72% are students and 53% pay '
                         'by card. What is the minimum number of buyers who are students and pay by card?',
          ['$16$', '$40$', '$25$', '$48$'], 2, [
        '$72\\%+53\\%=125\\%$ of the buyers, but there are only $100\\%$. '
        'So, at least $125\\%-100\\%=25\\%$ are in both groups.', '$25\\%$ of $160$ is $\\frac14\\cdot160=40$.'])
    # p02: art 26, music 19, both 11, all in at least one -> 34  ==>  basketball 31, volleyball 24, both 13 -> 42
    _rn_q(M, 'wp24-p02', 'Every member of a sports club plays basketball, volleyball, or both. There are 31 basketball players, '
                         '24 volleyball players, and 13 members who play both. How many members does the club have?',
          ['$55$', '$68$', '$42$', '$29$'], 3, [
        'Adding $31$ and $24$ counts the $13$ members who play both twice. Remove one copy: $31+24-13=42$.',
        'Or split into separate groups: basketball only $31-13=18$, volleyball only $24-13=11$, both $13$. '
        'Total: $18+11+13=42$.'])
    # p03: 3/5 get a company tablet = 72, 1/2 personal -> 120, min 12  ==>  3/4 bus pass = 135, 2/5 bicycle -> 180, min 27
    _rn_q(M, 'wp24-p03', 'A school gives a free bus pass to $\\frac34$ of its students, using 135 passes. $\\frac25$ of all the '
                         'students also have a bicycle. What is the minimum number of students who have both a bus pass and '
                         'a bicycle?',
          ['$45$', '$0$', '$27$', '$72$'], 3, [
        '$\\frac34$ of the students is $135$, therefore $\\frac14$ is $135\\div3=45$ and the total is $45\\cdot4=180$.',
        'Bicycles: $\\frac25\\cdot180=72$.', 'Minimum overlap: $135+72-180=27$.'])
    # p04: 120 hikers, map 54, compass 82, both 31 -> neither 15  ==>  140 runners, cap 63, sunglasses 88, both 36 -> 25
    _rn_q(M, 'wp24-p04', 'Of 140 runners in a race, 63 wear a cap, 88 wear sunglasses, and 36 wear both. '
                         'How many runners wear neither?',
          ['$27$', '$25$', '$36$', '$11$'], 2, [
        'At least one item: $63+88-36=115$.', 'Neither: $140-115=25$.'])
    # p05: town 3/5 cycle, 1/4 vegetables, 2/5 pets, 4/5 under 50; forced: under 50 & pets
    #      ==>  city 2/3 walk to work, 1/4 own a dog, 1/3 have a garden, 3/4 under 60; forced: under 60 & garden
    _rn_q(M, 'wp24-p05', 'In a city, $\\frac23$ of the residents walk to work, $\\frac14$ own a dog, $\\frac13$ have a garden, '
                         'and $\\frac34$ are under 60. Which of the following groups necessarily contains at least one resident?',
          ['Residents who walk to work and own a dog', 'Residents aged 60 or over who own a dog',
           'Residents under 60 who have a garden', 'Residents who walk to work and have a garden'], 3, [
        'Two groups must overlap only when they add up to more than the whole.',
        'Under 60 and garden owners: $\\frac34+\\frac13=\\frac{13}{12}>1$ — forced.',
        'The others: walkers and dog owners, $\\frac23+\\frac14=\\frac{11}{12}<1$. '
        'Aged 60 or over and dog owners, $\\frac14+\\frac14=\\frac12<1$. '
        'Walkers and garden owners, $\\frac23+\\frac13=1$ — not more than $1$. '
        'These groups can be separate.',
        'Hidden total: the size of the city is never given. The whole city is $1$. Under 60 and garden owners overlap by at '
        'least $\\frac34+\\frac13-1=\\frac1{12}$ of the city, therefore they surely share residents.'])
    # p06: 60 trainees 0-12; 26 in 9-12, 24 in 7-10, 20 below 7 -> 9-10: 10
    #      ==>  70 applicants 0-20; 31 in 15-20, 26 in 11-16, 24 below 11 -> 15-16: 11
    _rn_q(M, 'wp24-p06', 'Each of 70 applicants gets a score from 0 to 20. Of them, 31 score from 15 to 20, 26 score from 11 to 16, '
                         'and 24 score below 11. How many applicants score from 15 to 16? (All ranges include both ends.)',
          ['$15$', '$11$', '$9$', '$13$'], 2, [
        'Together, the bands "15 to 20" and "11 to 16" cover every score from 11 to 20. Everyone who does not score '
        'below 11 is in at least one band: $70-24=46$.',
        'The two bands share the scores 15 to 16. That is the overlap: $31+26-46=11$.'])
    # p07: 250 students, chess 205, instrument 190 -> max neither 45 = 18%
    #      ==>  300 hotel guests, breakfast 249, pool 216 -> max neither 51 = 17%
    _rn_q(M, 'wp24-p07', 'Of 300 hotel guests, 249 eat breakfast at the hotel and 216 use the pool. What is the greatest possible '
                         'percentage of guests who neither eat breakfast at the hotel nor use the pool?',
          ['$28\\%$', '$17\\%$', '$45\\%$', '$11\\%$'], 2, [
        'Neither $=300-\\text{union}$. Neither is greatest when the union is smallest.',
        'The union is at least the larger group, $249$. It is exactly $249$ when all $216$ pool users also eat breakfast.',
        'Neither: $300-249=51$, and $\\frac{51}{300}=\\frac{17}{100}=17\\%$.'])
    # p08: Spanish 3/4, Italian 5/8, all in at least one -> 3/8  ==>  pizza 4/5, cake 2/3 -> 7/15
    _rn_q(M, 'wp24-p08', 'Every guest at a party ate pizza, cake, or both. The guests who ate pizza are $\\frac45$ of the guests, '
                         'and the guests who ate cake are $\\frac23$. What fraction of the guests ate both?',
          ['$\\frac{1}{5}$', '$\\frac{8}{15}$', '$\\frac{7}{15}$', '$\\frac{1}{3}$'], 3, [
        'Everyone is in at least one group, therefore neither is $0$.',
        'Both: $\\frac45+\\frac23-1=\\frac{12}{15}+\\frac{10}{15}-\\frac{15}{15}=\\frac{7}{15}$.',
        'Hidden total: the number of guests is not given, but all the guests are a natural total, $1$ ($100\\%$). '
        'Pizza $+$ cake $-$ total: $\\frac45+\\frac23-1=\\frac{7}{15}$. Everyone ate at least one of them, therefore this '
        'overlap is exact, not only a minimum.'])
    # p09: 48 students, swim 28, cycle 24, 3/4 of cyclists swim -> neither 14
    #      ==>  56 members, hike 30, kayak 25, 3/5 of kayakers hike -> neither 16
    _rn_q(M, 'wp24-p09', 'A youth group has 56 members. Of them, 30 hike and 25 kayak. Three fifths of the kayakers also hike. '
                         'How many members do neither activity?',
          ['$15$', '$10$', '$16$', '$26$'], 3, [
        'Both: $\\frac35\\cdot25=15$.', 'At least one: $30+25-15=40$. Neither: $56-40=16$.'])
    # p10: bags 2/3 blue, 3/4 zips, 1/2 both -> 1/6 : 1/4 = 2:3
    #      ==>  cars 3/5 white, 4/5 four doors, 1/2 both -> 1/10 : 3/10 = 1:3
    _rn_q(M, 'wp24-p10', 'Of the cars in a parking lot, $\\frac35$ are white, $\\frac45$ have four doors, and $\\frac12$ are white '
                         'cars with four doors. What is the ratio of white cars without four doors to four-door cars that are '
                         'not white?',
          ['3:1', '1:3', '3:4', '1:2'], 2, [
        'White without four doors: $\\frac35-\\frac12=\\frac1{10}$. Four doors but not white: $\\frac45-\\frac12=\\frac3{10}$.',
        'The ratio is $\\frac1{10}:\\frac3{10}$. Multiply both parts by $10$: the ratio is $1:3$.'])


def rn_practice(M):
    """Approved clean-up (26 -> 16): no copies in this topic; keep 3 extra-bank items (p13 three groups / zero case,
    p16 the at-least-only trap, p17 exactly one); keep the September items of a type the Hebrew practice does not have
    and no guided question already drills (q-05 two-way table with percents, q-09 three groups, q-12 pairs given)."""
    N = lambda k: 'q-r26-t24-' + k
    out = [
        'wp24-p11',   # range of both: the overlap range (p01, p03, guided Q4)
        'wp24-p12',   # exactly one with neither given: p17 + the lesson's "exactly one"
        'wp24-p14',   # "of the French pupils": the "of the" whole, guided Q10 and q-05
        'wp24-p15',   # both from neither in percent: guided Q2 / p04
        N('04'),      # girls / glasses table by counts: the table, kept in q-05
        N('06'),      # "of the chess players": the same as guided Q10
        N('07'),      # greatest neither: the same as p07
        N('08'),      # greatest exactly one: the range of a region, as p07 / p16
        N('10'),      # greatest tennis only: the range of an only-region, as p16 and guided q-r26-t24-01
        N('11'),      # could be the union: the same as guided Q5 (could be neither)
    ]
    for qid in out:
        assert M.section_of(qid) == PRAC, qid
        M.unplace(qid)
    M.practice_order(PRAC, [
        'wp24-p02', 'wp24-p17', 'wp24-p04', 'wp24-p09', 'wp24-p01', 'wp24-p08', 'wp24-p16', 'wp24-p03', 'wp24-p06',
        'wp24-p07', 'wp24-p10', N('05'), 'wp24-p05', N('09'), 'wp24-p13', N('12')])


def renumber_pass(M):
    rn_lessons(M)
    rn_guided(M)
    rn_order(M)
    rn_practice_questions(M)
    rn_practice(M)
    tidy(M)   # video titles and pre-loaded question text follow the new stems


_apply_before_renumber = apply


def apply(M):
    _apply_before_renumber(M)
    renumber_pass(M)   # 2026-10-06 renumber pass: runs last
