"""Spoken labels -> natural speech (teacher 2026-10-09: "take off words like 'notice:' that seem like I'm reading and turn
it into speech like 'but when you see something like that it's important to notice...'").

Spoken (teacher-read) lines of the MATH videos (topics 1-38) that opened with a reading-style label - "Careful:",
"Notice:", "Step one:", "Check:", "Remember:", "Tip:", "Shortcut:", "Bottom line:", "Watch out", "Warning", "Important",
"Reminder", and the "The trap:" / "The rule:" headings - are rewritten BY HAND, one by one, in her spoken style
(real_exam/TEACHER_VOICE_GUIDE.md). Same meaning, no new content. The words change IN PLACE: no line is split, merged,
added or removed, so line counts and APPEAR / DRAW / POINT cues stay aligned. Labels on the slide text (board items,
titles) stay; only the `say` lines change.

Only videos not recorded yet: a video with a take recorded before CUTOFF keeps its old lines (time-gated, like
_trim_repeats.py / _clearer.py / _method_names.py - never a live "skip if recorded" check, which reverted videos that
were recorded later with the new text). Re-record list videos (_rerecord.RERECORD) may change; the only one with a
label line (solve-q-328, option 2 = continue from the old last slide) is left out of MAP on purpose: its line sits in
the recorded part. The three AI-pilot videos (solve-geo33-g091, solve-q-544, solve-q-r26-t22-02) are not touched.
2026-10-11 AI redo (_ai_redo.py): recorded math videos redone with the AI voice count as unrecorded (their old takes
are ignored); their 47 label lines are in MAP_AI_REDO (incl. solve-q-328, now a whole new video).

Not a patch itself (math_api only loads t*.py): each tNN.py calls spoken_labels(M, NN) LAST in its apply().
check_left(D) lists every spoken line of an unrecorded math video that still starts with a core label (build warning).
"""
import glob as _glob, os as _os, re as _re

# UTC; a take of a video recorded before this keeps the old lines. Set to the time this change was finished: a take
# recorded later was made with the new spoken lines, so they must stay.
CUTOFF = '2026-10-09T13-23-17'


