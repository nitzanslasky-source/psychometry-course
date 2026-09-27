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
   "Researchers gave every participant a box of chocolates.",
   "Half were told the chocolates were made by hand in a small workshop. The other half were told they were made in a large factory. In fact, all the chocolates were the same.",
   "After tasting them, each participant rated how tasty they were.",
   "The question: which hypothesis did the researchers test?",
  ]),
  ('Find X and Y', [
   "Remember: an experiment compares groups that differ in one thing only.",
   D("Underline: were told … made by hand in a small workshop · were told … made in a large factory"),
   A("X = what differs · Y = what is measured appears", P('X = what differs between the groups · Y = what is measured')),
   "What's different between the two halves? Only what they were told about how the chocolates were made. That's X.",
   "What's measured? How tasty the chocolates seemed. That's Y.",
   D("Write: X = what they were told · Y = how tasty"),
  ]),
  ('Match the hypothesis', [
   "Choice one: chocolates in a box versus loose. Everyone got a box — that's not the difference. Cross it out.",
   D("Cross out choice 1"),
   "Choice three: handmade food really is tastier. But the chocolates were the same! The only difference was what people were told. Cross it out.",
   D("Cross out choice 3"),
   "Choice four: tasting before rating. Everyone tasted. Cross it out.",
   D("Cross out choice 4"),
   "Choice two: what people are told about how a food was made influences how tasty it seems to them. That's exactly our X and Y.",
   D("Circle choice 2"),
   "Choice two.",
   A("Only the tested factor may differ appears", P('Only the tested factor may differ — everything else equal')),
   "Not a hard question — but it's the foundation: only the factor you test may differ.",
  ])], T47),

# ------------------------------------------------------------------ Q2 · Hebrew ex. 2 (medium-plus, even hard): assumptions behind a design
guided(1, 'vo-47-002', GT, SBQ,
 ["A sample question — medium-plus, even hard.", "A different question: we judge how a study was designed — and whether it can really test the belief."],
 [('Read the design', [
   "For many years, the farmers of a certain village believed that the dark spots on their figs are caused by the morning fog — and that the tiny wasps in the orchards in the same season play no part in this.",
   D("Underline: caused by the morning fog · the tiny wasps … play no part in this"),
   "Later observations showed the belief was wrong. Which of the following results would not have shown that?",
   "So three of the results would show it's wrong — we cross those out.",
   A("Everything equal except X appears", P('Design: everything equal except X — no alternative explanation')),
   "Remember: when you design an experiment, everything must be equal except the tested factor — so no alternative explanation can creep in.",
  ]),
  ('Test each result', [
   "Ask of each result: does it break the belief? If yes — it could be one of those observations.",
   A("Does the result break the belief? → it could be one of them appears", P('Does this result break the belief? → then it could be one of them')),
   "Choice two: a year when a late frost kept the wasps away — almost no spots, though the fog was as usual. Fog, but no spots. The belief is broken. Cross it out.",
   D("Cross out choice 2"),
   "Choice three: an orchard on the slope of the mountain, never any morning fog — and many figs had spots. Spots without fog — broken again. Cross it out.",
   D("Cross out choice 3"),
  ]),
  ('Generalize', [
   "Choice four: a farmer covered part of his trees with fine nets, and spots appeared only on the uncovered trees. The nets keep out the wasps, not the fog. Broken. Cross it out.",
   D("Cross out choice 4"),
   "Choice one: figs that were picked and eaten before the season of fog had no spots.",
   "No fog, no spots — that's exactly what the belief itself predicts. The result is about figs the belief doesn't even talk about.",
   "To break a belief, the test must stand for the very case the belief is about.",
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
   "Choice one: music arouses the listener — that prevents sleepiness in monotonous work, but disturbs the concentration careful reading needs. Both halves covered. It can explain. Cross it out.",
   D("Cross out choice 1"),
   "Choice two: music uses the same abilities as reading — so reading suffers; in monotonous work the music reduces boredom. Both halves. Cross it out.",
   D("Cross out choice 2"),
   "Choice four: music improves the mood — that helps in simple tasks, but makes people read less carefully. Both halves. Cross it out.",
   D("Cross out choice 4"),
  ]),
  ('What remains', [
   "Choice three: music draws attention away and harms every task — but in a monotonous task the harm is smaller.",
   "Smaller... but the finding says performance improves on monotonous tasks. A smaller harm is still a harm — it can't make you better.",
   D("Circle choice 3"),
   "Choice three.",
   A("'Can explain' = possible appears", P("'Can explain' = a possible explanation, not a proven one")),
   "And remember: 'can explain' doesn't mean it's certain — only that it's a possible explanation.",
  ])], T47),

