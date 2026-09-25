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
OUT = '/Users/nitzanslasky/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html'
DOCDIR = '/Users/nitzanslasky/Downloads'
VERBAL = range(39, 50)
DROP_OLD = os.environ.get('DROP_OLD', '1') == '1'
KEEP_COURSE_PRACTICE = {39, 40}          # topics whose practice stays the course's own (no bank category)

s, i, j, D = load(BASE)
s = renderer_patch.apply(s)
s = studio_patch.apply(s)

# ---------- bank questions + passages ----------
BQ, POOLS, BP, RC = vbank.questions()
D['questions'].update(BQ)
D.setdefault('passages', {}).update(BP)

# ---------- modules ----------
MODS, CARDS = {}, []
for f in sorted(glob.glob(os.path.join(HERE, 'modulesV*.py'))):
    name = os.path.basename(f)[:-3]
    m = importlib.import_module(name)
    for mod in m.MODULES: MODS.setdefault(mod['topic'], []).append(mod)
    CARDS += getattr(m, 'MEMORY', [])

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

json.dump(LOCK, open(LOCKF, 'w'), indent=0, sort_keys=True)
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
            if os.environ.get('PG','1')=='1': qq['practiceGroup'] = D['passages'][qq['passageId']]['title'] if qq.get('passageId') else 'Unit %d' % (k // 10 + 1)
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
        hy = {'num': m['num'], 'title': m['title'], 'sidebar': m['sidebar'], 'subject': 'VERBAL'}
        D['videos'][m['id']] = {'id': m['id'], 'topic': t, 'title': m['title'] if not m.get('guided') else
                                'Question %d · %s' % (m['qn'], m['title']), 'kind': m['kind'], 'beats': beats,
                                'sourceFiles': ['04-Verbal-Reasoning-Original-Subtitles.txt'], 'wordCount': words,
                                'minutes': round(words / 130, 1), 'navLabel': m['title'], 'hybrid': hy}
        if m.get('guided'): D['videos'][m['id']]['questionId'] = m['qid']
D['meta']['videos'] = len(D['videos'])

# ---------- memory cards ----------
for card in CARDS:
    ref = {k: card[k] for k in ('title', 'intro', 'tables', 'tips') if k in card}
    ref.update(kind='memory', rows=[], example='')
    D['references'][card['id']] = ref
    k = next(n for n, f in enumerate(flow) if f['type'] == 'video' and f['ref'] == card['after'])
    vf = flow[k]; fid = 'flow-' + card['id']
    flow.insert(k + 1, {'id': fid, 'topic': vf['topic'], 'section': vf['section'], 'type': 'reference', 'ref': card['id']})
    items = sections[vf['section']]['items']; items.insert(items.index(vf['id']) + 1, fid)

# ---------- write ----------
body = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
s2, i2, j2, _ = load(BASE)   # positions in the base; recompute on the patched html
k0 = s.find('window.COURSE=') + len('window.COURSE='); k1 = s.find('</script>', k0)
out = s[:k0] + body + ';' + s[k1:]
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
                else: md.append('%d. *[DRAW: %s]*' % (n, l['draw']))
            md += ['', b['nextCue'], '']
    p = os.path.join(DOCDIR, 'Verbal-Hybrid-Scripts-Topic%d.md' % t)
    open(p, 'w', encoding='utf-8').write('\n'.join(md)); print('wrote', p)
print(json.dumps(report))
