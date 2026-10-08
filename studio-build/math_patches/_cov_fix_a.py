"""Helpers for "2026-10-08 coverage fixes" (topics 1-20).

A full check compared the teacher's Hebrew course with the English course (WEAK / MISSING points). Each touched tNN.py
has coverage_fixes(M), called LAST in its apply(), that puts the point back as a few short spoken lines (+ a board item
by click if needed) into an UNRECORDED video - or, for a video already recorded, into the written explanation / card.

Not a patch itself (math_api only loads t*.py); tNN.py load it with importlib:

    import importlib.util as _ilu_cf, os as _os_cf
    _s_cf = _ilu_cf.spec_from_file_location('_cov_fix_a', _os_cf.path.join(_os_cf.path.dirname(_os_cf.path.abspath(__file__)), '_cov_fix_a.py'))
    CF = _ilu_cf.module_from_spec(_s_cf); _s_cf.loader.exec_module(CF)

    CF.recorded(vid)                    True if a take of vid was recorded before CUTOFF (and vid not in _rerecord.RERECORD)
    CF.add_lines(M, vid, title, anchor, new, where='after')   as _hebrew_back.add_lines, with this CUTOFF
    CF.replace_line(M, vid, title, sub, new)                  replace one line (str / list); False if recorded
    CF.add_slide(M, vid, after_title, slide, label)           new slide after the slide `after_title` with its own
                                                             sidebar item `label` (False if recorded)
    CF.add_expl(M, qid, text, before=None)                    written solution paragraph
"""
import glob as _glob, os as _os, re as _re
import importlib.util as _ilu

_s = _ilu.spec_from_file_location('_hebrew_back_cf', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_hebrew_back.py'))
HB = _ilu.module_from_spec(_s); _s.loader.exec_module(HB)

# UTC; a take recorded before this keeps the video as recorded (nothing added). Set to the time this change was
# finished: a take recorded later was made with the added lines, so they must stay.
CUTOFF = '2026-10-08T08-43-34'

add_expl = HB.add_expl
lines_of, set_slide, n_of = HB.lines_of, HB.set_slide, HB.n_of


def recorded(vid):
    if vid in HB.RERECORD: return False
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


def add_lines(M, vid, title, anchor, new, where='after'):
    if recorded(vid): return False
    return HB.add_lines(M, vid, title, anchor, new, where)


def replace_line(M, vid, title, sub, new):
    if recorded(vid): return False
    set_slide(M, vid, title, HB.replace_line(lines_of(M, vid, title), sub, new))
    return True


def add_slide(M, vid, after_title, slide, label):
    """slide = dict(title=, mode=, pre=[], script=[...]); gets a new sidebar item `label` right after the item of
    `after_title`; later slides' active indexes move up by one."""
    if recorded(vid): return False
    v = M.video(vid); n = n_of(M, vid, after_title); a = v['beats'][n - 1]['active']
    sb = list(v['hybrid']['sidebar'])
    for b in v['beats']:
        if b.get('active', -1) > a: b['active'] += 1
    sb.insert(a + 1, label)
    M.set_sidebar(vid, sb)
    M.insert_slides(vid, n, [dict(slide, active=a + 1)])
    return True