# ------------------------------------------------------------------ Q4 · Hebrew ex. 4 (easy): conclusions given → know what to look for
guided(3, 'vo-47-004', GT, SBQ,
 ["A sample question — easy.", "Here the research is already done — we're given its conclusions."],
 [('Read the conclusions', [
   "The ecologist Harari counted tern nests for twelve years in two parts of an island: the cliffs and the sandy shore.",
   "There are many more nests on the cliffs. More foxes hardly change the cliffs — but make the nests on the shore drop sharply.",
   D("Write: foxes ↑ → shore ↓↓ · cliffs ≈ same"),
   "The question: if there were more foxes in 1987 than in 1986, what's likely?",
  ]),
  ('Know what to look for', [
   A("Conclusions given → predict first appears", P('Conclusions given → work out what must follow, then go find it')),
   "In this type, don't test the choices one by one. Read the conclusions and work out what you expect first.",
   "More foxes: the cliffs stay about the same, the shore drops.",
   D("Write: foxes ↑ → shore ↓ · cliffs same → gap ↑"),
   "So the gap between the cliffs and the shore grows.",
   "Now go straight to it: choice four — the gap was greater in 1987.",
   D("Circle choice 4"),
   "Choice four.",
   "Choice two? More nests on the shore than on the cliffs — the cliffs have far more, and more foxes only widen that.",
  ])], T47),

# ------------------------------------------------------------------ Q5 · Hebrew ex. 5 (medium): combine facts into a chain
guided(4, 'vo-47-005', GT, SBQ,
 ["A sample question — medium level.", "Here we have to combine facts into one chain."],
 [('Read the paragraph', [
   "Researchers followed a certain desert shrub for several years. Its seeds have a hard coat, and they germinate only after passing through the digestive system of a gazelle, which softens the coat.",
   "The shrub bears fruit once a year, at the beginning of summer, and the fruit falls within about three weeks.",
   "And gazelles prefer grass. They eat the fruit of the shrub only when grass is hard to find.",
   "In which year is it most likely that many new shrubs will begin to grow? Which answer fits?",
   A("Combine facts appears", P('Combining facts: write each one briefly, then link them by a shared term')),
  ]),
  ('Build the chain', [
   "Each fact is a long line — so write each one briefly.",
   D("Write: little grass → gazelles eat the fruit"),
   D("Write: fruit only at the beginning of summer"),
   D("Write: seeds through a gazelle → coat softened → they germinate"),
   A("The chain appears", P('little grass at the beginning of summer → gazelles eat the fruit → seeds pass through → new shrubs')),
   "Link them by what they share — the gazelle eating the fruit. Little grass while the fruit is there, the gazelles eat it, the seeds pass through, new shrubs grow. That's the whole chain.",
  ]),
  ('Find the start', [
   "Now look for the choice that starts the chain.",
   "Choice one: the shrubs bore more fruit than usual. But will the gazelles eat it? Only if grass is hard to find. A step short. Out.",
   D("Cross out choice 1"),
   "Choice two: little grass at the end of winter. But there's no fruit at the end of winter — it comes at the beginning of summer. The timing breaks the chain. Out.",
   D("Cross out choice 2"),
   "Choice four: more gazelles than in other years. But with plenty of grass, they still won't touch the fruit. A step short.",
   D("Cross out choice 4"),
   "Choice three: little grass at the beginning of summer — just when the fruit is there. That's the first link of our chain.",
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
