"""2026-10-15 THE BOARD FOLLOWS HER READING (recorded videos; visual only - no spoken text, no slide / paragraph changes,
so no "needs re-read" flags).

Source: the reading study of her recorded takes (what she ADDED aloud, what she SKIPPED) + the early-answer check of the
recorded videos (a result on the board before she says it). Rules: real_exam/TEACHING_STYLE_GUIDE.md V3 / V4 (the
starting math written at its clause, every step at its clause, no early answers, nothing under the camera bubble),
calm highlights, handwriting chunks, "So far" boxes.

  - math she added aloud: written on the board, anchored on the script words next to her words (Rule V4.7). Her
    ad-libs are not script words, so an item is anchored on the nearest script phrase BEFORE them when it states the
    starting math, and AFTER them when it holds the result (never an early answer).
  - lines she skipped: their board items removed, or their cues dropped (a POINT / mark on words she never said).
  - early answers: a result is split off and anchored at the clause where she says it, or the line is hand-written so
    reading_to_video writes it chunk by chunk with her words (write_chunks), or the verdict becomes a pen mark at her
    verdict words.
Applied by _method_visuals.post() LAST (after Codex's clarity overlay and its cue checks, like the method-visual
fixes), so the overlay's reviewed_cues / cue_anchors still see exactly the plans they were made for.
Timing checked with her real word timings (her clean takes realigned to the current script) before it went in.
"""
import re

_MV = None


# ------------------------------------------------------------------------------------------------------------ helpers
def _ph(c):
    return c[3] if c[0] == 'mark' else c[2]


def _find_show(V, name):
    for si, sl in enumerate(V['slides']):
        for li, ln in enumerate(sl['lines']):
            for ci, c in enumerate(ln['cues']):
                if c[0] == 'show' and c[1]['_name'] == name: return si, li, ci
    raise AssertionError('no show of item %s' % name)


def item(V, name):
    si, li, ci = _find_show(V, name)
    return V['slides'][si]['lines'][li]['cues'][ci][1]


def ln(V, si, li):
    return V['slides'][si]['lines'][li]


def add(ns, V, si, li, it, phrase, before=None):
    """show a new item at `phrase` of line (si, li) (cues stay in speaking order); before = an item shown at the same
    phrase that the new one must precede on the board"""
    L = ln(V, si, li)
    assert ns._phrase_pos(L['say'], ('show', it, phrase)) >= 0, (phrase, L['say'][:80])
    if before:
        k = next(i for i, c in enumerate(L['cues']) if c[0] == 'show' and c[1]['_name'] == before)
        assert L['cues'][k][2] == phrase
        L['cues'].insert(k, ('show', it, phrase))
    else:
        _MV._insert(ns, L, ('show', it, phrase))
    return it


def move(ns, V, name, phrase, si=None, li=None):
    _MV.move_show(ns, V, name, phrase, si, li)


def drop(V, si, li, pred):
    """remove the cues of line (si, li) for which pred(cue) is true -> how many"""
    L = ln(V, si, li); n = len(L['cues'])
    L['cues'] = [c for c in L['cues'] if not pred(c)]
    return n - len(L['cues'])


def _targets(c, name):
    t = c[1] if c[0] == 'point' else c[2] if c[0] == 'mark' else ''
    return t.split(':')[0].strip() == name


def drop_item(V, name):
    """an item she never talks about: its show and every POINT / mark on it go"""
    si, li, ci = _find_show(V, name)
    n = 0
    for L in V['slides'][si]['lines']:
        k = len(L['cues'])
        L['cues'] = [c for c in L['cues'] if not ((c[0] == 'show' and c[1]['_name'] == name) or _targets(c, name))]
        n += k - len(L['cues'])
    return n


def rephrase(ns, V, si, li, pred, phrase):
    """the cues of line (si, li) matching pred get a new anchor phrase (kept in speaking order)"""
    L = ln(V, si, li); hit = [c for c in L['cues'] if pred(c)]
    assert hit, ('no cue to re-anchor', si, li)
    L['cues'] = [c for c in L['cues'] if not pred(c)]
    for c in hit:
        c = list(c)
        if c[0] == 'mark': c[3] = phrase
        else: c[2] = phrase
        _MV._insert(ns, L, tuple(c))