def _rerecord():
    import importlib.util
    p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_rerecord.py')
    s = importlib.util.spec_from_file_location('_rerecord', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m.RERECORD


def recorded(vid):
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


# MAP[video id] = (topic, [(old spoken line, new spoken line), ...]); a repeated old line is listed once per occurrence
# (replaced in slide order).
MAP = {
    'fast-calculation': (1, [
        ("Careful: don't add two to BOTH. That inflates the sum by four. For addition, you shift in opposite directions.",
         "But careful here, don't add two to BOTH. That inflates the sum by four. For addition, you shift in opposite directions."),
        ("Careful — it's a squaring pattern only. Not a rule for any two numbers ending in five.",
         "Now, be careful with this. It's a squaring pattern only. Not a rule for any two numbers ending in five."),
    ]),
    'r26-t05-power-count': (5, [
        ('The rule: count the power of the question. A choice with a different power is out. A mixed choice is out too.',
         "So here's the rule. Count the power of the question. A choice with a different power is out, and a mixed choice is out too."),
        ('Check: the top is x minus y, times x plus y. Cancel x plus y: x minus y, plus y. x. ✓',
         "Let's check it. The top is x minus y, times x plus y. Cancel x plus y: x minus y, plus y. x. ✓"),
        ('Choice one. Check: x squared plus two x y plus y squared is exactly x plus y, squared. ✓',
         'Choice one. And to check, x squared plus two x y plus y squared is exactly x plus y, squared. ✓'),
    ]),
    'solve-q-298': (11, [
        ('Check: root m times root m is m. Root n times minus root n is minus n. The middle terms cancel.',
         "Let's check it. Root m times root m is m. Root n times minus root n is minus n. The middle terms cancel."),
    ]),
    'r26-t13-mirror': (13, [
        ('Step one: is the given a mirror? Flip all signs.',
         'So first we ask, is the given a mirror? Flip all signs.'),
        ("Careful: in the swap it turns into y squared at most thirteen. That's a twin — not the opposite. Twins stay. Only opposites go out.",
         "Now careful, because in the swap it turns into y squared at most thirteen. That's a twin — not the opposite. Twins stay. Only opposites go out."),
        ("The rule: if the given doesn't change in the mirror, a choice that turns into its opposite is not necessarily true.",
         "So the rule is, if the given doesn't change in the mirror, a choice that turns into its opposite is not necessarily true."),
    ]),
    'solve-q-401': (14, [
        ('Choice two. The trap: seeing "prime" and deciding m is prime too. It\'s m SQUARED that\'s prime — m is its square root.',
         'Choice two. The trap here is seeing "prime" and deciding m is prime too. It\'s m SQUARED that\'s prime — m is its square root.'),
    ]),
    'solve-q-394': (14, [
        ('The rule: a power of a prime divides z only if z has that prime at least as many times.',
         'And this is the rule to remember. A power of a prime divides z only if z has that prime at least as many times.'),
    ]),
    'r26-t14-more-tools': (14, [
        ('The rule: in a perfect square every exponent is even.',
         "And here's the rule to remember. In a perfect square, every exponent is even."),
    ]),
    'r26-t14-summary': (14, [
        ("The trap: just multiplying the two numbers. That's too big when they share a prime.",
         "The trap is just multiplying the two numbers. That's too big when they share a prime."),
    ]),
    'divisibility': (15, [
        ("The rule: five divides fifteen, so it works. Six doesn't divide eight — so it doesn't.",
         "So it all depends on the divisor. Five divides fifteen, so it works. Six doesn't divide eight — so it doesn't."),
    ]),
    'solve-q-423': (15, [
        ('The rule: a fraction of a fraction — multiply the denominators. Half of a quarter? It must be divisible by eight, not just by four.',
         'Remember, a fraction of a fraction means we multiply the denominators. Half of a quarter? It must be divisible by eight, not just by four.'),
    ]),
    'solve-q-426': (15, [
        ('Shortcut: the five x part already divides — so everything built from it divides too. Just check two squared.',
         "Here's a little shortcut. The five x part already divides — so everything built from it divides too. Just check two squared."),
    ]),
    'solve-q-433': (15, [
        ('Check: fourteen times three forty-six plus six is four thousand eight hundred fifty. Ends in zero.',
         "Let's check. Fourteen times three forty-six plus six is four thousand eight hundred fifty. It ends in zero."),
    ]),
    'r26-t15-remainder-tools': (15, [
        ('The rule: tag each condition, do the operation, read the number in front.',
         "So it's always the same. Tag each condition, do the operation, read the number in front."),
    ]),
    'whole-numbers': (16, [
        ('Careful: a positive product does NOT mean both are positive. They could both be negative.',
         'Careful here, because a positive product does NOT mean both are positive. They could both be negative.'),
    ]),
    'solve-q-463': (16, [
        ("Step one: spot the contracted multiplication formula. Nine n squared is three n, squared. And the one isn't written as a square — that trips people up.",
         "First, we spot the contracted multiplication formula. Nine n squared is three n, squared. And the one isn't written as a square — that trips people up."),
        ('Step two: n is odd, so three n is odd too. So three n minus one and three n plus one are the even numbers just before and after it — consecutive evens.',
         'Next, n is odd, so three n is odd too. So three n minus one and three n plus one are the even numbers just before and after it — consecutive evens.'),
    ]),
    'solve-q-469': (16, [
        ("Careful: lots of students spot three, four, five, add all three and pick twelve. Read the question — only x plus z. And there's a second solution hiding — zero.",
         "Now, be careful here, because lots of students spot three, four, five, add all three and pick twelve. Read the question — only x plus z. And there's a second solution hiding — zero."),
    ]),
    'solve-q-r26-t16-03': (16, [
        ('The rule: an odd count of consecutive integers — the sum divides by the count. An even count — never.',
         'So the rule is this. With an odd count of consecutive integers, the sum divides by the count. With an even count, never.'),
    ]),
    'powers-on-number-line': (17, [
        ('Step one: look for exceptions. A negative number to an even power becomes positive — it changes sides.',
         'So the first step is to look for exceptions. A negative number to an even power becomes positive — it changes sides.'),
        ('Step two: the root gets in the way. Turn it into a power, so you can compare exponents.',
         'In the second step, we deal with the root, because it gets in the way. Turn it into a power, so you can compare exponents.'),
        ('Step three: draw the line and its arrows, and read the answer straight off.',
         'And in the last step, we draw the line and its arrows, and read the answer straight off.'),
    ]),
    'solve-q-494': (17, [
        ('Step one: exceptions. Is there a negative number with an even power?',
         'So first, the exceptions. Is there a negative number with an even power?'),
        ('Step two: roots to powers. The fifth root of m is m to the one fifth.',
         'Then we turn roots into powers. The fifth root of m is m to the one fifth.'),
        ('Step three: the line. Negative fractions — the arrow points right.',
         'And finally, the line. Negative fractions — the arrow points right.'),
    ]),
    'solve-q-500': (17, [
        ("One warning: change only t. Don't change the numbers in the question to make it easier — that can change the order of the choices.",
         "Now, one thing to be careful about. Change only t. Don't change the numbers in the question to make it easier — that can change the order of the choices."),
    ]),
    'solve-q-r26-t17-01': (17, [
        ('Four letters on the line. Step one: the range of each letter.',
         "Four letters on the line. So first, let's find the range of each letter."),
    ]),
    'solve-q-r26-t17-02': (17, [
        ('Check: x is one quarter, the root is one half — to the right of x, still below one.',
         "Let's check with a number. x is one quarter, the root is one half — to the right of x, still below one."),
    ]),
    'solve-q-512': (18, [
        ('Step one: write it vertically.',
         "First, let's write it vertically."),
        ('Step two: the ones. A plus A ends in A.',
         'Now the ones digit. A plus A ends in A.'),
        ('Step three: the leftmost digit. Two two-digit numbers — and the result has three digits.',
         'Next, the leftmost digit. Two two-digit numbers — and the result has three digits.'),
        ('Step four — plug in to check. B is three, D is eight, A is zero.',
         'And the last step is to plug in and check. B is three, D is eight, A is zero.'),
    ]),
    'solve-q-513': (18, [
        ('Step one: vertically.',
         "First, let's write it vertically."),
        ('Step two: the ones. B times B ends in B.',
         "Now let's look at the ones. B times B ends in B."),
    ]),
    'solve-q-515': (18, [
        ('Step one: vertical.',
         'As always, we start by writing it vertically.'),
    ]),
    'solve-q-516': (18, [
        ('Step one: vertical.',
         'First, we write it vertically.'),
    ]),
    'solve-q-517': (18, [
        ('Check: twenty-six squared, six seventy-six. Six hundred and something, ending in six. It fits. Choice three.',
         "Let's check it. Twenty-six squared is six seventy-six. Six hundred and something, ending in six. It fits. Choice three."),
    ]),
    'solve-q-518': (18, [
        ('Step two: the ones digit. Seven times A ends in A.',
         'Now the ones digit. Seven times A ends in A.'),
    ]),
    'solve-q-520': (18, [
        ('Check: sixty-three. Three cubed is twenty-seven, plus four times nine, thirty-six. Sixty-three. Choice four.',
         "Let's check sixty-three. Three cubed is twenty-seven, plus four times nine, thirty-six. Sixty-three. Choice four."),
    ]),
    'solve-q-r26-t18-01': (18, [
        ('Step one: vertical.',
         "First, let's put it vertically."),
        ('Step two: the ones. Six plus eight is fourteen. Write four — it matches. Carry one.',
         'Now the ones. Six plus eight is fourteen. Write four — it matches. Carry one.'),
        ('The trap: "ends in A, so B is zero". But there\'s a carry! A plus zero plus one ends in A plus one — not A.',
         'Now, a lot of students think "ends in A, so B is zero". But there\'s a carry! A plus zero plus one ends in A plus one — not A.'),
    ]),
    'solve-q-r26-t18-02': (18, [
        ('Check: A minus C must be five. Take six, two, one.',
         "Let's check. A minus C must be five. Take six, two, one."),
    ]),
    'new-operation': (19, [
        ('The rule: whatever goes in, goes in brackets. Every time.',
         'So remember this one. Whatever goes in, goes in brackets. Every time.'),
        ("One warning: don't test with two equal numbers. Four star four equals four star four — for every operation. It proves nothing.",
         "Now, one thing to watch out for. Don't test with two equal numbers. Four star four equals four star four — for every operation. It proves nothing."),
    ]),
    'solve-q-550': (19, [
        ('The rule: each number to the power of the product of the other two.',
         'So the rule is, each number goes to the power of the product of the other two.'),
    ]),
    'solve-q-553': (19, [
        ("Tip: don't open the squared brackets yet — they might cancel. And they do.",
         "Here's a little tip. Don't open the squared brackets yet, because they might cancel. And they do."),
    ]),
    'solve-q-579': (20, [
        ('Step one: simplify the equation.',
         "First, let's simplify the equation."),
    ]),
    'solve-wp22-g032': (22, [
        ('Step one: what does it cost to make one sandwich?',
         'So first, what does it cost to make one sandwich?'),
        ('Step two: what did they ask? Selling price minus ingredient cost.',
         'Now, what did they ask? Selling price minus ingredient cost.'),
        ("Careful — thirty-five is in the choices too. That's the cost, not what they asked.",
         "And be careful, because thirty-five is in the choices too. That's the cost, not what they asked."),
    ]),
    'solve-wp22-g036': (22, [
        ("Notice: even if you'd mixed up which is three and which is ten — the difference is still seven x and the sum is still thirteen x. Same answer.",
         "And here's something nice. Even if you'd mixed up which is three and which is ten, the difference is still seven x and the sum is still thirteen x. Same answer."),
    ]),
    'solve-wp22-g039': (22, [
        ('Notice: the gap is still nine. Everyone ages the same — the gap stays, only the ratio changes.',
         'And look, the gap is still nine. Everyone ages the same — the gap stays, only the ratio changes.'),
        ('Careful: nine is Tom five years ago — not now.',
         'But careful, nine is Tom five years ago — not now.'),
    ]),
    'solve-q-r26-t22-01': (22, [
        ("The trap: two to three to five. Then five units are thirty tenors, and the choir is sixty. Choice two — wrong, because the altos don't match.",
         "The trap here is two to three to five. Then five units are thirty tenors, and the choir is sixty. Choice two — wrong, because the altos don't match."),
    ]),
    'r26-t22-exam-tools': (22, [
        ('The rule: one equation, two unknowns — you can find only a multiple of that equation.',
         'So remember, with one equation and two unknowns, you can find only a multiple of that equation.'),
    ]),
    'r26-t22-summary': (22, [
        ('Tip: let x be the thing they ask for.',
         "Here's a little tip. Let x be the thing they ask for."),
    ]),
    'wp-052': (23, [
        ("Notice — we never found the whole. That's the advantage: you calculate straight what they ask for.",
         "And see what happened here? We never found the whole. That's the advantage: you calculate straight what they ask for."),
    ]),
    'wp-053': (23, [
        ('Shortcut: think about what STAYS. Lose thirty percent — keep seventy. Lose twenty percent of that — keep eighty percent of seventy: fifty-six. Straight there.',
         "Here's a shortcut. Think about what STAYS. Lose thirty percent — keep seventy. Lose twenty percent of that — keep eighty percent of seventy: fifty-six. Straight there."),
        ('The rule: up p percent and down p percent always loses p squared over a hundred percent. Twenty squared is four hundred. Over a hundred: four.',
         "And there's a rule for this. Up p percent and down p percent always loses p squared over a hundred percent. Twenty squared is four hundred. Over a hundred: four."),
        ('The rule: along the arrow, multiply. Against it, divide. The answer is the product along your path.',
         'So the rule is simple. Along the arrow, multiply. Against it, divide. The answer is the product along your path.'),
    ]),
    'solve-q-r26-t23-03': (23, [
        ('The rule: p percent more than a number is a hundred plus p percent of it.',
         'So the rule is, p percent more than a number is a hundred plus p percent of it.'),
    ]),
    'solve-q-r26-t23-16': (23, [
        ('The rule: the same part — flip the percents. The same whole — keep them.',
         "So here's how to remember it. The same part, flip the percents. The same whole, keep them."),
    ]),
    'wp-067': (24, [
        ('Careful: "music students" means the WHOLE music circle — music only plus both. Not just music only.',
         'Careful here, because "music students" means the WHOLE music circle — music only plus both. Not just music only.'),
    ]),
    'wp-069': (24, [
        ('Check: five, nine, four, seven — twenty-five.',
         "Let's check. Five, nine, four, seven — twenty-five."),
    ]),
    'solve-wp24-g074': (24, [
        ('A free reminder: the maximum overlap is the smaller group — a hundred sixty-two. Not needed here, but it costs nothing.',
         'And just as a reminder, the maximum overlap is the smaller group — a hundred sixty-two. Not needed here, but it costs nothing.'),
    ]),
    'solve-q-r26-t24-01': (24, [
        ('The trap: "at least" makes you think of the minimum overlap. Fifty-nine minus fifty — nine.',
         'Here\'s the trap. "At least" makes you think of the minimum overlap. Fifty-nine minus fifty — nine.'),
    ]),
    'r26-t24-summary': (24, [
        ('Careful: "music students" means the WHOLE circle — music only plus both.',
         'And careful, "music students" means the WHOLE circle — music only plus both.'),
    ]),
    'wp-086': (25, [
        ('And watch out: on the exam it\'ll just say "average" — you have to notice it\'s weighted.',
         'And on the exam it\'ll just say "average", so it\'s up to you to notice it\'s weighted.'),
    ]),
    'solve-wp25-g089': (25, [
        ('The rule: percent shares are weights. Cheap value, plus the expensive share times the gap.',
         'So remember, percent shares are weights. Cheap value, plus the expensive share times the gap.'),
    ]),
    'solve-wp25-g090': (25, [
        ('Careful: not two thousand over four. Five hundred is the trap.',
         "And careful, it's not two thousand over four. Five hundred is the trap."),
    ]),
    'solve-q-r26-t25-04': (25, [
        ("The trap: thirty-four. That's what you get if you forget that the numbers are even — two apart, not one.",
         'If you got thirty-four, you fell into the trap. You forgot that the numbers are even — two apart, not one.'),
    ]),
    'solve-wp26-g093': (26, [
        ("Careful: the two changes multiply — three times five. Don't add them to eight.",
         "Careful here, because the two changes multiply — three times five. Don't add them to eight."),
        ("Careful: the two changes multiply — three times five. Don't add them to eight.",
         "And again, be careful. The two changes multiply — three times five. Don't add them to eight."),
    ]),
    'solve-q-r26-t26-01': (26, [
        ('The rule: when the work is fixed, faster means less time — inverse.',
         "And the rule is, when the work is fixed, faster means less time. It's inverse."),
    ]),
    'r26-t26-factors': (26, [
        ('The rule: start from the old value and multiply by every factor that changed.',
         'So all you do is start from the old value and multiply by every factor that changed.'),
    ]),
    'solve-wp27-g112': (27, [
        ('Careful — this time the question does NOT stop when they meet.',
         'But watch out, because this time the question does NOT stop when they meet.'),
    ]),
    'solve-wp27-g116': (27, [
        ("Careful — that's not Sam's speed. That's how much FASTER he is than Zoe.",
         "Now careful, that's not Sam's speed. That's how much FASTER he is than Zoe."),
    ]),
    'r26-t27-graphs': (27, [
        ('One warning: a percent faster is NOT the same percent less time.',
         'And one thing to watch out for. A percent faster is NOT the same percent less time.'),
    ]),
    'solve-q-r26-t27-06': (27, [
        ("One warning: don't pick a speed of sixty here. Then choices three and four both give the target. Two choices give the target? Try other numbers on those two.",
         "Now, one warning here. Don't pick a speed of sixty, because then choices three and four both give the target. Two choices give the target? Try other numbers on those two."),
    ]),
    'wp-140-after': (28, [
        ('Remember: a factorial takes whole numbers zero and up — and zero factorial is one. Plug in legal values only.',
         'Remember that a factorial takes whole numbers zero and up — and zero factorial is one. Plug in legal values only.'),
        ('The trap: counting the even numbers. There are three even numbers — but four twos. Four hides two of them.',
         'The trap here is counting the even numbers. There are three even numbers — but four twos. Four hides two of them.'),
    ]),
    'solve-wp28-g126': (28, [
        ('Careful — here one choice depends on another.',
         'But here we have to be careful, because one choice depends on another.'),
    ]),
    'solve-wp28-g135': (28, [
        ('Careful: the rule works one way. Espresso needs a croissant — but a croissant still goes with any other drink.',
         'Now, careful, because the rule works only one way. Espresso needs a croissant — but a croissant still goes with any other drink.'),
    ]),
    'solve-wp28-g141': (28, [
        ('Tip: above each position write how many options it has; below, list what they are. Keeps you organized.',
         "Here's a little trick to stay organized. Above each position, write how many options it has, and below, list what they are."),
    ]),
    'solve-wp28-g142': (28, [
        ("Notice: it's a square, not a row. Doesn't matter. Count the options at each stage and multiply.",
         "Now, it's a square this time, not a row. But that doesn't matter. Count the options at each stage and multiply."),
    ]),
    'solve-wp28-g143': (28, [
        ('Careful: the last added number is eleven, but it comes from the TWELFTH player. Twelve players. Choice three.',
         'Be careful here. The last added number is eleven, but it comes from the TWELFTH player. So twelve players. Choice three.'),
    ]),
    'solve-wp29-g150': (29, [
        ('Careful: sixteen is the red count. They asked for blue.',
         'But careful, sixteen is the red count, and they asked for blue.'),
    ]),
    'solve-wp29-g158': (29, [
        ('The trap: "one eighth on the first try, one seventh on the second" — that\'s choice two. But you only get a second try after you miss the first.',
         'Now, the trap here is "one eighth on the first try, one seventh on the second" — that\'s choice two. But you only get a second try after you miss the first.'),
    ]),
    'solve-q-r26-t29-03': (29, [
        ('The trap: put all nine balls in one box. Five red out of nine — choice one.',
         'The trap is to put all nine balls in one box. Five red out of nine — choice one.'),
    ]),
    'geo-001': (30, [
        ('Notice: 90 is exactly a quarter of 360. A full circle is 360 — here we have a quarter, a quarter, a quarter, a quarter. 90, 90, 90, 90.',
         'And you can see that 90 is exactly a quarter of 360. A full circle is 360 — here we have a quarter, a quarter, a quarter, a quarter. 90, 90, 90, 90.'),
        ("Careful: two angles side by side that are NOT on one straight line don't have to add up to 180.",
         "But careful, two angles side by side that are NOT on one straight line don't have to add up to 180."),
    ]),
    'solve-geo30-g005': (30, [
        ('Remember: a line cutting two parallel lines makes 8 angles. 4 acute angles — all equal. 4 obtuse angles — all equal. And an acute plus an obtuse is 180.',
         "Let's remember, a line cutting two parallel lines makes 8 angles. 4 acute angles — all equal. 4 obtuse angles — all equal. And an acute plus an obtuse is 180."),
    ]),
    'r26-t30-summary-2': (30, [
        ('Shortcut: six plus eight is fourteen, so x must end in six. Only forty-six does.',
         "Here's a quick shortcut. Six plus eight is fourteen, so x must end in six. Only forty-six does."),
    ]),
    'solve-geo31-g032': (31, [
        ("Careful: beta is below 65, but it could be above or below 50. So here we can't order all three angles.",
         "Now careful. Beta is below 65, but it could be above or below 50. So here we can't order all three angles."),
    ]),
    'solve-geo31-g035': (31, [
        ("Now, how do we find the area of ABCD? Notice: it's made of the two triangles together.",
         "Now, how do we find the area of ABCD? Well, it's made of the two triangles together."),
    ]),
    'solve-geo31-g036': (31, [
        ("Careful: BD was a leg up there — here it's the hypotenuse, opposite the right angle at C.",
         "Careful, because BD was a leg up there — here it's the hypotenuse, opposite the right angle at C."),
    ]),
    'geo-013': (31, [
        ('Bottom line: what we have here is a symmetric triangle.',
         'So the bottom line is, what we have here is a symmetric triangle.'),
        ("Tip: find the right-angle mark first, then look across from it. That's the hypotenuse — however the triangle is turned.",
         "Here's a little trick. Find the right-angle mark first, then look across from it. That's the hypotenuse — however the triangle is turned."),
    ]),
    'geo-018-after': (31, [
        ('Careful: same area does NOT mean the triangles are congruent. Their shapes can be very different.',
         'But careful, the same area does NOT mean the triangles are congruent. Their shapes can be very different.'),
    ]),
    'geo-019': (31, [
        ('Step two: find the hypotenuse — the side opposite the right angle.',
         'Next, we find the hypotenuse — the side opposite the right angle.'),
    ]),
    'geo-024': (31, [
        ('Notice: the triples define a ratio between the sides.',
         'So what the triples really give us is a ratio between the sides.'),
        ("And it's important: the longest side is always the hypotenuse. The other two are the legs.",
         'And this is important. The longest side is always the hypotenuse, and the other two are the legs.'),
    ]),
    'geo-026': (31, [
        ("So there IS a fixed side ratio in the golden triangle, and it's important: a, a root 3, 2a.",
         "So there IS a fixed side ratio in the golden triangle, and it's an important one. a, a root 3, 2a."),
        ("Notice: the short leg is always half the hypotenuse. Say it's 11 — I know right away the hypotenuse is 22.",
         "And here's a nice thing. The short leg is always half the hypotenuse. Say it's 11 — I know right away the hypotenuse is 22."),
    ]),
    'solve-q-r26-t31-03': (31, [
        ('The rule: square the longest side. Compare it with the other two squares, added.',
         "So here's what we do. Square the longest side, and compare it with the other two squares, added."),
        ("Step one: the longest side. 10 — that's AC.",
         "First, the longest side. It's 10 — that's AC."),
    ]),
    'solve-geo32-g067': (32, [
        ('Triangle ABE is 6. Notice: the white triangle and the shaded triangle next to it are equal?',
         'Triangle ABE is 6. And do you see that the white triangle and the shaded triangle next to it are equal?'),
    ]),
    'solve-geo32-g069': (32, [
        ("Notice: this height to AD is also the trapezoid's height — the distance between the two parallel lines.",
         "Now, this height to AD is also the trapezoid's height — the distance between the two parallel lines."),
        ("The whole trapezoid: 15 plus 60 — 75. Careful: 60 alone is only the white triangle — that's a trap answer.",
         "The whole trapezoid: 15 plus 60 — 75. And careful, 60 alone is only the white triangle, so that's a trap answer."),
    ]),
    'solve-geo32-g071': (32, [
        ('180 minus 115 — 65. Notice: already choices two and four are out — the number must be 65, not 130.',
         '180 minus 115 — 65. So already choices two and four are out, because the number must be 65, not 130.'),
    ]),
    'solve-geo32-g072': (32, [
        ("Careful — nobody asked for x. It's not even in the answers. We were asked for the area.",
         "But wait, nobody asked for x. It's not even in the answers. We were asked for the area."),
    ]),
    'solve-geo32-g060': (32, [
        ('Remember: in a rhombus the diagonals bisect each other. Draw AC —',
         'Remember that in a rhombus the diagonals bisect each other. Draw AC —'),
        ("Notice: once you've found all the inner pieces, you can get the area in different ways.",
         "And once you've found all the inner pieces, you can get the area in different ways."),
    ]),
    'solve-geo32-g062': (32, [
        ('Careful — not the other way round. In a kite, AO is not equal to OC.',
         'But careful, not the other way round. In a kite, AO is not equal to OC.'),
        ("Notice: once we've found all the pieces, there are more ways to get the area.",
         "Now, once we've found all the pieces, there are more ways to get the area."),
    ]),
    'geo-043': (32, [
        ('Careful: this is only when ALL the lengths grow. Only the base grows and the height stays? Then the area grows by the same factor as the base.',
         'Careful, though, this is only when ALL the lengths grow. If only the base grows and the height stays, then the area grows by the same factor as the base.'),
    ]),
    'geo-047': (32, [
        ("Reminder: it's like a rectangle that someone squashed a little sideways.",
         "Remember, it's like a rectangle that someone squashed a little sideways."),
        ('Remember: two parallel lines and a transversal make small angles and large angles.',
         'And remember, two parallel lines and a transversal make small angles and large angles.'),
        ('Area: 8 times 3 — 24. The trap: 8 times 6. The sloping side is not the height.',
         'Area: 8 times 3 — 24. A lot of students do 8 times 6, but the sloping side is not the height.'),
    ]),
    'solve-geo32-g049': (32, [
        ('Notice: the moment a perpendicular is dropped — a right triangle forms here.',
         'And see, the moment a perpendicular is dropped, a right triangle forms here.'),
    ]),
    'geo-050': (32, [
        ('Bottom line: all the sides equal, opposite angles equal, diagonals perpendicular, bisecting the angles and each other.',
         'So the bottom line is, all the sides are equal, opposite angles equal, diagonals perpendicular, bisecting the angles and each other.'),
    ]),
    'geo-052': (32, [
        ('Bottom line: the product of the diagonals over 2. Exactly like the rhombus, and like the square.',
         "So in the end, it's the product of the diagonals over 2. Exactly like the rhombus, and like the square."),
    ]),
    'solve-geo32-g055': (32, [
        ('Watch out — a common mistake.',
         "Now watch out, because here's a common mistake."),
    ]),
    'solve-q-r26-t32-01': (32, [
        ('Remember: an angle of 30 — or 150 next to it — and the height is half the sloping side.',
         'And remember, when you see an angle of 30 — or 150 next to it — the height is half the sloping side.'),
    ]),
    'solve-q-r26-t32-02': (32, [
        ('The trap: 120 uses CD, 10, as the height. The sloping leg is not the height.',
         'If you got 120, you used CD, 10, as the height. But the sloping leg is not the height.'),
    ]),
    'geo-097-after': (33, [
        ('Careful: a length factor is not an area factor. Root 2 for sides means 2 for areas; 2 for sides means 4 for areas.',
         'Now, this is important. A length factor is not an area factor. Root 2 for sides means 2 for areas; 2 for sides means 4 for areas.'),
    ]),
    'solve-geo33-g102': (33, [
        ('Notice — angle B is an inscribed angle, resting on the bold arc. The central angle is twice as big.',
         "Now look at angle B. It's an inscribed angle, resting on the bold arc. The central angle is twice as big."),
    ]),
    'solve-geo33-g088': (33, [
        ('A reminder: in the golden triangle the sides are x, x root 3 and 2x. The short leg is half the hypotenuse.',
         'Just to remind you, in the golden triangle the sides are x, x root 3 and 2x. The short leg is half the hypotenuse.'),
    ]),
    'geo-074': (33, [
        ('Careful: if we just drew two lines and stopped somewhere inside the circle, the vertex would be inside — or outside.',
         'But careful, if we just drew two lines and stopped somewhere inside the circle, the vertex would be inside — or outside.'),
    ]),
    'geo-075': (33, [
        ('Important — if I know this angle is 75, I know the one opposite is 105.',
         'And this is important. If I know this angle is 75, I know the one opposite is 105.'),
    ]),
    'geo-079': (33, [
        ("Notice: minus 11 isn't relevant. A radius is a length — it's positive, never negative.",
         "Now, minus 11 isn't relevant here. A radius is a length — it's positive, never negative."),
    ]),
    'geo-104': (34, [
        ("Remember — that's exactly what we did in the quadrilateral: one diagonal, two triangles, 180 plus 180, 360.",
         'And this is exactly what we did in the quadrilateral, remember? One diagonal, two triangles, 180 plus 180, 360.'),
        ("Careful — it only works one way. If a polygon fits in a circle, that does NOT mean it's regular.",
         "But be careful, it only works one way. If a polygon fits in a circle, that does NOT mean it's regular."),
    ]),
    'solve-geo34-g108': (34, [
        ("Notice — there's a pattern here that's ALWAYS true in a regular octagon.",
         "And there's a pattern here that's ALWAYS true in a regular octagon."),
        ("Notice — this split is ALWAYS useful, even when they don't ask for the whole octagon.",
         "Now, this split is ALWAYS useful, even when they don't ask for the whole octagon."),
    ]),
    'solve-geo34-g111': (34, [
        ('Remember: the larger angle faces the longer side.',
         'And remember, the larger angle faces the longer side.'),
    ]),
    'solve-geo35-g125': (35, [
        ('Notice — this is a minimum–maximum question in geometry.',
         'So what we have here is a minimum–maximum question in geometry.'),
    ]),
    'solve-geo35-g129': (35, [
        ('Careful: not just any edge and any diagonal. They must meet at one corner, and the edge must stand on that face. Otherwise the angle can be 45, or something else.',
         'But careful, not just any edge and any diagonal. They must meet at one corner, and the edge must stand on that face. Otherwise the angle can be 45, or something else.'),
    ]),
    'solve-geo35-g121': (35, [
        ("Careful — that one's close. Pi is MORE than 3, not equal to 3. So the water is a bit more than 72 — the box is just too small.",
         "Now, that one's close, so be careful. Pi is MORE than 3, not equal to 3. So the water is a bit more than 72 — the box is just too small."),
    ]),
    'solve-geo35-g122': (35, [
        ("Careful — 3h is a trap choice: it's the height for EQUAL volumes.",
         "And watch out for 3h. It's a trap choice, because it's the height for EQUAL volumes."),
    ]),
    'solve-geo35-g124': (35, [
        ('Careful — this prism lies on its side. The bases are the two triangles, front and back.',
         'Careful here, because this prism lies on its side. The bases are the two triangles, front and back.'),
        ("Careful: adding the two triangle bases gives 288 — that's the total surface area, a trap choice.",
         "And be careful, adding the two triangle bases gives 288 — that's the total surface area, a trap choice."),
    ]),
    'solve-q-r26-t35-01': (35, [
        ("The rule: the water's height is the volume divided by the base area.",
         "So the rule is, the water's height is the volume divided by the base area."),
        ('Step one: how much water? A box — multiply.',
         "First, how much water do we have? It's a box, so we multiply."),
        ("Step two: the new base. The cube's base is 12 by 12 — 144.",
         "Then the new base. The cube's base is 12 by 12 — 144."),
    ]),
    'solve-q-r26-t35-02': (35, [
        ('The trap: the slant height is not the height.',
         "And don't fall for this one. The slant height is not the height."),
    ]),
    'solve-q-r26-t35-03': (35, [
        ('Check: 8 corners. 12 edges with 3 each — 36. 54 on the faces. And the inside, 3 cubed — 27. Together 125. Everything fits.',
         "Let's check it all adds up. 8 corners. 12 edges with 3 each — 36. 54 on the faces. And the inside, 3 cubed — 27. Together 125. Everything fits."),
    ]),
    'solve-geo36-g147': (36, [
        ("Careful — in the figure the ring looks big. With 1.6 the ring would be bigger. With 1.3, it isn't. Emma is wrong.",
         "Now, be careful, because in the figure the ring looks big. With 1.6 the ring would be bigger. With 1.3, it isn't. Emma is wrong."),
    ]),
    'solve-geo36-g148': (36, [
        ('Step one: understand the given — D and F are midpoints.',
         "First, let's understand the given. D and F are midpoints."),
    ]),
    'solve-geo36-g150': (36, [
        ('Careful — compare radius with radius, not diameter with radius.',
         'And make sure you compare radius with radius, not diameter with radius.'),
    ]),
    'solve-geo36-g144': (36, [
        ('Step one: prove that the small triangle EDC is similar to the big triangle ABC.',
         'The first step is to prove that the small triangle EDC is similar to the big triangle ABC.'),
    ]),
    'solve-geo36-g145': (36, [
        ('Remember: plugging in only rules answers out. After three are out, one is left.',
         'And remember, plugging in only rules answers out. After three are out, one is left.'),
    ]),
    'solve-geo36-g146': (36, [
        ('A small warning: we may plug in angles only to see what matches what. Opposite equal angles — matching sides.',
         'Just a small warning here. We may plug in angles only to see what matches what. Opposite equal angles — matching sides.'),
    ]),
    'geo-134': (36, [
        ("Notice: the linear ratio isn't only between sides.",
         "Now, the linear ratio isn't only between sides."),
    ]),
    'geo-135': (36, [
        ('Bottom line: 16 ratio units against 49 ratio units.',
         "So in the end, it's 16 ratio units against 49 ratio units."),
    ]),
    'solve-geo36-g137': (36, [
        ('Careful — only circumferences. The six small disks together cover just a sixth of the big AREA.',
         'But careful, this is only about circumferences. The six small disks together cover just a sixth of the big AREA.'),
    ]),
    'geo-139': (36, [
        ('Notice: the ratio between two sides in the SAME triangle is also equal in both triangles.',
         "And here's something useful. The ratio between two sides in the SAME triangle is also equal in both triangles."),
        ('The rule: parts of the two sides — part to part is fine. The parallel segment itself — always against the whole side.',
         'So the rule is this. For parts of the two sides, part to part is fine. But the parallel segment itself always goes against the whole side.'),
    ]),
    'solve-geo36-g140': (36, [
        ("Careful — the second shape isn't the big triangle. It's what's left, the trapezoid below.",
         "Careful here, because the second shape isn't the big triangle. It's what's left, the trapezoid below."),
    ]),
    'geo-141': (36, [
        ('Notice: similar 3D shapes are ONLY shapes where all the matching edges have the same ratio.',
         'Now, this is important. Similar 3D shapes are ONLY shapes where all the matching edges have the same ratio.'),
    ]),
    'solve-q-r26-t36-03': (36, [
        ("The trap: 3 times 20 — 60 percent. Percents don't work like that.",
         "A lot of students do 3 times 20 and get 60 percent. But percents don't work like that."),
    ]),
    'geo-154': (37, [
        ('Notice — I wrote the 6 first and the 2 second. x first, y second. A is (6, 2).',
         'See how I wrote the 6 first and the 2 second? x first, y second. A is (6, 2).'),
    ]),
    'geo-155': (37, [
        ('A reminder: a segment is a line bounded by two points. So, it has a definite length.',
         'Just a reminder, a segment is a line bounded by two points. So it has a definite length.'),
        ('Careful: this is about a whole line. A short segment can stop before it reaches the axis.',
         'Careful here, because this is about a whole line. A short segment can stop before it reaches the axis.'),
    ]),
    'solve-geo37-g168': (37, [
        ('Notice: choices one and two start the same, three and four start the same. If a claim fails, its twin with the same start is the next one to check.',
         "And when you see choices like these, it's worth noticing that one and two start the same, and three and four start the same. If a claim fails, its twin with the same start is the next one to check."),
    ]),
    'solve-geo38-g183': (38, [
        ("Careful: sides 4 and 8 with 60 degrees between them are NOT an equilateral triangle. The sides aren't equal.",
         "Now, careful, because sides 4 and 8 with 60 degrees between them are NOT an equilateral triangle. The sides aren't equal."),
        ('Notice: the sides are identical. AB equals EF — 4. BC equals FG — 8.',
         'And look, the sides are identical. AB equals EF — 4. BC equals FG — 8.'),
    ]),
    'solve-geo38-g178': (38, [
        ('Notice: FM is free. Nothing in the givens fixes it. So always ask: what is free? Push it to the end — or to the middle.',
         'Now, FM is free here. Nothing in the givens fixes it. So always ask: what is free? Push it to the end — or to the middle.'),
    ]),
    'solve-geo38-g180': (38, [
        ('Notice: every answer gives alpha a minimum and a maximum.',
         'And look at the answers. Every one gives alpha a minimum and a maximum.'),
    ]),
    'solve-geo38-g181': (38, [
        ('The rule: the more acute the angle, the more slanted the segment — and the longer it is.',
         'So the rule is, the more acute the angle, the more slanted the segment — and the longer it is.'),
    ]),
    'geo-172': (38, [
        ('A slightly fatter rectangle. Notice: I added really a tiny bit of border, top and bottom —',
         'A slightly fatter rectangle. You see, I added really a tiny bit of border, top and bottom —'),
    ]),
    'geo-175': (38, [
        ("Careful: 'straight away' matters. A point that is farther, but off to the side, is a different story.",
         "Now, 'straight away' really matters here. A point that is farther, but off to the side, is a different story."),
        ('The trap: use the diameter, not the radius.',
         'The trap here is the radius, so make sure you use the diameter.'),
    ]),
    'solve-geo38-g176': (38, [
        ("Careful: '18 is the longest side' only tells you α is the biggest angle — not that it's more than 90. The anchor is what decides.",
         "But careful, '18 is the longest side' only tells you α is the biggest angle — not that it's more than 90. The anchor is what decides."),
    ]),
    'solve-q-r26-t38-02': (38, [
        ('Careful: only the area stays. Slide the apex along the line, and the sides — the perimeter — change.',
         'But careful, only the area stays. Slide the apex along the line, and the sides — the perimeter — change.'),
    ]),
}

# 2026-10-11 AI redo (_ai_redo.py): the recorded math videos that are redone with the AI voice are no longer protected,
# so their label lines get the same treatment, written by hand in the same style (47 lines in 41 videos; the 14 label
# lines in the 8 first lessons kept as recorded stay). solve-q-328 (option 2) is now a whole new video, so its line is in.
MAP_AI_REDO = {
    'add-subtract': (1, [
        ("Remember — there's no calculator on this exam.",
         "And remember, there's no calculator on this exam."),
        ('Shortcut: different signs? Take the difference — fourteen minus nine is five — and the bigger one decides the sign.',
         "Here's a little shortcut. Different signs? Take the difference — fourteen minus nine is five — and the bigger one decides the sign."),
        ('Careful — turning it into a plus does NOT guarantee a positive answer. You still calculate.',
         'But careful here, turning it into a plus does NOT guarantee a positive answer. You still calculate.'),
    ]),
    'multiply-divide': (1, [
        ('Careful — the carried digit gets ADDED, not multiplied.',
         'And careful, the carried digit gets ADDED, not multiplied.'),
    ]),
    'decimals': (2, [
        ('Bottom line: zeros at the end? Just cross them out.',
         'So the bottom line is, zeros at the end? Just cross them out.'),
    ]),
    'systems': (6, [
        ("Tip: if they ask for x, isolate y. It disappears — and you're left with exactly the letter you want.",
         "So here's a tip. If they ask for x, isolate y. It disappears — and you're left with exactly the letter you want."),
        ('Check: six times two is twelve. Six over two is three.',
         "Let's check it. Six times two is twelve. Six over two is three."),
    ]),
    'solve-q-096': (3, [
        ('Remember: with negative numbers, the closer to zero, the bigger.',
         'And remember, with negative numbers, the closer to zero, the bigger.'),
    ]),
    'solve-q-099': (3, [
        ('Careful: they want the full order — biggest, middle and smallest. Not just the biggest.',
         'Now careful, because they want the full order — biggest, middle and smallest. Not just the biggest.'),
    ]),
    'solve-q-134': (5, [
        ('Only choice four is left. Check: forty-one times eight hundred six is thirty-three thousand forty-six. Choice four.',
         "Only choice four is left. Let's check it. Forty-one times eight hundred six is thirty-three thousand forty-six. Choice four."),
    ]),
    'solve-q-171': (6, [
        ("Notice: we could have jumped straight here with cross-multiplication. When fraction equals fraction, that's allowed.",
         "And you see, we could have jumped straight here with cross-multiplication. When fraction equals fraction, that's allowed."),
        ('Careful: multiply straight across — four times x minus two — and you get negative one. That is choice one, the trap.',
         'But careful, if you multiply straight across — four times x minus two — you get negative one. That is choice one, the trap.'),
    ]),
    'solve-q-164': (6, [
        ('Careful: eleven is two x plus y, not x. Stop there, and you pick choice four.',
         'But careful, eleven is two x plus y, not x. Stop there, and you pick choice four.'),
    ]),
    'solve-q-182': (7, [
        ('Shortcut: the right side IS the square of a difference.',
         "Now here's a shortcut. The right side IS the square of a difference."),
    ]),
    'solve-q-248': (10, [
        ('Careful — this could also show up in the choices as two cubed over three squared. The negative exponent just moves it to the bottom.',
         'And be careful, because this could also show up in the choices as two cubed over three squared. The negative exponent just moves it to the bottom.'),
    ]),
    'solve-q-250': (10, [
        ('An exponential equation. Step one: make the bases equal.',
         'An exponential equation. So first, we make the bases equal.'),
    ]),
    'solve-q-252': (10, [
        ('Check: six root six on both sides. Perfect.',
         "Let's check it. Six root six on both sides. Perfect."),
    ]),
    'solve-q-291': (11, [
        ('Careful: the pattern is only for whole numbers. With fractions there are other pairs — for example nine quarters and twenty-seven eighths.',
         'But careful, the pattern is only for whole numbers. With fractions there are other pairs — for example nine quarters and twenty-seven eighths.'),
    ]),
    'solve-q-293': (11, [
        ("Careful: four copies doesn't mean plus four. Choice one is the trap.",
         "And careful, four copies doesn't mean plus four. Choice one is the trap."),
    ]),
    'solve-q-294': (11, [
        ("Shortcut: you're allowed to cancel the root's index with the power. Divide both by three — square root of five to the one.",
         "Here's a little shortcut. You're allowed to cancel the root's index with the power. Divide both by three — square root of five to the one."),
    ]),
    'solve-q-295': (11, [
        ("Notice: choices one and three are close — and we didn't need to split them. Seven did the job.",
         "And look, choices one and three are close — and we didn't need to split them. Seven did the job."),
    ]),
    'solve-q-328': (12, [
        ('The rule: x squared on the SMALL side — x is trapped between the roots.',
         'So the rule is, x squared on the SMALL side — x is trapped between the roots.'),
    ]),
    'solve-q-331': (12, [
        ('Step one: simplify the left side. x y, squared, is x squared times y squared.',
         'First, we simplify the left side. x y, squared, is x squared times y squared.'),
        ("Step two: we'd like to cancel x squared from both sides. But that's dividing by an unknown.",
         "Next, we'd like to cancel x squared from both sides. But that's dividing by an unknown."),
    ]),
    'solve-q-360': (13, [
        ('Check: three plus three is six, and six is less than seven. ✓',
         "Let's check it. Three plus three is six, and six is less than seven. ✓"),
    ]),
    'solve-q-361': (13, [
        ('Check: two plus one is three — and three is not bigger than eight.',
         "Let's check it. Two plus one is three — and three is not bigger than eight."),
    ]),
    'solve-q-364': (13, [
        ('Notice: every answer uses absolute value. Absolute value means distance from zero.',
         'And look at the answers. Every one uses absolute value. Absolute value means distance from zero.'),
    ]),
    'solve-q-368': (13, [
        ('Remember: absolute value and an even power are basically the same. True with squares — true with bars.',
         'And remember, absolute value and an even power are basically the same. True with squares — true with bars.'),
    ]),
    'solve-q-390': (14, [
        ('Check: fifty itself is divisible by ten and by twenty-five. So the number might be just fifty.',
         "Let's check it. Fifty itself is divisible by ten and by twenty-five. So the number might be just fifty."),
    ]),
    'solve-q-r26-t02-05': (2, [
        ("The trap: two fifths of the WHOLE tank is ninety-six. Two hundred forty minus ninety minus ninety-six is fifty-four. That's choice one.",
         "The trap here is taking two fifths of the WHOLE tank, ninety-six. Two hundred forty minus ninety minus ninety-six is fifty-four. That's choice one."),
    ]),
    'r26-t03-summary': (3, [
        ('Careful: with two negatives, the bottom is the SMALLER number.',
         'But careful, with two negatives, the bottom is the SMALLER number.'),
    ]),
    'r26-t04-formulas': (4, [
        ("Careful: a squared PLUS b squared doesn't break apart like this. That minus is essential.",
         "But careful, a squared PLUS b squared doesn't break apart like this. That minus is essential."),
        ('The rule: square the sum, then subtract two a b.',
         'So the rule is, square the sum, then subtract two a b.'),
    ]),
    'solve-q-r26-t04-02': (4, [
        ('The trap: choice two, four. That is fifty-one minus forty-nine, squared. A different expression.',
         'The trap here is choice two, four. That is fifty-one minus forty-nine, squared. A different expression.'),
    ]),
    'solve-q-r26-t04-04': (4, [
        ('The trap: choice two, nine. That forgets the middle term.',
         'The trap here is choice two, nine. That forgets the middle term.'),
    ]),
    'solve-q-r26-t07-02': (7, [
        ('The trap: squaring each part and forgetting the middle term. That gives thirty-six — choice one.',
         'The trap here is squaring each part and forgetting the middle term. That gives thirty-six — choice one.'),
    ]),
    'solve-q-r26-t07-05': (7, [
        ('Check: one plus one is two, squared — four. One minus three is negative two, squared — four.',
         "Let's check it. One plus one is two, squared — four. One minus three is negative two, squared — four."),
    ]),
    'r26-t08-traps': (8, [
        ('Careful: a power makes a number smaller only between zero and one. Above one, it makes it bigger.',
         'But careful, a power makes a number smaller only between zero and one. Above one, it makes it bigger.'),
    ]),
    'solve-q-r26-t09-02': (9, [
        ('The trap: five point two looks big. But its square is only twenty-seven point zero four.',
         'The trap here is that five point two looks big. But its square is only twenty-seven point zero four.'),
    ]),
    'solve-q-r26-t09-04': (9, [
        ('The rule: between zero and one, powers make it smaller, and the root makes it bigger.',
         'So the rule is, between zero and one, powers make it smaller, and the root makes it bigger.'),
    ]),
    'solve-q-r26-t09-06': (9, [
        ("The trap: root three minus root two is NOT root one. That's choice one.",
         "The trap here is thinking root three minus root two is root one. It's NOT. That's choice one."),
    ]),
    'r26-t10-power-traps': (10, [
        ('Careful: this works only when the EXPONENTS are the same. Two cubed times two to the fifth is the other law — same base, add the exponents.',
         'But careful, this works only when the EXPONENTS are the same. Two cubed times two to the fifth is the other law — same base, add the exponents.'),
    ]),
    'solve-q-r26-t10-03': (10, [
        ('Tip: if the result is too big, try a smaller choice. Too small, try a bigger one.',
         "So here's a tip. If the result is too big, try a smaller choice. Too small, try a bigger one."),
    ]),
    'solve-q-r26-t12-02': (12, [
        ('Step one: where is each factor zero?',
         'So first we ask, where is each factor zero?'),
    ]),
    'r26-t12-combining': (12, [
        ('The trap: square the ends — four and nine. Wrong.',
         'The trap here is to square the ends — four and nine. Wrong.'),
    ]),
    'solve-q-r26-t12-13': (12, [
        ('The rule: a number that works must be inside the answer. A number that fails must be outside it.',
         'So the rule is, a number that works must be inside the answer. A number that fails must be outside it.'),
    ]),
    'solve-q-r26-t14-01': (14, [
        ('Notice: all three fakes divided by seven. Never forget to try seven.',
         "And look, all three fakes divided by seven. So never forget to try seven."),
    ]),
}
assert not set(MAP_AI_REDO) & set(MAP), set(MAP_AI_REDO) & set(MAP)
MAP.update(MAP_AI_REDO)

WARN = []          # entries that found nothing (text changed elsewhere / video missing)
CHANGED = {}       # vid -> number of lines changed
SKIPPED = {}       # vid -> number of lines left because the video is recorded


def spoken_labels(M, topic):
    rr = None
    for vid, (t, pairs) in MAP.items():
        if t != topic: continue
        if vid not in M.D['videos']: WARN.append('%s: no such video' % vid); continue
        if recorded(vid):
            rr = _rerecord() if rr is None else rr
            if vid not in rr: SKIPPED[vid] = len(pairs); continue
        lines = [l for b in M.video(vid)['beats'] for l in b['lines'] if 'say' in l]
        n = 0
        for old, new in pairs:
            hit = [l for l in lines if l['say'] == old]
            if not hit: WARN.append('%s: no spoken line %r' % (vid, old[:60])); continue
            hit[0]['say'] = new; n += 1
        if n: CHANGED[vid] = n; M.touched_videos.add(vid)


_CORE = _re.compile(r'^(Careful|Notice|Step (?:one|two|three|four|five|six|\d+)|Check|Remember|Tip|Shortcut|Bottom line|'
                    r'Watch out|Warning|Important|Reminder|The trap|The rule)\s*(:|—|–)', _re.I)


def check_left(D):
    """spoken lines of unrecorded math videos (topics 1-38) that still start with a core label -> list of strings."""
    import sys
    sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    import studio_done
    rec = {v for v, ts in studio_done.takes()}
    topic = {}
    for f in D['flow']:
        if f['type'] == 'video': topic.setdefault(f['ref'], f['topic'])
    out = []
    for vid, v in D['videos'].items():
        t = topic.get(vid)
        if not t or t > 38 or vid in rec: continue
        for b in v.get('beats', []):
            for l in b.get('lines', []):
                if l.get('say') and _CORE.match(l['say']):
                    out.append('t%02d %s | %s | %s' % (t, vid, b.get('title'), l['say'][:90]))
    return out
