# Verbal Reasoning · Topic 47 · Scientific reasoning.
# Hebrew (hebverbal.txt 3549-4001, "חשיבה מדעית") gives the concepts, order, methods and verdicts;
# every question is an English bank item, used word for word. (vb-inf_mix_0118 is a bank 'assumption'
# item filed under topic 46 — it is the only design-assumption question matching the Hebrew example.)
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
  "Suppose the eight-hour group did better. An explanation: they practised more types of questions.",
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
guided(0, 'vb-inf_v2_0200', GT, SBQ,
 ["A sample question — easy.", "A basic one — to lock in the idea of equal conditions."],
 [('Read the experiment', [
   "Memory researchers: participants walk around a room, collect objects and put them in a box, which is sealed.",
   "Then half stay in the room, and half are led to a different room.",
   "Finally, everyone names as many of the objects as they can.",
   "The question: which hypothesis were they testing?",
  ]),
  ('Find X and Y', [
   "Remember: an experiment compares groups that differ in ONE thing only.",
   D("Underline: remain in the room · led to a different room"),
   A("X = what differs · Y = what is measured appears", P('X = what differs between the groups · Y = what is measured')),
   "What's different between the two halves? Only the room — the same room or a different one. That's X.",
   "What's measured? How many objects they can name. That's Y.",
   D("Write: X = same / different room · Y = recall"),
  ]),
  ('Match the hypothesis', [
   "Choice one: choosing the items yourself. Did one half choose and the other not? No — everyone collected. Cross it out.",
   D("Cross out choice 1"),
   "Choice two: how many items you store at once. Everyone did the same task. Cross it out.",
   D("Cross out choice 2"),
   "Choice four: concealing the objects. Every box was sealed — that's not the difference. Cross it out.",
   D("Cross out choice 4"),
   "Choice three: recall is better in the same surroundings where the items were memorized. That's exactly our X and Y.",
   D("Circle choice 3"),
   "Choice three.",
   A("Only the tested factor may differ appears", P('Only the tested factor may differ — everything else equal')),
   "Not a hard question — but it's the foundation: only the factor you test may differ.",
  ])], T47),

# ------------------------------------------------------------------ Q2 · Hebrew ex. 2 (medium-plus, even hard): assumptions behind a design
guided(1, 'vb-inf_mix_0118', GT, SBQ,
 ["A sample question — medium-plus, even hard.", "A different question: what did the researchers ASSUME when they designed the experiment?"],
 [('Read the design', [
   "The hypothesis: a large payment raises teenagers' motivation to improve their performance; a small payment actually lowers it.",
   "Ninety teenagers, divided at random into three groups. Lift a light weight as many times as possible in thirty seconds.",
   "Group one: ten agorot per lift. Group two: five shekels. Group three: no payment.",
   "Which is NOT one of the assumptions they used?",
   A("Everything equal except X appears", P('Design: everything equal except X — no alternative explanation')),
   "Remember: when you design an experiment, everything must be equal except the tested factor — so no alternative explanation can creep in.",
  ]),
  ('Flip each assumption', [
   "Choice three: when participants are divided at random, the groups don't differ in fitness.",
   "Flip it: if the opposite would ruin the experiment, it's an assumption.",
   "Flip it: if one group were much fitter, that alone could explain the results. So they must assume this. Cross it out.",
   D("Cross out choice 3"),
   "Choice four: ten agorot counts as a small reward, five shekels as a large one.",
   "Flip it: if the teenagers didn't see it that way, the groups wouldn't test small against large at all. An assumption. Cross it out.",
   D("Cross out choice 4"),
  ]),
  ('Generalize', [
   "Choice two: success at lifting light weights reflects success at the usual exercises at a fitness club.",
   "They test one task — but want to conclude about performance at the club in general.",
   "To generalize, they must assume the test task stands for the rest.",
   "To generalize from one task, they must assume it represents the others. An assumption. Cross it out.",
   D("Cross out choice 2"),
   "Choice one: teenagers are highly motivated by any timed physical challenge.",
   "Did they need that? No — if anything, it would blur the effect of the money.",
   D("Circle choice 1"),
   "Choice one.",
   "A slightly different question — not a simple one. Good to have seen it once.",
  ])], T47),

