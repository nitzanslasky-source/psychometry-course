"""2026-10-14 topic 51 (Psychometric Thinking) for the teacher's own reading, ON CAMERA (every topic-51 video is a camera
video; long lessons in parts of about 3-4 minutes, math_patches/_camera_parts.py). Topic 51 is built by modulesV51.py in
build_verbal.py (not a math_patches/tNN.py topic), so build_verbal.py calls ai_redo_t51(MATH) right after the module videos
are in: every topic-51 video is rebuilt from its ONE spec in _ai_vis_t51.py (script ai_scripts/<vid>.json, visual plan,
slides) and _ai_visual.apply() adds the click items, POINT highlights and pen marks - exactly like ai_redo_tNN for the
math topics. A video with a camera take recorded before AI51_CUTOFF (UTC) keeps the module version.
(env AIVIS_T51 = another spec file, for tests)"""
import glob, importlib.util, os, re, sys

AI51_CUTOFF = '2026-10-14T00-00-00'
HERE = os.path.dirname(os.path.abspath(__file__))


def _recorded(vid):
    pat = re.compile(re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in glob.glob(os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(os.path.basename(f))
        if m and m.group(1) < AI51_CUTOFF: return True
    return False


def _mod(name, path=None):
    if name not in sys.modules:
        p = path or os.path.join(HERE, name + '.py')
        if not os.path.exists(p): return None
        spec = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(spec)
        sys.modules[name] = m; spec.loader.exec_module(m)
    return sys.modules[name]


# 2026-10-14 choice order like the real exam (math_patches/_choice_order.py convention: 1, 2, 3, 4 in their own place,
# "cannot be determined" in place 4); modulesV51.py's three guided questions that broke it are reordered here, together
# with their new reading scripts (which name the NEW positions). new order = old indices in the new places.
REORDER = {'pt-q06': [0, 2, 1, 3],      # 1, 3, -4, -7          -> 1, -4, 3, -7
           'pt-q09': [0, 1, 3, 2],      # 12, 8, 4, 16          -> 12, 8, 16, 4
           'pt-q24': [0, 2, 1, 3]}      # -5, -2, 2, cannot     -> -5, 2, -2, cannot


_DONE = set()


def reorder_choices(D):
    for qid, perm in REORDER.items():
        q = D['questions'].get(qid)
        if not q or id(q) in _DONE: continue
        for k in ('choices', 'choicesRich', 'choicesHtml'):
            if isinstance(q.get(k), list) and len(q[k]) == 4: q[k] = [q[k][i] for i in perm]
        q['correct'] = [perm.index(c) for c in q['correct']]
        _DONE.add(id(q))


def ai_redo_t51(M):
    S = _mod('_t51draft_env', os.environ['AIVIS_T51']) if os.environ.get('AIVIS_T51') else _mod('_ai_vis_t51')
    if S is None: return
    AV = _mod('_ai_visual')
    reorder_choices(M.D)
    for sec in M.D['sections']: M.sections.setdefault(sec['id'], sec)    # topic 51's sections came after MathCourse was made
    # 2026-10-15 a lesson that is not in modulesV51.py (pt51-understanding): created in the Learn section after its anchor
    for vid, (after, title) in getattr(S, 'NEW_VIDEOS', {}).items():
        if vid in M.D['videos'] or after not in M.D['videos']: continue
        sec = next(f['section'] for f in M.D['flow'] if f['ref'] == after)
        beats, sb = S.studio_slides(vid)
        M.new_video(vid, 51, title, sb, beats, sec, after=after)
    CP = _mod('_camera_parts'); CP.add_to_course(M, S, 51)
    for vid in S.ORDER:
        if vid not in M.D['videos'] or _recorded(vid): continue
        v = M.video(vid)
        S.rebuild(M, vid)
        hy = v.setdefault('hybrid', {}); hy['subject'] = 'QUANTITATIVE'      # new_video (camera parts) guesses by topic number
        AV.VIS[vid] = S.vis(vid)
        AV.apply(M, vid)
