"""Check math patches for some topics:  python3 math_check.py 5 6 [--no-layout]
Builds a math-only studio (base + patches for those topics) into tmp_check/, validates data, lints text, runs the
slide layout check on every video the patches touched, and writes fresh student-view dumps to tmp_check/view/."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_io import load
import renderer_patch, studio_patch, math_api
HERE = os.path.dirname(os.path.abspath(__file__))
topics = [int(a) for a in sys.argv[1:] if a.isdigit()]
tag = '-'.join(map(str, topics)) or 'all'
s, i, j, D = load(os.path.join(HERE, 'base-v18.html'))
s = renderer_patch.apply(s); s = studio_patch.apply(s)
M = math_api.apply_patches(D, only=topics or None)
import terminology; terminology.apply(D)   # NITE official wording, as in build_verbal.py
T = set(topics or range(1, 39))
P = []   # problems (must fix)
W = []   # warnings (review)
flow = D['flow']; refs = {f['ref'] for f in flow}
# --- data integrity ---
for f in flow:
    if f['topic'] not in T: continue
    if f['type'] == 'question' and f['ref'] not in D['questions']: P.append('flow question missing: ' + f['ref'])
    if f['type'] == 'video' and f['ref'] not in D['videos']: P.append('flow video missing: ' + f['ref'])
    if f['type'] == 'reference' and f['ref'] not in D['references']: P.append('flow card missing: ' + f['ref'])
for sec in D['sections']:
    if sec['topic'] in T and sec['items'] != [f['id'] for f in flow if f['section'] == sec['id']]: P.append('section items out of sync: ' + sec['id'])
for q in D['questions'].values():
    if q['topic'] not in T or q['id'] not in refs: continue
    if len(q.get('choicesRich') or []) != 4: P.append(q['id'] + ': not 4 choices')
    if not q.get('correct') or not 0 <= q['correct'][0] <= 3: P.append(q['id'] + ': bad correct')
    if not q.get('explanation'): W.append(q['id'] + ': no written solution')
    for fld in ['stemRich'] + ['explanation'] * 1:
        for t in (q.get(fld) if isinstance(q.get(fld), list) else [q.get(fld)]):
            t = str(t or '')
            if re.search(r'[\d)](:[\d(a-z]| : [\d(a-z])', re.sub(r'\b\d{1,2}:\d{2}\b', 'TIME', re.sub(r'\$[^$]*\$', '', t))) and not re.search(r'ratio|proportion|scale|odds', t, re.I): W.append('%s %s: colon used as division? «%s»' % (q['id'], fld, t[:90]))
            for tex in re.findall(r'\$([^$]*)\$', t):
                if re.search(r'[\d)}]\s?:\s?[\d(\\]', tex) and not re.search(r'ratio|proportion|scale|odds', t, re.I): W.append('%s %s: colon in math «%s»' % (q['id'], fld, tex[:60]))
            if re.search(r'[a-z°)],[A-Za-z(]|[a-z°)],\d(?!\d\d(\D|$))|\d,(?!\d\d\d)[A-Za-z0-9(]', re.sub(r'\$[^$]*\$', 'X', t)): W.append('%s %s: missing space after comma «%s»' % (q['id'], fld, t[:80]))
            if re.search(r'[A-Za-z]{2,}−[A-Za-z]{2,}', t): W.append('%s %s: math minus inside a word «%s»' % (q['id'], fld, t[:80]))
    st = q.get('stemRich') or ''
    eqs = [x for x in re.findall(r'\$([^$]*)\$', st) if '=' in x and '?' not in x and '\\begin' not in x]
    if len(eqs) >= 2: W.append('%s: %d equations given side by side - stack them (\\begin{cases} or aligned)' % (q['id'], len(eqs)))
for v in D['videos'].values():
    if v['topic'] not in T: continue
    for n, b in enumerate(v.get('beats', []), 1):
        for l in b['lines']:
            if 'appear' in l and not 0 <= l['appear'] < len(b['items']): P.append('%s #%d: appear index out of range' % (v['id'], n))
            dr = l.get('draw') or ''
            if re.search(r'[\d)](:[\d(a-z]| : [\d(a-z])', re.sub(r'\b\d{1,2}:\d{2}\b', 'TIME', dr)) and not re.search(r'ratio|proportion|scale', dr, re.I): W.append('%s #%d draw uses colon for division: «%s»' % (v['id'], n, dr[:80]))
        for it in b['items']:
            tx = it.get('t') or ''
            if re.search(r'[A-Za-z]{2,}−[A-Za-z]{2,}', tx): W.append('%s #%d board: math minus inside a word «%s»' % (v['id'], n, tx[:60]))
    if v.get('kind') == 'solution' and v.get('questionId') and v['questionId'] not in D['questions']: P.append(v['id'] + ': solution video for missing question')
VIEW = os.path.join(HERE, 'tmp_check', 'view-' + tag); os.makedirs(VIEW, exist_ok=True)
out = os.path.join(HERE, 'tmp_check', 'check-%s.html' % tag)
body = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
k0 = s.find('window.COURSE=') + len('window.COURSE='); k1 = s.find('</script>', k0)
open(out, 'w', encoding='utf-8').write(s[:k0] + body + ';' + s[k1:])
print('PATCHES: %d questions, %d videos touched' % (len(M.touched_questions), len(M.touched_videos)))
print('PROBLEMS (%d):' % len(P)); [print('  ' + x) for x in P]
print('WARNINGS (%d):' % len(W)); [print('  ' + x) for x in W[:400]]
if '--no-layout' not in sys.argv and M.touched_videos:
    r = subprocess.run([sys.executable, os.path.join(HERE, 'layoutcheck.py'), out, '|'.join(sorted(M.touched_videos))], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr[-500:])
env = dict(os.environ, SRC=out, OUTDIR=VIEW)
subprocess.run([sys.executable, os.path.join(HERE, 'student_view.py')] + [str(t) for t in (topics or [])], env=env, capture_output=True)
print('student view dumps: tmp_check/view-%s/t<N>.md' % tag + '  (figures: student_review/fig/)')
