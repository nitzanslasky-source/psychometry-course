# Verbal Reasoning · Topic 42 · Formal logic and deductions ("claims").
# Hebrew hebverbal.txt 1170-1950 decides the concepts, their order, the methods and the verdicts.
# All examples are ORIGINAL English questions (content/verbal_originals_A.json), quoted word for word. Hebrew example sentences are not translated:
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
  "In the middle there's a block of understanding-and-inference questions - and claims are the first type we'll learn there.",
 ]),
 dict(mode='concept', active=0, title='Where it sits', script=[
  "Honest truth: this exact type is rare. Very rare. One question every few exams.",
  A("Rare on its own - the base for other inference questions appears", L('Rare as its own type - but the base for other inference questions', 90)),
  "So why learn it? Because this logic sits underneath a lot of the other questions in the block.",
  "Before we run to questions - a short introduction. What is a claim, anyway?",
 ]),
 dict(mode='concept', active=1, title='Condition → result', script=[
  A("Given: All A are B appears", L('Given:   All A are B', 90, 50)),
  "Here's a given. It's a fact - but inside it hides a rule.",
  "It says: if you're an A, then you're a B.",
  A("If A → then B appears", L('If  A   →   then  B', 190, 50)),
  D("Label A 'condition' and B 'result'"),
  "There's a condition - A. And a result - B. If the condition holds, the result necessarily holds.",
  "That's the whole engine. Every claims question runs on it.",
 ]),
 dict(mode='concept', active=2, title='Six statements', script=[
  "Let's test six statements against 'All A are B'. Think with logic - don't try to memorize yet.",
  A("1. Everything that is not A is not B appears", L('1.   Everything that is not A is not B', 90, 36)),
  "Something that isn't an A - is it not a B? Why? There can be other B's. Not true.",
  D("Cross out 1"),
  A("2. All B are A appears", L('2.   All B are A', 150, 36)),
  "All B are A? Same problem - other things can be B too. Not true.",
  D("Cross out 2"),
  A("3. Everything that is not B is not A appears", L('3.   Everything that is not B is not A', 210, 36)),
  "Something that isn't a B - can it be an A? No! Every A is a B. True.",
  D("Tick 3"),
  A("4. Only A can be B appears", L('4.   Only A can be B', 270, 36)),
  "Only A can be B? No - there are other B's. Not true.",
  D("Cross out 4"),
  A("5. Only B can be A appears", L('5.   Only B can be A', 330, 36)),
  "Only B can be A? Yes - if it's not a B, it can't be an A. True.",
  D("Tick 5"),
  A("6. There is no A that is not B appears", L('6.   There is no A that is not B', 390, 36)),
  "No A that isn't a B? True - every A is a B. You can't be B and not-B at the same time.",
  D("Tick 6"),
 ]),
 dict(mode='concept', active=3, title='What we know', script=[
  "Keep only the true ones. What do they teach us?",
  A("Condition holds → result holds appears", L('Condition holds   →   result holds', 90)),
  "If you meet the condition, you necessarily meet the result.",
  A("Result fails → condition fails: not B → not A appears", L('Result fails   →   condition fails:     not B → not A', 170)),
  "And back: if the result didn't happen, the condition wasn't there. Because if it had been - the result would have had to happen.",
  A("Only B can be A · There is no A that is not B appears", L('"Only B can be A"     ·     "There is no A that is not B"', 250, 36)),
  "Only something that meets the result can be the condition. And there's no A without B.",
 ]),
 dict(mode='concept', active=4, title="What we don't", script=[
  "And the false ones? They all tried to say something about the wrong side.",
  A("Not A → ?   B → ?   We know nothing appears", L('not A  →  ?            B  →  ?            We know nothing', 90)),
  "Something that isn't A - we know nothing about it. Something that is B - nothing either.",
  "We only know what happens when the condition is met.",
  "Keep this in your head - in almost every question, the wrong answers break exactly this rule.",
 ]),
 dict(mode='concept', active=5, title='One-way arrow', script=[
  A("The arrow goes one way: A → B, never back appears", L('The arrow goes one way:   A → B  - it never comes back', 90)),
  "Picture the arrow. It runs from the condition to the result. It doesn't come back.",
  "Other conditions can lead to B as well. So B on its own proves nothing about A.",
 ]),
 dict(mode='concept', active=6, title='Recap', script=[
  "A short introduction - I hope it put some order into what a claim is.",
  A("A → B · not B → not A appears", L('A → B          ·          not B → not A', 90, 50)),
  A("not A → ? · B → ? appears", L('not A → ?          ·          B → ?', 190, 50)),
  "Now the first question. From there things get clearer.",
 ]),
], T42),

