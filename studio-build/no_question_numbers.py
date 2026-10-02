"""No question numbers inside videos (teacher decision 2026-10-01).

A number recorded into a video can never change, so adding / removing / reordering questions would break it.
Videos therefore never show or say a question's number; the website numbers questions itself (export_student.py).

Applied by build_verbal.py just before writing the studio:
- solution videos: the "Question N" title slide is removed; its spoken opener moves (without the number) to the start
  of the first real slide ("Question seven — a hard one." -> "This one is a hard one."; "First guided question." -> dropped)
- the slide sidebar no longer lists "Question 1 … Question 13": it lists this video's own slides (methods / steps),
  the current one highlighted
- video titles lose a leading "Question N · "
- spoken / written references to question numbers in lessons are reworded (REWORD); report() lists anything left
"""
import re

_W = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen ' \
     'eighteen nineteen twenty'.split()
NUM = r'(?:\d+|' + '|'.join(sorted(_W, key=len, reverse=True)) + r'|twenty-\w+|thirty(?:-\w+)?|forty(?:-\w+)?)'
ORD = r'(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|\w+th)'
QREF = re.compile(r'\b[Qq]uestions? (?:number )?' + NUM + r'\b', re.I)

# exact rewordings of lesson lines that point at numbered questions (old text -> new text)
# (lines about the REAL exam's order - "Questions 1–6 of the section", "why is this question number 6?", "the answer
#  to question two ... question three" in reading - are about NITE positions, not course numbers, and stay)
REWORD = {
    'This exact one is Question 1 — so try it yourself first.': 'This exact one is your next question — so try it yourself first.',
    "All ones is the fastest first try. It often works — you'll see it in Questions 3 and 4.":
        "All ones is the fastest first try. It often works — you'll see it in the questions that follow.",
    "And if a question GIVES you the value of a block — say, a plus b equals five — put the number in its place. You'll practise that after Question 12.":
        "And if a question GIVES you the value of a block — say, a plus b equals five — put the number in its place. You'll practise that in the questions ahead.",
    'Sometimes you must multiply one equation first — by five, say — so the unwanted letter cancels. Question fourteen does exactly that.':
        'Sometimes you must multiply one equation first — by five, say — so the unwanted letter cancels. One of the questions ahead does exactly that.',
    "You'll see a bigger one in question seven.": "You'll see a bigger one in the questions ahead.",
    'Sometimes you must multiply one equation first — by four, say — so the unwanted letter cancels. Question fourteen does exactly that.':
        'Sometimes you must multiply one equation first — by four, say — so the unwanted letter cancels. One of the questions ahead does exactly that.',
    "You'll see a bigger one in question six.": "You'll see a bigger one in the questions ahead.",
    'You will see this in questions fourteen, sixteen, seventeen and eighteen.': 'You will see this in several of the questions ahead.',
    'In question fifteen we do this with a sum and a difference.': 'In one of the questions ahead we do this with a sum and a difference.',
    "Same with division: flip it into a multiplication. We'll do that in question seven.":
        "Same with division: flip it into a multiplication. We'll do that in one of the questions ahead.",
    "You'll see this idea again in question four.": "You'll see this idea again in the questions ahead.",
    "On the exam it often hides inside a fraction. Factor, then cancel. You'll see it in Question 13.":
        "On the exam it often hides inside a fraction. Factor, then cancel. You'll see it in the questions ahead.",
    "That's how we solved question sixteen.": "That's how we solved one of the earlier questions.",
    'Two questions on this next — then question nineteen, a product of two ranges.': 'Two questions on this next — then one with a product of two ranges.',
    'In Question 1, one side was horizontal. That made the base and the height easy. What if no side is?':
        'Earlier, one side was horizontal. That made the base and the height easy. What if no side is?',
    'If one side is horizontal or vertical — like in Question 1 — use it as the base. The height is a straight drop.':
        'If one side is horizontal or vertical — like in the earlier question — use it as the base. The height is a straight drop.',
    # openers of solution videos that don't follow the usual patterns
    'Integer question one.': 'An integer question.',
    "This is exactly where people slip. You'll see it in the third question.": "This is exactly where people slip. You'll see it in the questions ahead.",
    'The boxes again — the same question as Question eight, with the same numbers.': 'The boxes again — the same question as before, with the same numbers.',
}
KEEP = {('solve-vr40-g005', 'So why is this question number 6?'), ('vr40-intro', 'Questions 1–6 of the section'),
        ('vr49-method', 'answer to question two'), ('vr49-method', 'jump straight to question three')}


