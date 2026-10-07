"""Helpers for "2026-10-07 trim added repeats" (teacher decision 2026-10-07: "My only concern is places where YOU
added it. Where the original (Hebrew) course teaches something in multiple subjects, that's OK.").

Content WE added (added_content.py manifest / r26 ids) that re-teaches something the student already learned earlier in
the study-plan order (src/lib/planData.ts) is trimmed: a pure repeat slide is removed, an added lesson that only repeats
shrinks to a one-line reminder, a partly new slide keeps only its new part. The teacher's own material is never cut.

Not a patch itself (math_api only loads t*.py); tNN.py load it with importlib, like _shaded_nl.py.

    recorded(vid)                    -> True if a take of vid was recorded before CUTOFF: the video stays as recorded
    n_of(M, vid, title)              -> 1-based number of the slide with that title (must be unique)
    drop_slide(M, vid, title)        -> remove the slide and its sidebar label (later slides' 'active' shift down)
    set_slide(M, vid, title, script, new_title=None, keep_pre=True)  -> rebuild one slide's script
    set_sidebar_label(M, vid, old, new)
    retitle(M, vid, title)           -> video title, nav label, studio title and the title slide's big title
"""
import glob as _glob, os as _os, re as _re

# UTC; takes recorded before this keep the old video. Set to the time this change was finished: a take recorded
# later was made with the trimmed slides, so the trim must stay.
CUTOFF = '2026-10-07T16-37-00'


def recorded(vid):
    pat = _re.compile(_re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in _glob.glob(_os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(_os.path.basename(f))
        if m and m.group(1) < CUTOFF: return True
    return False


def n_of(M, vid, title):
    ns = [i for i, b in enumerate(M.video(vid)['beats'], 1) if b['title'] == title]
    assert len(ns) == 1, (vid, title, ns)
    return ns[0]


def drop_slide(M, vid, title):
    n = n_of(M, vid, title)
    v = M.video(vid); b = v['beats'][n - 1]; a = b.get('active', -1)
    sb = list(v.get('hybrid', {}).get('sidebar') or [])
    shared = a >= 0 and any(x.get('active') == a for k, x in enumerate(v['beats']) if k != n - 1)
    M.remove_slides(vid, [n])
    if a >= 0 and not shared and a < len(sb):
        sb.pop(a)
        for x in v['beats']:
            if x.get('active', -1) > a: x['active'] -= 1
        M.set_sidebar(vid, sb)


def set_slide(M, vid, title, script, new_title=None, keep_pre=True):
    n = n_of(M, vid, title)
    kw = {} if keep_pre else {'pre': []}
    M.set_slide(vid, n, title=new_title if new_title is not None else title, script=script, **kw)


def set_sidebar_label(M, vid, old, new):
    sb = list(M.video(vid)['hybrid']['sidebar'])
    sb[sb.index(old)] = new
    M.set_sidebar(vid, sb)


def retitle(M, vid, title):
    v = M.video(vid)
    v['title'] = title; v['navLabel'] = title
    v.setdefault('hybrid', {})['title'] = title
    b0 = v['beats'][0]
    if b0.get('mode') == 'title':
        b0['bigTitle'] = title; b0['title'] = title
    M.touched_videos.add(vid)


def lines_of(M, vid, title):
    """the slide's current script in DSL form (str / A(...) / D(...)), to edit and pass back to set_slide."""
    from dsl import A, D
    b = M.video(vid)['beats'][n_of(M, vid, title) - 1]
    out = []
    for l in b['lines']:
        if 'say' in l: out.append(l['say'])
        elif 'appear' in l: out.append(A(l['label'], b['items'][l['appear']]))
        else: out.append(D(l['draw']))
    return out


def _text(x):
    if isinstance(x, str): return x
    if x[0] == 'A': return x[1] + ' ' + str((x[2] or {}).get('t', ''))
    return x[1]


def drop_lines(script, *subs):
    """script without the lines (spoken, drawn or appearing items) that contain any of subs; each sub must match."""
    hit = {s: 0 for s in subs}
    out = []
    for x in script:
        t = _text(x); m = [s for s in subs if s in t]
        for s in m: hit[s] += 1
        if not m: out.append(x)
    miss = [s for s, k in hit.items() if not k]
    assert not miss, ('drop_lines: no line with', miss)
    return out


def replace_line(script, sub, new):
    """replace the one line containing sub by new (a line or a list of lines)."""
    ks = [i for i, x in enumerate(script) if sub in _text(x)]
    assert len(ks) == 1, ('replace_line', sub, ks)
    k = ks[0]
    return script[:k] + (new if isinstance(new, list) else [new]) + script[k + 1:]