# ------------------------------------------------------------------ Q1 · easy (Hebrew 1246-1348): understanding, then arrows
Q(0, 'vo-42-001', [
  "A sample question - an easy one.",
  "We'll solve it two ways: first by understanding, then with arrows.",
 ], [
 ('By understanding', [
  "A 'no' to which question lets us be certain that every employee who does not drive to work lives within the city limits?",
  D("Underline 'every employee who does not drive to work' and 'lives within the city limits'"),
  "That's the claim we want: every employee who doesn't drive to work lives in the city.",
  "Choice 1: employees who drive to work. Someone who drives? The claim says nothing about them. A 'no' here proves nothing. Out.",
  D("Cross out choice 1"),
  "Choice 4: doesn't live in the city - but drives to work. Drivers again. Out.",
  D("Cross out choice 4"),
  "Choice 3: lives in the city and doesn't drive. Those employees just fit the claim - whether they exist or not, it proves nothing. Out.",
  D("Cross out choice 3"),
 ]),
 ('With arrows', [
  "Now the technique. Here understanding is enough - but as questions get harder, arrows make the data much easier to see.",
  A("not drive → city appears", P('does not drive   →   lives in the city', size=38)),
  D("Write 'condition' under 'does not drive' and 'result' under 'lives in the city'"),
  "Condition before the arrow, result after it.",
  "Drives to work - that's not-condition: I know nothing. Lives in the city - that's the result: I know nothing.",
  A("condition ✓ + result ✗ = the only employee who breaks it appears", P('does not drive   +   not in the city   =   the only one who breaks it', size=34)),
  "The only employee who can break the claim: condition yes, result no. Choice 2 asks exactly about them. A 'no' - and the claim is certain.",
  D("Circle choice 2"),
  "Choice 2.",
 ]),
 ('Flip and negate', [
  "Now look at the claim from the other side.",
  A("A → B = not B → not A appears", P('A → B     =     not B → not A', size=40)),
  A("not city → drives appears", P('does not live in the city   →   drives to work', size=36)),
  "Flip and negate: not living in the city leads to driving to work. Same claim - and choice 2's employee breaks it from this side too.",
  "If A is B, then not-B is not-A. Very, very important - it runs through almost every claims question.",
  "Back and forth. You may flip the arrow - but only if you negate both sides.",
 ]),
]),

