# Verbal Reasoning · Topic 43 · Understanding sentences.
# Hebrew (hebverbal.txt 1951-2273, "הבנת משפט") decides the concepts, order, methods and verdicts.
# Every question is an ORIGINAL English question (content/verbal_originals_A.json), quoted word for word.
from dsl import *

TOPIC = 43
SB = ['What they test', 'Why it matters', 'The question types']
SBQ = ['Question 1']

def C(t, size=40): return T(t, size=size)

MODULES = [
lesson('vr43-sentences', 'Understanding Sentences', SB, [
 dict(mode='title', title='Understanding Sentences', script=[
  "Understanding sentences.",
  "They give us one sentence - and check whether we really understand it.",
 ]),
 dict(mode='concept', active=0, title='What they test', script=[
  "Where does the difficulty come from?",
  A("Vocabulary - a word or phrase you don't know appears", C("Vocabulary - a word or phrase you don't know")),
  "Sometimes it's vocabulary - one word or expression you're not sure of.",
  A("Intention - what did the speaker actually mean? appears", C('Intention - what did the speaker actually mean?')),
  "Sometimes it's hard to see what the person who said it meant.",
  A("Structure - negations, double meanings, hidden assumptions appears", C('Structure - negations, double meanings, hidden assumptions')),
  "And sometimes it's the way the sentence is built.",
 ]),
 dict(mode='concept', active=1, title='Why it matters', script=[
  "This skill isn't one question type. It runs through the whole verbal section.",
  A("If you don't understand what you read - you can't draw conclusions from it appears", C("Don't understand it → can't draw conclusions from it")),
  "It's what inference questions stand on. If you don't understand what you read, you can't infer anything from it.",
  "And of course - reading comprehension.",
 ]),
 dict(mode='concept', active=2, title='The question types', script=[
  "We'll meet them one by one, each on a real question:",
  A("1 · Meaning and vocabulary appears", C('1 · What the speaker means - and the key expression')),
  A("2 · Fixing a sentence by replacing words appears", C('2 · Replacing words to change the meaning')),
  A("3 · Double negatives appears", C('3 · Double negatives')),
  A("4 · A sentence with two meanings appears", C('4 · A sentence with two meanings')),
  A("5 · Hidden assumptions appears", C('5 · Hidden assumptions - clear and unclear')),
  "Let's start with a sample question and move on from there.",
 ]),
], TOPIC),

# ---- Hebrew example 1 (medium): what the speaker thinks; structure first, then the key expression
guided(0, 'vo-43-001', 'Sentence Questions', SBQ,
 ["A sample question - medium difficulty.", "What did the speaker mean?"],
 [('Understand the speaker', [
   "An economist: whether the recovery will be sustained remains highly uncertain - so far, it's no more than an early indication.",
   "Let's try to understand what she thinks.",
   D("Underline 'remains highly uncertain'"),
   A("She is not sure the recovery will last appears", P('She is not sure the recovery will last')),
   "First, what I understand for sure: she doubts. She is not certain.",
  ]),
  ('Eliminate what you can', [
   D("Cross out choice 1"),
   "Choice one: 'it is certain that the recovery will continue.' The opposite. Out.",
   D("Cross out choice 3"),
   "Choice three: 'it is already clear that the recovery will be sustained.' Same problem. Out.",
   "Two gone - and I didn't need any hard vocabulary for that.",
   "Now two against each other. Here the exact expression decides.",
  ]),
  ('The key expression', [
   D("Circle 'be sustained'"),
   A("be sustained = last, continue over time appears", P("be sustained = last, continue over time")),
   "'Be sustained' - last, keep going over time. That's what she doubts: the future.",
   "Choice two doubts something else - whether the recovery reflects the state of the market now. A different question.",
   D("Cross out choice 2"),
   D("Circle choice 4"),
   "Choice 4. Given the other developments, it's doubtful whether the recovery will last for long.",
   "If you know the expression - this is quick. If not, you still eliminated half the choices from structure alone.",
  ])]
, TOPIC),

# ---- Hebrew example 2 (medium): replacing words to change the meaning
guided(1, 'vo-43-002', 'Sentence Questions', SBQ,
 ["Another sample question - medium difficulty.", "A different type: replacing words in a sentence."],
 [('Why is it not logical?', [
   "Maya: at the new restaurant, most diners come back - so I assume the food there is ____.",
   "We're told her words are not logical. One swap, or another swap, would make them logical.",
   "Some of these questions ask you to replace words, make a sentence logical or illogical, reorder it.",
   A("Most come back → the food sounds good appears", P('Most come back → the food sounds good')),
   "Most diners come back. What's the natural conclusion? The food is good.",
  ]),
  ('Fill in and check', [
   A("\"so\" + disappointing = not logical appears", P('"so" + a bad verdict = not logical')),
   "For her sentence to be illogical, the first blank must be a bad verdict. Most come back, so - disappointing? Doesn't follow.",
   D("Cross out choice 2"),
   "Choice two starts with 'excellent'. 'Most come back, so it's excellent' is perfectly logical. Out.",
   A("Fix 1: \"even so\" · Fix 2: \"excellent\" instead of \"disappointing\" appears", P('Fix 1: "even so" · Fix 2: "excellent" instead of "disappointing"')),
   "Two fixes: 'even so' instead of 'so' - most come back, even so I think the food is disappointing. Logical: a concession.",
   "Or keep 'so' and replace 'disappointing' with 'excellent'. Either one works on its own.",
  ]),
  ('The traps', [
   D("Cross out choice 1"),
   "Choice one: 'therefore' instead of 'so' - the same connector in other words. And 'few diners fail to come back' - the same fact in other words. Nothing changes. Out.",
   D("Underline 'and also' in choice 4"),
   "Choice four: 'and yet' - fine. But 'and also' - both swaps at once. Most come back, and yet the food is quite good? Illogical again. Out.",
   D("Circle choice 3"),
   "Choice 3.",
  ])]
, TOPIC),

# ---- Hebrew example 4 (hard): a sentence with two meanings
guided(2, 'vo-43-003', 'Sentence Questions', SBQ,
 ["A sample question - a hard one.", "A sentence that can be understood in two ways."],
 [('Find both readings', [
   "The scholarship will be awarded only to nursing students who work at the city hospital and residents of the northern district.",
   "A double meaning. By the way - a sentence can have more than two meanings. Here it has two.",
   A("Reading 1: nursing student + hospital + north - all three appears", P('Reading 1: nursing student + hospital + north - all three')),
   "The obvious reading: you need all three. A nursing student, working at the hospital, living in the north.",
   D("Circle 'and'"),
   A("Reading 2: (nursing student + hospital) or north appears", P('Reading 2: (nursing student + hospital) or north')),
   "The second reading: here 'and' works like 'or'. Nursing students who work at the hospital - or residents of the north.",
   "A resident of the north needs nothing else.",
  ]),
  ('"Only" is a condition', [
   "What's impossible under both readings?",
   "Careful: 'only' tells us who can get the scholarship. It doesn't say everyone who qualifies must get it.",
   A("Qualifies → may get it, not must appears", P('Qualifies → may get it, not must')),
   "It reminds us of claims and logic - a condition, not a promise.",
   D("Cross out choice 2"),
   "Ron - a resident of the north - got it. Possible under reading two. Out.",
   D("Cross out choice 4"),
   "Gil - a resident of the north - didn't get it. Always possible: qualifying doesn't force an award. Out.",
  ]),
  ('Check each reading', [
   D("Cross out choice 3"),
   "Shira - a nursing student who lives in the north, but doesn't work at the hospital - got it. Reading two: she lives in the north. Possible. Out.",
   D("Circle choice 1"),
   "Yael - works at the hospital, but isn't a nursing student and doesn't live in the north. Reading one? No. Reading two? No.",
   "She fails both readings - so 'Yael was awarded the scholarship' is impossible.",
   "Choice 1.",
  ])]
, TOPIC),

# ---- Hebrew example 5 (easy): hidden assumption - the clear kind
guided(3, 'vo-43-004', 'Sentence Questions', SBQ,
 ["A sample question - an easy one.", "A hidden assumption."],
 [('What are they relying on?', [
   "People who waited in a warm room donated more. The researcher estimates: warmth improves mood, so they were in a better mood when asked.",
   "A hidden assumption: the researcher relies on something never said.",
   A("Two kinds: the assumption is clear · or hard to see appears", P('Two kinds: the assumption is clear · or hard to see')),
   "Two kinds of these. Sometimes the assumption is fairly clear. Sometimes it's hard to see the connection at all.",
   "This one is the clear kind.",
  ]),
  ('Fill the gap', [
   A("Better mood → donated more ? appears", P('Better mood → donated more ?')),
   "The finding: donated more. The explanation: a better mood. What links the two?",
   "The researcher must assume that a person in a good mood gives more.",
   D("Circle choice 2"),
   "Choice 2. A person in a good mood contributes more generously than a person whose mood is less good.",
   D("Cross out choice 4"),
   "Choice four adds a condition - only after a warm room. The estimate never needed that.",
  ])]
, TOPIC),

# ---- Hebrew example 6 (hard): hidden assumption - the unclear kind (two speakers who know more than we do)
guided(4, 'vo-43-005', 'Sentence Questions', SBQ,
 ["A sample question - a hard one.", "A hidden assumption of the second kind - not clear at all."],
 [("What do they know that we don't?", [
   "Noa: I doubt I could arrange this violin sonata for the piano - much less for the guitar.",
   "Eyal: so you play the piano better than the guitar.",
   "It sounds like two people talking past each other. They're not. They just rely on things we weren't told.",
   A("Our job: find the unstated link appears", P('Our job: find the unstated link')),
  ]),
  ('Translate the dialogue', [
   D("Write: violin → piano hard · violin → guitar even harder"),
   A("violin→piano easier than violin→guitar appears", P('violin→piano easier than violin→guitar')),
   "'Much less for the guitar' - arranging for the guitar is even harder than for the piano.",
   A("⇒ piano better than guitar appears", P('⇒ piano better than guitar')),
   "Eyal concludes: the piano is the instrument she plays better.",
   "So his rule: arranging a piece for an instrument more easily means you play that instrument better.",
  ]),
  ('Match the letters', [
   A("C = violin · A = piano · B = guitar appears", P('C = violin · A = piano · B = guitar')),
   "The violin is the source, C. The piano is A, the instrument he says she plays better. The guitar is B.",
   D("Circle choice 4"),
   "From C for A more easily than from C for B. Choice 4.",
   D("Cross out choice 2"),
   "Choice two arranges from A and from B - the wrong direction. Always check what goes where.",
  ])]
, TOPIC),
]

