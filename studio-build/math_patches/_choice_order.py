"""Choice order like the real exam (teacher 2026-10-09: "if the answer can be 1 it will be in choice number 1, same with
2 3 4, and also same with 1/2 1/4 1/3, so it makes it a bit simpler to find for the student. Take a look at the actual
exam and then restructure ours").

THE CONVENTION (checked on all 760 parsed real NITE quantitative questions, 19 English sections 2019-2026,
real_exam/quant_real.md):
  * A choice whose value is the whole number 1, 2, 3 or 4 is ALWAYS choice (1), (2), (3), (4) - 381 of 381 such
    choices, no exception (e.g. 2020_autumn_q2_12: 5, 2, 3, 4 · 2021_autumn_q1_11: 1, 2, 0, 4 · 2025_winter_q2_19:
    10%, 2%, 3%, 6%). Units and % do not matter: "2%" sits in place 2.
  * A unit fraction 1/2, 1/3, 1/4 sits in place 2, 3, 4 - 32 of 34 when that place is free (the whole number wins the
    place: 2020_spring_q2_12 has 1/2, 2, √2, 2√2). E.g. 2023_winter_q2_20: 1/5, 1/2, 1/3, 1/6 · 2025_winter_q2_01:
    1, 1/2, 1/8, 1/4.
  * Not a rule: ascending / descending order (only 188 of 249 unpinned numeric sets, 76%), roots, π, negatives (-k in
    place k 11/15), leading digits (20/30/40 in place 2/3/4: 57%), expression choices (chance level).
  * "It cannot be determined / None of the above" is choice (4) (33 of 35) - unless the whole number 4 needs that
    place (2024_winter_q1_03: cannot, 9, 6, 4).
  Zero is not pinned (1, 2, 3, 0 · 1, 2, 0, 4).

WHAT CHANGES: every multiple-choice question of the math topics (1-38) whose choices break the pin rule and that is not
in a recorded video: the choices are reordered (pinned values to their place; "cannot be determined" to (4), else (1);
the rest keep their old relative order in the free places), the correct answer moves with its choice, and everything
that names a choice POSITION follows: spoken lines ("Choice three.", "The trap is choice two"), DRAW cues ("Circle
choice 3", "Cross out choices 1 and 4", "Next to choices 1, 2 and 3 write: 0, 1, 2"), value lists read in choice order
("Here the answers aren't in order: 5, 4, 2, 3"), and the written solutions ("The answer is choice 2", "choices (1)
and (4) are out"). Numbers, stories and choice texts are never changed - only the order. Lines are swapped IN PLACE
(no line added or removed), so line counts and APPEAR / DRAW cues stay aligned; no affected video has an AI script.

Only questions not shown in a recorded video: a question whose video has a take recorded before CUTOFF keeps its old
order (time-gated like _spoken_labels.py - never a live "skip if recorded" check). Re-record list videos
(_rerecord.RERECORD) may change: solve-q-249 (option 1, full re-record) is changed; solve-q-326 (option 2, continue
from the old last slide - its question sits in the recorded part) is left out of QMAP on purpose. The three AI-pilot
videos (solve-geo33-g091, solve-q-544, solve-q-r26-t22-02) are not touched (their questions already follow the rule).
Topics 51 / 52 (modulesV51.py / modulesV52*.py, not math_patches) are not changed here - check_left lists them.

Not a patch itself (math_api only loads t*.py): each tNN.py calls choice_order(M, NN) LAST in its apply().
check_left(D) lists every multiple-choice question of an unrecorded video / practice that still breaks the rule (build
warning in build_verbal.py); recorded(D) lists the ones in recorded videos (left for the teacher to decide).
"""
import glob as _glob, math as _math, os as _os, re as _re, warnings as _warnings

# UTC; a video with a take recorded before this keeps the old choice order. Set to the time this change was finished:
# a take recorded later was made with the new order.
CUTOFF = '2026-10-09T14-18-17'

PILOT = {'solve-geo33-g091', 'solve-q-544', 'solve-q-r26-t22-02'}   # AI-pilot videos: another agent edits them


# ---------------------------------------------------------------------------------------------------------------------
# the rule
# ---------------------------------------------------------------------------------------------------------------------
_UNITS = (r'(credits?|kph|km/h|cm|m|km|meters?|metres?|meter|cc|kg|g|liters?|litres?|hours?|minutes?|seconds?|NIS|shekels?|'
          r'units?|years?|days?|degrees?|students?|people|%)')


def _strip(s):
    s = str(s).replace('\\(', '').replace('\\)', '').replace('$', '').strip()
    s = _re.sub(r'\\[dt]frac', r'\\frac', s)
    s = _re.sub(r'\\frac\s*(\d)\s*(\d)', r'\\frac{\1}{\2}', s)          # \frac12
    s = _re.sub(r'\\frac\s*(\d)\s*\{', r'\\frac{\1}{', s)                # \frac3{10}
    s = _re.sub(r'\\frac\s*(\{[^{}]*\})\s*(\d)', r'\\frac\1{\2}', s)     # \frac{3}4
    s = s.replace('\\left', '').replace('\\right', '').replace('\\,', '').replace('\\ ', ' ').replace('{,}', ',')
    s = s.replace('−', '-').replace('–', '-').replace('\\cdot', '*').replace('\\times', '*').replace('·', '*').replace('×', '*')
    return s.replace('^\\circ', '').replace('°', '').replace('\\%', '%').strip()


def value(choice):
    """the number a choice shows (units / % ignored), or None for an expression / text choice."""
    t = _strip(choice)
    if not t or '!' in t or ':' in t: return None
    t = _re.sub(r'\s+' + _UNITS + r'(\^?[23])?\s*$', '', t, flags=_re.I).rstrip('%').strip()
    if _re.search(r'[a-zA-Z]', _re.sub(r'\\(frac|sqrt|pi)', '', t)): return None
    e = _re.sub(r'(\d),(\d{3})', r'\1\2', t)
    e = _re.sub(r'(?<![\d.])(\d+)\s*\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1+(\2)/(\3))', e)   # mixed number
    for _ in range(3):
        e = _re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', e)
        e = _re.sub(r'\\sqrt\{([^{}]+)\}', r'math.sqrt(\1)', e)
        e = _re.sub(r'\\sqrt(\d)', r'math.sqrt(\1)', e)
        e = _re.sub(r'\^\{([^{}]+)\}', r'**(\1)', e)
    e = _re.sub(r'\^(\d)', r'**\1', e)
    e = e.replace('\\pi', '*math.pi').replace('π', '*math.pi').replace('{', '(').replace('}', ')')
    e = _re.sub(r'(^|[(+\-*/])\*math\.pi', r'\1math.pi', e)
    e = _re.sub(r'(\d|\))\s*(math\.)', r'\1*\2', e)
    if _re.search(r'[^0-9.+\-*/() mathsqrpi]', e): return None
    try:
        with _warnings.catch_warnings():
            _warnings.simplefilter('ignore'); v = eval(e, {'__builtins__': {}, 'math': _math})
    except Exception: return None
    return float(v) if isinstance(v, (int, float)) else None


def pins(choices):
    """[place this choice must have (1-4) or None, ...]: the whole number k -> place k; 1/k (a written fraction) ->
    place k unless the whole number k is also a choice."""
    vs = [value(c) for c in choices]
    whole = {k for v in vs for k in (1, 2, 3, 4) if v is not None and abs(v - k) < 1e-9}
    out = []
    for c, v in zip(choices, vs):
        k = next((k for k in (1, 2, 3, 4) if v is not None and abs(v - k) < 1e-9), None)
        if k is None and v is not None and '\\frac' in _strip(c):
            k = next((k for k in (2, 3, 4) if abs(v - 1 / k) < 1e-9 and k not in whole), None)
        out.append(k)
    return out


def violations(choices):
    """[(place now, place it should have), ...] - empty when the choices follow the real-exam order."""
    return [(i + 1, k) for i, k in enumerate(pins(choices)) if k and k != i + 1]