def retarget(V, si, li, old, new, phrases):
    """POINT / mark cues on item `old` at the given phrases now target `new` (same part)"""
    L = ln(V, si, li); out = []
    for c in L['cues']:
        if c[0] in ('point', 'mark') and _ph(c) in phrases and _targets(c, old):
            c = list(c); k = 1 if c[0] == 'point' else 2
            c[k] = new + c[k][len(old):]; c = tuple(c)
        out.append(c)
    L['cues'] = out


def is_show(name): return lambda c: c[0] == 'show' and c[1]['_name'] == name
def is_point(target, phrase=None): return lambda c: c[0] == 'point' and c[1] == target and (phrase is None or c[2] == phrase)
def is_mark(kind, target, phrase=None): return lambda c: c[0] == 'mark' and c[1] == kind and c[2] == target and (phrase is None or c[3] == phrase)


def hand(it, text, tex=None):
    it['_hand'] = text
    if tex is not None: it['t'] = tex
    return it


# ------------------------------------------------------------------------------------------------------------ topic 13
def _q359(ns, V):
    # the chunk "so" matched "so that is the second possible x" (5-7 s late): written without it, the x = ... chunk
    # finds "x is negative sixteen"
    hand(item(V, 'a1'), 'x + 7 = 9,    x  =  \\hl{two}{2}')
    hand(item(V, 'a2'), 'x + 7 = −9,    x  =  \\hl{m16}{−16}')


def _t13_13(ns, V):
    # her both-negative case (paragraph 3, right after "seven minus three is four"): "minus seven minus three will be
    # negative ten, and in absolute value ten". Written in the right column; the third-given lines join it there, which
    # also clears the known overlap of |a+b| = 7 - 3 = 4 with the answer choices (left column full).
    hand(item(V, 'e1_'), 'same signs :   7 + 3 = 10')
    # (e2_ stays typed: "four" is said again later, so a hand-written "= 4" chunk was timed 13 s late)
    n1 = ns.I('n1_', '$-7-3=-10,\\ \\ |-10|=10$', size=34, col=1, hand='−7 − 3 = −10,    |−10| = 10')
    add(ns, V, 0, 2, n1, 'seven minus three is four')
    item(V, 'e3_')['_col'] = 1
    item(V, 'e4_')['_col'] = 1
    # verdicts at her verdict words (the "no" / "yes" were on the board 9-19 s early)
    item(V, 'd1_')['t'] = '$7,\\ 3$: $\\ |10|<|4|$?'
    item(V, 'd3_')['t'] = '$7,\\ -3$: $\\ |\\hl{f1}{4}|<|10|$'
    _MV._insert(ns, ln(V, 2, 1), ('mark', 'cross', 'd1_', 'Ten is not smaller'))
    _MV._insert(ns, ln(V, 2, 2), ('mark', 'tick', 'd3_', 'Four is smaller than ten'))
    hand(item(V, 'o3'), 'a = 5,   b = −2 :   |3| < |5|')


def _t13_01(ns, V):
    # closing rules: she read only "I'll see you in the next lesson"
    drop(V, 1, 4, lambda c: c[0] == 'point' and c[2] in ("don't assume", "When there's a"))


def _q369(ns, V):
    # she never says "the bait" (and skipped the roadmap / bait sentence of paragraph 2: no board items there)
    hand(item(V, 'bait'), 'Take off 1 :   3 < x < 4', 'Take off $1$: $\\ 3<x<4$')
    drop(V, 0, 5, is_mark('cross', 'choice 1', 'the bait'))
    _MV._insert(ns, ln(V, 0, 5), ('mark', 'cross', 'choice 1', 'choice number one, the'))
    # results written with her words, not all at once (6-17 s early)
    hand(item(V, 'sp3'), 'Both :    4 < x < 5    or    −4 < x < −3')
    hand(item(V, 'd1q'), '(1)   3.5 :   |6| = 6,   no')
    hand(item(V, 'd2q'), '(2)   5.5 :   |10| = 10,   no')
    hand(item(V, 'd3q'), '(3)   −3.5 :   |−8| = \\hl{eight}{8},   yes')
    hand(item(V, 'd4q'), '(4)   −4.5 :   |−10| = 10,   no')


