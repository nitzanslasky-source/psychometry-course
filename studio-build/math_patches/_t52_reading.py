"""2026-10-21 topic 52 (Charts & Tables) for the teacher's own reading. Topic 52 is built by modulesV52a.py (the lessons) and
modulesV52b.py (the three guided chart sets) in build_verbal.py (not a math_patches/tNN.py topic), so build_verbal.py
calls ai_redo_t52(MATH) right after the module videos are in (exactly like topic 51, math_patches/_t51_reading.py):
every topic-52 video listed in _ai_vis_t52.py is rebuilt from its ONE spec (script ai_scripts/<vid>.json, visual plan,
slides) and _ai_visual.apply() adds the click items, POINT highlights and chart layers - like ai_redo_tNN for the math
topics. The camera lesson ch52-intro is split into parts (math_patches/_camera_parts.py); the long lessons too (not on
camera). The summary video ch52-summary is not in the spec: summary_pages/t52.json replaces it. A video with a take
recorded before AI52_CUTOFF (UTC) keeps the module version (none of topic 52 is recorded on 21 Oct 2026).
(env AIVIS_T52 = another spec file, for tests)"""
import glob, importlib.util, os, re, sys

AI52_CUTOFF = '2026-10-21T00-00-00'
HERE = os.path.dirname(os.path.abspath(__file__))


def _recorded(vid):
    pat = re.compile(re.escape(vid) + r'-(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d)[\d-]*Z\.(mp4|webm)$')
    for f in glob.glob(os.path.expanduser('~/Documents/Course.recordings/**/*'), recursive=True):
        m = pat.match(os.path.basename(f))
        if m and m.group(1) < AI52_CUTOFF: return True
    return False


def _mod(name, path=None):
    if name not in sys.modules:
        p = path or os.path.join(HERE, name + '.py')
        if not os.path.exists(p): return None
        spec = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(spec)
        sys.modules[name] = m; spec.loader.exec_module(m)
    return sys.modules[name]


# choice order like the real exam (math_patches/_choice_order.py convention: 1, 2, 3, 4 in their own place); the guided
# question that broke it is reordered here, together with its new reading script (which names the NEW position).
# new order = old indices in the new places.
REORDER = {'ch-q01': [0, 2, 1, 3]}      # 7, 3, 6, 10  ->  7, 6, 3, 10  (the answer 6: choice number two)
_DONE = set()


def reorder_choices(D):
    for qid, perm in REORDER.items():
        q = D['questions'].get(qid)
        if not q or id(q) in _DONE: continue
        for k in ('choices', 'choicesRich', 'choicesHtml'):
            if isinstance(q.get(k), list) and len(q[k]) == 4: q[k] = [q[k][i] for i in perm]
        q['correct'] = [perm.index(c) for c in q['correct']]
        _DONE.add(id(q))


def ai_redo_t52(M):
    S = _mod('_t52draft_env', os.environ['AIVIS_T52']) if os.environ.get('AIVIS_T52') else _mod('_ai_vis_t52')
    if S is None: return
    AV = _mod('_ai_visual')
    reorder_choices(M.D)
    for sec in M.D['sections']: M.sections.setdefault(sec['id'], sec)    # topic 52's sections came after MathCourse was made
    CP = _mod('_camera_parts'); CP.add_to_course(M, S, 52)
    for vid in S.ORDER:
        if vid not in M.D['videos'] or _recorded(vid): continue
        S.rebuild(M, vid)
        hy = M.video(vid).setdefault('hybrid', {}); hy['subject'] = 'QUANTITATIVE'   # new_video guesses by topic number
        AV.VIS[vid] = S.vis(vid)
        AV.apply(M, vid)
