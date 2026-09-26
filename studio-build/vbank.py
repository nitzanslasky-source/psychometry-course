"""Verbal question bank (content/verbal_bank_all.json) → course questions, per-topic pools.

Question ids: 'vb-<bank id>' (e.g. vb-inf_v2_0001); reading passages: 'vbp-01'…, their questions 'vb-rc01-1'….
Trust rank (lower = better): 1 NITE key · 2 real exam / real English paper · 3 keyed with explanation ·
4 solved by Claude (verify) · 5 inf_v1 written from scratch (review). Unanswered / broken items are excluded.
"""
import json, os, re, html

BANK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'verbal_bank_all.json')
_B = json.load(open(BANK, encoding='utf-8'))

TOPIC_OF = {  # bank category → course topic
    'Sentence Completion': 41,
    'Claims and Logic': 42, 'necessary-conclusion': 42, 'contradiction': 42, 'logic-puzzle': 42,
    'Sentence Understanding': 43, 'clause': 43, 'meaning/equivalence': 43,
    'Paragraph Understanding': 44, 'other': 44, 'inference': 44, 'implication': 44,
    'Parables and Comparisons': 45, 'example-of-concept': 45,
    'Strengthen / Weaken': 46, 'weaken': 46, 'strengthen': 46, 'assumption': 46,
    'Scientific Thinking': 47, 'explain-findings': 47,
    'Rules and Arrangements': 48,
}

def trust_rank(x):
    t = str(x.get('trust', ''))
    if x['set'] == 'inf_v1': return 5
    if 'verify' in t: return 4
    if 'NITE published key' in t: return 1
    if 'real-exam' in t or 'real exam' in t or 'real English paper' in t: return 2
    return 3

HEB = re.compile(r'[֐-׿]')
EXCLUDE = {'inf_mix_0024', 'inf_mix_0063', 'inf_mix_0074', 'inf_v1_0348', 'inf_v2_0010'}   # junk choices / needs figure / two correct answers (found by writers)

# Only two sources are used (teacher's decision, 2026-09-26):
#  inf_v2 — English questions each rebuilt one-for-one from a real NITE exam question
#  sc_tr  — sentence completions translated from Hebrew exams whose answers MATCH the official NITE key
def approved(x):
    return x['set'] == 'inf_v2' or (x['set'] == 'sc_tr' and 'matches NITE published key' in str(x.get('trust', '')))

def usable(x):
    if not approved(x): return False
    if x['id'] in EXCLUDE: return False
    if x['set'] == 'inf_mix' and x['category'] == 'inference': return False   # sentence completions with the blanks stripped
    if x.get('answer') in (None, '', 0) or len(x.get('options', [])) != 4: return False
    txt = x['stem'] + ' '.join(x['options'])
    if HEB.search(txt): return False                                   # stray Hebrew
    if re.search(r'accompanying (figure|table|drawing)|see figure', txt, re.I): return False   # figure not in the bank
    return True

def _h(s): return html.escape(s, quote=False)

def _q(qid, topic, stem, options, ans, expl, extra):
    stem = ' ' + stem.strip() + ' '
    q = dict(id=qid, topic=str(topic), unit='vr%d-bank' % topic, stem=stem, stemRich=stem, stemHtml=_h(stem),
             choices=list(options), choicesRich=list(options), choicesHtml=[_h(o) for o in options],
             correct=[ans - 1], explanation=[expl] if expl else [], answerHtml=('<p>%s</p>' % _h(expl)) if expl else '',
             work=[], workText=[], methods=[], subject='verbal-reasoning', revisedExample=False,
             navLabel=re.sub(r'\s+', ' ', stem).strip()[:160])
    q.update(extra); return q