# ------------------------------------------------------------------------------------------------------------ topic 14
def _q402(ns, V):
    # her closing (after "it's choice number two"): a prime has two divisors, a prime squared three (2^2 = 4: 1, 2, 4),
    # and 2^3 = 8 has 1, 2, 4, 8. The cube example is written after it ("Okay? Now, try to keep this in mind").
    k4 = ns.I('k4', 'A prime: $2$ divisors', size=30)
    k4b = ns.I('k4b', '$2^2=4$: $\\ 1,\\ 2,\\ 4$ $\\ \\to\\ 3$ divisors', size=30)
    k5 = ns.I('k5', '$2^3=8$: $\\ 1,\\ 2,\\ 4,\\ 8$ $\\ \\to\\ 4$ divisors', size=30, col=1)
    add(ns, V, 2, 2, k4, "it's choice number two")
    add(ns, V, 2, 2, k4b, "it's choice number two")
    add(ns, V, 2, 2, k5, 'Okay')


def _t14_01(ns, V):
    # 1. her 90 / 91 test for three ("90 divides by 3, so 91 can't"), right before "Here's a quick test"
    a1b = ns.I('a1b', '$90=3\\cdot30$ $\\ \\to\\ 91$: not divisible by $3$', size=28)
    add(ns, V, 0, 3, a1b, "Here's a quick")
    # 2. 91: the digit sum (late) and 7 x 13 (8 s early) were one line; now 9 + 1 = 10 at its clause, the 70 + 21 working
    #    she says, and 91 = 7 x 13 at "So ninety-one is seven times thirteen" (left column, under the 90 / 91 test)
    a2 = item(V, 'a2'); hand(a2, '91 :   9 + 1 = 10   ✗', '$91$: $\\ 9+1=10$ ✗')
    move(ns, V, 'a2', 'So ninety-one, nine plus one')
    a2m = ns.I('a2m', '$7\\cdot10=70,\\ \\ 7\\cdot3=21$', size=30)
    add(ns, V, 0, 4, a2m, 'Seven times ten')
    a2b = ns.I('a2b', '$91=\\hl{f}{7\\cdot13}$', size=34, hand='91 = 70 + 21 = \\hl{f}{7·13}')
    add(ns, V, 0, 4, a2b, 'So ninety-one is seven')
    L = ln(V, 0, 4)
    L['cues'] = [tuple(['mark', 'circle', 'a2b: f', c[3]]) if c[0] == 'mark' and c[2] == 'a2: f' else c for c in L['cues']]
    retarget(V, 0, 4, 'a2', 'a2b', ("it's a fake",))
    # 3. the root bounds she says for 119, 133 and 113 (as for 91); 113's line without "113 :" (its chunk matched the
    #    later "a hundred thirteen leaves", 10-18 s late)
    b0 = ns.I('b0', '$10^2=100<119<121=11^2$', size=28)
    add(ns, V, 1, 0, b0, 'Ten squared is a hundred')
    b4 = ns.I('b4', '$11^2=121<133<144=12^2$', size=28)
    add(ns, V, 1, 1, b4, 'Eleven squared is')
    b1 = ns.I('b1', '$10^2=100<113<121=11^2$', size=28, col=1)
    add(ns, V, 1, 2, b1, 'Ten squared is')
    hand(item(V, 'a5'), 'odd,   1 + 1 + 3 = 5,   ends in 3', 'Odd, $\\ 1+1+3=5$, $\\ $ends in $3$')
    for n in ('a5', 'a7', 'a6', 'k3'): item(V, n)['_col'] = 1


def _primes2(ns, V):
    # paragraph 4 only (5 and 6 are held for her re-read): her 7 test of 91, "70 is 10 times 7 and 7 times 3 is 21,
    # so 70 plus 21 is 91, 13 times 7"
    c91d = ns.I('c91d', '$7\\cdot10=70,\\ \\ 7\\cdot3=21$', size=28)
    add(ns, V, 1, 2, c91d, 'Seven times thirteen is ninety-one', before='cp14')
    hand(item(V, 'cp14'), '91 = 70 + 21 = 7·13   ✗')