# ------------------------------------------------------------------ Q3 · Hebrew ex. 3 (very hard): which hypothesis can NOT explain the findings
guided(2, 'vb-inf_v2_0222', GT, SBQ,
 ["A sample question — hard. Very hard, even.", "Here we don't build a study — we explain its findings."],
 [('Two question types', [
   "There are two kinds of scientific-reasoning questions.",
   A("Type 1 appears", P('Type 1 — understanding the study: design, groups, equal conditions')),
   A("Type 2 appears", P('Type 2 — understanding the findings: what can explain them?')),
   "Type one: understanding the study — how it's built. Type two: understanding the findings. This one is type two.",
  ]),
  ('Read the finding', [
   "Onlookers improve a person's performance on a simple task — and impair it on a complex task.",
   D("Underline: simple task improves · complex task impairs"),
   "Which hypothesis does NOT explain this finding? So three of them can — we cross those out.",
   A("Cover both halves appears", P('A good explanation must cover BOTH halves of the finding')),
  ]),
  ('Test each hypothesis', [
   "Choice one: onlookers make you alert — that helps on a simple task, but on a complex one it makes you nervous. Both halves covered. It can explain. Cross it out.",
   D("Cross out choice 1"),
   "Choice three: you try to impress them — the effort helps on a simple task but overloads you on a complex one. Both halves. Cross it out.",
   D("Cross out choice 3"),
   "Choice four: onlookers hurt concentration — bad for a complex task, but simple tasks run automatically, so it actually helps. Both halves. Cross it out.",
   D("Cross out choice 4"),
  ]),
  ('What remains', [
   "Choice two: onlookers put pressure on you — but the simpler the task, the more the harm fades.",
   "Fades... but the finding says performance IMPROVES on a simple task. A harm that fades can't make you better.",
   D("Circle choice 2"),
   "Choice two.",
   A("'Can explain' = possible appears", P("'Can explain' = a possible explanation, not a proven one")),
   "And remember: 'can explain' doesn't mean it's certain — only that it's a possible explanation.",
  ])], T47),

# ------------------------------------------------------------------ Q4 · Hebrew ex. 4 (easy): conclusions given → know what to look for
guided(3, 'vb-inf_v2_0226', GT, SBQ,
 ["A sample question — easy.", "Here the research is already done — we're given its conclusions."],
 [('Read the conclusions', [
   "Researchers studied a desert plant, malaniel, on the slopes and in the wadis.",
   "Density is high in the wadis. More rain hardly changes the wadis — but raises the density on the slopes a lot.",
   D("Write: rain ↑ → slopes ↑↑ · wadis ≈ same"),
   "The question: if less rain fell in 2020 than in 2019, what's reasonable?",
  ]),
  ('Know what to look for', [
   A("Conclusions given → predict first appears", P('Conclusions given → work out what must follow, then go find it')),
   "In this type, don't test the choices one by one. Read the conclusions and work out what you expect first.",
   "Less rain: the wadis stay about the same, the slopes drop.",
   D("Write: rain ↓ → slopes ↓ · wadis same → gap ↑"),
   "So the gap between the wadis and the slopes grows.",
   "Now go straight to it: choice two — the gap was greater in 2020.",
   D("Circle choice 2"),
   "Choice two.",
   "Choice three? It's true every year — it says nothing about the rain.",
  ])], T47),

# ------------------------------------------------------------------ Q5 · Hebrew ex. 5 (medium): combine three facts into a chain
guided(4, 'vb-inf_mix_0028', GT, SBQ,
 ["A sample question — medium level.", "Here we have to combine facts into one chain."],
 [('Read the passage', [
   "NASA searches for life on other planets. Its scientists got interested in ice cauldrons — spiral cracks in ice, easy to recognize even from vast distances.",
   "They form when volcanoes erupt under ice — creating heat, humidity and a wide range of minerals.",
   "Three of the claims combine to explain NASA's interest. Which is the remaining claim?",
   A("Combine facts appears", P('Combining facts: write each one briefly, then link them by a shared term')),
  ]),
  ('Build the chain', [
   "Each choice is a long line — so write each one briefly.",
   "Choice one: the conditions aren't unique to Earth — so cauldrons may form on other planets too.",
   D("Write: cauldrons → on other planets too"),
   "Choice two: heat, humidity and minerals are ideal for life.",
   D("Write: cauldron conditions → life"),
   "Choice four: NASA can mostly only photograph planets from far away.",
   D("Write: only photos from far → spirals visible"),
   A("The chain appears", P('Seen from afar → a cauldron → conditions for life')),
   "Link them by what they share: from far away you can spot a spiral — a cauldron — which means conditions ideal for life. That's why NASA cares.",
  ]),
  ('What remains', [
   "Choice three: spiral cracks could also be formed by other factors.",
   "That doesn't explain the interest — it actually weakens it: a spiral may not mean a volcano at all.",
   D("Circle choice 3"),
   "Choice three.",
   A("Chicken and egg again appears", P('In research questions, watch for chicken and egg: cause and effect swapped')),
   "One last thing from strengthen and weaken: in research questions, the chicken-and-egg explanation — cause and effect swapped — comes up a lot.",
  ])], T47),
]

MEMORY = [
 dict(id='mem-research', after='solve-vb-inf_mix_0028', title='Scientific reasoning — the words to know',
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