def questions():
    """→ (questions dict, pools {topic: [qid…] sorted by trust}, passages dict, rc_pool [qid…])"""
    Q, pools = {}, {}
    for x in _B['items']:
        t = TOPIC_OF.get(x['category'])
        if t is None or not usable(x): continue
        qid = 'vb-' + x['id']; r = trust_rank(x)
        Q[qid] = _q(qid, t, x['stem'], x['options'], int(x['answer']), x.get('explanation') or '',
                    dict(bankSet=x['set'], bankTrust=x.get('trust', ''), trustRank=r, bankCategory=x['category'],
                         reviewFlag=r >= 4))
        pools.setdefault(t, []).append(qid)
    SETORD = {'inf_v2': 0, 'sc_tr': 1, 'sc_v2': 2, 'inf_mix': 3, 'sc_en': 4, 'inf_v1': 5}   # inf_v2 = strongest set
    for t in pools: pools[t].sort(key=lambda q: (Q[q]['trustRank'], SETORD.get(Q[q]['bankSet'], 9), q))
    # near-duplicates across sets (same question re-sourced): keep the best-trusted copy
    toks = {q: set(re.findall(r'[a-z]{3,}', Q[q]['stem'].lower())) for q in Q}
    for t in pools:
        keep = []
        for q in pools[t]:
            if any(len(toks[q] & toks[k]) / max(1, len(toks[q] | toks[k])) > .6 for k in keep): Q.pop(q); continue
            keep.append(q)
        pools[t] = keep
    P, rc = {}, []
    for n, p in enumerate(_B['reading_comprehension'], 1):
        pid = 'vbp-%02d' % n
        paras = [re.sub(r'\s+', ' ', s).strip() for s in re.split(r'\n\s*\n', p['passage']) if s.strip()]
        P[pid] = dict(id=pid, title='Passage %d' % n, paragraphs=paras, group='bank',
                      source=p['source'], glossary=p.get('glossary') or '')
        for k, qq in enumerate(p['questions'], 1):
            key = qq.get('key')
            if key in (None, '', 0) or len(qq.get('options', [])) != 4: continue
            qid = 'vb-rc%02d-%d' % (n, k)
            stem = line_refs_to_paragraphs(qq['stem'], paras)
            if stem is None or re.search(r'\b(graphs?|charts?|diagrams?)\b', stem, re.I): continue
            Q[qid] = _q(qid, 49, stem, qq['options'], int(key), qq.get('explanation') or '',
                        dict(passageId=pid, bankSet='rc', bankTrust=p.get('trust', ''), trustRank=3,
                             bankCategory='Reading Comprehension', reviewFlag=False, readingNumber=str(n)))
            rc.append(qid)
    # ORIGINAL questions written for the course (content/verbal_originals_*.json). Each mirrors the type, trap and
    # difficulty of one real NITE question (field "mirrors", internal) with entirely new content.
    import glob as _g
    for f in sorted(_g.glob(os.path.join(os.path.dirname(BANK), 'verbal_originals_*.json'))):
        doc = json.load(open(f, encoding='utf-8'))
        for x in doc.get('items', []):
            Q[x['id']] = _q(x['id'], x['topic'], x['stem'], x['options'], int(x['answer']), x.get('explanation', ''),
                            dict(bankSet='original', bankTrust='original, mirrors ' + x.get('mirrors', ''), trustRank=0,
                                 bankCategory=x.get('category', ''), reviewFlag=False, original=True))
            if x.get('pool', True): pools.setdefault(x['topic'], []).insert(0, x['id'])
        for n, p in enumerate(doc.get('passages', []), 1):
            P[p['id']] = dict(id=p['id'], title=p.get('title', 'Passage'), paragraphs=p['paragraphs'], group='original', source='original', glossary='')
            for k, qq in enumerate(p['questions'], 1):
                qid = '%s-%d' % (p['id'], k)
                Q[qid] = _q(qid, 49, qq['stem'], qq['options'], int(qq['answer']), qq.get('explanation', ''),
                            dict(passageId=p['id'], bankSet='original', bankTrust='original passage', trustRank=0,
                                 bankCategory='Reading Comprehension', reviewFlag=False, original=True, readingNumber=p['id']))
                rc.insert(0, qid)
    # Practice uses ORIGINALS ONLY wherever a topic has them: the bank's items are translations of real NITE questions.
    for t in pools:
        if any(Q[q].get('original') for q in pools[t]): pools[t] = [q for q in pools[t] if Q[q].get('original')]
    if any(Q[q].get('original') for q in rc): rc = [q for q in rc if Q[q].get('original')]
    _k = lambda q: [int(n) for n in re.findall(r'\d+', q)]
    for t in pools: pools[t].sort(key=lambda q: (not Q[q].get('original'), _k(q) if Q[q].get('original') else 0))
    rc.sort(key=lambda q: (not Q[q].get('original'), _k(q) if Q[q].get('original') else 0))
    return Q, pools, P, rc

def _para_of(stem, paras):
    for q in re.findall(r'["“\']([^"”\'…]{6,}?)(?:\s*…|["”\'])', stem):
        probe = q.strip()[:40].lower()
        for i, p in enumerate(paras, 1):
            if probe and probe in p.lower(): return i
    return None

def line_refs_to_paragraphs(stem, paras):
    """Exam line numbers can't be reproduced on screen: point to the paragraph holding the quoted words instead.
    Returns None when the reference can't be resolved (the question is then left out)."""
    if not re.search(r'\blines? \d', stem): return stem
    n = _para_of(stem, paras)
    if n is None: return None
    stem = re.sub(r'\s*\(lines? [\d–\-, ]+\)', ' (paragraph %d)' % n, stem)
    stem = re.sub(r'\b(?:in |mentioned in |described in )?lines? \d+(?:\s*[–-]\s*\d+)?', 'in paragraph %d' % n, stem)
    stem = re.sub(r'\b([Ii])n in paragraph', r'\1n paragraph', stem)
    return stem

if __name__ == '__main__':
    Q, pools, P, rc = questions()
    print(len(Q), 'questions ·', {t: len(v) for t, v in sorted(pools.items())}, '· passages', len(P), '· RC questions', len(rc))
    from collections import Counter
    print({t: dict(Counter(Q[q]['trustRank'] for q in v)) for t, v in sorted(pools.items())})
