"""Topic 2 - Fractions: Fundamentals.  Course review 2026-09 (student_review/review_t1-2.md).

1. Wording fixes in the videos (Expanding slide, spelling), ":" as division -> "÷" on boards, draw notes and cards.
2. New teaching: splitting a numerator, negative fractions, "of" = times / "of the rest", LCM named,
   fraction bar = brackets (stacked fractions with sums), mixed operations, ÷0.5 / ÷0.25 / ÷0.2 / ÷0.125,
   and a short strong-student lesson (estimate & eliminate, test a rule with numbers, cross shortcut,
   mixed numbers part by part). 5 guided questions with solution videos, 19 new practice questions, 2 new cards.
3. Every written solution rewritten with real fractions ($\\frac{}{}$) and numbers.
5. Practice: (Pass 2: q-041, q-042, q-045 and the original extra-2 restored; q-018 received from Topic 1), answer positions shuffled, practice ordered easy -> hard.
"""
import re
from dsl import T, H, A, D, Q, P

TOPIC = 2
QN = 'q-r26-t02-%02d'
SOLVE_SIDEBAR = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5']


# ---------------------------------------------------------------- helpers
def _renumber_actives(M, vid):
    """Every concept/question slide has its own sidebar entry, in order (title slide = -1)."""
    v = M.video(vid)
    for n, b in enumerate(v['beats']):
        b['active'] = -1 if b['mode'] == 'title' else n - 1
    M.touched_videos.add(vid)


def _draw_fix(s):
    s = re.sub(r'"\s*:(?=\d)', '"÷', s)                       # "":6"" -> ""÷6""
    s = re.sub(r'(?<=[\d/])\s?:\s?(?=\d)', ' ÷ ', s)          # 5/6 : 10/9 -> 5/6 ÷ 10/9
    s = s.replace("':  →", "'÷  →")
    return s


def _tex_fix(t):
    t = t.replace('$:$', '$\\div$')
    return re.sub(r'(?<=[\d}])\s*:\s*(?=[\d\\])', r'\\div ', t)


def _fix_colons(M):
    for vid in ('fraction-basics', 'fraction-multiply', 'fraction-add', 'decimals'):
        v = M.video(vid)
        for b in v['beats']:
            for l in b['lines']:
                if 'draw' in l: l['draw'] = _draw_fix(l['draw'])
                if 'label' in l: l['label'] = _draw_fix(l['label'])
            for it in b['items']:
                if it.get('t'): it['t'] = _tex_fix(it['t'])
            if b.get('canvas'): b['canvas'] = _draw_fix(b['canvas'])
        M.touched_videos.add(vid)


def _say_replace(M, vid, n, old, new):
    """Replace one spoken line (exact text) by one or more lines."""
    new = [new] if isinstance(new, str) else new
    def fn(lines):
        out = []; hit = False
        for l in lines:
            if l.get('say') == old:
                out += [{'say': s} for s in new]; hit = True
            else: out.append(l)
        assert hit, (vid, n, old)
        return out
    M.edit_lines(vid, n, fn)


def _guided(M, qid, section, after, title, intro, slide_title, script):
    N = M.next_question_number(TOPIC)
    M.place_q(qid, section, after=after)
    M.new_video('solve-' + qid, TOPIC, title, SOLVE_SIDEBAR, [
        dict(mode='title', title='Question %d' % N, script=intro),
        dict(mode='question', active=N - 1, title=slide_title, pre=[Q(qid)], script=script),
    ], section, kind='solution', qid=qid)


# ---------------------------------------------------------------- 1 + 3: videos, wording
def fix_videos(M):
    _fix_colons(M)
    # Expanding: the "two halves" line was unclear (review, weak student)
    _say_replace(M, 'fraction-basics', 7,
                 "Change only one of them? You've changed the amount. Two quarters is a half — but two halves is a whole.",
                 ["Change only one of them? You've changed the amount.",
                  "Change only the bottom of two quarters, and you get two halves. Two halves is one whole — not one half."])
    _say_replace(M, 'fraction-basics', 6, "The pieces didn't change size, so the denominator stays five.",
                 "The pieces didn't change size. The denominator stays five.")
    _say_replace(M, 'decimals', 8, "Times ten — the number has to grow, so the point moves one place to the RIGHT.",
                 "Times ten — the number has to grow. The point moves one place to the RIGHT.")
    _say_replace(M, 'fraction-multiply', 1,
                 "And we'll use the reducing skills from the last lesson. If those still feel shaky — go back and practise first.",
                 "And we'll use the reducing skills from the last lesson. If those still feel shaky — go back and practice first.")
    # Add/Sub slide 5: name the LCM (used in the written solutions)
    b = M.slide('fraction-add', 5)
    script = []
    for l in b['lines']:
        if 'say' in l: script.append(l['say'])
        elif 'appear' in l: script.append(A(l['label'], b['items'][l['appear']]))
        else: script.append(D(l['draw']))
        if l.get('say', '').startswith('Twelve — does eight go in?'):
            script += [A('"24 = LCM of 8 and 12" appears', T('$24$ = LCM of $8$ and $12$ = the smallest common denominator', size=36)),
                       "Twenty-four has a name: the LCM — the least common multiple of eight and twelve.",
                       "It's the smallest common denominator. You'll see \"LCM\" in the written solutions."]
    M.set_slide('fraction-add', 5, script=script)


# ---------------------------------------------------------------- 2: new slides
def lesson_basics(M):
    vid = 'fraction-basics'
    M.insert_slides(vid, 10, [
        dict(title='Splitting the top', mode='concept', script=[
            "One move that IS allowed with a sum on top: split it.",
            A('(6 + 5)/7 = 6/7 + 5/7 appears', T('$\\frac{6+5}{7}=\\frac{6}{7}+\\frac{5}{7}$', size=60)),
            "Eleven sevenths is six sevenths plus five sevenths. Every part of the top keeps the same denominator.",
            A('(12 + 8)/4 = 12/4 + 8/4 = 3 + 2 = 5 appears', T('$\\frac{12+8}{4}=\\frac{12}{4}+\\frac{8}{4}=3+2=5$', size=54)),
            "Twelve plus eight, over four. Split it: three plus two. Five.",
            D('Beside it write "20/4 = 5 ✓"'),
            "Check: twenty over four is five. Same answer.",
            A('7/(3 + 4) ≠ 7/3 + 7/4 appears', T('$\\frac{7}{3+4}\\ne\\frac{7}{3}+\\frac{7}{4}$', size=54)),
            D('Draw a big ✗ over the right side'),
            "But never split the bottom. Seven over seven is one. Seven thirds plus seven quarters is about four.",
            "Split the top — never the bottom.",
        ]),
        dict(title='Negative fractions', mode='concept', script=[
            "In Topic 1 we met negative numbers. Fractions can be negative too.",
            A('−3/4 = (−3)/4 = 3/(−4) appears', T('$-\\frac{3}{4}=\\frac{-3}{4}=\\frac{3}{-4}$', size=60)),
            "A fraction bar is division. Negative divided by positive is negative. Positive divided by negative is negative too.",
            "One minus sign can sit in front, on top, or at the bottom. It's the same number.",
            A('(−3)/(−4) = 3/4 appears', T('$\\frac{-3}{-4}=\\frac{3}{4}$', size=60)),
            "Two minus signs? Negative divided by negative is positive. They cancel.",
            A('−(3 + 1)/4 = (−3 − 1)/4 appears', T('$-\\frac{3+1}{4}=\\frac{-3-1}{4}$', size=60)),
            "Here's the trap. A minus in front of a fraction belongs to the WHOLE top.",
            "Move it up, and it flips every sign in the top — like a minus before brackets.",
            D('Write "= −4/4 = −1"'),
            "Minus four quarters: minus one.",
        ]),
    ])
    M.set_sidebar(vid, ['Part of a whole', 'Parts of a fraction', 'Improper & mixed', 'Improper → mixed', 'Mixed → improper',
                        'Expanding', 'Reducing', 'Bigger or smaller?', 'What cancelling means', 'Splitting the top',
                        'Negative fractions', 'Recap'])
    M.set_slide(vid, 13, script=[
        "Let's lock it in.",
        A("'Numerator: how many pieces · Denominator: how many make a whole' appears", T('Numerator: how many pieces · Denominator: how many make a whole', size=36)),
        A("'Bigger numerator → bigger · Bigger denominator → smaller' appears", T('Bigger numerator $\\to$ bigger · Bigger denominator $\\to$ smaller', size=36)),
        A("'Same factor on top and bottom → same value' appears", T('Same factor on top and bottom $\\to$ same value', size=36)),
        A("'Cancel factors — never terms in a sum' appears", T('Cancel factors — never terms in a sum', size=36)),
        A("'Split the top — never the bottom' appears", T('Split the top — never the bottom: $\\frac{a+b}{c}=\\frac{a}{c}+\\frac{b}{c}$', size=36)),
        A("'−3/4 = (−3)/4 = 3/(−4)' appears", T('$-\\frac{3}{4}=\\frac{-3}{4}=\\frac{3}{-4}$ · two minus signs cancel', size=36)),
        D('Underline "smaller" in the second line'),
        "This lesson is the foundation for every fraction you'll meet — in algebra, word problems and geometry.",
        "A guided question next, then practice. Before you calculate, say what the numbers are counting.",
        "Next: multiplying and dividing fractions.",
    ])
    _renumber_actives(M, vid)


