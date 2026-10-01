"""NITE official quantitative terminology (real_exam/TERMINOLOGY_AUDIT.md), applied to the built course data D
right before the studio is written. Only quantitative topics (1-38, 51, 52) are touched; verbal topics 39-50 never.

apply(D) rewrites text fields in place and returns a report {rule: Counter(category)}.
"""
import re, os, json, collections

QUANT = set(range(1, 39)) | {51, 52}

# keys whose string values are identifiers / production metadata that must never be rewritten
SKIP_KEYS = {'id', 'qid', 'pid', 'ref', 'questionId', 'k', 'unit', 'layout', 'mode', 'src', 'sourceFiles',
             'sourceSegment', 'source', 'passageId', 'type', 'ntTerminology', 'bankSet', 'bankCategory',
             'practiceGroup', 'mechanic', 'difficulty', 'kind', 'subject', 'fig', 'figalign', 'band', 'setTitle_id'}
PROD_KEYS = {'draw', 'label', 'loads', 'nextCue', 'canvas', 'script'}


def _topic(x):
    try: return int(x)
    except (TypeError, ValueError): return None


def units(D):
    """yield (category_root, topic, obj, obj_id) for every in-scope object"""
    for qid, q in D['questions'].items():
        yield 'question', _topic(q.get('topic')), q, qid
    for vid, v in D['videos'].items():
        yield 'video', _topic(v.get('topic')), v, vid
    rt = {}
    for f in D['flow']:
        if f['type'] == 'reference': rt.setdefault(f['ref'], _topic(f['topic']))
    for rid, r in D['references'].items():
        yield 'card', rt.get(rid), r, rid