def _prime_tools(ns, V):
    # "the rule only works with real primes": 56 = 4 x 14 broken into its primes (her words: "break that 4 into two
    # twos, and the 14 into 2 and 7"), and every step of the count she says
    g10a = ns.I('g10a', '$4=2\\cdot2,\\ \\ 14=2\\cdot7$', size=40)
    hand(item(V, 'g10'), '56 = 2^3·7 :   (3+1)(1+1) = 4·2 = 8   ✓', '$56=2^3\\cdot7$: $\\ (3+1)(1+1)=4\\cdot2=8$ ✓')
    move(ns, V, 'g10', 'Fifty-six is two')          # its "56" chunk had matched the closing "and fifty-six"
    add(ns, V, 3, 2, g10a, 'Fifty-six is two', before='g10')


def _q389(ns, V):
    # the LCM sentence (she stopped after "it doesn't even divide x")
    drop(V, 0, 8, lambda c: c[0] == 'point' and c[2] in ("That's the smallest", 'both of them', 'least common multiple', "It's the tool"))


# ------------------------------------------------------------------------------------------------------------ topic 15
def _q432(ns, V):
    # cue phrases with a pause tag in them cannot be found in the spoken line (reading_to_video stops on them)
    rephrase(ns, V, 0, 1, lambda c: _ph(c) == 'by? [short pause', 'always divide by')
    # her opening: a^2 - 1 = (a - 1)(a + 1) (she checks it by opening the brackets); x = 5(a-1)a(a+1) when she says
    # it (was 23 s early)
    o2a = ns.I('o2a', '$a^2-1=(a-1)(a+1)$', size=30)
    add(ns, V, 0, 3, o2a, 'Use the difference')     # her "a minus one times a plus one" is said twice: the later one wins
    move(ns, V, 'o2', 'So x is five')
    # her run 8, 9, 10 ("one of them will divide - let's say eight, nine and ten, again nine divides by three")
    o10a = ns.I('o10a', '$8,\\ \\hl{n}{9},\\ 10$: $\\ 9$ divides by $3$', size=28, col=1)
    add(ns, V, 1, 1, o10a, 'one of these three numbers')


def _q436(ns, V):
    # her no-numbers argument: one number divides by 6, so the other two only have to divide by 6 together
    g4b = ns.I('g4b', 'One divides by $6$ $\\to$ the other two together, not each', size=28, col=1)
    add(ns, V, 0, 3, g4b, 'even though neither')


# ------------------------------------------------------------------------------------------------------------ topic 16
def _cons_sums(ns, V):
    # "= 9" was written 17 s early (the one-chunk fraction ran past the matcher's reach): each step its own chunk
    m2 = item(V, 'm2'); m2['size'] = 34
    hand(m2, 'Evens 4 to 20 :    {(20 − 4)/2} = 8,    8 + 1 = 9', 'Evens $4$ to $20$: $\\ \\frac{20-4}{2}=8,\\ 8+1=9$')
    # her ad-lib after the neighbors examples: 17^2 - 16^2 = 17 + 16 = 33 (written right after she says it)
    q6 = ns.I('q6', '$17^2-16^2=17+16=33$', size=44)
    add(ns, V, 2, 3, q6, 'Careful, replacing')


def _q457(ns, V):
    # she skipped the (-2)^3 * 4 / 2 example: the item and every highlight on it go
    drop_item(V, 'a6')
    # |a| > 0 at "its absolute value must be positive"; b^2 > 0 at "So b squared must be positive" (was 13 s early)
    a1 = item(V, 'a1'); hand(a1, '|a| > 0', '$|a|>0$')
    move(ns, V, 'a1', 'its absolute value must be positive', 0, 2)
    a1b = ns.I('a1b', '$b^2>0$', col=1, hand='b^2 > 0')
    add(ns, V, 0, 3, a1b, 'So b squared must be positive')


def _q458(ns, V):
    # "These are even numbers in a row, so each gap is two" - not said
    drop(V, 0, 6, is_point('f4', 'even numbers in'))


# ------------------------------------------------------------------------------------------------------------ topic 17
def _given_said(ns, V):
    # she paraphrased the stem ("we're given this range"): the stem highlight at the words she said
    rephrase(ns, V, 0, 0, is_point('stem', 'Given'), 'Which of the following')


def _q496(ns, V):
    _given_said(ns, V)
    rephrase(ns, V, 0, 1, lambda c: _ph(c) == "short pause] We'll", "We'll solve it")


