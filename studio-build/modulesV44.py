# Verbal · Topic 44 · Understanding paragraphs.
# Hebrew hebverbal.txt 2274-2772 decides the concepts, structure, order, methods, tips and verdicts.
# Every guided question is an ORIGINAL course question (content/verbal_originals_B.json), quoted word for word;
# each mirrors the type, trap and difficulty of one real NITE question (field "mirrors").
from dsl import *

T44 = 44
SBL = ['Where they appear', 'Two kinds', 'Kind 1: it says so', 'Kind 2: understand it']
GQ = 'Paragraph Questions'
SBQ = ['Kind 1 · not correct', 'Kind 1 · hard text', 'Kind 2 · not implied', 'Concept in paragraph', 'Apply the idea']

MODULES = [
# ------------------------------------------------------------------ lesson (Hebrew 2274-2290)
lesson('vr44-paragraphs', 'Understanding Paragraphs', SBL, [
 dict(mode='title', title='Understanding Paragraphs', script=[
  "Understanding paragraphs.",
  "The most common question type in the whole understanding-and-inference part of the verbal section.",
  "Let's see what they are, and how to split them.",
 ]),
 dict(mode='concept', active=0, title='Where they appear', script=[
  A("Paragraph questions: in the understanding-and-inference part", T('Paragraph questions – inside the understanding-and-inference part of Verbal Reasoning', size=40, x=410, y=110, w=1140)),
  "These questions sit inside the understanding-and-inference part of the verbal section.",
  A("The most common type there", T('The most common question type in that part', size=40, x=410, y=260, w=1140)),
  "And they're the most common type there. So we'd better get them right.",
 ]),
 dict(mode='concept', active=1, title='Two kinds', script=[
  "Broadly, we split them into two kinds.",
  A("Kind 1: it says so in the paragraph", T('Kind 1 – What does the paragraph say? (correct / not correct according to it)', size=40, x=410, y=110, w=1140)),
  "Kind one: you get a paragraph, and they ask what's correct, or not correct, according to what's written.",
  A("Kind 2: what's behind the words", T('Kind 2 – What lies behind the words? (implied, meant, the idea)', size=40, x=410, y=260, w=1140)),
  "Kind two: a paragraph where you have to understand what stands behind what's written. What's implied, what's meant.",
 ]),
 dict(mode='concept', active=2, title='Kind 1: it says so', script=[
  A("Kind 1: read and check – don't over-think", T('Kind 1: read, then check each choice against the text. No need to over-think.', size=40, x=410, y=110, w=1140)),
  "Kind one: I don't need to think too much. Just read and check: which choice appears in the paragraph, and which doesn't.",
  A("Usually the easier ones", T('Usually the easier questions of this topic', size=40, x=410, y=260, w=1140)),
  "These are usually the easier questions in this topic.",
 ]),
 dict(mode='concept', active=3, title='Kind 2: understand it', script=[
  A("Kind 2: understand what's implied / meant", T('Kind 2: understand what is implied – what the writer means', size=40, x=410, y=110, w=1140)),
  "Kind two: I have to understand what's implied, what the words are getting at.",
  A("These can be hard", T('These can be far from easy', size=40, x=410, y=260, w=1140)),
  "And these can be not easy at all.",
  "Let's start with a sample question.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · Kind 1, "not correct" (Hebrew 2291-2347, easy-plus)
guided(0, 'vo-44-001', GQ, SBQ, ["A sample question – easy-plus."], [
 ('Kind 1: find it in the text', [
  "Two lakes and their ice. Let's read.",
  "\"According to the paragraph, which of the following statements about Lake Orven is not correct?\"",
  D("Underline 'According to the paragraph' and circle 'not'"),
  "Notice what they ask: according to the paragraph, what is not correct.",
  A("According to the paragraph → the answer is in the text appears", P("According to the paragraph → the answer is in the text", y=120)),
  "That means the answer is in the text. I just go through the choices and check each one against what's written.",
  "No inference needed here. This is kind one.",
 ]),
 ('Check each choice', [
  "Choice one: \"It gets less sunlight than Lake Talva.\"",
  D("Underline 'it lies in the shadow of a steep cliff that blocks most of the sunlight, and its ice therefore stays thick all year'"),
  "Which lake is in the shadow of the cliff? Lake Talva. That's why its ice stays thick all year. Lake Orven's ice is thin and melts, so it's not the one getting less sunlight.",
  A("Not correct → that's our answer appears", P("Not correct → that's our answer", y=120)),
  D("Circle choice 1"),
  "Choice 1.",
  "In the exam, mark it and move on. Here in the lesson, let's check the others too.",
  "Choice two: \"Its ice is thin compared with Lake Talva's.\"",
  D("Underline 'Lake Orven among them, this ice is thin'"),
  "Lake Orven's ice is thin; Lake Talva's is thick. Correct, and they asked for not correct. Out.",
  D("Cross out choice 2"),
  "Choice three: \"The air above it can stay below freezing.\" Ice forms when the air stays below freezing for several days, and Lake Orven has ice. Correct. Out.",
  D("Cross out choice 3"),
  "Choice four: \"Its ice does not remain throughout the year.\" It melts every spring. Correct. Out.",
  D("Cross out choice 4"),
 ]),
], T44),

# ------------------------------------------------------------------ Q · Kind 1, hard text (Hebrew 2348-2464, hard)
guided(1, 'vo-44-002', GQ, SBQ, ["A sample question – a hard one."], [
 ('Hard text – answer in the text', [
  "\"Which of the following statements is correct according to the paragraph?\"",
  D("Underline 'correct according to the paragraph'"),
  "What are they asking? What's correct according to the paragraph. So again, the answer appears in the paragraph.",
  A("Hard paragraph – but the answer is in the text appears", P("Hard paragraph – but the answer is in the text", y=120)),
  "No big inference. But the paragraph is hard. We need to read slowly, and understand it.",
 ]),
 ('Say it in your own words', [
  "Let's put some order into this long, complex text.",
  D("Bracket 'One group maintains…' and write 'Group 1'"),
  "Group one: Menck says the goal of painting is perfect imitation of nature. But he can't have seen that as the painter's calling, because he also shows no painter can reach it.",
  D("Bracket 'According to another group…' and write 'Group 2'"),
  "Group two: even so, the painter's calling is to get as close to that goal as possible.",
  A("even so · the same · this goal → go back: what does it point to? appears", P("even so · the same · this goal → go back: what does it point to?", y=120)),
  "When a text points back, like 'even so' or 'this goal', stop and pin down exactly what it means. 'Even so' means: even though it can't be reached.",
  A("Both: can't be reached · They differ: the painter's calling appears", P("Both: can't be reached · They differ: the painter's calling", y=200)),
  "So: both groups agree the goal can't be fully reached. They differ on the painter's calling.",
 ]),
 ('Check the choices', [
  "Choice one says they disagree about the goal, since the treatise doesn't say what it is. But the treatise does say it: perfect imitation of nature. Out.",
  D("Cross out choice 1"),
  "Choice two: what a perfect imitation would consist of. Nobody argues about that. Out.",
  D("Cross out choice 2"),
  "Choice three: \"Both groups of scholars agree that, according to Menck, no painter can fully achieve a perfect imitation of nature.\"",
  "Group one: beyond any painter's reach. Group two: 'even so', as close as possible. Both. That's exactly what's written.",
  D("Circle choice 3"),
  "Choice 3.",
  "In the exam we mark and move on. In the lesson, the last one:",
  "Choice four: whether a painter's materials can make it possible. Both groups say pigments can't. No disagreement. Out.",
  D("Cross out choice 4"),
  "A kind-one question, and not an easy one at all.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · Kind 2, not implied (Hebrew 2465-2553, medium)
guided(2, 'vo-44-003', GQ, SBQ, ["A sample question – medium level."], [
 ('Kind 2: what is not implied', [
  "\"Which of the following is not implied in the paragraph?\"",
  D("Underline 'not implied'"),
  "This is no longer 'what appears in the paragraph'. We need to understand what's implied, or not implied.",
  "That takes us to kind two.",
 ]),
 ('Kind 2 – many wordings', [
  "The wordings of kind two are very varied. Here's a partial list:",
  A("Main idea · central claim · best summary · best title appears", P("Main idea · central claim · best summary · best title", y=210)),
  "What's the main idea, the central claim, what best summarizes the paragraph, what title fits it.",
  A("Implied / not implied · purpose · author's position appears", P("Implied / not implied · purpose · author's position", y=300)),
  "What's implied, or not implied. The purpose of the paragraph. The author's position.",
  A("Completion · rephrasing · a concept in the paragraph appears", P("Completion · rephrasing · a concept in the paragraph", y=390)),
  "Completion: a missing part, and what could fit. Rephrasing: which idea is most similar. And a question about one concept from the paragraph.",
  "Ours is 'not implied'. Let's go through the choices.",
 ], dict(pre=[T('Kind 2 – the wording varies a lot', size=48, x=410, y=100, w=1140)])),
 ('Check each choice', [
  "Choice one: \"The peat bog on Harrow Tor preserved objects made of bone for thousands of years.\"",
  D("Underline 'A survey of a peat bog … has uncovered dozens of bone fishhooks, about 9,000 years old'"),
  "Bone hooks, 9,000 years old, came out of the bog. So the bog kept them all that time. Implied. Out.",
  D("Cross out choice 1"),
  "Choice two: the report treats the uniform sizes as evidence of how much fish was caught. It says the uniformity shows they caught far more than they needed. Implied. Out.",
  D("Cross out choice 2"),
  "Choice three: \"Farmers had already settled on Harrow Tor by the time the fishhooks found in the bog were carved.\"",
  D("Underline 'the farmers who settled there some 1,500 years later'"),
  "Wait. The farmers settled 1,500 years later. The report says the fishing people already did something known from the farmers, not that farmers were there. The timeline is flipped. Not implied.",
  D("Circle choice 3"),
  "Choice 3.",
  "In the exam we mark and move on. In the lesson, the last one:",
  "Choice four: the farmers who came later caught more fish than they needed. The practice was recorded among them, so yes. Implied. Out.",
  D("Cross out choice 4"),
 ]),
], T44),

# ------------------------------------------------------------------ Q · concept in the paragraph (Hebrew 2554-2667, medium-plus)
guided(3, 'vo-44-004', GQ, SBQ, ["A sample question – medium-plus."], [
 ('Read slowly – once', [
  "A question about a concept from the paragraph: \"Why is Dr. Sharon known as 'the defender of nurses'?\"",
  D("Circle 'the defender of nurses'"),
  "To answer it, we have to understand the paragraph. Which brings me to a very important point.",
  A("Don't skim → run to the choices → run back to the text appears", P("Don't skim → run to the choices → run back to the text", y=120)),
  "These questions have a lot of text. Many students skim, run to the choices, and for every choice run back to the text, and back, and back. Wrong approach. A waste of time.",
  A("Read slowly the first time – understand, then go to the choices appears", P("Read slowly the first time – understand, then go to the choices", y=200)),
  "Read slowly, the first time, and understand as much as you can. Then, when you reach the right answer, you'll know it right away.",
  "Torn between two? Then go back to the text to decide. Not for every choice.",
 ]),
 ('What does she actually claim?', [
  "So instead of going through the choices, let's understand the paragraph.",
  D("Underline 'are right, but only if \"human error\" is properly understood'"),
  "People say human error is behind most mistakes on hospital wards. She says: right, but only if you understand 'human error' properly.",
  D("Bracket 'The administrator…, the engineer…, the pharmacist…, the lecturer…'"),
  "Why? The administrator, the engineer, the pharmacist, the lecturer: they're all human too. Nearly every mistake traces back to an oversight by one of them.",
  A("Human error ≠ just the nurse → she defends the nurse appears", P("Human error ≠ just the nurse → she defends the nurse", y=120)),
  "The nurse just has to deal with everyone else's oversights. So she widens 'human error', and part of the blame moves away from the nurse. That's why she's the defender of nurses.",
 ]),
 ('Now the choices', [
  "Choice one: most mistakes are human, but a good share come from faulty equipment. She never mentions equipment. Out.",
  D("Cross out choice 1"),
  "Choice two: \"Because she believes that people who are not directly involved in treating the patient often bear part of the blame for mistakes.\"",
  "Exactly what we understood.",
  D("Circle choice 2"),
  "Choice 2.",
  "In the exam, mark and move on. In the lesson:",
  "Choice three: nurses are human, so we can't expect them to be perfect. Sounds kind, but that's not her argument. She moves the blame; she doesn't excuse errors. Out.",
  D("Cross out choice 3"),
  "Choice four: nurses often prevent harm by catching others' oversights. The text says the nurse must deal with them, not that she succeeds. Out.",
  D("Cross out choice 4"),
  "Not a simple question, but we got through it.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · apply the idea (Hebrew 2668-2770, medium-plus, even hard)
guided(4, 'vo-44-005', GQ, SBQ, ["A sample question – medium-plus, even hard.",
                                  "Before we read, remember what we learned: read slowly, and understand."], [
 ('Read, understand', [
  "Let's apply it.",
  D("Underline 'Rather than spreading in a single fixed form, it branches out'"),
  "A folk game doesn't spread in one fixed form, it \"branches out\". Not sure I understand yet. Keep reading.",
  D("Underline 'until each place has a version that is recognizably its own'"),
  "One town adds a rule, another changes the scoring, until each place has its own version. Now it's getting clearer.",
  A("Game → more rules, more versions, one for each town appears", P("Game → more rules, more versions, one for each town", y=120)),
  "And in the end those local versions give a town its identity. They set it apart from its neighbors.",
 ]),
 ('Apply – one step further', [
  "\"Which of the following processes best illustrates Dr. Ronen's claim?\"",
  A("Application: read → understand → apply to a new case appears", P("Application: read → understand → apply to a new case", y=120)),
  "This is an application question. Another kind of understanding, one step further. You read, you understood. Now can you apply it?",
  "Choice one: an association made a village game popular across the country. That's a game spreading, not a game splitting into town versions. Out.",
  D("Cross out choice 1"),
  "Choice two: several sets of rules became one uniform set. That's the reverse: convergence. Out.",
  D("Cross out choice 2"),
  "Choice three: a kite-flying contest has almost disappeared. That's decline, not branching out. Out.",
  D("Cross out choice 3"),
  "Choice four: \"Today each town in the valley plays the stone-throwing game with its own detailed scoring rules, whereas at first the game had no fixed rules at all.\"",
  "Each town, its own version. More detailed over time. That's branching out.",
  D("Circle choice 4"),
  "Choice 4.",
  "And we're done with this one.",
 ]),
], T44),
]

MEMORY = [
 dict(id='mem-paragraph-types', after='solve-vo-44-005', title='Paragraph questions: know the kind',
  intro='First decide which kind of question it is. That tells you how to work.',
  tables=[dict(head=['Kind', 'Typical wording', 'How to work'], rows=[
   ['1 · It says so', 'According to the paragraph… · Which is (not) correct… · not stated in the paragraph', 'The answer is in the text: check each choice against what is written'],
   ['2 · Understand it', 'Main idea / central claim · best summary / title · implied / not implied', 'Understand the paragraph first, then choose'],
   ['2 · Understand it', "Purpose · author's position · completion · rephrasing · a concept in the paragraph", 'Understand the paragraph first, then choose'],
   ['2 · Apply it', 'Which example / process best illustrates…', 'Understand the idea, then apply it to the new case'],
  ])],
  tips=['Read slowly the first time and understand. Do not bounce between the choices and the text.',
        'Back to the text only when you are torn between two choices.',
        'Pointer words (even so, the former, the latter, this goal): stop and pin down exactly what is meant.',
        'In the exam: mark the answer and move on.']),
]