# ------------------------------------------------------------------ Q2 · Hebrew "easy-plus" (1349-1425): check each one · "no" · "only" = reversed arrow
Q(1, 'vo-42-002', [
  "The next sample question.",
  "Here we meet the two words that show up again and again in claims: 'no' and 'only'.",
 ], [
 ('Write the base claim', [
  "Three of the claims have the same meaning. Which is the remaining claim?",
  "How do we attack it? Check each claim on its own, against the others. Turn every claim into an arrow.",
  A("(1) failed the test → not permitted appears", P('(1)   failed the safety test   →   not permitted to carry passengers', size=34)),
  "Claim 1 is simple: every boat that has failed the safety test is not permitted to carry passengers.",
 ]),
 ('"No" becomes "all"', [
  "Claim 2: there is no boat that has failed the safety test and is permitted to carry passengers.",
  A("No A that is B → A → not B appears", P('"No A is B"   =   all A are not B:     A → not B', size=34)),
  "Tip: when you see 'there is no A that is B' - 'no' turns into 'all', and you negate the other side.",
  A("(2) failed the test → not permitted appears", P('(2)   failed the safety test   →   not permitted', size=34)),
  "So claim 2 says exactly what claim 1 says.",
  D("Tick claims 1 and 2"),
 ]),
 ('"Only" = reversed arrow', [
  "Claim 4 starts with 'only'. Many claims start with 'only' - and they confuse people.",
  A("Only A is B → B → A (reverse the arrow) appears", P('"Only A is B"   →   B → A      (reverse the arrow)', size=34)),
  "'Only A can be B' doesn't say every A is a B. It says: if you're a B, you must be an A. The arrow runs backwards.",
  "Do it technically and fast: see 'only' at the start - reverse the arrow. Don't stop to think it through each time.",
  A("(4) failed the test → not permitted appears", P('(4)   failed the safety test   →   not permitted', size=34)),
  "Only a boat that is not permitted to carry passengers can have failed the test: failed leads to not permitted. Same again.",
  D("Tick claim 4"),
 ]),
 ('The odd one out', [
  "Claim 3: if a boat is not permitted to carry passengers, it has failed the safety test.",
  A("(3) not permitted → failed the test ✗ appears", P('(3)   not permitted   →   failed the safety test      ✗', size=34)),
  "That's the arrow from the result back to the condition. We know nothing about the result - so it's a different claim.",
  D("Circle choice 3"),
  "Choice 3.",
 ]),
]),

# ------------------------------------------------------------------ Q3 · medium-plus (1426-1515): contrapositive = same claim · two-way claim
Q(2, 'vo-42-003', [
  "A sample question - medium-plus difficulty.",
  "This one is all about which claims are really the same claim.",
 ], [
 ('Test pair 1', [
  "A pair is 'balanced' if each claim can be inferred from the other. Which pair is balanced?",
  "What do we do? We check. Arrows for every pair.",
  A("A: open → Dana at work · B: not at work → not open appears", P('A:   store open → Dana at work          B:   Dana not at work → store not open', size=32)),
  "Pair 1. Claim B uses 'not at work' and 'not open' - claim A uses 'open' and 'at work'. Problem? No - we can flip and negate.",
  A("open → at work = not at work → not open appears", P('open → at work     =     not at work → not open', size=36)),
  "Flip A and negate: Dana not at work leads to the store not open. That's B exactly. An equals sign between them - each one gives the other.",
  D("Draw '=' between A and B of choice 1"),
 ]),
 ('Why the others fail', [
  "In the lesson we check the rest. Pair 4.",
  A("not watered → wilts · wilts → not watered appears", P('A:   not watered → wilts          B:   wilts → not watered', size=34)),
  "A says not watered leads to wilting. B turns the arrow around without negating - result to condition. That's not the same claim.",
  "Pair 3: 'no painter in the group is without a studio' means every painter has a studio. B says there are painters with a studio - something else.",
  D("Cross out choices 3 and 4"),
  "Pair 2: someone did not attend, versus no one attended - different claims. Out.",
  D("Cross out choice 2"),
  D("Circle choice 1"),
  "Choice 1.",
 ]),
 ('Two-way claim', [
  "Now something that grows out of this. Sometimes the arrow really does run both ways.",
  A("A → B and B → A = A ↔ B appears", P('A → B   and   B → A      =      A ↔ B', size=38)),
  "That's a two-way claim. Both groups are the same group.",
  A("A ↔ B → not A ↔ not B (no flipping needed) appears", P('A ↔ B     →     not A ↔ not B      (no flipping needed)', size=34)),
  "In a normal claim you may negate only if you flip. Here the arrow already runs both ways - so just negate both sides.",
  A("'If and only if' · 'if…, and only then' appears", P("On the exam: 'if A, and only if A, then B'  ·  'if A then B, and only then'", size=30)),
  "On the exam it usually comes as one long sentence: 'if and only if', or 'and only then'. Both mean a two-way claim.",
 ]),
]),