def lesson_multiply(M):
    vid = 'fraction-multiply'
    M.insert_slides(vid, 2, [
        dict(title='"Of" means times', mode='concept', script=[
            "Word problems love one little word: OF.",
            A('"2/3 of 36" appears', T('$\\frac{2}{3}$ of $36$', size=60)),
            "Two thirds of thirty-six. In math, OF means times.",
            A('2/3 · 36 = 24 appears', T('$\\frac{2}{3}\\cdot36=\\frac{2\\cdot36}{3}=24$', size=54)),
            "Thirty-six split into thirds: twelve each. Two of them: twenty-four.",
            "We saw it on the grid: three quarters OF two fifths is three quarters TIMES two fifths.",
            A("'Spend 1/3, then 1/4 of the rest' appears", T('Spend $\\frac{1}{3}$, then $\\frac{1}{4}$ of the rest', size=42)),
            "Now a classic exam trap. Someone spends one third of their money. Then one quarter of the REST.",
            A("'After step 1: 1 − 1/3 = 2/3 left' appears", T('After step 1: $1-\\frac{1}{3}=\\frac{2}{3}$ left', size=42)),
            "After the first step, two thirds are left.",
            A("'After step 2: 3/4 · 2/3 = 1/2 left' appears", T('After step 2: $\\frac{3}{4}\\cdot\\frac{2}{3}=\\frac{1}{2}$ left', size=42)),
            "The second step takes a quarter of THAT. Three quarters of it stay. Three quarters of two thirds: one half.",
            "It's not one minus a third minus a quarter. \"Of the rest\" means of what is left — not of the whole.",
        ]),
    ])
    M.set_sidebar(vid, ['Multiplying', '"Of" means times', 'Cancel first', 'Whole numbers', 'Use the reciprocal', 'Stacked fractions',
                        'Whole over a fraction', 'Mixed numbers', 'What division means', 'Recap'])
    M.set_slide(vid, 11, script=[
        "Let's lock it in.",
        A('The multiplication rule appears: a/b · c/d = ac/bd', T('$\\frac{a}{b}\\cdot\\frac{c}{d}=\\frac{ac}{bd}$', size=52)),
        A("'Of → times. Of the rest → of what is left.' appears", T('"Of" $\\to$ times. "Of the rest" $\\to$ of what is left.', size=40)),
        A("'Cancel first — only across multiplication.' appears", T('Cancel first — only across multiplication.', size=40)),
        A("'Divide → keep, change, flip the second.' appears", T('Divide $\\to$ keep, change, flip the second.', size=40)),
        A("'Mixed numbers → improper fractions first.' appears", T('Mixed numbers $\\to$ improper fractions first.', size=40)),
        D('Circle "the second"'),
        "A guided question next, then practice. Cancel before you multiply — and know which factor you removed.",
        "Next: adding and subtracting fractions. Different operation — different rule.",
    ])
    _renumber_actives(M, vid)


def lesson_add(M):
    vid = 'fraction-add'
    M.insert_slides(vid, 7, [
        dict(title='Fraction bar = brackets', mode='question', pre=[T('$\\dfrac{1+\\frac{1}{2}}{2-\\frac{1}{4}}$', size=80, gap=40)], script=[
            "The exam loves this shape: a stacked fraction with a sum inside.",
            "Remember from Topic 1: a fraction bar works like brackets. Work out the whole top and the whole bottom first.",
            D('Trace over the long main bar'),
            A('The top and bottom worked out: (3/2) over (7/4)', T('$=\\dfrac{\\frac{3}{2}}{\\frac{7}{4}}$', size=64)),
            "Top: one plus a half — three halves. Bottom: two minus a quarter — seven quarters.",
            A('3/2 · 4/7 = 12/14 = 6/7 appears', T('$=\\frac{3}{2}\\cdot\\frac{4}{7}=\\frac{12}{14}=\\frac{6}{7}$', size=54)),
            "Now it's a plain stacked fraction. Multiply by the reciprocal: three halves times four sevenths. Twelve fourteenths — six sevenths.",
            "Don't cross out the one on top against anything below. Those are terms in a sum, not factors.",
        ]),
        dict(title='Mixed operations', mode='concept', script=[
            "Now several operations in one line. Name each operation, then use its rule.",
            A('3/4 − 1/2 · 2/3 appears', T('$\\frac{3}{4}-\\frac{1}{2}\\cdot\\frac{2}{3}$', size=60)),
            "Same order as Topic 1: multiply and divide BEFORE add and subtract.",
            A('= 3/4 − 1/3 = 9/12 − 4/12 = 5/12 appears', T('$=\\frac{3}{4}-\\frac{1}{3}=\\frac{9}{12}-\\frac{4}{12}=\\frac{5}{12}$', size=50)),
            "One half times two thirds is one third. Then three quarters minus one third: nine twelfths minus four twelfths. Five twelfths.",
            A("'Wrong order: (3/4 − 1/2) · 2/3 = 1/6' appears", T('Wrong order: $\\left(\\frac{3}{4}-\\frac{1}{2}\\right)\\cdot\\frac{2}{3}=\\frac{1}{6}$', size=42)),
            D('Draw a big ✗ over the wrong-order line'),
            "Subtract first by mistake? You get one quarter times two thirds — one sixth. The exam will offer you that wrong answer.",
            "Brackets change the order. With brackets, do the bracket first.",
        ]),
    ])
    M.set_sidebar(vid, ['Same denominator', 'Expand just one', 'Expand both', 'Common denominator', 'Subtracting', 'Whole & mixed numbers',
                        'Fraction bar = brackets', 'Mixed operations', 'Recap'])
    M.set_slide(vid, 10, script=[
        "All four operations, side by side.",
        A("'+ −  →  common denominator (LCM), then add the tops' appears", T('$+\\ \\ -$ $\\to$ common denominator (LCM), then add the tops', size=40)),
        A("'×  →  top times top, bottom times bottom' appears", T('$\\times$ $\\to$ top times top, bottom times bottom', size=40)),
        A("'÷  →  multiply by the reciprocal' appears", T('$\\div$ $\\to$ multiply by the reciprocal', size=40)),
        D('Circle the + − line'),
        "Most fraction mistakes come from using the right rule in the wrong place.",
        "So, before you calculate, name the operation. Then say the rule.",
        A("'Several operations → × and ÷ first · a fraction bar is brackets' appears", T('Several operations $\\to$ $\\times$ and $\\div$ first · a fraction bar is brackets', size=38)),
        "And with several operations: multiply and divide first. A fraction bar? Top and bottom first.",
        "A guided question and practice next. Then: fraction shortcuts, and decimal fractions.",
    ])
    _renumber_actives(M, vid)


def lesson_decimals(M):
    vid = 'decimals'
    M.insert_slides(vid, 9, [
        dict(title='÷0.5, ÷0.25, ÷0.2', mode='concept', script=[
            "Three decimals show up again and again in rate and motion questions: zero point five, zero point two five, zero point two.",
            A('0.5 = 1/2, 0.25 = 1/4, 0.2 = 1/5 appears', T('$0.5=\\frac{1}{2} \\qquad 0.25=\\frac{1}{4} \\qquad 0.2=\\frac{1}{5}$', size=50)),
            "Each one is a simple fraction: one half, one quarter, one fifth.",
            A('÷0.5 = ×2, ÷0.25 = ×4, ÷0.2 = ×5 appears', T('$\\div0.5=\\times2 \\qquad \\div0.25=\\times4 \\qquad \\div0.2=\\times5$', size=50)),
            "Dividing by one quarter means multiplying by its reciprocal: four. Dividing by zero point two five is the same as times four.",
            A('3.5 ÷ 0.25 = 3.5 · 4 = 14 appears', T('$3.5\\div0.25=3.5\\cdot4=14$', size=54)),
            "Three point five divided by zero point two five: three point five times four. Fourteen. No long division.",
            A('0.125 = 1/8, ÷0.125 = ×8 appears', T('$0.125=\\frac{1}{8} \\qquad \\div0.125=\\times8$', size=46)),
            "One more for strong students: zero point one two five is one eighth. Dividing by it is times eight.",
        ]),
    ])
    M.set_sidebar(vid, ['Place value', 'Decimal → fraction', 'Fraction → decimal', 'Trailing zeros', 'Adding & subtracting',
                        'Multiplying', '×10 and ÷10', 'Dividing', 'Quick divisors', 'Comparing decimals', 'Recap'])
    M.set_slide(vid, 12, script=[
        "Let's lock it in.",
        A("'Decimal places = zeros in the denominator' appears", T('Decimal places = zeros in the denominator', size=40)),
        A("'Add & subtract: point under point' appears", T('Add & subtract: point under point', size=40)),
        A("'Multiply: count the decimal places — or estimate' appears", T('Multiply: count the decimal places — or estimate', size=40)),
        A("'Divide: expand until both are whole' appears", T('Divide: expand until both are whole', size=40)),
        A("'÷0.5 = ×2 · ÷0.25 = ×4 · ÷0.2 = ×5' appears", T('$\\div0.5=\\times2$ · $\\div0.25=\\times4$ · $\\div0.2=\\times5$', size=40)),
        A('1/3 = 0.333… appears', T('$\\frac{1}{3}=0.333\\ldots$', size=46)),
        "Some fractions never end. One third is zero point three three three — forever. Zero point three three is only an approximation.",
        D('Next to 1/3 write "0.33 ≈ only!"'),
        "On the exam, you'll mostly need adding, subtracting, and expanding by ten to clear a decimal. Multiplying decimals is rare.",
        "A guided question and practice next — then the mixed fraction practice.",
    ])
    _renumber_actives(M, vid)


