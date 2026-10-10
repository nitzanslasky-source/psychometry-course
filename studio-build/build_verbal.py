"""Build the studio with Verbal Reasoning hybrid videos on top of the finished v18 studio (base-v18.html).

Inputs: base-v18.html (all Algebra / Word Problems / Geometry work, renderer, pen) · vbank.py (question bank) ·
modulesV<topic>[a-z].py files, each defining MODULES and MEMORY.
Output: ~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html + Verbal-Hybrid-Scripts-Topic<N>.md
"""
import json, re, glob, importlib, os, sys, html as _html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_io import load
import renderer_patch, studio_patch, vbank

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, 'base-v18.html')
OUT = os.environ.get('OUT', '/Users/nitzanslasky/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html')
DOCDIR = '/Users/nitzanslasky/Downloads'
VERBAL = list(range(39, 51)) + [51, 52]   # 52 = Charts & Tables   # 51 = Psychometric Thinking (quantitative methods, built like the verbal topics)
DROP_OLD = os.environ.get('DROP_OLD', '1') == '1'
KEEP_COURSE_PRACTICE = {39, 40}          # topics whose practice stays the course's own (no bank category)

s, i, j, D = load(BASE)
s = renderer_patch.apply(s)
s = studio_patch.apply(s)

# ---------- math fixes (course review 2026-09): math_patches/tNN.py on top of the baked Algebra/WP/Geometry ----------
import math_api
MATH = math_api.apply_patches(D)
print('math patches: %d questions, %d videos touched' % (len(MATH.touched_questions), len(MATH.touched_videos)))
# 2026-10-09 spoken labels (math_patches/_spoken_labels.py): warn about a spoken line in an UNRECORDED math video that still
# opens with a reading-style label ("Careful:", "Notice:", "Step one:", "The trap:" ...) - the teacher wants speech there
if '_spoken_labels' in sys.modules:
    _SL = sys.modules['_spoken_labels']
    print('spoken labels: %d lines rewritten in %d videos' % (sum(_SL.CHANGED.values()), len(_SL.CHANGED)))
    for _w in _SL.WARN: print('WARNING spoken labels:', _w)
    _left = _SL.check_left(D)
    if _left:
        print('WARNING spoken labels: %d spoken line(s) in unrecorded math videos still start with a label - say it as speech '
              '(add them to math_patches/_spoken_labels.py MAP):' % len(_left))
        for _w in _left: print('    ' + _w)
# 2026-10-09 choice order like the real exam (math_patches/_choice_order.py): a choice 1/2/3/4 (or 1/2, 1/3, 1/4) sits in
# its own place; the full check (topics 1-38, 51, 52) runs below, once the quantitative modules are in
if '_choice_order' in sys.modules:
    _CO = sys.modules['_choice_order']
    print('choice order: %d questions reordered (%d video / solution lines follow), %d kept as recorded'
          % (len(_CO.CHANGED), sum(_CO.CHANGED.values()), len(_CO.SKIPPED)))
    for _w in _CO.WARN: print('WARNING choice order:', _w)

# ---------- Topic 50: Writing task (new topic, not in the base) ----------
if not any(x['id'] == 50 for x in D['topics']):
    D['topics'].append({'id': 50, 'title': 'Writing task', 'description': 'Verbal reasoning · Writing task',
                        'subject': 'Verbal reasoning', 'sections': ['vr50-learn', 'vr50-practice']})
    D['sections'] += [{'id': 'vr50-learn', 'topic': 50, 'title': 'Learn', 'kind': 'learn', 'items': ['flow-vr50-anchor'], 'questionCount': 0},
                      {'id': 'vr50-practice', 'topic': 50, 'title': 'Practice tasks', 'kind': 'practice', 'items': [], 'questionCount': 0}]
    D['flow'].append({'id': 'flow-vr50-anchor', 'topic': 50, 'section': 'vr50-learn', 'type': 'reference', 'ref': 'vr50-anchor'})

if not any(x['id'] == 51 for x in D['topics']):
    D['topics'].append({'id': 51, 'title': 'Psychometric Thinking', 'description': 'Quantitative reasoning · Psychometric thinking',
                        'subject': 'Quantitative reasoning', 'sections': ['pt51-learn', 'pt51-practice']})
    D['sections'] += [{'id': 'pt51-learn', 'topic': 51, 'title': 'Learn', 'kind': 'learn', 'items': ['flow-pt51-anchor'], 'questionCount': 0},
                      {'id': 'pt51-practice', 'topic': 51, 'title': 'Practice', 'kind': 'practice', 'items': [], 'questionCount': 0}]
    D['flow'].append({'id': 'flow-pt51-anchor', 'topic': 51, 'section': 'pt51-learn', 'type': 'reference', 'ref': 'pt51-anchor'})