# ------------------------------------------------------------------ Q4 · medium-plus (1516-1566): a rule does not prove existence
Q(3, 'vo-42-004', [
  "A sample question - medium-plus.",
  "A slightly strange one - not quite what we're used to. Let's understand it.",
 ], [
 ('What the information says', [
  "Given: the members of the Amber Quartet are left-handed violinists who live in Lisbon. Which question can be answered on the basis of this information?",
  "Strange - we're not asked what follows. We're asked which question the information can answer.",
  A("quartet member → left-handed violinist in Lisbon appears", P('member of the quartet   →   left-handed violinist, lives in Lisbon', size=34)),
  "As an arrow: if you're a member of the Amber Quartet, then you're a left-handed violinist who lives in Lisbon.",
  "But careful. How should we read a rule like that?",
  A("If there is a member → ... appears", P('If there is a member   →   they are a left-handed violinist in Lisbon', size=34)),
  "The right way to read a rule: if there is one, then this is what it's like.",
 ]),
 ('A rule is not existence', [
  A("A rule does not prove that anything exists appears", P('A rule does not prove that anything exists', size=38)),
  "A rule on its own doesn't tell you that anything actually exists. It's a hard nuance to grasp - not very common - but important.",
  "Here the information gives us more than a rule. It talks about real people: the members of a quartet. A quartet has members. They exist.",
  D("Underline 'the members of the Amber Quartet' and 'live in Lisbon'"),
  "And because they exist, we have a real example in our hands.",
 ]),
 ('The answer', [
  "Choice 4: is it true that none of the left-handed musicians who live in Lisbon plays the violin?",
  A("'No' → left-handed Lisbon musician → does not play the violin appears", P("'none'  →  left-handed musician in Lisbon   →   does not play the violin", size=34)),
  "But the quartet's members exist - left-handed, living in Lisbon, and violinists, which are musicians. So the answer is: no, it isn't true. We can answer it.",
  D("Circle choice 4"),
  "Choice 4.",
  "Choice 3 - is every left-handed violinist in Lisbon a member of the quartet? That's the result pointing back at the condition. We know nothing.",
  D("Cross out choice 3"),
  "Choices 1 and 2 - other cities, other groups. The information says nothing about them.",
  D("Cross out choices 1 and 2"),
 ]),
]),

# ------------------------------------------------------------------ Q5 · medium (1567-1614): refute a claim = condition holds, result fails
Q(4, 'vo-42-005', [
  "A sample question - medium difficulty.",
  "Here we learn how to contradict - to refute - a claim.",
 ], [
 ('How to refute', [
  "In every month in which the bakery launches a new type of bread, its advertising expenses rise, and its profits fall. Which case certainly contradicts this?",
  A("new bread → expenses rise → profits fall appears", P('new bread   →   advertising expenses rise   →   profits fall', size=34)),
  "How do we show a claim is wrong? A case where the condition holds - but the result doesn't.",
  A("Refute: condition ✓ + result ✗ appears", P('Refute:   condition ✓   +   result ✗', size=40)),
  "The rule says the result must always follow. Show one case where it doesn't - and the rule is broken.",
 ]),
 ('Scan for the condition', [
  "So the condition - a new type of bread - must be in the case.",
  "Choice 2 and choice 3: no new bread. Not relevant. The claim says nothing about months without a launch.",
  D("Cross out choices 2 and 3"),
  "Choice 1: expenses didn't rise, but profits fell. Was a new bread launched? It doesn't say. It doesn't touch the claim.",
  D("Cross out choice 1"),
  "Choice 4: a new bread was launched - condition - and profits did not fall. Condition yes, result no.",
  D("Circle choice 4"),
  "Choice 4.",
 ]),
]),

