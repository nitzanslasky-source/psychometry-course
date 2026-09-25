# Verbal Reasoning · Topic 43 · Understanding sentences.
# Hebrew (hebverbal.txt 1951-2273, "הבנת משפט") decides the concepts, order, methods and verdicts.
# Every question is an English bank item (vcands43.txt), wording untouched.
from dsl import *

TOPIC = 43
SB = ['What they test', 'Why it matters', 'The question types']
SBQ = ['Question 1']

def C(t, size=40): return T(t, size=size)

MODULES = [
lesson('vr43-sentences', 'Understanding Sentences', SB, [
 dict(mode='title', title='Understanding Sentences', script=[
  "Understanding sentences.",
  "They give us one sentence — and check whether we really understand it.",
 ]),
 dict(mode='concept', active=0, title='What they test', script=[
  "Where does the difficulty come from?",
  A("Vocabulary — a word or phrase you don't know appears", C("Vocabulary — a word or phrase you don't know")),
  "Sometimes it's vocabulary — one word or expression you're not sure of.",
  A("Intention — what did the speaker actually mean? appears", C('Intention — what did the speaker actually mean?')),
  "Sometimes it's hard to see what the person who said it meant.",
  A("Structure — negations, double meanings, hidden assumptions appears", C('Structure — negations, double meanings, hidden assumptions')),
  "And sometimes it's the way the sentence is built.",
 ]),
 dict(mode='concept', active=1, title='Why it matters', script=[
  "This skill isn't one question type. It runs through the whole verbal section.",
  A("If you don't understand what you read — you can't draw conclusions from it appears", C("Don't understand it → can't draw conclusions from it")),
  "It's what inference questions stand on. If you don't understand what you read, you can't infer anything from it.",
  "And of course — reading comprehension.",
 ]),
 dict(mode='concept', active=2, title='The question types', script=[
  "We'll meet them one by one, each on a real question:",
  A("1 · Meaning and vocabulary appears", C('1 · What the speaker means — and the key expression')),
  A("2 · Fixing a sentence by replacing words appears", C('2 · Replacing words to change the meaning')),
  A("3 · Double negatives appears", C('3 · Double negatives')),
  A("4 · A sentence with two meanings appears", C('4 · A sentence with two meanings')),
  A("5 · Hidden assumptions appears", C('5 · Hidden assumptions — clear and unclear')),
  "Let's start with a sample question and move on from there.",
 ]),
], TOPIC),

# ---- Hebrew example 1 (medium): what the speaker thinks; structure first, then the key expression
guided(0, 'vb-inf_v2_0359', 'Sentence Questions', SBQ,
 ["A sample question — medium difficulty.", "What did the speaker mean?"],
 [('Understand the speaker', [
   "A political commentator: these are only first signs — there is still much doubt whether the mood will take real hold.",
   "Let's try to understand what he thinks.",
   D("Underline 'still much doubt whether'"),
   A("He is NOT sure the mood will last appears", P('He is NOT sure the mood will last')),
   "First, what I understand for sure: he doubts. He is not certain.",
  ]),
  ('Eliminate what you can', [
   D("Cross out choice 2"),
   "Choice two: 'we cannot doubt that the mood will spread.' The opposite. Out.",
   D("Cross out choice 4"),
   "Choice four: 'there is no doubt that the mood will take hold.' Same problem. Out.",
   "Two gone — and I didn't need any hard vocabulary for that.",
   "Now three against one. Here the exact expression decides.",
  ]),
  ('The key expression', [
   D("Circle 'take real hold'"),
   A("take real hold = take root, last appears", P("take real hold = take root, last")),
   "'Take real hold' — take root, become lasting. That's what he doubts.",
   "Choice three doubts something else — whether the mood represents the country now. A different question.",
   D("Cross out choice 3"),
   D("Circle choice 1"),
   "Choice 1. Not clear to what extent the mood will take root, given the other things happening.",
   "If you know the expression — this is quick. If not, you still eliminated half the choices from structure alone.",
  ])]
, TOPIC),

# ---- Hebrew example 2 (medium): replacing words to change the meaning
guided(1, 'vb-inf_v2_0353', 'Sentence Questions', SBQ,
 ["Another sample question — medium difficulty.", "A different type: replacing words in a sentence."],
 [('Why is it not logical?', [
   "Yigal: most students pass the Algebraic Structures exam — and so I think the course is ____.",
   "We're told his words are NOT logical. Swap one word, or swap another pair, and they become logical.",
   "Some of these questions ask you to replace words, make a sentence logical or illogical, reorder it.",
   A("Most pass → the course sounds EASY appears", P('Most pass → the course sounds EASY')),
   "Most students pass. What's the natural conclusion? The course is easy.",
  ]),
  ('Fill in and check', [
   A("\"and so\" + hard = not logical appears", P('"and so" + hard = not logical')),
   "For his sentence to be illogical, the blank must be 'very hard'. Most pass, and so — very hard? Doesn't follow.",
   D("Cross out choices 3 and 4"),
   "Choices three and four start with 'easy'. 'Most pass, and so it's easy' is perfectly logical. Out.",
   A("Fix 1: \"and yet\" · Fix 2: \"easy\" instead of \"very hard\" appears", P('Fix 1: "and yet" · Fix 2: "easy" instead of "very hard"')),
   "Two fixes: 'and yet' instead of 'and so' — most pass, and yet it's very hard. Logical.",
   "Or keep 'and so' and replace 'very hard' with 'easy'.",
   D("Cross out choice 2"),
   "Choice two swaps 'and so' for 'and so' — no change at all. Out.",
   D("Circle choice 1"),
   "Choice 1.",
  ])]
, TOPIC),

# ---- Hebrew example 4 (hard): a sentence with two meanings
guided(2, 'vb-inf_v2_0356', 'Sentence Questions', SBQ,
 ["A sample question — a hard one.", "A sentence that can be understood in two ways."],
 [('Find both readings', [
   "Only architects who hold a first degree in sociology and graduates of a diving course will be accepted.",
   "A double meaning. By the way — a sentence can have more than two meanings. Here it has two.",
   A("Reading 1: architect + sociology + diving — all three appears", P('Reading 1: architect + sociology + diving — all three')),
   "The obvious reading: you need all three. Architect, sociology degree, diving course.",
   D("Circle 'and'"),
   A("Reading 2: (architect + sociology) OR diving appears", P('Reading 2: (architect + sociology) OR diving')),
   "The second reading: here 'and' works like 'or'. Architects with a sociology degree — OR graduates of a diving course.",
   "A diving graduate needs nothing else.",
  ]),
  ('"Only" is a condition', [
   "What's impossible under BOTH readings?",
   "Careful: 'only' tells us who CAN be accepted. It doesn't say everyone who qualifies must be accepted.",
   A("Qualifies → may be accepted, not must appears", P('Qualifies → may be accepted, not must')),
   "It reminds us of claims and logic — a condition, not a promise.",
   D("Cross out choice 1"),
   "Elad — a diving graduate — accepted. Possible under reading two. Out.",
   D("Cross out choice 2"),
   "Nir — a diving graduate — not accepted. Always possible: qualifying doesn't force acceptance. Out.",
  ]),
  ('Check each reading', [
   D("Cross out choice 3"),
   "Anat — architect and diver, no sociology degree — accepted. Reading two: she's a diver. Possible. Out.",
   D("Circle choice 4"),
   "Drora — sociology degree, but not an architect and not a diver. Reading one? No. Reading two? No.",
   "She fails both readings — so 'Drora was accepted' is impossible.",
   "Choice 4.",
  ])]
, TOPIC),

# ---- Hebrew example 5 (easy): hidden assumption — the clear kind
guided(3, 'vb-inf_v2_0362', 'Sentence Questions', SBQ,
 ["A sample question — an easy one.", "A hidden assumption."],
 [('What are they relying on?', [
   "Caffeine drinkers were persuaded more by an argument. The researchers estimate: caffeine raises concentration, so they concentrated more on the arguments.",
   "A hidden assumption: they rely on something they never said.",
   A("Two kinds: the assumption is clear · or hard to see appears", P('Two kinds: the assumption is clear · or hard to see')),
   "Two kinds of these. Sometimes the assumption is fairly clear. Sometimes it's hard to see the connection at all.",
   "This one is the clear kind.",
  ]),
  ('Fill the gap', [
   A("Concentrated more → persuaded more ? appears", P('Concentrated more → persuaded more ?')),
   "They observed: persuaded more. They explain: concentrated more. What links the two?",
   "They must assume that concentrating on arguments makes you more persuaded.",
   D("Circle choice 3"),
   "Choice 3. A person who concentrates on the arguments is persuaded by them more.",
   D("Cross out choice 4"),
   "Choice four adds a condition — only with caffeine. They never needed that.",
  ])]
, TOPIC),

# ---- Hebrew example 6 (hard): hidden assumption — the unclear kind (two speakers who know more than we do)
guided(4, 'vb-inf_v2_0355', 'Sentence Questions', SBQ,
 ["A sample question — a hard one.", "A hidden assumption of the second kind — not clear at all."],
 [("What do they know that we don't?", [
   "Osnat: nobody could translate the article from German into French — let alone into Spanish.",
   "Shlomo: so you command French better than Spanish.",
   "It sounds like two people talking past each other. They're not. They just rely on things we weren't told.",
   A("Our job: find the unstated link appears", P('Our job: find the unstated link')),
  ]),
  ('Translate the dialogue', [
   D("Write: German → French hard · German → Spanish even harder"),
   A("German→French easier than German→Spanish appears", P('German→French easier than German→Spanish')),
   "'Let alone into Spanish' — into Spanish is even harder than into French.",
   A("⇒ French better than Spanish appears", P('⇒ French better than Spanish')),
   "Shlomo concludes: French is the language she commands better.",
   "So his rule: translating INTO a language more easily means you command that language better.",
  ]),
  ('Match the letters', [
   A("C = German · A = French · B = Spanish appears", P('C = German · A = French · B = Spanish')),
   "German is the source, C. French is A, the language he says she commands better. Spanish is B.",
   D("Circle choice 1"),
   "From C into A more easily than from C into B. Choice 1.",
   D("Cross out choice 2"),
   "Choice two translates FROM A and B — the wrong direction. Always check who goes where.",
  ])]
, TOPIC),
]