if not any(x['id'] == 52 for x in D['topics']):
    D['topics'].append({'id': 52, 'title': 'Charts & Tables', 'description': 'Quantitative reasoning · Charts and tables',
                        'subject': 'Quantitative reasoning', 'sections': ['ch52-learn', 'ch52-practice']})
    D['sections'] += [{'id': 'ch52-learn', 'topic': 52, 'title': 'Learn', 'kind': 'learn', 'items': ['flow-ch52-anchor'], 'questionCount': 0},
                      {'id': 'ch52-practice', 'topic': 52, 'title': 'Practice', 'kind': 'practice', 'items': [], 'questionCount': 0}]
    D['flow'].append({'id': 'flow-ch52-anchor', 'topic': 52, 'section': 'ch52-learn', 'type': 'reference', 'ref': 'ch52-anchor'})

# ---------- bank questions + passages ----------
BQ, POOLS, BP, RC = vbank.questions()
D['questions'].update(BQ)
D.setdefault('passages', {}).update(BP)

# ---------- modules ----------
MODS, CARDS, PRACT = {}, [], {}
TEST = 'OUT' in os.environ          # test build: own output file, no shared side files
ONLY = os.environ.get('VMODS')      # e.g. VMODS=modulesV50 -> load only module files starting with that
for f in sorted(glob.glob(os.path.join(HERE, 'modulesV*.py'))):
    name = os.path.basename(f)[:-3]
    if ONLY and not any(name.startswith(x) for x in ONLY.split(',')): continue
    m = importlib.import_module(name)
    for mod in m.MODULES: MODS.setdefault(mod['topic'], []).append(mod)
    CARDS += getattr(m, 'MEMORY', [])
    D['questions'].update(getattr(m, 'QUESTIONS', {}))          # a module may bring its own questions
    pr_ = getattr(m, 'PRACTICE', {})
    if isinstance(pr_, dict):
        for t_, qs_ in pr_.items(): PRACT.setdefault(t_, []).extend(qs_)

# topics created above but with no module loaded (test builds with VMODS): take them out again
for t_, anc in ((50, 'vr50-anchor'), (51, 'pt51-anchor'), (52, 'ch52-anchor')):
    if t_ not in MODS:
        D['topics'] = [x for x in D['topics'] if x['id'] != t_]
        D['sections'] = [x for x in D['sections'] if x.get('topic') != t_]
        D['flow'] = [f for f in D['flow'] if f.get('topic') != t_]

def tex_plain(t):
    return re.sub(r'\s+', ' ', t.replace('$', '')).strip()

def item_desc(it):
    if it.get('k') == 'q':
        q = D['questions'][it['qid']]
        return 'question %s with its four answer choices — "%s"' % (it['qid'], tex_plain(it.get('stem') or q['stemRich'])[:220])
    if it.get('k') == 'psg':
        return 'passage %s, paragraph(s) %s' % (it['pid'], it.get('paras', 'all'))
    return tex_plain(it.get('t', ''))

