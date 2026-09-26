# Verbal Reasoning · Topic 46 · Strengthening and weakening arguments.
# Hebrew (hebverbal.txt 3145-3548, "מחזק מחליש") gives the concepts, order, methods and verdicts;
# every question is an English bank item (vcands46.txt), used word for word.
from dsl import *

T46 = 46
GT = 'Strengthen & Weaken Questions'
SBQ = ['Q1 · Support it', 'Q2 · Does NOT weaken', 'Q3 · Strengthen it', 'Q4 · Chicken and egg',
       'Q5 · Attack the basis', 'Q6 · Clear-cut']

MODULES = [
# ------------------------------------------------------------------ lesson
lesson('vr46-intro', 'Strengthen and Weaken', ['Data and conclusion', 'Which way?'], [
 dict(mode='title', title='Strengthen and Weaken', script=[
  "Strengthen and weaken questions.",
  "They sit in the inference section of the verbal chapter — and once you know the tricks, they're fast points.",
 ]),
 dict(mode='concept', active=0, title='Data and conclusion', script=[
  "Here's the setup.",
  A("Data → a conclusion drawn from it appears", T('The question gives data → and a conclusion someone drew from it', size=40)),
  "The question gives you some data — and a conclusion someone drew from that data.",
  A("Each choice adds new data appears", T('Each answer choice adds one more piece of data', size=40)),
  "Then every answer choice adds one more piece of data.",
  "Your job: understand how that new data affects the conclusion.",
 ]),
 dict(mode='concept', active=1, title='Which way?', script=[
  A("Strengthens · weakens · irrelevant appears", T('New data: strengthens · weakens · irrelevant', size=44)),
  "Three possibilities: the new data strengthens the conclusion, weakens it — or has nothing to do with it.",
  A("No proof — more or less likely appears", T('No proof here — only: more likely or less likely?', size=40)),
  "Nothing here proves or disproves anything. We only ask: does it make the conclusion more likely, or less?",
  "And read the question carefully — sometimes it's 'strengthen', sometimes 'weaken', sometimes 'does NOT weaken'.",
  "Let's start with a sample question.",
 ]),
], T46),

# ------------------------------------------------------------------ Q1 · Hebrew ex. 1 (easy-plus): support a hypothesis
guided(0, 'vb-inf_v2_0378', GT, SBQ,
 ["A sample question — easy-plus.", "A shop owner, a drop in sales — and her explanation."],
 [('Read the claim', [
   "Pnina had up-to-date music played in her clothes shop, hoping to raise sales.",
   "A few weeks later sales had fallen — and she blamed the music.",
   D("Underline: she attributed the fall to the music"),
   "That's the conclusion: the music caused the fall.",
   "The question: which fact would SUPPORT her explanation?",
   A("Goal: support 'music → sales fell' appears", P("Goal: support 'music → sales fell'")),
  ]),
  ('Irrelevant data', [
   "Choice one: her clothes are designed along unusual lines.",
   "Wait — what does that have to do with the music? Or with the fall in sales?",
   A("Not about the music or the sales → irrelevant appears", P('Not about the music or the sales → irrelevant')),
   "Nothing. It's irrelevant — it doesn't help her. Cross it out.",
   D("Cross out choice 1"),
  ]),
  ('The gambler test', [
   "Choice two: the supermarket next door plays up-to-date music and is always full of customers.",
   "A supermarket isn't a clothes shop — so it's not related? Actually, it is.",
   "It's an example going the other way: music — and a full shop.",
   A("Gambler test appears", P('Gambler test: bet on the conclusion — does the new fact shake your bet?')),
   "Here's a great trick: the gambler test. Imagine you've put money on Pnina being right.",
   "Now someone tells you: next door there's the same music, and it's packed. Feeling a bit less sure? Then it weakens.",
   A("Counterexample → weakens appears", P('Counterexample → weakens')),
   "That's a counterexample. It weakens — and we want support. Cross it out.",
   D("Cross out choice 2"),
  ]),
  ('Supporting example', [
   "Choice three: in her other shops, with no up-to-date music, sales didn't change over the same period.",
   "Two situations. Music — sales fell. No music — no change.",
   D("Write: music → sales ↓ · no music → no change"),
   A("Supporting example appears", P('Supporting example: without the cause — no effect')),
   "That's a supporting example. The difference between the shops is the music — so it strengthens her explanation.",
   D("Circle choice 3"),
   "Choice three.",
   "On the exam you mark it and move on. In the lesson, let's check the last one too.",
  ]),
  ('The last choice', [
   "Choice four: a week before her instruction, a new shop opened nearby with good clothes at low prices.",
   "Gambler test: does that shake my bet on the music? Yes — there's another reason sales could fall.",
   "So it weakens her explanation. We'll give this idea its name in the next question — it's the big one.",
  ])], T46),

# ------------------------------------------------------------------ Q2 · Hebrew ex. 2 (easy-plus): "does NOT weaken" — alternative explanation
guided(1, 'vb-inf_v2_0385', GT, SBQ,
 ["Another sample question — easy-plus.", "This time there's a twist in the question: 'does NOT weaken'."],
 [('Read the question', [
   "Mr. Cohen saw his neighbor throw out several household objects made of blue glass.",
   "His conclusion: Mr. Levi doesn't like objects made of blue glass.",
   D("Underline: does NOT weaken"),
   "Which fact does NOT weaken the conclusion?",
   "Does NOT weaken — does that mean it strengthens? Not necessarily. It could also be irrelevant.",
   A("Find the 3 that weaken appears", P("'Does NOT weaken' → find the 3 that weaken, cross them out")),
   "So here's the method: find the three that DO weaken and cross them out. The one that's left is the answer.",
  ]),
  ('Alternative explanation', [
   "Choice two: all the objects in Mr. Levi's house are made of blue glass.",
   "Wait — if everything he owns is blue glass, throwing some of it out says nothing about the color.",
   A("Alternative explanation appears", P('Alternative explanation: another reason for the same data')),
   "That's an alternative explanation — a different reason that explains the same data.",
   "Gambler test: I bet he hates blue glass... but everything in his house is blue glass? My bet just got shakier. It weakens.",
   D("Cross out choice 2"),
   "Choice three: the objects he threw away were cracked or broken.",
   "Another reason! He threw them out because they were broken — not because they're blue.",
   D("Cross out choice 3"),
  ]),
  ('The top way to weaken', [
   "Choice four: his wife recently bought a new set of household objects.",
   "Again — a different reason to throw out the old ones. Alternative explanation. Cross it out.",
   D("Cross out choice 4"),
   A("Alternative explanation = #1 way to weaken appears", P('Alternative explanation = the most common way to weaken')),
   "Alternative explanation is the most common way to weaken in these questions. Very, very important to understand.",
   "We don't know which reason is the true one. But just offering another reason weakens his conclusion.",
  ]),
  ('What remains', [
   "Choice one: Mr. Levi received the blue glass objects a week before his birthday.",
   "When he received them — does that tell us why he threw them out? No.",
   A("Irrelevant → does not weaken appears", P('Irrelevant → does NOT weaken')),
   "Irrelevant. So it does NOT weaken.",
   D("Circle choice 1"),
   "Choice one.",
   A("Number vs percentage appears", P('Watch the data: a number or a percentage?')),
   "One more tip for these questions: watch whether the data gives a number or a percentage.",
   "A place with far more customers will have more complaints — the number goes up, while the percentage may stay the same. Another reason, another alternative explanation.",
  ])], T46),

# ------------------------------------------------------------------ Q3 · Hebrew ex. 3 (medium): negate an alternative explanation · flip it
guided(2, 'vb-inf_v2_0366', GT, SBQ,
 ["A sample question — medium level.", "Now the other side: how do you STRENGTHEN a conclusion?"],
 [('Read the study', [
   "Dr. Mor had two groups solve the same kind of crossword together: a group of four and a group of ten.",
   "The group of ten completed far more clues.",
   "Her hypothesis: the size of a group influences its success.",
   D("Underline: the size of a group influences its success"),
   "Which claim strengthens her hypothesis?",
  ]),
  ('Rival explanations', [
   "Choice three: one member of the ten had seen the crossword before and knew answers in advance.",
   "Gambler test — that's another reason the ten did better. An alternative explanation. It weakens.",
   D("Cross out choice 3"),
   "Choice four: the crossword the four got was noticeably harder.",
   "Another reason — the four had it harder. It weakens.",
   D("Cross out choice 4"),
   "Choice two: six of the ten left before the group began.",
   "So it was really four against four — size can't be the reason. It weakens.",
   D("Cross out choice 2"),
  ]),
  ('Negate the alternative', [
   "Choice one: the four were experienced solvers; the ten had rarely tried a crossword.",
   "Experience — that could have been an alternative explanation. But look which way it points.",
   "The experienced group LOST. The bigger group won — even though it had less experience.",
   A("Negating an alternative explanation → strengthens appears", P('Negating an alternative explanation → strengthens')),
   "That's negating an alternative explanation: the other possible reason is ruled out — it even works against the result, and the result still happened.",
   "It's the main way to strengthen — just as the alternative explanation is the main way to weaken.",
  ]),
  ('Flip the fact', [
   "Negating an alternative explanation is usually harder to spot. Here's a trick many students find easier.",
   A("Flip the fact appears", P('Flip it: if the flipped fact weakens → the original strengthens')),
   "Flip the fact. Suppose the TEN were the experienced solvers.",
   "Then we'd say: they won because of experience, not because of size. That weakens.",
   "If the flipped version weakens — the original strengthens.",
   D("Circle choice 1"),
   "Choice one.",
  ])], T46),

# ------------------------------------------------------------------ Q4 · Hebrew ex. 4 (medium-plus): a type of alternative explanation — chicken and egg
guided(3, 'vb-inf_v2_0382', GT, SBQ,
 ["A sample question — medium-plus.", "Alternative explanations come in types. Here's one you'll meet again and again."],
 [('Read the claim', [
   "Given: among people who take the drug Cyclodin, the share with high blood pressure is higher than in the general population.",
   "The supposition: high blood pressure is a side effect of Cyclodin.",
   D("Write: Cyclodin → high blood pressure"),
   "Cause: the drug. Effect: high blood pressure.",
   "Which data would weaken the supposition?",
  ]),
  ('Chicken and egg', [
   "Choice one: Cyclodin is a drug for headaches caused by high blood pressure.",
   "Wait — so who takes Cyclodin? People who ALREADY have high blood pressure!",
   D("Draw the arrow the other way: high blood pressure → Cyclodin"),
   A("Chicken and egg appears", P('Chicken and egg: cause and effect swapped')),
   "Chicken and egg. What came first? The supposition says the drug came first. This choice says the blood pressure came first.",
   "That's an alternative explanation of a special type: cause and effect swapped. It weakens.",
   D("Circle choice 1"),
   "Choice one.",
  ]),
  ('Check the rest', [
   "In the lesson, let's check the others.",
   "Choice three: doctors prescribe it only to people WITHOUT high blood pressure — and they still end up with more of it? That supports the supposition.",
   "Choice two is about a different drug, and choice four — stomach pain — is irrelevant.",
   A("Spot it appears", P("'People who do X have more Y' → ask: maybe Y leads to X?")),
   "Whenever you see 'people who do X have more Y', ask yourself: maybe Y is what leads to X?",
  ])], T46),

# ------------------------------------------------------------------ Q5 · Hebrew ex. 5 (easy): undermine the basis of the conclusion
guided(4, 'vb-inf_v2_0387', GT, SBQ,
 ["A sample question — easy.", "A new way to weaken: don't argue with the conclusion — attack what it rests on."],
 [('Read the claim', [
   "Oded drank a glass of wine at a party and felt dizzy. An hour later he drank 'El Abismo' — and the dizziness passed.",
   "His conclusion: licorice, a substance in 'El Abismo', neutralizes the effect of alcohol.",
   D("Underline: drank a glass of wine … felt dizzy · drank 'El Abismo' … the dizziness pass"),
   "His conclusion rests on those two facts: the alcohol made him dizzy, and the drink made it pass. That's its basis.",
   "Which does NOT weaken it? Find the three that weaken.",
  ]),
  ('Attack the basis', [
   "Choice three: the wine had a negligible amount of alcohol — Oded is allergic to that grape, and the allergy shows itself in dizziness.",
   "Wait — so the alcohol never made him dizzy at all. The fact he relied on isn't true.",
   A("Undermining the basis appears", P('Undermining the basis: the data the conclusion rests on is shaky')),
   "That's undermining the basis of the conclusion. Every conclusion rests on some data. Shake the data — and you shake the conclusion.",
   D("Cross out choice 3"),
   "Choice two: the effect of one glass on a man of Oded's weight passes after half an hour. He drank 'El Abismo' an hour later.",
   "So 'the drink made the dizziness pass' is shaky too — by then it was passing anyway. It weakens.",
   D("Cross out choice 2"),
   "Choice one: 'El Abismo' contains a lot of sugar, which helps dispel dizziness. Another substance could have done it — an alternative explanation. It weakens.",
   D("Cross out choice 1"),
  ]),
  ('What remains', [
   "Choice four: Oded drinks a licorice-rich drink almost every day, and it has never made him dizzy.",
   "Whether licorice causes dizziness says nothing about whether it removes the dizziness of alcohol. Irrelevant.",
   D("Circle choice 4"),
   "Choice four.",
   A("Check every choice appears", P("'Does NOT weaken': check every choice unless one is clear-cut")),
   "My recommendation in these questions: go through all the choices — the data isn't always clear-cut. If something is obvious, of course, mark it.",
  ])], T46),

# ------------------------------------------------------------------ Q6 · Hebrew ex. 6 (easy-plus): a clear-cut choice — mark it; strengthening the basis
guided(5, 'vb-inf_v2_0369', GT, SBQ,
 ["A sample question — easy-plus.", "The last one — and a lesson about when to stop checking."],
 [('Read the claim', [
   "Last week a school introduced a new punishment for lateness: sitting in the corridor outside the principal's office.",
   "In the days that followed, latenesses fell sharply.",
   "The secretary's conclusion: the new punishment deters pupils.",
   D("Write: new punishment → fewer latenesses"),
   "Which fact would weaken her conclusion?",
  ]),
  ('Clear-cut: mark it', [
   "Choice one: at the start of last week, the school announced a prize for the class with the fewest disciplinary offenses.",
   "Wait — at the very same moment, a new reason to be on time!",
   A("Clear-cut alternative explanation → mark it appears", P('A clear-cut alternative explanation → mark it and move on')),
   "That's an alternative explanation — and a very clear one.",
   "When a choice weakens this obviously, you don't need to check the rest. Mark it.",
   D("Circle choice 1"),
   "Choice one.",
  ]),
  ('In the lesson: the rest', [
   "Choice four: daylight saving time began, which makes it harder to get up on time.",
   "That should have RAISED latenesses — and they still fell. That negates an alternative explanation: it strengthens.",
   "Choices two and three are about the old punishment — they don't touch last week's drop.",
   A("Strengthening the basis appears", P('Strengthening the basis: the data behind the conclusion becomes even stronger')),
   "And the mirror image of attacking the basis: new data that makes the evidence even stronger — that strengthens the basis.",
  ])], T46),
]

MEMORY = [
 dict(id='mem-strengthen-weaken', after='solve-vb-inf_v2_0369', title='Strengthen and weaken — the toolkit',
  intro='Every choice adds data. Ask which way it pushes the conclusion.',
  tables=[dict(head=['Weakens', 'Strengthens'], rows=[
   ['!Alternative explanation — another reason for the same data', '!Negating an alternative explanation — the other reason is ruled out (or works against the result)'],
   ['Counterexample — the cause without the effect', 'Supporting example — no cause, no effect'],
   ['Chicken and egg — cause and effect swapped', ''],
   ['Undermining the basis — the data behind the conclusion is shaky', 'Strengthening the basis — the data becomes even stronger'],
  ])],
  tips=['Gambler test: bet on the conclusion — does the new fact shake your bet?',
        "'Does NOT weaken': cross out the 3 that weaken — the answer may be irrelevant, not only strengthening.",
        'Flip test: if the flipped fact weakens, the original strengthens.',
        'Watch whether the data is a number or a percentage.',
        'A clear-cut alternative explanation: mark it and move on.']),
]
