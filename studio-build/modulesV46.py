# Verbal Reasoning · Topic 46 · Strengthening and weakening arguments.
# Hebrew (hebverbal.txt 3145-3548, "מחזק מחליש") gives the concepts, order, methods and verdicts;
# every guided question is an ORIGINAL course question (content/verbal_originals_B.json), used word for word;
# each mirrors the type, trap and difficulty of one real NITE question (field "mirrors").
from dsl import *

T46 = 46
GT = 'Strengthen & Weaken Questions'
SBQ = ['Q1 · Support it', 'Q2 · Does not weaken', 'Q3 · Strengthen it', 'Q4 · Chicken and egg',
       'Q5 · Attack the basis', 'Q6 · Clear-cut']

MODULES = [
# ------------------------------------------------------------------ lesson
lesson('vr46-intro', 'Strengthen and Weaken', ['Data and conclusion', 'Which way?'], [
 dict(mode='title', title='Strengthen and Weaken', script=[
  "Strengthen and weaken questions.",
  "They sit in the inference section of the verbal chapter, and once you know the tricks, they're fast points.",
 ]),
 dict(mode='concept', active=0, title='Data and conclusion', script=[
  "Here's the setup.",
  A("Data → a conclusion drawn from it appears", T('The question gives data → and a conclusion someone drew from it', size=40)),
  "The question gives you some data, and a conclusion someone drew from that data.",
  A("Each choice adds new data appears", T('Each answer choice adds one more piece of data', size=40)),
  "Then every answer choice adds one more piece of data.",
  "Your job: understand how that new data affects the conclusion.",
 ]),
 dict(mode='concept', active=1, title='Which way?', script=[
  A("Strengthens · weakens · irrelevant appears", T('New data: strengthens · weakens · irrelevant', size=44)),
  "Three possibilities: the new data strengthens the conclusion, weakens it, or has nothing to do with it.",
  A("No proof – more or less likely appears", T('No proof here – only: more likely or less likely?', size=40)),
  "Nothing here proves or disproves anything. We only ask: does it make the conclusion more likely, or less?",
  "And read the question carefully: sometimes it's 'strengthens', sometimes 'weakens', sometimes 'does not weaken'.",
  "Let's start with a sample question.",
 ]),
], T46),

# ------------------------------------------------------------------ Q1 · Hebrew ex. 1 (easy-plus): support a hypothesis
guided(0, 'vo-46-001', GT, SBQ,
 ["A sample question – easy-plus.", "A shop owner, a drop in sales, and her explanation."],
 [('Read the claim', [
   "Nurit replaced the yellowish lighting in her bookstore with strong white lighting.",
   "Three weeks later her sales had dropped by about a fifth, and she blamed the new lighting: in her opinion it discourages customers from browsing at length among the shelves.",
   D("Underline: She attributed the drop to the new lighting"),
   "That's the conclusion: the lighting caused the drop - because customers browse less.",
   "The question: which statement strengthens her explanation?",
   A("Goal: support 'lighting → less browsing → sales fell' appears", P("Goal: support 'lighting → less browsing → sales fell'")),
  ]),
  ('Irrelevant data', [
   "Choice one: most of the customers are students from the nearby college.",
   "Wait, what does that have to do with the lighting? Or with the drop in sales?",
   A("Not about the lighting or the sales → irrelevant appears", P('Not about the lighting or the sales → irrelevant')),
   "Nothing. It's irrelevant, so it doesn't help her. Cross it out.",
   D("Cross out choice 1"),
  ]),
  ('The gambler test', [
   "Choice two: the pharmacy across the street has been lit with white light for years, and there are always many customers.",
   "A pharmacy isn't a bookstore, so it's not related? Actually, it is.",
   "It's an example going the other way: white light, and a crowded shop.",
   A("Gambler test appears", P('Gambler test: bet on the conclusion – does the new fact shake your bet?')),
   "Here's a great trick: the gambler test. Imagine you've put money on Nurit being right.",
   "Now someone tells you: across the street, the same lamps, and it's packed. Feeling a bit less sure? Then it weakens.",
   A("Counterexample → weakens appears", P('Counterexample → weakens')),
   "That's a counterexample. It weakens, and we want support. Cross it out.",
   D("Cross out choice 2"),
  ]),
  ('Supporting evidence', [
   "Choice four: in the weeks after the change, customers spent on average much less time in the store than before.",
   "Her explanation had a middle step: the lighting makes people browse less. And here it is - they really spent less time in the store.",
   D("Write: new lighting → less time in the store → sales ↓"),
   A("Supporting evidence appears", P('Supporting evidence: the data shows the claimed mechanism at work')),
   "That's supporting evidence. The step her explanation relies on actually happened, so it strengthens her explanation.",
   D("Circle choice 4"),
   "Choice four.",
  ]),
  ('The last choice', [
   "On the exam you mark it and move on. In the lesson, let's check the last one too.",
   "Choice three: ten days before the lighting was replaced, a large bookstore that sells at a discount opened in the same street.",
   "Gambler test: does that shake my bet on the lighting? Yes. There's another reason sales could fall.",
   "So it weakens her explanation. We'll give this idea its name in the next question. It's the big one.",
   D("Cross out choice 3"),
  ])], T46),

# ------------------------------------------------------------------ Q2 · Hebrew ex. 2 (easy-plus): "does not weaken" – alternative explanation
guided(1, 'vo-46-002', GT, SBQ,
 ["Another sample question – easy-plus.", "This time there's a twist in the question: 'does not weaken'."],
 [('Read the question', [
   "Ziva saw her neighbor, Mr. Adler, leave several chairs painted bright yellow on the sidewalk for the garbage collectors.",
   "Her conclusion: Mr. Adler doesn't like yellow furniture.",
   D("Underline: does not weaken"),
   "Which statement does not weaken the conclusion?",
   "Does not weaken: does that mean it strengthens? Not necessarily. It could also be irrelevant.",
   A("Find the 3 that weaken appears", P("'Does not weaken' → find the 3 that weaken, cross them out")),
   "So here's the method: find the three that do weaken and cross them out. The one that's left is the answer.",
  ]),
  ('Alternative explanation', [
   "Choice one: every piece of furniture in Mr. Adler's apartment is painted yellow.",
   "Wait. If everything he owns is yellow, throwing some of it out says nothing about the color.",
   A("Alternative explanation appears", P('Alternative explanation: another reason for the same data')),
   "That's an alternative explanation: a different reason that explains the same data.",
   "Gambler test: I bet he dislikes yellow furniture... but all his furniture is yellow? My bet just got shakier. It weakens.",
   D("Cross out choice 1"),
   "Choice two: the chairs he put out had cracked or wobbly legs.",
   "Another reason! He threw them out because they were broken, not because they're yellow.",
   D("Cross out choice 2"),
  ]),
  ('The top way to weaken', [
   "Choice four: his daughter had recently bought him a new dining set.",
   "Again, a different reason to throw out the old chairs. Alternative explanation. Cross it out.",
   D("Cross out choice 4"),
   A("Alternative explanation = #1 way to weaken appears", P('Alternative explanation = the most common way to weaken')),
   "Alternative explanation is the most common way to weaken in these questions. Very, very important to understand.",
   "We don't know which reason is the true one. But just offering another reason weakens her conclusion.",
  ]),
  ('What remains', [
   "Choice three: Mr. Adler received the yellow chairs as a gift a month before his wedding.",
   "When and how he got them: does that tell us why he threw them out? No.",
   A("Irrelevant → does not weaken appears", P('Irrelevant → does not weaken')),
   "Irrelevant. So it does not weaken.",
   D("Circle choice 3"),
   "Choice three.",
   A("Number vs percentage appears", P('Watch the data: a number or a percentage?')),
   "One more tip for these questions: watch whether the data gives a number or a percentage.",
   "A place with far more customers will have more complaints: the number goes up, while the percentage may stay the same. Another reason, another alternative explanation.",
  ])], T46),

# ------------------------------------------------------------------ Q3 · Hebrew ex. 3 (medium): negate an alternative explanation · flip it
guided(2, 'vo-46-003', GT, SBQ,
 ["A sample question – medium level.", "Now the other side: how do you strengthen a conclusion?"],
 [('Read the study', [
   "Dr. Elkin divided twelve volunteers into two teams, three and nine, and gave each team an hour to find objects hidden in a garden of the same size.",
   "The team of nine found three times as many objects.",
   "His hypothesis: in tasks of this kind, the size of the team affects its success.",
   D("Underline: the size of the team affects its success"),
   "Which statement strengthens his hypothesis?",
  ]),
  ('Rival explanations', [
   "Choice one: one member of the large team had helped hide the objects.",
   "Gambler test: that's another reason the nine did better. An alternative explanation. It weakens.",
   D("Cross out choice 1"),
   "Choice three: in the small team's garden, the objects were hidden in more difficult places.",
   "Another reason: the three had it harder. It weakens.",
   D("Cross out choice 3"),
   "Choice four: the large team searched in the morning, the small team at noon, in the heat.",
   "Again the three had it harder. Another reason. It weakens.",
   D("Cross out choice 4"),
  ]),
  ('Negate the alternative', [
   "Choice two: the small team had taken part in such searches before; the large team had not.",
   "Experience: that could have been an alternative explanation. But look which way it points.",
   "The experienced team lost. The bigger team won, even though it had less experience.",
   A("Negating an alternative explanation → strengthens appears", P('Negating an alternative explanation → strengthens')),
   "That's negating an alternative explanation: the other possible reason is ruled out. It even works against the result, and the result still happened.",
   "It's the main way to strengthen, just as the alternative explanation is the main way to weaken.",
  ]),
  ('Flip the fact', [
   "Negating an alternative explanation is usually harder to spot. Here's a trick many students find easier.",
   A("Flip the fact appears", P('Flip it: if the flipped fact weakens → the original strengthens')),
   "Flip the fact. Suppose the nine were the experienced ones.",
   "Then we'd say: they won because of experience, not because of size. That weakens.",
   "If the flipped version weakens, the original strengthens.",
   D("Circle choice 2"),
   "Choice two.",
  ])], T46),

# ------------------------------------------------------------------ Q4 · Hebrew ex. 4 (medium-plus): a type of alternative explanation – chicken and egg
guided(3, 'vo-46-004', GT, SBQ,
 ["A sample question – medium-plus.", "Alternative explanations come in types. Here's one you'll meet again and again."],
 [('Read the claim', [
   "Given: among people who use a certain skin cream, the proportion with dry skin is higher than in the general population.",
   "The hypothesis: dry skin is a side effect of the cream.",
   D("Write: cream → dry skin"),
   "Cause: the cream. Effect: dry skin.",
   "Which finding weakens the hypothesis?",
  ]),
  ('Chicken and egg', [
   "Choice three: the cream is meant to relieve the itching caused by dry skin.",
   "Wait, so who uses the cream? People who already have dry skin!",
   D("Draw the arrow the other way: dry skin → cream"),
   A("Chicken and egg appears", P('Chicken and egg: cause and effect swapped')),
   "Chicken and egg. What came first? The hypothesis says the cream came first. This choice says the dry skin came first.",
   "That's an alternative explanation of a special type: cause and effect swapped. It weakens.",
   D("Circle choice 3"),
   "Choice three.",
  ]),
  ('Check the rest', [
   "In the lesson, let's check the others.",
   "Choice two: dermatologists may recommend it only to people without dry skin, and its users still have more dry skin? That supports the hypothesis.",
   "Choice one is about a different cream, and choice four, a mild rash, is irrelevant.",
   A("Spot it appears", P("'People who do X have more Y' → ask: maybe Y leads to X?")),
   "Whenever you see 'people who do X have more Y', ask yourself: maybe Y is what leads to X?",
  ])], T46),

# ------------------------------------------------------------------ Q5 · Hebrew ex. 5 (easy): undermine the basis of the conclusion
guided(4, 'vo-46-005', GT, SBQ,
 ["A sample question – easy.", "A new way to weaken: don't argue with the conclusion. Attack what it rests on."],
 [('Read the claim', [
   "Yigal suffers from a burning in his mouth after spicy meals. He noticed that on the evenings when he ate a vanilla pudding after dinner, the burning passed quickly.",
   "His conclusion: vanilla neutralizes the burning caused by spicy food.",
   D("Underline: on the evenings on which he ate a vanilla pudding after dinner, the burning passed quickly"),
   "His conclusion rests on that observation: pudding evenings - the burning passed quickly. That's its basis.",
   "Which does not weaken it? Find the three that weaken.",
  ]),
  ('Attack the basis', [
   "Choice four: on most evenings without the pudding, the burning also passed quickly.",
   "Wait, so the pudding evenings aren't special at all. The observation he relied on doesn't hold.",
   A("Undermining the basis appears", P('Undermining the basis: the data the conclusion rests on is shaky')),
   "That's undermining the basis of the conclusion. Every conclusion rests on some data. Shake the data, and you shake the conclusion.",
   D("Cross out choice 4"),
   "Choice three: on the pudding evenings he usually ate a smaller and less spicy dinner.",
   "So maybe the meal, not the vanilla, made the difference. Another reason. It weakens.",
   D("Cross out choice 3"),
   "Choice two: he eats the pudding straight from the refrigerator, and the burning passes faster when he eats something cold. The cold could have done it: an alternative explanation. It weakens.",
   D("Cross out choice 2"),
  ]),
  ('What remains', [
   "Choice one: Yigal also drinks coffee with vanilla almost every morning.",
   "His morning coffee says nothing about whether vanilla eases the burning in the evening. Irrelevant.",
   D("Circle choice 1"),
   "Choice one.",
   A("Check every choice appears", P("'Does not weaken': check every choice unless one is clear-cut")),
   "My recommendation in these questions: go through all the choices. The data isn't always clear-cut. If something is obvious, of course, mark it.",
  ])], T46),

# ------------------------------------------------------------------ Q6 · Hebrew ex. 6 (easy-plus): a clear-cut choice – mark it; strengthening the basis
guided(5, 'vo-46-006', GT, SBQ,
 ["A sample question – easy-plus.", "The last one, and a lesson about when to stop checking."],
 [('Read the claim', [
   "In a youth orchestra, a player who is absent from a rehearsal without notice must help the caretaker arrange the chairs and music stands at the next rehearsal.",
   "Last month the caretaker was on leave, and absences without notice were much lower than usual.",
   "The conductor's conclusion: helping the caretaker doesn't deter anyone, because the players enjoy his company.",
   D("Write: caretaker away → fewer absences → 'they like helping him'"),
   "Which fact may weaken the conductor's conclusion?",
  ]),
  ('Clear-cut: mark it', [
   "Choice two: at the beginning of last month it was announced that only players who had not been absent would perform with the orchestra abroad.",
   "Wait. At the very same moment, a new reason to show up!",
   A("Clear-cut alternative explanation → mark it appears", P('A clear-cut alternative explanation → mark it and move on')),
   "That's an alternative explanation, and a very clear one.",
   "When a choice weakens this obviously, you don't need to check the rest. Mark it.",
   D("Circle choice 2"),
   "Choice two.",
  ]),
  ('In the lesson: the rest', [
   "Choice four: the school examination period began, and they had less free time than usual.",
   "That should have raised absences, and they still fell. That negates an alternative explanation: it strengthens.",
   "Choice three: when the caretaker came back, absences rose again. That supports the conductor too.",
   "Choice one, a record two months ago, doesn't touch last month's drop.",
   A("Strengthening the basis appears", P('Strengthening the basis: the data behind the conclusion becomes even stronger')),
   "And choice three shows the mirror image of attacking the basis: new data that makes the evidence even stronger. That strengthens the basis.",
  ])], T46),
]

MEMORY = [
 dict(id='mem-strengthen-weaken', after='solve-vo-46-006', title='Strengthen and weaken: the toolkit',
  intro='Every choice adds data. Ask which way it pushes the conclusion.',
  tables=[dict(head=['Weakens', 'Strengthens'], rows=[
   ['!Alternative explanation – another reason for the same data', '!Negating an alternative explanation – the other reason is ruled out (or works against the result)'],
   ['Counterexample – the cause without the effect', 'Supporting evidence – the claimed mechanism shows up in the data'],
   ['Chicken and egg – cause and effect swapped', ''],
   ['Undermining the basis – the data behind the conclusion is shaky', 'Strengthening the basis – the data becomes even stronger'],
  ])],
  tips=['Gambler test: bet on the conclusion. Does the new fact shake your bet?',
        "'Does not weaken': cross out the 3 that weaken. The answer may be irrelevant, not only strengthening.",
        'Flip test: if the flipped fact weakens, the original strengthens.',
        'Watch whether the data is a number or a percentage.',
        'A clear-cut alternative explanation: mark it and move on.']),
]
