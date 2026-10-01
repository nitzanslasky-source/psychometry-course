# Verbal · Topic 44 · Understanding paragraphs.
# Hebrew hebverbal.txt 2274-2772 decides the concepts, structure, order, methods, tips and verdicts.
# Every guided question is an ORIGINAL course question (content/verbal_originals_B.json), quoted word for word;
# each mirrors the type, trap and difficulty of one real NITE question (field "mirrors").
from dsl import *

T44 = 44
SBL = ['Where they appear', 'Two kinds', 'Kind 1: it says so', 'Kind 2: understand it']
GQ = 'Paragraph Questions'
SBQ = ['Kind 1 · not correct', 'Kind 1 · hard text', 'Kind 2 · not implied', 'Kind 2 · best summary',
       'Concept in paragraph', 'Apply the idea']

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
  "The Hula Valley, a lake that was drained, and a lake that was created later. Let's read.",
  "\"According to the paragraph, which of the following statements about Lake Agmon is not correct?\"",
  D("Underline 'According to the paragraph' and circle 'not'"),
  "Notice what they ask: according to the paragraph, what is not correct.",
  A("According to the paragraph → the answer is in the text appears", P("According to the paragraph → the answer is in the text", y=120)),
  "That means the answer is in the text. I just go through the choices and check each one against what's written.",
  "No inference needed here. This is kind one.",
 ]),
 ('Check each choice', [
  "Choice one: \"It was drained in the 1950s in order to add farmland.\"",
  D("Underline 'In the years 1951-1958 the lake and most of the swamps were drained'"),
  "Which lake was drained in the fifties? The old Hula Lake. Lake Agmon was created only in the nineties, when part of the drained area was flooded again.",
  A("Not correct → that's our answer appears", P("Not correct → that's our answer", y=120)),
  D("Circle choice 1"),
  "Choice 1.",
  "In the exam: a quick look at the others before you mark. Let's do that look.",
  "Choice two: \"Its area is smaller than the area that was drained.\"",
  D("Underline 'a small part of the drained area was flooded again'"),
  "Only a small part of the drained area was flooded again. Correct, and they asked for not correct. Out.",
  D("Cross out choice 2"),
  "Choice three: it was created after it turned out that the drainage had caused damage. 'Therefore' - because of the damage. Correct. Out.",
  D("Cross out choice 3"),
  "Choice four: birds spend the winter at it. Tens of thousands of cranes, every year. Correct. Out.",
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
  D("Bracket 'Some of them claim…' and write 'Group 1'"),
  "Group one: the unknown author says the goal of painting is perfect imitation of nature. But he can't have seen that as the painter's task, because in another chapter he writes that no painter can achieve it.",
  D("Bracket 'Others claim…' and write 'Group 2'"),
  "Group two: the painter must nevertheless come as close as possible to this goal, even though he will never reach it.",
  A("nevertheless · this imitation · this goal → go back: what does it point to? appears", P("nevertheless · this imitation · this goal → go back: what does it point to?", y=120)),
  "When a text points back, like 'nevertheless' or 'this goal', stop and pin down exactly what it means. 'Nevertheless' means: even though it can't be reached.",
  A("Both: can't be reached · They differ: the painter's task appears", P("Both: can't be reached · They differ: the painter's task", y=200)),
  "So: both groups agree the goal can't be fully reached. They differ on the task of the painter.",
 ]),
 ('Check the choices', [
  "Choice one says they disagree about the goal, since the treatise doesn't state it. But the treatise does state it: perfect imitation of nature. Out.",
  D("Cross out choice 1"),
  "Choice two: which colors painters in Florence had. Nobody argues about that. Out.",
  D("Cross out choice 2"),
  "Choice three: \"Both groups agree that, according to the author, a painter cannot achieve a perfect imitation of nature.\"",
  "Group one: no painter can achieve it. Group two: 'nevertheless' as close as possible, 'even though he will never reach it'. Both. That's exactly what's written.",
  D("Circle choice 3"),
  "Choice 3.",
  "Before marking - a quick look at the last one:",
  "Choice four: whether better colors would have made it possible. Neither group raises that question. Out.",
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
  "Choice one: \"Had the water level of the Sea of Galilee not dropped in 1989, the remains of the site would probably not have been discovered in that year.\"",
  D("Underline 'were discovered in 1989, when the water level of the lake dropped to an unusually low level'"),
  "The site was found when the water went down. Without that, probably not that year. Implied. Out.",
  D("Cross out choice 1"),
  "Choice two: the researchers drew their conclusion from the kinds of seeds. The weeds of cultivated fields led them to the conclusion. Implied. Out.",
  D("Cross out choice 2"),
  "Choice three: \"Agriculture was already widespread in the region when the inhabitants of Ohalo 2 tried to cultivate cereals.\"",
  D("Underline 'about 11,000 years before agriculture became widespread in the region'"),
  "Wait. They tried to cultivate about 11,000 years before agriculture became widespread - not when it already was. The timeline is flipped. Not implied.",
  D("Circle choice 3"),
  "Choice 3.",
  "Before marking - a quick look at the last one:",
  "Choice four: some of these weeds grow today in cultivated fields. That's written. Implied. Out.",
  D("Cross out choice 4"),
 ]),
], T44),

