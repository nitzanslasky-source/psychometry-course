"""AI redo of recorded math videos (teacher decision 2026-10-10/11).

Math only (topics 1-38, 51, 52): the teacher re-records only the FIRST teaching lesson of each topic, on camera. ALL other
math videos are redone with AI narration (her cloned voice), INCLUDING the ones she already recorded. So the old rule
"a recorded video keeps its old version" no longer holds for those: they get the NEWEST content.

    KEEP     = the first lessons that stay exactly as recorded (on camera; every time-gated guard still protects them).
               Checked 2026-10-11: these are the first lesson videos of topics 1-10 and 12 in course flow order.
    AI_REDO  = every OTHER recorded math video (178 ids, every take in ~/Documents/Course.recordings on 2026-10-11).
    CAMERA   = the AI_REDO ids that are first lessons the teacher re-records ON CAMERA with the new content (absolute-value
               t13, primes t14) or that go to a re-record (advanced-powers t11 - teacher: "AI or a re-record"; shown in
               the studio as a re-record until she decides). They get the new content like every AI_REDO video.

HOW (one central place): a take of an AI_REDO video recorded BEFORE CUTOFF is obsolete - every "was it recorded before
<cutoff>" check ignores it, so the video counts as UNRECORDED and gets every newer change. A take recorded after CUTOFF
counts again as usual (so a new on-camera take of absolute-value / primes is protected by later passes).
  - The recording guards of the math patches (_choice_order, _spoken_labels, _method_names, _clearer, _trim_repeats,
    _hebrew_back, _cov_fix_a, _shaded_nl and the per-topic _nd_recorded / _sp_recorded / _ht_recorded / _rs_recorded /
    _cf_recorded / _ai_recorded in tNN.py) all list the recordings folder with glob.glob('~/Documents/Course.recordings/
    **/*'). install() (called by math_api.apply_patches before any patch loads) wraps glob.glob / glob.iglob so that
    listing leaves out the obsolete takes. Nothing else is filtered (other paths pass through unchanged).
  - studio_done.takes() leaves them out too (stem_lines, studio_arrows CUTOFF, the build checks of _choice_order /
    _spoken_labels, the studio's green "recorded" ids). studio_done.takes(all=True) still lists every file.
  - Hand-written exemptions that named recorded ids (t03 new_numbers RECORDED = q-091..q-094) consult AI_REDO.
  - Re-record list (_rerecord.py): option-2 entries ("continue from the old last slide": solve-q-195, solve-q-326,
    solve-q-328) are treated as whole new videos - their recorded part also gets every newer change.
The recording FILES are never deleted or moved.

Not a patch itself (math_api only loads t*.py). Load with importlib (see math_api.apply_patches / studio_done).
"""
import fnmatch as _fn, glob as _glob, os as _os, re as _re

# UTC (take-file format, compared on 'YYYY-MM-DDTHH-MM-SS'): a take of an AI_REDO video recorded before this is obsolete.
# Set to the time this change was finished: a take recorded later was made with the newest content.
CUTOFF = '2026-10-10T23-30-00'

KEEP = frozenset({
    'numbers',              # t1  The Language of Algebra
    'fraction-basics',      # t2  What Is a Fraction?
    'compare-fractions',    # t3  Comparing Fractions
    'expression-basics',    # t4  Expressions - Fundamentals
    'expression-strategy',  # t5  Working with Expressions
    'linear-equations',     # t6  Equations - Fundamentals
    'equation-strategy',    # t7  Solving Equations Smarter
    'exponents',            # t8  Exponent Laws
    'roots',                # t9  Roots - Fundamentals
    'powers-techniques',    # t10 Exponents & Roots - Techniques
    'inequalities',         # t12 Inequalities
})

CAMERA = frozenset({'absolute-value', 'primes', 'advanced-powers'})   # first lessons of t13, t14, t11: new content, re-record