# ---------------------------------------------------------------------------------------------------------------------
# data (built 2026-10-09 from the rule above, every line read by hand)
# ---------------------------------------------------------------------------------------------------------------------
# QMAP[question id] = (topic, new order given as OLD places, old choices). new choices = [old[k - 1] for k in order];
# the correct answer moves with its choice. Applied only while the question still has exactly the old choices.
QMAP = {
    'alg-extra-unit-t1-1-7': (1, [2, 3, 1, 4], ["$3$", "$10$", "$15$", "$6$"]),
    'fast-practice-5': (1, [2, 3, 1, 4], ["$3$", "$9$", "$12$", "$6$"]),
    'q-019': (1, [1, 4, 2, 3], ["$-2$", "$14$", "$32$", "$2$"]),
    'q-024': (1, [1, 3, 2, 4], ["$-45$", "$3$", "$-3$", "$51$"]),
    'q-038': (1, [2, 3, 1, 4], ["$-1$", "$1$", "$2$", "$0$"]),
    'q-039': (1, [1, 2, 4, 3], ["$1$", "$2$", "$0$", "$3$"]),
    'q-040': (1, [3, 4, 1, 2], ["$0$", "$-1$", "$1$", "$2$"]),
    'q-r26-t01-02': (1, [2, 3, 1, 4], ["$3$", "$12$", "$18$", "$120$"]),
    'q-r26-t01-04': (1, [4, 1, 2, 3], ["$2$", "$3$", "$4$", "$6$"]),
    'q-r26-t01-11': (1, [1, 2, 4, 3], ["$-4$", "$2$", "$4$", "$14$"]),
    'q-r26-t01-13': (1, [2, 3, 4, 1], ["$4$", "$9$", "$12$", "$18$"]),
    'q-r26-t01-21': (1, [2, 1, 3, 4], ["$2$", "$6$", "$12$", "$36$"]),
    'alg-extra-unit-t2-1-6': (2, [1, 2, 4, 3], ["$6$", "$7$", "$8$", "$3$"]),
    'q-046': (2, [2, 1, 4, 3], ["$\\frac{1}{2}$", "$\\frac{1}{6}$", "$\\frac{2}{3}$", "$\\frac{1}{3}$"]),
    'q-047': (2, [1, 4, 3, 2], ["$\\frac{1}{5}$", "$\\frac{1}{4}$", "$\\frac{1}{3}$", "$\\frac{2}{5}$"]),
    'q-048': (2, [2, 3, 1, 4], ["$\\frac{1}{3}$", "$\\frac{50}{243}$", "$\\frac{2}{3}$", "$\\frac{3}{2}$"]),
    'q-049': (2, [1, 2, 4, 3], ["$\\frac{27}{50}$", "$\\frac{1}{6}$", "$6$", "$\\frac{1}{3}$"]),
    'q-055': (2, [1, 3, 4, 2], ["$\\frac{2}{3}$", "$\\frac{1}{4}$", "$\\frac{3}{4}$", "$\\frac{1}{3}$"]),
    'q-056': (2, [1, 3, 4, 2], ["$\\frac{2}{5}$", "$\\frac{1}{4}$", "$\\frac{4}{100}$", "$\\frac{1}{400}$"]),
    'q-067': (2, [1, 4, 3, 2], ["$0$", "$\\frac{1}{6}$", "$\\frac{1}{3}$", "$\\frac{1}{2}$"]),
    'q-070': (2, [2, 1, 3, 4], ["$\\frac{7}{8}$", "$1$", "$1\\,\\frac{1}{8}$", "$\\frac{3}{4}$"]),
    'q-071': (2, [1, 2, 4, 3], ["$\\frac{1}{6}$", "$\\frac{1}{9}$", "$\\frac{1}{5}$", "$\\frac{1}{3}$"]),
    'q-072': (2, [1, 4, 2, 3], ["$6$", "$3$", "$4$", "$5$"]),
    'q-077': (2, [2, 3, 4, 1], ["$\\frac{1}{4}$", "$\\frac{1}{5}$", "$\\frac{1}{6}$", "$\\frac{1}{7}$"]),
    'q-078': (2, [4, 1, 2, 3], ["$2$", "$3$", "$4$", "$5$"]),
    'q-r26-t02-11': (2, [3, 1, 2, 4], ["$\\frac{9}{10}$", "$\\frac{25}{36}$", "$1$", "$\\frac{5}{6}$"]),
    'q-081': (3, [4, 1, 3, 2], ["$\\frac{1}{2}$", "$\\frac{1}{4}$", "$\\frac{1}{3}$", "$\\frac{3}{4}$"]),
    'q-085': (3, [2, 3, 1, 4], ["$\\frac{1}{3}$", "$\\frac{13}{36}$", "$\\frac{7}{18}$", "$\\frac{11}{28}$"]),
    'q-106': (4, [3, 1, 2, 4], ["$x^5$", "$x^5-1$", "$1$", "$x^5+1$"]),
    'q-r26-t04-18': (4, [3, 2, 4, 1], ["$4$", "$5$", "$1$", "$3$"]),
    'q-expression-extra-01': (5, [2, 3, 1, 4], ["$3$", "$6$", "$9$", "$12$"]),
    'q-expression-extra-02': (5, [3, 4, 1, 2], ["$3$", "$4$", "$5$", "$-5$"]),
    'q-expression-extra-08': (5, [3, 1, 4, 2], ["$-3$", "$-1$", "$1$", "$3$"]),
    'q-expression-extra-10': (5, [1, 3, 4, 2], ["$-4$", "$4$", "$0$", "$a-4$"]),
    'q-expression-extra-11': (5, [4, 1, 2, 3], ["$\\frac{a-4b}{a-b}$", "$\\frac{a+4b}{a-b}$", "$\\frac{a-b}{a+b}$", "$1$"]),
    'q-expression-extra-15': (5, [4, 1, 2, 3], ["$x + 5$", "$x - 5$", "$x^2 - 5$", "$1$"]),
    'q-r26-t05-05': (5, [1, 2, 4, 3], ["$-28$", "$-4$", "$4$", "$28$"]),
    'q-r26-t05-06': (5, [1, 3, 4, 2], ["$\\frac{1}{2}$", "$\\frac{2}{3}$", "$2$", "$\\frac{1}{3}$"]),
    'q-r26-t05-18': (5, [2, 1, 3, 4], ["$2$", "$2b$", "$2ab$", "$b^2$"]),
    'alg-extra-unit-t6-1-7': (6, [1, 3, 4, 2], ["$5$", "$4$", "$6$", "$0$"]),
    'q-142': (6, [1, 3, 4, 2], ["$-4$", "$4$", "$8$", "$20$"]),
    'q-143': (6, [1, 3, 4, 2], ["$5$", "$4$", "$2$", "$-1$"]),
    'q-145': (6, [1, 4, 3, 2], ["$15$", "$5$", "$3$", "$2$"]),
    'q-147': (6, [3, 2, 4, 1], ["$4$", "$2$", "$6$", "$12$"]),
    'q-149': (6, [1, 4, 3, 2], ["$5$", "$4$", "$3$", "$2$"]),
    'q-150': (6, [3, 4, 1, 2], ["$3$", "$4$", "$6$", "$12$"]),
    'q-151': (6, [1, 4, 2, 3], ["$-2$", "$3$", "$4$", "$5$"]),
    'q-152': (6, [1, 3, 2, 4], ["$\\frac{1}{8}$", "$\\frac{1}{2}$", "$2$", "$8$"]),
    'q-155': (6, [2, 1, 3, 4], ["$2$", "$5$", "$10$", "$50$"]),
    'q-157': (6, [2, 1, 3, 4], ["$-9$", "$1$", "$9$", "$10$"]),
    'q-158': (6, [1, 4, 2, 3], ["$-8$", "$3$", "$4$", "$8$"]),
    'q-159': (6, [4, 3, 2, 1], ["$4$", "$3$", "$2$", "$1$"]),
    'q-160': (6, [2, 1, 3, 4], ["$2$", "$5$", "$7$", "$9$"]),
    'q-161': (6, [1, 3, 2, 4], ["$1$", "$3$", "$\\frac{9}{2}$", "$9$"]),
    'q-163': (6, [3, 1, 2, 4], ["$2$", "$3$", "$5$", "$7$"]),
    'q-166': (6, [1, 3, 2, 4], ["$\\frac{13}{3}$", "$3$", "$-3$", "$-9$"]),
    'q-167': (6, [1, 3, 2, 4], ["$-4$", "$0$", "$2$", "$4$"]),
    'q-168': (6, [2, 3, 1, 4], ["$3$", "$5$", "$7$", "$9$"]),
    'q-170': (6, [1, 3, 2, 4], ["$-\\frac{2}{3}$", "$0$", "$2$", "No value of $x$ satisfies the equation"]),
    'q-201': (7, [1, 4, 2, 3], ["$\\frac{x^2}{4} - 2$", "$\\frac{x^2}{4} - \\frac{1}{2}$", "$\\frac{x^2}{2}$", "$2$"]),
    'q-204': (7, [1, 3, 2, 4], ["$4a$", "$\\frac{1}{2}$", "$2$", "$\\frac{1}{4a}$"]),
    'q-206': (7, [1, 2, 4, 3], ["$1$", "$\\frac{2}{3}$", "$\\frac{3}{2}$", "$3$"]),
    'q-207': (7, [3, 1, 4, 2], ["$-1$", "$0$", "$1$", "$3$"]),
    'q-208': (7, [2, 1, 3, 4], ["$\\frac{1}{10}$", "$1$", "$\\frac{2}{5}$", "$0$"]),
    'q-213': (7, [2, 1, 3, 4], ["$2$", "$1$", "$3$", "$m$ cannot take any value."]),
    'q-r26-t07-08': (7, [2, 3, 4, 1], ["$0$", "$1$", "$2$", "$3$"]),
    'q-r26-t07-12': (7, [2, 1, 3, 4], ["$-1$", "$1$", "$3$", "$5$"]),
    'q-r26-t07-14': (7, [1, 3, 4, 2], ["$\\sqrt{12}$", "$4$", "$\\sqrt{14}$", "$16$"]),
    'q-r26-t07-15': (7, [2, 3, 1, 4], ["$3$", "$\\frac{1}{3}$", "$16$", "$192$"]),
    'alg-extra-exponent-extra-3': (8, [1, 3, 2, 4], ["$9$", "$3$", "$2$", "$4$"]),
    'alg-extra-exponent-extra-4': (8, [1, 3, 2, 4], ["$\\frac{1}{32}$", "$\\frac{1}{8}$", "$\\frac{1}{2}$", "$\\frac{3}{8}$"]),
    'q-218': (8, [2, 1, 3, 4], ["$0$", "$1$", "$\\sqrt{3}+1$", "$\\sqrt{3}$"]),
    'q-219': (8, [3, 2, 1, 4], ["$\\sqrt{7}+1$", "$2$", "$1$", "$\\sqrt{7}$"]),
    'q-223': (8, [4, 1, 2, 3], ["$49$", "$7^{6}$", "$7$", "$1$"]),
    'q-229': (8, [1, 3, 2, 4], ["$64$", "$3$", "$1728$", "$27$"]),
    'q-230': (8, [2, 1, 3, 4], ["$\\frac{1}{2}$", "$\\frac{1}{8}$", "$\\frac{1}{14}$", "$\\frac{1}{4}$"]),
    'q-expression-extra-09': (8, [4, 1, 3, 2], ["$5$", "$4$", "$x^{3}$", "$1$"]),
    'q-r26-t08-14': (8, [3, 1, 2, 4], ["$2$", "$3$", "$6$", "$12$"]),
    'q-r26-t08-23': (8, [1, 3, 2, 4], ["$1$", "$3$", "$9$", "$27$"]),
    'q-233': (9, [2, 3, 1, 4], ["$3$", "$-4$", "$2$", "$4$"]),
    'q-234': (9, [2, 4, 1, 3], ["$3$", "$-3$", "No real value", "$-9$"]),
    'q-236': (9, [1, 3, 2, 4], ["$64$", "$16$", "$2$", "$4$"]),
    'q-239': (9, [1, 4, 2, 3], ["$216$", "$6$", "$18$", "$2$"]),
    'q-240': (9, [1, 3, 2, 4], ["$49$", "$14$", "$2$", "$7$"]),
    'q-241': (9, [1, 2, 4, 3], ["$\\frac{1}{6}$", "$\\frac{1}{12}$", "$\\frac{1}{36}$", "$\\frac{1}{3}$"]),
    'q-242': (9, [4, 1, 2, 3], ["$5$", "$25$", "$125$", "$1$"]),
    'q-r26-t09-16': (9, [1, 3, 2, 4], ["$\\sqrt{2}$", "$12$", "$2$", "$\\sqrt{12}$"]),
    'q-r26-t09-18': (9, [4, 1, 2, 3], ["$\\sqrt{5}+1$", "$\\sqrt{5}-1$", "$4\\sqrt{5}+4$", "$1$"]),
    'q-249': (10, [1, 3, 2, 4], ["$4\\sqrt2$", "$16$", "$2$", "$4$"]),
    'q-258': (10, [1, 3, 2, 4], ["$1$", "$3$", "$6$", "$12$"]),
    'q-259': (10, [1, 4, 2, 3], ["$10$", "$-2$", "$-10$", "$2$"]),
    'q-261': (10, [2, 1, 3, 4], ["$\\sqrt2$", "$1$", "$7$", "$\\sqrt7$"]),
    'q-266': (10, [1, 2, 4, 3], ["$1$", "$\\frac{17}{3}$", "$5$", "$3$"]),
    'q-272': (10, [2, 1, 3, 4], ["$2$", "$2^{4}$", "$2^{14}$", "$2^{9}$"]),
    'q-274': (10, [2, 1, 3, 4], ["$5$", "$1$", "$3$", "$7$"]),
    'q-277': (10, [2, 1, 3, 4], ["$36$", "$1$", "$0$", "$6$"]),
    'q-280': (10, [2, 1, 3, 4], ["$x^{\\frac{29}{10}}$", "$1$", "$x^{\\frac{10}{29}}$", "$x$"]),
    'q-281': (10, [3, 1, 2, 4], ["$2$", "$\\frac13$", "$1$", "$\\frac12$"]),
    'q-286': (10, [1, 4, 2, 3], ["$25$", "$5$", "$\\sqrt2$", "$2$"]),
    'q-r26-t10-12': (10, [2, 3, 1, 4], ["$0$", "$1$", "$2$", "Every number $x$ satisfies the equation."]),
    'q-303': (11, [1, 4, 3, 2], ["$-1$", "$4$", "$\\frac{1}{4}$", "$2$"]),
    'q-305': (11, [3, 1, 2, 4], ["$\\frac{2^x}{3^x}$", "$\\frac{2}{3}$", "$1$", "$2^{x+1}\\cdot3^{x-1}$"]),
    'q-308': (11, [2, 1, 3, 4], ["$2$", "$6$", "$\\frac{3}{2}$", "$\\frac{2}{3}$"]),
    'q-311': (11, [2, 3, 4, 1], ["$4$", "$3\\cdot4^n$", "$4^n$", "$4^{-n}$"]),
    'q-316': (11, [3, 1, 4, 2], ["$\\frac{1}{2}$", "$\\frac{1}{4}$", "$1$", "$\\frac{1}{8}$"]),
    'q-318': (11, [4, 1, 2, 3], ["$2b$", "$b+1$", "$b^2$", "$1$"]),
    'q-r26-t11-06': (11, [1, 3, 4, 2], ["$\\sqrt{10}$", "$4$", "$16$", "$\\sqrt{19}$"]),
    'q-r26-t11-11': (11, [2, 1, 3, 4], ["$\\sqrt3-1$", "$1$", "$3$", "$2+\\sqrt3$"]),
    'q-344': (12, [1, 3, 2, 4], ["$7$", "$3$", "$6$", "$5$"]),
    'alg-extra-unit-t13-3-1': (13, [1, 3, 2, 4], ["$-5$", "$3$", "$8$", "$5$"]),
    'q-372': (13, [1, 3, 4, 2], ["$\\frac{1}{4}$", "$4$", "$-5$", "$0$"]),
    'q-374': (13, [3, 1, 2, 4], ["$2$", "$0$", "$1$", "It cannot be determined from the information given."]),
    'q-378': (13, [2, 3, 1, 4], ["$\\frac13$", "$0$", "$-\\frac13$", "No number $x$ satisfies the conditions."]),
    'q-380': (13, [2, 1, 3, 4], ["$2$", "$-5$", "$5$", "$-2$"]),
    'q-r26-t13-10': (13, [2, 1, 3, 4], ["$2$", "$6$", "$7$", "Infinitely many"]),
    'q-396': (14, [1, 3, 4, 2], ["$8$", "$4$", "$16$", "$12$"]),
    'q-402': (14, [1, 4, 2, 3], ["$1$", "$k$", "$0$", "$2$"]),
    'q-r26-t14-03': (14, [1, 3, 2, 4], ["$1$", "$-1$", "$2$", "$5$"]),
    'q-r26-t14-10': (14, [2, 1, 3, 4], ["$2$", "$5$", "$10$", "$30$"]),
    'alg-extra-unit-t15-3-2': (15, [3, 1, 4, 2], ["$7$", "$9$", "$1$", "$3$"]),
    'q-428': (15, [2, 3, 1, 4], ["$3$", "$1$", "$2$", "$0$"]),
    'q-441': (15, [4, 1, 2, 3], ["$0$", "$3$", "$4$", "It cannot be determined from the information given."]),
    'q-442': (15, [3, 1, 4, 2], ["$2$", "$4$", "$6$", "$3$"]),
    'q-447': (15, [3, 2, 4, 1], ["$4$", "$2$", "$0$", "$9$"]),
    'q-451': (15, [2, 1, 3, 4], ["$2$", "$15$", "$8$", "$4$"]),
    'q-452': (15, [3, 4, 1, 2], ["$0$", "$6$", "$1$", "$2$"]),
    'q-453': (15, [3, 2, 1, 4], ["$3$", "$0$", "$1$", "It cannot be determined from the information given."]),
    'q-r26-t15-01': (15, [4, 3, 1, 2], ["$3$", "$4$", "$5$", "It cannot be determined from the information given."]),
    'q-r26-t15-15': (15, [1, 2, 4, 3], ["$18$", "$15$", "$9$", "$3$"]),
    'q-458': (16, [1, 2, 4, 3], ["$1$", "$2$", "$4$", "$8$"]),
    'q-459': (16, [1, 3, 2, 4], ["$-4$", "$0$", "$2$", "$4$"]),
    'q-r26-t16-04': (16, [1, 2, 4, 3], ["$45$", "$15$", "$5$", "$3$"]),
    'alg-extra-unit-t17-3-3': (17, [1, 2, 4, 3], ["$8$", "$40$", "$13$", "$3$"]),
    'q-r26-t17-05': (17, [4, 1, 3, 2], ["$-1$", "$4$", "$-3$", "$1$"]),
    'q-r26-t17-12': (17, [3, 1, 4, 2], ["$-5$", "$-2$", "$1$", "$3$"]),
    'alg-extra-unit-t18-3-5': (18, [1, 3, 2, 4], ["$9$", "$37$", "$2$", "$5$"]),
    'alg-extra-unit-t18-3-6': (18, [1, 3, 2, 4], ["$1$", "$3$", "$6$", "$9$"]),
    'q-514': (18, [2, 4, 1, 3], ["$3$", "$11$", "$4$", "$10$"]),
    'q-515': (18, [3, 1, 2, 4], ["$0$", "$9$", "$1$", "$5$"]),
    'q-517': (18, [1, 2, 4, 3], ["$6$", "$2$", "$4$", "$5$"]),
    'q-519': (18, [1, 4, 2, 3], ["$7$", "$3$", "$5$", "$2$"]),
    'q-520': (18, [2, 3, 4, 1], ["$4$", "$7$", "$5$", "$6$"]),
    'q-522': (18, [2, 3, 1, 4], ["$3$", "$1$", "$2$", "$5$"]),
    'q-524': (18, [2, 3, 4, 1], ["$4$", "$5$", "$6$", "$9$"]),
    'q-525': (18, [1, 3, 4, 2], ["$8$", "$4$", "$10$", "$5$"]),
    'q-526': (18, [2, 4, 1, 3], ["$3$", "$5$", "$4$", "$6$"]),
    'q-527': (18, [1, 2, 4, 3], ["$6$", "$5$", "$4$", "$7$"]),
    'q-528': (18, [1, 3, 2, 4], ["$9$", "$3$", "$11$", "$7$"]),
    'q-533': (18, [4, 1, 2, 3], ["$8$", "$9$", "$5$", "$1$"]),
    'q-535': (18, [2, 3, 4, 1], ["$4$", "$9$", "$7$", "$3$"]),
    'q-537': (18, [2, 1, 3, 4], ["$2$", "$8$", "$5$", "$7$"]),
    'q-539': (18, [3, 2, 1, 4], ["$0$", "$2$", "$1$", "$5$"]),
    'q-r26-t18-01': (18, [2, 1, 3, 4], ["$0$", "$1$", "$8$", "$9$"]),
    'q-r26-t18-04': (18, [3, 1, 4, 2], ["$2$", "$4$", "$6$", "$9$"]),
    'q-r26-t18-07': (18, [1, 3, 2, 4], ["$1$", "$3$", "$9$", "It cannot be determined from the information given."]),
    'alg-extra-unit-t19-3-1': (19, [2, 1, 3, 4], ["$8$", "$1$", "$-7$", "$11$"]),
    'q-546': (19, [2, 1, 4, 3], ["$2$", "$6$", "$7$", "$3$"]),
    'q-547': (19, [2, 1, 3, 4], ["$7$", "$1$", "$0$", "$9$"]),
    'q-548': (19, [1, 2, 4, 3], ["$12$", "$20$", "$4$", "$28$"]),
    'q-550': (19, [2, 1, 3, 4], ["$2$", "$33$", "$35$", "$66$"]),
    'q-553': (19, [2, 1, 3, 4], ["$\\frac{a}{b}$", "$1$", "$\\frac{a^2}{b^2}$", "$\\frac{b^2}{a^2}$"]),
    'q-557': (19, [4, 1, 3, 2], ["$\\sqrt3$", "$9$", "$3$", "$1$"]),
    'q-558': (19, [2, 1, 3, 4], ["$2$", "$5$", "$8$", "$12$"]),
    'q-560': (19, [1, 4, 2, 3], ["$1$", "$3$", "$4$", "$16$"]),
    'q-561': (19, [1, 3, 4, 2], ["$\\frac{1}{8}$", "$\\frac{1}{4}$", "$\\frac{7}{8}$", "$\\frac{1}{7}$"]),
    'q-562': (19, [1, 2, 4, 3], ["$1$", "$2$", "$0$", "$3$"]),
    'q-563': (19, [1, 2, 4, 3], ["$\\frac{1}{16}$", "$\\frac{1}{32}$", "$\\frac{1}{4}$", "$\\frac{1}{256}$"]),
    'q-564': (19, [4, 1, 2, 3], ["$6$", "$3$", "$0$", "$1$"]),
    'q-565': (19, [2, 3, 4, 1], ["$4$", "$1$", "$0$", "$-1$"]),
    'q-570': (19, [2, 1, 3, 4], ["$2$", "$-2$", "$0$", "$-5$"]),
    'q-575': (19, [2, 1, 4, 3], ["$2$", "$1$", "Infinitely many", "$3$"]),
    'q-576': (19, [4, 1, 3, 2], ["$2$", "$0$", "$3$", "$1$"]),
    'q-r26-t19-11': (19, [2, 3, 4, 1], ["$0$", "$1$", "$2$", "$3$"]),
    'q-577': (20, [2, 1, 3, 4], ["$2$", "$-2$", "$-14$", "$14$"]),
    'q-582': (20, [2, 3, 1, 4], ["$3$", "$6$", "$8$", "$12$"]),
    'q-r26-t20-04': (20, [4, 1, 2, 3], ["$2$", "$3$", "$4$", "$10$"]),
    'q-r26-t21-01': (21, [2, 3, 4, 1], ["$4$", "$9$", "$7$", "$17$"]),
    'wp21-g009': (21, [2, 3, 1, 4], ["3", "8", "9", "18"]),
    'wp21-p07': (21, [1, 3, 2, 4], ["$5$", "$7$", "$2$", "$6$"]),
    'wp21-p25': (21, [2, 3, 4, 1], ["4", "5", "10", "6"]),
    'wp22-g042': (22, [1, 3, 2, 4], ["$\\frac{13}{3}$ credits", "3 credits", "5 credits", "6 credits"]),
    'wp22-g050': (22, [1, 4, 2, 3], ["$\\frac{10}{7}$", "$\\frac{2}{5}$", "$\\frac{5}{2}$", "$2$"]),
    'wp22-p01': (22, [1, 3, 2, 4], ["9", "3", "5", "6"]),
    'wp22-p20': (22, [2, 3, 1, 4], ["3", "24", "8", "6"]),
    'wp22-p34': (22, [2, 3, 4, 1], ["4", "6", "12", "8"]),
    'wp23-g061': (23, [4, 1, 2, 3], ["$\\frac32$", "$\\frac76$", "$\\frac23$", "$1$"]),
    'wp23-p01': (23, [2, 4, 1, 3], ["$\\frac13$", "$\\frac35$", "$\\frac14$", "$\\frac7{12}$"]),
    'wp23-p03': (23, [2, 3, 4, 1], ["$4$", "$6$", "$5$", "$7$"]),
    'wp24-g071': (24, [1, 3, 2, 4], ["$10$", "$8$", "$2$", "$5$"]),
    'wp24-p08': (24, [1, 2, 4, 3], ["$\\frac{1}{5}$", "$\\frac{8}{15}$", "$\\frac{7}{15}$", "$\\frac{1}{3}$"]),
    'wp25-g085': (25, [1, 3, 4, 2], ["11", "4", "16", "10"]),
    'wp25-p03': (25, [4, 1, 3, 2], ["$p-x$", "It cannot be determined from the information given.", "$0$", "$1$"]),
    'wp25-p05': (25, [2, 3, 1, 4], ["$\\frac{1}{3}$", "$\\frac{7}{8}$", "$\\frac{3}{8}$", "$\\frac{7}{16}$"]),
    'wp25-p18': (25, [1, 3, 4, 2], ["$12$", "$4$", "$18$", "$6$"]),
    'q-r26-t26-02': (26, [1, 2, 4, 3], ["12.5", "25", "4", "6"]),
    'q-r26-t26-03': (26, [1, 4, 2, 3], ["4.5", "3", "4", "6"]),
    'wp26-g101': (26, [1, 3, 4, 2], ["1", "4", "2", "10"]),
    'wp26-p07': (26, [1, 2, 4, 3], ["$6\\frac23$", "5", "4", "6"]),
    'wp26-p11': (26, [1, 2, 4, 3], ["12.5", "2.5", "4", "10"]),
    'wp26-p14': (26, [2, 4, 3, 1], ["$\\frac{1}{4}$", "$\\frac{1}{6}$", "$\\frac{1}{3}$", "$\\frac{1}{12}$"]),
    'q-r26-t27-02': (27, [1, 4, 2, 3], ["$8$", "$20$", "$4$", "$2$"]),
    'q-r26-t27-03': (27, [1, 3, 2, 4], ["$18$", "$3.6$", "$2$", "$4.5$"]),
    'wp27-g111': (27, [2, 3, 4, 1], ["$\\frac14$", "$\\frac49$", "$\\frac12$", "$\\frac59$"]),
    'wp27-g114': (27, [1, 2, 4, 3], ["$6$", "$10$", "$54$", "$3$"]),
    'wp27-g121': (27, [3, 1, 4, 2], ["$2$", "$4$", "$8$", "$16$"]),
    'wp27-p04': (27, [1, 2, 4, 3], ["$3\\frac13$", "$4.5$", "$4$", "$5$"]),
    'wp27-p07': (27, [4, 2, 1, 3], ["3 minutes", "12 minutes", "20 minutes", "1 hour"]),
    'wp27-p11': (27, [3, 1, 2, 4], ["20 minutes", "40 minutes", "1 hour", "It cannot be determined from the information given."]),
    'wp27-p15': (27, [2, 4, 1, 3], ["3", "5", "4", "6"]),
    'wp27-p18': (27, [2, 3, 1, 4], ["3 meters", "5 meters", "6 meters", "0.3 meter"]),
    'wp27-p22': (27, [4, 3, 2, 1], ["4", "3", "2", "3.5"]),
    'wp28-g124': (28, [1, 2, 4, 3], ["6", "24", "4", "12"]),
    'wp28-g142': (28, [1, 3, 4, 2], ["12", "4", "8", "16"]),
    'wp28-p06': (28, [3, 4, 1, 2], ["3", "4", "6", "12"]),
    'wp28-p18': (28, [3, 1, 4, 2], ["2", "4", "11", "6"]),
    'wp28-p20': (28, [1, 3, 4, 2], ["14", "4", "10", "9"]),
    'wp29-g149': (29, [2, 1, 3, 4], ["$\\frac12$", "$\\frac{11}{14}$", "$\\frac7{18}$", "$\\frac{11}{18}$"]),
    'wp29-g152': (29, [1, 4, 2, 3], ["$\\frac7{10}$", "$\\frac15$", "$\\frac1{10}$", "$\\frac12$"]),
    'wp29-g153': (29, [1, 3, 2, 4], ["$\\frac1{16}$", "$\\frac1{32}$", "$\\frac12$", "$\\frac18$"]),
    'wp29-g157': (29, [2, 1, 3, 4], ["$\\frac12$", "$\\frac5{11}$", "$\\frac6{11}$", "$\\frac14$"]),
    'wp29-g158': (29, [1, 2, 4, 3], ["$\\frac18$", "$\\frac{15}{56}$", "$\\frac14$", "$\\frac2{15}$"]),
    'wp29-g161': (29, [1, 3, 2, 4], ["$\\frac27$", "$\\frac1{14}$", "$\\frac12$", "$\\frac17$"]),
    'wp29-p07': (29, [1, 2, 4, 3], ["$\\frac4{25}$", "$\\frac17$", "$\\frac14$", "$\\frac3{25}$"]),
    'wp29-p08': (29, [2, 3, 4, 1], ["$\\frac14$", "$\\frac3{16}$", "$\\frac1{16}$", "$\\frac18$"]),
    'wp29-p10': (29, [2, 1, 3, 4], ["$\\frac12$", "$\\frac{11}{24}$", "$\\frac{13}{24}$", "$\\frac9{17}$"]),
    'wp29-p12': (29, [2, 3, 4, 1], ["$\\frac14$", "$\\frac1{24}$", "$\\frac16$", "$\\frac25$"]),
    'wp29-p13': (29, [1, 3, 4, 2], ["$\\frac{125}{1296}$", "$\\frac14$", "$\\frac1{1296}$", "$\\frac16$"]),
    'wp29-p19': (29, [1, 2, 4, 3], ["$\\frac1{64}$", "$\\frac12$", "$\\frac14$", "$\\frac5{16}$"]),
    'wp29-p23': (29, [2, 1, 3, 4], ["$\\frac{1}{2}$", "$\\frac{1}{16}$", "$\\frac{3}{8}$", "$\\frac{1}{4}$"]),
    'geo30-advanced-p01': (30, [3, 4, 1, 2], ["$3$", "$4$", "$6$", "$2$"]),
    'geo30-advanced-p03': (30, [1, 3, 4, 2], ["$\\frac52$", "$\\frac{11}{5}$", "$2$", "$3$"]),
    'geo31-advanced-p23': (31, [2, 1, 3, 4], ["$\\frac12$", "$\\frac17$", "$\\frac27$", "$\\frac25$"]),
    'geo31-g022': (31, [2, 3, 1, 4], ["$3$", "$\\sqrt{149}$", "$\\sqrt{17}$", "$\\sqrt{51}$"]),
    'geo31-g040': (31, [2, 3, 1, 4], ["$\\frac13$", "$1$", "$\\frac3{10}$", "$\\frac38$"]),
    'geo32-advanced-p16': (32, [2, 3, 4, 1], ["$4$", "$5$", "$6$", "$7$"]),
    'geo32-advanced-p18': (32, [2, 3, 1, 4], ["$3$", "$5$", "$6$", "$10$"]),
    'geo33-advanced-p03': (33, [1, 3, 4, 2], ["$8-4\\sqrt3$", "$4$", "$8-4\\sqrt2$", "$8-\\sqrt2$"]),
    'geo33-advanced-p22': (33, [2, 3, 1, 4], ["$3$", "$10$", "$30$", "$15$"]),
    'geo33-g080': (33, [1, 3, 4, 2], ["$8$", "$4$", "$16$", "$12$"]),
    'geo33-g097': (33, [3, 2, 4, 1], ["$\\frac14$", "$\\frac12$", "$\\frac2\\pi$", "$\\frac1{\\sqrt2}$"]),
    'geo33-g101': (33, [1, 3, 4, 2], ["$5$", "$4$", "$2$", "$3$"]),
    'q-r26-t33-07': (33, [1, 3, 4, 2], ["$13$", "$4$", "$5$", "$9$"]),
    'q-r26-t33-09': (33, [1, 2, 4, 3], ["$5$", "$6$", "$7$", "$3$"]),
    'geo34-core-p04': (34, [1, 2, 4, 3], ["$\\frac56$", "$\\frac12$", "$\\frac23$", "$\\frac13$"]),
    'geo35-core-p12': (35, [2, 3, 1, 4], ["$3$", "$\\frac72$", "$6$", "$7$"]),
    'q-r26-t35-05': (35, [1, 4, 3, 2], ["$1$", "$4$", "$16$", "$2$"]),
    'geo36-core-p10': (36, [3, 1, 4, 2], ["$\\frac12$", "$\\frac14$", "$\\frac34$", "$\\frac13$"]),
    'q-r26-t36-05': (36, [2, 1, 3, 4], ["$2$", "$0.08$", "$0.8$", "$8$"]),
    'q-r26-t36-17': (36, [1, 2, 4, 3], ["$6$", "$2$", "$54$", "$3$"]),
    'geo37-core-p09': (37, [1, 4, 2, 3], ["$15$", "$8$", "$17$", "$2$"]),
    'geo37-core-p11': (37, [2, 3, 1, 4], ["$3$", "$4.5$", "$9$", "$6$"]),
    'geo37-core-p20': (37, [1, 2, 4, 3], ["$6$", "$8$", "$4$", "$3$"]),
    'geo37-core-p26': (37, [2, 3, 1, 4], ["$3$", "$5$", "$\\sqrt{90}$", "$9$"]),
    'geo37-g167': (37, [1, 2, 4, 3], ["$1$", "Infinitely many", "$0$", "$3$"]),
    'geo38-core-p02': (38, [2, 3, 1, 4], ["$3$", "$4.5$", "$9$", "It cannot be determined from the information given."]),
    'geo38-core-p19': (38, [3, 2, 1, 4], ["$0$", "$2$", "$1$", "Infinitely many"]),
}