# Hebrew example 3 (easy-plus, double negatives) had no matching English bank question: taught on a concept slide.
MODULES[0]['slides'].insert(3, dict(mode='concept', active=2, title='Double negatives', script=[
  "One structure to master before we start: double negatives.",
  A("not + not = yes appears", C('not … not = yes')),
  "Two negatives cancel out.",
  A("It is not unusual for the museum not to open on time. appears", C('It is not unusual for the museum not to open on time.', 36)),
  "How do we handle it? Slowly — replace one pair of negatives at a time with something positive.",
  A("not unusual → usual appears", C('not unusual → usual')),
  A("→ It is usual for the museum to open late. appears", C('→ It is usual for the museum to open late.', 36)),
  "Now it's clear. And some of you will see it halfway through — that's fine, answer as soon as it's clear.",
  "This matters a lot on the exam — and especially in sentence completion, where double negatives are everywhere.",
]))
SB.insert(2, 'Double negatives')
for sl in MODULES[0]['slides'][4:]:
    if sl.get('active', -1) >= 2: sl['active'] += 1

MEMORY = [
 dict(id='mem-sentences', after='solve-vb-inf_v2_0355', title='Understanding sentences — the toolkit',
  intro='What makes a sentence hard, and what to do about it.',
  tables=[dict(head=['Difficulty', 'What to do'], rows=[
    ['A word or expression', 'Eliminate by structure first; the key expression decides the rest'],
    ['Replacing words', 'Find what makes it (il)logical; test each swap'],
    ['Double negatives', 'Turn one pair of negatives into a positive at a time'],
    ['Two meanings', 'Write both readings ("and" can act as "or"); check each choice against both'],
    ['Hidden assumption', 'Find the unstated link between what was said and the conclusion'],
  ])],
  tips=['"Only" = who can be accepted — not who must be.', 'Condition not met → result unknown.',
        'The skill runs through all of verbal: no understanding, no conclusions.']),
]
