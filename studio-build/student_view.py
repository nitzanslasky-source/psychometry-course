"""Dump what a student sees in each math topic (lessons with slide text + narration, cards, questions with
solutions) in course order, for the pedagogy review. Usage: python3 student_view.py [topic ...]  -> student_review/tN.md"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.environ.get('SRC', os.path.expanduser('~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html')), encoding='utf-8').read()
i = s.find('window.COURSE=') + len('window.COURSE=')
D, _ = json.JSONDecoder().raw_decode(s[i:])
strip = lambda x: re.sub(r'</?(span|p|br|div|sup|sub|em|strong|i|b|u|small|ul|ol|li)(\s[^<>]*)?/?>', '', x or '').strip()

FIG = []   # (name, svg) to render after writing
def fig(svg, name):
    m = re.search(r'aria-label="([^"]*)"', svg or '')
    FIG.append((name, svg)); return '[FIGURE: fig/%s.png - %s]' % (name, m.group(1) if m else '')

def item_text(it):
    if isinstance(it, str): return it
    if isinstance(it, dict) and it.get('k') == 'vis' and isinstance(it.get('v'), dict) and it['v'].get('svg'): return fig(it['v']['svg'], 'v' + __import__('hashlib').md5(str(it.get('v', it.get('fig', {})).get('svg', '')).encode()).hexdigest()[:10])
    if isinstance(it, dict) and it.get('k') == 'q': return 'question %s shown%s' % (it.get('qid'), (' ' + fig(it['fig']['svg'], 'v' + __import__('hashlib').md5(str(it.get('v', it.get('fig', {})).get('svg', '')).encode()).hexdigest()[:10])) if isinstance(it.get('fig'), dict) and it['fig'].get('svg') else '')
    if isinstance(it, dict): return ' | '.join(str(v) for k, v in it.items() if k in ('t', 'text', 'tex', 'label', 'title', 'body', 'html', 'q', 'a') and v)
    return ''

def video(vid, out):
    v = D['videos'].get(vid)
    if not v: out.append('  (video %s missing)' % vid); return
    for b in v['beats']:
        out.append('  --- slide %s: %s' % (b.get('number'), b.get('title', '')))
        if b.get('canvas'): out.append('  [on screen] ' + strip(b['canvas']))
        for it in b.get('items') or []:
            t = item_text(it)
            if t: out.append('  [board] ' + t)
        for l in b.get('lines') or []:
            if l.get('say'): out.append('  SAYS: ' + l['say'])
            elif l.get('do') or l.get('draw'): out.append('  (does: %s)' % strip(str(l.get('do') or l.get('draw'))))

def topic(n):
    """Course order straight from the (patched) studio data: sections -> flow items."""
    top = next(t for t in D['topics'] if t['id'] == n)
    secs = {x['id']: x for x in D['sections']}
    flow = {f['id']: f for f in D['flow']}
    out = ['# Topic %d: %s' % (n, top['title'])]
    qn = 0
    for sid in top['sections']:
        sec = secs[sid]
        out.append('\n## Section: %s (%s)' % (sec['title'], sec['kind']))
        for fid in sec['items']:
            f = flow.get(fid)
            if not f: continue
            if f['type'] == 'video':
                v = D['videos'].get(f['ref'], {})
                out.append('\n### VIDEO: %s (%s min)%s' % (v.get('title'), v.get('minutes'), ' [solution video for %s]' % v['questionId'] if v.get('questionId') else ''))
                video(f['ref'], out)
            elif f['type'] == 'reference':
                c = D['references'].get(f['ref'], {})
                out.append('\n### MEMORY CARD: ' + str(c.get('title', '')))
                out.append(json.dumps({k: c[k] for k in ('intro', 'tables', 'tips') if k in c}, ensure_ascii=False))
            elif f['type'] == 'question':
                q = D['questions'].get(f['ref'])
                if not q: out.append('\n### MISSING QUESTION ' + f['ref']); continue
                qn += 1
                out.append('\n### Q %d (%s): %s' % (qn, q['id'], q.get('stemRich')))
                if (q.get('questionVisual') or {}).get('svg'): out.append('  ' + fig(q['questionVisual']['svg'], q['id']))
                for j, c in enumerate(q.get('choicesRich') or [], 1): out.append('  (%d) %s' % (j, c))
                out.append('  correct: choice %d' % (q['correct'][0] + 1))
                for e in q.get('explanation') or []: out.append('  solution: ' + str(e))
    open(os.path.join(os.environ.get('OUTDIR', os.path.join(H, 'student_review')), 't%d.md' % n), 'w').write('\n'.join(out))
    return len(out)

for n in [int(a) for a in sys.argv[1:]] or range(1, 39):
    print(n, topic(n))
import subprocess
FD = os.path.join(H, 'student_review', 'fig'); os.makedirs(FD, exist_ok=True)
todo = []
for name, svg in FIG:
    sp = os.path.join(FD, name + '.svg')
    same = os.path.exists(sp) and open(sp).read() == svg
    if not (same and os.path.exists(os.path.join(FD, name + '.png'))):
        open(sp, 'w').write(svg); todo.append(name + '.svg')
for k in range(0, len(todo), 40):   # macOS Quick Look renders SVG -> <name>.svg.png
    subprocess.run(['qlmanage', '-t', '-s', '640', '-o', FD] + [os.path.join(FD, t) for t in todo[k:k + 40]], capture_output=True, timeout=300)
for t in todo:
    q = os.path.join(FD, t + '.png')
    if os.path.exists(q): os.replace(q, os.path.join(FD, t[:-4] + '.png'))
print('figures', len(FIG), 'rendered now', len(todo))