# LINES[video id] = [(old line, new line), ...] - spoken / DRAW / APPEAR-label lines that name a choice position (or read
# the choices in their order), in slide order; a repeated old line is listed once per occurrence. Read one by one.
LINES = {
    'solve-q-r26-t01-11': [
        ("Circle choice 4",
         "Circle choice 3"),
        ("Choice four. Flip only the first sign in each bracket, and you get two — choice two is waiting for you.",
         "Choice three. Flip only the first sign in each bracket, and you get two — choice two is waiting for you."),
    ],
    'solve-q-r26-t05-18': [
        ("Next to choices 1, 2 and 3 write: 0, 1, 2",
         "Next to choices 1, 2 and 3 write: 1, 0, 2"),
        ("Choice one, the number two: power zero. Out. Choice three, two a b: power two. Out.",
         "Choice two, the number two: power zero. Out. Choice three, two a b: power two. Out."),
        ("Circle choice 2",
         "Circle choice 1"),
        ("Two b — power one. Choice two.",
         "Two b — power one. Choice one."),
        ("Four a b over two a: two b. Choice two. ✓",
         "Four a b over two a: two b. Choice one. ✓"),
    ],
    'solve-q-402': [
        ("Circle choice 4",
         "Circle choice 2"),
        ("A prime has exactly two divisors: one and itself. Choice four.",
         "A prime has exactly two divisors: one and itself. Choice two."),
    ],
    'solve-q-r26-t14-03': [
        ("Circle choice 2",
         "Circle choice 3"),
        ("Choice two. Choice one is the trap — it swaps a and b.",
         "Choice three. Choice one is the trap — it swaps a and b."),
    ],
    'solve-q-428': [
        ("Circle choice 3",
         "Circle choice 2"),
        ("Choice three.",
         "Choice two."),
    ],
    'solve-q-r26-t15-01': [
        ("Circle choice 2",
         "Circle choice 4"),
        ("Choice two. Choice one is the trap: five minus two — the wrong order.",
         "Choice four. Choice three is the trap: five minus two — the wrong order."),
        ("Both examples agree with method one. Choice two.",
         "Both examples agree with method one. Choice four."),
        ("Circle choice 2",
         "Circle choice 4"),
        ("Every pair leaves four. Choice two — and choice four, cannot be determined, is out.",
         "Every pair leaves four. Choice four — and choice one, cannot be determined, is out."),
    ],
    'solve-q-r26-t15-15': [
        ("Circle choice 4",
         "Circle choice 3"),
        ("Choice four: three.",
         "Choice three: three."),
    ],
    'solve-q-458': [
        ("Write \"= 8q\", then \"8q / 2q = 4\", and circle choice 3",
         "Write \"= 8q\", then \"8q / 2q = 4\", and circle choice 4"),
        ("The q squareds cancel, the fours cancel. Eight q over two q — four. Choice three.",
         "The q squareds cancel, the fours cancel. Eight q over two q — four. Choice four."),
        ("Circle choice 3",
         "Circle choice 4"),
        ("Four — choice three.",
         "Four — choice four."),
    ],
    'solve-q-r26-t16-04': [
        ("Cross out choices 2 and 3",
         "Cross out choices 2 and 4"),
        ("Circle choice 4",
         "Circle choice 3"),
        ("Three is left. Choice four.",
         "Three is left. Choice three."),
    ],
    'solve-q-514': [
        ("Cross out choices 1 and 4",
         "Cross out choices 2 and 3"),
        ("Cross out choice 3",
         "Cross out choice 4"),
        ("Circle choice 2",
         "Circle choice 1"),
        ("Only eleven survives both. Choice two.",
         "Only eleven survives both. Choice one."),
        ("Circle choice 2",
         "Circle choice 1"),
        ("Eleven times anything is divisible by eleven. Choice two.",
         "Eleven times anything is divisible by eleven. Choice one."),
    ],
    'solve-q-515': [
        ("Circle choice 1",
         "Circle choice 2"),
        ("C is zero — choice one.",
         "C is zero — choice two."),
    ],
    'solve-q-517': [
        ("Next to 676 write \"A − C = 4\" and circle choice 3",
         "Next to 676 write \"A − C = 4\" and circle choice 4"),
        ("A is six: twenty-six squared, six seventy-six. Six minus two: four. Choice three.",
         "A is six: twenty-six squared, six seventy-six. Six minus two: four. Choice four."),
        ("Write \"26² = 676 ✓\" and circle choice 3",
         "Write \"26² = 676 ✓\" and circle choice 4"),
        ("Let's check it. Twenty-six squared is six seventy-six. Six hundred and something, ending in six. It fits. Choice three.",
         "Let's check it. Twenty-six squared is six seventy-six. Six hundred and something, ending in six. It fits. Choice four."),
    ],
    'solve-q-519': [
        ("Classic trial and error: plug in the answers. Choice three — C is five.",
         "Classic trial and error: plug in the answers. Choice four — C is five."),
        ("Circle choice 3",
         "Circle choice 4"),
        ("On the exam: mark it and move on. Choice three.",
         "On the exam: mark it and move on. Choice four."),
        ("Next to choices 2 and 4 write \"A + B ≥ 5 ✗\"",
         "Next to choices 2 and 3 write \"A + B ≥ 5 ✗\""),
        ("Cross out choices 1, 2 and 4",
         "Cross out choices 1, 2 and 3"),
        ("Only C equal five works. Choice three.",
         "Only C equal five works. Choice four."),
    ],
    'solve-q-520': [
        ("Write \"U = 3 → 6T = 36 → T = 6\" and circle choice 4",
         "Write \"U = 3 → 6T = 36 → T = 6\" and circle choice 3"),
        ("Six T is thirty-six, so T is six. The tens digit is six — choice four.",
         "Six T is thirty-six, so T is six. The tens digit is six — choice three."),
        ("Write \"63: 27 + 4 · 9 = 63 ✓\" and circle choice 4",
         "Write \"63: 27 + 4 · 9 = 63 ✓\" and circle choice 3"),
        ("Let's check sixty-three. Three cubed is twenty-seven, plus four times nine, thirty-six. Sixty-three. Choice four.",
         "Let's check sixty-three. Three cubed is twenty-seven, plus four times nine, thirty-six. Sixty-three. Choice three."),
        ("Next to choices 1, 2 and 3 write \"U³ + 3U = 24, 42, 30 ✗\"",
         "Next to choices 1, 2 and 4 write \"U³ + 3U = 42, 30, 24 ✗\""),
        ("The others work the same way: four gives twenty-four, seven gives forty-two, five gives thirty. U cubed plus three U is four, fourteen, thirty-six — never one of those.",
         "The others work the same way: seven gives forty-two, five gives thirty, four gives twenty-four. U cubed plus three U is four, fourteen, thirty-six — never one of those."),
    ],
    'solve-q-r26-t18-01': [
        ("Cross out choice 1",
         "Cross out choice 2"),
    ],
    'solve-q-546': [
        ("Circle choice 3",
         "Circle choice 4"),
        ("Choice three.",
         "Choice four."),
    ],
    'solve-q-553': [
        ("Next to the choices write their values: 1/2, 1, 1/4, 4",
         "Next to the choices write their values: 1, 1/2, 1/4, 4"),
        ("One half, one, one quarter, four. All different — one substitution is enough.",
         "One, one half, one quarter, four. All different — one substitution is enough."),
    ],
    'solve-q-577': [
        ("Next to choice 3 write \"(a, b, c) = (1, 0, −14) ✓\", next to choice 1 \"(3, 2, 0) ✓\", next to choice 2 \"(1, 0, −2) ✓\"",
         "Next to choice 3 write \"(a, b, c) = (1, 0, −14) ✓\", next to choice 2 \"(3, 2, 0) ✓\", next to choice 1 \"(1, 0, −2) ✓\""),
    ],
    'solve-q-r26-t20-04': [
        ("Circle choice 3",
         "Circle choice 4"),
        ("Four. Choice three.",
         "Four. Choice four."),
        ("The numbers five, seven and nine don't matter here. Choice four, ten, is the biggest pile plus one — a different question.",
         "The numbers five, seven and nine don't matter here. Choice one, ten, is the biggest pile plus one — a different question."),
    ],
    'solve-q-r26-t21-01': [
        ("Circle choice 3",
         "Circle choice 2"),
        ("Seven. Choice three.",
         "Seven. Choice two."),
        ("Next to choice 1 write \"a pair: 3 + 1\"",
         "Next to choice 4 write \"a pair: 3 + 1\""),
        ("Next to choice 4 write \"3 RED: 8 + 6 + 3\"",
         "Next to choice 3 write \"3 RED: 8 + 6 + 3\""),
        ("Next to choice 2 write \"3 of each\"",
         "Next to choice 1 write \"3 of each\""),
    ],
    'solve-wp21-g009': [
        ("Circle choice 2",
         "Circle choice 1"),
        ("Eight loaves. Choice two.",
         "Eight loaves. Choice one."),
    ],
    'solve-wp22-g042': [
        ("Write \"total > 4\" and cross out choice 2",
         "Write \"total > 4\" and cross out choice 3"),
        ("Three plus more than one: more than four. Choice two — three credits — is out.",
         "Three plus more than one: more than four. Choice three — three credits — is out."),
        ("Cross out choices 3 and 4, circle choice 1",
         "Cross out choices 2 and 4, circle choice 1"),
    ],
    'solve-wp22-g050': [
        ("Write \"50/20 = 5/2\" and circle choice 3",
         "Write \"50/20 = 5/2\" and circle choice 4"),
        ("Fifty over twenty — divide both by ten: five halves. Choice three.",
         "Fifty over twenty — divide both by ten: five halves. Choice four."),
        ("Write \"5/2\" and circle choice 3",
         "Write \"5/2\" and circle choice 4"),
        ("Five halves. Choice three.",
         "Five halves. Choice four."),
    ],
    'solve-wp23-g061': [
        ("Write \"100 ÷ 100 = 1\" and circle choice 4",
         "Write \"100 ÷ 100 = 1\" and circle choice 1"),
        ("Lior over Omer: a hundred over a hundred. One. Choice four.",
         "Lior over Omer: a hundred over a hundred. One. Choice one."),
        ("The trap is choice two: fifty minus thirty-three and a third, sixteen and two thirds percent more. But the third is taken from Dana's bigger wage.",
         "The trap is choice three: fifty minus thirty-three and a third, sixteen and two thirds percent more. But the third is taken from Dana's bigger wage."),
        ("Write \"2 halves → 3 halves → remove 1 of 3 → 2 halves\" and circle choice 4",
         "Write \"2 halves → 3 halves → remove 1 of 3 → 2 halves\" and circle choice 1"),
        ("Here: two halves, add one — three. Remove a third — one of the three — back to two halves. Consecutive unit fractions always cancel. Choice four.",
         "Here: two halves, add one — three. Remove a third — one of the three — back to two halves. Consecutive unit fractions always cancel. Choice one."),
        ("Circle choice 4",
         "Circle choice 1"),
        ("Choice four.",
         "Choice one."),
    ],
    'solve-wp25-g085': [
        ("Circle choice 3",
         "Circle choice 2"),
        ("Choice three. Eleven is the trap: six plus five forgets that an average lead of five is a total lead of ten.",
         "Choice two. Eleven is the trap: six plus five forgets that an average lead of five is a total lead of ten."),
        ("Seventy minus fifty-four: sixteen. Choice three — no equations.",
         "Seventy minus fifty-four: sixteen. Choice two — no equations."),
    ],
    'solve-wp25-p18': [
        ("Circle choice 3",
         "Circle choice 2"),
        ("Choice three. Four is the trap: that's the gap of the averages, not of the sums.",
         "Choice two. Four is the trap: that's the gap of the averages, not of the sums."),
        ("Twenty-eight minus ten: eighteen. Choice three again.",
         "Twenty-eight minus ten: eighteen. Choice two again."),
    ],
    'solve-q-r26-t26-02': [
        ("Cross out choice 3",
         "Cross out choice 4"),
        ("Circle choice 4",
         "Circle choice 3"),
        ("Between five and ten — only six. Choice four. No calculation at all.",
         "Between five and ten — only six. Choice three. No calculation at all."),
        ("Circle choice 4",
         "Circle choice 3"),
    ],
    'solve-q-r26-t26-03': [
        ("Circle choice 2",
         "Circle choice 3"),
        ("Three. Choice two.",
         "Three. Choice three."),
        ("Circle choice 2",
         "Circle choice 3"),
    ],
    'solve-wp26-g101': [
        ("Circle choice 2",
         "Circle choice 4"),
        ("Four. Choice two.",
         "Four. Choice four."),
        ("Circle choice 2",
         "Circle choice 4"),
    ],
    'solve-q-r26-t27-02': [
        ("Write \"2c = 8 → c = 4\" and circle choice 3",
         "Write \"2c = 8 → c = 4\" and circle choice 4"),
        ("Subtract the equations: two c equals eight. The current is four. Choice three.",
         "Subtract the equations: two c equals eight. The current is four. Choice four."),
    ],
    'solve-q-r26-t27-03': [
        ("Circle choice 3",
         "Circle choice 2"),
        ("Two minutes. Choice three.",
         "Two minutes. Choice two."),
    ],
    'solve-wp27-g111': [
        ("Write \"4/9\" and circle choice 2",
         "Write \"4/9\" and circle choice 1"),
        ("Maya covers four out of nine. Choice two.",
         "Maya covers four out of nine. Choice one."),
        ("Cross out choices 3 and 4",
         "Cross out choices 2 and 3"),
        ("Cross out choice 1 and circle choice 2",
         "Cross out choice 4 and circle choice 1"),
    ],
    'solve-wp27-g121': [
        ("Circle choice 3",
         "Circle choice 1"),
        ("Eight minutes. Choice three.",
         "Eight minutes. Choice one."),
    ],
    'solve-wp28-g124': [
        ("Circle choice 3",
         "Circle choice 4"),
        ("Four numbers. Choice three. What did we do? We counted and checked.",
         "Four numbers. Choice four. What did we do? We counted and checked."),
    ],
    'solve-wp28-g142': [
        ("Write \"2 × 2 × 2 × 1 = 8\" and circle choice 3",
         "Write \"2 × 2 × 2 × 1 = 8\" and circle choice 2"),
        ("Two times two times two times one: eight. Choice three.",
         "Two times two times two times one: eight. Choice two."),
        ("Write \"4 × 2 = 8\" and circle choice 3",
         "Write \"4 × 2 = 8\" and circle choice 2"),
    ],
    'solve-wp29-g149': [
        ("Write \"7/14 = 1/2\" and circle choice 1",
         "Write \"7/14 = 1/2\" and circle choice 2"),
        ("Seven out of fourteen. One half. Choice one.",
         "Seven out of fourteen. One half. Choice two."),
    ],
    'solve-wp29-g152': [
        ("Write \"1/2 · 1/5 = 1/10\" and circle choice 3",
         "Write \"1/2 · 1/5 = 1/10\" and circle choice 4"),
        ("One half times one fifth: one tenth. Choice three.",
         "One half times one fifth: one tenth. Choice four."),
    ],
    'solve-wp29-g153': [
        ("Write \"= 1/32\" and circle choice 2",
         "Write \"= 1/32\" and circle choice 3"),
        ("One thirty-second. Choice two.",
         "One thirty-second. Choice three."),
    ],
    'solve-wp29-g158': [
        ("Circle choice 3",
         "Circle choice 4"),
        ("Choice three.",
         "Choice four."),
    ],
    'solve-geo31-g040': [
        ("Cross out choices 1, 2 and 4",
         "Cross out choices 1, 3 and 4"),
        ("Only one answer is 3 to 10 or 10 to 3: 3 tenths. One third, 1 and 3 eighths are out.",
         "Only one answer is 3 to 10 or 10 to 3: 3 tenths. 1, one third and 3 eighths are out."),
        ("Circle choice 3",
         "Circle choice 2"),
        ("3 tenths — choice three.",
         "3 tenths — choice two."),
        ("Cross out choice 2",
         "Cross out choice 1"),
        ("Next to choice 1 write a = 1, b = 3: 9 − 1 = 8 ≠ 9, and cross it out",
         "Next to choice 3 write a = 1, b = 3: 9 − 1 = 8 ≠ 9, and cross it out"),
        ("Next to choice 3 write a = 3, b = 10: 30 − 3 = 27 = 3 · 9 ✓",
         "Next to choice 2 write a = 3, b = 10: 30 − 3 = 27 = 3 · 9 ✓"),
        ("Circle choice 3",
         "Circle choice 2"),
        ("Choice three.",
         "Choice two."),
    ],
    'solve-geo33-g101': [
        ("Circle choice 2",
         "Circle choice 4"),
        ("Choice two.",
         "Choice four."),
        ("Here the answers aren't in order: 5, 4, 2, 3. Order the values — 2, 3, 4, 5 — the middle values are 3 and 4.",
         "Here the answers aren't in order: 5, 2, 3, 4. Order the values — 2, 3, 4, 5 — the middle values are 3 and 4."),
        ("Cross out choices 3 and 4",
         "Cross out choices 2 and 3"),
        ("Circle choice 2",
         "Circle choice 4"),
        ("Choice two. Solved two ways — pick the one that suits you.",
         "Choice four. Solved two ways — pick the one that suits you."),
    ],
    'solve-geo37-g167': [
        ("Cross out choice 3",
         "Cross out choice 4"),
        ("Circle choice 4",
         "Circle choice 3"),
        ("And 3 is impossible. Choice four. To cross an axis more than once you need a parabola, or some other curve — not a straight line.",
         "And 3 is impossible. Choice three. To cross an axis more than once you need a parabola, or some other curve — not a straight line."),
    ],
}

