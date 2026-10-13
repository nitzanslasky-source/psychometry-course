"""Camera lessons in parts (teacher, 2026-10-14: "shorter parts, about 3-4 minutes each, so I can record each part in 1-2
takes - on camera, cuts are visible").

A topic's camera first lesson is written as ONE spec in _ai_vis_tNN.py and split here at idea boundaries into course
videos of about 2.5-4.5 minutes: part 1 keeps the lesson's id (so every reference to the lesson still finds its start),
part k gets the id '<lesson>-k'. Each part has its own title slide "<Title> (Part k of n)": part 1 keeps the lesson's
opening line, a later part opens with one short natural line (no recap); every part but the last ends with "Okay. I'll
see you in the next part." The content, examples, methods and board items are unchanged; each part is a new board.

    split(globals(), 'absolute-value', 'Absolute Value', [(1, None), (4, "Now ..."), (7, "Now ...")])
        called in _ai_vis_tNN.py right BEFORE the visual passes (for _v in ORDER: ...), so every part gets the passes.
        parts = [(first slide index of the part in the original lesson, its opening line)]; the first entry is (1, None).
    add_to_course(M, S, topic)
        called at the start of tNN.py ai_redo_tNN(): creates the part videos (part 2 onward) in the course right after
        the previous part, in the same section, and gives every part its "(Part k of n)" title.
    is_part(base, vid)  ->  vid is the camera lesson `base` or one of its parts
"""
import re

CLOSE = " [pause] Okay. I'll see you in the next part."


def is_part(base, vid):
    return bool(re.fullmatch(re.escape(base) + r'(-\d+)?', vid))


def split(ns, base, title, parts):
    V = ns['VIDEOS'][base]
    assert V['kind'] == 'lesson' and parts[0] == (1, None), (base, 'a lesson, split after its title slide')
    slides = V['slides']; n = len(parts)
    starts = [p[0] for p in parts] + [len(slides)]
    assert starts == sorted(starts) and starts[-2] < len(slides), (base, starts)
    ids = [base] + ['%s-%d' % (base, k) for k in range(2, n + 1)]
    reg = ns.setdefault('CAMERA_PARTS', {}); titles = ns.setdefault('PART_TITLES', {})
    order = ns['ORDER']; i = order.index(base)
    for k in range(n):
        ttl = '%s (Part %d of %d)' % (title, k + 1, n)
        body = slides[starts[k]:starts[k + 1]]
        if k == 0:
            head = dict(slides[0]); head['title'] = ttl; head['sb'] = ttl
        else:
            head = ns['S'](ttl, ns['L'](parts[k][1]))
        if k < n - 1:
            last = body[-1]['lines'][-1]
            assert "see you" not in last['say'], (base, 'part %d already ends with a closing' % (k + 1))
            last['say'] = last['say'].rstrip() + CLOSE
        nv = dict(V); nv['slides'] = [head] + list(body); nv['title'] = ttl
        ns['VIDEOS'][ids[k]] = nv
        if k: order.insert(i + k, ids[k])
        titles[ids[k]] = ttl
    reg[base] = ids
    return ids


def add_to_course(M, S, topic):
    for base, ids in getattr(S, 'CAMERA_PARTS', {}).items():
        if base not in M.D['videos']: continue
        sec = next(f['section'] for f in M.D['flow'] if f['ref'] == base)
        prev = base
        for vid in ids:
            title = S.PART_TITLES[vid]
            if vid not in M.D['videos']:
                beats, sb = S.studio_slides(vid)
                M.new_video(vid, topic, title, sb, beats, sec, after=prev)
            v = M.video(vid); v['title'] = title; v['navLabel'] = title
            v.setdefault('hybrid', {})['title'] = title
            prev = vid