def walk(obj, path=()):
    """yield (container, key, value, path) for every string leaf, skipping identifier keys"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in SKIP_KEYS: continue
            if isinstance(v, str): yield obj, k, v, path + (k,)
            else: yield from walk(v, path + (k,))
    elif isinstance(obj, list):
        for n, v in enumerate(obj):
            if isinstance(v, str): yield obj, n, v, path + (n,)
            else: yield from walk(v, path + (n,))


def category(root, path):
    if root != 'video': return root
    keys = [p for p in path if isinstance(p, str)]
    if 'say' in keys: return 'spoken'
    if any(k in PROD_KEYS for k in keys): return 'production'
    return 'screen'


# ---------------------------------------------------------------- protected-segment splitting
# TeX ($..$, $$..$$, \(..\)), HTML tags, and data-tex attributes are protected; rules run on plain text.
_PROT = re.compile(r'\$\$.*?\$\$|\$[^$]*\$|\\\(.*?\\\)|<[^>]*>', re.S)


def split_text(s):
    """list of (is_plain, segment)"""
    out, last = [], 0
    for m in _PROT.finditer(s):
        if m.start() > last: out.append((True, s[last:m.start()]))
        out.append((False, m.group(0))); last = m.end()
    if last < len(s): out.append((True, s[last:]))
    return out


# ---------------------------------------------------------------- masking
# Math and tags are replaced by placeholder tokens so that the rules see the sentence around them:
#   §k§  = a math token (TeX or a <span class="math" data-tex=..></span>), counts as a word / subject
#   ‹k›  = any other HTML tag (transparent)
_MASK = re.compile(r'<span class="math"[^>]*>(?:</span>)?|\$\$.*?\$\$|\$[^$]*\$|\\\(.*?\\\)|<[^>]*>', re.S)
_ARROW = re.compile(r'\$\s*(?:\\[;,]\s*)*\\(?:to|rightarrow|Rightarrow|longrightarrow)\s*(?:\\[;,]\s*)*\$|<span class="math" data-tex="\s*(?:\\[;,]\s*)*\\(?:to|rightarrow|Rightarrow)\s*(?:\\[;,]\s*)*"></span>')
_TEXT = re.compile(r'\\text\{([^{}]*)\}')
_ATTR = re.compile(r'\b(aria-label|title|alt|data-tex)="([^"]*)"')


def _mask(s):
    toks = []
    def rep(m):
        g = m.group(0); toks.append(g)
        n = len(toks) - 1
        return ('§%d§' % n) if (g.startswith('$') or g.startswith('\\(') or g.startswith('<span class="math"')) else ('‹%d›' % n)
    return _MASK.sub(rep, s), toks


def _unmask(s, toks):
    return re.sub(r'§(\d+)§|‹(\d+)›', lambda m: toks[int(m.group(1) or m.group(2))], s)


# ---------------------------------------------------------------- rules
QUANT_TOPICS_DOC = 'topics 1-38, 51, 52'
RULES = ['1 divisible', '2 units digit', '3 vertical angles', '4 deltoid', '5 contracted', '6 intercept',
         '7 toss', '8 kph', '9 key', '10 circle', '11 altitude', '12 lateral surface', '13 box', '14 positive integer']


def _cap(src, word):
    return word[:1].upper() + word[1:] if src[:1].isupper() else word


def _sub(pat, repl, s, flags=0):
    return re.subn(pat, repl, s, flags=flags)


# --- rule 1: "X divides by Y" (calque of מתחלק ב־) -> "X is divisible by Y"; the operation "divide by" stays
_SUBJ = r'(?:§\d+§|\d+|\b[a-z]|\ba \+ b)'


def r_divisible(s, ctx):
    n = 0
    specials = [
        ('Bonus: the boys divide by three, the girls by five, and the whole class by eight.',
         'Bonus: the number of boys is divisible by three, the number of girls by five, and the whole class by eight.'),
        ('three in a row divide by six', 'the product of three in a row is divisible by six'),
        ('Three in a row divide by six', 'The product of three in a row is divisible by six'),
        ('two times four — divide by eight', 'two times four — are divisible by eight'),
        ('Twenty divides by four exactly', 'Twenty is divisible by four'),
        ('The first equation divides by three', 'The first equation can be divided by three'),
    ]
    for a, b in specials:
        if a in s: s = s.replace(a, b); n += 1
    for pat, rep in [
        (r"\b([Dd])oes not divide by", lambda m: _cap(m.group(1), 'is not divisible by')),
        (r"\b([Dd])oesn't divide by", lambda m: _cap(m.group(1), "isn't divisible by")),
        (r"(%s\s+)do not divide by" % _SUBJ, r"\1are not divisible by"),
        (r"(%s\s+)don't divide by" % _SUBJ, r"\1aren't divisible by"),
        (r"\bDoes (\S+) divide by", r"Is \1 divisible by"),
        (r"\b(must|Must|MUST)(\s+also|\s+it)?\s+divide by", r"\1\2 be divisible by"),
        (r"((?:§\d+§|\d+|\bthey|\bx)\s+)(both|all)\s+divide by", r"\1are \2 divisible by"),
        (r"\b(both|all|Both|All)\s+divide by", r"\1 are divisible by"),
        (r"\bALWAYS\s+divide by", r"are ALWAYS divisible by"),
    ]:
        s, k = _sub(pat, rep, s); n += k
    toks = ctx.get('toks') or []

    def is_arrow(tok):
        m = re.fullmatch(r'§(\d+)§', tok)
        return bool(m) and int(m.group(1)) < len(toks) and bool(_ARROW.fullmatch(toks[int(m.group(1))]))

    def plural(m):
        if is_arrow(m.group(1)): return m.group(0)          # "Cycle $\to$ divide by its length" = the operation
        kept[0] += 1
        return m.group(1) + ' are divisible by'
    kept = [0]
    s, k = re.subn(r"(\b(?:parts|numbers|them|evens|digits)|§\d+§|\b\d+|\ba \+ b)\s+divide by", plural, s); n += kept[0]

    def subjectless(pre):
        tail = pre.rstrip()
        if not tail or tail[-1] in '→:—(\'"‘“.?!·' or re.search(r'‹\d+›$', tail): return True
        last = re.search(r'§\d+§$', tail)
        return bool(last) and is_arrow(last.group(0))

    def adverb(m):
        return (_cap(m.group(1), m.group(1)) + ' divisible by') if subjectless(s[:m.start()]) else ('is ' + m.group(1) + ' divisible by')
    s, k = re.subn(r"\b(always|also|never|NEVER|only|ALWAYS|Always)\s+divides(?:\s+(?:evenly|exactly))?\s+by", adverb, s); n += k

    def one(m):
        pre = s[:m.start()]
        sent = re.split(r'[.!?;:]\s', pre)[-1]
        if re.search(r'\bChoice\b', sent): return m.group(0)           # "Choice 4 divides by 3/4 instead of ..." = the operation
        kept[0] += 1
        return _cap(m.group(1), 'divisible by') if subjectless(pre) else 'is divisible by'
    kept = [0]
    s, k = re.subn(r"\b([Dd])ivides(?:\s+(?:evenly|exactly))?\s+by", one, s); n += kept[0]
    return s, n


# --- rule 2
def r_units(s, ctx):
    s, n = _sub(r"\b([Oo])nes['’]?(\s+)(digits?|place)\b", lambda m: _cap(m.group(1), 'units') + m.group(2) + m.group(3), s)
    if ctx.get('key') == 'navLabel':      # a label cut in the middle of the word: "... its ones d"
        s, k = _sub(r"\bones( d\w{0,4})$", r"units\1", s); n += k
    return s, n


# --- rule 3
def r_vertical(s, ctx):
    n = 0
    for pat, rep in [
        (r"\b([Tt]he marked angle(?: §\d+§)?(?: outside the triangle)?) is vertically opposite (the interior angle at A)",
         r"\1 and \2 are vertical angles"),
        (r"\bwith vertically opposite central angles", "whose central angles are vertical angles"),
        (r"\bare vertically opposite\b", "are vertical angles"),
        (r"\(vertically opposite\)", "(vertical angles)"),
        (r"\b([Vv])ertically opposite (angles?)", lambda m: _cap(m.group(1), 'vertical') + ' ' + m.group(2)),
    ]:
        s, k = _sub(pat, rep, s); n += k
    return s, n


# --- rule 4 (stateful: ctx['kite'] = 'question' | 'screen' | 'spoken' | 'card', ctx['kite_seen'] = set of scopes)
def r_deltoid(s, ctx):
    mode = ctx.get('kite')
    if not mode: return s, 0
    if mode == 'question':
        def q(m):
            w = m.group(0)
            out = 'deltoid' + ('s' if w.lower().endswith('s') else '')
            return _cap(w, out)
        return re.subn(r"\bkites?\b", q, s, flags=re.I)
    scope = ctx['kite_scope']
    if scope in ctx['kite_seen']: return s, 0
    if mode == 'screen':
        for a, b in [(r'A kite area from', 'Kite (deltoid) area from'),
                     (r'Rhombus, kite \((§\d+§) diagonals\)', r'Rhombus, kite (deltoid), \1 diagonals')]:
            if re.search(a, s): ctx['kite_seen'].add(scope); return re.sub(a, b, s), 1
    m = re.search(r"\b([Kk]ites?)\b(?!['’]s)(\s+[A-Z]{3,4}\b)?", s)
    if not m: return s, 0
    ctx['kite_seen'].add(scope)
    word = m.group(1); plural = word.lower().endswith('s')
    if mode == 'spoken':
        add = ' (also called deltoids)' if plural else ' (also called a deltoid)'
    else:
        add = ' (deltoids)' if plural else ' (deltoid)'
        if ctx.get('titlecase') and word[0].isupper(): add = add.replace('(d', '(D')
    return s[:m.end()] + add + s[m.end():], 1


# --- rule 5
def r_contracted(s, ctx):
    n = 0
    for pat, rep in [
        (r"\b([Ss])hort multiplication (formulas?)", lambda m: _cap(m.group(1), 'contracted') + ' multiplication ' + m.group(2)),
        (r"(?<![Cc]ontracted )(?<![Ss]hort )\b([Mm])ultiplication ([Ff])ormula(s?)\b",
         lambda m: (('Contracted M' if m.group(1) == 'M' and m.group(2) == 'F' else ('Contracted m' if m.group(1) == 'M' else 'contracted m'))
                    + 'ultiplication ' + m.group(2) + 'ormula' + m.group(3))),
    ]:
        s, k = _sub(pat, rep, s); n += k
    return s, n


# --- rule 6: angle "rests on / stands on the arc" -> "intercepts the arc"; "rests on a diameter" -> "lies on a diameter" (guide L1368)
_ARCOBJ = r"(?:(?:the|a|an|this|that|its)\s+)?(?:(?:same|highlighted|bold|long|short|major|minor|equal|whole)\s+)*arcs?\b"
_VERB_I = {'rests': 'intercepts', 'rest': 'intercept', 'resting': 'intercepting', 'stands': 'intercepts', 'stand': 'intercept',
           'standing': 'intercepting'}
_VERB_L = {'rests': 'lies', 'rest': 'lie', 'resting': 'lying', 'stands': 'lies', 'stand': 'lie', 'standing': 'lying'}


def r_intercept(s, ctx):
    n = 0
    specials = [
        ('When an angle closes off an arc like this, we say the angle rests on the arc. In English: it intercepts the arc.',
         'When an angle closes off an arc like this, we say the angle intercepts the arc.'),
        ("Here's an arc, and an angle resting on it", "Here's an arc, and an angle intercepting it"),
        ('Angle ABC rests on it.', 'Angle ABC intercepts it.'),
        ('Rests on an arc', 'Intercepts an arc'),
        ('there\'s no central angle on arc AG, or on arc ED', 'there\'s no central angle intercepting arc AG or arc ED'),
        ('inscribed angles on the same arc (or on equal arcs)', 'inscribed angles intercepting the same arc (or equal arcs)'),
        ('the one the angle rests on', 'the one the angle intercepts'),
    ]
    for a, b in specials:
        if a in s: s = s.replace(a, b); n += 1
    def verb(m, table):
        v = m.group(1); w = table[v.lower()]
        return _cap(v, w) + ' '
    s, k = re.subn(r"\b(rests|rest|resting|stands|stand|standing)\s+on\s+(?=%s)" % _ARCOBJ, lambda m: verb(m, _VERB_I), s, flags=re.I); n += k
    s, k = re.subn(r"\b(rests|rest|resting|stands|stand|standing)\s+on\s+(?=(?:a|the)\s+diameter\b)", lambda m: verb(m, _VERB_L) + 'on ', s); n += k
    s, k = re.subn(r"\bdoes (it|the angle) (?:rest|stand) on\b", r"does \1 intercept", s); n += k
    if ctx.get('circle'):   # arcs named by two letters, in the circle topic only ("Alpha stands on ED")
        s, k = re.subn(r"\b(stands|rests)\s+on\s+(?=[A-Z]{2}\b)", lambda m: verb(m, _VERB_I), s); n += k
    s, k = re.subn(r"\b(angles?)\s+on\s+(?=(?:the\s+same\s+arc|arc\s+[A-Z]{2,3}\b|equal\s+arcs))", r"\1 intercepting ", s); n += k
    return s, n


# --- rule 7 (dice context only)
def r_toss(s, ctx):
    if not ctx.get('dice'): return s, 0
    n = 0
    for pat, rep in [
        (r"\bprobability of rolling\b", "probability of obtaining"),
        (r"\b(\w+) rolls a (six|\d)\b", r"\1 gets a \2"),
        (r"\b([Rr])oll by roll\b", lambda m: _cap(m.group(1), 'toss by toss')),
        (r"\b([Rr])olled\b", lambda m: _cap(m.group(1), 'tossed')),
        (r"\b([Rr])olling\b", lambda m: _cap(m.group(1), 'tossing')),
        (r"\b([Rr])olls\b", lambda m: _cap(m.group(1), 'tosses')),
        (r"\b([Rr])oll\b", lambda m: _cap(m.group(1), 'toss')),
    ]:
        s, k = _sub(pat, rep, s); n += k
    return s, n


# --- rule 8 (written text only; spoken "kilometers per hour" stays)
def r_kph(s, ctx):
    if ctx.get('cat') == 'spoken': return s, 0
    n = 0
    if s == 'Motion: §0§ km per hour' or s.startswith('Motion: $20$ km per hour'):
        return s.replace('km per hour', 'kilometers per hour (kph)'), 1
    for pat, rep in [
        (r"\(km per hour\)", "(kph)"),
        (r"\bkm\s*/\s*h\b|\bkm per hour\b|\bkilomet(?:er|re)s per hour\b", "kph"),
    ]:
        s, k = _sub(pat, rep, s); n += k
    return s, n


# --- rule 9
def r_key(s, ctx):
    return _sub(r"\b([Ll])egend(s?)\b", lambda m: _cap(m.group(1), 'key') + ('s' if m.group(2) else ''), s)


# --- rule 10
def r_circle(s, ctx):
    if ctx.get('keep_disk_aside'): return s, 0
    n = 0
    for pat, rep in [(r"\bCircle and disk\b", "The circle"), (r"\bcircle and disk\b", "the circle")]:
        s, k = _sub(pat, rep, s); n += k
    s, k = _sub(r"\b([Dd])is[ck](s?)\b(['’]s)?", lambda m: _cap(m.group(1), 'circle') + m.group(2) + (m.group(3) or ''), s); n += k
    return s, n


# --- rule 11 (triangles only: ctx['altitude'] set by the caller)
def r_altitude(s, ctx):
    if not ctx.get('altitude'): return s, 0
    return _sub(r"\b([Hh])eight to (that side|THAT side|the side|side|it|its base|AD)\b",
                lambda m: _cap(m.group(1), 'altitude') + ' to ' + m.group(2), s)


# --- rule 12
def r_lateral(s, ctx):
    return _sub(r"\b([Ll])ateral area(s?)\b", lambda m: _cap(m.group(1), 'lateral') + ' surface area' + m.group(2), s)


# --- rule 13
def r_box(s, ctx):
    n = 0
    s, k = _sub(r"\b([Aa])n open rectangular box\b", r"\1n open box", s); n += k
    s, k = _sub(r"\b([Rr])ectangular (boxes|box)\b", lambda m: _cap(m.group(1), m.group(2)), s); n += k
    return s, n


# --- rule 14
def r_posint(s, ctx):
    n = 0
    if ctx.get('keep_natural'): return s, 0
    for a, b in [('It is a natural number', 'It is a positive integer'),
                 ('is a natural number: true', 'is a positive integer: true'),
                 ('Natural number / positive integer', 'Positive integer (natural number)'),
                 ('A prime is a natural number — positive and whole — bigger than one…', 'A prime is a positive integer bigger than one…'),
                 ("as a product of two smaller natural numbers", "as a product of two smaller positive integers"),
                 ('gives a natural number', 'gives a positive integer')]:
        if a in s: s = s.replace(a, b); n += 1
    return s, n


RULE_FNS = [('1 divisible', r_divisible), ('2 units digit', r_units), ('3 vertical angles', r_vertical), ('4 deltoid', r_deltoid),
            ('5 contracted', r_contracted), ('6 intercept', r_intercept), ('7 toss', r_toss), ('8 kph', r_kph), ('9 key', r_key),
            ('10 circle', r_circle), ('11 altitude', r_altitude), ('12 lateral surface', r_lateral), ('13 box', r_box),
            ('14 positive integer', r_posint)]


def _run(s, ctx, stats, in_svg_text=False):
    """apply all rules to one plain (masked) string; stats[rule] += changes"""
    for name, fn in RULE_FNS:
        if name == '4 deltoid' and ctx.get('kite_skip'): continue
        new, k = fn(s, ctx)
        if new != s:
            stats[name] += max(k, 1); s = new
    return s


def transform(s, ctx, stats):
    """rewrite one string field: masked plain text + \\text{} inside math + visible svg/html attributes"""
    masked, toks = _mask(s)
    ctx = dict(ctx, toks=toks)
    masked = _run(masked, ctx, stats)
    sub_ctx = dict(ctx, kite_skip=ctx.get('kite') not in (None, 'question'))   # never add "(deltoid)" inside math or attributes on slides
    for i, t in enumerate(toks):
        if t.startswith('<'):
            def attr(m):
                if m.group(1) == 'data-tex':
                    return 'data-tex="' + _TEXT.sub(lambda x: '\\text{' + _run(x.group(1), sub_ctx, stats) + '}', m.group(2)) + '"'
                return m.group(1) + '="' + _run(m.group(2), sub_ctx, stats) + '"'
            toks[i] = _ATTR.sub(attr, t)
        else:
            toks[i] = _TEXT.sub(lambda x: '\\text{' + _run(x.group(1), sub_ctx, stats) + '}', t)
    return _unmask(masked, toks)


# ---------------------------------------------------------------- driver
ALTITUDE_OK = {'geo-016', 'geo-017-after', 'geo-018-after', 'r26-t31-summary', 'geo-105', 'solve-q-r26-t31-01', 'solve-geo37-g164',
               'geo37-g164', 'solve-geo33-g094', 'solve-geo32-g069', 'mem-triangle-area'}      # triangle areas only
KITE_NOT_SHAPE = {'wp22-p24'}                                                                   # a flying kite (ratio question)
_DICE = re.compile(r'\bdice\b|\bdie\b', re.I)
_TITLE_KEYS = {'title', 'bigTitle', 'navLabel'}


def _is_titlecase(s):
    words = [w for w in re.findall(r"[A-Za-z]+", s) if len(w) > 3]
    return bool(words) and all(w[0].isupper() for w in words)


def _manual(D, stats, seen):
    """hand edits that a regex cannot do safely"""
    v = D['videos'].get('geo-042')
    # (only when geo-042 has its patched layout - a partial build such as `math_check.py 9` leaves it unpatched)
    if v and len(v['beats']) > 5 and len(v['beats'][4].get('items') or []) > 4 and v['beats'][5].get('items'):
        # "The family" slide: the kite drawing's label gets a second line; "Who is also who?" tree: two lines inside the box
        it = v['beats'][4]['items'][4]['v']
        old = it['svg']
        new = old.replace('viewBox="208.7 52.4 222.7 328.0"', 'viewBox="208.7 52.4 222.7 362.0"').replace(
            'font-size="42.9">Kite</text></svg>',
            'font-size="42.9">Kite</text><text x="320.0" y="401.0" text-anchor="middle" fill="#17233c" '
            'font-family="Inter,Arial,sans-serif" font-weight="600" font-size="30">(deltoid)</text></svg>')
        if new != old: it['svg'] = new; stats[('4 deltoid', 'screen')] += 1; seen.add(('geo-042', 'beat', 4, 'body'))
        it = v['beats'][5]['items'][0]['v']
        old = it['svg']
        new = old.replace('<text x="545.000" y="115.000" text-anchor="middle" dominant-baseline="middle" fill="#203344" '
                          'font-family="DejaVu Sans,Arial,sans-serif" font-size="19">Kite</text>',
                          '<text x="545.000" y="107.000" text-anchor="middle" dominant-baseline="middle" fill="#203344" '
                          'font-family="DejaVu Sans,Arial,sans-serif" font-size="18">Kite</text>'
                          '<text x="545.000" y="125.000" text-anchor="middle" dominant-baseline="middle" fill="#203344" '
                          'font-family="DejaVu Sans,Arial,sans-serif" font-size="13">(deltoid)</text>')
        if new != old: it['svg'] = new; stats[('4 deltoid', 'screen')] += 1; seen.add(('geo-042', 'beat', 5, 'body'))
    v = D['videos'].get('numbers')
    if v:   # t1 "Natural numbers" slide: the lesson keeps the explanation, the slide title names the exam term
        b = v['beats']
        for n, (bb, k) in enumerate([(b[3], 'title'), (b[3], 'loads'), (b[2], 'nextCue')]):
            if 'Natural numbers' in bb[k]:
                bb[k] = bb[k].replace('Natural numbers', 'Positive integers')
                stats[('14 positive integer', 'screen' if k == 'title' else 'production')] += 1
        sb = v['hybrid']['sidebar']
        if 'Natural numbers' in sb: sb[sb.index('Natural numbers')] = 'Positive integers'; stats[('14 positive integer', 'screen')] += 1
        if b[3]['items'][2].get('t') == 'Positive integer':
            b[3]['items'][2]['t'] = 'Positive integers'


def apply(D):
    stats = collections.Counter()
    seen = set()
    _manual(D, stats, seen)
    for root, t, obj, oid in units(D):
        if t not in QUANT: continue
        dice = bool(_DICE.search(json.dumps(obj, ensure_ascii=False)))
        for cont, k, s, path in walk(obj):
            cat = category(root, path)
            ctx = {'cat': cat, 'key': k, 'dice': dice, 'circle': t == 33, 'altitude': oid in ALTITUDE_OK}
            keys = [p for p in path if isinstance(p, str)]
            in_svg = 'svg' in keys
            # rule 4 mode and scope
            if root == 'question':
                ctx['kite'] = None if oid in KITE_NOT_SHAPE else 'question'
            elif root == 'card':
                ctx['kite'] = None if in_svg else 'card'; ctx['kite_scope'] = (oid,)
            elif cat == 'spoken':
                ctx['kite'] = 'spoken'; ctx['kite_scope'] = (oid, 'spoken')
            elif cat == 'screen' and not in_svg:
                ctx['kite'] = 'screen'
                if path[0] == 'beats':
                    part = 'title' if path[2] == 'title' else 'big' if path[2] == 'bigTitle' else 'body'
                    ctx['kite_scope'] = (oid, 'beat', path[1], part)
                else:
                    ctx['kite_scope'] = (oid,) + tuple(path)
                ctx['titlecase'] = (k in _TITLE_KEYS or path[:2] == ('hybrid', 'title')) and _is_titlecase(s)
            ctx['kite_seen'] = seen
            if oid == 'geo-074' and path[:5] == ('beats', 1, 'lines', 6, 'say'):
                ctx['keep_disk_aside'] = True
            local = collections.Counter()
            new = transform(s, ctx, local)
            if new != s:
                cont[k] = new
                for r, c in local.items(): stats[(r, cat)] += c
    return stats


def report(stats):
    cats = ['question', 'screen', 'spoken', 'card', 'production']
    lines = ['%-22s ' % 'rule' + ' '.join('%9s' % c for c in cats) + '    total']
    for r in RULES:
        row = [stats.get((r, c), 0) for c in cats]
        lines.append('%-22s ' % r + ' '.join('%9d' % x for x in row) + '   %6d' % sum(row))
    return '\n'.join(lines)