def lesson_shortcuts(M):
    """New short lesson for strong students, at the end of section 3 (Adding and subtracting)."""
    vid = 'r26-t02-shortcuts'
    M.new_video(vid, TOPIC, 'Fraction Shortcuts', ['Estimate first', 'Test a rule', 'Cross shortcut', 'Mixed numbers fast', 'Recap'], [
        dict(mode='title', title='Fraction Shortcuts', script=[
            "Fraction shortcuts.",
            "You already know the safe methods. They always work.",
            "This lesson is about speed: ways to kill wrong answers without long calculations.",
        ]),
        dict(title='Estimate first', mode='question', pre=[T('$\\frac{8}{9}+\\frac{4}{7}=?$', size=64, gap=30)], script=[
            A('The four choices appear', T('(1) $\\frac{12}{16}$     (2) $1\\frac{29}{63}$     (3) $1\\frac{4}{63}$     (4) $\\frac{32}{63}$', size=42)),
            "Before you calculate, estimate. Use three benchmarks: zero, one half, one.",
            "Eight ninths is almost one. Four sevenths is a little more than a half.",
            A('≈ 1 + 1/2 = 1 1/2 appears', T('$\\approx1+\\frac{1}{2}=1\\frac{1}{2}$', size=50)),
            "The answer is about one and a half.",
            D('Cross out choices 1 and 4'),
            "Choices one and four are less than one. Impossible.",
            D('Cross out choice 3'),
            "One and four sixty-thirds is barely more than one. Too small.",
            D('Circle choice 2'),
            "Twenty-nine sixty-thirds is almost a half. Choice two — and we never found a common denominator.",
        ]),
        dict(title='Test a rule', mode='concept', script=[
            "Not sure if a rule is true? Test it with easy numbers.",
            A('a/b + c/d =? (a + c)/(b + d) appears', T('$\\frac{a}{b}+\\frac{c}{d}\\overset{?}{=}\\frac{a+c}{b+d}$', size=56)),
            "A common mistake: add the tops and add the bottoms. Is that allowed?",
            A("'1/2 + 1/2 = 1, but (1 + 1)/(2 + 2) = 1/2' appears", T('$\\frac{1}{2}+\\frac{1}{2}=1$, but $\\frac{1+1}{2+2}=\\frac{1}{2}$', size=50)),
            "Try one half plus one half. We know it's one. The \"rule\" gives two quarters — one half. Wrong!",
            D('Draw a big ✗ over the rule'),
            "One example that fails kills a rule. Test easy numbers: one, two, one half.",
            "But one example that works does not prove a rule. Try a second pair to be safe.",
        ]),
        dict(title='Cross shortcut', mode='concept', script=[
            "Adding two fractions fast: the cross shortcut.",
            A('a/b + c/d = (ad + bc)/bd appears', T('$\\frac{a}{b}+\\frac{c}{d}=\\frac{ad+bc}{bd}$', size=58)),
            "Top: multiply across and add. Bottom: multiply the bottoms.",
            A('2/3 + 3/5 = (2·5 + 3·3)/(3·5) = 19/15 appears', T('$\\frac{2}{3}+\\frac{3}{5}=\\frac{2\\cdot5+3\\cdot3}{3\\cdot5}=\\frac{19}{15}$', size=50)),
            "Two times five is ten. Three times three is nine. Nineteen fifteenths.",
            "It's the common denominator b times d — just faster to write. Reduce at the end if you can.",
            A('1/4 − 1/5 = (5 − 4)/(4·5) = 1/20 appears', T('$\\frac{1}{4}-\\frac{1}{5}=\\frac{5-4}{4\\cdot5}=\\frac{1}{20}$', size=50)),
            "With ones on top it's even faster. One quarter minus one fifth: five minus four, over twenty. One twentieth.",
            "Watch the order on top: the SECOND bottom minus the first bottom.",
        ]),
        dict(title='Mixed numbers fast', mode='question', pre=[T('$4\\frac{2}{3}-2\\frac{1}{4}$', size=64, gap=30)], script=[
            "The safe way for mixed numbers: make them improper. Here's a faster way when the numbers are friendly.",
            A('= (4 − 2) + (2/3 − 1/4) appears', T('$=(4-2)+\\left(\\frac{2}{3}-\\frac{1}{4}\\right)$', size=50)),
            "Whole parts: four minus two — two. Fraction parts: two thirds minus one quarter.",
            A('= 2 + 8/12 − 3/12 = 2 5/12 appears', T('$=2+\\frac{8}{12}-\\frac{3}{12}=2\\frac{5}{12}$', size=50)),
            "Eight twelfths minus three twelfths: five twelfths. Two and five twelfths.",
            A("'3 1/6 − 1 3/4: 1/6 < 3/4 → use improper fractions' appears", T('$3\\frac{1}{6}-1\\frac{3}{4}$: $\\frac{1}{6}<\\frac{3}{4}$ $\\to$ use improper fractions', size=40)),
            "But if the second fraction part is bigger — like one sixth minus three quarters — it gets messy.",
            "Then use the safe way: improper fractions.",
        ]),
        dict(title='Recap', mode='concept', script=[
            "Let's lock it in.",
            A("'Estimate with 0, 1/2, 1 — kill choices' appears", T('Estimate with $0$, $\\frac{1}{2}$, $1$ — kill choices', size=40)),
            A("'Test a rule with easy numbers' appears", T('Not sure of a rule? Test it with easy numbers', size=40)),
            A('a/b + c/d = (ad + bc)/bd appears', T('$\\frac{a}{b}+\\frac{c}{d}=\\frac{ad+bc}{bd}$', size=46)),
            A("'Mixed numbers: whole parts + fraction parts (no borrowing)' appears", T('Mixed numbers: whole parts, then fraction parts — if no borrowing', size=40)),
            "These are for speed. When in doubt, the safe method always works.",
            "A guided question next: one where estimating beats calculating.",
        ]),
    ], 'fraction-add')
    return vid


# ---------------------------------------------------------------- memory cards
def cards(M):
    M.new_card('mem-r26-t02-basics', TOPIC, 'fraction-basics', dict(
        title='Fraction basics',
        intro='What a fraction is — and the moves that keep its value.',
        tables=[{'title': '', 'head': ['Idea', 'Rule', 'Example'], 'rows': [
            ['Numerator / denominator', 'top: pieces we have · bottom: equal pieces in one whole', '$\\frac{3}{4}$'],
            ['Improper → mixed', 'how many times it fits; remainder on top', '$\\frac{15}{4}=3\\frac{3}{4}$'],
            ['Mixed → improper', 'whole × denominator + numerator, same denominator', '$2\\frac{3}{5}=\\frac{13}{5}$'],
            ['Expand / reduce', 'same factor on top and bottom', '$\\frac{3}{5}=\\frac{12}{20}$, $\\frac{18}{24}=\\frac{3}{4}$'],
            ['Cancel', 'only a factor of the WHOLE top and the WHOLE bottom', '$\\frac{6\\cdot5}{6\\cdot7}=\\frac{5}{7}$'],
            ['Split the top', 'allowed on top — never on the bottom', '$\\frac{12+8}{4}=\\frac{12}{4}+\\frac{8}{4}=5$'],
            ['Negative fractions', 'one minus sign can sit anywhere; two cancel', '$-\\frac{3}{4}=\\frac{-3}{4}=\\frac{3}{-4}$, $\\frac{-3}{-4}=\\frac{3}{4}$'],
        ]}],
        tips=['Bigger numerator → bigger fraction. Bigger denominator → smaller fraction.',
              'A denominator can never be 0.',
              'A minus in front of a fraction belongs to the whole top: $-\\frac{3+1}{4}=\\frac{-3-1}{4}$.']),
        after='fraction-basics')
    M.new_card('mem-r26-t02-multiply', TOPIC, 'fraction-multiply', dict(
        title='Multiplying & dividing',
        intro='No common denominator needed — that is only for adding.',
        tables=[{'title': '', 'head': ['Case', 'Rule', 'Example'], 'rows': [
            ['Multiply', 'top × top, bottom × bottom (cancel first)', '$\\frac{14}{15}\\cdot\\frac{25}{21}=\\frac{10}{9}$'],
            ['"Of"', 'means times', '$\\frac{2}{3}$ of $36=\\frac{2}{3}\\cdot36=24$'],
            ['"Of the rest"', 'take the part of what is left', 'spend $\\frac{1}{3}$, then $\\frac{1}{4}$ of the rest: $\\frac{3}{4}\\cdot\\frac{2}{3}=\\frac{1}{2}$ left'],
            ['Divide', 'keep, change, flip the second', '$\\frac{3}{4}\\div\\frac{2}{5}=\\frac{3}{4}\\cdot\\frac{5}{2}=\\frac{15}{8}$'],
            ['Stacked fraction', 'the main bar means ÷', '$\\dfrac{\\frac{5}{6}}{\\frac{10}{9}}=\\frac{5}{6}\\cdot\\frac{9}{10}=\\frac{3}{4}$'],
            ['Mixed numbers', 'improper fractions first', '$1\\frac{2}{3}\\cdot\\frac{3}{5}=\\frac{5}{3}\\cdot\\frac{3}{5}=1$'],
        ]}],
        tips=['Cancel only across multiplication — never with a + or − inside.',
              'Dividing a positive number by a fraction between 0 and 1 makes it bigger: $\\frac{3}{4}\\div\\frac{1}{8}=6$.']),
        after='fraction-multiply')
    c = M.card('mem-fractions')
    rows = c['tables'][0]['rows']
    for r in rows:
        r[2] = _tex_fix(r[2])
    rows[0][1] = 'common denominator (the LCM), then add or subtract the tops'
    rows.insert(3, ['"Of"', 'means times', '$\\frac{2}{3}$ of $36=24$'])
    rows.append(['Several operations', '× and ÷ before + and −; a fraction bar is brackets',
                 '$\\frac{3}{4}-\\frac{1}{2}\\cdot\\frac{2}{3}=\\frac{3}{4}-\\frac{1}{3}=\\frac{5}{12}$'])
    c['tips'].append('LCM = least common multiple = the smallest common denominator.')
    c['tips'].append('Fast add: $\\frac{a}{b}+\\frac{c}{d}=\\frac{ad+bc}{bd}$. Estimate first with $0$, $\\frac{1}{2}$, $1$.')
    d = M.card('mem-decimals')
    d['tables'][0]['rows'] += [['$\\frac{2}{3}$', '$0.666\\ldots$ (never exact)', '$\\frac{3}{5}$', '$0.6$'],
                               ['$\\frac{1}{6}$', '$0.1666\\ldots$ (never exact)', '$\\frac{4}{5}$', '$0.8$'],
                               ['$\\frac{1}{20}$', '$0.05$', '$\\frac{1}{25}$', '$0.04$']]
    d['tables'][1]['rows'][1][0] = '$\\div10,\\ \\div100,\\ \\div1000$'
    d['tables'].append({'title': 'Quick division', 'head': ['Divide by', 'Same as'], 'rows': [
        ['$\\div0.5$', '$\\times2$'], ['$\\div0.25$', '$\\times4$'], ['$\\div0.2$', '$\\times5$'], ['$\\div0.125$', '$\\times8$']]})


