"""Reading Studio prompter, DISPLAY ONLY (2026-10-15, teacher re-recording q-555 #149: "when a is the variable and when it's
just 'a', I don't know"). Runs AFTER the display registry / formatter (_codex_reading_display_20261012.py), on every
lesson's display text, cached registry displays included. Never used for take text, sidecars or alignment.

  tidy(s)  finishes the math that the formatter left half in words, so one expression is never half figures, half words:
           "diamond of a" -> ◆(a); "three over a" / "b over a" -> 3/a, b/a (the variable a too, only in math context);
           "3/a, divided by 3/b" -> 3/a ÷ 3/b; "3/a is smaller than 3" -> 3/a < 3; "b/a is two" -> b/a = 2;
           "a is one" -> a = 1.  Conservative: both sides must be operands; the article "a" is never an operand.
  mark(s)  wraps every single-letter math variable in \\ue010 … \\ue011; the page renders it as math italics
           (<i class="mv">, serif italic, its own colour). English words ("a" the article, "I") are never marked.
"""
import re

OPEN, CLOSE = '', ''
_NUMW = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve'.split())}
_NW = r'(?:' + '|'.join(_NUMW) + r')'
# words that can follow the VARIABLE a but never the article a ("a is", "a cancels", "a and b", "by a without flipping")
_AFTER_A = (r"(?:is|isn't|was|equals|cancels|could|can|can't|must|has|have|ends|goes|gets|stays|becomes|and|or|"
            r"(?:to|heart|star)\s+(?:[A-Za-z]\b(?!['’])|two\b|three\b|\d)|"
            r"(?:times|plus|minus),?\s+(?:[A-Za-z]\b|\d|−|\(|the\b|root\b|in brackets\b|zero\b|one\b|two\b|three\b|four\b|five\b|six\b|seven\b|eight\b|nine\b|ten\b)|over|divided|squared|cubed|to the|without|off|on|at|from|into|in|by|with|itself|would|will|doesn't|does|"
            r"are|aren't|isn't|than|as|so|but|then|for|we|you|appears|means|stands|comes|divides|grows|lies|sits|changes|needs|"
            r"cannot|should|might|may|gives|makes|keeps|leaves|plays|works|starts|ends)")
_MATHCH = '=+−×÷/<>≤≥≠()|√·²³⁴⁵⁶⁷⁸⁹⁰¹ⁿ⁻^'
_SUPS = '²³⁴⁵⁶⁷⁸⁹⁰¹ⁿ⁻'
_A_VAR = (r"(?<![A-Za-z_'’̅])[aA](?![\w'’̅])(?=\s*(?:[,.;:?!)=<>+−×÷/≤≥≠²³⁴⁵⁶⁷⁸⁹⁰ⁿ]|$)|\s+%s\b)" % _AFTER_A)
_LET = r"(?<![A-Za-z_'’̅])(?:[b-hj-zB-HJ-Z]|%s)(?![\w'’̅])" % _A_VAR       # one-letter operand (a / A only as a variable)
_ATOM = (r"(?:◆\([^()]{1,12}\)|\([^()]{1,20}\)|(?<![\w/])−?\d+(?:\.\d+)?(?:/\d+)?(?![\w/])|(?<![\w/])\d*%s[%s]*)" % (_LET, _SUPS))
_PIECE = r"(?:\d+|%s|\([^()]{1,20}\))" % _LET
_FRAC = r"(?:(?<![\w/])%s/%s(?![\w/]))" % (_PIECE, _PIECE)
_OPND = r"(?:%s|%s)" % (_FRAC, _ATOM)


def _num(w):
    return str(_NUMW[w.lower()]) if w.lower() in _NUMW else w


TWO_INPUT = re.compile(r"[Dd]iamond of [\w−]+(?:,| and) [\w−]+(?:,| is| equals| over| and|\.)")