def _t17_05(ns, V):
    # she says the midpoint calculation (verified in her take: "Negative one is the midpoint exactly. Add negative seven
    # and five, then divide their sum by two"): it is written; "4: the distance" and "-1: the midpoint" are two lines
    m7 = item(V, 'm7'); m7['t'] = '$4$: the distance from $A$'
    m7b = ns.I('m7b', '$\\frac{-7+5}{2}=-1$: the midpoint', size=28, col=1, hand='{(−7 + 5)/2} = −1 :  the midpoint')
    add(ns, V, 0, 4, m7b, 'C. Negative one')
    drop(V, 0, 4, is_point('m7', 'C. Negative one'))
    retarget(V, 0, 4, 'm7', 'm7b', ('midpoint: add negative', 'then divide their'))


# ------------------------------------------------------------------------------------------------------------ topic 18
def _q514(ns, V):
    # her place-value working: AB - BA = (10A + B) - (10B + A) = 9A - 9B = 9(A - B); 62 - 26 = 36 = 4 x 9 when she says
    # it (was 12-35 s early); and "AB plus BA is a multiple of 11"
    c6 = item(V, 'c6'); c6['size'] = 25; hand(c6, 'AB − BA = (10A + B) − (10B + A)', '$\\overline{AB}-\\overline{BA}=(10A+B)-(10B+A)$')
    c6b = ns.I('c6b', '$=9A-9B=9(A-B)$', size=30, col=1)
    add(ns, V, 1, 3, c6b, 'nine times the whole')
    c6c = ns.I('c6c', '$62-26=36=4\\cdot9$', size=30, col=1, hand='62 − 26 = 36 = 4·9')
    add(ns, V, 1, 3, c6c, 'Sixty-two minus twenty-six')
    c6d = ns.I('c6d', '$\\overline{AB}+\\overline{BA}$: a multiple of $11$', size=30, col=1)
    add(ns, V, 1, 3, c6d, 'Both patterns appear')
    drop(V, 1, 3, lambda c: c[0] == 'point' and c[1] == 'c6' and c[2] in ('A minus B', 'Sixty-two minus twenty-six'))


def _q520(ns, V):
    # she stopped after "Thirty and twenty-four are in": both choices crossed there
    rephrase(ns, V, 2, 2, is_mark('cross', 'choice 4', 'choice numbers two and four are out'), 'twenty-four are in')


def _q517(ns, V):
    # she said "That gives sixteen, which the square is too small" - no 256, no "starting with six"
    i2 = item(V, 'i2'); hand(i2, '(1)  6 :   C = 0  ✗', '(1) $6$: $\\ C=0$ ✗')
    i2b = ns.I('i2b', '(3) $5$: $\\ 16^2$ is too small ✗', size=30, hand='(3)  5 :   16^2  too small  ✗')
    add(ns, V, 1, 1, i2b, 'That gives sixteen')
    rephrase(ns, V, 1, 1, is_mark('cross', 'choice 3', 'two hundred fifty'), 'So this choice is out')
    drop(V, 1, 1, is_point('i2', 'this choice is'))


FIX = {
    'solve-q-359': _q359, 'solve-q-r26-t13-13': _t13_13, 'solve-q-r26-t13-01': _t13_01, 'solve-q-369': _q369,
    'solve-q-402': _q402, 'solve-q-r26-t14-01': _t14_01, 'primes-2': _primes2, 'prime-tools': _prime_tools,
    'solve-q-389': _q389,
    'solve-q-432': _q432, 'solve-q-436': _q436,
    'r26-t16-consecutive-sums': _cons_sums, 'solve-q-457': _q457, 'solve-q-458': _q458,
    'solve-q-496': _q496, 'solve-q-497': _given_said, 'solve-q-501': _given_said, 'solve-q-r26-t17-04': _given_said,
    'solve-q-r26-t17-05': _t17_05,
    'solve-q-514': _q514, 'solve-q-520': _q520, 'solve-q-517': _q517,
}


def post(ns, topic, mv):
    """called by _method_visuals.post (mv = that module) after its own fixes, carry-overs and calm()"""
    global _MV
    _MV = mv
    for vid, fn in FIX.items():
        if vid in ns.VIDEOS: fn(ns, ns.VIDEOS[vid])