# ---------------------------------------------------------------- 3: rewrite every existing solution
def rewrite_existing(M):
    E = {
        'q-076': ["The denominator went from 4 to 24: it was multiplied by 6. Multiply the numerator by 6 as well: $3\\cdot6=18$.",
                  "$\\frac{3}{4}=\\frac{18}{24}$. The answer is 18."],
        'q-077': ["$240\\div60=4$: 60 fits into 240 exactly four times.",
                  "Divide top and bottom by 60: $\\frac{60}{240}=\\frac{1}{4}$."],
        'q-078': ["Reduce first (divide top and bottom by 3): $\\frac{6}{15}=\\frac{2}{5}$.",
                  "Then expand to tenths (multiply top and bottom by 2): $\\frac{2}{5}=\\frac{4}{10}$. The missing numerator is 4."],
        'q-079': ["$29\\div6=4$ remainder 5 ($6\\cdot4=24$ and $29-24=5$).",
                  "The whole part is 4, and the remainder goes on top: $\\frac{29}{6}=4\\frac{5}{6}$."],
        'q-080': ["Mixed to improper: $7\\cdot5+2=37$, over the same denominator: $7\\frac{2}{5}=\\frac{37}{5}$."],
        'q-071': ["Reduce each factor first: $\\frac{6}{12}=\\frac{1}{2}$ and $\\frac{2}{8}=\\frac{1}{4}$.",
                  "Then $\\frac{1}{2}\\cdot\\frac{1}{4}=\\frac{1}{8}$."],
        'q-072': ["Convert the mixed number: $4\\frac{2}{3}=\\frac{4\\cdot3+2}{3}=\\frac{14}{3}$.",
                  "Then $\\frac{15}{14}\\cdot\\frac{14}{3}$: the 14s cancel, leaving $\\frac{15}{3}=5$."],
        'q-073': ["Keep, change, flip: $\\frac{7}{12}\\div\\frac{1}{3}=\\frac{7}{12}\\cdot\\frac{3}{1}$.",
                  "Cancel 3 into 12 (1 and 4): $\\frac{7}{4}\\cdot\\frac{1}{1}=\\frac{7}{4}=1\\frac{3}{4}$.",
                  "The distractor $\\frac{7}{36}$ comes from multiplying by $\\frac{1}{3}$ without flipping."],
        'q-074': ["The main fraction bar means division: $\\frac{7}{5}\\div\\frac{3}{5}=\\frac{7}{5}\\cdot\\frac{5}{3}$.",
                  "The 5s cancel, leaving $\\frac{7}{3}=2\\frac{1}{3}$."],
        'q-075': ["Convert: $3\\frac{1}{5}=\\frac{3\\cdot5+1}{5}=\\frac{16}{5}$.",
                  "Then $8\\div\\frac{16}{5}=\\frac{8}{1}\\cdot\\frac{5}{16}$. Cancel 8 into 16 (1 and 2): $\\frac{1}{1}\\cdot\\frac{5}{2}=\\frac{5}{2}=2\\frac{1}{2}$."],
        'q-066': ["Same denominators: add the numerators and keep the denominator: $\\frac{3}{8}+\\frac{2}{8}=\\frac{5}{8}$.",
                  "The distractor $\\frac{5}{16}$ comes from also adding the denominators."],
        'q-067': ["Convert to eighths: $\\frac{1}{2}=\\frac{4}{8}$.",
                  "Then $\\frac{4}{8}-\\frac{3}{8}=\\frac{1}{8}$."],
        'q-068': ["The common denominator is 15, the LCM (least common multiple) of 3 and 5: $\\frac{1}{3}=\\frac{5}{15}$ and $\\frac{1}{5}=\\frac{3}{15}$.",
                  "The sum is $\\frac{5}{15}+\\frac{3}{15}=\\frac{8}{15}$."],
        'q-069': ["Convert: $4\\frac{2}{3}=\\frac{14}{3}$ and $2\\frac{1}{4}=\\frac{9}{4}$.",
                  "Common denominator 12: $\\frac{56}{12}-\\frac{27}{12}=\\frac{29}{12}=2\\frac{5}{12}$."],
        'q-070': ["Convert to tenths: $\\frac{2}{5}=\\frac{4}{10}$.",
                  "Then $\\frac{4}{10}-\\frac{1}{10}+\\frac{7}{10}=\\frac{10}{10}=1$."],
        'q-061': ["Two decimal places: $0.45=\\frac{45}{100}$.",
                  "Divide top and bottom by 5: $\\frac{45}{100}=\\frac{9}{20}$."],
        'q-062': ["Expand to hundredths (multiply top and bottom by 4): $\\frac{18}{25}=\\frac{72}{100}=0.72$."],
        'q-063': ["Write 12.3 as 12.30 and subtract with the points lined up: $12.30-4.15=8.15$."],
        'q-064': ["Multiply top and bottom by 10: $\\frac{18}{0.6}=\\frac{180}{6}=30$."],
        'q-065': ["Multiply the digits: $9\\cdot9=81$.",
                  "One decimal place in each factor makes two in the product: $0.9\\cdot0.9=0.81$."],
        'q-043': ["The greatest common divisor of 27 and 45 is 9.",
                  "Divide both: $27\\div9=3$ and $45\\div9=5$. The result is $\\frac{27}{45}=\\frac{3}{5}$."],
        'q-044': ["$52\\div10=5$ remainder 2. That gives $\\frac{52}{10}=5\\frac{2}{10}$.",
                  "Reduce the fraction part: $\\frac{2}{10}=\\frac{1}{5}$. The answer is $5\\frac{1}{5}$."],
        'q-046': ["Reduce before multiplying: $\\frac{6}{15}=\\frac{2}{5}$.",
                  "Then $\\frac{2}{5}\\cdot\\frac{5}{8}$: the 5s cancel, leaving $\\frac{2}{8}=\\frac{1}{4}$."],
        'q-047': ["Convert the mixed number: $2\\frac{1}{2}=\\frac{5}{2}$.",
                  "Cancel first: $\\frac{7}{35}=\\frac{1}{5}$. Then $\\frac{5}{2}\\cdot\\frac{1}{5}$: the 5s cancel, leaving $\\frac{1}{2}$."],
        'q-048': ["Keep, change, flip: $\\frac{6}{25}\\div\\frac{9}{5}=\\frac{6}{25}\\cdot\\frac{5}{9}$.",
                  "Cancel first: 6 and 9 share a 3 (they become 2 and 3). 5 and 25 share a 5 (they become 1 and 5).",
                  "$\\frac{2}{5}\\cdot\\frac{1}{3}=\\frac{2}{15}$.",
                  "The distractor $\\frac{54}{125}$ comes from multiplying without flipping."],
        'q-049': ["The main bar means division: $\\frac{2}{9}\\div\\frac{8}{3}=\\frac{2}{9}\\cdot\\frac{3}{8}$.",
                  "Cancel 2 into 8 (1 and 4) and 3 into 9 (1 and 3): $\\frac{1}{3}\\cdot\\frac{1}{4}=\\frac{1}{12}$.",
                  "The distractor $\\frac{16}{27}$ comes from multiplying instead of dividing."],
        'q-050': ["The main bar means division. Dividing by $\\frac{1}{8}$ is multiplying by 8: $4\\cdot8=32$.",
                  "The distractor $\\frac{1}{2}$ comes from multiplying by $\\frac{1}{8}$ instead of by its reciprocal."],
        'q-051': ["Common denominator 8: $\\frac{1}{4}=\\frac{2}{8}$.",
                  "Then $\\frac{2}{8}+\\frac{3}{8}=\\frac{5}{8}$."],
        'q-052': ["Common denominator 9: $\\frac{1}{3}=\\frac{3}{9}$.",
                  "Then $\\frac{5}{9}-\\frac{3}{9}=\\frac{2}{9}$."],
        'q-053': ["The LCM of 18 and 12 is 36 (multiples of 18: 18 no, 36 yes).",
                  "$\\frac{5}{18}=\\frac{10}{36}$ and $\\frac{7}{12}=\\frac{21}{36}$. The sum is $\\frac{10}{36}+\\frac{21}{36}=\\frac{31}{36}$."],
        'q-054': ["Method 1: convert $3\\frac{1}{4}=\\frac{13}{4}$. The LCM of 4 and 9 is 36: $\\frac{13}{4}=\\frac{117}{36}$ and $\\frac{7}{9}=\\frac{28}{36}$.",
                  "Subtract: $\\frac{117-28}{36}=\\frac{89}{36}=2\\frac{17}{36}$.",
                  "Method 2 (estimate and eliminate): $\\frac{7}{9}$ is a little more than $\\frac{3}{4}$. The answer is a little less than $3\\frac{1}{4}-\\frac{3}{4}=2\\frac{1}{2}$.",
                  "That kills $2\\frac{1}{2}$ and $2\\frac{19}{36}$ (it is more than $2\\frac{18}{36}=2\\frac{1}{2}$). A denominator of 13 is impossible: 4 and 9 lead to 36. Only $2\\frac{17}{36}$ is left."],
        'q-055': ["The LCM of 20, 4 and 5 is 20: $\\frac{3}{4}=\\frac{15}{20}$ and $\\frac{3}{5}=\\frac{12}{20}$.",
                  "Then $\\frac{7}{20}+\\frac{15}{20}-\\frac{12}{20}=\\frac{10}{20}=\\frac{1}{2}$."],
        'q-056': ["The trailing zero changes nothing: $0.250=0.25=\\frac{25}{100}=\\frac{1}{4}$."],
        'q-057': ["Reduce first (divide top and bottom by 6): $\\frac{6}{120}=\\frac{1}{20}$.",
                  "Then expand to hundredths: $\\frac{1}{20}=\\frac{5}{100}=0.05$."],
        'q-058': ["Compensate: 8.85 is 0.15 less than 9. Subtract 9: $30.25-9=21.25$.",
                  "We took away 0.15 too much. Add it back: $21.25+0.15=21.40=21.4$."],
        'q-059': ["Clear the decimal: multiply top and bottom by 10: $\\frac{12}{1.5}=\\frac{120}{15}=8$."],
        'q-060': ["Multiply the digits: $3\\cdot6=18$.",
                  "One decimal place in each factor makes two in the product: $0.3\\cdot0.6=0.18$."],
    }
    for qid, ex in E.items():
        M.set_q(qid, expl=ex)
    # stems: ":" -> "÷", and no power before powers are taught
    M.set_q('q-073', stem=' $\\frac{7}{12} \\div \\frac{1}{3} = ?$ ')
    M.set_q('q-075', stem=' $8 \\div 3\\,\\frac{1}{5} = ?$ ')
    M.set_q('q-048', stem=' $\\frac{6}{25} \\div \\frac{9}{5} = ?$ ')
    M.set_q('q-065', stem=' $0.9 \\cdot 0.9 = ?$ ')

    # extra practice questions: numbers in every solution, shuffled answer positions, extra-2 replaced
    X = 'alg-extra-unit-t2-1-%d'
    M.set_q(X % 1, stem='Evaluate $\\frac{3}{6}+\\frac{1}{4}$.',
            choices=['$\\frac{1}{4}$', '$\\frac{2}{3}$', '$1$', '$\\frac{3}{4}$'], correct=4,
            expl=["Reduce first: $\\frac{3}{6}=\\frac{1}{2}=\\frac{2}{4}$.",
                  "Then $\\frac{2}{4}+\\frac{1}{4}=\\frac{3}{4}$."])
    # Pass 2 (plan): the original extra-2 (5/6 - 1/4) is restored; the 7/10 - 1/4 version stays as q-r26-t02-25
    M.set_q(X % 2, stem='Evaluate $\\frac{5}{6}-\\frac{1}{4}$.',
            choices=['$\\frac{7}{12}$', '$\\frac{1}{2}$', '$\\frac{2}{3}$', '$\\frac{1}{3}$'], correct=1,
            expl=["The LCM of 6 and 4 is 12: $\\frac{5}{6}=\\frac{10}{12}$ and $\\frac{1}{4}=\\frac{3}{12}$.",
                  "$\\frac{10}{12}-\\frac{3}{12}=\\frac{7}{12}$."])
    M.new_q(QN % 25, TOPIC, 'Evaluate $\\frac{7}{10}-\\frac{1}{4}$.',
            ['$\\frac{3}{5}$', '$1$', '$\\frac{9}{20}$', '$\\frac{19}{20}$'], 3,
            ["The LCM of 10 and 4 is 20: $\\frac{7}{10}=\\frac{14}{20}$ and $\\frac{1}{4}=\\frac{5}{20}$.",
             "$\\frac{14}{20}-\\frac{5}{20}=\\frac{9}{20}$.",
             "Choice 4 ($\\frac{19}{20}$) adds instead of subtracting. Choice 2 ($1$) subtracts tops and bottoms: $\\frac{7-1}{10-4}=\\frac{6}{6}$."])
    M.set_q(X % 3, stem='Evaluate $\\frac{9}{7}\\cdot\\frac{14}{3}$.',
            choices=['$12$', '$6$', '$3$', '$7$'], correct=2,
            expl=["Cancel first: 3 into 9 (they become 1 and 3) and 7 into 14 (they become 1 and 2).",
                  "$\\frac{3}{1}\\cdot\\frac{2}{1}=6$."])
    M.set_q(X % 4, stem='Evaluate $\\frac{3}{4}\\div\\frac{9}{10}$.',
            choices=['$\\frac{27}{40}$', '$\\frac{6}{5}$', '$\\frac{2}{3}$', '$\\frac{5}{6}$'], correct=4,
            expl=["Multiply by the reciprocal: $\\frac{3}{4}\\div\\frac{9}{10}=\\frac{3}{4}\\cdot\\frac{10}{9}$.",
                  "Cancel 3 into 9 (1 and 3) and 2 into 4 and 10 (2 and 5): $\\frac{1}{2}\\cdot\\frac{5}{3}=\\frac{5}{6}$.",
                  "Choice 1 ($\\frac{27}{40}$) comes from multiplying without flipping."])
    M.set_q(X % 5, stem='Which fraction is equal to $0.375$?',
            choices=['$\\frac{3}{5}$', '$\\frac{37}{100}$', '$\\frac{3}{8}$', '$\\frac{1}{4}$'], correct=3,
            expl=["Three decimal places: $0.375=\\frac{375}{1000}$.",
                  "Divide top and bottom by 125: $375\\div125=3$ and $1000\\div125=8$. The answer is $\\frac{3}{8}$."])
    M.set_q(X % 6, stem='A ribbon is $\\frac{7}{2}$ meters long. It is cut into pieces of $\\frac{1}{2}$ meter each, with no waste. How many pieces are made?',
            choices=['$6$', '$7$', '$8$', '$3$'], correct=2,
            expl=["Divide the total length by the length of one piece: $\\frac{7}{2}\\div\\frac{1}{2}=\\frac{7}{2}\\cdot\\frac{2}{1}=7$.",
                  "Check: 7 pieces of half a meter are $\\frac{7}{2}$ meters."])
    M.set_q(X % 7, expl=["Swap the numerator and the denominator and keep the minus sign: the reciprocal of $-\\frac{3}{5}$ is $-\\frac{5}{3}$.",
                         "Check: $-\\frac{3}{5}\\cdot\\left(-\\frac{5}{3}\\right)=1$ (two minus signs make a plus)."])

    # Pass 2 (plan): q-041, q-042 and q-045 are restored (no longer removed), with clean solutions
    M.set_q('q-041', expl=["The numerator went from 5 to 35: it was multiplied by 7.",
                           "To keep the fraction's value, multiply the denominator by 7 too: $6\\cdot7=42$. The answer is 42."])
    M.set_q('q-042', expl=["First reduce (divide top and bottom by 4): $\\frac{4}{12}=\\frac{1}{3}$.",
                           "Then expand $\\frac{1}{3}$ to a denominator of 27: $27\\div3=9$. Multiply top and bottom by 9: $\\frac{1\\cdot9}{3\\cdot9}=\\frac{9}{27}$. The answer is 9."])
    M.set_q('q-045', expl=["Mixed to improper: multiply the whole part by the denominator and add the numerator: $7\\cdot6+1=43$.",
                           "Keep the same denominator: $7\\frac{1}{6}=\\frac{43}{6}$."])