# ------------------------------------------------------------------ Q6 · hard (1615-1702): refute two claims · "only if"/"every" mid-sentence · scan for the condition
Q(5, 'vo-42-006', [
  "A sample question - high difficulty.",
  "Two statements, one case - and a psychometric tip that saves a lot of time.",
 ], [
 ('Arrange both statements', [
  "Statement A: all top-floor apartments have balconies. Statement B: all apartments without balconies are on lower floors.",
  A("A: top floor → balcony appears", P('A:    top floor   →   balcony', size=38)),
  A("B: no balcony → lower floor appears", P('B:    no balcony   →   lower floor', size=38)),
  "Watch B - flip and negate: not on a lower floor means the top floor, not 'no balcony' means a balcony. Top floor leads to a balcony. The same as A!",
 ]),
 ('Words in the middle', [
  "A side note on how claims can be written.",
  A("'B only if A' → move 'only' to the front → B → A appears", P("'B only if A'   →   'Only if A, B'   →   B → A", size=34)),
  "Sometimes 'only' sits in the middle: B only if A. Swap the two halves - now 'only' is at the start, and you reverse the arrow.",
  A("'All'/'every' mid-sentence: draw from the condition to the result appears", P("'every' in the middle:   arrow from the condition to the result - not left to right", size=30)),
  "Same with 'every' in the middle. Don't draw the arrow left to right. Ask: what comes first? That's the condition.",
 ]),
 ('Scan for the condition', [
  "Now the case: a lower-floor apartment with a balcony. Does it contradict anything?",
  "To contradict a claim, its condition must appear. Always. So scan fast for the conditions: top floor - or no balcony.",
  A("To refute, the condition must appear appears", P('To refute, the condition must be there', size=38)),
  "Lower floor with a balcony: not the top floor. Not without a balcony. Neither condition. Neither statement says a word about it.",
  D("Underline 'lower-floor' and 'with a balcony' in the stem"),
  D("Circle choice 2"),
  "Choice 2.",
  "A tough question with an important nuance - and scanning for the condition saves a lot of time.",
 ]),
]),

# ------------------------------------------------------------------ Q7 · easy-plus (1703-1770): chaining through a common term
Q(6, 'vo-42-007', [
  "A sample question - easy-plus.",
  "Here we learn chaining: joining claims together.",
 ], [
 ('Link the claims', [
  "Twelve hikers on a trail. Every hiker who carried a map reached the lookout point. Every hiker who reached the lookout point returned before sunset.",
  A("map → reached the lookout appears", P('carried a map   →   reached the lookout point', size=38)),
  A("reached the lookout → back before sunset appears", P('reached the lookout point   →   returned before sunset', size=38)),
  "The map here, sunset there - they're split between two givens. We need to chain them.",
  "To chain, we need a term that appears in both claims. Reached the lookout point.",
  D("Circle 'reached the lookout point' in both givens"),
 ]),
 ('Read the chain', [
  A("map → lookout → before sunset appears", P('map   →   lookout point   →   before sunset', size=34)),
  "A map gives the lookout, the lookout gives back before sunset. Every hiker with a map returned before sunset.",
  "Which is not possible? Choice 2: a map and back before sunset - that's the chain from start to end. Possible.",
  D("Cross out choice 2"),
  "Choices 1 and 4: no map. That's not-condition - we know nothing. Possible.",
  D("Cross out choices 1 and 4"),
 ]),
 ('Backwards too', [
  "And just like a single claim, you can run the whole chain backwards with negation.",
  A("after sunset → no lookout → no map appears", P('after sunset   →   did not reach the lookout   →   no map', size=34)),
  "Returned after sunset - so didn't reach the lookout point, so carried no map.",
  "Choice 3: carried a map and returned after sunset. The backward chain says that can't happen.",
  D("Circle choice 3"),
  "Choice 3.",
  "To chain you need a shared term. Here it was easy - soon we'll see harder ones.",
 ]),
]),

