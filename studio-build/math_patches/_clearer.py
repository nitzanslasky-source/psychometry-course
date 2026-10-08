"""Helpers for "2026-10-08 clearer scripts" (teacher, while recording topic 13: "Make the script of the slides of what
I'm doing now and the next topic a bit more informative. Sometimes I feel stuck and reading what you wrote isn't
enough to understand.").

Spoken lines only: before a step say WHAT and WHY, after a calculation say what it MEANS, name the rule, say why a
choice is out, define a new term once, fill a big jump. Board items, numbers, methods and the pen/click split stay.

Not a patch itself (math_api only loads t*.py); tNN.py load it with importlib, like _hebrew_back.py:

    CL.recorded(vid)                       -> True if ANY take of vid was recorded before CUTOFF (never touched then)
    CL.edit(M, vid, title, ops)            -> apply ops to the spoken lines of the slide with that title; False if recorded
        ops = [('after', anchor, [str, ...]), ('before', anchor, [str, ...]), ('replace', anchor, str | [str, ...]),
               ('end', None, [str, ...])]
        anchor: a substring of exactly one line of the slide (spoken text, drawn text or the label of an appearing
        item). 'replace' only replaces a SPOKEN line. New entries are spoken lines (strings) only.
    CL.ADDED[(vid, title)] = number of NEW lines added on that slide (for the studio notes)
"""
import glob as _glob, os as _os, re as _re

# UTC; a take recorded before this keeps the video as recorded (nothing changed in it). Set to the time this change
# was finished: a take recorded later was made with the clearer lines, so they must stay.
CUTOFF = '2026-10-08T14-16-00'

ADDED = {}


def recorded(vid):
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


def _txt(l):
    return l.get('say') or l.get('draw') or l.get('label') or ''


def edit(M, vid, title, ops):
    if recorded(vid): return False
    beats = M.video(vid)['beats']
    ns = [i for i, b in enumerate(beats) if b['title'] == title or (b.get('mode') == 'title' and b.get('bigTitle') == title)]
    assert len(ns) == 1, ('clearer: slide', vid, title, ns)
    b = beats[ns[0]]
    lines = list(b['lines']); added = 0
    for op, anchor, new in ops:
        if op == 'end':
            lines += [{'say': x} for x in new]; added += len(new); continue
        ks = [i for i, l in enumerate(lines) if anchor in _txt(l)]
        assert len(ks) == 1, ('clearer: anchor', vid, title, anchor, ks)
        k = ks[0]
        if op == 'replace':
            assert 'say' in lines[k], ('clearer: replace a spoken line only', vid, title, anchor)
            new = new if isinstance(new, list) else [new]
            assert all(isinstance(x, str) for x in new)
            lines[k:k + 1] = [{'say': x} for x in new]; added += len(new) - 1
        else:
            assert all(isinstance(x, str) for x in new)
            at = k + 1 if op == 'after' else k
            lines[at:at] = [{'say': x} for x in new]; added += len(new)
    b['lines'] = lines
    M.touched_videos.add(vid)
    if added > 0: ADDED[(vid, title)] = ADDED.get((vid, title), 0) + added
    return True
