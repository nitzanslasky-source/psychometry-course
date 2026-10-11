"""Memory tricks for the English course (teacher approved ~/Downloads/Memory-Tricks-Proposal.md on 2026-10-11: "they
aren't super important" - so the changes are light and natural).

- The Hebrew-only hooks are replaced: hamsa / bat mitzvah / bar mitzvah (5-12-13) -> "high five, a dozen, and one more";
  "borekas triangle" (45-45-90) -> "the sandwich triangle"; the crosswalk gets "lean means long"; the merged worker gets
  one blended name; "give it to the little guy" is used for the x2 on the smaller side, and the setup tip that pointed
  the other way ("give the plain x to the little guy") becomes "let the smaller one be x"; the fraction-multiply
  "remember the name" line (a repeat of keep-change-flip) is dropped; the team table gets "Teamwork takes time".
- "The power is the flower, the root stays in the ground": the rule is first taught in the roots lesson (t9), which is
  a KEEP first lesson (recorded on camera, never changed) - so the trick goes into the first AI-redo video of topic 9
  that uses fraction powers, solve-q-r26-t09-01, plus the t9 summary and card; solve-q-294 (t11) keeps a short callback.
- The 5 NEW tricks, each where its slip happens: at most / at least (r26-t01-exam-words), opposites vs reciprocals
  (r26-t01-summary - the slip place solve-q-366 is topic 13, owned by another pass; numbers is KEEP), negative exponents
  (solve-q-289), times / divided by a fraction (fraction-multiply), same percent up and down (wp-053).
- Topic 13 is never touched here.

Spoken lines change IN PLACE (one old line -> one new line), so line counts and APPEAR / DRAW / POINT cues stay aligned;
the only exception is the dropped fraction-multiply line (a spoken line with no cue of its own). Drawn notes and board
items change their words only. AI-narrated videos with a script in ai_scripts/ (r26-t01-summary, r26-t09-summary) have
the same line changed there.

Time gate like the other helpers: a take recorded before CUTOFF keeps the video as recorded (the AI-redo takes are left
out by _ai_redo.install(), so those videos count as unrecorded). The KEEP first lessons are refused outright.

Not a patch itself (math_api only loads t*.py): each tNN.py that has an entry calls mnemonics(M, NN) LAST in its apply().
"""
import glob as _glob, os as _os, re as _re

# UTC; a take recorded before this keeps its video as recorded. Set to the time this change was finished.
CUTOFF = '2026-10-11T05-10-00'

KEEP = frozenset({'numbers', 'fraction-basics', 'compare-fractions', 'expression-basics', 'expression-strategy',
                  'linear-equations', 'equation-strategy', 'exponents', 'roots', 'powers-techniques', 'inequalities'})


def recorded(vid):
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