# ---------------------------------------------------------------- new questions
NEW = {
    # --- section 1: splitting the top, negative fractions
    1: dict(stem='$\\frac{-6+15}{-3} = ?$', choices=['$-3$', '$3$', '$17$', '$-7$'], correct=1,
            expl=["The fraction bar works like brackets. Work out the top first: $-6+15=9$.",
                  "$\\frac{9}{-3}=-3$ (positive divided by negative is negative).",
                  "Or split the top: $\\frac{-6}{-3}+\\frac{15}{-3}=2+(-5)=-3$.",
                  "Choice 3 (17) divides only the $-6$ and forgets the 15: $2+15$. The answer is choice 1."]),
    2: dict(stem='Which of the following is NOT equal to $-\\frac{2}{5}$?',
            choices=['$\\frac{-2}{5}$', '$\\frac{2}{-5}$', '$\\frac{-2}{-5}$', '$-\\frac{4}{10}$'], correct=3,
            expl=["$\\frac{-2}{5}$ and $\\frac{2}{-5}$ each have one minus sign. Both are equal to $-\\frac{2}{5}$.",
                  "$-\\frac{4}{10}$ reduces (divide top and bottom by 2) to $-\\frac{2}{5}$.",
                  "$\\frac{-2}{-5}$ has two minus signs. Negative divided by negative is positive: $\\frac{-2}{-5}=\\frac{2}{5}$. The answer is choice 3."]),
    3: dict(stem='$\\frac{48+36}{12} = ?$', choices=['$51$', '$40$', '$7$', '$8$'], correct=3,
            expl=["Split the top: $\\frac{48}{12}+\\frac{36}{12}=4+3=7$.",
                  "Check: $48+36=84$ and $\\frac{84}{12}=7$.",
                  "Choice 1 (51) divides only the 36: $48+3$. Choice 2 (40) divides only the 48: $4+36$."]),
    4: dict(stem='$-\\frac{1-4}{3}+\\frac{-2}{-6} = ?$',
            choices=['$-\\frac{2}{3}$', '$1\\frac{1}{3}$', '$\\frac{2}{3}$', '$-1\\frac{1}{3}$'], correct=2,
            expl=["First fraction: the top is $1-4=-3$. That gives $-\\frac{-3}{3}=-(-1)=1$.",
                  "Second fraction: two minus signs cancel: $\\frac{-2}{-6}=\\frac{2}{6}=\\frac{1}{3}$.",
                  "Sum: $1+\\frac{1}{3}=1\\frac{1}{3}$.",
                  "Choice 1 ($-\\frac{2}{3}$) forgets the minus in front of the first fraction: $-1+\\frac{1}{3}$."]),
    # --- section 2: "of" = times
    5: dict(stem='A water tank holds 240 liters. On Monday, $\\frac{3}{8}$ of the water is used. On Tuesday, $\\frac{2}{5}$ of the remaining water is used. How many liters are left in the tank?',
            choices=['$54$', '$60$', '$150$', '$90$'], correct=4,
            expl=["Monday: $\\frac{3}{8}\\cdot240=90$ liters used. Left: $240-90=150$ liters.",
                  "Tuesday: $\\frac{2}{5}$ of the remaining 150 liters: $\\frac{2}{5}\\cdot150=60$ liters used. Left: $150-60=90$ liters.",
                  "Faster: $\\frac{5}{8}$ stays after Monday and $\\frac{3}{5}$ of that stays after Tuesday: $\\frac{3}{5}\\cdot\\frac{5}{8}\\cdot240=\\frac{3}{8}\\cdot240=90$.",
                  "Choice 1 (54) takes $\\frac{2}{5}$ of the whole tank (96 liters): $240-90-96=54$. The answer is choice 4."]),
    6: dict(stem='What is $\\frac{3}{4}$ of 48?', choices=['$12$', '$32$', '$36$', '$64$'], correct=3,
            expl=["\"Of\" means times: $\\frac{3}{4}\\cdot48=\\frac{3\\cdot48}{4}$.",
                  "$48\\div4=12$, and $3\\cdot12=36$.",
                  "Choice 4 (64) divides by $\\frac{3}{4}$ instead of multiplying: $48\\cdot\\frac{4}{3}=64$."]),
    7: dict(stem='$\\frac{2}{5}$ of a number is 24. What is the number?',
            choices=['$9\\frac{3}{5}$', '$40$', '$36$', '$60$'], correct=4,
            expl=["2 fifths of the number are 24. One fifth is $24\\div2=12$.",
                  "The whole number is 5 fifths: $5\\cdot12=60$.",
                  "Check: $\\frac{2}{5}\\cdot60=24$.",
                  "Choice 1 ($9\\frac{3}{5}$) is $\\frac{2}{5}$ of 24. But 24 is the part, not the whole."]),
    8: dict(stem='Ron read $\\frac{1}{4}$ of a book on Sunday and $\\frac{1}{3}$ of the remaining pages on Monday. He still has 120 pages left to read. How many pages does the book have?',
            choices=['$288$', '$240$', '$160$', '$180$'], correct=2,
            expl=["After Sunday, $1-\\frac{1}{4}=\\frac{3}{4}$ of the book is left.",
                  "On Monday he reads $\\frac{1}{3}$ of the rest. Two thirds of the rest are still left: $\\frac{2}{3}\\cdot\\frac{3}{4}=\\frac{1}{2}$ of the book.",
                  "Half the book is 120 pages. The book has $2\\cdot120=240$ pages.",
                  "Check: Sunday $\\frac{1}{4}\\cdot240=60$, left 180. Monday $\\frac{1}{3}\\cdot180=60$, left 120.",
                  "Choice 1 (288) uses $1-\\frac{1}{4}-\\frac{1}{3}=\\frac{5}{12}$. But the $\\frac{1}{3}$ is of the rest, not of the whole book."]),
    9: dict(stem='A company has 40 workers. $\\frac{3}{8}$ of the workers are women. $\\frac{2}{3}$ of the women work part-time. How many women work full-time?',
            choices=['$10$', '$5$', '$15$', '$25$'], correct=2,
            expl=["Women: $\\frac{3}{8}\\cdot40=15$.",
                  "Part-time women: $\\frac{2}{3}\\cdot15=10$.",
                  "Full-time women: $15-10=5$.",
                  "Choice 1 (10) is the number of part-time women."]),
    # --- section 3: fraction bar = brackets, mixed operations
    10: dict(stem='$\\dfrac{\\frac{2}{3}-\\frac{1}{2}}{\\frac{1}{4}+\\frac{1}{3}} = ?$',
             choices=['$\\frac{7}{72}$', '$\\frac{2}{7}$', '$\\frac{7}{2}$', '$\\frac{7}{12}$'], correct=2,
             expl=["The fraction bar works like brackets. Work out the top and the bottom first.",
                   "Top: $\\frac{2}{3}-\\frac{1}{2}=\\frac{4}{6}-\\frac{3}{6}=\\frac{1}{6}$.",
                   "Bottom: $\\frac{1}{4}+\\frac{1}{3}=\\frac{3}{12}+\\frac{4}{12}=\\frac{7}{12}$.",
                   "Divide: $\\frac{1}{6}\\div\\frac{7}{12}=\\frac{1}{6}\\cdot\\frac{12}{7}=\\frac{2}{7}$ (cancel 6 into 12).",
                   "Choice 3 ($\\frac{7}{2}$) flips the wrong fraction. Choice 1 ($\\frac{7}{72}$) multiplies without flipping."]),
    11: dict(stem='$\\left(\\frac{1}{2}+\\frac{1}{3}\\right)\\div\\frac{5}{6} = ?$',
             choices=['$\\frac{9}{10}$', '$\\frac{25}{36}$', '$1$', '$\\frac{5}{6}$'], correct=3,
             expl=["Bracket first: $\\frac{1}{2}+\\frac{1}{3}=\\frac{3}{6}+\\frac{2}{6}=\\frac{5}{6}$.",
                   "Then $\\frac{5}{6}\\div\\frac{5}{6}=1$ (any nonzero number divided by itself is 1).",
                   "Choice 1 ($\\frac{9}{10}$) ignores the brackets: $\\frac{1}{2}+\\frac{1}{3}\\cdot\\frac{6}{5}=\\frac{1}{2}+\\frac{2}{5}$. Choice 2 multiplies instead of dividing."]),
    12: dict(stem='$\\frac{5}{6}-\\frac{2}{3}\\div\\frac{4}{5} = ?$',
             choices=['$0$', '$\\frac{5}{24}$', '$\\frac{3}{10}$', '$\\frac{1}{6}$'], correct=1,
             expl=["Division comes before subtraction. First: $\\frac{2}{3}\\div\\frac{4}{5}=\\frac{2}{3}\\cdot\\frac{5}{4}=\\frac{10}{12}=\\frac{5}{6}$.",
                   "Then $\\frac{5}{6}-\\frac{5}{6}=0$.",
                   "Choice 2 ($\\frac{5}{24}$) subtracts first: $\\left(\\frac{5}{6}-\\frac{2}{3}\\right)\\div\\frac{4}{5}=\\frac{1}{6}\\cdot\\frac{5}{4}$. Choice 3 ($\\frac{3}{10}$) multiplies by $\\frac{4}{5}$ instead of dividing."]),
    13: dict(stem='$\\dfrac{1}{1+\\dfrac{1}{1+\\frac{1}{2}}} = ?$',
             choices=['$\\frac{2}{3}$', '$\\frac{5}{3}$', '$\\frac{2}{5}$', '$\\frac{3}{5}$'], correct=4,
             expl=["Start with the smallest fraction at the bottom: $1+\\frac{1}{2}=\\frac{3}{2}$.",
                   "One divided by a fraction is its reciprocal: $\\frac{1}{\\frac{3}{2}}=\\frac{2}{3}$.",
                   "Next level: $1+\\frac{2}{3}=\\frac{5}{3}$.",
                   "Last step: $\\frac{1}{\\frac{5}{3}}=\\frac{3}{5}$. The answer is choice 4.",
                   "Choice 1 ($\\frac{2}{3}$) stops one level too early. Choice 2 ($\\frac{5}{3}$) forgets the last flip."]),
    14: dict(stem='$\\dfrac{1+\\frac{1}{2}}{2-\\frac{1}{3}} = ?$',
             choices=['$\\frac{5}{2}$', '$\\frac{10}{9}$', '$\\frac{9}{10}$', '$\\frac{3}{2}$'], correct=3,
             expl=["Top: $1+\\frac{1}{2}=\\frac{3}{2}$. Bottom: $2-\\frac{1}{3}=\\frac{6}{3}-\\frac{1}{3}=\\frac{5}{3}$.",
                   "Divide: $\\frac{3}{2}\\div\\frac{5}{3}=\\frac{3}{2}\\cdot\\frac{3}{5}=\\frac{9}{10}$.",
                   "Choice 2 ($\\frac{10}{9}$) is upside down. Choice 1 ($\\frac{5}{2}$) multiplies top and bottom instead of dividing."]),
    # --- section 4: quick divisors
    15: dict(stem='$\\frac{3.6}{0.25} = ?$', choices=['$0.9$', '$14.4$', '$144$', '$1.44$'], correct=2,
             expl=["$0.25=\\frac{1}{4}$. Dividing by $\\frac{1}{4}$ is multiplying by 4.",
                   "$3.6\\cdot4=14.4$.",
                   "Check the slow way: multiply top and bottom by 100: $\\frac{360}{25}=14.4$.",
                   "Choice 1 (0.9) multiplies by 0.25 instead of dividing."]),
    16: dict(stem='$7\\div0.2 = ?$', choices=['$1.4$', '$14$', '$3.5$', '$35$'], correct=4,
             expl=["$0.2=\\frac{1}{5}$. Dividing by $\\frac{1}{5}$ is multiplying by 5: $7\\cdot5=35$.",
                   "Choice 1 (1.4) multiplies by 0.2 instead of dividing."]),
    17: dict(stem='A rope 4.5 meters long is cut into pieces of 0.25 meters each, with no waste. How many pieces are made?',
             choices=['$18$', '$9$', '$1\\frac{1}{8}$', '$180$'], correct=1,
             expl=["Number of pieces: $4.5\\div0.25$.",
                   "Dividing by $0.25=\\frac{1}{4}$ is multiplying by 4: $4.5\\cdot4=18$.",
                   "Choice 2 (9) divides by 0.5 instead of 0.25. Choice 3 multiplies instead of dividing."]),
    18: dict(stem='$0.125\\cdot64 = ?$', choices=['$80$', '$0.8$', '$8$', '$16$'], correct=3,
             expl=["$0.125=\\frac{1}{8}$.",
                   "$\\frac{1}{8}\\cdot64=64\\div8=8$."]),
    # --- shortcuts (strong students)
    19: dict(stem='$\\frac{5}{11}+\\frac{8}{15}+\\frac{4}{9}$ is closest to:',
             choices=['$\\frac{1}{2}$', '$1$', '$1\\frac{1}{2}$', '$2$'], correct=3,
             expl=["Each fraction is close to $\\frac{1}{2}$: half of 11 is 5.5, half of 15 is 7.5, half of 9 is 4.5.",
                   "The sum is close to $\\frac{1}{2}+\\frac{1}{2}+\\frac{1}{2}=1\\frac{1}{2}$.",
                   "The differences are small: $\\frac{5}{11}\\approx0.45$, $\\frac{8}{15}\\approx0.53$, $\\frac{4}{9}\\approx0.44$, and the sum is about 1.43.",
                   "The answer is choice 3."]),
    20: dict(stem='$\\frac{7}{8}+\\frac{5}{9} = ?$',
             choices=['$\\frac{12}{17}$', '$\\frac{1}{6}$', '$1\\frac{5}{72}$', '$1\\frac{31}{72}$'], correct=4,
             expl=["Estimate: $\\frac{7}{8}$ is almost 1 and $\\frac{5}{9}$ is a little more than $\\frac{1}{2}$. The sum is about $1\\frac{1}{2}$.",
                   "Choices 1 and 2 are less than 1, and $1\\frac{5}{72}$ is barely more than 1. Only choice 4 is close to $1\\frac{1}{2}$.",
                   "Exact, with the cross shortcut: $\\frac{7\\cdot9+5\\cdot8}{8\\cdot9}=\\frac{63+40}{72}=\\frac{103}{72}=1\\frac{31}{72}$."]),
    21: dict(stem='$\\frac{1}{6}-\\frac{1}{7} = ?$',
             choices=['$\\frac{1}{42}$', '$\\frac{13}{42}$', '$-\\frac{1}{42}$', '$0$'], correct=1,
             expl=["Shortcut: $\\frac{1}{a}-\\frac{1}{b}=\\frac{b-a}{ab}$.",
                   "$\\frac{1}{6}-\\frac{1}{7}=\\frac{7-6}{6\\cdot7}=\\frac{1}{42}$.",
                   "Check: $\\frac{1}{6}$ is bigger than $\\frac{1}{7}$. The answer must be positive. Choice 2 ($\\frac{13}{42}$) is the sum."]),
    22: dict(stem='$5\\frac{3}{4}-2\\frac{1}{3} = ?$',
             choices=['$2\\frac{5}{12}$', '$3\\frac{5}{12}$', '$3\\frac{1}{12}$', '$8\\frac{1}{12}$'], correct=2,
             expl=["No borrowing is needed ($\\frac{3}{4}$ is bigger than $\\frac{1}{3}$). Work part by part.",
                   "Whole parts: $5-2=3$. Fraction parts: $\\frac{3}{4}-\\frac{1}{3}=\\frac{9}{12}-\\frac{4}{12}=\\frac{5}{12}$.",
                   "Together: $3\\frac{5}{12}$.",
                   "The safe way gives the same: $\\frac{23}{4}-\\frac{7}{3}=\\frac{69}{12}-\\frac{28}{12}=\\frac{41}{12}=3\\frac{5}{12}$. Choice 4 adds instead of subtracting."]),
    23: dict(stem='$a$ and $b$ are positive numbers.\nWhich of the following is always equal to $\\frac{1}{a}+\\frac{1}{b}$?',
             choices=['$\\frac{2}{a+b}$', '$\\frac{2}{ab}$', '$\\frac{1}{a+b}$', '$\\frac{a+b}{ab}$'], correct=4,
             expl=["Plug in $a=1$ and $b=1$: $\\frac{1}{1}+\\frac{1}{1}=2$. Choice 1 gives $\\frac{2}{2}=1$ and choice 3 gives $\\frac{1}{2}$. Both are out.",
                   "Choices 2 and 4 both give 2. Try a second pair: $a=1$ and $b=2$: $1+\\frac{1}{2}=\\frac{3}{2}$.",
                   "Choice 2 gives $\\frac{2}{2}=1$. Out. Choice 4 gives $\\frac{1+2}{1\\cdot2}=\\frac{3}{2}$.",
                   "Check with the cross shortcut: $\\frac{1}{a}+\\frac{1}{b}=\\frac{1\\cdot b+1\\cdot a}{ab}=\\frac{a+b}{ab}$. The answer is choice 4."]),
    24: dict(stem='In a class, $\\frac{3}{5}$ of the students are girls. $\\frac{1}{4}$ of the girls and $\\frac{1}{2}$ of the boys wear glasses. What fraction of the class wears glasses?',
             choices=['$\\frac{7}{20}$', '$\\frac{3}{4}$', '$\\frac{3}{8}$', '$\\frac{1}{8}$'], correct=1,
             expl=["Girls with glasses: $\\frac{1}{4}$ of $\\frac{3}{5}$ is $\\frac{1}{4}\\cdot\\frac{3}{5}=\\frac{3}{20}$ of the class.",
                   "Boys: $1-\\frac{3}{5}=\\frac{2}{5}$ of the class. Boys with glasses: $\\frac{1}{2}\\cdot\\frac{2}{5}=\\frac{1}{5}=\\frac{4}{20}$ of the class.",
                   "Together: $\\frac{3}{20}+\\frac{4}{20}=\\frac{7}{20}$.",
                   "Choice 2 ($\\frac{3}{4}$) adds $\\frac{1}{4}+\\frac{1}{2}$. But those are parts of different groups, not of the whole class."]),
}