# ------------------------------------------------------------------ Q8 · medium (1771-1854): one big scheme · "not possible" = a counterexample
Q(7, 'vo-42-008', [
  "A sample question - medium difficulty.",
  "Several givens with shared terms - we'll build one big scheme.",
 ], [
 ('Build one scheme', [
  "Of the books in the library, Omer leafed through all the books written in Spanish. All the books Omer leafed through are hardcovers.",
  "'All' sits in the middle of the first given. Ask what comes first: being written in Spanish is the condition.",
  A("in Spanish → Omer leafed through it → hardcover appears", P('in Spanish   →   Omer leafed through it   →   hardcover', size=34)),
  "'Leafed through' appears in both - chain them into one scheme.",
  "You don't have to write it in one line. Any shape works, as long as every arrow runs from condition to result.",
 ]),
 ('What is not possible?', [
  "Which is not possible? Something that contradicts the scheme - a condition without its result.",
  A("Not possible = condition ✓ + result ✗ appears", P('Not possible   =   condition ✓   +   result ✗', size=38)),
  "Choices 2 and 4 are in Italian. Italian is not a condition here - we know nothing about those books. Possible.",
  D("Cross out choices 2 and 4"),
  "Choice 3: Spanish and a hardcover. That's the scheme doing its job. Possible.",
  D("Cross out choice 3"),
  "Choice 1: in Spanish - condition - and a paperback. The result failed.",
  D("Circle choice 1"),
  "Choice 1.",
 ]),
]),

# ------------------------------------------------------------------ Q9 · hard (1855-1948): which added datum completes the chain?
Q(8, 'vo-42-009', [
  "A sample question - high difficulty.",
  "Now we're missing a link, and we need to find it.",
 ], [
 ('What do we want?', [
  "Which information would let us establish that every tile in the warehouse that is not glazed was made in Portugal?",
  A("Goal: not glazed → Portugal appears", P('Goal:    not glazed   →   made in Portugal', size=38)),
  "You could go answer by answer and try each one. Faster: understand right away what's missing.",
 ]),
 ('What exactly to look for', [
  "We're looking for this claim - or its flipped-and-negated twin. They're the same thing.",
  A("not glazed → Portugal = not Portugal → glazed appears", P('not glazed → Portugal      =      not Portugal → glazed', size=36)),
  "So scan for one of two starts: the condition 'not glazed' - or the negated result, 'not made in Portugal'.",
  D("Write 'not glazed…' and 'not Portugal…' in the margin"),
 ]),
 ('Scan the choices', [
  "Choice 1: all the tiles not made in Portugal are glazed. Not Portugal leads to glazed - the twin of our goal.",
  D("Circle choice 1"),
  "Choice 1.",
  "On the exam - stop here. For the lesson, a quick look at the rest.",
  "Choice 2: all the tiles made in Portugal are glazed. Starts with Portugal - that's our result, not what we need. Out.",
  D("Cross out choice 2"),
  "Choice 3: glazed leads to Portugal. Starts with 'glazed' - not our condition. Out.",
  D("Cross out choice 3"),
  "Choice 4: none of the Portuguese tiles are glazed - Portugal again. Out.",
  D("Cross out choice 4"),
  "Done with this one - and with the claims lesson. Now practice.",
 ]),
]),
]

MEMORY = [
 dict(id='mem-claims', after='solve-vo-42-009', title='Claims - the rules to know',
  intro='Turn every claim into an arrow from the condition to the result.',
  tables=[dict(title='Reading a claim', head=['The claim says', 'Arrow', 'What follows'], rows=[
   ['All A are B · If A then B', 'A → B', 'not B → not A'],
   ['There is no A that is B', 'A → not B', 'B → not A'],
   ['Only A is B · B only if A', 'B → A (reversed)', 'not A → not B'],
   ['A if and only if B', 'A ↔ B', 'not A ↔ not B'],
   ['not A  ·  B', '-', 'we know nothing'],
  ]), dict(title='Working with claims', head=['Task', 'How'], rows=[
   ['Refute / "not possible"', 'condition holds and result fails'],
   ['Chain claims', 'join them through a shared term'],
   ['Find the missing datum', 'look for the condition, or the negated result'],
   ['A rule alone', 'does not prove anything exists'],
  ])],
  tips=["'No' becomes 'all' - negate the other side.", "'Only' at the start - reverse the arrow.",
        "'Only' or 'every' mid-sentence: find what comes first - that's the condition."]),
]