# VIDEOS[topic] = [(video id, slide title, [(kind, old, new), ...])]
#   kind 'say'  : spoken line, exact old text -> new text (new None = drop the line)
#   kind 'draw' : teacher's draw note, exact old text -> new text
VIDEOS = {
    1: [
        ('r26-t01-exam-words', 'Distinct · at least', [
            ('say', 'At least three: three or more. Three itself is allowed.',
             'At least three: three or more. Three is the floor. You can stand on it, so three is allowed.'),
            ('say', 'At most three: three or less. Again, three is allowed.',
             "At most three: three or less. Three is the ceiling. You can touch it, you just can't go through it."),
        ]),
        ('r26-t01-summary', 'Opposites · reciprocals', [
            ('say', 'Opposites add up to zero. Reciprocals multiply to one.',
             'Opposites attract, so they cancel out to zero. Reciprocals flip upside down, and together they make one.'),
        ]),
    ],
    2: [
        ('fraction-multiply', 'Use the reciprocal', [
            ('say', 'Remember the name: multiply by the reciprocal. First you change to multiply — THEN you flip. '
                    'So the flip lands on the second one.', None),
        ]),
        ('fraction-multiply', 'What division means', [
            ('say', "That's not weird — you're counting how many little pieces fit.",
             "That's not weird. Times a half, you take half. Divided by a half, you ask how many halves fit. "
             "In three pizzas? Six halves."),
        ]),
    ],
    9: [
        ('solve-q-r26-t09-01', 'Method 1 · Power over index', [
            ('say', 'The power inside, six, goes on top. The root index, four, goes on the bottom.',
             'Think of a plant. The power is the flower, so the six goes up on top. '
             'And the root stays in the ground, so the four goes on the bottom.'),
        ]),
        ('r26-t09-summary', 'Roots as powers', [
            ('say', 'A root is a fractional power. The power inside goes on top. The root index goes on the bottom.',
             'A root is a fractional power. The power is the flower, up on top. The root stays in the ground, '
             'on the bottom.'),
        ]),
    ],
    11: [
        ('solve-q-289', 'Method 2 · Switch floors', [
            ('say', "Here's the shortcut. A negative exponent just switches floors.",
             "Here's the shortcut. A minus in the power is a ticket to the other floor. The letter moves, "
             "and the minus stays behind."),
        ]),
        ('solve-q-294', 'Match the roots, then merge', [
            ('say', 'Little memory trick: the power is up in the sky, the root is down in the ground.',
             'Remember, the power is the flower, up on top. The root stays in the ground, at the bottom.'),
        ]),
    ],
    22: [
        ('solve-wp22-g047', 'Method 1 · Algebra', [
            ('say', 'Give the plain x to the little guy: B is x, A is four x. No fractions, no dividing later.',
             'Let the smaller one be x: B is x, A is four x. No fractions, no dividing later.'),
        ]),
        ('solve-q-r26-t22-20', 'Method 2 · Algebra', [
            ('say', 'Or build it with a before-and-after table. Give the plain x to the little guy: B.',
             "Or build it with a before-and-after table. Let the smaller one be x, that's B."),
        ]),
    ],
    23: [
        ('wp-053', 'Up and down', [
            ('say', "Down first, then up? Zero point eight times one point two. The same. The order doesn't matter.",
             'Down first, then up? Zero point eight times one point two. The same. '
             'Same percent up and down, in any order, and you never get back home.'),
        ]),
        ('wp-053', 'Who is the 100?', [
            ('say', 'Here\'s the rule: the whole always comes right after "of" — or after "than".',
             'Here\'s my trick: "of" and "than" point at the whole. Whatever comes right after them gets the hundred.'),
        ]),
    ],
    26: [
        ('wp-097', 'The table', [
            ('say', 'Easy to remember: work ALWAYS sits in the middle — Team, Work, Time.',
             'How do I remember the order? Teamwork takes time. Team, work, time, so the work always sits in the middle.'),
        ]),
        ('solve-wp26-g101', 'Method 1 · Algebra', [
            ('say', 'Rule: the times two goes on the SMALLER side. Then both sides are equal.',
             'But think of four and eight. To make them equal, I double the four. '
             'So give it to the little guy: the times two goes on the SMALLER side.'),
        ]),
        ('solve-wp26-g104', 'Method 1 · Algebra', [
            ('draw', 'Bracket "Omar and Priya" and write "one worker"',
             'Bracket "Omar and Priya" and write "Omarpriya = one worker"'),
            ('say', "So merge them into one worker — call it Omar-Priya. Now it's a normal two-worker question.",
             "So merge them into one worker, with one name: Omarpriya. Now it's a normal two-worker question."),
            ('draw', 'Write "Omar-Priya: 1 job in 18 h → Sam: 1 job in 18 h"',
             'Write "Omarpriya: 1 job in 18 h → Sam: 1 job in 18 h"'),
            ('say', 'Omar-Priya does one of them. So Sam does the other — one job in eighteen hours.',
             'Omarpriya does one of them. So Sam does the other — one job in eighteen hours.'),
        ]),
        ('solve-wp26-g104', 'Method 2 · Insight', [
            ('say', 'All three work for nine hours. Omar-Priya needs eighteen for a whole job — so in nine hours they do half.',
             'All three work for nine hours. Omarpriya needs eighteen for a whole job — so in nine hours they do half.'),
        ]),
    ],
    31: [
        ('geo-024', 'How to remember', [
            ('say', '5, 12, 13? A hamsa, a bat mitzvah, a bar mitzvah.',
             '5, 12, 13? High five, a dozen, and one more.'),
            ('draw', 'Under 5, 12, 13 write: hamsa · bat mitzvah · bar mitzvah',
             'Under 5, 12, 13 write: high five · a dozen · one more'),
            ('say', 'Five fingers of the hamsa, a bat mitzvah at 12, a bar mitzvah at 13.',
             "Give me a high five, that's 5. A dozen, like a box of eggs, that's 12. And one more, 13."),
            ('say', 'Know 3, 4, 5 and hamsa, bat mitzvah, bar mitzvah by heart.',
             'Know 3, 4, 5 and high five, a dozen, and one more by heart.'),
        ]),
        ('geo-027-after', 'The 45°-45°-90° Triangle', [
            ('say', "Some call it the borekas triangle — soon you'll see why.",
             "I also call it the sandwich triangle — soon you'll see why."),
        ]),
        ('geo-027-after', 'Right and isosceles', [
            ('say', 'It looks just like a cheese borekas. That often helps students remember it.',
             'You know when you cut a square sandwich corner to corner? Each half is exactly this triangle.'),
            ('say', 'Think of a square cut along its diagonal: each half is this triangle.',
             'And the sandwich shows the sides too. The two edges of the sandwich are the equal legs, '
             'and the cut is the hypotenuse.'),
        ]),
    ],
    38: [
        ('solve-geo38-g181', 'Match the drawing to the givens', [
            ('say', 'Think of a crosswalk between line c and line d. Straight across is the shortest. '
                    'The more diagonal you cross — the longer the walk.',
             'Think of a crosswalk between line c and line d. Straight across is the shortest. '
             'The more you lean, the longer the walk. Lean means long.'),
        ]),
    ],
}