def tidy(s, diamond=True):
    # Greek letters and pi as symbols (the board and the question show them so)
    s = re.sub(r"\b(?:the )?(theta|alpha|beta|pi)\b", lambda m: m.group(0)[:-len(m.group(1))] + {'theta': 'θ', 'alpha': 'α', 'beta': 'β', 'pi': 'π'}[m.group(1)], s)
    s = re.sub(r"π ([a-z])\b(?![\w'’])", r"π\1", s)
    # diamond of a / diamond of 2 / diamond of (a + 1)   (the operation symbol the board and the question show)
    # (not a two-input "diamond of x, y", not "diamond of 2x", not "diamond of x + 1" whose scope speech leaves open)
    for _ in range(2 if diamond else 0):   # twice: "diamond of diamond of x" = ◆(◆(x))
        s = re.sub(r"\b[Dd]iamond of,? (◆\([^()]{1,12}\)|\([^()]{1,20}\)|−?\d+(?:/\d+)?|%s)(?![\w(])(?!,\s*(?:[A-Za-z]|\d|%s)\b(?!\s+(?:divided|times|is|equals)\b))(?!\s*[+−^²³]|\s+(?:plus|minus|squared|cubed)\b)" % (_LET, _NW),
                   lambda m: '◆(' + (m.group(1) if m.group(1).startswith('◆') else m.group(1).strip('()')) + ')', s)
    # number word / digit / letter OVER a letter: "three over a" -> "3/a", "b over a" -> "b/a"
    s = re.sub(r"(?<![\w/])(%s|\d+|%s) over (%s)" % (_NW, _LET, _LET), lambda m: _num(m.group(1)) + '/' + m.group(2), s, flags=0)
    s = re.sub(r"(?<![\w/])([Tt]hree|[Tt]wo|[Oo]ne|[Ff]our|[Ff]ive|[Ss]ix|\d+) over (%s)" % _LET,
               lambda m: _num(m.group(1)) + '/' + m.group(2), s)
    # "three over the whole a + 1" -> "3/(a + 1)"
    s = re.sub(r"(?<![\w/])(%s|\d+) over the whole (%s [+−×] %s)(?![\w/])" % (_NW, _ATOM, _ATOM),
               lambda m: _num(m.group(1)) + '/(' + m.group(2) + ')', s, flags=re.I)
    # a whole triple multiplied (Codex batch B): "5, 12, 13 × 3 = 15, 36 and 39" -> "(5, 12, 13) × 3 = (15, 36, 39)"
    _n = r"(?:\d+|%s)" % _NW
    def _triple(m):
        v = [int(_num(m.group(k))) for k in (1, 2, 3)]
        if not m.group(5) and v[0] ** 2 + v[1] ** 2 != v[2] ** 2:      # only a real triple, or one with its result
            return m.group(0)
        out = '(%s, %s, %s) × %s' % tuple(_num(m.group(k)) for k in (1, 2, 3, 4))
        if m.group(5):
            out += ' = (%s, %s, %s)' % tuple(_num(m.group(k)) for k in (5, 6, 7))
        return out
    s = re.sub(r"(?<![\w])(%s), (%s),? (?:and )?(%s) × (%s)(?: (?:=|is) (%s), (%s),? (?:and )?(%s))?(?![\w/])"
               % (_n, _n, _n, _n, _n, _n, _n), _triple, s, flags=re.I)
    # "a root three" -> "a√3" (the gold / silver triangle sides), "x root two" -> "x√2"
    #   (the article in "has a root three in it" stays: a / A only after a list comma, "is", "are", "and", "=", ...)
    s = re.sub(r"(?<![\w'’])([b-hj-zB-HJ-Z]|(?<=, )a|(?<=\bis )a|(?<=\bare )a|(?<=\band )a|(?<=\bbe )a|(?<=\bmatches )a|(?<== )a) root (%s|\d+)\b" % _NW,
               lambda m: m.group(1) + '√' + _num(m.group(2)), s)
    s = re.sub(r"(?<![\w'’])(\d+) root (%s|\d+)\b" % _NW, lambda m: m.group(1) + '√' + _num(m.group(2)), s)
    s = re.sub(r"(?<![\w'’])(?:the |[Tt]he )?([Rr])oot (two|three|five|six|seven|\d+)\b(?! of\b)", lambda m: '√' + _num(m.group(2)), s)
    s = re.sub(r"(?<![\w'’])(%s) √" % _NW, lambda m: _num(m.group(1)) + '√', s, flags=re.I)
    # a coefficient that the speech split: "+ 4 a =" -> "+ 4a =" (only right after an operator)
    s = re.sub(r"(?<=[=+−×÷(<>≤≥] )(\d+) (%s)(?=\s*[=+−×÷<>≤≥,.;)]|\s*$)" % _LET, r"\1\2", s)
    # binary words between two operands (a comma may sit before the word in speech)
    for _ in range(4):
        before = s
        for w, sym in ((r'divided by', ' ÷ '), (r'times', ' × '), (r'plus', ' + '), (r'minus', ' − '),
                       (r'(?:is equal to|equals)', ' = '), (r'is (?:smaller|less) than', ' < '),
                       (r'is (?:bigger|larger|greater) than', ' > ')):
            s = re.sub(r"(%s|%s)(,?) %s,? (%s|%s)(?![\w/])" % (_OPND, '◆\\([^()]{1,12}\\)', w, _OPND, _NW),
                       lambda m, sym=sym: _binop(m, sym), s)
        if s == before:
            break
    # "<letter / fraction / ◆(..)> is <number>" -> "=" when the sentence goes on with punctuation or and/but/so
    s = re.sub(r"((?:%s|◆\([^()]{1,12}\)|(?<![\w/])\d*%s[%s]*)),? is (%s|−?\d+(?:/\d+)?|%s)(?=[,.;:?!]|\s+(?:and|but|so|for|too)\b|$)"
               % (_FRAC, _LET, _SUPS, _FRAC, _NW), _is_eq, s)
    return s


