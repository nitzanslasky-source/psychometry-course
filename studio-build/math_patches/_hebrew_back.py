"""Helpers for "2026-10-08 Hebrew points restored".

The 2026-10-05 "cut repeats" pass shortened lessons on the assumption that the question videos right after teach the
same ideas. Often they only ANSWERED the questions: the teacher's Hebrew lesson explanation (the WHY, rules, analogies,
warnings, exam-frequency remarks) was lost. Rule (teacher): cut REPEATS, never CONTENT. Each tNN.py that lost a point
has a function hebrew_points_back(M), called LAST in its apply(), that puts the point back as 1-4 short spoken lines
(+ a board item if needed) into an UNRECORDED video - or, for a video already recorded, into the written explanation
of the related question.

Not a patch itself (math_api only loads t*.py); tNN.py load it with importlib, like _trim_repeats.py:

    import importlib.util as _ilu, os as _os
    _s = _ilu.spec_from_file_location('_hebrew_back', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_hebrew_back.py'))
    HB = _ilu.module_from_spec(_s); _s.loader.exec_module(HB)

    HB.recorded(vid)                             -> True if a take of vid was recorded before CUTOFF and vid is not in
                                                 _rerecord.RERECORD (then: don't touch). HB.was_recorded(vid) ignores RERECORD.
    HB.append_slides(M, vid, [slide, ...])       option 2: new slides at the END of a video (slide = dict(title=, mode='concept',
                                                 active=, pre=[], script=[...]); vid must be in RERECORD if recorded)
    HB.add_lines(M, vid, title, anchor, new, where='after')
        insert script entries `new` (str / A(label, T(...)) / D(...)) after/before the line whose text contains
        `anchor` (None = at the end of the slide) on the slide with that title. Returns False (and changes nothing)
        if the video was recorded.
    HB.add_expl(M, qid, text, before=None)       add one paragraph to a question's written solution (end, or before
                                                 the paragraph containing `before`)
    + everything from _trim_repeats (n_of, lines_of, set_slide, replace_line, drop_lines ...)
"""
import glob as _glob, os as _os, re as _re
import importlib.util as _ilu

_s = _ilu.spec_from_file_location('_trim_repeats_hb', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_trim_repeats.py'))
_TR = _ilu.module_from_spec(_s); _s.loader.exec_module(_TR)
n_of, lines_of, set_slide, replace_line, drop_lines = _TR.n_of, _TR.lines_of, _TR.set_slide, _TR.replace_line, _TR.drop_lines

# UTC; a take recorded before this keeps the video as recorded (nothing added to it). Set to the time this change was
# finished: a take recorded later was made with the restored lines, so they must stay.
CUTOFF = '2026-10-08T07-26-24'


_s2 = _ilu.spec_from_file_location('_rerecord_hb', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_rerecord.py'))
_RR = _ilu.module_from_spec(_s2); _s2.loader.exec_module(_RR)
RERECORD = _RR.RERECORD


def recorded(vid):
    """True = a take exists before CUTOFF and the video is NOT in _rerecord.RERECORD (= leave it as recorded)."""
    if vid in RERECORD: return False
    return was_recorded(vid)


def was_recorded(vid):
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


def _text(x):
    return _TR._text(x)


def add_lines(M, vid, title, anchor, new, where='after'):
    if recorded(vid): return False
    sc = lines_of(M, vid, title)
    if anchor is None:
        out = sc + list(new)
    else:
        ks = [i for i, x in enumerate(sc) if anchor in _text(x)]
        assert len(ks) == 1, ('add_lines', vid, title, anchor, ks)
        k = ks[0]
        out = sc[:k + 1] + list(new) + sc[k + 1:] if where == 'after' else sc[:k] + list(new) + sc[k:]
    set_slide(M, vid, title, out)
    return True


def add_expl(M, qid, text, before=None):
    ex = list(M.q(qid).get('explanation') or [])
    if before is None: ex.append(text)
    else:
        ks = [i for i, e in enumerate(ex) if before in e]
        assert len(ks) == 1, ('add_expl', qid, before, ks)
        ex.insert(ks[0], text)
    M.set_q(qid, expl=ex)


def append_slides(M, vid, slides):
    assert not recorded(vid), ('append_slides: recorded and not in RERECORD', vid)
    M.insert_slides(vid, len(M.video(vid)['beats']), slides)
