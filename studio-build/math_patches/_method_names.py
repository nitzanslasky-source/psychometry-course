"""One short vocabulary for method names (teacher request 2026-10-07: "the method names should come from ONE short
vocabulary, mostly based on the Psychometric Thinking lessons (topic 51) and the general names of the Hebrew course
(הברקה, הצבת מספרים, שאלות הבנה…), so students see the different ways and it doesn't look like 2 million different ones").

Every method slide of a solution video / lesson ("Method N · X", also "Way N · X" / "Approach N · X") becomes
"Method N · <vocabulary name>" ("Shortcut · X" -> "Shortcut · <name>"); the name was chosen by reading what the slide
does (spoken lines + board), not from its old title. Spoken lines that NAME the method in a short phrase are aligned
(LINES). The written solutions' "Method N · <name>" / "Shortcut · <name>" labels use the same names (QLABELS).

Only videos not recorded yet: a video with a take recorded before CUTOFF keeps its old titles (and lines).
Topic 51 (Psychometric Thinking, modulesV51.py) is where the names come from and is not changed; topic 52 has no
method titles; verbal topics are out of scope.

Not a patch itself (math_api only loads t*.py): each tNN.py calls method_names(M, NN) LAST in its apply().
"""
import glob as _glob, os as _os, re as _re

# UTC; a take of a video recorded before this keeps the old method titles. Set to the time this change was finished:
# a take recorded later was made with the new names.
CUTOFF = '2026-10-07T20-20-52'

THINKING = ['Plugging in numbers', 'Plugging in the answers', 'Estimation', 'Insight', 'Understanding', 'Algebra',
            'Calculation']   # added 2026-10-07: plain arithmetic, no letters ("Algebra" reads wrong there)
TECHNIQUES = [
    'Common factor', 'Contracted multiplication formulas', 'Prime factorization', 'Same base', 'Square both sides', 'Two cases',
    'Number line', 'Sign table', 'Ratios', 'Percent multipliers', 'The V method', 'Balance (averages)',
    'Venn diagram', 'Counting in stages', 'Angle sum in a triangle', 'Pythagoras', 'Similar triangles', 'Area formulas',
    'Power count', 'Mirror test', 'Tag it', 'Flip rule', 'Arrow map', 'Compare by factors',
    'Which door?', 'Given power → asked power',
    # added 2026-10-07 (a method needed a name the approved list did not have):
    'Listing', 'Complement', 'Remainders', 'Units digit', 'Symmetry', 'Inscribed angle', 'Parallel lines', 'The squares method',
]
VOCAB = THINKING + TECHNIQUES   # LEGACY (2026-10-07): the old-studio pass below (MAP / LINES / QLABELS) only


# =====================================================================================================================
# 2026-10-15 ONE VOCABULARY for the reading-script specs (_ai_vis_tNN.py, topics 13-20, 30-33, 51 and every new topic).
# Teacher: "What happened to naming the methods the same way, so students get a sense of the general thinking we use?"
# Derived from her Hebrew subtitles (algebra, word problems, geometry) and the topic-51 source (pt_src/seg*.txt): she
# names every solution "פתרון מתמטי" (the math way) or "פתרון פסיכומטרי באמצעות ..." (a psychometric way: plugging in
# numbers / plugging in the answers / estimation / an insight), plus "באמצעות הבנה" (by understanding). Table, Hebrew
# names, counts and when to use each: real_exam/TEACHING_STYLE_GUIDE.md "Method names (one vocabulary)".
#
# A method label (slide title "Method N · X" or, in geometry, the sidebar sb of SM(...)) is
#     Method N · <CORE>                 e.g. "Method 2 · Plugging in numbers"
#     Method N · <CORE>: <specific>     only when the specific technique helps, e.g. "Method 1 · The math way: two cases"
# The SPOKEN start of each method names the core in a natural transition (R13, no "Our first method."):
#     "Let's start with the math way." / "The math way first."   "Now let's plug in numbers."
#     "Now let's plug in the answers."   "Now by understanding."   "Now let's estimate." / "with an estimate"
#     "Now the insight." / "with an insight"
# The roadmap line uses the same words: "We'll solve it two ways, the math way, and then by plugging in numbers."
# =====================================================================================================================
CORE = {   # English label: (Hebrew, spoken forms)
    'The math way': ('פתרון מתמטי / הדרך המתמטית (אלגברית, טריוויאלית, חישובית; בניית משוואה)',
                     ('the math way', 'the math way first')),
    'Plugging in numbers': ('הצבת מספרים', ('plug in numbers', 'plug in a number', 'plugging in numbers')),
    'Plugging in the answers': ('הצבת תשובות', ('plug in the answers', 'plugging in the answers')),
    'Understanding': ('הבנה / פתרון באמצעות הבנה / שאלת הבנה', ('by understanding',)),
    'Estimation': ('הערכת סדר גודל', ('estimate', 'estimation', 'estimating')),
    'Insight': ('הברקה', ('the insight', 'an insight')),
}
_SPEC_LABEL = _re.compile(r'^Method (\d) · (.+)$')


def vocab_problems(videos):
    """method labels of the spec VIDEOS ({vid: {'slides': [{'title', 'sb'}]}}) that are not in the vocabulary"""
    probs = []
    for vid, V in videos.items():
        for si, sl in enumerate(V['slides']):
            # the sidebar label is what the student sees (S: sb = the title); a continuation slide may keep a step title
            # such as "Method 2 · A plus inside" under its method's sidebar label
            for lab in [sl.get('sb') or sl.get('title') or '']:
                m = _SPEC_LABEL.match(lab)
                if not m: continue
                core = m.group(2).split(': ', 1)[0]
                if core not in CORE:
                    probs.append('%s slide %d: "%s" - use Method N · <%s>[: specific]' % (vid, si + 1, lab, ' | '.join(CORE)))
    return probs


def check_vocab(videos):
    """called by every _ai_vis_tNN.py after its scripts: a new method name outside the vocabulary stops the run"""
    probs = vocab_problems(videos)
    assert not probs, 'method names outside the vocabulary (math_patches/_method_names.py CORE):\n  ' + '\n  '.join(probs)


_PREFIX = _re.compile(r'^(?:(Method|Way|Approach)\s+(\d+)|(Shortcut))\s*·\s*')


def recorded(vid):
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


def new_title(old, name):
    if name.startswith('= '): return name[2:]          # not a method after all: a plain slide title
    m = _PREFIX.match(old)
    assert m, old
    return ('Shortcut · ' if m.group(3) else 'Method %s · ' % m.group(2)) + name


WARN = []


def method_names(M, topic):
    """Rename the method slides (and align naming lines / written-solution labels) of the videos listed for topic."""
    for vid, (t, names) in MAP.items():
        if t != topic or vid not in M.D['videos'] or recorded(vid): continue
        v = M.video(vid)
        sb = v.get('hybrid', {}).get('sidebar')
        lines = LINES.get(vid, {})
        hit = set()
        for b in v['beats']:
            old = b.get('title')
            if old not in names: continue
            new = new_title(old, names[old]); hit.add(old)
            b['title'] = new
            if sb: v['hybrid']['sidebar'] = sb = [new if x == old else x for x in sb]
            for l in b['lines']:
                if l.get('say') in lines: l['say'] = lines[l['say']]
            M.touched_videos.add(vid)
        for old in names:
            if old not in hit: WARN.append('%s: no slide "%s"' % (vid, old))
    for qid, (t, labels) in QLABELS.items():
        if t != topic or qid not in M.D['questions']: continue
        ex = list(M.q(qid).get('explanation') or [])
        out = []
        for p in ex:
            for old, new in labels:
                if old in p: p = p.replace(old, new, 1)
            out.append(p)
        miss = [old for old, new in labels if not any(old in p for p in ex)]
        for old in miss: WARN.append('%s: no label "%s"' % (qid, old))
        if out != ex: M.set_q(qid, expl=out)
    for w in WARN: print('  method_names WARNING:', w)
    del WARN[:]


# ---------------- data (reviewed 2026-10-07) ----------------
# MAP: videoId -> (topic, {old slide title: vocabulary name})