# EXPL[question id] = [(old paragraph, new paragraph), ...] - written-solution paragraphs that name a choice position
# ("The answer is choice 2", "choices (1) and (4) are out", "The choices give 32, 31, 1 and 33").
EXPL = {
    'q-r26-t02-11': [
        ("Choice 1 ($\\frac{9}{10}$) ignores the brackets: $\\frac{1}{2}+\\frac{1}{3}\\cdot\\frac{6}{5}=\\frac{1}{2}+\\frac{2}{5}$. Choice 2 multiplies instead of dividing.",
         "Choice 2 ($\\frac{9}{10}$) ignores the brackets: $\\frac{1}{2}+\\frac{1}{3}\\cdot\\frac{6}{5}=\\frac{1}{2}+\\frac{2}{5}$. Choice 3 multiplies instead of dividing."),
    ],
    'q-081': [
        ("Choice 2.",
         "Choice 4."),
    ],
    'q-106': [
        ("Add: $x^4$, $x^3$, $x^2$ and $x$ cancel in pairs. What is left is $x^5-1$ (choice 2).",
         "Add: $x^4$, $x^3$, $x^2$ and $x$ cancel in pairs. What is left is $x^5-1$ (choice 3)."),
        ("Faster: plug in $x=2$. $(2-1)(16+8+4+2+1)=31$. The choices give $32$, $31$, $1$ and $33$. Only choice 2 gives $31$.",
         "Faster: plug in $x=2$. $(2-1)(16+8+4+2+1)=31$. The choices give $1$, $32$, $31$ and $33$. Only choice 3 gives $31$."),
    ],
    'q-expression-extra-01': [
        ("Main bar: $9\\div\\frac{3}{2}=9\\cdot\\frac{2}{3}=6$. The answer is choice 2.",
         "Main bar: $9\\div\\frac{3}{2}=9\\cdot\\frac{2}{3}=6$. The answer is choice 1."),
    ],
    'q-expression-extra-02': [
        ("Therefore the expression is $4-(-1)=4+1=5$. The answer is choice 3.",
         "Therefore the expression is $4-(-1)=4+1=5$. The answer is choice 1."),
    ],
    'q-expression-extra-08': [
        ("The bottom is $y-x=-(x-y)$. Therefore $\\frac{3(x-y)}{-(x-y)}=-3$. The answer is choice 1.",
         "The bottom is $y-x=-(x-y)$. Therefore $\\frac{3(x-y)}{-(x-y)}=-3$. The answer is choice 2."),
    ],
    'q-expression-extra-11': [
        ("Then $1-\\frac{3b}{a-b}=\\frac{a-b-3b}{a-b}=\\frac{a-4b}{a-b}$. The answer is choice 1.",
         "Then $1-\\frac{3b}{a-b}=\\frac{a-b-3b}{a-b}=\\frac{a-4b}{a-b}$. The answer is choice 2."),
        ("Check with $a=2$, $b=1$: $1-\\frac{3+6}{3}=-2$, and choice 1 gives $\\frac{-2}{1}=-2$ (the others give $6$, $\\frac{1}{3}$ and $1$).",
         "Check with $a=2$, $b=1$: $1-\\frac{3+6}{3}=-2$, and choice 2 gives $\\frac{-2}{1}=-2$ (the others give $1$, $6$ and $\\frac{1}{3}$)."),
    ],
    'q-expression-extra-15': [
        ("The top is $(x-5)^2$. Cancel one factor $x-5$ (not zero): $x-5$. The answer is choice 2.",
         "The top is $(x-5)^2$. Cancel one factor $x-5$ (not zero): $x-5$. The answer is choice 3."),
        ("Check with $x=6$: $\\frac{36-60+25}{1}=1$, and choice 2 gives $6-5=1$ ✓.",
         "Check with $x=6$: $\\frac{36-60+25}{1}=1$, and choice 3 gives $6-5=1$ ✓."),
    ],
    'q-r26-t05-18': [
        ("Choice 1 ($2$) has power $0$, choice 2 ($2b$) has power $1$, choice 3 ($2ab$) has power $2$. Only choice 2 is left.",
         "Choice 1 ($2b$) has power $1$, choice 2 ($2$) has power $0$, choice 3 ($2ab$) has power $2$. Only choice 1 is left."),
        ("Algebra: $(a+b)^2-(a-b)^2=(a^2+2ab+b^2)-(a^2-2ab+b^2)=4ab$, and $\\frac{4ab}{2a}=2b$. The answer is choice 2.",
         "Algebra: $(a+b)^2-(a-b)^2=(a^2+2ab+b^2)-(a^2-2ab+b^2)=4ab$, and $\\frac{4ab}{2a}=2b$. The answer is choice 1."),
    ],
    'q-142': [
        ("$5x=20$, so $x=4$. The answer is choice 2.",
         "$5x=20$, so $x=4$. The answer is choice 4."),
    ],
    'q-143': [
        ("$14x-8=6x+24 \\to 8x=32 \\to x=4$. The answer is choice 2.",
         "$14x-8=6x+24 \\to 8x=32 \\to x=4$. The answer is choice 4."),
    ],
    'q-145': [
        ("Put it into the first equation: $2+3y=17 \\to 3y=15 \\to y=5$. The answer is choice 2.",
         "Put it into the first equation: $2+3y=17 \\to 3y=15 \\to y=5$. The answer is choice 4."),
    ],
    'q-147': [
        ("$3y=12$, so $y=4$. The answer is choice 1.",
         "$3y=12$, so $y=4$. The answer is choice 4."),
    ],
    'q-149': [
        ("So $x=2$. The answer is choice 4.",
         "So $x=2$. The answer is choice 2."),
    ],
    'q-150': [
        ("So $x=3$. The answer is choice 1.",
         "So $x=3$. The answer is choice 3."),
    ],
    'q-151': [
        ("Add: $13x=65$, so $x=5$. The answer is choice 4.",
         "Add: $13x=65$, so $x=5$. The answer is choice 2."),
    ],
    'q-158': [
        ("So $x=8$. It is allowed ($8 \\ne -2$). The answer is choice 4.",
         "So $x=8$. It is allowed ($8 \\ne -2$). The answer is choice 2."),
    ],
    'q-159': [
        ("$-10+3y=-1 \\to 3y=9 \\to y=3$. The answer is choice 2.",
         "$-10+3y=-1 \\to 3y=9 \\to y=3$. The answer is choice 3."),
    ],
    'q-161': [
        ("Put $x$ in place of $y$ in the second equation: $2x+x=9 \\to 3x=9 \\to x=3$. The answer is choice 2.",
         "Put $x$ in place of $y$ in the second equation: $2x+x=9 \\to 3x=9 \\to x=3$. The answer is choice 3."),
    ],
    'q-163': [
        ("Add $x+y=7$: $2x=10$, so $x=5$. The answer is choice 3.",
         "Add $x+y=7$: $2x=10$, so $x=5$. The answer is choice 1."),
    ],
    'q-166': [
        ("Divide by $3$: $x=-3$. The answer is choice 3.",
         "Divide by $3$: $x=-3$. The answer is choice 2."),
    ],
    'q-201': [
        ("With $x=2$ the choices give $-1$, $\\frac12$, $2$ and $2$. Only choice 1. The right choice gives $y$ for every allowed $x$, so it must give $-1$ at $x=2$.",
         "With $x=2$ the choices give $-1$, $2$, $\\frac12$ and $2$. Only choice 1. The right choice gives $y$ for every allowed $x$, so it must give $-1$ at $x=2$."),
    ],
    'q-204': [
        ("Therefore $8x = 4$ and $x = \\frac{1}{2}$ (choice 2).",
         "Therefore $8x = 4$ and $x = \\frac{1}{2}$ (choice 3)."),
    ],
    'q-206': [
        ("Therefore $\\frac{x}{y} = \\frac{3}{2}$ (choice 3).",
         "Therefore $\\frac{x}{y} = \\frac{3}{2}$ (choice 4)."),
    ],
    'q-207': [
        ("Therefore $a - b = 1 - (-2) = 3$ (choice 4).",
         "Therefore $a - b = 1 - (-2) = 3$ (choice 3)."),
    ],
    'q-213': [
        ("For example, $n = k = 5$ fits both equations with $m = 0$. Therefore $m$ takes exactly one value: $0$ (choice 2).",
         "For example, $n = k = 5$ fits both equations with $m = 0$. Therefore $m$ takes exactly one value: $0$ (choice 1)."),
    ],
    'q-223': [
        ("$7^{-5}\\cdot7^{9}\\cdot7^{-2}=7^2=49$. The answer is choice 1.",
         "$7^{-5}\\cdot7^{9}\\cdot7^{-2}=7^2=49$. The answer is choice 2."),
        ("The trap is choice 2: losing the minus of $-2$ gives $-5+9+2=6$.",
         "The trap is choice 3: losing the minus of $-2$ gives $-5+9+2=6$."),
    ],
    'q-230': [
        ("$\\frac{7^3}{14^3}=\\left(\\frac{7}{14}\\right)^3=\\left(\\frac{1}{2}\\right)^3=\\frac{1}{8}$. The answer is choice 2.",
         "$\\frac{7^3}{14^3}=\\left(\\frac{7}{14}\\right)^3=\\left(\\frac{1}{2}\\right)^3=\\frac{1}{8}$. The answer is choice 1."),
    ],
    'q-expression-extra-09': [
        ("Then $x^3\\cdot\\frac{5}{x^3}=5$. The answer is choice 1.",
         "Then $x^3\\cdot\\frac{5}{x^3}=5$. The answer is choice 2."),
    ],
    'q-305': [
        ("Check with $x=1$: $\\frac{6}{2^0\\cdot3^2}=\\frac69=\\frac23$. Choices (1) and (2) both give $\\frac23$, so try $x=2$: $\\frac{36}{2\\cdot27}=\\frac{36}{54}=\\frac23$, while $\\frac{2^2}{3^2}=\\frac49$. Choice (2).",
         "Check with $x=1$: $\\frac{6}{2^0\\cdot3^2}=\\frac69=\\frac23$. Choices (2) and (3) both give $\\frac23$, so try $x=2$: $\\frac{36}{2\\cdot27}=\\frac{36}{54}=\\frac23$, while $\\frac{2^2}{3^2}=\\frac49$. Choice (3)."),
    ],
    'q-311': [
        ("Check with $n=1$: $16-4=12$, and $3\\cdot4^1=12$ ✓. The other choices give $4$, $4$ and $\\frac14$.",
         "Check with $n=1$: $16-4=12$, and $3\\cdot4^1=12$ ✓. The other choices give $4$, $\\frac14$ and $4$."),
    ],
    'q-374': [
        ("Method 2 · Plugging in numbers: take $n=1$. $|m+1|=|m-1|$ gives $m=0$, so $m\\cdot n=0$: choices 1 and 3 are out. Take $n=2$: again $m=0$ and $m\\cdot n=0$. The value does not change, so choice 4 is out too. The answer is choice 2.",
         "Method 2 · Plugging in numbers: take $n=1$. $|m+1|=|m-1|$ gives $m=0$, so $m\\cdot n=0$: choices 1 and 2 are out. Take $n=2$: again $m=0$ and $m\\cdot n=0$. The value does not change, so choice 4 is out too. The answer is choice 3."),
    ],
    'q-r26-t13-10': [
        ("The integers from $1$ to $7$: $7$ values. Choice 1 counts only the two ends.",
         "The integers from $1$ to $7$: $7$ values. Choice 2 counts only the two ends."),
    ],
    'q-r26-t15-01': [
        ("Method 2 · Tag it: $a=7k+2$ and $b=7m+5$ (different letters, because $a$ and $b$ are different numbers). $a-b=7k-7m-3=7(k-m-1)+4$. Whatever $k$ and $m$ are, the remainder is $4$, so choice 4 (\"cannot be determined\") is out too.",
         "Method 2 · Tag it: $a=7k+2$ and $b=7m+5$ (different letters, because $a$ and $b$ are different numbers). $a-b=7k-7m-3=7(k-m-1)+4$. Whatever $k$ and $m$ are, the remainder is $4$, so choice 1 (\"cannot be determined\") is out too."),
    ],
    'q-r26-t16-04': [
        ("The smallest case is only a candidate. Test a second case with no multiple of 5: $n=7$ gives $7\\cdot9\\cdot11=693$. It ends in 3, so it is not divisible by 5, and not by 15. (2) and (3) are out.",
         "The smallest case is only a candidate. Test a second case with no multiple of 5: $n=7$ gives $7\\cdot9\\cdot11=693$. It ends in 3, so it is not divisible by 5, and not by 15. (2) and (4) are out."),
    ],
    'q-514': [
        ("Plug in two different numbers. $71+17=88$: it is not divisible by 3 or by 10, so choices (1) and (4) are out.",
         "Plug in two different numbers. $71+17=88$: it is not divisible by 3 or by 10, so choices (2) and (3) are out."),
        ("$72+27=99$: it is not divisible by 4, so choice (3) is out. Only 11 is left.",
         "$72+27=99$: it is not divisible by 4, so choice (4) is out. Only 11 is left."),
    ],
    'q-r26-t21-01': [
        ("$6$ is not enough ($2$ red, $2$ blue, $2$ green), and $7$ always works. Choice 3.",
         "$6$ is not enough ($2$ red, $2$ blue, $2$ green), and $7$ always works. Choice 2."),
    ],
    'wp21-g009': [
        ("Tuesday: $78\\div2=39$, then $39-1=38$. Wednesday: $38\\div2=19$, then $19-1=18$. Thursday: $18\\div2=9$, then $9-1=8$. Choice 2.",
         "Tuesday: $78\\div2=39$, then $39-1=38$. Wednesday: $38\\div2=19$, then $19-1=18$. Thursday: $18\\div2=9$, then $9-1=8$. Choice 1."),
    ],
    'wp21-p07': [
        ("$n=5$ and $n=2$ also work, for example $1+2+3+4+11$ and $1+20$. Choice 2.",
         "$n=5$ and $n=2$ also work, for example $1+2+3+4+11$ and $1+20$. Choice 3."),
    ],
    'wp21-p25': [
        ("At least $16-10=6$ boxes stay at exactly $3$. Choice 4.",
         "At least $16-10=6$ boxes stay at exactly $3$. Choice 3."),
    ],
    'geo38-core-p02': [
        ("Area $=\\frac{3\\cdot3}{2}=4.5$ cm². Choice 2.",
         "Area $=\\frac{3\\cdot3}{2}=4.5$ cm². Choice 1."),
    ],
    'geo38-core-p19': [
        ("So there is exactly one rhombus: choice 3.",
         "So there is exactly one rhombus: choice 1."),
    ],
}


