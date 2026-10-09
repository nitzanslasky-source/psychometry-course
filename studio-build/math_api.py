"""Editing API for the Algebra / Word Problems / Geometry content baked into base-v18.html.

Math fixes are written as patch files math_patches/tNN.py, each defining apply(M). build_verbal.py (and math_check.py)
load the base, call every patch, then M.finish(). All text uses "rich" form: plain words with $TeX$ inline.

Questions
  M.q(qid)                          -> the question dict (read)
  M.set_q(qid, stem=, choices=, correct=, expl=, figure=)   rewrite; every derived field is regenerated.
        stem: str, choices: [4 str], correct: 1-based int, expl: [str, ...] (worked solution paragraphs),
        figure: svg string (geometry) or None to remove. Omitted args keep their value.
  M.new_q(qid, topic, stem, choices, correct, expl, figure=None)   create (not placed yet)
  M.place_q(qid, section, after=None, before=None)   put a question into a section's flow
        after/before = a flow ref (question id / video id / card id); default = end of section
  M.move(ref, section, after=None, before=None)  move a question/video/card (also into another topic) without deleting it
  M.section_title(section, title)   rename a section
  M.unplace(ref)                    remove a question/video/card from flow (question data is dropped too)
  M.section_of(ref) -> section id of a question/video/card;  M.sections_of_topic(t) -> [(id, kind, title)]
  M.practice_order(section, [qid, ...])  reorder the questions of a section (ids not listed keep their order at the end)

Videos and slides (slide numbers are 1-based, as shown in the review files)
  M.video(vid)                      -> video dict;  M.slide(vid, n) -> beat dict (read)
  M.set_slide(vid, n, title=, script=, pre=, mode=, active=)   rebuild one slide. script uses the DSL of dsl.py:
        plain str = spoken line · A(label, item) = pop-in item appears · D(text) = teacher draws/writes.
        Items: T(text, size=46) · H(heading) · Q(qid) (question on the board) · VIS(svg) (figure).
        pre = items already on the canvas when the slide loads (default: keep the slide's current pre items).
  M.edit_lines(vid, n, fn)          fn(list_of_line_dicts) -> new list (small wording edits keep items)
  M.insert_slides(vid, after_n, [slide, ...])   slide = dict(title=, mode='concept'|'question'|'title', active=, pre=[], script=[])
  M.remove_slides(vid, [n, ...])     M.move_slide(vid, n, to_n)
  M.set_sidebar(vid, [labels])      sidebar of the video (slide 'active' indexes into it)
  M.new_video(vid, topic, title, sidebar, slides, section, after=None, before=None, kind='lesson', qid=None)
        kind='solution' + qid = worked-solution video for a guided question; it is placed right after its question.
        Guided questions: M.new_q(...) + M.place_q(...) + M.new_video(..., kind='solution', qid=...).
        Title slide of a solution video: dict(mode='title', title='Question N', script=[...]) - use the next free N
        in the topic (M.next_question_number(topic)).

Memory cards
  M.card(cid)                       -> card dict (title, intro, tables=[{title, head, rows}], tips=[...]) editable in place
  M.new_card(cid, topic, section, card, after=None)

Helpers:  T, H, A, D, Q, PT, VIS (from dsl; PT = [POINT] highlight cue, see studio_autonarrate.py), M.find_text(regex, topics) for searching.
"""
import copy, html as _html, re
from dsl import T, H, A, D, Q, PT

def VIS(svg, **k): return dict(k='vis', v={'type': 'geometry', 'svg': svg}, **k)

def _esc(s): return _html.escape(str(s), quote=True)

def rich_html(s):
    """rich text ($TeX$ inline) -> studio HTML (same as the studio's md())."""
    out = []
    for p in re.split(r'(\$[^$]+\$)', str(s)):
        if len(p) > 1 and p[0] == '$' and p[-1] == '$': out.append('<span class="math" data-tex="%s"></span>' % _esc(p[1:-1]))
        else: out.append(_esc(p).replace('\n', '<br>'))
    return ''.join(out)

def rich_plain(s):
    return re.sub(r'\s+', ' ', str(s).replace('$', '')).strip()