def new_questions(M):
    for n, d in NEW.items():
        M.new_q(QN % n, TOPIC, d['stem'], d['choices'], d['correct'], d['expl'])


def place_all(M):
    q = lambda n: QN % n
    # ---- section 1
    _guided(M, q(1), 'fraction-basics', 'mem-r26-t02-basics', 'Split the top',
            ["A sum on top and a minus sign at the bottom.", "You've tried it. Now let's solve it together."],
            'Top first, or split', [
                "Two good ways. Both come from this lesson.",
                "Way one: the fraction bar is brackets. Work out the top first.",
                A('(−6 + 15)/(−3) = 9/(−3) = −3 appears', P('$\\frac{-6+15}{-3}=\\frac{9}{-3}=-3$', size=40)),
                "Minus six plus fifteen is nine. Nine divided by minus three: minus three.",
                "Way two: split the top. Each part keeps the minus three underneath.",
                A('(−6)/(−3) + 15/(−3) = 2 + (−5) = −3 appears', P('$\\frac{-6}{-3}+\\frac{15}{-3}=2+(-5)=-3$', size=40)),
                "Minus six over minus three: plus two. Fifteen over minus three: minus five. Two minus five: minus three.",
                D('Circle choice 1'),
                "Same answer. Choice one.",
                "Here's the trap: dividing only the minus six and forgetting the fifteen. That gives two plus fifteen — seventeen. Choice three.",
                "When you split the top, EVERY part gets the denominator.",
            ])
    M.place_q(q(2), 'fraction-basics'); M.place_q(q(3), 'fraction-basics')
    # ---- section 2
    _guided(M, q(5), 'fraction-multiply', 'mem-r26-t02-multiply', 'Of the remaining',
            ["A word problem with two steps.", "Watch the word \"remaining\"."],
            'Of the remaining', [
                "Monday: three eighths OF 240. Of means times.",
                A("'Monday: 3/8 · 240 = 90 used, 150 left' appears", P('Monday: $\\frac{3}{8}\\cdot240=90$ used, $240-90=150$ left', size=36)),
                "Two hundred forty divided by eight is thirty. Times three: ninety liters used. One hundred fifty left.",
                "Tuesday: two fifths of the REMAINING water. That's two fifths of 150 — not of 240.",
                A("'Tuesday: 2/5 · 150 = 60 used, 90 left' appears", P('Tuesday: $\\frac{2}{5}\\cdot150=60$ used, $150-60=90$ left', size=36)),
                "One hundred fifty divided by five is thirty. Times two: sixty. One hundred fifty minus sixty: ninety liters left.",
                D('Circle choice 4'),
                "Ninety. Choice four.",
                "The trap: two fifths of the WHOLE tank is ninety-six. Two hundred forty minus ninety minus ninety-six is fifty-four. That's choice one.",
                A("'Faster: 3/5 · 5/8 · 240 = 3/8 · 240 = 90' appears", P('Faster: $\\frac{3}{5}\\cdot\\frac{5}{8}\\cdot240=\\frac{3}{8}\\cdot240=90$', size=36)),
                "Faster: five eighths stay after Monday. Three fifths of that stay after Tuesday. Three fifths of five eighths is three eighths — ninety liters.",
            ])
    for n in (6, 7, 9): M.place_q(q(n), 'fraction-multiply')
    # ---- section 3
    _guided(M, q(10), 'fraction-add', 'mem-fractions', 'Fraction bar = brackets',
            ["A stacked fraction with sums inside.", "Let's solve it together."],
            'Top, bottom, divide', [
                "The main bar is the long one. It works like brackets: top first, bottom first, then divide.",
                D('Trace over the long main bar'),
                A("'Top: 2/3 − 1/2 = 1/6' appears", P('Top: $\\frac{2}{3}-\\frac{1}{2}=\\frac{4}{6}-\\frac{3}{6}=\\frac{1}{6}$', size=36)),
                "Top: sixths. Four sixths minus three sixths: one sixth.",
                A("'Bottom: 1/4 + 1/3 = 7/12' appears", P('Bottom: $\\frac{1}{4}+\\frac{1}{3}=\\frac{3}{12}+\\frac{4}{12}=\\frac{7}{12}$', size=36)),
                "Bottom: twelfths. Three plus four: seven twelfths.",
                A("'1/6 ÷ 7/12 = 1/6 · 12/7 = 2/7' appears", P('$\\frac{1}{6}\\div\\frac{7}{12}=\\frac{1}{6}\\cdot\\frac{12}{7}=\\frac{2}{7}$', size=36)),
                "One sixth divided by seven twelfths. Flip the second: twelve sevenths. Six goes into twelve twice. Two sevenths.",
                D('Circle choice 2'),
                "Choice two.",
                "Choice three is seven halves — the same fraction upside down. It comes from flipping the wrong one.",
            ])
    M.place_q(q(14), 'fraction-add'); M.place_q(q(11), 'fraction-add')
    lesson_shortcuts(M)
    _guided(M, q(19), 'fraction-add', 'r26-t02-shortcuts', 'Estimate with ½',
            ["\"Closest to\" — that means you may estimate.", "No exact calculation needed."],
            'Benchmarks', [
                "Three fractions. Each one is close to a half.",
                A("'5/11 ≈ 1/2, 8/15 ≈ 1/2, 4/9 ≈ 1/2' appears", P('$\\frac{5}{11}\\approx\\frac{1}{2} \\qquad \\frac{8}{15}\\approx\\frac{1}{2} \\qquad \\frac{4}{9}\\approx\\frac{1}{2}$', size=36)),
                "Half of eleven is five and a half — five is just below. Half of fifteen is seven and a half — eight is just above.",
                "Half of nine is four and a half — four is just below.",
                A("'1/2 + 1/2 + 1/2 = 1 1/2' appears", P('$\\frac{1}{2}+\\frac{1}{2}+\\frac{1}{2}=1\\frac{1}{2}$', size=36)),
                "Three halves: one and a half. The small differences are tiny — they can't take us to one or to two.",
                D('Circle choice 3'),
                "Choice three.",
                "The exact common denominator for eleven, fifteen and nine is four hundred ninety-five. On the exam, estimating here saves minutes.",
            ])
    for n in (20, 21, 22): M.place_q(q(n), 'fraction-add')
    # ---- section 4
    _guided(M, q(15), 'decimals', 'mem-decimals', 'Divide by 0.25',
            ["Dividing by a decimal.", "There's a fast way."],
            '÷0.25 = ×4', [
                "Zero point two five is one quarter.",
                A("'0.25 = 1/4' appears", P('$0.25=\\frac{1}{4}$', size=40)),
                "Dividing by one quarter means multiplying by its reciprocal: four.",
                A("'3.6/0.25 = 3.6 · 4 = 14.4' appears", P('$\\frac{3.6}{0.25}=3.6\\cdot4=14.4$', size=40)),
                "Three point six times four: fourteen point four.",
                D('Circle choice 2'),
                "Choice two.",
                "Check with the slow way: times a hundred on top and bottom. Three hundred sixty over twenty-five — fourteen point four again.",
                "Choice one, zero point nine, multiplies by zero point two five instead of dividing.",
            ])
    M.place_q(q(18), 'decimals'); M.place_q(q(16), 'decimals')
    # ---- section 5: exam-level practice
    for n in (17, 4, 24, 8, 12, 23, 13): M.place_q(q(n), 'unit-t2-1')
    M.place_q(q(25), 'unit-t2-1')
    X = 'alg-extra-unit-t2-1-%d'
    M.practice_order('unit-t2-1', [
        'q-041', 'q-042', 'q-043', 'q-045', 'q-044', 'q-018', 'q-056', X % 5, 'q-057', 'q-060', 'q-051', 'q-052', X % 1, 'q-046', X % 3, 'q-050', X % 7,
        'q-058', 'q-059', 'q-047', 'q-048', X % 4, 'q-049', X % 2, q(25), X % 6, 'q-053', 'q-055', 'q-054',
        q(17), q(4), q(24), q(8), q(12), q(23), q(13)])


