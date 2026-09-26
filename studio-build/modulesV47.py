# Verbal Reasoning · Topic 47 · Scientific reasoning.
# Hebrew (hebverbal.txt 3549-4001, "חשיבה מדעית") gives the concepts, order, methods and verdicts;
# every guided question is an original written for the course (content/verbal_originals_C.json, vo-47-…).
from dsl import *

T47 = 47
GT = 'Research Questions'
SBQ = ['Q1 · Find X and Y', 'Q2 · Assumptions', 'Q3 · Explain findings', 'Q4 · Use conclusions',
       'Q5 · Combine facts']

MODULES = [
# ------------------------------------------------------------------ lesson
lesson('vr47-research', 'How Research Works',
 ['Where these appear', 'Hypothesis: X → Y', 'Compare groups', 'Everything else equal', 'Link to strengthen',
  'Control group', 'Two kinds of control', 'Results → conclusion', 'Explaining findings', 'Recap'], [
 dict(mode='title', title='How Research Works', script=[
  "Scientific reasoning.",
  "Hypotheses, experiments, studies, findings, conclusions — before we solve questions, a short introduction to how research works.",
 ]),
 dict(mode='concept', active=0, title='Where these appear', script=[
  A("Inside the inference section appears", T('Part of the inference section of the verbal chapter', size=40)),
  "These questions appear inside the inference section of the verbal chapter.",
  A("Hypotheses · experiments · findings · conclusions appears", T('Hypotheses · experiments · studies · findings · conclusions', size=40)),
  "Because the world of experiments is less familiar to many students, let's first understand what an experiment and a hypothesis really are.",
 ]),
 dict(mode='concept', active=1, title='Hypothesis: X → Y', src='hebrew', script=[
  "We always, always start from a hypothesis.",
  A("Hypothesis = cause and effect appears", T('A hypothesis = cause and effect', size=44)),
  "Not 'I suppose there's life on Mars'. In experiments, a hypothesis is built as cause and effect.",
  A("If X changes → Y changes appears", T('If we change X → Y grows / shrinks / changes', size=40)),
  "If we add, change, increase or decrease X — then Y grows, shrinks, or changes.",
  A("X = the factor we change · Y = the result we measure appears", T('X = the factor we change · Y = the result we measure', size=36)),
  "X is the factor we change. Y is the result — what we check to see how it was affected.",
  "Example: how do our study hours affect our exam score? Hypothesis: more hours — a higher score.",
 ]),
 dict(mode='concept', active=2, title='Compare groups', src='hebrew', script=[
  "Now we can design an experiment.",
  A("Compare groups appears", T('An experiment compares groups', size=44)),
  "To design an experiment, we compare groups. Why? Because 'Y grows' is relative — grows compared with what?",
  A("X1: 4 hours a day · X2: 8 hours a day appears", T('Group X1: 4 hours a day · Group X2: 8 hours a day', size=38)),
  "So we make two groups: one studies four hours a day, the other eight.",
 ]),
 dict(mode='concept', active=3, title='Everything else equal', src='hebrew', script=[
  A("All conditions equal — except X appears", T('All conditions identical — except the factor we test', size=40)),
  "Very, very important — one of the most basic ideas, and it comes back in many exam questions:",
  "all the conditions in the groups must be identical, except the factor we're testing.",
  "Why? Suppose the four-hour group sleeps three hours a night and the eight-hour group sleeps nine.",
  A("Otherwise → alternative explanation appears", T('Otherwise → an alternative explanation', size=40)),
  "Wait — now there's an alternative explanation. Maybe it wasn't the studying — maybe it was the sleep.",
 ]),
 dict(mode='concept', active=4, title='Link to strengthen', script=[
  A("Strengthen / weaken is part of scientific reasoning appears", T('Strengthen / weaken is a sub-topic of scientific reasoning', size=40)),
  "See how it connects to strengthen and weaken? Many of those questions are really about research:",
  "'In a certain study they did this — what strengthens, what weakens?'",
  "Strengthen and weaken is really a sub-topic of scientific reasoning.",
 ]),
 dict(mode='concept', active=5, title='Control group', src='hebrew', script=[
  A("Control group appears", T('The control group = the regular group we compare with', size=40)),
  "In the experiment, one group is the one we're testing — say, the eight-hour group.",
  "The other is called the control group: the regular group, the four hours. We check whether raising the hours helps.",
 ]),
 dict(mode='concept', active=6, title='Two kinds of control', script=[
  A("X absent appears", T('Control 1: X absent — e.g. no fertilizer at all', size=40)),
  "There are two kinds of control. One: X is absent. Say we test a fertilizer — one group of plants gets no fertilizer at all.",
  A("X at a different level appears", T('Control 2: X at a different level — e.g. less fertilizer', size=40)),
  "Two: X at a different level — both groups get fertilizer, in different amounts.",
 ]),
 dict(mode='concept', active=7, title='Results → conclusion', script=[
  A("Results support or contradict appears", T('Results: support the hypothesis — or contradict it', size=40)),
  "We run the experiment and get results. They either support the hypothesis — or contradict it.",
  A("Supported hypothesis → conclusion appears", T('Supported → the hypothesis becomes the conclusion', size=40)),
  "When the finding supports it, the hypothesis becomes our conclusion.",
 ]),
 dict(mode='concept', active=8, title='Explaining findings', src='hebrew', script=[
  A("Explanation of the findings appears", T('Explaining the findings: why did it come out this way?', size=40)),
  "One more link in the chain: explaining the findings.",
  "Suppose the eight-hour group did better. An explanation: they practiced more types of questions.",
  "And if they did worse? Maybe eight hours a day exhausted them. Explaining findings is a question type too.",
 ]),
 dict(mode='concept', active=9, title='Recap', script=[
  A("Recap chain appears", T('Hypothesis → experiment (groups, only X differs) → results → support or not', size=36)),
  "Quick recap. I form a hypothesis. I run an experiment: two groups, and only the tested factor differs — everything else equal.",
  "I get results — they support what I supposed, or they don't.",
  "Let's start with the first question.",
 ]),
], T47),

# ------------------------------------------------------------------ Q1 · Hebrew ex. 1 (easy): only X differs
guided(0, 'vo-47-001', GT, SBQ,
 ["A sample question — easy.", "A basic one — to lock in the idea of equal conditions."],
 [('Read the experiment', [
   "Consumer researchers: every participant gets a kit for a small wooden shelf and an instruction booklet.",
   "Half assemble the shelf on their own. The other half watch while a member of the research team assembles it for them.",
   "Then every shelf is wrapped in paper, and each participant states the highest price they'd pay for their shelf.",
   "The question: which hypothesis did the researchers test?",
  ]),
  ('Find X and Y', [
   "Remember: an experiment compares groups that differ in one thing only.",
   D("Underline: assemble the shelf on their own · watched while … assembled it for them"),
   A("X = what differs · Y = what is measured appears", P('X = what differs between the groups · Y = what is measured')),
   "What's different between the two halves? Only who built the shelf — the participant, or someone else. That's X.",
   "What's measured? The highest price they'd pay. That's Y.",
   D("Write: X = built it yourself / built for you · Y = price"),
  ]),
  ('Match the hypothesis', [
   "Choice one: a product you can examine closely versus one hidden from view. But every shelf was wrapped — that's not the difference. Cross it out.",
   D("Cross out choice 1"),
   "Choice three: clearer instructions. Everyone got the same booklet. Cross it out.",
   D("Cross out choice 3"),
   "Choice four: a product you chose yourself. Did one half choose and the other not? No — nobody chose anything. Cross it out.",
   D("Cross out choice 4"),
   "Choice two: people value an object more if they built it themselves than if someone else built it for them. That's exactly our X and Y.",
   D("Circle choice 2"),
   "Choice two.",
   A("Only the tested factor may differ appears", P('Only the tested factor may differ — everything else equal')),
   "Not a hard question — but it's the foundation: only the factor you test may differ.",
  ])], T47),

# ------------------------------------------------------------------ Q2 · Hebrew ex. 2 (medium-plus, even hard): assumptions behind a design
guided(1, 'vo-47-002', GT, SBQ,
 ["A sample question — medium-plus, even hard.", "A different question: we judge how a study was designed — and whether it can really test the belief."],
 [('Read the design', [
   "For many years, farmers in a certain valley believed the soil was too salty for earthworms to live in — so earthworms couldn't be the cause of the tunnels in their fields.",
   D("Underline: the valley's soil was too salty for earthworms to live in"),
   "A later study showed the belief was wrong. Which of the following cannot be that study?",
   "So three of the studies could show it's wrong — we cross those out.",
   A("Everything equal except X appears", P('Design: everything equal except X — no alternative explanation')),
   "Remember: when you design an experiment, everything must be equal except the tested factor — so no alternative explanation can creep in.",
  ]),
  ('Flip each study', [
   "Flip it: imagine the study came out positive. Would the old belief be broken? If yes — it could be the study.",
   A("Positive result breaks the belief → it could be the one appears", P('Imagine a positive result: does it break the belief? → it could be the one')),
   "Choice two: dig up soil from the valley's fields — earthworms found. In the real soil, salt and all, earthworms live. The belief is broken. Cross it out.",
   D("Cross out choice 2"),
   "Choice three: prepare soil as salty as the valley's — earthworms live in it. Broken again. Cross it out.",
   D("Cross out choice 3"),
  ]),
  ('Generalize', [
   "Choice four: a substance that kills only earthworms — and new tunnels stop appearing. So earthworms were there, digging. Broken. Cross it out.",
   D("Cross out choice 4"),
   "Choice one: wash the salt out of a field with fresh water — and then check for earthworms.",
   "They changed the very thing the belief is about. To generalize to the real valley, the test must stand for the real valley.",
   "Earthworms in a field whose salt was washed out say nothing about the salty soil.",
   D("Circle choice 1"),
   "Choice one.",
   "A slightly different question — not a simple one. Good to have seen it once.",
  ])], T47),

# ------------------------------------------------------------------ Q3 · Hebrew ex. 3 (very hard): which hypothesis does not explain the findings
guided(2, 'vo-47-003', GT, SBQ,
 ["A sample question — hard. Very hard, even.", "Here we don't build a study — we explain its findings."],
 [('Two question types', [
   "There are two kinds of scientific-reasoning questions.",
   A("Type 1 appears", P('Type 1 — understanding the study: design, groups, equal conditions')),
   A("Type 2 appears", P('Type 2 — understanding the findings: what can explain them?')),
   "Type one: understanding the study — how it's built. Type two: understanding the findings. This one is type two.",
  ]),
  ('Read the finding', [
   "With background music, people do repetitive tasks better than in silence — and tasks that need careful reading worse.",
   D("Underline: repetitive tasks better · careful reading worse"),
   "Which hypothesis does not explain this finding? So three of them can — we cross those out.",
   A("Cover both halves appears", P('A good explanation must cover both halves of the finding')),
  ]),
  ('Test each hypothesis', [
   "Choice one: music raises arousal — that keeps you awake on a repetitive task, but makes you restless when you need to read carefully. Both halves covered. It can explain. Cross it out.",
   D("Cross out choice 1"),
   "Choice two: music and reading compete for the same language resources — so reading suffers; repetitive tasks don't use them, and the music relieves boredom and keeps your pace up. Both halves. Cross it out.",
   D("Cross out choice 2"),
   "Choice four: music puts you in a good mood — that helps on tasks without much thought, but makes you process information less carefully, which harms reading. Both halves. Cross it out.",
   D("Cross out choice 4"),
  ]),
  ('What remains', [
   "Choice three: music diverts attention and harms performance — but on a repetitive task the harm becomes negligible.",
   "Negligible... but the finding says performance improves on repetitive tasks. A harm that becomes negligible can't make you better.",
   D("Circle choice 3"),
   "Choice three.",
   A("'Can explain' = possible appears", P("'Can explain' = a possible explanation, not a proven one")),
   "And remember: 'can explain' doesn't mean it's certain — only that it's a possible explanation.",
  ])], T47),

# ------------------------------------------------------------------ Q4 · Hebrew ex. 4 (easy): conclusions given → know what to look for
guided(3, 'vo-47-004', GT, SBQ,
 ["A sample question — easy.", "Here the research is already done — we're given its conclusions."],
 [('Read the conclusions', [
   "An ecologist counted seabird nests in two parts of an island: the cliffs and the sandy shore.",
   "There are many more nests on the cliffs. More foxes hardly change the cliffs — but make the nests on the shore drop sharply.",
   D("Write: foxes ↑ → shore ↓↓ · cliffs ≈ same"),
   "The question: if there were more foxes in 2023 than in 2022, what's reasonable?",
  ]),
  ('Know what to look for', [
   A("Conclusions given → predict first appears", P('Conclusions given → work out what must follow, then go find it')),
   "In this type, don't test the choices one by one. Read the conclusions and work out what you expect first.",
   "More foxes: the cliffs stay about the same, the shore drops.",
   D("Write: foxes ↑ → shore ↓ · cliffs same → gap ↑"),
   "So the gap between the cliffs and the shore grows.",
   "Now go straight to it: choice four — the gap was greater in 2023.",
   D("Circle choice 4"),
   "Choice four.",
   "Choice two? More nests on the shore than on the cliffs — the cliffs have far more, and more foxes only widen that.",
  ])], T47),

# ------------------------------------------------------------------ Q5 · Hebrew ex. 5 (medium): combine facts into a chain
guided(4, 'vo-47-005', GT, SBQ,
 ["A sample question — medium level.", "Here we have to combine facts into one chain."],
 [('Read the paragraph', [
   "A virus that attacks cucumber plants is carried from plant to plant by a small beetle.",
   "When the beetle feeds on an infected plant, virus particles stick to its mouthparts — and it leaves them on the next plant.",
   "If one plant receives particles from several different infected plants, they exchange genetic material inside it — new forms of the virus, some able to overcome the plants' resistance.",
   "Why do such forms arise sooner where the virus is common than where it is rare? Which explanation fits?",
   A("Combine facts appears", P('Combining facts: write each one briefly, then link them by a shared term')),
  ]),
  ('Build the chain', [
   "Each fact is a long line — so write each one briefly.",
   D("Write: one plant gets particles from several infected plants"),
   D("Write: particles together in one plant → genetic exchange → new forms"),
   D("Write: new forms → some overcome resistance"),
   A("The chain appears", P('particles from several plants → exchange → new forms → resistance overcome')),
   "Link them by what they share — the particles meeting in one plant. Several sources, exchange, new forms, resistance overcome. That's the whole chain.",
  ]),
  ('Find the start', [
   "Now look for the choice that starts the chain.",
   "Choice one: farmers grow older varieties never bred for resistance. That's a new fact from outside the paragraph, and it doesn't lead to forms that overcome resistance. Out.",
   D("Cross out choice 1"),
   "Choice two: each beetle feeds on only one plant in its life. Then it never carries particles to another plant. That breaks the chain. Out.",
   D("Cross out choice 2"),
   "Choice four: a larger beetle population. But does each plant get particles from several infected plants? Not necessarily. A step short.",
   D("Cross out choice 4"),
   "Choice three: a single plant is more likely to be fed on by beetles carrying particles from several different infected plants. That's the first link of our chain.",
   D("Circle choice 3"),
   "Choice three.",
   A("Chicken and egg again appears", P('In research questions, watch for chicken and egg: cause and effect swapped')),
   "One last thing from strengthen and weaken: in research questions, the chicken-and-egg explanation — cause and effect swapped — comes up a lot.",
  ])], T47),
]

MEMORY = [
 dict(id='mem-research', after='solve-vo-47-005', title='Scientific reasoning — the words to know',
  intro='Every study follows one chain: hypothesis → experiment → results → conclusion.',
  tables=[dict(head=['Term', 'What it means'], rows=[
   ['!Hypothesis', 'Cause and effect: if X changes, Y changes'],
   ['X · Y', 'X = the factor we change · Y = the result we measure'],
   ['!Equal conditions', 'Groups identical except X — otherwise an alternative explanation'],
   ['Control group', 'The comparison group: X absent, or X at a different level'],
   ['Finding', 'The result — supports the hypothesis or contradicts it'],
   ['Conclusion', 'A hypothesis the findings support'],
   ['Explaining findings', 'Why the results came out as they did'],
  ])],
  tips=['Two question types: understanding the study · understanding the findings.',
        "Assumptions: flip it — if the opposite would ruin the experiment, it's an assumption.",
        'Conclusions given: work out what must follow before reading the choices.',
        'An explanation must cover every part of the finding.']),
]