class MathCourse:
    def __init__(self, D):
        self.D = D
        self.sections = {s['id']: s for s in D['sections']}
        self.touched_videos = set()
        self.touched_questions = set()
        self.log = []

    # ---------------- questions ----------------
    def q(self, qid): return self.D['questions'][qid]

    def _derive(self, q):
        q['stemRich'] = q['stemRich']
        q['stem'] = rich_plain(q['stemRich'])
        q['stemHtml'] = rich_html(q['stemRich'])
        q['choices'] = [rich_plain(c) for c in q['choicesRich']]
        q['choicesHtml'] = [rich_html(c) for c in q['choicesRich']]
        q['navLabel'] = rich_plain(re.sub(r'\\begin\{(cases|aligned)\}.*?\\end\{(cases|aligned)\}', '…', q['stemRich'], flags=re.S).replace('\n', ' '))[:120]
        ex = q.get('explanation') or []
        q['answerHtml'] = ''.join('<p>%s</p>' % rich_html(e) for e in ex)
        q['work'] = []; q['workText'] = []
        q['methods'] = [{'title': 'Worked solution', 'steps': list(ex), 'work': [], 'independent': False, 'board': []}]

    def set_q(self, qid, stem=None, choices=None, correct=None, expl=None, figure=Ellipsis):
        q = self.q(qid)
        if stem is not None: q['stemRich'] = stem
        if choices is not None:
            assert len(choices) == 4, qid + ': need 4 choices'
            q['choicesRich'] = list(choices)
        if correct is not None:
            assert 1 <= correct <= 4, qid; q['correct'] = [correct - 1]
        if expl is not None: q['explanation'] = [expl] if isinstance(expl, str) else list(expl)
        if figure is not Ellipsis:
            if figure: q['questionVisual'] = {'type': 'geometry', 'svg': figure}
            else: q.pop('questionVisual', None)
        self._derive(q); self.touched_questions.add(qid)
        # keep pre-loaded copies of the stem on slides in sync
        for v in self.D['videos'].values():
            for b in v.get('beats', []):
                for it in b.get('items', []):
                    if it.get('k') == 'q' and it.get('qid') == qid and 'stem' in it: it['stem'] = q['stemRich']
        return q

    def new_q(self, qid, topic, stem, choices, correct, expl, figure=None):
        assert qid not in self.D['questions'], 'exists: ' + qid
        self.D['questions'][qid] = {'id': qid, 'topic': topic, 'unit': None, 'stemRich': stem, 'choicesRich': list(choices),
                                    'correct': [correct - 1], 'explanation': [], 'source': 'Course review 2026-09', 'methods': []}
        return self.set_q(qid, expl=expl, figure=figure)

    # ---------------- flow ----------------
    def _flow_index(self, ref):
        for k, f in enumerate(self.D['flow']):
            if f['ref'] == ref: return k
        raise KeyError('not in flow: %s' % ref)

    def _insert_flow(self, typ, ref, section, after=None, before=None):
        sec = self.sections[section]; flow = self.D['flow']
        fid = 'flow-%s-%s-%s' % (section, typ[0], ref)
        entry = {'id': fid, 'topic': sec['topic'], 'section': section, 'type': typ, 'ref': ref}
        if after is not None: k = self._flow_index(after) + 1
        elif before is not None: k = self._flow_index(before)
        else:
            ks = [n for n, f in enumerate(flow) if f['section'] == section]
            k = ks[-1] + 1 if ks else len(flow)
        flow.insert(k, entry)
        prev = next((flow[j]['id'] for j in range(k - 1, -1, -1) if flow[j]['section'] == section), None)
        items = sec['items']
        items.insert(items.index(prev) + 1 if prev in items else 0, fid)
        if typ == 'question':
            self.D['questions'][ref]['unit'] = section
            sec['questionCount'] = sum(1 for f in flow if f['section'] == section and f['type'] == 'question')
        return fid

    def section_of(self, ref):
        return self.D['flow'][self._flow_index(ref)]['section']

    def sections_of_topic(self, topic):
        return [(s['id'], s['kind'], s['title']) for s in self.D['sections'] if s['topic'] == topic]

    def place_q(self, qid, section, after=None, before=None):
        return self._insert_flow('question', qid, section, after, before)

    def unplace(self, ref):
        flow = self.D['flow']
        for f in [f for f in flow if f['ref'] == ref]:
            flow.remove(f); sec = self.sections[f['section']]
            if f['id'] in sec['items']: sec['items'].remove(f['id'])
            if f['type'] == 'question':
                sec['questionCount'] = sum(1 for g in flow if g['section'] == f['section'] and g['type'] == 'question')
        if ref in self.D['questions'] and not any(f['ref'] == ref for f in flow):
            # drop its solution video too
            for vid in [v for v, x in self.D['videos'].items() if x.get('questionId') == ref]: self.unplace(vid); self.D['videos'].pop(vid, None)
            self.D['questions'].pop(ref, None)

    def move(self, ref, section, after=None, before=None):
        """Move a question/video/card to another place (any topic's section) without deleting it."""
        k = self._flow_index(ref); f = self.D['flow'].pop(k); sec = self.sections[f['section']]
        if f['id'] in sec['items']: sec['items'].remove(f['id'])
        fid = self._insert_flow(f['type'], ref, section, after, before)
        if f['type'] == 'question':
            sec['questionCount'] = sum(1 for g in self.D['flow'] if g['section'] == f['section'] and g['type'] == 'question')
            self.D['questions'][ref]['topic'] = self.sections[section]['topic']
        return fid

    def section_title(self, section, title): self.sections[section]['title'] = title

    def practice_order(self, section, order):
        sec = self.sections[section]; flow = self.D['flow']
        ents = [f for f in flow if f['section'] == section]
        qs = [f for f in ents if f['type'] == 'question']
        rank = {q: n for n, q in enumerate(order)}
        qs_sorted = sorted(qs, key=lambda f: (rank.get(f['ref'], len(order)), qs.index(f)))
        it = iter(qs_sorted); new = [next(it) if f['type'] == 'question' else f for f in ents]
        pos = [k for k, f in enumerate(flow) if f['section'] == section]
        for k, f in zip(pos, new): flow[k] = f
        sec['items'] = [f['id'] for f in new]

    # ---------------- videos / slides ----------------
    def video(self, vid): return self.D['videos'][vid]
    def slide(self, vid, n): return self.video(vid)['beats'][n - 1]

    def _beat(self, v, sl):
        items = [dict(it) for it in sl.get('pre', [])]; pre = len(items); lines = []
        for x in sl['script']:
            if isinstance(x, str): lines.append({'say': x})
            elif x[0] == 'A': items.append(dict(x[2])); lines.append({'appear': len(items) - 1, 'label': x[1]})
            elif x[0] == 'P': lines.append(dict(x[1]))
            else: lines.append({'draw': x[1]})
        mode = sl.get('mode', 'concept')
        return {'title': sl.get('title', ''), 'layout': 'hybrid', 'mode': mode, 'active': sl.get('active', -1), 'items': items,
                'pre': pre, 'lines': lines, 'loads': '', 'canvas': '', 'src': 'html', 'number': 0,
                'bigTitle': sl.get('title') if mode == 'title' else None, 'nextCue': '', 'board': [], 'visual': None, 'script': ''}

    def set_slide(self, vid, n, title=None, script=None, pre=None, mode=None, active=None):
        v = self.video(vid); old = v['beats'][n - 1]
        keep = (old.get('bigTitle') or old['title']) if old['mode'] == 'title' else old['title']
        sl = {'title': keep if title is None else title, 'mode': old['mode'] if mode is None else mode,
              'active': old['active'] if active is None else active,
              'pre': old['items'][:old['pre']] if pre is None else pre}
        if script is None:
            script = []
            for l in old['lines']:
                if 'say' in l: script.append(l['say'])
                elif 'appear' in l: script.append(A(l['label'], old['items'][l['appear']]))
                elif 'point' in l: script.append(('P', dict(l)))
                else: script.append(D(l['draw']))
        sl['script'] = script
        v['beats'][n - 1] = self._beat(v, sl); self.touched_videos.add(vid)

    def edit_lines(self, vid, n, fn):
        b = self.slide(vid, n); b['lines'] = fn(b['lines']); self.touched_videos.add(vid)

    def insert_slides(self, vid, after_n, slides):
        v = self.video(vid)
        for k, sl in enumerate(slides): v['beats'].insert(after_n + k, self._beat(v, sl))
        self.touched_videos.add(vid)

    def remove_slides(self, vid, ns):
        v = self.video(vid)
        for n in sorted(ns, reverse=True): v['beats'].pop(n - 1)
        self.touched_videos.add(vid)

    def move_slide(self, vid, n, to_n):
        b = self.video(vid)['beats']; x = b.pop(n - 1); b.insert(to_n - 1, x); self.touched_videos.add(vid)

    def set_sidebar(self, vid, labels):
        self.video(vid).setdefault('hybrid', {})['sidebar'] = list(labels); self.touched_videos.add(vid)

    def next_question_number(self, topic):
        ns = [0]
        for v in self.D['videos'].values():
            if v['topic'] == topic and v.get('kind') == 'solution' and v.get('beats'):
                m = re.match(r'Question (\d+)', v['beats'][0].get('bigTitle') or '')
                if m: ns.append(int(m.group(1)))
        return max(ns) + 1

    def new_video(self, vid, topic, title, sidebar, slides, section, after=None, before=None, kind='lesson', qid=None):
        assert vid not in self.D['videos'], 'exists: ' + vid
        subj = 'ALGEBRA' if topic <= 20 else 'WORD PROBLEMS' if topic <= 29 else 'GEOMETRY'
        v = {'id': vid, 'topic': topic, 'title': title, 'kind': kind, 'beats': [], 'sourceFiles': ['course review 2026-09'],
             'wordCount': 0, 'minutes': 0, 'navLabel': title, 'hybrid': {'num': 0, 'title': title, 'sidebar': list(sidebar), 'subject': subj}}
        if qid: v['questionId'] = qid
        self.D['videos'][vid] = v
        v['beats'] = [self._beat(v, sl) for sl in slides]; self.touched_videos.add(vid)
        if kind == 'solution' and qid and after is None and before is None: after = qid
        self._insert_flow('video', vid, section, after, before)
        return v

    # ---------------- memory cards ----------------
    def card(self, cid): return self.D['references'][cid]

    def new_card(self, cid, topic, section, card, after=None):
        ref = {k: card[k] for k in ('title', 'intro', 'tables', 'tips') if k in card}
        ref.update(kind='memory', rows=[], example='')
        self.D['references'][cid] = ref
        self._insert_flow('reference', cid, section, after)

    # ---------------- search ----------------
    def find_text(self, rx, topics=range(1, 39)):
        out = []; r = re.compile(rx)
        for q in self.D['questions'].values():
            if q['topic'] in topics:
                for fld in ('stemRich', 'explanation', 'choicesRich'):
                    for t in (q.get(fld) if isinstance(q.get(fld), list) else [q.get(fld)]):
                        if t and r.search(str(t)): out.append(('q', q['id'], fld, t))
        for v in self.D['videos'].values():
            if v['topic'] in topics:
                for n, b in enumerate(v.get('beats', []), 1):
                    for l in b['lines']:
                        t = l.get('say') or l.get('draw') or l.get('label')
                        if t and r.search(t): out.append(('v', v['id'], n, t))
                    for it in b['items']:
                        if it.get('t') and r.search(it['t']): out.append(('item', v['id'], n, it['t']))
        return out

    # ---------------- finish ----------------
    def finish(self):
        for vid in self.touched_videos:
            v = self.D['videos'].get(vid)
            if not v: continue
            sb = v.get('hybrid', {}).get('sidebar', [])
            for n, b in enumerate(v['beats']):
                b['number'] = n + 1
                nxt = v['beats'][n + 1]['title'] if n + 1 < len(v['beats']) else None
                b['nextCue'] = '[NEXT SLIDE → %s]' % nxt if nxt else '[END VIDEO]'
                if b['mode'] == 'title':
                    b['loads'] = 'Clean title slide: the sidebar (nothing highlighted yet) and one massive centred title. Nothing else.'
                    b['canvas'] = 'Massive title — "%s"' % (b.get('bigTitle') or b['title'])
                elif b['mode'] == 'concept' and not b['pre']:
                    lab = sb[b['active']] if 0 <= b['active'] < len(sb) else b['title']
                    b['loads'] = 'Sidebar with "%s" highlighted; the main canvas is completely blank.' % lab; b['canvas'] = 'Blank'
                elif not b['loads']:
                    lab = sb[b['active']] if 0 <= b['active'] < len(sb) else b['title']
                    b['loads'] = 'Sidebar with "%s" highlighted; the items listed are already on the canvas.' % lab
                    b['canvas'] = 'Pre-loaded — ' + '; '.join(rich_plain(it.get('t', it.get('qid', 'figure'))) for it in b['items'][:b['pre']])
            words = sum(len(l['say'].split()) for b in v['beats'] for l in b['lines'] if 'say' in l)
            v['wordCount'] = words; v['minutes'] = round(words / 130, 1)
        self.D['meta']['videos'] = len(self.D['videos'])