def _binop(m, sym):
    """a spoken comma before + − × ÷ groups everything before it ("a + 2, times a" = (a + 2)·a): keep the words then,
    unless the left operand is a whole expression on its own (◆(..), a fraction or a bracket, not after an operator)"""
    left, comma = m.group(1), m.group(2)
    if comma and sym.strip() in '+−×÷':
        before = m.string[:m.start()].rstrip()
        if not re.fullmatch(r"◆\(.*\)|\(.*\)|.+/.+", left) or before[-1:] in '+−×÷=/':
            return m.group(0)
    return left + sym + _num(m.group(3))


def _is_eq(m):
    """the is-rule: a plain letter needs "x is 5" (no comma) and must not be the end of a point name ("A G, is 10",
    "at O, is 60" stay in words)"""
    left = m.group(1); before = m.string[:m.start()]
    if re.fullmatch(r"\d*[A-Za-z][%s]*" % _SUPS, left):
        if ',' in m.group(0)[len(left):len(left) + 2] or re.search(r"(?:\b[A-Z] |\bat |\bpoint |\bangle )$", before):
            return m.group(0)
    return left + ' = ' + _num(m.group(2))


def _is_math_letter(s, i):
    """s[i] is a standalone letter: is it a math variable here?"""
    c = s[i]
    if c in 'Ii':
        return False
    prev = s[:i].rstrip(); nxt = s[i + 1:].lstrip()
    pc = prev[-1:] ; nc = nxt[:1]
    near = (pc and pc in _MATHCH) or (nc and nc in _MATHCH) or (i + 1 < len(s) and s[i + 1] in _SUPS) or (i > 0 and s[i - 1].isdigit())
    if c == 'A' and (re.match(r"\s+[B-Z](?![A-Za-z'’])", s[i + 1:]) or re.search(r"(?<![A-Za-z'’])[B-Z]\s+$", s[:i])
                     or re.search(r"(?:\b(?:point|points|vertex|angle|side|line|segment|circle|center|centre|centers|end|digit|"
                                  r"digits|letter|at|from|to|through|of)\s+|,\s*)$", s[:i])):
        return True     # a point / digit name: "A B C D", "on A B", "the angle at A", "A, B and C"
    if c in 'aA':
        return bool(near or re.match(_A_VAR, s[i:]) and (c == 'a' or near or not re.search(r'(?:^|[.!?:]\s*)$', s[:i])))
    if c.isupper():
        # capitals: geometry points / digit letters, but never the V method or V table names
        if re.match(r'\s*(?:method|table|shape|-shape)\b', s[i + 1:], re.I):
            return False
        return True
    return True


def mark(s):
    out = []; last = 0
    for m in re.finditer(r"(?<![A-Za-z_'’̅.])[A-Za-z](?![A-Za-z0-9_'’̅])", s):
        i = m.start()
        if s[i + 1:i + 2] == '.' and re.match(r'\.[A-Za-z]', s[i + 1:i + 3]):   # e.g. / i.e.
            continue
        if i > 0 and s[i - 1].isdigit() and s[i] == 's':                        # the 1990s
            continue
        if re.match(r'-[a-z]{2,}', s[i + 1:]) and s[i] not in 'xyz':           # e-mails, U-turn (x-axis stays)
            continue
        if re.match(r'\. ?[A-Z]\.', s[i + 1:]) or re.search(r'\b[A-Z]\. ?$', s[:i]):   # initials: J. K. Rowling
            continue
        if not _is_math_letter(s, i):
            continue
        out.append(s[last:i]); out.append(OPEN + s[i] + CLOSE); last = i + 1
    out.append(s[last:])
    return ''.join(out)


def display(text, video_text='', video_id=''):
    """video_text = the whole lesson: a two-input diamond lesson ("diamond of x, y") keeps "diamond of" in words.
    Verbal lessons (vr…) are not math: their letters (side A, position X) stay plain."""
    if video_id.startswith('vr'):
        return text
    return mark(tidy(text, diamond=not TWO_INPUT.search(video_text)))
