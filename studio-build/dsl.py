"""Slide-writing helpers for hybrid modules (same conventions as the Algebra/Word Problems/Geometry modules).

Script lines: plain string = spoken line · A(label, item) = [APPEAR] pop-in · D(text) = [DRAW] teacher annotation.
Items: H (heading) · T (rich text, $TeX$ allowed) · Q (question, pre-loaded) · PSG (reading passage).
"""

def T(t, size=46, x=None, y=None, w=None, **k):
    d = dict(k='t', t=t, size=size, **k)
    if x is not None: d['x'] = x
    if y is not None: d['y'] = y
    if w is not None: d['w'] = w
    return d

def H(t, size=60, **k): return dict(k='h', t=t, size=size, **k)
def A(label, item): return ('A', label, item)
def D(text): return ('D', text)

def Q(qid, **k):
    """Pre-loaded question. Verbal questions use the text layout (tq=True): stem on top, answers as wrapped full-width rows."""
    return dict(k='q', qid=qid, **k)

def VQ(qid, **k): return Q(qid, tq=True, **k)

def PSG(pid, paras=None, **k):
    """Reading passage with numbered paragraphs. paras = list of 1-based paragraph numbers (None = all)."""
    d = dict(k='psg', pid=pid, **k)
    if paras: d['paras'] = list(paras)
    return d

# pop-in below the question text, full width (auto-stacks under the stem and earlier pop-ins)
def P(t, size=34, y=120, x=410, w=1140): return T(t, size=size, x=x, y=y, w=w)

def lesson(id, title, sidebar, slides, topic):
    """slides: list of dict(mode='title'|'concept', title=…, active=…, script=[…], src='hebrew'?)"""
    return dict(id=id, num=0, title=title, sidebar=sidebar, slides=slides, topic=topic, kind='lesson')

def guided(i, qid, group_title, sidebar, intro, slides, topic, q=None):
    """One guided question (i = 0-based index inside its group). slides: [(title, script) …] or (title, script, extra_q_opts)."""
    out = [dict(mode='title', title='Question %d' % (i + 1), script=intro)]
    for s in slides:
        t, script = s[0], s[1]
        extra = dict(q or {}, **(s[2] if len(s) > 2 else {}))
        pre = extra.pop('pre', None) or [VQ(qid, **extra)]      # e.g. pre=[PSG(pid, [2])] for a passage slide
        out.append(dict(mode='question', active=i, title=t, pre=pre, script=script))
    return dict(id='solve-' + qid, num=0, title=group_title, sidebar=sidebar, slides=out, guided=i + 1,
                qid=qid, topic=topic, kind='solution')
