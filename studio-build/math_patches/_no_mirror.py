"""2026-10-11 teacher decision: the "mirror test" is removed from the whole course (topic 13 lesson + its question, and
the "Mirror test" method lines that were spread to written solutions in topics 3, 8, 13, 16 and 30).
drop_lines(M, qid, prefixes, replace=None): remove the explanation lines that start with one of the prefixes (each prefix
must match exactly one line); `replace` lines go where the first removed line was."""


def drop_lines(M, qid, prefixes, replace=None):
    ex = list(M.q(qid)['explanation'])
    hit = []
    for p in prefixes:
        ks = [k for k, e in enumerate(ex) if e.startswith(p)]
        assert len(ks) == 1, (qid, p, ks)
        hit.append(ks[0])
    first = min(hit)
    out = []
    for k, e in enumerate(ex):
        if k == first and replace: out.extend(replace)
        if k not in hit: out.append(e)
    assert not any('mirror' in e.lower() for e in out), (qid, out)
    M.set_q(qid, expl=out)