# CARDS[topic] = [(card id, path into the card, old text, new text)]
CARDS = {
    1: [('mem-r26-t01-exam-words', ('tables', 0, 'rows', 9, 1),
         '$\\ge$ / $\\le$ (the number itself is allowed)',
         '$\\ge$ / $\\le$ (the number itself is allowed: $3$ is the floor / the ceiling, you can touch it)')],
    2: [('mem-r26-t02-multiply', ('tips', 1),
         'Dividing a positive number by a fraction between 0 and 1 makes it bigger: $\\frac{3}{4}\\div\\frac{1}{8}=6$.',
         'Dividing a positive number by a fraction between 0 and 1 makes it bigger: times a half takes half, divided by '
         'a half asks how many halves fit. $\\frac{3}{4}\\div\\frac{1}{8}=6$.')],
    9: [('roots', ('tables', 0, 'rows', 4, 1),
         'power on top, root index on the bottom: \\(\\sqrt[4]{3^8}=3^2\\)',
         'the power is the flower (on top), the root stays in the ground (on the bottom): \\(\\sqrt[4]{3^8}=3^2\\)')],
    22: [('mem-general-advanced', ('tips', 2),
          'One thing is twice another? The $\\times2$ goes on the smaller side: $B=x$, $A=2x$.',
          'One thing is twice another? Give it to the little guy: the $\\times2$ goes on the smaller side. '
          '$A$ is twice $B$: $A=2B$.')],
    23: [('mem-percent', ('tips', 0),
          'The whole comes right after "of" / "than" — use the one in the question.',
          '"Of" and "than" point at the whole: what comes right after them gets the $100$. Use the one in the question.'),
         ('mem-percent', ('tips', 3),
          'Up $p\\%$ and down $p\\%$ (any order): a loss of $\\frac{p^2}{100}\\%$. $+20\\%$, $-20\\%$ → $-4\\%$.',
          'Up $p\\%$ and down $p\\%$ (any order): a loss of $\\frac{p^2}{100}\\%$ - you never get back home. '
          '$+20\\%$, $-20\\%$ → $-4\\%$.')],
    26: [('mem-work-rate', ('tables', 2, 'rows', 4, 1),
          'table Team · Work · Time → ratios or the V method',
          'table Team · Work · Time ("teamwork takes time") → ratios or the V method')],
    31: [('mem-triples', ('tips', 2),
          '5, 12, 13: a hamsa, a bat mitzvah, a bar mitzvah.',
          '5, 12, 13: high five, a dozen, and one more.')],
}

# EXPL[topic] = [(question id, old paragraph text, new paragraph text)] - written solutions that name the trick
EXPL = {
    26: [('wp26-g101',
          'The large team is twice as fast, so the 2 goes on the smaller side: $5L=2\\cdot10S=20S$, therefore $L=4S$.',
          'The large team is twice as fast, so the 2 goes on the smaller side (give it to the little guy): '
          '$5L=2\\cdot10S=20S$, therefore $L=4S$.')],
}

WARN = []
CHANGED = {}


def _warn(x):
    WARN.append(x); print('WARNING mnemonics:', x)


def _slide(v, title):
    ns = [b for b in v['beats'] if b['title'] == title or b.get('bigTitle') == title]
    return ns[0] if len(ns) == 1 else None


def mnemonics(M, topic):
    assert topic != 13, 'topic 13 belongs to another pass'
    for vid, title, edits in VIDEOS.get(topic, []):
        assert vid not in KEEP, ('KEEP first lesson - never changed', vid)
        v = M.D['videos'].get(vid)
        if not v: _warn('%s: no such video' % vid); continue
        assert v.get('topic') != 13, vid
        if recorded(vid): continue
        b = _slide(v, title)
        if b is None: _warn('%s: no single slide %r' % (vid, title)); continue
        n = 0
        for kind, old, new in edits:
            ks = [k for k, l in enumerate(b['lines']) if l.get(kind) == old]
            if len(ks) != 1: _warn('%s / %s: %d %s line(s) %r' % (vid, title, len(ks), kind, old[:60])); continue
            if new is None: b['lines'].pop(ks[0])
            else: b['lines'][ks[0]][kind] = new
            n += 1
        if n: CHANGED[vid] = CHANGED.get(vid, 0) + n; M.touched_videos.add(vid)
    for cid, path, old, new in CARDS.get(topic, []):
        c = M.D['references'].get(cid)
        if c is None: _warn('card %s missing' % cid); continue
        o = c
        try:
            for p in path[:-1]: o = o[p]
            cur = o[path[-1]]
        except (KeyError, IndexError, TypeError):
            _warn('card %s: no %r' % (cid, path)); continue
        if cur != old: _warn('card %s %r: text changed %r' % (cid, path, str(cur)[:60])); continue
        o[path[-1]] = new
    for qid, old, new in EXPL.get(topic, []):
        q = M.D['questions'].get(qid)
        ex = list((q or {}).get('explanation') or [])
        if old not in ex: _warn('%s: no written-solution paragraph %r' % (qid, old[:60])); continue
        ex[ex.index(old)] = new
        M.set_q(qid, expl=ex)