def apply(M):
    fix_videos(M)
    lesson_basics(M)
    lesson_multiply(M)
    lesson_add(M)
    lesson_decimals(M)
    cards(M)
    rewrite_existing(M)
    new_questions(M)
    place_all(M)
    summary(M)
    dedupe_examples(M)   # 2026-10-04: runs last


def _b(label, tex, size=44):
    """A board line that pops in (label = what the teacher sees in the script)."""
    return A("'%s' appears" % label, T(tex, size=size))


def summary(M):
    """Pass 2: a summary lesson right before the mixed fraction practice (end of the decimals section)."""
    last = [f['ref'] for f in M.D['flow'] if f['section'] == 'decimals'][-1]
    sb = ['What a fraction is', 'Same value', 'Multiplying', 'Dividing', 'Adding & subtracting', 'Several operations',
          'Shortcuts', 'Decimals', 'Before you practice']
    M.new_video('r26-t02-summary', TOPIC, 'Summary', sb, [
        dict(mode='title', title='Summary', script=[
            'A quick summary before the mixed fraction practice.',
            'Every rule from the fraction lessons — in about three minutes.']),
        dict(title='What a fraction is', active=0, script=[
            _b('Numerator: pieces we have · Denominator: pieces in one whole', 'Numerator: pieces we have · Denominator: pieces in one whole', size=40),
            _b('Bigger numerator → bigger · bigger denominator → smaller', 'Bigger numerator $\\to$ bigger · Bigger denominator $\\to$ smaller', size=40),
            'More cakes — everyone gets more. More people — everyone gets less.',
            _b('17/5 = 3 2/5 · 2 5/6 = 17/6', '$\\frac{17}{5}=3\\frac{2}{5} \\qquad 2\\frac{5}{6}=\\frac{2\\cdot 6+5}{6}=\\frac{17}{6}$'),
            'Improper to mixed: how many times it fits, and the remainder goes on top.',
            'Mixed to improper: whole times denominator, plus numerator. Same denominator.',
            'And a denominator can never be zero.']),
        dict(title='Same value', active=1, script=[
            _b('20/35 = 4/7 = 12/21', 'Same factor on top and bottom: $\\frac{20}{35}=\\frac{4}{7}=\\frac{12}{21}$'),
            'Expand or reduce: the same factor on top AND bottom. The value stays.',
            _b('(5·2)/(5·9) = 2/9 but (5+2)/(5·9): no cancelling', '$\\frac{5\\cdot 2}{5\\cdot 9}=\\frac{2}{9}$ ✓ $\\qquad \\frac{5+2}{5\\cdot 9}$: no cancelling ✗'),
            'Cancel factors only — never a term in a sum.',
            _b('(15+9)/3 = 15/3 + 9/3 = 8', 'Split the top — never the bottom: $\\frac{15+9}{3}=\\frac{15}{3}+\\frac{9}{3}=8$'),
            _b('−5/7 = (−5)/7 = 5/(−7)', '$-\\frac{5}{7}=\\frac{-5}{7}=\\frac{5}{-7} \\qquad \\frac{-5}{-7}=\\frac{5}{7}$'),
            'One minus sign can sit anywhere. Two minus signs cancel.']),
        dict(title='Multiplying', active=2, script=[
            _b('a/b · c/d = ac/bd', '$\\frac{a}{b}\\cdot\\frac{c}{d}=\\frac{ac}{bd}$ — cancel first'),
            'Top times top, bottom times bottom. Cancel first, and the numbers stay small.',
            _b('5/6 of 42 = 35', '"Of" means times: $\\frac{5}{6}$ of $42=\\frac{5}{6}\\cdot 42=35$'),
            _b('Spend 1/5, then 1/4 of the rest: 3/4 · 4/5 = 3/5 left', 'Spend $\\frac{1}{5}$, then $\\frac{1}{4}$ of the rest: $\\frac{3}{4}\\cdot\\frac{4}{5}=\\frac{3}{5}$ left', size=40),
            '"Of the rest" means of what is left — not of the whole.']),
        dict(title='Dividing', active=3, script=[
            _b('5/7 ÷ 3/4 = 5/7 · 4/3 = 20/21', 'Keep, change, flip: $\\frac{5}{7}\\div\\frac{3}{4}=\\frac{5}{7}\\cdot\\frac{4}{3}=\\frac{20}{21}$'),
            'Multiply by the reciprocal. Flip only the second one.',
            _b('Stacked fraction: the main bar means ÷', 'Stacked fraction: the main bar means $\\div$'),
            _b('Mixed numbers → improper first', 'Mixed numbers $\\to$ improper fractions first'),
            'Mixed numbers first become improper fractions. Never multiply the parts separately.',
            _b('2/5 ÷ 1/10 = 4', '$\\frac{2}{5}\\div\\frac{1}{10}=4$: dividing by a small fraction makes it bigger'),
            'You count how many tenths fit into two fifths: four.']),
        dict(title='Adding & subtracting', active=4, script=[
            _b('1/6 + 4/9 = 3/18 + 8/18 = 11/18', 'Common denominator (LCM): $\\frac{1}{6}+\\frac{4}{9}=\\frac{3}{18}+\\frac{8}{18}=\\frac{11}{18}$', size=40),
            'Adding and subtracting need a common denominator. Run through the multiples of the bigger one: nine no, eighteen yes.',
            'Then add the tops. The denominator stays.',
            _b('3 − 2/7 = 21/7 − 2/7 = 19/7', 'Whole numbers: $3-\\frac{2}{7}=\\frac{21}{7}-\\frac{2}{7}=\\frac{19}{7}$'),
            'A whole number can wear any denominator. Mixed numbers? Improper fractions first.']),
        dict(title='Several operations', active=5, script=[
            _b('5/6 − 1/3 · 3/4 = 5/6 − 1/4 = 7/12', '$\\frac{5}{6}-\\frac{1}{3}\\cdot\\frac{3}{4}=\\frac{5}{6}-\\frac{1}{4}=\\frac{7}{12}$'),
            'Same order as Topic 1: multiply and divide before add and subtract.',
            _b('A fraction bar is brackets', 'A fraction bar is brackets: $\\dfrac{1+\\frac{1}{3}}{3-\\frac{1}{2}}=\\dfrac{\\frac{4}{3}}{\\frac{5}{2}}=\\frac{8}{15}$'),
            'Work out the whole top and the whole bottom first. Then divide.',
            'Name the operation. Then use its rule.']),
        dict(title='Shortcuts', active=6, script=[
            _b('Estimate with 0, 1/2, 1', 'Estimate with $0,\\ \\frac{1}{2},\\ 1$ — kill choices'),
            'Six sevenths is almost one. Five ninths is a little more than a half. The sum is about one and a half.',
            _b('Test a rule with easy numbers', 'Test a rule: $\\frac{1}{3}+\\frac{1}{3}=\\frac{2}{3}$, but $\\frac{1+1}{3+3}=\\frac{1}{3}$ ✗'),
            'One example that fails kills a rule.',
            _b('a/b + c/d = (ad + bc)/bd', 'Cross shortcut: $\\frac{a}{b}+\\frac{c}{d}=\\frac{ad+bc}{bd}$'),
            'Cross shortcut: multiply across and add on top, multiply the bottoms. These are for speed — the safe method always works.']),
        dict(title='Decimals', active=7, script=[
            _b('0.64 = 64/100 = 16/25', 'Places = zeros: $0.64=\\frac{64}{100}=\\frac{16}{25}$'),
            'Decimal places tell you the zeros in the denominator.',
            _b('1.3 · 0.4 = 0.52', 'Multiply: count the places: $1.3\\cdot 0.4=0.52$'),
            _b('2.4 ÷ 0.08 = 240/8 = 30', 'Divide: expand until whole: $\\frac{2.4}{0.08}=\\frac{240}{8}=30$'),
            _b('÷0.5 = ×2 · ÷0.25 = ×4 · ÷0.2 = ×5', '$\\div 0.5=\\times 2 \\quad \\div 0.25=\\times 4 \\quad \\div 0.2=\\times 5 \\quad \\div 0.125=\\times 8$', size=40),
            'And to compare decimals, give them the same number of places: zero point five nine is bigger than zero point five one two.']),
        dict(title='Before you practice', active=8, script=[
            'Before you practice, ask yourself these questions.',
            _b('Which operation? Which rule?', 'Which operation is it? Which rule goes with it?'),
            'Adding needs a common denominator. Multiplying doesn\'t.',
            _b('Can I cancel? Only factors.', 'Can I cancel? Only factors of the whole top and the whole bottom.', size=40),
            _b('Of what? Of the whole or of the rest?', 'Of what? The whole, or the rest?'),
            _b('About how big is the answer?', 'About how big is the answer? Estimate with $0,\\ \\frac{1}{2},\\ 1$'),
            'The traps: adding tops and bottoms, flipping the wrong fraction, splitting the bottom, and "of the rest."',
            'Good luck.'])],
        'decimals', after=last)


