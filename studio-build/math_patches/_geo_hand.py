"""Handwriting for geometry worked lines (2026-10-18, teacher via Codex: "handwriting wherever practical" in ALL geometry
lessons - worked calculations, equations, substitutions, intermediate results; question text, figures, titles and tables
stay typed).

auto(vid, item) -> the hand-written text (studio_handwrite.py syntax) for a typed math board line, or None (stays typed).
Only in handwriting renders (AI_HANDWRITE, as before) is a 'write' cue drawn by hand; the studio itself keeps the typed item.

FROZEN = the geometry videos that were already rendered (Done / Check) on 18 Oct 2026: the teacher chose "only videos not
made yet", so their boards stay exactly as rendered (_geo_hand_frozen.json, a fixed snapshot - never regenerate it, or
videos rendered later WITH handwriting would lose it)."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import studio_handwrite as HWR

FROZEN = set(json.load(open(os.path.join(HERE, '_geo_hand_frozen.json')))['ids'])

_CMD = [('\\blacklozenge', '◆'), ('\\cdot', '·'), ('\\times', '×'), ('\\div', '÷'), ('\\pm', '±'),
        ('\\neq', '≠'), ('\\ne', '≠'), ('\\leq', '≤'), ('\\le', '≤'), ('\\geq', '≥'), ('\\ge', '≥'), ('\\approx', '≈'),
        ('\\Leftrightarrow', '⇔'), ('\\leftrightarrow', '↔'), ('\\Rightarrow', '⇒'), ('\\rightarrow', '→'), ('\\to', '→'), ('\\leftarrow', '←'),
        ('\\angle', '∠'), ('\\triangle', '△'), ('\\perp', '⊥'), ('\\parallel', '∥'),
        ('\\alpha', 'α'), ('\\beta', 'β'), ('\\gamma', 'γ'), ('\\delta', 'δ'), ('\\theta', 'θ'), ('\\pi', 'π'),
        ('\\qquad', '      '), ('\\quad', '    '), ('\\enspace', '  '), ('\\;', ' '), ('\\:', ' '), ('\\ ', ' '),
        ('\\,', ''), ('\\!', ''), ('\\left', ''), ('\\right', ''), ('\\displaystyle', '')]


def _group(t, i):
    """t[i] == '{' -> (inside, index after the matching '}')"""
    d = 0
    for j in range(i, len(t)):
        if t[j] == '{': d += 1
        elif t[j] == '}':
            d -= 1
            if d == 0: return t[i + 1:j], j + 1
    raise ValueError('unbalanced')


def _conv(t):
    out = []; i = 0
    while i < len(t):
        m = re.match(r'\\[dt]?frac\s*', t[i:])
        if m:                                                     # \frac{a}{b}, \frac12, \frac a2, \frac3{10}
            j = i + m.end(); args = []
            for _ in range(2):
                while j < len(t) and t[j] == ' ': j += 1
                if j < len(t) and t[j] == '{': x, j = _group(t, j)
                elif j < len(t): x, j = t[j], j + 1
                else: raise ValueError('frac')
                args.append(_conv(x))
            out.append('{%s/%s}' % tuple(args)); i = j; continue
        if t.startswith('\\sqrt{', i):
            a, j = _group(t, i + 5); out.append('√{%s}' % _conv(a)); i = j
        elif re.match(r'\\sqrt\s*\d', t[i:]):
            m = re.match(r'\\sqrt\s*(\d)', t[i:]); out.append('√{%s}' % m.group(1)); i += m.end()
        elif t.startswith('\\hl{', i):
            n, j = _group(t, i + 3); a, k = _group(t, j); out.append('\\hl{%s}{%s}' % (n, _conv(a))); i = k
        elif re.match(r'\\(text|mathrm|textbf|mathbf|operatorname)\{', t[i:]):
            a, j = _group(t, t.index('{', i)); out.append(_conv(a)); i = j
        elif re.match(r'\^\{?\\circ\}?', t[i:]):
            m = re.match(r'\^\{?\\circ\}?', t[i:]); out.append('°'); i += m.end()
        elif t.startswith('\\circ', i):
            out.append('°'); i += 5
        elif t.startswith('^{', i):
            a, j = _group(t, i + 1); out.append('^{%s}' % _conv(a)); i = j
        else:
            for a, b in _CMD:
                if t.startswith(a, i) and not (a[-1].isalpha() and i + len(a) < len(t) and t[i + len(a)].isalpha()):
                    out.append(b); i += len(a); break
            else:
                out.append(t[i]); i += 1
    return ''.join(out)


def hand(tex):
    """the hand-written twin of a typed line, or None if the pen can't write it"""
    if '$' not in tex: return None                               # plain words: stay typed
    words = re.findall(r'[A-Za-z]{2,}', re.sub(r'\$[^$]*\$', ' ', tex))
    if len(words) > 4: return None                               # a sentence / key line, not a worked line: stays typed
    t = tex.replace('²', '^2').replace('³', '^3').replace('√', '\\sqrt')
    try:
        t = _conv(t)
    except ValueError:
        return None
    t = t.replace('$', '').replace('-', '−').replace('{', '{').strip()
    t = re.sub(r'\s{7,}', '      ', t)
    if '\\' in t.replace('\\hl{', '') or '_' in t or '&' in t or '\n' in t: return None
    try:
        HWR.write(t); return t
    except Exception:
        return None


# slides (1-based) whose handwritten lines would overflow or overlap (math_check with AI_HANDWRITE=all): stay typed
NOHAND = {('solve-geo32-g068', 1), ('solve-geo32-g068', 2), ('solve-geo32-g071', 3), ('solve-geo32-g059', 2),
          ('solve-geo32-g048', 2), ('geo-081', 9)}


def auto(vid, it, si=None):
    if vid in FROZEN or it.get('k') != 't' or it.get('_typed'): return None
    if si is not None and (vid, si + 1) in NOHAND: return None
    return hand(it.get('t', ''))