MAP = {
    # ---- topic 5 ----
    'solve-q-r26-t05-17': (5, {
        'Method 1 · Count the powers': 'Power count',
        'Method 2 · The algebra': 'Algebra',
    }),
    'solve-q-r26-t05-18': (5, {
        'Method 1 · Plug in, then count': 'Plugging in numbers',
        'Method 2 · The algebra': 'Algebra',
    }),
    # ---- topic 11 ----
    'solve-q-298': (11, {
        'Method 1 · Difference of squares': 'Contracted multiplication formulas',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    # ---- topic 12 ----
    'solve-q-330': (12, {
        'Method 1 · Solve it': 'Algebra',
        'Method 2 · Spot the pattern': 'Insight',
    }),
    'solve-q-332': (12, {
        'Method 1 · Two cases': 'Two cases',
        'Method 2 · Plug in the choices': 'Plugging in the answers',
    }),
    'solve-q-333': (12, {
        'Method 1 · The math': 'Algebra',
        'Method 2 · Understanding': 'Understanding',
    }),
    'solve-q-337': (12, {
        'Method 1 · Understanding': 'Understanding',
        'Method 2 · Counterexamples': 'Plugging in numbers',
    }),
    # ---- topic 13 ----
    'solve-q-362': (13, {
        'Method 1 · Plug in': 'Plugging in numbers',
        'Method 2 · Replace |x|': 'Algebra',
    }),
    'solve-q-363': (13, {
        'Method 1 · Understand the givens': 'Understanding',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-364': (13, {
        'Method 1 · Put it on the number line': 'Number line',
    }),
    'solve-q-365': (13, {
        'Method 1 · Analyze the givens': 'Understanding',
    }),
    'solve-q-366': (13, {
        'Method 1 · Test each choice': 'Understanding',
    }),
    'solve-q-367': (13, {
        'Method 1 · Full algebra': 'Algebra',
        'Method 2 · Algebra, then plug in': 'Plugging in the answers',
        'Method 3 · Plug in right away': 'Plugging in the answers',
    }),
    'solve-q-368': (13, {
        'Method 1 · Equal or opposite': 'Two cases',
        'Method 2 · Square both sides': 'Square both sides',
        'Method 3 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-369': (13, {
        'Method 1 · Two symmetric bands': 'Number line',
        'Method 2 · Plug in the answers': 'Plugging in the answers',
    }),
    'solve-q-370': (13, {
        'Method 1 · Two cases': 'Two cases',
        'Method 2 · Plug in': 'Plugging in the answers',
    }),
    'solve-q-r26-t13-03': (13, {
        'Method 1 · Two cases, then check': 'Two cases',
        'Method 2 · The right side is never negative': 'Understanding',
    }),
    'solve-q-r26-t13-13': (13, {
        'Method 1 · Read the signs': 'Understanding',
        'Method 2 · Try the four sign cases': 'Plugging in numbers',
    }),
    'solve-q-r26-t13-15': (13, {   # removed from the course 2026-10-11 (t13.py remove_mirror); kept so the older passes still run
        'Method 1 · The mirror test': 'Mirror test',
        'Method 2 · Check with algebra': 'Algebra',
    }),
    # ---- topic 14 ----
    'solve-q-392': (14, {
        'Method 1 · Break into primes': 'Prime factorization',
        'Method 2 · Plug in the answers': 'Plugging in the answers',
    }),
    'solve-q-394': (14, {
        'Method 1 · Understanding': 'Understanding',
        'Method 2 · Plug in primes': 'Plugging in numbers',
    }),
    'solve-q-397': (14, {
        'Method 1 · Prime squared': 'Understanding',
        'Method 2 · Find the pattern': 'Plugging in numbers',
    }),
    'solve-q-401': (14, {
        'Method 1 · Understand it': 'Understanding',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    # ---- topic 15 ----
    'solve-q-423': (15, {
        "Method 1 · Eliminate what can't be": 'Understanding',
        'Method 2 · Build it from the smallest group': 'Algebra',
    }),
    'solve-q-424': (15, {
        'Method 1 · Test the choices': 'Plugging in the answers',
        'Method 2 · List the pattern': 'Remainders',
    }),
    'solve-q-426': (15, {
        'Method 1 · Look at the constant': 'Understanding',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-430': (15, {
        'Method 1 · Count exactly': 'Calculation',
        'Method 2 · Estimate': 'Estimation',
    }),
    'solve-q-431': (15, {
        'Method 1 · Algebra': 'Algebra',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-432': (15, {
        'Method 1 · Factor it': 'Common factor',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-435': (15, {
        'Method 1 · Algebra + understanding': 'Tag it',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-r26-t15-01': (15, {
        'Method 1 · Subtract the remainders': 'Remainders',
        'Method 2 · Check with numbers': 'Plugging in numbers',
        'Method 3 · Tag it': 'Tag it',
    }),
    'solve-q-r26-t15-15': (15, {
        'Method 1 · Tag it': 'Tag it',
    }),
    # ---- topic 16 ----
    'consecutive-integers': (16, {
        'Way 1 · Algebra': 'Algebra',
        'Way 2 · Plug in': 'Plugging in numbers',
        'Way 3 · Differences': 'Understanding',
    }),
    'solve-q-458': (16, {
        'Way 1 · From the middle': 'Algebra',
        'Way 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-459': (16, {
        'Way 1 · Plug in': 'Plugging in numbers',
        'Way 2 · Differences': 'Understanding',
    }),
    'solve-q-460': (16, {
        'Way 1 · Plug in': 'Plugging in numbers',
        'Way 2 · Delete the powers': 'Insight',
    }),
    'solve-q-465': (16, {
        'Method 1 · Mark the signs': 'Understanding',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-466': (16, {
        'Method 1 · Read the givens': 'Understanding',
        'Method 2 · Simplify, then read': 'Algebra',
        'Method 3 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-467': (16, {
        'Method 1 · Start with the simple choices': 'Understanding',
        'Method 2 · Rule out the others': 'Plugging in numbers',
    }),
    'solve-q-468': (16, {
        'Method 1 · Formula three': 'Contracted multiplication formulas',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-469': (16, {
        'Method 1 · One unknown': 'Algebra',
        'Method 2 · Plug in the answers': 'Plugging in the answers',
    }),
    'solve-q-470': (16, {
        'Method 1 · Pure parity': 'Understanding',
        'Method 2 · Drop the powers': 'Insight',
        'Method 3 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-471': (16, {
        'Method 1 · Factor by factor': 'Understanding',
    }),
    'solve-q-472': (16, {
        'Method 1 · Count the 2s': 'Prime factorization',
        'Method 2 · Plug in — carefully': 'Plugging in numbers',
    }),
    # ---- topic 17 ----
    'solve-q-495': (17, {
        'Method 1 · Understanding': 'Understanding',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-497': (17, {
        'Method 1 · Understanding': 'Understanding',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-498': (17, {
        'Method 1 · The axis': 'Number line',
        'Method 2 · Plug in the answers': 'Plugging in the answers',
    }),
    'solve-q-499': (17, {
        'Method 1 · The axis': 'Number line',
        'Method 2 · Plug in': 'Plugging in numbers',
        'Method 3 · The shortcut': 'Insight',
    }),
    'solve-q-500': (17, {
        'Method 1 · Understanding': 'Understanding',
        'Method 2 · A smart plug-in': 'Plugging in numbers',
    }),
    'solve-q-r26-t17-03': (17, {
        'Method 1 · Flip, then multiply': 'Algebra',
        'Method 2 · Test the ends': 'Plugging in numbers',
    }),
    # ---- topic 18 ----
    'solve-q-517': (18, {
        'Method 1 · Size first': 'Estimation',
        'Method 2 · Insight': 'Units digit',
    }),
    'solve-q-520': (18, {
        'Method 1 · Algebraic form': 'Algebra',
        'Method 2 · Plug in the choices': 'Plugging in the answers',
    }),
    'solve-q-r26-t18-01': (18, {
        'Method 2 · Write 10A + B and collect': 'Algebra',
    }),
    # ---- topic 19 ----
    'solve-q-541': (19, {
        'Method 1 · Substitute': 'Calculation',
        'Method 2 · Factor first': 'Common factor',
    }),
    'solve-q-542': (19, {
        'Method 1 · Inside out': 'Calculation',
        'Method 2 · Twice the rule': 'Algebra',
    }),
    'solve-q-543': (19, {
        'Method 1 · Test each choice': 'Plugging in the answers',
    }),
    'solve-q-544': (19, {
        'Method 1 · Match the input': 'Understanding',
    }),
    'solve-q-545': (19, {
        'Method 1 · Check every step': 'Calculation',
    }),
    'solve-q-546': (19, {
        'Method 1 · Down, then up': 'Calculation',
        'Method 2 · Spot the pattern': 'Insight',
    }),
    'solve-q-547': (19, {
        'Method 1 · Down to the start': 'Understanding',
    }),
    'solve-q-548': (19, {
        'Method 1 · Isolate the operation': 'Algebra',
    }),
    'solve-q-549': (19, {
        'Method 1 · Check each choice': 'Algebra',
        'Method 2 · Plug in x = 1': 'Plugging in numbers',
    }),
    'solve-q-550': (19, {
        'Method 1 · Inside out': 'Calculation',
        'Method 2 · Spot the shortcut': 'Insight',
    }),
    'solve-q-551': (19, {
        'Method 1 · Three calculations': 'Calculation',
        'Method 2 · Spot the formulas': 'Contracted multiplication formulas',
    }),
    'solve-q-552': (19, {
        'Method 1 · Full math': 'Algebra',
        'Method 2 · Plug in a = 1': 'Plugging in numbers',
    }),
    'solve-q-553': (19, {
        'Method 1 · Full math': 'Algebra',
        'Method 2 · The insight': 'Insight',
        'Method 3 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-554': (19, {
        'Method 1 · Calculate each choice': 'Calculation',
        'Method 2 · Min–max thinking': 'Understanding',
    }),
    'solve-q-556': (19, {
        'Method 1 · Plug in x = 1': 'Plugging in numbers',
        'Method 2 · Understanding': 'Understanding',
    }),
    'solve-q-r26-t19-01': (19, {
        'Method 1 · Brackets': 'Algebra',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-q-r26-t19-02': (19, {
        'Method 1 · One counterexample': 'Plugging in numbers',
        'Method 2 · Swap the letters': 'Algebra',
    }),
    'solve-q-r26-t19-03': (19, {
        'Method 1 · Try both rules': 'Two cases',
        'Method 2 · Work back from the answers': 'Plugging in the answers',
    }),
    'solve-q-r26-t19-05': (19, {
        'Method 1 · Full calculation': 'Calculation',
        'Method 2 · Only odd powers survive': 'Insight',
    }),
    'solve-q-r26-t19-18': (19, {
        'Method 1 · Put each rule on trial': 'Plugging in numbers',
        'Method 2 · Know the family': 'Understanding',
    }),
    # ---- topic 20 ----
    'solve-q-577': (20, {
        'Method 1 · Find the maximum': 'Understanding',
        'Method 2 · Plug in the maximum': 'Plugging in numbers',
        'Method 3 · Test the answers': 'Plugging in the answers',
    }),
    'solve-q-578': (20, {
        'Method 1 · Plug in 1 and 1': 'Plugging in numbers',
        'Method 2 · Scale factor k': 'Algebra',
    }),
    'solve-q-r26-t20-03': (20, {
        'Method 1 · First and last': 'Algebra',
        'Method 2 · Half of the numbers': 'Insight',
    }),
    # ---- topic 21 ----
    'solve-q-r26-t21-01': (21, {
        'Method 1 · Worst luck + 1': 'Understanding',
        'Method 2 · Spot the traps': '= Spot the traps',
    }),
    'solve-q-r26-t21-02': (21, {
        'Method 1 · Hunt for counterexamples': 'Plugging in numbers',
        'Method 2 · Prove the survivor': 'Understanding',
    }),
    'solve-wp21-g004': (21, {
        'Method 1 · Draw and follow': 'Understanding',
        'Method 2 · The other road': 'Understanding',
        'Method 3 · Net change': 'Insight',
    }),
    'solve-wp21-g005': (21, {
        'Method 1 · Build and test': 'Plugging in numbers',
        'Method 2 · Count the gaps': 'Insight',
    }),
    'solve-wp21-g007': (21, {
        'Method 1 · Give each the minimum': 'Understanding',
        'Method 2 · Smallest-sum formula': 'Algebra',
    }),
    'solve-wp21-g009': (21, {
        'Method 1 · Step by step': 'Calculation',
        'Method 2 · Check backwards': 'Plugging in the answers',
    }),
    'solve-wp21-g010': (21, {
        'Method 1 · Plug in n = 3': 'Plugging in numbers',
        'Method 2 · Why not n = 1?': 'Plugging in numbers',
    }),
    'solve-wp21-g013': (21, {
        'Method 1 · In order, from the minimum': 'Understanding',
        'Method 2 · The pattern': 'Remainders',
    }),
    'solve-wp21-g014': (21, {
        'Method 1 · Plug in from the middle': 'Plugging in the answers',
        'Method 2 · Divisibility elimination': 'Understanding',
    }),
    'solve-wp21-g017': (21, {
        'Method 1 · Min and max per student': 'Understanding',
        'Method 2 · Last digit — and its limit': 'Units digit',
    }),
    'solve-wp21-g018': (21, {
        'Method 1 · Min front, max back': 'Understanding',
        'Shortcut · The most precise range': 'Plugging in the answers',
    }),
    'solve-wp21-g019': (21, {
        'Method 1 · Least in, most out': 'Understanding',
        'Method 2 · Last digit': 'Units digit',
    }),
    'solve-wp21-g020': (21, {
        'Method 1 · Plug in the answers': 'Plugging in the answers',
        'Method 2 · Min and max thinking': 'Understanding',
    }),
    'solve-wp21-g021': (21, {
        'Method 1 · Count the spare stickers': 'Understanding',
        'Method 2 · Only the ends?': 'Insight',
    }),
    'solve-wp21-g024': (21, {
        'Method 1 · Draw it the quick way': 'Understanding',
        'Method 2 · The remainder': 'Remainders',
    }),
    'solve-wp21-g025': (21, {
        'Method 1 · List them': 'Listing',
        'Method 2 · Common multiple': 'Insight',
    }),
    # ---- topic 22 ----
    'solve-q-r26-t22-03': (22, {
        'Method 1 · Keep the fixed part': 'Ratios',
        'Method 2 · Equation': 'Algebra',
    }),
    'solve-q-r26-t22-04': (22, {
        'Method 1 · Choose numbers': 'Plugging in numbers',
        'Method 2 · Build it': 'Algebra',
    }),
    'solve-q-r26-t22-05': (22, {
        'Method 1 · Assume all the same': 'Insight',
        'Method 2 · Assume the other kind': 'Insight',
    }),
    'solve-q-r26-t22-20': (22, {
        'Method 1 · The gap': 'Insight',
        'Method 2 · Before and after': 'Algebra',
    }),
    'solve-wp22-g042': (22, {
        'Method 1 · Same ratios': 'Ratios',
        'Method 2 · Size estimate': 'Estimation',
    }),
    'solve-wp22-g043': (22, {
        'Method 1 · Stage by stage': 'Calculation',
        'Method 2 · Write it all first': 'Insight',
    }),
    'solve-wp22-g044': (22, {
        'Method 1 · Ratio units': 'Ratios',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-wp22-g045': (22, {
        'Method 1 · Plug in, then fix it': 'Plugging in numbers',
        'Method 2 · Size estimate': 'Estimation',
    }),
    'solve-wp22-g046': (22, {
        'Method 1 · Check each option': 'Two cases',
        'Method 2 · Size estimate': 'Estimation',
    }),
    'solve-wp22-g047': (22, {
        'Method 1 · Build an equation': 'Algebra',
        'Method 2 · Divisibility': 'Ratios',
    }),
    'solve-wp22-g048': (22, {
        'Method 1 · What changed?': 'Insight',
        'Method 2 · Two equations': 'Algebra',
        'Method 3 · Plug in the answers': 'Plugging in the answers',
    }),
    'solve-wp22-g049': (22, {
        'Method 1 · Scale everything': 'Insight',
        'Method 2 · Shrink first': 'Algebra',
    }),
    'solve-wp22-g050': (22, {
        'Method 1 · Build equations': 'Algebra',
        'Method 2 · Start from the end': 'Insight',
    }),
    # ---- topic 23 ----
    'solve-q-r26-t23-01': (23, {
        'Method 1 · Multipliers': 'Percent multipliers',
        'Method 2 · Plug in 100': 'Plugging in numbers',
    }),
    'solve-q-r26-t23-03': (23, {
        'Method 1 · Plug in 100': 'Plugging in numbers',
        'Method 2 · Arrow map': 'Arrow map',
    }),
    'solve-q-r26-t23-04': (23, {
        'Method 1 · What stays?': 'Insight',
        'Method 2 · Test the choices': 'Plugging in the answers',
    }),
    'solve-q-r26-t23-05': (23, {
        'Method 1 · Plug in numbers': 'Plugging in numbers',
        'Method 2 · Build it': 'Algebra',
    }),
    'solve-q-r26-t23-16': (23, {
        'Method 1 · The flip rule': 'Flip rule',
    }),
    'solve-wp23-g054': (23, {
        'Method 1 · Plug in 100': 'Plugging in numbers',
        'Method 2 · Percent tree': 'Percent multipliers',
    }),
    'solve-wp23-g057': (23, {
        'Method 1 · Calculate': 'Calculation',
        'Method 2 · Read the choices': 'Insight',
    }),
    'solve-wp23-g058': (23, {
        'Method 1 · Calculate the drop': 'Calculation',
        'Method 2 · The complement': 'Complement',
    }),
    'solve-wp23-g059': (23, {
        'Method 1 · Two fractions': 'Calculation',
        'Method 2 · Add 25% again': 'Understanding',
    }),
    'solve-wp23-g060': (23, {
        'Method 1 · Algebra': 'Percent multipliers',
        'Method 2 · Plug in 100': 'Plugging in numbers',
    }),
    'solve-wp23-g061': (23, {
        'Method 1 · Plug in 100': 'Plugging in numbers',
        'Method 2 · Consecutive fractions': 'Insight',
        'Method 3 · Arrow map': 'Arrow map',
    }),
    'solve-wp23-g062': (23, {
        'Method 1 · Calculate': 'Algebra',
        'Method 2 · Swap and scale': 'Insight',
    }),
    'solve-wp23-g063': (23, {
        'Method 1 · Compare the tops': 'Algebra',
        'Method 2 · Inverse ratio': 'Compare by factors',
    }),
    'solve-wp23-g064': (23, {
        'Method 1 · Equal ratios': 'Ratios',
        'Method 2 · Shortcut': 'Insight',
    }),
    'solve-wp23-g065': (23, {
        'Method 1 · Plug in 100%': 'Plugging in numbers',
        'Method 2 · Test the round answer': 'Plugging in the answers',
    }),
    # ---- topic 24 ----
    'solve-q-r26-t24-01': (24, {
        'Method 1 · What makes it small': 'Understanding',
        'Method 2 · Check on the strip': 'The squares method',
    }),
    'solve-q-r26-t24-02': (24, {
        'Method 1 · The table': 'Plugging in numbers',
    }),
    'solve-q-r26-t24-03': (24, {
        'Method 1 · Who is missing': 'Complement',
        'Method 2 · One line': 'Algebra',
    }),
    'solve-wp24-g070': (24, {
        'Method 1 · The squares': 'The squares method',
        'Method 2 · One line': 'Algebra',
    }),
    'solve-wp24-g071': (24, {
        'Method 1 · Through the union': 'Algebra',
        'Method 2 · The squares': 'The squares method',
    }),
    'solve-wp24-g072': (24, {
        'Method 1 · Boxes with x': 'The squares method',
        'Method 2 · Plug in': 'Plugging in numbers',
        'Method 3 · Flip rule': 'Flip rule',
    }),
    'solve-wp24-g074': (24, {
        'Method 1 · Counts': 'Algebra',
        'Method 2 · Stay in percent': 'Insight',
        'Method 3 · See the range': 'The squares method',
    }),
    'solve-wp24-g075': (24, {
        'Method 1 · Through the union': 'Understanding',
        'Method 2 · Complements': 'Complement',
        'Method 3 · The insight': 'Insight',
    }),
    'solve-wp24-g076': (24, {
        'Method 1 · Add the fractions': 'Algebra',
        'Method 2 · Percent': 'Plugging in numbers',
    }),
    'solve-wp24-g077': (24, {
        'Method 1 · Boxes in fractions': 'The squares method',
        'Method 2 · People first': 'Algebra',
    }),
    'solve-wp24-g078': (24, {
        'Method 1 · Read it right': 'Understanding',
        'Method 2 · The squares': 'The squares method',
    }),
    # ---- topic 25 ----
    'solve-q-r26-t25-01': (25, {
        'Method 1 · The balance': 'Balance (averages)',
        'Method 2 · Equation': 'Algebra',
    }),
    'solve-q-r26-t25-02': (25, {
        'Method 1 · The balance': 'Balance (averages)',
        'Method 2 · The formula': 'Algebra',
    }),
    'solve-q-r26-t25-05': (25, {
        'Method 1 · Every value changes': 'Understanding',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-wp25-g083': (25, {
        'Method 1 · The formula': 'Algebra',
        'Method 2 · The balance point': 'Balance (averages)',
    }),
    'solve-wp25-g084': (25, {
        'Method 1 · The formula': 'Algebra',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-wp25-g085': (25, {
        'Method 1 · Table and formula': 'Algebra',
        'Method 2 · Plug in + balance point': 'Plugging in numbers',
    }),
    'solve-wp25-g087': (25, {
        'Method 1 · The formula': 'Algebra',
        'Method 2 · Ratios': 'Balance (averages)',
    }),
    'solve-wp25-g088': (25, {
        'Method 1 · Ratios': 'Balance (averages)',
        'Method 2 · The formula': 'Algebra',
    }),
    'solve-wp25-g089': (25, {
        'Method 1 · The formula': 'Algebra',
        'Method 2 · Eliminate, then ratios': 'Balance (averages)',
    }),
    'solve-wp25-g090': (25, {
        'Method 1 · The formula': 'Algebra',
        'Method 2 · Ratios': 'Balance (averages)',
        'Method 3 · Extra per item': 'Insight',
    }),
    'solve-wp25-p18': (25, {
        'Method 1 · Averages into sums': 'Algebra',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    # ---- topic 26 ----
    'solve-q-r26-t26-01': (26, {
        'Method 1 · Flip the fraction': 'Compare by factors',
        'Method 2 · Pick a job size': 'Plugging in numbers',
    }),
    'solve-q-r26-t26-02': (26, {
        'Method 1 · Sense check': 'Estimation',
        'Method 2 · The shortcut': 'Algebra',
    }),
    'solve-q-r26-t26-03': (26, {
        'Method 1 · Pick a job size': 'Plugging in numbers',
        'Method 2 · Fractions': 'Algebra',
    }),
    'solve-q-r26-t26-04': (26, {
        'Method 1 · Total work ÷ total time': 'Algebra',
        'Method 2 · Estimate': 'Estimation',
        'Method 3 · Shares as weights': 'Balance (averages)',
    }),
    'solve-q-r26-t26-21': (26, {
        'Method 1 · Compare by factors': 'Compare by factors',
    }),
    'solve-wp26-g093': (26, {
        'Method 1 · Step by step': 'Compare by factors',
        'Method 2 · Triangle value': 'Ratios',
        'Method 3 · Rate × time': 'Algebra',
        'Method 4 · Plug in numbers': 'Plugging in numbers',
    }),
    'solve-wp26-g095': (26, {
        'Method 1 · Combined rate': 'Algebra',
        'Method 2 · Pick a pond size': 'Plugging in numbers',
    }),
    'solve-wp26-g096': (26, {
        'Method 1 · Equalize the times': 'Ratios',
        'Method 2 · Add the rates': 'Algebra',
    }),
    'solve-wp26-g098': (26, {
        'Method 1 · Ratios': 'Ratios',
        'Method 2 · The V method': 'The V method',
        'Method 3 · Worker-hours': 'Insight',
    }),
    'solve-wp26-g101': (26, {
        'Method 1 · Build an equation': 'Algebra',
        'Method 2 · Plug in numbers': 'Plugging in numbers',
    }),
    'solve-wp26-g102': (26, {
        'Method 1 · Ratios in minutes': 'Ratios',
        'Method 2 · Work in hours': 'Algebra',
    }),
    'solve-wp26-g103': (26, {
        'Method 1 · Equalize the times': 'Ratios',
        'Method 2 · Estimate': 'Estimation',
    }),
    'solve-wp26-g104': (26, {
        'Method 1 · Merge two workers': 'Algebra',
        'Method 2 · The insight': 'Insight',
    }),
    'solve-wp26-g105': (26, {
        'Method 1 · The V method': 'The V method',
        'Method 2 · Ratios': 'Ratios',
        'Method 3 · Worker-hours': 'Insight',
    }),
    'solve-wp26-g105b': (26, {
        'Method 1 · Estimate first': 'Estimation',
        'Method 2 · Plug in numbers': 'Plugging in numbers',
        'Method 3 · Team question': 'The V method',
    }),
    # ---- topic 27 ----
    'solve-q-r26-t27-06': (27, {
        'Method 1 · Plug in numbers': 'Plugging in numbers',
        'Method 2 · Algebra': 'Algebra',
        'Method 3 · Power count with units': 'Power count',
    }),
    'solve-q-r26-t27-31': (27, {
        'Method 1 · The V': 'The V method',
        'Method 2 · Compare by factors': 'Compare by factors',
    }),
    'solve-wp27-g109': (27, {
        'Method 1 · Logic, then a table': 'Plugging in numbers',
        'Method 2 · Shares as weights': 'Balance (averages)',
    }),
    'solve-wp27-g111': (27, {
        'Method 1 · Ratios': 'Ratios',
        'Method 2 · Plug in numbers': 'Plugging in numbers',
        'Method 3 · Eliminate': 'Understanding',
    }),
    'solve-wp27-g112': (27, {
        'Method 1 · Ratios': 'Ratios',
        'Method 2 · Plug in numbers': 'Plugging in numbers',
    }),
    'solve-wp27-g116': (27, {
        'Method 1 · The starting gap': 'Algebra',
        'Method 2 · A quick check': 'Insight',
    }),
    'solve-wp27-g117': (27, {
        'Method 1 · Calculate': 'Calculation',
        'Method 2 · Identical ratios': 'Ratios',
    }),
    'solve-wp27-g118': (27, {
        'Method 1 · Calculate': 'Calculation',
        'Method 2 · Ratios': 'Ratios',
        'Method 3 · Insight': 'Insight',
    }),
    'solve-wp27-g119': (27, {
        'Method 1 · Equation': 'Algebra',
        'Method 2 · Plug in answers': 'Plugging in the answers',
    }),
    'solve-wp27-g120': (27, {
        'Method 1 · Calculate': 'Calculation',
        'Method 2 · Ratios': 'Ratios',
        'Method 3 · Estimate': 'Estimation',
    }),
    'solve-wp27-g121': (27, {
        'Method 1 · Relative speed': 'Insight',
        'Method 2 · Check with an equation': 'Algebra',
    }),
    # ---- topic 28 ----
    'solve-q-r26-t28-04': (28, {
        'Method 1 · All minus none': 'Complement',
    }),
    'solve-q-r26-t28-05': (28, {
        'Method 1 · Every letter chooses': 'Counting in stages',
        'Method 2 · Check a small case': 'Plugging in numbers',
    }),
    'solve-q-r26-t28-06': (28, {
        'Method 1 · Glue, then the order inside': 'Counting in stages',
    }),
    'solve-q-r26-t28-07': (28, {
        'Method 1 · Gaps': 'Counting in stages',
        'Method 2 · All minus together': 'Complement',
    }),
    'solve-q-r26-t28-08': (28, {
        'Method 1 · Divide by the repeats': 'Counting in stages',
    }),
    'solve-q-r26-t28-09': (28, {
        'Method 1 · Glue, then fix one': 'Counting in stages',
        'Method 2 · Fix Dana': 'Counting in stages',
    }),
    'solve-q-r26-t28-28': (28, {
        'Method 1 · Take out the smaller factorial': 'Common factor',
        'Method 2 · Everything in eight factorials': 'Calculation',
    }),
    'solve-wp28-g124': (28, {
        'Method 1 · List and check': 'Listing',
        'Method 2 · Leave one digit out': 'Insight',
    }),
    'solve-wp28-g125': (28, {
        'Method 1 · Multiply the stages': 'Counting in stages',
        'Method 2 · The grid': 'Understanding',
    }),
    'solve-wp28-g126': (28, {
        'Method 1 · Stages, with dependence': 'Counting in stages',
        'Method 2 · List them': 'Listing',
    }),
    'solve-wp28-g128': (28, {
        'Method 1 · The pool stays full': 'Counting in stages',
    }),
    'solve-wp28-g129': (28, {
        'Method 1 · The pool shrinks': 'Counting in stages',
    }),
    'solve-wp28-g130': (28, {
        'Method 1 · Stage by stage': 'Counting in stages',
    }),
    'solve-wp28-g132': (28, {
        'Method 1 · Count, then halve': 'Counting in stages',
        'Method 2 · Descending list': 'Listing',
    }),
    'solve-wp28-g133': (28, {
        'Method 1 · Draw and count': 'Listing',
        'Method 2 · All lines minus sides': 'Counting in stages',
        'Method 3 · Descending sum': 'Insight',
        'Method 4 · The formula': 'Algebra',
    }),
    'solve-wp28-g135': (28, {
        'Method 1 · Two cases, then add': 'Two cases',
        'Method 2 · All minus forbidden': 'Complement',
    }),
    'solve-wp28-g136': (28, {
        'Method 1 · All minus forbidden': 'Complement',
        'Method 2 · Count directly': 'Counting in stages',
    }),
    'solve-wp28-g138': (28, {
        'Method 1 · Choose, then divide by 5!': 'Counting in stages',
        'Method 2 · No extra ÷2': 'Understanding',
    }),
    'solve-wp28-g139': (28, {
        'Method 1 · Choose who stays out': 'Complement',
        'Method 2 · The long way': 'Counting in stages',
    }),
    'solve-wp28-g140': (28, {
        'Method 1 · Write it all out': 'Calculation',
        'Method 2 · Expand only as far as needed': 'Insight',
    }),
    'solve-wp28-g141': (28, {
        'Method 1 · Option counts per digit': 'Counting in stages',
        'Method 2 · List the outside pairs': 'Listing',
    }),
    'solve-wp28-g142': (28, {
        'Method 1 · Options per position': 'Counting in stages',
        'Method 2 · Trial and error': 'Listing',
        'Method 3 · Subtract the failures': 'Complement',
    }),
    'solve-wp28-g143': (28, {
        'Method 1 · The mutual-action formula': 'Algebra',
        'Method 2 · Test the answers': 'Plugging in the answers',
        'Method 3 · A growing sequence': 'Listing',
    }),
    'solve-wp28-g144': (28, {
        'Method 1 · Trial and error': 'Listing',
        'Method 2 · Choose who stays out': 'Complement',
    }),
    # ---- topic 29 ----
    'solve-q-r26-t29-01': (29, {
        'Method 2 · Two circles': 'Venn diagram',
    }),
    'solve-wp29-g147': (29, {
        'Method 2 · Pair them up': 'Insight',
    }),
    'solve-wp29-g149': (29, {
        'Method 2 · Equal groups': 'Understanding',
    }),
    'solve-wp29-g150': (29, {
        'Method 2 · Red first': 'Calculation',
    }),
    'solve-wp29-g152': (29, {
        'Method 2 · Count the pairs': 'Counting in stages',
    }),
    'solve-wp29-g153': (29, {
        'Method 2 · Count the sequences': 'Counting in stages',
    }),
    'solve-wp29-g156': (29, {
        'Method 2 · Count the matches': 'Calculation',
    }),
    'solve-wp29-g157': (29, {
        'Method 2 · Both orders': 'Two cases',
    }),
    'solve-wp29-g158': (29, {
        'Method 1 · Count the boxes': 'Calculation',
        'Method 2 · Two cases': 'Two cases',
        'Method 3 · Complement': 'Complement',
    }),
    'solve-wp29-g160': (29, {
        'Method 2 · Count them': 'Calculation',
    }),
    'solve-wp29-g161': (29, {
        'Method 1 · Ella first': 'Calculation',
        'Method 2 · Omar first': 'Insight',
    }),
    'solve-wp29-g162': (29, {
        'Method 1 · Multiply': 'Algebra',
        'Method 2 · Plug in': 'Plugging in numbers',
    }),
    'solve-wp29-g163': (29, {
        'Method 1 · Wanted over total': 'Calculation',
        'Method 2 · Complement': 'Complement',
    }),
    'solve-wp29-g164': (29, {
        'Method 1 · Day by day': 'Calculation',
    }),
    'solve-wp29-g165': (29, {
        'Method 1 · Multiply': 'Calculation',
        'Method 2 · Symmetry': 'Symmetry',
    }),
    # ---- topic 30 ----
    'solve-geo30-g006': (30, {
        'Method 1 · The full math': 'Algebra',
        'Method 2 · Plug in numbers': 'Plugging in numbers',
        'Method 3 · A flash of insight': 'Insight',
    }),
    'solve-q-r26-t30-03': (30, {
        'Method 1 · The zig-zag rule': 'Insight',
        'Method 2 · Parallel lines': 'Parallel lines',
    }),
    # ---- topic 31 ----
    'solve-geo31-g011': (31, {
        'Shortcut · Pick values that fit': 'Plugging in numbers',
    }),
    'solve-geo31-g031': (31, {
        'Method 1 · Angle sum': 'Angle sum in a triangle',
        'Method 2 · Exterior angle': 'Insight',
        'Method 3 · Plug in numbers': 'Plugging in numbers',
    }),
    'solve-geo31-g037': (31, {
        'Method 1 · Subtract areas': 'Area formulas',
        'Method 2 · The shaded triangles': 'Insight',
    }),
    'solve-geo31-g038': (31, {
        'Method 1 · Unknowns': 'Algebra',
        'Method 2 · Area ratio': 'Ratios',
    }),
    'solve-geo31-g039': (31, {
        'Method 1 · Full calculation': 'Pythagoras',
        'Method 2 · Cancel sides': 'Insight',
        'Method 3 · Estimate': 'Estimation',
    }),
    'solve-geo31-g040': (31, {
        'Method 1 · The equation': 'Algebra',
        'Method 2 · Plug in answers': 'Plugging in the answers',
    }),
    # ---- topic 32 ----
    'solve-geo32-g048': (32, {
        'Shortcut · Pick values that fit': 'Plugging in numbers',
    }),
    'solve-geo32-g059': (32, {
        'Way 1 · A median': 'Insight',
        'Way 2 · Four equal areas': 'Symmetry',
        'Way 3 · Base × height': 'Area formulas',
    }),
    'solve-geo32-g067': (32, {
        'Method 1 · The math way': 'Algebra',
        'Method 2 · Symmetry': 'Symmetry',
    }),
    'solve-geo32-g069': (32, {
        'Method 1 · The math way': 'Algebra',
        'Method 2 · Ratios': 'Ratios',
    }),
    'solve-geo32-g070': (32, {
        'Approach 1 · Subtract areas': 'Area formulas',
        'Approach 2 · Completions': 'Insight',
        'Approach 3 · Split with symmetry': 'Symmetry',
    }),
    'solve-geo32-g071': (32, {
        'Method 1 · Full solution': 'Algebra',
        'Method 2 · Plug in numbers': 'Plugging in numbers',
    }),
    'solve-q-r26-t32-07': (32, {
        'Method 1 · The identity': 'Contracted multiplication formulas',
        'Method 2 · Work back from the answers': 'Plugging in numbers',
    }),
    # ---- topic 33 ----
    'solve-geo33-g076': (33, {
        'Method 1 · Add a point': 'Inscribed angle',
        'Method 2 · The big central angle': 'Insight',
    }),
    'solve-geo33-g096': (33, {
        'Method 1 · The math way': 'Algebra',
        'Method 2 · Plug in r': 'Plugging in numbers',
        'Method 3 · Estimate': 'Estimation',
    }),
    'solve-geo33-g097': (33, {
        'Shortcut · Symmetry': 'Symmetry',
    }),
    'solve-geo33-g100': (33, {
        'Method 1 · The math way': 'Algebra',
        'Method 2 · Estimate': 'Estimation',
    }),
    'solve-geo33-g101': (33, {
        'Method 1 · The math way': 'Algebra',
        'Method 2 · Plug in from the middle': 'Plugging in the answers',
    }),
    'solve-geo33-g102': (33, {
        'Method 1 · The math way': 'Algebra',
        'Method 2 · Plug in numbers': 'Plugging in numbers',
    }),
    # ---- topic 34 ----
    'solve-geo34-g110': (34, {
        'Way 1 · The triangle': 'Angle sum in a triangle',
        'Way 2 · The trapezoid': 'Insight',
        'Way 3 · The diagonals': 'Inscribed angle',
    }),
    # ---- topic 35 ----
    'solve-geo35-g126': (35, {
        'Approach 1 · Full math': 'Algebra',
        'Approach 2 · Plug in numbers': 'Plugging in numbers',
        'Approach 3 · Estimate': 'Estimation',
    }),
    'solve-geo35-g127': (35, {
        'Approach 1 · An equation': 'Algebra',
        'Approach 2 · Ratio units': 'Ratios',
    }),
    'solve-geo35-g128': (35, {
        'Approach 1 · The inner triangle': 'Pythagoras',
        'Approach 2 · Estimate': 'Estimation',
    }),
    'solve-geo35-g129': (35, {
        'Approach 1 · Base and height': 'Area formulas',
        'Approach 2 · It is equilateral': 'Insight',
    }),
}

# LINES: videoId -> {spoken line that names the method: aligned line}
LINES = {
    'consecutive-integers': {
        'Way one: write them with algebra.':
            'Method one: algebra.',
        'Way two: plug in numbers.':
            'Method two: plugging in numbers.',
        'Way three: understand the differences.':
            'Method three: understanding the differences.',
    },
    'solve-geo32-g067': {
        'Method one: the full math solution.':
            'Method one: algebra.',
    },
    'solve-geo33-g101': {
        "Now the psychometric way: plugging in answers. They're all round numbers — easy to plug in.":
            "Now the psychometric way: plugging in the answers. They're all round numbers — easy to plug in.",
    },
    'solve-q-367': {
        'Method one: full algebra.':
            'Method one: algebra.',
    },
    'solve-q-466': {
        'Approach two: simplify each expression first, then read the signs.':
            'Approach two: algebra — simplify each expression first, then read the signs.',
        'Approach three: plug in. x is positive — take one. y is negative — take negative one.':
            'Approach three: plugging in numbers. x is positive — take one. y is negative — take negative one.',
    },
    'solve-q-517': {
        'Method one: the full math. First — estimate the size.':
            'Method one: estimation. First — estimate the size.',
        'Method two — the insight. A times A ends in A, so A is zero, one, five or six.':
            'Method two — the units digit. A times A ends in A, so A is zero, one, five or six.',
    },
    'solve-q-520': {
        'Method one: the math. x is a two-digit number — tens digit T, units digit U.':
            'Method one: algebra. x is a two-digit number — tens digit T, units digit U.',
        'Method two: plug in the choices. They offer the tens digit — try each one as T.':
            'Method two: plugging in the answers. They offer the tens digit — try each one as T.',
    },
    'solve-q-577': {
        "Third way: test the answers. Which value can't b plus c be?":
            "Third way: plug in the answers. Which value can't b plus c be?",
    },
    'solve-q-r26-t23-04': {
        'Or test the choices. Try the round one — a hundred.':
            'Or plug in the answers. Try the round one — a hundred.',
    },
    'solve-wp22-g042': {
        'Two ways: same ratios, then a size estimate.':
            'Two ways: ratios, then estimation.',
    },
    'solve-wp22-g045': {
        'Two groups, two different fractions. Plug in — then a size estimate.':
            'Two groups, two different fractions. Plug in numbers — then estimation.',
    },
    'solve-wp23-g065': {
        'Or test the choices. Which first? The roundest one — three hundred.':
            'Or plug in the answers. Which first? The roundest one — three hundred.',
    },
    'solve-wp25-g083': {
        'Two ways: the formula — and the balance point.':
            'Two ways: algebra — and the balance.',
    },
    'solve-wp25-g087': {
        'The exam weighs twice as much. Formula first — then the see-saw.':
            'The exam weighs twice as much. Algebra first — then the balance.',
    },
}

# QLABELS: questionId -> (topic, [(old written-solution label, new label)])
QLABELS = {
    'q-r26-t01-11': (1, [('Method 1 · brackets first', 'Method 1 · Calculation'), ('Method 2 · open the brackets', 'Method 2 · Algebra')]),
    'q-r26-t01-15': (1, [('Method 1 · last digit and estimate', 'Method 1 · Units digit'), ('Method 2 · split', 'Method 2 · Calculation')]),
    'q-187': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-194': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-199': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-201': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-202': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-204': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-206': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-216': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-217': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-r26-t07-15': (7, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-300': (11, [('Method 2 · Try a choice', 'Method 2 · Plugging in the answers')]),
    'q-315': (11, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'alg-extra-unit-t12-3-1': (12, [('Method 2 · Two moves', 'Method 2 · Plugging in numbers')]),
    'q-324': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-325': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-328': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-331': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-346': (12, [('Method 2 · Two moves', 'Method 2 · Plugging in numbers')]),
    'q-347': (12, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-349': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-352': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-353': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-354': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-355': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-r26-t12-02': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-r26-t12-06': (12, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-370': (13, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-371': (13, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-374': (13, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-375': (13, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-498': (17, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-506': (17, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-r26-t17-03': (17, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'q-r26-t17-09': (17, [('Method 2 · The most precise range', 'Method 2 · Plugging in the answers')]),
    'alg-extra-unit-t18-3-6': (18, [('Method 2 · Words, no columns', 'Method 2 · Algebra')]),
    'alg-extra-unit-t18-3-7': (18, [('Method 2 · Write 10A + B and collect', 'Method 2 · Algebra')]),
    'q-526': (18, [('Method 2 · Write 10A + B and collect', 'Method 2 · Algebra')]),
    'q-530': (18, [('Method 2 · Words, no columns', 'Method 2 · Algebra')]),
    'q-533': (18, [('Method 2 · Write 10A + B and collect', 'Method 2 · Algebra')]),
    'q-535': (18, [('Method 2 · Write 10A + B and collect', 'Method 2 · Algebra')]),
    'q-r26-t18-01': (18, [('Method 2 · Write 10A + B and collect', 'Method 2 · Algebra')]),
    'q-r26-t18-04': (18, [('Method 2 · Write 10A + B and collect', 'Method 2 · Algebra')]),
    'wp21-g018': (21, [('Shortcut · The most precise range', 'Shortcut · Plugging in the answers')]),
    'wp21-p09': (21, [('Shortcut · The most precise range', 'Shortcut · Plugging in the answers')]),
    'wp21-p19': (21, [('Shortcut · The most precise range', 'Shortcut · Plugging in the answers')]),
    'wp22-g045': (22, [('Shortcut · Percent shares as weights', 'Shortcut · Balance (averages)')]),
    'wp22-p18': (22, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'wp22-p27': (22, [('Shortcut · Two moves', 'Shortcut · Plugging in numbers')]),
    'wp22-p29': (22, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'q-r26-t23-12': (23, [('Shortcut · Percent shares as weights', 'Shortcut · Balance (averages)')]),
    'q-r26-t24-05': (24, [('Shortcut · Percent shares as weights', 'Shortcut · Balance (averages)')]),
    'wp25-g087': (25, [('Shortcut · Percent shares as weights', 'Shortcut · Balance (averages)')]),
    'wp25-g088': (25, [('Shortcut · Percent shares as weights', 'Shortcut · Balance (averages)')]),
    'wp25-g089': (25, [('Method 2 · Percent shares as weights', 'Method 2 · Balance (averages)')]),
    'wp25-g090': (25, [('Method 2 · Percent shares as weights, backwards', 'Method 2 · Balance (averages), backwards')]),
    'wp25-p02': (25, [('Method 2 · Percent shares as weights', 'Method 2 · Balance (averages)')]),
    'wp25-p04': (25, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'wp25-p16': (25, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'wp25-p19': (25, [('Method 2 · Percent shares as weights', 'Method 2 · Balance (averages)')]),
    'wp25-p20': (25, [('Method 2 · Percent shares as weights', 'Method 2 · Balance (averages)')]),
    'wp25-p23': (25, [('Method 2 · Percent shares as weights', 'Method 2 · Balance (averages)')]),
    'wp25-p27': (25, [('Method 2 · Percent shares as weights, backwards', 'Method 2 · Balance (averages), backwards')]),
    'q-r26-t26-04': (26, [('Method 3 · Percent shares as weights (the weights are the hours)', 'Method 3 · Balance (averages), the weights are the hours')]),
    'wp26-g102': (26, [('Method 3 · Catching up (difference in rates)', 'Method 3 · Insight')]),
    'wp26-p09': (26, [('Method 2 · Percent shares as weights (the weights are the days)', 'Method 2 · Balance (averages), the weights are the days')]),
    'q-r26-t27-06': (27, [('Method 3 · Power count with units', 'Method 3 · Power count')]),
    'q-r26-t27-22': (27, [('Method 2 · Percent shares as weights (the weights are the hours)', 'Method 2 · Balance (averages), the weights are the hours')]),
    'wp27-g109': (27, [('Method 2 · Percent shares as weights (the weights are the hours)', 'Method 2 · Balance (averages), the weights are the hours')]),
    'wp27-p02': (27, [('Method 2 · The V in motion', 'Method 2 · The V method')]),
    'wp28-p16': (28, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
    'geo30-advanced-p09': (30, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo31-g011': (31, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo32-advanced-p05': (32, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo32-advanced-p13': (32, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo32-g048': (32, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo33-advanced-p07': (33, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo33-advanced-p15': (33, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo33-foundation-p04': (33, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'q-r26-t33-10': (33, [('Shortcut · Pick values that fit', 'Shortcut · Plugging in numbers')]),
    'geo37-core-p13': (37, [('Method 2 · Pick values that fit', 'Method 2 · Plugging in numbers')]),
}

for _t, _m in MAP.values():
    for _n in _m.values(): assert _n in VOCAB or _n.startswith('= '), _n


# 2026-10-15: the old -> new method labels (slide titles and geometry sidebars) of the reading-script videos, so code
# that matches slides by title (added_content.same_slide_title -> added_notes.json, METHODS) still finds the old
# entries. Visual only: the spoken text of recorded videos was not changed.
SPEC_RENAMES_20261015 = {
    'algebraic-understanding': {'Plug in numbers': 'Plugging in numbers', 'Test the answers': 'Plugging in the answers', 'Algebra and understanding': 'The math way and understanding'},
    'r26-t13-summary': {'Plug in': 'Plugging in numbers'},
    'solve-geo30-g005': {'Method 1 · One pair at a time': 'Method 1 · The math way', 'Method 2 · The last digit': 'Method 2 · Understanding: last digit'},
    'solve-geo30-g006': {'Method 1 · An anchor: 180': 'Method 1 · The math way', 'Method 3 · Overlapping angles': 'Method 3 · Insight'},
    'solve-geo30-g007': {'Method 1 · A line through the bend': 'Method 1 · The math way: a helper line', 'Method 2 · The zig-zag rule': 'Method 2 · Understanding: the zig-zag rule'},
    'solve-geo31-g011': {'Method 1 · The angle rules': 'Method 1 · The math way', 'Method 2 · Plugging in a number': 'Method 2 · Plugging in numbers'},
    'solve-geo31-g017': {'Method 1 · Letters': 'Method 1 · The math way', 'Method 2 · Equal small triangles': 'Method 2 · Insight'},
    'solve-geo31-g018': {'Method 1 · Big minus small': 'Method 1 · The math way: subtract areas', 'Method 2 · A quicker ratio': 'Method 2 · Understanding: a ratio'},
    'solve-geo31-g020': {'Method 1 · Rule out, then the theorem': 'Rule out, then the theorem'},
    'solve-geo31-g027': {'Method 1 · The side ratio': 'Method 1 · The math way: the side ratio', 'Method 2 · Check with Pythagoras': 'Method 2 · The math way: Pythagoras'},
    'solve-geo31-g028': {'Method 1 · The side ratio': 'Method 1 · The math way: the side ratio', 'Method 2 · An equation': 'Method 2 · The math way: Pythagoras'},
    'solve-geo31-g031': {'Method 1 · The angle sum': 'Method 1 · The math way: the angle sum', 'Method 2 · An exterior angle': 'Method 2 · The math way: an exterior angle', 'Method 3 · Plugging in a number': 'Method 3 · Plugging in numbers'},
    'solve-geo31-g037': {'Method 1 · Subtract areas': 'Method 1 · The math way: subtract areas', 'Method 2 · Two triangles': 'Method 2 · Insight'},
    'solve-geo31-g038': {'Method 1 · Algebra': 'Method 1 · The math way', 'Method 2 · Area ratio': 'Method 2 · Insight: area ratio'},
    'solve-geo31-g039': {'Method 1 · Every side': 'Method 1 · The math way', 'Method 2 · Shared sides cancel': 'Method 2 · Insight', 'Method 3 · A quick check': 'Method 3 · Estimation'},
    'solve-geo31-g040': {'Method 1 · Algebra': 'Method 1 · The math way', 'Method 2 · Testing the answers': 'Method 2 · Plugging in the answers'},
    'solve-geo32-g044': {'Method 1 · The diagonals': 'Method 1 · The math way: the diagonals', 'Method 2 · Through the side': 'Method 2 · The math way: through the side'},
    'solve-geo32-g048': {'Adjacent angles': 'Method 1 · The math way'},
    'solve-geo32-g055': {'Method 1 · Symmetry': 'Method 1 · Understanding: symmetry', 'Method 2 · The area formula': 'Method 2 · The math way: the area formula'},
    'solve-geo32-g059': {'Method 1 · The median': 'Method 1 · Understanding: the median', 'Method 2 · Four equal triangles': 'Method 2 · Understanding: four equal triangles', 'Method 3 · Base times height': 'Method 3 · The math way: base times height'},
    'solve-geo32-g060': {'Method 1 · The diagonals': 'Method 1 · The math way: the diagonals', 'Method 2 · Two equilateral triangles': 'Method 2 · Insight'},
    'solve-geo32-g067': {'Method 1 · Algebra': 'Method 1 · The math way', 'Method 2 · Symmetry': 'Method 2 · Understanding: symmetry'},
    'solve-geo32-g069': {'Method 1 · The full math': 'Method 1 · The math way', 'Method 2 · A ratio': 'Method 2 · Understanding: a ratio'},
    'solve-geo32-g070': {'Method 1 · Subtracting areas': 'Method 1 · The math way: subtract areas', 'Method 2 · Completions': 'Method 2 · Understanding: completions', 'Method 3 · Symmetry': 'Method 3 · Understanding: symmetry'},
    'solve-geo32-g071': {'Method 1 · Algebra': 'Method 1 · The math way'},
    'solve-geo32-g072': {'Method 1 · The hidden ratio': 'Method 1 · The math way', 'Method 2 · Parts of the perimeter': 'Method 2 · Understanding'},
    'solve-geo33-g076': {'Method 1 · Inscribed quadrilateral': 'Method 1 · The math way', 'Method 2 · The big central angle': 'Method 2 · The math way: the big central angle', 'One more route · Radii': 'Method 3 · The math way: radii'},
    'solve-geo33-g078': {'Method 1 · Radii and 360°': 'Method 1 · The math way', 'Method 2 · Symmetry': 'Method 2 · Understanding: symmetry'},
    'solve-geo33-g080': {'Method 2 · Area over circumference': 'Method 2 · Understanding'},
    'solve-geo33-g086': {'Method 2 · Symmetry': 'Method 2 · Understanding: symmetry'},
    'solve-geo33-g094': {'Triangle minus sector': 'Method 1 · The math way: subtract areas', 'Stop and look at the choices': 'Method 2 · The math way: partial calculation', 'Estimating sizes': 'Method 3 · Estimation'},
    'solve-geo33-g096': {'Method 1 · Algebra': 'Method 1 · The math way', 'Method 2 · Plugging in': 'Method 2 · Plugging in numbers', 'Method 3 · Estimating sizes': 'Method 3 · Estimation'},
    'solve-geo33-g097': {'Method 1 · Plugging in': 'Method 1 · Plugging in numbers', 'Method 2 · Symmetry': 'Method 2 · Understanding: symmetry'},
    'solve-geo33-g099': {'Method 1 · Pieces we know': 'Method 1 · The math way', 'Method 2 · Take away the overlap': 'Method 2 · The math way: subtract the overlap', 'Estimating': 'Method 3 · Estimation'},
    'solve-geo33-g100': {'Method 1 · An equation': 'Method 1 · The math way', 'Method 2 · A size check': 'Method 2 · Estimation'},
    'solve-geo33-g101': {'Method 1 · An equation': 'Method 1 · The math way'},
    'solve-geo33-g102': {'Method 1 · The full math': 'Method 1 · The math way'},
    'solve-pt-q02': {'Method 1 · An equation': 'Method 1 · The math way'},
    'solve-pt-q03': {'Method 1 · Algebra': 'Method 1 · The math way'},
    'solve-pt-q04': {'Method 1 · The formula': 'Method 1 · The math way'},
    'solve-pt-q05': {'Method 1 · A table of cases': 'Method 1 · The math way: a table', 'Method 2 · An insight': 'Method 2 · Insight'},
    'solve-pt-q10': {'Method 1 · Plugging in a number': 'Method 1 · Plugging in numbers', 'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-pt-q11': {'Plugging in a number': 'Method 1 · Plugging in numbers', 'With letters': 'Method 2 · The math way'},
    'solve-pt-q12': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-pt-q13': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-pt-q14': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-pt-q16': {'Estimation': 'Method 1 · Estimation', 'Partial calculation': 'Method 2 · The math way: partial calculation'},
    'solve-pt-q17': {'Method 1 · The partner': 'Method 1 · The math way'},
    'solve-pt-q24': {'Method 1 · Picking values': 'Method 1 · Plugging in numbers', 'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-q-358': {'Method 1 · Understanding': 'Method 1 · Understanding', 'Method 2 · Plugging in numbers': 'Method 2 · Plugging in numbers'},
    'solve-q-359': {'Method 1 · Two cases': 'Method 1 · The math way: two cases', 'Method 2 · Number line': 'Method 2 · The math way: number line'},
    'solve-q-360': {'Method 1 · Inside the limits': 'Method 1 · The math way', 'Method 2 · Number line': 'Method 2 · The math way: number line'},
    'solve-q-361': {'Method 1 · Outside the limits': 'Method 1 · The math way', 'Method 2 · Number line': 'Method 2 · The math way: number line'},
    'solve-q-362': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-q-364': {'Method 1 · Number line': 'Method 1 · Understanding: number line'},
    'solve-q-366': {'Method 1 · The rules': 'Method 1 · The math way'},
    'solve-q-367': {'Method 1 · Algebra': 'Method 1 · The math way', 'Method 2 · Algebra, then the answers': 'Method 2 · Plugging in the answers: halfway', 'Method 3 · Plugging in the answers': 'Method 3 · Plugging in the answers'},
    'solve-q-368': {'Method 1 · Two cases': 'Method 1 · The math way: two cases', 'Method 2 · Square both sides': 'Method 2 · The math way: square both sides'},
    'solve-q-369': {'Method 1 · Two bands': 'Method 1 · The math way: number line', 'Method 2 · Split it': 'Method 2 · The math way: two inequalities'},
    'solve-q-370': {'Method 1 · Two cases': 'Method 1 · The math way: two cases'},
    'solve-q-387': {'Method 1 · Trial and error': 'Method 1 · Plugging in numbers'},
    'solve-q-388': {'Method 1 · Break into primes': 'Method 1 · The math way: prime factors', 'Method 2 · Divide the number': 'Method 2 · The math way: calculate'},
    'solve-q-389': {'Method 1 · Common factor': 'Method 1 · The math way: prime factors', 'Method 2 · Which choices divide both': 'Method 2 · Plugging in the answers'},
    'solve-q-390': {'Method 1 · Primes': 'Method 1 · The math way: prime factors', 'Method 2 · The smallest number': 'Method 2 · Plugging in numbers', 'Method 3 · Product over GCD': 'Method 3 · The math way: a formula'},
    'solve-q-392': {'Method 1 · Prime factorization': 'Method 1 · The math way: prime factors'},
    'solve-q-393': {'Method 1 · Common factor, then pairs': 'Method 1 · The math way: common factor', 'Method 2 · Check the sum 17': 'Method 2 · Plugging in the answers'},
    'solve-q-395': {'Method 1 · Test each statement': 'Method 1 · Understanding'},
    'solve-q-396': {'Method 1 · Build the smallest': 'Method 1 · Understanding'},
    'solve-q-397': {'Method 1 · The rule': 'Method 1 · Understanding', 'Method 2 · Trial and error': 'Method 2 · Plugging in numbers'},
    'solve-q-398': {'Method 1 · Break into primes': 'Method 1 · The math way: prime factors', 'Method 2 · Even and odd': 'Method 2 · Understanding'},
    'solve-q-399': {'Method 1 · Every pair': 'Method 1 · The math way: listing', 'Method 2 · The extremes': 'Method 2 · Understanding: the extremes'},
    'solve-q-400': {'Method 1 · Build every product': 'Method 1 · The math way: listing', 'Method 2 · Look at the choices': 'Method 2 · Estimation'},
    'solve-q-402': {'Method 1 · Divisor pairs': 'Method 1 · The math way: divisor pairs', 'Method 2 · Plugging in a number': 'Method 2 · Plugging in numbers'},
    'solve-q-423': {'Method 1 · Step by step': 'Method 1 · The math way', 'Method 2 · Build from the inside': 'Method 2 · The math way: one letter'},
    'solve-q-424': {'Method 1 · Test the choices': 'Method 1 · Plugging in the answers', 'Method 2 · List the numbers': 'Method 2 · The math way: listing'},
    'solve-q-425': {'Method 1 · The biggest remainder': 'Method 1 · Understanding', 'Method 2 · List the remainders': 'Method 2 · Plugging in numbers'},
    'solve-q-426': {'Method 1 · Split off the fives': 'Method 1 · The math way: tag it', 'Method 2 · Plugging in a number': 'Method 2 · Plugging in numbers'},
    'solve-q-428': {'Method 1 · Divisible by 3 first': 'Method 1 · The math way: divisibility rules', 'Method 2 · Even first': 'Method 2 · The math way: the other order'},
    'solve-q-430': {'Method 1 · Count them': 'Method 1 · The math way: count', 'Method 2 · Compare without counting': 'Method 2 · Understanding'},
    'solve-q-431': {'Method 1 · One letter': 'Method 1 · The math way: one letter'},
    'solve-q-432': {'Method 1 · Three in a row': 'Method 1 · The math way: three in a row', 'Method 2 · Plugging in a number': 'Method 2 · Plugging in numbers'},
    'solve-q-433': {'Method 1 · The last digit': 'Method 1 · Understanding: last digit', 'Method 2 · Test the choices': 'Method 2 · Plugging in the answers'},
    'solve-q-434': {'Method 1 · What is left': 'Method 1 · The math way', 'Method 2 · What she paid': 'Method 2 · Plugging in the answers'},
    'solve-q-435': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-q-457': {'Method 1 · Positive pieces first': 'Method 1 · Understanding'},
    'solve-q-458': {'Method 1 · One letter': 'Method 1 · The math way: one letter'},
    'solve-q-459': {'Method 2 · The differences': 'Method 2 · The math way'},
    'solve-q-460': {'Method 1 · Drop the powers': 'Method 1 · Understanding', 'Method 2 · Plugging in both cases': 'Method 2 · Plugging in numbers'},
    'solve-q-461': {'Method 1 · Cancel first': 'Method 1 · The math way', 'Method 2 · Plugging in three times': 'Method 2 · Plugging in numbers'},
    'solve-q-462': {'Method 1 · Same parity': 'Method 1 · Understanding'},
    'solve-q-463': {'Method 1 · Plugging in three times': 'Method 1 · Plugging in numbers', 'Method 2 · The shortcut formula': 'Method 2 · The math way: shortcut formula'},
    'solve-q-464': {'Method 1 · Plugging in': 'Method 1 · Plugging in numbers', 'Method 2 · Three in a row': 'Method 2 · The math way: three in a row'},
    'solve-q-465': {'Method 1 · Read the signs': 'Method 1 · Understanding'},
    'solve-q-466': {'Method 1 · Read the signs': 'Method 1 · Understanding', 'Method 2 · Simplify first': 'Method 2 · The math way'},
    'solve-q-467': {'Method 1 · Start smart': 'Method 1 · Understanding', 'Method 2 · Knock out the others': 'Method 2 · Plugging in numbers'},
    'solve-q-468': {'Method 1 · The shortcut formula': 'Method 1 · The math way: shortcut formula'},
    'solve-q-469': {'Method 1 · One letter': 'Method 1 · The math way: one letter'},
    'solve-q-470': {'Method 1 · Different parities': 'Method 1 · Understanding: even and odd', 'Method 2 · Drop the powers': 'Method 2 · Understanding: drop the powers'},
    'solve-q-471': {'Method 1 · An odd product': 'Method 1 · Understanding'},
    'solve-q-472': {'Method 1 · Count the twos': 'Method 1 · Understanding: count the twos', 'Method 2 · Plugging in the smallest': 'Method 2 · Plugging in numbers'},
    'solve-q-493': {'Method 1 · Strong on strong': 'Method 1 · Understanding: strong on strong'},
    'solve-q-496': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-q-498': {'Method 1 · The arrows': 'Method 1 · The math way: the arrows'},
    'solve-q-499': {'Method 1 · The arrows': 'Method 1 · The math way: the arrows', 'Method 3 · A sharp shortcut': 'Method 3 · Understanding'},
    'solve-q-500': {'Method 2 · Plugging in a clean-root number': 'Method 2 · Plugging in numbers'},
    'solve-q-514': {'Method 2 · The algebraic form': 'Method 2 · The math way: place values'},
    'solve-q-517': {'Method 1 · The size first': 'Method 1 · Estimation', 'Method 2 · Start from the choices': 'Method 2 · Plugging in the answers'},
    'solve-q-519': {'Plugging in the choices': 'Plugging in the answers'},
    'solve-q-520': {'Method 1 · The algebraic form': 'Method 1 · The math way: place values', 'Method 2 · Testing the answers': 'Method 2 · Plugging in the answers'},
    'solve-q-541': {'Method 1 · Substitute': 'Method 1 · The math way', 'Method 2 · A common factor': 'Method 2 · The math way: common factor'},
    'solve-q-542': {'Method 1 · Inside out': 'Method 1 · The math way: inside out', 'Method 2 · The rule itself': 'Method 2 · Understanding'},
    'solve-q-544': {'Method 1 · Match the input': 'Method 1 · The math way', 'Method 2 · Rewrite the rule': 'Method 2 · Understanding'},
    'solve-q-546': {'Method 1 · Down, then back up': 'Method 1 · The math way', 'Method 2 · The pattern': 'Method 2 · Understanding: the pattern'},
    'solve-q-549': {'Method 1 · Algebra': 'Method 1 · The math way', 'Method 2 · Plugging in a number': 'Method 2 · Plugging in numbers'},
    'solve-q-550': {'Method 1 · The standard way': 'Method 1 · The math way', 'Method 2 · The outer diamond first': 'Method 2 · Understanding'},
    'solve-q-551': {'Method 1 · The standard way': 'Method 1 · The math way', 'Method 2 · The shortcut formulas': 'Method 2 · Understanding: shortcut formulas'},
    'solve-q-552': {'Method 1 · The full math': 'Method 1 · The math way', 'Method 2 · Plugging in a number': 'Method 2 · Plugging in numbers'},
    'solve-q-553': {'Method 1 · The full math': 'Method 1 · The math way', 'Method 2 · Read the definition first': 'Method 2 · Understanding'},
    'solve-q-554': {'Method 1 · The standard way': 'Method 1 · The math way', 'Method 2 · Think about the powers': 'Method 2 · Understanding'},
    'solve-q-555': {'Method 1 · Algebra': 'Method 1 · The math way', 'Method 2 · By understanding': 'Method 2 · Understanding'},
    'solve-q-577': {'Method 1 · The biggest value': 'Method 1 · Understanding: the extremes', 'Method 2 · Numbers for the biggest sum': 'Method 2 · Plugging in numbers', 'Method 3 · Testing the answers': 'Method 3 · Plugging in the answers'},
    'solve-q-578': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-q-579': {'Method 1 · Whole numbers': 'Method 1 · Plugging in numbers', 'Method 2 · A right triangle': 'Method 2 · Insight'},
    'solve-q-r26-t13-01': {'Method 1 · Two cases': 'Method 1 · The math way: two cases'},
    'solve-q-r26-t13-02': {'Method 1 · Look at the right side': 'Method 1 · Understanding'},
    'solve-q-r26-t13-03': {'Method 1 · Two cases and a check': 'Method 1 · The math way: two cases'},
    'solve-q-r26-t14-01': {'Method 1 · Test up to the root': 'Method 1 · The math way', 'Method 2 · Count by sevens': 'Method 2 · Understanding'},
    'solve-q-r26-t14-03': {'Method 1 · Break and match': 'Method 1 · The math way: prime factors', 'Method 2 · Divide down': 'Method 2 · The math way: calculate'},
    'solve-q-r26-t15-01': {'Method 1 · Tag it': 'Method 1 · The math way: tag it'},
    'solve-q-r26-t15-15': {'Method 1 · Tag it': 'Method 1 · The math way: tag it'},
    'solve-q-r26-t16-01': {'Method 1 · The bigger size wins': 'Method 1 · Understanding'},
    'solve-q-r26-t16-02': {'Method 1 · Count times middle': 'Method 1 · Understanding: the middle', 'Method 2 · One letter': 'Method 2 · The math way: one letter'},
    'solve-q-r26-t16-03': {'Method 1 · One letter': 'Method 1 · The math way: one letter'},
    'solve-q-r26-t16-04': {'Method 1 · Smallest case, then a second case': 'Method 1 · Plugging in numbers', 'Method 2 · Why 3': 'Method 2 · Understanding'},
    'solve-q-r26-t17-01': {'Method 1 · Ranges first': 'Method 1 · Understanding'},
    'solve-q-r26-t17-02': {'Method 1 · The arrows': 'Method 1 · The math way: the arrows', 'Method 2 · Plugging in a number': 'Method 2 · Plugging in numbers'},
    'solve-q-r26-t17-03': {'Method 1 · Reciprocals': 'Method 1 · The math way: reciprocals', 'Method 2 · Plugging in the ends': 'Method 2 · Plugging in numbers'},
    'solve-q-r26-t17-04': {'Method 2 · Plugging in at the edges': 'Method 2 · Plugging in numbers'},
    'solve-q-r26-t17-05': {'Method 1 · The distance': 'Method 1 · The math way'},
    'solve-q-r26-t18-01': {'Method 1 · The columns': 'Method 1 · The math way: columns', 'Method 2 · The algebraic form': 'Method 2 · The math way: place values'},
    'solve-q-r26-t18-02': {'Trying numbers': 'Method 2 · Plugging in numbers'},
    'solve-q-r26-t19-01': {'Method 1 · Algebra': 'Method 1 · The math way'},
    'solve-q-r26-t19-02': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-q-r26-t19-03': {'Method 1 · Two cases': 'Method 1 · The math way: two cases'},
    'solve-q-r26-t19-05': {'Method 1 · Calculate both': 'Method 1 · The math way', 'Method 2 · Even powers cancel': 'Method 2 · Understanding'},
    'solve-q-r26-t20-01': {'Method 2 · Algebra': 'Method 2 · The math way'},
    'solve-q-r26-t20-02': {'Method 1 · One number': 'Method 1 · Plugging in numbers', 'Method 2 · Place the choices': 'Method 2 · Understanding'},
    'solve-q-r26-t20-03': {'Method 1 · Steps of two': 'Method 1 · The math way', 'Method 2 · Half of all': 'Method 2 · Understanding'},
    'solve-q-r26-t30-03': {'Method 1 · The zig-zag rule': 'Method 1 · Understanding: the zig-zag rule', 'Method 2 · A line through each bend': 'Method 2 · The math way: helper lines'},
    'solve-q-r26-t32-07': {'Method 1 · A shortcut formula': 'Method 1 · The math way: shortcut formula', 'Method 2 · A triple': 'Method 2 · Understanding: a triple'},
    'solve-q-r26-t33-02': {'Method 1 · Tangent pieces': 'Method 1 · The math way', 'Method 2 · The shortcut': 'Method 2 · The math way: a short formula'},
    'solve-q-r26-t33-03': {'Method 2 · Easy numbers': 'Method 2 · Plugging in numbers'},
}


def spec_new_title(vid, title):
    """the 2026-10-15 vocabulary name of an old method title (or the title itself)"""
    return SPEC_RENAMES_20261015.get(vid, {}).get(title, title)
