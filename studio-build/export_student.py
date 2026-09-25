"""Export the student course (what students see) from the built studio → psychometry-course/content/full-course/.

Only student-facing data goes out: course order, video ids/titles/lengths, questions with answers and explanations,
figures, passages, memory cards. No scripts, slides, prompter text or teacher notes.

    python3 export_student.py [studio.html]
"""
import json, os, re, sys
from course_io import load

SRC = sys.argv[1] if len(sys.argv) > 1 else '/Users/nitzanslasky/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html'
HERE_ = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE_), 'content', 'full-course')
HERE = os.path.dirname(os.path.abspath(__file__))

SUBJECTS = [('algebra', 'Algebra', range(1, 21)), ('word-problems', 'Word Problems', range(21, 30)),
            ('geometry', 'Geometry', range(30, 39)), ('verbal', 'Verbal Reasoning', range(39, 50))]
def subject_of(t): return next(k for k, _, r in SUBJECTS if t in r)

def tex(s):
    """Studio uses $…$; the app's MathJax uses \\(…\\) only."""
    return re.sub(r'\$([^$]+)\$', lambda m: '\\(' + m.group(1) + '\\)', str(s or '')).strip()

def instructions(q, t):
    if t == 40: return 'Find the relationship between the two words. Choose the pair whose relationship is most similar, keeping the word order.'
    if t == 41:
        sep = 'slashes' if any('/' in c for c in q['choicesRich']) else 'dots'
        return 'Choose the completion that makes the sentence coherent. Insert the phrases in order; the %s separate the blanks.' % sep
    return None

def main():
    _, _, _, D = load(SRC)
    lock = json.load(open(os.path.join(HERE, 'question_numbers.json')))
    qnum = {}   # question id -> locked number (via its worked-solution video)
    for vid, e in lock.items():
        v = D['videos'].get(vid)
        if v and v.get('questionId'): qnum[v['questionId']] = e['n']
    os.makedirs(os.path.join(OUT, 'topics'), exist_ok=True)
    flow_by_id = {f['id']: f for f in D['flow']}
    outline = {'subjects': [dict(key=k, title=t, topics=[]) for k, t, _ in SUBJECTS]}
    stats = dict(videos=0, questions=0, cards=0)
    for top in D['topics']:
        t = int(top['id']); sections = []; passages = {}; minutes = 0; nv = nq = nl = 0
        for sid in top['sections']:
            sec = next(x for x in D['sections'] if x['id'] == sid)
            steps = []
            for fid in sec['items']:
                f = flow_by_id[fid]
                if f['type'] == 'video':
                    v = D['videos'][f['ref']]
                    st = dict(kind='video', id=v['id'], minutes=v.get('minutes'))
                    if v.get('questionId'):
                        n = qnum.get(v['questionId']); st.update(solution=True, questionId=v['questionId'], title='Worked solution' + (' · Question %d' % n if n else ''))
                    else:
                        st['title'] = v.get('navLabel') or v['title']
                    steps.append(st); minutes += v.get('minutes') or 0; nv += 1; nl += 0 if v.get('questionId') else 1
                elif f['type'] == 'question':
                    q = D['questions'][f['ref']]
                    st = dict(kind='question', id=q['id'], stem=tex(q['stemRich']), choices=[tex(c) for c in q['choicesRich']],
                              correct=q['correct'][0], explanation=[tex(e) for e in (q.get('explanation') or [])])
                    if q['id'] in qnum: st['number'] = qnum[q['id']]
                    if (q.get('questionVisual') or {}).get('type') == 'geometry': st['figure'] = q['questionVisual']['svg']
                    if q.get('passageId'):
                        st['passageId'] = q['passageId']; p = D['passages'][q['passageId']]
                        passages[q['passageId']] = dict(title=p.get('title', ''), paragraphs=p['paragraphs'])
                    if sec['kind'] == 'practice' and q.get('practiceGroup') and q['practiceGroup'] != 'None': st['group'] = q['practiceGroup']
                    ins = instructions(q, t)
                    if ins: st['instructions'] = ins
                    steps.append(st); nq += 1
                else:
                    r = D['references'][f['ref']]
                    steps.append(dict(kind='card', id=f['ref'], title=r['title'], intro=tex(r.get('intro', '')),
                                      tables=[dict(title=tex(tb.get('title', '')), head=[tex(h) for h in (tb.get('head') or [])],
                                                   rows=[[tex(c) for c in row] for row in (tb.get('rows') or [])]) for tb in (r.get('tables') or [])],
                                      tips=[tex(x) for x in (r.get('tips') or [])]))
                    stats['cards'] += 1
            sections.append(dict(id=sid, title=sec['title'], kind=sec['kind'], steps=steps))
        doc = dict(id=t, title=top['title'], subject=subject_of(t), sections=sections, passages=passages)
        json.dump(doc, open(os.path.join(OUT, 'topics', 't%d.json' % t), 'w'), ensure_ascii=False, separators=(',', ':'))
        subj = next(s for s in outline['subjects'] if s['key'] == subject_of(t))
        subj['topics'].append(dict(id=t, title=top['title'], videos=nv, lessons=nl, questions=nq, minutes=round(minutes),
                                   steps=sum(len(s['steps']) for s in sections)))
        stats['videos'] += nv; stats['questions'] += nq
    json.dump(outline, open(os.path.join(OUT, 'outline.json'), 'w'), ensure_ascii=False, indent=1)
    man = os.path.join(OUT, 'video-manifest.json')
    if not os.path.exists(man):
        json.dump({'_about': 'videoId -> {provider: "bunny", libraryId, videoGuid} or {provider: "url", url}. Missing = coming soon.'},
                  open(man, 'w'), indent=1)
    print('exported', stats, '→', OUT)

if __name__ == '__main__':
    main()