# ---------------- 2026-10-04: a question must not be a lesson example the student just watched ----------------
def _dd_sub(M, vid, n, pairs):
    """Replace exact text on one slide (board items, spoken lines, draw cues, labels). Every pair must match."""
    b = M.slide(vid, n)
    for old, new in pairs:
        hit = 0
        for it in b['items']:
            if it.get('t') and old in it['t']: it['t'] = it['t'].replace(old, new); hit += 1
        for l in b['lines']:
            for k in ('say', 'draw', 'label'):
                if k in l and old in l[k]: l[k] = l[k].replace(old, new); hit += 1
        assert hit, '%s #%d: not found: %s' % (vid, n, old)
    M.touched_videos.add(vid)

def dedupe_examples(M):
    # alg-extra-unit-t2-1-2 was the lesson example 5/6 - 1/4 of "fraction-add" (RECORDED) -> new numbers.
    M.set_q('alg-extra-unit-t2-1-2', stem=r'Evaluate $\frac{3}{4}-\frac{1}{6}$.',
            choices=[r'$\frac{7}{12}$', r'$\frac{1}{6}$', r'$\frac{2}{3}$', r'$\frac{1}{5}$'], correct=1,
            expl=[r'The LCM of 4 and 6 is 12: $\frac{3}{4}=\frac{9}{12}$ and $\frac{1}{6}=\frac{2}{12}$.',
                  r'$\frac{9}{12}-\frac{2}{12}=\frac{7}{12}$.',
                  r'The trap: subtracting the tops and adding the bottoms, $\frac{3-1}{4+6}=\frac{1}{5}$.'])
    # q-069 was the lesson example 4 2/3 - 2 1/4 of "r26-t02-shortcuts" (RECORDED) -> new numbers.
    M.set_q('q-069', stem=r'$5\,\frac{3}{4} - 2\,\frac{1}{3} = ?$',
            choices=[r'$3\,\frac{5}{12}$', r'$3\,\frac{1}{2}$', r'$3\,\frac{1}{12}$', r'$3\,\frac{7}{12}$'], correct=1,
            expl=[r'Convert: $5\frac{3}{4}=\frac{23}{4}$ and $2\frac{1}{3}=\frac{7}{3}$.',
                  r'Common denominator 12: $\frac{69}{12}-\frac{28}{12}=\frac{41}{12}=3\frac{5}{12}$.',
                  r'Faster: whole parts $5-2=3$, fraction parts $\frac{9}{12}-\frac{4}{12}=\frac{5}{12}$. Together: $3\frac{5}{12}$.'])