def _opener(line):
    """Spoken line from the old title slide -> the same line without a number (None = drop it)."""
    s = REWORD.get(line.strip(), line.strip())
    if re.fullmatch(ORD + r' guided question\.?', s, re.I):
        return None
    m = re.fullmatch(r'Question ' + NUM + r'(?:\s*[—–-]\s*(.+?))?\.?', s, re.I)
    if m:
        rest = (m.group(1) or '').strip()
        return ('This one is ' + rest + '.') if rest else None
    s = re.sub(r'\s*[—–-]\s*question ' + NUM + r'\.?$', '.', s, flags=re.I)        # "Advanced motion — question nine."
    s = re.sub(r'([.!?])\s*Question ' + NUM + r'\.$', r'\1', s, flags=re.I)        # "Factor questions. Question seven."
    m = re.match(r'Question ' + NUM + r'\s*[.:]\s*(.+)$', s, re.I)                 # "Question two: a queue of vehicles."
    if m:
        s = m.group(1)
        s = s[:1].upper() + s[1:]
    # course-order words: "Second system question." / "Last question of the set. A hard one." / "Third question: the range."
    s = re.sub(r'([.!?])\s*(?:' + ORD + r'|last) question\.$', r'\1', s, flags=re.I)        # "Advanced number line. First question."
    s = re.sub(r'^The (?:' + ORD + r'|last) chart:', 'A new chart:', s, flags=re.I)           # chart sets
    m = re.match(r'(?:' + ORD + r'|last) question on the ([^.—–:]+?)(?=\s*[.:—–]|$)', s, re.I)  # "Second question on the weddings."
    if m:
        s = 'Another question on the ' + m.group(1) + s[m.end():]
    m = re.match(r'(?:our )?(?:' + ORD + r'|last)\s+((?:[\w-]+\s+){0,2}?)question(?:\s+(?:of|in)\s+(?:the|this)\s+set)?(?=\s*[.:—–-]|$)', s, re.I)
    if m and not re.search(r'\bsection\b', s, re.I):
        kind, tail = (m.group(1) or '').strip(), s[m.end():]
        if kind:
            s = ('An ' if kind[0].lower() in 'aeiou' else 'A ') + kind + ' question' + tail
        else:
            tail = tail.lstrip(' .:—–-')
            s = tail[:1].upper() + tail[1:]
    return s or None


def apply(D):
    n = 0
    for v in D['videos'].values():
        beats = v.get('beats') or []
        if v.get('kind') == 'solution' and len(beats) > 1 and beats[0].get('mode') == 'title' \
                and re.fullmatch(r'Question \d+', beats[0].get('bigTitle') or ''):
            intro = [x for x in (_opener(l['say']) for l in beats[0].get('lines') or [] if l.get('say')) if x]
            beats = v['beats'] = beats[1:]
            beats[0]['lines'] = [{'say': x} for x in intro] + (beats[0].get('lines') or [])
            hy = v.get('hybrid')
            if hy is not None:
                hy['sidebar'] = [b.get('title') or 'Solution' for b in beats]
            for i, b in enumerate(beats):
                b['active'] = i
                b['number'] = i + 1
            n += 1
        v['title'] = re.sub(r'^Question \d+\s*·\s*', '', v.get('title') or '')
        for b in v.get('beats') or []:
            for l in b.get('lines') or []:
                for k in ('say', 'draw', 'label'):
                    if l.get(k) in REWORD:
                        l[k] = REWORD[l[k]]
            if b.get('script') in REWORD:
                b['script'] = REWORD[b['script']]
    return n


def report(D):
    """Every remaining place a video shows or says a question number."""
    out = []
    for vid, v in D['videos'].items():
        for side in (v.get('hybrid') or {}).get('sidebar') or []:
            if QREF.search(side): out.append((vid, 'sidebar', side))
        for i, b in enumerate(v.get('beats') or []):
            for k in ('title', 'bigTitle', 'nextCue', 'script'):
                if isinstance(b.get(k), str) and QREF.search(b[k]): out.append((vid, i, b[k][:140]))
            for l in b.get('lines') or []:
                for k in ('say', 'draw', 'label'):
                    if isinstance(l.get(k), str) and QREF.search(l[k]) and not any(vid == a and t in l[k] for a, t in KEEP):
                        out.append((vid, i, l[k][:140]))
    return out