AI_REDO = frozenset({
    'absolute-value', 'add-subtract', 'advanced-powers', 'decimals', 'fraction-add', 'fraction-multiply',
    'inequality-systems', 'multiply-divide', 'order-of-operations', 'primes', 'r26-t01-exam-words',
    'r26-t01-must-could', 'r26-t02-shortcuts', 'r26-t03-summary', 'r26-t04-formulas', 'r26-t05-shortcuts',
    'r26-t07-quadratic', 'r26-t08-traps', 'r26-t09-traps', 'r26-t10-power-traps', 'r26-t12-combining', 'r26-t12-signs',
    'r26-t13-tools',
    'solve-q-091', 'solve-q-092', 'solve-q-093', 'solve-q-094', 'solve-q-095', 'solve-q-096', 'solve-q-097',
    'solve-q-098', 'solve-q-099', 'solve-q-120', 'solve-q-121', 'solve-q-125', 'solve-q-126', 'solve-q-127',
    'solve-q-128', 'solve-q-129', 'solve-q-130', 'solve-q-131', 'solve-q-132', 'solve-q-133', 'solve-q-134',
    'solve-q-135', 'solve-q-136', 'solve-q-137', 'solve-q-138', 'solve-q-164', 'solve-q-165', 'solve-q-171',
    'solve-q-178', 'solve-q-179', 'solve-q-180', 'solve-q-181', 'solve-q-182', 'solve-q-183', 'solve-q-184',
    'solve-q-185', 'solve-q-186', 'solve-q-187', 'solve-q-188', 'solve-q-189', 'solve-q-190', 'solve-q-191',
    'solve-q-192', 'solve-q-193', 'solve-q-194', 'solve-q-195', 'solve-q-196', 'solve-q-197', 'solve-q-224',
    'solve-q-226', 'solve-q-231', 'solve-q-248', 'solve-q-249', 'solve-q-250', 'solve-q-251', 'solve-q-252',
    'solve-q-288', 'solve-q-289', 'solve-q-290', 'solve-q-291', 'solve-q-292', 'solve-q-293', 'solve-q-294',
    'solve-q-295', 'solve-q-296', 'solve-q-297', 'solve-q-299', 'solve-q-300', 'solve-q-301', 'solve-q-322',
    'solve-q-323', 'solve-q-324', 'solve-q-325', 'solve-q-326', 'solve-q-327', 'solve-q-328', 'solve-q-329',
    'solve-q-330', 'solve-q-331', 'solve-q-332', 'solve-q-333', 'solve-q-334', 'solve-q-335', 'solve-q-336',
    'solve-q-337', 'solve-q-358', 'solve-q-359', 'solve-q-360', 'solve-q-361', 'solve-q-362', 'solve-q-363',
    'solve-q-364', 'solve-q-365', 'solve-q-366', 'solve-q-367', 'solve-q-368', 'solve-q-369', 'solve-q-370',
    'solve-q-386', 'solve-q-387', 'solve-q-388', 'solve-q-389', 'solve-q-390',
    'solve-q-r26-t01-01', 'solve-q-r26-t01-05', 'solve-q-r26-t01-06', 'solve-q-r26-t01-15', 'solve-q-r26-t02-01',
    'solve-q-r26-t02-05', 'solve-q-r26-t02-10', 'solve-q-r26-t02-15', 'solve-q-r26-t02-19', 'solve-q-r26-t03-01',
    'solve-q-r26-t03-02', 'solve-q-r26-t03-03', 'solve-q-r26-t04-01', 'solve-q-r26-t04-02', 'solve-q-r26-t04-03',
    'solve-q-r26-t04-04', 'solve-q-r26-t05-02', 'solve-q-r26-t05-03', 'solve-q-r26-t05-04', 'solve-q-r26-t06-01',
    'solve-q-r26-t06-02', 'solve-q-r26-t06-03', 'solve-q-r26-t06-04', 'solve-q-r26-t07-01', 'solve-q-r26-t07-02',
    'solve-q-r26-t07-05', 'solve-q-r26-t08-01', 'solve-q-r26-t08-02', 'solve-q-r26-t08-05', 'solve-q-r26-t09-01',
    'solve-q-r26-t09-02', 'solve-q-r26-t09-03', 'solve-q-r26-t09-04', 'solve-q-r26-t09-05', 'solve-q-r26-t09-06',
    'solve-q-r26-t10-01', 'solve-q-r26-t10-02', 'solve-q-r26-t10-03', 'solve-q-r26-t11-01', 'solve-q-r26-t11-02',
    'solve-q-r26-t11-13', 'solve-q-r26-t12-01', 'solve-q-r26-t12-02', 'solve-q-r26-t12-03', 'solve-q-r26-t12-04',
    'solve-q-r26-t12-13', 'solve-q-r26-t13-01', 'solve-q-r26-t13-02', 'solve-q-r26-t13-03', 'solve-q-r26-t13-13',
    'solve-q-r26-t14-01', 'systems',
})
assert not KEEP & AI_REDO and CAMERA <= AI_REDO and len(AI_REDO) == 178

ROOT = _os.path.expanduser('~/Documents/Course.recordings')
TAKE = _re.compile(r'^(.+)-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')


def obsolete(vid, ts):
    """True = this take (video id, time stamp in take-file format) no longer counts: AI_REDO video, recorded before CUTOFF."""
    return vid in AI_REDO and ts[:19] < CUTOFF


def obsolete_file(path):
    m = TAKE.match(_os.path.basename(str(path)))
    return bool(m) and obsolete(m.group(1), m.group(2))


def ai_redo(vid):
    """True = an AI redo video narrated by the AI voice (AI_REDO without the on-camera first lessons)."""
    return vid in AI_REDO and vid not in CAMERA


# ---- the central filter on "list the recordings folder" ------------------------------------------------------------
FILTERED = {}   # 'module:function' of the caller -> number of obsolete take files left out (build report)


def _caller():
    import sys
    f = sys._getframe(1)
    while f and _os.path.basename(f.f_code.co_filename) in ('_ai_redo.py', 'glob.py'): f = f.f_back
    if f is None: return '?'
    return '%s:%s' % (_os.path.basename(f.f_code.co_filename), f.f_code.co_name)


def _wrap(orig):
    def g(pathname, *a, **k):
        res = orig(pathname, *a, **k)
        if 'Course.recordings' not in str(pathname): return res
        out = [p for p in res if not obsolete_file(p)]
        if len(out) != len(res):
            c = _caller(); FILTERED[c] = FILTERED.get(c, 0) + len(res) - len(out)
        return out
    g._ai_redo = orig
    return g


def install():
    """Make glob.glob / glob.iglob leave out obsolete takes when they list the recordings folder (idempotent)."""
    if not getattr(_glob.glob, '_ai_redo', None):
        _glob.glob = _wrap(_glob.glob)
    if not getattr(_glob.iglob, '_ai_redo', None):
        o = _glob.iglob
        w = _wrap(lambda *a, **k: list(o(*a, **k)))
        def ig(*a, **k): return iter(w(*a, **k))
        ig._ai_redo = o
        _glob.iglob = ig


def check(takes):
    """takes = [(video id, ts)] of EVERY file. Warns about a math take recorded before CUTOFF that is neither KEEP nor
    AI_REDO (a video recorded after the list was made: decide which it is and add it)."""
    known = KEEP | AI_REDO
    return sorted({v for v, ts in takes if ts[:19] < CUTOFF and v not in known})
