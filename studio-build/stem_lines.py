"""The asked part of a question goes on its own line (teacher request 2026-10-06).

"Given: $a^4 = a^3 b$. $b = ?$"  ->  "Given: $a^4 = a^3 b$\n$b = ?$"
"m and n are opposite numbers. $m + n = ?$"  ->  "m and n are opposite numbers.\n$m + n = ?$"

Same layout as the real NITE booklets: the given / the sentence on one line, "x = ?" on the line below. A sentence
keeps its punctuation ("2% of W is 10." / "W = ?", "Based on this information and the information in the figure," /
"α = ?"), but a given that ends in a FORMULA loses its period (teacher 2026-10-06: in "...= \\pi x^2$. $x = ?$" the
period reads as a multiplication dot; the real booklets end such a line with the formula: "Given: a^{2x} = 8 , 0 < a").

Applied by build_verbal.py after the math patches, modules, terminology and no_question_numbers, so it covers every
topic. Conservative: only a stem whose LAST line ends with  <sentence>. $expr = ?$  or  <sentence>, $expr = ?$
(the asked part a whole TeX span ending in "?") is split. "= ?" inside a sentence ("What is $a\\cdot b$?"),
stems already on their own line, tables and answer choices are left alone. Verbal topics have no such stems.

Boards in solution videos / lessons:
- a board item {k:'q', qid} draws the question's stemRich, so unrecorded videos get the new layout by themselves;
  an item that carries its own 'stem' text in an unrecorded video is split the same way.
- a plain board text line {k:'t'} of the same shape ("$4x+6y=18$. $6x+9y=?$") is split too, unrecorded videos only.
- stems already on two lines ("Given: $c\\ne d$.\\n$...=?$") lose the period after a formula the same way.
- RECORDED videos (any take in ~/Documents/Course.recordings, studio_done.takes()) must keep their board exactly:
  their q items for a changed question get the OLD stem pinned in item['stem'] (the renderer draws it.stem first),
  so the slide is drawn byte-for-byte as before. Nothing else in those videos changes.
"""
import re
import math_api, studio_done

ASK = re.compile(r'([.,])(?:[ \t]+|[ \t]*\n)(\$[^$\n]*\?\s*\$)(\s*)$')   # "\n": already on its own line
FORMULA = re.compile(r'[=<>+\-^]|\\(?:ne|neq|le|leq|ge|geq|frac|sqrt|cdot|times|div|begin)(?![a-zA-Z])')


def split(stem):
    """stem with the asked part moved to its own line, or None if the stem doesn't qualify."""
    if not isinstance(stem, str):
        return None
    m = ASK.search(stem)
    if not m:
        return None
    head = stem[:m.start()]
    line = head.rsplit('\n', 1)[-1]
    if not line.strip() or head.count('$') % 2:      # nothing before it on the line / we are inside a TeX span
        return None
    punct = m.group(1)
    last = re.search(r'\$([^$]*)\$$', head)          # no period right after a FORMULA: "... = \pi x^2$." reads as a
    if punct == '.' and last and FORMULA.search(last.group(1)):   # multiplication dot before "x = ?" (teacher, q-185);
        punct = ''                                   # a sentence ending in a number / letter keeps it ("... is $50$.")
    new = head + punct + '\n' + m.group(2) + m.group(3)
    return None if new == stem else new              # an already-split stem changes only if its period goes


def apply(D, recorded=None):
    rec = set(studio_done.recorded_ids() if recorded is None else recorded)
    st = dict(stems=[], boards=set(), pinned=set(), pinned_items=0, own_stem_items=0, text_items=[])
    old = {}
    for qid, q in D['questions'].items():
        new = split(q.get('stemRich'))
        if new is None:
            continue
        old[qid] = q['stemRich']
        q['stemRich'] = new
        q['stemHtml'] = math_api.rich_html(new)
        st['stems'].append((qid, old[qid], new))
    for vid, v in D['videos'].items():
        for b in v.get('beats') or []:
            for it in b.get('items') or []:
                if it.get('k') == 't' and vid not in rec:    # a lesson board line "<given>. $x=?$" (unrecorded only)
                    new = split(it.get('t'))
                    if new is not None:
                        it['t'] = new; st['boards'].add(vid); st['text_items'].append((vid, new))
                if it.get('k') != 'q':
                    continue
                if vid in rec:
                    if it.get('qid') in old and not it.get('stem'):
                        it['stem'] = old[it['qid']]; st['pinned'].add(vid); st['pinned_items'] += 1
                    continue
                if it.get('stem'):
                    new = split(it['stem'])
                    if new is not None:
                        it['stem'] = new; st['boards'].add(vid); st['own_stem_items'] += 1
                elif it.get('qid') in old:
                    st['boards'].add(vid)
    return st


def report(st):
    return ('asked part on its own line: %d stems; %d unrecorded videos show it on the board (%d items with their own stem, %d text lines); '
            '%d recorded videos keep the old board (%d items pinned)'
            % (len(st['stems']), len(st['boards']), st['own_stem_items'], len(st['text_items']), len(st['pinned']), st['pinned_items']))
