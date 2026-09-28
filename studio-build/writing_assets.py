"""Figures for the Writing Task lessons (topic 50): a re-created exam page and answer sheet.

These imitate the LOOK of the NITE writing-task page and 50-line answer sheet so students know what to expect,
but use an ORIGINAL prompt and our own wording of the public instructions - no NITE exam page is copied.

Use in modulesV50*.py:   from writing_assets import TASK_PAGE, ANSWER_SHEET, task_page, prompt_box
   A('exam page appears', TASK_PAGE)          # full page, portrait
   A('answer sheet appears', ANSWER_SHEET)
   A('prompt appears', prompt_box(['line 1', 'line 2', ...], 'In your opinion, ...? Give reasons.'))
"""
from xml.sax.saxutils import escape as _e

INK = '#1f2937'; MUTED = '#6b7280'; RULE = '#cbd5e1'; ACCENT = '#2F6BFF'; PAPER = '#ffffff'

EXAMPLE_PROMPT = [
    'In recent years, some cities have allowed schools to move to a four-day',
    'school week. Supporters say that a longer weekend lets students rest and',
    'pursue other interests, and that it saves money on transport and heating.',
    'Opponents warn that longer school days tire young children and that',
    'working parents will struggle to arrange care on the fifth day.',
]
EXAMPLE_QUESTION = 'In your opinion, should schools move to a four-day week? Give reasons.'


def _text(x, y, s, size=13, weight=400, color=INK, anchor='start', italic=False):
    st = ' font-style="italic"' if italic else ''
    return ('<text x="%g" y="%g" font-family="Georgia, \'Times New Roman\', serif" font-size="%g" font-weight="%d" '
            'fill="%s" text-anchor="%s"%s>%s</text>') % (x, y, size, weight, color, anchor, st, _e(s))


def _wrap(s, n):
    out, cur = [], ''
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return out + ([cur] if cur else [])


def _svg(w, h, body, label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s"><title>%s</title>'
            '<rect x="0" y="0" width="%d" height="%d" fill="%s" stroke="#94a3b8" stroke-width="1.5"/>%s</svg>') % (
        w, h, _e(label), _e(label), w, h, PAPER, body)


def task_page_svg(prompt_lines=EXAMPLE_PROMPT, question=EXAMPLE_QUESTION):
    W, H = 600, 780
    b = [_text(W / 2, 46, 'Verbal Reasoning – Writing Task', 20, 700, anchor='middle'),
         '<line x1="40" y1="62" x2="560" y2="62" stroke="%s" stroke-width="1.2"/>' % INK]
    instr = ['This section consists of a writing task.', 'The time allotted is 35 minutes.',
             'Read the task carefully and write your essay on the lined answer sheet.',
             'The essay must be at least 25 lines long and must not go beyond the',
             'lines of the answer sheet. Scrap paper: use the pages in the test booklet',
             '(the draft is not marked).',
             'Write in a style suited to academic writing. Make sure the essay is',
             'well organized and written in clear, correct language.',
             'Write in pencil, legibly and neatly.']
    y = 96
    for s in instr:
        b.append(_text(52, y, s, 13.5, color=INK)); y += 21
    y += 18
    box_top = y
    b.append(_text(W / 2, y + 26, 'Writing Task', 16, 700, anchor='middle'))
    y += 58
    for s in prompt_lines:
        b.append(_text(64, y, s, 14)); y += 23
    y += 12
    for q in _wrap(question, 64):
        b.append(_text(64, y, q, 14, 700)); y += 22
    b.insert(0, '')
    b.append('<rect x="40" y="%g" width="520" height="%g" fill="none" stroke="%s" stroke-width="1.6"/>' % (box_top, y - box_top + 8, INK))
    H = max(620, int(y + 90))
    b.append(_text(W / 2, H - 28, 'Re-created example page · original task written for this course', 11, 400, MUTED, 'middle', True))
    return _svg(W, H, ''.join(b), 'Writing task page (re-created example with an original task)')


def answer_sheet_svg(filled_lines=0):
    W, H = 600, 780
    b = [_text(W / 2, 40, 'Writing Task – Answer Sheet', 18, 700, anchor='middle'),
         _text(W / 2, 62, 'Write only on the lines. Anything outside the lines is not read.', 12, 400, MUTED, 'middle', True)]
    top, gap, n = 84, 13.2, 50
    for i in range(n):
        y = top + i * gap
        b.append('<line x1="62" y1="%g" x2="510" y2="%g" stroke="%s" stroke-width="0.8"/>' % (y, y, RULE))
        if (i + 1) % 5 == 0 or i == 0:
            b.append(_text(52, y + 1, str(i + 1), 9, 400, MUTED, 'end'))
    # the 25-line minimum and the 30-40 recommended zone
    y25 = top + 24 * gap
    b.append('<line x1="62" y1="%g" x2="510" y2="%g" stroke="%s" stroke-width="2"/>' % (y25, y25, '#dc2626'))
    b.append(_text(518, y25 + 4, 'minimum 25', 11, 700, '#dc2626'))
    b.append('<rect x="62" y="%g" width="448" height="%g" fill="%s" opacity="0.08"/>' % (top + 29 * gap, 10 * gap, ACCENT))
    b.append(_text(518, top + 35 * gap, 'good: 30–40', 11, 700, ACCENT))
    b.append(_text(518, top + 49 * gap + 4, 'maximum 50', 11, 700, MUTED))
    for i in range(min(filled_lines, n)):
        y = top + i * gap - 3
        b.append('<path d="M70 %g q 55 -4 110 0 t 110 0 t 110 0 t 100 0" fill="none" stroke="#475569" stroke-width="1"/>' % y)
    b.append(_text(W / 2, H - 20, 'Re-created example sheet', 11, 400, MUTED, 'middle', True))
    return _svg(W, H, ''.join(b), 'Writing task answer sheet with 50 lines')


def vis(svg, w=560, h=730):
    return dict(k='vis', v={'type': 'geometry', 'svg': svg}, w=w, h=h)


TASK_PAGE = vis(task_page_svg())
ANSWER_SHEET = vis(answer_sheet_svg())


def task_page(prompt_lines, question):
    return vis(task_page_svg(prompt_lines, question))


def prompt_box(prompt_lines, question, w=1000, h=None):
    """Just the boxed task (landscape) for question-analysis slides."""
    W = max(800, int(w * 0.8)); y = 40; b = []   # ~26px text on the board
    for s in prompt_lines:
        b.append(_text(24, y, s, 21)); y += 30
    y += 8
    for q in _wrap(question, int((W - 48) / 10.5)):
        b.append(_text(24, y, q, 21, 700)); y += 29
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Writing task"><title>Writing task</title>'
           '<rect x="1" y="1" width="%d" height="%d" fill="#fff" stroke="%s" stroke-width="2"/>%s</svg>') % (W, y, W - 2, y - 2, INK, ''.join(b))
    return dict(k='vis', v={'type': 'geometry', 'svg': svg}, w=w, h=h or int(w * y / W))