# ------------------------------------------------------------------ Q · Kind 2, best summary: "true but not the answer" and "too strong"
# (NITE guide, critical reading: a summary question "may include a response that is implied by the text or that is even
#  stated explicitly in it, but does not summarize it"). Original question vo-44-201 (content/verbal_originals_M.json).
guided(3, 'vo-44-201', GQ, SBQ, ["A sample question – medium level.", "A summary question, and its two favorite traps."], [
 ('Two traps', [
  "\"Which of the following best summarizes the paragraph?\" Kind two.",
  D("Underline 'best summarizes'"),
  "Summary, main idea, conclusion - these questions have two favorite traps.",
  A("Trap 1: true - but not the answer appears", P("Trap 1: true but not the answer – stated in the text, but only a detail", y=120)),
  "Trap one: a choice that's true. It's even written in the paragraph. But it's a detail - it doesn't summarize. NITE's own guide warns about exactly this.",
  A("Trap 2: too strong appears", P("Trap 2: too strong – says more than the text: everyone · always · never · proven", y=200)),
  "Trap two: a choice that says too much. Everyone, always, never, proven - when the text talked about one case.",
  A("Pick the most careful choice that still says something appears", P("Pick the most careful choice that still says something", y=280)),
  "So pick the most careful choice - but one that still says something.",
 ]),
 ('Understand, then check', [
  "First, what does the paragraph build to?",
  D("Underline 'the number of residents holding a library card hardly changed'"),
  "Visits went up by a third - but the same people, just at a different hour. New readers? Hardly any.",
  D("Underline 'should therefore look for other means of achieving this goal'"),
  "And the ending: the goal - new readers - wasn't achieved.",
  "Choice one: visits rose by about a third. It's written, word for word. But is that the point? No - it's the detail the paragraph turns against. True, but not the answer.",
  D("Cross out choice 1"),
  "Choice two: extending hours never brings any library new readers. One library, one year - and suddenly never? Too strong.",
  D("Cross out choice 2"),
  "Choice three: hard to know whether it had any effect. Careful, all right - but wrong. The visits clearly rose. And it says nothing about the point.",
  D("Cross out choice 3"),
  "Choice four: more visits - but no new readers. Careful, and it says the whole point.",
  D("Circle choice 4"),
  "Choice 4.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · concept in the paragraph (Hebrew 2554-2667, medium-plus)
guided(4, 'vo-44-004', GQ, SBQ, ["A sample question – medium-plus."], [
 ('Read slowly – once', [
  "A question about a concept from the paragraph: \"Why do these researchers call the nurse 'the last link'?\"",
  D("Circle 'the last link'"),
  "To answer it, we have to understand the paragraph. Which brings me to a very important point.",
  A("Don't skim → run to the choices → run back to the text appears", P("Don't skim → run to the choices → run back to the text", y=120)),
  "These questions have a lot of text. Many students skim, run to the choices, and for every choice run back to the text, and back, and back. Wrong approach. A waste of time.",
  A("Read slowly the first time – understand, then go to the choices appears", P("Read slowly the first time – understand, then go to the choices", y=200)),
  "Read slowly, the first time, and understand as much as you can. Then, when you reach the right answer, you'll know it right away.",
  "Torn between two? Then go back to the text to decide. Not for every choice.",
 ]),
 ('What do they actually claim?', [
  "So instead of going through the choices, let's understand the paragraph.",
  D("Underline 'most errors in the wards are indeed human errors, but they begin long before the nurse's shift'"),
  "Yes, most errors are human errors. But they begin long before the nurse's shift.",
  D("Bracket 'in the planning of the shifts, in the design of the labels…, in the preparation of the doses… and in the training of the staff'"),
  "Where? In planning the shifts, designing the labels, preparing the doses, training the staff. People far from the bedside.",
  A("Error = a chain · the nurse = its last link appears", P("Error = a chain of people · the nurse = only its last link", y=120)),
  "The nurse is only the last to handle the medicine - the one in whose hands the error is revealed. The error passed through a whole chain before her. That's why she's the last link.",
 ]),
 ('Now the choices', [
  "Choice one: most errors are human, but a good part come from faulty equipment. They never mention equipment. Out.",
  D("Cross out choice 1"),
  "Choice two: \"Because in their opinion, people who do not treat the patient directly are often partly responsible for the errors.\"",
  "Exactly what we understood.",
  D("Circle choice 2"),
  "Choice 2.",
  "A quick look at the others before marking:",
  "Choice three: a nurse is human, so we can't expect her never to make a mistake. Sounds kind, but that's not their argument. They move the responsibility along the chain; they don't excuse errors. Out.",
  D("Cross out choice 3"),
  "Choice four: the nurse usually discovers others' errors in time and prevents harm. The text says the error is revealed in her hands, not that she prevents it. Out.",
  D("Cross out choice 4"),
  "Not a simple question, but we got through it.",
 ]),
], T44),

# ------------------------------------------------------------------ Q · apply the idea (Hebrew 2668-2770, medium-plus, even hard)
guided(5, 'vo-44-005', GQ, SBQ, ["A sample question – medium-plus, even hard.",
                                  "Before we read, remember what we learned: read slowly, and understand."], [
 ('Read, understand', [
  "Let's apply it.",
  D("Underline 'It does not spread from place to place as one fixed game, but splits into many versions'"),
  "A folk game doesn't spread as one fixed game, it \"splits into many versions\". Not sure I understand yet. Keep reading.",
  D("Underline 'until almost every place has a version of its own'"),
  "One village adds a rule, another changes the counting of points, until almost every place has its own version. Eleven versions of one game in one small region. Now it's getting clearer.",
  A("Game → more rules, more versions, one for each place appears", P("Game → more rules, more versions, one for each place", y=120)),
  "And in the end those local versions give the inhabitants of a place a sense of a common identity.",
 ]),
 ('Apply – one step further', [
  "\"Which of the following processes best illustrates the claim made in the article?\"",
  A("Application: read → understand → apply to a new case appears", P("Application: read → understand → apply to a new case", y=120)),
  "This is an application question. Another kind of understanding, one step further. You read, you understood. Now can you apply it?",
  "Choice one: a sports association made a village game into one game with the same rules across the country. That's a game spreading in one form, not splitting into versions. Out.",
  D("Cross out choice 1"),
  "Choice two: several sets of rules became one set. That's the reverse: convergence. Out.",
  D("Cross out choice 2"),
  "Choice three: flying kites on the first day of spring has almost disappeared. That's decline, not splitting into versions. Out.",
  D("Cross out choice 3"),
  "Choice four: \"A game that in the past had no fixed rules is played today in each town of the valley according to scoring rules of its own.\"",
  "Each town, its own version, out of one game that had no fixed rules. That's splitting into versions.",
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
        'Summary / main idea / conclusion: a choice can be stated in the text and still not summarize it; a choice can say too much (everyone, always, proven). Pick the most careful choice that still says something.',
        'In the exam: a quick look at the other choices, then mark the answer and move on.']),
]
