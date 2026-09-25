# Verbal Reasoning · Topic 42 · Formal logic and deductions ("claims").
# Hebrew hebverbal.txt 1170-1950 decides the concepts, their order, the methods and the verdicts.
# All examples are English bank questions, quoted word for word. Hebrew example sentences are NOT translated:
# the lesson teaches the same rules with abstract A / B.
from dsl import *

T42 = 42
def L(t, y, size=40): return T(t, size=size, x=410, y=y, w=1140)

SB = ['Where it sits', 'Condition → result', 'Six statements', 'What we know', "What we don't", 'One-way arrow', 'Recap']
SBQ = ['Question %d' % k for k in range(1, 10)]
G = 'Claims Questions'

def Q(i, qid, intro, slides): return guided(i, qid, G, SBQ, intro, slides, T42)

MODULES = [
# ------------------------------------------------------------------ lesson (Hebrew 1170-1245)
lesson('vr42-claims', 'Claims: Condition and Result', SB, [
 dict(mode='title', title='Claims: Condition and Result', script=[
  "Claims.",
  "The verbal section opens with analogies and closes with reading comprehension.",
  "In the middle there's a block of understanding-and-inference questions — and claims are the first type we'll learn there.",
 ]),
 dict(mode='concept', active=0, title='Where it sits', script=[
  "Honest truth: this exact type is rare. Very rare. One question every few exams.",
  A("Rare on its own — the base for other inference questions appears", L('Rare as its own type — but the base for other inference questions', 90)),
  "So why learn it? Because this logic sits underneath a lot of the other questions in the block.",
  "Before we run to questions — a short introduction. What is a claim, anyway?",
 ]),
 dict(mode='concept', active=1, title='Condition → result', script=[
  A("Given: All A are B appears", L('Given:   All A are B', 90, 50)),
  "Here's a given. It's a fact — but inside it hides a rule.",
  "It says: if you're an A, then you're a B.",
  A("If A → then B appears", L('If  A   →   then  B', 190, 50)),
  D("Label A 'condition' and B 'result'"),
  "There's a condition — A. And a result — B. If the condition holds, the result necessarily holds.",
  "That's the whole engine. Every claims question runs on it.",
 ]),
 dict(mode='concept', active=2, title='Six statements', script=[
  "Let's test six statements against 'All A are B'. Think with logic — don't try to memorise yet.",
  A("1. Everything that is not A is not B appears", L('1.   Everything that is not A is not B', 90, 36)),
  "Something that isn't an A — is it not a B? Why? There can be other B's. Not true.",
  D("Cross out 1"),
  A("2. All B are A appears", L('2.   All B are A', 150, 36)),
  "All B are A? Same problem — other things can be B too. Not true.",
  D("Cross out 2"),
  A("3. Everything that is not B is not A appears", L('3.   Everything that is not B is not A', 210, 36)),
  "Something that isn't a B — can it be an A? No! Every A is a B. True.",
  D("Tick 3"),
  A("4. Only A can be B appears", L('4.   Only A can be B', 270, 36)),
  "Only A can be B? No — there are other B's. Not true.",
  D("Cross out 4"),
  A("5. Only B can be A appears", L('5.   Only B can be A', 330, 36)),
  "Only B can be A? Yes — if it's not a B, it can't be an A. True.",
  D("Tick 5"),
  A("6. There is no A that is not B appears", L('6.   There is no A that is not B', 390, 36)),
  "No A that isn't a B? True — every A is a B. You can't be B and not-B at the same time.",
  D("Tick 6"),
 ]),
 dict(mode='concept', active=3, title='What we know', script=[
  "Keep only the true ones. What do they teach us?",
  A("Condition holds → result holds appears", L('Condition holds   →   result holds', 90)),
  "If you meet the condition, you necessarily meet the result.",
  A("Result fails → condition fails: not B → not A appears", L('Result fails   →   condition fails:     not B → not A', 170)),
  "And back: if the result didn't happen, the condition wasn't there. Because if it had been — the result would have had to happen.",
  A("Only B can be A · There is no A that is not B appears", L('"Only B can be A"     ·     "There is no A that is not B"', 250, 36)),
  "Only something that meets the result can be the condition. And there's no A without B.",
 ]),
 dict(mode='concept', active=4, title="What we don't", script=[
  "And the false ones? They all tried to say something about the wrong side.",
  A("Not A → ?   B → ?   We know nothing appears", L('not A  →  ?            B  →  ?            We know nothing', 90)),
  "Something that isn't A — we know nothing about it. Something that is B — nothing either.",
  "We only know what happens when the condition is met.",
  "Keep this in your head — in almost every question, the wrong answers break exactly this rule.",
 ]),
 dict(mode='concept', active=5, title='One-way arrow', script=[
  A("The arrow goes one way: A → B, never back appears", L('The arrow goes one way:   A → B  — it never comes back', 90)),
  "Picture the arrow. It runs from the condition to the result. It doesn't come back.",
  "Other conditions can lead to B as well. So B on its own proves nothing about A.",
 ]),
 dict(mode='concept', active=6, title='Recap', script=[
  "A short introduction — I hope it put some order into what a claim is.",
  A("A → B · not B → not A appears", L('A → B          ·          not B → not A', 90, 50)),
  A("not A → ? · B → ? appears", L('not A → ?          ·          B → ?', 190, 50)),
  "Now the first question. From there things get clearer.",
 ]),
], T42),

# ------------------------------------------------------------------ Q1 · easy (Hebrew 1246-1348): understanding, then arrows
Q(0, 'vb-inf_v1_0044', [
  "A sample question — an easy one.",
  "We'll solve it two ways: first by understanding, then with arrows.",
 ], [
 ('By understanding', [
  "Given: all the members of the choir are students at the college. Which necessarily follows?",
  D("Underline 'All the members of the choir' and 'students at the college'"),
  "Every choir member is a student at the college. Fine.",
  "Choice 1: everyone not in the choir is not a student. Someone outside the choir? I know nothing about them — could be a student. Out.",
  D("Cross out choice 1"),
  "Choice 2: all the students are in the choir. No — plenty of students never sang a note. Out.",
  D("Cross out choice 2"),
  "Choice 4: only choir members can be students. Same mistake. Out.",
  D("Cross out choice 4"),
 ]),
 ('With arrows', [
  "Now the technique. Here understanding is enough — but as questions get harder, arrows make the data much easier to see.",
  A("Choir → college student appears", P('choir   →   college student', size=38)),
  D("Write 'condition' under choir and 'result' under college student"),
  "Condition before the arrow, result after it.",
  "Not in the choir — that's not-condition: I know nothing. A student — that's the result: I know nothing.",
  A("not student → not choir ✓ appears", P('not student   →   not choir   ✓', size=38)),
  "Choice 3: not a student, so not in the choir. Result fails, condition fails. That's it.",
  D("Circle choice 3"),
  "Choice 3.",
 ]),
 ('Flip and negate', [
  "Look at what choice 3 did. It went backwards — and negated both sides.",
  A("A → B = not B → not A appears", P('A → B     =     not B → not A', size=40)),
  "If A is B, then not-B is not-A. Very, very important — it runs through almost every claims question.",
  "Back and forth. You may flip the arrow — but only if you negate both sides.",
 ]),
]),

# ------------------------------------------------------------------ Q2 · Hebrew "easy-plus" (1349-1425): check each one · "no" · "only" = reversed arrow
Q(1, 'vb-inf_v2_0403', [
  "The next sample question.",
  "Here we meet the two words that show up again and again in claims: 'no' and 'only'.",
 ], [
 ('Write the base claim', [
  "Three of the claims mean the same thing. Which is the remaining claim?",
  "How do we attack it? Check each claim on its own, against the others. Turn every claim into an arrow.",
  A("(2) untrained army → not a great power appears", P('(2)   untrained army   →   not a great power', size=34)),
  "Claim 2 is simple: every country with an untrained army is not a great power.",
 ]),
 ('"No" becomes "all"', [
  "Claim 3: there is no country that has an untrained army and is a great power.",
  A("No A that is B → A → not B appears", P('"No A is B"   =   all A are not B:     A → not B', size=34)),
  "Tip: when you see 'there is no A that is B' — 'no' turns into 'all', and you negate the other side.",
  A("(3) untrained army → not a great power appears", P('(3)   untrained army   →   not a great power', size=34)),
  "So claim 3 says exactly what claim 2 says.",
  D("Tick claims 2 and 3"),
 ]),
 ('"Only" = reversed arrow', [
  "Claim 4 starts with 'only'. Many claims start with 'only' — and they confuse people.",
  A("Only A is B → B → A (reverse the arrow) appears", P('"Only A is B"   →   B → A      (reverse the arrow)', size=34)),
  "'Only A can be B' doesn't say every A is a B. It says: if you're a B, you must be an A. The arrow runs backwards.",
  "Do it technically and fast: see 'only' at the start — reverse the arrow. Don't stop to think it through each time.",
  A("(4) untrained army → not a great power appears", P('(4)   untrained army   →   not a great power', size=34)),
  "Only a country that isn't a great power can have an untrained army: untrained army leads to not a great power. Same again.",
  D("Tick claim 4"),
 ]),
 ('The odd one out', [
  "Claim 1: if a country is not a great power, it has an untrained army.",
  A("(1) not a great power → untrained army ✗ appears", P('(1)   not a great power   →   untrained army      ✗', size=34)),
  "That's the arrow from the result back to the condition. We know nothing about the result — so it's a different claim.",
  D("Circle choice 1"),
  "Choice 1.",
 ]),
]),

# ------------------------------------------------------------------ Q3 · medium-plus (1426-1515): contrapositive = same claim · two-way claim
Q(2, 'vb-inf_v2_0406', [
  "A sample question — medium-plus difficulty.",
  "This one is all about which claims are really the same claim.",
 ], [
 ('Test pair 2', [
  "A pair is 'complete' if each claim can be inferred from the other. Which pair is complete?",
  "What do we do? We check. Arrows for every pair.",
  A("A: rain → happy · B: not happy → not rain appears", P('A:   rain → happy          B:   not happy → not rain', size=34)),
  "Pair 2. Claim B uses 'not happy' and 'not rain' — the claim in A uses 'rain' and 'happy'. Problem? No — we can flip and negate.",
  A("rain → happy = not happy → not rain appears", P('rain → happy     =     not happy → not rain', size=36)),
  "Flip A and negate: not happy leads to not raining. That's B exactly. An equals sign between them — each one gives the other.",
  D("Draw '=' between A and B of choice 2"),
 ]),
 ('Why pair 3 fails', [
  "In the lesson we check the rest. Pair 3.",
  A("not red → tasty · tasty → not red appears", P('A:   not red → tasty          B:   tasty → not red', size=34)),
  "A says not red leads to tasty. B turns the arrow around without negating — result to condition. That's not the same claim.",
  "Pair 4: 'no professors who are not absent-minded' means all professors are absent-minded. B says there ARE absent-minded professors — something else.",
  D("Cross out choices 3 and 4"),
  "Pair 1: something is not mine, versus nothing is mine — different claims. Out.",
  D("Cross out choice 1"),
  D("Circle choice 2"),
  "Choice 2.",
 ]),
 ('Two-way claim', [
  "Now something that grows out of this. Sometimes the arrow really does run both ways.",
  A("A → B and B → A = A ↔ B appears", P('A → B   and   B → A      =      A ↔ B', size=38)),
  "That's a two-way claim. Both groups are the same group of people.",
  A("A ↔ B → not A ↔ not B (no flipping needed) appears", P('A ↔ B     →     not A ↔ not B      (no flipping needed)', size=34)),
  "In a normal claim you may negate only if you flip. Here the arrow already runs both ways — so just negate both sides.",
  A("'If and only if' · 'if…, and only then' appears", P("On the exam: 'if A, and only if A, then B'  ·  'if A then B, and only then'", size=30)),
  "On the exam it usually comes as one long sentence: 'if and only if', or 'and only then'. Both mean a two-way claim.",
 ]),
]),

# ------------------------------------------------------------------ Q4 · medium-plus (1516-1566): a rule does not prove existence
Q(3, 'vb-inf_v1_0143', [
  "A sample question — medium-plus.",
  "A slightly strange one — not quite what we're used to. Let's understand it.",
 ], [
 ('What the rule says', [
  "No employee of the bank owns shares in it. Some residents of the town are employees of the bank.",
  A("No employee owns shares: employee → no shares appears", P("'No'  →  employee   →   no shares", size=36)),
  "'No' — we know what to do: every employee does not own shares.",
  "But careful. How should we read that rule?",
  A("If there is an employee → he owns no shares appears", P('If there IS an employee   →   he owns no shares', size=36)),
  "The right way to read it: IF there is an employee, then he owns no shares.",
 ]),
 ('A rule is not existence', [
  A("A rule does not prove that anything exists appears", P('A rule does not prove that anything exists', size=38)),
  "A rule doesn't tell you that anyone actually exists. It's a hard nuance to grasp — not very common — but important.",
  "That's exactly why the second given matters: SOME residents ARE employees. Now we know they exist.",
  D("Underline 'Some residents of the town are employees'"),
  "And those residents — they're employees — so they own no shares.",
 ]),
 ('The answer', [
  "Choice 4: some residents of the town do not own shares. Exactly those.",
  D("Circle choice 4"),
  "Choice 4.",
  "Choice 2 — no resident owns shares? We only know about the residents who are employees. The others — we know nothing.",
  D("Cross out choice 2"),
 ]),
]),

# ------------------------------------------------------------------ Q5 · medium (1567-1614): refute a claim = condition holds, result fails
Q(4, 'vb-inf_v2_0411', [
  "A sample question — medium difficulty.",
  "Here we learn how to contradict — to refute — a claim.",
 ], [
 ('How to refute', [
  "In every year with heavy winter rain, the crop shrinks, and its prices rise. Which case certainly contradicts this?",
  A("heavy rain → crop shrinks → prices rise appears", P('heavy rain   →   crop shrinks   →   prices rise', size=36)),
  "How do we show a claim is wrong? A case where the condition holds — but the result doesn't.",
  A("Refute: condition ✓ + result ✗ appears", P('Refute:   condition ✓   +   result ✗', size=40)),
  "The rule says the result must always follow. Show one case where it doesn't — and the rule is broken.",
 ]),
 ('Scan for the condition', [
  "So the condition — heavy rain — must be in the case.",
  "Choice 3 and choice 4: no heavy rain. Not relevant. The claim says nothing about winters without heavy rain.",
  D("Cross out choices 3 and 4"),
  "Choice 1: the crop didn't shrink, but prices rose. Were there heavy rains? It doesn't say. It doesn't touch the claim.",
  D("Cross out choice 1"),
  "Choice 2: heavy rain — condition — and prices did not rise. Condition yes, result no.",
  D("Circle choice 2"),
  "Choice 2.",
 ]),
]),

# ------------------------------------------------------------------ Q6 · hard (1615-1702): refute two claims · "only if"/"every" mid-sentence · scan for the condition
Q(5, 'vb-inf_v2_0408', [
  "A sample question — high difficulty.",
  "Two statements, one case — and a psychometric tip that saves a lot of time.",
 ], [
 ('Arrange both statements', [
  "Statement A: all the tall workers are married. Statement B: all the unmarried workers are short.",
  A("A: tall → married appears", P('A:    tall   →   married', size=38)),
  A("B: unmarried → short appears", P('B:    unmarried   →   short', size=38)),
  "Watch B — flip and negate: not short means tall, not unmarried means married. Tall leads to married. The same as A!",
 ]),
 ('Words in the middle', [
  "A side note on how claims can be written.",
  A("'B only if A' → move 'only' to the front → B → A appears", P("'B only if A'   →   'Only if A, B'   →   B → A", size=34)),
  "Sometimes 'only' sits in the middle: B only if A. Swap the two halves — now 'only' is at the start, and you reverse the arrow.",
  A("'All'/'every' mid-sentence: draw from the condition to the result appears", P("'every' in the middle:   arrow from the condition to the result — not left to right", size=30)),
  "Same with 'every' in the middle. Don't draw the arrow left to right. Ask: what comes first? That's the condition.",
 ]),
 ('Scan for the condition', [
  "Now the case: a short, married worker. Does it contradict anything?",
  "To contradict a claim, its condition must appear. Always. So scan fast for the conditions: tall — or unmarried.",
  A("To refute, the condition must appear appears", P('To refute, the condition must be there', size=38)),
  "Short and married: not tall. Not unmarried. Neither condition. Neither statement says a word about him.",
  D("Underline 'short' and 'married' in the stem"),
  D("Circle choice 3"),
  "Choice 3.",
  "A tough question with an important nuance — and scanning for the condition saves a lot of time.",
 ]),
]),

# ------------------------------------------------------------------ Q7 · easy-plus (1703-1770): chaining through a common term
Q(6, 'vb-inf_v1_0229', [
  "A sample question — easy-plus.",
  "Here we learn chaining: joining claims together.",
 ], [
 ('Link the claims', [
  "Every book on the top shelf is a first edition. No first edition may be borrowed. Which necessarily follows?",
  A("top shelf → first edition appears", P('top shelf   →   first edition', size=38)),
  A("first edition → not borrowable appears", P("'No' →   first edition   →   may not be borrowed", size=38)),
  "Top shelf here, borrowing there — they're mixed up. We need to chain them.",
  "To chain, we need a term that appears in both claims. First edition.",
  D("Circle 'first edition' in both givens"),
 ]),
 ('Read the chain', [
  A("top shelf → first edition → not borrowable appears", P('top shelf   →   first edition   →   may not be borrowed', size=34)),
  "Top shelf gives first edition, first edition gives not borrowable.",
  "Choice 1: no book on the top shelf may be borrowed. That's the chain from start to end.",
  D("Circle choice 1"),
  "Choice 1.",
 ]),
 ('Backwards too', [
  "And just like a single claim, you can run the whole chain backwards with negation.",
  A("borrowable → not first edition → not top shelf appears", P('may be borrowed   →   not first edition   →   not top shelf', size=34)),
  "In the lesson we check the others. Choice 2 — every first edition on the top shelf? That's the result pointing back at the condition. We know nothing. Out.",
  "Choice 3 — every book that can't be borrowed is on the top shelf? Again from the result. Out.",
  D("Cross out choices 2 and 3"),
  "To chain you need a shared term. Here it was easy — soon we'll see harder ones.",
 ]),
]),

# ------------------------------------------------------------------ Q8 · medium (1771-1854): one big scheme · "not possible" = a counterexample
Q(7, 'vb-inf_v2_0416', [
  "A sample question — medium difficulty.",
  "Several givens with shared terms — we'll build one big scheme.",
 ], [
 ('Build one scheme', [
  "Neta saw all the zoo animals that come from Africa. All the animals Neta saw eat grass only.",
  "'All' sits in the middle of the first given. Ask what comes first: coming from Africa is the condition.",
  A("from Africa → Neta saw it → eats grass only appears", P('from Africa   →   Neta saw it   →   eats grass only', size=34)),
  "'Seen' appears in both — chain them into one scheme.",
  "You don't have to write it in one line. Any shape works, as long as every arrow runs from condition to result.",
 ]),
 ('What is not possible?', [
  "Which is NOT possible? Something that contradicts the scheme — a condition without its result.",
  A("Not possible = condition ✓ + result ✗ appears", P('Not possible   =   condition ✓   +   result ✗', size=38)),
  "Choices 2 and 3 come from Asia. From Asia is not a condition here — we know nothing about those animals. Possible.",
  D("Cross out choices 2 and 3"),
  "Choice 1: grass and Africa. That's the scheme doing its job. Possible.",
  D("Cross out choice 1"),
  "Choice 4: comes from Africa — condition — and eats insects. The result failed.",
  D("Circle choice 4"),
  "Choice 4.",
 ]),
]),

# ------------------------------------------------------------------ Q9 · hard (1855-1948): which added datum completes the chain?
Q(8, 'vb-inf_v2_0405', [
  "A sample question — high difficulty.",
  "Now we're missing a link, and we need to find it.",
 ], [
 ('What do we want?', [
  "Which data would let us establish that every elephant that does NOT have green eyes is an Asian elephant?",
  A("Goal: not green eyes → Asian appears", P('Goal:    not green eyes   →   Asian', size=38)),
  "You could go answer by answer and try each one. Faster: understand right away what's missing.",
 ]),
 ('What exactly to look for', [
  "We're looking for this claim — or its flipped-and-negated twin. They're the same thing.",
  A("not green → Asian = not Asian → green appears", P('not green → Asian      =      not Asian → green', size=36)),
  "So scan for one of two starts: the condition 'not green eyes' — or the negated result, 'not Asian'.",
  D("Write 'not green…' and 'not Asian…' in the margin"),
 ]),
 ('Scan the choices', [
  "Choice 1: all Asian elephants have green eyes. Starts with Asian — that's our result, not what we need. Out.",
  D("Cross out choice 1"),
  "Choice 3: green-eyed leads to Asian. Starts with 'green' — not our condition. Out.",
  D("Cross out choice 3"),
  "Choice 4: no Asian elephant has green eyes — Asian again. Out.",
  D("Cross out choice 4"),
  "Choice 2: all elephants that are not Asian have green eyes. Not Asian leads to green — the twin of our goal.",
  D("Circle choice 2"),
  "Choice 2.",
  "Done with this one — and with the claims lesson. Now practise.",
 ]),
]),
]

MEMORY = [
 dict(id='mem-claims', after='solve-vb-inf_v2_0405', title='Claims — the rules to know',
  intro='Turn every claim into an arrow from the condition to the result.',
  tables=[dict(title='Reading a claim', head=['The claim says', 'Arrow', 'What follows'], rows=[
   ['All A are B · If A then B', 'A → B', 'not B → not A'],
   ['There is no A that is B', 'A → not B', 'B → not A'],
   ['Only A is B · B only if A', 'B → A (reversed)', 'not A → not B'],
   ['A if and only if B', 'A ↔ B', 'not A ↔ not B'],
   ['not A  ·  B', '—', 'we know nothing'],
  ]), dict(title='Working with claims', head=['Task', 'How'], rows=[
   ['Refute / "not possible"', 'condition holds and result fails'],
   ['Chain claims', 'join them through a shared term'],
   ['Find the missing datum', 'look for the condition, or the negated result'],
   ['A rule alone', 'does not prove anything exists'],
  ])],
  tips=["'No' becomes 'all' — negate the other side.", "'Only' at the start — reverse the arrow.",
        "'Only' or 'every' mid-sentence: find what comes first — that's the condition."]),
]