_W = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
def _word(n):
    if n < 21: return _W[n]
    return {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty'}[n // 10] + ('-' + _W[n % 10] if n % 10 else '')
_NUMRX = r'(\d+|(?i:' + '|'.join(sorted({_word(k) for k in range(1, 60)}, key=len, reverse=True)) + r'))'
def _val(w): return int(w) if w.isdigit() else next(k for k in range(1, 60) if _word(k) == w.lower())

def renumber_guided(D, topics=range(1, 39)):
    """Number each math topic's guided questions 1, 2, 3 ... in course order (nothing is recorded yet) and update
    title slides, video titles, sidebars and spoken/written 'Question N' references inside that topic's videos."""
    for t in topics:
        vids = [f['ref'] for f in D['flow'] if f['topic'] == t and f['type'] == 'video']
        sol = [v for v in vids if D['videos'].get(v, {}).get('kind') == 'solution' and D['videos'][v].get('beats')
               and re.match(r'Question \d+$', D['videos'][v]['beats'][0].get('bigTitle') or '')]
        old = {v: int(D['videos'][v]['beats'][0]['bigTitle'].split()[1]) for v in sol}
        if len(set(old.values())) != len(old): pass   # duplicates: renumber anyway by order
        mp = {}; new = {}
        for k, v in enumerate(sol, 1): new[v] = k; mp.setdefault(old[v], k)
        if all(old[v] == new[v] for v in sol): continue
        def fix(x):
            def r(mo):
                n = _val(mo.group(2))
                if n not in mp: return mo.group(0)
                k = mp[n]; w = str(k) if mo.group(2).isdigit() else _word(k)
                if mo.group(2)[:1].isupper(): w = w.capitalize()
                return mo.group(1) + 'uestion ' + w
            return re.sub(r'\b([Qq])uestion ' + _NUMRX + r'\b', r, x)
        for v in set(vids):
            V = D['videos'].get(v)
            if not V: continue
            if v in new:
                b0 = V['beats'][0]; b0['bigTitle'] = 'Question %d' % new[v]
                if b0.get('title', '').startswith('Question '): b0['title'] = 'Question %d' % new[v]
                b0['canvas'] = 'Massive title — "Question %d"' % new[v]
            V['title'] = fix(V.get('title', ''))
            hy = V.get('hybrid') or {}
            if hy.get('sidebar'):
                lab = [fix(x) for x in hy['sidebar']]
                own = [b.get('active', -1) for b in V['beats']]
                if v in new and all(re.match(r'Question \d+$', x) for x in lab):
                    mine = 'Question %d' % new[v]; lab = sorted(set(lab), key=lambda x: int(x.split()[1]))
                    for b in V['beats']:
                        if b.get('active', -1) >= 0: b['active'] = lab.index(mine) if mine in lab else b['active']
                hy['sidebar'] = lab
            for bi, b in enumerate(V['beats']):
                if not (v in new and bi == 0): b['title'] = fix(b.get('title', ''))   # title slide already set above
                for l in b['lines']:
                    for key in ('say', 'draw', 'label'):
                        if key in l: l[key] = fix(l[key])
                if b.get('nextCue'): b['nextCue'] = fix(b['nextCue'])

def renumber_modules(D):
    """Module numbers per subject in course order: every lesson its own number; a run of consecutive solution
    videos of one guided group (same sidebar) shares one number. Only when all math topics are patched."""
    num = {}; last = {}
    for f in D['flow']:
        if f['type'] != 'video' or f['topic'] > 38: continue
        v = D['videos'].get(f['ref']); hy = (v or {}).get('hybrid')
        if not hy: continue
        subj = hy.get('subject')
        key = ('sol', f['section'], tuple(hy.get('sidebar') or [])) if v.get('kind') == 'solution' else ('lesson', f['ref'])
        if last.get(subj) != key: num[subj] = num.get(subj, 0) + 1; last[subj] = key
        hy['num'] = num[subj]

def apply_patches(D, only=None):
    """Import math_patches/tNN.py (all, or only the given topic numbers) and apply them."""
    import glob, importlib.util, os
    here = os.path.dirname(os.path.abspath(__file__))
    M = MathCourse(D)
    for f in sorted(glob.glob(os.path.join(here, 'math_patches', 't*.py'))):
        n = int(re.findall(r't(\d+)', os.path.basename(f))[0])
        if only and n not in only: continue
        spec = importlib.util.spec_from_file_location('mp_t%d' % n, f); mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod); mod.apply(M)
    M.finish()
    renumber_guided(D, only or range(1, 39))
    if not only: renumber_modules(D)
    return M