# Hebrew example 3 (easy-plus, double negatives) has no guided question: taught on a concept slide.
MODULES[0]['slides'].insert(3, dict(mode='concept', active=2, title='Double negatives', script=[
  "One structure to master before we start: double negatives.",
  A("not + not = yes appears", C('not … not = yes')),
  "Two negatives cancel out.",
  A("It is not unusual for the museum not to open on time. appears", C('It is not unusual for the museum not to open on time.', 36)),
  "How do we handle it? Slowly - replace one pair of negatives at a time with something positive.",
  A("not unusual → usual appears", C('not unusual → usual')),
  A("→ It is usual for the museum to open late. appears", C('→ It is usual for the museum to open late.', 36)),
  "Now it's clear. And some of you will see it halfway through - that's fine, answer as soon as it's clear.",
  "This matters a lot on the exam - and especially in sentence completion, where double negatives are everywhere.",
]))
SB.insert(2, 'Double negatives')
for sl in MODULES[0]['slides'][4:]:
    if sl.get('active', -1) >= 2: sl['active'] += 1

MEMORY = [
 dict(id='mem-sentences', after='solve-vo-43-005', title='Understanding sentences - the toolkit',
  intro='What makes a sentence hard, and what to do about it.',
  tables=[dict(head=['Difficulty', 'What to do'], rows=[
    ['A word or expression', 'Eliminate by structure first; the key expression decides the rest'],
    ['Replacing words', 'Find what makes it (il)logical; test each swap'],
    ['Double negatives', 'Turn one pair of negatives into a positive at a time'],
    ['Two meanings', 'Write both readings ("and" can act as "or"); check each choice against both'],
    ['Hidden assumption', 'Find the unstated link between what was said and the conclusion'],
  ])],
  tips=['"Only" = who can be accepted - not who must be.', 'Condition not met → result unknown.',
        'The skill runs through all of verbal: no understanding, no conclusions.']),
]