def build_video(m):
    beats = []
    for si, sl in enumerate(m['slides']):
        items = [dict(it) for it in sl.get('pre', [])]
        pre = len(items); lines = []
        for x in sl['script']:
            if isinstance(x, str): lines.append({'say': x})
            elif x[0] == 'A': items.append(dict(x[2])); lines.append({'appear': len(items) - 1, 'label': x[1]})
            elif x[0] == 'P': lines.append(dict(x[1]))
            else: lines.append({'draw': x[1]})
        # text-question slides: reserve room between the question and the answers for this slide's pop-ins
        tq = [it for it in items[:pre] if it.get('k') == 'q' and it.get('tq')]
        if tq and 'band' not in tq[0]:
            need = 0
            for it in items[pre:]:
                if it.get('k') == 't':
                    z = it.get('size', 46); w = it.get('w', 1130)
                    nl = max(1, -(-len(tex_plain(it['t'])) * z * .52 // w))
                    need += nl * z * 1.3 + 16
            tq[0]['band'] = int(max(70, need + 40))
            if need and not any('draw' in l and re.search(r'choice|cross|answer|option', l['draw'], re.I) for l in lines): tq[0]['hideok'] = True
        mode = sl['mode']; active = sl.get('active', -1)
        topic = m['sidebar'][active] if active >= 0 else None
        if mode == 'title':
            loads = 'Clean title slide: the sidebar (nothing highlighted yet) and one massive centred title. Nothing else.'
            canvas = 'Massive title — "%s"' % sl['title']
        elif mode == 'concept':
            loads = 'Sidebar with "%s" highlighted; the main canvas is completely blank.' % topic; canvas = 'Blank'
        else:
            loads = 'Sidebar with "%s" highlighted; the full question is already on the canvas as typed text.' % topic
            canvas = 'Pre-loaded — ' + '; '.join(item_desc(it) for it in sl['pre'])
        nxt = m['slides'][si + 1]['title'] if si + 1 < len(m['slides']) else None
        beats.append({'title': sl['title'] if mode != 'title' else m['title'], 'layout': 'hybrid', 'mode': mode,
                      'active': active, 'items': items, 'pre': pre, 'lines': lines, 'loads': loads, 'canvas': canvas,
                      'src': sl.get('src', 'html'), 'number': si + 1, 'bigTitle': sl['title'] if mode == 'title' else None,
                      'nextCue': '[NEXT SLIDE → %s]' % nxt if nxt else '[END VIDEO]',
                      'board': [], 'visual': None, 'script': ''})
    return beats

# ---------- guided questions: "Question N" per topic ----------
_W = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
def _word(n):
    if n < 21: return _W[n]
    return {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty'}[n // 10] + ('-' + _W[n % 10] if n % 10 else '')
_NUMRX = r'(\d+|' + '|'.join(sorted({_word(k) for k in range(1, 60)}, key=len, reverse=True)) + r')'
def _val(w): return int(w) if w.isdigit() else next(k for k in range(1, 60) if _word(k) == w)

# Locked numbers: once a question has a number it keeps it forever (recordings show it). New questions get the next free number.
LOCKF = os.path.join(HERE, 'question_numbers.json')
LOCK = json.load(open(LOCKF)) if os.path.exists(LOCKF) else {}
if not LOCK:   # first run: record the numbers already baked into Algebra / Word Problems / Geometry
    for vid, v in D['videos'].items():
        if v.get('hybrid') and v.get('kind') == 'solution' and v['beats'] and v['beats'][0].get('bigTitle', '') and v['beats'][0]['bigTitle'].startswith('Question '):
            LOCK[vid] = {'topic': v['topic'], 'n': int(v['beats'][0]['bigTitle'].split()[1])}
for t, mods in MODS.items():
    groups, order = {}, []
    for m in mods:
        if m.get('guided'):
            key = (m['title'], tuple(m['sidebar']))
            if key not in groups: groups[key] = []; order.append(key)
            groups[key].append(m)
    taken = {e['n'] for e in LOCK.values() if e['topic'] == t}
    for key in order:
        ms = sorted(groups[key], key=lambda m: m['guided'])
        nums = []
        for m in ms:
            if m['id'] not in LOCK:
                k = max(taken | {0}) + 1; taken.add(k); LOCK[m['id']] = {'topic': t, 'n': k}
            nums.append(LOCK[m['id']]['n'])
        sb = ['Question %d' % k for k in sorted(nums)]
        for m, k in zip(ms, nums):
            old = m['guided']; m['qn'] = k; m['sidebar'] = sb
            for sl in m['slides']:
                if sl['mode'] != 'title': sl['active'] = sb.index('Question %d' % k)
            def fix(x, old=old, k=k):
                def r(mo):
                    if _val(mo.group(2).lower()) != old: return mo.group(0)
                    return mo.group(1) + 'uestion ' + (str(k) if mo.group(2).isdigit() else _word(k))
                return re.sub(r'\b([Qq])uestion ' + _NUMRX + r'\b', r, x)
            for sl in m['slides']:
                if sl['mode'] == 'title': sl['title'] = 'Question %d' % k
                sl['script'] = [fix(x) if isinstance(x, str) else x for x in sl['script']]

for vid, v in D['videos'].items():   # math solution videos added by math_patches
    if v.get('topic', 99) <= 38 and v.get('kind') == 'solution' and v.get('beats') and (v['beats'][0].get('bigTitle') or '').startswith('Question '):
        LOCK[vid] = {'topic': v['topic'], 'n': int(v['beats'][0]['bigTitle'].split()[1])}
if not TEST: json.dump(LOCK, open(LOCKF, 'w'), indent=0, sort_keys=True)
# ---------- module numbers (per subject, course order; a guided group shares one number) ----------
num, seen = 0, {}
for t in sorted(MODS):
    for m in MODS[t]:
        key = (t, m['title'], tuple(m['sidebar'])) if m.get('guided') else m['id']
        if key not in seen: num += 1; seen[key] = num
        m['num'] = seen[key]

# ---------- rebuild flow + sections of converted topics ----------
USED_ANY = {it['qid'] for ms in MODS.values() for m in ms for sl in m['slides'] for it in sl.get('pre', []) if it.get('k') == 'q'}
flow = D['flow']
sections = {x['id']: x for x in D['sections']}
report = {}
for t in sorted(MODS):
    mods = MODS[t]
    top = next(x for x in D['topics'] if x['id'] == t)
    learn_id = next(sid for sid in top['sections'] if sections[sid]['kind'] == 'learn')
    prac_id = next(sid for sid in top['sections'] if sections[sid]['kind'] == 'practice')
    old_items = sections[learn_id]['items'] + sections[prac_id]['items']
    old_flow = {f['id']: f for f in flow if f['section'] in (learn_id, prac_id)}
    old_refs = {(f['type'], f['ref']) for f in old_flow.values()}
    pos = min(k for k, f in enumerate(flow) if f['id'] in old_flow)
    flow[:] = [f for f in flow if f['id'] not in old_flow]
    new = []
    used_q = set()
    for m in mods:
        vid = m['id']
        if m.get('guided'):
            used_q.add(m['qid'])
            new.append({'id': 'flow-%s-q-%s' % (learn_id, m['qid']), 'topic': t, 'section': learn_id, 'type': 'question', 'ref': m['qid']})
        new.append({'id': 'flow-%s-v-%s' % (learn_id, vid), 'topic': t, 'section': learn_id, 'type': 'video', 'ref': vid})
    # practice
    if t in KEEP_COURSE_PRACTICE:
        prac = [old_flow[fid]['ref'] for fid in sections[learn_id]['items'] + sections[prac_id]['items']
                if old_flow[fid]['type'] == 'question' and old_flow[fid]['ref'] not in USED_ANY]   # unused course learn questions join practice
    elif t == 49:
        prac = [q for q in RC if q not in USED_ANY]
    elif t in PRACT:
        prac = [q for q in PRACT[t] if q not in USED_ANY]
    else:
        target = sum(1 for fid in sections[prac_id]['items'] if old_flow[fid]['type'] == 'question')
        pool = [q for q in POOLS.get(t, []) if q not in USED_ANY]
        trusted = [q for q in pool if D['questions'][q]['trustRank'] <= 4]
        extra = [q for q in pool if D['questions'][q]['trustRank'] == 5]
        prac = trusted + extra[:max(0, target - len(trusted))]
    for k, q in enumerate(prac):
        qq = D['questions'][q]
        if t not in KEEP_COURSE_PRACTICE:
            qq['unit'] = prac_id
            if os.environ.get('PG','1')=='1': qq['practiceGroup'] = qq.get('setTitle') or (D['passages'][qq['passageId']]['title'] if qq.get('passageId') else 'Unit %d' % (k // 10 + 1))
        new.append({'id': 'flow-%s-q-%s' % (prac_id, q), 'topic': t, 'section': prac_id, 'type': 'question', 'ref': q})
    for q in used_q: D['questions'][q]['unit'] = learn_id; D['questions'][q]['guided'] = True
    flow[pos:pos] = new
    sections[learn_id]['items'] = [f['id'] for f in new if f['section'] == learn_id]
    sections[prac_id]['items'] = [f['id'] for f in new if f['section'] == prac_id]
    # drop the replaced course videos (questions stay in the data only if still referenced)
    new_refs = {(f['type'], f['ref']) for f in new}
    for typ, ref in old_refs - new_refs:
        if typ == 'video' and DROP_OLD: D['videos'].pop(ref, None)
        elif typ == 'question' and DROP_OLD and not any(f['ref'] == ref for f in flow): D['questions'].pop(ref, None)
    report[t] = dict(modules=len(mods), guided=len(used_q), practice=len(prac),
                     practice_review=sum(D['questions'][q].get('reviewFlag', False) for q in prac))

# ---------- videos ----------
for t in sorted(MODS):
    for m in MODS[t]:
        beats = build_video(m)
        words = sum(len(l['say'].split()) for b in beats for l in b['lines'] if 'say' in l)
        hy = {'num': m['num'], 'title': m['title'], 'sidebar': m['sidebar'], 'subject': 'QUANTITATIVE' if t in (51, 52) else 'VERBAL'}
        D['videos'][m['id']] = {'id': m['id'], 'topic': t, 'title': m['title'] if not m.get('guided') else
                                'Question %d · %s' % (m['qn'], m['title']), 'kind': m['kind'], 'beats': beats,
                                'sourceFiles': ['04-Verbal-Reasoning-Original-Subtitles.txt'], 'wordCount': words,
                                'minutes': round(words / 130, 1), 'navLabel': m['title'], 'hybrid': hy}
        if m.get('guided'): D['videos'][m['id']]['questionId'] = m['qid']
D['meta']['videos'] = len(D['videos'])

# ---------- memory cards ----------
PLACED = set()
for card in CARDS:
    ref = {k: card[k] for k in ('title', 'intro', 'tables', 'tips') if k in card}
    ref.update(kind='memory', rows=[], example='')
    D['references'][card['id']] = ref
    k = next(n for n, f in enumerate(flow) if f['type'] == 'video' and f['ref'] == card['after'])
    vf = flow[k]; fid = 'flow-' + card['id']
    sec = card.get('section') or vf['section']          # a card may go straight into another section (e.g. practice)
    if sec != vf['section']:
        ks = [n for n, f in enumerate(flow) if f['section'] == sec]; k = (ks[-1] if ks else k)
        flow.insert(k + 1, {'id': fid, 'topic': vf['topic'], 'section': sec, 'type': 'reference', 'ref': card['id']})
        sections[sec]['items'].append(fid); continue
    items = sections[vf['section']]['items']; ki = items.index(vf['id'])
    while k + 1 < len(flow) and flow[k + 1]['type'] == 'reference' and flow[k + 1]['id'] in PLACED:   # keep list order
        k += 1; ki += 1
    flow.insert(k + 1, {'id': fid, 'topic': vf['topic'], 'section': vf['section'], 'type': 'reference', 'ref': card['id']})
    items.insert(ki + 1, fid); PLACED.add(fid)

# ---------- NITE terminology (quantitative topics only) ----------
import terminology; TERM = terminology.apply(D)

# ---------- no question numbers inside videos (the website numbers questions; see no_question_numbers.py) ----------
import no_question_numbers; print('question-number title slides removed: %d' % no_question_numbers.apply(D))
_left = no_question_numbers.report(D)
assert not _left, 'videos still mention question numbers: %r' % _left[:5]
print('NITE terminology (changes per rule and field type):'); print(terminology.report(TERM))

# ---------- "x = ?" on its own line under the given (stem_lines.py); recorded videos keep their old board ----------
import stem_lines; STEM = stem_lines.apply(D); print(stem_lines.report(STEM))

# 2026-10-09 choice order check: every multiple-choice question (topics 1-38, 51, 52) of an UNRECORDED video or of
# practice must follow the real-exam order (1, 2, 3, 4 and 1/2, 1/3, 1/4 in their own place)
if '_choice_order' in sys.modules:
    _left = sys.modules['_choice_order'].check_left(D)
    _rec = sys.modules['_choice_order'].recorded(D)
    if _left:
        print('WARNING choice order: %d unrecorded multiple-choice question(s) break the real-exam order - put 1, 2, 3, 4 '
              '(and 1/2, 1/3, 1/4) in their own place (math: add them to math_patches/_choice_order.py QMAP):' % len(_left))
        for _w in _left: print('    ' + _w)
    print('choice order: %d question(s) in recorded videos keep their old order (teacher to decide)' % len(_rec))

# ---------- arrow chains reveal one part per click (studio_arrows.py); videos recorded before its CUTOFF stay frozen ----------
import studio_arrows
ARW_FROZEN, ARW_LATE = studio_arrows.frozen_ids()
ARW = studio_arrows.apply_data(D, ARW_FROZEN)
print('arrow parts: %d items in %d videos (%d beats, %d extra clicks); %d recorded videos frozen (%d of them have arrow lines, kept whole)'
      % (ARW['items'], len(ARW['videos']), ARW['beats'], ARW['cues'], len(ARW_FROZEN), len(ARW['frozen_skipped'])))
_late = sorted({vid for vid, ts in ARW_LATE if vid in ARW['videos']})
if _late: print('  WARNING: takes recorded after CUTOFF %s for videos that now reveal arrows in parts: %s — if they were made with an older studio file, move CUTOFF later and rebuild' % (studio_arrows.CUTOFF, _late))

# ---------- write ----------
body = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
s2, i2, j2, _ = load(BASE)   # positions in the base; recompute on the patched html
k0 = s.find('window.COURSE=') + len('window.COURSE='); k1 = s.find('</script>', k0)
out = s[:k0] + body + ';' + s[k1:]
import slide_style, studio_ui, studio_cut, studio_edit, studio_continue, studio_ai, studio_done; out = studio_arrows.apply(studio_done.apply(studio_ai.apply(studio_continue.apply(studio_edit.apply(studio_cut.apply(studio_ui.apply(slide_style.apply(out))))), D)), ARW_FROZEN)   # slide look: teal theme, bold labels, panels, larger text
# ---------- added content (not from the teacher's Hebrew course) marked in the studio UI (added_content.py, studio_added.py) ----------
import added_content, studio_added
ADDED, _aw = added_content.manifest(D, load(BASE)[3], MATH.touched_videos)
for x in _aw: print('  added_content WARNING:', x)
_nw = added_content.attach_notes(ADDED, D)          # WHAT each added item teaches (added_notes.json)
for x in _nw: print('  added_notes WARNING:', x)
print('added content (vs base-v18):'); print(added_content.report(ADDED, D))
print('  notes: %d added items / slides with new lines, %d without a note' % (sum((1 if r['added'] else 0) + (0 if r['added'] else sum(1 for x in r['slides'].values() if x['kind'] == 'new')) + len(r['lines']) for r in ADDED.values()), len(_nw)))
out = studio_added.apply(out, ADDED, D)
# ---------- navigation order: by topic | by the students' study plan (src/lib/planData.ts) (studio_order.py) ----------
import studio_order; out = studio_order.apply(out, D)
# ---------- videos to re-record (math_patches/_rerecord.py): red ⟳ instead of green until a newer take exists (studio_rerecord.py) ----------
import studio_rerecord; out = studio_rerecord.apply(out, D)
# ---------- AI auto-narrate + POINT cues (studio_autonarrate.py): needs AI_VIDEOS from studio_ai ----------
import studio_autonarrate; out = studio_autonarrate.apply(out)
_amd = os.path.join(DOCDIR, 'Added-Content-List.md') if not TEST else os.path.splitext(OUT)[0] + '-Added-Content-List.md'
open(_amd, 'w', encoding='utf-8').write(added_content.markdown(ADDED, D, studio_done.recorded_ids())); print('wrote', _amd)
open(OUT, 'w', encoding='utf-8').write(out)
print('wrote', OUT, '%.1f MB' % (len(out) / 1e6))

# ---------- script documents ----------
for t in sorted(MODS):
    top = next(x for x in D['topics'] if x['id'] == t)
    md = ['# Verbal Reasoning · Topic %d · %s — Hybrid Whiteboard Scripts' % (t, top['title']), '']
    for m in MODS[t]:
        v = D['videos'][m['id']]
        md += ['---', '', '## Module %d: %s%s' % (m['num'], m['title'], (' — Question %d (%s)' % (m['qn'], m['qid'])) if m.get('guided') else ''), '']
        for b in v['beats']:
            md += ['### Slide %d · %s%s' % (b['number'], b['title'], '  *(Hebrew-only example)*' if b['src'] == 'hebrew' else ''), '',
                   '**[SLIDE LOADS]:** ' + b['loads'], '',
                   '**Sidebar:** ' + ' · '.join(('**%s (Active)**' % x) if n == b['active'] else x for n, x in enumerate(m['sidebar'])), '']
            for n, l in enumerate(b['lines'], 1):
                if 'say' in l: md.append('%d. %s' % (n, l['say']))
                elif 'appear' in l: md.append('%d. **[APPEAR: %s]**' % (n, l['label']))
                elif 'point' in l: md.append('%d. *[POINT: %s]*' % (n, l.get('label') or l['point']))
                else: md.append('%d. *[DRAW: %s]*' % (n, l['draw']))
            md += ['', b['nextCue'], '']
    p = os.path.join(DOCDIR, 'Verbal-Hybrid-Scripts-Topic%d.md' % t)
    if not TEST: open(p, 'w', encoding='utf-8').write('\n'.join(md)); print('wrote', p)
print(json.dumps(report))