# ---------------------------------------------------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------------------------------------------------
WARN = []          # entries that found nothing (text changed elsewhere / question changed)
CHANGED = {}       # question id -> number of video lines + solution paragraphs changed with it
SKIPPED = {}       # question id -> its recorded video (kept in the old order)
_TAKES = None


def _takes():
    global _TAKES
    if _TAKES is None:
        pat = _re.compile(r'^(.+)-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$'); _TAKES = {}
        for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
            m = pat.match(_os.path.basename(f))
            if m: _TAKES.setdefault(m.group(1), []).append(m.group(2))
    return _TAKES


def recorded_before_cutoff(vid):
    return any(ts < CUTOFF for ts in _takes().get(vid, []))


def _rerecord():
    import importlib.util
    p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_rerecord.py')
    s = importlib.util.spec_from_file_location('_rerecord', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m.RERECORD


def shown_in(D, qid):
    """videos that show the question: its solution video(s) and any slide with the question on the board."""
    out = set()
    for vid, v in D['videos'].items():
        if v.get('questionId') == qid: out.add(vid); continue
        for b in v.get('beats', []):
            if any(it.get('k') == 'q' and it.get('qid') == qid for it in b.get('items', [])): out.add(vid); break
    return out


def choice_order(M, topic):
    rr = None
    for qid, (t, order, old) in QMAP.items():
        if t != topic: continue
        if qid not in M.D['questions']: WARN.append('%s: no such question' % qid); continue
        q = M.q(qid)
        if list(q.get('choicesRich') or []) != old: WARN.append('%s: choices changed elsewhere - not reordered' % qid); continue
        vids = shown_in(M.D, qid)
        if vids & PILOT: WARN.append('%s: shown in an AI-pilot video - not reordered' % qid); continue
        rec = [v for v in sorted(vids) if recorded_before_cutoff(v)]
        if rec:
            rr = _rerecord() if rr is None else rr
            if any(v not in rr for v in rec): SKIPPED[qid] = rec[0]; continue
        new = [old[k - 1] for k in order]
        if violations(new): WARN.append('%s: new order still breaks the rule' % qid); continue
        n = 0
        ex = list(q.get('explanation') or [])
        for a, b in EXPL.get(qid, []):
            if a in ex: ex[ex.index(a)] = b; n += 1
            else: WARN.append('%s: no solution paragraph %r' % (qid, a[:60]))
        for vid in sorted(vids):
            lines = [l for b in M.video(vid)['beats'] for l in b['lines']]
            for a, b in LINES.get(vid, []):
                hit = next((l for l in lines if any(l.get(k) == a for k in ('say', 'draw', 'label'))), None)
                if hit is None: WARN.append('%s: no line %r' % (vid, a[:60])); continue
                for k in ('say', 'draw', 'label'):
                    if hit.get(k) == a: hit[k] = b
                lines.remove(hit); n += 1
            M.touched_videos.add(vid)
        M.set_q(qid, choices=new, correct=order.index(q['correct'][0] + 1) + 1, expl=ex)
        CHANGED[qid] = n


# ---------------------------------------------------------------------------------------------------------------------
# build-time check
# ---------------------------------------------------------------------------------------------------------------------
def _quant_questions(D):
    """(topic, question id, videos showing it) for every placed multiple-choice question of topics 1-38, 51, 52."""
    shown = {}
    for vid, v in D['videos'].items():
        if v.get('questionId'): shown.setdefault(v['questionId'], set()).add(vid)
        for b in v.get('beats', []):
            for it in b.get('items', []):
                if it.get('k') == 'q' and it.get('qid'): shown.setdefault(it['qid'], set()).add(vid)
    placed = {f['ref'] for f in D['flow'] if f['type'] == 'question'}
    for qid, q in D['questions'].items():
        t = q.get('topic'); t = int(t) if str(t).isdigit() else None
        if not t or not (t <= 38 or t in (51, 52)) or (qid not in placed and qid not in shown): continue
        if len(q.get('choicesRich') or q.get('choices') or []) != 4: continue
        yield t, qid, shown.get(qid, set())


def _bad(D):
    import sys
    sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    import studio_done
    rec = {v for v, ts in studio_done.takes()}
    for t, qid, vids in _quant_questions(D):
        q = D['questions'][qid]; ch = q.get('choicesRich') or q.get('choices')
        bad = violations(ch)
        if bad: yield t, qid, sorted(vids), sorted(vids & rec), ch, bad


def check_left(D):
    """multiple-choice questions (topics 1-38, 51, 52) NOT in a recorded video whose choices break the real-exam order
    -> list of strings (build warning)."""
    return ['t%02d %s%s | %s | %s' % (t, qid, ' (' + ', '.join(v) + ')' if v else ' (practice)', ' · '.join(_strip(c) for c in ch),
                                     ', '.join('%s in place %d, belongs in %d' % (_strip(ch[i - 1]), i, k) for i, k in bad))
            for t, qid, v, r, ch, bad in _bad(D) if not r]


def recorded(D):
    """the same for questions in RECORDED videos (left as recorded - for the teacher to decide)."""
    return ['t%02d %s (%s) | %s' % (t, qid, ', '.join(r), ' · '.join(_strip(c) for c in ch)) for t, qid, v, r, ch, bad in _bad(D) if r]
